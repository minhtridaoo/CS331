# Kiểm chéo bằng mắt của Triệu — B2

Ghi nhận từ nhận xét trực tiếp của Triệu trong chat. Đây là review định tính, chưa phải nhãn độc lập từng bbox hoặc xác nhận mọi ground truth. Số box lấy từ predictions đã lưu. Giữ riêng với USER_VISUAL_REVIEW.md của Trí; không thay thế bản gốc.

## q01_2 — amplifiers — mcac_100.jpg

- GT MUCCA: 11. Stage 1: 44 box. Final: 38 box.
- Triệu đã gửi ảnh stage 1 và pseudo, xác nhận final có cùng kiểu khoanh lẫn vật.
- Stage 1: có ampli nhưng khoanh lẫn nhiều guitar và ghế.
- Pseudo: 0/3 mẫu đúng loại; cả 3 khoanh guitar thay vì ampli, được xác nhận từ ảnh gửi trong chat.
- Final: vẫn khoanh lẫn nhiều loại. Nhận xét “y chang” được ghi là cùng kiểu lỗi, không phải tập khung giống hệt.
- Chưa gán nhãn từng box hoặc kết luận mẫu sai là nguyên nhân duy nhất.

## q01_3 — chairs — mcac_100.jpg

- GT MUCCA: 1. Stage 1: 0 box. Final: 0 box.
- Triệu báo: cả ba ảnh stage 1 / pseudo / final đều không có vật được khoanh.
- Theo dữ liệu chạy: không có pseudo-exemplar, stage2_executed=false; final trả kết quả lượt đầu. Không coi đây là ba lượt inference độc lập.
- Đây là bỏ sót lớp có mặt theo GT, không phải query absent.

## q02_1 — plates — mcac_11.jpg

- GT MUCCA: 15. Stage 1: 28 box. Final: 31 box.
- Triệu báo stage 1 khoanh dư 2 cái bát và miệng ly; box miệng ly mang số 25 trên overlay. Giữ nguyên số hiển thị, chưa quy đổi sang chỉ số mảng prediction.
- Đây là các box sai loại đã được người review nhận diện; chưa kết luận đã phân loại hết mọi box thừa hoặc mọi sai số count.
- Triệu xác nhận pseudo đúng cả 3/3 mẫu: cả ba đều là đĩa và bao trọn đĩa. Chốt bản kiểm chéo của Triệu là 3/3 đúng loại, 3/3 bao trọn vật.
- Bản review gốc của Trí ghi 0/3 mẫu đúng; giữ riêng thông tin nguồn này để thấy hai nhận xét khác nhau, không ghi đè bản gốc của Trí. Xác nhận mới của Triệu đã làm rõ nhận xét trong bản kiểm chéo này.
- Triệu báo final khoanh giống stage 1: ghi là cùng kiểu lỗi theo nhận xét; count thay đổi 28 → 31, chưa xác nhận từng box tương ứng.

## q02_2 — bowls — mcac_11.jpg

- GT MUCCA: 3. Stage 1: 31 box. Final: 31 box.
- Triệu gửi hai ảnh overlay và báo stage 1 chỉ phát hiện đúng 2 bát, bát thứ ba bị bỏ sót. Overlay có nhiều box khoanh các vật khác như đĩa và cốc.
- Theo Triệu, pseudo có 1/3 mẫu đúng loại là bát; 2/3 mẫu còn lại khoanh đĩa. Tin nhắn này không kèm ảnh pseudo riêng để assistant xác nhận độc lập từng mẫu.
- Theo Triệu, final vẫn chỉ phát hiện đúng 2 bát và bỏ sót bát thứ ba, đồng thời có nhiều box thừa/sai loại. Chưa khắc phục việc chọn đúng loại và bỏ sót đối tượng.
- “Chỉ đếm đúng 2 bát” là số bát thật được phát hiện đúng theo review, không phải final_count=2. Dữ liệu lưu vẫn có final_count=31.
- Chưa phân loại từng box, đối sánh vật thật hoặc lượng hóa các box trùng/phần vật; không suy ra tự động có đúng 29 false-positive box chỉ từ số bát được phát hiện.
- Số mẫu đúng loại 1/3 phù hợp bản review của Trí; đây là đối chiếu định tính, chưa phải precision/recall định vị chính thức.

## q02_3 — cups — mcac_11.jpg

