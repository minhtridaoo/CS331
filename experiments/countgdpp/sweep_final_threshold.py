"""M6/E1: offline final-threshold sweep, fixed B2 pseudo exemplars; never retrains/reruns forward."""
import argparse
import csv
import hashlib
import json
import math
import re
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageOps

ROOT=Path(__file__).resolve().parents[2]
GRID=[0.10,0.23,0.35,0.50]  # Existing protocol grid, fixed before inspecting this run.

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def filter_raw(raw, threshold, width, height):
    scores=raw["scores"];boxes=raw["normalized_cxcywh"];ids=raw["input_ids"].tolist()
    if scores.ndim!=2 or boxes.shape!=(scores.shape[0],4) or len(ids)>scores.shape[1]:raise ValueError("Bad raw shape")
    if not np.isfinite(scores).all() or not np.isfinite(boxes).all():raise ValueError("Nonfinite raw output")
    if np.any(scores<0) or np.any(scores>1):raise ValueError("Expected sigmoid scores")
    dot=ids.index(1012)
    pos=scores[:,:dot+1].max(axis=1);neg=scores[:,dot+1:].max(axis=1)
    kept=np.flatnonzero((pos>threshold)&(pos>neg))
    b=boxes[kept];cx=b[:,0]*width;cy=b[:,1]*height;w=b[:,2]*width;h=b[:,3]*height
    xyxy=np.stack((cx-w/2,cy-h/2,cx+w/2,cy+h/2),axis=1)
    return kept,xyxy,scores[kept].max(axis=1)

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--source-run",default="b2_two_images_20261015")
    p.add_argument("--run-id",required=True)
    a=p.parse_args()
    for value in [a.run_id,a.source_run]:
        if not re.fullmatch(r"[A-Za-z0-9_-]+",value):raise ValueError("Invalid run name")
    source=ROOT/"results/countgdpp"/a.source_run
    cfg=json.loads((source/"run_config.json").read_text(encoding="utf-8"))
    if cfg["status"]!="complete" or cfg["tau_sample"]!=.23 or cfg["tau_final"]!=.23:raise ValueError("Expected complete source run at 0.23/0.23")
    records=[json.loads(s) for s in (source/"predictions.jsonl").read_text(encoding="utf-8").splitlines() if s.strip()]
    keys=[(r["image_id"],r["query_id"]) for r in records]
    if len(set(keys))!=len(keys) or set(keys)!={(r["image_id"],r["query_id"]) for r in cfg["inputs"]}:raise ValueError("Missing/duplicate source IDs")
    manifest=ROOT/"experiments/countgdpp/m4_inputs/manifest.csv"
    gt={}
    for r in csv.DictReader(manifest.open(encoding="utf-8")):
        key=(r["image_id"],r["query_id"])
        if key in gt:raise ValueError("Duplicate manifest ID")
        gt[key]=r
    inputs={r["query_id"]:r for r in cfg["inputs"]}
    # Validate references at 0.23 before producing any new experiment output.
    cache={};raw_hashes={}
    for r in records:
        if r["execution_status"]!="ok":raise ValueError("Source error must not become count zero")
        g=gt[(r["image_id"],r["query_id"])]
        if g["presence_status"]!="present" or int(g["gt_count"])<=0:raise ValueError("This review expects verified present queries only")
        for variant in ["B0","B2"]:
            stage="stage1" if variant=="B0" or r["no_pseudo"] else "stage2"
            path=source/r["query_id"]/(stage+"_raw.npz")
            with np.load(path,allow_pickle=False) as raw: data={k:raw[k].copy() for k in raw.files}
            cache[(r["query_id"],variant)]=data;raw_hashes[str(path.relative_to(ROOT))]=sha(path)
            kept,boxes,scores=filter_raw(data,.23,r["image_width"],r["image_height"])
            prefix="stage1" if variant=="B0" else "final"
            if len(kept)!=r[prefix+"_count"]:raise ValueError("Replay count mismatch")
            np.testing.assert_allclose(boxes,np.array(r[prefix+"_boxes"]).reshape(-1,4),atol=.001,rtol=0)
            np.testing.assert_allclose(scores,r[prefix+"_scores"],atol=1e-5,rtol=0)
    out=ROOT/"results/countgdpp"/a.run_id;out.mkdir(exist_ok=False)
    config=dict(status="running",experiment="M6 E1 fixed-pseudo final threshold sweep",grid=GRID,
        tau_sample_fixed=.23,max_pseudo=cfg["max_pseudo"],source_run=a.source_run,
        source_config_sha256=sha(source/"run_config.json"),source_predictions_sha256=sha(source/"predictions.jsonl"),
        manifest_sha256=sha(manifest),adapter_sha256=sha(Path(__file__)),raw_sha256=raw_hashes,
        no_pseudo="No second pass. Refilter stage1 at each tau_final; pseudo selection remains fixed at tau_sample 0.23.",
        filter="Original app strict positive max > tau_final and positive max > remaining max; inserted exemplar tokens retained",
        scope="Same 2-image/6-query exploratory dev subset; no per-query tuned thresholds, no holdout selection, no inference timing",replay_023_verified=True)
    def save(): (out/"run_config.json").write_text(json.dumps(config,indent=2)+"\n")
    save();table=[];allpred=[];summaries=[]
    for r in records:
        g=gt[(r["image_id"],r["query_id"])];n=int(g["gt_count"])
        original=Image.open(ROOT/inputs[r["query_id"]]["image_path"]).convert("RGB")
        sheet=Image.new("RGB",(1440,820),"white");sheet_draw=ImageDraw.Draw(sheet)
        for vi,variant in enumerate(["B0","B2"]):
            previous=None
            for ti,tau in enumerate(GRID):
                ids,boxes,scores=filter_raw(cache[(r["query_id"],variant)],tau,r["image_width"],r["image_height"])
                if previous is not None and not set(ids).issubset(previous):raise ValueError("Nonmonotonic fixed-output filtering")
                previous=set(ids)
                table.append(dict(image_id=r["image_id"],query_id=r["query_id"],prompt=g["prompt"],variant=variant,tau_final=tau,tau_sample=.23 if variant=="B2" else None,gt_count=n,predicted_count=len(ids),absolute_error=abs(len(ids)-n),source_no_pseudo=r["no_pseudo"],second_pass_used=variant=="B2" and r["stage2_executed"]))
                allpred.append(dict(schema_version=1,run_id=a.run_id,variant=variant,tau_final=tau,image_id=r["image_id"],query_id=r["query_id"],execution_status="ok",final_count=len(ids),final_boxes=boxes.tolist(),final_scores=scores.tolist(),proposal_ids=ids.tolist(),box_format="xyxy_pixels",image_width=r["image_width"],image_height=r["image_height"],source_stage="stage1" if variant=="B0" or r["no_pseudo"] else "stage2"))
                overlay=original.copy();d=ImageDraw.Draw(overlay)
                for b in boxes:d.rectangle(tuple(map(float,b)),outline="red",width=2)
                tile=ImageOps.contain(overlay,(355,375));sheet.paste(tile,(ti*360,vi*410+30))
                sheet_draw.text((ti*360+5,vi*410+5),f"{variant} tau={tau} count={len(ids)} GT={n}",fill="black")
        sheet.save(out/(r["query_id"]+"_sweep.jpg"))
    for variant in ["B0","B2"]:
        for tau in GRID:
            batch=[r for r in table if r["variant"]==variant and r["tau_final"]==tau]
            err=[r["absolute_error"] for r in batch]
            summaries.append(dict(variant=variant,tau_final=tau,images=len({r['image_id'] for r in batch}),queries=len(batch),coverage=1.0,MAE_present=sum(err)/len(err),RMSE_present=math.sqrt(sum(e*e for e in err)/len(err)),exact_count=sum(e==0 for e in err),presence_recall=sum(r['predicted_count']>0 for r in batch)/len(batch),zero_predictions=sum(r['predicted_count']==0 for r in batch),FPR_absent=None))
    for name,data in [("per_query.csv",table),("summary.csv",summaries)]:
        with (out/name).open("w",encoding="utf-8",newline="") as f:
            w=csv.DictWriter(f,fieldnames=list(data[0]));w.writeheader();w.writerows(data)
    (out/"predictions.jsonl").write_text(''.join(json.dumps(r,allow_nan=False)+"\n" for r in allpred))
    (out/"summary.json").write_text(json.dumps(summaries,indent=2)+"\n")
    config.update(status="complete",query_configurations=len(table));save()
    print("Original 0.23 boxes/scores/count replay verified for both variants; 48 query/configurations completed on CPU.")
    for r in summaries: print(f"{r['variant']} tau={r['tau_final']}: MAE={r['MAE_present']:.3f}, exact={r['exact_count']}/{r['queries']}, zero={r['zero_predictions']}")

if __name__=="__main__":main()
