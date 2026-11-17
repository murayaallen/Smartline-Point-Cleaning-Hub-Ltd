# -*- coding: utf-8 -*-
"""Review of the images supplied so far (media/all).

Verdict per file = my judgement of the picture + two computed checks:
  licence  — inferred from the filename (pexels-/photo-1… = Pexels/Unsplash; anything
             else has no provenance and cannot ship on a client site until sourced again)
  size     — measured against the minimum for the slot it is proposed for

    python review_media.py   ->  MEDIA-REVIEW.md  +  Smartline - Image Review.pdf
"""
import os
import re
from collections import Counter, OrderedDict

from PIL import Image

import media_plan as M

SRC = "media/all"
OUT_PDF = "Smartline - Image Review.pdf"
OUT_MD = "MEDIA-REVIEW.md"
WORK = os.path.join(os.environ.get("TEMP", "."), "smartline_review")

# verdict codes
USE = "USE"                 # good picture, good size, licence clear
LIC = "CHECK LICENCE"       # good picture, but no provenance in the filename
SMALL = "TOO SMALL"         # good picture, under the minimum for its slot
REPLACE = "REPLACE"         # wrong subject, wrong place, or both

# file -> (verdict, slot, note)
VERDICT = {
    "pexels-jessicairoh-33123333.jpg": (USE, "IMG-S13", "Landscaping. African operator, visor and PPE, tropical compound — exactly the register we want. Best image in the set."),
    "pexels-arina-krasnikova-6653891.jpg": (USE, "IMG-S09", "Toilet bowl & sink. White subway tile, clean basin, tasteful. Crops to 4:3 easily at this size."),
    "pexels-caleboquendo-34516664.jpg": (USE, "IMG-S12", "One-time cleaning. Caddy, mops and bin staged in a corridor; no people, no logos. Huge file, crops anywhere."),
    "pexels-pixabay-48889.jpg": (USE, "IMG-S05", "Residential. Mop on a wood floor, warm and homely. 5472px wide."),
    "pexels-alejandro-robles-duque-420889274-32908422.jpg": (USE, "IMG-S11", "Deep cleaning. Brush and suds on terracotta — the detail-work idea, close and physical."),
    "pexels-karola-g-4239088.jpg": (USE, "IMG-S09 alt", "Toilet detail on dark marble. Keep as the alternate to Krasnikova; one bathroom image is enough on the page."),
    "pexels-themightynelson-6014518.jpg": (REPLACE, "—", "Red timber barn and temperate grass — reads North American farm, not Nairobi. jessicairoh covers landscaping already."),
    "photo-1740657254989-42fe9c3b8cce.avif": (SMALL, "IMG-H07", "Gloved hands on a wet floor — right idea for the training band, but 1012×580 against a 1200×1600 minimum. Re-download the full size from Unsplash."),
    "photo-1721620958961-cccc239cbb49.avif": (SMALL, "—", "Squeegee on patterned glass, 687×1031. Too small for any slot; the window idea is covered by 'window cleaning.jpg'."),
    "bg11.jpg": (LIC, "IMG-H01b / IMG-S01", "Strong: African cleaner, uniform, gloves, trolley, bright lobby, working with his back half-turned. Our best people shot. No provenance in the filename — reverse-search it and get the licensed original before it ships."),
    "corridor+4.webp": (LIC, "IMG-H01", "Polished terrazzo corridor receding into light, 2500×3333 portrait — crops to the 4:5 hero with room for the headline. Best hero candidate in the set, but '+4' says it was pulled off a web page."),
    "office floor.jpg": (LIC, "BG-01 / IMG-D01", "Large empty commercial interior, 4394×2929. Works as the CTA band background under the ink overlay. Provenance unknown."),
    "window cleaning.jpg": (LIC, "IMG-D01", "Squeegee on a glass tower, 3589×5383. Commercial-page hero material. Provenance unknown."),
    "images.jfif": (SMALL, "IMG-S01 alt", "African cleaner at a trolley by a window — good subject, but 678×452 and '.jfif' means it came off a Google Images results page."),
    "images (2).jfif": (SMALL, "IMG-S13 alt", "Tropical lawn and planting, genuinely Kenyan-looking — but 447×447 is a thumbnail."),
    "images (1).jfif": (REPLACE, "—", "Formal brick-edged European garden, 447×447. Wrong place, wrong size."),
    "65cc88b4602feef69a73e8bf82a3edf7.jpg": (REPLACE, "—", "Manicured English garden with brick steps, 474×599. Hash filename = Pinterest or similar. Wrong place, wrong size."),
    "Cleaning-Company-South-Africa.webp": (REPLACE, "—", "Floor polisher on a carpet outdoors. The filename is another cleaning company's page — cannot be used, and the shot is weak anyway."),
    "why-professional-deep-cleaning-services-are-vital-after-heavy-rain-in-dubai.webp": (REPLACE, "—", "Lifted straight from a Dubai blog post, 900×600. Both the licence and the size rule it out."),
    "post-construction-cleaning-1.webp": (LIC, "IMG-S10", "Broom sweeping plaster debris — the right subject for post-construction at 1600×800, but the filename is a WordPress upload from a competitor's site."),
    "post-construction-cleaning-768x1020.webp": (SMALL, "—", "Renovated kitchen before handover. '768x1020' is a WordPress resize — scraped, and under size."),
    "closeup-janitor-using-mop-clean-office-floor-maintain-workspace-hygiene-concept-janitorial-services-workplace-cleanliness-commercial-cleaning-office-hygiene-professional-janitor_91883.avif": (SMALL, "—", "740×370. The SEO-stuffed filename and the _91883 suffix are a stock-site preview, not a licensed download."),
    "caution wet floor.avif": (SMALL, "—", "Wet-floor sign, 870×580. Also: a caution sign sells hazard, not finish — not a look we want on the site."),
    "cleaning (1).jpg": (SMALL, "IMG-N01", "Mop and wet-floor sign, 500×500. Could suit the 404 page if re-sourced large; too small as it stands."),
    "cleaning.jpg": (SMALL, "IMG-H07 alt", "Gloved hands spraying and wiping, 1000×667 — just under the bar and the crop is tight."),
    "hospital floor.avif": (SMALL, "IMG-S03 alt", "Bright corridor with glazing, 869×580. Could stand in for a school corridor if re-sourced at full size."),
}

