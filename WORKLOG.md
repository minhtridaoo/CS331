# WORKLOG CS331 — nhật ký chung

**Cập nhật 27/10/2026.** Ghi mỗi buổi tại đây; xem trạng thái tổng thể ở [ROADMAP](roadmap/ROADMAP.md). [Trang bắt đầu](README.md) · [Handoff](HANDOFF/HANDOFF.md).

**Điểm tiếp tục (29/10, tối):** V1 + V2 đã push (be4da26), chờ Trí ghép bảng tra. V3 q05_3 xong 103/103 khung, chờ commit; tiếp theo V5 rồi V4.

**Điểm tiếp tục (27/10):** đã push e877541 lên origin/main và kiểm HEAD khớp remote ngày 27/10. P4.6 count đã xong; N4 tầng A giao Triệu. Trí gửi đường dẫn giao việc, nghiệm thu phần kiểm chéo đã đạt và chốt quy tắc dữ liệu mới; chưa có quyết định chọn P/R.

## Cách dùng nhật ký

Mỗi buổi thêm một mục mới ngay trên mục ngày gần nhất. Không xóa kết luận cũ; ghi mục đính chính có ngày nếu cần. Khi hoàn thành một mốc, cập nhật dòng trạng thái trong ROADMAP và bước tiếp trong HANDOFF; không chép toàn bộ nhật ký sang đó.

```text
## YYYY-MM-DD — tên việc
Người thực hiện:
Việc/lệnh đã thực sự chạy:
Input/cấu hình hoặc run ID:
Output/bằng chứng (đường dẫn):
Kiểm tra và kết quả:
Lỗi/điểm chưa rõ:
Trạng thái: Chưa làm / Đang làm / Chờ kiểm / Đã xác nhận
Bước tiếp theo + người làm:
```

## 29/10/2026 — Triệu: V3 gán nhãn khung q05_3

**Người thực hiện:** Triệu tự gán 103/103 khung (3 mẫu pseudo + 21 B0 + 79 B2 final) trong `results/countgdpp/q05_error_analysis_package_20261027/*_labels_BLANK.csv`, từng khung một bằng app mới [evaluation/box_label_app.py](evaluation/box_label_app.py) (chỉ hiển thị và ghi cột nhãn; không gợi ý nhãn, không chạy model). Assistant hướng dẫn quy ước, kiểm nhất quán, tính bảng; điền ngày còn trống cho 3 dòng pseudo.

**Kết quả:** B0 21 = 3 target + 18 wrong_class. B2 79 = 2 target + 58 part + 19 wrong_class. B0 có target cho cả 3 quả; **B2 không có khung target cho quả b1** (chỉ 23 part), dù b1 là mẫu pseudo P1. Chi tiết: [mục V3](reports/TRIEU_TU_KIEM_PHAN2_20261027.md).

**Trạng thái:** V3 Chờ kiểm (Trí). **Bước tiếp:** Triệu commit + push; làm V5 (phân tích B2/B0, dùng V2 + V3), rồi V4.

## 28–29/10/2026 — Triệu: N4 tầng A (V1 + V2)

**Người thực hiện:** Triệu tự gán nhãn từng khung; assistant chỉ hướng dẫn, đối chiếu với ảnh crop và chuẩn hóa cột `date` (không đổi nhãn). Review mù: không mở `_KEY_mo_sau_khi_review/` và file `A_u01_1_people_labels_TRI_20261027.csv`.

**V1, gói chính** (`results/countgdpp/p4_n4_review_package_20261027/A_*_labels_*.csv`, 7 query, 78 khung): wrong_class 71, multi_object 6, uncertain 1, **target 0**. Mô hình vẽ gần như cùng các khung cho "people" và "sheep" (mcac_123), "people" và "bicycles" (mcac_88), tức là gần như bỏ qua prompt.

**V2, bổ sung** (`.../bo_sung_F0/A_*_{pseudo,e3}_labels_BLANK.csv`):
- 21 mẫu tự chọn (E1): **1/21 đúng loại** (u01_1 P2, một người); còn lại wrong_class 10, multi_object 10. Riêng 4 query people: 1/12. u07_1 P2 và u07_3 P2 gần như cùng một khung (taxi) dù prompt khác nhau.
- 18 ứng viên E3 (khung bị lọc xóa): target 13, part 3, uncertain 2. u01_1: 4/9 người thật bị xóa (GT 10); u02_1: 2/2 (mẹ bế con + người đi bộ; GT 3 nếu tính em bé); **u08_1: 7/7, bằng GT 7**, trong khi khung giữ lại toàn ô tô. u01_1 E3 #18 trùng người với mẫu pseudo P2: mô hình lấy người này làm mẫu ở lượt 1 rồi lọc mất ở lượt 2.

**Kiểm tra:** assistant đọc lại mọi CSV, đối chiếu crop; Triệu đã sửa theo góp ý (thiếu reviewer/actual_class, thống nhất multi_object chỉ khi không có vật chính). Cột `date` bị Excel đổi (`########`, `10/28/2026`, năm nhảy 2027/2028) đã chuẩn hóa về `2026-10-28`/`2026-10-29` cho dòng reviewer=Trieu, các cột khác giữ nguyên byte nội dung.

**Điểm chưa rõ:** u02_1 E3 #16 note cũ vẫn ghi "không biết xác định target", nhãn đã chốt là target p2. Chưa ghép với bảng tra/khóa, chưa tính E1–E4 chính thức; chọn P hay R vẫn là quyết định của nhóm.

**Trạng thái:** V1 + V2 Chờ kiểm (Trí). **Bước tiếp:** Triệu commit + push, báo Trí; Trí/assistant ghép bảng tra và tính E1–E4. Triệu làm tiếp V3 (q05_3).

## 27/10/2026 — đồng bộ Git theo yêu cầu Trí

**Đã thực hiện:** fetch origin, xác nhận main không lệch remote; rà 448 file và commit `e8775412f84f0927a6fe692f1f106bf53aacd369`, rồi `git push origin main` thành công. `git ls-remote --heads origin main` trả đúng cùng commit với HEAD local.

**Nội dung đã lên GitHub:** code runner/chấm P4, dữ liệu truy vấn đã khóa, kết quả dev và p4_unseen_v1, ảnh/gói N4 và q05, gói giao việc cho Triệu, báo cáo, roadmap/handoff. Dung lượng file trước nén khoảng 68,5 MiB; không file nào vượt 100 MB.

**Kiểm trước push:** phân tích cú pháp Python và JSON/JSONL đạt; kiểm ZIP CRC đạt; không tìm thấy dấu xung đột hoặc token truy cập theo mẫu đã quét. Các artifact và script được stage giữ nguyên byte. Ba hash dữ liệu LOCKED khớp selection_meta. Git whitespace chỉ còn CRLF cần bảo toàn và dấu xuống dòng Markdown có chủ ý trong tài liệu nguồn; không sửa dữ liệu đã khóa để làm đẹp kiểm định dạng.

**Giữ tại máy:** checkpoint, data_external và 7 ZIP snapshot trong `quá khứ/`. Đã thêm quy tắc bỏ qua snapshot, giữ nguyên các file. `.gitattributes` bảo toàn byte của dữ liệu/đầu ra đã khóa và adapter có hash khi clone trên Windows; không đổi freeze, GT hay dự đoán.

**Phạm vi:** chỉ đồng bộ Git và tài liệu, không chạy evaluator/self-test/inference/train, không gửi tin cho Triệu, không ký nghiệm thu thay nhóm. Gói đã có trên GitHub không có nghĩa Triệu đã nhận hoặc hoàn thành.

**Bước tiếp:** Trí gửi đường dẫn `HANDOFF/GIAO_VIEC_TRIEU_20261028.md`, đọc và nghiệm thu phần đạt của bản tự kiểm, chốt quy tắc dữ liệu v2. Triệu làm N4 tầng A V1–V2; sau đó mới chọn P/R. Bản cập nhật nhật ký/handoff này là commit tài liệu tiếp nối e877541.

## 27/10/2026 (khuya, cuối ngày) — giao N4 cho Triệu, lập việc cho Triệu, chốt vị trí pipeline

**Yêu cầu của Trí:** hôm nay không làm tiếp được, nên giao N4 cho Triệu, lập kế hoạch việc cho Triệu (gợi ý cả việc của Trí mà Triệu làm thay được), cập nhật tiến độ, nói rõ đang ở đâu trong pipeline.

**Trạng thái N4 lúc giao:**
- Trí đã chấm **u01_1, 9/9 khung**: 7 `wrong_class` dog, 2 `multi_object` dog. Hỏi "people" thì mọi khung bộ lọc giữ đều là chó. Chưa ghi reviewer/date.
- Lưu nguyên bản của Trí: `A_u01_1_people_labels_TRI_20261027.csv`, sha256 `40c800d9…`, trùng hash file gốc. Đã xóa file gốc cùng tên BLANK để không lộ nhãn khi review mù.
- Tạo `A_u01_1_people_labels_TRIEU_BLANK.csv`, để 9 khung này thành phép đo đồng ý giữa 2 người.
- 8 query còn lại và toàn bộ `bo_sung_F0/` chưa chấm.

**Đã tạo:**
- [HANDOFF/GIAO_VIEC_TRIEU_20261028.md](HANDOFF/GIAO_VIEC_TRIEU_20261028.md):
  - V1–V2: N4 tầng A, hạn 30/10, đường găng;
  - V3: q05_3; V4: 2 ca thử; V5: phân tích B2/B0 (hạn 01/11);
  - V6: N4 tầng B (02/11); V7: duyệt chung (03/11);
  - gợi ý V8–V10 làm thay Trí: kiểm absent/GT test 40 ảnh, Related Work, review test cuối;
  - 47 nhãn q03 đề xuất tạm hoãn;
  - quy tắc dự phòng: 31/10 chưa có N4 thì chọn nhánh bằng chỉ báo tự động.
- `HANDOFF/TRIEU_GIAO_VIEC_20261028.zip`: 79 file, 11,2 MB, sha256 `027042df…`, CRC đạt. **Không** có `_KEY_` và bản chấm của Trí. Thay ZIP V2 cũ chưa gửi.
- [roadmap/VI_TRI_PIPELINE_20261028.md](roadmap/VI_TRI_PIPELINE_20261028.md): sơ đồ 11 bước; hiện ở bước [5] N4; lịch việc của Trí theo tuần (khoảng 14–15 giờ tập trung đến 02/12), rủi ro và cách xử lý, lệnh commit/push.
  - Toàn bộ file cần commit khoảng 120 MB; bỏ snapshot `quá khứ/*.zip` (59,5 MB) thì còn khoảng 60 MB.

**Chưa làm:** không commit/push (Trí tự làm 28/10), không gửi tin cho Triệu, không chạy model.

**Bước tiếp theo (28/10, Trí, 45 phút):** push → gửi Triệu file giao việc → nghiệm thu bản tự kiểm → chốt quy tắc dữ liệu.

## 27/10/2026 (khuya) — pull commit Triệu 36eaf96, hợp nhất và đánh giá bản tự kiểm

**Yêu cầu của Trí:** pull Git về và xem Triệu làm ổn chưa, trong lúc Trí làm N4.

**Git:**
- Fetch thấy 1 commit mới `36eaf96` "Triệu tự kiểm chéo Phần 2 (8/8)", gồm 13 file. 5 file trùng với thay đổi local chưa commit: HANDOFF_TRIEU, WORKLOG, PILOT_SUMMARY, PHAN_2_DANH_GIA, ROADMAP.
- Snapshot trước pull: `quá khứ/2026-10-27_truoc_pull_36eaf96.zip` (448 file kèm manifest hash).
- `git stash` (f81ac9a) → `pull --ff-only` (HEAD d6db189 → 36eaf96) → `stash pop` → ghép tay 5 file xung đột, giữ cả hai phía (dòng trạng thái cũ thay bằng bản gộp).
- Kiểm bằng script: không mất dòng nào Triệu thêm; các dòng local "mất" đều là dòng trạng thái được cố ý cập nhật.
- Xóa stash tạm f81ac9a; stash cũ a34cf35 vẫn giữ. Không stage, không commit/push.
- Lưu ý: sau stash pop, một số file trong working tree chuyển sang CRLF (autocrlf của Git), nội dung không đổi.

**Kiểm bằng chứng của Triệu (chỉ đọc):**
- `pilot_eval_20261027_trieu` có metrics/per_query/manual_check giống hệt run 20/10.
- `TRIEU_TINH_TAY.xlsx` có công thức thật, 3 sheet.
- stdout self-test có PASS.
- Số độ nhạy q05_3 đúng: 273/14 và 254/14.

**Đánh giá** ([reports/DANH_GIA_TRIEU_TU_KIEM_20261027.md](reports/DANH_GIA_TRIEU_TU_KIEM_20261027.md)):
- Đạt: nhận xét 1 (tự chạy, 5 ca hỏng) và q05_2 (tự gán nhãn mù, khớp 14/14). Mức độc lập: "tự kiểm có hướng dẫn", Triệu có ghi rõ.
- Còn thiếu: q05_3 gán nhãn từng khung; 2 ca uncertain / absent > 0; bảng chênh lệch từng query, liên hệ mẫu tự chọn và đề xuất cải thiện. Khi Triệu làm, gói V2 và gói q05 chưa được push.
- Lưu ý: tập mới p4_unseen_v1 xác nhận B2 kém B0 (CI [+2.0, +12.3]), nên kết luận "tùy trường hợp" chỉ đúng cho pilot.

**Trạng thái:** Trí chưa nghiệm thu; chưa duyệt chung pilot.

**Bước tiếp theo:**
- Trí đọc đánh giá và quyết định nghiệm thu.
- Push các file local để Triệu có gói q05 + kế hoạch V2, rồi Triệu làm phần còn thiếu.
- Trí tiếp tục N4.

## 27/10/2026 — Triệu tự kiểm chéo Phần 2, xong 8/8

