# CS331 UIT — Zero-Shot Object Counting
## V3.3 — Bản chốt để làm (Prompt Robustness + Target Sensitivity)

**Tên đề tài (khuyên dùng, chờ thầy duyệt):**

> **Stable to Wording, Sensitive to Targets: Improving Query Fidelity in Text-Guided Zero-Shot Object Counting**

Phương án dự phòng (nếu cần tên kỹ thuật hơn):

> Improving Query Fidelity in Zero-Shot Object Counting via Cross-Class Mosaic Supervision and Prompt Consistency

Không dùng: *"Evaluating Query Fidelity through Grounding-to-Counting Consistency…"* (lệch trọng tâm sang VA-Count; CLIP-Count không có bước grounding; chữ "Evaluating" làm mất phần phương pháp; dễ bị đánh đồng với PrACo++).

**Trạng thái:** V3.3 = V3.2 + sửa theo review `CS331_BaoCao_Review_V3_2.md` (25/09, đã đối chiếu từng điểm với code và link). **V3.3.1 (26/09)** = vá nhỏ theo `CS331_BaoCao_Review_V3_3.md`, xem changelog ngay dưới. Research direction **không đổi** so với V3.1. Các bản cũ (Zero-to-Hero, V2, V3, V3.1, V3.2) nằm trong `roadmap\ban_cu\`, chỉ để tham khảo; **roadmap Zero-to-Hero (VA-Count + Region loss) đã lỗi thời.**

**Việc còn mở:**
- [ ] **Xác nhận hạn nộp** với thầy/lớp. Roadmap 4 tuần ở §48–51 giả định còn ≥4 tuần. Nếu ít hơn, cắt theo §52.
- [ ] Thầy duyệt tên đề tài.

---

# 0. Changelog V3.1 → V3.2

| Mục | Thay đổi | Lý do |
|---|---|---|
| Đầu file | Chốt tên đề tài | Handoff 23/09 |
| §9 | Thêm 9.4–9.7: tỉ lệ mosaic hiệu dụng, null-mosaic có sẵn, viền Gauss, scale | Đọc lại `util/FSC147.py:304–401` |
| §17 | Tách prompt theo *template* trong từng họ + họ E để riêng | Báo được 2 số: seen-family / unseen-family |
| §21 | L_same dạng teacher–student (detach nhánh tên lớp), áp cho ~30% batch | Chi phí 2 forward + tránh trùng lặp với MSE |
| §22 | Null-query = mosaic toàn tile âm (không phải random negative trên ảnh đơn) | Giữ đúng §44 |
| §25 | Thêm control **E1-aug** (paraphrase augmentation, không L_same) | Trả lời câu "L_same có hơn augment prompt không?" |
| §30 | Bỏ CPL | FSC-147/MUCCA chỉ có point, không tính được vùng |
| §38–41 | VA-Count: đo recall trên PairTally, slide riêng, kết luận theo số đo | Đụng trực tiếp vấn đề 2 của thầy |
| §61 (mới) | Implementation notes: 3 bẫy code khi fine-tune, môi trường, seed, budget | Đã kiểm tra dòng code thật |
| §62 (mới) | Vị trí code trên máy | — |
| §63 (mới) | Góp ý review đã **không** đưa vào và lý do | Tránh bị hỏi lại |
| §4.8, §6, §43 (25/09 chiều) | T2ICount thành related work trực tiếp; sửa lý do chọn CLIP-Count (không nói "hiệu quả hơn") | T2ICount nhắm đúng vấn đề text sensitivity, MAE 11.76 < 17.78 |
| §33, §46 (25/09 chiều) | Thêm FSC-147-S-v2 (230 ảnh) + T2ICount inference-only làm SHOULD HAVE | Rẻ, thầy đã gửi link T2ICount |
| §21.2 (25/09 chiều) | Sửa câu chữ VRAM: phải đo trước; k mẫu cố định mỗi batch | "Bắt buộc 30%" là chưa có căn cứ |
| §61.8–61.9 (mới) | Đường dẫn data hardcode; bảng 3 con số baseline khác nhau | Chuẩn bị chạy E0 |
| §64 (mới) | Đánh giá chốt + checklist bắt đầu | — |

## Changelog V3.2 → V3.3 (theo review 25/09)

| Mục | Thay đổi | Nguồn |
|---|---|---|
| §61.4, §64.2 | **`pip install "numpy<2"` + restart runtime trước mọi thứ** (imgaug 0.4.0 crash với NumPy 2, mà `FSC147.py:18` import imgaug) | Review 5.1 |
| §9.5 | Null-mosaic ≈ 1.5% toàn tập, chưa chắc density = 0 | Review 5.2, đã kiểm `FSC147.py:370` |
| §9.7 | Hệ số scale 0.55–0.93 | Review 5.2 |
| §18, §61.2 | Sửa lý do: `run.py:157–158` là code chết | Review 5.2, đã kiểm `run.py:150–202` |
| §15 | Khớp với §17 | Review 5.3 |
| §23 | Bỏ λ_m (mosaic chỉ đổi dữ liệu) | Review 5.3 |
| §11.1 (mới) | Hai loại cặp: hard-pair (gần) vs null-mosaic (xa) | Review 5.3 |
| §20, §48 | Bỏ nhãn "V3.1" còn sót | Review 5.3 |
| §21.4 (mới) | q2 sinh trong `training_step`; **không dùng `prompt_add`** (bị lỗi index) | Review 5.4 + mình kiểm thêm `util/CLIP_caption.py` |
| §25 | E1-aug dùng cùng k mẫu, cùng pool template với E1 | Review 5.4 |
| §24.1 (mới) | Limitation: text encoder CLIP bị đóng băng | Review 5.4 |
| §31.1 (mới) | NPV đo trên tập nào + cách đo **cùng lúc** hai vế (paraphrase-PrACo, scatter NPV–CntF1) | Review 5.4 |
| §45 | Bootstrap CI thành MUST cho MUCCA (200 ảnh) và FSC-147-S-v2 | Review 6 |
| §48 Day 5 | Đo thời gian mỗi epoch ngay tuần 1 | Review 5.4 |
| §4.2, §4.6, §4.7, §6, §59 | Sửa tên/venue bài báo; MUCCA đã có trên Zenodo; repo PrACo có sẵn wrapper CLIP-Count | Review 6 + mình kiểm lại link |

## Changelog V3.3 → V3.3.1 (26/09, theo `CS331_BaoCao_Review_V3_3.md`)

Không đổi hướng, không đổi thiết kế thí nghiệm. Chỉ thêm bẫy môi trường, chi tiết cách chạy PrACo/MUCCA và sửa lỗi nhỏ. Mọi điểm đã đối chiếu lại với code/link ngày 26/09.

| Mục | Thay đổi | Đã kiểm |
|---|---|---|
| §61.4, §64.2 | Cell đầu: `pip install "numpy<2" "setuptools<81"` rồi restart | `pkg_resources` bị **xoá ở setuptools 82.0.0** (08/02/2026, changelog chính thức). Bản 81 vẫn còn, nhưng review chỉ thử 80.10 → giữ `<81` cho chắc |
| §4.2, §48 Day 6 | MUCCA: metadata đã có sẵn trong repo PrACo, chỉ cần bỏ ảnh vào `data/multiclass-dataset/images/` | Đã xem thư mục repo + default `--img_directory` của `multiclass_main.py` |
| §4.2, §58, §64.1 | **CLIP-Count CÓ trong bảng của PrACo++** (Table 1 FSC test, Table 2 FSC val, Table 3 MUCCA) → đóng việc "còn phải xác nhận" | Đọc bản HTML arXiv 2605.02752 |
| §28.1 (mới), §32.2, §57 | Cách cắm checkpoint E0-ft…E3 vào PrACo + **2 bẫy mới**: `strict=False` và checkpoint "filtered" mặc định | `models/clipcount_model.py`, `models/loader.py` (nhánh `master`) |
| §61.5 | Lý do chọn LR 1e-5 + nhắc: chưa vá bẫy 1 thì `--lr` cũng bị bỏ qua | `run.py:81, 400–407` |
| §49, §58, §62 | Sửa nhãn cũ (cách chia prompt, "V3.2", tên branch, cây thư mục) | — |
| §4.6 | Số liệu MixCount (−20.14% / −18.3% MAE) | Đã khớp với abstract |

---

# 1. Research Question chính

Một text-guided Zero-Shot Object Counting model tốt cần đồng thời có hai tính chất:

## 1.1. Ổn định khi đổi cách diễn đạt

Ví dụ cùng một đối tượng:

```text
apple
apples
the apples
all apples in the image
objects belonging to the apple category
how many apples are visible?
```

Prediction nên gần nhau.

Đây là:

> **Prompt Robustness**

## 1.2. Nhạy khi đổi đối tượng cần đếm

Cùng một ảnh:

```text
8 apples
3 oranges
```

Prompt:

```text
apple  → ~8
orange → ~3
```

không nên:

```text
apple  → 8
orange → 8
```

Đây là:

> **Target / Query Sensitivity**

---

# 2. Câu hỏi nghiên cứu đề xuất

> **Can a text-guided zero-shot counter remain invariant to semantically equivalent prompt formulations while remaining discriminative when the requested target changes?**

Tiếng Việt:

> Mô hình đếm zero-shot dùng văn bản có thể vừa ổn định trước các cách diễn đạt tương đương, vừa đủ nhạy khi đối tượng cần đếm thực sự thay đổi hay không?

---

# 3. Cốt lõi của hướng nghiên cứu

```text
SAME TARGET
different wording
→ stable