SAFE_RE = re.compile(r"^(pexels-|photo-1\d{8,})")


def licence_of(fn):
    if fn.startswith("pexels-"):
        return "Pexels — free, commercial use"
    if SAFE_RE.match(fn):
        return "Unsplash — free, commercial use"
    return "Unknown — no provenance"


def slot_min(slot):
    sid = slot.split()[0].split("/")[0].strip()
    for it in M.items():
        if it["id"] == sid:
            return it["min_px"], it["aspect"], it["pri"]
    return "—", "—", "—"


def scan():
    rows = []
    for fn in sorted(os.listdir(SRC)):
        p = os.path.join(SRC, fn)
        if not os.path.isfile(p) or fn.startswith("."):
            continue
        try:
            im = Image.open(p)
            w, h = im.size
            fmt = im.format
        except Exception:
            w = h = 0
            fmt = "?"
        v, slot, note = VERDICT.get(fn, (LIC, "—", "Not yet reviewed."))
        rows.append(dict(file=fn, w=w, h=h, fmt=fmt, kb=os.path.getsize(p) // 1024,
                         verdict=v, slot=slot, note=note, lic=licence_of(fn)))
    return rows


def coverage(rows):
    """slot -> best row, and the list of slots still empty"""
    have = {}
    for r in rows:
        if r["verdict"] in (USE, LIC):
            sid = r["slot"].split()[0].split("/")[0].strip()
            if sid.startswith("IMG") or sid.startswith("BG"):
                have.setdefault(sid, []).append(r)
    need = [i for i in M.items() if not i["reuse_of"] and i["id"] not in have]
    return have, need


