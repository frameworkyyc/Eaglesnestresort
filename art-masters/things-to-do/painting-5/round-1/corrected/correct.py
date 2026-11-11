"""Painting 5: the three approved local touch-ups. Reads the raw master (never written to) and saves painting-5-final.png.

  1. Top edge. Rows 0-67 of the raw are a flat, featureless dark band (#282C38) where the locked cloud band should be.
     They are refilled with the painting's own sky from just below (rows 68-136, mirrored), so the paper grain carries on,
     then a colour-only LAB offset makes the top edge exactly H45 #E4E3DC: full strength on rows 0-68, eased out to
     nothing by row 258 (30 reference px). Below the band nothing painted is replaced.
  2. The tiny upright mark on the tip of the lake's point (about x 3140-3152, y 1562-1587). That short stretch of
     shoreline is rebuilt from the clean columns on either side (x 3136 and x 3156), following the line's own slope
     (0.15 px per px), so the shore runs on unbroken and the snow above and ice below stay as painted.
  3. Bottom edge. A colour-only LAB offset makes the bottom edge exactly H56 #3A4763 (the raw ends at #333B56):
     full strength from row 2610 (303 reference px) down, eased in from row 2240 (260 reference px).

Run from the repository root:  python3 art-masters/things-to-do/painting-5/round-1/corrected/correct.py
"""
import hashlib, os
import numpy as np, cv2
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "..", "painting-5-raw-nano-banana-2-1.png")
OUT = os.path.join(HERE, "painting-5-final.png")
RAW_SHA256 = "b7436672"

sha = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()
assert sha(RAW).startswith(RAW_SHA256), "raw master has changed"
img = np.asarray(Image.open(RAW).convert("RGB")).astype(np.float32)
H, W = img.shape[:2]
assert (H, W) == (2688, 6280)
lab = lambda rgb: cv2.cvtColor((rgb / 255).astype(np.float32), cv2.COLOR_RGB2LAB)
rgb = lambda l: np.clip(cv2.cvtColor(l.astype(np.float32), cv2.COLOR_LAB2RGB) * 255, 0, 255)
target = lambda hexs: lab(np.array([[[int(hexs[i:i + 2], 16) for i in (1, 3, 5)]]], np.float32)).reshape(3)
ease = lambda t: (lambda u: u * u * (3 - 2 * u))(np.clip(t, 0, 1))

# 1. top edge ------------------------------------------------------------------------------------------------
B, END = 68, 258
img[:B] = img[2 * B:B:-1][:B]                       # row y takes the sky from row 136 - y (mirror about row 68)
band = lab(img[:END])
mean0 = cv2.GaussianBlur(band[:8].mean(0, keepdims=True), (0, 0), sigmaX=200, sigmaY=0.1)[0]   # per column, smooth
offset = target("#E4E3DC")[None, :] - mean0          # (W, 3)
w = 1 - ease((np.arange(END) - B) / (END - B))       # 1 on rows 0-68, eased to 0 at row 258
img[:END] = rgb(band + offset[None] * w[:, None, None])

# 2. the mark on the lake's point ---------------------------------------------------------------------------------
XL, XR, SLOPE = 3136, 3156, 0.15
Y0, Y1 = 1554, 1596
ys, xs = np.mgrid[Y0:Y1, XL:XR + 1].astype(np.float32)
t = (xs - XL) / (XR - XL)
left = cv2.remap(img, np.full_like(xs, XL), ys - SLOPE * (xs - XL), cv2.INTER_LINEAR)
right = cv2.remap(img, np.full_like(xs, XR), ys + SLOPE * (XR - xs), cv2.INTER_LINEAR)
patch = left * (1 - t[..., None]) + right * t[..., None]
a = np.ones_like(t)
a *= ease((xs - XL) / 2) * ease((XR - xs) / 2)       # feather the two side edges
a *= ease((ys - Y0) / 3) * ease((Y1 - 1 - ys) / 3)   # and the top and bottom
img[Y0:Y1, XL:XR + 1] = img[Y0:Y1, XL:XR + 1] * (1 - a[..., None]) + patch * a[..., None]

# 3. bottom edge -----------------------------------------------------------------------------------------------
S0, S1 = 2240, 2610
low = lab(img[S0:])
off = target("#3A4763") - low[S1 - S0:].reshape(-1, 3).mean(0)
w = ease((np.arange(S0, H) - S0) / (S1 - S0))
img[S0:] = rgb(low + off[None, None, :] * w[:, None, None])

Image.fromarray(np.round(img).astype(np.uint8), "RGB").save(OUT, optimize=True)
assert sha(RAW).startswith(RAW_SHA256)
print("top offset (mean LAB)", np.round(offset.mean(0), 2), " bottom offset LAB", np.round(off, 2), "->", sha(OUT)[:16])
