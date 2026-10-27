# Phần 2 — chấm lại pilot và kiểm chéo evaluator

**Cập nhật sau nhận handoff 20/10/2026: ĐÃ CHẠY; output đã được assistant đối chiếu; CHỜ TRIỆU KIỂM CHÉO.** Không cần chạy lại model hoặc evaluator chỉ vì tài liệu cũ còn ghi “chưa chạy”.

[Trang bắt đầu](../README.md) · [Roadmap](ROADMAP.md) · [Báo cáo pilot](../reports/PILOT_SUMMARY.md).

## 1. Những việc đã được xác nhận

- Minhtri báo self-test **PASS** với `python3 evaluation/evaluate_pilot.py --self-test`. Nguồn: handoff ngày 20/10 của người chạy; chưa có file stdout self-test riêng. Không gọi đây là self-test do assistant vừa thực thi.
- Có đủ 5 file trong [pilot_eval_20261020](../results/countgdpp/pilot_eval_20261020): metrics.json, per_query.json, manual_check.json, run_config.json, SUMMARY.md. Đây là run chính để trích báo cáo.
- Có thêm [pilot_eval_20261020_r2](../results/countgdpp/pilot_eval_20261020_r2): đủ 5 file. Bốn file kết quả giống hệt run chính; cùng 7 hash nguồn, command chỉ khác tên output. Đây là lần chấm lại cùng dự đoán, không phải mẫu thí nghiệm độc lập hay lần inference mới.
- Assistant đã đọc code và kiểm cả 15 dòng: ghép ID/GT/prediction, coverage, phép tính MAE/RMSE, exact count, error_change và nhãn q05_2. 7/7 hash trong metadata khớp file hiện tại ở mỗi run.
- Không import/chạy lại evaluator hoặc model trong lượt kiểm này. Audit artifact của assistant không thay tên/ngày xác nhận của Triệu.

## 2. Kết quả đang giữ

| Kiểm tra | Kết quả đã đối chiếu |
|---|---|
| Số query / số ảnh | 15 / 5 |
| B0, B2 hợp lệ | 15 mỗi bên; 0 error; 0 uncertain |
| Paired queries | 15 |
| B0 MAE / RMSE | 19.4 / 24.315975544210986 |
| B2 MAE / RMSE | 22.0 / 30.090973175799196 |
| Exact count | 1/15 mỗi bên |
| B2 cải thiện / kém đi / không đổi | 6 / 4 / 5 |
| Present / absent | 15 / 0; các metric absent là null |
| q05_2 | 14 khung = 5 khung mục tiêu (4 vật + 1 khung dư) + 9 khung sai loại |

[SUMMARY](../results/countgdpp/pilot_eval_20261020/SUMMARY.md) · [metrics](../results/countgdpp/pilot_eval_20261020/metrics.json) · [per_query](../results/countgdpp/pilot_eval_20261020/per_query.json) · [manual_check](../results/countgdpp/pilot_eval_20261020/manual_check.json) · [run_config](../results/countgdpp/pilot_eval_20261020/run_config.json).

## 3. Việc còn lại của Triệu — kiểm chéo một lần có ghi nhận

Mở [evaluate_pilot.py](../evaluation/evaluate_pilot.py). Đọc luồng `indexed` → `validate_prediction` → `evaluate` → `manual_check`. Ghép theo `(image_id, query_id)`, không theo thứ tự dòng; B2 ghép hai run 6+9 query. Chỉ lấy 15 query của [first5_inputs](../experiments/countgdpp/m4_inputs/first5_inputs.jsonl) trong [manifest](../experiments/countgdpp/m4_inputs/manifest.csv), dù manifest có 30 query.

Kiểm vài ca dễ nhìn trong per_query và nguồn predictions; đây là các giá trị để đối chiếu, không phải kết quả model cần chạy lại:

