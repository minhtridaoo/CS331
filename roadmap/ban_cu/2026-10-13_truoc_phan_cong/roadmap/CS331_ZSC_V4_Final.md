# CS331 — Roadmap Zero-Shot Object Counting với CountGD++

**Phiên bản V4.2 — cập nhật 13/10/2026 (Asia/Bangkok).**
**Trạng thái: đã chốt kế hoạch triển khai khảo sát; chưa có kết quả inference của nhóm.**

- [Handoff mới nhất — 13/10/2026](../HANDOFF_CS331_2026-10-13.md).
- [Pipeline và quy ước thực nghiệm](PIPELINE_COUNTGDPP.md).
- [Bản V4.1 được giữ nguyên để tra cứu](ban_cu/CS331_ZSC_V4_1_2026-10-07.md).

## 1. Quyết định có hiệu lực

1. **CountGD++ là baseline chính.** Giữ lựa chọn này trong đợt khảo sát đầu tiên. Không chờ DualCount, không mở thêm cuộc so sánh chọn model.
2. **Mục tiêu: đếm đúng loại vật thể được hỏi trên cùng một ảnh.** Giữ trường hợp X và Y đều có mặt để bám yêu cầu số 3 của thầy.
3. **Hướng A là ưu tiên khảo sát:** khi hỏi một loại không có trong ảnh, mô hình có vẫn đếm những vật khác không? Đây là một phần liên quan của vấn đề chọn đúng đối tượng, chưa thay thế toàn bộ trường hợp X/Y cùng có mặt.
4. **Bắt đầu bằng checkpoint công bố, chưa train/fine-tune.** Chỉ quyết định can thiệp sau khi có lỗi lặp lại được trên dữ liệu phát triển.
5. **Lượt đầu chỉ B0/B2.** B0 = văn bản một lượt; B2 = văn bản → tự chọn mẫu → lượt hai. Chưa chạy toàn bộ B0–B6.
6. Chỉnh ngưỡng là đối chứng đơn giản phải thử trước. Chưa gọi chỉnh ngưỡng, negative prompting hay “thêm bộ kiểm tra ngữ nghĩa” là đóng góp mới.
7. Không mở nhánh Deep Learning, giao diện tương tác, paraphrase hoặc huấn luyện nhiều model trong đợt này.
8. Chưa xác nhận deadline chính thức, tên đề tài được duyệt hay yêu cầu bắt buộc huấn luyện. Những điều này không chặn việc dựng môi trường và khảo sát.

Các quyết định này thay thế ưu tiên DualCount/T2ICount, mốc chọn model 20/10 và các can thiệp fine-tune đã định trước trong V4.1. Code CLIP-Count cũ chỉ còn để tra cứu.

## 2. Bài toán sẽ giải quyết

**Tên làm việc:** Đánh giá và nghiên cứu giảm lỗi đếm sai đối tượng theo truy vấn trong Zero-Shot Object Counting với CountGD++.

**Đầu vào được phép:** một ảnh I và tên loại vật thể q do người dùng muốn đếm.
**Đầu ra:** số lượng dự đoán và vị trí các vật thể được tính vào số lượng đó.

Ví dụ minh họa, không phải kết quả đã chạy: một ảnh có 5 quả táo, 2 chiếc cốc, không có xe đạp.

| Truy vấn | Kết quả mong muốn | Lỗi cần phát hiện |
|---|---|---|
| Đếm táo | 5, các vị trí thuộc táo | Đếm thiếu/thừa hoặc lấy nhầm cốc |
| Đếm cốc | 2, các vị trí thuộc cốc | Vẫn chọn các quả táo khi đổi câu hỏi |
| Đếm xe đạp | 0, không có vị trí nào | Đếm táo/cốc dù xe đạp vắng mặt |

Hai số đếm bằng nhau không tự chứng minh mô hình bỏ qua câu hỏi: X và Y có thể có cùng số lượng thật. Phải kiểm tra vị trí dự đoán. Chỉ số MAE tốt cũng không đủ chứng minh mô hình chọn đúng lớp.

**Quan hệ với yêu cầu thầy:**

- Nếu yêu cầu số 3 bắt buộc: trường hợp X/Y cùng hiện diện phải có trong đánh giá chính; hướng A là phần hỗ trợ.
- Nếu thầy cho phép tập trung vào vật thể vắng mặt: có thể thu hẹp tên đề tài sau khảo sát thành “Nghiên cứu giảm lỗi đếm nhầm đối tượng vắng mặt trong Zero-Shot Object Counting với CountGD++”.
- Chưa có bằng chứng thầy đã duyệt việc thu hẹp đó. Hiện chuẩn bị chung cả hai kiểu truy vấn, không phải hai đồ án hay hai pipeline độc lập.

