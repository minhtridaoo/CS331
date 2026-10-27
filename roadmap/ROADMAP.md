# Roadmap CS331 — CountGD++ và lỗi đếm sai đối tượng

**V4.9 — Triệu chấp nhận bản kiểm được ủy quyền 24/10/2026.** Đây là bảng tiến độ chính. [Trang bắt đầu](../README.md) · [Nhật ký](../WORKLOG.md) · [Handoff](../HANDOFF/HANDOFF.md).

Đã có [bản hỗ trợ Triệu kiểm evaluator](../reports/TRIEU_EVALUATOR_CROSSCHECK_20261021.md), chưa ký xác nhận thay người kiểm. Repo cũng đã có artifact P4/CLIP; cần đồng bộ log và audit riêng, không dùng trạng thái “chưa chạy” của tài liệu ngày 20/10 như kết luận hiện tại.

**24/10:** assistant đã làm hộ toàn bộ đối chiếu kỹ thuật trên file pilot, gồm 15 dòng, bốn ví dụ, manual q05_2 và đọc logic error/null/uncertain/absent; [bản kết quả](../reports/TRIEU_KET_QUA_KIEM_CHEO_20261024.md). Triệu đang ưu tiên deadline paper. Triệu đã xác nhận trực tiếp đã đọc, hiểu và đồng ý dùng kết quả assistant kiểm; duyệt nhóm vẫn chờ. Không ghi Triệu đã tự audit code.

## Nhìn toàn bộ đồ án trong bốn chặng

| Chặng | Kết quả cần có | Trạng thái thực tế |
|---|---|---|
| 1. Chạy được baseline | Môi trường, checkpoint, inference và nhánh kiểm trên tập chuẩn | **Đã có.** Benchmark FSCD-147 1.190 ảnh đã kiểm count metrics ngày 20/10. |
| **2. Hiểu và đo lỗi X/Y** | Bộ thử nhỏ, review, evaluator, báo cáo lỗi | **ĐANG CHỐT CHẶNG NÀY.** Pilot/evaluator đã chạy; báo cáo đã điền. Triệu đã chấp nhận bản kiểm do assistant thực hiện; còn nhóm duyệt. |
| 3. Thử một cải tiến | Một giả thuyết có lý do, phương pháp, đối chứng trên cùng dữ liệu | **Có artifact khảo sát P4, chờ đồng bộ/audit/duyệt.** Score CLIP và report count đã có trong repo; chưa xác nhận hiệu quả hoặc nhóm duyệt ở lượt kiểm evaluator này. |
| 4. Đánh giá và báo cáo cuối | Cấu hình khóa trước đánh giá, tập riêng, bảng so sánh, ví dụ và giới hạn | **Chưa hoàn thành.** |

Bạn gần xong vòng kiểm baseline/pilot đầu tiên, chưa gần xong toàn bộ đồ án. Không gán phần trăm vì phạm vi cải tiến chưa chốt.

## Pilot và benchmark là hai nhánh khác nhau

**Pilot = bộ thử nhỏ để tìm lỗi:** 5 ảnh, 15 câu hỏi. Cùng ảnh hỏi những loại khác nhau để quan sát khung dự đoán. B0 là văn bản một lượt; B2 là lượt đầu → tối đa 3 mẫu tự chọn → lượt hai. Đây là đối chứng thành phần qua adapter.

**Benchmark = phép kiểm trên tập chuẩn:** FSCD-147 test, 1.190 ảnh, cấu hình text + synthetic + pseudo + adaptive cropping. Đã chạy đủ, số liệu MAE/RMSE khớp log. [Bằng chứng và giới hạn](../reports/BENCHMARK_FSCD147.md). Kết quả tổng thể này chưa trả lời đầy đủ câu hỏi đổi X/Y trên cùng ảnh.

## Tiến độ chi tiết

