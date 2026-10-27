# P4 – CLIP Exploratory Findings

**Date:** 2026-10-21

**Status:** Exploratory development results; pending label verification.

## 1. Count evaluation – 15 queries, 5 images

| Method | MAE | RMSE | Exact |
|---|---:|---:|---:|
| B2 original | 22.0000 | 30.0910 | 1/15 |
| B2 threshold | 4.6000 | 6.6182 | 1/15 |
| CLIP threshold | 6.8000 | 8.8468 | 0/15 |
| B2 + CLIP (50/50) | 5.8000 | 7.7932 | 0/15 |

Evaluation: leave-one-original-image-out cross-validation on five development images.

## 2. Object-level review – 4 selected queries

**Naming clarification (22 October):** `B2` below means the **B2 confidence filter with CV thresholds**, not unfiltered B2. `CLIP` means the CLIP threshold filter; `Fusion` uses the corresponding CV-fold threshold and normalization. These tables do not use the later full-development frozen thresholds.

`Correct` counts distinct target objects, `Wrong` non-target boxes, `Duplicate` extra target boxes, and `Missed` target objects without any retained box. Useful-box rate = Correct / Kept; object recall = Correct / 22 for the totals. These manual-review quantities are provisional, not a formal detection benchmark.

| Method | Kept | Correct | Wrong | Duplicate | Missed | Useful-box rate | Object recall |
|---|---:|---:|---:|---:|---:|---:|---:|
| B2 | 22 | 12 | 10 | 0 | 10 | 54.55% | 54.55% |
| CLIP | 20 | 9 | 10 | 1 | 13 | 45.00% | 40.91% |
| Fusion | 24 | 16 | 8 | 0 | 6 | 66.67% | 72.73% |

### Per-query results

| Query | Method | Kept | Correct | Wrong | Duplicate | Missed |
|---|---|---:|---:|---:|---:|---:|
| q03_1 | B2 | 10 | 6 | 4 | 0 | 0 |
| q03_1 | CLIP | 1 | 0 | 1 | 0 | 6 |
| q03_1 | Fusion | 12 | 6 | 6 | 0 | 0 |
| q03_2 | B2 | 4 | 4 | 0 | 0 | 2 |
| q03_2 | CLIP | 5 | 5 | 0 | 0 | 1 |
| q03_2 | Fusion | 5 | 5 | 0 | 0 | 1 |
| q03_3 | B2 | 6 | 0 | 6 | 0 | 6 |
| q03_3 | CLIP | 1 | 0 | 1 | 0 | 6 |
| q03_3 | Fusion | 1 | 1 | 0 | 0 | 5 |
| q05_2 | B2 | 2 | 2 | 0 | 0 | 2 |
| q05_2 | CLIP | 13 | 4 | 8 | 1 | 0 |
| q05_2 | Fusion | 6 | 4 | 2 | 0 | 0 |

## 3. Interpretation

- B2 threshold gives the lowest count MAE (4.6).
- Fixed 50/50 Fusion has higher count MAE (5.8).
- In four selected object-level reviews, Fusion retains 16 distinct target objects versus 12 for B2 threshold.
- The object-level improvement does not establish generalization to unseen images.
- Count accuracy and correct-object selection can disagree.

## 4. Negative experimental results

- CLIP-only threshold: count MAE 6.8.
- Singular prompts did not improve Top-K results across q03_1, q03_2 and q03_3.
- Fixed 50/50 Fusion did not outperform B2 threshold on count MAE.

## 5. Limitations

- Only five development images and fifteen queries.
- Three of four object-reviewed queries share image mcac_200.
- q03 per-box labels are preliminary assistant visual annotations.
- q05_2 uses an earlier manual object cross-check.
- Approaches were explored after inspecting development results.
- No independent untouched holdout evaluation.
- Object review is not a formal IoU-based detection benchmark.

## 6. Decision

- Preserve B2 threshold as the count-error baseline.
- Preserve fixed 50/50 Fusion as an object-selection candidate.
- Do not tune further on the same five images.
- Obtain independent verification of object labels.
- Freeze configurations before testing on genuinely unseen images.

## 7. Evidence files

- results/countgdpp/p4_count_cv_20261020/
- results/countgdpp/p4_fixed_fusion_cv_20261021/report.json
- results/countgdpp/p4_fusion_object_review_20261021.json
- results/countgdpp/p4_rank_diagnostic_20261021.json
- results/countgdpp/p4_prompt_number_20261021/report.json
- results/countgdpp/p4_class_score_analysis_20261021.json

## 8. Artifact audit and continuation — 22 October 2026

[Artifact consistency audit](P4_AUDIT_20261022.md) verified saved IDs/scores, source hashes, image-disjoint CV folds, saved threshold applications, normalization bounds and arithmetic. It did not run inference or certify the visual labels. The 47-box blank review ZIP exists and is readable; independent annotation remains pending.

The two candidates are already frozen in [this JSON](../results/countgdpp/p4_candidate_freeze_20261021.json). Full-dev fitted MAE values (4.333333 / 4.4) are not the CV values above and are not independent test results. Continue with the [new-data and runner plan](../roadmap/P4_TIEP_THEO.md); no unseen-data result is available yet.
