# -*- coding: utf-8 -*-
"""Smartline Point Cleaning Hub Ltd — premium logo system (vector, ReportLab).

The first round failed because it was built from uniform fat round-capped
strokes and cartoon sparkles. Premium comes from the opposite set of moves:

  * high-contrast letterforms (Bodoni / Baskerville) instead of drawn blobs
  * flat, cut terminals; no rounded caps anywhere
  * hairlines \u2014 0.4pt rules, inset borders, engraved rings
  * tracked-out small caps (Copperplate) for the wordmark
  * a deep ink navy with brass, not a bright orange at full saturation
  * air: the mark occupies less of its box, so it reads as a seal, not a sticker

Every mark is drawn as vector on the canvas, so it stays sharp at any size.
"""
import math
from reportlab.lib.colors import HexColor, Color
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

F = "C:/Windows/Fonts/"
pdfmetrics.registerFont(TTFont("Bodoni", F + "BOD_R.TTF"))
pdfmetrics.registerFont(TTFont("Bodoni-B", F + "BOD_B.TTF"))
pdfmetrics.registerFont(TTFont("Bodoni-I", F + "BOD_I.TTF"))
pdfmetrics.registerFont(TTFont("Baskerville", F + "BASKVILL.TTF"))
pdfmetrics.registerFont(TTFont("Copper", F + "COPRGTL.TTF"))
pdfmetrics.registerFont(TTFont("Copper-B", F + "COPRGTB.TTF"))

# ---------------------------------------------------------------- palette
INK = HexColor("#0E1430")      # deep ink navy  (their navy, taken deeper)
INDIGO = HexColor("#241E63")   # their indigo, settled
BRASS = HexColor("#B8862F")    # brass accent  (their orange, matured)
BRASS_LT = HexColor("#D7B468")
AMBER = HexColor("#D9812A")    # for the warmer option
PAPER = HexColor("#FAF8F4")
STONE = HexColor("#E7E3DA")
WHITE = HexColor("#FFFFFF")
GREY = HexColor("#6E6A64")


def mode_colors(mode):
    """returns (body, accent, counter) for color | mono | rev"""
    if mode == "mono":
        return INK, INK, WHITE
    if mode == "rev":
        return WHITE, BRASS_LT, INK
    return INK, BRASS, WHITE


def tracked(c, text, x, y, font, size, tracking, color, centre=None):
    """letterspaced text. centre=x gives centred tracked text."""
    c.setFont(font, size)
    c.setFillColor(color)
    w = sum(pdfmetrics.stringWidth(ch, font, size) + tracking for ch in text) - tracking
    cx = (centre - w / 2.0) if centre is not None else x
    for ch in text:
        c.drawString(cx, y, ch)
        cx += pdfmetrics.stringWidth(ch, font, size) + tracking
    return w


def arc_text(c, text, cx, cy, r, font, size, color, tracking=0.0, bottom=False,
             center_deg=None):
    """Text set around a circle, reading left to right.

    Top (bottom=False): characters run clockwise from the 12 o'clock centre,
    baseline on the radius, up pointing outward.
    Bottom (bottom=True): characters run anticlockwise from 6 o'clock, up
    pointing inward, so the legend still reads the right way up.
    """
    c.setFont(font, size)
    c.setFillColor(color)
    widths = [pdfmetrics.stringWidth(ch, font, size) + tracking for ch in text]
    total = sum(widths) - tracking
    half = math.degrees((total / 2.0) / r)
    if center_deg is None:
        center_deg = 90.0 if not bottom else 270.0
    ang = center_deg + half if not bottom else center_deg - half
    for ch, w in zip(text, widths):
        step = math.degrees(w / r)
        a = ang - step / 2.0 if not bottom else ang + step / 2.0
        c.saveState()
        c.translate(cx, cy)
        if not bottom:
            c.rotate(a - 90.0)
            c.translate(0, r)
        else:
            c.rotate(a + 90.0)
            c.translate(0, -r)
        c.drawCentredString(0, 0, ch)
        c.restoreState()
        ang = ang - step if not bottom else ang + step


def _glyph(c, ch, cx, y, size, font, color):
    c.setFont(font, size)
    c.setFillColor(color)
    c.drawCentredString(cx, y, ch)


def diamond(c, cx, cy, r, color):
    c.setFillColor(color)
    p = c.beginPath()
    p.moveTo(cx, cy + r); p.lineTo(cx + r * .62, cy); p.lineTo(cx, cy - r)
    p.lineTo(cx - r * .62, cy); p.close()
    c.drawPath(p, stroke=0, fill=1)


