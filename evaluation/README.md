# Evaluator pilot và script P4

**Ưu tiên trạng thái mới nhất 27/10:** Trí đã đọc C1 và chưa duyệt; Triệu tự làm T1–T4 theo [kế hoạch V2](../reports/KE_HOACH_SUA_KIEM_CHEO_20261027.md), hạn đề xuất 30/10–03/11. Việc chấp nhận bản assistant 24/10 không thay yêu cầu tự chạy mới. Trí chọn B, p4_unseen_v1 DRAFT; adapter đã viết, kiểm (1) từ điểm dev đạt, (2)–(4) chưa kiểm đầy đủ. T1 không sửa evaluator; fixtures đủ 15 query, giữ q05_2. Các mô tả giai đoạn trước bên dưới là nguồn tham khảo nếu khác điểm tiếp tục này.

**Cập nhật 27/10/2026.** [Phần 2](../roadmap/PHAN_2_DANH_GIA.md) · [Checklist tiếp tục](../roadmap/CHECKLIST_3_GIO.md).

Evaluator pilot đã được Minhtri chạy 20/10, output đã audit. Self-test PASS theo người chạy, chưa có stdout riêng. Ngày 24/10 Triệu đã đọc/hiểu/chấp nhận bản kiểm được ủy quyền cho assistant; không yêu cầu kiểm lại hoặc chạy lại để cập nhật tiến độ. Run chính `pilot_eval_20261020`, _r2 cùng dữ liệu; nhãn q05_2 không phải AP/IoU benchmark.

Script P4 có CLIP scorer và CV/Fusion/diagnostic trên dev. Scorer hiện gắn đường dẫn 15 query cũ; B2 runner trong experiments cũng phụ thuộc B0 pilot cũ. Cần adapter nhận input/output/B0 tương ứng trước ảnh mới; xem C3 checklist. Freeze có sẵn, chưa có runner ảnh mới đạt kiểm; không refit theo test.

Assistant phải hỏi trước nếu chạy evaluator/model/thực nghiệm thay. Lượt 27/10 chỉ pull, đối chiếu artifact và cập nhật tài liệu; giữ nguyên code/dự đoán gốc.
