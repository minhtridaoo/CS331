# Nhánh P1: pilot trên Colab T4 và đề xuất tiêu chí tái hiện (03/11/2026)

**Người chạy:** Triệu, trên Colab T4, notebook `experiments/countgdpp/colab_p1_verified_pseudo.ipynb`, code commit 9606a59. **Bản nháp:** Claude soạn từ kết quả Triệu dán lại, theo yêu cầu của Triệu. **Cần Trí:** đọc mục 4 và trả lời 3 đề xuất + câu hỏi về tập dev.

## 1. Tóm tắt

- Pilot P1 (5 ảnh, 15 query, tập dev cũ) **đã chạy hết** trên Colab T4. Chạy 2 lần với cùng lệnh.
- **Kiểm A đạt** (CLIP trên Colab chấm giống bản đã lưu). **Kiểm C đạt** (chạy lại trên T4 khớp tuyệt đối).
- **Kiểm B không khớp tuyệt đối** với kết quả A2000 của Trí. Lượt 1 lệch tối đa 1 khung. Lý do là **đổi GPU**, không phải cài sai (mục 3).
- Đề xuất: lấy **Colab T4 làm máy chuẩn**, đổi tiêu chí tái hiện, chỉ so các cách **trong cùng một lần chạy T4** (mục 4).
- Số MAE theo `tau_pseudo` ở pilot **chỉ để dò lỗi**, chưa dùng chọn gì. Chọn `tau_pseudo`/`M` phải đợi tập dev 30 ảnh.

## 2. Đã chạy gì

```text
run_b2_verified_pseudo.py --inputs experiments/countgdpp/m4_inputs/first5_inputs.jsonl
  --tau-pseudo 0.20 0.22 0.24 0.26 0.28 --m 10 --replay-b2
  --b0-reference results/countgdpp/m4_first5_b0/predictions.jsonl
  --b2-reference results/countgdpp/b2_two_images_20261015/predictions.jsonl results/countgdpp/b2_remaining3_20261015/predictions.jsonl
  --reference-mode report
```

- Run ID: `p1_pilot_colab_20261103_1519` (lần 1), `p1_pilot_colab_20261103_1528` (lần 2). Output nằm trên Google Drive của Triệu (`MyDrive/CS331_colab/<run_id>/`), **chưa đưa vào repo** vì có nhiều file raw `.npz` và ảnh. Trí cần thì Triệu chia sẻ thư mục hoặc nhóm quyết đưa vào repo.
- Môi trường: Python 3.10.22, torch 2.5.1+cu121, transformers 4.44.2, numpy 2.2.6, pillow 10.4.0 (giống máy Trí), GPU Tesla T4. Checkpoint và mã nguồn qua kiểm băm của audit 14/10.
- Cách cài trên Colab (Python 3.10 riêng, CUDA 12.1, build CUDA ops) và các lỗi đã gặp: [COLAB_P1_HUONG_DAN.md](../experiments/countgdpp/COLAB_P1_HUONG_DAN.md).

## 3. Kết quả kiểm

| Kiểm | So cái gì | Kết quả |
|---|---|---|
| A | CLIP chấm lại 663 khung `p4_unseen_v1` so với điểm đã lưu | **Đạt**, lệch lớn nhất 3.28e-07 |
| B | Lượt 1 so với B0 đã lưu; B2 chạy lại so với B2 đã lưu (A2000), khớp tuyệt đối (khung 0.001, điểm 1e-5) | **Không đạt**: 1/15 và 1/15 (chỉ q01_3, 0 khung) |
| C | Lần 2 so với lần 1 trên T4, khớp tuyệt đối (lượt 1, id mẫu, khung và điểm cuối) | **Đạt**: 6 cách (B2, tau 0.20–0.28) × 15/15 |

**Vì sao nghĩ Kiểm B lệch do đổi GPU:**
- Lượt 1: 10/15 query cùng số khung với B0 đã lưu. 5 query lệch đúng 1 khung (q01_2, q02_1, q04_1, q04_2, q05_2). Ở query cùng số khung, điểm lệch tối đa 0.023, khung thường lệch dưới 1 pixel. Vài số lệch khung hàng trăm pixel là do một khung ra, một khung vào làm xô thứ tự so (hàm `compare` so theo thứ tự).
- Trên A2000, các lần chạy B2 ngày 15/10 đều có `stage1_matches_B0: true` ở 15/15 query, tức A2000 tự lặp lại được. T4 cũng tự lặp lại được (Kiểm C). Chỉ khi đổi máy mới lệch.
- Nguyên nhân cụ thể **chưa kiểm**. Giả thuyết: A2000 là đời Ampere, PyTorch mặc định cho cuDNN dùng TF32; T4 không có TF32.

**Mẫu pseudo của B2 trên T4 so với A2000:** trùng ở 14/15 query.
- q04_3 red currants khác đúng 1 mẫu (đề xuất 3 thay vì 4), và B2 đổi **84 → 61** (GT 39).
- q02_2 bowls cùng 3 mẫu nhưng B2 ra 30 so với 31 (lượt 2 lệch số lẻ).
- MAE B2 pilot: T4 20.40, A2000 22.00. Toàn bộ chênh lệch 1.60 đến từ 2 query này ((23 + 1)/15).
- Quan sát: B2 rất nhạy với việc chọn mẫu, đổi 1 mẫu có thể đổi hơn 20 vật. Đây thêm một lý do để kiểm mẫu trước lượt 2 (nhánh P).

