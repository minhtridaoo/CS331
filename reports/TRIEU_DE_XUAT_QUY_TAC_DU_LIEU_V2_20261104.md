# Đề xuất quy tắc rút tập dev/test mới (v2) cho nhánh P (04/11/2026)

**Người đề xuất:** Triệu. **Bản nháp:** Claude soạn script và văn bản theo yêu cầu của Triệu, dựa trên §4 của [KE_HOACH_CAI_TIEN_20261027.md](../roadmap/KE_HOACH_CAI_TIEN_20261027.md) và §5.1 kế hoạch của Trí. **Cần Trí:** duyệt quy tắc và trả lời 5 câu ở mục 4 **trước khi rút ảnh**. Chưa rút ảnh thật nào.

## 1. Tóm tắt

- Script mới: [experiments/countgdpp/select_dev_test_v2.py](../experiments/countgdpp/select_dev_test_v2.py). Chỉ đọc nhãn MUCCA, không đọc output model nào. Script v1 (`p4_select_unseen.py`) và tập `p4_unseen_v1` giữ nguyên.
- MUCCA còn **185 ảnh chưa dùng**: đã bỏ 5 ảnh pilot và 10 ảnh `p4_unseen_v1` (10 ảnh này chỉ dùng phân tích lỗi và demo).
- Nếu chỉ lấy cặp **khác hẳn** (khác siêu nhóm) thì chỉ có **19 ảnh**. Muốn có 60–80 ảnh thì phải thêm cặp **dễ nhầm** (cùng siêu nhóm). Có 90 ảnh như vậy.
- Đã chạy thử bằng seed chỉ dùng để kiểm (không phải seed thật) cho cả 20+40 và 30+50: đạt mọi bài kiểm (mục 3). Kết quả rút thử đã xóa.

## 2. Quy tắc đề xuất

1. **Pool:** MUCCA 1.0 (Zenodo 19231375; kiểm md5 của zip và sha256 của file nhãn) trừ 5 ảnh pilot và 10 ảnh `p4_unseen_v1`.
2. **Mỗi ảnh một cặp có mặt (X, Y)**, mỗi lớp 3–40 điểm (để người kiểm bằng mắt được).
   - **Khác hẳn:** X, Y khác siêu nhóm, đúng câu hỏi của thầy. **Lấy hết** ảnh đủ điều kiện.
   - **Dễ nhầm:** X, Y cùng siêu nhóm (trái cây, bát đĩa, chìa khóa/ổ khóa…). Chỉ dùng cho ảnh không có cặp khác hẳn. Rút xoay vòng qua các siêu nhóm cho đến khi đủ số ảnh, nên nhóm nào cũng có mặt.
   - Chọn cặp trong một ảnh giống v1: ưu tiên cặp không có `people`, rồi cặp mà lớp ít điểm hơn vẫn có nhiều điểm nhất, rồi theo id lớp.
3. **Chia dev/test theo ảnh.** Chia đúng tỉ lệ theo loại cặp trước, rồi theo nhóm siêu nhóm bên trong mỗi loại (largest remainder); mỗi nhóm xáo bằng seed.
4. **Một truy vấn vắng mặt mỗi ảnh**, giống v1. Ưu tiên loại "khó": lớp cùng siêu nhóm với Y mà ảnh không có nhãn. Không có thì lấy loại "dễ". **Người phải xác nhận bằng mắt** là vật đó thật sự vắng. Tùy chọn `--easy-absent` thêm một truy vấn vắng mặt loại dễ (§5.1 của Trí: "nếu đủ nguồn lực").
5. **Output** (trạng thái `DRAFT_NOT_LOCKED`): `dev/` và `test/`, mỗi thư mục có `inputs.jsonl` (không có GT) và `manifest.csv` (cho evaluator); thêm `absent_candidates.csv` có cột để người kiểm điền, và `selection_meta.json` (quy tắc, seed, các nhóm, hash ảnh, hash script). Script không ghi đè thư mục đã có.

**Số ảnh đủ điều kiện (đã chạy `--stats`):**

