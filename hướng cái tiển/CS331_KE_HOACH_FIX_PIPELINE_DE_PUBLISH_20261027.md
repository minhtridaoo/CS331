# CS331 / CountGD++ — BẢN SỬA THUẬT TOÁN CỤ THỂ ĐỂ HƯỚNG TỚI PAPER HỘI NGHỊ

> **Bản thay thế phần định hướng quá chung của tài liệu trước** · 27/10/2026  
> **Nhóm:** Trí – Triệu · **Mốc báo cáo môn học:** 02/12/2026  
> **Phạm vi:** sửa chính hệ thống B0 → B2 → Fusion đang có; không xây dự án mới, không huấn luyện lại CountGD++ ở nhánh đầu.  
> **Trạng thái:** đề xuất cách sửa và giao thức thí nghiệm, **chưa được thực thi hoặc chứng minh**. Quyết định công bố phụ thuộc kết quả kiểm chứng và mức phù hợp của hội nghị.

## 0. Trả lời thẳng: cần sửa cái gì?

**KHÔNG nên dừng ở “CountGD++ + CLIP 50/50 giảm MAE”.** Đây là một cách kết hợp khá trực tiếp; nghiên cứu trước đã có bước phát hiện rồi xác minh và dùng CLIP phân loại vùng ảnh. Kết quả của nhóm còn một nhược điểm lớn: **lọc được nhiều vật sai, nhưng cũng bỏ mất nhiều vật đúng**.

**Phương án chính nên kiểm tra:** *Xác minh ngữ nghĩa của khung mẫu tự chọn trước khi đưa vào lượt đếm thứ hai của CountGD++*, sau đó dùng lại Fusion hiện tại làm đối chứng. Mục tiêu là **chặn mẫu sai gây lan truyền lỗi nhưng vẫn giữ được vật đúng**.

Tuy nhiên, đây chỉ là lựa chọn có điều kiện:

- **Nếu hậu kiểm N4 chứng minh khung mẫu tự chọn sai loại thường kéo theo B2 nhận diện sai**, ưu tiên sửa **GIỮA lượt 1 và lượt 2** (nhánh P: *verified pseudo-exemplar*).
- **Nếu khung mẫu đúng mà phần lớn vật đúng bị mất ở chính bộ lọc Fusion**, ưu tiên sửa **SAU lượt 2** (nhánh R: *recall-preserving filtering*).
- Không phát triển đồng thời cả hai ngay lập tức. Chốt nhánh chính bằng bằng chứng lỗi, không quyết định chỉ dựa vào cảm giác.

**Thông điệp nghiên cứu cần chứng minh:** “Một cơ chế kiểm chứng phù hợp với cấu trúc hai lượt của CountGD++ có thể loại sai loại **mà không phải hy sinh quá nhiều vật đúng**, so với bộ lọc cuối cố định.” Đây là **giả thuyết**, chưa phải phát hiện đã công bố.

---

## 1. Nhóm đã có gì? Cái gì phải giữ nguyên?

### 1.1. Nền tảng đang hoạt động

1. **B0:** đưa ảnh + câu hỏi văn bản vào CountGD++ và lấy khung/số lượng sau **một lượt**.
2. **B2:** lượt 1 lấy các khung ứng viên, chọn **tối đa 3 pseudo-exemplar** bằng điểm của CountGD++ (`tau_sample=0.23`), rồi chạy lượt 2 với ảnh + văn bản + mẫu tự chọn.
3. **Lọc điểm:** chỉ giữ các khung có điểm CountGD++ qua ngưỡng; đã có thử nghiệm.
4. **Fusion 50/50:** ghép tín hiệu CountGD++ và CLIP (`a photo of {X}`) để lọc các khung cuối. **CLIP không đếm**, chỉ cho điểm phù hợp vùng ảnh–văn bản.
5. **Benchmark FSCD-147:** 1.190 ảnh, MAE khoảng **8,34** với cấu hình mô hình nguồn đầy đủ hơn. Đây là kiểm tái lập, **không phải kết quả cải tiến**; không đem so trực tiếp với MUCCA.

### 1.2. Kết quả hiện có cần ghi trung thực

Theo bản demo nhóm cung cấp ngày 27/10 trên **10 ảnh MUCCA mới / 30 truy vấn**:

| Cách | MAE có mặt (20 truy vấn) | Đếm TB ở truy vấn vắng mặt (10 truy vấn) | MAE chung | Khung sai theo phép tự động |
|---|---:|---:|---:|---:|
| B0 | **5,70** | 8,9 | 6,77 | 106 |
| B2 | 12,95 | 13,1 | 13,00 | 238 |
| Lọc điểm sau B2 | 8,75 | 4,3 | 7,27 | 92 |
| Fusion sau B2 | 7,80 | **1,0** | **5,53** | **31** |