DIFFERENT TARGET
same image
→ discriminative
```

Hai tính chất này phải được đánh giá cùng nhau.

Nếu chỉ tối ưu robustness thì model bỏ qua text hoàn toàn vẫn có thể cho mọi prompt cùng output và đạt điểm ổn định rất đẹp.

Nếu chỉ tối ưu sensitivity thì model có thể phân biệt apple/orange nhưng lại dao động mạnh khi cách diễn đạt của cùng một target thay đổi.

---

# 4. Related Work bắt buộc phải cite

## 4.1. PrACo — WACV 2025

**Mind the Prompt**

Đã nghiên cứu việc prompt-guided counting models có thực sự nghe prompt hay không.

Có:
- negative-label test;
- mosaic / distractor evaluation.

Vì vậy không claim:

> “Chúng tôi là người đầu tiên kiểm tra model có nghe prompt hay không.”

## 4.2. PrACo++ / MUCCA — arXiv 2026 (chưa có venue)

**Does it Really Count? Assessing Semantic Grounding in Text-Guided Class-Agnostic Counting** (Pacini, Ciampi, Messina, Tonellotto, Amato, Falchi; arXiv 2605.02752)

Có các metric:

```text
NMN
PCCN
CntP
CntR
CntF1
```

và benchmark 10 model. Repo PrACo có sẵn wrapper cho CLIP-Count, ZSC, CounTX, VLCounter, DAVE, PseCo, CountGD, CountGD++… (đã kiểm README 25/09). **Đã xác nhận (26/09): CLIP-Count có trong Table 1 (FSC test), Table 2 (FSC val) và Table 3 (MUCCA) của paper.** Trên MUCCA paper báo NMN, PCCN, CntP, CntR, CntF1, GAME(1), MAE, RMSE → có số CLIP-Count để đối chiếu khi chạy lại.

Ngoài synthetic test còn có **MUCCA** để đánh giá trên ảnh thật có nhiều object category:
- Zenodo, bản 1.0 (26/03/2026), CC BY 4.0, `MUCCA_1.0.zip` 30.9 MB: https://zenodo.org/records/19231375
- **Chỉ 200 ảnh**; annotation dạng point + class id.
- Code đánh giá: `multiclass_main.py`, `multiclass_main_statistics.py` trong repo PrACo. README chưa hướng dẫn → phải đọc code.
- **V3.3.1:** repo PrACo **đã có sẵn metadata** trong `data/multiclass-dataset/` (`multiclass_split_images.json`, `multiclass_split_classes.json`, `multiclass_image_classes.txt`, `annotations_no_scaling.json`, `class_mapping.json`, `multiclass_gt_counts.json`…). Chỉ cần giải nén **ảnh** từ zip Zenodo vào `data/multiclass-dataset/images/` (default `--img_directory` của `multiclass_main.py`). Tên thư mục bên trong zip chưa kiểm → kiểm khi giải nén.

## 4.3. CounTR — BMVC 2022

CLIP-Count ghi rõ FSC-147 implementation được kế thừa từ CounTR.

CounTR đã có mosaic-style augmentation.

Do đó nếu dùng mosaic phải cite CounTR.

## 4.4. MGCAC — ACCV 2024

**A Recipe for CAC: Mosaic-based Generalized Loss for Improved Class-Agnostic Counting**

Đã dùng mosaic augmentation để tạo distractor / multi-class supervision.

Không claim mosaic là mới.

## 4.5. CountGD++ — CVPR 2026

CountGD++ train trên FSC-147 cộng synthetic mosaic data để tạo positive / negative prompt supervision.

Không claim multi-class mosaic supervision là first-ever.

## 4.6. MixCount — arXiv 2026 (bài dataset)

**The MixCount Dataset: Bridging the Data Gap for Open-Vocabulary Object Counting** (arXiv 2605.18063).

Đây là **bài dataset**: pipeline tự động sinh ảnh tổng hợp nhiều loại vật, có mô tả text chi tiết và nhãn đếm chính xác. Train model SOTA trên đó giảm MAE 20.14% trên FSC-147 và 18.3% trên PairTally.

Cite khi thảo luận multi-object supervision. Điểm khác: MixCount tạo dữ liệu tổng hợp mới; đồ án chỉ tái dùng ảnh thật FSC-147 qua mosaic.

## 4.7. PairTally — DICTA 2025

**Can Current AI Models Count What We Mean, Not What They See? A Benchmark and Systematic Evaluation** (arXiv 2509.13939). Trích theo tên này; "PairTally" là tên benchmark.

681 ảnh, gồm ảnh có hai nhóm object:

```text
INTER
INTRA
```

phù hợp để đánh giá target discrimination thật.

## 4.8. T2ICount — CVPR 2025 (thầy đã gửi link)

**T2ICount: Enhancing Cross-modal Understanding for Zero-Shot Counting** (arXiv 2502.20625, repo `cha15yq/T2ICount`).

Đã làm gì (theo abstract + README, đã kiểm tra 25/09):
- Chỉ ra các model dựa trên CLIP có *"limited sensitivity to text prompts"*. Đây **gần như đúng vấn đề 3 của thầy** và vế Target Sensitivity của đề tài.
- Backbone: **Stable Diffusion v1.5**, khử nhiễu một bước.
- Đề xuất **Hierarchical Semantic Correction Module** và **Representational Regional Coherence Loss** (lấy cross-attention map từ U-Net làm tín hiệu giám sát).
- Tạo **FSC-147-S**: tập con FSC-147 gán nhãn lại, nhắm vào vật thiểu số để lộ ra model không nghe text. Repo phát hành **v2, 230 ảnh**.
- Có **checkpoint công khai**. README báo FSC test MAE **11.76**, tốt hơn CLIP-Count (17.78 trong paper) rất nhiều.

Viết trong related work:

> T2ICount cải thiện độ nhạy với text bằng backbone diffusion và đạt MAE tốt hơn, nhưng chi phí train cao, khó chạy một ablation có kiểm soát (E0-ft/E1-aug/E1/E2/E3, nhiều seed) với tài nguyên Colab. CLIP-Count nhẹ, đã có trong benchmark PrACo++, và cho phép tách riêng tác dụng của từng can thiệp lúc train. Ngoài ra T2ICount không đo độ bền khi đổi cách diễn đạt (Gap A) và không đánh giá trade-off giữa robustness và sensitivity (Gap B).

**Không viết:** "CLIP-Count hiệu quả hơn T2ICount", "hướng của chúng tôi hiệu quả hơn". Mục tiêu của đồ án là **phân tích can thiệp lúc train**, không phải SOTA.

---

# 5. Khoảng trống hợp lý còn lại

## Gap A — Robustness với paraphrase cùng nghĩa

PrACo / PrACo++ tập trung mạnh vào:

```text
correct target
negative target
distractor
multi-class grounding
```

Nhưng không tập trung chính vào controlled paraphrase robustness:

```text
same semantic target
different wording
```

## Gap B — Đo robustness và sensitivity đồng thời

Mục tiêu:

```text
same target
→ invariant

