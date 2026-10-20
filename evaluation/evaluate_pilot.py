"""Đánh giá số đếm từ file đã lưu; chỉ dùng Python chuẩn, không chạy model.

Đọc hướng dẫn roadmap/PHAN_2_DANH_GIA.md trước khi chạy.
--self-test kiểm các dữ liệu giả, không ghi kết quả nghiên cứu.
"""
import argparse
import csv
import hashlib
import json
import math
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def require(condition, message):
    if not condition:
        raise ValueError(message)


def path(value):
    p = Path(value)
    return p if p.is_absolute() else ROOT / p


def read_jsonl(p):
    return [json.loads(line) for line in p.read_text(encoding="utf-8-sig").splitlines() if line.strip()]


def key(row):
    return row["image_id"], row["query_id"]


def indexed(rows, label):
    result = {}
    for row in rows:
        k = key(row)
        require(k not in result, f"{label}: ID trùng {k}")
        result[k] = row
    return result


def number(value):
    return isinstance(value, (float, int)) and not isinstance(value, bool) and math.isfinite(value)


def validate_prediction(row):
    k = key(row)
    require(row.get("schema_version") == 1, f"{k}: cần schema_version=1")
    status = row.get("execution_status")
    require(status in {"ok", "error"}, f"{k}: execution_status không hợp lệ")
    if status == "error":
        require(row.get("final_count") is None, f"{k}: error phải có final_count=null")
        return
    count = row.get("final_count")
    require(type(count) is int and count >= 0, f"{k}: count phải là số nguyên không âm")
    boxes, scores = row.get("final_boxes"), row.get("final_scores")
    require(isinstance(boxes, list) and isinstance(scores, list), f"{k}: thiếu boxes/scores")
    require(count == len(boxes) == len(scores), f"{k}: count khác số boxes/scores")
    require(row.get("box_format") == "xyxy_pixels", f"{k}: cần xyxy_pixels")
    for b in boxes:
        require(isinstance(b, list) and len(b) == 4 and all(number(v) for v in b), f"{k}: bbox không hữu hạn")
        require(b[0] < b[2] and b[1] < b[3], f"{k}: bbox có diện tích không dương")
    require(all(number(v) and 0 <= v <= 1 for v in scores), f"{k}: score không hợp lệ")


def evaluate(manifest_rows, inputs, b0_rows, b2_rows):
    """Ghép bằng (image_id, query_id), không ghép theo số thứ tự dòng."""
    gt_all = indexed(manifest_rows, "manifest")
    expected = indexed(inputs, "inputs")
    require(bool(expected), "Inputs rỗng")
    require(set(expected) <= set(gt_all), "Có input không có GT trong manifest")
    gt, uncertain = {}, []
    for k in expected:
        row = gt_all[k]
        require(row["split"] == "dev", f"{k}: runner pilot chỉ nhận split dev")
        presence = row["presence_status"]
        require(presence in {"present", "absent", "uncertain"}, f"{k}: presence không hợp lệ")
        if presence == "uncertain":
            uncertain.append(k)
            continue
        n = int(row["gt_count"])
        require((presence == "present" and n > 0) or (presence == "absent" and n == 0), f"{k}: GT/presence mâu thuẫn")
        gt[k] = (n, presence)
    pred = {}
    for name, rows in [("B0", b0_rows), ("B2", b2_rows)]:
        pred[name] = indexed(rows, name)
        require(set(pred[name]) == set(expected), f"{name}: ID thiếu/thừa: thiếu={sorted(set(expected)-set(pred[name]))}, thừa={sorted(set(pred[name])-set(expected))}")
        for row in rows:
            validate_prediction(row)
            require(row.get("variant") == name, f"{name}: variant không khớp")

    valid = {v: {k for k in gt if pred[v][k]["execution_status"] == "ok"} for v in pred}
    common = valid["B0"] & valid["B2"]

    def metrics(variant, keys):
        present = [k for k in keys if gt[k][1] == "present"]
        absent = [k for k in keys if gt[k][1] == "absent"]
        errors = [pred[variant][k]["final_count"] - gt[k][0] for k in keys]
        ep = [pred[variant][k]["final_count"] - gt[k][0] for k in present]
        return {
            "n_queries": len(keys), "n_images": len({k[0] for k in keys}),
            "MAE": sum(abs(x) for x in errors)/len(errors) if errors else None,
            "RMSE": math.sqrt(sum(x*x for x in errors)/len(errors)) if errors else None,
            "exact_count": sum(x == 0 for x in errors),
            "n_present": len(present), "n_absent": len(absent),
            "MAE_present": sum(abs(x) for x in ep)/len(ep) if ep else None,
            "RMSE_present": math.sqrt(sum(x*x for x in ep)/len(ep)) if ep else None,
            "presence_recall": sum(pred[variant][k]["final_count"] > 0 for k in present)/len(present) if present else None,
            "FPR_absent": sum(pred[variant][k]["final_count"] > 0 for k in absent)/len(absent) if absent else None,
            "MeanAbsentCount": sum(pred[variant][k]["final_count"] for k in absent)/len(absent) if absent else None,
        }

    comparisons = Counter()
    per_query = []
    for k in sorted(expected):
        item = {"image_id": k[0], "query_id": k[1], "gt_count": gt[k][0] if k in gt else None,
                "presence_status": gt_all[k]["presence_status"], "included_in_paired": k in common}
        for v in pred:
            row = pred[v][k]
            item[v+"_status"] = row["execution_status"]
            item[v+"_count"] = row["final_count"]
            item[v+"_absolute_error"] = abs(row["final_count"]-gt[k][0]) if k in valid[v] else None
        if k in common:
            d = item["B2_absolute_error"] - item["B0_absolute_error"]
            item["error_change"] = "improved" if d < 0 else "worsened" if d > 0 else "unchanged"
            comparisons[item["error_change"]] += 1
        per_query.append(item)
    summary = {
        "expected_queries": len(expected), "expected_images": len({k[0] for k in expected}),
        "uncertain_excluded": [list(k) for k in uncertain], "eligible_queries": len(gt),
        "coverage": {v: {"valid": len(valid[v]), "errors": sum(r["execution_status"] == "error" for r in pred[v].values()),
                         "eligible": len(gt)} for v in pred},
        "individual": {v: metrics(v, valid[v]) for v in pred},
        "paired": {"n_queries": len(common), "B0": metrics("B0", common), "B2": metrics("B2", common),
                   "error_change": {label: comparisons[label] for label in ["improved", "worsened", "unchanged"]}},
        "limits": ["Count metrics do not establish correct class or localization.",
                   "Absent metrics are null when no absent queries exist; never interpret null as zero error.",
                   "Errors and uncertain annotations are reported, not converted to zero counts."],
    }
    return summary, per_query