Người thực hiện: Triệu (tự chạy lệnh, tự tính, tự xem ảnh, tự gán nhãn); assistant hướng dẫn và chấm câu trả lời, không làm hộ.
Việc/lệnh đã thực sự chạy: `evaluate_pilot.py --self-test` trên Windows (conda ai_new); tính lại MAE/RMSE bằng Excel; đọc predictions q05_3 bằng PowerShell và xem pseudo/final; tự gán nhãn 14 box q05_2 trước khi mở nhãn cũ; 5 ca dữ liệu hỏng trên bản sao ngoài repo; chạy evaluator thật ra `pilot_eval_20261027_trieu`.
Input/cấu hình hoặc run ID: commit d6db189; m4_first5_b0, b2_two_images_20261015, b2_remaining3_20261015; manifest/first5_inputs mặc định của evaluator.
Output/bằng chứng: [tiến độ chi tiết](reports/TRIEU_TU_KIEM_PHAN2_20261027.md), [stdout self-test](reports/audits/TRIEU_SELFTEST_stdout.txt), [bảng tính + nhãn q05_2](reports/audits/TRIEU_TINH_TAY.xlsx), [run evaluator của Triệu](results/countgdpp/pilot_eval_20261027_trieu).
Kiểm tra và kết quả: self-test PASS; MAE 19.4/22, RMSE 24.316/30.091, 6/4/5 khớp; q05_3 B0=21, B2 lượt 1=21, cuối=79, tăng ở lượt 2; q05_2 loại quả khớp 14/14, 5/4/1/9 khớp manual_check; 5/5 ca hỏng được xử lý đúng (4 dừng, 1 lỗi hợp lệ được loại và báo coverage); metrics/per_query/manual_check của run mới giống hệt run 20/10.
Lỗi/điểm chưa rõ: bỏ riêng q05_3 thì MAE đảo chiều (B0 19.5, B2 18.14), kết luận B0/B2 trên 15 câu rất mong manh. Box 12/13 q05_2: nhãn cũ partial, Triệu tron (khác định nghĩa, không đổi số đếm). Vai trò box mẫu raspberry trong lỗi q05_3 mới là giả thuyết.
Trạng thái: Đã xác nhận. Kết luận nguyên văn của Triệu ghi ở PILOT_SUMMARY mục 7: đồng ý dùng số liệu Phần 2, nhưng không ghi B2 kém hơn B0 như kết luận tổng quát; đã thêm lưu ý độ nhạy q05_3 vào mục 3. Bản 24/10 giữ làm lịch sử.
Bước tiếp theo + người làm: Trí và Triệu cùng duyệt toàn bộ PILOT_SUMMARY, ghi quyết định đóng pilot và bốn mục 6C trước P4.

## 27/10/2026 (tối) — đọc đề xuất cải tiến, bổ sung N4 cho F0, lập kế hoạch thực thi

**Nguồn:** Trí chưa ưng kết quả P4.6 và đưa hai tài liệu trong `hướng cái tiển/`: đánh giá tiềm năng paper, và kế hoạch fix pipeline (nhánh P / R, F0 = N4 bắt buộc). Trí hỏi có cần làm N4 trước không.

**Trả lời:** có. N4 là F0, dùng để chọn P hay R.

**Đã làm (chỉ đọc dữ liệu đã lưu, không chạy model):**
1. Đo chỉ báo tự động E1–E4 trên 30 query p4_unseen_v1:
   - E1: 21/65 mẫu sai loại; sai số tăng +11.7 khi có mẫu sai, so với +5.8 khi mẫu đều đúng.
   - E2: có, ví dụ chairs 15 → 49 và motorbikes 33 → 80 dù mẫu đều đúng.
   - E3: 152 khung chứa điểm mục tiêu bị Fusion loại.
   - E4: 12/289 điểm không có khung nào.
2. Viết `evaluation/p4_n4_make_supplement.py`, tạo `results/countgdpp/p4_n4_review_package_20261027/bo_sung_F0/`: 27 mẫu tự chọn + 29 ứng viên E3 cho 9 query N4. Phần này không mù. Gói chính giữ nguyên.
3. Đếm ảnh MUCCA còn dùng được: 185 ảnh chưa dùng.
   - Cặp khác siêu nhóm: chỉ 19 ảnh (3–40 điểm), 26 ảnh (3–60), 34 ảnh (2–80).
   - Mọi cặp: 109 ảnh (3–40 điểm).
   - Vậy đề xuất 30 dev + 50 test buộc phải thêm cặp dễ nhầm.
4. Viết [roadmap/KE_HOACH_CAI_TIEN_20261027.md](roadmap/KE_HOACH_CAI_TIEN_20261027.md): đối chiếu đề xuất với code thật, gồm
   - runner hiện hành là run_b2_frozen;
   - evaluator mở rộng từ p4_unseen_score;
   - CLIP và CountGD++ ở hai WSL khác nhau nên nhánh P chạy 3 bước;
   - thêm đối chứng C6 = B0 + bộ lọc;
   - đề xuất dev 20 + test 40;
   - lịch W0–W5.

**Chưa làm:** chưa viết code nhánh P/R, chưa rút dữ liệu mới, chưa chạy thí nghiệm.

**Bước tiếp theo:**
- Trí làm N4 tầng A rồi báo lại; assistant ghép bảng tra, tính E1–E4 bằng nhãn người và đề xuất P hoặc R.
- Trí chốt quy tắc dữ liệu (§4 kế hoạch).
- Triệu làm T0–T4.

## 27/10/2026 — chuẩn bị N4 chọn lọc và viết tóm tắt dự án

**Người quyết định:** Trí. Trí chọn làm N4 nhưng chỉ kiểm chọn lọc, và yêu cầu một file md tóm tắt toàn bộ dự án trước khi làm báo cáo thật. Commit/push Trí tự làm.

**N4:** viết `evaluation/p4_n4_make_review_package.py` và tạo gói `results/countgdpp/p4_n4_review_package_20261027/`.
- Quy tắc chọn ca chốt trước khi xem từng khung: đây là phân tích lỗi có chủ đích, không phải mẫu ngẫu nhiên.
- Tầng A: u01_1, u02_1, u07_1, u08_1 (people) và u01_3, u07_3, u10_3 (vắng mặt bị báo > 0), tổng 78 khung.
- Tầng B: u06_2, u07_2, tổng 41 khung.
- Khung xét = hợp các khung được ít nhất một bộ lọc giữ.
- Mỗi query có ảnh tổng quan + ảnh cắt từng khung + CSV trắng. Bảng tra khung–cách lọc để riêng trong `_KEY_mo_sau_khi_review/` để review mù.
- Assistant không gán nhãn.

**Tóm tắt dự án:** [reports/TOM_TAT_DU_AN_20261027.md](reports/TOM_TAT_DU_AN_20261027.md). Gồm bài toán X/Y, CountGD++ B0/B2, pilot, cách lọc + freeze, tập mới, kết quả, cải thiện và đánh đổi, việc còn lại. Không có số liệu mới; mọi số lấy từ các báo cáo đã có.

**Bước tiếp theo:**
- Trí review N4 tầng A rồi báo lại; assistant ghép bảng tra và tính kết quả.
- Bắt đầu báo cáo P5.
- Triệu làm T0–T4.

## 27/10/2026 — P4.6c–d: chạy 3 cách trên tập mới đã khóa và chấm số đếm

**Người yêu cầu:** Trí ("chạy đủ cả 3 cách đi rồi báo cáo"). **Người chạy:** assistant. Máy local RTX A2000 4 GB; B2 khoảng 10 phút, không cần Kaggle.

**Lệnh** (log ở `reports/audits/p4_unseen_v1_run_20261027/`):
1. `run_b2_frozen.py --inputs experiments/countgdpp/p4_unseen_v1/inputs.jsonl --run-id p4_unseen_v1_b2_20261027`: 30/30 ok.
2. `p4_clip_score.py … --run-id p4_unseen_v1_clip_20261027`: 663 khung.
3. `p4_apply_freeze.py --scores results/countgdpp/p4_unseen_v1_clip_20261027 --run-id p4_unseen_v1_freeze_20261027`: freeze không đổi.
4. `evaluation/p4_unseen_score.py --run-id p4_unseen_v1_eval_20261027`: script mới. Trước khi chấm, script kiểm hash bản đã khóa và trạng thái LOCKED. GT chỉ được đọc ở bước này.

**Kết quả** ([báo cáo](reports/P4_6_UNSEEN_RESULTS_20261027.md)). MAE trên 20 query có mặt / count TB trên 10 query vắng mặt / MAE cả 30:

| Cách | MAE có mặt | Count TB vắng mặt | MAE cả 30 |
|---|---:|---:|---:|
| B0 | 5.70 | 8.9 | 6.77 |
| B2 gốc | 12.95 | 13.1 | 13.00 |
| Lọc điểm | 8.75 | 4.3 | 7.27 |
| Fusion | 7.80 | 1.0 | 5.53 |

Bootstrap theo ảnh:
- Fusion so với lọc điểm: Δ = −1.73, CI [−3.2, −0.3] → Fusion tốt hơn, ngược với CV trên dev.
- B2 gốc so với B0: +6.23, CI [+2.0, +12.3] → B2 kém B0.
- Hai bộ lọc so với B2 gốc: CI chạm 0, chưa chắc.

Chỉ số tự động điểm-trong-khung:
- Fusion có 31 khung chỉ chứa vật loại khác, lọc điểm có 92, B2 gốc 238.
- Đổi lại, các bộ lọc chỉ phủ 44–50% điểm mục tiêu.
- 3/10 query vắng mặt gần nghĩa (sheep, bicycles ×2) bị báo > 0 ở mọi cách.

**Trạng thái:** P4.6c xong; P4.6d phần count + chỉ số tự động xong. Review khung bằng người theo §4 chưa làm. Không chỉnh gì theo kết quả này.

**Bước tiếp theo:**
- Trí quyết định có review khung bằng người không (N4: số khung giữ của Fusion là 157, lọc điểm là 204).
- Bắt đầu báo cáo P5 với kết luận đánh đổi.
- Triệu vẫn làm T0–T4.

## 27/10/2026 17:08 — đổi 2 absent và KHÓA p4_unseen_v1 (P4.6a xong)

**Người quyết định:** Trí (chọn qua câu hỏi trực tiếp). **Người thực hiện:** assistant.

**Kiểm trước khi khóa:** assistant xem ảnh gốc mcac_88 và mcac_84.
- mcac_88 có 2 xe van Mercedes, 1 minibus và 1 van nhỏ, nên "trucks" còn tranh cãi.
- mcac_84 có xe bán tải thùng hở, nên "trucks" có khả năng có mặt.

Trí chọn đổi cả hai sang ứng viên kế tiếp `bicycles` (class 24, cùng siêu nhóm xe; assistant không thấy xe đạp trong cả hai ảnh). Lúc này chưa có output model nào.

**Đã sửa:** u07_3 và u10_3 trong `inputs.jsonl` (chỉ prompt), `manifest.csv` (class_id/target_class/prompt/verified_by/uncertainty_note), `absent_candidates.csv` (ghi lớp cũ và lý do). Bản trước khi sửa ở `experiments/countgdpp/p4_unseen_v1/draft_before_absent_swap_20261027/`. Định dạng file giữ nguyên; diff chỉ đúng 2 dòng mỗi file.

**Kiểm nhất quán §5.2:** PASS. 30 ID duy nhất / 10 ảnh, 20 present + 10 absent, prompt và class khớp giữa inputs/manifest/class_mapping, GT = số điểm MUCCA, absent = 0 điểm, hash 10 ảnh khớp.

**Khóa:** Trí đồng ý quy ước chấm §4 (HUONG_DAN_KIEM_DU_LIEU.md, bản 27/10). `selection_meta.json` đổi sang `status=LOCKED`, `locked_at=2026-10-27T17:07:55+07:00`, kèm `review_protocol`, `usage_history` và `post_selection_changes`.

sha256 các file đã khóa:
- inputs.jsonl `53e91e8151eee327cb058d70e522d4081e89ec02e64b074fce53e57cd69bc28b`
- manifest.csv `9161d8f44fb498e61633acdb025e2f1932e15d1300b7db669cfd7150c55daa38`
- absent_candidates.csv `2d1f5b415ee0a10515e5a320338347377b1f0673c0ed52d3e3bf1c1b1acb285f`
- selection_meta.json `69e63f94cdebdff434a4a60ae35734a7fa4776901a8247166abe8a8af4b46abe`

**Giới hạn:** chỉ một người kiểm (Trí); GT là điểm MUCCA. Không khẳng định model chưa thấy ảnh khi pretraining.

**Bước tiếp theo:** P4.6c chạy B2 (không có `--b0-reference`), CLIP và apply_freeze trên `p4_unseen_v1/inputs.jsonl`. Cần Trí cho phép trước khi chạy. Sau đó P4.6d chấm bằng manifest.

## 27/10/2026 — ghi xác nhận kiểm nhãn C2 của Trí

**Nguồn xác nhận:** Trí trực tiếp nhắn: “tôi kiểm thì thấy oki hết á bạn diền giúp tôi vs tôi thấy data của mucca làm chính xác hết á”. Assistant ghi theo xác nhận này cho bộ 10 ảnh đang kiểm; không suy rộng sang toàn MUCCA, không ghi assistant/Triệu đã kiểm độc lập.

**Đã ghi:** absent_candidates.csv đủ 10 dòng absent_ok, checked_by=Trí, date=2026-10-27; manifest.csv đủ 30 dòng verified_by/uncertainty_note (20 present, 10 absent). Evidence ở [human_review_20261027.json](experiments/countgdpp/p4_unseen_v1/human_review_20261027.json), gồm nguyên văn tin nhắn và hash trước/sau.

