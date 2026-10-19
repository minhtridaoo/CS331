# CS331 UIT — Zero-Shot Object Counting
## V3.4.2 — Bản chốt phạm vi 6 tuần (Target Sensitivity, paraphrase chỉ đánh giá)

Soạn 07/10/2026. Thay cho V3.3.1. **Đây là bản chốt: từ giờ không mở thêm vòng review roadmap. Mọi quyết định tiếp theo dựa trên số đo của tuần 1** (baseline, chất lượng nhãn mosaic, GPU-hours).

**Nguồn gộp (đều nằm trong `ban_cu/`):**
- `CS331_ZSC_V3_3_Final.md` (V3.3.1, 26/09). Phần kỹ thuật vẫn dùng, xem §11.
- `CS331_Roadmap_DanhGiaLai_2026-10-07.md`: đánh giá lại V3.3.1.
- `CS331_DeXuat_ChotDeTai_6Tuan_2026-10-07.md`: đề xuất thu phạm vi, là khung của V3.4.
- `CS331_ZSC_V3_4_Review_2026-10-07.md`: review V3.4, đã đưa vào V3.4.1.
- `CS331_BaoCao_DanhGia_VanDe.md`: đánh giá 6 vấn đề của V3.4.1, đã đưa vào V3.4.2.

**Thay đổi so với V3.3, tóm tắt một dòng:** bỏ `L_same`/E1/E3 khỏi phạm vi chính và chỉ giữ cross-class mosaic (E0/E0-ft/E2). Thêm khảo sát theo xác suất ghép α, có control khớp crop. Thêm đánh giá paraphrase, chỉ làm inference.

## Changelog V3.4 → V3.4.1 (07/10, theo review V3.4, đã đối chiếu code)

| # | Sửa | Đã kiểm |
|---|---|---|
| 1 | α là **xác suất chọn nhánh out-mosaic**, không phải "tỉ lệ ô ghép khác lớp". Log riêng các tỉ lệ thực tế (§4.2). Sửa câu trong form (§13) | `FSC147.py:352` lấy ảnh phụ ngẫu nhiên, có thể trùng lớp. Dòng 370 giữ density của ảnh phụ trùng lớp |
| 2 | Bỏ câu "phần này chưa ai đo" | Không có khảo sát hệ thống để chứng minh câu đó |
| 3 | Bỏ câu "rẻ, 1–2 ngày". Tính lại theo 6 checkpoint. Phần bắt buộc thu về các target có mặt (§6.3) | Evaluator MUCCA lặp qua **45 lớp** của split `test` (`multiclass_split_classes.json`) cho mỗi ảnh |
| 4 | Mỗi run có thư mục riêng theo cấu hình × seed × checkpoint × protocol × template (§6.5) | `benchmark/multiclass_benchmark.py` đọc lại CSV có sẵn để bỏ qua ảnh đã chạy. Density lưu ở `<results>/<model_name>/density_maps/<ảnh>_<lớp>.npy`, không có checkpoint, template hay seed trong đường dẫn |
| 5 | E2-half chỉ là điểm khảo sát. Khi cắt seed thì cắt cả hai bên. Khóa template test và K ở cuối tuần 3 (§3, §6, §8) | — |
| 6 | Sửa chiều scale: out-mosaic (crop 250–384) làm vật **nhỏ hơn** so với self-mosaic (150–384), không phải to hơn | Ô ra có cạnh cố định `resize_l` 212–232, nên crop nguồn càng lớn thì vật càng co |
| 7 | Sửa nhỏ: null-mosaic chỉ là ý định của sampler; lọc cặp phải kiểm lại trên mẫu mới; E0 trên FSC test chỉ để đối chiếu tái lập; missing keys | `run.py:410–415` `on_save_checkpoint` cố ý xoá tham số CLIP đóng băng |
| 8 | Công thức kiểm tra density ở tuần 2: `sum(density)/60` ≈ số point. Thêm MUCCA CntF1 theo template làm metric chọn target dưới paraphrase (§6.4, §7) | `util/constant.py:1` `SCALE_FACTOR = 60`, `run.py:189`; PrACo++ §3.3 |

## Changelog V3.4.1 → V3.4.2 (07/10, theo `CS331_BaoCao_DanhGia_VanDe.md`)

| # | Sửa | Lý do |
|---|---|---|
| 1 | **Sampler ảnh phụ khác nhãn** cho E2-half/E2: ảnh phụ phải có nhãn FSC-147 khác target (§4.2) | Ảnh phụ ngẫu nhiên có thể trùng lớp nên liều can thiệp thật thấp hơn α. Ước lượng thô: tần suất out-mosaic ≈ 0.3 × α × P(N<70), phải đo ở tuần 1 |
| 2 | Checkpoint chính = best FSC val MAE cho mọi cấu hình. Thêm **last-epoch** làm kiểm tra độ nhạy cho E0-ft/E2. Val-mosaic chỉ để theo dõi, không chọn checkpoint (§3, §5, §7) | Sửa mâu thuẫn giữa §3 và §5. Val MAE có thể không chọn đúng epoch tốt nhất về target sensitivity |
| 3 | Định nghĩa trước con số chính: trung bình delta theo cặp seed, kèm bootstrap theo ảnh dùng chung tập ảnh lấy mẫu (§7) | Tránh chọn cách gộp có lợi sau khi thấy kết quả |
| 4 | Thêm mục định vị và đóng góp (§0) | Đóng góp là nghiên cứu can thiệp có đối chứng, không phải phương pháp mới |
| 5 | Dàn lại tuần 1–2: tuần 1 chỉ smoke test MUCCA, tuần 2 hoàn thiện MUCCA (§8) | Tuần 1 đang quá tải |
| 6 | Nhóm 2 người **đã xác nhận**. Tách cột số seed và seed ID. Đánh số changelog liên tục | Sửa trình bày |

