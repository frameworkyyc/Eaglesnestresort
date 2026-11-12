"""Builds the cinematic prototype (hero to chapter 5) from the site's own built page, so the hero and every chapter's
content render exactly as on the website. Only the stage (the layered painting) and the motion are new.

  python3 art-masters/things-to-do/cinematic-prototype/cut-layers.py a1 a2 a3 p4 p5   # the layers (if changed)
  npm run build                                                                     # the site, if src changed
  python3 art-masters/things-to-do/cinematic-prototype/build-prototype.py

Reads public/things-to-do.html and public/assets (never writes there). Writes prototype/index.html plus copies of the
assets it uses under prototype/assets/. Nothing here is part of the website.
"""
import os, re, shutil

ROOT = os.getcwd()
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'prototype')
page = open(os.path.join(ROOT, 'public/things-to-do.html'), encoding='utf-8').read()
css_name = re.search(r'/assets/(ttd\.[0-9a-f]+\.css)', page).group(1)

def block(start_pat, tag):
    """The element starting at start_pat, through its matching closing tag."""
    i = page.index(start_pat); depth = 0
    for m in re.finditer(rf'<{tag}\b|</{tag}>', page[i:]):
        depth += 1 if m.group(0) != f'</{tag}>' else -1
        if depth == 0: return page[i:i + m.end()]
    raise ValueError(start_pat)

def inner(html, start_pat, tag):
    i = html.index(start_pat); depth = 0
    for m in re.finditer(rf'<{tag}\b|</{tag}>', html[i:]):
        depth += 1 if m.group(0) != f'</{tag}>' else -1
        if depth == 0: return html[i:i + m.end()]
    raise ValueError(start_pat)

hero = block('<header class="fg-sec fg-hero"', 'header')
chapters = {n: block(f'<section class="fg-ch fg-ch{n}', 'section') for n in range(1, 6)}

# ---- per chapter: the stage (layers cut from the approved paintings) and its sky -----------------------------
STAGES = {  # aspect of the layer images, focal x, sky colour, layer names (back to front)
    1: dict(art='a1', ar=2560 / 966, fx=.5, sky='#F6E5D5', layers=['back', 'front']),
    2: dict(art='a2', ar=2560 / 1061, fx=.5, sky='#F4E3D2', layers=['back', 'peaks', 'mid', 'front']),
    3: dict(art='p3', ar=2560 / 1440, fx=.5, sky='#F2DFCC', layers=['back', 'peaks', 'mid', 'front']),
    4: dict(art='p4', ar=2560 / 901, fx=.43, sky='#E3D3C0', layers=['back', 'peaks', 'mid', 'front']),
    5: dict(art='p5', ar=2560 / 1096, fx=.36, sky='#E4E3DC', layers=['back', 'peaks', 'mid', 'front']),
}
LABELS = {
    1: ['back · parchment', 'front · the shore'],
    2: ['back · sky', 'peaks · snowy range', 'mid · the valley map', 'front · near spruce'],
    3: ['back · sky', 'far · pale treelines', 'mid · misty forest', 'front · tall spruce'],
    4: ['back · sky', 'peaks · far ranges', 'mid · forested mountain', 'front · outcrop'],
    5: ['back · sky', 'peaks · snowy peaks', 'mid · forest, lake, snowfield', 'front · near spruce'],
}
SLOTS = {(4, 'front'): '<div class="slot" data-label="Hiker asset" style="--sx:.165;--sy:.648;--sw:.05;--sh:.22"></div>',
         (5, 'mid'): '<div class="slot" data-label="Snowmobile asset" style="--sx:.29;--sy:.74;--sw:.075;--sh:.12"></div>'}

