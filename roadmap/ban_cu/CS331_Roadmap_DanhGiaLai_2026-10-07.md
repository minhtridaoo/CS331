# Đánh giá lại roadmap CS331 V3.3.1

Ngày đánh giá: 07/10/2026. Nguồn chính: `CS331_ZSC_V3_3_Final.md`, code CLIP-Count local tại commit `ba57fd0`, bài báo gốc và evaluator công khai. Đây là đánh giá thiết kế và kiểm tra code tĩnh; chưa phải kết quả thực nghiệm GPU.

## Bổ sung sau khi nhận nguyên văn gợi ý của giảng viên

**Đánh giá theo đề gốc: roadmap có cơ sở và bám rõ nhất vào vấn đề thứ ba của thầy.** Đồ án có thể có giá trị nhờ tái lập, phân tích và can thiệp có kiểm soát; không cần tự đặt điều kiện phải có tính mới ngang một bài nghiên cứu để được tiếp tục.

| Gợi ý của thầy | V3.3 đang làm gì | Kết luận được phép hướng tới |
|---|---|---|
| Học theo GT density nhưng đếm cả vùng/đối tượng không liên quan | Mosaic tạo giám sát có chọn lọc theo target | Kiểm tra giả thuyết về thiếu giám sát phân biệt lớp; chưa chứng minh density map là nguyên nhân và chưa loại bỏ nhu cầu density GT |
| Grounding DINO xác định đúng nhưng VA-Count đếm sai vùng | Chẩn đoán Grounding DINO/exemplars/density ở §38–41 | Phân tích lỗi theo giai đoạn; chuyển sang CLIP-Count không đồng nghĩa đã sửa lỗi VA-Count |
| Cùng ảnh, hỏi X và Y nhưng vẫn đếm như nhau dù target khác | Cross-class mosaic và đánh giá target sensitivity | Đây là mục tiêu chính, trực tiếp nhất của roadmap |

Prompt robustness là phần nhóm bổ sung. Nó hợp lý khi được dùng để kiểm tra rằng phương pháp chọn đúng target vẫn ổn định với diễn đạt tương đương. Trong thứ tự triển khai, ưu tiên selective counting trước, consistency sau. Nếu giữ cả hai là contribution ngang nhau như tên hiện tại, các đối chứng và đánh giá kết hợp nêu trong bản review vẫn cần thiết.

### Làm rõ gợi ý về density map

Việc dùng GT density để học tự nó không phải lỗi. Giả thuyết phù hợp để kiểm tra là: khi mỗi ảnh chỉ giám sát một lớp, mô hình có thể học đếm nhóm vật nổi bật và sử dụng text chưa đủ. Đó là một khả năng cần thực nghiệm, không phải nguyên nhân đã được chứng minh cho mọi mô hình.

