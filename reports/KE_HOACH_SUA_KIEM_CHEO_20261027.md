# Kế hoạch sửa phần kiểm chéo pilot — V2, 27/10/2026

**Trạng thái: Trí CHƯA DUYỆT phần kiểm chéo.** Bản kiểm 24/10 chủ yếu do assistant làm; Triệu chỉ đọc và chấp nhận. Kế hoạch dưới đây do assistant soạn theo nhận xét của Trí. **Việc kiểm và phân tích phải do Triệu tự làm.** Assistant chỉ chuẩn bị tài liệu, không điền kết quả thay.

## 1. Nhận xét của Trí (27/10/2026, nguyên văn)

> **Kiểm chứng trực tiếp:** Phần kiểm kỹ thuật hiện chủ yếu do AI thực hiện. Bạn cần tự chạy lại chương trình đánh giá, kiểm tra kết quả và lưu bằng chứng chạy thực tế, đặc biệt với các trường hợp dữ liệu lỗi, thiếu hoặc không chắc chắn.
>
> **Phân tích kỹ các mẫu sai:** Tập trung vào q05_2 và q05_3 (thực tế 3 vật nhưng B2 đếm 79). Xác định rõ các khung nhận diện sai loại, đếm trùng hoặc bỏ sót. Những phần đã hậu kiểm thì bổ sung bằng chứng và nguyên nhân còn chưa rõ.
>
> **Giải thích nguyên nhân B2 kém hơn B0:** B0 có MAE = 19,4, còn B2 = 22. Cần phân tích vì sao B2 làm sai số tăng, đặc biệt các trường hợp sai nghiêm trọng, rồi đề xuất hướng cải thiện cụ thể.
>
> **Hoàn thiện báo cáo:** Ghi rõ phần nào đã tự kiểm chứng, kết quả trước/sau kiểm tra và các hạn chế còn tồn tại. Sau đó phối hợp với Trí duyệt báo cáo cuối và thống nhất hướng triển khai P4.

## 2. Kết luận rà soát và phạm vi giao việc

**Giữ T1–T4, sửa cách triển khai và nghiệm thu.** Bốn góp ý có cơ sở, với điểm số P4 được làm rõ: **4.6 là B2 lọc confidence; 6.8 là CLIP-only; 5.8 là Fusion 50/50**, không phải cùng một phương pháp báo hai kết quả.

Đã đọc code evaluator và file tại máy Trí; fetch xác nhận `origin/main` vẫn ở **d6db189**. `CHECKLIST_3_GIO.md`, gói q05, `p4_unseen_v1` và kết quả Fusion có ở máy nhưng chưa được commit/push lên main. Không coi local có file là Triệu đã nhận được.

| Việc | Người làm | Hạn đề xuất | Thời lượng dự kiến | Điều kiện nghiệm thu |
|---|---|---|---|---|
| T0: nhận đủ gói | Trí chuẩn bị, Triệu kiểm nhận | Trước T1 | 15–20 phút | Mở được code/input/ảnh/CSV và biết phiên bản nguồn |
| T1: tự chạy evaluator + 7 ca | Triệu | 30/10 | 1.5–2.5 giờ | Log, exit code, output thực tế, bảng kỳ vọng/thực tế, giải thích tự viết |
| T2: kiểm q05_2/q05_3 | Triệu | 01/11 | 3–5 giờ, chia hai buổi | Đủ nhãn/độ chưa chắc và phân rã count; không ép nhãn để đẹp số |
| T3: phân tích từ T2 | Triệu | **02/11**, sau T2 một ngày | 1–1.5 giờ | Bảng chênh lệch, độ nhạy, quan sát/giả thuyết tách rõ |
| T4: báo cáo và duyệt | Triệu + Trí | **03/11** | 0.5–1 giờ | Bằng chứng liên kết đủ, phần còn bất đồng được ghi, quyết định chung |

Đây là hạn/thời lượng **đề xuất**, chưa ghi Triệu đã nhận hoặc đồng ý. Nếu nhận gói muộn, hai bạn điều chỉnh theo thời gian thực tế và giữ thứ tự phụ thuộc T2 → T3 → T4. Không giữ cùng hạn 01/11 cho cả T2 và T3.

