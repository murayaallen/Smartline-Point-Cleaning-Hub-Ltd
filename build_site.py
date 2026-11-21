# -*- coding: utf-8 -*-
"""Smartline Point Cleaning Hub Ltd — static site generator.

    python build_assets.py      # once, or when images/logo change
    python build_site.py        # writes site/ and verifies it

Reads site_layout.py (structure), site_content.py (copy, config, images),
seo_plan.py (keywords) and build_cache/assets.json (image sizes). Writes plain
HTML, so the deploy is: upload site/ to public_html. The output is committed —
a deploy never depends on someone remembering to run this.

verify() runs last and fails the build on: a broken internal link or anchor, a
missing image or icon, an <img> without alt/width/height, an inline style or
inline script (the CSP forbids both), a page without exactly one H1, a title or
description outside its limits, JSON-LD that does not parse, a form control
without a label, any leftover placeholder, fumigation, or a blown size budget.
"""
import hashlib
import html
import json
import os
import re
import sys
from html.parser import HTMLParser
from urllib.parse import quote, urlparse

import site_content as C
import site_layout as L
import seo_plan as SEO
import logo_original as LO

ROOT = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.join(ROOT, "site")
MAN = json.load(open(os.path.join(ROOT, "build_cache", "assets.json"), encoding="utf-8"))
E = lambda s: html.escape(str(s), quote=True)


def ver(path):
    with open(os.path.join(SITE, path.lstrip("/")), "rb") as f:
        return hashlib.sha1(f.read()).hexdigest()[:8]


def minify_js(name):
    """assets/js/<name>.js is the hand-written source; ship <name>.min.js: block comments out,
    indentation and blank lines gone, line breaks kept (no ASI surprises)."""
    src = open(os.path.join(SITE, "assets/js/%s.js" % name), encoding="utf-8").read()
    out = re.sub(r"/\*.*?\*/", "", src, flags=re.S)
    out = "\n".join(l.strip() for l in out.splitlines() if l.strip()) + "\n"
    with open(os.path.join(SITE, "assets/js/%s.min.js" % name), "w", encoding="utf-8", newline="\n") as f:
        f.write(out)


minify_js("main")
minify_js("wipe")          # loaded on demand by main.js when the wipe section comes near
minify_js("fx")            # mouse-only effects, loaded at idle on pointer devices
V_CSS, V_BOOT, V_JS = ver("assets/css/main.css"), ver("assets/js/boot.js"), ver("assets/js/main.min.js")
V_WIPE = ver("assets/js/wipe.min.js")
V_FX = ver("assets/js/fx.min.js")
SPRITE = "/assets/img/icons.svg?v=" + ver("assets/img/icons.svg")


