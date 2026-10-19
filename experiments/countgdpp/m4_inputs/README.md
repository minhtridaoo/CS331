# M4 — Chạy bộ ảnh Triệu gửi

**Cập nhật 14/10/2026. Trạng thái: đã chạy và review 5 ảnh/15 query; tiếp theo chẩn đoán nguyên nhân nhầm loại trước khi mở rộng.**

## Đã kiểm

- Nguồn nhận: workspace Trí and Triệu/Triệu/MUCCA_10_queries/MUCCA_10_queries/.
- 10 ảnh đọc được; 30 query có ID duy nhất; GT khớp điểm/class trong annotations.json; tọa độ điểm nằm trong ảnh.
- Cả 30 query đều present. Không tính FPR_absent từ bộ này; cần Triệu bổ sung lớp vắng mặt đã kiểm bằng mắt.
- Mới kiểm tính nhất quán nhãn trong gói nhận, chưa xác minh độc lập nhãn gốc, nguồn URL/quyền sử dụng hay đếm tay toàn bộ vật thể.
- Bộ này là dev nội bộ để khảo sát, không phải holdout hoặc đánh giá toàn benchmark. Không chia các query cùng ảnh sang hai split khác nhau.
- Các ảnh chứa nhóm gần nhau (trái cây, đồ dùng, cừu/dê) lẫn loại khác nhau (guitar/ampli/ghế, người/ô); khi phân tích cần tách để bám yêu cầu X/Y khác hẳn nhau.

## File đã tạo

- inference_inputs.jsonl: 10 ảnh/30 query, chỉ 5 trường schema v1, không đáp án/class_id.
- first5_inputs.jsonl: 5 ảnh/15 query đầu theo thứ tự gói nhận, chọn trước khi xem dự đoán.
- first_image_inputs.jsonl: mcac_100, ba query guitars/amplifiers/chairs để nối luồng đầu tiên.
- manifest.csv: đáp án chỉ dành evaluator; GT theo gói nhận, chưa kiểm chéo thủ công. source_url để trống thay vì tự đoán nguồn.
- data_audit.json: kết quả kiểm dữ liệu và hash nguồn. contact_sheet.jpg: ảnh tổng quan, không phải prediction.
- adapter_check_inputs.jsonl: cat trên ảnh utensils cũ để kiểm chương trình, không thuộc pilot MUCCA.

## Lệnh ảnh đầu — đã chạy thành công

Trong Ubuntu WSL:

~~~bash
source /root/.venvs/countgdpp/bin/activate
cd /mnt/d/MINHTRIHOCCODE/HOCKI5/CS331
python experiments/countgdpp/run_b0_batch.py --inputs experiments/countgdpp/m4_inputs/first_image_inputs.jsonl --run-id m4_first_image_b0
~~~

Kết quả ở results/countgdpp/m4_first_image_b0/: predictions.jsonl, run_config.json, jobs/<query>/raw/results.json, ảnh overlay, prompt và console.log. Không ghi đè run cũ: nếu thư mục đã tồn tại, đọc kết quả trước rồi chỉ dùng run-id mới khi chủ động chạy lại.

**Lệnh batch 5 — đã chạy:** thu thập 5 ảnh trong khi Triệu hoàn thiện evaluator (sẽ chạy lại cả ảnh đầu để tạo một run 15 query đầy đủ):

~~~bash
python experiments/countgdpp/run_b0_batch.py --inputs experiments/countgdpp/m4_inputs/first5_inputs.jsonl --run-id m4_first5_b0
~~~

Chỉ sau khi bộ 5 ảnh ổn mới chạy toàn bộ bằng inference_inputs.jsonl và run-id m4_all10_b0. Chưa mở B2, train hoặc đổi ngưỡng.

## Cách runner hoạt động và giới hạn

Runner gọi nguyên process_folder.py của commit đã pin, từng query là một tiến trình riêng, checkpoint được nạp lại mỗi lần nên chậm hơn cách nạp một lần. Mỗi job có đúng một ảnh, positive text đúng text_prompt, exemplar boxes/negative rỗng, ngưỡng 0.23. Giữ nguyên lọc gốc: max điểm token trước dấu chấm (có token đặc biệt/dấu chấm) > ngưỡng, rồi so với phần sau dấu chấm. Không âm thầm sửa lọc hoặc NMS; chưa kết luận logic token là nguyên nhân sai lớp.

Checkpoint audit: 1108 state keys của app được nạp, missing=0, shape load thành công; 38 unexpected thuộc feature_map_encoder. App không có khối này; bản groundingdino.py có khai báo nhưng lời gọi khối bị comment. Đã ghi nhận là tương thích với đường B0 app đã pin, không chứng minh đầy đủ kết quả paper. Hash checkpoint là hash file local, chưa đối chiếu hash tác giả.

elapsed_ms là thời gian toàn tiến trình mỗi query, gồm khởi tạo/nạp trọng số và vẽ/lưu; không gọi là thời gian inference thuần. peak_vram_mib=null vì chưa đo. Crash lưu error/count=null rồi dừng để xem log; những query chưa chạy không được tính là 0. Việc đo tài nguyên P0 còn chờ.

Kiểm tra đã chạy: input hợp lệ 30 query; từ chối ID trùng, trường GT và count không khớp boxes; một run GPU kiểm adapter với cat trên ảnh cũ trả 0 như output gốc. Chưa xác nhận toàn bộ batch MUCCA đã chạy hoặc Triệu đã ghép evaluator.


**Kết quả ảnh đầu ngày 14/10:** guitars 25/GT25; amplifiers 44/GT11 (khung nhầm guitar); chairs 0/GT1. Chi tiết trong results/countgdpp/m4_first_image_b0/REVIEW.md. Chưa có kết quả cả 5 ảnh hoặc evaluator chính thức.


**Sau batch 5, 14/10:** 15/15 query thành công; lỗi nhầm loại lặp lại, nhất là mcac_200. Xem [review](../../../results/countgdpp/m4_first5_b0/REVIEW.md). **Bước tiếp theo:** giữ B0/ngưỡng 0.23, phân tích khung sai loại và điểm theo token trên mcac_200 cùng mcac_100; chưa thay lọc, train hoặc mở B2. Triệu ghép evaluator, kiểm nhãn và bổ sung absent. Chẩn đoán token là giả thuyết kiểm tra, chưa phải nguyên nhân đã chứng minh.
