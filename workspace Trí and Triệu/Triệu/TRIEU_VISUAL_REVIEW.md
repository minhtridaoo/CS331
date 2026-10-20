# Kiểm chéo bằng mắt của Triệu — B2

**Trạng thái: ĐÃ CHỐT v1 — 19/10/2026.** Phạm vi: review định tính **5 ảnh / 15 query** của cấu hình B2 đã lưu. Có thể dùng bản này để bàn giao cho Trí và viết phần phân tích lỗi pilot.

**Giới hạn của bản chốt:** phần ghép chi tiết q02_1 do assistant thực hiện có đánh dấu các nhóm độ chắc chắn vừa; không trình bày thành mọi box đã được Triệu xác nhận. Bản này không xác nhận evaluator/fixture, nhãn bbox benchmark hoặc kiểm chứng độc lập mọi GT đã hoàn tất. Các giới hạn đó được giữ trong nội dung, không phải query còn thiếu review.

Ghi nhận từ nhận xét trực tiếp của Triệu trong chat. Đây là review định tính, chưa phải nhãn độc lập từng bbox hoặc xác nhận mọi ground truth. Số box lấy từ predictions đã lưu. Giữ riêng với USER_VISUAL_REVIEW.md của Trí; không thay thế bản gốc.

## Quy ước review được Triệu xác nhận ngày 19/10/2026

- Trong bộ 15 query này, Triệu chỉ gửi nhận xét chi tiết cho các ca sai; query không được nhận xét là ca đã kiểm và thấy đúng nên bỏ qua. Theo quy ước này, q01_1 được xác nhận đúng định tính, không còn là ca chưa review.
- “Box khoanh đủ vật” nghĩa là box bao trọn vật, trừ các lỗi Triệu đã nêu rõ. Đây không phải xác nhận model tìm đủ mọi vật trong ảnh hoặc không bỏ sót đối tượng.
- Các box chưa được nêu lỗi bao một phần được ghi là bao trọn vật theo xác nhận chung của Triệu. Không tự gán thêm lỗi trùng hoặc phần vật chỉ từ số box chênh lệch.
- Giữ nguyên các lỗi đã nêu cụ thể: ghế q01_3 và bát q02_2 bị bỏ sót; box miệng ly trong q02_1/q02_3; một raspberry bị đếm trùng ở q05_2; các phần nhỏ blackberry bị đếm như quả ở q05_3.
- Bổ sung q02_1 stage 1: Triệu xác nhận hai cặp box trùng 24/26 và 17/28; box 26 chỉ khoanh vùng nhỏ hơn trên cùng đĩa mà box 24 bao toàn bộ. Đây là lỗi trùng/phần vật được nêu rõ sau quy ước chung, được giữ như ngoại lệ đã xác nhận.
- Quan sát trước đó của assistant về box 12/13 ở q05_2 là nhận định thị giác riêng, không thay thế xác nhận của Triệu hoặc tự trở thành nhãn lỗi phần vật trong bản kiểm chéo này.
- Đã có kết luận review định tính cho 15/15 query; việc đối sánh đầy đủ từng bbox/GT và chấm định vị chính thức vẫn là bước riêng.

## q01_1 — guitars — mcac_100.jpg

