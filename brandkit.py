# -*- coding: utf-8 -*-
"""Allen Muraya Maina house style for client documents (ReportLab).
Palette, fonts, logo mark and the shared furniture used by every sheet."""
from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import HexColor, Color
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT

NAVY = HexColor("#14213D"); DEEP = HexColor("#0B1529"); MID = HexColor("#1D3A6B")
SKY = HexColor("#0EA5E9"); INDIGO = HexColor("#6366F1")
INK = HexColor("#14161F"); BODY = HexColor("#4A4F60"); MUTE = HexColor("#8A8F9E")
LINE = HexColor("#E2E4EA"); SOFT = HexColor("#F6F7F9"); WHITE = HexColor("#FFFFFF")
TINT = HexColor("#EAF6FD")

F = "C:/Windows/Fonts/"
pdfmetrics.registerFont(TTFont("S", F + "segoeui.ttf"))
pdfmetrics.registerFont(TTFont("S-SB", F + "seguisb.ttf"))
pdfmetrics.registerFont(TTFont("S-B", F + "segoeuib.ttf"))
pdfmetrics.registerFont(TTFont("S-L", F + "segoeuil.ttf"))
pdfmetrics.registerFontFamily("S", normal="S", bold="S-SB", italic="S", boldItalic="S-SB")

W, H = A4
M = 46
CW = W - 2 * M


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
    p = c.beginPath(); p.roundRect(x, y, w, h, h / 2); c.clipPath(p, stroke=0)
    c.linearGradient(x, y, x + w, y, [NAVY, MID, SKY], [0, .42, 1], extend=True)
    c.restoreState()


def corner_facets(c):
    c.saveState()

    def plane(pts, col, alpha):
        c.setFillColor(Color(col.red, col.green, col.blue, alpha=alpha))
        p = c.beginPath(); p.moveTo(*pts[0])
        for q in pts[1:]:
            p.lineTo(*q)
        p.close(); c.drawPath(p, stroke=0, fill=1)

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
    c.setFillColor(fill); c.setStrokeColor(border); c.setLineWidth(lw)
    c.roundRect(x, y, w, h, r, stroke=1 if border else 0, fill=1)


def eyebrow_ls(c, txt, x, y, color=MUTE, size=7, ls=1.6, font="S-SB"):
    c.setFont(font, size); c.setFillColor(color)
    cx = x
    for ch in txt:
        c.drawString(cx, y, ch)
        cx += pdfmetrics.stringWidth(ch, font, size) + ls
    return cx


def logo_mark(c, x, y, s):
    c.saveState()
    p = c.beginPath(); p.roundRect(x, y, s, s, s * 0.235); c.clipPath(p, stroke=0)
    c.linearGradient(x, y + s, x + s, y, [MID, NAVY, DEEP], [0, .48, 1], extend=True)
    c.setFillColor(Color(1, 1, 1, alpha=.13))
    q = c.beginPath(); q.moveTo(x, y + s); q.lineTo(x + s, y + s); q.lineTo(x, y); q.close()
    c.drawPath(q, stroke=0, fill=1)
    c.setFillColor(WHITE)
    u = s / 100.0
    m = c.beginPath()
    pts = [(24, 26), (24, 74), (36, 74), (50, 50), (64, 74), (76, 74), (76, 26), (65, 26),
           (65, 56), (54, 37), (46, 37), (35, 56), (35, 26)]
    m.moveTo(x + pts[0][0] * u, y + pts[0][1] * u)
    for px, py in pts[1:]:
        m.lineTo(x + px * u, y + py * u)
    m.close(); c.drawPath(m, stroke=0, fill=1)
    c.restoreState()
    c.setFillColor(SKY); c.circle(x + s * 0.80, y + s * 0.80, s * 0.062, stroke=0, fill=1)


def masthead(c, title, subtitle, caption=None):
    """full masthead + title block. returns y below the title block."""
    corner_facets(c)
    top = H - 46
    logo_mark(c, M, top - 46, 46)
    c.setFont("S-SB", 15); c.setFillColor(NAVY)
    c.drawString(M + 58, top - 18, "Allen Muraya Maina")
    eyebrow_ls(c, "DESIGN. CODE. EXECUTE.", M + 58, top - 32, MUTE, 7, 1.5)
    c.setFont("S", 7.8); c.setFillColor(HexColor("#9AA0AE"))
    c.drawString(M + 58, top - 44, "Web Development  \u00b7  Data & Systems Consultant")

    rx = W - M
    eyebrow_ls(c, "CONTACT", rx - 62, top - 6, HexColor("#A8ACB8"), 6.8, 1.4)
    c.setFont("S-SB", 9); c.setFillColor(NAVY); c.drawRightString(rx, top - 20, "+254 792 507 750")
    c.setFont("S", 8.4); c.setFillColor(BODY)
    c.drawRightString(rx, top - 32, "murayamakingedits@gmail.com")
    c.drawRightString(rx, top - 43, "KRA PIN  A013413450I")

    grad_rule(c, M, top - 62, CW, 3)

    ty = top - 82
    c.setFont("S-L", 27); c.setFillColor(NAVY); c.drawString(M, ty - 20, title)
    c.setFont("S-SB", 10.5); c.setFillColor(MID); c.drawString(M, ty - 38, subtitle)
    y = ty - 38
    if caption:
        c.setFont("S", 8.6); c.setFillColor(MUTE); c.drawString(M, ty - 51, caption)
        y = ty - 51
    return y


def tickbox(c, x, y, s=11):
    c.setStrokeColor(HexColor("#B9BECC")); c.setLineWidth(.8); c.setFillColor(WHITE)
    c.roundRect(x, y, s, s, 2.2, stroke=1, fill=1)


def footer(c, label, page=None, pages=None):
    y = 40
    c.setStrokeColor(LINE); c.setLineWidth(.5); c.line(M, y + 16, W - M, y + 16)
    c.setFillColor(SKY); c.circle(M + 2, y + 5.5, 1.7, stroke=0, fill=1)
    c.setFont("S", 7.6); c.setFillColor(MUTE)
    c.drawString(M + 10, y + 3,
                 "Allen Muraya Maina  \u00b7  +254 792 507 750  \u00b7  murayamakingedits@gmail.com")
    c.setFont("S-SB", 7.6); c.setFillColor(NAVY)
    tail = label if page is None else "%s   |   Page %d of %d" % (label, page, pages)
    c.drawRightString(W - M, y + 3, tail)
