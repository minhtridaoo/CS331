# P4 — việc Trí có thể làm tiếp khi chờ Triệu

**Cập nhật 27/10/2026.** Bắt đầu buổi 3 giờ và ghi điểm dừng ở [CHECKLIST_3_GIO](CHECKLIST_3_GIO.md). Đây là hướng dẫn tiếp theo; trạng thái chung ở [ROADMAP](ROADMAP.md), kết quả đã kiểm ở [audit P4](../reports/P4_AUDIT_20261022.md). Các ô chưa đánh dấu là việc dự kiến, chưa thực thi.

## 1. Chốt phạm vi trước khi làm

**Câu hỏi:** trên cùng ảnh, thay loại cần đếm có giúp chọn đúng vật thể của loại đó không? Giữ **CountGD++ B2** tạo khung. CLIP chỉ chấm độ phù hợp giữa crop và câu hỏi; không phải chuyển sang model CLIP-Count.

Trí đã đủ phần chạy/chấm/viết để chờ duyệt pilot. P4.1–P4.5c đã có kết quả thăm dò và cấu hình khóa. P4.6 là kiểm chứng tiếp nhánh cải tiến, **không phải yêu cầu bổ sung để được đóng PILOT_SUMMARY**.

Giữ hai ứng viên đã khóa: lọc bằng điểm CountGD++ và Fusion 50/50. Dừng chỉnh prompt/ngưỡng/trọng số trên 5 ảnh cũ. Fusion chưa thắng đối chứng về MAE; nhãn cho lợi ích chọn đúng vật còn chờ kiểm độc lập.

## 2. Việc đầu tiên — P4.6a: chọn dữ liệu kiểm tra mới

**Người làm: Trí. Có thể chuẩn bị ngay, chưa chạy model.**

1. Liệt kê ảnh có thể dùng, nguồn ảnh/nhãn, quyền sử dụng, nhóm ảnh gốc và lịch sử đã dùng. Năm ảnh dev phải loại khỏi tập kiểm tra: `mcac_100`, `mcac_11`, `mcac_200`, `mcac_20`, `mcac_27`.
2. Đối chiếu lịch sử run/review: ảnh còn lại trong gói 10 ảnh **không tự động là holdout**. Ảnh hoặc biến thể/crop đã dùng để chọn phương pháp phải ở dev. Nếu không rõ lịch sử, đánh dấu chưa xác nhận và tìm ảnh khác.
3. Đề xuất phạm vi vừa sức: **10 ảnh gốc mới, mỗi ảnh 2 truy vấn về hai loại khác hẳn nhau cùng có mặt, cộng 1 truy vấn loại chắc chắn vắng mặt**. Tổng 30 truy vấn, trong đó 10 absent. Đây là đề xuất quy mô, chưa phải bộ dữ liệu đã có hoặc đủ để khái quát toàn bài toán. Nếu đổi quy mô, ghi lý do trước khi xem kết quả.
4. Xác minh count/object_id từ annotation hoặc đếm tay. Quy định đơn vị đếm là cả vật, cách xử lý che khuất/khung chứa nhiều vật. Absent phải được kiểm, không suy từ model trả 0. Không chỉ chọn ảnh trông dễ hoặc chỉ giữ lỗi đẹp sau khi chạy.
5. Khóa danh sách trước lần dự đoán đầu. Mọi query/crop/biến thể cùng ảnh gốc phải thuộc cùng tập. Chụp hash ảnh và manifest để truy vết.

**Sản phẩm đã tạo, nhãn Trí xác nhận 27/10 nhưng CHƯA KHÓA:** `experiments/countgdpp/p4_unseen_v1/README.md`, `inputs.jsonl` chỉ chứa ID/ảnh/prompt, và `manifest.csv` cho evaluator chứa GT/nguồn/split. Dùng schema pilot đã có; mở rộng trường nguồn/lịch sử nếu cần. Không đưa count, nhãn từng khung hoặc danh sách lớp thật của ảnh vào bộ lọc.

Điền quyết định dữ liệu tại đây trước khi chạy:

| Mục | Trí cập nhật |
|---|---|
| Nguồn ảnh và nguồn nhãn | MUCCA 1.0 (Zenodo 19231375, CC-BY-4.0); GT = điểm MUCCA. Bản tải ở `data_external/` (không commit) |
| Danh sách ảnh / số ảnh / số query | **LOCKED 27/10 17:07** (trước đó là DRAFT): `experiments/countgdpp/p4_unseen_v1/`, 10 ảnh / 30 query (20 present + 10 absent), rút r2 phân tầng seed 331 |
| Kiểm trùng ảnh gốc với dev và lịch sử sử dụng | Bộ B r2 đã loại 5 ID dev theo bộ chọn; lịch sử dùng ngoài workspace/chọn prompt-ngưỡng vẫn chờ Trí xác nhận. Không dùng bảng 5 ảnh local §2A cũ làm xác nhận cho 10 ảnh r2. |
| Người kiểm GT/absent và ngày | Trí xác nhận 27/10/2026: 10 ảnh, 20 present và 10 absent. Assistant ghi vào CSV theo tin nhắn; không phải kiểm độc lập. Xem human_review_20261027.json. |
| Quy ước đếm và xử lý nhãn không chắc chắn | Đề xuất §4 HUONG_DAN_KIEM_DU_LIEU: đúng loại/cả vật, ghép một-một, trùng/uncertain; chờ Trí chốt. Point-in-box chỉ hỗ trợ ghép, không tự chứng minh đúng vật. |
| Ngày khóa danh sách; manifest/hash | 27/10/2026 17:07:55, Trí; inputs `53e91e81…`, manifest `9161d8f4…` (đủ hash trong selection_meta.json) |

### 2A. Kiểm kê DRAFT do assistant chuẩn bị 27/10 — chưa khóa, chưa đếm tay

**Cách kiểm:** đọc `annotations.json`/`class_mapping.json` gói MUCCA của Triệu; grep toàn CS331 (trừ `CountGDPlusPlus/`) và hai ZIP kết quả tìm `mcac_44/58/81/171/176` và `q06_`–`q10_`. Không chạy model.

| Ảnh | Kích thước | Lớp có điểm MUCCA (số điểm) | Cặp X/Y khác hẳn gợi ý | Ghi chú rủi ro |
|---|---|---|---|---|
| mcac_44 | 360×240 | apples 6, grapes 20, oranges 5, pears 2, bananas 1 | grapes / apples | Cả ảnh là trái cây; "khác hẳn" yếu nhất; ảnh nhỏ |
| mcac_58 | 800×533 | people 125, beach umbrellas 53, chairs 7 | beach umbrellas / people | Ảnh chụp trên cao, vật rất nhỏ và đông; kiểm tay tốn công |
| mcac_81 | 1000×667 | people 70, motorbikes 56, cars 14, trucks 1, bicycles 1 | cars / motorbikes | Đông; người ngồi trên xe máy dễ trùng khung |
| mcac_171 | 1300×957 | sheeps 80, goats 7, dogs 4 | sheep / dogs | Cừu đông; dê gần giống cừu nên không dùng làm cặp chính |
| mcac_176 | 612×406 | people 83, boats 12, cars 7, motorbikes 1 | boats / cars | 83 người rất nhỏ trong ảnh nhỏ: cần xem nhãn có hợp lý không |

**Lịch sử sử dụng (đã kiểm):** không có prediction, review, CLIP score hay chẩn đoán nào chứa 5 ảnh này. Chúng chỉ có trong `inference_inputs.jsonl`, `manifest.csv` (split=`dev`), `contact_sheet.jpg` và bộ query Triệu tạo sau khi xem ảnh. Như vậy **chưa dùng để chọn phương pháp/ngưỡng**. Muốn dùng làm tập kiểm thì phải đổi vai trò khỏi `dev` một cách có ghi chép (lý do, ngày, người), **trước** lần chạy đầu.

