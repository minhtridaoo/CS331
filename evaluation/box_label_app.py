"""Mini app gán nhãn từng khung: xem crop + ảnh toàn cảnh, điền nhãn, "Lưu & tiếp" ghi thẳng vào CSV.
Hai gói: q05 (V3, q05_3) và n4b (V6, N4 tầng B: u06_2, u07_2 — khung chính, mẫu pseudo, ứng viên E3).
Chỉ đọc ảnh/CSV đã có, không chạy model, không đọc `_KEY_mo_sau_khi_review/`. Chỉ ghi các cột nhãn (label_type,
actual_class, object_id, uncertain, note, reviewer, date) của đúng dòng đang sửa; giữ nguyên thứ tự cột, BOM và kiểu xuống dòng.

Example (from CS331 root): python evaluation/box_label_app.py --set n4b  rồi mở http://127.0.0.1:8790
"""
import argparse
import csv
import datetime
import io
import json
import sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
Q05 = ROOT / "results/countgdpp/q05_error_analysis_package_20261027"
N4 = ROOT / "results/countgdpp/p4_n4_review_package_20261027"
MUCCA = ROOT / "data_external/mucca_zenodo_19231375/MUCCA_1.0/images"
N4_LABELS = ["target", "duplicate", "part", "multi_object", "wrong_class", "background", "uncertain"]


def n4b_sheets(qid, stem):
    return {f"{qid}_main": {"query": qid, "file": N4 / f"B_{qid}_{stem}_labels_BLANK.csv", "label": f"{qid} · khung chính",
                            "desc": "khung được ít nhất một bộ lọc giữ (review mù: số là rank của B2, không biết bộ lọc nào giữ)"},
            f"{qid}_pseudo": {"query": qid, "file": N4 / f"bo_sung_F0/B_{qid}_{stem}_pseudo_labels_BLANK.csv", "label": f"{qid} · mẫu pseudo",
                              "desc": "3 mẫu tự chọn P1–P3 mà B2 đưa vào lượt 2: đúng loại không, có đúng một vật không?"},
            f"{qid}_e3": {"query": qid, "file": N4 / f"bo_sung_F0/B_{qid}_{stem}_e3_labels_BLANK.csv", "label": f"{qid} · ứng viên E3",
                          "desc": "khung B2 bị cả hai bộ lọc loại nhưng có điểm GT bên trong: vật đúng bị xóa nhầm (E3), hay trùng / nhiều vật / một phần?"}}


# Ảnh nền: ảnh gốc nếu có, không thì *_overview.jpg của gói (cùng kích thước gốc, đã vẽ sẵn khung vàng).
SETS = {
    "q05": {"title": "Gán nhãn khung q05_3", "start": "B0",
            "labels": ["target", "duplicate", "part", "wrong_class", "background"], "uncertain_col": True,
            "classes": ["blackberries", "raspberries", "blueberries", "strawberries", "cherries"],
            "object_ids": ["b1", "b2", "b3"], "id_hint": "b1 trên phải có cuống · b2 trên giữa · b3 dưới phải sau dâu/cherry",
            "queries": {"q05_3": {"image_id": "mcac_27", "prompt": "blackberries", "gt": 3,
                                  "images": [ROOT / "results/countgdpp/m4_first5_b0/jobs/015_q05_3/input/mcac_27.jpg"]}},
            "sheets": {"pseudo": {"query": "q05_3", "file": Q05 / "q05_3_B2_pseudo_labels_BLANK.csv", "label": "pseudo",
                                  "desc": "3 mẫu tự chọn sau lượt 1 (B2 dùng làm exemplar cho lượt 2)"},
                       "B0": {"query": "q05_3", "file": Q05 / "q05_3_B0_stage1_labels_BLANK.csv", "label": "B0",
                              "desc": "khung đếm của B0: một lượt, ảnh + text"},
                       "B2": {"query": "q05_3", "file": Q05 / "q05_3_B2_final_labels_BLANK.csv", "label": "B2 final",
                              "desc": "khung đếm cuối của B2: lượt 2 dùng 3 mẫu tự chọn"}}},
    "n4b": {"title": "Gán nhãn N4 tầng B", "start": "u06_2_main",
            "labels": N4_LABELS, "uncertain_col": False,
            "classes": ["beach umbrellas", "chairs", "people", "cars", "trucks", "buses", "motorcycles", "bicycles"],
            "object_ids": [], "id_hint": "cùng một vật thì cùng id (ví dụ u1, u2 hoặc c1, c2), dùng chung cho cả 3 sheet của query; khung trùng ghi duplicate",
            "queries": {"u06_2": {"image_id": "mcac_61", "prompt": "beach umbrellas", "gt": 30,
                                  "images": [MUCCA / "mcac_61.jpg", N4 / "B_u06_2_beach_umbrellas_overview.jpg"]},
                        "u07_2": {"image_id": "mcac_88", "prompt": "cars", "gt": 22,
                                  "images": [MUCCA / "mcac_88.jpg", N4 / "B_u07_2_cars_overview.jpg"]}},
            "sheets": {**n4b_sheets("u06_2", "beach_umbrellas"), **n4b_sheets("u07_2", "cars")}},
}
EDITABLE = ["label_type", "actual_class", "object_id", "uncertain", "note", "reviewer"]


