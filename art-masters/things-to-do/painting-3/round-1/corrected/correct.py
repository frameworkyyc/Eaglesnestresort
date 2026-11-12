"""Painting 3: the two approved local touch-ups. Reads the raw master (never written to) and saves painting-3-final.png.

  1. The top band. Rows 0-75 of the raw are the locked mist band (#E4D3C0), darker than the painting's own parchment
     sky, and two spruce crowns are cut flat against it. The band is replaced with the painting's own sky, and E rows of
     the same sky are added above, so the two trees have room to finish. The sky is the painting's clean sky texture
     (rows 100-700, x 1000-4200), mirrored to fill the width and the height, toned per column to the sky just below
     the band. With E = 876 the canvas becomes 6336 x 3564, 16:9.
  2. The two clipped treetops are finished from the painting itself:
     - The tallest spruce (A, trunk at x 4983) was cut through a tier about 570 px wide, so its natural top is far
       above. Its crown continues upward as a stack of its own crown (rows 76-252, ending in the gap between two tiers; its dark ink inside its own spruce
       outline, so the pale trees beside it are left out) at 0.9, 0.75, 0.6, 0.48 and 0.38
       scale, so the tiers grow smaller toward the top as a spruce's do, and ends in the apex of the grey-green spruce
       whose tip is at x 5621, at 0.62 scale, toned to A's ink. Only shrinking is used, so the engraving stays crisp.
       Each section's outermost branch ends near its top are trimmed into a spruce taper where the next section takes
       over, and so are A's own sliced branch ends at the old cut.
     - The far-right spruce (B, spine at x 6010) gets the apex of the spruce whose tip is at x 4516, at 0.74 scale.
     Only each source tree's own ink is taken (the ink connected to its spine), and every piece is aligned on the
     receiving tree's trunk and faded into the crown below it.

Run from the repository root:  python3 art-masters/things-to-do/painting-3/round-1/corrected/correct.py
"""
import hashlib, os
import numpy as np, cv2
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, '..', 'painting-3-raw-nano-banana-2-1.png')
OUT = os.path.join(HERE, 'painting-3-final.png')
RAW_SHA256 = 'a45e2f79'
BAND = 75                      # last row of the locked band in the raw
E = 3564 - 2688                # rows of sky added above: 876, which makes the canvas 16:9

sha = lambda p: hashlib.sha256(open(p, 'rb').read()).hexdigest()
assert sha(RAW).startswith(RAW_SHA256), 'raw master has changed'
raw = np.asarray(Image.open(RAW).convert('RGB')).astype(np.float32)
H, W = raw.shape[:2]; assert (H, W) == (2688, 6336)
lab = lambda x: cv2.cvtColor((x / 255).astype(np.float32), cv2.COLOR_RGB2LAB)
rgb = lambda x: np.clip(cv2.cvtColor(x.astype(np.float32), cv2.COLOR_LAB2RGB) * 255, 0, 255)
ease = lambda t: (lambda u: u * u * (3 - 2 * u))(np.clip(t, 0, 1))
Lr = lab(raw)[..., 0]

