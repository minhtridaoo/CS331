# M5 — B2: tự chọn mẫu rồi đếm lại

**Trạng thái hiện tại 16/10:** B2 đủ 5 ảnh/15 query, Trí review 15, Triệu review 14 (thiếu guitar). q05_2 final đã có nhãn 14 khung; plates hiệu chỉnh 3/3 đúng loại. MAE B0=19.4, B2=22.0 giữ nguyên. [Đối chiếu và việc tiếp theo](../../../../results/countgdpp/b2_remaining3_20261015/TRIEU_CROSSCHECK_2026-10-16.md). Các mục M5/E2 bên dưới là lịch sử.

**Cập nhật 15/10/2026. Runner đã chạy/review 2 ảnh/6 query MUCCA; kết quả ở b2_two_images_20261015.**

**Cập nhật sau E2:** runner đã có `--tau-sample` (mặc định 0.23), người dùng chạy .10 và .50; `tau_final` giữ .23. E2 pilot đã đóng, .35 không chạy do top-3 sẽ giữ nguyên theo điểm lưu. Trí đã review 6 query bằng mắt; tiếp theo Triệu kiểm chéo/evaluator và Trí mở B2 .23 trên 3 ảnh dev còn lại. [Review E2](../../../../results/countgdpp/m6_e2_sample050_20261015/REVIEW.md) · [Review của Trí](../../../../results/countgdpp/b2_two_images_20261015/USER_VISUAL_REVIEW.md). Phần M5 bên dưới ghi lại cấu hình và quy trình ban đầu; các câu “chưa khảo sát ngưỡng” chỉ áp dụng tại thời điểm M5.

## Bạn đang ở đâu

M0–M2: môi trường/trọng số và audit đã thực hiện. M3: smoke B0 đủ ba query. M4: B0 dev 5 ảnh/15 query đã chạy/review; chẩn đoán token 5 query/2 ảnh không tìm thấy khung sai được giữ chỉ vì CLS/dấu chấm. Hiện sang M5: kiểm tác động pseudo-exemplar. Các phần evaluator/G1, absent queries, nguồn dữ liệu và holdout chưa đầy đủ; M4 chưa phải toàn bộ benchmark.

## Lệnh B2 đã thực hiện trong Ubuntu

~~~bash
source /root/.venvs/countgdpp/bin/activate
cd /mnt/d/MINHTRIHOCCODE/HOCKI5/CS331
python experiments/countgdpp/run_b2_pilot.py --run-id b2_two_images_20261015
~~~

Đọc b2_two_images.jsonl: mcac_100 guitars/amplifiers/chairs và mcac_200 pens/rulers/pencils, tổng 6 query. Chương trình nạp model một lần và chạy tuần tự. Mỗi query có B0 replay trước B2; nếu khác baseline cũ thì dừng và báo lỗi. Không đọc GT vào model. Không ghi đè thư mục run cũ.

## Chính sách đã cố định trước khi xem kết quả pilot

- Lượt đầu giống script app B0; giữ ngưỡng 0.23 và lọc gốc.
- Chọn từ toàn bộ 900 proposals lượt đầu, lấy max điểm các token tên vật, strict score > tau_sample=0.23. Sort giảm dần, tối đa 3 mẫu; không NMS, không lựa bằng GT, không chọn thủ công.
- Quy tắc threshold/top-3/clamp đối chiếu get_pseudo_exemplars trong test_shanghai_tech.py (commit đã pin). Kiểm ca giả với hàm gốc cho cùng kết quả chọn mẫu/tọa độ. App có API khác, nên đây là B2 adapter của nhóm, không gọi là tái hiện toàn pipeline paper.
- Tọa độ mẫu được đổi về xyxy pixel ảnh gốc và clamp trong ảnh; transforms_app resize lại trước khi dùng làm exemplar. Đã kiểm scaling. Degenerate box báo lỗi, không âm thầm đổi quy tắc.
- Lượt hai dùng cùng ảnh + text + mẫu tự chọn, không negative prompt, synthetic hoặc adaptive crop. Giữ tau_final=0.23 và logic lọc app; positive ở lượt hai bao gồm các exemplar token chèn trước dấu chấm. Không thay lọc theo kết quả chẩn đoán trước đó.
- Không có mẫu: trả B0, no_pseudo=true, stage2_executed=false, stage2_count=null. Đây là quy ước adapter; upstream ShanghaiTech gọi lượt hai cả khi mẫu rỗng.
- Seed 42 mỗi query; resize short side 800/max 1333; checkpoint giữ nguyên. Chưa khảo sát ngưỡng hoặc fine-tune.

