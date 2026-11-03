"""Nhánh P1 (kế hoạch Trí §3.2): kiểm từng ứng viên mẫu của lượt 1 bằng CLIP trước khi đưa vào lượt 2.

Ứng viên: cùng quy tắc select_pseudo (max điểm token tên vật, strict > 0.23, sort giảm dần, clamp xyxy),
nhưng lấy tối đa M khung và đánh dấu khung suy biến (valid=False) thay vì dừng.
CLIP: cùng model/revision, crop (round + clamp, không đệm), mẫu câu "a photo of {prompt}", batch 2,
cosine L2-normalized như p4_clip_score.py. Không đọc GT.
"""
from p4_clip_score import BATCH_SIZE, MODEL_ID, REVISION, TEMPLATE, crop_box


def top_candidates(scores, boxes, ids, image_size, threshold, maximum):
    import torch
    dot = ids.index(1012)
    indices = [i for i in range(dot) if ids[i] not in {0, 101, 102, 1012, 1029}]
    if not indices:
        raise ValueError("Missing target tokens")
    target = scores[:, indices].max(dim=-1).values
    candidates = torch.nonzero(target > threshold, as_tuple=False).flatten()
    if not len(candidates):
        return [], indices
    values, order = torch.sort(target[candidates], descending=True)
    selected = candidates[order[:maximum]]
    b = boxes[selected]
    width, height = image_size
    cx, cy, w, h = b[:, 0] * width, b[:, 1] * height, b[:, 2] * width, b[:, 3] * height
    xyxy = torch.stack(((cx - w / 2).clamp(0, width), (cy - h / 2).clamp(0, height),
                        (cx + w / 2).clamp(0, width), (cy + h / 2).clamp(0, height)), dim=1)
    out = []
    for rank, (pid, value, box) in enumerate(zip(selected.tolist(), values[:maximum].tolist(), xyxy.tolist()), start=1):
        out.append(dict(rank=rank, proposal_id=pid, countgd_score=value, box_xyxy=box,
                        valid=box[2] > box[0] and box[3] > box[1]))
    return out, indices


def choose(candidates, tau, maximum=3):
    """Giữ ứng viên hợp lệ có clip_cosine >= tau, lấy tối đa `maximum` theo điểm CountGD giảm dần."""
    return [c for c in candidates if c["valid"] and c["clip_cosine"] >= tau][:maximum]


class ClipVerifier:
    def __init__(self, device):
        import torch
        import transformers
        from transformers import CLIPModel, CLIPProcessor
        self.torch, self.device = torch, device
        self.processor = CLIPProcessor.from_pretrained(MODEL_ID, revision=REVISION, use_fast=False)
        self.model = CLIPModel.from_pretrained(MODEL_ID, revision=REVISION).to(device).eval()
        self.revision = getattr(self.model.config, "_commit_hash", None)
        if self.revision != REVISION:
            raise ValueError(f"Resolved CLIP revision {self.revision} != pinned {REVISION}")
        self.transformers_version = transformers.__version__

    def score(self, image, boxes, prompt):
        if not boxes:
            return []
        torch = self.torch
        width, height = image.size
        crops = [image.crop(tuple(crop_box(b, width, height))) for b in boxes]
        with torch.inference_mode():
            text = self.processor(text=[TEMPLATE.format(prompt=prompt)], return_tensors="pt", padding=True)
            text = {k: v.to(self.device) for k, v in text.items()}
            text_features = torch.nn.functional.normalize(self.model.get_text_features(**text), dim=-1)
            out = []
            for start in range(0, len(crops), BATCH_SIZE):
                pixels = self.processor(images=crops[start:start + BATCH_SIZE], return_tensors="pt")["pixel_values"].to(self.device)
                image_features = torch.nn.functional.normalize(self.model.get_image_features(pixel_values=pixels), dim=-1)
                out.extend((image_features @ text_features.T)[:, 0].cpu().tolist())
        return out