**Giữ nguyên:** gt_count/class_id/target_class/prompt/ID và mọi cột ngoài metadata review; inputs.jsonl, selection_meta.json, annotation nguồn, freeze và artifact kiểm dev. Sao lưu trước sửa tại `quá khứ/2026-10-27_truoc_ghi_xac_nhan_GT.zip`. Không chạy evaluator/self-test/model trong lượt này.

**Tiến độ:** phần kiểm nhãn C2 đã ghi nhận hoàn thành theo người kiểm Trí. P4.6b đã đạt ở phiên song song, đã đọc SUMMARY/run_config hiện có; không chạy lại. Dữ liệu vẫn DRAFT_NOT_LOCKED vì chưa có xác nhận riêng quy tắc chấm/lịch sử sử dụng. Nhãn được xác nhận không đồng nghĩa pilot đã được hai người duyệt.

**Bước tiếp:** chốt quy tắc chấm và lịch sử sử dụng rồi khóa, sau đó mới P4.6c (người dùng tự chạy hoặc cho phép). Đồng bộ README, handoff, checklist, roadmap, P4_TIEP_THEO và hướng dẫn; giữ nguyên các mục lịch sử.

## 27/10/2026 (tối, tiếp) — P4.6b: kiểm dev bước (2)–(4) ĐẠT

**Người chạy:** assistant, theo yêu cầu trực tiếp của Trí. Trong lúc đó Trí tự kiểm absent/GT của `p4_unseen_v1`. Ghi chèn trên mục T1–T4 V2 của phiên song song; nội dung mục đó giữ nguyên.

**Đã chạy:**
- (2) B2 trên WSL `Ubuntu-22.04` (venv countgdpp, torch 2.5.1+cu121, GPU RTX A2000): 15/15 replay khớp B0. So với hai run B2 15/10: count trùng, Δbox = Δscore = 0, pseudo trùng.
- (3) CLIP trên WSL `Ubuntu` (venv cs331-p4-clip, torch 2.9.1+cu128, transformers 4.57.1, revision 3d74acf…): 481 khung.
- (4) `p4_apply_freeze.py` với `--check-audit` và `--reference-scores`: cả hai PASS. Δclip = 0, 0 khung đổi quyết định giữ/bỏ.

Lệnh, log, hash và giới hạn ở [SUMMARY](reports/audits/devcheck_20261027/SUMMARY.md). Output: `results/countgdpp/p4_b2_devcheck_20261027/`, `p4_clip_devcheck_20261027/`, `p4_freeze_e2e_devcheck_20261027/`.

**Kết luận:** runner mới tái lập đúng pipeline dev trên cùng máy và môi trường, nên **P4.6b xong**. Đây là kiểm triển khai, không phải kết quả hiệu quả hay holdout.

**Bước tiếp theo:**
- Trí khóa `p4_unseen_v1`.
- P4.6c chạy ba lệnh trên `p4_unseen_v1/inputs.jsonl`: B2 không có `--b0-reference`, CLIP, rồi apply_freeze không có `--check-audit`.
- Sau đó P4.6d chấm bằng manifest.
- Việc của Triệu theo kế hoạch V2 (T0–T4) không đổi.

## 27/10/2026 — hướng dẫn Trí tự kiểm C2 và chuẩn bị ảnh điểm GT

**Người thực hiện:** assistant, theo yêu cầu hướng dẫn cách kiểm absent/GT/quy ước/khóa. Chỉ chuẩn bị tài liệu và hiển thị annotation nguồn; không evaluator, inference hoặc xác nhận người dùng.

**Việc thực sự đã làm:** đọc schema hiện tại, vẽ bằng Python/Pillow 10 ảnh GT (mỗi ảnh hai lớp, đánh số điểm nguồn), viết [HUONG_DAN_KIEM_DU_LIEU](experiments/countgdpp/p4_unseen_v1/HUONG_DAN_KIEM_DU_LIEU.md). Output ở `experiments/countgdpp/p4_unseen_v1/gt_review_images/`; SOURCE_MANIFEST ghi hash nguồn/output. Số chấm vẽ khớp annotation và gt_count, tọa độ trong ảnh; đây là kiểm sao chép nguồn, không xác nhận nhãn đúng bằng mắt. Đã xem thử ảnh mcac_121 để kiểm việc hiển thị.

**Làm rõ hướng dẫn:** absent thay thế phải được người xem xác nhận và đồng bộ cả class_id/target_class/prompt; giữ lịch sử lớp cũ. Sửa câu point-in-box thành chỉ là hỗ trợ ghép; đề xuất kiểm loại/cả vật/ghép một-một/trùng/uncertain, chưa được Trí chốt. Runner hiện không tự đọc status LOCKED, nên điều kiện khóa là bước cần người kiểm xác nhận và kiểm dev phải đạt trước chạy ảnh mới.

**Bảo toàn:** không sửa inputs/manifest/absent_candidates/selection_meta, ảnh/annotation nguồn hoặc freeze. Không đánh dấu review/khóa hộ; vẫn DRAFT_NOT_LOCKED. Snapshot trước sửa 5 tài liệu và hash 17 file cần giữ: `quá khứ/2026-10-27_truoc_huong_dan_C2.zip`. Đồng bộ README bộ ảnh, checklist, handoff, roadmap; bản ZIP T1–T4 cũ vẫn là snapshot bàn giao cũ, không thay nó bằng bản khác lặng lẽ.

**Điểm tiếp tục:** Trí mở hướng dẫn, tự kiểm mcac_123 và mcac_121 (2 absent + 4 present); điền đúng nhận xét/người/ngày. Còn bất đồng thì giữ PENDING/needs_review và DRAFT; sau hai ảnh tiếp tám ảnh còn lại. Chưa chạy ảnh mới. Lượt này thấy thư mục `p4_b2_devcheck_20261027/` mới xuất hiện nhưng không audit run đang/đã chạy; không kết luận C3(2) đạt chỉ vì có thư mục.

## 27/10/2026 — rà giao việc T1–T4 V2 và chuẩn bị gói bàn giao

**Người thực hiện:** assistant theo yêu cầu Trí kiểm chứng góp ý và cập nhật phân công. Đây là rà tài liệu/code/artifact và chuẩn bị bàn giao, không phải Triệu đã thực hiện T1–T4.

**Đã kiểm thực tế:**
- Fetch origin, HEAD = origin/main = `d6db18931c07671763137962f7db54bd1fc3be70`; chưa có các file mới trên main: checklist, gói q05, p4_unseen_v1 và kết quả Fusion. Giữ nguyên thay đổi local, không commit/push, không apply stash.
- Đọc evaluator: CLI luôn gọi manual_check(q05_2). Sửa hướng dẫn T1 dùng bản đủ 15 query và giữ nguyên q05_2; mỗi ca thay q01_1 từ bản sạch. Không thêm cờ bỏ qua manual, không sửa evaluator. Bổ sung tạo thư mục trước redirect, exit code, phân biệt lỗi bị từ chối đúng dự kiến với lỗi thiếu đầu vào.
- Đối chiếu JSON CV: confidence=4.6, CLIP-only=6.8, Fusion=5.8. Đối chiếu trace: B0/B2 tổng lỗi 291/330 (+39); q05_3 lỗi 18/76 (+58); 14 query khác 273/254 (−19). Đây là đọc và tính lại từ số đã lưu, không chạy evaluator hoặc inference mới.

**Cập nhật giao việc:** giữ T1–T4, thêm T0 giao nhận. Hạn đề xuất T1 30/10, T2 01/11, T3 02/11, T4 03/11; chưa xác nhận Triệu nhận hoặc đồng ý lịch. T2 có nhãn chính loại trừ nhau, object_id, uncertain, tổng 21/79 và đối chiếu 14 khung q05_2; T3 tách quan sát/giả thuyết, không yêu cầu thêm ablation. 47 nhãn q03 là việc P4 riêng. Mục tiêu P4 là kiểm chứng hiệu quả, không mặc định cải tiến phải thắng.

**Output bàn giao:** [TRIEU_T1_T4_20261027_v2.zip](HANDOFF/TRIEU_T1_T4_20261027_v2.zip), 45 file tính cả manifest, 2,168,079 byte. Bao gồm code/input/prediction/manual cần thiết, ảnh gốc pilot, overlay q05, CSV trắng, kết quả tham chiếu, hai báo cáo CV và hướng dẫn. Kiểm CRC ZIP và toàn bộ SHA-256 nội bộ đạt. Không có checkpoint hoặc dữ liệu test DRAFT của Trí, vì T1–T4 không cần.
- SHA-256 ZIP: `a7cd8bc9c4342d795b07661fe31b1f46b9270b5f0d066ce1c70161c753cd33bc`.
- Trạng thái **PREPARED_LOCAL_NOT_DELIVERED**. T0 chưa hoàn tất; không có xác nhận nhận hàng, log chạy mới hay chữ ký duyệt mới.

**Đồng bộ:** kế hoạch V2, README, BAT_DAU_SESSION_MOI, ba handoff, ROADMAP, CHECKLIST_3_GIO, hai pipeline, hướng dẫn Phần 2/3, evaluation/README và PILOT_SUMMARY; nối nhật ký này, không sửa các mục lịch sử. Snapshot trước sửa: [2026-10-27_truoc_sua_giao_viec_T1_T4.zip](<quá khứ/2026-10-27_truoc_sua_giao_viec_T1_T4.zip>), 15 tài liệu và manifest hash bảo vệ 55 file code/dữ liệu/kết quả.

**Không thực hiện trong lượt này:** evaluator/self-test/model/train, sửa dự đoán/GT/nhãn, đổi freeze, gửi tin cho Triệu hoặc ký duyệt. PASS dev (1) là kết quả lượt trước, không phải lần chạy mới này.

**Bước tiếp theo:** Trí chia sẻ ZIP; Triệu kiểm nhận T0 rồi tự chạy T1. Trí song song xác nhận absent/GT và khóa dữ liệu khi đủ điều kiện, sau đó tự chạy hoặc cho phép assistant chạy kiểm dev GPU (2)–(4). Chưa mở đánh giá ảnh mới trước khi dữ liệu khóa và kiểm dev đạt. Điểm dừng/lệnh/output còn lại nằm trong bảng §3 của checklist.

## 27/10/2026 (tối) — C1 của Trí, kiểm freeze trên dev, chọn dữ liệu B, lập kế hoạch sửa kiểm chéo

**Người quyết định:** Trí. Trí cho phép chạy kiểm freeze trên dev, chọn phương án dữ liệu B, và gửi nhận xét về bản kiểm chéo. **Người thực hiện kỹ thuật:** assistant.

**C1 (Trí):** đã đọc bản kiểm chéo 24/10, **chưa duyệt**. Bốn nhận xét được ghi nguyên văn ở [kế hoạch sửa](reports/KE_HOACH_SUA_KIEM_CHEO_20261027.md) §1 và PILOT_SUMMARY §7:
1. tự chạy evaluator và các ca lỗi;
2. phân tích q05_2/q05_3;
3. giải thích B2 kém B0 kèm đề xuất cải thiện;
4. hoàn thiện báo cáo rồi duyệt chung.

Assistant lập kế hoạch T1–T4 cho Triệu, hạn đề xuất 30/10–02/11. Assistant chỉ chuẩn bị tài liệu, không làm thay.

**Kiểm dev bước (1), đã chạy:** `python experiments/countgdpp/p4_apply_freeze.py --scores results/countgdpp/p4_clip_all15_20261020 --run-id p4_freeze_devcheck_20261027 --check-audit results/countgdpp/p4_freeze_audit_20261021.json`.
- Kết quả: `CHECK audit: PASS`, cả 15 query khớp audit 21/10 về B2_threshold và Fusion.
- Output: `results/countgdpp/p4_freeze_devcheck_20261027/`.
- Đây chỉ là kiểm triển khai trên điểm đã lưu, không phải kết quả mới.

**Dữ liệu B:**
- Tải MUCCA 1.0 từ Zenodo 19231375 (CC-BY-4.0, Ciampi et al.) về `data_external/mucca_zenodo_19231375/`. md5 zip `b182e445445dad017493ffb35803f816` khớp Zenodo; sha256 `da33e64e…`. Đã thêm `data_external/` vào .gitignore.
- Gói 10 ảnh của Triệu trùng từng byte với bản chính thức, cả ảnh lẫn annotation.
- Viết `experiments/countgdpp/p4_select_unseen.py`, quy tắc chỉ dùng annotation.
- Bản rút r1 bị loại **trước khi chạy model**, vì 10/10 cặp đều là people + xe/chó. Lưu ở `p4_unseen_v1/draft_r1_rejected/`.
- Bản rút r2: 5 tầng × 2 ảnh, seed 331, absent ưu tiên cùng siêu nhóm với Y. Kết quả: `mcac_123, 121, 109, 110, 63, 61, 88, 72, 227, 84`, tổng 30 query (20 present + 10 absent). Có contact sheet và README.
- Trạng thái **DRAFT**: Trí cần xác nhận absent (chú ý `trucks` ở mcac_88/84) và GT rồi mới khóa.

**Chuẩn bị cho Triệu:** gói nhãn trắng `results/countgdpp/q05_error_analysis_package_20261027/`, gồm overlay đánh số + CSV trắng cho 79 khung B2, 21 khung B0 và 3 pseudo của q05_3. Khung được vẽ lại từ prediction đã lưu, không chạy model.

**Đồng bộ:** PILOT_SUMMARY §7, checklist (C1, C2 nguồn/phạm vi, kiểm dev (1), bảng §3), P4_TIEP_THEO, ROADMAP, HANDOFF, HANDOFF_TRIEU, BAT_DAU_SESSION_MOI. Chưa commit/push.

**Bước tiếp theo:**
- Trí: điền `absent_candidates.csv` và kiểm GT, khóa `p4_unseen_v1`; chạy kiểm dev (2)–(4) trong WSL GPU.
- Triệu: T1–T4.
- Sau khi tập đã khóa và kiểm dev đạt: P4.6c chạy `run_b2_frozen.py` trên `p4_unseen_v1/inputs.jsonl`.

