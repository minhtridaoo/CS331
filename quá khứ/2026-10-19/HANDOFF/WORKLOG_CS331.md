# CS331 — Nhật ký công việc

**Cập nhật: 15/10/2026 (Asia/Bangkok).**
[Handoff hiện hành](HANDOFF.md) · [Pipeline phân công](../roadmap/PIPELINE_PHAN_CONG.md) · [Pipeline thực nghiệm](../roadmap/PIPELINE_COUNTGDPP.md)

## Quy tắc lưu tiến độ

Theo yêu cầu của người dùng: sau mỗi mốc có bằng chứng, nối thêm mục vào nhật ký này và đồng bộ handoff, pipeline, bước tiếp theo. Giữ lịch sử; không đổi kế hoạch thành kết quả đã thực hiện. Phân biệt log người dùng gửi, file kiểm tra trực tiếp và giả thuyết. Không tự ghi Triệu đã hoàn thành hoặc đã được gửi file. Quy tắc áp dụng khi làm việc trong cuộc trò chuyện; không phải tác vụ theo dõi nền.

## Các mốc đến ngày 13/10/2026

Các mốc dưới đây được tổng hợp từ cuộc trò chuyện và kiểm tra workspace; không có giờ thực hiện đầy đủ nên không gán giờ giả.

| Mốc | Đã thực hiện và bằng chứng | Phần còn lại |
|---|---|---|
| Chốt phạm vi | CountGD++ là baseline; cùng ảnh hỏi X/Y và lớp vắng mặt; bạn làm model, Triệu làm dữ liệu/evaluator | Chưa chọn can thiệp hoặc train |
| M0 — môi trường | Clone commit 8489f836d75eb407ae778c56cff1f72cc6f8baae; WSL Ubuntu-22.04, Python 3.10.12, torch 2.5.1+cu121, torchvision 0.20.1+cu121, GCC 11, nvcc 12.1.105 | Lỗi cài torch ban đầu đã vượt qua khi dùng đúng môi trường WSL |
| M1 — thư viện | transformers 4.44.2; GPU True; MultiScaleDeformableAttention và detectron2._C import được sau import torch; inference thật đã chạy | Chưa lưu/đối chiếu log đầy đủ của bộ test CUDA ops; import và inference không thay thế mọi test |
| M2 — trọng số | BERT local có config/tokenizer/model.safetensors; CountGD++ checkpoint 1,250,122,586 byte; script nạp và chạy ra output | Chưa ghi SHA256 vào metadata; chưa kiểm missing/unexpected keys của strict=False |
| M3 — một ảnh | Đã chuẩn bị utensils.jpg và ba prompt spoon/fork/cat; đã có một kết quả thật spoon | Còn fork/cat, chuẩn hóa schema v1 và metadata trước bàn giao |

Snapshot môi trường: [environment_countgdpp.txt](../../../environment_countgdpp.txt).

## Run đầu tiên — spoon, 13/10/2026

- Người dùng thực thi process_folder.py và gửi log hoàn tất; đã kiểm tra file đầu ra trực tiếp.
- Ảnh: [utensils.jpg](../../../experiments/countgdpp/smoke_inputs/images/utensils.jpg), lấy từ ảnh demo trong checkout upstream. Đây là smoke test kỹ thuật, không phải pilot/holdout độc lập.
- Prompt: [spoon.json](../../../experiments/countgdpp/smoke_inputs/spoon.json); positive text spoon, exemplar boxes rỗng, negative rỗng; ảnh exemplar trỏ chính ảnh đầu vào.
- Cấu hình: B0 một lượt qua script gốc; conf_thresh=0.23; có lưu overlay. Chưa chạy B2.
- [Kết quả gốc](../../../results/countgdpp/smoke_spoon/results.json): count=19, 19 boxes, 19 scores.
- [Overlay](../../../results/countgdpp/smoke_spoon/utensils.jpg): quan sát thấy lấy cả nĩa và khung trùng trên một muỗng.
- Đếm thủ công ảnh: 7 muỗng, 7 nĩa, 0 mèo. Đây là nhãn kiểm bằng mắt, chưa phải manifest đã được hai người kiểm chéo.
- Log TRAIN/FutureWarning không làm dừng run và không tự chứng minh cần fine-tune.
- RTX A2000 Laptop 4 GB chạy được cấu hình smoke này. Chưa đo peak VRAM/thời gian; không suy rộng sang toàn bộ B2/benchmark.
- Chưa xác định nguyên nhân lỗi: cần giữ cấu hình, chạy hai prompt còn lại, kiểm prompt, tải trọng số và logic lọc trước khi kết luận lỗi mô hình.

