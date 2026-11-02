# Kiểm việc Triệu sau khi pull 71009c8 — 02/11/2026

**Người kiểm:** assistant, theo yêu cầu của Trí. Chỉ đọc file, không chạy model/evaluator. Đây là đề xuất để Trí nghiệm thu, không phải chữ duyệt.
**Commit mới:** `415af3b` (29/10 18:22, V3 + app gán nhãn), `71009c8` (30/10 00:09, V5 + đề xuất nhánh P).

## 1. Trạng thái V1–V7

| Việc | Hạn | Trạng thái | Kiểm |
|---|---|---|---|
| V1–V2 N4 tầng A | 30/10 | ✅ nộp 29/10 | Đạt cấu trúc (117 dòng). Chất lượng phân rã lỗi còn vài ca cần thống nhất, xem [RA_SOAT](RA_SOAT_TRIEU_N4_20261029.md) §4, §7 |
| **V3** q05_3, 103 khung | 01/11 | ✅ nộp 29/10 | 103/103 có nhãn và reviewer; rank/tọa độ trùng gói gốc. B0 21 = 3 target + 18 sai loại; B2 79 = 2 target + **58 part** + 19 sai loại; part theo quả b1/b2/b3 = 23/21/14. Quy ước object_id ghi rõ |
| V4 2 ca thử (uncertain, absent > 0) | 01/11 | ❌ **chưa có** | Báo cáo vẫn chỉ có 5 ca cũ |
| **V5** phân tích B2/B0 + đề xuất | 01/11 | ✅ nộp 30/10 | Số khớp khi tính lại: tập mới 2 tốt hơn / 15 kém hơn / 13 bằng; bỏ u10_2 thì MAE B0 = 187/29 = 6.45, B2 = 327/29 = 11.28. Có bảng mẫu tự chọn gắn với chênh lệch từng query; đề xuất ở [TRIEU_DE_XUAT_NHANH_P](TRIEU_DE_XUAT_NHANH_P_20261029.md) |
| V6 N4 tầng B | **02/11 (hôm nay)** | ❌ **chưa có** (0/58 dòng) | — |
| V7 duyệt chung | 03/11 | Chờ buổi 03/11 | — |

**App gán nhãn** `evaluation/box_label_app.py` (Triệu, có assistant hỗ trợ): chạy local, chỉ đọc gói q05_3, ghi đúng các cột nhãn; không đọc `_KEY_`, không gợi ý nhãn. Có hiện "các khung chồng lên", nên **đã khắc phục hạn chế "crop không vẽ biên bbox thật"** mà bản RA_SOAT nêu, nhưng hiện chỉ dùng cho gói q05.

## 2. Nhận xét chất lượng

**Tốt:**
- V3 cho bằng chứng **lỗi kiểu thứ hai**: mẫu đúng loại (2/3) mà B2 vẫn tăng từ 21 lên 79 khung, toàn bộ phần tăng là khung một phần quả (`part`). Kiểm loại bằng CLIP không chặn được lỗi này. Phát hiện tốt, có số liệu.
- V5 sửa kết luận cũ "B2 tùy trường hợp" bằng dữ liệu tập mới, tách rõ pilot với tập mới, có ghi chú "không so MAE giữa hai tập".
- Đề xuất nhánh P ghi rõ phần nào là ý của Trí, phần nào Triệu thêm; ghi "chưa có bằng chứng riêng" cho bước kiểm một vật; có §7 "đã cân nhắc và không chọn".

**Cần sửa khi đưa vào báo cáo:**
1. "20/21 mẫu không đúng loại" có **9 mẫu của query vắng mặt** (không thể đúng). Với query có mặt nên ghi **1/12** (giống RA_SOAT §2).
2. "E1 phổ biến hơn E3" và "rủi ro R đã xảy ra thật": hai nhóm khác mẫu, khác đơn vị. N4 A chưa đủ để loại R (RA_SOAT §5). Chính đề xuất cũng đã ghi "nếu P1 không thắng Fusion, R vẫn còn giá trị". Giữ cách nói đó.
3. Tầng A là ca lỗi chọn có chủ đích. Thiếu V6 (tầng B), nên chưa thấy được P có làm hỏng các ca đang tốt hay không.

## 3. Bằng chứng mới cần đưa vào buổi chọn nhánh 03/11

RA_SOAT §3 (đọc raw đã lưu): ở lượt 2, điểm cuối mỗi khung là **max của cả token chữ lẫn token mẫu ảnh**. Ô tô khi hỏi "people" có điểm chữ 0,04–0,08 nhưng điểm mẫu ảnh khoảng 0,97, nên qua ngưỡng. Người thật có điểm chữ khoảng 0,44, nên bị loại.

Gợi ý thêm một biến thể **rẻ nhất, không cần CLIP và không cần GT** vào danh sách so sánh trên dev:
- **T — chấm lượt 2 chỉ bằng token chữ.** Bỏ token mẫu ảnh khỏi phép max khi quyết định giữ khung. Biến thể này kiểm trực tiếp cơ chế vừa thấy, và có thể giảm cả E1 lẫn E3 cùng lúc.

Bộ đối chứng sẽ là B0, B2, F, **T**, P, P+F, C6 (B0 + F). Ngưỡng của T chọn trên dev.

## 4. Đề xuất cho Trí

1. **Nghiệm thu V3 và V5** (đạt). Ghi chú cho Triệu sửa 3 điểm diễn đạt ở §2.
2. **Nhắc Triệu V4 (15 phút) và V6 (khoảng 40 phút)**, dời hạn sang 04/11. Không chờ V6 để họp 03/11; buổi họp chọn nhánh vẫn chạy được.
3. **Buổi 03/11** chốt hai việc:
   - danh sách biến thể thử trên dev: đề xuất T + P (+ chống chia mảnh nếu kịp), luôn có C6; R giữ dự phòng;
   - quy tắc dữ liệu dev 20 + test 40.
