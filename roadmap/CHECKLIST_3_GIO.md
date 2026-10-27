# Checklist làm tiếp — buổi 3 giờ, lập ngày 27/10/2026

**Mở file này mỗi khi bắt đầu session mới.** Trạng thái chung: [HANDOFF](../HANDOFF/HANDOFF.md). Chỉ đánh dấu xong khi có artifact hoặc xác nhận; kế hoạch không phải kết quả đã thực hiện.

## 0. Điểm tiếp tục hiện tại

- Ngày cập nhật: **27/10/2026**.
- **Deadline báo cáo cuối: 02/12/2026**, người dùng xác nhận; còn 36 ngày tính từ 27/10. Các mốc trung gian bên dưới là đề xuất, chưa phải cam kết của Triệu.
- Git đã pull: `main`, commit `d6db18931c07671763137962f7db54bd1fc3be70` từ `origin/main`.
- Triệu đã đọc/hiểu và chấp nhận **bản kiểm kỹ thuật được ủy quyền cho assistant** ngày 24/10. Đây là lịch sử chấp nhận bản kiểm được ủy quyền; **yêu cầu mới của Trí ngày 27/10 là Triệu tự làm T1–T4**, không đồng nhất hai việc.
- Pilot **Trí chưa duyệt, yêu cầu sửa T1–T4**; có rerun evaluator/fixtures do Triệu tự làm, không cần inference model mới. 47 nhãn P4 **vẫn chưa có bản kiểm độc lập**.
- P4 đã đến **P4.5c**, freeze còn giữ nguyên. Bộ ảnh mới chưa khóa; runner đã đạt kiểm dev (1)–(4).
- **Cập nhật cuối 27/10:**
  - C1 xong: Trí chưa duyệt kiểm chéo → Triệu làm T1–T4 theo [kế hoạch sửa](../reports/KE_HOACH_SUA_KIEM_CHEO_20261027.md).
  - Dữ liệu: phương án B, tập `p4_unseen_v1` **ĐÃ KHÓA 27/10 17:07** (absent của mcac_88/84 đổi trucks→bicycles trước khi khóa).
  - Kiểm dev bước (1) đạt.
  - **Việc đầu tiên của Trí:** chốt quy tắc chấm và lịch sử sử dụng, rồi khóa p4_unseen_v1. Nhãn đã xác nhận; C3 đã đạt; chưa chạy ảnh mới.
- Các thay đổi tài liệu/P4 local đã được bảo toàn khi pull, **chưa commit/push**. Snapshot: [trước pull](<../quá khứ/2026-10-27_truoc_pull.zip>). Stash an toàn được giữ nguyên để phục hồi, không apply lại vào workspace hiện tại.

## 1. Buổi 3 giờ tiếp theo của Trí — không lặp C1

| Thời gian | Việc | Đầu ra |
|---|---|---|
| 0–15 phút | Chia sẻ/kiểm gói T0 theo [kế hoạch V2](../reports/KE_HOACH_SUA_KIEM_CHEO_20261027.md) | Triệu có đường nhận đúng gói; chưa gửi thì giữ trạng thái chờ |
| 15–75 phút | C2: nhãn đã xác nhận; chốt quy tắc chấm và lịch sử sử dụng | Chỉ khóa khi đủ điều kiện; không bắt kiểm lại tất cả nhãn |
| 75–165 phút | C3 đã đạt; chuẩn bị P4.6c và cách chấm N4 | Chỉ chạy ảnh mới sau khóa tập và khi người dùng tự chạy/cho phép |
| 165–180 phút | C4 bàn giao | Lệnh/output/lỗi/việc đầu tiên lần sau |

Không cần chờ Triệu xong T1–T3 để chuẩn bị P4. Không mở bộ test để debug; chỉ chạy ảnh mới sau dữ liệu khóa và kiểm dev đạt. C1 đã đọc và chưa duyệt là kết quả của C1, không phải C1 chưa làm.

## 2. Checklist cụ thể — dùng làm nơi đánh dấu duy nhất cho buổi này

### C0 — assistant đã hoàn thành trước buổi tự làm

