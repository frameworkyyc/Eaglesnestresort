# Chapter 3 layout guide (input image 1) and mask (image 4) for Painting 3: a deep, misty spruce forest, scenery only.
# Built only from Painting A's own chapter 3 forest (its spruce silhouettes and misty middle distance, never the moose),
# soft mist fills and the agreed edge colour. Canvas: 729 x 410 reference px at 4 px each = 2916 x 1640 (16:9).
# Run from the repository root.
import os, cv2, numpy as np
P = os.path.dirname(os.path.abspath(__file__)) + '/'
S = 4; W, H = 729, 410; CW, CH = W * S, H * S
bgr = lambda h: np.array([int(h[5:7], 16), int(h[3:5], 16), int(h[1:3], 16)], np.float32)
H34 = bgr('#E3D4C0')
src = cv2.imread('art-masters/things-to-do/cinematic-prototype/work/a3-2560.png').astype(np.float32)   # Painting A rows 430-704
Y = (np.arange(CH, dtype=np.float32) / S)[:, None]; X = (np.arange(CW, dtype=np.float32) / S)[None, :]
ss = lambda e0, e1, v: (lambda t: t * t * (3 - 2 * t))(np.clip((v - e0) / (e1 - e0), 0, 1))
def lay(cv, col, a):
    a = np.asarray(a, np.float32); a = a[..., None] if a.ndim == 2 else a
    return cv * (1 - a) + col * a
def paste(cv, piece, alpha, x, y):
    h, w = piece.shape[:2]; x0, y0 = max(0, x), max(0, y); x1, y1 = min(CW, x + w), min(CH, y + h)
    if x1 <= x0 or y1 <= y0: return cv
    p = piece[y0 - y:y1 - y, x0 - x:x1 - x]; a = alpha[y0 - y:y1 - y, x0 - x:x1 - x][..., None]
    cv[y0:y1, x0:x1] = cv[y0:y1, x0:x1] * (1 - a) + p * a; return cv

# dark spruce silhouettes from Painting A's left stand (never the moose, never the valley's small map trees)
L = cv2.GaussianBlur(cv2.cvtColor(src.astype(np.uint8), cv2.COLOR_BGR2LAB)[..., 0].astype(np.float32), (0, 0), 3) * 100 / 255
dark = (L < 30).astype(np.uint8)
dark = cv2.morphologyEx(dark, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (9, 9)))
inv = (1 - dark).astype(np.uint8); n, lb, st, _ = cv2.connectedComponentsWithStats(inv)
for i in range(1, n):                      # fill mist gaps enclosed inside a stand
    x, y, w, h, a = st[i]
    if a < 9000 and x > 0 and y > 0 and x + w < dark.shape[1] and y + h < dark.shape[0]: dark[lb == i] = 1
stand_box = (0, 0, 640, 800); dark[:240, 450:] = 0; dark[:, 640:] = 0
def stand(x0, x1, scale, mirror=False, fade_rows=60, fade_l=0, fade_r=0):
    piece = src[0:800, x0:x1]; m = dark[0:800, x0:x1].astype(np.float32)
    piece = cv2.resize(piece, None, fx=scale, fy=scale, interpolation=cv2.INTER_CUBIC)
    m = cv2.GaussianBlur(cv2.resize(m, (piece.shape[1], piece.shape[0]), interpolation=cv2.INTER_LINEAR), (0, 0), 1.5)
    if mirror: piece, m = piece[:, ::-1], m[:, ::-1]
    f = np.clip(np.arange(m.shape[0])[::-1] / (fade_rows * S), 0, 1)[:, None]; m = m * (f * f * (3 - 2 * f))   # bases sink into mist
    xs = np.arange(m.shape[1], dtype=np.float32)
    if fade_l: m = m * ss(0, fade_l * S, xs)[None, :]                      # no hard edge where the stand was cut
    if fade_r: m = m * ss(0, fade_r * S, xs[::-1])[None, :]
    return piece, np.clip(m, 0, 1)

