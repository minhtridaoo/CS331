"""Nhánh P1: B2 nhưng mẫu tự chọn được CLIP kiểm trước lượt 2 (kế hoạch Trí §3.2–3.4). Không sửa run_b2_frozen.py.

Mỗi query: lượt 1 (= B0) -> tối đa M ứng viên (score > 0.23) -> CLIP cosine từng ứng viên -> với mỗi tau_pseudo,
giữ ứng viên có cosine >= tau, lấy tối đa 3 theo điểm CountGD -> lượt 2 với các mẫu đó; không còn mẫu thì trả B0.
Nhiều tau dùng chung một lượt 1; cùng một bộ mẫu thì lượt 2 chỉ chạy một lần. Trước mỗi lượt 2 trạng thái RNG được
đưa về đúng lúc vừa xong lượt 1, như trong B2.

--replay-b2 thêm biến thể B2 (top 3 gốc, không CLIP) để kiểm tái hiện; --b2-reference so nó với B2 đã lưu.
Ngưỡng tau_pseudo và M chỉ được chọn trên dev (kế hoạch §3.2, §5); không chỉnh trên p4_unseen_v1.

Example (from CS331 root):
  python experiments/countgdpp/run_b2_verified_pseudo.py --inputs experiments/countgdpp/m4_inputs/first5_inputs.jsonl \
      --run-id p1_pilot_YYYYMMDD --tau-pseudo 0.22 0.24 0.26 0.28 --replay-b2 \
      --b0-reference results/countgdpp/m4_first5_b0/predictions.jsonl \
      --b2-reference results/countgdpp/b2_two_images_20261015/predictions.jsonl results/countgdpp/b2_remaining3_20261015/predictions.jsonl
"""
import argparse
import ast
import json
import os
import re
import sys
import time
from pathlib import Path
from PIL import Image
from run_b0_batch import ROOT, REPO, SOURCE_HASH, sha, load_inputs, project_path
from run_b2_pilot import select_pseudo, draw_boxes
from pseudo_clip_verifier import MODEL_ID, REVISION, TEMPLATE, ClipVerifier, choose, top_candidates

TAU = .23
MAX_PSEUDO = 3


def read_predictions(paths):
    out = {}
    for p in paths:
        for row in map(json.loads, project_path(p).read_text(encoding="utf-8").splitlines()):
            key = (row["image_id"], row["query_id"])
            if key in out:
                raise ValueError(f"Duplicate reference row {key}")
            out[key] = row
    return out


