# -*- coding: utf-8 -*-
"""Smartline Point Cleaning Hub Ltd — logo concept geometry.

Six improved marks, each written as SVG in a 100x100 box so they scale from a
van door down to a 16px favicon. Every concept keeps the three things the
current logo already owns: the S, the indigo-to-orange sweep and the droplet.

Modes:  color  -> full brand palette
        mono   -> single black (stamps, faxed tender documents, embroidery)
        rev    -> knocked out white for navy backgrounds
"""
import os

INDIGO = "#2E2482"
NAVY = "#121439"
ORANGE = "#F98719"
AMBER = "#FBB040"
DEEP = "#F26F21"
WHITE = "#FFFFFF"
BLACK = "#0B0B12"

# the S spine — one stroke, consistent weight, used by most concepts
S_PATH = ("M74 33 C74 21 63 14 50 14 C36 14 26 22 26 33 C26 44 36 48.5 50 50 "
          "C64 51.5 74 57 74 68 C74 79 63 86 50 86 C37 86 26 79 26 68")
DROPLET = "M50 7 C50 7 81 40 81 60 A31 31 0 0 1 19 60 C19 40 50 7 50 7 Z"
SHIELD = "M50 7 L87 21 V51 C87 72 71 87 50 93 C29 87 13 72 13 51 V21 Z"
SPARKLE = "M79 12 L83.5 25.5 L97 30 L83.5 34.5 L79 48 L74.5 34.5 L61 30 L74.5 25.5 Z"
TILE = None  # drawn as a rounded rect


def palette(mode):
    """returns (primary, accent, accent2, surface, onsurface)"""
    if mode == "mono":
        return BLACK, BLACK, BLACK, BLACK, WHITE
    if mode == "rev":
        return WHITE, ORANGE, AMBER, WHITE, NAVY
    return INDIGO, ORANGE, AMBER, INDIGO, WHITE


def _grad(gid, c1, c2, x1=0, y1=0, x2=1, y2=1):
    return ('<linearGradient id="%s" x1="%s" y1="%s" x2="%s" y2="%s">'
            '<stop offset="0" stop-color="%s"/><stop offset="1" stop-color="%s"/>'
            '</linearGradient>' % (gid, x1, y1, x2, y2, c1, c2))


def wrap(inner, defs=""):
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" '
            'width="100" height="100"><defs>%s</defs>%s</svg>' % (defs, inner))


# ---------------------------------------------------------------- concepts
# Flat brand colours only: gradients do not survive everyprint pipeline (vinyl
# cutting, embroidery, one-colour stamps) and the renderer that builds the
# review sheet rasterises them unreliably. Two-tone reads stronger anyway.

DROP_SMALL = "M83 6 C83 6 92 18 92 23.5 A9 9 0 0 1 74 23.5 C74 18 83 6 83 6 Z"
SPARK_BIG = "M79 11 L83.6 25 L97.6 29.6 L83.6 34.2 L79 48.2 L74.4 34.2 L60.4 29.6 L74.4 25 Z"
SPARK_SM = "M14 58 L16.8 65.2 L24 68 L16.8 70.8 L14 78 L11.2 70.8 L4 68 L11.2 65.2 Z"


def c1_refined(mode):
    """01 Refined S — the current mark, drawn properly. Even stroke, true arcs,
    the tail resolving into the orange sweep, droplet as a counterweight."""
    p, a, a2, _, _ = palette(mode)
    inner = ('<path d="%s" fill="none" stroke="%s" stroke-width="13" '
             'stroke-linecap="round"/>' % (S_PATH, p))
    inner += ('<path d="M26 68 C26 79 37 86 50 86 C63 86 74 79 74 68" fill="none" '
              'stroke="%s" stroke-width="13" stroke-linecap="round"/>' % a)
    inner += '<path d="%s" fill="%s"/>' % (DROP_SMALL, a2)
    return wrap(inner)


def c2_droplet(mode):
    """02 Droplet S — the S held inside a water droplet. Reads as cleaning
    instantly, and the solid silhouette survives at 16px."""
    p, a, a2, _, _ = palette(mode)
    cut = WHITE if mode != "rev" else NAVY
    if mode == "mono":
        cut = WHITE
    inner = '<path d="%s" fill="%s"/>' % (DROPLET, p)
    inner += ('<path d="M46 82 A28 28 0 0 0 73 63" fill="none" stroke="%s" '
              'stroke-width="7" stroke-linecap="round"/>' % a)
    inner += ('<path d="M65 44 C65 36.5 58 32 50 32 C42 32 35.5 36 35.5 43 '
              'C35.5 49.5 42 52.5 50 53.5 C58 54.5 64.5 58 64.5 65 '
              'C64.5 72 58 76.5 50 76.5 C42.5 76.5 35.5 72 35.5 64.5" fill="none" '
              'stroke="%s" stroke-width="8.5" stroke-linecap="round"/>' % cut)
    return wrap(inner)


