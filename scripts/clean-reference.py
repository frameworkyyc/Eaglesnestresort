"""Build the text-free composition input for the hero from the approved reference.
Usage: python3 scripts/clean-reference.py [reference.jpg] [out.png]  (defaults: src/ttd/reference.jpg -> art-masters/inputs/hero-reference-clean.png, 729x312, 21:9)
No generative tools: classical image processing only."""
import cv2, numpy as np
rng = np.random.default_rng(11)
import sys, os
REF = sys.argv[1] if len(sys.argv) > 1 else 'src/ttd/reference.jpg'
OUT = sys.argv[2] if len(sys.argv) > 2 else 'art-masters/inputs/hero-reference-clean.png'
ref = cv2.imread(REF)
if ref is None: sys.exit(f'cannot read {REF}')
hero = ref[62:286, :].astype(np.float32)            # below the nav, above the chapter 1 badge
hero[0:4, 10:110] = hero[5:6, 10:110]                # the reference logo's lower edge (ref rows 56-61) bleeds into rows 62-65
H0, W = hero.shape[:2]

def paper_grain(h, w, amp):
    """Structureless paper tooth: two octaves of smoothed noise, no tiling, no edges."""
    g = cv2.GaussianBlur(rng.normal(0, 1, (h, w)).astype(np.float32), (0, 0), .7) * .7 \
        + cv2.GaussianBlur(rng.normal(0, 1, (h, w)).astype(np.float32), (0, 0), 1.8) * .5
    g = g / g.std() * amp
    return np.repeat(g[..., None], 3, 2)

# grain strength measured on clean sky at the far left of the reference
hp = hero[2:60, 2:34] - cv2.GaussianBlur(hero[2:60, 2:34], (0, 0), 2)
AMP = float(hp.std()) * .9

# ---- 1. text blocks, measured on the reference (hero-crop pixels: x0, y0, x1, y1) ----
boxes = [(88, 19, 210, 37),    # eyebrow
         (40, 37, 234, 80),    # headline, line 1
         (40, 79, 319, 123),   # headline, line 2
         (40, 121, 287, 175)]  # intro paragraph, three lines (joined to the headline: no untreated rows between)
mask = np.zeros((H0, W), np.float32)
for x0, y0, x1, y1 in boxes: mask[y0:y1 + 1, x0:x1 + 1] = 1
mask[37:176, 0:40] = 1     # the narrow strip left of the text joins the fill, so no edge is left at x=40

# ---- 2. fill: per row, interpolate between the clean colours just outside the text area.
#         The boundary colours are smoothed down the rows first, so rows don't streak. ----
Lc = np.zeros((H0, 3), np.float32); Rc = np.zeros((H0, 3), np.float32); span = np.zeros((H0, 2), int)
for y in range(H0):
    xs = np.where(mask[y] > 0)[0]
    if not len(xs): continue
    x0, x1 = xs.min(), xs.max(); span[y] = (x0, x1)
    Lc[y] = hero[y, 0:6].mean(0) if x0 == 0 else hero[y, max(0, x0 - 6):max(1, x0 - 1)].mean(0)
    Rc[y] = hero[y, x1 + 2:x1 + 8].mean(0)
rows = np.where(mask.sum(1) > 0)[0]
Lc[rows] = cv2.GaussianBlur(Lc[rows][:, None, :], (1, 0), sigmaX=.1, sigmaY=2.2)[:, 0, :]
Rc[rows] = cv2.GaussianBlur(Rc[rows][:, None, :], (1, 0), sigmaX=.1, sigmaY=2.2)[:, 0, :]
fill = hero.copy()
for y in rows:
    x0, x1 = span[y]; t = np.linspace(0, 1, x1 - x0 + 1)[:, None]
    t = t * t * (3 - 2 * t)                          # smoothstep: no visible gradient kinks
    fill[y, x0:x1 + 1] = Lc[y] * (1 - t) + Rc[y] * t
fill = cv2.GaussianBlur(fill, (0, 0), sigmaX=2.5, sigmaY=1.2)
fill = fill + paper_grain(H0, W, AMP)
soft = cv2.GaussianBlur(cv2.dilate(mask, np.ones((5, 5), np.uint8)), (0, 0), 2.5)
ramp = np.clip((np.arange(W) - 4) / 34, 0, 1)   # full strength by x=38, before any glyph (first glyph at x=46); ramp = ramp * ramp * (3 - 2 * ramp)
soft[37:176, :40] = np.minimum(soft[37:176, :40], ramp[:40])   # far-left ridges fade gradually into the haze
soft = cv2.GaussianBlur(soft, (0, 0), 1.5)[..., None]
out = hero * (1 - soft) + fill * soft

# ---- 3. torn-paper ridges along the bottom -> lake water ----
lum = cv2.cvtColor(np.clip(out, 0, 255).astype(np.uint8), cv2.COLOR_BGR2GRAY)
paper = (lum > 168).astype(np.uint8); ridge = np.zeros((H0, W), np.uint8)
for xs, ys in ((slice(0, 215), slice(170, H0)), (slice(585, W), slice(180, H0))):
    n, lab = cv2.connectedComponents(paper[ys, xs])
    for k in range(1, n):
        if (lab[-1] == k).any(): ridge[ys, xs][lab == k] = 1
ridge = cv2.dilate(ridge, np.ones((5, 5), np.uint8), iterations=2)
src = out.copy()
for y in range(H0):
    xs = np.where(ridge[y])[0]
    if not len(xs): continue
    left = xs[xs < W // 2]; right = xs[xs >= W // 2]
    if len(left):                                     # reflect the open water beside the ridge (x 175-235)
        b = left.max() + 1
        for x in left: out[y, x] = src[y, min(W - 1, b + (b - x) % 56)]
    if len(right):
        b = right.min() - 1
        for x in right: out[y, x] = src[y, max(0, b - (x - b) % 56)]
rm = cv2.GaussianBlur(ridge.astype(np.float32), (0, 0), 1.6)[..., None]
out = out * (1 - rm) + cv2.GaussianBlur(out, (0, 0), 1.0) * rm

# ---- 4. extend the lake 88 rows down to 21:9, from water only (dock and boat excluded) ----
H = round(W * 9 / 21); ext = H - H0
band = out[H0 - 30:H0].copy()
objects = np.zeros(W, bool); objects[232:392] = True  # dock + boat columns
col = band.mean(0)                                    # per-column water colour (keeps the sun path)
xs = np.arange(W); good = ~objects
for c in range(3): col[objects, c] = np.interp(xs[objects], xs[good], col[good, c])
col = cv2.GaussianBlur(col[None], (0, 0), sigmaX=3, sigmaY=.1)[0]
streak = cv2.GaussianBlur(rng.normal(0, 1, (ext + 20, W)).astype(np.float32), (0, 0), sigmaX=14, sigmaY=.7)[10:-10]
streak = streak / streak.std() * 5.5
lower = np.zeros((ext, W, 3), np.float32)
for y in range(ext):
    lower[y] = col * (1 - .1 * y / ext) + streak[y][:, None]
lower += paper_grain(ext, W, AMP * .8)
full = np.concatenate([out, lower], 0)
full[H0 - 4:H0 + 4] = cv2.GaussianBlur(full[H0 - 8:H0 + 8], (0, 0), sigmaX=.5, sigmaY=2)[4:12]
full = np.clip(full, 0, 255).astype(np.uint8)
cv2.imwrite(OUT, full)
print('wrote', OUT, full.shape, 'grain amp', round(AMP, 2))