def slug(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


def icon(name, cls=""):
    return ('<svg class="icon %s" aria-hidden="true" focusable="false"><use href="%s#i-%s"></use></svg>'
            % (cls, SPRITE, name)).replace('class="icon "', 'class="icon"')


SERVICES = [s for _, _, items in L.GROUPS for s, _ in items]
SERVICE_LINK = {s: (link or "/services#" + slug(s)) for _, _, items in L.GROUPS for s, link in items}
GROUP_ANCHOR = {g: a.split("#")[1] for g, a, _ in L.GROUPS}
# home "Why Smartline": one photo per reason (none of them used elsewhere on the home page)
REASON_IMAGE = ["svc-onetime", "about-hero", "why", "ra-hero", "svc-deep", "pc-standard"]
GROUP_IMAGE = {"Commercial & institutional": "svc-commercial", "Homes & apartments": "svc-apartment",
               "Specialist cleans": "svc-postcon", "Outdoor": "svc-landscaping"}
QQ_SERVICES = {
    "/commercial-cleaning": ["Commercial cleaning", "Office carpet cleaning", "School cleaning", "Church cleaning",
                             "Toilet bowl & sink cleaning"],
    "/residential-apartment-cleaning": ["Residential cleaning", "Apartment cleaning", "Move in / move out cleaning",
                                        "Sofa set & upholstery cleaning", "Deep cleaning"],
    "/post-construction-cleaning": ["Post-construction cleaning", "Deep cleaning", "One-time cleaning"],
}
TRAINING_ICON = {"Proper communication": "messages-square", "Equipment use": "wrench", "Chemical handling": "flask-conical",
                 "Grooming and PPE": "shirt", "Teamwork": "users", "Code of conduct": "scale"}


def file_for(slug_):
    return "index.html" if slug_ == "/" else slug_.strip("/") + ".html"


def quote_url(service=None):
    return "/contact" + ("?service=" + quote(service) if service else "") + "#quote"


# ================================================================== images
def img(key, sizes, cls="", eager=False, alt=None, decorative=False):
    rec = MAN["images"][key]
    files = rec["files"]
    srcset = ", ".join("/assets/img/%s %dw" % (f["file"], f["w"]) for f in files)
    fallback = files[min(1, len(files) - 1)]
    a = "" if decorative else E(alt if alt is not None else rec["alt"])
    attrs = ['src="/assets/img/%s"' % fallback["file"], 'srcset="%s"' % srcset, 'sizes="%s"' % sizes,
             'width="%d"' % files[0]["w"], 'height="%d"' % files[0]["h"], 'alt="%s"' % a]
    if eager:
        attrs += ['fetchpriority="high"', 'decoding="async"']
    else:
        attrs += ['loading="lazy"', 'decoding="async"']
    if cls:
        attrs.insert(0, 'class="%s"' % cls)
    return "<img %s>" % " ".join(attrs)


def logo(fn, h, alt="", lazy=False, cls=""):
    """<img> for a logo file at height h, width from the file's real proportions."""
    w0, h0 = MAN["logo"][fn]
    return '<img%s src="/assets/img/%s" width="%d" height="%d" alt="%s"%s>' % (
        (' class="%s"' % cls) if cls else "", fn, round(w0 * h / h0), h, E(alt), ' loading="lazy"' if lazy else "")


def hero_picture():
    """Art-directed hero: a tall crop for phones, a wide one for everything else."""
    tall, wide = MAN["images"]["hero-tall"], MAN["images"]["hero-wide"]
    ss = lambda rec: ", ".join("/assets/img/%s %dw" % (f["file"], f["w"]) for f in rec["files"])
    fb = wide["files"][1]
    return ('<picture><source media="(max-width: 760px)" srcset="%s" sizes="100vw">'
            '<img class="hero__img" src="/assets/img/%s" srcset="%s" sizes="100vw" width="%d" height="%d" alt="%s" '
            'fetchpriority="high" decoding="async"></picture>'
            % (ss(tall), fb["file"], ss(wide), wide["files"][0]["w"], wide["files"][0]["h"], E(wide["alt"])))


def largest(key):
    return "/assets/img/" + MAN["images"][key]["files"][-1]["file"]


# ================================================================== shared chrome
def page_transition():
    """The loading screen between pages: a navy panel with the client's S and a loading line."""
    return ('<div class="pt" aria-hidden="true"><div class="pt__panel"></div><div class="pt__mark">%s'
            '<span class="pt__bar"><span></span></span></div></div>' % LO.mark_parts_svg(64, "pt__s", "ptg"))


def loader():
    """First visit per session: the client's S assembles — swoosh, body, droplet — then the
    screen wipes away diagonally like a squeegee pass. CSS-driven; main.js only removes it."""
    words = "".join("<span>%s</span> " % w for w in "Assuring you the best".split())
    return ('<div class="loader" aria-hidden="true"><div class="loader__stage">%s'
            '<p class="loader__tag">%s</p></div><span class="loader__line"></span></div>'
            % (LO.mark_parts_svg(104, "loader__mark", "ldg"), words.strip()))


def mega():
    cols = []
    for i, (g, anchor, items) in enumerate(L.GROUPS):
        links = "".join('<li><a href="%s">%s%s</a></li>' % (SERVICE_LINK[s], E(s), icon("arrow-right")) for s, _ in items)
        cols.append('<div class="mega__col"><p class="mega__n">%02d</p><h3>%s</h3><ul>%s</ul></div>' % (i + 1, E(g), links))
    return ('<div class="mega" id="mega-services"><div class="mega__grid">%s'
            '<a class="mega__feature" href="%s"><span class="label label--sun">Site visit</span>'
            '<b>Not sure what you need?</b><span>We see the space, then price it in writing.</span>'
            '<span class="mega__go">Book a visit %s</span></a></div>'
            '<div class="mega__foot"><span>Thirteen services, one point of contact, one invoice.</span>'
            '<a class="link-arrow" href="/services">See all services %s</a></div></div>'
            % ("".join(cols), quote_url(), icon("arrow-right"), icon("arrow-right")))


NAV = [("/", "Home"), ("/about", "About"), ("/services", "Services"), ("/clients", "Clients"), ("/contact", "Contact")]


def header(current):
    items = []
    for href, label in NAV:
        cur = ' aria-current="page"' if href == current or (href == "/services" and current in QQ_SERVICES) else ""
        if href == "/services":
            items.append('<li class="nav__item nav__item--mega"><button class="nav__link" type="button" aria-expanded="false" '
                         'aria-controls="mega-services"%s>Services %s</button>%s</li>' % (cur, icon("chevron-down"), mega()))
        else:
            items.append('<li class="nav__item"><a class="nav__link" href="%s"%s>%s</a></li>' % (href, cur, label))
    return ('<header class="hdr"><div class="wrap hdr__inner">'
            '<a class="brand" href="/" aria-label="%s, home">%s%s</a>'
            '<nav class="nav" aria-label="Main"><ul class="nav__list">%s</ul></nav>'
            '<div class="hdr__actions"><a class="hdr__phone" href="tel:%s">%s<span>%s</span></a>'
            '<a class="btn btn--sun btn--sm hdr__cta" href="%s" data-magnetic>Get a quote %s</a>'
            '<button class="hdr__burger" type="button" aria-label="Open menu" aria-expanded="false" aria-controls="drawer">'
            '<span></span><span></span></button></div></div>'
            '<div class="hdr__progress" aria-hidden="true"><span></span></div></header>'
            % (E(C.SHORT), logo("logo-lockup-rev.svg", 44, cls="brand__rev"), logo("logo-lockup.svg", 44, cls="brand__col"),
               "".join(items), C.PHONE_E164, icon("phone"), E(C.PHONE), quote_url(), icon("arrow-right")))


def drawer():
    acc = "".join('<li><a href="%s">%s</a></li>' % (SERVICE_LINK[s], E(s)) for s in SERVICES)
    return ('<div class="drawer" id="drawer" hidden><div class="drawer__scrim" data-close-drawer></div>'
            '<div class="drawer__panel" role="dialog" aria-modal="true" aria-label="Menu">'
            '<div class="drawer__top">%s'
            '<button class="drawer__close" type="button" aria-label="Close menu" data-close-drawer>%s</button></div>'
            '<nav class="drawer__nav" aria-label="Mobile"><a href="/"><small>01</small>Home</a><a href="/about"><small>02</small>About</a>'
            '<details class="drawer__acc"><summary><small>03</small>Services %s</summary><ul><li><a href="/services">All services</a></li>%s</ul></details>'
            '<a href="/clients"><small>04</small>Clients</a><a href="/contact"><small>05</small>Contact</a></nav>'
            '<div class="drawer__foot"><a class="btn btn--sun btn--block" href="%s">Request a quote %s</a>'
            '<a class="btn btn--glass btn--block" href="%s" target="_blank" rel="noopener">%s WhatsApp us</a>'
            '<p>Call %s<br>%s</p></div></div></div>'
            % (logo("logo-lockup-rev.svg", 40, C.BRAND), icon("x"), icon("plus"), acc, quote_url(), icon("arrow-right"),
               E(C.wa_link()), icon("message-circle"), E(C.PHONE), C.EMAIL))


def footer():
    svc = "".join('<li><a href="%s">%s</a></li>' % (h, E(t)) for h, t in [
        ("/commercial-cleaning", "Commercial cleaning"), ("/residential-apartment-cleaning", "Homes & apartments"),
        ("/post-construction-cleaning", "Post-construction"), ("/services#specialist", "Deep & one-time cleans"),
        ("/services#outdoor", "Landscaping"), ("/services", "All 13 services")])
    co = "".join('<li><a href="%s">%s</a></li>' % (h, E(t)) for h, t in [
        ("/about", "About Smartline"), ("/clients", "Clients"), ("/contact", "Request a quote"),
        ("mailto:%s?subject=%s" % (C.CAREERS_EMAIL, quote("Job application")), "Careers"),
        ("/privacy", "Privacy notice")])
    contact = ('<li><a href="tel:%s">%s%s</a></li><li><a href="%s" target="_blank" rel="noopener">%sWhatsApp %s</a></li>'
               '<li><a href="mailto:%s">%s%s</a></li><li><span>%s%s, %s</span></li><li><span>%s%s</span></li>'
               % (C.PHONE_E164, icon("phone"), E(C.PHONE), E(C.wa_link()), icon("message-circle"), E(C.PHONE),
                  C.EMAIL, icon("mail"), C.EMAIL, icon("map-pin"), E(C.STREET), E(C.LOCALITY), icon("file-text"), E(C.POSTAL)))
    cookie_btn = '<button type="button" data-cookie-settings>Cookie settings</button>' if C.GA_ID else ""
    return ('<footer class="ftr"><span class="glow glow--a" aria-hidden="true"></span>'
            '<div class="wrap"><div class="ftr__top"><p class="ftr__big" data-reveal>Assuring you <span class="grad">the best.</span></p>'
            '<div class="btns"><a class="btn btn--sun" href="%s" data-magnetic>Request a quote %s</a>'
            '<a class="btn btn--glass" href="%s" target="_blank" rel="noopener">%s WhatsApp us</a></div></div>'
            '<div class="ftr__grid"><div class="ftr__brand">%s'
            '<p>Commercial, residential and post-construction cleaning, and landscaping, across Nairobi and Kiambu since %s.</p>'
            '<span class="ftr__badge">%s Clean Quality Guaranteed</span></div>'
            '<div><h2>Services</h2><ul>%s</ul></div><div><h2>Company</h2><ul>%s</ul></div>'
            '<div><h2>Contact</h2><ul>%s</ul></div></div>'
            '<div class="ftr__bar"><span>&copy; %s %s. All rights reserved.</span>'
            '<nav aria-label="Legal"><a href="/privacy">Privacy notice</a>%s<span>Website by Allen Muraya Maina</span></nav></div></div>'
            '<p class="ftr__word" aria-hidden="true">SMARTLINE</p></footer>'
            % (quote_url(), icon("arrow-right"), E(C.wa_link()), icon("message-circle"),
               logo("logo-lockup-rev.svg", 50, C.BRAND, lazy=True), C.FOUNDED, icon("shield-check"), svc, co, contact,
               C.YEAR, E(C.BRAND), cookie_btn))


def actionbar():
    return ('<nav class="actionbar" aria-label="Quick contact"><a href="tel:%s">%sCall</a>'
            '<a href="%s" target="_blank" rel="noopener">%sWhatsApp</a><a class="is-quote" href="%s">%sGet a quote</a></nav>'
            '<a class="wa-float" href="%s" target="_blank" rel="noopener" aria-label="WhatsApp us">%s<span class="wa-float__tip">WhatsApp us</span></a>'
            % (C.PHONE_E164, icon("phone"), E(C.wa_link()), icon("message-circle"), quote_url(), icon("send"),
               E(C.wa_link()), icon("message-circle")))


def cookie_bar():
    if not C.GA_ID:
        return ""
    return ('<div class="cookie" role="region" aria-label="Cookie notice" hidden><p>We use analytics cookies to understand '
            'how the site is used. Nothing else, and only if you agree. <a class="link-u" href="/privacy">Privacy notice</a></p>'
            '<div class="btns"><button class="btn btn--sun btn--sm" type="button" data-consent="granted">Accept</button>'
            '<button class="btn btn--ghost btn--sm" type="button" data-consent="denied">Decline</button></div></div>')


# ================================================================== reusable blocks
def eyebrow(t, cls=""):
    return '<p class="label%s">%s</p>' % ((" " + cls) if cls else "", E(t))


def sec_head(eb, title, text="", center=False, h="h2", size="d2", tag_id=""):
    ident = ' id="%s"' % tag_id if tag_id else ""
    return ('<div class="sec-head%s">%s<%s class="%s"%s data-split>%s</%s>%s</div>'
            % (" sec-head--center" if center else "", eyebrow(eb) if eb else "", h, size, ident, title, h,
               '<p class="lede" data-reveal>%s</p>' % text if text else ""))


def crumbs(trail):
    lis = []
    for i, (href, label) in enumerate(trail):
        if i == len(trail) - 1:
            lis.append('<li><span aria-current="page">%s</span></li>' % E(label))
        else:
            lis.append('<li><a href="%s">%s</a></li>' % (href, E(label)))
    return '<nav aria-label="Breadcrumb"><ol class="crumbs">%s</ol></nav>' % "".join(lis)


SHAPE_DIM = {"waves": (1600, 360), "drops": (640, 640), "rings-light": (600, 600), "rings-dark": (600, 600), "ribbon": (820, 620)}


def shape(name, cls):
    """One of the generated vector shapes (build_assets.build_shapes), decorative."""
    w, h = SHAPE_DIM[name]
    return ('<img class="shape %s" src="/assets/img/shapes/%s.svg" width="%d" height="%d" alt="" loading="lazy" decoding="async">'
            % (cls, name, w, h))


def waves(pos="b"):
    """Wiped-streak lines along the top or bottom edge of a light section."""
    return '<div class="shapes" aria-hidden="true">%s</div>' % shape("waves", "shape--waves-" + pos)


def bg_depth(mark=True, ribbon=False, hero=False):
    """The navy 'depth' background system: two drifting glows, a dot field, the S watermark,
    and optionally the logo's swoosh as a ribbon, or the hero's seal rings and droplets."""
    wm = ('<img class="wm" src="/assets/img/logo-mark-rev.svg" width="353" height="400" alt="" loading="lazy">' if mark else "")
    extra = (shape("ribbon", "shape--ribbon") if ribbon else "") + (
        shape("rings-light", "shape--hero-rings") + shape("drops", "shape--hero-drops") if hero else "")
    return ('<div class="depth" aria-hidden="true"><span class="glow glow--a"></span><span class="glow glow--b"></span>'
            '<span class="dots"></span>%s%s</div>' % (wm, extra))


TICK = ('<svg class="record__tick" viewBox="0 0 24 24" aria-hidden="true" focusable="false">'
        '<circle cx="12" cy="12" r="10.5" pathLength="1"/><path d="M7 12.4l3.3 3.3L17 9" pathLength="1"/></svg>')


def training_record(foot="Refreshed on the job by a named supervisor"):
    """Six training areas as one record card; the ticks draw in sequence when it scrolls in."""
    rows = "".join('<li class="record__row"><span class="ico">%s</span><div><b>%s</b><span>%s</span></div>%s</li>'
                   % (icon(TRAINING_ICON[t]), E(t), E(dsc), TICK) for t, dsc in L.TRAINING)
    return ('<div class="record" data-reveal><div class="record__head"><span class="record__t">Training record</span>'
            '<span class="record__stamp">Before placement</span></div><ol class="record__list">%s</ol>'
            '<div class="record__foot"><img src="/assets/img/logo-mark.svg" width="26" height="29" alt="" loading="lazy">'
            '<span>%s</span></div></div>' % (rows, E(foot)))


def bg_photo(key, side="right", cls=""):
    """A photo laid into the white space of a light section: faded, masked into the page."""
    return ('<div class="bgph bgph--%s%s" aria-hidden="true"><div class="bgph__in">%s</div></div>'
            % (side, (" " + cls) if cls else "", img(key, "(max-width: 760px) 100vw, 60vw", decorative=True).replace("<img ", '<img fetchpriority="low" ', 1)))


def orbs(kind="a"):
    """Soft colour drifting behind a light section (the logo's sun and indigo, heavily blurred)."""
    return '<div class="orbs orbs--%s" aria-hidden="true"><span></span><span></span><span></span></div>' % kind


def faq_block(items, eb, title, text, link=True):
    rows = "".join('<details class="faq__item"><summary><span class="faq__q">%s</span><span class="faq__pm" aria-hidden="true"></span></summary>'
                   '<div class="faq__a"><p>%s</p></div></details>' % (E(q), E(C.FAQ[q])) for q in items)
    more = ('<a class="link-arrow" href="/contact">Ask us something else %s</a>' % icon("arrow-right")) if link else ""
    return ('<div class="wrap faq-wrap"><div class="faq-wrap__head">%s<h2 class="d2" data-split>%s</h2><p class="lede" data-reveal>%s</p>%s</div>'
            '<div class="faq" data-reveal>%s</div></div>' % (eyebrow(eb), E(title), E(text), more, rows))


def cta_band(heading="Book your clean today", sub=None, eb="Assuring you the best", bg="cta-bg"):
    sub_html = ('<p class="lede">%s</p>' % E(sub)) if sub else '<p class="lede">Call, WhatsApp or send the form. We reply within one working day.</p>'
    run = "".join('<span>%s</span><i aria-hidden="true"></i>' % E(heading) for _ in range(4))
    return ('<section class="cta" aria-label="%s"><div class="cta__bg" aria-hidden="true">%s%s<span class="glow glow--a"></span>'
            '<span class="glow glow--sun"></span></div>'
            '<div class="marquee marquee--cta" aria-hidden="true" data-marquee="-0.6"><div class="marquee__track">'
            '<div class="marquee__group">%s</div><div class="marquee__group">%s</div></div></div>'
            '<div class="wrap cta__grid"><div>%s<h2 class="d1 cta__title" data-split>%s</h2>%s</div>'
            '<div class="cta__side" data-reveal><a class="cta__phone" href="tel:%s"><small>Call or WhatsApp</small>%s</a>'
            '<div class="btns"><a class="btn btn--sun" href="%s" data-magnetic>Request a quote %s</a>'
            '<a class="btn btn--glass" href="%s" target="_blank" rel="noopener">%s WhatsApp us</a></div></div></div></section>'
            % (E(heading), img(bg, "100vw", decorative=True), shape("rings-light", "shape--cta-rings"), run, run, eyebrow(eb, "label--sun"), E(heading), sub_html,
               C.PHONE_E164, E(C.PHONE), quote_url(), icon("arrow-right"), E(C.wa_link()), icon("message-circle")))


def chips(items, link=None, cls=""):
    out = []
    for it in items:
        href = link(it) if link else None
        if href:
            out.append('<a class="chip %s" href="%s">%s</a>' % (cls, href, E(it)))
        else:
            out.append('<span class="chip %s">%s</span>' % (cls, E(it)))
    return '<div class="chips" data-stagger>%s</div>' % "".join(out).replace('class="chip "', 'class="chip"')


def timeline(items):
    """Numbered steps on a line that draws itself as the section scrolls in."""
    lis = "".join('<li class="tl__item" data-reveal><span class="tl__n">%02d</span><h3 class="h3">%s</h3><p>%s</p></li>'
                  % (i + 1, E(t), E(dsc)) for i, (t, dsc) in enumerate(items))
    return '<ol class="tl tl--%d" data-stagger><span class="tl__line" aria-hidden="true"><span></span></span>%s</ol>' % (len(items), lis)


def seal(cls="seal"):
    return ('<div class="%s" aria-hidden="true"><img src="/assets/img/seal-core.svg" width="200" height="200" alt="">'
            '<img class="seal__ring" src="/assets/img/seal-ring.svg" width="200" height="200" alt=""></div>' % cls)


def page_hero(trail, h1, lede, image=None, chips_html="", tex=False, service=False, eb=None, btns="", bg_key=None):
    if bg_key:
        tex = True
    bg = img(bg_key or "page-bg", "100vw", decorative=True, eager=True) if tex else ""
    media = ""
    if image:
        media = ('<figure class="phero__media" data-reveal="wipe"><div class="phero__frame">%s</div></figure>'
                 % img(image, "(max-width: 1040px) 92vw, 600px", eager=True))
    cls = "phero" + (" phero--tex" if tex else "") + (" phero--service" if service else "") + (" phero--media" if image else "")
    inner = ('<div class="phero__text">%s%s<h1 class="d1" data-split>%s</h1><p class="lede" data-reveal>%s</p>%s%s</div>'
             % (crumbs(trail) if trail else "", eyebrow(eb, "label--sun") if eb else "", E(h1), E(lede),
                ('<div data-reveal>%s</div>' % btns) if btns else "", chips_html))
    return ('<section class="%s"><div class="phero__bg" aria-hidden="true">%s</div>%s'
            '<div class="wrap phero__grid">%s%s</div></section>' % (cls, bg, bg_depth(hero=True), inner, media))


# ================================================================== forms
def select(name, options, label, required=True, value=None, ident=None):
    ident = ident or "f-" + name
    opts = '<option value="">Choose&hellip;</option>' + "".join(
        '<option%s>%s</option>' % (' selected' if o == value else "", E(o)) for o in options)
    return ('<div class="field field--select"><label for="%s">%s%s</label><select id="%s" name="%s"%s aria-describedby="%s-err">%s</select>'
            '<span class="field__err" id="%s-err"></span></div>'
            % (ident, E(label), ' <span class="req" aria-hidden="true">*</span>' if required else "", ident, name,
               " required" if required else "", ident, opts, ident))


def field(name, label, typ="text", required=False, full=False, auto=None, extra="", ident=None, textarea=False):
    ident = ident or "f-" + name
    req = " required" if required else ""
    ac = ' autocomplete="%s"' % auto if auto else ""
    if textarea:
        ctrl = '<textarea id="%s" name="%s" rows="4" maxlength="1500" aria-describedby="%s-err"%s></textarea>' % (ident, name, ident, req)
    else:
        ctrl = ('<input id="%s" name="%s" type="%s"%s%s%s aria-describedby="%s-err">'
                % (ident, name, typ, req, ac, extra, ident))
    return ('<div class="field%s"><label for="%s">%s%s</label>%s<span class="field__err" id="%s-err"></span></div>'
            % (" field--full" if full else "", ident, E(label),
               ' <span class="req" aria-hidden="true">*</span>' if required else ' <span class="muted">(optional)</span>',
               ctrl, ident))


def hidden_bits(ret, form_name):
    return ('<input type="hidden" name="form" value="%s"><input type="hidden" name="return" value="%s">'
            '<input type="hidden" name="t" value="">'
            '<div class="hp" aria-hidden="true"><label for="hp-%s">Leave this empty</label>'
            '<input id="hp-%s" type="text" name="website" tabindex="-1" autocomplete="off"></div>' % (form_name, ret, form_name, form_name))


def consent(ident):
    return ('<div class="consent"><input id="%s" type="checkbox" name="consent" value="yes" required aria-describedby="%s-err">'
            '<label for="%s">I agree to Smartline contacting me about this request. <a class="link-u" href="/privacy">How we use your details</a></label>'
            '<span class="field__err" id="%s-err"></span></div>' % (ident, ident, ident, ident))


def quote_form():
    s1 = (select("service", SERVICES, "Service needed") + select("property", C.PROPERTY_TYPES, "Type of premises")
          + field("location", "Location or estate", required=True, auto="address-level2", extra=' maxlength="120"')
          + select("frequency", C.FREQUENCIES, "How often", required=False)
          + field("date", "Preferred start date", typ="date", full=True))
    s2 = (field("name", "Full name", required=True, auto="name", extra=' maxlength="100"')
          + field("phone", "Phone (WhatsApp)", typ="tel", required=True, auto="tel", extra=' inputmode="tel" maxlength="20"')
          + field("email", "Email", typ="email", auto="email", extra=' maxlength="120"')
          + field("organisation", "Organisation", auto="organization", extra=' maxlength="120"')
          + field("message", "Anything we should know", full=True, textarea=True)
          + consent("f-consent"))
    return ('<form class="form-card js-form" id="quote" action="/form/enquiry.php" method="post" novalidate>'
            '<div class="form-card__head"><p class="label">Request a quote</p><h2 class="d3">Tell us about the job</h2>'
            '<p class="muted">Two short steps. We reply within one working day.</p></div>'
            '<div class="progress" aria-hidden="true"><span class="progress__step is-on"><b>1</b>The job</span>'
            '<span class="progress__step"><b>2</b>You</span><span class="progress__bar"><span></span></span></div>'
            '%s<fieldset class="fstep" data-step="1"><legend>The job</legend>%s</fieldset>'
            '<fieldset class="fstep" data-step="2"><legend>Your details</legend>%s</fieldset>'
            '<div class="form-actions"><button class="btn btn--sun" type="button" data-next hidden>Continue %s</button>'
            '<button class="btn btn--ghost" type="button" data-back hidden>Back</button>'
            '<button class="btn btn--sun" type="submit" data-submit>Send request %s</button></div>'
            '<p class="form-msg" id="form-msg" role="alert" data-phone="%s" hidden></p>'
            '<ul class="proofbox"><li>%sTrusted by Uwezo Microfinance Bank, St Christopher&rsquo;s International School and Jewel Complex</li>'
            '<li>%s%s</li><li>%sTrained, uniformed, supervised teams</li></ul></form>'
            % (hidden_bits("/contact", "quote"), s1, s2, icon("arrow-right"), icon("send"), E(C.PHONE),
               icon("building-2"), icon("shield-check"), E(C.GUARANTEE_SHORT), icon("badge-check")))


def quick_quote(slug_, nav):
    opts = QQ_SERVICES[slug_]
    fid = slug(nav)
    grid = (field("name", "Full name", required=True, auto="name", ident="qq-name", extra=' maxlength="100"')
            + field("phone", "Phone (WhatsApp)", typ="tel", required=True, auto="tel", ident="qq-phone",
                    extra=' inputmode="tel" maxlength="20"')
            + field("location", "Location or estate", required=True, auto="address-level2", ident="qq-location",
                    extra=' maxlength="120"')
            + select("service", opts, "Service", value=opts[0], ident="qq-service")
            + '<button class="btn btn--sun" type="submit">Get my quote %s</button>' % icon("arrow-right"))
    return ('<section class="sec sec--paper" aria-labelledby="qq-%s"><div class="wrap"><form class="qq js-form" data-reveal action="/form/enquiry.php" method="post" novalidate>'
            '<div class="qq__head"><div><p class="label">Quick quote</p><h2 class="d3" id="qq-%s">Get a quote for %s</h2></div>'
            '<p>Three details and we call you back within one working day.</p></div>%s'
            '<input type="hidden" name="property" value="Other"><div class="qq__grid">%s</div>%s'
            '<p class="form-msg" id="form-msg" role="alert" data-phone="%s" hidden></p></form></div></section>'
            % (fid, fid, E(nav.lower()), hidden_bits(slug_, "qq"), grid, consent("qq-consent"), E(C.PHONE)))


# ================================================================== pages
def home(pg):
    S = {s["id"]: s for s in pg["sections"]}
    h = S["H-01"]["p"]
    trust = "".join('<li>%s%s</li>' % (icon("check"), E(t)) for t in h["trust"])
    out = ['<section class="hero" aria-labelledby="hero-title"><div class="hero__media" aria-hidden="true">%s'
           '<span class="hero__fog"></span><span class="hero__blade"></span></div>'
           '<div class="hero__shade" aria-hidden="true"></div><span class="hero__sheen" aria-hidden="true"></span>'
           '<div class="wrap hero__inner"><div class="hero__copy">%s'
           '<h1 class="hero__title" id="hero-title"><span class="ln"><span class="w">Where</span> <span class="w">cleanliness</span></span> '
           '<span class="ln"><span class="w">meets</span> <span class="w grad">excellence.</span></span></h1>'
           '<p class="hero__lede">%s</p><div class="btns hero__btns"><a class="btn btn--sun btn--lg" href="%s" data-magnetic>Request a quote %s</a>'
           '<a class="btn btn--glass btn--lg" href="%s" target="_blank" rel="noopener">%s WhatsApp us</a></div>'
           '<ul class="hero__trust">%s</ul></div>%s</div>'
           '<div class="hero__foot"><div class="wrap hero__foot-in"><a class="hero__cue" href="#welcome"><i aria-hidden="true"></i>Scroll to explore</a>'
           '<span class="hero__where">Kasarani, Nairobi &middot; serving Nairobi &amp; Kiambu</span></div></div></section>'
           % (hero_picture(), eyebrow("Commercial · residential · post-construction · since 2018", "label--sun"),
              E(h["sub"]), quote_url(), icon("arrow-right"), E(C.wa_link()), icon("message-circle"), trust,
              seal("seal hero__seal"))]

    # trusted-by: the client names run past in display type
    names = "".join("<span>%s</span><i aria-hidden=\"true\"></i>" % E(n) for n, _ in L.CLIENTS)
    out.append('<section class="trusted" aria-label="Trusted by"><div class="wrap trusted__head"><p class="label">Trusted by</p>'
               '<a class="link-arrow" href="/clients">All clients %s</a></div>'
               '<div class="marquee marquee--names" data-marquee="0.5"><div class="marquee__track">'
               '<div class="marquee__group">%s</div><div class="marquee__group" aria-hidden="true">%s</div></div></div></section>'
               % (icon("arrow-right"), names, names))

    # welcome — the client's own words, lit word by word as you read down
    w = S["H-03"]["p"]
    body = E(w["body"])
    for phrase in ("cleanliness meets excellence", "spotless", "fresh", "healthier, happier", "satisfaction"):
        body = body.replace(phrase, '<span class="kw">%s</span>' % phrase, 1)
    head = E(w["heading"]).replace("every clean.", '<span class="grad">every clean.</span>')
    out.append('<section class="sec welcome" id="welcome">%s%s<span class="tiles" aria-hidden="true"></span>'
               '<div class="welcome__draw" aria-hidden="true">%s</div><div class="wrap">'
               '<div class="welcome__head">%s<h2 class="d2 welcome__title" data-split>%s</h2></div>'
               '<p class="statement" data-scrub>%s</p>'
               '<div class="welcome__foot" data-reveal><div class="signature"><img src="/assets/img/logo-mark.svg" width="39" height="44" alt="" loading="lazy">'
               '<span>Assuring you the best</span></div><a class="btn btn--ghost" href="/about">About Smartline %s</a></div></div></section>'
               % (bg_photo("cc-hero", "right", "bgph--tall"), orbs("a"), LO.mark_outline_svg(560, "draw-s", "dso"),
                  eyebrow("Welcome"), head, body, icon("arrow-right")))

    # services — a pinned horizontal rail on desktop, a swipe deck on phones
    cards = []
    for i, (g, anchor, items) in enumerate(L.GROUPS):
        lis = "".join("<li>%s</li>" % E(s) for s, _ in items)
        cards.append('<article class="rcard" data-glow><a class="rcard__link" href="%s" aria-label="Explore %s"></a>'
                     '<div class="rcard__img">%s</div><div class="rcard__body"><span class="rcard__n">%02d<small>/%02d</small></span>'
                     '<h3 class="d4">%s</h3><p>%s</p><ul class="rcard__list">%s</ul>'
                     '<span class="link-arrow">Explore %s</span></div></article>'
                     % (anchor, E(g), img(GROUP_IMAGE[g], "(max-width: 760px) 84vw, 460px"), i + 1, len(L.GROUPS), E(g),
                        E(C.HOME_SERVICE_BLURB[g]), lis, icon("arrow-right")))
    sched = "".join('<span class="chip chip--dark">%s</span>' % E(x) for x in L.SCHEDULES)
    cards.append('<article class="rcard rcard--end"><div class="rcard__body"><p class="label label--sun">Schedules</p>'
                 '<h3 class="d3">Once, or on a schedule</h3><div class="chips">%s</div>'
                 '<a class="btn btn--sun" href="/services">See all 13 services %s</a></div></article>' % (sched, icon("arrow-right")))
    out.append('<section class="rail" id="services" aria-labelledby="h-services">' + orbs("b") + waves("t") + '<div class="rail__pin"><div class="wrap rail__head">'
               '<div>%s<h2 class="d2" id="h-services" data-split>What we clean</h2></div>'
               '<p class="lede" data-reveal>Thirteen services across offices, institutions, homes and new builds &mdash; one point of contact for all of them.</p>'
               '<div class="rail__meter" aria-hidden="true"><span class="rail__count">01</span><span class="rail__bar"><span></span></span><span>05</span></div></div>'
               '<div class="rail__viewport"><div class="rail__track">%s</div></div></div></section>'
               % (eyebrow("Services"), "".join(cards)))

    # why — bento
    rx_imgs = "".join('<figure class="rx__img%s" data-rx-img>%s</figure>'
                      % (" is-on" if i == 0 else "", img(REASON_IMAGE[i], "(max-width: 1040px) 92vw, 600px"))
                      for i in range(len(L.WHY)))
    rx_items = "".join(
        '<li class="rx__item%s" data-rx-item><h3 class="rx__h"><button class="rx__btn" type="button" id="rx-b%d" aria-controls="rx-p%d" aria-expanded="%s">'
        '<span class="rx__n">%02d</span><span class="rx__t">%s</span><span class="rx__pm" aria-hidden="true"></span></button></h3>'
        '<div class="rx__p" id="rx-p%d" role="region" aria-labelledby="rx-b%d"><div><p>%s</p></div></div>'
        '<span class="rx__bar" aria-hidden="true"><span></span></span></li>'
        % (" is-on" if i == 0 else "", i + 1, i + 1, "true" if i == 0 else "false", i + 1, E(t), i + 1, i + 1, E(dsc))
        for i, (t, dsc) in enumerate(L.WHY))
    out.append('<section class="sec sec--white why" id="why">%s%s<div class="wrap">%s<div class="rx" data-rx>'
               '<div class="rx__stage" aria-hidden="true">%s<div class="rx__cap"><span class="rx__count"><b data-rx-now>01</b> / %02d</span>'
               '<span class="rx__title" data-rx-title>%s</span></div></div><ol class="rx__list">%s</ol></div></div></section>'
               % (orbs("c"), waves("b"), sec_head("Why Smartline", "Why clients stay with Smartline",
                                      "Six reasons, each one something you can hold us to."),
                  rx_imgs, len(L.WHY), E(L.WHY[0][0]), rx_items))

    # how we work — pinned scrollytelling
    steps = S["H-06"]["p"]["items"]
    lis = "".join('<li class="sx__item" data-sx-item><span class="sx__n">%02d</span><div><h3 class="d4">%s</h3><p>%s</p></div></li>'
                  % (i + 1, E(t), E(dsc)) for i, (t, dsc) in enumerate(steps))
    out.append('<section class="sec sec--navy sx" id="how">%s<div class="wrap sx__grid"><div class="sx__sticky">%s'
               '<div class="sx__meter" aria-hidden="true"><span class="sx__now">01</span><span class="sx__of">/ %02d</span></div>'
               '<div class="sx__bar" aria-hidden="true"><span></span></div></div><ol class="sx__list">%s</ol></div></section>'
               % (bg_depth(ribbon=True), sec_head("How we work", "From first call to a standard that holds",
                                       "Five steps, the same on every contract &mdash; so the clean in month twelve matches the clean in week one."),
                  len(steps), lis))

    # training
    out.append('<section class="sec sec--white training">' + orbs("a") + '<div class="wrap split"><figure class="split__media" data-reveal="wipe">'
               '<div class="frame" data-parallax-box>%s</div><figcaption class="tag">%s Trained before placement</figcaption></figure>'
               '<div>%s%s</div></div></section>'
               % (img("training", "(max-width: 1040px) 92vw, 560px"), icon("badge-check"),
                  sec_head("Training", "Every Smartline cleaner is trained in"), training_record()))

    # the finish — wipe the glass (the window photo, misted; the visitor clears it)
    out.append('<section class="sec sec--navy wipe" id="finish" aria-labelledby="h-finish">%s<div class="wrap wipe__grid"><div class="wipe__copy">%s'
               '<h2 class="d2" id="h-finish" data-split>Clean you can <span class="grad">see through.</span></h2>'
               '<p class="lede" data-reveal>Glass shows every shortcut. It is where a hurried clean gives itself away &mdash; and where ours '
               'should not. Clear the pane and see the standard we work to on every visit.</p>'
               '<div class="btns" data-reveal><button class="btn btn--sun wipe__go" type="button" data-wipe-go>%s<span class="wipe__go-t">Wipe it clean</span></button>'
               '<a class="btn btn--glass" href="%s">Book a clean %s</a></div>'
               '<p class="wipe__note" data-reveal>%sOn a phone, drag a finger across the glass. On a computer, just move the cursor over it.</p></div>'
               '<figure class="wipe__stage" data-wipe="/assets/js/wipe.min.js?v=%s">%s<canvas class="wipe__fog" aria-hidden="true"></canvas>'
               '<span class="wipe__hint" aria-hidden="true"><i></i>Wipe the glass</span>'
               '<span class="wipe__done" aria-hidden="true">%sStreak-free</span><span class="wipe__bar" aria-hidden="true"><span></span></span>'
               '</figure></div></section>'
               % (bg_depth(mark=False, ribbon=True), eyebrow("The finish"), icon("scan-search"), quote_url(), icon("arrow-right"),
                  icon("arrow-right"), V_WIPE, img("wipe", "(max-width: 1040px) 92vw, 560px"), icon("circle-check")))

    # guarantee
    g = S["H-08"]["p"]
    pts = "".join("<li>%s</li>" % E(x) for x in g["points"])
    out.append('<section class="sec sec--sun guarantee"><span class="glow glow--sun" aria-hidden="true"></span>' + bg_photo("svc-washroom", "right") + '<div class="wrap guarantee__grid">'
               '<div class="guarantee__seal" data-reveal>%s</div><div>%s<h2 class="d2" data-split>%s</h2>'
               '<p class="promise" data-reveal>%s</p><ul class="ticks" data-stagger>%s</ul>'
               '<a class="btn btn--navy" href="%s" data-magnetic>Book a clean with the guarantee %s</a></div></div></section>'
               % (seal("seal seal--lg"), eyebrow("Our promise"), E(g["heading"]), E(g["promise"]), pts, quote_url(), icon("arrow-right")))

    out.append('<section class="sec sec--paper faqsec">%s%s</section>'
               % (bg_photo("svc-residential", "left", "bgph--low"), faq_block(S["H-09"]["p"]["items"], "Questions", "Questions we are asked",
                           "The things clients ask before they book. Anything else, call or WhatsApp.")))
    out.append(cta_band(bg="duo-team-bg"))
    return "".join(out)


def spec_table(rows, caption):
    trs = "".join('<div class="spec__row" data-reveal><dt>%s</dt><dd>%s</dd></div>' % (E(k), E(v)) for k, v in rows)
    return '<dl class="spec" aria-label="%s">%s</dl>' % (E(caption), trs)


def about(pg):
    S = {s["id"]: s for s in pg["sections"]}
    out = [page_hero([("/", "Home"), ("/about", "About")], "About Smartline", S["A-01"]["p"]["sub"], image="about-hero",
                     eb="Est. 2018 · Kasarani, Nairobi", bg_key="duo-team-bg")]
    st = S["A-02"]["p"]
    out.append('<section class="sec sec--white story"><div class="wrap split"><div>%s<h2 class="d2" data-split>%s</h2>'
               '<p class="body-lg" data-reveal>%s</p><p class="body-lg" data-reveal>%s</p></div>'
               '<figure class="split__media" data-reveal="wipe"><div class="frame" data-parallax-box>%s</div>'
               '<figcaption class="story__year" aria-hidden="true">2018</figcaption></figure></div></section>'
               % (eyebrow("Our story"), E(st["heading"]), E(st["body"]), E(C.ABOUT_STORY_2), img("story", "(max-width: 1040px) 92vw, 560px")))
    vm = "".join('<article class="vcard" data-glow data-reveal><p class="label label--sun">%s</p><p class="vcard__text">%s</p></article>'
                 % (E(t), E(lines[0])) for t, lines, _ in S["A-03"]["p"]["items"])
    out.append('<section class="sec sec--navy">%s<div class="wrap">%s<div class="vgrid" data-stagger>%s</div></div></section>'
               % (bg_depth(ribbon=True), sec_head("Purpose", "Vision and mission"), vm))
    ap = S["A-04"]["p"]
    out.append('<section class="sec sec--paper approach">' + bg_photo("svc-commercial", "right", "bgph--tall") + orbs("b") + '<span class="tiles" aria-hidden="true"></span><div class="wrap">%s<h2 class="d3" data-split>%s</h2>'
               '<p class="statement" data-scrub>%s</p></div></section>' % (eyebrow("Our approach"), E(ap["heading"]), E(ap["body"])))
    out.append('<section class="sec sec--white training">%s<div class="wrap split split--rev"><figure class="split__media" data-reveal="wipe">'
               '<div class="frame" data-parallax-box>%s</div><figcaption class="tag">%s Equipment, chemicals, conduct</figcaption></figure>'
               '<div>%s%s</div></div></section>'
               % (orbs("b"), img("svc-carpet", "(max-width: 1040px) 92vw, 560px"), icon("badge-check"),
                  sec_head("Training", "How our cleaners are trained",
                           "Six areas, covered before anyone is placed on a site &mdash; and refreshed by the supervisor on the job."),
                  training_record()))
    out.append('<section class="sec sec--paper"><div class="wrap">%s<div class="facts-wrap">%s'
               '<aside class="doc-card" data-reveal><span class="ico">%s</span><h3 class="h3">Supplier documents</h3>'
               '<p>Procurement teams can request our registration documents and anything else their supplier process needs.</p>'
               '<a class="btn btn--navy btn--sm" href="mailto:%s?subject=%s">Request documents %s</a></aside></div></div></section>'
               % (sec_head("Vetting and supervision", "Who comes into your building",
                           "The questions a facility manager asks before awarding a contract, answered plainly."),
                  spec_table(C.COMPLIANCE, "How we vet and supervise"), icon("file-text"), C.EMAIL,
                  quote("Supplier documents request"), icon("arrow-right")))
    out.append('<section class="sec sec--white"><div class="wrap split split--rev"><div>%s<h2 class="d2" data-split>%s</h2><p class="body-lg" data-reveal>%s</p></div>'
               '<figure class="split__media" data-reveal="wipe"><div class="frame" data-parallax-box>%s</div></figure></div></section>'
               % (eyebrow("Community"), E(S["A-07"]["p"]["heading"]), E(C.COMMUNITY), img("community", "(max-width: 1040px) 92vw, 560px")))
    wk = S["A-08"]["p"]
    out.append('<section class="sec sec--navy careers">%s<div class="wrap careers__grid"><div>%s<h2 class="d2" data-split>%s</h2></div>'
               '<div data-reveal><p class="body-lg">%s</p><div class="btns"><a class="btn btn--sun" href="mailto:%s?subject=%s" data-magnetic>Apply to join the team %s</a></div></div></div></section>'
               % (bg_depth(False), eyebrow("Careers", "label--sun"), E(wk["heading"]), E(wk["body"]), C.CAREERS_EMAIL,
                  quote("Job application"), icon("arrow-right")))
    rows = [("Registered name", C.BRAND), ("Established", C.FOUNDED), ("Office", C.STREET + ", " + C.LOCALITY),
            ("Postal", C.POSTAL), ("Phone", C.PHONE), ("Email", C.EMAIL)]
    out.append('<section class="sec sec--white"><div class="wrap">%s<div class="facts-wrap">%s'
               '<aside class="doc-card" data-reveal><span class="ico">%s</span><h3 class="h3">Company profile</h3>'
               '<p>Our company profile, for supplier files and boards.</p><a class="btn btn--navy btn--sm" href="mailto:%s?subject=%s">Request a copy %s</a></aside></div></div></section>'
               % (sec_head("Company details", "The facts for your supplier form"), spec_table(rows, "Company details"),
                  icon("file-text"), C.EMAIL, quote("Company profile request"), icon("arrow-right")))
    out.append(cta_band())
    return "".join(out)


# "Find your service": premises -> photo + the services usually booked for it (CSS-only tabs)
PREMISES = [
    ("office", "Office", "g-glass", ["Commercial cleaning", "Office carpet cleaning", "Toilet bowl & sink cleaning", "Deep cleaning"],
     "Daily or weekly cleaning on a written schedule, with carpets and washrooms on their own rota."),
    ("bank", "Bank or branch", "cc-hero", ["Commercial cleaning", "Office carpet cleaning", "Deep cleaning"],
     "Banking halls and back offices, cleaned around opening hours."),
    ("school", "School", "g-wetfloor", ["School cleaning", "Toilet bowl & sink cleaning", "Landscaping", "Deep cleaning"],
     "Classrooms, washrooms and dining halls, plus a deep clean between terms."),
    ("church", "Church", "g-polish", ["Church cleaning", "Office carpet cleaning", "Landscaping"],
     "Before and after services and events, with the compound kept as neat as the hall."),
    ("home", "Home", "g-upholstery", ["Residential cleaning", "Sofa set & upholstery cleaning", "Deep cleaning", "Move in / move out cleaning"],
     "Regular cleans, sofas and the occasional top-to-bottom clean."),
    ("airbnb", "Apartment or Airbnb", "ra-hero", ["Apartment cleaning", "One-time cleaning", "Sofa set & upholstery cleaning"],
     "Turnovers between guests and linen changes, timed to check-in."),
    ("newbuild", "New build", "g-newbuild", ["Post-construction cleaning", "Deep cleaning", "One-time cleaning"],
     "Builders' dust to handover-ready, phased to your handover date."),
    ("compound", "Compound", "g-compound", ["Landscaping", "Commercial cleaning"],
     "Lawns, hedges and common areas kept to the same standard as the inside."),
]


def premises_picker():
    radios = "".join('<input class="pf__r" type="radio" name="pf" id="pf-%s"%s>' % (k, " checked" if i == 0 else "")
                     for i, (k, _, _, _, _) in enumerate(PREMISES))
    tabs = "".join('<label class="chip pf__tab" for="pf-%s">%s</label>' % (k, E(lbl)) for k, lbl, _, _, _ in PREMISES)
    panels = []
    for k, lbl, key, svcs, line in PREMISES:
        links = "".join('<li><a href="%s">%s%s</a></li>' % (SERVICE_LINK[x] if SERVICE_LINK[x].startswith("/services#") is False else SERVICE_LINK[x],
                                                           E(x), icon("arrow-right")) for x in svcs)
        panels.append('<div class="pf__panel" data-p="%s"><figure class="pf__img">%s</figure><div class="pf__body">'
                      '<p class="label">Usually booked for %s</p><p class="pf__line">%s</p><ul class="pf__list">%s</ul>'
                      '<a class="btn btn--sun" href="%s">Get a quote for your %s %s</a></div></div>'
                      % (k, img(key, "(max-width: 760px) 92vw, 560px"), E(lbl.lower()), E(line), links,
                         quote_url(svcs[0]), E(lbl.split(" or ")[0].lower()), icon("arrow-right")))
    return ('<section class="sec sec--white pfsec" aria-labelledby="h-pf">%s%s<div class="wrap">%s'
            '<div class="pf" data-reveal>%s<div class="pf__tabs" role="radiogroup" aria-label="Type of premises">%s</div>'
            '<div class="pf__panels">%s</div></div></div></section>'
            % (orbs("c"), waves("b"), sec_head("Find your service", "Start with your premises",
                                                "Pick the kind of building and we will show you what is usually booked for it.",
                                                tag_id="h-pf"), radios, tabs, "".join(panels)))


def services(pg):
    S = {s["id"]: s for s in pg["sections"]}
    hero = S["S-01"]["p"]
    ch = chips([g for g, _, _ in L.GROUPS], link=lambda g: "#" + GROUP_ANCHOR[g], cls="chip--glass")
    out = [page_hero([("/", "Home"), ("/services", "Services")], "Our services", hero["sub"], chips_html=ch,
                     eb="13 services · one point of contact", image="trolley", bg_key="duo-kitchen-bg")]
    sub = "".join('<li><a href="#%s"><small>%02d</small>%s</a></li>' % (GROUP_ANCHOR[g], i + 1, E(g)) for i, (g, _, _) in enumerate(L.GROUPS))
    out.append('<nav class="subnav" aria-label="Service groups"><div class="wrap"><ul class="subnav__list">%s</ul></div></nav>' % sub)
    out.append(premises_picker())
    blurb = {"Commercial & institutional": "Offices, banks, schools and churches, cleaned on a written schedule.",
             "Homes & apartments": "Houses, apartments and short-stay units, regular or once.",
             "Specialist cleans": "The jobs a routine clean is not built for.",
             "Outdoor": "Because the compound is the first thing anyone sees."}
    for i, (g, anchor, items) in enumerate(L.GROUPS):
        rows = []
        for s, link in items:
            line, incl, who = L.SERVICE_COPY[s]
            tag = '<span class="srow__tag">Dedicated page</span>' if link else ""
            second = ('<a class="btn btn--ghost btn--sm" href="%s">View service %s</a>' % (link, icon("arrow-right"))) if link else (
                '<a class="btn btn--ghost btn--sm" href="%s" target="_blank" rel="noopener">%s WhatsApp</a>' % (E(C.wa_link(s)), icon("message-circle")))
            rows.append('<article class="srow" id="%s" data-reveal data-glow><div class="srow__img">%s</div><div class="srow__body"><h3 class="d4">%s %s</h3>'
                        '<p>%s</p>%s<p class="srow__who"><b>For:</b> %s</p></div>'
                        '<div class="srow__actions"><a class="btn btn--sun btn--sm" href="%s">Get a quote %s</a>%s</div></article>'
                        % (slug(s), img(C.SERVICE_IMAGE[s], "(max-width: 760px) 92vw, 320px"), E(s), tag, E(line),
                           chips(incl, cls="chip--sm"), E(who), quote_url(s), icon("arrow-right"), second))
        bg = " sec--white" if i % 2 == 0 else " sec--paper"
        gid = GROUP_ANCHOR[g]
        out.append('<section class="sec group%s" id="%s" aria-labelledby="h-%s"><div class="wrap"><div class="group-head">'
                   '<span class="group-head__n" aria-hidden="true">%02d</span><div>%s<h2 class="d2" id="h-%s" data-split>%s</h2></div><p data-reveal>%s</p></div>'
                   '<div class="srows">%s</div></div></section>'
                   % (bg, gid, gid, i + 1, eyebrow("Group %02d" % (i + 1)), gid, E(g), E(blurb[g]), "".join(rows)))
    tiers = []
    for n, (title, for_, key, desc) in enumerate(C.PRICING_MODELS):
        if C.PRICES and C.PRICES.get(key):
            unit = {"visit": "per visit", "month": "per month", "sqm": "per m²"}[key]
            fig = '<p class="tier__fig">From KES %s <small>%s</small></p>' % (E(C.PRICES[key]), unit)
        else:
            fig = '<p class="tier__fig">Quoted to your space</p>'
        tiers.append('<article class="tier%s" data-glow data-reveal><span class="tier__n">%02d</span><h3 class="d4">%s</h3><p class="tier__for">%s</p>%s<p>%s</p>'
                     '<a class="btn btn--%s btn--sm" href="%s">Get a figure %s</a></article>'
                     % (" tier--feature" if n == 1 else "", n + 1, E(title), E(for_), fig, E(desc),
                        "sun" if n == 1 else "ghost", quote_url(), icon("arrow-right")))
    note = ("Prices exclude VAT where it applies. The final figure follows a site visit." if C.PRICES else
            "Send photographs on WhatsApp for a one-off clean and we can often price it the same day.")
    out.append('<section class="sec sec--navy">%s<div class="wrap">%s<div class="tiers" data-stagger>%s</div><p class="foot-note" data-reveal>%s</p></div></section>'
               % (bg_depth(ribbon=True), sec_head("Pricing", "How we price",
                                       "Three ways a job is priced. The figure is always in writing before any work starts."),
                  "".join(tiers), E(note)))
    sect = S["S-08"]["p"]["items"]
    out.append('<section class="sec sec--white"><div class="wrap two-head"><div>%s</div><div>%s</div></div></section>'
               % (sec_head("Sectors", "Premises we already clean",
                           "Every one of these is a building type we clean today. Tap one to see who we clean it for."),
                  chips(sect, link=lambda c: "/clients?sector=" + C.CHIP_TO_SECTOR[c] if c in C.CHIP_TO_SECTOR else "/post-construction-cleaning", cls="chip--lg")))
    out.append('<section class="sec sec--paper"><div class="wrap two-head"><div>%s</div><div>%s</div></div></section>'
               % (sec_head("Schedules", "Once, or on a schedule",
                           "From a single move-out clean to a full annual programme for your premises."), chips(L.SCHEDULES, cls="chip--lg")))
    out.append(cta_band("Not sure what you need?", "Book a site visit — we will scope it with you.", "Site visit"))
    return "".join(out)


def service_page(pg):
    slug_ = pg["slug"]
    pre = {"/commercial-cleaning": "CC", "/residential-apartment-cleaning": "RA", "/post-construction-cleaning": "PC"}[slug_]
    S = {s["id"]: s for s in pg["sections"]}
    hp = S[pre + "-01"]["p"]
    btns = ('<div class="btns"><a class="btn btn--sun" href="%s" data-magnetic>Request a quote %s</a>'
            '<a class="btn btn--glass" href="%s" target="_blank" rel="noopener">%s WhatsApp us</a></div>'
            % (quote_url(QQ_SERVICES[slug_][0]), icon("arrow-right"), E(C.wa_link(pg["nav"])), icon("message-circle")))
    hero_bg = {"/commercial-cleaning": "office-mop", "/residential-apartment-cleaning": "duo-kitchen-bg",
               "/post-construction-cleaning": "duo-team-bg"}[slug_]
    out = [page_hero([("/", "Home"), ("/services", "Services"), (slug_, pg["nav"])], pg["h1"], hp["sub"],
                     image=C.PAGE_IMAGES[slug_], service=True, btns=btns, bg_key=hero_bg)]
    intro = C.SERVICE_INTRO[slug_]
    who = S[pre + "-02"]["p"]["items"]
    intro_bg = {"CC": "g-glass", "RA": "g-upholstery", "PC": "g-debris"}[pre]
    out.append('<section class="sec sec--white">%s%s<div class="wrap intro"><div>%s<h2 class="d2" data-split>Who we do this for</h2>'
               '%s</div><div>%s</div></div></section>'
               % (bg_photo(intro_bg, "right", "bgph--low"), waves("b"), eyebrow("Overview"), chips(who, cls="chip--lg"),
                  "".join('<p class="body-lg" data-reveal>%s</p>' % E(p) for p in intro)))
    groups = S[pre + "-03"]["p"]["groups"]
    blocks = "".join('<div class="scope__group"><h3 class="scope__h"><span>%02d</span>%s</h3><ul class="scope__list">%s</ul></div>'
                     % (i + 1, E(t), "".join("<li>%s%s</li>" % (TICK, E(x)) for x in xs)) for i, (t, xs) in enumerate(groups))
    out.append('<section class="sec sec--paper"><span class="tiles" aria-hidden="true"></span><div class="wrap">%s'
               '<div class="record scope" data-reveal><div class="record__head"><span class="record__t">Scope of work &middot; %s</span>'
               '<span class="record__stamp">Agreed in writing</span></div><div class="scope__cols">%s</div>'
               '<div class="record__foot"><img src="/assets/img/logo-mark.svg" width="26" height="29" alt="" loading="lazy">'
               '<span>Checked against on every visit &middot; signed off by a named supervisor</span>'
               '<a class="link-arrow scope__cta" href="%s">Get this scoped for your premises %s</a></div></div></div></section>'
               % (sec_head("Scope", "What is included",
                           "Agreed in writing before the first visit, and checked against on every visit after it."),
                  E(pg["nav"]), blocks, quote_url(QQ_SERVICES[slug_][0]), icon("arrow-right")))
    out.append('<section class="sec sec--navy">%s<div class="wrap">%s%s</div></section>'
               % (bg_depth(ribbon=True), sec_head("Method", "How it runs"), timeline(S[pre + "-04"]["p"]["items"])))
    stp = S[pre + "-05"]["p"]
    out.append('<section class="sec sec--white"><div class="wrap split"><figure class="split__media" data-reveal="wipe"><div class="frame" data-parallax-box>%s</div>'
               '<figcaption class="tag">%s %s</figcaption></figure>'
               '<div>%s<h2 class="d2" data-split>%s</h2><p class="body-lg" data-reveal>%s</p><ul class="ticks" data-stagger><li>Worked against the written scope</li>'
               '<li>Signed off by a named supervisor before the team leaves</li><li>Missed something? Tell us within 24 hours and we come back</li></ul></div></div></section>'
               % (img(C.STANDARD_IMAGE[pre], "(max-width: 1040px) 92vw, 560px"), icon("shield-check"), E(C.GUARANTEE_SHORT),
                  eyebrow("The standard"), E(stp["heading"]), E(stp["body"])))
    out.append('<section class="sec sec--paper"><div class="wrap two-head"><div>%s</div><div>%s</div></div></section>'
               % (sec_head("Schedules", "Once, or on a schedule"), chips(L.SCHEDULES, cls="chip--lg")))
    out.append('<section class="sec sec--white">%s</section>'
               % faq_block(S[pre + "-07"]["p"]["items"], "Questions", "Questions about %s" % pg["nav"].lower(),
                           "Straight answers. If yours is not here, ask us."))
    rel = []
    for name, lines, _ in S[pre + "-08"]["p"]["items"]:
        rel.append('<a class="relcard" href="%s" data-reveal data-glow><div class="relcard__img">%s</div><div class="relcard__body"><h3 class="d4">%s</h3>'
                   '<p>%s</p><span class="link-arrow">Learn more %s</span></div></a>'
                   % (SERVICE_LINK[name], img(C.SERVICE_IMAGE[name], "(max-width: 760px) 92vw, 400px"), E(name), E(lines[0]), icon("arrow-right")))
    out.append('<section class="sec sec--paper"><div class="wrap">%s<div class="related" data-stagger>%s</div></div></section>'
               % (sec_head("Related", "Often booked with this"), "".join(rel)))
    out.append(quick_quote(slug_, pg["nav"]))
    out.append(cta_band())
    return "".join(out)


def clients(pg):
    out = [page_hero([("/", "Home"), ("/clients", "Clients")], pg["h1"], pg["sections"][0]["p"]["sub"],
                     eb="Named with permission", image="office-mop", bg_key="duo-team-bg")]
    present = []
    for _, sector in L.CLIENTS:
        k = C.SECTOR_KEY[sector]
        if k not in present:
            present.append(k)
    flt = ('<div class="filters" data-reveal role="group" aria-label="Filter clients by sector">'
           '<button class="chip" type="button" data-filter="all" aria-pressed="true">All</button>%s</div>'
           '<p class="sr-only" id="filter-status" aria-live="polite"></p>'
           % "".join('<button class="chip" type="button" data-filter="%s" aria-pressed="false">%s</button>'
                     % (k, E(C.SECTOR_LABEL[k])) for k in present))
    cl = "".join('<li class="client" data-sector="%s"><span class="client__n">%02d</span><span class="client__name">%s</span>'
                 '<span class="client__rule" aria-hidden="true"></span><span class="client__sector">%s</span></li>'
                 % (C.SECTOR_KEY[s], i + 1, E(n), E(s)) for i, (n, s) in enumerate(L.CLIENTS))
    out.append('<section class="sec sec--white"><div class="wrap">%s%s<ul class="clients" data-stagger>%s</ul></div></section>'
               % (sec_head("Clients", "Clients served",
                           "Banks, schools, churches, apartment blocks, short-stay hosts and hospitality."), flt, cl))
    sect_link = {"Banking": "/services#commercial", "Education": "/services#commercial", "Churches": "/services#commercial",
                 "Residential complexes": "/services#residential", "Short-stay and Airbnb": "/services#residential",
                 "Hospitality": "/commercial-cleaning", "Construction": "/post-construction-cleaning"}
    out.append('<section class="sec sec--paper"><div class="wrap two-head"><div>%s</div><div>%s</div></div></section>'
               % (sec_head("Sectors", "Premises we know"), chips(pg["sections"][2]["p"]["items"], link=lambda c: sect_link.get(c), cls="chip--lg")))
    tiles = []
    for key, src, aspect, focal, caption, alt in C.GALLERY:
        rec = MAN["images"][key]
        thumb = rec["files"][:2]
        srcset = ", ".join("/assets/img/%s %dw" % (f["file"], f["w"]) for f in thumb)
        tiles.append('<a class="tile" data-reveal href="%s" data-caption="%s"><figure><img src="/assets/img/%s" srcset="%s" '
                     'sizes="(max-width: 760px) 46vw, 400px" width="%d" height="%d" alt="%s" loading="lazy" decoding="async">'
                     '<figcaption>%s</figcaption></figure><span class="tile__zoom" aria-hidden="true">%s</span></a>'
                     % (largest(key), E(caption), thumb[0]["file"], srcset, thumb[0]["w"], thumb[0]["h"], E(alt), E(caption), icon("plus")))
    out.append('<section class="sec sec--navy">%s<div class="wrap">%s<div class="gallery">%s</div></div></section>'
               % (bg_depth(), sec_head("Premises", "Spaces we look after",
                                       "The kinds of spaces we clean every week, from bank halls to compounds."), "".join(tiles)))
    out.append(cta_band())
    return "".join(out)


def contact(pg):
    S = {s["id"]: s for s in pg["sections"]}
    out = [page_hero([("/", "Home"), ("/contact", "Contact")], pg["h1"], S["K-01"]["p"]["sub"],
                     eb="Reply within one working day", image="svc-school", bg_key="page-bg")]
    card = ('<aside class="contact-card" data-reveal>%s<h2 class="d4">Prefer to talk?</h2><div class="btns">'
            '<a class="btn btn--sun btn--sm" href="tel:%s">%s Call</a><a class="btn btn--glass btn--sm" href="%s" target="_blank" rel="noopener">%s WhatsApp</a></div>'
            '<ul class="clist"><li><a href="tel:%s">%s<span><small>Call</small>%s</span></a></li>'
            '<li><a href="%s" target="_blank" rel="noopener">%s<span><small>WhatsApp</small>%s</span></a></li>'
            '<li><a href="mailto:%s">%s<span><small>Email</small>%s</span></a></li>'
            '<li><span>%s<span><small>Office</small>%s<br>%s</span></span></li>'
            '<li><span>%s<span><small>Postal</small>%s</span></span></li>'
            '<li><span>%s<span><small>Reply time</small>Within one working day</span></span></li></ul>'
            '<div class="qr"><img src="/assets/img/wa-qr.svg" width="120" height="120" alt="QR code that opens a WhatsApp chat with Smartline" loading="lazy">'
            '<p><b>On a computer?</b> Scan with your phone to chat on WhatsApp.</p></div></aside>'
            % (bg_depth(False), C.PHONE_E164, icon("phone"), E(C.wa_link()), icon("message-circle"), C.PHONE_E164, icon("phone"), E(C.PHONE),
               E(C.wa_link()), icon("message-circle"), E(C.PHONE), C.EMAIL, icon("mail"), C.EMAIL,
               icon("map-pin"), E(C.STREET), E(C.LOCALITY), icon("file-text"), E(C.POSTAL), icon("clock")))
    out.append('<section class="sec sec--paper"><div class="wrap form-wrap"><div data-reveal>%s</div>%s</div></section>' % (quote_form(), card))
    out.append('<section class="sec sec--white"><div class="wrap mapcard"><div class="mapcard__map" data-reveal="wipe">'
               '<img src="/assets/img/map.svg" width="800" height="600" alt="Schematic map: our office on ICIPE Road, off Thika Road in Kasarani" loading="lazy"></div>'
               '<div>%s<h2 class="d2" data-split>Find us</h2><p class="body-lg" data-reveal>%s, %s. Just off Thika Road, beside the Moi International Sports Centre.</p>'
               '<div class="btns" data-reveal><a class="btn btn--navy" href="%s" target="_blank" rel="noopener">Open in Google Maps %s</a></div></div></div></section>'
               % (eyebrow("Office"), E(C.STREET), E(C.LOCALITY), E(C.MAP_URL), icon("arrow-up-right")))
    out.append('<section class="sec sec--paper"><div class="wrap two-head"><div>%s</div><div>%s</div></div></section>'
               % (sec_head("Coverage", "Areas we serve",
                           "Based in Kasarani, working across Nairobi and Kiambu. Outside these areas? Ask &mdash; for contract work we often can."),
                  chips(S["K-04"]["p"]["items"], cls="chip--lg")))
    out.append('<section class="sec sec--white">%s</section>'
               % faq_block(S["K-05"]["p"]["items"], "Before you book", "Before you book", "Three things people ask first.", link=False))
    return "".join(out)


def thank_you(pg):
    S = {s["id"]: s for s in pg["sections"]}
    out = [page_hero(None, pg["h1"], S["T-01"]["p"]["sub"], eb="Request received", image="community", bg_key="duo-kitchen-bg")]
    out.append('<section class="sec sec--white"><div class="wrap">%s%s</div></section>'
               % (sec_head("Next", "What happens next"), timeline(S["T-02"]["p"]["items"])))
    out.append(cta_band("Need us sooner?", "Call or WhatsApp and we will pick it up straight away.", "Urgent"))
    return "".join(out)


def privacy(pg):
    secs = "".join('<section id="p-%s" data-reveal><h2>%s</h2><p>%s</p></section>' % (slug(t), E(t), E(b)) for t, b in C.PRIVACY)
    toc = "".join('<li><a href="#p-%s"><small>%02d</small>%s</a></li>' % (slug(t), i + 1, E(t)) for i, (t, _) in enumerate(C.PRIVACY))
    out = [page_hero([("/", "Home"), ("/privacy", "Privacy notice")], pg["h1"],
                     "How we collect, use and protect your personal data under Kenya’s Data Protection Act, 2019.",
                     bg_key="duo-team-bg", eb="Data Protection Act, 2019")]
    out.append('<section class="sec sec--white">%s<div class="wrap doc-wrap"><nav class="doc-toc" aria-label="On this page"><p class="label">On this page</p><ol>%s</ol>'
               '<a class="btn btn--ghost btn--sm" href="mailto:%s?subject=%s">Ask about your data %s</a></nav>'
               '<div class="doc">%s<p class="doc__meta">Last updated %s</p></div></div></section>'
               % (orbs("b"), toc, C.EMAIL, quote("Personal data request"), icon("arrow-right"), secs, C.LAST_UPDATED))
    return "".join(out)


def not_found(pg):
    out = ['<section class="phero phero--media nf"><div class="phero__bg" aria-hidden="true"></div>%s<div class="wrap phero__grid">'
           '<div class="phero__text"><p class="nf__code" aria-hidden="true">404</p><h1 class="d1" data-split>%s</h1>'
           '<p class="lede">%s</p><div class="btns"><a class="btn btn--sun" href="/">Go to the home page %s</a>'
           '<a class="btn btn--glass" href="/services">See our services</a></div></div>'
           '<figure class="phero__media" data-reveal="wipe"><div class="phero__frame">%s</div></figure></div></section>'
           % (bg_depth(), E(pg["h1"]), E(pg["sections"][0]["p"]["sub"]), icon("arrow-right"),
              img("notfound", "(max-width: 1040px) 92vw, 600px", eager=True))]
    cards = []
    for i, (g, anchor, items) in enumerate(L.GROUPS):
        lis = "".join("<li>%s</li>" % E(s) for s, _ in items[:3])
        cards.append('<article class="ccard" data-glow data-reveal><span class="ccard__n">%02d</span><h2 class="d4">%s</h2>'
                     '<ul class="ticks">%s</ul><a class="link-arrow" href="%s">Explore %s</a></article>'
                     % (i + 1, E(g), lis, anchor, icon("arrow-right")))
    out.append('<section class="sec sec--paper"><div class="wrap"><div class="checklist checklist--4" data-stagger>%s</div></div></section>' % "".join(cards))
    out.append(cta_band("Or just ask us", None, "Help"))
    return "".join(out)


def map_svg():
    """A schematic locator in the brand palette. Not to scale and labelled as such:
    it shows where we are relative to landmarks a Nairobi visitor already knows."""
    svg = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 600" role="img" aria-label="Schematic map: ICIPE Road off Thika Road, Kasarani">'
           '<rect width="800" height="600" fill="#EEEEF6"/>'
           '<g stroke="#DCDCEA" stroke-width="10" fill="none">'
           '<path d="M0 120 L800 160"/><path d="M0 470 L800 430"/><path d="M180 0 L140 600"/><path d="M640 0 L690 600"/>'
           '<path d="M0 300 L300 290"/><path d="M420 0 L460 260"/></g>'
           '<rect x="470" y="300" width="210" height="150" rx="6" fill="#DDEBDD"/>'
           '<text x="575" y="372" text-anchor="middle" font-family="Segoe UI, Arial, sans-serif" font-size="15" fill="#4C6250">Moi International</text>'
           '<text x="575" y="392" text-anchor="middle" font-family="Segoe UI, Arial, sans-serif" font-size="15" fill="#4C6250">Sports Centre</text>'
           '<path d="M-20 560 L820 40" stroke="#FFFFFF" stroke-width="34" fill="none"/>'
           '<path d="M-20 560 L820 40" stroke="#C3C3D6" stroke-width="2" stroke-dasharray="14 12" fill="none"/>'
           '<text transform="translate(205 395) rotate(-31.8)" font-family="Segoe UI, Arial, sans-serif" font-size="17" font-weight="700" '
           'letter-spacing="4" fill="#101238">THIKA ROAD</text>'
           '<path d="M392 318 C430 300 452 280 470 262 L560 214" stroke="#FFFFFF" stroke-width="18" fill="none"/>'
           '<text transform="translate(470 238) rotate(-26)" font-family="Segoe UI, Arial, sans-serif" font-size="14" font-weight="700" '
           'letter-spacing="2" fill="#101238">ICIPE ROAD</text>'
           '<path d="M470 262 L470 300" stroke="#FFFFFF" stroke-width="12" fill="none"/>'
           '<text x="300" y="540" font-family="Segoe UI, Arial, sans-serif" font-size="30" font-weight="800" fill="#2F2483">Kasarani</text>'
           '<circle cx="470" cy="262" r="34" fill="#F8951A" opacity=".18"/>'
           '<path d="M470 220 C455 220 444 231 444 246 C444 266 470 290 470 290 C470 290 496 266 496 246 C496 231 485 220 470 220 Z" '
           'fill="#101238" stroke="#F8951A" stroke-width="2"/><circle cx="470" cy="246" r="8" fill="#F8951A"/>'
           '<rect x="510" y="96" width="250" height="78" rx="3" fill="#FFFFFF" stroke="#E1E1EC"/>'
           '<rect x="510" y="96" width="3" height="78" fill="#F8951A"/>'
           '<text x="530" y="128" font-family="Segoe UI, Arial, sans-serif" font-size="20" font-weight="800" fill="#101238">Smartline</text>'
           '<text x="530" y="154" font-family="Segoe UI, Arial, sans-serif" font-size="13" fill="#5B5D78">ICIPE Road, Sports Drive, Suite 8</text>'
           '<text x="24" y="584" font-family="Segoe UI, Arial, sans-serif" font-size="12" fill="#8587A0">Schematic — not to scale</text>'
           '</svg>')
    with open(os.path.join(SITE, "assets", "img", "map.svg"), "w", encoding="utf-8") as f:
        f.write(svg)



