# -*- coding: utf-8 -*-
"""The client's ORIGINAL logo, lifted as exact vector from their company profile.

Allen, 20/11/2026: "Use their original logo but high quality."

Nothing here is traced or redrawn. Page 1 of `smart.pdf` carries the logo as
PDF vector paths; this module parses that page's content stream and re-emits
the same geometry as clean SVG:

  * the indigo S                     CMYK 100/100/0/0  -> #2F2483 (as the profile renders it)
  * the navy droplet                 RGB               -> #101238
  * the swoosh, a 3-segment axial    #FF6600 / #FFC200 / #F8951A / #FC621C, stops and axis
    shading clipped to its path      taken from the shading dictionary itself
  * the tagline "Assuring you the best", already outlined in the profile (navy)

The wordmark is set from the profile's embedded Gotham Black subset (CFF, read
with fontTools) with the widths from the PDF's /W array, so the letterforms
are the client's own typeface, not a substitute.

verify() runs on import and fails loudly if the profile ever stops yielding
the expected parts.
"""
import io
import os
import re

import pymupdf
from fontTools.cffLib import CFFFontSet
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen

ROOT = os.path.dirname(os.path.abspath(__file__))
PDF = os.path.join(ROOT, "smart.pdf")

INDIGO = "#2F2483"
NAVY = "#101238"
WHITE = "#FFFFFF"
BRAND = "Smartline Point Cleaning Hub Ltd"

# the logo occupies this box of page 1 user space (PDF units, y up)
REGION = (10.0, 350.0, 80.0, 412.0)
MARK_MIN_Y = 362.0          # below this line is the tagline


# ------------------------------------------------------------------ content-stream parsing
_TOK = re.compile(rb"<<|>>|\[|\]|/[^\s/\[\]<>()%]+|<[0-9A-Fa-f\s]*>|\((?:\\.|[^\\)])*\)"
                  rb"|[-+]?(?:\d+\.?\d*|\.\d+)|[A-Za-z'\"]+\*?")


def _mul(a, b):
    """3x2 affine matrices as (a, b, c, d, e, f); returns a then b."""
    return (a[0] * b[0] + a[1] * b[2], a[0] * b[1] + a[1] * b[3],
            a[2] * b[0] + a[3] * b[2], a[2] * b[1] + a[3] * b[3],
            a[4] * b[0] + a[5] * b[2] + b[4], a[4] * b[1] + a[5] * b[3] + b[5])


def _parse(page):
    """Yield every filled path and every clipped shading on the page, in user space."""
    data = page.read_contents()
    ctm = (1, 0, 0, 1, 0, 0)
    stack = []
    ops = []
    path = []          # list of subpaths; each subpath is a list of ("M"/"L"/"C"/"Z", pts)
    clip_pending = False
    clip = None
    fill = (None, ())
    cs = None
    in_text = False
    out = []

    def P(x, y):
        a, b, c, d, e, f = ctm
        return (a * x + c * y + e, b * x + d * y + f)

    for m in _TOK.finditer(data):
        t = m.group(0)
        if re.fullmatch(rb"[-+]?(?:\d+\.?\d*|\.\d+)", t):
            ops.append(float(t))
            continue
        if t[:1] in (b"/", b"<", b"(", b"[", b"]") or t in (b"<<", b">>"):
            ops.append(t)
            continue
        op = t.decode("latin-1")
        nums = [o for o in ops if isinstance(o, float)]
        if op == "BT":
            in_text = True
        elif op == "ET":
            in_text = False
        elif in_text:
            pass
        elif op == "q":
            stack.append(ctm)
        elif op == "Q":
            ctm = stack.pop()
        elif op == "cm":
            ctm = _mul(tuple(nums[-6:]), ctm)
        elif op in ("cs", "CS"):
            if op == "cs":
                cs = ops[-1].decode("latin-1")
        elif op in ("scn", "sc", "rg", "k", "g"):
            space = {"rg": "/CS9", "k": "/CS19", "g": "gray"}.get(op, cs)
            fill = (space, tuple(nums))
        elif op == "m":
            path.append([("M", [P(*nums[-2:])])])
        elif op == "l":
            path[-1].append(("L", [P(*nums[-2:])]))
        elif op == "c":
            v = nums[-6:]
            path[-1].append(("C", [P(v[0], v[1]), P(v[2], v[3]), P(v[4], v[5])]))
        elif op == "h":
            if path:
                path[-1].append(("Z", []))
        elif op == "re":
            x, y, w, h = nums[-4:]
            path.append([("M", [P(x, y)]), ("L", [P(x + w, y)]), ("L", [P(x + w, y + h)]),
                         ("L", [P(x, y + h)]), ("Z", [])])
        elif op in ("W", "W*"):
            clip_pending = True
        elif op in ("f", "f*", "F"):
            out.append({"kind": "fill", "path": path, "rule": "evenodd" if op == "f*" else "nonzero",
                        "fill": fill})
            path = []
        elif op == "n":
            if clip_pending:
                clip = path
            clip_pending = False
            path = []
        elif op == "sh":
            out.append({"kind": "shade", "path": clip, "rule": "evenodd", "shading": ops[-1].decode("latin-1")})
        ops = []
    return out


