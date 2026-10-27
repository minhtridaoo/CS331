# CS331 — Đánh giá tiềm năng công bố khoa học và lộ trình nâng cấp CountGD++

> **Tài liệu định hướng nghiên cứu để trao đổi với giảng viên và nhóm**  
> **Nhóm:** Trí – Triệu  
> **Ngày soạn:** 27/10/2026  
> **Hạn báo cáo môn học:** 02/12/2026; hạn hoàn thiện nội bộ dự kiến 29/11/2026  
> **Trạng thái:** Phân tích/đề xuất, **không phải** bài báo đã được chấp nhận hay kết quả thử nghiệm mới.

## 0. Cách đọc và mức độ xác thực

Tài liệu phân biệt ba loại thông tin:

- **[KẾT QUẢ NHÓM BÁO CÁO]**: các số liệu do nhóm cung cấp trong bản tóm tắt demo ngày 27/10. Chúng được dùng để phân tích, nhưng **chưa được tác giả tài liệu này kiểm toán trực tiếp từ toàn bộ tệp thí nghiệm P4.6**.
- **[ĐÃ ĐỐI CHIẾU]**: thông tin có thể đối chiếu từ kho mã nguồn `minhtridaoo/CS331` ở các báo cáo và tệp đã truy cập được, chẳng hạn benchmark và thử nghiệm P4 trước đó.
- **[ĐỀ XUẤT NGHIÊN CỨU]**: giả thuyết, phương pháp, cỡ mẫu và quy trình được đề nghị; không được viết vào báo cáo dưới dạng “đã thực hiện” khi chưa có bằng chứng.

Mục tiêu không phải tạo một bản báo cáo có số đẹp bằng mọi giá. Mục tiêu là xây dựng **một luận điểm khoa học được chứng minh bằng thí nghiệm công bằng, có giới hạn được công bố rõ ràng**.

---

## 1. Kết luận điều hành: đã đủ để làm paper chưa?

**Câu trả lời:** Đủ cơ sở **bắt đầu viết bản thảo theo cấu trúc bài báo** và đủ tốt để báo cáo một hướng cải tiến có căn cứ cho đồ án CS331. **Chưa đủ để kết luận rằng phương pháp mới có tính mới mạnh hoặc đã sẵn sàng gửi tới một hội nghị lớn.**

Nhóm đã có một chuỗi nghiên cứu hợp lý:

1. Tái hiện CountGD++ bằng checkpoint công khai, không huấn luyện lại.
2. Chỉ ra lỗi đếm lẫn loại trong ảnh có nhiều loại vật, đặc biệt ở bài toán đổi câu hỏi X/Y.
3. Tìm ra vấn đề của B2: khung mẫu tự chọn và các khung ở lượt đếm cuối có thể sai loại, trùng lặp hoặc chỉ chứa một phần vật.
4. Đề xuất lọc khung sau CountGD++, so sánh lọc theo điểm tin cậy với lọc kết hợp CLIP.
5. Khóa cấu hình trên ảnh phát triển rồi kiểm trên một nhóm ảnh MUCCA mới.
6. Công bố cả kết quả tích cực lẫn thất bại: giảm đếm nhầm rõ rệt nhưng cũng bỏ sót nhiều vật đúng.

**Luận điểm nghiên cứu hiện đã có bằng chứng bước đầu:** kiểm tra lại tính phù hợp giữa khung ảnh và mô tả bằng CLIP có thể giúp giảm lỗi đếm nhầm trong cấu hình B2 của CountGD++, đặc biệt khi vật được hỏi vắng mặt.

**Chỗ còn thiếu để phát triển thành đóng góp khoa học đủ mạnh:** giải quyết hoặc lý giải định lượng sự đánh đổi **loại được vật sai ↔ giữ được vật đúng**, tăng quy mô và chất lượng kiểm chứng, và chỉ ra khác biệt với những công trình đã dùng CLIP hoặc cơ chế “phát hiện rồi kiểm tra”.

### 1.1. Đánh giá theo cấp độ mục tiêu

| Mục tiêu | Nhận định | Điều kiện trước khi chốt |
|---|---|---|
| Báo cáo CS331 theo chuẩn cấu trúc bài báo | **Khả thi ngay** | Hoàn thiện N4, nguồn số liệu, phần giới hạn và nội dung đối chứng |
| Bản thảo bài báo nghiên cứu/thực nghiệm | **Có thể soạn từ bây giờ** | Viết đúng đóng góp thực tế, không tuyên bố phương pháp hoàn toàn mới |
| Đề xuất giảng viên xem xét công bố ở nơi phù hợp | **Có tiềm năng** | Thêm tập đánh giá độc lập lớn hơn; rà soát công trình gần nhất; kiểm kê tính mới |
| Hội nghị hàng đầu CVPR/ICCV/ECCV | **Chưa đủ căn cứ** | Cần đóng góp mới rõ, đánh giá rộng và so sánh mạnh với công trình liên quan |

Đây là đánh giá chuyên môn định tính, **không phải xác suất được nhận bài**.

---

## 2. Bài toán của nhóm và vì sao đáng nghiên cứu

### 2.1. Bài toán gốc

Cho ảnh `I` và tên loại vật `q`, mô hình cần dự đoán số lượng `c(I, q)`.

Trong cùng một ảnh có hai loại đối tượng `X` và `Y`:

- Hỏi `X` → đếm đúng các đối tượng thuộc `X`.
- Đổi sang `Y` → đếm đúng các đối tượng thuộc `Y`, **không đếm lại đối tượng thuộc `X`**.
- Hỏi `Z` không có trong ảnh → trả `0`.

Đếm đúng **số lượng** chưa đủ để chứng minh hiểu câu hỏi. Chẳng hạn ảnh có 3 người và 3 con chó: hỏi người, mô hình khoanh 3 chó và báo 3 vẫn có sai số đếm bằng 0, nhưng là **kết quả sai về đối tượng**.

### 2.2. Khoảng trống nghiên cứu

Thước đo thông thường như MAE/RMSE trên ảnh một loại vật dễ bỏ qua khả năng mô hình có thực sự đếm đúng loại được hỏi hay không. Công trình PrACo++ (2026) đã đặt vấn đề này một cách trực tiếp và đưa ra bộ kiểm tra cho truy vấn vật vắng mặt và vật gây nhiễu [4]. Vì vậy, nhóm **không được tự nhận mình là nhóm đầu tiên phát hiện vấn đề X/Y**.

Điểm phù hợp để nhóm đóng góp là: **thử và phân tích một cách khắc phục cụ thể cho CountGD++**, lượng hóa khả năng giảm đếm sai loại, đồng thời chỉ rõ mất mát ở vật đúng.

### 2.3. Giữ đúng phạm vi phương pháp

- **CountGD++ là mô hình gốc của tác giả**, có khả năng dùng mô tả tích cực và tiêu cực, mẫu tự chọn và ví dụ bổ sung [1].
- **B0 và B2 của nhóm** là các cấu hình thành phần phục vụ đối chứng; không được gọi B2 là *toàn bộ* CountGD++ gốc.
- **Fusion hiện tại** là bước kiểm tra/lọc thêm **sau B2**, không phải chứng minh CountGD++ trong mọi cấu hình đã được cải thiện.
- Nhánh benchmark FSCD-147 có thêm các thành phần như mẫu tổng hợp và xử lý ảnh dày đặc; **không được so trực tiếp MAE của nhánh benchmark ấy với MAE trên MUCCA**.