- [x] Fetch/pull commit mới của Triệu; sao lưu và hợp nhất thay đổi tài liệu với P4 local.
- [x] Đọc xác nhận 24/10 và đối chiếu trace 15 query với nguồn; count metrics khớp.
- [x] Nhận đủ artifact q02_1; giữ cờ `human_adjudication_complete=false` trong nguồn, không nâng thành mọi bbox đã được người kiểm phân xử.
- [x] Xác định 47 nhãn q03 chưa được bổ sung trong commit mới.
- [x] Chuẩn bị checklist 3 giờ và điểm bắt đầu session mới; chưa chạy evaluator/model/train.

### C1 — Trí đã đọc, yêu cầu sửa T1–T4

- [x] Đọc [kết quả Triệu chấp nhận](../reports/TRIEU_KET_QUA_KIEM_CHEO_20261024.md), nhất là kết luận và giới hạn. *(Trí, 27/10)*
- [x] Đọc [PILOT_SUMMARY §7](../reports/PILOT_SUMMARY.md); ghi Trí đã đọc, đồng ý hoặc cần sửa mục nào, ngày thực tế. *(27/10: Trí **chưa duyệt**, 4 nhận xét → [kế hoạch sửa T1–T4](../reports/KE_HOACH_SUA_KIEM_CHEO_20261027.md))*
- [ ] *(chờ Triệu làm T1–T4, rồi duyệt chung)* Nếu nhóm đã cùng duyệt, ghi quyết định đóng pilot. Nếu chưa, để **chờ duyệt chung** và tiếp C2; việc này không chặn chuẩn bị P4.

**Không lặp vô cớ** review guitar/q04_2 hoặc benchmark. Riêng evaluator/self-test/7 ca lỗi là yêu cầu T1 mới để Triệu tự kiểm, làm theo kế hoạch V2; assistant không chạy thay trong lượt chuẩn bị.

### C2 — quyết định dữ liệu trước khi chạy

**Hướng dẫn thao tác đã chuẩn bị:** [C2: mở ảnh và điền từng cột](../experiments/countgdpp/p4_unseen_v1/HUONG_DAN_KIEM_DU_LIEU.md), có 10 ảnh chấm GT từ annotation nguồn. Trí đã xác nhận nhãn cả 10 ảnh qua tin nhắn; đã ghi vào CSV, dữ liệu vẫn DRAFT chờ quy tắc/lịch sử sử dụng.

- [ ] Ghi lịch sử sử dụng của ảnh: đã dùng để chọn phương pháp/prompt/ngưỡng chưa, có trùng/crop từ ảnh dev không.
- [x] *(27/10: MUCCA 1.0, Zenodo 19231375, CC-BY-4.0; gói Triệu trùng từng byte bản chính thức)* Ghi URL/nguồn gốc, quyền sử dụng và nguồn GT; không coi thiếu annotation là absent.
- [x] *(27/10: Trí chọn phương án B; rút r2 phân tầng → `experiments/countgdpp/p4_unseen_v1/`, 10 ảnh/30 query, DRAFT)* Chọn phạm vi dự kiến: **10 ảnh gốc / 30 query** (2 loại khác hẳn cùng có mặt + 1 absent mỗi ảnh). Đây là đề xuất đã có, chưa phải dữ liệu sẵn sàng. Có thể đổi số lượng trước kết quả nếu thiếu thời gian; phải ghi lý do và giữ phạm vi nhất quán.
- [x] Trí xác nhận kiểm nhãn toàn bộ 10 ảnh: 20 GT present và 10 absent; assistant ghi theo tin nhắn 27/10.
- [ ] Chốt riêng quy tắc đếm/ghép khung/trùng/uncertain theo hướng dẫn §4; xác nhận nhãn đúng không thay chốt protocol.
- [x] Ghi xác nhận nhãn và phần còn chờ vào bảng §2 [P4_TIEP_THEO](P4_TIEP_THEO.md); inputs giữ nguyên, manifest chỉ đổi metadata review.
- [x] **KHÓA 27/10 17:07:55** (Trí xác nhận, quy ước §4; hash ghi trong selection_meta và WORKLOG). Chỉ đánh dấu **khóa tập kiểm** khi đủ danh sách/nhãn/lịch sử và hash; còn thiếu thì ghi `DRAFT`, không chạy như holdout.