def _bounds(path, steps=24):
    xs, ys = [], []
    for sub in path:
        cur = None
        for kind, pts in sub:
            if kind in ("M", "L"):
                cur = pts[0]
                xs.append(cur[0]); ys.append(cur[1])
            elif kind == "C":
                p0, (p1, p2, p3) = cur, pts
                for i in range(steps + 1):
                    t = i / steps
                    mt = 1 - t
                    xs.append(mt ** 3 * p0[0] + 3 * mt * mt * t * p1[0] + 3 * mt * t * t * p2[0] + t ** 3 * p3[0])
                    ys.append(mt ** 3 * p0[1] + 3 * mt * mt * t * p1[1] + 3 * mt * t * t * p2[1] + t ** 3 * p3[1])
                cur = p3
    return min(xs), min(ys), max(xs), max(ys)


def _hex(rgb):
    return "#%02X%02X%02X" % tuple(int(round(max(0, min(1, v)) * 255)) for v in rgb)


def _shading(doc, page, name):
    """Axial shading -> (axis x0,y0,x1,y1, [(offset, hex)]) from the PDF's own function tree."""
    res = doc.xref_get_key(page.xref, "Resources")[1]
    sx = int(re.search(name.replace("/", r"/") + r"\s+(\d+) 0 R", res).group(1))
    so = doc.xref_object(sx)
    assert "/ShadingType 2" in so, "swoosh is no longer an axial shading"
    axis = [float(v) for v in re.search(r"/Coords\s*\[([^\]]+)\]", so).group(1).split()]
    fx = int(re.search(r"/Function (\d+) 0 R", so).group(1))
    fo = doc.xref_object(fx)
    bounds = [float(v) for v in re.search(r"/Bounds\s*\[([^\]]*)\]", fo).group(1).split()]
    encode = [float(v) for v in re.search(r"/Encode\s*\[([^\]]+)\]", fo).group(1).split()]
    subs = [int(v) for v in re.findall(r"(\d+) 0 R", re.search(r"/Functions\s*\[([^\]]+)\]", fo).group(1))]
    edges = [0.0] + bounds + [1.0]
    stops = []
    for i, sub in enumerate(subs):
        so2 = doc.xref_object(sub)
        c0 = [float(v) for v in re.search(r"/C0\s*\[([^\]]+)\]", so2).group(1).split()]
        c1 = [float(v) for v in re.search(r"/C1\s*\[([^\]]+)\]", so2).group(1).split()]
        e0, e1 = encode[2 * i], encode[2 * i + 1]
        at = lambda s: c0 if s == 0 else c1        # N = 1 and the encode is 0/1 at the ends
        stops.append((edges[i], _hex(at(e0))))
        stops.append((edges[i + 1], _hex(at(e1))))
    dedup = []
    for o, c in stops:
        if not dedup or dedup[-1] != (o, c):
            dedup.append((o, c))
    return axis, dedup


def _colour(fill):
    space, vals = fill
    if space == "/CS19" and vals == (1.0, 1.0, 0.0, 0.0):
        return INDIGO
    if len(vals) == 3:
        return _hex(vals)
    raise ValueError("unexpected logo colour %r" % (fill,))