**Nghiêm túc về bằng chứng:** đây là số **nhóm cung cấp**, chưa tự xác minh từ toàn bộ tệp chạy P4.6 trong lần biên soạn này. Hai tệp `reports/P4_6_UNSEEN_RESULTS_20261027.md` và gói `p4_n4_review_package_20261027` **chưa tìm thấy ở nhánh `main`** tại lần đối chiếu; có thể nằm nhánh khác/máy khác. Đồng bộ chúng trước khi viết con số vào bản nộp cuối.

Diễn giải đúng:

- Fusion giảm MAE so với B2 và phương pháp chỉ lọc điểm trong **thử nghiệm nhỏ hiện tại**.
- **B0 vẫn tốt hơn Fusion ở trường hợp vật có mặt** (5,70 < 7,80).
- Nhóm báo mất khoảng 50% vật đúng; con số cần xác nhận cách tính bằng đối chiếu vật thể/khung và hậu kiểm.
- “31 khung sai” là **phép đánh dấu tự động dựa trên nhãn điểm**, chưa tương đương 31 khung được người xác nhận.
- Những ca `people` đếm chó, `sheep` đếm chó và `bicycles` đếm xe máy cho thấy vấn đề chưa giải quyết hoàn toàn.

### 1.3. Các tệp/điểm mã nguồn đã kiểm để định vị vị trí sửa

| Tệp trong `minhtridaoo/CS331` | Có gì | Ý nghĩa thay đổi |
|---|---|---|
| `experiments/countgdpp/run_b2_pilot.py` | Hàm **`select_pseudo(...)`**: lọc ứng viên bằng điểm, chọn tối đa 3 khung; có dữ liệu `cap0` của lượt 1 | **ĐIỂM CHÍNH để thử nhánh P**. Tạo tệp chạy mới, không ghi đè bản B2 gốc. |
| `experiments/countgdpp/run_b0_batch.py` | Đọc đầu vào, xác minh nguồn và xuất kết quả B0 | Giữ nguyên làm đối chứng. |
| `results/countgdpp/p4_clip_all15_20261020/run_config.json` | CLIP `openai/clip-vit-base-patch32`, revision `3d74acf9a28c67741b2f4f2ea7635f0aaf6f0268`, mẫu câu `a photo of {prompt}` | Khóa cùng mô hình/cách cắt ảnh khi so sánh với P4 cũ. |
| `results/countgdpp/p4_clip_all15_20261020/*_clip_scores.json` | Điểm CLIP và điểm B2 theo từng khung | Đối chứng lọc cuối, không thay đổi nguồn dự đoán B2. |
| `evaluation/evaluate_pilot.py` | Tính MAE/RMSE, coverage, kiểm nhãn; **đang giới hạn `split=dev`** | Không dùng nguyên trạng để đánh giá test độc lập nếu chưa thiết kế phép đánh giá mới; nên tạo evaluator nghiên cứu riêng. |
| `reports/PILOT_SUMMARY.md` | Các mẫu lỗi B0/B2 và đánh giá thủ công | Nguồn để kiểm giả thuyết, **không phải bộ test mới**. |

**Quy tắc mã nguồn:** thêm phiên bản thử nghiệm trong `experiments/countgdpp/`, giữ nguyên mã B0/B2 để có đối chứng. Mọi thay đổi ghi lại commit, cấu hình, đầu vào và kết quả; không chỉnh tệp nguồn để chạy lại rồi gọi là “B2 gốc”.

---

## 2. GIAI ĐOẠN F0 — Bắt lỗi đúng trước khi sửa (bắt buộc)

### F0.1. Hoàn thiện N4, không chỉ nhìn MAE

Với **7 truy vấn ưu tiên + 2 truy vấn đối chiếu** nhóm đã đề xuất, đặc biệt các ca `people` và truy vấn vắng mặt:

- Cho từng khung của B2, lọc điểm, Fusion: phân loại **vật đúng / vật sai loại / khung trùng / một phần vật / nền / chưa chắc**.
- Gán `object_id` cho các khung cùng một vật; ghi vật thật nào **không được khung nào giữ lại**.
- Với từng khung bị Fusion loại, trả lời: **loại đúng khung sai** hay **loại nhầm khung đúng**?
- Kiểm xem các mẫu tự chọn ở giữa hai lượt có đúng loại, đúng **một** vật không; đừng chỉ nhìn số cuối.
- Nếu đánh giá vị trí bằng điểm nhãn thật trong khung, ghi đó là **xấp xỉ**, không gọi là chuẩn phát hiện vị trí.

