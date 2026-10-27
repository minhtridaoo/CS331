# HANDOFF TOÀN DIỆN — CS331 CountGD++: Từ `PILOT_SUMMARY.md` đến P4.5c

**Ngày đóng gói:** 22/10/2026  
**Phạm vi thời gian:** công việc với ChatGPT từ lúc thực hiện phần đánh giá–tổng kết pilot (`PILOT_SUMMARY.md`, tập trung 20/10/2026) đến khi nhận được log `P4 FREEZE AUDIT PASS` (21/10/2026), cộng quyết định phạm vi đã trao đổi ngày 22/10.  
**Người chạy và gửi log:** Minhtri (theo handoff cũ và báo cáo).  
**Người kiểm độc lập đang chờ:** Triệu (không tự coi đã nghiệm thu).  
**Trạng thái:** Bản bàn giao **dựa trên tài liệu và nội dung cuộc trò chuyện**, không phải bản kiểm toán trực tiếp toàn bộ workspace đang chạy tại máy của Minhtri.  
**Thư mục dự án Minhtri dùng:** `/mnt/d/MINHTRIHOCCODE/HOCKI5/CS331` (Ubuntu/WSL), tương ứng ổ `D:` Windows.

> **QUY TẮC ĐỌC BẰNG CHỨNG**
>
> - **[LOG]**: Minhtri đã gửi kết quả đầu ra thực tế của lệnh trong hội thoại; xác nhận lệnh chạy trên máy Minhtri, không đồng nghĩa ChatGPT tự chạy hoặc đọc tất cả file tại máy đó.
> - **[TÀI LIỆU]**: nội dung lấy từ `PILOT_SUMMARY.md`, `PHAN_2_DANH_GIA.md`, `PHAN_3_TONG_KET.md`, handoff P2/P3 đã có; nội dung lịch sử có thể chưa được kiểm chứng lần nữa.
> - **[PHÂN TÍCH SƠ BỘ]**: nhãn từng bbox do assistant đọc ảnh người dùng gửi; đã dùng tính chẩn đoán nhưng **chưa** phải nhãn được Triệu chấm độc lập.
> - **[ĐỀ XUẤT]**: mã lệnh hoặc kế hoạch assistant cung cấp, chưa có log chạy tương ứng.
> - **[CHỜ]**: chưa có xác nhận hoặc chưa hoàn tất tính đến bản handoff này.
>
> Báo cáo này **không tạo thêm thực nghiệm, không tự nhận đã huấn luyện lại CountGD++, không bịa thời gian chạy, không gọi kết quả dev là holdout**, và không suy diễn việc nhóm/Triệu đã duyệt nếu không có bằng chứng.

---

## 0. Đọc nhanh: tình trạng cuối cùng

| Hạng mục | Trạng thái chứng cứ | Kết luận ngắn |
|---|---|---|
| P2: tự chạy evaluator B0/B2 | **[LOG] Đã chạy** | 5 ảnh/15 query; B0 MAE 19.4; B2 MAE 22.0; self-test được người chạy xác nhận PASS |
| P3: `reports/PILOT_SUMMARY.md` | **[TÀI LIỆU] Đã cập nhật, vẫn là bản nháp** | `CHỜ KIỂM CHÉO VÀ DUYỆT` |
| Review định tính pilot | **[TÀI LIỆU] Có review 15/15 từ Trí/Triệu** | Review bằng mắt, không phải chuẩn IoU/AP |
| P4 CLIP probe | **[LOG] Đã chạy** | `q03_2`, `q05_2`, chẩn đoán điểm crop–text |
| P4 CLIP cho toàn 15 query | **[LOG] Đã chạy** | 481 bbox; 15 file điểm |
| P4 so sánh lọc điểm B2 / CLIP | **[LOG] Đã chạy** | Cross-validation theo ảnh gốc: MAE 4.6 / 6.8; B2 gốc 22.0 |
| P4 review vật thể `q03_1`,`q03_2`,`q03_3`,`q05_2` | **[LOG] Đã tính từ nhãn hiện có** | 22 vật mục tiêu; nhãn `q03_*` cần Triệu xác nhận độc lập |
| P4 kiểm tra xếp hạng và prompt | **[LOG] Đã chạy** | Top-K/AUC, phân tích class means; đổi số nhiều→số ít không cải thiện ở ba truy vấn q03 |
| P4 Fusion cố định 50/50 | **[LOG] Đã chạy** | Cross-validation MAE 5.8; review vật: giữ 16/22 vs B2 12/22 trên 4 query được chọn |
| Báo cáo P4 | **[LOG] Đã sinh** | `reports/P4_CLIP_EXPLORATORY_FINDINGS_20261021.md` |
| Bộ ZIP nhờ Triệu gán nhãn độc lập | **[NGƯỜI DÙNG XÁC NHẬN “xong r”]** | Chưa có stdout PASS hoặc CSV Triệu điền trong nội dung đối thoại; cần kiểm trên máy |
| Freeze 2 ứng viên | **[LOG] Đã chạy** | B2 threshold `0.906739`; Fusion threshold `0.655183`, 50/50 |
| Audit freeze | **[LOG] PASS** | 16 nguồn SHA-256 PASS; chuẩn hóa PASS; metrics tái lập PASS |
| P4.6 a–d: kiểm tra ảnh mới và chạy holdout | **[ĐỀ XUẤT] Chưa chạy** | Không phải điều kiện để đóng pilot gốc; cần nếu muốn kiểm chứng khả năng tổng quát của cải tiến |
| Triệu xác nhận kiểm chéo evaluator, nhóm duyệt pilot | **[CHỜ]** | Hai điều kiện chính để chính thức đóng pilot |

**Hai kết luận tách biệt:**

1. **Task pilot ban đầu:** phần tính toán và báo cáo đã làm; chưa có bằng chứng Triệu kiểm chéo evaluator mới và nhóm duyệt nên **không tự ghi “đã chốt pilot”**. Không yêu cầu P4.6 để đóng pilot.
2. **Nhánh nghiên cứu CLIP/Fusion:** đã hoàn thành chuỗi chẩn đoán trên dữ liệu phát triển và khóa cấu hình; **chưa có holdout độc lập**, chưa thể tuyên bố đã chứng minh cải tiến hiệu quả trên dữ liệu mới.

---

## 1. Bối cảnh, câu hỏi nghiên cứu và phạm vi pilot

### 1.1. Câu hỏi ban đầu

Trong **cùng một ảnh có nhiều loại vật**, khi đổi loại cần đếm trong câu hỏi (*query X/Y*), mô hình CountGD++ có thực sự tìm/đếm đúng **loại** được hỏi không, hay chỉ giảm/tăng số bbox mà vẫn khoanh sai vật?

**Baseline được giữ từ dự án:**

- **B0:** một lượt suy luận theo mô tả văn bản.
- **B2:** lượt đầu → tự chọn tối đa **3 pseudo exemplar** → lượt thứ hai. Báo cáo pilot ghi `tau_sample = tau_final = 0.23`; nếu không có mẫu thì adapter trả về B0. Không được gọi adapter này là toàn bộ pipeline tái hiện nguyên bản bài báo CountGD++.
- **Tập pilot:** **5 ảnh gốc**, **15 truy vấn dev**; cả 15 là truy vấn vật cần tìm **có mặt**. Không có thử nghiệm absent hoặc holdout trong 15 query.
- **GT:** nhãn đếm chuẩn dùng cho tính chỉ số, không làm input cho model khi sinh dự đoán.
- **Benchmark FSCD-147 1.190 ảnh:** có báo cáo riêng `reports/BENCHMARK_FSCD147.md`; **không trộn** metrics với pilot 5 ảnh.

### 1.2. 5 ảnh dev đã dùng xuyên suốt P4