## Hướng dẫn tại mốc spoon — đã thực hiện ở cập nhật bên dưới

Chạy trong Ubuntu WSL, lần lượt từng lệnh; nếu crash thì lưu log, không ghi count=0.

~~~bash
source /root/.venvs/countgdpp/bin/activate
cd /mnt/d/MINHTRIHOCCODE/HOCKI5/CS331/CountGDPlusPlus
python process_folder.py --input_folder ../experiments/countgdpp/smoke_inputs/images --prompts ../experiments/countgdpp/smoke_inputs/fork.json --output_folder ../results/countgdpp/smoke_fork --conf_thresh 0.23 --vis_output
python process_folder.py --input_folder ../experiments/countgdpp/smoke_inputs/images --prompts ../experiments/countgdpp/smoke_inputs/cat.json --output_folder ../results/countgdpp/smoke_cat --conf_thresh 0.23 --vis_output
~~~

Giữ ảnh, checkpoint, ngưỡng và tiền xử lý; chỉ đổi prompt và thư mục kết quả. Mục tiêu tham chiếu thủ công: fork=7, cat=0. Không đoán dự đoán trước khi chạy.

Sau hai run: so cả count và vị trí; kiểm đường tải checkpoint/prompt/lọc; chuyển kết quả gốc sang predictions.jsonl + run_config.json theo schema v1. Thời gian/VRAM của run cũ chưa đo phải để null kèm lý do; muốn có số đo thì chạy lại với bộ đo được ghi rõ. Chưa chuyển sang pilot hoặc chỉnh ngưỡng chỉ vì script đã chạy xong.

Triệu tiếp tục T1–T4 trên CPU: 5 ảnh/15 query, manifest tách GT, evaluator và fixture giả. Chưa xác nhận nhánh này đã có sản phẩm. Bạn chưa xong toàn bộ phần việc; mốc gần nhất là hoàn thành bộ bàn giao M3 rồi ghép G1.


## Cập nhật sau fork/cat — 13/10/2026, trạng thái mới nhất

Người dùng báo chạy xong; đã đọc trực tiếp ba results.json và xem overlay fork/cat. Không dùng số liệu từ demo tương tác mô phỏng.

| Query | GT thủ công | Dự đoán | Quan sát |
|---|---:|---:|---|
| spoon | 7 | 19 | Lần kiểm trước thấy khung nhầm nĩa và khung trùng |
| fork | 7 | 14 | Overlay khoanh cả 7 nĩa và 7 muỗng |
| cat | 0 | 0 | Không có khung, đúng trên ảnh này |

Đã kiểm: mỗi JSON đúng một ảnh, count bằng số boxes/scores; giá trị hữu hạn, tọa độ có thứ tự, score trong [0,1]; prompt đúng spoon/fork/cat, exemplar boxes và negative rỗng; có đủ overlay. [Báo cáo kiểm chứng và hash output/prompt](../../../results/countgdpp/smoke_verification_2026-10-13.json).

Kết luận đúng mức: hoàn thành inference smoke 3/3 query. Mô hình không trả cùng kết quả cho mọi query; truy vấn cat đúng nhưng fork vẫn lấy nhầm muỗng. Một ảnh chưa đủ kết luận đã giải quyết lớp vắng mặt hoặc xác định nguyên nhân lỗi X/Y; muỗng/nĩa cũng là hai loại đồ dùng có hình dạng tương tự nên cần pilot có hai loại khác hẳn nhau theo yêu cầu thầy.

**Bước tiếp theo:** giữ nguyên các output; audit missing/unexpected keys khi nạp checkpoint và logic lọc điểm; chuẩn hóa predictions.jsonl/run_config.json để ghép evaluator. Hash checkpoint, thời gian và peak VRAM chưa hoàn tất; không bịa số cho run cũ. Chưa đổi ngưỡng, train hoặc mở B2. M3/P0 và G1 chưa đóng chỉ vì đã có đủ ba JSON. Triệu tiếp tục T1–T4; chưa xác nhận tiến độ của Triệu.


## 14/10/2026 — tiếp nhận dữ liệu Triệu, chuẩn bị M4