different target
→ discriminative
```

Đây là framing trung tâm.

(T2ICount và PrACo++ đều chỉ nhìn vế sensitivity; chưa bài nào báo đồng thời sensitivity và paraphrase robustness trên held-out prompt.)

## Gap C — Training intervention trên CLIP-Count

Không chỉ benchmark.

Thử kết hợp:

```text
Cross-class Mosaic Supervision
+
Equivalent-Prompt Consistency
```

trên CLIP-Count.

Không dùng từ:

```text
first
novel mosaic
first multi-class supervision
```

Nên dùng:

```text
investigate
reactivate
extend
adapt
combine
```

---

# 6. Model chính: CLIP-Count

Repository:

https://github.com/songrise/CLIP-Count

Lý do chọn:
- text embedding đi trực tiếp vào model;
- text tham gia visual encoder / decoder interaction;
- nhẹ hơn T2ICount nhiều (không cần Stable Diffusion), nên chạy được ablation 5–6 cấu hình × nhiều seed trên Colab. **Lưu ý:** T2ICount có MAE tốt hơn; lý do chọn là khả năng làm thí nghiệm có kiểm soát, không phải độ chính xác (§4.8);
- repo PrACo có sẵn wrapper CLIP-Count (đã kiểm), nên chạy được PrACo/MUCCA cho E0–E3 mà không phải tự viết evaluator;
- sửa được training loss;
- sửa được FSC-147 dataloader;
- phù hợp trực tiếp với nghiên cứu query fidelity.

---

# 7. Phát hiện quan trọng trong code CLIP-Count

Trong:

```text
util/FSC147.py
```

có:

```python
self.use_out_mosaic = False
```

Tức official config đang tắt nhánh cross-image / cross-class mosaic.

Mặc định code vẫn có self-mosaic.

---

# 8. Cross-class mosaic đã tồn tại sẵn trong code

Khi:

```python
self.use_out_mosaic = True
```

code có nhánh lấy tile từ các ảnh khác.

Nếu class tile khác target class thì:

```text
GT density của tile đó = 0
```

Đây chính là selective supervision mà V3 định xây E2.

Do đó phải viết trung thực:

> **The official CLIP-Count code contains a disabled cross-image mosaic branch inherited from CounTR. We reactivate and extend this mechanism to study its effect on query sensitivity.**

Không viết:

> “We propose cross-class mosaic.”

---

# 9. Một số giới hạn của mosaic có sẵn

## 9.1. Không đảm bảo 4 tile là 4 class khác nhau

Các ảnh phụ được lấy ngẫu nhiên.

## 9.2. Có điều kiện count < 70

Nhánh cross-class chỉ chạy trong một số trường hợp.

Ảnh đông object có thể quay lại self-mosaic.

## 9.3. Tile bị resize nhỏ

Mỗi tile sau xử lý có kích thước xấp xỉ 192×192 trước khi ghép vào output lớn hơn.

Object nhỏ có nguy cơ bị shrink mạnh.

## 9.4. Tỉ lệ mosaic hiệu dụng rất thấp (đã đọc code)

`FSC147.py:238–245`: chỉ khi `aug_p < 0.3` mới vào nhánh mosaic. `FSC147.py:321`: nếu ảnh có ≥70 vật thì luôn rơi về self-mosaic. Vậy dù bật `use_out_mosaic`, **tối đa ~30% sample** là cross-class mosaic, và thấp hơn nữa sau khi loại ảnh đông vật.

→ Phải **log tỉ lệ cross-class thực tế** mỗi epoch. Tỉ lệ mosaic là một hyperparameter của E2/E3, cần chốt trước khi chạy (xem §61.5).

## 9.5. Null-mosaic đã có sẵn

`FSC147.py:338–342`: **trong nhánh cross-class**, với xác suất 0.25 × 1/5 = 5%, `gt_pos = 4`, tức **không tile nào lấy từ ảnh của query**.

Sửa lại theo review (V3.3):
- **Tỉ lệ thực tế trên toàn tập ≈ 0.3 × 5% ≈ 1.5%**, và còn thấp hơn vì chỉ ảnh < 70 vật mới vào nhánh này (§9.4).
- **Density chưa chắc bằng 0**: 4 tile phụ được lấy ngẫu nhiên, và nếu tile nào trùng lớp với query thì `FSC147.py:370–373` vẫn giữ density của tile đó. GT vẫn **đúng** theo nhãn lớp, chỉ là không phải lúc nào cũng là null-query thật.

→ Muốn dùng null-mosaic như một can thiệp (§22.1) thì phải **sửa sampler ở `FSC147.py:352`** để chủ động chọn tile khác lớp, và log tỉ lệ null thực tế.

## 9.6. Viền Gauss: không phải vấn đề

Code đặt dot lên từng tile, ghép cả canvas, **rồi mới** `gaussian_filter` (σ=1) ở `FSC147.py:401`. Không có vệt Gauss bị cắt cụt ở mép tile.

Artifact nhỏ còn lại (ghi vào limitations, không sửa):
- vật bị cắt đôi ở mép tile vẫn tính là 1 nếu tâm nằm trong tile;
- ảnh được blend mượt 10–20px ở đường ghép, còn density thì cắt thẳng.

## 9.7. Lệch scale do 2×2

Nhánh cross-class: crop cạnh 250–384px, resize về `resize_l = 192 + 2·blending_l` (212–232px), phần hiển thị mỗi tile là 192px. Hệ số scale = `resize_l / length` ≈ **0.55–0.93** (vật bị co). Nhánh self-mosaic crop 150–384px nên hệ số ≈ 0.55–1.55 (có thể phóng to).

Code gốc vốn đã chạy self-mosaic 2×2 (30%) và affine scale 0.8–1.2, nên đây không phải rủi ro mới.

**Quyết định:** giữ 2×2. Chỉ thử bố cục 1×2 giữ scale nếu **E2 tệ hơn E0-ft trên MUCCA/PairTally**.

---

# 10. Phần mở rộng mosaic nên nghiên cứu

Không rewrite toàn bộ nếu chưa cần.

Bắt đầu bằng:

```text
reactivate existing branch
```

sau đó thử:
- bỏ / sửa điều kiện object count;
- random horizontal layout;
- random vertical layout;
- random 2×2 layout;
- random split ratio;
- kiểm tra scale của object nhỏ;
- hard-pair sampling một phần.

---

# 11. Hard-pair Mosaic

Random pair thường tạo cặp dễ:

```text
car ↔ strawberry
dog ↔ book
```

Nên bổ sung một tỷ lệ hard pair.

Gợi ý:

```text
70% random different-class
30% hard different-class
```

Hard pair chọn dựa trên:

\[
s(A,B)=\cos(e_A,e_B)
\]

với CLIP text embedding.

Nhưng phải filter để loại:

```text
synonym
near-synonym
ambiguous label
semantic overlap
```

Ví dụ `cup / mug` có thể không phải negative class đủ sạch.

## 11.1. Hai loại cặp, hai mục đích (V3.3)

| Loại | Chọn cặp thế nào | Dùng cho | Rủi ro nhãn |
|---|---|---|---|
| **Hard-pair** | Cosine CLIP **cao** nhưng không đồng nghĩa, **kiểm tay** danh sách cặp | Mosaic có tile đúng lớp + tile lớp gần → dạy phân biệt khó | Cao hơn: tile lớp gần dễ chứa target không gán nhãn → phải kiểm tay |
| **Null-mosaic** | Cosine CLIP **thấp** (xa về ngữ nghĩa) | Mosaic không có tile đúng lớp → dạy "không có thì đếm 0" | Thấp, vì lớp xa ít khi xuất hiện chung |
| Random (mặc định) | Ngẫu nhiên | Phần còn lại | Trung bình |

Hai danh sách cặp này **tách riêng**, sinh một lần ở tuần 2, lưu thành file (ví dụ `pairs_hard.json`, `pairs_far.json`) để mọi E dùng chung.

---

# 12. Không để model học shortcut đường ghép

Nếu train chỉ:

```text
left = positive
right = negative
```

model có thể học shortcut.

Do đó random:

```text
horizontal
vertical
2×2
positive tile position
crop ratio
```

Và bằng chứng quan trọng phải đến từ:

```text
PairTally
MUCCA
```

là ảnh thật.

---

# 13. Prompt robustness: bộ prompt đơn giản là chưa đủ

Các prompt:

```text
apple
apples
the apples
all apples in the image
```

có thể có CLIP embedding quá gần nhau.

Nếu vậy:

```text
NPV ≈ 0
```

ngay cả trước khi train.

Khi đó benchmark quá dễ.

---

# 14. P0 bắt buộc cho prompt benchmark

Ngay tuần 1:

## P0-A
Tạo candidate prompt families.

## P0-B
Tính CLIP cosine similarity giữa các prompt.

## P0-C
Chạy official CLIP-Count checkpoint với các prompt này.

## P0-D
Đo NPV của baseline E0.

Nếu:

```text
NPV gần 0
```

thì redesign prompt set ngay.

---

# 15. Prompt families

Không train và test trên cùng một kiểu prompt.

**V3.3:** cách chia train/test theo §17. Họ A–D **đều có** template train và template test; chỉ họ E là test hoàn toàn. (Nhãn "TRAIN / HELD-OUT" bên dưới là cách chia cũ của V3.1, giữ lại chỉ để minh hoạ các họ.)

Lưu ý: tên lớp FSC-147 phần lớn **đã ở số nhiều** ("sea shells", "hot air balloons") → template số ít/số nhiều của họ A phải map tay hoặc dùng thư viện chia số (ví dụ `inflect`) rồi kiểm tay.

## TRAIN FAMILIES (cách chia V3.1, đã thay bằng §17)

### Family A — morphology / article

```text
apple
apples
the apples
```

### Family B — simple templates

```text
all apples
apple objects
objects of class apple
```

## HELD-OUT TEST FAMILIES (cách chia V3.1, đã thay bằng §17)

### Family C — noun phrase paraphrases

```text
instances belonging to the apple category
objects identified as apples
```

### Family D — natural requests

```text
how many apples are visible?
count the apples in the image
```

### Family E — LLM-generated paraphrases

Sau đó manual filter để đảm bảo semantic equivalence.

---

# 16. Không thêm visual attribute giả

Nếu GT target chỉ là:

```text
apple
```

thì không tự đổi thành:

```text
red apples
large apples
apples on the left
```

vì có thể không còn equivalent target.

Prompt paraphrase phải đổi cách diễn đạt, không đổi điều kiện chọn object.

---

# 17. Train/Test prompt phải tách họ

**V3.2: tách theo template, không chỉ theo họ.**

Mỗi họ A–D có một pool template. Chia template của **mỗi họ** thành train/test. Họ E (LLM sinh + lọc tay) để riêng hoàn toàn cho test.

```text
TRAIN
một phần template của A, B, C, D

TEST — seen family
template còn lại của A, B, C, D

