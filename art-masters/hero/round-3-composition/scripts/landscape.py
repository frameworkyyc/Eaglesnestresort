"""Landscape layout guide (no generation): Candidate A's alpine peaks become a low, hazy distant range,
with two bands of rolling forested hills in front, built from A's own drawing."""
import json, sys
import cv2, numpy as np

P = json.load(open(sys.argv[1]))
A = cv2.imread('../../gen/A-nano-banana-2-1.png')[:, :, :3]
H, W = A.shape[:2]
f32 = lambda i: i.astype(np.float32)
LAB = lambda i: cv2.cvtColor(np.clip(i, 0, 255).astype(np.uint8), cv2.COLOR_BGR2LAB).astype(np.float32)
BGR = lambda l: cv2.cvtColor(np.clip(l, 0, 255).astype(np.uint8), cv2.COLOR_LAB2BGR)
X = lambda v: int(round(v * W)); Y = lambda v: int(round(v * H))
L4 = cv2.cvtColor(cv2.GaussianBlur(A, (0, 0), 4), cv2.COLOR_BGR2LAB)[:, :, 0]
xa, xb = X(P['x_range'][0]), X(P['x_range'][1])

# 1. old mountains: below the mountain/sky line, above the far-shore treeline
mt = (L4 < P['sky_thr']).astype(np.uint8); mt[:Y(.18)] = 0; mt[Y(.53):] = 0
_n, _lab, _st, _ = cv2.connectedComponentsWithStats(mt)       # keep only the mountain mass, not cloud outlines or geese
_keep = np.zeros_like(mt)
for i in range(1, _n):
    if _st[i, cv2.CC_STAT_TOP] + _st[i, cv2.CC_STAT_HEIGHT] >= Y(.44) and _st[i, cv2.CC_STAT_AREA] > 20000: _keep[_lab == i] = 1
mt = _keep
# bright snow faces sit inside the ink outlines: anything the sky cannot reach is mountain
mc = cv2.morphologyEx(mt, cv2.MORPH_CLOSE, np.ones((P['close_px'], P['close_px']), np.uint8))
reach = (1 - mc).astype(np.uint8); reach[:Y(.18)] = 1
ff = np.zeros((H + 2, W + 2), np.uint8)
cv2.floodFill(reach, ff, (5, 5), 2)
mt = ((reach != 2) & (np.arange(H)[:, None] >= Y(.18)) & (np.arange(H)[:, None] < Y(.53))).astype(np.uint8)
top = np.full(W, Y(.50)); 
for x in range(xa, xb):
    ys = np.nonzero(mt[Y(.18):Y(.50), x])[0]
    if len(ys): top[x] = ys[0] + Y(.18)
sx0, sx1 = X(P['sun_gap'][0]), X(P['sun_gap'][1])          # the sun's glare hides the ridge: bridge it
top[sx0:sx1] = np.linspace(top[sx0 - 1], top[sx1], sx1 - sx0).astype(int)
top = cv2.GaussianBlur(top.astype(np.float32)[None], (0, 0), 2)[0].astype(int) - P['ridge_margin']
env = cv2.erode(top.astype(np.float32)[None], np.ones((1, P['env_win']), np.uint8))[0]   # above every nearby peak
top_s = cv2.GaussianBlur(env[None], (0, 0), P['env_win'] / 4)[0].astype(int) - P['mirror_gap']
tree = (L4 < P['tree_thr']).astype(np.uint8); tree[:Y(.42)] = 0; tree[Y(.53):] = 0
n, lab, st, _ = cv2.connectedComponentsWithStats(tree)
keep = np.zeros_like(tree)
for i in range(1, n):
    if st[i, cv2.CC_STAT_AREA] > 4000 and st[i, cv2.CC_STAT_TOP] + st[i, cv2.CC_STAT_HEIGHT] > Y(.50): keep[lab == i] = 1
ttop = np.full(W, Y(.52))
for x in range(W):
    ys = np.nonzero(keep[Y(.42):Y(.53), x])[0]
    if len(ys): ttop[x] = ys[0] + Y(.42)
yy, xx = np.mgrid[0:H, 0:W]
xs = X(P['split_x'])
old = ((yy >= top[None, :] - 4) & (xx >= xa) & (xx < xs) & (yy < Y(.52))).astype(np.uint8)
lab4 = cv2.cvtColor(cv2.GaussianBlur(A, (0, 0), 4), cv2.COLOR_BGR2LAB).astype(np.float32)
chroma = np.hypot(lab4[..., 1] - 128, lab4[..., 2] - 128)
mp = ((lab4[..., 0] >= 112) & (lab4[..., 0] < P['sky_thr']) & (chroma < P['mtn_chroma']) & (yy >= np.where(xx > X(.90), Y(.02), Y(.20))) & (yy < Y(.50))
      & (xx >= xs) & (xx < xb)).astype(np.uint8)
mp = cv2.morphologyEx(mp, cv2.MORPH_CLOSE, np.ones((9, 9), np.uint8))
mp = cv2.morphologyEx(mp, cv2.MORPH_OPEN, np.ones((7, 7), np.uint8))
old |= mp
for poly in P.get('extra_old', []):                    # bright snow the threshold cannot see
    cv2.fillPoly(old, [np.array([[X(px), Y(py)] for px, py in poly], np.int32)], 1)
