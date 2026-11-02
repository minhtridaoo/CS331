# Rà lại việc Triệu và nguyên nhân lỗi N4 — 29/10/2026

**Yêu cầu:** Trí hỏi Triệu đã làm đủ việc giao chưa và N4 lỗi do người review hay công cụ. Assistant kiểm chỉ đọc các artifact, ảnh và code đã có; không chạy evaluator, self-test, inference, training hoặc thay ngưỡng. Đây là kiểm kỹ thuật và đề xuất, không phải Trí ký nghiệm thu hay hai người duyệt chung.

**Kết luận:** Triệu đã nộp đủ V1–V2 N4 tầng A, đúng hạn; chưa hoàn thành toàn bộ V1–V7. Các khung hỏi người nhưng khoanh chó/xe đã có trong dự đoán ngày 27/10, trước lần gán nhãn của Triệu. Có bằng chứng về điểm mẫu ảnh lấn át điểm chữ ở một số khung lượt hai. Công cụ hiển thị crop và quy ước nhãn cũng có chỗ dễ gây nhầm, cần tách khỏi lỗi model.

## 1. Đối chiếu việc đã giao với bằng chứng

Nguồn phân công hiện hành: [GIAO_VIEC_TRIEU_20261028](../HANDOFF/GIAO_VIEC_TRIEU_20261028.md), thay gói T1–T4 cũ. `git ls-remote --heads origin main` và HEAD đều là `be4da2655edecdaf502bdca28786e966cca65d01` khi kiểm. Không có commit mới hơn trên main lúc kiểm; chưa biết các phần chưa push trên máy Triệu.

| Việc | Bằng chứng tại repo ngày 29/10 | Trạng thái / hạn |
|---|---|---|
| Kiểm evaluator và q05_2 trước đây | stdout self-test có PASS; 3 JSON metrics/per_query/manual_check của run Triệu trùng nội dung run 20/10. Báo cáo tự kiểm và bảng tính đã nộp | Có bằng chứng; không chạy lại trong lượt này. Chữ “8/8” là checklist cũ, không phải toàn bộ việc mới |
| V1 — N4 A gói chính | 7 CSV, 78/78 dòng đã điền | Đã nộp đủ, trước hạn 30/10 |
| V2 — N4 A bổ sung | 7 CSV pseudo, 21/21 dòng; 3 CSV E3, 18/18 dòng | Đã nộp đủ, trước hạn 30/10; còn lưu ý chất lượng dưới đây |
| V3 — q05_3 | 79 B2 + 21 B0 + 3 pseudo đều chưa có label_type | Chưa có bài nộp hoàn chỉnh; hạn 01/11 |
| V4 — uncertain và absent > 0 | Báo cáo hiện vẫn chỉ có 5 ca cũ; chưa có bằng chứng 2 ca bổ sung | Chưa xác nhận hoàn thành; hạn 01/11 |
| V5 — phân tích B2/B0 và đề xuất | Có phân tích độ nhạy q05_3 trước đây; chưa có phần phân tích bổ sung theo V5 | Mới làm một phần; hạn 01/11 |
| V6 — N4 B | 41 khung chính + 6 pseudo + 11 E3 đều chưa có nhãn | Chưa nộp; hạn 02/11 |
| V7 — duyệt chung | Chưa có quyết định đóng pilot của cả Trí và Triệu | Chờ hai người; hạn 03/11 |

V3–V7 chưa quá hạn vào ngày rà này. V8–V10 là đề xuất việc sau, cần Trí đồng ý, không tính là phần đang thiếu bắt buộc. 47 nhãn q03 đang tạm hoãn theo phân công mới.

## 2. Đã kiểm gì ở 117 dòng N4 A?

