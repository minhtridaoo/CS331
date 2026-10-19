# Handoff của bạn — Mô hình và inference CountGD++

**Mốc mới nhất 16/10 — đã nhận kiểm chéo của Triệu cho 14/15 query:** số đếm/GT khớp file kết quả; còn q01_1 guitars chưa có review trực tiếp. Plates hiệu chỉnh từ 0/3 theo Trí thành 3/3 đúng loại theo Triệu và ảnh đã kiểm; bản gốc giữ nguyên. Raspberries final đã giải thích đủ 14 = 4 quả mục tiêu + 1 khung trùng + 9 khung sai loại. Stage1 có 2 strawberry ở số 6/7, giải thích đủ 11 khung. **Tiếp theo:** bổ sung guitar và đối sánh q04_2 blueberries; dùng nhãn q05_2 để kiểm evaluator, không làm lại từ đầu. Giữ kế hoạch benchmark Kaggle hiện có; chưa có metric Kaggle mới. [Đối chiếu chi tiết](../results/countgdpp/b2_remaining3_20261015/TRIEU_CROSSCHECK_2026-10-16.md).

**Cập nhật 16/10/2026. Người phụ trách: bạn.**
[Handoff chung](HANDOFF.md) · [Pipeline phân công](../roadmap/PIPELINE_PHAN_CONG.md) · [Lệnh sau CUDA](../roadmap/SETUP_COUNTGDPP_SAU_CUDA.md)

## Trạng thái đã kiểm tra

- [x] Repo tại D:/MINHTRIHOCCODE/HOCKI5/CS331/CountGDPlusPlus, commit 8489f836d75eb407ae778c56cff1f72cc6f8baae; không thấy thay đổi code.
- [x] WSL Ubuntu-22.04, môi trường /root/.venvs/countgdpp, Python 3.10.12.
- [x] PyTorch 2.5.1+cu121, torchvision 0.20.1+cu121; GPU nhận được và phép tính thử trước đó thành công.
- [x] GCC/G++ 11; CUDA Toolkit package 12.1.1-1, nvcc 12.1.105.
- [x] GPU RTX A2000 Laptop 4 GB đã chạy được smoke một query; đã có số đo PyTorch allocated và B2 pilot; chưa benchmark tài nguyên đầy đủ.
- [x] transformers 4.44.2; custom op và detectron2._C import được sau import torch; inference thật đã chạy. Chưa đối chiếu log đầy đủ bộ test CUDA ops.
- [x] Có BERT và checkpoint CountGD++ ở checkpoints; script nạp được để inference.
- [x] Đã ghi SHA256, missing=0; 38 unexpected feature_map_encoder đã đối chiếu code, phù hợp đường B0 app.
- [x] B0 smoke spoon có 19 boxes/scores, GT thủ công 7; [output](../results/countgdpp/smoke_spoon/results.json).
- [ ] M3 đã có fork=14/GT7, cat=0/GT0; audit đã kiểm; còn hoàn thiện bàn giao và tài nguyên. Đã có B0/B2 5 ảnh, E1/E2 2 ảnh; chưa train.

## Việc làm ngay

**Hiện tại: đã kiểm chéo 14 query và phân loại final q05_2; còn guitar/q04_2 và evaluator.** [Lịch sử và kiểm chứng](WORKLOG_CS331.md). Fork khoanh 7 nĩa và 7 muỗng; cat không có khung. Audit đã kiểm và runner xuất schema v1 đã có. Batch 5 ảnh đã chạy và review; cả 5 query đã chẩn đoán; B2 đã có 15 query và Trí đã review đủ; M6/E1/E2 pilot trên 2 ảnh đã xong. Đã có nhãn 14 bbox q05_2, dùng kiểm evaluator; các điểm còn mở theo mốc đầu file. Không cần chạy lại ba lệnh chỉ để xác nhận hoàn tất.

Đã so khung/count và kiểm JSON prompt: đúng tên, boxes/negative rỗng. Đã đối chiếu tải trọng số và lọc gốc; query rulers không bị giữ nhầm do dấu chấm/token đặc biệt, chưa xác định cơ chế sâu bên trong gây điểm sai. Chuyển output gốc sang schema v1, bổ sung config và tài nguyên. Run cũ chưa đo thời gian/VRAM: để null kèm lý do, không suy ra từ timestamp. Đã khảo sát ngưỡng ở E1/E2 nhưng chưa đổi baseline .23 hoặc train. Sau mỗi mốc, cập nhật work log, handoff và pipeline.

## Pipeline cá nhân

1. **M1:** hoàn thành kiểm tra import, custom ops và log môi trường.
2. **M2:** tải trọng số, hash, kiểm tra nạp với config; phân tích missing/unexpected keys quan trọng.
3. **M3:** nhận một ảnh cùng ba query từ Triệu; chỉ đưa image_path/prompt vào model. Lưu đầu ra theo schema v1.
4. **M4:** mở rộng B0 sau khi Triệu ghép được ba kết quả đầu tiên. Tách mỗi run, có trạng thái lỗi riêng.
5. **M5:** B2 dùng mẫu từ chính ảnh; lưu cả hai lượt và xử lý không có mẫu.
6. **M6:** tách ngưỡng mẫu/cuối, giữ B0 đối chứng trên cùng dữ liệu. Cùng Triệu quyết định can thiệp sau khi thấy lỗi.

## Bàn giao cho Triệu

- predictions.jsonl chuẩn trong pipeline phân công, cùng run_config.json và overlay.
- ID đúng, khung xyxy pixel ảnh gốc, count khớp số khung.
- execution_status=error và count=null nếu OOM/crash, không thay bằng 0.
- Lệnh tái chạy, nguồn/hash trọng số, môi trường và thời gian/VRAM.
- Đầu ra gốc của repo là nguồn tham khảo; bạn viết bước chuyển đổi sang schema chung.

Mốc đầu tiên chỉ cần một ảnh/ba query thật. Triệu có thể viết evaluator trước bằng fixture giả, nên bạn không cần đợi đủ 20–30 ảnh.

## Khi viết adapter

- process_folder.py có luồng khởi tạo/chạy ở cấp module, không có bảo vệ main; tránh import nguyên file như một thư viện không tác dụng phụ.
- Script gốc đọc prompts JSON riêng và luôn mở positive.exemplars.image. Nếu thử B0 qua script gốc: dùng chính ảnh đầu vào, boxes rỗng và negative rỗng; kiểm tra hành vi trước khi mở rộng.
- Chạy từng query phải có thư mục/ID riêng, tránh ghi đè results.json. Mỗi ảnh phải dùng đúng ảnh đầu vào cho nhánh exemplar rỗng.
- Giữ chính xác logic lọc gốc khi làm B0; mọi thay đổi lọc là cấu hình khác, không sửa âm thầm.
- Kiểm tra tọa độ và overlay bằng mắt, không chỉ count.
- Lưu diff của adapter ngoài hoặc cùng commit model, không trình bày code đã sửa như nguyên bản tác giả.

## Nhật ký bàn giao buổi sau

- Chặng hoàn thành:
- File/log và lệnh:
- Kết quả kiểm tra:
- Trở ngại:
- Việc tiếp theo:
- File đã gửi cho Triệu:

Đây là mẫu nhật ký chưa điền, không phải xác nhận đã gửi file hoặc có kết quả.
