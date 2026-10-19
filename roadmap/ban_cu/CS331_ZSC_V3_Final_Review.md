# CS331 UIT — Zero-Shot Object Counting
## V3 Final Review Draft — Prompt Robustness + Target Sensitivity

**Mục đích file này:**  
Đây là bản V3 để gửi bạn review trước khi chốt hướng đồ án.  
Bản này đã sửa các vấn đề của V1/V2, đặc biệt là:

- không dùng VA-Count làm model train prompt loss;
- không claim novelty trùng với PrACo/PrACo++;
- không dùng negative class ngẫu nhiên trên FSC-147;
- không dùng contrastive density như contribution chính;
- thêm mosaic training để tạo supervision phân biệt đối tượng;
- dùng metric published khi có thể;
- giữ PairTally làm test benchmark, không tune trực tiếp trên đó.

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
```

Prediction nên gần nhau.

Đây là:

> **Prompt Robustness**

---

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

# 3. Tại sao phải nghiên cứu đồng thời cả hai?

Nếu chỉ tối ưu Prompt Robustness:

```text
apple
the apples
all apples
```

đều ra giống nhau.

Nghe có vẻ tốt.

Nhưng model bỏ qua text hoàn toàn cũng có thể:

```text
mọi prompt → cùng prediction
```

=> robustness cao nhưng model vô dụng.

Ngược lại, nếu chỉ tăng sensitivity:

```text
apple ≠ orange
```

nhưng mỗi cách diễn đạt khác nhau của `"apple"` lại làm count dao động mạnh thì cũng chưa tốt.

Do đó mục tiêu phải là:

```text
SAME TARGET
different wording
→ stable

DIFFERENT TARGET
same image
→ discriminative
```

---

# 4. Related Work cần cite để tránh claim sai novelty

## 4.1. PrACo — WACV 2025

Paper:

**Mind the Prompt**

PrACo đã chỉ ra rằng các benchmark counting truyền thống có thể không đủ để kiểm tra model có thực sự nghe prompt hay không.

Các protocol nổi bật:

- negative-label test;
- mosaic / distractor-style evaluation.

Vì vậy không được claim:

> “Chúng tôi là người đầu tiên kiểm tra model có nghe prompt hay không.”

---

## 4.2. PrACo++ / MUCCA — 2026

Paper:

**Does it Really Count? Assessing Semantic Grounding in Text-Guided Class-Agnostic Counting**

Bài này tiếp tục đánh giá semantic grounding.

Có các metric như:

```text
NMN
PCCN
CntP
CntR
CntF1
```

Và đã benchmark nhiều model, trong đó có CLIP-Count và ZSC.

Do đó phần benchmark semantic grounding đơn thuần không đủ làm novelty.

---

## 4.3. Mosaic-based CAC — ACCV 2024

Paper:

**A Recipe for CAC: Mosaic-based Generalized Loss for Improved Class-Agnostic Counting**

Đã dùng mosaic augmentation để cải thiện class-agnostic counting trong bối cảnh nhiều object/class.

Do đó không claim:

> “Mosaic training là mới.”

---

## 4.4. CountGD++ — CVPR 2026

CountGD++ cũng dùng synthetic mosaic / multi-category supervision để tạo positive-negative class signal.

Do đó novelty của đồ án không nằm ở “mosaic”.

---

## 4.5. MixCount — 2026

MixCount nghiên cứu mixed-object training và cho thấy mixed scenes giúp generalization trên multi-object counting.

Cũng cần cite nếu dùng mixed-object training.

---

## 4.6. PairTally — DICTA 2025

Paper:

**Can Current AI Models Count What We Mean, Not What They See?**

PairTally có:

- 681 ảnh;
- 2 nhóm object trong mỗi ảnh;
- INTER-category;
- INTRA-category;
- positive / negative prompt;
- point annotation;
- bounding boxes.

Dùng làm final benchmark cho target discrimination.

---

## 4.7. CountEx — 2026

CountEx nghiên cứu:

```text
what to count
+
what not to count
```

nên các ý tưởng positive/negative prompt phải cite bài này.

---

# 5. Điểm còn trống đáng nghiên cứu

Sau khi xét các paper trên, khoảng trống hợp lý nhất là:

## Gap A — Prompt paraphrase robustness

PrACo/PrACo++ chủ yếu kiểm tra:

```text
correct target
wrong target
negative target
distractors
```

nhưng chưa tập trung mạnh vào:

```text
same semantic target
different wording
```

theo protocol controlled paraphrase.

Ví dụ:

```text
apple
apples
the apples
all apples in the image
objects that are apples
```

---

## Gap B — Joint robustness + sensitivity

Điểm cốt lõi:

```text
same target
→ invariant

