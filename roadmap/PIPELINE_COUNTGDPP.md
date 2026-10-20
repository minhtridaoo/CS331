# Pipeline kỹ thuật CS331 — CountGD++

**Cập nhật 20/10/2026, theo ROADMAP V4.6.** Đây là protocol kỹ thuật để tra cấu hình; bắt đầu công việc mỗi buổi ở [README](../README.md), xem trạng thái ở [ROADMAP](ROADMAP.md) và [HANDOFF hiện hành](../HANDOFF/HANDOFF.md).

**Đã có:** smoke 3/3; B0/B2 pilot 5 ảnh/15 query; E1/E2 trên 2 ảnh/6 query; review định tính Trí/Triệu đều 15/15; bản Triệu chốt v1 đã làm rõ guitar/q04_2. **Còn chốt:** [phần 2 evaluator](PHAN_2_DANH_GIA.md) và [phần 3 tổng kết pilot](PHAN_3_TONG_KET.md). Evaluator đã chạy ngày 20/10, output/hash/15 dòng đã audit; còn Triệu kiểm chéo và nhóm duyệt báo cáo. Mục 6 báo cáo có đề xuất CLIP sau B2; chưa có phương pháp cải tiến được kiểm chứng.

**Nhánh benchmark đã hoàn thành lượt chạy:** FSCD-147 1.190 ảnh, MAE=8.336975, RMSE=24.637626; count metrics đã đối chiếu ngày 20/10. [Báo cáo](../reports/BENCHMARK_FSCD147.md). Cấu hình có text + synthetic + pseudo + adaptive crop. Các B0/B2 bên dưới chỉ là cấu hình thành phần của pilot, không phải toàn bộ nhánh đó.

**Phân công/schema đang dùng:** [PIPELINE_PHAN_CONG.md](PIPELINE_PHAN_CONG.md). Trí chạy model; Triệu phụ trách dữ liệu và kiểm evaluator, cùng Trí chốt số liệu. Các kế hoạch mở rộng dưới đây không tự trở thành việc đã hoàn thành.

## 1. Đầu vào và đầu ra

- Hệ thống chỉ nhận ảnh I và tên loại q. Dùng một mẫu prompt tiếng Anh cố định trong pilot.
- Nhãn đếm, vị trí thật, lớp đang hiện diện và lớp vắng mặt chỉ dành cho evaluator.
- Không cung cấp khung mẫu thủ công, danh sách lớp loại trừ từ nhãn thật hoặc ảnh tham chiếu được chọn nhờ nhãn test cho B0/B2.
- Mỗi lượt trả khung và score; count là số khung giữ lại theo code lọc của cấu hình. Khung được quy về tọa độ ảnh gốc khi đánh giá.
- Đầu ra rỗng hợp lệ: count = 0, boxes = [], scores = []. Không đổi crash/OOM thành count = 0.
- Không dùng phản hồi người dùng trên ảnh test để tinh chỉnh B0/B2.

## 2. Dữ liệu và chia tập

**Pilot đã chạy:** 5 ảnh/15 query để khám phá lỗi. **Kế hoạch mở rộng dev:** 20–30 ảnh, chưa hoàn thành và chưa phải benchmark kết luận. Bộ đầu tiên chọn ảnh dễ kiểm tra; ưu tiên ảnh thật nhiều loại vật, mật độ vừa để kiểm nhãn/vị trí. Ghi rõ thiên lệch chọn ảnh dễ; sau đó mở rộng điều kiện khó có kiểm soát.

Mỗi ảnh ưu tiên có qX và qY thuộc hai loại khác hẳn nhau cùng hiện diện, kèm số lượng thật; thêm qAbsent đã xác nhận không có trong ảnh. Có cả cặp X/Y khác số lượng và bằng số lượng. Lớp vắng mặt dễ nhầm có thể thêm sau, phân tầng riêng. Ảnh mơ hồ/che khuất cần quy tắc đếm hoặc loại khỏi chỉ số đòi hỏi nhãn chắc chắn, báo số loại.

**Nguồn:** phần dev được tách trước của dữ liệu công khai phù hợp hoặc ảnh được phép sử dụng. Đã nhận gói MUCCA 10 ảnh/30 query từ Triệu và chuẩn hóa thành dev nội bộ; chưa xác minh độc lập nguồn URL/split gốc. Chưa xác nhận bộ PrACo++ đầy đủ. Nếu trích benchmark test công khai để phát triển, công bố split nội bộ; không gọi phần còn lại là kết quả toàn benchmark gốc.

**Split:** tách theo ảnh gốc trước khi xem dự đoán. Query, crop và phiên bản chỉnh sửa của một ảnh cùng split. Dành holdout độc lập; không dùng holdout chọn prompt, ngưỡng, lớp khó hay module.