Zero-shot không có nghĩa mô hình chưa từng được huấn luyện. Đợt đầu của nhóm không cập nhật trọng số. Khi báo cáo, nêu chính xác split lớp và dữ liệu của checkpoint; không khẳng định mô hình nền chưa từng thấy mọi lớp thử nghiệm. “Không nhập exemplar thủ công” cũng không có nghĩa bên trong không dùng pseudo-exemplar.

## 3. Điều đã xác minh và điều còn là giả thuyết

| Nội dung | Mức bằng chứng hiện có |
|---|---|
| CountGD++ có repo chính thức, README ghi CVPR 2026 và liên kết checkpoint | Đã kiểm tra tài liệu; chưa tải/nạp checkpoint ở workspace này |
| Demo và pipeline đánh giá paper không giống nhau | README nói demo chưa dùng pseudo-exemplar/adaptive cropping |
| Wrapper PrACo đã kiểm tra dùng ngưỡng 0.23 cho chọn mẫu và lọc cuối | Đã đọc mã ở commit được ghi trong pipeline |
| Pseudo-exemplar có thể làm lỗi chọn nhầm lớp lan sang lượt hai | Giả thuyết cần kiểm tra, chưa phải kết quả của nhóm |
| Cấu hình có nhãn lớp loại trừ khác cấu hình chỉ nhận I + q | Khác điều kiện đầu vào; phải báo riêng |
| Synthetic exemplar có thể dùng ảnh tham chiếu | Cần ghi nguồn và cách chọn ảnh; không suy ra kết quả tác giả không hợp lệ |
| Hướng A còn đủ khoảng trống để đề xuất phương pháp mới | Chưa biết, quyết định sau pilot và đối chứng đơn giản |

Ba loại bằng chứng phải tách rõ: số tác giả báo cáo; số nhóm tự tái hiện đúng protocol; số nhóm chạy trên protocol riêng.

## 4. Pipeline tổng thể

~~~mermaid
flowchart TD
    A["Ảnh và tên vật thể cần đếm"] --> B["B0: dự đoán một lượt bằng văn bản"]
    B --> C["Lưu số đếm, khung, điểm tin cậy"]
    B --> D["B2: chọn pseudo-exemplar từ chính ảnh"]
    D --> E["Lượt hai và lọc kết quả cuối"]
    E --> C
    C --> F["Đối chiếu nhãn: X, Y và lớp vắng mặt"]
    F --> G["Khảo sát riêng ngưỡng chọn mẫu và ngưỡng cuối"]
    G --> H["Chọn một lỗi còn tồn tại trên dev"]
    H --> I["Một can thiệp có đối chứng"]
    I --> J["Khóa cấu hình rồi đánh giá holdout"]
~~~

Nhãn thật chỉ đi vào bộ đánh giá, không truyền vào B0/B2. Pipeline chạy, dữ liệu cần lưu, thí nghiệm ngưỡng và chỉ số nằm trong [PIPELINE_COUNTGDPP.md](PIPELINE_COUNTGDPP.md).

## 5. Các giai đoạn và điều kiện hoàn thành

Lịch tính theo sản phẩm hoàn thành, không phải lời hứa tốc độ chạy. **Ngày bắt đầu dự kiến: 14/10/2026.** Chưa áp lại lịch 6 tuần hoặc hạn nộp của bản cũ.

| Giai đoạn | Việc chính | Điều kiện hoàn thành |
|---|---|---|
| P0 — Chạy được | Pin code, dựng môi trường, tải đúng checkpoint, chạy B0 một ảnh | Nạp trọng số đúng; xuất count/boxes/scores; ghi môi trường, thời gian, VRAM hoặc lỗi cụ thể |
| P1 — Có bộ khảo sát | Chuẩn bị 20–30 ảnh dev, kiểm tra X/Y và lớp vắng mặt; chạy B0 | Manifest có nguồn, nhãn, truy vấn, split; có kết quả và hình overlay |
| P2 — Kiểm tra pseudo | Cài/đối chiếu B2, giữ điều kiện khác khớp B0 | Lưu cả hai lượt, mẫu đã chọn và xử lý khi không có mẫu; có bảng B0/B2 |
| P3 — Đối chứng đơn giản | Tách tau_sample/tau_final; thử E1/E2, E3 khi cần | Có đánh đổi giữa lỗi vắng mặt và chất lượng trên lớp có mặt |
| P4 — Chọn một can thiệp | Phân tích lỗi còn lại; kiểm tra phương pháp liên quan phù hợp | Một giả thuyết cụ thể, một phương pháp ứng viên, một đối chứng và tiêu chí đánh giá |
| P5 — Kiểm chứng và báo cáo | Khóa protocol, chạy holdout, phân tích lỗi và giới hạn | Bảng kết quả tái lập, hình đúng/sai, số đo tài nguyên, kết luận đúng mức bằng chứng |