**Phạm vi kết thúc:** 7 ca evaluator, hai query q05 và một báo cáo phân tích; không mở thêm model/train, không yêu cầu chứng minh nguyên nhân nội tại kiến trúc hoặc chạy ablation mới để được nghiệm thu. Mục tiêu tiếp theo là **kiểm chứng cải tiến CountGD++ có hiệu quả hay không**, không mặc định phải ra kết quả tốt.

## 3. T0 — giao đủ đầu vào trước khi tính thời gian làm

Đường giao thay thế cho Git: [TRIEU_T1_T4_20261027_v2.zip](../HANDOFF/TRIEU_T1_T4_20261027_v2.zip), do assistant chuẩn bị, **chưa gửi thay người dùng**. Gói giữ cấu trúc thư mục, có manifest SHA-256 và hướng dẫn trong `DELIVERY_README.md`. Giải nén vào thư mục riêng; không ghi đè checkout đang có thay đổi. Dùng repo Git đã đồng bộ cũng được, nhưng phải có đủ các file tương đương.

**Bắt buộc cho T1–T4:**

- `evaluation/evaluate_pilot.py`; manifest/input pilot; B0 15 dòng và B2 hai file 6+9 dòng; manual q05_2 giữ nguyên.
- Kết quả `pilot_eval_20261020/` để đối chiếu; trace đủ 15 query.
- Gói [q05](../results/countgdpp/q05_error_analysis_package_20261027/README.json): 21 khung B0, 79 khung B2, 3 pseudo, ảnh và 3 CSV trắng. Thêm ảnh gốc mcac_27 và overlay q05_2 để kiểm lại 14 khung.
- Review nguồn và báo cáo/JSON của **cả B2/CLIP CV lẫn Fusion CV**, cùng kế hoạch này.

`p4_unseen_v1` là đầu vào **nhánh Trí/P4**, đang DRAFT; **không phải điều kiện để Triệu chạy T1–T3**. Không phát sinh yêu cầu cài GPU, tải CountGD++ hoặc tải toàn bộ dataset để làm kiểm evaluator/nhãn này. Gói ZIP chỉ bảo đảm tài liệu và đầu vào của T1–T4; các link ngoài phạm vi đó có thể cần checkout đầy đủ.

- [ ] Trí đã chia sẻ ZIP hoặc commit chứa đủ đầu vào; ghi nơi gửi/commit/hash thực tế.
- [ ] Triệu giải nén/checkout, kiểm manifest và mở được file; ghi ngày nhận, máy/OS/Python.
- [ ] Nếu thiếu file/hỏng hash thì xử lý giao nhận trước; không ghi lỗi môi trường/thiếu đầu vào thành lỗi evaluator.

## 4. T1 — tự chạy evaluator và 7 tình huống có kiểm soát

**Không sửa evaluator trong vòng này.** Code CLI luôn gọi `manual_check` sau `evaluate`, nên ca 1–3 dòng bỏ q05_2 có thể lỗi ở phần không định thử. Cách sửa kế hoạch: **mỗi fixture là bản sao đầy đủ 15 query**, chỉ thay q01_1, giữ q05_2 nguyên vẹn. Bản full pilot tự chạy đóng vai trò ca đối chứng trước 7 tình huống.

### T1A. Lệnh chạy thật và lưu bằng chứng

Chạy **Bash trong Ubuntu/WSL**, tại thư mục gốc dự án hoặc thư mục gốc gói giải nén có `evaluation/`. Dùng Python 3 hệ thống; không cần GPU. Với checkout của Trí, lệnh chuyển thư mục là `cd /mnt/d/MINHTRIHOCCODE/HOCKI5/CS331`; máy Triệu dùng đúng đường dẫn của mình.

```bash
# Tạo thư mục cha trước khi redirect stdout; không tạo trước pilot_eval_rerun.
run_dir="reports/audits/trieu_rerun_$(date +%Y%m%d_%H%M%S)"
mkdir -p "$run_dir/fixtures" "$run_dir/cases"
python3 --version > "$run_dir/environment.txt" 2>&1

if python3 evaluation/evaluate_pilot.py --self-test > "$run_dir/selftest_stdout.txt" 2>&1; then
  rc=0
else
  rc=$?
fi
printf '%s\n' "$rc" > "$run_dir/selftest_exit_code.txt"
cat "$run_dir/selftest_stdout.txt"
```

