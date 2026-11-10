import Image from "@11ty/eleventy-img";
import { readFileSync } from "node:fs";

const artManifest = JSON.parse(readFileSync("src/art/manifest.json", "utf8"));

export default function (eleventyConfig) {
  // ---- legacy pages stay live while the new design is rolled out page by page ----
  eleventyConfig.addPassthroughCopy({
    "legacy/css": "css", "legacy/js": "js", "legacy/images": "images", "legacy/lodge": "lodge",
    "legacy/booking.html": "booking.html", "legacy/getting-here.html": "getting-here.html",
    "legacy/hosts.html": "hosts.html", "legacy/lodge.html": "lodge.html",
  });
  // Things To Do is rebuilt from src/things-to-do.njk; its placeholder massing and review overlay:
  eleventyConfig.addPassthroughCopy({ "src/ttd": "assets/ttd" });
  eleventyConfig.addPassthroughCopy({ "src/_generated": "assets", "src/art": "assets/art" });

  // ---- real photographs: responsive AVIF / WebP / JPEG ----
  eleventyConfig.addAsyncShortcode("photo", async (file, alt, o = {}) => {
    const meta = await Image(`src/photos/${file}`, {
      widths: o.widths || [480, 800, 1200], formats: ["avif", "webp", "jpeg"],
      outputDir: "public/assets/img/", urlPath: "/assets/img/",
      sharpAvifOptions: { quality: 52 }, sharpWebpOptions: { quality: 70 }, sharpJpegOptions: { quality: 76, mozjpeg: true },
    });
    return Image.generateHTML(meta, {
      alt, sizes: o.sizes || "(min-width: 900px) 40vw, 92vw", loading: o.loading || "lazy", decoding: "async",
      class: o.class || "", ...(o.priority ? { fetchpriority: "high" } : {}),
    });
  });

  // ---- illustrations (transparent AVIF with WebP fallback). Decorative by default: alt="" ----
  eleventyConfig.addShortcode("art", (name, o = {}) => {
    const m = artManifest[name];
    if (!m) throw new Error(`unknown art asset: ${name}`);
    const cls = o.class ? ` class="${o.class}"` : "";
    const alt = (o.alt || "").replace(/"/g, "&quot;");
    return `<picture${cls}><source type="image/avif" srcset="/assets/art/${name}.avif">` +
      `<img src="/assets/art/${name}.webp" width="${m.width}" height="${m.height}" alt="${alt}" ` +
      `loading="${o.loading || "lazy"}" decoding="async"${o.alt ? "" : ' aria-hidden="true"'}></picture>`;
  });

  eleventyConfig.addFilter("year", () => new Date().getFullYear());

  return {
    dir: { input: "src", output: "public", includes: "_includes", data: "_data" },
    templateFormats: ["njk", "md"], htmlTemplateEngine: "njk",
  };
}