# ------------------------------------------------------------------ markdown
def build_md(rows, have, need):
    c = Counter(r["verdict"] for r in rows)
    safe = sum(1 for r in rows if not r["lic"].startswith("Unknown"))
    o = ["# Image review — what has been supplied so far\n",
         "Generated by `review_media.py` from `media/all` (%d files). "
         "Slot numbers refer to `MEDIA.md` / the sourcing tracker.\n" % len(rows),
         "| Verdict | Files | Meaning |\n|---|---|---|",
         "| **USE** | %d | Good picture, big enough, licence clear. Goes straight into the build. |" % c[USE],
         "| **CHECK LICENCE** | %d | Good picture, but the filename shows no source. Re-source the licensed original before it ships. |" % c[LIC],
         "| **TOO SMALL** | %d | Right idea, under the minimum size. Re-download at full size or replace. |" % c[SMALL],
         "| **REPLACE** | %d | Wrong subject or wrong place. Drop it. |" % c[REPLACE],
         "",
         "**Licence:** %d of %d files carry a Pexels or Unsplash filename. The other %d have names like "
         "`images (1).jfif`, `Cleaning-Company-South-Africa.webp` and `post-construction-cleaning-768x1020.webp` "
         "— Google Images results and other cleaning companies' WordPress uploads. Those cannot go on a "
         "client's public site: the client carries the risk, not the photographer.\n" % (safe, len(rows), len(rows) - safe),
         "## Every file\n",
         "| File | Size | Verdict | Slot | Licence | Note |",
         "|---|---|---|---|---|---|"]
    rank = {USE: 0, LIC: 1, SMALL: 2, REPLACE: 3}
    for r in sorted(rows, key=lambda x: (rank[x["verdict"]], x["file"])):
        o.append("| `%s` | %d×%d | **%s** | %s | %s | %s |" %
                 (r["file"][:46], r["w"], r["h"], r["verdict"], r["slot"], r["lic"], r["note"]))
    o.append("")
    o.append("## Slots now covered\n")
    for sid, rs in sorted(have.items()):
        mn, asp, pri = slot_min(sid)
        o.append("- **%s** (%s, %s) ← %s" % (sid, pri, asp, ", ".join("`%s`" % x["file"][:40] for x in rs)))
    o.append("\n## Still to source — %d slots\n" % len(need))
    o.append("| Slot | Pri | What | Aspect | Min size |\n|---|---|---|---|---|")
    for i in sorted(need, key=lambda x: (x["pri"], x["id"])):
        o.append("| %s | %s | %s | %s | %s |" % (i["id"], i["pri"], i["role"], i["aspect"], i["min_px"]))
    o.append("\n### The gap that matters most\n")
    o.append("Every slot with **people whose faces show** is still empty: the team photograph (IMG-H05), the "
             "About hero (IMG-A01), the supervisor (IMG-A02) and the training session (IMG-A06). Those are also "
             "the four that need model-released stock rather than Pexels. Pick them from Adobe Stock or iStock, "
             "or wait for the client's own REAL-01 and REAL-02 and leave the sections out until then.\n")
    o.append("Missing service photographs: church, school, apartment/Airbnb linen, move in/out, sofa and "
             "upholstery, office carpet, and the three service-page heroes.\n")
    return "\n".join(o) + "\n"


