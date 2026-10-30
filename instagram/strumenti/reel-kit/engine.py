"""Inkasa Reel Kit — renders a 1080x1920 animated reel from a JSON config.

usage:
  python3 engine.py reel.json                 -> renders MP4
  python3 engine.py reel.json --preview 1.5 6 -> saves preview JPGs at those seconds
  python3 engine.py reel.json --sheet         -> contact sheet of one frame per scene
See README.md for every option.
"""
import json, math, os, re, subprocess, sys, wave
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont
from layers import split, hex2rgb

HERE = os.path.dirname(os.path.abspath(__file__))
W, H = 1080, 1920
PAD = 360
FONTS = {
    'sans': ('InterDisplay-ExtraBold.otf', 'Inter-Black.otf', 'InterDisplay-Medium.otf'),
    'serif': ('Caladea-Bold.ttf', 'Caladea-BoldItalic.ttf', 'Caladea-Bold.ttf'),
    'cormorant': ('CormorantGaramond-SemiBold.ttf', 'CormorantGaramond-SemiBoldItalic.ttf', 'CormorantGaramond-Medium.ttf'),
    'mono': ('DejaVuSansMono-Bold.ttf', 'DejaVuSansMono-Bold.ttf', 'DejaVuSansMono-Bold.ttf'),
}


# ---------------- easing ----------------
def clamp(x, a=0., b=1.): return max(a, min(b, x))
def eob(x, s=1.7): x = clamp(x) - 1; return x * x * ((s + 1) * x + s) + 1
def eoc(x): x = clamp(x); return 1 - (1 - x) ** 3
def bounce(x):
    x = clamp(x); n, d = 7.5625, 2.75
    if x < 1 / d: return n * x * x
    if x < 2 / d: x -= 1.5 / d; return n * x * x + .75
    if x < 2.5 / d: x -= 2.25 / d; return n * x * x + .9375
    x -= 2.625 / d; return n * x * x + .984375


def set_alpha(im, a):
    if a >= 1: return im
    im = im.copy(); im.putalpha(im.getchannel('A').point(lambda v: int(v * a))); return im


def paste_scaled(frame, im, cx, cy, sc, rot=0, alpha=1.0):
    if sc <= .01 or alpha <= 0: return
    im2 = im.resize((max(1, int(im.width * sc)), max(1, int(im.height * sc))), Image.BICUBIC)
    if rot: im2 = im2.rotate(rot, Image.BICUBIC, expand=True)
    im2 = set_alpha(im2, alpha)
    frame.alpha_composite(im2, (int(cx - im2.width / 2), int(cy - im2.height / 2)))


def paste_any(dst, src, x, y):
    sx, sy = max(0, -x), max(0, -y)
    if sx >= src.width or sy >= src.height: return
    src = src.crop((sx, sy, min(src.width, sx + dst.width - max(0, x)), min(src.height, sy + dst.height - max(0, y))))
    if src.width > 0 and src.height > 0: dst.alpha_composite(src, (max(0, x), max(0, y)))


def with_shadow(im, off=(8, 14), blur=10, op=.38, pad=40):
    c = Image.new('RGBA', (im.width + 2 * pad, im.height + 2 * pad), (0, 0, 0, 0))
    sh = Image.new('RGBA', im.size, (20, 15, 10, 255)); sh.putalpha(im.getchannel('A').point(lambda p: int(p * op)))
    c.alpha_composite(sh, (pad + off[0], pad + off[1])); c = c.filter(ImageFilter.GaussianBlur(blur))
    c.alpha_composite(im, (pad, pad)); return c, pad


