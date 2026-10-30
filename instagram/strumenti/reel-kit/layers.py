"""Split an image into paper background, card (photo cut-out) and accent-coloured objects.

Works on any 9:16 image. Objects = pixels close to the brand accent colour (plus their white sticker outline).
layout='card'  -> the image has a cut-out photo on plain paper (collage style)
layout='full'  -> full-bleed image, no paper/card separation
"""
import numpy as np, cv2
from PIL import Image

W, H = 1080, 1920


def hex2rgb(h):
    h = h.lstrip('#'); return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def accent_mask(big, accent, tol=16, loose=False):
    hsv = cv2.cvtColor(big, cv2.COLOR_RGB2HSV).astype(int)
    ah = cv2.cvtColor(np.uint8([[accent]]), cv2.COLOR_RGB2HSV)[0, 0].astype(int)
    dh = np.abs(hsv[..., 0] - ah[0]); dh = np.minimum(dh, 180 - dh)
    smin = 60 if not loose else 35
    return ((dh < (tol if not loose else tol + 8)) & (hsv[..., 1] > smin) & (hsv[..., 2] > (60 if not loose else 40))).astype(np.uint8)


def fit(src):
    s = W / src.shape[1]
    big = cv2.resize(src, (W, round(src.shape[0] * s)), interpolation=cv2.INTER_LANCZOS4)
    if big.shape[0] < H:  # too short: scale to height
        s = H / src.shape[0]
        big = cv2.resize(src, (round(src.shape[1] * s), H), interpolation=cv2.INTER_LANCZOS4)
        x = (big.shape[1] - W) // 2; return big[:, x:x + W].copy()
    top = (big.shape[0] - H) // 2
    return big[top:top + H].copy()


def split(path, accent='#B8853C', layout='card', fill='inpaint', min_area=250, detect=True, outline=True, roi=None):
    src = np.array(Image.open(path).convert('RGB'))
    big = fit(src)
    acc = hex2rgb(accent)
    lum = big.mean(axis=2)
    objs, keep = [], np.zeros(big.shape[:2], np.uint8)
    gold = accent_mask(big, acc)
    if roi:  # only look for objects inside these rectangles [x0,y0,x1,y1] (1080x1920 coords)
        rm = np.zeros_like(gold)
        for x0, y0, x1, y1 in roi: rm[int(y0):int(y1), int(x0):int(x1)] = 1
        gold = gold * rm
    if detect:
        g2 = cv2.morphologyEx(gold, cv2.MORPH_CLOSE, np.ones((9, 9), np.uint8))
        near = cv2.dilate(g2, np.ones((17, 17), np.uint8))
        rim = ((near > 0) & (lum > 205)) if outline else np.zeros_like(g2, bool)
        obj = ((g2 > 0) | rim).astype(np.uint8)
        obj = cv2.morphologyEx(obj, cv2.MORPH_CLOSE, np.ones((7, 7), np.uint8))
        n, lab, stats, _ = cv2.connectedComponentsWithStats(obj)
        for k in range(1, n):
            x, y, w, h, a = stats[k]
            if a < min_area * 2.3: continue
            if w > W * .85 and h > H * .6: continue  # whole background tinted: not an object
            m = (lab == k)
            if (g2[m] > 0).sum() < 80: continue
            if w * h > .15 * W * H: continue  # warm wall / whole photo region, not an object
            if min(w, h) < 28 or (g2[m] > 0).sum() < .18 * w * h: continue  # thin edges / sparse warm streaks (wood, door frames, card borders)
            keep[m] = 1
            alpha = cv2.GaussianBlur(m.astype(np.float32), (3, 3), 0)
            rgba = np.dstack([big, (alpha * 255).astype(np.uint8)])[y:y + h, x:x + w]
            objs.append(dict(img=Image.fromarray(rgba, 'RGBA'), x=int(x), y=int(y), w=int(w), h=int(h)))
        objs.sort(key=lambda o: (o['y'], o['x']))

    # remove objects from the base image
    if objs:
        if fill == 'clone':
            near_g = cv2.dilate(gold, np.ones((61, 61), np.uint8)) > 0
            loose = accent_mask(big, acc, loose=True) & near_g
            hole = cv2.dilate(((keep > 0) | (gold > 0) | (loose > 0)).astype(np.uint8), np.ones((41, 41), np.uint8))
            ys_, xs_ = np.where(hole > 0)
            dh = int(ys_.max() - ys_.min()) + 10
            srcimg = big.copy(); srcimg[:-dh] = big[dh:]
            fm = cv2.GaussianBlur(hole.astype(np.float32), (31, 31), 0)[..., None]
            clean = (big * (1 - fm) + srcimg * fm).astype(np.uint8)
        else:
            hole = cv2.dilate(keep, np.ones((15, 15), np.uint8))
            clean = cv2.inpaint(big, hole, 9, cv2.INPAINT_TELEA)
    else:
        clean = big

    if layout == 'full':
        card = np.dstack([clean, np.full(big.shape[:2], 255, np.uint8)])
        return dict(paper=None, card=Image.fromarray(card, 'RGBA'), cx0=0, cy0=0, objs=objs, layout='full')

    # card mask: everything that is not paper (paper colour sampled from top strip)
    strip = big[30:200].reshape(-1, 3).astype(int)
    pc = np.median(strip, axis=0)
    bi = big.astype(int)
    lum_p = pc.mean(); crb_p = pc[0] - pc[2]; cgb_p = pc[1] - pc[2]
    paper = (np.abs(bi.mean(axis=2) - lum_p) < 32) & (np.abs((bi[..., 0] - bi[..., 2]) - crb_p) < 9) & (np.abs((bi[..., 1] - bi[..., 2]) - cgb_p) < 8)
    if abs(crb_p) < 6:  # neutral (white/grey) paper: cannot be told apart from photo highlights
        return split(path, accent, 'full', fill, min_area, detect, outline, roi)
    cardm = (~paper).astype(np.uint8)
    cardm = cv2.morphologyEx(cardm, cv2.MORPH_OPEN, np.ones((5, 5), np.uint8))
    cardm = cv2.morphologyEx(cardm, cv2.MORPH_CLOSE, np.ones((15, 15), np.uint8))
    n, lab, stats, _ = cv2.connectedComponentsWithStats(cardm)
    if n < 2:
        return split(path, accent, 'full', fill, min_area, detect, outline, roi)
    k = 1 + np.argmax(stats[1:, 4])
    cm = (lab == k).astype(np.uint8)
    cnts, _ = cv2.findContours(cm, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    cm = np.zeros_like(cm); cv2.drawContours(cm, cnts, -1, 1, -1)
    cm = cv2.erode(cm, np.ones((3, 3), np.uint8))
    if cm.sum() > .93 * W * H:  # basically full-bleed
        return split(path, accent, 'full', fill, min_area, detect, outline, roi)
    ca = cv2.GaussianBlur(cm.astype(np.float32), (5, 5), 0)
    ys, xs = np.where(cm > 0)
    x0, y0, x1, y1 = xs.min(), ys.min(), xs.max() + 1, ys.max() + 1
    card_rgba = np.dstack([clean, (ca * 255).astype(np.uint8)])[y0:y1, x0:x1]
    st = big[30:260]
    rep = np.concatenate([st, st[::-1]] * 9)[:H]
    return dict(paper=Image.fromarray(rep), card=Image.fromarray(card_rgba, 'RGBA'), cx0=int(x0), cy0=int(y0),
                objs=[dict(o, x=o['x'] - int(x0), y=o['y'] - int(y0)) for o in objs], layout='card')
