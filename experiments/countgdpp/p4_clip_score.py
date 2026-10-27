"""P4.6b: CLIP crop scorer with CLI paths (generalizes evaluation/p4_clip_score_all15_20261020.py).

Scoring is kept identical to the 20/10 dev run: RGB crop of each final B2 box (Python round +
clamp, no padding), CLIPProcessor(use_fast=False), template "a photo of {prompt}", L2-normalized
cosine, batch size 2, no softmax. Model and processor are pinned to the revision recorded in
results/countgdpp/p4_clip_all15_20261020/run_config.json. Reads inputs + B2 predictions only (no GT).

Example (from CS331 root):
  python experiments/countgdpp/p4_clip_score.py --inputs experiments/countgdpp/m4_inputs/first5_inputs.jsonl \
      --predictions results/countgdpp/b2_two_images_20261015/predictions.jsonl \
                    results/countgdpp/b2_remaining3_20261015/predictions.jsonl \
      --run-id p4_clip_devcheck_YYYYMMDD
"""
import argparse
import json
import math
import re
from pathlib import Path

from PIL import Image
from run_b0_batch import ROOT, sha, load_inputs, project_path

MODEL_ID = "openai/clip-vit-base-patch32"
REVISION = "3d74acf9a28c67741b2f4f2ea7635f0aaf6f0268"
BATCH_SIZE = 2
TEMPLATE = "a photo of {prompt}"