- Người dùng chỉ đường dẫn workspace Trí and Triệu/Triệu/MUCCA_10_queries/MUCCA_10_queries. Đã kiểm trực tiếp 10 ảnh và 30 query/GT, IDs duy nhất, mapping khớp, số điểm theo class bằng toàn bộ GT, không có tọa độ điểm ngoài ảnh. Đã xem ảnh tổng quan; chưa đếm tay mọi ảnh.
- Tất cả query có đối tượng (GT>0); chưa có absent query. Không tính FPR_absent hoặc tuyên bố đủ protocol X/Y/absent. Cần thêm absent đã xác minh và nguồn dữ liệu; giữ nhóm gần nhau/khác hẳn nhau để phân tích riêng.
- Đã xuất input schema v1 không GT và manifest evaluator riêng trong experiments/countgdpp/m4_inputs/. Chọn batch 5 ảnh đầu theo thứ tự nguồn trước khi xem dự đoán; ảnh đầu mcac_100. Đây là dev nội bộ, không phải holdout.
- Audit checkpoint: 1108 state keys của app; missing=0, nạp shape thành công, 38 unexpected chỉ thuộc feature_map_encoder. Lần audit thô dừng để review; đối chiếu groundingdino.py dòng 110/325 và groundingdino_app.py cho thấy khối dư không dùng trong đường app, nên ghi quyết định tương thích B0 đã pin. Không sửa code upstream và không quy lỗi đếm cho checkpoint. Hash local b89395d79711c9b9f13f3ef80cd2e528386fb1d70453f99443be4eccab33592f.
- Tạo run_b0_batch.py gọi script gốc từng query, ngưỡng 0.23, xuất predictions.jsonl/run_config/overlay/log; đo elapsed toàn tiến trình, peak VRAM chưa đo. Kiểm input hợp lệ; từ chối trùng ID, GT leakage và count không khớp boxes.
- Chạy thật adapter_check_cat_20261014 trên ảnh utensils cũ: thành công, count=0 giống gốc. Đây là kiểm adapter, không phải MUCCA. Chưa chuẩn hóa đủ cả ba output cũ hoặc xác nhận ghép evaluator/G1.
- Đã tạo handoff mới ngày 14/10 và hướng dẫn M4. **Chưa chạy 30 query MUCCA.** Người dùng chạy tiếp ảnh đầu 3 query, kiểm output rồi mở 5 ảnh sau khi nối evaluator. Không train, chỉnh ngưỡng hoặc mở B2.


## 14/10/2026 — M4 ảnh đầu đã hoàn tất

Người dùng chạy m4_first_image_b0 và gửi log 3/3 ok. Đã kiểm trực tiếp run_config status=complete, failed_queries=0; ba dòng dự đoán có IDs khớp manifest, count/boxes/scores khớp và đủ overlay. Guitars 25/GT25, amplifiers 44/GT11, chairs 0/GT1. Đã xem cả ba overlay: truy vấn amplifiers vẫn khoanh nhiều guitar; chairs bỏ sót ghế/stool phía dưới trái theo nhãn nguồn. Đúng số guitar chưa đồng nghĩa đã chấm vị trí chính xác tuyệt đối.

Đã lưu REVIEW.md và initial_review.json cùng run, gồm hash manifest/predictions để truy vết. Không sửa output gốc. Đây là review độc lập ba dòng, chưa xác nhận Triệu có evaluator hoặc hoàn tất G1. Tiếp theo thu thập 5 ảnh/15 query ở ngưỡng 0.23, cho phép chạy dữ liệu song song với hoàn thiện evaluator; chưa dùng để chốt hướng cải tiến hay chỉnh ngưỡng. Ảnh đầu nằm trong batch 5, không tính lặp là mẫu độc lập. Đồng bộ handoff/pipeline/hướng dẫn.


## 14/10/2026 — hoàn tất và kiểm batch M4 5 ảnh / 15 query

Người dùng chạy m4_first5_b0 và gửi 15 count. Đã kiểm trực tiếp run_config complete, 15/15 dự đoán hợp lệ, IDs đúng, count/boxes/scores và tọa độ/score hữu hạn; đủ overlay. Ghép với manifest: GT lần lượt 25,11,1; 15,3,2; 6,6,6; 6,24,39; 2,4,3. Dự đoán 25,44,0; 28,31,23; 17,18,17; 60,43,84; 20,11,21.

Review sơ bộ: 1 đúng count, 13 thừa, 1 thiếu; MAE=19.4, RMSE≈24.316, coverage=1.0; presence recall=14/15 không chứng minh chọn đúng loại. Không có absent nên các chỉ số absent=null. Không gộp ảnh chạy lặp với run đầu như mẫu độc lập. Chưa phải đánh giá toàn benchmark hoặc xác nhận evaluator của Triệu.

