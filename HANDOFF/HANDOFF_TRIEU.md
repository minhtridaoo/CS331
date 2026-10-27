# Handoff Triệu — thực hiện T1–T4 theo kế hoạch V2
> **MỚI NHẤT 28/10:** việc hiện hành của Triệu nằm ở [GIAO_VIEC_TRIEU_20261028.md](GIAO_VIEC_TRIEU_20261028.md): V1–V2 N4 tầng A (hạn 30/10), V3 q05_3, V4 2 ca thử, V5 phân tích B2/B0 (01/11), V6 N4 tầng B (02/11), V7 duyệt chung (03/11). Gói: `TRIEU_GIAO_VIEC_20261028.zip`. ZIP V2 (`TRIEU_T1_T4_20261027_v2.zip`) **không dùng nữa**. 47 nhãn q03: đề xuất tạm hoãn, Trí quyết.

**Cập nhật 27/10/2026.** Nguồn giao việc: [KE_HOACH_SUA_KIEM_CHEO V2](../reports/KE_HOACH_SUA_KIEM_CHEO_20261027.md). [Gói đầu vào ZIP](TRIEU_T1_T4_20261027_v2.zip).

Triệu đã chấp nhận bản kiểm do assistant làm ngày 24/10. **Trí đã đọc và chưa duyệt ngày 27/10**, yêu cầu Triệu tự chạy/kiểm/phân tích. Không ghi việc chấp nhận bản kiểm cũ là đã đáp ứng yêu cầu sửa mới.

| Việc | Hạn đề xuất | Bàn giao |
|---|---|---|
| T0 nhận đủ đầu vào | Trước T1 | Kiểm file/hash/ảnh/Python, ghi ngày nhận |
| T1 tự chạy evaluator + 7 ca | 30/10 | stdout, exit code, output, fixtures, CASE_RESULTS và giải thích tự viết |
| T2 q05_2/q05_3 | 01/11 | Nhãn 21/79/3 dòng + đối chiếu 14 khung q05_2; tổng/uncertain/bỏ sót/minh chứng |
| T3 phân tích từ T2 | 02/11 | Bảng delta, sensitivity q05_3, quan sát/giả thuyết tách rõ và đề xuất |
| T4 duyệt chung | 03/11 | PILOT_SUMMARY có nguồn và người/ngày/quyết định thật |

**T1 đã sửa cách chạy:** mkdir trước redirect; không tạo trước thư mục output của evaluator. Mỗi fixture giữ đủ 15 query, chỉ sửa q01_1, giữ nguyên q05_2 để manual_check không phát sinh lỗi ngoài mục tiêu. Không dùng --skip-manual-review vì code chưa có flag đó. Ca dự kiến bị từ chối cần đúng exit code/lý do, không coi mọi crash là PASS.

**Đã tự kiểm ngày 27/10:** Triệu tự làm lại kiểm chéo Phần 2 (self-test, tính lại metric, truy ngược q05_3, tự gán nhãn q05_2, thử dữ liệu hỏng, chạy lại evaluator), tất cả khớp. [Báo cáo tự kiểm](../reports/TRIEU_TU_KIEM_PHAN2_20261027.md). Đã thêm lưu ý độ nhạy q05_3 vào PILOT_SUMMARY mục 3.

**Việc ngay tiếp:** cùng Trí duyệt toàn bộ PILOT_SUMMARY và ghi quyết định chung. Phần tự kiểm của Triệu đã xong; chưa có quyết định duyệt nhóm, đóng pilot hoặc chọn P4. Trí cần đồng bộ log/cấu hình với artifact P4 đã có.

**Đánh giá của assistant 27/10 tối (để Trí nghiệm thu):** [DANH_GIA_TRIEU_TU_KIEM_20261027.md](../reports/DANH_GIA_TRIEU_TU_KIEM_20261027.md). Nhận xét 1 (tự chạy evaluator, ca hỏng) và q05_2 **đạt**. Còn thiếu: 2 ca thử (`uncertain`, absent > 0); nhãn từng khung q05_3 (79 + 21) trong gói q05; bảng chênh lệch từng query, liên hệ mẫu tự chọn và đề xuất cải thiện (T3). Lúc làm, Triệu chưa có gói V2/q05 vì chúng chưa được push.

**Hướng dẫn V2 cho phần còn lại:** **T2:** một nhãn chính/box, có uncertain; không tính part/wrong_class thêm lần nữa vào duplicate. Không cố ép khớp nhãn cũ khi có bằng chứng khác. **T3:** B2 confidence=4.6, CLIP-only=6.8, Fusion=5.8; tổng lỗi +39 nhưng q05_3 riêng +58, phần còn lại −19. Phải viết phân tích của mình, không chép mốc tham chiếu như việc tự làm.

Những mốc này là đề xuất, chưa có xác nhận nhận việc. ZIP mới chuẩn bị tại máy Trí, chưa được assistant gửi; các gói vẫn chưa nằm trên origin/main d6db189. T1–T4 không cần tập P4_unseen hoặc GPU.

47 nhãn q03 là việc P4 riêng, không cộng vào điều kiện đóng pilot T1–T4. Trí tiếp tục kiểm dữ liệu và runner song song. Không yêu cầu ablation/đổi model/train trong vòng sửa này; chưa biết cơ chế nội tại được ghi như giới hạn.