---

## 3. Thực nghiệm đã làm: những gì đã chứng minh và chưa chứng minh

### 3.1. Tái hiện mô hình gốc

**[ĐÃ ĐỐI CHIẾU]** Theo `reports/BENCHMARK_FSCD147.md` của nhóm, đã chạy đủ **1.190/1.190 ảnh** FSCD-147 ở nhánh benchmark, MAE ≈ **8,34**, RMSE ≈ **24,64**. Bản báo cáo xác nhận đối chiếu tên ảnh, nhãn đếm và phép tính từ nhật ký, đồng thời nhấn mạnh **chưa có cải tiến mới** trong kết quả này. Cấu hình có văn bản + mẫu tổng hợp + mẫu tự chọn + xử lý ảnh dày đặc.

**Giá trị khoa học:** giúp xác nhận khả năng tái hiện kết quả mô hình nguồn. **Không phải thành tích cải tiến** và không thay thế đánh giá X/Y.

### 3.2. Pilot 5 ảnh / 15 truy vấn

**[ĐÃ ĐỐI CHIẾU]** Theo `reports/PILOT_SUMMARY.md`:

| Cấu hình | MAE | RMSE |
|---|---:|---:|
| B0 (văn bản một lượt) | 19,40 | 24,32 |
| B2 (mẫu tự chọn, hai lượt) | 22,00 | 30,09 |

- B2 có 6 truy vấn tốt hơn B0, 4 tệ hơn, 5 không đổi.
- `q05_3`: hỏi *blackberries*, số thật 3, B2 đếm tới 79.
- Trong đánh giá định tính cũ, 23/42 khung mẫu tự chọn được ghi là đúng loại; con số này không phải chỉ số nhận diện chuẩn hóa.

**Cách kết luận đúng:** trong phạm vi pilot này, B2 không nhất thiết tốt hơn B0. Việc chọn mẫu và đếm sau đó có lỗi đáng phân tích. **Chưa đủ chứng cứ khẳng định nguyên nhân duy nhất của mọi lỗi là khung mẫu tự chọn**, vì bước tạo khung cuối, trùng khung, vật bị chia nhỏ và quy tắc lọc cũng có thể góp phần.

### 3.3. Cải tiến thử trên tập phát triển

**[ĐÃ ĐỐI CHIẾU]** Tệp `results/countgdpp/p4_count_cv_20261020/report.json` ghi kết quả khảo sát trên **5 ảnh / 15 truy vấn**:

| Phương pháp | MAE |
|---|---:|
| B2 gốc | 22,0 |
| Chỉ lọc điểm CountGD++ | 4,6 |
| Chỉ lọc theo CLIP | 6,8 |

**[KẾT QUẢ NHÓM BÁO CÁO]** Trong bản tóm tắt gần đây, nhóm còn nêu biến thể **Fusion 50/50: MAE = 5,8 trên tập phát triển**. Đây là biến thể khác với **CLIP-only = 6,8**. Bảng khảo sát cũ không đủ để tự xác nhận số Fusion = 5,8; khi nộp báo cáo phải dẫn tới đúng tệp kết quả Fusion.

**Không suy rộng:** đây là tập dùng để phát triển và lựa chọn ngưỡng. Kết quả chưa chứng minh khả năng khái quát.

### 3.4. P4.6 trên 10 ảnh MUCCA mới

**[KẾT QUẢ NHÓM BÁO CÁO]** Theo bản tóm tắt demo ngày 27/10: 10 ảnh mới; mỗi ảnh 2 truy vấn có vật và 1 truy vấn vắng mặt; tổng 30 truy vấn. Cấu hình được khai báo là đã khóa trước khi chạy.

| Phương pháp | MAE 20 truy vấn có vật | Số đếm TB ở 10 truy vấn vắng mặt (đúng = 0) | MAE chung 30 truy vấn | Khung bị đánh dấu sai theo phép tự động |
|---|---:|---:|---:|---:|
| B0 | **5,70** | 8,9 | 6,77 | 106 |
| B2 | 12,95 | 13,1 | 13,00 | 238 |
| Lọc điểm | 8,75 | 4,3 | 7,27 | 92 |
| **Fusion 50/50** | 7,80 | **1,0** | **5,53** | **31** |

Các phép tính có thể suy ra:

- **So với B2 gốc:** giảm MAE từ 13,00 xuống 5,53, khoảng **57,5%**.
- **So với chỉ lọc điểm:** giảm MAE từ 7,27 xuống 5,53, khoảng **23,9%**.
- **Truy vấn vắng mặt:** số đếm trung bình giảm từ 13,1 xuống 1,0, khoảng **92,4%** so với B2.
- **Khung bị đánh dấu sai theo quy tắc tự động:** 238 xuống 31, khoảng **87,0%**.
- **So với B0:** MAE chung cải thiện 6,77 → 5,53; nhưng trên 20 truy vấn có vật, **Fusion kém B0**: 7,80 so với 5,70.

**Điểm mạnh thật sự:** Fusion có xu hướng giảm đếm nhầm đối tượng, nhất là khi loại được hỏi không có trong ảnh; việc bổ sung CLIP có dấu hiệu mang lại lợi ích vượt việc chỉ tăng ngưỡng điểm CountGD++.

**Điểm yếu thật sự:** theo nhóm báo cáo, bộ lọc mất khoảng 50% vật đúng; chưa có truy vấn có vật nào được Fusion đếm đúng tuyệt đối. Đây là sự đánh đổi nghiêm trọng, không nên giấu ở phần phụ lục.

**Lưu ý diễn giải số liệu:**

1. “Số đếm TB trên truy vấn vắng mặt = 1,0” **không đồng nghĩa** “tỷ lệ báo nhầm chỉ 1%” hoặc “10%”. Cần tính riêng tỷ lệ truy vấn vắng mặt có dự đoán > 0.
2. “Khung sai loại = 31” hiện lấy từ quy tắc tự động dựa vào điểm nhãn thật nằm trong khung; **chưa đồng nghĩa đã có 31 khung sai được người xác nhận**.
3. MAE chung bị ảnh hưởng bởi cơ cấu 20 truy vấn có vật + 10 truy vấn vắng mặt. Cần luôn công bố riêng hai nhóm thay vì chỉ lấy 5,53 làm thông điệp duy nhất.
4. 30 truy vấn thuộc **10 ảnh gốc**, không phải 30 quan sát độc lập khi tính độ chắc chắn thống kê.
5. Báo cáo nhóm nói khoảng tin cậy cho chênh lệch Fusion – lọc điểm không chứa 0. Cần lưu kèm cách lấy mẫu lại **theo ảnh**, số lần lấy mẫu, hạt giống ngẫu nhiên và khoảng cụ thể; không tuyên bố chắc chắn thống kê khi chưa có log để đối chiếu.

