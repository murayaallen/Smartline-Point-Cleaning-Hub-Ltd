# -*- coding: utf-8 -*-
"""Smartline Point Cleaning Hub Ltd — media plan, single source of truth.

Every image the website needs: what to source online, what only the client can
supply (real proof), and what we produce ourselves. Checked against
site_layout.py so no image slot in the layout is left without a plan.

    python media_plan.py
        -> MEDIA.md                                   (the brief)
        -> Smartline - Image Sourcing List.xlsx       (the tracker you fill in)
        -> media/incoming/<folder>/                   (where downloads go)
"""
import os
import re
from collections import Counter, OrderedDict

import site_layout as L

KE_PEOPLE = "Black African people; Kenyan / East African setting"
AVOID = ("Third-party logos on uniforms or products; US/EU plug sockets; snow or autumn out of windows; "
         "fumigation, pest spraying or hazmat suits; sparkle effects; thumbs-up poses; watermarks")
FREE = "Pexels · Unsplash (free, commercial use)"
PAID = "Adobe Stock · iStock · Shutterstock (model-released); Pexels as fallback"

# ------------------------------------------------------------------ stock to source
# (id, priority, page, section, role, subject, must, avoid, aspect, min_px, keep_clear,
#  search_terms, where, folder, reuse_of, notes)
STOCK = [
    # ---------------- HOME
    ("IMG-H01", "P1", "Home", "H-01", "Main — hero",
     "A freshly cleaned modern open-plan office or reception: polished floor catching daylight, glass partitions, nobody in frame.",
     "Daylight; gleaming floor with depth; warm-neutral whites",
     "People; clutter; screens showing text; " + AVOID,
     "4:5 portrait", "1600 × 2000", "Bottom-left corner — the seal overlaps it",
     ["clean modern office interior", "empty office polished floor daylight", "minimal reception marble floor"],
     FREE, "home", None, "The most important image on the site. Shortlist 3–4 and we choose in the layout."),
    ("IMG-H01b", "P2", "Home", "H-01", "Main — hero alternate",
     "Same office brief with one cleaner in a plain navy uniform mid-task (mopping or wiping glass), back or three-quarter to camera.",
     KE_PEOPLE + "; plain navy or grey uniform; gloves",
     "Faces straight to camera; " + AVOID,
     "4:5 portrait", "1600 × 2000", "Bottom-left corner",
     ["african cleaner office mopping", "black woman cleaning office glass", "janitor uniform modern office"],
     PAID, "home", None, "We test H01 against H01b in the hero and keep one."),
    ("IMG-H05", "P1", "Home", "H-05", "Main — beside the six reasons",
     "A small team of 3–4 cleaners in matching plain uniforms, natural and confident, in a clean commercial interior.",
     KE_PEOPLE + "; men and women; matching uniforms; equipment in hand",
     "Arms-crossed poses; forced grins at camera; " + AVOID,
     "3:4 portrait", "1200 × 1600", "None (sits beside text)",
     ["african cleaning team uniform", "professional cleaners group", "black janitorial staff team"],
     PAID, "home", None, "Caption must not say “our team” while this is stock. Replaced by REAL-01 when it exists."),
    ("IMG-H07", "P1", "Home", "H-07", "Main — on the ink training band",
     "Careful hands: a gloved cleaner measuring or diluting a cleaning product, or putting on PPE.",
     "Gloves; labelled bottles with no brand legible; a controlled, careful action; darker tones",
     "Respirators or fogging that read as fumigation; " + AVOID,
     "3:4 portrait", "1200 × 1600", "None (sits beside text on ink)",
     ["gloved hands cleaning product", "cleaner putting on gloves", "measuring cleaning chemical"],
     FREE, "home", None, "Training is the tender argument — this image should look disciplined, not domestic."),
    ("BG-01", "P2", "Global", "G-07", "Background — CTA band on every page",
     "Abstract clean surface: light raking across a polished floor, water beading on glass, or a folded microfibre cloth on stone.",
     "Low detail; generous negative space; works under a dark overlay",
     "People; bright colours; busy texture",
     "21:9 landscape", "2400 × 1000", "Whole frame — sits under an 85% ink overlay with text",
     ["polished floor reflection abstract", "water droplets glass macro dark", "microfiber cloth texture"],
     FREE, "backgrounds", None, "Seen on every page; it must stay quiet."),

    # ---------------- ABOUT
    ("IMG-A01", "P1", "About", "A-01", "Main — page hero",
     "A cleaning crew being briefed by a supervisor in or outside a commercial building; wide.",
     KE_PEOPLE + "; uniforms; a visible supervisor figure",
     AVOID, "16:9 landscape", "1920 × 1080", "Left third if used behind the title on mobile",
     ["cleaning crew briefing", "african workers team meeting uniform", "facility services team"],
     PAID, "about", None, "Stock until REAL-01. Neutral caption: “Trained, supervised teams”."),
    ("IMG-A02", "P1", "About", "A-02", "Main — our story",
     "A supervisor with a clipboard or tablet inspecting a finished space — the “single point of contact” idea.",
     KE_PEOPLE + "; professional dress or uniform; checklist visible",
     AVOID, "4:5 portrait", "1200 × 1500", "None",
     ["supervisor inspection checklist cleaning", "facility manager clipboard office", "african woman supervisor tablet"],
     PAID, "about", None, "Replaced by REAL-02 when it exists."),
    ("IMG-A06", "P2", "About", "A-06", "Main — community and jobs",
     "A training session: a trainer demonstrating equipment to a small group of new cleaners.",
     KE_PEOPLE + "; learning in progress; hands-on",
     AVOID, "4:5 portrait", "1200 × 1500", "None",
     ["cleaning training session", "workplace training demonstration africa", "vocational training group"],
     PAID, "about", None, "Supports the job-creation line in the vision."),

    # ---------------- SERVICES HUB — one per service row
    ("IMG-S01", "P1", "Services", "S-03", "Service row — Commercial cleaning",
     "A cleaner vacuuming or mopping an open-plan office after hours.",
     "Uniform; office furniture; floor visibly cleaner where worked", AVOID,
     "4:3", "1200 × 900", "None",
     ["office cleaning vacuum", "cleaner mopping office floor", "commercial cleaning night office"],
     FREE, "services", None, "Hands, backs or faces turned away keep free stock safe."),
    ("IMG-S02", "P1", "Services", "S-03", "Service row — Office carpet cleaning",
     "A carpet extraction or shampoo machine working an office carpet, a clean stripe visible.",
     "The before/after line within one frame", AVOID,
     "4:3", "1200 × 900", "None",
     ["carpet cleaning machine office", "carpet shampoo extraction", "commercial carpet cleaning"],
     FREE, "services", None, None),
    ("IMG-S03", "P1", "Services", "S-03", "Service row — School cleaning",
     "An empty, bright classroom with neat rows of desks and a freshly cleaned floor.",
     "African school setting if one can be found", "Children's faces; " + AVOID,
     "4:3", "1200 × 900", "None",
     ["empty classroom desks africa", "clean classroom", "school hallway clean"],
     FREE, "services", None, None),
    ("IMG-S04", "P1", "Services", "S-03", "Service row — Church cleaning",
     "A bright church interior: rows of wooden pews, a clean aisle, morning light.",
     "Order and light", "People praying; a denominational symbol as the subject; " + AVOID,
     "4:3", "1200 × 900", "None",
     ["church interior pews light", "empty church aisle", "church hall clean"],
     FREE, "services", None, None),
    ("IMG-S05", "P1", "Services", "S-04", "Service row — Residential cleaning",
     "A bright, lived-in living room being dusted or vacuumed — homely, not a luxury showroom.",
     KE_PEOPLE + " if a person is shown", "Mansions; " + AVOID,
     "4:3", "1200 × 900", "None",
     ["cleaning living room vacuum", "dusting home interior", "house cleaning african woman"],
     FREE, "services", None, None),
    ("IMG-S06", "P1", "Services", "S-04", "Service row — Apartment cleaning",
     "A hotel-neat apartment bedroom: crisp white linen, folded towels — the Airbnb turnover look.",
     "White linen; tidy; daylight", AVOID,
     "4:3", "1200 × 900", "None",
     ["airbnb bedroom white linen", "apartment bedroom neat", "making bed fresh linen"],
     FREE, "services", None, None),
    ("IMG-S07", "P1", "Services", "S-04", "Service row — Move in / move out",
     "An empty apartment with a few moving boxes; a cleaner wiping a sill or cupboard.",
     "Empty rooms; boxes; cleaning in progress", AVOID,
     "4:3", "1200 × 900", "None",
     ["empty apartment moving boxes cleaning", "move out cleaning", "empty room boxes"],
     FREE, "services", None, None),
    ("IMG-S08", "P1", "Services", "S-04", "Service row — Sofa set & upholstery",
     "A fabric sofa being cleaned with an upholstery tool or brush, a stain lifting.",
     "Fabric texture; tool in contact", AVOID,
     "4:3", "1200 × 900", "None",
     ["sofa upholstery cleaning machine", "couch cleaning", "upholstery steam clean"],
     FREE, "services", None, None),
    ("IMG-S09", "P1", "Services", "S-04", "Service row — Toilet bowl & sink",
     "A gleaming white sink and chrome tap, a gloved hand finishing a wipe. Tasteful — no toilet close-up.",
     "Shine on chrome; white ceramic", "Grime close-ups; dirty toilets; " + AVOID,
     "4:3", "1200 × 900", "None",
     ["clean bathroom sink chrome", "gloved hand cleaning sink", "white bathroom clean"],
     FREE, "services", None, None),
    ("IMG-S10", "P1", "Services", "S-05", "Service row — Post-construction",
     "A newly finished interior with builders' dust; a cleaner wiping a window frame; ladder or tape still visible.",
     "Evidence of building work; cleaning in progress", AVOID,
     "4:3", "1200 × 900", "None",
     ["post construction cleaning", "new building interior dust cleaning", "cleaning after renovation"],
     FREE, "services", None, None),
    ("IMG-S11", "P1", "Services", "S-05", "Service row — Deep cleaning",
     "Detail work: scrubbing tile grout, or inside an oven or under a fridge.",
     "Close detail; a brush in contact", "Disgusting grime; " + AVOID,
     "4:3", "1200 × 900", "None",
     ["scrubbing grout brush", "deep cleaning kitchen oven", "cleaning tile grout"],
     FREE, "services", None, None),
    ("IMG-S12", "P1", "Services", "S-05", "Service row — One-time cleaning",
     "A cleaning caddy with tools and cloths set down at a doorway — ready to start.",
     "Neat kit; a threshold", AVOID,
     "4:3", "1200 × 900", "None",
     ["cleaning supplies caddy", "cleaning kit bucket doorway", "cleaning tools basket"],
     FREE, "services", None, None),
    ("IMG-S13", "P1", "Services", "S-06", "Service row — Landscaping",
     "A trimmed lawn, clipped hedges and a swept compound under clear sky; tropical or highland planting.",
     "Kenyan vegetation; a compound or estate", "Snow; autumn leaves; temperate suburbia; " + AVOID,
     "4:3", "1200 × 900", "None",
     ["landscaping lawn mowing africa", "trimmed hedge garden compound", "gardener hedge trimming"],
     FREE, "services", None, None),

    # ---------------- SERVICE PAGE HEROES
    ("IMG-D01", "P1", "Commercial cleaning", "CC-01", "Main — page hero",
     "A team cleaning a glass-walled boardroom or a bank hall — wider and more polished than IMG-S01.",
     KE_PEOPLE + "; two or more cleaners; glass and hard floors", AVOID,
     "4:3", "1600 × 1200", "None (split layout)",
     ["cleaning glass office boardroom", "janitorial team office", "bank interior clean"],
     PAID, "service-pages", None, None),
    ("IMG-D02", "P1", "Homes & apartments", "RA-01", "Main — page hero",
     "A cleaner in an apartment kitchen wiping a counter, morning light; warm and homely.",
     KE_PEOPLE + "; a real-looking Nairobi apartment", AVOID,
     "4:3", "1600 × 1200", "None (split layout)",
     ["cleaner kitchen counter apartment", "home cleaning service kitchen", "african cleaner kitchen"],
     PAID, "service-pages", None, None),
    ("IMG-D03", "P1", "Post-construction", "PC-01", "Main — page hero",
     "A wide, newly built interior being cleaned for handover: dust, ladders, protective film coming off.",
     "Scale; the moment before handover", AVOID,
     "4:3", "1600 × 1200", "None (split layout)",
     ["construction cleanup interior", "new apartment handover cleaning", "builders clean dust"],
     FREE, "service-pages", None, None),

    # ---------------- CLIENTS — stock fallback for the gallery only
    ("IMG-C01", "P2", "Clients", "C-05", "Gallery fallback — Offices", "Reuse IMG-D01.", "", "", "4:3", "—", "None",
     [], "—", "clients", "IMG-D01", None),
    ("IMG-C02", "P2", "Clients", "C-05", "Gallery fallback — Banking",
     "A clean banking hall: polished floor, counters, no customers, no bank branding.",
     "Marble or terrazzo; order", "Bank logos; customers' faces; " + AVOID,
     "4:3", "1200 × 900", "None",
     ["bank interior empty", "banking hall marble floor", "bank lobby clean"],
     FREE, "clients", None, None),
    ("IMG-C03", "P2", "Clients", "C-05", "Gallery fallback — Education", "Reuse IMG-S03.", "", "", "4:3", "—", "None",
     [], "—", "clients", "IMG-S03", None),
    ("IMG-C04", "P2", "Clients", "C-05", "Gallery fallback — Churches", "Reuse IMG-S04.", "", "", "4:3", "—", "None",
     [], "—", "clients", "IMG-S04", None),
    ("IMG-C05", "P2", "Clients", "C-05", "Gallery fallback — Residential complexes",
     "A mid-rise apartment block or its clean common stairwell — Nairobi-style architecture.",
     "Kenyan apartment architecture", AVOID,
     "4:3", "1200 × 900", "None",
     ["nairobi apartment building", "apartment block stairwell clean", "residential building africa"],
     FREE, "clients", None, None),
    ("IMG-C06", "P2", "Clients", "C-05", "Gallery fallback — Short-stay", "Reuse IMG-S06.", "", "", "4:3", "—", "None",
     [], "—", "clients", "IMG-S06", None),
    ("IMG-C07", "P2", "Clients", "C-05", "Gallery fallback — Hospitality",
     "A lounge or bar before opening: chairs up, floor clean, soft light.",
     "Order before service", "Drinking customers; liquor brands; " + AVOID,
     "4:3", "1200 × 900", "None",
     ["empty lounge interior", "bar before opening chairs", "restaurant interior clean empty"],
     FREE, "clients", None, None),
    ("IMG-C08", "P2", "Clients", "C-05", "Gallery fallback — Construction", "Reuse IMG-D03.", "", "", "4:3", "—", "None",
     [], "—", "clients", "IMG-D03", None),
    ("IMG-C09", "P2", "Clients", "C-05", "Gallery fallback — Compounds", "Reuse IMG-S13.", "", "", "4:3", "—", "None",
     [], "—", "clients", "IMG-S13", None),

    # ---------------- UTILITY + QUIET BACKGROUNDS
    ("IMG-N01", "P3", "404", "N-01", "Main — 404 page",
     "A single mop leaning against a clean white wall — quiet, a little wry.",
     "Minimal; lots of wall", AVOID,
     "4:3", "1200 × 900", "Right half",
     ["mop against wall minimal", "cleaning mop white wall", "minimal cleaning still life"],
     FREE, "utility", None, "Optional."),
    ("BG-02", "P3", "Global", "S-01", "Background — compact page heroes (Services, Clients, Contact)",
     "A very subtle architectural surface: light terrazzo, limestone or soft-focus clean interior lines.",
     "Pale; almost no contrast", "Anything that competes with the title",
     "21:9 landscape", "2400 × 1000", "Whole frame — sits under a 90% paper overlay",
     ["terrazzo texture light", "limestone surface texture", "minimal architecture lines soft"],
     FREE, "backgrounds", None, "Optional — adds depth to the three pages without a hero photo."),
]

