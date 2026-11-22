# -*- coding: utf-8 -*-
"""Smartline Point Cleaning Hub Ltd — social media pack.

    python make_social.py            # -> social/ (gitignored), plus social/00-overview.jpg

Branded templates in the website's v7 "Bright" look (sky-white grounds, the logo's navy and
indigo, the swoosh gradient, a water-blue accent, bubbles and sparkle glints), set in Mona Sans
beside the client's own vector logo. Every template is filled from the same data as the
website (site_layout / site_content), so the copy matches the site word for word.

Rules carried over from the website (CLAUDE.md):
  - no people photographed: no fake personnel, no faces
  - stock photos illustrate a service; nothing says "our job", "our team" or "our client's site"
  - no metrics, counters or "trusted by N" figures; no testimonials
  - fumigation appears nowhere
Formats: 1080x1080 feed, 1080x1350 carousel, 1080x1920 stories/status, 1200x630 link posts,
covers and profile images. Captions and a four-week calendar go to social/CAPTIONS.md.
"""
import math
import os
import re
import shutil

import pymupdf as fitz  # renders the SVG logo, seal and icons
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

import site_content as C
import site_layout as L

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "social")
IMG = os.path.join(ROOT, "site", "assets", "img")
SRC = os.path.join(ROOT, "media", "all")
CACHE = os.path.join(ROOT, "build_cache")
K = 2  # supersampling: everything is drawn at 2x and downsampled once

NAVY = (16, 18, 56); NAVY9 = (10, 11, 38); INDIGO = (47, 36, 131); INDIGO6 = (62, 49, 166)
TEXT = (21, 22, 46); TEXT2 = (59, 61, 90); MUTED = (92, 94, 126); LINE = (225, 225, 237)
SKY50 = (247, 247, 252); SKY100 = (239, 238, 249); SKY200 = (222, 220, 242)   # v8: indigo-tinted whites
AQUA = INDIGO6; AQUA_INK = INDIGO; WHITE = (255, 255, 255)   # v8 three tones: no separate blue
SUN = (255, 194, 0); AMBER = (248, 149, 26); FLAME = (252, 98, 28); AMBER_INK = (176, 78, 8)
SWOOSH = [(0, SUN), (.46, AMBER), (1, FLAME)]
DEEP = [(0, (240, 138, 12)), (.52, (234, 90, 12)), (1, (194, 65, 12))]
FRESH = [(0, INDIGO6), (.45, INDIGO), (1, NAVY)]

SITE = C.DOMAIN
PHONE = C.PHONE

SERVICE_PHOTO = {  # file in media/all (full resolution), or img:<key> = largest built WebP
    "Commercial cleaning": "unsplash-pYlBAu3de0w.jpg",
    "Office carpet cleaning": "img:svc-carpet",
    "School cleaning": "img:svc-school",
    "Church cleaning": "img:g-church",
    "Residential cleaning": "img:svc-residential",
    "Apartment cleaning": "unsplash-ooDvIpnXkwo.jpg",
    "Move in / move out cleaning": "img:svc-move",
    "Sofa set & upholstery cleaning": "img:g-upholstery",
    "Toilet bowl & sink cleaning": "img:svc-washroom",
    "Post-construction cleaning": "img:g-debris",
    "Deep cleaning": "img:svc-deep",
    "One-time cleaning": "img:svc-onetime",
    "Landscaping": "unsplash-BoVg3wUOJ_g.jpg",
}
GROUP_ICON = {"Commercial & institutional": "building-2", "Homes & apartments": "house",
              "Specialist cleans": "hard-hat", "Outdoor": "sprout"}
GROUP_PHOTO = {"Commercial & institutional": "unsplash-pYlBAu3de0w.jpg", "Homes & apartments": "unsplash-7pvC_d2iXSE.jpg",
               "Specialist cleans": "unsplash-XKLZia7hPYI.jpg", "Outdoor": "unsplash-BoVg3wUOJ_g.jpg"}
REASON_ICON = ["calendar-clock", "badge-check", "users", "wallet", "scan-search", "shield-check"]
TRAINING_ICON = ["messages-square", "wrench", "flask-conical", "shirt", "users", "scale"]
STEPS = [("Site visit", "We see the space before we price it."),
         ("Scope and quote", "Written scope, clear price, agreed schedule."),
         ("Team assigned", "A trained team and a named supervisor."),
         ("Supervised clean", "Checked against the scope on every visit."),
         ("Review", "Regular check-ins; the schedule adjusts with you.")]


# ------------------------------------------------------------------ primitives
def font(kind, size):
    return ImageFont.truetype(os.path.join(CACHE, "mona-%s.ttf" % kind), int(round(size * K)))


def gradient(w, h, stops, angle=100):
    """Linear gradient image (RGB) across w x h at `angle` degrees (CSS convention)."""
    a = math.radians(angle)
    dx, dy = math.sin(a), -math.cos(a)
    ys, xs = np.mgrid[0:h, 0:w].astype(np.float32)
    proj = (xs - w / 2) * dx + (ys - h / 2) * dy
    half = abs(w / 2 * dx) + abs(h / 2 * dy)
    t = np.clip((proj + half) / (2 * half + 1e-6), 0, 1)
    out = np.zeros((h, w, 3), np.float32)
    pos = [p for p, _ in stops]
    for ch in range(3):
        out[..., ch] = np.interp(t, pos, [c[ch] for _, c in stops])
    return Image.fromarray(out.astype(np.uint8), "RGB")


def radial(w, h, cx, cy, rx, ry, color, alpha):
    """A soft radial colour blob as an RGBA layer (cx, cy, rx, ry in px)."""
    ys, xs = np.mgrid[0:h, 0:w].astype(np.float32)
    d = np.sqrt(((xs - cx) / rx) ** 2 + ((ys - cy) / ry) ** 2)
    a = np.clip(1 - d, 0, 1) ** 1.6 * alpha * 255
    layer = np.zeros((h, w, 4), np.uint8)
    layer[..., 0], layer[..., 1], layer[..., 2] = color
    layer[..., 3] = a.astype(np.uint8)
    return Image.fromarray(layer, "RGBA")


def bubble(px):
    """A soap bubble: clear centre, an iridescent rim (aqua -> indigo -> sun), a highlight."""
    s = max(4, int(px))
    ys, xs = np.mgrid[0:s, 0:s].astype(np.float32)
    r = np.sqrt((xs - s / 2) ** 2 + (ys - s / 2) ** 2) / (s / 2)
    img = np.zeros((s, s, 4), np.float32)
    rim = np.clip(1 - np.abs(r - .8) / .2, 0, 1)
    ang = np.arctan2(ys - s / 2, xs - s / 2)
    mix = (np.sin(ang * 1.5) + 1) / 2
    img[..., 0] = 62 * (1 - mix) + 252 * mix
    img[..., 1] = 49 * (1 - mix) + 140 * mix
    img[..., 2] = 166 * (1 - mix) + 40 * mix
    a = rim * .55 + np.clip(1 - r, 0, 1) * .06
    hl = np.sqrt((xs - s * .34) ** 2 + (ys - s * .3) ** 2) / (s * .12)
    hla = np.clip(1 - hl, 0, 1) ** 1.2
    img[..., :3] = img[..., :3] * (1 - hla[..., None]) + 255 * hla[..., None]
    a = np.maximum(a, hla * .95)
    a[r > 1] = 0
    img[..., 3] = a * 255
    return Image.fromarray(img.astype(np.uint8), "RGBA")


SPARK = [(0, -1), (.13, -.13), (1, 0), (.13, .13), (0, 1), (-.13, .13), (-1, 0), (-.13, -.13)]


