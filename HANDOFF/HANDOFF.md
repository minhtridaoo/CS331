# Handoff CS331 — tiếp tục sau Phần 2–3

**Cập nhật 20/10/2026 sau nhận handoff mới.** [Trang bắt đầu](../README.md) · [Roadmap V4.6](../roadmap/ROADMAP.md) · [Nhật ký](../WORKLOG.md).

**Bổ sung 21/10:** có [bản hỗ trợ Triệu kiểm evaluator](../reports/TRIEU_EVALUATOR_CROSSCHECK_20261021.md), đủ artifact chi tiết q02_1 và đối chiếu lại 15 dòng. Các xác nhận cá nhân/nhóm vẫn chờ. Repo đã có artifact score/khảo sát P4; các câu “chưa triển khai CLIP/P4” dưới đây là trạng thái tài liệu ngày 20/10, cần Trí đồng bộ log với nguồn hiện có, chưa coi P4 được audit/duyệt trong lượt này.

**Bổ sung 24/10:** theo yêu cầu Triệu ưu tiên deadline paper, assistant đã hoàn thành phần đối chiếu kỹ thuật; [bản kết quả đọc nhanh](../reports/TRIEU_KET_QUA_KIEM_CHEO_20261024.md). Sau đó Triệu đã trực tiếp xác nhận đọc/hiểu và đồng ý dùng bản kiểm do assistant thực hiện; duyệt nhóm vẫn chưa có. Trí có thể chuẩn bị/đồng bộ log P4 song song; không ghi P4 đã đạt hoặc nhóm đã chọn.

## Đang ở đâu?

**Cuối chặng 2: đã chạy/chấm pilot, assistant đã đối chiếu kỹ thuật và Triệu đã đọc/hiểu/chấp nhận kết quả; chờ nhóm duyệt toàn báo cáo.** Artifact khảo sát P4 đã có, chưa được audit hiệu quả ở lượt này.

## Đã kiểm trên file thật

- Phần 2 có đủ 5 output tại [pilot_eval_20261020](../results/countgdpp/pilot_eval_20261020). Có thêm `_r2` với 4 file kết quả giống hệt và cùng 7 hash nguồn. Dùng run đầu làm nguồn báo cáo; giữ `_r2` làm lịch sử chấm lại.
- Đối chiếu đủ 15 dòng/5 ảnh: B0 MAE=19.4, RMSE=24.315976; B2 MAE=22.0, RMSE=30.090973. Hai bên hợp lệ 15/15, không error/uncertain; absent=0 nên metric absent=null; cải thiện/kém đi/giữ nguyên=6/4/5.
- Manual q05_2 khớp: 14 khung = 4 vật đúng + 1 trùng + 9 sai loại. Đây là phép đếm nhãn thủ công, không phải AP/IoU.
- Self-test **PASS theo xác nhận Minhtri trong handoff**, chưa có stdout riêng; assistant không chạy lại evaluator/model. Lượt vừa rồi dùng `python3` hệ thống, không cần venv model để chấm JSON.
- Phần 3 đã điền run, số liệu, nguồn/giới hạn và **mục 6 đề xuất CLIP**. Triệu đã chấp nhận bản kiểm được ủy quyền; trạng thái còn **CHỜ NHÓM DUYỆT BÁO CÁO**.
- Review định tính Trí/Triệu 15/15, benchmark FSCD-147 1.190 ảnh đã kiểm trước đó giữ nguyên. [Benchmark](../reports/BENCHMARK_FSCD147.md).

Handoff đính kèm nói chưa thấy per_query/run_config hoặc chưa xác nhận đã sửa mục 6; kiểm workspace lần này đã xác nhận cả hai. Bản gửi gốc lưu trong [ZIP trước cập nhật](<../quá khứ/2026-10-20_truoc_xac_nhan_P2_P3.zip>), đường dẫn `incoming/HANDOFF_CS331_P2_P3_2026-10-20.md` bên trong.

## Việc tiếp theo theo người làm

1. **Triệu:** đã đọc/hiểu và chấp nhận bản kiểm kỹ thuật do assistant thực hiện, ghi nhận ngày 24/10 ở [PILOT_SUMMARY, mục 7](../reports/PILOT_SUMMARY.md). Cùng Trí duyệt báo cáo; không ghi Triệu đã tự audit code. Review ảnh đã xong.
2. **Trí:** đọc mục 6 của báo cáo, xác nhận có muốn thử bộ lọc CLIP sau B2 theo phạm vi tối thiểu. Chuẩn bị bốn mục 6C: phạm vi, checkpoint/cấu hình, nhãn/phép đo, phân công. Có thể tiếp tục chuẩn bị trong lúc nhóm duyệt báo cáo; chưa tự coi ứng viên là phương pháp đã chọn.
3. **Cả nhóm:** duyệt báo cáo và ghi quyết định đóng pilot để chuẩn bị P4. Trước lần thử P4 phải thống nhất đối chứng/dữ liệu/cách đo; chưa chạy model mới trong lượt kiểm này.

## Các điểm giữ đúng phạm vi

- CountGD++ vẫn là model nền. CLIP chỉ là ứng viên kiểm crop–text; chưa có kết quả chứng minh cải thiện. Không quay sang tìm nhiều model mới.
- Không dùng GT ảnh test để chọn tên lớp loại trừ. Đo giữ vật đúng và loại khung sai, không chỉ nhìn count giảm. Có đối chứng confidence và dev/holdout tách theo ảnh gốc.
- File chi tiết q02_1 và các JSON/ảnh bằng chứng đã được bổ sung ngày 21/10 từ bản review cuộc trò chuyện Triệu ngày 19/10; giữ các nhóm độ chắc chắn vừa và nguồn xác nhận riêng.
- Audit assistant không phải xác nhận của Triệu hoặc duyệt của nhóm. Không tự điền các ô xác nhận thay người thực hiện.

Theo yêu cầu người dùng ngày 19/10, assistant chạy evaluator/self-test/inference/train thay phải hỏi trước. Lượt này chỉ đọc/đối chiếu artifact, rà code, kiểm tài liệu nguồn và cập nhật tài liệu được yêu cầu.

[Phần Trí](HANDOFF_MODEL.md) · [Phần Triệu](HANDOFF_TRIEU.md) · [Protocol](../roadmap/PIPELINE_COUNTGDPP.md) · [Phân công](../roadmap/PIPELINE_PHAN_CONG.md).