`mcac_100`, `mcac_11`, `mcac_20`, `mcac_200`, `mcac_27` (thứ tự ở các vòng fold có thể khác). Tổng 15 truy vấn, bình quân 3 query/ảnh. Vì ba query `q03_*` đều dùng `mcac_200`, chúng **không phải ba ảnh kiểm thử độc lập**.

### 1.3. Bằng chứng định tính đã có trước phần P4 mới

Theo `PILOT_SUMMARY.md` và review Triệu chốt v1 ngày 19/10:

- Trí và Triệu đã review định tính **15/15 query**; 23/42 pseudo mẫu được review là đúng loại (14 query có 3 mẫu, ca chairs không có mẫu). Đây không phải IoU/AP.
- `q04_2` blueberries: 32 bbox cuối được diễn giải là 24 blueberry + 7 blackberry + 1 red currant; khác biệt 35/32 lịch sử được làm rõ theo review. Không đổi GT blueberries = 24.
- `q05_2` raspberries: **14 bbox = 4 quả đúng phân biệt + 1 bbox dư/trùng + 9 bbox sai loại**.
- `q02_1` plates: phần ghép bbox/nhóm vật có ghi nhận của assistant, mức chắc chắn không hoàn toàn đồng nhất; file chi tiết được liên kết trong review nhưng không được xác minh tồn tại lúc handoff P2/P3.
- `q03_1` pens: theo review Triệu, pseudo 1/3 đúng loại; final có tất cả bút và 1 thước.
- `q03_2` rulers: pseudo 3/3 đúng loại nhưng final vẫn có các loại khác.
- `q03_3` pencils: pseudo 0/3 đúng loại (cả ba là bút mực), final trộn bút/chì/thước.
- `q01_3` chairs: GT=1 nhưng B2 về 0; bộ lọc sau B2 **không có cơ chế khôi phục bbox đã mất**.
- Ca blackberries từng tăng dự đoán từ 21 lên 79; chưa phân loại đầy đủ mọi khung để kết luận toàn bộ nguyên nhân.

Nhận định khoa học lúc này: **count đúng không đảm bảo class đúng; pseudo đúng không bảo đảm final đúng; count giảm chưa chứng minh đã lọc đúng đối tượng.** Không gán một cơ chế nhân quả duy nhất chỉ từ quan sát.

---

## 2. Mốc P2 — chạy lại evaluator pilot ngày 20/10

### 2.1. Khởi động / sự cố môi trường

- Người dùng chạy Ubuntu WSL (có dùng `wsl -d Ubuntu -u root` trong tài liệu bàn giao cũ) rồi `cd /mnt/d/MINHTRIHOCCODE/HOCKI5/CS331`.
- Trong lượt P2, lệnh `python` không có alias và venv `/root/.venvs/countgdpp/bin/activate` theo chỉ dẫn ban đầu không tồn tại; thực tế chuyển qua `python3` của hệ thống. **Đừng nhầm venv P2 này với venv P4 được tạo về sau**.
- Lệnh self-test mà Minhtri báo PASS: `python3 evaluation/evaluate_pilot.py --self-test`. Có **xác nhận PASS của người chạy**, không có stdout nguyên vẹn của lần self-test trong handoff P2/P3 cũ.

### 2.2. Chạy evaluator trên dự đoán B0/B2 đã lưu

```bash
python3 evaluation/evaluate_pilot.py --out results/countgdpp/pilot_eval_20261020
```

**[LOG/TÀI LIỆU]** Chương trình **chấm lại dự đoán đã lưu**, không sinh dự đoán bằng CountGD++ trong bước này. Nguồn B0/B2, nhãn và query được ghép theo ID; B2 ghép 6 query trong run 2 ảnh + 9 query trong run 3 ảnh. Dữ liệu nhãn q05_2 được đọc để kiểm tra thủ công.

5 tệp output theo P2 và nội dung báo cáo:

```
results/countgdpp/pilot_eval_20261020/
├── metrics.json
├── per_query.json
├── manual_check.json
├── run_config.json
└── SUMMARY.md
```

Bản `PILOT_SUMMARY.md` sau cập nhật ghi đã đối chiếu 15 dòng, metrics, manual_check, SHA-256 của **7 nguồn**; có run `_r2` cho output tương ứng và hash nguồn tương đương, không coi `_r2` là mẫu độc lập. Đây là thông tin **theo nội dung báo cáo**, không có lý do nhân đôi số lần thử nghiệm.

### 2.3. Kết quả định lượng pilot

| Chỉ số | B0 | B2 |
|---|---:|---:|
| Số ảnh | 5 | 5 |
| Truy vấn hợp lệ | 15/15 | 15/15 |
| Error/uncertain | 0/0 | 0/0 |
| MAE | **19.4** | **22.0** |
| RMSE | **24.315975544210986** | **30.090973175799196** |
| Exact count | **1/15** | **1/15** |

- `paired.n_queries = 15`; B2 cải thiện so với B0 trên 6 query, kém trên 4, giữ nguyên trên 5.
- Không có query absent: `n_absent=0`; các metric dành cho absent phải để **null**, không chuyển thành 0.
- `q05_2` hậu kiểm: `final_boxes=14`, `target_boxes=5`, `distinct_target_objects=4`, `extra_target_boxes=1`, `wrong_class_boxes=9`.
- Đánh giá: **B2 không cải thiện MAE trung bình pilot so với B0**, dù có một số query được cải thiện.

### 2.4. P2 hoàn thành đến đâu?

Phần chạy và đối chiếu nội bộ có kết quả. **Chưa nhận được xác nhận Triệu kiểm tra chéo evaluator mới** (logic ghép ID, công thức, từng dòng nguồn, `q05_2`) và chưa có biên bản duyệt. Review định tính Triệu ngày 19/10 không thay cho bước kiểm chéo evaluator này.

---

## 3. Mốc P3 — làm `reports/PILOT_SUMMARY.md`

### 3.1. Người dùng và assistant đã làm gì?

- Minhtri mở, đọc, chỉnh và in lại nội dung `reports/PILOT_SUMMARY.md`; assistant hỗ trợ đối chiếu với P2.
- Điền người chạy **Minhtri**, ngày **20/10/2026**, lệnh self-test, đường dẫn run, coverage 15/15, 0 errors/uncertain, bảng B0/B2, phép kiểm `q05_2` và review định tính.
- Vẫn giữ ghi chú đầu file **BẢN NHÁP**, trạng thái **`CHỜ KIỂM CHÉO VÀ DUYỆT`**, không tự điền chữ ký/duyệt của Triệu và nhóm.
- Đề xuất nhánh P4 nhằm giảm **giữ bbox sai loại mà không loại nhầm bbox của vật đúng**. Một ứng viên là CLIP chấm crop–text, luôn so với B2 chỉ lọc theo confidence.
- Có handoff cũ `HANDOFF_CS331_P2_P3_2026-10-20.md`, chốt trạng thái đúng **tại thời điểm 20/10**: CLIP lúc đó mới là đề xuất, chưa có chạy thử trong phạm vi của handoff cũ. **Các thử nghiệm CLIP sau đó là bằng chứng mới, không mâu thuẫn với mốc thời gian handoff cũ.**

### 3.2. Trạng thái `PILOT_SUMMARY.md` khi đóng gói

Bản được truy xuất ở cuộc trò chuyện ghi:

- Mục 1–5: có dữ liệu P2/P3 được cập nhật.
- Mục 6: vẫn viết theo giọng **kế hoạch CLIP dự kiến**, trong đó có câu chưa chạy CLIP; nay **đã lạc hậu** so với log P4 ngày 20–21/10. Cần cập nhật bằng **đường dẫn đến báo cáo P4**, không âm thầm xóa lịch sử kế hoạch ban đầu.
- Mục 7: ô Triệu kiểm chéo evaluator và nhóm duyệt vẫn trống/chưa xác nhận.
- Không có bằng chứng người dùng đã cập nhật `WORKLOG.md`, `roadmap/ROADMAP.md`, `HANDOFF/HANDOFF.md` hoặc đã commit/push các thay đổi lên GitHub.

