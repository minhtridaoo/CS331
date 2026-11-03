# Chạy nhánh P1 trên Colab (03/11/2026)

**File:** [colab_p1_verified_pseudo.ipynb](colab_p1_verified_pseudo.ipynb) gọi [run_b2_verified_pseudo.py](run_b2_verified_pseudo.py) + [pseudo_clip_verifier.py](pseudo_clip_verifier.py). Runner B2 cũ (`run_b2_frozen.py`, `run_b2_pilot.py`) giữ nguyên.

**P1 làm gì:** lượt 1 (= B0) → tối đa `M=10` ứng viên điểm > 0.23 → CLIP (`a photo of {prompt}`, cùng model/revision/crop với P4) chấm từng ứng viên → giữ ứng viên có cosine ≥ `tau_pseudo`, lấy tối đa 3 theo điểm CountGD → lượt 2. Không còn mẫu nào thì trả B0. Nhiều `tau` dùng chung một lượt 1. Kèm `--replay-b2` để chạy lại B2 gốc từ cùng lượt 1 và so với B2 đã lưu (kiểm tái hiện trên GPU mới).

**Mã băm nguồn:** audit 14/10 tính trên bản checkout Windows (CRLF); clone trên Colab là LF. Runner P1 đưa xuống dòng về CRLF trước khi băm (`source_sha`), nên vẫn bắt được mọi thay đổi code. `run_b2_frozen.py` cũ chưa có bước này nên sẽ báo "Stock source changed" nếu chạy trên Colab.

**Đã kiểm trước khi chạy GPU (CPU, raw đã lưu):** cách chọn ứng viên trùng `select_pseudo` và trùng mẫu B2 đã lưu ở 45/45 query (pilot 15 + p4_unseen_v1 30). Ô tóm tắt chạy đúng trên dữ liệu giả lập (MAE B2 pilot = 22.00). Chưa chạy model.

## Cách chính: Colab trên trình duyệt

1. Mở notebook:
   - Sau khi file đã lên GitHub: https://colab.research.google.com/github/minhtridaoo/CS331/blob/main/experiments/countgdpp/colab_p1_verified_pseudo.ipynb
   - Hoặc trên Colab: **File > Upload notebook**, chọn file `.ipynb` trong máy.
2. **Runtime > Change runtime type** → chọn **T4 GPU** → Save. T4 khoảng 2 compute unit/giờ, A100 khoảng 11–13 (quỹ 200 unit/tháng); CountGD++ chỉ cần vài GB VRAM nên T4 đủ. Máy chạy chuẩn của nhóm từ 03/11 là Colab T4; kết quả cũ trong repo chạy trên RTX A2000 (WSL), nên Kiểm B có thể lệch rất nhỏ ở số lẻ.
3. Chạy từng ô (Shift+Enter) từ Ô 1 đến Ô 10. Ô 2 sẽ hỏi quyền Google Drive: chọn tài khoản của bạn, cho phép.
4. Ô 4 tạo môi trường riêng `/content/venv310` (Python 3.10, torch 2.5.1+cu121, giống máy Trí), vì Colab mặc định là Python 3.13 không cài được torch 2.5.1. Colab cũng có sẵn CUDA 13 + gcc 13, nên **lần đầu** Ô 4 tải bộ CUDA 12.1 chính thức của NVIDIA (~4 GB) vào `/content/cuda-12.1`, build CUDA ops bằng gcc-12 cho T4/A100/L4 và lưu file build vào `MyDrive/CS331_colab/wheels`; các phiên sau cài thẳng từ file đó. Không cần Restart session. Nếu lỡ restart thì chạy lại từ Ô 5.
5. Gửi lại phần in ra của **Ô 5**, **Ô 8** và **Ô 10**.
6. Xong việc: **Runtime > Disconnect and delete runtime** để khỏi tốn compute unit.

Kết quả và checkpoint được lưu ở Drive `MyDrive/CS331_colab/`. Lần sau Ô 7 lấy checkpoint từ Drive, không tải lại.

## Tham khảo: chạy cùng notebook từ VS Code

Code vẫn chạy trên máy chủ Colab; VS Code chỉ là giao diện. Tên nút có thể khác chút theo phiên bản extension.

1. Trong VS Code, mở **Extensions** (Ctrl+Shift+X), cài **Jupyter** (Microsoft) và **Google Colab** (Google).
2. Mở `experiments/countgdpp/colab_p1_verified_pseudo.ipynb`.
3. Bấm **Select Kernel** (góc trên bên phải notebook) → **Colab** → tạo server mới (New Colab Server) → đăng nhập Google → chọn loại GPU **A100**.
4. Chạy từng ô như trên. "Restart session" ở VS Code là nút **Restart** trên thanh công cụ của notebook.
5. Lưu ý:
   - File (`/content/...`) nằm trên máy chủ Colab, **không** nằm trong máy bạn.
   - Nếu Ô 2 (mount Drive) báo lỗi trong VS Code: đổi `USE_DRIVE = False`. Khi đó kết quả nằm ở `/content/CS331_colab_out` trên máy chủ và mất khi tắt server, nên chạy lại bằng Colab trình duyệt nếu cần giữ kết quả.
   - Xong việc thì tắt server Colab (lệnh Colab trong Command Palette, Ctrl+Shift+P, gõ "Colab") để khỏi tốn compute unit.

## Quy tắc

- 5 ảnh pilot = dò lỗi/kiểm cài đặt. `tau_pseudo`, `M` chính thức chọn trên **tập dev 30 ảnh** sau khi nhóm khóa danh sách (kế hoạch Trí §3.2, §5). Không chỉnh trên `p4_unseen_v1`.
- **Kiểm B** chưa đạt 15/15 thì chưa dùng số P1 để kết luận.
- Model không đọc GT; GT chỉ dùng ở Ô 10 để tính MAE.
