"""Audit the pinned stock model loader, without running inference or editing upstream."""
import ast
import hashlib
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
REPO = ROOT / "CountGDPlusPlus"
EXPECTED = "c6adbad84897f266d25ad6d1672ddea5ef52d1fcdd8f6ec54d94be04c8fa32e9"

def sha(path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def main():
    source = REPO / "process_folder.py"
    if sha(source) != EXPECTED:
        raise RuntimeError("Upstream source changed; review before auditing")
    tree = ast.parse(source.read_text())
    tree.body = [n for n in tree.body if isinstance(n, (ast.Import, ast.ImportFrom, ast.FunctionDef))]
    changed = 0
    for fn in tree.body:
        if isinstance(fn, ast.FunctionDef) and fn.name == "build_model_and_transforms":
            for i, node in enumerate(fn.body):
                if isinstance(node, ast.Expr) and isinstance(node.value, ast.Call) and isinstance(node.value.func, ast.Attribute) and node.value.func.attr == "load_state_dict":
                    fn.body[i] = ast.Assign(targets=[ast.Attribute(value=ast.Name(id="model", ctx=ast.Load()), attr="_audit_load_report", ctx=ast.Store())], value=node.value)
                    changed += 1
    assert changed == 1
    ast.fix_missing_locations(tree)
    sys.path.insert(0, str(REPO))
    os.chdir(REPO)
    ns = {"__name__": "countgdpp_stock_definitions"}
    exec(compile(tree, str(source), "exec"), ns)
    args = ns["build_arg_parser"]().parse_args([])
    model, _ = ns["build_model_and_transforms"](args)
    report = model._audit_load_report
    result = {
        "audit_date": "2026-10-14",
        "checkpoint_sha256": sha(REPO / args.pretrain_model_path),
        "process_folder_sha256": EXPECTED,
        "model_state_keys": len(model.state_dict()),
        "missing_keys": list(report.missing_keys),
        "unexpected_keys": list(report.unexpected_keys),
        "shape_load_succeeded": True,
        "scope": "Local checkpoint compatibility, not author-published hash authentication or inference correctness",
    }
    out = ROOT / "results/countgdpp/checkpoint_audit_2026-10-14.json"
    out.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))
    if result["missing_keys"] or result["unexpected_keys"]:
        raise SystemExit("Review incompatible keys before pilot")

if __name__ == "__main__":
    main()