# ------------------------------------------------------------------ real photos only the client can supply
REAL = [
    ("REAL-01", "Team photograph", "Home H-05, About A-01",
     "The whole team in uniform at the office or on a site. Replaces stock IMG-H05 and IMG-A01.",
     "Daylight; everyone in uniform; landscape and portrait versions"),
    ("REAL-02", "Supervisor at work", "About A-02",
     "A named supervisor inspecting a finished job. Replaces stock IMG-A02.", "Natural, not posed"),
    ("REAL-03", "Before / after — commercial (2 pairs)", "Commercial cleaning CC-05",
     "Office floor and washroom, each shot before and after the clean.",
     "Same spot, same angle, same light — phone on the same mark"),
    ("REAL-04", "Before / after — homes (2 pairs)", "Homes & apartments RA-05",
     "Sofa set and bathroom, before and after.", "Same spot, same angle, same light"),
    ("REAL-05", "Before / after — post-construction (2 pairs)", "Post-construction PC-05",
     "Before handover and the floor finish.", "Same spot, same angle, same light"),
    ("REAL-06", "Job gallery (9–12)", "Clients C-05 “The work”",
     "Real jobs across sectors. Until they exist the section runs as “Spaces we look after” using IMG-C01…C09.",
     "Landscape and portrait mix; no client faces without consent"),
    ("REAL-07", "Google Business Profile set (10+)", "Google Business Profile",
     "Logo, cover, office exterior or signage, interior, team, and at least five at-work shots. Google removes stock photos from profiles.",
     "Real premises and people only"),
    ("REAL-08", "Client logos", "Home H-02, Clients C-02",
     "Logo files from clients who give written permission to be named.", "SVG or large PNG"),
]