# ================================================================== head + JSON-LD
BIZ = C.ORIGIN + "/#business"
SITE_ID = C.ORIGIN + "/#website"


def business_node():
    return {
        "@type": "LocalBusiness", "@id": BIZ, "name": C.BRAND, "alternateName": C.SHORT, "url": C.ORIGIN + "/",
        "logo": {"@type": "ImageObject", "url": C.ORIGIN + "/icon-512.png", "width": 512, "height": 512},
        "image": C.ORIGIN + "/assets/img/og/home.jpg", "telephone": C.PHONE_E164, "email": C.EMAIL,
        "slogan": "Assuring you the best", "foundingDate": C.FOUNDED, "priceRange": "KES",
        "description": "Commercial, residential and post-construction cleaning and landscaping in Nairobi and Kiambu.",
        "address": {"@type": "PostalAddress", "streetAddress": C.STREET, "addressLocality": "Kasarani",
                    "addressRegion": "Nairobi", "postalCode": "00100", "addressCountry": "KE"},
        "areaServed": [{"@type": "AdministrativeArea", "name": a} for a in C.AREAS],
        "knowsAbout": SERVICES,
        "hasOfferCatalog": {"@type": "OfferCatalog", "name": "Cleaning services", "itemListElement": [
            {"@type": "Offer", "itemOffered": {"@type": "Service", "name": s, "url": C.ORIGIN + SERVICE_LINK[s].replace("#", "#")}}
            for s in SERVICES]},
    }