def read_sheet(path):
    raw = path.read_bytes()
    rows = list(csv.reader(raw.decode("utf-8-sig").splitlines()))
    meta = {"bom": raw.startswith(b"\xef\xbb\xbf"), "eol": "\r\n" if b"\r\n" in raw else "\n"}
    key = "rank" if "rank" in rows[0] else "tag"  # gói N4 bổ sung đánh số bằng tag (P1, #4)
    out = [dict(zip(rows[0], r)) for r in rows[1:] if r]
    for r in out:
        r["_id"] = r[key]
    return rows[0], out, meta


def write_sheet(path, header, rows, meta):
    buf = io.StringIO()
    w = csv.writer(buf, lineterminator=meta["eol"])
    w.writerow(header)
    w.writerows([r.get(k, "") for k in header] for r in rows)
    text = buf.getvalue()
    bom = meta["bom"] or not text.isascii()  # có dấu tiếng Việt thì thêm BOM để Excel đọc đúng
    tmp = path.with_suffix(".tmp")
    tmp.write_bytes((chr(0xFEFF) if bom else "").encode("utf-8") + text.encode("utf-8"))
    tmp.replace(path)


def box(r):
    return [float(r[k]) for k in ("x1", "y1", "x2", "y2")]


def iou(a, b):
    ix, iy = max(0, min(a[2], b[2]) - max(a[0], b[0])), max(0, min(a[3], b[3]) - max(a[1], b[1]))
    inter = ix * iy
    union = (a[2] - a[0]) * (a[3] - a[1]) + (b[2] - b[0]) * (b[3] - b[1]) - inter
    return inter / union if union > 0 else 0.0


