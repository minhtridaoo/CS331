# Evaluator pilot

[Hướng dẫn tự chạy phần 2](../roadmap/PHAN_2_DANH_GIA.md).

`evaluate_pilot.py` là script CPU dùng thư viện chuẩn, đọc predictions đã có; không train hoặc gọi model. Được chuẩn bị ngày 19/10; Minhtri đã báo self-test PASS và có output pilot ngày 20/10. Không còn ở trạng thái chỉ kiểm cú pháp. Lượt hỗ trợ Triệu ngày 21/10 chỉ đọc/đối chiếu nguồn và output, không chạy lại evaluator hoặc self-test.

Xem [bản kiểm chéo cho Triệu](../reports/TRIEU_EVALUATOR_CROSSCHECK_20261021.md) và [kết quả ngày 24/10](../reports/TRIEU_KET_QUA_KIEM_CHEO_20261024.md). Triệu đã đọc/hiểu và đồng ý dùng kết quả kiểm kỹ thuật do assistant thực hiện; nhóm vẫn chờ duyệt toàn báo cáo. Không cần chạy lại chỉ vì câu “chưa chạy” trong tài liệu lịch sử.

Kết quả lưu riêng trong `results/countgdpp/pilot_eval_<ngày>`, không ghi đè B0/B2 gốc. `manual_check` chỉ tổng hợp nhãn thủ công q05_2, không phải evaluator định vị tự động toàn tập.
