"""Paste the combined edit back into Candidate A so nothing outside the edit area changes.
Usage: composite.py EDIT.png OUT.png   (run from this folder)
Strokes the model drew slightly past the mask edge are kept when they clearly differ from Candidate A,
touch the mask, and lie within 60 px of it ("spill"); the sun disc and geese are never touched."""
import sys, cv2, numpy as np
A = cv2.imread('../gen/A-nano-banana-2-1.png')[:, :, :3]; H, W = A.shape[:2]
E = cv2.imread(sys.argv[1])[:, :, :3]
if E.shape[:2] != (H, W): E = cv2.resize(E, (W, H), interpolation=cv2.INTER_LANCZOS4)
m = (cv2.imread('mask-full.png', 0) > 0).astype(np.uint8)
lab = lambda i: cv2.cvtColor(i, cv2.COLOR_BGR2LAB).astype(np.float32)
d = np.linalg.norm(cv2.GaussianBlur(lab(E), (0, 0), 3) - cv2.GaussianBlur(lab(A), (0, 0), 3), axis=2)
band = cv2.dilate(m, np.ones((3, 3), np.uint8), iterations=60) - m
spill = ((d > 28) & (band > 0)).astype(np.uint8)
spill = cv2.morphologyEx(spill, cv2.MORPH_OPEN, np.ones((5, 5), np.uint8))
n, labels = cv2.connectedComponents(cv2.bitwise_or(spill, m))
keep = np.isin(labels, np.unique(labels[m > 0]))
ext = (keep & ((spill > 0) | (m > 0))).astype(np.uint8)
ext = cv2.morphologyEx(ext, cv2.MORPH_CLOSE, np.ones((9, 9), np.uint8))
ext = cv2.dilate(ext, np.ones((3, 3), np.uint8), iterations=3)
# protected: the sun disc and the geese stay exactly as in Candidate A
L = cv2.cvtColor(A, cv2.COLOR_BGR2LAB)[:, :, 0]
prot = np.zeros_like(m); cv2.circle(prot, (int(.5813 * W), int(.3126 * H)), 60, 1, -1)
dark = (L < 150).astype(np.uint8); dark[int(.23 * H):] = 0
nn, lb, st, _ = cv2.connectedComponentsWithStats(dark)
for i in range(1, nn):
    x, y, w, h, a = st[i]
    if a > 3000 and y + h < .215 * H and .55 * W < x and x + w < .84 * W: prot[lb == i] = 1
prot = cv2.dilate(prot, np.ones((13, 13), np.uint8))
ext[prot > 0] = 0
alpha = cv2.GaussianBlur(ext.astype(np.float32), (0, 0), 4); alpha[alpha < 1 / 255] = 0
alpha[prot > 0] = 0
# the hills fade into the morning haze on the left instead of ending at a straight edge
xx = np.arange(W)[None, :].astype(np.float32); yy = np.arange(H)[:, None]
r = np.clip((xx - .405 * W) / (.075 * W), 0, 1); r = r * r * (3 - 2 * r)
alpha = np.where(yy < .56 * H, alpha * r, alpha).astype(np.float32)
alpha[alpha < 1 / 255] = 0
# beyond x = 0.9884 the model's frame has no content (it came back ~1.2% zoomed in): keep A's own trees and rocks in that strip
edge = np.clip((.9884 * W - 4 - xx) / 60, 0, 1); edge = edge * edge * (3 - 2 * edge)
alpha = (alpha * edge).astype(np.float32)
alpha[alpha < 1 / 255] = 0
# keep Candidate A's own far-shore treeline (crisper, golden-lit, and it matches its reflection in the water)
L4 = cv2.cvtColor(cv2.GaussianBlur(A, (0, 0), 4), cv2.COLOR_BGR2LAB)[:, :, 0]
tree = (L4 < 135).astype(np.uint8); tree[:int(.42 * H)] = 0; tree[int(.53 * H):] = 0
nt, lt, stt, _ = cv2.connectedComponentsWithStats(tree)
tl = np.zeros_like(tree)
for i in range(1, nt):
    if stt[i, cv2.CC_STAT_AREA] > 4000 and stt[i, cv2.CC_STAT_TOP] + stt[i, cv2.CC_STAT_HEIGHT] > .50 * H: tl[lt == i] = 1
ttop = np.full(W, int(.52 * H))
for x in range(W):
    ys = np.nonzero(tl[int(.42 * H):int(.53 * H), x])[0]
    if len(ys): ttop[x] = ys[0] + int(.42 * H)
ttop = cv2.erode(ttop.astype(np.float32)[None], np.ones((1, 9), np.uint8))[0]     # bridge single missed columns
keepA = ((tl > 0) | (yy >= ttop[None, :] + 25)) & (yy < .56 * H) & (xx >= .40 * W) & (xx < .645 * W)
keepA = cv2.GaussianBlur(keepA.astype(np.float32), (0, 0), 1.5)
alpha = (alpha * (1 - keepA)).astype(np.float32); alpha[alpha < 1 / 255] = 0
# the lower goose's downstroke wing reaches into the lodge's tree tops: keep the whole bird exactly as in A
g2 = cv2.imread('goose2-mask.png', 0).astype(np.float32) / 255
alpha = (alpha * (1 - cv2.GaussianBlur(g2, (0, 0), 1.2))).astype(np.float32); alpha[g2 > .5] = 0; alpha[alpha < 1 / 255] = 0
a = alpha[..., None]
out = np.clip(A * (1 - a) + E * a, 0, 255).astype(np.uint8)
cv2.imwrite(sys.argv[2], out)
cv2.imwrite(sys.argv[2].replace('.png', '-alpha.png'), (alpha * 255).astype(np.uint8))
print('paste area %.2f%% (mask %.2f%%); spill added %.2f%%' % ((alpha > 0).mean() * 100, m.mean() * 100, ((ext > 0) & (m == 0)).mean() * 100))