**Đầu ra:** `n4_review.csv`, `n4_error_summary.md`, ít nhất 3 hình trước/sau đúng/sai, có người kiểm và ngày. N4 chọn lọc là **phân tích lỗi**, không tự đại diện cho tất cả ảnh.

### F0.2. Phân chia nguyên nhân thất bại thành 4 nhóm

| Mã lỗi | Dấu hiệu | Vị trí cần sửa |
|---|---|---|
| E1 — Mẫu tự chọn sai | Stage 1 chọn chó để đếm `people` | **Giữa lượt 1–2**, thử nhánh P |
| E2 — Mẫu đúng nhưng lượt 2 vẫn sai | Có mẫu đúng, B2 sinh nhiều khung sai/trùng/phần vật | Kiểm lượt 2 và chiến lược giữ/loại khung |
| E3 — Khung đúng có sẵn nhưng bị Fusion loại | Điểm CLIP thấp khiến vật thật biến mất | **Sau lượt 2**, thử nhánh R |
| E4 — Không có ứng viên đúng ngay từ đầu | Cả B0/B2 không khoanh đúng | Lọc sau B2 không thể phục hồi; cần sinh ứng viên tốt hơn / phạm vi đóng góp khác |

**Điểm dừng quyết định:** nếu E1 không phổ biến hoặc không liên quan tới tăng lỗi, **không cố trình bày “sửa pseudo” là giải pháp chính**. Chuyển sang nhánh R và báo lại lý do.

---

## 3. NHÁNH P — Thuật toán cụ thể để thử trước, nếu E1 chiếm ưu thế

### 3.1. Ý tưởng mới nằm ở đâu trong chương trình?

Hiện trạng:

```
Ảnh + loại vật X
    → CountGD++ lượt 1 → tất cả khung ứng viên
    → chọn tối đa 3 khung có điểm CountGD++ cao nhất (> 0,23)
    → đưa 3 khung vào CountGD++ lượt 2
    → các khung cuối → Fusion 50/50 → số đếm
```

Phiên bản thử nghiệm:

```
Ảnh + loại vật X
    → CountGD++ lượt 1 → các khung ứng viên
    → CLIP kiểm từng ỨNG VIÊN MẪU với câu hỏi X
    → CHỌN LẠI tối đa 3 mẫu có bằng chứng phù hợp hơn
    → CountGD++ lượt 2 với mẫu đã kiểm
    → giữ nguyên bước Fusion cuối / so sánh có và không có bước này
    → số đếm + nhật ký tại sao giữ/bỏ từng mẫu
```

**Điểm khác so với Fusion hiện có:** can thiệp **trước khi khung mẫu sai làm sai lượt đếm thứ hai**, không chỉ sửa số đếm sau cùng. Đây là khác biệt về vị trí và cơ chế; **chưa được gọi là tính mới được chứng minh** cho tới khi so với nghiên cứu liên quan và thử nghiệm đủ mạnh.

### 3.2. Định nghĩa phiên bản đầu (P1), không thêm quá nhiều tham số

- **Đầu vào duy nhất của mô hình:** ảnh `I` và câu hỏi `q`. Không đưa nhãn thật, tên vật đang có trong ảnh, hoặc danh sách loại gây nhiễu rút từ tập test.
- **Ứng viên:** dùng lại khung từ **lượt 1**; lấy tối đa `M` ứng viên điểm cao nhất thỏa `score_CountGD > 0.23`. `M=10` là **đề xuất khởi tạo**, có thể chọn lại trên tập phát triển. **Không thay ngưỡng sinh ứng viên trong thử nghiệm đầu**, để tách tác động của riêng bước kiểm mẫu.
- **CLIP:** dùng đúng mô hình và khuôn câu đã khóa (`a photo of {q}`), cắt các khung ứng viên về đúng tọa độ ảnh gốc, giữ cùng quy tắc làm tròn/đệm khi đối chứng.
- **Chọn mẫu:** trong tối đa `M` ứng viên, giữ các khung có `clip_similarity >= tau_pseudo` rồi lấy tối đa 3 khung theo `score_CountGD` giảm dần. `tau_pseudo` **chỉ chọn trên dev**, không lấy thẳng ngưỡng lọc cuối vì ý nghĩa điểm/đầu vào đã khác.
- **Không đủ 3 mẫu:** dùng 1 hoặc 2 mẫu hợp lệ; ghi chính xác số lượng.
- **Không có mẫu qua kiểm:** giữ nguyên quy ước B2 adapter là dùng B0 nếu không chạy lượt 2; vẫn có thể áp **cùng bộ lọc cuối cố định** ở các phương pháp so sánh liên quan. Không lấy việc “không thấy mẫu” làm bằng chứng chắc chắn đối tượng vắng mặt.
- **Không sửa mô hình gốc/không huấn luyện:** đây là bước chọn đầu vào cho lượt 2.

