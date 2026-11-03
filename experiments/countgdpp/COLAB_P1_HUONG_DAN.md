# Chạy nhánh P1 trên Colab (03/11/2026)

**File:** [colab_p1_verified_pseudo.ipynb](colab_p1_verified_pseudo.ipynb) gọi [run_b2_verified_pseudo.py](run_b2_verified_pseudo.py) + [pseudo_clip_verifier.py](pseudo_clip_verifier.py). Runner B2 cũ (`run_b2_frozen.py`, `run_b2_pilot.py`) giữ nguyên.

**P1 làm gì:** lượt 1 (= B0) → tối đa `M=10` ứng viên điểm > 0.23 → CLIP (`a photo of {prompt}`, cùng model/revision/crop với P4) chấm từng ứng viên → giữ ứng viên có cosine ≥ `tau_pseudo`, lấy tối đa 3 theo điểm CountGD → lượt 2. Không còn mẫu nào thì trả B0. Nhiều `tau` dùng chung một lượt 1. Kèm `--replay-b2` để chạy lại B2 gốc từ cùng lượt 1 và so với B2 đã lưu (kiểm tái hiện trên GPU mới).

**Mã băm nguồn:** audit 14/10 tính trên bản checkout Windows (CRLF); clone trên Colab là LF. Runner P1 đưa xuống dòng về CRLF trước khi băm (`source_sha`), nên vẫn bắt được mọi thay đổi code. `run_b2_frozen.py` cũ chưa có bước này nên sẽ báo "Stock source changed" nếu chạy trên Colab.

**Đã kiểm trước khi chạy GPU (CPU, raw đã lưu):** cách chọn ứng viên trùng `select_pseudo` và trùng mẫu B2 đã lưu ở 45/45 query (pilot 15 + p4_unseen_v1 30). Ô tóm tắt chạy đúng trên dữ liệu giả lập (MAE B2 pilot = 22.00).

## Kết quả chạy trên Colab T4 (03/11/2026, commit 9606a59)

Hai lần chạy pilot: `p1_pilot_colab_20261103_1519` và `p1_pilot_colab_20261103_1528`, lưu ở Drive `MyDrive/CS331_colab/` (chưa đưa vào repo). Bản gửi Trí kèm đề xuất cần quyết: [TRIEU_P1_COLAB_T4_20261103.md](../../reports/TRIEU_P1_COLAB_T4_20261103.md).

- **Môi trường (Ô 5):** Python 3.10.22, torch 2.5.1+cu121, transformers 4.44.2, numpy 2.2.6, pillow 10.4.0, Tesla T4.
- **Kiểm A (Ô 8): đạt.** 663 khung, CLIP lệch lớn nhất 3.28e-07.
- **Kiểm B (Ô 10): không khớp tuyệt đối với A2000.** Lượt 1 và B2 chỉ khớp 1/15 (q01_3, 0 khung). Lượt 1: 10/15 cùng số khung, 5 query lệch đúng 1 khung (q01_2, q02_1, q04_1, q04_2, q05_2); query cùng số khung lệch điểm tối đa 0.023. Số lệch khung vài trăm pixel là do một khung ra, một khung vào làm xô thứ tự so (hàm `compare` so theo thứ tự). Trên A2000, các lần chạy B2 ngày 15/10 khớp B0 tuyệt đối 15/15, nên lệch là do **đổi GPU**, không phải do cài sai. Nguyên nhân cụ thể chưa kiểm; giả thuyết: A2000 (Ampere) mặc định cho cuDNN dùng TF32, T4 không có TF32.
- **Kiểm C (Ô 11): đạt.** Lần 2 khớp lần 1 tuyệt đối ở cả 6 cách (B2, tau 0.20–0.28), mỗi cách 15/15. T4 tự lặp lại được.
- **Mẫu B2 T4 so với A2000:** trùng 14/15 query. q04_3 khác đúng 1 mẫu (đề xuất 3 thay vì 4), B2 đổi 84 → 61 (GT 39). q02_2 cùng 3 mẫu nhưng B2 30 so với 31 (lượt 2 lệch số lẻ). MAE B2 pilot trên T4 là 20.40, trên A2000 là 22.00; toàn bộ chênh lệch đến từ 2 query này.

**Hệ quả:** chỉ so B0/B2/P **trong cùng một lần chạy T4** (runner đã chạy lại B2 bằng `--replay-b2`); không trộn số T4 với số A2000 trong một bảng. Đề xuất (chờ nhóm chốt): dùng Colab T4 làm máy chạy chuẩn, thay tiêu chí "Kiểm B 15/15" bằng Kiểm A + Kiểm C 15/15, còn Kiểm B chỉ ghi lại mức lệch so với A2000. Số MAE theo tau của pilot này chỉ để dò lỗi, chưa dùng chọn `tau_pseudo`.

