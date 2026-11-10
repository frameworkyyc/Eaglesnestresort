"""Paste the lodge edit back into Candidate A so that nothing outside the lodge changes.

Run from the repository root:
    python3 art-masters/hero/round-2-lodge/composite.py \
        art-masters/hero/round-2-lodge/edit-1-nano-banana-2-1.png out.png

The edit model may redraw a roof or a tree a little past the white mask. Those strokes are kept
(the "spill" extension: pixels within 60 px of the mask that differ clearly from Candidate A and
touch the mask); everything else comes from Candidate A unchanged. Alpha below 1/255 is zeroed so
rounding cannot alter any pixel outside the paste area.
"""
import json
import os
import sys

import cv2
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
A = cv2.imread(os.path.join(HERE, '..', 'round-1', 'A-nano-banana-2-1.png'))[:, :, :3]
g = json.load(open(os.path.join(HERE, 'inputs', 'geometry.json')))
cx0, cy0, cw, ch = g['crop']
E = cv2.resize(cv2.imread(sys.argv[1]), (cw, ch), interpolation=cv2.INTER_LANCZOS4)
region = A[cy0:cy0 + ch, cx0:cx0 + cw]
m = (cv2.imread(os.path.join(HERE, 'inputs', 'mask-crop.png'), 0) > 0).astype(np.uint8)


def lab(i):
    return cv2.cvtColor(i, cv2.COLOR_BGR2LAB).astype(np.float32)


d = np.linalg.norm(cv2.GaussianBlur(lab(E), (0, 0), 3) - cv2.GaussianBlur(lab(region), (0, 0), 3), axis=2)
band = cv2.dilate(m, np.ones((3, 3), np.uint8), iterations=60) - m
spill = ((d > 28) & (band > 0)).astype(np.uint8)
spill = cv2.morphologyEx(spill, cv2.MORPH_OPEN, np.ones((5, 5), np.uint8))
n, labels = cv2.connectedComponents(cv2.bitwise_or(spill, m))
keep = np.isin(labels, np.unique(labels[m > 0]))
ext = (keep & ((spill > 0) | (m > 0))).astype(np.uint8)
ext = cv2.morphologyEx(ext, cv2.MORPH_CLOSE, np.ones((9, 9), np.uint8))
ext = cv2.dilate(ext, np.ones((3, 3), np.uint8), iterations=3)
alpha = cv2.GaussianBlur(ext.astype(np.float32), (0, 0), 4)
alpha[alpha < 1 / 255] = 0
alpha = alpha[..., None]
out = A.copy()
out[cy0:cy0 + ch, cx0:cx0 + cw] = np.clip(region * (1 - alpha) + E * alpha, 0, 255).astype(np.uint8)
cv2.imwrite(sys.argv[2], out)
