# WORKLOG CS331 — nhật ký chung

**Cập nhật 24/10/2026.** Ghi mỗi buổi tại đây; xem trạng thái tổng thể ở [ROADMAP](roadmap/ROADMAP.md). [Trang bắt đầu](README.md) · [Handoff](HANDOFF/HANDOFF.md).

**Điểm tiếp tục:** phần kiểm chéo kỹ thuật đã được assistant làm hộ ngày 24/10 theo yêu cầu Triệu; [kết quả đọc nhanh](reports/TRIEU_KET_QUA_KIEM_CHEO_20261024.md). Triệu đã xác nhận đọc/hiểu và đồng ý dùng kết quả kiểm được ủy quyền; nhóm chưa duyệt báo cáo. Phần 2 đã chạy; đã có [bản hỗ trợ Triệu kiểm chéo ngày 21/10](reports/TRIEU_EVALUATOR_CROSSCHECK_20261021.md), chưa ghi xác nhận thay Triệu. Nhóm vẫn cần duyệt báo cáo. Repo đã có artifact score/khảo sát P4, khác trạng thái “chưa chạy” trong tài liệu ngày 20/10; cần Trí đồng bộ log và kiểm riêng P4. [Việc cụ thể](roadmap/PHAN_3_TONG_KET.md).

## Cách dùng nhật ký

Mỗi buổi thêm một mục mới ngay trên mục ngày gần nhất. Không xóa kết luận cũ; ghi mục đính chính có ngày nếu cần. Khi hoàn thành một mốc, cập nhật dòng trạng thái trong ROADMAP và bước tiếp trong HANDOFF; không chép toàn bộ nhật ký sang đó.

```text
## YYYY-MM-DD — tên việc
Người thực hiện:
Việc/lệnh đã thực sự chạy:
Input/cấu hình hoặc run ID:
Output/bằng chứng (đường dẫn):
Kiểm tra và kết quả:
Lỗi/điểm chưa rõ:
Trạng thái: Chưa làm / Đang làm / Chờ kiểm / Đã xác nhận
Bước tiếp theo + người làm:
```

## 24/10/2026 — Triệu xác nhận đã đọc và chấp nhận bản kiểm được ủy quyền

**Người xác nhận:** Triệu, trực tiếp trong cuộc trò chuyện ngày 24/10/2026.

> Tôi đã đọc và hiểu bản kiểm ngày 24/10, đồng ý dùng kết quả kiểm kỹ thuật do assistant thực hiện.

**Phạm vi được xác nhận:** đọc/hiểu và đồng ý dùng [bản kiểm kỹ thuật ngày 24/10](reports/TRIEU_KET_QUA_KIEM_CHEO_20261024.md). Người thực hiện đối chiếu kỹ thuật vẫn là assistant; không nâng thành Triệu đã tự audit code hoặc dữ liệu nguồn. [Bản ghi xác nhận](reports/audits/TRIEU_ACCEPTANCE_20261024.json).

**Đã cập nhật:** PILOT_SUMMARY mục 1/3/7, ROADMAP, HANDOFF chung/cá nhân và phần tiếp tục của bản kiểm. Giữ nguyên bản audit kỹ thuật trước xác nhận và nhật ký cũ như lịch sử.

**Trạng thái:** Triệu đã chấp nhận kết quả kiểm được ủy quyền. Nhóm chưa duyệt toàn báo cáo, chưa quyết định đóng pilot hoặc chọn phương pháp P4.

**Bước tiếp theo:** Triệu cùng Trí duyệt PILOT_SUMMARY; Trí đồng bộ log/cấu hình với artifact P4 đã có. Lượt này chỉ cập nhật tài liệu, không chạy evaluator/model, không gửi tin nhắn, commit hoặc push GitHub.

## 24/10/2026 — làm hộ phần kiểm chéo kỹ thuật khi Triệu ưu tiên deadline paper

**Người thực hiện:** assistant theo yêu cầu trực tiếp của Triệu. Không ghi Triệu đã tự đọc/xác nhận hoặc nhóm đã duyệt.

**Việc thực sự chạy:** PowerShell đối chiếu các file pilot đã lưu, tính độc lập sai số 15 query, so kết quả evaluator và nhãn q05_2; đọc logic xử lý error/null/uncertain/absent. Không import/chạy evaluator/self-test/model/CLIP/train, không tạo run inference hoặc metric nghiên cứu mới.

**Nguồn:** checkout commit `31278dd`; 7 hash checkout nguồn không đổi so với 21/10. Hash đối chiếu run: 3 byte thô khớp, 4 khác CRLF/LF nhưng nội dung khớp.