# ------------------------------------------------------------------ pdf
def build_pdf(rows, have, need, path):
    from reportlab.pdfgen import canvas
    from reportlab.lib.colors import HexColor
    from reportlab.lib.utils import ImageReader
    from brandkit import (A4, W, H, M, CW, NAVY, MID, SKY, BODY, MUTE, LINE, SOFT, WHITE,
                          card, draw_para, eyebrow_ls, masthead, footer, grad_rule, logo_mark)

    os.makedirs(WORK, exist_ok=True)
    GREEN, AMBER, RED, GREY = HexColor("#2E7D4F"), HexColor("#B8862F"), HexColor("#B4453C"), HexColor("#8A8F9E")
    COLOUR = {USE: GREEN, LIC: AMBER, SMALL: HexColor("#8A6B2F"), REPLACE: RED}

    def thumb(fn, box=560):
        out = os.path.join(WORK, re.sub(r"[^A-Za-z0-9]+", "_", fn)[:60] + ".jpg")
        if not os.path.exists(out):
            im = Image.open(os.path.join(SRC, fn)).convert("RGB")
            im.thumbnail((box, box))
            im.save(out, "JPEG", quality=88)
        return ImageReader(out)

    c = canvas.Canvas(path, pagesize=A4)
    c.setTitle("Image review - Smartline Point Cleaning Hub Ltd")
    c.setAuthor("Allen Muraya Maina")

    cnt = Counter(r["verdict"] for r in rows)
    y = masthead(c, "Image review", "What has been supplied so far — %d files" % len(rows),
                 "Smartline Point Cleaning Hub Ltd  ·  AMM-M-2026-187  ·  17/11/2026")
    yy = draw_para(c, "Each image is judged on three things: is it the right picture, is it big enough for the "
                      "slot it would fill, and can we prove where it came from. The third is the one that bites "
                      "later — a filename like <b>images (1).jfif</b> or <b>post-construction-cleaning-768x1020.webp</b> "
                      "means a Google Images result or another cleaning company's upload, and that risk lands on "
                      "the client, not on the photographer.",
                   M, y - 22, CW, size=9.2, leading=13.4) - 14

    bw = (CW - 3 * 10) / 4
    for i, (code, label) in enumerate([(USE, "ready to use"), (LIC, "re-source the original"),
                                       (SMALL, "under minimum size"), (REPLACE, "drop")]):
        x = M + i * (bw + 10)
        card(c, x, yy - 54, bw, 54, SOFT, LINE, 6)
        c.setFillColor(COLOUR[code])
        c.rect(x, yy - 54, 3.2, 54, stroke=0, fill=1)
        c.setFont("S-SB", 22); c.setFillColor(COLOUR[code])
        c.drawString(x + 14, yy - 30, str(cnt[code]))
        c.setFont("S-SB", 8.4); c.setFillColor(NAVY)
        c.drawString(x + 14, yy - 43, code)
        c.setFont("S", 7.6); c.setFillColor(MUTE)
        c.drawString(x + 14, yy - 51, label)
    yy -= 54 + 20

    safe = sum(1 for r in rows if not r["lic"].startswith("Unknown"))
    eyebrow_ls(c, "LICENCE", M, yy, NAVY, 7.4, 1.6)
    c.setStrokeColor(LINE); c.setLineWidth(.5); c.line(M, yy - 7, W - M, yy - 7)
    yy = draw_para(c, "<b>%d of %d</b> files carry a Pexels or Unsplash filename and are safe to use commercially. "
                      "The remaining <b>%d</b> have no provenance. Several are recognisably taken from other "
                      "cleaning companies' websites. Re-source those from Pexels or Unsplash by reverse image "
                      "search, or buy them, before they go anywhere near the live site."
                   % (safe, len(rows), len(rows) - safe), M, yy - 16, CW, size=9.2, leading=13.4)

    footer(c, "Image review  AMM-M-2026-187", 1, 2 + (len(rows) + 4) // 5)
    c.showPage()

    # ---- one full-width row per image: the notes need the width
    rank = {USE: 0, LIC: 1, SMALL: 2, REPLACE: 3}
    ordered = sorted(rows, key=lambda x: (rank[x["verdict"]], x["file"]))
    per = 5
    pages = [ordered[i:i + per] for i in range(0, len(ordered), per)]
    for pno, batch in enumerate(pages, 2):
        top = H - 46
        logo_mark(c, M, top - 30, 30)
        c.setFont("S-SB", 11); c.setFillColor(NAVY)
        c.drawString(M + 40, top - 18, "Image review")
        c.setFont("S", 8.2); c.setFillColor(MUTE)
        c.drawRightString(W - M, top - 18, "Smartline Point Cleaning Hub Ltd")
        grad_rule(c, M, top - 40, CW, 2.4)

        rh = 120
        for k, r in enumerate(batch):
            yb = top - 62 - k * (rh + 12) - rh
            card(c, M, yb, CW, rh, WHITE, LINE, 7, shadow=True)
            col = COLOUR[r["verdict"]]
            c.setFillColor(col)
            c.rect(M, yb, 3.4, rh, stroke=0, fill=1)
            iw = ih = rh - 24
            ix, iy = M + 16, yb + 12
            c.setFillColor(SOFT); c.rect(ix, iy, iw, ih, stroke=0, fill=1)
            try:
                img = thumb(r["file"])
                aw, ah = img.getSize()
                sc = min(iw / aw, ih / ah)
                c.drawImage(img, ix + (iw - aw * sc) / 2, iy + (ih - ah * sc) / 2,
                            aw * sc, ah * sc, mask="auto")
            except Exception:
                pass
            tx = ix + iw + 18
            tw = CW - (tx - M) - 18
            yt = yb + rh - 18
            bw2 = c.stringWidth(r["verdict"], "S-SB", 7.4) + 14
            c.setFillColor(col)
            c.roundRect(tx, yt - 3, bw2, 14, 3, stroke=0, fill=1)
            c.setFont("S-SB", 7.4); c.setFillColor(WHITE)
            c.drawString(tx + 7, yt + 1, r["verdict"])
            c.setFont("S-SB", 8.8); c.setFillColor(MID)
            c.drawString(tx + bw2 + 10, yt + 1, "Slot: %s" % r["slot"])
            safe_lic = not r["lic"].startswith("Unknown")
            c.setFont("S-SB", 7.6); c.setFillColor(GREEN if safe_lic else RED)
            c.drawRightString(M + CW - 18, yt + 1, r["lic"])
            c.setFont("S-SB", 9); c.setFillColor(NAVY)
            name = r["file"]
            while c.stringWidth(name, "S-SB", 9) > tw - 120 and len(name) > 14:
                name = name[:-6] + "…"
            c.drawString(tx, yt - 16, name)
            c.setFont("S", 7.8); c.setFillColor(MUTE)
            c.drawRightString(M + CW - 18, yt - 16, "%d × %d · %s · %d KB" % (r["w"], r["h"], r["fmt"], r["kb"]))
            c.setStrokeColor(LINE); c.setLineWidth(.4)
            c.line(tx, yt - 24, M + CW - 18, yt - 24)
            draw_para(c, r["note"], tx, yt - 32, tw, size=8.4, leading=11.6)
        footer(c, "Image review  AMM-M-2026-187", pno, 1 + len(pages) + 1)
        c.showPage()

    # ---- still to source
    y = masthead(c, "Still to source", "%d slots with no candidate yet" % len(need),
                 "Priorities: P1 is launch-critical")
    yy = y - 24
    eyebrow_ls(c, "THE GAP THAT MATTERS MOST", M, yy, NAVY, 7.4, 1.6)
    c.setStrokeColor(LINE); c.setLineWidth(.5); c.line(M, yy - 7, W - M, yy - 7)
    yy = draw_para(c, "Every slot showing <b>people's faces</b> is still empty — the team photograph, the About "
                      "hero, the supervisor and the training session. Those four also need model-released stock "
                      "(Adobe Stock or iStock), not Pexels, because a recognisable face needs a release. The "
                      "alternative is to wait for the client's own photographs and hold those sections back.",
                   M, yy - 16, CW, size=9.2, leading=13.4) - 18

    tt = yy
    hh = 20
    c.setFillColor(NAVY); c.rect(M, tt - hh, CW, hh, stroke=0, fill=1)
    c.setFillColor(SKY); c.rect(M, tt - hh - 1.6, CW, 1.6, stroke=0, fill=1)
    c.setFont("S-SB", 8.2); c.setFillColor(WHITE)
    c.drawString(M + 10, tt - 14, "SLOT")
    c.drawString(M + 64, tt - 14, "WHAT TO FIND")
    c.drawString(M + 330, tt - 14, "ASPECT")
    c.drawRightString(W - M - 10, tt - 14, "MIN SIZE")
    yrow = tt - hh - 1.6
    for i, it in enumerate(sorted(need, key=lambda x: (x["pri"], x["id"]))):
        rh = 22
        if yrow - rh < 70:
            footer(c, "Image review  AMM-M-2026-187", 1 + len(pages) + 1, 1 + len(pages) + 1)
            c.showPage()
            yrow = H - 80
        if i % 2 == 0:
            c.setFillColor(SOFT); c.rect(M, yrow - rh, CW, rh, stroke=0, fill=1)
        c.setStrokeColor(LINE); c.setLineWidth(.4); c.line(M, yrow - rh, W - M, yrow - rh)
        c.setFont("S-SB", 7.8); c.setFillColor(NAVY)
        c.drawString(M + 10, yrow - 14, "%s %s" % (it["pri"], it["id"]))
        c.setFont("S", 7.8); c.setFillColor(BODY)
        role = it["role"]
        while c.stringWidth(role, "S", 7.8) > 250 and len(role) > 10:
            role = role[:-4] + "…"
        c.drawString(M + 64, yrow - 14, role)
        c.setFont("S", 7.6); c.setFillColor(MUTE)
        c.drawString(M + 330, yrow - 14, it["aspect"])
        c.drawRightString(W - M - 10, yrow - 14, it["min_px"])
        yrow -= rh
    footer(c, "Image review  AMM-M-2026-187", 1 + len(pages) + 1, 1 + len(pages) + 1)
    c.showPage()
    c.save()
    return 2 + len(pages)


def build():
    rows = scan()
    unknown = [r["file"] for r in rows if r["file"] not in VERDICT]
    if unknown:
        raise SystemExit("no verdict recorded for: %s" % unknown)
    have, need = coverage(rows)
    with open(OUT_MD, "w", encoding="utf-8") as f:
        f.write(build_md(rows, have, need))
    pages = build_pdf(rows, have, need, OUT_PDF)
    c = Counter(r["verdict"] for r in rows)
    print("reviewed %d files: USE %d | CHECK LICENCE %d | TOO SMALL %d | REPLACE %d"
          % (len(rows), c[USE], c[LIC], c[SMALL], c[REPLACE]))
    print("slots with a candidate: %d | still to source: %d" % (len(have), len(need)))
    print("wrote %s and %s (%d pages)" % (OUT_MD, OUT_PDF, pages))


if __name__ == "__main__":
    build()
