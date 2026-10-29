# Triệu tự kiểm chéo Phần 2 — tiến độ 27/10/2026

**Trạng thái: XONG 8/8 — 27/10/2026.** Còn nhóm (Trí và Triệu) duyệt toàn bộ PILOT_SUMMARY. [Hướng dẫn Phần 2](../roadmap/PHAN_2_DANH_GIA.md) · [Báo cáo pilot](PILOT_SUMMARY.md) · [WORKLOG](../WORKLOG.md).

**Khác bản 24/10:** ngày 24/10 assistant làm hộ phần đối chiếu kỹ thuật, Triệu chỉ đọc và chấp nhận ([bản đó](TRIEU_KET_QUA_KIEM_CHEO_20261024.md)). Lần này **Triệu tự chạy lệnh, tự tính và tự nhìn ảnh**; assistant (Claude) chỉ hướng dẫn từng bước, giải thích code và chấm câu trả lời. Bản 24/10 giữ nguyên làm lịch sử. Chưa sửa PILOT_SUMMARY mục 7; chỉ sửa khi xong cả 8 bước.

Checkout: commit `d6db189`, máy Windows của Triệu, Python conda `ai_new` (3.10). Không chạy model, không sửa code, GT hoặc predictions.

## Bước 1 — self-test evaluator: ĐẠT

```powershell
C:\Users\diosodumb\miniconda3\envs\ai_new\python.exe evaluation\evaluate_pilot.py --self-test
```

Kết quả: `SELF-TEST PASS: fixture, duplicate/missing IDs, count mismatch, error/null coverage`. Lưu tại [TRIEU_SELFTEST_stdout.txt](audits/TRIEU_SELFTEST_stdout.txt). Đây là stdout self-test đầu tiên được lưu trong repo; trước đó chỉ có lời báo PASS trong handoff.

## Bước 2 — đọc code `evaluate_pilot.py`: ĐÃ HIỂU CÁC ĐIỂM CHÍNH

- Ghép theo `(image_id, query_id)`, không theo thứ tự dòng. Triệu đã tự xem: B2 nằm trong 2 file, thứ tự nối là q01, q03 | q02, q04, q05, khác thứ tự manifest q01…q05. Ghép theo dòng sẽ so q03_1 với đáp án q02_1 mà không báo lỗi.
- Lỗi thực thi phải có `final_count=null`, không được ghi 0: ghi 0 sẽ phạt oan câu có vật hoặc khen oan câu vắng mặt.
- `uncertain` bị loại khỏi phép chấm, không gộp vào `absent`. So B0/B2 chỉ trên tập `common` mà cả hai đều chạy được.
- `FPR_absent` = số câu vắng mặt mà model đếm > 0 / tổng số câu vắng mặt; `MeanAbsentCount` = trung bình số đếm trên các câu đó. Pilot không có câu vắng mặt nên cả hai là `null` (chưa đo), không phải 0 (đo được và đúng). Phần này Triệu hiểu sau khi được giải thích lại.
- `presence_recall` chỉ kiểm count > 0, không chứng minh đếm đúng loại.

## Bước 3 — tự tính lại metric bằng Excel: KHỚP

File: [TRIEU_TINH_TAY.xlsx](audits/TRIEU_TINH_TAY.xlsx), 15 dòng GT/B0/B2 lấy từ `results/countgdpp/pilot_eval_20261020/per_query.json`.

| | Triệu tính | Evaluator |
|---|---|---|
| MAE B0 / B2 | 19.4 / 22 | 19.4 / 22.0 |
| RMSE B0 / B2 | 24.31597554 / 30.09097318 | 24.3159755… / 30.0909731… |
| B2 so với B0: tốt hơn / kém hơn / giữ nguyên | 6 / 4 / 5 | 6 / 4 / 5 |

**Phát hiện thêm — kết luận B0/B2 rất nhạy với một câu:** bỏ riêng q05_3 (sai số B2 = 76) thì MAE B0 = 273/14 = 19.5, B2 = 254/14 ≈ 18.14, tức kết luận đảo chiều. Vì vậy chỉ nên ghi "trên pilot 15 câu, MAE B2 cao hơn, chủ yếu do q05_3", không ghi "B2 kém hơn B0" như kết luận chung. Vẫn **giữ** q05_3 trong metric vì đây là lỗi thật của model, không phải lỗi dữ liệu. Đây là thêm một lý do cần mở rộng dev/holdout (T6).

Bước này kiểm phép tính của evaluator; việc số liệu được lấy đúng từ file nguồn được kiểm ở bước 4 (mới làm cho q05_3).

