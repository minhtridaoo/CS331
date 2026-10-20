# Kết quả evaluator pilot

Đây là số liệu được tính lại từ predictions lưu sẵn.

| Cấu hình | Số query ghép chung | MAE | RMSE | Đúng count |
|---|---:|---:|---:|---:|
| B0 | 15 | 19.4 | 24.315975544210986 | 1 |
| B2 | 15 | 22.0 | 30.090973175799196 | 1 |

Xem metrics.json để biết coverage/errors/uncertain. Không có query absent thì metric absent=null.
manual_check.json chỉ tổng hợp nhãn thủ công q05_2; chưa là metric định vị tự động.
Chuyển sang roadmap/PHAN_3_TONG_KET.md sau khi đối chiếu kết quả.
