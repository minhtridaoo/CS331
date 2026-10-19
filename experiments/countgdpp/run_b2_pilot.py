"""B2 component comparison on pinned app: text -> automatic top-3 exemplars -> text+exemplars.
Not full paper reproduction. Original B0/final app filter is preserved.
"""
import argparse
import ast
import json
import os
import re
import sys
import time
from pathlib import Path
from PIL import Image, ImageDraw
from run_b0_batch import ROOT, REPO, SOURCE_HASH, sha, load_inputs, project_path


def select_pseudo(scores, boxes, ids, image_size, threshold=.23, maximum=3):
    import torch
    # Single positive category, no negative or visual tokens at first pass.
    dot = ids.index(1012)
    indices = [i for i in range(dot) if ids[i] not in {0,101,102,1012,1029}]
    if not indices:
        raise ValueError("Missing target tokens")
    target = scores[:, indices].max(dim=-1).values
    candidates = torch.nonzero(target > threshold, as_tuple=False).flatten()
    if not len(candidates):
        return torch.empty((0,4)), torch.empty(0), [], indices
    values, order = torch.sort(target[candidates], descending=True)
    selected = candidates[order[:maximum]]
    b = boxes[selected]
    width, height = image_size
    cx, cy, w, h = b[:,0]*width, b[:,1]*height, b[:,2]*width, b[:,3]*height
    xyxy = torch.stack(((cx-w/2).clamp(0,width),(cy-h/2).clamp(0,height),
                        (cx+w/2).clamp(0,width),(cy+h/2).clamp(0,height)),dim=1)
    if not torch.all((xyxy[:,2]>xyxy[:,0]) & (xyxy[:,3]>xyxy[:,1])):
        raise ValueError("Degenerate selected exemplar; inspect instead of silently changing policy")
    return xyxy, values[:maximum], selected.tolist(), indices


def draw_boxes(image, boxes, path, color):
    result=image.copy();draw=ImageDraw.Draw(result)
    for i,b in enumerate(boxes):
        draw.rectangle(tuple(b),outline=color,width=2)
        draw.text((b[0],max(0,b[1]-10)),str(i+1),fill=color)
    result.save(path)


