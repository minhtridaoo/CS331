# BÁO CÁO ĐÁNH GIÁ CHỦ ĐỀ VÀ CÁC VẤN ĐỀ CỦA ĐỒ ÁN CS331

**Ngày đánh giá:** 07/10/2026  
**Tài liệu được đánh giá:** `CS331_ZSC_V3_4_Final.md`, nội dung phiên bản V3.4.1  
**Quy mô nhóm:** 2 thành viên, đã xác nhận  
**Thời gian dự kiến:** 6 tuần  
**Tên đề tài:** *Evaluating and Improving Target Sensitivity in Text-Guided Zero-Shot Object Counting*

Báo cáo này tổng hợp đánh giá về mức độ phù hợp của chủ đề, sáu vấn đề đã được góp ý và hướng xử lý đề xuất. Đây là báo cáo review; các lựa chọn đề xuất dưới đây chưa phải thay đổi đã thực hiện trong mã nguồn hoặc thí nghiệm. Những nhận xét về code được kế thừa từ tài liệu đính kèm, chưa được kiểm tra lại trên repository trong lần review này.

## 1. Đánh giá tổng thể về chủ đề và hướng nghiên cứu

**Chủ đề đủ cơ sở để báo và thảo luận chốt với giảng viên ở mức đồ án môn học cho nhóm 2 người. Tuy nhiên, protocol V3.4.1 cần làm rõ một số điểm trước khi chạy thí nghiệm chính.**

Câu chuyện nghiên cứu tương đối rõ: mô hình có thể đếm tốt trên ảnh chủ yếu chứa một lớp nhưng chưa chắc chọn đúng đối tượng được chỉ định bằng văn bản. Nhóm dùng CLIP-Count làm mô hình nền, fine-tune với cross-class mosaic supervision, sau đó kiểm tra trên ảnh đa lớp thật và đánh giá hiệu quả khi truy vấn được viết lại cùng nghĩa. Hướng này phù hợp với vấn đề text sensitivity và semantic grounding được T2ICount và PrACo++ quan tâm [1], [2].

Điểm mạnh của kế hoạch là có checkpoint official E0, có đối chứng fine-tune E0-ft và có can thiệp E2. Nhờ vậy, nhóm có thể phân biệt ảnh hưởng của việc học thêm với ảnh hưởng của cross-class mosaic. Việc giữ cùng lượng mosaic và khoảng crop giữa control/can thiệp cũng giúp giảm biến gây nhiễu về augmentation và kích thước vật thể.

MUCCA được chọn làm bằng chứng chính là hợp lý: đây là ảnh đa lớp thật, giúp kiểm tra khả năng chọn target vượt ra ngoài bố cục mosaic tổng hợp. Kết quả tốt trên PrACo mosaic vẫn hữu ích nhưng gần phân phối huấn luyện của E2, nên chưa đủ để kết luận mô hình grounding tốt hơn trong cảnh thật [2].

Hạn chế lớn nhất hiện tại nằm ở cách kiểm chứng, không phải chủ đề: liều can thiệp có thể nhỏ, tiêu chí checkpoint chưa nhất quán và kết quả chính qua hai seed chưa được định nghĩa. Đóng góp cũng cần được trình bày đúng mức: một nghiên cứu can thiệp có đối chứng và phân tích robustness, không phải phát minh mosaic hoặc một kiến trúc mới.

## 2. Vấn đề 1 — Liều can thiệp có thể quá thấp

### Nhận xét

Cảnh báo này có cơ sở. Trong V3.4.1, α chỉ được áp dụng sau khi mẫu vào nhánh mosaic và ảnh nguồn có dưới 70 point. Tần suất out-mosaic trên toàn bộ mẫu train có thể ước lượng:

\[
P(\mathrm{out\text{-}mosaic})\approx 0.3\times\alpha\times P(N<70).
\]

Vì vậy, α=1 không có nghĩa 100% mẫu train được cross-class supervision. Con số khoảng 20% được nêu trong góp ý chỉ là ước lượng thô, cần đo từ dữ liệu và pipeline thực tế.

Ngoài ra, ảnh phụ hiện được lấy ngẫu nhiên nên có thể cùng nhãn target. **Out-mosaic không đồng nghĩa mosaic đa lớp.** Phần mẫu thật sự cung cấp tín hiệu phân biệt target với distractor có thể thấp hơn tần suất out-mosaic. Với LR khoảng 1e-5 và hai seed, hiệu ứng nhỏ có thể khó phân biệt với biến thiên của quá trình huấn luyện; kết quả không cải thiện cũng khó diễn giải nếu chưa biết liều thực tế.

### Hướng xử lý đề xuất