### 3.5. Những phần còn chưa xác nhận

- N4 kiểm bằng người: gói kiểm chọn lọc 7 truy vấn tầng A và 2 truy vấn tầng B được nhóm báo là đã chuẩn bị; **chưa có bản tổng hợp hậu kiểm hoàn tất** trong dữ liệu cung cấp.
- Báo cáo P4.6 nêu trong bản tóm tắt chưa được kiểm chứng trực tiếp từ các tệp nguồn ngay trong lần soạn tài liệu này.
- Thực nghiệm mới trên 10 ảnh chỉ giúp đánh giá bước đầu, chưa là bằng chứng về hiệu quả trên toàn bộ MUCCA hay trên những bộ dữ liệu khác.

---

## 4. Đối chiếu công trình liên quan: “Tính mới” nằm ở đâu?

### 4.1. CountGD++ (CVPR 2026) — nền tảng gốc [1]

Tác giả phát triển mô hình đếm mở, có hỗ trợ mô tả văn bản, ví dụ ảnh, mô tả **không được đếm**, và tự chọn mẫu (pseudo-exemplars).

**Hệ quả đối với nhóm:** phải thừa nhận mô hình gốc đã có khả năng mô tả loại cần loại trừ. Một đối chứng quan trọng là **CountGD++ dùng mô tả tiêu cực theo cách được tác giả hỗ trợ**, thay vì so Fusion chỉ với phiên bản B2 giản lược. Cần kiểm xem điều kiện so sánh có cung cấp thêm thông tin đầu vào không; nếu có, ghi thành đối chứng với phạm vi đầu vào khác, không gộp chung mà không giải thích.

### 4.2. PseCo (CVPR 2024) — dùng CLIP để kiểm các vùng ảnh [2]

PseCo phối hợp SAM và CLIP trong quy trình định vị, phân vùng và phân loại đối tượng cần đếm. CLIP dùng để đánh giá đối tượng trong vùng ảnh có phù hợp với tên lớp không.

**Hệ quả:** câu “lần đầu tiên dùng CLIP để lọc vùng ảnh trước khi đếm” là **không chính xác**. Sự kết hợp CountGD++ + CLIP có thể hữu ích, nhưng cần một cơ chế hoặc bằng chứng mới rõ ràng hơn để thành đóng góp phương pháp.

### 4.3. DAVE (CVPR 2024) — phát hiện rồi kiểm chứng [3]

DAVE xuất phát từ quan sát bộ đếm hay báo nhiều đối tượng sai, đề xuất hai bước: tạo tập đối tượng ứng viên rồi kiểm lại để loại ngoại lai.

**Hệ quả:** triết lý “đếm sau khi có người kiểm tra thứ hai” đã được nghiên cứu. Nếu paper của nhóm chỉ dựa vào cấu trúc hai bước thì tính mới yếu.

### 4.4. PrACo++ và MUCCA (2026) — đúng bài toán X/Y [4, 5]

PrACo++ đánh giá khả năng mô hình hiểu đúng tên lớp, trong đó có **truy vấn loại vật không xuất hiện** và tình huống có đối tượng gây nhiễu. MUCCA gồm **200 ảnh nhiều loại vật**, có nhãn điểm theo từng loại.

**Hệ quả:** nhóm nên tham khảo giao thức kiểm tra và các chỉ số có sẵn, đồng thời **không được nhận việc tự nghĩ ra phép kiểm X/Y hoặc bộ MUCCA là đóng góp riêng**. Giá trị của nhóm nằm ở phương pháp sửa lỗi và chứng minh được sự khác biệt.

### 4.5. CLIP-Count (2023) — mô hình đếm dựa trên biểu diễn hình–chữ [6]

Đây là mô hình đếm khác, khai thác khả năng liên kết hình ảnh – văn bản của CLIP. **Không đồng nhất CLIP-Count với việc dùng CLIP chỉ để lọc khung sau CountGD++**.

### 4.6. Bảng định vị đóng góp của nhóm

| Thành phần | Đã có trong nghiên cứu trước? | Nhóm có thể đóng góp gì? |
|---|---|---|
| Đếm không cần huấn luyện riêng từng lớp | Có | Tái lập và đánh giá có kiểm soát |
| Bài toán X/Y, loại vắng mặt, MUCCA | Có | Phân tích lỗi sâu riêng cho CountGD++ |
| Dùng CLIP đánh giá vùng ảnh | Có | Kiểm tra hiệu quả cụ thể trên khung CountGD++ và so đối chứng công bằng |
| Phát hiện – kiểm lại – đếm | Có | Làm rõ mức độ giảm nhầm và mất vật đúng |
| Bộ lọc **thích ứng** để cân bằng giữ đúng/loại sai | Chưa thể tuyên bố mới | **Ứng viên hướng nghiên cứu**, chỉ thành đóng góp sau khi rà soát thêm và có thử nghiệm chứng minh |
| Bộ đánh giá chi tiết phân rã vật sai, vật trùng, vật mất | Có khái niệm tương tự | Có thể đóng góp một nghiên cứu thực nghiệm tái lập được nếu nhãn và giao thức chắc chắn |

**Nguyên tắc:** việc một tổ hợp công cụ chưa thấy trong vài paper **không tự động có nghĩa đó là phát minh mới**. Tính mới phải nằm ở giả thuyết giải quyết vấn đề, khác biệt kỹ thuật hoặc hiểu biết thực nghiệm có ý nghĩa, và được đối chiếu có hệ thống với công trình liên quan.

---

## 5. Câu chuyện khoa học nên viết thành paper

### 5.1. Không nên kể theo hướng

> “Chúng tôi thêm CLIP vào CountGD++, đạt MAE 5,53; do đó hệ thống đã giải quyết bài toán đếm theo câu chữ.”

Cách kể này thiếu công bằng vì bỏ qua B0 tốt hơn trên truy vấn có mặt, còn CLIP và phát hiện–kiểm chứng đã có trong nghiên cứu trước.

### 5.2. Nên kể theo hướng

> **Câu hỏi nghiên cứu:** Bước xác minh lại khung ứng viên bằng điểm phù hợp hình ảnh–văn bản có giúp giảm đếm nhầm loại của CountGD++ trong ảnh nhiều loại vật không, và cái giá phải trả là bao nhiêu đối tượng đúng bị loại nhầm?

Câu chuyện gồm bốn luận điểm:

1. **Vấn đề thật:** mô hình có thể trả sai loại vật ngay cả khi số đếm gần đúng.
2. **Giải pháp tối thiểu:** kiểm lại khung bằng tín hiệu ngữ nghĩa CLIP trước khi đếm, không cần huấn luyện lại CountGD++.
3. **Bằng chứng bước đầu:** giảm sai số toàn bộ và lỗi ở truy vấn vắng mặt so với B2/lọc điểm trên tập MUCCA nhỏ.
4. **Phát hiện mới cần khai thác:** giảm nhận nhầm kéo theo tăng bỏ sót; một cơ chế chọn khung tốt cần xử lý cả hai mục tiêu.

### 5.3. Ba câu hỏi nghiên cứu đề xuất

