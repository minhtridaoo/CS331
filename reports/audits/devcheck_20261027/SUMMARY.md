# Kiểm triển khai P4.6b trên dev — 27/10/2026

**Người chạy:** assistant, theo yêu cầu trực tiếp của Trí ngày 27/10. **Phạm vi:** 5 ảnh / 15 query dev (`m4_inputs/first5_inputs.jsonl`). Đây là kiểm xem runner mới có tái lập đúng pipeline cũ hay không, **không phải kết quả thí nghiệm mới hay holdout**.

| Bước | Lệnh | Kết quả |
|---|---|---|
| (1) Freeze trên điểm lưu sẵn (CPU, Windows) | `p4_apply_freeze.py --scores results/countgdpp/p4_clip_all15_20261020 --run-id p4_freeze_devcheck_20261027 --check-audit …` | `CHECK audit: PASS`: B2_threshold/Fusion khớp audit 21/10 ở 15/15 query |
| (2) B2 trên GPU (WSL `Ubuntu-22.04`, venv `countgdpp`, torch 2.5.1+cu121, RTX A2000 4 GB) | `run_b2_frozen.py --inputs …/first5_inputs.jsonl --run-id p4_b2_devcheck_20261027 --b0-reference results/countgdpp/m4_first5_b0/predictions.jsonl` | 15/15 `replay_matches=True`. So với `b2_two_images_20261015` + `b2_remaining3_20261015`: count trùng, max \|Δbox\| = 0, max \|Δscore\| = 0, pseudo trùng. Log: `step2_b2_stdout.txt` |
| (3) CLIP (WSL `Ubuntu`, venv `cs331-p4-clip`, torch 2.9.1+cu128, transformers 4.57.1) | `p4_clip_score.py --inputs …/first5_inputs.jsonl --predictions results/countgdpp/p4_b2_devcheck_20261027/predictions.jsonl --run-id p4_clip_devcheck_20261027` | 15 query / 481 khung. Revision `3d74acf9…` khớp; sha256 `pytorch_model.bin` = `a6308213…f1576f`. Log: `step3_clip_stdout.txt` |
| (4) Freeze trên điểm mới | `p4_apply_freeze.py --scores results/countgdpp/p4_clip_devcheck_20261027 --run-id p4_freeze_e2e_devcheck_20261027 --check-audit … --reference-scores results/countgdpp/p4_clip_all15_20261020` | `CHECK audit: PASS`, `CHECK reference_scores: PASS`: max \|Δclip\| = 0, max \|Δb2\| = 0, 0 khung đổi quyết định giữ/bỏ. Log: `step4_apply_stdout.txt` |

**Kết luận:** chuỗi ảnh → B2 → CLIP → freeze chạy bằng runner mới cho kết quả **trùng tuyệt đối** với các artifact dev 15–21/10, trên cùng máy và cùng môi trường.

Hash adapter: `run_b2_frozen.py` 535b4484…, `p4_clip_score.py` c51666fa…, `p4_apply_freeze.py` cf2784bb…; checkpoint CountGD++ b89395d7… (khớp audit 14/10).

**Giới hạn:**
- Trùng tuyệt đối ở đây nghĩa là cùng GPU và cùng phiên bản thư viện. Máy khác có thể lệch nhỏ; nếu đổi máy, chạy lại bước (4) để đo.
- Bước này không nói gì về hiệu quả của phương pháp. Hiệu quả chỉ đánh giá trên tập `p4_unseen_v1` sau khi đã khóa.
