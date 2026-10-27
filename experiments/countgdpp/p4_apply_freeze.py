"""P4.6b: apply the FROZEN P4 candidates to saved CLIP score files (CPU only, no GT, no refitting).

Methods per query (same box source = final B2 boxes):
  B2_original  = all B2 boxes
  B2_threshold = keep b2_score >= freeze.b2_threshold.threshold
  Fusion_50_50 = keep 0.5*norm(b2) + 0.5*norm(clip) >= freeze.fusion_50_50.threshold,
                 norm = (v - low) / (high - low) clamped to [0, 1], bounds frozen from dev.
Rules copied from evaluation/p4_compare_count_cv_20261020.py and p4_fixed_fusion_cv_20261021.py.

Optional implementation checks (do not turn this into a new experiment):
  --check-audit results/countgdpp/p4_freeze_audit_20261021.json
      counts on the stored dev scores must equal the audit, query by query;
  --reference-scores <dir of *_clip_scores.json>
      compare re-generated scores with stored ones: max |delta| and keep decisions that flip.

Example (from CS331 root):
  python experiments/countgdpp/p4_apply_freeze.py --scores results/countgdpp/p4_clip_all15_20261020 \
      --run-id p4_freeze_devcheck_YYYYMMDD --check-audit results/countgdpp/p4_freeze_audit_20261021.json
"""
import argparse
import csv
import json
import math
import re
from pathlib import Path

from run_b0_batch import ROOT, sha, project_path

FREEZE = "results/countgdpp/p4_candidate_freeze_20261021.json"
FREEZE_SHA256 = "3c4634e79d21d0c58bd7c0e3db0972c3a3eeff6d25996c716b4def1267def4da"  # from p4_freeze_audit_20261021.json
METHODS = ("B2_original", "B2_threshold", "Fusion_50_50")


def load_freeze():
    path = project_path(FREEZE)
    if sha(path) != FREEZE_SHA256:
        raise ValueError("Freeze JSON changed since the 21/10 audit; do not apply an edited freeze")
    f = json.loads(path.read_text(encoding="utf-8"))
    fusion = f["fusion_50_50"]
    if (fusion["weight_B2"], fusion["weight_CLIP"], fusion["normalization"]) != (0.5, 0.5, "minmax_clip_0_1"):
        raise ValueError("Unexpected fusion definition")
    return dict(b2_threshold=float(f["b2_threshold"]["threshold"]),
                fusion_threshold=float(fusion["threshold"]),
                bounds={k: tuple(map(float, v)) for k, v in fusion["bounds_from_development_only"].items()},
                clip_model=fusion["clip_model"])


def normalize(value, bounds):
    low, high = bounds
    if high == low:
        return 0.5
    return max(0.0, min(1.0, (float(value) - low) / (high - low)))


def decisions(rows, fz):
    out = []
    for r in rows:
        b2, clip = float(r["b2_score"]), float(r["clip_cosine_target"])
        if not (math.isfinite(b2) and math.isfinite(clip)):
            raise ValueError("Non-finite score")
        fused = 0.5 * normalize(b2, fz["bounds"]["B2"]) + 0.5 * normalize(clip, fz["bounds"]["CLIP"])
        out.append(dict(rank=r["rank"], b2_score=b2, clip_cosine_target=clip, fusion_score=fused,
                        keep_B2_threshold=b2 >= fz["b2_threshold"], keep_Fusion_50_50=fused >= fz["fusion_threshold"]))
    return out


