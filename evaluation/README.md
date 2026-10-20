# Evaluator pilot

[Hướng dẫn tự chạy phần 2](../roadmap/PHAN_2_DANH_GIA.md).

`evaluate_pilot.py` là script CPU dùng thư viện chuẩn, đọc predictions đã có; không train hoặc gọi model. Chuẩn bị ngày 19/10/2026. Chưa chạy self-test/dữ liệu thật; chỉ kiểm cú pháp trong lượt chuẩn bị. Người dùng chạy `--self-test` trước, rồi mới chạy với `--out`.

Kết quả lưu riêng trong `results/countgdpp/pilot_eval_<ngày>`, không ghi đè B0/B2 gốc. `manual_check` chỉ tổng hợp nhãn thủ công q05_2, không phải evaluator định vị tự động toàn tập.