| Việc | Trạng thái ngày 20/10 | Bằng chứng / điều kiện xong |
|---|---|---|
| M0–M2: môi trường, checkpoint | Đã chạy được và audit | Inference thật; benchmark có log ops 6/6 đạt |
| M3: smoke 1 ảnh / 3 query | Đã chạy/xem ảnh | [Lịch sử trong WORKLOG](../WORKLOG.md) |
| M4–M5: B0/B2 pilot | Đã chạy đủ 5 ảnh / 15 query | [Review và bảng kết quả](../results/countgdpp/b2_remaining3_20261015/REVIEW.md) |
| M6: E1/E2 kiểm ngưỡng | Đã đóng phạm vi 2 ảnh / 6 query | E2 .35 không chạy; E3 chưa cần mở chỉ để đủ lưới |
| Review Trí / Triệu | **15/15 mỗi người về định tính** | [Review Triệu chốt v1 ngày 19/10](<../workspace Trí and Triệu/Triệu/TRIEU_VISUAL_REVIEW.md>), đọc lại 20/10; guitar/q04_2 đã làm rõ |
| **Phần 2: chấm lại pilot** | **Đã chạy; assistant audit; Triệu tự kiểm chéo 27/10, khớp** | Self-test PASS theo Minhtri; 5 file/run, 15 dòng khớp; 7 nguồn khớp nội dung (Windows: 3 byte thô, 4 chuẩn hóa EOL); [run chính](../results/countgdpp/pilot_eval_20261020/SUMMARY.md) |
| **Phần 3: tổng kết pilot** | **Đã điền; Triệu chấp nhận kết quả kiểm; chờ nhóm duyệt báo cáo** | [PILOT_SUMMARY](../reports/PILOT_SUMMARY.md) mục 6 kế hoạch, mục 7 xác nhận nhóm |
| Benchmark FSCD-147 theo cấu hình paper | **Đã chạy đủ; count metrics đã kiểm** | Run `full_20261015T080230Z`, audit 20/10; MAE=8.336975, RMSE=24.637626; chưa xác nhận AP/AP50 |
| P4: chọn một can thiệp | **Có đề xuất và artifact thử, chờ đồng bộ/audit/duyệt** | `p4_clip_all15_20261020`, `p4_count_cv_20261020/report.json`; lượt 21/10 chỉ đọc metadata, chưa xác nhận toàn bộ kết quả hoặc hiệu quả |
| P5: đánh giá cải tiến/holdout/báo cáo | Chưa làm | Khóa cấu hình, đánh giá tập riêng, báo kết quả và giới hạn |

Trạng thái “chưa có bằng chứng” được xác định từ file đang có; nếu bạn chạy ở máy khác thì nhập output/log để kiểm. Có code không có nghĩa đã chạy đạt.

## Phần 2 và phần 3 lần trước nghĩa là gì?

**Phần 2 = kiểm số liệu pilot bằng evaluator.** Đọc các dự đoán B0/B2 đã lưu, ghép đúng 15 ID với nhãn thật, tính MAE/RMSE và kiểm nhãn q05_2. Dùng CPU; không cần rerun model. Khác với **E2**, vốn là thí nghiệm đổi ngưỡng chọn mẫu đã làm trước đó.

**Phần 3 = chốt bản tổng kết pilot.** Ghi số liệu đã xác nhận, ví dụ lỗi, điều còn chưa chắc và câu hỏi sẽ thử tiếp. Phần này sửa Markdown, không có lệnh train. Khác với **E3**, vốn là lưới hai ngưỡng chưa cần chạy.

## Điều kiện đóng vòng pilot hiện tại