**Nhãn âm:** thiếu annotation không đồng nghĩa đối tượng vắng mặt. Kiểm tra thủ công hoặc dùng annotation đủ phạm vi; đánh dấu chưa chắc thay vì coi count = 0.

## 3. Luồng inference bắt buộc

### B0 — Văn bản, một lượt

1. Đọc ảnh và q; chuẩn hóa theo code/config đã pin.
2. Chạy CountGD++ với văn bản; không exemplar thủ công, synthetic, pseudo hay negative label.
3. Giữ dự đoán thô/score cần cho khảo sát ngưỡng, không chỉ kết quả đã lọc.
4. Lọc bằng tau_final. Lưu count/boxes/scores và overlay.
5. Pilot không dùng adaptive cropping; ghi rõ khác toàn bộ pipeline paper.

### B2 — Văn bản rồi tự chọn mẫu

1. Lượt một khớp B0 về ảnh, prompt, weights, resize và precision.
2. Chọn pseudo-exemplar từ dự đoán trên chính ảnh bằng tau_sample và quy tắc chọn mẫu được đối chiếu với code gốc.
3. Ghi khung/score mẫu, số mẫu, quy tắc chọn và tọa độ chuyển đổi.
4. Chạy lượt hai với q và mẫu tự chọn. Lọc bằng tau_final.
5. Lưu cả hai lượt; kiểm tra mẫu chọn sai lớp có đi cùng lỗi lượt hai không.
6. Nếu không có mẫu: xác minh hành vi code gốc trước. Với adapter pilot, dùng quy ước trả B0 và log no_pseudo=true; ghi đây là quy ước của adapter nếu khác mã gốc, không gọi là tái hiện nguyên bản.
7. Số mẫu tối đa và xử lý trùng khung phải ghi trong config, dùng nhất quán.

**Trước khi chạy hàng loạt:** thử một ảnh với X/Y/vắng mặt; count khớp số khung; overlay đúng tọa độ; prompt thật sự đổi; exemplar không lấy từ nhãn; nhánh không mẫu chạy được; lỗi được ghi riêng. Đối chiếu B0 với suy luận gốc cùng thiết lập, B2 với logic hai lượt đã đọc.

## 4. Ma trận cấu hình cho pilot và bước cải tiến

Bảng này áp dụng nhánh dev chẩn đoán. “Hoãn B3” nghĩa là chưa tích hợp B3 vào runner pilot; nhánh benchmark riêng đã chạy synthetic/pseudo/crop.

| Mã | Cấu hình | Trạng thái |
|---|---|---|
| B0 | Text một lượt | Đã chạy 15 query |
| B2 | Text → pseudo từ ảnh → lượt hai | Đã chạy 15 query |
| B4(B2) | B2, khảo sát riêng hai ngưỡng | E1/E2 đã làm trên 6 query; E3 chưa mở |
| B1 | Text + synthetic, một lượt | Hoãn; cần nguồn exemplar rõ |
| B3 | Text + synthetic + pseudo | Hoãn; không bắt buộc cho pilot |
| B4(B3) | B3, khảo sát riêng hai ngưỡng | Chỉ nếu đã triển khai B3 |
| B5 | B2 hoặc B3 đã khóa + phương pháp đã công bố | Sau phân tích lỗi/kiểm tra tích hợp |
| B6 | Bổ sung nhãn lớp loại trừ từ dữ liệu | Có thêm thông tin, báo riêng |

B4 được mở rộng để áp dụng ngay lên B2; không chờ B3. Mọi bảng ghi B4(B2) hay B4(B3), không dùng tên B4 mơ hồ.

B0/B2/B4(B2) cùng điều kiện I + q. B1/B3/B4(B3)/B5 chỉ vào bảng cùng điều kiện nếu mọi thông tin phụ tuân thủ đầu vào đã công bố. Tham chiếu được chọn bằng nhãn benchmark phải sang bảng có thêm thông tin.

B6 không phải cải thiện trong cùng đầu vào, cũng không mặc nhiên là cận trên. Phương pháp nhóm đề xuất sau này gọi M1 với định nghĩa riêng; so với nền khớp điều kiện, không đổi tên phương pháp đã có thành M1.

## 5. Tách ngưỡng: E1/E2/E3

Wrapper PrACo đã kiểm tra dùng CONF_THRESH = 0.23 cho chọn pseudo và lọc cuối. Đây là điểm xuất phát theo code, không bảo đảm tối ưu.

