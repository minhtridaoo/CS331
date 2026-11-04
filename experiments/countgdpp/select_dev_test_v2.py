"""Draft data rule v2 (roadmap/KE_HOACH_CAI_TIEN_20261027.md section 4): new dev + test sets from MUCCA annotations only
(no model output). NOT APPROVED YET: Trí approves the rule and the sizes BEFORE the real draw.
--stats only reports the pool (no draw, no files); a draw writes a DRAFT_NOT_LOCKED folder that people then check and lock.

Rule v2-draft:
1. Pool = MUCCA 1.0 minus the 5 pilot images and the 10 LOCKED p4_unseen_v1 images (kept for error analysis/demo).
2. One present pair (X, Y) per image, each class with MIN_POINTS <= points <= MAX_POINTS:
   distinct   = different super-categories (the X/Y question of the course); every eligible image is taken;
   confusable = same super-category (e.g. fruit, tableware), only for images without a distinct pair; fills the
                remaining slots round-robin over super-categories (seeded group order per round) so every group appears.
   Pair choice inside an image as r2: prefer pairs without people, then largest min(n_X, n_Y), then class ids;
   people/chairs become X so that Y (and the hard absent) comes from the other super-category.
3. Split by image: dev quotas by largest remainder, first per pair type, then per stratum (super-categories of the
   pair) inside each type; each stratum is shuffled with a seeded RNG. Dev gets exactly N_DEV images, test the rest.
4. Absent query per image as r2: hard first (classes not annotated in the image, same super-category as Y), then
   easy (super-categories absent from the image); a human must confirm it visually and log any swap.
   --easy-absent adds a second absent query of the easy type (plan section 5.1, "if resources allow").
Writes <out>/dev/ and <out>/test/ (inputs.jsonl without GT, manifest.csv for the evaluator), absent_candidates.csv
and selection_meta.json; refuses to overwrite. Image paths point to the repo copy under data_external/.

Examples (from CS331 root):
  python experiments/countgdpp/select_dev_test_v2.py --stats
  python experiments/countgdpp/select_dev_test_v2.py --n-dev 20 --n-test 40 --out experiments/countgdpp/p1_dev_test_v2
  (--mucca C:/path/to/MUCCA_1.0 if the dataset is not under data_external/)
"""
import argparse
import csv
import hashlib
import itertools
import json
import random
from collections import Counter, defaultdict
from pathlib import Path

from p4_select_unseen import DEV as PILOT, FIELDS, PROMPT_FIX, SUPER, ZIP_MD5, md5

ROOT = Path(__file__).resolve().parents[2]
REPO_MUCCA = "data_external/mucca_zenodo_19231375/MUCCA_1.0"
FILE_SHA256 = {"annotations.json": "95d9908c367d43184fb1bda392b173107793f90b4595ba74e7e61c3cdbf2eb3f",
               "class_mapping.json": "4a9daeaef21b27e13db42c986a397fb97035f886d0094ea55bc409be1a9b355d"}  # from the Zenodo zip
UNSEEN_V1 = ROOT / "experiments/countgdpp/p4_unseen_v1/selection_meta.json"
SEED = 331
MIN_POINTS, MAX_POINTS = 3, 40


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def pick_pair(pairs, names, counts):
    x, y = min(pairs, key=lambda xy: (names[xy[0]] == "people" or names[xy[1]] == "people", -min(counts[xy[0]], counts[xy[1]]), xy))
    return (y, x) if names[y] in ("people", "chairs") else (x, y)