- GT MUCCA: 2. Stage 1: 23 box. Final: 26 box.
- Theo Triệu, stage 1 khoanh đúng 2 cốc có quai, các box còn lại khoanh sai sang đĩa, miệng ly và ly. Đây là nhận xét theo ảnh của người review, chưa đối sánh độc lập từng box với vật thật.
- Theo Triệu, pseudo đúng 2/3 mẫu là hai cốc có quai; mẫu còn lại là đĩa. Tin nhắn này không kèm ảnh pseudo riêng để assistant kiểm lại từng mẫu.
- Triệu chưa rõ mẫu sai có phải do phải chọn đủ 3 mẫu hoặc nhầm nghĩa cốc/ly. Theo run_config, max_pseudo=3 là tối đa, không bắt buộc đủ ba. Quy tắc chọn tối đa ba proposal có điểm token mục tiêu >0.23 theo điểm giảm dần; không dùng GT=2 để giới hạn số mẫu. Đĩa được chọn cho thấy một proposal sai loại vẫn lọt bước chọn theo điểm; chưa xác định cơ chế bên trong hoặc chứng minh lỗi nghĩa từ.
- Triệu mô tả final “khoanh sai toàn bộ”. Trong ảnh final đính kèm, assistant vẫn thấy hai khung bao các cốc có quai ở phía trên trái (nhãn hiển thị 19 và 1), bên cạnh nhiều box trên vật khác. Vì vậy ghi kết quả là còn khoanh được hai cốc nhưng lẫn nhiều box sai; không xác nhận mọi box final đều sai.
- Final chưa tách riêng được lớp cups; count 26 so với GT 2. Chưa gán nhãn đầy đủ từng box, chưa suy ra chính xác số box sai/trùng hoặc nguyên nhân từ một mẫu sai.
- Số mẫu đúng loại 2/3 phù hợp review của Trí.

## q03_1 — pens — mcac_200.jpg

- GT MUCCA: 6 bút mực. Stage 1: 17 box. Final: 13 box.
- Triệu xác nhận stage 1 khoanh đúng đủ 6 bút mực, đồng thời khoanh 5 thước và 6 bút chì. Các số theo review cộng thành 17, khớp count lưu.
- Theo Triệu, pseudo gồm 1 bút mực và 2 bút chì: 1/3 mẫu đúng loại, 2/3 sai loại.
- Triệu báo final khoanh tất cả bút và thêm 1 thước. Với 6 bút mực + 6 bút chì + 1 thước, mô tả phù hợp tổng final_count=13; chưa đối sánh độc lập từng box trong lượt ghi nhận này.
- Count giảm 17 → 13 nhưng final vẫn lẫn bút chì và thước, chưa tách riêng được loại pens. Không kết luận giảm count đồng nghĩa đã chọn đúng loại, hoặc mẫu sai là nguyên nhân duy nhất.
- Nhận xét phù hợp review của Trí về mẫu 1/3 và final lẫn cả bút mực, bút chì, một thước.

## q03_2 — rulers — mcac_200.jpg

- GT MUCCA: 6 thước. Stage 1: 18 box. Final: 18 box.
- Theo Triệu, stage 1 khoanh tất cả các món trong ảnh, lẫn bút mực và bút chì cùng thước.
- Pseudo: Triệu xác nhận cả 3 mẫu đều là thước, 3/3 đúng loại. Chưa có xác nhận riêng về mức độ bao trọn từng mẫu trong tin nhắn này.
- Theo Triệu, final vẫn khoanh tất cả các món, không tách riêng loại rulers. Count 18 không tự chứng minh tập tọa độ box stage 1/final giống hệt nhau.
- Đây là ca mẫu đúng loại nhưng final vẫn sai loại trong cấu hình đang kiểm; chưa xác định nguyên nhân bên trong model.
- Nhận xét phù hợp review của Trí về mẫu đúng 3/3 và final lẫn các loại vật.

## q03_3 — pencils — mcac_200.jpg

- GT MUCCA: 6 bút chì. Stage 1: 17 box. Final: 16 box.
- Theo Triệu, stage 1 khoanh tất cả các món. Ghi đây là mô tả khoanh lẫn các loại vật; count lưu là 17 so với 18 vật theo tổng nhãn ảnh, chưa xác nhận mỗi vật đều có box riêng hoặc không bị bỏ sót.
- Pseudo: cả 3 mẫu là bút mực thay vì bút chì, 0/3 đúng loại.
- Theo Triệu, final khoanh tất cả bút và 4 thước. Diễn giải theo mô tả: 6 bút mực + 6 bút chì + 4 thước = 16 box, khớp final_count; chưa kiểm độc lập từng box trong lượt ghi nhận này.
- Final vẫn lẫn loại; count giảm 17 → 16 nhưng chưa tách riêng được bút chì.
- Mẫu sai đi cùng final sai chưa chứng minh mẫu sai là nguyên nhân duy nhất, vì stage 1 đã lẫn loại.
- Nhận xét về số mẫu đúng 0/3 phù hợp review của Trí.

