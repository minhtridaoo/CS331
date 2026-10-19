# Kiểm tra bằng mắt của Trí — B2, 2 ảnh / 6 truy vấn

**Ngày ghi nhận: 15/10/2026 (Asia/Bangkok).** Nguồn: nhận xét trực tiếp của người dùng trong chat sau khi được hướng dẫn xem run `b2_two_images_20261015` (tau_sample=tau_final=0.23). Không phải review của run 0.50: ở run đó ampli/thước/bút chì không có mẫu.

Đây là đánh giá thủ công của người dùng, chưa có xác nhận độc lập của Triệu và chưa phải nhãn từng khung hoặc phép đo precision/recall. Số B0/B2 dưới đây lấy từ predictions.jsonl; số mẫu đúng lấy từ nhận xét của người dùng. GT đếm tham khảo từ gói dữ liệu Triệu: 25/11/1/6/6/6 theo thứ tự bảng.

| Query | Stage1 theo người dùng | Mẫu đúng | Final theo người dùng | B0 → B2 |
|---|---|---:|---|---:|
| q01_1 guitars | Nhận diện đủ guitar | 3/3 | Đúng guitar | 25 → 25 |
| q01_2 amplifiers | Khoanh cả guitar và ghế | 0/3; cả 3 là guitar | Vẫn khoanh lẫn nhiều loại; người dùng mô tả “khoanh all” | 44 → 38 |
| q01_3 chairs | Không khoanh gì | Không có mẫu; không tính 0/3 | Không khoanh gì; trả B0, không chạy lượt hai | 0 → 0 |
| q03_1 pens | Khoanh cả thước và bút | 1/3; 2 mẫu còn lại là bút chì | Theo người dùng: 1 thước, tất cả bút chì và bút | 17 → 13 |
| q03_2 rulers | Khoanh mọi loại trong ảnh | 3/3 | Vẫn khoanh mọi loại trong ảnh | 18 → 18 |
| q03_3 pencils | Khoanh mọi loại trong ảnh | 0/3; cả 3 là bút | Khoanh gần hết các vật | 17 → 16 |

## Cách diễn giải

- Guitar là ca đối chiếu thành công theo mắt người dùng; chưa tính độ chính xác định vị bằng evaluator.
- Ampli và bút chì: mẫu sai loại đi cùng kết quả cuối lẫn loại. Chưa chứng minh mẫu sai là nguyên nhân duy nhất; lượt đầu đã sai.
- Pens: mẫu pha trộn; kết quả cuối vẫn lẫn loại dù số đếm giảm.
- Rulers: mẫu đúng 3/3 nhưng kết quả cuối vẫn lẫn loại. Đây là phản ví dụ cho khẳng định “chỉ cần chọn đúng mẫu là sẽ đếm đúng” trong cấu hình đang kiểm. Chưa xác định thành phần bên trong gây lỗi.
- Chairs: dữ liệu có 1 ghế; đây là bỏ sót lớp có mặt, không phải kiểm tra lớp vắng mặt. Không có lượt hai để đánh giá.
- “Khoanh all/tương tự stage1” là mô tả loại vật bị lẫn, không phải xác nhận tập khung giống hệt. Ampli 44→38 và bút chì 17→16 đã thay đổi số khung. Chưa đối sánh từng khung để phân loại trùng/lệch/bỏ sót.

**Cập nhật sau review 9 query còn lại:** đã chạy và Trí đã review đủ 5 ảnh; xem [bản tổng hợp và bước tiếp hiện tại](../b2_remaining3_20261015/USER_VISUAL_REVIEW.md).

## Bước tiếp theo và phân công tại thời điểm review 6 query

1. Triệu kiểm chéo các mẫu và nhãn trên 6 query, ghi bất đồng theo query/khung; hoàn thiện evaluator và nhãn định vị phù hợp.
2. Trí tiếp tục khảo sát B2 ở cấu hình cố định tau_sample=tau_final=0.23 trên 3 ảnh còn lại của bộ dev 5 ảnh đã có B0. Đây là kế hoạch, chưa chạy; không gọi các ảnh này là holdout vì đã xem B0.
3. Hai người tổng hợp tần suất hai kiểu lỗi: mẫu sai và mẫu đúng nhưng final sai. Dùng dữ liệu phát triển để chọn một can thiệp có đối chứng; chưa chọn module hoặc train từ hai ảnh hiện tại.

Các nhãn review chỉ phục vụ đánh giá, không đưa vào model để chọn mẫu hoặc loại vật. Chưa mở E3; E2 pilot đã đóng với 0.35 được bỏ qua có giải thích, không báo là đã chạy đủ bốn mức.

[Review M5 trước đó](REVIEW.md) · [Review E2](../m6_e2_sample050_20261015/REVIEW.md)