old = cv2.dilate(old, np.ones((P["dil_px"], P["dil_px"]), np.uint8))
trees = cv2.dilate((L4 < P['tree_dark']).astype(np.uint8), np.ones((P['tree_guard'], P['tree_guard']), np.uint8))
old[(trees > 0) & (xx >= xs)] = 0                     # never eat into A's own spruces and aspens
sx, sy = P["sun"]
sun = np.zeros_like(old); cv2.circle(sun, (X(sx), Y(sy)), int(P['sun_disc_px']), 1, -1)
old &= (1 - sun); old &= (keep == 0); old[:, :xa] = 0; old[:, xb:] = 0

# 2. sky where the peaks were: the hazy sky of the same rows on the left, plus the sun's glow
ref = LAB(A)[:, X(P['sky_ref'][0]):X(P['sky_ref'][1])]
rowc = np.median(ref, axis=1)                                   # H x 3
det = f32(A) - cv2.GaussianBlur(f32(A), (0, 0), 6)               # paper grain and faint strokes
detl = det[:, X(P['sky_ref'][0]):X(P['sky_ref'][1])]
reps = int(np.ceil(W / detl.shape[1])) + 1
detf = np.tile(np.concatenate([detl, detl[:, ::-1]], 1), (1, reps, 1))[:, :W]
sky = np.repeat(rowc[:, None, :], W, 1)
sx, sy = P['sun']; d2 = ((xx - X(sx)) / W) ** 2 + ((yy - Y(sy)) / W) ** 2
g = np.exp(-d2 / (2 * P['glow_sigma'] ** 2))[..., None]
sky = sky * (1 - g * P['glow_amt']) + np.array(P['glow_lab'], np.float32) * g * P['glow_amt']
skyb = f32(BGR(sky)) + detf * .8
src_y = np.clip(2 * top_s[None, :] - yy, Y(.03), H - 1)
refl = f32(A)[src_y, xx]
srcL = L4[src_y, xx]
dark = (srcL < P['bird_thr']).astype(np.uint8)                # geese: never mirrored into the sky
dark = cv2.dilate(dark, np.ones((25, 25), np.uint8)).astype(np.float32)
dark = cv2.GaussianBlur(dark, (0, 0), 6)[..., None]
refl = refl * (1 - dark) + skyb * dark
ds = np.sqrt(((xx - X(sx)) / W) ** 2 + ((src_y - Y(sy)) / W) ** 2)
sunw = np.clip(1 - (ds - P['sun_r']) / P['sun_r'], 0, 1)[..., None]   # 1 inside the disc's halo
refl = refl * (1 - sunw) + skyb * sunw
skyb = refl * (1 - g * P['glow_amt'] * .6) + skyb * g * P['glow_amt'] * .6

def haze_to(img_bgr, amt):
    return f32(img_bgr) * (1 - amt) + skyb * amt

fade = np.clip((xx - xa) / max(X(P['fade_left']), 1), 0, 1); fade = fade * fade * (3 - 2 * fade)
# make the borrowed sky continuous with the real sky at the edge of the old peaks (Poisson, at 1/4 size)
ys_, xs_ = np.nonzero(old); bx0, bx1, by0, by1 = max(xs_.min() - 40, 0), min(xs_.max() + 40, W), max(ys_.min() - 40, 0), min(ys_.max() + 40, H)
q = 4; sw, sh = (bx1 - bx0) // q, (by1 - by0) // q
srcs = cv2.resize(np.clip(skyb[by0:by1, bx0:bx1], 0, 255).astype(np.uint8), (sw, sh), interpolation=cv2.INTER_AREA)
realsky = (yy < top[None, :]) & (old == 0) & (L4 >= P['bird_thr'])           # only true sky may steer the blend
for (cx, cy, rr) in P.get('src_holes', []):
    realsky &= ((xx - X(cx)) ** 2 + (yy - Y(cy)) ** 2) > (rr * W) ** 2
