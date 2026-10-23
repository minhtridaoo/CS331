# CS331 — mở trang này để làm tiếp

**Cập nhật xác nhận: 24/10/2026.** Nhóm: Trí và Triệu. Model đang dùng: **CountGD++**.

**Bạn đang gần khép lại giai đoạn chạy baseline và tìm lỗi.** Benchmark trên tập chuẩn đã chạy đủ. **Phần 2 đã chạy và output đã đối chiếu; Phần 3 đã điền báo cáo; Triệu đã đọc/hiểu và chấp nhận bản kiểm kỹ thuật do assistant thực hiện, còn nhóm duyệt.** Việc tiếp là duyệt báo cáo chung và đồng bộ log P4. Phần cải tiến và kiểm chứng cải tiến vẫn ở phía sau.

## 1. Đồ án đang giải quyết gì?

Cùng một ảnh có X và Y khác loại: hỏi X thì đếm X, đổi sang Y thì phải đếm Y. Nhóm đang kiểm tra CountGD++ mắc lỗi gì trong tình huống này, rồi mới chọn một cách cải thiện có thể đo được.

**Baseline** là cấu hình gốc dùng làm mốc so sánh. **Pilot** nghĩa là *bộ thử nhỏ để khám phá lỗi*: ở đây là **5 ảnh / 15 câu hỏi bằng văn bản**, không phải tên model hay một đồ án khác.

| Nhánh | Làm để biết gì? | Hiện có gì? |
|---|---|---|
| **Pilot — 5 ảnh, 15 câu hỏi** | Khi đổi đối tượng cần đếm, model có khoanh đúng loại không? Sai ở mẫu tự chọn hay kết quả cuối? | Đã chạy B0/B2; Trí và Triệu đều review định tính 15/15. Evaluator đã chạy, số liệu khớp; Triệu đã chấp nhận bản kiểm được ủy quyền, còn nhóm duyệt phần 2–3 để đóng vòng này. |
| **Benchmark FSCD-147 — 1.190 ảnh test** | Chạy cấu hình theo paper trên tập chuẩn, kiểm kết quả đếm tổng thể. | **Đã chạy đủ và kiểm log ngày 20/10:** MAE **8.336975**, RMSE **24.637626**. [Bản kết quả để báo cáo](reports/BENCHMARK_FSCD147.md). |

B0 = ảnh + văn bản, chạy một lượt. B2 = lượt đầu → lấy tối đa 3 khung làm mẫu tự chọn → chạy lượt hai. Pilot B0/B2 không có đầy đủ synthetic exemplars và adaptive cropping như nhánh benchmark. Vì khác dữ liệu và cấu hình, không lấy hai bảng MAE để tính mức cải thiện cho nhau.

## 2. Hôm nay chỉ làm theo thứ tự này

1. **Phần kiểm kỹ thuật đã có xác nhận của Triệu.** Assistant đã đối chiếu 15 query và ghi [bản kết quả](reports/TRIEU_KET_QUA_KIEM_CHEO_20261024.md); Triệu xác nhận đã đọc/hiểu và đồng ý dùng kết quả ngày 24/10 tại PILOT_SUMMARY mục 7. Không ghi Triệu đã tự audit code. Hai run `pilot_eval_20261020` và `_r2` có kết quả giống nhau; không cộng thành mẫu độc lập.
2. **Trí và Triệu duyệt Phần 3.** [PILOT_SUMMARY](reports/PILOT_SUMMARY.md) đã có run, số liệu và kế hoạch P4. Điền phiếu xác nhận ở mục 7; [hướng dẫn phần 3](roadmap/PHAN_3_TONG_KET.md) chỉ rõ mục còn lại.
3. **Trí đồng bộ trạng thái P4:** repo đã có score CLIP và báo cáo khảo sát count ngày 20/10, khác các câu “chưa triển khai” trong tài liệu trước đó. Cần ghi rõ người/lệnh/config, audit kết quả và duyệt kế hoạch ở mục 6 báo cáo; lượt hỗ trợ evaluator ngày 21/10 chưa thay việc audit/duyệt P4.

**“Phần 2, phần 3” là hai công việc chốt pilot; không phải E2/E3 hoặc cell Kaggle.** Phần chạy, đối chiếu kỹ thuật và xác nhận đọc/chấp nhận của Triệu đã có. Duyệt toàn báo cáo và quyết định đóng pilot/P4 thuộc nhóm.

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
| `roadmap/` | Kế hoạch, hướng dẫn phần 2–3; pipeline và notebook chi tiết | Đọc hướng dẫn; sửa trạng thái ở ROADMAP |
| `HANDOFF/` | Bước tiếp chung và phân công riêng Trí/Triệu | Trở lại làm việc hoặc bàn giao |
| `reports/` | Tổng kết pilot đang viết; kết quả benchmark đã kiểm | Viết kết luận, chuẩn bị báo cáo thầy |
| `experiments/countgdpp/` | Code chạy B0/B2/E1/E2 và input pilot đã chuẩn hóa | Khi cần đọc/chạy thí nghiệm |
| `evaluation/` | Code chấm kết quả đã có | Phần 2 |
| `results/countgdpp/` | Dự đoán, overlay, review của từng run pilot | Xem bằng chứng; không sửa dự đoán gốc |
| `workspace Trí and Triệu/` | Gói dữ liệu/review bàn giao; kết quả Kaggle bạn tải về | Giữ tài nguyên của từng người; xem bản đồ bên dưới |
| `CountGDPlusPlus/` | Repo model đang dùng, checkpoint và thư viện | Chạy/đọc model; không dọn đổi vị trí tùy ý |
| `CLIP-Count/` | Repo tham khảo từ hướng cũ | Không có công việc hiện tại bắt buộc trong đây |
| `quá khứ/` | Bản tài liệu cũ và bản lưu trước sửa | Chỉ tra lịch sử hoặc khôi phục. [Đọc giải thích](<quá khứ/README.md>). |
| `.kilo/`, `.gitignore`, `.gitattributes`, `environment_countgdpp.txt` | Cấu hình công cụ và ghi nhận môi trường | Không phải đầu việc mới |

Đường dẫn được giữ ổn định để các lệnh đang dùng tiếp tục hoạt động; việc sắp xếp lần này tập trung vào trang chỉ đường, trạng thái và tách lịch sử khỏi hướng dẫn hiện tại.

## 5. Mở bằng chứng để báo cáo tiến độ

- **Kết quả benchmark:** [bản đọc nhanh](reports/BENCHMARK_FSCD147.md) → [metrics gốc](<workspace Trí and Triệu/Trí/countgdpp_paper_results/full_20261015T080230Z/metrics.json>); `console.log` được báo cáo benchmark tham chiếu nhưng chưa có trong checkout này.
- **Lỗi khi đổi đối tượng:** [báo cáo pilot đang viết](reports/PILOT_SUMMARY.md) → [review Triệu đã chốt](<workspace Trí and Triệu/Triệu/TRIEU_VISUAL_REVIEW.md>).
- **Triệu đã bàn giao:** [review gốc](<workspace Trí and Triệu/Triệu/TRIEU_VISUAL_REVIEW.md>).

Câu báo cáo ngắn: “Nhóm đã chạy CountGD++ trên 1.190 ảnh FSCD-147 và kiểm lại chỉ số đếm. Song song, nhóm đã thử 5 ảnh với 15 câu hỏi để phân tích lỗi đếm nhầm loại. Nhóm đã chấm lại pilot; Triệu đã chấp nhận kết quả kiểm được ủy quyền, còn chờ duyệt báo cáo và đồng bộ khảo sát P4.”
