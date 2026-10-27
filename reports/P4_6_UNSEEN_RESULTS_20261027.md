# P4.6c–d — kết quả trên tập kiểm mới p4_unseen_v1 (27/10/2026)

**Tập:** 10 ảnh MUCCA / 30 query (20 có mặt + 10 vắng mặt), **khóa 17:07:55 trước khi chạy**. **Cấu hình:** CountGD++ B2 như pilot; hai bộ lọc dùng freeze 21/10, không chỉnh gì theo tập này. **Người chạy:** assistant, theo yêu cầu của Trí ("chạy đủ cả 3 cách"). Máy: RTX A2000 4 GB, không cần Kaggle.

B0 = lượt 1 của chính run này (chỉ text, chưa có mẫu tự chọn). B0 không phải ứng viên P4, chỉ để tham chiếu.

## 1. Số đếm

| Cách | MAE có mặt (20) | RMSE có mặt | Đúng tuyệt đối | Vắng mặt: count TB | Vắng mặt báo > 0 | MAE cả 30 |
|---|---:|---:|---:|---:|---:|---:|
| B0 (tham chiếu) | **5.70** | **9.44** | **4/20** | 8.9 | 3/10 | 6.77 |
| B2 gốc | 12.95 | 21.14 | 3/20 | 13.1 | 3/10 | 13.00 |
| B2 lọc điểm (freeze) | 8.75 | 10.80 | 0/20 | 4.3 | 3/10 | 7.27 |
| **Fusion 50/50 (freeze)** | 7.80 | 10.12 | 0/20 | **1.0** | 3/10 | **5.53** |

So từng cặp trên cả 30 query. Khoảng tin cậy 95% lấy bằng bootstrap theo ảnh (10 ảnh, 5000 lần, seed 331). Δ = MAE của cách sau trừ cách trước; âm nghĩa là cách sau tốt hơn.

| So sánh | Tốt hơn / kém hơn / bằng | Δ MAE | 95% CI |
|---|---|---:|---|
| B2 gốc so với B0 | 2 / 15 / 13 | +6.23 | [+2.0, +12.3] → **B2 kém B0 rõ ràng** |
| B2 lọc điểm so với B2 gốc | 12 / 10 / 8 | −5.73 | [−15.6, +0.9]: chưa chắc |
| Fusion so với B2 gốc | 12 / 10 / 8 | −7.47 | [−18.2, +0.1]: sát ngưỡng, chưa chắc |
| **Fusion so với B2 lọc điểm** | 13 / 7 / 10 | **−1.73** | **[−3.2, −0.3]** → Fusion tốt hơn |

## 2. Đúng vật — chỉ số tự động từ điểm MUCCA (KHÔNG phải review người theo §4)

Với mỗi khung được giữ, đếm xem có điểm GT nào nằm trong khung không (gộp 20 query có mặt, tổng 289 điểm mục tiêu):

| Cách | Khung giữ | Khung chứa vật đúng | Khung chỉ chứa vật loại khác | …trong đó là đúng loại của query kia (nhầm X↔Y) | Điểm mục tiêu được phủ |
|---|---:|---:|---:|---:|---:|
| B0 | 369 | 258 | 106 | 67 | 269/289 (93%) |
| B2 gốc | 532 | 278 | 238 | 119 | 277/289 (96%) |
| B2 lọc điểm | 204 | 111 | 92 | 63 | 127/289 (44%) |
| Fusion | 157 | 126 | **31** | **16** | 145/289 (50%) |

## 3. Đọc kết quả

1. **Bước mẫu tự chọn (B2) làm hại, đúng như pilot.** B2 gốc kém B0 rõ ràng (CI không chứa 0). Ca nặng: u10_2 motorbikes 17 → B2 đếm 80; u06_1 chairs 23 → 49; u01_1 people 10 → 38.
2. **Cả hai bộ lọc giảm sai số so với B2 gốc**, nhưng với 10 ảnh thì chưa đủ chắc chắn về thống kê.
3. **Fusion tốt hơn lọc điểm CountGD++ trên tập mới** (CI không chứa 0). Kết quả này **ngược với CV trên dev** (4.6 vs 5.8), nên chỉ được coi là kết quả của bộ 10 ảnh này, không khái quát. Lợi thế lớn nhất của Fusion nằm ở query vắng mặt (count TB 1.0 so với 4.3) và ở việc bỏ khung sai loại (31 so với 92).
4. **Đánh đổi:** các bộ lọc bỏ cả khoảng một nửa vật đúng (chỉ phủ 44–50% điểm mục tiêu) và không query nào đếm đúng tuyệt đối. Trên các query có mặt, **B0 vẫn tốt nhất** (MAE 5.70). Fusion thắng ở MAE cả 30 query chủ yếu nhờ phần vắng mặt.
5. **Vấn đề X/Y của thầy vẫn còn:**
   - Hỏi "people" trên ảnh có chó/ghế/xe thì model trả về khung trên vật kia (u01_1, u02_1, u05_1, u07_1, u08_1).
   - Hỏi lớp vắng mặt "gần nghĩa" thì model đếm vật thật đang có: "sheep" trên ảnh chó (u01_3), "bicycles" trên ảnh xe máy (u07_3, u10_3). Ba query này là 3/10 query vắng mặt bị báo > 0 ở **mọi** cách.

   Fusion giảm số khung nhầm nhưng chưa đưa các ca này về 0.
6. 7/10 query vắng mặt (cats, bicycles ở mcac_109, amplifiers, forks, blackberries, boats, trucks) đều trả 0 ngay từ lượt 1 (`no_pseudo`), ở mọi cách. Query có mặt `amplifiers` ở mcac_109 (GT 4) cũng trả 0 ở mọi cách: đây là **bỏ sót**.

## 4. Giới hạn

- 10 ảnh / 30 query, các query trong cùng ảnh không độc lập; CI bootstrap theo ảnh chỉ mang tính tham khảo.
- GT là điểm MUCCA, một người kiểm (Trí). Chỉ số "đúng vật" là đối chiếu tự động điểm-trong-khung: một khung lớn có thể chứa nhiều điểm, và khung trùng không bị tách. **Review khung bằng người theo §4 chưa làm.**
- B0 không thuộc kế hoạch P4. Gợi ý "áp bộ lọc lên B0 thay vì B2" là **giả thuyết cho vòng sau**; không được chỉnh trên tập này rồi báo lại như kết quả độc lập.

## 5. Bằng chứng

Chạy theo thứ tự (log ở `reports/audits/p4_unseen_v1_run_20261027/`):
1. `run_b2_frozen.py --inputs experiments/countgdpp/p4_unseen_v1/inputs.jsonl --run-id p4_unseen_v1_b2_20261027` (WSL Ubuntu-22.04, 30/30 ok)
2. `p4_clip_score.py … --run-id p4_unseen_v1_clip_20261027` (WSL Ubuntu, 663 khung)
3. `p4_apply_freeze.py --scores results/countgdpp/p4_unseen_v1_clip_20261027 --run-id p4_unseen_v1_freeze_20261027`
4. `evaluation/p4_unseen_score.py --run-id p4_unseen_v1_eval_20261027`: `metrics.json`, `per_query.csv`, `run_config.json` (hash của bản đã khóa đều khớp).