class Art:
    def __init__(self, w, h, bg=WHITE):
        self.w, self.h = w, h
        self.im = Image.new("RGBA", (w * K, h * K), bg + (255,))
        self.d = ImageDraw.Draw(self.im)

    # geometry in 1x units; everything is multiplied by K internally
    def box(self, b):
        return [int(round(v * K)) for v in b]

    def layer(self, im, xy=(0, 0)):
        self.im.alpha_composite(im, (int(xy[0] * K), int(xy[1] * K)))

    def fresh_bg(self, base_top=SKY50, base_bot=WHITE, aqua=(0.86, 0.0), sun=(0.0, 1.0), strength=1.0):
        W, H = self.w * K, self.h * K
        g = gradient(W, H, [(0, base_top), (1, base_bot)], 180).convert("RGBA")
        g.alpha_composite(radial(W, H, aqua[0] * W, aqua[1] * H, W * .75, H * .65, (164, 157, 235), .34 * strength))
        g.alpha_composite(radial(W, H, sun[0] * W, sun[1] * H, W * .6, H * .5, (255, 194, 0), .22 * strength))
        self.im.alpha_composite(g)
        self.d = ImageDraw.Draw(self.im)

    def dots(self, region, color=(47, 36, 131), alpha=26, step=26):
        x0, y0, x1, y1 = region
        lay = Image.new("RGBA", self.im.size, (0, 0, 0, 0))
        dd = ImageDraw.Draw(lay)
        cx, cy, rx, ry = (x0 + x1) / 2, (y0 + y1) / 2, (x1 - x0) / 2, (y1 - y0) / 2
        for y in range(int(y0), int(y1), step):
            for x in range(int(x0), int(x1), step):
                f = 1 - math.hypot((x - cx) / rx, (y - cy) / ry)
                if f > 0:
                    r = 1.3 * K
                    dd.ellipse([x * K - r, y * K - r, x * K + r, y * K + r], fill=color + (int(alpha * min(1, f * 1.6)),))
        self.im.alpha_composite(lay)

    def bubbles(self, spots):
        for x, y, s in spots:
            b = bubble(s * K)
            self.im.alpha_composite(b, (int((x - s / 2) * K), int((y - s / 2) * K)))

    def sparkle(self, x, y, s, color=AQUA, alpha=255):
        pts = [((x + px * s / 2) * K, (y + py * s / 2) * K) for px, py in SPARK]
        lay = Image.new("RGBA", self.im.size, (0, 0, 0, 0))
        ImageDraw.Draw(lay).polygon(pts, fill=color + (alpha,))
        self.im.alpha_composite(lay)

    def rrect(self, b, r, fill=None, outline=None, width=1, alpha=255):
        lay = Image.new("RGBA", self.im.size, (0, 0, 0, 0))
        ImageDraw.Draw(lay).rounded_rectangle(self.box(b), radius=int(r * K), fill=(fill + (alpha,)) if fill else None,
                                              outline=(outline + (alpha,)) if outline else None, width=int(width * K))
        self.im.alpha_composite(lay)

    def shadow(self, b, r, blur=40, offset=(0, 30), alpha=90, color=NAVY):
        lay = Image.new("RGBA", self.im.size, (0, 0, 0, 0))
        x0, y0, x1, y1 = b
        ImageDraw.Draw(lay).rounded_rectangle(self.box((x0 + 20, y0 + offset[1], x1 - 20, y1 + offset[1])), radius=int(r * K), fill=color + (alpha,))
        self.im.alpha_composite(lay.filter(ImageFilter.GaussianBlur(blur * K)))

    def fill_grad(self, b, stops, angle=100, r=0):
        x0, y0, x1, y1 = self.box(b)
        g = gradient(x1 - x0, y1 - y0, stops, angle).convert("RGBA")
        if r:
            m = Image.new("L", g.size, 0)
            ImageDraw.Draw(m).rounded_rectangle([0, 0, g.size[0] - 1, g.size[1] - 1], radius=int(r * K), fill=255)
            g.putalpha(m)
        self.im.alpha_composite(g, (x0, y0))

    def photo(self, im, b, r=36, focal=(.5, .5), ring=None, shadow=True):
        x0, y0, x1, y1 = b
        if shadow:
            self.shadow(b, r, blur=34, offset=(0, 34), alpha=80)
        if ring:
            self.rrect((x0 - 14, y0 - 14, x1 - 14 + 0, y1 - 14), r + 8, outline=ring, width=2)
        W, H = int((x1 - x0) * K), int((y1 - y0) * K)
        src = im.convert("RGB")
        sw, sh = src.size
        sc = max(W / sw, H / sh)
        nw, nh = int(math.ceil(sw * sc)), int(math.ceil(sh * sc))
        src = src.resize((nw, nh), Image.LANCZOS)
        ox = int(max(0, min(nw - W, focal[0] * nw - W / 2)))
        oy = int(max(0, min(nh - H, focal[1] * nh - H / 2)))
        crop = src.crop((ox, oy, ox + W, oy + H)).convert("RGBA")
        m = Image.new("L", (W, H), 0)
        ImageDraw.Draw(m).rounded_rectangle([0, 0, W - 1, H - 1], radius=int(r * K), fill=255)
        crop.putalpha(m)
        self.im.alpha_composite(crop, (int(x0 * K), int(y0 * K)))

    # ---- text
    def text(self, xy, s, kind, size, fill, anchor="la", track=0.0):
        f = font(kind, size)
        x, y = xy[0] * K, xy[1] * K
        if not track:
            self.d.text((x, y), s, font=f, fill=fill, anchor=anchor)
            return f.getlength(s) / K
        total = sum(f.getlength(ch) for ch in s) + track * size * K * (len(s) - 1)
        if anchor[0] == "m":
            x -= total / 2
        elif anchor[0] == "r":
            x -= total
        for ch in s:
            self.d.text((x, y), ch, font=f, fill=fill, anchor="l" + anchor[1])
            x += f.getlength(ch) + track * size * K
        return total / K

    def measure(self, s, kind, size):
        return font(kind, size).getlength(s) / K

    def wrap(self, s, kind, size, maxw):
        words, lines, line = s.split(), [], ""
        for w in words:
            t = (line + " " + w).strip()
            if self.measure(t, kind, size) > maxw and line:
                lines.append(line)
                line = w
            else:
                line = t
        lines.append(line)
        return lines

    def para(self, x, y, s, kind, size, fill, maxw, lh=1.35, anchor="la", max_lines=None):
        lines = self.wrap(s, kind, size, maxw)
        if max_lines:
            lines = lines[:max_lines]
        for ln in lines:
            self.text((x, y), ln, kind, size, fill, anchor=anchor)
            y += size * lh
        return y

    def gtext(self, xy, s, kind, size, stops, anchor="la"):
        f = font(kind, size)
        m = Image.new("L", self.im.size, 0)
        ImageDraw.Draw(m).text((xy[0] * K, xy[1] * K), s, font=f, fill=255, anchor=anchor)
        bb = m.getbbox()
        if not bb:
            return 0
        g = gradient(bb[2] - bb[0], bb[3] - bb[1], stops, 100).convert("RGBA")
        g.putalpha(m.crop(bb))
        self.im.alpha_composite(g, (bb[0], bb[1]))
        return f.getlength(s) / K

    def label(self, x, y, s, color=AMBER_INK, size=17, dash=True):
        if dash:
            self.fill_grad((x, y + size * .45 - 1.5, x + 34, y + size * .45 + 1.5), SWOOSH, 90, r=2)
            x += 48
        return self.text((x, y), s.upper(), "label", size, color, track=.14)

    def icon(self, name, x, y, s, color):
        self.layer(icon_img(name, s, color), (x, y))

    def chip_icon(self, name, x, y, s, stops=FRESH, color=WHITE):
        """An icon in a gradient circle (the website's badge treatment)."""
        self.fill_grad((x, y, x + s, y + s), stops, 135, r=s / 2)
        pad = s * .24
        self.icon(name, x + pad, y + pad, s - 2 * pad, color)

    def save(self, path, quality=92):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        out = self.im.resize((self.w, self.h), Image.LANCZOS).convert("RGB")
        if path.endswith(".png"):
            out.save(path, optimize=True)
        else:
            out.save(path, "JPEG", quality=quality, optimize=True, progressive=True)
        return out