TEST — unseen family
toàn bộ Family E
```

Báo **2 số NPV/WPMAE**: diễn đạt mới trong họ đã gặp và họ chưa gặp. Như vậy nếu E1/E3 cải thiện held-out paraphrase robustness thì mới có ý nghĩa, và biết được nó tổng quát tới mức nào.

Không train `L_same` trên đúng prompt variants rồi dùng chính chúng để báo NPV.

**Kiểm tra ở P0 (§14):** nếu cosine CLIP giữa prompt train và tên lớp > ~0.95 thì L_same gần như không có tín hiệu → phải thêm template xa hơn.

---

# 18. Lưu ý về `"a photo of {}"`

Sau khi đọc `run.py`, không nên mặc định wrap prompt bằng:

```text
a photo of {prompt}
```

Đã kiểm lại `run.py` (V3.3):

- **Train:** `run.py:155` forward với prompt thô. Dòng 157–158 (bọc "a photo of" khi `use_contrast=False`) nằm **sau** forward và `prompt_gt` không được dùng lại → **code chết**, không ảnh hưởng gì.
- **Validation:** `run.py:206–207` bọc "a photo of" **nếu** `use_contrast=False`. Mặc định `use_contrast=True` nên không bọc.
- **Test:** `test_step` không bao giờ bọc.

Vậy với config mặc định, model **luôn nhận prompt thô**. Tắt `use_contrast` chỉ làm lệch prompt ở validation (tức chọn checkpoint theo val_mae với prompt khác lúc train/test).

Do đó protocol đúng là:

> **Giữ đúng prompt preprocessing của official checkpoint / config. Không tự thêm `"a photo of {}"` nếu baseline chính thức không làm vậy.**

Nếu nghiên cứu wrapper thì phải coi đó là experiment riêng.

---

# 19. Một correction quan trọng khác

Default:

```text
coop_width = 2
```

không phải 22.

---

# 20. Core Method

```text
CLIP-Count
+
Cross-class Mosaic Supervision
+
Equivalent-Prompt Consistency
```

---

# 21. L_same

Với hai prompt cùng target:

```text
q1
q2
```

Ta muốn:

\[
D_{q_1}\approx D_{q_2}
\]

Ví dụ:

\[
L_{same}=\|D_{q_1}-D_{q_2}\|_1
\]

hoặc MSE.

## 21.1. Thiết kế cụ thể (V3.2)

**Teacher–student:**
- `q1` = tên lớp gốc (prompt mà checkpoint official quen). Nhánh này nhận `L_density` với GT và được **detach** khi tính L_same.
- `q2` = paraphrase lấy từ pool train (§17). Nhánh này **chỉ** nhận L_same, không nhận MSE với GT.

\[
L_{same}=\|\,\mathrm{sg}(D_{q_1})-D_{q_2}\|_1
\]

Lý do không cho `q2` nhận MSE với GT: nếu cả hai nhánh cùng regress về một GT thì L_same gần như bị ngầm thực hiện. Trường hợp đó được tách thành control riêng là **E1-aug** (§25).

## 21.2. Chi phí

Visual encoder của CLIP-Count **nhận text embedding** (`models/clip_count.py:139`, `deep_vpt_forward(x, text_embedding)` ở dòng 291). Vì vậy **không cache được đặc trưng ảnh** giữa hai prompt, mà phải chạy 2 forward đầy đủ.

Mặc định CLIP bị đóng băng (`unfreeze_vit=False`), nhưng gradient vẫn đi xuyên qua ViT để tới VPT và CoOp. Vì vậy activation của nhánh thứ hai vẫn phải lưu lại, và bộ nhớ tăng đáng kể.

Cách làm:
- Áp L_same cho **k mẫu cố định mỗi batch** (ví dụ k = 10/32 ≈ 30%), không chọn ngẫu nhiên theo tỉ lệ. Như vậy bộ nhớ ổn định từng bước. Mục đích chính là **tiết kiệm thời gian**.
- **Đo VRAM trước** (1 epoch ngắn, batch 32, fp16 như mặc định `run.py:466`) ngay ngày đầu tuần 3. Chưa đo thì chưa biết có tràn T4 16GB hay không.
- Nếu tràn: **giảm `--batch_size` và tăng `--accum_iter` cùng lúc** (ví dụ 16 × 2) để giữ batch hiệu dụng 32. Chỉ tăng `accum_iter` mà không giảm batch thì **không** đỡ bộ nhớ.
- Cặp `batch_size × accum_iter` phải **giống nhau cho mọi E**, kể cả E0-ft và E1-aug (vốn không cần forward thứ hai).

## 21.3. Bẫy λ

λ quá lớn → mọi density map phẳng giống nhau, L_same ≈ 0 mà đếm sai. MSE với GT ở nhánh `q1` giữ model lại, nhưng vẫn phải:
- log riêng `L_density` và `L_same`;
- theo dõi MAE song song với NPV;
- quét λ trên FSC-147 val, không trên tập test.

## 21.4. q2 được sinh ở đâu (V3.3)

Dataloader chỉ trả tên lớp (`FSC147.py:94`), nên q2 phải sinh **trong `training_step`**:

```text
prompt_gt (tên lớp)
→ tra bảng class → danh sách template TRAIN (§17)
→ chọn ngẫu nhiên 1 template cho mỗi mẫu trong k mẫu
→ q2 = template.format(class)
```

Bảng template lưu thành file (ví dụ `prompts/train_templates.json`), sinh một lần ở tuần 2 và dùng chung cho E1-aug, E1 và E3.

**KHÔNG dùng `prompt_add`**, dù dataloader có trả thêm biến này (`FSC147.py:96, 119`; `run.py:152`). Nó lấy từ `util/CLIP_caption.pkl`, và script sinh ra nó (`util/CLIP_caption.py`) bị **lỗi index**: lấy chỉ số trong danh sách `close_prompt` nhưng tra trên toàn bộ corpus. Kết quả là rác, ví dụ "hot air balloons" → `["glass", "design pattern", "Animal Husbandry", "gaming keyboard", "sphere"]` (xem `util/CLIP_caption.json`). Code gốc cũng không dùng biến này lúc train.

---

# 22. Mosaic supervision

Nếu ghép:

```text
Image A → class A
Image B → class B
```

và hỏi class A:

```text
GT density của A tile = density A
GT density của B tile = 0
```

Nếu hỏi class B thì ngược lại.

Không cần random negative class không xác minh.

## 22.1. Null-query (V3.2)

Null-query ("hỏi orange trên ảnh chỉ có táo → density ≈ 0") nhắm thẳng vào vấn đề 3 của thầy. Nhưng làm theo kiểu **random negative trên ảnh FSC-147 đơn** là **không** được (§44 vẫn giữ), vì ảnh FSC-147 có thể chứa vật lớp Y mà không được gán nhãn → dạy model sai.

Cách làm: dùng **null-mosaic** (toàn bộ tile thuộc lớp khác target, chọn từ danh sách cặp **xa** ở §11.1). Code gốc chỉ có khoảng 1.5% và chưa chắc là null thật (§9.5), nên muốn dùng thì phải sửa sampler. Có thể tăng tỉ lệ này như một mức của E2 (SHOULD HAVE).

Ba bẫy phải xử lý:
1. **Nhãn bẩn:** tile lớp khác vẫn có thể chứa target không gán nhãn. Ưu tiên cặp lớp **xa về ngữ nghĩa** (cosine CLIP thấp), loại cặp gần đồng nghĩa (cup/mug).
2. **Sụp về "đoán thấp":** giữ tỉ lệ null-mosaic nhỏ, theo dõi MAE trên ảnh dương.
3. **Rò rỉ đánh giá:** null-mosaic rất giống negative-label test của PrACo → NMN sẽ đẹp một phần vì đã "học đúng dạng bài test". **Phải ghi rõ trong báo cáo**, và dựa vào MUCCA/PairTally để kết luận.

---

# 23. Total loss

\[
L=L_{density}+\lambda_sL_{same}
\]

Trong đó:
- `L_density`: MSE density như code gốc (`run.py:164–166`), tính trên **batch đã qua mosaic hay không** tuỳ E. Mosaic chỉ **thay đổi dữ liệu và GT** (tile lớp khác có GT = 0), không thêm số hạng loss nào.
- `L_same`: prompt consistency (§21.1), chỉ trên k mẫu.

(V3.3: bỏ `λ_m·L_mosaic` của V3.1 vì không có loss mosaic riêng. Tỉ lệ mosaic là hyperparameter của dữ liệu, xem §61.5.)

---

# 24. Không kết luận quá mạnh về density supervision

Nếu mosaic cải thiện sensitivity, có thể nói:

> Single-class supervision is an important contributor to query insensitivity, and density-map regression can still support selective counting when explicit multi-class supervision is introduced.

Không nói:

> Density map không phải vấn đề.

## 24.1. Limitation: text encoder bị đóng băng (V3.3)

`models/clip_count.py:73`: `self.clip.requires_grad_(False)`. Text encoder và image encoder của CLIP bị đóng băng; chỉ có context token CoOp (`coop_width=2`), VPT và decoder được học.

Hệ quả:
- Hai paraphrase đi qua **cùng một text encoder cố định**, chỉ khác nhau ở token. Model chỉ học được bất biến qua 2 context token dùng chung, VPT và decoder → **tác dụng của L_same có thể nhỏ**.
- Nếu E1 ≈ E0-ft thì đây là một **phát hiện**, không phải thất bại: "với text encoder đóng băng, consistency loss ở đầu ra khó sửa được độ nhạy với cách diễn đạt".
- Ghi vào limitations. Không mở khoá text encoder trong scope chính (tốn compute, dễ phá alignment của CLIP).

---

# 25. Ablation mới — phải có E0-ft

Nếu E1/E2/E3 đều fine-tune từ checkpoint E0 thì phải thêm control:

| ID | Extra Fine-tune | Paraphrase có MSE với GT | L_same | Cross-class Mosaic |
|---|---:|---:|---:|---:|
| E0 | ✗ | ✗ | ✗ | official behavior |
| E0-ft | ✓ | ✗ | ✗ | official behavior |
| **E1-aug** (mới, V3.2) | ✓ | ✓ | ✗ | official behavior |
| E1 | ✓ | ✗ | ✓ | official behavior |
| E2 | ✓ | ✗ | ✗ | ✓ |
| E3 | ✓ | ✗ | ✓ | ✓ |

(Bảng gốc V3.1 không có cột "Paraphrase có MSE với GT" và dòng E1-aug.)

**Vì sao cần E1-aug:** hội đồng gần như chắc chắn hỏi *"L_same có hơn việc chỉ augment prompt không?"*. E1-aug có cùng chi phí với E0-ft (1 forward, chỉ đổi prompt) nên rẻ. Nếu E1 ≈ E1-aug thì phải viết trung thực là L_same không thêm gì so với augmentation.

**Cách chạy E1-aug để so công bằng với E1 (V3.3):**
- cùng **k mẫu mỗi batch** (≈30%) như E1;
- cùng **pool template TRAIN** (§17, §21.4);
- khác biệt duy nhất: k mẫu đó được **thay** tên lớp bằng q2 và nhận MSE với GT (1 forward), thay vì forward thêm nhánh q2 với L_same như E1.

**Seed:** ≥2 seed cho E0-ft và E3, báo mean ± std. Nếu còn budget thì thêm cho E1/E2.

---

# 26. Vì sao E0-ft bắt buộc?

Nếu:

```text
E1/E2/E3 = train thêm N epoch
```

mà E0 không train thêm thì improvement có thể chỉ vì:

```text
more optimization steps
```

Do đó giữ cùng:

```text
same epochs
same LR
same optimizer
same batch size
same seed policy
same data budget
```

---

# 27. Hypothesis

Không coi đây là result chắc chắn.

```text
E0
baseline

E0-ft
control for extra training

E1-aug
robustness ↑ (có thể gần bằng E1)

E1
robustness ↑ (phải hơn E1-aug thì L_same mới có giá trị riêng)
sensitivity có thể ↓

E2
sensitivity ↑

