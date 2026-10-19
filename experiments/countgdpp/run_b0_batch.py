"""Run pinned upstream B0, one isolated stock-script process per image/query."""
import argparse
import hashlib
import json
import math
import os
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
REPO = ROOT / "CountGDPlusPlus"
FIELDS = {"schema_version", "image_id", "query_id", "image_path", "prompt"}
SOURCE_HASH = "c6adbad84897f266d25ad6d1672ddea5ef52d1fcdd8f6ec54d94be04c8fa32e9"

def sha(p):
    h = hashlib.sha256()
    with p.open("rb") as f:
        for b in iter(lambda: f.read(1024 * 1024), b""):
            h.update(b)
    return h.hexdigest()

def project_path(value):
    p = (ROOT / value).resolve()
    if not p.is_relative_to(ROOT):
        raise ValueError("Path must stay within CS331")
    return p

def load_inputs(path):
    rows = [json.loads(s) for s in path.read_text(encoding="utf-8-sig").splitlines() if s.strip()]
    if not rows:
        raise ValueError("No inputs")
    seen = set()
    for row in rows:
        if set(row) != FIELDS or row["schema_version"] != 1:
            raise ValueError("Expected schema v1 input-only fields; no GT allowed")
        for field in ("image_id", "query_id"):
            if not isinstance(row[field], str) or not re.fullmatch(r"[A-Za-z0-9_-]+", row[field]):
                raise ValueError("Invalid ID")
        key = (row["image_id"], row["query_id"])
        if key in seen:
            raise ValueError("Duplicate image/query ID")
        seen.add(key)
        if not isinstance(row["prompt"], str) or not row["prompt"].strip():
            raise ValueError("Empty prompt")
        with Image.open(project_path(row["image_path"])) as im:
            im.verify()
    return rows