Triệu đọc stdout; **chỉ chạy khối tiếp khi exit code = 0 và có SELF-TEST PASS**. Self-test có sẵn không thay đủ 7 tình huống được ghi riêng; trong code hiện tại chưa thấy ca `uncertain` trong self-test.

```bash
if python3 evaluation/evaluate_pilot.py \
  --out "$run_dir/pilot_eval_rerun" \
  > "$run_dir/eval_stdout.txt" 2>&1; then
  rc=0
else
  rc=$?
fi
printf '%s\n' "$rc" > "$run_dir/eval_exit_code.txt"
cat "$run_dir/eval_stdout.txt"
```

**Kỳ vọng cho dữ liệu thật:** exit 0, đủ 5 output; paired=15, MAE B0/B2=19.4/22.0, RMSE≈24.315976/30.090973, exact=1/15 mỗi bên. Đối chiếu nội dung `metrics.json`, `per_query.json`, `manual_check.json` với run 20/10; `run_config` có command/output khác là bình thường. Không ép toàn bộ file metadata phải giống byte. Ghi máy/OS, ngày/người chạy, commit Git hoặc hash manifest ZIP trong ghi chú; các script/log thật là bằng chứng, không dùng ảnh chụp màn hình thay toàn bộ log.

### T1B. Triệu tự tạo 7 fixture từ cùng một bản sạch

Trong mỗi `fixtures/<case_id>/`, tạo `manifest.csv`, `inputs.jsonl`, `b0.jsonl`, `b2.jsonl`:

- Copy manifest gốc (30 dòng cũng hợp lệ) và input first5 (15 query).
- B0 copy đủ 15 query; B2 gộp hai nguồn 6+9 dòng, mỗi ID đúng một lần. Giữ `variant`, schema và tất cả field hợp lệ trước khi sửa tình huống đang thử.
- **Không thay dòng q05_2 của B2:** giữ `run_id`, box/index/count để khớp manual review gốc. Không sửa manual review.
- Mỗi ca bắt đầu từ bản sạch, không cộng dồn mutation. Chỉ sửa **q01_1** như bảng. Manifest vẫn `split=dev` vì evaluator này chỉ nhận dev.
- Ghi rõ fixture là **dữ liệu giả để kiểm code**, không phải prediction/GT thực tế; không ghi đè nguồn hoặc đưa metric fixture vào báo cáo hiệu quả model.

| case_id | Chỉ thay gì? | Kỳ vọng phải kiểm |
|---|---|---|
| `execution_error` | B2 q01_1: status `error`, count `null`; có thể để box/score rỗng | Exit 0; B2 errors=1, valid=14, paired=14; q01_1 không được zero-fill |
| `error_with_count` | B2 q01_1: status `error`, giữ count=25 | Exit khác 0; `EVALUATION STOP`, lý do `error phải có final_count=null` |
| `missing_query` | Xóa q01_1 khỏi B2, giữ nguyên inputs | Exit khác 0; thiếu ID B2, không phải lỗi manual q05_2 |
| `duplicate_id` | Thêm bản sao q01_1 vào B2 | Exit khác 0; ID trùng |
| `count_mismatch` | Tăng count q01_1 B2 25→26, giữ 25 box/score | Exit khác 0; count khác số box/score |
| `uncertain_gt` | Manifest q01_1: presence `uncertain`; có thể để gt_count trống. Predictions vẫn hợp lệ | Exit 0; eligible=14, paired=14; uncertain_excluded chứa đúng ID này, không tính như absent |
| `absent_prediction` | Manifest q01_1: presence `absent`, gt_count=0; **cả B0/B2** count=2 và chỉ giữ 2 box/score tương ứng | Exit 0; n_absent=1, FPR_absent=1.0, MeanAbsentCount=2.0 ở cả hai; paired=15 |

Trong bảng, `status`, `count`, `box/score`, `presence` lần lượt là các field `execution_status`, `final_count`, `final_boxes`/`final_scores`, `presence_status`. Với ca absent, cắt cùng hai phần tử đầu của cả boxes và scores. Không đổi các field khác.

Kỳ vọng trên suy từ code, **chưa phải kết quả đã chạy**. Ca dữ liệu hỏng được coi là kiểm thành công nếu code từ chối đúng lý do dự kiến. Crash do thiếu file/import hay lỗi manual q05_2 không đạt ca đó.