# ------------------------------------------------------------------ we produce (not sourced)
PRODUCE = [
    ("Logo set", "Chosen round-2 concept drawn to final vector: SVG, PDF, PNG; colour, one-colour, reversed",
     "After the client picks 01–06"),
    ("Favicon and app icons", "favicon.svg, 32, 180 (Apple), 192 and 512 (Android) from the mark", "With the logo"),
    ("Clean Quality Guaranteed seal", "Vector seal in ink and brass for the hero and the profile", "Build week 1"),
    ("Icons (≈ 20)", "Lucide line icons (ISC licence), 1.5px stroke, brass on paper, ink on brass: the six reasons, "
     "six training areas, phone, WhatsApp, email, location, clock, calendar, check, arrow", "Build week 1"),
    ("Map", "Static map of ICIPE Road, Kasarani drawn from OpenStreetMap data in brand colours, with the "
     "© OpenStreetMap contributors credit; links to Google Maps", "Build week 1"),
    ("Open Graph share images (8)", "1200 × 630, one per content page, from a brand template over a sourced photo", "Before launch"),
    ("Social launch pack (6 posts)", "From the sourced set: 1 We are live (IMG-H01) · 2 services carousel (S01, S05, S10, S13) · "
     "3 post-construction (IMG-D03) · 4 trained cleaners (IMG-H07) · 5 who we clean for (typographic) · 6 Book your clean (IMG-D02)",
     "Launch week"),
    ("Company profile reprint", "Redesigned with the round-2 identity and the new domain; uses the sourced and real sets", "Before launch"),
]