### 3.3. Mã giả thuật toán P1 (để lập trình, chưa phải mã chạy hoàn chỉnh)

```python
# stage1 gồm proposals / scores / token IDs từ run_b2_pilot.py
candidates = top_m_target_proposals(stage1, threshold=0.23, m=M)
# Tọa độ crop phải quy về ảnh gốc, cùng quy tắc ảnh với bản CLIP hiện tại.
verified = []
for item in candidates:
    crop = crop_original_image(image, item.xyxy)
    sim = clip_similarity(crop, f"a photo of {query}")
    log_candidate(item, sim)
    if sim >= tau_pseudo:  # được chọn CHỈ trên dev
        verified.append((item, sim))

pseudo = top_k(verified, key="countgd_score", k=3)
if pseudo:
    stage2 = countgd_forward(image, query, pseudo_boxes=pseudo)
else:
    stage2 = original_b0_result

# P1a: không lọc cuối; P1b: cùng Fusion cuối đã khóa như đối chứng.
output_p1a = stage2
output_p1b = frozen_fusion(stage2, image, query)
```

**Quan trọng:** mã giả chỉ mô tả logic. Hàm đọc mẫu của `run_b2_pilot.py` có thêm xử lý token/định dạng khung và kiểm mã nguồn; phải giữ các quy tắc đó khi cài đặt. Không được coi việc thay ít dòng mã là một thực nghiệm hợp lệ nếu B2 gốc không còn tái lập giống kết quả cũ.

### 3.4. File nên tạo (không phá pipeline cũ)

```text
experiments/countgdpp/
  run_b2_pilot.py                   # GIỮ NGUYÊN
  run_b2_verified_pseudo.py         # MỚI: lấy Stage 1, kiểm CLIP rồi chọn pseudo
  pseudo_clip_verifier.py           # MỚI: crop, CLIP, chọn và ghi lý do
  configs/
    p1_dev_config.json              # MỚI: M, tau_pseudo, clip revision, crop

evaluation/
  evaluate_pilot.py                 # GIỮ NGUYÊN
  evaluate_research.py              # MỚI: hỗ trợ dev/test hợp lệ, tách present/absent

results/countgdpp/
  p1_dev_<run_id>/                  # MỚI: stage1, pseudo cũ/mới, final, score, log
  p1_test_<run_id>/                 # CHỈ TẠO SAU KHI ĐÃ KHÓA THAM SỐ
```

**Nhật ký bắt buộc theo query:** `image_id`, `query_id`, `stage1_proposals`, `pseudo_before`, `pseudo_after`, điểm CountGD, điểm CLIP, quyết định giữ/bỏ và lý do, `stage2_executed`, `B0_count`, `B2_count`, `new_count`, danh sách khung và thời gian. Ảnh nhãn thật **không bao giờ** nằm trong đầu vào cho hàm chọn mẫu.

### 3.5. Đối chứng để biết “sửa mẫu” thật sự có ích

| Ký hiệu | Phương án | Phải có? |
|---|---|---|
| B0 | CountGD++ một lượt | Có |
| B2 | CountGD++ hai lượt, chọn pseudo gốc | Có |
| F | B2 + Fusion 50/50 cố định hiện tại | Có |
| P | B2 + **pseudo được CLIP kiểm**; không lọc cuối | Có |
| P+F | B2 + kiểm pseudo + **cùng Fusion cuối như F** | Có |
| B0+F | B0 + cùng cách lọc Fusion ở đầu ra B0 | Nên có — vì B0 vốn tốt hơn trên truy vấn có mặt |
| S-only | B2 + lọc điểm CountGD++ | Có, là đối chứng không cần CLIP |

**Nếu chỉ P+F tốt hơn B2 mà không tốt hơn F**, chưa chứng minh kiểm pseudo đóng góp thêm. Nếu P+F tốt hơn F **nhưng vẫn thua B0 ở truy vấn có mặt**, phải tiếp tục giải quyết sự đánh đổi hoặc giới hạn kết luận.

