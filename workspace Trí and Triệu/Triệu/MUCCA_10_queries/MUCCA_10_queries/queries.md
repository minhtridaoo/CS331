# MUCCA: 10 ảnh, 30 query đếm

Mỗi query đếm một loại vật thể trên toàn ảnh. Dùng **text_prompt** cho ô positive text của CountGD++; dùng **question_en** nếu test một model trả lời câu hỏi. Không cần visual exemplar hoặc negative prompt cho bộ này.

Các query là do mình tạo sau khi xem ảnh. Ground truth lấy từ annotations MUCCA, chưa phải kết quả chạy model. Đây là bộ test nhanh, không phải split đánh giá chính thức.

| Ảnh | Query ID | Prompt cho CountGD++ | Câu hỏi tiếng Anh | Tiếng Việt |
|---|---|---|---|---|
| [mcac_100.jpg](images/mcac_100.jpg) | q01_1 | guitars | How many guitars are in the image? | Trong ảnh có bao nhiêu đàn guitar? |
| [mcac_100.jpg](images/mcac_100.jpg) | q01_2 | amplifiers | How many amplifiers are in the image? | Trong ảnh có bao nhiêu ampli? |
| [mcac_100.jpg](images/mcac_100.jpg) | q01_3 | chairs | How many chairs are in the image? | Trong ảnh có bao nhiêu ghế? |
| [mcac_11.jpg](images/mcac_11.jpg) | q02_1 | plates | How many plates are in the image? | Trong ảnh có bao nhiêu đĩa? |
| [mcac_11.jpg](images/mcac_11.jpg) | q02_2 | bowls | How many bowls are in the image? | Trong ảnh có bao nhiêu bát? |
| [mcac_11.jpg](images/mcac_11.jpg) | q02_3 | cups | How many cups are in the image? | Trong ảnh có bao nhiêu cốc có quai? |
| [mcac_200.jpg](images/mcac_200.jpg) | q03_1 | pens | How many pens are in the image? | Trong ảnh có bao nhiêu bút mực? |
| [mcac_200.jpg](images/mcac_200.jpg) | q03_2 | rulers | How many rulers are in the image? | Trong ảnh có bao nhiêu thước kẻ? |
| [mcac_200.jpg](images/mcac_200.jpg) | q03_3 | pencils | How many pencils are in the image? | Trong ảnh có bao nhiêu bút chì? |
| [mcac_20.jpg](images/mcac_20.jpg) | q04_1 | strawberries | How many strawberries are in the image? | Trong ảnh có bao nhiêu dâu tây? |
| [mcac_20.jpg](images/mcac_20.jpg) | q04_2 | blueberries | How many blueberries are in the image? | Trong ảnh có bao nhiêu việt quất? |
| [mcac_20.jpg](images/mcac_20.jpg) | q04_3 | red currants | How many red currants are in the image? | Trong ảnh có bao nhiêu quả lý chua đỏ? |
| [mcac_27.jpg](images/mcac_27.jpg) | q05_1 | cherries | How many cherries are in the image? | Trong ảnh có bao nhiêu quả anh đào? |
| [mcac_27.jpg](images/mcac_27.jpg) | q05_2 | raspberries | How many raspberries are in the image? | Trong ảnh có bao nhiêu mâm xôi đỏ? |
| [mcac_27.jpg](images/mcac_27.jpg) | q05_3 | blackberries | How many blackberries are in the image? | Trong ảnh có bao nhiêu mâm xôi đen? |
| [mcac_44.jpg](images/mcac_44.jpg) | q06_1 | apples | How many apples are in the image? | Trong ảnh có bao nhiêu táo? |
| [mcac_44.jpg](images/mcac_44.jpg) | q06_2 | pears | How many pears are in the image? | Trong ảnh có bao nhiêu lê? |
| [mcac_44.jpg](images/mcac_44.jpg) | q06_3 | oranges | How many oranges are in the image? | Trong ảnh có bao nhiêu cam? |
| [mcac_58.jpg](images/mcac_58.jpg) | q07_1 | people | How many people are in the image? | Trong ảnh có bao nhiêu người? |
| [mcac_58.jpg](images/mcac_58.jpg) | q07_2 | beach umbrellas | How many beach umbrellas are in the image? | Trong ảnh có bao nhiêu ô che nắng trên bãi biển? |
| [mcac_58.jpg](images/mcac_58.jpg) | q07_3 | chairs | How many chairs are in the image? | Trong ảnh có bao nhiêu ghế? |
| [mcac_81.jpg](images/mcac_81.jpg) | q08_1 | cars | How many cars are in the image? | Trong ảnh có bao nhiêu ô tô? |
| [mcac_81.jpg](images/mcac_81.jpg) | q08_2 | motorbikes | How many motorbikes are in the image? | Trong ảnh có bao nhiêu xe máy? |
| [mcac_81.jpg](images/mcac_81.jpg) | q08_3 | people | How many people are in the image? | Trong ảnh có bao nhiêu người? |
| [mcac_171.jpg](images/mcac_171.jpg) | q09_1 | sheep | How many sheep are in the image? | Trong ảnh có bao nhiêu cừu? |
| [mcac_171.jpg](images/mcac_171.jpg) | q09_2 | goats | How many goats are in the image? | Trong ảnh có bao nhiêu dê? |
| [mcac_171.jpg](images/mcac_171.jpg) | q09_3 | dogs | How many dogs are in the image? | Trong ảnh có bao nhiêu chó? |
| [mcac_176.jpg](images/mcac_176.jpg) | q10_1 | boats | How many boats are in the image? | Trong ảnh có bao nhiêu thuyền? |
| [mcac_176.jpg](images/mcac_176.jpg) | q10_2 | cars | How many cars are in the image? | Trong ảnh có bao nhiêu ô tô? |
| [mcac_176.jpg](images/mcac_176.jpg) | q10_3 | people | How many people are in the image? | Trong ảnh có bao nhiêu người? |

File: `images/` chứa 10 ảnh gốc; `queries.json` chứa 30 query, không có đáp án; `ground_truth.json` chứa đáp án tương ứng; `annotations.json` và `class_mapping.json` giữ nhãn nguồn. Khi chạy model chỉ truyền ảnh và prompt/câu hỏi; dùng ground_truth.json để chấm sau đó.

Nhãn gốc MUCCA dùng `sheeps`; prompt đã sửa thành `sheep` đúng tiếng Anh, class ID 39 được giữ nguyên.