ART_DIRECTION = OrderedDict([
    ("People", [
        "Black African people in every frame that shows people; men and women; Kenyan or East African settings where possible.",
        "Plain navy, charcoal or grey uniforms. No third-party logos on clothing, equipment or bottles.",
        "Gloves when cleaning. Faces turned to the task, not grinning at the lens.",
    ]),
    ("Places", [
        "Realistic Nairobi offices, apartments, schools and churches — not US suburban houses, not luxury mansions.",
        "Check the background: UK-style three-pin sockets (Kenya uses type G), right-hand-drive vehicles, tropical or highland planting, no snow, no autumn.",
    ]),
    ("Light and colour", [
        "Natural daylight, clean warm-neutral whites. No blue clinical cast, no heavy HDR.",
        "Mixed sources are fine: we grade the whole set in one pass (slight warmth, saturation −10, highlights held) so it reads as one shoot.",
    ]),
    ("Composition", [
        "Real negative space wherever text sits — the “Keep clear” column says where.",
        "Download the largest size available; we crop, grade and export WebP with srcset at build.",
    ]),
    ("Avoid", [
        "Fumigation, pest spraying, fogging, hazmat suits — the service is not licensed and the site does not offer it.",
        "Sparkle graphics, thumbs-up, gloves thrust at the camera, cartoon or illustration, AI-generated people (check the hands), watermarked previews.",
    ]),
    ("Licensing", [
        "Pexels and Unsplash allow free commercial use without attribution but give no model releases: fine for spaces, objects, hands and backs.",
        "For recognisable faces in the hero, team and About slots, use model-released stock (Adobe Stock, iStock, Shutterstock).",
        "Never Google Images, Pinterest, Facebook, or a competitor's website.",
        "Record the source URL, photographer and licence for every image in the tracker — that column is the proof of licence if anyone asks.",
    ]),
    ("Honesty", [
        "Stock is illustration, never evidence. No stock image is captioned as a Smartline job, team member or client.",
        "No stock faces on testimonials — testimonials run as text with name and title.",
        "The before/after sliders stay hidden until REAL-03 to REAL-05 exist. The gallery runs as “Spaces we look after” until REAL-06 exists.",
    ]),
])