| Thí nghiệm | tau_sample | tau_final | Câu hỏi |
|---|---|---|---|
| B2 mặc định pilot | 0.23 | 0.23 | Hai lượt ở mốc tham chiếu ra sao? |
| E1 | Giữ 0.23 | Quét trên dev | Chỉ đổi lọc cuối có đủ không? |
| E2 | Quét trên dev | Giữ 0.23 | Đổi mẫu tự chọn ảnh hưởng gì? |
| E3 | Quét trên dev | Quét trên dev | Kết hợp có đánh đổi tốt hơn không? |

Lưới đề xuất ban đầu: {0.10, 0.23, 0.35, 0.50}. E1 đã chạy đủ lưới cho B0/B2; E2 đã chạy .10/.23/.50, bỏ .35 sau khi kiểm điểm top-3 vì mẫu sẽ giữ nguyên (suy luận, không phải lần chạy). E3 chỉ mở khi còn câu hỏi cụ thể; hiện chưa cần chạy thêm chỉ để đủ lưới.

E1 chỉ được tái dùng đầu ra lượt hai khi thay riêng lọc cuối và đã lưu đủ dự đoán trước lọc. E2/E3 đổi mẫu thì chạy lại lượt hai tương ứng. Không tái dùng cache từ tau_sample khác.

Lợi ích E1/E2 là dấu hiệu chẩn đoán, không tự chứng minh nguyên nhân hay phương pháp mới. Luôn đọc đồng thời kết quả truy vấn có mặt.

## 6. Chỉ số

### Vật thể vắng mặt

- FPR_absent = số cặp vắng mặt có count dự đoán > 0 / tổng cặp vắng mặt hợp lệ.
- MeanAbsentCount = trung bình count dự đoán trên query vắng mặt.
- Báo cả số ảnh và query, không chỉ một tỷ lệ thiếu mẫu số.

### Vật thể có mặt và đổi X/Y

- MAE_present/RMSE_present: trên query có đối tượng thật.
- Presence recall = tỷ lệ query có mặt được dự đoán count > 0. Chỉ đo trả số dương, không chứng minh chọn đúng lớp hoặc đủ số lượng.
- Kiểm tra khung X/Y; chấm thủ công: đúng lớp / nhầm lớp khác / nền / chưa rõ, kèm người kiểm tra.
- Pilot lập bảng số ca nhầm lớp và minh họa vị trí, ghi cách chấm. Chưa gọi đó là CntF1 hay metric chuẩn của paper.
- Đo vị trí tự động cần GT phù hợp và quy tắc ghép dự đoán–GT/evaluator được khóa trước. Nhãn count đơn thuần không đủ suy precision/recall vị trí.
- Phân biệt trùng khung, đếm thiếu, nhầm lớp và lỗi chuyển tọa độ.

### So sánh và thống kê

- Xem FPR_absent ở presence recall tương đương trên dev, cùng MAE_present và lỗi chọn sai lớp.
- Chọn operating point trên dev rồi khóa trước holdout. Trên holdout báo recall thực đạt; không chỉnh ngưỡng để ép khớp recall trên test.
- Giữ cùng ảnh, query, weights, resize, precision và crop; ghi mọi khác biệt.
- Đo thời gian/VRAM cùng thiết bị, batch size, quy tắc warm-up và đồng bộ GPU. Ghi thời gian có gồm tiền xử lý/tạo mẫu không.
- Khoảng tin cậy: bootstrap theo ảnh, giữ toàn bộ query của ảnh cùng nhau; so trước–sau trên cùng mẫu ảnh. Báo giới hạn khi pilot nhỏ.

### Nếu tái hiện PrACo

PCCN không phải tỷ lệ đếm chính xác. Với PrACo gốc, d_pos = |c_pos - y|, d_neg = |mean(c_absent) - y|; PCCN là phần trăm ảnh có d_pos < d_neg. NMN là đếm nhầm chuẩn hóa theo count thật, không phải FPR_absent.

Bảng 3 CountGD++ báo NMN/PCCN 0.88/62.86 cho dòng không negative text, 0.07/97.99 cho dòng có negative text. Đây là số tác giả trong protocol có synthetic/pseudo, không phải kết quả B0 hay nhóm tự chạy.

Không trộn định nghĩa PrACo/PrACo++ hoặc split khác nhau. Muốn tái hiện hai dòng phải kiểm tra nhánh có/không negative prompt; benchmark đã đọc không có tùy chọn trực tiếp tắt nhãn âm ở nhánh query vắng mặt.

## 7. File đầu ra cần triển khai

B0/B2 đã có manifest, inputs, predictions.jsonl và run_config. Evaluator đã chạy với 5 output/run; số liệu và hash nguồn đã đối chiếu. Báo cáo đã điền kết quả và kế hoạch, chờ kiểm chéo/duyệt. Mô tả dưới đây là đặc tả chung, tên trường thực tế theo schema v1 trong [phân công](PIPELINE_PHAN_CONG.md).