### 3.6. Thử nghiệm kiểm nguyên nhân (không dùng khi triển khai thực tế)

Trên **dev có nhãn thủ công cho pseudo**, chạy một nhánh tham chiếu dùng người chọn pseudo đúng. Đây là **cận tham chiếu/khảo sát nguyên nhân**: nếu pseudo đúng khiến B2 tốt rõ rệt thì bước chọn pseudo có thể là nút nghẽn đáng sửa. **Tuyệt đối không đưa nhãn người vào đầu vào mô hình ở test hoặc gọi nhánh này là zero-shot tự động.**

---

## 4. NHÁNH R — Nếu nguyên nhân chính là Fusion làm rơi vật đúng

### 4.1. Không sửa chỗ không hỏng

Nếu N4 xác nhận nhiều khung đúng đã tồn tại trong B2 nhưng bị Fusion loại, vấn đề chính là **quyết định giữ/loại cuối**, không phải pseudo. Khi đó chọn hướng R:

- Tính lại điểm hai nguồn bằng cách **chuẩn hóa điểm trên dev**; giữ công thức Fusion cố định làm nền.
- Phân tích các khung `đúng vật nhưng bị loại` so với `sai loại nhưng được giữ`: phân bố hai điểm khác nhau thế nào?
- **Đề xuất biến thể R1 để thử:** giữ khung khi qua Fusion **hoặc** khi điểm CountGD rất cao **và** điểm CLIP không quá thấp; nhưng chỉ kích hoạt quy tắc cứu khung khi bằng chứng có mặt của loại vật đủ mạnh. Tất cả ngưỡng/điều kiện chỉ chọn trên dev.
- So với đối chứng **giảm ngưỡng Fusion cố định**: nếu chỉ cần giảm ngưỡng là đạt như R1 thì R1 **không có đóng góp phương pháp đáng kể**.
- Vật không được tạo khung ngay từ đầu **không thể phục hồi bằng R1**.

Mã giả R1:

```python
# Các ngưỡng chỉ định nghĩa/chọn bằng dev, chưa có giá trị nào được công nhận.
keep_base = fused_score >= tau_f
rescue = (countgd_score >= tau_high and clip_score >= tau_low)
keep_new = keep_base or (query_presence_evidence >= tau_presence and rescue)
```

**Rủi ro bắt buộc kiểm:** nếu chó được CountGD chấm điểm rất cao khi hỏi `people`, quy tắc cứu có thể khôi phục **chính các khung sai**. Bởi vậy chỉ chạy R khi có N4 và đối chứng riêng với truy vấn vắng mặt. Nếu chưa tìm được bằng chứng hiện diện đáng tin mà không dùng GT, bỏ nhánh cứu khung này.

### 4.2. Tiêu chuẩn chọn giữa P và R

- Nếu **P cải thiện được cả việc giữ vật đúng và MAE khi có mặt** mà không tăng mạnh lỗi absent → giữ P làm phương pháp chính.
- Nếu P không có tác dụng, nhưng R vượt được Fusion ngưỡng thấp đơn giản → giữ R làm phương pháp chính.
- Nếu cả hai không vượt đối chứng trên tập khóa → báo **kết quả thực nghiệm âm tính**, không tự tuyên bố phương pháp mới tốt hơn.

---

## 5. Cách chia dữ liệu để nâng từ demo thành paper hội nghị

**Tuyệt đối không dùng lại 10 ảnh P4.6 vừa đọc kết quả để sửa P/R rồi gọi chúng là tập kiểm tra độc lập cuối.** Chúng vẫn dùng phân tích lỗi, demo và so sánh **phiên bản cũ**; việc điều chỉnh phương pháp mới trên chúng làm mất tính độc lập của đánh giá sau này.

### 5.1. Phân chia đề xuất (điều chỉnh theo nguồn lực)

- **5 ảnh pilot cũ:** phát hiện lỗi / phát triển; **không** tính là đánh giá cuối.
- **10 ảnh P4.6 đã xem:** đánh giá phiên bản Fusion *trước đây*, phân tích lỗi; **không dùng làm test cuối cho P/R thiết kế sau khi xem chúng**.
- **30 ảnh MUCCA khác:** tập phát triển mới để chọn `tau_pseudo`, `M` và các ngưỡng nhánh R; khóa ảnh theo ID trước khi chạy.
- **Tối thiểu 50 ảnh MUCCA khác nữa:** tập kiểm tra cuối cho phương pháp được chốt; chọn trước theo phân tầng, **không mở số liệu dự đoán để chỉnh nữa**.
- Nếu có thời gian: mở rộng tối đa theo MUCCA (200 ảnh tổng, số ảnh thực tế còn có thể dùng phụ thuộc trùng lặp); lý tưởng bổ sung thêm nguồn dữ liệu khác nếu bảo đảm giao thức nhãn.