- **RQ1:** So với B2 gốc và lọc điểm thông thường, CLIP có thực sự giúp loại khung sai loại mà vẫn giữ vật đúng không?
- **RQ2:** Hiệu quả có khác nhau giữa truy vấn có mặt, vắng mặt, và các cặp loại vật dễ nhầm lẫn không?
- **RQ3:** Có thể thiết kế quy tắc kiểm tra **thích ứng theo ảnh/câu hỏi** giúp giảm bỏ sót mà không làm tăng mạnh số khung sai không?

### 5.4. Các giả thuyết cần kiểm bằng dữ liệu

- **H1:** Fusion ít sai số hơn lọc điểm đơn thuần trên tập ảnh giữ riêng, khi cả hai dùng cùng khung đầu vào.
- **H2:** Fusion giảm số khung sai loại nhưng có thể hạ tỷ lệ giữ vật đúng, nhất là khi khung đúng có điểm CLIP thấp.
- **H3:** Một phương pháp điều chỉnh mức lọc theo sự chắc chắn của điểm và quan hệ ngữ nghĩa có thể cải thiện cân bằng giữa hai loại lỗi.

**H3 là giả thuyết mới, chưa có kết quả.** Nếu thử nghiệm bác bỏ H3, vẫn phải báo kết quả âm tính trung thực.

---

## 6. Hướng phương pháp tiếp theo: làm thế nào để paper mạnh hơn?

### Hướng A — Paper thực nghiệm/phân tích lỗi: ít rủi ro nhất

**Mục tiêu:** chứng minh rõ hơn tính chất của bộ lọc cố định, xác định khi nào nó có ích, khi nào nó phá hỏng khả năng giữ vật đúng.

Thực hiện:

- Đối chiếu B0/B2/lọc điểm/CLIP-only/Fusion trên cùng tập và cùng điều kiện.
- Hậu kiểm bằng người trên mẫu đại diện để phân loại `đúng vật`, `sai loại`, `trùng vật`, `chỉ một phần vật`, `nền`, `bỏ sót`.
- Phân tích theo cặp loại vật, số vật, kích thước vật, mức độ chồng lấp và có/vắng mặt.
- Nêu rõ Fusion cải thiện mặt nào và làm xấu mặt nào.

**Ưu điểm:** tận dụng được dữ liệu hiện tại, ít phải phát triển mô hình mới.  
**Giới hạn:** phù hợp với một bài phân tích thực nghiệm/hội thảo thích hợp hơn là tuyên bố đóng góp thuật toán lớn.

### Hướng B — Bộ lọc thích ứng: ứng viên bài báo phương pháp

**Vấn đề:** ngưỡng cứng và tỷ lệ Fusion 50/50 đối xử các câu hỏi khác nhau giống nhau. Ví dụ, `people` trong ảnh nhiều chó có thể cần tiêu chí loại sai rất khác với `chairs` trong ảnh có nhiều ghế.

**[ĐỀ XUẤT NGHIÊN CỨU]** Thử một quy tắc ra quyết định có kiểm soát, dựa trên:

- Độ chắc chắn của điểm CountGD++ ở các khung ứng viên.
- Độ tương đồng giữa ô ảnh cắt ra và câu hỏi theo CLIP.
- Mức đồng thuận hoặc xung đột giữa hai nguồn điểm.
- Thống kê của cả ảnh/câu hỏi, thay vì chỉ xét từng khung riêng lẻ.

Ví dụ nghiên cứu (chưa phải thuật toán đã chứng minh):

1. Khi cả hai nguồn đều đồng ý rất cao → giữ.
2. Khi cả hai đều thấp → loại.
3. Khi mâu thuẫn → kiểm thêm bằng một tín hiệu đã lựa chọn trên tập phát triển hoặc dùng quy tắc bảo vệ để không loại khung đúng chỉ vì CLIP thấp.
4. Đánh giá riêng ảnh mà mô hình không tạo ra khung nào: **bộ lọc hậu xử lý không thể tự tìm lại vật không được đề xuất**.

**Điểm cần tránh:** nếu thay đổi quy tắc sau khi nhìn thấy kết quả trên 10 ảnh P4.6, **10 ảnh đó không còn là tập kiểm tra cuối độc lập cho phương pháp mới**. Phải dùng tập khác được khóa trước để đánh giá cuối.

**Đối chứng bắt buộc:** so với cách chỉnh ngưỡng cố định tốt nhất, tỷ lệ kết hợp cố định khác 50/50, CLIP-only, chỉ lọc điểm, và nếu phù hợp thì CountGD++ gốc có mô tả loại cần loại trừ. Nếu quy tắc thích ứng không tốt hơn những cách đơn giản này, không nên giới thiệu nó như đóng góp có hiệu quả.

### Hướng C — Xác minh khung mẫu *trước* lượt B2 thứ hai

**Động cơ:** pilot cho thấy khung mẫu tự chọn có thể sai loại; nếu truyền mẫu sai vào lượt 2, mô hình có nguy cơ tạo thêm khung không phù hợp.

**[ĐỀ XUẤT NGHIÊN CỨU]** Kiểm các mẫu tự chọn từ lượt 1 bằng tín hiệu hình–chữ trước khi dùng làm mẫu cho lượt 2. Có thể so ba vị trí đặt bộ kiểm:

- Trước khi chọn mẫu (sớm).
- Sau B2 để lọc khung cuối (muộn, hướng hiện tại).
- Cả hai vị trí, nếu chi phí tính toán chấp nhận được.

**Cảnh báo:** đây là giả thuyết, **chưa chứng minh được lỗi chọn mẫu là nguyên nhân gốc duy nhất**. Cần đối chứng qua thí nghiệm thay đổi đúng một thành phần ở mỗi lần chạy.

### Chọn hướng nào?

**Khuyến nghị theo thứ tự:** hoàn thành **A** để có báo cáo môn học chắc chắn, song song thử **một** biến thể đơn giản của B hoặc C trên tập phát triển. Chỉ đưa B/C thành đóng góp phương pháp khi nó giải quyết được nhược điểm bỏ sót trên tập kiểm tra độc lập.

Không nên triển khai hàng loạt ý tưởng mới rồi chọn kết quả đẹp nhất ở tập 10 ảnh đã biết.

---

## 7. Giao thức kiểm chứng cần có để thầy tin kết quả

### 7.1. Chia tập theo **ảnh gốc**, không theo câu hỏi

Các câu hỏi khác nhau trên cùng một ảnh chia sẻ vật thể và bối cảnh. Nếu một câu hỏi của ảnh nằm ở tập chọn ngưỡng còn câu hỏi khác của cùng ảnh nằm ở tập kiểm tra, kết quả có thể bị ảnh hưởng bởi việc đã “biết” ảnh ấy.

- **5 ảnh pilot cũ:** tập phát triển, không gọi độc lập.
- **10 ảnh P4.6 đã xem kết quả:** vẫn có giá trị cho phân tích hiện tại; **không tái dùng làm tập kiểm tra cuối** nếu phương pháp mới được thiết kế sau khi xem lỗi của 10 ảnh này.
- **Ảnh mới còn chưa xem kết quả:** chọn trước theo quy tắc công bố, chia tập phát triển và tập kiểm tra khóa. Không dùng tập kiểm tra để chỉnh tham số.

