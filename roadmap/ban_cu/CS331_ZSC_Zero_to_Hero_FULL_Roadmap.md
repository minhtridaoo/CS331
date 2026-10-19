# CS331 UIT — Zero-Shot Object Counting (ZSC)
## Roadmap Zero → Hero trong 2 tháng + Hướng nghiên cứu đồ án

**Môn:** CS331 — UIT  
**Giảng viên:** Thầy Mai Tiến Dũng  
**Chủ đề:** Zero-Shot Object Counting (ZSC)  
**Mục tiêu:** Hoàn thành đồ án có chiều sâu nghiên cứu, có baseline, phân tích lỗi, cải tiến mô hình, thí nghiệm loại bỏ thành phần, bộ đánh giá riêng và demo trực quan.

---

# 1. Bài toán Zero-Shot Object Counting là gì?

Zero-Shot Object Counting (ZSC) là bài toán:

> Cho một ảnh và một câu chữ chỉ đối tượng cần đếm, mô hình phải trả về số lượng của đối tượng đó, kể cả khi lớp đối tượng này chưa xuất hiện trong tập huấn luyện.

Ví dụ:

```text
Ảnh: có 8 quả táo + 3 quả cam

Prompt 1: "apple"
→ kết quả mong muốn: 8

Prompt 2: "orange"
→ kết quả mong muốn: 3
```

Điểm quan trọng:

- Không cần người dùng đưa các bounding box mẫu như few-shot.
- Chỉ dùng tên lớp hoặc mô tả bằng ngôn ngữ.
- Các lớp train/validation/test nên không trùng nhau để đảm bảo tính zero-shot thật sự.
- Mục tiêu không chỉ là “đếm đúng”, mà phải “đếm đúng thứ mà người dùng hỏi”.

---

# 2. Các tài liệu chính

## 2.1. Zero-Shot Object Counting — CVPR 2023

Repository:

https://github.com/cvlab-stonybrook/zero-shot-counting

Ý tưởng chính:

```text
Class name
   ↓
Class prototype
   ↓
Candidate patches
   ↓
Exemplar scoring
   ↓
Best exemplars
   ↓
Counting network
   ↓
Density map
   ↓
Count
```

Điểm mạnh:

- Là một baseline nền tảng của Zero-Shot Counting.
- Chuyển tên lớp thành các exemplar (mẫu thị giác) tự động.
- Không cần người dùng tự đánh dấu exemplar.

Điểm cần hiểu:

- class prototype
- exemplar
- candidate patch
- regression/scoring
- density map
- count = tổng density map

---

## 2.2. VA-Count — ECCV 2024

Repository:

https://github.com/HopooLinZ/VA-Count

Tên bài:

**Zero-shot Object Counting with Good Exemplars**

VA-Count tập trung vào hai phần:

### Exemplar Enhancement Module (EEM)

Mục tiêu:

> chọn exemplar tốt hơn.

VA-Count kết hợp Grounding DINO để tìm vùng ứng viên có khả năng chứa đối tượng cần đếm.

### Noise Suppression Module (NSM)

Mục tiêu:

> giảm ảnh hưởng của các đối tượng không thuộc lớp cần đếm.

Pipeline khái quát:

```text
Text Prompt
    ↓
Grounding DINO
    ↓
Candidate regions
    ↓
Exemplar Enhancement
    ↓
Noise Suppression
    ↓
Counter
    ↓
Density Map
    ↓
Object Count
```

Đây là baseline phù hợp nhất để phát triển đồ án vì:

1. Grounding DINO đã nằm sẵn trong pipeline.
2. Đúng với vấn đề thầy đưa ra:
   - Grounding DINO tìm đúng.
   - Nhưng vùng cuối cùng mà VA-Count dùng để đếm có thể sai.
3. Có thể can thiệp trực tiếp vào phần sau Grounding DINO.

---

## 2.3. T2ICount — CVPR 2025

Repository:

https://github.com/cha15yq/T2ICount

Tên bài:

**T2ICount: Enhancing Cross-modal Understanding for Zero-Shot Counting**

T2ICount chú trọng vào khả năng hiểu tương tác giữa:

```text
Text
↕
Image
```

Mô hình sử dụng Stable Diffusion v1.5 làm nền đặc trưng.

Điểm đáng chú ý:

- Có mã train và inference.
- Có checkpoint.
- Có FSC-147-S-v2.
- FSC-147-S-v2 được thiết kế để kiểm tra liệu mô hình có thực sự hiểu bài toán zero-shot counting hay không.

Tuy nhiên:

- Kiến trúc nặng hơn.
- Thiết lập môi trường phức tạp hơn.
- Tốn thời gian debug hơn VA-Count.

=> Nên dùng T2ICount làm **mô hình tham khảo mạnh + benchmark**, không nên dùng làm baseline đầu tiên trong 2 tháng nếu chưa reproduce được VA-Count.

---

## 2.4. RichCount — 2025

Paper:

**Expanding Zero-Shot Object Counting with Rich Prompts**

Ý tưởng quan trọng:

RichCount chỉ ra ba vấn đề của các mô hình Zero-Shot Counting dựa trên text:

1. **Khoảng cách giữa đặc trưng chữ và ảnh**
2. **Text prompt quá nghèo thông tin**
3. **Text input thiếu linh hoạt**

Ví dụ:

```text
"apple"
```

chỉ cho mô hình biết tên lớp.

Trong khi:

```text
"red apples on the left side of the wooden table"
```

cung cấp thêm:

- màu
- vị trí
- hình dáng
- ngữ cảnh

RichCount dùng hai giai đoạn:

```text
Stage 1
Visual-Text Alignment

Stage 2
Text-Based Counting
```

Pipeline:

```text
Image ──→ Image Encoder ──→ Visual Feature
                                ↕
                           Alignment
                                ↕
Prompt ──→ Text Encoder ──→ Text Feature
                                ↓
                         Interaction Module
                                ↓
                             Decoder
                                ↓
                           Density Map
                                ↓
                              Count
```

RichCount rất phù hợp với vấn đề:

> Cùng một ảnh, hỏi X và hỏi Y nhưng mô hình lại cho kết quả gần giống nhau.

---

# 3. Paper Domain Adversarial Reinforcement Learning có vai trò gì?

Paper:

**Domain Adversarial Reinforcement Learning**

Đây không phải paper Zero-Shot Object Counting.

Nó nghiên cứu zero-shot generalization trong reinforcement learning:

```text
Train:
environment A, B, C

Test:
environment D chưa gặp
```

Mục tiêu là học feature không bị ảnh hưởng bởi:

- background
- màu sắc
- độ sáng
- nhiễu thị giác

Ý tưởng có thể tham khảo:

> Học representation giữ thông tin liên quan nhiệm vụ và loại bỏ thông tin gây nhiễu.

Nhưng:

**Không nên lấy paper này làm trục chính của đồ án ZSC.**

---

# 4. Ba vấn đề nghiên cứu thầy đưa ra

## Vấn đề 1 — phụ thuộc Ground Truth Density Map

Các mô hình thường học bằng density map ground truth.

Ví dụ:

```text
Image
 ↓
Network
 ↓
Predicted density map
 ↓
MSE với GT density map
```

Vấn đề:

Mô hình có thể học mạnh vào hình dạng/phân bố density thay vì thật sự hiểu câu chữ chỉ đối tượng.

Câu hỏi nghiên cứu:

> Liệu mô hình đang hiểu "apple" hay chỉ học cách tái tạo các vùng mật độ thường gặp?

---

## Vấn đề 2 — Grounding DINO đúng nhưng vùng đếm sai

Ví dụ:

```text
Prompt = "apple"

Ảnh:
┌───────────────────────────┐
│ apple apple   orange      │
│ apple apple   orange      │
│             orange        │
└───────────────────────────┘
```

Grounding DINO:

```text
apple → đúng vùng apple
```

Nhưng counter:

```text
density map → lan sang orange
```

Đây là failure case rất đáng nghiên cứu.

---

## Vấn đề 3 — prompt X và Y cho kết quả giống nhau

Ví dụ:

```text
Prompt X = "apple"
Prompt Y = "orange"
```

Ground truth:

```text
apple = 8
orange = 3
```

Model:

```text
apple → 8.1
orange → 7.9
```

=> Mô hình gần như không thực sự phân biệt ý nghĩa câu lệnh.

---

# 5. Hướng đồ án đề xuất

# Region-Aware Contrastive Prompt Learning for Zero-Shot Object Counting

Tên tiếng Việt:

**Đếm đối tượng Zero-Shot dựa trên ràng buộc vùng ngữ nghĩa và học phân biệt câu lệnh**

---

# 6. Kiến trúc tổng quát đề xuất

```text
                         TEXT QUERY
                             │
                ┌────────────┴────────────┐
                ↓                         ↓
          Rich Prompt               Grounding DINO
                ↓                         ↓
          Text Encoder              Candidate Regions
                │                         │
                └─────────┬───────────────┘
                          ↓
                 Visual-Text Alignment
                          ↓
                    Counting Network
                          ↓
                      Density Map
                          │
           ┌──────────────┼──────────────┐
           ↓              ↓              ↓
      Density Loss    Region Loss    Prompt Loss
                                         │
                             ┌───────────┴───────────┐
                             ↓                       ↓
                          Same                    Different
                         prompts                   prompts
                             ↓                       ↓
                         similar                separated
```

---

# 7. Thành phần A — Region-Aware Counting

Grounding DINO tạo vùng:

\[
M_q(x,y)
\]

Trong đó:

- `q` là prompt
- `M_q` biểu diễn vùng ảnh có khả năng chứa đối tượng được prompt yêu cầu

Density map dự đoán:

\[
D_q(x,y)
\]

Ta muốn:

> Density chỉ tập trung chủ yếu trong vùng đúng.

Một loss đơn giản:

\[
L_{region}
=
\sum_{x,y}
D_q(x,y)\cdot(1-M_q(x,y))
\]

Ý nghĩa:

- density nằm trong vùng target → không phạt
- density nằm ngoài vùng target → bị phạt

## Không nên hard-mask ngay

Không nên làm:

```text
D = D × Mask
```

vì Grounding DINO có thể bỏ sót object.

Thay vào đó nên dùng:

**soft constraint — ràng buộc mềm**

để mô hình vẫn có cơ hội sửa lỗi detector.

---

# 8. Thành phần B — Query Contrastive Learning

Ta cần mô hình hiểu:

## Prompt cùng ý nghĩa

```text
"apple"
"red apple"
"apples on the left side"
```

nên sinh prediction tương tự.

Ta có:

\[
L_{same}
=
\|D_{q_1}-D_{q_2}\|
\]

với `q1`, `q2` chỉ cùng một loại object.

---

## Prompt khác đối tượng

```text
"apple"
"orange"
```

phải tạo prediction khác nhau.

Ta thêm:

\[
L_{diff}
\]

với mục tiêu ép representation hoặc density map của hai prompt khác lớp tách nhau.

Ý tưởng:

```text
same-object prompts
        ↓
close

different-object prompts
        ↓
far
```

---

# 9. Hàm mất mát tổng

Baseline:

\[
L=L_{density}
\]

Đề xuất:

\[
\boxed{
L =
L_{density}
+\lambda_1L_{count}
+\lambda_2L_{region}
+\lambda_3L_{same}
+\lambda_4L_{diff}
}
\]

Trong đó:

| Loss | Mục tiêu |
|---|---|
| `L_density` | học density map |
| `L_count` | tổng số lượng phải chính xác |
| `L_region` | giảm density ngoài vùng target |
| `L_same` | prompt cùng nghĩa → prediction gần nhau |
| `L_diff` | prompt khác object → prediction phải tách |

---

# 10. Chỉ số đánh giá

Không nên chỉ dùng MAE và RMSE.

## 10.1. MAE

\[
MAE=
\frac{1}{N}
\sum_i
|\hat y_i-y_i|
\]

Đo sai số đếm trung bình.

## 10.2. RMSE

\[
RMSE=
\sqrt{
\frac{1}{N}
\sum_i
(\hat y_i-y_i)^2
}
\]

Nhạy hơn với các lỗi lớn.

## 10.3. Cross-Prompt Leakage — CPL

Đề xuất:

\[
CPL=
\frac{
\text{density rơi vào vùng của class khác}
}{
\text{tổng predicted density}
}
\]

Ví dụ prompt `"apple"`:

```text
density trong vùng apple  = 7.5
density trong vùng orange = 2.5

CPL = 2.5 / 10 = 0.25
```

CPL càng thấp càng tốt.

## 10.4. Prompt Confusion Rate — PCR

Nếu:

```text
GT apple = 10
GT orange = 3
```

nhưng:

```text
Pred apple = 9.8
Pred orange = 9.5
```

