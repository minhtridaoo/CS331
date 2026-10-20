import json
import math
import hashlib
from pathlib import Path

import torch
import transformers
from PIL import Image
from transformers import CLIPModel, CLIPProcessor

MODEL_ID = "openai/clip-vit-base-patch32"
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
BATCH_SIZE = 2

ROOT = Path.cwd()

INPUTS = ROOT / "experiments/countgdpp/m4_inputs/first5_inputs.jsonl"

PRED_FILES = [
    ROOT / "results/countgdpp/b2_two_images_20261015/predictions.jsonl",
    ROOT / "results/countgdpp/b2_remaining3_20261015/predictions.jsonl",
]

OUT = ROOT / "results/countgdpp/p4_clip_all15_20261020"

def read_jsonl(path):
    with path.open(encoding="utf-8") as f:
        return [
            json.loads(line)
            for line in f
            if line.strip()
        ]

def sha256(path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

# 1. Validate source inputs
inputs = {}
for row in read_jsonl(INPUTS):
    qid = row["query_id"]
    if qid in inputs:
        raise ValueError(f"Duplicate input: {qid}")
    inputs[qid] = row

preds = {}
for path in PRED_FILES:
    for row in read_jsonl(path):
        qid = row["query_id"]
        if qid in preds:
            raise ValueError(f"Duplicate prediction: {qid}")
        preds[qid] = row

if len(inputs) != 15 or set(inputs) != set(preds):
    raise ValueError("Expected exactly 15 matching queries")

for qid, row in preds.items():
    boxes = row["final_boxes"]
    scores = row["final_scores"]

    if row["execution_status"] != "ok":
        raise ValueError(f"Prediction error: {qid}")

    if row["box_format"] != "xyxy_pixels":
        raise ValueError(f"Unexpected box format: {qid}")

    if not (len(boxes) == len(scores) == row["final_count"]):
        raise ValueError(f"Count mismatch: {qid}")

    path = ROOT / inputs[qid]["image_path"]
    if not path.is_file():
        raise FileNotFoundError(path)

if OUT.exists():
    raise SystemExit(
        "Output directory exists. Use a new run name; "
        "do not overwrite the previous result."
    )

print("INPUT VALIDATION PASS", flush=True)
print("Queries:", len(inputs), flush=True)
print("Loading CLIP:", MODEL_ID, flush=True)

# 2. Load model
processor = CLIPProcessor.from_pretrained(
    MODEL_ID,
    use_fast=False
)

model = CLIPModel.from_pretrained(MODEL_ID).to(DEVICE)
model.eval()

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

@torch.inference_mode()
def score_images(crops, prompt):
    text = processor(
        text=[f"a photo of {prompt}"],
        return_tensors="pt",
        padding=True
    )
    text = {k: v.to(DEVICE) for k, v in text.items()}

    text_features = model.get_text_features(**text)
    text_features = torch.nn.functional.normalize(
        text_features, dim=-1
    )

    all_scores = []

    for start in range(0, len(crops), BATCH_SIZE):
        group = crops[start:start + BATCH_SIZE]

        image_data = processor(
            images=group,
            return_tensors="pt"
        )
        pixels = image_data["pixel_values"].to(DEVICE)

        image_features = model.get_image_features(
            pixel_values=pixels
        )
        image_features = torch.nn.functional.normalize(
            image_features, dim=-1
        )

        scores = image_features @ text_features.T

        all_scores.extend(
            scores[:, 0].cpu().tolist()
        )

    return all_scores

# 3. Save scored predictions
OUT.mkdir(parents=True)

summary = []
total_boxes = 0

for qid in sorted(inputs):
    inp = inputs[qid]
    pred = preds[qid]

    image_path = ROOT / inp["image_path"]

    with Image.open(image_path) as original:
        image = original.convert("RGB")

    width, height = image.size

    if (width, height) != (
        pred["image_width"],
        pred["image_height"]
    ):
        raise ValueError(f"Image size mismatch: {qid}")

    boxes = pred["final_boxes"]
    b2_scores = pred["final_scores"]

    pixel_boxes = [
        crop_box(box, width, height)
        for box in boxes
    ]

    crops = [
        image.crop(tuple(box))
        for box in pixel_boxes
    ]

    clip_scores = score_images(crops, inp["prompt"])

    rows = []

    for idx, (original_box, pixel_box, b2, clip) in enumerate(
        zip(boxes, pixel_boxes, b2_scores, clip_scores),
        start=1
    ):
        rows.append({
            "rank": idx,
            "original_box_xyxy": original_box,
            "box_xyxy": pixel_box,
            "b2_score": float(b2),
            "clip_cosine_target": float(clip),
        })

    result = {
        "query_id": qid,
        "image_id": pred["image_id"],
        "image_path": inp["image_path"],
        "prompt": inp["prompt"],
        "text_prompt": f"a photo of {inp['prompt']}",
        "clip_model": MODEL_ID,
        "device": DEVICE,
        "n_boxes": len(rows),
        "rows_original_order": rows,
        "rows_sorted_by_clip": sorted(
            rows,
            key=lambda x: x["clip_cosine_target"],
            reverse=True
        ),
    }

    output = OUT / f"{qid}_clip_scores.json"

    output.write_text(
        json.dumps(result, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )

    total_boxes += len(rows)

    summary.append({
        "query_id": qid,
        "n_boxes": len(rows),
        "output_file": str(output.relative_to(ROOT)),
    })

    print(
        f"PASS {qid}: {len(rows)} boxes",
        flush=True
    )

# 4. Record run configuration
config = {
    "model_id": MODEL_ID,
    "model_revision": getattr(model.config, "_commit_hash", None),
    "device": DEVICE,
    "batch_size": BATCH_SIZE,
    "processor_use_fast": False,
    "text_template": "a photo of {prompt}",
    "torch_version": torch.__version__,
    "transformers_version": transformers.__version__,
    "inputs_sha256": sha256(INPUTS),
    "prediction_sha256": {
        str(p.relative_to(ROOT)): sha256(p)
        for p in PRED_FILES
    },
    "uses_ground_truth_for_scoring": False,
    "status": "scores_only_no_filtering",
}

(OUT / "run_config.json").write_text(
    json.dumps(config, indent=2, ensure_ascii=False),
    encoding="utf-8"
)

(OUT / "summary.json").write_text(
    json.dumps(summary, indent=2, ensure_ascii=False),
    encoding="utf-8"
)

print("\nTOTAL QUERIES:", len(summary))
print("TOTAL SCORED BOXES:", total_boxes)
print("OUTPUT:", OUT)
print("P4 ALL15 PASS")
