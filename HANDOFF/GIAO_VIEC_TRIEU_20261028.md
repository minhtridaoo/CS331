# Giao việc cho Triệu — từ 28/10/2026

**Người giao:** Trí (assistant soạn theo yêu cầu của Trí, 27/10 khuya). **Hạn báo cáo môn: 02/12/2026.**
Gói file kèm theo: `HANDOFF/TRIEU_GIAO_VIEC_20261028.zip`. Nếu Trí đã push thì lấy thẳng trong repo, cùng đường dẫn.
Bản này **thay** ZIP V2 cũ (`TRIEU_T1_T4_20261027_v2.zip`, chưa từng gửi).

## 0. Bối cảnh trong 5 dòng

1. Bản tự kiểm Phần 2 ngày 27/10 của Triệu **đạt** phần tự chạy evaluator và q05_2 ([đánh giá](../reports/DANH_GIA_TRIEU_TU_KIEM_20261027.md)).
2. Nhóm đã chạy CountGD++ + 2 bộ lọc trên **10 ảnh MUCCA mới**, xem [tóm tắt dự án](../reports/TOM_TAT_DU_AN_20261027.md). Fusion có MAE tốt nhất, nhưng bỏ khoảng 50% vật đúng, và lỗi X/Y vẫn còn (hỏi "people" thì model khoanh chó).
3. Trí muốn cải tiến tiếp theo một trong hai nhánh ([kế hoạch](../roadmap/KE_HOACH_CAI_TIEN_20261027.md)):
   - **P**: kiểm mẫu tự chọn bằng CLIP trước lượt 2;
   - **R**: bộ lọc giữ được vật đúng.
4. **Chọn P hay R phụ thuộc vào review khung N4, và đó là việc của Triệu tuần này.** N4 nằm trên đường găng: N4 trễ thì cả đồ án trễ.
5. Trí đã chấm u01_1 (9 khung). Phần còn lại giao cho Triệu.

## 1. Việc và hạn

| # | Việc | Ước lượng | Hạn | Ưu tiên |
|---|---|---:|---|---|
| **V1** | **N4 tầng A**, gói chính: 7 query, 78 khung (gồm u01_1 chấm lại độc lập) | 60 phút | **30/10** | Cao nhất |
| **V2** | **N4 tầng A**, phần bổ sung `bo_sung_F0/`: 21 mẫu tự chọn + 18 ứng viên E3 | 30 phút | **30/10** | Cao nhất |
| V3 | q05_3: gán nhãn 79 khung B2 + 21 khung B0 + 3 mẫu; bảng phân rã (đúng / trùng / một phần / sai loại / bỏ sót) | 90 phút | 01/11 | Cao |
| V4 | Thêm 2 ca thử evaluator: GT `uncertain`; query `absent` mà model đếm > 0 | 15 phút | 01/11 | Vừa |
| V5 | Phân tích B2 so với B0: bảng chênh lệch từng query (pilot), liên hệ với mẫu tự chọn (dùng V2 + V3), thêm kết quả tập mới; 2–3 đề xuất cải thiện | 45 phút | 01/11 | Cao |
| V6 | N4 tầng B: 2 query, 41 khung + 6 mẫu + 11 E3 | 40 phút | 02/11 | Vừa |
| V7 | Duyệt chung PILOT_SUMMARY §7 với Trí | 20 phút | 03/11 | Cao |
| — | 47 nhãn q03 (dev cũ) | — | **Tạm hoãn** | Đề xuất bỏ: N4 trên tập mới đã thay vai trò này; Trí quyết |

**Tổng tuần này khoảng 5 giờ.** Nếu thiếu thời gian, làm theo thứ tự V1 → V2 → V3 → V5 → V4 → V6.

### Việc của Trí mà Triệu có thể làm thay (tuần sau, Trí đồng ý mới làm)

