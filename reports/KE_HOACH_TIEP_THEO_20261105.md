# Kiểm bài nộp Triệu (02–04/11) và kế hoạch từ 06/11 — soạn 05/11/2026

**Người soạn:** assistant. Chỉ đọc file, không chạy model. Đây là đề xuất; các quyết định ở §3 thuộc về Trí.

## 1. Kiểm bài nộp

| Việc | Kết quả kiểm |
|---|---|
| V4: 2 ca thử evaluator | ✅ Đạt. Ca `uncertain` loại đúng q05_3, MAE ra 19.5 / 18.14, khớp V5. Ca absent > 0 báo FPR_absent = 1.0, MeanAbsentCount = 25. Kết luận của Triệu đúng, kèm nhận xét hay: "unchanged" không có nghĩa là đúng |
| V6: N4 tầng B | ✅ Đạt. 58/58 dòng, tọa độ không đổi. **Assistant đã ghép bảng tra:** Fusion giữ u06_2 26/26 đúng, u07_2 14/14 đúng; lọc điểm giữ 13/14 và 9/9 đúng. Mẫu tự chọn đúng 6/6 |
| P1: code + notebook Colab | ✅ Có đủ: `run_b2_verified_pseudo.py`, `pseudo_clip_verifier.py`, `p1_controls.py`, `evaluate_research.py`. Pilot chạy trên T4: Kiểm A đạt (CLIP lệch 3e-7), Kiểm C đạt (T4 chạy lại khớp tuyệt đối), Kiểm B lệch nhẹ so với A2000 (5/15 query lệch 1 khung ở lượt 1) |
| Đề xuất dữ liệu v2 + script | ✅ Script chỉ đọc nhãn, đã rút thử và đạt các bài kiểm. **Chưa rút thật**, chờ Trí duyệt |
| Output P1 trên Drive | ⚠️ Chưa vào repo, nên assistant chưa kiểm độc lập được số liệu pilot P1 |

## 2. Bức tranh sau N4 tầng A + B (nhãn người)

| | Ca model bị nhầm (tầng A) | Ca model làm tốt (tầng B) |
|---|---|---|
| Mẫu tự chọn đúng loại | 1/12 (query có mặt) | **6/6** |
| Khung bộ lọc giữ có đúng không | 0 đúng (lọc điểm 0/78, Fusion 0/14) | Fusion 40/40 đúng |
| Vật đúng bị bộ lọc xóa (E3) | 13/18 | **11/11** |

Đọc bảng:
1. Bộ lọc cuối (F, S) **chỉ giúp được khi model đã đúng**, mà ngay cả khi đó vẫn xóa nhầm vật đúng. Khi model nhầm loại thì bộ lọc không cứu được.
2. Mẫu tự chọn sai đúng ở những ca model nhầm. Vậy kiểm mẫu (P) nhắm đúng chỗ, và có lẽ không làm hỏng ca tốt.
3. Cơ chế đã thấy trong raw (RA_SOAT §3): ở lượt 2, điểm khung = max(điểm chữ, điểm mẫu ảnh), nên điểm mẫu ảnh lấn át điểm chữ.

→ Nên thử **P không kèm bộ lọc cuối** và **T** (chỉ dùng điểm chữ ở lượt 2), thay vì chỉ thử P + F.

## 3. Quyết định — **ĐÃ CHỐT 05/11/2026: Trí đồng ý toàn bộ khuyến nghị D1–D10**

> Trí xác nhận trực tiếp trong chat ngày 05/11: "Triệu cần tôi submit việc thì oki luôn nha để Triệu làm tiếp". Assistant ghi lại theo ủy quyền đó; mọi quyết định dưới đây áp dụng **đúng như cột Khuyến nghị**. Cùng xác nhận đó, Trí nghiệm thu V3–V6 và đồng ý duyệt pilot V7 về phía Trí; Triệu ghi phần xác nhận của mình.

