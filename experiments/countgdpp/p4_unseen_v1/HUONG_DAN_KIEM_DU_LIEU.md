# C2 — Trí tự kiểm 10 ảnh trước khi khóa tập

**Ngày chuẩn bị: 27/10/2026. Trạng thái: DRAFT_NOT_LOCKED.** Đây là hướng dẫn và ảnh hiển thị điểm có sẵn từ MUCCA. Không có model inference, nhãn mới hoặc xác nhận thay Trí. Chưa chọn xong absent, chưa xác nhận GT và chưa chốt quy tắc chấm.

**Cập nhật sau khi Trí kiểm, 27/10:** đã ghi 10 absent_ok và xác nhận 20 GT present theo [tin nhắn của Trí](human_review_20261027.json). Không phải bước kiểm độc lập của assistant. Các bước 2–3 bên dưới giữ để tham khảo; việc còn lại là chốt quy tắc, lịch sử sử dụng và khóa tập.

## 1. Mở ảnh đúng chỗ

Làm trên Windows, không cần vào Ubuntu hoặc bật GPU. Mở hướng dẫn này và hai file CSV bằng trình soạn thảo bạn quen dùng. Nếu dùng Excel, giữ định dạng CSV UTF-8 phân cách bằng dấu phẩy; không đổi tên thành xlsx. Không bỏ dấu ngoặc kép đang bao ô có dấu phẩy.

Xem ảnh gốc/phóng to để kiểm absent; xem ảnh chấm GT để đối chiếu hai lớp present. Ảnh GT có hai nửa: mỗi nửa là một lớp, số thứ tự đặt cạnh điểm nguồn. Chấm GT không chứng minh nhãn nguồn đúng; ảnh gốc giúp kiểm vị trí bị chấm che hoặc vật bị bỏ sót. Ảnh liên kết vẫn là kích thước gốc; có thể cần mở toàn ảnh và zoom.

| Ảnh | Để kiểm absent | Để kiểm GT present | Số điểm nguồn, chưa xác nhận | Absent đang đề xuất |
|---|---|---|---|---|
| mcac_123 | [Ảnh gốc](../../../data_external/mucca_zenodo_19231375/MUCCA_1.0/images/mcac_123.jpg) | [Hai lớp có chấm GT](gt_review_images/mcac_123_GT.jpg) | people=10; dogs=27 | sheeps |
| mcac_121 | [Ảnh gốc](../../../data_external/mucca_zenodo_19231375/MUCCA_1.0/images/mcac_121.jpg) | [Hai lớp có chấm GT](gt_review_images/mcac_121_GT.jpg) | people=3; dogs=20 | cats |
| mcac_109 | [Ảnh gốc](../../../data_external/mucca_zenodo_19231375/MUCCA_1.0/images/mcac_109.jpg) | [Hai lớp có chấm GT](gt_review_images/mcac_109_GT.jpg) | people=3; amplifiers=4 | bicycles |
| mcac_110 | [Ảnh gốc](../../../data_external/mucca_zenodo_19231375/MUCCA_1.0/images/mcac_110.jpg) | [Hai lớp có chấm GT](gt_review_images/mcac_110_GT.jpg) | people=4; guitars=7 | amplifiers |
| mcac_63 | [Ảnh gốc](../../../data_external/mucca_zenodo_19231375/MUCCA_1.0/images/mcac_63.jpg) | [Hai lớp có chấm GT](gt_review_images/mcac_63_GT.jpg) | chairs=3; beach umbrellas=24 | forks |
| mcac_61 | [Ảnh gốc](../../../data_external/mucca_zenodo_19231375/MUCCA_1.0/images/mcac_61.jpg) | [Hai lớp có chấm GT](gt_review_images/mcac_61_GT.jpg) | chairs=23; beach umbrellas=30 | blackberries |
| mcac_88 | [Ảnh gốc](../../../data_external/mucca_zenodo_19231375/MUCCA_1.0/images/mcac_88.jpg) | [Hai lớp có chấm GT](gt_review_images/mcac_88_GT.jpg) | people=6; cars=22 | trucks |
| mcac_72 | [Ảnh gốc](../../../data_external/mucca_zenodo_19231375/MUCCA_1.0/images/mcac_72.jpg) | [Hai lớp có chấm GT](gt_review_images/mcac_72_GT.jpg) | people=7; cars=14 | boats |
| mcac_227 | [Ảnh gốc](../../../data_external/mucca_zenodo_19231375/MUCCA_1.0/images/mcac_227.jpg) | [Hai lớp có chấm GT](gt_review_images/mcac_227_GT.jpg) | people=30; boats=8 | trucks |
| mcac_84 | [Ảnh gốc](../../../data_external/mucca_zenodo_19231375/MUCCA_1.0/images/mcac_84.jpg) | [Hai lớp có chấm GT](gt_review_images/mcac_84_GT.jpg) | people=27; motorbikes=17 | trucks |

## 2. Kiểm absent — 10 dòng

Mở [absent_candidates.csv](absent_candidates.csv). Mỗi ảnh làm tuần tự:

1. Đọc `proposed_absent`, mở ảnh gốc và rà toàn ảnh, kể cả vật nhỏ/che khuất. Đây là hỏi “loại này có xuất hiện không?”, không phải xem model có khoanh nó không.
2. Nếu chắc chắn không có: `human_check=absent_ok`; `checked_by=Trí`; `date=ngày bạn thực sự kiểm` theo YYYY-MM-DD; `note` mô tả ngắn căn cứ/giới hạn.
3. Nếu có: `human_check=visible`, điền tên/ngày và mô tả vị trí. Đọc `next_candidates` từ trái sang phải; từng lớp thay thế cũng phải được xem ảnh xác nhận. Không tự lấy lớp kế tiếp và mặc định nó vắng mặt.
4. Nếu chưa phân biệt được: giữ `PENDING`, điền tên/ngày và ghi “chưa chắc ...” trong note. Đừng ghi absent_ok để đủ tiến độ. Chưa khóa tập khi câu hỏi absent cuối còn chưa rõ.

**Ví dụ giả định, không phải nhãn cho ảnh thật:** nếu đã kiểm mcac_123 và không thấy sheep, có thể điền `absent_ok`, `Trí`, ngày kiểm và `Da ra toan anh; khong thay sheep`. Chỉ điền nếu đó là quan sát của bạn.

**Khi đổi absent:** trước tiên ghi vào note dạng `Cu: trucks; quan sat: ...; de xuat moi: bicycles; ket qua kiem lop moi: ...`. Giữ ghi nhận này và bản sao trước sửa. Không tự chuyển trucks thành bicycles chỉ vì một ví dụ trong tài liệu.

Sau khi xác nhận lớp thay thế thật sự absent, đồng bộ bằng `image_id` + `query_id`:

| File | Field cần đồng bộ |
|---|---|
| absent_candidates.csv | proposed_absent = tên lớp mới trong mapping; human_check=absent_ok cho lớp cuối; note giữ lớp cũ/lý do/kết quả kiểm lớp mới; checked_by/date thật |
| manifest.csv | Dòng có presence_status=absent của đúng ảnh: class_id, target_class, prompt; giữ gt_count=0, presence_status=absent và ID. verified_by ghi người/ngày; uncertainty_note phản ánh kiểm thật |
| inputs.jsonl | Dòng cùng query_id: chỉ đổi prompt tương ứng, không thêm GT |

Mã/tên lớp lấy ở [class_mapping.json](../../../data_external/mucca_zenodo_19231375/MUCCA_1.0/class_mapping.json); không tự đoán mã. `sheeps` trong tên lớp dùng prompt `sheep`, `cigaretts` dùng prompt `cigarettes` theo prompt_fix có sẵn; các lớp khác giữ cách gọi đã quy định. Nếu lớp thay khác siêu nhóm, cập nhật proposed_type cho đúng; ghi rõ đó là thay sau kiểm người, không phải đầu ra gốc của bộ chọn r2. Không sửa quy tắc/seed lịch sử.

**Ưu tiên hôm nay:** làm hai ảnh đầu để quen thao tác; sau đó kiểm kỹ trucks ở mcac_88 và mcac_84. Gợi ý của assistant chưa phải xác nhận chúng có hoặc không có xe tải.

## 3. Kiểm GT present — 20 dòng

GT là số lượng chuẩn để chấm model; ở bản nháp đang bằng số điểm MUCCA. Mở [manifest.csv](manifest.csv), chỉ tìm 20 dòng presence_status=present. Mỗi dòng:

1. Mở ảnh GT đúng image_id và lớp. Mỗi điểm phải gắn với một vật đúng loại; xem có điểm đặt nhầm, lặp một vật hoặc vật nhìn thấy mà thiếu điểm không. Rà thêm ảnh gốc, không chỉ đếm số chấm.
2. Đối chiếu số vật với gt_count. Nếu kiểm được và đồng ý: thay verified_by=PENDING... bằng `Trí | YYYY-MM-DD | visual_checked`; uncertainty_note ghi `Da doi chieu anh va diem nguon; khong thay bat dong`. Đây chỉ là kiểm của Trí, không phải hai reviewer.
3. Nếu khác/chưa rõ: verified_by ghi `Trí | YYYY-MM-DD | needs_review`; uncertainty_note ghi cụ thể số/điểm/vị trí bạn thấy, ví dụ “nguồn 3, tôi chỉ thấy chắc 2; cần xem điểm số 3”. Giữ gt_count và annotation nguồn nguyên trạng lúc này.
4. Với bất đồng ảnh hưởng count/loại, dừng khóa cho đến khi xử lý có bằng chứng hoặc chốt quy tắc uncertain trước đánh giá. Không chọn cách xử lý theo output model vì bộ này chưa chạy.

Đặc biệt xem chairs=3 ở mcac_63 và people=3 ở mcac_121. Không đánh dấu tất cả verified chỉ vì số chấm vẽ ra khớp manifest; đó là cùng một nguồn dữ liệu.

## 4. Chốt cách chấm — trước khi đánh giá, chưa làm gán nhãn output ngay

