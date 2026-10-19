# Kiểm tra ảnh đầu M4 — 14/10/2026

Run m4_first_image_b0 hoàn tất 3/3, không có lỗi thực thi. Đã ghép IDs với manifest và kiểm count/boxes/scores, xem cả ba overlay.

| Query | GT theo gói Triệu | Dự đoán | Sai số tuyệt đối |
|---|---:|---:|---:|
| guitars | 25 | 25 | 0 |
| amplifiers | 11 | 44 | 33 |
| chairs | 1 | 0 | 1 |

Guitars đúng số đếm, khung nhìn chủ yếu vào đàn; chưa chấm vị trí chính thức. Amplifiers khoanh nhiều guitar và vùng khác bên cạnh ampli; không được hiểu 44 là 44 ampli đúng. Chairs không có khung, bỏ sót ghế/stool phía dưới trái theo nhãn nguồn.

Đây là bằng chứng ban đầu cho lỗi chọn sai loại khi đổi câu hỏi, không chứng minh mô hình hoàn toàn bỏ qua prompt hay xác định nguyên nhân. Giữ ngưỡng 0.23, chưa train/chỉnh lọc; chạy 5 ảnh đầu để xem lỗi có lặp lại. Bộ 5 ảnh bao gồm ảnh đầu, không tính lần chạy lại là một ảnh độc lập. Chưa có query vắng mặt.

Đã ghép ba kết quả bằng kiểm tra độc lập, chưa xác nhận Triệu đã triển khai evaluator hoặc đóng G1. Có thể chạy thu thập pilot song song; chỉ kết luận chỉ số khi evaluator được kiểm. Thời gian trong run_config là toàn tiến trình; peak VRAM chưa đo.