# ------------------------------------------------------------------ assets
_cache = {}


def svg(path, height=None, width=None, recolor=None):
    key = (path, height, width, recolor)
    if key in _cache:
        return _cache[key]
    data = open(path, "rb").read()
    if recolor:
        data = recolor(data)
    def render(b):
        doc = fitz.open(stream=b, filetype="svg")
        page = doc[0]
        z = (height * K / page.rect.height) if height else (width * K / page.rect.width)
        pix = page.get_pixmap(matrix=fitz.Matrix(z, z), alpha=True)
        return Image.frombytes("RGBA", (pix.width, pix.height), pix.samples)
    im = render(data)
    # MuPDF does not paint SVG gradient fills (the logo's swoosh came out flat navy). For each
    # gradient, render only the shapes that use it as a mask and paint its own stops through it.
    t = data.decode("utf-8")
    for gid, body in re.findall(r'<linearGradient id="([^"]+)"[^>]*>(.*?)</linearGradient>', t, flags=re.S):
        stops = [(float(o), tuple(int(c[i:i + 2], 16) for i in (0, 2, 4)))
                 for o, c in re.findall(r'offset="([\d.]+)"\s+stop-color="#([0-9A-Fa-f]{6})"', body)]
        if len(stops) < 2:
            continue
        only = re.sub(r'fill="#[0-9A-Fa-f]{3,6}"', 'fill="none"', t)
        only = re.sub(r'stroke="#[0-9A-Fa-f]{3,6}"', 'stroke="none"', only)
        only = only.replace('fill="url(#%s)"' % gid, 'fill="#000000"')
        mask = render(only.encode("utf-8")).split()[3]
        bb = mask.getbbox()
        if not bb:
            continue
        g = gradient(bb[2] - bb[0], bb[3] - bb[1], stops, 97).convert("RGBA")
        g.putalpha(mask.crop(bb))
        im.alpha_composite(g, (bb[0], bb[1]))
    _cache[key] = im
    return im


def icon_img(name, s, color):
    hexc = "#%02x%02x%02x" % color

    def rc(b):
        t = b.decode("utf-8")
        t = re.sub(r"<!--.*?-->", "", t, flags=re.S)
        t = t.replace("currentColor", hexc).replace('stroke-linecap="round"', 'stroke-linecap="square"')
        t = t.replace('stroke-linejoin="round"', 'stroke-linejoin="miter"').replace('stroke-width="2"', 'stroke-width="2.1"')
        return t.encode("utf-8")
    return svg(os.path.join(CACHE, "icons", name + ".svg"), height=s, recolor=rc)


def logo(kind="lockup", height=60, reverse=False):
    fn = "logo-%s%s.svg" % (kind, "-rev" if reverse else "")
    return svg(os.path.join(IMG, fn), height=height)


def seal(size):
    core = svg(os.path.join(IMG, "seal-core.svg"), height=size).copy()
    ring = svg(os.path.join(IMG, "seal-ring.svg"), height=size)
    core.alpha_composite(ring.resize(core.size, Image.LANCZOS))
    return core


def photo(ref):
    """Full-resolution original when we have it, else the largest WebP the site build made."""
    if ref.startswith("img:"):
        key = ref[4:]
        files = sorted((f for f in os.listdir(IMG) if re.match(re.escape(key) + r"-\d+\.webp$", f)),
                       key=lambda f: int(re.search(r"-(\d+)\.webp$", f).group(1)))
        return Image.open(os.path.join(IMG, files[-1])).convert("RGB")
    return Image.open(os.path.join(SRC, ref)).convert("RGB")


def service_group(name):
    for g, _, items in L.GROUPS:
        if any(n == name for n, _ in items):
            return g
    return ""


ALL_SERVICES = [n for _, _, items in L.GROUPS for n, _ in items]


# ------------------------------------------------------------------ shared furniture
def header(a, x=60, y=56, reverse=False, tag=None, tag_color=AMBER_INK):
    lg = logo("lockup", 54, reverse)
    a.layer(lg, (x, y))
    if tag:
        tw = a.measure(tag.upper(), "label", 15) + 15 * .14 * len(tag) + 36
        bx1 = a.w - x
        a.rrect((bx1 - tw, y + 8, bx1, y + 48), 20, fill=WHITE if not reverse else NAVY, alpha=235)
        a.rrect((bx1 - tw, y + 8, bx1, y + 48), 20, outline=LINE if not reverse else (60, 62, 110), width=1.2)
        a.text((bx1 - tw / 2, y + 28), tag.upper(), "label", 15, tag_color if not reverse else SUN, anchor="mm", track=.14)


def contact_band(a, y, h=None, dark=True):
    """Bottom band: phone / WhatsApp and the web address, with the swoosh line on top."""
    h = h or (a.h - y)
    a.rrect((0, y, a.w, a.h + 40), 0, fill=NAVY if dark else WHITE)
    a.fill_grad((0, y, a.w, y + 6), SWOOSH, 90)
    cy = y + 6 + (h - 6) / 2
    a.chip_icon("phone", 60, cy - 24, 48, SWOOSH, NAVY)
    a.text((124, cy - 13), "CALL OR WHATSAPP", "label", 13, SUN if dark else AMBER_INK, anchor="lm", track=.14)
    a.text((124, cy + 14), PHONE, "display", 27, WHITE if dark else NAVY, anchor="lm")
    a.text((a.w - 60, cy - 13), "GET A FREE QUOTE", "label", 13, SUN if dark else AMBER_INK, anchor="rm", track=.14)
    a.text((a.w - 60, cy + 14), SITE, "text", 22, (210, 212, 235) if dark else TEXT2, anchor="rm")


def fizz(a, seed, n=9, area=None, sparkles=4):
    import random
    rnd = random.Random(seed)
    x0, y0, x1, y1 = area or (0, 0, a.w, a.h)
    a.bubbles([(rnd.uniform(x0, x1), rnd.uniform(y0, y1), rnd.choice([14, 20, 26, 34, 46, 62])) for _ in range(n)])
    for i in range(sparkles):
        a.sparkle(rnd.uniform(x0, x1), rnd.uniform(y0, y1), rnd.choice([16, 22, 28]), [AQUA, AMBER, INDIGO6, AQUA][i % 4], 230)


def badge(a, x, y, txt, ic="circle-check", stops=FRESH, icolor=WHITE, size=19):
    w = a.measure(txt, "text", size) + 76
    a.shadow((x, y, x + w, y + 54), 27, blur=16, offset=(0, 14), alpha=60)
    a.rrect((x, y, x + w, y + 54), 27, fill=WHITE, alpha=240)
    a.chip_icon(ic, x + 9, y + 9, 36, stops, icolor)
    a.text((x + 56, y + 27), txt, "label", size * .82, NAVY, anchor="lm", track=.02)
    return w


# ------------------------------------------------------------------ feed posts (1080 x 1080)
def post_service(name, idx):
    line, inc, who = L.SERVICE_COPY[name]
    grp = service_group(name)
    a = Art(1080, 1080)
    a.fresh_bg()
    fizz(a, idx, 7, (40, 120, 1040, 640), 3)
    header(a, tag="Service %02d / %02d" % (idx, len(ALL_SERVICES)))
    a.photo(photo(SERVICE_PHOTO[name]), (60, 140, 1020, 570), r=40, ring=SKY200)
    badge(a, 84, 506, who, "badge-check")
    y = 612
    a.label(60, y, grp, AMBER_INK, 15)
    y += 34
    size = 54 if a.measure(name, "display", 54) < 960 else 44
    for ln in a.wrap(name, "display", size, 960):
        a.text((60, y), ln, "display", size, NAVY)
        y += size * 1.02
    y = a.para(60, y + 10, line, "text", 23, TEXT2, 930, 1.38, max_lines=2)
    x = 60
    y += 14
    for it in inc:
        w = a.measure(it, "text", 18) + 58
        if x + w > 1020:
            break
        a.rrect((x, y, x + w, y + 42), 21, fill=WHITE, alpha=235)
        a.rrect((x, y, x + w, y + 42), 21, outline=SKY200, width=1.4)
        a.chip_icon("check", x + 7, y + 7, 28, FRESH)
        a.text((x + 44, y + 21), it, "text", 18, TEXT, anchor="lm")
        x += w + 10
    contact_band(a, 966)
    return a