**Cỡ mẫu đề xuất, không phải yêu cầu bắt buộc:** mở rộng lên khoảng 30–50 ảnh để phát triển/kiểm tra quy tắc, dành thêm 50–100 ảnh chưa chạm tới để đánh giá cuối; tốt hơn nữa là tiến tới đánh giá tối đa trong phạm vi 200 ảnh MUCCA nếu quy trình cho phép. Nếu không đủ thời gian, ít nhất hãy công bố rõ cỡ mẫu nhỏ và giới hạn thay vì mô tả như kết quả phổ quát.

### 7.2. Tập dữ liệu cần đủ tình huống

Chủ động có:

- Truy vấn **có mặt** và **vắng mặt**.
- Loại vật khác nhau rõ ràng và loại dễ nhầm.
- Ảnh ít vật, vừa và nhiều vật; đối tượng nhỏ, bị khuất, có phần thân tương đồng.
- Những cặp đã gây lỗi như `people` – `dogs` và loại gần nghĩa (`motorcycle` – `bicycle`...), tùy nhãn thật.
- Ảnh không được chọn dựa trên việc mô hình có thất bại hay không, trừ khi đó là một **tập phân tích lỗi riêng**, không dùng để kết luận hiệu quả tổng quát.

Với truy vấn vắng mặt, cần người xem ảnh xác nhận loại đó thực sự không có (kể cả vật rất nhỏ hoặc khuất). Nếu nhãn vắng mặt không chắc, ghi `uncertain` và xử lý minh bạch.

### 7.3. So sánh công bằng

Bảng đối chứng tối thiểu:

| Mã | Cách chạy | Câu hỏi nó trả lời |
|---|---|---|
| C0 | B0, chỉ văn bản | Mức nền đơn giản có tốt hơn B2 không? |
| C1 | B2 gốc | Hai lượt có thật sự giúp không? |
| C2 | B2 + lọc điểm CountGD++ | Có phải chỉ cần bỏ bớt khung là đủ? |
| C3 | B2 + CLIP-only | CLIP riêng lẻ giúp tới đâu? |
| C4 | B2 + Fusion cố định | Lợi ích của việc kết hợp hai tín hiệu? |
| C5 | B2 + phương pháp thích ứng đề xuất | Có giải quyết được đánh đổi không? |
| C6 (khuyến nghị) | B0 + lọc điểm/Fusion | Có cần phải đi qua B2 không? |
| C7 (nếu tương thích) | CountGD++ hỗ trợ mô tả loại loại trừ | So với khả năng sẵn có của bài gốc thì sao? |

**Đối chứng C7 cần đặc biệt cẩn thận:** nếu đưa thêm tên lớp gây nhiễu từ nhãn thật vào đầu vào, đó là việc cung cấp thông tin bổ sung không công bằng. Nếu dùng, phải thiết kế nguồn thông tin loại trừ hợp lệ tại lúc suy luận hoặc đánh dấu đây là điều kiện có đầu vào mạnh hơn.

Không được gọi một cách là “tốt nhất” chỉ vì nó có MAE thấp nhất nếu nó làm mất nghiêm trọng khả năng đếm khi vật có mặt.

### 7.4. Không chỉ đo MAE

Đề xuất bảng chỉ số:

| Nhóm | Chỉ số | Giải thích |
|---|---|---|
| Đếm tổng thể | MAE, RMSE | Mức sai số về số lượng |
| Khi vật có mặt | MAE_present | Có đếm đúng số vật thực hay không? |
| Khi vật vắng mặt | MeanAbsentCount | Trung bình mô hình báo nhầm bao nhiêu vật |
| Khi vật vắng mặt | FPR_absent | Tỷ lệ câu hỏi vắng mặt mà mô hình vẫn báo > 0 |
| Tính đúng vật | Tỷ lệ khung đúng/sai đã hậu kiểm | Kiểm liệu mô hình khoanh đúng loại |
| Khả năng giữ vật đúng | Tỷ lệ vật đúng được giữ sau lọc | Bộ lọc có làm mất vật thật không? |
| Nhận diện trùng | Số khung trùng một vật | Có đếm một vật nhiều lần? |
| Chi phí | Thời gian/ảnh, bộ nhớ nếu đo được | Bước kiểm thêm có quá tốn không? |

**Không báo AP/IoU chuẩn chỉ từ nhãn điểm.** MUCCA có nhãn điểm theo lớp, không mặc nhiên có khung thật. Nếu cần đánh giá khung chuẩn, phải xây dựng nhãn và cách ghép phù hợp. “Một điểm thật nằm trong khung” chỉ là phép xấp xỉ và có thể chấm nhầm khi khung bao nhiều vật hoặc bao vùng rất rộng.

### 7.5. N4 — hậu kiểm bằng người

Khuyến nghị **thực hiện N4 chọn lọc**, nhưng phải nói đúng phạm vi:

1. Kiểm đầy đủ các truy vấn `people` và truy vấn vắng mặt bị báo có vật.
2. Kiểm các khung mà lọc điểm giữ nhưng Fusion loại, hoặc ngược lại (điểm khác biệt giữa hai phương pháp).
3. Lấy ngẫu nhiên một phần khung từ các truy vấn còn lại để tránh chỉ xem ca xấu.
4. Với mỗi khung, phân loại: **đúng loại/đúng vật**, **sai loại**, **khung trùng**, **chỉ một phần vật**, **nền**, **không chắc**; nếu có thể gán `object_id` để biết có bao nhiêu vật đúng phân biệt.
5. Xem trực tiếp ảnh gốc để ghi **vật đúng bị bỏ sót**, không chỉ đếm số khung được giữ.

Nếu N4 chỉ gồm 9 truy vấn có chủ đích, nó là **bằng chứng định tính và chẩn đoán lỗi**, chưa thay được hậu kiểm đại diện trên toàn bộ tập.

Nên có thêm người thứ hai xem một phần nhãn và lưu các trường hợp bất đồng để tránh phụ thuộc một người kiểm.

### 7.6. Độ tin cậy thống kê

- So sánh **theo cặp trên cùng ảnh và cùng truy vấn**.
- Khi lấy mẫu lại để lập khoảng tin cậy 95%, **lấy ảnh gốc làm đơn vị**, mỗi ảnh mang theo tất cả truy vấn của nó.
- Ghi rõ: số ảnh, số lần lấy mẫu lại, hạt giống ngẫu nhiên, hiệu số MAE và khoảng tin cậy.
- Với chỉ 10 ảnh, khoảng tin cậy có thể kém ổn định; không diễn giải kết quả như chắc chắn cho mọi trường hợp.
- Khi so nhiều biến thể/ngưỡng, ghi rõ đã thử bao nhiêu phương án; không điều chỉnh theo tập giữ riêng rồi tiếp tục gọi nó là độc lập.

### 7.7. Tài liệu tái lập tối thiểu