**Điều kiện đóng pilot theo tài liệu gốc:** xác nhận kiểm chéo evaluator, nhóm duyệt báo cáo, đồng bộ trạng thái tài liệu. **Không yêu cầu CLIP thành công hoặc chạy P4.6.**

---

## 4. P4 hình thành — mô hình và quy tắc thử nghiệm

### 4.1. Câu hỏi can thiệp

Sau khi thấy B2 khoanh lẫn vật sai, nhóm thí nghiệm dùng `openai/clip-vit-base-patch32` (CLIP, không fine-tune) chấm mức tương đồng cosine giữa **crop của mỗi bbox B2 đã có** và mô tả văn bản của query, để nghiên cứu xem có nên loại bbox có điểm thấp.

- Không chạy lại B2 cho các thí nghiệm lọc điểm này; sử dụng `final_boxes`/`final_scores` đã lưu.
- Đầu vào pilot: `experiments/countgdpp/m4_inputs/first5_inputs.jsonl`; B2 JSONL từ `results/countgdpp/b2_two_images_20261015/` và `results/countgdpp/b2_remaining3_20261015/`.
- Crop bbox gốc `xyxy` theo ảnh, dùng `CLIPProcessor`/`CLIPModel`, điểm embedding chuẩn hóa cosine. **Cosine không phải xác suất đúng lớp đã hiệu chuẩn.**
- Prompt ban đầu: `a photo of {prompt}`; ví dụ `a photo of pens`, `a photo of rulers`, `a photo of pencils`.
- Các nhãn người dùng/reviewer **chỉ dùng phân tích sau dự đoán**, không làm input mô hình CLIP.
- Không thay bbox gốc và không khẳng định đã huấn luyện CountGD++ hoặc CLIP.

### 4.2. Máy và môi trường ở P4

- Người dùng ở WSL/Ubuntu, thư mục CS331 trên ổ D.
- GPU theo các log môi trường trước đó: **NVIDIA RTX A2000 Laptop GPU 4 GB**; phép kiểm Torch trên GPU đã hoạt động.
- Venv P4: `/root/.venvs/cs331-p4-clip`, Python **3.12.3**, Torch **2.9.1+cu128**, torchvision **0.24.1+cu128**, transformers **4.57.1** theo phiên kiểm môi trường đã ghi trước.
- Cách kích hoạt đã được Minhtri xác nhận hoạt động:

  ```bash
  source /root/.venvs/cs331-p4-clip/bin/activate
  python --version  # Python 3.12.3
  ```

- Có một lần chạy heredoc bị `python: command not found` do chưa kích hoạt venv; đã khắc phục. Lệnh kết thúc heredoc `PY` phải đứng riêng một dòng. Đây là lỗi thao tác terminal, không phải lỗi model.

---

## 5. P4.1–P4.3: CLIP probe, mở rộng 15 query và so sánh đếm (20/10)

### 5.1. Probe hai truy vấn: `q03_2` và `q05_2`

**[LOG] `CLIP PROBE PASS`** trên hai trường hợp dev đã xem lỗi:

| Query | Vật mục tiêu | GT count | B2 final boxes |
|---|---|---:|---:|
| `q03_2` | Rulers | 6 | 18 |
| `q05_2` | Raspberries | 4 | 14 |

Nguồn lưu:

```
results/countgdpp/p4_clip_probe_20261020/
├── q03_2_clip_scores.json
├── q05_2_clip_scores.json
└── summary.json
```

**Nhận xét quan trọng:** `q05_2` có bốn quả mâm xôi đúng được nhãn ở các rank 1,2,3,7; rank 11 là bbox lặp của quả ở rank 7; một số blackberry được CLIP cho điểm cao. Thử ngưỡng B2 0.8 trên riêng q05_2 từng giữ 4/4 quả đúng, nhưng đây là **chọn hậu nghiệm từ ca đã biết**, không được coi là hiệu quả tổng quát.

Có bước chẩn đoán `q05_2_diagnostic.json` trên cùng ca; nhiều ngưỡng B2/CLIP đã được xem để hiểu lỗi, không phải kết quả holdout.

### 5.2. Chấm điểm CLIP toàn bộ 15 query

**[LOG] `P4 ALL15 PASS`**: CLIP đã chấm điểm **481 bbox B2** trên toàn bộ 5 ảnh/15 query; gồm **15 file `{qid}_clip_scores.json`** và metadata `run_config.json`, `summary.json` ở:

```
results/countgdpp/p4_clip_all15_20261020/
```

Số bbox từng query:

| Query | B2 boxes | Query | B2 boxes | Query | B2 boxes |
|---|---:|---|---:|---|---:|
| q01_1 | 25 | q01_2 | 38 | q01_3 | 0 |
| q02_1 | 31 | q02_2 | 31 | q02_3 | 26 |
| q03_1 | 13 | q03_2 | 18 | q03_3 | 16 |
| q04_1 | 59 | q04_2 | 32 | q04_3 | 84 |
| q05_1 | 15 | q05_2 | 14 | q05_3 | 79 |

Tổng 481. `q01_3` là ca **0 bbox**, bộ lọc sau dự đoán không tìm lại được vật còn thiếu.

### 5.3. So sánh cross-validation theo ảnh gốc

Script được sử dụng theo lịch sử:

```
evaluation/p4_compare_count_cv_20261020.py
results/countgdpp/p4_count_cv_20261020/
├── report.json
└── per_query.csv
```

**[LOG] `P4 COUNT CV PASS`**. Thiết kế: **leave-one-original-image-out** trên 5 ảnh; mỗi lượt chọn ngưỡng dựa trên 4 ảnh phát triển còn lại, kiểm ở ảnh thứ 5. Đây là kiểm tra chéo **bên trong tập phát triển**, không phải holdout chưa động tới trong cả quá trình thiết kế phương pháp.

| Phương pháp | MAE ↓ | RMSE ↓ | Exact |
|---|---:|---:|---:|
| B2 original | 22.0000 | 30.0910 | 1/15 |
| **B2-score threshold** | **4.6000** | **6.6182** | **1/15** |
| CLIP-score threshold | 6.8000 | 8.8468 | 0/15 |

Trong 15 query, lọc CLIP có sai số đếm tốt hơn B2 threshold trên 3, tệ hơn trên 9, bằng trên 3 (theo báo cáo so sánh đã ghi); **B2-score threshold là đối chứng mạnh và đơn giản hơn theo MAE**.

Ngưỡng theo ảnh gốc trong CV (B2 / CLIP):

| Ảnh kiểm | B2 ngưỡng | CLIP ngưỡng |
|---|---:|---:|
| mcac_100 | 0.90674 | 0.24672 |
| mcac_11 | 0.90645 | 0.24706 |
| mcac_20 | 0.90674 | 0.24496 |
| mcac_200 | 0.89714 | 0.24672 |
| mcac_27 | 0.90806 | 0.24421 |

Dự đoán đếm từ file `per_query.csv`:

| Query | GT | B2 gốc | B2 lọc | CLIP lọc |
|---|---:|---:|---:|---:|
| q01_1 | 25 | 25 | 19 | 23 |
| q01_2 | 11 | 38 | 17 | 2 |
| q01_3 | 1 | 0 | 0 | 0 |
| q02_1 | 15 | 31 | 7 | 1 |
| q02_2 | 3 | 31 | 6 | 0 |
| q02_3 | 2 | 26 | 3 | 1 |
| q03_1 | 6 | 13 | 10 | 1 |
| q03_2 | 6 | 18 | 4 | 5 |
| q03_3 | 6 | 16 | 6 | 1 |
| q04_1 | 6 | 59 | 14 | 18 |
| q04_2 | 24 | 32 | 27 | 25 |
| q04_3 | 39 | 84 | 19 | 18 |
| q05_1 | 2 | 15 | 0 | 10 |
| q05_2 | 4 | 14 | 2 | 13 |
| q05_3 | 3 | 79 | 0 | 13 |

