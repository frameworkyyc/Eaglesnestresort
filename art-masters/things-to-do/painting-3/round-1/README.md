# Things To Do, painting 3 (chapter 3, "Chase a waterfall"), round 1 (2026-11-12): raw output (awaiting the client's assessment)

Chapter 3's own painting, replacing chapter 3's band of Painting A in the cinematic design: a deep, misty spruce forest,
scenery only, composed for full-screen parallax. Painting A is unchanged and keeps chapters 1 and 2.

One Nano Banana 2.1 masked edit: 16:9 requested, 4K, thinking level high, 3.00 credits (confirmed by the free cost
check). Job 99ec2ba3-947e-4c07-b83e-57c9c1544b9a. It came back 6336 x 2688 (2.36:1, not 16:9). Stored exactly as
generated, with nothing composited or corrected.

| File | What it is |
|---|---|
| `painting-3-raw-nano-banana-2-1.png` | Raw output, byte-identical to the download (sha256 a45e2f79...761cd088). |
| `prompt.txt` | Exact prompt, as sent (checked character for character), including the scenery-only line and the mandatory no-text clause. |
| `inputs/image1-layout.jpg` | Image 1 (media df249267-0103-4432-b071-dd18faeb6385): layout guide, 2916 x 1640 (16:9). Built only from Painting A's chapter 3 forest (its spruce silhouettes and misty middle distance, never the moose), soft mist and the locked edge colour #E3D4C0 at the top and bottom. |
| `inputs/image2-hero.jpg` | Image 2 (media 1302d841-622f-4187-a546-7a82dddb4aae): the approved hero, for style. |
| `inputs/image3-painting-4-final.jpg` | Image 3 (media 7e014204-8a1b-4601-8663-55c7faecd108): the approved painting 4, which follows chapter 3. |
| `inputs/image4-mask.png` | Mask (media 2434142a-01f5-4256-960d-31ae514b79cc): top 12 and bottom 20 reference px locked, 92% editable. |
| `inputs/build-layout.py` | The script that built images 1 and 4 (run from the repository root; it reads Painting A's chapter 3 band as cut by `cinematic-prototype/cut-layers.py a3`). |

## Measurements (729 reference px = full width, 8.691 px each; 309.3 reference px tall)
- Layout: as the guide asked. Tall, finely engraved spruce and fir rise almost the full height at the right (with a
  rocky, fern-covered forest floor), a tall stand at the left edge, nearer spruce low in the centre, a misty middle
  forest and pale far treelines, three depths separated by mist, and a mist bank along the bottom.
- Edges: both locked bands were kept. Top rows 0-10 #E4D3C0 and bottom rows ~299-309 #E4D1BE, each within dE 1.4 of
  #E3D4C0. The painting's own sky above the forest is a lighter parchment, #F7E7DA, so the top band shows as a step.
- Two treetops run into the top band and are cut flat by it: the tallest spruce (x 4808-5176 px) and one at the far
  right (x 5951-6063 px).
- Scenery only: no people, figures, animals, birds, vehicles, buildings or signs. Two tiny saplings in the mist at the
  bottom centre.
- Palette: greyer and more monochrome than Painting A's forest (grey-green spruce, warm parchment sky).
- TEXT: 20 OCR FAIL boxes, all inspected by eye: branch edges, stipple, hatching and trunks. No text.
