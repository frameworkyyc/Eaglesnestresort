"""Depth layers cut from the approved chapter paintings, for the cinematic full-screen chapters. No generation.

Each painting is cut into four layers that recombine into the exact painting at rest:
  back   sky (with a soft transparent top, so it can rise out of the chapter before it)
  peaks  the far ranges: everything below a sky/ridge seam
  mid    the middle distance: everything below a ridgeline seam
  front  near trees / rock: 2D cutouts of local ink contrast inside guide boxes, joined to a soft ground band
Seams are dynamic-programming paths that snap to the painting's own edges inside a band around a hand guide line
(guides.json). Hidden areas behind each layer get a soft mist fill, seen only while the layers move apart.

Run from the repository root:  python3 art-masters/things-to-do/cinematic-prototype/cut-layers.py a1 a2 a3 p4 p5
(a1-a3 are Painting A's bands for chapters 1-3; p4, p5 the approved paintings 4 and 5)
Reads the approved finals in art-masters/, writes work/ (full PNG layers and review sheets, not committed) and
prototype/layers/ (the WebP files the prototype loads).
"""
import sys, os, json, numpy as np, cv2
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__))
W = HERE + '/'
FINALS = {'p4': 'art-masters/things-to-do/painting-4/round-1/corrected/painting-4-final.png',
          'p5': 'art-masters/things-to-do/painting-5/round-1/corrected/painting-5-final.png'}

PAINTING_A = 'art-masters/things-to-do/painting-a/round-1/painting-a-raw-nano-banana-2-1.png'
A_BANDS = {'a1': (-25, 250), 'a2': (228, 530), 'a3': (430, 704)}   # page rows (reference px; 0 = the hero's foot)

def source(name):
    """The approved painting (or Painting A's band for a chapter) at 2560 px wide, the working size for cutting."""
    os.makedirs(W + 'work', exist_ok=True)
    if name in A_BANDS:
        r0, r1 = A_BANDS[name]; k = 2560 / 729       # Painting A: 729 x 729 reference px, page rows -25..704
        a = Image.open(PAINTING_A).convert('RGB').resize((2560, 2560), Image.LANCZOS)
        a.crop((0, round((r0 + 25) * k), 2560, round((r1 + 25) * k))).save(W + f'work/{name}-2560.png')
        return
    im = Image.open(FINALS[name]).convert('RGB')
    im.resize((2560, round(2560 * im.height / im.width)), Image.LANCZOS).save(W + f'work/{name}-2560.png')

def export(name):
    """WebP layers for the prototype, at 2560 and 1440 px wide."""
    os.makedirs(W + 'prototype/layers', exist_ok=True)
    for nm in ('back', 'peaks', 'mid', 'front'):
        im = Image.open(W + f'work/{name}-{nm}.png').convert('RGBA')
        if nm == 'back':
            a = np.asarray(im).copy(); H = a.shape[0]; t = np.clip(np.arange(H) / (0.16 * H), 0, 1); t = t * t * (3 - 2 * t)
            a[..., 3] = (a[..., 3] * t[:, None]).astype(np.uint8); im = Image.fromarray(a)
        for w in (2560, 1440):
            r = im if w == im.width else im.resize((w, round(w * im.height / im.width)), Image.LANCZOS)
            r.save(W + f'prototype/layers/{name}-{nm}-{w}.webp', 'WEBP', quality=80, method=6)

def boxmean(a, r0, r1, up):
    """Mean of rows [y-r1, y-r0] (up) or [y+r0, y+r1] (down) for every y, per column."""
    H = a.shape[0]; c = np.concatenate([np.zeros((1,) + a.shape[1:], a.dtype), np.cumsum(a, 0)], 0)
    y = np.arange(H)
    if up: lo, hi = np.clip(y - r1, 0, H), np.clip(y - r0 + 1, 0, H)
    else:  lo, hi = np.clip(y + r0, 0, H), np.clip(y + r1 + 1, 0, H)
    n = np.maximum(hi - lo, 1).reshape((-1,) + (1,) * (a.ndim - 1))
    return (c[hi] - c[lo]) / n

