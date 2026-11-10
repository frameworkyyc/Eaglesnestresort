# Hero, round 2 (2026-11-10): lodge correction on Candidate A, attempt 1 (awaiting review)

Candidate A (`../round-1/A-nano-banana-2-1.png`) with only the lodge replaced, using the client's
lodge illustration as the main architectural reference and three photos for materials.

| File | What it is |
|---|---|
| `hero-A-lodge-1.png` | The corrected hero, 6336 x 2688. Pixel-identical to Candidate A outside the paste area. |
| `edit-1-nano-banana-2-1.png` | Raw model output for the crop, 2400 x 1792 (job 9485e584-6087-406f-9977-ab81c8be3573). |
| `prompt.txt` | Exact prompt sent. Ends with the mandatory no-text clause. |
| `composite.py` | Pastes the edit back into Candidate A. Re-running it on the raw output reproduces `hero-A-lodge-1.png` byte for byte. |
| `inputs/geometry.json` | Crop of Candidate A sent to the model (x, y, w, h in px) and the mask polygon (fractions of A). |
| `inputs/mask-crop.png` | The mask in crop space (white = may change). |
| `inputs/ref-illustration-lodge.png` | Lodge crop of the client's illustration (image 2 of the request). |

## Request
- Model `nano_banana_2_1`, inpaint (`is_inpaint`), 4:3, 2k. 2.00 credits. Balance 30.50 -> 28.50.
- Images, in order: crop of Candidate A x 3801-6336, y 499-2400 (media 97e1385e-d34c-4a0c-b870-7d836801210b);
  mask (270cda59-c547-4519-93cd-ab1e606e01e4); illustration crop (aad3deff-2dfd-4e46-a6aa-36f70bd6b5c9);
  photos: glass gable among trees (0a463ead-fc6f-468b-b850-7f69878c549a), balcony wing
  (a774fa5f-ec62-4add-be60-db11da4c0b65), timber mullions (81a862f1-26e3-4b1e-9447-daaf05d4b539).
  The woodpile photo was left out because it shows a printed brand label.

## Checks
- Change map against Candidate A: 12.83% of pixels changed, all inside the paste area (12.90%, x .670-.998, y .207-.699).
  0 pixels changed outside it; 0 changed in the hero text-safe zone (0,0,.46,.60), so SPACE equals Candidate A.
- TEXT: OCR flagged one spot in the new area, a 6 x 9 px curtain fold inside a window; inspected at full size, not lettering.
  Gable, glass wall, windows and corners clean.
- Against the request: glass curtain wall, steep gable with vertical boards and diamond windows, two-tier balcony,
  engraving style and sunrise light all met. Wings and tree cover only partly: the wings are shorter than in the
  illustration and only one tall spruce stands in front of the building. Wing siding is cooler than the real stain.