def manual_check(annotation, predictions):
    """Kiểm nhãn hậu kiểm đã có, không chạy phân loại ảnh tự động."""
    matches = [r for r in predictions if r["query_id"] == annotation["query_id"] and r["run_id"] == annotation["run"]]
    require(len(matches) == 1, "Nhãn thủ công không khớp duy nhất một prediction")
    row = matches[0]
    labels = annotation["final"]
    require(len(labels) == row["final_count"], "Thiếu/thừa nhãn bbox thủ công")
    require(sorted(x["prediction_index"] for x in labels) == list(range(row["final_count"])), "Nhãn bbox có index trùng/thiếu")
    target = []
    for label in labels:
        i = label["prediction_index"]
        require(label["overlay_number"] == i+1, "Overlay ID phải là index+1")
        require(len(label["box_xyxy"]) == 4 and all(abs(a-b) <= .001 for a,b in zip(label["box_xyxy"],row["final_boxes"][i])), "Nhãn thủ công dùng bbox khác run")
        require(type(label["is_target"]) is bool, "is_target phải là bool")
        if label["is_target"]:
            require(bool(label["visual_object_id"]), "Thiếu object ID cho khung mục tiêu")
            target.append(label)
    objects = {x["visual_object_id"] for x in target}
    return {"query_id": row["query_id"], "final_boxes": len(labels), "target_boxes": len(target),
            "distinct_target_objects": len(objects), "extra_target_boxes": len(target)-len(objects),
            "wrong_class_boxes": len(labels)-len(target),
            "note": "Recounts supplied manual labels; not model-derived labels or formal IoU precision/recall."}