Đã xem cả 15 overlay: ampli lấy guitar; bowls/cups lấy nhiều đĩa; pens/rulers/pencils đều khoanh gần hết ba nhóm; hai ảnh trái cây lấy cả loại khác. Lưu REVIEW.md, review_per_query.csv, review_metrics.json (kèm hash GT/predictions), hai bảng ảnh và stationery_query_comparison.jpg trong run. Giữ nguyên predictions/config gốc.

Thay bước chạy thêm ảnh ngay bằng chẩn đoán có mục tiêu trên mcac_200 và mcac_100: kiểm điểm từng token và lọc gốc, đặc biệt token tên vật so với token đặc biệt/dấu chấm. Đây là giả thuyết điều tra, chưa chứng minh nguyên nhân và chưa sửa baseline. Triệu kiểm nhãn/khung và nối evaluator, bổ sung absent. Chưa B2/train hoặc chốt cải tiến. Đã đồng bộ handoff/pipeline.


## 15/10/2026 — chẩn đoán điểm token rulers, giữ nguyên B0

Người dùng yêu cầu next move sau baseline → lỗi → nguyên nhân → cải tiến → kiểm chứng. Đã tạo diagnose_tokens.py, chỉ nạp import/định nghĩa hàm của process_folder.py đã pin và thêm observer trả nguyên kết quả lọc. Script kiểm hash model/checkpoint, không đọc GT vào model, lưu raw sigmoid scores/boxes/input_ids, token CSV, ảnh proposal IDs và so lại count/boxes/scores với baseline.

Kiểm ca giả phân biệt điểm từ nội dung, dấu chấm, rejected bởi negative-side và dưới ngưỡng đạt. Chạy GPU token_diagnostic_rulers_20261015/q03_2: count=18, counterfactual chỉ token nội dung=18, khớp count/boxes (atol 0.001 pixel)/scores (1e-5) với B0. Cả 18 top-positive token là rulers. Không có khung nào bị loại chỉ nhờ bỏ CLS/dấu chấm. Điều này bác bỏ giả thuyết dấu chấm là nguyên nhân cho query này, chưa khái quát các query khác.

Đã xem proposal_ids và gán nhãn hậu kiểm: thước IDs 0,1,2,3,4,13; bút mực 5,6,7,8,11,44; bút chì 9,10,12,14,15,16. Điểm rulers: thước 0.4252–0.4906, bút mực 0.4232–0.4445, bút chì 0.3540–0.3776. Cần Triệu kiểm chéo; không dùng nhãn này làm model input. Không có một ngưỡng trên điểm này vừa giữ đủ 6 thước vừa bỏ hết bút trong ca này; chưa chọn ngưỡng hoặc kết luận ngưỡng vô ích trên dataset.

Predict có capture, chưa warm-up: 1736.6 ms; peak PyTorch allocated 1461.12 MiB gồm model, không phải tổng device VRAM. Không so với thời gian subprocess batch cũ hoặc ghi hồi tố cho run cũ.

Đã lưu REVIEW.md và manual_box_review.csv cùng run, tạo handoff 15/10 và đồng bộ tài liệu. Bốn query pens/pencils/guitars/amplifiers chưa chạy chẩn đoán; người dùng chạy tiếp theo lệnh trong review. Chưa B2/train/chỉnh lọc hoặc chọn module cải tiến.


## 15/10/2026 — hoàn tất bốn query chẩn đoán bổ sung

Người dùng chạy token_diagnostic_more_20261015, cung cấp log pens=17, pencils=17, guitars=25, amplifiers=44; replay_matches=True. Đã kiểm run_config complete và summary. Đã đọc raw_scores.npz của cả bốn query và rulers ở run trước, tự tính lại masks theo max positive/remaining và max token tên vật. Cả 5 query/2 ảnh có tập proposal giữ nguyên, tổng 121 retained proposals; không chỉ count bằng nhau. Pencils tách pencil + ##s; top token của 17 khung là pencil. Các query còn lại top token đúng tên vật. Không có khung được giữ chỉ vì CLS/dấu chấm ở các ca này.

Kết luận giới hạn: cách tổng hợp điểm token đặc biệt không giải thích lỗi đã kiểm; chưa thử caption không có dấu chấm và chưa biết nguyên nhân learned score gán cao cho lớp khác. Autocast FutureWarning không làm hỏng run. Không sửa baseline/env hoặc chạy lại chỉ vì cảnh báo.