**Kết quả:** 15/15 ID và per_query khớp, paired=15, error=uncertain=absent=0. MAE B0=291/15=19.4, B2=330/15=22; RMSE=sqrt(8869/15) và sqrt(13582/15), exact=1 mỗi nhánh; tốt/kém/giữ=6/4/5. q05_2 khớp 14 box/5 target box/4 vật/1 dư/9 sai loại. Bốn ca minh họa và nhánh null đã kiểm; không gọi đọc code nhánh giả định là test động.

**Bằng chứng:** [báo cáo đọc nhanh](reports/TRIEU_KET_QUA_KIEM_CHEO_20261024.md), [audit JSON](reports/audits/TRIEU_EVALUATOR_20261024.json), [trace đủ 15 dòng](reports/audits/PER_QUERY_TRACE_20261024.csv).

**Trạng thái:** phần kỹ thuật được ủy quyền đã hoàn thành bởi assistant; xác nhận cá nhân Triệu/duyệt nhóm vẫn chưa có. Triệu có thể ưu tiên deadline paper, khi quay lại đọc bản kết quả thay vì tự tạo lại toàn bộ audit. Trí có thể chuẩn bị/đồng bộ log P4 song song; chưa xác nhận P4 hiệu quả. Chưa commit/push hoặc gửi tin nhắn cho Trí.

## 21/10/2026 — hỗ trợ Triệu kiểm chéo evaluator theo worklog

**Người thực hiện phần đối chiếu:** assistant theo yêu cầu Triệu đọc repo và làm theo worklog. Nguồn repo tại commit `31278dd`; đây không phải chữ ký xác nhận người kiểm của Triệu hoặc duyệt của nhóm.

**Đã kiểm:** đọc `indexed` → `validate_prediction` → `evaluate` → `manual_check`; đối chiếu 15 cặp image_id/query_id giữa input, manifest, B0/B2, per_query và metric đã lưu. Manifest có 30 dòng, input chọn 15, B2 ghép 6+9. Kết quả khớp: B0 MAE 19.4/RMSE 24.315975544210986; B2 22.0/30.090973175799196; exact 1 mỗi bên; thay đổi 6 tốt hơn/4 kém hơn/5 giữ nguyên; absent 0 và metric absent null. q05_2 đủ 14 index/tọa độ, gồm 5 box mục tiêu trên 4 vật + 9 sai loại, 1 box dư do trùng. Bốn file kết quả `_r2` giống run chính.

**Hash trên checkout Windows:** 3/7 nguồn khớp byte thô, 4/7 khớp sau đối chiếu CRLF→LF, không còn khác biệt nội dung chưa giải thích. Không ghi là 7/7 khớp byte thô của checkout này; giữ hash cả hai dạng trong [audit JSON](reports/audits/TRIEU_EVALUATOR_20261021.json). Không sửa nguồn để ép hash.

**Artifact bổ sung:** đã đưa bản chi tiết q02_1, ba JSON và chín ảnh bằng chứng từ kết quả ngày 19/10 của cuộc trò chuyện Triệu vào `workspace Trí and Triệu/Triệu/`. Hash bản sao khớp nguồn. Giữ mức chắc chắn vừa cho các nhóm mép đĩa sát nhau; không nâng thành nhãn bbox được Triệu xác nhận toàn bộ. Không thay review gốc hoặc raw prediction.

**Điểm tài liệu mới:** repo có `p4_clip_all15_20261020/run_config.json` và score, `p4_count_cv_20261020/report.json`, cùng review hai case P4. Vì vậy các câu “chưa chạy/chưa có CLIP” ở mục ngày 20/10 là trạng thái tài liệu lúc đó, không đại diện đầy đủ artifact đang có. Lượt này chỉ đọc metadata, chưa audit kết quả P4, không tự xác nhận nhóm đã duyệt.

**Phạm vi thực thi:** chỉ đọc/đối chiếu số học các file đã lưu và chuẩn bị tài liệu. Không import/chạy evaluator, không chạy self-test/inference/CLIP/train; PASS self-test vẫn theo Minhtri báo trước đó. Không tạo run metric nghiên cứu mới.

**Trạng thái:** phần hỗ trợ kiểm chéo đã có [hướng dẫn và bằng chứng](reports/TRIEU_EVALUATOR_CROSSCHECK_20261021.md); Triệu cần tự đọc và ghi kết luận ở PILOT_SUMMARY §7. Nhóm duyệt/đóng pilot/P4 còn để riêng. Chưa commit/push các thay đổi của lượt này.

