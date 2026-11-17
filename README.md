# Smartline Point Cleaning Hub Ltd

Client project: website, brand identity and sales documents for Smartline Point
Cleaning Hub Ltd (Nairobi) — commercial, residential and post-construction
cleaning, and landscaping, trading since 2018.

Domain chosen by the client: **smartlinepointcleaning.co.ke**

## What is here

| File | What it is |
|---|---|
| `CLAUDE.md` | Project memory — settled figures, settled wording, decisions not to re-open |
| `PLAN.md` | Website plan: domain, sitemap, services, design direction, build spec, timeline |
| `brandkit.py` | Shared ReportLab house style for every client document |
| `make_quotation.py` | 2-page quotation (single source of truth for the figures, `verify()` on import) |
| `make_choices.py` | One-page client tick-sheet: domain options and build decisions |
| `logo_premium.py` | Logo system round 2 — six vector marks, Bodoni + Copperplate, brass on ink |
| `make_logo_premium.py` | 6-page logo presentation built from those marks |
| `site_layout.py` | **Website layout, single source of truth** — pages, sections, copy, SEO, design system |
| `make_layout.py` | Renders it to `LAYOUT.md` (spec) and `wireframes.html` (clickable wireframe); `verify()` gates the build |
| `media_plan.py` | **Media plan** — every image to source, with art direction; renders `MEDIA.md` and the XLSX tracker |
| `review_media.py` | Verdict on each supplied image; renders `MEDIA-REVIEW.md` and the review PDF |
| `logo_concepts.py` | Round 1, rejected. Kept for the record; archived output in `logo/_round1_rejected/` |

## Running

Plain `python`, not `python -I` — the scripts import `brandkit` from this folder.

```bash
python make_quotation.py        # quotation PDF
python make_choices.py          # domain / decisions sheet
python make_logo_premium.py     # logo concept deck
python make_layout.py           # LAYOUT.md + wireframes.html
python media_plan.py            # MEDIA.md + image sourcing tracker
python review_media.py          # review whatever is in media/all
```

Fonts are loaded from `C:/Windows/Fonts` (Segoe UI, Bodoni MT, Copperplate Gothic).

## Status

Quote accepted. Domain chosen (smartlinepointcleaning.co.ke). Logo concepts rev B with the client.
Website layout planned and verified — open `wireframes.html`. Build next.