def page_type(slug_):
    return {"/about": "AboutPage", "/contact": "ContactPage", "/services": "CollectionPage", "/clients": "CollectionPage"}.get(slug_, "WebPage")


def jsonld(pg, trail, faqs):
    url = C.ORIGIN + ("/" if pg["slug"] == "/" else pg["slug"])
    graph = []
    if pg["slug"] in ("/", "/contact", "/about"):
        graph.append(business_node())
    if pg["slug"] == "/":
        graph.append({"@type": "WebSite", "@id": SITE_ID, "url": C.ORIGIN + "/", "name": C.BRAND, "inLanguage": "en-GB",
                      "publisher": {"@id": BIZ}})
    page = {"@type": page_type(pg["slug"]), "@id": url + "#webpage", "url": url, "name": pg["title"],
            "description": pg["desc"], "inLanguage": "en-GB", "isPartOf": {"@id": SITE_ID}, "about": {"@id": BIZ},
            "primaryImageOfPage": C.ORIGIN + "/assets/img/" + MAN["og"].get(pg["slug"], MAN["og"]["/"])["file"]}
    if trail:
        page["breadcrumb"] = {"@id": url + "#breadcrumb"}
        graph.append({"@type": "BreadcrumbList", "@id": url + "#breadcrumb", "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "name": label,
             "item": C.ORIGIN + ("/" if href == "/" else href)} for i, (href, label) in enumerate(trail)]})
    graph.append(page)
    if pg["slug"] in QQ_SERVICES:
        graph.append({"@type": "Service", "@id": url + "#service", "name": pg["h1"], "serviceType": pg["nav"],
                      "description": pg["desc"], "provider": {"@id": BIZ}, "url": url,
                      "areaServed": [{"@type": "AdministrativeArea", "name": a} for a in C.AREAS]})
    if faqs:
        graph.append({"@type": "FAQPage", "@id": url + "#faq", "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": C.FAQ[q]}} for q in faqs]})
    return json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, separators=(",", ":"))