- Đối chiếu 17 CSV với bản gốc `e877541`: đủ dòng; query/prompt/rank hoặc tag không đổi; tọa độ bằng nhau về giá trị số. Đối chiếu thêm với final_boxes/pseudo_boxes của prediction gốc, sau làm tròn một chữ số theo script tạo gói: khớp.
- 117 dòng có label_type hợp lệ, actual_class, reviewer và ngày 28 hoặc 29/10/2026. Các ô ngày hiện tại không lỗi. WORKLOG ghi trước đó có vấn đề Excel/điền ngày đã được sửa; không có bằng chứng để quy lỗi ngày cũ hoàn toàn cho người hay phần mềm.
- Gói chính: 71 wrong_class, 6 multi_object, 1 uncertain, 0 target. Khi đọc bảng tra đã lưu: lọc điểm giữ 78 khung; Fusion giữ 14 (11 wrong_class, 2 multi_object, 1 uncertain). **0 nhãn target không đồng nghĩa mọi khung uncertain đã được xác nhận sai.**
- Pseudo: 1 target, 10 wrong_class, 10 multi_object. Trong 21 mẫu có 9 mẫu của query vắng mặt, vốn không thể có vật đúng. Với 4 query people có mặt, chỉ 1/12 được gán target. Không dùng 1/21 làm tỷ lệ chất lượng toàn bộ model.
- E3: 13 target, 3 part, 2 uncertain. Đây là các ứng viên B2 bị cả hai bộ lọc loại, được chọn bằng điểm GT trong khung; không phải mẫu đầy đủ của tất cả khung bị loại.
- Đã xem lại một số ảnh tiêu biểu (u07_1 chính/pseudo, u01_1 E3, u08_1 E3). Kết quả sai loại nhìn thấy trong ảnh phù hợp với xu hướng nhãn; **chưa có lần phân xử độc lập từng khung cho toàn bộ 117 dòng**.

## 3. Bằng chứng lỗi nằm trước bước Triệu review

Prediction lưu ngày 27/10 có 30/30 dòng execution_status=ok, không error_message. N4 chỉ cắt và đánh số những khung có sẵn. Commit Triệu `be4da26` chỉ thay WORKLOG và 17 CSV, không sửa model, prompt, prediction hay bộ lọc.

Runner `experiments/countgdpp/run_b2_frozen.py` truyền `row['prompt']` ở cả hai lượt. Raw input_ids lưu cho u07_1 people, u07_2 cars, u07_3 bicycles khác nhau (token chữ lần lượt 2111, 3765, 21066). Vì vậy không có bằng chứng ở các ca kiểm rằng script gửi cùng một prompt hoặc bỏ mất prompt.

Trong `CountGDPlusPlus/process_folder.py:get_boxes_from_prediction`, điểm dương lấy max các token trước và gồm dấu chấm. Ở lượt hai, khoảng này chứa cả token chữ lẫn token mẫu ảnh (1008). Do đó điểm cuối cao không bảo đảm điểm của riêng chữ cần đếm cao.

Đối chiếu tọa độ final với stage2_raw.npz (sai khác do float < 0,0001 pixel ở các khung đã kiểm), đọc trực tiếp các điểm đã lưu:

| Query / rank | Quan sát theo nhãn và ảnh | Điểm token chữ | Max điểm token mẫu ảnh | Điểm final lưu |
|---|---|---:|---:|---:|
| u07_1 / 1 | Hỏi people, khung ô tô | 0,0398 | 0,9675 | 0,9675 |
| u07_1 / 2 | Hỏi people, khung ô tô | 0,0488 | 0,9631 | 0,9631 |
| u08_1 / 1 | Hỏi people, khung ô tô | 0,0770 | 0,9700 | 0,9700 |
| u08_1 / 9 | Khung được Triệu gán target people | 0,4448 | 0,1564 | 0,4448 |
| u08_1 / 11 | Khung được Triệu gán target people | 0,4376 | 0,1342 | 0,4376 |
| u01_1 / 1 | Hỏi people, khung chó | 0,2018 | 0,9743 | 0,9743 |

Ngưỡng lọc điểm đã khóa là 0,9067394733428955. Trong ví dụ u08_1, ô tô qua ngưỡng còn người thật không qua. Đây là cơ chế cụ thể giải thích một phần lỗi giữ sai/bỏ đúng: mẫu ảnh và cách tổng hợp điểm ở lượt hai có thể ưu tiên vật khác câu hỏi. Fusion dùng thêm CLIP nhưng không bảo đảm mọi khung giữ đều đúng.

