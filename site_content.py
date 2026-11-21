# -*- coding: utf-8 -*-
"""Smartline Point Cleaning Hub Ltd — website content that the layout data does
not carry: configuration, FAQ answers, long copy, image crops and alt text.

site_layout.py   = structure + short copy (the plan)
site_content.py  = everything else the live site needs (this file)
build_site.py    = renders both into site/ and refuses to write a broken page

Rules this file keeps (CLAUDE.md):
  * nothing invented that a customer could rely on — no hours, no prices, no
    certificates we have not seen. Where the client has not decided, the copy is
    written so it is true today, and CLIENT-REVIEW.md lists what to confirm.
  * stock is illustration, never evidence: captions never say "our team".
  * no testimonials. The named clients carry the proof.
"""

# ------------------------------------------------------------------ configuration
DOMAIN = "smartlinepointcleaning.co.ke"
ORIGIN = "https://" + DOMAIN
BRAND = "Smartline Point Cleaning Hub Ltd"
SHORT = "Smartline"
PHONE = "+254 711 128736"
PHONE_E164 = "+254711128736"
WA = "254711128736"                       # wa.me format: no plus, no spaces
EMAIL = "info@" + DOMAIN
CAREERS_EMAIL = "operations@" + DOMAIN
STREET = "ICIPE Road, Sports Drive, Suite 8"
LOCALITY = "Kasarani, Nairobi"
POSTAL = "P.O. Box 48018-00100, Nairobi"
FOUNDED = "2018"
AREAS = ["Nairobi", "Kiambu"]
LAST_UPDATED = "20/11/2026"
YEAR = "2026"

# The logo is still the client's pick from the round-2 deck. The Stamp is used
# provisionally because it is the one that stays legible at 32px in a header and
# as a favicon. Change this one word and rebuild to swap every instance.
LOGO_CONCEPT = "original"       # the client's own logo, lifted from smart.pdf (Allen 20/11/2026)
                                # round-2 concepts still selectable: seal | plate | letter | cipher | droplet | stamp

# Google Analytics 4 measurement ID. None = no analytics, and therefore no cookie
# banner: there is nothing to consent to. Set it ("G-XXXXXXX") and rebuild — the
# consent bar and the deferred loader switch on together.
GA_ID = None

# Guide prices (S-07). None = the section explains how pricing works without
# figures. Give it numbers and the same cards show "From KES ..." instead.
#   PRICES = {"visit": "4,500", "month": "18,000", "sqm": "45"}
PRICES = None

MAP_URL = "https://www.google.com/maps/search/?api=1&query=ICIPE+Road+Sports+Drive+Kasarani+Nairobi"
WA_TEXT = "Hello Smartline, I'd like a quote for "


def wa_link(service=""):
    from urllib.parse import quote
    text = WA_TEXT + (service.lower() if service else "cleaning") + "."
    return "https://wa.me/%s?text=%s" % (WA, quote(text))