| # | Câu hỏi | Khuyến nghị | Lý do |
|---|---|---|---|
| D1 | Máy chuẩn + tiêu chí tái hiện | **Colab T4 làm máy chuẩn**; tiêu chí = Kiểm A + Kiểm C; chỉ so các cách trong cùng một lần chạy T4. Kết quả cũ trên A2000 giữ nguyên làm lịch sử | T4 tự lặp lại được, Triệu chạy được; lệch so với A2000 là do khác GPU, không phải lỗi |
| D2 | C6: bộ lọc cho B0 | **(b) chọn lại ngưỡng S/F riêng cho từng nguồn trên dev mới**, cùng quy tắc chọn như 21/10, khóa trước test | Ngưỡng cũ được khớp trên điểm lượt 2 (cao hơn hẳn), nên nếu giữ nguyên thì C6 thiệt oan |
| D3 | Cỡ tập | **dev 20 + test 40** | Vừa 2,5–3 giờ công kiểm nhãn; 30 + 50 tốn thêm khoảng 1 giờ, chỉ lợi khi dư thời gian |
| D4 | Khoảng điểm | **giữ 3–40** | Đã lấy hết 19 ảnh cặp khác hẳn; nới lên 60 thì phải đếm tay tới 60 vật |
| D5 | Lấy cặp dễ nhầm | **xoay vòng qua siêu nhóm** | Tập đa dạng; tránh lặp lại lỗi r1 (toàn một kiểu cặp) |
| D6 | Thêm absent loại dễ | **không** | 7/10 absent dễ đã trả 0 ngay ở lượt 1; tốn công kiểm mà ít thông tin |
| D7 | Seed | **331** | Giống v1; v2 dùng tên khác nên luồng ngẫu nhiên vẫn khác |
| D8 | Biến thể thử trên dev | **B0, B2, P (lưới tau, M), T, P+T, F/S chọn lại riêng từng nguồn, C6** | P đã có code. T tính được **ngoại tuyến** từ `stage2_raw.npz` đã lưu (có điểm từng token), không cần chạy lại GPU |
| D9 | Luật chọn cấu hình cuối (chốt **trước** khi xem dev) | Chọn cấu hình có **MAE cả tập nhỏ nhất trên dev**, với điều kiện **MAE có mặt ≤ MAE có mặt của B0** và **FPR_absent ≤ của B0**. Nếu không cấu hình nào đạt điều kiện thì báo kết quả âm (B0 là tốt nhất) | Tránh lặp lại tình huống Fusion "thắng" MAE chung nhờ hy sinh query có mặt |
| D10 | Output Drive | Nhờ Triệu đưa `predictions_*.jsonl` + `run_config.json` + bảng đối chứng vào repo; bỏ file `.npz` và ảnh | Để kiểm độc lập và trích dẫn được trong báo cáo |

## 4. Kế hoạch tối ưu từ 06/11

Đường găng: **quyết định → dữ liệu khóa → chạy dev → khóa cấu hình → test 1 lần → báo cáo**. Mọi việc khác làm song song.

| Ngày | Trí | Triệu | Assistant |
|---|---|---|---|
| **06/11** | Chốt D1–D10 (khoảng 30 phút, chọn theo bảng §3); cùng Triệu duyệt pilot V7 (khoảng 30 phút) | Rút dữ liệu thật ngay sau khi Trí chốt (vài giây); đẩy output Drive (D10) | Viết T ngoại tuyến + gắn vào `p1_controls.py`; kiểm trên pilot (CPU) |
| 07–08/11 | Kiểm absent/GT **dev 20 ảnh** (khoảng 1 giờ) → khóa dev | Kiểm absent/GT **test 40 ảnh** (khoảng 2 giờ) → khóa test | Kiểm độc lập output P1 pilot từ D10 |
| 09–12/11 | Xem bảng dev (khoảng 1 giờ) | Chạy trên T4 toàn bộ biến thể D8 trên dev (khoảng 2–3 giờ GPU) | Chấm theo luật D9, viết báo cáo dev |
| 13/11 | **Khóa cấu hình v2** (freeze v2) | — | Kiểm freeze |
| 13–22/11 | **Bắt đầu viết báo cáo sớm**: giới thiệu, phương pháp, pilot, N4 (khoảng 4 giờ) | Related Work (V9, khoảng 2 giờ) | Dựng bảng/hình từ kết quả có sẵn |
| 23–24/11 | — | Chạy **test một lần** trên T4 | Chấm, CI theo ảnh |
| 25/11–01/12 | Viết phần kết quả + hạn chế, slide, tập thuyết trình (khoảng 5 giờ) | Review N4 nhỏ trên test (V10), góp slide | Kiểm số liệu trong báo cáo |
| **02/12** | **Nộp** | | |

**Tiến độ:** trễ khoảng 3 ngày so với lịch 28/10 (bước [6] dự kiến 02/11), nhưng vẫn còn đệm 30/11–01/12. Viết báo cáo **song song từ 13/11**, không đợi xong test.

**Phương án dự phòng:**
- Nếu dev cho thấy không biến thể nào thắng theo D9: chuyển sang báo cáo dạng **phân tích lỗi + kết quả âm có bằng chứng N4**. Phần này đã có sẵn khoảng 70% tư liệu.
- Nếu T4/Colab hết quota: chạy trên A2000 local, nhưng phải chạy **mọi cách trong cùng một lần**, như D1.