Lưu REVIEW.md và combined_review.json trong run bổ sung. Bước tiếp theo chuyển sang chuẩn bị đối chứng B0/B2 trên cùng mcac_200/mcac_100 (ba query mỗi ảnh), trước tiên kiểm code/chính sách chọn pseudo-exemplar. Chưa triển khai/chạy B2, chưa coi là phương pháp cải tiến mới/full paper và chưa train. Nhãn/evaluator/absent/holdout phía Triệu còn cần kiểm. Đã đồng bộ handoff/pipeline.


## 15/10/2026 — bắt đầu M5, chuẩn bị B2 và kiểm kỹ thuật

Người dùng yêu cầu bước tiếp và vị trí pipeline. M4 có baseline 5 ảnh/15 query và chẩn đoán token; chuyển M5 đối chứng pseudo-exemplar. Đọc test_shanghai_tech.py:get_pseudo_exemplars: max token target, score>threshold, sort top tối đa 3, clamp xyxy. Đọc app/transforms xác nhận exemplar nhận pixel theo ảnh resize; adapter chọn trong ảnh gốc rồi transform lại. Không chỉnh code upstream.

Tạo run_b2_pilot.py, check_b2_selection.py, b2_two_images.jsonl (6 query không GT) và b2_smoke_inputs.jsonl (spoon/fork/cat). B2 chọn toàn bộ proposals lượt đầu bằng tau_sample .23, top3, không NMS; giữ final filter app và tau_final .23. Không synthetic/crop/negative labels. Nhánh không mẫu trả B0 và stage2=null theo protocol adapter, khác upstream luôn gọi lượt hai. Config ghi rõ khác biệt, raw NPZ lưu đủ 900 proposals mỗi lượt, ảnh pseudo xanh và stage1/final đỏ; errors null và dừng, không ghi đè run.

Kiểm chọn mẫu với hàm gốc trên ca giả, clipping, scaling, strict threshold và empty đạt. GPU smoke b2_smoke_20261015: spoon B0=19/pseudo3/B2=19; fork 14/3/18; cat 0/0/0 no_pseudo=True, không forward2. Cả ba stage1 khớp B0 count/boxes/scores; kiểm JSON/schema/tọa độ/overlay đạt. Đã xem bảng ảnh: spoon chọn 3 mẫu nĩa; fork mẫu nĩa nhưng final vẫn có muỗng. Đây là kiểm kỹ thuật và quan sát, chưa khẳng định nguyên nhân hay hiệu quả nghiên cứu.

Đã viết README_B2 và đồng bộ handoff/pipeline. Người dùng chạy tiếp b2_two_images_20261015 trên mcac_100/mcac_200. Chưa chạy B2 MUCCA, chưa mở M6/ngưỡng/cải tiến/train. Tài nguyên ghi predict+capture, khác elapsed toàn subprocess cũ; không đánh dấu evaluator/G1/holdout hoàn tất.


## 15/10/2026 — M5 B2 hai ảnh/sáu query đã chạy và review

Người dùng gửi đủ sáu log b2_two_images_20261015. Đã kiểm file config complete, IDs/GT, count/boxes/scores, khung mẫu trong ảnh, stage1_matches_B0=True cả sáu. Kết quả B0→B2: guitars25→25, amplifiers44→38, chairs0→0, pens17→13, rulers18→18, pencils17→16. Chairs không mẫu nên fallback, không forward2; năm query còn lại tự chọn 3 mẫu và chạy lượt hai.

Đã xem bảng ghép stage1/pseudo/final trên cả hai ảnh. Nhận xét bằng mắt: mẫu guitar đúng; mẫu amplifiers đều guitar; pens trộn pen/pencil; mẫu rulers đúng thước nhưng final vẫn đếm cả18; mẫu pencils đều pen. Cần Triệu kiểm chéo, không dùng nhận xét làm đầu vào. Chưa thể quy mọi lỗi cho chọn sai mẫu hoặc tuyên bố nhân quả.

Đối chiếu GT cùng sáu query: MAE B0=11.3333, B2=9.5; 3 ca giảm sai số, 3 không đổi; exact count vẫn 1/6. Không so B2 9.5 với MAE19.4 của15 query khác tập. Lưu REVIEW.md, review_per_query.csv, review_metrics.json/hash và hai bảng ảnh trong run; output model giữ nguyên.

Bước tiếp theo M6: khảo sát ngưỡng cuối trên raw lượt2 đã lưu, giữ mẫu/tau_sample cố định, ghi riêng fallback; đổi mẫu phải chạy lại lượt2. Chưa thực hiện sweep, chưa train/chốt phương pháp mới hoặc B2 cả5 ảnh. Còn evaluator/absent/holdout. Đã đồng bộ handoff/pipeline.


