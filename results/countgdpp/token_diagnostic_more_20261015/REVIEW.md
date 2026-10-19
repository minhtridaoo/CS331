# Hoàn tất chẩn đoán token — 15/10/2026

Đã kiểm lại tensors raw của 5 query trên 2 ảnh (rulers ở run trước, 4 query ở run này), không chỉ đọc số count trên terminal. Run mới complete, tất cả replay_matches=True: số lượng, tọa độ và scores khớp baseline theo sai số cho phép của script.

| Query | Count gốc | Chỉ lấy điểm token tên vật | Khung thay đổi? |
|---|---:|---:|---|
| rulers | 18 | 18 | Không |
| pens | 17 | 17 | Không |
| pencils | 17 | 17 | Không |
| guitars | 25 | 25 | Không |
| amplifiers | 44 | 44 | Không |

121 proposal được giữ qua 5 query đều giữ nguyên khi bỏ token đặc biệt/dấu chấm khỏi phép max positive. Ở pencils, tên từ được tách pencil + ##s; cả 17 khung có top token pencil. Các query còn lại có top token chính tên vật. Không có bằng chứng các khung sai trong 5 query này được giữ chỉ vì CLS/dấu chấm.

Đây là phép thay cách tổng hợp điểm trên cùng đầu ra, không phải thử caption không có dấu chấm. Chưa khẳng định mọi dạng xử lý prompt đều không có tác dụng hoặc đã biết nguyên nhân bên trong model. Đúng số guitar cũng chưa phải xác nhận định vị tuyệt đối đúng.

Cảnh báo deprecated autocast không làm dừng run; không cần sửa môi trường chỉ vì dòng cảnh báo này. Giữ nguyên baseline và các kết quả gốc.

## Bước tiếp theo đã chốt

Chuẩn bị đối chứng B0/B2 trên cùng hai ảnh mcac_200 và mcac_100, giữ cả ba query mỗi ảnh. B0 dùng văn bản một lượt. B2 theo pipeline nhóm: lượt đầu tự chọn vùng mẫu từ chính ảnh rồi chạy lượt hai. Mục tiêu là kiểm tra bước này giảm hay khuếch đại lỗi chọn loại, chưa gọi B2 là cải tiến mới hoặc toàn cấu hình paper.

Trước khi chạy B2 phải đối chiếu implementation chọn pseudo-exemplar (số mẫu, ngưỡng, xử lý không có mẫu), cố định chính sách trước khi xem kết quả; lưu khung/mẫu/lượt đầu/lượt hai. Không chọn khung đúng bằng GT, không negative prompt lấy từ nhãn, không synthetic/crop trong đối chứng này. Giữ B0 cố định để so sánh. Có thể khảo sát ngưỡng như đối chứng tiếp theo nhưng không chọn từ holdout hoặc chỉ một ảnh thuận lợi.

Chưa triển khai hoặc chạy B2 trong lần cập nhật này. Chưa cần train hoặc viết module mới. Triệu kiểm nhãn/khung và evaluator, bổ sung absent, chuẩn bị holdout độc lập. Không tiếp tục chỉnh riêng token dấu chấm như một giải pháp đã được bằng chứng hỗ trợ.

[Chi tiết kiểm tensor và giới hạn](combined_review.json) · [Chẩn đoán rulers trước đó](../token_diagnostic_rulers_20261015/REVIEW.md)
