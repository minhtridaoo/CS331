# Phần 3 — duyệt tổng kết pilot và chuẩn bị sang P4

**Cập nhật 24/10/2026: báo cáo đã điền run/kết quả/đề xuất; Triệu đã chấp nhận bản kiểm do assistant thực hiện; CHỜ NHÓM DUYỆT BÁO CÁO.** File cần sửa duy nhất cho phần này: [reports/PILOT_SUMMARY.md](../reports/PILOT_SUMMARY.md).

Phần 2 đã có output được đối chiếu; Phần 3 không phải việc chạy model. “P2/P3” trong handoff gửi kèm là tên tắt Phần 2/3 này, không phải thí nghiệm E2/E3 hoặc cell Kaggle.

## Đã có, không cần làm lại

- Thông tin Minhtri chạy ngày 20/10, self-test PASS theo xác nhận người chạy, run `pilot_eval_20261020`.
- MAE/RMSE/coverage và q05_2 được kiểm trên file thật; run `_r2` cho cùng kết quả.
- Review định tính Trí/Triệu đều 15/15; guitar/q04_2 đã giải thích.
- Mục 6 **đã có** đề xuất dùng CLIP làm bộ lọc sau B2. Đây chưa phải phương pháp được nhóm chọn. Repo đã có artifact score/khảo sát P4; cần đồng bộ log và audit riêng, chưa xác nhận hiệu quả.

## Việc tiếp theo

1. **Triệu:** đã đọc/hiểu và đồng ý dùng [kết quả kiểm kỹ thuật do assistant thực hiện](../reports/TRIEU_KET_QUA_KIEM_CHEO_20261024.md); xác nhận trực tiếp ngày 24/10 đã ghi ở PILOT_SUMMARY mục 7. Cùng Trí duyệt báo cáo; không ghi Triệu đã tự audit code.
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
- [x] Triệu xác nhận đã đọc/hiểu và đồng ý dùng bản kiểm kỹ thuật do assistant thực hiện ngày 24/10; không coi là Triệu tự audit code.
- [ ] Nhóm duyệt báo cáo, ghi người/ngày và quyết định đóng pilot.
- [ ] Nhóm thống nhất kế hoạch P4; đồng bộ/audit artifact CLIP đã có trước khi chốt hiệu quả hoặc bước chạy tiếp; chưa có xác nhận holdout.

Ngày 21/10 đã bổ sung [Q02_1_DETAILED_REVIEW.md](<../workspace Trí and Triệu/Triệu/Q02_1_DETAILED_REVIEW.md>) và bằng chứng từ cuộc trò chuyện Triệu ngày 19/10. Giữ giới hạn nguồn/độ chắc chắn, không coi mọi nhóm là nhãn bbox đã được Triệu phân xử. [Bản hướng dẫn kiểm evaluator ngày 21/10](../reports/TRIEU_EVALUATOR_CROSSCHECK_20261021.md) là tài liệu tham chiếu; xác nhận đọc/chấp nhận của Triệu đã ghi ngày 24/10.

Lưu ý cập nhật trạng thái P4: repo đã có score CLIP và report khảo sát count; chưa audit toàn bộ trong lượt kiểm evaluator này. Trí cần đồng bộ log nguồn chạy và nhóm duyệt riêng, không đọc “chưa có kết quả CLIP” trong tài liệu ngày 20/10 như trạng thái hiện tại.

[Roadmap](ROADMAP.md) · [Handoff](../HANDOFF/HANDOFF.md) · [Nhật ký](../WORKLOG.md).