Sau khi tự tạo đủ fixture, chạy mỗi ca và lưu exit code; khối `if` cho phép các ca dự kiến bị từ chối vẫn có log và không làm dừng vòng lặp:

```bash
for case_id in execution_error error_with_count missing_query duplicate_id count_mismatch uncertain_gt absent_prediction; do
  case_dir="$run_dir/fixtures/$case_id"
  log_dir="$run_dir/cases/$case_id"
  mkdir -p "$log_dir"
  if python3 evaluation/evaluate_pilot.py \
    --manifest "$case_dir/manifest.csv" \
    --inputs "$case_dir/inputs.jsonl" \
    --b0 "$case_dir/b0.jsonl" \
    --b2 "$case_dir/b2.jsonl" \
    --manual-review results/countgdpp/b2_remaining3_20261015/q05_2/manual_crosscheck_20261016.json \
    --out "$log_dir/output" > "$log_dir/stdout_stderr.txt" 2>&1; then
    rc=0
  else
    rc=$?
  fi
  printf '%s\n' "$rc" > "$log_dir/exit_code.txt"
done
```

Không tạo trước `output` hoặc `pilot_eval_rerun`; evaluator từ chối thư mục đã tồn tại. Khi chạy lại, tạo `run_dir` mới. Nếu mở terminal mới, đặt lại `run_dir` đúng lượt cần tiếp; không vô tình ghi đè log.

**Triệu bàn giao:** `CASE_RESULTS.md` có case/kỳ vọng/thực tế/exit code/đường dẫn log/đạt-chưa đạt; toàn bộ fixtures và output; 5–10 dòng tự giải thích điều đã kiểm. Assistant không chạy hoặc điền kết quả thay Triệu. Nếu có lỗi thật, lưu bằng chứng, sửa có phiên bản rồi mới chạy lại ca liên quan và dữ liệu thật.

## 5. T2 — phân tích hai query, quy tắc nhãn đủ rõ để cộng lại được

Phạm vi: **q05_3 = 100 box kết quả (21 B0 + 79 B2) + 3 pseudo; q05_2 = kiểm lại 14 box có nhãn**, tổng khoảng 117 lượt xem. Chia hai buổi; thời gian 2–3 giờ ban đầu có thể quá sát. Không mở review toàn bộ dataset.

Triệu copy CSV trắng sang thư mục output của mình, giữ file BLANK gốc. Dùng `rank` một-based trên overlay; không trộn với `prediction_index` zero-based trong manual JSON. Mỗi dòng có người/ngày và ghi chú khi chưa chắc. Giữ nguyên tọa độ/score gốc.

### Quy tắc một nhãn chính mỗi box

| Nhãn | Cách dùng để tránh đếm hai lần |
|---|---|
| `background` | Không có vật đếm được trong box |
| `wrong_class` | Box nhận dạng vật thuộc loại khác; ghi actual_class. Dù box sai loại lặp nhau, vẫn tính vào nhãn chính wrong_class |
| `part` | Chỉ khoanh phần/hạt của blackberry, không phải cả một quả; ghi object_id quả chứa phần đó nếu biết |
| `target` | Khoanh cả một quả blackberry; dùng một box đại diện cho mỗi quả trong từng stage |
| `duplicate` | Box bổ sung cũng khoanh cả chính quả đã có đại diện target trong stage đó; ghi cùng object_id |
| `uncertain` | Không phân biệt được hoặc box bao nhiều quả mà chưa quy được một vật; ghi lý do, `uncertain=true`; không đoán để đủ bảng |

Sau khi phân loại cả quả, chọn **rank nhỏ nhất trong các box đủ điều kiện cùng object_id** làm target, các box đủ điều kiện còn lại là duplicate. Không chọn đại diện bằng score để thuận lợi cho một phương pháp. Part/wrong_class không đồng thời cộng duplicate. Dùng ID ba quả, ví dụ `blackberry_1..3`, nhất quán giữa B0/B2 và ghi bằng chứng trên ảnh. Pseudo dùng cùng tiêu chí mô tả nhưng không cộng vào tổng count B0/B2; pseudo bao nhiều quả phải ghi rõ.