different target
→ discriminative
```

Hai tính chất này phải được đo cùng lúc.

---

## Gap C — Training intervention cho CLIP-Count

PrACo/PrACo++ thiên về diagnostic/evaluation.

Đồ án này muốn thử:

```text
Prompt Consistency
+
Multi-class Mosaic Supervision
```

trên CLIP-Count.

Không claim là first-ever method.

Nên dùng ngôn ngữ:

> investigate / adapt / combine

---

# 6. Model chính

# CLIP-Count

Repository:

https://github.com/songrise/CLIP-Count

Lý do chọn:

- text embedding đi trực tiếp vào model;
- text ảnh hưởng encoder/decoder;
- nhẹ hơn T2ICount;
- dễ sửa loss và dataloader;
- phù hợp trực tiếp với Prompt Robustness / Query Sensitivity.

---

# 7. Vai trò của VA-Count

Repository:

https://github.com/HopooLinZ/VA-Count

Không dùng VA-Count làm model train prompt loss vì counter chính nhận:

```text
image
+
exemplar patches / boxes
```

Text chủ yếu đi qua Grounding DINO để sinh exemplar trước.

Vai trò của VA-Count:

> **diagnostic model**

Dùng để kiểm tra vấn đề thầy nêu:

```text
Grounding DINO có tìm đúng không?
Nếu đúng, VA-Count density có vẫn leak không?
```

---

# 8. T2ICount

Repository:

https://github.com/cha15yq/T2ICount

Chỉ để:

```text
Nice-to-have reference
```

Không phải dependency của hướng chính.

Lý do:

- Stable Diffusion 1.5;
- setup nặng;
- GPU hạn chế;
- thời gian đồ án ngắn.

---

# 9. Dataset chính

## 9.1. FSC-147

Dùng để:

```text
train CLIP-Count
validation
standard MAE/RMSE
create synthetic mosaic training
create synthetic mosaic validation
```

---

## 9.2. PairTally

Repository:

https://github.com/bbvisual/PairTally_Benchmark

Dùng làm:

> **untouched final multi-object benchmark**

Không tune hyperparameter trên PairTally.

Đánh giá tách:

```text
Overall
INTER
INTRA
Strict unseen subset
```

---

# 10. Không dùng 20% PairTally để tune

PairTally official split hiện được phát hành như test benchmark.

Do đó:

```text
FSC-147 train
→ training

FSC-147 val
→ tune λ / hyperparameter

Synthetic FSC-147 val mosaics
→ tune mosaic-related settings

PairTally
→ final untouched test
```

Không nhìn PairTally để chọn:

```text
λ
β
threshold
mosaic ratio
```

---

# 11. Audit seen / unseen

Trước final report cần map:

```text
PairTally category
↓
FSC-147 train categories
```

Báo riêng:

```text
Overall
Seen categories
Unseen categories
INTER
INTRA
```

Lý do:

Nếu PairTally class đã xuất hiện trong FSC-147 train thì không nên gọi toàn bộ kết quả là strict zero-shot.

---

# 12. Core Method V3

Mục tiêu:

```text
Mosaic
→ dạy model khác target thì output phải khác

