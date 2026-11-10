# Hero, round 1 (2026-11-10): candidates only, none approved yet

Same prompt (`prompt.txt`) and same five reference images for both:
1. `art-masters/inputs/hero-reference-clean.png` (uploaded at 3x, Higgsfield media b0308efe-1548-4a52-b96e-28a41105621b)
2. lodge-exterior.jpg (679a3648-bd14-44b0-9f07-20f090d54743)
3. lodge-decks.jpg (8499a20a-6511-4e6d-b403-38d9bfcda3ac)
4. lodge-entrance.jpg (bed36b76-7c36-46b9-8977-e4013ddb6361)
5. aerial-wide.jpg (995667af-3956-4bab-a782-1d4e238f6274)

| File | Model | Settings | Job id | Credits | Size |
|---|---|---|---|---|---|
| A-nano-banana-2-1.png | nano_banana_2_1 | 21:9, 4k | 96e4634a-aac5-4821-898e-aa35c280049c | 3.00 | 6336 x 2688 |
| B-gpt-image-2-6.png | gpt_image_2_6 | 21:9, 2k, quality high | 47b2f2be-a99c-4a6a-b8c7-3aed45274061 | 2.75 | 2688 x 1152 |

Balance 36.25 -> 30.50.

## Checks (scripts/art-qa.py, text-safe zone 0,0,.46,.6)
- A: OCR auto-flagged 4 spots (snow streaks, slope, aspen trunk, spruce foliage); all inspected at full size, none is lettering.
  Corners clean. SPACE pass (detail 3.3, edges 0.008). Composition: 99% of reference outlines within 1% of width.
- B: OCR auto-flagged 1 spot (dock post bolt); inspected, not lettering. Corners clean.
  SPACE fail on edges (detail 7.5, edges 0.060; reference sky measures about 0.007): sky hatching needs softening.
  Composition: 95% within 1% of width.