## 27/10/2026 — session mới: kiểm kê dữ liệu C2 (DRAFT) và viết code adapter C3

**Người thực hiện:** assistant, theo yêu cầu của Trí là tiếp tục từ BAT_DAU_SESSION_MOI.md. Trí chưa báo đã làm C1, nên C1 vẫn để trống. Không ký hoặc duyệt thay ai.

**Git:** `fetch origin`: không có commit mới, HEAD vẫn d6db189 = origin/main. Các thay đổi local trước đó còn nguyên. Không commit/push, không đụng stash.

**C2 (DRAFT):** đọc annotation gói MUCCA; grep toàn CS331 (trừ CountGDPlusPlus/) và hai ZIP kết quả. 5 ảnh mcac_44/58/81/171/176 chưa có trong run, review hay score nào. Chúng chỉ có trong inputs/manifest (split=dev), contact sheet và bộ query. Đếm điểm theo lớp, 4/5 ảnh có lớp ≥ 53 vật. Chưa có query absent. GT là điểm, không phải box. Đã ghi bảng và hai phương án A (5 ảnh/15 query) / B (thêm ảnh MUCCA gốc) ở [P4_TIEP_THEO §2A](roadmap/P4_TIEP_THEO.md). Chưa đếm tay, chưa chọn, chưa khóa.

**C3 (code, chưa chạy):** thêm `experiments/countgdpp/run_b2_frozen.py`, `p4_clip_score.py`, `p4_apply_freeze.py`.
- B2: bỏ B0 cố định; `--b0-reference` dùng để kiểm replay trên dev; τ = .23 cố định.
- CLIP: tham số hoá đường dẫn; pin revision 3d74acf… cho cả model và processor; ghi hash file cache.
- Freeze: kiểm SHA256 `3c4634e7…`; đếm ba cách; có `--check-audit` và `--reference-scores` (báo khung đổi quyết định giữ/bỏ).

`run_b2_pilot.py`/`run_b0_batch.py` không đổi (git diff rỗng).

**Đã chạy:** chỉ `ast.parse` ba file (đạt) và sha256 freeze (khớp audit). Không chạy evaluator, model, CLIP, self-test hay apply_freeze, vì quy tắc là hỏi Trí trước.

**Đồng bộ:** checklist (C3 code-prep đã đánh dấu kèm "chưa kiểm chạy"; bảng §3 có 4 lệnh kiểm dev), P4_TIEP_THEO §2/§2A/§3, HANDOFF, BAT_DAU_SESSION_MOI.

**Bước tiếp theo:**
1. Trí làm C1.
2. Trí chọn phương án dữ liệu A hoặc B.
3. Cho phép chạy (hoặc Trí tự chạy) kiểm dev bước (1): apply_freeze trên điểm đã lưu, CPU. Sau đó bước (2)–(4) trong WSL GPU.

Chưa có runner đạt kiểm và chưa khóa tập mới.

## 27/10/2026 — tạo file bàn giao ở thư mục gốc để chuyển session

**Theo yêu cầu Trí:** đã tạo [BAT_DAU_SESSION_MOI.md](BAT_DAU_SESSION_MOI.md), tổng hợp mục tiêu/CountGD++, trạng thái P4.5c, phần Triệu đã làm và 47 nhãn còn thiếu, phương án xử lý kiểm chưa đạt, lịch 3 giờ, deadline 02/12, mốc nội bộ và câu mở session mới. Thêm liên kết trong README/HANDOFF/ROADMAP/checklist.

**Phạm vi:** chỉ tạo/cập nhật tài liệu; không chạy evaluator/model hoặc thay số liệu. File ghi rõ bản tổng hợp tại 27/10, ưu tiên checklist/WORKLOG nếu có cập nhật sau. Chưa có bằng chứng C1–C4 hoàn thành; việc đầu tiên vẫn C1. Các file mới đang local, chưa commit/push.

## 27/10/2026 — xác nhận hạn báo cáo 02/12 và phương án kiểm chéo còn thiếu

**Người dùng xác nhận:** final báo cáo đề tài ngày 02/12; theo năm dự án là **02/12/2026**, còn 36 ngày từ 27/10. Người dùng hỏi giả định phần kiểm chéo Triệu chưa đạt, chưa cung cấp bằng chứng lỗi mới.

**Làm rõ:** phần kiểm số liệu được ủy quyền đã có và Triệu chấp nhận; không phải Triệu tự audit độc lập. Nhóm duyệt pilot và 47 nhãn P4 vẫn riêng. Chưa có lý do kết luận phần Triệu gửi sai hoặc bắt chạy lại toàn bộ. Nếu rubric đòi người thứ hai tự kiểm, cần bổ sung đúng bước đó; hiện chưa có rubric chứng minh yêu cầu này.

**Kế hoạch cập nhật:** giữ C1–C4 cho buổi 3 giờ. Mốc đề xuất 01/11 xử lý phần kiểm còn thiếu, 08/11 runner/dữ liệu sẵn, 15/11 có đánh giá bộ mới, 22/11 bản thảo, 29/11 báo cáo/demo hoàn thiện, 30/11–01/12 dự phòng. Checklist §5A thêm tiêu chí nhận nhãn và cách xử lý thiếu xác nhận, sai phép chấm thật hoặc nhãn không nhất quán. Các mốc này là đề xuất, không ghi Triệu đã nhận hoặc nhóm đã duyệt.

**Thực hiện:** đọc lại xác nhận Triệu, cập nhật CHECKLIST_3_GIO/ROADMAP/HANDOFF/README và nhật ký. Snapshot trước sửa: quá khứ/2026-10-27_truoc_chot_deadline.zip. Không chạy evaluator/model, không sửa kết quả hoặc nhãn; chưa có tiến độ C1–C4 mới. Việc tiếp của Trí vẫn C1 rồi chuẩn bị dữ liệu/runner song song phần kiểm nhãn.

## 27/10/2026 — pull phần Triệu, hợp nhất P4 local và chuẩn bị buổi 3 giờ

**Yêu cầu của Trí:** kéo phần Triệu vừa push; xác định việc tiếp, checklist/ước lượng thời gian; chỉ có 3 giờ hôm nay; lưu đủ trạng thái để session mới tiếp tục không cần lịch sử chat.

**Git đã thực hiện:** fetch rồi pull --ff-only origin main, HEAD từ 31278dd70377578accda4d126a95b14d33bcdef0 lên d6db18931c07671763137962f7db54bd1fc3be70 (27 file trong commit mới). Trước pull có 13 file tracked đang sửa và 20 file untracked: đã lưu [ZIP trước pull](<quá khứ/2026-10-27_truoc_pull.zip>) + patch/manifest, stash phần tracked ở a34cf35f5b5ce959b7f8469fe7c14afec242d263. Hợp nhất 8 xung đột tài liệu giữa P4 ngày 22 và phần Triệu ngày 21/24; giữ hai bên. Không commit/push thay người dùng; stash giữ để phục hồi, không apply lại.

**Phần Triệu đã nhận:** bản kiểm kỹ thuật được ủy quyền, trace 15 query, audit và xác nhận Triệu đã đọc/hiểu/chấp nhận ngày 24/10; q02_1 chi tiết gồm 3 JSON và 9 ảnh. [Bản tiếp nhận](reports/SYNC_TRIEU_20261027.md). Không ghi Triệu đã tự audit code. Duyệt chung pilot còn chờ; commit không có 3 CSV độc lập cho 47 nhãn q03.

**Kiểm từ file thật:** 7/7 hash nguồn khớp byte thô tại checkout Trí; audit 24/10 của checkout khác giữ ghi chú 3 byte/4 EOL. Trace đủ 15 dòng khớp ID/GT/B0/B2/sai số, MAE 19.4/22.0 và RMSE 24.315975544210986/30.090973175799196. q02_1 JSON giữ human_adjudication_complete=false, không nâng thành đã phân xử mọi nhóm. Lượt này không chạy evaluator/self-test/model/train hoặc tạo thí nghiệm mới.

**Điểm cần chuẩn bị:** run_b2_pilot.py đọc B0 tham chiếu cố định từ m4_first5_b0 và từ chối ID mới; CLIP scorer cũng gắn 15 query cũ. Cần adapter trước khi mở tập mới. Quét prediction JSONL cấp run không thấy mcac_44/58/81/171/176, nhưng toàn gói đang là dev và chưa đủ nguồn/lịch sử để nhận là holdout.

**Kế hoạch, chưa thực thi:** C1 đọc/ghi nhận pilot 15 phút; C2 dữ liệu 55; C3 adapter 75; kiểm dev nếu sẵn sàng 20; C4 bàn giao 15. Dành 15 phút cuối cho file/lệnh/lỗi/ô tiếp theo. Hết giờ thì ghi checkpoint thật, không mặc định tất cả đã hoàn thành. Ước lượng tổng còn 15–24 giờ tập trung cho vòng kiểm nhỏ + báo cáo/demo, gồm 3 giờ hôm nay; có điều kiện dữ liệu/môi trường, chưa biết deadline chính thức, không tính chờ GPU/đồng đội.

**Đồng bộ:** README, ROADMAP V4.8, HANDOFF chung/cá nhân, hướng dẫn Phần 2–3/P4, hai pipeline, PILOT_SUMMARY, evaluation README và chỉ mục archive. Tạo [CHECKLIST_3_GIO](roadmap/CHECKLIST_3_GIO.md) có bảng điểm dừng và câu mở session mới; thêm AGENTS.md chỉ dẫn session mới đọc file hiện hành, bảo toàn kết quả và tuân thủ yêu cầu hỏi trước khi chạy thực nghiệm. Giữ các mục WORKLOG cũ của cả Trí/Triệu, ngày lịch sử không đổi.

**Kiểm sau hợp nhất:** HEAD khớp origin/main ở d6db189, không còn unmerged hoặc file staged; git diff --check đạt. 55 artifact P4 giữ nguyên hash; 19 file mới nhận từ commit Triệu không bị sửa; 19/20 file untracked cũ giữ nguyên (chỉ cập nhật hướng dẫn P4_TIEP_THEO). Các mục lịch sử 21/24 từ remote, 22 local và toàn bộ mục 20/10 trở về trước được giữ nguyên nội dung. 17 tài liệu/194 liên kết local đã kiểm, không có link hỏng hoặc conflict marker.

**Trạng thái tiếp tục:** C0 đồng bộ đã xong; C1–C4 của Trí chưa được báo làm. Việc đầu tiên là C1; nếu chờ duyệt nhóm, chuẩn bị C2/C3 song song. 47 nhãn P4, dữ liệu mới, runner đạt kiểm và đánh giá holdout đều chưa hoàn tất.

## 24/10/2026 — Triệu xác nhận đã đọc và chấp nhận bản kiểm được ủy quyền

**Người xác nhận:** Triệu, trực tiếp trong cuộc trò chuyện ngày 24/10/2026.

> Tôi đã đọc và hiểu bản kiểm ngày 24/10, đồng ý dùng kết quả kiểm kỹ thuật do assistant thực hiện.

**Phạm vi được xác nhận:** đọc/hiểu và đồng ý dùng [bản kiểm kỹ thuật ngày 24/10](reports/TRIEU_KET_QUA_KIEM_CHEO_20261024.md). Người thực hiện đối chiếu kỹ thuật vẫn là assistant; không nâng thành Triệu đã tự audit code hoặc dữ liệu nguồn. [Bản ghi xác nhận](reports/audits/TRIEU_ACCEPTANCE_20261024.json).

**Đã cập nhật:** PILOT_SUMMARY mục 1/3/7, ROADMAP, HANDOFF chung/cá nhân và phần tiếp tục của bản kiểm. Giữ nguyên bản audit kỹ thuật trước xác nhận và nhật ký cũ như lịch sử.

**Trạng thái:** Triệu đã chấp nhận kết quả kiểm được ủy quyền. Nhóm chưa duyệt toàn báo cáo, chưa quyết định đóng pilot hoặc chọn phương pháp P4.

**Bước tiếp theo:** Triệu cùng Trí duyệt PILOT_SUMMARY; Trí đồng bộ log/cấu hình với artifact P4 đã có. Lượt này chỉ cập nhật tài liệu, không chạy evaluator/model, không gửi tin nhắn, commit hoặc push GitHub.

## 24/10/2026 — làm hộ phần kiểm chéo kỹ thuật khi Triệu ưu tiên deadline paper

**Người thực hiện:** assistant theo yêu cầu trực tiếp của Triệu. Không ghi Triệu đã tự đọc/xác nhận hoặc nhóm đã duyệt.

**Việc thực sự chạy:** PowerShell đối chiếu các file pilot đã lưu, tính độc lập sai số 15 query, so kết quả evaluator và nhãn q05_2; đọc logic xử lý error/null/uncertain/absent. Không import/chạy evaluator/self-test/model/CLIP/train, không tạo run inference hoặc metric nghiên cứu mới.

**Nguồn:** checkout commit `31278dd`; 7 hash checkout nguồn không đổi so với 21/10. Hash đối chiếu run: 3 byte thô khớp, 4 khác CRLF/LF nhưng nội dung khớp.

**Kết quả:** 15/15 ID và per_query khớp, paired=15, error=uncertain=absent=0. MAE B0=291/15=19.4, B2=330/15=22; RMSE=sqrt(8869/15) và sqrt(13582/15), exact=1 mỗi nhánh; tốt/kém/giữ=6/4/5. q05_2 khớp 14 box/5 target box/4 vật/1 dư/9 sai loại. Bốn ca minh họa và nhánh null đã kiểm; không gọi đọc code nhánh giả định là test động.

**Bằng chứng:** [báo cáo đọc nhanh](reports/TRIEU_KET_QUA_KIEM_CHEO_20261024.md), [audit JSON](reports/audits/TRIEU_EVALUATOR_20261024.json), [trace đủ 15 dòng](reports/audits/PER_QUERY_TRACE_20261024.csv).

