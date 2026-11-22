# -*- coding: utf-8 -*-
"""Smartline — animated hero concepts for review (dev only, never deployed).

    python make_concepts.py     # -> dist/concepts/ (gitignored); view with serve_local.py:
                                #    http://127.0.0.1:8765/concepts/a  /b  /c

Each concept is the real home page with only the hero swapped, so a reviewer lands, sees the
entrance, then scrolls from the hero into the actual site. Styles and behaviour live in
concepts/concepts.css and concepts/concepts.js; once a concept is chosen it moves into
main.css / main.js and this file goes back to being a sketchbook.

  A  Squeegee     a misted photo is wiped clear beside a frosted panel; scroll settles it into a card
  B  Droplet      the logo's droplet falls in with the photo inside; scroll grows it to full screen
  C  Navy deck    navy statement, the accent word cycles services, a card deck fans out on scroll

Three tones throughout: white (base), navy/indigo (base), the swoosh orange (accent).
"""
import os
import re
import shutil

from PIL import Image

import build_assets as BA
import build_site as B
import logo_original as LO
import site_content as C
import site_layout as L

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "dist", "concepts")
SRC_DIR = os.path.join(ROOT, "concepts")
E = B.E

PHOTOS = {  # name -> (source in media/all, aspect, focal, widths)
    "a-wide": ("unsplash-vrNujj2iGGY.jpg", "16:10", (.5, .62), [1280, 1920]),
    "a-tall": ("unsplash-vrNujj2iGGY.jpg", "4:5", (.5, .66), [640, 900]),
    "b-wide": ("unsplash-7NvBEeHDY7M.jpg", "16:9", (.5, .5), [1280, 1920]),
    "b-tall": ("unsplash-7NvBEeHDY7M.jpg", "9:16", (.42, .5), [640, 900]),
    "c-office": ("unsplash-pYlBAu3de0w.jpg", "4:5", (.45, .55), [480, 720]),
    "c-home": ("unsplash-ooDvIpnXkwo.jpg", "4:5", (.5, .55), [480, 720]),
    "c-newbuild": ("unsplash-XKLZia7hPYI.jpg", "4:5", (.5, .55), [480, 720]),
    "c-compound": ("unsplash-BoVg3wUOJ_g.jpg", "4:5", (.5, .6), [480, 720]),
}
ALTS = {
    "a": "A bright glass lobby, its polished floor mirroring the columns and daylight",
    "b": "A bright open-plan living space, clean and ready for its owners",
    "c-office": "A bright open-plan office", "c-home": "A freshly made bed with white linen",
    "c-newbuild": "A newly fitted white kitchen ready for handover", "c-compound": "A freshly mown, striped lawn",
}


def export_photos():
    os.makedirs(os.path.join(OUT, "img"), exist_ok=True)
    made = {}
    for name, (src, aspect, focal, widths) in PHOTOS.items():
        im = Image.open(os.path.join(BA.SRC, src))
        im.load()
        crop = BA._grade(BA._crop(im, aspect, focal), bright=True)
        files = []
        for w in widths:
            w = min(w, crop.size[0])
            h = round(w * crop.size[1] / crop.size[0])
            fn = "%s-%d.webp" % (name, w)
            crop.resize((w, h), Image.LANCZOS).save(os.path.join(OUT, "img", fn), "WEBP", quality=78, method=6)
            files.append((fn, w, h))
        made[name] = files
    d, w = LO.part_path("droplet", 100)
    with open(os.path.join(OUT, "img", "droplet.svg"), "w", encoding="utf-8") as f:
        f.write('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %.2f 100" width="%.0f" height="1000">'
                '<path fill="#000" d="%s"/></svg>' % (w, w * 10, d))
    return made


def pic(made, wide, tall, alt, cls, sizes="100vw", eager=True):
    ss = lambda k: ", ".join("/concepts/img/%s %dw" % (fn, w) for fn, w, h in made[k])
    fn, w, h = made[wide][0]
    return ('<picture><source media="(max-width: 760px)" srcset="%s" sizes="100vw">'
            '<img class="%s" src="/concepts/img/%s" srcset="%s" sizes="%s" width="%d" height="%d" alt="%s"%s decoding="async"></picture>'
            % (ss(tall), cls, fn, ss(wide), sizes, w, h, E(alt), ' fetchpriority="high"' if eager else ' loading="lazy"'))


def one(made, k, alt):
    fn, w, h = made[k][-1]
    small = made[k][0]
    return ('<img src="/concepts/img/%s" srcset="/concepts/img/%s %dw, /concepts/img/%s %dw" sizes="(max-width: 760px) 44vw, 300px" '
            'width="%d" height="%d" alt="%s" decoding="async">' % (small[0], small[0], small[1], fn, w, w, h, E(alt)))


def copy_block(title_html, extra_cls=""):
    h = next(s for s in next(p for p in L.PAGES if p["slug"] == "/")["sections"] if s["id"] == "H-01")["p"]
    trust = "".join('<li>%s%s</li>' % (B.icon("check"), E(t)) for t in h["trust"])
    return ('<div class="cx__copy %s"><p class="label">Commercial · residential · post-construction · since 2018</p>'
            '<h1 class="cx__title" id="hero-title">%s</h1><p class="cx__lede">%s</p>'
            '<div class="btns"><a class="btn btn--sun btn--lg" href="%s">Request a quote %s</a>'
            '<a class="btn btn--ghost btn--lg" href="%s" target="_blank" rel="noopener">%s WhatsApp us</a></div>'
            '<ul class="cx__trust">%s</ul></div>'
            % (extra_cls, title_html, E(h["sub"]), B.quote_url(), B.icon("arrow-right"), E(C.wa_link()), B.icon("message-circle"), trust))


