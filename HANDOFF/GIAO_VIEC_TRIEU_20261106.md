# Giao việc cho Triệu — đợt 2, từ 06/11/2026

**Người giao:** Trí (assistant soạn theo yêu cầu của Trí, 05/11). Thay cho phần còn lại của [đợt 1](GIAO_VIEC_TRIEU_20261028.md); V1–V6 đợt 1 đã xong và đạt kiểm.
**Quyết định đã chốt:** Trí đồng ý **toàn bộ khuyến nghị D1–D10** trong [KE_HOACH_TIEP_THEO_20261105.md](../reports/KE_HOACH_TIEP_THEO_20261105.md) §3, đồng thời nghiệm thu V3–V6. Triệu **không cần chờ Trí** để làm các việc dưới đây.

## 0. Tóm tắt quyết định (chi tiết ở §3 kế hoạch)

- **Máy chuẩn = Colab T4.** Tiêu chí tái hiện = Kiểm A + Kiểm C. Chỉ so các cách **trong cùng một lần chạy T4**.
- **Dữ liệu:** dev 20 + test 40 ảnh, mỗi lớp 3–40 điểm, cặp dễ nhầm lấy xoay vòng qua các siêu nhóm, không thêm absent loại dễ, seed 331. **Đây đúng là các giá trị mặc định của `select_dev_test_v2.py`.**
- **Biến thể thử trên dev:** B0, B2, P (lưới tau), T, P+T, bộ lọc S/F **chọn lại ngưỡng riêng cho từng nguồn**, C6.
- **Luật chọn cấu hình cuối (D9, chốt trước khi xem dev):** MAE cả tập nhỏ nhất trên dev, với điều kiện MAE có mặt ≤ của B0 và FPR_absent ≤ của B0. Không cấu hình nào đạt thì báo kết quả âm.

## 1. Việc và hạn

| # | Việc | Ước lượng | Hạn | Chặn việc khác? |
|---|---|---:|---|---|
| **W1** | **Rút dữ liệu thật** (lệnh ở §2), commit thư mục `experiments/countgdpp/dev_test_v2/` ở trạng thái DRAFT | 10 phút | **06/11** | **Có**: Trí cần để kiểm dev |
| **W2** | Đưa output P1 pilot từ Drive vào repo: `predictions_*.jsonl`, `run_config.json`, bảng đối chứng (`_controls_eval`) của run `p1_pilot_colab_20261103_1519` và `_1528`. **Không** đưa `.npz` hay ảnh | 15 phút | 06/11 | Có: để assistant kiểm độc lập |
| W3 | Ghi xác nhận duyệt pilot (V7) của Triệu vào PILOT_SUMMARY §7 (Trí đã đồng ý ngày 05/11) | 10 phút | 06/11 | Không |
| **W4** | **Kiểm absent/GT tập test 40 ảnh** theo `HUONG_DAN_KIEM_DU_LIEU.md` (Trí kiểm tập dev 20 ảnh) | khoảng 2 giờ | **08/11** | **Có**: chưa khóa thì chưa chạy được |
| W5 | Khi cả dev lẫn test đã kiểm xong: khóa (`status=LOCKED`, người/ngày, hash) | 10 phút | 08/11 | Có |
| **W6** | **Chạy trên T4 với tập dev** (lệnh ở §3). **Không chạy test** | khoảng 2–3 giờ GPU | **10/11** | Có |
| W7 | Bắt đầu viết Related Work (CountGD++, PseCo, DAVE, PrACo++/MUCCA, VA-Count) | khoảng 2 giờ | 20/11 | Không |

**Thứ tự làm:** W1 → W2 → W3 (cùng ngày 06/11) → W4 → W5 → W6. W7 làm khi rảnh.

## 2. Lệnh rút dữ liệu (W1)

```text
python experiments/countgdpp/select_dev_test_v2.py --n-dev 20 --n-test 40 --mucca C:/Users/diosodumb/Downloads/MUCCA_1.0 --out experiments/countgdpp/dev_test_v2
```

Không thêm tham số nào khác. Mặc định đã là seed 331, 3–40 điểm, không `--easy-absent`. Rút **một lần duy nhất**; nếu cần rút lại, ghi lý do vào WORKLOG **trước** khi rút.

## 3. Lệnh chạy dev (W6, chỉ sau W5)

Trên notebook Colab hiện có (`colab_p1_verified_pseudo.ipynb`), đổi input sang dev:

```text
run_b2_verified_pseudo.py --inputs experiments/countgdpp/dev_test_v2/dev/inputs.jsonl
  --run-id p1_dev_t4_<ngày> --tau-pseudo 0.18 0.20 0.22 0.24 0.26 0.28 --m 10 --replay-b2
```

- Lưu đủ raw `stage1_raw.npz` và `stage2_*_raw.npz` (runner đã lưu sẵn). **Biến thể T và việc chọn lại ngưỡng S/F riêng từng nguồn sẽ tính ngoại tuyến từ raw này**, nên không cần chạy lại GPU.
- Nếu còn quota, chạy thêm một lần với `--m 5` (run-id riêng) để có lưới M.
- Đưa vào repo `predictions_*.jsonl` + `run_config.json`; giữ `.npz` trên Drive và chia sẻ cho Trí.
- **Không mở `dev_test_v2/test/`** để chạy hay xem kết quả. Test chỉ chạy **một lần** ngày 23–24/11, sau khi khóa cấu hình.

## 4. Việc của Trí và assistant song song (để Triệu biết)

| Ai | Việc | Hạn |
|---|---|---|
| Trí | Kiểm absent/GT tập **dev 20 ảnh** (khoảng 1 giờ) | 07–08/11 |
| Assistant | Viết công cụ ngoại tuyến cho: (a) biến thể **T** (chấm lượt 2 chỉ bằng token chữ); (b) **chọn lại ngưỡng S/F riêng từng nguồn** trên dev; (c) chấm theo luật D9. Kiểm trên raw pilot | 09/11 |
| Assistant | Kiểm độc lập output P1 pilot (W2) và kết quả dev (W6) | sau W2, W6 |

## 5. Báo lại

Mỗi việc xong thì commit + push, kèm 1 mục WORKLOG, rồi báo Trí. Không cần chờ Trí duyệt giữa các bước W1–W6, trừ khi gặp chuyện bất thường, ví dụ phải rút lại dữ liệu hay lớp absent nhìn thấy trong ảnh mà không có lớp dự phòng.
