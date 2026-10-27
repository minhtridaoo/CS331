# Đánh giá bản tự kiểm của Triệu (commit 36eaf96) — 27/10/2026

**Người đánh giá:** assistant, theo yêu cầu của Trí. Đây là **đề xuất để Trí nghiệm thu**, không phải chữ duyệt thay Trí. Nguồn: [báo cáo tự kiểm của Triệu](TRIEU_TU_KIEM_PHAN2_20261027.md) và các file bằng chứng trong commit `36eaf96`. Commit này được làm từ checkout `d6db189` nên **chưa có** kế hoạch V2, gói ZIP T0 và gói q05 (các file đó còn local, chưa push). Vì vậy Triệu làm theo checklist PHAN_2 trên `main`.

## Assistant đã kiểm lại (chỉ đọc file)

- `pilot_eval_20261027_trieu/metrics.json`, `per_query.json`, `manual_check.json` **giống hệt** run 20/10 (so nội dung JSON).
- `TRIEU_TINH_TAY.xlsx` có 3 sheet:
  - tính tay 15 dòng bằng công thức thật (`=ABS(C2-B2)`…);
  - nhãn 14 box q05_2;
  - 5 ca dữ liệu hỏng, có ghi Triệu đoán trước kết quả.
- `TRIEU_SELFTEST_stdout.txt` có dòng `SELF-TEST PASS`. Đây là stdout self-test đầu tiên được lưu trong repo.
- Số độ nhạy đúng: bỏ q05_3 thì B0 = 273/14 = 19.5 và B2 = 254/14 ≈ 18.14.

## Đối chiếu với 4 nhận xét của Trí

| Nhận xét của Trí | Triệu đã làm | Đánh giá |
|---|---|---|
| 1. Tự chạy lại evaluator, lưu bằng chứng, thử ca lỗi/thiếu/không chắc | Self-test (có stdout); chạy lại evaluator (trùng run cũ); 5 ca hỏng: trùng ID, thiếu dòng, count lệch, error có count, error hợp lệ | **ĐẠT phần lớn.** Còn thiếu 2 ca trong kế hoạch: GT `uncertain` và query `absent` mà model đếm > 0. File thử nằm ngoài repo (`C:\Users\diosodumb\documents\CS331_nhap`), nên chưa tái lập được từ repo |
| 2. Phân tích kỹ q05_2, q05_3: sai loại, trùng, bỏ sót | q05_2: tự gán 14 box **trước khi mở nhãn cũ**, khớp 14/14, giải thích rõ chỗ lệch box 12/13. q05_3: truy ngược số (21 → 21 → 79, tăng ở lượt 2), nhìn ảnh mẫu (2/3 đúng loại) và ảnh final, mô tả định tính | q05_2 **ĐẠT**. q05_3 **CHƯA ĐỦ**: chưa gán nhãn từng khung (79 khung B2, 21 khung B0), chưa có con số sai loại / trùng / một phần / bỏ sót. Lý do khách quan: gói nhãn trắng q05 chưa được push |
| 3. Giải thích vì sao B2 kém B0, đề xuất cải thiện | Phát hiện độ nhạy: bỏ q05_3 thì kết luận đảo chiều; giả thuyết mẫu raspberry gây lỗi (ghi đúng là giả thuyết) | **ĐẠT một phần.** Phát hiện độ nhạy đúng và có giá trị. Còn thiếu: bảng chênh lệch từng query, liên hệ với chất lượng mẫu tự chọn, và đề xuất cải thiện cụ thể |
| 4. Hoàn thiện báo cáo, ghi rõ phần tự kiểm, trước/sau, hạn chế; duyệt chung | Báo cáo ghi rõ "Triệu tự chạy, assistant chỉ hướng dẫn", so với bản 24/10, ghi kết luận nguyên văn vào PILOT_SUMMARY §7 | **ĐẠT phần ghi chép**; mục hạn chế còn ngắn. Duyệt chung chưa làm (đúng, đó là bước tiếp) |

**Về độ độc lập:** Triệu tự chạy lệnh, tự tính bằng Excel, tự xem ảnh. Assistant của Triệu có hướng dẫn, giải thích lại và chấm câu trả lời, và báo cáo ghi điều đó rõ ràng. Mức này nên gọi là **"tự kiểm có hướng dẫn"**. So với bản 24/10 (AI làm hộ), đây là tiến bộ thật, đáp ứng đúng nhận xét 1.

## Lưu ý cập nhật kết luận B0/B2

Triệu kết luận "B2 kém B0 tùy trường hợp, không ghi tổng quát". Kết luận này **đúng với pilot 15 câu**. Tuy nhiên trên tập mới `p4_unseen_v1` (10 ảnh khóa, 27/10), B2 kém B0 rõ ràng: Δ MAE +6.23, CI theo ảnh [+2.0, +12.3]. Đọc thêm [kết quả P4.6](P4_6_UNSEEN_RESULTS_20261027.md). Báo cáo nên ghi: "pilot thì mong manh (phụ thuộc q05_3); tập mới xác nhận B2 kém B0".

## Đề xuất cho Trí

1. **Nghiệm thu nhận xét 1 và phần q05_2** (đạt). Có thể chấp nhận thiếu 2 ca thử, hoặc nhờ Triệu bổ sung (khoảng 15 phút).
2. Push các file local (kế hoạch V2, gói q05, P4.6), rồi nhờ Triệu làm **phần còn lại**:
   - q05_3: gán nhãn 79 + 21 khung bằng `results/countgdpp/q05_error_analysis_package_20261027/`, ra bảng phân rã;
   - B2 so với B0: thêm bảng chênh lệch từng query, liên hệ với mẫu tự chọn, 2–3 đề xuất cải thiện; dùng thêm kết quả tập mới.
3. 47 nhãn q03 (P4 dev) vẫn chưa làm. Ưu tiên thấp hơn N4 hiện tại.
4. Sau đó hai bạn duyệt chung PILOT_SUMMARY §7.
