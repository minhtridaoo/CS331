# Handoff CS331 — bắt đầu session mới tại đây

**Bản tổng hợp để chuyển session:** [BAT_DAU_SESSION_MOI.md](../BAT_DAU_SESSION_MOI.md). Trạng thái mới hơn trong checklist/WORKLOG vẫn được ưu tiên.

**Cập nhật 27/10/2026, sau pull phần Triệu.** [Checklist 3 giờ + điểm dừng](../roadmap/CHECKLIST_3_GIO.md) · [Roadmap V4.8](../roadmap/ROADMAP.md) · [WORKLOG](../WORKLOG.md).

> **MỚI NHẤT — 27/10 khuya (Trí nghỉ, giao việc):**
> - **Vị trí pipeline + lịch đến 02/12:** [roadmap/VI_TRI_PIPELINE_20261028.md](../roadmap/VI_TRI_PIPELINE_20261028.md).
> - **N4 giao Triệu** (hạn 30/10). Trí đã chấm u01_1 (9/9: 7 wrong_class chó, 2 multi_object chó). Việc của Triệu V1–V7, kèm gợi ý V8–V10 làm thay Trí: [HANDOFF/GIAO_VIEC_TRIEU_20261028.md](../HANDOFF/GIAO_VIEC_TRIEU_20261028.md). Gói gửi: `HANDOFF/TRIEU_GIAO_VIEC_20261028.zip` (thay ZIP V2 cũ chưa gửi).
> - **Việc đầu tiên của Trí ngày 28/10 (45 phút):** commit + push (lệnh ở §4 file vị trí pipeline) → gửi Triệu file giao việc → nghiệm thu bản tự kiểm của Triệu → chốt quy tắc dữ liệu dev 20 + test 40.

## Việc đầu tiên của phiên tiếp theo

**C1 đã xong: Trí đọc và CHƯA DUYỆT phần kiểm chéo.** Theo [kế hoạch V2](../reports/KE_HOACH_SUA_KIEM_CHEO_20261027.md), Triệu tự làm T1–T4; việc chấp nhận audit 24/10 không thay yêu cầu mới.

- **Trí:** chia sẻ/kiểm nhận T0 nếu chưa. P4.6c–d (count) **XONG 27/10**: trên 30 query mới, MAE cả 30 = B2 gốc 13.00 / lọc điểm 7.27 / **Fusion 5.53** (Fusion tốt hơn lọc điểm, CI [−3.2, −0.3]). B0 tham chiếu 6.77, và B0 tốt nhất trên query có mặt (5.70). Bộ lọc bỏ ~50% vật đúng; X/Y vẫn còn lỗi (hỏi people ra chó/xe; sheep/bicycles gần nghĩa bị đếm). [Báo cáo](../reports/P4_6_UNSEEN_RESULTS_20261027.md). Tiếp: quyết định có review khung bằng người (N4) hay không, rồi viết báo cáo (P5).
- **Pull 36eaf96 (27/10 tối):** Triệu tự kiểm chéo Phần 2: self-test, tính lại bằng Excel, 5 ca dữ liệu hỏng, chạy lại evaluator (trùng run 20/10), tự gán nhãn q05_2. Assistant đánh giá ([đánh giá](../reports/DANH_GIA_TRIEU_TU_KIEM_20261027.md)): nhận xét 1 + q05_2 **đạt**; còn thiếu q05_3 gán nhãn từng khung (79 + 21), 2 ca thử (uncertain, absent > 0), phân tích B2/B0 + đề xuất cải thiện. Trí chưa nghiệm thu.
- **Hướng cải tiến (27/10 tối):** Trí đưa đề xuất trong `hướng cái tiển/` (nhánh P kiểm mẫu tự chọn / nhánh R bộ lọc giữ vật đúng, dev và test mới). Kế hoạch thực thi: [roadmap/KE_HOACH_CAI_TIEN_20261027.md](../roadmap/KE_HOACH_CAI_TIEN_20261027.md). **Việc đầu tiên là N4 tầng A** (gói chính + `bo_sung_F0/`) để chọn P hoặc R. Chỉ báo tự động: E1 (mẫu sai) và E3 (Fusion xóa vật đúng) đều lớn. MUCCA chỉ còn 19–34 ảnh có cặp khác siêu nhóm, nên tập mới phải thêm cặp dễ nhầm.
- **N4 (27/10):** gói review khung chọn lọc, mù với cách lọc, đã sẵn ở [gói](../results/countgdpp/p4_n4_review_package_20261027/README.md). Tầng A gồm 7 query / 78 khung (4 query people + 3 query vắng mặt bị báo sai), tầng B gồm 2 query / 41 khung. Trí điền CSV rồi assistant ghép với bảng tra. Tóm tắt toàn dự án cho demo: [TOM_TAT](../reports/TOM_TAT_DU_AN_20261027.md).
- **Triệu:** T1 (30/10) → T2 (01/11) → T3 (02/11) → T4 cùng Trí (03/11), hạn đề xuất. 47 nhãn q03 là việc P4 riêng.
- Adapter đã kiểm đủ (1)–(4) trên dev, trùng artifact tham chiếu. Đây là kiểm triển khai, chưa chứng minh hiệu quả trên ảnh mới.