---

# 0. Nội dung báo thầy (đọc phần này trước)

**Vấn đề chọn:** vấn đề 3 thầy nêu. Cùng một ảnh, hỏi X rồi hỏi Y mà mô hình vẫn đếm gần như nhau, dù target đã khác.

**Vai trò của hai vấn đề còn lại:**
- Vấn đề 1 (học theo GT density nhưng đếm cả vùng không liên quan) là bối cảnh và giả thuyết. Đồ án kiểm tra giả thuyết rằng khi mỗi ảnh train chỉ có một lớp được giám sát, mô hình thiếu tín hiệu để phân biệt target. Đồ án không chứng minh density là nguyên nhân và không thay thế density supervision.
- Vấn đề 2 (Grounding DINO đúng nhưng VA-Count đếm sai) chỉ làm chẩn đoán nhỏ nếu còn thời gian, tối đa 2 ngày, không retrain VA-Count.

**Câu hỏi nghiên cứu:** cho CLIP-Count học thêm trên ảnh ghép từ nhiều ảnh nguồn, với GT density chỉ tính lớp được hỏi (cross-class mosaic), thì mô hình có đếm đúng lớp được yêu cầu trong ảnh nhiều loại vật hơn không? Hiệu quả đó có giữ được khi query được viết theo cách khác cùng nghĩa không, và độ chính xác đếm thông thường có được giữ không?

**Làm gì:**
1. Fine-tune CLIP-Count với xác suất ghép từ nhiều ảnh nguồn α ∈ {0, 0.5, 1}, trong đó ảnh phụ được lấy từ lớp khác target. α = 0 là control (E0-ft). Mọi cấu hình có cùng lượng ảnh ghép, cùng khoảng crop, cùng số epoch, LR và batch. Tham số can thiệp duy nhất được thay đổi là α. Tỉ lệ mẫu đa lớp thực tế được thống kê, không suy ra từ α.
2. Đánh giá trên FSC-147 (đếm thông thường), PrACo (negative-label, mosaic) và MUCCA (ảnh đa lớp thật, bằng chứng chính).
3. Đánh giá có kiểm soát với các cách diễn đạt tương đương, để kiểm tra hiệu quả chọn đúng target sau fine-tune còn giữ được khi query đổi cách viết hay không. Phần này chỉ làm inference.

**Định vị:** một nghiên cứu can thiệp có đối chứng trên CLIP-Count, kiểm tra tác động của cross-class supervision đến target sensitivity, sự đánh đổi với độ chính xác đếm thông thường, và độ bền khi truy vấn được diễn đạt lại cùng nghĩa.

**Đóng góp nêu trong báo cáo:**
- Control fine-tune khớp (cùng lượng ảnh ghép, crop, lịch tối ưu).
- Sampler ảnh phụ khác nhãn, kèm audit chất lượng nhãn (đây là sửa đổi kỹ thuật nhỏ, không phải phương pháp mới).
- Đánh giá chọn target trên ảnh đa lớp thật (MUCCA).
- Đánh giá paraphrase tách riêng độ ổn định của count với việc đếm đúng target.
- Báo hiệu ứng theo cặp seed và độ nhạy theo cách chọn checkpoint.

Nếu thầy yêu cầu đóng góp phương pháp mới ở mức paper thì phải chốt tiêu chí đó ngay tuần 1, không mở rộng vào cuối lịch.

**Không nhận:** không nhận mosaic là phát minh (đã có trong CounTR, MGCAC, CountGD++). Không nhận tính mới tuyệt đối của phép đo paraphrase. Không nhắm SOTA. Không retrain VA-Count hay T2ICount.

**Sản phẩm:** code và notebook tái lập, checkpoint, bảng E0/E0-ft/E2, khảo sát theo α, hình cùng ảnh khác target (cả ca đúng lẫn ca sai), báo cáo, slide, demo.

---

# 1. Bốn chỗ V3.4 sửa so với bản đề xuất 6 tuần

| # | Bản đề xuất | V3.4.2 | Lý do |
|---|---|---|---|
| 1 | "Kích hoạt và **điều chỉnh**" mosaic nhưng không nói điều chỉnh gì | Thêm xác suất α, khảo sát α ∈ {0, 0.5, 1}, sampler ảnh phụ khác nhãn (§4.2). Tùy chọn: lọc cặp lớp hay xuất hiện chung (§4.3) | Không thêm gì thì E2 chỉ là đổi `use_out_mosaic` ở `FSC147.py:224`. Khảo sát theo α giúp hiểu mức độ và giới hạn của can thiệp. Bản thân việc quét tham số không phải phương pháp mới, và không cần thêm module chỉ để phương pháp trông phức tạp hơn |
| 2 | Paraphrase ở phần mở rộng | **Bắt buộc ở mức tối thiểu, chỉ inference** (§6.3) | Giúp phần "Evaluating" không chỉ lặp lại PrACo++, vì PrACo++ đã có số của CLIP-Count trên PrACo và MUCCA. Bản đánh giá lại §7 cũng yêu cầu đánh giá kết hợp |
| 3 | PrACo++ xếp ngang các nguồn khác | **MUCCA là bằng chứng chính.** Test mosaic của PrACo ghi rõ là "tổng hợp, gần phân phối train của E2" | E2 train trên ảnh ghép 2×2, nên tốt lên ở test mosaic không chứng minh được gì về cảnh thật |
| 4 | "Giữ self-mosaic của control khi phù hợp" | Control **khớp chính xác**: cùng 30% ảnh ghép, cùng crop 250–384 (§4.2) | Code gốc cho self-mosaic crop 150–384 (dòng 323), out-mosaic crop 250–384 (dòng 364), cùng resize về `resize_l` 212–232. Out-mosaic vì vậy cho vật **nhỏ hơn** (hệ số co 0.55–0.93, so với 0.55–1.55 của self-mosaic). Để nguyên thì scale vật là một biến gây nhiễu |

