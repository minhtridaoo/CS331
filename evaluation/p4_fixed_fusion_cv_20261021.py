import csv
import json
import math
from pathlib import Path

ROOT = Path("results/countgdpp")
SCORES = ROOT / "p4_clip_all15_20261020"
PREVIOUS = ROOT / "p4_count_cv_20261020/per_query.csv"
OUT = ROOT / "p4_fixed_fusion_cv_20261021"

if OUT.exists():
    raise SystemExit("Output exists; do not overwrite.")

with PREVIOUS.open(encoding="utf-8", newline="") as f:
    previous_rows = list(csv.DictReader(f))

assert len(previous_rows) == 15
previous = {r["query_id"]: r for r in previous_rows}
assert len(previous) == 15

data = {}

for qid, prev in previous.items():
    path = SCORES / f"{qid}_clip_scores.json"
    obj = json.loads(path.read_text(encoding="utf-8"))

    rows = obj["rows_original_order"]

    assert obj["query_id"] == qid
    assert obj["image_id"] == prev["image_id"]
    assert obj["n_boxes"] == len(rows)
    assert [x["rank"] for x in rows] == list(
        range(1, len(rows) + 1)
    )

    for r in rows:
        assert all(
            math.isfinite(float(r[k]))
            for k in ["b2_score", "clip_cosine_target"]
        )

    data[qid] = {
        "image_id": obj["image_id"],
        "gt": int(prev["gt_count"]),
        "rows": rows,
    }

assert sum(len(x["rows"]) for x in data.values()) == 481

images = sorted({x["image_id"] for x in data.values()})
assert len(images) == 5

def calculate_metrics(pairs):
    errors = [abs(pred - gt) for pred, gt in pairs]
    return {
        "MAE": sum(errors) / len(errors),
        "RMSE": math.sqrt(
            sum(e * e for e in errors) / len(errors)
        ),
        "exact_count": sum(e == 0 for e in errors),
    }

def get_bounds(train_ids, key):
    vals = [
        float(r[key])
        for qid in train_ids
        for r in data[qid]["rows"]
    ]
    return (min(vals), max(vals))

def normalize(value, bounds):
    low, high = bounds
    if high == low:
        return 0.5

    value = (float(value) - low) / (high - low)
    return max(0.0, min(1.0, value))

def combined_score(row, bounds):
    b2 = normalize(row["b2_score"], bounds["B2"])
    clip = normalize(
        row["clip_cosine_target"], bounds["CLIP"]
    )
    return 0.5 * b2 + 0.5 * clip

def count_kept(qid, bounds, threshold):
    return sum(
        combined_score(r, bounds) >= threshold
        for r in data[qid]["rows"]
    )

def choose_threshold(train_ids, bounds):
    vals = sorted({
        combined_score(r, bounds)
        for qid in train_ids
        for r in data[qid]["rows"]
    })

    assert vals

    candidates = [vals[0] - 1e-6]
    candidates += [
        (a + b) / 2
        for a, b in zip(vals[:-1], vals[1:])
    ]
    candidates.append(vals[-1] + 1e-6)

    best_key = None
    best_threshold = None

    for threshold in candidates:
        pairs = [
            (
                count_kept(qid, bounds, threshold),
                data[qid]["gt"]
            )
            for qid in train_ids
        ]

        m = calculate_metrics(pairs)
        criterion = (
            m["MAE"],
            m["RMSE"],
            threshold
        )

        if best_key is None or criterion < best_key:
            best_key = criterion
            best_threshold = threshold

    return best_threshold

folds = []
results = {}

for test_image in images:
    train_ids = sorted(
        qid for qid in data
        if data[qid]["image_id"] != test_image
    )

    test_ids = sorted(
        qid for qid in data
        if data[qid]["image_id"] == test_image
    )

    assert len(train_ids) == 12
    assert len(test_ids) == 3

    bounds = {
        "B2": get_bounds(train_ids, "b2_score"),
        "CLIP": get_bounds(train_ids, "clip_cosine_target")
    }

    threshold = choose_threshold(train_ids, bounds)

    folds.append({
        "test_image": test_image,
        "train_ids": train_ids,
        "test_ids": test_ids,
        "bounds": bounds,
        "threshold": threshold
    })

    for qid in test_ids:
        results[qid] = {
            "image_id": test_image,
            "gt": data[qid]["gt"],
            "combined_count": count_kept(
                qid, bounds, threshold
            ),
            "selected_threshold": threshold
        }

assert len(results) == 15

fusion = calculate_metrics([
    (results[qid]["combined_count"], results[qid]["gt"])
    for qid in sorted(results)
])

baselines = {}

for method in [
    "B2_original",
    "B2_threshold",
    "CLIP_threshold"
]:
    baselines[method] = calculate_metrics([
        (int(previous[qid][method]), data[qid]["gt"])
        for qid in sorted(data)
    ])

assert abs(baselines["B2_original"]["MAE"] - 22.0) < 1e-8
assert abs(baselines["B2_threshold"]["MAE"] - 4.6) < 1e-8
assert abs(baselines["CLIP_threshold"]["MAE"] - 6.8) < 1e-8

report = {
    "experiment": "fixed_half_half_score_fusion",
    "method": "train_only_minmax_then_equal_weight",
    "evaluation": "five_fold_leave_one_image_out",
    "scope": "exploratory_dev_only",
    "weight_b2": 0.5,
    "weight_clip": 0.5,
    "baselines": baselines,
    "fusion": fusion,
    "folds": folds,
    "per_query": results,
    "limitations": [
        "No independent holdout",
        "Fusion design motivated by prior pilot observations",
        "Count metrics do not verify correct object class",
        "Normalization and threshold fitted on training images",
        "No claim of generalization or improvement"
    ]
}

OUT.mkdir(parents=True)

(OUT / "report.json").write_text(
    json.dumps(report, ensure_ascii=False, indent=2),
    encoding="utf-8"
)

print("\nP4 FIXED FUSION CROSS-VALIDATION")
print("Method             MAE       RMSE      Exact")

for name, m in {
    **baselines,
    "B2_CLIP_fusion": fusion
}.items():
    print(
        f"{name:<19} "
        f"{m['MAE']:<9.4f} "
        f"{m['RMSE']:<9.4f} "
        f"{m['exact_count']}/15"
    )

print("\nFOLD THRESHOLDS")
for fold in folds:
    print(
        fold["test_image"],
        round(fold["threshold"], 6)
    )

print("\nSaved:", OUT)
print("P4 FUSION CV PASS")
