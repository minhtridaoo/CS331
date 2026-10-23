# q02_1 — Kiểm từng box stage 1 và final

**Ngày:** 19/10/2026. **Prompt:** plates. **Ảnh:** mcac_11.jpg.

Đây là bản đối chiếu bằng mắt của assistant, kết hợp ảnh gốc 390×280, từng box hiển thị riêng, tọa độ prediction và 15 điểm nhãn đĩa nguồn. Các cặp Triệu đã xác nhận được giữ nguyên. Các phép giao/bao chứa box chỉ hỗ trợ tìm ca cần xem; không tự coi box chồng nhau là cùng vật.

## Kết quả đối chiếu

| Lượt | Tổng box | Nhóm đĩa riêng biệt | Box sai loại | Box dư do cùng khoanh một đĩa |
|---|---:|---:|---:|---:|
| Stage 1 | 28 | 15 | 3 | 10 |
| Final | 31 | 15 | 3 | 13 |

Theo cách ghép vật thể trong bản review này:

- Stage 1: **15 đĩa + 10 box trùng + 3 box sai loại = 28**.
- Final: **15 đĩa + 13 box trùng + 3 box sai loại = 31**.
- Cả hai lượt có box tương ứng với cả 15 vị trí đĩa trong nhãn nguồn. Final tăng số box dư do trùng, chưa khắc phục sai loại. Kết quả này không chứng minh nguyên nhân nằm ở một mẫu hoặc một thành phần cụ thể.

**Độ chắc chắn:** ảnh nhỏ, nhiều mép đĩa mảnh/che khuất; các nhóm ở chồng đĩa phía trên và vùng chuyển giữa hai tầng bên trái có độ chắc chắn vừa. Đã gán đối tượng cho toàn bộ 59 box để giải thích số đếm, nhưng đây chưa phải bộ nhãn bbox đã được con người phân xử đầy đủ hoặc phép chấm định vị benchmark. Không ép nhóm box chỉ để tổng bằng 15.

## Các box sai loại

| Lượt | Bát | Miệng ly |
|---|---|---|
| Stage 1 | 10, 19 | 25 |
| Final | 7, 16 | 25 |

Số box là số trên overlay của đúng lượt đó, bắt đầu từ 1.

## Bảng ghép từng đĩa giữa hai lượt

L01–L12 là các vị trí đĩa bên trái, từ trên xuống. R01–R03 là ba đĩa bên phải, từ trên xuống. Nhóm có nhiều ID biểu thị nhiều box cùng chỉ một đĩa theo review; không phải nhiều đĩa khác nhau.

| Đĩa | Điểm nhãn nguồn (x,y) | Box stage 1 | Box final | Độ chắc chắn |
|---|---|---|---|---|
| L01 | 128,140 | **8, 17, 28** | **6, 30** | Vừa |
| L02 | 130,146 | 5 | **4, 9** | Vừa |
| L03 | 129,153 | **2, 3** | 5 | Vừa |
| L04 | 129,161 | 13 | **3, 31** | Vừa |
| L05 | 130,166 | 11 | 2 | Vừa |
| L06 | 131,170 | 1 | 1 | Vừa |
| L07 | 105,183 | **9, 15, 21** | **10, 15, 21, 24, 27** | Vừa |
| L08 | 105,189 | 6 | 23 | Vừa |
| L09 | 104,196 | 4 | 8 | Vừa |
| L10 | 105,204 | **14, 18** | 11 | Cao |
| L11 | 105,211 | 20 | **13, 17, 18** | Cao |
| L12 | 131,218 | **16, 23** | 20 | Cao |
| R01 | 273,218 | **7, 27** | **12, 19, 28** | Cao |
| R02 | 273,226 | **12, 22** | **22, 26** | Vừa |
| R03 | 274,236 | **24, 26** | **14, 29** | Cao |

Stage 1 có 8 nhóm nhiều box với tổng 10 box dư. Final cũng có 8 nhóm nhiều box nhưng tổng 13 box dư. Cặp 24/26 stage 1 giữ nhận xét của Triệu: 24 khoanh toàn bộ đĩa, 26 là vùng nhỏ hơn trên chính đĩa đó. Không chỉ định một box “chuẩn” trong các nhóm khác khi chưa chấm độ khít.

## Đối chiếu GT 15 đĩa

Ảnh và nhãn nguồn phù hợp cách đếm **12 vị trí đĩa bên trái + 3 bên phải = 15**. Các điểm nhãn đã được ghép theo vị trí và các tầng đĩa nhìn thấy, không phải 28 hay 31 vật khác nhau. Không thấy cơ sở để đổi GT 15 chỉ vì model trả nhiều box. Các tầng sát nhau vẫn có hạn chế do độ phân giải; nên xem đây là GT nguồn được kiểm tra tính phù hợp, chưa phải nhãn vị trí hoàn chỉnh mới.

## Ảnh đối chiếu từng box

Các ảnh dưới được chụp từ bản hiển thị ảnh gốc với một khung mỗi ô. Đây là phóng to hiển thị, không bổ sung chi tiết ảnh hoặc chạy model mới.

- [Stage 1 — chồng đĩa trên](q02_1_evidence/upper-stack.png)
- [Stage 1 — đoạn giữa bên trái](q02_1_evidence/left-middle.png)
- [Stage 1 — các đĩa dưới bên trái](q02_1_evidence/left-bottom.png)
- [Stage 1 — ba đĩa bên phải](q02_1_evidence/right-stack.png)
- [Final — chồng đĩa trên](q02_1_evidence/final-upper.png)
- [Final — đoạn giữa bên trái](q02_1_evidence/final-left-middle.png)
- [Final — các đĩa dưới bên trái](q02_1_evidence/final-left-bottom.png)
- [Final — ba đĩa bên phải](q02_1_evidence/final-right.png)

## Dữ liệu review

- `q02_1_stage1_box_review.json`: đủ 28 box, cập nhật từ các nhận xét ban đầu của Triệu; phân biệt phần Triệu đã xác nhận và phần assistant ghép thêm.
- `q02_1_final_box_review.json`: đủ 31 box.
- `q02_1_plate_correspondence.json`: 15 nhóm đĩa và ID tương ứng hai lượt.

Prediction, ảnh đầu vào, ngưỡng và annotations nguồn giữ nguyên. Tổng số box đã được kiểm tính đủ/duy nhất và phân rã số đếm khớp cả hai lượt.
