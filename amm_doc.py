# -*- coding: utf-8 -*-
"""Allen Muraya Maina - document kit for this engagement's PDFs (quotation, invoice).
Brand palette (navy / deep / mid / sky / indigo), Segoe UI, the faceted M mark, the masthead,
cards, letter-spaced eyebrows and the footer. Moved out of make_quotation.py unchanged so the
quotation still renders pixel-identical and the invoice matches it."""
from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import HexColor, Color
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT

# ---------------------------------------------------------------- brand
NAVY = HexColor("#14213D"); DEEP = HexColor("#0B1529"); MID = HexColor("#1D3A6B")
SKY = HexColor("#0EA5E9"); INDIGO = HexColor("#6366F1")
INK = HexColor("#14161F"); BODY = HexColor("#4A4F60"); MUTE = HexColor("#8A8F9E")
LINE = HexColor("#E2E4EA"); SOFT = HexColor("#F6F7F9"); WHITE = HexColor("#FFFFFF")

F = "C:/Windows/Fonts/"
pdfmetrics.registerFont(TTFont("S", F + "segoeui.ttf"))
pdfmetrics.registerFont(TTFont("S-SB", F + "seguisb.ttf"))
pdfmetrics.registerFont(TTFont("S-B", F + "segoeuib.ttf"))
pdfmetrics.registerFont(TTFont("S-L", F + "segoeuil.ttf"))
pdfmetrics.registerFontFamily("S", normal="S", bold="S-SB", italic="S", boldItalic="S-SB")

W, H = A4
M  = 46
CW = W - 2 * M

ISSUER = "Allen Muraya Maina"
PHONE = "+254 792 507 750"
EMAIL = "murayamakingedits@gmail.com"
KRA_PIN = "A013413450I"


def para(txt, font="S", size=9, leading=13, color=BODY, align=TA_LEFT):
    return Paragraph(txt, ParagraphStyle("p", fontName=font, fontSize=size,
                                         leading=leading, textColor=color, alignment=align))


def draw_para(c, txt, x, y, w, **kw):
    p = para(txt, **kw)
    _, h = p.wrap(w, 1000)
    p.drawOn(c, x, y - h)
    return y - h


def grad_rule(c, x, y, w, h):
    c.saveState()
    p = c.beginPath()
    p.roundRect(x, y, w, h, h / 2)
    c.clipPath(p, stroke=0)
    c.linearGradient(x, y, x + w, y, [NAVY, MID, SKY], [0, .42, 1], extend=True)
    c.restoreState()


def corner_facets(c):
    c.saveState()

    def plane(pts, col, alpha):
        c.setFillColor(Color(col.red, col.green, col.blue, alpha=alpha))
        p = c.beginPath()
        p.moveTo(*pts[0])
        for q in pts[1:]:
            p.lineTo(*q)
        p.close()
        c.drawPath(p, stroke=0, fill=1)

    plane([(W, H), (W, H - 128), (W - 128, H)], MID, .10)
    plane([(W, H), (W, H - 74), (W - 74, H)], INDIGO, .14)
    plane([(W - 54, H - 96), (W, H - 96), (W, H - 150)], SKY, .10)
    c.setFillColor(Color(SKY.red, SKY.green, SKY.blue, alpha=.55))
    c.circle(W - 48, H - 52, 4.4, stroke=0, fill=1)
    c.restoreState()


def card(c, x, y, w, h, fill=WHITE, border=LINE, r=7, lw=.6, shadow=False):
    if shadow:
        c.setFillColor(Color(0.08, 0.11, 0.2, alpha=.055))
        c.roundRect(x + 1.6, y - 2.0, w, h, r, stroke=0, fill=1)
    c.setFillColor(fill)
    c.setStrokeColor(border)
    c.setLineWidth(lw)
    c.roundRect(x, y, w, h, r, stroke=1 if border else 0, fill=1)


def eyebrow_ls(c, txt, x, y, color=MUTE, size=7, ls=1.6, font="S-SB"):
    c.setFont(font, size)
    c.setFillColor(color)
    cx = x
    for ch in txt:
        c.drawString(cx, y, ch)
        cx += pdfmetrics.stringWidth(ch, font, size) + ls
    return cx