def stage(n, extra_mid=''):
    s = STAGES[n]; out = [f'<div class="stage" style="--ar:{s["ar"]:.4f};--fxd:{s["fx"]};--top:{s["sky"]}">']
    out.append('<div class="skygrp" aria-hidden="true"><div class="sky"></div><div class="cap"></div></div>')
    for nm, lab in zip(s['layers'], LABELS[n]):
        img = (f'<img src="layers/{s["art"]}-{nm}-2560.webp" srcset="layers/{s["art"]}-{nm}-1440.webp 1440w, '
               f'layers/{s["art"]}-{nm}-2560.webp 2560w" sizes="(max-width:1099px) 300vw, 125vw" alt="" aria-hidden="true" decoding="async"'
               + (' loading="lazy"' if n > 2 else '') + '>')
        extra = SLOTS.get((n, nm), '') + (extra_mid if nm == 'mid' else '')
        out.append(f'<div class="ly {nm}" data-name="{lab}">{img}{extra}</div>')
    out.append('</div>')
    return '\n      '.join(out)

def remove_ground(html):
    g = inner(html, '<div class="fg-ground"', 'div'); return html.replace(g, '')

def scene(n):
    html = remove_ground(chapters[n])
    open_tag = re.match(r'<section [^>]*>', html).group(0)
    body = html[len(open_tag):-len('</section>')]
    sid = re.search(r'id="([^"]+)"', open_tag).group(1); lab = re.search(r'aria-labelledby="([^"]+)"', open_tag).group(1)
    trail = inner(body, '<svg class="fg-trailseg"', 'svg')
    fgc = inner(body, '<div class="fg-c">', 'div')
    pinmap = ''
    if n == 2:   # desktop: the map's pins sit on the painted valley (the mid layer) and move with it
        fig = inner(fgc, '<figure class="fg-map"', 'figure').replace('id="map-cap"', 'id="map-cap-d"').replace('aria-labelledby="map-cap"', 'aria-labelledby="map-cap-d"')
        pinmap = f'<div class="pinmap">{fig}</div>'
    if n >= 2:   # tablets and phones: the heading and paragraph share one card (display:contents on desktop)
        head = inner(fgc, '<div class="fg-head', 'div')
        para = re.search(r'<p class="fg-p[^"]*fg-para[^"]*">.*?</p>', fgc, re.S).group(0)
        fgc = fgc.replace(head, '').replace(para, f'<div class="card">{head}{para}</div>', 1)
    return (f'<section class="scene s{n} fg-ch{n}" id="{sid}" aria-labelledby="{lab}">\n      {stage(n, pinmap)}\n'
            f'    <div class="content">{trail}{fgc}</div>\n    <div class="run" aria-hidden="true"></div>\n  </section>')

body = '\n\n  '.join([hero] + [scene(n) for n in range(1, 6)])

# ---- copy the assets the markup uses, and rewrite their URLs to relative ones --------------------------------
used = set(re.findall(r'/assets/[^\s"\',)]+', body))
for u in used | {f'/assets/{css_name}', '/assets/fonts/roboto-serif-cond.woff2', '/assets/ttd/deckle-c.svg'}:
    src = os.path.join(ROOT, 'public' + u); dst = os.path.join(OUT, u.lstrip('/'))
    os.makedirs(os.path.dirname(dst), exist_ok=True); shutil.copyfile(src, dst)
css = open(os.path.join(OUT, 'assets', css_name)).read().replace('url(/assets/', 'url(')
os.remove(os.path.join(OUT, 'assets', css_name)); open(os.path.join(OUT, 'assets/ttd.css'), 'w').write(css)
body = body.replace('"/assets/', '"assets/').replace(' /assets/', ' assets/').replace(',/assets/', ',assets/')
body = body.replace('href="lodge.html"', 'href="#farther"')    # the prototype has no lodge page

template = open(os.path.join(HERE, 'prototype-template.html'), encoding='utf-8').read()
open(os.path.join(OUT, 'index.html'), 'w', encoding='utf-8').write(template.replace('<!--CHAPTERS-->', body))
print('prototype/index.html written;', len(used), 'site assets copied')