## Cách chính: Colab trên trình duyệt

1. Mở notebook:
   - Sau khi file đã lên GitHub: https://colab.research.google.com/github/minhtridaoo/CS331/blob/main/experiments/countgdpp/colab_p1_verified_pseudo.ipynb
   - Hoặc trên Colab: **File > Upload notebook**, chọn file `.ipynb` trong máy.
2. **Runtime > Change runtime type** → chọn **T4 GPU** → Save. T4 khoảng 2 compute unit/giờ, A100 khoảng 11–13 (quỹ 200 unit/tháng); CountGD++ chỉ cần vài GB VRAM nên T4 đủ. Kết quả cũ trong repo chạy trên RTX A2000 (WSL), nên trên T4 Kiểm B lệch nhỏ (xem mục kết quả 03/11); đề xuất dùng Colab T4 làm máy chạy chuẩn, chờ Trí đồng ý.
3. Chạy từng ô (Shift+Enter) từ Ô 1 đến Ô 10. Ô 11 (Kiểm C) chỉ chạy khi trên Drive đã có một lần chạy T4 trước để đối chiếu. Ô 2 sẽ hỏi quyền Google Drive: chọn tài khoản của bạn, cho phép.
4. Ô 4 tạo môi trường riêng `/content/venv310` (Python 3.10, torch 2.5.1+cu121, giống máy Trí), vì Colab mặc định là Python 3.13 không cài được torch 2.5.1. Colab cũng có sẵn CUDA 13 + gcc 13, nên **lần đầu** Ô 4 tải bộ CUDA 12.1 chính thức của NVIDIA (~4 GB) vào `/content/cuda-12.1`, build CUDA ops bằng gcc-12 cho T4/A100/L4 và lưu file build vào `MyDrive/CS331_colab/wheels`; các phiên sau cài thẳng từ file đó. Không cần Restart session. Nếu lỡ restart thì chạy lại từ Ô 5.
5. Gửi lại phần in ra của **Ô 5**, **Ô 8**, **Ô 10** (và **Ô 11** nếu chạy).
6. Xong việc: **Runtime > Disconnect and delete runtime** để khỏi tốn compute unit.

Kết quả và checkpoint được lưu ở Drive `MyDrive/CS331_colab/`. Lần sau Ô 7 lấy checkpoint từ Drive, không tải lại.

## Tham khảo: chạy cùng notebook từ VS Code

Code vẫn chạy trên máy chủ Colab; VS Code chỉ là giao diện. Tên nút có thể khác chút theo phiên bản extension.

1. Trong VS Code, mở **Extensions** (Ctrl+Shift+X), cài **Jupyter** (Microsoft) và **Google Colab** (Google).
2. Mở `experiments/countgdpp/colab_p1_verified_pseudo.ipynb`.
3. Bấm **Select Kernel** (góc trên bên phải notebook) → **Colab** → tạo server mới (New Colab Server) → đăng nhập Google → chọn loại GPU **T4**.
4. Chạy từng ô như trên. "Restart session" ở VS Code là nút **Restart** trên thanh công cụ của notebook.
5. Lưu ý:
   - File (`/content/...`) nằm trên máy chủ Colab, **không** nằm trong máy bạn.
   - Nếu Ô 2 (mount Drive) báo lỗi trong VS Code: đổi `USE_DRIVE = False`. Khi đó kết quả nằm ở `/content/CS331_colab_out` trên máy chủ và mất khi tắt server, nên chạy lại bằng Colab trình duyệt nếu cần giữ kết quả.
   - Xong việc thì tắt server Colab (lệnh Colab trong Command Palette, Ctrl+Shift+P, gõ "Colab") để khỏi tốn compute unit.

## Quy tắc

- 5 ảnh pilot = dò lỗi/kiểm cài đặt. `tau_pseudo`, `M` chính thức chọn trên **tập dev 30 ảnh** sau khi nhóm khóa danh sách (kế hoạch Trí §3.2, §5). Không chỉnh trên `p4_unseen_v1`.
- Trên GPU khác A2000, **Kiểm C** chưa đạt 15/15 ở mọi cách thì chưa dùng số P1 để kết luận. Tiêu chí chính thức chờ nhóm chốt (xem mục kết quả 03/11).
- Model không đọc GT; GT chỉ dùng ở Ô 10 để tính MAE.
