# Handoff Trí — mô hình và thí nghiệm

Cập nhật 20/10/2026. [Trạng thái chung](HANDOFF.md) · [Work log](../WORKLOG.md)

Đã có model/checkpoint chạy, B0/B2 5 ảnh/15 query và E1/E2 pilot 2 ảnh. Phần chạy và review nhỏ đã có bằng chứng; không cần rerun inference để tính metric.

Phần 2 đã chạy bằng python3; hai run không hậu tố và _r2 có cùng kết quả, đã audit đủ ID/hash/metric. Phần 3 đã điền run và mục 6 đề xuất CLIP, chờ kiểm chéo/duyệt. Không cần lặp evaluator để cập nhật tiến độ.

**Việc của Trí ngay tiếp:** đọc [PILOT_SUMMARY mục 6–7](../reports/PILOT_SUMMARY.md), chuẩn bị bốn lựa chọn 6C cho P4 (phạm vi, checkpoint/cấu hình, nhãn/phép đo, phân công); phối hợp Triệu kiểm evaluator và duyệt báo cáo. CLIP chỉ là ứng viên sau B2, chưa chọn/chạy. Giữ đối chứng confidence, không chọn negative labels từ GT ảnh test.

Kaggle đã chạy đủ 1.190 ảnh; kiểm ngày 20/10: MAE=8.336975, RMSE=24.637626. [Báo cáo benchmark](../reports/BENCHMARK_FSCD147.md). Không cần chạy lại nhánh này để làm phần 2–3 pilot. Chưa train/cải tiến/holdout. Đo thời gian/VRAM chuẩn còn cần làm trước khi báo hiệu năng.

Mỗi buổi thêm mục WORKLOG; khi xong mốc mới đồng bộ trạng thái ROADMAP và việc tiếp HANDOFF. Assistant chạy đánh giá/thực nghiệm thay phải hỏi bạn trước.