def seam(lab, guide, band, beta):
    H, Wd = lab.shape[:2]
    gx = np.interp(np.arange(Wd), [p[0] for p in guide], [p[1] for p in guide])
    bx = np.interp(np.arange(Wd), [p[0] for p in guide], [p[2] if len(p) > 2 else band for p in guide])
    up, dn = boxmean(lab, 2, 16, True), boxmean(lab, 2, 16, False)
    d = up - dn; diff = np.sqrt((d ** 2).sum(-1)) + np.maximum(d[..., 0], 0) * 0.5   # lighter above scores extra
    diff /= np.percentile(diff, 99.5) + 1e-6
    off = np.arange(-band, band + 1); n = off.size
    cost = np.empty((Wd, n), np.float32); arg = np.zeros((Wd, n), np.int32)
    ys0 = np.clip(np.round(gx[0] + off).astype(int), 0, H - 1)
    cost[0] = -diff[ys0, 0] + np.where(np.abs(off) > bx[0], 1e6, 0)
    J = np.arange(n)
    for x in range(1, Wd):
        ys = np.clip(np.round(gx[x] + off).astype(int), 0, H - 1)
        yprev = np.clip(np.round(gx[x - 1] + off).astype(int), 0, H - 1)
        trans = cost[x - 1][None, :] + beta * np.abs(ys[:, None] - yprev[None, :])   # (new, old)
        a = np.argmin(trans, 1); arg[x] = a
        cost[x] = trans[J, a] - diff[ys, x] + 0.15 * np.abs(off) / band + np.where(np.abs(off) > bx[x], 1e6, 0)
    path = np.zeros(Wd, int); j = int(np.argmin(cost[-1]))
    for x in range(Wd - 1, -1, -1): path[x] = j; j = arg[x, j]
    return np.array([np.clip(gx[x] + off[path[x]], 0, H - 1) for x in range(Wd)], np.float32)

def seam_sky(img, guide, band, beta):
    # sky is smooth and pale; ranges are hatched. Cost: texture below minus texture above, plus luminance drop.
    L = cv2.cvtColor(img.astype(np.uint8), cv2.COLOR_BGR2LAB)[..., 0].astype(np.float32)
    mu = cv2.GaussianBlur(L, (0, 0), 2); tex = np.sqrt(np.maximum(cv2.GaussianBlur(L * L, (0, 0), 2) - mu * mu, 0))
    t3 = np.dstack([tex, mu * 0.15, np.zeros_like(mu)])
    return seam(t3, guide, band, beta)

def below(y, H, feather):
    ys = np.arange(H, dtype=np.float32)[:, None]
    return np.clip((ys - y[None, :]) / feather[None, :] + 0.5, 0, 1)

def ramp(H, Wd, y0, y1):
    t = np.clip((np.arange(H, dtype=np.float32) - y0) / (y1 - y0), 0, 1); t = t * t * (3 - 2 * t)
    return np.repeat(t[:, None], Wd, 1)

def cutout(img, boxes, thr, exclude=()):
    L = cv2.cvtColor(img.astype(np.uint8), cv2.COLOR_BGR2LAB)[..., 0].astype(np.float32)
    mu = cv2.GaussianBlur(L, (0, 0), 5); sd = np.sqrt(np.maximum(cv2.GaussianBlur(L * L, (0, 0), 5) - mu * mu, 0))
    score = sd / 40 + cv2.GaussianBlur((L < 110).astype(np.float32), (0, 0), 5) * 1.5
    m = np.zeros(L.shape, np.uint8)
    for box in boxes:
        x0, y0, x1, y1 = box[:4]; envelope = len(box) > 4 and box[4] == 'envelope'
        sc = score.copy()
        for ex in exclude:
            if isinstance(ex[0], list): cv2.fillPoly(sc, [np.array(ex, np.int32)], 0)   # polygon
            else: sc[ex[1]:ex[3], ex[0]:ex[2]] = 0
        sub = (sc[y0:y1, x0:x1] > thr).astype(np.uint8)
        sub = cv2.morphologyEx(sub, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
        sub = cv2.morphologyEx(sub, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (13, 13)))
        n, lab, st, _ = cv2.connectedComponentsWithStats(sub)
        keep = np.zeros_like(sub)
        for i in range(1, n):
            if st[i, cv2.CC_STAT_AREA] > 2500: keep[lab == i] = 1
        # fill enclosed holes (snow clumps inside a tree)
        ff = np.pad(keep, 1); h, w = ff.shape; mm = np.zeros((h + 2, w + 2), np.uint8)
        cv2.floodFill(ff, mm, (0, 0), 1)          # from the padded corner: always outside every tree
        keep = keep | (1 - ff[1:-1, 1:-1])
        if envelope:   # a grounded solid (rock): everything below its own silhouette inside the box
            has = keep.any(0); top = np.where(has, keep.argmax(0), keep.shape[0])
            top = cv2.morphologyEx(top.astype(np.float32).reshape(1, -1), cv2.MORPH_CLOSE, np.ones((1, 9), np.float32)).ravel()
            keep = (np.arange(keep.shape[0])[:, None] >= top[None, :]).astype(np.uint8)
        m[y0:y1, x0:x1] = np.maximum(m[y0:y1, x0:x1], keep)
    m = cv2.erode(m, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5)))   # the score is blurred: pull back to the ink
    return cv2.GaussianBlur(m.astype(np.float32), (0, 0), 1.2)