## q04_1 — strawberries — mcac_20.jpg

- GT MUCCA: 6 dâu tây. Stage 1: 60 box. Final: 59 box.
- Triệu mô tả stage 1 khoanh các loại quả trừ việt quất; ghi đây là phạm vi loại vật bị khoanh lẫn, chưa xác nhận mọi quả của các loại còn lại đều được phát hiện hoặc mỗi quả chỉ có một box.
- Pseudo theo Triệu: 2 dâu tây + 1 raspberry, tức 2/3 mẫu đúng loại.
- Final theo Triệu có kết quả như stage 1: vẫn cùng kiểu khoanh lẫn loại. Số box thực tế đổi 60 → 59, chưa xác nhận tập khung giống hệt nhau.
- Chưa đếm riêng được dâu tây. Nhận xét số mẫu đúng 2/3 phù hợp review của Trí.

## q04_2 — blueberries — mcac_20.jpg

- GT MUCCA: 24 việt quất. Stage 1: 43 box. Final: 32 box.
- Triệu mô tả stage 1 khoanh raspberries, việt quất, dâu tây nhưng thiếu 1 quả, và khoanh thêm 3 red currants. Chưa rõ quả bị thiếu thuộc loại nào; chưa đối sánh từng box hoặc xác nhận số quả của từng loại được khoanh.
- Pseudo theo Triệu: 2 việt quất + 1 blackberry, tức 2/3 mẫu đúng loại.
- Theo Triệu, final khoanh toàn bộ việt quất và blackberries, lẫn 1 red currant. Ghi nhận đây là mô tả lớp vật được khoanh; cần kiểm lại độ bao phủ từng quả trước khi xác nhận “toàn bộ”.
- Lý do cần kiểm độ bao phủ: nhãn ảnh có 24 việt quất và 10 blackberries; nếu mỗi quả đều có đúng một box riêng, cộng thêm 1 red currant sẽ là 35 box, khác final_count=32. Không tự sửa lời người review hoặc suy ra chính xác vật bị bỏ sót chỉ từ chênh lệch này.
- Count giảm 43 → 32 nhưng final vẫn lẫn blackberry và red currant, chưa tách riêng blueberries. Chưa kết luận nguyên nhân từ mẫu sai.
- Nhận xét số mẫu đúng 2/3 phù hợp review của Trí.

## q04_3 — red currants — mcac_20.jpg

- GT MUCCA: 39 quả lý chua đỏ. Stage 1: 84 box. Final: 84 box.
- Triệu mô tả cả stage 1 lẫn final khoanh toàn bộ các loại quả. Ghi là khoanh lẫn các loại, chưa xác nhận mọi quả đều được phát hiện và chỉ có một box; tổng nhãn ảnh là 90 vật, khác count lưu 84.
- Pseudo theo Triệu: 1 raspberry + 1 blackberry + 1 dâu tây, tức 0/3 mẫu đúng loại red currants.
- Final vẫn không tách riêng được red currants. Count 84 → 84 không chứng minh tọa độ và tập khung hai lượt giống hệt nhau.
- Nhận xét số mẫu đúng 0/3 phù hợp review của Trí.

## q05_1 — cherries — mcac_27.jpg

- GT MUCCA: 2 cherries. Stage 1: 20 box. Final: 15 box.
- Triệu mô tả stage 1 khoanh tất cả trừ 1 blackberry; ghi là phạm vi các vật/lớp bị khoanh theo quan sát, chưa đối sánh đầy đủ từng box với từng quả.
- Pseudo theo Triệu: 1 cherry + 2 raspberries, tức 1/3 mẫu đúng loại.
- Triệu mô tả final khoanh tất cả trừ 2 blackberries; vẫn lẫn các loại quả khác với cherries, chưa tách riêng loại được hỏi.
- Count lưu giảm 20 → 15. Không đồng nhất mô tả “tất cả trừ...” với một phép đếm đầy đủ: nhãn ảnh có 22 quả, nên cần đối sánh từng vật trước khi kết luận chính xác số bỏ sót hoặc trùng box.
- Số mẫu đúng 1/3 phù hợp review của Trí; chưa xác định quan hệ nhân quả giữa mẫu sai và lỗi final.

## q05_2 — raspberries — mcac_27.jpg

