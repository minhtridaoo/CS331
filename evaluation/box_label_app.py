"""Mini app gán nhãn từng khung cho gói q05_3 (V3): xem crop + ảnh toàn cảnh, điền nhãn, "Lưu & tiếp" ghi thẳng vào CSV.
Chỉ đọc ảnh/CSV đã có, không chạy model. Chỉ ghi các cột nhãn (label_type, actual_class, object_id, uncertain, note,
reviewer, date) của đúng dòng đang sửa; giữ nguyên thứ tự cột, BOM và kiểu xuống dòng của file.

Example (from CS331 root): python evaluation/box_label_app.py  rồi mở http://127.0.0.1:8790
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
PKG = ROOT / "results/countgdpp/q05_error_analysis_package_20261027"
IMAGE = ROOT / "results/countgdpp/m4_first5_b0/jobs/015_q05_3/input/mcac_27.jpg"
QUERY = {"image_id": "mcac_27", "query_id": "q05_3", "prompt": "blackberries", "gt": 3}
SHEET_DESC = {"pseudo": "3 mẫu tự chọn sau lượt 1 (B2 dùng làm exemplar cho lượt 2)",
              "B0": "khung đếm của B0: một lượt, ảnh + text",
              "B2": "khung đếm cuối của B2: lượt 2 dùng 3 mẫu tự chọn"}
SHEETS = {"pseudo": "q05_3_B2_pseudo_labels_BLANK.csv", "B0": "q05_3_B0_stage1_labels_BLANK.csv",
          "B2": "q05_3_B2_final_labels_BLANK.csv"}
EDITABLE = ["label_type", "actual_class", "object_id", "uncertain", "note", "reviewer"]


def read_sheet(path):
    raw = path.read_bytes()
    rows = list(csv.reader(raw.decode("utf-8-sig").splitlines()))
    meta = {"bom": raw.startswith(b"\xef\xbb\xbf"), "eol": "\r\n" if b"\r\n" in raw else "\n"}
    return rows[0], [dict(zip(rows[0], r)) for r in rows[1:] if r], meta


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
    def __init__(self, pkg, image):
        self.pkg, self.img = pkg, Image.open(image).convert("RGB")

    def load(self, name):
        return read_sheet(self.pkg / SHEETS[name])

    def sheet_json(self, name):
        _, rows, _ = self.load(name)
        others = {n: self.load(n)[1] for n in SHEETS if n != name}
        out = []
        for r in rows:
            b = box(r)
            overlaps = sorted(([round(iou(b, box(o)), 2), o["rank"], o.get("label_type", ""), o.get("object_id", "")]
                               for o in rows if o is not r and iou(b, box(o)) >= 0.3), reverse=True)
            same = [f"{n} rank {o['rank']}" for n, rs in others.items() for o in rs if iou(b, box(o)) > 0.98]
            out.append({**r, "w": round(b[2] - b[0]), "h": round(b[3] - b[1]), "overlaps": overlaps, "same_as": same})
        return {"name": name, "file": str(self.pkg / SHEETS[name]), "image": f"{self.img.width}x{self.img.height}",
                "query": QUERY, "desc": SHEET_DESC[name],
                "rows": out}

    def render(self, name, rank, kind, others):
        _, rows, _ = self.load(name)
        cur = next(r for r in rows if r["rank"] == rank)
        b = box(cur)
        if kind == "overview":
            im = self.img.copy()
            d = ImageDraw.Draw(im)
            if others:
                for o in rows:
                    if o is not cur:
                        d.rectangle(box(o), outline=(255, 220, 0), width=2)
            d.rectangle(b, outline=(255, 0, 0), width=8)
            im.thumbnail((900, 900))
        else:
            w, h = b[2] - b[0], b[3] - b[1]
            pad = max(max(w, h) * 0.35, (320 - max(w, h)) / 2)  # khung nhỏ (từng hạt) vẫn thấy cả quả xung quanh
            c = (max(0, b[0] - pad), max(0, b[1] - pad), min(self.img.width, b[2] + pad), min(self.img.height, b[3] + pad))
            im = self.img.crop(c)
            s = 560 / max(im.width, im.height)
            im = im.resize((round(im.width * s), round(im.height * s)))
            d = ImageDraw.Draw(im)
            shift = lambda q: [(q[0] - c[0]) * s, (q[1] - c[1]) * s, (q[2] - c[0]) * s, (q[3] - c[1]) * s]
            if others:
                for o in rows:
                    if o is not cur and iou(box(o), list(c)) > 0:
                        ob = shift(box(o))
                        d.rectangle(ob, outline=(255, 220, 0), width=1)
                        d.text((ob[0] + 2, ob[1] + 1), o["rank"], fill=(255, 220, 0))
            d.rectangle(shift(b), outline=(255, 0, 0), width=3)
        buf = io.BytesIO()
        im.save(buf, "JPEG", quality=90)
        return buf.getvalue()

    def save(self, name, rank, fields):
        header, rows, meta = self.load(name)
        r = next(r for r in rows if r["rank"] == rank)
        for k in EDITABLE:
            if k in header and k in fields:
                r[k] = str(fields[k]).strip()
        r["date"] = datetime.date.today().isoformat()
        write_sheet(self.pkg / SHEETS[name], header, rows, meta)


PAGE = r"""<!doctype html><html lang="vi"><head><meta charset="utf-8"><title>Gán nhãn khung q05_3</title>
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
textarea{height:70px}
.btns{display:flex;gap:8px;margin-top:12px}button{font-size:15px;padding:7px 14px;cursor:pointer}
#next{background:#2563eb;color:#fff;border:0;border-radius:6px}
#msg{margin-top:8px;font-size:14px}.warn{color:#b45309}.ok{color:#15803d}
.hint{font-size:12px;color:#71717a}
#banner{padding:10px 14px;background:#eff6ff;border-bottom:1px solid #bfdbfe;font-size:15px;line-height:1.5}
#banner .p{font-size:20px;font-weight:700;color:#1d4ed8}
</style></head><body>
<header><b>Gán nhãn khung q05_3</b>
<select id="sheet"><option value="pseudo">pseudo (3)</option><option value="B0">B0 (21)</option><option value="B2">B2 final (79)</option></select>
<span id="prog"></span><label style="margin:0;font-weight:400"><input type="checkbox" id="others"> hiện các khung khác</label>
<span class="hint">Phím tắt (ngoài ô chữ): 1 target · 2 duplicate · 3 part · 4 wrong_class · 5 background · ←/→ chuyển khung · Ctrl+Enter lưu &amp; tiếp</span></header>
<div id="banner"></div>
<div id="chips"></div>
<main>
<div class="card"><div id="title" style="font-weight:700;margin-bottom:6px"></div><img id="crop"><div class="hint">Đỏ = khung đang xét (đã nới rộng để thấy xung quanh, tối thiểu 320 px ảnh gốc)</div></div>
<div>
<div class="card"><img id="ov" style="max-height:330px"></div>
<div class="card" style="margin-top:10px"><table id="info"></table></div>
<div class="card" style="margin-top:10px">
<label>label_type</label><select id="label_type"><option></option><option>target</option><option>duplicate</option><option>part</option><option>wrong_class</option><option>background</option></select>
<label>actual_class</label><input type="text" id="actual_class" list="cls"><datalist id="cls"><option>blackberries</option><option>raspberries</option><option>blueberries</option><option>strawberries</option><option>cherries</option></datalist>
<label>object_id <span class="hint">b1 trên phải có cuống · b2 trên giữa · b3 dưới phải sau dâu/cherry</span></label><select id="object_id"><option></option><option>b1</option><option>b2</option><option>b3</option></select>
<label><input type="checkbox" id="uncertain"> uncertain (phân vân)</label>
<label>note</label><textarea id="note"></textarea>
<label>reviewer</label><input type="text" id="reviewer">
<div class="btns"><button id="prev">← Trước</button><button id="savebtn">Lưu</button><button id="next">Lưu &amp; tiếp →</button></div>
<div id="msg"></div></div></div></main>
<script>
let data=null,i=0;const $=id=>document.getElementById(id);
async function load(name,keep){data=await (await fetch('/api/sheet?name='+name)).json();if(!keep){i=data.rows.findIndex(r=>!r.label_type);if(i<0)i=0}show()}
function show(){const r=data.rows[i],o=$('others').checked?1:0,q=`name=${data.name}&rank=${r.rank}&others=${o}`;
$('crop').src='/img/crop?'+q;$('ov').src='/img/overview?'+q;
$('title').textContent=`${data.name} · rank ${r.rank}  (${i+1}/${data.rows.length})`;
const ov=r.overlaps.length?r.overlaps.map(x=>`rank ${x[1]} (IoU ${x[0]})${x[2]?' = '+x[2]+(x[3]?' '+x[3]:''):''}`).join('<br>'):'không có';
const Q=data.query;$('banner').innerHTML=`Prompt: <span class="p">"${Q.prompt}"</span> · query <b>${Q.query_id}</b> · ảnh <b>${Q.image_id}</b> · GT <b>${Q.gt}</b> quả<br>
Đang xem: <b>${data.name}</b>, ${data.desc}. Câu hỏi cho mỗi khung: khung đỏ có ôm đúng <b>một quả ${Q.prompt} trọn vẹn</b> không? Nếu không thì nó là gì?`;
$('info').innerHTML=`<tr><td>File</td><td>${data.file}</td></tr><tr><td>Ảnh</td><td>${Q.image_id} (${data.image}) · ${Q.query_id} "${Q.prompt}" · GT ${Q.gt}</td></tr>
<tr><td>Tọa độ</td><td>x1 ${r.x1}, y1 ${r.y1}, x2 ${r.x2}, y2 ${r.y2}</td></tr><tr><td>Kích thước</td><td>${r.w} × ${r.h} px · area ${r.area_px} · score ${r.score}</td></tr>
<tr><td>Chồng lên (IoU≥0.3)</td><td>${ov}</td></tr>${r.same_as.length?`<tr><td>Trùng tọa độ</td><td>${r.same_as.join(', ')}</td></tr>`:''}`;
for(const k of ['label_type','actual_class','object_id','note'])$(k).value=r[k]||'';
$('uncertain').checked=(r.uncertain||'')!=='';$('reviewer').value=r.reviewer||'Trieu';$('msg').textContent='';
const done=data.rows.filter(x=>x.label_type).length;$('prog').textContent=`đã điền ${done}/${data.rows.length}`;
$('chips').innerHTML=data.rows.map((x,j)=>`<span class="chip ${x.label_type?'done':''} ${x.uncertain?'unc':''} ${j===i?'cur':''}" data-j="${j}" title="${x.label_type} ${x.object_id||x.actual_class||''}">${x.rank}</span>`).join('');
document.querySelectorAll('.chip').forEach(c=>c.onclick=()=>{i=+c.dataset.j;show()})}
function warn(f){const t=f.label_type;if(!t)return 'Chưa chọn label_type.';
if(['target','duplicate','part'].includes(t)&&!f.object_id)return t+' cần object_id (b1/b2/b3).';
if(t==='wrong_class'&&!f.actual_class)return 'wrong_class cần actual_class.';
if(t!=='wrong_class'&&t!=='background'&&f.actual_class&&f.actual_class!=='blackberries')return t+' nhưng actual_class không phải blackberries?';return ''}
async function save(go){const r=data.rows[i],f={label_type:$('label_type').value,actual_class:$('actual_class').value,object_id:$('object_id').value,
uncertain:$('uncertain').checked?'yes':'',note:$('note').value,reviewer:$('reviewer').value};
if(['target','duplicate','part'].includes(f.label_type)&&!f.actual_class)f.actual_class='blackberries';
const w=warn(f);if(w&&!confirm(w+'\nVẫn lưu?'))return;
const res=await fetch('/api/save',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({name:data.name,rank:r.rank,fields:f})});
if(!res.ok){$('msg').innerHTML=`<span class="warn">Lỗi lưu: ${await res.text()}</span>`;return}
const keep=i;await load(data.name,true);i=go&&keep<data.rows.length-1?keep+1:keep;show();$('msg').innerHTML=`<span class="ok">Đã lưu rank ${r.rank}.</span>`}
$('next').onclick=()=>save(true);$('savebtn').onclick=()=>save(false);$('prev').onclick=()=>{if(i>0){i--;show()}};
$('sheet').onchange=e=>load(e.target.value);$('others').onchange=show;
document.addEventListener('keydown',e=>{if(e.ctrlKey&&e.key==='Enter'){save(true);return}
if(['INPUT','TEXTAREA','SELECT'].includes(document.activeElement.tagName))return;
const m={'1':'target','2':'duplicate','3':'part','4':'wrong_class','5':'background'};
if(m[e.key])$('label_type').value=m[e.key];if(e.key==='ArrowRight'&&i<data.rows.length-1){i++;show()}if(e.key==='ArrowLeft'&&i>0){i--;show()}});
load('B0');$('sheet').value='B0';
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
                if q.get("name") not in SHEETS:
                    return self.send(404, b"not found", "text/plain")
                if u.path == "/api/sheet":
                    return self.send(200, json.dumps(app.sheet_json(q["name"]), ensure_ascii=False).encode("utf-8"),
                                     "application/json; charset=utf-8")
                if u.path in ("/img/crop", "/img/overview"):
                    return self.send(200, app.render(q["name"], q["rank"], u.path[5:], q.get("others") == "1"), "image/jpeg")
                self.send(404, b"not found", "text/plain")
            except Exception as e:
                self.send(500, str(e).encode("utf-8"), "text/plain; charset=utf-8")

        def do_POST(self):
            try:
                body = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
                if urlparse(self.path).path != "/api/save" or body.get("name") not in SHEETS:
                    return self.send(404, b"not found", "text/plain")
                app.save(body["name"], str(body["rank"]), body["fields"])
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
    ap.add_argument("--pkg", type=Path, default=PKG)
    ap.add_argument("--image", type=Path, default=IMAGE)
    ap.add_argument("--port", type=int, default=8790)
    a = ap.parse_args()
    srv = ThreadingHTTPServer(("127.0.0.1", a.port), handler(App(a.pkg, a.image)))
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")  # console Windows mặc định cp1252
    print(f"Mở http://127.0.0.1:{a.port}  (Ctrl+C để dừng)", flush=True)
    srv.serve_forever()


if __name__ == "__main__":
    main()