def validate_prediction(d):
    n, boxes, scores = d["count"], d["boxes"], d["scores"]
    if type(n) is not int or n < 0 or n != len(boxes) or n != len(scores):
        raise ValueError("Count/boxes/scores mismatch")
    if not all(len(b) == 4 and all(math.isfinite(v) for v in b) and b[0] <= b[2] and b[1] <= b[3] for b in boxes):
        raise ValueError("Invalid boxes")
    if not all(math.isfinite(v) and 0 <= v <= 1 for v in scores):
        raise ValueError("Invalid scores")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--inputs", required=True, help="Path relative to CS331")
    parser.add_argument("--run-id")
    parser.add_argument("--check-inputs", action="store_true")
    args = parser.parse_args()
    inputs = project_path(args.inputs)
    rows = load_inputs(inputs)
    print(f"Validated {len(rows)} queries / {len({r['image_id'] for r in rows})} images", flush=True)
    if args.check_inputs:
        return
    if not args.run_id or not re.fullmatch(r"[A-Za-z0-9_-]+", args.run_id):
        raise ValueError("Provide a unique --run-id")
    if sha(REPO / "process_folder.py") != SOURCE_HASH:
        raise ValueError("Upstream source changed; review first")
    checkpoint = REPO / "checkpoints/countgd_plusplus.pth"
    audit = json.loads((ROOT / "results/countgdpp/checkpoint_audit_2026-10-14.json").read_text())
    checkpoint_hash = sha(checkpoint)
    if audit.get("review_decision") != "compatible_with_pinned_B0_app" or audit["checkpoint_sha256"] != checkpoint_hash:
        raise ValueError("Checkpoint audit must be reviewed for this checkpoint")
    for source_name, expected_hash in audit.get("review_source_sha256", {}).items():
        if sha(REPO / source_name) != expected_hash:
            raise ValueError("Reviewed model code changed; repeat audit review")
    out = ROOT / "results/countgdpp" / args.run_id
    out.mkdir(exist_ok=False)
    config = dict(schema_version=1, run_id=args.run_id, variant="B0", status="running",
        model_commit=subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=REPO, text=True).strip(),
        adapter_sha256=sha(Path(__file__)), process_folder_sha256=SOURCE_HASH,
        checkpoint_sha256=checkpoint_hash, input_sha256=sha(inputs), manifest_sha256=None,
        manifest_note="GT manifest is evaluator-only; identify its version when joining predictions",
        checkpoint_source="https://github.com/niki-amini-naieni/CountGDPlusPlus",
        conf_thresh=0.23, seed=42, resize=dict(short_side=800, max_size=1333), precision="stock default; no AMP flag",
        pseudo_exemplars=False, negative_prompts=False, crop=False, synthetic_exemplars=False,
        elapsed_ms_definition="Per-query stock subprocess wall time, includes model load/preprocess/inference/overlay/write; not pure inference latency",
        peak_vram_mib_note="Not measured, null; resource profiling remains pending",
        python=sys.version, executable=sys.executable, inputs=rows)
    def save_config():
        (out / "run_config.json").write_text(json.dumps(config, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    save_config()
    failures = 0
    with (out / "predictions.jsonl").open("w", encoding="utf-8") as pred_file:
        for i, row in enumerate(rows):
            job = out / "jobs" / f"{i+1:03d}_{row['query_id']}"
            image_dir = job / "input"
            image_dir.mkdir(parents=True)
            source = project_path(row["image_path"])
            image = image_dir / source.name
            shutil.copy2(source, image)
            with Image.open(image) as im:
                w, h = im.size
            prompts = {"positive": {"text": row["prompt"], "exemplars": {"image": str(image), "boxes": []}}, "negative": []}
            prompt_file = job / "prompt.json"
            prompt_file.write_text(json.dumps(prompts, ensure_ascii=False), encoding="utf-8")
            raw = job / "raw"
            cmd = [sys.executable, "process_folder.py", "--input_folder", str(image_dir), "--prompts", str(prompt_file), "--output_folder", str(raw), "--conf_thresh", "0.23", "--vis_output"]
            (job / "command.json").write_text(json.dumps(cmd, ensure_ascii=False), encoding="utf-8")
            record = dict(schema_version=1, run_id=args.run_id, variant="B0", image_id=row["image_id"], query_id=row["query_id"],
                execution_status="error", final_count=None, final_boxes=[], final_scores=[], box_format="xyxy_pixels",
                image_width=w, image_height=h, error_message=None, overlay_path=None, elapsed_ms=None, peak_vram_mib=None)
            start = time.perf_counter()
            try:
                with (job / "console.log").open("w", encoding="utf-8") as log:
                    result = subprocess.run(cmd, cwd=REPO, stdout=log, stderr=subprocess.STDOUT, env={**os.environ, "PYTHONUNBUFFERED": "1"})
                if result.returncode:
                    raise RuntimeError(f"Process exit {result.returncode}; see jobs/{job.name}/console.log")
                data = json.loads((raw / "results.json").read_text())
                if set(data) != {image.name}:
                    raise ValueError("Unexpected image IDs in raw output")
                d = data[image.name]
                validate_prediction(d)
                overlay = raw / image.name
                if not overlay.exists():
                    raise ValueError("Missing overlay")
                record.update(execution_status="ok", final_count=d["count"], final_boxes=d["boxes"], final_scores=d["scores"], overlay_path=overlay.relative_to(ROOT).as_posix())
            except Exception as exc:
                failures += 1
                record["error_message"] = str(exc)
            record["elapsed_ms"] = round((time.perf_counter() - start) * 1000, 2)
            pred_file.write(json.dumps(record, ensure_ascii=False, allow_nan=False) + "\n")
            pred_file.flush()
            print(f"{i+1}/{len(rows)} {row['query_id']} {row['prompt']}: {record['execution_status']} count={record['final_count']}", flush=True)
            if record["execution_status"] == "error":
                break  # diagnose first failure; remaining rows are not silently treated as zero
    config.update(status="failed" if failures else "complete", completed_queries=i+1, failed_queries=failures)
    save_config()
    if failures:
        raise SystemExit(1)

if __name__ == "__main__":
    main()
