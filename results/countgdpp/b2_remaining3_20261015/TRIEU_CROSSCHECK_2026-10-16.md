# Đối chiếu review của Triệu — 16/10/2026

## Nguồn và phạm vi

Đọc [TRIEU_VISUAL_REVIEW.md](<../../../workspace Trí and Triệu/Triệu/TRIEU_VISUAL_REVIEW.md>) và hai bản review của Trí. Đã đối chiếu GT đếm/B0/final của 14 query trong file với combined_first5_metrics.json: tất cả khớp. Triệu có nhận xét 14/15 query, còn q01_1 guitars chưa có kiểm chéo trực tiếp. Một số nhận xét trong nguồn là tường thuật từ chat; lượt này không xác minh lịch sử chat đó, mà kiểm lại trực tiếp các điểm then chốt từ ảnh và tọa độ hiện có.

Đã mở ảnh q02_1 pseudo, q05_2 final và stage1. Không chỉnh file nguồn của Trí/Triệu, predictions, GT hoặc thuật toán. Đây là kiểm bằng mắt và tọa độ, chưa phải evaluator định vị chuẩn. Nhãn GT được lấy từ gói dữ liệu Triệu; tên MUCCA trong file nguồn không tự xác minh xuất xứ/giấy phép dữ liệu.

## 1. Điểm khác nhau: plates q02_1

Trí ghi 0/3 mẫu đúng; Triệu ghi 3/3 mẫu đúng và bao trọn đĩa. Assistant kiểm ảnh pseudo gốc: ba khung xanh nằm trên ba đĩa trong chồng đĩa bên trái, phù hợp nhãn đúng loại 3/3 của Triệu. Ảnh nhỏ và đĩa che nhau; chưa chấm độ bao trọn/IoU chính thức, không dùng “đúng loại” thay cho kiểm định định vị hoàn hảo.

Sử dụng 3/3 đúng loại trong tổng hợp cập nhật; bảo tồn nhận xét 0/3 ban đầu với nguồn là Trí. Tổng cũ 20/42 là đúng theo nhận xét ban đầu; sau điều chỉnh này, tổng hợp hỗn hợp nguồn là 23/42 mẫu đúng loại. Không gọi 23/42 là toàn bộ đã được hai người kiểm chéo: guitar vẫn chỉ có review của Trí. Ba ca mẫu đúng 3/3 nhưng final còn sai/thừa: plates, rulers, raspberries. Guitar đúng 3/3 và final đúng theo Trí, chưa có Triệu kiểm chéo.

## 2. Raspberries q05_2: đã hoàn tất bước phân loại 14 khung final

Số dưới đây là số hiển thị 1-based trên final.jpg, không phải proposal ID thô.

| Loại vật theo kiểm bằng mắt | Số khung | Tổng |
|---|---|---:|
| Raspberry | 1, 2, 3, 7, 11 | 5 |
| Blackberry | 10, 14 | 2 |
| Blueberry | 9, 12, 13 | 3 |
| Strawberry | 5, 6 | 2 |
| Cherry | 4, 8 | 2 |

Khớp tổng 14. Khung 7 và 11 cùng chỉ raspberry phía sau bên trái; khung 11 chỉ bao một phần quả. Bốn raspberry thật đều có khung theo kiểm tra bằng mắt. Do đó: **14 = 4 quả mục tiêu + 1 khung trùng trên quả mục tiêu + 9 khung sai loại**. Khung 12 và 13 là phần của blueberry; đồng thời sai loại khi query là raspberries. Không cộng lại “phần vật” vào tổng lỗi như một nhóm loại trừ với sai loại/trùng.

Số dư 10 so với GT=4 được giải thích trên ca này: 9 khung sai loại và 1 khung trùng mục tiêu. Đây là phân tích thủ công một ca, không phải tuyên bố tỷ lệ lỗi chung trên dataset. Bỏ khung trùng đơn thuần sẽ chưa loại bỏ các quả khác. Mẫu đúng 3/3 vẫn đi cùng final sai loại; chưa xác định nguyên nhân bên trong model.

[Ảnh final](q05_2/final.jpg) · [Nhãn khung và hash nguồn](q05_2/manual_crosscheck_20261016.json)

## 3. Giải thích thêm chênh lệch stage1 raspberries

Nguồn Triệu nêu 4 raspberries + 1 strawberry + 2 cherries + 3 blueberries = 10, trong khi log là 11. Kiểm ảnh stage1 và tọa độ cho thấy **2 strawberry ở khung 6 và 7**. Phân loại stage1: raspberries 1/2/3/4, cherries 5/8, strawberries 6/7, blueberries 9/10/11. Tổng 4+2+2+3=11. Đây là bổ sung của assistant, chưa sửa nguyên văn file Triệu; nhờ Triệu xác nhận hai khung 6/7 nếu cần chốt nhãn nhóm.

## 4. Còn cần làm rõ

- q01_1 guitars: Triệu chưa ghi review trực tiếp; chưa báo kiểm chéo đủ 15/15.
- q04_2 blueberries: mô tả “toàn bộ 24 blueberries + 10 blackberries + 1 red currant” cho 35 vật nếu mỗi vật có một khung, nhưng final chỉ 32. Phải đối sánh từng vật/khung để xác định thiếu/trùng/khung gộp; không tự suy ra đúng 3 quả bị bỏ sót. Quả bị thiếu ở stage1 cũng chưa rõ thuộc loại nào.
- q02_1: xác nhận 3/3 đúng loại có bằng chứng ảnh; mức bao trọn vẫn là nhận xét bằng mắt, chưa chấm định vị chuẩn.
- q05_3 blackberries: nhóm thống nhất dấu hiệu đếm phần quả và lẫn loại, chưa phân loại đủ 79 khung.
- Chưa coi kiểm chéo định tính là hoàn thành evaluator hoặc xác minh toàn bộ GT/absent/holdout.

## 5. Quyết định tiếp theo

Không yêu cầu làm lại phân loại final q05_2 từ đầu. Triệu bổ sung guitar, làm rõ q04_2 và xác nhận phần hiệu chỉnh plates/strawberries nếu cần; Trí dùng nhãn khung q05_2 để kiểm cách đo sai loại/trùng/bỏ sót với evaluator. Giữ trọng tâm giảm đếm nhầm loại; chưa chốt NMS/ngưỡng/module mới từ một ca.

Nhánh benchmark paper trên Kaggle đã được chuẩn bị ở handoff hiện hành: giữ tiến trình đó, chưa xác nhận đã chạy hoặc có metric mới. Theo hướng dẫn hiện có, bắt đầu bằng kiểm GPU/môi trường cell 1–2 khi người dùng tiếp tục nhánh đó. MAE B0=19.4/B2=22.0 của pilot 5 ảnh giữ nguyên; không so trực tiếp với FSCD-147 khác tập.
