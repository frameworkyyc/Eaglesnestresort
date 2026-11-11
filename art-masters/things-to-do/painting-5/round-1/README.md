# Things To Do, painting 5 (chapter 5, "When the lake freezes"), round 1 (2026-11-11): raw output (awaiting the client's assessment)

Chapter 5's own painting: a quiet winter valley in late-afternoon light, scenery only. The snowmobile and rider become a
separate animated asset later; the painting keeps open snow and a pair of tracks for it.

One Nano Banana 2.1 masked edit: 21:9 requested, 4K, thinking level high, 3.00 credits (confirmed by the free cost check).
Job fa238188-2ba9-4dea-bbd2-ffab117b9ae7. It came back 6280 x 2688 (21:9, as requested). Stored exactly as generated,
with nothing composited or corrected.

| File | What it is |
|---|---|
| `painting-5-raw-nano-banana-2-1.png` | Raw output, byte-identical to the download (sha256 b7436672...eefdd6a3). |
| `prompt.txt` | Exact prompt, as sent (checked character for character against the request), including the scenery-only line and the mandatory no-text clause. |
| `inputs/image1-layout.jpg` | Image 1 (media 8e8ecb73-d057-43ef-b82f-d0f840a0cbc3): layout guide, 2916 x 1248. Soft colour zones, the reference's own snow-laden spruce at both edges, a pair of track lines, a locked cloud band at the top (#E4E3DC) and a locked dusk band at the bottom (#3A4763). The reference's text, photographs, rider and footprints are left out. |
| `inputs/image2-hero.jpg` | Image 2 (media 1302d841-622f-4187-a546-7a82dddb4aae, the same upload as painting 4's): the approved hero, for style. |
| `inputs/image3-painting-4-final.jpg` | Image 3 (media 7e014204-8a1b-4601-8663-55c7faecd108): the approved painting 4, final version, for continuity. |
| `inputs/image4-mask.png` | Mask (media 944b01fd-cc2e-496e-9cd9-7e3c00796d4b, byte-identical to painting 4's): top 12 and bottom 20 reference px locked. |
| `inputs/build-layout.py` | The script that built images 1 and 4 (run from the repository root). |

## Measurements (729 reference px = full width, 8.615 px each; 312 reference px tall)
- Top edge: a flat, featureless dark band (#282C38) on rows 0-7.8, then pale sky (#E0E3EB). The agreed cloud colour
  #E4E3DC was not kept (dE 72.7). The band holds no scenery, so a colour-only local fill would correct it.
- Bottom edge: #333B56 against the agreed dusk #3A4763 (dE 5.5), reached through a smooth fade on rows ~260-300.
- Layout against the guide: the snowy ranges, rose-gold light, frozen lake, edge spruce, open snowfield, tracks and dusk
  are all there. The landscape sits lower than in the guide (the lake's far shore at row ~180, not ~104); the left spruce
  are taller (up to row ~48, mostly under the gold trail's margin); the tracks run from the lake shore at (227, 196) in
  an S-curve toward the viewer and leave at the bottom near x 300.
- Quiet text zone (x 76-281, rows 46-133): pass, detail 6.1 and edges 0.022. Text contrast in the page preview, measured
  per glyph: 5.6:1 or better at 1100, 1458 and 1920 px (heading about 12:1).
- Scenery only: no people, animals, birds, vehicles, buildings or signs. One tiny upright mark (under 2 reference px)
  on the tip of the lake's point at about (365, 183): a stump or rock at full size, invisible at page scale.
- TEXT: 9 OCR FAIL words in 19 boxes (AN, SS, SSS, WH, WS, fff, the, ty, ve). All 19 inspected by eye: slope hatching,
  a distant row of small spruce and spruce branches. No text.