# ------------------------------------------------------------------ FAQ answers
# Conservative by design: true today, no commitment the client has not made.
# Every one of these is listed in CLIENT-REVIEW.md for sign-off before launch.
FAQ = {
    "Do you bring your own equipment and chemicals?":
        "Yes. Our teams arrive equipped with the machines, tools and cleaning products the job needs, and every "
        "cleaner is trained in correct dilution and safe handling. If your premises have products you prefer, tell "
        "us and we will work with them.",
    "Do you charge for a site visit?":
        "For contract work and larger jobs we see the space before we price it, so the quote matches the real "
        "premises. For smaller one-off cleans we can often quote from a few photographs sent on WhatsApp. We tell "
        "you which applies on the first call, before any cost is involved.",
    "Can you clean outside working hours?":
        "Yes. Early mornings, evenings and weekends are routine for offices, schools and churches. Cleaning should "
        "fit around your work, not interrupt it.",
    "Are your cleaners vetted?":
        "Every cleaner is trained before placement — communication, equipment use, chemical handling, grooming "
        "and PPE, teamwork and our code of conduct — and works under a named supervisor who is accountable for "
        "your site.",
    "Which areas do you cover?":
        "We are based in Kasarani and work across Nairobi and Kiambu, including Roysambu, Ruiru, Thika Road, the "
        "CBD and Westlands. Outside those areas, ask: for contract work we often can.",
    # commercial
    "Can you clean outside office hours?":
        "Yes. Most offices are cleaned early in the morning or after close so your people never work around a mop. "
        "Banks, schools and churches get a schedule built around their own hours.",
    "Do you supply equipment and chemicals?":
        "Yes — machines, tools and products suited to your floors and surfaces, handled by cleaners trained in "
        "correct dilution and storage. Consumables such as soap and tissue can be supplied or restocked from yours.",
    "Can the same cleaners stay on our site?":
        "Yes, and that is the point. Your site keeps the same team wherever possible, under one named supervisor, "
        "so the people cleaning learn how your premises run.",
    "What happens if a cleaner is absent?":
        "The supervisor arranges cover from the trained team so the agreed scope is still delivered. Cover is our "
        "problem to solve, not yours to chase.",
    # homes & apartments
    "Do I need to be home?":
        "Not necessarily. Many clients leave a key or arrange access with the caretaker, and we agree how access "
        "works when you book. For a first clean we suggest being there for the walk-through at the end.",
    "Do you do Airbnb turnovers between guests?":
        "Yes. Linen changed on request, bathrooms and kitchen reset, the unit made ready for the next check-in — "
        "scheduled around your bookings.",
    "Can you clean sofas on site?":
        "Yes. Sofa sets, chairs and upholstery are cleaned in place: stains pre-treated, fabric shampooed, cushions "
        "and crevices done. Drying time depends on the fabric, and we tell you before we start.",
    "How long does a move-out clean take?":
        "It depends on the size of the home and the state it is in, so we confirm the time when we scope the job. "
        "Tell us your handover date and we plan to it.",
    # post-construction
    "When in the build should we book?":
        "As soon as you know your handover date. The clean is phased — a rough clean once the trades finish, a "
        "final clean before handover, a touch-up after snagging — so the earlier we see the site, the better the plan.",
    "Do you remove construction debris?":
        "Yes. Debris from the clean is cleared, bagged and removed from site. For large volumes of rubble we agree "
        "the arrangement when we scope the job.",
    "Can you work to a handover date?":
        "Yes. We work back from your date and phase the rough clean, final clean and touch-up so the space is ready "
        "when the keys change hands.",
    "Do you clean occupied buildings after renovation?":
        "Yes. Offices and homes that stay in use during works get the same post-construction clean, scheduled around "
        "the people using them.",
    # contact
    "How fast will you reply?":
        "Within one working day, and usually sooner. If it is urgent, call or WhatsApp " + PHONE + ".",
    "Is the site visit free?":
        "We see the space before we price contract and larger jobs; smaller one-off cleans can often be quoted from "
        "photographs. We tell you which applies on the first call, before any cost is involved.",
    "Do you bring equipment and chemicals?":
        "Yes — the team arrives equipped, and every cleaner is trained in safe handling and correct dilution.",
}

# ------------------------------------------------------------------ long copy
SERVICE_INTRO = {
    "/commercial-cleaning": [
        "A clean office is noticed only when it is not. Smartline runs scheduled cleaning for offices, banks, schools, "
        "churches and commercial complexes across Nairobi — daily, weekly or on a programme — with a trained "
        "team and a named supervisor who knows your premises.",
        "We learn how your building runs before we clean it: when people arrive, which areas carry the most traffic, "
        "what your staff and visitors expect. The scope is agreed in writing, checked on every visit and reviewed "
        "monthly, so the standard holds long after the first week.",
    ],
    "/residential-apartment-cleaning": [
        "Your home should not need a second clean after the cleaners leave. Smartline cleans houses and apartments "
        "across Nairobi — weekly, fortnightly or once — and turns Airbnb units around between guests, ready "
        "for the next check-in.",
        "Our cleaners arrive equipped, work through an agreed checklist and walk you through the result before they "
        "go. Moving in or out? We do the top-to-bottom clean that gets a house ready to hand over, or to live in.",
    ],
    "/post-construction-cleaning": [
        "Builders finish; the dust does not. Fine dust settles for days, paint and cement splatter set hard, and glass, "
        "frames and tracks hold everything the trades left behind. Post-construction cleaning is its own discipline.",
        "Smartline phases the work to your handover date: a rough clean once the trades are out, a final clean before "
        "handover and a touch-up after snagging. Contractors, developers and owners get a space ready for people, "
        "not just finished.",
    ],
}

HOME_SERVICE_BLURB = {
    "Commercial & institutional": "Offices, banks, schools and churches on a written schedule.",
    "Homes & apartments": "Regular cleans, Airbnb turnovers, move-ins and sofas.",
    "Specialist cleans": "Post-construction, deep and one-time cleans, phased to your date.",
    "Outdoor": "Lawns, hedges and compounds kept as neat as the inside.",
}

