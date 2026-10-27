# Tổng kết pilot CS331 — CountGD++ và lỗi chọn đối tượng

**BẢN NHÁP cập nhật xác nhận 24/10/2026.** Số liệu pilot giữ từ run 15/10; review Triệu chốt v1 ngày 19/10 đã đọc lại ngày 20/10. Evaluator đã chạy và được đối chiếu ngày 20/10/2026; chưa coi báo cáo được nhóm duyệt.

**Bổ sung 21/10:** đã có [bản hỗ trợ kiểm chéo evaluator cho Triệu](TRIEU_EVALUATOR_CROSSCHECK_20261021.md) và artifact chi tiết q02_1. Các ô xác nhận của Triệu/nhóm vẫn giữ nguyên. Repo cũng có artifact P4/CLIP mới hơn trạng thái tài liệu bên dưới; cần đồng bộ log và kiểm riêng trước khi chốt P4.

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

**Xác nhận sau phần 2:** Run `results/countgdpp/pilot_eval_20261020/`; B0 và B2 đều có 15/15 query hợp lệ, 0 error, 0 uncertain. Hai bên ghép chung 15 query. MAE/RMSE và exact_count khớp bảng tham chiếu. Hậu kiểm q05_2 cũng khớp. Có đủ 5 file output. Cả 7 nguồn khớp nội dung đã lưu; trong checkout Windows ngày 24/10 có 3 hash byte thô khớp, 4 hash chỉ khớp sau chuẩn hóa CRLF→LF (xem audit). Run `_r2` có cùng 4 file kết quả và cùng hash nguồn; chỉ khác tên output trong command, không coi là mẫu thí nghiệm độc lập. Ngày 24/10, Triệu đã đọc, hiểu và đồng ý dùng kết quả kiểm kỹ thuật do assistant thực hiện; không coi đây là Triệu tự audit code.

## 4. Bằng chứng định tính và kiểm chéo

**Trí và Triệu đều đã review định tính 15/15 query.** Nguồn hiện hành: [TRIEU_VISUAL_REVIEW.md — chốt v1 ngày 19/10](<../workspace Trí and Triệu/Triệu/TRIEU_VISUAL_REVIEW.md>), đọc lại tại workspace ngày 20/10. Bản [đối chiếu ngày 16/10](../results/countgdpp/b2_remaining3_20261015/TRIEU_CROSSCHECK_2026-10-16.md) là lịch sử; các ghi chú còn thiếu guitar/q04_2 trong bản đó đã được cập nhật bởi review mới.

- Guitar: theo quy ước Triệu xác nhận, ca không nêu lỗi là đã xem và thấy đúng; stage 1, pseudo và final được chốt đúng định tính. Không coi đây là chấm IoU chính thức.
- Plates: pseudo được Triệu xác nhận 3/3 đúng loại, bao trọn đĩa. Review gốc Trí ghi 0/3 được giữ nguyên như lịch sử. Plates/rulers/raspberries có mẫu đúng 3/3 nhưng final vẫn sai/thừa.
- Tổng số pseudo đúng loại theo bảng review chốt: 23/42 (14 query có 3 mẫu, chairs không có mẫu). Đây là phân loại định tính của review, không phải precision/recall định vị hoặc 42 mẫu đều được hai người phân xử độc lập.
- q04_2 blueberries: final 32 = 24 blueberry + 7 blackberry + 1 red currant theo bản chốt; chênh lệch 35/32 đã được giải quyết. 10 điểm blackberry trong nguồn khác với 7 quả nhìn thấy theo review; giữ dữ liệu nguồn, không đổi GT mục tiêu blueberries=24.
- q05_2 raspberries: final 14 = 4 quả mục tiêu + 1 khung trùng + 9 khung sai loại. Triệu chốt lỗi trùng/sai loại; các nhận xét cũ của assistant về “bao một phần” không tự trở thành nhãn đã được Triệu xác nhận.
- q02_1 plates: bản chốt ghi phần đối sánh bổ sung của assistant, stage 1 = 15 nhóm đĩa + 10 khung dư do trùng + 3 sai loại; final = 15 nhóm đĩa + 13 dư trùng + 3 sai loại. Một số nhóm chắc chắn vừa. Ngày 21/10 đã bổ sung [bản chi tiết](<../workspace Trí and Triệu/Triệu/Q02_1_DETAILED_REVIEW.md>), ba JSON và ảnh bằng chứng từ cuộc trò chuyện Triệu ngày 19/10; bản sao khớp hash nguồn, không xem mọi nhóm đã được Triệu phân xử.
- Blackberries 21→79: có sai loại và đếm phần quả; chưa phân loại đủ 79 khung để lượng hóa mọi cơ chế.
- Chairs GT=1 nhưng trả 0; bowls có bỏ sót một bát theo review. Đây là ca lớp có mặt, không phải truy vấn absent.

