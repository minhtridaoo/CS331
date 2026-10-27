# Roadmap CS331 — CountGD++ và lỗi đếm sai đối tượng

**V4.9 — cập nhật 27/10/2026 sau pull phần Triệu (d6db189).** [Trang bắt đầu](../README.md) · [Nhật ký](../WORKLOG.md) · [Handoff](../HANDOFF/HANDOFF.md).

**P4.6b đã đạt kiểm dev; P4.6a đã xác nhận nhãn, còn chốt quy tắc/lịch sử sử dụng và khóa.** Phần chạy/chấm/viết pilot của Trí đã đủ để chờ duyệt; Triệu đã chấp nhận bản kiểm kỹ thuật được ủy quyền ngày 24/10; Trí đọc và chưa duyệt ngày 27/10, yêu cầu T1–T4 V2. Chưa đánh giá hai ứng viên trên tập ảnh mới độc lập. CountGD++ vẫn là model đếm; CLIP chỉ chấm crop, không phải CLIP-Count.

> **Vị trí hiện tại và lịch đến 02/12 (27/10 khuya):** [VI_TRI_PIPELINE_20261028.md](VI_TRI_PIPELINE_20261028.md). Đang ở bước [5] N4, giao Triệu, hạn 30/10.

## Toàn bộ đồ án trong bốn chặng

| Chặng | Trạng thái ngày 27/10 | Còn gì? |
|---|---|---|
| 1. Chạy baseline | Đã có môi trường, checkpoint, inference và benchmark FSCD-147 | Không cần rerun để ghi tiến độ |
| 2. Hiểu và đo lỗi X/Y | Pilot 5 ảnh/15 query, review, evaluator và nội dung báo cáo đã có | Triệu tự làm T1–T4 V2 theo yêu cầu Trí; nghiệm thu chung |
| 3. Thử một cải tiến | Đã thăm dò CLIP, đối chứng confidence, Fusion 50/50 và khóa ứng viên | Triệu kiểm nhãn P4; runner áp dụng freeze đã đạt kiểm dev |
| 4. Kiểm trên tập riêng và báo cáo cuối | Chưa có kết quả tập mới | P4.6a–d rồi quyết định kết luận/phương pháp cuối |

Không cần chờ Triệu để chuẩn bị dữ liệu và code cho bước tiếp. Không coi việc chuẩn bị này là pilot đã được nhóm duyệt, cũng không thêm P4.6 vào điều kiện đóng pilot. Chưa đủ căn cứ nói sắp xong toàn bộ đồ án hoặc gán phần trăm.

## Mốc đã làm và bằng chứng