- GT MUCCA: 25. Stage 1: 25 box. Final: 25 box.
- Theo quy ước được Triệu xác nhận, query này không có nhận xét lỗi vì đã kiểm và thấy đúng. Ghi kết quả stage 1, pseudo và final là đúng theo review định tính của Triệu.
- Pseudo đúng loại 3/3 theo xác nhận chung về ca đúng; các box bao trọn vật theo quy ước review, chưa phải điểm định vị benchmark.

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
- Ở lượt nhận xét đầu, đây là các box sai loại người review đã nhận diện, chưa phải phân loại đầy đủ. Bản đối chiếu bổ sung của assistant cho toàn bộ hai lượt được ghi bên dưới.
- Kiểm từng box ở stage 1, Triệu xác nhận: 10, 19, 25 không phải đĩa. Box 10/19 là hai bát, box 25 là miệng ly theo ảnh và nhận xét trước đó. Các ID là số hiển thị trong stage 1, không áp dụng tự động cho final hoặc pseudo.
- Triệu xác nhận cặp 24/26 cùng một đĩa: 24 bao toàn bộ đĩa, 26 khoanh vùng nhỏ hơn trên chính đĩa đó. Ghi cả trùng vật và khoanh một phần cho box 26.
- Triệu xác nhận cặp 17/28 cùng một đĩa. Chưa chỉ định box nào là đại diện chuẩn; lưu cặp cùng vật, không tự chọn box để loại bỏ.
- Phần Triệu trực tiếp xác nhận có ít nhất 3 box sai loại và 2 nhóm trùng (mỗi nhóm gồm 2 box, tương ứng 2 box dư do trùng). Từ nhận xét còn có thể có cặp khác, assistant đã đối chiếu toàn bộ và bổ sung riêng bên dưới. Prediction, NMS và GT giữ nguyên.
- Triệu xác nhận pseudo đúng cả 3/3 mẫu: cả ba đều là đĩa và bao trọn đĩa. Chốt bản kiểm chéo của Triệu là 3/3 đúng loại, 3/3 bao trọn vật.
- Bản review gốc của Trí ghi 0/3 mẫu đúng; giữ riêng thông tin nguồn này để thấy hai nhận xét khác nhau, không ghi đè bản gốc của Trí. Xác nhận mới của Triệu đã làm rõ nhận xét trong bản kiểm chéo này.
- Triệu báo final khoanh giống stage 1: ghi là cùng kiểu lỗi theo nhận xét; count thay đổi 28 → 31. Đối chiếu từng box của assistant được ghi riêng bên dưới.
- Rà soát bổ sung 19/10 theo yêu cầu Triệu: assistant đã xem từng box riêng ở cả hai lượt, đối chiếu tọa độ và các vị trí nhãn. Đã gán đủ 28 box stage 1 và 31 box final vào bản review riêng: stage 1 = 15 nhóm đĩa + 10 box dư do trùng + 3 sai loại; final = 15 nhóm đĩa + 13 box dư do trùng + 3 sai loại.
- Stage 1, các nhóm cùng đĩa theo assistant: [8,17,28], [2,3], [9,15,21], [14,18], [16,23], [7,27], [12,22], [24,26]. Sai loại: 10,19,25.
- Final, các nhóm cùng đĩa theo assistant: [6,30], [4,9], [3,31], [10,15,21,24,27], [13,17,18], [12,19,28], [22,26], [14,29]. Sai loại: 7,16,25.
- Cách ghép phù hợp 12 vị trí đĩa bên trái + 3 bên phải của GT nguồn 15; không thấy cơ sở đổi GT từ số box model. Một số mép đĩa sát nhau/che khuất chỉ có độ chắc chắn vừa, nên tách đây là review của assistant, chưa coi mọi nhóm là đã được Triệu phân xử hoặc là nhãn bbox benchmark.
- Bảng 15 đĩa, điểm nhãn, ID hai lượt, mức chắc chắn và ảnh đối chiếu: [Q02_1_DETAILED_REVIEW.md](Q02_1_DETAILED_REVIEW.md). Không sửa prediction hoặc dùng các nhóm này để tự chạy NMS.

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
- Pseudo: Triệu xác nhận cả 3 mẫu đều là thước, 3/3 đúng loại; bao trọn vật theo quy ước review bổ sung ngày 19/10/2026.
- Theo Triệu, final vẫn khoanh tất cả các món, không tách riêng loại rulers. Count 18 không tự chứng minh tập tọa độ box stage 1/final giống hệt nhau.
- Đây là ca mẫu đúng loại nhưng final vẫn sai loại trong cấu hình đang kiểm; chưa xác định nguyên nhân bên trong model.
- Nhận xét phù hợp review của Trí về mẫu đúng 3/3 và final lẫn các loại vật.

## q03_3 — pencils — mcac_200.jpg