# ------------------------------------------------------------------ extraction
def _extract():
    doc = pymupdf.open(PDF)
    page = doc[0]
    x0, y0, x1, y1 = REGION
    parts = {"S": None, "droplet": None, "swoosh": None, "tagline": []}
    for item in _parse(page):
        if not item["path"]:
            continue
        bx0, by0, bx1, by1 = _bounds(item["path"])
        if not (bx0 >= x0 and by0 >= y0 and bx1 <= x1 and by1 <= y1):
            continue
        if item["kind"] == "shade":
            axis, stops = _shading(doc, page, item["shading"])
            parts["swoosh"] = dict(item, axis=axis, stops=stops, bbox=(bx0, by0, bx1, by1))
            continue
        col = _colour(item["fill"])
        rec = dict(item, colour=col, bbox=(bx0, by0, bx1, by1))
        if by0 < MARK_MIN_Y:
            parts["tagline"].append(rec)
        elif col == INDIGO:
            parts["S"] = rec
        else:
            parts["droplet"] = rec
    return parts


def _font():
    """Gotham Black subset from the profile: unicode -> (outline charstring, advance /1000)."""
    doc = pymupdf.open(PDF)
    fobj = doc.xref_object(12)
    assert "Gotham-Black" in fobj, "profile font changed"
    tu = doc.xref_stream(int(re.search(r"/ToUnicode (\d+) 0 R", fobj).group(1))).decode("latin-1")
    cid_of = {}
    for a, b in re.findall(r"<([0-9a-fA-F]{4})>\s*<([0-9a-fA-F]{4})>", tu.split("beginbfchar", 1)[1]):
        cid_of[chr(int(b, 16))] = int(a, 16)
    desc = doc.xref_object(int(re.search(r"/DescendantFonts\s*\[\s*(\d+)", fobj).group(1)))
    wtxt = doc.xref_object(int(re.search(r"/W (\d+) 0 R", desc).group(1)))
    widths = {}
    for start, arr in re.findall(r"(\d+)\s*\[([^\]]*)\]", wtxt):
        for i, w in enumerate(arr.split()):
            widths[int(start) + i] = float(w) / 1000.0
    fd = doc.xref_object(int(re.search(r"/FontDescriptor (\d+) 0 R", desc).group(1)))
    buf = doc.xref_stream(int(re.search(r"/FontFile3 (\d+) 0 R", fd).group(1)))
    cff = CFFFontSet()
    cff.decompile(io.BytesIO(buf), None)
    top = cff[cff.fontNames[0]]
    glyphs = {}
    for ch, cid in cid_of.items():
        name = "cid%05d" % cid
        if name in top.CharStrings:
            glyphs[ch] = (top.CharStrings[name], widths.get(cid, 0.6))
    return glyphs


PARTS = _extract()
GLYPHS = _font()


# ------------------------------------------------------------------ SVG writers
def _fmt(v):
    s = "%.3f" % v
    s = s.rstrip("0").rstrip(".")
    return "0" if s in ("-0", "") else s


def _d(path, T):
    out = []
    for sub in path:
        for kind, pts in sub:
            if kind == "Z":
                out.append("Z")
            else:
                out.append(kind + " ".join("%s %s" % tuple(map(_fmt, T(*p))) for p in pts))
    return "".join(out)


def _text_paths(text, size, x, baseline, colour, tracking=0.0, opacity=None):
    """Set `text` in the profile's Gotham Black; returns (svg, advance width)."""
    pieces, pen_x = [], x
    for ch in text:
        if ch == " ":
            pen_x += GLYPHS[" "][1] * size + tracking if " " in GLYPHS else 0.277 * size + tracking
            continue
        cs, adv = GLYPHS[ch]
        pen = SVGPathPen(None, ntos=_fmt)
        cs.draw(TransformPen(pen, (size / 1000.0, 0, 0, -size / 1000.0, pen_x, baseline)))
        d = pen.getCommands()
        if d:
            pieces.append(d)
        pen_x += adv * size + tracking
    width = pen_x - x - tracking
    op = (' fill-opacity="%s"' % opacity) if opacity is not None else ""
    return '<path fill="%s"%s d="%s"/>' % (colour, op, "".join(pieces)), width