Cần lưu với mỗi thử nghiệm: danh sách ảnh/truy vấn và nhãn thật, mã commit, lệnh chạy, cấu hình, ngưỡng, tên và phiên bản checkpoint, quy tắc chọn ảnh, log, kết quả từng truy vấn, chương trình chấm, cách hậu kiểm và các giới hạn. Không sửa kết quả trước đó để “đẹp số”.

---

## 8. Những sai lầm có thể khiến paper bị phản biện

1. **Tuyên bố tính mới quá rộng:** “lần đầu dùng CLIP xác minh đối tượng” → không đúng vì có PseCo, DAVE và các nghiên cứu liên quan.
2. **Gọi B2 là CountGD++ đầy đủ:** bỏ qua các chức năng tác giả gốc đã hỗ trợ.
3. **Chỉ khoe MAE 5,53:** che việc Fusion kém B0 trên truy vấn có mặt.
4. **Gọi 31 khung là ‘31 lỗi xác nhận bằng người’:** hiện mới là phép tính tự động dựa trên nhãn điểm.
5. **Nhầm số đếm trên truy vấn vắng mặt với tỷ lệ báo sai:** số lượng trung bình khác tỷ lệ trường hợp bị báo nhầm.
6. **Dùng ảnh đã nhìn kết quả để chỉnh thuật toán rồi đánh giá lại:** sẽ làm tập kiểm mất tính độc lập.
7. **Lấy câu hỏi làm đơn vị độc lập thay vì ảnh:** làm khoảng tin cậy có vẻ chắc hơn thực tế.
8. **Đổ mọi lỗi cho pseudo-exemplar:** mới có quan sát tương quan; cần kiểm qua các phương án đặt bộ lọc khác nhau.
9. **Báo ‘không cần huấn luyện’ rồi âm thầm tối ưu tham số trên test:** dù không cập nhật trọng số mô hình, chỉnh ngưỡng theo test vẫn là học từ test.
10. **Không so với chức năng negative prompt của CountGD++ gốc:** có thể bỏ qua một khả năng vốn có của mô hình mà paper đang cố cải thiện.

---

## 9. Lộ trình thực hiện tới hạn 02/12/2026

Các mốc sau là **đề xuất tổ chức**, không phải công việc đã thực hiện. Điều chỉnh theo lịch nhóm và tài nguyên thực tế; ưu tiên đầu ra có thể kiểm chứng thay vì số lượng thí nghiệm.

| Mốc | Thời gian gợi ý | Công việc trọng tâm | Đầu ra bắt buộc |
|---|---|---|---|
| G1 — Khóa bằng chứng cũ | 27/10–02/11 | N4, Triệu hoàn thành kiểm chéo pilot, chốt số P4.6 và dữ liệu 10 ảnh | Log, bảng số đúng, ảnh minh chứng, ghi giới hạn |
| G2 — Thiết kế nghiên cứu | 03–09/11 | Chốt RQ/H1–H3, đối chứng, chia tập ảnh mới theo ảnh gốc, quy tắc chọn, tiêu chí đánh giá | Giao thức đánh giá và danh sách tập khóa |
| G3 — Đánh giá mở rộng | 10–16/11 | Chạy các đối chứng cố định, kiểm chất lượng nhãn và chỉ số vật có/vắng mặt | Bảng kết quả theo ảnh/query; thống kê sai số |
| G4 — Một phương pháp cải tiến có mục tiêu | 17–23/11 | Thử *một* hướng thích ứng hoặc kiểm mẫu sớm; lựa chọn trên tập phát triển | Bảng so sánh và phân tích có/không cải thiện |
| G5 — Đánh giá độc lập & viết | 24–29/11 | Khóa bản cuối, chạy đánh giá giữ riêng, tạo hình minh họa, hoàn chỉnh paper/slide/demo | Bản thảo đủ mục, cấu hình cuối, hình bảng, giới hạn |
| G6 — Duyệt với giảng viên | 30/11–02/12 | Kiểm tra số liệu, trình bày đóng góp và thảo luận khả năng công bố | Bản nộp và đề xuất bước mở rộng nếu thầy đồng ý |

**Quyết định ưu tiên:** nếu tới G4 hướng thích ứng không cải thiện đáng tin so với Fusion/lọc điểm thì **không cố ép** vào paper. Chốt một bài phân tích thực nghiệm tử tế, bảo toàn uy tín khoa học của nhóm.

### 9.1. Phân vai đề xuất

| Người | Việc chính | Bằng chứng giao nộp |
|---|---|---|
| Trí | Chạy mô hình, thiết kế các biến thể/đối chứng, lưu cấu hình và nhật ký | Mã nguồn, log, bảng theo ảnh, thời gian |
| Triệu | Hậu kiểm nhãn và khung, tự xác nhận evaluator, phân tích lỗi và rà soát đầu vào vắng mặt | Bảng nhãn có người/ngày, ảnh minh họa, kết quả đánh giá đã tự chạy |
| Cả hai | Chốt giả thuyết, kiểm số, đánh giá tính mới, viết bài, duyệt kết luận | Biên bản chốt và bản thảo paper |

Phân công có thể thay đổi, nhưng **người làm, người kiểm và người phê duyệt phải rõ ràng**.

---

## 10. Cấu trúc bài báo gợi ý

### Tên bài (tạm thời, cần đổi theo đóng góp cuối)

**Hướng phân tích thực nghiệm:**

*On the Precision–Recall Trade-off of CLIP-Assisted Verification for CountGD++ in Multi-Category Object Counting*

Tạm dịch: *Phân tích sự đánh đổi giữa giữ đúng và bỏ sót đối tượng khi dùng CLIP kiểm tra khung của CountGD++ trong ảnh nhiều loại vật.*

**Nếu có phương pháp thích ứng thực sự hiệu quả:** tên bài nên nhấn vào cơ chế cụ thể sau khi chốt, không tự dùng chữ “novel” hay “state-of-the-art” khi chưa có so sánh đầy đủ.

### Dàn ý theo phong cách bài báo nghiên cứu

1. **Abstract — Tóm tắt:** bài toán, điểm yếu của phương pháp cũ, giải pháp nhóm đề xuất, kết quả trên tập giữ riêng, giới hạn. Chỉ đưa số đã xác nhận.
2. **Introduction — Mở đầu:** vì sao đếm đúng loại quan trọng hơn chỉ khớp số; ví dụ X/Y và truy vấn vắng mặt; câu hỏi nghiên cứu và đóng góp có thể kiểm chứng.
3. **Related Work — Công trình liên quan:** CountGD++, PseCo, DAVE, PrACo++, CLIP-Count; chỉ rõ nhóm kế thừa và khác ở đâu.
4. **Method — Phương pháp:** luồng B0/B2 → khung ứng viên → điểm CountGD++/CLIP → quy tắc giữ/loại → số đếm; mô tả công thức/ngưỡng và phần nào không huấn luyện.
5. **Experimental Setup — Thiết kế thực nghiệm:** tập ảnh, cách chia, nguồn và giấy phép, khung đối chứng, quy tắc khóa tham số, thiết bị, chỉ số.
6. **Results — Kết quả:** bảng có mặt/vắng mặt, MAE/RMSE, FPR_absent, số khung đúng/sai, thời gian; độ tin cậy theo ảnh.
7. **Ablation & Error Analysis — Phân tích thành phần/lỗi:** ảnh hưởng CLIP, Fusion, ngưỡng, vị trí đặt bộ kiểm; ảnh người–chó và ví dụ giữ sai/bỏ sót.
8. **Limitations — Hạn chế:** số mẫu, nhãn, không phục hồi khung thiếu, khác biệt với mô hình gốc đầy đủ; cảnh báo khái quát hóa.
9. **Conclusion — Kết luận:** phát hiện đã được dữ liệu ủng hộ, những gì chưa làm được và hướng tiếp theo.