def main():
    p=argparse.ArgumentParser()
    p.add_argument("--inputs",default="experiments/countgdpp/b2_two_images.jsonl")
    p.add_argument("--run-id",required=True)
    p.add_argument("--tau-sample", type=float, default=0.23)
    args=p.parse_args()
    if not re.fullmatch(r"[A-Za-z0-9_-]+",args.run_id):raise ValueError("Invalid run ID")
    inputs=project_path(args.inputs);rows=load_inputs(inputs)
    audit=json.loads((ROOT/"results/countgdpp/checkpoint_audit_2026-10-14.json").read_text())
    checkpoint=REPO/"checkpoints/countgd_plusplus.pth"
    if sha(checkpoint)!=audit["checkpoint_sha256"] or audit.get("review_decision")!="compatible_with_pinned_B0_app":raise ValueError("Checkpoint audit mismatch")
    if sha(REPO/"process_folder.py")!=SOURCE_HASH:raise ValueError("Stock source changed")
    for source,digest in audit["review_source_sha256"].items():
        if sha(REPO/source)!=digest:raise ValueError("Reviewed model code changed")
    prior_path=ROOT/"results/countgdpp/m4_first5_b0/predictions.jsonl"
    prior={(r["image_id"],r["query_id"]):r for r in map(json.loads,prior_path.read_text().splitlines())}
    # Legacy smoke output, used only for regression checks, contains no GT.
    for q in ["spoon","fork","cat"]:
        raw=json.loads((ROOT/f"results/countgdpp/smoke_{q}/results.json").read_text())["utensils.jpg"]
        prior[("utensils","smoke_"+q)]={"final_count":raw["count"],"final_boxes":raw["boxes"],"final_scores":raw["scores"]}
    if any((r["image_id"],r["query_id"]) not in prior for r in rows):raise ValueError("Missing B0 reference")
    out=ROOT/"results/countgdpp"/args.run_id;out.mkdir(exist_ok=False)
    config=dict(status="running",variant="B2",scope="App-based two-pass component comparison; not full paper",inputs=rows,
        checkpoint_sha256=audit["checkpoint_sha256"],source_sha256=SOURCE_HASH,adapter_sha256=sha(Path(__file__)),input_sha256=sha(inputs),
        model_commit="8489f836d75eb407ae778c56cff1f72cc6f8baae",selection_reference="test_shanghai_tech.py:get_pseudo_exemplars",
        selection_reference_sha256=sha(REPO/"test_shanghai_tech.py"),tau_sample=args.tau_sample,tau_final=.23,max_pseudo=3,
        selection="Max target-word token score on all first-pass proposals, strict > threshold, descending torch.sort CPU, top 3, clamp xyxy",
        nms=False,no_pseudo_policy="return B0 without second forward (adapter convention, unlike upstream unconditional second pass)",
        final_filter="Unchanged app positive-vs-remaining filter, includes inserted exemplar tokens before period in stage 2",
        negative_prompts=False,synthetic=False,crop=False,seed=42,resize=dict(short_side=800,max_size=1333),
        timing="elapsed_ms = both predict calls including preprocess/capture and selection; excludes model load, replay check, disk/overlay; no warmup",
        memory="peak_vram_mib = peak torch CUDA allocated including resident model, not total device memory",
        raw_arrays="All 900 proposals: normalized cxcywh, sigmoid token scores and input_ids for each executed pass")
    def save(): (out/"run_config.json").write_text(json.dumps(config,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    save()
    import torch
    import numpy as np
    if not torch.cuda.is_available():raise RuntimeError("CUDA required")
    sys.path.insert(0,str(REPO));os.chdir(REPO)
    source=REPO/"process_folder.py";tree=ast.parse(source.read_text())
    tree.body=[n for n in tree.body if isinstance(n,(ast.Import,ast.ImportFrom,ast.FunctionDef))]
    ns={"__name__":"pinned_stock_definitions"};exec(compile(tree,str(source),"exec"),ns)
    model,transform=ns["build_model_and_transforms"](ns["build_arg_parser"]().parse_args([]))
    device=torch.device("cuda");model=model.to(device)
    config.update(device=torch.cuda.get_device_name(),torch_version=torch.__version__,python=sys.version)
    save()
    original=ns["get_boxes_from_prediction"];capture={}
    def observe(output,text,keywords="",conf_thresh=.23):
        returned=original(output,text,keywords,conf_thresh)
        capture.update(scores=output["pred_logits"][0].sigmoid().detach().cpu(),boxes=output["pred_boxes"][0].detach().cpu(),ids=output["input_ids"][0].detach().cpu().tolist())
        return returned
    ns["get_boxes_from_prediction"]=observe
    def predict(image,prompt,exemplars):
        prompts={"image":image,"points":[[b[0],b[1],2.0,b[2],b[3],3.0] for b in exemplars]}
        b,s=ns["predict"](model,transform,image,prompt,prompts,[],[],device,.23)
        x,y,w,h=ns["get_box_coords_from_boxes"](image,b)
        return np.stack((x,y,x+w,y+h),axis=1),s,dict(capture)
    def save_raw(job,label,cap):
        np.savez_compressed(job/(label+"_raw.npz"),scores=cap["scores"].numpy(),normalized_cxcywh=cap["boxes"].numpy(),input_ids=np.array(cap["ids"]))
    failed=False
    with (out/"predictions.jsonl").open("w",encoding="utf-8") as f:
        for i,row in enumerate(rows):
            job=out/row["query_id"];job.mkdir()
            rec=dict(schema_version=1,run_id=args.run_id,variant="B2",image_id=row["image_id"],query_id=row["query_id"],
                execution_status="error",final_count=None,final_boxes=[],final_scores=[],error_message=None,box_format="xyxy_pixels",
                image_width=None,image_height=None,overlay_path=None,elapsed_ms=None,peak_vram_mib=None,
                stage1_count=None,stage1_boxes=[],stage1_scores=[],pseudo_boxes=[],pseudo_scores=[],no_pseudo=None,
                stage2_count=None,stage2_boxes=None,stage2_scores=None,stage2_executed=False)
            try:
                image=Image.open(project_path(row["image_path"])).convert("RGB")
                rec.update(image_width=image.width,image_height=image.height)
                torch.manual_seed(42);np.random.seed(42);ns["random"].seed(42)
                torch.cuda.synchronize();torch.cuda.reset_peak_memory_stats();start=time.perf_counter()
                b0,s0,cap0=predict(image,row["prompt"],[])
                torch.cuda.synchronize();stage1_ms=(time.perf_counter()-start)*1000
                rec.update(stage1_count=len(b0),stage1_boxes=b0.tolist(),stage1_scores=s0.tolist())
                ref=prior[(row["image_id"],row["query_id"])]
                matches=len(b0)==ref["final_count"] and np.allclose(b0,np.asarray(ref["final_boxes"]).reshape(-1,4),atol=.001,rtol=0) and np.allclose(s0,ref["final_scores"],atol=1e-5,rtol=0)
                rec["stage1_matches_B0"]=bool(matches)
                save_raw(job,"stage1",cap0)
                if not matches:raise ValueError("Stage 1 differs from B0; stop before interpreting B2")
                start=time.perf_counter()
                pb,ps,pids,tindices=select_pseudo(cap0["scores"],cap0["boxes"],cap0["ids"],image.size,threshold=args.tau_sample,)
                rec.update(pseudo_boxes=pb.tolist(),pseudo_scores=ps.tolist(),pseudo_proposal_ids=pids,no_pseudo=len(pb)==0,target_token_indices=tindices)
                if len(pb):
                    final,sfinal,cap2=predict(image,row["prompt"],pb.tolist())
                    rec.update(stage2_executed=True,stage2_count=len(final),stage2_boxes=final.tolist(),stage2_scores=sfinal.tolist())
                else:
                    final,sfinal=b0,s0;cap2=None
                torch.cuda.synchronize();rec["elapsed_ms"]=round(stage1_ms+(time.perf_counter()-start)*1000,2)
                rec["peak_vram_mib"]=round(torch.cuda.max_memory_allocated()/1024**2,2)
                if cap2 is not None:save_raw(job,"stage2",cap2)
                draw_boxes(image,b0.tolist(),job/"stage1.jpg","red")
                draw_boxes(image,pb.tolist(),job/"pseudo.jpg","lime")
                draw_boxes(image,final.tolist(),job/"final.jpg","red")
                rec.update(execution_status="ok",final_count=len(final),final_boxes=final.tolist(),final_scores=sfinal.tolist(),overlay_path=(job/"final.jpg").relative_to(ROOT).as_posix(),pseudo_overlay_path=(job/"pseudo.jpg").relative_to(ROOT).as_posix())
                assert len(final)==len(sfinal)
                print(f"{i+1}/{len(rows)} {row['query_id']} {row['prompt']}: B0={len(b0)}, pseudo={len(pb)}, B2={len(final)}, replay_matches={matches}, no_pseudo={len(pb)==0}",flush=True)
            except Exception as exc:
                rec["error_message"]=f"{type(exc).__name__}: {exc}";failed=True
                print(rec["error_message"],flush=True)
            f.write(json.dumps(rec,ensure_ascii=False,allow_nan=False)+"\n");f.flush()
            if failed:break
    config.update(status="failed" if failed else "complete",completed_queries=i+1);save()
    if failed:raise SystemExit(1)

if __name__=="__main__":main()