def post_brand():
    """The headline: Where cleanliness meets excellence — over the bright lobby."""
    a = Art(1080, 1080)
    a.photo(photo("unsplash-vrNujj2iGGY.jpg"), (0, 0, 1080, 1080), r=0, focal=(.5, .62), shadow=False)
    a.layer(Image.fromarray(np.dstack([np.full((1080 * K, 1080 * K), c, np.uint8) for c in WHITE] +
                                      [np.tile(np.clip(np.linspace(1.25, -.15, 1080 * K), 0, .96)[:, None] * 255, (1, 1080 * K)).astype(np.uint8)]), "RGBA"))
    fizz(a, 3, 12, (0, 380, 1080, 1000), 5)
    header(a)
    a.label(60, 190, "Commercial · residential · post-construction")
    y = 232
    for ln, grad in (("Where", False), ("cleanliness", False), ("meets", False), ("excellence.", True)):
        if grad:
            a.gtext((58, y), ln, "display", 104, DEEP)
        else:
            a.text((58, y), ln, "display", 104, NAVY)
        y += 104
    a.para(60, y + 26, "Reliable, affordable, professional cleaning for homes, offices, churches and commercial spaces across Nairobi.",
           "text", 26, TEXT2, 760, 1.4)
    contact_band(a, 966)
    return a


def post_guarantee():
    a = Art(1080, 1080)
    a.fresh_bg((255, 247, 232), WHITE, aqua=(1.0, 1.0), sun=(.9, .0), strength=1.2)
    fizz(a, 11, 8, (0, 120, 1080, 940), 4)
    header(a, tag="Our promise")
    sl = seal(330)
    a.shadow((375, 170, 705, 500), 165, blur=30, offset=(0, 28), alpha=90)
    a.layer(sl, (375, 165))
    a.text((540, 560), "Clean Quality", "display", 66, NAVY, anchor="ma")
    a.gtext((540, 632), "Guaranteed", "display", 66, DEEP, anchor="ma")
    y = a.para(540, 728, "Missed something? Tell us within 24 hours and we come back and re-clean it — no argument, no extra charge.",
               "text", 26, TEXT2, 820, 1.4, anchor="ma")
    pills = ["Named supervisor", "Checked against the scope", "Monthly review"]
    x = 540 - (sum(a.measure(p, "text", 17) + 52 for p in pills) + 20) / 2
    for p in pills:
        w = a.measure(p, "text", 17) + 52
        a.rrect((x, y + 18, x + w, y + 58), 20, fill=WHITE)
        a.rrect((x, y + 18, x + w, y + 58), 20, outline=(255, 226, 170), width=1.4)
        a.chip_icon("check", x + 6, y + 24, 28, SWOOSH, NAVY)
        a.text((x + 42, y + 38), p, "text", 17, TEXT, anchor="lm")
        x += w + 10
    contact_band(a, 966)
    return a