**Thông tin đã kiểm để tiết kiệm thời gian tìm:** gói cũ có 5 ảnh ngoài bộ 5 ảnh pilot: `mcac_44`, `mcac_58`, `mcac_81`, `mcac_171`, `mcac_176`. Lượt 27/10 không thấy các ID này trong các file `results/countgdpp/*/predictions.jsonl` đã quét. **Điều đó không chứng minh chưa dùng ở nơi khác hoặc là holdout**: toàn bộ manifest 10 ảnh đang mang nhãn dev nội bộ, nguồn/split gốc chưa xác minh. Không tự đổi nhãn tập chỉ để đủ số. Một số ảnh có 80–125 vật, chi phí kiểm nhãn có thể cao; chốt tiêu chí mật độ/phạm vi trước khi xem output.

### C3 — chuẩn bị runner ảnh mới; đây là phần kỹ thuật cấp thiết

**Code hiện tại cần đọc:** [run_b2_pilot.py](../experiments/countgdpp/run_b2_pilot.py), [run_b0_batch.py](../experiments/countgdpp/run_b0_batch.py), [CLIP scorer](../evaluation/p4_clip_score_all15_20261020.py), [freeze](../results/countgdpp/p4_candidate_freeze_20261021.json).

- [x] Chuẩn bị adapter mới, giữ script pilot cũ để tái lập. **Assistant viết code 27/10:** [run_b2_frozen.py](../experiments/countgdpp/run_b2_frozen.py), [p4_clip_score.py](../experiments/countgdpp/p4_clip_score.py), [p4_apply_freeze.py](../experiments/countgdpp/p4_apply_freeze.py). Đã có kiểm (1) apply_freeze trên điểm lưu sẵn đạt; **B2/CLIP và freeze (2)–(4) đã đạt 27/10**. `run_b2_pilot.py`/`run_b0_batch.py` không đổi.
- [x] (đã kiểm dev 27/10) `run_b2_frozen.py`: không còn B0 cố định; stage 1 của chính run là B0, `--b0-reference <predictions.jsonl>` bật lại kiểm replay cho dev. B2 cũ dòng khoảng 61–67 chỉ đọc B0 trong `m4_first5_b0` và sẽ dừng `Missing B0 reference` với ID mới. Adapter cần nhận đường dẫn B0 tham chiếu của **cùng input mới**, hoặc tính/lưu stage1 của chính input mới; kiểm replay là chế độ riêng trên dev. Không bỏ kiểm rồi âm thầm dùng B0 khác ảnh/query.
- [x] (đã kiểm dev 27/10) `p4_clip_score.py --inputs --predictions --run-id`; pin `revision=3d74acf…` cho cả model/processor, dừng nếu revision lệch; ghi hash file trọng số trong cache. CLIP scorer nhận đường dẫn input/prediction/output qua tham số; bỏ assert/đường dẫn gắn 15 query cũ ở bản adapter. Giữ nguyên cách crop RGB, làm tròn/giới hạn biên, template, L2 cosine và processor `use_fast=False`; pin revision như run_config.
- [x] (đã kiểm dev 27/10) `p4_apply_freeze.py`: từ chối freeze nếu SHA256 khác audit `3c4634e7…`. Bộ áp dụng freeze đọc đủ precision ngưỡng/min–max từ JSON; `>=`, clamp [0,1], trọng số .5/.5. Không refit theo ảnh mới, không dùng GT để chọn K hoặc class loại trừ.
- [x] (đã kiểm dev 27/10) cả ba script ghi run_config + hash adapter/input/prediction; `kept_boxes.json` lưu rank/điểm/quyết định giữ. Ghi ID/rank/box/score/khung giữ/count, checkpoint/code/config hash và môi trường; kết quả mới vào thư mục run mới, không ghi đè pilot.
- [x] **ĐẠT 27/10** (Trí cho phép, assistant chạy): 15/15 query khớp audit, output `results/countgdpp/p4_freeze_devcheck_20261027/`. Kiểm riêng việc áp dụng freeze trên **điểm dev đã lưu**: số count từng query khớp [freeze audit](../results/countgdpp/p4_freeze_audit_20261021.json). Đây là kiểm triển khai, không phải thí nghiệm độc lập.
- [x] **ĐẠT 27/10** (assistant chạy theo yêu cầu Trí): ảnh → B2 → CLIP → freeze trùng tuyệt đối, Δbox = Δscore = Δclip = 0, 0 khung đổi quyết định, audit 15/15 ([SUMMARY](../reports/audits/devcheck_20261027/SUMMARY.md)). Sau đó mới kiểm lại ảnh → B2 → CLIP trên dev. Nếu score lệch, lưu phiên bản/mức lệch và ảnh hưởng qua ngưỡng; không sửa ngưỡng để che lỗi.