**manifest.csv:** image_id, source_group_id, image_path, source_url, license_note, split; query_id, target_class, prompt, presence_status, gt_count, pair_id; annotation_source, verified_by, uncertainty_note. GT vị trí lưu riêng nếu có; không truyền GT vào model.

**run_config.json:** run_id, model_commit, adapter_commit_or_diff, checkpoint_source, checkpoint_sha256, dataset_manifest_sha256, variant, prompt_template, seed; tau_sample, tau_final, max_pseudo, no_pseudo_policy, synthetic_source, negative_prompt_source; resize, precision, cropping, device, environment_versions.

**predictions.jsonl:** run_id, image_id, query_id, variant, execution_status, error_message; stage1_boxes/scores/count, pseudo_boxes/scores, no_pseudo; stage2_boxes/scores/count nếu có lượt hai; final_boxes/scores/count; quy ước tọa độ, thời gian, peak_vram, overlay_path. Lưu dự đoán thô đủ cho lưới ngưỡng; ghi mức lọc lưu trữ nếu không giữ tất cả.

**error_review.csv:** run_id, image_id, query_id, pred_box_id, reviewed_class, error_type, reviewer, note. Phân biệt nhầm lớp, nền, trùng khung, thiếu đối tượng và nhãn chưa rõ.

**reports/PILOT_SUMMARY.md:** B0/B2, E1/E2 nếu có; số ảnh/query, lỗi thực thi, bảng chỉ số, ca đúng/sai, giới hạn và quyết định tiếp theo.

Đường dẫn hiện hành: input ở experiments/countgdpp/m4_inputs/; runner ở experiments/countgdpp/; evaluator ở evaluation/; kết quả ở results/countgdpp/<run_id>/; báo cáo ở reports/. Chưa cần tạo thêm data/pilot/ hoặc configs/countgdpp/ chỉ để khớp tên kế hoạch cũ. Không ghi đè cấu hình khác. Chỉ resume/cache khi metadata khớp checkpoint, dữ liệu, prompt, mẫu và ngưỡng.

## 8. Phần hoãn lại

Nếu mở B1/B3, ghi exemplar từ text, ảnh đầu vào hay tham chiếu ngoài; cách chọn ảnh, model tạo mẫu, seed, nhãn dev/test có được dùng không. Phụ lục C.4 mô tả tham chiếu ảnh, còn benchmark đã kiểm tra có chọn ảnh khác theo lớp để lấy mẫu. Đây là khác biệt protocol cần công bố, không phải kết luận tác giả sai.

Fantastic Tractor-Dogs (ICLR 2026) là ứng viên đối chứng đã công bố cho lỗi detector theo văn bản. Chưa xác minh tích hợp CountGD++ hoạt động; nối vài token tùy ý không đồng nghĩa tái hiện đúng phương pháp. Chỉ mở B5 sau khi baseline/lỗi rõ.

Không chốt “semantic verifier” là đóng góp mới trước khi đối chiếu công trình liên quan và thử đối chứng đơn giản.

## 9. Nguồn để tái lập

Các commit là snapshot đã đọc, không tuyên bố luôn là nhánh mới nhất hoặc đã chạy thành công:

- CountGD++: 8489f836d75eb407ae778c56cff1f72cc6f8baae.
  [README](https://github.com/niki-amini-naieni/CountGDPlusPlus/blob/8489f836d75eb407ae778c56cff1f72cc6f8baae/README.md) · [process_folder.py](https://github.com/niki-amini-naieni/CountGDPlusPlus/blob/8489f836d75eb407ae778c56cff1f72cc6f8baae/process_folder.py).
- PrACo: 34c7a8d3fdff5f77741bc8f598e6db8cfc50655b.
  [benchmark.py](https://github.com/ciampluca/PrACo/blob/34c7a8d3fdff5f77741bc8f598e6db8cfc50655b/benchmark/benchmark.py) · [wrapper CountGD++](https://github.com/ciampluca/PrACo/blob/34c7a8d3fdff5f77741bc8f598e6db8cfc50655b/models/countgdplusplus_model.py).
- [CountGD++ — paper v2](https://arxiv.org/html/2512.23351v2).
- [PrACo — định nghĩa metric](https://arxiv.org/html/2409.15953v2).
- [PrACo++](https://arxiv.org/html/2605.02752v1).
- [Fantastic Tractor-Dogs — ICLR 2026](https://proceedings.iclr.cc/paper_files/paper/2026/hash/ae50a5245a775b10c621b0f5b28eb460-Abstract-Conference.html).

Khi triển khai xác minh snapshot khớp checkpoint, log phiên bản thực dùng; đổi commit phải lưu lý do/khác biệt. Không trình bày trọng số tác giả như sản phẩm nhóm tự huấn luyện.