def post_why():
    a = Art(1080, 1080)
    a.fresh_bg()
    fizz(a, 5, 6, (0, 100, 1080, 300), 3)
    header(a, tag="Why Smartline")
    a.label(60, 150, "Six reasons")
    a.text((60, 186), "Why clients stay", "display", 58, NAVY)
    a.gtext((60, 246), "with Smartline.", "display", 58, DEEP)
    cw, ch, gx, gy = 470, 196, 20, 18
    for i, (t, dsc) in enumerate(L.WHY):
        cx = 60 + (i % 2) * (cw + gx)
        cy = 344 + (i // 2) * (ch + gy)
        a.shadow((cx, cy, cx + cw, cy + ch), 26, blur=18, offset=(0, 14), alpha=40)
        a.rrect((cx, cy, cx + cw, cy + ch), 26, fill=WHITE)
        a.rrect((cx, cy, cx + cw, cy + ch), 26, outline=LINE, width=1.2)
        a.chip_icon(REASON_ICON[i], cx + 24, cy + 24, 52, FRESH if i % 2 == 0 else SWOOSH, WHITE if i % 2 == 0 else NAVY)
        a.text((cx + cw - 26, cy + 30), "%02d" % (i + 1), "display", 20, (200, 202, 222), anchor="ra")
        a.text((cx + 24, cy + 94), t, "display", 24, NAVY)
        a.para(cx + 24, cy + 130, dsc, "text", 16.5, TEXT2, cw - 48, 1.36, max_lines=3)
    contact_band(a, 1000, 80)
    return a


def post_process():
    a = Art(1080, 1080)
    a.fresh_bg(SKY50, WHITE, aqua=(.1, 0), sun=(1, 1))
    fizz(a, 21, 7, (560, 120, 1080, 940), 4)
    header(a, tag="How we work")
    a.label(60, 150, "Five steps, every contract")
    a.text((60, 186), "From first call to", "display", 52, NAVY)
    a.gtext((60, 242), "a standard that holds.", "display", 52, DEEP)
    x0, y = 104, 350
    a.fill_grad((x0 - 1.5, y + 20, x0 + 1.5, y + 4 * 130 + 20), FRESH, 180)
    for i, (t, dsc) in enumerate(STEPS):
        a.fill_grad((x0 - 34, y - 14, x0 + 34, y + 54), SWOOSH if i == 0 else FRESH, 135, r=34)
        a.text((x0, y + 20), "%02d" % (i + 1), "display", 24, NAVY if i == 0 else WHITE, anchor="mm")
        a.text((x0 + 64, y - 2), t, "display", 30, NAVY)
        a.text((x0 + 64, y + 40), dsc, "text", 21, TEXT2)
        y += 130
    contact_band(a, 1000, 80)
    return a


def post_training():
    a = Art(1080, 1080)
    a.fresh_bg()
    fizz(a, 8, 6, (700, 120, 1080, 500), 3)
    header(a, tag="Training")
    a.label(60, 150, "Before placement")
    a.text((60, 186), "Every Smartline cleaner", "display", 50, NAVY)
    a.gtext((60, 240), "is trained in:", "display", 50, DEEP)
    bx = (60, 330, 1020, 968)
    a.shadow(bx, 30, blur=26, offset=(0, 24), alpha=55)
    a.rrect(bx, 30, fill=WHITE)
    a.fill_grad((60, 330, 66, 968), SWOOSH, 180)
    a.text((96, 372), "TRAINING RECORD", "label", 16, NAVY, anchor="lm", track=.14)
    st = "BEFORE PLACEMENT"
    sw = a.measure(st, "label", 13) + 13 * .14 * len(st) + 30
    a.rrect((984 - sw, 354, 984, 390), 8, outline=FLAME, width=1.6)
    a.text((984 - sw / 2, 372), st, "label", 13, AMBER_INK, anchor="mm", track=.14)
    y = 410
    for i, (t, dsc) in enumerate(L.TRAINING):
        a.rrect((60, y - 2, 1020, y), 0, fill=LINE)
        a.rrect((96, y + 18, 148, y + 70), 14, fill=(240, 239, 251))
        a.icon(TRAINING_ICON[i], 108, y + 30, 28, INDIGO)
        a.text((172, y + 22), t, "display", 23, NAVY)
        a.text((172, y + 56), dsc, "text", 18, MUTED)
        a.chip_icon("check", 944, y + 28, 36, SWOOSH, NAVY)
        y += 88
    a.layer(logo("mark", 30), (96, 932))
    a.text((134, 948), "Refreshed on the job by a named supervisor", "text", 18, INDIGO, anchor="lm")
    return a


def post_clients():
    a = Art(1080, 1080)
    a.fresh_bg(WHITE, SKY50, aqua=(1, 1), sun=(0, 0))
    fizz(a, 13, 6, (620, 100, 1080, 420), 3)
    header(a, tag="Named with permission")
    a.label(60, 150, "Clients served")
    a.text((60, 186), "Spaces we look", "display", 56, NAVY)
    a.gtext((60, 244), "after in Nairobi.", "display", 56, DEEP)
    y = 350
    for i, (n, sector) in enumerate(L.CLIENTS):
        a.rrect((60, y, 1020, y + 1.4), 0, fill=LINE)
        a.text((60, y + 34), "%02d" % (i + 1), "label", 15, AMBER_INK, anchor="lm", track=.1)
        size = 27 if a.measure(n, "display", 27) < 700 else 23
        a.text((112, y + 34), n, "display", size, NAVY, anchor="lm")
        sw = a.measure(sector, "text", 15) + 28
        a.rrect((1020 - sw, y + 19, 1020, y + 49), 15, fill=SKY100)
        a.text((1020 - sw / 2, y + 34), sector, "text", 15, AQUA_INK, anchor="mm")
        y += 68
    contact_band(a, 1000, 80)
    return a


def post_schedules():
    a = Art(1080, 1080)
    a.photo(photo("unsplash-7NvBEeHDY7M.jpg"), (0, 0, 1080, 600), r=0, focal=(.5, .5), shadow=False)
    fade = np.tile(np.clip((np.arange(1080 * K) - 380 * K) / (240 * K), 0, 1)[:, None] * 255, (1, 1080 * K)).astype(np.uint8)
    a.layer(Image.fromarray(np.dstack([np.full((1080 * K, 1080 * K), 255, np.uint8)] * 3 + [fade]), "RGBA"))
    fizz(a, 17, 9, (0, 420, 1080, 940), 4)
    header(a, tag="Schedules")
    a.label(60, 560, "One clean or a programme")
    a.text((60, 596), "Once, or on", "display", 64, NAVY)
    a.gtext((60, 664), "a schedule.", "display", 64, DEEP)
    x, y = 60, 770
    for s in L.SCHEDULES:
        w = a.measure(s, "text", 21) + 46
        if x + w > 1020:
            x, y = 60, y + 64
        a.rrect((x, y, x + w, y + 50), 25, fill=WHITE)
        a.rrect((x, y, x + w, y + 50), 25, outline=SKY200, width=1.6)
        a.text((x + w / 2, y + 25), s, "text", 21, NAVY, anchor="mm")
        x += w + 12
    contact_band(a, 966)
    return a


def post_about():
    a = Art(1080, 1080)
    a.fresh_bg()
    fizz(a, 23, 8, (0, 120, 1080, 960), 4)
    header(a, tag="About us")
    a.photo(photo("unsplash-SaVqlZczQXs.jpg"), (600, 150, 1020, 640), r=36, ring=SKY200, focal=(.47, .55))
    a.label(60, 160, "Est. 2018 · Kasarani")
    y = 200
    for ln in ("A single", "point of", "contact for"):
        a.text((60, y), ln, "display", 60, NAVY)
        y += 64
    a.gtext((60, y), "every clean.", "display", 60, DEEP)
    a.para(60, y + 96, "Smartline Point Cleaning Hub Ltd cleans offices, banks, schools, churches, homes, apartments and new builds — "
           "with trained, supervised teams — and keeps compounds and gardens neat.", "text", 22, TEXT2, 500, 1.42)
    y = 690
    cols = (("building-2", "Commercial", "Offices, banks, schools"), ("house", "Residential", "Homes, apartments, Airbnbs"),
            ("hard-hat", "Post-construction", "New builds, renovations"), ("sprout", "Landscaping", "Lawns, hedges, compounds"))
    for i, (ic, t, dsc) in enumerate(cols):
        cx = 60 + i * 240
        a.rrect((cx, y, cx + 226, y + 226), 26, fill=WHITE)
        a.rrect((cx, y, cx + 226, y + 226), 26, outline=LINE, width=1.2)
        a.chip_icon(ic, cx + 22, y + 22, 56, FRESH if i % 2 == 0 else SWOOSH, WHITE if i % 2 == 0 else NAVY)
        a.text((cx + 22, y + 104), t, "display", 21 if len(t) < 14 else 17.5, NAVY)
        a.para(cx + 22, y + 140, dsc, "text", 16.5, TEXT2, 190, 1.35)
    contact_band(a, 966)
    return a


def post_contact():
    a = Art(1080, 1080)
    a.fresh_bg(SKY100, WHITE, aqua=(.9, .1), sun=(.1, .9), strength=1.3)
    fizz(a, 29, 14, (0, 100, 1080, 1000), 6)
    header(a, tag="Free quote")
    a.label(60, 190, "Assuring you the best")
    a.text((60, 230), "Book your", "display", 96, NAVY)
    a.gtext((60, 330), "clean today.", "display", 96, DEEP)
    a.para(60, 470, "Call, WhatsApp or send the form on our website. We reply within one working day.", "text", 26, TEXT2, 820, 1.4)
    rows = (("phone", "Call or WhatsApp", PHONE), ("mail", "Email", C.EMAIL), ("map-pin", "Office", "ICIPE Road, Sports Drive, Suite 8, Kasarani"),
            ("send", "Website", SITE))
    y = 600
    for ic, t, v in rows:
        a.chip_icon(ic, 60, y, 56, SWOOSH if ic == "phone" else FRESH, NAVY if ic == "phone" else WHITE)
        a.text((136, y + 6), t.upper(), "label", 14, AMBER_INK, track=.14)
        a.text((136, y + 28), v, "display" if ic == "phone" else "text", 26 if ic == "phone" else 22, NAVY)
        y += 92
    return a


# ------------------------------------------------------------------ carousel (1080 x 1350, Instagram 4:5)
def carousel():
    slides = []
    a = Art(1080, 1350)
    a.photo(photo("unsplash-vrNujj2iGGY.jpg"), (0, 0, 1080, 1350), r=0, focal=(.5, .6), shadow=False)
    fade = np.tile(np.clip(1.15 - np.arange(1350 * K) / (1350 * K) * 1.3, .0, .94)[:, None] * 255, (1, 1080 * K)).astype(np.uint8)
    a.layer(Image.fromarray(np.dstack([np.full((1350 * K, 1080 * K), 255, np.uint8)] * 3 + [fade]), "RGBA"))
    fizz(a, 31, 12, (0, 500, 1080, 1300), 6)
    header(a, tag="Swipe")
    a.label(60, 200, "Smartline Point Cleaning Hub")
    a.text((58, 240), "Thirteen", "display", 112, NAVY)
    a.text((58, 352), "services.", "display", 112, NAVY)
    a.gtext((58, 464), "One point", "display", 112, DEEP)
    a.gtext((58, 576), "of contact.", "display", 112, DEEP)
    badge(a, 60, 1230, "Swipe through all four groups", "arrow-right", SWOOSH, NAVY)
    slides.append(a)
    for gi, (g, _, items) in enumerate(L.GROUPS):
        a = Art(1080, 1350)
        a.fresh_bg()
        header(a, tag="%d / 4" % (gi + 1))
        a.photo(photo(GROUP_PHOTO[g]), (60, 150, 1020, 640), r=40, ring=SKY200)
        fizz(a, 40 + gi, 6, (60, 150, 1020, 640), 3)
        a.chip_icon(GROUP_ICON[g], 60, 690, 70, FRESH)
        a.text((150, 700), "GROUP %02d" % (gi + 1), "label", 15, AMBER_INK, track=.14)
        a.text((150, 726), g, "display", 44 if len(g) < 22 else 38, NAVY)
        y = 810
        step = min(104, (1236 - 810) / len(items))   # five services in Homes & apartments must clear the band
        for n, _ in items:
            a.rrect((60, y, 1020, y + 1.4), 0, fill=LINE)
            a.text((60, y + 28), n, "display", 26, NAVY, anchor="lm")
            a.para(60, y + 52, L.SERVICE_COPY[n][0], "text", 17.5, MUTED, 940, 1.3, max_lines=1)
            y += step
        contact_band(a, 1250, 100)
        slides.append(a)
    a = Art(1080, 1350)
    a.fresh_bg(SKY100, WHITE, strength=1.3)
    fizz(a, 51, 14, (0, 100, 1080, 1250), 6)
    header(a)
    sl = seal(260)
    a.layer(sl, (410, 200))
    a.text((540, 520), "Not sure what", "display", 72, NAVY, anchor="ma")
    a.gtext((540, 600), "you need?", "display", 72, DEEP, anchor="ma")
    a.para(540, 716, "Book a site visit — we will scope the clean with you and send a written quote.", "text", 27, TEXT2, 820, 1.4, anchor="ma")
    a.fill_grad((290, 880, 790, 966), SWOOSH, 100, r=43)
    a.text((540, 923), "WhatsApp " + PHONE, "display", 26, NAVY, anchor="mm")
    a.text((540, 1010), SITE, "text", 24, INDIGO, anchor="ma")
    contact_band(a, 1250, 100)
    slides.append(a)
    return slides


# ------------------------------------------------------------------ stories (1080 x 1920)
SAFE_TOP, SAFE_BOT = 250, 1670   # keep text clear of the app's own chrome


def story_launch():
    a = Art(1080, 1920)
    a.fresh_bg(SKY100, WHITE, strength=1.4)
    fizz(a, 61, 18, (0, 200, 1080, 1800), 8)
    a.layer(logo("lockup", 72), (540 - logo("lockup", 72).size[0] / K / 2, SAFE_TOP))
    a.label(330, 470, "Now live")
    a.text((540, 530), "Our new", "display", 120, NAVY, anchor="ma")
    a.gtext((540, 660), "website", "display", 120, DEEP, anchor="ma")
    a.text((540, 790), "is live.", "display", 120, NAVY, anchor="ma")
    ph = (140, 990, 940, 1450)
    a.photo(photo("unsplash-vrNujj2iGGY.jpg"), ph, r=44, ring=SKY200, focal=(.5, .65))
    badge(a, 170, 1400, "Request a quote in two steps", "send", SWOOSH, NAVY)
    a.fill_grad((180, 1530, 900, 1630), SWOOSH, 100, r=50)
    a.text((540, 1580), SITE, "display", 30, NAVY, anchor="mm")
    return a


def story_quote():
    a = Art(1080, 1920)
    a.photo(photo("unsplash-7pvC_d2iXSE.jpg"), (0, 0, 1080, 1100), r=0, shadow=False)
    fade = np.tile(np.clip((np.arange(1920 * K) - 760 * K) / (360 * K), 0, 1)[:, None] * 255, (1, 1080 * K)).astype(np.uint8)
    a.layer(Image.fromarray(np.dstack([np.full((1920 * K, 1080 * K), 255, np.uint8)] * 3 + [fade]), "RGBA"))
    fizz(a, 71, 12, (0, 900, 1080, 1800), 6)
    a.rrect((60, SAFE_TOP - 20, 60 + logo("lockup", 60).size[0] / K + 40, SAFE_TOP + 80), 30, fill=WHITE, alpha=235)
    a.layer(logo("lockup", 60), (80, SAFE_TOP))
    a.label(60, 1040, "Homes · offices · churches · new builds")
    a.text((60, 1090), "Spotless,", "display", 104, NAVY)
    a.text((60, 1196), "fresh and", "display", 104, NAVY)
    a.gtext((60, 1302), "ready to use.", "display", 104, DEEP)
    a.para(60, 1440, "Trained, supervised cleaners across Nairobi and Kiambu. Free site visit and a written quote.", "text", 30, TEXT2, 900, 1.4)
    a.fill_grad((60, 1600, 1020, 1700), SWOOSH, 100, r=50)
    a.text((540, 1650), "Call or WhatsApp  " + PHONE, "display", 30, NAVY, anchor="mm")
    return a


def story_services():
    a = Art(1080, 1920)
    a.fresh_bg()
    fizz(a, 81, 10, (600, 150, 1080, 700), 5)
    a.layer(logo("lockup", 60), (60, SAFE_TOP - 40))
    a.label(60, 360, "Everything we clean")
    a.text((60, 400), "13 services,", "display", 84, NAVY)
    a.gtext((60, 490), "one contact.", "display", 84, DEEP)
    y = 640
    for g, _, items in L.GROUPS:
        a.chip_icon(GROUP_ICON[g], 60, y, 54, FRESH)
        a.text((132, y + 27), g, "display", 32, NAVY, anchor="lm")
        y += 78
        x = 60
        for n, _ in items:
            w = a.measure(n, "text", 22) + 40
            if x + w > 1020:
                x, y = 60, y + 60
            a.rrect((x, y, x + w, y + 48), 24, fill=WHITE)
            a.rrect((x, y, x + w, y + 48), 24, outline=SKY200, width=1.5)
            a.text((x + w / 2, y + 24), n, "text", 22, TEXT, anchor="mm")
            x += w + 10
        y += 92
    a.fill_grad((60, 1600, 1020, 1700), SWOOSH, 100, r=50)
    a.text((540, 1650), "Free quote · " + PHONE, "display", 30, NAVY, anchor="mm")
    return a


def story_guarantee():
    a = Art(1080, 1920)
    a.fresh_bg((255, 244, 222), WHITE, aqua=(1, 1), sun=(.8, 0), strength=1.3)
    fizz(a, 91, 14, (0, 200, 1080, 1800), 6)
    a.layer(logo("lockup", 60), (540 - logo("lockup", 60).size[0] / K / 2, SAFE_TOP - 40))
    sl = seal(460)
    a.shadow((310, 400, 770, 860), 230, blur=40, offset=(0, 40), alpha=90)
    a.layer(sl, (310, 390))
    a.text((540, 950), "Clean Quality", "display", 88, NAVY, anchor="ma")
    a.gtext((540, 1046), "Guaranteed.", "display", 88, DEEP, anchor="ma")
    a.para(540, 1190, "If something is missed, tell us within 24 hours. We come back and re-clean it — no argument, no extra charge.",
           "text", 32, TEXT2, 880, 1.42, anchor="ma")
    a.fill_grad((180, 1560, 900, 1660), SWOOSH, 100, r=50)
    a.text((540, 1610), "Book a clean · " + PHONE, "display", 30, NAVY, anchor="mm")
    return a


def story_service(name, idx):
    line, inc, who = L.SERVICE_COPY[name]
    a = Art(1080, 1920)
    a.fresh_bg()
    a.layer(logo("lockup", 60), (60, SAFE_TOP - 40))
    a.photo(photo(SERVICE_PHOTO[name]), (60, 360, 1020, 1060), r=44, ring=SKY200)
    fizz(a, 100 + idx, 8, (60, 360, 1020, 1060), 4)
    a.label(60, 1120, service_group(name))
    y = 1160
    for ln in a.wrap(name, "display", 72, 960):
        a.text((60, y), ln, "display", 72, NAVY)
        y += 76
    y = a.para(60, y + 16, line, "text", 29, TEXT2, 940, 1.4, max_lines=3)
    for it in inc:
        a.chip_icon("check", 60, y + 14, 38, FRESH)
        a.text((114, y + 33), it, "text", 26, TEXT, anchor="lm")
        y += 56
    a.fill_grad((60, 1600, 1020, 1700), SWOOSH, 100, r=50)
    a.text((540, 1650), "Get a quote · " + PHONE, "display", 30, NAVY, anchor="mm")
    return a


# ------------------------------------------------------------------ landscape (1200 x 630)
def wide(kind):
    a = Art(1200, 630)
    a.fresh_bg(SKY50, WHITE, aqua=(.95, .1), sun=(0, 1))
    if kind == "launch":
        a.photo(photo("unsplash-vrNujj2iGGY.jpg"), (700, 60, 1140, 570), r=36, ring=SKY200, focal=(.5, .65))
        fizz(a, 111, 10, (0, 60, 700, 600), 5)
        a.layer(logo("lockup", 50), (60, 56))
        a.label(60, 170, "Now live")
        a.text((58, 206), "Our new website", "display", 54, NAVY)
        a.gtext((58, 266), "is live.", "display", 54, DEEP)
        a.para(60, 352, "Services, how we work, our guarantee and a two-step quote form — in one place.", "text", 22, TEXT2, 580, 1.4)
        a.fill_grad((60, 470, 520, 540), SWOOSH, 100, r=35)
        a.text((290, 505), SITE, "display", 21, NAVY, anchor="mm")
        badge(a, 730, 500, "Clean Quality Guaranteed", "shield-check", SWOOSH, NAVY, 17)
    elif kind == "intro":
        a.photo(photo("unsplash-7NvBEeHDY7M.jpg"), (700, 60, 1140, 570), r=36, ring=SKY200)
        fizz(a, 121, 10, (0, 60, 700, 600), 5)
        a.layer(logo("lockup", 50), (60, 56))
        a.label(60, 170, "Since 2018 · Kasarani, Nairobi")
        a.text((58, 206), "Where cleanliness", "display", 50, NAVY)
        a.gtext((58, 262), "meets excellence.", "display", 50, DEEP)
        a.para(60, 344, "Commercial, residential and post-construction cleaning, and landscaping — trained, supervised teams across Nairobi and Kiambu.",
               "text", 21, TEXT2, 600, 1.42)
        a.text((60, 520), PHONE, "display", 30, NAVY)
        a.text((60, 566), SITE, "text", 20, INDIGO)
    else:  # commercial contracts
        a.photo(photo("unsplash-pYlBAu3de0w.jpg"), (700, 60, 1140, 570), r=36, ring=SKY200)
        fizz(a, 131, 10, (0, 60, 700, 600), 5)
        a.layer(logo("lockup", 50), (60, 56))
        a.label(60, 170, "For facility managers")
        a.text((58, 206), "Office & commercial", "display", 48, NAVY)
        a.gtext((58, 260), "cleaning contracts.", "display", 48, DEEP)
        y = 350
        for t in ("Written scope and a named supervisor", "Daily, weekly or quarterly schedules", "Supplier documents on request"):
            a.chip_icon("check", 60, y, 34, FRESH)
            a.text((108, y + 17), t, "text", 21, TEXT, anchor="lm")
            y += 50
        a.text((60, 530), "Free site visit · " + PHONE, "display", 24, NAVY)
        a.text((60, 570), SITE, "text", 19, INDIGO)
    return a


# ------------------------------------------------------------------ covers and profile images
def cover(w, h, name):
    a = Art(w, h)
    a.fresh_bg(SKY100, WHITE, aqua=(.95, .2), sun=(.05, 1), strength=1.3)
    a.dots((w * .02, 0, w * .5, h), alpha=30)
    fizz(a, w + h, int(w / 90), (0, 0, w, h), int(w / 260) + 2)
    lh = h * .26
    lg = logo("lockup", lh)
    # Facebook/LinkedIn crop the edges and overlay the profile picture bottom-left: keep content centred
    cx = w / 2
    a.layer(lg, (cx - lg.size[0] / K / 2, h * .2))
    t = "Where cleanliness meets excellence."
    size = h * .11
    tw = a.measure(t, "display", size)
    if tw > w * .7:
        size *= w * .7 / tw
    a.text((cx, h * .56), t, "display", size, NAVY, anchor="mm")
    a.text((cx, h * .74), "Commercial · Residential · Post-construction · Landscaping   |   %s   |   %s" % (PHONE, SITE),
           "label", h * .035, AMBER_INK, anchor="mm", track=.06)
    a.fill_grad((0, h - h * .025, w, h), SWOOSH, 90)
    return a


def profile(size, ring=True):
    a = Art(size, size)
    a.fresh_bg(WHITE, SKY50, strength=.6)
    mk = logo("mark", size * .56)
    a.layer(mk, (size / 2 - mk.size[0] / K / 2, size / 2 - mk.size[1] / K / 2 - size * .01))
    return a


# ------------------------------------------------------------------ captions
TAGS_CORE = "#Smartline #CleaningServices #Nairobi #Kenya #CleaningCompany #Kasarani"
TAGS = {
    "Commercial & institutional": "#OfficeCleaning #CommercialCleaning #FacilityManagement #NairobiBusiness",
    "Homes & apartments": "#HomeCleaning #HouseCleaning #AirbnbHost #NairobiHomes",
    "Specialist cleans": "#DeepCleaning #PostConstructionCleaning #Renovation #NewBuild",
    "Outdoor": "#Landscaping #GardenMaintenance #LawnCare #Kiambu",
}
CTA = "📞 Call or WhatsApp %s\n🌐 %s" % (PHONE, SITE)


def captions(entries):
    lines = ["# Smartline — social media pack: captions and calendar", "",
             "Generated by `make_social.py` from the same copy as the website. Paste the caption with each image.",
             "All photos are licensed stock or brand graphics: **they illustrate the service — never caption them as",
             "Smartline jobs, teams or client sites.** Swap in real job photos as the client supplies them.",
             "Posts that send people to the website go out **after the domain is live** (launch posts on go-live day).", "",
             "| Folder | Size | Where it goes |", "|---|---|---|",
             "| `01-feed-square` | 1080×1080 | Instagram and Facebook feed, LinkedIn, WhatsApp chats |",
             "| `02-instagram-carousel` | 1080×1350 | Instagram carousel (upload the six slides in order) — also works on LinkedIn as a document |",
             "| `03-stories-status` | 1080×1920 | Instagram and Facebook Stories, WhatsApp Status, TikTok photo posts |",
             "| `04-link-posts` | 1200×630 | LinkedIn and Facebook link posts, X |",
             "| `05-covers-profile` | various | Facebook cover, LinkedIn banner, X header, profile pictures |", ""]
    lines += ["## Four-week launch calendar", "",
              "| Week | Mon | Wed | Fri | Stories / Status |", "|---|---|---|---|---|",
              "| 1 — launch | Website launch (link post + story) | Brand: Where cleanliness meets excellence | About us | Launch, Services, Quote |",
              "| 2 — trust | Clean Quality Guaranteed | Commercial cleaning | Training record | Guarantee, Commercial |",
              "| 3 — homes | Residential cleaning | Carousel: 13 services | Move in / move out | Residential, Apartment |",
              "| 4 — specialist | Post-construction cleaning | How we work | Clients served | Post-construction, Deep |",
              "", "After week 4: one service spotlight a week (all 13 are ready), alternating with the reasons, schedules and contact posts.", ""]
    lines.append("## Captions")
    for fn, title, body, tags in entries:
        lines += ["", "### %s" % title, "`%s`" % fn, "", body, "", CTA, "", tags]
    return "\n".join(lines) + "\n"


# ------------------------------------------------------------------ build
def main():
    if os.path.isdir(OUT):
        shutil.rmtree(OUT)
    made, entries = [], []

    def put(a, rel, title=None, body=None, tags=None):
        path = os.path.join(OUT, rel)
        a.save(path)
        made.append(path)
        if title:
            entries.append((rel.replace("\\", "/"), title, body, tags))

    sq = "01-feed-square"
    put(post_brand(), os.path.join(sq, "01-brand-where-cleanliness-meets-excellence.jpg"), "Brand — Where cleanliness meets excellence",
        "Where cleanliness meets excellence. ✨\n\nReliable, affordable, professional cleaning for homes, offices, churches and commercial "
        "spaces across Nairobi — by trained, supervised teams.", TAGS_CORE)
    put(post_about(), os.path.join(sq, "02-about-us.jpg"), "About us",
        "A single point of contact for every clean. Since 2018, Smartline Point Cleaning Hub Ltd has looked after offices, banks, "
        "schools, churches, homes, apartments and new builds from our base in Kasarani — and kept compounds and gardens neat too.",
        TAGS_CORE + " #NairobiBusiness")
    put(post_guarantee(), os.path.join(sq, "03-clean-quality-guaranteed.jpg"), "Clean Quality Guaranteed",
        "Our promise: if something is missed, tell us within 24 hours and we come back and re-clean it — no argument, no extra charge. "
        "Every account has a named supervisor, and every visit is checked against the written scope.", TAGS_CORE + " #QualityGuaranteed")
    put(post_why(), os.path.join(sq, "04-why-smartline.jpg"), "Why Smartline — six reasons",
        "Six reasons clients stay with Smartline:\n✅ Flexible scheduling\n✅ Qualified cleaners\n✅ Trustworthy and friendly\n"
        "✅ Affordable\n✅ Keen on details\n✅ Quality results", TAGS_CORE)
    put(post_process(), os.path.join(sq, "05-how-we-work.jpg"), "How we work — five steps",
        "From first call to a standard that holds: site visit → scope and quote → team assigned → supervised clean → review. "
        "The same five steps on every contract, so the clean in month twelve matches the clean in week one.", TAGS_CORE + " #FacilityManagement")
    put(post_training(), os.path.join(sq, "06-training-record.jpg"), "Training record",
        "Every Smartline cleaner is trained before placement: communication, equipment use, chemical handling, grooming and PPE, "
        "teamwork and our code of conduct — then refreshed on the job by a named supervisor.", TAGS_CORE)
    put(post_clients(), os.path.join(sq, "07-clients-served.jpg"), "Clients served",
        "Proud to look after banks, schools, churches, apartment blocks, Airbnbs and hospitality venues across Nairobi — "
        "named here with their permission. Thank you for trusting us with your spaces. 🙏", TAGS_CORE)
    put(post_schedules(), os.path.join(sq, "08-schedules.jpg"), "Once, or on a schedule",
        "One clean, or a programme: one-time, daily or weekly contracts, quarterly, semi-annual, annual or a comprehensive "
        "programme. Tell us what the space needs and we will plan around you.", TAGS_CORE)
    put(post_contact(), os.path.join(sq, "09-book-your-clean.jpg"), "Book your clean today",
        "Book your clean today — call, WhatsApp or use the form on our website. We reply within one working day.", TAGS_CORE)
    for i, name in enumerate(ALL_SERVICES, 1):
        line, inc, who = L.SERVICE_COPY[name]
        slug = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")
        put(post_service(name, i), os.path.join(sq, "service-%02d-%s.jpg" % (i, slug)), "Service %02d — %s" % (i, name),
            "%s\n\n%s\n\nIdeal for: %s." % (line, "\n".join("✅ " + x for x in inc), who.lower()),
            TAGS_CORE + " " + TAGS[service_group(name)])

    for i, a in enumerate(carousel(), 1):
        put(a, os.path.join("02-instagram-carousel", "slide-%d.jpg" % i),
            "Instagram carousel — 13 services, one point of contact" if i == 1 else None,
            "Thirteen services, one point of contact. 👉 Swipe through: commercial and institutional, homes and apartments, "
            "specialist cleans and landscaping. Not sure what you need? Book a free site visit." if i == 1 else None,
            TAGS_CORE + " #OfficeCleaning #HomeCleaning #Landscaping" if i == 1 else None)

    st = "03-stories-status"
    put(story_launch(), os.path.join(st, "01-website-launch.jpg"), "Story — website launch",
        "Our new website is live! 🎉 Services, how we work, our guarantee and a two-step quote form — all in one place.", TAGS_CORE)
    put(story_quote(), os.path.join(st, "02-get-a-quote.jpg"), "Story — get a quote",
        "Spotless, fresh and ready to use. Free site visit and a written quote — tap to call or WhatsApp.", TAGS_CORE)
    put(story_services(), os.path.join(st, "03-all-services.jpg"), "Story — all services",
        "13 services, one contact. Which one do you need? Reply to this story. 👇", TAGS_CORE)
    put(story_guarantee(), os.path.join(st, "04-guarantee.jpg"), "Story — guarantee",
        "Clean Quality Guaranteed: missed something? Tell us within 24 hours and we re-clean it free.", TAGS_CORE)
    for i, name in enumerate(("Commercial cleaning", "Residential cleaning", "Apartment cleaning", "Post-construction cleaning",
                              "Deep cleaning", "Sofa set & upholstery cleaning", "Landscaping"), 5):
        slug = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")
        put(story_service(name, i), os.path.join(st, "%02d-%s.jpg" % (i, slug)), "Story — " + name,
            L.SERVICE_COPY[name][0], TAGS_CORE + " " + TAGS[service_group(name)])

    lk = "04-link-posts"
    put(wide("launch"), os.path.join(lk, "01-website-launch.jpg"), "Link post — website launch (LinkedIn / Facebook)",
        "We are delighted to launch our new website: %s\n\nSee our 13 services, how we work, the training every cleaner completes "
        "and our Clean Quality Guarantee — and request a quote in two steps." % SITE, TAGS_CORE + " #NairobiBusiness")
    put(wide("intro"), os.path.join(lk, "02-company-intro.jpg"), "Link post — company introduction",
        "Smartline Point Cleaning Hub Ltd: commercial, residential and post-construction cleaning, and landscaping, "
        "across Nairobi and Kiambu since 2018.", TAGS_CORE)
    put(wide("commercial"), os.path.join(lk, "03-commercial-contracts.jpg"), "Link post — commercial contracts (LinkedIn)",
        "Facility managers: cleaning contracts with a written scope, a named supervisor and schedules from daily to quarterly. "
        "Supplier documents on request. Book a free site visit.", TAGS_CORE + " #FacilityManagement #OfficeCleaning")

    cv = "05-covers-profile"
    put(cover(1640, 624, "facebook"), os.path.join(cv, "facebook-cover-1640x624.jpg"))
    put(cover(1584, 396, "linkedin"), os.path.join(cv, "linkedin-banner-1584x396.jpg"))
    put(cover(1500, 500, "x"), os.path.join(cv, "x-header-1500x500.jpg"))
    p = profile(1080)
    put(p, os.path.join(cv, "profile-picture-1080.png"))

    with open(os.path.join(OUT, "CAPTIONS.md"), "w", encoding="utf-8") as f:
        f.write(captions(entries))
    overview(made)
    verify(entries)
    print("social pack: %d images in %s" % (len(made), OUT))


def overview(paths):
    """One contact sheet of the whole pack for a quick look (social/00-overview.jpg)."""
    thumbs = []
    for pth in paths:
        im = Image.open(pth).convert("RGB")
        im.thumbnail((300, 380))
        thumbs.append(im)
    cols = 8
    rows = (len(thumbs) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * 316 + 16, rows * 396 + 16), (236, 238, 245))
    for i, t in enumerate(thumbs):
        x = 16 + (i % cols) * 316 + (300 - t.size[0]) // 2
        y = 16 + (i // cols) * 396 + (380 - t.size[1]) // 2
        sheet.paste(t, (x, y))
    sheet.save(os.path.join(OUT, "00-overview.jpg"), quality=86)


def verify(entries):
    text = " ".join(b or "" for _, _, b, _ in entries).lower()
    errs = []
    if "fumigat" in text:
        errs.append("fumigation appears in a caption")
    for bad in ("our team at work", "our job", "testimonial", "5-star", "%", "happy clients"):
        if bad in text:
            errs.append("caption contains '%s'" % bad)
    if len([e for e in entries if e[0].startswith("01-feed-square/service-")]) != 13:
        errs.append("expected 13 service spotlights")
    if errs:
        raise SystemExit("social verify FAILED:\n  " + "\n  ".join(errs))


if __name__ == "__main__":
    main()
