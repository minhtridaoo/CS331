import csv
import json
import math
import hashlib
from pathlib import Path

ROOT = Path.cwd()
INPUT = ROOT / "experiments/countgdpp/m4_inputs/first5_inputs.jsonl"
MANIFEST = ROOT / "experiments/countgdpp/m4_inputs/manifest.csv"
SCORES = ROOT / "results/countgdpp/p4_clip_all15_20261020"
OUTPUT = ROOT / "results/countgdpp/p4_count_cv_20261020"

METHODS = {
    "B2_original": None,
    "B2_threshold": "b2_score",
    "CLIP_threshold": "clip_cosine_target",
}

def read_jsonl(path):
    with path.open(encoding="utf-8") as f:
        return [json.loads(x) for x in f if x.strip()]

def sha256(path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()

# Read the exact pilot query set.
inputs = {
    x["query_id"]: x
    for x in read_jsonl(INPUT)
}
assert len(inputs) == 15, "Expected 15 input queries"

metadata = {}
with MANIFEST.open(encoding="utf-8-sig", newline="") as f:
    for row in csv.DictReader(f):
        qid = row["query_id"]
        if qid in inputs:
            if qid in metadata:
                raise ValueError(f"Duplicate GT: {qid}")
            metadata[qid] = row

assert set(metadata) == set(inputs)

data = {}
source_paths = [INPUT, MANIFEST]

for qid in sorted(inputs):
    path = SCORES / f"{qid}_clip_scores.json"
    obj = json.loads(path.read_text(encoding="utf-8"))
    source_paths.append(path)

    rows = obj["rows_original_order"]
    assert obj["query_id"] == qid
    assert obj["image_id"] == inputs[qid]["image_id"]
    assert obj["n_boxes"] == len(rows)
    assert [r["rank"] for r in rows] == list(range(1, len(rows) + 1))

    for r in rows:
        assert all(
            math.isfinite(float(r[key]))
            for key in ("b2_score", "clip_cosine_target")
        )

    gt = int(metadata[qid]["gt_count"])
    assert gt >= 0

    data[qid] = {
        "image_id": obj["image_id"],
        "gt": gt,
        "rows": rows,
    }

assert sum(len(x["rows"]) for x in data.values()) == 481

groups = sorted({x["image_id"] for x in data.values()})
assert len(groups) == 5, "Expected 5 distinct images"

def predicted_count(qid, key, threshold=None):
    rows = data[qid]["rows"]

    if key is None:
        return len(rows)

    return sum(
        float(r[key]) >= threshold
        for r in rows
    )

def metrics(pairs):
    errors = [abs(pred - gt) for pred, gt in pairs]
    n = len(errors)

    return {
        "n_queries": n,
        "MAE": sum(errors) / n,
        "RMSE": math.sqrt(sum(e * e for e in errors) / n),
        "exact_count": sum(e == 0 for e in errors),
    }

def select_threshold(train_ids, key):
    # Candidate thresholds are derived only from the training images.
    values = sorted({
        float(r[key])
        for qid in train_ids
        for r in data[qid]["rows"]
    })

    if not values:
        raise ValueError("No training scores available")

    candidates = [values[0] - 1e-6]
    candidates += [
        (a + b) / 2
        for a, b in zip(values[:-1], values[1:])
    ]
    candidates.append(values[-1] + 1e-6)

    best = None

    for threshold in candidates:
        pairs = [
            (
                predicted_count(qid, key, threshold),
                data[qid]["gt"],
            )
            for qid in train_ids
        ]

        result = metrics(pairs)

        # Primary: MAE. Secondary: RMSE.
        # Final tie-break: lower threshold.
        criterion = (
            result["MAE"],
            result["RMSE"],
            threshold,
        )

        if best is None or criterion < best[0]:
            best = (criterion, threshold)

    return best[1]

# Five folds: one image held out per fold.
predictions = {}
folds = []

for held_image in groups:
    train_ids = sorted(
        qid for qid, x in data.items()
        if x["image_id"] != held_image
    )

    test_ids = sorted(
        qid for qid, x in data.items()
        if x["image_id"] == held_image
    )

    assert len(train_ids) == 12
    assert len(test_ids) == 3

    t_b2 = select_threshold(train_ids, "b2_score")
    t_clip = select_threshold(train_ids, "clip_cosine_target")

    folds.append({
        "held_out_image": held_image,
        "training_queries": train_ids,
        "test_queries": test_ids,
        "B2_threshold": t_b2,
        "CLIP_threshold": t_clip,
    })

    for qid in test_ids:
        predictions[qid] = {
            "image_id": held_image,
            "query_id": qid,
            "gt_count": data[qid]["gt"],
            "B2_original": predicted_count(qid, None),
            "B2_threshold": predicted_count(
                qid, "b2_score", t_b2
            ),
            "CLIP_threshold": predicted_count(
                qid, "clip_cosine_target", t_clip
            ),
            "B2_selected_threshold": t_b2,
            "CLIP_selected_threshold": t_clip,
        }

assert len(predictions) == 15

results = {}
for method in METHODS:
    results[method] = metrics([
        (predictions[qid][method], data[qid]["gt"])
        for qid in sorted(predictions)
    ])

# Verify original B2 agrees with the prior pilot evaluator.
assert abs(results["B2_original"]["MAE"] - 22.0) < 1e-8
assert results["B2_original"]["exact_count"] == 1

if OUTPUT.exists():
    raise SystemExit("Output already exists. Preserve it and use a new run name.")

OUTPUT.mkdir(parents=True)

report = {
    "study": "P4 count-only exploratory image-group cross-validation",
    "split": "5-fold leave-one-original-image-out",
    "threshold_selection": "MAE then RMSE on other four dev images",
    "n_images": len(groups),
    "n_queries": len(data),
    "n_scored_boxes": 481,
    "results": results,
    "folds": folds,
    "limitations": [
        "All five images belong to development data.",
        "This is not independent holdout evaluation.",
        "Count metrics cannot establish correct object class.",
        "Count metrics cannot establish localization quality.",
        "Zero-box predictions cannot be recovered by filtering.",
        "Thresholds are reselected on training images for each fold.",
    ],
    "source_sha256": {
        str(path.relative_to(ROOT)): sha256(path)
        for path in source_paths
    },
}

(OUTPUT / "report.json").write_text(
    json.dumps(report, ensure_ascii=False, indent=2),
    encoding="utf-8"
)

rows = [predictions[qid] for qid in sorted(predictions)]

with (OUTPUT / "per_query.csv").open(
    "w", encoding="utf-8", newline=""
) as f:
    writer = csv.DictWriter(f, fieldnames=list(rows[0]))
    writer.writeheader()
    writer.writerows(rows)

print("\nP4 COUNT CROSS-VALIDATION")
print("Images:", len(groups))
print("Queries:", len(data))
print("Boxes:", 481)

print("\nMETHOD              MAE       RMSE      EXACT")
for method, result in results.items():
    print(
        f"{method:<19} "
        f"{result['MAE']:<9.4f} "
        f"{result['RMSE']:<9.4f} "
        f"{result['exact_count']}/15"
    )

print("\nTHRESHOLDS CHOSEN ON TRAINING IMAGES")
for fold in folds:
    print(
        fold["held_out_image"],
        "B2:", round(fold["B2_threshold"], 5),
        "CLIP:", round(fold["CLIP_threshold"], 5),
    )

print("\nSaved:", OUTPUT)
print("P4 COUNT CV PASS")
