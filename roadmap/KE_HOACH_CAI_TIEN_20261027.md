# Kế hoạch cải tiến — thực thi đề xuất trong `hướng cái tiển/` (27/10/2026)

**Nguồn:** [Đánh giá tiềm năng paper](<../hướng cái tiển/CS331_Danh_gia_tiem_nang_Paper_va_Lo_trinh_20261027.md>) và [Kế hoạch fix pipeline](<../hướng cái tiển/CS331_KE_HOACH_FIX_PIPELINE_DE_PUBLISH_20261027.md>), cả hai do Trí đưa. File này đối chiếu đề xuất với code, dữ liệu và kết quả thật, rồi chốt thứ tự làm. **Chưa chạy thí nghiệm mới nào.**

## 1. Trả lời: có cần làm N4 trước không? **Có, và N4 là bước bắt buộc (F0).**

Kết quả N4 quyết định chọn nhánh P (kiểm mẫu tự chọn trước lượt 2) hay nhánh R (bộ lọc giữ lại vật đúng). Gói N4 cũ thiếu hai thứ F0 cần, **nay đã bổ sung**: `results/countgdpp/p4_n4_review_package_20261027/bo_sung_F0/`, gồm 27 mẫu tự chọn và 29 ứng viên E3.

**Chỉ báo tự động (đặt giả thuyết, chưa phải kết luận; tính bằng điểm MUCCA nằm trong khung, trên 30 query p4_unseen_v1):**

| Mã | Đo được | Đọc |
|---|---|---|
| E1 mẫu tự chọn sai | 21/65 mẫu sai loại. Tập trung ở query "people" (u01_1, u02_1, u05_1, u07_1, u08_1, u10_1) và 3 query vắng mặt (9/9 sai, đương nhiên vì vật không có). Query có ≥ 1 mẫu sai: sai số B2 tăng trung bình **+11.7** so với B0; query 3 mẫu đều đúng: **+5.8** | E1 có ảnh hưởng thật |
| E2 mẫu đúng nhưng lượt 2 vẫn phình | chairs u06_1 15 → 49, motorbikes u10_2 33 → 80, cả 3 mẫu đều đúng | Có. Nhánh P **không** sửa được lỗi này |
| E3 Fusion xóa vật đúng | **152** khung B2 chứa điểm mục tiêu bị Fusion loại | Nguồn chính của việc mất khoảng 50% vật đúng |
| E4 không có ứng viên | 12/289 điểm mục tiêu không nằm trong khung B2 nào; amplifiers (u03_2) bỏ sót hoàn toàn | Nhỏ |

**Hệ quả cho việc chọn nhánh, cần N4 xác nhận:** E1 và E3 đều lớn. Nhánh P giảm được phần phình do mẫu sai, nhưng **không** cứu được vật bị Fusion xóa (E3). P cũng không chặn được query vắng mặt: khi bỏ hết mẫu sai, adapter quay về B0, mà B0 vẫn đếm 20 con chó cho "sheep". Nhánh R nhắm đúng E3 nhưng có rủi ro "cứu nhầm" khung sai.

Vì vậy đề xuất **bổ sung đối chứng C6 = B0 + bộ lọc**. B0 phủ 93% vật đúng và chỉ có 106 khung sai loại so với 238 của B2. Nếu C6 tốt bằng các cách khác thì không cần lượt 2. Đây là câu hỏi phản biện dễ gặp nhất (§6.3 của đề xuất).

## 2. Đối chiếu đề xuất với thực tế