**Trạng thái:** phần kỹ thuật được ủy quyền đã hoàn thành bởi assistant; xác nhận cá nhân Triệu/duyệt nhóm vẫn chưa có. Triệu có thể ưu tiên deadline paper, khi quay lại đọc bản kết quả thay vì tự tạo lại toàn bộ audit. Trí có thể chuẩn bị/đồng bộ log P4 song song; chưa xác nhận P4 hiệu quả. Chưa commit/push hoặc gửi tin nhắn cho Trí.

## 22/10/2026 — kiểm handoff P4, đồng bộ tiến độ và chốt việc Trí làm tiếp

**Nguồn:** Trí gửi [HANDOFF_CS331_PILOT_TO_P4_2026-10-22.md](<workspace Trí and Triệu/Trí/HANDOFF_CS331_PILOT_TO_P4_2026-10-22.md>), cho biết đã hoàn thành pilot summary và Triệu chưa kiểm chéo được. Handoff tổng hợp lịch sử ngày 20–21/10; ngày 22/10 là ngày tiếp nhận/audit, không đổi ngày chạy.

**Đã kiểm tại workspace:** có CLIP score 15 query/481 khung, CV theo ảnh gốc, diagnostic, Fusion, ZIP nhãn và freeze/audit. Hash 16 nguồn freeze, 17 nguồn CV, 2 prediction CLIP, input và freeze đều khớp. ID/rank/box/điểm B2/crop khớp nguồn. Kiểm các ngưỡng đã lưu và phép tính đủ 15 query; fold không trùng ảnh và min/max Fusion chỉ từ training fold. ZIP không lỗi, 3 bảng nhãn trắng 13/18/16 dòng. [Báo cáo audit](reports/P4_AUDIT_20261022.md).

**Phạm vi thực hiện của assistant:** đọc file/code, kiểm hash và số học từ điểm đã lưu; không chạy script evaluator hiện hữu, self-test, model, train hoặc tìm lại ngưỡng tối ưu. Không xem/đánh lại nhãn thị giác để thay kiểm độc lập của Triệu. Một lệnh audit ban đầu dừng vì tên khóa `train_queries` khác schema thực tế `training_queries`; đã sửa phép đọc và kiểm hoàn tất, không thay artifact thực nghiệm.

**Kết quả P4 dev CV:** B2 gốc MAE 22.0, RMSE 30.090973; lọc điểm B2 MAE 4.6, RMSE 6.618157; CLIP-only MAE 6.8, RMSE 8.846845; Fusion 50/50 MAE 5.8, RMSE 7.793159. Fusion chưa tốt hơn đối chứng về count. Review 4 query theo nhãn hiện tại: B2 lọc điểm giữ 12/22 vật đúng, Fusion 16/22; q03 vẫn là nhãn assistant sơ bộ. Kiểm được phép tính, chưa xác nhận đúng/sai từng nhãn độc lập.

**Freeze:** B2 threshold 0.9067394733428955; Fusion threshold 0.6551826746408328, min/max cố định từ dev. Dev-fit MAE 4.333333/4.4 khác CV, không phải kết quả test. CLIP run_config có revision 3d74acf9a28c67741b2f4f2ea7635f0aaf6f0268. Chưa có bằng chứng đã pin đầy đủ/check hash trọng số trong runner ảnh mới hoặc tái lập ảnh → score; freeze audit chỉ kiểm từ score lưu.

**Đánh giá phần Trí:** phần chạy/chấm/nội dung tổng kết pilot đã đủ để chờ duyệt; không yêu cầu P4.6 để đóng PILOT_SUMMARY. P4 đã thực nghiệm đến P4.5c, vượt trạng thái tài liệu cũ “chưa chạy CLIP”. CountGD++ vẫn là model đếm; CLIP phụ trợ không phải CLIP-Count. Pilot còn Triệu kiểm evaluator và nhóm duyệt; P4 còn kiểm 47 nhãn và kiểm trên ảnh mới. Chưa ký hoặc nhận thay việc của Triệu.

**Kế hoạch tiếp theo:** giữ đối chứng lọc điểm B2 và ứng viên Fusion, dừng tuning 5 ảnh cũ. Trí làm P4.6a kiểm kê nguồn/GT/lịch sử/split ảnh mới, đề xuất 10 ảnh/30 query khi đủ dữ liệu; rồi P4.6b chuẩn bị runner đọc freeze không GT. Triệu khi có thể kiểm evaluator và 3 bảng nhãn độc lập. P4.6c–d chạy/chấm tập mới chưa làm. Hướng dẫn và checklist tại [P4_TIEP_THEO](roadmap/P4_TIEP_THEO.md); không đổi model hoặc train thêm trong kế hoạch này.

**Đồng bộ tài liệu:** README, ROADMAP V4.7, handoff chung/cá nhân, hướng dẫn Phần 2–3, hai pipeline, PILOT_SUMMARY, báo cáo P4 và evaluation README. Tạo audit và hướng dẫn P4 tiếp theo; giữ nguyên các mục WORKLOG cũ. [Snapshot trước sửa](<quá khứ/2026-10-22_truoc_dong_bo_P4.zip>) gồm 14 tài liệu, handoff đầu vào và manifest bảo toàn 55 artifact. Không di chuyển dữ liệu/code/checkpoint/results.

**Kiểm sau cập nhật:** 16 tài liệu đã kiểm, 180 liên kết local hợp lệ; ZIP snapshot không lỗi; cả 55 artifact được theo dõi giữ nguyên hash; toàn bộ mục WORKLOG trước ngày 22/10 được bảo toàn. Không đổi handoff đầu vào, code thí nghiệm, điểm số hoặc dự đoán gốc.

**Trạng thái:** artifact P4 nhất quán; pilot chờ kiểm chéo/duyệt, nhãn P4 chờ kiểm, dữ liệu mới/runner/đánh giá độc lập chưa thực hiện. Lượt này không chạy thêm thực nghiệm; assistant vẫn hỏi trước nếu chạy evaluator/model/thực nghiệm thay.

## 21/10/2026 — hỗ trợ Triệu kiểm chéo evaluator theo worklog

**Người thực hiện phần đối chiếu:** assistant theo yêu cầu Triệu đọc repo và làm theo worklog. Nguồn repo tại commit `31278dd`; đây không phải chữ ký xác nhận người kiểm của Triệu hoặc duyệt của nhóm.

**Đã kiểm:** đọc `indexed` → `validate_prediction` → `evaluate` → `manual_check`; đối chiếu 15 cặp image_id/query_id giữa input, manifest, B0/B2, per_query và metric đã lưu. Manifest có 30 dòng, input chọn 15, B2 ghép 6+9. Kết quả khớp: B0 MAE 19.4/RMSE 24.315975544210986; B2 22.0/30.090973175799196; exact 1 mỗi bên; thay đổi 6 tốt hơn/4 kém hơn/5 giữ nguyên; absent 0 và metric absent null. q05_2 đủ 14 index/tọa độ, gồm 5 box mục tiêu trên 4 vật + 9 sai loại, 1 box dư do trùng. Bốn file kết quả `_r2` giống run chính.

**Hash trên checkout Windows:** 3/7 nguồn khớp byte thô, 4/7 khớp sau đối chiếu CRLF→LF, không còn khác biệt nội dung chưa giải thích. Không ghi là 7/7 khớp byte thô của checkout này; giữ hash cả hai dạng trong [audit JSON](reports/audits/TRIEU_EVALUATOR_20261021.json). Không sửa nguồn để ép hash.

**Artifact bổ sung:** đã đưa bản chi tiết q02_1, ba JSON và chín ảnh bằng chứng từ kết quả ngày 19/10 của cuộc trò chuyện Triệu vào `workspace Trí and Triệu/Triệu/`. Hash bản sao khớp nguồn. Giữ mức chắc chắn vừa cho các nhóm mép đĩa sát nhau; không nâng thành nhãn bbox được Triệu xác nhận toàn bộ. Không thay review gốc hoặc raw prediction.

**Điểm tài liệu mới:** repo có `p4_clip_all15_20261020/run_config.json` và score, `p4_count_cv_20261020/report.json`, cùng review hai case P4. Vì vậy các câu “chưa chạy/chưa có CLIP” ở mục ngày 20/10 là trạng thái tài liệu lúc đó, không đại diện đầy đủ artifact đang có. Lượt này chỉ đọc metadata, chưa audit kết quả P4, không tự xác nhận nhóm đã duyệt.

**Phạm vi thực thi:** chỉ đọc/đối chiếu số học các file đã lưu và chuẩn bị tài liệu. Không import/chạy evaluator, không chạy self-test/inference/CLIP/train; PASS self-test vẫn theo Minhtri báo trước đó. Không tạo run metric nghiên cứu mới.

**Trạng thái:** phần hỗ trợ kiểm chéo đã có [hướng dẫn và bằng chứng](reports/TRIEU_EVALUATOR_CROSSCHECK_20261021.md); Triệu cần tự đọc và ghi kết luận ở PILOT_SUMMARY §7. Nhóm duyệt/đóng pilot/P4 còn để riêng. Chưa commit/push các thay đổi của lượt này.

**Bước tiếp theo:** Triệu đọc bốn điểm code và bốn ca minh họa trong bản hỗ trợ, xác nhận hiểu error/null/uncertain/absent và q05_2; sau đó điền tên/ngày/kết luận. Trí đồng bộ log P4 với artifact đã có; cả nhóm duyệt báo cáo. Không yêu cầu review lại 15 ảnh hoặc chạy model để làm bước này.

## 20/10/2026 — xác nhận Phần 2 đã chạy, Phần 3 chờ duyệt, chuẩn bị P4

**Nguồn mới:** Minhtri gửi `C:/Users/ADMIN/Downloads/HANDOFF_CS331_P2_P3_2026-10-20.md`. Bản gốc đã lưu nguyên trạng trong [ZIP snapshot](<quá khứ/2026-10-20_truoc_xac_nhan_P2_P3.zip>), thư mục `incoming/`. Handoff là ghi nhận cuộc trao đổi khác; trạng thái hiện tại được kiểm lại trên file workspace.

**Người chạy:** Minhtri. Lệnh thực tế theo handoff: `python3 evaluation/evaluate_pilot.py --self-test` (người chạy báo PASS, không có stdout riêng), sau đó `python3 evaluation/evaluate_pilot.py --out results/countgdpp/pilot_eval_20261020`. Dùng Python 3 hệ thống trong Ubuntu vì lệnh python/activate trong distro đang mở không có; evaluator chỉ dùng thư viện chuẩn, không cần khôi phục/cài lại môi trường model để làm phần này.

**Bằng chứng kiểm trực tiếp:** cả `pilot_eval_20261020` và `pilot_eval_20261020_r2` có đủ 5 file. Bốn file kết quả ở hai run giống hệt, metadata cùng 7 hash nguồn, chỉ command khác output. Assistant đọc code và đối chiếu độc lập 15 dòng với input/manifest/prediction gốc, kiểm MAE/RMSE/exact/error_change và q05_2; không import/chạy lại evaluator hay inference. Run đầu là nguồn chính, _r2 là lịch sử chấm lại cùng dự đoán, không tính thành mẫu độc lập.

**Kết quả:** 15 query/5 ảnh, B0/B2 đều 15 hợp lệ, 0 error/uncertain, paired=15. B0 MAE=19.4, RMSE=24.315975544210986; B2 MAE=22.0, RMSE=30.090973175799196; exact=1 mỗi bên; cải thiện/kém đi/giữ nguyên=6/4/5. Absent=0 và metric absent=null. Manual q05_2: 14 khung, 5 khung mục tiêu, 4 vật mục tiêu phân biệt, 1 dư, 9 sai loại. Khớp nguồn lịch sử, không phải kết quả inference mới.

**Phần 3:** PILOT_SUMMARY đã có thông tin run và mục 6 CLIP, mới hơn trạng thái chưa xác nhận mục 6 trong handoff gửi kèm. Giữ trạng thái CHỜ KIỂM CHÉO VÀ DUYỆT; bổ sung phạm vi audit, nguồn xác nhận self-test và phiếu xác nhận nhóm tại mục 7. Không tự ghi Triệu đã kiểm evaluator hoặc nhóm đã đồng ý CLIP.

**Rà kế hoạch P4:** kiểm tài liệu gốc CLIP (Radford et al., ICML 2021); phù hợp làm cơ sở ảnh–văn bản, chưa chứng minh hiệu quả lọc crop B2 trên CS331. Đề xuất bản tối thiểu chỉ crop+query, không chọn negative labels bằng GT test. Giữ B2 và đối chứng confidence; đo giữ vật đúng/loại khung sai cùng MAE. Chốt checkpoint/crop/prompt/ngưỡng trên dev, nhãn và phân công trước thực thi; không coi ứng viên là đóng góp mới đã chứng minh.

**Đồng bộ:** README, ROADMAP V4.6, HANDOFF chung/cá nhân, hướng dẫn Phần 2–3 và hai pipeline. Bản trước sửa và handoff gửi vào được lưu ZIP có manifest; code, dữ liệu và output run giữ nguyên. Các trạng thái “chưa chạy” trong mục nhật ký phía dưới là lịch sử trước khi nhận handoff mới này.

**Kiểm sau cập nhật:** 14 tài liệu Markdown hiện hành, 149 liên kết local hợp lệ; 18 artifact nguồn/output/code/review giữ nguyên hash; handoff gửi vào và các mục WORKLOG trước đó được bảo toàn. Không chạy thêm self-test, evaluator hoặc model.

**Việc tiếp theo:** Triệu kiểm evaluator theo Phần 2 mục 3 rồi ghi tên/ngày/kết luận ở PILOT_SUMMARY §7; Trí đọc và chuẩn bị bốn lựa chọn P4 §6C; cả nhóm duyệt báo cáo và quyết định đóng pilot để chuẩn bị P4. Chưa thực thi CLIP, E3, train hoặc holdout. Assistant vẫn hỏi trước nếu chạy evaluator/model/thực nghiệm thay người dùng.

