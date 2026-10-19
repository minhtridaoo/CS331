"""Instrument pinned B0 without modifying its filtering or upstream files.
The target-token mask is an offline counterfactual, never the returned prediction.
"""
import argparse
import ast
import csv
import json
import os
import sys
import time
from pathlib import Path
from PIL import Image, ImageDraw
from run_b0_batch import ROOT, REPO, SOURCE_HASH, sha, load_inputs, project_path


def summarize(scores, ids, tokenizer, threshold):
    import numpy as np
    tokens = tokenizer.convert_ids_to_tokens(ids)
    dot = ids.index(1012)
    positive = scores[:, :dot + 1].max(axis=1)
    remaining = scores[:, dot + 1:].max(axis=1)
    special_ids = set(tokenizer.all_special_ids) | {1012, 1029}
    word_indices = [i for i in range(dot) if ids[i] not in special_ids]
    if not word_indices:
        raise ValueError("No target word tokens before first period")
    excluded_indices = [i for i in range(dot + 1) if i not in word_indices]
    target = scores[:, word_indices].max(axis=1)
    excluded = scores[:, excluded_indices].max(axis=1) if excluded_indices else np.zeros(len(scores))
    original = (positive > threshold) & (positive > remaining)
    content = (target > threshold) & (target > remaining)
    top_positive_indices = scores[:, :dot + 1].argmax(axis=1)
    kept_ids = np.flatnonzero(original)
    summary = dict(tokens=tokens, token_ids=ids, target_token_indices=word_indices,
        excluded_positive_indices=excluded_indices, first_period_index=dot,
        proposals=len(scores), stock_count=int(original.sum()),
        target_tokens_only_counterfactual_count=int(content.sum()),
        stock_kept_but_target_only_rejects=int((original & ~content).sum()),
        kept_top_positive_tokens={t: int(sum(tokens[top_positive_indices[k]] == t for k in kept_ids)) for t in tokens[:dot+1]})
    details = []
    for k in kept_ids:
        record = dict(proposal_id=int(k), stock_positive_max=float(positive[k]),
            target_word_max=float(target[k]), excluded_positive_max=float(excluded[k]),
            remaining_columns_max=float(remaining[k]), top_positive_token=tokens[top_positive_indices[k]],
            target_only_keeps=bool(content[k]))
        for j, token in enumerate(tokens):
            record[f"token_{j}_{token}"] = float(scores[k, j])
        record["columns_beyond_input_ids_max"] = float(scores[k, len(ids):].max()) if scores.shape[1] > len(ids) else None
        details.append(record)
    return summary, details, kept_ids


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--query-ids", nargs="+", default=["q03_2"])
    parser.add_argument("--run-id", required=True)
    args = parser.parse_args()
    import re
    if not re.fullmatch(r"[A-Za-z0-9_-]+", args.run_id):
        raise ValueError("Invalid run ID")
    if len(set(args.query_ids)) != len(args.query_ids):
        raise ValueError("Duplicate query ID")
    inputs_file = ROOT / "experiments/countgdpp/m4_inputs/first5_inputs.jsonl"
    inputs = load_inputs(inputs_file)
    by_id = {r["query_id"]: r for r in inputs}
    rows = [by_id[q] for q in args.query_ids]
    prior_path = ROOT / "results/countgdpp/m4_first5_b0/predictions.jsonl"
    prior = {r["query_id"]: r for r in map(json.loads, prior_path.read_text().splitlines())}
    audit = json.loads((ROOT / "results/countgdpp/checkpoint_audit_2026-10-14.json").read_text())
    checkpoint_hash = sha(REPO / "checkpoints/countgd_plusplus.pth")
    if audit.get("review_decision") != "compatible_with_pinned_B0_app" or checkpoint_hash != audit["checkpoint_sha256"]:
        raise ValueError("Checkpoint audit mismatch")
    if sha(REPO / "process_folder.py") != SOURCE_HASH:
        raise ValueError("Upstream script changed")
    for name, digest in audit["review_source_sha256"].items():
        if sha(REPO / name) != digest:
            raise ValueError("Reviewed model source changed")
    out = ROOT / "results/countgdpp" / args.run_id
    out.mkdir(exist_ok=False)
    config = dict(status="running", scope="Instrumented original B0; target-token alternative is offline diagnostic only",
        query_ids=args.query_ids, inputs=rows, source_script_sha256=SOURCE_HASH, diagnostic_script_sha256=sha(Path(__file__)),
        checkpoint_sha256=checkpoint_hash, input_sha256=sha(inputs_file), reference_predictions_sha256=sha(prior_path),
        threshold=0.23, seed=42, date="2026-10-15", measurements="Predict call including preprocessing, transfers and tensor capture; excludes model load/overlay/write, no warm-up. Peak allocated memory includes resident model; not total device VRAM.")
    config_path = out / "run_config.json"
    def save_config():
        config_path.write_text(json.dumps(config, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
    save_config()
    import torch
    import numpy as np
    if not torch.cuda.is_available():
        raise RuntimeError("CUDA required for comparison with prior GPU run")
    sys.path.insert(0, str(REPO))
    os.chdir(REPO)
    source = REPO / "process_folder.py"
    tree = ast.parse(source.read_text())
    tree.body = [n for n in tree.body if isinstance(n, (ast.Import, ast.ImportFrom, ast.FunctionDef))]
    ns = {"__name__": "pinned_stock_definitions"}
    exec(compile(tree, str(source), "exec"), ns)
    model, transform = ns["build_model_and_transforms"](ns["build_arg_parser"]().parse_args([]))
    device = torch.device("cuda")
    model = model.to(device)
    original_filter = ns["get_boxes_from_prediction"]
    captured = {}
    def observe(model_output, text, keywords="", conf_thresh=0.23):
        result = original_filter(model_output, text, keywords, conf_thresh)
        captured["scores"] = model_output["pred_logits"].sigmoid()[0].detach().cpu().numpy()
        captured["boxes"] = model_output["pred_boxes"][0].detach().cpu().numpy()
        captured["ids"] = model_output["input_ids"][0].detach().cpu().tolist()
        return result  # exact stock return, no change to predictions
    ns["get_boxes_from_prediction"] = observe
    summaries = []
    for row in rows:
        q = row["query_id"]
        job = out / q
        job.mkdir()
        image = Image.open(project_path(row["image_path"])).convert("RGB")
        torch.manual_seed(42); np.random.seed(42); ns["random"].seed(42)
        torch.cuda.synchronize(); torch.cuda.reset_peak_memory_stats()
        start = time.perf_counter()
        boxes, scores = ns["predict"](model, transform, image, row["prompt"], {"image": image, "points": []}, [], [], device, 0.23)
        torch.cuda.synchronize()
        elapsed = (time.perf_counter()-start)*1000
        peak = torch.cuda.max_memory_allocated()/1024**2
        summary, details, kept = summarize(captured["scores"], captured["ids"], model.tokenizer, 0.23)
        np.testing.assert_allclose(boxes, captured["boxes"][kept], rtol=0, atol=0)
        np.testing.assert_allclose(scores, captured["scores"][kept].max(axis=1), rtol=0, atol=1e-7)
        x, y, w, h = ns["get_box_coords_from_boxes"](image, boxes)
        xyxy = np.stack((x, y, x+w, y+h), axis=-1)
        before = prior[q]
        matches = len(boxes) == before["final_count"]
        matches = matches and np.allclose(xyxy, np.asarray(before["final_boxes"]).reshape(-1,4), rtol=0, atol=0.001)
        matches = matches and np.allclose(scores, before["final_scores"], rtol=0, atol=1e-5)
        summary.update(query_id=q, prompt=row["prompt"], image_id=row["image_id"], prior_count=before["final_count"],
            matches_prior_count_boxes_scores=bool(matches), predict_capture_ms=round(elapsed,2), peak_allocated_mib=round(peak,2))
        np.savez_compressed(job / "raw_scores.npz", scores=captured["scores"], normalized_cxcywh=captured["boxes"], input_ids=np.array(captured["ids"]))
        for r,b in zip(details,xyxy):
            r.update(zip(["x1","y1","x2","y2"],map(float,b)))
        if details:
            with (job/"kept_box_tokens.csv").open("w",encoding="utf-8",newline="") as f:
                writer=csv.DictWriter(f,fieldnames=list(details[0])); writer.writeheader(); writer.writerows(details)
        (job/"summary.json").write_text(json.dumps(summary,indent=2)+"\n")
        annotated=image.copy();draw=ImageDraw.Draw(annotated)
        for k,b in zip(kept,xyxy):
            draw.rectangle(tuple(map(float,b)),outline="red",width=2)
            draw.text((float(b[0]),max(0,float(b[1])-10)),str(k),fill="red")
        annotated.save(job/"proposal_ids.jpg")
        summaries.append(summary)
        (out/"summary.json").write_text(json.dumps(summaries,indent=2)+"\n")
        print(f"{q} {row['prompt']}: stock={len(boxes)}, target-token counterfactual={summary['target_tokens_only_counterfactual_count']}, replay_matches={matches}",flush=True)
        if not matches:
            config["status"]="replay_mismatch"; save_config()
            raise RuntimeError("Diagnostic replay differs from original; inspect before interpreting")
    config["status"]="complete"; save_config()

if __name__ == "__main__":
    main()
