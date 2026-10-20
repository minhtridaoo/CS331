# Phần 3 — duyệt tổng kết pilot và chuẩn bị sang P4

**Cập nhật sau handoff 20/10/2026: báo cáo đã điền run, kết quả và đề xuất mục 6; CHỜ KIỂM CHÉO VÀ DUYỆT.** File cần sửa duy nhất cho phần này: [reports/PILOT_SUMMARY.md](../reports/PILOT_SUMMARY.md).

Phần 2 đã có output được đối chiếu; Phần 3 không phải việc chạy model. “P2/P3” trong handoff gửi kèm là tên tắt Phần 2/3 này, không phải thí nghiệm E2/E3 hoặc cell Kaggle.

## Đã có, không cần làm lại

- Thông tin Minhtri chạy ngày 20/10, self-test PASS theo xác nhận người chạy, run `pilot_eval_20261020`.
- MAE/RMSE/coverage và q05_2 được kiểm trên file thật; run `_r2` cho cùng kết quả.
- Review định tính Trí/Triệu đều 15/15; guitar/q04_2 đã giải thích.
- Mục 6 **đã có** đề xuất dùng CLIP làm bộ lọc sau B2. Đây là điểm cập nhật mới hơn handoff gửi kèm, vẫn chưa phải phương pháp được nhóm chọn hoặc đã triển khai.

## Việc tiếp theo

1. **Triệu:** theo [mục 3 của Phần 2](PHAN_2_DANH_GIA.md), kiểm code/ID/vài dòng kết quả và q05_2. Ghi kết luận ở phiếu xác nhận cuối PILOT_SUMMARY. Không thay xác nhận này bằng review ảnh cũ.
2. **Trí:** đọc mục 6 đã làm rõ trong PILOT_SUMMARY; xác nhận muốn thử giả thuyết lọc khung sai loại. Phiên bản tối thiểu đề xuất dùng crop + query, chưa dùng tên lớp dễ nhầm lấy từ nhãn thật ảnh kiểm tra.
3. **Cả hai:** duyệt kết luận và giới hạn; quyết định “đóng pilot, chuyển sang chuẩn bị P4” hoặc chỉ rõ một điểm cần sửa. Chưa cần hoàn tất toàn bộ bộ dữ liệu P4 để đóng báo cáo pilot.
4. Trước lần thử P4, chốt checkpoint CLIP, quy tắc crop/prompt/score, nhãn và đối chứng. Giữ B2 gốc; thêm đối chứng chỉ lọc confidence để kiểm liệu lợi ích có vượt việc giảm số khung đơn thuần. Chọn tham số trên dev, chưa mở holdout.

## Checklist nghiệm thu báo cáo

- [x] Phạm vi 5 ảnh/15 query dev, E1/E2 chỉ 2 ảnh/6 query rõ ràng.
- [x] Có run thực tế, cùng IDs và coverage, số liệu khớp bằng chứng.
- [x] Tách kết quả chấm lại khỏi dữ liệu/review kế thừa.
- [x] Review Triệu chốt 15/15; không gọi là metric định vị chính thức.
- [x] Benchmark FSCD-147 để riêng; B2 adapter không được gọi là toàn bộ pipeline paper.
- [x] Mục 6 có giả thuyết, ứng viên và đối chứng ở trạng thái đề xuất.
- [ ] Triệu xác nhận kiểm chéo evaluator.
- [ ] Nhóm duyệt báo cáo, ghi người/ngày và quyết định đóng pilot.
- [ ] Kế hoạch P4 cụ thể được nhóm thống nhất trước thực thi; chưa có kết quả CLIP/cải tiến/holdout.

File `Q02_1_DETAILED_REVIEW.md` chưa có trong workspace khi kiểm; chỉ cần bổ sung nếu dùng bảng ghép chi tiết đó làm bằng chứng. Giữ kết luận định tính và giới hạn nguồn trong bản review, không chặn count evaluator hoặc tự tạo nhãn thay thế.

[Roadmap](ROADMAP.md) · [Handoff](../HANDOFF/HANDOFF.md) · [Nhật ký](../WORKLOG.md).