---

# 2. Tên đề tài

**Tiếng Anh (chính):** Evaluating and Improving Target Sensitivity in Text-Guided Zero-Shot Object Counting

**Tiếng Việt:** Đánh giá và nghiên cứu cải thiện khả năng đếm đúng đối tượng theo truy vấn trong bài toán Zero-Shot Object Counting

**Phương án dự phòng (nếu muốn nêu rõ phần paraphrase):** Improving Target Sensitivity in Text-Guided Zero-Shot Object Counting and Its Robustness to Query Paraphrasing

"Improving" là mục tiêu nghiên cứu, chưa phải kết quả đã có. Tên V3.3 ("Stable to Wording, Sensitive to Targets…") không dùng nữa, vì V3.4 không còn huấn luyện consistency.

---

# 3. Cấu hình thí nghiệm

| ID | α | Số seed | Seed ID | Vai trò |
|---|---|---|---|---|
| E0 | checkpoint official, không fine-tune | — | — (không train mới) | Mốc tái lập |
| E0-ft | 0 (toàn self-mosaic, crop khớp) | 2 | s1, s2 | Control: tách tác dụng của việc học thêm |
| E2-half | 0.5 | 1 | s1 | **Điểm khảo sát**, không có error bar theo seed |
| E2 | 1 | 2 | s1, s2 (cùng E0-ft) | Can thiệp chính |

Seed ID cụ thể (ví dụ s1 = 0, s2 = 1) chốt ở tuần 1 và ghi vào `meta.json` (§6.5).

**Định nghĩa α:** xác suất chọn nhánh out-mosaic, áp dụng khi mẫu đã vào nhánh mosaic **và** ảnh nguồn có dưới 70 point. Tần suất out-mosaic kỳ vọng trên toàn bộ mẫu xấp xỉ `0.3 × α × P(ảnh < 70 point)`. Với sampler khác nhãn (§4.2), mỗi out-mosaic có ít nhất hai nhãn nguồn, trừ khi sampler rơi vào fallback (phải log). Đây vẫn chỉ là ước lượng thô, **phải đo từ dữ liệu ở tuần 1**: nếu liều thật quá thấp thì ghi đó là giới hạn của can thiệp. Mọi quyết định tăng tổng tỉ lệ mosaic chỉ được đưa ra trên train/dev trước khi khóa thiết kế, và áp dụng chung cho control lẫn can thiệp. α còn làm thay đổi phân bố số vật của target và tần suất GT bằng 0. Vì vậy không nói rằng thí nghiệm đã tách riêng tuyệt đối ảnh hưởng ngữ nghĩa.

**Giống nhau ở mọi cấu hình fine-tune** (chi tiết ở V3.3 §61.5):
- 30–50 epoch (chốt một số sau khi đo thời gian ở tuần 1), LR ~1e-5, AdamW, cùng effective batch.
- Cùng 30% ảnh ghép (`FSC147.py:243`) và cùng crop ô 250–384.
- **Checkpoint chính (primary)** = `val_mae` thấp nhất trên FSC-147 val, cùng quy tắc cho mọi cấu hình, chốt trước. Val-mosaic **không** tham gia chọn checkpoint.
- **Checkpoint last** (epoch cuối, `save_last=True`) của E0-ft và E2, cả hai seed, dùng làm kiểm tra độ nhạy. Báo bảng primary và bảng last riêng. Không chuyển last thành kết quả chính sau khi xem test.

**So sánh chính:** E2 với E0-ft trên cùng các seed, checkpoint primary. Ưu tiên MUCCA CntF1 với prompt gốc, xem MAE đi kèm. Cách tính con số chính và CI chốt trước ở §7.

**Ngân sách:** 5 lượt fine-tune. **6 checkpoint primary** cần đánh giá: E0 (1), E0-ft (2), E2-half (1), E2 (2). Thêm **tối đa 4 checkpoint last** (E0-ft, E2 × 2 seed); last nào trùng primary thì không chạy lại. Checkpoint last chỉ đánh giá FSC MAE/RMSE và MUCCA CntF1/MAE với prompt gốc, không chạy paraphrase. Ngân sách tính gồm cả validation, primary/last, paraphrase và lưu density, không chỉ giờ train. Nếu số đo tuần 1 cho thấy không đủ GPU, cắt theo thứ tự:
1. Cắt E2-half.
2. Giảm số epoch đồng đều cho mọi cấu hình, quyết định dựa trên dev.
3. Bỏ seed 2 **của cả E0-ft lẫn E2 cùng lúc**, giữ cùng một seed cho cặp này. Không giữ seed 2 cho chỉ một bên.

Nếu chỉ còn 1 seed thì ghi rõ và nói nhẹ kết luận đi.