def read_jsonl(path):
    with path.open(encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


def crop_box(box, width, height):
    if len(box) != 4 or not all(math.isfinite(float(v)) for v in box):
        raise ValueError("Invalid box values")
    x1, y1, x2, y2 = map(float, box)
    if not (x1 < x2 and y1 < y2):
        raise ValueError("Invalid box geometry")
    a = max(0, min(round(x1), width - 1))
    b = max(0, min(round(y1), height - 1))
    c = max(a + 1, min(round(x2), width))
    d = max(b + 1, min(round(y2), height))
    return [a, b, c, d]


def cached_weight_hashes():
    """sha256 of locally cached weight files for the pinned revision (no download)."""
    try:
        from huggingface_hub import try_to_load_from_cache
    except ImportError:
        return {}
    found = {}
    for name in ("model.safetensors", "pytorch_model.bin", "config.json", "preprocessor_config.json",
                 "tokenizer.json", "vocab.json", "merges.txt"):
        path = try_to_load_from_cache(MODEL_ID, name, revision=REVISION)
        if isinstance(path, str):
            found[name] = sha(Path(path))
    return found


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--inputs", required=True, help="Input-only JSONL (schema v1), relative to CS331")
    p.add_argument("--predictions", required=True, nargs="+", help="B2 predictions.jsonl file(s), relative to CS331")
    p.add_argument("--run-id", required=True, help="New folder under results/countgdpp; never overwritten")
    p.add_argument("--check-inputs", action="store_true", help="Validate inputs/predictions, then stop before loading CLIP")
    args = p.parse_args()
    if not re.fullmatch(r"[A-Za-z0-9_-]+", args.run_id):
        raise ValueError("Invalid run ID")

    inputs_path = project_path(args.inputs)
    inputs = {}
    for row in load_inputs(inputs_path):
        if row["query_id"] in inputs:
            raise ValueError(f"Duplicate input query_id: {row['query_id']}")
        inputs[row["query_id"]] = row

    pred_paths = [project_path(x) for x in args.predictions]
    preds = {}
    for path in pred_paths:
        for row in read_jsonl(path):
            qid = row["query_id"]
            if qid in preds:
                raise ValueError(f"Duplicate prediction: {qid}")
            preds[qid] = row
    if set(inputs) != set(preds):
        raise ValueError(f"Input/prediction query sets differ: missing={sorted(set(inputs)-set(preds))} extra={sorted(set(preds)-set(inputs))}")
    for qid, row in preds.items():
        if row["execution_status"] != "ok":
            raise ValueError(f"Prediction error: {qid}")
        if row["image_id"] != inputs[qid]["image_id"]:
            raise ValueError(f"Image ID mismatch: {qid}")
        if row["box_format"] != "xyxy_pixels":
            raise ValueError(f"Unexpected box format: {qid}")
        if not (len(row["final_boxes"]) == len(row["final_scores"]) == row["final_count"]):
            raise ValueError(f"Count mismatch: {qid}")

    out = ROOT / "results/countgdpp" / args.run_id
    if out.exists():
        raise SystemExit("Output directory exists. Use a new run ID; do not overwrite previous results.")
    print(f"INPUT VALIDATION PASS: {len(inputs)} queries, {sum(r['final_count'] for r in preds.values())} boxes", flush=True)
    if args.check_inputs:
        return

    import torch
    import transformers
    from transformers import CLIPModel, CLIPProcessor

    device = "cuda" if torch.cuda.is_available() else "cpu"
    processor = CLIPProcessor.from_pretrained(MODEL_ID, revision=REVISION, use_fast=False)
    model = CLIPModel.from_pretrained(MODEL_ID, revision=REVISION).to(device)
    model.eval()
    resolved = getattr(model.config, "_commit_hash", None)
    if resolved != REVISION:
        raise ValueError(f"Resolved CLIP revision {resolved} != pinned {REVISION}")

    @torch.inference_mode()
    def score_images(crops, prompt):
        text = processor(text=[TEMPLATE.format(prompt=prompt)], return_tensors="pt", padding=True)
        text = {k: v.to(device) for k, v in text.items()}
        text_features = torch.nn.functional.normalize(model.get_text_features(**text), dim=-1)
        scores = []
        for start in range(0, len(crops), BATCH_SIZE):
            pixels = processor(images=crops[start:start + BATCH_SIZE], return_tensors="pt")["pixel_values"].to(device)
            image_features = torch.nn.functional.normalize(model.get_image_features(pixel_values=pixels), dim=-1)
            scores.extend((image_features @ text_features.T)[:, 0].cpu().tolist())
        return scores

    out.mkdir(parents=True)
    summary = []
    for qid in sorted(inputs):
        inp, pred = inputs[qid], preds[qid]
        with Image.open(project_path(inp["image_path"])) as original:
            image = original.convert("RGB")
        width, height = image.size
        if (width, height) != (pred["image_width"], pred["image_height"]):
            raise ValueError(f"Image size mismatch: {qid}")
        boxes, b2_scores = pred["final_boxes"], pred["final_scores"]
        pixel_boxes = [crop_box(box, width, height) for box in boxes]
        clip_scores = score_images([image.crop(tuple(b)) for b in pixel_boxes], inp["prompt"]) if boxes else []
        rows = [dict(rank=i, original_box_xyxy=ob, box_xyxy=pb, b2_score=float(b2), clip_cosine_target=float(c))
                for i, (ob, pb, b2, c) in enumerate(zip(boxes, pixel_boxes, b2_scores, clip_scores), start=1)]
        result = dict(query_id=qid, image_id=pred["image_id"], image_path=inp["image_path"], prompt=inp["prompt"],
                      text_prompt=TEMPLATE.format(prompt=inp["prompt"]), clip_model=MODEL_ID, clip_revision=REVISION,
                      device=device, n_boxes=len(rows), rows_original_order=rows,
                      rows_sorted_by_clip=sorted(rows, key=lambda x: x["clip_cosine_target"], reverse=True))
        path = out / f"{qid}_clip_scores.json"
        path.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
        summary.append(dict(query_id=qid, image_id=pred["image_id"], n_boxes=len(rows), output_file=path.relative_to(ROOT).as_posix()))
        print(f"PASS {qid}: {len(rows)} boxes", flush=True)

    config = dict(runner="p4_clip_score.py (P4.6b)", adapter_sha256=sha(Path(__file__)), model_id=MODEL_ID,
                  model_revision=resolved, pinned_revision=REVISION, cached_file_sha256=cached_weight_hashes(),
                  device=device, device_name=torch.cuda.get_device_name() if device == "cuda" else None,
                  batch_size=BATCH_SIZE, processor_use_fast=False, text_template=TEMPLATE,
                  torch_version=torch.__version__, transformers_version=transformers.__version__,
                  inputs=args.inputs, inputs_sha256=sha(inputs_path),
                  prediction_sha256={x: sha(pp) for x, pp in zip(args.predictions, pred_paths)},
                  uses_ground_truth_for_scoring=False, status="scores_only_no_filtering")
    (out / "run_config.json").write_text(json.dumps(config, indent=2, ensure_ascii=False), encoding="utf-8")
    (out / "summary.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"TOTAL QUERIES: {len(summary)}  TOTAL SCORED BOXES: {sum(s['n_boxes'] for s in summary)}  OUTPUT: {out}")


if __name__ == "__main__":
    main()