# A-06, rewritten so every line is supported by the client's own material today.
# The stronger statutory and insurance claims wait for documents (CLIENT-REVIEW.md).
COMPLIANCE = [
    ("Training before placement", "Communication, equipment, chemical handling, grooming and PPE, teamwork, code of conduct"),
    ("Supervision", "Every site has a named supervisor accountable for the standard"),
    ("Presentation", "Uniformed, groomed and equipped for the job on every visit"),
    ("Products", "Cleaning chemicals used at the right dilution, stored and labelled"),
    ("Waste", "Segregated and taken to the agreed collection point"),
    ("Procurement documents", "Company registration and KRA PIN certificate, plus the supplier documents your process asks for"),
]

PRICING_MODELS = [
    ("Per clean", "One-time, deep and move-out work", "visit",
     "Priced on the size of the space and the state it is in. Photographs on WhatsApp are often enough."),
    ("Monthly contract", "Daily or weekly cleaning, one invoice", "month",
     "Priced on the scope and frequency agreed after a site visit. Contract rates are lower than one-off rates."),
    ("By area", "Offices and large floors", "sqm",
     "Priced per square metre for large or open-plan floors, after we have walked the space."),
]

GUARANTEE_SHORT = "Clean Quality Guaranteed · 24-hour re-clean"

ABOUT_STORY_2 = ("We learn each client's culture and ethics and align our cleaners' training to your standards. "
                 "We support and equip our teams to make a difference you can see, and we customise the programme "
                 "— comprehensive, quarterly, semi-annual or annual — to how your premises actually run.")

COMMUNITY = ("Growing Smartline means employing and training more people from the communities we work in. "
             "Job creation and corporate social responsibility are written into our vision, not added to it.")

# ------------------------------------------------------------------ privacy notice
PRIVACY = [
    ("Who we are",
     "Smartline Point Cleaning Hub Ltd (“Smartline”, “we”), " + STREET + ", " + LOCALITY + ", "
     + POSTAL + ". We decide how the personal data described here is used, under Kenya's Data Protection Act, 2019."),
    ("What we collect",
     "When you request a quote or contact us: your name, phone number, email address if you give it, your "
     "organisation if you give it, the location of the premises and the details of the job. When you call, email or "
     "WhatsApp us, the same details you choose to share."),
    ("Why we use it",
     "To reply to you, arrange a site visit, prepare a quote and deliver the service you ask for. We rely on your "
     "consent, given on the form, and on taking the steps you have asked for before a contract."),
    ("Cookies",
     "This site uses no advertising cookies. If analytics is switched on, it runs only after you accept it in the "
     "cookie notice, and you can change your mind at any time from the link in the footer."),
    ("Who we share it with",
     "No one, except as needed to run this website and our email. We do not sell or rent personal data."),
    ("How long we keep it",
     "Enquiries that do not lead to work are deleted within 12 months. Client records are kept for as long as the "
     "contract runs and any period the law requires after it."),
    ("Your rights",
     "You may ask to see the personal data we hold about you, to correct it, to delete it, or to object to how we use "
     "it. Write to " + EMAIL + " with “Data request” in the subject. If you are not satisfied with our reply, "
     "you may complain to the Office of the Data Protection Commissioner."),
]

