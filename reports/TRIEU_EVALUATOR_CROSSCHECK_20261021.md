# Triệu — kiểm chéo evaluator theo WORKLOG

**Ngày chuẩn bị: 21/10/2026. Trạng thái: assistant đã đối chiếu; chờ Triệu đọc và tự xác nhận.**

Nguồn: repo `minhtridaoo/CS331`, commit `31278dd`, WORKLOG ngày 20/10 và Phần 2 mục 3. Đây là phần hỗ trợ Triệu kiểm phép chấm đã có, không phải review lại 15 ảnh, chạy inference mới hoặc tự ký thay người kiểm.

## 1. Việc của Triệu ở mốc này

1. Hiểu cách evaluator ghép ID và chọn 15 query.
2. Kiểm bốn dòng minh họa và cách tính sai số.
3. Kiểm cách `manual_check` đếm nhãn q05_2.
4. Hiểu ý nghĩa error/null/uncertain và absent=null.
5. Sau khi thực sự kiểm, điền tên/ngày/kết luận tại `reports/PILOT_SUMMARY.md`, mục 7. Nhóm duyệt báo cáo/P4 là xác nhận riêng.

Không cần cài CUDA, chạy lại model, gán nhãn lại 15 query hoặc viết một evaluator khác cho bước này.

## 2. Đọc code theo bốn điểm

### A. Ghép ID