| # | Việc | Ước lượng | Khi nào |
|---|---|---:|---|
| V8 | Kiểm absent/GT cho **tập test mới 40 ảnh** (Trí kiểm tập dev 20 ảnh). Người kiểm test nên khác người chỉnh phương pháp | khoảng 2 giờ | 03–08/11, sau khi Trí chốt quy tắc dữ liệu |
| V9 | Viết phần Related Work (CountGD++, PseCo, DAVE, PrACo++/MUCCA) cho báo cáo; nguồn có sẵn ở §9 của `hướng cái tiển/CS331_KE_HOACH_FIX_PIPELINE_DE_PUBLISH_20261027.md` | khoảng 2 giờ | 09–22/11 |
| V10 | Review khung nhỏ trên tập test cuối (như N4) | khoảng 1 giờ | 23–26/11 |

## 2. Cách làm N4 (V1, V2, V6)

Quy ước đầy đủ ở [§4 HUONG_DAN](../experiments/countgdpp/p4_unseen_v1/HUONG_DAN_KIEM_DU_LIEU.md). Tóm tắt:

1. Mở `results/countgdpp/p4_n4_review_package_20261027/README.md`.
2. Với từng query, xem `*_crops.jpg` (ảnh cắt từng khung, đánh số `#rank`) và `*_overview.jpg` (vị trí của khung trong ảnh), rồi điền file `*_labels_BLANK.csv`.
   - Riêng u01_1: điền `A_u01_1_people_labels_TRIEU_BLANK.csv`, **không mở** bản của Trí (`..._TRI_20261027.csv`).
3. Mỗi dòng (một khung) điền:
   - `label_type`: một trong `target` (đúng loại, cả vật) / `duplicate` (trùng vật đã có) / `part` (một phần vật) / `multi_object` (bao nhiều vật) / `wrong_class` / `background` / `uncertain`;
   - `actual_class`: vật thật trong khung, ví dụ `dog`, `motorbike`;
   - `object_id`: cùng một vật thì cùng id;
   - `note` khi chưa chắc;
   - `reviewer` = Triệu, `date`.
4. **Review mù:** không mở thư mục `_KEY_mo_sau_khi_review/` (thư mục này không có trong ZIP).
5. Làm gói chính xong thì làm `bo_sung_F0/` (README riêng):
   - với mẫu P1–P3: đúng loại không, có đúng **một** vật không;
   - với khung E3: có thật là vật đúng bị lọc mất không.
6. Câu hỏi chính mà N4 trả lời: **lỗi đến từ mẫu tự chọn sai (E1) hay từ bộ lọc xóa vật đúng (E3)?** Không cần kết luận; chỉ cần nhãn đúng và trung thực, ghi `uncertain` khi phân vân.

## 3. Cách làm q05_3 (V3)

Gói `results/countgdpp/q05_error_analysis_package_20261027/`: ảnh đánh số + CSV trắng cho B2 final (79 khung), B0 (21 khung), mẫu (3 khung); chi tiết trong README.json. Dùng cùng bộ `label_type` như N4. Cuối cùng viết bảng:

```
B0 21 = ? target + ? duplicate + ? part + ? wrong_class + ? background
B2 79 = ...
Quả blackberry nào (trong 3 quả GT) không có khung target nào?
```

## 4. Trả kết quả

- Điền thẳng vào CSV ở đúng đường dẫn trong repo, giữ tên file. Commit với message `Triệu: N4 tầng A ...`, rồi push.
- Phần V3–V5: thêm một mục vào `reports/TRIEU_TU_KIEM_PHAN2_20261027.md` (bảng q05_3, 2 ca thử, phân tích B2/B0), kèm 1 mục trong `WORKLOG.md`.
- Báo Trí khi xong V1 + V2. Assistant sẽ ghép với bảng tra, tính E1–E4 bằng nhãn người và đề xuất P hay R.

**Nếu đến 31/10 V1 + V2 chưa xong:** nhóm chọn nhánh bằng chỉ báo tự động đã có (E1 và E3 đều lớn), ghi rõ là chưa có xác nhận của người. Đường găng không chờ thêm.
