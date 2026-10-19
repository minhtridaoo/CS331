# M5 — review B0/B2 trên cùng hai ảnh

**15/10/2026. Run b2_two_images_20261015, ngưỡng chọn mẫu/cuối 0.23, top3.**

**Bổ sung cùng ngày:** Trí đã kiểm bằng mắt cả 6 query; [nhận xét của người dùng](USER_VISUAL_REVIEW.md) được lưu riêng, chưa được Triệu kiểm chéo. E1/E2 pilot đã thực hiện; phần “tiếp theo” phía dưới là kế hoạch tại thời điểm review M5, xem [kết quả E2 và bước hiện tại](../m6_e2_sample050_20261015/REVIEW.md).

Đã kiểm run complete, đủ 6 IDs/GT, schema/khung/score và tọa độ mẫu. Cả 6 stage1 khớp baseline cũ. Có 5 lượt hai thực sự; chairs không có mẫu nên dùng fallback B0. Đã xem 18 ảnh stage1/pseudo/final trong hai bảng ghép.

| Query | GT gói Triệu | B0 | B2 | Số mẫu |
|---|---:|---:|---:|---:|
| guitars | 25 | 25 | 25 | 3 |
| amplifiers | 11 | 44 | 38 | 3 |
| chairs | 1 | 0 | 0 | 0 |
| pens | 6 | 17 | 13 | 3 |
| rulers | 6 | 18 | 18 | 3 |
| pencils | 6 | 17 | 16 | 3 |

## Quan sát mẫu và khung

- Guitar: ba mẫu nhìn là guitar; số đếm 25 giữ nguyên. Chưa chấm đúng vị trí tuyệt đối.
- Ampli: ba mẫu nhìn đều là guitar; lượt hai vẫn lấy nhiều guitar. Count giảm 44→38 chưa giải quyết sai loại.
- Ghế: không có mẫu, không gọi lượt hai; 0→0 là fallback, không phải bằng chứng bước hai đã thử mà không giúp.
- Bút mực: mẫu trộn bút mực và bút chì; final 13 vẫn gồm nhiều loại.
- Thước: ba mẫu chọn đúng thước, nhưng final 18 vẫn lấy bút mực/bút chì. Đây là ca cho thấy trong cấu hình hiện tại, chỉ chọn mẫu đúng chưa đủ giải quyết lỗi.
- Bút chì: ba mẫu nhìn đều là bút mực; final 16 vẫn gồm nhiều loại.

Nhận xét bằng mắt của assistant, cần Triệu kiểm chéo. Không thay GT hoặc dùng các nhãn nhận xét này làm mẫu đầu vào.

## Kết luận có giới hạn

Trên cùng 6 query, MAE_present B0=11.3333 và B2=9.5; sai số giảm ở 3 query, không đổi ở 3 query. Cả hai chỉ 1/6 query đúng count. Không so 9.5 trực tiếp với MAE 19.4 của 15 query trước vì khác tập đánh giá. Số đếm giảm không tự chứng minh chọn đúng loại. Chưa có absent query, chưa phải holdout hoặc cấu hình đầy đủ paper.

Có bằng chứng hai tình huống để nghiên cứu: mẫu bị chọn nhầm loại; mẫu đúng nhưng lượt hai vẫn đếm nhầm. Không quy toàn bộ lỗi cho mẫu sai và không khẳng định quan hệ nhân quả chỉ từ quan sát.

## Bước tiếp theo — M6 đối chứng ngưỡng

Khảo sát riêng tau_final trên raw lượt hai đã lưu, giữ nguyên mẫu/tau_sample=0.23. Ghi rõ đây là khảo sát dev, xem cả bỏ khung sai và mất vật đúng; không chọn ngưỡng chỉ để count gần GT của từng ảnh. Query fallback báo riêng. Nếu đổi tau_sample phải chọn mẫu và chạy lượt hai lại; không tái dùng raw stage2 cũ.

Giữ baseline/cấu hình gốc; chưa train/chốt module cải tiến. Sau đối chứng đơn giản và kiểm trên bộ dev rộng hơn mới quyết định hướng đào sâu. Triệu cần kiểm chéo mẫu/khung, evaluator, absent và holdout. M5 hiện mới pilot 2 ảnh/6 query, chưa B2 đủ 5 ảnh.

[Bảng từng query](review_per_query.csv) · [Chỉ số có hash](review_metrics.json) · [Guitar/ampli](guitars_comparison.jpg) · [Văn phòng phẩm](stationery_comparison.jpg)
