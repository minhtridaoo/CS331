"""P4.6d: score the locked p4_unseen_v1 run (CPU, saved files only; GT is read here, never by the runners).

Methods: B0 (= stage 1 of the same B2 run, reference only), B2_original, B2_threshold, Fusion_50_50.
Count metrics: present MAE/RMSE/exact; absent mean count and share of absent queries with count > 0.
Paired comparison per query and an image-level bootstrap of MAE differences (10 images, seed 331).

Object proxy (AUTOMATIC, from MUCCA points, NOT the human box review of protocol §4):
for each kept box, which annotated points fall inside it. Reported per present query:
  target_pts_covered  = GT points of the target class inside >= 1 kept box
  boxes_with_target   = kept boxes containing >= 1 target point
  boxes_other_only    = kept boxes containing points of other annotated classes but no target point
  boxes_other_query   = subset of boxes_other_only containing a point of the OTHER present query class (X/Y confusion)
  boxes_no_point      = kept boxes containing no annotated point
A box can contain several points; this is not AP/IoU and does not resolve duplicates.

Example (from CS331 root):
  python evaluation/p4_unseen_score.py --run-id p4_unseen_v1_eval_20261027
"""
import argparse
import csv
import hashlib
import json
import math
import random
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SET = ROOT / "experiments/countgdpp/p4_unseen_v1"
LOCKED = {"inputs.jsonl": "53e91e8151eee327cb058d70e522d4081e89ec02e64b074fce53e57cd69bc28b",
          "manifest.csv": "9161d8f44fb498e61633acdb025e2f1932e15d1300b7db669cfd7150c55daa38"}
ANN = ROOT / "data_external/mucca_zenodo_19231375/MUCCA_1.0/annotations.json"
METHODS = ["B0", "B2_original", "B2_threshold", "Fusion_50_50"]


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def inside(pt, box):
    x, y = pt
    return box[0] <= x <= box[2] and box[1] <= y <= box[3]