thì mô hình đang prompt-confused.

Có thể định nghĩa:

\[
|\hat C_X-\hat C_Y| < \epsilon
\]

trong khi:

\[
|C_X-C_Y|
\]

lớn đáng kể.

Tỷ lệ các trường hợp như vậy:

\[
PCR=
\frac{\text{số cặp prompt bị nhầm}}
{\text{tổng cặp prompt}}
\]

PCR càng thấp càng tốt.

---

# 11. Bộ dữ liệu

## FSC-147

Dataset chính cho class-agnostic counting / zero-shot counting.

Có:

- 6,135 ảnh
- 147 class
- point annotation
- train/validation/test split

Dùng cho:

- train
- baseline
- MAE
- RMSE

## FSC-147-S-v2

Từ T2ICount.

Mục tiêu:

> kiểm tra mô hình có thật sự thực hiện zero-shot object counting hay không.

Dùng như semantic stress-test.

## X/Y Challenge Set — tự tạo

Đây là dataset quan trọng nhất để kiểm tra vấn đề của thầy.

Mỗi ảnh nên có ≥ 2 class.

Ví dụ:

```text
apple + orange
cars + motorcycles
dogs + cats
red flowers + white flowers
cups + bottles
```

Mỗi ảnh phải có:

```json
{
  "image": "...",
  "queries": [
    {
      "text": "apple",
      "count": 8
    },
    {
      "text": "orange",
      "count": 3
    }
  ]
}
```

Mục tiêu:

50–100 ảnh chất lượng tốt là đủ cho một bộ stress-test đồ án.

---

# 12. Failure Analysis Notebook

Trước khi cải tiến mô hình, phải xây notebook phân tích lỗi.

Ví dụ:

```text
Image ID: 00251

GT
apple  = 8
orange = 3

Grounding DINO
apple recall  = 8/8
orange recall = 3/3

VA-Count
prompt apple  → 8.4
prompt orange → 8.1
```

Kết luận:

```text
Detector:
apple ≠ orange
→ đúng

Counter:
apple ≈ orange
→ sai
```

=> lỗi nằm sau Grounding DINO.

---

# 13. Ablation Study

Ablation là thí nghiệm loại bỏ từng thành phần.

| Model | Region | Same Prompt | Different Prompt | Rich Prompt |
|---|---:|---:|---:|---:|
| VA-Count | ✗ | ✗ | ✗ | ✗ |
| Model A | ✓ | ✗ | ✗ | ✗ |
| Model B | ✓ | ✓ | ✗ | ✗ |
| Model C | ✓ | ✓ | ✓ | ✗ |
| Full Model | ✓ | ✓ | ✓ | ✓ |

Đánh giá:

```text
MAE ↓
RMSE ↓
CPL ↓
PCR ↓
```

Điều quan trọng:

Không nhất thiết MAE phải giảm cực mạnh.

Nếu kết quả:

```text
VA-Count
PCR = 37%

Ours
PCR = 14%
```

trong khi MAE không giảm hoặc cải thiện nhẹ thì vẫn là kết quả nghiên cứu rất có giá trị.

---

# 14. Lộ trình 8 tuần

## TUẦN 1 — FOUNDATION

### Mục tiêu

Hiểu bài toán từ đầu.

### Học

- Object Counting
- Class-specific counting
- Class-agnostic counting
- Few-shot counting
- Zero-shot counting
- Density map
- Gaussian kernel
- FSC-147
- MAE
- RMSE
- tensor
- feature map

### Code

- đọc ảnh FSC-147
- đọc point annotation
- vẽ point
- tự sinh density map
- tính tổng density map
- kiểm tra:

\[
\sum D \approx \text{number of objects}
\]

### Deliverable

```text
01_density_map_basics.ipynb
```

Phải giải thích được:

> Tại sao density map có thể được dùng để đếm?

---

## TUẦN 2 — ZSC 2023

### Học

- class prototype
- exemplar
- candidate patch
- exemplar scoring
- regression
- density estimation

### Code

Clone:

```bash
git clone https://github.com/cvlab-stonybrook/zero-shot-counting
```

Chạy inference trên tập nhỏ.

### Deliverable

```text
02_zsc_baseline.ipynb
```

Phải hiểu:

```text
class name
→ exemplar
→ counter
→ density map
→ count
```