def largest_remainder(sizes, total):
    """Integer quotas proportional to sizes that sum to total (ties broken by stratum name)."""
    n = sum(sizes.values())
    exact = {k: v * total / n for k, v in sizes.items()}
    quota = {k: int(e) for k, e in exact.items()}
    for k in sorted(exact, key=lambda k: (-(exact[k] - quota[k]), k))[:total - sum(quota.values())]:
        quota[k] += 1
    return quota


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--stats", action="store_true", help="Report the eligible pool only; no draw, no files")
    p.add_argument("--n-dev", type=int, help="Dev images (plan options: 20 or 30)")
    p.add_argument("--n-test", type=int, help="Test images (plan options: 40 or >= 50)")
    p.add_argument("--min-points", type=int, default=MIN_POINTS)
    p.add_argument("--max-points", type=int, default=MAX_POINTS)
    p.add_argument("--seed", type=int, default=SEED)
    p.add_argument("--easy-absent", action="store_true", help="Add a second, easy absent query per image")
    p.add_argument("--mucca", default=REPO_MUCCA, help="MUCCA_1.0 folder (absolute, or relative to CS331)")
    p.add_argument("--out", help="New folder relative to CS331")
    args = p.parse_args()

    mucca = Path(args.mucca) if Path(args.mucca).is_absolute() else ROOT / args.mucca
    for name, digest in FILE_SHA256.items():
        if sha256(mucca / name) != digest:
            raise ValueError(f"{name} differs from the Zenodo MUCCA 1.0 copy")
    zip_path = mucca.parent / "MUCCA_1.0.zip"
    if zip_path.exists() and md5(zip_path) != ZIP_MD5:
        raise ValueError("MUCCA zip md5 differs from Zenodo")
    names = {int(k): v for k, v in json.loads((mucca / "class_mapping.json").read_text(encoding="utf-8")).items()}
    sup = {c: s for s, cs in SUPER.items() for c in cs}
    if set(sup) != set(names.values()):
        raise ValueError("Super-category table must cover the 45 MUCCA classes exactly")
    unseen = json.loads(UNSEEN_V1.read_text(encoding="utf-8"))
    if unseen["status"] != "LOCKED" or len(unseen["chosen"]) != 10:
        raise ValueError("p4_unseen_v1 is not the locked 10-image set")
    used = set(PILOT) | set(unseen["chosen"])
    ann = json.loads((mucca / "annotations.json").read_text(encoding="utf-8"))

    eligible = {}  # image_id -> (fname, counts, (x, y), pair_type)
    for fname in sorted(ann):
        image_id = Path(fname).stem
        if image_id in used:
            continue
        counts = Counter(ann[fname]["classes"])
        pairs = [(x, y) for x, y in itertools.combinations(sorted(counts), 2)
                 if all(args.min_points <= counts[c] <= args.max_points for c in (x, y))]
        distinct = [(x, y) for x, y in pairs if sup[names[x]] != sup[names[y]]]
        if distinct or pairs:
            kind = "distinct" if distinct else "confusable"
            eligible[image_id] = (fname, counts, pick_pair(distinct or pairs, names, counts), kind)
    by_num = lambda s: int(s.split("_")[1])
    stratum = {i: f"{e[3]}:{'-'.join(sorted({sup[names[e[2][0]]], sup[names[e[2][1]]]}))}" for i, e in eligible.items()}
    distinct_pool = sorted((i for i, e in eligible.items() if e[3] == "distinct"), key=by_num)
    groups = defaultdict(list)
    for i, e in eligible.items():
        if e[3] == "confusable":
            groups[sup[names[e[2][0]]]].append(i)
    print(f"Pool {len(ann) - len(used)} unused images (excluded {len(used)}: pilot + p4_unseen_v1); points {args.min_points}-{args.max_points}: "
          f"distinct {len(distinct_pool)}, confusable {sum(map(len, groups.values()))}")
    print("  distinct by super-category pair:", dict(sorted(Counter(stratum[i] for i in distinct_pool).items())))
    print("  confusable by super-category:", {g: len(v) for g, v in sorted(groups.items())})
    if args.stats:
        return

    if args.n_dev is None or args.n_test is None or not args.out:
        raise SystemExit("A draw needs --n-dev, --n-test and --out (sizes and rule must be approved first)")
    out = (ROOT / args.out).resolve()
    if not out.is_relative_to(ROOT):
        raise ValueError("Output must stay within CS331")
    if out.exists():
        raise SystemExit("Selection folder exists; do not redraw. Use a new version folder.")
    total = args.n_dev + args.n_test
    if total > len(eligible):
        raise SystemExit(f"Only {len(eligible)} eligible images for {total}")

    if len(distinct_pool) > total:
        chosen = random.Random(f"{args.seed}-v2-distinct").sample(distinct_pool, total)
    else:
        chosen = list(distinct_pool)
    queues = {g: random.Random(f"{args.seed}-v2-{g}").sample(sorted(v, key=by_num), len(v)) for g, v in groups.items()}
    order_rng = random.Random(f"{args.seed}-v2-rounds")
    while len(chosen) < total:
        for g in order_rng.sample(sorted(queues), len(queues)):
            if queues[g] and len(chosen) < total:
                chosen.append(queues[g].pop(0))
    members = defaultdict(list)
    for i in chosen:
        members[stratum[i]].append(i)
    kinds = Counter(s.split(":")[0] for s, v in members.items() for _ in v)
    quota = {}
    for kind, q in largest_remainder(kinds, args.n_dev).items():
        quota.update(largest_remainder({s: len(v) for s, v in members.items() if s.startswith(kind + ":")}, q))
    split = {}
    for s in sorted(members):
        drawn = random.Random(f"{args.seed}-v2-split-{s}").sample(sorted(members[s], key=by_num), len(members[s]))
        split.update({i: "dev" if k < quota[s] else "test" for k, i in enumerate(drawn)})

    rows, inputs, absent = {"dev": [], "test": []}, {"dev": [], "test": []}, []
    for part in ("dev", "test"):
        for n, image_id in enumerate(sorted((i for i in chosen if split[i] == part), key=by_num), start=1):
            fname, counts, (x, y), kind = eligible[image_id]
            present_sup = {sup[names[c]] for c in counts}
            rng = random.Random(f"{args.seed}-v2-{image_id}")
            hard = sorted(c for c, name in names.items() if c not in counts and sup[name] == sup[names[y]])
            easy = sorted(c for c, name in names.items() if c not in counts and sup[name] not in present_sup)
            rng.shuffle(hard); rng.shuffle(easy)
            candidates = hard + easy
            queries = [(x, "present", counts[x]), (y, "present", counts[y]), (candidates[0], "absent", 0)]
            if args.easy_absent:
                queries.append((next(c for c in easy if c != candidates[0]), "absent", 0))
            image_path = f"{REPO_MUCCA}/images/{fname}"
            for k, (cid, status, gt) in enumerate(queries, start=1):
                qid = f"{part[0]}{n:02d}_{k}"
                prompt = PROMPT_FIX.get(names[cid], names[cid])
                inputs[part].append(dict(schema_version=1, image_id=image_id, query_id=qid, image_path=image_path, prompt=prompt))
                rows[part].append(dict(schema_version=1, image_id=image_id, query_id=qid, source_group_id=image_id, image_path=image_path,
                                       class_id=cid, target_class=names[cid], prompt=prompt, presence_status=status, gt_count=gt,
                                       split=f"{part}_v2", pair_id=image_id, source_url="https://zenodo.org/records/19231375",
                                       license_note="CC-BY-4.0 (MUCCA 1.0, Ciampi et al.)",
                                       verified_by="PENDING: GT = MUCCA point count; not yet visually checked" if status == "present"
                                       else "PENDING: absent not yet visually confirmed by a human",
                                       uncertainty_note="DRAFT until the list is locked"))
            absent.append(dict(split=part, image_id=image_id, pair_type=kind, pair=f"{names[x]} / {names[y]}",
                               proposed_absent=names[candidates[0]],
                               proposed_type="hard_same_supercategory_as_Y" if candidates[0] in hard else "easy_other_supercategory",
                               easy_absent=names[queries[3][0]] if args.easy_absent else "",
                               next_candidates="; ".join(names[c] for c in candidates[1:6]),
                               annotated_classes="; ".join(f"{names[c]}={counts[c]}" for c in sorted(counts)),
                               human_check="PENDING", checked_by="", date="", note=""))

    for part in ("dev", "test"):
        (out / part).mkdir(parents=True)
        with (out / part / "inputs.jsonl").open("w", encoding="utf-8", newline="\n") as f:
            f.writelines(json.dumps(r, ensure_ascii=False) + "\n" for r in inputs[part])
        with (out / part / "manifest.csv").open("w", encoding="utf-8", newline="") as f:
            w = csv.DictWriter(f, fieldnames=FIELDS, lineterminator="\n")
            w.writeheader(); w.writerows(rows[part])
    with (out / "absent_candidates.csv").open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(absent[0]), lineterminator="\n")
        w.writeheader(); w.writerows(absent)
    meta = dict(status="DRAFT_NOT_LOCKED", rule="v2_draft_distinct_all_plus_confusable_round_robin", rule_script_sha256=sha256(Path(__file__)),
                mucca_zip_md5=ZIP_MD5, mucca_file_sha256=FILE_SHA256, seed=args.seed, n_dev=args.n_dev, n_test=args.n_test,
                min_points=args.min_points, max_points=args.max_points, easy_absent=args.easy_absent,
                excluded=dict(pilot=sorted(PILOT), p4_unseen_v1=sorted(unseen["chosen"])),
                eligible=dict(distinct=distinct_pool, confusable={g: sorted(v, key=by_num) for g, v in sorted(groups.items())}),
                strata={s: sorted(v, key=by_num) for s, v in sorted(members.items())}, dev_quota=quota,
                dev=sorted((i for i in chosen if split[i] == "dev"), key=by_num), test=sorted((i for i in chosen if split[i] == "test"), key=by_num),
                super_categories=SUPER, prompt_fix=PROMPT_FIX,
                image_sha256={i: sha256(mucca / "images" / eligible[i][0]) for i in chosen})
    (out / "selection_meta.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")

    for part in ("dev", "test"):
        ids = meta[part]
        present = [r["gt_count"] for r in rows[part] if r["presence_status"] == "present"]
        print(f"{part}: {len(ids)} images, {len(rows[part])} queries | pair types {dict(Counter(eligible[i][3] for i in ids))} | "
              f"super-categories {len({g for i in ids for g in stratum[i].split(':')[1].split('-')})} | "
              f"present GT median {sorted(present)[len(present) // 2]}, max {max(present)} | "
              f"hard absent {sum(a['split'] == part and a['proposed_type'].startswith('hard') for a in absent)}/{len(ids)}")
    print("Saved DRAFT (not locked):", out)


if __name__ == "__main__":
    main()