**Thiếu so với đề xuất 10 ảnh/30 query:**
- Chỉ có 5 ảnh, nên tối đa 15 query (10 present + 5 absent).
- Chưa có query absent. Lớp absent phải không có trong annotation **và** được Trí xem ảnh xác nhận, ví dụ `guitars` cho bãi biển. Không suy absent chỉ vì annotation thiếu.
- GT là **điểm** chứ không phải box. Điểm này có lợi cho N4: chấm "giữ đúng vật" bằng điểm nằm trong khung giữ, không cần vẽ box. Quy tắc một điểm rơi vào nhiều khung phải chốt trước.
- Nguồn/giấy phép MUCCA chưa ghi trong gói. Ghi chú cũ của nhóm nói MUCCA có trên Zenodo 19231375 (200 ảnh); cần kiểm lại trang gốc trước khi trích dẫn.

**Kết quả 27/10:** Trí chọn **B**. Tải MUCCA 1.0 chính thức, chọn theo quy tắc trong `experiments/countgdpp/p4_select_unseen.py`; kết quả ở `experiments/countgdpp/p4_unseen_v1/` (README). Năm ảnh local ở trên không lọt vào bản rút r2. Hai phương án ban đầu:
- **A — dùng 5 ảnh local:** 5 ảnh × (2 present + 1 absent) = 15 query. Làm ngay được. Mẫu nhỏ, nên báo cáo như kiểm chứng nhỏ.
- **B — lấy thêm ảnh từ MUCCA gốc:** chốt tiêu chí chọn **trước khi xem output**, ví dụ: 2 lớp khác siêu loại, mỗi lớp ≤ 40 điểm, không trùng 5 ảnh dev. Chọn thêm 5 ảnh cho đủ 10/30. Cần tải dữ liệu và kiểm giấy phép, tốn thêm khoảng 1–2 giờ.

Được xem ảnh để chuẩn bị nhãn; điều cần giữ độc lập là **không dùng kết quả trên tập kiểm tra để chọn/sửa phương pháp**. Nhãn dùng chấm điểm phải tách khỏi đầu vào inference. Nếu đã dùng tập này để chỉnh cách làm, đổi vai trò thành dev và cần tập kiểm tra khác.

## 3. P4.6b: chuẩn bị cách áp dụng cấu hình đã khóa

**Người làm: Trí.** Có thể đọc code và viết adapter trong lúc chờ kiểm nhãn; thử chạy model/evaluator do Trí tự thực hiện hoặc assistant hỏi trước nếu chạy thay.

Nguồn chuẩn: [freeze JSON](../results/countgdpp/p4_candidate_freeze_20261021.json), [CLIP run_config](../results/countgdpp/p4_clip_all15_20261020/run_config.json), [code chấm CLIP cũ](../evaluation/p4_clip_score_all15_20261020.py). Script chấm cũ gắn đường dẫn 15 query dev; chưa dùng nó nguyên trạng làm runner cho ảnh mới.

| Thành phần cần giữ | Quy tắc đã dùng |
|---|---|
| CountGD++ | B2 như pilot, tau_sample=tau_final=.23; tối đa 3 pseudo; không có mẫu thì trả B0 theo adapter. Ghi checkpoint hash, code/config và môi trường thực tế khi chạy |
| CLIP | `openai/clip-vit-base-patch32`; revision đã ghi `3d74acf9a28c67741b2f4f2ea7635f0aaf6f0268`; pin cả model và processor vào revision phù hợp, `use_fast=False`, eval mode |
| Crop | Ảnh RGB, bbox xyxy ảnh gốc; Python round và giới hạn biên như hàm trong script cũ; không thêm padding/resize riêng ngoài processor |
| Prompt và score | `a photo of {prompt}` giữ tên query như input; L2-normalize hai embedding, lấy cosine, không softmax và không gọi score là xác suất |
| Bộ lọc điểm B2 | Đọc ngưỡng đủ precision từ JSON: `0.9067394733428955`; giữ khi `score >= threshold` |
| Fusion | Chuẩn hóa riêng hai điểm bằng min/max **đã khóa từ dev**, clamp [0,1], lấy 0.5 mỗi phía; ngưỡng `0.6551826746408328` từ JSON |
| Giới hạn | Không fit lại min/max/ngưỡng theo ảnh hoặc tập mới; không top-K dùng GT; không sửa bbox/thêm NMS trong phép so sánh này |