---

## TUẦN 3 — VA-COUNT

### Học

- Grounding DINO
- visual grounding
- bounding box
- EEM
- NSM
- contrastive loss

### Code

Clone:

```bash
git clone https://github.com/HopooLinZ/VA-Count
```

Chạy pretrained.

Lưu lại:

```text
input image
prompt
Grounding DINO boxes
selected exemplar
density map
final count
```

### Deliverable

```text
03_vacount_failure_analysis.ipynb
```

Tìm ít nhất:

**20 failure cases**

---

## TUẦN 4 — RESEARCH DESIGN

### Đọc

- RichCount
- T2ICount
- nghiên cứu prompt alignment
- negative prompt
- contrastive learning

### Xây X/Y Challenge Set

Tối thiểu:

```text
30–50 images
```

Tốt hơn:

```text
50–100 images
```

### Chốt research question

> How can zero-shot object counting models better distinguish different textual queries in the same image?

### Chốt hypothesis

> Region-aware supervision combined with prompt contrastive learning can reduce cross-class counting leakage.

### Deliverable

```text
04_research_design.md
XY_dataset_v1.json
```

---

## TUẦN 5 — MODEL V1

### Thêm Region Loss

Pipeline:

```text
Grounding DINO
     ↓
Target Mask
     ↓
Density Map
     ↓
Region Loss
```

### Experiment

Baseline:

```text
VA-Count
```

Model A:

```text
VA-Count + Region Loss
```

Đánh giá:

```text
MAE
RMSE
CPL
```

### Deliverable

```text
checkpoint_region_v1.pth
results_region_v1.csv
```

---

## TUẦN 6 — MODEL V2

### Thêm prompt contrastive learning

Positive pair:

```text
"apple"
"red apple"
"apples on the table"
```

Negative pair:

```text
"apple"
"orange"
```

Loss:

```text
L_same
L_diff
```

### Ablation

```text
Baseline
+Region
+Region+Same
+Region+Same+Diff
Full
```

### Deliverable

```text
checkpoint_full_v1.pth
ablation_results.csv
```

---

## TUẦN 7 — FULL EVALUATION

### Dataset

1. FSC-147
2. FSC-147-S-v2
3. X/Y Challenge Set
4. CARPK nếu còn thời gian

### Metrics

```text
MAE
RMSE
CPL
PCR
```

### Visualization

Mỗi case:

```text
Image
Ground Truth
Grounding DINO
VA-Count density
Ours density
VA-Count count
Ours count
```

### Deliverable

```text
evaluation/
├── fsc147_results.csv
├── fsc147s_results.csv
├── xy_results.csv
├── plots/
└── failure_cases/
```

---

## TUẦN 8 — HERO

### Hoàn thiện

- report
- GitHub
- demo
- slide
- thuyết trình
- video demo nếu cần

### Demo nên hiển thị

```text
               SAME IMAGE
                   │
       ┌───────────┴───────────┐
       ↓                       ↓
    "apple"                 "orange"
       ↓                       ↓
Grounding regions       Grounding regions
       ↓                       ↓
 Density map             Density map
       ↓                       ↓
      8                         3
```

Có chế độ:

```text
Compare with VA-Count
```

Ví dụ:

| Prompt | VA-Count | Ours |
|---|---:|---:|
| apple | 8 | 8 |
| orange | 8 | 3 |

---

# 15. Lịch học chi tiết 60 ngày

## Ngày 1–3

Học:

- object counting
- zero-shot
- few-shot
- density map
- MAE/RMSE

Code density map từ annotation.

## Ngày 4–7

Học:

- CNN
- feature map
- embedding
- cosine similarity

Học vừa đủ, không lan man.

## Ngày 8–10

Học:

- Transformer
- attention
- ViT

Mục tiêu:

hiểu query/key/value ở mức đọc paper.

## Ngày 11–14

Học:

- CLIP
- text encoder
- image encoder
- contrastive learning

## Ngày 15–18

Đọc ZSC 2023.

Chạy code.

## Ngày 19–21

Visualize pipeline ZSC.

## Ngày 22–25

Đọc VA-Count.

## Ngày 26–28

Reproduce VA-Count.

## Ngày 29–31

Build failure-analysis pipeline.

## Ngày 32–34

Đọc RichCount.

## Ngày 35–36

Đọc T2ICount.