## 20/10/2026 — kiểm benchmark đã chạy và làm rõ workspace

**Trí cung cấp:** gói `workspace Trí and Triệu/Trí/countgdpp_paper_results`. Run `full_20261015T080230Z` ghi ngày 15/10 trong log; ngày 20/10 là ngày tiếp nhận/kiểm tại workspace, không đổi ngày chạy gốc.

**Assistant đã làm:** đọc log/config/artifact, đối chiếu 1.190 tên ảnh duy nhất với annotation, kiểm GT đếm theo point labels và tính kiểm tra số học từ log. MAE **8.336974789915967**, RMSE **24.63762579961829** khớp metrics.json và tổng cuối log. Không thiếu/thừa/trùng ảnh. Cấu hình có text + synthetic + 3 pseudo + adaptive crop; ngưỡng .23. [Báo cáo đầy đủ](reports/BENCHMARK_FSCD147.md).

**Đối chiếu review mới:** file gốc Triệu hiện ghi “ĐÃ CHỐT v1 — 19/10”, đủ 15/15 query. Guitar và q04_2 đã giải quyết, không còn là đầu việc phải review lại. Handoff cũ 14/15 được sửa theo bản nguồn hiện hành. q04_2 final = 24 blueberry + 7 blackberry + 1 red currant = 32. Review q02_1 dẫn tới Q02_1_DETAILED_REVIEW.md nhưng artifact này chưa có local; giữ giới hạn nếu dùng chi tiết ghép box. SHA256 bản review đọc ngày 20/10: `ab5c4980daae03766f0b43477a4dac72d46de7e605b149a8f0244bad912dfe69`.

**Giới hạn đã ghi:** chỉ xác nhận count metrics, chưa xác nhận AP/AP50. Root run_config còn trạng thái lúc chuẩn bị; trạng thái hoàn tất ở run_config trong full_*. Info báo working tree chưa commit, gói chưa lưu diff; không tuyên bố tái lập chính xác mọi file/môi trường. Không gọi chênh lệch nhỏ với paper là phương pháp cải tiến.

**Tài liệu đã tổ chức:** README thành trang bắt đầu (giải thích pilot/benchmark, bốn chặng, bản đồ thư mục); ROADMAP V4.5 là bảng tiến độ; HANDOFF/owner handoffs/pipelines đồng bộ. Hướng dẫn phần 2–3 và bản nháp pilot nói rõ phạm vi. “Quá khứ” có index giải thích; 14 tài liệu trước sửa được lưu ZIP có hash, không chuyển code/data/checkpoint. Lịch sử cũ trong WORKLOG giữ bên dưới và thu gọn khi xem Markdown.

**Chưa thực hiện:** self-test/evaluator pilot mới, inference mới, train, cải tiến hoặc holdout. Không có output pilot_eval trong kết quả local khi kiểm. Việc đọc/tính kiểm tra artifact benchmark đã được yêu cầu; chưa tự chạy script phần 2 thay người dùng.

**Kiểm tài liệu sau sửa:** 14 file Markdown hiện hành, 141 liên kết local hợp lệ; 30 artifact được kiểm hash giữ nguyên; 6 code cell notebook không đổi; lịch sử WORKLOG giữ nguyên. Liên kết tới file chi tiết q02_1 còn thiếu nằm trong review nguồn đã được ghi rõ, không tự tạo bằng chứng thay thế.

**Trạng thái:** benchmark chạy đủ và count metrics đã xác nhận; phần 2 đã chuẩn bị; phần 3 còn nháp.

**Bước tiếp theo:** Trí chạy `python evaluation/evaluate_pilot.py --self-test`; PASS mới chạy `python evaluation/evaluate_pilot.py --out results/countgdpp/pilot_eval_20261020`. Triệu kiểm code/ID/evaluator; review định tính đã chốt 15/15. Cả hai điền báo cáo phần 3. Theo yêu cầu ngày 19/10, assistant muốn chạy evaluator/thực nghiệm thay phải hỏi trước.

## 19/10/2026 — sắp xếp tài liệu và chuẩn bị phần 2–3

Theo yêu cầu người dùng, tạo README ở gốc, work log chính này, roadmap hiện hành, hướng dẫn phần 2/phần 3, evaluator Python có chú thích và bản nháp tổng kết. Đưa 40 tài liệu/bản trước chỉnh sửa vào “quá khứ/2026-10-19”, lưu manifest nguồn/đích/SHA256; giữ các artifact model/data tại chỗ. Các liên kết local được cập nhật theo vị trí mới.

Evaluator mới chỉ được kiểm cú pháp; **chưa chạy self-test hoặc đánh giá dữ liệu**, không tạo metric mới. Bản tổng kết dùng số liệu đã có đến 16/10, không tự ghi phần 2–3 hoàn thành. Người dùng tự chạy 2B/2C rồi điền phần 3; assistant muốn thực thi đánh giá/thực nghiệm thay phải hỏi trước theo yêu cầu ngày 19/10. Chuẩn bị code/tài liệu không phải chạy thí nghiệm.

Bước ngay tiếp: mở roadmap/PHAN_2_DANH_GIA.md, đọc luồng code, chạy --self-test; khi PASS mới đánh giá thật. Đừng sửa raw predictions để khớp số mong đợi. Nhánh Kaggle vẫn được giữ riêng.

<details>
<summary>Lịch sử trước 19/10 — bấm mở khi cần tra, không dùng làm trạng thái hiện tại</summary>

## Lịch sử trước khi tổ chức lại ngày 19/10

Các mục dưới đây giữ nội dung lịch sử; trạng thái cũ không thay thế bảng hiện hành ở đầu file. Liên kết đã được chỉnh theo cấu trúc thư mục mới.

# CS331 — Nhật ký công việc

**Cập nhật: 15/10/2026 (Asia/Bangkok).**
[Handoff hiện hành](HANDOFF/HANDOFF.md) · [Pipeline phân công](roadmap/PIPELINE_PHAN_CONG.md) · [Pipeline thực nghiệm](roadmap/PIPELINE_COUNTGDPP.md)

## Quy tắc lưu tiến độ

Theo yêu cầu của người dùng: sau mỗi mốc có bằng chứng, nối thêm mục vào nhật ký này và đồng bộ handoff, pipeline, bước tiếp theo. Giữ lịch sử; không đổi kế hoạch thành kết quả đã thực hiện. Phân biệt log người dùng gửi, file kiểm tra trực tiếp và giả thuyết. Không tự ghi Triệu đã hoàn thành hoặc đã được gửi file. Quy tắc áp dụng khi làm việc trong cuộc trò chuyện; không phải tác vụ theo dõi nền.

## Các mốc đến ngày 13/10/2026

Các mốc dưới đây được tổng hợp từ cuộc trò chuyện và kiểm tra workspace; không có giờ thực hiện đầy đủ nên không gán giờ giả.

| Mốc | Đã thực hiện và bằng chứng | Phần còn lại |
|---|---|---|
| Chốt phạm vi | CountGD++ là baseline; cùng ảnh hỏi X/Y và lớp vắng mặt; bạn làm model, Triệu làm dữ liệu/evaluator | Chưa chọn can thiệp hoặc train |
| M0 — môi trường | Clone commit 8489f836d75eb407ae778c56cff1f72cc6f8baae; WSL Ubuntu-22.04, Python 3.10.12, torch 2.5.1+cu121, torchvision 0.20.1+cu121, GCC 11, nvcc 12.1.105 | Lỗi cài torch ban đầu đã vượt qua khi dùng đúng môi trường WSL |
| M1 — thư viện | transformers 4.44.2; GPU True; MultiScaleDeformableAttention và detectron2._C import được sau import torch; inference thật đã chạy | Chưa lưu/đối chiếu log đầy đủ của bộ test CUDA ops; import và inference không thay thế mọi test |
| M2 — trọng số | BERT local có config/tokenizer/model.safetensors; CountGD++ checkpoint 1,250,122,586 byte; script nạp và chạy ra output | Chưa ghi SHA256 vào metadata; chưa kiểm missing/unexpected keys của strict=False |
| M3 — một ảnh | Đã chuẩn bị utensils.jpg và ba prompt spoon/fork/cat; đã có một kết quả thật spoon | Còn fork/cat, chuẩn hóa schema v1 và metadata trước bàn giao |

Snapshot môi trường: [environment_countgdpp.txt](environment_countgdpp.txt).

## Run đầu tiên — spoon, 13/10/2026

- Người dùng thực thi process_folder.py và gửi log hoàn tất; đã kiểm tra file đầu ra trực tiếp.
- Ảnh: [utensils.jpg](experiments/countgdpp/smoke_inputs/images/utensils.jpg), lấy từ ảnh demo trong checkout upstream. Đây là smoke test kỹ thuật, không phải pilot/holdout độc lập.
- Prompt: [spoon.json](experiments/countgdpp/smoke_inputs/spoon.json); positive text spoon, exemplar boxes rỗng, negative rỗng; ảnh exemplar trỏ chính ảnh đầu vào.
- Cấu hình: B0 một lượt qua script gốc; conf_thresh=0.23; có lưu overlay. Chưa chạy B2.
- [Kết quả gốc](results/countgdpp/smoke_spoon/results.json): count=19, 19 boxes, 19 scores.
- [Overlay](results/countgdpp/smoke_spoon/utensils.jpg): quan sát thấy lấy cả nĩa và khung trùng trên một muỗng.
- Đếm thủ công ảnh: 7 muỗng, 7 nĩa, 0 mèo. Đây là nhãn kiểm bằng mắt, chưa phải manifest đã được hai người kiểm chéo.
- Log TRAIN/FutureWarning không làm dừng run và không tự chứng minh cần fine-tune.
- RTX A2000 Laptop 4 GB chạy được cấu hình smoke này. Chưa đo peak VRAM/thời gian; không suy rộng sang toàn bộ B2/benchmark.
- Chưa xác định nguyên nhân lỗi: cần giữ cấu hình, chạy hai prompt còn lại, kiểm prompt, tải trọng số và logic lọc trước khi kết luận lỗi mô hình.

## Hướng dẫn tại mốc spoon — đã thực hiện ở cập nhật bên dưới

Chạy trong Ubuntu WSL, lần lượt từng lệnh; nếu crash thì lưu log, không ghi count=0.

~~~bash
source /root/.venvs/countgdpp/bin/activate
cd /mnt/d/MINHTRIHOCCODE/HOCKI5/CS331/CountGDPlusPlus
python process_folder.py --input_folder ../experiments/countgdpp/smoke_inputs/images --prompts ../experiments/countgdpp/smoke_inputs/fork.json --output_folder ../results/countgdpp/smoke_fork --conf_thresh 0.23 --vis_output
python process_folder.py --input_folder ../experiments/countgdpp/smoke_inputs/images --prompts ../experiments/countgdpp/smoke_inputs/cat.json --output_folder ../results/countgdpp/smoke_cat --conf_thresh 0.23 --vis_output
~~~

Giữ ảnh, checkpoint, ngưỡng và tiền xử lý; chỉ đổi prompt và thư mục kết quả. Mục tiêu tham chiếu thủ công: fork=7, cat=0. Không đoán dự đoán trước khi chạy.

Sau hai run: so cả count và vị trí; kiểm đường tải checkpoint/prompt/lọc; chuyển kết quả gốc sang predictions.jsonl + run_config.json theo schema v1. Thời gian/VRAM của run cũ chưa đo phải để null kèm lý do; muốn có số đo thì chạy lại với bộ đo được ghi rõ. Chưa chuyển sang pilot hoặc chỉnh ngưỡng chỉ vì script đã chạy xong.

Triệu tiếp tục T1–T4 trên CPU: 5 ảnh/15 query, manifest tách GT, evaluator và fixture giả. Chưa xác nhận nhánh này đã có sản phẩm. Bạn chưa xong toàn bộ phần việc; mốc gần nhất là hoàn thành bộ bàn giao M3 rồi ghép G1.


## Cập nhật sau fork/cat — 13/10/2026, trạng thái mới nhất

Người dùng báo chạy xong; đã đọc trực tiếp ba results.json và xem overlay fork/cat. Không dùng số liệu từ demo tương tác mô phỏng.

| Query | GT thủ công | Dự đoán | Quan sát |
|---|---:|---:|---|
| spoon | 7 | 19 | Lần kiểm trước thấy khung nhầm nĩa và khung trùng |
| fork | 7 | 14 | Overlay khoanh cả 7 nĩa và 7 muỗng |
| cat | 0 | 0 | Không có khung, đúng trên ảnh này |

Đã kiểm: mỗi JSON đúng một ảnh, count bằng số boxes/scores; giá trị hữu hạn, tọa độ có thứ tự, score trong [0,1]; prompt đúng spoon/fork/cat, exemplar boxes và negative rỗng; có đủ overlay. [Báo cáo kiểm chứng và hash output/prompt](results/countgdpp/smoke_verification_2026-10-13.json).

Kết luận đúng mức: hoàn thành inference smoke 3/3 query. Mô hình không trả cùng kết quả cho mọi query; truy vấn cat đúng nhưng fork vẫn lấy nhầm muỗng. Một ảnh chưa đủ kết luận đã giải quyết lớp vắng mặt hoặc xác định nguyên nhân lỗi X/Y; muỗng/nĩa cũng là hai loại đồ dùng có hình dạng tương tự nên cần pilot có hai loại khác hẳn nhau theo yêu cầu thầy.

**Bước tiếp theo:** giữ nguyên các output; audit missing/unexpected keys khi nạp checkpoint và logic lọc điểm; chuẩn hóa predictions.jsonl/run_config.json để ghép evaluator. Hash checkpoint, thời gian và peak VRAM chưa hoàn tất; không bịa số cho run cũ. Chưa đổi ngưỡng, train hoặc mở B2. M3/P0 và G1 chưa đóng chỉ vì đã có đủ ba JSON. Triệu tiếp tục T1–T4; chưa xác nhận tiến độ của Triệu.


