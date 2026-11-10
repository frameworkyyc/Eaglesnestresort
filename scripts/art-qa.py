#!/usr/bin/env python3
"""Artwork QA for the Eagle's Nest site. Every reference input and every generated image
must pass before it is used (see art-masters/ARTWORK-STANDARD.md).

  python3 scripts/art-qa.py IMAGE [--zone x0,y0,x1,y1] [--zone ...]

Checks
  1. TEXT   OCR (Tesseract) at several scales and page modes, on the whole image and on
            overlapping tiles. Tesseract also "reads" letters in foliage, ripples and window
            mullions, so results are graded:
              FAIL    a token of 3+ characters read with confidence >= 85, or a 2-character
                      token read with confidence >= 92. Real lettering reads at 90+ (the reference's
                      own headline and intro read at 96-97); texture rarely does. Dense engraving
                      can still trigger this, so every FAIL is also inspected by eye.
              REVIEW  any other token read with confidence >= 60. Each is boxed in IMAGE.qa.png
                      and must be inspected by eye before the image is accepted.
              ignored boxes under 5 px tall (smaller than any letter could be) and
                      low-confidence guesses.
  2. SPACE  For each --zone (fractions of width/height, e.g. 0,0,.46,.6 for the hero's text
            area), measures fine detail (high-pass luminance std) and object edges (Canny
            density). Above the limits = too busy for HTML text to sit on.
Exit code 0 = pass, 1 = fail. Needs: tesseract, opencv-python-headless, numpy.
"""
import argparse, csv, io, subprocess, sys, tempfile, os
import cv2, numpy as np

CONF = 60          # OCR confidence that counts as a reading
MIN_H = 5          # px; boxes shorter than this cannot hold a letter
FAIL_CONF = 85     # confidence at which a 3+ character reading fails outright
DETAIL_MAX = 9.0   # high-pass luminance std allowed in a text zone
EDGE_MAX = 0.035   # fraction of Canny edge pixels allowed in a text zone


def ocr_tokens(img):
    hits = []
    with tempfile.TemporaryDirectory() as d:
        p = os.path.join(d, "t.png")
        h, w = img.shape[:2]
        tiles = [(0, 0, w, h)]
        tw, th = max(w // 2, 1), max(h // 2, 1)
        for y in range(0, h - th // 2, th // 2):
            for x in range(0, w - tw // 2, tw // 2):
                tiles.append((x, y, min(w, x + tw), min(h, y + th)))
        for x0, y0, x1, y1 in tiles:
            crop = img[y0:y1, x0:x1]
            for scale in (2, 3):
                cv2.imwrite(p, cv2.resize(crop, None, fx=scale, fy=scale, interpolation=cv2.INTER_CUBIC))
                for psm in ("3", "11"):
                    out = subprocess.run(["tesseract", p, "-", "--psm", psm, "tsv"], capture_output=True, text=True).stdout
                    for r in csv.DictReader(io.StringIO(out), delimiter="\t"):
                        t = (r.get("text") or "").strip()
                        try:
                            c = float(r["conf"])
                        except (TypeError, ValueError, KeyError):
                            continue
                        if len(t) >= 2 and any(ch.isalnum() for ch in t) and c > 0:
                            bx = x0 + int(r["left"]) // scale; by = y0 + int(r["top"]) // scale
                            bw = int(r["width"]) // scale; bh = int(r["height"]) // scale
                            hits.append((t, int(c), (bx, by, bw, bh)))
    return hits


def zone_stats(img, z):
    h, w = img.shape[:2]
    x0, y0, x1, y1 = (int(z[0] * w), int(z[1] * h), int(z[2] * w), int(z[3] * h))
    g = cv2.cvtColor(img[y0:y1, x0:x1], cv2.COLOR_BGR2GRAY).astype(np.float32)
    detail = float((g - cv2.GaussianBlur(g, (0, 0), 3)).std())
    edges = float((cv2.Canny(g.astype(np.uint8), 60, 140) > 0).mean())
    return detail, edges


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("image")
    ap.add_argument("--zone", action="append", default=[], help="x0,y0,x1,y1 as fractions")
    a = ap.parse_args()
    img = cv2.imread(a.image)
    if img is None:
        sys.exit(f"cannot read {a.image}")
    ok = True
    hits = ocr_tokens(img)
    sized = [(t, c, b) for t, c, b in hits if b[3] >= MIN_H and c >= CONF]
    fail = [(t, c, b) for t, c, b in sized if (len(t) >= 3 and c >= FAIL_CONF) or c >= 92]
    review = [(t, c, b) for t, c, b in sized if (t, c, b) not in fail]
    if sized:
        dbg = img.copy()
        for t, c, (x, y, w, h) in sized:
            col = (0, 0, 255) if (t, c, (x, y, w, h)) in fail else (0, 200, 255)
            cv2.rectangle(dbg, (x, y), (x + w, y + h), col, 1)
        cv2.imwrite(os.path.splitext(a.image)[0] + ".qa.png", dbg)
    print(f"TEXT   {'FAIL' if fail else 'pass'}  words: {sorted({t for t, _, _ in fail}) or 'none'}")
    for t, c, (x, y, w, h) in sorted(set(review), key=lambda r: (r[2][1], r[2][0])):
        print(f"       REVIEW '{t}' conf {c} at x{x} y{y} {w}x{h}  -> inspect by eye in .qa.png")
    print(f"       ignored: {len(hits) - len(sized)} sub-glyph or low-confidence texture guesses")
    ok &= not fail
    for zs in a.zone:
        z = [float(v) for v in zs.split(",")]
        d, e = zone_stats(img, z)
        bad = d > DETAIL_MAX or e > EDGE_MAX
        ok &= not bad
        print(f"SPACE  {'FAIL' if bad else 'pass'}  zone {zs}: detail {d:.1f} (max {DETAIL_MAX}), edges {e:.3f} (max {EDGE_MAX})")
    print("RESULT", "PASS" if ok else "FAIL")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
