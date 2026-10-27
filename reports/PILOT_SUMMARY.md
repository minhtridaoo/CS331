# Tổng kết pilot CS331 — CountGD++ và lỗi chọn đối tượng

**CẬP NHẬT 27/10/2026: TRIỆU ĐÃ CHẤP NHẬN BẢN KIỂM — CHỜ NHÓM DUYỆT.** Số liệu pilot giữ từ run 15/10; review Triệu chốt v1 ngày 19/10 đã đọc lại ngày 20/10. Evaluator đã chạy và được đối chiếu ngày 20/10/2026; chưa coi báo cáo được nhóm duyệt.

**Pilot là bộ thử nhỏ 5 ảnh/15 câu hỏi để tìm lỗi.** Đây là file hoàn thiện ở phần 3, sau khi chạy evaluator ở phần 2. Nhánh benchmark 1.190 ảnh đã có [báo cáo riêng](BENCHMARK_FSCD147.md), không thay thế việc xác nhận các ô dưới đây.

## 1. Thông tin bạn tự điền

- Người chạy evaluator: **Minhtri**
- Ngày chạy: **20/10/2026**
- Self-test: **PASS theo xác nhận Minhtri trong handoff — `python3 evaluation/evaluate_pilot.py --self-test`**; chưa có stdout riêng, assistant không chạy lại self-test.
- Thư mục evaluator thực tế: **results/countgdpp/pilot_eval_20261020/**
- Coverage/IDs đã kiểm: **15/15 B0 và B2; 0 error, 0 uncertain; paired=15**
- Audit artifact/code: **assistant ngày 20/10 đã đối chiếu trực tiếp đủ 15 dòng, metrics, manual_check và hash nguồn**; không thực thi evaluator/model.
- Người thực hiện kiểm kỹ thuật: **assistant**. Người đọc, hiểu và chấp nhận kết quả kiểm được ủy quyền: **Triệu — 24/10/2026**, xác nhận trực tiếp trong chat; không ghi Triệu đã tự audit code. Review định tính đã chốt ngày 19/10 là công việc khác.
- Trạng thái báo cáo: **TRIỆU ĐÃ CHẤP NHẬN KẾT QUẢ KIỂM ĐƯỢC ỦY QUYỀN — CHỜ NHÓM DUYỆT**

## 2. Câu hỏi và thiết lập

Cùng ảnh, đổi tên loại X/Y có làm mô hình đếm riêng đúng loại được hỏi không? Dùng checkpoint CountGD++, chưa fine-tune. B0 là text một lượt; B2 là lượt đầu → top tối đa 3 mẫu tự chọn → lượt hai. Tau_sample=tau_final=.23; không mẫu thì trả B0 theo quy ước adapter. Đây không phải tái hiện toàn pipeline paper.

Tập 5 ảnh/15 query dev từ gói dữ liệu Triệu; mọi query trong tập này có đối tượng. GT chỉ đưa vào evaluator. Không có holdout độc lập hoặc absent query trong 15 dòng. Mẫu và khung được review bằng mắt để chẩn đoán, không dùng nhãn hậu kiểm làm input model.

## 3. Kết quả pilot đã đối chiếu bằng evaluator

Nguồn hiện tại: [metrics.json](../results/countgdpp/pilot_eval_20261020/metrics.json), [per_query.json](../results/countgdpp/pilot_eval_20261020/per_query.json), [manual_check.json](../results/countgdpp/pilot_eval_20261020/manual_check.json). Khớp [số liệu lịch sử](../results/countgdpp/b2_remaining3_20261015/combined_first5_metrics.json). **Assistant đã đọc file và kiểm phép ghép/phép tính ngày 20/10/2026.**

| Cấu hình | Số query | MAE | RMSE | Đúng count |
|---|---:|---:|---:|---:|
| B0 | 15 | 19.4 | 24.315976 | 1/15 |
| B2 | 15 | 22.0 | 30.090973 | 1/15 |

B2 giảm sai số 6 query, tăng 4, giữ nguyên 5. Đếm giảm chưa chứng minh đúng loại; B2 không cải thiện MAE trung bình trên pilot này. Không loại ca blackberries để làm kết quả đẹp hơn.

**Lưu ý độ nhạy (Triệu tự kiểm 27/10):** kết luận B0/B2 phụ thuộc mạnh vào q05_3 blackberries (sai số B2 = 76). Bỏ riêng câu này thì MAE B0 = 273/14 = 19.5, B2 = 254/14 ≈ 18.14, tức chiều so sánh đảo ngược. Vì vậy chỉ ghi "trên pilot 15 câu, MAE B2 cao hơn B0, chủ yếu do q05_3", không ghi B2 kém hơn B0 như kết luận tổng quát. Vẫn giữ q05_3 trong metric vì đây là lỗi thật của model. [Chi tiết](TRIEU_TU_KIEM_PHAN2_20261027.md).

**Xác nhận sau phần 2:** Run `results/countgdpp/pilot_eval_20261020/`; B0 và B2 đều có 15/15 query hợp lệ, 0 error, 0 uncertain. Hai bên ghép chung 15 query. MAE/RMSE và exact_count khớp bảng tham chiếu. Hậu kiểm q05_2 cũng khớp. Có đủ 5 file output. Cả 7 nguồn khớp nội dung đã lưu; trong checkout Windows ngày 24/10 có 3 hash byte thô khớp, 4 hash chỉ khớp sau chuẩn hóa CRLF→LF (xem audit). Run `_r2` có cùng 4 file kết quả và cùng hash nguồn; chỉ khác tên output trong command, không coi là mẫu thí nghiệm độc lập. Ngày 24/10, Triệu đã đọc, hiểu và đồng ý dùng kết quả kiểm kỹ thuật do assistant thực hiện; không coi đây là Triệu tự audit code. Lượt tiếp nhận 27/10 trên máy Trí: 7/7 hash khớp byte thô; khác biệt EOL trong audit 24/10 thuộc checkout của lần đó, không sửa metadata để ép khớp.

## 4. Bằng chứng định tính và kiểm chéo

**Trí và Triệu đều đã review định tính 15/15 query.** Nguồn hiện hành: [TRIEU_VISUAL_REVIEW.md — chốt v1 ngày 19/10](<../workspace Trí and Triệu/Triệu/TRIEU_VISUAL_REVIEW.md>), đọc lại tại workspace ngày 20/10. Bản [đối chiếu ngày 16/10](../results/countgdpp/b2_remaining3_20261015/TRIEU_CROSSCHECK_2026-10-16.md) là lịch sử; các ghi chú còn thiếu guitar/q04_2 trong bản đó đã được cập nhật bởi review mới.

- Guitar: theo quy ước Triệu xác nhận, ca không nêu lỗi là đã xem và thấy đúng; stage 1, pseudo và final được chốt đúng định tính. Không coi đây là chấm IoU chính thức.
- Plates: pseudo được Triệu xác nhận 3/3 đúng loại, bao trọn đĩa. Review gốc Trí ghi 0/3 được giữ nguyên như lịch sử. Plates/rulers/raspberries có mẫu đúng 3/3 nhưng final vẫn sai/thừa.
- Tổng số pseudo đúng loại theo bảng review chốt: 23/42 (14 query có 3 mẫu, chairs không có mẫu). Đây là phân loại định tính của review, không phải precision/recall định vị hoặc 42 mẫu đều được hai người phân xử độc lập.
- q04_2 blueberries: final 32 = 24 blueberry + 7 blackberry + 1 red currant theo bản chốt; chênh lệch 35/32 đã được giải quyết. 10 điểm blackberry trong nguồn khác với 7 quả nhìn thấy theo review; giữ dữ liệu nguồn, không đổi GT mục tiêu blueberries=24.
- q05_2 raspberries: final 14 = 4 quả mục tiêu + 1 khung trùng + 9 khung sai loại. Triệu chốt lỗi trùng/sai loại; các nhận xét cũ của assistant về “bao một phần” không tự trở thành nhãn đã được Triệu xác nhận.
- q02_1 plates: đã pull [bản chi tiết](<../workspace Trí and Triệu/Triệu/Q02_1_DETAILED_REVIEW.md>), ba JSON và 9 ảnh bằng chứng. Stage1 = 15 nhóm đĩa + 10 khung dư + 3 sai loại; final = 15 nhóm + 13 khung dư + 3 sai loại. Một số nhóm chắc chắn vừa; JSON giữ `human_adjudication_complete=false`, không coi toàn bộ nhãn đã được Triệu phân xử.
- Blackberries 21→79: có sai loại và đếm phần quả; chưa phân loại đủ 79 khung để lượng hóa mọi cơ chế.
- Chairs GT=1 nhưng trả 0; bowls có bỏ sót một bát theo review. Đây là ca lớp có mặt, không phải truy vấn absent.

[Nhãn hậu kiểm q05_2 ngày 16/10](../results/countgdpp/b2_remaining3_20261015/q05_2/manual_crosscheck_20261016.json) vẫn dùng cho phép kiểm số khung/lớp/vật trong evaluator. Phép kiểm không chấm hoặc xác nhận các cờ phần vật; ghi nguồn/giới hạn theo review mới ở trên.

## 5. Đối chứng ngưỡng và giới hạn

E1 thay ngưỡng cuối với mẫu cố định; E2 thay ngưỡng mẫu giữ cuối=.23, chỉ trên 2 ảnh/6 query. E2 chạy .10/.23/.50; .35 bỏ qua có lý do từ điểm top-3, không báo là đã chạy. Chưa E3 hoặc train. Nhánh lọc khung P4 đã được thử ngày 20–21/10, tách khỏi E1/E2 và trình bày ở mục 6. [E1](../results/countgdpp/m6_e1_final_20261015/REVIEW.md) · [E2](../results/countgdpp/m6_e2_sample050_20261015/REVIEW.md).

5 ảnh chưa đại diện toàn benchmark. Nhãn đếm có từ gói nguồn nhưng xuất xứ/giấy phép và toàn bộ định vị chưa được xác minh đầy đủ. Chưa có absent/holdout trong pilot; benchmark tài nguyên chuẩn còn chờ. Nhánh FSCD-147 Kaggle đã xác nhận count metrics ngày 20/10 trong báo cáo riêng; không suy rộng kết quả đó sang phép thử X/Y của pilot. Chưa tìm ra nguyên nhân nội tại kiến trúc từ các quan sát này.

## 6. Kết quả thăm dò P4 và hướng tiếp — cập nhật 22/10

**P4 đã được thực hiện đến P4.5c**, mới hơn bản tài liệu ngày 20/10. CountGD++ B2 vẫn tạo dự đoán; CLIP là model phụ so crop–query, **không phải CLIP-Count**. Bản này ghi kết quả thực tế, không tự xác nhận nhóm đã duyệt phương pháp hoặc pilot.

### 6A. Những gì đã chạy và có artifact

- CLIP `openai/clip-vit-base-patch32` đã chấm đủ 481 bbox/15 query trên 5 ảnh dev; prompt `a photo of {prompt}`, cosine hai embedding chuẩn hóa. [Cấu hình](../results/countgdpp/p4_clip_all15_20261020/run_config.json).
- Đã so lọc điểm B2 với lọc điểm CLIP bằng CV chia theo ảnh gốc, và thử Fusion 50/50. Mỗi fold chọn ngưỡng trên 4 ảnh, kiểm trên ảnh còn lại; min/max Fusion cũng chỉ dùng 4 ảnh training. Toàn bộ vẫn là dev đã dùng thiết kế/chọn cách làm.
- Đã có review 4 query, chẩn đoán oracle Top-K/AUC và prompt số ít. K từ GT chỉ dành cho chẩn đoán, không được dùng suy luận đếm ảnh mới. Các nhánh không tốt hơn được giữ trong [báo cáo P4](P4_CLIP_EXPLORATORY_FINDINGS_20261021.md).

| Cấu hình từ cùng khung B2 | MAE CV dev | RMSE CV dev |
|---|---:|---:|
| B2 gốc | 22.0 | 30.090973 |
| Chỉ lọc theo điểm CountGD++ | 4.6 | 6.618157 |
| Chỉ lọc theo điểm CLIP | 6.8 | 8.846845 |
| Fusion 50/50 | 5.8 | 7.793159 |

**Kết luận đúng phạm vi:** lọc điểm CountGD++ tốt nhất về MAE trong bảng này; chưa thể nói Fusion tốt hơn. Trên 4 query chọn để review, nhãn hiện tại cho B2 lọc điểm giữ 12/22 vật đúng, Fusion 16/22. Nhãn q03 là assistant sơ bộ, chờ Triệu kiểm độc lập; không dùng các số này để tuyên bố đã khái quát hoặc đạt AP/IoU.

### 6B. Khóa cấu hình và điều audit đã xác nhận

Đã có [freeze 21/10](../results/countgdpp/p4_candidate_freeze_20261021.json) và [audit từ điểm lưu sẵn](../results/countgdpp/p4_freeze_audit_20261021.json). Ngưỡng B2 `0.9067394733428955`, Fusion `0.6551826746408328`; Fusion dùng min/max toàn dev đã khóa, clamp [0,1]. Khi áp dụng phải đọc JSON đủ precision.

**Dev-fit MAE B2=4.333333, Fusion=4.4** là kết quả trên chính 5 ảnh dùng chọn ngưỡng, khác CV và không phải holdout. [Audit 22/10](P4_AUDIT_20261022.md) xác nhận 16 hash nguồn freeze, 17 hash nguồn CV, ID/box/score và các phép tính khớp; không chạy inference/evaluator hay xác nhận nhãn thị giác thay Triệu.

Gói [47 nhãn trắng cho Triệu](../results/countgdpp/p4_label_review_handoff_20261021.zip) đã kiểm mở được, đủ 13/18/16 dòng. Chưa nhận 3 CSV đã kiểm độc lập.

### 6C. Quyết định kế hoạch tiếp theo

- Giữ lọc điểm B2 làm đối chứng, Fusion là ứng viên chọn đúng vật; dừng chỉnh tham số/prompt trên 5 ảnh này.
- Trí chuẩn bị **P4.6a dữ liệu mới** và **P4.6b runner dùng freeze** theo [hướng dẫn](../roadmap/P4_TIEP_THEO.md) trong lúc chờ Triệu. Chưa có tập mới/runner đạt kiểm hoặc kết quả P4.6c–d.
- Khóa nguồn/split/GT/cách đo trước dự đoán; so cùng khung, đo count và đúng vật. Không dùng GT test chọn ngưỡng, tên lớp loại trừ hoặc K.
- Cần pin cấu hình model/processor/code khi làm runner. Freeze audit hiện chỉ kiểm từ score lưu, chưa xác minh hash model hoặc tái lập ảnh → score.
- Bộ lọc chỉ loại khung hiện có, không tìm lại chiếc ghế bị bỏ sót hoàn toàn. Không tuyên bố đã sửa mọi lỗi CountGD++ hoặc thay thế kiểm cấu hình paper.

**P4.6 không phải điều kiện mới để đóng pilot này.** Đóng pilot còn Trí đọc và quyết định duyệt chung; bản kiểm evaluator đã được Triệu chấp nhận; nhánh cải tiến tiếp tục theo kế hoạch riêng.

## 7. Phiếu xác nhận của nhóm — chỉ điền sau khi thực sự kiểm

Audit assistant: output pilot kiểm ngày **20/10**, artifact P4 kiểm ngày **22/10/2026**. Không thay chữ xác nhận của Triệu/nhóm.

- [x] Triệu đã đọc/hiểu và đồng ý dùng bản kiểm kỹ thuật ngày **24/10/2026** do assistant thực hiện theo ủy quyền; không ghi Triệu đã tự audit code. [Báo cáo được chấp nhận](TRIEU_KET_QUA_KIEM_CHEO_20261024.md).
- Người kiểm kỹ thuật: **assistant**. Người xác nhận chấp nhận: **Triệu — 24/10/2026**; [bản ghi xác nhận](audits/TRIEU_ACCEPTANCE_20261024.json). Trí đã đọc ngày 27/10, chưa duyệt và yêu cầu sửa T1–T4; chờ nghiệm thu lại.
- **Trí đã đọc bản kiểm chéo — 27/10/2026: CHƯA DUYỆT.** Nhận xét của Trí (nguyên văn trong [kế hoạch sửa](KE_HOACH_SUA_KIEM_CHEO_20261027.md) §1):
  1. kiểm kỹ thuật chủ yếu do AI làm, Triệu cần tự chạy lại evaluator và lưu bằng chứng, nhất là ca lỗi/thiếu/không chắc;
  2. phân tích kỹ q05_2 và q05_3 (GT 3, B2 đếm 79): sai loại, trùng, bỏ sót;
  3. giải thích vì sao B2 (MAE 22) kém B0 (19,4) và đề xuất cải thiện cụ thể;
  4. hoàn thiện báo cáo, ghi rõ phần tự kiểm, kết quả trước/sau và hạn chế, rồi duyệt chung và thống nhất hướng P4.
- [x] **Triệu tự kiểm chéo Phần 2 — 27/10/2026.** Lần này Triệu tự chạy self-test và evaluator, tự tính lại MAE/RMSE, truy ngược q05_3 về predictions, tự gán nhãn 14 box q05_2 trước khi mở nhãn cũ, và thử 5 ca dữ liệu hỏng; assistant chỉ hướng dẫn. Kết quả khớp run 20/10. [Báo cáo tự kiểm và bằng chứng](TRIEU_TU_KIEM_PHAN2_20261027.md). Kết luận của Triệu, nguyên văn: “Đã check lại metric, q05_3 và tự gán nhãn lại q05_2, check thử đưa dữ liệu hỏng vào thì xảy ra chuyện gì đối với evaluator. Ở q05_2 thì box 12 với [13] chấm khác với nhãn cũ, cũng tùy vào người chấm cũng như máy chấm thì khác nữa, quan điểm mỗi người thôi, theo tôi thì 2 box đó đã làm tốt việc của mình. Nên ghi rõ ở q05_3, thực chất B2 kém hơn B0 thì cũng tùy trường hợp nữa chứ không thể ghi tổng quát như vậy được, các số liệu đó ghi vào báo cáo được đó.” Phạm vi đồng ý: dùng số liệu Phần 2 (MAE/RMSE, 6/4/5, coverage, q05_2) kèm lưu ý độ nhạy ở mục 3. Bản 24/10 phía trên giữ làm lịch sử.
- **Đánh giá của assistant về bản tự kiểm (27/10 tối):** [DANH_GIA_TRIEU_TU_KIEM_20261027.md](DANH_GIA_TRIEU_TU_KIEM_20261027.md). Nhận xét 1 + q05_2 đạt; q05_3 (nhãn từng khung) và phân tích B2/B0 + đề xuất cải thiện chưa đủ. **Trí chưa nghiệm thu lại.**
- Nhóm duyệt nội dung pilot: **CHƯA — Triệu đã tự kiểm Phần 2 (27/10); chờ Trí nghiệm thu và Triệu bổ sung phần còn thiếu (T2 q05_3, T3)**.
- Quyết định pilot: **còn sửa: phần kiểm chéo (mục 1, 3, 4) và phân tích lỗi q05_2/q05_3, B2>B0**.

Theo dõi riêng cho P4, không phải điều kiện cộng thêm vào pilot:

- Triệu kiểm độc lập 47 nhãn q03 và phân xử bất đồng: **[CHƯA]**.
- Nhóm thống nhất phạm vi dữ liệu/cách đo cho tập mới: **[CHƯA XÁC NHẬN]**.
- P4.6 chạy/chấm ảnh mới: **ĐÃ CHẠY 27/10, phần count** ([kết quả](P4_6_UNSEEN_RESULTS_20261027.md)); review khung N4 đang làm.

Trí có thể chuẩn bị dữ liệu/runner ngay theo kế hoạch trong lúc chờ; chưa train lại, chưa đánh giá holdout và chưa chứng minh cải tiến tổng quát. Cập nhật [WORKLOG](../WORKLOG.md), [ROADMAP](../roadmap/ROADMAP.md), [HANDOFF](../HANDOFF/HANDOFF.md) khi có bằng chứng mới.

**Điểm tiếp tục 27/10 (cập nhật cuối ngày):** C1 xong, Trí chưa duyệt; việc sửa theo [kế hoạch](KE_HOACH_SUA_KIEM_CHEO_20261027.md). P4.6: tập `p4_unseen_v1` đã chọn (DRAFT), freeze áp dụng đúng trên dev. [Checklist](../roadmap/CHECKLIST_3_GIO.md). Mục 6 giữ kết quả P4 đã audit ngày 22/10; commit mới không làm mất hay bắt chạy lại phần này.

**Rà phân công V2 ngày 27/10:** giữ nguyên nhận xét Trí; kế hoạch sửa đã có T0 giao đủ đầu vào, T1 fixtures 15 query không phá q05_2, T2 tiêu chí nhãn, T3 phân tích +39/+58/−19 và đúng tên điểm P4, T4 ngày 03/11. Lượt này chưa có run/nhãn/kết luận mới của Triệu.
