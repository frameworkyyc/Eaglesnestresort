"""Input for a full redraw (no generation): the model's own full-scene redraw (job e0d73545), with
Candidate A's calm haze and water restored on the left, where the model invented a forested point, and
Candidate A's lower goose restored. Usage: prepare.py OUT.png"""
import sys, cv2, numpy as np
A = cv2.imread('../gen/A-nano-banana-2-1.png'); H, W = A.shape[:2]
E = cv2.resize(cv2.imread('../combined/edit-raw.png'), (W, H), interpolation=cv2.INTER_AREA)
Mf = np.load('../combined/ecc.npy')
AE = cv2.warpAffine(A, Mf, (W, H), flags=cv2.INTER_LANCZOS4, borderMode=cv2.BORDER_REPLICATE)
yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
def ramp(v, a, b): r = np.clip((v - a) / (b - a), 0, 1); return r * r * (3 - 2 * r)
left_all = (1 - ramp(xx, .30 * W, .37 * W)) * (1 - ramp(yy, .80 * H, .86 * H))   # sky, invented point and its reflection
sky_band = (1 - ramp(xx, .40 * W, .47 * W)) * (1 - ramp(yy, .52 * H, .56 * H))    # hills fading into haze
k = np.maximum(left_all, sky_band)[..., None]
I = E * (1 - k) + AE * k
g = cv2.imread('../combined/goose2-mask.png', 0).astype(np.float32) / 255
gE = cv2.GaussianBlur(cv2.warpAffine(g, Mf, (W, H), flags=cv2.INTER_LINEAR), (0, 0), 1.2)[..., None]
I = np.clip(I * (1 - gE) + AE * gE, 0, 255).astype(np.uint8)
cv2.imwrite(sys.argv[1], I)
