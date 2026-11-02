# CS331 — bàn giao session mới, cập nhật sau rà giao việc V2 ngày 27/10/2026

> **Trạng thái hiện hành — đồng bộ 02/11/2026:** Bản trước cập nhật `71009c8` đã gồm `415af3b` (V3 + app gán nhãn) và `71009c8` (V5 + đề xuất P). V3/V5 đã nộp; xem [đánh giá đã lưu](reports/DANH_GIA_TRIEU_V3_V5_20261102.md). Còn V4 (hạn gốc 01/11), V6 (hạn gốc 02/11), V7 duyệt chung dự kiến 03/11. **Dời V4/V6 sang 04/11 chỉ là đề xuất, chưa có xác nhận trong lượt này.** N4 A còn ca nhãn cần thống nhất; app mới dành cho q05 không tự chứng minh N4 đã được sửa. P/T, C6 và dữ liệu dev/test mới đang ở mức đề xuất, chưa duyệt hoặc chạy. Các mốc cũ bên dưới giữ để tra lịch sử; ưu tiên ghi chú này và bảng resume. Đã push đủ 13 file đánh giá/tiến độ trong commit `22a10e2`; kiểm local và remote main khớp ngày 02/11.

> **Đồng bộ Git đã xác nhận — 27/10/2026:** đã push commit [`e877541`](https://github.com/minhtridaoo/CS331/commit/e8775412f84f0927a6fe692f1f106bf53aacd369) lên `origin/main`; HEAD local khớp remote. Code, kết quả P4.6, gói N4 và phân công đã có trên GitHub. Bản ZIP sao lưu trong `quá khứ/`, dữ liệu MUCCA gốc và checkpoint vẫn ở máy.
> **Việc tiếp theo:** Trí gửi đường dẫn [giao việc cho Triệu](HANDOFF/GIAO_VIEC_TRIEU_20261028.md), nghiệm thu phần kiểm chéo đã đạt và chốt quy tắc dữ liệu mới. Triệu làm N4 tầng A (V1–V2); chưa xác nhận đã nhận/hoàn thành.
> **Trạng thái ưu tiên:** P4.6a–b đã xong; tập 10 ảnh/30 query đã khóa và P4.6c–d phần count đã chạy. Hiện ở N4 review khung, chưa chọn nhánh cải tiến P/R. Các hướng dẫn chuẩn bị C2/C3 và câu “chưa push/chưa chạy ảnh mới” còn lại bên dưới mô tả thời điểm trước; không phải việc phải làm lại. Lượt đồng bộ Git này không chạy thí nghiệm.

**Deadline báo cáo cuối: 02/12/2026.** Đây là bản tổng hợp; ưu tiên trạng thái mới hơn trong [HANDOFF](HANDOFF/HANDOFF.md), [checklist](roadmap/CHECKLIST_3_GIO.md) và [WORKLOG](WORKLOG.md).

> **MỚI NHẤT — 02/11:** đã pull `71009c8`. Triệu nộp **V3** (q05_3, 103 khung: B2 tăng 58 khung `part` dù 2/3 mẫu đúng loại) và **V5** (tập mới: B2 kém B0 ở 15/30 query; đề xuất nhánh P). Cả hai đạt kiểm. **Chưa có V4 (2 ca thử) và V6 (tầng B, hạn 02/11).** Đánh giá: [reports/DANH_GIA_TRIEU_V3_V5_20261102.md](reports/DANH_GIA_TRIEU_V3_V5_20261102.md).
> - Bằng chứng mới ([RA_SOAT](reports/RA_SOAT_TRIEU_N4_20261029.md) §3): ở lượt 2, điểm khung = max(token chữ, token mẫu ảnh), nên ô tô giữ nhờ điểm mẫu 0,97 dù điểm chữ "people" chỉ 0,04. Gợi ý thêm biến thể **T (chấm lượt 2 chỉ bằng token chữ)** cạnh P; R giữ dự phòng; C6 bắt buộc.
> - **Buổi 03/11:** Trí + Triệu duyệt pilot (V7), chốt danh sách biến thể thử trên dev và quy tắc dữ liệu dev 20 + test 40. Nhắc Triệu V4 + V6, hạn 04/11.

> **MỚI NHẤT — 29/10:** đã pull `be4da26`. **Triệu xong N4 tầng A (V1 + V2) đúng hạn**; nhãn đạt kiểm (117 dòng, tọa độ không đổi; Trí và Triệu đồng ý 9/9 ở u01_1). Kết quả: [reports/N4_KET_QUA_TANG_A_20261029.md](reports/N4_KET_QUA_TANG_A_20261029.md).
> - Khung bộ lọc giữ trong 7 query lỗi: **0 vật đúng** (lọc điểm 0/78, Fusion 0/14). Hỏi "people" ở mcac_88 thì 21/21 khung trùng khung "cars".
> - Mẫu tự chọn: **1/21 đúng loại** (E1 chiếm ưu thế). Người thật bị lọc mất: 13/18 ứng viên E3.
> - **Đề xuất: nhánh P** (kiểm mẫu bằng CLIP + điều kiện một vật), C6 làm đối chứng bắt buộc, **bỏ nhánh R** (R sẽ cứu nhầm chó/ô tô). **Chờ Trí quyết.**
> - Triệu tiếp V3 q05_3, V4, V5 (hạn 01/11) và V6 tầng B (02/11).

> **MỚI NHẤT — 27/10 khuya (Trí nghỉ, giao việc):**
> - **Vị trí pipeline + lịch đến 02/12:** [roadmap/VI_TRI_PIPELINE_20261028.md](roadmap/VI_TRI_PIPELINE_20261028.md).
> - **N4 giao Triệu** (hạn 30/10). Trí đã chấm u01_1 (9/9: 7 wrong_class chó, 2 multi_object chó). Việc của Triệu V1–V7, kèm gợi ý V8–V10 làm thay Trí: [HANDOFF/GIAO_VIEC_TRIEU_20261028.md](HANDOFF/GIAO_VIEC_TRIEU_20261028.md). Gói gửi: `HANDOFF/TRIEU_GIAO_VIEC_20261028.zip` (thay ZIP V2 cũ chưa gửi).
> - **Việc đầu tiên của Trí ngày 28/10 (45 phút):** commit + push **đã xong 27/10** → gửi Triệu file giao việc → nghiệm thu bản tự kiểm của Triệu → chốt quy tắc dữ liệu dev 20 + test 40.

## 1. Việc đầu tiên cần tiếp

**C1 đã làm:** Trí đã đọc bản kiểm ngày 24/10 và **chưa duyệt**, yêu cầu Triệu tự chạy evaluator, phân tích q05_2/q05_3 và giải thích B2 kém B0. Không tiếp tục nói C1 chưa làm hoặc audit cũ đã đủ để bỏ yêu cầu mới.

- **Trí:** chia sẻ ZIP T0 nếu chưa. P4.6c–d (count) **XONG 27/10**: trên 30 query mới, MAE cả 30 = B2 gốc 13.00 / lọc điểm 7.27 / **Fusion 5.53** (Fusion tốt hơn lọc điểm, CI [−3.2, −0.3]). B0 tham chiếu 6.77, và B0 tốt nhất trên query có mặt (5.70). Bộ lọc bỏ ~50% vật đúng; X/Y vẫn còn lỗi (hỏi people ra chó/xe; sheep/bicycles gần nghĩa bị đếm). [Báo cáo](reports/P4_6_UNSEEN_RESULTS_20261027.md). Việc tiếp theo: quyết định review khung bằng người (N4) và viết báo cáo/demo (P5).
- **Pull 36eaf96 (27/10 tối):** Triệu tự kiểm chéo Phần 2: self-test, tính lại bằng Excel, 5 ca dữ liệu hỏng, chạy lại evaluator (trùng run 20/10), tự gán nhãn q05_2. Assistant đánh giá ([đánh giá](reports/DANH_GIA_TRIEU_TU_KIEM_20261027.md)): nhận xét 1 + q05_2 **đạt**; còn thiếu q05_3 gán nhãn từng khung (79 + 21), 2 ca thử (uncertain, absent > 0), phân tích B2/B0 + đề xuất cải thiện. Trí chưa nghiệm thu.
- **Hướng cải tiến (27/10 tối):** Trí đưa đề xuất trong `hướng cái tiển/` (nhánh P kiểm mẫu tự chọn / nhánh R bộ lọc giữ vật đúng, dev và test mới). Kế hoạch thực thi: `roadmap/KE_HOACH_CAI_TIEN_20261027.md`. **Việc đầu tiên là N4 tầng A** (gói chính + `bo_sung_F0/`) để chọn P hoặc R. Chỉ báo tự động: E1 (mẫu sai) và E3 (Fusion xóa vật đúng) đều lớn. MUCCA chỉ còn 19–34 ảnh có cặp khác siêu nhóm, nên tập mới phải thêm cặp dễ nhầm.
- **N4 (27/10):** gói review khung chọn lọc, mù với cách lọc, đã sẵn ở `results/countgdpp/p4_n4_review_package_20261027/`. Tầng A gồm 7 query / 78 khung (4 query people + 3 query vắng mặt bị báo sai), tầng B gồm 2 query / 41 khung. Trí điền CSV rồi assistant ghép với bảng tra. Tóm tắt toàn dự án cho demo: `reports/TOM_TAT_DU_AN_20261027.md`.
- **Triệu:** thực hiện [T1–T4 V2](reports/KE_HOACH_SUA_KIEM_CHEO_20261027.md). Assistant đã chuẩn bị hướng dẫn/gói, chưa chạy hoặc điền nhãn/kết luận thay Triệu.
- T0 và T1–T4 chưa có bằng chứng đã nhận/xong; chỉ đánh dấu khi có file/log/xác nhận thật.

## 2. Trạng thái kỹ thuật

CountGD++ là model đếm, CLIP là bộ chấm crop–query phụ trợ, không phải CLIP-Count. Bài toán là cùng ảnh hỏi X/Y khác loại phải chọn đúng loại được hỏi.

- Pilot 5 ảnh/15 query đã chạy: B0 MAE 19.4, B2 22.0. Benchmark FSCD-147 1.190 ảnh là nhánh khác; không so trực tiếp hai bảng để tuyên bố cải thiện.
- P4 dev CV: **B2 lọc confidence 4.6, CLIP-only 6.8, Fusion 50/50 5.8**. Fusion chưa thắng về count; nhãn cho nhận xét giữ đúng vật còn tạm.
- Freeze đã khóa; dev-fit 4.333333/4.4 khác CV và không phải holdout.
- Runner mới đã kiểm đủ (1)–(4) trên dev, trùng tuyệt đối. Nguồn: [SUMMARY](reports/audits/devcheck_20261027/SUMMARY.md). Không phải kết quả holdout.
- Dữ liệu B 10 ảnh/30 query: Trí xác nhận nhãn; **LOCKED 27/10 17:07:55**. Hash và các thay đổi trước khi khóa ghi trong `experiments/countgdpp/p4_unseen_v1/selection_meta.json` và WORKLOG. Chưa chạy model trên tập này.
- **47 nhãn q03 vẫn riêng cho P4**, không cộng vào gate đóng pilot T1–T4.

## 3. Những điểm đã sửa trong phân công

1. T1 mkdir trước redirect; từng fixture giữ đủ 15 query, chỉ sửa q01_1, giữ nguyên q05_2 để manual_check vẫn hợp lệ. Không tự dùng flag skip chưa có trong code. Triệu lưu cả stdout và exit code; ca lỗi phải bị từ chối đúng lý do.
2. Các gói có local nhưng chưa có trên origin/main d6db189. Đã chuẩn bị ZIP có input/code/overlay/CSV trắng/report nguồn, chưa gửi. p4_unseen_v1 thuộc nhánh Trí, không chặn T1–T3.
3. Gọi đúng 4.6/6.8/5.8. Tổng lỗi +39 nhưng q05_3 riêng +58, còn 14 query giảm tổng 19. Không kết luận B2 luôn kém; sensitivity không thay metric chính.
4. T2 đủ 100 box B0/B2 + 3 pseudo q05_3 và kiểm lại 14 box q05_2; một nhãn chính/box, có uncertain và bảng cộng. T3 hoàn tất sau T2 một ngày.

| Việc | Hạn nội bộ đề xuất | Điều kiện xong |
|---|---|---|
| T0 | Trước T1 | Triệu nhận và mở đủ gói |
| T1 | 30/10 | Tự chạy thật + 7 ca, log/exit code/ghi chú |
| T2 | 01/11 | Đủ nhãn, tổng cộng, bỏ sót/uncertain và minh chứng |
| T3 | 02/11 | Delta, sensitivity, quan sát/giả thuyết và đề xuất có căn cứ |
| T4 | 03/11 | Báo cáo nguồn rõ và quyết định duyệt chung |

Các hạn chưa phải cam kết Triệu đã nhận. T1–T4 khoảng 6–10 giờ, có thể song song việc Trí. Không bắt chứng minh nguyên nhân kiến trúc, chạy ablation hay đổi model để được nghiệm thu. Khi có lỗi thật, sửa đúng file/dòng và kiểm lại; không thay GT để giảm MAE. Mục tiêu P4 là **kiểm chứng hiệu quả hay không**, kể cả kết quả âm/đánh đổi.

## 4. Buổi 3 giờ tiếp theo của Trí

15 phút giao/kiểm T0 → (P4.6c đã chạy 27/10) → đọc reports/P4_6_UNSEEN_RESULTS_20261027.md → quyết định review khung N4 → bắt đầu báo cáo P5. Assistant phải hỏi trước khi chạy evaluator/model.

Cuối buổi ghi WORKLOG và mục “Dừng ở đâu” trong checklist: file sửa, lệnh cuối, output/log/lỗi, ô đầu tiên lần sau. Không ghi kế hoạch thành việc đã thực hiện.

## 5. Lịch và Git

Mốc nội bộ: 03/11 nghiệm thu sửa pilot; 08/11 runner/dữ liệu sẵn; 15/11 kết quả mới; 22/11 bản thảo; 29/11 hoàn thiện; 30/11–01/12 dự phòng; **02/12 báo cáo cuối**. Ước lượng cũ 15–24 giờ cho một vòng nhỏ không tự bao gồm mọi phần tự kiểm mới hoặc thời gian chờ/sửa theo góp ý.

HEAD/origin/main tại lần fetch 27/10 là d6db189. Tài liệu/P4/gói mới còn local, **chưa commit/push**. Không giả định máy Triệu đã có. Snapshot trước sửa giao việc: [ZIP](<quá khứ/2026-10-27_truoc_sua_giao_viec_T1_T4.zip>). Stash a34cf35 là bản phục hồi trước pull, **không apply lại**. Giữ nguyên dữ liệu/prediction/nhãn gốc và freeze.

## 6. Câu mở session mới

> Tiếp tục CS331 tại D:\MINHTRIHOCCODE\HOCKI5\CS331. Đọc AGENTS.md, BAT_DAU_SESSION_MOI.md, HANDOFF/HANDOFF.md, roadmap/CHECKLIST_3_GIO.md và mục mới nhất WORKLOG.md; kiểm Git/artifact thật. C1 đã xong: Trí chưa duyệt, Triệu cần T1–T4 V2. Nhãn p4_unseen_v1 đã xác nhận; Trí còn chốt quy tắc chấm/lịch sử sử dụng rồi khóa; kiểm dev (1)–(4) đã đạt 27/10, trùng tuyệt đối, nên sau khi khóa chạy P4.6c. Gói T0 đã chuẩn bị local, chưa gửi/push. Giữ CountGD++ và freeze, không bắt làm lại việc đã có bằng chứng. Hỏi tôi trước nếu chạy evaluator/model/thực nghiệm thay. Sau mỗi mốc cập nhật checklist, handoff, worklog; ghi đúng bước đầu tiên chưa hoàn thành.