E3
cân bằng robustness + sensitivity tốt hơn
```

---

# 28. PrACo evaluation

Không tự viết lại từ đầu nếu không cần.

Dùng official repo:

https://github.com/ciampluca/PrACo

Workflow:

```text
official PrACo evaluator
↓
verify official checkpoint metrics
↓
plug E0-ft / E1 / E2 / E3 checkpoints
```

## 28.1. Cắm checkpoint của mình vào PrACo (V3.3.1, đã đọc code nhánh `master`)

- Wrapper: `models/clipcount_model.py`. Nạp model bằng `run.Model.load_from_checkpoint(model_ckpt, map_location=device, strict=False)`, dùng bản copy code CLIP-Count **đi kèm repo PrACo** (`models/CLIPCount/`), không dùng `run.py` đã vá của mình. Vì các can thiệp chỉ đổi loss/dữ liệu, không đổi kiến trúc → checkpoint E0-ft…E3 cắm vào được.
- Đường dẫn checkpoint bị hardcode trong `models/loader.py`: `CLIPCount/checkpoints/clipcount_pretrained.ckpt` (thường) và `CLIPCount/checkpoints/clipcount_fsc147_filtered.ckpt` ("filtered"). Muốn chạy E nào thì **copy/đổi tên checkpoint vào đúng chỗ** (hoặc sửa loader thêm tham số đường dẫn).
- **Bẫy A — `strict=False`:** nếu tên key lệch thì model vẫn nạp, phần thiếu giữ trọng số khởi tạo ngẫu nhiên, **không báo lỗi**. Kiểm tra: chạy PrACo với checkpoint official trước, số phải khớp Table 1/3 của paper; với checkpoint của mình, in `missing_keys/unexpected_keys` một lần.
- **Bẫy B — checkpoint "filtered" là mặc định:** `multiclass_main.py` có cờ `--use_unfiltered_checkpoints`, tức mặc định nạp bản *filtered*. README không giải thích "filtered" là gì → Day 6 phải đọc code/paper để biết số trong paper dùng bản nào, và dùng **cùng loại** khi so với E0 của mình. E0-ft…E3 đều fine-tune từ checkpoint official (unfiltered) → đánh giá bằng `--use_unfiltered_checkpoints`.

---

# 29. Metric chính

Bảng chính chỉ nên giữ:

```text
MAE ↓
NMN ↓
PCCN ↑
CntF1 ↑
NPV ↓
WPMAE ↓
```

---

# 30. Metric phụ / appendix

Có thể đưa:

```text
RMSE
CntP
CntR
APMAE
POA
bootstrap CI
```

Không làm main table quá nhiều metric.

**V3.2: bỏ CPL.** FSC-147 và MUCCA chỉ có point annotation, không có vùng của lớp kia, nên không tính được "density rơi vào vùng lớp khác" một cách tự động. Dùng bộ metric chuẩn của PrACo++ (NMN, PCCN, CntP, CntR, CntF1) thay thế.

Nếu cần minh hoạ density bị rò sang lớp khác thì chỉ làm trên **PairTally** (có box cho cả hai lớp) hoặc ảnh mosaic (biết chính xác vùng từng tile), và để ở phụ lục/hình qualitative.

---

# 31. NPV

Với K paraphrases cho ảnh i:

\[
NPV=
\frac1N\sum_i
\frac{std_k(\hat c_{ik})}{c_i+\epsilon}
\]

Thấp hơn tốt hơn.

Nhưng phải đọc cùng:

```text
NMN / PCCN / CntF1
```

vì NPV thấp một mình có thể do model bỏ qua text.

---

# 32. Worst-Prompt MAE

\[
WPMAE=
\frac1N\sum_i
\max_k|\hat c_{ik}-c_i|
\]

Đo worst-case wording.

## 32.1. NPV / WPMAE đo trên tập nào (V3.3)

| Tập | Prompt | Báo |
|---|---|---|
| **FSC-147 test** (chính) | template TEST của A–D (seen-family) và họ E (unseen-family), K prompt mỗi họ | NPV, WPMAE, tách seen/unseen |
| PairTally (phụ) | cùng bộ template, áp cho **từng target** trong ảnh | NPV theo INTER/INTRA |

Ước tính compute: mỗi cấu hình E chạy inference `K × số họ` lần trên FSC-147 test. Đo thời gian 1 lượt test ở tuần 1 rồi chốt K (ví dụ K = 5).

## 32.2. Đo cùng lúc hai vế (V3.3)

NPV một mình không đủ (model bỏ qua text cũng có NPV = 0), và NMN/CntF1 một mình chỉ đo bằng tên lớp. Vì vậy thêm hai cách đo kết hợp:

1. **Paraphrase-PrACo:** chạy negative-label test và mosaic test của PrACo, nhưng **thay tên lớp bằng prompt TEST đã paraphrase** (§17). Báo NMN_para, CntF1_para. Nếu model bền thật và nhạy thật thì CntF1_para ≈ CntF1 với tên lớp.
2. **Scatter NPV (trục x, thấp tốt) vs CntF1 (trục y, cao tốt)** cho 6 cấu hình E0 / E0-ft / E1-aug / E1 / E2 / E3. Góc trên-trái là mục tiêu. Đây là **hình chính** của báo cáo, minh hoạ trực tiếp "Stable to Wording, Sensitive to Targets".

Paraphrase-PrACo cần sửa phần prompt trong evaluator của PrACo. Làm ở tuần 4, sau khi đã chạy được PrACo gốc (Day 6 tuần 1).

**V3.3.1 — dễ hơn dự tính:** hàm `get_text_prompt(self, text)` trong `PrACo/models/clipcount_model.py` hiện chỉ `return f"{text}"`. Thay bằng hàm tra template TEST (§17) là xong phần prompt; phần còn lại của evaluator giữ nguyên. Checkpoint cắm theo §28.1.

---

# 33. Dataset / evaluation hierarchy

## FSC-147

```text
standard counting
training
validation
synthetic mosaic creation
```

## PrACo Mosaic

```text
controlled synthetic semantic grounding test
```

## MUCCA

```text
real multi-category scenes
```

## PairTally

```text
controlled two-target
INTER / INTRA
fine-grained discrimination
```

## FSC-147-S-v2 (V3.2, SHOULD HAVE)

```text
230 ảnh, từ T2ICount
đếm vật thiểu số trong ảnh
→ đo vế target sensitivity trên ảnh thật
→ untouched final test, không tune
```

Ghi chú: ảnh lấy từ FSC-147, cần kiểm tra ảnh nào thuộc split train. Nếu có trùng thì báo riêng phần trùng / không trùng.

---

# 34. Vì sao phải có MUCCA?

E2/E3 được train với mosaic.

Nếu chỉ test bằng PrACo mosaic:

```text
train = synthetic composite
test = synthetic composite
```

model có thể hưởng lợi từ familiarity với format.

MUCCA giúp kiểm tra real multi-class scene.

---

# 35. PairTally vẫn giữ

PairTally và MUCCA khác vai trò:

```text
MUCCA
→ real-world multi-class grounding

PairTally
→ controlled pair discrimination
→ INTER / INTRA
```

---

# 36. PairTally không dùng để tune

```text
FSC-147 train
→ train

FSC-147 val
→ tune

synthetic val mosaics
→ tune mosaic-related settings

PairTally
→ untouched final test

MUCCA
→ untouched final test
```

---

# 37. Seen / Unseen audit

Map:

```text
PairTally labels
↓
FSC-147 train labels
```

Cần xử lý thủ công:

```text
plural
synonym
near synonym
parent-child label
```

Báo:

```text
Overall
Seen
Unseen
INTER
INTRA
```

Lưu ý wording:

> “unseen with respect to counting training categories”

không phải unseen đối với CLIP pretraining.

---

# 38. VA-Count diagnostic — giữ nhưng giới hạn scope

Giữ tối đa **2 ngày**.

Mục tiêu: đụng trực tiếp vấn đề 2 của thầy.

Subset:

```text
30–50 cases
```

---

# 39. VA-Count / Grounding DINO flow

```text
Prompt
 ↓
Grounding DINO
 ↓
detections
 ↓
VA-Count exemplars
 ↓
