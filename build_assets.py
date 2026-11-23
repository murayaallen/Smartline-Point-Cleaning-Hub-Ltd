# -*- coding: utf-8 -*-
"""Smartline Point Cleaning Hub Ltd — asset pipeline for the website.

    python build_assets.py [--force]

Produces, under site/:
  assets/img/icons.svg            one sprite; Lucide paths redrawn to the house style
                                  (1.25px stroke, square caps, mitred joins — no rounded,
                                  bubbly line ends anywhere in this identity)
  assets/img/logo-*.svg           mark and lock-ups, colour and reversed, text outlined
  assets/img/seal-*.svg           Clean Quality Guaranteed seal: ring (rotates) + core
  assets/img/*.webp               every photograph cropped on its focal point, graded
                                  as one set, exported at 1x / 1.5x / 2x
  assets/img/og/*.jpg             1200x630 share cards
  favicon.svg, *.png, favicon.ico icons from the logo
and build_cache/assets.json, which build_site.py reads for sizes and srcsets.

  assets/fonts/mona-sans.woff2    Mona Sans (OFL), one variable file: wght 400-900 x wdth
                                  100-125, instanced from build_cache/mona-sans-latin.woff2
  assets/img/grain.png            the 3% film-grain tile laid over the whole site

Nothing downloads at build time — the build is repeatable offline.
"""
import io
import json
import os
import re
import sys

from PIL import Image, ImageDraw, ImageEnhance, ImageFont

import site_content as C

ROOT = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.join(ROOT, "site")
IMG = os.path.join(SITE, "assets", "img")
OG = os.path.join(IMG, "og")
SRC = os.path.join(ROOT, "media", "all")
CACHE = os.path.join(ROOT, "build_cache")
MANIFEST = os.path.join(CACHE, "assets.json")
FORCE = "--force" in sys.argv

INK = (14, 20, 48)
BRASS = (184, 134, 47)
PAPER = (250, 248, 244)

# ------------------------------------------------------------------ icons
ICON_NAMES = [
    "phone", "mail", "map-pin", "message-circle", "clock", "arrow-right", "arrow-up-right", "check",
    "chevron-down", "chevron-left", "chevron-right", "menu", "x", "plus", "minus", "file-text", "send",
    "building-2", "house", "hard-hat", "sprout", "shield-check", "badge-check", "calendar-clock",
    "messages-square", "wrench", "flask-conical", "shirt", "users", "scale", "circle-check", "scan-search",
]


def build_icons():
    out = os.path.join(IMG, "icons.svg")
    symbols = []
    for name in ICON_NAMES:
        src = os.path.join(CACHE, "icons", name + ".svg")
        with open(src, encoding="utf-8") as f:
            raw = f.read()
        body = raw[raw.index(">", raw.index("<svg")) + 1:raw.rindex("</svg>")]
        body = re.sub(r"<!--.*?-->", "", body, flags=re.S)
        body = re.sub(r"\s+", " ", body).strip()
        symbols.append('<symbol id="i-%s" viewBox="0 0 24 24">%s</symbol>' % (name, body))
    # stroke styling lives on the referencing <svg class="icon"> via CSS, so one
    # rule controls the weight of every icon on the site
    sprite = ('<svg xmlns="http://www.w3.org/2000/svg"><!-- Lucide icons, ISC licence, '
              'restyled for Smartline -->%s</svg>' % "".join(symbols))
    with open(out, "w", encoding="utf-8") as f:
        f.write(sprite)
    return {"icons": ICON_NAMES, "bytes": len(sprite)}


# ------------------------------------------------------------------ fonts
FONT_SRC = os.path.join(CACHE, "mona-sans-latin.woff2")
STATIC = {   # static instances for the share cards (PIL) and the seal (ReportLab)
    "display": {"wdth": 108, "wght": 600},    # v8: slimmer (was 125 / 800)
    "label": {"wdth": 125, "wght": 650},
    "text": {"wdth": 100, "wght": 500},
}


