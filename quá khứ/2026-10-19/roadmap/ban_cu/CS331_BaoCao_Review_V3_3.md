# CS331 — Báo cáo review bản V3.3 (25/09/2026)

Bản V3.3 đã được đối chiếu với code thật: CLIP-Count commit `ba57fd0`, repo PrACo, repo PairTally. Môi trường cũng đã được chạy thử.

**Kết luận:** V3.3 đã sửa đúng **mọi điểm** của review V3.2, và các claim mới thêm vào đều đúng. Hướng đi giữ nguyên, có thể bắt đầu làm.

Còn **1 bẫy môi trường mới** phải thêm vào Day 1, và vài chỗ cần bổ sung hoặc sửa nhỏ.

---

## 1. Các claim mới trong V3.3 đã kiểm

| Claim | Kết quả |
|---|---|
| `FSC147.py:18` import imgaug | ✅ Đúng |
| `prompt_add` bị lỗi index (`util/CLIP_caption.py:47–48`) | ✅ Đúng. Chỉ số lấy từ `close_prompt` nhưng lại tra trên toàn bộ corpus. Ví dụ "hot air balloons" ra `["glass", "design pattern", "Animal Husbandry", "gaming keyboard", "sphere"]` |
| Repo PrACo có wrapper CLIP-Count, ZSC, CounTX, VLCounter, DAVE, PseCo, CountGD, CountGD++ | ✅ Đúng (thư mục `PrACo/models/`) |
| PairTally có 681 ảnh | ✅ Đúng (README của repo) |
| §9.7: scale của self-mosaic 0.55–1.55 | ✅ Đúng (crop 150–384px → resize 212–232px) |
| §9.5: sửa sampler ở `FSC147.py:352` | ✅ Đúng dòng |

---

## 2. Vấn đề mới

### 2.1. ⚠️ Bẫy môi trường thứ hai: setuptools (phải sửa trước Day 1)

Đã chạy thử trên Python 3.12 + torch 2.x + numpy 1.26:

| setuptools | `import pytorch_lightning` (1.8.0) |
|---|---|
| ≥ 81 | ❌ Lỗi `No module named 'pkg_resources'`, do `lightning_utilities` gọi tới |
| < 81 (đã thử 80.10) | ✅ Import được, tạo `Trainer` bình thường |

Gói `clip` của OpenAI cũng dùng `pkg_resources`, nên cũng hỏng theo khi dùng setuptools mới.

→ **Sửa §61.4 và §64.2.** Cell đầu tiên của notebook phải là:

```bash
pip install "numpy<2" "setuptools<81"
```

Sau đó **Restart session**, rồi mới cài các gói còn lại.

### 2.2. MUCCA dễ chạy hơn file đang ghi

Repo PrACo **đã có sẵn metadata** của MUCCA trong `data/multiclass-dataset/`:

- `multiclass_split_images.json`: 200 ảnh, split `test`
- `multiclass_split_classes.json`, `multiclass_image_classes.txt`
- `annotations_no_scaling.json`, `class_mapping.json`, `multiclass_gt_counts.json`

→ Chỉ cần lấy **ảnh** từ file zip trên Zenodo, bỏ vào `data/multiclass-dataset/images/`. Đây là đường dẫn mặc định của `multiclass_main.py`.

Chưa kiểm được tên thư mục ảnh bên trong file zip, vì môi trường review không tải được Zenodo. Khi giải nén thì kiểm lại.

→ **Cập nhật §4.2 và Day 6 ở §48.**

### 2.3. Paraphrase-PrACo (§32.2) dễ làm hơn dự tính

- Chỗ cần sửa: `PrACo/models/clipcount_model.py`, hàm `get_text_prompt(text)`. Hàm này hiện chỉ trả thẳng tên lớp, nên thay prompt paraphrase vào đây là xong.
- Wrapper nạp checkpoint bằng `run.Model.load_from_checkpoint(..., strict=False)`, nên **checkpoint của E0-ft đến E3 cắm vào được ngay**, miễn là không đổi kiến trúc model.

→ **Ghi thêm vào §32.2 và §57.**

### 2.4. Lý do chọn LR ~1e-5 (§61.5)

- Code gốc: `lr=1e-4` (`run.py:81`), AdamW, `StepLR(step_size=100, gamma=0.33)` (`run.py:407`).
- Sau khoảng 220 epoch train gốc, LR giảm 2 lần, còn khoảng **1.1e-5**. Vậy fine-tune ở 1e-5 là nối tiếp đúng mức LR cuối của checkpoint official.
- Với 30–50 epoch fine-tune thì StepLR không kích hoạt lần nào.

→ **Ghi lý do này vào §61.5**, phòng khi bị hỏi.

---

## 3. Lỗi nhỏ

| Mục | Sửa |
|---|---|
| §49 | "Train families / Held-out test families" vẫn là cách chia cũ, đổi thành "template train/test theo §17" |
| §58 | Tiêu đề cột "Trạng thái V3.2" đổi thành V3.3 |
| §62 | Tên branch `cs331-v32` đổi thành `cs331-v33` |
| §4.6 | Con số MAE giảm 20.14% (FSC-147) / 18.3% (PairTally) của MixCount chưa kiểm được, cần đối chiếu abstract trước khi đưa vào báo cáo |

---

## 4. Checklist Day 1 (đã cập nhật)

1. Cell đầu: `pip install "numpy<2" "setuptools<81"`, rồi **Restart session**.
2. Kiểm `numpy.__version__` ra 1.x, rồi cài `pytorch_lightning==1.8.0 einops imgaug ftfy regex tqdm git+https://github.com/openai/CLIP.git`.
3. Kiểm nhanh `python -c "import imgaug, cv2, pytorch_lightning, clip"`. Không lỗi thì mới đi tiếp.
4. Tải FSC-147 và checkpoint official lên Drive, copy vào `/content/CLIP-Count/data/FSC/`.
5. Chạy E0 từ thư mục gốc repo. Mục tiêu MAE ≈ **17.45 (test) / 18.93 (val)**, lệch trong khoảng ±0.5 là chấp nhận được.
6. Ghi lại version torch / PL / numpy / setuptools thực tế.