**Bước tiếp theo:** Triệu đọc bốn điểm code và bốn ca minh họa trong bản hỗ trợ, xác nhận hiểu error/null/uncertain/absent và q05_2; sau đó điền tên/ngày/kết luận. Trí đồng bộ log P4 với artifact đã có; cả nhóm duyệt báo cáo. Không yêu cầu review lại 15 ảnh hoặc chạy model để làm bước này.

## 20/10/2026 — xác nhận Phần 2 đã chạy, Phần 3 chờ duyệt, chuẩn bị P4

**Nguồn mới:** Minhtri gửi `C:/Users/ADMIN/Downloads/HANDOFF_CS331_P2_P3_2026-10-20.md`. Bản gốc đã lưu nguyên trạng trong [ZIP snapshot](<quá khứ/2026-10-20_truoc_xac_nhan_P2_P3.zip>), thư mục `incoming/`. Handoff là ghi nhận cuộc trao đổi khác; trạng thái hiện tại được kiểm lại trên file workspace.

**Người chạy:** Minhtri. Lệnh thực tế theo handoff: `python3 evaluation/evaluate_pilot.py --self-test` (người chạy báo PASS, không có stdout riêng), sau đó `python3 evaluation/evaluate_pilot.py --out results/countgdpp/pilot_eval_20261020`. Dùng Python 3 hệ thống trong Ubuntu vì lệnh python/activate trong distro đang mở không có; evaluator chỉ dùng thư viện chuẩn, không cần khôi phục/cài lại môi trường model để làm phần này.

**Bằng chứng kiểm trực tiếp:** cả `pilot_eval_20261020` và `pilot_eval_20261020_r2` có đủ 5 file. Bốn file kết quả ở hai run giống hệt, metadata cùng 7 hash nguồn, chỉ command khác output. Assistant đọc code và đối chiếu độc lập 15 dòng với input/manifest/prediction gốc, kiểm MAE/RMSE/exact/error_change và q05_2; không import/chạy lại evaluator hay inference. Run đầu là nguồn chính, _r2 là lịch sử chấm lại cùng dự đoán, không tính thành mẫu độc lập.

**Kết quả:** 15 query/5 ảnh, B0/B2 đều 15 hợp lệ, 0 error/uncertain, paired=15. B0 MAE=19.4, RMSE=24.315975544210986; B2 MAE=22.0, RMSE=30.090973175799196; exact=1 mỗi bên; cải thiện/kém đi/giữ nguyên=6/4/5. Absent=0 và metric absent=null. Manual q05_2: 14 khung, 5 khung mục tiêu, 4 vật mục tiêu phân biệt, 1 dư, 9 sai loại. Khớp nguồn lịch sử, không phải kết quả inference mới.

**Phần 3:** PILOT_SUMMARY đã có thông tin run và mục 6 CLIP, mới hơn trạng thái chưa xác nhận mục 6 trong handoff gửi kèm. Giữ trạng thái CHỜ KIỂM CHÉO VÀ DUYỆT; bổ sung phạm vi audit, nguồn xác nhận self-test và phiếu xác nhận nhóm tại mục 7. Không tự ghi Triệu đã kiểm evaluator hoặc nhóm đã đồng ý CLIP.

**Rà kế hoạch P4:** kiểm tài liệu gốc CLIP (Radford et al., ICML 2021); phù hợp làm cơ sở ảnh–văn bản, chưa chứng minh hiệu quả lọc crop B2 trên CS331. Đề xuất bản tối thiểu chỉ crop+query, không chọn negative labels bằng GT test. Giữ B2 và đối chứng confidence; đo giữ vật đúng/loại khung sai cùng MAE. Chốt checkpoint/crop/prompt/ngưỡng trên dev, nhãn và phân công trước thực thi; không coi ứng viên là đóng góp mới đã chứng minh.

**Đồng bộ:** README, ROADMAP V4.6, HANDOFF chung/cá nhân, hướng dẫn Phần 2–3 và hai pipeline. Bản trước sửa và handoff gửi vào được lưu ZIP có manifest; code, dữ liệu và output run giữ nguyên. Các trạng thái “chưa chạy” trong mục nhật ký phía dưới là lịch sử trước khi nhận handoff mới này.

**Kiểm sau cập nhật:** 14 tài liệu Markdown hiện hành, 149 liên kết local hợp lệ; 18 artifact nguồn/output/code/review giữ nguyên hash; handoff gửi vào và các mục WORKLOG trước đó được bảo toàn. Không chạy thêm self-test, evaluator hoặc model.

