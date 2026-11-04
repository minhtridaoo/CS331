"""P1 controls (plan section 3.5): apply the FROZEN P4 final filters to every box source of one P1 run (no GT).

Box sources, all from the same run (same GPU, same stage 1):
  B0    = stage 1 (stage1_boxes/scores; identical in every predictions file of the run)
  B2    = predictions_B2.jsonl (the run must use --replay-b2)
  tauX  = predictions_tauX.jsonl (P1 with tau_pseudo = X)
Methods per source X: X (all boxes), X+S (CountGD++ score >= frozen b2_threshold), X+F (frozen Fusion 50/50).
So B2+F = F, B2+S = S-only, B0+F = C6, tauX+F = P+F. The freeze was fitted on pilot B2 boxes (20-21/10); on B0
and P boxes the box's own CountGD++ score takes the place of b2_score (same rule, no refit).

CLIP scores come from p4_clip_score.py, unchanged, called once for all sources (query IDs prefixed "<source>__");
keep decisions from p4_apply_freeze.load_freeze/decisions. Every score row is checked against its source box.

Example (from CS331 root):
  python experiments/countgdpp/p1_controls.py --run results/countgdpp/p1_pilot_colab_20261103_1519 \
      --run-id p1_pilot_colab_20261103_1519_controls
Writes results/countgdpp/<run-id>_clip/ (CLIP scores) and results/countgdpp/<run-id>/ (counts, kept boxes, config).
"""
import argparse
import csv
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

from p4_apply_freeze import FREEZE, FREEZE_SHA256, decisions, load_freeze, load_scores
from run_b0_batch import ROOT, sha, project_path

SEP = "__"