def c3_shield(mode):
    """03 Shield S — for tender files and facility managers: vetted, insured,
    contracted. The orange band carries the sweep across the base."""
    p, a, a2, _, _ = palette(mode)
    body = NAVY if mode == "color" else p
    cut = WHITE if mode != "rev" else NAVY
    if mode == "mono":
        cut = WHITE
    inner = '<path d="%s" fill="%s"/>' % (SHIELD, body)
    inner += ('<path d="M20 67 C30 75.5 41 79.5 50 79.5 C59 79.5 70 75.5 80 67" fill="none" '
              'stroke="%s" stroke-width="7" stroke-linecap="round"/>' % a)
    inner += ('<path d="M64.5 41 C64.5 34 58 29.5 50 29.5 C42 29.5 36 33.5 36 40 '
              'C36 46 42 49 50 50 C58 51 64 54.5 64 61 C64 67.5 58 72 50 72 '
              'C42.5 72 36 67.5 36 60.5" fill="none" stroke="%s" stroke-width="8" '
              'stroke-linecap="round"/>' % cut)
    return wrap(inner)


def c4_sparkle(mode):
    """04 Sparkle S — the shine cue the sector is judged on, kept geometric
    rather than cartoon. The sparkle takes over from the old droplet dot."""
    p, a, a2, _, _ = palette(mode)
    inner = ('<path d="%s" fill="none" stroke="%s" stroke-width="12.5" '
             'stroke-linecap="round"/>' % (S_PATH, p))
    inner += '<path d="%s" fill="%s"/>' % (SPARK_BIG, a)
    inner += '<path d="%s" fill="%s"/>' % (SPARK_SM, a2)
    return wrap(inner)


def c5_tile(mode):
    """05 Tile S — app icon, embroidery patch, van decal, WhatsApp avatar.
    One flat shape, one colour, no fine detail to lose on overalls."""
    p, a, a2, _, _ = palette(mode)
    bg = NAVY if mode == "color" else p
    cut = WHITE if mode != "rev" else NAVY
    if mode == "mono":
        cut = WHITE
    inner = '<rect x="4" y="4" width="92" height="92" rx="22" fill="%s"/>' % bg
    if mode == "color":
        inner += ('<path d="M4 76 C20 85 36 89 50 89 C64 89 80 85 96 76 L96 74 '
                  'C96 86.1 86.1 96 74 96 L26 96 C13.9 96 4 86.1 4 74 Z" fill="%s"/>' % a)
    inner += ('<path d="M67 41 C67 33.5 59.5 29 50 29 C40.5 29 33 33 33 40 '
              'C33 46.5 40.5 49.5 50 50.5 C59.5 51.5 67 55 67 62 '
              'C67 69 59.5 73.5 50 73.5 C41 73.5 33 69 33 61.5" fill="none" '
              'stroke="%s" stroke-width="9" stroke-linecap="round"/>' % cut)
    return wrap(inner)


def c6_orbit(mode):
    """06 Orbit S — the S inside an open ring: scheduled, repeating service
    (daily, quarterly, annual) rather than a one-off clean."""
    p, a, a2, _, _ = palette(mode)
    ring = a if mode != "mono" else p
    inner = ('<path d="M20 64 A34 34 0 1 1 37 84" fill="none" stroke="%s" '
             'stroke-width="9" stroke-linecap="round"/>' % ring)
    inner += ('<path d="M66 42 C66 35 59 30.5 50 30.5 C41.5 30.5 35 34.5 35 41 '
              'C35 47 41.5 50 50 51 C58.5 52 65 55.5 65 62 C65 68.5 58.5 73 50 73 '
              'C42 73 35 68.5 35 61.5" fill="none" stroke="%s" stroke-width="9" '
              'stroke-linecap="round"/>' % p)
    return wrap(inner)


CONCEPTS = [
    ("01", "Refined S", c1_refined,
     "Your mark, drawn properly — even weight, true arcs, the orange sweep resolved. "
     "Nothing to re-learn; everything already printed still reads as you."),
    ("02", "Droplet S", c2_droplet,
     "The S held inside a water droplet. Says cleaning before a word is read, and the solid "
     "silhouette still works at 16 pixels on a phone tab."),
    ("03", "Shield S", c3_shield,
     "Built for tender files and facility managers — vetted, insured, contracted. "
     "The orange band carries your sweep along the base."),
    ("04", "Sparkle S", c4_sparkle,
     "The shine cue the sector is judged on, kept geometric instead of cartoon. "
     "The sparkle takes over the job the old droplet dot was doing."),
    ("05", "Tile S", c5_tile,
     "An app icon, an embroidery patch, a van decal, a WhatsApp avatar. One flat shape, "
     "one colour, no fine detail to lose on overalls."),
    ("06", "Orbit S", c6_orbit,
     "The S inside an open ring — scheduled, repeating service: daily, quarterly, annual. "
     "Speaks to contracts rather than one-off jobs."),
]

MODES = ["color", "mono", "rev"]


def write_all(outdir="logo/svg"):
    os.makedirs(outdir, exist_ok=True)
    paths = {}
    for num, name, fn, _ in CONCEPTS:
        for mode in MODES:
            slug = "%s-%s-%s.svg" % (num, name.lower().replace(" ", "-"), mode)
            fp = os.path.join(outdir, slug)
            with open(fp, "w", encoding="utf-8") as f:
                f.write(fn(mode))
            paths[(num, mode)] = fp
    return paths


if __name__ == "__main__":
    p = write_all()
    print("wrote %d svg files" % len(p))
