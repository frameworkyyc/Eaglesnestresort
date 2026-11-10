# Round 5, colour-corrected (awaiting review)

`hero-r5-colour-corrected.png` (6344 x 2688) is `../restyle-raw-nano-banana-2-1.png` with Round 3's forest greens
restored. No generation was used. Only colour (LAB a*, b*) moved, on vegetation (13.2% of pixels); every
pixel's lightness (L*) was held, so the engraving, linework, textures, architecture and composition are Round 5's
(mean L* change 0.014; 99.9% of pixels within 0.31, the rest 8-bit rounding). All other pixels are byte-identical.

- `recolour.py` builds it. It needs Round 3 aligned into Round 5's frame (`r3-in-r5-frame.png`), made by warping
  `../../round-3-composition/hero-final.png` with the affine fitted between Round 3 and Round 5 (ECC on the 6336-wide
  frame: scale 1.0032 / 1.0003, shift -0.0012 W) and resizing to 6344 wide.
- `vegetation-mask.png`: where colour moved. Excludes the geese (`protect-geese.png`), sky, water, rocks, the dock,
  timber, roofs, the glass wall and diamond windows.
- Each vegetation area takes Round 3's local mean colour (normalised blur, sigma 28 px) while keeping Round 5's own
  variation within it.

Checks: water 0 px changed, geese 0 of 102,748, sky 203 stray px at tree tips. Headline contrast (page's real
headline at 1440 px, no haze): 7.1:1 or better over 95% of the background behind every line.
