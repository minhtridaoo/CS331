# CS331 — Báo cáo tình hình đồ án (25/09/2026)

Tóm tắt kế hoạch V3.2 và kết quả review vừa làm. Mọi chỗ dẫn code đã đối chiếu với repo CLIP-Count gốc (commit `ba57fd0`), các link bài báo đã mở kiểm tra từng cái.

---

## 1. Đề tài

**Tên dự kiến (chờ thầy duyệt):** *Stable to Wording, Sensitive to Targets: Improving Query Fidelity in Text-Guided Zero-Shot Object Counting*

**Câu hỏi nghiên cứu:** model đếm zero-shot dùng text có đạt được cả hai điều sau không?

- **Prompt Robustness:** đổi cách diễn đạt nhưng vẫn cùng một vật ("apples", "count the apples…") thì số đếm vẫn phải ổn định.
- **Target Sensitivity:** cùng một ảnh, hỏi "apple" và hỏi "orange" phải ra hai số khác nhau.

**Điểm khác các bài trước:** PrACo, PrACo++ và T2ICount chỉ đo vế sensitivity. Tụi mình đo cả hai vế cùng lúc, dùng prompt held-out, và có can thiệp lúc train.

## 2. Phương pháp

**Model:** CLIP-Count. Lý do chọn là model nhẹ, chạy ablation có kiểm soát trên Colab được. Không chọn vì nó chính xác hơn: T2ICount có MAE tốt hơn (11.76 so với 17.78).

**Hai can thiệp lúc train:**

1. **Cross-class mosaic:** code gốc có sẵn nhánh này nhưng đang tắt, tụi mình bật lại và mở rộng. Tile thuộc lớp khác có GT = 0. Khi viết phải dùng chữ "reactivate + extend", không được claim là ý tưởng mới.
2. **L_same:** loss teacher–student, ép density map của prompt paraphrase giống density map của tên lớp gốc.

**Ablation:**

| ID | Cấu hình | Vai trò |
|---|---|---|
| E0 | checkpoint gốc | baseline |
| E0-ft | train thêm, không đổi gì | kiểm soát tác dụng của việc train thêm |
| E1-aug | chỉ đổi prompt khi train | xem L_same có hơn augmentation không |
| E1 | + L_same | robustness |
| E2 | + mosaic | sensitivity |
| E3 | + cả hai | kỳ vọng cân bằng hai vế |

Chạy ≥2 seed cho E0-ft và E3.

## 3. Đánh giá

- **Train/tune:** FSC-147.
- **Test cuối (không dùng để tune):** PrACo (ảnh tổng hợp), MUCCA và PairTally (ảnh thật; PairTally chia INTER/INTRA và Seen/Unseen). FSC-147-S-v2 để ở mức SHOULD HAVE.
- **Metric bảng chính:** MAE, NMN, PCCN, CntF1, NPV, WPMAE.
- **Prompt:** chia thành 5 họ A–E. Template của A–D được chia train/test, riêng họ E chỉ dùng để test. Báo 2 số: họ đã gặp và họ chưa gặp.
- **Phần phụ:** chẩn đoán nhỏ VA-Count + Grounding DINO (≤2 ngày) để trả lời vấn đề 2 của thầy. T2ICount chỉ chạy inference làm dòng tham chiếu (≤1 ngày).

## 4. Roadmap 4 tuần

| Tuần | Việc |
|---|---|
| 1 | Reproduce E0, dựng PrACo, kiểm tra bộ prompt có đủ khó không (P0) |
| 2 | Làm mosaic, chia prompt, vá 3 bẫy code fine-tune |
| 3 | Train theo thứ tự E0-ft → E2 → E3 → E1 → E1-aug |
| 4 | Đánh giá cuối và viết báo cáo |

**Nếu thiếu thời gian**, cắt theo thứ tự: Gate → T2ICount → hard-pair → seed thứ 2 → thu nhỏ VA-Count → E1-aug → E1.

**Không được cắt:** E0-ft, E2, PrACo, MUCCA/PairTally, đánh giá prompt held-out.

**Hạn nộp:** chưa có thông báo. Tụi mình làm sớm.

---

## 5. Kết quả review — các lỗi cần sửa

### 5.1. Nghiêm trọng: sửa trước khi chạy E0

**imgaug 0.4.0 bị crash với NumPy 2**, mà Colab hiện mặc định dùng NumPy 2.x. `FSC147.py` import imgaug nên chạy `--mode test` cũng chết ngay lúc import. Mình đã chạy thử để xác nhận.

→ Chạy lệnh này **trước** khi cài các gói khác, rồi **restart runtime**:

```bash
pip install "numpy<2"
```