**Không hiểu nhầm:** MAE giảm rất nhiều khi lọc bbox **không chứng minh** các bbox giữ lại đúng loại. Đây là động lực cho review từng vật ở bước kế tiếp.

---

## 6. P4 review bbox thủ công: từ hai ca đến ba query cùng ảnh

### 6.1. Hai ca mở đầu `q03_2` và `q05_2`

- `q03_2` (rulers): Minhtri sinh ảnh tổng quan đánh số, contact sheet crop và CSV mẫu ở `results/countgdpp/p4_review_q03_2_20261020/`. Người dùng gửi ảnh; assistant gán nhãn từng rank sơ bộ. Theo ảnh, 6 thước là rank 1–6, 6 bút mực rank 7–12, 6 bút chì rank 13–18; cần phân biệt đây là review **của assistant** theo ảnh, không phải nhãn bbox độc lập Triệu duyệt.
- `q05_2`: dùng nhãn hậu kiểm có sẵn `results/countgdpp/b2_remaining3_20261015/q05_2/manual_crosscheck_20261016.json`; đúng 4 quả phân biệt, 1 bbox lặp, 9 bbox sai loại.
- **[LOG] `P4 TWO-CASE OBJECT REVIEW PASS`** lưu `results/countgdpp/p4_two_case_object_review_20261020.json`:

| Hai query được chọn (GT tổng 10 vật) | B2 threshold | CLIP threshold |
|---|---:|---:|
| Khung giữ | 6 | 18 |
| Vật đúng phân biệt | 6 | 9 |
| Khung sai loại | 0 | 8 |
| Khung trùng | 0 | 1 |
| Vật bỏ sót | 4 | 1 |

Nhãn phần `q03_2` chưa xác nhận độc lập; chỉ là chẩn đoán hai query dev, không thể dùng như đánh giá khách quan đại diện toàn tập.

### 6.2. `q03_3` – pencils, cùng ảnh `mcac_200`

Ảnh đánh số được người dùng gửi, script in:

```
B2 threshold: 0.897137
B2 kept ranks: [1, 2, 3, 4, 5, 7]
CLIP threshold: 0.246715
CLIP kept ranks: [16]
REVIEW q03_3 MATERIALS PASS
```

Theo phân loại từ ảnh do assistant thực hiện:

- **Bút chì thật:** rank **6, 8, 9, 10, 11, 15** (6 vật).
- **Bút mực:** rank **1, 2, 3, 4, 5, 7** (6 vật).
- **Thước:** rank **12, 13, 14, 16** (4 vật).

Người dùng tải bảng `q03_3_annotation_review_assistant_20261020.csv` vào thư mục `results/countgdpp/p4_review_q03_3_20261020/` và chạy kiểm tra. **[LOG] `P4 Q03_3 LABEL CHECK PASS`**:

| Phương pháp | Khung giữ | Vật bút chì đúng | Sai loại | Bỏ sót |
|---|---:|---:|---:|---:|
| B2 threshold | 6 | **0/6** | 6 | 6 |
| CLIP threshold | 1 | **0/6** | 1 | 6 |

**Bài học:** B2 giữ *đúng số lượng 6* nhưng **cả 6 là bút mực**, tức sai số đếm = 0 mà không phát hiện đúng loại được hỏi. CLIP ở đây giữ một thước chứ không phải bút chì.

### 6.3. `q03_1` – pens, cùng ảnh `mcac_200`

**[LOG] `REVIEW q03_1 MATERIALS PASS`**, người dùng gửi ảnh đánh số và trích dẫn mục review Triệu:

```
B2 threshold: 0.897137
B2 kept ranks: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
CLIP threshold: 0.246715
CLIP kept ranks: [12]
```

Theo phân loại sơ bộ của assistant từ ảnh:

- **Bút mực mục tiêu:** rank **1, 2, 4, 6, 7, 9**.
- **Bút chì sai loại:** rank **3, 5, 8, 10, 11, 12**.
- **Thước sai loại:** rank **13**.

Người dùng tải bảng `q03_1_annotation_review_assistant_20261021.csv` vào `results/countgdpp/p4_review_q03_1_20261020/` và chạy. **[LOG] `P4 Q03_1 LABEL CHECK PASS`**:

| Phương pháp | Khung giữ | Vật bút mực đúng | Sai loại | Bỏ sót |
|---|---:|---:|---:|---:|
| B2 threshold | 10 | **6/6** | 4 | 0 |
| CLIP threshold | 1 | **0/6** | 1 | 6 |

Kết quả sơ bộ phù hợp review tổng đếm của Triệu: final 6 bút mực + 6 bút chì + 1 thước. Tuy nhiên **Triệu chưa duyệt mapping rank→vật cụ thể**.

### 6.4. Hoàn thành ba query trên `mcac_200`

| Query | Mục tiêu | B2 threshold đúng | CLIP threshold đúng |
|---|---|---:|---:|
| q03_1 | 6 bút mực | 6/6 | 0/6 |
| q03_2 | 6 thước | 4/6 | 5/6 |
| q03_3 | 6 bút chì | 0/6 | 0/6 |
| **Tổng ba query** | **18 vật** | **10/18** | **5/18** |

Các con số này được suy từ bộ nhãn sơ bộ, **không phải ba phép thử ảnh độc lập**, không phải AP/IoU chuẩn.

---

## 7. P4.4h – Chẩn đoán khả năng xếp hạng (21/10)

**Câu hỏi mới:** Có phải CLIP xếp đúng vật lên cao nhưng dùng ngưỡng sai, hay nó thực sự xếp sai loại? Người dùng đã chạy **[LOG] `P4 RANK DIAGNOSTIC PASS`**, lưu:

```
results/countgdpp/p4_rank_diagnostic_20261021.json
```

Thiết kế: so **Top-K với K bằng GT thật** (oracle chỉ dùng để **chẩn đoán, không thể là luật suy luận trên ảnh mới**), cộng box-label AUC phân biệt bbox đúng loại/sai loại. AUC không đo trùng vật đúng cách như AP định vị và không phải AP theo IoU.

| Query | K | B2 Top-K đúng | B2 AUC | CLIP Top-K đúng | CLIP AUC |
|---|---:|---:|---:|---:|---:|
| q03_1 | 6 | 6/6 | 1.0000 | 1/6 | 0.1667 |
| q03_2 | 6 | 6/6 | 1.0000 | 6/6 | 1.0000 |
| q03_3 | 6 | 0/6 | 0.4000 | 4/6 | 0.7833 |
| q05_2 | 4 | 4/4 | 0.8222 | 2/4 | 0.9556 |
| **Tổng** | **22** | **16/22** | — | **13/22** | — |

Ở q05_2, Top-4 CLIP chứa 2 vật đúng phân biệt, 1 bbox trùng của một vật đúng và 1 bbox sai loại. Vì bbox trùng vẫn được tính như nhãn dương trong AUC, AUC=0.9556 **không** có nghĩa đếm đúng 4 quả.

**Bài học:** quyết định giữ/loại dựa trên **thứ tự** và dựa trên **ngưỡng tuyệt đối** là hai vấn đề khác nhau. Tùy query, CLIP có thể xếp hạng tốt hơn hoặc rất kém.

---

## 8. P4.4i – Điểm trung bình theo loại vật (21/10)

**[LOG] `P4 CLASS SCORE ANALYSIS PASS`**. Nguồn:

```
results/countgdpp/p4_class_score_analysis_20261021.json
```

