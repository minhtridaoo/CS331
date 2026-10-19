# Đề xuất chốt phạm vi đồ án CS331 trong 6 tuần

Ngày soạn: 07/10/2026. Trạng thái: **đề xuất để nhóm trưởng duyệt trước khi đăng ký với giảng viên**.

## 1. Quyết định đề nghị

**Chọn một hướng chính: hướng 3 — cải thiện khả năng đếm đúng đối tượng khi thay đổi truy vấn văn bản trên cùng một ảnh.**

Hướng 1 được sử dụng để hình thành giả thuyết về dữ liệu giám sát. Hướng 2 có thể làm một chẩn đoán nhỏ nếu còn thời gian. Nhóm không cam kết phát triển ba phương pháp độc lập trong sáu tuần.

| Gợi ý của giảng viên | Vai trò trong đề tài đề xuất | Lý do |
|---|---|---|
| Mô hình học theo GT density nhưng đếm vùng/đối tượng không liên quan | Bối cảnh và giả thuyết về thiếu giám sát phân biệt target | Chứng minh nguyên nhân do density hoặc thay thế density supervision sẽ cần một thiết kế thí nghiệm riêng |
| Grounding DINO đúng nhưng VA-Count đếm sai vùng | Chẩn đoán bổ sung, tối đa hai ngày nếu pipeline sẵn sàng | Cần kiểm tra detection, exemplar selection và counter; triển khai sửa cả pipeline sẽ mở rộng phạm vi đáng kể |
| Đổi query từ X sang Y nhưng mô hình vẫn đếm như X | **Mục tiêu chính** | Có thể xác định đầu vào/đầu ra rõ ràng, áp dụng can thiệp trên một mô hình và dùng benchmark có sẵn để kiểm chứng |

Đây là lựa chọn phạm vi nghiên cứu, không khẳng định ba gợi ý của thầy là ba bài bắt buộc phải hoàn thành. Nội dung thầy cung cấp chưa đặt ra yêu cầu phải giải quyết trọn vẹn cả ba.

## 2. Tên đề tài đề xuất

**Tiếng Anh:** Evaluating and Improving Target Sensitivity in Text-Guided Zero-Shot Object Counting

**Tiếng Việt:** Đánh giá và nghiên cứu cải thiện khả năng đếm đúng đối tượng theo truy vấn trong bài toán Zero-Shot Object Counting.

“Improving” thể hiện mục tiêu nghiên cứu, không phải tuyên bố đã có kết quả cải thiện. Tên này phù hợp với phạm vi thu gọn hơn tên V3.3 đặt prompt robustness và target sensitivity ngang nhau.

## 3. Câu hỏi nghiên cứu và phương pháp

**Câu hỏi:** Giám sát đa lớp có chọn lọc bằng ảnh ghép có giúp CLIP-Count đếm đúng lớp được yêu cầu trong ảnh nhiều loại đối tượng, đồng thời duy trì độ chính xác đếm thông thường hay không?

Ví dụ minh họa: cùng ảnh có 8 quả táo và 3 quả cam, query “apples” cần tập trung vào táo, query “oranges” cần tập trung vào cam. Nếu hai lớp có cùng số lượng, đánh giá thêm density theo vùng; không đòi hai tổng số phải khác nhau.

Phương pháp dự kiến:

1. Sử dụng checkpoint CLIP-Count công khai làm điểm khởi đầu. Mã nguồn đã có trong dự án, thuận tiện sửa dữ liệu huấn luyện và đối chứng. [CLIP-Count](https://github.com/songrise/CLIP-Count)
2. Kích hoạt và điều chỉnh cơ chế cross-class mosaic có sẵn: tạo ảnh ghép từ dữ liệu train, xây density mục tiêu theo lớp được yêu cầu và kiểm tra chất lượng nhãn tile phụ.
3. Fine-tune với cùng lịch tối ưu, cùng số bước và cấu hình tiền xử lý đã thống nhất cho các thí nghiệm so sánh.
4. Đánh giá trên ảnh ghép có kiểm soát và ảnh đa lớp thật để kiểm tra khả năng chuyển sang cảnh tự nhiên.

Không nhận mosaic là phát minh mới. Đóng góp dự kiến là triển khai can thiệp có kiểm soát, đo tác dụng trên CLIP-Count và phân tích điều kiện thành công/thất bại.

Zero-shot ở đây nói đến đếm các lớp chưa gặp trong huấn luyện counting theo protocol thích hợp; không có nghĩa hoàn toàn không huấn luyện mô hình. Tách riêng các lớp seen/unseen khi đánh giá ngoài FSC-147, không suy ra unseen đối với dữ liệu tiền huấn luyện CLIP.

## 4. Phạm vi bắt buộc

### Các cấu hình

| Mã kế thừa V3.3 | Cấu hình | Mục đích |
|---|---|---|
| E0 | Checkpoint CLIP-Count công khai | Mốc tái lập ban đầu |
| E0-ft | Fine-tune không có cross-class supervision | Tách tác dụng của việc học thêm khỏi tác dụng của can thiệp |
| E2 | Fine-tune với cross-class mosaic supervision | Kiểm tra can thiệp chính |

Giữ cùng số epoch/optimizer/LR/effective batch size giữa E0-ft và E2. Thống nhất bố cục, crop/resize và tăng cường ảnh trong phạm vi có thể kiểm soát; ghi rõ mọi khác biệt còn lại. Giữ self-mosaic của control khi phù hợp để giảm ảnh hưởng riêng của đường ghép và biến đổi kích thước. Không kết luận nguyên nhân hoàn toàn do thông tin đa lớp nếu các yếu tố này vẫn thay đổi cùng lúc.

Mục tiêu là hai seed cho E0-ft và E2. Nếu thời gian chạy đo được không cho phép, báo rõ chỉ một seed và giới hạn kết luận. Ưu tiên lặp lại so sánh chính hơn mở thêm mô hình/loss.

### Dữ liệu và đánh giá

| Thành phần | Vai trò |
|---|---|
| FSC-147 train | Fine-tune, tạo mosaic từ dữ liệu train |
| FSC-147 validation và mosaic từ validation | Pilot, chọn tỉ lệ mosaic, kiểm tra lỗi, chọn checkpoint |
| FSC-147 test | Đánh giá cuối về sai số đếm thông thường |
| PrACo/PrACo++ | Negative-label test và distractor test theo protocol được chọn |
| MUCCA | Đánh giá cuối trên ảnh đa lớp thật |

PrACo++ và MUCCA được thiết kế để đánh giá sự phù hợp giữa query và đối tượng được đếm, phù hợp với mục tiêu này. Chốt phiên bản evaluator và định nghĩa metric trước khi chạy; không gộp các kết quả khác protocol như thể tương đương. [PrACo++/MUCCA](https://arxiv.org/abs/2605.02752)

Metric chính: MAE, NMN, PCCN và CntF1 theo đúng evaluator. Bổ sung hình cùng ảnh/khác query với density dự đoán. Giữ dự đoán theo ảnh để tính paired bootstrap CI trên MUCCA, lấy mẫu theo ảnh và giữ các query của cùng ảnh chung một nhóm.

E2 tốt hơn cần được đánh giá đồng thời về chọn target và sai số đếm. Nếu hai mặt đánh đổi, báo riêng; không chọn duy nhất metric có lợi. Nếu chưa thấy cải thiện chắc chắn, sản phẩm vẫn là nghiên cứu đối chứng có kết quả và giới hạn rõ ràng; không ghi thành cải thiện đã được chứng minh.

### Kiểm tra chất lượng bắt buộc

- Tất cả tile phục vụ train phải lấy từ split train. Không chọn thiết kế dựa vào kết quả MUCCA/test.
- Tile khác nhãn không bảo đảm không có target. Kiểm tra thủ công một mẫu mosaic cố định, ghi lỗi và điều chỉnh danh sách ảnh/cặp nếu cần; cosine ngữ nghĩa không phải bằng chứng target vắng mặt.
- Bắt đầu với bố cục 2×2 và một cơ chế lấy mẫu đơn giản. Chỉ thêm biến thể khi pilot validation cho thấy cần thiết.
- Kiểm tra tổng density theo số point sau biến đổi và scale density ×60 của CLIP-Count.
- Vá đường truyền args khi fine-tune; tắt giai đoạn contrastive warm-up không phù hợp bằng cấu hình đã kiểm; xác nhận số epoch thực tế; kiểm tra load/save/resume checkpoint.
- Đối chiếu dự đoán giữa inference CLIP-Count và wrapper evaluator trên cùng ảnh/query trước khi chạy toàn bộ.
- Audit trùng ảnh và lớp đã gặp của dữ liệu đánh giá; báo riêng seen/unseen khi có thể xác định.

## 5. Phần mở rộng và giới hạn cam kết

Chỉ mở rộng sau khi ba cấu hình chính, pipeline đánh giá và lưu kết quả đã ổn định:

| Phần mở rộng | Giới hạn |
|---|---|
| Kiểm tra vài paraphrase bảo toàn nghĩa | Chỉ đánh giá độ ổn định; tách prompt phát triển và prompt đánh giá; không thêm một nhánh huấn luyện consistency |
| VA-Count/Grounding DINO diagnostic | Tối đa hai ngày, tập ảnh nhỏ; lưu box, exemplar thực dùng và density; không cam kết sửa/retrain VA-Count |
| T2ICount inference hoặc PairTally INTER | Chỉ chọn một nếu còn ngân sách và môi trường đã chạy được |

Trong kế hoạch sáu tuần này, E1/E3 và loss consistency thuộc hướng phát triển tiếp theo. Nếu nhóm quyết định đưa chúng trở lại contribution chính, phải bổ sung E1-aug và đánh giá kết hợp; đó là thay đổi phạm vi cần tính lại lịch.

Không đưa vào cam kết hiện tại: bỏ/thay thế density supervision, train lại ZSC/VA-Count/T2ICount, nhiều bộ dữ liệu phụ, attribute grounding trên PairTally INTRA, nhiều bố cục/hard-pair/null-mosaic đồng thời hoặc mục tiêu đạt SOTA.

T2ICount vẫn là tài liệu liên quan trực tiếp vì nghiên cứu hạn chế về text sensitivity; không chạy lại mô hình này không đồng nghĩa được bỏ qua khi so sánh ý tưởng. [T2ICount](https://arxiv.org/abs/2502.20625)

## 6. Kế hoạch sáu tuần

| Tuần | Công việc chính | Đầu ra phải có |
|---|---|---|
| 1 | Tái lập E0; chuẩn bị FSC-147/evaluator; đo thời gian một epoch và một lượt đánh giá trên cấu hình dự kiến | Notebook chạy được, số baseline, cấu hình môi trường, dự toán GPU-hours; chốt số epoch/seed dựa trên phép đo |
| 2 | Nối mosaic sampler, kiểm tra nhãn/density, thử fine-tune ngắn, kiểm tra save/resume và wrapper | Phiên bản can thiệp tối thiểu hoạt động, hình kiểm tra dữ liệu, protocol dev/test rõ ràng |
| 3 | Pilot E0-ft/E2 trên validation, chọn cấu hình trong ngân sách nhỏ đã định trước; bắt đầu chạy chính | Thiết kế và tham số được khóa; checkpoint/log của so sánh chính |
| 4 | Hoàn tất E0-ft/E2, ưu tiên seed thứ hai; sửa lỗi thực thi có bằng chứng | Checkpoint, log và dự đoán của các cấu hình; không mở nhánh phương pháp lớn mới |
| 5 | Đánh giá cuối FSC/PrACo++/MUCCA, CI và phân tích lỗi; thêm một phần mở rộng nếu hoàn tất sớm | Bảng kết quả, hình cùng ảnh/khác target, đánh giá giới hạn |
| 6 | Hoàn thiện báo cáo, slide, demo, hướng dẫn tái lập và dự phòng | Bộ nộp hoàn chỉnh và buổi chạy thử trình bày |

Khả thi còn phụ thuộc GPU và số giờ nhóm có thể sử dụng. Kế hoạch không coi quota Colab hay thời gian một epoch là điều đã được xác nhận.

Mốc quyết định:

- Cuối tuần 1: nếu E0/evaluator chưa chạy hoặc chưa có GPU đáp ứng, xử lý hạ tầng và báo lại nhóm trưởng trước khi nhận thêm phạm vi.
- Cuối tuần 2: nếu pipeline can thiệp chưa ổn định, cắt toàn bộ phần mở rộng.
- Cuối tuần 3: khóa thiết kế bằng validation; tuần 4 không thêm backbone/loss/dataset mới vào phần bắt buộc.
- Tuần 5 có kết quả chưa cải thiện: kiểm tra tính đúng của thực nghiệm, báo kết quả âm/đánh đổi; không đổi phương pháp sau khi nhìn test để chạy lại và chọn kết quả đẹp hơn.

## 7. Phân công đề xuất cho nhóm hai người

| Người phụ trách | Trách nhiệm chính |
|---|---|
| Thành viên A | Môi trường, CLIP-Count, fine-tune E0-ft/E2, checkpoint và log |
| Thành viên B | Dữ liệu/split, kiểm tra mosaic, evaluator/metric, lưu dự đoán và bảng/hình |
| Cả nhóm | Kiểm tra nhãn, thống nhất protocol, đọc related work, phân tích kết quả, báo cáo và slide |

Chưa gán tên cụ thể; nhóm trưởng phân công theo kỹ năng và quyền truy cập GPU. Thống nhất schema kết quả và đường dẫn dữ liệu ngay tuần 1 để hai phần ghép được với nhau.

## 8. Sản phẩm bàn giao

1. Mã nguồn và notebook chạy baseline/fine-tune/đánh giá, kèm phiên bản môi trường.
2. Checkpoint hoặc đường dẫn checkpoint; cấu hình, seed và log.
3. Bảng E0/E0-ft/E2 với chỉ số chuẩn, dự đoán theo ảnh và CI phù hợp.
4. Hình minh họa cùng ảnh nhưng thay target, gồm cả ca thành công và thất bại.
5. Báo cáo, slide và demo nhận ảnh cùng tên lớp, trả số đếm và density map. Demo không cần hệ thống triển khai web riêng.

## 9. Nội dung có thể điền vào form sau khi nhóm duyệt

**Chủ đề:** Evaluating and Improving Target Sensitivity in Text-Guided Zero-Shot Object Counting

**Tóm tắt:**

Đề tài tập trung vào hiện tượng mô hình Zero-Shot Object Counting chưa phân biệt đúng đối tượng cần đếm khi truy vấn văn bản thay đổi trên cùng một ảnh. Nhóm sử dụng CLIP-Count làm mô hình nền và nghiên cứu tác dụng của giám sát đa lớp có chọn lọc bằng ảnh ghép (cross-class mosaic supervision). Cơ chế mosaic có sẵn được kích hoạt và điều chỉnh để tạo mẫu huấn luyện với bản đồ mật độ tương ứng với lớp được yêu cầu. Nhóm dự kiến so sánh checkpoint gốc, mô hình được fine-tune thông thường và mô hình fine-tune với mosaic để phân tích tác dụng của can thiệp. Việc đánh giá sử dụng FSC-147, các bài kiểm tra PrACo/PrACo++ và dữ liệu đa lớp thật MUCCA, kết hợp sai số đếm với các chỉ số đánh giá khả năng chọn đúng đối tượng. Sản phẩm gồm mã nguồn, notebook tái lập, kết quả thực nghiệm, phân tích lỗi, báo cáo và demo. Mục tiêu là kiểm chứng khả năng cải thiện độ nhạy theo target và làm rõ giới hạn của phương pháp.

**Tài liệu tham khảo chính trong giai đoạn 2024–2026:**

- Ciampi et al., *Mind the Prompt: A Novel Benchmark for Prompt-based Class-Agnostic Counting*, WACV 2025. [Bài báo](https://arxiv.org/abs/2409.15953)
- Qian et al., *T2ICount: Enhancing Cross-modal Understanding for Zero-Shot Counting*, CVPR 2025. [Bài báo](https://arxiv.org/abs/2502.20625)
- Pacini et al., *Does it Really Count? Assessing Semantic Grounding in Text-Guided Class-Agnostic Counting*, arXiv 2026. [Bài báo](https://arxiv.org/abs/2605.02752)

Báo cáo đầy đủ vẫn cần trích CLIP-Count và các công trình nguồn của mosaic dù nằm ngoài giai đoạn ưu tiên của ô tài liệu tham khảo trong form.