[Nhãn hậu kiểm q05_2 ngày 16/10](../results/countgdpp/b2_remaining3_20261015/q05_2/manual_crosscheck_20261016.json) vẫn dùng cho phép kiểm số khung/lớp/vật trong evaluator. Phép kiểm không chấm hoặc xác nhận các cờ phần vật; ghi nguồn/giới hạn theo review mới ở trên.

## 5. Đối chứng ngưỡng và giới hạn

E1 thay ngưỡng cuối với mẫu cố định; E2 thay ngưỡng mẫu giữ cuối=.23, chỉ trên 2 ảnh/6 query. E2 chạy .10/.23/.50; .35 bỏ qua có lý do từ điểm top-3, không báo là đã chạy. Chưa E3, train hoặc cải tiến mới. [E1](../results/countgdpp/m6_e1_final_20261015/REVIEW.md) · [E2](../results/countgdpp/m6_e2_sample050_20261015/REVIEW.md).

5 ảnh chưa đại diện toàn benchmark. Nhãn đếm có từ gói nguồn nhưng xuất xứ/giấy phép và toàn bộ định vị chưa được xác minh đầy đủ. Chưa có absent/holdout trong pilot; benchmark tài nguyên chuẩn còn chờ. Nhánh FSCD-147 Kaggle đã xác nhận count metrics ngày 20/10 trong báo cáo riêng; không suy rộng kết quả đó sang phép thử X/Y của pilot. Chưa tìm ra nguyên nhân nội tại kiến trúc từ các quan sát này.

## 6. Kế hoạch sang P4 — đề xuất chờ nhóm duyệt

**Đích thử tiếp:** giảm khung sai loại khi thay query X/Y, kể cả lúc pseudo đúng loại. Giữ CountGD++ làm model nền; CLIP được đề xuất làm bước kiểm tra crop–văn bản sau dự đoán B2. Chưa chọn phương pháp cuối, chưa chạy thử hoặc có bằng chứng hiệu quả.

