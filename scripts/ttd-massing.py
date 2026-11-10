"""Phase 1 placeholder massing for the Things To Do page.

Draws flat landscape silhouettes (ridges, spruce rows, torn paper edges) in colours
sampled from the approved reference image. Coordinates are reference pixels
(the reference is 729 px wide). These are composition placeholders only; Phase 3
replaces them with Higgsfield artwork. Run: python3 scripts/ttd-massing.py
"""
import random, math, os
OUT = os.path.join(os.path.dirname(__file__), '..', 'src', 'ttd', 'bg')
W = 729

def f(v): return f'{v:.1f}'.rstrip('0').rstrip('.')

def ridge(pts, rnd, rough=1.2, step=(2.5, 6)):
    """Interpolate control points into a jagged, hand-torn line."""
    out = []
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        x = x0
        while x < x1:
            t = (x - x0) / (x1 - x0)
            y = y0 + (y1 - y0) * t + rnd.uniform(-rough, rough)
            out.append((x, y)); x += rnd.uniform(*step)
    out.append(pts[-1])
    return out

def poly(points, bottom, fill, extra=''):
    d = f'M{f(points[0][0])} {f(bottom)} ' + ' '.join(f'L{f(x)} {f(y)}' for x, y in points) + f' L{f(points[-1][0])} {f(bottom)}Z'
    return f'<path d="{d}" fill="{fill}"{extra}/>'

def mountains(peaks, base, rnd, rough=1.0):
    """peaks: list of (x, y) apex points; valleys are generated between them."""
    pts = [(peaks[0][0] - 40, base)]
    for i, (px, py) in enumerate(peaks):
        pts.append((px, py))
        if i < len(peaks) - 1:
            nx, ny = peaks[i + 1]
            pts.append(((px + nx) / 2 + rnd.uniform(-8, 8), max(py, ny) + rnd.uniform(12, 30)))
    pts.append((peaks[-1][0] + 40, base))
    return ridge(pts, rnd, rough)

def spruce(x, base, h, w, rnd):
    tiers = 5
    pts = [(x, base - h)]
    for i in range(1, tiers + 1):
        ty = base - h + h * 0.88 * i / tiers
        hw = w * 0.5 * (0.35 + 0.65 * i / tiers)
        pts.append((x + hw + rnd.uniform(-0.6, 0.6), ty))
        if i < tiers: pts.append((x + hw * 0.45, ty - h * 0.05))
    pts.append((x + w * 0.06, base - h * 0.1)); pts.append((x + w * 0.06, base))
    pts.append((x - w * 0.06, base)); pts.append((x - w * 0.06, base - h * 0.1))
    for i in range(tiers, 0, -1):
        ty = base - h + h * 0.88 * i / tiers
        hw = w * 0.5 * (0.35 + 0.65 * i / tiers)
        if i < tiers: pts.append((x - hw * 0.45, ty - h * 0.05 + h * 0.88 / tiers))
        pts.append((x - hw + rnd.uniform(-0.6, 0.6), ty))
    return 'M' + ' L'.join(f'{f(a)} {f(b)}' for a, b in pts) + 'Z'

def forest(x0, x1, base, hfn, rnd, spacing=(5, 10), wr=0.32):
    d = []; x = x0
    while x < x1:
        h = hfn(x) * rnd.uniform(0.82, 1.12)
        d.append(spruce(x, base + rnd.uniform(-2, 2), h, h * wr, rnd)); x += rnd.uniform(*spacing)
    return ' '.join(d)