FOLDERS = ["home", "about", "services", "service-pages", "clients", "backgrounds", "utility"]


# ================================================================== helpers
def items():
    keys = ["id", "pri", "page", "section", "role", "subject", "must", "avoid", "aspect", "min_px",
            "keep_clear", "terms", "where", "folder", "reuse_of", "notes"]
    return [dict(zip(keys, row)) for row in STOCK]


def save_as(it):
    if it["reuse_of"]:
        return "(reuse %s)" % it["reuse_of"]
    words = (it["page"] + " " + it["role"].split("—")[-1]).lower()
    for ch in "&/,()":
        words = words.replace(ch, " ")
    seen, out = set(), []
    for w in words.split():
        if w not in seen:
            seen.add(w)
            out.append(w)
    return "%s_%s.jpg" % (it["id"], "-".join(out)[:48].rstrip("-"))


def by_section():
    m = OrderedDict()
    for it in items():
        m.setdefault(it["section"], []).append(it["id"])
    for rid, name, where, _, _ in REAL:
        for sec in re.findall(r"\b[A-Z]{1,2}-\d{2}\b", where):
            m.setdefault(sec, []).append(rid)
    return m


def image_slots():
    """section ids in site_layout that draw a photograph placeholder"""
    slots = []
    for pg in L.PAGES:
        for s in pg["sections"]:
            t, p = s["type"], s["p"]
            if t in ("hero_split", "split_media", "service_rows", "gallery", "beforeafter"):
                slots.append(s["id"])
            elif t in ("page_hero", "icon_grid", "band") and p.get("image"):
                slots.append(s["id"])
    return slots


