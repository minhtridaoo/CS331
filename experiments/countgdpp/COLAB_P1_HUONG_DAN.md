# Chạy nhánh P1 trên Colab (03/11/2026)

**File:** [colab_p1_verified_pseudo.ipynb](colab_p1_verified_pseudo.ipynb) gọi [run_b2_verified_pseudo.py](run_b2_verified_pseudo.py) + [pseudo_clip_verifier.py](pseudo_clip_verifier.py). Runner B2 cũ (`run_b2_frozen.py`, `run_b2_pilot.py`) giữ nguyên.

**P1 làm gì:** lượt 1 (= B0) → tối đa `M=10` ứng viên điểm > 0.23 → CLIP (`a photo of {prompt}`, cùng model/revision/crop với P4) chấm từng ứng viên → giữ ứng viên có cosine ≥ `tau_pseudo`, lấy tối đa 3 theo điểm CountGD → lượt 2. Không còn mẫu nào thì trả B0. Nhiều `tau` dùng chung một lượt 1. Kèm `--replay-b2` để chạy lại B2 gốc từ cùng lượt 1 và so với B2 đã lưu (kiểm tái hiện trên GPU mới).

**Đã kiểm trước khi chạy GPU (CPU, raw đã lưu):** cách chọn ứng viên trùng `select_pseudo` và trùng mẫu B2 đã lưu ở 45/45 query (pilot 15 + p4_unseen_v1 30). Ô tóm tắt chạy đúng trên dữ liệu giả lập (MAE B2 pilot = 22.00). Chưa chạy model.

## Cách chính: Colab trên trình duyệt

1. Mở notebook:
   - Sau khi file đã lên GitHub: https://colab.research.google.com/github/minhtridaoo/CS331/blob/main/experiments/countgdpp/colab_p1_verified_pseudo.ipynb
   - Hoặc trên Colab: **File > Upload notebook**, chọn file `.ipynb` trong máy.
2. **Runtime > Change runtime type** → chọn **A100 GPU** → Save.
3. Chạy từng ô (Shift+Enter) từ Ô 1 đến Ô 4. Ô 2 sẽ hỏi quyền Google Drive: chọn tài khoản của bạn, cho phép.
4. Ô 4 cài xong sẽ nhắc: **Runtime > Restart session**. Làm theo, rồi chạy tiếp **từ Ô 5** (không chạy lại Ô 1–4).
5. Chạy Ô 5 → Ô 10. Gửi lại phần in ra của **Ô 8** và **Ô 10**.
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
