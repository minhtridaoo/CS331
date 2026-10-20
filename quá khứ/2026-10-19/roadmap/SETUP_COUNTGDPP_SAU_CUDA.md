# CountGD++ — Tiếp tục sau khi cài CUDA

**Cập nhật 13/10/2026. Dành cho người phụ trách mô hình.**
[Handoff của bạn](../HANDOFF/HANDOFF_MODEL.md) · [Pipeline phân công](PIPELINE_PHAN_CONG.md)

## 0. Trạng thái đã kiểm chứng

Đã có Ubuntu-22.04 trong WSL, /root/.venvs/countgdpp dùng Python 3.10.12, PyTorch 2.5.1+cu121, torchvision 0.20.1+cu121, GPU nhận được, GCC 11, nvcc 12.1.105. Repo nằm tại D:/MINHTRIHOCCODE/HOCKI5/CS331/CountGDPlusPlus.

**Cập nhật sau smoke:** đã có phụ thuộc/extension import được, BERT/checkpoint và output spoon thật. Các phần cài đặt dưới đây giữ để tái lập, không cần chạy lại. Đã chạy đủ spoon/fork/cat; điểm tiếp tục là audit tải trọng số/lọc và chuẩn hóa bàn giao theo [work log](../HANDOFF/WORKLOG_CS331.md). Chưa xác nhận đầy đủ bộ test CUDA ops hoặc hoàn thành pilot.

Repo không khóa toàn bộ phiên bản thư viện. Các pin bên dưới là cấu hình khởi đầu đề xuất của nhóm, chưa phải môi trường đã tái hiện thành công paper. Giữ log; nếu gặp xung đột/import lỗi thì xử lý tại chặng đó và ghi thay đổi, không tự nâng torch qua yêu cầu torch<2.6.

## 1. Mở đúng Ubuntu và cài thư viện — lưu để tái lập

Trong **PowerShell**, chỉ chạy dòng này trước:

~~~powershell
wsl -d Ubuntu-22.04
~~~

Sau khi terminal đã vào Ubuntu, chạy các khối **bash** bên dưới. Đợi từng khối hoàn thành; lỗi ở đâu thì dừng ở đó.

~~~bash
source /root/.venvs/countgdpp/bin/activate
cd /mnt/d/MINHTRIHOCCODE/HOCKI5/CS331/CountGDPlusPlus
python -c "import sys; print(sys.executable)"
~~~

Đường dẫn phải là /root/.venvs/countgdpp/bin/python. Nếu thấy đường dẫn Windows/Python 3.14, chưa chạy pip.

~~~bash
export CUDA_HOME=/usr/local/cuda-12.1
export PATH="$CUDA_HOME/bin:$PATH"
export CC=/usr/bin/gcc-11
export CXX=/usr/bin/g++-11
export MAX_JOBS=2
nvcc --version
~~~

Các biến export chỉ có hiệu lực trong terminal hiện tại; mở lại Ubuntu thì chạy lại khối này. MAX_JOBS giới hạn số tiến trình biên dịch để giảm áp lực RAM.

~~~bash
sudo apt-get install -y python3-dev libgl1 libglib2.0-0
python -m pip install "setuptools<81" wheel ninja
python -m pip install -r requirements.txt "torch==2.5.1+cu121" "torchvision==0.20.1+cu121" "transformers==4.44.2" "setuptools<81" matplotlib gdown
~~~

Giữ cặp torch/torchvision đã chạy được. Pin Transformers 4.44.2 là lựa chọn khởi đầu cho code BERT hiện tại, tránh tự chuyển sang major mới; chưa xác nhận mọi luồng CountGD++ tương thích cho đến khi import/load model thực tế. Setuptools cũng được giới hạn cho luồng build setup.py của repo. Không sửa requirements.txt gốc chỉ để làm mất lỗi; lưu khác biệt cấu hình của nhóm.

Kiểm tra:

~~~bash
python -m pip check
python -c "import torch, torchvision, transformers, timm, cv2, matplotlib, gradio; from transformers import BertModel; print('Imports OK'); print(torch.__version__, torchvision.__version__, transformers.__version__); print('GPU:', torch.cuda.is_available())"
~~~

**Đạt §1:** pip check không báo xung đột, import thành công, GPU True. Chưa đạt thì chưa build tiếp.

## 2. Biên dịch phần mở rộng CUDA

Vẫn cùng terminal Ubuntu và môi trường ở §1:

~~~bash
cd /mnt/d/MINHTRIHOCCODE/HOCKI5/CS331/CountGDPlusPlus/models/GroundingDINO/ops
python setup.py build install
python test.py
~~~

Ở snapshot đang dùng, test.py có hai kiểm tra forward và bốn kiểm tra gradient; mong đợi sáu kết quả True. Import được chưa thay thế cho việc chạy bài kiểm tra này. Nếu thiếu CUDA_HOME, sai compiler hoặc báo lỗi import .so, giữ traceback và đối chiếu đúng toolkit/torch/compiler đã chọn.

~~~bash
python -c "import torch; import MultiScaleDeformableAttention; print('CUDA extension import OK')"
~~~