Mục tiêu đợt đầu là P0–P3. Nếu môi trường mất nhiều thời gian, điều chỉnh lịch theo log thực tế; không vừa gỡ môi trường vừa mở thêm model.

### 5.1. Khi nào tiếp tục hướng A?

- **Lỗi vắng mặt có lặp lại, còn tồn tại sau chỉnh ngưỡng và gây đánh đổi rõ với truy vấn có mặt:** tiếp tục phân tích hướng A.
- **Chỉnh ngưỡng đã xử lý tốt:** ghi nhận giải pháp kỹ thuật; chưa cần thêm module phức tạp hay tuyên bố phương pháp mới. Đánh giá đủ yêu cầu môn học khi biết rubric.
- **Lỗi vắng mặt ít nhưng X/Y vẫn nhầm nhau:** chuyển trọng tâm phân tích sang chọn nhầm lớp trên cùng baseline.
- **Cả hai ít lỗi trên pilot:** mở rộng một bộ dev có kiểm soát để kiểm tra tính đại diện; không tạo kết luận về “bug chưa ai giải quyết” từ vài ví dụ.
- **Cải tiến chỉ làm mọi số đếm giảm về 0:** không đạt mục tiêu. Phải giữ chất lượng trên truy vấn có đối tượng.
- **Giải pháp đã công bố xử lý tốt lỗi đang xét:** ghi rõ là áp dụng/tái hiện. Chỉ nghiên cứu phần còn thiếu nếu có bằng chứng và đủ thời gian.

Không đặt trước một ngưỡng “đủ nhiều lỗi” tùy ý để đảm bảo có đề tài. Ghi số ca, mức sai, loại ảnh và độ bất định; quyết định trên dev, không chọn hướng dựa trên holdout.

## 6. Môi trường và tài nguyên

Kiểm tra ngày 13/10/2026:

- GPU local: NVIDIA RTX A2000 Laptop GPU, 4096 MiB VRAM.
- Python trên PATH: C:/Python314/python.exe. Git và chương trình wsl.exe có trên PATH; chưa xác minh Linux distro đã sẵn sàng.
- Chưa thấy conda trên PATH; không kết luận máy chưa cài ở nơi khác.
- Thư mục code/ hiện chỉ có CLIP-Count; chưa có checkout CountGD++ trong dự án.

Repo hướng dẫn Python 3.10 và công cụ biên dịch trên Ubuntu. Dựng môi trường riêng theo README; không cài chồng vào Python 3.14 đang có. Bắt đầu batch 1, ghi bộ nhớ đỉnh; 4 GB chưa được kiểm chứng đủ cho cấu hình này.

**Thứ tự xử lý:** xác minh môi trường Linux/WSL phù hợp → nếu không sẵn hoặc bị giới hạn VRAM, dùng môi trường GPU đám mây có thể truy cập → lưu log tái lập. Chưa giả định tài khoản/quota GPU cloud đã có. Không tự thay mô hình hay giảm kích thước ảnh để rồi gọi kết quả là tái hiện nguyên bản. Nếu đổi resize/precision/crop, ghi thành cấu hình riêng.

Chưa cần tạo synthetic exemplar, dịch vụ tạo ảnh trả phí hoặc super-crop cho P0–P3. B0/B2 là đối chứng thành phần, không đại diện toàn bộ cấu hình đạt điểm paper.

## 7. Công việc ngày mai — 14/10/2026

**Mốc tối thiểu:** B0 chạy được một ảnh với X, Y, một lớp vắng mặt và có đủ đầu ra để xem mô hình đang đếm vật nào. Nếu chưa chạy được, bàn giao lỗi môi trường cụ thể và bước xử lý tiếp theo, không ghi “đã hoàn thành baseline”.

### Bạn — triển khai môi trường và inference

