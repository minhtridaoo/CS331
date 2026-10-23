# Kết quả kiểm chéo làm hộ Triệu — 24/10/2026

**Phần đối chiếu kỹ thuật: đã hoàn thành bởi assistant theo yêu cầu Triệu.** Triệu đang ưu tiên deadline đọc/phân tích paper. Đây là kết quả kiểm được ủy quyền, không phải xác nhận Triệu đã tự đọc code hoặc quyết định duyệt của nhóm. Bạn có thể tiếp tục deadline paper; báo cáo này lưu phần kỹ thuật để quay lại đọc nhanh.

Nguồn kiểm: checkout local `minhtridaoo/CS331`, commit `31278dd70377578accda4d126a95b14d33bcdef0` và các file pilot đã lưu. Chưa đồng bộ hoặc xác nhận trạng thái GitHub mới hơn. Bảy file nguồn giữ nguyên hash checkout so với lần kiểm 21/10.

## 1. Kết luận đọc nhanh

- Ghép đủ 15/15 query bằng `(image_id, query_id)`; không ghép theo thứ tự dòng. Manifest 30 dòng, input chọn 15; B2 ghép 6+9 dòng từ hai run.
- Số đếm, số box/score và bảng `per_query` khớp nguồn. 15 query đều present, B0/B2 đều ok; paired=15.
- Tính độc lập từ prediction đã lưu: B0 MAE=19.4, RMSE≈24.315976; B2 MAE=22, RMSE≈30.090973. Exact count=1/15 mỗi nhánh. B2 tốt hơn 6, kém hơn 4, giữ nguyên 5 query.
- q05_2: 14 box = 5 box trên 4 raspberry phân biệt + 9 sai loại; trong 5 box mục tiêu có 1 box dư do cùng vật. Box 7 và 11 cùng object ID.
- Trong phạm vi count metrics trên pilot đã lưu, không phát hiện chênh lệch giữa nguồn và kết quả evaluator. Điều này không khẳng định các box đều đúng loại hoặc đúng vị trí.

## 2. Bốn ca đã kiểm hộ

| Query / prompt | GT | B0 | B2 | Sai số B0 | Sai số B2 | Kết luận |
|---|---:|---:|---:|---:|---:|---|
| q01_1 / guitars | 25 | 25 | 25 | 0 | 0 | Count khớp; không thay phép chấm box |
| q01_3 / chairs | 1 | 0 | 0 | 1 | 1 | Lớp có mặt bị bỏ sót; không phải absent |
| q05_2 / raspberries | 4 | 11 | 14 | 7 | 10 | B2 kém hơn về count dù tìm đủ 4 vật mục tiêu |
| q05_3 / blackberries | 3 | 21 | 79 | 18 | 76 | Giữ nguyên ca sai lớn trong metric |

MAE B0=291/15=19.4; B2=330/15=22. RMSE B0=sqrt(8869/15), B2=sqrt(13582/15). Bảng [đối chiếu đủ 15 dòng](audits/PER_QUERY_TRACE_20261024.csv) và [audit có hash, coverage, manual](audits/TRIEU_EVALUATOR_20261024.json) là bằng chứng kèm theo.

## 3. Các nhánh error/null/uncertain/absent đã đọc hộ

Đây là đối chiếu logic bằng cách đọc code, chưa phải chạy test nhánh giả lập trong lượt này.

| Trường hợp | Hành vi của code | Ý nghĩa |
|---|---|---|
| `execution_status=error` | Yêu cầu `final_count=null`; loại khỏi tập valid/paired | Không đổi lỗi thực thi thành dự đoán 0 |
| GT `uncertain` | Loại khỏi GT dùng tính metric | Không coi nhãn chưa chắc là absent |
| GT `absent` | Yêu cầu `gt_count=0` | Khác trường hợp chairs GT=1 nhưng model trả 0 |
| Không có query absent | FPR_absent và MeanAbsentCount trả null | Chưa có dữ liệu để đo, không phải lỗi bằng 0 |
| B0 hoặc B2 bị lỗi | So sánh paired trên giao hai tập valid; báo coverage | Không so hai nhánh trên tập mẫu khác nhau |

