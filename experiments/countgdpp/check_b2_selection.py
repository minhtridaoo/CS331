"""Focused checks: selection parity with upstream, strict threshold, empty branch and coordinate scale."""
import ast
import torch
from run_b2_pilot import REPO, select_pseudo
source=REPO/"test_shanghai_tech.py"
tree=ast.parse(source.read_text())
tree.body=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=="get_pseudo_exemplars"]
ns={"torch":torch};exec(compile(tree,str(source),"exec"),ns)
class Sample:
    def char_to_token(self,pos):return 1
class Tokens:
    def __getitem__(self,key):
        return torch.tensor([[101,11117,1012,102]]) if key=="input_ids" else Sample()
prob=torch.tensor([[.01,.2,.01,.01],[.01,.9,.01,.01],[.01,.4,.01,.01],[.01,.8,.01,.01],[.01,.6,.01,.01]])
boxes=torch.tensor([[.5,.5,.1,.1],[.01,.02,.1,.1],[.4,.3,.2,.2],[.7,.8,.2,.3],[.5,.4,.3,.2]])
# Use the same sigmoid result on both sides, avoiding any artificial rounding difference.
logits=torch.logit(prob);scores=logits.sigmoid()
ours,values,ids,_=select_pseudo(scores,boxes,[101,11117,1012,102],(626,506))
reference=ns["get_pseudo_exemplars"]({"pred_logits":logits[None],"pred_boxes":boxes[None],"token":Tokens()},[(506,626)],[torch.tensor([0])],[["rulers"]],["rulers ."],.23)[0]
torch.testing.assert_close(ours,reference)
assert ids==[1,3,4] and len(ours)==3 and ours.min()>=0
empty,_,ids,_=select_pseudo(torch.zeros_like(scores),boxes,[101,11117,1012,102],(626,506))
assert empty.shape==(0,4) and ids==[]
threshold=torch.zeros((1,4));threshold[0,1]=.23
assert len(select_pseudo(threshold,boxes[:1],[101,11117,1012,102],(626,506))[0])==0
large,_,_,_=select_pseudo(scores,boxes,[101,11117,1012,102],(1252,1012))
torch.testing.assert_close(large,ours*2)
print("PASS: upstream top-3 parity, coordinate clipping/scaling, strict threshold and no-pseudo selection")
