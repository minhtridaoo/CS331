# M4 — Review 5 ảnh / 15 truy vấn

**Kiểm tra ngày 14/10/2026. Run: m4_first5_b0, B0 nguyên script gốc, ngưỡng 0.23.**

Đủ 15/15 query hợp lệ, 5 ảnh; IDs khớp cấu hình, count/boxes/scores nhất quán, đủ overlay. Không có lỗi thực thi. Ba count của ảnh đầu lặp lại đúng run trước; không tính chúng như ảnh độc lập.

| Ảnh | Query | GT trong gói Triệu | Dự đoán | Sai số tuyệt đối |
|---|---|---:|---:|---:|
| mcac_100 | guitars | 25 | 25 | 0 |
| mcac_100 | amplifiers | 11 | 44 | 33 |
| mcac_100 | chairs | 1 | 0 | 1 |
| mcac_11 | plates | 15 | 28 | 13 |
| mcac_11 | bowls | 3 | 31 | 28 |
| mcac_11 | cups | 2 | 23 | 21 |
| mcac_200 | pens | 6 | 17 | 11 |
| mcac_200 | rulers | 6 | 18 | 12 |
| mcac_200 | pencils | 6 | 17 | 11 |
| mcac_20 | strawberries | 6 | 60 | 54 |
| mcac_20 | blueberries | 24 | 43 | 19 |
| mcac_20 | red currants | 39 | 84 | 45 |
| mcac_27 | cherries | 2 | 20 | 18 |
| mcac_27 | raspberries | 4 | 11 | 7 |
| mcac_27 | blackberries | 3 | 21 | 18 |

## Nhận xét từ toàn bộ overlay

- mcac_100: guitar đúng count; ampli vẫn lấy nhiều guitar; ghế bị bỏ sót. Đúng count guitar chưa phải điểm định vị chính thức.
- mcac_11: hỏi bowls/cups vẫn có nhiều khung vào chồng đĩa; có vùng chồng khung, cần phân loại chi tiết trước khi quy tất cả lỗi cho trùng.
- mcac_200: ba lớp pens/rulers/pencils đều GT=6; dự đoán 17/18/17, khung chọn cả bút, thước và bút chì. Đây là ví dụ rõ cho lỗi chọn loại, không suy luận chỉ từ count gần bằng nhau.
- mcac_20: hỏi từng loại trái cây nhưng khung vẫn chọn các loại khác. strawberries 60/GT6; không có nghĩa có 60 quả dâu trong ảnh.
- mcac_27: các prompt cherries/raspberries/blackberries tiếp tục lấy vùng trái cây khác. Có khung chồng lấn; chưa chấm từng khung để lượng hóa trùng/nhầm/nền.

## Chỉ số sơ bộ

Theo GT trong gói nhận: 1/15 query đúng số, 13 đếm thừa, 1 đếm thiếu; MAE_present=19.4, RMSE_present≈24.316. Coverage=15/15. Presence recall=14/15 chỉ là trả count dương, không chứng minh chọn đúng lớp. Không có absent query nên FPR_absent/MeanAbsentCount=null, không phải 0.

Chỉ số của 5 ảnh dev nội bộ, không phải toàn MUCCA, không phải cấu hình đầy đủ paper. GT đã kiểm khớp annotations đi kèm, chưa kiểm chéo thủ công toàn bộ. Chưa xác nhận evaluator của Triệu đã triển khai hoặc kiểm đạt.

## Bước tiếp theo

Đã có lỗi lặp lại để điều tra; chưa cần tiếp tục chạy rộng chỉ để gom thêm số. Giữ nguyên output/ngưỡng/checkpoint. Trên ảnh mcac_200 (bút/thước) và mcac_100 (guitar/ampli), kiểm điểm theo token: điểm nào khiến khung của lớp khác vượt lọc? So token tên vật với token đặc biệt/dấu chấm trong logic lọc gốc, chỉ ghi log chẩn đoán trước; chưa sửa âm thầm baseline hoặc tuyên bố đây là nguyên nhân. Sau khi rõ đường lọc, mới quyết định đối chứng ngưỡng/lọc/B2.

Triệu kiểm nhãn/đánh dấu khung sai loại, ghép evaluator và bổ sung query vắng mặt đã xác minh. Chưa có holdout; không chốt phương pháp mới hoặc train từ 5 ảnh này.

[Bảng từng query](review_per_query.csv) · [Chỉ số và hash nguồn](review_metrics.json) · [Ảnh so sánh văn phòng phẩm](stationery_query_comparison.jpg)