So sánh cùng ảnh `mcac_200`, phân nhóm bằng nhãn sơ bộ:

| Query/prompt | Nhóm vật | N | B2 mean | CLIP mean |
|---|---|---:|---:|---:|
| q03_1 `a photo of pens` | pen — mục tiêu | 6 | 0.9356 | 0.2274 |
| | pencil | 6 | 0.8723 | 0.2357 |
| | ruler | 1 | 0.2765 | 0.2418 |
| q03_3 `a photo of pencils` | pen | 6 | 0.9329 | 0.2011 |
| | pencil — mục tiêu | 6 | 0.8173 | 0.2274 |
| | ruler | 4 | 0.3733 | 0.2326 |

**Diễn giải đúng phạm vi:** với `pens`, CLIP trung bình chấm **pencil/ruler cao hơn pen**; với `pencils`, CLIP trung bình chấm pencil hơn pen nhưng ruler còn nhỉnh hơn pencil. Chưa thể khẳng định nguyên nhân do text, crop, dữ liệu tiền huấn luyện hoặc kiến trúc chỉ bằng bảng này. Điểm số giữa prompt khác nhau không được xem như xác suất so sánh trực tiếp.

---

## 9. P4.4j – Thử prompt số ít/số nhiều (21/10)

Giả thuyết xuất phát từ lỗi đã thấy: mỗi crop chứa một vật thì prompt số ít có thể hợp hơn số nhiều. **Đây là thí nghiệm sau khi đã xem dữ liệu dev**, không phải chứng cứ độc lập.

Script tạo và chạy:

```
evaluation/p4_prompt_number_20261021.py
results/countgdpp/p4_prompt_number_20261021/report.json
```

Model giữ nguyên `openai/clip-vit-base-patch32`, crop/bbox không đổi, chỉ thay `a photo of pens/rulers/pencils` bằng `a photo of a pen/ruler/pencil`.

**[LOG] `P4 PROMPT NUMBER PASS`**:

| Query | Plural Top-K | Singular Top-K | Plural AUC | Singular AUC |
|---|---:|---:|---:|---:|
| q03_1 | 1/6 | 0/6 | 0.1667 | 0.1429 |
| q03_2 | 6/6 | 6/6 | 1.0000 | 1.0000 |
| q03_3 | 4/6 | 2/6 | 0.7833 | 0.6000 |
| **Tổng** | **11/18** | **8/18** | — | — |

Các điểm cosine trung bình tăng khi đổi sang số ít cho cả đúng lẫn sai, nhưng **khả năng phân biệt không tăng**. Ví dụ q03_1 pen `0.2274→0.2409`, pencil `0.2357→0.2539`, ruler `0.2418→0.2586`. Với q03_2 ruler `0.2626→0.2913`, vẫn giữ Top-K 6/6; với q03_3 pencil `0.2274→0.2440`, ruler `0.2326→0.2631`.

**Quyết định:** bác bỏ giả thuyết “số ít tốt hơn” **trong ba ca đã thử**, không tiếp tục mò vô hạn cách viết trên cùng ảnh.

---

## 10. P4.4k – Fusion 50/50 cố định, cross-validation 5 ảnh (21/10)

Sau khi CLIP-only không hơn B2, assistant đề xuất ứng viên kết hợp **cố định trước lần chạy**:

`fusion_score = 0.5 * minmax_clamp(B2_score) + 0.5 * minmax_clamp(CLIP_cosine)`

Ở mỗi fold CV, min/max và threshold lấy từ **4 ảnh train/dev** của fold, không lấy min/max của ảnh test-fold. 50/50 là **một ứng viên** (không thử hoặc điều chỉnh nhiều tỷ trọng sau log này).

Script và output:

```
evaluation/p4_fixed_fusion_cv_20261021.py
results/countgdpp/p4_fixed_fusion_cv_20261021/report.json
```

**[LOG] `P4 FUSION CV PASS`**:

| Phương pháp | MAE ↓ | RMSE ↓ | Exact |
|---|---:|---:|---:|
| B2 gốc | 22.0000 | 30.0910 | 1/15 |
| **B2 threshold** | **4.6000** | **6.6182** | **1/15** |
| CLIP threshold | 6.8000 | 8.8468 | 0/15 |
| **Fusion B2+CLIP 50/50** | **5.8000** | **7.7932** | **0/15** |

Ngưỡng Fusion theo ảnh để đánh giá cross-validation:

| Ảnh gốc bị giữ ra | Threshold Fusion |
|---|---:|
| mcac_100 | 0.674430 |
| mcac_11 | 0.659461 |
| mcac_20 | 0.641531 |
| mcac_200 | 0.635343 |
| mcac_27 | 0.606663 |

**Diễn giải:** Fusion tốt hơn CLIP lọc riêng về MAE (5.8 < 6.8) nhưng **chưa vượt B2 chỉ dùng score gốc** (5.8 > 4.6). Kết quả chưa đủ để chọn Fusion theo sai số đếm.

---

## 11. P4.4l – Fusion giữ đúng vật nào? (21/10)

Assistant đề xuất đối chiếu object-level **chỉ trên bốn query có nhãn đang có** (`q03_1`,`q03_2`,`q03_3`,`q05_2`) với chính ngưỡng cross-validation theo ảnh tương ứng. Người dùng gửi log bảng per-query và FOUR-QUERY TOTAL. File lệnh được hướng dẫn lưu output:

```
results/countgdpp/p4_fusion_object_review_20261021.json
```

**[LOG] các bảng kết quả được gửi**:

| Query | Phương pháp | Bbox giữ | Vật đúng | Khung sai | Trùng | Bỏ sót |
|---|---|---:|---:|---:|---:|---:|
| q03_1 | B2 | 10 | 6 | 4 | 0 | 0 |
| q03_1 | CLIP | 1 | 0 | 1 | 0 | 6 |
| q03_1 | Fusion | 12 | 6 | 6 | 0 | 0 |
| q03_2 | B2 | 4 | 4 | 0 | 0 | 2 |
| q03_2 | CLIP | 5 | 5 | 0 | 0 | 1 |
| q03_2 | Fusion | 5 | 5 | 0 | 0 | 1 |
| q03_3 | B2 | 6 | 0 | 6 | 0 | 6 |
| q03_3 | CLIP | 1 | 0 | 1 | 0 | 6 |
| q03_3 | Fusion | 1 | 1 | 0 | 0 | 5 |
| q05_2 | B2 | 2 | 2 | 0 | 0 | 2 |
| q05_2 | CLIP | 13 | 4 | 8 | 1 | 0 |
| q05_2 | Fusion | 6 | 4 | 2 | 0 | 0 |

| Tổng 4 query (GT=22 vật) | B2 lọc | CLIP lọc | Fusion |
|---|---:|---:|---:|
| Khung giữ | 22 | 20 | 24 |
| **Vật đúng phân biệt** | **12** | **9** | **16** |
| Khung sai loại | 10 | 10 | 8 |
| Khung trùng | 0 | 1 | 0 |
| Vật mục tiêu bỏ sót | 10 | 13 | 6 |
| Tỷ lệ vật đúng giữ được (trên 22) | 54.55% | 40.91% | 72.73% |
| Tỷ lệ khung hữu ích (= vật đúng/khung giữ) | 54.55% | 45.00% | 66.67% |

**Điểm quan trọng:** trong **bốn query được chọn** Fusion giữ 16/22 vật, cao hơn B2 12/22, dù trên **15 query CV theo count** Fusion lại có MAE cao hơn B2 (5.8 vs 4.6). **Không chọn một bảng “đẹp hơn” để lờ bảng còn lại.** Hai nhóm metric đo hai điều khác nhau và dùng nhãn/độ bao phủ khác nhau.

