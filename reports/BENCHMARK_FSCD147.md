# CountGD++ — kết quả benchmark FSCD-147 đã kiểm

**Kiểm tại workspace: 20/10/2026.** Người thực hiện run: Trí. Run: `full_20261015T080230Z`; log ghi ngày chạy 15/10. Lượt kiểm ngày 20/10 chỉ đọc artifact, đối chiếu ID/GT/cấu hình và tính kiểm tra số học từ log; không chạy lại inference.

[Trang bắt đầu](../README.md) · [Roadmap](../roadmap/ROADMAP.md) · [Hướng dẫn tái chạy nếu cần](../roadmap/KAGGLE_PAPER_EVAL.md).

## Kết quả có thể báo cáo

| Nội dung | Kết quả |
|---|---:|
| Tập | FSCD-147 test |
| Ảnh đã chạy / dự kiến | **1.190 / 1.190** |
| ID/tên ảnh thiếu, thừa, trùng | **0 / 0 / 0** |
| MAE | **8.336974789915967** |
| RMSE | **24.63762579961829** |
| MAE/RMSE tính từ từng ảnh khớp log và metrics.json | **Có** |
| GT đếm trong log khớp point annotation của 1.190 ảnh | **Có** |

Đọc nhanh: MAE khoảng **8,34 vật/ảnh**, RMSE khoảng **24,64**. Đây là kết quả chạy lại checkpoint tác giả với cấu hình được ghi bên dưới; nhóm chưa thêm phương pháp cải tiến.

