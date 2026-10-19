# Review bằng mắt của Trí — 9 query còn lại và tổng hợp 15 query

**Bổ sung 16/10:** đã nhận kiểm chéo Triệu 14/15 query; hiệu chỉnh plates 3/3 đúng loại và giải thích đủ final q05_2. [Đối chiếu mới](TRIEU_CROSSCHECK_2026-10-16.md). Phần nhận xét ngày 15/10 bên dưới giữ nguyên nguồn/lịch sử, gồm số 20/42 trước hiệu chỉnh; không còn yêu cầu phân loại lại q05_2 từ đầu.

**Ghi nhận 15/10/2026 (Asia/Bangkok).** Nguồn: nhận xét trực tiếp của người dùng trong chat. Run `b2_remaining3_20261015`, tau_sample=tau_final=0.23; số đếm đối chiếu từ kết quả đã lưu. Đây là đánh giá định tính theo query, chưa phải nhãn độc lập từng bbox hoặc xác nhận của Triệu.

## Chín truy vấn mới

| Query | Stage1 theo Trí | Mẫu đúng theo Trí | Final theo Trí | B0 → B2 |
|---|---|---:|---|---:|
| q02_1 plates | Khoanh thừa nhiều | 0/3 | Có nhận diện đúng nhưng khoanh thừa nhiều | 28 → 31 |
| q02_2 bowls | Có bowl nhưng khoanh sai/thừa nhiều | 1/3 | Có khoanh đúng nhưng thừa nhiều | 31 → 31 |
| q02_3 cups | Có khoanh được cốc nhưng sai/thừa nhiều | 2/3 | Có khoanh được cốc nhưng sai/thừa nhiều | 23 → 26 |
| q04_1 strawberries | Có khoanh được, sai/thừa nhiều | 2/3 | Có khoanh được, sai/thừa nhiều | 60 → 59 |
| q04_2 blueberries | Có khoanh được, sai/thừa nhiều | 2/3 | Có khoanh được, sai/thừa nhiều | 43 → 32 |
| q04_3 red currants | Có khoanh được, sai/thừa nhiều | 0/3 | Có khoanh được, sai/thừa nhiều | 84 → 84 |
| q05_1 cherries | Có khoanh được, sai/thừa nhiều; người dùng xác nhận có 2 quả cherry | 1/3 | Còn kiểu lỗi như stage1 | 20 → 15 |
| q05_2 raspberries | Có khoanh được, sai/thừa nhiều | 3/3 | Còn kiểu lỗi như stage1 | 11 → 14 |
| q05_3 blackberries | Có khoanh được, sai/thừa nhiều | 2/3 | Khoanh từng múi blackberry thành bbox, đồng thời khoanh các loại quả khác | 21 → 79 |

**Đã làm rõ q02_3:** người dùng xác nhận “bowl” là gõ nhầm, ý là vẫn khoanh được cốc (cups). Đã sửa dòng trên theo xác nhận này. Các dòng “khoanh thừa” chưa đủ để phân loại tất cả khung thừa là trùng, sai lớp hay một phần vật.

“Final như stage1” được ghi là cùng kiểu lỗi, không phải cùng tập khung: cherries đổi 20→15, raspberries 11→14. Review về múi của blackberries phù hợp quan sát sơ bộ trước đó của assistant; chưa kiểm từng khung hoặc lượng hóa mỗi loại lỗi.

## Tổng hợp cùng 6 query đầu

[Review 6 query trước](../b2_two_images_20261015/USER_VISUAL_REVIEW.md).

- Đã có review của Trí cho 15/15 query, 5 ảnh dev; đã làm rõ lỗi gõ bowls/cups. Chưa đánh dấu kiểm chéo của Triệu hoặc evaluator hoàn tất.
- 14 query có mẫu, mỗi query 3 mẫu; chairs không có mẫu và không chạy lượt hai. Theo số mẫu đúng do Trí báo: 7/15 mẫu ở run đầu + 13/27 mẫu ở run sau = **20/42 mẫu đúng loại**. Đây là tổng hợp đánh giá bằng mắt, không phải metric benchmark đã kiểm độc lập.
- **3 query có mẫu đúng 3/3:** guitars, rulers, raspberries. Guitar được đánh giá final đúng; rulers và raspberries vẫn sai/thừa. Chọn đúng mẫu chưa đủ bảo đảm final đúng trong cấu hình này.
- **4 query có mẫu đúng 0/3:** amplifiers, pencils, plates, red currants. **7 query còn lại có mẫu pha trộn**. Mẫu sai đi cùng lỗi final không tự chứng minh mẫu sai là nguyên nhân duy nhất.
- Chairs: GT gói dữ liệu có 1 ghế; model trả 0, là bỏ sót đối tượng có mặt, không phải kiểm tra lớp vắng mặt.
- Blackberries: vừa có nhầm loại vừa có dấu hiệu sai đơn vị đếm (một phần quả được tính như một vật). NMS chưa được thử; không suy ra khung phần vật sẽ được xử lý hết bằng NMS hoặc tăng ngưỡng.

## Kết luận làm việc

Đã đủ để xác lập vấn đề khảo sát trên pilot: đầu ra chưa chọn riêng đúng loại/đúng vật thể được hỏi; top-3 mẫu tự động và các ngưỡng đã kiểm chưa giải quyết các ca này. Chưa đủ để khẳng định mọi cấu hình CountGD++ đều lỗi, định vị nguyên nhân trong kiến trúc, hay gọi đây là vấn đề chưa có nghiên cứu giải quyết. B0/B2 là đối chứng thành phần qua app; chưa tái hiện toàn paper.

Giữ hướng chính bám câu hỏi X/Y của thầy: giảm đếm nhầm loại mà vẫn giữ vật đúng. Lỗi theo phần quả của blackberries được ghi là nhóm lỗi riêng cần đo, chưa mở thành mục tiêu đồ án thứ hai. Không chốt giải pháp chỉ sửa mẫu, vì đã có 2 ca đúng 3/3 mẫu nhưng final sai.

## Bước kế tiếp cụ thể

Chuyển từ nhận xét chung sang nhãn từng khung trên một ca nhỏ trước: **q05_2 raspberries, B2 có 14 bbox và mẫu đúng 3/3 theo Trí**. Trí và Triệu đối chiếu các số bbox trên final.jpg:

- Loại vật thật: raspberry / loại khác / chưa rõ.
- Khung bao cả quả hay chỉ một phần: cả quả / phần quả / chưa rõ.
- Nếu nhiều khung cùng chỉ một quả, ghi cùng ID vật để phát hiện đếm trùng. Không coi các khung chồng nhau là trùng chỉ vì giao nhau.
- Ghi quả raspberry thật nào bị bỏ sót; GT gói dữ liệu là 4, cần đối chiếu ảnh/nhãn.

Một khung có thể vừa sai loại vừa chỉ bao một phần vật; dùng các trường riêng, không ép lỗi thành một nhóm duy nhất. Đây là nhãn hậu kiểm, không đưa GT hoặc nhãn lớp khác vào đầu vào model. Triệu kiểm chéo và ghép evaluator; Trí tiếp tục tự làm thí nghiệm khi đã chốt một can thiệp và cách đo. Chưa chạy thêm model, train, E3 hoặc thay NMS/ngưỡng ở mốc này.

[Ảnh final q05_2](q05_2/final.jpg) · [Ảnh mẫu q05_2](q05_2/pseudo.jpg) · [Số liệu 15 query](REVIEW.md)
