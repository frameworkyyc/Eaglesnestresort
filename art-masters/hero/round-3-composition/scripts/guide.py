"""Layout guide for the lodge, built only from the client's illustration and Candidate A (no generation).
Places the illustration's lodge, its tree screen and the bank in front into Candidate A at an agreed
position and scale, tone-matched to A's sunrise palette."""
import json, sys
import cv2, numpy as np

P = json.load(open(sys.argv[1]))          # layout parameters
A = cv2.imread(P.get('base', '../../gen/A-nano-banana-2-1.png'))[:, :, :3]
A0 = cv2.imread('../../gen/A-nano-banana-2-1.png')[:, :, :3]
I = cv2.imread('../ref-illustration.png')[:, :, :3]
H, W = A.shape[:2]
s = P['scale']                             # hero px per illustration px
ax, ay = P['anchor_ill']                   # gable centre at the base of the glass, illustration px
hx, hy = P['anchor_hero'][0] * W, P['anchor_hero'][1] * H
x0, y0, x1, y1 = P['cut_ill']

# 1. silhouette of everything in front of the mountains: dense ink (trees, building, bank)
L = cv2.cvtColor(cv2.GaussianBlur(I, (0, 0), 5), cv2.COLOR_BGR2LAB)[:, :, 0]
fg = (L < P['dark']).astype(np.uint8)
fg = cv2.morphologyEx(fg, cv2.MORPH_OPEN, np.ones((5, 5), np.uint8))
fg = cv2.morphologyEx(fg, cv2.MORPH_CLOSE, np.ones((5, 5), np.uint8))
box = np.zeros_like(fg); box[y0:y1, x0:x1] = fg[y0:y1, x0:x1]
box[y1 - 3:y1, x0:x1] = 1                    # the bank runs off the bottom of the cut
n, lab_, st, _ = cv2.connectedComponentsWithStats(box)
big = np.argmax(st[1:, cv2.CC_STAT_AREA]) + 1   # the forest and lodge are one connected mass
box = (lab_ == big).astype(np.uint8)
bg = np.zeros((box.shape[0] + 2, box.shape[1] + 2), np.uint8)
inv = (1 - box).astype(np.uint8)
inv[:y0] = 1                                 # everything above the cut is background
cv2.floodFill(inv, bg, (x0 + 1, 0), 2)       # sky and mountains: background reachable from the top
sil = (inv != 2).astype(np.uint8)
sil[:, :x0] = 0; sil[:, x1:] = 0; sil[:y0] = 0; sil[y1:] = 0
for poly in P.get('cut_out_ill', []):        # parts not wanted (the tall tree that would block the mountains)
    cv2.fillPoly(sil, [np.array(poly, np.int32)], 0)
# 2. place it in hero space
M = np.float32([[s, 0, hx - ax * s], [0, s, hy - ay * s]])
T = cv2.warpAffine(I, M, (W, H), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REFLECT)
S = cv2.warpAffine(sil.astype(np.float32), M, (W, H), flags=cv2.INTER_LINEAR)
# soft edges: narrow at the tree tops, wide along the bottom and left cut lines
S = cv2.GaussianBlur(S, (0, 0), 3)
yy, xx = np.mgrid[0:H, 0:W]
bot = hy + (y1 - ay) * s; left = hx + (x0 - ax) * s
S *= np.clip((bot - yy) / P['feather_bottom'], 0, 1) * np.clip((xx - left) / P['feather_left'], 0, 1)

# 3. tone-match the transplant to Candidate A's lodge area (Reinhard, in LAB)
def lab(i): return cv2.cvtColor(i, cv2.COLOR_BGR2LAB).astype(np.float32)
rx0, ry0, rx1, ry1 = [int(v * d) for v, d in zip(P['tone_ref'], (W, H, W, H))]
ref = lab(A0)[ry0:ry1, rx0:rx1].reshape(-1, 3)
Tl = lab(T); m = S > 0.5
src = Tl[m]
k = np.array(P['tone_strength'], np.float32)
mu_s, sd_s, mu_r, sd_r = src.mean(0), src.std(0), ref.mean(0), ref.std(0)
Tl = (Tl - mu_s) * (1 - k + k * sd_r / sd_s) + mu_s + k * (mu_r - mu_s)
T = cv2.cvtColor(np.clip(Tl, 0, 255).astype(np.uint8), cv2.COLOR_LAB2BGR)

a = S[..., None]
G = np.clip(A * (1 - a) + T * a, 0, 255).astype(np.uint8)
for (px0, py0, px1, py1, dx) in P.get('clone', []):      # copy A's own background over old-house bits
    X0, Y0, X1, Y1, D = int(px0 * W), int(py0 * H), int(px1 * W), int(py1 * H), int(dx * W)
    patch = G[Y0:Y1, X0 + D:X1 + D].astype(np.float32)
    wgt = np.zeros((Y1 - Y0, X1 - X0), np.float32); wgt[8:-8, 8:-8] = 1
    wgt = cv2.GaussianBlur(wgt, (0, 0), 5)[..., None]
    G[Y0:Y1, X0:X1] = np.clip(G[Y0:Y1, X0:X1] * (1 - wgt) + patch * wgt, 0, 255).astype(np.uint8)
cv2.imwrite(P['out'], G)
cv2.imwrite(P['out'].replace('.png', '-alpha.png'), (S * 255).astype(np.uint8))
print('building in hero x %.3f-%.3f, glass base y %.3f, apex y %.3f' % (
    (hx + (P['bldg_ill'][0] - ax) * s) / W, (hx + (P['bldg_ill'][1] - ax) * s) / W, hy / H,
    (hy + (P['apex_ill'] - ay) * s) / H))