**Cơ sở:** CLIP học liên hệ ảnh và mô tả văn bản, hỗ trợ chuyển sang tác vụ mới bằng mô tả lớp. Việc dùng nó lọc khung B2 là giả thuyết của kế hoạch này; bài gốc không xác nhận hiệu quả trên pilot CS331. [Radford et al., ICML 2021](https://proceedings.mlr.press/v139/radford21a.html).

### 6A. Phép thử nhỏ được đề xuất

1. Giữ nguyên ảnh/query, checkpoint và dự đoán B2 đã lưu; crop từng khung trong tọa độ ảnh gốc, lưu ID khung để truy vết.
2. Bản đầu chỉ so crop với mô tả **loại đang được hỏi**. Chuẩn hóa embedding ảnh/văn bản rồi tính độ tương đồng cosine; score này không được gọi là xác suất đúng lớp đã hiệu chỉnh. Chọn quy tắc crop, prompt và ngưỡng trên dev, ghi cấu hình trước khi dùng cho tập khác.
3. Giữ/loại khung theo score, đếm lại phần giữ. Không sửa bbox, GT, dự đoán gốc hoặc đồng thời thêm NMS trong phép thử đầu.
4. Có thể kiểm khả thi trên q03_2 rulers và q05_2 raspberries (cả hai có pseudo đúng 3/3 nhưng final sai loại). Chúng là case dev đã xem, không phải holdout và không dùng riêng hai ca để tuyên bố cải thiện toàn tập.

**Nguồn tên lớp dễ nhầm:** chưa dùng trong bản thử tối thiểu. Nếu sau này bổ sung, phải dùng danh mục cố định từ dev hoặc bộ đề xuất tự động chỉ nhận ảnh/query và báo rõ nguồn. Không lấy lớp hiện diện/GT của ảnh test để chọn negative labels; cấu hình có thông tin bổ sung phải được công bố riêng.

### 6B. Đối chứng và cách đo

- Giữ bảng B0 và B2 hiện có để tham chiếu. So trực tiếp **B2 gốc**, **B2 chỉ lọc thêm theo confidence của CountGD++**, **B2 + bộ lọc CLIP**, trên cùng ảnh/query và cùng nguồn khung B2. Đối chứng confidence được chọn trên dev, không điều chỉnh theo kết quả holdout.
- Ngoài MAE/RMSE, báo số vật mục tiêu phân biệt còn giữ, số vật đúng mất hết khung sau lọc, số khung sai loại bị loại và khung trùng còn lại. Báo cả tử/mẫu số hoặc số lượng trước/sau; count giảm chưa đủ để kết luận tốt hơn.
- Với phép thử khung đã lưu, cần nhãn từng khung gồm loại, object_id/nhóm cùng vật và mức chắc chắn. Nhãn dùng cho evaluator; không đưa vào bộ lọc. q05_2 đã có nhãn để khởi đầu; các ca khác cần kiểm đủ theo phạm vi đã chọn.
- Khi đánh giá định vị rộng hơn, chuẩn bị nhãn vị trí và khóa quy tắc matching trước; không tự gọi các số kiểm thủ công là AP/IoU benchmark.
- Bộ lọc chỉ loại bớt khung đã có nên không thể tìm lại chiếc ghế mà B2 không phát hiện. Bỏ sót/sai đơn vị đếm cần theo dõi, chưa phải vấn đề được phép thử này giải quyết đầy đủ.

### 6C. Bốn mục cần thống nhất trước lần chạy P4

- [ ] Phạm vi: thử bộ lọc sau B2, chỉ ảnh + query; baseline và đối chứng như mục 6B.
- [ ] Checkpoint CLIP cụ thể, nguồn/hash; quy tắc crop/prompt/score và cách chọn ngưỡng trên dev.
- [ ] Danh sách case dev, nhãn/object_id, cách tính giữ đúng/loại sai. Chia theo ảnh gốc; chưa mở holdout khi đang chọn cấu hình. Nếu chưa có holdout hợp lệ thì kết luận giới hạn ở dev.
- [ ] Người thực hiện và người kiểm: đề xuất Trí chuẩn bị prototype/cấu hình; Triệu kiểm nhãn/evaluator. Chưa tự ghi nhóm đã nhận hoặc duyệt phân công.

**Quyết định đề xuất:** đóng vòng pilot sau kiểm chéo và duyệt báo cáo, rồi chuyển sang **chuẩn bị P4**. Bản kế hoạch trên chưa phải phương pháp mới đã chứng minh; không yêu cầu train lại CountGD++ cho phép thử này. Tính mới cần đối chiếu công trình liên quan nếu muốn trình bày như đóng góp nghiên cứu.

## 7. Phiếu xác nhận của nhóm — chỉ điền sau khi thực sự kiểm

**Kiểm được ủy quyền ngày 24/10:** assistant đã làm hộ phần kỹ thuật theo yêu cầu Triệu đang ưu tiên deadline paper; [báo cáo và bằng chứng](TRIEU_KET_QUA_KIEM_CHEO_20261024.md). 15 dòng, bốn ca minh họa, metric, q05_2 và logic null đã đối chiếu; không chạy evaluator/model. Ghi nhận đúng người kiểm kỹ thuật là assistant; xác nhận đọc/chấp nhận của Triệu đã có bên dưới, duyệt nhóm vẫn chờ.

Audit artifact/code của assistant: **20/10/2026, đạt trong phạm vi file pilot đã lưu**. Các ô dưới đây dành cho nhóm; không dùng xác nhận assistant để tự ghi Triệu đã kiểm hoặc nhóm đã đồng ý dùng CLIP.

Hỗ trợ đọc/kiểm chéo ngày 21/10: xem [bốn điểm code, bốn dòng nguồn và q05_2](TRIEU_EVALUATOR_CROSSCHECK_20261021.md). Đối chiếu đủ 15 dòng khớp; hash checkout Windows được giải thích theo byte/EOL. Bản hỗ trợ này chưa thay việc Triệu tự đọc và xác nhận các ô dưới đây.

- [x] Triệu đã đọc, hiểu và đồng ý dùng bản kiểm kỹ thuật ngày 24/10 do assistant thực hiện. Phạm vi là chấp nhận kết quả kiểm được ủy quyền; không ghi Triệu đã tự kiểm code/nguồn.
- Người xác nhận: **Triệu — 24/10/2026**. Xác nhận trực tiếp: “Tôi đã đọc và hiểu bản kiểm ngày 24/10, đồng ý dùng kết quả kiểm kỹ thuật do assistant thực hiện.” [Bản ghi xác nhận](audits/TRIEU_ACCEPTANCE_20261024.json).
- [x] **Triệu tự kiểm chéo Phần 2 — 27/10/2026.** Lần này Triệu tự chạy self-test và evaluator, tự tính lại MAE/RMSE, truy ngược q05_3 về predictions, tự gán nhãn 14 box q05_2 trước khi mở nhãn cũ, và thử 5 ca dữ liệu hỏng; assistant chỉ hướng dẫn. Kết quả khớp run 20/10. [Báo cáo tự kiểm và bằng chứng](TRIEU_TU_KIEM_PHAN2_20261027.md). Kết luận của Triệu, nguyên văn: “Đã check lại metric, q05_3 và tự gán nhãn lại q05_2, check thử đưa dữ liệu hỏng vào thì xảy ra chuyện gì đối với evaluator. Ở q05_2 thì box 12 với [13] chấm khác với nhãn cũ, cũng tùy vào người chấm cũng như máy chấm thì khác nữa, quan điểm mỗi người thôi, theo tôi thì 2 box đó đã làm tốt việc của mình. Nên ghi rõ ở q05_3, thực chất B2 kém hơn B0 thì cũng tùy trường hợp nữa chứ không thể ghi tổng quát như vậy được, các số liệu đó ghi vào báo cáo được đó.” Phạm vi đồng ý: dùng số liệu Phần 2 (MAE/RMSE, 6/4/5, coverage, q05_2) kèm lưu ý độ nhạy ở mục 3. Bản 24/10 phía trên giữ làm lịch sử.
- Nhóm duyệt nội dung pilot: **[CHƯA DUYỆT — tên/ngày]**.
- Quyết định pilot: **[đóng vòng pilot để chuẩn bị P4 / còn sửa mục ...]**.
- Quyết định ứng viên P4: **[thử CLIP theo phạm vi mục 6 / cần chỉnh giả thuyết]**.
- Đã chốt bốn mục 6C trước thực thi: **[CHƯA]**.

Tại lượt cập nhật 21/10 đã thấy score CLIP và báo cáo khảo sát P4 trong repo; chưa audit toàn bộ hoặc xác nhận hiệu quả/duyệt P4 tại lượt này. Không tiếp tục coi “chưa có artifact CLIP” là trạng thái hiện tại. Sau khi có xác nhận nhóm, cập nhật [WORKLOG](../WORKLOG.md), [ROADMAP](../roadmap/ROADMAP.md) và [HANDOFF](../HANDOFF/HANDOFF.md).