class App:
    def __init__(self, cfg):
        self.cfg, self.sheets, self.imgs, self.src = cfg, cfg["sheets"], {}, {}
        for qid, q in cfg["queries"].items():
            src = next((p for p in q["images"] if p.exists()), None)
            if src is None:
                raise SystemExit(f"Không thấy ảnh cho {qid}: {[str(p) for p in q['images']]}")
            self.imgs[qid], self.src[qid] = Image.open(src).convert("RGB"), src

    def load(self, name):
        return read_sheet(self.sheets[name]["file"])

    def config_json(self):
        c = self.cfg
        return {"title": c["title"], "start": c["start"], "labels": c["labels"], "uncertain_col": c["uncertain_col"],
                "classes": c["classes"], "id_hint": c["id_hint"],
                "sheets": [{"name": n, "label": s["label"], "n": len(self.load(n)[1])} for n, s in self.sheets.items()]}

    def sheet_json(self, name):
        qid = self.sheets[name]["query"]
        _, rows, _ = self.load(name)
        others = {n: self.load(n)[1] for n, s in self.sheets.items() if n != name and s["query"] == qid}
        ids = set(self.cfg["object_ids"]) | {o["object_id"] for rs in [rows, *others.values()] for o in rs if o.get("object_id")}
        out = []
        for r in rows:
            b = box(r)
            overlaps = sorted(([round(iou(b, box(o)), 2), o["_id"], o.get("label_type", ""), o.get("object_id", "")]
                               for o in rows if o is not r and iou(b, box(o)) >= 0.3), reverse=True)
            cross = sorted(([round(iou(b, box(o)), 2), f"{self.sheets[n]['label']} {o['_id']}", o.get("label_type", ""), o.get("object_id", "")]
                            for n, rs in others.items() for o in rs if iou(b, box(o)) >= 0.3), reverse=True)
            out.append({**r, "w": round(b[2] - b[0]), "h": round(b[3] - b[1]), "overlaps": overlaps, "cross": cross})
        img = self.imgs[qid]
        fallback = " · ảnh nền là overview của gói (khung vàng vẽ sẵn)" if "overview" in self.src[qid].name else ""
        return {"name": name, "file": str(self.sheets[name]["file"]), "image": f"{img.width}x{img.height}{fallback}",
                "query": {"query_id": qid, **{k: v for k, v in self.cfg["queries"][qid].items() if k != "images"}},
                "desc": self.sheets[name]["desc"], "ids": sorted(ids), "rows": out}

    def render(self, name, rid, kind, others):
        _, rows, _ = self.load(name)
        img = self.imgs[self.sheets[name]["query"]]
        cur = next(r for r in rows if r["_id"] == rid)
        b = box(cur)
        if kind == "overview":
            im = img.copy()
            d = ImageDraw.Draw(im)
            if others:
                for o in rows:
                    if o is not cur:
                        d.rectangle(box(o), outline=(255, 220, 0), width=2)
            d.rectangle(b, outline=(255, 0, 0), width=max(4, img.width // 375))
            im.thumbnail((900, 900))
        else:
            w, h = b[2] - b[0], b[3] - b[1]
            pad = max(max(w, h) * 0.35, (320 - max(w, h)) / 2)  # khung nhỏ (từng hạt) vẫn thấy cả vật xung quanh
            c = (max(0, b[0] - pad), max(0, b[1] - pad), min(img.width, b[2] + pad), min(img.height, b[3] + pad))
            im = img.crop(c)
            s = 560 / max(im.width, im.height)
            im = im.resize((round(im.width * s), round(im.height * s)))
            d = ImageDraw.Draw(im)
            shift = lambda q: [(q[0] - c[0]) * s, (q[1] - c[1]) * s, (q[2] - c[0]) * s, (q[3] - c[1]) * s]
            if others:
                for o in rows:
                    if o is not cur and iou(box(o), list(c)) > 0:
                        ob = shift(box(o))
                        d.rectangle(ob, outline=(255, 220, 0), width=1)
                        d.text((ob[0] + 2, ob[1] + 1), o["_id"], fill=(255, 220, 0))
            d.rectangle(shift(b), outline=(255, 0, 0), width=3)
        buf = io.BytesIO()
        im.save(buf, "JPEG", quality=90)
        return buf.getvalue()

    def save(self, name, rid, fields):
        header, rows, meta = self.load(name)
        r = next(r for r in rows if r["_id"] == rid)
        for k in EDITABLE:
            if k in header and k in fields:
                r[k] = str(fields[k]).strip()
        r["date"] = datetime.date.today().isoformat()
        write_sheet(self.sheets[name]["file"], header, rows, meta)


PAGE = r"""<!doctype html><html lang="vi"><head><meta charset="utf-8"><title>Gán nhãn khung</title>
<style>
body{font-family:system-ui,Segoe UI,sans-serif;margin:0;background:#f4f4f5;color:#18181b}
header{display:flex;gap:12px;align-items:center;padding:8px 14px;background:#fff;border-bottom:1px solid #ddd;flex-wrap:wrap}
main{display:grid;grid-template-columns:minmax(0,580px) minmax(0,1fr);gap:14px;padding:14px}
@media (max-width:900px){main{grid-template-columns:minmax(0,1fr)}}
td{word-break:break-all}
.card{background:#fff;border:1px solid #ddd;border-radius:8px;padding:10px}
img{max-width:100%;display:block}
#chips{display:flex;flex-wrap:wrap;gap:3px;padding:6px 14px;background:#fff;border-bottom:1px solid #ddd}
.chip{font-size:12px;padding:2px 6px;border-radius:4px;background:#e4e4e7;cursor:pointer}
.chip.done{background:#bbf7d0}.chip.unc{background:#fde68a}.chip.cur{outline:2px solid #ef4444}
table{border-collapse:collapse;font-size:14px}td{padding:2px 8px 2px 0;vertical-align:top}
label{display:block;margin-top:8px;font-weight:600;font-size:14px}
select,input[type=text],textarea{width:100%;font-size:15px;padding:5px;box-sizing:border-box}
#sheet{width:auto}
textarea{height:70px}
.btns{display:flex;gap:8px;margin-top:12px}button{font-size:15px;padding:7px 14px;cursor:pointer}
#next{background:#2563eb;color:#fff;border:0;border-radius:6px}
#msg{margin-top:8px;font-size:14px}.warn{color:#b45309}.ok{color:#15803d}
.hint{font-size:12px;color:#71717a}
#banner{padding:10px 14px;background:#eff6ff;border-bottom:1px solid #bfdbfe;font-size:15px;line-height:1.5}
#banner .p{font-size:20px;font-weight:700;color:#1d4ed8}
</style></head><body>
<header><b id="apptitle"></b>
<select id="sheet"></select>
<span id="prog"></span><label style="margin:0;font-weight:400"><input type="checkbox" id="others"> hiện các khung khác</label>
<span class="hint" id="keys"></span></header>
<div id="banner"></div>
<div id="chips"></div>
<main>
<div class="card"><div id="title" style="font-weight:700;margin-bottom:6px"></div><img id="crop"><div class="hint">Đỏ = khung đang xét (đã nới rộng để thấy xung quanh, tối thiểu 320 px ảnh gốc)</div></div>
<div>
<div class="card"><img id="ov" style="max-height:330px"></div>
<div class="card" style="margin-top:10px"><table id="info"></table></div>
<div class="card" style="margin-top:10px">
<label>label_type</label><select id="label_type"></select>
<label>actual_class</label><input type="text" id="actual_class" list="cls"><datalist id="cls"></datalist>
<label>object_id <span class="hint" id="idhint"></span></label><input type="text" id="object_id" list="ids"><datalist id="ids"></datalist>
<label id="uncwrap"><input type="checkbox" id="uncertain"> uncertain (phân vân)</label>
<label>note</label><textarea id="note"></textarea>
<label>reviewer</label><input type="text" id="reviewer">
<div class="btns"><button id="prev">← Trước</button><button id="savebtn">Lưu</button><button id="next">Lưu &amp; tiếp →</button></div>
<div id="msg"></div></div></div></main>
<script>
let C=null,data=null,i=0;const $=id=>document.getElementById(id);const opt=v=>`<option>${v}</option>`;
async function init(){C=await (await fetch('/api/config')).json();document.title=C.title;$('apptitle').textContent=C.title;
$('sheet').innerHTML=C.sheets.map(s=>`<option value="${s.name}">${s.label} (${s.n})</option>`).join('');
$('label_type').innerHTML='<option></option>'+C.labels.map(opt).join('');$('cls').innerHTML=C.classes.map(opt).join('');
$('idhint').textContent=C.id_hint;$('uncwrap').style.display=C.uncertain_col?'':'none';
$('keys').innerHTML='Phím tắt (ngoài ô chữ): '+C.labels.map((l,j)=>`${j+1} ${l}`).join(' · ')+' · ←/→ chuyển khung · Ctrl+Enter lưu &amp; tiếp';
$('sheet').value=C.start;load(C.start)}
async function load(name,keep){data=await (await fetch('/api/sheet?name='+encodeURIComponent(name))).json();if(!keep){i=data.rows.findIndex(r=>!r.label_type);if(i<0)i=0}show()}
function show(){const r=data.rows[i],o=$('others').checked?1:0,q=`name=${data.name}&id=${encodeURIComponent(r._id)}&others=${o}`;
$('crop').src='/img/crop?'+q;$('ov').src='/img/overview?'+q;
$('title').textContent=`${data.name} · ${r._id}  (${i+1}/${data.rows.length})`;
const fmt=xs=>xs.length?xs.map(x=>`${x[1]} (IoU ${x[0]})${x[2]?' = '+x[2]+(x[3]?' '+x[3]:''):''}`).join('<br>'):'không có',ov=fmt(r.overlaps);
const Q=data.query;$('banner').innerHTML=`Prompt: <span class="p">"${Q.prompt}"</span> · query <b>${Q.query_id}</b> · ảnh <b>${Q.image_id}</b> · GT <b>${Q.gt}</b><br>
Đang xem: <b>${data.name}</b>, ${data.desc}. Câu hỏi cho mỗi khung: khung đỏ có ôm đúng <b>một "${Q.prompt}" trọn vẹn</b> không? Nếu không thì nó là gì?`;
$('info').innerHTML=`<tr><td>File</td><td>${data.file}</td></tr><tr><td>Ảnh</td><td>${Q.image_id} (${data.image}) · ${Q.query_id} "${Q.prompt}" · GT ${Q.gt}</td></tr>
<tr><td>Tọa độ</td><td>x1 ${r.x1}, y1 ${r.y1}, x2 ${r.x2}, y2 ${r.y2}</td></tr><tr><td>Kích thước</td><td>${r.w} × ${r.h} px${r.area_px?' · area '+r.area_px:''}${r.score?' · score '+r.score:''}</td></tr>
<tr><td>Chồng lên (IoU≥0.3)</td><td>${ov}</td></tr><tr><td>Chồng lên ở sheet khác (cùng query)</td><td>${fmt(r.cross)}</td></tr>`;
$('ids').innerHTML=data.ids.map(opt).join('');
for(const k of ['label_type','actual_class','object_id','note'])$(k).value=r[k]||'';
$('uncertain').checked=(r.uncertain||'')!=='';$('reviewer').value=r.reviewer||'Trieu';$('msg').textContent='';
const done=data.rows.filter(x=>x.label_type).length;$('prog').textContent=`đã điền ${done}/${data.rows.length}`;
$('chips').innerHTML=data.rows.map((x,j)=>`<span class="chip ${x.label_type?'done':''} ${x.uncertain||x.label_type==='uncertain'?'unc':''} ${j===i?'cur':''}" data-j="${j}" title="${x.label_type} ${x.object_id||x.actual_class||''}">${x._id}</span>`).join('');
document.querySelectorAll('.chip').forEach(c=>c.onclick=()=>{i=+c.dataset.j;show()})}
function warn(f){const t=f.label_type,p=data.query.prompt;if(!t)return 'Chưa chọn label_type.';
if(['target','duplicate','part'].includes(t)&&!f.object_id)return t+' cần object_id.';
if(['wrong_class','multi_object'].includes(t)&&!f.actual_class)return t+' cần actual_class (vật thật trong khung).';
if(['target','duplicate','part'].includes(t)&&f.actual_class&&f.actual_class!==p)return t+` nhưng actual_class không phải ${p}?`;return ''}
async function save(go){const r=data.rows[i],f={label_type:$('label_type').value,actual_class:$('actual_class').value,object_id:$('object_id').value,
uncertain:$('uncertain').checked?'yes':'',note:$('note').value,reviewer:$('reviewer').value};
if(['target','duplicate','part'].includes(f.label_type)&&!f.actual_class)f.actual_class=data.query.prompt;
const w=warn(f);if(w&&!confirm(w+'\nVẫn lưu?'))return;
const res=await fetch('/api/save',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({name:data.name,id:r._id,fields:f})});
if(!res.ok){$('msg').innerHTML=`<span class="warn">Lỗi lưu: ${await res.text()}</span>`;return}
const keep=i;await load(data.name,true);i=go&&keep<data.rows.length-1?keep+1:keep;show();$('msg').innerHTML=`<span class="ok">Đã lưu ${r._id}.</span>`}
$('next').onclick=()=>save(true);$('savebtn').onclick=()=>save(false);$('prev').onclick=()=>{if(i>0){i--;show()}};
$('sheet').onchange=e=>load(e.target.value);$('others').onchange=show;
document.addEventListener('keydown',e=>{if(e.ctrlKey&&e.key==='Enter'){save(true);return}
if(['INPUT','TEXTAREA','SELECT'].includes(document.activeElement.tagName))return;
const l=C.labels[+e.key-1];if(l)$('label_type').value=l;if(e.key==='ArrowRight'&&i<data.rows.length-1){i++;show()}if(e.key==='ArrowLeft'&&i>0){i--;show()}});
init();
</script></body></html>"""


def handler(app):
    class H(BaseHTTPRequestHandler):
        def send(self, code, body, ctype):
            try:
                self.send_response(code)
                self.send_header("Content-Type", ctype)
                self.send_header("Cache-Control", "no-store")
                self.end_headers()
                self.wfile.write(body)
            except (ConnectionAbortedError, ConnectionResetError, BrokenPipeError):
                pass  # trình duyệt bỏ ảnh cũ khi chuyển khung nhanh; không ảnh hưởng dữ liệu

        def do_GET(self):
            u = urlparse(self.path)
            q = {k: v[0] for k, v in parse_qs(u.query).items()}
            try:
                if u.path == "/":
                    return self.send(200, PAGE.encode("utf-8"), "text/html; charset=utf-8")
                if u.path == "/api/config":
                    return self.send(200, json.dumps(app.config_json(), ensure_ascii=False).encode("utf-8"),
                                     "application/json; charset=utf-8")
                if q.get("name") not in app.sheets:
                    return self.send(404, b"not found", "text/plain")
                if u.path == "/api/sheet":
                    return self.send(200, json.dumps(app.sheet_json(q["name"]), ensure_ascii=False).encode("utf-8"),
                                     "application/json; charset=utf-8")
                if u.path in ("/img/crop", "/img/overview"):
                    return self.send(200, app.render(q["name"], q["id"], u.path[5:], q.get("others") == "1"), "image/jpeg")
                self.send(404, b"not found", "text/plain")
            except Exception as e:
                self.send(500, str(e).encode("utf-8"), "text/plain; charset=utf-8")

        def do_POST(self):
            try:
                body = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
                if urlparse(self.path).path != "/api/save" or body.get("name") not in app.sheets:
                    return self.send(404, b"not found", "text/plain")
                app.save(body["name"], str(body["id"]), body["fields"])
                self.send(200, b"ok", "text/plain")
            except PermissionError:
                self.send(500, "File CSV đang mở trong Excel? Đóng Excel rồi lưu lại.".encode("utf-8"), "text/plain; charset=utf-8")
            except Exception as e:
                self.send(500, str(e).encode("utf-8"), "text/plain; charset=utf-8")

        def log_message(self, *a):
            pass
    return H


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--set", choices=sorted(SETS), default="q05", help="q05 = gói q05_3 (V3); n4b = N4 tầng B (V6)")
    ap.add_argument("--port", type=int, default=8790)
    a = ap.parse_args()
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")  # console Windows mặc định cp1252
    srv = ThreadingHTTPServer(("127.0.0.1", a.port), handler(App(SETS[a.set])))
    print(f"Mở http://127.0.0.1:{a.port}  (Ctrl+C để dừng)", flush=True)
    srv.serve_forever()


if __name__ == "__main__":
    main()