- [x] Phần chạy Phần 2: Minhtri báo self-test PASS; đã kiểm output cho 15 query/5 ảnh, metric/coverage hợp lệ và q05_2. Chưa có stdout self-test riêng; không yêu cầu chạy lại chỉ để lấy log.
- [x] Triệu đọc/hiểu và đồng ý dùng kết quả kiểm kỹ thuật do assistant thực hiện; ghi nhận trực tiếp ngày 24/10 tại mục 7 PILOT_SUMMARY. Không ghi Triệu đã tự audit code.
- [x] Triệu tự kiểm chéo Phần 2 ngày 27/10: self-test, tính lại metric, truy ngược q05_3, tự gán nhãn q05_2, thử dữ liệu hỏng, chạy lại evaluator; tất cả khớp. Đồng ý dùng số liệu kèm lưu ý kết luận B0/B2 phụ thuộc q05_3. [Báo cáo](../reports/TRIEU_TU_KIEM_PHAN2_20261027.md).
- [x] Review định tính đã đủ: bản Triệu chốt 15/15, guitar được xác nhận đúng theo quy ước review, q04_2 final giải thích đủ 32 khung. Không đồng nhất review này với annotation định vị chính thức hoặc xác minh độc lập mọi GT.
- [x] Phần 3 đã có run, dữ liệu đối chiếu và mục 6 đề xuất; phân biệt số liệu/quan sát/giả thuyết.
- [ ] Nhóm duyệt báo cáo, ghi người/ngày và quyết định đóng pilot để chuẩn bị P4. Bốn mục 6C phải được thống nhất trước lần chạy P4.

Đóng vòng nhỏ này chưa thay cho phần mở rộng dữ liệu: dự kiến 20–30 ảnh dev, xác minh nguồn/nhãn, có truy vấn vắng mặt chắc chắn và tập holdout theo ảnh gốc. Chốt phạm vi vừa sức cùng Triệu trước khi thực thi. Chỉ số định vị cần nhãn phù hợp và quy tắc matching, không suy ra từ count.

## Điều đã học được

Trên cùng 15 query: B0 MAE=19.4, RMSE≈24.316; B2 MAE=22.0, RMSE≈30.091; exact count 1/15 cả hai. B2 giảm sai số 6, tăng 4, giữ nguyên 5 query. Các số trong [evaluator ngày 20/10](../results/countgdpp/pilot_eval_20261020/metrics.json) đã đối chiếu với dữ liệu gốc và khớp kết quả cũ. Run `_r2` giống run chính, không cộng thành mẫu thí nghiệm độc lập.

Plates/rulers/raspberries có mẫu đúng loại 3/3 nhưng final vẫn sai/thừa. Blackberries có hiện tượng đếm phần quả. Những quan sát này hỗ trợ ưu tiên lỗi đếm nhầm loại, chưa chứng minh nguyên nhân nội tại hoặc khái quát ra mọi cấu hình CountGD++.

## Bước sau khi chốt pilot

Đã có **đề xuất** kiểm crop–query bằng CLIP sau B2 và artifact khảo sát trong repo. Trí cần đồng bộ log/config với artifact đã chạy và nhóm xác nhận bốn mục trong §6C [PILOT_SUMMARY](../reports/PILOT_SUMMARY.md) cho bước tiếp theo; lượt kiểm evaluator 21/10 chưa audit hiệu quả P4. Phạm vi vẫn là ảnh/query, không dùng lớp dễ nhầm rút từ GT ảnh test; so với B2 gốc và đối chứng chỉ lọc confidence. Mục tiêu là giảm khung sai loại mà giữ được vật đúng. Nếu cải tiến trên B2 thì kết luận giới hạn ở B2; muốn kết luận cho cấu hình paper phải kiểm cấu hình đó trên cùng dữ liệu/câu hỏi liên quan. MAE tổng thể trên FSCD-147 không thay phép đo X/Y.

Xác định phép đo, nhãn, dev/holdout trước khi chạy. Không train hay mở thêm model chỉ để có thêm việc. Khi chọn được phương pháp mới cập nhật kế hoạch thực thi, không xem lựa chọn còn bỏ trống là kết quả đã làm.

## Cách ghi tiến độ

Mỗi buổi thêm một mục ở [WORKLOG](../WORKLOG.md). Khi có mốc được kiểm, sửa dòng trạng thái ở đây và bước tiếp ở [HANDOFF](../HANDOFF/HANDOFF.md). Không tạo thêm handoff theo ngày tại thư mục hiện hành. Các bản cũ chỉ để tra cứu trong [quá khứ](<../quá khứ/README.md>).

[Protocol kỹ thuật](PIPELINE_COUNTGDPP.md) · [Phân công/schema](PIPELINE_PHAN_CONG.md). Mã M0–M6/E1–E3/P4–P5 được giữ để tra log cũ; dùng bốn chặng ở đầu trang khi báo cáo tiến độ.
