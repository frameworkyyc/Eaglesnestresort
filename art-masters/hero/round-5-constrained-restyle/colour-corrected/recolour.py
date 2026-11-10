"""Colour-only correction of Round 5 (no generation): restore Round 3's foliage colour.
Lightness (LAB L*) of every pixel is kept exactly, so the engraving, linework, textures, architecture and
composition cannot change. Only the colour (a*, b*) of vegetation moves toward Round 3's local colour.
Usage: recolour.py OUT.png [strength]"""
import sys, cv2, numpy as np
R0 = cv2.imread('../r5/restyle-raw.png'); B3 = cv2.imread('r3-in-r5-frame.png'); H, W = R0.shape[:2]
k = float(sys.argv[2]) if len(sys.argv) > 2 else 1.0
lab = lambda i: cv2.cvtColor(i.astype(np.float32) / 255, cv2.COLOR_BGR2LAB)
L5, L3 = lab(R0), lab(B3)
yy, xx = np.mgrid[0:H, 0:W].astype(np.float32) / np.array([H, W], np.float32)[:, None, None]
g = lambda a, s: cv2.GaussianBlur(a, (0, 0), s)
a3, b3 = g(L3[..., 1], 6), g(L3[..., 2], 6)
# where vegetation can be: the lodge's woods down to the shore rocks, and the far-shore forest band
shore = .60 + .06 * np.clip((xx - .62) / .38, 0, 1)                      # top of the shore rocks, sloping down to the right
zone = ((xx > .615) & (yy < shore)) | ((xx > .33) & (xx <= .615) & (yy > .405) & (yy < .525))
# vegetation in Round 3 reads olive/green (low a*); timber and roofs read orange-brown (high a*)
bldg = np.zeros((H, W), np.uint8)                                      # the lodge itself: roofs, gable, wings
cv2.fillPoly(bldg, [np.array([[x * W, y * H] for x, y in [(.650, .445), (.700, .405), (.745, .365), (.795, .240), (.845, .315),
                                                          (.905, .315), (.955, .330), (.955, .575), (.650, .585)]], np.int32)], 1)
thr = np.where(bldg > 0, 2.5, 6.0)                                      # over the building only clearly green trees count
veg = zone & (a3 < thr) & (L5[..., 0] < 72)                              # bright glass and sky are left alone
veg &= cv2.imread('geese-r5.png', 0) == 0                               # never the geese
veg &= ~((bldg > 0) & (g(L3[..., 0], 3) > 52))                          # diamond windows and glass
veg &= ~((L3[..., 0] > 70) & (np.hypot(a3, b3) < 8))                    # Round 3's pale glass reflections
veg = cv2.morphologyEx(veg.astype(np.uint8), cv2.MORPH_OPEN, np.ones((5, 5), np.uint8))
veg = cv2.morphologyEx(veg, cv2.MORPH_CLOSE, np.ones((9, 9), np.uint8)).astype(np.float32)
w = np.clip(g(veg, 3), 0, 1) * k
# local mean colour of the vegetation in each round (normalised blur, so timber and sky never mix in)
def local_mean(c, m, s=28): return g(c * m, s) / np.maximum(g(m, s), 1e-3)
out = L5.copy()
for ch in (1, 2):
    shift = local_mean(L3[..., ch], veg) - local_mean(L5[..., ch], veg)
    out[..., ch] = L5[..., ch] + w * shift
res = np.clip(cv2.cvtColor(out, cv2.COLOR_LAB2BGR) * 255 + .5, 0, 255).astype(np.uint8)
res[w <= 1e-3] = R0[w <= 1e-3]                                          # untouched pixels stay byte-identical
cv2.imwrite(sys.argv[1], res)
cv2.imwrite(sys.argv[1].replace('.png', '-mask.png'), (np.clip(w / max(k, 1e-6), 0, 1) * 255).astype(np.uint8))
Lr = lab(res)[..., 0]
print('changed pixels %.1f%%; max lightness change %.2f L* (mean %.3f) - rounding only' % ((np.abs(res.astype(int) - R0.astype(int)).sum(2) > 0).mean() * 100,
      np.abs(Lr - L5[..., 0]).max(), np.abs(Lr - L5[..., 0]).mean()))