## 14/10/2026 — tiếp nhận dữ liệu Triệu, chuẩn bị M4

- Người dùng chỉ đường dẫn workspace Trí and Triệu/Triệu/MUCCA_10_queries/MUCCA_10_queries. Đã kiểm trực tiếp 10 ảnh và 30 query/GT, IDs duy nhất, mapping khớp, số điểm theo class bằng toàn bộ GT, không có tọa độ điểm ngoài ảnh. Đã xem ảnh tổng quan; chưa đếm tay mọi ảnh.
- Tất cả query có đối tượng (GT>0); chưa có absent query. Không tính FPR_absent hoặc tuyên bố đủ protocol X/Y/absent. Cần thêm absent đã xác minh và nguồn dữ liệu; giữ nhóm gần nhau/khác hẳn nhau để phân tích riêng.
- Đã xuất input schema v1 không GT và manifest evaluator riêng trong experiments/countgdpp/m4_inputs/. Chọn batch 5 ảnh đầu theo thứ tự nguồn trước khi xem dự đoán; ảnh đầu mcac_100. Đây là dev nội bộ, không phải holdout.
- Audit checkpoint: 1108 state keys của app; missing=0, nạp shape thành công, 38 unexpected chỉ thuộc feature_map_encoder. Lần audit thô dừng để review; đối chiếu groundingdino.py dòng 110/325 và groundingdino_app.py cho thấy khối dư không dùng trong đường app, nên ghi quyết định tương thích B0 đã pin. Không sửa code upstream và không quy lỗi đếm cho checkpoint. Hash local b89395d79711c9b9f13f3ef80cd2e528386fb1d70453f99443be4eccab33592f.
- Tạo run_b0_batch.py gọi script gốc từng query, ngưỡng 0.23, xuất predictions.jsonl/run_config/overlay/log; đo elapsed toàn tiến trình, peak VRAM chưa đo. Kiểm input hợp lệ; từ chối trùng ID, GT leakage và count không khớp boxes.
- Chạy thật adapter_check_cat_20261014 trên ảnh utensils cũ: thành công, count=0 giống gốc. Đây là kiểm adapter, không phải MUCCA. Chưa chuẩn hóa đủ cả ba output cũ hoặc xác nhận ghép evaluator/G1.
- Đã tạo handoff mới ngày 14/10 và hướng dẫn M4. **Chưa chạy 30 query MUCCA.** Người dùng chạy tiếp ảnh đầu 3 query, kiểm output rồi mở 5 ảnh sau khi nối evaluator. Không train, chỉnh ngưỡng hoặc mở B2.


## 14/10/2026 — M4 ảnh đầu đã hoàn tất

Người dùng chạy m4_first_image_b0 và gửi log 3/3 ok. Đã kiểm trực tiếp run_config status=complete, failed_queries=0; ba dòng dự đoán có IDs khớp manifest, count/boxes/scores khớp và đủ overlay. Guitars 25/GT25, amplifiers 44/GT11, chairs 0/GT1. Đã xem cả ba overlay: truy vấn amplifiers vẫn khoanh nhiều guitar; chairs bỏ sót ghế/stool phía dưới trái theo nhãn nguồn. Đúng số guitar chưa đồng nghĩa đã chấm vị trí chính xác tuyệt đối.

Đã lưu REVIEW.md và initial_review.json cùng run, gồm hash manifest/predictions để truy vết. Không sửa output gốc. Đây là review độc lập ba dòng, chưa xác nhận Triệu có evaluator hoặc hoàn tất G1. Tiếp theo thu thập 5 ảnh/15 query ở ngưỡng 0.23, cho phép chạy dữ liệu song song với hoàn thiện evaluator; chưa dùng để chốt hướng cải tiến hay chỉnh ngưỡng. Ảnh đầu nằm trong batch 5, không tính lặp là mẫu độc lập. Đồng bộ handoff/pipeline/hướng dẫn.


## 14/10/2026 — hoàn tất và kiểm batch M4 5 ảnh / 15 query

Người dùng chạy m4_first5_b0 và gửi 15 count. Đã kiểm trực tiếp run_config complete, 15/15 dự đoán hợp lệ, IDs đúng, count/boxes/scores và tọa độ/score hữu hạn; đủ overlay. Ghép với manifest: GT lần lượt 25,11,1; 15,3,2; 6,6,6; 6,24,39; 2,4,3. Dự đoán 25,44,0; 28,31,23; 17,18,17; 60,43,84; 20,11,21.

Review sơ bộ: 1 đúng count, 13 thừa, 1 thiếu; MAE=19.4, RMSE≈24.316, coverage=1.0; presence recall=14/15 không chứng minh chọn đúng loại. Không có absent nên các chỉ số absent=null. Không gộp ảnh chạy lặp với run đầu như mẫu độc lập. Chưa phải đánh giá toàn benchmark hoặc xác nhận evaluator của Triệu.

Đã xem cả 15 overlay: ampli lấy guitar; bowls/cups lấy nhiều đĩa; pens/rulers/pencils đều khoanh gần hết ba nhóm; hai ảnh trái cây lấy cả loại khác. Lưu REVIEW.md, review_per_query.csv, review_metrics.json (kèm hash GT/predictions), hai bảng ảnh và stationery_query_comparison.jpg trong run. Giữ nguyên predictions/config gốc.

Thay bước chạy thêm ảnh ngay bằng chẩn đoán có mục tiêu trên mcac_200 và mcac_100: kiểm điểm từng token và lọc gốc, đặc biệt token tên vật so với token đặc biệt/dấu chấm. Đây là giả thuyết điều tra, chưa chứng minh nguyên nhân và chưa sửa baseline. Triệu kiểm nhãn/khung và nối evaluator, bổ sung absent. Chưa B2/train hoặc chốt cải tiến. Đã đồng bộ handoff/pipeline.


## 15/10/2026 — chẩn đoán điểm token rulers, giữ nguyên B0

Người dùng yêu cầu next move sau baseline → lỗi → nguyên nhân → cải tiến → kiểm chứng. Đã tạo diagnose_tokens.py, chỉ nạp import/định nghĩa hàm của process_folder.py đã pin và thêm observer trả nguyên kết quả lọc. Script kiểm hash model/checkpoint, không đọc GT vào model, lưu raw sigmoid scores/boxes/input_ids, token CSV, ảnh proposal IDs và so lại count/boxes/scores với baseline.

Kiểm ca giả phân biệt điểm từ nội dung, dấu chấm, rejected bởi negative-side và dưới ngưỡng đạt. Chạy GPU token_diagnostic_rulers_20261015/q03_2: count=18, counterfactual chỉ token nội dung=18, khớp count/boxes (atol 0.001 pixel)/scores (1e-5) với B0. Cả 18 top-positive token là rulers. Không có khung nào bị loại chỉ nhờ bỏ CLS/dấu chấm. Điều này bác bỏ giả thuyết dấu chấm là nguyên nhân cho query này, chưa khái quát các query khác.

Đã xem proposal_ids và gán nhãn hậu kiểm: thước IDs 0,1,2,3,4,13; bút mực 5,6,7,8,11,44; bút chì 9,10,12,14,15,16. Điểm rulers: thước 0.4252–0.4906, bút mực 0.4232–0.4445, bút chì 0.3540–0.3776. Cần Triệu kiểm chéo; không dùng nhãn này làm model input. Không có một ngưỡng trên điểm này vừa giữ đủ 6 thước vừa bỏ hết bút trong ca này; chưa chọn ngưỡng hoặc kết luận ngưỡng vô ích trên dataset.

Predict có capture, chưa warm-up: 1736.6 ms; peak PyTorch allocated 1461.12 MiB gồm model, không phải tổng device VRAM. Không so với thời gian subprocess batch cũ hoặc ghi hồi tố cho run cũ.

Đã lưu REVIEW.md và manual_box_review.csv cùng run, tạo handoff 15/10 và đồng bộ tài liệu. Bốn query pens/pencils/guitars/amplifiers chưa chạy chẩn đoán; người dùng chạy tiếp theo lệnh trong review. Chưa B2/train/chỉnh lọc hoặc chọn module cải tiến.


## 15/10/2026 — hoàn tất bốn query chẩn đoán bổ sung

Người dùng chạy token_diagnostic_more_20261015, cung cấp log pens=17, pencils=17, guitars=25, amplifiers=44; replay_matches=True. Đã kiểm run_config complete và summary. Đã đọc raw_scores.npz của cả bốn query và rulers ở run trước, tự tính lại masks theo max positive/remaining và max token tên vật. Cả 5 query/2 ảnh có tập proposal giữ nguyên, tổng 121 retained proposals; không chỉ count bằng nhau. Pencils tách pencil + ##s; top token của 17 khung là pencil. Các query còn lại top token đúng tên vật. Không có khung được giữ chỉ vì CLS/dấu chấm ở các ca này.

Kết luận giới hạn: cách tổng hợp điểm token đặc biệt không giải thích lỗi đã kiểm; chưa thử caption không có dấu chấm và chưa biết nguyên nhân learned score gán cao cho lớp khác. Autocast FutureWarning không làm hỏng run. Không sửa baseline/env hoặc chạy lại chỉ vì cảnh báo.

Lưu REVIEW.md và combined_review.json trong run bổ sung. Bước tiếp theo chuyển sang chuẩn bị đối chứng B0/B2 trên cùng mcac_200/mcac_100 (ba query mỗi ảnh), trước tiên kiểm code/chính sách chọn pseudo-exemplar. Chưa triển khai/chạy B2, chưa coi là phương pháp cải tiến mới/full paper và chưa train. Nhãn/evaluator/absent/holdout phía Triệu còn cần kiểm. Đã đồng bộ handoff/pipeline.


## 15/10/2026 — bắt đầu M5, chuẩn bị B2 và kiểm kỹ thuật

Người dùng yêu cầu bước tiếp và vị trí pipeline. M4 có baseline 5 ảnh/15 query và chẩn đoán token; chuyển M5 đối chứng pseudo-exemplar. Đọc test_shanghai_tech.py:get_pseudo_exemplars: max token target, score>threshold, sort top tối đa 3, clamp xyxy. Đọc app/transforms xác nhận exemplar nhận pixel theo ảnh resize; adapter chọn trong ảnh gốc rồi transform lại. Không chỉnh code upstream.

Tạo run_b2_pilot.py, check_b2_selection.py, b2_two_images.jsonl (6 query không GT) và b2_smoke_inputs.jsonl (spoon/fork/cat). B2 chọn toàn bộ proposals lượt đầu bằng tau_sample .23, top3, không NMS; giữ final filter app và tau_final .23. Không synthetic/crop/negative labels. Nhánh không mẫu trả B0 và stage2=null theo protocol adapter, khác upstream luôn gọi lượt hai. Config ghi rõ khác biệt, raw NPZ lưu đủ 900 proposals mỗi lượt, ảnh pseudo xanh và stage1/final đỏ; errors null và dừng, không ghi đè run.

Kiểm chọn mẫu với hàm gốc trên ca giả, clipping, scaling, strict threshold và empty đạt. GPU smoke b2_smoke_20261015: spoon B0=19/pseudo3/B2=19; fork 14/3/18; cat 0/0/0 no_pseudo=True, không forward2. Cả ba stage1 khớp B0 count/boxes/scores; kiểm JSON/schema/tọa độ/overlay đạt. Đã xem bảng ảnh: spoon chọn 3 mẫu nĩa; fork mẫu nĩa nhưng final vẫn có muỗng. Đây là kiểm kỹ thuật và quan sát, chưa khẳng định nguyên nhân hay hiệu quả nghiên cứu.

Đã viết README_B2 và đồng bộ handoff/pipeline. Người dùng chạy tiếp b2_two_images_20261015 trên mcac_100/mcac_200. Chưa chạy B2 MUCCA, chưa mở M6/ngưỡng/cải tiến/train. Tài nguyên ghi predict+capture, khác elapsed toàn subprocess cũ; không đánh dấu evaluator/G1/holdout hoàn tất.


## 15/10/2026 — M5 B2 hai ảnh/sáu query đã chạy và review

Người dùng gửi đủ sáu log b2_two_images_20261015. Đã kiểm file config complete, IDs/GT, count/boxes/scores, khung mẫu trong ảnh, stage1_matches_B0=True cả sáu. Kết quả B0→B2: guitars25→25, amplifiers44→38, chairs0→0, pens17→13, rulers18→18, pencils17→16. Chairs không mẫu nên fallback, không forward2; năm query còn lại tự chọn 3 mẫu và chạy lượt hai.

Đã xem bảng ghép stage1/pseudo/final trên cả hai ảnh. Nhận xét bằng mắt: mẫu guitar đúng; mẫu amplifiers đều guitar; pens trộn pen/pencil; mẫu rulers đúng thước nhưng final vẫn đếm cả18; mẫu pencils đều pen. Cần Triệu kiểm chéo, không dùng nhận xét làm đầu vào. Chưa thể quy mọi lỗi cho chọn sai mẫu hoặc tuyên bố nhân quả.

Đối chiếu GT cùng sáu query: MAE B0=11.3333, B2=9.5; 3 ca giảm sai số, 3 không đổi; exact count vẫn 1/6. Không so B2 9.5 với MAE19.4 của15 query khác tập. Lưu REVIEW.md, review_per_query.csv, review_metrics.json/hash và hai bảng ảnh trong run; output model giữ nguyên.

Bước tiếp theo M6: khảo sát ngưỡng cuối trên raw lượt2 đã lưu, giữ mẫu/tau_sample cố định, ghi riêng fallback; đổi mẫu phải chạy lại lượt2. Chưa thực hiện sweep, chưa train/chốt phương pháp mới hoặc B2 cả5 ảnh. Còn evaluator/absent/holdout. Đã đồng bộ handoff/pipeline.


## 15/10/2026 — M6/E1 quét ngưỡng lọc cuối, không chạy lại mô hình

