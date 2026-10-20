# Handoff CS331 — tiếp tục sau Phần 2–3

**Cập nhật 20/10/2026 sau nhận handoff mới.** [Trang bắt đầu](../README.md) · [Roadmap V4.6](../roadmap/ROADMAP.md) · [Nhật ký](../WORKLOG.md).

## Đang ở đâu?

**Cuối chặng 2: đã chạy/chấm pilot và đã điền báo cáo; đang chờ kiểm chéo, duyệt để chuyển sang chuẩn bị P4.** Chưa triển khai hay có kết quả cải tiến.

## Đã kiểm trên file thật

- Phần 2 có đủ 5 output tại [pilot_eval_20261020](../results/countgdpp/pilot_eval_20261020). Có thêm `_r2` với 4 file kết quả giống hệt và cùng 7 hash nguồn. Dùng run đầu làm nguồn báo cáo; giữ `_r2` làm lịch sử chấm lại.
- Đối chiếu đủ 15 dòng/5 ảnh: B0 MAE=19.4, RMSE=24.315976; B2 MAE=22.0, RMSE=30.090973. Hai bên hợp lệ 15/15, không error/uncertain; absent=0 nên metric absent=null; cải thiện/kém đi/giữ nguyên=6/4/5.
- Manual q05_2 khớp: 14 khung = 4 vật đúng + 1 trùng + 9 sai loại. Đây là phép đếm nhãn thủ công, không phải AP/IoU.
- Self-test **PASS theo xác nhận Minhtri trong handoff**, chưa có stdout riêng; assistant không chạy lại evaluator/model. Lượt vừa rồi dùng `python3` hệ thống, không cần venv model để chấm JSON.
- Phần 3 đã điền run, số liệu, nguồn/giới hạn và **mục 6 đề xuất CLIP**. Trạng thái vẫn **CHỜ KIỂM CHÉO VÀ DUYỆT**.
- Review định tính Trí/Triệu 15/15, benchmark FSCD-147 1.190 ảnh đã kiểm trước đó giữ nguyên. [Benchmark](../reports/BENCHMARK_FSCD147.md).

Handoff đính kèm nói chưa thấy per_query/run_config hoặc chưa xác nhận đã sửa mục 6; kiểm workspace lần này đã xác nhận cả hai. Bản gửi gốc lưu trong [ZIP trước cập nhật](<../quá khứ/2026-10-20_truoc_xac_nhan_P2_P3.zip>), đường dẫn `incoming/HANDOFF_CS331_P2_P3_2026-10-20.md` bên trong.

## Việc tiếp theo theo người làm

1. **Triệu:** kiểm code/ghép ID/vài dòng nguồn/q05_2 theo [Phần 2, mục 3](../roadmap/PHAN_2_DANH_GIA.md); ghi tên/ngày/kết luận vào [PILOT_SUMMARY, mục 7](../reports/PILOT_SUMMARY.md). Review ảnh đã xong; không giao lại guitar/q04_2.
2. **Trí:** đọc mục 6 của báo cáo, xác nhận có muốn thử bộ lọc CLIP sau B2 theo phạm vi tối thiểu. Chuẩn bị bốn mục 6C: phạm vi, checkpoint/cấu hình, nhãn/phép đo, phân công. Có thể chuẩn bị song song lúc chờ Triệu; chưa tự coi ứng viên là phương pháp đã chọn.
3. **Cả nhóm:** duyệt báo cáo và ghi quyết định đóng pilot để chuẩn bị P4. Trước lần thử P4 phải thống nhất đối chứng/dữ liệu/cách đo; chưa chạy model mới trong lượt kiểm này.

## Các điểm giữ đúng phạm vi

- CountGD++ vẫn là model nền. CLIP chỉ là ứng viên kiểm crop–text; chưa có kết quả chứng minh cải thiện. Không quay sang tìm nhiều model mới.
- Không dùng GT ảnh test để chọn tên lớp loại trừ. Đo giữ vật đúng và loại khung sai, không chỉ nhìn count giảm. Có đối chứng confidence và dev/holdout tách theo ảnh gốc.
- File chi tiết q02_1 được nhắc trong review chưa có local; chỉ bổ sung nếu dùng bảng ghép chi tiết đó làm bằng chứng. Không chặn đánh giá count đã hoàn thành.
- Audit assistant không phải xác nhận của Triệu hoặc duyệt của nhóm. Không tự điền các ô xác nhận thay người thực hiện.

Theo yêu cầu người dùng ngày 19/10, assistant chạy evaluator/self-test/inference/train thay phải hỏi trước. Lượt này chỉ đọc/đối chiếu artifact, rà code, kiểm tài liệu nguồn và cập nhật tài liệu được yêu cầu.

[Phần Trí](HANDOFF_MODEL.md) · [Phần Triệu](HANDOFF_TRIEU.md) · [Protocol](../roadmap/PIPELINE_COUNTGDPP.md) · [Phân công](../roadmap/PIPELINE_PHAN_CONG.md).