def load_scores(directory):
    files = sorted(directory.glob("*_clip_scores.json"))
    if not files:
        raise ValueError(f"No *_clip_scores.json in {directory}")
    data = {}
    for path in files:
        obj = json.loads(path.read_text(encoding="utf-8"))
        rows = obj["rows_original_order"]
        if obj["n_boxes"] != len(rows) or [r["rank"] for r in rows] != list(range(1, len(rows) + 1)):
            raise ValueError(f"Malformed score file: {path.name}")
        if obj["query_id"] in data:
            raise ValueError(f"Duplicate query: {obj['query_id']}")
        data[obj["query_id"]] = dict(obj=obj, rows=rows, path=path)
    return data


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--scores", required=True, help="Folder of *_clip_scores.json, relative to CS331")
    p.add_argument("--run-id", required=True, help="New folder under results/countgdpp; never overwritten")
    p.add_argument("--check-audit", help="Freeze audit JSON; per-query counts must match exactly")
    p.add_argument("--reference-scores", help="Stored score folder to compare against (dev replay check)")
    args = p.parse_args()
    if not re.fullmatch(r"[A-Za-z0-9_-]+", args.run_id):
        raise ValueError("Invalid run ID")
    out = ROOT / "results/countgdpp" / args.run_id
    if out.exists():
        raise SystemExit("Output directory exists. Use a new run ID; do not overwrite previous results.")

    fz = load_freeze()
    scores_dir = project_path(args.scores)
    data = load_scores(scores_dir)
    for q in data.values():
        if q["obj"].get("clip_model", fz["clip_model"]) != fz["clip_model"]:
            raise ValueError("Scores come from a different CLIP model")

    per_query, kept = [], {}
    for qid in sorted(data):
        d = decisions(data[qid]["rows"], fz)
        counts = dict(B2_original=len(d), B2_threshold=sum(x["keep_B2_threshold"] for x in d),
                      Fusion_50_50=sum(x["keep_Fusion_50_50"] for x in d))
        per_query.append(dict(query_id=qid, image_id=data[qid]["obj"]["image_id"], prompt=data[qid]["obj"]["prompt"], **counts))
        kept[qid] = d

    checks = {}
    if args.check_audit:
        audit_path = project_path(args.check_audit)
        audit = json.loads(audit_path.read_text(encoding="utf-8"))["per_query"]
        mismatches = []
        for row in per_query:
            ref = audit.get(row["query_id"])
            if ref is None:
                mismatches.append(dict(query_id=row["query_id"], reason="not in audit"))
            elif (row["B2_threshold"], row["Fusion_50_50"]) != (ref["B2"], ref["Fusion"]):
                mismatches.append(dict(query_id=row["query_id"], new=(row["B2_threshold"], row["Fusion_50_50"]), audit=(ref["B2"], ref["Fusion"])))
        missing = sorted(set(audit) - set(data))
        checks["audit"] = dict(path=args.check_audit, sha256=sha(audit_path), mismatches=mismatches,
                               audit_queries_missing_here=missing, passed=not mismatches and not missing)

    if args.reference_scores:
        ref_dir = project_path(args.reference_scores)
        ref = load_scores(ref_dir)
        rows = []
        for qid in sorted(set(ref) | set(data)):
            if qid not in ref or qid not in data:
                rows.append(dict(query_id=qid, status="missing_in_" + ("reference" if qid not in ref else "new")))
                continue
            a, b = ref[qid]["rows"], data[qid]["rows"]
            if len(a) != len(b):
                rows.append(dict(query_id=qid, status="n_boxes_differ", reference=len(a), new=len(b)))
                continue
            da, db = decisions(a, fz), decisions(b, fz)
            rows.append(dict(
                query_id=qid, status="compared", n_boxes=len(a),
                max_abs_box=max((abs(x - y) for ra, rb in zip(a, b) for x, y in zip(ra["original_box_xyxy"], rb["original_box_xyxy"])), default=0.0),
                max_abs_b2=max((abs(float(ra["b2_score"]) - float(rb["b2_score"])) for ra, rb in zip(a, b)), default=0.0),
                max_abs_clip=max((abs(float(ra["clip_cosine_target"]) - float(rb["clip_cosine_target"])) for ra, rb in zip(a, b)), default=0.0),
                flips_B2_threshold=[x["rank"] for x, y in zip(da, db) if x["keep_B2_threshold"] != y["keep_B2_threshold"]],
                flips_Fusion_50_50=[x["rank"] for x, y in zip(da, db) if x["keep_Fusion_50_50"] != y["keep_Fusion_50_50"]]))
        ok = all(r["status"] == "compared" and not r["flips_B2_threshold"] and not r["flips_Fusion_50_50"] for r in rows)
        checks["reference_scores"] = dict(path=args.reference_scores, per_query=rows, no_decision_flips=ok)

    out.mkdir(parents=True)
    with (out / "per_query_counts.csv").open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["query_id", "image_id", "prompt", *METHODS])
        w.writeheader()
        w.writerows(per_query)
    (out / "kept_boxes.json").write_text(json.dumps(kept, indent=2, ensure_ascii=False), encoding="utf-8")
    config = dict(runner="p4_apply_freeze.py (P4.6b)", adapter_sha256=sha(Path(__file__)), freeze=FREEZE, freeze_sha256=FREEZE_SHA256,
                  frozen_values=dict(b2_threshold=fz["b2_threshold"], fusion_threshold=fz["fusion_threshold"], bounds=fz["bounds"]),
                  comparison=">= threshold; minmax clamp [0,1]; weights 0.5/0.5; no refit, no GT, no top-K",
                  scores=args.scores, score_file_sha256={q["path"].name: sha(q["path"]) for q in data.values()},
                  uses_ground_truth=False, checks=checks)
    (out / "run_config.json").write_text(json.dumps(config, indent=2, ensure_ascii=False), encoding="utf-8")

    print(f"{'query':<10}{'B2_orig':>8}{'B2_thr':>8}{'Fusion':>8}")
    for r in per_query:
        print(f"{r['query_id']:<10}{r['B2_original']:>8}{r['B2_threshold']:>8}{r['Fusion_50_50']:>8}")
    for name, c in checks.items():
        status = c.get("passed", c.get("no_decision_flips"))
        print(f"CHECK {name}: {'PASS' if status else 'FAIL'}")
    print("Saved:", out)
    if any(not c.get("passed", c.get("no_decision_flips")) for c in checks.values()):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
