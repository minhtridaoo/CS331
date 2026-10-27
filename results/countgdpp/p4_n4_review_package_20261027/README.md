# N4 — review khung chọn lọc (tập p4_unseen_v1)

**Quy tắc chọn ca (chốt 27/10, trước khi xem từng khung):** phân tích lỗi có chủ đích, KHÔNG phải mẫu ngẫu nhiên. Kết quả chỉ dùng để giải thích lỗi, không thay số đếm chính.
- Tầng A (bắt buộc): u01_1, u02_1, u07_1, u08_1, u01_3, u07_3, u10_3. Gồm 4 query "people" nhiều khung rơi vào vật loại khác, cộng 3 query vắng mặt bị báo > 0.
- Tầng B (nếu còn giờ): u06_2, u07_2. Fusion giữ nhiều khung hơn lọc điểm.

Tổng 119 khung = hợp các khung được ít nhất một bộ lọc giữ.

**Review mù:** khung chỉ đánh số theo rank của B2, cùng một màu. Đừng mở `_KEY_mo_sau_khi_review/` trước khi điền xong; bảng đó cho biết cách nào giữ khung nào.

**Cách điền** (quy ước §4 trong HUONG_DAN_KIEM_DU_LIEU.md): mở `*_crops.jpg` (ảnh cắt từng khung) và `*_overview.jpg` (vị trí trong ảnh), rồi điền `*_labels_BLANK.csv`, mỗi dòng một khung:
- `label_type` chọn một trong: target | duplicate | part | multi_object | wrong_class | background | uncertain
- `actual_class`: vật thật trong khung (ví dụ dogs, motorbikes)
- `object_id`: cùng một vật thì cùng id; khung trùng đánh `duplicate`
- `note`: ghi khi chưa chắc
- `reviewer` / `date`: người điền, ngày điền

Với query vắng mặt, khung nào cũng là sai; chỉ cần ghi khung đó thật ra là vật gì. Điền xong thì báo assistant để ghép với bảng tra và tính kết quả.

**Cập nhật 27/10 khuya:** u01_1 đã được Trí chấm (9/9) → `A_u01_1_people_labels_TRI_20261027.csv`. Người thứ hai chấm độc lập vào `A_u01_1_people_labels_TRIEU_BLANK.csv`, **không mở** bản của Trí. 8 query còn lại vẫn dùng `*_labels_BLANK.csv`.