**Việc tiếp theo:** Triệu kiểm evaluator theo Phần 2 mục 3 rồi ghi tên/ngày/kết luận ở PILOT_SUMMARY §7; Trí đọc và chuẩn bị bốn lựa chọn P4 §6C; cả nhóm duyệt báo cáo và quyết định đóng pilot để chuẩn bị P4. Chưa thực thi CLIP, E3, train hoặc holdout. Assistant vẫn hỏi trước nếu chạy evaluator/model/thực nghiệm thay người dùng.

## 20/10/2026 — kiểm benchmark đã chạy và làm rõ workspace

**Trí cung cấp:** gói `workspace Trí and Triệu/Trí/countgdpp_paper_results`. Run `full_20261015T080230Z` ghi ngày 15/10 trong log; ngày 20/10 là ngày tiếp nhận/kiểm tại workspace, không đổi ngày chạy gốc.

**Assistant đã làm:** đọc log/config/artifact, đối chiếu 1.190 tên ảnh duy nhất với annotation, kiểm GT đếm theo point labels và tính kiểm tra số học từ log. MAE **8.336974789915967**, RMSE **24.63762579961829** khớp metrics.json và tổng cuối log. Không thiếu/thừa/trùng ảnh. Cấu hình có text + synthetic + 3 pseudo + adaptive crop; ngưỡng .23. [Báo cáo đầy đủ](reports/BENCHMARK_FSCD147.md).

**Đối chiếu review mới:** file gốc Triệu hiện ghi “ĐÃ CHỐT v1 — 19/10”, đủ 15/15 query. Guitar và q04_2 đã giải quyết, không còn là đầu việc phải review lại. Handoff cũ 14/15 được sửa theo bản nguồn hiện hành. q04_2 final = 24 blueberry + 7 blackberry + 1 red currant = 32. Review q02_1 dẫn tới Q02_1_DETAILED_REVIEW.md nhưng artifact này chưa có local; giữ giới hạn nếu dùng chi tiết ghép box. SHA256 bản review đọc ngày 20/10: `ab5c4980daae03766f0b43477a4dac72d46de7e605b149a8f0244bad912dfe69`.

**Giới hạn đã ghi:** chỉ xác nhận count metrics, chưa xác nhận AP/AP50. Root run_config còn trạng thái lúc chuẩn bị; trạng thái hoàn tất ở run_config trong full_*. Info báo working tree chưa commit, gói chưa lưu diff; không tuyên bố tái lập chính xác mọi file/môi trường. Không gọi chênh lệch nhỏ với paper là phương pháp cải tiến.

**Tài liệu đã tổ chức:** README thành trang bắt đầu (giải thích pilot/benchmark, bốn chặng, bản đồ thư mục); ROADMAP V4.5 là bảng tiến độ; HANDOFF/owner handoffs/pipelines đồng bộ. Hướng dẫn phần 2–3 và bản nháp pilot nói rõ phạm vi. “Quá khứ” có index giải thích; 14 tài liệu trước sửa được lưu ZIP có hash, không chuyển code/data/checkpoint. Lịch sử cũ trong WORKLOG giữ bên dưới và thu gọn khi xem Markdown.

**Chưa thực hiện:** self-test/evaluator pilot mới, inference mới, train, cải tiến hoặc holdout. Không có output pilot_eval trong kết quả local khi kiểm. Việc đọc/tính kiểm tra artifact benchmark đã được yêu cầu; chưa tự chạy script phần 2 thay người dùng.

**Kiểm tài liệu sau sửa:** 14 file Markdown hiện hành, 141 liên kết local hợp lệ; 30 artifact được kiểm hash giữ nguyên; 6 code cell notebook không đổi; lịch sử WORKLOG giữ nguyên. Liên kết tới file chi tiết q02_1 còn thiếu nằm trong review nguồn đã được ghi rõ, không tự tạo bằng chứng thay thế.

**Trạng thái:** benchmark chạy đủ và count metrics đã xác nhận; phần 2 đã chuẩn bị; phần 3 còn nháp.

**Bước tiếp theo:** Trí chạy `python evaluation/evaluate_pilot.py --self-test`; PASS mới chạy `python evaluation/evaluate_pilot.py --out results/countgdpp/pilot_eval_20261020`. Triệu kiểm code/ID/evaluator; review định tính đã chốt 15/15. Cả hai điền báo cáo phần 3. Theo yêu cầu ngày 19/10, assistant muốn chạy evaluator/thực nghiệm thay phải hỏi trước.