| Mốc | Trạng thái | Nguồn / giới hạn |
|---|---|---|
| M0–M3: môi trường, checkpoint, smoke | Đã chạy | Lịch sử [WORKLOG](../WORKLOG.md) |
| M4–M5: B0/B2 | Đủ 5 ảnh / 15 query | [Pilot](../reports/PILOT_SUMMARY.md); B0 một lượt, B2 tối đa 3 pseudo rồi lượt hai |
| M6: E1/E2 | Đóng phạm vi 2 ảnh / 6 query | E2 .10/.23/.50; .35 không chạy; E3 chưa chạy |
| Review định tính | Trí và Triệu đều 15/15 | [Triệu chốt v1 19/10](<../workspace Trí and Triệu/Triệu/TRIEU_VISUAL_REVIEW.md>); không phải nhãn bbox P4 đã kiểm độc lập |
| Phần 2: evaluator | Đã chạy/audit; Triệu chấp nhận bản kiểm 24/10; **Triệu tự kiểm chéo 27/10, khớp** (self-test, Excel, 5 ca hỏng, chạy lại trùng run 20/10) | [Run chính](../results/countgdpp/pilot_eval_20261020/SUMMARY.md), [tự kiểm](../reports/TRIEU_TU_KIEM_PHAN2_20261027.md), [đánh giá](../reports/DANH_GIA_TRIEU_TU_KIEM_20261027.md) |
| Phần 3: tổng kết pilot | 27/10: Trí chưa duyệt kiểm chéo → Triệu tự kiểm Phần 2 (tối 27/10); còn q05_3 nhãn từng khung + phân tích B2/B0 (T2/T3); chờ nghiệm thu và duyệt chung | [PILOT_SUMMARY](../reports/PILOT_SUMMARY.md), phiếu nhóm ở §7 |
| Benchmark paper | 1.190 ảnh đã chạy, count metrics kiểm 20/10 | [FSCD-147](../reports/BENCHMARK_FSCD147.md): MAE 8.336975, RMSE 24.637626; chưa xác nhận AP/AP50 |
| P4.1–P4.2 | Có CLIP score và đối chứng CV | 15 query/481 khung; [CV](../results/countgdpp/p4_count_cv_20261020/report.json) |
| P4.3–P4.5 | Có review, ranking/prompt diagnostic và Fusion | [Báo cáo P4](../reports/P4_CLIP_EXPLORATORY_FINDINGS_20261021.md); nhãn q03 sơ bộ |
| P4.5a | Đã có gói kiểm nhãn; chưa nhận nhãn độc lập | [ZIP](../results/countgdpp/p4_label_review_handoff_20261021.zip): 47 khung, 3 CSV trắng |
| P4.5b–c | Đã khóa cấu hình, kiểm từ điểm lưu sẵn | [Freeze](../results/countgdpp/p4_candidate_freeze_20261021.json), [audit 22/10](../reports/P4_AUDIT_20261022.md); chưa kiểm inference ảnh mới |
| P4.6a–b | **XONG 27/10:** tập [p4_unseen_v1](../experiments/countgdpp/p4_unseen_v1/README.md) khóa 17:07; runner đạt kiểm dev (1)–(4) | [Hướng dẫn](P4_TIEP_THEO.md) |
| P4.6c–d | **Count xong 27/10**; review khung bằng người còn chờ | [Kết quả](../reports/P4_6_UNSEEN_RESULTS_20261027.md): P4.6c–d (count) **XONG 27/10**: trên 30 query mới, MAE cả 30 = B2 gốc 13.00 / lọc điểm 7.27 / **Fusion 5.53** (Fusion tốt hơn lọc điểm, CI [−3.2, −0.3]). B0 tham chiếu 6.77, và B0 tốt nhất trên query có mặt (5.70). Bộ lọc bỏ ~50% vật đúng; X/Y vẫn còn lỗi (hỏi people ra chó/xe; sheep/bicycles gần nghĩa bị đếm). |
| Cải tiến v2 (P/R) | **Lên kế hoạch 27/10**, chưa chạy. N4 → chọn nhánh → dev/test mới → một lần test | [roadmap/KE_HOACH_CAI_TIEN_20261027.md](KE_HOACH_CAI_TIEN_20261027.md) |
| P5: hoàn thiện kết luận/báo cáo cuối | Chưa hoàn thành | Phụ thuộc bằng chứng P4 và yêu cầu giảng viên, không mở thêm thí nghiệm chỉ để đủ mã mốc |

**C2 cập nhật xác nhận 27/10:** Trí đã xác nhận nhãn của 10 ảnh (20 present + 10 absent), assistant ghi theo tin nhắn 27/10. Chưa khóa: còn chốt quy tắc chấm và xác nhận lịch sử sử dụng ảnh. C3/dev (1)–(4) đã đạt ở phiên song song; chưa chạy ảnh mới. Nguồn: [xác nhận của Trí](../experiments/countgdpp/p4_unseen_v1/human_review_20261027.json).

## Những số liệu cần phân biệt

- **Pilot gốc:** B0 MAE 19.4; B2 MAE 22.0. B2 giảm sai số 6 query, tăng 4, giữ nguyên 5. Chỉ chấm lại dự đoán đã có, không phải lần inference mới.
- **CV trên 5 ảnh dev:** B2 lọc điểm MAE **4.6**, CLIP-only **6.8**, Fusion **5.8**. Mỗi lần dùng 4 ảnh chọn ngưỡng, 1 ảnh kiểm; cả 5 ảnh vẫn thuộc tập dev đã dùng thiết kế phương pháp. Fusion chưa thắng đối chứng về count.
- **Review 4 query:** nhãn hiện tại cho B2 lọc điểm giữ 12/22 vật đúng, Fusion 16/22. Kết quả tạm, q03 chờ kiểm độc lập; không phải AP/IoU hay bằng chứng khái quát.
- **Fit ngưỡng trên toàn dev:** B2 MAE 4.333333, Fusion 4.4. Đây là điểm trên dữ liệu chọn tham số, không thay bảng CV và không phải holdout.