- [ ] Đọc handoff mới nhất và pipeline; xác nhận môi trường GPU sẽ dùng.
- [ ] Clone repo chính thức, pin commit, ghi checkpoint/config và phụ thuộc.
- [ ] Kiểm tra nạp trọng số, lỗi missing/unexpected keys quan trọng và custom ops.
- [ ] Chạy B0 cho ba truy vấn trên cùng một ảnh, giữ thông số xử lý ảnh giống nhau.
- [ ] Lưu count, boxes, scores, hình overlay, thời gian, VRAM và metadata.

### Triệu — dữ liệu và kiểm tra nhãn

- [ ] Chọn trước 5 ảnh rõ ràng có ít nhất hai loại vật khác nhau để hai bạn kiểm tra chéo.
- [ ] Ghi số lượng thật của X/Y; xác nhận bằng mắt lớp vắng mặt, không suy ra từ thiếu annotation.
- [ ] Ghi nguồn ảnh, quyền sử dụng, ID và tên truy vấn tiếng Anh thống nhất.
- [ ] Mở rộng dần thành 20–30 ảnh dev; có cặp X/Y khác số lượng và một số cặp bằng số lượng.
- [ ] Kiểm tra overlay B0 với bạn; đánh dấu ca sai lớp, thiếu/thừa và trường hợp chưa rõ.

Đây là phân công đề xuất để bắt đầu, không phải xác nhận Triệu đã nhận việc. Hai người kiểm tra chéo ít nhất các ca dùng làm ví dụ trong báo cáo.

**Chưa đưa vào ngày mai:** fine-tune, toàn bộ B0–B6, chạy nhiều seed train, xây UI, so sánh thêm DualCount/Count Anything, hoặc chọn tên một module mới.

## 8. Sản phẩm cần giữ

1. Môi trường chạy và lệnh tái lập.
2. Manifest dữ liệu/nhãn, quy ước split và nguồn ảnh.
3. Kết quả theo từng ảnh–truy vấn–cấu hình, gồm dự đoán trước/sau pseudo.
4. Bảng so sánh B0/B2 và ngưỡng; hình minh họa cả ca đúng lẫn ca sai.
5. Nhật ký quyết định: lỗi nào được chọn, vì sao, bằng chứng nào hỗ trợ.
6. Khi có cải tiến: baseline khớp điều kiện, ablation, đánh đổi tài nguyên và đánh giá holdout.
7. Báo cáo/slide chỉ gọi là “cải thiện” khi số nhóm tự chạy thực sự hỗ trợ kết luận.

Demo đếm tương tác đã phác thảo trước đây là mô phỏng theo kịch bản, không phải kết quả CountGD++ và không được đưa vào bảng thực nghiệm.

## 9. Những việc chỉ xác nhận khi cần

- Với thầy: deadline, mức đóng góp cần có, việc tập trung riêng hướng A có được chấp nhận không.
- Với môi trường: GPU/quota, bộ phụ thuộc và chi phí chạy.
- Sau pilot: quy mô holdout và yêu cầu annotation để đo vị trí tự động.

Không đặt lại câu hỏi chọn model nếu chưa gặp trở ngại kỹ thuật đã được ghi log hoặc yêu cầu mới từ thầy.

## 10. Nguồn và lịch sử

- [CountGD++ — repo chính thức, hướng dẫn và checkpoint](https://github.com/niki-amini-naieni/CountGDPlusPlus).
- [CountGD++ — bài báo, Bảng 3 và Phụ lục C.4](https://arxiv.org/html/2512.23351v2).
- [PrACo — bài báo](https://arxiv.org/html/2409.15953v2).
- [PrACo++ — bài báo và bối cảnh đánh giá nhiều lớp](https://arxiv.org/html/2605.02752v1).
- [PrACo — mã benchmark đã kiểm tra](https://github.com/ciampluca/PrACo/blob/34c7a8d3fdff5f77741bc8f598e6db8cfc50655b/benchmark/benchmark.py).
- [V4.1 lịch sử](ban_cu/CS331_ZSC_V4_1_2026-10-07.md).

**13/10/2026:** thay kế hoạch DualCount/T2ICount bằng CountGD++; giữ yêu cầu X/Y, ưu tiên khảo sát hướng A; bắt đầu B0/B2; bỏ việc chốt can thiệp trước thực nghiệm; cập nhật pipeline và handoff. Lần cập nhật này chỉ sửa tài liệu, chưa clone model, tải trọng số, chạy inference hoặc huấn luyện.