def droplet_path(c, cx, cy, s):
    """classic droplet, apex up, centred on (cx, cy) in a box of side s"""
    p = c.beginPath()
    top = cy + s * .46
    r = s * .30
    bot_c = cy - s * .10
    p.moveTo(cx, top)
    p.curveTo(cx + s * .20, cy + s * .18, cx + r, bot_c + r * .55, cx + r, bot_c)
    p.curveTo(cx + r, bot_c - r * 1.32, cx - r, bot_c - r * 1.32, cx - r, bot_c)
    p.curveTo(cx - r, bot_c + r * .55, cx - s * .20, cy + s * .18, cx, top)
    p.close()
    return p


# ================================================================ concepts
def crest(c, x, y, s, mode):
    """01 \u2014 The Seal. Engraved roundel, tracked legend, Bodoni S.
    The register of a chartered firm, not a cleaning flyer."""
    body, accent, counter = mode_colors(mode)
    cx, cy = x + s / 2, y + s / 2
    c.setFillColor(body)
    c.circle(cx, cy, s * .50, stroke=0, fill=1)
    c.setStrokeColor(accent); c.setLineWidth(max(.4, s * .008))
    c.circle(cx, cy, s * .445, stroke=1, fill=0)
    c.setLineWidth(max(.3, s * .004))
    c.circle(cx, cy, s * .425, stroke=1, fill=0)
    _glyph(c, "S", cx, cy - s * .115, s * .40, "Bodoni", accent if mode != "mono" else counter)
    arc_text(c, "SMARTLINE POINT", cx, cy, s * .330, "Copper",
             s * .060, counter, s * .026, bottom=False)
    arc_text(c, "CLEANING HUB LTD", cx, cy, s * .365, "Copper",
             s * .052, counter, s * .024, bottom=True)
    diamond(c, cx - s * .345, cy - s * .01, s * .030, accent)
    diamond(c, cx + s * .345, cy - s * .01, s * .030, accent)


def plate(c, x, y, s, mode):
    """02 \u2014 The Plate. A brass-bordered monogram plate: door signage,
    embossed on a folder, foil-blocked on a card."""
    body, accent, counter = mode_colors(mode)
    c.setFillColor(body)
    c.roundRect(x + s * .085, y + s * .02, s * .83, s * .96, s * .055, stroke=0, fill=1)
    c.setStrokeColor(accent); c.setLineWidth(max(.45, s * .009))
    c.roundRect(x + s * .125, y + s * .055, s * .75, s * .89, s * .04, stroke=1, fill=0)
    c.setLineWidth(max(.3, s * .0045))
    c.roundRect(x + s * .150, y + s * .080, s * .70, s * .84, s * .032, stroke=1, fill=0)
    cx = x + s / 2
    _glyph(c, "S", cx, y + s * .40, s * .42, "Bodoni", counter)
    c.setStrokeColor(accent); c.setLineWidth(max(.4, s * .008))
    c.line(cx - s * .16, y + s * .315, cx + s * .16, y + s * .315)
    tracked(c, "EST. 2018", 0, y + s * .17, "Copper", s * .055,
            s * .030, accent, centre=cx)


def modulated(c, x, y, s, mode):
    """03 — The Letter. One high-contrast S over an engraved rule. Nothing
    else. Cheapest to print, strongest at distance, impossible to date."""
    body, accent, counter = mode_colors(mode)
    cx = x + s / 2
    _glyph(c, "S", cx, y + s * .285, s * .80, "Bodoni", body)
    c.setStrokeColor(accent); c.setLineWidth(max(.45, s * .009))
    c.line(x + s * .125, y + s * .175, x + s * .875, y + s * .175)
    c.setLineWidth(max(.3, s * .005))
    c.line(x + s * .125, y + s * .150, x + s * .875, y + s * .150)
    diamond(c, x + s * .07, y + s * .1635, s * .036, accent)
    diamond(c, x + s * .93, y + s * .1635, s * .036, accent)


def ligature(c, x, y, s, mode):
    """04 \u2014 The Cipher. S and P interlocked inside an engraved ring \u2014 the
    monogram a hotel or a law firm would use. The most ownable of the six."""
    body, accent, counter = mode_colors(mode)
    cx, cy = x + s / 2, y + s / 2
    c.setStrokeColor(body); c.setLineWidth(max(.5, s * .011))
    c.circle(cx, cy, s * .47, stroke=1, fill=0)
    c.setStrokeColor(accent); c.setLineWidth(max(.3, s * .005))
    c.circle(cx, cy, s * .435, stroke=1, fill=0)
    _glyph(c, "S", cx - s * .135, cy - s * .180, s * .58, "Bodoni", body)
    _glyph(c, "P", cx + s * .150, cy - s * .180, s * .58, "Bodoni", accent)