**Đã bỏ khỏi phạm vi chính, để vào hướng phát triển:** E1-aug, E1, E3, `L_same`, hard-pair, null-mosaic mở rộng, nhiều bố cục mosaic, spatial gate. Muốn đưa consistency trở lại thì bắt buộc kèm E1-aug và tính lại lịch.

---

# 4. Thay đổi code (tất cả trong `code/CLIP-Count`)

## 4.1. Bật out-mosaic qua args (bắt buộc)

- `util/FSC147.py:224`: thay `self.use_out_mosaic = False` bằng giá trị đọc từ args.
- `run.py:435`: `FSC147(split="train")` đang được tạo mà không truyền args, cần sửa để truyền args vào.
- Vá bẫy `overwrite_args`, `--contrast_pre_epoch -1`, `save_last=True` lưu lên Drive: xem V3.3 §61.1–61.3 và §61.6. **Chưa vá thì mọi flag mới, kể cả `--lr`, đều bị bỏ qua mà không báo lỗi.** `overwrite_args` chỉ gán `self.args`, nên phải kiểm tra thêm hyperparameters được lưu vào checkpoint mới.

## 4.2. Xác suất α và crop khớp (bắt buộc)

- Thêm `--out_mosaic_ratio α`. Sửa điều kiện ở `FSC147.py:321`: trong nhánh mosaic, nếu ảnh có ≥70 vật hoặc `random.random() >= α` thì dùng self-mosaic, còn lại dùng out-mosaic. Tổng lượng ảnh ghép vẫn là 30%.
- **Sampler ảnh phụ khác nhãn (bắt buộc, áp dụng như nhau cho E2-half và E2):** ở dòng 352, lấy lại ảnh phụ cho tới khi `class_dict[Tim_id] != class_dict[im_id]`, tối đa 20 lần. Hết 20 lần thì dùng ảnh cuối và tính là fallback. Đây là sửa đổi kỹ thuật nhỏ để can thiệp rõ hơn, không nhận là phương pháp mới. E0-ft (α = 0) không đi vào nhánh này nên không bị ảnh hưởng.
- Thêm `--mosaic_min_crop`, đặt 250 cho mọi cấu hình fine-tune. Sửa `randint(150, 384)` ở dòng 323 cho self-mosaic khớp out-mosaic (dòng 364). E0-ft vì vậy khác cách train official một chút. Điều này chấp nhận được vì E0-ft là control của E2; E0 mới là bản tái lập official.
- **Log theo epoch.** `__getitem__` trả thêm thông tin loại mẫu. Không dùng biến đếm trong dataset, vì với `num_workers > 0` các worker không cộng dồn được. Các số phải log:
  - tỉ lệ mẫu đi vào nhánh out-mosaic;
  - tỉ lệ mosaic thực sự có nhiều nhãn lớp nguồn;
  - số ô có nhãn lớp khác target;
  - tỉ lệ GT count bằng 0 sau crop;
  - tỉ lệ fallback của sampler khác nhãn.

  Ghi rõ mẫu số của từng tỉ lệ (toàn bộ mẫu hay chỉ mẫu mosaic). Không suy liều thực tế trực tiếp từ α.

  Nhãn lớp khác target **không chứng minh** ô đó không chứa target chưa được gán nhãn (xem §4.3).

## 4.3. Lọc cặp lớp (tùy chọn, quyết định ở cuối tuần 2)

Sampler khác nhãn (§4.2) chỉ bảo đảm **nhãn nguồn** khác target, không bảo đảm target vắng mặt. Ô khác lớp có density bằng 0, dù vật thuộc lớp được hỏi có thể có mặt trong ô đó mà không được gán nhãn (ví dụ hỏi "people", ô phụ là ảnh "cars" có người trong đó).

- **Chốt trước** ngưỡng "lỗi cao đáng kể", ví dụ trên 10% số ô phụ, trước khi đếm.
- Tuần 2: kiểm tra thủ công **mẫu A gồm 100 ảnh ghép train** (seed cố định), đếm tỉ lệ ô phụ chứa target mà không có nhãn.
- Nếu vượt ngưỡng: lập danh sách cặp lớp cấm từ mẫu A, thêm vào bước lấy mẫu ở dòng 352. Kiểm tra lại trên **mẫu B mới**, gồm 100 ảnh với seed khác, không trùng A. Báo tỉ lệ lỗi trên B.
- Nếu không vượt ngưỡng: giữ sampler khác nhãn, không thêm danh sách cấm, và ghi tỉ lệ đo được vào phần giới hạn.
- Không dùng cosine ngữ nghĩa thấp làm bằng chứng target vắng mặt. Không dùng kết quả test để chọn ngưỡng.

## 4.4. Những điểm code biết rồi nhưng không sửa (ghi vào báo cáo)

- `FSC147.py:328`: self-mosaic tính `Augmentation(...)` rồi bỏ kết quả, vì dòng 334 append ảnh chưa augment. Giữ nguyên để giống official.
- Vật bị cắt ở mép ô vẫn tính 1 nếu tâm nằm trong ô. Ảnh được blend 10–20 px ở đường ghép, còn density thì cắt thẳng (V3.3 §9.6).
- Null-mosaic: con số khoảng 1.5% chỉ là **ý định của sampler** (`gt_pos = 4`), tính trước các điều kiện khác. Đó không phải tỉ lệ null thật: ô phụ có thể chứa target chưa gán nhãn (§4.3), lần fallback của sampler có thể lấy ảnh trùng lớp, và crop làm mất point của target cũng tạo ra GT bằng 0. Log riêng ba thứ: ý định sampler, GT bằng 0, và target vắng mặt đã được kiểm tra (khi có thể).