## Bước 4 — truy ngược q05_3 blackberries về file nguồn: KHỚP

| Nguồn | Trường | Giá trị |
|---|---|---|
| `results/countgdpp/m4_first5_b0/predictions.jsonl` | B0 `final_count` / số box | 21 / 21 |
| `results/countgdpp/b2_remaining3_20261015/predictions.jsonl` | B2 `stage1_count` | 21 |
| | `pseudo_boxes` / `stage2_executed` | 3 / True |
| | B2 `final_count` / số box / số score | 79 / 79 / 79 |

- Lượt 1 của B2 bằng B0 (21); số đếm **tăng vọt ở lượt 2**, sau khi có 3 box mẫu.
- `pseudo.jpg` (Triệu tự nhìn): box 1, 2 khoanh trọn quả blackberry; box 3 khoanh nhầm vào raspberry (khoảng nửa quả, bị quả khác che). Mẫu đúng loại 2/3.
- `final.jpg` (Triệu tự nhìn, có trao đổi thêm): **quan sát** model khoanh từng hạt nhỏ trên quả blackberry, nhiều box chồng nhau, cùng các box nhầm sang raspberry (một quả có khoảng 4 box), blueberry và cherry. 79 box = đếm từng phần quả + nhầm loại.
- **Giả thuyết, chưa chứng minh:** box mẫu raspberry góp phần gây khoanh nhầm loại ở lượt 2. Chỉ một ảnh nên chưa kết luận nhân quả.

## Bước 5 — tự gán nhãn 14 box q05_2 raspberries, rồi mới so với nhãn cũ: KHỚP

Triệu gán nhãn từ `results/countgdpp/b2_remaining3_20261015/q05_2/final.jpg` **trước khi mở** `manual_crosscheck_20261016.json`. Bảng nằm ở sheet `q05_2` của [TRIEU_TINH_TAY.xlsx](audits/TRIEU_TINH_TAY.xlsx).

Quy tắc Triệu tự chốt trước khi chấm: *tron = bao gần hết phần nhìn thấy của quả, hụt < ~1/4; chỉ xét phần không bị che. Box lấn sang quả bên cạnh không tính là lỗi. Box nhắm tới quả có phần lớn nhất trong box. Box chứa ~2 quả nguyên → gop_2_qua. Ước lượng bằng mắt, không phải IoU.*

| | Triệu | Nhãn cũ / `manual_check.json` |
|---|---|---|
| Box đúng loại raspberry | 5 (box 1, 2, 3, 7, 11) | 5 |
| Quả raspberry khác nhau | 4 | 4 |
| Box trùng | 1 (box 7 và 11 cùng quả) | 1 (`duplicate_of_overlay` 11 → 7) |
| Box sai loại | 9 | 9 |

- Loại quả khớp **14/14**; cách nhóm 4 quả khớp (tên đặt khác nhau, ví dụ `trai_sau_ben_trai` ↔ `raspberry_left_back`).
- Box 11 "một phần" khớp với `partial` trong nhãn cũ.
- **Lệch duy nhất:** box 12, 13 (blueberry, sai loại). Nhãn cũ ghi `partial`; Triệu ghi `tron` vì quả bị quả khác che phần lớn và box bao đủ phần nhìn thấy. Đây có thể là khác định nghĩa (xét cả quả hay chỉ phần nhìn thấy), không đổi 4 con số. Các box nhãn cũ ghi `not_formally_rated` thì nhãn `tron` của Triệu là thông tin bổ sung, không mâu thuẫn.

## Bước 6 — thử đưa dữ liệu hỏng vào evaluator: ĐẠT

Tạo 5 bản sao hỏng của `results/countgdpp/m4_first5_b0/predictions.jsonl` trong thư mục nháp ngoài repo (`C:\Users\diosodumb\documents\CS331_nhap`); file gốc không bị sửa. Chạy `evaluate_pilot.py --b0 <bản sao>`. Triệu đoán trước kết quả, đúng 2/5.

| Ca | Làm hỏng | Triệu đoán | Evaluator |
|---|---|---|---|
| 1 | Nhân đôi dòng q01_1 | chạy | **Dừng:** `B0: ID trùng ('mcac_100', 'q01_1')` |
| 2 | Xóa dòng q05_3 | báo lỗi | **Dừng:** `B0: ID thiếu/thừa: thiếu=[('mcac_27', 'q05_3')]` |
| 3 | `final_count` 25 → 26, vẫn 25 box | chạy | **Dừng:** `count khác số boxes/scores` |
| 4 | `error` nhưng vẫn count 25 | báo lỗi | **Dừng:** `error phải có final_count=null` |
| 5 | `error` + `final_count=null` | báo lỗi | **Chạy:** B0 valid 14, errors 1; B2 valid 15; paired n_queries 14 |

