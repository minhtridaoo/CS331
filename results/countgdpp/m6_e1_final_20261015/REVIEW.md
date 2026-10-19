# M6/E1 — khảo sát ngưỡng lọc cuối

**Ngày 15/10/2026. CPU hậu xử lý, không forward model hoặc train.**

Cùng hai ảnh/sáu query; giữ tau_sample=0.23, mẫu B2 cố định, max3. Lưới đã có trong protocol trước khi xem kết quả: 0.10, 0.23, 0.35, 0.50. Áp dụng cùng lưới cho B0 và B2. Đã tái lập chính xác count/boxes/scores tại 0.23 và kiểm tập khung chỉ giảm khi tăng ngưỡng. Có 48 tổ hợp query/cấu hình.

| Cách chạy | Ngưỡng cuối | MAE có mặt | Đúng count | Trả 0 |
|---|---:|---:|---:|---:|
| B0 | 0.1 | 16.833 | 0/6 | 1/6 |
| B0 | 0.23 | 11.333 | 1/6 | 1/6 |
| B0 | 0.35 | 7.833 | 1/6 | 1/6 |
| B0 | 0.5 | 5.000 | 1/6 | 4/6 |
| B2 | 0.1 | 14.167 | 0/6 | 1/6 |
| B2 | 0.23 | 9.500 | 1/6 | 1/6 |
| B2 | 0.35 | 8.000 | 1/6 | 1/6 |
| B2 | 0.5 | 6.000 | 1/6 | 1/6 |

## Kết quả từng query

| Query (GT) | B0 tại .10/.23/.35/.50 | B2 tại .10/.23/.35/.50 |
|---|---|---|
| guitars (25) | 32 / 25 / 25 / 25 | 30 / 25 / 25 / 25 |
| amplifiers (11) | 67 / 44 / 29 / 0 | 50 / 38 / 32 / 28 |
| chairs (1) | 0 / 0 / 0 / 0 | 0 / 0 / 0 / 0 |
| pens (6) | 18 / 17 / 12 / 12 | 20 / 13 / 12 / 12 |
| rulers (6) | 18 / 18 / 18 / 0 | 18 / 18 / 18 / 12 |
| pencils (6) | 19 / 17 / 16 / 0 | 20 / 16 / 14 / 12 |

## Quan sát và giới hạn

- B0 .50 có MAE thấp nhất trong lưới này, nhưng bỏ hết ampli/thước/bút chì; ghế vẫn 0. Presence recall chỉ còn 2/6, so với 5/6 tại .23. Không coi count-error thấp là giải quyết đúng loại.
- Pens: cả B0/B2 tại .35/.50 giữ 12 khung gồm bút mực và bút chì; vẫn không tách đúng loại. Đã xem ảnh.
- Rulers: B0 .35 vẫn18, .50 về0; B2 .50 còn12 gồm thước và bút mực. Đã xem ảnh. Ngưỡng cao không tự đảm bảo lọc đúng lớp.
- Ampli: B0 .50 về0; B2 .50 còn28, vẫn khoanh nhiều guitar. Đã xem ảnh.
- Chỉ guitar đúng count ở mọi ngưỡng >=.23 trong lưới này. Cả B0/B2 không tăng số query đúng count khỏi1/6. Chưa chấm định vị chính thức.
- Chairs không có mẫu ở tau_sample .23; B2 ở mọi tau_final dùng refiltered stage1, không có forward2. Không tự chọn thêm mẫu khi giảm tau_final.
- Đây là dev nhỏ, không phải holdout hoặc benchmark đầy đủ; không chứng minh mọi ngưỡng đều thất bại, không chọn một ngưỡng riêng cho từng query dựa GT. Không có absent nên FPR_absent=null.

## Bước tiếp theo

E1 đã xong trên hai ảnh. M6 chưa hoàn tất E2: giữ tau_final .23, thay tau_sample theo cùng lưới để kiểm chất lượng/khả dụng mẫu; lưu mẫu và chạy lượt hai theo cấu hình mới. Không dùng raw lượt hai cũ như thể mẫu mới đã chạy. Trước khi kết luận đóng góp, cần kiểm nhãn/mẫu, evaluator, thêm absent và dữ liệu dev/holdout độc lập.

Chưa train, chọn module hay đổi baseline mặc định. Giữ .23 làm mốc tham chiếu, các cấu hình sweep lưu riêng.

## Tái chạy nếu cần

Chỉ cần Python với numpy/Pillow, không GPU; dùng run-id mới để tránh ghi đè:

~~~bash
python experiments/countgdpp/sweep_final_threshold.py --run-id m6_e1_final_repeat
~~~

[Bảng chỉ số](summary.csv) · [Bảng từng query](per_query.csv) · [Thước](q03_2_sweep.jpg) · [Bút mực](q03_1_sweep.jpg) · [Ampli](q01_2_sweep.jpg)
