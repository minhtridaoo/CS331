# Pipeline phân công — Bạn và Triệu

**Ưu tiên trạng thái mới nhất 27/10:** Trí đã đọc C1 và chưa duyệt; Triệu tự làm T1–T4 theo [kế hoạch V2](../reports/KE_HOACH_SUA_KIEM_CHEO_20261027.md), hạn đề xuất 30/10–03/11. Việc chấp nhận bản assistant 24/10 không thay yêu cầu tự chạy mới. Trí chọn B, p4_unseen_v1 DRAFT; adapter đã viết, kiểm (1) từ điểm dev đạt, (2)–(4) chưa kiểm đầy đủ. T1 không sửa evaluator; fixtures đủ 15 query, giữ q05_2. Các mô tả giai đoạn trước bên dưới là nguồn tham khảo nếu khác điểm tiếp tục này.

**Điểm tiếp tục 27/10:** pilot đã đủ phần chạy/chấm/viết, Triệu đã chấp nhận bản kiểm evaluator 24/10; còn nhóm duyệt. P4 đã có CLIP/CV/Fusion/freeze đến P4.5c; Trí chuẩn bị dữ liệu mới và runner trong lúc chờ Triệu kiểm 47 nhãn. [Việc tiếp cụ thể](P4_TIEP_THEO.md) · [Roadmap](ROADMAP.md) · [Work log](../WORKLOG.md).

**Cập nhật 27/10/2026. Áp dụng cho CountGD++, roadmap V4.8.**
[Handoff chung](../HANDOFF/HANDOFF.md) · [Handoff của bạn](../HANDOFF/HANDOFF_MODEL.md) · [Handoff Triệu](../HANDOFF/HANDOFF_TRIEU.md) · [Protocol nghiên cứu](PIPELINE_COUNTGDPP.md)

Benchmark của Trí đã chạy đủ FSCD-147 1.190 ảnh; count metrics được kiểm ngày 20/10, MAE=8.336975, RMSE=24.637626. [Báo cáo](../reports/BENCHMARK_FSCD147.md). Nhánh này không thay phần 2–3 của pilot.

## 1. Mục tiêu chung và phần chịu trách nhiệm

Cùng ảnh, đổi X sang Y phải đếm đúng loại được hỏi; hỏi lớp vắng mặt phải trả 0. Đã thử B0 một lượt và B2 có pseudo-exemplar; P4 thử bộ lọc sau B2 bằng CLIP/Fusion, chưa train trọng số. Có dùng nhãn dev chọn ngưỡng, chưa kiểm tập mới.

- **Bạn: nhánh mô hình.** Môi trường GPU, trọng số, chương trình inference, B0/B2, thí nghiệm ngưỡng và tài nguyên.
- **Triệu: nhánh dữ liệu và đánh giá.** Chọn/kiểm nhãn ảnh, chia tập, lập bảng đầu vào, lập trình evaluator và phân tích lỗi. Đây là một nhánh kỹ thuật có sản phẩm code.
- **Cả hai:** thống nhất giao diện dữ liệu, kiểm tra chéo nhãn/vị trí, giải thích kết quả, chọn một can thiệp rồi cùng viết báo cáo.
- Thời gian theo mốc hoàn thành, không phải deadline chính thức. Phân công chưa đồng nghĩa Triệu đã thực hiện việc nào.

## 2. Khung phân công lúc khởi động — để tra lịch sử

Các mốc/diagram dưới đây là khung ban đầu, không phải yêu cầu làm lại. Việc hiện tại theo P4_TIEP_THEO; evaluator đã có, Triệu cần kiểm code/output thay vì bắt đầu viết lại.

~~~mermaid
flowchart LR
    A["Cùng chốt ID, query và định dạng file"] --> M["Bạn: thư viện → custom ops → checkpoint"]
    A --> T["Triệu: 5 ảnh → 15 query → nhãn"]
    T --> I["Đầu vào inference không có GT"]
    M --> B["Bạn: B0 một ảnh, ba query"]
    I --> B
    T --> E["Triệu: evaluator kiểm bằng số giả"]
    B --> P["Dự đoán thật và overlay"]
    P --> E
    E --> R["Cùng kiểm tra kết quả đầu tiên"]
    R --> N["20–30 ảnh → B0/B2 → ngưỡng"]
    N --> C["Chọn một lỗi và can thiệp có đối chứng"]
~~~

## 3. Việc của bạn