def verify():
    errs = []
    its = items()
    ids = [i["id"] for i in its] + [r[0] for r in REAL]
    if len(ids) != len(set(ids)):
        errs.append("duplicate ids: %s" % [k for k, v in Counter(ids).items() if v > 1])
    names = [save_as(i) for i in its if not i["reuse_of"]]
    if len(names) != len(set(names)):
        errs.append("duplicate save-as filenames")
    known = {i["id"] for i in its}
    for i in its:
        if i["reuse_of"] and i["reuse_of"] not in known:
            errs.append("%s reuses unknown %s" % (i["id"], i["reuse_of"]))
        if not i["reuse_of"]:
            if len(i["terms"]) < 3:
                errs.append("%s needs three search terms" % i["id"])
            if i["folder"] not in FOLDERS:
                errs.append("%s has unknown folder %s" % (i["id"], i["folder"]))
        if i["pri"] not in ("P1", "P2", "P3"):
            errs.append("%s bad priority" % i["id"])
    covered = by_section()
    for sid in image_slots():
        if sid not in covered:
            errs.append("layout image slot %s has no media planned" % sid)
    # every service row has its own photograph
    rows = [i for i in its if i["role"].startswith("Service row")]
    n_services = sum(len(x) for _, _, x in L.GROUPS)
    if len(rows) != n_services:
        errs.append("service rows: %d images for %d services" % (len(rows), n_services))
    blob = " ".join(str(v) for i in its for v in (i["subject"], i["terms"])).lower()
    if "fumigat" in blob.replace("fumigation, pest spraying", ""):
        errs.append("fumigation in a sourcing brief")
    if errs:
        raise SystemExit("media verify() FAILED:\n  - " + "\n  - ".join(errs))
    return its


# ================================================================== MEDIA.md
def build_md(its):
    to_source = [i for i in its if not i["reuse_of"]]
    pri = Counter(i["pri"] for i in to_source)
    o = ["# Smartline Point Cleaning Hub Ltd — media plan\n",
         "Generated from `media_plan.py`. The tracker is **`Smartline - Image Sourcing List.xlsx`** — "
         "fill in status, source URL, photographer and licence there as you go.\n",
         "**To source online: %d images** — %d launch-critical (P1), %d strongly wanted (P2), %d optional (P3). "
         "Plus %d reuses, %d real-photo items only the client can supply, and %d things we produce ourselves.\n"
         % (len(to_source), pri["P1"], pri["P2"], pri["P3"], len(its) - len(to_source), len(REAL), len(PRODUCE)),
         "Save each download as the **Save as** name into `media/incoming/<folder>/`.\n"]

    o.append("## Art direction — read before searching\n")
    for head, rules in ART_DIRECTION.items():
        o.append("**%s**\n" % head)
        o.extend("- %s" % r for r in rules)
        o.append("")

    order = OrderedDict()
    for i in its:
        order.setdefault(i["page"], []).append(i)
    o.append("## Images to source, by page\n")
    for page, group in order.items():
        o.append("### %s\n" % page)
        for i in group:
            if i["reuse_of"]:
                o.append("- [ ] **%s** · %s · %s — *reuse %s, nothing to source*" %
                         (i["id"], i["pri"], i["role"], i["reuse_of"]))
                continue
            o.append("- [ ] **%s** · %s · %s · `%s` · %s, min %s" %
                     (i["id"], i["pri"], i["role"], i["section"], i["aspect"], i["min_px"]))
            o.append("  - **Find:** %s" % i["subject"])
            if i["must"]:
                o.append("  - **Must show:** %s" % i["must"])
            o.append("  - **Search:** %s  ·  **Where:** %s" % (" · ".join("“%s”" % t for t in i["terms"]), i["where"]))
            if i["keep_clear"] and i["keep_clear"] != "None":
                o.append("  - **Keep clear for text:** %s" % i["keep_clear"])
            if i["notes"]:
                o.append("  - **Note:** %s" % i["notes"])
            o.append("  - **Save as:** `media/incoming/%s/%s`" % (i["folder"], save_as(i)))
        o.append("")

    o.append("## Real photographs — only the client can supply\n")
    o.append("These are proof. Stock cannot stand in for them.\n")
    for rid, name, where, what, how in REAL:
        o.append("- [ ] **%s · %s** (%s) — %s *%s.*" % (rid, name, where, what, how))
    o.append("\nSave to `media/real/` as they arrive.\n")

    o.append("## We produce — not sourced\n")
    o.append("| Asset | What | When |\n|---|---|---|")
    for a, w, when in PRODUCE:
        o.append("| %s | %s | %s |" % (a, w, when))
    o.append("")
    return "\n".join(o) + "\n"


