# Tổng kết pilot CS331 — CountGD++ và lỗi chọn đối tượng

**BẢN NHÁP cập nhật 20/10/2026.** Số liệu pilot giữ từ run 15/10; review Triệu chốt v1 ngày 19/10 đã đọc lại ngày 20/10. Evaluator đã chạy và được đối chiếu ngày 20/10/2026; chưa coi báo cáo được nhóm duyệt.

**Pilot là bộ thử nhỏ 5 ảnh/15 câu hỏi để tìm lỗi.** Đây là file hoàn thiện ở phần 3, sau khi chạy evaluator ở phần 2. Nhánh benchmark 1.190 ảnh đã có [báo cáo riêng](BENCHMARK_FSCD147.md), không thay thế việc xác nhận các ô dưới đây.

## 1. Thông tin bạn tự điền

- Người chạy evaluator: **Minhtri**
- Ngày chạy: **20/10/2026**
- Self-test: **PASS theo xác nhận Minhtri trong handoff — `python3 evaluation/evaluate_pilot.py --self-test`**; chưa có stdout riêng, assistant không chạy lại self-test.
- Thư mục evaluator thực tế: **results/countgdpp/pilot_eval_20261020/**
- Coverage/IDs đã kiểm: **15/15 B0 và B2; 0 error, 0 uncertain; paired=15**
- Audit artifact/code: **assistant ngày 20/10 đã đối chiếu trực tiếp đủ 15 dòng, metrics, manual_check và hash nguồn**; không thực thi evaluator/model.
- Người kiểm chéo của nhóm/ngày: **Triệu chưa xác nhận kiểm evaluator mới**; review định tính đã chốt ngày 19/10 là công việc khác.
- Trạng thái báo cáo: **CHỜ KIỂM CHÉO VÀ DUYỆT**

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

**Xác nhận sau phần 2:** Run `results/countgdpp/pilot_eval_20261020/`; B0 và B2 đều có 15/15 query hợp lệ, 0 error, 0 uncertain. Hai bên ghép chung 15 query. MAE/RMSE và exact_count khớp bảng tham chiếu. Hậu kiểm q05_2 cũng khớp. Có đủ 5 file output. Cả 7 hash nguồn trong run_config khớp file hiện tại. Run `_r2` có cùng 4 file kết quả và cùng hash nguồn; chỉ khác tên output trong command, không coi là mẫu thí nghiệm độc lập. Chưa có xác nhận kiểm chéo evaluator mới của Triệu.

## 4. Bằng chứng định tính và kiểm chéo

**Trí và Triệu đều đã review định tính 15/15 query.** Nguồn hiện hành: [TRIEU_VISUAL_REVIEW.md — chốt v1 ngày 19/10](<../workspace Trí and Triệu/Triệu/TRIEU_VISUAL_REVIEW.md>), đọc lại tại workspace ngày 20/10. Bản [đối chiếu ngày 16/10](../results/countgdpp/b2_remaining3_20261015/TRIEU_CROSSCHECK_2026-10-16.md) là lịch sử; các ghi chú còn thiếu guitar/q04_2 trong bản đó đã được cập nhật bởi review mới.

- Guitar: theo quy ước Triệu xác nhận, ca không nêu lỗi là đã xem và thấy đúng; stage 1, pseudo và final được chốt đúng định tính. Không coi đây là chấm IoU chính thức.
- Plates: pseudo được Triệu xác nhận 3/3 đúng loại, bao trọn đĩa. Review gốc Trí ghi 0/3 được giữ nguyên như lịch sử. Plates/rulers/raspberries có mẫu đúng 3/3 nhưng final vẫn sai/thừa.
- Tổng số pseudo đúng loại theo bảng review chốt: 23/42 (14 query có 3 mẫu, chairs không có mẫu). Đây là phân loại định tính của review, không phải precision/recall định vị hoặc 42 mẫu đều được hai người phân xử độc lập.
- q04_2 blueberries: final 32 = 24 blueberry + 7 blackberry + 1 red currant theo bản chốt; chênh lệch 35/32 đã được giải quyết. 10 điểm blackberry trong nguồn khác với 7 quả nhìn thấy theo review; giữ dữ liệu nguồn, không đổi GT mục tiêu blueberries=24.
- q05_2 raspberries: final 14 = 4 quả mục tiêu + 1 khung trùng + 9 khung sai loại. Triệu chốt lỗi trùng/sai loại; các nhận xét cũ của assistant về “bao một phần” không tự trở thành nhãn đã được Triệu xác nhận.
- q02_1 plates: bản chốt ghi phần đối sánh bổ sung của assistant, stage 1 = 15 nhóm đĩa + 10 khung dư do trùng + 3 sai loại; final = 15 nhóm đĩa + 13 dư trùng + 3 sai loại. Một số nhóm chắc chắn vừa. File `Q02_1_DETAILED_REVIEW.md` được liên kết trong review chưa có ở workspace hiện tại; chưa coi bảng ghép chi tiết là artifact đã kiểm tại lượt này. Bổ sung nếu dùng bảng đó làm bằng chứng chi tiết.
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

Audit artifact/code của assistant: **20/10/2026, đạt trong phạm vi file pilot đã lưu**. Các ô dưới đây dành cho nhóm; không dùng xác nhận assistant để tự ghi Triệu đã kiểm hoặc nhóm đã đồng ý dùng CLIP.

- Triệu đã kiểm ghép ID/công thức/một vài dòng nguồn/q05_2: **[CHƯA XÁC NHẬN]**.
- Người kiểm, ngày và kết luận hoặc điểm phải sửa: **[Triệu điền]**.
- Nhóm duyệt nội dung pilot: **[CHƯA DUYỆT — tên/ngày]**.
- Quyết định pilot: **[đóng vòng pilot để chuẩn bị P4 / còn sửa mục ...]**.
- Quyết định ứng viên P4: **[thử CLIP theo phạm vi mục 6 / cần chỉnh giả thuyết]**.
- Đã chốt bốn mục 6C trước thực thi: **[CHƯA]**.

Hiện chưa có kết quả CLIP, E3, cải tiến hoặc holdout mới. Sau khi có xác nhận, cập nhật [WORKLOG](../WORKLOG.md), [ROADMAP](../roadmap/ROADMAP.md) và [HANDOFF](../HANDOFF/HANDOFF.md).