# ---- 1. sky ---------------------------------------------------------------------------------------------------------
NS = E + BAND + 90                                       # sky rows: the new rows, the band, and the trim/blend zone
p = raw[100:700, 1000:4200]
p = np.concatenate([p, p[::-1]], 0); p = np.concatenate([p] * (NS // p.shape[0] + 1), 0)[:NS]
p = np.concatenate([p, p[:, ::-1]], 1)
sky = np.concatenate([p] * (W // p.shape[1] + 1), 1)[:, :W].copy()
ref = raw[BAND + 14:BAND + 40]; refL = lab(ref)[..., 0]
clean = (refL > 86).mean(0) > 0.97                       # columns of pure sky just below the band
col = np.median(ref, 0); xs = np.arange(W)
for c in range(3): col[:, c] = np.interp(xs, xs[clean], col[clean, c])
col = cv2.GaussianBlur(col[None], (0, 0), sigmaX=120, sigmaY=0.1)[0]
pm = cv2.GaussianBlur(sky.mean(0)[None], (0, 0), sigmaX=120, sigmaY=0.1)[0]
sky = sky - pm[None] + col[None]

out = np.zeros((H + E, W, 3), np.float32)
out[E:] = raw
out[:E + BAND + 31] = sky[:E + BAND + 31]
treeish = cv2.GaussianBlur((Lr[:BAND + 31] < 84).astype(np.float32), (0, 0), 1.2)
w = np.zeros((BAND + 31, 1), np.float32); w[BAND + 1:] = ease((np.arange(BAND + 1, BAND + 31) - (BAND + 12)) / 18.0)[:, None]
keep_raw = np.maximum(w, treeish * (np.arange(BAND + 31)[:, None] > BAND))
out[E:E + BAND + 31] = sky[E:E + BAND + 31] * (1 - keep_raw[..., None]) + raw[:BAND + 31] * keep_raw[..., None]

# ---- 2. treetops -------------------------------------------------------------------------------------------------------
def own_ink(box, spine, dark=None):
    """A source tree's own ink (connected to its spine) as colour and alpha, from the raw. With dark=L, only ink
    darker than lightness L counts (tree A's crown is dark; the pale trees standing beside it are left out)."""
    x0, y0, x1, y1 = box; piece = raw[y0:y1, x0:x1]
    s = np.median(raw[y0:y0 + 20, x0:x0 + 30].reshape(-1, 3), 0) if y0 > BAND + 10 else np.median(raw[BAND + 20:BAND + 40, 1000:1400].reshape(-1, 3), 0)
    sL = lab(s[None, None])[0, 0, 0]; Lp = lab(piece)[..., 0]
    a = np.clip((sL - Lp - 3) / 9, 0, 1) if dark is None else np.clip((dark - Lp) / 8, 0, 1)
    a = cv2.GaussianBlur(a, (0, 0), 0.8)
    n, lb, _, _ = cv2.connectedComponentsWithStats((a > 0.35).astype(np.uint8))
    sx = spine - x0; ids = set(lb[:, max(0, sx - 6):sx + 7].ravel().tolist()) - {0}
    keep = cv2.dilate(np.isin(lb, list(ids)).astype(np.uint8), np.ones((5, 5), np.uint8)).astype(np.float32)
    return piece.copy(), a * cv2.GaussianBlur(keep, (0, 0), 1.0)

def tone_to(piece, a, tone_box):
    tl = lab(raw[tone_box[1]:tone_box[3], tone_box[0]:tone_box[2]]); tm = tl[..., 0] < 75
    pl = lab(piece); pm = a > 0.6; mp = pl.copy()
    mp[..., 0] = (pl[..., 0] - pl[..., 0][pm].mean()) / (pl[..., 0][pm].std() + 1e-6) * tl[..., 0][tm].std() + tl[..., 0][tm].mean()
    for c in (1, 2): mp[..., c] = pl[..., c] - pl[..., c][pm].mean() + tl[..., c][tm].mean()
    m = ease((a - 0.25) / 0.6)[..., None]
    return rgb(pl * (1 - m) + mp * m)

def half_width(a, rows, side=max):
    """Half-width of the ink about the centre column, for the given rows (its wider side, or with side=min the narrower)."""
    c = a.shape[1] // 2; hw = []
    for r in rows:
        idx = np.where(a[r] > 0.4)[0]; hw.append(side(c - idx.min(), idx.max() - c) if len(idx) else 0)
    return np.array(hw, np.float32)

def taper(a, top_hw, T):
    """Trim the ink in the top T rows to a spruce taper: half-width top_hw at the top, the full width at row T."""
    h, w = a.shape; c = w / 2; full = max(half_width(a, [min(T, h - 1)])[0], top_hw + 1)
    rows = np.arange(min(T, h))
    hw = top_hw + (full - top_hw) * (rows / T)
    rng = np.random.default_rng(7); hw = hw + cv2.GaussianBlur(rng.normal(0, 6, len(rows)).astype(np.float32)[None], (0, 0), 3)[0]
    xs = np.abs(np.arange(w)[None, :] + 0.5 - c)
    a[:len(rows)] *= np.clip((hw[:, None] - xs) / 4 + 0.5, 0, 1)
    return a

def place(piece, a, spine_x, bottom_row, fade):
    """Composite a piece whose centre column is its spine, its bottom at bottom_row, its base faded over fade rows."""
    h, w = a.shape; ya = bottom_row - h; xa = int(round(spine_x - w / 2))
    assert ya >= 40, 'not enough sky above'
    a = a * (1 - ease((np.arange(h)[:, None] - (h - fade)) / fade))
    out[ya:bottom_row, xa:xa + w] = out[ya:bottom_row, xa:xa + w] * (1 - a[..., None]) + piece * a[..., None]
    return ya

def centred(box, spine):
    x0, y0, x1, y1 = box; r = max(spine - x0, x1 - spine); return (spine - r, y0, spine + r, y1)

def scaled(piece, a, s, mirror=False):
    if mirror: piece, a = piece[:, ::-1], a[:, ::-1]
    sz = (max(2, round(piece.shape[1] * s)), max(2, round(piece.shape[0] * s)))
    return cv2.resize(piece, sz, interpolation=cv2.INTER_AREA), np.clip(cv2.resize(a, sz, interpolation=cv2.INTER_AREA), 0, 1)

# tree A: its own crown, stacked smaller and smaller, then a native-size apex
A_SPINE, cut = 4983, E + BAND
crownA, aA = own_ink((A_SPINE - 305, BAND + 1, A_SPINE + 305, 253), A_SPINE, dark=76)   # ends in the gap between tiers at row 252
# only A's own crown: inside its spruce outline (the pale trees beside it are outside)
_r = np.arange(aA.shape[0])[:, None]; _x = np.abs(np.arange(aA.shape[1])[None, :] + 0.5 - aA.shape[1] / 2)
aA *= np.clip(((285 + 0.18 * _r) - _x) / 8 + 0.5, 0, 1)
apex, aApex = own_ink(centred((5500, 236, 5742, 620), 5621), 5621)
apex = tone_to(apex, aApex, (4780, 90, 5200, 300))
stack = [(0.9, False, 60), (0.75, False, 50), (0.6, False, 42), (0.48, False, 36), (0.38, False, 30)]
apexS, aApexS = scaled(apex, aApex, 0.62)
sections = [scaled(crownA, aA, s, m) + (ov,) for s, m, ov in stack] + [(apexS, aApexS, 34)]
# trim A's own sliced branch ends at the old cut to the first section's base width
hw0 = half_width(sections[0][1], [sections[0][1].shape[0] - 1])[0]
zone = out[cut:cut + 70].copy(); zx0 = int(A_SPINE - 340)
xsz = np.abs(np.arange(680) + 0.5 - 340)[None, :]
hwz = hw0 * 0.95 + (300 - hw0 * 0.95) * (np.arange(70)[:, None] / 70)
keepA = np.clip((hwz - xsz) / 6 + 0.5, 0, 1)
inkA = (lab(out[cut:cut + 70, zx0:zx0 + 680])[..., 0] < 84).astype(np.float32)
rep = (1 - keepA) * cv2.GaussianBlur(inkA, (0, 0), 1.5)
out[cut:cut + 70, zx0:zx0 + 680] = out[cut:cut + 70, zx0:zx0 + 680] * (1 - rep[..., None]) + sky[cut:cut + 70, zx0:zx0 + 680] * rep[..., None]
bottom = cut
for i, (pc, a, ov) in enumerate(sections):
    if i + 1 < len(sections):                           # taper this section's top to the next section's base
        nxt = sections[i + 1][1]
        base = np.median(half_width(nxt, range(nxt.shape[0] - 30, nxt.shape[0] - 5), side=min))
        a = taper(a.copy(), base * 0.85, max(40, a.shape[0] // 3))
    top = place(pc, a, A_SPINE, bottom + ov, 16)       # its base overlaps the crown below by ov rows
    bottom = top
apex_top_A = bottom

# tree B: one apex, scaled to its narrow top
B_SPINE = 6010
pB, aB = own_ink(centred((4430, 395, 4602, 610), 4516), 4516)
pB = tone_to(pB, aB, (5940, 90, 6070, 260))
pB, aB = scaled(pB, aB, 0.74)
apex_top_B = place(pB, aB, B_SPINE, cut + 34, 34)

Image.fromarray(np.round(out).astype(np.uint8), 'RGB').save(OUT, optimize=True)
assert sha(RAW).startswith(RAW_SHA256)
print('final', W, 'x', H + E, '| A tip at row', apex_top_A, '| B tip at row', apex_top_B, '->', sha(OUT)[:16])
