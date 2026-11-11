# Things To Do, painting 4 (chapter 4, "Find a trail"), round 1 (2026-11-11): raw output (awaiting the client's assessment)

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