density
```

Đo:

```text
GDINO precision
GDINO recall
GDINO-only count
VA-Count count
qualitative density
```

---

# 40. GDINO-only baseline bắt buộc

\[
C_{GDINO}=\#detections
\]

Phải so:

```text
GDINO-only
vs
VA-Count
```

để biết detector đã giải bài toán tới mức nào.

---

# 41. Không mặc định Grounding DINO đúng

Đặc biệt ở PairTally INTRA:

```text
red apple
vs
green apple
```

Grounding DINO có thể chính là stage fail.

Do đó phải đo detector trước khi kết luận lỗi ở counter.

## 41.1. Đo ở đâu (V3.2)

- **Ưu tiên PairTally** để lấy 30–50 case: có box cho cả hai lớp, nên precision/recall của GDINO tính sạch bằng IoU.
- Trên FSC-147 chỉ có point + 3 box exemplar → recall phải tính bằng "mỗi point có rơi vào box nào không". Chỉ dùng nếu cần thêm case.

## 41.2. Slide riêng cho vấn đề 2 của thầy

Chuẩn bị **1 slide riêng** (xem §55, Slide 4b) gồm bảng:

```text
GDINO precision / recall
GDINO-only count vs VA-Count count vs GT
vài hình density của VA-Count bị lan sang lớp khác
```

**Kết luận phải rút ra từ số đo, không viết sẵn.** Nếu số đo cho thấy lỗi chủ yếu ở counter/exemplar → dùng làm lý do chuyển sang CLIP-Count (text đi thẳng vào model). Nếu lỗi chủ yếu ở GDINO → nói đúng như vậy; lúc đó lý do chuyển sang CLIP-Count là "bỏ được stage detector có thể fail".

Cách trình bày này biến việc đổi model thành **một phát hiện có chủ đích**, không bị xem là né câu hỏi của thầy.

---

# 42. Hard/Soft Gate hạ xuống optional

Nếu còn thời gian:

```text
No Gate
Hard Gate
Soft Gate
```

Nhưng không nằm trong core contribution.

---

# 43. T2ICount: không train, chỉ inference làm dòng tham chiếu (V3.2)

Không dùng làm base, không train lại.

Lý do không train:
- Stable Diffusion v1.5;
- compute nặng;
- setup/debug dài.

**Nhưng** vì có checkpoint công khai và thầy đã gửi link, nâng lên **SHOULD HAVE**: chạy **inference-only** để có một dòng tham chiếu trong bảng, trên:

```text
FSC-147 test (đối chiếu 11.76 trong README)
FSC-147-S-v2
held-out prompt benchmark (NPV / WPMAE)   ← nếu kịp
```

Dòng này đánh dấu rõ "reference, không cùng setting train". Không dùng để claim hơn/kém.

Budget: tối đa **1 ngày**, làm ở tuần 4. Nếu setup quá 1 ngày thì bỏ, chỉ trích số từ paper.

---

# 44. Bỏ khỏi scope chính

- REC-8K
- full T2ICount training
- count-only supervision experiment
- contrastive-density contribution
- full VA-Count retraining
- custom X/Y dataset mới
- random negative class trên FSC-147

---

# 45. Scope MUST HAVE

1. CLIP-Count reproduce.
2. Official PrACo evaluation.
3. Prompt robustness benchmark với held-out prompt families.
4. NPV + WPMAE.
5. E0.
6. E0-ft.
7. E1.
8. E2.
9. E3.
10. MUCCA evaluation.
11. PairTally evaluation.
12. INTER / INTRA breakdown.
13. Seen / Unseen audit.
14. VA-Count + GDINO small diagnostic (+ slide riêng, §41.2).
15. **Vá 3 bẫy code fine-tune (§61.1–61.3) trước khi chạy bất kỳ E nào.**
16. **Bootstrap CI** (V3.3) cho mọi số trên MUCCA (200 ảnh) và FSC-147-S-v2 (230 ảnh). Tập nhỏ, chênh lệch giữa các E dễ nằm trong nhiễu.
17. **Scatter NPV vs CntF1** cho các cấu hình (§32.2).

---

# 46. Scope SHOULD HAVE

- **E1-aug** (khuyên làm; cùng chi phí với E0-ft);
- ≥2 seed cho E0-ft và E3;
- hard-pair mosaic;
- tăng tỉ lệ null-mosaic (§22.1);
- paraphrase-PrACo (§32.2);
- bootstrap CI cho FSC-147 và PairTally (MUCCA/FSC-147-S-v2 đã là MUST);
- qualitative density plots;
- prompt-family breakdown (seen-family / unseen-family);
- **FSC-147-S-v2 evaluation** (230 ảnh, §33);
- **T2ICount inference-only reference** (≤1 ngày, §43);
- hard/soft spatial gate.

---

# 47. Scope NICE TO HAVE

- advanced query-aware module;
- extra dataset.

---

# 48. Roadmap 4 tuần

## TUẦN 1 — Reproduce + Evaluation

### Day 1–2

Hiểu:

```text
density map
FSC-147
MAE/RMSE
CLIP text/image embedding
```

**Song song từ Day 1:** dựng môi trường Colab + tải FSC-147 (vài GB) lên Drive + tải checkpoint official. Xem §61.4 về pin version. Đừng để việc cài đặt dồn sang Day 5.

### Day 3

Đọc:

```text
CLIP-Count paper
models/clip_count.py
run.py
```

### Day 4

Đọc kỹ:

```text
util/FSC147.py
```

Đặc biệt:

```text
self mosaic
cross-class mosaic
use_out_mosaic
```

### Day 5

Run official CLIP-Count checkpoint và verify standard result.

**Đo compute (V3.3):**
- thời gian 1 lượt test FSC-147 (để ước tính NPV cho K prompt, §32.1);
- thời gian mỗi epoch train: chạy `--mode train` với code gốc khoảng 100–200 step rồi dừng, nhân ra cả epoch.

→ Từ đó mới chốt số epoch fine-tune và số seed (§61.5).

### Day 6

Clone / run official PrACo. Không tự rewrite evaluator.

Kèm theo (V3.3): tải MUCCA từ Zenodo, đọc `multiclass_main.py`, và xác nhận CLIP-Count có trong bảng kết quả của paper PrACo++.

V3.3.1: CLIP-Count **đã xác nhận** có trong bảng. Việc Day 6 cụ thể:
- giải nén ảnh MUCCA vào `data/multiclass-dataset/images/` (metadata đã có sẵn, §4.2);
- đặt checkpoint official vào `models/CLIPCount/checkpoints/clipcount_pretrained.ckpt` (§28.1);
- tìm hiểu "filtered" vs `--use_unfiltered_checkpoints`, chạy lại CLIP-Count và so với Table 1/3 của paper (§28.1, bẫy A–B).

### Day 7

P0 prompt benchmark:

```text
prompt families
CLIP cosine
E0 NPV
WPMAE
```

Cuối tuần 1 phải biết prompt set có đủ khó hay không.

---

# 49. TUẦN 2 — Data intervention

## Cross-class mosaic

Bắt đầu từ code có sẵn.

Không rewrite nếu chưa cần.

Thử:

```text
enable existing branch
fix scaling
random layouts
random position
```

## Prompt split

```text
Template TRAIN / TEST theo §17
(A–D: mỗi họ chia template train/test; họ E chỉ test)
```

## Hard pairs

Nếu đủ thời gian:

```text
70% random
30% CLIP-similar + manually verified
```

## Vá code fine-tune (V3.2)

Làm ngay trong tuần 2, **trước** tuần 3:

```text
§61.1 overwrite_args sau load_from_checkpoint
§61.2 --contrast_pre_epoch -1, giữ use_contrast=True
§61.3 truyền flag mosaic vào FSC147(split="train")
§61.6 checkpoint mỗi epoch lên Drive
```

Kiểm tra bằng một run 1 epoch: in ra args thực tế, tỉ lệ cross-class mosaic, và xác nhận `L_density` có mặt ngay từ epoch 0.

Deliverable:

```text
mosaic_v1
prompt_family_v1  → prompts/train_templates.json, prompts/test_templates.json (§17, §21.4)
pairs_far.json (null-mosaic) + pairs_hard.json nếu làm hard-pair (§11.1)
synthetic_val
patched run.py / FSC147.py (đã test 1 epoch)
```

---

# 50. TUẦN 3 — Controlled training

Train / fine-tune:

```text
E0-ft
E1-aug   (SHOULD HAVE)
E1
E2
E3
```

Thứ tự chạy khuyên dùng: **E0-ft → E2 → E3 → E1 → E1-aug**. Làm vậy để phần không được cắt (§52) xong trước.

Giữ cùng:

```text
epoch count
LR
optimizer
seed policy
batch size
training budget
```

Lưu checkpoint mỗi epoch nếu storage cho phép.

---

# 51. TUẦN 4 — Final evaluation

Chạy:

```text
E0
E0-ft
E1-aug
E1
E2
E3
```

trên:

```text
FSC-147
PrACo
MUCCA
PairTally
held-out prompt benchmark
```

Báo:

```text
MAE
NMN
PCCN
CntF1
NPV
WPMAE
```

PairTally:

```text
Overall
INTER
INTRA
Seen
Unseen
```

---

# 52. Fallback plan

Nếu E3 fail:

```text
E0-ft
E1
E2
```

vẫn đủ ablation.

Nếu thiếu thời gian, cắt theo thứ tự:

```text
1. Gate
2. T2ICount inference (chỉ trích số từ paper)
3. Hard-pair mosaic
4. Seed thứ 2
5. VA-Count giảm xuống GDINO-only + vài qualitative cases (vẫn giữ slide §41.2)
6. E1-aug
7. E1
```

(Lưu ý: nếu cắt E1 thì E1-aug cũng mất ý nghĩa; cắt cả hai cùng lúc.)

Không cắt:

```text
E0-ft
E2
PrACo
MUCCA / PairTally
held-out prompt evaluation
```

---

# 53. Contribution viết lại

### Contribution 1

> We study two complementary dimensions of query fidelity in text-guided zero-shot counting: invariance to semantically equivalent prompt formulations and sensitivity to changes in the requested target.

### Contribution 2

> We reactivate and extend the disabled cross-image mosaic mechanism in the official CLIP-Count implementation to investigate how explicit multi-class selective supervision affects query sensitivity.

### Contribution 3

> We combine selective mosaic supervision with equivalent-prompt consistency and evaluate the trade-off between linguistic robustness and semantic discrimination using established PrACo/PrACo++ metrics together with held-out paraphrase robustness evaluation.

---

# 54. Không claim

Không claim:

```text
first semantic grounding benchmark
first mosaic training
first multi-class counting
first positive-negative counting
first prompt-aware counter
```

---

# 55. Storyline bảo vệ

## Slide 1

```text
Tell the model what to count.
```

## Slide 2

Prior work:

```text
PrACo / PrACo++
→ models may ignore the prompt

T2ICount (CVPR 2025)
→ fixes text sensitivity with a diffusion backbone
→ strong, but heavy to train
→ no paraphrase-robustness evaluation

→ Our choice: controlled training interventions on light CLIP-Count
```

## Slide 3

Our question:

```text
Same target + new wording
→ stable?

Different target + same image
→ sensitive?
```

## Slide 4

Why standard FSC-147 supervision is limited:

```text
one annotated target per image
```

## Slide 4b (V3.2) — Vấn đề 2 của thầy: VA-Count / Grounding DINO

```text
GDINO precision / recall (PairTally)
GDINO-only vs VA-Count vs GT
→ kết luận rút từ số đo (§41.2)
→ vì sao chuyển trọng tâm sang CLIP-Count
```

## Slide 5

Important code finding:

```text
CLIP-Count already contains
disabled cross-class mosaic
```

## Slide 6

Method:

```text
reactivated / extended mosaic
+
L_same
```

## Slide 7

Controlled ablation:

```text
E0
E0-ft
E1-aug
E1
E2
E3
```

## Slide 8

Synthetic + real evaluation:

```text
PrACo
MUCCA
PairTally
```

## Slide 9

Metrics:

```text
MAE
NMN
PCCN
CntF1
NPV
WPMAE
```

## Slide 10

# Stable when wording changes. Sensitive when the target changes.

---

# 56. Roadmap học mới — không dùng Zero-to-Hero cũ

Thứ tự học mới:

```text
1. Density Map + FSC-147 + MAE/RMSE
2. CLIP fundamentals
3. Contrastive Learning
4. CoOp + VPT
5. CLIP-Count paper
6. CLIP-Count code:
   - models/clip_count.py
   - run.py
   - util/FSC147.py
