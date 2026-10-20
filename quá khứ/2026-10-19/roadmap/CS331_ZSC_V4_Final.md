# CS331 — Roadmap Zero-Shot Object Counting với CountGD++

**Mốc mới nhất 16/10 — đã nhận kiểm chéo của Triệu cho 14/15 query:** số đếm/GT khớp file kết quả; còn q01_1 guitars chưa có review trực tiếp. Plates hiệu chỉnh từ 0/3 theo Trí thành 3/3 đúng loại theo Triệu và ảnh đã kiểm; bản gốc giữ nguyên. Raspberries final đã giải thích đủ 14 = 4 quả mục tiêu + 1 khung trùng + 9 khung sai loại. Stage1 có 2 strawberry ở số 6/7, giải thích đủ 11 khung. **Tiếp theo:** bổ sung guitar và đối sánh q04_2 blueberries; dùng nhãn q05_2 để kiểm evaluator, không làm lại từ đầu. Giữ kế hoạch benchmark Kaggle hiện có; chưa có metric Kaggle mới. [Đối chiếu chi tiết](../../../results/countgdpp/b2_remaining3_20261015/TRIEU_CROSSCHECK_2026-10-16.md).

**Phiên bản V4.3 — cập nhật 16/10/2026 (Asia/Bangkok).**
**Trạng thái: M4 đã chạy/review 5 ảnh MUCCA nội bộ, 15 query; đã chẩn đoán 5 query/2 ảnh; B2 đã chạy đủ 5 ảnh/15 query và Trí đã review bằng mắt đủ 15 query. M6/E1/E2 pilot chỉ trên 2 ảnh. Triệu đã kiểm chéo 14/15 query, q05_2 đã có phân loại final; chưa train, còn tài nguyên, guitar/q04_2 và evaluator.**
[Lịch sử và lệnh tiếp theo](../HANDOFF/WORKLOG_CS331.md).
**Phân công:** bạn phụ trách mô hình; Triệu phụ trách dữ liệu và lập trình evaluator.
- [Pipeline phân công và định dạng bàn giao](PIPELINE_PHAN_CONG.md).
- [Handoff của bạn](../HANDOFF/HANDOFF_MODEL.md) · [Handoff Triệu](../HANDOFF/HANDOFF_TRIEU.md).
- [Việc của bạn ngay sau CUDA](SETUP_COUNTGDPP_SAU_CUDA.md).

- [Handoff mới nhất — 16/10/2026](../HANDOFF/HANDOFF_CS331_2026-10-16.md).
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
| CountGD++ có repo chính thức, README ghi CVPR 2026 và liên kết checkpoint | Đã clone snapshot, tải BERT/checkpoint và chạy smoke; kiểm đầy đủ key khi nạp còn chờ |
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

Lịch tính theo sản phẩm hoàn thành, không phải lời hứa tốc độ chạy. **Đã bắt đầu triển khai và có smoke đầu tiên ngày 13/10/2026.** Chưa áp lại lịch 6 tuần hoặc hạn nộp của bản cũ.

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

Kiểm tra trực tiếp ngày 13/10/2026:

- Checkout: D:/MINHTRIHOCCODE/HOCKI5/CS331/CountGDPlusPlus; commit 8489f836d75eb407ae778c56cff1f72cc6f8baae.
- WSL Ubuntu-22.04; /root/.venvs/countgdpp dùng Python 3.10.12.
- PyTorch 2.5.1+cu121, torchvision 0.20.1+cu121; GPU được nhận và phép tính thử đã đạt.
- GCC/G++ 11; CUDA Toolkit 12.1.1-1, nvcc 12.1.105.
- RTX A2000 Laptop GPU 4096 MiB VRAM; đã chạy B0/B2 pilot; có số đo allocated trong script, chưa benchmark hiệu năng đầy đủ.
- transformers 4.44.2; custom op và detectron2._C import đạt sau import torch; inference thật đã chạy. Chưa lưu kiểm đầy đủ bộ test CUDA ops.
- Đã có BERT và trọng số CountGD++ trong checkpoints; chạy ra output spoon. Đã audit missing=0, 38 key dư không dùng trong app; có hash local và báo cáo ngày 14/10.

Python mặc định của Windows là 3.14, khác môi trường đồ án. Lỗi pip “No matching distribution” trước đó được xử lý bằng chọn rõ Python WSL 3.10. Từ đây chạy cài đặt/build trong đúng môi trường, không quay lại pip Windows.

