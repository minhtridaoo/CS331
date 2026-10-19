# CS331 UIT — Đề xuất hướng đồ án Zero-Shot Object Counting
## Bản V2 để review: Query Sensitivity + Prompt Robustness

**Mục tiêu của tài liệu này:**  
Tóm gọn hướng đồ án hiện tại để một người khác có thể đọc, phản biện và kiểm tra xem hướng nghiên cứu có hợp lý, khả thi và bám đúng vấn đề giảng viên đưa ra hay không.

---

# 1. Bài toán gốc

Đề tài môn CS331:

> **Đếm đối tượng trong ảnh theo phương pháp Zero-Shot Object Counting (ZSC).**

Các tài liệu thầy gợi ý:

- Zero-Shot Object Counting — CVPR 2023  
  https://github.com/cvlab-stonybrook/zero-shot-counting
- VA-Count — ECCV 2024  
  https://github.com/HopooLinZ/VA-Count
- T2ICount — CVPR 2025  
  https://github.com/cha15yq/T2ICount

Ba vấn đề thầy nêu cần nghiên cứu thêm:

1. Các mô hình hiện tại học từ **ground-truth density map**, nên có nguy cơ phụ thuộc mạnh vào cấu trúc density thay vì thực sự hiểu đối tượng mà prompt yêu cầu.
2. **Grounding DINO có thể xác định đúng đối tượng**, nhưng vùng/density mà VA-Count dùng để đếm sau đó vẫn sai.
3. Cùng một ảnh:
   - hỏi đếm X → ra đúng;
   - hỏi đếm Y → kết quả lại gần giống X;
   - dù X và Y là hai đối tượng khác nhau.

---

# 2. Vì sao roadmap cũ cần sửa?

Roadmap cũ đề xuất:

```text
VA-Count
+
Region Loss
+
Prompt Contrastive Loss
```

Ý tưởng này bám đúng vấn đề thầy nhưng có một lỗi kiến trúc quan trọng:

## VA-Count counter không nhận text trực tiếp

Trong mã nguồn VA-Count, counter chính nhận:

```text
image
+
exemplar boxes/patches
+
shot number
```

Text được Grounding DINO xử lý ở bước trước để sinh exemplar.

Luồng thực tế:

```text
Text
 ↓
Grounding DINO
 ↓
Candidate exemplar patches
 ↓
VA-Count counter
 ↓
Density map
```

Vì vậy:

```text
L_same(prompt1, prompt2)
L_diff(promptX, promptY)
```

không có vị trí tự nhiên để gắn trực tiếp vào VA-Count counter.

Do đó:

> **VA-Count không nên là mô hình chính để train prompt loss.**

---

# 3. Mô hình phù hợp hơn: CLIP-Count

CLIP-Count là mô hình Zero-Shot Counting nhận text trực tiếp.

Repository:

https://github.com/songrise/CLIP-Count

Luồng chính:

```text
Image
  ↓
Image Encoder
  ↓
Visual Feature
       ↕
   Text Feature
       ↑
Text Prompt

       ↓
Interaction
       ↓
Density Map
       ↓
Count
```

Trong code chính thức, text embedding được truyền trực tiếp vào:

- visual encoder
- decoder

Do đó CLIP-Count phù hợp hơn để nghiên cứu:

```text
same prompt meaning
vs
different object prompt
```

---

# 4. Ý tưởng trung tâm của đồ án

Tên gợi ý:

# Evaluating and Improving Query Sensitivity in Zero-Shot Object Counting

Hoặc:

# Robust to Wording, Sensitive to Objects: Query Fidelity in Zero-Shot Object Counting

---

# 5. Research Question chính

Một mô hình Zero-Shot Object Counting tốt phải thỏa mãn **hai yêu cầu ngược nhau nhưng bổ sung cho nhau**.

## 5.1. Cùng một đối tượng → phải ổn định

Ví dụ:

```text
"apple"
"red apples"
"apples on the table"
```

Nếu đều chỉ cùng một nhóm đối tượng thì:

```text
Count ≈ giống nhau
Density map ≈ giống nhau
```

Đây là:

> **Prompt Robustness**

---

## 5.2. Khác đối tượng → phải nhạy

Cùng một ảnh:

```text
Prompt A = "apple"
Prompt B = "orange"
```

Nếu ảnh có:

```text
8 apples
3 oranges
```

thì model phải cho:

```text
apple → ~8
orange → ~3
```

chứ không phải:

```text
apple → 8
orange → 8
```

Đây là:

> **Query Sensitivity**

---

# 6. Tại sao phải nghiên cứu cả hai?

Nếu chỉ tối ưu Prompt Robustness:

```text
"apple"
"red apple"
"apple on table"
```

đều ra giống nhau.

Nghe có vẻ tốt.

Nhưng một model **bỏ qua text hoàn toàn** cũng sẽ:

```text
mọi prompt → cùng prediction
```

=> Prompt Stability rất tốt nhưng model vô dụng.

Ngược lại:

Nếu chỉ tối ưu sensitivity:

```text
apple ≠ orange
```

mà mỗi cách diễn đạt khác nhau của `"apple"` lại làm kết quả dao động mạnh thì cũng chưa tốt.

Do đó hai yêu cầu phải được đánh giá đồng thời:

```text
SAME TARGET
→ Stable

DIFFERENT TARGET
→ Sensitive
```

Đây là phần cốt lõi nhất của hướng nghiên cứu.

---

# 7. Phân vai các mô hình

## Mô hình chính để train

# CLIP-Count

Vai trò:

- baseline chính
- nghiên cứu prompt
- train `L_same`
- thử các cơ chế cải thiện query sensitivity

---

## VA-Count

Không dùng làm model chính để train prompt loss.

Vai trò:

> **chẩn đoán vấn đề vùng**

Dùng để kiểm tra:

```text
Grounding DINO đúng
↓
nhưng density map VA-Count vẫn lan sai
```

---

## T2ICount

Vai trò:

> strong pretrained reference

Không ưu tiên train lại vì:

- nặng hơn
- dựa trên Stable Diffusion
- mất nhiều thời gian setup/debug

Chỉ cần chạy checkpoint nếu khả thi.

---

# 8. Benchmark quan trọng: PairTally

Repository:

https://github.com/bbvisual/PairTally_Benchmark

Paper:

https://arxiv.org/abs/2509.13939

PairTally được thiết kế để trả lời câu hỏi:

> **Can current models count what we mean, not simply what they see?**

## Dataset

- 681 ảnh
- mỗi ảnh có hai nhóm đối tượng
- 54 categories
- 98 subcategories

Có hai loại:

### INTER-category

Ví dụ:

```text
tomato
vs
chili
```

### INTRA-category

Ví dụ:

```text
red apple
vs
green apple
```

hoặc:

```text
big marble
vs
small marble
```

---

# 9. PairTally có annotation đủ mạnh

Mỗi ảnh có:

```text
points
negative_points

positive_prompt
negative_prompt

positive boxes
negative boxes
```

Do đó có thể đánh giá:

```text
Count X
Count Y
Density X
Density Y
Density leakage
```

mà không cần tự gán thêm 50–100 ảnh như roadmap cũ.

---

# 10. Lưu ý quan trọng về novelty

Không được claim:

> “Chúng tôi tạo benchmark đầu tiên để kiểm tra X/Y.”

PairTally đã làm việc đó.

Contribution phù hợp hơn:

> **Đánh giá có hệ thống các text-guided zero-shot counting models trên bài toán query fidelity, đồng thời thử các cải tiến nhẹ để tăng robustness và sensitivity.**

Một khoảng trống thực nghiệm đáng chú ý:

PairTally công bố kết quả cho nhiều model như:

```text
CountGD
DAVE
GeCo
LoCA
FamNet
VLMs
...
```

nhưng repository hiện không liệt kê trực tiếp:

```text
CLIP-Count
VA-Count
T2ICount
```

Do đó việc benchmark các model ZSC dạng này trên PairTally vẫn có giá trị thực nghiệm.

---

# 11. Related Work cần bổ sung

## PairTally — DICTA 2025

Benchmark fine-grained selective counting.

## CountEx — ECCV 2026

Hướng inclusion/exclusion:

```text
what to count
+
what not to count
```

Do đó nếu đồ án dùng ý tưởng positive/negative prompt thì không được claim hoàn toàn mới.

## QICA — CVPR 2026

Tiếp tục nghiên cứu vấn đề:

- quantitative awareness
- spatial awareness
- query-conditioned counting

Điểm này cho thấy vấn đề thầy đưa ra vẫn còn rất mới.

---

# 12. Dataset chính

## Dataset A — FSC-147

Dùng để:

```text
train CLIP-Count
benchmark chuẩn
MAE
RMSE
```

Điểm yếu:

FSC-147 thường chỉ annotate một target category mỗi ảnh.

Do đó không phù hợp để đo đầy đủ:

```text
X vs Y trong cùng ảnh
```

---

## Dataset B — PairTally

Dùng để:

```text
query sensitivity
fine-grained discrimination
CPL
pairwise comparison
```

Đây là dataset bắt buộc của hướng mới.

---

## Dataset C — FSC-147-S-v2

Từ T2ICount.

Dùng như semantic stress-test bổ sung.

---

## Dataset D — REC-8K

CVPR 2024.

Có referring expression như:

```text
red apple
green apple
person standing
person sitting
```

Rất phù hợp kiểm tra attribute-aware counting.

Nhưng:

> Priority 2.

Chỉ dùng nếu PairTally + FSC-147 đã chạy ổn.

---

# 13. Experiment 1 — Query Dependence Test

Không cần train.

Cùng một ảnh, chạy:

```text
Correct prompt
Wrong prompt
Blank prompt
Random prompt
```

Ví dụ:

```text
Image contains apples

"apple"       → 38
"orange"      → 37
"banana"      → 38
""            → 36
```

Nếu output gần như giống nhau:

> model có độ nhạy với query thấp.

Đo:

```text
ΔCount
Density-map similarity
```

Lưu ý:

Thí nghiệm này chứng minh:

> query insensitivity

Nó **không đủ để chứng minh trực tiếp** rằng nguyên nhân chắc chắn là ground-truth density map.

---

# 14. Experiment 2 — Prompt Robustness

Cùng target:

```text
apple
red apples
apples in the image
```

Đo:

## Prompt Stability

Ví dụ:

```text
std(counts)
```

hoặc normalized deviation.

## Worst-Prompt MAE

Lấy prompt gây lỗi nặng nhất.

Metric này giúp trả lời:

> Model có ổn định khi người dùng diễn đạt cùng một đối tượng bằng nhiều cách hay không?

---

# 15. Experiment 3 — Pairwise Query Sensitivity

Trên PairTally:

```text
Image:
A count = 40
B count = 15
```

Model:

```text
Pred A
Pred B
```

Dùng metric:

# Pairwise Order Accuracy

\[
POA =
\frac{
\#[
sign(\hat C_A-\hat C_B)
=
sign(C_A-C_B)
]
}{
N
}
\]

Ý nghĩa:

> model có ít nhất hiểu đối tượng nào nhiều hơn đối tượng nào hay không.

Ưu điểm:

- không cần threshold epsilon
- dễ giải thích

Lưu ý:

Nếu:

```text
GT A = GT B
```

thì bỏ cặp đó khỏi metric và báo số lượng cặp bị loại.

---

# 16. Experiment 4 — Cross-Prompt Leakage

PairTally có vị trí của cả hai lớp.

Ví dụ:

Prompt:

```text
apple
```

Density dự đoán:

```text
D_apple
```

Ground-truth vùng orange:

```text
R_orange
```

Định nghĩa:

\[
CPL_{apple} =
\frac{
\sum_{(x,y)\in R_{orange}}D_{apple}(x,y)
}{
\sum_{x,y}D_{apple}(x,y)
}
\]

CPL thấp:

```text
model tập trung đúng target
```

CPL cao:

```text
density bị leak sang distractor
```

---

# 17. Experiment 5 — VA-Count spatial diagnosis

VA-Count chỉ dùng để kiểm tra vấn đề số 2 của thầy.

Pipeline:

```text
Prompt
 ↓
Grounding DINO
 ↓
ALL detections
 ↓
VA-Count
 ↓
Density
```

So sánh:

```text
No gate
Hard gate
Soft gate
```

---

# 18. Không được dùng top-3 exemplar làm mask

VA-Count dùng top exemplar cho counter.

Nhưng nếu ảnh có:

```text
100 apples
```

top-3 exemplar chỉ chứa:

```text
3 apples
```

Nếu mask density bằng top-3 box thì chắc chắn sai.

Phải lấy:

> **toàn bộ Grounding DINO detections trước bước top-k exemplar selection**

---

# 19. Hard Gate baseline

\[
D' = D\cdot M
\]

Trong đó:

```text
M = union of all target detection boxes
```

Ưu:

- cực đơn giản
- không cần train

Nhược:

Grounding DINO miss object thì:

```text
density đúng cũng bị xóa
```

---

# 20. Soft Gate baseline

Đề xuất:

\[
D' =
D\cdot
[\beta+(1-\beta)M]
\]

với:

\[
0<\beta<1
\]

Trong box:

```text
weight = 1
```

Ngoài box:

```text
weight = β
```

Do đó model vẫn có khả năng đếm object bị Grounding DINO miss.

So sánh:

```text
No Gate
Hard Gate
Soft Gate
```

Đây là thí nghiệm đơn giản nhưng rất dễ giải thích khi bảo vệ.

---

# 21. Training chính — L_same

Baseline:

\[
L=L_{density}
\]

Thêm:

\[
L =
L_{density}
+
\lambda L_{same}
\]

Với hai prompt cùng target:

```text
q1 = apple
q2 = red apples
```

Ta muốn:

\[
D_{q1}\approx D_{q2}
\]

Có thể dùng:

\[
L_{same}
=
\|D_{q1}-D_{q2}\|_1
\]

hoặc MSE.

---

# 22. Không nên random negative class trên FSC-147

Ý tưởng cũ:

```text
Image target = apple
Random negative = cup
→ force count(cup)=0
```

có vấn đề.

FSC-147 chỉ annotate target class chính.

Ảnh apple vẫn có thể chứa cup nhưng không được annotate.

Khi đó:

```text
cup = 0
```

là false negative.

Vì vậy:

> Không sử dụng negative prompt ngẫu nhiên trên FSC-147 nếu không xác minh object thật sự vắng mặt.

---

# 23. Contrastive inference không cần train

Trên PairTally đã biết:

```text
A
B
```

Có thể chạy:

\[
D_A
\]

và:

\[
D_B
\]

sau đó thử:

\[
D_A' =
ReLU(D_A-\alpha D_B)
\]

Tương tự:

\[
D_B' =
ReLU(D_B-\alpha D_A)
\]

Đây là một baseline nhẹ:

```text
what to count
-
what not to count
```

Không claim là concept hoàn toàn mới vì CountEx 2026 đã nghiên cứu inclusion/exclusion sâu hơn.

---

# 24. Metric cuối cùng

## Counting Accuracy

```text
MAE ↓
RMSE ↓
```

## Same-target Robustness

```text
Prompt Stability ↓
Worst-Prompt MAE ↓
```

## Different-target Sensitivity

