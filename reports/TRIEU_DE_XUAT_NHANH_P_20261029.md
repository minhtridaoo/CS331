# Đề xuất chọn nhánh cải tiến: nhánh P có bổ sung (29/10/2026)

**Người đề xuất:** Triệu. **Bản nháp:** Claude soạn từ phân tích N4 tầng A (V2), q05_3 (V3) và V5 bước 2–3 của Triệu; Triệu đọc, sửa rồi mới gửi Trí. **Mục đích:** bàn với Trí để chọn nhánh P hay R (buổi review chung 03/11). Đây là đề xuất, **chưa chạy thí nghiệm nào mới**.

## 1. Tóm tắt

- Nhóm **không cần đổi bài toán** (X/Y, vật vắng mặt, pseudo-exemplar). Bằng chứng đã có đều nằm ở bài toán này.
- Đề xuất **chọn nhánh P** (kiểm pseudo-exemplar trước lượt 2), đúng như Trí đã viết trong `hướng cái tiển/CS331_KE_HOACH_FIX_PIPELINE_DE_PUBLISH_20261027.md` §3. Ý "kiểm mẫu" **không phải ý mới của Triệu**.
- Phần Triệu thêm: (a) **số liệu N4** để chọn P thay vì R; (b) **một kiểu lỗi mà P1 (chỉ kiểm bằng CLIP) chưa xử lý**: vật bị chia thành nhiều mảnh; thêm một bước kiểm "một vật" để phòng, hiện **chưa có bằng chứng riêng**; (c) đề xuất ablation tương ứng.

## 2. Nhóm đang ở đâu

| Cách | Can thiệp ở đâu | MAE có mặt (20) | Đếm TB khi vắng mặt (10) | MAE cả 30 |
|---|---|---:|---:|---:|
| B0 | Không có lượt 2 | **5.70** | 8.9 | 6.77 |
| B2 gốc | Lượt 2 với top-3 theo điểm | 12.95 | 13.1 | 13.00 |
| B2 lọc điểm | Lọc khung **sau** lượt 2 | 8.75 | 4.3 | 7.27 |
| Fusion 50/50 | Lọc khung **sau** lượt 2 | 7.80 | **1.0** | **5.53** |

Nguồn: `reports/P4_6_UNSEEN_RESULTS_20261027.md`. Cả hai bộ lọc hiện có đều **chữa sau lượt 2**, và bỏ khoảng 50% vật đúng (phủ 44–50% điểm mục tiêu). Trên query có mặt, B0 vẫn tốt nhất. Nhánh P/R **chưa được chọn** (README, HANDOFF).

## 3. Bằng chứng từ phần việc của Triệu

### 3.1. E1: mẫu tự chọn gần như luôn sai (N4 tầng A, `bo_sung_F0/`)

| Query | Prompt | Presence | target | wrong_class | multi_object | Mẫu thực ra là | Delta B2−B0 |
|---|---|---|---:|---:|---:|---|---:|
| u01_1 | people | có mặt | 1 | 0 | 2 | dogs ×2 | +24 |
| u01_3 | sheep | vắng mặt | 0 | 2 | 1 | dogs ×3 | +12 |
| u02_1 | people | có mặt | 0 | 1 | 2 | dogs ×3 | +5 |
| u07_1 | people | có mặt | 0 | 1 | 2 | cars ×3 | +14 |
| u07_3 | bicycles | vắng mặt | 0 | 2 | 1 | motorcycles ×2, cars ×1 | +3 |
| u08_1 | people | có mặt | 0 | 3 | 0 | cars ×3 | +4 |
| u10_3 | bicycles | vắng mặt | 0 | 1 | 2 | motorcycles ×2, cars ×1 | +27 |
| **Tổng** | | | **1/21** | **10/21** | **10/21** | | **7/7 worsened** |

- Chỉ 1/21 mẫu đúng loại (≈4.8%). Mẫu sai không ngẫu nhiên: là vật **giống hình dáng** (sheep↔dogs, bicycles↔motorcycles) hoặc **hay đứng cạnh** vật cần đếm (người dắt chó).
- 10/21 mẫu là khung bao nhiều vật (`multi_object`). Cả 10 khung này đều gom vật **loại khác** (chó, ô tô, xe máy), nên tính cả hai nhóm thì **20/21 mẫu không đúng loại**.
- Giới hạn: 7 query này được chọn để soi lỗi; chưa xem mẫu của query improved (u01_2, u02_2).