L_same
→ dạy model cùng target nhưng khác wording thì output phải ổn định
```

---

# 13. Mosaic Training

Lấy hai ảnh FSC-147 thuộc hai class khác nhau:

```text
Image A → apple
Image B → orange
```

Ghép thành:

```text
┌──────────────┬──────────────┐
│    APPLES    │   ORANGES    │
│              │              │
└──────────────┴──────────────┘
```

Nếu prompt:

```text
apple
```

GT density:

```text
┌──────────────┬──────────────┐
│ D_apple_GT   │      0       │
└──────────────┴──────────────┘
```

Nếu prompt:

```text
orange
```

GT:

```text
┌──────────────┬──────────────┐
│      0       │ D_orange_GT  │
└──────────────┴──────────────┘
```

Điểm quan trọng:

> Không cần random negative class.

Negative region đã chắc chắn đúng vì chính ta tạo ảnh mosaic.

---

# 14. Vì sao Mosaic tốt hơn random negative?

Random negative trên FSC-147 có vấn đề:

```text
target = apple
negative = cup
```

Ảnh vẫn có thể chứa cup nhưng không được annotate.

=> false negative.

Mosaic thì:

```text
left = apple image
right = orange image
```

với prompt apple:

```text
right-side density GT = 0
```

là supervision hợp lệ do data construction kiểm soát.

---

# 15. Tránh model học mẹo đường ghép

Không chỉ dùng một layout ngang cố định.

Nên random:

```text
horizontal
vertical
2×2
random crop ratio
random boundary location
```

Nếu cần có thể thêm:

```text
resize jitter
small overlap
boundary blending
```

Mục tiêu:

> model không được học “nửa trái luôn là positive”.

Final evaluation phải dùng ảnh thật PairTally.

---

# 16. Prompt Consistency Loss

Với cùng target:

```text
q1 = apple
q2 = apples
q3 = the apples
```

Ta muốn:

\[
D_{q_1}
\approx
D_{q_2}
\]

Một loss đơn giản:

\[
L_{same}
=
\|D_{q_1}-D_{q_2}\|_1
\]

hoặc MSE.

---

# 17. Total Loss

Baseline:

\[
L = L_{density}
\]

V3:

\[
\boxed{
L =
L_{density}
+
\lambda_m L_{mosaic}
+
\lambda_s L_{same}
}
\]

Trong đó:

- `L_density`: standard density supervision;
- `L_mosaic`: selective density supervision trên synthetic multi-class scene;
- `L_same`: equivalent-prompt consistency.

---

# 18. Ý nghĩa hai thành phần

## Mosaic

Dạy:

```text
apple ≠ orange
```

## L_same

Dạy:

```text
apple
≈
apples
≈
the apples
```

Hai thành phần bổ sung nhau:

```text
Mosaic
→ sensitivity

L_same
→ robustness
```

---

# 19. Ablation chính

Đây là bảng nên khóa:

| ID | Standard CLIP-Count | L_same | Mosaic |
|---|---:|---:|---:|
| E0 | ✓ | ✗ | ✗ |
| E1 | ✓ | ✓ | ✗ |
| E2 | ✓ | ✗ | ✓ |
| E3 | ✓ | ✓ | ✓ |

---

# 20. Hypothesis

Không coi đây là kết quả chắc chắn.

Hypothesis:

```text
E0
baseline

E1
Prompt robustness ↑
Target sensitivity có thể ↓

E2
Target sensitivity ↑

E3
Giữ được cả robustness và sensitivity tốt hơn
```

Nếu E1 thực sự làm robustness tốt lên nhưng sensitivity xấu đi:

> đó là một result quan trọng về trade-off.

---

# 21. Không nói mosaic “giải quyết hoàn toàn density supervision”

Nếu mosaic làm query sensitivity tốt hơn nhưng vẫn dùng density loss:

Ta có thể nói:

> Single-class supervision là một nguyên nhân quan trọng của query insensitivity, và density-map regression vẫn có khả năng học selective counting khi được cung cấp multi-class supervision phù hợp.

Không nói:

> Density map không phải vấn đề.

Vì chưa đủ bằng chứng để kết luận tuyệt đối.

---

# 22. Published metrics nên dùng lại

Để tránh tự tạo metric không cần thiết:

## Standard accuracy

```text
MAE
RMSE
```

## Negative-label / semantic grounding

Theo PrACo / PrACo++:

```text
NMN
PCCN
```

## Spatial / distractor evaluation

Theo PrACo++:

```text
CntP
CntR
CntF1
```

---

# 23. Metric riêng cho paraphrase robustness

Đây là phần mới cần đo riêng.

Giả sử:

```text
K prompt variants
```

cho cùng target.

## Average Prompt MAE

\[
APMAE
=
\frac{1}{NK}
\sum_i\sum_k
|\hat c_{ik}-c_i|
\]

Thấp hơn tốt hơn.

---

## Normalized Prompt Variation

\[
NPV
=
\frac{1}{N}
\sum_i
\frac{
std_k(\hat c_{ik})
}{
c_i+\epsilon
}
\]

Thấp hơn tốt hơn.

---

## Worst-Prompt MAE

\[
WPMAE
=
\frac1N
\sum_i
\max_k
|\hat c_{ik}-c_i|
\]

Đo worst-case wording.

---

# 24. Không dùng Prompt Stability một mình

Model bỏ qua text hoàn toàn có thể:

```text
mọi prompt → cùng output
```

và đạt variation rất thấp.

Do đó luôn báo:

```text
NPV
+
NMN/PCCN
+
CntF1
+
MAE
```

tức robustness và sensitivity phải đi cùng nhau.

---

# 25. POA chỉ là supplementary

Pairwise Order Accuracy:

\[
sign(\hat C_A-\hat C_B)
=
sign(C_A-C_B)
\]

có thể dùng như metric phụ.

Nhưng:

- random behavior có thể quanh 50%;
- không đo magnitude;
- 40 vs 39 vẫn được tính đúng direction.

Nếu dùng:

```text
POA
+
bootstrap confidence interval
```

và không coi đây là metric chính.

---

# 26. PairTally phải tách INTER và INTRA

Báo riêng:

```text
INTER
different object categories