def build_fonts():
    from fontTools.ttLib import TTFont
    from fontTools.varLib import instancer
    os.makedirs(os.path.join(SITE, "assets", "fonts"), exist_ok=True)
    f = TTFont(FONT_SRC)
    web = instancer.instantiateVariableFont(f, {"wght": (400, 900), "wdth": (100, 125)})
    web.flavor = "woff2"
    dest = os.path.join(SITE, "assets", "fonts", "mona-sans.woff2")
    web.save(dest)
    for old_font in ("bodoni-moda.woff2", "bodoni-moda-italic.woff2", "manrope.woff2"):
        stale = os.path.join(SITE, "assets", "fonts", old_font)
        if os.path.exists(stale):
            os.remove(stale)
    for name, axes in STATIC.items():
        out = os.path.join(CACHE, "mona-%s.ttf" % name)
        if FORCE or not os.path.exists(out):
            st = instancer.instantiateVariableFont(TTFont(FONT_SRC), axes)
            st.flavor = None
            st.save(out)
    return {"mona-sans.woff2": os.path.getsize(dest)}


def mona(name):
    return os.path.join(CACHE, "mona-%s.ttf" % name)


def build_grain():
    """A seamless 128px monochrome noise tile; CSS lays it over everything at ~3%."""
    import random
    rnd = random.Random(2018)
    n = 128
    im = Image.new("L", (n, n))
    im.putdata([max(0, min(255, int(rnd.gauss(128, 40)) // 32 * 32 + 16)) for _ in range(n * n)])
    dest = os.path.join(IMG, "grain.png")
    im.save(dest, optimize=True, bits=4)
    return os.path.getsize(dest)




def build_qr():
    """A WhatsApp QR for desktop visitors on the contact page (segno, navy on white, quiet zone kept)."""
    import segno
    qr = segno.make(C.wa_link(), error="m")
    buf = io.BytesIO()
    qr.save(buf, kind="svg", scale=1, border=2, dark="#101238", light="#ffffff", xmldecl=False, svgns=True, nl=False,
            svgclass=None, lineclass=None)
    svg = buf.getvalue().decode("utf-8").replace("<svg ", '<svg role="img" aria-label="QR code: chat with Smartline on WhatsApp" ', 1)
    with open(os.path.join(IMG, "wa-qr.svg"), "w", encoding="utf-8") as f:
        f.write(svg)
    return {"modules": qr.symbol_size(scale=1, border=2)[0], "bytes": len(svg)}

# ------------------------------------------------------------------ vector shapes (original, from the logo's geometry)
def build_shapes():
    """Decorative vectors for the backgrounds — drawn here, not downloaded, so nothing to license:
      waves     wiped streaks: parallel flowing lines, indigo to sun
      drops     the logo's own droplet, scattered at sizes and angles
      rings     seal language: hairline rings, a dashed ring, two diamonds (light + dark versions)
      ribbon    the logo's swoosh, outlined and echoed, as a ribbon for navy sections
    """
    import math
    import random
    import logo_original as LO
    out_dir = os.path.join(IMG, "shapes")
    os.makedirs(out_dir, exist_ok=True)
    grad = ('<linearGradient id="g" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#2F2483"/>'
            '<stop offset=".55" stop-color="#F8951A"/><stop offset="1" stop-color="#FFC200"/></linearGradient>')
    files = {}

    # waves: seven lines, each a smooth sum of two sines, drifting apart toward the right
    W, H = 1600, 360
    lines = []
    for i in range(7):
        pts = []
        for x in range(0, W + 1, 20):
            t = x / W
            y = (H * 0.18 + i * 26 + math.sin(t * 5.2 + i * 0.45) * (18 + i * 3)
                 + math.sin(t * 11.0 + i) * 6 + t * i * 9)
            pts.append("%d %.1f" % (x, y))
        lines.append('<path d="M%s" stroke-opacity="%.2f"/>' % (" L".join(pts), 0.9 - i * 0.1))
    files["waves.svg"] = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" preserveAspectRatio="none"><defs>%s</defs>'
                          '<g fill="none" stroke="url(#g)" stroke-width="1.3">%s</g></svg>' % (W, H, grad, "".join(lines)))

    # drops: the client's droplet, scattered (fixed seed: the same picture every build)
    rnd = random.Random(48018)
    S = 640
    drops = []
    for i in range(13):
        size = rnd.choice([14, 18, 24, 32, 44, 60])
        x, y = rnd.uniform(20, S - 80), rnd.uniform(20, S - 80)
        d, _ = LO.part_path("droplet", size, x, y, rnd.uniform(-30, 30))
        if i % 3 == 0:
            drops.append('<path d="%s" fill="none" stroke="#2F2483" stroke-opacity=".5" stroke-width="1.2"/>' % d)
        else:
            drops.append('<path d="%s" fill="url(#gd)" fill-opacity="%.2f"/>' % (d, rnd.uniform(0.35, 0.85)))
    files["drops.svg"] = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d"><defs><linearGradient id="gd" x1="0" y1="0" x2="1" y2="1">'
                          '<stop offset="0" stop-color="#FFC200"/><stop offset="1" stop-color="#FC621C"/></linearGradient></defs>%s</svg>'
                          % (S, S, "".join(drops)))

    # rings: concentric hairlines with a dashed ring and diamonds, two colourways
    def rings(col):
        c = 300
        parts = ['<circle cx="%d" cy="%d" r="%d" stroke-opacity="%.2f"/>' % (c, c, r, op)
                 for r, op in ((290, .35), (240, .55), (236, .25), (170, .45), (110, .3))]
        parts.append('<circle cx="%d" cy="%d" r="205" stroke-dasharray="2 9" stroke-opacity=".7"/>' % (c, c))
        dia = "".join('<path d="M%d %d l7 -11 l7 11 l-7 11z" fill="%s" stroke="none" fill-opacity=".8"/>' % (x - 7, c, "#F8951A")
                      for x in (c - 240, c + 240))
        return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 600"><g fill="none" stroke="%s" stroke-width="1">%s</g>%s</svg>'
                % (col, "".join(parts), dia))
    files["rings-light.svg"] = rings("#FFFFFF")
    files["rings-dark.svg"] = rings("#2F2483")

    # ribbon: the swoosh outlined, echoed three times, drifting
    rib = []
    for i, (dx, dy, op) in enumerate(((0, 0, .9), (26, 18, .55), (52, 36, .3))):
        d, w = LO.part_path("swoosh", 420, 40 + dx, 40 + dy, -12)
        rib.append('<path d="%s" stroke-opacity="%.2f"/>' % (d, op))
    files["ribbon.svg"] = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 820 620"><defs>%s</defs>'
                           '<g fill="none" stroke="url(#g)" stroke-width="1.4">%s</g></svg>' % (grad, "".join(rib)))

    sizes = {}
    for name, svg in files.items():
        with open(os.path.join(out_dir, name), "w", encoding="utf-8") as f:
            f.write(svg)
        sizes[name] = len(svg)
    return sizes


