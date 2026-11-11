// Things To Do, Painting A: responsive images cut from the raw master (no generation, no change to the art).
// Run when the master changes:  node scripts/ttd-art.mjs
// Writes src/ttd/art/, which Eleventy copies to /assets/ttd/art/.
//
// The master is 4096 x 4096 and covers 729 x 729 reference px: page x 0..729, page y -25..704
// (page y 0 = the bottom of the hero). Its top 25 px continue the hero's lake.
import sharp from "sharp";
import { mkdirSync, rmSync } from "node:fs";

const src = "art-masters/things-to-do/painting-a/round-1/painting-a-raw-nano-banana-2-1.png";
const out = "src/ttd/art";
rmSync(out, { recursive: true, force: true });
mkdirSync(out, { recursive: true });
const m = await sharp(src).metadata();
const s = m.width / 729; // master px per reference px
const fmts = [["avif", { quality: 50, effort: 4 }], ["webp", { quality: 72 }], ["jpg", { quality: 78, mozjpeg: true }]];
const save = (img, name, f, o) => img.toFormat(f === "jpg" ? "jpeg" : f, o).toFile(`${out}/${name}.${f}`);

// crops in page coordinates (reference px)
const region = (x0, x1, y0, y1) => {
  const left = Math.round(x0 * s), top = Math.round((y0 + 25) * s);
  return { left, top, width: Math.min(m.width, Math.round(x1 * s)) - left, height: Math.min(m.height, Math.round((y1 + 25) * s)) - top };
};
const cuts = {
  // desktop: the whole painting behind chapters 1-3
  "paint-a": { r: null, widths: [960, 1440, 1920, 2560, 3200] },
  // tablets and phones: bands matched to the hero's own crops (tablet hero shows x 165.6-714.6, phone hero x 379.1-729)
  "shore-tablet": { r: region(165.6, 714.6, 0, 100), widths: [900, 1400, 2000] },
  "shore-phone": { r: region(379.1, 729, 0, 100), widths: [480, 780, 1170] },
  "peaks-tablet": { r: region(0, 729, 245, 340), widths: [900, 1400, 2000] },
  "peaks-phone": { r: region(369, 729, 245, 345), widths: [480, 780, 1170] },
  "moose-tablet": { r: region(300, 729, 555, 704), widths: [900, 1400, 2000] },
  "moose-phone": { r: region(369, 729, 555, 704), widths: [480, 780, 1170] },
  // the painted map under the pannable map on tablets and phones: the map figure's own box
  "map": { r: region(175, 610, 311, 516), widths: [640, 1280, 1920] },
};
for (const [name, { r, widths }] of Object.entries(cuts)) {
  for (const w of widths)
    for (const [f, o] of fmts) {
      const img = r ? sharp(src).extract(r) : sharp(src);
      await save(img.resize({ width: w }), `${name}-${w}`, f, o);
    }
  const { width, height } = r || m;
  console.log(`${name}: ${width}x${height} (aspect ${(width / height).toFixed(4)})`);
}