## 19/10/2026 — sắp xếp tài liệu và chuẩn bị phần 2–3

Theo yêu cầu người dùng, tạo README ở gốc, work log chính này, roadmap hiện hành, hướng dẫn phần 2/phần 3, evaluator Python có chú thích và bản nháp tổng kết. Đưa 40 tài liệu/bản trước chỉnh sửa vào “quá khứ/2026-10-19”, lưu manifest nguồn/đích/SHA256; giữ các artifact model/data tại chỗ. Các liên kết local được cập nhật theo vị trí mới.

Evaluator mới chỉ được kiểm cú pháp; **chưa chạy self-test hoặc đánh giá dữ liệu**, không tạo metric mới. Bản tổng kết dùng số liệu đã có đến 16/10, không tự ghi phần 2–3 hoàn thành. Người dùng tự chạy 2B/2C rồi điền phần 3; assistant muốn thực thi đánh giá/thực nghiệm thay phải hỏi trước theo yêu cầu ngày 19/10. Chuẩn bị code/tài liệu không phải chạy thí nghiệm.

Bước ngay tiếp: mở roadmap/PHAN_2_DANH_GIA.md, đọc luồng code, chạy --self-test; khi PASS mới đánh giá thật. Đừng sửa raw predictions để khớp số mong đợi. Nhánh Kaggle vẫn được giữ riêng.

<details>
<summary>Lịch sử trước 19/10 — bấm mở khi cần tra, không dùng làm trạng thái hiện tại</summary>

## Lịch sử trước khi tổ chức lại ngày 19/10

Các mục dưới đây giữ nội dung lịch sử; trạng thái cũ không thay thế bảng hiện hành ở đầu file. Liên kết đã được chỉnh theo cấu trúc thư mục mới.

# CS331 — Nhật ký công việc

**Cập nhật: 15/10/2026 (Asia/Bangkok).**
[Handoff hiện hành](HANDOFF/HANDOFF.md) · [Pipeline phân công](roadmap/PIPELINE_PHAN_CONG.md) · [Pipeline thực nghiệm](roadmap/PIPELINE_COUNTGDPP.md)

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

Snapshot môi trường: [environment_countgdpp.txt](environment_countgdpp.txt).

## Run đầu tiên — spoon, 13/10/2026

- Người dùng thực thi process_folder.py và gửi log hoàn tất; đã kiểm tra file đầu ra trực tiếp.
- Ảnh: [utensils.jpg](experiments/countgdpp/smoke_inputs/images/utensils.jpg), lấy từ ảnh demo trong checkout upstream. Đây là smoke test kỹ thuật, không phải pilot/holdout độc lập.
- Prompt: [spoon.json](experiments/countgdpp/smoke_inputs/spoon.json); positive text spoon, exemplar boxes rỗng, negative rỗng; ảnh exemplar trỏ chính ảnh đầu vào.
- Cấu hình: B0 một lượt qua script gốc; conf_thresh=0.23; có lưu overlay. Chưa chạy B2.
- [Kết quả gốc](results/countgdpp/smoke_spoon/results.json): count=19, 19 boxes, 19 scores.
- [Overlay](results/countgdpp/smoke_spoon/utensils.jpg): quan sát thấy lấy cả nĩa và khung trùng trên một muỗng.
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

Đã kiểm: mỗi JSON đúng một ảnh, count bằng số boxes/scores; giá trị hữu hạn, tọa độ có thứ tự, score trong [0,1]; prompt đúng spoon/fork/cat, exemplar boxes và negative rỗng; có đủ overlay. [Báo cáo kiểm chứng và hash output/prompt](results/countgdpp/smoke_verification_2026-10-13.json).

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

</details>

## 20/10/2026 — Phần 2: Đánh giá pilot

- Self-test: PASS (python3).
- Evaluator: evaluation/evaluate_pilot.py
- Output: results/countgdpp/pilot_eval_20261020/
- Số ảnh: 5
- Số query: 15
- B0: MAE=19.4, RMSE=24.315975544210986, exact_count=1
- B2: MAE=22.0, RMSE=30.090973175799196, exact_count=1
- Coverage: B0=15/15, B2=15/15
- Errors=0, uncertain=0
- Improved=6, worsened=4, unchanged=5
- Absent queries=0 (absent metrics=null)
- Manual q05_2: final_boxes=14, target_boxes=5, distinct_target_objects=4, extra_target_boxes=1, wrong_class_boxes=9
- Ket luan: So lieu khop bang tham chieu.
- Trang thai: Cho Trieu kiem tra cheo code/schema va q05_2.