**Cách chọn:** chia **theo ảnh gốc**, không theo query. Mỗi ảnh có ít nhất 2 truy vấn vật có mặt và 1 vật vắng mặt được người xác nhận. Nếu đủ nguồn lực, thêm 1 loại vắng mặt dễ để kiểm tính tổng quát. Chọn đủ nhóm vật, mật độ và độ khó theo tiêu chí **định trước**, không vì mô hình chạy sai mới lấy ảnh.

**Cảnh báo chọn tham số:** có thể dùng kết quả 5+10 ảnh đã biết để đặt giả thuyết, nhưng không được chỉnh qua lại nhiều phương án trên 50 ảnh cuối. Nếu đã xem kết quả 50 ảnh cuối và tiếp tục sửa, phải tìm **tập cuối khác**.

### 5.2. Chỉ số cần báo cáo và vì sao

| Chỉ số | Phải báo | Trả lời câu hỏi |
|---|---|---|
| `MAE_all`, `RMSE_all` | Có | Sai số đếm chung |
| `MAE_present` | **Bắt buộc** | Có giảm bỏ sót vật thật không? |
| `MeanAbsentCount` | **Bắt buộc** | Vắng mặt vẫn đếm nhầm trung bình bao nhiêu? |
| `FPR_absent` | **Bắt buộc** | Bao nhiêu truy vấn vắng mặt bị báo > 0? |
| Tỷ lệ vật đúng được giữ | **Bắt buộc nếu tuyên bố giữ vật đúng** | Vật thật còn giữ sau lọc? |
| Khung sai loại/khung trùng, có phân định mơ hồ | Có | Đếm đúng loại hay chỉ đếm đúng con số? |
| Phân rã E1–E4 và mẫu pseudo sai | Có | Phương pháp đang sửa đúng nút nghẽn không? |
| Thời gian/ảnh, GPU/RAM | Nên có | CLIP ở giữa hai lượt tốn bao nhiêu? |

Đếm vật đúng nên ghép **một–một** giữa khung được giữ và vật có nhãn, tránh một vật bị nhiều khung được tính nhiều lần. MUCCA có **nhãn điểm theo loại**, không mặc định có khung thật; phép điểm-nằm-trong-khung vẫn phải báo là xấp xỉ và hậu kiểm những trường hợp khung bao nhiều vật. Không ngụy tạo IoU/AP từ nhãn điểm.

**Thống kê:** lấy mẫu lại theo **ảnh**, kèm mọi truy vấn thuộc ảnh; báo chênh MAE theo cặp, khoảng tin cậy 95%, số lần lấy mẫu, seed và hạn chế khi số ảnh nhỏ. Không xem 3 query cùng ảnh là 3 quan sát độc lập.

---

## 6. Các câu hỏi phản biện và điều kiện quyết định gửi thầy

### 6.1. Nếu thầy hỏi “thay đổi so với paper gốc thực sự là gì?”

Trả lời **nếu nhánh P thành công:** “CountGD++ gốc chọn pseudo bằng điểm của chính mô hình. Nhóm bổ sung bước kiểm chứng ngữ nghĩa **trước khi đưa mẫu vào lượt đếm thứ hai**, nhằm giảm tác động của mẫu chọn sai. Khác với Fusion lọc cuối, phương pháp can thiệp vào nguồn hướng dẫn lượt hai. Nhóm đo riêng lỗi pseudo, khung sai loại, vật đúng bị mất và trường hợp đối tượng vắng mặt.”

Phải minh họa được **một mẫu sai ở lượt 1 → lượt 2 sinh khung sai**, và so sánh trước/sau sửa. Nếu chưa có bằng chứng thì dùng từ “giả thuyết”, không gọi là cơ chế đã được xác nhận.

### 6.2. Nếu thầy hỏi “CLIP đã có, đóng góp mới ở đâu?”

Cần thừa nhận:

- PseCo đã dùng CLIP để phân loại vùng ảnh được đề xuất.
- DAVE đã nghiên cứu phát hiện rồi xác minh để giảm đối tượng sai.
- CountGD++ có sẵn pseudo-exemplar và khả năng mô tả tiêu cực.
- PrACo++/MUCCA đã nêu bài toán đếm đúng loại và loại vắng mặt.