# ================================================================== XLSX tracker
def build_xlsx(its, path):
    from openpyxl import Workbook
    from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
    from openpyxl.formatting.rule import FormulaRule
    from openpyxl.worksheet.datavalidation import DataValidation
    from openpyxl.utils import get_column_letter

    INK, BRASS, PAPER, STONE = "0E1430", "B8862F", "FAF8F4", "E7E3DA"
    head_font = Font(name="Calibri", bold=True, color="FFFFFF", size=10)
    head_fill = PatternFill("solid", fgColor=INK)
    gold = Side(style="medium", color=BRASS)
    hair = Side(style="thin", color=STONE)
    zebra = PatternFill("solid", fgColor=PAPER)
    wrap = Alignment(wrap_text=True, vertical="top")
    body = Font(name="Calibri", size=10)

    def header(ws, cols, widths, row=1):
        for c, (name, w) in enumerate(zip(cols, widths), 1):
            cell = ws.cell(row=row, column=c, value=name)
            cell.font, cell.fill = head_font, head_fill
            cell.alignment = Alignment(wrap_text=True, vertical="center")
            cell.border = Border(bottom=gold)
            ws.column_dimensions[get_column_letter(c)].width = w
        ws.row_dimensions[row].height = 30
        ws.freeze_panes = ws.cell(row=row + 1, column=3)

    def body_rows(ws, rows, start=2):
        for r, vals in enumerate(rows, start):
            for c, v in enumerate(vals, 1):
                cell = ws.cell(row=r, column=c, value=v)
                cell.alignment, cell.font = wrap, body
                cell.border = Border(bottom=hair)
                if (r - start) % 2:
                    cell.fill = zebra

    wb = Workbook()

    # ---- sheet 1: source list
    ws = wb.active
    ws.title = "Source list"
    cols = ["#", "ID", "Priority", "Page", "Section", "Role", "Find — subject", "Must show", "Avoid",
            "Aspect", "Min size (px)", "Keep clear for text", "Search terms", "Where to look", "Save as",
            "Folder", "Status", "Source URL", "Photographer", "Licence", "Notes"]
    widths = [4, 10, 8, 14, 8, 26, 46, 30, 34, 11, 13, 22, 34, 26, 34, 13, 13, 34, 18, 16, 30]
    header(ws, cols, widths)
    order = {"P1": 0, "P2": 1, "P3": 2}
    rows = []
    for n, i in enumerate(sorted(its, key=lambda x: (order[x["pri"]], x["id"])), 1):
        reuse = bool(i["reuse_of"])
        rows.append([n, i["id"], i["pri"], i["page"], i["section"], i["role"], i["subject"], i["must"],
                     i["avoid"], i["aspect"], i["min_px"], i["keep_clear"], "\n".join(i["terms"]), i["where"],
                     save_as(i), "media/incoming/" + i["folder"], "Reuse" if reuse else "To source",
                     "", "", "", i["notes"] or ""])
    body_rows(ws, rows)
    last = len(rows) + 1
    dv = DataValidation(type="list", formula1='"To source,Shortlisted,Downloaded,Approved,Rejected,Reuse"',
                        allow_blank=False)
    ws.add_data_validation(dv)
    dv.add("Q2:Q%d" % last)
    lic = DataValidation(type="list", formula1='"Pexels,Unsplash,Adobe Stock,iStock,Shutterstock,Other (note it)"',
                         allow_blank=True)
    ws.add_data_validation(lic)
    lic.add("T2:T%d" % last)
    rng = "A2:U%d" % last
    for status, colour in (("Approved", "DCEFD9"), ("Downloaded", "E3ECF7"), ("Shortlisted", "FBF1DC"),
                           ("Rejected", "F6DADA"), ("Reuse", "EEEEEE")):
        ws.conditional_formatting.add(rng, FormulaRule(formula=['$Q2="%s"' % status],
                                                       fill=PatternFill("solid", fgColor=colour)))
    ws.conditional_formatting.add("C2:C%d" % last, FormulaRule(formula=['$C2="P1"'],
                                  font=Font(bold=True, color=BRASS)))
    ws.auto_filter.ref = "A1:U%d" % last

    # ---- sheet 2: real photos
    wr = wb.create_sheet("Real photos (client)")
    header(wr, ["ID", "What", "Used in", "Brief", "How to shoot", "Status", "Received"], [10, 30, 26, 60, 40, 14, 14])
    body_rows(wr, [[r[0], r[1], r[2], r[3], r[4], "Requested", ""] for r in REAL])
    dv2 = DataValidation(type="list", formula1='"Requested,Received,Approved,Not available"')
    wr.add_data_validation(dv2)
    dv2.add("F2:F%d" % (len(REAL) + 1))

    # ---- sheet 3: we produce
    wp = wb.create_sheet("We produce")
    header(wp, ["Asset", "What", "When", "Status"], [28, 90, 22, 14])
    body_rows(wp, [[a, w, when, "Not started"] for a, w, when in PRODUCE])

    # ---- sheet 4: art direction
    wa = wb.create_sheet("Art direction")
    header(wa, ["Topic", "Rule"], [18, 120])
    ad_rows = [[head, rule] for head, rules in ART_DIRECTION.items() for rule in rules]
    body_rows(wa, ad_rows)

    # ---- sheet 5: summary (live formulas)
    sm = wb.create_sheet("Summary", 0)
    sm.column_dimensions["A"].width = 34
    sm.column_dimensions["B"].width = 14
    sm.column_dimensions["C"].width = 14
    sm["A1"] = "Smartline Point Cleaning Hub — image sourcing"
    sm["A1"].font = Font(name="Calibri", bold=True, size=14, color=INK)
    sm["A2"] = "Counts update as you change Status on the Source list."
    sm["A2"].font = Font(name="Calibri", italic=True, size=10, color="5F5B55")
    S = "'Source list'!"
    lines = [
        ("Images to source (excluding reuses)", '=COUNTIF(%sQ2:Q%d,"<>Reuse")' % (S, last)),
        ("  P1 — launch-critical", '=COUNTIFS(%sC2:C%d,"P1",%sQ2:Q%d,"<>Reuse")' % (S, last, S, last)),
        ("  P2 — strongly wanted", '=COUNTIFS(%sC2:C%d,"P2",%sQ2:Q%d,"<>Reuse")' % (S, last, S, last)),
        ("  P3 — optional", '=COUNTIFS(%sC2:C%d,"P3",%sQ2:Q%d,"<>Reuse")' % (S, last, S, last)),
        ("Approved", '=COUNTIF(%sQ2:Q%d,"Approved")' % (S, last)),
        ("Downloaded, awaiting approval", '=COUNTIF(%sQ2:Q%d,"Downloaded")' % (S, last)),
        ("Shortlisted", '=COUNTIF(%sQ2:Q%d,"Shortlisted")' % (S, last)),
        ("Still to source", '=COUNTIF(%sQ2:Q%d,"To source")' % (S, last)),
        ("P1 approved", '=COUNTIFS(%sC2:C%d,"P1",%sQ2:Q%d,"Approved")' % (S, last, S, last)),
        ("P1 progress", "=IF(B5=0,0,B12/B5)"),
        ("Approved without a licence recorded", '=COUNTIFS(%sQ2:Q%d,"Approved",%sT2:T%d,"")' % (S, last, S, last)),
        ("Real photos requested from the client", "=COUNTA('Real photos (client)'!A2:A%d)" % (len(REAL) + 1)),
    ]
    for r, (label, f) in enumerate(lines, 4):
        sm.cell(row=r, column=1, value=label).font = Font(name="Calibri", size=11, bold=not label.startswith("  "))
        c = sm.cell(row=r, column=2, value=f)
        c.font = Font(name="Calibri", size=11, bold=True, color=INK)
        c.border = Border(bottom=hair)
    sm["B13"].number_format = "0%"
    sm["A16"] = "Launch rule: every P1 approved, and the licence column filled for every approved image."
    sm["A16"].font = Font(name="Calibri", size=10, color=BRASS, bold=True)
    for ws_ in wb.worksheets:
        ws_.sheet_view.showGridLines = False
        ws_.page_setup.orientation = "landscape"
        ws_.page_setup.fitToWidth = 1
    wb.save(path)
    return last - 1, lines