| Mã | Việc | Bàn giao khi hoàn thành |
|---|---|---|
| M0 | Clone repo; Python 3.10, PyTorch GPU, GCC, CUDA Toolkit | Đã xác minh ở máy hiện tại; xem handoff cá nhân |
| M1 | Cài phụ thuộc; biên dịch custom ops; cài Detectron2 | Log kiểm tra, phiên bản thư viện, kiểm tra CUDA ops đạt |
| M2 | Tải BERT và checkpoint CountGD++ | Nguồn, SHA256, cấu hình, kết quả kiểm tra nạp trọng số |
| M3 | B0 trên một ảnh/ba query | predictions.jsonl, run_config.json, overlay, thời gian/VRAM |
| M4 | B0 trên 5 ảnh rồi 20–30 ảnh dev | Kết quả đủ ID, tách lỗi thực thi, lệnh tái chạy |
| M5 | B2, ghi mẫu và cả hai lượt | Dự đoán và pseudo-exemplar; chính sách không có mẫu |
| M6 | E1/E2 tách ngưỡng, E3 nếu cần | Các run riêng, cấu hình cố định; chưa chọn bằng holdout |

**Bước hiện tại:** Trí đã hoàn thành B0/B2, evaluator, nội dung pilot và thăm dò P4 đến freeze/audit. Chuẩn bị P4.6a–b; chưa chạy ảnh mới. Triệu đã chấp nhận kiểm evaluator; còn 47 nhãn q03 độc lập và duyệt chung. Tài nguyên/absent/holdout mới chưa hoàn thành; không suy kết quả dev thành hiệu quả tổng quát.

Bạn chịu trách nhiệm chuyển đầu ra gốc của repo sang định dạng chung. Không yêu cầu Triệu đọc riêng từng định dạng nội bộ của B0/B2.

## 4. Việc Triệu có thể bắt đầu ngay

| Mã | Việc | Bàn giao khi hoàn thành |
|---|---|---|
| T1 | Chọn 5 ảnh rõ ràng, mỗi ảnh có X/Y khác loại và một lớp chắc chắn vắng mặt | Ảnh, nguồn, quy tắc đếm, ID ổn định |
| T2 | Tạo manifest, tách trường GT khỏi đầu vào model | 15 dòng manifest.csv và inference_inputs.jsonl không chứa GT |
| T3 | Viết evaluator bằng Python, chạy CPU | Code đọc file, kiểm ID/định dạng, tính chỉ số, bảng từng query |
| T4 | Kiểm evaluator bằng dữ liệu giả biết trước đáp án | Ví dụ trong §7 chạy đúng; tách rõ mock với dự đoán thật |
| T5 | Nhận B0, đánh giá và kiểm tra overlay cùng bạn | metrics.json, per_query.csv, error_review.csv |
| T6 | Mở rộng 20–30 ảnh dev, chuẩn bị holdout riêng và so B0/B2 | Manifest có phiên bản; bảng so cùng ảnh/query, coverage và lỗi |

Triệu không cần chờ GPU hoặc cài CountGD++ để làm T1–T4. Có thể bắt đầu bằng Python với csv/json/math; công cụ gán nhãn khác chỉ thêm khi cần. Chưa biết cấu hình máy Triệu, không áp đường dẫn WSL của bạn sang máy Triệu.

## 5. Định dạng bàn giao v1 — hai bên phải dùng chung

Đây là schema đã dùng cho B0/B2 pilot. Đã có predictions.jsonl chuẩn hóa 15 query; evaluator chuẩn bị 19/10 đã được Trí chạy ngày 20/10, đủ 5 output/run và đã audit; Triệu đã chấp nhận bản kiểm được ủy quyền ngày 24/10, còn duyệt chung pilot.

### 5.1. Triệu → bạn

**manifest.csv** (chỉ evaluator đọc GT):
- schema_version = 1.
- image_id, query_id, source_group_id, image_path, target_class, prompt.
- presence_status: present / absent / uncertain; gt_count: số nguyên không âm hoặc trống nếu chưa chắc.
- split: dev / holdout; pair_id; source_url, license_note, verified_by, uncertainty_note.
- Khóa duy nhất: (image_id, query_id). ID không đổi giữa B0/B2.
- image_path tương đối từ thư mục gốc CS331, dùng dấu /; không dùng đường dẫn tuyệt đối của máy Triệu.

**inference_inputs.jsonl** (model đọc):
- Chỉ schema_version, image_id, query_id, image_path, prompt.
- Không gt_count, presence_status, danh sách lớp có mặt/vắng mặt hoặc nhãn loại trừ.
- Triệu xuất file riêng cho split dev để bạn không vô tình chạy/tinh chỉnh bằng holdout.
- Kèm ảnh hoặc cách truy cập ảnh và phiên bản/hash của manifest.