1. Điền đủ 21/79/3 dòng. Được để nhãn uncertain có lý do, nhưng không để dòng chưa xem trống rồi ghi review xong.
2. Lập bảng: `21 hoặc 79 = target + duplicate + part + wrong_class + background + uncertain`. Đếm vật mục tiêu phân biệt từ object_id; không đồng nhất số box với số quả.
3. Bỏ sót: trong 3 quả, quả nào không có box đủ điều kiện target? Nếu chỉ có part thì vẫn chưa có box cả quả. Nếu còn uncertain ảnh hưởng kết luận thì báo phạm vi chưa xác nhận.
4. So bảng phân rã B0/B2: phần tăng 21→79 chủ yếu ở nhóm nào theo nhãn của Triệu? Mỗi nhận xét lớn có rank và ảnh/crop minh họa. Diện tích pseudo là metadata, không tự chứng minh nguyên nhân.
5. q05_2: tự xem lại 14 box và nhãn 16/10; ghi phần xác nhận/khác biệt. Mốc cũ 14 = 4 vật đúng + 1 khung trùng + 9 sai loại là **tham chiếu**, không bắt nhãn mới phải khớp nếu quan sát có bằng chứng khác.

**Xong khi:** CSV đủ hàng, tổng cộng khớp, object_id nhất quán, có danh sách bỏ sót/uncertain và minh chứng. Đầu ra có thể là “chưa rõ cơ chế”; không bắt chứng minh mọi giả thuyết. Bất đồng phải được ghi để hai người phân xử ở T4.

## 6. T3 — phân tích có giới hạn, không viết kết luận trước dữ liệu

Làm sau bản T2 hoàn chỉnh hoặc bản T2 đã ghi rõ mọi ca chưa chắc. Bắt đầu phần số học trước được, nhưng phần diễn giải hoàn tất **02/11**, sau T2 một ngày.

Nguồn: [trace 15 query](audits/PER_QUERY_TRACE_20261024.csv), [review pseudo](<../workspace Trí and Triệu/Triệu/TRIEU_VISUAL_REVIEW.md>), đầu ra T2. Mốc **đã đối chiếu từ trace**, để kiểm cách tính:

- Tổng sai số tuyệt đối: B0=291, B2=330, chênh **+39**.
- Riêng q05_3: 18→76, chênh **+58**.
- Còn lại 14 query: 273→254, chênh **−19**. Do đó không được viết “B2 luôn kém B0”.

Triệu tự lập bảng delta từng query, sắp theo mức tăng; tự giải thích tác động của q05_3. Phân tích độ nhạy tối thiểu là bỏ riêng q05_3: B0=273/14=19.5, B2=254/14≈18.142857. **Đây chỉ là sensitivity diagnostic**, không thay số chính 19.4/22.0 và không loại ca xấu khỏi kết quả.

Dùng nhãn T2 để liên hệ: đếm phần quả, sai loại, trùng, box bao nhiều vật hoặc bỏ sót. So nhóm pseudo đúng/sai là quan sát trên ít ảnh dev, không chứng minh quan hệ nhân quả. Chia bài viết thành **số liệu → quan sát có rank minh chứng → giả thuyết chưa kiểm → đề xuất**. Không bắt chạy thêm ablation để phân tích này được nghiệm thu.

### Gọi đúng tên số liệu P4

| Cấu hình trên cùng 5 ảnh dev, CV theo ảnh | MAE | Nguồn |
|---|---:|---|
| B2 gốc | 22.0 | [B2/CLIP CV](../results/countgdpp/p4_count_cv_20261020/report.json) |
| B2 chỉ lọc confidence | **4.6** | Cùng nguồn trên |
| CLIP-only filter | **6.8** | Cùng nguồn trên |
| Fusion 50/50 (B2 + CLIP chuẩn hóa) | **5.8** | [Fusion CV](../results/countgdpp/p4_fixed_fusion_cv_20261021/report.json) |

Không gọi 5.8 là CLIP-only. Dev-fit 4.333333/4.4 trong freeze là loại điểm khác, không thay CV. **P4.6 chưa chạy/chấm trên ảnh mới**: mới có DRAFT dữ liệu và kiểm áp dụng freeze trên điểm dev lưu sẵn; không viết “đang kiểm trên tập mới” như một kết quả đã có.

**Đầu ra:** một báo cáo ngắn 1–2 trang có bảng delta, sensitivity, 2–3 giải thích/đề xuất gắn bằng chứng. Có thể đề xuất kiểm chất lượng pseudo hoặc chống đếm phần quả, nhưng đánh dấu chưa thử. Không cần chứng minh Fusion thắng đối chứng hoặc tạo thêm nhánh nghiên cứu trong T3.

