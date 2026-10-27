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