Một ảnh X/Y/vắng mặt dùng chung image_id, ba query_id khác nhau. Tên prompt tiếng Anh phải thống nhất trước khi chạy.

### 5.2. Bạn → Triệu

**predictions.jsonl**: mỗi dòng là một ảnh–query của một run.

| Trường bắt buộc | Quy ước |
|---|---|
| schema_version, run_id, variant | 1; tên run duy nhất; B0/B2/E1... |
| image_id, query_id | Khớp đầu vào của Triệu |
| execution_status | ok hoặc error |
| final_count | Số nguyên không âm khi ok; null khi error |
| final_boxes | Danh sách [x1,y1,x2,y2], pixel trên ảnh gốc |
| final_scores | Danh sách điểm tin cậy cùng thứ tự khung |
| box_format, image_width, image_height | xyxy_pixels; kích thước ảnh gốc |
| error_message | null khi ok; lý do khi error |
| overlay_path, elapsed_ms, peak_vram_mib | Đường dẫn minh họa và tài nguyên; ghi quy ước đo trong config |

elapsed_ms và peak_vram_mib được phép null khi chưa đo, phải ghi lý do trong run_config; không bịa số hoặc dùng thời gian tải file thay inference. Hoàn thiện phép đo trước khi đóng mốc tài nguyên P0.

Quy tắc: final_count = len(final_boxes) = len(final_scores) khi ok. Kết quả 0 hợp lệ dùng hai danh sách rỗng. Error dùng final_count=null và báo riêng, không đổi thành 0.

B2 thêm stage1_boxes/stage1_scores/stage1_count, pseudo_boxes/pseudo_scores, no_pseudo, stage2_boxes/stage2_scores/stage2_count. Các khung phải có quy ước tọa độ rõ; ưu tiên đồng nhất về ảnh gốc.

**run_config.json:** commit model/adapter, nguồn và hash checkpoint, hash manifest, prompt, ngưỡng, số mẫu, resize/precision/crop, seed, thiết bị và phiên bản môi trường.

### 5.3. Triệu → cả nhóm

- metrics.json: số ảnh/query, số hợp lệ/lỗi/thiếu, MAE_present, RMSE_present, presence_recall, FPR_absent, MeanAbsentCount.
- per_query.csv: GT và dự đoán ghép bằng ID, sai số, trạng thái, đường dẫn overlay.
- error_review.csv: phân loại đúng lớp / nhầm lớp / nền / trùng / thiếu / chưa rõ, người kiểm tra và ghi chú.
- pilot_summary.md: bảng kết quả, ca đúng/sai, giới hạn, câu hỏi cần nhóm quyết định.

Vị trí hiện hành: dữ liệu/input chuẩn hóa trong experiments/countgdpp/m4_inputs/; code inference trong experiments/countgdpp/; evaluator trong evaluation/; kết quả từng run trong results/countgdpp/<run_id>/. Gói dữ liệu/review gốc của Triệu và artifact Kaggle của Trí giữ trong workspace Trí and Triệu/. Đã có experiments/countgdpp/smoke_inputs/ và results/countgdpp/smoke_spoon/, smoke_fork/, smoke_cat/; đã có adapter và bộ input/manifest dev trong experiments/countgdpp/m4_inputs/; evaluation/evaluate_pilot.py đã chạy ngày 20/10 bằng python3: Minhtri báo self-test PASS, output thật đủ và đã đối chiếu. Không yêu cầu venv model cho evaluator CPU.

## 6. Quy tắc evaluator

- Không âm thầm bỏ ID trùng/thiếu, dự đoán không có GT hoặc count khác số khung. Báo lỗi dữ liệu để người tạo sửa.
- Query uncertain không được coi là absent; báo số bị loại. Lỗi inference không được coi là đếm 0.
- Metric trên kết quả hợp lệ phải kèm coverage. So hai cấu hình trên cùng tập cặp hợp lệ và báo riêng số lỗi mỗi bên; không kết luận cải thiện nếu một bên làm rơi nhiều ca khó.
- GT present phải > 0; absent phải = 0, đã xác minh. Thiếu annotation không đủ để coi vật thể vắng mặt.
- Presence recall chỉ là trả số dương, không chứng minh đúng lớp. Đánh giá X/Y phải xem khung.
- Chia dev/holdout theo ảnh gốc; cùng ảnh/crop/query cùng split. Không chọn ngưỡng bằng holdout.
- Dùng định nghĩa trong protocol chung. Chưa tự tính CntF1 nếu chỉ có nhãn count và chưa có quy tắc ghép vị trí.