## 7. T4 — nghiệm thu chung, kết thúc vòng kiểm chéo

Triệu ghi “Phần Triệu tự kiểm chứng” trong PILOT_SUMMARY, liên kết bằng chứng **đã chạy/đã gán thật**, phân biệt với các bản assistant ngày 24/10. Không thay bản cũ hoặc ký thay người khác.

**Bốn gói bàn giao:**

1. T1: môi trường, self-test, rerun thật, 7 fixture/log/exit code, CASE_RESULTS và giải thích tự viết.
2. T2: ba CSV q05_3, bảng/ghi chú đối chiếu q05_2, phân rã/bỏ sót/uncertain và ảnh minh chứng.
3. T3: delta 15 query, độ nhạy q05_3, phân tích quan sát/giả thuyết và đề xuất có nguồn.
4. T4: PILOT_SUMMARY cập nhật và phiếu duyệt chung.

Trí kiểm: đường dẫn mở được, log có nội dung/exit code thật, tổng nhãn khớp và không còn lỗi chấm ảnh hưởng số liệu. Hai bạn xem các ca bất đồng quan trọng; ghi nhãn đã thống nhất hoặc giới hạn còn lại. Chưa biết nguyên nhân nội tại không tự động làm T3 “không đạt”. Không nhận nhãn chưa xem chỉ để hoàn thành hạn.

- [ ] T0: Triệu đã nhận đủ đầu vào và kiểm được.
- [ ] T1: Triệu tự chạy, 7 ca có kết quả đúng lý do hoặc lỗi thật đã xử lý và kiểm lại.
- [ ] T2: đủ nhãn/bảng; bất đồng/uncertain đã ghi, không giấu số chưa rõ.
- [ ] T3: số liệu đúng, tên cấu hình đúng, không suy tương quan thành nguyên nhân.
- [ ] T4: hai người ghi tên/ngày/quyết định; **pilot chỉ được đóng sau quyết định này**.

**Giới hạn vòng sửa:** nếu thiếu, Trí chỉ rõ hàng/file/log cần bổ sung; một lượt chỉnh tập trung, không tự thêm query/model/đối chứng mới vào điều kiện đóng. **47 nhãn q03 là việc P4 riêng**, không cộng thêm vào gate đóng pilot T1–T4. Sau nghiệm thu chuyển trọng tâm sang P4.6, đo hiệu quả và cả đánh đổi/kết quả âm.

## 8. Trí làm song song và trạng thái tiếp tục

- **C1 đã xong:** Trí đã đọc, **chưa duyệt**, yêu cầu T1–T4. Không quay lại ghi C1 chưa làm hoặc bỏ yêu cầu mới vì Triệu từng chấp nhận audit 24/10.
- **C2:** phương án B; [p4_unseen_v1](../experiments/countgdpp/p4_unseen_v1/README.md) đã có DRAFT 10 ảnh/30 query. Trí kiểm absent/GT/quy tắc chấm rồi khóa; không coi tên `unseen` hay manifest `test` là bằng chứng tập đã sẵn sàng.
- **C3:** adapter đã viết; [kiểm dev bước (1)](../results/countgdpp/p4_freeze_devcheck_20261027/run_config.json) áp dụng freeze trên điểm cũ khớp 15/15. Bước (2) B2, (3) CLIP, (4) áp dụng freeze trên điểm mới vẫn cần kiểm; không gọi toàn runner đạt.
- Chuẩn bị dữ liệu/kiểm triển khai có thể làm song song T1–T3. Chỉ mở đánh giá ảnh mới khi dữ liệu đã khóa và kiểm dev đạt. Không thay freeze hoặc dùng GT test vào model/bộ lọc.
- Không coi point-in-box đơn thuần là chứng minh box đếm đúng loại; quy tắc matching/nhãn dùng cho kết luận chọn đúng vật cần chốt trước N4.

**Trạng thái V2:** kế hoạch và gói bàn giao đã chuẩn bị, chưa có bằng chứng Triệu nhận/chạy/hoàn thành T1–T4; chưa commit/push hoặc gửi tin thay người dùng. Assistant lượt sửa này chỉ đọc code/file, kiểm số học, chuẩn bị tài liệu/gói, không chạy evaluator/self-test/model và không điền nhãn/kết luận thay Triệu.