def text_width(text, size, tracking=0.0):
    w = 0.0
    for ch in text:
        w += (GLYPHS[ch][1] if ch in GLYPHS else 0.277) * size + tracking
    return w - tracking


def _mark_group(T, mode, gid):
    """The S, swoosh and droplet under transform T; mode colour|rev|mono-white."""
    s, sw, dr = PARTS["S"], PARTS["swoosh"], PARTS["droplet"]
    s_col = INDIGO if mode == "color" else WHITE
    d_col = NAVY if mode == "color" else WHITE
    ax = sw["axis"]
    (gx1, gy1), (gx2, gy2) = T(ax[0], ax[1]), T(ax[2], ax[3])
    stops = "".join('<stop offset="%s" stop-color="%s"/>' % (_fmt(o), c) for o, c in sw["stops"])
    grad = ('<linearGradient id="%s" gradientUnits="userSpaceOnUse" x1="%s" y1="%s" x2="%s" y2="%s">%s</linearGradient>'
            % (gid, _fmt(gx1), _fmt(gy1), _fmt(gx2), _fmt(gy2), stops))
    body = ('<path fill="%s" fill-rule="%s" d="%s"/>' % (s_col, s["rule"], _d(s["path"], T))
            + '<path fill="url(#%s)" fill-rule="%s" d="%s"/>' % (gid, sw["rule"], _d(sw["path"], T))
            + '<path fill="%s" fill-rule="%s" d="%s"/>' % (d_col, dr["rule"], _d(dr["path"], T)))
    return grad, body


def _union(*boxes):
    return (min(b[0] for b in boxes), min(b[1] for b in boxes), max(b[2] for b in boxes), max(b[3] for b in boxes))


MARK_BOX = _union(PARTS["S"]["bbox"], PARTS["swoosh"]["bbox"], PARTS["droplet"]["bbox"])
TAG_BOX = _union(*[t["bbox"] for t in PARTS["tagline"]])


def _svg(w, h, inner, label, defs=""):
    lab = ' role="img" aria-label="%s"' % label if label else ' aria-hidden="true"'
    return ('<svg xmlns="http://www.w3.org/2000/svg"%s width="%s" height="%s" viewBox="0 0 %s %s">%s%s</svg>'
            % (lab, _fmt(w), _fmt(h), _fmt(w), _fmt(h), ("<defs>%s</defs>" % defs) if defs else "", inner))


def mark_svg(mode="color", height=100.0, pad=0.0, label=BRAND, gid="slg", square=False):
    """The S alone, scaled to `height` px tall (square=True centres it in a height x height box)."""
    bx0, by0, bx1, by1 = MARK_BOX
    k = (height - 2 * pad) / (by1 - by0)
    w = (bx1 - bx0) * k + 2 * pad
    ox = (height - w) / 2 if square else 0.0
    if square:
        w = height
    T = lambda x, y: ((x - bx0) * k + pad + ox, (by1 - y) * k + pad)
    grad, body = _mark_group(T, mode, gid)
    return _svg(w, height, body, label, grad), w, height


def full_svg(mode="color", height=140.0, label=BRAND, gid="slf"):
    """The original logo exactly as the profile shows it: the S over the italic tagline."""
    bx0, by0, bx1, by1 = _union(MARK_BOX, TAG_BOX)
    pad = 2.0
    k = (height - 2 * pad) / (by1 - by0)
    w = (bx1 - bx0) * k + 2 * pad
    T = lambda x, y: ((x - bx0) * k + pad, (by1 - y) * k + pad)
    grad, body = _mark_group(T, mode, gid)
    tag_col = NAVY if mode == "color" else WHITE
    tag = "".join(_d(t["path"], T) for t in PARTS["tagline"])
    body += '<path fill="%s" d="%s"/>' % (tag_col, tag)
    return _svg(w, height, body, label, grad), w, height