Ưu tiên sửa sampler để **ảnh phụ có nhãn FSC-147 khác nhãn target**, áp dụng cùng quy tắc cho E2 và E2-half. Đây là một sửa đổi nhỏ giúp bảo đảm khác nhãn nguồn, không cần thêm loss hoặc module mới. Mặc định vẫn giữ mosaic tổng 30% chung cho control và can thiệp.

Log theo epoch: tỉ lệ out-mosaic trên toàn bộ mẫu, tỉ lệ mosaic có nhiều nhãn nguồn, số ô khác target, tỉ lệ GT count bằng 0 và tỉ lệ fallback nếu không lấy được ảnh phụ hợp lệ. Cần ghi mẫu số rõ; không suy liều thực tế trực tiếp từ α.

**Khác nhãn nguồn vẫn không bảo đảm target vắng mặt.** Ví dụ ô nguồn có nhãn `cars` có thể chứa `people` chưa được gán nhãn. Do đó vẫn giữ audit 100 mosaic train; ngưỡng kích hoạt lọc cặp phải được đặt trước khi audit, và nếu sửa sampler từ mẫu A thì kiểm lại bằng mẫu B mới. Không dùng kết quả test để chọn cặp cấm.

Nếu liều vẫn thấp, báo đây là giới hạn của can thiệp; mọi quyết định tăng tỷ lệ mosaic, nếu có, phải dựa trên train/dev trước khi khóa thiết kế và giữ các tham số augmentation chung khớp giữa control/can thiệp.

## 3. Vấn đề 2 — Tiêu chí chọn checkpoint có thể bất lợi cho E2

### Nhận xét

FSC-147 val MAE chủ yếu phản ánh sai số đếm thông thường, không trực tiếp tối ưu khả năng chọn đúng target trong ảnh nhiều lớp. Epoch có val MAE tốt nhất chưa chắc là epoch có target sensitivity tốt nhất; chọn bằng MAE có thể làm hiệu ứng grounding của E2 trông nhỏ hơn.

Tài liệu còn có mâu thuẫn cần sửa: §3 quy định checkpoint có FSC val MAE thấp nhất, trong khi §5 ghi FSC val cộng val-mosaic được dùng để chọn checkpoint. Nếu không làm rõ, nhóm có thể vô tình thay tiêu chí sau khi thấy kết quả.

### Hướng xử lý đề xuất

Giữ **primary checkpoint = best FSC-147 val MAE**, cùng quy tắc cho mọi cấu hình. Val-mosaic dùng để pilot, kiểm pipeline và theo dõi grounding, không tham gia chọn checkpoint chính.

Bổ sung **last epoch checkpoint** làm kiểm tra độ nhạy cho E0-ft/E2 ở cả hai seed, cùng số epoch huấn luyện. Báo bảng primary và bảng last riêng; không chuyển last thành kết quả chính sau khi xem test.

Theo dõi FSC val MAE và val-mosaic CntF1 theo epoch hoặc lịch đánh giá cố định. Nếu hai đường có xu hướng khác nhau, nhóm có dữ liệu để thảo luận sự khác nhau giữa counting accuracy và target sensitivity. Tuy nhiên, val-mosaic vẫn là dữ liệu tổng hợp, nên chưa thể tự suy ra training dynamics tương tự trên ảnh thật.

Việc thêm last checkpoint làm tăng chi phí đánh giá. Kế hoạch cũ có 6 primary checkpoint; cặp E0-ft/E2 với hai seed có thể thêm tối đa 4 last checkpoint khác primary. Nếu best trùng last thì không cần inference lại. Để giữ scope, kiểm tra last tối thiểu bằng FSC MAE/RMSE và MUCCA CntF1/MAE với prompt gốc; chưa cần lặp toàn bộ paraphrase.

## 4. Vấn đề 3 — Chưa định nghĩa cách gộp hai seed vào kết quả chính

### Nhận xét

V3.4.1 đã yêu cầu báo từng seed và paired CI theo ảnh nhưng chưa nói rõ delta chính được tính thế nào. Nếu để đến khi có kết quả mới quyết định, nhóm dễ bị xem là chọn cách tổng hợp có lợi.

Hai seed là mức ngân sách có thể dùng cho đồ án, nhưng quá ít để ước lượng tốt phân bố biến thiên do huấn luyện. Bootstrap ảnh và bootstrap seed trả lời hai loại uncertainty khác nhau, không thể thay thế nhau.

### Hướng xử lý đề xuất

Với metric M, tính delta trên từng cặp seed:

\[
\Delta_s=M(E2,s)-M(E0\text{-}ft,s).
\]

