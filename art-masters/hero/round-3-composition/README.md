# Hero, round 3 (2026-11-10): corrected composition, one combined edit (awaiting review)

Candidate A (`../round-1/A-nano-banana-2-1.png`) with the alpine peaks replaced by rolling forested hills and a
low, hazy distant range, and the lodge rebuilt to the approved revised Layout 1. Everything outside the edited
area is pixel-for-pixel Candidate A.

| File | What it is |
|---|---|
| `hero-final.png` | The result, 6336 x 2688. |
| `edit-raw-nano-banana-2-1.png` | Raw model output, 6344 x 2688 (job e0d73545-c5d5-43b4-a919-f63b39845f01). |
| `prompt.txt` | Exact prompt sent. Ends with the mandatory no-text clause. |
| `inputs/composition-guide.jpg` | Image 1: the approved composition, assembled locally from Candidate A and the client's lodge illustration (no generation). |
| `inputs/mask.png` | The edit area (white), 22.5% of the image; the sun disc and geese excluded. |
| `inputs/alignment-affine.npy` | Affine that maps the raw output onto Candidate A (fitted by ECC on water, dock and rocks). |
| `inputs/protect-lower-goose.png` | Silhouette of the lower goose, kept exactly as in Candidate A. |
| `scripts/landscape.py`, `scripts/guide.py` (+ params) | Build the composition guide: landscape from A's own drawing, lodge from the illustration. |
| `scripts/composite.py` | Pastes the aligned edit into Candidate A (see "Compositing" below). |

## Request
`nano_banana_2_1`, inpaint, 21:9, 4k, 3.00 credits (balance 28.50 -> 25.50). Images: composition guide
(media 728734b3-7bf9-474a-89b9-f2c22d2d85ab), lodge illustration crop (de9a99a8-cd5a-4f44-a7b5-f56bb37fd2ba),
mask (4ad4f9c6-34e9-4045-a5cf-94c2c51d1d2a).

## Compositing (no further generation)
- The output came back 8 px wider and about 1.2% zoomed in; aligned to A with the stored affine (residual a few px).
- Only the edit area is used. The model also drew a forested shore in the headline space; that is discarded.
- The new hills fade into the haze over x 0.405-0.48 instead of ending at a straight edge.
- A's own far-shore treeline is kept (the model's was paler and blurrier, and A's matches its reflection).
- The lower goose's downstroke wing is restored from A; the sun disc and the upper goose are untouched.
- The rightmost 1.2% (beyond the model's frame after alignment) keeps A's own aspen and rocks.

## Checks
- 0 pixels changed outside the paste area; sun, both geese, person fishing and boats: 0 pixels changed.
- Lodge outline: 98% of the approved layout's edges within 0.5% of frame width (glass gable 98%).
- Highest land in the landscape: 36.5% from the top (guide 33.5%; Candidate A's peaks 25-30%).
- Headline zone (0,0,.46,.60): detail 2.37, edges 0.0024 (Candidate A 2.56 / 0.0041).
- TEXT: OCR readings in foliage, rocks, shingles, window frames and hatching; every high-confidence one inspected
  at full size, none is lettering.
- Known minor issue: a soft darker patch between the top-right spruces where A had slivers of the old peaks.
