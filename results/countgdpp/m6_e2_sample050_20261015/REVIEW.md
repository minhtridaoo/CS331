# M6/E2 — thay ngưỡng chọn mẫu, giữ ngưỡng cuối 0.23

**Kiểm tra ngày 15/10/2026.** Người dùng tự sửa tùy chọn tau_sample và chạy mô hình. Assistant đọc run_config.json/predictions.jsonl để đối chiếu, không chạy thêm inference trong lần cập nhật này.

## Phạm vi và bằng chứng

- Cùng 2 ảnh / 6 query, tối đa 3 mẫu. Tau_final giữ 0.23; chỉ thay tau_sample.
- Run tham chiếu 0.23: `b2_two_images_20261015`.
- Run thực tế 0.10: `m6_e2_sample010_20261015`.
- Run thực tế 0.50: `m6_e2_sample050_20261015`.
- Mỗi run đủ 6 query, execution_status=ok và stage1_matches_B0=True. Config các run có đúng tau_sample và tau_final.
- 0.10 và 0.23 có cùng pseudo_boxes và final_boxes theo so sánh JSON, không chỉ bằng số đếm; IDs/điểm mẫu cũng khớp khi đọc kết quả.

| Query | B0 | B2 sample 0.10 | B2 sample 0.23 | B2 sample 0.50 | Số mẫu ở 0.50 |
|---|---:|---:|---:|---:|---:|
| q01_1 guitars | 25 | 25 | 25 | 25 | 3 |
| q01_2 amplifiers | 44 | 38 | 38 | 44 | 0 |
| q01_3 chairs | 0 | 0 | 0 | 0 | 0 |
| q03_1 pens | 17 | 13 | 13 | 13 | 3 |
| q03_2 rulers | 18 | 18 | 18 | 18 | 0 |
| q03_3 pencils | 17 | 16 | 16 | 17 | 0 |

Ở 0.50, ampli/thước/bút chì không có mẫu, stage2_executed=false và stage2_count=null; kết quả cuối trả về B0 theo quy ước adapter. Ghế đã không có mẫu ở cả ba mức. Guitar/pens giữ nguyên mẫu và khung cuối so với 0.23. Count thước 18 ở hai cấu hình không có nghĩa tập khung final giống nhau: một bên có lượt hai, một bên trả B0; đối chiếu JSON cho thấy khung khác.

## Mức 0.35 không chạy

Đây là thay đổi so với lưới đề xuất ban đầu {.10,.23,.35,.50}, quyết định sau khi kiểm điểm mẫu. Ở 0.23, mẫu xếp thứ ba của 5 query có mẫu lần lượt đạt khoảng .8597/.4212/.7310/.4842/.4216, đều >.35; ghế vốn không có mẫu >.23. Theo quy tắc top-3 cố định, 0.35 sẽ chọn cùng bộ mẫu như 0.23 trên các đầu ra lượt đầu đã lưu. Đây là suy luận từ điểm/quy tắc, không phải kết quả inference mới và không phải phép kiểm raw độc lập ở 0.35.

## Kết luận và giới hạn

Đóng E2 pilot trên 2 ảnh, không báo quét thực tế đủ 4 mức hoặc hoàn tất toàn bộ benchmark M6. Hạ ngưỡng không đổi mẫu; tăng lên .50 làm mất mẫu của ba query, chưa cải thiện nhầm loại. Không suy ra mọi ngưỡng đều vô ích hoặc lỗi có một nguyên nhân duy nhất. Baseline .23 giữ nguyên. Chưa thực hiện E3, chưa train, chưa có absent/holdout hoặc xác nhận evaluator đầy đủ.

Trí đã kiểm bằng mắt cả 6 query của run 0.23: [bản ghi người dùng](../b2_two_images_20261015/USER_VISUAL_REVIEW.md). Có cả ca mẫu sai và ca mẫu đúng nhưng final sai. Tiếp theo Triệu kiểm chéo/evaluator; Trí khảo sát cấu hình .23 trên 3 ảnh dev còn lại đã có B0, trước khi chọn can thiệp.