Vì thế **chỉ ghép CountGD++ và CLIP không đủ chắc để tự nhận là đóng góp thuật toán mới**. Nếu P/R không vượt cách lọc/ngưỡng đơn giản thì định vị bài viết là **phân tích thực nghiệm**, phù hợp hơn với hội thảo/ngữ cảnh thích hợp.

### 6.3. Đối chứng bị thiếu có thể khiến paper bị từ chối

- **B0 + cùng bộ lọc**: nếu tốt hơn toàn bộ nhánh B2, tại sao nhóm phải dùng hai lượt?
- **CountGD++ cấu hình chính thức phù hợp**: B0/B2 adapter không phải toàn bộ khả năng mô hình gốc. Kiểm thêm nhánh có mô tả loại không cần đếm nếu có đầu vào hợp lệ, không lấy tên vật gây nhiễu từ nhãn thật test.
- **Giảm ngưỡng Fusion đơn thuần**: nếu đạt kết quả giống R thì R không có ưu thế.
- **Pseudo kiểm bằng người trên dev**: cho biết lỗi chọn mẫu có thực sự là điểm nghẽn (chỉ làm phân tích, không dùng trong kết quả zero-shot test).
- **Chi phí tính toán**: thêm CLIP có đáng với cải thiện không?

### 6.4. Điều kiện nghiệm thu cải tiến mạnh (đề xuất, không phải tiêu chí của một hội nghị)

Trên **cùng bộ ảnh kiểm cuối chưa dùng chọn tham số**:

1. `MAE_present` **tốt hơn** Fusion cũ, tốt nhất là tiến gần hoặc vượt B0.
2. `MeanAbsentCount` và `FPR_absent` **không tăng đáng kể** so với Fusion cũ.
3. Tỷ lệ **vật đúng được giữ** tăng, có hậu kiểm độc lập và phân rã lỗi.
4. `MAE_all` cải thiện hoặc có bằng chứng đánh đổi rõ ràng được chấp nhận từ trước.
5. Hiệu quả vẫn thấy ở nhiều ảnh/cặp loại, không chỉ một vài trường hợp; có ước lượng độ không chắc chắn.
6. Không sử dụng GT hoặc nhãn/test để chọn mẫu/ngưỡng vào lúc suy luận.

Nếu chỉ tốt hơn B2 gốc mà **thua lọc điểm đơn giản** hoặc làm mất vật đúng như cũ, **chưa có cơ sở mạnh** để nói hướng phương pháp mới đủ sức gửi hội nghị có phản biện nghiêm ngặt.

---

## 7. Kế hoạch hành động gắn trực tiếp với mốc 02/12/2026

| Giai đoạn | Việc *phải làm* | Ai phụ trách đề xuất | Điều kiện chuyển bước |
|---|---|---|---|
| **W0 — 27/10–02/11** | Đồng bộ dữ liệu P4.6; N4 (9 query); Triệu hoàn tất T1–T4; phân rã E1–E4 | Trí chạy & tổng hợp; Triệu hậu kiểm | Có bằng chứng chọn nhánh P **hoặc** R, chưa sửa vội |
| **W1 — 03–08/11** | Khóa 30 dev mới + 50 test cuối bằng ID ảnh; quyết định chỉ số, cách nhãn; lập bảng đối chứng | Cả hai | Giao thức có người duyệt; không mở test cuối |
| **W2 — 09–15/11** | Tạo script thử nhánh P **hoặc** R; chạy phát triển, so B0/B2/Fusion/đối chứng đơn giản; lưu log | Trí; Triệu kiểm một phần kết quả | Có bảng cùng ảnh + ca giữ sai/bỏ đúng cụ thể |
| **W3 — 16–22/11** | Chốt **một** phương pháp, ngưỡng, CLIP checkpoint, tất cả cài đặt; làm rõ tính mới và đối chứng | Cả hai | Commit khóa và kế hoạch đánh giá cuối ký duyệt |
| **W4 — 23–26/11** | **Một lần đánh giá cuối** trên 50 ảnh khóa; tính số liệu và khoảng tin cậy, hoàn tất hậu kiểm đại diện | Trí chạy; Triệu chấm và đối chiếu | Có output, cấu hình, kiểm nhãn và bảng kết quả cuối |
| **W5 — 27/11–02/12** | Viết paper theo đúng kết quả, slide, hình ablation, demo, xin thầy góp ý nơi gửi | Cả hai | Bài hoàn chỉnh, không thổi phồng tính mới |

