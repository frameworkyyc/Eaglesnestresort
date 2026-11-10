// Builds CSS, JS and fonts into src/_generated (hashed names) and writes src/_data/assets.json.
// Eleventy then copies src/_generated to public/assets.
import { readFileSync, writeFileSync, mkdirSync, rmSync, copyFileSync, existsSync } from "node:fs";
import { createHash } from "node:crypto";
import { transform } from "lightningcss";
import { build } from "esbuild";

const out = "src/_generated";
rmSync(out, { recursive: true, force: true });
mkdirSync(`${out}/fonts`, { recursive: true });

const hash = (buf) => createHash("sha1").update(buf).digest("hex").slice(0, 8);

// ---- fonts (self-hosted, latin subset) ----
const fonts = {
  "fraunces-soft.woff2": "node_modules/@fontsource-variable/fraunces/files/fraunces-latin-soft-normal.woff2",
  "figtree.woff2": "node_modules/@fontsource-variable/figtree/files/figtree-latin-wght-normal.woff2",
  "barlow-condensed-500.woff2": "node_modules/@fontsource/barlow-condensed/files/barlow-condensed-latin-500-normal.woff2",
  "barlow-condensed-600.woff2": "node_modules/@fontsource/barlow-condensed/files/barlow-condensed-latin-600-normal.woff2",
  "caveat-700.woff2": "node_modules/@fontsource/caveat/files/caveat-latin-700-normal.woff2",
};
for (const [name, src] of Object.entries(fonts)) {
  if (!existsSync(src)) throw new Error("missing font " + src);
  copyFileSync(src, `${out}/fonts/${name}`);
}

// ---- CSS ----
const cssFiles = ["tokens", "base", "components", "home"].map((n) => readFileSync(`src/styles/${n}.css`, "utf8"));
const css = transform({
  filename: "site.css",
  code: Buffer.from(cssFiles.join("\n")),
  minify: true,
  targets: { chrome: 111 << 16, safari: 16 << 16, firefox: 111 << 16 },
}).code;
const cssName = `site.${hash(css)}.css`;
writeFileSync(`${out}/${cssName}`, css);

// ---- JS ----
const js = await build({
  entryPoints: ["src/scripts/main.js"], bundle: true, minify: true, format: "iife",
  target: ["es2020"], write: false,
});
const jsCode = js.outputFiles[0].contents;
const jsName = `site.${hash(jsCode)}.js`;
writeFileSync(`${out}/${jsName}`, jsCode);

writeFileSync("src/_data/assets.json", JSON.stringify({ css: `/assets/${cssName}`, js: `/assets/${jsName}` }, null, 2));
console.log(`assets: ${cssName} ${(css.length / 1024).toFixed(1)} KB, ${jsName} ${(jsCode.length / 1024).toFixed(1)} KB`);