**Việc tiếp theo:** E1/E2 pilot đã xong; [review 15 query và phân loại lỗi từng bbox](../../../results/countgdpp/b2_remaining3_20261015/USER_VISUAL_REVIEW.md). Nối evaluator song song. Không cần cài lại các phần đã đạt. GPU cloud vẫn là phương án nếu OOM; chưa xác nhận quota.

P0–P3 chưa cần synthetic exemplar, dịch vụ tạo ảnh hoặc super-crop. B0/B2 là đối chứng thành phần, không đại diện toàn bộ cấu hình đạt điểm paper.

## 7. Phân công và mốc tiếp tục

**Nguồn phân công chi tiết:** [PIPELINE_PHAN_CONG.md](PIPELINE_PHAN_CONG.md). Hai nhánh dùng schema v1 ở đó; không tự thay tên trường/ID riêng.

| Người | Làm ngay | Mốc bàn giao đầu tiên |
|---|---|---|
| Bạn | M4: chạy ảnh đầu, kiểm output và ghép evaluator | M3: 3 dự đoán B0 thật của một ảnh, metadata và overlay |
| Triệu | T1–T2: 5 ảnh/15 query có nhãn; T3–T4: viết và kiểm evaluator trên CPU | manifest + đầu vào không GT; evaluator đạt fixture biết trước đáp án |
| Cả hai | Chốt ID/prompt, kiểm nhãn một ảnh | Ghép 3 dự đoán đầu tiên và kiểm tra khung bằng mắt |

### Trạng thái của bạn

- [x] Clone CountGD++ và ghi commit.
- [x] Dựng Python 3.10, PyTorch GPU, GCC và CUDA Toolkit.
- [x] Thư viện/extension import được và inference thật đã chạy; chưa xác nhận đầy đủ bộ test CUDA ops.
- [x] Tải BERT/checkpoint, script nạp và chạy spoon.
- [x] Audit key/hash đã xem xét; runner xuất schema/config đã kiểm trên cat cũ.
- [ ] Đo peak VRAM/inference thuần và nối evaluator; M3 chưa hoàn tất toàn bộ bàn giao.
- [ ] B0 một ảnh/ba query; xuất theo schema chung.
- [ ] B0 trên pilot; B2 và thí nghiệm ngưỡng sau đó.

### Trạng thái nhánh Triệu

- [ ] 5 ảnh ban đầu, 15 query và nhãn đã kiểm.
- [x] Đã chuyển gói Triệu sang manifest và inference_inputs tách GT ngày 14/10; cần Triệu kiểm chéo.
- [ ] Code evaluator và kiểm tra với fixture giả.
- [ ] Ghép kết quả B0 thật, kiểm overlay với bạn.
- [ ] Mở rộng 20–30 ảnh dev, giữ holdout riêng.

Đã nhận và kiểm gói Triệu gồm 10 ảnh/30 query có mặt; thiếu query vắng mặt và chưa xác nhận evaluator. Không đánh dấu toàn nhánh hoàn thành. Không đợi cả bộ 20–30 ảnh mới ghép việc. B0 một ảnh là mốc đầu, chưa train hoặc mở toàn bộ B0–B6.

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

**13/10/2026:** thay kế hoạch DualCount/T2ICount bằng CountGD++; giữ yêu cầu X/Y, ưu tiên khảo sát hướng A; bắt đầu B0/B2; bỏ việc chốt can thiệp trước thực nghiệm; cập nhật pipeline và handoff. Lần cập nhật đầu chỉ sửa tài liệu. Sau đó người dùng đã clone repo, dựng Python/PyTorch và cài CUDA. Cập nhật V4.3 bổ sung phân công, handoff riêng và hướng dẫn sau CUDA; tại thời điểm đó vẫn chưa tải/nạp trọng số, chạy CountGD++ hoặc huấn luyện.

**13/10/2026 — sau smoke đầu tiên:** người dùng đã hoàn thành cài phụ thuộc và tải trọng số; B0 spoon xuất 19 khung, GT thủ công 7. Đã kiểm file output và import extension. Cập nhật M3 1/3 query; tiếp theo fork/cat, chưa train. Lịch sử chi tiết và quy tắc đồng bộ sau mỗi mốc nằm trong work log; chưa đóng P0 vì còn audit/metadata/tài nguyên.

**13/10/2026 — sau fork/cat:** đã kiểm đủ ba output thật: spoon=19/GT7, fork=14/GT7, cat=0/GT0; fork khoanh cả hai loại, cat không có khung. M3 inference đủ 3/3; chưa hoàn tất schema, audit và đo tài nguyên. Không suy rộng từ một ảnh sang kết luận benchmark hoặc nguyên nhân lỗi.
