# CS331 — mở trang này để làm tiếp

> **MỚI NHẤT — 05/11 tối: ĐÃ CHỐT D1–D10** (Trí đồng ý toàn bộ khuyến nghị qua chat; nghiệm thu V3–V6; đồng ý duyệt pilot, chờ Triệu ghi xác nhận).
> - **Triệu làm tiếp, không cần chờ Trí:** [HANDOFF/GIAO_VIEC_TRIEU_20261106.md](HANDOFF/GIAO_VIEC_TRIEU_20261106.md). Gồm W1 rút dữ liệu dev 20 + test 40 (06/11); W2 đưa output P1 vào repo; W3 ghi duyệt pilot; W4 kiểm test 40 ảnh; W5 khóa (08/11); W6 chạy dev trên T4 (10/11).
> - **Trí 07–08/11:** kiểm absent/GT tập dev 20 ảnh (khoảng 1 giờ), sau khi Triệu rút xong W1. **Assistant (khi Trí mở phiên):** viết công cụ ngoại tuyến cho T, chọn lại ngưỡng S/F riêng từng nguồn, chấm theo luật D9 (trước 09/11).

> **MỚI NHẤT — 05/11 (đã kiểm nội dung):** V4, V6, P1 (code + pilot T4) và đề xuất dữ liệu v2 của Triệu **đạt kiểm**. Kế hoạch + 10 quyết định có khuyến nghị: [reports/KE_HOACH_TIEP_THEO_20261105.md](reports/KE_HOACH_TIEP_THEO_20261105.md).
> - Ghép tầng B với bảng tra: ở ca model làm tốt, Fusion giữ 40/40 khung đúng nhưng vẫn xóa 11/11 vật đúng (E3); mẫu tự chọn đúng 6/6. Vậy bộ lọc cuối luôn làm mất vật đúng; thử **P không kèm lọc** và **T** (chỉ điểm chữ ở lượt 2, tính ngoại tuyến từ raw).
> - **Việc đầu tiên 06/11 (Trí, khoảng 1 giờ):** chốt D1–D10 (khuyến nghị: T4 làm máy chuẩn; C6 chọn lại ngưỡng riêng từng nguồn; dev 20 + test 40; 3–40 điểm; luật chọn cuối D9) + duyệt pilot V7 với Triệu → Triệu rút dữ liệu thật.

> **Trạng thái hiện hành — nhận bài nộp 05/11/2026:** đã pull `3b7df25 → 71264bd` (9 commit, 19 file), không xung đột. Triệu đã nộp báo cáo V4, 6 CSV N4 tầng B/V6 (báo cáo 58/58), code/notebook nhánh P1 và công cụ đối chứng. [Báo cáo T4](reports/TRIEU_P1_COLAB_T4_20261103.md) ghi đã chạy pilot và bảng đối chứng; dự đoán/log gốc P1 ở Drive của Triệu, chưa có trong repo để đối chiếu độc lập ở lượt này. Đã nhận bài nộp không thay nghiệm thu của Trí hoặc V7 duyệt chung.
> **Việc tiếp:** Trí đọc mục 4 và 6 báo cáo T4 (máy chuẩn, tiêu chí tái hiện, đối chứng C6), rồi mục 4 [đề xuất dữ liệu v2](reports/TRIEU_DE_XUAT_QUY_TAC_DU_LIEU_V2_20261104.md); nhận output P1/V4 gốc, rà nhãn N4 còn vướng và duyệt chung. Chưa rút tập dev/test thật theo báo cáo. Không kết luận P1 đã tốt hơn từ 5 ảnh pilot; nguyên nhân lệch T4/A2000 chưa được xác minh. Lượt này chỉ pull/đọc/đồng bộ tài liệu, không chạy thực nghiệm. Các ghi chú cũ bên dưới giữ làm lịch sử; ưu tiên mục này và bảng resume.