def cutout_parts(img, parts):
    """Silhouettes by tone instead of ink density, for dense painting where every box is full of ink:
    'dark' keeps the darkest shapes (near trees against mist), 'tint' keeps one warm-coloured shape (the moose)."""
    lab = cv2.cvtColor(img.astype(np.uint8), cv2.COLOR_BGR2LAB).astype(np.float32)
    L = cv2.GaussianBlur(lab[..., 0], (0, 0), 3) * 100 / 255; bb = cv2.GaussianBlur(lab[..., 2], (0, 0), 3) - 128
    m = np.zeros(L.shape, np.uint8)
    for p in parts:
        x0, y0, x1, y1 = p['box']
        if p['mode'] == 'grabcut':          # one distinct object inside a rectangle (the moose)
            rx0, ry0, rx1, ry1 = p['rect']; gm = np.zeros((y1 - y0, x1 - x0), np.uint8)
            bg, fg = np.zeros((1, 65), np.float64), np.zeros((1, 65), np.float64)
            cv2.grabCut(img[y0:y1, x0:x1].astype(np.uint8), gm, (rx0 - x0, ry0 - y0, rx1 - rx0, ry1 - ry0), bg, fg, 8, cv2.GC_INIT_WITH_RECT)
            sub = ((gm == cv2.GC_FGD) | (gm == cv2.GC_PR_FGD)).astype(np.uint8)
        else:
            sub = (L[y0:y1, x0:x1] < p['thr']) if p['mode'] == 'dark' else (bb[y0:y1, x0:x1] > p['thr'])
        sub = cv2.morphologyEx(sub.astype(np.uint8), cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (p.get('close', 9),) * 2))
        n, lb, st, _ = cv2.connectedComponentsWithStats(sub)
        keep = np.zeros_like(sub)
        if p.get('largest') and n > 1: keep[lb == 1 + int(np.argmax(st[1:, cv2.CC_STAT_AREA]))] = 1
        else:
            for i in range(1, n):
                if st[i, cv2.CC_STAT_AREA] > p.get('min_area', 1500): keep[lb == i] = 1
        # fill enclosed holes smaller than a few trees' worth (mist gaps inside a dense stand)
        inv = (1 - keep).astype(np.uint8); n2, lb2, st2, _ = cv2.connectedComponentsWithStats(inv)
        for i in range(1, n2):
            x, y, w, h, a = st2[i]
            if a < p.get('hole', 6000) and x > 0 and y > 0 and x + w < keep.shape[1] and y + h < keep.shape[0]: keep[lb2 == i] = 1
        m[y0:y1, x0:x1] = np.maximum(m[y0:y1, x0:x1], keep)
    m = cv2.erode(m, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3)))
    return cv2.GaussianBlur(m.astype(np.float32), (0, 0), 1.2)

def pushpull(img, valid):
    levels = []; a = img * valid[..., None]; w = valid.astype(np.float32)
    while min(w.shape) > 4:
        levels.append((a, w)); a = cv2.pyrDown(a); w = cv2.pyrDown(w)
    out = a / np.maximum(w, 1e-6)[..., None]
    for a, w in reversed(levels):
        up = cv2.resize(out, (w.shape[1], w.shape[0]), interpolation=cv2.INTER_LINEAR)
        cur = a / np.maximum(w, 1e-6)[..., None]; t = np.clip(w * 4, 0, 1)[..., None]
        out = cur * t + up * (1 - t)
    return out

