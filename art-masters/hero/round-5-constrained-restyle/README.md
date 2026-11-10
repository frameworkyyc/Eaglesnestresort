# Hero, round 5 (2026-11-10): constrained restyle, raw output (awaiting the client's assessment)

One Nano Banana 2.1 masked edit of the whole scene: 21:9, 4k, thinking level high, 3.00 credits
(balance 22.50 -> 19.50). Job ae2360c4-03a7-4dfb-afdc-a7fdddf08117. Stored exactly as generated (6344 x 2688);
nothing composited or corrected.

| File | What it is |
|---|---|
| `restyle-raw-nano-banana-2-1.png` | Raw output, byte-identical to the download (sha256 3a9f8b22...be49b4). |
| `prompt.txt` | Exact prompt. Ends with the mandatory no-text clause. |
| `inputs/image1-layout-softened.jpg` | Image 1 (media 0dd92926-64df-4eee-9757-0a706d1c9959): Round 3 hero, mildly edge-preserving smoothed, headline area untouched. |
| `inputs/image2-style-swatches.jpg` | Image 2 (media 59498f1e-2acb-4e1e-b8ba-899b25f0ed5b): eight close-ups from Round 4, technique without layout. |
| `inputs/mask.png` | Edit area (white, 76.6%): everything except the headline space (media f2d32566-6f10-46fc-938b-dad2095953a2). |

Image 3 was the client's lodge illustration crop (media de9a99a8-cd5a-4f44-a7b5-f56bb37fd2ba).

## Measurements against Round 3
- Frame: scale 1.003, shift -0.1% W; lodge outline 99%, glass gable 99%, dock and boat 99%, geese 100%.
- Sun: same place (0.582, 0.308 vs 0.581, 0.313), softer and wider glow.
- Mountain tops still about 0.365 H; the range and its hatched slopes now reach about 0.05 W further left (to ~0.34 W).
- Colour: sky warmth unchanged (LAB b* +22.4 vs +22.3); water slightly bluer; foliage and timber around the lodge
  shifted to brown (a* +8.9 vs +2.3), the green is gone.
- Headline zone (0,0,.46,.60): detail 7.9, edges 0.024 - passes (9.0 / 0.035) but busier than Round 3 (2.4 / 0.002);
  the far left (x < 0.33) is calmer than Round 3 (1.5 vs 1.8); the added detail is hatched cloud and slope at 0.33-0.46.
- TEXT: 3 OCR FAIL readings, all hatching on spruce and slopes; no lettering or logos.
