# Things To Do: cinematic full-screen chapters, prototype (2026-11-11)

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

| Path | What it is |
|---|---|
| `cut-layers.py` | Cuts the layers from the approved finals: `python3 art-masters/things-to-do/cinematic-prototype/cut-layers.py p4 p5` (from the repository root). Writes `work/` (full PNG layers and review sheets, git-ignored) and `prototype/layers/`. Prints the at-rest recombination error (0.14 and 0.69 levels out of 255). |
| `guides.json` | The hand guide lines and boxes for each painting's seams and cutouts. |
| `prototype/index.html` | The prototype page. Its layers, five 640 px photo copies and the heading font are alongside. |
| `capture/` | The Playwright scripts that made the review stills (`stills.js`), the desktop recording (`rec.js`) and the frame-by-frame phone recording (`frames.js`). They expect the prototype served at `http://127.0.0.1:8770/local.html`, a copy of `index.html` with a `<!doctype html>` head added (the published artifact adds its own). |

Published for review at https://claude.ai/artifact/5NJ1o1ngc9htionZU5QLxK (private to the owner).