def build(name, s):
    img = cv2.imread(W + f'work/{name}-2560.png').astype(np.float32); H, Wd = img.shape[:2]
    lab = cv2.cvtColor(cv2.GaussianBlur(img, (0, 0), 2).astype(np.uint8), cv2.COLOR_BGR2LAB).astype(np.float32)
    b1 = seam(lab, s['b1']['pts'], s['b1']['band'], s['b1']['beta'])
    b1 = cv2.GaussianBlur(b1.reshape(1, -1), (0, 0), s['b1'].get('smooth', 1.0)).ravel()
    fe = np.full(Wd, 1.6, np.float32)
    for (x0, x1, f) in s['b1'].get('soft', []): fe[x0:x1] = f
    fe = cv2.GaussianBlur(fe.reshape(1, -1), (0, 0), 20).ravel()
    a_mid = below(b1, H, fe)
    b0 = seam_sky(img, s['b0']['pts'], s['b0']['band'], s['b0']['beta'])
    b0 = cv2.GaussianBlur(b0.reshape(1, -1), (0, 0), 1.2).ravel(); b0 = np.minimum(b0, b1 - 2)
    a_peaks = below(b0, H, np.full(Wd, 1.4, np.float32))
    a_front = np.maximum(cutout(img, s['front']['boxes'], s['front']['thr'], s['front'].get('exclude', [])), ramp(H, Wd, *s['front']['ground']))
    alphas = [np.ones((H, Wd), np.float32), a_peaks, a_mid, a_front]
    layers = []
    for i in range(4):
        core = [cv2.erode((alphas[j] > 0.99).astype(np.uint8), np.ones((5, 5), np.uint8)) for j in range(i + 1, 4)]
        cov = np.maximum.reduce(core).astype(np.float32) if core else np.zeros((H, Wd), np.float32)
        vis = (alphas[i] > 0.5) & (cov < 0.5)
        fill = cv2.GaussianBlur(pushpull(img, vis), (0, 0), 22)
        # deeper into the hidden area the haze settles to the painting's own mist colour
        dist = cv2.distanceTransform((cov > 0.5).astype(np.uint8), cv2.DIST_L2, 5)
        t = np.clip(dist / 40, 0, 1); t = (t * t * (3 - 2 * t))[..., None]
        mist = np.array(s['mist'][::-1], np.float32)   # RGB in the spec, BGR here
        fill = fill * (1 - t) + mist * t
        layers.append(img * (1 - cov[..., None]) + fill * cov[..., None])
    comp = layers[0]
    for i in (1, 2, 3): comp = layers[i] * alphas[i][..., None] + comp * (1 - alphas[i][..., None])
    print(name, 'recombined at rest: max error', round(float(np.abs(comp - img).max()), 2))
    for i, nm in enumerate(('back', 'peaks', 'mid', 'front')):
        rgba = np.dstack([np.clip(layers[i], 0, 255).astype(np.uint8), np.clip(alphas[i] * 255, 0, 255).astype(np.uint8)])
        cv2.imwrite(W + f'work/{name}-{nm}.png', rgba)
    # review: each layer on a checkerboard, plus the seam
    def checker(rgba):
        h, w = rgba.shape[:2]; c = ((np.indices((h, w)).sum(0) // 24) % 2 * 40 + 200).astype(np.float32)[..., None]
        a = rgba[..., 3:4] / 255.0; return (rgba[..., :3] * a + c * (1 - a)).astype(np.uint8)
    tiles = [checker(cv2.imread(W + f'work/{name}-{nm}.png', cv2.IMREAD_UNCHANGED)) for nm in ('back', 'peaks', 'mid', 'front')]
    ov = img.astype(np.uint8).copy(); cv2.polylines(ov, [np.stack([np.arange(Wd), b1], 1).astype(np.int32)], False, (0, 140, 255), 2, cv2.LINE_AA)
    cv2.polylines(ov, [np.stack([np.arange(Wd), b0], 1).astype(np.int32)], False, (255, 60, 200), 2, cv2.LINE_AA)
    sheet = np.vstack([cv2.resize(t, (1200, round(1200 * H / Wd)), interpolation=cv2.INTER_AREA) for t in [ov] + tiles])
    cv2.imwrite(W + f'work/{name}-layers.jpg', sheet, [cv2.IMWRITE_JPEG_QUALITY, 86])
    json.dump({'b1': [round(float(v), 1) for v in b1]}, open(W + f'work/{name}-b1.json', 'w'))

def build_general(name, s):
    """Layers listed back to front. Each layer's alpha is 'full', 'below' or 'above' a seam, or a 'cutout'
    (optionally joined to a ground band). A band that starts with a 'below' layer has no full back layer:
    above that seam it is transparent, and the stage's own sky colour shows (chapter 3)."""
    img = cv2.imread(W + f'work/{name}-2560.png').astype(np.float32); H, Wd = img.shape[:2]
    lab = cv2.cvtColor(cv2.GaussianBlur(img, (0, 0), 2).astype(np.uint8), cv2.COLOR_BGR2LAB).astype(np.float32)
    seams = {}
    def get_seam(key):
        if key not in seams:
            g = s['seams'][key]
            y = seam_sky(img, g['pts'], g['band'], g['beta']) if g.get('texture') else seam(lab, g['pts'], g['band'], g['beta'])
            seams[key] = cv2.GaussianBlur(y.reshape(1, -1), (0, 0), g.get('smooth', 1.0)).ravel()
        return seams[key]
    names, alphas = [], []
    for L in s['layers']:
        t = L['type']
        if t == 'full': a = np.ones((H, Wd), np.float32)
        elif t in ('below', 'above'):
            a = below(get_seam(L['seam']), H, np.full(Wd, L.get('feather', 1.6), np.float32))
            if t == 'above': a = 1 - a
        else:
            a = cutout_parts(img, L['parts']) if 'parts' in L else cutout(img, L['boxes'], L['thr'], L.get('exclude', []))
            if L.get('ground'): a = np.maximum(a, ramp(H, Wd, *L['ground']))
            if L.get('clip'):      # never above the band's own soft top (chapter 3's forest line)
                a = a * below(get_seam(L['clip']) - L.get('clip_lift', 0), H, np.full(Wd, L.get('clip_feather', 30), np.float32))
        names.append(L['name']); alphas.append(a.astype(np.float32))
    mist = np.array(s['mist'][::-1], np.float32)
    layers = []
    for i in range(len(alphas)):
        core = [cv2.erode((alphas[j] > 0.99).astype(np.uint8), np.ones((5, 5), np.uint8)) for j in range(i + 1, len(alphas))]
        cov = np.maximum.reduce(core).astype(np.float32) if core else np.zeros((H, Wd), np.float32)
        vis = (alphas[i] > 0.5) & (cov < 0.5)
        fill = cv2.GaussianBlur(pushpull(img, vis), (0, 0), 22)
        dist = cv2.distanceTransform((cov > 0.5).astype(np.uint8), cv2.DIST_L2, 5)
        tt = np.clip(dist / 40, 0, 1); tt = (tt * tt * (3 - 2 * tt))[..., None]
        fill = fill * (1 - tt) + mist * tt
        layers.append(img * (1 - cov[..., None]) + fill * cov[..., None])
    comp = img.copy()                          # where no layer covers, the stage sky shows instead (not compared)
    for i in range(len(layers)): comp = layers[i] * alphas[i][..., None] + comp * (1 - alphas[i][..., None])
    covered = np.maximum.reduce(alphas) > 0.99
    print(name, 'recombined at rest: max error', round(float(np.abs(comp - img)[covered].max()), 2),
          '| layers', names)
    def checker(rgba):
        h, w = rgba.shape[:2]; c = ((np.indices((h, w)).sum(0) // 24) % 2 * 40 + 200).astype(np.float32)[..., None]
        a = rgba[..., 3:4] / 255.0; return (rgba[..., :3] * a + c * (1 - a)).astype(np.uint8)
    tiles = []
    for i, nm in enumerate(names):
        rgba = np.dstack([np.clip(layers[i], 0, 255).astype(np.uint8), np.clip(alphas[i] * 255, 0, 255).astype(np.uint8)])
        cv2.imwrite(W + f'work/{name}-{nm}.png', rgba); tiles.append(checker(rgba))
    ov = img.astype(np.uint8).copy()
    for key, col in zip(seams, ((255, 60, 200), (0, 140, 255), (40, 200, 40))):
        cv2.polylines(ov, [np.stack([np.arange(Wd), seams[key]], 1).astype(np.int32)], False, col, 2, cv2.LINE_AA)
    sheet = np.vstack([cv2.resize(t, (1200, round(1200 * H / Wd)), interpolation=cv2.INTER_AREA) for t in [ov] + tiles])
    cv2.imwrite(W + f'work/{name}-layers.jpg', sheet, [cv2.IMWRITE_JPEG_QUALITY, 86])
    return names

def export_general(name, names, soft_top=()):
    os.makedirs(W + 'prototype/layers', exist_ok=True)
    for nm in names:
        im = Image.open(W + f'work/{name}-{nm}.png').convert('RGBA')
        if nm in soft_top:
            a = np.asarray(im).copy(); H = a.shape[0]; t = np.clip(np.arange(H) / (0.16 * H), 0, 1); t = t * t * (3 - 2 * t)
            a[..., 3] = (a[..., 3] * t[:, None]).astype(np.uint8); im = Image.fromarray(a)
        for w in (2560, 1440):
            r = im if w == im.width else im.resize((w, round(w * im.height / im.width)), Image.LANCZOS)
            r.save(W + f'prototype/layers/{name}-{nm}-{w}.webp', 'WEBP', quality=80, method=6)

if __name__ == '__main__':
    spec = json.load(open(W + 'guides.json'))
    for name in sys.argv[1:]:
        source(name)
        if 'layers' in spec[name]:
            names = build_general(name, spec[name]); export_general(name, names, spec[name].get('soft_top', []))
        else:
            build(name, spec[name]); export(name)
