"""P4.6a: deterministic selection of the unseen MUCCA test set from annotations only (no model output).

Rule (fixed 27/10/2026 before any prediction on these images):
1. Pool = MUCCA 1.0 (Zenodo 19231375, md5 b182e445445dad017493ffb35803f816) minus the 5 dev images.
2. An image is eligible if it has a pair (X, Y) of annotated classes from DIFFERENT super-categories,
   each with MIN_POINTS <= points <= MAX_POINTS (manual checking must stay feasible).
   Pair choice inside an image: largest min(n_X, n_Y), then smaller class ids.
3. Draw N_IMAGES eligible images with random.Random(SEED).sample over the sorted eligible list.
4. Absent query: classes not annotated in the image AND from a super-category absent from the image,
   ordered by random.Random(f"{SEED}-{image_id}").shuffle. The first candidate is proposed; a human must
   confirm visually it is absent. If it is visible, take the next candidate and log why.
Writes inputs.jsonl (no GT), manifest.csv (evaluator only) and absent_candidates.csv; refuses to overwrite.

Example (from CS331 root):
  python experiments/countgdpp/p4_select_unseen.py --out experiments/countgdpp/p4_unseen_v1
"""
import argparse
import csv
import hashlib
import itertools
import json
import random
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MUCCA = ROOT / "data_external/mucca_zenodo_19231375/MUCCA_1.0"
ZIP_MD5 = "b182e445445dad017493ffb35803f816"
DEV = {"mcac_100", "mcac_11", "mcac_200", "mcac_20", "mcac_27"}
SEED = 331
N_IMAGES = 10
MIN_POINTS, MAX_POINTS = 3, 40
SUPER = {
    "tableware": ["plates", "bowls", "cups", "forks", "glasses", "knives", "spoons"],
    "furniture": ["chairs", "desks"],
    "fruit": ["cherries", "raspberries", "strawberries", "blueberries", "blackberries", "red currants",
              "grapes", "lemons", "apples", "pears", "bananas", "oranges"],
    "person": ["people"],
    "beach": ["beach umbrellas"],
    "vehicle": ["cars", "motorbikes", "bicycles", "trucks", "boats"],
    "music": ["amplifiers", "guitars"],
    "animal": ["cats", "dogs", "cows", "sheeps", "goats"],
    "building": ["balconies", "windows"],
    "smoking": ["cigaretts", "lighters"],
    "locks": ["keys", "padlocks", "key holders"],
    "stationery": ["pens", "rulers", "pencils"],
}
PROMPT_FIX = {"sheeps": "sheep", "cigaretts": "cigarettes"}  # MUCCA label typos; class id kept in manifest
FIELDS = ["schema_version", "image_id", "query_id", "source_group_id", "image_path", "class_id", "target_class", "prompt",
          "presence_status", "gt_count", "split", "pair_id", "source_url", "license_note", "verified_by", "uncertainty_note"]


