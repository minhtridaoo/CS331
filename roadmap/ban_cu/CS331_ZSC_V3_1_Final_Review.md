# CS331 UIT — Zero-Shot Object Counting
## V3.1 Final Review Draft — Prompt Robustness + Target Sensitivity

**Mục đích file này:**  
Đây là bản V3.1 để gửi bạn review lần cuối trước khi chốt hướng và bắt đầu học/triển khai.

Bản này giữ nguyên research direction của V3, nhưng sửa các chi tiết mới phát hiện sau khi đọc trực tiếp code CLIP-Count và rà lại PrACo / PrACo++ / CounTR / PairTally / MUCCA.

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

## 4.2. PrACo++ / MUCCA — 2026

**Does it Really Count? Assessing Semantic Grounding in Text-Guided Class-Agnostic Counting**

Có các metric:

```text
NMN
PCCN
CntP
CntR
CntF1
```

và benchmark nhiều model, trong đó có CLIP-Count và ZSC.

Ngoài synthetic test còn có **MUCCA** để đánh giá trên ảnh thật có nhiều object category.

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

## 4.6. MixCount — 2026

Mixed-object training cho counting.

Cũng cần cite nếu thảo luận multi-object supervision.

## 4.7. PairTally — DICTA 2025

Benchmark gồm ảnh có hai nhóm object:

```text
INTER
INTRA
```

phù hợp để đánh giá target discrimination thật.

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
- nhẹ hơn T2ICount;
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

## TRAIN FAMILIES

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

## HELD-OUT TEST FAMILIES

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

Ví dụ:

```text
TRAIN
Family A + B

TEST
Family C + D + E
```

Như vậy nếu E1/E3 cải thiện held-out paraphrase robustness thì mới có ý nghĩa.

Không train `L_same` trên đúng prompt variants rồi dùng chính chúng để báo NPV.

---

# 18. Lưu ý về `"a photo of {}"`

Sau khi đọc `run.py`, không nên mặc định wrap prompt bằng:

```text
a photo of {prompt}
```

Trong official default training:

```python
output = self.model(samples, prompt_gt, ...)
```

được gọi trước nhánh wrap.

`use_contrast=True` cũng là default.

Trong test step, prompt được đưa trực tiếp vào model.

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

# 20. Core Method V3.1

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

---

# 23. Total loss

\[
L=L_{density}+\lambda_mL_{mosaic}+\lambda_sL_{same}
\]

Trong đó:
- `L_density`: standard density supervision;
- `L_mosaic`: selective supervision;
- `L_same`: prompt consistency.

---

# 24. Không kết luận quá mạnh về density supervision

Nếu mosaic cải thiện sensitivity, có thể nói:

> Single-class supervision is an important contributor to query insensitivity, and density-map regression can still support selective counting when explicit multi-class supervision is introduced.

Không nói:

> Density map không phải vấn đề.

---

# 25. Ablation mới — phải có E0-ft

Nếu E1/E2/E3 đều fine-tune từ checkpoint E0 thì phải thêm control:

| ID | Extra Fine-tune | L_same | Cross-class Mosaic |
|---|---:|---:|---:|
| E0 | ✗ | ✗ | official behavior |
| E0-ft | ✓ | ✗ | official behavior |
| E1 | ✓ | ✓ | official behavior |
| E2 | ✓ | ✗ | ✓ |
| E3 | ✓ | ✓ | ✓ |

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

E1
robustness ↑
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
CPL
bootstrap CI
```

Không làm main table quá nhiều metric.

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

# 43. T2ICount chuyển xuống Nice-to-have

Không dùng làm dependency chính.

Lý do:
- Stable Diffusion;
- compute nặng;
- setup/debug dài.

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
14. VA-Count + GDINO small diagnostic.

---

# 46. Scope SHOULD HAVE

- hard-pair mosaic;
- bootstrap CI;
- qualitative density plots;
- prompt-family breakdown;
- hard/soft spatial gate.

---

# 47. Scope NICE TO HAVE

- T2ICount reference;
- advanced query-aware module;
- extra dataset.

---

# 48. Roadmap 4 tuần V3.1

## TUẦN 1 — Reproduce + Evaluation

### Day 1–2

Hiểu:

```text
density map
FSC-147
MAE/RMSE
CLIP text/image embedding
```

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

### Day 6

Clone / run official PrACo. Không tự rewrite evaluator.

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
Train families
Held-out test families
```

## Hard pairs

Nếu đủ thời gian:

```text
70% random
30% CLIP-similar + manually verified
```

Deliverable:

```text
mosaic_v1
prompt_family_v1
synthetic_val
```

---

# 50. TUẦN 3 — Controlled training

Train / fine-tune:

```text
E0-ft
E1
E2
E3
```

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
2. T2ICount
3. VA-Count giảm xuống GDINO-only + vài qualitative cases
4. E1
```

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
benchmark/*
models/CLIP-Count/*
```

## CounTR

Đọc phần:

```text
mosaic augmentation
training data pipeline
```

---

# 58. Các câu muốn người review phản biện lần cuối

1. Framing robustness + sensitivity hiện đã đủ khác PrACo / PrACo++ chưa?
2. Viết contribution 2 theo hướng “reactivate + extend disabled mosaic” đã đủ trung thực chưa?
3. Có paper nào đã làm đúng `CLIP-Count + cross-class mosaic + held-out prompt consistency` chưa?
4. E0-ft control đã đủ công bằng chưa?
5. Prompt train/test family split như trên đã đủ tránh leakage chưa?
6. Có nên dùng LLM-generated prompts ở test nếu manual filtering chặt?
7. Main table 6 metric hiện đã đủ gọn chưa?
8. MUCCA + PairTally có đủ làm real-data evidence không?
9. Hard-pair mosaic có đáng làm ngay hay chỉ nên để SHOULD HAVE?
10. Với 4 tuần, scope hiện tại đã đủ an toàn chưa?

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

- PairTally paper  
  https://arxiv.org/abs/2509.13939

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

---

# 60. Chốt V3.1

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
                 E0 / E0-ft / E1 / E2 / E3
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