Phần này là **đề xuất cần Trí chốt**, chưa có xác nhận đồng ý. Dùng một quy ước cho cả B2 gốc, B2 lọc confidence và Fusion.

- Đơn vị là cả vật (một người, một ghế, một quả...), không đếm bộ phận như một vật mới. Quy ước vật che khuất phải phù hợp GT; ca không đủ căn cứ được ghi chưa chắc.
- Chấm count bằng GT đã kiểm: sai số số lượng không đủ chứng minh model chọn đúng loại.
- Khi review khung ở N4: kiểm đúng loại và đúng đơn vị trước, rồi gán một object_id nếu xác định được. Mỗi khung chỉ ghép tối đa một vật, mỗi vật chỉ được tính đúng một lần. Khung bao nhiều vật không được nhận nhiều true positives; ghi riêng multi_object/uncertain.
- Nếu nhiều khung hợp lệ cùng một vật: dùng rank nhỏ nhất của candidate B2 gốc trong các khung còn giữ làm đại diện, các khung còn lại là trùng. Quy tắc cố định giữa các phương pháp; không chọn đại diện bằng score để thuận lợi cho phương pháp đang kiểm.
- Sai loại, chỉ khoanh bộ phận, nền và chưa chắc phải được ghi riêng. Vật không có khung hợp lệ là bỏ sót.
- **Điểm GT nằm trong khung chỉ hỗ trợ tìm vật để đối chiếu.** Khung rất rộng hoặc khoanh sai loại vẫn có thể chứa điểm. Vì chỉ có point GT, không gọi kết quả này là AP/IoU bbox chuẩn.

Trong WORKLOG ghi phiên bản quy ước bạn đồng ý, người/ngày hoặc điểm muốn sửa. Không dùng việc tài liệu đã có đoạn đề xuất làm bằng chứng bạn đã chốt.

## 5. Khóa tập — bước cuối, không chỉ đổi một chữ

Chỉ làm khi: 10 câu absent cuối đã được xác nhận; 20 GT present đã kiểm/giải quyết bất đồng; đã xác nhận lịch sử sử dụng và không dùng các ảnh này để chọn ngưỡng/prompt/phương pháp; ID/lớp/prompt của các file khớp; quy tắc chấm và uncertain đã chốt. Bộ nháp sàng lọc bằng annotation không có nghĩa là mô hình chưa từng thấy ảnh trong pretraining; chỉ xác nhận đây là ảnh chưa dùng phát triển phương pháp của nhóm.

1. Sao lưu bản DRAFT trước sửa cuối; giữ lịch sử đổi lớp/GT. Ghi rõ nếu sau này phải tạo bản v2 do phát hiện lỗi, không sửa lặng lẽ một bản đã chạy.
2. Đối chiếu tổng 10 ảnh / 30 query, 20 present / 10 absent; mỗi ID đúng một lần và prompt giữa inputs/manifest khớp. Tên/mã lớp nhất quán. Kiểm hash ảnh vẫn khớp selection_meta.
3. Đổi selection_meta.json status từ DRAFT_NOT_LOCKED thành LOCKED; thêm locked_by, locked_at (thời điểm thật), review_protocol (phiên bản quy tắc đã đồng ý). Chưa xác nhận thì giữ DRAFT. Đây là bước người dùng ký xác nhận, không tự động do assistant.
4. Lấy hash các file cuối bằng PowerShell bên dưới, ghi đầy đủ hash và người/ngày vào WORKLOG. Ít nhất inputs và manifest; lưu thêm absent/selection_meta để giữ bằng chứng phiên bản.

```powershell
Set-Location -LiteralPath 'D:\MINHTRIHOCCODE\HOCKI5\CS331'
Get-FileHash -Algorithm SHA256 -LiteralPath @(
  'experiments/countgdpp/p4_unseen_v1/inputs.jsonl',
  'experiments/countgdpp/p4_unseen_v1/manifest.csv',
  'experiments/countgdpp/p4_unseen_v1/absent_candidates.csv',
  'experiments/countgdpp/p4_unseen_v1/selection_meta.json'
) | Format-List Path, Hash
```

Đổi status không phải bảo vệ kỹ thuật tự động; runner hiện chưa đọc selection_meta để bắt buộc LOCKED. Nhóm phải tuân thủ bước kiểm trước chạy. **Khóa dữ liệu xong chưa đồng nghĩa được chạy ngay ảnh mới: C3 kiểm dev (2)–(4) cũng phải đạt.** Hướng dẫn này không chạy evaluator/model, không thay freeze và không ký thay bạn.

## Điểm dừng đầu tiên để bạn tự làm

Làm mcac_123 và mcac_121: 2 dòng absent + 4 dòng present. Nếu còn mơ hồ, ghi PENDING/needs_review và vị trí cần xem, rồi dừng ở đó; không phải hoàn thành/khóa cả bộ trong một lần. Sau đó làm tám ảnh còn lại theo cùng cách. Các file vẫn DRAFT cho đến khi đủ điều kiện trên.