---

# 5. Dữ liệu và quy tắc dùng test

| Tập | Vai trò |
|---|---|
| FSC-147 train | Fine-tune, nguồn ô ghép |
| FSC-147 val, cộng mosaic dựng từ val (seed cố định) | FSC val MAE: chọn checkpoint primary. Val-mosaic: pilot, kiểm tra pipeline, theo dõi CntF1 theo lịch cố định (ví dụ mỗi 5 epoch), **không** chọn checkpoint. Nếu đường val MAE và val-mosaic CntF1 đi khác chiều thì đưa vào thảo luận, nhưng val-mosaic là dữ liệu tổng hợp nên không suy ra được diễn biến tương tự trên ảnh thật. Lớp val không trùng lớp train, nên mosaic từ val là phép thử chọn target trên lớp chưa gặp |
| FSC-147 test | Đánh giá cuối về độ chính xác đếm thông thường (MAE/RMSE) |
| PrACo (negative-label, mosaic) | Đánh giá cuối. **Test mosaic gần phân phối train của E2**, chỉ ghi là bằng chứng tổng hợp |
| MUCCA (200 ảnh thật, 45 lớp, Zenodo 19231375) | **Bằng chứng chính** về chọn đúng target. Paired bootstrap theo ảnh |
| PairTally INTER | Mở rộng, chỉ chạy nếu còn thời gian. **Không** dùng INTRA làm tiêu chí (cần hiểu thuộc tính, nằm ngoài phạm vi) |

**Quy tắc khóa (sửa chỗ mâu thuẫn giữa V3.3 §9.7 và §36):**
- Mọi quyết định thiết kế (crop, lọc cặp, số epoch, bộ prompt, K) đều dựa trên FSC-147 val và mosaic từ val. Tất cả khóa ở **cuối tuần 3**.
- Tuần 1–3 kiểm thử pipeline trên val. **Ngoại lệ duy nhất:** chạy E0 trên FSC test để đối chiếu với số đã công bố (17.78 / 17.45 / 17.19, V3.3 §61.9). Số này ghi rõ mục đích "đối chiếu tái lập" và không dùng để chọn can thiệp.
- Không chạy MUCCA hay PrACo trên checkpoint fine-tune trước khi khóa thiết kế. Bố cục mosaic giữ 2×2.

**Seen/unseen:** audit lớp của MUCCA và PairTally so với lớp train của FSC-147, báo riêng từng nhóm (V3.3 §37). "Zero-shot" ở đây là lớp chưa gặp khi train counting, không phải chưa gặp khi pretrain CLIP.

---

# 6. Đánh giá paraphrase (chỉ inference)

## 6.1. Mục tiêu

Kiểm tra hai điều trên cùng bộ query cho mọi checkpoint:
- (a) Count và density có ổn định khi đổi cách viết cùng nghĩa không.
- (b) E2 có còn chọn đúng target khi query được viết lại không.

## 6.2. Bộ prompt

- Tiêu chí: tự nhiên, giữ đúng tập đối tượng, không thêm màu, vị trí hay số lượng (V3.3 §16).
- Chia template thành **dev** (để kiểm tra prompt hợp lệ và chọn K) và **test**. Loại các template trùng hoặc gần trùng giữa hai phần. Không có prompt train.
- Nếu dùng LLM để sinh thì gọi đúng là "held-out LLM-generated prompts", không nói là "unseen family".
- Mặc định K = 5. **Template test và K khóa ở cuối tuần 3**, cùng lúc với thiết kế.

## 6.3. Phạm vi bắt buộc và mở rộng

| Mức | Nội dung |
|---|---|
| **Bắt buộc** | (1) Prompt gốc theo protocol chuẩn trên FSC, PrACo, MUCCA. (2) Paraphrase × K trên FSC test. (3) Paraphrase × K trên MUCCA, **chỉ các target có mặt và có nhãn** trong từng ảnh |
| Mở rộng (nếu còn ngân sách) | Toàn bộ negative-label protocol của MUCCA (45 lớp × mỗi ảnh) dưới mọi paraphrase. Nếu chỉ lấy tập con query thì định nghĩa trước trên dev và báo là **protocol bổ sung**, không so trực tiếp với số full protocol |

**Ước lượng quy mô** (số cặp ảnh–query, chưa phải thời gian GPU): full negative-label dưới paraphrase là 200 ảnh × 45 lớp × 6 checkpoint × 5 template = **270.000 cặp** chỉ riêng MUCCA. Đó là lý do phần này để ở mở rộng. **Ngân sách thật chốt ở tuần 1**, sau khi đo thời gian một lượt đánh giá trên dữ liệu dev.

## 6.4. Metric

- MAE theo từng template, NPV và WPMAE theo định nghĩa ở V3.3 §31–32.
- **NPV chỉ tính trên target có count dương**, để mẫu số epsilon không chi phối kết quả. Các query vắng mặt đánh giá riêng bằng metric negative-label.
- Chốt epsilon và cách tổng hợp theo ảnh trước khi chạy.
- **Metric chọn đúng target dưới paraphrase (bắt buộc):** MUCCA CntP/CntR/CntF1 theo **từng template**, trên các target có mặt và có nhãn, so với prompt gốc (báo delta CntF1 so với prompt gốc, paired theo ảnh). Theo PrACo++ §3.3, CntF1 tính TP/FP/FN theo từng patch và chỉ trên lớp có mặt, nên khớp đúng phạm vi bắt buộc ở §6.3 và cần density map lưu đúng thư mục theo template (§6.5).
- Không coi NPV thấp là thành công nếu thiếu CntF1 và sai số trên cùng ảnh và cùng target: count ổn định chưa chứng minh mô hình vẫn đếm đúng vùng của đối tượng được hỏi.