```text
Pairwise Order Accuracy ↑
Cross-Prompt Leakage ↓
```

## Query Dependence

```text
ΔCount(correct, wrong) ↑
Density similarity(correct, wrong) ↓
```

Không đọc từng metric riêng lẻ.

Ví dụ:

```text
PS rất tốt
```

nhưng:

```text
POA rất thấp
```

có thể nghĩa là model đang bỏ qua prompt.

---

# 25. Ablation hợp lý

Không train 5–10 model nặng.

Tối thiểu:

| ID | Model |
|---|---|
| E0 | CLIP-Count pretrained/original |
| E1 | CLIP-Count + L_same |
| E2 | Contrastive inference |
| E3 | CLIP-Count + L_same + contrastive inference |

VA-Count:

| ID | Mode |
|---|---|
| V0 | Original |
| V1 | Hard spatial gate |
| V2 | Soft spatial gate |

Nếu còn thời gian mới thêm module khác.

---

# 26. Optional experiment cho vấn đề density supervision

Nếu đủ thời gian:

Baseline:

\[
L_{density}
\]

Thử:

\[
L_{count}
=
|\sum D-C_{GT}|
\]

và:

\[
L_{hybrid}
=
\alpha L_{density}
+
L_{count}
\]

So sánh:

```text
Density-only
Count-only
Hybrid
```

Mục tiêu:

> kiểm tra trực tiếp mức độ cần thiết của pixel-level density supervision.

Đây mới là thí nghiệm bám trực tiếp vấn đề số 1 của thầy.

Nhưng đây là:

> **Optional**

vì có thể tốn thời gian và làm training không ổn định.

---

# 27. Lịch triển khai khoảng 4 tuần

# TUẦN 1 — Baseline + Evaluation Infrastructure

Mục tiêu:

> cuối tuần phải có bảng baseline.

Làm:

```text
CLIP-Count → FSC-147
CLIP-Count → PairTally

VA-Count → diagnostic subset
T2ICount → PairTally/FSC nếu checkpoint chạy được
```

Implement:

```text
MAE
RMSE
Prompt Stability
Worst-Prompt MAE
POA
CPL
```

Thêm:

```text
Correct Prompt
Wrong Prompt
Blank Prompt
Random Prompt
```

Deliverable:

```text
baseline_results.csv
pairtally_eval.py
prompt_sensitivity_eval.py
```

---

# TUẦN 2 — No-Train Methods

CLIP-Count:

```text
Prompt ensemble
Contrastive density
```

VA-Count:

```text
No Gate
Hard Gate
Soft Gate
```

Deliverable:

```text
inference_ablation.csv
visualizations/
```

Đây là lớp bảo hiểm:

> Nếu tuần 3 train thất bại thì tuần 1–2 vẫn tạo thành một nghiên cứu thực nghiệm hoàn chỉnh.

---

# TUẦN 3 — Train CLIP-Count

Tối thiểu:

```text
Original
+ L_same
```

Nếu ổn mới thêm:

```text
verified negative training
```

Không random negative bừa.

Lưu:

```text
checkpoint mỗi epoch
training log
validation metrics
```

---

# TUẦN 4 — Final Evaluation + Report

Không thêm module mới.

Làm:

```text
final evaluation
ablation
failure analysis
figures
demo
report
slides
```

Demo:

```text
same image

apple → 8
orange → 3

vs baseline

apple → 8
orange → 8
```

---

# 28. Fallback Plan

## Nếu train thành công

Contribution:

```text
evaluation
+
L_same
+
contrastive inference
+
spatial diagnosis
```

## Nếu train thất bại

Vẫn còn:

```text
systematic benchmark
+
PairTally evaluation
+
query sensitivity diagnosis
+
VA-Count spatial gate analysis
+
no-train improvements
```

=> vẫn có thể làm thành một đồ án hoàn chỉnh.

---

# 29. Contribution nên viết thế nào?

Không viết:

> “We propose the first solution for fine-grained zero-shot counting.”

Nên viết:

> Existing ZSC benchmarks can hide query insensitivity because many images focus on one annotated target. We systematically evaluate whether text-guided zero-shot counters are stable to equivalent wording yet sensitive to changes in the requested target, and investigate lightweight mechanisms to improve these behaviors.

Ba contribution hợp lý:

### Contribution 1

Systematic evaluation of:

```text
Prompt Robustness
+
Query Sensitivity
```

trên text-guided Zero-Shot Counting.

### Contribution 2

Evaluate ZSC models on:

```text
PairTally
```

để đo:

```text
X vs Y
```

thay vì chỉ one-target FSC-147.

### Contribution 3

Investigate lightweight improvements:

```text
L_same
contrastive density
soft spatial gating
```

---

# 30. Storyline khi bảo vệ

## Slide 1

```text
Zero-shot counting says:
"Tell me what to count."
```

Câu hỏi:

> Does the model actually listen?

---

## Slide 2

Ảnh:

```text
8 apples
3 oranges
```

Model:

```text
apple → 8
orange → 8
```

---

## Slide 3

Hai yêu cầu:

```text
same meaning
→ stable

different target
→ sensitive
```

---

## Slide 4

FSC-147 không đủ để kiểm tra đầy đủ X/Y.

Giới thiệu:

```text
PairTally
```

---

## Slide 5

Baseline:

```text
CLIP-Count
VA-Count
T2ICount
```

---

## Slide 6

Metrics:

```text
MAE
RMSE
PS
POA
CPL
```

---

## Slide 7

Diagnosis:

```text
correct / wrong / blank / random prompt
```

---

## Slide 8

Improvement:

```text
L_same
Contrastive Density
Soft Spatial Gate
```

---

## Slide 9

Ablation.

---

## Slide 10

Demo:

```text
What do you want to count?
```

---

# 31. Những câu thầy có thể hỏi

## “Sao không nhân mask Grounding DINO luôn?”

Trả lời:

> Đó chính là hard-gate baseline. Tuy nhiên Grounding DINO có thể miss object, đặc biệt trong ảnh đông vật. Vì vậy nhóm so sánh no gate, hard gate và soft gate.

---

## “Tại sao không train VA-Count?”

Trả lời:

> Text không đi trực tiếp vào counter của VA-Count. Nó chỉ ảnh hưởng quá trình chọn exemplar trước counter. Vì vậy prompt-level loss phù hợp hơn với CLIP-Count, còn VA-Count được dùng để phân tích lỗi spatial grounding.

---

## “Prompt Stability thấp có chắc model tốt?”

Trả lời:

> Không. Model bỏ qua text hoàn toàn cũng có stability cao. Vì vậy phải báo stability cùng query sensitivity như Pairwise Order Accuracy và Cross-Prompt Leakage.

---

## “Làm sao biết wrong prompt thật sự không có trong ảnh?”

Trả lời:

> Với FSC-147 không thể đảm bảo vì dataset chỉ annotate target chính. Vì vậy không ép random negative = 0 khi train nếu chưa xác minh.

---

## “CPL lấy ground truth ở đâu?”

Trả lời:

> PairTally có annotation riêng cho cả positive và negative objects, bao gồm point và bounding-box information.

---

## “Em có giải quyết vấn đề density-map supervision không?”

Trả lời an toàn:

> Phần chính của đồ án trước hết chẩn đoán query insensitivity. Nếu thời gian cho phép, nhóm sẽ làm ablation density-only vs count-only vs hybrid để kiểm tra trực tiếp ảnh hưởng của density supervision.

---

# 32. Các rủi ro chính

## Risk 1 — CLIP-Count không reproduce được

Giải pháp:

```text
pretrained checkpoint
+
inference study
```

---

## Risk 2 — PairTally adapter khó viết

Dataset đã có format tương thích khá gần FSC-147 và có evaluation template.