def svg(name, h, body, defs=''):
    s = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {h}" width="{W}" height="{h}">'
         f'<defs>{defs}</defs>{body}</svg>')
    open(os.path.join(OUT, name), 'w').write(s)
    print(name, len(s) // 1024, 'KB')

def torn(points, bottom, fill, shade, light):
    """Paper edge: soft shadow above, fill, and a pale torn lip along the top."""
    sh = [(x, y - 1.6) for x, y in points]
    lip = ' '.join(f'{f(x)},{f(y + 0.7)}' for x, y in points)
    return (poly(sh, bottom, shade, ' opacity=".35"') + poly(points, bottom, fill) +
            f'<polyline points="{lip}" fill="none" stroke="{light}" stroke-width="1.1" stroke-opacity=".8"/>')

def hatch(x0, x1, y0, y1, rnd, color, n=40, op=.35):
    lines = []
    for _ in range(n):
        x = rnd.uniform(x0, x1); y = rnd.uniform(y0, y1); l = rnd.uniform(4, 12)
        lines.append(f'M{f(x)} {f(y)}l{f(l * .7)} {f(l * .45)}')
    return f'<path d="{" ".join(lines)}" stroke="{color}" stroke-width=".45" stroke-opacity="{op}" fill="none"/>'

# ---------------------------------------------------------------- hero (h 238)
r = random.Random(1)
defs = ('<linearGradient id="lake" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#9A988C"/><stop offset=".45" stop-color="#76776D"/><stop offset="1" stop-color="#565B55"/></linearGradient>'
        '<linearGradient id="refl" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FFE7A8" stop-opacity=".95"/><stop offset="1" stop-color="#E8B86A" stop-opacity="0"/></linearGradient>'
        '<radialGradient id="sun" cx="0" cy="0" r="1" gradientUnits="userSpaceOnUse" gradientTransform="translate(424 98) scale(95 70)"><stop offset="0" stop-color="#FFF6D6"/><stop offset=".18" stop-color="#F8DFA0" stop-opacity=".9"/><stop offset="1" stop-color="#E7C690" stop-opacity="0"/></radialGradient>')
b = '<rect width="729" height="238" fill="url(#sun)"/>'
b += poly(mountains([(10, 112), (80, 104), (150, 116), (230, 100), (290, 108)], 150, r), 160, '#B9AD93', ' opacity=".8"')
b += poly(mountains([(300, 92), (355, 78), (405, 94), (470, 70), (525, 84), (585, 88), (650, 98)], 150, r), 160, '#A39680')
b += poly(mountains([(330, 108), (390, 98), (450, 104), (515, 96), (580, 104)], 150, r, .8), 160, '#8A7F6A')
b += '<circle cx="424" cy="98" r="7.5" fill="#FFF8E2"/>'
b += poly(ridge([(-5, 140), (200, 139), (420, 137), (560, 134), (734, 136)], r, .8), 238, 'url(#lake)')
b += poly(ridge([(-5, 141), (180, 139), (380, 137), (560, 135), (734, 136)], r, .9), 146, '#5F5B48', ' opacity=".45"')
b += '<rect x="414" y="140" width="20" height="96" fill="url(#refl)"/>'
for i in range(14):
    y = 146 + i * 6.5 + r.uniform(-1, 1); w = 30 - i * 1.2
    b += f'<rect x="{f(424 - w / 2 + r.uniform(-2, 2))}" y="{f(y)}" width="{f(w)}" height=".9" fill="#FFF1C7" opacity=".55"/>'
b += poly(ridge([(530, 200), (580, 186), (640, 182), (734, 178)], r, 1.5), 212, '#5A5340')
b += f'<path d="{forest(530, 735, 190, lambda x: 36 + (x - 530) * .55, r, (4, 8))}" fill="#4A4F3C"/>'
b += f'<path d="{forest(575, 740, 200, lambda x: 70 + max(0, x - 610) * 1.05, r, (6, 11), .34)}" fill="#2E3628"/>'
svg('hero-scene.svg', 238, b, defs)

# ---------------------------------------------------------------- T1 snowy torn ridge (h 70)
r = random.Random(2)
pk = mountains([(10, 8), (60, 2), (120, 18), (175, 10), (230, 34), (300, 52), (380, 58), (450, 54), (520, 26), (585, 6), (650, 16), (705, 4)], 70, r, 1.4)
b = torn(pk, 70, '#E3D5BA', '#6B6550', '#FBF5E6')
b += poly(mountains([(40, 30), (110, 36), (190, 40), (540, 40), (620, 30), (690, 34)], 70, r, 1.2), 70, '#D8C8AB')
b += '<rect y="58" width="729" height="12" fill="#D8C8AB"/>'
b += hatch(0, 729, 10, 60, r, '#8E846D', 120, .4)
svg('t1-snow.svg', 70, b)

# ---------------------------------------------------------------- T2 sage mountains (h 110)
r = random.Random(3)
b = poly(mountains([(-10, 40), (50, 26), (110, 44), (165, 36), (215, 60)], 110, r), 110, '#A9A88E')
b += poly(mountains([(560, 30), (610, 8), (655, 22), (700, 2), (745, 14)], 110, r), 110, '#A3A58B')
b += poly(mountains([(-10, 62), (70, 48), (140, 66), (200, 70)], 110, r), 110, '#868D74')
b += poly(mountains([(575, 54), (630, 36), (680, 46), (720, 30), (750, 40)], 110, r), 110, '#7C866D')
b += poly(ridge([(-5, 92), (180, 86), (330, 94), (480, 88), (734, 84)], r, 1.6), 110, '#D8C8AB')
b += hatch(0, 230, 30, 90, r, '#5D6553', 60, .35) + hatch(560, 729, 10, 85, r, '#5D6553', 60, .35)
svg('t2-sage.svg', 110, b)

# ---------------------------------------------------------------- map paper + lake (stage 435 x 210)
r = random.Random(4)
def blob(cx, cy, rx, ry, n, jit, rnd):
    pts = []
    for i in range(n):
        a = 2 * math.pi * i / n
        k = 1 + rnd.uniform(-jit, jit) + .08 * math.sin(3 * a)
        pts.append((cx + rx * k * math.cos(a), cy + ry * k * math.sin(a)))
    return 'M' + ' L'.join(f'{f(x)} {f(y)}' for x, y in pts) + 'Z'
paper = blob(218, 108, 214, 104, 140, .035, r)
lake = blob(212, 115, 118, 52, 90, .07, r)
b = (f'<path d="{paper}" fill="#DECDA9" stroke="#B49F78" stroke-width=".8"/>'
     f'<path d="{lake}" fill="#6E8796" stroke="#4E6672" stroke-width="1"/>'
     f'<path d="{blob(212, 115, 104, 44, 90, .05, r)}" fill="none" stroke="#9DB0B8" stroke-width=".5" stroke-dasharray="2 3"/>')
b += hatch(20, 420, 20, 200, r, '#8C7A57', 90, .25)
open(os.path.join(OUT, 'map-paper.svg'), 'w').write(
    f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 435 210" width="435" height="210">{b}</svg>')
print('map-paper.svg')

# ---------------------------------------------------------------- forest band (falls, h 300; top at falls-relative -100)
r = random.Random(5)
def edge_h(x):  # tall at the sides, low under the map, kept clear of the chapter 2 copy
    h = 95 - 70 * math.exp(-((x - 390) / 190) ** 2)
    return min(h, 42) if 45 < x < 215 else h
b = f'<path d="{forest(-5, 735, 104, edge_h, r, (5, 9))}" fill="#4A5B4A"/>'
b += f'<path d="{forest(-5, 735, 118, lambda x: edge_h(x) * .85, r, (4, 8))}" fill="#34443A"/>'
b += '<rect x="0" y="116" width="729" height="200" fill="#2F3E34"/>'
b += f'<path d="{forest(-5, 735, 300, lambda x: 120 + 40 * math.sin(x / 60), r, (5, 10))}" fill="#2A372E" opacity=".9"/>'
b += f'<path d="{forest(-5, 260, 300, lambda x: 150, r, (6, 11))}" fill="#25312A"/>'
b += f'<path d="{forest(560, 735, 300, lambda x: 155, r, (6, 11))}" fill="#25312A"/>'
svg('falls-forest.svg', 300, b)

# ---------------------------------------------------------------- T3 pale ridge (h 60)
r = random.Random(6)
pk = mountains([(0, 22), (60, 8), (130, 26), (200, 14), (270, 30), (350, 18), (430, 32), (500, 12), (580, 26), (650, 6), (720, 20)], 60, r, 1.3)
b = torn(pk, 60, '#C4C1A6', '#1E2A22', '#EEEADB') + poly(mountains([(30, 36), (160, 30), (300, 40), (460, 34), (610, 30), (720, 38)], 60, r), 60, '#B4B297')
b += hatch(0, 729, 10, 55, r, '#6B6E5C', 90, .35)
svg('t3-pale.svg', 60, b)

# ---------------------------------------------------------------- trails backdrop (h 150)
r = random.Random(7)
b = poly(mountains([(160, 40), (240, 22), (330, 44), (420, 20), (520, 38), (610, 16), (700, 34)], 150, r), 150, '#B1B099')
b += poly(mountains([(-10, 70), (60, 58), (140, 80), (600, 74), (680, 52), (740, 64)], 150, r), 150, '#9EA088')
b += poly(ridge([(-5, 150), (10, 128), (40, 112), (70, 96), (92, 94), (115, 108), (140, 122), (165, 150)], r, 1.2), 150, '#3B4237')
b += hatch(150, 729, 20, 90, r, '#6E705E', 90, .3)
svg('trails-bg.svg', 150, b)

# ---------------------------------------------------------------- T4 icy ridge (h 60)
r = random.Random(8)
pk = mountains([(0, 18), (70, 4), (140, 22), (215, 10), (290, 28), (370, 12), (450, 26), (530, 6), (600, 22), (670, 8), (735, 16)], 60, r, 1.4)
b = torn(pk, 60, '#93A2AB', '#2E3B44', '#F2F4F3') + poly(mountains([(20, 32), (180, 30), (340, 38), (500, 28), (660, 34)], 60, r), 60, '#7C8E98')
b += hatch(0, 729, 6, 50, r, '#F4F6F6', 110, .5)
svg('t4-ice.svg', 60, b)

# ---------------------------------------------------------------- winter (h 190, top at winter-relative -20)
r = random.Random(9)
defs = '<linearGradient id="w" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#7D8E98"/><stop offset=".55" stop-color="#A9B4BA"/><stop offset="1" stop-color="#D4DADC"/></linearGradient>'
b = '<rect width="729" height="190" fill="url(#w)"/>'
b += poly(mountains([(200, 50), (300, 36), (420, 54), (520, 40), (640, 56)], 190, r), 190, '#9AA8B0', ' opacity=".7"')
b += poly(ridge([(-5, 128), (120, 140), (300, 156), (500, 152), (734, 146)], r, 1.4), 190, '#D3DADD')
b += f'<path d="{forest(-5, 230, 160, lambda x: 120 - x * .3, r, (7, 13), .4)}" fill="#33444E"/>'
b += f'<path d="{forest(640, 735, 156, lambda x: 90 + (x - 640) * .5, r, (7, 12), .4)}" fill="#33444E"/>'
b += hatch(0, 230, 40, 150, r, '#F1F4F4', 90, .5) + hatch(640, 729, 60, 150, r, '#F1F4F4', 40, .5)
svg('winter-bg.svg', 190, b, defs)

# ---------------------------------------------------------------- T5 night treeline (h 70)
r = random.Random(10)
def hill(x):  # ground rises toward the left, as in the reference
    return 64 - 26 * math.exp(-((x - 60) / 170) ** 2)
b = poly(ridge([(-5, hill(-5)), (120, hill(120)), (260, hill(260)), (420, hill(420)), (734, hill(734))], r, 1.0), 72, '#22344A')
d = []; x = -5
while x < 735:
    h = min(r.uniform(14, 44) * (1.3 if r.random() < .18 else 1), hill(x) - 3)
    d.append(spruce(x, hill(x) + 2, h, h * r.uniform(.3, .42), r)); x += r.uniform(4, 15)
b += f'<path d="{' '.join(d)}" fill="#22344A"/>'
b += '<rect x="0" y="64" width="729" height="8" fill="#22344A"/>'
svg('t5-night.svg', 70, b)

# ---------------------------------------------------------------- night (h 132)
r = random.Random(11)
b = poly(mountains([(150, 52), (260, 40), (380, 56), (500, 44), (620, 58), (720, 46)], 132, r), 132, '#22344A')
b += f'<path d="{forest(-5, 735, 120, lambda x: 40 + 22 * math.sin(x / 38) + (25 if x > 470 else 0), r, (5, 9), .34)}" fill="#111C26"/>'
b += '<rect x="0" y="116" width="729" height="16" fill="#111C26"/>'
stars = ''
for _ in range(90):
    x, y = r.uniform(0, 729), r.uniform(2, 70)
    stars += f'<circle cx="{f(x)}" cy="{f(y)}" r="{f(r.uniform(.25, .8))}" fill="#F3EEE1" opacity="{f(r.uniform(.35, .95))}"/>'
const = [(190, 40), (222, 30), (251, 36), (276, 22), (310, 30)], [(390, 18), (420, 34), (452, 30), (470, 48), (440, 56)]
for c in const:
    stars += '<polyline points="' + ' '.join(f'{x},{y}' for x, y in c) + '" fill="none" stroke="#F3EEE1" stroke-opacity=".5" stroke-width=".6" stroke-dasharray="1.2 2.2"/>'
    stars += ''.join(f'<circle cx="{x}" cy="{y}" r="1.1" fill="#F3EEE1"/>' for x, y in c)
svg('night-bg.svg', 132, stars + b)  # sky gradient lives in CSS so the torn treeline above can own the edge

# ---------------------------------------------------------------- T6 ragged paper edge (h 30)
r = random.Random(12)
pts = ridge([(-5, 12), (120, 8), (260, 14), (400, 9), (560, 13), (734, 8)], r, 2.6, (1.5, 3.5))
b = poly(pts, 30, '#DCCDB0') + hatch(0, 729, 4, 18, r, '#16222E', 140, .5)
svg('t6-ragged.svg', 30, b)