**Đạt §2:** build thành công, sáu kiểm tra đạt, import thành công.

## 3. Cài Detectron2 và lưu môi trường

~~~bash
cd /mnt/d/MINHTRIHOCCODE/HOCKI5/CS331/CountGDPlusPlus
python -m pip install --no-build-isolation "git+https://github.com/facebookresearch/detectron2.git"
python -c "import torch; import detectron2; from detectron2 import _C; print('Detectron2 extension import OK')"
python -m pip check
python -m pip freeze > ../environment_countgdpp.txt
~~~

Đây là cách cài từ source theo README; nhánh remote có thể thay đổi. Lưu commit Detectron2 thực được cài (pip freeze/direct_url metadata) trước khi tái chạy hoặc đưa sang máy khác. Nếu thay torch/CUDA về sau, cần kiểm tra lại những extension đã build; không tiếp tục dùng bản biên dịch cũ một cách mặc định.

**Đạt §3:** import extension thành công, không có xung đột pip; đã lưu phiên bản thực dùng. Chưa tuyên bố model chạy được ở bước này.

## 4. Chuẩn bị trọng số

Chỉ làm sau khi §1–3 đạt:

~~~bash
cd /mnt/d/MINHTRIHOCCODE/HOCKI5/CS331/CountGDPlusPlus
mkdir -p checkpoints
python download_bert.py
gdown 1j6N22TtKu2NVcKpgfrf-sJHGeLDqs9hs -O checkpoints/countgd_plusplus.pth
sha256sum checkpoints/countgd_plusplus.pth
~~~

Nếu file đã có từ lần chạy trước, kiểm tra nguồn/hash và khả năng tải hoàn chỉnh trước khi quyết định tải lại, tránh ghi đè tùy ý. Link trọng số lấy từ README tác giả; nhóm chưa có hash chuẩn tác giả để khẳng định chỉ riêng hash tự tính đã chứng minh file đúng.

Cần có checkpoints/bert-base-uncased và checkpoints/countgd_plusplus.pth. Tải thành công chưa bằng nạp model thành công. Khi nạp, ghi các missing/unexpected keys quan trọng và cấu hình; không bỏ qua vì code gốc dùng strict=False.

**Đạt §4:** có tài nguyên đúng nguồn và log hash; xác minh nạp ở bước tiếp theo.

## 5. Chạy B0 một ảnh và bàn giao đầu tiên

Nhận từ Triệu một ảnh với X/Y/lớp vắng mặt đã kiểm nhãn. Mục tiêu là ba dự đoán độc lập, giữ resize/precision/ngưỡng và ảnh giống nhau.

- Mốc source: process_folder.py có đường chạy một lượt và xuất count/boxes/scores.
- Script dùng JSON prompts riêng, không trực tiếp đọc schema nhóm. Viết adapter hoặc chuyển đổi dữ liệu; đừng đưa manifest chứa GT vào model.
- Với nhánh B0 qua script gốc, positive.exemplars.image dùng chính ảnh đang xét, boxes rỗng; negative rỗng. Chạy thử trước để xác nhận nhánh không exemplar hoạt động.
- Script gốc xử lý khởi tạo ở cấp module; tránh import nguyên file như thư viện. Không ghi đè kết quả giữa ba query.
- Schema nhóm và trách nhiệm chuyển đổi nằm trong pipeline phân công. B2 chưa thuộc lần chạy này.
- Kiểm tra count bằng số khung, tọa độ ảnh gốc, overlay và error status; ghi thời gian/VRAM.
- GPU 4 GB chưa được kiểm chứng đủ cho mô hình. Nếu OOM, ghi đúng cấu hình/lỗi rồi chuyển GPU phù hợp hoặc nghiên cứu một cấu hình bộ nhớ khác có nhãn riêng; không đổi âm thầm protocol.

**Đạt §5:** ba dòng dự đoán thật theo schema v1, metadata và overlay; Triệu ghép được với GT và hai người cùng kiểm tra. Chưa cần chờ đủ 20–30 ảnh.

## 6. Những gì cần ghi lại khi lỗi

Ghi chặng, lệnh, traceback đầy đủ, Python/torch/CUDA/compiler, và thay đổi vừa thực hiện. Nếu có lỗi trong §1–4, chưa chuyển sang đổ lỗi cho checkpoint hay chất lượng model. Không dùng sudo pip hoặc pip Windows để sửa môi trường WSL.

## 7. Nguồn hướng dẫn

- [README CountGD++ tại snapshot của checkout](https://github.com/niki-amini-naieni/CountGDPlusPlus/blob/8489f836d75eb407ae778c56cff1f72cc6f8baae/README.md).
- [Detectron2 — cài đặt và đối chiếu CUDA/PyTorch](https://detectron2.readthedocs.io/en/latest/tutorials/install.html).
- [PyTorch — bộ phiên bản 2.5.1](https://pytorch.org/get-started/previous-versions/#v251).

Đây là hướng dẫn thực hiện tiếp, không phải log xác nhận §1–5 đã đạt. Chỉ cập nhật handoff thành hoàn thành sau khi có đầu ra kiểm tra.
