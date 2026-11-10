# Hero, round 4 (2026-11-10): full redraw, raw output (awaiting the client's assessment)

One Nano Banana 2.1 redraw of the whole picture: 21:9, 4k, thinking level high, no mask, 3.00 credits
(balance 25.50 -> 22.50). Job d537bfcf-73d3-42c2-b14d-5d32dec9a10a. The output is stored exactly as
generated (6336 x 2688); nothing was composited or corrected, at the client's request.

| File | What it is |
|---|---|
| `redraw-raw-nano-banana-2-1.png` | The raw output, byte-identical to the download (sha256 740721de...c2c95c). |
| `prompt.txt` | Exact prompt sent. Ends with the mandatory no-text clause. |
| `inputs/redraw-input.jpg` | Image 1 (media f2cc9f01-eafa-4ed0-8888-4e3243c86d34): the model's own full-scene render from round 3 with Candidate A's calm haze and water restored on the left and the lower goose restored. |
| `inputs/prepare.py` | Builds that input from round 3's raw output and Candidate A. |

Image 2 was the client's lodge illustration crop (media de9a99a8-cd5a-4f44-a7b5-f56bb37fd2ba).

## Assessment (raw output)
- Consistent linework, hatching and texture across the whole scene.
- Lodge architecture kept (glass curtain wall under the gable, diamond windows, dark timber, in-line right wing
  with balconies), but the lodge is about 1.3x larger and moved left (gable centre ~0.65 W instead of ~0.80 W);
  the setback is reduced (glass base ~0.63 H instead of ~0.55 H); the left wing is no longer screened by trees.
- Palette shifted to sepia and brown; the sun is faint. Dock and boat moved lower and left; large foreground rocks added.
- Headline zone (0,0,.46,.60) fails SPACE: detail 11.0, edges 0.044 (limits 9.0 / 0.035).
- TEXT: 12 OCR FAIL readings, all hatching on inspection; no lettering or logos.
