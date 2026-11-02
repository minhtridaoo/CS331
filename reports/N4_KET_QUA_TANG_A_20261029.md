# N4 tầng A — kết quả review khung bằng người và đề xuất chọn nhánh (29/10/2026)

> **Đính chính 02/11:** vài diễn giải ở bản này mạnh hơn bằng chứng ("model bỏ qua prompt", "E1 chiếm ưu thế", "bỏ R"). Xem [RA_SOAT_TRIEU_N4_20261029](RA_SOAT_TRIEU_N4_20261029.md) §5. Các con số giữ nguyên; với query có mặt, mẫu đúng loại là 1/12.

**Nhãn:** Triệu gán, commit `be4da26` (29/10 00:26, trước hạn 30/10). u01_1 có thêm nhãn của Trí (27/10). **Ghép bảng tra và tính:** assistant, chỉ đọc file đã lưu, không chạy model.
**Phạm vi:** 7 query lỗi có chủ đích (4 "people" + 3 absent bị báo > 0). Đây là **phân tích lỗi, không phải mẫu đại diện** cho cả tập. Tầng B (V6) chưa làm.

## 1. Kiểm chất lượng nhãn

- 17 CSV / 117 dòng: đủ dòng, mọi nhãn thuộc bộ quy ước, đủ `actual_class` / `reviewer` / `date`.
- Rank, ID và tọa độ khớp tuyệt đối với gói gốc. Excel chỉ đổi cách hiển thị `474.0` → `474`, giá trị số không đổi.
- Review mù: Triệu ghi đã không mở `_KEY_` và bản của Trí. Assistant của Triệu có hướng dẫn và đối chiếu; Triệu tự gán nhãn.
- **Hai người đồng ý ở u01_1: 9/9** (cùng `label_type`, cùng vật thật là chó).

## 2. Kết quả

**Khung được bộ lọc giữ lại (gói chính, 7 query):**

| Bộ lọc | Khung giữ | Đúng loại (`target`) | Sai loại | Bao nhiều vật | Chưa chắc |
|---|---:|---:|---:|---:|---:|
| B2 lọc điểm | 78 | **0** | 71 | 6 | 1 |
| Fusion 50/50 | 14 | **0** | 11 | 2 | 1 |

Vật thật trong các khung đó:
- u01_1 people → 9 chó;
- u01_3 sheep → 10 chó;
- u02_1 people → 11 chó;
- u07_1 people → 9 ô tô;
- u07_3 bicycles → 9 ô tô;
- u08_1 people → 6 ô tô;
- u10_3 bicycles → 24 ô tô.

**Model bỏ qua prompt** (đo trực tiếp từ prediction, IoU ≥ 0.8):

| Ảnh | Cặp query | Khung trùng |
|---|---|---|
| mcac_88 | "people" so với "cars" | **21/21** |
| mcac_88 | "people" so với "bicycles" | 21/21 |
| mcac_84 | "motorbikes" so với "bicycles" | 73/80 |
| mcac_123 | "people" so với "sheep" | 24/38 |

Đây là bằng chứng trực tiếp cho lỗi X/Y.

**E1, mẫu tự chọn** (21 mẫu): **chỉ 1/21 đúng loại** (u01_1 P2, một người). Còn lại 10 `multi_object` (một khung bao nhiều vật) và 10 `wrong_class`. Chỉ báo tự động trước đó ước 3/21 đúng.

**E3, khung đúng bị lọc mất** (18 ứng viên ở 3 query people): **13 là người thật**, 3 là một phần người, 2 chưa chắc. Có khoảng 72% ứng viên tự động đúng là người.
- u08_1: cả 7/7 người thật (bằng GT 7) đều bị lọc, trong khi bộ lọc giữ toàn ô tô.
- u01_1: người ở khung E3 #18 chính là mẫu P2. Model đã chọn đúng người làm mẫu, nhưng sang lượt 2 lại lọc mất người đó.

## 3. Nghĩa là gì cho việc chọn nhánh

1. **Lỗi bắt đầu từ mẫu tự chọn (E1 chiếm ưu thế):** 20/21 mẫu sai loại hoặc bao nhiều vật. Lượt 2 được dẫn bởi mẫu sai, nên tạo khung của loại kia.
2. **Vật đúng có sẵn trong ứng viên (E3 có thật), nhưng bộ lọc chấm ngược:** cả lọc điểm CountGD++ lẫn Fusion đều giữ 0 vật đúng và bỏ người thật. Với các query này, điểm CountGD++ ưu tiên loại sai.
3. Hệ quả:
   - **Nhánh R** ("cứu" khung có điểm CountGD++ cao) sẽ cứu nhầm chính các khung chó/ô tô, đúng rủi ro mà kế hoạch đã cảnh báo. **Không nên chọn R làm nhánh chính.**
   - **Nhánh P** (kiểm mẫu bằng CLIP trước lượt 2) nhắm đúng nút thắt: mẫu đúng loại có tồn tại (ví dụ u01_1 P2, các người ở u08_1), chỉ là không được chọn. Nên thêm điều kiện "mẫu chỉ chứa **một** vật", vì 10/21 mẫu bao nhiều vật.
4. **Rủi ro cho P:** ở mcac_88, khung cuối gần như giống hệt nhau dù đổi prompt và đổi mẫu. Có thể lượt 2 bị ảnh chi phối mạnh, khi đó chỉ sửa mẫu là chưa đủ. Vì vậy **bắt buộc có đối chứng C6 (B0 + bộ lọc)** và phải thử nhanh trên dev trước.
5. Chỉ báo tự động điểm-trong-khung **lạc quan hơn** nhãn người (E1 3/21 so với 1/21). Con số "31 khung sai loại" của Fusion trong báo cáo P4.6 nhiều khả năng còn thấp hơn thực tế. Khi viết báo cáo, nhấn mạnh rằng đây là phép xấp xỉ.

**Đề xuất (Trí quyết):** chọn **nhánh P** (P1 + điều kiện một vật) làm nhánh chính, giữ C6 làm đối chứng bắt buộc, bỏ R. Trước khi chốt hẳn, nên có tầng B (V6): các query mà mẫu đúng sẵn, để chắc P không làm hỏng các ca đang tốt.

## 4. Nguồn

- Nhãn: `results/countgdpp/p4_n4_review_package_20261027/` (`A_*_labels_*.csv`, `bo_sung_F0/`). Bảng tra: `_KEY_mo_sau_khi_review/rank_kept_by.json`.
- Prediction: `results/countgdpp/p4_unseen_v1_b2_20261027/predictions.jsonl`. Quy ước chấm: HUONG_DAN §4.