## 15/10/2026 — M6/E1 quét ngưỡng lọc cuối, không chạy lại mô hình

Người dùng yêu cầu tiếp M6. Đã đọc protocol và giữ lưới định trước {.10,.23,.35,.50}; tau_sample=.23/mẫu cố định. Tạo sweep_final_threshold.py và thực thi CPU vào m6_e1_final_20261015. Áp dụng nguyên mask positive max>tau_final và positive max>remaining max cho stage1 B0, stage2 B2; fallback chairs refilter stage1. Không train/forward hoặc thay mẫu. Manifest chỉ dùng để chấm sau lọc, không chọn ngưỡng từng query.

Đã kiểm đủ6IDs/GT và raw hữu hạn, tái lập count/boxes/scores ở.23 cho cảB0/B2, monotonic tập khung qua4ngưỡng, hoàn tất48tổ hợp. B0 MAE lần lượt16.833/11.333/7.833/5.0; B2 14.167/9.5/8.0/6.0. Exactcount vẫn1/6 từ.23 trở lên. B0 .50 có4query trả0, gồm3lớp mới bị bỏ hoàn toàn (amplifiers/rulers/pencils) và chairs đã0; không chốt .50 chỉ vìMAE thấp. Đã xem ảnh sweeps pens/rulers/amplifiers: nhầm loại vẫn có ở cấu hình giữ khung, hoặc mất toàn bộ vật đúng khi lọc cao.

Lưu per_query.csv, summary.csv/json, predictions.jsonl mỗi ngưỡng kèm proposal IDs, sáu ảnh sweep, run_config có hash nguồn/GT/adapter và REVIEW.md. Baseline gốc và B2 nguồn không sửa. Chưa có absent/holdout, chưa xác nhận evaluator củaTriệu. M6/E1 đã xong trên2ảnh; bước tiếp E2 thaytau_sample giữtau_final=.23, chưa chạy. Đã đồng bộ handoff/pipeline.

## 15/10/2026 — đóng E2 pilot và ghi nhận review bằng mắt của Trí

Người dùng tự thêm --tau-sample vào runner và chạy m6_e2_sample010_20261015, m6_e2_sample050_20261015. Đã đọc config/predictions của hai run và B2 nguồn .23: đủ 6 query/run, execution_status=ok, stage1_matches_B0=True; final=.23, max_pseudo=3. .10 giữ nguyên pseudo_boxes/final_boxes so với .23, không chỉ count. .50 giữ mẫu/final của guitar và pens; ampli/thước/bút chì không mẫu nên stage2=false/null và trả B0. Ghế không mẫu ở mọi mức. Counts .50: 25,44,0,13,18,17. Mức .35 bỏ qua sau khi kiểm điểm top-3 đều >.35 ở 5 query có mẫu; đây là suy luận từ selection, chưa chạy inference .35. Đóng E2 pilot không đồng nghĩa đã chạy đầy đủ bốn mức hoặc hoàn tất benchmark/M6 tổng thể.

Trí gửi review cả 6 query của run .23: guitar mẫu 3/3 và final đúng theo mắt; ampli mẫu 0/3 (đều guitar), final vẫn lẫn nhiều loại; ghế không mẫu/khung (GT có 1); pens mẫu 1/3, hai mẫu là pencils, final theo người dùng có 1 ruler và cả pens/pencils; rulers mẫu 3/3 nhưng final vẫn lẫn tất cả; pencils mẫu 0/3 (đều pens), final gần hết các vật. Lưu USER_VISUAL_REVIEW.md riêng trong run B2 nguồn, giữ nguyên nhận xét với nguồn là người dùng; chưa có xác nhận của Triệu hoặc phân loại từng khung. “Khoanh all” không diễn giải thành khung stage1/final giống hệt vì count ampli 44→38, pencils 17→16. Nhận xét này không phải nhãn model input.

Kết luận: cả lỗi chọn mẫu lẫn lỗi final khi mẫu đúng đều xuất hiện; không quy toàn bộ lỗi cho pseudo hoặc tuyên bố nhân quả. Lưu REVIEW.md E2 trong run .50; đồng bộ handoff/roadmap/README. Không chạy thêm model hoặc sửa thuật toán trong lần cập nhật này. Chưa mở E3/train/module mới.