### 10.1. Các hình/bảng nên có

- **Hình 1:** cùng ảnh, đổi tên lớp X/Y và một ví dụ truy vấn vắng mặt.
- **Hình 2:** sơ đồ luồng B0, B2 và Fusion; xác định rõ CLIP chỉ chấm vùng cắt, không trực tiếp đếm.
- **Hình 3:** ảnh trước/sau lọc khung; chú thích các khung đúng bị loại và khung sai được loại.
- **Bảng 1:** benchmark tái hiện CountGD++ trên FSCD-147 để xác nhận nền, tách biệt khỏi MUCCA.
- **Bảng 2:** toàn bộ đối chứng trên tập đánh giá X/Y, tách có mặt/vắng mặt.
- **Bảng 3:** hậu kiểm khung/vật đúng–sai và chi phí tính toán.
- **Bảng 4:** phân tích đóng góp từng thành phần (lọc điểm, CLIP, Fusion, thích ứng nếu có).
- **Hình 4:** biểu đồ đánh đổi: tỷ lệ giữ vật đúng với tỷ lệ loại vật sai theo các ngưỡng, trên tập phát triển và kiểm tra.

### 10.2. Mẫu đoạn kết luận hiện tại, viết trung thực

> Trên thử nghiệm bước đầu gồm 10 ảnh MUCCA mới và 30 truy vấn, phép lọc kết hợp CountGD++ với CLIP cho MAE trung bình 5,53, thấp hơn cấu hình B2 gốc (13,00) và phương pháp chỉ lọc theo điểm tin cậy (7,27). Mức đếm trung bình trong các truy vấn vật vắng mặt cũng giảm đáng kể. Tuy nhiên, phương pháp làm mất nhiều vật đúng, dẫn tới sai số trên các truy vấn có vật còn cao hơn B0. Vì vậy, kết quả ủng hộ giá trị của bước xác minh ngữ nghĩa nhưng cũng chỉ ra nhu cầu thiết kế bộ lọc cân bằng tốt hơn giữa loại sai và giữ đúng. Các kết luận hiện bị giới hạn bởi quy mô và chất lượng kiểm chứng thủ công của tập thử.

**Chú thích:** đoạn trên diễn giải từ bản kết quả nhóm cung cấp, cần cập nhật sau hậu kiểm và đánh giá mở rộng; không gọi là kết luận cuối cùng.

---

## 11. Tiêu chí quyết định: khi nào nên đề xuất thầy cho công bố?

### Mức A — Hoàn thành đồ án theo chuẩn paper

- Có mô hình nền tái lập được và mô tả trung thực cấu hình.
- Có bài toán X/Y rõ ràng và bộ câu hỏi có mặt/vắng mặt.
- Có phương pháp cải tiến được định nghĩa đầy đủ.
- Có đối chứng công bằng, kết quả theo nhiều chỉ số, hình minh họa.
- Có phần hạn chế và tái lập.

**Nhóm đang tiến gần mức này**, với điều kiện hoàn thành N4 và chốt toàn bộ nguồn P4.6.

### Mức B — Bản thảo có tiềm năng gửi nơi công bố phù hợp

Ngoài mức A:

- Có phạm vi kiểm độc lập lớn hơn đáng kể 10 ảnh và được khóa trước.
- Có phần chứng minh khung/vật đúng-sai bằng nhãn đủ tin cậy.
- Có so sánh với các phương pháp gần nhất và ít nhất một đối chứng mạnh hơn chỉ lọc điểm.
- Có sự cải thiện được diễn giải thống kê hợp lý, hoặc có một phát hiện thực nghiệm mới rõ và tái lập.
- Có luận điểm phân biệt với PseCo, DAVE, PrACo++, CountGD++ gốc.

### Mức C — Paper phương pháp mạnh

Ngoài mức B:

- Có một **cơ chế thực sự mới** hoặc cải tiến không tầm thường, không chỉ đổi tên của ghép điểm.
- Cơ chế làm tốt hơn đáng kể sự đánh đổi hiện tại: giảm nhầm loại **và** không mất quá nhiều vật đúng.
- Hiệu quả không phụ thuộc một vài trường hợp/cặp loại vật hoặc một bộ dữ liệu duy nhất.
- Có kiểm tra các giả thuyết thay thế và điều kiện thất bại.

**Không hứa trước đầu ra mức C.** Nếu B/C chưa đạt, vẫn có thể nộp một báo cáo nghiên cứu trung thực và đề nghị giảng viên tư vấn chiến lược viết tiếp.

---

## 12. Năm câu hỏi dự kiến giảng viên/phản biện sẽ hỏi

**Q1. Dùng CLIP sau CountGD++ có gì mới?**  
**Trả lời nên có:** Việc dùng CLIP kiểm vùng ảnh đã có trong PseCo; phát hiện–kiểm chứng cũng có trong DAVE. Phần nhóm cần chứng minh là hiệu quả và giới hạn cụ thể trên CountGD++ cho truy vấn nhiều loại/vắng mặt; nếu phát triển được bộ lọc thích ứng thì phải nêu chính xác khác biệt thuật toán và đối chứng.

**Q2. MAE Fusion 5,53 tốt hơn B0 6,77, sao lại nói bỏ sót?**  
**Trả lời nên có:** MAE chung gồm 10 câu hỏi vắng mặt, Fusion làm rất tốt ở nhóm này. Riêng 20 câu hỏi có vật, B0 = 5,70 còn Fusion = 7,80; do đó tốt hơn ở một mục tiêu nhưng kém ở mục tiêu khác.

**Q3. 31 khung sai có chắc là sai loại không?**  
**Trả lời nên có:** Hiện là kết quả của quy tắc tự động dựa trên nhãn điểm. N4 sẽ kiểm bằng người và phân biệt khung sai loại, trùng, chỉ một phần vật, bao cả vật khác và khung khó xác định.

**Q4. Vì sao không dùng tính năng mô tả loại không cần đếm mà CountGD++ đã hỗ trợ?**  
**Trả lời nên có:** Nhóm đang nghiên cứu tình huống đầu vào chỉ có ảnh và tên loại cần đếm, không mặc nhiên biết tên các loại gây nhiễu. Tuy nhiên, sẽ bổ sung đối chứng với khả năng negative prompt trong điều kiện đầu vào phù hợp, và ghi rõ nếu đối chứng được bổ sung tên lớp ngoài truy vấn.