Paper v2 Table 1, dòng `Ours(t+p+s)`, ghi MAE **8.39**, RMSE **27.03**. Chênh lệch run này so với dòng đó: MAE **−0.053025**, RMSE **−2.392374**. Đây là đối chiếu tham chiếu; số thấp hơn không chứng minh nhóm đã cải tiến model hoặc tái lập chính xác mọi điều kiện. [Paper gốc](https://arxiv.org/html/2512.23351v2#S6.T1).

## File gốc để mở/show

Gói bạn tải về được giữ nguyên ở [countgdpp_paper_results](<../workspace Trí and Triệu/Trí/countgdpp_paper_results>).

| Cần xem | Artifact |
|---|---|
| Chỉ số tổng | [metrics.json](<../workspace Trí and Triệu/Trí/countgdpp_paper_results/full_20261015T080230Z/metrics.json>) |
| Chạy đủ ảnh, số từng ảnh, tổng cuối log | [console.log](<../workspace Trí and Triệu/Trí/countgdpp_paper_results/full_20261015T080230Z/console.log>) |
| Bảng đã xuất từ notebook | [counts.csv](<../workspace Trí and Triệu/Trí/countgdpp_paper_results/full_20261015T080230Z/counts.csv>) |
| Lệnh và metadata của run hoàn tất | [run_config.json trong full_*](<../workspace Trí and Triệu/Trí/countgdpp_paper_results/full_20261015T080230Z/run_config.json>) |
| Cấu hình thực tế | [config_args_all.json](<../workspace Trí and Triệu/Trí/countgdpp_paper_results/full_20261015T080230Z/config_args_all.json>) |
| Commit/command được chương trình ghi | [info.txt](<../workspace Trí and Triệu/Trí/countgdpp_paper_results/full_20261015T080230Z/info.txt>) |
| GPU / kiểm CUDA ops | [gpu.txt](<../workspace Trí and Triệu/Trí/countgdpp_paper_results/gpu.txt>) · [ops_tests.txt](<../workspace Trí and Triệu/Trí/countgdpp_paper_results/ops_tests.txt>) |

**Lưu ý trạng thái:** `run_config.json` ở gốc gói là bản lúc chuẩn bị, còn ghi `prepared_not_run`. Bản trong `full_20261015T080230Z` ghi `complete_count_metrics_verified`, và được log/metric/coverage xác nhận. Giữ nguyên hai bản để bảo toàn lịch sử; dùng bản trong run khi báo cáo. Tên `detections_test_text_only.json` do lệnh đặt không phản ánh đầy đủ các nhánh bật; xem cấu hình thực tế.

## Cấu hình đã đối chiếu

- Commit ghi trong manifest và info: `8489f836d75eb407ae778c56cff1f72cc6f8baae`.
- `box_threshold=0.23`, `num_pseudo_exemplars=3`, `num_exemplars=0`.
- `use_synth_exemplars=true`, `crop=true`, `no_text=false`, `debug=false`, `seed=42`.
- Cấu hình: **text + synthetic exemplars + pseudo-exemplars + adaptive cropping**, không dùng exemplar thủ công từ ảnh test làm input.
- Checkpoint SHA256 **được metadata ghi nhận**: `b89395d79711c9b9f13f3ef80cd2e528386fb1d70453f99443be4eccab33592f`. Gói kết quả không chứa bản checkpoint Kaggle để hash lại ở lượt kiểm này.
- GPU log: Tesla T4. Vòng test ghi **00:46:22**, khoảng **2.3386 s/iteration**; không bao gồm toàn bộ cài đặt/tải dữ liệu và không thay benchmark thời gian/VRAM được thiết kế riêng.
- Log CUDA ops có **6/6 kiểm tra True**. Đây là bằng chứng từ run Kaggle, không phải một lần test mới tại máy local.

## Đã kiểm gì và giới hạn nào còn lại?

1. Parse tên ảnh và `Pred Count / GT Count` từ console.log, cho phép warning xen giữa. Đủ 1.190 tên duy nhất, khớp toàn bộ danh sách trong `countgd_test_fscd147.json`; không có ảnh bị thay thế/trùng tên.
2. Tính MAE/RMSE từ số từng ảnh; khớp cả dòng tổng cuối log và metrics.json. Không dùng số bbox trong detections JSON thay count sau adaptive cropping.
3. Hash annotation local khớp metadata run. GT count khớp point annotation; mỗi ảnh còn có 3 annotation khung mẫu mà loader tách riêng tại [datasets/coco.py](../CountGDPlusPlus/datasets/coco.py). Không cộng các khung mẫu vào count GT; nhãn box trong `instances_test.json` phục vụ detection và không được dùng thay nhãn điểm để đếm.
4. JSON detections đọc được, chứa 1.190 ảnh và 83.881 annotations; số annotation này không phải metric đếm trung bình.
5. **Chưa xác nhận AP/AP50 theo evaluator detection của paper.** Không dùng số `test_coco_eval_bbox` ở log.txt để tuyên bố tái lập AP/AP50; nhánh notebook này được chốt ở count metrics.
6. `info.txt` báo working tree có thay đổi chưa commit; gói không lưu diff đầy đủ. Commit nền/cấu hình đã được ghi, nhưng chưa thể chứng thực mọi file chạy giống nguyên trạng repo. Không cần rerun ngay để hoàn tất phần 2–3 pilot; lưu giới hạn này khi báo cáo tái lập. Lần chạy sau nên xuất thêm git diff/status.

SHA256 đã đối chiếu với metadata: `countgd_test_fscd147.json` = `e301c6933396b98040ff9b7d86e18d66c14cc8c2118ce0e4cae24f4f5807c35c`; `instances_test.json` = `f17e99d481c3a1f1dfa9e42d7d1dc0a96bb76498eda9d5440efb033d7763f5d2`.

Dấu vết artifact kiểm ngày 20/10:

| File trong run | SHA256 |
|---|---|
| console.log | `af91506be1048b51e7b93b452e9eead4a3a98f574d016a3485d37ebdf27d4a47` |
| metrics.json | `22dbcfdaf2f264d3b04f7720b345a91b730cac138f5e6eab6159cefaabd127b8` |
| run_config.json | `1f33e3b2105ccfd7632dbc6a6524f17a3224202ef8d03371e7a209e4d56588d2` |

## Liên hệ với câu hỏi đồ án

Benchmark cho nhóm một mốc kết quả trên tập chuẩn và bằng chứng triển khai chạy được. Câu hỏi thầy yêu cầu — **cùng ảnh đổi X/Y thì phải đếm đúng loại** — vẫn cần bộ thử nhiều loại và phép đo phù hợp. Nhánh [pilot](PILOT_SUMMARY.md) cung cấp những ví dụ đó; MAE 19.4/22.0 của pilot không được so trực tiếp với 8.336975 trên FSCD-147.

Bước ngay tiếp là [phần 2](../roadmap/PHAN_2_DANH_GIA.md) và [phần 3](../roadmap/PHAN_3_TONG_KET.md), rồi chốt giả thuyết cải tiến. Kết quả benchmark này là của nhóm đã nộp trong thư mục Trí, không phải ảnh chụp điểm nhóm khác từng trao đổi trước đây.