Rút ra: dữ liệu sai định dạng thì dừng; lỗi chạy được ghi đúng quy ước thì cho qua nhưng báo coverage, và loại câu đó khỏi phép so sánh của cả B0 lẫn B2. Đây là kiểm bằng dữ liệu giả; pilot thật không có error/uncertain/absent.

## Bước 7 — tự chạy evaluator trên dữ liệu thật: GIỐNG HỆT RUN CHÍNH

```powershell
C:\Users\diosodumb\miniconda3\envs\ai_new\python.exe evaluation\evaluate_pilot.py --out results\countgdpp\pilot_eval_20261027_trieu
```

Output: [pilot_eval_20261027_trieu](../results/countgdpp/pilot_eval_20261027_trieu). So với [pilot_eval_20261020](../results/countgdpp/pilot_eval_20261020) sau khi chuẩn hóa xuống dòng CRLF→LF: `metrics.json`, `per_query.json`, `manual_check.json` **giống hệt** (cả ba `True`). Không so `run_config.json` vì hash nguồn trên Windows có thể khác do kiểu xuống dòng, như bản audit 24/10 đã giải thích. Đây là lần chấm lại cùng dự đoán, không phải mẫu thí nghiệm mới.

## Bước 8 — kết luận của Triệu

Nguyên văn trong chat ngày 27/10 (chỉ thêm dấu câu; "[13]" là bản sửa lỗi gõ "12 với 12"):

> Đã check lại metric, q05_3 và tự gán nhãn lại q05_2, check thử đưa dữ liệu hỏng vào thì xảy ra chuyện gì đối với evaluator.
>
> Ở q05_2 thì box 12 với [13] chấm khác với nhãn cũ, cũng tùy vào người chấm cũng như máy chấm thì khác nữa, quan điểm mỗi người thôi, theo tôi thì 2 box đó đã làm tốt việc của mình.
>
> Nên ghi rõ ở q05_3, thực chất B2 kém hơn B0 thì cũng tùy trường hợp nữa chứ không thể ghi tổng quát như vậy được, các số liệu đó ghi vào báo cáo được đó.

Đã ghi vào [PILOT_SUMMARY](PILOT_SUMMARY.md) mục 7, thêm lưu ý độ nhạy q05_3 vào mục 3, đánh dấu checklist [PHAN_2](../roadmap/PHAN_2_DANH_GIA.md) và đồng bộ ROADMAP/HANDOFF_TRIEU.

## V3 (29/10) — gán nhãn từng khung q05_3 blackberries (GT 3): XONG 103/103

**Giao việc:** [GIAO_VIEC_TRIEU_20261028](../HANDOFF/GIAO_VIEC_TRIEU_20261028.md) §3. **Gói:** [q05_error_analysis_package_20261027](../results/countgdpp/q05_error_analysis_package_20261027), khung vẽ lại từ dự đoán đã lưu (B0 `m4_first5_b0`, B2 `b2_remaining3_20261015`), không chạy model.

**Cách làm:** Triệu tự gán nhãn cả 103 khung (3 mẫu pseudo + 21 B0 + 79 B2 final), từng khung một, bằng app [box_label_app.py](../evaluation/box_label_app.py). App chỉ hiện crop, ảnh toàn cảnh, tọa độ và các khung chồng lên, rồi ghi đúng các cột nhãn vào CSV; app không gợi ý nhãn. Assistant hướng dẫn quy ước, kiểm tính nhất quán và tính bảng; Triệu sửa 1 nhãn (B2 rank 2: `wrong_class` → `part`, khớp note) và 2 lỗi gõ trong note sau khi kiểm.

**Quy ước:** `object_id` b1 = quả trên cùng bên phải có cuống, b2 = quả trên cùng ở giữa, b3 = quả dưới bên phải sau dâu tây/cherry. `target` = khung rank nhỏ nhất ôm trọn quả; `duplicate` = khung sau ôm trọn cùng quả; `part` = một phần/hạt của blackberry. Trùng hoặc một phần của quả khác loại vẫn ghi `wrong_class` (ghi trong note). Xét trùng trong từng lần đếm, không chéo B0/B2.

**Mẫu pseudo (3):** P1 = b1 `target`, P2 = b2 `target`, P3 = `wrong_class` raspberries (quả sau, bị một quả raspberry khác che nửa). Cả 3 mẫu là khung cả quả; 2/3 đúng loại.