# 1) mist: locked top colour, a pale quiet upper half, a cooler grey-green forest atmosphere lower down
cv = np.zeros((CH, CW, 3), np.float32) + H34
cv = lay(cv, bgr('#E6DDCF'), ss(12, 40, Y) * (1 - ss(150, 230, Y)))
cv = lay(cv, bgr('#CDD0C2'), ss(170, 250, Y) * (1 - ss(340, 385, Y)))
# 2) the far forest: Painting A's misty middle distance, made pale and distant, a ghost treeline across the full width
far = cv2.resize(src[300:620, 700:2050], (CW, round(320 * CW / 1350)), interpolation=cv2.INTER_CUBIC)
mist_far = bgr('#DCDCD0'); far = far * 0.38 + mist_far * 0.62
fa = ss(0, 70 * S, np.arange(far.shape[0], dtype=np.float32))[:, None] * np.ones((1, CW), np.float32) * 0.9
cv = paste(cv, far, fa, 0, 112 * S)
# 3) the middle forest: the same misty stands at full strength, lower and nearer
mid = cv2.resize(src[340:860, 700:2050], (CW, round(520 * CW / 1350 * 0.82)), interpolation=cv2.INTER_CUBIC)
ma = ss(0, 40 * S, np.arange(mid.shape[0], dtype=np.float32))[:, None] * np.ones((1, CW), np.float32)
ma *= (1 - ss(mid.shape[0] - 70 * S, mid.shape[0] - 10 * S, np.arange(mid.shape[0], dtype=np.float32)))[:, None]
cv = paste(cv, mid, ma * 0.95, 0, 188 * S)
# 4) quiet upper left and centre: where the heading, paragraph and two photographs sit, only pale far trees show
qa = np.zeros((CH, CW), np.float32); cv2.rectangle(qa, (24 * S, 12 * S), (505 * S, 192 * S), 1, -1)
qa = cv2.GaussianBlur(qa, (0, 0), sigmaX=34 * S, sigmaY=18 * S); qa = qa / qa.max()
cv = lay(cv, bgr('#E4DDD0'), qa * np.where(Y < 150, 0.72, 0.5))
# 5) the near forest: tall spruce rising almost the full height at the right, a narrow stand at the left edge,
#    and a few nearer trees low in the centre-right; their bases sink into the mist
pc, pa = stand(0, 470, 1.95, mirror=True, fade_l=75); cv = paste(cv, pc, pa, CW - pc.shape[1] + 6 * S, 382 * S - pc.shape[0])
pc, pa = stand(0, 175, 1.62, fade_r=38); cv = paste(cv, pc, pa, -6 * S, 384 * S - pc.shape[0])
pc, pa = stand(170, 470, 0.92, fade_rows=40, fade_l=30, fade_r=30); cv = paste(cv, pc, pa, 338 * S, 380 * S - pc.shape[0])
# 6) the forest floor dissolves into a bank of mist: the colour chapter 4 rises out of
cv = lay(cv, H34, ss(338, 392, Y))
# 7) locked bands, exact colour
cv[:12 * S] = H34; cv[390 * S:] = H34
guide = np.clip(cv, 0, 255).astype(np.uint8)
cv2.imwrite(P + 'ch3-image1-layout.png', guide); cv2.imwrite(P + 'ch3-image1-layout.jpg', guide, [cv2.IMWRITE_JPEG_QUALITY, 95])
mask = np.full((CH, CW), 255, np.uint8); mask[:12 * S] = 0; mask[390 * S:] = 0
cv2.imwrite(P + 'ch3-image4-mask.png', mask)
cv2.imwrite(P + 'guide-small.jpg', cv2.resize(guide, (1458, 820), interpolation=cv2.INTER_AREA))
print('guide', guide.shape, 'mask white %.1f%%' % (100 * (mask > 0).mean()))