> **Rà lại 29/10 — ưu tiên hơn phần tổng hợp trước:** [Kiểm việc Triệu và nguyên nhân lỗi N4](reports/RA_SOAT_TRIEU_N4_20261029.md). V1–V2 đã nộp đủ 117 dòng, khớp nguồn; V3–V7 còn chờ và chưa quá hạn. Khung sai loại có từ dự đoán trước khi Triệu review; raw lượt hai cho thấy điểm mẫu ảnh có thể lấn át điểm chữ. Crop nới lề nhưng thiếu biên bbox thật, một số nhãn/ID cần đối chiếu. **Chưa đủ bằng chứng kết luận E1 là nguyên nhân chủ đạo hoặc bỏ R; các đề xuất trước chỉ là tạm thời.** Không chạy thêm thí nghiệm hay ký nghiệm thu thay Trí.

> **Đồng bộ Git đã xác nhận — 27/10/2026:** đã push commit [`e877541`](https://github.com/minhtridaoo/CS331/commit/e8775412f84f0927a6fe692f1f106bf53aacd369) lên `origin/main`; HEAD local khớp remote. Code, kết quả P4.6, gói N4 và phân công đã có trên GitHub. Bản ZIP sao lưu trong `quá khứ/`, dữ liệu MUCCA gốc và checkpoint vẫn ở máy.
> **Việc tiếp theo:** Trí gửi đường dẫn [giao việc cho Triệu](HANDOFF/GIAO_VIEC_TRIEU_20261028.md), nghiệm thu phần kiểm chéo đã đạt và chốt quy tắc dữ liệu mới. Triệu làm N4 tầng A (V1–V2); chưa xác nhận đã nhận/hoàn thành.
> **Trạng thái ưu tiên:** P4.6a–b đã xong; tập 10 ảnh/30 query đã khóa và P4.6c–d phần count đã chạy. Hiện ở N4 review khung, chưa chọn nhánh cải tiến P/R. Các hướng dẫn chuẩn bị C2/C3 và câu “chưa push/chưa chạy ảnh mới” còn lại bên dưới mô tả thời điểm trước; không phải việc phải làm lại. Lượt đồng bộ Git này không chạy thí nghiệm.

**Chuyển sang session mới:** mở [BAT_DAU_SESSION_MOI.md](BAT_DAU_SESSION_MOI.md) để đọc bản bàn giao tổng hợp và câu mở đầu sẵn dùng.

**Cập nhật và kiểm kết quả: 27/10/2026, đã pull d6db189.** Nhóm: Trí và Triệu. Model đang dùng: **CountGD++**.

**Điểm tiếp tục mới nhất:** C1 đã làm — Trí đọc và **chưa duyệt** phần kiểm chéo. Triệu tự làm [T1–T4 theo kế hoạch V2](reports/KE_HOACH_SUA_KIEM_CHEO_20261027.md); đã có [ZIP đầu vào](HANDOFF/TRIEU_T1_T4_20261027_v2.zip) local, chưa gửi/commit/push. T1 30/10, T2 01/11, T3 02/11, T4 03/11 là hạn đề xuất.

**Trí làm song song:** P4.6c–d (count) **XONG 27/10**: trên 30 query mới, MAE cả 30 = B2 gốc 13.00 / lọc điểm 7.27 / **Fusion 5.53** (Fusion tốt hơn lọc điểm, CI [−3.2, −0.3]). B0 tham chiếu 6.77, và B0 tốt nhất trên query có mặt (5.70). Bộ lọc bỏ ~50% vật đúng; X/Y vẫn còn lỗi (hỏi people ra chó/xe; sheep/bicycles gần nghĩa bị đếm). [Báo cáo](reports/P4_6_UNSEEN_RESULTS_20261027.md). CountGD++ vẫn là model đếm, CLIP phụ trợ; 47 nhãn q03 riêng cho P4.

**Pull 36eaf96 (27/10 tối):** Triệu tự kiểm chéo Phần 2: self-test, tính lại bằng Excel, 5 ca dữ liệu hỏng, chạy lại evaluator (trùng run 20/10), tự gán nhãn q05_2. Assistant đánh giá ([đánh giá](reports/DANH_GIA_TRIEU_TU_KIEM_20261027.md)): nhận xét 1 + q05_2 **đạt**; còn thiếu q05_3 gán nhãn từng khung (79 + 21), 2 ca thử (uncertain, absent > 0), phân tích B2/B0 + đề xuất cải thiện. Trí chưa nghiệm thu.

**Hướng cải tiến (27/10 tối):** Trí đưa đề xuất trong `hướng cái tiển/` (nhánh P kiểm mẫu tự chọn / nhánh R bộ lọc giữ vật đúng, dev và test mới). Kế hoạch thực thi: `roadmap/KE_HOACH_CAI_TIEN_20261027.md`. **Việc đầu tiên là N4 tầng A** (gói chính + `bo_sung_F0/`) để chọn P hoặc R. Chỉ báo tự động: E1 (mẫu sai) và E3 (Fusion xóa vật đúng) đều lớn. MUCCA chỉ còn 19–34 ảnh có cặp khác siêu nhóm, nên tập mới phải thêm cặp dễ nhầm.

**N4 (27/10):** gói review khung chọn lọc, mù với cách lọc, đã sẵn ở `results/countgdpp/p4_n4_review_package_20261027/`. Tầng A gồm 7 query / 78 khung (4 query people + 3 query vắng mặt bị báo sai), tầng B gồm 2 query / 41 khung. Trí điền CSV rồi assistant ghép với bảng tra. Tóm tắt toàn dự án cho demo: `reports/TOM_TAT_DU_AN_20261027.md`.

**Hạn báo cáo cuối: 02/12/2026.** Lịch dự kiến và cách xử lý kiểm chéo chưa đủ nằm ở checklist §5A; không cần làm lại toàn pilot.

> **MỚI NHẤT — 02/11:** đã pull `71009c8`. Triệu nộp **V3** (q05_3, 103 khung: B2 tăng 58 khung `part` dù 2/3 mẫu đúng loại) và **V5** (tập mới: B2 kém B0 ở 15/30 query; đề xuất nhánh P). Cả hai đạt kiểm. **Chưa có V4 (2 ca thử) và V6 (tầng B, hạn 02/11).** Đánh giá: [reports/DANH_GIA_TRIEU_V3_V5_20261102.md](reports/DANH_GIA_TRIEU_V3_V5_20261102.md).
> - Bằng chứng mới ([RA_SOAT](reports/RA_SOAT_TRIEU_N4_20261029.md) §3): ở lượt 2, điểm khung = max(token chữ, token mẫu ảnh), nên ô tô giữ nhờ điểm mẫu 0,97 dù điểm chữ "people" chỉ 0,04. Gợi ý thêm biến thể **T (chấm lượt 2 chỉ bằng token chữ)** cạnh P; R giữ dự phòng; C6 bắt buộc.
> - **Buổi 03/11:** Trí + Triệu duyệt pilot (V7), chốt danh sách biến thể thử trên dev và quy tắc dữ liệu dev 20 + test 40. Nhắc Triệu V4 + V6, hạn 04/11.

> **MỚI NHẤT — 29/10:** đã pull `be4da26`. **Triệu xong N4 tầng A (V1 + V2) đúng hạn**; nhãn đạt kiểm (117 dòng, tọa độ không đổi; Trí và Triệu đồng ý 9/9 ở u01_1). Kết quả: [reports/N4_KET_QUA_TANG_A_20261029.md](reports/N4_KET_QUA_TANG_A_20261029.md).
> - Khung bộ lọc giữ trong 7 query lỗi: **0 vật đúng** (lọc điểm 0/78, Fusion 0/14). Hỏi "people" ở mcac_88 thì 21/21 khung trùng khung "cars".
> - Mẫu tự chọn: **1/21 đúng loại** (E1 chiếm ưu thế). Người thật bị lọc mất: 13/18 ứng viên E3.
> - **Đề xuất: nhánh P** (kiểm mẫu bằng CLIP + điều kiện một vật), C6 làm đối chứng bắt buộc, **bỏ nhánh R** (R sẽ cứu nhầm chó/ô tô). **Chờ Trí quyết.**
> - Triệu tiếp V3 q05_3, V4, V5 (hạn 01/11) và V6 tầng B (02/11).

> **MỚI NHẤT — 27/10 khuya (Trí nghỉ, giao việc):**
> - **Vị trí pipeline + lịch đến 02/12:** [roadmap/VI_TRI_PIPELINE_20261028.md](roadmap/VI_TRI_PIPELINE_20261028.md).
> - **N4 giao Triệu** (hạn 30/10). Trí đã chấm u01_1 (9/9: 7 wrong_class chó, 2 multi_object chó). Việc của Triệu V1–V7, kèm gợi ý V8–V10 làm thay Trí: [HANDOFF/GIAO_VIEC_TRIEU_20261028.md](HANDOFF/GIAO_VIEC_TRIEU_20261028.md). Gói gửi: `HANDOFF/TRIEU_GIAO_VIEC_20261028.zip` (thay ZIP V2 cũ chưa gửi).
> - **Việc đầu tiên của Trí ngày 28/10 (45 phút):** commit + push **đã xong 27/10** → gửi Triệu file giao việc → nghiệm thu bản tự kiểm của Triệu → chốt quy tắc dữ liệu dev 20 + test 40.

## 1. Đồ án đang giải quyết gì?

Cùng một ảnh có X và Y khác loại: hỏi X thì đếm X, đổi sang Y thì phải đếm Y. Nhóm đang kiểm tra CountGD++ mắc lỗi gì trong tình huống này, rồi mới chọn một cách cải thiện có thể đo được.

**Baseline** là cấu hình gốc dùng làm mốc so sánh. **Pilot** nghĩa là *bộ thử nhỏ để khám phá lỗi*: ở đây là **5 ảnh / 15 câu hỏi bằng văn bản**, không phải tên model hay một đồ án khác.

| Nhánh | Làm để biết gì? | Hiện có gì? |
|---|---|---|
| **Pilot — 5 ảnh, 15 câu hỏi** | Khi đổi đối tượng cần đếm, model có khoanh đúng loại không? Sai ở mẫu tự chọn hay kết quả cuối? | Đã chạy B0/B2; Trí và Triệu đều review định tính 15/15. Evaluator đã chạy, số liệu khớp; Triệu đã chấp nhận bản kiểm được ủy quyền, còn duyệt chung để đóng vòng này. |
| **Benchmark FSCD-147 — 1.190 ảnh test** | Chạy cấu hình theo paper trên tập chuẩn, kiểm kết quả đếm tổng thể. | **Đã chạy đủ và kiểm log ngày 20/10:** MAE **8.336975**, RMSE **24.637626**. [Bản kết quả để báo cáo](reports/BENCHMARK_FSCD147.md). |

B0 = ảnh + văn bản, chạy một lượt. B2 = lượt đầu → lấy tối đa 3 khung làm mẫu tự chọn → chạy lượt hai. Pilot B0/B2 không có đầy đủ synthetic exemplars và adaptive cropping như nhánh benchmark. Vì khác dữ liệu và cấu hình, không lấy hai bảng MAE để tính mức cải thiện cho nhau.

## 2. Làm tiếp ở đâu?

Mở [CHECKLIST_3_GIO](roadmap/CHECKLIST_3_GIO.md) để xem điểm dừng. C1–C3 và P4.6c xong; tiếp N4 (review khung) / P5 báo cáo. Triệu nhận T0 rồi tự thực hiện T1–T4.

Evaluator không bị sửa trong lượt rà phân công. T1 dùng fixture đầy đủ 15 query, chỉ sửa q01_1 và giữ q05_2, tránh lỗi manual check không liên quan. Các kết quả P4 dev khác cấu hình: B2 confidence 4.6, CLIP-only 6.8, Fusion 5.8. Mục tiêu là kiểm chứng hiệu quả, không bắt kết quả phải tốt hơn.

Kế hoạch giới hạn ở 7 ca evaluator, hai query q05 và báo cáo ngắn; chưa được nhóm duyệt, chưa coi Triệu đã nhận/chạy. Giữ các mốc 08/11 dữ liệu/runner, 15/11 kết quả, 22/11 bản thảo, 29/11 hoàn thiện, 02/12 báo cáo cuối.

## 3. Chỉ cần nhớ ba file

| Cần gì? | Mở ở đâu? |
|---|---|
| Biết đang ở đâu, điều kiện nào để xong | [roadmap/ROADMAP.md](roadmap/ROADMAP.md) — bảng tiến độ chính |
| Ghi hôm nay đã chạy gì và bước kế | [WORKLOG.md](WORKLOG.md) — nhật ký chung duy nhất |
| Trở lại sau vài ngày, xem bước tiếp và chia việc | [HANDOFF/HANDOFF.md](HANDOFF/HANDOFF.md) — bản bàn giao hiện hành |

Mỗi buổi bạn chỉ cần thêm một mục vào WORKLOG. Khi hoàn thành một mốc, đồng bộ dòng trạng thái ở ROADMAP và bước tiếp ở HANDOFF. Không phải chép toàn bộ nhật ký vào ba file. Assistant sẽ đồng bộ khi bạn nhờ kiểm tiến độ, không có tác vụ tự cập nhật nền.

## 4. Bản đồ thư mục — mỗi nơi một vai trò

| Thư mục/file | Chứa gì? | Bạn dùng lúc nào? |
|---|---|---|
| `roadmap/` | Kế hoạch, hướng dẫn phần 2–3 và P4; pipeline, notebook chi tiết | Đọc hướng dẫn; sửa trạng thái ở ROADMAP |
| `HANDOFF/` | Bước tiếp chung và phân công riêng Trí/Triệu | Trở lại làm việc hoặc bàn giao |
| `reports/` | Tổng kết pilot đang viết; kết quả benchmark đã kiểm | Viết kết luận, chuẩn bị báo cáo thầy |
| `experiments/countgdpp/` | Code chạy B0/B2/E1/E2 và input pilot đã chuẩn hóa | Khi cần đọc/chạy thí nghiệm |
| `evaluation/` | Evaluator pilot và script chấm CLIP/phân tích P4 | Phần 2 hoặc đọc quy trình P4; chưa có runner tập mới đã kiểm |
| `results/countgdpp/` | Dự đoán, overlay, review của từng run pilot | Xem bằng chứng; không sửa dự đoán gốc |
| `workspace Trí and Triệu/` | Gói dữ liệu/review bàn giao; kết quả Kaggle bạn tải về | Giữ tài nguyên của từng người; xem bản đồ bên dưới |
| `CountGDPlusPlus/` | Repo model đang dùng, checkpoint và thư viện | Chạy/đọc model; không dọn đổi vị trí tùy ý |
| `CLIP-Count/` | Repo tham khảo từ hướng cũ | Không có công việc hiện tại bắt buộc trong đây |
| `quá khứ/` | Bản tài liệu cũ và bản lưu trước sửa | Chỉ tra lịch sử hoặc khôi phục. [Đọc giải thích](<quá khứ/README.md>). |
| `.kilo/`, `.gitignore`, `.gitattributes`, `environment_countgdpp.txt` | Cấu hình công cụ và ghi nhận môi trường | Không phải đầu việc mới |

Đường dẫn được giữ ổn định để các lệnh đang dùng tiếp tục hoạt động; việc sắp xếp lần này tập trung vào trang chỉ đường, trạng thái và tách lịch sử khỏi hướng dẫn hiện tại.

## 5. Mở bằng chứng để báo cáo tiến độ

- **Kết quả benchmark:** [bản đọc nhanh](reports/BENCHMARK_FSCD147.md) → [metrics gốc](<workspace Trí and Triệu/Trí/countgdpp_paper_results/full_20261015T080230Z/metrics.json>) và [console.log](<workspace Trí and Triệu/Trí/countgdpp_paper_results/full_20261015T080230Z/console.log>).
- **Lỗi khi đổi đối tượng:** [báo cáo pilot đang viết](reports/PILOT_SUMMARY.md) → [review Triệu đã chốt](<workspace Trí and Triệu/Triệu/TRIEU_VISUAL_REVIEW.md>).
- **Triệu đã bàn giao:** [review gốc](<workspace Trí and Triệu/Triệu/TRIEU_VISUAL_REVIEW.md>).

- **P4 đã thăm dò:** [báo cáo](reports/P4_CLIP_EXPLORATORY_FINDINGS_20261021.md) và [audit](reports/P4_AUDIT_20261022.md).

Câu báo cáo ngắn: “Nhóm đã chạy CountGD++ và đo lỗi đổi loại đối tượng trên pilot. Đã thử lọc bằng điểm model, CLIP và kết hợp 50/50; đối chứng đơn giản hiện tốt hơn Fusion về MAE dev. Nhóm đã khóa ứng viên, đang chờ kiểm nhãn độc lập và chuẩn bị đánh giá trên ảnh mới.”