Benchmark FSCD-147 dùng text + synthetic + pseudo + adaptive cropping, khác adapter B0/B2 pilot. Không so trực tiếp MAE giữa hai bộ để tuyên bố cải thiện. Nếu sau này cải thiện trên B2, kết luận giới hạn ở cấu hình đó.

## Điều kiện đóng pilot — T1–T4 có giới hạn

- [x] Trí đã chạy Phần 2; đủ output/IDs/metrics. Self-test PASS theo người chạy, không có stdout riêng.
- [x] Review định tính đã đủ 15/15; giữ giới hạn và bất đồng đã xử lý trong nguồn.
- [x] Phần 3 có thông tin run, số liệu, lỗi, nguồn/giới hạn và hướng tiếp.
- [x] Triệu đọc/hiểu và chấp nhận bản kiểm kỹ thuật do assistant thực hiện 24/10; bằng chứng ở PILOT_SUMMARY §7. Không ghi Triệu tự audit code.
- [x] Triệu tự kiểm chéo Phần 2 ngày 27/10: self-test, tính lại metric, truy ngược q05_3, tự gán nhãn q05_2, thử dữ liệu hỏng, chạy lại evaluator; tất cả khớp. Đồng ý dùng số liệu kèm lưu ý kết luận B0/B2 phụ thuộc q05_3. [Báo cáo](../reports/TRIEU_TU_KIEM_PHAN2_20261027.md).
- [~] Triệu T1 xong phần lớn (thiếu 2 ca uncertain/absent); T2 q05_2 xong, q05_3 chưa gán nhãn từng khung; T3 mới có phân tích độ nhạy.
- [ ] T4 nhóm duyệt báo cáo, ghi tên/ngày/quyết định đóng vòng pilot.

**Kiểm nhãn 47 khung P4 là việc riêng.** Không đợi P4.6 hoàn thành mới đóng pilot, không ký thay Triệu.

## Việc làm ngay

**Trí:** nhãn C2 đã xác nhận, C3 đã đạt. Tiếp chốt quy tắc chấm/lịch sử sử dụng rồi khóa; chia sẻ T0 nếu chưa. Không cần kiểm lại nhãn hoặc rerun dev để ghi tiến độ.

**Triệu:** [T1–T4 V2](../reports/KE_HOACH_SUA_KIEM_CHEO_20261027.md), hạn đề xuất 30/10 → 01/11 → 02/11 → 03/11. T1 giữ 15 query trong fixtures, q05_2 nguyên trạng; T2 có nhãn uncertain và quy tắc cộng; T3 phân biệt B2=4.6/CLIP-only=6.8/Fusion=5.8. 47 nhãn q03 riêng cho P4, không thêm vào gate đóng pilot.

Các file bổ sung vẫn local, không có trên origin/main d6db189; đã chuẩn bị ZIP T1–T4, chưa gửi/commit/push. Có code/gói không có nghĩa Triệu đã chạy hoặc nhãn đã được kiểm.

**Deadline cuối: 02/12/2026.** Mốc nội bộ: sửa kiểm chéo trước 03/11, runner/dữ liệu trước 08/11, kết quả mới trước 15/11, bản thảo 22/11, hoàn thiện 29/11, dự phòng 30/11–01/12. Thời lượng T1–T4 đề xuất 6–10 giờ, có thể song song việc Trí; ước lượng tổng cũ 15–24 giờ không tự bao gồm phạm vi tự kiểm mới.

Mỗi buổi thêm một mục [WORKLOG](../WORKLOG.md); khi có mốc mới, sửa trạng thái ở đây và [HANDOFF](../HANDOFF/HANDOFF.md). [Protocol kỹ thuật](PIPELINE_COUNTGDPP.md) · [Phân công/schema](PIPELINE_PHAN_CONG.md). Tài liệu cũ lưu ở [quá khứ](<../quá khứ/README.md>).

[Bản bàn giao tổng hợp cho session mới](../BAT_DAU_SESSION_MOI.md) được tạo ngày 27/10; không đánh dấu thêm mốc thực nghiệm nào hoàn thành.
