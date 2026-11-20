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

Fonts are already instanced into site/assets/fonts (see README); nothing here
downloads at build time — the build is repeatable offline.
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


def build_logo():
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
    """Clean Quality Guaranteed: a static core and a ring that rotates over it."""
    import logo_premium as LP
    from reportlab.lib.colors import HexColor
    ink, brass, brass_lt, white = HexColor("#0E1430"), HexColor("#B8862F"), HexColor("#D7B468"), HexColor("#FFFFFF")
    S = 200.0
    cx = cy = S / 2

    def core(c):
        c.setFillColor(ink)
        c.circle(cx, cy, 99, stroke=0, fill=1)
        c.setStrokeColor(brass)
        c.setLineWidth(0.9)
        c.circle(cx, cy, 64, stroke=1, fill=0)
        c.setFont("Bodoni", 70)
        c.setFillColor(white)
        c.drawCentredString(cx, cy - 24, "S")
        c.setStrokeColor(brass_lt)
        c.setLineWidth(0.8)
        c.line(cx - 18, cy - 34, cx + 18, cy - 34)

    def ring(c):
        c.setStrokeColor(brass)
        c.setLineWidth(1.4)
        c.circle(cx, cy, 95, stroke=1, fill=0)
        c.setLineWidth(0.6)
        c.circle(cx, cy, 91, stroke=1, fill=0)
        c.setLineWidth(0.6)
        c.circle(cx, cy, 70, stroke=1, fill=0)
        LP.arc_text(c, "CLEAN \u00b7 QUALITY", cx, cy, 77, "Copper-B", 12.5, brass_lt, 2.6, bottom=False)
        LP.arc_text(c, "GUARANTEED", cx, cy, 86, "Copper-B", 12.5, brass_lt, 3.0, bottom=True)
        LP.diamond(c, cx - 80.5, cy, 3.4, brass)
        LP.diamond(c, cx + 80.5, cy, 3.4, brass)

    out = {}
    for name, fn in (("seal-core.svg", core), ("seal-ring.svg", ring)):
        svg, doc, page = _pdf_to_svg(fn, S, S, crop=False)
        with open(os.path.join(IMG, name), "w", encoding="utf-8") as f:
            f.write(_clean_svg(svg, "Clean Quality Guaranteed"))
        out[name] = (S, S)
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


def _grade(im, background=False):
    """One grade for the whole set so mixed sources read as one shoot:
    a touch warmer, saturation -10%, contrast +3%."""
    im = im.convert("RGB")
    r, g, b = im.split()
    r = r.point(lambda v: min(255, int(v * 1.025)))
    b = b.point(lambda v: int(v * 0.975))
    im = Image.merge("RGB", (r, g, b))
    im = ImageEnhance.Color(im).enhance(0.88 if not background else 0.75)
    im = ImageEnhance.Contrast(im).enhance(1.03)
    return im


def _export(key, src, aspect, focal, display, quality=80, background=False, extra_large=None):
    path = os.path.join(SRC, src)
    im = Image.open(path)
    im.load()
    crop = _grade(_crop(im, aspect, focal), background)
    cw, ch = crop.size
    if background:
        wants = [960, 1440, 1920]
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
        q = 74 if key == "hero" else (66 if bg else 76)
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


def build_og(images):
    import site_layout as L
    os.makedirs(OG, exist_ok=True)
    F = "C:/Windows/Fonts/"
    bodoni = F + "BOD_R.TTF"
    copper = F + "COPRGTB.TTF"
    mark = Image.open(os.path.join(SITE, "icon-192.png")).convert("RGB").resize((76, 76), Image.LANCZOS)
    out = {}
    pages = L.PAGES + [p for p in L.UTILITY_PAGES if p["slug"] == "/privacy"]
    for pg in pages:
        slug = pg["slug"]
        key = C.PAGE_IMAGES.get(slug, "hero")
        rec = images[key]
        src = Image.open(os.path.join(IMG, rec["files"][-1]["file"])).convert("RGB")
        card = Image.new("RGB", (1200, 630), INK)
        photo = _crop(src, "510:630", (0.5, 0.5)).resize((510, 630), Image.LANCZOS)
        card.paste(photo, (690, 0))
        d = ImageDraw.Draw(card)
        d.rectangle([688, 0, 690, 630], fill=BRASS)
        card.paste(mark, (64, 60))
        d.text((158, 74), "SMARTLINE", font=_font(copper, 30), fill=(255, 255, 255))
        d.text((159, 112), "POINT CLEANING HUB LTD", font=_font(copper, 15), fill=(215, 180, 104))
        title = pg["h1"]
        size = 64 if len(title) < 30 else 52
        font = _font(bodoni, size)
        words, lines, line = title.split(), [], ""
        for w in words:
            trial = (line + " " + w).strip()
            if d.textlength(trial, font=font) > 560 and line:
                lines.append(line)
                line = w
            else:
                line = trial
        lines.append(line)
        y = 250 if len(lines) <= 2 else 220
        for ln in lines[:4]:
            d.text((64, y), ln, font=font, fill=(255, 255, 255))
            y += int(size * 1.12)
        d.rectangle([64, y + 18, 124, y + 20], fill=BRASS)
        d.text((64, 560), C.DOMAIN, font=_font(copper, 17), fill=(215, 180, 104))
        name = "home" if slug == "/" else slug.strip("/")
        dest = os.path.join(OG, name + ".jpg")
        card.save(dest, "JPEG", quality=84, optimize=True, progressive=True)
        out[slug] = {"file": "og/" + name + ".jpg", "bytes": os.path.getsize(dest)}
    return out


def main():
    os.makedirs(IMG, exist_ok=True)
    manifest = {}
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