Paraphrase-PrACo: sửa `get_text_prompt` trong `PrACo/models/clipcount_model.py` (hiện chỉ `return f"{text}"`) để tra template test (V3.3 §32.2). **Chỉ sửa chỗ này chưa đủ**, xem §6.5.

Tối ưu tùy chọn: `deep_vpt_forward` (`models/clip_count.py:300–334`) không đọc `text_embedding`, nên có thể tính đặc trưng ảnh một lần cho K prompt. Điều này sửa nhận định sai ở V3.3 §21.2. Trước khi dùng, phải đối chiếu đầu ra với forward đầy đủ trên dev ở chế độ eval. Mức tăng tốc chưa được đo.

## 6.5. Định danh kết quả (điều kiện tính đúng, bắt buộc)

Evaluator MUCCA đọc lại CSV có sẵn để bỏ qua ảnh đã chạy, và lưu density ở `<results>/<model_name>/density_maps/<ảnh>_<lớp>.npy`. Đường dẫn này không có checkpoint, template hay seed. Đổi checkpoint hoặc template mà giữ nguyên `model_name` và thư mục thì sẽ **đọc nhầm kết quả cũ hoặc ghi đè density**.

- Mỗi run có thư mục riêng: `results/<cấu hình>/seed_<s>/<ckpt_id>/<benchmark>_<protocol>/template_<id>/`, ví dụ `results/E2/seed_1/ep37/MUCCA_present/template_03/`.
- Mỗi thư mục có `meta.json` (checkpoint hash, cấu hình, seed, protocol, template). Khi resume phải **so khớp `meta.json`** trước khi đọc kết quả cũ, không khớp thì dừng.
- Script tính thống kê đọc density cùng đường dẫn đó.

---

# 7. Metric và thống kê

**Bảng chính:**
- FSC test: MAE, RMSE.
- PrACo: NMN, PCCN, CntF1, theo đúng evaluator của PrACo.
- MUCCA: metric theo evaluator PrACo++.
- Paraphrase: MUCCA CntF1 theo từng template (so với prompt gốc), NPV và WPMAE trên target có mặt, kèm MAE theo template.

**Hình bắt buộc:**
- Khảo sát theo α (0 / 0.5 / 1): MUCCA CntF1 và FSC MAE. α = 0 và α = 1 có error bar theo seed. α = 0.5 là **một điểm khảo sát**, không dùng để kết luận một quy luật tăng hay giảm.
- Cùng ảnh, khác target, kèm density dự đoán: ca thành công lẫn ca thất bại.

**Thống kê (chốt trước khi chạy test):**
- Với metric M, delta theo từng seed: `Δ_s = M(E2, s) − M(E0-ft, s)`. **Con số chính:** `Δ_main = (Δ_s1 + Δ_s2) / 2`.
- CI bằng bootstrap theo ảnh. Mỗi replicate lấy mẫu **ảnh có hoàn lại**, giữ mọi query và patch của cùng một ảnh chung một nhóm, và dùng **cùng tập ảnh đã lấy mẫu** cho cả hai cấu hình lẫn hai seed. Tính lại M cho từng run theo đúng phép tổng hợp của evaluator (CntF1 và RMSE là phi tuyến, không thay bằng trung bình delta theo query), tính Δ_s, rồi lấy trung bình hai Δ_s.
- CI này chỉ phản ánh sai số do lấy mẫu ảnh, **có điều kiện trên hai run đã train**. Không diễn giải nó là CI của biến thiên giữa các seed. Không dùng hierarchical bootstrap seed × ảnh khi chỉ có hai seed.
- Luôn báo thêm Δ_s1 và Δ_s2 để thấy hai seed có cùng chiều tác động không.
- **Không** lấy trung bình count hay density của hai seed rồi mới tính metric, vì cách đó đánh giá một ensemble chứ không phải tác động trung bình của can thiệp.
- Bảng last-checkpoint dùng cùng quy trình, báo riêng.
- CI chứa 0 không tự chứng minh can thiệp không có tác dụng. Nếu không cải thiện, báo đủ: liều thực tế, chất lượng nhãn, Δ từng seed, độ nhạy theo checkpoint và sự đánh đổi.

**Diễn giải kết quả:**
- E2 phải được xét đồng thời về chọn target và sai số đếm. Nếu có đánh đổi thì báo cả hai, không chỉ chọn metric có lợi.
- Hai target có cùng số lượng thì hai count bằng nhau vẫn có thể đúng. Không dùng "count phải đổi" làm tiêu chí duy nhất.
- Kết quả không cải thiện vẫn được báo cáo như một thí nghiệm có đối chứng, kèm giới hạn.

**Trước khi chạy cả benchmark:**
- Đối chiếu đầu ra của inference CLIP-Count local và wrapper PrACo trên cùng ảnh và query.
- Wrapper dùng `load_from_checkpoint(strict=False)`. Checkpoint CLIP-Count **cố ý** bỏ tham số CLIP đóng băng (`run.py:410–415`), nên missing keys thuộc `model.clip*`, `model.img_encoder.clip*`, `model.text_encoder.clip*`, `model.img_encoder.vit*` là bình thường, vì phần này được nạp lại từ CLIP gốc. **Chỉ báo lỗi khi thiếu key của phần trainable.** In danh sách missing keys và so với danh sách trên.
- Ghi rõ dùng checkpoint filtered hay unfiltered.

