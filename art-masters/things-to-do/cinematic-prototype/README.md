# Things To Do: cinematic full-screen chapters, prototype

Approved by the client as the working design direction, with this prototype's motion strength and one-screen
transition length as the baseline. Prototype only: nothing here is part of the website. `art-masters/` is never read by
the site build (Eleventy reads `src/`, the Worker serves `public/`).

Chapters 4 and 5 as full-screen scenes. Each painting is cut into four depth layers (sky, far ranges, middle distance,
near trees or rock) that recombine into the exact approved painting at rest. Each chapter's scene stays pinned while its
content scrolls over it; during the last screen the next chapter rises over it, its far layers first and its near
layers fastest, while the outgoing chapter's layers part. Text and photographs never sit on a moving layer. The hiker
and snowmobile assets have reserved spots inside the layer they stand on. Scroll-driven CSS (view timelines) on
transform and opacity only; reduced motion, or a browser without scroll-driven animations, gets the scenes stacked
statically with soft fades.

## Phase 1 (2026-11-12): the hero to chapter 5

The client approved the seven-chapter plan and asked for phase 1: the prototype extended from the hero through chapter 5
with the existing artwork only. The hero and every chapter's content are the website's own built markup and stylesheet;
only the stage (the layered painting) and the motion are new.

- Hero to 1: no takeover. Chapter 1's shore continues the hero's lake exactly as on the page (the same 25 reference px
  faded overlap on desktop, the hero's own crop on tablets and phones), and lifts away as chapter 2 rises.
- 1 to 2: Painting A's snowy range rises over the parchment, the valley follows faster, the near spruce fastest. On
  desktop the map's pins sit on the painted valley and appear once it has settled; they fade before chapter 3 arrives.
  Below 1100 px the site's pannable map card is chapter 2's scene.
- 2 to 3: the misty forest rises over the valley; the near spruce and the moose (cut out on their own) come fastest.
- 3 to 4 and 4 to 5: as prototyped before.
- Tablets and phones: heading and paragraph on a pale card, photographs in a swipeable row. Landscape phones (under
  561 px tall), reduced motion and browsers without scroll-driven animations get the static version.

| Path | What it is |
|---|---|
| `cut-layers.py` | Cuts the layers: `python3 art-masters/things-to-do/cinematic-prototype/cut-layers.py a1 a2 p3 p4 p5` from the repository root. `a1` and `a2` are Painting A's bands for chapters 1 and 2 (`a3`, its old chapter 3 band, can still be cut for reference), `p3`-`p5` the approved paintings 3, 4 and 5. Writes `work/` (full PNG layers and review sheets) and `prototype/layers/`. Prints each band's at-rest recombination error (0.0-0.69 levels out of 255). |
| `guides.json` | The hand guide lines, boxes and cut-out rules for each band's seams and layers. |
| `build-prototype.py` | Assembles `prototype/index.html` from `public/things-to-do.html` (run `npm run build` first if `src/` changed) and `prototype-template.html`, and copies the site assets it uses into `prototype/assets/`. Never writes to `public/` or `src/`. |
| `prototype-template.html` | The stage, motion and fallback rules around the site's content. |
| `prototype/` | The prototype: `index.html` and `layers/` (committed); `assets/` (rebuilt, git-ignored). |
| `capture/` | Playwright scripts (`.cjs`, because the repository is an ES module package): `rest.cjs` (each chapter at rest and each transition's midpoint), `journey.cjs` (the complete scroll, frame by frame), and the earlier `stills.cjs`, `rec.cjs`, `frames.cjs`. They expect the prototype served at `http://127.0.0.1:8771/local.html`, a copy of `index.html` with a `<!doctype html>` head added. |

Nothing here is part of the website: Eleventy reads `src/`, the Worker serves `public/`.

## Chapter 3: painting 3 (2026-11-12)
Chapter 3 now uses the approved painting 3 (`painting-3/round-1/corrected/painting-3-final.png`) instead of Painting
A's forest band: four layers (sky; the pale far treelines; the misty middle forest; the tall near spruce, cut out),
the same motion as chapters 4 and 5, its sky the painting's parchment `#F2DFCC`. For this painting the layers beneath
the near trees are filled to the trees' full outline (`cover` 0.4 in guides.json) so no tree-shaped outlines show while
the layers part; at rest 0.42% of pixels, all on tree edges, differ by more than 8 levels. Painting A's chapter 3 band
(`a3`) is no longer used. Tablets and phones now take each chapter's own crop (the inline value became `--fxd`, so the
media rules can override it). `capture/transitions.cjs` records the chapter 2 -> 3 -> 4 scroll.

Performance: once a chapter's scene is fully covered by the next (its sky is opaque from the end of the takeover), it
is hidden, so only one chapter's layers are painted at a time; scrolling back shows it again. Each chapter's layer
images declare their real desktop width in `sizes` (100-128vw), so the browser picks the 1440 or 2560 px file that
fits.