## Đầu ra cần xem

Trong results/countgdpp/b2_two_images_20261015/:

- predictions.jsonl: B0/stage1, mẫu tự chọn, stage2, final, scores/boxes và metadata.
- run_config.json: cấu hình, hash nguồn/model/adapter/input, chính sách mẫu và giới hạn.
- Mỗi query: stage1.jpg, pseudo.jpg (khung xanh), final.jpg; stage1_raw.npz và stage2_raw.npz nếu thực sự chạy lượt hai. Raw giữ toàn bộ proposals để phân tích lọc cuối về sau.
- elapsed_ms đo hai predict + chọn mẫu, có capture, không gồm load model/vẽ/lưu/check replay, không warm-up. peak_vram_mib là PyTorch allocated gồm model cư trú, không phải tổng VRAM card. Không so thẳng với thời gian subprocess B0 cũ.
- Lỗi là execution_status=error, final_count=null; dừng ở lỗi đầu tiên. Query chưa chạy không được tính là 0.

Khi chạy xong, so B0/B2 và **xem mẫu chọn đúng loại hay không**. Count giảm chưa chứng minh chọn đúng loại. Không điều chỉnh mẫu bằng đáp án sau khi xem kết quả.

## Kiểm chứng đã thực hiện

check_b2_selection.py kiểm parity top-3/clamp với hàm upstream, ngưỡng strict, không mẫu và scaling tọa độ. Đã chạy GPU b2_smoke_20261015 trên ảnh utensils với spoon/fork/cat:

| Query | B0 | Số mẫu | B2 cuối | Nhánh |
|---|---:|---:|---:|---|
| spoon | 19 | 3 | 19 | Hai lượt |
| fork | 14 | 3 | 18 | Hai lượt |
| cat | 0 | 0 | 0 | Trả B0, không lượt hai |

Cả ba lượt đầu khớp baseline count/boxes/scores, schema/tọa độ mẫu/overlay đạt. Đã xem ảnh: spoon chọn cả ba mẫu là nĩa; fork chọn mẫu nĩa nhưng kết quả vẫn lấy muỗng. Đây là quan sát trên ảnh kiểm kỹ thuật, không phải kết luận hiệu quả B2 hay cơ chế nhân quả. [Ảnh kiểm kỹ thuật](../../../../results/countgdpp/b2_smoke_20261015/smoke_comparison.jpg).

## Sau 6 query

Lập bảng cùng ảnh/query giữa B0 và B2, kiểm mẫu đúng/sai và khung cuối. Sau đó mới quyết định mở B2 cho cả 5 ảnh, khảo sát ngưỡng M6 hoặc thử một can thiệp có căn cứ. Triệu kiểm nhãn/mẫu/khung, evaluator và bổ sung absent. Chưa tuyên bố có phương pháp mới hoặc hoàn thành đồ án.


**Kết quả mới nhất:** [review M5](../../../../results/countgdpp/b2_two_images_20261015/REVIEW.md). Đã có đủ 6 query, chưa cần chạy lại. Tiếp theo M6 khảo sát ngưỡng cuối với mẫu cố định; không so MAE tập 6 query trực tiếp với MAE tập 15 query.
