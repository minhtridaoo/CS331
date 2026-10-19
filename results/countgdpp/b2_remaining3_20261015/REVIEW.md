# B2 mở rộng — đủ 5 ảnh / 15 truy vấn dev

**Bổ sung 16/10:** đã nhận kiểm chéo Triệu 14/15 query; hiệu chỉnh plates 3/3 đúng loại và giải thích đủ final q05_2. [Đối chiếu mới](TRIEU_CROSSCHECK_2026-10-16.md). Phần nhận xét ngày 15/10 bên dưới giữ nguyên nguồn/lịch sử, gồm số 20/42 trước hiệu chỉnh; không còn yêu cầu phân loại lại q05_2 từ đầu.

**Kiểm ngày 15/10/2026.** Người dùng chạy thêm 3 ảnh/9 query; assistant kiểm đầu ra và tổng hợp, không chạy thêm inference.

## Kiểm tra kỹ thuật

Run mới complete, 9/9 execution_status=ok, tất cả có 3 mẫu và chạy lượt hai. Cả 9 lượt đầu khớp B0 cũ về count, boxes (sai số <=0.001 pixel), scores (<=1e-5). Ghép run 2 ảnh trước được 15 IDs duy nhất đúng tập first5; cả 15 lượt đầu khớp B0. Kiểm count bằng số boxes/scores, số hữu hạn và nhánh không mẫu đạt. Tau_sample=tau_final=.23; max_pseudo=3; checkpoint, nguồn model, quy tắc chọn/lọc và cấu hình suy luận khớp. Hash adapter khác vì đã thêm tùy chọn ngưỡng; không gọi hai script là giống từng byte.

## Kết quả đếm trên cùng 5 ảnh

| Query | GT gói Triệu | B0 | B2 | Thay đổi sai số tuyệt đối |
|---|---:|---:|---:|---|
| q01_1 guitars | 25 | 25 | 25 | Giữ nguyên |
| q01_2 amplifiers | 11 | 44 | 38 | Giảm |
| q01_3 chairs | 1 | 0 | 0 | Giữ nguyên |
| q02_1 plates | 15 | 28 | 31 | Tăng |
| q02_2 bowls | 3 | 31 | 31 | Giữ nguyên |
| q02_3 cups | 2 | 23 | 26 | Tăng |
| q03_1 pens | 6 | 17 | 13 | Giảm |
| q03_2 rulers | 6 | 18 | 18 | Giữ nguyên |
| q03_3 pencils | 6 | 17 | 16 | Giảm |
| q04_1 strawberries | 6 | 60 | 59 | Giảm |
| q04_2 blueberries | 24 | 43 | 32 | Giảm |
| q04_3 red currants | 39 | 84 | 84 | Giữ nguyên |
| q05_1 cherries | 2 | 20 | 15 | Giảm |
| q05_2 raspberries | 4 | 11 | 14 | Tăng |
| q05_3 blackberries | 3 | 21 | 79 | Tăng |

MAE B0=19.400, B2=22.000; RMSE B0=24.316, B2=30.091. Exact count: B0=1/15, B2=1/15. Sai số giảm 6, tăng 4, giữ nguyên 5 truy vấn.

Kết quả B2 trung bình kém hơn B0 trên bộ dev này; không khái quát chất lượng mô hình hoặc paper từ 5 ảnh. Count giảm không đồng nghĩa chọn đúng loại. GT từ manifest gói Triệu, chưa xác nhận independent visual review toàn bộ hoặc evaluator chính thức. Không bỏ ca blackberries để báo metric tốt hơn.

## Quan sát q05_3 — assistant và bổ sung của người dùng

Đã mở pseudo.jpg và final.jpg: hai mẫu nhìn là toàn quả blackberry; mẫu còn lại nhìn là raspberry đỏ. Ảnh final có nhiều khung nhỏ trên các phần tròn của quả blackberry, đồng thời khoanh nhiều loại quả khác và có khung chồng nhau. Đây là dấu hiệu có thể đếm phần của quả thay vì cả quả, bên cạnh nhầm loại/trùng khung; chưa gán nhãn từng proposal, chưa chứng minh nguyên nhân là mẫu sai. B0=21, B2=79, GT gói Triệu=3. Không suy ra mọi khung thừa đều là múi hoặc đều trùng.

**Bổ sung:** người dùng đã xác nhận mẫu 2/3 đúng, final đếm múi và lẫn các quả khác; [review đủ 15 query của Trí](USER_VISUAL_REVIEW.md). Chưa có kiểm chéo của Triệu hoặc phân loại từng bbox.

## Bước tiếp theo

Review 9 query mới đã hoàn tất; chuyển sang phân loại 14 bbox q05_2 như hướng dẫn trong USER_VISUAL_REVIEW.md, Triệu kiểm chéo/evaluator.

Kế hoạch tại lúc nhận run (nay đã xong phần review của Trí): số mẫu đúng/n, loại nhầm, khung ôm cả vật hay một phần, có nhiều khung cho cùng vật không. Ưu tiên q05_3; so q05_1/q05_2 cùng ảnh, sau đó hai ảnh còn lại. Triệu kiểm chéo và hoàn thiện evaluator. Chưa sửa NMS/ngưỡng hoặc chọn module chỉ theo ca này; chưa mở E3/train. E1/E2 vẫn chỉ khảo sát 2 ảnh, không tự tính là đã quét trên 5 ảnh.

[Số liệu và hash nguồn](combined_first5_metrics.json) · [Review người dùng 6 query đầu](../b2_two_images_20261015/USER_VISUAL_REVIEW.md)