def lockup_svg(mode="color", height=56.0, label=BRAND, gid="sll"):
    """Header/footer lock-up: the S beside the company name in the profile's Gotham Black.

    Two lines, as the profile's one-line heading does not fit a header:
    SMARTLINE / POINT CLEANING HUB LTD, the second line tracked to the width of the first.
    """
    bx0, by0, bx1, by1 = MARK_BOX
    k = height / (by1 - by0)
    mw = (bx1 - bx0) * k
    T = lambda x, y: ((x - bx0) * k, (by1 - y) * k)
    grad, body = _mark_group(T, mode, gid)

    s1 = height * 0.50                           # cap height 0.70 em -> 35% of the mark
    w1 = text_width("SMARTLINE", s1)
    line2 = "POINT CLEANING HUB LTD"
    s2 = height * 0.170
    natural = text_width(line2, s2)
    gaps = len(line2) - 1
    track = (w1 - natural) / gaps
    cap1, cap2 = 0.70 * s1, 0.70 * s2
    gap = height * 0.15
    block = cap1 + gap + cap2
    top = (height - block) / 2
    tx = mw + height * 0.26
    c1 = INDIGO if mode == "color" else WHITE
    c2 = NAVY if mode == "color" else WHITE
    l1, _ = _text_paths("SMARTLINE", s1, tx, top + cap1, c1)
    l2, _ = _text_paths(line2, s2, tx, top + cap1 + gap + cap2, c2, tracking=track,
                        opacity=None if mode == "color" else "0.78")
    w = tx + w1 + 1
    return _svg(w, height, body + l1 + l2, label, grad), w, height


def mark_parts_svg(height=96.0, cls="", gid="slp", mode="rev"):
    """Inline <svg> of the S with each part addressable (.m-s, .m-sw, .m-dr) so CSS can
    assemble it — used by the loader. Decorative: aria-hidden."""
    bx0, by0, bx1, by1 = MARK_BOX
    k = height / (by1 - by0)
    w = (bx1 - bx0) * k
    T = lambda x, y: ((x - bx0) * k, (by1 - y) * k)
    s, sw, dr = PARTS["S"], PARTS["swoosh"], PARTS["droplet"]
    ax = sw["axis"]
    (gx1, gy1), (gx2, gy2) = T(ax[0], ax[1]), T(ax[2], ax[3])
    stops = "".join('<stop offset="%s" stop-color="%s"/>' % (_fmt(o), c) for o, c in sw["stops"])
    fill = WHITE if mode == "rev" else INDIGO
    drop = WHITE if mode == "rev" else NAVY
    return ('<svg class="%s" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %s %s" width="%s" height="%s" aria-hidden="true" focusable="false">'
            '<defs><linearGradient id="%s" gradientUnits="userSpaceOnUse" x1="%s" y1="%s" x2="%s" y2="%s">%s</linearGradient></defs>'
            '<path class="m-s" fill="%s" fill-rule="%s" d="%s"/>'
            '<path class="m-sw" fill="url(#%s)" fill-rule="%s" d="%s"/>'
            '<path class="m-dr" fill="%s" fill-rule="%s" d="%s"/></svg>'
            % (cls, _fmt(w), _fmt(height), _fmt(w), _fmt(height), gid, _fmt(gx1), _fmt(gy1), _fmt(gx2), _fmt(gy2), stops,
               fill, s["rule"], _d(s["path"], T), gid, sw["rule"], _d(sw["path"], T), drop, dr["rule"], _d(dr["path"], T)))


def seal_core_svg(size=200.0):
    """Centre of the Clean Quality Guaranteed seal: ink disc, brass ring, the reversed S."""
    c = size / 2
    mh = size * 0.40
    bx0, by0, bx1, by1 = MARK_BOX
    k = mh / (by1 - by0)
    mw = (bx1 - bx0) * k
    ox, oy = c - mw / 2, c - mh / 2
    T = lambda x, y: ((x - bx0) * k + ox, (by1 - y) * k + oy)
    grad, body = _mark_group(T, "rev", "sls")
    inner = ('<circle cx="%s" cy="%s" r="%s" fill="#101238"/>' % (_fmt(c), _fmt(c), _fmt(size * 0.495))
             + '<circle cx="%s" cy="%s" r="%s" fill="none" stroke="#F8951A" stroke-width="0.9" stroke-opacity="0.7"/>'
             % (_fmt(c), _fmt(c), _fmt(size * 0.32)) + body)
    return _svg(size, size, inner, "Clean Quality Guaranteed", grad)