# ------------------------------------------------------------------ images
# key -> (source file in media/all, aspect "w:h", focal point (x, y) 0..1, display width px, alt text)
# The build crops around the focal point, grades the whole set in one pass and
# exports WebP at 1x/1.5x/2x of the display width (capped at the source).
IMAGES = {
    # home
    "hero": ("corridor+4.webp", "4:5", (0.50, 0.55), 560,
             "A freshly cleaned corridor, its polished terrazzo floor reflecting the light"),
    # v2 full-bleed hero: wide for laptops, tall for phones (same photograph, art-directed)
    "hero-wide": ("corridor+4.webp", "16:9", (0.56, 0.30), 1440,
                  "A freshly cleaned corridor, its polished terrazzo floor reflecting the light"),
    "hero-tall": ("corridor+4.webp", "9:16", (0.58, 0.50), 480,
                  "A freshly cleaned corridor, its polished terrazzo floor reflecting the light"),
    "why": ("pexels-6196222.jpg", "3:4", (0.50, 0.62), 480,
            "A uniformed cleaning crew with their equipment outside a house"),
    "training": ("cleaning.jpg", "4:3", (0.62, 0.50), 520,
                 "Gloved hands spraying and wiping a surface"),
    # backgrounds
    "cta-bg": ("window cleaning.jpg", "21:9", (0.50, 0.42), 1440,
               ""),  # decorative under an ink overlay
    "page-bg": ("office floor.jpg", "21:9", (0.50, 0.70), 1440, ""),
    # about
    "about-hero": ("pexels-6195121.jpg", "16:9", (0.50, 0.38), 640,
                   "Three cleaners in uniform at the start of a shift"),
    "story": ("pexels-6196695.jpg", "4:5", (0.60, 0.45), 480,
              "A cleaner in overalls working on a kitchen wall"),
    "community": ("pexels-6195895.jpg", "4:5", (0.40, 0.55), 480,
                  "A cleaning crew loading equipment into a van"),
    # service rows
    "svc-commercial": ("bg11.jpg", "4:3", (0.55, 0.50), 400,
                       "A cleaner with a trolley wiping a lift panel in a bright office lobby"),
    "svc-carpet": ("Cleaning-Company-South-Africa.webp", "4:3", (0.50, 0.62), 400,
                   "A rotary machine shampooing a carpet"),
    "svc-school": ("hospital floor.avif", "4:3", (0.50, 0.50), 400,
                   "A bright glazed corridor with a clean floor"),
    "svc-church": ("pexels-8468417.jpg", "4:3", (0.50, 0.62), 400,
                   "Wooden benches and arched windows in a bright church hall"),
    "svc-residential": ("pexels-pixabay-48889.jpg", "4:3", (0.55, 0.50), 400,
                        "A flat mop working across a wooden floor"),
    "svc-apartment": ("pexels-9462733.jpg", "4:3", (0.50, 0.58), 400,
                      "Housekeepers changing the linen on a bed"),
    "svc-move": ("pexels-4246098.jpg", "4:3", (0.50, 0.55), 400,
                 "Furniture under dust sheets and stacked moving boxes"),
    "svc-sofa": ("pexels-4401535.jpg", "4:3", (0.45, 0.50), 400,
                 "A cleaning machine working on the fabric of a sofa"),
    "svc-washroom": ("pexels-arina-krasnikova-6653891.jpg", "4:3", (0.50, 0.64), 400,
                     "A clean white basin and tiled washroom wall"),
    "svc-postcon": ("pexels-15798784.jpg", "4:3", (0.50, 0.55), 400,
                    "A room under renovation with debris across the floor"),
    "svc-deep": ("pexels-alejandro-robles-duque-420889274-32908422.jpg", "4:3", (0.50, 0.55), 400,
                 "A scrubbing brush and suds on terracotta tiles"),
    "svc-onetime": ("pexels-caleboquendo-34516664.jpg", "4:3", (0.55, 0.58), 400,
                    "A cleaning trolley, mops and a bin ready in a corridor"),
    "svc-landscaping": ("pexels-jessicairoh-33123333.jpg", "4:3", (0.50, 0.62), 400,
                        "A groundsman with a brush cutter in a green compound"),
    # service pages
    "cc-hero": ("office floor.jpg", "4:3", (0.55, 0.50), 600,
                "A clean open office lobby with glazed partitions"),
    "ra-hero": ("pexels-6196692.jpg", "4:3", (0.50, 0.50), 600,
                "Two cleaners at work in a modern apartment kitchen"),
    "pc-hero": ("pexels-7937304.jpg", "4:3", (0.50, 0.55), 600,
                "A freshly plastered room before handover"),
    "cc-standard": ("corridor+4.webp", "4:5", (0.50, 0.62), 460,
                    "A polished corridor floor after a commercial clean"),
    "ra-standard": ("pexels-6197124.jpg", "4:5", (0.50, 0.42), 460,
                    "A cleaner finishing a glass window in a home"),
    "pc-standard": ("pexels-6197122.jpg", "4:5", (0.50, 0.42), 460,
                    "A cleaner working a full-height window"),
    # utility
    "notfound": ("cleaning (1).jpg", "4:3", (0.50, 0.55), 340, "A mop and a wet-floor sign"),
    # v3 (21/11/2026) — inner page heroes. Two photos dropped only for being black and white
    # come back as navy duotones (background only); two unused small photos frame the heroes.
    "duo-kitchen-bg": ("pexels-6196682.jpg", "16:9", (0.50, 0.50), 1440, ""),
    "duo-team-bg": ("pexels-6196225.jpg", "16:9", (0.50, 0.38), 1440, ""),
    "trolley": ("images.jfif", "4:3", (0.50, 0.50), 600,
                "A cleaner in yellow gloves preparing a trolley of cleaning supplies"),
    "office-mop": ("closeup-janitor-using-mop-clean-office-floor-maintain-workspace-hygiene-concept-janitorial-services-workplace-cleanliness-commercial-cleaning-office-hygiene-professional-janitor_91883.avif",
                   "16:9", (0.55, 0.55), 640, "A flat mop working across a polished office floor"),
}