```
B0 21 = 3 target + 0 duplicate + 0 part  + 18 wrong_class + 0 background
        wrong_class: 11 blueberries, 4 raspberries, 2 cherries, 1 strawberries
B2 79 = 2 target + 0 duplicate + 58 part + 19 wrong_class + 0 background
        wrong_class: 11 blueberries, 7 raspberries (gồm 2 khung một phần quả, 1 khung trùng), 1 cherries
        part theo quả: b1 23, b2 21, b3 14
```

**Quả blackberry nào không có khung target?** B0: không có (b2 rank 2, b3 rank 11, b1 rank 16). **B2: quả b1**, chỉ có 23 khung `part`; kiểm tọa độ: B2 không có khung lớn nào ở vị trí b1, dù b1 chính là mẫu pseudo P1.

**Nhận xét sự kiện (chưa phải phân tích V5):** B0 đếm 21 vì nhận nhầm quả mọng khác loại (18/21). B2 vẫn nhầm loại (19) và thêm 58 khung khoanh từng hạt, đồng thời mất khung cả quả của b1. B2 có một mẫu pseudo là raspberry, và số khung raspberry sai loại tăng 4 → 7; chưa đủ để nói mẫu sai là nguyên nhân. Chỉ một ảnh/một query, không suy rộng.

## V5 (29–30/10) — phân tích B2 so với B0: XONG

**Giao việc:** [GIAO_VIEC_TRIEU_20261028](../HANDOFF/GIAO_VIEC_TRIEU_20261028.md) §1. **Cách làm:** Triệu tự tính bằng Excel trên file kết quả đã lưu ([TRIEU_TINH_TAY.xlsx](audits/TRIEU_TINH_TAY.xlsx), sheet `TRIEU_TINH_TAY` cho pilot, sheet `tap_moi` cho tập mới), rồi đối chiếu với nhãn V2 + V3 của chính mình. Không chạy model hay evaluator. Assistant đưa công thức, kiểm số và góp ý câu chữ; các đoạn trích dưới đây là lời của Triệu, giữ nguyên văn. `delta = |B2−GT| − |B0−GT|`, dương là B2 kém hơn.

### Bước 1 — tập pilot (15 query)

| | B0 | B2 |
|---|---:|---:|
| MAE | 19.4 | 22.0 |
| RMSE | 24.3 | 30.1 |
| MAE bỏ q05_3 | 19.5 | **18.14** |

B2 so với B0: 6 improved / 4 worsened / 5 unchanged (khớp evaluator). Tệ nhất q05_3 +58, tốt nhất q04_2 −11. Ba query worsened còn lại cộng chung chỉ +9.

> B2 không phải khi nào cũng kém hơn, MAE cao hơn hay thấp hơn còn tuy thuộc vào query, giả sử xét q05_3: sai số tăng từ 18 lên 76, gần như áp đảo khi so với các query khác; khi thử bỏ q05_3 đi thì MAE giảm liền và khi này MAE_B2 thấp hơn nữa

### Bước 2 — tập mới p4_unseen_v1 (30 query, khóa trước khi chạy)

Nguồn: `results/countgdpp/p4_unseen_v1_eval_20261027/per_query.csv`, cột `pred_B2_original`. Số tự tính khớp [P4_6_UNSEEN_RESULTS](P4_6_UNSEEN_RESULTS_20261027.md).

| | B0 | B2 gốc |
|---|---:|---:|
| MAE cả 30 | 6.77 | 13.00 |
| MAE có mặt (20) | 5.70 | 12.95 |
| MAE bỏ u10_2 (29) | 6.45 | 11.28 |
| Query vắng mặt bị báo > 0 | 3/10 | 3/10 |

- B2 so với B0: **2 improved / 15 worsened / 13 unchanged**. Hai query improved (u01_2, u02_2) mỗi query chỉ giảm sai số 1. CI 95% của ΔMAE [+2.0, +12.3] (báo cáo P4.6).
- Kém nhất: u10_2 motorbikes +47, u10_3 bicycles +27, u01_1 people +24.
- Vắng mặt bị báo > 0: u01_3 sheep (B0 20 → B2 32), u07_3 bicycles (21 → 24), u10_3 bicycles (48 → 75). B2 đếm nhiều hơn B0 ở cả 3. Bảy query vắng mặt còn lại B0 = B2 = 0.