def self_test():
    """Đáp án mô phỏng theo PIPELINE_PHAN_CONG; không phải model inference."""
    import copy
    truths, inputs, pred = [], [], []
    for i,(gt,n) in enumerate([(5,4),(2,2),(0,1),(3,3),(1,0),(0,0)]):
        ids = dict(image_id=f"mock{i//3+1}", query_id=f"q{i+1}")
        truths.append(dict(**ids, gt_count=str(gt), presence_status="present" if gt else "absent", split="dev"))
        inputs.append(ids)
        pred.append(dict(**ids, schema_version=1, variant="B0", execution_status="ok", final_count=n,
                         final_boxes=[[0,0,1,1] for _ in range(n)], final_scores=[.5]*n, box_format="xyxy_pixels"))
    other = [dict(r, variant="B2") for r in pred]
    result,_ = evaluate(truths,inputs,pred,other)
    m = result["paired"]["B0"]
    for field,expected in [("MAE_present",.5),("RMSE_present",math.sqrt(.5)),("presence_recall",.75),("FPR_absent",.5),("MeanAbsentCount",.5)]:
        require(math.isclose(m[field],expected), f"Fixture lệch {field}")
    def rejects(rows):
        try: evaluate(truths,inputs,rows,other)
        except ValueError: return
        raise AssertionError("Evaluator không phát hiện input hỏng")
    rejects(pred+pred[:1])
    rejects(pred[:-1])
    bad=copy.deepcopy(pred);bad[0]["final_count"]+=1;rejects(bad)
    bad=copy.deepcopy(pred);bad[0]["execution_status"]="error";rejects(bad)
    bad=copy.deepcopy(pred);bad[0].update(execution_status="error",final_count=None)
    r,_=evaluate(truths,inputs,bad,other)
    require(r["paired"]["n_queries"]==5 and r["coverage"]["B0"]["errors"]==1,"Error/null bị xử lý sai")
    print("SELF-TEST PASS: fixture, duplicate/missing IDs, count mismatch, error/null coverage")


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--self-test",action="store_true")
    parser.add_argument("--manifest",default="experiments/countgdpp/m4_inputs/manifest.csv")
    parser.add_argument("--inputs",default="experiments/countgdpp/m4_inputs/first5_inputs.jsonl")
    parser.add_argument("--b0",nargs="+",default=["results/countgdpp/m4_first5_b0/predictions.jsonl"])
    parser.add_argument("--b2",nargs="+",default=["results/countgdpp/b2_two_images_20261015/predictions.jsonl","results/countgdpp/b2_remaining3_20261015/predictions.jsonl"])
    parser.add_argument("--manual-review",default="results/countgdpp/b2_remaining3_20261015/q05_2/manual_crosscheck_20261016.json")
    parser.add_argument("--out",help="Thư mục mới tương đối CS331; không ghi đè")
    args=parser.parse_args()
    if args.self_test:
        self_test();return
    require(args.out is not None,"Cần --out cho lần đánh giá thật")
    with path(args.manifest).open(encoding="utf-8-sig",newline="") as f:
        gt=list(csv.DictReader(f))
    b0=[r for p in args.b0 for r in read_jsonl(path(p))]
    b2=[r for p in args.b2 for r in read_jsonl(path(p))]
    summary,per_query=evaluate(gt,read_jsonl(path(args.inputs)),b0,b2)
    manual=manual_check(json.loads(path(args.manual_review).read_text(encoding="utf-8-sig")),b2)
    sources=[path(args.manifest),path(args.inputs),*[path(p) for p in args.b0+args.b2],path(args.manual_review),Path(__file__)]
    config={"scope":"dev pilot; CPU evaluation of saved predictions; no model inference",
            "command":sys.argv,"sources_sha256":{str(p.relative_to(ROOT)) if p.is_relative_to(ROOT) else str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in sources}}
    dest=path(args.out)
    require(not dest.exists(),f"Output đã tồn tại: {dest}; chọn tên run mới")
    dest.mkdir(parents=True,exist_ok=False)
    for filename,data in [("metrics.json",summary),("per_query.json",per_query),("manual_check.json",manual),("run_config.json",config)]:
        (dest/filename).write_text(json.dumps(data,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    lines=["# Kết quả evaluator pilot","","Đây là số liệu được tính lại từ predictions lưu sẵn.","",
           "| Cấu hình | Số query ghép chung | MAE | RMSE | Đúng count |","|---|---:|---:|---:|---:|"]
    for v in ["B0","B2"]:
        m=summary["paired"][v]
        lines.append(f"| {v} | {m['n_queries']} | {m['MAE']} | {m['RMSE']} | {m['exact_count']} |")
    lines += ["", "Xem metrics.json để biết coverage/errors/uncertain. Không có query absent thì metric absent=null.",
              "manual_check.json chỉ tổng hợp nhãn thủ công q05_2; chưa là metric định vị tự động.",
              "Chuyển sang roadmap/PHAN_3_TONG_KET.md sau khi đối chiếu kết quả."]
    (dest/"SUMMARY.md").write_text("\n".join(lines)+"\n",encoding="utf-8")
    print(json.dumps({"paired":summary["paired"],"manual_check":manual,"output":str(dest)},ensure_ascii=False,indent=2))


if __name__ == "__main__":
    # Hiển thị tiếng Việt khi chạy từ cả Ubuntu lẫn PowerShell.
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8")
    try:
        main()
    except (ValueError,KeyError,OSError) as exc:
        raise SystemExit(f"EVALUATION STOP: {exc}")
