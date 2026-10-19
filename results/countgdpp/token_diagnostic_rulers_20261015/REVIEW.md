# Chẩn đoán B0: vì sao hỏi thước nhưng lấy cả bút?

**15/10/2026. Một ảnh/ một query: mcac_200, q03_2, rulers.**

## Kết quả kiểm được

- Tái hiện 18 khung; số đếm, tọa độ (sai khác cho phép 0.001 pixel) và scores (1e-5) khớp run m4_first5_b0.
- Observer trả nguyên kết quả hàm lọc gốc; không đổi checkpoint, threshold 0.23 hoặc sửa code upstream.
- Token đầu ra: [CLS], rulers, dấu chấm, [SEP]. Cả 18 khung có điểm lớn nhất ở token rulers trong phần positive.
- Nếu chỉ tính token tên vật và bỏ token đặc biệt/dấu chấm khỏi positive, vẫn giữ nguyên 18 khung. Đây là phép kiểm offline trên scores đã lưu; không phải phương pháp mới hoặc bản baseline đã sửa.
- Xem proposal_ids.jpg và gán nhãn bằng mắt: 6 thước đúng, 6 bút mực nhầm, 6 bút chì nhầm. Nhãn này chỉ dùng phân tích sau inference; cần Triệu kiểm chéo.

| Loại khung thực tế | Số khung | Khoảng điểm token rulers |
|---|---:|---|
| Thước | 6 | 0.4252–0.4906 |
| Bút mực | 6 | 0.4232–0.4445 |
| Bút chì | 6 | 0.3540–0.3776 |

Ngưỡng 0.23 giữ cả ba nhóm. Điểm của một số bút mực cao hơn điểm của thước xanh phía dưới, nên một ngưỡng duy nhất trên điểm này không thể giữ đủ sáu thước và loại hết bút trong ca hiện tại. Điều này không có nghĩa chỉnh ngưỡng không có ích trên bộ dữ liệu; chưa chọn ngưỡng từ ảnh này.

## Kết luận có giới hạn

Đã loại được cách giải thích rằng token dấu chấm/đặc biệt làm các khung sai vượt lọc trong query này. Chính điểm liên kết với từ rulers cũng cao trên vật khác. Chưa biết cơ chế sâu bên trong khiến điểm sai, chưa suy rộng kết luận sang mọi query hoặc toàn model. Chưa khẳng định cần fine-tune, thêm module hay thay phương pháp.

## Bạn chạy tiếp

Đối chiếu q03_1 pens, q03_3 pencils, q01_1 guitars (ca đúng count) và q01_2 amplifiers (ca sai khác loại). Không chạy lại baseline toàn bộ 5 ảnh.

~~~bash
source /root/.venvs/countgdpp/bin/activate
cd /mnt/d/MINHTRIHOCCODE/HOCKI5/CS331
python experiments/countgdpp/diagnose_tokens.py --query-ids q03_1 q03_3 q01_1 q01_2 --run-id token_diagnostic_more_20261015
~~~

Đầu ra trong results/countgdpp/token_diagnostic_more_20261015/: summary.json; mỗi query có raw_scores.npz, kept_box_tokens.csv, proposal_ids.jpg. Mục tiêu: đối chiếu khung/score với B0 và kiểm token nào giữ khung sai; không đặt mục tiêu kết quả phải tốt lên trong bước chẩn đoán.

Triệu kiểm chéo manual_box_review.csv và tiếp tục evaluator/absent queries. Sau khi có bốn query bổ sung, chọn một đối chứng nhỏ dựa trên bằng chứng; không mặc định chốt B2 hoặc một module cải tiến.

## Tài nguyên và tái lập

Run này đo predict + preprocessing/transfers + capture, chưa warm-up, không gồm khởi tạo model/vẽ/lưu: 1736.6 ms. Peak PyTorch allocated 1461.12 MiB gồm model cư trú, không phải tổng VRAM thiết bị. Không so trực tiếp với elapsed_ms toàn subprocess trong batch cũ. Xem run_config.json và q03_2/summary.json để tra hash/cấu hình. Không gán các số đo này cho run cũ.