- GT MUCCA: 6 bút chì. Stage 1: 17 box. Final: 16 box.
- Theo Triệu, stage 1 khoanh tất cả các món. Ghi đây là mô tả khoanh lẫn các loại vật; count lưu là 17 so với 18 vật theo tổng nhãn ảnh, chưa xác nhận mỗi vật đều có box riêng hoặc không bị bỏ sót.
- Assistant kiểm lại stage1.jpg ngày 19/10: 6 bút mực + 6 bút chì + 5 thước = 17 box; thước xanh lá nằm ngang dưới cùng chưa được khoanh. Đã giải thích chênh lệch 17/18, không cần suy ra box trùng hoặc vật mục tiêu bị bỏ sót ở stage này.
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
- Triệu mô tả stage 1 khoanh đủ raspberries, đủ việt quất, 4 dâu tây, và khoanh thêm 3 red currants.
- Assistant kiểm lại stage1.jpg và tọa độ ngày 19/10: 24 box việt quất + 7 blackberry + 5 raspberry + 4 dâu tây + 3 red currants = 43 box. Bản mô tả trước bỏ qua các box blackberry và dùng “đủ raspberries” chưa tương ứng kiểm đếm từng box; giữ nguyên nhận xét người review như nguồn, bổ sung bảng lớp theo ảnh để đối chiếu, chưa tự khẳng định số raspberry thật toàn ảnh.
- Pseudo theo Triệu: 2 việt quất + 1 blackberry, tức 2/3 mẫu đúng loại.
- Triệu xác nhận từ ảnh final có 7 quả blackberry, không phải 10. Sau khi xem ảnh và đối chiếu tọa độ prediction, final gồm 24 box việt quất + 7 box blackberry + 1 box red currant = 32 box, khớp final_count.
- Theo số trên overlay: blackberry = 17, 22, 24, 26, 28, 30, 31; red currant = 32; 24 box còn lại là việt quất. Theo review, đủ 24 việt quất và đủ 7 blackberry nhìn thấy; không còn chênh lệch 35 so với 32 như nhận định trước.
- Nhãn nguồn MUCCA có 10 điểm class blackberry, với các điểm cùng nằm trên một số quả nhìn thấy (ví dụ hai điểm [517,76] và [520,121] trên quả phía trên bên trái). Assistant trước đây lấy số điểm nguồn làm số quả thực tế để đối chiếu là không phù hợp với xác nhận đếm cả quả của Triệu. Giữ 10 điểm nguồn như dữ liệu gốc, ghi 7 quả theo review riêng; không sửa annotations nguồn.
- Final được giải thích là 24 vật đúng loại và 8 box sai loại (7 blackberry + 1 red currant) theo kiểm chéo định tính. Chênh lệch này không làm thay đổi GT mục tiêu blueberries=24 hoặc số đếm model.
- Count giảm 43 → 32 nhưng final vẫn lẫn blackberry và red currant, chưa tách riêng blueberries. Chưa kết luận nguyên nhân từ mẫu sai.
- Nhận xét số mẫu đúng 2/3 phù hợp review của Trí.

## q04_3 — red currants — mcac_20.jpg

- GT MUCCA: 39 quả lý chua đỏ. Stage 1: 84 box. Final: 84 box.
- Triệu mô tả cả stage 1 lẫn final khoanh toàn bộ các loại quả. Ghi là khoanh lẫn các loại, chưa xác nhận mọi quả đều được phát hiện và chỉ có một box; tổng nhãn nguồn ảnh là 90 điểm, không tự đồng nhất với 90 quả thực tế. Riêng blackberry đã được Triệu xác nhận 7 quả nhìn thấy so với 10 điểm nguồn; cần kiểm riêng nếu muốn lượng hóa độ bao phủ tất cả các loại.
- Pseudo theo Triệu: 1 raspberry + 1 blackberry + 1 dâu tây, tức 0/3 mẫu đúng loại red currants.
- Final vẫn không tách riêng được red currants. Count 84 → 84 không chứng minh tọa độ và tập khung hai lượt giống hệt nhau.
- Nhận xét số mẫu đúng 0/3 phù hợp review của Trí.

## q05_1 — cherries — mcac_27.jpg