**Giới hạn:** đây là đọc lại raw đã lưu, không phải thử thay mẫu hoặc thay bộ lọc. Không khẳng định toàn bộ lỗi do duy nhất pseudo, model hỏng hoàn toàn, hoặc đã chứng minh sửa P sẽ thắng R. Cấu hình này là adapter B2 của nhóm, không phải toàn bộ cấu hình benchmark paper.

## 4. Chỗ công cụ/hướng dẫn dễ gây nhầm

1. **Crop có lề nhưng không có biên bbox thật.** Cả `evaluation/p4_n4_make_review_package.py` và `evaluation/p4_n4_make_supplement.py` đều nới 15% chiều rộng/cao ở mỗi phía khi cắt, rồi chỉ ghi số khung. Vật nhìn thấy ở lề crop có thể nằm ngoài bbox model. Ảnh overview có biên khung nhưng nhiều khung chồng nhau. Đây là hạn chế của công cụ chuẩn bị review do assistant tạo; không thể quy mọi nhãn multi_object cho Triệu chấm sai. Cần đối chiếu bbox thật ở các ca multi_object/part/uncertain, không tự đổi nhãn.
2. **Hai chiều lỗi đang chung một label_type.** Một khung có thể vừa sai loại vừa bao nhiều vật. Nhãn multi_object không tự cho biết đúng/sai loại; phải đọc actual_class và note. Hướng dẫn cần rõ thứ tự và tiêu chí “một vật chính”.
3. **object_id chưa thống nhất xuyên file.** u01_1 pseudo P2 là p1; E3 #18 là p4 và note nói cùng người; E3 #4 lại là p1 của người khác. Dùng ID trong từng file thì hiểu được, nhưng ghép thẳng xuyên file sẽ sai. Khi cần đếm vật riêng biệt phải có bảng đối sánh được xác nhận. Không ảnh hưởng nhận xét chó/xe là sai loại; chưa sửa CSV gốc.
4. **Vật che khuất/ở rìa ảnh cần thống nhất.** Chẳng hạn u01_1 E3 #36 được ghi part vì người ra ngoài mép ảnh. Cần đối chiếu đơn vị vật theo GT và phần nhìn thấy; đây là ca cần phân xử, không tự kết luận người chấm sai.

## 5. Đính chính cách diễn giải của bản tổng hợp trước

[N4_KET_QUA_TANG_A_20261029](N4_KET_QUA_TANG_A_20261029.md) do assistant tổng hợp trước lượt rà này; giữ nguyên để tra lịch sử. Các số đếm nhãn khớp, nhưng các câu dưới đây mạnh hơn bằng chứng:

- “Model bỏ qua prompt”: khung giống nhau cho thấy chọn sai loại/ít nhạy với yêu cầu ở các ca này; không chứng minh phần mềm không nhận prompt. Raw token cho thấy có nhận các chữ khác nhau.
- “Lỗi bắt đầu từ mẫu tự chọn, E1 chiếm ưu thế”: có mẫu sai và lỗi lọc vật đúng cùng tồn tại. Chưa có can thiệp/đối chứng để xác định nguyên nhân chủ đạo. Tầng A được cố ý chọn ca lỗi; có cả absent.
- “Bỏ R vì sẽ cứu nhầm”: R1 trong đề xuất có điều kiện CLIP và bằng chứng có mặt, không chỉ giữ điểm CountGD cao. Chưa thử nên chưa được kết luận R thất bại. E3 có khung người thật bị bỏ, nên đây vẫn là vấn đề cần đối chứng.
- Người ở E3 là ứng viên **lượt hai**, không tự chứng minh nằm trong tập ứng viên top-M **lượt một** mà P dự kiến chọn.