7. PrACo / PrACo++
8. CounTR mosaic
9. Mosaic code branch in CLIP-Count
10. E0-ft / E1 / E2 / E3
11. PairTally + MUCCA
12. VA-Count + Grounding DINO diagnostic
```

Không cần dành gần hai tuần đầu để reproduce ZSC 2023 và VA-Count full training như roadmap cũ.

---

# 57. Các file code bắt buộc phải đọc

## CLIP-Count

```text
models/clip_count.py
run.py
util/FSC147.py
models/contrastive_loss.py
util/misc.py
```

## PrACo

```text
main.py
main_statistics.py
multiclass_main.py             (MUCCA)
multiclass_main_statistics.py
benchmark/*
models/loader.py               (đường dẫn checkpoint hardcode, §28.1)
models/clipcount_model.py      (get_text_prompt, load_from_checkpoint strict=False)
models/CLIPCount/*             (tên thư mục thật, không có gạch nối)
```

## CounTR

Đọc phần:

```text
mosaic augmentation
training data pipeline
```

---

# 58. Trạng thái các câu hỏi review của V3.1

| # | Câu hỏi | Trạng thái V3.3 |
|---|---|---|
| 1 | Framing robustness + sensitivity đủ khác PrACo/PrACo++? | Đủ, với điều kiện có held-out paraphrase (Gap A) + training intervention (Gap C) |
| 2 | "Reactivate + extend" đủ trung thực? | Đủ |
| 3 | Đã có paper làm đúng CLIP-Count + cross-class mosaic + held-out prompt consistency? | Chưa tìm thấy. Vẫn phải cite CounTR, MGCAC, CountGD++, MixCount |
| 4 | E0-ft đủ công bằng? | Đủ cho mosaic; cho L_same thì cần thêm **E1-aug** |
| 5 | Prompt split tránh leakage? | Đã sửa: tách theo template + họ E để riêng (§17) |
| 6 | Dùng LLM prompt ở test? | Có, nếu lọc tay chặt; chỉ ở họ E |
| 7 | Main table 6 metric đủ gọn? | Đủ |
| 8 | MUCCA + PairTally đủ làm bằng chứng ảnh thật? | Đủ; lưu ý PairTally từng loại CLIP-Count vì yếu → số có thể thấp, vẫn báo trung thực |
| 9 | Hard-pair làm ngay? | Không, để SHOULD HAVE |
| 10 | 4 tuần đủ an toàn? | **Phụ thuộc hạn nộp (chưa xác nhận)**. Nếu <4 tuần, cắt theo §52 |

---

# 59. Các nguồn chính

- CLIP-Count  
  https://github.com/songrise/CLIP-Count

- PrACo  
  https://github.com/ciampluca/PrACo

- PrACo paper — Mind the Prompt  
  https://arxiv.org/abs/2409.15953

- PrACo++ / MUCCA — Does it Really Count?  
  https://arxiv.org/abs/2605.02752

- PairTally  
  https://github.com/bbvisual/PairTally_Benchmark

- PairTally paper — *Can Current AI Models Count What We Mean, Not What They See? A Benchmark and Systematic Evaluation* (DICTA 2025)  
  https://arxiv.org/abs/2509.13939

- MUCCA data (Zenodo, v1.0, CC BY 4.0)  
  https://zenodo.org/records/19231375

- VA-Count  
  https://github.com/HopooLinZ/VA-Count

- ZSC CVPR 2023  
  https://github.com/cvlab-stonybrook/zero-shot-counting

- CountEx  
  https://arxiv.org/abs/2602.19432

- MixCount  
  https://arxiv.org/abs/2605.18063

- CountGD++  
  https://arxiv.org/abs/2512.23351

- T2ICount (CVPR 2025)  
  https://github.com/cha15yq/T2ICount · https://arxiv.org/abs/2502.20625

---

# 60. Chốt V3.3

Core:

```text
                         QUERY FIDELITY
                              │
             ┌────────────────┴────────────────┐
             │                                 │
             ↓                                 ↓
     PROMPT ROBUSTNESS                TARGET SENSITIVITY
             │                                 │
     Held-out paraphrases             Multi-class scenes
             │                                 │
             ↓                                 ↓
           L_same                 Cross-class Mosaic
             │                                 │
             └────────────────┬────────────────┘
                              ↓
                          CLIP-COUNT
                              ↓
            E0 / E0-ft / E1-aug / E1 / E2 / E3
                              ↓
           FSC + PrACo + MUCCA + PairTally
                              ↓
      MAE + NMN + PCCN + CntF1 + NPV + WPMAE
```

VA-Count:

```text
diagnostic only
↓
GDINO precision / recall
↓
GDINO-only count
↓
VA-Count density
```

Thông điệp cuối:

> **Mục tiêu không còn là chứng minh model “không nghe prompt” — PrACo đã làm điều đó. Mục tiêu là nghiên cứu xem một text-guided counter có thể vừa ổn định trước các biến thể ngôn ngữ chưa từng thấy trong training, vừa giữ khả năng phân biệt đúng khi target thay đổi hay không; đồng thời kiểm tra liệu việc kích hoạt và mở rộng cross-class mosaic supervision có giúp cân bằng hai yêu cầu này trên CLIP-Count hay không.**

---

# 61. Implementation notes (V3.2 — đã kiểm tra với code thật)

Tất cả số dòng dưới đây ứng với commit `ba57fd0` (2024-03-20) của `songrise/CLIP-Count`.

## 61.1. Bẫy 1 — Flag CLI mới bị bỏ qua khi fine-tune

`run.py:473`: chế độ train với `--ckpt` gọi `Model.load_from_checkpoint(...)`. Hàm này lấy lại args đã lưu trong checkpoint (`save_hyperparameters(args)` ở `run.py:132`). `overwrite_args` **chỉ** được gọi ở chế độ test (`run.py:510`).

→ Mọi flag mới (λ, mosaic, L_same...) **bị bỏ qua mà không báo lỗi**.

**Sửa:** gọi `model.overwrite_args(args)` ngay sau dòng 473. Sau đó in args thực tế ra log để kiểm tra.

(Ngoại lệ nhỏ: `run.py:175` dùng biến toàn cục `args.w_contrast` chứ không phải `self.args`, nên `w_contrast` luôn lấy từ CLI. Không gây lỗi, chỉ cần biết khi debug.)

## 61.2. Bẫy 2 — Mất 21 epoch không học density

`trainer.fit` đếm epoch lại từ 0. `run.py:167–175`: khi `use_contrast and current_epoch <= contrast_pre_epoch` (mặc định 20), loss contrastive **thay thế** density loss (`loss = args.w_contrast * contrast_loss`, không phải `+=`).

→ Fine-tune ngây thơ sẽ mất 21 epoch đầu không học density.

**Sửa:** chạy với `--contrast_pre_epoch -1` và **giữ `use_contrast=True`**.

**Không** tắt `use_contrast`: khi đó `run.py:206–207` sẽ bọc `"a photo of {}"` **ở validation**, trong khi train và test vẫn dùng prompt thô → checkpoint được chọn theo val_mae với prompt khác lúc train/test. (V3.3: `run.py:157–158` là code chết vì nằm sau forward, xem §18.)

## 61.3. Bẫy 3 — Số epoch và flag mosaic

- `run.py:467`: `max_epochs = epochs + contrast_pre_epoch`. Với `contrast_pre_epoch = -1` thì số epoch thực là `epochs − 1` → đặt `--epochs` bù thêm 1.
- `FSC147.py:224`: `use_out_mosaic = False` bị hardcode.
- `run.py:435`: `FSC147(split="train")` được tạo mà không truyền args.

**Sửa:** thêm tham số vào `FSC147(...)` → truyền xuống transform train → gán `use_out_mosaic` và tỉ lệ mosaic từ CLI.

## 61.4. Môi trường

- `requirements.txt` pin `pytorch_lightning==1.8.0` nhưng **không pin torch**. Ngoài ra `numpy==1.21.2`/`scipy==1.7.3` không có wheel cho Python mới của Colab.
- **⚠️ NumPy 2 (V3.3, review đã chạy thử xác nhận):** `imgaug==0.4.0` crash với NumPy 2.x, mà Colab mặc định NumPy 2. `FSC147.py:18` import imgaug ở đầu file → **kể cả `--mode test` cũng chết ngay lúc import**. Cách sửa: **chạy đầu tiên** `pip install "numpy<2"`, rồi **Restart runtime**, rồi mới cài các gói khác.
- **⚠️ setuptools (V3.3.1):** `pytorch_lightning==1.8.0` (qua `lightning_utilities`) và gói `clip` của OpenAI đều import `pkg_resources`. `pkg_resources` **đã bị xoá khỏi setuptools từ bản 82.0.0** (08/02/2026). Review chạy thử trên Python 3.12: setuptools 80.10 thì import được và tạo `Trainer` bình thường; bản mới báo `No module named 'pkg_resources'`. Code CLIP-Count tự nó không dùng `pkg_resources` (đã grep). → Gộp vào cùng cell đầu: **`pip install "numpy<2" "setuptools<81"`**, rồi Restart.
- Nếu sau khi hạ numpy mà `import cv2` báo lỗi (bản opencv mới của Colab có thể đòi NumPy 2): cài `opencv-python-headless` bản cũ hơn tương thích NumPy 1.x, rồi restart lại.
- **Làm Day 1:** giữ `pytorch_lightning==1.8.0`, numpy < 2, để scipy/torch theo Colab, rồi chạy test checkpoint official. Nếu PL 1.8 lỗi với torch 2.x thì mới hạ torch. Ghi lại version cuối cùng vào báo cáo (mục reproducibility).
- FSC-147 nặng vài GB → để trên Drive, copy vào `/content` đầu mỗi session để đọc nhanh.

## 61.5. Budget fine-tune — chốt trước khi chạy

Giống nhau cho mọi E:

```text
epochs      : 30–50 (chốt một số)
LR          : ~1e-5
batch/accum : giống nhau
seed        : ≥2 cho E0-ft và E3
mosaic ratio: chốt trước, log tỉ lệ thực tế mỗi epoch (§9.4)
```

**Vì sao LR ~1e-5 (V3.3.1, phòng khi bị hỏi):** code gốc dùng `lr=1e-4` (`run.py:81`), AdamW (`run.py:400`), `StepLR(step_size=100, gamma=0.33)` (`run.py:407`). Checkpoint official train khoảng 220 epoch → LR đã giảm 2 lần: 1e-4 × 0.33² ≈ **1.1e-5**. Fine-tune ở 1e-5 là nối tiếp đúng mức LR cuối. Với 30–50 epoch thì StepLR không giảm lần nào (fine-tune bằng `load_from_checkpoint` tạo optimizer/scheduler mới).

**Chú ý:** `--lr` cũng là flag CLI → **chưa vá bẫy 1 (§61.1) thì LR thật sẽ là 1e-4 lấy từ checkpoint**, gấp 10 lần dự định, không báo lỗi. In `self.args.lr` ra log ở run thử 1 epoch.

## 61.6. Checkpoint và Colab

`run.py:459`: `ModelCheckpoint(save_top_k=4, monitor='val_mae')` **không** lưu mỗi epoch, và mặc định ghi vào `lightning_logs` trong máy Colab.

**Sửa:** thêm `save_last=True`, đặt `dirpath` lên Drive. Khi Colab ngắt, **resume** bằng `trainer.fit(..., ckpt_path=last.ckpt)` (giữ epoch/optimizer), không dùng `load_from_checkpoint` (cách đó dùng để *bắt đầu* fine-tune).

## 61.7. Tóm tắt các con số đã xác minh trong code

| Tham số | Giá trị | Vị trí |
|---|---|---|
| `coop_width` | 2 | `run.py:64` |
| `use_contrast` | True | `run.py:71` |
| `contrast_pre_epoch` | 20 | `run.py:76` |
| Xác suất mosaic | 0.3 | `FSC147.py:243` |
| Ngưỡng cross-class | < 70 vật | `FSC147.py:321` |
| Null-mosaic | 5% trong nhánh cross-class ≈ 1.5% toàn tập, chưa chắc null thật | `FSC147.py:338–342, 370` |
| Gaussian σ | 1, sau khi ghép | `FSC147.py:401` |
| Density scale | ×60 | `FSC147.py:404` |
| batch_size / accum_iter | 32 / 1 | `run.py:44–47` |
| Precision | fp16 | `run.py:466` |

## 61.8. Đường dẫn data bị hardcode

`FSC147.py:45`: `self.data_dir = "data/FSC/"` là **đường dẫn tương đối**. Phải chạy `run.py` từ thư mục gốc repo, và cấu trúc phải đúng như README:

```text
data/FSC/
├─ images_384_VarV2/
├─ gt_density_map_adaptive_384_VarV2/
└─ FSC_147/
   ├─ ImageClasses_FSC147.txt
   ├─ Train_Test_Val_FSC_147.json
   └─ annotation_FSC147_384.json
```

Annotation phải tải **riêng** từ repo `cvlab-stonybrook/LearningToCountEverything` (thư mục `data/`). Trên Colab: copy data từ Drive vào `/content/CLIP-Count/data/FSC/` (đọc nhanh hơn đọc thẳng từ Drive).

## 61.9. Ba con số baseline CLIP-Count khác nhau (mục reproducibility)

| Nguồn | FSC val MAE | FSC test MAE |
|---|---:|---:|
| Paper CLIP-Count | 18.79 | 17.78 |
| README, checkpoint công khai | 18.93 | 17.45 |
| RichCount Table 1 (tự chạy lại) | 19.85 | 17.19 |
| **Mình chạy lại (E0)** | ? | ? |

Mục tiêu E0: gần **17.45 / 18.93** (vì dùng đúng checkpoint công khai). Lệch trong khoảng ±0.5 là chấp nhận được. Nếu lệch nhiều hơn thì kiểm tra version thư viện và cách xử lý sliding window lúc test trước khi làm tiếp.

---

# 62. Vị trí code trên máy

Thư mục dự án: `D:\MINHTRIHOCCODE\HOCKI5\CS331\`

```text
CS331\
├── HANDOFF_CS331_2026-09-25.md   ← handoff mới nhất (cập nhật 26/09)
├── roadmap\
│   ├── CS331_ZSC_V3_3_Final.md   ← bản chốt (file này, V3.3.1)
│   ├── CS331_BaoCao_Review_V3_2.md, CS331_BaoCao_Review_V3_3.md  ← review của bạn, đã đưa hết vào
│   └── ban_cu\                   ← V3.2, V3.1, V3, V2, Zero-to-Hero, handoff 23/09 (chỉ tham khảo)
└── code\CLIP-Count\              ← git clone của songrise/CLIP-Count
```

- **Code:** `D:\MINHTRIHOCCODE\HOCKI5\CS331\code\CLIP-Count` (commit `ba57fd0`, sạch, chưa sửa gì, ~4 MB, chưa có data/checkpoint). Chuyển từ Temp sang ngày 25/09.
- Khi bắt đầu sửa code: tạo branch riêng (ví dụ `cs331-v33`). Nên fork lên GitHub của bạn để clone trên Colab.
- Code train thật sẽ chạy trên **Colab** (GPU local chỉ 4GB).

---

# 63. Góp ý review đã KHÔNG đưa vào (và lý do)

| Góp ý | Lý do không đưa vào |
|---|---|
| L_region dùng mask Grounding DINO | Thuộc roadmap Zero-to-Hero đã lỗi thời. Mask GDINO bỏ sót vật → phạt nhầm vật đúng. Mosaic đã cho nhãn vùng sạch hơn |
| L_anti_leak với M_Y từ GDINO | FSC-147 chỉ gán nhãn 1 lớp/ảnh → M_Y toàn false positive |
| Random negative class trên ảnh FSC-147 đơn | Nhãn bẩn (vật lớp Y không được gán nhãn). Thay bằng null-mosaic (§22.1) |
| Adapter/FFN của RichCount vào VA-Count | Counter của VA-Count không nhận text; GDINO chạy offline. RichCount không có code công khai. Prompt thuộc tính/vị trí ("red apples on the left") nằm ngoài phạm vi (§16) |
| Sửa viền Gauss khi ghép mosaic | Code đã áp Gaussian sau khi ghép (§9.6) |
| Đổi ngay sang bố cục 1×2 để giữ scale | Chưa cần; chỉ làm nếu E2 tệ trên ảnh thật (§9.7) |

---

# 64. Đánh giá chốt (25/09, cập nhật V3.3) + checklist bắt đầu

## 64.1. Đã chốt được chưa?

**Hướng nghiên cứu: CHỐT. V3.3 là bản để làm.** Review 25/09 không đụng tới hướng đi; toàn bộ là sửa số liệu, sửa mâu thuẫn và bổ sung chi tiết cách làm. Mọi điểm trong review đều đã được đưa vào (xem changelog V3.2 → V3.3).

| Phần | Trạng thái |
|---|---|
| Research question, Gap A/B/C | Chốt |
| Base model (CLIP-Count) + lý do chọn so với T2ICount/VA-Count | Chốt |
| Method (mosaic + L_same teacher–student) | Chốt |
| Ablation (E0 / E0-ft / E1-aug / E1 / E2 / E3) | Chốt |
| Metric bảng chính (MAE, NMN, PCCN, CntF1, NPV, WPMAE) + hình scatter NPV–CntF1 | Chốt |
| NPV đo trên tập nào, q2 sinh ở đâu, E1-aug chạy thế nào | Chốt (V3.3: §32.1, §21.4, §25) |
| Dataset (FSC-147, PrACo, MUCCA, PairTally; FSC-147-S-v2 ở mức SHOULD HAVE) | Chốt; **MUCCA đã xác nhận tải được** (Zenodo, 200 ảnh) |
| Scope MUST/SHOULD/NICE + thứ tự cắt | Chốt |
| Bẫy code khi fine-tune | Đã xác định, sửa ở tuần 2 |
| Bẫy môi trường (NumPy 2 + imgaug; setuptools + pkg_resources) | Đã xác định, xử lý ngay Day 1 bằng 1 cell |
| CLIP-Count có trong bảng PrACo++ | **Đã xác nhận 26/09** (Table 1–3) |

**Còn mở, nhưng KHÔNG chặn việc bắt đầu:**

| Việc | Khi nào phải xong | Ảnh hưởng |
|---|---|---|
| Hạn nộp thật | Trước cuối tuần 1 | Quyết định có phải cắt theo §52 không |
| Thầy duyệt tên đề tài | Trước khi viết báo cáo | Chỉ ảnh hưởng tên |
| λ, số epoch, tỉ lệ mosaic | Tuần 2–3, tune trên FSC-147 val | Hyperparameter, không đổi hướng |
| Nội dung pool prompt | Tuần 1 (P0, §14) | Nếu NPV của E0 ≈ 0 thì làm lại prompt, không đổi hướng |
| Số epoch, số seed | Day 5 tuần 1, sau khi đo thời gian mỗi epoch | Nếu quá chậm: giảm epoch, bỏ seed thứ 2 trước |
| PrACo wrapper CLIP-Count chạy được trên Colab không; checkpoint "filtered" là gì | Day 6 tuần 1 | Wrapper có sẵn (đã đọc code); còn rủi ro môi trường + bẫy A–B ở §28.1 |

→ **Có thể bắt đầu làm ngay.**

## 64.2. Chiều nay làm gì (Tuần 1, Day 1)

Mục tiêu buổi chiều: **có số E0 đầu tiên trên FSC-147**, hoặc ít nhất dựng xong môi trường và dữ liệu.

1. **Colab notebook** `CS331_E0.ipynb`:
   - mount Drive; tạo `MyDrive/CS331/{data,ckpt,logs}`;
   - đưa code lên Colab: fork `songrise/CLIP-Count` về GitHub của bạn rồi clone (khuyên dùng), hoặc upload thư mục `code\CLIP-Count`;
   - **cell đầu tiên:** `!pip install "numpy<2" "setuptools<81"` → menu *Runtime → Restart session* (bắt buộc: imgaug crash với NumPy 2; PL 1.8 và `clip` cần `pkg_resources`, §61.4);
   - sau khi restart, kiểm `import numpy, setuptools; print(numpy.__version__, setuptools.__version__)` ra 1.x và < 81, rồi cài: `pip install pytorch_lightning==1.8.0 einops imgaug ftfy regex tqdm git+https://github.com/openai/CLIP.git`. Dùng torch sẵn có của Colab trước;
   - kiểm nhanh: `python -c "import imgaug, cv2, pytorch_lightning, clip"` không lỗi thì mới đi tiếp.
2. **Dữ liệu FSC-147** (link trong README của CLIP-Count → repo LearningToCountEverything):
   - `images_384_VarV2`, `gt_density_map_adaptive_384_VarV2`, và 3 file annotation;
   - lưu lên Drive **một lần**, mỗi session copy vào `/content/CLIP-Count/data/FSC/` (§61.8).
3. **Checkpoint công khai** (link Google Drive trong README) → `MyDrive/CS331/ckpt/clipcount_official.ckpt`.
4. **Chạy E0:**
   ```bash
   cd /content/CLIP-Count
   python run.py --mode test --exp_name e0 --batch_size 32 --dataset_type FSC --ckpt /content/drive/MyDrive/CS331/ckpt/clipcount_official.ckpt
   ```
   Phải chạy từ thư mục gốc repo vì `data/FSC/` và `util/CLIP_caption.pkl` là đường dẫn tương đối. Lần đầu chạy sẽ tự tải trọng số CLIP ViT-B/16.
   Điền kết quả vào bảng §61.9. Ghi lại version torch / PL / numpy / setuptools thực tế.
5. **Nếu lỗi môi trường:** ghi lại lỗi, xem §61.4 (numpy, opencv, torch). Đừng sửa code model ở bước này.
6. **Còn thời gian:** đọc paper CLIP-Count mục 3 (method), đối chiếu với `models/clip_count.py:188–199` (hàm `forward`).

**Chưa làm chiều nay:** vá bẫy code (§61.1–61.3), mosaic, L_same. Những việc đó thuộc tuần 2.
