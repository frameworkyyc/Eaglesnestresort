# Artwork standard: illustrations only, never text

Applies to every image generated for the Eagle's Nest website, on every page and section.

## 1. No text in artwork

Generated images contain illustration and texture only. All of these are HTML, styled with CSS:

- headlines, paragraphs, captions, labels, species names, map labels and place names
- chapter numbers and any other numerals
- buttons, phone numbers and calls to action
- the Eagle's Nest logo (always the official file, placed in HTML, never drawn into art)

Not even decorative or illegible lettering is allowed: no signage text, signatures, monograms,
watermarks, scribbles that read as handwriting, or numbers on signs. A sign, label, note or map in
the artwork is drawn blank; the words are laid over it in HTML.

Every prompt ends with this clause, unchanged:

> Absolutely no text of any kind: no letters, words, numbers, chapter numbers, labels, captions,
> sign lettering, map labels, logos, monograms, signatures, watermarks or decorative pseudo-writing,
> not even tiny or illegible marks that resemble writing. Any sign, note or label stays blank.

## 2. Negative space for the HTML

Each section's text sits where it sits in the approved reference. The artwork keeps those areas calm:
soft, open and low in contrast, with no birds, trees, boats, rocks or strong detail. The prompt names
the zone in plain words and as a fraction of the frame.

| Section | Text-safe zone (fraction of the image: x0, y0, x1, y1) |
|---|---|
| Hero | 0, 0, 0.46, 0.60 (left side: misty sky down to just below the far shoreline) |
| Other sections | defined from the reference when each section's artwork is planned |

## 3. Inputs must be clean before use

Any crop of the reference that is given to a generator is first made text-free with classical image
processing (no generation), using `scripts/clean-reference.py`:

- text blocks are filled from the clean pixels on either side, row by row, with the boundary colours
  smoothed first so no streaks appear, then re-textured with structureless paper grain
- reference-only elements (torn paper edges, nav, logo, badges) are removed the same way
- the result must show no ghost letters, smears, hard edges, streaks or repeated textures at 4x zoom

## 4. Acceptance checks (inputs and every generated image)

Run `python3 scripts/art-qa.py IMAGE --zone x0,y0,x1,y1` with the section's text-safe zone.

- **TEXT** must pass: OCR finds no words. Short low-confidence readings are listed as REVIEW and boxed
  in `IMAGE.qa.png`; each one is inspected by eye (foliage, ripples and window bars are typical).
- **SPACE** must pass: the text-safe zone measures as calm (detail and edge limits in the script).
- A visual check at 4x zoom over the whole image, looking for letter-like marks.

An image that fails is regenerated, or the affected area is repainted with a masked edit. It is never
used with the text covered up by HTML.

### Record

| Image | TEXT | SPACE | Visual | Notes |
|---|---|---|---|---|
| `inputs/hero-reference-clean.png` | pass (0 words; 4 REVIEW items checked: snow streaks, dock reflections, window bars) | pass (detail 3.9, edges 0.006) | pass | Original crop fails: 46 words, detail 37.2 |
| `hero/round-1/A-nano-banana-2-1.png` | auto-flag 4, all texture on inspection: no text | pass (3.3 / 0.008) | pass, corners clean | candidate, not approved |
| `hero/round-1/B-gpt-image-2-6.png` | auto-flag 1, texture on inspection: no text | fail on edges (7.5 / 0.060), sky hatching | pass, corners clean | candidate, not approved |
| `hero/round-2-lodge/hero-A-lodge-1.png` | auto-flag 1 (6 x 9 px curtain fold), not text | pass (unchanged from A: 0 px changed in the text-safe zone) | pass, corners clean | lodge correction on A, attempt 1; superseded by round 3 |
| `hero/round-3-composition/hero-final.png` | OCR readings in texture only; high-confidence ones inspected: no text | pass (2.37 / 0.0024, calmer than A) | pass, corners clean | combined landscape + lodge edit; client found it composited-looking |
| `hero/round-4-full-redraw/redraw-raw-nano-banana-2-1.png` | 12 OCR flags, all hatching: no text | fail (11.0 / 0.044): hatched sky and far-shore slope in the headline zone | pass | full redraw, raw; cohesive but re-composed; style reference only |
| `hero/round-5-constrained-restyle/restyle-raw-nano-banana-2-1.png` | 3 OCR flags, all hatching: no text | pass (7.9 / 0.024), busier than Round 3 at x .33-.46 | pass | constrained restyle, raw; layout 99%; awaiting client's assessment |
| `things-to-do/painting-a/round-1/painting-a-raw-nano-banana-2-1.png` | 1 FAIL + 208 REVIEW, the strongest inspected: hatching, reeds, ripples, animals; no text | fail in 4 of 8 text zones (chapter 1 heading, bird column, chapter 2 heading and paragraph) | pass | Painting A raw; lake 97% / road within 1 ref px of the SVG; awaiting client's assessment |
| `things-to-do/painting-4/round-1/painting-4-raw-nano-banana-2-1.png` | 5 FAIL + 492 REVIEW, the 24 strongest inspected: hatching, rocks, spruce, cloud; no text | quiet text area on pale sky (previewed in the page at 1100 and 1458) | pass; one tiny curled knot on a rock spike | Chapter 4 scenery-only painting, raw; came back 2.84:1; top edge lighter than the agreed mist; awaiting client's assessment |
