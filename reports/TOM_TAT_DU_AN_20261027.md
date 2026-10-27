# CS331 — Tóm tắt dự án (bản demo trước báo cáo chính thức)

**Nhóm:** Trí, Triệu · **Cập nhật:** 27/10/2026 · **Hạn báo cáo:** 02/12/2026
Bản sơ lược để nắm toàn bộ việc đã làm. Số liệu chi tiết nằm ở các file nguồn ghi cuối mỗi mục.

---

## 1. Bài toán

Đếm đối tượng zero-shot bằng câu chữ: đưa ảnh và tên loại vật, model trả về số lượng.

**Câu hỏi của thầy (bài toán X/Y):** trong cùng một ảnh có hai loại khác hẳn nhau X và Y. Hỏi X thì phải đếm X; đổi sang hỏi Y thì phải đếm Y, **không được đếm lại vật của X**. Hỏi một loại không có trong ảnh thì phải trả 0.

## 2. Model và cách làm

- **Model đếm: CountGD++** (checkpoint công khai, **không train lại**).
  - **B0:** chỉ dùng text, chạy 1 lượt.
  - **B2:** lượt 1 → model tự chọn tối đa 3 khung tốt nhất làm "mẫu" → lượt 2 đếm với text + mẫu.
- **Kiểm tái lập:** chạy lại CountGD++ trên benchmark FSCD-147 (1.190 ảnh), được MAE 8.34, để chắc môi trường chạy đúng. *(reports/BENCHMARK_FSCD147.md)*

## 3. Pilot: tìm ra lỗi (5 ảnh MUCCA, 15 query)

| | B0 | B2 |
|---|---:|---:|
| MAE | 19.4 | 22.0 |

- CountGD++ **đếm lẫn loại** rất nhiều. Ví dụ hỏi *blackberries*: thực tế 3 quả, B2 đếm 79 (khoanh cả quả khác lẫn từng "hạt" của quả).
- B2 **còn kém hơn B0**: chỉ 23/42 mẫu tự chọn đúng loại, nên mẫu sai kéo cả lượt 2 sai theo.
- **Kết luận pilot:** model đã khoanh được vật đúng, nhưng giữ lại quá nhiều khung sai loại. *(reports/PILOT_SUMMARY.md)*

## 4. Cải tiến: lọc khung sau CountGD++ (không cần train)

Giữ CountGD++ để tạo khung, thêm một bước **lọc bỏ khung sai** trước khi đếm:

| Cách lọc | Ý tưởng |
|---|---|
| **Lọc điểm** | Bỏ khung có điểm tự tin CountGD++ < 0.907 |
| **Fusion 50/50** | Trộn điểm CountGD++ với điểm CLIP. CLIP chấm ô cắt có giống "a photo of {X}" không, đóng vai **người kiểm tra thứ hai**; CLIP không đếm |

- **"Tối ưu" ở đây là:** chọn ngưỡng lọc trên 5 ảnh dev sao cho sai số đếm nhỏ nhất, rồi **khóa (freeze)** toàn bộ tham số. Không chỉnh thêm gì sau đó.
- Kiểm chéo trên dev (mỗi lần để riêng 1 ảnh ra làm kiểm tra): B2 gốc 22.0 → lọc điểm **4.6**, Fusion **5.8**, CLIP-only 6.8.
- Vì ngưỡng được chọn trên chính dev, kết quả dev còn lạc quan. **Phải kiểm lại trên ảnh mới.** *(reports/P4_CLIP_EXPLORATORY_FINDINGS_20261021.md)*

## 5. Kiểm trên tập ảnh mới (P4.6)

- **Dữ liệu:** 10 ảnh MUCCA chưa dùng (Zenodo, CC-BY-4.0), chọn bằng quy tắc cố định chia 5 nhóm cặp (người–chó, người–nhạc cụ, ghế–ô, người–ô tô, người–xe máy/thuyền).
  - Mỗi ảnh có 2 loại có mặt + 1 loại vắng mặt "khó" (gần nghĩa), tổng **30 query**.
  - Nhãn do Trí kiểm. Tập **khóa trước khi chạy model**.
- **Kiểm code:** runner mới chạy lại trên dev cho kết quả **trùng tuyệt đối** với kết quả cũ.

**Kết quả (cấu hình đã khóa, không chỉnh theo tập mới):**

| Cách | MAE 20 query có mặt | Count TB trên 10 query vắng mặt (đúng = 0) | MAE cả 30 | Khung sai loại |
|---|---:|---:|---:|---:|
| B0 | **5.70** | 8.9 | 6.77 | 106 |
| B2 gốc | 12.95 | 13.1 | 13.00 | 238 |
| Lọc điểm | 8.75 | 4.3 | 7.27 | 92 |
| **Fusion** | 7.80 | **1.0** | **5.53** | **31** |

*(reports/P4_6_UNSEEN_RESULTS_20261027.md; cột "khung sai loại" tính tự động bằng điểm GT nằm trong khung)*

## 6. Đã cải thiện được gì và chưa được gì

**Được:**
- So với B2 gốc, Fusion **giảm sai số còn khoảng 0.4 lần** (13.00 → 5.53).
- **Báo vật không có giảm 13 lần** (13.1 → 1.0).
- **Khung sai loại giảm khoảng 8 lần** (238 → 31).
- Fusion **tốt hơn lọc điểm thường** trên ảnh mới; lấy mẫu lại theo ảnh, mức chênh có khoảng tin cậy không chứa 0. Nghĩa là "người kiểm tra thứ hai" CLIP có ích.

**Chưa được:**
- **Đánh đổi:** bộ lọc bỏ khoảng **50% vật đúng**, nên không query có mặt nào đếm đúng tuyệt đối. Riêng trên query có mặt, B0 vẫn tốt nhất.
- **X/Y chưa giải quyết hẳn:** hỏi *people* trên ảnh có chó thì model vẫn khoanh chó. Hỏi *sheep* hay *bicycles* (vắng mặt nhưng gần nghĩa) thì model đếm chó / xe máy.
- Mẫu nhỏ (10 ảnh), một người kiểm nhãn. Đây là kiểm chứng nhỏ, không khái quát cho mọi trường hợp.

**Kết luận một câu:** *Lọc khung bằng CountGD++ + CLIP giảm mạnh lỗi đếm nhầm loại và báo vật không có, nhưng đổi lại bỏ sót nhiều vật đúng. Lỗi gốc nằm ở bước tự chọn mẫu của B2.*

## 7. Còn lại trước báo cáo

| Việc | Ai | Trạng thái |
|---|---|---|
| N4: review khung chọn lọc (7 query tầng A, 2 query tầng B) | Trí | Gói đã sẵn: results/countgdpp/p4_n4_review_package_20261027/ |
| Sửa kiểm chéo pilot T0–T4 | Triệu | Đang chờ (kế hoạch V2) |
| Duyệt chung pilot | Cả hai | Sau T4 |
| Báo cáo + slide + demo | Cả hai | Bắt đầu sau N4; hạn nội bộ 29/11 |

**Hướng phát triển** (chỉ nêu, chưa làm): áp bộ lọc lên B0 thay vì B2; kiểm mẫu tự chọn trước lượt 2. Muốn thử phải dùng tập ảnh mới khác, không chỉnh trên tập vừa kiểm.

**Ảnh minh họa gợi ý cho demo:** `results/countgdpp/p4_n4_review_package_20261027/A_u01_1_people_crops.jpg`: hỏi "people", 9 khung giữ lại đều khoanh vào chó (khung #19 chỉ lẫn một phần chân người ở góc). Cần xác nhận bằng review N4.