def count_metrics(pairs):
    if not pairs:
        return None
    e = [abs(p - g) for p, g in pairs]
    return dict(n=len(e), MAE=sum(e) / len(e), RMSE=math.sqrt(sum(x * x for x in e) / len(e)), exact=sum(x == 0 for x in e))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--b2", default="results/countgdpp/p4_unseen_v1_b2_20261027/predictions.jsonl")
    ap.add_argument("--freeze-out", default="results/countgdpp/p4_unseen_v1_freeze_20261027")
    ap.add_argument("--run-id", required=True)
    args = ap.parse_args()
    out = ROOT / "results/countgdpp" / args.run_id
    if out.exists():
        raise SystemExit("Output exists; use a new run ID")
    for f, h in LOCKED.items():
        if sha(SET / f) != h:
            raise ValueError(f"{f} differs from the locked version")
    if json.loads((SET / "selection_meta.json").read_text(encoding="utf-8"))["status"] != "LOCKED":
        raise ValueError("Set is not LOCKED")

    man = {r["query_id"]: r for r in csv.DictReader((SET / "manifest.csv").open(encoding="utf-8", newline=""))}
    b2_path, fz_dir = ROOT / args.b2, ROOT / args.freeze_out
    preds = {r["query_id"]: r for r in map(json.loads, b2_path.read_text(encoding="utf-8").splitlines()) if r}
    kept = json.loads((fz_dir / "kept_boxes.json").read_text(encoding="utf-8"))
    counts = {r["query_id"]: r for r in csv.DictReader((fz_dir / "per_query_counts.csv").open(encoding="utf-8", newline=""))}
    if not (set(man) == set(preds) == set(kept) == set(counts)):
        raise ValueError("Query sets differ between manifest, predictions and freeze output")
    if any(p["execution_status"] != "ok" for p in preds.values()):
        raise ValueError("Some prediction failed; report it instead of scoring as 0")
    ann = json.loads(ANN.read_text(encoding="utf-8"))
    names = json.loads((ANN.parent / "class_mapping.json").read_text(encoding="utf-8"))

    def kept_boxes(qid, method):
        p = preds[qid]
        if method == "B0":
            return p["stage1_boxes"]
        boxes = p["final_boxes"]
        if method == "B2_original":
            return boxes
        key = "keep_B2_threshold" if method == "B2_threshold" else "keep_Fusion_50_50"
        return [boxes[d["rank"] - 1] for d in kept[qid] if d[key]]

    present_of_image = defaultdict(list)
    for q, r in man.items():
        if r["presence_status"] == "present":
            present_of_image[r["image_id"]].append(int(r["class_id"]))

    rows = []
    for qid in sorted(man):
        m, p = man[qid], preds[qid]
        assert int(counts[qid]["B2_original"]) == p["final_count"]
        pred = dict(B0=p["stage1_count"], B2_original=p["final_count"],
                    B2_threshold=int(counts[qid]["B2_threshold"]), Fusion_50_50=int(counts[qid]["Fusion_50_50"]))
        row = dict(query_id=qid, image_id=m["image_id"], prompt=m["prompt"], presence=m["presence_status"],
                   gt=int(m["gt_count"]), no_pseudo=p["no_pseudo"], **{f"pred_{k}": v for k, v in pred.items()})
        a = ann[m["image_id"] + ".jpg"]
        pts = list(zip(a["points"], a["classes"]))
        target = int(m["class_id"])
        other_q = [c for c in present_of_image[m["image_id"]] if c != target]
        for meth in METHODS:
            boxes = kept_boxes(qid, meth)
            assert len(boxes) == pred[meth]
            if m["presence_status"] == "present":
                row[f"{meth}_target_pts_covered"] = sum(any(inside(pt, b) for b in boxes) for pt, c in pts if c == target)
            tw = oo = oq = nop = 0
            for b in boxes:
                cl = {c for pt, c in pts if inside(pt, b)}
                if target in cl:
                    tw += 1
                elif cl:
                    oo += 1
                    oq += bool(cl & set(other_q))
                else:
                    nop += 1
            row.update({f"{meth}_boxes_with_target": tw, f"{meth}_boxes_other_only": oo,
                        f"{meth}_boxes_other_query": oq, f"{meth}_boxes_no_point": nop})
        rows.append(row)

    pres = [r for r in rows if r["presence"] == "present"]
    absn = [r for r in rows if r["presence"] == "absent"]
    summary = {}
    for meth in METHODS:
        k = f"pred_{meth}"
        summary[meth] = dict(
            present=count_metrics([(r[k], r["gt"]) for r in pres]),
            absent=dict(n=len(absn), mean_count=sum(r[k] for r in absn) / len(absn),
                        share_nonzero=sum(r[k] > 0 for r in absn) / len(absn)),
            all_MAE=sum(abs(r[k] - r["gt"]) for r in rows) / len(rows),
            proxy_present=dict(
                target_pts_covered=sum(r[f"{meth}_target_pts_covered"] for r in pres),
                target_pts_total=sum(r["gt"] for r in pres),
                kept_boxes=sum(r[k] for r in pres),
                boxes_with_target=sum(r[f"{meth}_boxes_with_target"] for r in pres),
                boxes_other_only=sum(r[f"{meth}_boxes_other_only"] for r in pres),
                boxes_other_query=sum(r[f"{meth}_boxes_other_query"] for r in pres),
                boxes_no_point=sum(r[f"{meth}_boxes_no_point"] for r in pres)))

    def paired(a, b):
        ea = {r["query_id"]: abs(r[f"pred_{a}"] - r["gt"]) for r in rows}
        eb = {r["query_id"]: abs(r[f"pred_{b}"] - r["gt"]) for r in rows}
        better = sum(eb[q] < ea[q] for q in ea); worse = sum(eb[q] > ea[q] for q in ea)
        imgs = sorted({r["image_id"] for r in rows})
        by_img = {i: [r["query_id"] for r in rows if r["image_id"] == i] for i in imgs}
        rng = random.Random(331); diffs = []
        for _ in range(5000):
            s = [q for i in (rng.choice(imgs) for _ in imgs) for q in by_img[i]]
            diffs.append(sum(eb[q] - ea[q] for q in s) / len(s))
        diffs.sort()
        return dict(comparison=f"{b} vs {a} (all 30 queries)", better=better, worse=worse, same=len(ea) - better - worse,
                    mean_abs_err_diff=sum(eb[q] - ea[q] for q in ea) / len(ea),
                    bootstrap_images_95ci=[diffs[124], diffs[4874]])

    comparisons = [paired("B2_original", "B2_threshold"), paired("B2_original", "Fusion_50_50"),
                   paired("B2_threshold", "Fusion_50_50"), paired("B0", "B2_original")]

    out.mkdir(parents=True)
    with (out / "per_query.csv").open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]) + [k for k in pres[0] if k not in rows[0]], lineterminator="\n")
        w.writeheader(); w.writerows(rows)
    (out / "metrics.json").write_text(json.dumps(dict(summary=summary, comparisons=comparisons), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    cfg = dict(scorer_sha256=sha(Path(__file__)), locked_sha256=LOCKED, b2_predictions=args.b2, b2_sha256=sha(b2_path),
               freeze_out=args.freeze_out, kept_sha256=sha(fz_dir / "kept_boxes.json"),
               note="B0 = stage 1 of the same run (reference). Object columns are an automatic point-in-box proxy, not the §4 human review.")
    (out / "run_config.json").write_text(json.dumps(cfg, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(dict(summary=summary, comparisons=comparisons), ensure_ascii=False, indent=1))
    print("Saved:", out)


if __name__ == "__main__":
    main()