---

# 8. Lịch 6 tuần (07/10 → 17/11; form có ngày báo cáo từ 18/11 đến 16/12)

| Tuần | Ngày | Việc | Đầu ra |
|---|---|---|---|
| 1 | 07–13/10 | Báo thầy chốt đề tài (hỏi luôn tiêu chí về tính mới). Colab (V3.3 §61.4: `numpy<2`, `setuptools<81`). Tái lập E0 (val; FSC test chỉ để đối chiếu, §5). PrACo chạy được với E0. MUCCA **chỉ smoke test** vài ảnh để kiểm tra format và pipeline, không dùng số của smoke test để chọn sampler hay prompt. Dựng schema kết quả và thư mục §6.5. Đo P(N<70) trên FSC train và thời gian 1 epoch, 1 lượt đánh giá | Số baseline E0, P(N<70), **dự toán GPU-hours (bắt buộc)**, chốt số epoch và seed ID |
| 2 | 14–20/10 | **A:** vá code §4.1–4.2 (sampler khác nhãn, crop, log), smoke fine-tune. **B:** hoàn thiện evaluator MUCCA, audit mẫu A, bộ prompt, metric, đo thời gian 1 lượt paraphrase trên dev. **Phải xong trước run chính:** kiểm tra density/count, so local với wrapper, save/resume. Kiểm tra trực quan ảnh ghép. Kiểm tra density: với density đã nhân 60 (`FSC147.py:404`), `sum(density) / 60` ≈ số point của target sau crop; nếu kiểm trước bước nhân thì `sum(density)` ≈ số point (code tính count cũng chia `SCALE_FACTOR = 60`, `run.py:189`). Kiểm tra mẫu A (§4.3). Fine-tune thử 1 epoch: kiểm tra `self.args.lr`, gradient, missing keys, save/resume. Dựng bộ prompt dev/test | Pipeline can thiệp chạy được, log tỉ lệ §4.2, quyết định lọc cặp |
| 3 | 21–27/10 | Pilot ngắn E0-ft/E2 trên val. **Cuối tuần khóa thiết kế, template test và K.** Bắt đầu chạy chính | Protocol đã khóa, các run đầu tiên |
| 4 | 28/10–03/11 | Chạy xong E0-ft/E2 (cùng 2 seed), rồi E2-half. Không thêm loss, backbone hay dataset mới | Checkpoint, log, dự đoán theo ảnh |
| 5 | 04–10/11 | Đánh giá cuối: FSC, PrACo, MUCCA, paraphrase bắt buộc (§6.3). Tính CI, phân tích lỗi. Nếu xong sớm thì thêm **một** phần mở rộng (§6.3 hoặc §9) | Bảng kết quả, hình |
| 6 | 11–17/11 | Viết báo cáo, slide, demo, hướng dẫn tái lập. Chạy thử buổi trình bày | Bộ nộp hoàn chỉnh |

**Mốc quyết định:**
- Cuối tuần 1: E0 hoặc evaluator chưa chạy được thì xử lý hạ tầng trước, chưa nhận thêm việc. Áp dụng thứ tự cắt ở §3 nếu dự toán GPU vượt ngân sách.
- Cuối tuần 2: pipeline chưa ổn định thì cắt hết phần mở rộng và cắt E2-half. Luôn giữ cặp E0-ft/E2 và đánh giá trên ảnh thật.
- Cuối tuần 3: khóa thiết kế, template và K.
- Tuần 5: nếu không cải thiện thì kiểm tra lại tính đúng của thí nghiệm và báo kết quả âm. Không đổi phương pháp sau khi đã xem test.

---

# 9. Phần mở rộng (chỉ chọn MỘT, chỉ khi tuần 5 còn dư)

| Mở rộng | Giới hạn |
|---|---|
| Full negative-label dưới paraphrase (§6.3) | Tập con query định nghĩa trên dev, báo là protocol bổ sung |
| Chẩn đoán VA-Count / Grounding DINO cho vấn đề 2 của thầy | Tối đa 2 ngày, tập ảnh nhỏ. Lưu box, exemplar thực sự đưa vào counter, density. Khi đổi query phải chạy lại phần phụ thuộc query (V3.3 §38–41) |
| T2ICount inference làm dòng tham chiếu | Dùng checkpoint công khai, không train |
| PairTally INTER | Chỉ dùng làm test, không tune |

---

# 10. Related work bắt buộc (bổ sung so với V3.3 §4)

- **RichCount** (arXiv 2505.15398): Eq. 14 đã kết hợp density supervision với consistency giữa các dạng text, và liên quan trực tiếp đến việc dùng nhiều dạng đầu vào văn bản. Đây là lý do V3.4 **không** nhận consistency là đóng góp. Nêu ở phần hướng phát triển.
- **PrACo** (WACV 2025), **PrACo++ / MUCCA** (Pacini et al., "Does it Really Count?", arXiv 2605.02752): evaluator và benchmark chính, chủ yếu là negative-label và distractor evaluation. Đã có số của CLIP-Count. Phần đồ án thêm vào là can thiệp bằng training và đánh giá có kiểm soát với paraphrase.
- **T2ICount** (CVPR 2025, thầy gửi): nhắm đúng vấn đề text sensitivity, FSC test MAE 11.76, tốt hơn CLIP-Count. Lý do chọn CLIP-Count là để làm thí nghiệm có đối chứng, không phải vì nó mạnh hơn.
- **CounTR, MGCAC, CountGD++**: nguồn gốc của mosaic.
- **CLIP-Count** (ACM MM 2023): mô hình nền.
- Các mô tả khác giữ như V3.3 §4.