## Ngày 37–39

Build X/Y Challenge Set.

## Ngày 40–43

Implement Region Loss.

## Ngày 44–46

Train / fine-tune Model A.

## Ngày 47–49

Implement Same-Prompt Loss.

## Ngày 50–52

Implement Different-Prompt Loss.

## Ngày 53–55

Full ablation.

## Ngày 56–57

Evaluate.

## Ngày 58

Generate figures.

## Ngày 59

Report + slides.

## Ngày 60

Demo + rehearsal.

---

# 16. Kiến thức cần học — mức độ ưu tiên

| Kiến thức | Mức độ |
|---|---|
| Tensor | Bắt buộc |
| CNN | Bắt buộc |
| Feature Map | Bắt buộc |
| Density Map | Bắt buộc |
| Gaussian Kernel | Bắt buộc |
| MAE/RMSE | Bắt buộc |
| Embedding | Bắt buộc |
| Cosine Similarity | Bắt buộc |
| Contrastive Learning | Bắt buộc |
| CLIP | Bắt buộc |
| Grounding DINO | Bắt buộc |
| Transformer | Quan trọng |
| Vision Transformer | Quan trọng |
| Cross Attention | Quan trọng |
| Stable Diffusion | Đọc hiểu |
| SAM | Tùy chọn |
| DETR | Tùy chọn |
| Domain Adversarial Learning | Ý tưởng phụ |

---

# 17. Những thứ KHÔNG nên làm sớm

## Không train T2ICount từ đầu tuần 1

Lý do:

- Stable Diffusion
- environment phức tạp
- debug nặng
- dễ mất 1–2 tuần mà chưa hiểu bài toán

## Không bỏ density map ngay

Đừng lập tức chuyển sang detector-based counting.

Trước tiên:

```text
density
+ count
+ region
+ prompt
```

Nếu còn thời gian mới nghiên cứu architecture không density map.

## Không chỉ báo cáo MAE/RMSE

Vì thầy đang hỏi vấn đề semantic.

Phải có metric phản ánh:

```text
X ≠ Y
```

---

# 18. Các câu hỏi nghiên cứu chính

## RQ1

> Grounding DINO đã xác định đúng object nhưng tại sao density map vẫn lan sang class khác?

## RQ2

> Zero-shot counter có thực sự sử dụng prompt hay chỉ phụ thuộc mạnh vào image/density prior?

## RQ3

> Region-aware supervision có giảm density leakage không?

## RQ4

> Contrastive prompt training có giúp phân biệt X và Y trong cùng ảnh không?

## RQ5

> Rich prompts có cải thiện semantic grounding so với chỉ dùng class name không?

---

# 19. Experimental Matrix

| Experiment | Baseline | Region | Same | Diff | Rich |
|---|---:|---:|---:|---:|---:|
| E0 | ✓ | ✗ | ✗ | ✗ | ✗ |
| E1 | ✓ | ✓ | ✗ | ✗ | ✗ |
| E2 | ✓ | ✓ | ✓ | ✗ | ✗ |
| E3 | ✓ | ✓ | ✓ | ✓ | ✗ |
| E4 | ✓ | ✓ | ✓ | ✓ | ✓ |

Metrics:

```text
FSC-147 MAE
FSC-147 RMSE
FSC-147-S MAE
XY-CPL
XY-PCR
```

---

# 20. Folder structure đề xuất

```text
zsc-project/
│
├── data/
│   ├── FSC147/
│   ├── FSC147-S/
│   └── XY-Challenge/
│
├── baselines/
│   ├── zsc/
│   ├── vacount/
│   └── t2icount/
│
├── src/
│   ├── models/
│   ├── losses/
│   │   ├── density_loss.py
│   │   ├── count_loss.py
│   │   ├── region_loss.py
│   │   └── prompt_contrastive_loss.py
│   ├── grounding/
│   ├── datasets/
│   └── evaluation/
│
├── notebooks/
│   ├── 01_density_map.ipynb
│   ├── 02_zsc.ipynb
│   ├── 03_vacount.ipynb
│   ├── 04_failure_analysis.ipynb
│   └── 05_ablation.ipynb
│
├── experiments/
│   ├── baseline/
│   ├── region/
│   ├── contrastive/
│   └── full/
│
├── results/
│   ├── csv/
│   ├── plots/
│   └── visualizations/
│
├── report/
│
└── README.md
```