TITLE = ('<span class="ln"><span class="w">Where</span> <span class="w">cleanliness</span></span> '
         '<span class="ln"><span class="w">meets</span> <span class="w acc">excellence.</span></span>')


def hero_a(made):
    return ('<section class="cx cx-a" data-cx="a" aria-labelledby="hero-title"><div class="cx__pin">'
            '<div class="cxa__photo">%s</div>'
            '<div class="cxa__veil" aria-hidden="true"></div><div class="cxa__blade" aria-hidden="true"><i></i></div>'
            '<div class="cxa__panel" aria-hidden="true"></div>%s'
            '<div class="wrap cxa__inner">%s</div>'
            '<div class="cxa__end" aria-hidden="true"><p>Assuring you <em>the best.</em></p></div>'
            '<a class="cx__cue" href="#welcome"><i aria-hidden="true"></i>Scroll</a></div></section>'
            % (pic(made, "a-wide", "a-tall", ALTS["a"], "cxa__img"), B.fizz("hero", 10, 5), copy_block(TITLE)))


def hero_b(made):
    return ('<section class="cx cx-b" data-cx="b" aria-labelledby="hero-title"><div class="cx__pin">'
            '<div class="cxb__photo">%s<span class="cxb__shade" aria-hidden="true"></span></div>'
            '<span class="cxb__ripple" aria-hidden="true"></span><span class="cxb__ripple cxb__ripple--2" aria-hidden="true"></span>'
            '<div class="wrap cxb__inner">%s</div>'
            '<div class="cxb__end" aria-hidden="true"><p class="label">Assuring you the best</p>'
            '<p class="cxb__big">Spotless, fresh and <em>ready to use.</em></p></div>'
            '<a class="cx__cue" href="#welcome"><i aria-hidden="true"></i>Scroll</a></div></section>'
            % (pic(made, "b-wide", "b-tall", ALTS["b"], "cxb__img"), copy_block(TITLE, "cx__copy--center")))


WORDS = [("offices.", "c-office", "Offices & banks"), ("homes.", "c-home", "Homes & Airbnbs"),
         ("new builds.", "c-newbuild", "New builds"), ("compounds.", "c-compound", "Compounds & gardens")]


def hero_c(made):
    rot = "".join('<span class="cxc__word%s">%s</span>' % (" is-on" if i == 0 else "", E(w)) for i, (w, _, _) in enumerate(WORDS))
    title = ('<span class="ln"><span class="w">Spotless</span></span> '
             '<span class="ln"><span class="w cxc__rot" aria-live="off">%s</span></span>' % rot)
    cards = "".join('<figure class="cxc__card" data-k="%d">%s<figcaption>%s</figcaption></figure>'
                    % (i, one(made, k, ALTS[k]), E(cap)) for i, (_, k, cap) in enumerate(WORDS))
    return ('<section class="cx cx-c" data-cx="c" aria-labelledby="hero-title"><div class="cx__pin">'
            '<div class="cxc__bg" aria-hidden="true"><span class="cxc__glow"></span></div><span class="cxc__edge" aria-hidden="true"></span>'
            '<div class="wrap cxc__grid">%s<div class="cxc__deck" aria-hidden="true">%s</div></div>'
            '<a class="cx__cue" href="#welcome"><i aria-hidden="true"></i>Scroll</a></div></section>'
            % (copy_block(title), cards))


def switcher(cur):
    items = [("a", "A · Squeegee"), ("b", "B · Droplet"), ("c", "C · Navy deck")]
    links = "".join('<a href="/concepts/%s"%s>%s</a>' % (k, ' aria-current="page"' if k == cur else "", t) for k, t in items)
    return '<nav class="cxnav" aria-label="Hero concepts"><b>Hero concept</b>%s<a href="/">Live site</a></nav>' % links


def main():
    if os.path.isdir(OUT):
        shutil.rmtree(OUT)
    os.makedirs(OUT)
    made = export_photos()
    for fn in ("concepts.css", "concepts.js"):
        shutil.copy(os.path.join(SRC_DIR, fn), os.path.join(OUT, fn))
    pg = next(p for p in L.PAGES if p["slug"] == "/")
    faqs = pg["sections"][8]["p"]["items"]
    base = B.page(pg, B.home(pg), "/", None, faqs, index=False, key="home")
    base = re.sub(r'<link rel="preload" as="image"[^>]*>', "", base)
    v = str(int(os.path.getmtime(os.path.join(SRC_DIR, "concepts.css")) + os.path.getmtime(os.path.join(SRC_DIR, "concepts.js"))))
    for key, fn in (("a", hero_a), ("b", hero_b), ("c", hero_c)):
        html = re.sub(r'<section class="hero".*?</section>', lambda m: fn(made), base, count=1, flags=re.S)
        html = html.replace("</head>", '<link rel="stylesheet" href="/concepts/concepts.css?v=%s"></head>' % v, 1)
        html = html.replace("</body>", '%s<script src="/concepts/concepts.js?v=%s" defer></script></body>' % (switcher(key), v), 1)
        html = html.replace("<title>", "<title>Concept %s · " % key.upper(), 1)
        with open(os.path.join(OUT, key + ".html"), "w", encoding="utf-8") as f:
            f.write(html)
    with open(os.path.join(OUT, "index.html"), "w", encoding="utf-8") as f:
        f.write('<!doctype html><meta charset="utf-8"><meta http-equiv="refresh" content="0; url=/concepts/a"><a href="/concepts/a">Concepts</a>')
    print("concepts: /concepts/a  /concepts/b  /concepts/c  ->", OUT)


if __name__ == "__main__":
    main()