def compare(np, boxes, scores, ref):
    """Khớp như run_b2_frozen (box atol .001, score atol 1e-5); kèm độ lệch lớn nhất khi cùng số khung."""
    b, rb = np.asarray(boxes).reshape(-1, 4), np.asarray(ref["final_boxes"]).reshape(-1, 4)
    same_n = len(b) == ref["final_count"]
    diff = dict(count=len(b), ref_count=ref["final_count"],
                max_box_diff=float(np.abs(b - rb).max()) if same_n and len(b) else None,
                max_score_diff=float(np.abs(np.asarray(scores) - np.asarray(ref["final_scores"])).max()) if same_n and len(b) else None)
    diff["matches"] = bool(same_n and np.allclose(b, rb, atol=.001, rtol=0) and np.allclose(scores, ref["final_scores"], atol=1e-5, rtol=0))
    return diff


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--inputs", required=True, help="Input-only JSONL (schema v1, no GT), path relative to CS331")
    p.add_argument("--run-id", required=True)
    p.add_argument("--tau-pseudo", type=float, nargs="+", required=True, help="CLIP cosine thresholds; choose on dev only")
    p.add_argument("--m", type=int, default=10, help="Max first-pass candidates checked by CLIP (plan §3.2: start at 10)")
    p.add_argument("--replay-b2", action="store_true", help="Also write the original B2 (top 3, no CLIP) from the same stage 1")
    p.add_argument("--b0-reference", nargs="+", help="Saved B0 predictions; stage 1 must replay exactly")
    p.add_argument("--b2-reference", nargs="+", help="Saved B2 predictions; requires --replay-b2, final must replay exactly")
    p.add_argument("--reference-mode", choices=["stop", "report"], default="stop",
                   help="stop at the first replay mismatch (default), or record the differences and continue (new GPU diagnosis only)")
    p.add_argument("--check-inputs", action="store_true", help="Validate inputs/checkpoint/source hashes, then stop before loading models")
    args = p.parse_args()
    if not re.fullmatch(r"[A-Za-z0-9_-]+", args.run_id):
        raise ValueError("Invalid run ID")
    if args.b2_reference and not args.replay_b2:
        raise ValueError("--b2-reference needs --replay-b2")
    if args.m < MAX_PSEUDO:
        raise ValueError("M must be >= 3")
    taus = sorted(set(args.tau_pseudo))
    inputs = project_path(args.inputs); rows = load_inputs(inputs)
    qids = [r["query_id"] for r in rows]
    if len(set(qids)) != len(qids):
        raise ValueError("query_id must be unique (used as job folder)")
    audit = json.loads((ROOT / "results/countgdpp/checkpoint_audit_2026-10-14.json").read_text())
    checkpoint = REPO / "checkpoints/countgd_plusplus.pth"
    if sha(checkpoint) != audit["checkpoint_sha256"] or audit.get("review_decision") != "compatible_with_pinned_B0_app":
        raise ValueError("Checkpoint audit mismatch")
    if sha(REPO / "process_folder.py") != SOURCE_HASH:
        raise ValueError("Stock source changed")
    for source, digest in audit["review_source_sha256"].items():
        if sha(REPO / source) != digest:
            raise ValueError("Reviewed model code changed")
    refs = {}
    for name, paths in (("B0", args.b0_reference), ("B2", args.b2_reference)):
        if paths:
            refs[name] = read_predictions(paths)
            if any((r["image_id"], r["query_id"]) not in refs[name] for r in rows):
                raise ValueError(f"Missing {name} reference for some input rows")
    print(f"Validated {len(rows)} queries / {len({r['image_id'] for r in rows})} images; taus={taus}; M={args.m}; "
          f"replay_b2={args.replay_b2}; references={sorted(refs)}", flush=True)
    if args.check_inputs:
        return

    out = ROOT / "results/countgdpp" / args.run_id; out.mkdir(exist_ok=False)
    variants = (["B2"] if args.replay_b2 else []) + [f"tau{t:.3f}" for t in taus]
    config = dict(status="running", variant="P1", runner="run_b2_verified_pseudo.py", scope="P1 verified pseudo-exemplars; dev only until tau/M are locked",
        inputs=rows, checkpoint_sha256=audit["checkpoint_sha256"], source_sha256=SOURCE_HASH, adapter_sha256=sha(Path(__file__)),
        verifier_sha256=sha(Path(__file__).with_name("pseudo_clip_verifier.py")), b2_adapter_sha256=sha(Path(__file__).with_name("run_b2_frozen.py")),
        input_sha256=sha(inputs), model_commit="8489f836d75eb407ae778c56cff1f72cc6f8baae", tau_sample=TAU, tau_final=TAU, max_pseudo=MAX_PSEUDO,
        m=args.m, tau_pseudo=taus, outputs={v: f"predictions_{v}.jsonl" for v in variants},
        candidates="select_pseudo rule with maximum=M; degenerate boxes kept in log with valid=false and never chosen",
        verifier=dict(model_id=MODEL_ID, revision=REVISION, template=TEMPLATE, crop="round+clamp, no padding (p4_clip_score.crop_box)"),
        choose="valid and clip_cosine >= tau, top 3 by CountGD score; none left -> stage 1 (B0), stage2_executed=false",
        rng="seed 42 before stage 1; RNG state restored to end-of-stage-1 before every stage-2 forward",
        references={k: v for k, v in (("B0", args.b0_reference), ("B2", args.b2_reference)) if v}, reference_mode=args.reference_mode,
        uses_ground_truth=False, negative_prompts=False, synthetic=False, crop=False, seed=42, resize=dict(short_side=800, max_size=1333))
    def save(): (out / "run_config.json").write_text(json.dumps(config, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    save()
    import random
    import numpy as np
    import torch
    if not torch.cuda.is_available():
        raise RuntimeError("CUDA required")
    sys.path.insert(0, str(REPO)); os.chdir(REPO)
    source = REPO / "process_folder.py"; tree = ast.parse(source.read_text())
    tree.body = [n for n in tree.body if isinstance(n, (ast.Import, ast.ImportFrom, ast.FunctionDef))]
    ns = {"__name__": "pinned_stock_definitions"}; exec(compile(tree, str(source), "exec"), ns)
    model, transform = ns["build_model_and_transforms"](ns["build_arg_parser"]().parse_args([]))
    device = torch.device("cuda"); model = model.to(device)
    clip = ClipVerifier(device)
    config.update(device=torch.cuda.get_device_name(), torch_version=torch.__version__, transformers_version=clip.transformers_version,
                  clip_resolved_revision=clip.revision, allow_tf32=dict(matmul=torch.backends.cuda.matmul.allow_tf32, cudnn=torch.backends.cudnn.allow_tf32),
                  python=sys.version, executable=sys.executable)
    save()
    original = ns["get_boxes_from_prediction"]; capture = {}
    def observe(output, text, keywords="", conf_thresh=TAU):
        returned = original(output, text, keywords, conf_thresh)
        capture.update(scores=output["pred_logits"][0].sigmoid().detach().cpu(), boxes=output["pred_boxes"][0].detach().cpu(), ids=output["input_ids"][0].detach().cpu().tolist())
        return returned
    ns["get_boxes_from_prediction"] = observe
    def predict(image, prompt, exemplars):
        prompts = {"image": image, "points": [[b[0], b[1], 2.0, b[2], b[3], 3.0] for b in exemplars]}
        b, s = ns["predict"](model, transform, image, prompt, prompts, [], [], device, TAU)
        x, y, w, h = ns["get_box_coords_from_boxes"](image, b)
        return np.stack((x, y, x + w, y + h), axis=1), s, dict(capture)
    def save_raw(path, cap):
        np.savez_compressed(path, scores=cap["scores"].numpy(), normalized_cxcywh=cap["boxes"].numpy(), input_ids=np.array(cap["ids"]))
    def rng_state():
        return torch.get_rng_state(), torch.cuda.get_rng_state_all(), np.random.get_state(), ns["random"].getstate(), random.getstate()
    def set_rng(state):
        torch.set_rng_state(state[0]); torch.cuda.set_rng_state_all(state[1]); np.random.set_state(state[2]); ns["random"].setstate(state[3]); random.setstate(state[4])

    files = {v: (out / f"predictions_{v}.jsonl").open("w", encoding="utf-8") for v in variants}
    log = (out / "candidates.jsonl").open("w", encoding="utf-8")
    failed = False; done = 0
    try:
        for i, row in enumerate(rows):
            job = out / row["query_id"]; job.mkdir()
            key = (row["image_id"], row["query_id"])
            base = dict(schema_version=1, run_id=args.run_id, image_id=row["image_id"], query_id=row["query_id"], execution_status="error",
                        final_count=None, final_boxes=[], final_scores=[], error_message=None, box_format="xyxy_pixels", image_width=None, image_height=None)
            recs = {v: dict(base, variant="B2" if v == "B2" else "P1", tau_pseudo=None if v == "B2" else float(v[3:]), m=None if v == "B2" else args.m) for v in variants}
            try:
                image = Image.open(project_path(row["image_path"])).convert("RGB")
                torch.manual_seed(42); np.random.seed(42); ns["random"].seed(42)
                torch.cuda.synchronize(); start = time.perf_counter()
                b0, s0, cap0 = predict(image, row["prompt"], [])
                torch.cuda.synchronize(); stage1_ms = (time.perf_counter() - start) * 1000
                after_stage1 = rng_state()
                save_raw(job / "stage1_raw.npz", cap0)
                stage1_matches = None
                if "B0" in refs:
                    stage1_matches = compare(np, b0, s0, refs["B0"][key])
                    if not stage1_matches["matches"] and args.reference_mode == "stop":
                        raise ValueError(f"Stage 1 differs from B0 reference {stage1_matches}; stop before interpreting P1")
                cands, tindices = top_candidates(cap0["scores"], cap0["boxes"], cap0["ids"], image.size, TAU, args.m)
                for c, cos in zip(cands, clip.score(image, [c["box_xyxy"] if c["valid"] else [0, 0, 1, 1] for c in cands], row["prompt"])):
                    c["clip_cosine"] = cos if c["valid"] else None
                cache = {}
                def stage2(chosen_boxes, label):
                    ck = json.dumps(chosen_boxes)
                    if ck not in cache:
                        set_rng(after_stage1)
                        t = time.perf_counter()
                        final, sfinal, cap2 = predict(image, row["prompt"], chosen_boxes)
                        torch.cuda.synchronize()
                        raw = f"stage2_{label}_raw.npz"; save_raw(job / raw, cap2)
                        cache[ck] = (final, sfinal, raw, round((time.perf_counter() - t) * 1000, 2))
                    return cache[ck]
                common = dict(image_width=image.width, image_height=image.height, stage1_count=len(b0), stage1_boxes=b0.tolist(),
                              stage1_scores=s0.tolist(), stage1_matches_B0=stage1_matches, stage1_ms=round(stage1_ms, 2), target_token_indices=tindices)
                for v in variants:
                    rec = recs[v]; rec.update(common)
                    if v == "B2":
                        pb, ps, pids, _ = select_pseudo(cap0["scores"], cap0["boxes"], cap0["ids"], image.size, threshold=TAU, maximum=MAX_PSEUDO)
                        chosen = dict(boxes=pb.tolist(), scores=ps.tolist(), ids=pids, clip=None)
                    else:
                        picked = choose(cands, float(v[3:]), MAX_PSEUDO)
                        chosen = dict(boxes=[c["box_xyxy"] for c in picked], scores=[c["countgd_score"] for c in picked],
                                      ids=[c["proposal_id"] for c in picked], clip=[c["clip_cosine"] for c in picked])
                    rec.update(pseudo_boxes=chosen["boxes"], pseudo_scores=chosen["scores"], pseudo_proposal_ids=chosen["ids"],
                               pseudo_clip=chosen["clip"], n_pseudo=len(chosen["boxes"]), no_pseudo=not chosen["boxes"])
                    if chosen["boxes"]:
                        final, sfinal, raw, ms = stage2(chosen["boxes"], v)
                        rec.update(stage2_executed=True, stage2_raw=raw, stage2_ms=ms, stage2_count=len(final), stage2_boxes=final.tolist(), stage2_scores=sfinal.tolist())
                    else:
                        final, sfinal = b0, s0
                        rec.update(stage2_executed=False, stage2_raw=None, stage2_ms=None, stage2_count=None, stage2_boxes=None, stage2_scores=None)
                    if v == "B2" and "B2" in refs:
                        rec["final_matches_B2_reference"] = compare(np, final, sfinal, refs["B2"][key])
                        if not rec["final_matches_B2_reference"]["matches"] and args.reference_mode == "stop":
                            raise ValueError(f"B2 replay differs from saved B2 {rec['final_matches_B2_reference']}; stop before interpreting P1")
                    draw_boxes(image, final.tolist(), job / f"final_{v}.jpg", "red")
                    rec.update(execution_status="ok", final_count=len(final), final_boxes=final.tolist(), final_scores=sfinal.tolist(),
                               overlay_path=(job / f"final_{v}.jpg").relative_to(ROOT).as_posix())
                draw_boxes(image, [c["box_xyxy"] for c in cands if c["valid"]], job / "candidates.jpg", "lime")
                log.write(json.dumps(dict(image_id=row["image_id"], query_id=row["query_id"], prompt=row["prompt"], candidates=cands,
                                          chosen={v: recs[v]["pseudo_proposal_ids"] for v in variants}), ensure_ascii=False) + "\n")
                counts = ", ".join(f"{v}={recs[v]['final_count']}({recs[v]['n_pseudo']})" for v in variants)
                print(f"{i + 1}/{len(rows)} {row['query_id']} {row['prompt']}: B0={len(b0)}, cand={len(cands)}, {counts}", flush=True)
            except Exception as exc:
                failed = True
                for rec in recs.values():
                    if rec["execution_status"] != "ok":
                        rec["error_message"] = f"{type(exc).__name__}: {exc}"
                print(f"{row['query_id']}: {type(exc).__name__}: {exc}", flush=True)
            for v in variants:
                files[v].write(json.dumps(recs[v], ensure_ascii=False, allow_nan=False) + "\n"); files[v].flush()
            log.flush(); done = i + 1
            if failed:
                break
    finally:
        for f in files.values():
            f.close()
        log.close()
        config.update(status="failed" if failed else "complete", completed_queries=done); save()
    if failed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