---

# 21. Tiêu chí “Done” cho từng giai đoạn

## Foundation Done

Bạn giải thích được:

```text
image
→ density
→ sum
→ count
```

## ZSC Done

Bạn giải thích được:

```text
text
→ exemplar
→ density
```

## VA-Count Done

Bạn nhìn một sample và biết:

- Grounding DINO chọn gì
- exemplar nào được dùng
- density sinh ở đâu
- lỗi xảy ra ở stage nào

## Research Done

Bạn có ít nhất:

```text
20 confirmed failure cases
```

## Method V1 Done

Region loss chạy end-to-end.

## Method V2 Done

X/Y prompts cho prediction khác nhau hợp lý hơn baseline.

## Evaluation Done

Có:

```text
MAE
RMSE
CPL
PCR
ablation
qualitative examples
```

## Hero Done

Bạn trả lời được 5 câu:

1. Problem là gì?
2. Baseline fail ở đâu?
3. Bạn sửa gì?
4. Vì sao sửa như vậy?
5. Thí nghiệm nào chứng minh nó hiệu quả?

---

# 22. Storyline khi thuyết trình

## Slide 1 — Problem

```text
Can a model really count what we ask?
```

## Slide 2 — Failure Case

Một ảnh có:

```text
8 apples
3 oranges
```

VA-Count:

```text
apple → 8
orange → 8
```

## Slide 3 — Diagnosis

Grounding DINO:

```text
correct
```

Counter:

```text
wrong
```

## Slide 4 — Hypothesis

Counter chưa bị ràng buộc đủ mạnh bởi:

```text
target region
+
prompt identity
```

## Slide 5 — Proposed Method

```text
Region Loss
+
Prompt Contrastive Loss
```

## Slide 6 — Results

```text
MAE
RMSE
CPL
PCR
```

## Slide 7 — Ablation

Chứng minh mỗi module đóng góp gì.

## Slide 8 — Demo

```text
same image
apple → 8
orange → 3
```

---

# 23. Mục tiêu cuối cùng

Một đồ án mạnh không cần phải tạo một mô hình khổng lồ.

Đồ án nên có:

```text
Clear Problem
      ↓
Reproducible Baseline
      ↓
Failure Analysis
      ↓
Research Hypothesis
      ↓
Minimal but meaningful modification
      ↓
Controlled Experiments
      ↓
New Evaluation Metric
      ↓
Ablation
      ↓
Visual Evidence
      ↓
Demo
```

Nếu làm đầy đủ chuỗi này, đồ án sẽ có phong cách gần với một mini research paper hơn là chỉ chạy lại repository.

---

# 24. 72 giờ đầu tiên

## Ngày 1

Học:

- Zero-Shot
- Few-Shot
- Object Counting
- Density Map
- FSC-147
- MAE/RMSE

## Ngày 2

Học:

- Embedding
- CLIP
- Contrastive Learning
- Grounding DINO

## Ngày 3

Chuẩn bị VA-Count:

```bash
git clone https://github.com/HopooLinZ/VA-Count
```

Chuẩn bị FSC-147.

## Ngày 4

Chạy pretrained inference.

## Ngày 5

Visualize:

```text
Grounding box
exemplar
density map
count
```

## Ngày 6

Cùng một ảnh:

```text
prompt X
prompt Y
prompt Z
```

ghi toàn bộ output.

## Ngày 7

Viết Failure Analysis đầu tiên.

---

# 25. Milestone quan trọng nhất đầu tiên

Mục tiêu không phải:

> “train được model”.

Mục tiêu là chứng minh được:

```text
Grounding DINO hiểu X ≠ Y

NHƯNG

VA-Count counter lại cho:
X ≈ Y
```

Khi chứng minh được failure này bằng nhiều sample, bạn đã xác định được chính xác phần cần nghiên cứu.

---

# 26. Proposal ngắn gọn có thể gửi giảng viên

## Title

**Region-Aware Contrastive Prompt Learning for Zero-Shot Object Counting**

## Problem

Existing Zero-Shot Object Counting models may produce similar counting results for different textual queries within the same image, even when visual grounding correctly identifies distinct target regions.

## Hypothesis

Combining region-aware supervision from Grounding DINO with prompt-level contrastive learning can improve query-specific counting and reduce cross-class density leakage.