INTRA
same object family
different attribute
```

Ví dụ:

```text
tomato vs chili
```

khác với:

```text
red apple vs green apple
```

INTRA khó hơn và gần semantic fine-grained discrimination hơn.

---

# 27. PairTally có thể rất khó cho CLIP-Count

Điều này không làm đề tài thất bại.

Mục tiêu không phải SOTA PairTally.

Mục tiêu là:

```text
E0 vs E1 vs E2 vs E3
```

và xem:

- semantic grounding;
- paraphrase robustness;
- multi-class selectivity;

thay đổi thế nào.

---

# 28. P0 đầu tiên: test CLIP-Count trên ảnh PairTally lớn

Trước khi viết toàn bộ adapter:

Chạy:

```text
5 PairTally images
```

Kiểm tra:

```text
official sliding-window inference
density size
density sum
runtime
GPU memory
```

Nếu ổn mới mở rộng toàn dataset.

---

# 29. VA-Count diagnostic

Chỉ làm subset nhỏ:

```text
30–50 cases
```

Flow:

```text
Prompt
 ↓
Grounding DINO
 ↓
all detections
 ↓
VA-Count
 ↓
density
```

Cần đo:

```text
GDINO precision
GDINO recall
GDINO box count
VA-Count count
```

---

# 30. Grounding DINO-only baseline bắt buộc

Nếu Grounding DINO trả box:

\[
C_{GDINO}
=
\#boxes
\]

Phải so:

```text
GDINO-only
vs
VA-Count
```

Nếu GDINO đã đếm tốt ngang VA-Count:

> không được nói gate cải thiện counter nếu thực chất detector đã giải được bài toán.

---

# 31. Không mặc định “Grounding DINO đúng”

Đặc biệt PairTally INTRA:

```text
red apple
vs
green apple
```

Grounding DINO có thể tự nó đã fail.

Do đó phải kiểm tra:

```text
precision
recall
```

trước khi kết luận lỗi nằm ở counter.

---

# 32. Hard/Soft Gate chuyển thành optional

Nếu còn thời gian:

## Hard

\[
D'=D\cdot M
\]

## Soft

\[
D'
=
D[
\beta+(1-\beta)M
]
\]

Nhưng không để gate thành core contribution nữa.

Core vẫn là:

```text
CLIP-Count
+
Mosaic
+
L_same
```

---

# 33. Contrastive Density bỏ khỏi core

V2 từng có:

\[
D_A'
=
ReLU(D_A-\alpha D_B)
\]

Nhưng nếu:

\[
D_A\approx D_B
\]

thì:

\[
D_A'
\approx
(1-\alpha)D_A
\]

nó chỉ scale density chứ không tạo discrimination mới.

Do đó:

> bỏ khỏi contribution chính.

Nếu muốn giữ thì chỉ làm appendix/no-train baseline.

---

# 34. Scope cuối cùng

# MUST HAVE

- CLIP-Count reproduce
- FSC-147
- PrACo / PrACo++ protocol
- NMN
- PCCN
- CntP
- CntR
- CntF1
- paraphrase robustness evaluation
- APMAE
- NPV
- WPMAE
- E0
- E1
- E2
- E3
- PairTally final test
- INTER / INTRA breakdown
- seen / unseen audit
- small VA-Count + GDINO diagnostic

---

# SHOULD HAVE

- bootstrap CI cho supplementary metrics
- qualitative density visualization
- hard / soft gate
- prompt-family breakdown

---

# NICE TO HAVE

- T2ICount
- extra dataset
- more advanced query-aware module

---

# 35. Những thứ bỏ khỏi scope chính

- REC-8K
- full T2ICount training
- count-only training
- contrastive density contribution
- full VA-Count retraining
- tự tạo X/Y dataset mới
- random negative class trên FSC-147

---

# 36. Lịch 4 tuần V3

# TUẦN 1 — Reproduce + Evaluation

## Mục tiêu

Cuối tuần phải có baseline table.

### Làm

```text
CLIP-Count pretrained
↓
FSC-147 val/test
```

Implement / reproduce:

```text
MAE
RMSE
NMN
PCCN
CntP
CntR
CntF1
```

Sau đó:

```text
5–20 PairTally images
```

để kiểm tra:

```text
resolution
sliding-window
memory
runtime
density map
```

### Deliverable

```text
baseline_results.csv
eval_praco.py
eval_prompt_robustness.py
pairtally_adapter.py
```

---

# TUẦN 2 — Mosaic + Prompt Paraphrase

## Mosaic dataloader

Random:

```text
horizontal
vertical
2×2
random split ratio
```

Tạo synthetic validation mosaic từ FSC-147 val.

## Prompt set

Ví dụ:

```text
apple
apples
the apples
all apples in the image
objects that are apples
```

Không thêm attribute không tồn tại trong GT.

### Deliverable

```text
mosaic_dataset.py
prompt_templates.json
mosaic_visualization.ipynb
```

---

# TUẦN 3 — Train E1 / E2 / E3

E0:

```text
original checkpoint
```

Train:

```text
E1 = +L_same
E2 = +Mosaic
E3 = +Mosaic + L_same
```

Tune hyperparameters trên:

```text
FSC-147 val
+
synthetic mosaic val
```

Không tune trên PairTally.

### Deliverable

```text
checkpoints/E1/
checkpoints/E2/
checkpoints/E3/
training_logs/
```

---

# TUẦN 4 — Final Evaluation

Chạy:

```text
E0
E1
E2
E3
```

trên:

```text
FSC-147
PrACo-style protocol
PairTally
```

PairTally:

```text
Overall
INTER
INTRA
Seen
Unseen
```

Làm:

```text
tables
plots
density maps
failure cases
demo
report
slides
```

---

# 37. Fallback plan

Nếu training lỗi:

Vẫn còn:

```text
PrACo/PrACo++ reproduction
+
paraphrase robustness benchmark
+
PairTally evaluation
+
VA-Count/GDINO diagnosis
```

Nếu E2 chạy được mà E3 fail:

```text
E0 vs E1 vs E2
```

vẫn đủ phân tích.

Nếu chỉ E0 chạy:

tập trung thành:

> systematic diagnostic study

nhưng contribution method sẽ yếu hơn.

---

# 38. Contribution viết lại

Không claim:

> first prompt-grounding benchmark

Không claim:

> first mosaic training

Không claim:

> first multi-object counting

Nên viết:

### Contribution 1

> We study two complementary dimensions of query fidelity in text-guided zero-shot counting: invariance to semantically equivalent prompt formulations and sensitivity to changes in the requested target.

### Contribution 2

> We investigate multi-category mosaic supervision for CLIP-Count to provide explicit target-vs-distractor supervision while retaining density-map regression.

### Contribution 3

> We combine selective mosaic supervision with equivalent-prompt consistency and analyze the trade-off between linguistic robustness and semantic discrimination using established semantic-grounding metrics together with a dedicated paraphrase-robustness evaluation.

---

# 39. Storyline bảo vệ

## Slide 1

```text
Zero-shot counting:
Tell the model what to count.
```

Câu hỏi:

> Does the model really understand both the meaning and the wording of the query?

---

## Slide 2 — Prior Work

```text
PrACo / PrACo++
→ models may ignore prompts
```

Không claim phát hiện này là của mình.

---

## Slide 3 — Our Question

```text
Same target
different wording
→ stable