**Giới hạn nặng:** 3/4 query thuộc cùng ảnh `mcac_200`; nhãn ba q03 từ assistant (đang chờ Triệu xác nhận), còn q05_2 từ manual review trước; thiếu object-level GT cho 11 query còn lại. Tỷ lệ ở trên **không phải** precision/recall hoặc mAP chuẩn trên holdout; không kết luận Fusion đã được xác nhận tổng quát tốt hơn.

---

## 12. P4.4m – Lưu báo cáo nghiên cứu thăm dò (21/10)

**[LOG] `P4 EXPLORATORY REPORT PASS`**: Minhtri đã chạy đoạn Python tổng hợp từ hai tệp `p4_fixed_fusion_cv_20261021/report.json` và `p4_fusion_object_review_20261021.json` để tạo:

```
reports/P4_CLIP_EXPLORATORY_FINDINGS_20261021.md
```

Sau đó Minhtri vô tình gõ trực tiếp đường dẫn `.md` ở shell, sinh lỗi `**Date:**: command not found` và `syntax error near unexpected token |`. Đây **không phải** lỗi tạo tệp hay lỗi kết quả; Markdown cần đọc bằng `cat`, `less`, `code` hoặc trình xem văn bản. Minhtri đã mở và dán nội dung báo cáo đầy đủ trong hội thoại; các bảng khớp log.

Báo cáo lưu kết quả thuận lợi (Fusion object-level selected cases) và âm tính (CLIP-only, singular prompt, Fusion count MAE) cùng hạn chế dev/holdout.

---

## 13. P4.5a – Bàn giao bảng nhãn cho Triệu

Assistant cung cấp chương trình đóng ZIP độc lập chỉ gồm:

- `README.md` hướng dẫn Triệu review.
- `q03_1/overview_numbered.jpg`, `crops_numbered.jpg`, `annotation_template.csv` (**13 bbox**).
- `q03_2/...` (**18 bbox**).
- `q03_3/...` (**16 bbox**).

Tổng **47 bbox**, ba template CSV trắng (không gửi bảng assistant đã gán để tránh ảnh hưởng người kiểm).

Đường dẫn dự kiến theo script:

```
results/countgdpp/p4_label_review_handoff_20261021.zip
```

Sau khi được cung cấp lệnh tạo ZIP, Minhtri trả lời **“xong r”**. Đây là xác nhận ngắn của người dùng rằng đã làm bước đó; hội thoại **không có stdout nguyên vẹn** `P4 INDEPENDENT REVIEW PACKAGE PASS`, cũng **chưa có** ba bảng đã được Triệu điền/trả và chưa có kết quả đối chiếu liên-annotator. Người nhận handoff hãy kiểm file ZIP tồn tại, mở được và là template trắng trước khi gửi/chấm.

**Cần tách riêng:** Triệu đã có review định tính tổng quan từ trước **không đồng nghĩa** đã xác nhận bảng nhãn từng rank của cả 47 bbox.

---

## 14. P4.5b – Khóa hai cấu hình ứng viên (21/10)

Để tránh tiếp tục thay ngưỡng/weight theo 5 ảnh dev đã xem nhiều lần, assistant đề xuất fit **một ngưỡng cố định trên toàn bộ 5 ảnh dev**, lưu thành artifact có hash nguồn.

**[LOG] `P4 CANDIDATE FREEZE PASS`**:

```
Development: 5 images, 15 queries, 481 boxes
B2 threshold:      0.906739
B2 Dev-fit MAE:    4.3333
Fusion threshold:  0.655183
Fusion Dev-fit MAE: 4.4000
Saved: results/countgdpp/p4_candidate_freeze_20261021.json
```

Quy tắc:

- Ứng viên **B2-score filter**: giữ B2 bbox có `b2_score >= 0.906739` (giá trị hiển thị đã làm tròn; khi chạy thật phải đọc **đủ precision** từ JSON freeze).
- Ứng viên **Fusion 50/50**: score bằng nửa điểm B2 min–max cộng nửa cosine CLIP min–max; min/max `bounds_from_development_only` được lấy **toàn bộ 5 ảnh dev**, `clamp[0,1]`; giữ khi score ≥ ngưỡng Fusion đầy đủ precision từ JSON.
- Các ngưỡng fit trên 15 query dev bằng quy tắc tối thiểu **MAE → RMSE → ngưỡng**.
- Tệp freeze lưu danh sách ảnh/query dev, normalization bounds, CLIP model, 16 checksum SHA-256 (15 file điểm + per_query.csv), limitations.

**Tuyệt đối không nhầm:** `Dev-fit MAE 4.3333/4.4` là **training-fit trên chính dữ liệu chọn threshold**, không được tuyên bố tốt hơn CV 4.6/5.8 hay là điểm holdout.

---

## 15. P4.5c – Audit tái lập freeze (21/10)

Assistant hướng dẫn kiểm hash input, đọc ngưỡng/bounds cố định, tái tạo dự đoán trên 15 query dev và đối chiếu MAE/RMSE với freeze.

**[LOG người dùng gửi nguyên kết quả]**:

```
Source checksum verification: PASS
Frozen normalization verification: PASS

P4 FROZEN CONFIGURATION AUDIT
Development: 5 images, 15 queries, 481 boxes
Method    Threshold   Dev-fit MAE   Dev-fit RMSE
B2        0.906739    4.3333        6.5269
Fusion    0.655183    4.4000        6.4704

Saved: results/countgdpp/p4_freeze_audit_20261021.json
P4 FREEZE AUDIT PASS
```

**Điều được xác nhận:** trên máy Minhtri, tại lần audit, 16 input có hash khớp freeze; min/max chuẩn hóa tái lập; metric khớp freeze. **Không có bằng chứng** đã kiểm hash checkpoint model CLIP/CountGD++ hoặc đã viết và chạy một pipeline inference mới dựa trên freeze; audit chỉ kiểm kết quả từ **điểm đã lưu**.

---

## 16. P4.6 — mới là kế hoạch, chưa thực hiện

Assistant từng đề xuất:

- **P4.6a:** kiểm kê dữ liệu ảnh ngoài 5 ảnh dev, kiểm tính độc lập; đã cung cấp lệnh **nhưng chưa có log chạy**.
- **P4.6b:** chuẩn bị pipeline suy luận khớp quy trình B2 + CLIP, không đọc GT khi dự đoán; **chưa có artifact chứng minh hoàn tất**.
- **P4.6c:** chạy hai phương pháp với ngưỡng freeze trên dữ liệu chưa dùng thiết kế; **chưa chạy**.
- **P4.6d:** đánh giá count và object-level trên dữ liệu mới; **chưa chạy**.

Ngày 22/10, Minhtri đặt câu hỏi vì kế hoạch mở rộng quá dài. Assistant đã **phân biệt rõ mục tiêu**:

- Để **đóng nhiệm vụ trong `PILOT_SUMMARY.md`**, không cần P4.6; cần Triệu kiểm chéo evaluator + nhóm duyệt + đồng bộ tài liệu.
- Để **kiểm chứng nhánh cải tiến CLIP/Fusion**, P4.6 (hoặc đánh giá độc lập tương đương) là giai đoạn hợp lý nhưng phải xác định dữ liệu truly unseen và không chỉnh ngưỡng theo kết quả test.
- Để **hoàn thành toàn bộ đề tài CS331**, còn phụ thuộc mục tiêu được giảng viên/nhóm yêu cầu: chốt câu hỏi khoa học, kiểm chứng, báo cáo, khả năng cần phương pháp tốt hơn baseline. **Không tự thêm P5/P6** hay hứa “P4.6 xong là chắc chắn xong đề tài”.

---

## 17. Bảng nghiệm thu đúng phạm vi và những việc CHƯA hoàn thành

### 17.1. Đóng pilot P2/P3 — những điều còn thiếu