Bản V2 sửa lệnh T1 và fixtures, nguồn đầu vào, tên số liệu P4, lịch phụ thuộc và tiêu chí nghiệm thu. ZIP chỉ chuẩn bị local, chưa gửi/commit/push. Kết thúc mỗi buổi cập nhật bảng “Dừng ở đâu” trong checklist và WORKLOG; kế hoạch chưa thực thi phải giữ trống.

**C2 cập nhật 27/10 17:08:** Trí xác nhận nhãn của 10 ảnh và quy ước chấm §4. Absent mcac_88/84 đổi trucks→bicycles trước khi khóa; tập **LOCKED** (hash trong selection_meta.json và WORKLOG).

## Trạng thái đã xác nhận

- Đã pull `origin/main` từ `31278dd` lên **d6db18931c07671763137962f7db54bd1fc3be70**. Hợp nhất tài liệu ngày 22/10 local với phần Triệu ngày 21/24. Chưa commit/push cập nhật local của lượt này.
- **Phần 2 đã được chấp nhận:** Triệu xác nhận đọc/hiểu và đồng ý dùng bản kiểm kỹ thuật do assistant thực hiện ngày 24/10. Không phải Triệu tự audit code. [Xác nhận](../reports/audits/TRIEU_ACCEPTANCE_20261024.json).
- **Phần 3 chưa được Trí duyệt:** ngày 27/10 yêu cầu T1–T4 tự kiểm/phân tích; sau sửa mới duyệt chung. Không yêu cầu model inference mới để đóng pilot.
- **P4 đã chạy P4.6c–d (count) trên tập mới đã khóa, 27/10.** Xem báo cáo P4_6_UNSEEN_RESULTS_20261027.md. CountGD++ là model đếm, CLIP phụ trợ.
- **47 nhãn P4 còn chờ:** commit mới không có ba CSV q03 được kiểm độc lập. Không nhầm xác nhận evaluator với kiểm nhãn.
- Đã nhận đủ q02_1 chi tiết (3 JSON, 9 ảnh); các nhóm chưa được người kiểm phân xử hết vẫn ghi rõ trong nguồn.

## Kết quả cần giữ nguyên

Pilot B0/B2 MAE **19.4/22.0**. P4 dev CV: lọc điểm B2 **4.6**, CLIP-only **6.8**, Fusion **5.8**; Fusion chưa thắng về count. Review giữ 12/22 so với 16/22 vật đúng là tạm, q03 cần kiểm độc lập. Dev-fit 4.333333/4.4 khác CV, không phải holdout.

Freeze: B2 threshold `0.9067394733428955`, Fusion `0.6551826746408328`, min/max từ dev cố định. Không chỉnh theo ảnh mới. Benchmark FSCD-147 đã kiểm 1.190 ảnh, MAE 8.336975/RMSE 24.637626, khác dữ liệu/cấu hình pilot.

## Chia việc và lịch

[Kế hoạch V2](../reports/KE_HOACH_SUA_KIEM_CHEO_20261027.md) là nguồn nghiệm thu T0–T4. [Checklist](../roadmap/CHECKLIST_3_GIO.md) giữ tiến độ Trí/C2/C3. T1–T4 giới hạn ở 7 tình huống evaluator, q05_2/q05_3 và một báo cáo phân tích; không yêu cầu nghiên cứu mới để đóng kiểm chéo. Nếu còn bất đồng nhãn, ghi và phân xử, không tự ký thay.

Deadline báo cáo cuối **02/12/2026**. Mốc sửa kiểm chéo đề xuất kết thúc **03/11** để giữ lịch kiểm dev/dữ liệu trước 08/11, kết quả tập mới trước 15/11, bản thảo trước 22/11 và hoàn thiện trước 29/11. Không có cam kết rằng Triệu đã nhận mốc. Thời lượng T1–T4 khoảng 6–10 giờ cho nhánh kiểm/phân tích, riêng công việc Trí/P4; không dùng ước lượng 15–24 giờ cũ như cam kết tổng sau mở rộng yêu cầu.

## Lưu trạng thái và quyền thực hiện

Snapshot trước pull: [ZIP](<../quá khứ/2026-10-27_truoc_pull.zip>), đủ 13 file tracked đang sửa và 20 file untracked. Stash giữ để phục hồi: `a34cf35f5b5ce959b7f8469fe7c14afec242d263`; **không apply lại** vào workspace đã hợp nhất. Raw artifact, freeze và các bản nhận của Triệu giữ nguyên. [Bản kiểm tiếp nhận](../reports/SYNC_TRIEU_20261027.md).

Assistant phải hỏi trước nếu chạy evaluator/self-test/inference/train/thực nghiệm thay; đã được phép đọc/đối chiếu, pull và cập nhật tài liệu. Không tự ký duyệt nhóm hoặc gửi tin cho Triệu. Người dùng có thể tự chạy theo workflow đã chốt.

[Phần Trí](HANDOFF_MODEL.md) · [Phần Triệu](HANDOFF_TRIEU.md) · [Protocol P4](../roadmap/P4_TIEP_THEO.md). Câu mở session mới nằm ở cuối checklist; không cần giữ chat cũ để dùng được các file trên.