def md5(path):
    h = hashlib.md5()
    with path.open("rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--out", required=True, help="New folder relative to CS331")
    args = p.parse_args()
    out = (ROOT / args.out).resolve()
    if not out.is_relative_to(ROOT):
        raise ValueError("Output must stay within CS331")
    if out.exists() and any(out.glob("*.jsonl")):
        raise SystemExit("Selection already exists; do not redraw. Use a new version folder.")
    if md5(MUCCA.parent / "MUCCA_1.0.zip") != ZIP_MD5:
        raise ValueError("MUCCA zip md5 differs from Zenodo")

    names = {int(k): v for k, v in json.loads((MUCCA / "class_mapping.json").read_text(encoding="utf-8")).items()}
    sup = {c: s for s, cs in SUPER.items() for c in cs}
    if set(sup) != set(names.values()):
        raise ValueError("Super-category table must cover the 45 MUCCA classes exactly")
    ann = json.loads((MUCCA / "annotations.json").read_text(encoding="utf-8"))

    eligible = {}
    for fname in sorted(ann):
        image_id = Path(fname).stem
        if image_id in DEV:
            continue
        counts = Counter(ann[fname]["classes"])
        pairs = [(x, y) for x, y in itertools.combinations(sorted(counts), 2)
                 if sup[names[x]] != sup[names[y]] and all(MIN_POINTS <= counts[c] <= MAX_POINTS for c in (x, y))]
        if pairs:
            eligible[image_id] = (fname, counts, min(pairs, key=lambda xy: (-min(counts[xy[0]], counts[xy[1]]), xy)))
    pool = sorted(eligible, key=lambda s: int(s.split("_")[1]))
    chosen = random.Random(SEED).sample(pool, N_IMAGES)
    print(f"Pool {len(ann) - len(DEV)} non-dev images; eligible {len(pool)}; drawn {N_IMAGES} with seed {SEED}")

    rows, inputs, absent = [], [], []
    for n, image_id in enumerate(chosen, start=1):
        fname, counts, (x, y) = eligible[image_id]
        present_sup = {sup[names[c]] for c in counts}
        candidates = sorted(c for c, name in names.items() if c not in counts and sup[name] not in present_sup)
        random.Random(f"{SEED}-{image_id}").shuffle(candidates)
        image_path = (MUCCA / "images" / fname).relative_to(ROOT).as_posix()
        queries = [(x, "present", counts[x]), (y, "present", counts[y]), (candidates[0], "absent", 0)]
        for k, (cid, status, gt) in enumerate(queries, start=1):
            qid = f"u{n:02d}_{k}"
            prompt = PROMPT_FIX.get(names[cid], names[cid])
            inputs.append(dict(schema_version=1, image_id=image_id, query_id=qid, image_path=image_path, prompt=prompt))
            rows.append(dict(schema_version=1, image_id=image_id, query_id=qid, source_group_id=image_id, image_path=image_path,
                             class_id=cid, target_class=names[cid], prompt=prompt, presence_status=status, gt_count=gt,
                             split="test_p4_unseen_v1", pair_id=image_id, source_url="https://zenodo.org/records/19231375",
                             license_note="CC-BY-4.0 (MUCCA 1.0, Ciampi et al.)",
                             verified_by="PENDING: GT = MUCCA point count; not yet visually checked" if status == "present"
                             else "PENDING: absent not yet visually confirmed by a human",
                             uncertainty_note="DRAFT until the list is locked"))
        absent.append(dict(image_id=image_id, proposed_absent=names[candidates[0]],
                           next_candidates="; ".join(names[c] for c in candidates[1:6]),
                           annotated_classes="; ".join(f"{names[c]}={counts[c]}" for c in sorted(counts)),
                           human_check="PENDING", checked_by="", date="", note=""))

    out.mkdir(parents=True, exist_ok=True)
    with (out / "inputs.jsonl").open("w", encoding="utf-8", newline="\n") as f:
        f.writelines(json.dumps(r, ensure_ascii=False) + "\n" for r in inputs)
    with (out / "manifest.csv").open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS, lineterminator="\n")
        w.writeheader(); w.writerows(rows)
    with (out / "absent_candidates.csv").open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(absent[0]), lineterminator="\n")
        w.writeheader(); w.writerows(absent)
    meta = dict(status="DRAFT_NOT_LOCKED", created="2026-10-27", rule_script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                mucca_zip_md5=ZIP_MD5, seed=SEED, n_images=N_IMAGES, min_points=MIN_POINTS, max_points=MAX_POINTS,
                eligible_pool=pool, chosen=chosen, dev_excluded=sorted(DEV), super_categories=SUPER, prompt_fix=PROMPT_FIX,
                image_sha256={i: hashlib.sha256((MUCCA / "images" / eligible[i][0]).read_bytes()).hexdigest() for i in chosen})
    (out / "selection_meta.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    for r in rows:
        print(r["query_id"], r["image_id"], r["prompt"], r["presence_status"], r["gt_count"])


if __name__ == "__main__":
    main()