**Không có lệnh chạy ảnh mới hoàn chỉnh để copy lúc này**: adapter đã kiểm đạt trên dev; tập mới vẫn chưa khóa. Session sau phải kiểm file/CLI thật trước khi hướng dẫn chạy. Người dùng có thể tự chạy các bước đã hiểu; assistant phải hỏi trước nếu chạy evaluator/model/thực nghiệm thay, theo yêu cầu trước đó.

Môi trường được ghi trong lịch sử: CountGD++ từng chạy WSL tại `/root/.venvs/countgdpp`; CLIP score lưu torch `2.9.1+cu128`, transformers `4.57.1`. Không suy rằng hiện tại cả hai dùng chung môi trường hoặc vẫn hoạt động. Kiểm lại môi trường thực tế trước lần chạy, không cài lại toàn bộ chỉ vì lệnh `python` khác `python3`.

### C4 — bàn giao 15 phút cuối, bắt buộc dù chưa xong C2/C3

- [ ] Ghi việc **đã làm thật**, file/code/output mới, lệnh cuối, kết quả/lỗi vào [WORKLOG](../WORKLOG.md).
- [ ] Điền bảng “Dừng ở đâu” ngay dưới; checkbox nào chưa đủ bằng chứng thì giữ trống.
- [ ] Đổi “Việc đầu tiên chưa làm” ở đầu checklist và HANDOFF sang đúng checkpoint tiếp theo.
- [ ] Kiểm `git status --short --branch`; chỉ ghi commit/push nếu thực sự thực hiện. File local vẫn còn sau đổi session, nhưng không tự xuất hiện ở máy Triệu/GitHub nếu chưa push.

## 3. Dừng ở đâu — cập nhật cuối mỗi buổi

