"""Lightweight freshness estimator.

This implements a fast, dependency-light heuristic that inspects
color saturation, brightness (value) and edge strength in the image.
It's not a substitute for a trained model, but it gives a per-image
signal instead of always returning the same value.

The function accepts:
- a filesystem path (str)
- a PIL.Image.Image instance
- a numpy array (H,W,3) uint8 or float in [0,1]

Returns: one of 'fresh', 'stale', or 'uncertain'.
"""
from PIL import Image
import numpy as np


def _to_array(img):
    # accept path, PIL Image, or numpy array
    if isinstance(img, str):
        pil = Image.open(img).convert('RGB')
        arr = np.array(pil)
        return arr
    try:
        from PIL import Image as _PILImage
        if isinstance(img, _PILImage.Image):
            return np.array(img.convert('RGB'))
    except Exception:
        pass
    arr = np.asarray(img)
    # if float, scale to 0-255
    if arr.dtype.kind == 'f':
        arr = (arr * 255).clip(0, 255).astype('uint8')
    return arr


def estimate_freshness(image, *, debug=False):
    """Estimate freshness using simple image statistics.

    Heuristics:
    - low saturation and low brightness often indicate wilted / stale produce
    - very low edge strength (blurry / flat) can indicate spoiled or low-detail images
    - otherwise mark as 'fresh'
    """
    try:
        arr = _to_array(image)
    except Exception:
        return 'uncertain'

    if arr is None or arr.size == 0:
        return 'uncertain'

    # normalize to 0..1 floats
    a = arr.astype('float32') / 255.0
    # compute per-pixel max/min -> value and saturation (simple HSV approximation)
    mx = a.max(axis=2)
    mn = a.min(axis=2)
    # avoid divide-by-zero
    sat = np.where(mx > 1e-6, (mx - mn) / mx, 0.0)
    val = mx

    avg_sat = float(np.mean(sat))
    avg_val = float(np.mean(val))

    # simple edge strength: mean abs gradient (x and y)
    gray = 0.299 * a[..., 0] + 0.587 * a[..., 1] + 0.114 * a[..., 2]
    dx = np.abs(gray[:, 1:] - gray[:, :-1])
    dy = np.abs(gray[1:, :] - gray[:-1, :])
    edge = float(np.mean(np.concatenate([dx.ravel(), dy.ravel()]))) if dx.size + dy.size > 0 else 0.0

    if debug:
        print(f"[FRESHNESS] avg_sat={avg_sat:.3f}, avg_val={avg_val:.3f}, edge={edge:.4f}")

    # Tunable thresholds (conservative):
    # - very low saturation (<0.15) and low brightness (<0.45) -> stale
    if avg_sat < 0.15 and avg_val < 0.45:
        return 'stale'

    # - low edge strength + low brightness -> stale (blurry or decomposed)
    if edge < 0.01 and avg_val < 0.5:
        return 'stale'

    # - extremely low brightness -> uncertain
    if avg_val < 0.18:
        return 'uncertain'

    return 'fresh'