---

# 11. Phần nào của V3.3 còn dùng được

File: `roadmap/ban_cu/CS331_ZSC_V3_3_Final.md`

| V3.3 | Trạng thái trong V3.4.2 |
|---|---|
| §6–8, §9.1–9.4, §9.6 (CLIP-Count, code, mosaic có sẵn) | **Dùng.** §9.5 được làm rõ ở §4.4. §9.7 bị thay bởi §5 |
| §16, §31–32 (thuộc tính giả, NPV, WPMAE) | **Dùng** cho §6, kèm quy tắc NPV chỉ trên target dương |
| §17 (tách họ prompt train/test) | Thay bằng dev/test ở §6.2 (không còn prompt train) |
| §10–12, §21–23, §25 (hard-pair, L_same, total loss, ablation E1/E3) | **Không dùng** (hướng phát triển) |
| §28, §28.1 (PrACo, cắm checkpoint) | **Dùng**, kèm §6.5 và quy tắc missing keys ở §7 |
| §33–37 (dataset, MUCCA, PairTally, seen/unseen) | **Dùng**, nhưng PairTally hạ xuống mở rộng |
| §38–43 (VA-Count, T2ICount) | Chỉ dùng khi chọn phần mở rộng tương ứng |
| §44–52 (scope, lịch 4 tuần, fallback) | **Thay** bởi §3, §8 |
| §53–55 (contribution, storyline slide) | Cần viết lại theo V3.4.2 ở tuần 6 |
| §56–57 (lộ trình học, file code phải đọc) | **Dùng** |
| §61 (bẫy code, môi trường, budget, checkpoint, Colab) | **Dùng, bắt buộc đọc trước khi chạy** |
| §62 (vị trí code) | **Dùng** |

---

# 12. Phân công (nhóm 2 người, đã xác nhận)

| Người | Phụ trách |
|---|---|
| A | Môi trường, vá code §4, fine-tune E0-ft/E2/E2-half, checkpoint, log |
| B | Dữ liệu và split, kiểm tra mosaic §4.3, bộ prompt §6, evaluator, cấu trúc kết quả §6.5, metric, bảng và hình |
| Cả nhóm | Kiểm tra nhãn, thống nhất protocol, related work, phân tích, báo cáo, slide |

Hai người giúp làm song song phần kỹ thuật nhưng không tăng ngân sách GPU hay số seed. Cả hai phải hiểu thiết kế chung và kiểm tra chéo phần của nhau.

Thống nhất trong tuần 1: schema file kết quả (dự đoán theo ảnh × query × cấu hình × seed × checkpoint × template) và cấu trúc thư mục ở §6.5.

---

# 13. Nội dung điền form

**Chủ đề:** Evaluating and Improving Target Sensitivity in Text-Guided Zero-Shot Object Counting

**Tóm tắt:**

Đề tài nghiên cứu hiện tượng mô hình Zero-Shot Object Counting chưa phân biệt đúng đối tượng cần đếm khi truy vấn văn bản thay đổi trên cùng một ảnh. Nhóm dùng CLIP-Count làm mô hình nền và khảo sát tác dụng của giám sát đa lớp bằng ảnh ghép (cross-class mosaic supervision). Cơ chế mosaic có sẵn trong mã nguồn được kích hoạt và điều chỉnh: xác suất sử dụng nhánh ghép ảnh từ nhiều ảnh nguồn khác nhãn được thay đổi có kiểm soát, tỉ lệ mẫu đa lớp thực tế được thống kê, đối chứng được giữ cùng lượng ảnh ghép và cách cắt ảnh, và chất lượng nhãn của các ô ghép được kiểm tra. Nhóm so sánh checkpoint gốc, mô hình fine-tune thông thường và các mô hình fine-tune với các mức can thiệp khác nhau. Việc đánh giá dùng FSC-147, các bài kiểm tra PrACo và tập ảnh đa lớp thật MUCCA, kết hợp sai số đếm với các chỉ số chọn đúng đối tượng. Nhóm bổ sung đánh giá có kiểm soát với các cách diễn đạt tương đương, để kiểm tra hiệu quả chọn đúng đối tượng sau fine-tune còn duy trì khi truy vấn thay đổi cách viết hay không. Sản phẩm gồm mã nguồn, notebook tái lập, kết quả thực nghiệm, phân tích lỗi, báo cáo và demo. Mục tiêu là kiểm chứng khả năng cải thiện độ nhạy theo đối tượng và làm rõ giới hạn của phương pháp.

**Tài liệu tham khảo chính (2024–2026):**

- Ciampi et al., *Mind the Prompt: A Novel Benchmark for Prompt-based Class-Agnostic Counting*, WACV 2025. https://arxiv.org/abs/2409.15953
- Qian et al., *T2ICount: Enhancing Cross-modal Understanding for Zero-Shot Counting*, CVPR 2025. https://arxiv.org/abs/2502.20625
- Pacini et al., *Does it Really Count? Assessing Semantic Grounding in Text-Guided Class-Agnostic Counting*, arXiv 2026. https://arxiv.org/abs/2605.02752

(Báo cáo đầy đủ vẫn trích CLIP-Count, RichCount và các nguồn của mosaic.)