def head(pg, trail, faqs, index=True, key="page"):
    slug_ = pg["slug"]
    url = C.ORIGIN + ("/" if slug_ == "/" else slug_)
    og_name = "home" if slug_ == "/" else slug_.strip("/")
    og = MAN["og"].get(slug_, MAN["og"]["/"])
    kw = SEO.KEYWORDS.get(slug_)
    keywords = ", ".join([kw[0]] + kw[1]) if kw else ""
    preload = ""
    if slug_ == "/":
        ss = lambda k: ", ".join("/assets/img/%s %dw" % (f["file"], f["w"]) for f in MAN["images"][k]["files"])
        preload = ('<link rel="preload" as="image" imagesrcset="%s" imagesizes="100vw" media="(max-width: 760px)" fetchpriority="high">'
                   '<link rel="preload" as="image" imagesrcset="%s" imagesizes="100vw" media="(min-width: 761px)" fetchpriority="high">'
                   % (ss("hero-tall"), ss("hero-wide")))
    ga = ' data-ga="%s"' % E(C.GA_ID) if C.GA_ID else ""
    return ('<!doctype html><html lang="en-GB"%s><head><meta charset="utf-8">'
            '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">'
            '<title>%s</title><meta name="description" content="%s">%s'
            '<meta name="robots" content="%s">%s'
            '<meta name="theme-color" content="#101238"><meta name="author" content="%s">'
            '<meta name="geo.region" content="KE-30"><meta name="geo.placename" content="Nairobi">'
            '<link rel="icon" href="/favicon.svg" type="image/svg+xml"><link rel="icon" href="/favicon.ico" sizes="any">'
            '<link rel="apple-touch-icon" href="/apple-touch-icon.png"><link rel="manifest" href="/site.webmanifest">'
            '<link rel="preload" href="/assets/fonts/mona-sans.woff2" as="font" type="font/woff2" crossorigin>%s'
            '<link rel="stylesheet" href="/assets/css/main.css?v=%s">'
            '<script src="/assets/js/boot.js?v=%s"></script><script src="/assets/js/main.min.js?v=%s" defer></script>'
            '<meta property="og:type" content="website"><meta property="og:site_name" content="%s">'
            '<meta property="og:locale" content="en_GB"><meta property="og:title" content="%s">'
            '<meta property="og:description" content="%s"><meta property="og:url" content="%s">'
            '<meta property="og:image" content="%s/assets/img/%s"><meta property="og:image:width" content="1200">'
            '<meta property="og:image:height" content="630"><meta property="og:image:alt" content="%s">'
            '<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="%s">'
            '<meta name="twitter:description" content="%s"><meta name="twitter:image" content="%s/assets/img/%s">'
            '<script type="application/ld+json">%s</script></head><body data-page="%s" data-fx="/assets/js/fx.min.js?v=%s">'
            % (ga, E(pg["title"]), E(pg["desc"]), ('<meta name="keywords" content="%s">' % E(keywords)) if keywords else "",
               "index, follow, max-image-preview:large" if index else "noindex, follow",
               "" if slug_ == "/404" else '<link rel="canonical" href="%s">' % url, E(C.BRAND), preload,
               V_CSS, V_BOOT, V_JS, E(C.BRAND), E(pg["title"]), E(pg["desc"]), url, C.ORIGIN, og["file"],
               E(pg["h1"]), E(pg["title"]), E(pg["desc"]), C.ORIGIN, og["file"], jsonld(pg, trail, faqs), key, V_FX))