Con số chính là trung bình hai paired effects:

\[
\Delta_{\mathrm{main}}=\frac{\Delta_{s_1}+\Delta_{s_2}}{2}.
\]

Trong mỗi bootstrap replicate, lấy mẫu **ảnh có hoàn lại**, giữ tất cả query/patch của cùng ảnh trong một nhóm và dùng cùng tập ảnh lấy mẫu cho cả cấu hình lẫn hai seed. Tính lại metric cho từng run, tính delta từng seed, rồi lấy trung bình hai delta. Với metric phi tuyến như CntF1 hoặc RMSE, phải tính lại theo phép tổng hợp của evaluator, không tùy ý thay bằng trung bình delta query.

CI này phản ánh uncertainty do lấy mẫu ảnh, **có điều kiện trên hai run đã train**; không được diễn giải là CI của training-seed variability. Báo thêm delta từng seed để người đọc thấy hai run có nhất quán về chiều tác động hay không. Không ưu tiên hierarchical bootstrap seed×image với chỉ hai seed.

Không lấy trung bình predicted count/density qua hai seed rồi mới tính metric làm con số chính: cách đó đánh giá ensemble thay vì tác động trung bình của can thiệp qua các run độc lập.

## 5. Vấn đề 4 — Đóng góp về phương pháp còn mỏng

### Nhận xét

Cảnh báo đúng nếu nhóm trình bày đóng góp là “đề xuất mosaic cho zero-shot counting”. CounTR đã có pipeline tổng hợp ảnh từ nhiều semantic category; MGCAC kết hợp mosaic với generalized loss để xử lý việc đếm vật thể trội; CountGD++ cũng có training pipeline liên quan mosaic [3]–[5]. PrACo++ đã đánh giá CLIP-Count, nên chỉ chạy lại benchmark chưa đủ để tạo đóng góp rõ [2].

Tuy vậy, điều này không làm đề tài mất giá trị ở mức đồ án môn học. Đóng góp có thể nằm ở câu hỏi được kiểm chứng, thiết kế đối chứng, chất lượng thực nghiệm và phân tích giới hạn. Việc thêm module chỉ để trông mới hơn có thể làm vỡ lịch mà không tăng chất lượng nghiên cứu.

### Hướng xử lý đề xuất

Định vị đề tài là:

> Một nghiên cứu can thiệp có đối chứng trên CLIP-Count nhằm kiểm tra tác động của cross-class supervision đến target sensitivity, trade-off với counting thông thường và độ bền khi truy vấn được diễn đạt lại cùng nghĩa.

Phần đóng góp nên nêu gồm: matched fine-tuning control; sampler khác nhãn có audit chất lượng supervision; đánh giá grounding trên ảnh đa lớp thật; đánh giá paraphrase tách count stability khỏi target correctness; báo paired seed effects và checkpoint sensitivity.

Cross-label sampler là sửa đổi kỹ thuật nhỏ để làm can thiệp rõ hơn, không nên nhận là phương pháp hoàn toàn mới. Khảo sát α giúp hiểu mức can thiệp, nhưng tự nó cũng không phải novelty lớn. Không tuyên bố “chưa ai làm” hoặc “nghiên cứu đầu tiên” khi chưa có khảo sát đầy đủ. RichCount là một nguồn cần đối chiếu về rich prompts/alignment khi viết related work [6].

Không khuyến nghị thêm consistency loss, backbone, adapter hoặc spatial gate trong scope hiện tại. Nếu giảng viên yêu cầu đóng góp phương pháp mới ở mức paper, nhóm cần chốt tiêu chí đó sớm thay vì mở rộng vào cuối lịch.

## 6. Vấn đề 5 — Khối lượng tuần 1–2 bị dồn

### Nhận xét

Tuần 1 của kế hoạch hiện tại gồm báo thầy, dựng Colab, tái lập E0, cài hai evaluator và đo GPU-hours. Tuần 2 gồm vá augmentation, kiểm density, audit 100 mosaic, smoke fine-tune và dựng prompt. Phạm vi này có rủi ro trễ mốc khóa cuối tuần 3, nhất là khi môi trường hoặc wrapper có lỗi.

### Hướng xử lý đề xuất

**Tuần 1:** ưu tiên E0, môi trường, PrACo chạy được, schema kết quả và runtime. MUCCA chỉ cần smoke test một số ảnh với E0 hoặc dữ liệu giả lập để kiểm format/pipeline; đo GPU-hours training/evaluation là đầu ra bắt buộc. Không dùng metric/lỗi của smoke test MUCCA để chọn sampler hoặc prompt.