- GT MUCCA: 4 raspberries. Stage 1: 11 box. Final: 14 box.
- Triệu báo stage 1 khoanh đủ raspberries, thêm 1 dâu tây, 2 cherries và 3 việt quất. Nếu mỗi vật tương ứng một box riêng, các số này cộng thành 10, khác count lưu 11; chưa đối sánh từng box để tìm chênh lệch.
- Pseudo theo Triệu: cả 3 mẫu đều đúng là raspberry, 3/3 đúng loại. Chưa có xác nhận riêng rằng từng mẫu bao trọn quả.
- Triệu đã làm rõ final: 1 raspberry bị khoanh 2 lần (2 box cùng một quả), 3 raspberries còn lại mỗi quả được khoanh đúng một lần. Theo mô tả này, cả 4 quả thật được phát hiện và có tổng 5 box trên lớp mục tiêu, gồm 1 box dư do đếm trùng.
- Triệu ban đầu liệt kê thêm 2 blackberries + 2 việt quất + 2 dâu tây + 2 cherries. Sau đó Triệu gửi ảnh final đầy đủ; assistant kiểm ảnh và đối chiếu tọa độ trong prediction, xác định có 3 box trên việt quất (số 9, 12, 13), thay vì 2. Box 13 nhỏ, bao một phần việt quất bên trái quả raspberry tiền cảnh; box 12 cũng chỉ bao một phần việt quất phía trước bên phải.
- Phân loại 14 box theo số trên overlay: raspberry = 1, 2, 3, 7, 11; blackberry = 10, 14; blueberry = 9, 12, 13; strawberry = 5, 6; cherry = 4, 8.
- Box 7 và 11 cùng chỉ quả raspberry ở phía sau bên trái; box 11 bao một phần của cùng quả, nên vừa có dấu hiệu phần vật vừa đếm trùng. Bốn raspberry thật đều có box theo kiểm chéo định tính; tổng 5 box trên lớp mục tiêu gồm 1 box dư do trùng.
- Tổng đã giải thích đủ 14: 4 raspberry thật + 1 box trùng raspberry + 9 box sai loại. Không còn box final chưa phân loại theo lớp; mức độ bao trọn/định vị của mọi box chưa được chấm chính thức.
- Đã quan sát đồng thời sai loại và đếm trùng cùng vật; không dùng 5 box trên raspberry làm 5 quả thật. Đây là kiểm chéo bằng mắt và tọa độ, chưa phải metric định vị benchmark chuẩn.
- Quan sát mẫu đúng 3/3 phù hợp review của Trí. Chưa gọi mẫu đúng là bảo đảm final đúng hoặc chấm precision/recall từ mô tả chưa đối sánh từng box.

## q05_3 — blackberries — mcac_27.jpg

- GT MUCCA: 3 blackberries. Stage 1: 21 box. Final: 79 box.
- Triệu báo stage 1 khoanh tất cả quả trừ 1 dâu tây. Mô tả phù hợp số lượng 22 quả nguồn trừ 1 = 21, nhưng chưa kiểm độc lập từng box/vật trong lượt ghi nhận này.
- Pseudo theo Triệu: 2 blackberries + 1 raspberry, tức 2/3 mẫu đúng loại.
- Triệu báo final vẫn khoanh lẫn các loại quả, trừ 1 dâu tây, đồng thời khoanh cả các phần nhỏ trên blackberry như thể mỗi phần là một quả. Người review gọi các phần nhỏ này là “hạt”; ghi lỗi đơn vị đếm phần vật thay cho cả quả, không tự xác định đó là hạt thật theo nghĩa thực vật học.
- Final đồng thời có dấu hiệu sai loại và sai đơn vị đếm. Một box có thể có nhiều loại lỗi, cần các trường nhãn riêng.
- Count tăng 21 → 79 trong khi GT=3. Chưa phân loại từng box hoặc kết luận mọi box thừa đều là phần quả, box trùng, hay lỗi do một mẫu sai.
- Nhận xét phù hợp review của Trí về số mẫu đúng 2/3 và việc đếm các phần nhỏ của blackberry.

## Cần làm rõ tiếp

- q02_1 đã được Triệu xác nhận: pseudo 3/3 đúng loại và bao trọn đĩa. Không còn câu hỏi chờ Triệu làm rõ về số mẫu đúng trong bản này.
- Tiếp tục review các query còn lại và gán nhãn từng box khi cần lượng hóa lỗi.
- q04_2: làm rõ loại quả bị thiếu ở stage 1; đối sánh final 32 box với từng quả trước khi xác nhận bao phủ toàn bộ 24 việt quất và 10 blackberries.
- q05_2 final đã giải thích đủ 14 box sau khi kiểm ảnh đầy đủ: 5 box trên 4 raspberries và 9 box sai loại (3 blueberry thay vì 2). Stage 1 vẫn còn chênh lệch giữa mô tả 10 và count lưu 11.
- Còn q01_1 chưa có nhận xét kiểm chéo trực tiếp của Triệu trong bản này. Đã có ghi nhận cho 14/15 query, một số chi tiết cần làm rõ như trên.
