# p4_unseen_v1 — tập kiểm mới cho P4.6 (LOCKED 27/10/2026 17:07:55)

**ĐÃ KHÓA 27/10/2026 17:07:55 theo xác nhận trực tiếp của Trí** (thông tin khóa ghi trong `selection_meta.json`).
- Trước khi khóa, đổi absent u07_3 (mcac_88) và u10_3 (mcac_84) từ `trucks` → `bicycles`: ảnh có xe van/minibus và xe bán tải nên trucks không chắc vắng mặt. Trí duyệt; bản trước khi đổi ở `draft_before_absent_swap_20261027/`.
- Quy ước chấm = §4 của HUONG_DAN_KIEM_DU_LIEU.md (Trí đồng ý).
- Kiểm nhất quán đạt: 30 ID duy nhất, 20 present / 10 absent, prompt và class khớp, GT = số điểm MUCCA, hash ảnh khớp.
- sha256: inputs.jsonl `53e91e81…`, manifest.csv `9161d8f4…`, absent_candidates.csv `2d1f5b41…`.
- **Không sửa các file này sau khi đã chạy model.** Nếu phát hiện lỗi, tạo bản v2 có lịch sử.


**Tạo 27/10/2026, phương án B do Trí chọn.** Ảnh lấy từ MUCCA 1.0 chính thức (Zenodo 19231375, CC-BY-4.0, Ciampi et al.). Bản tải về nằm ở `data_external/mucca_zenodo_19231375/`, md5 zip `b182e445…` khớp Zenodo. Gói 10 ảnh của Triệu trùng từng byte với bản chính thức, cả ảnh lẫn annotation.

## Cách chọn (chỉ dùng annotation, chưa có output model nào trên các ảnh này)

Quy tắc r2 nằm trong [p4_select_unseen.py](../p4_select_unseen.py):
- Loại 5 ảnh dev.
- Mỗi ảnh lấy cặp X/Y thuộc hai siêu nhóm khác nhau, mỗi lớp 3–40 điểm (29/195 ảnh đạt).
- Rút phân tầng 5 nhóm × 2 ảnh, seed 331: người–động vật, người–nhạc cụ, ghế–ô bãi biển, người–ô tô/xe tải, người–xe máy/thuyền.
- Lớp absent ưu tiên **cùng siêu nhóm với Y** (loại "khó").

Bản rút r1 (rút ngẫu nhiên thường) bị loại **trước khi chạy model**, vì 10/10 cặp đều là "people + xe/chó". Bản đó lưu ở `draft_r1_rejected/`.

10 ảnh / 30 query (20 present, 10 absent): `mcac_123, 121, 109, 110, 63, 61, 88, 72, 227, 84`. Xem `contact_sheet.jpg`.

| File | Nội dung | Đưa vào model? |
|---|---|---|
| `inputs.jsonl` | ID / ảnh / prompt (schema v1) | Có |
| `manifest.csv` | GT = số điểm MUCCA, presence, nguồn, giấy phép, split `test_p4_unseen_v1` | Không, chỉ evaluator |
| `absent_candidates.csv` | lớp absent đề xuất + 5 lớp dự phòng; cột để người kiểm điền | Không |
| `selection_meta.json` | quy tắc, seed, các tầng, hash ảnh, hash script | Không |

## Trí cần làm trước khi khóa

**Mở [HUONG_DAN_KIEM_DU_LIEU.md](HUONG_DAN_KIEM_DU_LIEU.md)**: có bảng 10 ảnh gốc + 10 ảnh chấm GT hai lớp, ví dụ điền cột và cách đồng bộ khi đổi absent. Ảnh GT chỉ vẽ điểm nguồn; Trí đã xác nhận nhãn qua tin nhắn 27/10, không phải output model.

1. **Absent:** kiểm từng proposed_absent trên ảnh gốc. Điền absent_ok / visible, người/ngày thật; chưa chắc giữ PENDING và ghi note. Mọi lớp thay thế cũng phải được xem ảnh xác nhận. Khi thay lớp, lưu lịch sử và đồng bộ class_id/target_class/prompt ở manifest, prompt ở inputs, cùng dòng absent_candidates. Chú ý trucks ở mcac_88/mcac_84; gợi ý trước của assistant chưa phải xác nhận.
2. **GT present:** đối chiếu 20 query với cả điểm nguồn lẫn ảnh gốc; ghi verified_by và uncertainty_note đúng mức kiểm. Bất đồng phải được ghi, không tự sửa annotation/gt_count hoặc đánh dấu kiểm xong chỉ vì số chấm khớp. Xem kỹ chairs=3 ở mcac_63 và people=3 ở mcac_121.
3. **Quy ước chấm:** trước khi N4, Trí chốt quy tắc đúng loại/cả vật/che khuất, ghép một-một, trùng và uncertain theo §4 hướng dẫn. **Đính chính hướng dẫn cũ:** một điểm nằm trong box chỉ gợi ý vị trí, chưa đủ chứng minh box đúng vật; box rộng có thể chứa nhiều điểm. Quy tắc hiện là đề xuất, chưa được Trí duyệt; không gọi đây là AP/IoU bbox chuẩn.
4. **Khóa:** chỉ sau khi nhãn/lịch sử sử dụng/ID/prompt và quy tắc đã kiểm đủ, mới đặt status=LOCKED trong selection_meta, ghi người/ngày/phiên bản quy ước và hash file cuối vào WORKLOG. Xem §5 hướng dẫn. Runner hiện không tự bắt buộc status LOCKED; nhóm phải kiểm điều kiện trước chạy. **Chỉ chạy ảnh mới khi dữ liệu đã khóa và kiểm dev C3 đạt.** Không sửa danh sách sau khi xem output; nếu phát hiện lỗi cần bản sửa có lịch sử.

**Cập nhật xác nhận 27/10:** Trí xác nhận đã kiểm bộ 10 ảnh và thấy nhãn đúng. Đã ghi 10 absent_ok và verified_by cho 30 query theo [tin nhắn xác nhận](human_review_20261027.json). Giữ nguyên lớp/prompt/GT; không suy rộng thành toàn bộ MUCCA đã kiểm. **Vẫn DRAFT_NOT_LOCKED:** còn chốt quy tắc chấm và xác nhận lịch sử sử dụng trước khi khóa.