**Nếu thiếu thời gian:** ưu tiên N4 + dữ liệu test cuối + bảng đối chứng + bản viết tốt, **không** mở thêm 5 ý tưởng và bỏ dở phép thử chính.

---

## 8. Cấu trúc paper và kết luận được phép nêu

**Tên hướng P (chỉ dùng nếu được chứng minh):** *Semantic Verification of Pseudo-Exemplars for Robust Open-World Object Counting*.

**Tên hướng R (chỉ dùng nếu được chứng minh):** *Recall-Preserving Semantic Verification for Text-Guided Object Counting*.

**Nếu thuật toán mới không cải thiện:** dùng hướng phân tích *Failure Modes and Precision–Recall Trade-offs of Semantic Verification in CountGD++*; vẫn có giá trị báo cáo CS331, nhưng khả năng công bố sẽ phụ thuộc chất lượng phân tích và mức phù hợp của nơi gửi.

**Cấu trúc:** Abstract → Introduction (vấn đề X/Y, vật vắng mặt) → Related Work (CountGD++, PseCo, DAVE, PrACo++) → Method (chọn pseudo hoặc cứu vật đúng, ghi công thức + mã) → Experiments (chia ảnh/đối chứng/nhãn/chỉ số) → Results (có mặt/vắng mặt/giữ đúng) → Ablation (sửa mẫu hay chỉ thêm CLIP/ngưỡng) → Limitations → Conclusion.

**Chưa được khẳng định:** `Fusion` hay `P/R` đã giải quyết hoàn toàn X/Y; “tối ưu hơn tác giả gốc trên FSCD-147”; “một phương pháp chưa từng có”; “sẽ được nhận tại hội nghị”. Chỉ được khẳng định theo các phép thử được nêu cụ thể.

---

## 9. Nguồn nghiên cứu dùng để định vị tính mới

1. N. Amini-Naieni, A. Zisserman, **CountGD++: Generalized Prompting for Open-World Counting**, CVPR 2026. Trang tác giả: https://www.robots.ox.ac.uk/~vgg/publications/2026/AminiNaienib26/ ; mã nguồn: https://github.com/niki-amini-naieni/CountGDPlusPlus
2. Z. Huang và cộng sự, **Point, Segment and Count: A Generalized Framework for Object Counting (PseCo)**, CVPR 2024. https://openaccess.thecvf.com/content/CVPR2024/html/Huang_Point_Segment_and_Count_A_Generalized_Framework_for_Object_Counting_CVPR_2024_paper.html
3. J. Pelhan và cộng sự, **DAVE — A Detect-and-Verify Paradigm for Low-Shot Counting**, CVPR 2024. https://openaccess.thecvf.com/content/CVPR2024/html/Pelhan_DAVE_-_A_Detect-and-Verify_Paradigm_for_Low-Shot_Counting_CVPR_2024_paper.html
4. G. Pacini và cộng sự, **Does it Really Count? Assessing Semantic Grounding in Text-Guided Class-Agnostic Counting (PrACo++)**, 2026. https://arxiv.org/abs/2605.02752
5. **MUCCA dataset**, Zenodo, 2026, 200 ảnh có nhãn điểm theo loại: https://zenodo.org/records/19231375
6. Báo cáo và mã nguồn của nhóm: https://github.com/minhtridaoo/CS331 ; các con số P4.6 trong tài liệu này lấy từ bản tóm tắt do nhóm cung cấp ngày 27/10 và cần đồng bộ tệp gốc trước khi nộp.

---

## 10. Quyết định cần chốt trong cuộc họp nhóm

> **Chốt W0 trước khi viết thêm mô hình:** Sau N4, hãy trả lời bằng dữ liệu: **sai lệch lớn chủ yếu do pseudo sai trước lượt 2 (E1), hay do Fusion xóa vật đúng sau lượt 2 (E3)?** Nếu E1 chủ đạo → thử P1 ở đúng `select_pseudo` bằng một script mới. Nếu E3 chủ đạo → thử R1 với đối chứng hạ ngưỡng đơn giản. Chỉ chọn **một** đường làm đóng góp chính, chuẩn bị ảnh khóa độc lập, rồi chứng minh nó vượt Fusion hiện tại trên cả *giữ đúng vật* và *không đếm nhầm vật vắng mặt*.

**Bài tập giao ngay:** Trí trích `stage1_raw.npz`, danh sách pseudo và số đếm B0/B2/Fusion của 9 query N4; Triệu kiểm từng mẫu/khung, gán nhãn và kết luận E1/E2/E3/E4. Từ bảng đó mới quyết định chính xác sửa phương pháp nào.