class Reel:
    def __init__(self, cfg, base):
        self.cfg, self.base = cfg, base
        pal = cfg.get('palette', {})
        self.ACC = hex2rgb(pal.get('accent', '#B8853C'))
        self.INK = hex2rgb(pal.get('ink', '#111111'))
        self.PAPER = hex2rgb(pal.get('paper', '#F2ECE0'))
        self.CAPC = hex2rgb(pal.get('caption', '#FFFFFF'))
        self.ONACC = hex2rgb(pal.get('on_accent', '#FFFFFF'))
        fam = FONTS[cfg.get('font', 'sans')]
        self.fpath = [os.path.join(HERE, 'fonts', f) for f in fam]
        self.text_style = cfg.get('text_style', 'box')        # box | marker | underline | sticker
        self.caption_style = cfg.get('caption_style', 'stroke')  # stroke | pill | plain
        self.badge_style = cfg.get('badge_style', 'square')    # square | circle | outline | none
        self.fps = cfg.get('fps', 30)
        self.scenes, t = [], 0.0
        for sc in cfg['scenes']:
            sc = dict(sc); sc['t0'] = t; t += sc['dur']; sc['t1'] = t
            self.scenes.append(sc)
        self.dur = t
        self.layers = {}
        self.blocks, self.pops, self.ticks = [], [], []
        self.logo = Image.open(os.path.join(base, cfg.get('logo', os.path.join(HERE, 'assets/logo.png')))).convert('RGBA')
        for sc in self.scenes: self._prep(sc)
        self.grain = [Image.fromarray((np.random.RandomState(i).rand(H // 2, W // 2) * 255).astype('uint8')).resize((W, H)) for i in range(4)] if cfg.get('grain', True) else None

    # ---------- fonts / text ----------
    def font(self, size, kind=0): return ImageFont.truetype(self.fpath[kind], size)

    def word_img(self, text, size, hl, role):
        caption = role == 'caption'
        st = self.text_style
        if role == 'label': text = '\u200a'.join(text.upper())
        f = self.font(size, 1 if (hl and st == 'accent') else 0)
        bb = f.getbbox(text); hb = f.getbbox('Hg')
        tw, th = bb[2] - bb[0], hb[3] - hb[1]
        stroke = int(size * .09) if (caption and self.caption_style == 'stroke') else 0
        col = self.CAPC if (caption and self.caption_style not in ('plain', 'card')) else self.INK
        if role == 'pill': col = self.ONACC
        if role == 'label': col = tuple(int(c * .6 + p * .4) for c, p in zip(self.INK, self.PAPER))
        if hl and st in ('box', 'sticker'):
            padx, pady = int(size * .28), int(size * .16)
        else:
            padx, pady = stroke + 2, stroke + int(size * .08)
        w, h = tw + 2 * padx, th + 2 * pady + int(size * .12)
        im = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
        tx, ty = padx - bb[0], pady - hb[1]
        if hl and st == 'box':
            d.rounded_rectangle((0, 0, w - 1, h - 1), radius=int(size * .16), fill=self.ACC + (255,))
            d.text((tx, ty), text, font=f, fill=self.ONACC)
        elif hl and st == 'sticker':
            d.rounded_rectangle((0, 0, w - 1, h - 1), radius=int(size * .12), fill=self.INK + (255,))
            d.text((tx, ty), text, font=f, fill=self.ACC)
            im = im.rotate(-3, Image.BICUBIC, expand=True)
        elif hl and st == 'marker':
            d.rectangle((0, int(h * .45), w, int(h * .92)), fill=self.ACC + (230,))
            d.text((tx, ty), text, font=f, fill=col, stroke_width=stroke, stroke_fill=self.INK)
        elif hl and st == 'underline':
            d.text((tx, ty), text, font=f, fill=col, stroke_width=stroke, stroke_fill=self.INK)
            d.rounded_rectangle((padx, h - int(size * .2), w - padx, h - int(size * .06)), radius=6, fill=self.ACC + (255,))
        else:
            if hl: col = self.ACC
            d.text((tx, ty), text, font=f, fill=col, stroke_width=stroke, stroke_fill=self.INK)
        if role == 'label' or (caption and self.caption_style == 'card'): return im
        if caption and self.caption_style == 'pill' and not hl:
            p = Image.new('RGBA', (w + 24, h + 8), (0, 0, 0, 0))
            ImageDraw.Draw(p).rounded_rectangle((0, 0, w + 23, h + 7), radius=int(size * .2), fill=self.INK + (215,))
            p.alpha_composite(im, (12, 4)); im = p
        return im

    def block(self, text_lines, size, cy, t0, t1, role='title', step=.11):
        lh = int(size * 1.22); items = []; ext = []
        y0 = cy - lh * len(text_lines) / 2
        n = 0
        for li, line in enumerate(text_lines):
            toks = re.findall(r'\[[^\]]+\]|[^ \[\]]+', line)
            for attempt in range(2):
                ims = [self.word_img(t.strip('[]'), size, t.startswith('['), role) for t in toks]
                gap = int(size * (.12 if role == 'caption' and self.caption_style == 'stroke' else .24 if role == 'caption' and self.caption_style == 'card' else .26))
                total = sum(i.width for i in ims) + gap * (len(ims) - 1)
                if total <= W - 110: break
                size2 = int(size * (W - 110) / total)
                ims = [self.word_img(t.strip('[]'), size2, t.startswith('['), role) for t in toks]
                gap = int(size2 * .2); total = sum(i.width for i in ims) + gap * (len(ims) - 1); break
            x = (W - total) / 2
            if role == 'caption' and self.caption_style == 'card':
                hh = max(i.height for i in ims); ly = y0 + li * lh + (lh - hh) / 2
                ext.append((x, x + total, ly, ly + hh, size))
            for im in ims:
                items.append((im, x, y0 + li * lh + (lh - im.height) / 2, t0 + n * step)); x += im.width + gap; n += 1
        if ext:  # one white card behind the whole block
            sz = min(e[4] for e in ext); px, py = int(sz * .55), int(sz * .32)
            x0, x1 = min(e[0] for e in ext) - px, max(e[1] for e in ext) + px
            y0_, y1_ = min(e[2] for e in ext) - py, max(e[3] for e in ext) + py
            cw, ch = int(x1 - x0), int(y1_ - y0_); r = int(min(ch, sz * 1.6) * .32)
            bg = Image.new('RGBA', (cw + 60, ch + 70), (0, 0, 0, 0))
            sh = Image.new('RGBA', bg.size, (0, 0, 0, 0))
            ImageDraw.Draw(sh).rounded_rectangle((30, 42, 30 + cw, 42 + ch), radius=r, fill=(60, 40, 20, 70))
            bg.alpha_composite(sh.filter(ImageFilter.GaussianBlur(14)))
            ImageDraw.Draw(bg).rounded_rectangle((30, 30, 30 + cw, 30 + ch), radius=r, fill=(255, 255, 255, 250))
            items.insert(0, (bg, x0 - 30, y0_ - 30, t0 - .06))
        self.ticks += [it[3] for it in items]
        self.blocks.append(dict(items=items, t1=t1))

    def draw_blocks(self, frame, t):
        for b in self.blocks:
            ok = 1.0
            if b['t1'] is not None:
                ok = 1 - clamp((t - b['t1']) / .18)
                if ok <= 0: continue
            if self.cfg.get('text_anim') == 'fade':
                if b['t1'] is not None: ok = 1 - clamp((t - b['t1']) / .35)
                for im, x, y, ts in b['items']:
                    k = (t - ts) / .55
                    if k <= 0: continue
                    frame.alpha_composite(set_alpha(im, eoc(k) * ok), (int(x), int(y + (1 - eoc(k)) * 26)))
                continue
            for im, x, y, ts in b['items']:
                k = (t - ts) / .2
                if k <= 0: continue
                sc = .6 + .4 * eob(k, 2.2)
                a = clamp(k * 1.6) * ok
                im2 = im.resize((max(1, int(im.width * sc)), max(1, int(im.height * sc))), Image.BILINEAR) if sc != 1 else im
                frame.alpha_composite(set_alpha(im2, a), (int(x + (im.width - im2.width) / 2), int(y + (im.height - im2.height) / 2 - (1 - ok) * 20)))

    def badge(self, num, size=128):
        im = Image.new('RGBA', (size, size), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
        bs = self.badge_style
        if bs == 'circle': d.ellipse((0, 0, size - 1, size - 1), fill=self.ACC + (255,)); col = self.ONACC
        elif bs == 'outline': d.rounded_rectangle((4, 4, size - 5, size - 5), radius=18, outline=self.ACC + (255,), width=8, fill=self.PAPER + (255,)); col = self.INK
        else: d.rounded_rectangle((0, 0, size - 1, size - 1), radius=18, fill=self.ACC + (255,)); col = self.ONACC
        f = self.font(int(size * .7), 1); s = str(num); bb = f.getbbox(s)
        d.text(((size - (bb[2] - bb[0])) / 2 - bb[0], (size - (bb[3] - bb[1])) / 2 - bb[1]), s, font=f, fill=col)
        return im

    def logo_pill(self, name, sub):
        lg = self.logo.resize((150, int(self.logo.height * 150 / self.logo.width)), Image.LANCZOS)
        f1, f2 = self.font(54, 1), self.font(26)
        tw = max(f1.getlength(name), f2.getlength(sub))
        w, h = int(60 + lg.width + 26 + tw + 60), 150
        im = Image.new('RGBA', (w + 20, h + 24), (0, 0, 0, 0))
        sh = Image.new('RGBA', im.size, (0, 0, 0, 0))
        ImageDraw.Draw(sh).rounded_rectangle((10, 18, w + 10, h + 18), radius=h // 2, fill=(0, 0, 0, 90))
        im.alpha_composite(sh.filter(ImageFilter.GaussianBlur(8)))
        d = ImageDraw.Draw(im)
        d.rounded_rectangle((10, 6, w + 10, h + 6), radius=h // 2, fill=(255, 255, 255, 255))
        im.alpha_composite(lg, (70, 6 + (h - lg.height) // 2))
        x = 70 + lg.width + 26
        d.text((x, 28), name, font=f1, fill=self.INK); d.text((x + 2, 96), sub, font=f2, fill=self.ACC)
        return im

    def pill(self, text, size=40, fill=None, col=None):
        f = self.font(size); tw = int(f.getlength(text)); hb = f.getbbox('Hg')
        hh = hb[3] - hb[1] + int(size * .9)
        im = Image.new('RGBA', (tw + int(size * 1.4), hh), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
        d.rounded_rectangle((0, 0, im.width - 1, hh - 1), radius=hh // 2, fill=(fill or self.INK) + (255,))
        d.text((int(size * .7), (hh - (hb[3] - hb[1])) / 2 - hb[1]), text, font=f, fill=col or (255, 255, 255))
        return im

    def star(self, size, col):
        im = Image.new('RGBA', (size, size), (0, 0, 0, 0)); d = ImageDraw.Draw(im); c = size / 2; q = size * .12
        d.polygon([(c, 0), (c + q, c - q), (size, c), (c + q, c + q), (c, size), (c - q, c + q), (0, c), (c - q, c - q)], fill=col + (255,))
        return im

    # ---------- scene preparation ----------
    def _prep(self, sc):
        saved = (self.text_style, self.caption_style, self.badge_style, self.fpath)
        self.text_style = sc.get('text_style', self.text_style); self.caption_style = sc.get('caption_style', self.caption_style)
        self.badge_style = sc.get('badge_style', self.badge_style)
        if sc.get('font'): self.fpath = [os.path.join(HERE, 'fonts', f) for f in FONTS[sc['font']]]
        try:
            self._prep2(sc)
        finally:
            self.text_style, self.caption_style, self.badge_style, self.fpath = saved

    def _prep2(self, sc):
        oa = sc.get('objects', {}).get('anim', 'none')
        fill = sc.get('objects', {}).get('fill') or ('clone' if oa == 'drop' else 'inpaint')
        ol = sc.get('objects', {}).get('outline', self.cfg.get('outline', True))
        roi = sc.get('objects', {}).get('roi')
        key = (sc['img'], sc.get('layout', 'card'), fill, oa != 'none', ol, str(roi))
        if key not in self.layers:
            L = split(os.path.join(self.base, sc['img']), '#%02x%02x%02x' % self.ACC, sc.get('layout', 'card'), fill, detect=oa != 'none', outline=ol, roi=roi)
            P = {}
            P['layout'] = L['layout']
            if L['layout'] == 'card':
                P['paper'] = L['paper'].convert('RGBA') if not self.cfg.get('paper_fill') else Image.new('RGBA', (W, H), self.PAPER + (255,))
                P['card_alpha'] = L['card'].getchannel('A').filter(ImageFilter.MinFilter(25))
                P['card'], cp = with_shadow(L['card'], off=(10, 20), blur=16, op=.35, pad=60)
            else:
                P['paper'] = Image.new('RGBA', (W, H), self.PAPER + (255,))
                P['card_alpha'] = L['card'].getchannel('A'); P['card'], cp = L['card'], 0
            P['cpad'] = cp; P['cx0'], P['cy0'] = L['cx0'] - cp, L['cy0'] - cp
            P['objs'] = []
            for o in L['objs']:
                im, p = with_shadow(o['img'], off=(5, 9), blur=6, op=.4, pad=24)
                P['objs'].append(dict(img=im, x=o['x'] + cp - p, y=o['y'] + cp - p, w=o['w'], h=o['h'], p=p))
            self.layers[key] = P
        sc['L'] = self.layers[key]
        # texts
        t0 = sc['t0']
        ty = sc.get('title_y', 360)
        if sc.get('badge'):
            sc['badge_img'] = self.badge(sc['badge']); self.pops.append(t0 + .12)
        if sc.get('title'):
            self.block(sc['title'], sc.get('title_size', 74), ty, t0 + (.3 if sc.get('badge') else .35), sc['t1'] - .22, 'title', .09)
        for tx in sc.get('texts', []):
            role = tx.get('role', 'caption')
            until = tx.get('until')
            self.block(tx['text'] if isinstance(tx['text'], list) else [tx['text']], tx.get('size', 80 if role == 'caption' else 74),
                       tx['y'], t0 + tx.get('at', .9), (t0 + until) if until is not None else (None if sc is self.scenes[-1] else sc['t1'] - .22),
                       role, tx.get('step', .14 if role == 'caption' else .11))
        for ex in sc.get('extras', []):
            if ex['type'] == 'logo_pill':
                ex['img'] = self.logo_pill(ex.get('name', 'INKASA'), ex.get('sub', 'PROPERTY MANAGEMENT')); self.pops.append(t0 + ex.get('at', 3))
            elif ex['type'] == 'pill':
                ex['img'] = self.pill(ex['text'], ex.get('size', 40), hex2rgb(ex['fill']) if ex.get('fill') else None); self.pops.append(t0 + ex.get('at', 3))
            elif ex['type'] == 'logo':
                lw = ex.get('w', 300); ex['img'] = self.logo.resize((lw, int(self.logo.height * lw / self.logo.width)), Image.LANCZOS)
            elif ex['type'] == 'stamp':
                f = self.font(ex.get('size', 92), 1)
                im = Image.new('RGBA', (900, 300), (0, 0, 0, 0))
                ImageDraw.Draw(im).text((10, 10), ex['text'], font=f, fill=hex2rgb(ex['color']) if ex.get('color') else self.INK)
                ex['img'] = im.crop(im.getbbox()); self.pops.append(t0 + ex.get('at', 1.1))
            elif ex['type'] == 'glow':
                r = ex.get('radius', 120); P_ = 170
                g = Image.new('L', (2 * r + 2 * P_, 2 * r + 2 * P_), 0)
                ImageDraw.Draw(g).ellipse((P_, P_, P_ + 2 * r, P_ + 2 * r), fill=255); g = g.filter(ImageFilter.GaussianBlur(r * .45))
                c = hex2rgb(ex.get('color', '#FFFFFF'))
                ex['img'] = Image.merge('RGBA', [Image.new('L', g.size, v) for v in c] + [g])
                if ex.get('pos') == 'auto_object' and sc['L']['objs']:
                    o = sc['L']['objs'][0]; ex['cpos'] = (o['x'] + o['p'] + o['w'] / 2, o['y'] + o['p'] + o['h'] / 2)
                elif ex.get('pos', 'auto') in ('auto', 'auto_object'):
                    import cv2
                    a = cv2.GaussianBlur(np.array(sc['L']['card'].convert('L')).astype(np.float32), (0, 0), 15)
                    m = 140; sub = a[m:a.shape[0] // 3, m:a.shape[1] - m]
                    y, x = np.unravel_index(np.argmax(sub), sub.shape); ex['cpos'] = (x + m, y + m)
                else:
                    ex['cpos'] = (ex['pos'][0] - sc['L']['cx0'], ex['pos'][1] - sc['L']['cy0'])
            elif ex['type'] == 'sparkles':
                rs = np.random.RandomState(ex.get('seed', 3))
                ex['stars'] = [(self.star(int(rs.randint(40, 75)), self.ACC if i % 2 == 0 else self.INK), int(rs.randint(90, 990)), int(rs.randint(560, 1700)), rs.rand() * 1.5) for i in range(ex.get('n', 5))]

    # ---------- object animation ----------
    def put(self, canvas, o, ang=0, dx=0, dy=0, sc=1.0, alpha=1.0, piv=(.5, .5), img=None):
        im = img or o['img']
        if alpha <= 0 or sc <= .02: return
        if sc != 1: im = im.resize((max(1, int(im.width * sc)), max(1, int(im.height * sc))), Image.BICUBIC)
        px = o['p'] * sc + piv[0] * o['w'] * sc; py = o['p'] * sc + piv[1] * o['h'] * sc
        ax = o['x'] + o['p'] + piv[0] * o['w']; ay = o['y'] + o['p'] + piv[1] * o['h']
        if ang:
            w0, h0 = im.width, im.height
            im = im.rotate(ang, Image.BICUBIC, expand=True)
            a = math.radians(ang); vx, vy = px - w0 / 2, py - h0 / 2
            px = im.width / 2 + vx * math.cos(a) + vy * math.sin(a); py = im.height / 2 - vx * math.sin(a) + vy * math.cos(a)
        canvas.alpha_composite(set_alpha(im, alpha), (int(ax - px + dx), int(ay - py + dy)))

    def anim_objects(self, sc, cv, lt, off):
        O = sc.get('objects', {}); kind = O.get('anim', 'none')
        if kind == 'none': return
        A = O.get('amp', 1.0); piv = tuple(O.get('pivot', [.5, .5])); stg = O.get('stagger', .22)
        only = O.get('only')
        stamps = [e for e in sc.get('extras', []) if e['type'] == 'stamp']
        for i, o in enumerate(sc['L']['objs']):
            if only is not None and i not in only:
                o2 = dict(o, x=o['x'] + off, y=o['y'] + off); self.put(cv, o2); continue
            o = dict(o, x=o['x'] + off, y=o['y'] + off)
            img = None
            for e in stamps:
                if e.get('obj', 0) == i:
                    kt = (lt - e.get('at', 1.1)) / .3
                    if kt > 0:
                        img = (img or o['img']).copy(); s = eob(kt, 2.2) * e.get('scale', .95)
                        t = e['img'].resize((max(1, int(e['img'].width * s)), max(1, int(e['img'].height * s))), Image.BICUBIC).rotate(e.get('rot', -12), Image.BICUBIC, expand=True)
                        px, py = e.get('pos', [.5, .6])
                        img.alpha_composite(t, (int(o['p'] + o['w'] * px - t.width / 2), int(o['p'] + o['h'] * py - t.height / 2)))
            ph = i * 1.3
            if kind == 'swing':
                self.put(cv, o, ang=A * (9 * math.sin(2.3 * lt + ph) * math.exp(-.3 * lt) + 2.5 * math.sin(1.4 * lt + ph)), piv=piv, img=img)
            elif kind == 'jingle':
                env = math.exp(-3.2 * ((lt + i * .3) % 1.4))
                self.put(cv, o, ang=A * (14 * math.sin(lt * 11) * env + 3 * math.sin(lt * 2)), piv=piv, img=img)
            elif kind == 'buzz':
                p_ = (lt + i * .2) % 1.3; b = p_ < .45 and lt > .5
                self.put(cv, o, ang=A * 1.6 * math.sin(lt * 70) if b else 0, dx=A * 6 * math.sin(lt * 95) if b else 0, img=img)
            elif kind == 'drop':
                kd = (lt - .25 - i * stg) / .75
                self.put(cv, o, ang=(1 - eoc(kd)) * -25 * A + 2 * math.sin(lt * 3) * clamp(kd), dy=-(1 - bounce(kd)) * 520, piv=piv, alpha=clamp(kd * 5), img=img)
            elif kind == 'pop':
                kp = (lt - .35 - i * stg) / .3
                if kp > 0: self.put(cv, o, ang=(1 - eoc(kp)) * 18 * (1 if i % 2 else -1), sc=1.6 - .6 * eob(kp, 2.4), alpha=clamp(kp * 3), piv=piv, img=img)
            elif kind == 'slide_in':
                kp = (lt - .3 - i * stg) / .55; side = -1 if (o['x'] + o['w'] / 2) < cv.width / 2 else 1
                self.put(cv, o, dx=side * (1 - eob(kp, 1.4)) * 750, ang=(1 - eoc(kp)) * 12 * side, alpha=clamp(kp * 4), img=img)
            elif kind == 'spin':
                kp = (lt - .3 - i * stg) / .7
                self.put(cv, o, ang=(1 - eoc(kp)) * 360 + 3 * math.sin(lt * 1.5 + ph), sc=.4 + .6 * eob(kp, 1.8), alpha=clamp(kp * 4), img=img)
            elif kind == 'float':
                self.put(cv, o, dy=A * 12 * math.sin(1.8 * lt + ph), ang=A * 3 * math.sin(1.3 * lt + ph), img=img)
            elif kind == 'pulse':
                self.put(cv, o, sc=1 + A * .06 * (math.sin(4 * lt + ph) * .5 + .5), img=img)

    # ---------- frame ----------
    def scene_frame(self, sc, lt):
        L = sc['L']
        fr = L['paper'].copy()
        off = PAD
        cv = Image.new('RGBA', (L['card'].width + 2 * PAD, L['card'].height + 2 * PAD), (0, 0, 0, 0))
        cv.alpha_composite(L['card'], (PAD, PAD))
        for ex in sc.get('extras', []):
            if ex['type'] == 'glow':
                fl = ex.get('strength', .45)
                if ex.get('flicker', True): fl = fl + .2 * math.sin(lt * 23) * math.sin(lt * 7.3) + (.25 if (lt % 1.7) < .08 else 0)
                else: fl = fl * (.7 + .3 * math.sin(lt * 4))
                gl = Image.new('RGBA', cv.size, (0, 0, 0, 0))
                gl.alpha_composite(set_alpha(ex['img'], clamp(fl)), (int(PAD + ex['cpos'][0] - ex['img'].width / 2), int(PAD + ex['cpos'][1] - ex['img'].height / 2)))
                ca = Image.new('L', cv.size, 0); ca.paste(L['card_alpha'], (PAD + L['cpad'], PAD + L['cpad']))
                gl.putalpha(Image.fromarray((np.array(gl.getchannel('A')).astype(np.uint16) * np.array(ca) // 255).astype(np.uint8)))
                cv.alpha_composite(gl)
        if sc.get('objects', {}).get('anim', 'none') != 'none':
            self.anim_objects(sc, cv, lt, off)
        entry = sc.get('entry', 'slap'); idle = sc.get('idle', 'float')
        ke = lt / sc.get('entry_dur', .5)
        if L['layout'] == 'full':
            z = 1 + (1 - eob(ke, 1.4)) * .12 if entry != 'none' else 1
            z *= 1 + .05 * lt / sc['dur'] if idle != 'still' else 1
            w, h = int(cv.width * z), int(cv.height * z)
            cv2_ = cv.resize((w, h), Image.BILINEAR)
            fr2 = Image.new('RGBA', (W, H), self.PAPER + (255,))
            cx, cy = w / 2, h / 2
            fr2.alpha_composite(cv2_.crop((int(cx - W / 2), int(cy - H / 2), int(cx - W / 2) + W, int(cy - H / 2) + H)))
            return fr2
        e = eob(ke, 1.25)
        tx = ty = rot = 0.0; scl = 1.0
        if entry == 'slap': ty = (1 - e) * 340; rot = (1 - e) * 7; scl = 1 + (1 - eoc(ke)) * .06
        elif entry == 'slide_left': tx = (1 - e) * -1100; rot = (1 - e) * -10
        elif entry == 'slide_right': tx = (1 - e) * 1100; rot = (1 - e) * 10
        elif entry == 'drop': ty = -(1 - bounce(ke)) * 1500; rot = (1 - eoc(ke)) * -5
        elif entry == 'zoom': scl = .3 + .7 * eob(ke, 1.6); rot = (1 - e) * -14
        elif entry == 'spin': rot = (1 - eoc(ke)) * 180; scl = .5 + .5 * eob(ke, 1.5)
        elif entry == 'rise': ty = (1 - eoc(ke)) * 900
        if idle == 'float': ty += 5 * math.sin(1.6 * lt); rot += .7 * math.sin(1.05 * lt + .4)
        elif idle == 'sway': rot += 1.6 * math.sin(1.2 * lt)
        elif idle == 'breathe': scl *= 1 + .015 * math.sin(2 * lt)
        elif idle == 'drift': tx += 14 * math.sin(.9 * lt); ty += 8 * math.sin(1.3 * lt)
        if scl != 1: cv = cv.resize((max(1, int(cv.width * scl)), max(1, int(cv.height * scl))), Image.BILINEAR)
        if abs(rot) > .01: cv = cv.rotate(rot, Image.BILINEAR)
        base_w, base_h = L['card'].width + 2 * PAD, L['card'].height + 2 * PAD
        x = L['cx0'] - PAD - (cv.width - base_w) / 2 + tx
        y = L['cy0'] - PAD - (cv.height - base_h) / 2 + ty
        paste_any(fr, cv, int(x), int(y))
        return fr

    def render(self, t):
        sc = next((s for s in self.scenes if s['t0'] <= t < s['t1']), self.scenes[-1])
        lt = t - sc['t0']
        frame = self.base_frame(sc, lt)
        td = self.cfg.get('transition_dur', .6)
        i = self.scenes.index(sc)
        if self.cfg.get('transition') == 'fade' and i > 0 and lt < td:
            pv = self.scenes[i - 1]
            frame = Image.blend(self.base_frame(pv, pv['dur'] + lt), frame, eoc(lt / td) if lt > 0 else 0)
        self.draw_blocks(frame, t)
        if self.grain:
            g = self.grain[int(t * self.fps) % 4]
            frame = Image.composite(frame, Image.new('RGBA', (W, H), (40, 30, 20, 255)), g.point(lambda p: 255 if p > 14 else 235))
        return frame.convert('RGB')

    def base_frame(self, sc, lt):
        frame = self.scene_frame(sc, lt)
        if sc.get('badge'):
            kb = (lt - .12) / .28
            if kb > 0: paste_scaled(frame, sc['badge_img'], W / 2, sc.get('title_y', 360) - 150, eob(kb, 2.6), rot=(1 - clamp(kb)) * 25)
        for ex in sc.get('extras', []):
            k = (lt - ex.get('at', 0)) / .35
            if ex['type'] in ('logo_pill', 'pill') and k > 0:
                paste_scaled(frame, ex['img'], W / 2, ex.get('y', 1260), eob(k, 2))
            elif ex['type'] == 'sparkles':
                for st, x, y, ph in ex['stars']:
                    s = .55 + .45 * math.sin((lt + ph) * 5)
                    paste_scaled(frame, st, x, y, clamp((lt - ph * .5) / .3) * s, rot=lt * 30)
            elif ex['type'] == 'dust':
                rs = np.random.RandomState(7); d = ImageDraw.Draw(frame)
                for i in range(ex.get('n', 40)):
                    x0, y0, sp = rs.randint(0, W), rs.randint(400, H), 20 + rs.rand() * 40
                    y = (y0 - lt * sp) % H; x = x0 + 10 * math.sin(lt + i); r = 1.5 + rs.rand() * 2.5
                    d.ellipse((x - r, y - r, x + r, y + r), fill=(255, 255, 255, int(120 + 100 * rs.rand())))
            elif ex['type'] == 'logo' and k > 0:
                frame.alpha_composite(set_alpha(ex['img'], eoc(k / 1.6)), (int((W - ex['img'].width) / 2), int(ex.get('y', 260) - ex['img'].height / 2 + (1 - eoc(k / 1.6)) * 20)))
            elif ex['type'] == 'rule' and k > 0:
                L_ = ex.get('w', 120) * eoc(k / 1.8); y = ex.get('y', 300)
                ImageDraw.Draw(frame).rectangle((W / 2 - L_ / 2, y, W / 2 + L_ / 2, y + ex.get('h', 3)), fill=self.ACC + (255,))
        return frame

    # ---------- audio ----------
    def audio(self, path):
        sr = 44100; n = int(self.dur * sr) + sr; out = np.zeros(n); rng = np.random.RandomState(1)
        sfx = self.cfg.get('sfx', {})
        def add(sig, t, g):
            i = max(0, int(t * sr)); j = min(n, i + len(sig)); out[i:j] += sig[:j - i] * g
        L = int(.45 * sr); tt = np.arange(L) / sr
        spec = np.fft.rfft(rng.randn(L)); fr = np.fft.rfftfreq(L, 1 / sr)
        spec *= np.exp(-((np.log(fr + 1) - np.log(1800)) ** 2) / 1.2)
        wh = np.fft.irfft(spec, L); wh /= np.abs(wh).max(); wh *= np.sin(np.pi * np.clip(tt / .45, 0, 1)) ** 2 * np.exp(-tt * 2)
        if sfx.get('whoosh', True):
            for s in self.scenes[1:]: add(wh, s['t0'] - .2, .45)
        L = int(.12 * sr); tt = np.arange(L) / sr
        pop = np.sin(2 * np.pi * np.cumsum(900 * np.exp(-tt * 18) + 280) / sr) * np.exp(-tt * 38)
        if sfx.get('pop', True):
            for t in self.pops: add(pop, t, .55)
        L = int(.03 * sr); tt = np.arange(L) / sr
        tick = np.convolve(rng.randn(L) * np.exp(-tt * 260), np.ones(6) / 6, 'same')
        if sfx.get('ticks', True):
            for t in self.ticks: add(tick, t, .22)
        L = int(.55 * sr); tt = np.arange(L) / sr
        rip = np.convolve(rng.randn(L) * (rng.rand(L) > .55) * np.exp(-tt * 4) * np.clip(tt / .03, 0, 1), np.ones(3) / 3, 'same')
        if sfx.get('rip', True):
            add(rip, .02, .35); add(rip, self.scenes[-1]['t0'] - .05, .3)
        out = np.tanh(out[:int(self.dur * sr)] * 1.2) * .8
        with wave.open(path, 'wb') as w:
            w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr); w.writeframes((out * 32767).astype('<i2').tobytes())


def main():
    cfgp = sys.argv[1]; base = os.path.dirname(os.path.abspath(cfgp))
    cfg = json.load(open(cfgp)); R = Reel(cfg, base)
    out = os.path.join(base, cfg.get('out', 'reel.mp4'))
    if '--preview' in sys.argv:
        for t in sys.argv[sys.argv.index('--preview') + 1:]:
            R.render(float(t)).save(os.path.join(base, f'preview_{float(t):05.2f}.jpg'), quality=85)
        return
    if '--sheet' in sys.argv:
        ims = [R.render(s['t0'] + min(s['dur'] * .7, 2.8)).resize((270, 480)) for s in R.scenes]
        g = Image.new('RGB', (270 * len(ims), 480)); [g.paste(im, (i * 270, 0)) for i, im in enumerate(ims)]
        g.save(os.path.join(base, 'sheet.jpg'), quality=85); return
    wav = out + '.wav'; R.audio(wav)
    audio_in = ['-i', os.path.join(base, cfg['voice'])] if cfg.get('voice') else []
    amix = ['-filter_complex', '[1:a][2:a]amix=inputs=2:duration=first:weights=1 1[a]', '-map', '0:v', '-map', '[a]'] if audio_in else []
    p = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(R.fps), '-i', '-',
                          '-i', wav] + audio_in + amix + ['-c:v', 'libx264', '-preset', 'veryfast', '-crf', '19', '-pix_fmt', 'yuv420p', '-c:a', 'aac',
                          '-b:a', '160k', '-shortest', '-movflags', '+faststart', out], stdin=subprocess.PIPE)
    N = int(R.dur * R.fps)
    for i in range(N):
        p.stdin.write(R.render(i / R.fps).tobytes())
        if i % 150 == 0: print(f'{i}/{N}', flush=True)
    p.stdin.close(); p.wait(); os.remove(wav); print('done ->', out)


if __name__ == '__main__':
    main()