> ở tập cũ thì B2 gốc tốt hơn 6 và kém hơn 4, khá là cân bằng, MAE_B2 cao hơn MAE_B0 do có 1 trường hợp là B2 tăng đột biến, nếu bỏ trường hợp đó thì MAE_B2 thấp hơn MAE_B0 nên tôi mới kết luận là "tùy trường hợp). ở tập mới thì kết quả khác hẳn, chỉ có 2 trường hợp là B2 tốt hơn(và chỉ tốt hơn có 1) so với 15 trường hợp B2 tệ hơn, và tệ hơn rất nhiều luôn. Nếu so delta cao nhất của tập cũ và tập mới thì tập cũ vẫn cao hơn(58>47) nhưng mặt bằng chung ở tập mới delta cao đều chứ không phải do 1 câu ngoại lệ, bỏ u10_2 thì MAE vẫn 11.28 so với 6.45. kết luận là tập kiểm độc lập thì B2 kém hơn B0  ở phần lớn query, cũng có trường hợp B2 sẽ tốt hơn nhưng ít, kết luận cũ là nhiều khả năng là do tập nhỏ và chỉ có 1 ca ngoại lệ chi phối

Ghi chú: MAE giữa hai tập không so trực tiếp được (độ khó, số vật khác nhau); chỉ so B2 với B0 trong cùng một tập.

### Bước 3 — liên hệ với mẫu tự chọn (nhãn V2 + V3)

Nhãn mẫu V2 (`results/countgdpp/p4_n4_review_package_20261027/bo_sung_F0/A_*_pseudo_labels_BLANK.csv`), delta lấy từ sheet `tap_moi`:

| query | prompt | presence | target | wrong_class | multi_object | mẫu thực ra là | delta |
|---|---|---|---:|---:|---:|---|---:|
| u01_1 | people | có mặt | 1 | 0 | 2 | dogs ×2 | +24 |
| u01_3 | sheep | vắng mặt | 0 | 2 | 1 | dogs ×3 | +12 |
| u02_1 | people | có mặt | 0 | 1 | 2 | dogs ×3 | +5 |
| u07_1 | people | có mặt | 0 | 1 | 2 | cars ×3 | +14 |
| u07_3 | bicycles | vắng mặt | 0 | 2 | 1 | motorcycles ×2, cars ×1 | +3 |
| u08_1 | people | có mặt | 0 | 3 | 0 | cars ×3 | +4 |
| u10_3 | bicycles | vắng mặt | 0 | 1 | 2 | motorcycles ×2, cars ×1 | +27 |
| **Tổng** | | | **1/21** | **10/21** | **10/21** | | **7/7 worsened** |

q05_3 (pilot, [mục V3](#v3-2910--gán-nhãn-từng-khung-q05_3-blackberries-gt-3-xong-103103)): 2/3 mẫu đúng loại; B0 21 khung (0 `part`) → B2 79 khung (58 `part`).

> Lỗi kiểu 1 (E1, mẫu sai loại),7 query được review: chỉ 1/21 mẫu đúng loại (≈4.8%), 10/21 mẫu bao nhiều vật; cả 7 query đều worsened, mẫu sai là vật có hình dáng tương đối giống nhau(sheep ~dogs cùng màu; bicycles~motorcycles) hoặc do đứng liền kề nhau(people đứng trong bầy chó; người đi xe máy có thể ngay cạnh ô tô) hoặc có khả năng do trong ô tô có người, các query này được chọn để soi lỗi, chưa xem mẫu của query improved. Lỗi kiểu 2 (chia nhỏ vật), có lẽ 1 kiểu lỗi là model vô tình hiểu nhầm 1 hạt trong blackberries cũng được tính là 1 object=blackberries, 2/3 mẫu đúng loại, vậy mà B2 tăng từ 21 lên 79 khung; 58 khung tăng thêm đúng bằng 58 khung part. Kết luận,B2 kém không chỉ vì một nguyên nhân, mà theo 2 cơ chế: (1) mẫu sai loại thì lần 2 tìm thêm vật sai loại; (2) mẫu đúng loại nhưng model chia một vật thành nhiều mảnh

### Bước 4 — đề xuất cải thiện

Đề xuất đầy đủ nằm ở [TRIEU_DE_XUAT_NHANH_P_20261029.md](TRIEU_DE_XUAT_NHANH_P_20261029.md) (đã gửi Trí, bàn ở buổi 03/11). Tóm tắt: chọn nhánh P của Trí (kiểm loại mẫu bằng CLIP, không đạt thì quay về B0) cho cơ chế 1; bổ sung bước chống chia mảnh sau lượt 2 cho cơ chế 2; bước kiểm "một vật" chưa có bằng chứng riêng, để ablation trả lời. Giới hạn: quay về B0 không sửa lỗi sẵn có của B0 ở 3 query vắng mặt. Chưa chạy thí nghiệm nào mới.