Người dùng yêu cầu tiếp M6. Đã đọc protocol và giữ lưới định trước {.10,.23,.35,.50}; tau_sample=.23/mẫu cố định. Tạo sweep_final_threshold.py và thực thi CPU vào m6_e1_final_20261015. Áp dụng nguyên mask positive max>tau_final và positive max>remaining max cho stage1 B0, stage2 B2; fallback chairs refilter stage1. Không train/forward hoặc thay mẫu. Manifest chỉ dùng để chấm sau lọc, không chọn ngưỡng từng query.

Đã kiểm đủ6IDs/GT và raw hữu hạn, tái lập count/boxes/scores ở.23 cho cảB0/B2, monotonic tập khung qua4ngưỡng, hoàn tất48tổ hợp. B0 MAE lần lượt16.833/11.333/7.833/5.0; B2 14.167/9.5/8.0/6.0. Exactcount vẫn1/6 từ.23 trở lên. B0 .50 có4query trả0, gồm3lớp mới bị bỏ hoàn toàn (amplifiers/rulers/pencils) và chairs đã0; không chốt .50 chỉ vìMAE thấp. Đã xem ảnh sweeps pens/rulers/amplifiers: nhầm loại vẫn có ở cấu hình giữ khung, hoặc mất toàn bộ vật đúng khi lọc cao.

Lưu per_query.csv, summary.csv/json, predictions.jsonl mỗi ngưỡng kèm proposal IDs, sáu ảnh sweep, run_config có hash nguồn/GT/adapter và REVIEW.md. Baseline gốc và B2 nguồn không sửa. Chưa có absent/holdout, chưa xác nhận evaluator củaTriệu. M6/E1 đã xong trên2ảnh; bước tiếp E2 thaytau_sample giữtau_final=.23, chưa chạy. Đã đồng bộ handoff/pipeline.

## 15/10/2026 — đóng E2 pilot và ghi nhận review bằng mắt của Trí

Người dùng tự thêm --tau-sample vào runner và chạy m6_e2_sample010_20261015, m6_e2_sample050_20261015. Đã đọc config/predictions của hai run và B2 nguồn .23: đủ 6 query/run, execution_status=ok, stage1_matches_B0=True; final=.23, max_pseudo=3. .10 giữ nguyên pseudo_boxes/final_boxes so với .23, không chỉ count. .50 giữ mẫu/final của guitar và pens; ampli/thước/bút chì không mẫu nên stage2=false/null và trả B0. Ghế không mẫu ở mọi mức. Counts .50: 25,44,0,13,18,17. Mức .35 bỏ qua sau khi kiểm điểm top-3 đều >.35 ở 5 query có mẫu; đây là suy luận từ selection, chưa chạy inference .35. Đóng E2 pilot không đồng nghĩa đã chạy đầy đủ bốn mức hoặc hoàn tất benchmark/M6 tổng thể.

Trí gửi review cả 6 query của run .23: guitar mẫu 3/3 và final đúng theo mắt; ampli mẫu 0/3 (đều guitar), final vẫn lẫn nhiều loại; ghế không mẫu/khung (GT có 1); pens mẫu 1/3, hai mẫu là pencils, final theo người dùng có 1 ruler và cả pens/pencils; rulers mẫu 3/3 nhưng final vẫn lẫn tất cả; pencils mẫu 0/3 (đều pens), final gần hết các vật. Lưu USER_VISUAL_REVIEW.md riêng trong run B2 nguồn, giữ nguyên nhận xét với nguồn là người dùng; chưa có xác nhận của Triệu hoặc phân loại từng khung. “Khoanh all” không diễn giải thành khung stage1/final giống hệt vì count ampli 44→38, pencils 17→16. Nhận xét này không phải nhãn model input.

Kết luận: cả lỗi chọn mẫu lẫn lỗi final khi mẫu đúng đều xuất hiện; không quy toàn bộ lỗi cho pseudo hoặc tuyên bố nhân quả. Lưu REVIEW.md E2 trong run .50; đồng bộ handoff/roadmap/README. Không chạy thêm model hoặc sửa thuật toán trong lần cập nhật này. Chưa mở E3/train/module mới.

Bước tiếp theo: Triệu kiểm chéo và hoàn thiện evaluator/absent; Trí chuẩn bị mở B2 cấu hình .23 trên 3 ảnh còn lại của bộ dev 5 ảnh đã có B0, chưa chạy. Đây là dev đã xem B0, không phải holdout. Mục đích kiểm tra lỗi có lặp ở ảnh khác trước khi chọn một can thiệp. Người dùng tự thực hiện thí nghiệm; assistant chỉ đường và kiểm kết quả. Không gửi tin nhắn cho Triệu bằng công cụ.


## 15/10/2026 — B2 mở rộng đủ 5 ảnh / 15 query

Người dùng tạo b2_remaining3_inputs.jsonl và tự chạy b2_remaining3_20261015 ở tau_sample=tau_final=.23. Đã kiểm config complete, 9 query đúng IDs và đều ok; 3 mẫu/query, có lượt hai, stage1 khớp B0 count/boxes (<=.001 pixel)/scores (<=1e-5). Ghép hai run được đúng 15 IDs/5 ảnh trong first5; kiểm count bằng số khung/score, tọa độ hợp lệ và giá trị hữu hạn. Cấu hình suy luận/selection/checkpoint khớp; adapter hash khác sau khi thêm CLI tau_sample, không gọi script byte-identical. Không chạy thêm model.

Counts B0→B2 mới: plates 28→31, bowls 31→31, cups 23→26, strawberries 60→59, blueberries 43→32, red currants 84→84, cherries 20→15, raspberries 11→14, blackberries 21→79. Trên cùng 15 query, GT từ manifest gói Triệu: MAE 19.4→22.0; RMSE 24.315976→30.090973; exact count 1/15 cả hai. Sai số giảm 6, tăng 4, giữ nguyên 5. Đây là metric đếm trên dev nhỏ, không chứng minh chọn đúng loại hoặc kết luận chất lượng paper. Không bỏ ca blackberries khỏi tổng hợp.

Assistant xem pseudo/final q05_3: mẫu nhìn là 2 blackberry và 1 raspberry đỏ; final có nhiều khung nhỏ theo phần tròn trên blackberry, nhiều lớp khác và khung chồng nhau. Ghi là quan sát sơ bộ, cần Trí/Triệu kiểm chéo; chưa phân loại từng proposal hoặc chứng minh mẫu sai gây tăng count. Không coi mọi khung thừa đều là trùng hay đều đếm phần vật.

Lưu REVIEW.md và combined_first5_metrics.json (bảng 15 query, metric và hash nguồn) trong run mới; đồng bộ handoff/pipeline/README. Trí review tiếp 9 query mới, ưu tiên q05_3 rồi so cùng ảnh q05_1/q05_2. Triệu kiểm chéo nhãn và evaluator; chưa xác nhận evaluator/absent/holdout đầy đủ. E1/E2 chỉ trên 2 ảnh, không tự mở rộng trạng thái thành 5 ảnh. Chưa E3/train/chốt module; người dùng tiếp tục tự làm thí nghiệm.


## 15/10/2026 — Trí hoàn tất review bằng mắt 15 query

Người dùng báo mẫu đúng ở 9 query mới: plates 0/3, bowls 1/3, cups 2/3, strawberries 2/3, blueberries 2/3, red currants 0/3, cherries 1/3, raspberries 3/3, blackberries 2/3. Người dùng xác nhận q02_3 ghi bowl là gõ nhầm, vẫn khoanh được cups; giữ phần khoanh sai/thừa nhiều. Cherry có 2 quả phù hợp GT gói Triệu. Final blackberries đếm múi thành bbox và khoanh cả các loại quả khác. Lưu USER_VISUAL_REVIEW.md trong run remaining3, không sửa predictions/GT.

Ghép nhận xét cũ: 20/42 mẫu đúng theo người dùng trên 14 query có mẫu; 3 query đúng 3/3 (guitar/thước/raspberries), 4 query sai 0/3, 7 query pha trộn; chairs không có mẫu. Guitar final đúng theo mắt, hai ca thước/raspberries mẫu đúng nhưng final vẫn sai/thừa. Đây là review định tính của Trí, chưa là chấm từng bbox hoặc kiểm chéo của Triệu; không khẳng định mẫu sai là nguyên nhân duy nhất. “Final như stage1” không hiểu là cùng tập khung, vì cherries 20→15 và raspberries 11→14. Metric count toàn tập giữ nguyên MAE 19.4→22.0.

Kết thúc vòng nhận xét chung 5 ảnh, chuyển sang phân loại từng khung. Việc kế tiếp: Trí và Triệu gán nhãn 14 bbox q05_2 raspberries theo loại thật, cả vật/phần vật, ID vật để phát hiện trùng và vật thật bị bỏ sót. Nhãn chỉ để đánh giá, không cung cấp GT cho model. Giữ trọng tâm giảm đếm nhầm loại theo X/Y; phần quả là nhóm lỗi cần đo, chưa mở thành mục tiêu thứ hai. Chưa chọn giải pháp, chạy inference mới, E3, train hoặc thay NMS. E1/E2 vẫn chỉ 2 ảnh. Đã cập nhật handoff/pipeline/README và liên kết review.


## Chuẩn bị benchmark Kaggle — 15/10/2026

Người dùng xác nhận ảnh 1.190 ảnh/MAE 10.20 thuộc nhóm khác và yêu cầu hỗ trợ chạy đánh giá giống paper. Đã tạo roadmap/COUNTGDPP_FSCD147_KAGGLE.ipynb và KAGGLE_PAPER_EVAL.md; cấu hình text+synthetic+pseudo+crop theo README, pin commit hiện có; số tham chiếu paper v2 8.39/27.03. Đã kiểm cú pháp 6 code cell và đọc code upstream. Chưa chạy trên Kaggle, chưa tải assets tại Kaggle, chưa có kết quả benchmark mới. Script phụ test_fscd147.py không có trong checkout; notebook kiểm MAE/RMSE từ engine chính và log từng ảnh, không nhận đã tái lập AP/AP50. Tiếp theo: người dùng import notebook và chạy cell kiểm môi trường; giữ nguyên nhánh pilot, không so trực tiếp metric khác tập.


## 16/10/2026 — nhận kiểm chéo của Triệu, giải thích đủ q05_2

Đọc workspace Trí and Triệu/Triệu/TRIEU_VISUAL_REVIEW.md, hash SHA256 08767b8b77cdd42aeecb7bfa2c573f6b8be94ee959bde382678ed8c07fa8fd0f. Có 14/15 query (thiếu q01_1), GT/B0/final của tất cả 14 khớp bảng kết quả. Giữ nguyên file nguồn và các review gốc của Trí, không xem mọi diễn giải trong nguồn là đã tự kiểm độc lập.

Assistant mở q02_1 pseudo và q05_2 stage1/final, đối chiếu tọa độ prediction. Plates: cả 3 mẫu là đĩa, phù hợp Triệu thay vì Trí cũ 0/3; ảnh nhỏ/che khuất, chưa chấm độ bao trọn chuẩn. Tổng hợp hiệu chỉnh 23/42 mẫu đúng (20/42 theo Trí trước đó), chưa gọi toàn bộ được hai người kiểm chéo vì guitar chưa có Triệu. Ba ca plates/rulers/raspberries mẫu đúng 3/3 nhưng final còn sai/thừa.

q05_2 final: 5 khung raspberry 1/2/3/7/11, 9 khung sai loại (blackberry10/14; blueberry9/12/13; strawberry5/6; cherry4/8). 7 và11 cùng quả,11 chỉ bao phần quả. Tổng14 =4 quả mục tiêu+1khung trùng+9khung sai loại. Khung12/13 là phần blueberry; nhãn lỗi phần vật và sai loại có thể cùng tồn tại. Đã lưu manual_crosscheck_20261016.json gồm 14final/11stage1, overlay1-based và index0-based, tọa độ/hash; không dùng nhãn làm model input. Đây là visual audit, không tuyên bố metric định vị benchmark.

Stage1 q05_2 được assistant giải thích thêm: 2 strawberry ở số6/7, không phải1; 4raspberry+2strawberry+2cherry+3blueberry=11. File nguồn Triệu giữ nguyên; ghi riêng bổ sung. q04_2 còn cần đối sánh32khung với mô tả “toàn bộ” các quả; không suy ra số/loại bỏ sót từ chênh lệch35vs32.

Tạo TRIEU_CROSSCHECK_2026-10-16.md, handoff ngày16, cập nhật index/ngày và pipeline/README; giữ snapshot15 và ưu tiên benchmark Kaggle từ phiên khác. Không chạy thêm model/train, không chọn module. Tiếp theo Triệu bổ sung guitar/q04_2; dùng nhãn q05_2 kiểm evaluator, không yêu cầu làm lại từ đầu. Kaggle notebook mới chuẩn bị; chưa xác nhận run/metric mới và không so trực tiếp với MAE pilot. Không gửi tin nhắn cho Triệu bằng công cụ.

</details>

## 20/10/2026 — Phần 2: Đánh giá pilot

- Self-test: PASS (python3).
- Evaluator: evaluation/evaluate_pilot.py
- Output: results/countgdpp/pilot_eval_20261020/
- Số ảnh: 5
- Số query: 15
- B0: MAE=19.4, RMSE=24.315975544210986, exact_count=1
- B2: MAE=22.0, RMSE=30.090973175799196, exact_count=1
- Coverage: B0=15/15, B2=15/15
- Errors=0, uncertain=0
- Improved=6, worsened=4, unchanged=5
- Absent queries=0 (absent metrics=null)
- Manual q05_2: final_boxes=14, target_boxes=5, distinct_target_objects=4, extra_target_boxes=1, wrong_class_boxes=9
- Ket luan: So lieu khop bang tham chieu.
- Trang thai: Cho Trieu kiem tra cheo code/schema va q05_2.