# ------------------------------------------------------------------ logo + seal (vector, text outlined)
def _pdf_to_svg(draw, w, h, crop=True, pad=1.0):
    """draw(canvas) on a w x h point page -> SVG with text converted to outlines."""
    import pymupdf
    from reportlab.pdfgen import canvas as rl_canvas
    buf = io.BytesIO()
    c = rl_canvas.Canvas(buf, pagesize=(w, h))
    draw(c)
    c.showPage()
    c.save()
    doc = pymupdf.open(stream=buf.getvalue(), filetype="pdf")
    page = doc[0]
    if crop:
        rects = [d["rect"] for d in page.get_drawings()]
        for b in page.get_text("dict")["blocks"]:
            rects.append(pymupdf.Rect(b["bbox"]))
        r = rects[0]
        for x in rects[1:]:
            r |= x
        r = pymupdf.Rect(r.x0 - pad, r.y0 - pad, r.x1 + pad, r.y1 + pad) & page.rect
        page.set_cropbox(r)
    svg = page.get_svg_image(text_as_path=True)
    png_page = page
    return svg, doc, png_page


def _clean_svg(svg, label):
    svg = re.sub(r"<\?xml[^>]*>\s*", "", svg)
    svg = svg.replace("<svg ", '<svg role="img" aria-label="%s" ' % label, 1)
    svg = re.sub(r"(\.\d{4})\d+", r"\1", svg)   # glyph outlines come out at 8+ decimals; 4 is sub-pixel
    svg = svg.replace(' xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape"', "")
    return svg