## 7. Ví dụ giả để Triệu kiểm tra evaluator

**Dữ liệu mô phỏng, không phải kết quả CountGD++.** Khi tạo fixture JSONL, thêm đủ khung/score giả để count khớp số khung; đánh dấu fixture và lưu riêng với kết quả thật.

| Ảnh | Query | Có mặt? | GT | Dự đoán giả |
|---|---|---|---:|---:|
| mock01 | X | Có | 5 | 4 |
| mock01 | Y | Có | 2 | 2 |
| mock01 | Z | Không | 0 | 1 |
| mock02 | X | Có | 3 | 3 |
| mock02 | Y | Có | 1 | 0 |
| mock02 | Z | Không | 0 | 0 |

Đáp án: MAE_present = 0.5; RMSE_present = sqrt(0.5) ≈ 0.7071; presence_recall = 3/4 = 0.75; FPR_absent = 1/2 = 0.5; MeanAbsentCount = 0.5. Tỷ lệ lưu dạng 0–1, chỉ nhân 100 khi hiển thị phần trăm.

Thêm ca kiểm tra có ý nghĩa: thiếu một ID; ID trùng; error/null; count khác số khung. Evaluator phải phát hiện/báo số lỗi thay vì lặng lẽ cho một bảng điểm đẹp.

## 8. Mốc ghép việc và cách phối hợp

1. **G0 — thống nhất giao diện:** đọc §5, cùng kiểm nhãn một ảnh, thống nhất prompt. Nếu đổi schema, cập nhật ở đây trước rồi cả hai cùng sửa.
2. **G1 — nối được:** bạn trả 3 dự đoán thật của một ảnh; Triệu ghép GT đúng, hai người nhìn overlay và bảng lỗi.
3. **G2 — có pilot nhỏ:** 5 ảnh/15 query B0 được kiểm tra; mới mở rộng 20–30 ảnh.
4. **G3 — có đối chứng:** cùng ảnh/query B0/B2 và E1/E2; đọc cả lỗi vắng mặt và chất lượng có mặt.
5. **G4 — quyết định nghiên cứu:** chọn một lỗi có bằng chứng và một can thiệp; thống nhất trước khi mở holdout.

Sau mỗi mốc có bằng chứng, nối thêm [work log](../WORKLOG.md), đồng bộ handoff và pipeline theo yêu cầu người dùng. Cuối mỗi buổi, cập nhật handoff cá nhân: việc xong, đường dẫn/lệnh tái chạy, kết quả kiểm tra, lỗi còn lại, bước kế tiếp. Chỉ ghi “xong” khi có sản phẩm kiểm được. Không cần đợi người kia hoàn thành toàn nhánh mới ghép G1.


## 9. Phần 2–3 và P4 hiện hành, cập nhật 22/10

[Phần 2](PHAN_2_DANH_GIA.md) chỉ rõ code, input, lệnh self-test/đánh giá và đáp án mong đợi. [Phần 3](PHAN_3_TONG_KET.md) chỉ rõ bản báo cáo phải sửa. Trong bản evaluator ban đầu, bảng từng query xuất per_query.json thay vì CSV; cùng nội dung/khóa schema. Nếu cần CSV để báo cáo thì xuất thêm có kiểm tra, không là điều kiện bắt buộc để chốt pilot.

M0–M6, T1–T6 và G0–G4 phía trên là khung đầy đủ; hoàn thành pilot nhỏ không đồng nghĩa mọi gate dev/absent/holdout đã đạt. Người dùng tự chạy; assistant muốn chạy đánh giá thay phải hỏi trước.

[Hướng dẫn P4 tiếp theo](P4_TIEP_THEO.md) tách rõ đóng pilot, nhãn P4, dữ liệu mới và runner dùng freeze. Không cần thực hiện lại toàn bộ kế hoạch 20–30 ảnh dev cũ trước khi làm bước tiếp đã chốt này.

**Buổi tiếp theo có 3 giờ:** theo [CHECKLIST_3_GIO](CHECKLIST_3_GIO.md), chia sẻ T0 → tiếp C2/C3 → ghi C4. C1 đã đọc, Trí chưa duyệt và yêu cầu Triệu tự làm T1–T4 V2. Chưa chạy ảnh mới; chỉ đánh dấu sau bằng chứng.
