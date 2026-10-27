# Đang ở đâu trong pipeline và lịch đến 02/12 (cập nhật 27/10 khuya)

## 1. Pipeline toàn đồ án

```
[1] Chạy CountGD++ ✅ ─ [2] Pilot tìm lỗi ✅ ─ [3] Cải tiến v1 (lọc khung + freeze) ✅ ─ [4] Kiểm trên 10 ảnh mới ✅
                                                                                              │
          ┌───────────────────────────────────────────────────────────────────────────────────┘
          ▼
[5] N4 review khung ◀── BẠN ĐANG Ở ĐÂY (u01_1 xong 9/78; phần còn lại giao Triệu, hạn 30/10)
          ▼
[6] Chọn nhánh cải tiến v2: P (kiểm mẫu trước lượt 2) hay R (lọc giữ vật đúng)   ~02/11
          ▼
[7] Tập dữ liệu mới: dev 20 + test 40 ảnh, kiểm absent/GT, khóa                   03–08/11
          ▼
[8] Code nhánh đã chọn + đối chứng C6 (B0 + lọc), chạy và chọn tham số trên dev   09–15/11
          ▼
[9] Chốt + freeze v2                                                               16–22/11
          ▼
[10] Một lần chạy trên test 40 ảnh → bảng cuối                                    23–26/11
          ▼
[11] Báo cáo + slide + demo                                                        27/11–02/12
```

Song song: Triệu làm nốt kiểm chéo pilot (q05_3, phân tích B2/B0) → nhóm duyệt pilot (03/11).

**Đã xong khoảng 45–50% khối lượng.** Phần còn lại tập trung vào [7]–[8] (dữ liệu + code + chạy) và [11] (viết).

## 2. Việc của Trí, theo buổi, để xếp lịch tập trung

| Khi nào | Việc của Trí | Thời gian tập trung | Ghi chú |
|---|---|---:|---|
| **28/10** | (a) Commit + push toàn bộ file local (lệnh ở §4) và gửi Triệu [GIAO_VIEC](../HANDOFF/GIAO_VIEC_TRIEU_20261028.md); (b) đọc [đánh giá Triệu](../reports/DANH_GIA_TRIEU_TU_KIEM_20261027.md), nghiệm thu phần đạt; (c) chốt quy tắc dữ liệu mới ([§4 kế hoạch](KE_HOACH_CAI_TIEN_20261027.md)): dev 20 + test 40, trộn cặp khác hẳn và cặp dễ nhầm | **45 phút** | (a) là việc **chặn** Triệu: chưa push thì Triệu không có gói |
| 31/10–02/11 | Khi Triệu xong N4: cùng assistant xem bảng E1–E4 và **chọn P hay R** | 45 phút | Quá 31/10 thì chọn bằng chỉ báo tự động |
| 03–08/11 | Assistant rút và chia tập. Trí kiểm absent/GT **dev 20 ảnh** (Triệu kiểm test 40), rồi khóa. Duyệt pilot chung | **2 giờ** | Làm theo HUONG_DAN như lần trước |
| 09–15/11 | Cho phép assistant viết code + chạy dev (GPU local khoảng 1 giờ / cấu hình / 60 query). Trí đọc bảng dev, quyết tham số | **1,5 giờ** | Không cần Kaggle |
| 16–22/11 | Chốt + freeze v2. Bắt đầu viết báo cáo: giới thiệu, phương pháp, thiết lập thí nghiệm | **3 giờ** | Dùng [TOM_TAT](../reports/TOM_TAT_DU_AN_20261027.md) làm khung |
| 23–26/11 | Cho phép chạy test **một lần**; đọc kết quả, viết phần kết quả và hạn chế | **2,5 giờ** | Kết quả âm vẫn báo trung thực |
| 27/11–01/12 | Hoàn thiện báo cáo, slide, demo, diễn tập | **4 giờ** | 30/11–01/12 để dự phòng |
| **02/12** | **Nộp / báo cáo** | | |

**Tổng thời gian tập trung của Trí: khoảng 14–15 giờ trong 5 tuần (khoảng 3 giờ/tuần).** Tuần nặng nhất là 23/11–01/12 (khoảng 6,5 giờ). Triệu khoảng 5 giờ tuần này, sau đó khoảng 5 giờ (V8–V10).

## 3. Rủi ro và cách xử lý

| Rủi ro | Dấu hiệu | Xử lý |
|---|---|---|
| N4 trễ | 31/10 chưa có CSV | Chọn nhánh bằng chỉ báo tự động, ghi rõ giới hạn |
| Nhánh P/R không thắng trên dev | Bảng dev 15/11 | Dừng sớm; báo cáo theo hướng **phân tích lỗi + đánh đổi** (vẫn đủ cho môn học) |
| Kiểm absent/GT 60 ảnh quá tốn | Quá 08/11 | Giảm còn dev 15 + test 30, ghi lý do **trước** khi chạy |
| GPU 4 GB không đủ (CLIP chen giữa 2 lượt) | Lỗi OOM | Chạy 3 bước tách rời (đã thiết kế); bí quá thì dùng Kaggle |

## 4. Lệnh commit/push cho 28/10 (Trí tự chạy)

```powershell
cd D:\MINHTRIHOCCODE\HOCKI5\CS331
git status --short          # xem lại; data_external/ đã được .gitignore
git add -A
git reset -q -- "quá khứ/*.zip"   # snapshot local 59,5 MB, không cần đưa lên GitHub
git commit -m "P4.6: tập p4_unseen_v1, runner frozen, kết quả, N4, kế hoạch cải tiến, đánh giá Triệu"
git push origin main
```

Sau khi bỏ snapshot, commit còn khoảng 60 MB (ảnh N4, q05, kết quả P4.6); không file nào vượt giới hạn 100 MB của GitHub. Ảnh MUCCA gốc (`data_external/`) không lên GitHub. Triệu nếu cần thì tải lại từ Zenodo 19231375; N4/q05 không cần vì gói đã có sẵn ảnh cắt.