dstf = np.where(realsky[..., None], f32(A), skyb)
dsts = cv2.resize(np.clip(dstf[by0:by1, bx0:bx1], 0, 255).astype(np.uint8), (sw, sh), interpolation=cv2.INTER_AREA)
ms = cv2.resize(old[by0:by1, bx0:bx1] * 255, (sw, sh), interpolation=cv2.INTER_NEAREST)
ms = cv2.dilate(ms, np.ones((3, 3), np.uint8)); ms[:2] = 0; ms[-2:] = 0; ms[:, :2] = 0; ms[:, -2:] = 0
rx, ry, rw, rh = cv2.boundingRect(ms)
cl = cv2.seamlessClone(srcs, dsts, ms, (rx + rw // 2, ry + rh // 2), cv2.NORMAL_CLONE)
corr = cv2.GaussianBlur(cl.astype(np.float32) - srcs.astype(np.float32), (0, 0), 2)
corr = cv2.resize(corr, (bx1 - bx0, by1 - by0), interpolation=cv2.INTER_CUBIC)
skyb[by0:by1, bx0:bx1] += corr
G = f32(A).copy()
fo = np.clip((xx - xa) / max(X(P['fade_old']), 1), 0, 1)
o = (old * fo)[..., None].astype(np.float32)
G = G * (1 - o) + skyb * o

# 3. the distant range: A's own peaks, flattened and pushed back
s0, s1 = P['mtn_src_y']; d0, d1 = P['mtn_dst_y']; k = (d1 - d0) / (s1 - s0)
M = np.float32([[1, 0, 0], [0, k, Y(d1) - Y(s1) * k]])
mtn = cv2.warpAffine(A, M, (W, H), flags=cv2.INTER_AREA)
srcm = (mt * (yy < Y(.475)) * (yy >= Y(P['mtn_src_y'][0])) * (xx < xs)).astype(np.float32)
for (cx, cy, rr) in P.get('src_holes', []):          # the sun and its glare are not mountain
    cv2.circle(srcm, (X(cx), Y(cy)), int(rr * W), 0, -1)
ma = cv2.warpAffine(srcm, M, (W, H))
mtn[:, xs:xb] = mtn[:, 2 * xs - xb:xs][:, ::-1][:, :xb - xs]   # mirror the range behind the lodge
ma[:, xs:xb] = ma[:, 2 * xs - xb:xs][:, ::-1][:, :xb - xs]
ma *= ((xx >= xa) & (xx < xb))
ma = (cv2.GaussianBlur(ma, (0, 0), 1.5) * fade)[..., None]
G = G * (1 - ma) + haze_to(mtn, P['mtn_haze']) * ma

# 4. rolling forested hills from A's far-shore treeline
tx0, tx1 = X(P['tex_x'][0]), X(P['tex_x'][1]); ty0, ty1 = Y(.435), Y(.515)
tex = A[ty0:ty1, tx0:tx1]; ta = keep[ty0:ty1, tx0:tx1].astype(np.float32)
tex = np.concatenate([tex, tex[:, ::-1]], 1); ta = np.concatenate([ta, ta[:, ::-1]], 1)
def ridge(base, amp, seed):
    r = np.random.RandomState(seed); x = np.arange(W) / W
    y = sum(a * np.sin(2 * np.pi * x / wl + r.uniform(0, 6.28)) for a, wl in zip(amp, P['wavelengths']))
    return Y(base) + (y * H).astype(int)
for layer in P['hills']:
    s = layer['scale']; t = cv2.resize(tex, None, fx=s, fy=s, interpolation=cv2.INTER_AREA)
    a = cv2.resize(ta, None, fx=s, fy=s, interpolation=cv2.INTER_AREA)
    th, tw = t.shape[:2]
    r = ridge(layer['base'], layer['amp'], layer['seed'])
    canvas = np.zeros((H, W, 3), np.float32); alpha = np.zeros((H, W), np.float32)
    for row in range(layer['rows']):                       # rows of tree tops stepping down the hillside
        off = int(row * th * .45); shift = (row * 137) % tw
        for x in range(xa, xb):
            y0 = r[x] + off; c = (x + shift) % tw
            y1 = min(y0 + th, H)
            if y1 <= y0: continue
            aa = a[:y1 - y0, c]
            canvas[y0:y1, x] = canvas[y0:y1, x] * (1 - aa[:, None]) + t[:y1 - y0, c] * aa[:, None]
            alpha[y0:y1, x] = np.maximum(alpha[y0:y1, x], aa)
        # everything below the second row is solid forest
    fill = (yy >= (r[None, :] + int(th * .8))) & (xx >= xa) & (xx < xb)
    alpha[fill] = np.maximum(alpha[fill], 1)
    canvas[fill & (alpha > 0) & (canvas.sum(2) == 0)] = f32(cv2.resize(tex, (1, 1)))[0, 0]
    alpha *= fade
    al = alpha[..., None]
    G = G * (1 - al) + haze_to(canvas, layer['haze']) * al

# 5. A's own far-shore treeline and everything below it stay exactly as drawn
k3 = keep.astype(np.float32)[..., None]
below = (yy >= ttop[None, :] + 6)[..., None].astype(np.float32)
keepA = np.maximum(k3, below) * ((xx >= xa) & (xx < xb))[..., None] + ((xx < xa) | (xx >= xb))[..., None]
G = G * (1 - keepA) + f32(A) * keepA
G = np.clip(G, 0, 255).astype(np.uint8)
cv2.imwrite(P['out'], G)

# edit area for the landscape: from above the old peaks down to the treeline tips
newtop = Y(P['mtn_dst_y'][0]) - Y(.02)
em = cv2.dilate(old, np.ones((41, 41), np.uint8)) | ((yy >= newtop) & (yy <= ttop[None, :] + 20) & (xx >= xa) & (xx < xs)).astype(np.uint8)
em = (em * (fo > 0)).astype(np.uint8)
cv2.imwrite(P['out'].replace('.png', '-mask.png'), em * 255)
print('old peaks top min y %.3f; treeline top median y %.3f' % (top[xa:xb].min() / H, np.median(ttop[xa:xb]) / H))