- GT MUCCA: 2 cherries. Stage 1: 20 box. Final: 15 box.
- Triệu mô tả stage 1 khoanh tất cả trừ 1 blackberry; ghi là phạm vi các vật/lớp bị khoanh theo quan sát, chưa đối sánh đầy đủ từng box với từng quả.
- Pseudo theo Triệu: 1 cherry + 2 raspberries, tức 1/3 mẫu đúng loại.
- Triệu mô tả final khoanh tất cả trừ 2 blackberries; vẫn lẫn các loại quả khác với cherries, chưa tách riêng loại được hỏi.
- Count lưu giảm 20 → 15. Không đồng nhất mô tả “tất cả trừ...” với một phép đếm đầy đủ: nhãn ảnh có 22 quả, nên cần đối sánh từng vật trước khi kết luận chính xác số bỏ sót hoặc trùng box.
- Assistant kiểm lại hai overlay và tọa độ ngày 19/10: stage 1 có 4 raspberry + 2 cherry + 2 dâu tây + 2 blackberry + 10 việt quất = 20 box; final có 4 raspberry + 2 cherry + 2 dâu tây + 1 blackberry + 6 việt quất = 15 box. Vì vậy final không chỉ thiếu 2 blackberry; còn ít box việt quất hơn stage 1. Số 11 việt quất trong GT nguồn cần được phân biệt với kiểm đếm quả thật nếu đánh giá độ bao phủ định lượng.
- Số mẫu đúng 1/3 phù hợp review của Trí; chưa xác định quan hệ nhân quả giữa mẫu sai và lỗi final.

## q05_2 — raspberries — mcac_27.jpg

- GT MUCCA: 4 raspberries. Stage 1: 11 box. Final: 14 box.
- Nhận xét ban đầu của Triệu về stage 1 là đủ raspberries, thêm 1 dâu tây, 2 cherries và 3 việt quất, cộng thành 10 thay vì 11 box. Chênh lệch này đã được kiểm và giải thích ở dòng kế tiếp.
- Assistant kiểm lại stage1.jpg và tọa độ ngày 19/10: có 2 dâu tây (box 6 và 7), thay vì 1 trong mô tả trước. Đủ 11 box được giải thích: 4 raspberry (1,2,3,4) + 2 cherry (5,8) + 2 dâu tây (6,7) + 3 việt quất (9,10,11). Đã giải quyết chênh lệch 10/11, không tự thêm lỗi trùng.
- Pseudo theo Triệu: cả 3 mẫu đều đúng là raspberry, 3/3 đúng loại; bao trọn vật theo quy ước review bổ sung ngày 19/10/2026.
- Triệu đã làm rõ final: 1 raspberry bị khoanh 2 lần (2 box cùng một quả), 3 raspberries còn lại mỗi quả được khoanh đúng một lần. Theo mô tả này, cả 4 quả thật được phát hiện và có tổng 5 box trên lớp mục tiêu, gồm 1 box dư do đếm trùng.
- Triệu ban đầu liệt kê thêm 2 blackberries + 2 việt quất + 2 dâu tây + 2 cherries. Sau đó Triệu gửi ảnh final đầy đủ; assistant kiểm ảnh và đối chiếu tọa độ trong prediction, xác định có 3 box trên việt quất (số 9, 12, 13), thay vì 2. Assistant trước đây cho rằng box 12/13 bao một phần quả; sau xác nhận chung ngày 19/10 của Triệu, các box này được ghi sai loại, không tự chốt thêm lỗi phần vật. Giữ nhận định cũ như lịch sử quan sát riêng.
- Phân loại 14 box theo số trên overlay: raspberry = 1, 2, 3, 7, 11; blackberry = 10, 14; blueberry = 9, 12, 13; strawberry = 5, 6; cherry = 4, 8.
- Box 7 và 11 cùng chỉ quả raspberry ở phía sau bên trái, xác nhận lỗi đếm trùng. Assistant trước đây còn nhận xét box 11 bao một phần quả; Triệu chỉ chốt lỗi trùng cho ca này, nên không tự gán thêm nhãn phần vật. Bốn raspberry thật đều có box theo kiểm chéo định tính; tổng 5 box trên lớp mục tiêu gồm 1 box dư do trùng.
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