1. **[CHỜ] Triệu kiểm chéo evaluator ngày 20/10**: code `evaluation/evaluate_pilot.py`, join ID/schema, count/error/null, vài dòng per-query, nhãn q05_2, kết luận và ngày. Review thị giác ngày 19/10 **không thay thế**.
2. **[CHỜ] Nhóm duyệt `reports/PILOT_SUMMARY.md`**: mục 7 ghi đúng người duyệt/ngày, quyết định đóng pilot hoặc yêu cầu sửa.
3. **[CHƯA CÓ BẰNG CHỨNG]** cập nhật `WORKLOG.md`, `roadmap/ROADMAP.md` và `HANDOFF/HANDOFF.md` để chốt trạng thái.
4. **[NÊN ĐỒNG BỘ]** mục 6 cũ của `PILOT_SUMMARY.md` đang nói CLIP chưa chạy; cần dẫn sang báo cáo P4 như sự kiện **sau pilot**, không biến CLIP thành điều kiện mới của pilot.

### 17.2. Đánh giá giá trị nhánh P4 — những điều còn thiếu

1. **[CHỜ]** Triệu trả 3 CSV gán nhãn 47 bbox; so bất đồng từng rank, ghi phân xử, tính lại object-level nếu cần.
2. **[CHỜ]** Kiểm tra nguồn ảnh/nhãn mới đủ độc lập nếu nhóm muốn claim cải tiến ngoài tập dev. Ba q03 cùng ảnh không là ba phép kiểm độc lập.
3. **[CHƯA]** Chạy suy luận mới với code bảo đảm tái lập crop/preprocess, version model, frozen bounds/threshold **không cập nhật từ ảnh test**.
4. **[CHƯA]** Báo cáo holdout về MAE/RMSE và object-level; nếu dữ liệu chỉ có count GT, **không tự bịa object-level GT**.
5. **[CHƯA CÓ XÁC NHẬN]** nhóm chọn CLIP/Fusion làm phương pháp cuối hoặc đóng góp chính của đề tài. Nên giữ cả kết quả âm tính.

### 17.3. Không nhầm những chỉ số sau

| Số | Ý nghĩa chính xác |
|---|---|
| B0 MAE **19.4** và B2 MAE **22.0** | Pilot gốc từ các prediction B0/B2, 15 query |
| B2-threshold MAE **4.6**, CLIP-threshold MAE **6.8**, Fusion MAE **5.8** | 5-fold leave-one-**original**-image-out trên **cùng dev 5 ảnh**, không phải holdout độc lập |
| B2-threshold **12/22**, Fusion **16/22** | Giữ đúng vật trên **4 query được chọn**, 3 query cùng ảnh, nhãn q03 sơ bộ |
| B2 threshold **0.906739**, Fusion threshold **0.655183** | Cấu hình cố định fit từ **toàn bộ 5 ảnh dev** để kiểm trên ảnh mới (chỉ sử dụng full precision JSON) |
| Dev-fit MAE **4.3333** / **4.4000** | Fit trên cùng dev dùng chọn ngưỡng; **không phải CV** |
| `P4 FREEZE AUDIT PASS` | Tái lập hash và metric trên artifacts dev; **không chứng minh generalization** |
| Top-K lấy **GT K** | Dùng để **chẩn đoán khả năng ranking**, không phải thuật toán dự đoán count khi chưa biết nhãn |

---

## 18. Danh mục file/artifact theo từng mốc

> Các đường dẫn dưới đây là **đường dẫn tương đối bên trong dự án CS331 theo file, lệnh và log trong hội thoại**. Handoff này được tạo bên ngoài máy WSL người dùng: **không phải tất cả tệp đã được assistant mở trực tiếp ở thời điểm đóng gói**. Hãy kiểm tra tồn tại/version trong workspace nếu cần dùng lại.

### 18.1. Nguồn pilot và hướng dẫn

```text
PHAN_2_DANH_GIA.md              # tài liệu hướng dẫn P2 (vị trí trong repo cần kiểm)
PHAN_3_TONG_KET.md               # hướng dẫn P3 (vị trí trong repo cần kiểm)
evaluation/evaluate_pilot.py
experiments/countgdpp/m4_inputs/manifest.csv
experiments/countgdpp/m4_inputs/first5_inputs.jsonl
results/countgdpp/m4_first5_b0/
results/countgdpp/b2_two_images_20261015/
results/countgdpp/b2_remaining3_20261015/
results/countgdpp/b2_remaining3_20261015/q05_2/manual_crosscheck_20261016.json
results/countgdpp/pilot_eval_20261020/
reports/PILOT_SUMMARY.md
reports/BENCHMARK_FSCD147.md
workspace Trí and Triệu/Triệu/TRIEU_VISUAL_REVIEW.md
WORKLOG.md
roadmap/ROADMAP.md
HANDOFF/HANDOFF.md
```

Lưu ý `PHAN_2_DANH_GIA.md`, `PHAN_3_TONG_KET.md` có trong tài liệu người dùng cung cấp; đường dẫn **đúng trong repo** có thể là dưới `roadmap/` hoặc vị trí khác. Không tự suy ra từ tên file trong Library.

### 18.2. P4 điểm CLIP và CV

```text
results/countgdpp/p4_clip_probe_20261020/
results/countgdpp/p4_clip_all15_20261020/
evaluation/p4_compare_count_cv_20261020.py
results/countgdpp/p4_count_cv_20261020/report.json
results/countgdpp/p4_count_cv_20261020/per_query.csv
results/countgdpp/p4_two_case_object_review_20261020.json
```

### 18.3. Review bbox có đánh số

```text
results/countgdpp/p4_review_q03_1_20261020/
  overview_numbered.jpg
  crops_numbered.jpg
  annotation_template.csv
  q03_1_annotation_review_assistant_20261021.csv
results/countgdpp/p4_review_q03_2_20261020/
  overview_numbered.jpg
  crops_numbered.jpg
  annotation_template.csv
  q03_2_annotation_review_assistant_20261020.csv
results/countgdpp/p4_review_q03_3_20261020/
  overview_numbered.jpg
  crops_numbered.jpg
  annotation_template.csv
  q03_3_annotation_review_assistant_20261020.csv
results/countgdpp/p4_label_review_handoff_20261021.zip  # user nói 'xong r'; cần kiểm trực tiếp
```

### 18.4. Chẩn đoán ranking, prompt, Fusion

```text
results/countgdpp/p4_rank_diagnostic_20261021.json
results/countgdpp/p4_class_score_analysis_20261021.json
evaluation/p4_prompt_number_20261021.py
results/countgdpp/p4_prompt_number_20261021/report.json
evaluation/p4_fixed_fusion_cv_20261021.py
results/countgdpp/p4_fixed_fusion_cv_20261021/report.json
results/countgdpp/p4_fusion_object_review_20261021.json
reports/P4_CLIP_EXPLORATORY_FINDINGS_20261021.md
```

### 18.5. Cấu hình đóng băng và audit

```text
results/countgdpp/p4_candidate_freeze_20261021.json
results/countgdpp/p4_freeze_audit_20261021.json
```

**Chưa có:** tệp hoặc số liệu `P4.6a–d` thành công, CSV kết quả Triệu gán nhãn độc lập, independent holdout benchmark cho CLIP/Fusion; không được tự tạo chỉ vì kế hoạch đã có tên bước.

---

## 19. Những bài học kỹ thuật / vì sao phương án thay đổi