### 3.2. E3: bộ lọc cuối xóa vật đúng

18 khung bị **cả hai** bộ lọc loại nhưng có điểm MUCCA đúng loại (3 query `people`): **13 target**, 3 part, 2 uncertain. u08_1 cả 7/7 khung bị xóa là người thật (GT 7). E3 có thật, nhưng chỉ ở 3 query, trong khi E1 xuất hiện ở cả 7 query được review.

### 3.3. Kiểu lỗi thứ hai: chia một vật thành nhiều mảnh (q05_3, tập pilot)

q05_3 `blackberries`, GT 3. Mẫu: P1 = b1, P2 = b2 (target), P3 = raspberries.

| Run | Số khung | target | part | wrong_class |
|---|---:|---:|---:|---:|
| B0 | 21 | 3 | 0 | 18 |
| B2 | 79 | 2 | **58** | 19 |

B2 tăng đúng 58 khung, và 58 khung đó là `part` (hạt, cụm hạt). 2/3 mẫu **đúng loại** mà sai số vẫn tăng từ 18 lên 76. b1 là mẫu P1 nhưng B2 không còn khung target nào cho b1, chỉ còn 23 mảnh của nó. **Kiểm loại bằng CLIP không chặn được lỗi này**, vì mẫu đã đúng loại.

### 3.4. B2 gốc kém B0 có hệ thống (V5 bước 2, tập p4_unseen_v1)

2 improved / 15 worsened / 13 unchanged. Bỏ query tệ nhất (u10_2) vẫn còn MAE B2 11.28 so với B0 6.45. CI ΔMAE [+2.0, +12.3]. Kết luận "B2 tùy trường hợp" ở pilot 15 query không còn đứng trên tập độc lập.

## 4. Vì sao chọn P

1. E1 phổ biến (20/21 mẫu sai, 7/7 query xấu đi), đúng điều kiện chọn P mà Trí đặt ra ở §0 của kế hoạch.
2. P1 khi không có mẫu đạt thì **quay về B0**, mà B0 đang tốt nhất trên query có mặt. Nhánh P vì vậy có "sàn" an toàn.
3. Nếu mẫu sạch hơn, lượt 2 sinh ít khung sai hơn, nên có thể không cần bộ lọc cuối mạnh như Fusion. Đây là **giả thuyết**: nó có thể giảm E3, nhưng phải đo.
4. Rủi ro mà kế hoạch §4.1 đã nêu cho R1 ("chó được chấm điểm rất cao khi hỏi `people`") **đã xảy ra thật** trong N4: top mẫu của u01_1, u02_1 là chó, của u07_1, u08_1 là ô tô. Quy tắc cứu khung theo điểm CountGD cao vì vậy dễ cứu lại chính các khung sai.
5. Giới hạn của "quay về B0": nó **không sửa được lỗi của chính B0**. Ở 3 query vắng mặt u01_3, u07_3, u10_3, B0 đã đếm sai sẵn (20, 21, 48). P chỉ chặn được việc lỗi đó bị khuếch đại thêm ở lượt 2.

Điều làm P yếu đi: E3 cũng lớn (13/18). Nếu P1 không thắng Fusion, nhánh R vẫn còn nguyên giá trị.

## 5. Bổ sung cho P1

P1 trong kế hoạch của Trí: lấy tối đa `M` ứng viên lượt 1 (score > 0.23), giữ khung có `clip_similarity ≥ tau_pseudo`, lấy tối đa 3; không có khung nào đạt thì dùng B0. Bổ sung đề xuất:

| Mã | Bổ sung | Nhắm lỗi | Bằng chứng | Không dùng GT? |
|---|---|---|---|---|
| P | CLIP gate + quay về B0 (P1 của Trí) | Mẫu sai loại | 20/21 mẫu không đúng loại (10 wrong_class + 10 multi_object gom vật loại khác) | Có |
| P+S | Thêm **kiểm một vật**: loại ứng viên mà trong nó có tâm của ≥ 2 khung lượt 1 khác | Mẫu bao nhiều vật | **Chưa có bằng chứng riêng**: cả 10 khung multi_object đều đã sai loại, nên về nguyên tắc P đã loại được (nếu CLIP chấm đúng). Giữ để phòng khung gom nhiều vật **đúng** loại (ví dụ đám đông người); ablation P+S so với P ở §6 sẽ trả lời | Có |
| P+S+chống mảnh | Thêm **chống chia mảnh** sau lượt 2: bỏ khung nằm gần trọn trong một khung giữ khác và nhỏ hơn nhiều so với kích thước mẫu | Chia nhỏ vật | q05_3: 58/79 part | Có |
| (bàn thêm) | CLIP so **tương đối** với một danh sách loại cố định chọn trước (ví dụ 80 lớp COCO), thay vì chỉ một ngưỡng tuyệt đối | Cặp gần nghĩa sheep/dogs, bicycles/motorcycles | 3/10 query vắng mặt bị báo > 0 ở mọi cách | Có, nhưng phải kiểm với quy tắc §3.2 của Trí: danh sách **không được rút từ tập test** |

Mọi ngưỡng (`M`, `tau_pseudo`, số tâm, tỉ lệ kích thước) **chỉ chọn trên tập dev 30 ảnh MUCCA mới**, khóa trước khi xem test. Không chỉnh trên 10 ảnh P4.6 (§5 kế hoạch Trí).

## 6. So sánh cần chạy

Giữ nguyên bộ đối chứng §3.5 của Trí: B0, B2, F, P, P+F, B0+F, S-only. Chỉ thêm:

| Thêm | So với | Câu hỏi |
|---|---|---|
| P+S | P | Kiểm một vật có thêm lợi ích so với chỉ kiểm loại không? |
| P+S+chống mảnh | P+S | Chống chia mảnh có lợi, hay lại xóa vật đúng? |
| Mẫu do người chọn (§3.6 của Trí, chỉ để khảo sát) | P, B2 | Mẫu đúng thì B2 tốt lên bao nhiêu? Nhãn V2 của Triệu dùng được làm phần khởi đầu cho việc này. |

Chỉ số: theo §5.2 của Trí, thêm **tỉ lệ mẫu đúng loại sau khi kiểm** và **số khung `part`**.

## 7. Đã cân nhắc và không đề xuất

| Hướng | Lý do không chọn bây giờ |
|---|---|
| Hạ ngưỡng khi lượt 1 rỗng (hướng của một nhóm khác, FSCD-147) | Giả định vật luôn có mặt. Ở tập của mình, 7/10 query vắng mặt trả 0 ngay ở lượt 1, và đó là **đáp án đúng**. Hạ ngưỡng có nguy cơ đếm "ma". |
| Contrastive loss (C-REX), prototype thích nghi (CoDi) | Cần huấn luyện lại CountGD++, không vừa phần cứng (T4 / A2000 4 GB) và hạn 02/12. |
| Cắt ảnh thích nghi, re-ID video (SAM3Count) | Nhắm cảnh đông hoặc video, lệch khỏi bài toán X/Y mà nhóm đã có bằng chứng. |

Về tính mới: cần đối chiếu với các bài cũng chọn mẫu tốt cho đếm zero-shot (PseCo đã có trong Related Work của kế hoạch; VA-Count ECCV 2024 cần kiểm thêm). Nếu P không vượt đối chứng đơn giản, nên định vị bài là **phân tích thực nghiệm**, đúng như Trí đã ghi.

## 8. Câu hỏi cần Trí quyết

1. Đồng ý chọn P làm đóng góp chính, R để dự phòng?
2. Có thêm P+S và P+S+chống mảnh vào ablation không, hay chỉ giữ P cho gọn?
3. Danh sách loại cố định cho CLIP so tương đối có vi phạm quy tắc "không đưa loại gây nhiễu" không?
4. Có cần Triệu gán thêm nhãn mẫu cho 2 query improved (u01_2, u02_2) để bớt thiên lệch chọn mẫu ở §3.1 không?