| Trường | Hiện tại sau rà giao việc V2 ngày 27/10 |
|---|---|
| Mốc đã xác nhận | C1: Trí đọc, chưa duyệt. C2: B, đã ghi xác nhận nhãn 10 ảnh/30 query, chưa khóa. C3: code đã viết, kiểm (1) từ điểm lưu sẵn đạt 15/15; (2)–(4) **ĐẠT 27/10, trùng tuyệt đối** ([SUMMARY](../reports/audits/devcheck_20261027/SUMMARY.md)) |
| Việc đầu tiên cần tiếp | **Trí 28/10 (45 phút):** push (lệnh §4 [roadmap/VI_TRI_PIPELINE_20261028.md](../roadmap/VI_TRI_PIPELINE_20261028.md)) → gửi Triệu [HANDOFF/GIAO_VIEC_TRIEU_20261028.md](../HANDOFF/GIAO_VIEC_TRIEU_20261028.md) → nghiệm thu bản tự kiểm → chốt quy tắc dữ liệu. **Triệu:** N4 tầng A trước 30/10 (Trí đã chấm u01_1). Sau N4: chọn nhánh P hoặc R |
| Pilot còn chờ gì | Triệu tự làm T1–T4 theo yêu cầu mới; Trí tiếp C2/C3 song song |
| Danh sách dữ liệu / trạng thái khóa | B, 10 ảnh/30 query (20 present + 10 absent). **LOCKED 27/10 17:07:55**, Trí xác nhận; u07_3/u10_3 đổi trucks→bicycles trước khi khóa; quy ước chấm §4. **P4.6c đã chạy 27/10** ([kết quả](../reports/P4_6_UNSEEN_RESULTS_20261027.md)) |
| Runner / log kiểm dev | **P4.6b ĐẠT 27/10: (1)–(4) đều PASS, trùng tuyệt đối** ([SUMMARY](../reports/audits/devcheck_20261027/SUMMARY.md)). Lệnh đã dùng: `run_b2_frozen.py`, `p4_clip_score.py`, `p4_apply_freeze.py` (thư mục experiments/countgdpp). Thứ tự kiểm dev: (1) apply_freeze trên điểm đã lưu, CPU: `python experiments/countgdpp/p4_apply_freeze.py --scores results/countgdpp/p4_clip_all15_20261020 --run-id p4_freeze_devcheck_<ngày> --check-audit results/countgdpp/p4_freeze_audit_20261021.json`; (2) WSL GPU: `run_b2_frozen.py --inputs experiments/countgdpp/m4_inputs/first5_inputs.jsonl --run-id p4_b2_devcheck_<ngày> --b0-reference results/countgdpp/m4_first5_b0/predictions.jsonl`; (3) `p4_clip_score.py` trên predictions của (2); (4) apply_freeze trên điểm mới với `--reference-scores results/countgdpp/p4_clip_all15_20261020 --check-audit …` |
| Lệnh thực nghiệm cuối đã kiểm / output | Phiên song song: p4_apply_freeze.py trên p4_clip_devcheck_20261027 với --check-audit và --reference-scores → cả hai PASS; output results/countgdpp/p4_freeze_e2e_devcheck_20261027/. Lượt hiện tại chỉ ghi CSV/xác nhận, không chạy model. |
| Lỗi đang chặn / cách tái hiện | Không còn chờ xác nhận nhãn. Còn chốt quy tắc chấm/lịch sử sử dụng và khóa. C3 đã đạt; T0 cần chia sẻ nếu chưa gửi. |
| Cập nhật gần nhất, không chạy thực nghiệm | Ghi xác nhận Trí vào 10 dòng absent và 30 dòng manifest; human_review_20261027.json lưu nguồn tin nhắn. Không đổi input/GT/prompt/freeze, không khóa tập. |
| Run đã mở trên ảnh mới | Chưa chạy |
| Việc Triệu còn cần bàn giao | Theo [HANDOFF/GIAO_VIEC_TRIEU_20261028.md](../HANDOFF/GIAO_VIEC_TRIEU_20261028.md): V1–V2 N4 tầng A (30/10); V3 q05_3, V4 2 ca thử, V5 phân tích B2/B0 (01/11); V6 N4 tầng B (02/11); V7 duyệt chung (03/11). 47 nhãn q03 đề xuất tạm hoãn |
| Git | HEAD d6db189; tài liệu/P4 local chưa commit/push; snapshot/stash còn giữ |

## 4. Sau 3 giờ hôm nay, làm tiếp theo thứ tự nào?

1. **N1:** hoàn thiện runner và kiểm dev nếu C3 còn dở. Chưa đạt thì chưa chạy tập mới.
2. **N2:** hoàn thiện/khóa dữ liệu, GT, cách chấm; nhận/đối chiếu nhãn q03 từ Triệu khi có. Có thể chuẩn bị song song N1, không tuyên bố nhãn đã được kiểm.
3. **N3:** chạy **B2 gốc → B2 lọc điểm đã khóa → Fusion đã khóa** trên cùng bộ mới; lưu toàn bộ kết quả, không chỉ ảnh tốt. Không chỉnh theo test.
4. **N4:** chấm count và kiểm vật nào giữ/bỏ, báo absent và lỗi thực thi riêng. Nếu chưa có nhãn vật thì chỉ kết luận count; nhãn q03 cũ không thay nhãn tập mới.
5. **N5:** viết bảng kết quả, ví dụ đúng/sai, hạn chế và demo. Nếu Fusion không hơn đối chứng, báo kết quả âm/đánh đổi; chưa mở thêm một đợt tuning ngay trên test.

P4.6a = C2/N2; P4.6b = C3/N1; P4.6c = N3; P4.6d = N4. N5 là hoàn thiện báo cáo, không phải yêu cầu tự tạo thêm model. Pilot có thể được nhóm đóng riêng trước các bước này.

## 5. Ước lượng công việc còn lại

Đây là **ước lượng lập kế hoạch**, chưa phải thời gian đo hoặc cam kết ngày nộp. Deadline báo cáo cuối đã xác nhận: **02/12/2026**. Mục tiêu nội bộ là hoàn thiện bản báo cáo/demo trước 29/11, giữ 30/11–01/12 làm dự phòng. Với một bộ kiểm nhỏ khoảng 10 ảnh/30 query, môi trường còn dùng được và không mở hướng mới:

| Phần | Giờ tập trung dự kiến |
|---|---:|
| Buổi chuẩn bị hôm nay | 3 |
| Hoàn thiện runner và kiểm dev sau hôm nay | 3–5 |
| Hoàn thiện dữ liệu, GT và nhãn cần cho phép đo | 4–7 |
| Chạy/chấm bộ mới, phân tích kết quả | 2–4 |
| Báo cáo và demo tối thiểu | 3–5 |
| **Tổng từ hiện tại** | **15–24 giờ, khoảng 5–8 buổi × 3 giờ** |

Nếu hôm nay đạt mốc dự kiến thì còn khoảng **12–21 giờ**. Đây là tổng khối lượng thực hiện; có thể chia với Triệu và làm song song. Chưa tính chờ GPU/đồng đội hoặc khôi phục môi trường. Nếu thiếu nguồn dữ liệu/nhãn hoặc phải gán nhãn quá nhiều vật, cần dự phòng thêm khoảng 6–12 giờ và điều chỉnh phạm vi trước test. Không bảo đảm một vòng kết quả âm tự đáp ứng yêu cầu cải tiến của giảng viên; cần đối chiếu tiêu chí chấm.

## 5A. Lịch đến hạn báo cáo 02/12 và cách xử lý kiểm chéo chưa đạt

**36 ngày lịch từ 27/10 đến 02/12; không đồng nghĩa 36 ngày làm toàn thời gian.** Giữ lịch 3 giờ hôm nay; 15–24 giờ là ước lượng cho vòng thực nghiệm nhỏ và bản báo cáo/demo tối thiểu khi dữ liệu/môi trường thuận lợi, không bao gồm mọi vòng sửa theo góp ý thầy.

| Mốc nội bộ đề xuất | Việc cần chốt |
|---|---|
| 27/10–03/11 | Triệu T1–T4 theo kế hoạch V2; Trí xác minh dữ liệu và kiểm adapter song song; duyệt khi đủ bằng chứng |
| 02–08/11 | Runner kiểm trên dev đạt; khóa bộ kiểm mới và quy tắc chấm |
| 09–15/11 | Chạy/chấm bộ mới, kiểm count và đúng vật; không tuning trên test |
| 16–22/11 | Chốt phân tích, giới hạn và bản thảo báo cáo/demo; nếu cần đổi hướng phải ghi rõ phạm vi và thời gian còn lại |
| 23–29/11 | Hoàn thiện báo cáo/slide, diễn tập, kiểm khả năng tái lập |
| 30/11–01/12 | Dự phòng sửa lỗi/file trình bày; không mặc định mở thí nghiệm lớn |
| **02/12** | **Báo cáo cuối** |

**Không có bằng chứng hiện tại rằng phần Triệu gửi bị sai.** Trace/metric khớp; Triệu đã chấp nhận bản kiểm do assistant thực hiện. Điều này khác việc Triệu tự kiểm độc lập và khác việc duyệt chung pilot. Yêu cầu mới của Trí đã rõ trong kế hoạch V2: Triệu tự chạy evaluator và phân tích, không cần chờ rubric để thực hiện phần được giao; ghi đúng người/ngày/phạm vi.

| Trường hợp chưa đạt | Cách xử lý | Việc Trí vẫn làm được |
|---|---|---|
| Thiếu duyệt chung | Hai người đọc và ghi quyết định ở PILOT_SUMMARY §7; không chạy lại model để thay chữ duyệt | Chuẩn bị dữ liệu và adapter |
| Cần Triệu tự kiểm evaluator độc lập | Triệu đối chiếu ID/GT/count đủ 15 dòng, kiểm công thức và bốn ví dụ nguồn/q05_2, ghi sai khác và kết luận bằng lời của mình; không chỉ ký bản assistant. Không tự đánh dấu đã làm | Chuẩn bị adapter; chưa dùng chữ “kiểm độc lập” trong báo cáo |
| Phát hiện sai ID/GT/công thức thật | Ghi query/file/dòng cụ thể; xác định lỗi nguồn hay evaluator, sửa đúng chỗ có phiên bản; sau sửa mới chấm lại và cập nhật kết luận. Không tự đổi GT để giảm MAE, không train lại model chỉ vì lỗi chấm | Tiếp công việc không phụ thuộc số liệu sai; tạm giữ kết luận bị ảnh hưởng |
| 47 nhãn P4 thiếu hoặc không nhất quán | Hoàn thành ba CSV; mỗi rank có phân loại/object_id hoặc lý do chưa chắc; kiểm target/duplicate nhất quán; cùng xử lý bất đồng, giữ bản trước sửa | Chuẩn bị dữ liệu/runner; kết luận lợi ích chọn đúng vật vẫn ghi tạm |