## Baseline

VA-Count.

## Main Components

1. Region-aware density constraint
2. Same-prompt consistency
3. Different-prompt separation
4. Optional rich-prompt augmentation

## Evaluation

- FSC-147
- FSC-147-S-v2
- X/Y Challenge Set

## Metrics

- MAE
- RMSE
- Cross-Prompt Leakage
- Prompt Confusion Rate

## Expected Contribution

A lightweight extension to VA-Count that strengthens the dependency between the textual query and the final counting prediction.

---

# 27. Tài liệu tham khảo

1. Zero-Shot Object Counting — CVPR 2023  
   https://github.com/cvlab-stonybrook/zero-shot-counting

2. VA-Count — Zero-shot Object Counting with Good Exemplars — ECCV 2024  
   https://github.com/HopooLinZ/VA-Count

3. T2ICount — Enhancing Cross-modal Understanding for Zero-Shot Counting — CVPR 2025  
   https://github.com/cha15yq/T2ICount

4. RichCount — Expanding Zero-Shot Object Counting with Rich Prompts  
   Paper đã cung cấp: `2505.15398v2.pdf`

5. Domain Adversarial Reinforcement Learning  
   Paper đã cung cấp: `2102.07097v1.pdf`

---

# 28. Hướng học tiếp theo

Roadmap học nên đi theo:

```text
Lesson 1
Zero-Shot Object Counting + Density Map

        ↓

Lesson 2
FSC-147 + metrics

        ↓

Lesson 3
Embedding + CLIP

        ↓

Lesson 4
Contrastive Learning

        ↓

Lesson 5
Grounding DINO

        ↓

Lesson 6
ZSC 2023

        ↓

Lesson 7
VA-Count

        ↓

Lesson 8
RichCount

        ↓

Lesson 9
T2ICount

        ↓

Lesson 10
Failure Analysis

        ↓

Research Implementation
```

---

# 29. Checkpoint hằng tuần

Đã đặt lịch nhắc:

**Mỗi tối Chủ nhật — Checkpoint đồ án ZSC**

Nội dung checkpoint:

```text
1. Tuần này đã hoàn thành gì?
2. Đang mắc lỗi/vướng ở đâu?
3. Baseline/model có chạy ổn định không?
4. Có failure case mới nào đáng chú ý?
5. Có kết quả định lượng mới không?
6. Có cần đổi giả thuyết nghiên cứu không?
7. Mục tiêu ưu tiên tuần tiếp theo là gì?
```

Mỗi tuần nên lưu một file:

```text
checkpoints/
├── week_01.md
├── week_02.md
├── week_03.md
├── ...
└── week_08.md
```

---

# 30. Kết luận chiến lược

Hướng triển khai ưu tiên:

```text
ZSC 2023
   ↓
học nền

VA-Count 2024
   ↓
baseline code chính

RichCount 2025
   ↓
ý tưởng prompt / semantic alignment

T2ICount 2025
   ↓
benchmark + stress test

Ours
   ↓
Region-Aware
+
Prompt-Contrastive
Zero-Shot Counting
```

Mục tiêu cuối cùng:

> Không chỉ đếm đúng số lượng, mà phải đếm **đúng thứ mà người dùng hỏi**.

---

# Checklist cuối kỳ

- [ ] Hiểu density map
- [ ] Hiểu ZSC 2023
- [ ] Reproduce ZSC baseline
- [ ] Hiểu VA-Count
- [ ] Reproduce VA-Count
- [ ] Visualize Grounding DINO boxes
- [ ] Visualize exemplar
- [ ] Visualize density map
- [ ] Có ≥20 failure cases
- [ ] Có X/Y Challenge Set
- [ ] Có Region Loss
- [ ] Có Same-Prompt Loss
- [ ] Có Different-Prompt Loss
- [ ] Có ablation study
- [ ] Có FSC-147 results
- [ ] Có FSC-147-S-v2 results
- [ ] Có X/Y results
- [ ] Có MAE
- [ ] Có RMSE
- [ ] Có CPL
- [ ] Có PCR
- [ ] Có demo so sánh VA-Count vs Ours
- [ ] Có report
- [ ] Có slide
- [ ] Có GitHub sạch
- [ ] Có script thuyết trình
- [ ] Có rehearsal trước ngày bảo vệ

