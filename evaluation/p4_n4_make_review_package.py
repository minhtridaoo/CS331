"""N4 (selective human box review) package for p4_unseen_v1. Blind: boxes are numbered by B2 rank only;
which filter kept each box is written to a separate key folder to open AFTER reviewing.

Selection (fixed 27/10/2026 before looking at individual boxes; targeted error analysis, NOT a random sample):
  Tier A: people queries whose kept boxes mostly fall on other classes (u01_1, u02_1, u07_1, u08_1)
          + absent queries counted > 0 by the filters (u01_3, u07_3, u10_3)
  Tier B: u06_2, u07_2 (Fusion keeps more boxes than the score filter)
Boxes reviewed = union of boxes kept by B2_threshold or Fusion_50_50.

Example (from CS331 root): python evaluation/p4_n4_make_review_package.py
"""
import csv
import json
from pathlib import Path
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results/countgdpp/p4_n4_review_package_20261027"
TIERS = {"A": ["u01_1", "u02_1", "u07_1", "u08_1", "u01_3", "u07_3", "u10_3"], "B": ["u06_2", "u07_2"]}
LABELS = "target | duplicate | part | multi_object | wrong_class | background | uncertain"


def main():
    if OUT.exists():
        raise SystemExit("Package exists; do not overwrite")
    preds = {r["query_id"]: r for r in map(json.loads, (ROOT / "results/countgdpp/p4_unseen_v1_b2_20261027/predictions.jsonl").read_text(encoding="utf-8").splitlines()) if r}
    kept = json.loads((ROOT / "results/countgdpp/p4_unseen_v1_freeze_20261027/kept_boxes.json").read_text(encoding="utf-8"))
    inputs = {r["query_id"]: r for r in map(json.loads, (ROOT / "experiments/countgdpp/p4_unseen_v1/inputs.jsonl").read_text(encoding="utf-8").splitlines()) if r}
    (OUT / "_KEY_mo_sau_khi_review").mkdir(parents=True)
    key, total = {}, 0
    for tier, qids in TIERS.items():
        for qid in qids:
            inp, p = inputs[qid], preds[qid]
            ranks = [d["rank"] for d in kept[qid] if d["keep_B2_threshold"] or d["keep_Fusion_50_50"]]
            key[qid] = {d["rank"]: [m for m, k in (("B2_threshold", "keep_B2_threshold"), ("Fusion_50_50", "keep_Fusion_50_50")) if d[k]]
                        for d in kept[qid] if d["rank"] in ranks}
            img = Image.open(ROOT / inp["image_path"]).convert("RGB")
            scale = 2 if img.width < 900 else 1
            big = img.resize((img.width * scale, img.height * scale))
            d = ImageDraw.Draw(big)
            boxes = {r: p["final_boxes"][r - 1] for r in ranks}
            for r, b in boxes.items():
                bb = [v * scale for v in b]
                d.rectangle(bb, outline="yellow", width=2)
                d.text((bb[0] + 2, bb[1] + 1), str(r), fill="yellow")
            name = f"{tier}_{qid}_{inp['prompt'].replace(' ', '_')}"
            big.save(OUT / f"{name}_overview.jpg", quality=92)
            # crop sheet: each box with 15% margin, 4 per row
            tiles = []
            for r, b in boxes.items():
                w, h = b[2] - b[0], b[3] - b[1]
                c = img.crop((max(0, b[0] - .15 * w), max(0, b[1] - .15 * h), min(img.width, b[2] + .15 * w), min(img.height, b[3] + .15 * h)))
                c.thumbnail((220, 220)); t = Image.new("RGB", (230, 250), "white"); t.paste(c, (5, 25))
                ImageDraw.Draw(t).text((5, 5), f"#{r}", fill="black"); tiles.append(t)
            if tiles:
                rows = (len(tiles) + 3) // 4
                sheet = Image.new("RGB", (230 * 4, 250 * rows), "white")
                for i, t in enumerate(tiles):
                    sheet.paste(t, ((i % 4) * 230, (i // 4) * 250))
                sheet.save(OUT / f"{name}_crops.jpg", quality=92)
            with (OUT / f"{name}_labels_BLANK.csv").open("w", encoding="utf-8", newline="") as f:
                w = csv.writer(f, lineterminator="\n")
                w.writerow(["query_id", "prompt", "rank", "x1", "y1", "x2", "y2", "label_type", "actual_class", "object_id", "note", "reviewer", "date"])
                for r, b in boxes.items():
                    w.writerow([qid, inp["prompt"], r, *[round(v, 1) for v in b], "", "", "", "", "", ""])
            total += len(boxes)
            print(tier, qid, inp["prompt"], len(boxes))
    (OUT / "_KEY_mo_sau_khi_review" / "rank_kept_by.json").write_text(json.dumps(key, indent=2) + "\n", encoding="utf-8")
    (OUT / "README.md").write_text(f"""# N4 — review khung chọn lọc (tập p4_unseen_v1)

**Quy tắc chọn ca (chốt 27/10, trước khi xem từng khung):** phân tích lỗi có chủ đích, KHÔNG phải mẫu ngẫu nhiên. Kết quả chỉ dùng để giải thích lỗi, không thay số đếm chính.
- Tầng A (bắt buộc): {', '.join(TIERS['A'])}. Gồm 4 query "people" nhiều khung rơi vào vật loại khác, cộng 3 query vắng mặt bị báo > 0.
- Tầng B (nếu còn giờ): {', '.join(TIERS['B'])}. Fusion giữ nhiều khung hơn lọc điểm.

Tổng {total} khung = hợp các khung được ít nhất một bộ lọc giữ.

**Review mù:** khung chỉ đánh số theo rank của B2, cùng một màu. Đừng mở `_KEY_mo_sau_khi_review/` trước khi điền xong; bảng đó cho biết cách nào giữ khung nào.

**Cách điền** (quy ước §4 trong HUONG_DAN_KIEM_DU_LIEU.md): mở `*_crops.jpg` (ảnh cắt từng khung) và `*_overview.jpg` (vị trí trong ảnh), rồi điền `*_labels_BLANK.csv`, mỗi dòng một khung:
- `label_type` chọn một trong: {LABELS}
- `actual_class`: vật thật trong khung (ví dụ dogs, motorbikes)
- `object_id`: cùng một vật thì cùng id; khung trùng đánh `duplicate`
- `note`: ghi khi chưa chắc
- `reviewer` / `date`: người điền, ngày điền

Với query vắng mặt, khung nào cũng là sai; chỉ cần ghi khung đó thật ra là vật gì. Điền xong thì báo assistant để ghép với bảng tra và tính kết quả.
""", encoding="utf-8")
    print("total", total, "->", OUT)


if __name__ == "__main__":
    main()
