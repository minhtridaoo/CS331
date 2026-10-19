# CS331 — Điểm tiếp tục hiện hành

**Ưu tiên bổ sung 15/10 — chuẩn bị đánh giá theo paper trên Kaggle:** người dùng yêu cầu chạy FSCD-147 test; đã tạo [notebook và hướng dẫn](../roadmap/KAGGLE_PAPER_EVAL.md), chưa chạy Kaggle/chưa có metric mới. Tiếp theo import notebook, bật GPU/Internet và kiểm cell 1–2. Kết quả nhóm khác không phải kết quả của Triệu. Giữ kết quả pilot bên dưới; không so trực tiếp MAE khác tập dữ liệu.

**Mốc mới nhất 16/10 — đã nhận kiểm chéo của Triệu cho 14/15 query:** số đếm/GT khớp file kết quả; còn q01_1 guitars chưa có review trực tiếp. Plates hiệu chỉnh từ 0/3 theo Trí thành 3/3 đúng loại theo Triệu và ảnh đã kiểm; bản gốc giữ nguyên. Raspberries final đã giải thích đủ 14 = 4 quả mục tiêu + 1 khung trùng + 9 khung sai loại. Stage1 có 2 strawberry ở số 6/7, giải thích đủ 11 khung. **Tiếp theo:** bổ sung guitar và đối sánh q04_2 blueberries; dùng nhãn q05_2 để kiểm evaluator, không làm lại từ đầu. Giữ kế hoạch benchmark Kaggle hiện có; chưa có metric Kaggle mới. [Đối chiếu chi tiết](../results/countgdpp/b2_remaining3_20261015/TRIEU_CROSSCHECK_2026-10-16.md).

**Cập nhật mới nhất: 16/10/2026 (Asia/Bangkok). Roadmap V4.3.**

| Cần làm gì | Mở tài liệu |
|---|---|
| Lịch sử công việc và lệnh tiếp theo | [Work log](WORKLOG_CS331.md) |
| Xem trạng thái chung | [Handoff chung ngày 16/10](HANDOFF_CS331_2026-10-16.md) |
| Phần việc của bạn | [Handoff mô hình](HANDOFF_MODEL.md) |
| Phần việc Triệu | [Handoff dữ liệu/evaluator](HANDOFF_TRIEU.md) |
| Ghép hai nhánh và định dạng file | [Pipeline phân công](../roadmap/PIPELINE_PHAN_CONG.md) |
| Bạn làm gì sau CUDA | [Hướng dẫn cài thư viện/build/checkpoint](../roadmap/SETUP_COUNTGDPP_SAU_CUDA.md) |
| Phạm vi và các giai đoạn | [Roadmap V4.3](../roadmap/CS331_ZSC_V4_Final.md) |
| Quy tắc thực nghiệm | [Pipeline CountGD++](../roadmap/PIPELINE_COUNTGDPP.md) |

**Đã đạt:** môi trường, import extension, BERT/checkpoint và đủ ba query smoke: spoon=19/GT7, fork=14/GT7, cat=0/GT0. Fork khoanh cả muỗng; cat không có khung.
**Bạn làm tiếp:** q05_2 final đã có nhãn 14 khung; dùng để kiểm evaluator. Triệu bổ sung guitar và làm rõ q04_2. Giữ nhánh Kaggle theo hướng dẫn hiện có, chưa có kết quả benchmark mới. Chưa train hoặc chọn ngưỡng theo holdout. [Lệnh M4](../experiments/countgdpp/m4_inputs/README.md).
**Triệu:** đã cung cấp dữ liệu và review 14/15 query; còn guitar, độ bao phủ q04_2, absent và evaluator. Chưa xác nhận evaluator đã chạy.

Giữ CountGD++ làm baseline, kiểm tra X/Y và lớp vắng mặt. Đã chạy B0/B2 5 ảnh; E1/E2 pilot 2 ảnh; chưa train. Điểm mở phiên sau là file này trong thư mục HANDOFF/, không phải đường dẫn root trước khi di chuyển tài liệu.

**Quy tắc tiếp tục:** sau mỗi mốc được xác nhận, nối thêm work log và đồng bộ handoff/pipeline; chỉ đánh dấu xong khi có bằng chứng.
