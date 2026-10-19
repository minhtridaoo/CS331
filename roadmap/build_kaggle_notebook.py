import json
from pathlib import Path

OUT = Path(__file__).parent
cells = []
def md(s):
    cells.append(dict(cell_type='markdown', metadata={}, source=s.strip().splitlines(True)))
def code(s):
    cells.append(dict(cell_type='code', metadata={}, execution_count=None, outputs=[], source=s.strip().splitlines(True)))

md('''# CountGD++ — FSCD-147 test trên Kaggle
Mục tiêu: chạy cấu hình README chính thức text + synthetic + pseudo + adaptive cropping.
Paper v2, Table 1, Ours(t+p+s): MAE **8.39**, RMSE **27.03** (số tham chiếu, không bảo đảm khớp).
Nguồn: https://arxiv.org/html/2512.23351v2#S6.T1 và https://github.com/niki-amini-naieni/CountGDPlusPlus

Bật **GPU** và **Internet** trong Kaggle. Chạy từng cell theo thứ tự; gặp lỗi thì dừng và gửi log.
Notebook dùng môi trường Python riêng, không cần thay kernel. Chỉ dùng 1 GPU.
Chưa được thực thi trên Kaggle; đã kiểm cấu trúc và cú pháp ở máy local.
Không thay ngưỡng theo test. Không so trực tiếp MAE này với 5 ảnh/15 query dev khác dữ liệu.
''')
md('## 1. Kiểm GPU và tạo thư mục')
code(r'''
import os, sys, subprocess, json, shutil, re, hashlib, zipfile, tarfile, math, csv
from pathlib import Path
ROOT = Path('/kaggle/working/countgdpp_paper')
assert Path('/kaggle').exists(), 'Cell này dành cho Kaggle.'
ROOT.mkdir(exist_ok=True)
REPO = ROOT / 'CountGDPlusPlus'
OUT = ROOT / 'results'
OUT.mkdir(exist_ok=True)
ENV = os.environ.copy()
ENV.update(CUDA_VISIBLE_DEVICES='0', MAX_JOBS='2', MPLBACKEND='Agg')
def run(args, cwd=None, log=None):
    args = [str(x) for x in args]
    print('RUN:', ' '.join(args), flush=True)
    f = open(log, 'w', encoding='utf-8') if log else None
    try:
        with subprocess.Popen(args, cwd=cwd, env=ENV, stdout=subprocess.PIPE,
                              stderr=subprocess.STDOUT, text=True, bufsize=1) as p:
            for line in p.stdout:
                print(line, end='', flush=True)
                if f: f.write(line); f.flush()
            rc = p.wait()
        if rc: raise RuntimeError(f'Exit {rc}; xem log {log}. Không chạy cell tiếp.')
    finally:
        if f: f.close()
def sha(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for b in iter(lambda: f.read(8*1024*1024), b''): h.update(b)
    return h.hexdigest()
run(['nvidia-smi'], log=OUT/'gpu.txt')
print('Disk free GB:', round(shutil.disk_usage(ROOT).free/1e9, 1))
''')
md('## 2. Môi trường Python 3.10, PyTorch 2.5.1 và CUDA build tools\nCell này tải/cài thư viện, có thể lâu. Nếu CUDA toolkit hiện tại không phải 12.x, cell dừng để xử lý môi trường thay vì chạy cấu hình không kiểm chứng.')
code(r'''
run([sys.executable, '-m', 'pip', 'install', '-q', 'uv'])
UV = shutil.which('uv')
assert UV
run([UV, 'venv', '--python', '3.10', ROOT/'venv'])
PY = ROOT/'venv/bin/python'
def pip(*args): run([UV, 'pip', 'install', '--python', PY, *args])
nvcc = shutil.which('nvcc')
assert nvcc, 'Kaggle thiếu nvcc. Gửi output cell này để bổ sung CUDA toolkit.'
nv = subprocess.check_output([nvcc, '--version'], text=True)
print(nv)
assert re.search(r'release 12\.', nv), 'Cần CUDA toolkit 12.x cho môi trường đã chọn. Gửi log để điều chỉnh.'
ENV['CUDA_HOME'] = str(Path(nvcc).resolve().parent.parent)
run(['apt-get', 'update', '-qq'])
run(['apt-get', 'install', '-y', '-qq', 'gcc-11', 'g++-11', 'ninja-build'])
ENV.update(CC='/usr/bin/gcc-11', CXX='/usr/bin/g++-11')
pip('torch==2.5.1', 'torchvision==0.20.1', '--index-url', 'https://download.pytorch.org/whl/cu121')
pip('setuptools<81', 'wheel', 'ninja', 'numpy==1.26.4', 'transformers==4.44.2',
    'timm==1.0.9', 'scipy', 'termcolor', 'addict', 'yapf==0.40.1',
    'opencv-python-headless==4.10.0.84', 'pycocotools', 'colorlog', 'ushlex',
    'tqdm', 'matplotlib', 'Pillow', 'gdown', 'einops', 'supervision==0.22.0',
    'pyyaml', 'requests', 'pandas', 'scikit-learn', 'segment-anything==1.0', 'deeplake<4')
COMMIT = '8489f836d75eb407ae778c56cff1f72cc6f8baae'
if not REPO.exists(): run(['git','clone','https://github.com/niki-amini-naieni/CountGDPlusPlus.git',REPO])
run(['git','checkout',COMMIT], cwd=REPO)
run([PY, '-c', 'import torch; assert torch.cuda.is_available(); print(torch.__version__, torch.version.cuda, torch.cuda.get_device_name(0))'])
# Pin the exact detectron2 checkout selected in this session and retain its hash.
D2 = ROOT/'detectron2'
if not D2.exists(): run(['git','clone','https://github.com/facebookresearch/detectron2.git',D2])
run(['git','rev-parse','HEAD'], cwd=D2, log=OUT/'detectron2_commit.txt')
run([UV,'pip','install','--python',PY,'--no-build-isolation',D2], log=OUT/'detectron2_build.txt')
OPS = REPO/'models/GroundingDINO/ops'
run([PY,'setup.py','build','install'], cwd=OPS, log=OUT/'ops_build.txt')
run([PY,'test.py'], cwd=OPS, log=OUT/'ops_tests.txt')
checks = re.findall(r'\* (True|False) check_', (OUT/'ops_tests.txt').read_text())
assert len(checks) == 6 and all(x=='True' for x in checks), checks
run([PY,'-c','import torch; import detectron2._C; import MultiScaleDeformableAttention; import segment_anything; import engine_inference; import main_inference; print("Imports OK")'],cwd=REPO)
run([UV,'pip','freeze','--python',PY], log=OUT/'packages.txt')
''')
md('''## 3. Tải dữ liệu và checkpoint chính thức
Nếu Google Drive giới hạn tải, tải các file từ link README bằng trình duyệt rồi đính kèm dưới dạng **Kaggle Dataset riêng tư**.
Điền đường dẫn file nén/checkpoint trong LOCAL bên dưới, rồi chạy lại cell này. Không bỏ synthetic/crops để vượt lỗi vì sẽ đổi cấu hình.
''')
code(r'''
LOCAL = dict(images='', crops='', synthetic='', weights='')
IDS = dict(images='1m_v_hBwXH1NzcuUj_qa-ziKn-LYfUWA6',
           crops='1QyMfhPRp85La8URii8xL6wOoqcQpXhsD',
           synthetic='1XyE77D0bxEKDsPYvpaeD6KyXnSLye1Qg',
           weights='1j6N22TtKu2NVcKpgfrf-sJHGeLDqs9hs')
DOWNLOADS = ROOT/'downloads'; DOWNLOADS.mkdir(exist_ok=True)
EXTRACT = ROOT/'assets'; EXTRACT.mkdir(exist_ok=True)
def asset(key):
    if LOCAL[key]:
        p = Path(LOCAL[key]); assert p.is_file(), p
        return p
    p = DOWNLOADS/(key+'.download')
    if not p.exists():
        tmp = p.with_suffix('.partial')
        run([PY,'-m','gdown',IDS[key],'-O',tmp])
        tmp.rename(p)
    return p
def unpack(p, target):
    if (target/'.complete').exists(): return
    target.mkdir(exist_ok=True)
    if zipfile.is_zipfile(p):
        with zipfile.ZipFile(p) as z:
            for n in z.namelist():
                assert (target/n).resolve().is_relative_to(target.resolve()), n
            z.extractall(target)
    elif tarfile.is_tarfile(p):
        with tarfile.open(p) as t: t.extractall(target, filter='data')
    else: raise ValueError(f'{p} không phải archive hợp lệ; kiểm tra tải Google Drive.')
    (target/'.complete').touch()
for key in ('images','crops','synthetic'): unpack(asset(key), EXTRACT/key)
CKPT = REPO/'checkpoints'; CKPT.mkdir(exist_ok=True)
WEIGHTS = CKPT/'countgd_plusplus.pth'
if not WEIGHTS.exists(): shutil.copy2(asset('weights'), WEIGHTS)
assert WEIGHTS.stat().st_size > 1_000_000_000, 'Checkpoint tải thiếu hoặc là trang HTML.'
if not (CKPT/'bert-base-uncased/config.json').exists():
    run([PY,'download_bert.py'], cwd=REPO, log=OUT/'bert_download.txt')
''')
md('## 4. Kiểm đủ 1.190 ảnh, synthetic exemplars và crops; lưu cấu hình')
code(r'''
def unique_dir(name, base):
    hits = [p for p in base.rglob(name) if p.is_dir()]
    assert len(hits)==1, f'Cần đúng 1 thư mục {name}, tìm được {hits}'
    return hits[0]
IMAGES = unique_dir('images_384_VarV2', EXTRACT/'images')
SYNTH = next((EXTRACT/'synthetic').rglob('generated_exemplars.json')).parent
CROPS = unique_dir('pseudo-crops', EXTRACT/'crops').parent
ANNO = REPO/'data/fscd147/countgd_test_fscd147.json'
GT = REPO/'data/fscd147/instances_test.json'
ann = json.loads(ANNO.read_text()); gt = json.loads(GT.read_text())
images = ann['images']; names = [x['file_name'] for x in images]
assert len(images)==1190 and len(set(names))==1190
assert {x['id'] for x in images} == {x['id'] for x in gt['images']}
for name in names: assert (IMAGES/name).is_file(), name
exemplars = json.loads((SYNTH/'generated_exemplars.json').read_text())
for name in names:
    assert name in exemplars and (SYNTH/name).is_file(), 'Thiếu synthetic: '+name
assert list((CROPS/'pseudo-crops').glob('crop-*.png')), 'Thiếu super-resolution crops'
cfg = json.loads((REPO/'config/datasets_fscd147_test.json').read_text())
cfg['val'][0].update(root=str(IMAGES), anno=str(ANNO))
DATA_CFG = OUT/'datasets_test.json'; DATA_CFG.write_text(json.dumps(cfg,indent=2))
manifest = dict(status='prepared_not_run', repo_commit=COMMIT, dataset='FSCD-147',split='test',
    expected_images=1190, paper='https://arxiv.org/html/2512.23351v2#S6.T1',
    variant='text+synthetic+pseudo+adaptive_crop', paper_mae=8.39,paper_rmse=27.03,
    checkpoint_sha256=sha(WEIGHTS), annotation_sha256=sha(ANNO),gt_sha256=sha(GT),
    synthetic_annotation_sha256=sha(SYNTH/'generated_exemplars.json'),
    input_images=str(IMAGES), synthetic=str(SYNTH), crops=str(CROPS),
    note='Môi trường Kaggle; không tuyên bố tái tạo môi trường tác giả từng phiên bản.')
(OUT/'run_config.json').write_text(json.dumps(manifest,indent=2,ensure_ascii=False))
print('PASS: đủ 1190 ảnh và synthetic; crops có sẵn. Chưa chạy inference.')
''')
md('''## 5. Chạy đánh giá đầy đủ
Chạy một lần, không bật debug và không đổi ngưỡng. Không có resume theo ảnh trong script gốc;
nếu phiên bị ngắt, lần chạy chưa hoàn tất và cần chạy lại. Mỗi lần có thư mục riêng.
Thời gian phụ thuộc GPU, không suy từ ảnh chụp của nhóm khác.
''')
code(r'''
from datetime import datetime, timezone
RUN = OUT/('full_'+datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ'))
RUN.mkdir()
PRED = RUN/'detections_test_text_only.json'
CMD = [PY,'-u','main_inference.py','--output_dir',RUN,
       '-c','config/cfg_fscd147_test.py','--eval','--datasets',DATA_CFG,
       '--pretrain_model_path',WEIGHTS,'--options',
       'text_encoder_type='+str(CKPT/'bert-base-uncased'),
       '--coco_output_file',PRED,'--fscd_gt_file',GT,'--num_exemplars','0',
       '--use_synth_exemplars','--synth_exemplar_folder',SYNTH,
       '--superres_folder',CROPS,'--crop','--num_workers','2']
manifest['command'] = [str(x) for x in CMD]
manifest['status'] = 'running'
(RUN/'run_config.json').write_text(json.dumps(manifest,indent=2,ensure_ascii=False))
try:
    run(CMD,cwd=REPO,log=RUN/'console.log')
except Exception:
    manifest['status']='failed_or_interrupted'
    (RUN/'run_config.json').write_text(json.dumps(manifest,indent=2,ensure_ascii=False))
    raise
manifest['status']='inference_finished_pending_validation'
(RUN/'run_config.json').write_text(json.dumps(manifest,indent=2,ensure_ascii=False))
''')
md('## 6. Tính lại MAE/RMSE từ log, kiểm đủ ảnh và đóng gói kết quả\nKhông dùng số boxes của JSON để thay số đếm sau adaptive cropping. Giữ nguyên JSON để phân tích detection riêng.')
code(r'''
log = (RUN/'console.log').read_text()
rows=[]; current=None
name_set=set(names)
for line in log.splitlines():
    name=line.strip()
    if name in name_set: current=name
    match=re.search(r'Pred Count: ([\d.eE+-]+), GT Count: ([\d.eE+-]+)',line)
    if match:
        assert current is not None, 'Không ghép được tên ảnh với count'
        rows.append(dict(image=current,pred=float(match[1]),gt=float(match[2])))
        current=None
assert len(rows)==1190 and {x['image'] for x in rows}==set(names)
assert len({x['image'] for x in rows})==len(rows)
assert all(math.isfinite(x[k]) and x[k]>=0 for x in rows for k in ('pred','gt'))
err=[abs(x['pred']-x['gt']) for x in rows]
mae=sum(err)/len(err); rmse=math.sqrt(sum(x*x for x in err)/len(err))
summary=re.findall(r'Total MAE: ([\d.eE+-]+), Total RMSE: ([\d.eE+-]+)',log)
assert len(summary)==1
assert math.isclose(mae,float(summary[0][0]),rel_tol=1e-8,abs_tol=1e-8)
assert math.isclose(rmse,float(summary[0][1]),rel_tol=1e-8,abs_tol=1e-8)
assert PRED.is_file() and isinstance(json.loads(PRED.read_text())['annotations'],list)
with open(RUN/'counts.csv','w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=['image','pred','gt']); w.writeheader(); w.writerows(rows)
metrics=dict(n=len(rows),mae=mae,rmse=rmse,paper_mae=8.39,paper_rmse=27.03,
             delta_mae=mae-8.39,delta_rmse=rmse-27.03)
(RUN/'metrics.json').write_text(json.dumps(metrics,indent=2))
manifest['status']='complete_count_metrics_verified'
(RUN/'run_config.json').write_text(json.dumps(manifest,indent=2,ensure_ascii=False))
archive=shutil.make_archive('/kaggle/working/countgdpp_paper_results','zip',OUT)
print(json.dumps(metrics,indent=2)); print('Tải về:',archive)
from IPython.display import FileLink, display
display(FileLink(archive))
''')
md('''## Đọc kết quả
- Chỉ coi hoàn tất khi cell 6 xác nhận đủ 1.190 ảnh và tạo metrics.json.
- Đối chiếu với dòng **Ours(t+p+s)**, không phải Ours(t+p) hoặc B0 một lượt.
- Nếu lệch paper: kiểm log tải checkpoint, code version, dữ liệu và assets; không chỉnh threshold trên test cho khớp số.
- Kết quả 5 ảnh/15 query dev để bảng riêng. Muốn so công bằng các cấu hình phải chạy cùng dữ liệu và evaluator.
- Lưu ZIP bằng Download hoặc Save Version sau khi chạy. Không xóa repo/log khi chưa tải kết quả.
''')
nb=dict(cells=cells,metadata=dict(kernelspec=dict(display_name='Python 3',language='python',name='python3'),language_info=dict(name='python',version='3.10')),nbformat=4,nbformat_minor=5)
for i,c in enumerate(cells):
    c['id']=f'cell-{i:02d}'
    if c['cell_type']=='code': compile(''.join(c['source']),f'cell-{i}','exec')
dest=OUT/'COUNTGDPP_FSCD147_KAGGLE.ipynb'
dest.write_text(json.dumps(nb,ensure_ascii=False,indent=1),encoding='utf-8')
print(dest)
print('Validated code cells:',sum(c['cell_type']=='code' for c in cells))