def droplet(c, x, y, s, mode):
    """05 \u2014 The Droplet, drawn as a hairline. The cleaning cue kept quiet:
    an outline, not a solid blob, with the S sitting inside it."""
    body, accent, counter = mode_colors(mode)
    cx, cy = x + s / 2, y + s / 2
    p = droplet_path(c, cx, cy + s * .02, s * 1.02)
    c.setStrokeColor(body); c.setLineWidth(max(.6, s * .013))
    c.drawPath(p, stroke=1, fill=0)
    _glyph(c, "S", cx, cy - s * .145, s * .42, "Bodoni", body)
    c.setFillColor(accent)
    p3 = droplet_path(c, x + s * .845, y + s * .80, s * .20)
    c.drawPath(p3, stroke=0, fill=1)


def stamp(c, x, y, s, mode):
    """06 \u2014 The Stamp. A quiet ink square for a wordmark-led identity: the
    name does the talking, the stamp signs it."""
    body, accent, counter = mode_colors(mode)
    c.setFillColor(body)
    c.rect(x + s * .10, y + s * .10, s * .80, s * .80, stroke=0, fill=1)
    c.setStrokeColor(accent); c.setLineWidth(max(.4, s * .008))
    c.rect(x + s * .155, y + s * .155, s * .69, s * .69, stroke=1, fill=0)
    cx = x + s / 2
    _glyph(c, "S", cx, y + s * .325, s * .44, "Bodoni", counter)
    c.setStrokeColor(accent); c.setLineWidth(max(.3, s * .005))
    c.line(cx - s * .13, y + s * .265, cx + s * .13, y + s * .265)


CONCEPTS = [
    ("01", "The Seal", crest,
     "An engraved roundel with the name set around it and a Bodoni S at the centre. "
     "Reads as a chartered firm \u2014 the register facility managers and schools trust."),
    ("02", "The Plate", plate,
     "A brass-bordered monogram plate: door signage, foil on a folder, embossed on a card. "
     "Premium comes from the double hairline border and the air inside it."),
    ("03", "The Letter", modulated,
     "One high-contrast S with a single brass hairline passing behind it. Nothing else. "
     "Cheapest to print, strongest at distance, impossible to date."),
    ("04", "The Cipher", ligature,
     "S and P interlocked inside an engraved ring \u2014 the monogram a hotel or a law firm "
     "would use. The most ownable of the six, and the hardest to copy."),
    ("05", "The Droplet", droplet,
     "The cleaning cue kept quiet: a hairline droplet outline with the S inside, and one "
     "small brass droplet off the shoulder. Light, modern, unmistakably clean."),
    ("06", "The Stamp", stamp,
     "A wordmark-led identity \u2014 the name does the talking and this quiet ink square signs "
     "it. The most understated, and the easiest to apply across uniforms and vehicles."),
]


# ---------------------------------------------------------------- lock-ups
def wordmark(c, x, y, scale, mode="color", tagline=True):
    """tracked Copperplate lock-up text. y = baseline of SMARTLINE."""
    body, accent, counter = mode_colors(mode)
    name_c = body if mode != "rev" else WHITE
    sub_c = GREY if mode == "color" else (body if mode == "mono" else HexColor("#B9BCCB"))
    tracked(c, "SMARTLINE", x, y, "Copper-B", 13.5 * scale, 2.3 * scale, name_c)
    c.setStrokeColor(accent); c.setLineWidth(.5 * scale)
    c.line(x + .5, y - 7.5 * scale, x + 126 * scale, y - 7.5 * scale)
    tracked(c, "POINT CLEANING HUB LTD", x, y - 17 * scale, "Copper",
            6.6 * scale, 1.7 * scale, sub_c)
    if tagline:
        c.setFont("Bodoni-I", 9 * scale)
        c.setFillColor(sub_c)
        c.drawString(x + .5, y - 31 * scale, "Assuring you the best")


def stacked(c, cx, y, scale, mode="color"):
    """centred stacked lock-up. y = baseline of SMARTLINE."""
    body, accent, counter = mode_colors(mode)
    name_c = body if mode != "rev" else WHITE
    sub_c = GREY if mode == "color" else (body if mode == "mono" else HexColor("#B9BCCB"))
    tracked(c, "SMARTLINE", 0, y, "Copper-B", 11 * scale, 2.0 * scale, name_c, centre=cx)
    c.setStrokeColor(accent); c.setLineWidth(.5 * scale)
    c.line(cx - 46 * scale, y - 6.5 * scale, cx + 46 * scale, y - 6.5 * scale)
    tracked(c, "POINT CLEANING HUB LTD", 0, y - 15 * scale, "Copper",
            5.6 * scale, 1.5 * scale, sub_c, centre=cx)