def logo_mark(c, x, y, s):
    c.saveState()
    p = c.beginPath()
    p.roundRect(x, y, s, s, s * 0.235)
    c.clipPath(p, stroke=0)
    c.linearGradient(x, y + s, x + s, y, [MID, NAVY, DEEP], [0, .48, 1], extend=True)
    c.setFillColor(Color(1, 1, 1, alpha=.13))
    q = c.beginPath()
    q.moveTo(x, y + s); q.lineTo(x + s, y + s); q.lineTo(x, y); q.close()
    c.drawPath(q, stroke=0, fill=1)
    c.setFillColor(WHITE)
    u = s / 100.0
    m = c.beginPath()
    pts = [(24, 26), (24, 74), (36, 74), (50, 50), (64, 74), (76, 74), (76, 26), (65, 26),
           (65, 56), (54, 37), (46, 37), (35, 56), (35, 26)]
    m.moveTo(x + pts[0][0] * u, y + pts[0][1] * u)
    for px, py in pts[1:]:
        m.lineTo(x + px * u, y + py * u)
    m.close()
    c.drawPath(m, stroke=0, fill=1)
    c.restoreState()
    c.setFillColor(SKY)
    c.circle(x + s * 0.80, y + s * 0.80, s * 0.062, stroke=0, fill=1)


def footer(c, label, page, pages):
    y = 40
    c.setStrokeColor(LINE); c.setLineWidth(.5); c.line(M, y + 16, W - M, y + 16)
    c.setFillColor(SKY); c.circle(M + 2, y + 5.5, 1.7, stroke=0, fill=1)
    c.setFont("S", 7.6); c.setFillColor(MUTE)
    c.drawString(M + 10, y + 3,
                 "%s  \u00b7  %s  \u00b7  %s" % (ISSUER, PHONE, EMAIL))
    c.setFont("S-SB", 7.6); c.setFillColor(NAVY)
    c.drawRightString(W - M, y + 3, "%s   |   Page %d of %d" % (label, page, pages))


def masthead(c):
    """Page-one masthead: mark, name, tagline, contact block, gradient rule. Returns the rule's y."""
    top = H - 46
    logo_mark(c, M, top - 46, 46)
    c.setFont("S-SB", 15); c.setFillColor(NAVY)
    c.drawString(M + 58, top - 18, ISSUER)
    eyebrow_ls(c, "DESIGN. CODE. EXECUTE.", M + 58, top - 32, MUTE, 7, 1.5)
    c.setFont("S", 7.8); c.setFillColor(HexColor("#9AA0AE"))
    c.drawString(M + 58, top - 44, "Web Development  \u00b7  Data & Systems Consultant")
    rx = W - M
    eyebrow_ls(c, "CONTACT", rx - 62, top - 6, HexColor("#A8ACB8"), 6.8, 1.4)
    c.setFont("S-SB", 9); c.setFillColor(NAVY); c.drawRightString(rx, top - 20, PHONE)
    c.setFont("S", 8.4); c.setFillColor(BODY)
    c.drawRightString(rx, top - 32, EMAIL)
    c.drawRightString(rx, top - 43, "KRA PIN  " + KRA_PIN)
    grad_rule(c, M, top - 62, CW, 3)
    return top


def running_head(c, right_text):
    """Page-two-onward header: small mark, name, document name, gradient rule. Returns its top y."""
    top = H - 52
    logo_mark(c, M, top - 34, 34)
    c.setFont("S-SB", 11); c.setFillColor(NAVY); c.drawString(M + 44, top - 20, ISSUER)
    c.setFont("S", 8.2); c.setFillColor(MUTE)
    c.drawRightString(W - M, top - 20, right_text)
    grad_rule(c, M, top - 44, CW, 2.4)
    return top


def section(c, title, y):
    """Letter-spaced section eyebrow with a hairline under it."""
    eyebrow_ls(c, title, M, y, NAVY, 7.4, 1.6)
    c.setStrokeColor(LINE); c.setLineWidth(.5); c.line(M, y - 7, W - M, y - 7)


def navy_panel(c, x, y, w, h, r=8, corner=46):
    """Gradient navy panel with the sky corner facet (top-left at x, y)."""
    c.saveState()
    p = c.beginPath(); p.roundRect(x, y - h, w, h, r); c.clipPath(p, stroke=0)
    c.linearGradient(x, y, x + w, y - h, [MID, NAVY, DEEP], [0, .5, 1], extend=True)
    c.setFillColor(Color(SKY.red, SKY.green, SKY.blue, alpha=.16))
    q = c.beginPath(); q.moveTo(x + w, y); q.lineTo(x + w, y - corner); q.lineTo(x + w - corner, y); q.close()
    c.drawPath(q, stroke=0, fill=1)
    c.restoreState()