def make_folders():
    for f in FOLDERS:
        d = os.path.join("media", "incoming", f)
        os.makedirs(d, exist_ok=True)
        keep = os.path.join(d, ".gitkeep")
        if not os.path.exists(keep):
            open(keep, "w").close()
    real = os.path.join("media", "real")
    os.makedirs(real, exist_ok=True)
    if not os.path.exists(os.path.join(real, ".gitkeep")):
        open(os.path.join(real, ".gitkeep"), "w").close()


def build():
    its = verify()
    md = build_md(its)
    with open("MEDIA.md", "w", encoding="utf-8") as f:
        f.write(md)
    xlsx = "Smartline - Image Sourcing List.xlsx"
    n_rows, _ = build_xlsx(its, xlsx)
    make_folders()
    to_source = [i for i in its if not i["reuse_of"]]
    pri = Counter(i["pri"] for i in to_source)
    print("media verify OK: %d layout image slots covered" % len(image_slots()))
    print("to source: %d (P1 %d, P2 %d, P3 %d) + %d reuses | real-only %d | we produce %d"
          % (len(to_source), pri["P1"], pri["P2"], pri["P3"], len(its) - len(to_source), len(REAL), len(PRODUCE)))
    print("wrote MEDIA.md, %s (%d rows), media/incoming/{%s}, media/real" % (xlsx, n_rows, ",".join(FOLDERS)))


if __name__ == "__main__":
    build()
