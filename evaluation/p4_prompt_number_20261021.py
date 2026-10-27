import csv
import json
import hashlib
from pathlib import Path
from collections import defaultdict
from statistics import mean

import torch
from PIL import Image
from transformers import CLIPModel, CLIPProcessor

ROOT = Path.cwd()
SOURCE = ROOT / "results/countgdpp"
OUT = SOURCE / "p4_prompt_number_20261021"

MODEL_ID = "openai/clip-vit-base-patch32"
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

QUERIES = {
    "q03_1": (
        "a photo of a pen",
        SOURCE / "p4_review_q03_1_20261020/q03_1_annotation_review_assistant_20261021.csv"
    ),
    "q03_2": (
        "a photo of a ruler",
        SOURCE / "p4_review_q03_2_20261020/q03_2_annotation_review_assistant_20261020.csv"
    ),
    "q03_3": (
        "a photo of a pencil",
        SOURCE / "p4_review_q03_3_20261020/q03_3_annotation_review_assistant_20261020.csv"
    ),
}

if OUT.exists():
    raise SystemExit("Output exists. Do not overwrite.")

print("Loading CLIP:", MODEL_ID, flush=True)

processor = CLIPProcessor.from_pretrained(
    MODEL_ID, use_fast=False
)
model = CLIPModel.from_pretrained(MODEL_ID).to(DEVICE)
model.eval()

@torch.inference_mode()
def score_crops(crops, prompt):
    text = processor(
        text=[prompt],
        return_tensors="pt",
        padding=True
    )
    text = {k: v.to(DEVICE) for k, v in text.items()}

    tf = model.get_text_features(**text)
    tf = torch.nn.functional.normalize(tf, dim=-1)

    result = []

    for start in range(0, len(crops), 2):
        group = crops[start:start + 2]

        images = processor(
            images=group,
            return_tensors="pt"
        )

        pixels = images["pixel_values"].to(DEVICE)

        vf = model.get_image_features(pixel_values=pixels)
        vf = torch.nn.functional.normalize(vf, dim=-1)

        result.extend((vf @ tf.T)[:, 0].cpu().tolist())

    return result

def compute_auc(rows, labels, key):
    positives = [
        r[key] for r in rows if labels[r["rank"]]["target"]
    ]
    negatives = [
        r[key] for r in rows if not labels[r["rank"]]["target"]
    ]

    return sum(
        1 if p > n else (0.5 if p == n else 0)
        for p in positives
        for n in negatives
    ) / (len(positives) * len(negatives))

report = {}

# Stage 1: score without reading ground-truth annotations.
for qid, (new_prompt, ann_path) in QUERIES.items():
    source_path = SOURCE / f"p4_clip_all15_20261020/{qid}_clip_scores.json"
    data = json.loads(source_path.read_text(encoding="utf-8"))
    rows = data["rows_original_order"]

    with Image.open(ROOT / data["image_path"]) as image_file:
        image = image_file.convert("RGB")

    crops = [
        image.crop(tuple(r["box_xyxy"]))
        for r in rows
    ]

    new_scores = score_crops(crops, new_prompt)

    scored = [
        {
            "rank": r["rank"],
            "visual_box": r["box_xyxy"],
            "plural_score": r["clip_cosine_target"],
            "singular_score": float(score)
        }
        for r, score in zip(rows, new_scores)
    ]

    report[qid] = {
        "old_prompt": data["text_prompt"],
        "new_prompt": new_prompt,
        "annotation_source": str(ann_path.relative_to(ROOT)),
        "rows": scored,
    }

# Stage 2: use preliminary labels for diagnostic evaluation.
print("\nP4 PROMPT NUMBER DIAGNOSTIC")
print("Query    Prompt     TopK correct    AUC")

for qid, (_, ann_path) in QUERIES.items():
    with ann_path.open(encoding="utf-8-sig", newline="") as f:
        raw = list(csv.DictReader(f))

    labels = {
        int(r["rank"]): {
            "target": r["is_target"].strip().lower() == "true",
            "object_id": r["visual_object_id"],
            "visual_class": r["visual_class"]
        }
        for r in raw
    }

    rows = report[qid]["rows"]

    assert len(labels) == len(rows)
    assert set(labels) == {r["rank"] for r in rows}

    target_ids = {
        x["object_id"]
        for x in labels.values()
        if x["target"]
    }

    assert len(target_ids) == 6

    results = {}

    for method, key in [
        ("Plural", "plural_score"),
        ("Singular", "singular_score")
    ]:
        ranked = sorted(
            rows,
            key=lambda x: (-x[key], x["rank"])
        )

        top = ranked[:len(target_ids)]

        correct_ids = {
            labels[x["rank"]]["object_id"]
            for x in top
            if labels[x["rank"]]["target"]
        }

        auc = compute_auc(rows, labels, key)

        results[method] = {
            "correct_topk": len(correct_ids),
            "topk": len(target_ids),
            "auc": auc,
            "top_ranks": [x["rank"] for x in top],
        }

        print(
            f"{qid:<8} "
            f"{method:<10} "
            f"{len(correct_ids)}/{len(target_ids):<11} "
            f"{auc:.4f}"
        )

    grouped = defaultdict(lambda: {"plural": [], "singular": []})

    for r in rows:
        cls = labels[r["rank"]]["visual_class"]
        grouped[cls]["plural"].append(r["plural_score"])
        grouped[cls]["singular"].append(r["singular_score"])

    class_means = {
        cls: {
            "plural_mean": mean(values["plural"]),
            "singular_mean": mean(values["singular"])
        }
        for cls, values in grouped.items()
    }

    report[qid]["results"] = results
    report[qid]["class_means"] = class_means

    print("Class mean scores:")
    for cls, values in sorted(class_means.items()):
        print(
            f"  {cls}: "
            f"plural={values['plural_mean']:.4f}, "
            f"singular={values['singular_mean']:.4f}"
        )

OUT.mkdir(parents=True)

(OUT / "report.json").write_text(
    json.dumps({
        "model": MODEL_ID,
        "device": DEVICE,
        "processor_use_fast": False,
        "experiment": "plural_vs_singular_prompt",
        "scope": "exploratory_development_only",
        "cases": report,
        "limitations": [
            "Prompt revision motivated by observed development errors",
            "Annotations for q03 cases are preliminary",
            "TopK uses the true object count for diagnosis",
            "No independent holdout evaluation",
            "No model fine-tuning or threshold optimization",
            "Cosine scores are not calibrated probabilities"
        ]
    }, ensure_ascii=False, indent=2),
    encoding="utf-8"
)

print("\nSaved:", OUT / "report.json")
print("P4 PROMPT NUMBER PASS")