Bước tiếp theo: Triệu kiểm chéo và hoàn thiện evaluator/absent; Trí chuẩn bị mở B2 cấu hình .23 trên 3 ảnh còn lại của bộ dev 5 ảnh đã có B0, chưa chạy. Đây là dev đã xem B0, không phải holdout. Mục đích kiểm tra lỗi có lặp ở ảnh khác trước khi chọn một can thiệp. Người dùng tự thực hiện thí nghiệm; assistant chỉ đường và kiểm kết quả. Không gửi tin nhắn cho Triệu bằng công cụ.


## 15/10/2026 — B2 mở rộng đủ 5 ảnh / 15 query

Người dùng tạo b2_remaining3_inputs.jsonl và tự chạy b2_remaining3_20261015 ở tau_sample=tau_final=.23. Đã kiểm config complete, 9 query đúng IDs và đều ok; 3 mẫu/query, có lượt hai, stage1 khớp B0 count/boxes (<=.001 pixel)/scores (<=1e-5). Ghép hai run được đúng 15 IDs/5 ảnh trong first5; kiểm count bằng số khung/score, tọa độ hợp lệ và giá trị hữu hạn. Cấu hình suy luận/selection/checkpoint khớp; adapter hash khác sau khi thêm CLI tau_sample, không gọi script byte-identical. Không chạy thêm model.

Counts B0→B2 mới: plates 28→31, bowls 31→31, cups 23→26, strawberries 60→59, blueberries 43→32, red currants 84→84, cherries 20→15, raspberries 11→14, blackberries 21→79. Trên cùng 15 query, GT từ manifest gói Triệu: MAE 19.4→22.0; RMSE 24.315976→30.090973; exact count 1/15 cả hai. Sai số giảm 6, tăng 4, giữ nguyên 5. Đây là metric đếm trên dev nhỏ, không chứng minh chọn đúng loại hoặc kết luận chất lượng paper. Không bỏ ca blackberries khỏi tổng hợp.

Assistant xem pseudo/final q05_3: mẫu nhìn là 2 blackberry và 1 raspberry đỏ; final có nhiều khung nhỏ theo phần tròn trên blackberry, nhiều lớp khác và khung chồng nhau. Ghi là quan sát sơ bộ, cần Trí/Triệu kiểm chéo; chưa phân loại từng proposal hoặc chứng minh mẫu sai gây tăng count. Không coi mọi khung thừa đều là trùng hay đều đếm phần vật.

Lưu REVIEW.md và combined_first5_metrics.json (bảng 15 query, metric và hash nguồn) trong run mới; đồng bộ handoff/pipeline/README. Trí review tiếp 9 query mới, ưu tiên q05_3 rồi so cùng ảnh q05_1/q05_2. Triệu kiểm chéo nhãn và evaluator; chưa xác nhận evaluator/absent/holdout đầy đủ. E1/E2 chỉ trên 2 ảnh, không tự mở rộng trạng thái thành 5 ảnh. Chưa E3/train/chốt module; người dùng tiếp tục tự làm thí nghiệm.


## 15/10/2026 — Trí hoàn tất review bằng mắt 15 query

Người dùng báo mẫu đúng ở 9 query mới: plates 0/3, bowls 1/3, cups 2/3, strawberries 2/3, blueberries 2/3, red currants 0/3, cherries 1/3, raspberries 3/3, blackberries 2/3. Người dùng xác nhận q02_3 ghi bowl là gõ nhầm, vẫn khoanh được cups; giữ phần khoanh sai/thừa nhiều. Cherry có 2 quả phù hợp GT gói Triệu. Final blackberries đếm múi thành bbox và khoanh cả các loại quả khác. Lưu USER_VISUAL_REVIEW.md trong run remaining3, không sửa predictions/GT.

Ghép nhận xét cũ: 20/42 mẫu đúng theo người dùng trên 14 query có mẫu; 3 query đúng 3/3 (guitar/thước/raspberries), 4 query sai 0/3, 7 query pha trộn; chairs không có mẫu. Guitar final đúng theo mắt, hai ca thước/raspberries mẫu đúng nhưng final vẫn sai/thừa. Đây là review định tính của Trí, chưa là chấm từng bbox hoặc kiểm chéo của Triệu; không khẳng định mẫu sai là nguyên nhân duy nhất. “Final như stage1” không hiểu là cùng tập khung, vì cherries 20→15 và raspberries 11→14. Metric count toàn tập giữ nguyên MAE 19.4→22.0.