def read_jsonl(path):
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def write_jsonl(path, rows):
    path.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows), encoding="utf-8")


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--run", required=True, help="P1 run folder (run_b2_verified_pseudo.py), relative to CS331")
    p.add_argument("--run-id", required=True, help="New folder under results/countgdpp; never overwritten")
    p.add_argument("--clip-scores", help="Reuse an existing CLIP score folder (prefixed query IDs) instead of calling CLIP")
    p.add_argument("--check-inputs", action="store_true", help="Build the source files and let p4_clip_score.py validate them, then stop")
    args = p.parse_args()
    if not re.fullmatch(r"[A-Za-z0-9_-]+", args.run_id):
        raise ValueError("Invalid run ID")

    run = project_path(args.run)
    cfg_path = run / "run_config.json"
    cfg = json.loads(cfg_path.read_text(encoding="utf-8"))
    if cfg.get("runner") != "run_b2_verified_pseudo.py" or cfg.get("status") != "complete":
        raise ValueError("Expected a complete run of run_b2_verified_pseudo.py")
    if "B2" not in cfg["outputs"]:
        raise ValueError("Run has no B2 replay (--replay-b2); F and S-only need B2 from the same run")
    inputs = {r["query_id"]: r for r in cfg["inputs"]}
    preds = {}
    for variant, name in cfg["outputs"].items():
        rows = {r["query_id"]: r for r in read_jsonl(run / name)}
        if set(rows) != set(inputs):
            raise ValueError(f"{name}: query set differs from the run inputs")
        for qid, r in rows.items():
            if r["execution_status"] != "ok" or r["image_id"] != inputs[qid]["image_id"] or r["box_format"] != "xyxy_pixels":
                raise ValueError(f"{name}: bad record {qid}")
            if not len(r["final_boxes"]) == len(r["final_scores"]) == r["final_count"]:
                raise ValueError(f"{name}: count mismatch {qid}")
        preds[variant] = rows
    b2 = preds["B2"]
    for variant, rows in preds.items():
        for qid, r in rows.items():
            if (r["stage1_boxes"], r["stage1_scores"]) != (b2[qid]["stage1_boxes"], b2[qid]["stage1_scores"]):
                raise ValueError(f"Stage 1 differs between B2 and {variant} for {qid}")

    # label = column name in the outputs; key = ID-safe prefix for the CLIP scorer
    sources = {"B0": {q: (r["stage1_boxes"], r["stage1_scores"]) for q, r in b2.items()}}
    for variant, rows in preds.items():
        sources[variant] = {q: (r["final_boxes"], r["final_scores"]) for q, r in rows.items()}
    keys = {label: label.replace(".", "p") for label in sources}

    out = ROOT / "results/countgdpp" / args.run_id
    clip_dir = project_path(args.clip_scores) if args.clip_scores else ROOT / "results/countgdpp" / (args.run_id + "_clip")
    if out.exists() or (not args.clip_scores and clip_dir.exists()):
        raise SystemExit("Output directory exists. Use a new run ID; do not overwrite previous results.")
    out.mkdir(parents=True)
    src_inputs, src_preds = [], []
    for label, per_query in sources.items():
        for qid in sorted(inputs):
            inp, (boxes, scores) = inputs[qid], per_query[qid]
            sid = keys[label] + SEP + qid
            src_inputs.append(dict(schema_version=1, image_id=inp["image_id"], query_id=sid, image_path=inp["image_path"], prompt=inp["prompt"]))
            src_preds.append(dict(query_id=sid, image_id=inp["image_id"], execution_status="ok", box_format="xyxy_pixels",
                                  final_boxes=boxes, final_scores=scores, final_count=len(boxes),
                                  image_width=b2[qid]["image_width"], image_height=b2[qid]["image_height"]))
    in_path, pred_path = out / "sources_inputs.jsonl", out / "sources_predictions.jsonl"
    write_jsonl(in_path, src_inputs)
    write_jsonl(pred_path, src_preds)
    print(f"{len(sources)} sources x {len(inputs)} queries, {sum(r['final_count'] for r in src_preds)} boxes: {', '.join(sources)}", flush=True)

    if args.check_inputs or not args.clip_scores:
        cmd = [sys.executable, str(Path(__file__).with_name("p4_clip_score.py")), "--inputs", in_path.relative_to(ROOT).as_posix(),
               "--predictions", pred_path.relative_to(ROOT).as_posix(), "--run-id", args.run_id + "_clip"]
        subprocess.run(cmd + (["--check-inputs"] if args.check_inputs else []), cwd=ROOT, check=True)
    if args.check_inputs:
        shutil.rmtree(out)
        print("CHECK-INPUTS PASS; nothing kept")
        return

    fz = load_freeze()
    data = load_scores(clip_dir)
    if set(data) != {r["query_id"] for r in src_preds}:
        raise ValueError("CLIP score files do not cover exactly the source queries")
    for r in src_preds:
        obj, rows = data[r["query_id"]]["obj"], data[r["query_id"]]["rows"]
        if obj.get("clip_model") != fz["clip_model"]:
            raise ValueError("Scores come from a different CLIP model")
        if ([x["original_box_xyxy"] for x in rows] != r["final_boxes"]
                or [float(x["b2_score"]) for x in rows] != [float(s) for s in r["final_scores"]]):
            raise ValueError(f"CLIP score rows do not match the source boxes: {r['query_id']}")

    labels = list(sources)
    per_query, kept = [], {label: {} for label in labels}
    for qid in sorted(inputs):
        row = dict(query_id=qid, image_id=inputs[qid]["image_id"], prompt=inputs[qid]["prompt"])
        for label in labels:
            d = decisions(data[keys[label] + SEP + qid]["rows"], fz)
            kept[label][qid] = [dict(rank=x["rank"], box_xyxy=box, countgd_score=x["b2_score"], clip_cosine_target=x["clip_cosine_target"],
                                     fusion_score=x["fusion_score"], keep_S=x["keep_B2_threshold"], keep_F=x["keep_Fusion_50_50"])
                                for x, box in zip(d, sources[label][qid][0])]
            row.update({label: len(d), label + "+S": sum(x["keep_B2_threshold"] for x in d), label + "+F": sum(x["keep_Fusion_50_50"] for x in d)})
        row.update({f"{v}_n_pseudo": len(preds[v][qid].get("pseudo_boxes") or []) for v in preds})
        per_query.append(row)

    with (out / "per_query_counts.csv").open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(per_query[0]), lineterminator="\n")
        w.writeheader()
        w.writerows(per_query)
    (out / "kept_boxes.json").write_text(json.dumps(kept, ensure_ascii=False) + "\n", encoding="utf-8")
    clip_cfg = clip_dir / "run_config.json"
    config = dict(runner="p1_controls.py", adapter_sha256=sha(Path(__file__)),
                  clip_scorer_sha256=sha(Path(__file__).with_name("p4_clip_score.py")),
                  freeze_applier_sha256=sha(Path(__file__).with_name("p4_apply_freeze.py")),
                  freeze=FREEZE, freeze_sha256=FREEZE_SHA256,
                  frozen_values=dict(b2_threshold=fz["b2_threshold"], fusion_threshold=fz["fusion_threshold"], bounds=fz["bounds"]),
                  p1_run=args.run, p1_run_config_sha256=sha(cfg_path), prediction_sha256={n: sha(run / n) for n in cfg["outputs"].values()},
                  clip_scores=clip_dir.relative_to(ROOT).as_posix(), clip_run_config_sha256=sha(clip_cfg) if clip_cfg.exists() else None,
                  sources=labels, methods="per source X: X (all boxes), X+S (score >= b2_threshold), X+F (Fusion 50/50 >= threshold)",
                  plan_names={"F": "B2+F", "S-only": "B2+S", "C6": "B0+F", "P": "tauX", "P+F": "tauX+F"},
                  note="Freeze fitted on pilot B2 boxes; on B0/P boxes the box's own CountGD++ score replaces b2_score. No refit, no GT.",
                  uses_ground_truth=False)
    (out / "run_config.json").write_text(json.dumps(config, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    taus = [v for v in preds if v != "B2"]
    print(f"{'query':<8}{'B0':>5}{'B0+F':>6}{'B2':>5}{'B2+S':>6}{'B2+F':>6}" + "".join(f"{t + ' / +F':>18}" for t in taus))
    for r in per_query:
        print(f"{r['query_id']:<8}{r['B0']:>5}{r['B0+F']:>6}{r['B2']:>5}{r['B2+S']:>6}{r['B2+F']:>6}"
              + "".join(f"{str(r[t]) + ' / ' + str(r[t + '+F']):>18}" for t in taus))
    print("Saved:", out)


if __name__ == "__main__":
    main()
