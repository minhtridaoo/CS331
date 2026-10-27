# Phần 3 — duyệt tổng kết pilot

**Cập nhật 27/10/2026: C1 đã đọc, Trí CHƯA DUYỆT; Triệu cần hoàn thành T1–T4 V2.** [Kế hoạch có lệnh/đầu vào/tiêu chí](../reports/KE_HOACH_SUA_KIEM_CHEO_20261027.md).

Phần 2 là chấm lại dự đoán B0/B2; Phần 3 là viết/chốt báo cáo. Hai việc này khác E2/E3 và khác nhánh cải tiến P4. Không cần làm thêm P4.6 để được đóng phần tổng kết pilot.

## Đã có, không cần làm lại

- Thông tin Minhtri chạy ngày 20/10, self-test PASS theo người chạy; output/ID/hash/metrics đã audit, _r2 cùng dữ liệu.
- B0/B2 MAE 19.4/22.0; review định tính Trí/Triệu 15/15 và các giới hạn nguồn.
- Kết quả benchmark FSCD-147 tách riêng, không đồng nhất với adapter B2.
- Mục 6 cập nhật kết quả P4 đã chạy ngày 20–21/10: CLIP/CV/Fusion/freeze; ghi rõ dev, nhãn tạm và chưa có holdout. [Audit 22/10](../reports/P4_AUDIT_20261022.md).

## Việc còn lại để đóng báo cáo

Triệu tự chạy T1 (30/10), gán/kiểm T2 (01/11), phân tích T3 (02/11). T4 ngày 03/11 hai người nghiệm thu, ghi rõ bằng chứng và giới hạn còn lại. Hạn đề xuất, chưa xác nhận đã nhận/xong. Giữ bản audit 24/10 như lịch sử; thêm mục việc Triệu tự làm thật, không đổi tác giả audit.

Không yêu cầu P4.6/47 nhãn q03 hoặc ablation mới để đóng vòng kiểm chéo. Trí tiếp chuẩn bị P4 song song; phần chưa biết cơ chế có thể báo là giới hạn, không bắt biến giả thuyết thành kết luận.

## Checklist

- [x] Có run, coverage, IDs và số liệu đối chiếu.
- [x] Có bằng chứng lỗi X/Y; giới hạn của review thủ công được nêu.
- [x] Phân biệt pilot, benchmark, P4 dev CV và dev-fit.
- [x] Mục 6 đã cập nhật theo artifact, không còn ghi chưa chạy CLIP.
- [x] Triệu đọc/hiểu/chấp nhận bản kiểm được ủy quyền ngày 24/10; không ghi là tự audit code.
- [ ] Triệu bàn giao đủ T1–T3 theo tiêu chí V2.
- [ ] T4 nhóm duyệt báo cáo, ghi người/ngày/quyết định đóng pilot.

**Việc làm trong 3 giờ:** [CHECKLIST_3_GIO](CHECKLIST_3_GIO.md); protocol ở [P4_TIEP_THEO](P4_TIEP_THEO.md), bắt đầu chuẩn bị dữ liệu mới rồi runner dùng freeze. Đây là nghiên cứu tiếp; không bổ sung vào checklist nghiệm thu pilot trên. 47 nhãn P4 cũng là việc kiểm riêng, chưa phải đã được Triệu xác nhận.

[Roadmap](ROADMAP.md) · [Handoff](../HANDOFF/HANDOFF.md) · [Nhật ký](../WORKLOG.md).
