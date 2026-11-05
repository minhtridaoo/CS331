# Kiểm lại trước khi duyệt các phần của Triệu — 05/11/2026 (khuya)

**Yêu cầu của Trí:** sau khi đã đồng ý, kiểm lại xem các phần Triệu muốn Trí duyệt có thật sự ổn không. **Người kiểm:** assistant. Chỉ đọc code/file, chạy `select_dev_test_v2.py --stats` (chỉ đếm, không rút, không ghi file), tính tay từ số đã lưu. Không chạy model/evaluator.

## Kết luận: **duyệt được**, kèm 3 lưu ý (một lưu ý cần xử lý trước 09/11)

| Phần | Kiểm gì | Kết quả |
|---|---|---|
| V3 q05_3 | 103/103 nhãn; tọa độ trùng gói gốc; tổng khớp | ✅ |
| V4 2 ca thử | **Tính tay lại từ `pilot_eval_20261020/per_query.json`:** bỏ q05_3 → 19.50 / 18.14; q01_1 thành absent → MAE_present 20.79, MAE chung 21.07, MeanAbsent 25 | ✅ khớp từng số Triệu báo |
| V5 | Số đã tính lại ngày 02/11 | ✅ |
| V6 tầng B | 58/58 dòng; đã ghép bảng tra; **xem ảnh crop u06_2**: 26 ô bãi biển + #9 phao bơi (`wrong_class`), đúng nhãn | ✅ |
| Code P1 (`run_b2_verified_pseudo.py`, `pseudo_clip_verifier.py`) | Đọc toàn bộ logic | ✅ Đúng thiết kế §3.2: ứng viên = cùng luật `select_pseudo` lấy tối đa M; CLIP cùng model/revision/crop/template đã khóa; giữ cosine ≥ tau rồi lấy top 3 theo điểm CountGD; không còn mẫu thì trả B0; trạng thái ngẫu nhiên đưa về đúng lúc vừa xong lượt 1; kiểm hash checkpoint/source; **không đọc GT**; lưu raw lượt 2 cho từng biến thể (đủ để tính T ngoại tuyến) |
| `p1_controls.py` | Đọc mô tả + luồng | ✅ Áp **ngưỡng đã khóa** cho mọi nguồn, đúng như ghi chú. Việc chọn lại ngưỡng riêng từng nguồn (D2) **chưa có**; đây là việc của assistant, hạn 09/11 |
| `select_dev_test_v2.py` | Đọc logic; chạy `--stats` trên MUCCA của máy Trí | ✅ Ra **185 / 19 / 90 và chia nhóm khớp đúng** báo cáo của Triệu. Loại đúng 5 ảnh pilot + 10 ảnh p4_unseen_v1 (có kiểm trạng thái LOCKED); kiểm md5 zip; mặc định = D3–D7 |

## 3 lưu ý

1. **(Cần xử lý trước 09/11) `evaluate_research.py` không nhận GT `uncertain`.** Gặp `uncertain` là dừng ("Manifest row does not fit"), khác evaluator pilot (loại `uncertain` ra khỏi phép tính, như V4 đã thử).
   - **Dặn Triệu cho W4:** nếu lớp absent nhìn thấy trong ảnh thì **đổi sang lớp dự phòng kế tiếp** (như đã làm với p4_unseen_v1), **không** ghi `uncertain`. GT có mặt mà nghi ngờ thì ghi vào `uncertainty_note`, giữ số điểm MUCCA.
   - **Assistant:** thêm vào `evaluate_research.py` cách xử lý `uncertain` giống evaluator pilot (loại ra và ghi tên), trước 09/11.
2. **N4 tầng A còn vài nhãn chưa nhất quán** giữa `wrong_class` và `multi_object`, cùng `object_id` khác nhau giữa các file (RA_SOAT §4, §7). Điều này **không đổi** kết luận chính ("mẫu đúng loại 1/12"), vì cả hai nhãn đều là "không đúng loại". Chỉ cần ghi là hạn chế trong báo cáo, không cần gán nhãn lại.
3. **Số pilot P1 (bảng MAE theo tau, Kiểm A/C) và output V4 đang ở máy/Drive của Triệu**, nên assistant chưa kiểm độc lập được. Duyệt ở đây là duyệt **code và quy trình**; số pilot chỉ dùng chẩn đoán, không dùng chọn tham số. Khi Triệu xong W2, assistant sẽ kiểm.

**Vậy việc Trí đã đồng ý ngày 05/11 (D1–D10, nghiệm thu V3–V6, duyệt pilot phía Trí) giữ nguyên**, kèm 3 lưu ý trên.
