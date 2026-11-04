"""Score a P1 controls table (experiments/countgdpp/p1_controls.py) against GT (CPU, saved files only; GT is read
here, never by the runners).

Metrics per method (plan section 5.2): MAE_all, RMSE_all, MAE_present (+RMSE, exact), MeanAbsentCount and
FPR_absent (share of absent queries counted > 0); for P methods also how many queries had no verified exemplar.
Paired comparisons (plan section 3.5): per query better/worse/same and the mean |error| difference, on all queries
and on present queries, with an image-level bootstrap 95% CI (all queries of a drawn image, 5000 draws, seed 331,
same procedure as p4_unseen_score.py). Few images = wide, unreliable intervals; say so when reporting.
Optional --annotations: MUCCA point-in-box proxy for present queries (needs class_id in the manifest). It is an
automatic approximation, not the human box review.

Example (from CS331 root):
  python evaluation/evaluate_research.py --controls results/countgdpp/p1_pilot_colab_20261103_1519_controls \
      --manifest experiments/countgdpp/m4_inputs/manifest.csv --run-id p1_pilot_colab_20261103_1519_controls_eval
"""
import argparse
import csv
import hashlib
import json
import math
import random
import re
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
N_BOOT, SEED = 5000, 331


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


def comparisons_for(taus):
    """(reference, candidate) pairs from plan section 3.5; diff < 0 means the candidate errs less."""
    pairs = [("B2", "B2+S"), ("B2", "B2+F"), ("B0", "B0+F"), ("B2", "B0"), ("B0+F", "B2+F")]
    for t in taus:
        pairs += [("B2", t), ("B2+F", t + "+F"), ("B0+F", t + "+F"), ("B0", t + "+F")]
    return pairs


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--controls", required=True, help="p1_controls.py output folder, relative to CS331")
    ap.add_argument("--manifest", required=True, help="Manifest CSV with presence_status and gt_count, relative to CS331")
    ap.add_argument("--annotations", help="MUCCA annotations.json for the point-in-box proxy (absolute or relative to CS331)")
    ap.add_argument("--run-id", required=True, help="New folder under results/countgdpp; never overwritten")
    args = ap.parse_args()
    if not re.fullmatch(r"[A-Za-z0-9_-]+", args.run_id):
        raise ValueError("Invalid run ID")
    out = ROOT / "results/countgdpp" / args.run_id
    if out.exists():
        raise SystemExit("Output exists; use a new run ID")

    ctrl = ROOT / args.controls
    cfg = json.loads((ctrl / "run_config.json").read_text(encoding="utf-8"))
    if cfg.get("runner") != "p1_controls.py":
        raise ValueError("Not a p1_controls.py output folder")
    counts = {r["query_id"]: r for r in csv.DictReader((ctrl / "per_query_counts.csv").open(encoding="utf-8", newline=""))}
    kept = json.loads((ctrl / "kept_boxes.json").read_text(encoding="utf-8"))
    sources = cfg["sources"]
    taus = [s for s in sources if s not in ("B0", "B2")]
    methods = [m for s in sources for m in (s, s + "+S", s + "+F")]
    man_path = ROOT / args.manifest
    man = {r["query_id"]: r for r in csv.DictReader(man_path.open(encoding="utf-8-sig", newline=""))}
    missing = sorted(set(counts) - set(man))
    if missing:
        raise ValueError(f"Queries missing from the manifest: {missing}")
    for qid, r in counts.items():
        if man[qid]["image_id"] != r["image_id"] or man[qid]["presence_status"] not in ("present", "absent"):
            raise ValueError(f"Manifest row does not fit {qid}")
        if man[qid]["presence_status"] == "absent" and int(man[qid]["gt_count"]) != 0:
            raise ValueError(f"Absent query with gt_count != 0: {qid}")

    rows = []
    for qid in sorted(counts):
        m, c = man[qid], counts[qid]
        row = dict(query_id=qid, image_id=m["image_id"], prompt=m["prompt"], presence=m["presence_status"], gt=int(m["gt_count"]))
        row.update({f"pred_{k}": int(c[k]) for k in methods})
        row.update({f"{t}_n_pseudo": int(c[f"{t}_n_pseudo"]) for t in ["B2", *taus]})
        rows.append(row)
    pres = [r for r in rows if r["presence"] == "present"]
    absn = [r for r in rows if r["presence"] == "absent"]

    summary = {}
    for meth in methods:
        k = f"pred_{meth}"
        summary[meth] = dict(all=count_metrics([(r[k], r["gt"]) for r in rows]),
                             present=count_metrics([(r[k], r["gt"]) for r in pres]),
                             absent=dict(n=len(absn), MeanAbsentCount=sum(r[k] for r in absn) / len(absn),
                                         FPR_absent=sum(r[k] > 0 for r in absn) / len(absn)) if absn else None)
        src = meth.split("+")[0]
        if src in taus:
            summary[meth]["no_pseudo_queries"] = sum(r[f"{src}_n_pseudo"] == 0 for r in rows)

    def paired(a, b, subset):
        sub = rows if subset == "all" else pres
        ea = {r["query_id"]: abs(r[f"pred_{a}"] - r["gt"]) for r in sub}
        eb = {r["query_id"]: abs(r[f"pred_{b}"] - r["gt"]) for r in sub}
        better = sum(eb[q] < ea[q] for q in ea); worse = sum(eb[q] > ea[q] for q in ea)
        imgs = sorted({r["image_id"] for r in sub})
        by_img = {i: [r["query_id"] for r in sub if r["image_id"] == i] for i in imgs}
        rng = random.Random(SEED); diffs = []
        for _ in range(N_BOOT):
            s = [q for i in (rng.choice(imgs) for _ in imgs) for q in by_img[i]]
            diffs.append(sum(eb[q] - ea[q] for q in s) / len(s))
        diffs.sort()
        return dict(comparison=f"{b} vs {a}", subset=subset, n_queries=len(sub), n_images=len(imgs), better=better, worse=worse,
                    same=len(ea) - better - worse, mean_abs_err_diff=sum(eb[q] - ea[q] for q in ea) / len(ea),
                    bootstrap_images_95ci=[diffs[int(0.025 * N_BOOT) - 1], diffs[int(0.975 * N_BOOT) - 1]])

    comparisons = [paired(a, b, s) for a, b in comparisons_for(taus) for s in (["all", "present"] if absn else ["all"])]

    proxy = None
    if args.annotations:
        if not all("class_id" in man[q] and man[q]["class_id"] for q in counts):
            raise ValueError("Point-in-box proxy needs class_id in the manifest")
        ann_path = Path(args.annotations) if Path(args.annotations).is_absolute() else ROOT / args.annotations
        ann = json.loads(ann_path.read_text(encoding="utf-8"))
        present_of_image = defaultdict(list)
        for q in counts:
            if man[q]["presence_status"] == "present":
                present_of_image[man[q]["image_id"]].append(int(man[q]["class_id"]))
        proxy = {meth: dict(target_pts_covered=0, target_pts_total=0, kept_boxes=0, boxes_with_target=0,
                            boxes_other_only=0, boxes_other_query=0, boxes_no_point=0) for meth in methods}
        for r in pres:
            qid = r["query_id"]
            a = ann[r["image_id"] + ".jpg"]
            pts = list(zip(a["points"], a["classes"]))
            target = int(man[qid]["class_id"])
            other_q = {c for c in present_of_image[r["image_id"]] if c != target}
            for meth in methods:
                src, _, flt = meth.partition("+")
                boxes = [x["box_xyxy"] for x in kept[src][qid] if not flt or x["keep_" + flt]]
                assert len(boxes) == r[f"pred_{meth}"]
                p = proxy[meth]
                p["target_pts_covered"] += sum(any(inside(pt, b) for b in boxes) for pt, c in pts if c == target)
                p["target_pts_total"] += r["gt"]
                p["kept_boxes"] += len(boxes)
                for b in boxes:
                    cl = {c for pt, c in pts if inside(pt, b)}
                    if target in cl:
                        p["boxes_with_target"] += 1
                    elif cl:
                        p["boxes_other_only"] += 1
                        p["boxes_other_query"] += bool(cl & other_q)
                    else:
                        p["boxes_no_point"] += 1

    out.mkdir(parents=True)
    with (out / "per_query.csv").open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]), lineterminator="\n")
        w.writeheader(); w.writerows(rows)
    result = dict(summary=summary, comparisons=comparisons, proxy_present=proxy)
    (out / "metrics.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    run_cfg = dict(scorer="evaluate_research.py", scorer_sha256=sha(Path(__file__)), controls=args.controls,
                   controls_counts_sha256=sha(ctrl / "per_query_counts.csv"), controls_kept_sha256=sha(ctrl / "kept_boxes.json"),
                   manifest=args.manifest, manifest_sha256=sha(man_path), annotations=args.annotations,
                   bootstrap=dict(unit="image", draws=N_BOOT, seed=SEED, ci="2.5/97.5 percentile of paired mean |error| difference"),
                   note="GT read only here. Proxy columns are an automatic point-in-box approximation, not the human review.")
    (out / "run_config.json").write_text(json.dumps(run_cfg, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"{len(rows)} queries ({len(pres)} present, {len(absn)} absent), {len({r['image_id'] for r in rows})} images")
    print(f"{'method':<14}{'MAE_all':>8}{'MAE_pres':>9}{'exact':>6}{'MeanAbs':>8}{'FPR_abs':>8}{'no_pseudo':>10}")
    for meth in methods:
        s = summary[meth]
        ab = s["absent"]
        print(f"{meth:<14}{s['all']['MAE']:>8.2f}{s['present']['MAE'] if s['present'] else float('nan'):>9.2f}"
              f"{s['present']['exact'] if s['present'] else 0:>6}"
              + (f"{ab['MeanAbsentCount']:>8.2f}{ab['FPR_absent']:>8.2f}" if ab else f"{'-':>8}{'-':>8}")
              + f"{s.get('no_pseudo_queries', ''):>10}")
    print()
    print(f"{'comparison (diff<0: first is better)':<34}{'subset':>8}{'better/worse/same':>19}{'diff':>8}  95% CI (image bootstrap)")
    for c in comparisons:
        print(f"{c['comparison']:<34}{c['subset']:>8}{str(c['better']) + '/' + str(c['worse']) + '/' + str(c['same']):>19}"
              f"{c['mean_abs_err_diff']:>8.2f}  [{c['bootstrap_images_95ci'][0]:.2f}, {c['bootstrap_images_95ci'][1]:.2f}]")
    print("Saved:", out)


if __name__ == "__main__":
    main()