def page(pg, body, current, trail, faqs, index=True, key="page"):
    return (head(pg, trail, faqs, index, key) + '<a class="skip" href="#main">Skip to content</a>' + page_transition() + loader()
            + header(current) + drawer() + '<main id="main">' + body + '</main>' + footer()
            + actionbar() + cookie_bar() + '</body></html>')


# ================================================================== server files
HTACCESS = r"""# Smartline Point Cleaning Hub Ltd — Apache config for public_html
# Generated by build_site.py. HTTPS, one canonical host, clean URLs, strict headers.

Options -Indexes -MultiViews
DirectoryIndex index.html
ErrorDocument 404 /404.html
AddDefaultCharset UTF-8
AddType image/svg+xml .svg
AddType font/woff2 .woff2
AddType application/manifest+json .webmanifest

<IfModule mod_rewrite.c>
RewriteEngine On

# 1. HTTPS and the bare domain, in a single hop
RewriteCond %{HTTPS} !=on [OR]
RewriteCond %{HTTP_HOST} ^www\. [NC]
RewriteCond %{REQUEST_URI} !^/\.well-known/
RewriteRule ^ https://__DOMAIN__%{REQUEST_URI} [R=301,L,NE]

# 2. Never serve dotfiles, build leftovers or source maps (the speculation rules are the one .json we publish)
RewriteRule (^|/)\.(?!well-known/) - [F]
RewriteCond %{REQUEST_URI} !^/speculation-rules\.json$
RewriteRule \.(py|md|json|lock|map|log|bak|sql)$ - [F,NC]

# 3. /index.html -> /   and   /page.html -> /page
RewriteCond %{THE_REQUEST} \s/+index\.html[\s?] [NC]
RewriteRule ^ / [R=301,L]
RewriteCond %{THE_REQUEST} \s/+(.+?)\.html[\s?] [NC]
RewriteRule ^ /%1 [R=301,L,NE]

# 4. Strip a trailing slash from anything that is not a real directory
RewriteCond %{REQUEST_FILENAME} !-d
RewriteRule ^(.+)/$ /$1 [R=301,L]

# 5. Serve /page from page.html
RewriteCond %{REQUEST_FILENAME} !-f
RewriteCond %{REQUEST_FILENAME}.html -f
RewriteRule ^(.+)$ $1.html [L]
</IfModule>

<IfModule mod_headers.c>
Header always set Strict-Transport-Security "max-age=31536000"
Header always set X-Content-Type-Options "nosniff"
Header always set X-Frame-Options "DENY"
Header always set Referrer-Policy "strict-origin-when-cross-origin"
Header always set Permissions-Policy "camera=(), microphone=(), geolocation=(), payment=(), usb=(), magnetometer=(), gyroscope=()"
Header always set Cross-Origin-Opener-Policy "same-origin"
Header always set Content-Security-Policy "default-src 'self'; script-src 'self' https://www.googletagmanager.com; style-src 'self'; img-src 'self' data: https://www.googletagmanager.com https://*.google-analytics.com; font-src 'self'; connect-src 'self' https://*.google-analytics.com https://*.analytics.google.com https://www.googletagmanager.com; form-action 'self'; frame-ancestors 'none'; base-uri 'self'; object-src 'none'; upgrade-insecure-requests"
# Chromium prefetches a page when a visitor hovers its link (rules in a file, so the CSP stays strict)
Header set Speculation-Rules "\"/speculation-rules.json\""
Header unset X-Powered-By
Header always unset X-Powered-By

# HTML is always revalidated; CSS/JS carry ?v=hash and fonts never change, so a year;
# images keep their filenames when swapped (stock -> real photos), so 30 days, no immutable
<FilesMatch "\.(html)$">
Header set Cache-Control "no-cache"
</FilesMatch>
<FilesMatch "\.(css|js|woff2)$">
Header set Cache-Control "public, max-age=31536000, immutable"
</FilesMatch>
<FilesMatch "\.(webp|jpg|png|svg|ico)$">
Header set Cache-Control "public, max-age=2592000"
</FilesMatch>
<FilesMatch "\.(webmanifest|xml|txt)$">
Header set Cache-Control "public, max-age=86400"
</FilesMatch>
</IfModule>

<Files "speculation-rules.json">
ForceType application/speculationrules+json
</Files>

<IfModule mod_deflate.c>
AddOutputFilterByType DEFLATE text/html text/css text/plain text/xml application/javascript application/json application/xml image/svg+xml application/manifest+json
</IfModule>

<Files "enquiry.php">
<IfModule mod_headers.c>
Header always set X-Robots-Tag "noindex, nofollow"
</IfModule>
</Files>
""".replace("__DOMAIN__", C.DOMAIN)