### 5.2. Số liệu hoặc lý do bị ghi sai

| Mục | Vấn đề |
|---|---|
| §9.5 | Tỉ lệ null-mosaic thực tế ≈ **1.5% toàn tập** (0.3 × 5%), không phải 5%. Density cũng không chắc bằng 0, vì tile lấy ngẫu nhiên có thể trùng lớp (`FSC147.py:370`). |
| §18, §61.2 | Dòng `run.py:157–158` bọc "a photo of" **sau** khi đã forward, nên là code chết. Tắt `use_contrast` chỉ làm lệch prompt ở validation (dòng 206), `test_step` không bao giờ bọc. Kết luận giữ `use_contrast=True` vẫn đúng, chỉ cần sửa lại lý do. |
| §9.7 | Tile hiển thị 192px, hệ số scale 0.55–0.93 (không phải 0.6–0.9). Lỗi nhỏ. |

### 5.3. Mâu thuẫn trong file

| Mục | Vấn đề |
|---|---|
| §15 và §17 | §15 ghi C, D là họ chỉ để test, nhưng §17 lại lấy một phần template của C, D để train. Cần sửa §15. |
| §23 | Có `λ_m·L_mosaic`, nhưng mosaic chỉ thay đổi dữ liệu, không có loss riêng. Bỏ λ_m hoặc định nghĩa rõ. |
| §11 và §22.1 | Hard-pair cần cặp lớp gần nhau, null-mosaic cần cặp xa nhau để nhãn sạch. Phải ghi rõ cặp nào dùng cho việc gì. |
| §20, §48 | Còn sót nhãn "V3.1". |

### 5.4. Thiếu trong thiết kế

| Vấn đề | Đề xuất |
|---|---|
| Chưa có cách đo **cùng lúc** hai vế. NPV chưa ghi đo trên tập ảnh nào. | Chạy negative test của PrACo với prompt paraphrase, và thêm hình scatter **NPV vs CntF1** cho 6 cấu hình |
| E1-aug chưa ghi tỉ lệ paraphrase | Dùng ~30% mẫu, cùng pool template với E1, để so công bằng |
| Chưa ghi prompt paraphrase q2 được sinh ở đâu (dataloader chỉ trả tên lớp) | Map lớp → template trong `training_step` |
| Text encoder CLIP bị đóng băng, chỉ CoOp/VPT/decoder được học, nên khả năng học invariance có hạn | Ghi vào limitations |
| Chưa ước tính compute | Đo thời gian mỗi epoch khi chạy thử, rồi mới chốt số epoch |

---

## 6. Kiểm tra link bài báo và MUCCA

**MUCCA đã phát hành data, tải về được.**

- Data nằm trên Zenodo (bản 1.0, đăng ngày 26/03/2026, giấy phép CC BY 4.0), một file `MUCCA_1.0.zip` (30.9 MB): https://zenodo.org/records/19231375
- **Chỉ có 200 ảnh**, nên bootstrap CI nên nâng lên mức bắt buộc khi báo kết quả trên MUCCA.
- Code đánh giá nằm trong repo PrACo (`multiclass_main.py`, `multiclass_main_statistics.py`). README chưa hướng dẫn, nên phải tự đọc code.

**Các link bài báo:** cả 7 link đều trỏ đúng bài. Những chỗ cần sửa trong file:

| Bài | Ghi chú |
|---|---|
| PrACo++ / MUCCA (2605.02752) | Chưa có venue, nên ghi là "arXiv 2026" |
| PairTally (2509.13939) | Tên thật: *"Can Current AI Models Count What We Mean, Not What They See?"*. Trích theo tên thật |
| MixCount (2605.18063) | Đây là **bài dataset** (*"The MixCount Dataset…"*). Sửa mô tả ở §4.6 |
| CountGD++ (2512.23351) | Đã xác nhận CVPR 2026 |
| T2ICount (2502.20625) | Đã xác nhận CVPR 2025 |
| PrACo, CountEx | Đúng |

**Chưa kiểm:** ý "PrACo++ có benchmark CLIP-Count" (§6 dùng ý này làm lý do chọn model). Cần mở mục thí nghiệm của bài để xác nhận.

---

## 7. Việc tiếp theo

1. Cài `numpy<2`, chạy E0 trên Colab. Mục tiêu MAE ≈ **17.45 (test) / 18.93 (val)**, lệch trong khoảng ±0.5 là chấp nhận được.
2. Đo thời gian mỗi epoch để ước tính compute.
3. Sửa doc lên V3.3 theo mục 5 và mục 6.
4. Tải MUCCA và đọc `multiclass_main.py` của PrACo.
5. Làm P0: dựng các họ prompt, đo cosine CLIP, đo NPV của E0.