**Tuần 2:** hoàn thiện MUCCA evaluator; người phụ trách training vá sampler/crop/log và smoke fine-tune; người phụ trách evaluation hoàn thiện audit, prompt và metric. Kiểm density/count, local-vs-wrapper, save/resume phải xong trước run chính.

Giữ **cuối tuần 3 là mốc khóa thiết kế**, bộ prompt và K. Nếu trễ, cắt E2-half và phần mở rộng trước; giữ cặp E0-ft/E2 và đánh giá ảnh thật. Tính ngân sách cả validation, primary/last, paraphrase và lưu density; không chỉ tính giờ train.

## 7. Vấn đề 6 — Số thành viên trong nhóm

### Nhận xét và cập nhật

**Nhóm có 2 người, đã xác nhận.** Vì vậy, giả định làm song song trong kế hoạch là phù hợp và vấn đề “chưa chốt số người” đã được giải quyết. Cần sửa tiêu đề §12 đang ghi “nhóm 2 người, chưa xác nhận số người”.

Phân công định hướng:

| Thành viên | Phụ trách chính |
|---|---|
| Người A | Môi trường, patch training/sampler, fine-tune, checkpoint và training log |
| Người B | Dữ liệu/split, evaluator, bộ prompt, thống kê, bảng và hình |
| Cả hai | Audit leakage, khóa protocol, kiểm tra chéo, related work, phân tích và báo cáo |

Hai người giúp giảm thời gian công việc kỹ thuật nhưng không làm tăng ngân sách GPU hoặc số seed. Mỗi thành viên cần hiểu thiết kế chung; không nên để một người chỉ biết train và người còn lại chỉ biết làm bảng.

## 8. Lỗi trình bày cần sửa

- Cột “Seed” tại §3 đang chứa số lượng seed nhưng dễ bị hiểu là seed ID. Nên tách “Số seed” và “Seed ID”; E0 không có lượt train mới.
- Changelog có dòng 7a đứng trước dòng 7. Cần đánh số liên tục hoặc ghi rõ đây là bổ sung lịch sử.
- Thống nhất vai trò val-mosaic: pilot/diagnostic, không phải tiêu chí chọn checkpoint chính theo đề xuất của báo cáo này.
- Xóa ghi chú “chưa xác nhận số người” và ghi rõ nhóm 2 thành viên.

## 9. Kết luận và thứ tự ưu tiên xử lý

**Giữ chủ đề và hướng nghiên cứu hiện tại.** Trước khi chạy chính, ưu tiên bốn thay đổi: cross-label auxiliary sampler kèm audit; thống nhất best-val-MAE primary và last-epoch sensitivity; định nghĩa mean paired seed delta cùng image bootstrap; điều chỉnh tuần 1–2 để runtime được đo sớm và MUCCA hoàn thiện ở tuần 2.

Đồng thời, sửa cách trình bày đóng góp và ghi nhận nhóm 2 người. Sau các điều chỉnh này, thiết kế có cơ sở hơn để triển khai trong 6 tuần mà không cần thêm loss, backbone hoặc benchmark mới.

Nếu kết quả không cải thiện, cần báo liều thực tế, chất lượng nhãn, delta từng seed, checkpoint sensitivity và trade-off. Kết quả âm vẫn có giá trị khi thí nghiệm đúng và được báo đầy đủ; CI chứa 0 không tự chứng minh can thiệp không có tác dụng. Việc chấp nhận đề tài cuối cùng và yêu cầu novelty vẫn cần đối chiếu với tiêu chí của giảng viên.

## 10. Nguồn tham khảo

Tài liệu nội bộ được review: `CS331_ZSC_V3_4_Final.md` (V3.4.1) và sáu góp ý đã cung cấp trong cuộc trao đổi. Các nguồn công khai hỗ trợ phần định vị nghiên cứu:

[1] *T2ICount: Enhancing Cross-modal Understanding for Zero-Shot Counting*. https://arxiv.org/abs/2502.20625

[2] *Does it Really Count? Assessing Semantic Grounding in Text-Guided Class-Agnostic Counting* — PrACo++/MUCCA. https://arxiv.org/abs/2605.02752

[3] *CounTR: Transformer-based Generalised Visual Counting*. https://arxiv.org/abs/2208.13721

[4] *A Recipe for CAC: Mosaic-based Generalized Loss for Improved Class-Agnostic Counting*. https://arxiv.org/abs/2404.09826

[5] Repository *CountGD++: Generalized Prompting for Open-World Counting*. https://github.com/niki-amini-naieni/CountGDPlusPlus

[6] *Expanding Zero-Shot Object Counting with Rich Prompts* — RichCount. https://arxiv.org/abs/2505.15398
