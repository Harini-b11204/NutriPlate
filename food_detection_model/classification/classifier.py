import os
from PIL import Image
import sys

# Load ImageNet labels from the package directory (no network required)
LABELS_FILE = os.path.join(os.path.dirname(__file__), 'imagenet_classes.txt')
if os.path.exists(LABELS_FILE):
    with open(LABELS_FILE, 'r', encoding='utf-8') as f:
        idx2label = [line.strip() for line in f.readlines()]
else:
    idx2label = []

# Try to import torch/torchvision; if unavailable, fall back gracefully
try:
    import torch
    import torchvision.transforms as transforms
    from torchvision import models
    TORCH_AVAILABLE = True
except Exception:
    torch = None
    transforms = None
    models = None
    TORCH_AVAILABLE = False

# If torch is available, try to load a pre-trained ResNet18 model lazily
model = None
transform = None
if TORCH_AVAILABLE:
    try:
        model = models.resnet18(pretrained=True)
        model.eval()
        transform = transforms.Compose([
            transforms.Resize(256),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
        ])
    except Exception:
        # model load failed (possibly no internet or missing cached weights)
        model = None


def classify_food(image_path):
    """Classify a food image and return a human-readable label.

    Behavior:
    - If torchvision model is available and loads, returns the top predicted ImageNet label.
    - If model is unavailable but label file exists, returns the first label as a fallback.
    - On error, returns 'unknown_food'.
    """
    # If model is not available, avoid heavy processing
    if model is None or not TORCH_AVAILABLE:
        if idx2label:
            return idx2label[0]
        return 'unknown_food'

    try:
        image = Image.open(image_path).convert('RGB')
        img_t = transform(image)
        batch_t = torch.unsqueeze(img_t, 0)
        with torch.no_grad():
            out = model(batch_t)
        _, index = torch.max(out, 1)
        idx = index.item()
        if 0 <= idx < len(idx2label):
            return idx2label[idx]
        return f'label_{idx}'
    except Exception:
        return 'unknown_food'


def get_topk(image_path, k=5):
    """Return list of (label, prob) for the top-k ImageNet predictions.

    Each item is a dict: {"label": str, "prob": float, "idx": int}
    Gracefully falls back if model/labels are unavailable.
    """
    # fallback when model not available
    if model is None or not TORCH_AVAILABLE:
        if idx2label:
            return [{"label": idx2label[0], "prob": 1.0, "idx": 0}]
        return [{"label": "unknown_food", "prob": 1.0, "idx": -1}]

    try:
        image = Image.open(image_path).convert('RGB')
        img_t = transform(image)
        batch_t = torch.unsqueeze(img_t, 0)
        with torch.no_grad():
            out = model(batch_t)
        probs = torch.nn.functional.softmax(out, dim=1)[0]
        topk = probs.topk(k)
        indices = topk.indices.cpu().tolist()
        values = topk.values.cpu().tolist()
        res = []
        for idx, p in zip(indices, values):
            label = idx2label[idx] if (0 <= idx < len(idx2label)) else f'label_{idx}'
            res.append({"label": label, "prob": float(p), "idx": int(idx)})
        return res
    except Exception:
        return [{"label": "unknown_food", "prob": 1.0, "idx": -1}]
