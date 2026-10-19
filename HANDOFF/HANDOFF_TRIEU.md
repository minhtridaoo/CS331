# Handoff Triệu — Dữ liệu và bộ đánh giá

**Mốc mới nhất 16/10 — đã nhận kiểm chéo của Triệu cho 14/15 query:** số đếm/GT khớp file kết quả; còn q01_1 guitars chưa có review trực tiếp. Plates hiệu chỉnh từ 0/3 theo Trí thành 3/3 đúng loại theo Triệu và ảnh đã kiểm; bản gốc giữ nguyên. Raspberries final đã giải thích đủ 14 = 4 quả mục tiêu + 1 khung trùng + 9 khung sai loại. Stage1 có 2 strawberry ở số 6/7, giải thích đủ 11 khung. **Tiếp theo:** bổ sung guitar và đối sánh q04_2 blueberries; dùng nhãn q05_2 để kiểm evaluator, không làm lại từ đầu. Giữ kế hoạch benchmark Kaggle hiện có; chưa có metric Kaggle mới. [Đối chiếu chi tiết](../results/countgdpp/b2_remaining3_20261015/TRIEU_CROSSCHECK_2026-10-16.md).

**Cập nhật 16/10/2026. Người phụ trách theo kế hoạch: Triệu.**
[Handoff chung](HANDOFF.md) · [Pipeline phân công và schema v1](../roadmap/PIPELINE_PHAN_CONG.md) · [Protocol nghiên cứu](../roadmap/PIPELINE_COUNTGDPP.md)

## Mục tiêu của phần việc

Tạo đầu vào có nhãn đáng tin và viết chương trình đo mô hình có đếm đúng loại được hỏi hay không. Trên cùng ảnh: X có mặt, Y khác loại cũng có mặt, Z chắc chắn vắng mặt. Count bằng nhau không tự chứng minh mô hình sai; phải kiểm tra khung dự đoán.

Phần này làm được bằng CPU, không cần chờ bạn kia cài GPU hoặc chạy CountGD++. Đã kiểm gói Triệu cung cấp gồm 10 ảnh/30 query cùng GT/annotations ngày 14/10; không còn trạng thái chưa có dữ liệu. Checklist dưới đây là yêu cầu đầy đủ còn phải đối chiếu, chưa xác nhận evaluator.

## Cập nhật từ nhánh mô hình

Đã có một output spoon thật: [results.json](../results/countgdpp/smoke_spoon/results.json), count=19 so với GT thủ công 7. Đã có thêm fork=14/GT7 và cat=0/GT0, đủ ba output gốc smoke; chưa chuẩn hóa schema v1 hoặc ghép evaluator để đóng G1. Nhánh model đã audit, chuẩn hóa input/manifest, chạy B0/B2 5 ảnh và E1/E2 2 ảnh. Trí đã review đủ 15 query; Triệu đã kiểm chéo 14 query, còn guitar/q04_2, evaluator T3–T5 và absent có xác nhận. [Work log](WORKLOG_CS331.md).

## Việc đầu tiên

- [ ] Đọc schema v1 ở pipeline phân công; thống nhất ID/prompt với bạn kia trên một ảnh mẫu.
- [ ] Chọn 5 ảnh rõ, mỗi ảnh có hai loại khác nhau, đếm được bằng mắt. Ghi nguồn và quyền sử dụng.
- [ ] Mỗi ảnh tạo ba query: X, Y, Z vắng mặt → tổng 15 dòng ban đầu.
- [ ] Kiểm nhãn theo cả ảnh; không coi lớp thiếu annotation là vắng mặt.
- [ ] Tạo manifest.csv và xuất inference_inputs.jsonl chỉ chứa thông tin được phép.
- [ ] Viết evaluator bằng Python, kiểm bằng bảng giả ở pipeline §7.

## Pipeline cá nhân

1. **T1 — dữ liệu:** 5 ảnh đầu; ghi nguồn, source_group_id, quy tắc đếm.
2. **T2 — manifest:** nhãn đếm/presence/split; mỗi cặp image_id/query_id duy nhất. Tất cả biến thể của cùng ảnh gốc cùng split.
3. **T3 — evaluator:** đọc manifest và predictions.jsonl; kiểm schema/ID/count–boxes; ghép bảng; tính các metric và coverage.
4. **T4 — kiểm chương trình:** fixture giả có đáp án biết trước; thêm lỗi thiếu/trùng ID, null/error, count không khớp khung.
5. **T5 — nối kết quả thật:** nhận 3 dòng B0 đầu tiên, đối chiếu nhãn/overlay với bạn kia; sau đó 15 dòng.
6. **T6 — phân tích:** mở rộng 20–30 ảnh dev; chuẩn bị holdout riêng; so B0/B2 và các ngưỡng trên cùng ảnh/query.

Không cần tìm thêm model hay viết UI trong nhánh này. Triệu có trách nhiệm code evaluator và phân tích lỗi, không chỉ thu thập ảnh/viết báo cáo.

## Sản phẩm phải bàn giao

**Cho người chạy model:**
- Ảnh và file inference_inputs.jsonl của dev, không có GT.
- Manifest riêng cho đánh giá, nguồn dữ liệu, phiên bản/hash, ghi chú ca chưa chắc.
- Quy tắc tên prompt và một ảnh đã kiểm tra chéo.

**Cho cả nhóm:**
- Code evaluator trong evaluation/ (vị trí dự kiến).
- metrics.json, per_query.csv, error_review.csv, pilot_summary.md.
- Hướng dẫn chạy evaluator trên fixture và dữ liệu thật.
- Ca đúng lẫn ca sai, không chỉ ảnh đẹp.

## Cách biết phần việc đạt

- Fixture ở pipeline §7 cho MAE 0.5, RMSE ≈ 0.7071, presence recall 0.75, FPR_absent 0.5, MeanAbsentCount 0.5.
- ID thiếu/trùng hoặc count không khớp khung được báo rõ.
- Crash không trở thành số 0; unknown GT không trở thành absent.
- Mỗi metric có số ảnh/query và coverage; so biến thể trên cùng tập hợp hợp lệ.
- Có thể giải thích ít nhất một ví dụ count đúng nhưng khung sai lớp, nếu thực tế gặp; không tự bịa ví dụ thành kết quả model.
- Chỉ gọi kết quả thật sau khi nhận prediction từ CountGD++; mọi fixture ghi rõ mô phỏng.

## Giới hạn nghiên cứu

Không dùng holdout để chọn prompt/ngưỡng/phương pháp. Nếu chưa có nhãn vị trí đầy đủ thì chấm lỗi lớp thủ công theo quy ước, không tự gọi là CntF1 chuẩn. Presence recall chỉ là trả số dương; cần MAE và kiểm khung để đánh giá đúng yêu cầu thầy.

## Nhật ký bàn giao buổi sau

- Số ảnh/query đã kiểm:
- File dữ liệu/evaluator:
- Fixture đã đạt:
- Ca nhãn mơ hồ hoặc lỗi:
- Kết quả thật đã nhận:
- Việc tiếp theo:

Mẫu này chưa điền; chưa có kết quả hoặc xác nhận Triệu đã thực hiện.
