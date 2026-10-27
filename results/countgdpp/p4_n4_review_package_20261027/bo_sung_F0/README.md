# Bổ sung F0 cho N4 — đo E1 (mẫu tự chọn sai) và E3 (Fusion xóa vật đúng)

Theo §2 của `hướng cái tiển/CS331_KE_HOACH_FIX_PIPELINE_DE_PUBLISH_20261027.md`. Dùng cùng 9 query với gói N4. Phần này **không mù**: tên file đã cho biết loại khung.

- `*_pseudo_*`: 27 khung mẫu tự chọn (P1–P3) mà B2 đưa vào lượt 2. Với mỗi mẫu, trả lời: đúng loại không? Có đúng **một** vật không? (`label_type`: target / wrong_class / multi_object / part / background / uncertain)
- `*_e3_*`: 29 khung B2 bị **cả hai** bộ lọc loại nhưng có chứa điểm MUCCA của loại cần đếm. Câu hỏi: đây có thật là vật đúng bị xóa nhầm (E3) không, hay là khung trùng / khung lớn bao nhiều vật / một phần vật?
- `*_supplement_overview.jpg`: khung xanh lá là mẫu tự chọn, khung xanh dương là ứng viên E3.

Điền CSV giống gói chính. Thứ tự làm: gói chính trước (review mù), phần bổ sung sau.