def render_png(svg_kind, px, bg=None, pad_frac=0.14):
    """Raster from the ORIGINAL profile page (MuPDF renders the real shading), square, centred.

    svg_kind: 'mark' only for now. bg None -> transparent RGBA.
    """
    from PIL import Image
    doc = pymupdf.open(PDF)
    page = doc[0]
    bx0, by0, bx1, by1 = MARK_BOX
    # user space -> page space: x shifts by the MediaBox origin (-9); y flips about the MediaBox top
    mb = page.mediabox
    top = mb.y1
    clip = pymupdf.Rect(bx0 - mb.x0 - 0.3, top - by1 - 0.3, bx1 - mb.x0 + 0.3, top - by0 + 0.3)
    inner = px * (1 - 2 * pad_frac)
    zoom = inner / max(clip.width, clip.height) * 4          # 4x supersample, then downsize
    pix = page.get_pixmap(matrix=pymupdf.Matrix(zoom, zoom), clip=clip, alpha=True)
    im = Image.frombytes("RGBA", (pix.width, pix.height), pix.samples)
    scale = inner / max(im.width, im.height)
    im = im.resize((max(1, round(im.width * scale)), max(1, round(im.height * scale))), Image.LANCZOS)
    canvas = Image.new("RGBA", (px, px), bg + (255,) if bg else (0, 0, 0, 0))
    canvas.alpha_composite(im, ((px - im.width) // 2, (px - im.height) // 2))
    return canvas


# ------------------------------------------------------------------ verify
def verify():
    p = PARTS
    errs = []
    if not p["S"] or p["S"]["colour"] != INDIGO:
        errs.append("indigo S not found")
    if not p["droplet"] or p["droplet"]["colour"] != NAVY:
        errs.append("navy droplet not found (got %r)" % (p["droplet"] and p["droplet"]["colour"]))
    if not p["swoosh"] or len(p["swoosh"]["stops"]) < 3:
        errs.append("gradient swoosh not found")
    if len(p["tagline"]) < 15:
        errs.append("tagline outlines: %d shapes, expected ~18" % len(p["tagline"]))
    missing = sorted(set("SMARTLINEPOINTCLEANINGHUBLTD") - set(GLYPHS))
    if missing:
        errs.append("Gotham Black subset lacks %s" % missing)
    w = MARK_BOX[2] - MARK_BOX[0]
    h = MARK_BOX[3] - MARK_BOX[1]
    if not (0.8 < w / h < 1.0):
        errs.append("mark proportions off: %.3f" % (w / h))
    if errs:
        raise SystemExit("logo_original verify() FAILED:\n  - " + "\n  - ".join(errs))
    return "logo_original OK: S %s, droplet %s, swoosh %d stops %s, tagline %d outlines, %d glyphs" % (
        p["S"]["colour"], p["droplet"]["colour"], len(p["swoosh"]["stops"]),
        "/".join(c for _, c in p["swoosh"]["stops"]), len(p["tagline"]), len(GLYPHS))


STATUS = verify()

if __name__ == "__main__":
    print(STATUS)
    out = os.path.join(ROOT, "logo", "original")
    os.makedirs(out, exist_ok=True)
    for name, (svg, w, h) in {
        "smartline-mark.svg": mark_svg("color", 400),
        "smartline-mark-reverse.svg": mark_svg("rev", 400),
        "smartline-logo.svg": full_svg("color", 560),
        "smartline-logo-reverse.svg": full_svg("rev", 560),
        "smartline-lockup.svg": lockup_svg("color", 112),
        "smartline-lockup-reverse.svg": lockup_svg("rev", 112),
    }.items():
        with open(os.path.join(out, name), "w", encoding="utf-8") as f:
            f.write(svg)
        print("wrote logo/original/%s  %.0f x %.0f" % (name, w, h))
    for px in (512, 1024):
        render_png("mark", px).save(os.path.join(out, "smartline-mark-%d.png" % px), optimize=True)
    print("wrote logo/original/smartline-mark-512.png, -1024.png (transparent)")