| Điểm trong đề xuất | Thực tế | Điều chỉnh |
|---|---|---|
| Không tìm thấy P4_6_UNSEEN_RESULTS và gói N4 trên `main` | Đúng: các file đó chưa push (Trí sẽ tự commit/push) | Push trước khi gửi bản đề xuất cho thầy |
| Sửa ở `run_b2_pilot.py: select_pseudo` | Runner hiện hành là `experiments/countgdpp/run_b2_frozen.py` (import `select_pseudo`, đã kiểm dev trùng tuyệt đối) | Nhánh P viết file mới dựa trên `run_b2_frozen.py`; giữ hai file cũ |
| Tạo `evaluate_research.py` | Đã có `evaluation/p4_unseen_score.py`: tách có mặt / vắng mặt, FPR_absent, bootstrap theo ảnh, chỉ số điểm-trong-khung | **Mở rộng** script này (thêm ghép một–một, nhiều phương pháp) thay vì viết từ đầu |
| CLIP chèn giữa lượt 1 và lượt 2 | CountGD++ chạy ở WSL `Ubuntu-22.04` (torch 2.5.1), CLIP ở WSL `Ubuntu` (torch 2.9.1); không chung môi trường | Chạy 3 bước: (1) lượt 1 lưu ứng viên (đã có `stage1_raw.npz`) → (2) CLIP chấm top-M ứng viên bằng đúng môi trường CLIP đã khóa → (3) lượt 2 với mẫu đã chọn. Cần thêm chế độ "lượt 2 với mẫu cho trước" vào runner |
| Dữ liệu: 30 ảnh dev + ≥ 50 ảnh test mới | MUCCA còn 185 ảnh chưa dùng. Nhưng nếu giữ cặp X/Y **khác siêu nhóm** thì chỉ còn **19** ảnh (3–40 điểm), 26 ảnh (3–60), 34 ảnh (2–80) | **Không đủ 80 ảnh** nếu chỉ dùng cặp khác hẳn. Phải thêm cặp **dễ nhầm** cùng siêu nhóm (§7.2 đề xuất cũng muốn có): 3–40 điểm mọi cặp còn **109** ảnh |
| Kiểm nhãn vắng mặt cho mọi ảnh | Mỗi ảnh cần người xác nhận absent + soát GT | 80 ảnh ≈ 3–4 giờ công. Đề xuất bản vừa sức: **dev 20 + test 40** (60 ảnh / 180 query) |
| Thời gian chạy | B2 khoảng 10 phút / 30 query trên RTX A2000 | 180 query ≈ 1 giờ mỗi cấu hình. Chạy local được, chưa cần Kaggle |

## 3. Thứ tự làm (gắn với W0–W5 của đề xuất)

| Mốc | Việc | Ai | Xong khi |
|---|---|---|---|
| **W0 (đến 02/11)** | **N4 tầng A** (gói chính 78 khung + bổ sung 21 mẫu + 18 ứng viên E3); tầng B nếu còn giờ | Trí (Triệu xem lại một phần nếu kịp) | CSV điền đủ → assistant ghép bảng tra, tính E1–E4 bằng nhãn người → **chọn P hoặc R** |
| W0 song song | Chốt quy tắc chia dev/test mới (§4); Triệu làm T0–T4 | Trí duyệt; assistant soạn script chọn | Quy tắc được duyệt **trước khi rút ảnh** |
| W1 (03–08/11) | Rút và khóa dev 20 + test 40; Trí/Triệu kiểm absent/GT | Cả hai | Hai tập LOCKED, có hash |
| W2 (09–15/11) | Viết nhánh đã chọn (P1 hoặc R1) + C6; chạy trên **dev mới**; chọn tham số trên dev | Assistant viết/chạy khi Trí cho phép | Bảng dev: B0, B2, lọc điểm, Fusion, C6, phương pháp mới |
| W3 (16–22/11) | Chốt một phương pháp, khóa cấu hình | Cả hai | Freeze v2 + commit |
| W4 (23–26/11) | **Một lần** đánh giá trên test 40 ảnh | Assistant chạy, Triệu đối chiếu | Bảng cuối + CI theo ảnh |
| W5 (27/11–02/12) | Báo cáo / paper / slide / demo | Cả hai | Bản nộp |

**Nếu phương pháp mới không vượt Fusion / C6 trên test:** báo kết quả âm, viết theo hướng phân tích lỗi (hướng A của đề xuất). Không chỉnh lại trên test.

## 4. Quy tắc dữ liệu mới — cần Trí chốt trước khi rút ảnh

Đề xuất bản v2 của `p4_select_unseen.py`:
- Pool: 185 ảnh chưa dùng (loại 5 ảnh dev pilot + 10 ảnh p4_unseen_v1).
- Mỗi ảnh lấy 1 cặp có mặt, 3–40 điểm mỗi lớp, kèm 1 query vắng mặt loại "khó".
- Hai loại cặp:
  - **"khác hẳn"**: khác siêu nhóm, trả lời đúng câu hỏi của thầy; lấy hết số ảnh có thể;
  - **"dễ nhầm"**: cùng siêu nhóm, ví dụ trái cây, đồ ăn, văn phòng phẩm.
- Rút phân tầng có seed, rồi chia dev/test **theo ảnh**.
- 10 ảnh p4_unseen_v1 chỉ dùng phân tích lỗi và demo; **không** dùng làm test cho phương pháp mới.
