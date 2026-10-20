# Chạy CountGD++ theo cấu hình paper trên Kaggle

Cập nhật 20/10/2026. Notebook: [COUNTGDPP_FSCD147_KAGGLE.ipynb](COUNTGDPP_FSCD147_KAGGLE.ipynb).

## Trạng thái

**Đã có run của Trí chạy đủ 1.190 ảnh; kiểm tại workspace ngày 20/10.** Run `full_20261015T080230Z`: MAE **8.336975**, RMSE **24.637626**, khớp số từng ảnh/log/metrics. Xem [báo cáo xác nhận và giới hạn](../reports/BENCHMARK_FSCD147.md). Run mang ngày 15/10 theo log, khác ngày audit.

Các bước dưới đây giữ để tái chạy khi cần; công việc ngay tiếp hiện tại là phần 2–3 pilot. Không phải bắt đầu lại Kaggle. File run_config ở gốc gói là bản chuẩn bị, dùng bản trong `full_*` cho trạng thái run hoàn tất.

## Cách làm

1. Tạo notebook trên Kaggle, dùng chức năng Import/Upload Notebook để mở file ipynb này.
2. Bật GPU và Internet. Chạy từng cell; bắt đầu cell 1 và 2 để kiểm GPU/môi trường. Nếu lỗi, giữ log và gửi lại, không chạy tiếp các cell phụ thuộc.
3. Cell 3 tải checkpoint, ảnh FSCD-147, synthetic exemplars và super-resolution crops từ các link tác giả. Nếu Drive giới hạn tải: tải archive từ README, đưa vào Kaggle Dataset riêng tư, gắn vào notebook và điền LOCAL. Không công khai checkpoint/dữ liệu chỉ để khắc phục tải lỗi.
4. Cell 4 kiểm đủ 1.190 ảnh test và synthetic, lưu hash checkpoint và annotation. Kiểm crops có sẵn; lần chạy thật còn có thể phát hiện crop của ảnh cụ thể bị thiếu.
5. Cell 5 chạy script inference gốc, không đổi threshold, không bật debug. Mỗi lần chạy có thư mục riêng. Không hỗ trợ resume theo ảnh; bị ngắt thì chưa hoàn thành benchmark.
6. Cell 6 kiểm đủ tên ảnh, tính lại MAE/RMSE từ log, đối chiếu số script in ra, xuất counts.csv, metrics.json và ZIP. Tải ZIP hoặc lưu output bằng Save Version.

## Cấu hình và cách so

- Repo pin: 8489f836d75eb407ae778c56cff1f72cc6f8baae.
- FSCD-147 test; cấu hình text + synthetic + 3 pseudo-exemplars + adaptive cropping, confidence 0.23 theo config upstream; không dùng 3 exemplar thủ công.
- Python 3.10, torch 2.5.1 cu121, torchvision 0.20.1, transformers 4.44.2. Đây là môi trường triển khai Kaggle, không tuyên bố khớp mọi phiên bản môi trường paper. Detectron2 ghi lại commit thực tế; toàn bộ packages được lưu.
- Paper v2 Table 1, Ours(t+p+s): MAE 8.39, RMSE 27.03. Đây là số tham chiếu của paper. Run nhóm đã kiểm đạt 8.336975 / 24.637626; số thấp hơn chưa chứng minh có cải tiến hoặc khớp mọi điều kiện tái lập.
- Repo hiện thiếu test_fscd147.py mà README nhắc. Notebook dùng count metrics của engine_inference.py và tính lại từ log; không tuyên bố tái lập evaluator AP/AP50 của script bị thiếu.
- Notebook được thiết kế dùng thuật toán upstream. Log run báo working tree có thay đổi chưa commit nhưng gói không có diff; vì vậy chưa khẳng định mọi file chạy giống nguyên trạng repo. Lần chạy sau lưu git diff/status. CUDA toolkit khác major 12 hoặc môi trường build lỗi thì dừng để xử lý.
- Không chỉnh threshold theo test để khớp paper. Nếu số lệch, audit checkpoint/code/assets/protocol và báo độ lệch.
- MAE B0=19.4/B2=22.0 trên 5 ảnh/15 query dev phải để bảng riêng. Không tính phần trăm cải thiện giữa hai tập khác nhau. Muốn so trực tiếp cần chạy các cấu hình trên cùng tập và evaluator.

## Nguồn

- [README chính thức](https://github.com/niki-amini-naieni/CountGDPlusPlus)
- [Paper v2, Table 1](https://arxiv.org/html/2512.23351v2#S6.T1)

## Bước tiếp theo

Giữ nguyên gói kết quả đã tải và mở [báo cáo benchmark](../reports/BENCHMARK_FSCD147.md) khi cần báo cáo thầy. Tiếp tục [phần 2](PHAN_2_DANH_GIA.md) → [phần 3](PHAN_3_TONG_KET.md) của pilot; không cần rerun benchmark để làm hai phần này.
