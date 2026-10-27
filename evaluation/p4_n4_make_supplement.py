"""N4 supplement for plan F0 (hướng cái tiển/CS331_KE_HOACH_FIX_PIPELINE_DE_PUBLISH_20261027.md §2).
Same 9 queries as the N4 package. Adds, per query:
  pseudo  : the <=3 pseudo-exemplars chosen after stage 1 (E1: is the exemplar the right class / one object?)
  e3      : B2 final boxes dropped by BOTH filters that contain >= 1 MUCCA point of the target class
            (E3 candidates from the automatic proxy; reviewer checks whether they really are correct objects)
These two sheets are not blind to the method (by construction). Saved outputs only, no model run.

Example (from CS331 root): python evaluation/p4_n4_make_supplement.py
"""
import csv
import json
from pathlib import Path
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
PKG = ROOT / "results/countgdpp/p4_n4_review_package_20261027"
OUT = PKG / "bo_sung_F0"
TIERS = {"A": ["u01_1", "u02_1", "u07_1", "u08_1", "u01_3", "u07_3", "u10_3"], "B": ["u06_2", "u07_2"]}


def crops_sheet(img, items, path):
    tiles = []
    for tag, b in items:
        w, h = b[2] - b[0], b[3] - b[1]
        c = img.crop((max(0, b[0] - .15 * w), max(0, b[1] - .15 * h), min(img.width, b[2] + .15 * w), min(img.height, b[3] + .15 * h)))
        c.thumbnail((220, 220)); t = Image.new("RGB", (230, 250), "white"); t.paste(c, (5, 25))
        ImageDraw.Draw(t).text((5, 5), tag, fill="black"); tiles.append(t)
    rows = (len(tiles) + 3) // 4
    sheet = Image.new("RGB", (230 * 4, 250 * rows), "white")
    for i, t in enumerate(tiles):
        sheet.paste(t, ((i % 4) * 230, (i // 4) * 250))
    sheet.save(path, quality=92)


def main():
    if OUT.exists():
        raise SystemExit("Supplement exists; do not overwrite")
    OUT.mkdir()
    preds = {r["query_id"]: r for r in map(json.loads, (ROOT / "results/countgdpp/p4_unseen_v1_b2_20261027/predictions.jsonl").read_text(encoding="utf-8").splitlines()) if r}
    kept = json.loads((ROOT / "results/countgdpp/p4_unseen_v1_freeze_20261027/kept_boxes.json").read_text(encoding="utf-8"))
    man = {r["query_id"]: r for r in csv.DictReader((ROOT / "experiments/countgdpp/p4_unseen_v1/manifest.csv").open(encoding="utf-8", newline=""))}
    ann = json.loads((ROOT / "data_external/mucca_zenodo_19231375/MUCCA_1.0/annotations.json").read_text(encoding="utf-8"))
    inside = lambda p, b: b[0] <= p[0] <= b[2] and b[1] <= p[1] <= b[3]
    total = {"pseudo": 0, "e3": 0}
    for tier, qids in TIERS.items():
        for qid in qids:
            m, p = man[qid], preds[qid]
            img = Image.open(ROOT / m["image_path"]).convert("RGB")
            a = ann[m["image_id"] + ".jpg"]; t = int(m["class_id"]); fb = p["final_boxes"]
            name = f"{tier}_{qid}_{m['prompt'].replace(' ', '_')}"
            sets = {"pseudo": [(f"P{i}", b) for i, b in enumerate(p["pseudo_boxes"], 1)]}
            if m["presence_status"] == "present":
                drop = [r["rank"] for r in kept[qid] if not r["keep_B2_threshold"] and not r["keep_Fusion_50_50"]]
                sets["e3"] = [(f"#{r}", fb[r - 1]) for r in drop
                              if any(inside(pt, fb[r - 1]) for pt, c in zip(a["points"], a["classes"]) if c == t)]
            for kind, items in sets.items():
                if not items:
                    continue
                crops_sheet(img, items, OUT / f"{name}_{kind}_crops.jpg")
                with (OUT / f"{name}_{kind}_labels_BLANK.csv").open("w", encoding="utf-8", newline="") as f:
                    w = csv.writer(f, lineterminator="\n")
                    w.writerow(["query_id", "prompt", "kind", "tag", "x1", "y1", "x2", "y2", "label_type", "actual_class", "object_id", "note", "reviewer", "date"])
                    for tag, b in items:
                        w.writerow([qid, m["prompt"], kind, tag, *[round(v, 1) for v in b], "", "", "", "", "", ""])
                total[kind] += len(items)
            # overview: pseudo in green, e3 candidates in cyan
            scale = 2 if img.width < 900 else 1
            big = img.resize((img.width * scale, img.height * scale)); d = ImageDraw.Draw(big)
            for kind, color in (("e3", "cyan"), ("pseudo", "lime")):
                for tag, b in sets.get(kind, []):
                    bb = [v * scale for v in b]; d.rectangle(bb, outline=color, width=3); d.text((bb[0] + 2, bb[1] + 1), tag, fill=color)
            big.save(OUT / f"{name}_supplement_overview.jpg", quality=92)
            print(tier, qid, m["prompt"], {k: len(v) for k, v in sets.items()})
    (OUT / "README.md").write_text(f"""# Bổ sung F0 cho N4 — đo E1 (mẫu tự chọn sai) và E3 (Fusion xóa vật đúng)

Theo §2 của `hướng cái tiển/CS331_KE_HOACH_FIX_PIPELINE_DE_PUBLISH_20261027.md`. Dùng cùng 9 query với gói N4. Phần này **không mù**: tên file đã cho biết loại khung.

- `*_pseudo_*`: {total['pseudo']} khung mẫu tự chọn (P1–P3) mà B2 đưa vào lượt 2. Với mỗi mẫu, trả lời: đúng loại không? Có đúng **một** vật không? (`label_type`: target / wrong_class / multi_object / part / background / uncertain)
- `*_e3_*`: {total['e3']} khung B2 bị **cả hai** bộ lọc loại nhưng có chứa điểm MUCCA của loại cần đếm. Câu hỏi: đây có thật là vật đúng bị xóa nhầm (E3) không, hay là khung trùng / khung lớn bao nhiều vật / một phần vật?
- `*_supplement_overview.jpg`: khung xanh lá là mẫu tự chọn, khung xanh dương là ứng viên E3.

Điền CSV giống gói chính. Thứ tự làm: gói chính trước (review mù), phần bổ sung sau.
""", encoding="utf-8")
    print("total", total)


if __name__ == "__main__":
    main()
