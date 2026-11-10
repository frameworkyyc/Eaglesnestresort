// Things To Do hero: responsive images from the approved master (no generation, no change to the art).
// Run when the master changes:  node scripts/hero-images.mjs
// Writes src/ttd/hero/, which Eleventy copies to /assets/ttd/hero/.
import sharp from "sharp";
import { mkdirSync } from "node:fs";

const src = "art-masters/hero/round-5-constrained-restyle/colour-corrected/hero-r5-colour-corrected.png";
const out = "src/ttd/hero";
mkdirSync(out, { recursive: true });
const m = await sharp(src).metadata();
const fmts = [["avif", { quality: 50, effort: 4 }], ["webp", { quality: 72 }], ["jpg", { quality: 78, mozjpeg: true }]];
const save = (img, name, f, o) => img.toFormat(f === "jpg" ? "jpeg" : f, o).toFile(`${out}/${name}.${f}`);

// tablets and desktops: the whole scene
for (const w of [960, 1440, 1920, 2560, 3200])
  for (const [f, o] of fmts) await save(sharp(src).resize({ width: w }), `scene-${w}`, f, o);

// phones: the right 48% (lodge, its woods, the end of the dock, sun and geese); the lodge is the priority
const left = Math.round(m.width * 0.52);
for (const w of [480, 780, 1170])
  for (const [f, o] of fmts)
    await save(sharp(src).extract({ left, top: 0, width: m.width - left, height: m.height }).resize({ width: w }), `phone-${w}`, f, o);
console.log(`hero images: master ${m.width}x${m.height}, phone crop ${m.width - left}x${m.height}`);