| Query | GT | B0 → B2 | Sai số B0 → B2 | Điểm cần hiểu |
|---|---:|---:|---:|---|
| q01_1 guitars | 25 | 25 → 25 | 0 → 0 | Exact count |
| q01_3 chairs | 1 | 0 → 0 | 1 → 1 | Present nhưng bỏ sót; không phải absent |
| q05_2 raspberries | 4 | 11 → 14 | 7 → 10 | Số liệu count và nhãn khung khác khái niệm |
| q05_3 blackberries | 3 | 21 → 79 | 18 → 76 | Giữ ca lỗi lớn, không loại khỏi bảng |

Các nguồn predictions được liệt kê và hash trong run_config. Với q05_2, đối chiếu [nhãn đã lưu](../results/countgdpp/b2_remaining3_20261015/q05_2/manual_crosscheck_20261016.json), chỉ số khung và object_id với manual_check. Script chỉ đếm lại nhãn người gán; không tự nhận diện lớp hoặc chấm IoU/AP.

- [x] Triệu đã đọc phần ghép ID, công thức MAE/RMSE và cách xử lý error/null/uncertain (27/10; thử thêm 5 ca dữ liệu hỏng).
- [x] Triệu đối chiếu các ca trong bảng với nguồn, kiểm manual q05_2 (27/10; truy ngược q05_3, tự gán nhãn 14 box q05_2 trước khi mở nhãn cũ).
- [x] Triệu hiểu `n_absent=0` → metric absent=null, không phải sai số bằng 0; presence_recall chỉ là trả count dương (27/10).
- [x] Ghi tên, ngày và kết luận trong phiếu xác nhận ở cuối [PILOT_SUMMARY](../reports/PILOT_SUMMARY.md) (27/10). [Báo cáo tự kiểm](../reports/TRIEU_TU_KIEM_PHAN2_20261027.md).

Không cần gán nhãn lại 15 query hoặc viết một evaluator thứ hai để hoàn thành phần này. Review định tính Triệu đã chốt 15/15 trước đó; nhiệm vụ hiện tại là kiểm phép chấm và dữ liệu ghép.

## 4. Lệnh tham khảo khi thật sự cần chạy lại

Lượt vừa rồi chạy bằng **Python 3 hệ thống trong Ubuntu**, không cần PyTorch/GPU hoặc venv model vì evaluator chỉ dùng thư viện chuẩn. Lỗi không tìm thấy `python`/file activate trong distro đó không chứng minh môi trường model ở distro khác đã mất; không cần cài lại CUDA để chấm JSON.

Các lệnh dưới đây để tái kiểm sau khi code/input thay đổi hoặc người kiểm muốn chạy; không phải bước bắt buộc phải lặp ngay:

```bash
cd /mnt/d/MINHTRIHOCCODE/HOCKI5/CS331
python3 evaluation/evaluate_pilot.py --self-test
# Chỉ sau PASS; chọn thư mục mới. Hai run không hậu tố và _r2 đã tồn tại.
python3 evaluation/evaluate_pilot.py --out results/countgdpp/pilot_eval_20261020_r3
```

Mọi lỗi phải được ghi riêng, không chuyển thành count 0. Không sửa GT/predictions để ép số. Source/ID thay đổi hợp lệ phải ghi phiên bản; không yêu cầu số mới khớp số cũ khi dữ liệu đã khác.

## 5. Trạng thái nghiệm thu

- [x] Người chạy báo self-test PASS, nguồn được ghi rõ.
- [x] Output đủ 5 file; số liệu/IDs/hash đã đối chiếu trên file thật.
- [x] ROADMAP/HANDOFF/WORKLOG đã đồng bộ sau lượt kiểm ngày 20/10.
- [x] Triệu tự kiểm chéo evaluator ngày 27/10: self-test PASS, tính lại metric khớp, run `pilot_eval_20261027_trieu` giống hệt run 20/10.

Phần chạy và audit output đã xong; chỉ còn xác nhận nhóm để đóng Phần 2. Tiếp tục [Phần 3](PHAN_3_TONG_KET.md), không chạy lại inference. Assistant chạy self-test/evaluator/thực nghiệm thay vẫn phải hỏi trước theo yêu cầu của bạn ngày 19/10.