def _build_logo_original():
    """The client's own logo, lifted as vector from their profile (logo_original.py)."""
    import logo_original as LO
    out = {}
    files = {
        "logo-mark.svg": LO.mark_svg("color", 100, gid="slm"),
        "logo-mark-rev.svg": LO.mark_svg("rev", 100, gid="slmr"),
        "logo-lockup.svg": LO.lockup_svg("color", 56, gid="sll"),
        "logo-lockup-rev.svg": LO.lockup_svg("rev", 56, gid="sllr"),
        "logo-full.svg": LO.full_svg("color", 140, gid="slf"),
        "logo-full-rev.svg": LO.full_svg("rev", 140, gid="slfr"),
    }
    for fn, (svg, w, h) in files.items():
        with open(os.path.join(IMG, fn), "w", encoding="utf-8") as f:
            f.write(svg)
        out[fn] = (round(w, 2), round(h, 2))
    svg, w, h = LO.mark_svg("color", 64, pad=3, gid="slv", square=True)
    with open(os.path.join(SITE, "favicon.svg"), "w", encoding="utf-8") as f:
        f.write(svg)
    # rasters come from the profile page itself, so the shading is MuPDF's render of the original
    for px, name, bg, pad in ((180, "apple-touch-icon.png", (255, 255, 255), 0.17),
                              (192, "icon-192.png", PAPER, 0.16), (512, "icon-512.png", PAPER, 0.16)):
        LO.render_png("mark", px, bg=bg, pad_frac=pad).convert("RGB").save(os.path.join(SITE, name), optimize=True)
    LO.render_png("mark", 256, pad_frac=0.03).save(os.path.join(SITE, "favicon.ico"),
                                                    sizes=[(16, 16), (32, 32), (48, 48)])
    out["mark_png"] = os.path.join(SITE, "icon-512.png")
    return out