Pilot hiện tại không có error/uncertain/absent, nên các nhánh đó không được kiểm bằng dữ liệu pilot thật. `presence_recall=14/15` ở cả hai nhánh chỉ thể hiện query có count dương, không chứng minh đếm đúng loại.

Điểm code: [key/indexed](https://github.com/minhtridaoo/CS331/blob/31278dd70377578accda4d126a95b14d33bcdef0/evaluation/evaluate_pilot.py#L32), [validate_prediction](https://github.com/minhtridaoo/CS331/blob/31278dd70377578accda4d126a95b14d33bcdef0/evaluation/evaluate_pilot.py#L49), [evaluate](https://github.com/minhtridaoo/CS331/blob/31278dd70377578accda4d126a95b14d33bcdef0/evaluation/evaluate_pilot.py#L69), [manual_check](https://github.com/minhtridaoo/CS331/blob/31278dd70377578accda4d126a95b14d33bcdef0/evaluation/evaluate_pilot.py#L146).

## 4. Phạm vi và điểm còn mở

- Lượt này chạy script PowerShell đối chiếu độc lập các file đã lưu; không import/chạy evaluator, self-test, model, CLIP hoặc train. Self-test PASS vẫn là Minhtri báo trong handoff, chưa có stdout mới.
- Hash nguồn: 3/7 khớp byte của run; 4/7 chỉ khác CRLF/LF trên Windows. Không có khác biệt nội dung chưa giải thích trong 7 nguồn. Không ép sửa nguồn hoặc metadata.
- `manual_check` đếm nhãn đã cung cấp; không tự nhận diện lại ảnh, không chấm IoU/AP hoặc xác nhận các cờ extent lịch sử thay Triệu.
- Validator chưa yêu cầu bbox nằm hoàn toàn trong biên ảnh; đây là giới hạn cần xử lý nếu mở đánh giá vị trí, không sửa count nguồn trong audit này.
- File kết quả `_r2` trùng run chính, không tăng cỡ mẫu. Chưa có absent/holdout để kết luận rộng hơn pilot dev.
- P4 đã có artifact score/khảo sát trong repo nhưng chưa được audit hiệu quả ở lượt này. Trí cần đồng bộ log; lựa chọn phương pháp/duyệt thuộc nhóm.

## 5. Triệu đã đọc và chấp nhận kết quả — 24/10/2026

Triệu xác nhận trực tiếp trong chat:

> Tôi đã đọc và hiểu bản kiểm ngày 24/10, đồng ý dùng kết quả kiểm kỹ thuật do assistant thực hiện.

[Bản ghi xác nhận](audits/TRIEU_ACCEPTANCE_20261024.json) đã lưu. Người kiểm kỹ thuật là assistant; Triệu đã đọc/hiểu và chấp nhận kết quả được ủy quyền, không ghi Triệu đã tự audit code. Phần xác nhận này đã cập nhật vào PILOT_SUMMARY mục 7. Bản audit kỹ thuật trước đó được giữ nguyên như lịch sử.

**Việc tiếp theo:** Triệu cùng Trí duyệt toàn bộ PILOT_SUMMARY và ghi quyết định chung; Trí đồng bộ log/cấu hình P4 với artifact đã có. Chưa ghi nhóm đã duyệt, pilot đã đóng hoặc P4 đã được chọn.

Tin nhắn nháp để Triệu tự gửi Trí (assistant chưa gửi):

> Tớ đã đọc, hiểu và đồng ý dùng bản kiểm kỹ thuật do assistant thực hiện. 15 query, metric và q05_2 đều khớp; xác nhận đã được ghi vào PILOT_SUMMARY mục 7. Mình cùng duyệt báo cáo pilot và chốt bước tiếp theo nhé. Phần P4 đã có artifact thì cậu đồng bộ giúp log/cấu hình trước khi chốt.