FORM_HTACCESS = """# only the handler is reachable in this folder
Options -Indexes
<FilesMatch "^(?!enquiry\\.php$).*$">
Require all denied
</FilesMatch>
"""


def php_handler():
    def arr(xs):
        return "[" + ", ".join("'%s'" % x.replace("\\", "\\\\").replace("'", "\\'") for x in xs) + "]"
    returns = ["/contact"] + list(QQ_SERVICES)
    return r"""<?php
/**
 * Smartline Point Cleaning Hub Ltd — enquiry handler.
 * Generated by build_site.py. PHP 7.4+, no dependencies.
 *
 * POST only. Same-origin check, honeypot, minimum fill time, per-IP rate limit
 * (5 an hour), server-side validation against fixed lists, header-injection-safe
 * mail to the sales inbox, plain-text copy to the customer, 303 to /thank-you.
 */
declare(strict_types=1);

const HOST     = '__DOMAIN__';
const TO       = '__EMAIL__';
const FROM     = 'website@__DOMAIN__';
const PHONE    = '__PHONE__';
const SERVICES = __SERVICES__;
const PROPERTY = __PROPERTY__;
const FREQ     = __FREQ__;
const RETURNS  = __RETURNS__;
const LIMIT    = 5;      // submissions per IP per hour

header('X-Robots-Tag: noindex, nofollow');
header('Cache-Control: no-store');

function go(string $path): void { header('Location: ' . $path, true, 303); exit; }
function fail(string $return, string $code): void { go($return . '?error=' . $code . '#' . ($return === '/contact' ? 'quote' : 'main')); }

function field(string $key, int $max, bool $multiline = false): string {
    $v = isset($_POST[$key]) && is_string($_POST[$key]) ? $_POST[$key] : '';
    $v = preg_replace('/[\x00-\x09\x0B\x0C\x0E-\x1F\x7F]/u', '', $v) ?? '';
    if (!$multiline) { $v = str_replace(["\r", "\n"], ' ', $v); }
    $v = trim($v);
    return function_exists('mb_substr') ? mb_substr($v, 0, $max) : substr($v, 0, $max);
}

if (($_SERVER['REQUEST_METHOD'] ?? '') !== 'POST') { go('/contact'); }

$return = field('return', 60);
if (!in_array($return, RETURNS, true)) { $return = '/contact'; }

// same-origin: browsers send Origin on POST; reject anything from another site
$origin = $_SERVER['HTTP_ORIGIN'] ?? '';
if ($origin !== '') {
    $host = strtolower((string) parse_url($origin, PHP_URL_HOST));
    if ($host !== HOST && $host !== 'www.' . HOST) { fail($return, 'invalid'); }
}

// bots: a filled honeypot or an instant submit gets a quiet thank-you and no email
if (field('website', 200) !== '') { go('/thank-you'); }
$t = (int) field('t', 12);
if ($t > 0 && (time() - $t) < 3) { go('/thank-you'); }

// rate limit per IP, stored outside public_html
$ip = $_SERVER['REMOTE_ADDR'] ?? '0.0.0.0';
$rl = rtrim(sys_get_temp_dir(), '/\\') . DIRECTORY_SEPARATOR . 'smartline_rl_' . sha1($ip . HOST) . '.json';
$hits = [];
if (is_file($rl)) {
    $hits = json_decode((string) @file_get_contents($rl), true);
    if (!is_array($hits)) { $hits = []; }
}
$now = time();
$hits = array_values(array_filter($hits, function ($ts) use ($now) { return is_int($ts) && $ts > $now - 3600; }));
if (count($hits) >= LIMIT) { fail($return, 'rate'); }

// fields
$name     = field('name', 100);
$phone    = field('phone', 20);
$email    = field('email', 120);
$org      = field('organisation', 120);
$service  = field('service', 60);
$property = field('property', 40);
$location = field('location', 120);
$freq     = field('frequency', 30);
$date     = field('date', 10);
$message  = field('message', 1500, true);
$consent  = field('consent', 5);
$form     = field('form', 10) === 'qq' ? 'Quick quote' : 'Quote form';

$digits = preg_replace('/\D+/', '', $phone) ?? '';
$ok = $name !== '' && $location !== '' && $consent === 'yes'
    && preg_match('/^(?:254|0)?[17]\d{8}$/', $digits) === 1
    && in_array($service, SERVICES, true)
    && in_array($property, PROPERTY, true)
    && ($freq === '' || in_array($freq, FREQ, true))
    && ($email === '' || filter_var($email, FILTER_VALIDATE_EMAIL) !== false)
    && ($date === '' || preg_match('/^\d{4}-\d{2}-\d{2}$/', $date) === 1);
if (!$ok) { fail($return, 'invalid'); }

$hits[] = $now;
@file_put_contents($rl, json_encode($hits), LOCK_EX);

function subject(string $s): string {
    return function_exists('mb_encode_mimeheader') ? mb_encode_mimeheader($s, 'UTF-8', 'Q') : $s;
}
function send(string $to, string $subject, string $body, string $replyTo): bool {
    $headers = implode("\r\n", [
        'From: Smartline website <' . FROM . '>',
        'Reply-To: ' . $replyTo,
        'MIME-Version: 1.0',
        'Content-Type: text/plain; charset=UTF-8',
        'Content-Transfer-Encoding: 8bit',
        'X-Mailer: smartline-site',
    ]);
    if (@mail($to, subject($subject), $body, $headers, '-f' . FROM)) { return true; }
    return @mail($to, subject($subject), $body, $headers);
}

$lines = [
    'New quote request from the website (' . $form . ')',
    '',
    'Service:      ' . $service,
    'Premises:     ' . $property,
    'Location:     ' . $location,
    'How often:    ' . ($freq !== '' ? $freq : '-'),
    'Start date:   ' . ($date !== '' ? $date : '-'),
    '',
    'Name:         ' . $name,
    'Phone:        ' . $phone,
    'Email:        ' . ($email !== '' ? $email : '-'),
    'Organisation: ' . ($org !== '' ? $org : '-'),
    '',
    'Message:',
    $message !== '' ? $message : '-',
    '',
    'Consent to contact: yes (' . gmdate('d/m/Y H:i') . ' UTC)',
    'Reply within one working day — that is the promise on the website.',
];
$replyTo = $email !== '' ? $email : FROM;
if (!send(TO, 'Quote request: ' . $service . ' — ' . $name, implode("\n", $lines), $replyTo)) {
    fail($return, 'server');
}

if ($email !== '') {
    $copy = [
        'Hello ' . $name . ',',
        '',
        'Thank you for contacting Smartline Point Cleaning Hub Ltd. We have your request for ' . strtolower($service)
            . ' at ' . $location . ' and will call or WhatsApp you within one working day.',
        '',
        'If it is urgent, call or WhatsApp ' . PHONE . '.',
        '',
        'Smartline Point Cleaning Hub Ltd',
        'Assuring you the best',
        'https://' . HOST,
    ];
    send($email, 'We have your request — Smartline Point Cleaning Hub', implode("\n", $copy), TO);
}

go('/thank-you');
""".replace("__DOMAIN__", C.DOMAIN).replace("__EMAIL__", C.EMAIL).replace("__PHONE__", C.PHONE) \
       .replace("__SERVICES__", arr(SERVICES)).replace("__PROPERTY__", arr(C.PROPERTY_TYPES)) \
       .replace("__FREQ__", arr(C.FREQUENCIES)).replace("__RETURNS__", arr(returns))


def write(rel, text):
    path = os.path.join(SITE, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)