**Q5. Vì sao chưa đủ để nói phương pháp có khả năng công bố?**  
**Trả lời nên có:** Chỉ 10 ảnh kiểm mới, ảnh thuộc cùng một bộ dữ liệu, hậu kiểm chưa hoàn tất, và cơ chế ghép điểm gần với ý tưởng nghiên cứu đã có. Muốn thuyết phục cần tính mới được làm rõ cùng đánh giá độc lập đủ rộng.

---

## 13. Việc cần làm ngay sau tài liệu này

**Ưu tiên 1 — Kết thúc phần còn dang dở**

- [ ] Xong N4: kiểm tra khung bằng người và ghi đủ người/ngày; lưu cả ví dụ Fusion loại sai *và* loại nhầm vật đúng.
- [ ] Triệu hoàn tất T0–T4 theo kế hoạch, tự chạy kiểm chéo và giải thích các lỗi lớn B0/B2.
- [ ] Kiểm tra lại nguồn P4.6, đưa đúng tệp `report`, cấu hình, tập ảnh và khoảng tin cậy vào phần phụ lục.
- [ ] Xác minh giấy phép của bản dữ liệu MUCCA đã dùng; trích dẫn tác giả, phiên bản và DOI chính thức. Trang Zenodo xác nhận quy mô 200 ảnh và DOI, nhưng phần giấy phép không hiển thị rõ trong bản dữ liệu web kiểm tại đây.

**Ưu tiên 2 — Khóa luận điểm khoa học**

- [ ] Thống nhất RQ1–RQ3 và lựa chọn giữa paper phân tích thực nghiệm hay paper phương pháp.
- [ ] Chốt cách chia tập theo ảnh, chỉ số có mặt/vắng mặt, quy tắc kiểm nhãn và đối chứng.
- [ ] Đọc đầy đủ công trình CountGD++, PseCo, DAVE, PrACo++ thay vì chỉ đọc tóm tắt để kiểm tra tính mới trước khi viết đóng góp.

**Ưu tiên 3 — Chỉ một cải tiến mới có mục tiêu**

- [ ] Nếu còn thời gian, thử một quy tắc thích ứng **hoặc** kiểm mẫu tự chọn trước lượt 2 trên tập phát triển.
- [ ] Nếu không cải thiện, giữ kết quả âm tính và hoàn thiện paper thực nghiệm. Tuyệt đối không chạy nhiều biến thể trên tập giữ riêng để lựa chọn kết quả đẹp.

---

## 14. Tài liệu tham khảo và đường dẫn kiểm chứng

### Nghiên cứu công khai

1. **Amini-Naieni, N. & Zisserman, A. (2026).** *CountGD++: Generalized Prompting for Open-World Counting.* CVPR 2026. Bản chính thức: https://www.robots.ox.ac.uk/~vgg/publications/2026/AminiNaienib26/ ; mã nguồn: https://github.com/niki-amini-naieni/CountGDPlusPlus
2. **Huang, Z. và cộng sự (2024).** *Point, Segment and Count: A Generalized Framework for Object Counting (PseCo).* CVPR 2024. https://openaccess.thecvf.com/content/CVPR2024/html/Huang_Point_Segment_and_Count_A_Generalized_Framework_for_Object_Counting_CVPR_2024_paper.html
3. **Pelhan, J. và cộng sự (2024).** *DAVE — A Detect-and-Verify Paradigm for Low-Shot Counting.* CVPR 2024. https://openaccess.thecvf.com/content/CVPR2024/html/Pelhan_DAVE_-_A_Detect-and-Verify_Paradigm_for_Low-Shot_Counting_CVPR_2024_paper.html
4. **Pacini, G. và cộng sự (2026).** *Does it Really Count? Assessing Semantic Grounding in Text-Guided Class-Agnostic Counting.* PrACo++ — arXiv:2605.02752. https://arxiv.org/abs/2605.02752 ; dự án/giao thức: https://github.com/ciampluca/PrACo
5. **Ciampi, L. và cộng sự (2026).** *MUCCA (Multi-Category Class-Agnostic Counting) Dataset.* Zenodo, bản 1.0.0, **DOI 10.5281/zenodo.19231375**. https://zenodo.org/records/19231375
6. **Jiang, R., Liu, L., Chen, C. (2023).** *CLIP-Count: Towards Text-Guided Zero-Shot Object Counting.* https://arxiv.org/abs/2305.07304

### Dữ liệu/báo cáo nội bộ nhóm

- Repo: https://github.com/minhtridaoo/CS331
- `reports/BENCHMARK_FSCD147.md` — benchmark 1.190 ảnh và giới hạn cấu hình.
- `reports/PILOT_SUMMARY.md` — 5 ảnh/15 truy vấn, B0/B2 và phân tích lỗi.
- `results/countgdpp/p4_count_cv_20261020/report.json` — khảo sát P4 trên tập phát triển.
- **Theo bản tóm tắt nhóm ngày 27/10, cần đính kèm và xác minh thêm:** `reports/P4_CLIP_EXPLORATORY_FINDINGS_20261021.md`, `reports/P4_6_UNSEEN_RESULTS_20261027.md`, `results/countgdpp/p4_n4_review_package_20261027/` (các đường dẫn này chưa được xác nhận có trên nhánh `main` khi đối chiếu, có thể ở máy hoặc nhánh khác).

> **Lưu ý về trích dẫn MUCCA:** mô tả Zenodo có một URL mẫu trích dẫn không nhất quán với DOI của bản ghi. Khi viết paper, dùng **DOI hiển thị tại trường DOI chính thức: `10.5281/zenodo.19231375`** và kiểm thông tin trích dẫn từ bản ghi gốc trước khi nộp.

---

## 15. Lời kết dành cho nhóm và giảng viên

Dự án không chỉ dừng ở việc tải mô hình CountGD++ về chạy lại. Nhóm đã tạo ra một câu hỏi thực nghiệm có giá trị: **một bộ đếm có thể đếm ra con số hợp lý nhưng lại khoanh sai đối tượng được hỏi**. Nhóm đã thử một bước xác minh ngữ nghĩa bằng CLIP và có kết quả ban đầu thuận lợi khi giảm đếm nhầm loại, đặc biệt trong những trường hợp đối tượng vắng mặt.

Điểm trưởng thành về nghiên cứu là nhóm **không che giấu tác dụng phụ**: phương pháp còn loại mất nhiều vật đúng, làm kém kết quả trên nhóm truy vấn có vật. Nếu tài liệu được phát triển thành paper, chính mâu thuẫn ấy phải trở thành trung tâm của câu chuyện — hoặc được giải quyết bằng một cơ chế mới có kiểm chứng, hoặc được phân tích đầy đủ như một phát hiện thực nghiệm có giới hạn rõ ràng.

**Khuyến nghị cuối:** hãy xây dựng **một bài nghiên cứu đáng tin trước, rồi mới lựa chọn nơi gửi công bố**. Đủ số liệu tốt chưa đủ; tính mới, đối chứng công bằng, khả năng tái lập và sự trung thực với kết quả bất lợi mới là những điều giúp giảng viên có cơ sở mạnh để hỗ trợ nhóm phát triển thành bài báo khoa học.