# gallery: "Spaces we look after" (true of stock). Becomes "The work" when real photos replace it.
GALLERY = [
    ("g-church", "pexels-8468417.jpg", "3:4", (0.50, 0.55), "Churches", "A bright church hall with wooden benches"),
    ("g-linen", "pexels-9462733.jpg", "3:4", (0.50, 0.55), "Short-stay turnovers", "Bed linen being changed"),
    ("g-glass", "photo-1721620958961-cccc239cbb49.avif", "3:4", (0.50, 0.50), "Glass and partitions", "A squeegee on patterned glass"),
    ("g-polish", "why-professional-deep-cleaning-services-are-vital-after-heavy-rain-in-dubai.webp", "4:3", (0.50, 0.55), "Hard floors", "A floor machine on a polished floor"),
    ("g-newbuild", "pexels-7937304.jpg", "4:3", (0.50, 0.55), "New builds", "A plastered room awaiting handover"),
    ("g-kitchen", "post-construction-cleaning-768x1020.webp", "3:4", (0.50, 0.55), "Renovations", "A renovated kitchen before handover"),
    ("g-upholstery", "pexels-4401538.jpg", "4:3", (0.55, 0.55), "Upholstery", "An upholstery tool on a cushion"),
    ("g-compound", "pexels-themightynelson-6014518.jpg", "2:1", (0.50, 1.00), "Compounds", "Cut grass and a trimmer at work beside a palm"),
    ("g-wetfloor", "photo-1740657254989-42fe9c3b8cce.avif", "4:3", (0.55, 0.50), "Washrooms and floors", "Gloved hands cleaning a wet floor"),
    ("g-debris", "post-construction-cleaning-1.webp", "4:3", (0.50, 0.55), "Builders' clean", "A broom clearing plaster debris"),
    ("g-lawn", "images (2).jfif", "1:1", (0.50, 0.55), "Gardens", "A tropical lawn and planting"),
    ("g-moving", "pexels-4568707.jpg", "3:4", (0.55, 0.55), "Moving day", "A doorway onto stacked moving boxes"),
]

# service name -> image key for its row on /services
SERVICE_IMAGE = {
    "Commercial cleaning": "svc-commercial", "Office carpet cleaning": "svc-carpet",
    "School cleaning": "svc-school", "Church cleaning": "svc-church",
    "Residential cleaning": "svc-residential", "Apartment cleaning": "svc-apartment",
    "Move in / move out cleaning": "svc-move", "Sofa set & upholstery cleaning": "svc-sofa",
    "Toilet bowl & sink cleaning": "svc-washroom", "Post-construction cleaning": "svc-postcon",
    "Deep cleaning": "svc-deep", "One-time cleaning": "svc-onetime", "Landscaping": "svc-landscaping",
}

PAGE_IMAGES = {   # hero image per page, and the photo used in its share card
    "/": "hero", "/about": "about-hero", "/services": "svc-commercial",
    "/commercial-cleaning": "cc-hero", "/residential-apartment-cleaning": "ra-hero",
    "/post-construction-cleaning": "pc-hero", "/clients": "svc-church", "/contact": "svc-onetime",
}
STANDARD_IMAGE = {"CC": "cc-standard", "RA": "ra-standard", "PC": "pc-standard"}

# client sector -> filter key; chips on /services link to /clients?sector=<key>
SECTOR_KEY = {
    "Commercial complex": "commercial", "Banking": "banking", "Residential": "residential",
    "Church": "church", "Education": "education", "Short-stay": "short-stay", "Hospitality": "hospitality",
}
SECTOR_LABEL = {
    "banking": "Banking", "education": "Education", "church": "Churches", "residential": "Residential",
    "short-stay": "Short-stay", "hospitality": "Hospitality", "commercial": "Commercial",
}
CHIP_TO_SECTOR = {   # S-08 / C-03 chips that map onto a filter
    "Offices": "commercial", "Banks": "banking", "Schools": "education", "Churches": "church",
    "Apartment blocks": "residential", "Airbnb and short-stay": "short-stay",
    "Lounges and hospitality": "hospitality", "Banking": "banking", "Education": "education",
    "Residential complexes": "residential", "Short-stay and Airbnb": "short-stay", "Hospitality": "hospitality",
}

PROPERTY_TYPES = ["Office", "Home", "Apartment", "School", "Church", "Construction site", "Other"]
FREQUENCIES = ["One-time", "Daily", "Weekly", "Monthly", "Quarterly", "Semi-annual", "Annual", "Not sure yet"]