Một vấn đề riêng là dùng ngưỡng trên density để tạo nhãn vùng foreground/background. T2ICount §3.3 phân tích giới hạn đó và dùng tín hiệu cross-attention để phân biệt vùng dương, âm và chưa chắc chắn. V3.3 không trực tiếp khảo sát cách dựng density hay thay thế density supervision. [T2ICount, §3.3](https://arxiv.org/html/2502.20625v3#S3.SS3)

Nếu muốn khẳng định mosaic cải thiện nhờ giám sát chọn lớp, cần kiểm soát hoặc ghi nhận các thay đổi đi kèm về crop, scale và phân bố số lượng. So sánh giữ nguyên số epoch là cần thiết nhưng chưa tự loại mọi yếu tố gây nhiễu.

### Chẩn đoán VA-Count đúng với vấn đề thầy nêu

VA-Count gồm phát hiện ứng viên, lọc/chọn exemplars và bộ đếm dựa trên exemplars. [VA-Count, §3](https://arxiv.org/html/2407.04948v1#S3)

Với các ảnh chẩn đoán chọn trước, lưu đầu ra của từng giai đoạn: box Grounding DINO, exemplar thật sự được đưa vào counter, density dự đoán và GT theo target. Khi đổi query, phải cập nhật các đầu vào phụ thuộc query; tránh vô tình dùng lại exemplars của query trước.

Đếm số box và đo precision/recall của detector là tham chiếu hữu ích, nhưng không đủ để xác định vì sao counter sai: VA-Count dùng một số exemplars làm mẫu, không yêu cầu detector tìm đủ mọi instance để rồi cộng box. Nếu có điều kiện, một đối chứng chẩn đoán mạnh là cấp exemplars đã được kiểm tra thủ công, giữ bộ đếm cố định. Phải báo riêng đây là diagnostic có hỗ trợ annotation, không phải kết quả zero-shot chính thức.

Nếu exemplars đúng mà density vẫn sai, bằng chứng hướng tới lỗi trong khâu suy rộng từ exemplar sang các vật trong ảnh; vẫn cần loại lỗi crop/tọa độ/preprocessing trước khi kết luận về mô hình.

### Thứ tự thực nghiệm đề nghị theo đề gốc

1. Kiểm chứng hiện tượng đổi target trên một bộ ảnh dev đa lớp: cùng ảnh, query X, query Y, và query lớp được xác minh là không có nếu có dữ liệu phù hợp. Đo count lẫn phân bố density. Hai lớp có cùng số lượng không bắt buộc phải cho count khác nhau.
2. Làm chẩn đoán VA-Count giới hạn để trả lời vấn đề giai đoạn grounding/exemplar/counting; không mở một nhánh huấn luyện đầy đủ thứ hai.
3. Chạy E0-ft so với E2 để kiểm tra can thiệp selective mosaic; đánh giá cuối trên ảnh thật sau khi khóa thiết kế bằng dev.
4. Khi pipeline ổn định, chạy E1-aug/E1/E3 để kiểm tra phần mở rộng về paraphrase. E1-aug vẫn cần nếu nhận đóng góp riêng từ consistency.

T2ICount cần được đối chiếu trong phần giải thích phương pháp vì thầy đã dẫn và bài nhắm trực tiếp vào text sensitivity. Chạy checkpoint làm tham chiếu nếu tài nguyên cho phép; không suy ra phải train lại cả ba mô hình thầy liệt kê. Đoạn gợi ý được cung cấp cũng chưa quy định nhóm phải giải quyết trọn vẹn cả ba thách thức.

Định vị phù hợp để trình bày với thầy: **nghiên cứu khả năng đếm đúng đối tượng theo truy vấn, ưu tiên vấn đề đổi X/Y; kiểm tra giám sát đa lớp bằng mosaic trên CLIP-Count; dùng chẩn đoán VA-Count để phân tích lỗi từng giai đoạn và dùng paraphrase để đánh giá tính ổn định của giải pháp.**

Các nhận xét kỹ thuật và protocol bên dưới vẫn có hiệu lực. Phần bổ sung này điều chỉnh thứ tự ưu tiên theo đề gốc, không xem paraphrase robustness là yêu cầu thầy đã nêu.

## Kết luận

**Giữ hướng nghiên cứu, nhưng cần chỉnh protocol trước khi gọi đây là bản chốt để chạy toàn bộ thí nghiệm.** Câu hỏi “ổn định khi đổi cách diễn đạt, chọn đúng khi đổi đối tượng” phù hợp với đồ án CS331. Giá trị có thể đến từ thực nghiệm có kiểm soát, phân tích lỗi và một bộ đánh giá tái lập được. Chưa có cơ sở bảo đảm E3 sẽ tốt hơn, hay khẳng định phương pháp có tính mới mạnh.

Ba vấn đề đáng ưu tiên nhất:

1. RichCount là related work trực tiếp của density-map consistency, cần đưa vào đối chiếu phương pháp.
2. §21.2 diễn giải sai đường đi của text trong visual encoder, dẫn đến nhận định chi phí chưa đúng.
3. Thiết kế prompt split, điều kiện dùng tập test và ablation chưa thống nhất với các kết luận dự kiến.

## Những điểm nên giữ

- Đánh giá đồng thời độ chính xác, độ ổn định với paraphrase và khả năng chọn đúng đối tượng. NPV thấp đơn độc không đủ chứng minh thành công.
- Giữ CLIP-Count làm nền cho nghiên cứu có kiểm soát; việc dùng một mô hình cũ có thể phù hợp nếu kết luận giới hạn đúng trên mô hình đó.
- Giữ E0-ft để phân biệt tác dụng của can thiệp với tác dụng của việc huấn luyện thêm.
- Giữ dữ liệu đa lớp thật để kiểm tra khả năng chuyển từ mosaic sang cảnh tự nhiên.
- Giữ cách trình bày trung thực rằng mosaic được kế thừa/kích hoạt/mở rộng, không tự nhận phát minh mosaic.
- Giữ phân biệt lớp chưa gặp trong huấn luyện counting với lớp chưa gặp trong CLIP pretraining.
- Các bẫy `overwrite_args`, giai đoạn contrastive thay density loss, số epoch và resume trong §61 phần lớn có căn cứ trong code đang kiểm tra.

## 1. Related work và tính mới cần viết lại

RichCount §3.2, phương trình (14), đã kết hợp density supervision với consistency giữa density maps của nhiều dạng đầu vào văn bản. Vì vậy cần xem đây là công trình liên quan trực tiếp tới `L_same`. [RichCount, §3.2](https://arxiv.org/html/2505.15398v2#S3.SS2)

Điểm khác có thể kiểm chứng của đồ án:

- Paraphrase bảo toàn đối tượng cần đếm và được tách khỏi phần dùng huấn luyện.
- Khảo sát consistency kết hợp selective mosaic supervision trên CLIP-Count.
- Đánh giá cả bất biến ngôn ngữ và khả năng phân biệt đối tượng, kể cả trên cùng một bộ truy vấn.
- Phân tích lợi ích, tác hại và giới hạn của từng thành phần.

Đây là cách định vị một nghiên cứu thực nghiệm có kiểm soát. Stop-gradient, L1 và việc kết hợp hai thành phần là khác biệt thiết kế; riêng những khác biệt đó chưa đủ chứng minh đóng góp phương pháp mới mạnh. Tránh câu “chưa bài nào…” ở §5 nếu chưa có khảo sát hệ thống.

**Đề nghị:** thêm RichCount vào §4, lập bảng so sánh input text, supervision, consistency, dữ liệu đa lớp và protocol paraphrase. Không cần tái triển khai toàn bộ RichCount chỉ để có đồ án hợp lệ.

## 2. Lỗi cụ thể ở §21.2: visual encoder không sử dụng text trong code hiện tại

Bằng chứng local:

- `models/clip_count.py:291` truyền `text_embedding` vào `deep_vpt_forward`.
- `models/clip_count.py:300` khai báo tham số `text_embdding`.
- Thân hàm ở dòng 301–334 không đọc tham số đó. Kiểm tra AST cho kết quả số lần đọc bằng 0.
- Text được sử dụng ở phần tương tác ảnh–văn bản/decoder.

Vì vậy nhận định “visual encoder nhận text nên không thể tái sử dụng đặc trưng ảnh, bắt buộc hai forward đầy đủ” là sai với đường thực thi đang kiểm tra.

**Sửa:** có thể tính đặc trưng ảnh một lần rồi dùng cho hai nhánh prompt trong cùng bước huấn luyện. Khi suy luận nhiều prompt trên một ảnh cũng có khả năng tái sử dụng đặc trưng. Tuy nhiên, đây mới là khả năng về kiến trúc, chưa phải tối ưu đã cài đặt hay số đo tiết kiệm VRAM/thời gian.

Khi triển khai cần giữ computation graph tới VPT, xử lý dropout nhất quán giữa hai nhánh và không tái sử dụng đặc trưng đã cũ sau khi trọng số cập nhật. Không tự suy ra rằng đóng băng CLIP đồng nghĩa toàn bộ visual path có thể chạy `no_grad`, vì VPT còn được học.

Một bẫy liên quan: `CLIPCount.forward` mặc định `coop_require_grad=False`; dòng 195 bọc text encoder trong `torch.no_grad()`. Nhánh train q1 hiện đặt cờ này thành True. Nhánh q2 mới cũng phải cho phép gradient vào context token nếu dự định học CoOp qua consistency.

## 3. Prompt benchmark: phải tách train/dev/test và định nghĩa lại “unseen family”

§17 mới có template train/test, trong khi §14 cho phép thay prompt set dựa vào NPV của E0. Cần ghi rõ P0 và việc chọn prompt diễn ra trên tập phát triển; nếu dùng test để chọn bộ prompt thì đánh giá cuối không còn độc lập.

Quy trình đề nghị:

1. Định nghĩa tiêu chí ngôn ngữ: tự nhiên, giữ nguyên tập đối tượng, không thêm màu/vị trí/số lượng chưa có trong yêu cầu.
2. Tách các nhóm template gần nhau thành train/dev/test; loại trùng và gần trùng giữa các phần.
3. Dùng FSC-147 validation và prompt dev để đo pilot, chọn lambda, tỉ lệ mosaic và quy tắc chọn checkpoint.
4. Khóa prompt test, số prompt K, seed, tiêu chí lọc và cách tổng hợp metric trước đánh giá cuối.

**LLM-generated là nguồn sinh, không tự động là một họ ngôn ngữ mới.** LLM có thể sinh lại các mẫu A–D. Nếu chưa phân loại cấu trúc và loại gần trùng, gọi E là “held-out LLM-generated prompts”, không khẳng định unseen-family generalization.

Ngưỡng cosine 0.95 trong §17 là heuristic chưa được kiểm chứng. Cosine cao không bảo đảm density giống nhau; cosine thấp cũng không bảo đảm ngữ nghĩa tương đương. Dùng chất lượng ngôn ngữ, sai số dự đoán và kiểm tra nhánh gradient để đánh giá tín hiệu học.

Nếu các prompt tự nhiên cho NPV thấp trên dev, đó là kết quả cần ghi nhận. Có thể thu hẹp mục tiêu consistency; không nên liên tục tạo prompt kém tự nhiên chỉ để baseline thất bại.

## 4. Có xung đột giữa §9.7 và §36 về dùng tập test

§9.7 đề nghị thử bố cục 1×2 nếu E2 kém trên MUCCA/PairTally. §36 lại quy định MUCCA/PairTally là untouched final test. Dùng kết quả hai tập này để chọn bố cục là một quyết định mô hình dựa trên test.

**Sửa:** chọn bố cục/tỉ lệ/null sampling trên synthetic validation mosaics và FSC-147 validation. Nếu thật sự cần ảnh đa lớp tự nhiên để phát triển, phải tách trước một phần dev và phần test còn độc lập; khi đó kết quả không tương đương protocol toàn bộ benchmark.

Khác biệt cần ghi rõ: huấn luyện và kiểm tra đều dùng mosaic không tự động là rò rỉ dữ liệu nếu ảnh/lớp được tách đúng. Đó là hạn chế về mức độ đại diện của đánh giá, cần bổ sung ảnh thật. Việc chọn thiết kế sau khi nhìn test mới là vấn đề độc lập của phép đánh giá.

## 5. Nhãn tile âm không mặc nhiên sạch

§11.1 cho rằng lớp xa về ngữ nghĩa ít xuất hiện chung; đó không phải một bảo đảm hợp lệ. Hai lớp khác nghĩa vẫn thường cùng xuất hiện, ví dụ người và xe. Nhãn FSC-147 của ảnh chỉ mô tả lớp được gán nhãn, không xác nhận mọi lớp khác đều vắng mặt.

Rủi ro này áp dụng cả mosaic thường, không chỉ hard-pair hay null-mosaic. Chọn cặp cosine thấp là heuristic lấy mẫu; nó không chứng minh GT zero cho target trong tile phụ.

**Sửa:** giới hạn các can thiệp ban đầu, kiểm tra thủ công một mẫu mosaic train được chọn bằng quy tắc cố định, thống kê tile có target chưa gán nhãn và lưu ví dụ lỗi. Có thể dùng danh sách ảnh/cặp đã kiểm tra để giảm rủi ro. Tránh mô tả supervision này là hoàn toàn sạch nếu chưa xác minh.

## 6. Ablation cần thống nhất với đóng góp muốn khẳng định

§25 nói cần E1-aug để trả lời “consistency có hơn augmentation không”, nhưng §46 xếp nó là SHOULD HAVE và §52 cho cắt sớm.

**Nếu giữ consistency là đóng góp chính, E1-aug phải thuộc phạm vi chính.** Nếu cắt nó, giới hạn kết luận: chỉ báo hiệu quả của cấu hình đã thử, không khẳng định consistency có lợi ích riêng so với thay prompt khi huấn luyện.

| Cấu hình | Vai trò |
|---|---|
| E0 | Checkpoint official, mốc tham chiếu |
| E0-ft | Đối chứng huấn luyện thêm |
| E1-aug | Chỉ dùng paraphrase augmentation với GT |
| E1 | Chỉ dùng prompt consistency |
| E2 | Chỉ bật selective cross-class mosaic |
| E3 | Kết hợp mosaic và consistency |

E1-aug như roadmap là một baseline thực dụng nhưng không phải đối chứng “khác đúng một yếu tố”: E1 có thêm nhánh q2; E1-aug thay q1 bằng q2 trên một phần mẫu. Cùng epoch và batch không đồng nghĩa cùng FLOPs, số lượt xử lý prompt hoặc GPU-hours. Nên báo rõ kiểu ngân sách được giữ cố định và chi phí thực tế.

Chỉ bổ sung đối chứng sâu hơn khi cần cho kết luận:

- Muốn quy lợi ích cho consistency thay vì số nhánh/tín hiệu học: xét đối chứng hai nhánh đều học GT, không consistency.
- Muốn khẳng định consistency hơn augmentation trong cấu hình kết hợp: cần mosaic + augmentation để so với E3.
- Muốn nhận đóng góp từ phần “extend mosaic”: cần phân biệt bật nhánh nguyên bản với phần mở rộng cụ thể. Nếu chỉ bật nhánh có sẵn, mô tả đúng như vậy.

Không cần chạy mọi đối chứng mở rộng ngay. Điều quan trọng là phạm vi kết luận phải tương ứng với đối chứng đã có.

## 7. Phải kiểm tra hai yêu cầu trên cùng truy vấn

Scatter NPV trên FSC-147 và CntF1 trên một benchmark khác có giá trị tổng quan, nhưng chưa đủ chứng minh rằng mô hình vẫn chọn đúng target khi chính prompt bị diễn đạt lại.

**Đưa đánh giá kết hợp vào phần chính:** với cùng ảnh đa lớp, thay cách diễn đạt của từng target, rồi đo độ chính xác và khả năng phân biệt. Có thể dùng paraphrase-PrACo với số template cố định để giới hạn chi phí; bổ sung một phần ảnh thật nếu ngân sách cho phép.

PrACo++ dùng thông tin theo vùng để đánh giá confusion; chỉ so hai con số tổng có thể bỏ sót việc đếm nhầm vị trí. [PrACo++, §3.3](https://arxiv.org/html/2605.02752v2#S3.SS3)

Hai target có cùng số lượng vẫn có thể cho hai kết quả đếm bằng nhau một cách đúng. Vì vậy không dùng “count phải đổi khi target đổi” làm tiêu chí duy nhất. Cần xem sai số theo target và density/metric theo vùng.

## 8. PairTally INTRA là kiểm tra mở rộng, không nên là điều kiện thành công bắt buộc

PairTally có các trường hợp INTRA phân biệt bằng màu, kích thước và texture/shape. [PairTally, §5.3](https://arxiv.org/html/2509.13939v1#S5.SS3)

Điều này đòi hỏi khả năng hiểu thuộc tính, trong khi can thiệp chính của đồ án học từ tên lớp FSC-147. Bảo toàn “red apples” khi paraphrase một query vốn đã có thuộc tính là hợp lệ; tự thêm “red” vào “apples” khi dùng cùng GT là không hợp lệ. Hai trường hợp phải phân biệt rõ.

**Sửa phạm vi:** MUCCA và PairTally INTER phục vụ đánh giá chọn lớp. PairTally INTRA là kiểm tra khả năng chuyển sang yêu cầu chi tiết hơn; báo riêng và dùng phân tích giới hạn. Không khẳng định đã học attribute grounding chỉ từ class-level mosaic.

## 9. Các chi tiết triển khai và thống kê cần bổ sung

- `L_same` là self-distillation giữa hai nhánh dùng chung trọng số, với stop-gradient ở nhánh q1. Nó không phải một teacher độc lập đã được bảo đảm đúng.
- Nếu E1 không cải thiện, chỉ kết luận trong cấu hình/ngân sách đã thử. Không quy ngay nguyên nhân cho text encoder đóng băng nếu chưa có ablation kiểm chứng nguyên nhân.
- Chốt reduction của L1/MSE và đơn vị density trước khi chọn lambda. Code hiện tại scale density ×60. Ghi rõ mean theo pixel, theo mẫu và cách lấy k mẫu.
- `drop_last=False`: xử lý batch cuối có ít hơn k mẫu. Khi giảm batch và tăng accumulation, giữ tỉ lệ mẫu paraphrase trên effective batch theo quy tắc đã chọn.
- Lưu ảnh/crop giống nhau cho hai prompt trong consistency, tránh vô tình học cả bất biến với hai phép tăng cường ảnh khác nhau.
- `overwrite_args` hiện chỉ gán `self.args`. Kiểm tra cả hyperparameters được lưu trong checkpoint mới để tránh log/resume dùng cấu hình cũ.
- Checkpoint official chủ động bỏ tham số CLIP đóng băng ở `run.py:410–415`. Vì vậy không đòi mọi `missing_keys` bằng zero; cần phân biệt missing keys dự kiến với phần trainable bị mất ngoài ý muốn.
- Kiểm tra checkpoint của một cấu hình trong cả inference local và wrapper PrACo trên cùng ảnh/prompt. Chốt quy tắc resize, padding, sliding window và density scale.
- PrACo có lựa chọn filtered/unfiltered checkpoint. Phải ghi rõ loại dùng, split ảnh và preprocessing; không mặc định chỉ đổi cờ là số phải khớp bảng paper. [PrACo loader](https://github.com/ciampluca/PrACo/blob/master/models/loader.py), [MUCCA entry point](https://github.com/ciampluca/PrACo/blob/master/multiclass_main.py)
- Với NPV/WPMAE: giữ cùng K và cùng prompt giữa cấu hình; định nghĩa epsilon, cách xử lý target có count 0, cách tổng hợp theo ảnh/target/họ prompt. WPMAE phụ thuộc vào số lượng và độ đa dạng prompt được thử.
- Bootstrap phải lấy mẫu theo ảnh và giữ các target/prompt của một ảnh cùng nhóm. Dùng paired bootstrap cho chênh lệch giữa hai cấu hình. CI theo ảnh không thay thế biến thiên giữa các seed huấn luyện.
- Audit seen/unseen nên áp dụng cho cả MUCCA và PairTally; việc không train trên ảnh benchmark không bảo đảm lớp target chưa từng xuất hiện trong counting training.

## 10. Phạm vi và lịch khả thi hơn

Form cung cấp các ngày báo cáo từ 18/11 đến 16/12/2026. Tính từ 07/10/2026, nhóm có 42–70 ngày tới các mốc đó, nhưng ngày đã chọn và hạn nộp báo cáo/code chưa rõ. Có thể dùng lịch sáu tuần tới mốc sớm nhất; không nên giả định đã được chọn ngày muộn.

| Giai đoạn | Việc cần chốt |
|---|---|
| 07–13/10 | Đối chiếu RichCount; tái lập E0; kiểm tra evaluator; xây train/dev/test prompt; đo GPU-hours sơ bộ |
| 14–20/10 | Cài đặt can thiệp tối thiểu, kiểm tra GT mosaic, gradient và checkpoint; chưa mở rộng nhiều biến thể |
| 21–27/10 | Pilot E0-ft/E1-aug/E1/E2/E3; chọn lambda/tỉ lệ bằng dev; khóa thiết kế |
| 28/10–03/11 | Chạy cấu hình chính và lặp seed cho các so sánh quyết định; lưu dự đoán để tái tính metric |
| 04–10/11 | Đánh giá test với protocol đã khóa; đánh giá paraphrase cùng target/different target; paired CI |
| 11–17/11 | Viết báo cáo, hình minh họa, demo, giới hạn nghiên cứu và thời gian dự phòng |

Chi phí cần đo, không ước lượng bằng tên GPU: 6 cấu hình × 5 họ × 5 prompt là 150 lượt suy luận tương đương toàn tập FSC-147, chưa tính các benchmark khác. Có thể giảm số prompt sau pilot dev và trước khi khóa test, hoặc chia sẻ đặc trưng ảnh sau khi xác minh triển khai.

Ưu tiên giữ: CLIP-Count, E0-ft, đối chứng prompt augmentation, các can thiệp riêng/kết hợp, FSC-147, PrACo++, ít nhất một bộ ảnh đa lớp thật, đánh giá kết hợp bằng paraphrase.

Ưu tiên giảm: hard-pair/null-mosaic mở rộng, nhiều bố cục mosaic, T2ICount inference, spatial gate và pipeline VA-Count đầy đủ. Nếu thầy yêu cầu giải thích lỗi VA-Count/GDINO, giữ một chẩn đoán có giới hạn và trình bày riêng; không dùng nó để mở rộng contribution chính.

## Điều kiện trước khi chạy dài

1. E0 và evaluator cho dự đoán nhất quán; hiểu khác biệt giữa số công bố và số tái lập.
2. Bộ prompt dev hợp lệ về nghĩa, có số đo đủ để quyết định mục tiêu consistency.
3. Mosaic được kiểm tra trực quan và tổng density khớp số point target sau biến đổi.
4. Các tham số dự kiến học có gradient; load/save checkpoint không mất phần trainable.
5. Có thời gian/VRAM thực đo cho một epoch và một lượt đánh giá; chốt số cấu hình và seed phù hợp.

Nếu đạt các điều kiện trên, hướng này đủ cơ sở để triển khai thành đồ án có giá trị. Nếu consistency không có hiệu quả, kết quả vẫn hữu ích khi ablation và giới hạn kết luận được giữ đúng; khi đó tránh dùng tiêu đề hứa hẹn cải thiện đã được chứng minh.

Tên an toàn trong giai đoạn chưa có kết quả: **Studying Prompt Robustness and Target Sensitivity in Text-Guided Zero-Shot Object Counting**. Có thể giữ tên hiện tại như mục tiêu nghiên cứu, nhưng phần tóm tắt cần dùng “nghiên cứu/đánh giá khả năng cải thiện”.