Kết thúc vòng nhận xét chung 5 ảnh, chuyển sang phân loại từng khung. Việc kế tiếp: Trí và Triệu gán nhãn 14 bbox q05_2 raspberries theo loại thật, cả vật/phần vật, ID vật để phát hiện trùng và vật thật bị bỏ sót. Nhãn chỉ để đánh giá, không cung cấp GT cho model. Giữ trọng tâm giảm đếm nhầm loại theo X/Y; phần quả là nhóm lỗi cần đo, chưa mở thành mục tiêu thứ hai. Chưa chọn giải pháp, chạy inference mới, E3, train hoặc thay NMS. E1/E2 vẫn chỉ 2 ảnh. Đã cập nhật handoff/pipeline/README và liên kết review.


## Chuẩn bị benchmark Kaggle — 15/10/2026

Người dùng xác nhận ảnh 1.190 ảnh/MAE 10.20 thuộc nhóm khác và yêu cầu hỗ trợ chạy đánh giá giống paper. Đã tạo roadmap/COUNTGDPP_FSCD147_KAGGLE.ipynb và KAGGLE_PAPER_EVAL.md; cấu hình text+synthetic+pseudo+crop theo README, pin commit hiện có; số tham chiếu paper v2 8.39/27.03. Đã kiểm cú pháp 6 code cell và đọc code upstream. Chưa chạy trên Kaggle, chưa tải assets tại Kaggle, chưa có kết quả benchmark mới. Script phụ test_fscd147.py không có trong checkout; notebook kiểm MAE/RMSE từ engine chính và log từng ảnh, không nhận đã tái lập AP/AP50. Tiếp theo: người dùng import notebook và chạy cell kiểm môi trường; giữ nguyên nhánh pilot, không so trực tiếp metric khác tập.


## 16/10/2026 — nhận kiểm chéo của Triệu, giải thích đủ q05_2

Đọc workspace Trí and Triệu/Triệu/TRIEU_VISUAL_REVIEW.md, hash SHA256 08767b8b77cdd42aeecb7bfa2c573f6b8be94ee959bde382678ed8c07fa8fd0f. Có 14/15 query (thiếu q01_1), GT/B0/final của tất cả 14 khớp bảng kết quả. Giữ nguyên file nguồn và các review gốc của Trí, không xem mọi diễn giải trong nguồn là đã tự kiểm độc lập.

Assistant mở q02_1 pseudo và q05_2 stage1/final, đối chiếu tọa độ prediction. Plates: cả 3 mẫu là đĩa, phù hợp Triệu thay vì Trí cũ 0/3; ảnh nhỏ/che khuất, chưa chấm độ bao trọn chuẩn. Tổng hợp hiệu chỉnh 23/42 mẫu đúng (20/42 theo Trí trước đó), chưa gọi toàn bộ được hai người kiểm chéo vì guitar chưa có Triệu. Ba ca plates/rulers/raspberries mẫu đúng 3/3 nhưng final còn sai/thừa.

q05_2 final: 5 khung raspberry 1/2/3/7/11, 9 khung sai loại (blackberry10/14; blueberry9/12/13; strawberry5/6; cherry4/8). 7 và11 cùng quả,11 chỉ bao phần quả. Tổng14 =4 quả mục tiêu+1khung trùng+9khung sai loại. Khung12/13 là phần blueberry; nhãn lỗi phần vật và sai loại có thể cùng tồn tại. Đã lưu manual_crosscheck_20261016.json gồm 14final/11stage1, overlay1-based và index0-based, tọa độ/hash; không dùng nhãn làm model input. Đây là visual audit, không tuyên bố metric định vị benchmark.

Stage1 q05_2 được assistant giải thích thêm: 2 strawberry ở số6/7, không phải1; 4raspberry+2strawberry+2cherry+3blueberry=11. File nguồn Triệu giữ nguyên; ghi riêng bổ sung. q04_2 còn cần đối sánh32khung với mô tả “toàn bộ” các quả; không suy ra số/loại bỏ sót từ chênh lệch35vs32.

Tạo TRIEU_CROSSCHECK_2026-10-16.md, handoff ngày16, cập nhật index/ngày và pipeline/README; giữ snapshot15 và ưu tiên benchmark Kaggle từ phiên khác. Không chạy thêm model/train, không chọn module. Tiếp theo Triệu bổ sung guitar/q04_2; dùng nhãn q05_2 kiểm evaluator, không yêu cầu làm lại từ đầu. Kaggle notebook mới chuẩn bị; chưa xác nhận run/metric mới và không so trực tiếp với MAE pilot. Không gửi tin nhắn cho Triệu bằng công cụ.