Different target
same image
→ sensitive
```

---

## Slide 4 — Why standard FSC supervision is limited

```text
one annotated target per image
```

ít explicit selective pressure.

---

## Slide 5 — Proposed Training

```text
Mosaic
→ discrimination

L_same
→ wording robustness
```

---

## Slide 6 — Ablation

```text
E0
E1
E2
E3
```

---

## Slide 7 — Metrics

```text
MAE / RMSE
NMN / PCCN
CntP / CntR / CntF1
APMAE / NPV / WPMAE
```

---

## Slide 8 — PairTally

```text
INTER
INTRA
seen
unseen
```

---

## Slide 9 — Diagnostic VA-Count

```text
GDINO precision/recall
GDINO-only count
VA-Count count
```

---

## Slide 10 — Final message

# Stable when wording changes. Sensitive when the target changes.

---

# 40. Những câu muốn người review phản biện tiếp

1. Research question hiện đã đủ khác PrACo/PrACo++ chưa?
2. `Mosaic + L_same` có phải combination đủ hợp lý để làm main method không?
3. Có paper nào đã làm đúng combination này trên CLIP-Count chưa?
4. Bộ metric hiện đã đủ chưa hay vẫn còn thừa?
5. Có nên giữ VA-Count diagnostic hay bỏ hẳn để giảm scope?
6. Seen/unseen mapping nên định nghĩa strict thế nào?
7. Prompt paraphrase nên sinh bằng template cố định hay LLM rồi manual filter?
8. Mosaic layout random như trên đã đủ tránh shortcut chưa?
9. Có cần train E1 hay chỉ E0/E2/E3 để tiết kiệm thời gian?
10. Với khoảng 4 tuần, phần nào nên cắt đầu tiên nếu trễ tiến độ?

---

# 41. Các nguồn chính để kiểm tra

- CLIP-Count  
  https://github.com/songrise/CLIP-Count

- VA-Count  
  https://github.com/HopooLinZ/VA-Count

- T2ICount  
  https://github.com/cha15yq/T2ICount

- Zero-Shot Counting CVPR 2023  
  https://github.com/cvlab-stonybrook/zero-shot-counting

- PairTally  
  https://github.com/bbvisual/PairTally_Benchmark

- PairTally paper  
  https://arxiv.org/abs/2509.13939

- PrACo — Mind the Prompt  
  https://arxiv.org/abs/2409.15953

- PrACo++ / MUCCA — Does it Really Count?  
  https://arxiv.org/abs/2605.02752

- CountEx  
  https://arxiv.org/abs/2602.19432

- MixCount  
  https://arxiv.org/abs/2605.18063

---

# 42. Chốt V3

Hướng hiện tại:

```text
                        QUERY FIDELITY
                              │
            ┌─────────────────┴─────────────────┐
            │                                   │
            ↓                                   ↓
     PROMPT ROBUSTNESS                 TARGET SENSITIVITY
            │                                   │
      equivalent wording                different object
            │                                   │
            └─────────────────┬─────────────────┘
                              ↓
                          CLIP-COUNT
                              │
                 ┌────────────┴────────────┐
                 ↓                         ↓
              L_same                  Mosaic Training
                 │                         │
                 ↓                         ↓
             robustness                discrimination
                 └────────────┬────────────┘
                              ↓
                          E0/E1/E2/E3
                              ↓
            FSC-147 + PrACo protocol + PairTally
                              ↓
          MAE/RMSE + NMN/PCCN + CntF1 + NPV/WPMAE
```

VA-Count:

```text
diagnostic only
↓
Grounding DINO precision/recall
↓
GDINO-only vs VA-Count
```

Thông điệp cuối:

> **Mục tiêu không còn là chứng minh model “không nghe prompt” — PrACo đã làm điều đó. Mục tiêu là nghiên cứu xem một counter có thể đồng thời ổn định trước biến đổi ngôn ngữ và vẫn đủ phân biệt khi target thay đổi hay không, và liệu multi-class mosaic supervision kết hợp prompt consistency có giúp cân bằng hai yêu cầu này hay không.**