[indexed, dòng 36](https://github.com/minhtridaoo/CS331/blob/31278dd/evaluation/evaluate_pilot.py#L36) tạo bảng theo cặp `(image_id, query_id)`, báo lỗi nếu trùng. Không ghép ảnh/prediction bằng số thứ tự dòng.

[evaluate, dòng 69](https://github.com/minhtridaoo/CS331/blob/31278dd/evaluation/evaluate_pilot.py#L69) lấy tập ID từ `first5_inputs.jsonl`. Manifest có 30 dòng nhưng tập input chỉ có 15 dòng: 5 ảnh đầu, mỗi ảnh 3 query. B0 có 15 dòng; B2 ghép 6 dòng và 9 dòng từ hai run.

Code yêu cầu B0/B2 có đúng tập ID input: thiếu hoặc thừa đều dừng. Bảng `per_query.json` có thể được sắp xếp khác input vì code sort ID, nhưng phép ghép vẫn đúng.

**Đối chiếu 21/10:** đã kiểm đủ 15/15 cặp ID, prompt input/manifest và số liệu per_query với prediction gốc; khớp.

### B. Kiểm prediction và các ca không hợp lệ

[validate_prediction, dòng 49](https://github.com/minhtridaoo/CS331/blob/31278dd/evaluation/evaluate_pilot.py#L49) kiểm schema/status, count nguyên không âm, count bằng số box và score, tọa độ hữu hạn/diện tích dương, score trong [0,1].

- `execution_status=error` phải có `final_count=null`. Ca lỗi không được đổi thành count 0.
- GT `uncertain` được loại khỏi tập chấm, không coi là absent.
- So B0/B2 bằng tập query hợp lệ chung; ngoài ra có coverage của từng nhánh.
- Với 15 query đang lưu: cả hai nhánh có 15 valid, 0 error; không có uncertain.

**Giới hạn code hiện tại:** không kiểm box nằm hoàn toàn trong biên ảnh hoặc chấm độ khít của box. Điều này không thay đổi count metric đang kiểm. Chấm vị trí sau này cần quy tắc rõ; không tự loại/cắt box trong lượt kiểm này.

### C. Công thức và bốn dòng dễ kiểm

- Sai số tuyệt đối của một query: `abs(predicted_count - gt_count)`.
- MAE: trung bình các sai số tuyệt đối.
- RMSE: căn bậc hai của trung bình các sai số bình phương.
- Exact count: số query có count bằng GT, không phải xác nhận box đúng loại.

| Query | GT | B0 | B2 | Sai số B0 | Sai số B2 | Cần hiểu |
|---|---:|---:|---:|---:|---:|---|
| q01_1 guitars | 25 | 25 | 25 | 0 | 0 | Count khớp |
| q01_3 chairs | 1 | 0 | 0 | 1 | 1 | Bỏ sót vật có mặt, không phải absent |
| q05_2 raspberries | 4 | 11 | 14 | 7 | 10 | Count khác số vật mục tiêu được phát hiện |
| q05_3 blackberries | 3 | 21 | 79 | 18 | 76 | Giữ ca lỗi lớn khi tính metric |

**Kết quả đối chiếu số học từ prediction đã lưu:**

| Nhánh | Query hợp lệ chung | MAE | RMSE | Exact count |
|---|---:|---:|---:|---:|
| B0 | 15 | 19.4 | 24.315975544210986 | 1 |
| B2 | 15 | 22.0 | 30.090973175799196 | 1 |

B2 cải thiện 6 query, kém đi 4, giữ nguyên 5. Các số khớp metrics.json và per_query.json của run chính. Bốn file kết quả của run `_r2` giống run chính; không cộng thành 30 mẫu.

**Absent:** 15 query đều present, nên `n_absent=0`, `FPR_absent=null`, `MeanAbsentCount=null`. Null ở đây là không có dữ liệu để đo, không phải mô hình không mắc lỗi absent. `presence_recall=14/15` chỉ cho biết 14 query trả count dương; không cho biết chúng đếm đúng loại.

### D. q05_2: số box và số vật là hai khái niệm

[manual_check, dòng 146](https://github.com/minhtridaoo/CS331/blob/31278dd/evaluation/evaluate_pilot.py#L146) đọc nhãn đã gán, đối chiếu run/query, index, số trên overlay và tọa độ với prediction. Sau đó đếm `is_target` và số `visual_object_id` phân biệt.

| Nội dung | Kết quả |
|---|---:|
| Tổng box final | 14 |
| Box trên raspberry: 1, 2, 3, 7, 11 | 5 |
| Raspberry phân biệt | 4 |
| Box dư trên cùng raspberry: 11 cùng vật với 7 | 1 |
| Box sai loại còn lại | 9 |

Đã đối chiếu đủ 14 index, overlay ID và tọa độ với prediction; manual_check.json khớp. Các cờ `extent=partial` trong nhãn lịch sử không được hàm này dùng để tính kết quả, không tự coi là nhãn phần vật do Triệu xác nhận. Hàm không nhận diện lại ảnh, không chấm IoU/AP.

## 3. Hash nguồn trên Windows

Run_config lưu 7 hash nguồn. Trong checkout Windows của lượt này:

- 3/7 khớp chính xác byte: manifest, first5_inputs và nhãn manual q05_2.
- 4/7 lệch byte nhưng khớp chính xác sau khi đổi CRLF về LF: ba file prediction và evaluate_pilot.py.
- Không còn chênh lệch nội dung chưa giải thích trong 7 nguồn.

Không gọi đây là 7/7 khớp byte thô. Không sửa raw prediction hoặc metadata cũ để ép hash. Đã lưu cả hash checkout và hash LF trong [audit JSON](audits/TRIEU_EVALUATOR_20261021.json).

Self-test PASS là thông tin Minhtri đã báo trong handoff trước; lượt này không chạy/import evaluator, self-test hoặc model. Phép đối chiếu số học và kiểm các file đã lưu không phải run đánh giá nghiên cứu mới.

## 4. Bổ sung artifact review q02_1 đã có

Repo thiếu file chi tiết được bản review Triệu liên kết. Đã bổ sung từ kết quả của chính cuộc trò chuyện ngày 19/10, giữ hash nguồn của bản sao:

- [Q02_1_DETAILED_REVIEW.md](<../workspace Trí and Triệu/Triệu/Q02_1_DETAILED_REVIEW.md>).
- Ba JSON đối chiếu stage1/final/15 nhóm đĩa và thư mục chín ảnh bằng chứng.

Các nhóm có độ chắc chắn vừa vẫn được ghi rõ là review của assistant; không dùng chúng để giả xác nhận Triệu đã phân xử mọi box. Không thay đổi GT, ảnh, prediction, ngưỡng hoặc code evaluator.

## 5. Điểm tài liệu chưa đồng bộ về P4

WORKLOG/HANDOFF/PILOT_SUMMARY ngày 20/10 còn các câu “chưa chạy CLIP/P4”. Tuy nhiên commit đang kiểm đã có:

- `results/countgdpp/p4_clip_all15_20261020/run_config.json`, checkpoint/revision CLIP và trạng thái `scores_only_no_filtering`, cùng 15 file score.
- `results/countgdpp/p4_count_cv_20261020/report.json`, ghi phép khảo sát count trên 5-fold theo ảnh dev.
- `results/countgdpp/p4_two_case_object_review_20261020.json`, có phần nhãn q03_2 đánh dấu assistant_preliminary.

Vì vậy không tiếp tục dùng “chưa có artifact P4” làm trạng thái hiện tại. Lượt này chỉ xác nhận các file đó tồn tại/đọc metadata; chưa audit toàn bộ code, score, nguồn chạy hoặc kết luận hiệu quả P4. Cần Trí cập nhật log người chạy/lệnh/cấu hình và trạng thái duyệt trước khi chốt báo cáo P4. Việc này độc lập với phép chấm pilot B0/B2 đang kiểm.

## 6. Triệu xác nhận sau khi đọc

Các mục để tự kiểm:

- [ ] Tôi hiểu ghép theo `(image_id, query_id)`, chọn 15 input từ manifest 30 dòng.
- [ ] Tôi kiểm bốn ví dụ và hiểu MAE/RMSE/exact count.
- [ ] Tôi hiểu error/null/uncertain và absent=null; count dương chưa chứng minh đúng loại.
- [ ] Tôi đối chiếu q05_2: 14 box = 5 box mục tiêu trên 4 vật + 9 sai loại.

**Mẫu chỉ dùng sau khi thực sự kiểm; hiện chưa phải chữ ký:**

> Triệu — [ngày tự kiểm]: đã đọc luồng ghép ID, kiểm bốn ca minh họa và manual q05_2. Kết quả pilot khớp trong phạm vi count metrics trên 15 query dev. Hiểu absent=null và giới hạn của nhãn hậu kiểm; [đạt / còn sửa mục ...].

Sau đó điền mục 7 PILOT_SUMMARY. Không tự tích “nhóm duyệt”, chọn CLIP hoặc đóng pilot thay Trí/cả nhóm. Không cần chạy lại evaluator chỉ để hoàn thành phần đọc/kiểm chéo này.