Trách nhiệm các suy luận quá mức trên thuộc phần tổng hợp của assistant, không phải nhãn Triệu. Có thể đề xuất thử P có giới hạn trên dev, cùng C6; vẫn giữ quyết định phương pháp ở trạng thái chưa chốt và không loại R chỉ dựa trên N4 A.

## 6. Bước tiếp

1. Nhận V1–V2 là đã nộp đủ và qua kiểm cấu trúc; Trí quyết nghiệm thu. Chỉ rà lại các ca cần phân xử bằng bbox thật, không yêu cầu chấm lại toàn bộ từ đầu.
2. Triệu tiếp V3, V5, V4 theo hạn 01/11 và V6 hạn 02/11; V7 là việc hai người cùng làm. Tầng B giúp có thêm các query khác nhóm lỗi A trước khi chọn hướng.
3. Nếu làm tiếp công cụ, thêm đường biên bbox thật trên crop có lề, giữ ảnh/nhãn gốc và bảng đối sánh ID riêng. Lượt này chưa sửa công cụ, chưa gán lại nhãn hay chạy phương pháp mới.

**Bảo toàn:** không sửa CSV, predictions, raw NPZ, GT, freeze hoặc code model. SHA256 predictions: `bae674d7a171edaedb8cbd61b9e28a233953e4eaf3a46dc833c7a4f3e0db7fc3`; freeze: `3c4634e79d21d0c58bd7c0e3db0972c3a3eeff6d25996c716b4def1267def4da`. Chỉ bổ sung báo cáo rà và đồng bộ điểm tiếp tục; không commit/push hay gửi tin cho Triệu.

## 7. Bổ sung cùng ngày — kiểm chất lượng nhãn sau khi Trí hỏi N4 chưa ổn

Trí muốn đánh giá chất lượng thực tế, không chỉ đủ dòng. Assistant dựng ảnh đối chiếu từ ảnh gốc và tọa độ đã lưu, vẽ biên bbox thật trên cùng vùng ảnh; không chạy model hoặc đổi CSV.

| Cùng query u07_1 — people | Nhãn hiện tại | Quan sát |
|---|---|---|
| Final #5 và pseudo P1 | wrong_class / multi_object; cả hai actual_class=cars | Cùng xe đỏ, vùng ảnh gần nhau; IoU giữa hai khung là 0,8900 |
| Final #13 và pseudo P3 | wrong_class / multi_object; cả hai actual_class=cars | Cùng xe tối màu ở giữa, vùng ảnh gần nhau; IoU 0,9029 |

IoU ở đây chỉ mô tả độ chồng giữa hai khung dự đoán, không phải chấm định vị với GT. Hai khung mỗi cặp không hoàn toàn giống nhau; nhãn khác không tự chứng minh người chấm sai. Tuy nhiên, tiêu chí hiện tại chưa giải thích rõ vì sao cả hai đều có xe chính và vật lân cận mà lại đổi loại lỗi. Cần xác nhận có chủ ý dùng tiêu chí khác giữa pseudo/final hay do lề crop/cách hiểu một vật chính; nếu tiêu chí khác phải ghi rõ và không gộp như một định nghĩa.

**Đánh giá sau xem ảnh:** nhận diện sai loại có bằng chứng sử dụng được; phân rã wrong_class/multi_object/part và ghép vật chưa đủ nhất quán để coi là bộ nhãn cuối đã nghiệm thu. Chỉ kết luận trong các ca đã kiểm, không gán tỷ lệ sai nhãn cho 117 dòng.

**Đề xuất sửa hẹp:** thêm biên bbox thật khi xem crop, thống nhất ưu tiên nhãn (hoặc tách đúng loại khỏi đơn vị vật trong bước sau), đối chiếu các nhãn multi_object/part/uncertain và hai cặp trên. Giữ bản gốc và ghi lý do nếu sửa. Không suy E1 lớn hơn E3 từ 20/21 so với 13/18 vì khác mẫu, khác đơn vị và E1 có 9 mẫu absent. N4 hiện đủ minh họa lỗi, chưa tự đủ để chốt nguyên nhân/cải tiến.