**Tiêu chí nhận 47 nhãn:** đủ 13/18/16 rank, không đổi thứ tự hoặc box; nhãn đúng/sai tương ứng query; cùng vật có cùng object_id; khung trùng chỉ tới rank hợp lệ; nhãn không chắc có ghi chú; có người/ngày. Không cần ép hai người đồng ý 100% ngay; cần ghi bất đồng và cách phân xử. Nếu reviewer đã xem nhãn assistant trước, ghi rõ điều đó, không gọi là review mù độc lập.

**Mốc mới theo kế hoạch V2: T1 30/10, T2 01/11, T3 02/11, T4 03/11.** Nếu Triệu chưa làm được, Trí có thể tự đối chiếu hoặc nhờ người khác phù hợp kiểm. Ghi đúng người và mức độc lập: Trí tự kiểm không thay bằng chứng hai reviewer. Không chờ vô thời hạn, cũng không nâng nhãn chưa kiểm thành kết luận đã xác nhận. Với lỗi chưa giải quyết, đánh dấu uncertain và báo phạm vi, không loại các ca khó theo kết quả model.

**Việc ngay bây giờ: C1 đã xong (chưa duyệt); Trí chốt quy tắc/lịch sử sử dụng để khóa C2 (nhãn đã xác nhận, C3 đã đạt); Triệu T1–T4.** Chỉ sửa lại đầu việc kiểm chéo cụ thể còn thiếu; không quay lại từ đầu toàn bộ pipeline. Các mốc trên chưa được đánh dấu hoàn thành và chưa được gửi/nhận thay Triệu.

## 6. Câu mở đầu cho session mới

Bản tổng hợp ngay thư mục gốc: [BAT_DAU_SESSION_MOI.md](../BAT_DAU_SESSION_MOI.md). Khi tiến độ thay đổi, bảng “Dừng ở đâu” trong checklist này và WORKLOG là nguồn cập nhật.

Copy nội dung sau, không cần dán lại toàn bộ chat cũ:

> Tiếp tục CS331 tại D:\MINHTRIHOCCODE\HOCKI5\CS331. Đọc README.md, HANDOFF/HANDOFF.md, roadmap/CHECKLIST_3_GIO.md và mục mới nhất của WORKLOG.md; kiểm Git/artifact thực tế rồi bắt đầu ở ô đầu tiên chưa hoàn thành. Đã pull commit d6db189, hợp nhất tài liệu P4 local. CountGD++ vẫn là baseline; CLIP chỉ chấm crop. Triệu đã chấp nhận bản kiểm evaluator 24/10, còn duyệt chung pilot và 47 nhãn q03. Không lặp việc đã có bằng chứng, không đổi freeze, không apply lại stash. Hỏi tôi trước khi chạy evaluator/model/thực nghiệm thay. Sau mỗi mốc, cập nhật checklist, handoff và worklog; kế hoạch chưa chạy phải giữ trạng thái chưa làm.

Không cần giữ session này để đọc được tài liệu đã lưu. Khi chuyển máy/checkout, phải mang theo hoặc commit/push các file local cần thiết; không coi việc xóa chat là thao tác đồng bộ Git.

**Giao việc V2:** T0 chưa xác nhận đã nhận; T1–T4 chưa thực thi trong lượt rà này. Gói chuẩn bị tại HANDOFF/TRIEU_T1_T4_20261027_v2.zip, chưa push/gửi. 47 nhãn q03 không cộng vào điều kiện đóng pilot. Ước lượng tổng cũ cần cộng phần T1–T4 tự kiểm mới, không coi nó là cam kết thời gian mới.