Freeze hiện chứng minh tái lập **từ điểm đã lưu**, chưa chứng minh pipeline mới chạy ảnh → B2 → CLIP giống hệt. Revision CLIP có trong run_config, nhưng chưa có hash trọng số model được xác nhận trong lượt audit 22/10. Bổ sung manifest code/checkpoint/processor khi chuẩn bị runner; giữ nguyên freeze và kết quả gốc.

**Code adapter viết 27/10, kiểm dev ĐẠT cùng ngày** ([SUMMARY](../reports/audits/devcheck_20261027/SUMMARY.md)) (thư mục `experiments/countgdpp/`):

- `run_b2_frozen.py`: B2 như pilot (τ = .23 cố định, không có tham số dòng lệnh để chỉnh). Không cần B0 của run khác; `--b0-reference` dùng để kiểm replay trên dev.
- `p4_clip_score.py`: crop/template/cosine giống bản 20/10; pin revision, dừng nếu revision lệch.
- `p4_apply_freeze.py`: đếm B2_original / B2_threshold / Fusion_50_50 từ file điểm. Kiểm SHA256 của freeze. Có `--check-audit` (so với audit 21/10) và `--reference-scores` (đo độ lệch điểm và số khung đổi quyết định giữ/bỏ).

Lệnh kiểm dev theo thứ tự nằm ở bảng §3 của [CHECKLIST_3_GIO](CHECKLIST_3_GIO.md).

**Điều kiện qua bước này:** runner nhận input không GT, lưu ID/rank/box/điểm B2/điểm CLIP/khung giữ và count cho từng cách. Kiểm áp dụng freeze trên dev phải khớp [audit cũ](../results/countgdpp/p4_freeze_audit_20261021.json); kiểm lại scorer trên dev với môi trường ghi rõ trước khi dùng ảnh mới. Nếu có sai số điểm, báo độ lệch và tác động qua ngưỡng, không lặng lẽ thay ngưỡng để khớp. Việc kiểm dev này là kiểm triển khai, không được ghi như đánh giá độc lập mới.

## 4. P4.6c–d: chạy và đánh giá một lần theo quy trình đã chốt

**Chưa làm.** Chỉ thực hiện sau khi dữ liệu/GT/cấu hình và cách chấm sẵn sàng.

- So cùng ảnh/query/nguồn bbox: **B2 gốc**, **B2 lọc điểm đã khóa**, **Fusion 50/50 đã khóa**. CLIP-only và B0 là kết quả dev tham khảo, không bắt buộc mở thêm nhánh cho vòng này.
- Đo MAE/RMSE/exact trên toàn bộ, tách present/absent; absent thêm tỷ lệ trả khác 0 và count sai trung bình. Báo đầy đủ ca kém đi và ca không có proposal.
- Để trả lời đúng yêu cầu X/Y, cần kiểm cả **vật nào được giữ**: vật đúng phân biệt giữ được, vật đúng bị bỏ, khung sai loại, khung trùng. Ưu tiên review toàn bộ bộ thử nhỏ; nếu cần lấy mẫu, chốt danh sách ảnh trước kết quả và ghi rõ phạm vi. Dùng cùng nhãn khung gốc để chấm các bộ lọc, không chỉ chọn ảnh Fusion tốt.
- Reviewer nên xem khung đánh số không kèm tên phương pháp/điểm/nhãn sơ bộ. Chốt cách xử lý khung mơ hồ/trùng/phần vật trước chấm; báo số chưa phân xử. Không tự gọi kiểm thủ công là AP/IoU benchmark.
- Giữ nhóm theo ảnh khi phân tích; 30 query trên 10 ảnh không phải 30 ảnh độc lập. Không tuyên bố đã chữa toàn bộ lỗi CountGD++ từ bộ thử nhỏ.