| loại | số ảnh | chi tiết |
|---|---|---|
| khác hẳn | 19 | người–xe 13, người–động vật 4, người–nhạc cụ 1, ghế–ô bãi biển 1 |
| dễ nhầm | 90 | trái cây 24, bát đĩa 19, chìa khóa/ổ khóa 10, xe 8, ban công/cửa sổ 8, động vật 6, ghế/bàn 6, nhạc cụ 5, văn phòng phẩm 3, thuốc lá/bật lửa 1 |

Nới khoảng điểm thì có thêm cặp khác hẳn: 26 ảnh nếu 3–60 điểm, 34 ảnh nếu 2–80 điểm.

## 3. Đã kiểm (rút thử, seed chỉ để kiểm, kết quả đã xóa)

| cỡ | dev | test | kiểm |
|---|---|---|---|
| 20 + 40 | 6 khác hẳn + 14 dễ nhầm, 60 query | 13 + 27, 120 query | đạt |
| 30 + 50 | 7 + 23, 90 query | 12 + 38, 150 query | đạt |

Các bài kiểm: đúng số ảnh, dev và test không trùng, không dùng ảnh đã loại, lấy đủ 19 ảnh khác hẳn, mỗi ảnh có 2 query có mặt và 1 (hoặc 2) query vắng mặt, GT bằng số điểm MUCCA và nằm trong 3–40, lớp vắng mặt không có nhãn trong ảnh, `inputs.jsonl` không chứa GT, tỉ lệ dev mỗi nhóm lệch dưới 1 ảnh, chạy 2 lần ra file giống hệt, và không ghi đè thư mục cũ. Khoảng 65–75% ảnh có truy vấn vắng mặt loại khó; số còn lại là loại dễ vì siêu nhóm của Y đã có nhãn hết (ví dụ nhạc cụ chỉ có 2 lớp).

## 4. Cần Trí quyết

1. **Cỡ tập:** dev 20 + test 40 (60 ảnh, 180 query, theo kế hoạch thực thi) hay dev 30 + test 50 (80 ảnh, 240 query, theo §5.1 của Trí; kế hoạch thực thi ước 80 ảnh tốn khoảng 3–4 giờ công kiểm nhãn)?
2. **Khoảng điểm:** giữ 3–40 (19 ảnh khác hẳn), hay nới 3–60 (26 ảnh) để có thêm cặp khác hẳn nhưng kiểm bằng mắt lâu hơn?
3. **Cách lấy cặp dễ nhầm:** xoay vòng qua siêu nhóm (như trên: nhóm nhỏ như nhạc cụ, văn phòng phẩm được lấy gần hết), hay theo tỉ lệ có sẵn của MUCCA (trái cây và bát đĩa sẽ chiếm phần lớn)?
4. **Thêm truy vấn vắng mặt loại dễ** (`--easy-absent`)? Thêm 1 query mỗi ảnh để người kiểm.
5. **Seed:** dùng 331 như v1 (luồng ngẫu nhiên khác vì tên khác) hay số khác?

**Một điểm cần biết:** 13/19 cặp khác hẳn là người–xe, vì MUCCA vốn như vậy. Bản rút r1 của v1 từng bị loại vì 10/10 cặp là người + xe/chó. Ở v2, cặp khác hẳn chỉ chiếm khoảng 1/3 tập, phần còn lại trải qua 10 siêu nhóm.

## 5. Sau khi Trí duyệt

1. Triệu rút thật (CPU, vài giây), ví dụ với 20 + 40:
   ```text
   python experiments/countgdpp/select_dev_test_v2.py --n-dev 20 --n-test 40 --mucca C:/Users/diosodumb/Downloads/MUCCA_1.0 --out experiments/countgdpp/dev_test_v2
   ```
2. Trí và Triệu kiểm vật vắng mặt và GT bằng mắt, theo cách đã làm với `p4_unseen_v1` (`HUONG_DAN_KIEM_DU_LIEU.md`). Đổi lớp vắng mặt nào thì ghi lý do.
3. Khóa (`status=LOCKED`, người/ngày, hash) **trước khi chạy model**. Sau đó chạy P1 trên dev (Ô 9 + Ô 12) để chọn `tau_pseudo` và `M`; test chỉ chạy một lần ở cuối.
