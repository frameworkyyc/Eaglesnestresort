# Things To Do, painting 4 (chapter 4, "Find a trail"), round 1 (2026-11-11): approved, with two local touch-ups

Chapter 4's own painting: high country in summer, scenery only. People, animals and anything that moves
become separate animated assets later. The outcrop's flat ledge is left empty for the hiker asset.

One Nano Banana 2.1 masked edit: 21:9 requested, 4K, thinking level high, 3.00 credits (balance 216.50 -> 213.50).
Job fe3eb9a7-1eec-4cd8-be3e-438849011c57. It came back 6912 x 2432 (2.84:1, not 21:9). Stored exactly as generated,
with nothing composited or corrected.

| File | What it is |
|---|---|
| `painting-4-raw-nano-banana-2-1.png` | Raw output, byte-identical to the download (sha256 0925d095...7286c26). |
| `prompt.txt` | Exact prompt, including the scenery-only line and the mandatory no-text clause. |
| `inputs/image1-layout.jpg` | Image 1 (media 4ea59538-57ca-46ff-88e7-1a3a57681a98): layout guide, 2916 x 1248. Built from the original reference's chapter 4 artwork with its text, photographs, gold trail and torn edges removed and the hiker removed. The outcrop is moved under the text, with a locked mist band at the top (#E3D4C0) and a locked cloud band at the bottom (#E4E3DC). |
| `inputs/image2-hero.jpg` | Image 2 (media 1302d841-622f-4187-a546-7a82dddb4aae): the approved hero, for style. |
| `inputs/image3-painting-a-foot.jpg` | Image 3 (media 2a5dccca-b8be-49fa-95ec-c3297c1d8c6c): the foot of Painting A (chapter 3's crop), for continuity. |
| `inputs/image4-mask.png` | Mask (media 944b01fd-cc2e-496e-9cd9-7e3c00796d4b): top 12 and bottom 20 reference px locked. |
| `inputs/build-layout.py` | The script that built images 1 and 4 from the reference. |

## Measurements (729 reference px = full width, 9.481 px each; 256.5 reference px tall)
- Edges: the top is #F1E8E0, lighter than the agreed mist #E3D4C0, because the wider output did not keep the locked band.
  The bottom is #E7E4DD against the agreed cloud #E4E3DC, which matches.
- Outcrop ledge at reference row ~166, x 84-175. Placed 40 reference px down in the chapter on the mist colour, the
  ledge is at row 206 and the heading and paragraph sit on pale sky at 1100 and 1458 px. This was previewed in a
  browser session only.
- Scenery only: no people, animals, birds or vehicles. One tiny curled knot (about 10 reference px) sits on a rock
  spike at the right end of the ledge.
- TEXT: 5 OCR FAIL readings and 492 REVIEW readings. The 24 strongest were inspected: slope hatching, rock shading,
  spruce and cloud lines. No text.

## Approved, with two local touch-ups (2026-11-11)
The client approved painting 4 and asked for two local corrections, made without any new generation or credits.
The raw output above stays byte-identical; the corrected painting is a separate file.

| File | What it is |
|---|---|
| `corrected/painting-4-final.png` | The painting to use: 6912 x 2432, RGB (the raw's alpha channel was 255 everywhere, so nothing is lost). |
| `corrected/correct.py` | The script that makes it from the raw file. It checks the raw checksum before and after. |

1. **Top mist colour.** The top edge now matches chapter 3's handoff colour, H34 `#E3D4C0` (row 0 measures `#E3D4C0`,
   ΔE76 0.2, against 9.6 in the raw). This is a colour-only grade: one LAB offset (L -6.85, a +0.56, b +6.52) at full
   strength on rows 0-16, eased out to nothing by row 200 (8% of the height). An offset adds no blur: the paper grain is
   unchanged (high-pass 0.746 raw, 0.754 final) and every line is as painted.
2. **The knot.** The looped ornament on the tip of the rock spike at the right end of the ledge (about x 1745-1792,
   y 1612-1642) is removed. The spike's own two edges, measured on rows 1648-1664 and extended, meet at (1775, ~1639),
   so the spike now ends in its own point, inked like its flanks. The knot's area is refilled with the clean parchment sky
   from 64 rows above, tone-matched and feathered.

Checks: no pixel changed outside rows 0-199 and the knot's box (x 1730-1809, y 1596-1647); the bottom edge is unchanged
(`#E7E4DE`, against the agreed cloud `#E4E3DC`); the raw checksum is unchanged. TEXT: 7 OCR FAIL readings (iff, SSS, SS, AN, WN, NY, SS),
every one on pixels identical to the raw, all inspected by eye: slope hatching, rock shading and stipple. No text.