1. **Pilot B2 chưa đạt:** B2 MAE 22 > B0 MAE 19.4; điều này tạo nhu cầu chẩn đoán lỗi sai loại thay vì chỉ thêm tầng mẫu tự chọn.
2. **Chọn CLIP làm phép thử nhỏ:** lọc crop–text có thể bổ sung tín hiệu semantic mà không phải chạy lại detector. **Giả thuyết**, không phải đã chứng minh.
3. **CLIP-only cho MAE kém hơn B2-score threshold:** 6.8 > 4.6 trong CV dev → không dùng CLIP đơn độc làm mặc định.
4. **Count đúng có thể giữ toàn vật sai:** `q03_3` B2 đúng 6 nhưng 0/6 bút chì được giữ → yêu cầu đánh giá object-level, không chỉ MAE.
5. **AUC và oracle Top-K làm rõ lỗi:** CLIP `q03_3` ranking khả quan hơn B2 nhưng threshold lọc không giữ bút chì; `q03_1` CLIP ranking tệ thật; q05_2 AUC cao nhưng trùng vật vẫn phá counting.
6. **Prompt singular/plural không chữa lỗi:** số ít làm Top-K giảm ở q03_1/q03_3; không tiếp tục mò prompt trên cùng dev.
7. **Fusion là phương án bổ sung, không phải chiến thắng:** count CV 5.8 thua B2 4.6, nhưng 4 query được chọn giữ đúng 16/22 vs 12/22; hai metric trái hướng → giữ làm ứng viên cần kiểm chứng, **không chọn vội**.
8. **Khóa cấu hình trước khi test:** dừng đổi trọng số/ngưỡng liên tục trên dev, lưu hash và minmax vào JSON; đã audit tái lập.
9. **Tách task pilot và đề tài:** pilot có thể đóng khi evaluator được kiểm chéo và báo cáo được duyệt; P4.6 dành cho kiểm tra generalization của ứng viên, không được thêm thành tiêu chí mới cho task pilot.

---

## 20. Hướng dẫn người tiếp nhận: cần làm gì, theo thứ tự nào?

### Nhánh A — muốn đóng ngay `PILOT_SUMMARY.md`

1. Đọc `reports/PILOT_SUMMARY.md`, `PHAN_2_DANH_GIA.md`, `PHAN_3_TONG_KET.md` và `results/countgdpp/pilot_eval_20261020/{metrics,per_query,manual_check,run_config}.json`.
2. Triệu kiểm chéo evaluator P2 (không chỉ nhìn ảnh), ghi tên/ngày/những dòng/công thức đã kiểm, các bất đồng và kết luận.
3. Đề nghị nhóm duyệt Pilot; nếu đạt, mới cập nhật mục 7 thành `ĐÃ CHỐT PILOT` với bằng chứng.
4. Ở mục 6, ghi cập nhật **sau ngày 20/10**: P4 CLIP/Fusion đã chạy exploratory; chỉ liên kết báo cáo `P4_CLIP_EXPLORATORY_FINDINGS_20261021.md`, không viết lại lịch sử như thể pilot lúc đầu đã có CLIP.
5. Đồng bộ `WORKLOG.md`, `roadmap/ROADMAP.md`, `HANDOFF/HANDOFF.md`; chưa tự nhận đã commit/push.

### Nhánh B — muốn tiếp tục nghiên cứu P4 một cách khoa học

1. Kiểm tra ZIP 47 bbox đã tạo và yêu cầu Triệu gán nhãn **độc lập**; làm bảng đối chiếu bất đồng rank→lớp→object_id, chỉ sau đó sửa object-level result nếu cần.
2. Xác nhận có **ảnh/GT ngoài năm ảnh dev thực sự chưa dùng**. Không giả định “còn file ảnh khác” là lập tức có holdout độc lập nếu trước đây đã dùng để thiết kế.
3. Chỉ khi có dữ liệu hợp lệ, xây pipeline inference khớp CLIP crop/processor/checkpoint gốc; dùng **giá trị full precision** và bounds từ freeze JSON, không tính minmax từ ảnh test và không tối ưu lại sau xem đáp án.
4. Lưu predictions trước khi đọc GT. Sau đó đánh giá count MAE/RMSE, exact_count; với bbox GT/nhãn object đáng tin mới đánh giá giữ đúng/sai/trùng theo quy tắc cố định.
5. Báo cáo cả kết quả tiêu cực. Nếu không có độc lập holdout hoặc nhãn object đủ tốt thì **chỉ kết luận exploratory dev**.

**Không chủ động mở P5/P6, không kết luận phải huấn luyện mô hình mới, không khẳng định CLIP/Fusion đã cải tiến thành công trước khi có chứng cứ.**

---

## 21. Mẫu câu bàn giao ngắn có thể gửi cho người khác

> Tôi đã hoàn thành phần chạy evaluator pilot CountGD++ B0/B2 trên 5 ảnh/15 query và cập nhật `PILOT_SUMMARY.md`. B0 MAE=19.4, B2 MAE=22.0; báo cáo pilot còn chờ Triệu kiểm chéo evaluator và nhóm duyệt. Sau đó tôi thử CLIP trên 481 bbox B2, đánh giá CV theo ảnh gốc: B2-score threshold MAE=4.6; CLIP-only MAE=6.8; Fusion 50/50 MAE=5.8. Với 4 query được chọn và nhãn object sơ bộ, Fusion giữ 16/22 vật đúng so với B2 threshold 12/22; 3 query có cùng ảnh và nhãn cần Triệu xác nhận. Tôi đã đóng băng B2 threshold khoảng 0.906739 và Fusion khoảng 0.655183, audit SHA-256/metrics PASS. Chưa chạy P4.6 hay có kết quả holdout độc lập. Hai mục tiêu tiếp theo là đóng duyệt pilot theo phạm vi gốc và, nếu tiếp tục nghiên cứu, kiểm nhãn độc lập rồi thử cấu hình đã khóa trên dữ liệu mới.

---

## 22. Nguồn dùng để biên soạn handoff này và giới hạn truy xuất

**Đã có nội dung để đối chiếu trong hội thoại / nguồn người dùng:**

1. `PILOT_SUMMARY.md` bản nháp sau P2, bao gồm mục 1–7, số liệu B0/B2, review định tính và trạng thái duyệt.
2. `PHAN_2_DANH_GIA.md` hướng dẫn cách chạy evaluator, schema, tiêu chí PASS.
3. `PHAN_3_TONG_KET.md` hướng dẫn điều kiện đóng báo cáo pilot.
4. `HANDOFF_CS331_P2_P3_2026-10-20.md` ghi chính xác bằng chứng đã có vào ngày 20/10, trước các thử nghiệm CLIP.
5. Các bảng và log kết quả Minhtri gửi trực tiếp cho assistant trong cuộc hội thoại: `P4 COUNT CV`, `Q03_1/Q03_3 LABEL CHECK`, `RANK DIAGNOSTIC`, `CLASS SCORE ANALYSIS`, `PROMPT NUMBER`, `FUSION CV`, `FOUR-QUERY TOTAL`, `EXPLORATORY REPORT PASS`, `CANDIDATE FREEZE`, `FREEZE AUDIT`.
6. Hai ảnh đánh số từng khung `q03_1`, `q03_3`, cùng review `TRIEU_VISUAL_REVIEW.md` được người dùng trích trong hội thoại; nhãn assistant chưa thay thế xác nhận Triệu.

**Chưa được xác minh tại lượt biên soạn này:** mở trực tiếp mọi JSON/script trong thư mục WSL của Minhtri; hash model weights; trạng thái git/commit/push; bản Triệu đã điền sau khi nhận ZIP; thí nghiệm P4.6. **Đường dẫn và PASS từ log người dùng là bằng chứng lời khai/kết quả đầu ra, không phải kiểm toán độc lập chạy lại trên máy.**

**Kết luận cuối handoff:** Ta đã có một lịch sử thực nghiệm pilot→P4 chi tiết, bảo toàn cả thất bại và các quyết định chuyển hướng. **Điểm dừng đã được chứng minh là P4.5c `P4 FREEZE AUDIT PASS`; P4.6 mới là kế hoạch.** Pilot gốc chưa được ghi hoàn tất ở cấp nhóm vì thiếu xác nhận kiểm chéo và phê duyệt.
