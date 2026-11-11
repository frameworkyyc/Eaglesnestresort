# Things To Do, Painting A, round 1 (2026-11-11): raw output (awaiting the client's assessment)

Painting A is the first illustrated panel below the hero. It runs from the lakeshore through the map country
to the forest of chapter 3 (page y -25 to 704 in reference pixels, 729 x 729).

One Nano Banana 2.1 masked edit: 1:1, 4k, thinking level high, 3.00 credits (balance 19.50 -> 16.50).
Job 88c98a68-63a8-42df-b4ba-d48b5d80cf55. Stored exactly as generated (4096 x 4096); nothing composited,
aligned or corrected.

| File | What it is |
|---|---|
| `painting-a-raw-nano-banana-2-1.png` | Raw output, byte-identical to the download (sha256 fd410ae4...f06e853). |
| `prompt.txt` | Exact prompt. Ends with the mandatory no-text clause. |
| `inputs/image1-layout.jpg` | Image 1 (media 58d6f218-e704-4724-a3da-96653739a3f4): text-free layout guide, 2916 x 2916. It holds the hero's bottom strip, artwork from the original reference with all content removed, calm fills and the site's own SVG lake and road. |
| `inputs/image2-hero.jpg` | Image 2 (media 20c009b1-2b77-41f1-82fd-080948629b01): the approved hero (colour-corrected Round 5), style and continuity reference. |
| `inputs/image3-mask.png` | Mask (media 4e7561a0-9056-493e-bd48-d684cb9cad38): top 25 reference px locked (black), the rest edited (white). |

## Measurements (output scaled to 2916 px; 4 px = 1 reference px)
- Lake against the SVG lake: 97.1% overlap (IoU); outline mean deviation 3.8 px (about 1 reference px), max 16 px.
  Centroid 2 px from the SVG's.
- Road against the SVG road: centreline mean deviation 0.3 px across 66 columns; runs about 20 reference px further right.
- Seam with the hero: the locked strip was redrawn, not copied (mean difference 18.6/255) and about 0.5% larger.
  Lake ripples and the sunrise reflection continue across the join. Needs alignment before use.
- Map pins: the painted lodge is about 25 reference px east of the "Eagle's Nest Resort" pin. No waterfall is painted
  at either falls pin. The painted falls sit far left at (154, 480).
- TEXT: 1 OCR FAIL ("SS", mountain hatching) and 208 REVIEW readings. The 24 strongest were inspected: hatching, reeds,
  ripples, loon, moose antlers, cabin roof. No lettering, numbers, map labels or signatures.
- SPACE (text zones): fails at the chapter 1 heading (28.4 / 0.174, reeds and rocks), the bird-watching column
  (10.4 / 0.015), and the chapter 2 heading (17.9 / 0.053) and paragraph (12.1 / 0.022) (left mountains and hills).
  The other text zones pass.