def build_logo():
    if C.LOGO_CONCEPT == "original":
        return _build_logo_original()
    import logo_premium as LP
    concept = {c[1].split()[-1].lower(): c[2] for c in LP.CONCEPTS}[C.LOGO_CONCEPT]
    out = {}

    for mode in ("color", "rev"):
        # mark alone
        svg, doc, page = _pdf_to_svg(lambda c, m=mode: concept(c, 0, 0, 100, m), 100, 100)
        fn = "logo-mark%s.svg" % ("" if mode == "color" else "-rev")
        with open(os.path.join(IMG, fn), "w", encoding="utf-8") as f:
            f.write(_clean_svg(svg, C.BRAND))
        out[fn] = page.rect.width, page.rect.height

        # horizontal lock-up: mark + tracked wordmark
        def lockup(c, m=mode):
            concept(c, 0, 6, 62, m)
            LP.wordmark(c, 76, 44, 1.18, m, tagline=False)
        svg, doc, page = _pdf_to_svg(lockup, 360, 76)
        fn = "logo-lockup%s.svg" % ("" if mode == "color" else "-rev")
        with open(os.path.join(IMG, fn), "w", encoding="utf-8") as f:
            f.write(_clean_svg(svg, C.BRAND))
        out[fn] = page.rect.width, page.rect.height

    # favicons from the colour mark, rendered straight from vector
    import pymupdf
    svg, doc, page = _pdf_to_svg(lambda c: concept(c, 0, 0, 100, "color"), 100, 100)
    with open(os.path.join(SITE, "favicon.svg"), "w", encoding="utf-8") as f:
        f.write(_clean_svg(svg, C.BRAND))
    for px, name in ((180, "apple-touch-icon.png"), (192, "icon-192.png"), (512, "icon-512.png")):
        zoom = px / max(page.rect.width, page.rect.height)
        pix = page.get_pixmap(matrix=pymupdf.Matrix(zoom, zoom), alpha=False)
        im = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
        sq = Image.new("RGB", (px, px), PAPER if name != "apple-touch-icon.png" else INK)
        if name == "apple-touch-icon.png":       # iOS crops corners itself; fill with ink
            sq = Image.new("RGB", (px, px), INK)
            im = im.resize((px, px), Image.LANCZOS)
        sq.paste(im.resize((min(px, im.width), min(px, im.height)), Image.LANCZOS),
                 ((px - min(px, im.width)) // 2, (px - min(px, im.height)) // 2))
        sq.save(os.path.join(SITE, name), optimize=True)
    zoom = 64 / page.rect.width
    pix = page.get_pixmap(matrix=pymupdf.Matrix(zoom, zoom), alpha=True)
    ico = Image.frombytes("RGBA", (pix.width, pix.height), pix.samples)
    ico.save(os.path.join(SITE, "favicon.ico"), sizes=[(16, 16), (32, 32), (48, 48)])
    out["mark_png"] = os.path.join(SITE, "icon-512.png")
    return out


def build_seal():
    """Clean Quality Guaranteed: the client's S on navy (static) and a ring that rotates over it."""
    import logo_premium as LP
    from reportlab.lib.colors import HexColor
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont as RLTTFont
    try:
        pdfmetrics.getFont("MonaLabel")
    except KeyError:
        pdfmetrics.registerFont(RLTTFont("MonaLabel", mona("label")))
    amber, sun, white = HexColor("#F8951A"), HexColor("#FFC200"), HexColor("#FFFFFF")
    S = 200.0
    cx = cy = S / 2

    def ring(c):
        c.setStrokeColor(amber)
        c.setLineWidth(1.6)
        c.circle(cx, cy, 95, stroke=1, fill=0)
        c.setStrokeColor(white)
        c.setLineWidth(0.5)
        c.circle(cx, cy, 91, stroke=1, fill=0)
        c.circle(cx, cy, 70, stroke=1, fill=0)
        LP.arc_text(c, "CLEAN \u00b7 QUALITY", cx, cy, 77.5, "MonaLabel", 11.5, white, 2.2, bottom=False)
        LP.arc_text(c, "GUARANTEED", cx, cy, 85.5, "MonaLabel", 11.5, sun, 2.6, bottom=True)
        LP.diamond(c, cx - 80.5, cy, 3.6, amber)
        LP.diamond(c, cx + 80.5, cy, 3.6, amber)

    import logo_original as LO
    out = {}
    with open(os.path.join(IMG, "seal-core.svg"), "w", encoding="utf-8") as f:
        f.write(LO.seal_core_svg(S))
    out["seal-core.svg"] = (S, S)
    svg, doc, page = _pdf_to_svg(ring, S, S, crop=False)
    with open(os.path.join(IMG, "seal-ring.svg"), "w", encoding="utf-8") as f:
        f.write(_clean_svg(svg, "Clean Quality Guaranteed"))
    out["seal-ring.svg"] = (S, S)
    return out


# ------------------------------------------------------------------ photographs
def _ratio(a):
    w, h = a.split(":")
    return float(w) / float(h)


def _crop(im, aspect, focal):
    W, H = im.size
    r = _ratio(aspect)
    if W / H > r:
        cw, ch = int(round(H * r)), H
    else:
        cw, ch = W, int(round(W / r))
    fx, fy = focal
    x0 = int(round(fx * W - cw / 2))
    y0 = int(round(fy * H - ch / 2))
    x0 = max(0, min(W - cw, x0))
    y0 = max(0, min(H - ch, y0))
    return im.crop((x0, y0, x0 + cw, y0 + ch))


# sourced after v7 from somewhere other than Unsplash: they take the bright grade too
BRIGHT_SOURCES = {"pexels-4008563-tight.jpg"}


def _grade(im, background=False, bright=False):
    """One grade for the whole set so mixed sources read as one shoot:
    a touch warmer, saturation -10%, contrast +3%.
    v7 (22/11/2026, "vivid, bright, imply clean"): photos sourced from then on take the
    bright grade instead — lifted exposure, a cool fresh white, saturation +8%."""
    im = im.convert("RGB")
    if bright:
        r, g, b = im.split()
        r = r.point(lambda v: int(v * 0.985))
        b = b.point(lambda v: min(255, int(v * 1.02 + 2)))
        im = Image.merge("RGB", (r, g, b))
        im = ImageEnhance.Brightness(im).enhance(1.05)
        im = ImageEnhance.Color(im).enhance(1.08 if not background else 0.98)
        return ImageEnhance.Contrast(im).enhance(1.04)
    r, g, b = im.split()
    r = r.point(lambda v: min(255, int(v * 1.025)))
    b = b.point(lambda v: int(v * 0.975))
    im = Image.merge("RGB", (r, g, b))
    im = ImageEnhance.Color(im).enhance(0.88 if not background else 0.75)
    im = ImageEnhance.Contrast(im).enhance(1.03)
    return im


def _duotone(im):
    """Black-and-white source -> the brand's navy/indigo duotone with a warm highlight."""
    from PIL import ImageOps
    g = ImageOps.autocontrast(im.convert("L"), cutoff=1)
    return ImageOps.colorize(g, black=(8, 9, 32), mid=(47, 36, 131), white=(255, 224, 170), midpoint=120)


def _previous():
    try:
        with open(MANIFEST, encoding="utf-8") as f:
            return json.load(f).get("images", {})
    except (OSError, ValueError):
        return {}


PREVIOUS = _previous()


def _export(key, src, aspect, focal, display, quality=80, background=False, extra_large=None):
    path = os.path.join(SRC, src)
    if not os.path.exists(path):
        # media/all is gitignored, so a fresh clone has no originals. Reuse the WebP files
        # already built from this exact source; fail only when there is nothing to reuse.
        old = PREVIOUS.get(key)
        if (not FORCE and old and old.get("src") == src
                and all(os.path.exists(os.path.join(IMG, x["file"])) for x in old["files"])):
            return {k: v for k, v in old.items() if k not in ("alt", "caption")}
        raise SystemExit("image %s: source media/all/%s is missing and no built files match it" % (key, src))
    im = Image.open(path)
    im.load()
    cropped = _crop(im, aspect, focal)
    crop = (_duotone(cropped) if key.startswith("duo-")
            else _grade(cropped, background, bright=src.startswith("unsplash-") or src in BRIGHT_SOURCES))
    cw, ch = crop.size
    if background:
        wants = [960, 1440, 1920]
    elif key == "hero-wide":
        wants = [960, 1440, 1920]        # v9: full-bleed again (the Squeegee hero)
    elif key == "hero-tall":
        wants = [480, 760, 960]          # 760: a 412px phone at 1.75x needs 721px, so 720 tipped it to 960
    elif key == "hero":
        wants = [display, 700, int(round(display * 1.5)), 1000]   # 700 = phones at ~1.75x; 1000 caps it under 200 KB
    else:
        wants = [display, int(round(display * 1.5)), display * 2]
    if extra_large:
        wants.append(extra_large)
    widths = sorted({min(w, cw) for w in wants})
    files = []
    for w in widths:
        h = int(round(w * ch / cw))
        fn = "%s-%d.webp" % (key, w)
        dest = os.path.join(IMG, fn)
        if FORCE or not os.path.exists(dest):
            crop.resize((w, h), Image.LANCZOS).save(dest, "WEBP", quality=quality, method=6)
        files.append({"file": fn, "w": w, "h": h, "bytes": os.path.getsize(dest)})
    return {"src": src, "aspect": aspect, "display": display, "crop": [cw, ch], "files": files,
            "ratio": [files[0]["w"], files[0]["h"]]}


def build_images():
    out = {}
    for key, (src, aspect, focal, display, alt) in C.IMAGES.items():
        bg = key.endswith("-bg")
        q = 74 if key == "hero" else (60 if key == "hero-tall" else 68 if key == "hero-wide" else (66 if bg else 76))
        rec = _export(key, src, aspect, focal, display, quality=q, background=bg)
        rec["alt"] = alt
        out[key] = rec
    for key, src, aspect, focal, caption, alt in C.GALLERY:
        rec = _export(key, src, aspect, focal, 380, quality=78, extra_large=1400)
        rec["alt"] = alt
        rec["caption"] = caption
        out[key] = rec
    return out


# ------------------------------------------------------------------ share cards
def _font(path, size):
    return ImageFont.truetype(path, size)


def _gradient_bar(w, h):
    """The swoosh gradient from the client's logo, left to right."""
    stops = [(0, (255, 194, 0)), (.45, (248, 149, 26)), (1, (252, 98, 28))]
    bar = Image.new("RGB", (w, h))
    px = bar.load()
    for x in range(w):
        t = x / max(1, w - 1)
        for i in range(len(stops) - 1):
            a, ca = stops[i]
            b, cb = stops[i + 1]
            if a <= t <= b:
                k = (t - a) / (b - a)
                col = tuple(int(ca[j] + (cb[j] - ca[j]) * k) for j in range(3))
                break
        for y in range(h):
            px[x, y] = col
    return bar


def build_og(images):
    """1200x630: navy, the client's mark, the page H1 in Mona Sans Expanded, photo on the right."""
    import site_layout as L
    import logo_original as LO
    os.makedirs(OG, exist_ok=True)
    NAVY = (16, 18, 56)
    mark = LO.render_png("mark", 120, pad_frac=0.02)
    out = {}
    pages = L.PAGES + [p for p in L.UTILITY_PAGES if p["slug"] == "/privacy"]
    for pg in pages:
        slug = pg["slug"]
        key = C.PAGE_IMAGES.get(slug, "hero")
        rec = images[key]
        src = Image.open(os.path.join(IMG, rec["files"][-1]["file"])).convert("RGB")
        card = Image.new("RGB", (1200, 630), NAVY)
        photo = _crop(src, "480:630", (0.5, 0.5)).resize((480, 630), Image.LANCZOS)
        # the photo fades into the navy along its left edge
        fade = Image.linear_gradient("L").rotate(90).resize((480, 630))
        fade = fade.point(lambda v: min(255, int(v * 2.2)))
        card.paste(photo, (720, 0), fade)
        # a soft indigo glow behind the text
        glow = Image.new("RGB", (1200, 630), (47, 36, 131))
        gmask = Image.new("L", (1200, 630), 0)
        gd = ImageDraw.Draw(gmask)
        gd.ellipse([-260, -320, 640, 520], fill=120)
        from PIL import ImageFilter
        gmask = gmask.filter(ImageFilter.GaussianBlur(120))
        card.paste(glow, (0, 0), gmask)
        d = ImageDraw.Draw(card)
        # the colour mark on a white tile, as the client's own profile carries it on navy
        tile = Image.new("RGBA", (92, 92), (0, 0, 0, 0))
        ImageDraw.Draw(tile).rounded_rectangle([0, 0, 91, 91], radius=20, fill=(255, 255, 255, 255))
        small = mark.resize((64, 64), Image.LANCZOS)
        tile.alpha_composite(small, (14, 14))
        card.paste(tile, (64, 52), tile)
        d.text((176, 62), "SMARTLINE", font=_font(mona("display"), 34), fill=(255, 255, 255))
        d.text((178, 106), "POINT CLEANING HUB LTD", font=_font(mona("label"), 14), fill=(255, 194, 0))
        title = pg["h1"]
        size = 62 if len(title) < 26 else 50
        font = _font(mona("display"), size)
        words, lines, line = title.split(), [], ""
        for w in words:
            trial = (line + " " + w).strip()
            if d.textlength(trial, font=font) > 600 and line:
                lines.append(line)
                line = w
            else:
                line = trial
        lines.append(line)
        y = 262 if len(lines) <= 2 else 228
        for ln in lines[:4]:
            d.text((64, y), ln, font=font, fill=(255, 255, 255))
            y += int(size * 1.08)
        card.paste(_gradient_bar(96, 6), (66, y + 22))
        d.text((64, 556), C.DOMAIN, font=_font(mona("label"), 16), fill=(255, 255, 255))
        d.text((64, 580), "Assuring you the best", font=_font(mona("text"), 15), fill=(190, 192, 220))
        name = "home" if slug == "/" else slug.strip("/")
        dest = os.path.join(OG, name + ".jpg")
        card.save(dest, "JPEG", quality=86, optimize=True, progressive=True)
        out[slug] = {"file": "og/" + name + ".jpg", "bytes": os.path.getsize(dest)}
    return out


def main():
    os.makedirs(IMG, exist_ok=True)
    manifest = {}
    manifest["fonts"] = build_fonts()
    manifest["grain"] = build_grain()
    manifest["shapes"] = build_shapes()
    manifest["qr"] = build_qr()
    manifest["icons"] = build_icons()
    manifest["logo"] = build_logo()
    manifest["seal"] = build_seal()
    manifest["images"] = build_images()
    manifest["og"] = build_og(manifest["images"])
    with open(MANIFEST, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=1)
    n = sum(len(v["files"]) for v in manifest["images"].values())
    kb = sum(x["bytes"] for v in manifest["images"].values() for x in v["files"]) // 1024
    print("icons: %d in one sprite (%d bytes)" % (len(manifest["icons"]["icons"]), manifest["icons"]["bytes"]))
    print("logo: %s" % ", ".join(k for k in manifest["logo"] if k.endswith(".svg")))
    print("images: %d keys, %d files, %d KB" % (len(manifest["images"]), n, kb))
    print("share cards: %d" % len(manifest["og"]))


if __name__ == "__main__":
    main()