---

## Risk 3 — VA-Count Grounding DINO quá chậm

Chỉ chạy:

```text
diagnostic subset
```

không nhất thiết toàn bộ PairTally.

---

## Risk 4 — T2ICount setup fail

T2ICount là:

```text
reference model
```

không phải dependency của contribution chính.

---

## Risk 5 — L_same làm model quá invariant

Đây thậm chí có thể trở thành một kết quả nghiên cứu tốt:

```text
L_same
→ Prompt Stability tốt hơn

nhưng
→ Query Sensitivity giảm
```

Nếu xảy ra:

> chứng minh rằng robustness và sensitivity có trade-off.

---

# 33. Scope cuối cùng

## MUST HAVE

- CLIP-Count baseline
- FSC-147
- PairTally
- MAE/RMSE
- Prompt robustness test
- Query sensitivity test
- POA
- CPL
- correct/wrong/random prompt diagnosis
- VA-Count spatial diagnosis
- hard/soft gate baseline

## SHOULD HAVE

- L_same training
- contrastive density inference
- T2ICount reference

## NICE TO HAVE

- REC-8K
- density-only vs count-only supervision
- verified-negative training
- more sophisticated query-aware module

---

# 34. Kết luận

Hướng cuối:

```text
                   ZERO-SHOT COUNTING
                          │
           ┌──────────────┴───────────────┐
           │                              │
           ↓                              ↓
       ROBUSTNESS                     SENSITIVITY
           │                              │
same wording variants             different objects
           │                              │
           └──────────────┬───────────────┘
                          ↓
                      CLIP-COUNT
                       main model
                          │
                 ┌────────┴────────┐
                 ↓                 ↓
              L_same       contrastive density
                          │
                          ↓
                       PairTally


                    VA-COUNT
                       │
             spatial diagnosis only
                       │
         No Gate / Hard Gate / Soft Gate


                    T2ICOUNT
                       │
              pretrained reference
```

Thông điệp cuối cùng:

> **Một Zero-Shot Counter tốt không chỉ cần giữ kết quả ổn định khi người dùng diễn đạt cùng một ý theo nhiều cách, mà còn phải thay đổi đúng khi người dùng thực sự đổi đối tượng cần đếm.**

Hay ngắn hơn:

# Stable when wording changes. Sensitive when the target changes.

---

# 35. Các nguồn chính để người review kiểm tra

- Zero-Shot Object Counting  
  https://github.com/cvlab-stonybrook/zero-shot-counting

- CLIP-Count  
  https://github.com/songrise/CLIP-Count

- VA-Count  
  https://github.com/HopooLinZ/VA-Count

- T2ICount  
  https://github.com/cha15yq/T2ICount

- PairTally  
  https://github.com/bbvisual/PairTally_Benchmark

- PairTally paper  
  https://arxiv.org/abs/2509.13939

- REC-8K — CVPR 2024  
  https://openaccess.thecvf.com/content/CVPR2024/papers/Dai_Referring_Expression_Counting_CVPR_2024_paper.pdf

---

# 36. Những điểm muốn người review phản biện

Khi đọc file này, hãy tập trung phản biện các câu hỏi:

1. Research question có đủ rõ không?
2. Việc chọn CLIP-Count làm model train chính có hợp lý không?
3. Có metric nào đang đo trùng nhau hoặc thiếu không?
4. POA + CPL có đủ để chứng minh query sensitivity không?
5. L_same có khả năng gây model bỏ qua text nhiều hơn không?
6. Contrastive density có hợp lý về mặt toán học không?
7. Hard/Soft Grounding DINO gate có phải baseline công bằng không?
8. Contribution có đủ cho đồ án CS331 hay còn quá thiên về benchmark?
9. Có experiment nào nên bỏ vì quá tốn thời gian?
10. Có cách nào kiểm tra trực tiếp vấn đề density-map supervision với chi phí thấp hơn không?