**Số pilot (chỉ dò lỗi, không dùng chọn tau):**

| cách | MAE (15 query có mặt) | số query không còn mẫu |
|---|---|---|
| B0 (lượt 1, Claude tính từ bảng số đếm) | 19.47 | – |
| B2 | 20.40 | 1 |
| tau 0.20 | 20.40 (cùng số đếm với B2 ở 15/15 query; **đính chính 04/11:** mẫu khác B2 ở q01_2 và q03_3, xem mục 6) | 1 |
| tau 0.22 | 22.87 | 2 |
| tau 0.24 | 22.33 | 4 |
| tau 0.26 | 22.80 | 7 |
| tau 0.28 | 22.73 | 9 |

Số đếm từng query có trong Ô 10 của notebook và `predictions_*.jsonl` trên Drive.

## 4. Cần Trí quyết

1. **Máy chuẩn:** lấy Colab T4 làm máy chạy chuẩn cho P1 (và các so sánh mới). Khoảng 2 compute unit/giờ; Triệu và Trí có thể dùng chung tài khoản.
2. **Tiêu chí tái hiện mới:** Kiểm A + Kiểm C 15/15 ở mọi cách. Kiểm B chỉ ghi lại mức lệch so với A2000, không bắt buộc khớp tuyệt đối.
3. **Cách so:** chỉ so B0/B2/P trong cùng một lần chạy T4 (runner đã chạy lại B2 bằng `--replay-b2`); không trộn số T4 với số A2000 trong một bảng. Kết quả cũ trên A2000 giữ nguyên, không sửa.
4. **Tập dev 30 ảnh:** khi nào nhóm khóa được danh sách? Sau đó Triệu chạy P1 trên dev để chọn `tau_pseudo` và `M` (kế hoạch Trí §3.2, §5).

## 5. Giới hạn

- Mới có 5 ảnh pilot, đã dùng nhiều lần trước đây; không kết luận P1 tốt hay kém từ bảng trên.
- Chưa kiểm nguyên nhân lệch T4/A2000 (TF32 chỉ là giả thuyết).
- Notebook chạy lần này là bản 9606a59 cộng vài ô vá tay trên Colab (tìm file build, `MPLBACKEND`, tải BERT); các bản vá đã đưa vào notebook trong lần push kèm báo cáo này. Runner và code model không đổi.

## 6. Bổ sung 04/11: bảng đối chứng trên pilot và một câu hỏi về C6

Ngày 04/11 Triệu chạy công cụ bảng đối chứng mới (`experiments/countgdpp/p1_controls.py` + `evaluation/evaluate_research.py`, Ô 12 của notebook) trên run `p1_pilot_colab_20261103_1519`. Cách làm và bài kiểm code: `experiments/countgdpp/COLAB_P1_HUONG_DAN.md`, mục "Bảng đối chứng". Output trên Drive của Triệu.

| cách (tên kế hoạch §3.5) | MAE (15 query có mặt) |
|---|---|
| B0 | 19.47 |
| B0+F (C6) | 8.73 |
| B2 | 20.40 |
| B2+S (S-only) | 4.87 |
| B2+F (F) | 4.60 |
| P+F, tau 0.20 / 0.22 / 0.24 / 0.26 / 0.28 | 4.53 / 4.80 / 4.87 / 4.93 / 6.60 |

Ngưỡng S và F được khớp trên chính 5 ảnh này (21/10), nên F và S-only lạc quan. Bảng chỉ để kiểm code, không kết luận.

**Đính chính về tau 0.20:** số đếm trùng B2 ở 15/15 query, nhưng CLIP đã đổi mẫu ở 2 query. q01_2 amplifiers: mẫu B2 là đề xuất 25, 42, 17 với cosine 0.199, 0.202, 0.199, nên P bỏ 25 và 17, lấy 42, 11, 28. q03_3: bỏ đề xuất 6 (cosine 0.195), thay bằng 3. Số đếm trùng là tình cờ; khung và điểm cuối khác, nên B2+S (4.87) khác tau 0.20+S (4.93). Cosine CLIP của mẫu nằm sát các mức tau đang thử (khoảng 0.19–0.22), nên đổi tau một bước nhỏ cũng đổi mẫu.

**Câu hỏi 5 (C6):** luật lọc khóa 21/10 được khớp trên điểm **lượt 2**. Điểm **lượt 1** thấp hơn hẳn (pilot A2000: trung vị 0.434 so với 0.672; điểm ≥ ngưỡng S 0.907 chỉ 2% so với 27%), nên B0+F đếm 0 ở 11/15 query. Làm C6 đúng chữ "cùng cách lọc" thì C6 bị thiệt và chưa trả lời được câu "có cần lượt 2 không". Trí chọn:
- (a) giữ luật khóa cho mọi nguồn, như hiện tại; hoặc
- (b) trên dev mới, chọn lại ngưỡng S/F cho **từng nguồn** (B0, B2, P) theo cùng quy tắc chọn của 21/10 (MAE dev nhỏ nhất, rồi RMSE, rồi ngưỡng), rồi khóa trước khi chạy test.

Gợi ý của Claude (Triệu chưa chốt): (b), vì công bằng cho C6; đổi lại (b) thêm tham số chọn trên dev cho mọi cách.
