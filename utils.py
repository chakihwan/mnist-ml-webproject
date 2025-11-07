import numpy as np
from PIL import Image, ImageOps

def preprocess_image(file_obj):
    img = Image.open(file_obj).convert("L") # 그레이스케일
    img = ImageOps.invert(img)
    img = ImageOps.pad(img, (28, 28), method=Image.BILINEAR, color=255, centering=(0.5, 0.5))
    arr = np.array(img).astype("float32") / 255.0
    arr = arr.reshape(1, 28, 28, 1)
    return arr

def _to_probs(vec):
    """vec가 이미 확률(합≈1, [0,1])이면 그대로, 아니면 softmax 적용"""
    a = np.asarray(vec, dtype=np.float32)
    if a.min() >= 0.0 and a.max() <= 1.0 and np.isclose(a.sum(), 1.0, atol=1e-3):
        p = a
    else:
        a = a - np.max(a)
        ea = np.exp(a)
        p = ea / np.sum(ea)
    return p


def postprocess(pred):
    """
    pred: (10,) 형태. 확률 또는 로짓.
    반환: digit, prob(최대확률), probs(길이 10 리스트)
    """
    probs = _to_probs(pred)
    cls = int(np.argmax(probs))
    prob = float(probs[cls])
    return {"digit": cls, "prob": prob, "probs": probs.tolist()}