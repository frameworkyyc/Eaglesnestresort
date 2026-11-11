"""Painting 4: the two approved local touch-ups. Reads the raw master (never written to) and saves painting-4-final.png.

  1. Top mist: a colour-only grade, so the top edge is exactly the chapter 3 handoff colour H34 #E3D4C0.
     It is one LAB offset (target minus the measured top band), full strength on rows 0-16, then eased out to
     nothing by row 200 (8% of the height). An offset adds no blur, so every line and the paper grain stay as painted.
  2. The looped ornament ("knot") on the tip of the rock spike at about x 1745-1792, y 1612-1642 is removed. The spike's
     own two edges, measured on rows 1648-1664 and extended, meet at (1775, ~1638), so the spike now ends in its own
     tip. The knot's area is refilled with the clean parchment sky from 64 rows above, tone-matched and feathered.

Run from the repository root:  python3 art-masters/things-to-do/painting-4/round-1/corrected/correct.py
"""
import hashlib, os
import numpy as np, cv2
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "..", "painting-4-raw-nano-banana-2-1.png")
OUT = os.path.join(HERE, "painting-4-final.png")
RAW_SHA256 = "0925d095"  # prefix of the raw master's checksum, checked before and after

def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()

assert sha(RAW).startswith(RAW_SHA256), "raw master has changed"
rgba = np.asarray(Image.open(RAW))
assert rgba.shape == (2432, 6912, 4) and (rgba[..., 3] == 255).all()  # alpha carries nothing; output is RGB
img = rgba[..., :3].astype(np.float32)

# 1. top mist grade -----------------------------------------------------------------------------------------
TARGET = np.array([0xE3, 0xD4, 0xC0], np.float32)
FULL, END = 16, 200
lab = lambda rgb: cv2.cvtColor((rgb / 255).astype(np.float32), cv2.COLOR_RGB2LAB)
band = img[:END]
measured = lab(img[0:8].reshape(1, -1, 3)).reshape(-1, 3).mean(0)
target = lab(TARGET.reshape(1, 1, 3)).reshape(3)
offset = target - measured
y = np.arange(END, dtype=np.float32)
t = np.clip((y - FULL) / (END - FULL), 0, 1)
w = 1 - t * t * (3 - 2 * t)  # 1 on rows 0-16, smoothstep down to 0 at row 200
graded = lab(band) + offset[None, None, :] * w[:, None, None]
img[:END] = np.clip(cv2.cvtColor(graded.astype(np.float32), cv2.COLOR_LAB2RGB) * 255, 0, 255)

# 2. knot removal --------------------------------------------------------------------------------------------
X0, X1, Y0, Y1 = 1730, 1810, 1596, 1648  # working box
SHIFT = 64                                # sky source: same columns, 64 rows up (clean, std < 1)
yy, xx = np.mgrid[Y0:Y1, X0:X1].astype(np.float32)
# the spike's edges, measured: left x = 1765 - 1.25 (y - 1648), right x = 1782 + 0.875 (y - 1648);
# plus 1 px for the outline's antialiasing, so the spike tapers to a point at about y 1639
left = 1765 - 1.25 * (yy - 1648) - 1
right = 1782 + 0.875 * (yy - 1648) + 1
inside = np.minimum(xx - left, right - xx)              # > 0 inside the spike, in px
keep = np.clip(inside + 0.5, 0, 1)                       # soft (1 px) rock coverage
remove = (1 - keep) * (yy < 1646)                        # everything else in the box, above the spike's flanks
remove = cv2.GaussianBlur(remove.astype(np.float32), (0, 0), 0.8)
remove[:, :2] *= 0; remove[:, -2:] *= 0; remove[:2] *= 0  # nothing reaches the box edge
patch = img[Y0 - SHIFT:Y1 - SHIFT, X0:X1].copy()
ring = (remove < 0.01) & (keep < 0.01)                   # untouched sky inside the box
patch += (img[Y0:Y1, X0:X1][ring].mean(0) - patch[ring].mean(0))  # match tone (well under 1 level)
a = remove[..., None]
img[Y0:Y1, X0:X1] = img[Y0:Y1, X0:X1] * (1 - a) + patch * a
# the new tip (above row 1646) is solid outline ink, like the spike's flanks just below
flank = img[1656:1672, 1786:1800].reshape(-1, 3)
ink = flank[flank.mean(1) < 60].mean(0)
tip = (keep * np.clip((1646 - yy) / 2, 0, 1))[..., None]
img[Y0:Y1, X0:X1] = img[Y0:Y1, X0:X1] * (1 - tip) + np.minimum(img[Y0:Y1, X0:X1], ink) * tip

Image.fromarray(np.round(img).astype(np.uint8), "RGB").save(OUT, optimize=True)
assert sha(RAW).startswith(RAW_SHA256)
print("offset LAB", np.round(offset, 2), "->", OUT, sha(OUT)[:16])