def build():
    map_svg()
    pages = {}
    for pg in L.PAGES:
        s = pg["slug"]
        if s == "/":
            body, trail, faqs = home(pg), None, pg["sections"][8]["p"]["items"]
        elif s == "/about":
            body, trail, faqs = about(pg), [("/", "Home"), ("/about", "About")], None
        elif s == "/services":
            body, trail, faqs = services(pg), [("/", "Home"), ("/services", "Services")], None
        elif s in QQ_SERVICES:
            pre = {"/commercial-cleaning": "CC", "/residential-apartment-cleaning": "RA", "/post-construction-cleaning": "PC"}[s]
            body = service_page(pg)
            trail = [("/", "Home"), ("/services", "Services"), (s, pg["nav"])]
            faqs = [x for x in pg["sections"] if x["id"] == pre + "-07"][0]["p"]["items"]
        elif s == "/clients":
            body, trail, faqs = clients(pg), [("/", "Home"), ("/clients", "Clients")], None
        elif s == "/contact":
            body, trail, faqs = contact(pg), [("/", "Home"), ("/contact", "Contact")], pg["sections"][4]["p"]["items"]
        pages[file_for(s)] = page(pg, body, s, trail, faqs, key=s.strip("/") or "home")
    for pg in L.UTILITY_PAGES:
        s = pg["slug"]
        if s == "/thank-you":
            pages["thank-you.html"] = page(pg, thank_you(pg), s, None, None, index=False, key="thank-you")
        elif s == "/privacy":
            pages["privacy.html"] = page(pg, privacy(pg), s, [("/", "Home"), ("/privacy", "Privacy notice")], None, key="privacy")
        elif s == "/404":
            pages["404.html"] = page(pg, not_found(pg), s, None, None, index=False, key="404")
    for fn, text in pages.items():
        write(fn, text)

    indexable = [p for p in L.PAGES] + [p for p in L.UTILITY_PAGES if p["slug"] == "/privacy"]
    urls = "".join('<url><loc>%s</loc><lastmod>%s</lastmod><changefreq>monthly</changefreq><priority>%s</priority></url>'
                   % (C.ORIGIN + ("/" if p["slug"] == "/" else p["slug"]), "2026-11-20",
                      "1.0" if p["slug"] == "/" else ("0.9" if p["slug"] in QQ_SERVICES or p["slug"] == "/services" else
                                                      ("0.3" if p["slug"] == "/privacy" else "0.7")))
                   for p in indexable)
    write("sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">%s</urlset>\n' % urls)
    write("robots.txt", "User-agent: *\nAllow: /\nDisallow: /form/\n\nSitemap: %s/sitemap.xml\n" % C.ORIGIN)
    write("site.webmanifest", json.dumps({
        "name": C.BRAND, "short_name": C.SHORT, "start_url": "/", "display": "browser",
        "background_color": "#FAF8F4", "theme_color": "#0E1430", "lang": "en-GB",
        "icons": [{"src": "/icon-192.png", "sizes": "192x192", "type": "image/png"},
                  {"src": "/icon-512.png", "sizes": "512x512", "type": "image/png"}]}, indent=1))
    write(".htaccess", HTACCESS)
    write("form/.htaccess", FORM_HTACCESS)
    write("form/enquiry.php", php_handler())
    write(".well-known/security.txt", "Contact: mailto:%s\nExpires: 2027-11-20T00:00:00.000Z\nPreferred-Languages: en\nCanonical: %s/.well-known/security.txt\n"
          % (C.EMAIL, C.ORIGIN))
    # prefetch (not prerender: the hero intro should play when the page is actually seen)
    write("speculation-rules.json", json.dumps({"prefetch": [{
        "where": {"and": [{"href_matches": "/*"}, {"not": {"href_matches": "/form/*"}},
                          {"not": {"selector_matches": "[target=_blank], [download]"}}]},
        "eagerness": "moderate"}]}, indent=1) + "\n")
    return pages


# ================================================================== verify
class Scan(HTMLParser):
    VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "source", "track", "wbr", "use", "path", "rect", "circle"}

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack, self.errors, self.ids, self.tags = [], [], [], []
        self.ldjson, self._in_ld, self._in_script, self.inline_scripts, self.text = [], False, False, 0, []
        self._h1, self.h1 = False, []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        self.tags.append((tag, a))
        if "id" in a:
            self.ids.append(a["id"])
        if "style" in a:
            self.errors.append("inline style attribute on <%s>" % tag)
        for k in a:
            if k.startswith("on"):
                self.errors.append("inline event handler %s on <%s>" % (k, tag))
        if tag == "script":
            if a.get("type") == "application/ld+json":
                self._in_ld = True
                self.ldjson.append("")
            elif not a.get("src"):
                self._in_script = True
        if tag == "style":
            self.errors.append("inline <style> block")
        if tag == "h1":
            self._h1 = True
            self.h1.append("")
        if tag not in self.VOID:
            self.stack.append(tag)

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag not in self.VOID and self.stack and self.stack[-1] == tag:
            self.stack.pop()

    def handle_endtag(self, tag):
        if tag == "script":
            if self._in_script:
                self.inline_scripts += 1
            self._in_ld = self._in_script = False
        if tag == "h1":
            self._h1 = False
        if tag in self.VOID:
            return
        if not self.stack or self.stack[-1] != tag:
            self.errors.append("unbalanced </%s> (open: %s)" % (tag, "/".join(self.stack[-4:])))
            if tag in self.stack:
                while self.stack and self.stack[-1] != tag:
                    self.stack.pop()
                self.stack.pop()
            return
        self.stack.pop()

    def handle_data(self, data):
        if self._in_ld:
            self.ldjson[-1] += data
        elif not self._in_script:
            self.text.append(data)
        if self._h1:
            self.h1[-1] += data


def verify(pages):
    errs = []
    sprite = open(os.path.join(SITE, "assets", "img", "icons.svg"), encoding="utf-8").read()
    sprite_ids = set(re.findall(r'id="([^"]+)"', sprite))
    page_ids = {}
    scans = {}
    for fn, text in pages.items():
        sc = Scan()
        sc.feed(text)
        sc.close()
        scans[fn] = sc
        page_ids[fn] = set(sc.ids)
        for e in sc.errors:
            errs.append("%s: %s" % (fn, e))
        if sc.stack:
            errs.append("%s: unclosed tags at end: %s" % (fn, "/".join(sc.stack)))
        dup = {i for i in sc.ids if sc.ids.count(i) > 1}
        if dup:
            errs.append("%s: duplicate ids %s" % (fn, sorted(dup)))
        if len(sc.h1) != 1:
            errs.append("%s: %d <h1> elements" % (fn, len(sc.h1)))
        if sc.inline_scripts:
            errs.append("%s: %d inline scripts (CSP forbids)" % (fn, sc.inline_scripts))
        for blob in sc.ldjson:
            try:
                json.loads(blob)
            except ValueError as ex:
                errs.append("%s: JSON-LD does not parse: %s" % (fn, ex))
        title = re.search(r"<title>(.*?)</title>", text).group(1)
        desc = re.search(r'<meta name="description" content="([^"]*)"', text).group(1)
        if len(html.unescape(title)) > 60:
            errs.append("%s: title %d chars" % (fn, len(html.unescape(title))))
        if fn not in ("404.html", "thank-you.html") and not 110 <= len(html.unescape(desc)) <= 160:
            errs.append("%s: description %d chars" % (fn, len(html.unescape(desc))))
        canon = re.findall(r'<link rel="canonical" href="([^"]+)">', text)
        if fn == "404.html":
            if canon:
                errs.append("404.html: a 404 must not declare a canonical")
        elif len(canon) != 1 or not canon[0].startswith(C.ORIGIN + "/"):
            errs.append("%s: canonical %s" % (fn, canon))
        for need in ('property="og:image"', 'property="og:title"', 'name="twitter:card"'):
            if need not in text:
                errs.append("%s: missing %s" % (fn, need))
        if not sc.ldjson:
            errs.append("%s: no JSON-LD" % fn)
        if re.search(r'<style[\s>]|\sstyle="', text):
            errs.append("%s: inline style (CSP style-src 'self' would block it)" % fn)
        raw_visible = html.unescape(" ".join(sc.text))
        visible = raw_visible.lower()
        for bad in ("to confirm", "from kes —", "todo", "lorem", "placeholder", "photo:", "hours: ", "undefined", "nan "):
            if bad in visible:
                errs.append("%s: forbidden text '%s'" % (fn, bad))
        if "fumigat" in text.lower():
            errs.append("%s: fumigation appears on the page" % fn)
        if re.search(r"\bNone\b", raw_visible) or re.search(r'="None"', text):
            errs.append("%s: a Python None leaked into the page" % fn)
        seen_src = {}
        for t, a in sc.tags:
            if t == "img" and a.get("src", "").startswith("/assets/img/") and a.get("src", "").endswith(".webp"):
                key = re.sub(r"-\d+\.webp$", "", a["src"].rsplit("/", 1)[1])
                src = (C.IMAGES.get(key) or next(((g[1],) for g in C.GALLERY if g[0] == key), (key,)))[0]
                if src in seen_src and seen_src[src] != key or list(seen_src.values()).count(key) and key not in ("hero-wide",):
                    errs.append("%s: photo %s appears twice (%s)" % (fn, src, key))
                seen_src[src] = key
        labels = {a.get("for") for t, a in sc.tags if t == "label"}
        for t, a in sc.tags:
            if t == "img":
                for att in ("alt", "width", "height"):
                    if att not in a:
                        errs.append("%s: <img %s> missing %s" % (fn, a.get("src"), att))
                for src in [a.get("src")] + [x.strip().split(" ")[0] for x in (a.get("srcset") or "").split(",") if x.strip()]:
                    if src and src.startswith("/") and not os.path.exists(os.path.join(SITE, src.split("?")[0].lstrip("/"))):
                        errs.append("%s: missing image %s" % (fn, src))
            if t in ("input", "select", "textarea") and a.get("type") != "hidden":
                if a.get("id") not in labels:
                    errs.append("%s: <%s name=%s> has no label" % (fn, t, a.get("name")))
            if t == "use":
                ref = a.get("href", "")
                if ref.split("#")[-1] not in sprite_ids:
                    errs.append("%s: icon %s not in sprite" % (fn, ref))
            if t in ("link", "script") and (a.get("href") or a.get("src", "")).startswith("/"):
                p = (a.get("href") or a.get("src")).split("?")[0]
                if not os.path.exists(os.path.join(SITE, p.lstrip("/"))):
                    errs.append("%s: missing asset %s" % (fn, p))
            if t == "a":
                href = a.get("href", "")
                if a.get("target") == "_blank" and "noopener" not in (a.get("rel") or ""):
                    errs.append("%s: target=_blank without noopener: %s" % (fn, href))
                if href.startswith("/") and not href.startswith("//"):
                    path, _, frag = href.partition("#")
                    path = path.split("?")[0]
                    target = file_for(path) if path else fn
                    if path.startswith("/assets/"):
                        if not os.path.exists(os.path.join(SITE, path.lstrip("/"))):
                            errs.append("%s: link to missing file %s" % (fn, path))
                        continue
                    if target not in pages:
                        errs.append("%s: broken link %s" % (fn, href))
                    elif frag and frag not in page_ids.get(target, set()) and target in page_ids:
                        errs.append("%s: missing anchor %s" % (fn, href))
                elif href.startswith("#") and len(href) > 1 and href[1:] not in set(sc.ids):
                    errs.append("%s: missing in-page anchor %s" % (fn, href))
    # anchors to pages scanned later
    for fn, sc in scans.items():
        for t, a in sc.tags:
            href = a.get("href", "") if t == "a" else ""
            if href.startswith("/") and "#" in href and not href.startswith("/assets/"):
                path, _, frag = href.partition("#")
                target = file_for(path.split("?")[0]) if path else fn
                if target in page_ids and frag not in page_ids[target]:
                    errs.append("%s: missing anchor %s" % (fn, href))
    # budgets
    js = os.path.getsize(os.path.join(SITE, "assets/js/main.min.js")) + os.path.getsize(os.path.join(SITE, "assets/js/boot.js"))
    fonts = sum(os.path.getsize(os.path.join(SITE, "assets/fonts", f)) for f in os.listdir(os.path.join(SITE, "assets/fonts")))
    if js > 30 * 1024:
        errs.append("JavaScript %d bytes > 30 KB budget" % js)
    for mod in ("wipe", "fx"):
        size = os.path.getsize(os.path.join(SITE, "assets/js/%s.min.js" % mod))
        if size > 8 * 1024:
            errs.append("%s.min.js %d bytes > 8 KB budget (it loads on demand, but stays small)" % (mod, size))
    if fonts > 120 * 1024:
        errs.append("fonts %d bytes > 120 KB budget" % fonts)
    for f in MAN["images"]["hero-tall"]["files"]:
        if f["bytes"] > 200 * 1024:
            errs.append("phone hero %s is %d KB > 200 KB" % (f["file"], f["bytes"] // 1024))
    for f in MAN["images"]["hero-wide"]["files"]:
        if f["w"] <= 1920 and f["bytes"] > 300 * 1024:
            errs.append("desktop hero %s is %d KB > 300 KB" % (f["file"], f["bytes"] // 1024))
    errs = sorted(set(errs))
    if errs:
        raise SystemExit("site verify() FAILED (%d):\n  - " % len(errs) + "\n  - ".join(errs[:80]))
    return js, fonts


def main():
    pages = build()
    js, fonts = verify(pages)
    total = sum(len(t.encode("utf-8")) for t in pages.values())
    print("site verify OK: %d pages, %d KB of HTML, JS %.1f KB, fonts %.1f KB, %d icons in the sprite"
          % (len(pages), total // 1024, js / 1024, fonts / 1024, len(MAN["icons"]["icons"])))


if __name__ == "__main__":
    main()