**Quyết định sau kết quả:** nếu Fusion cải thiện chọn đúng vật nhưng làm count kém đi, trình bày đánh đổi thay vì gọi là thắng chung. Nếu không có lợi ích ổn định, báo kết quả âm và kết thúc vòng giả thuyết; thảo luận hướng mới sau đó, không chỉnh trên test rồi báo lại như test độc lập. Nếu chưa đủ nhãn chi tiết, chỉ kết luận về count, giữ kết luận X/Y chờ kiểm.

## 5. Phần đã nhận của Triệu và việc còn lại

1. **Đóng pilot:** Triệu đã chấp nhận bản kiểm evaluator được ủy quyền ngày 24/10; không cần kiểm lại. Trí đọc và cùng nhóm duyệt [PILOT_SUMMARY §7](../reports/PILOT_SUMMARY.md). Không cần hoàn thành P4.6 để đóng pilot.
2. **Kiểm nhãn P4:** [ZIP 47 khung](../results/countgdpp/p4_label_review_handoff_20261021.zip) có 13 + 18 + 16 dòng trắng cho q03_1/2/3. Triệu điền độc lập, chưa xem nhãn assistant trước; trả 3 CSV rồi ghi điểm bất đồng và cách phân xử. q05_2 dùng review cũ, không nằm trong 47 khung này. Review định tính ngày 19/10 không thay bước này.

Trí vẫn làm P4.6a và chuẩn bị P4.6b trong lúc chờ; không tự ký thay Triệu hoặc biến nhãn sơ bộ thành nhãn đã kiểm.

## 6. Checklist để biết đã tiến thêm gì

- [x] P4.1–P4.5c: có artifact thăm dò, cấu hình khóa và kiểm tính nhất quán ngày 22/10.
- [x] Triệu chấp nhận bản kiểm evaluator được ủy quyền ngày 24/10.
- [ ] Trí đọc; nhóm duyệt pilot (độc lập với P4.6).
- [ ] Triệu kiểm 47 nhãn P4; xử lý bất đồng.
- [x] P4.6a: khóa dữ liệu/nhãn/split và lịch sử sử dụng. *(27/10 17:07, Trí xác nhận)*
- [x] P4.6b: runner áp dụng freeze và kiểm trên dev đạt, đủ provenance. *(27/10, trùng tuyệt đối; [SUMMARY](../reports/audits/devcheck_20261027/SUMMARY.md))*
- [x] P4.6c: dự đoán trên tập mới, không dùng GT vào model/bộ lọc. *(27/10, [kết quả](../reports/P4_6_UNSEEN_RESULTS_20261027.md))*
- [~] P4.6d: chấm count + đúng vật, báo cả kết quả xấu và giới hạn. *(27/10: count + chỉ số tự động điểm-trong-khung xong; review khung bằng người theo §4 chưa làm)*
  - **N4 (27/10):** gói review khung chọn lọc, mù với cách lọc, đã sẵn ở `results/countgdpp/p4_n4_review_package_20261027/`. Tầng A gồm 7 query / 78 khung (4 query people + 3 query vắng mặt bị báo sai), tầng B gồm 2 query / 41 khung. Trí điền CSV rồi assistant ghép với bảng tra. Tóm tắt toàn dự án cho demo: `reports/TOM_TAT_DU_AN_20261027.md`.

Sau đó mới quyết định phương pháp cuối và báo cáo đồ án; không hứa P4.6 tự động đáp ứng mọi tiêu chí của giảng viên. Ghi mỗi mốc tại [WORKLOG](../WORKLOG.md), không tạo thêm chuỗi handoff ngày trong thư mục hiện hành.

**Lưu ý kỹ thuật 27/10:** B2 pilot hiện chỉ đọc B0 tham chiếu từ run m4_first5_b0, không nhận ID mới nếu chưa sửa adapter; không đưa lệnh inference ảnh mới như thể runner đã sẵn. C3 của checklist chỉ rõ chỗ cần chuẩn bị.
