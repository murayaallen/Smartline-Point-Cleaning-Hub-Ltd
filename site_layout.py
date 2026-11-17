# -*- coding: utf-8 -*-
"""Smartline Point Cleaning Hub Ltd — website layout, single source of truth.

Every page, every section, in order. make_layout.py renders this into
LAYOUT.md (the written spec) and wireframes.html (the visual plan), so the two
can never disagree. Edit here, rebuild both.

Section keys
  id      page prefix + order (H-03 = third section of Home)
  name    section name
  type    wireframe layout type (see make_layout.py)
  p       props used by the wireframe (real copy wherever the client gave us words)
  what    one line for the spec: what the section does
  mobile  how it changes under 768px
  needs   client inputs that block this section (empty = buildable today)
"""

SITE = "smartlinepointcleaning.co.ke"
PHONE = "+254 711 128736"
EMAIL = "info@smartlinepointcleaning.co.ke"

# ------------------------------------------------------------------ content
WELCOME = ("Welcome to Smartline Point Cleaning Hub Ltd, where cleanliness meets excellence. "
           "We provide reliable, affordable and professional cleaning for homes, offices, churches "
           "and commercial spaces. Our trained cleaners work with care and attention to detail, "
           "leaving every space spotless, fresh and ready to use. We believe a clean environment "
           "makes for a healthier, happier place to live and work. Clean spaces are our priority, "
           "and our clients' satisfaction is how we measure it.")

WHY = [  # client's own six points, from the share card
    ("Flexible scheduling", "Early mornings, weekends, after hours — cleaning fits around your work, not the other way round."),
    ("Qualified cleaners", "Trained in equipment, chemical handling, PPE and conduct before they set foot on site."),
    ("Trustworthy and friendly", "The same supervised team on your site, people your staff and residents get to know."),
    ("Affordable", "Clear quotes after a site visit, contract rates for regular work, no surprise charges."),
    ("Keen on details", "Skirting boards, switch plates, under the sink — the places a quick clean misses."),
    ("Quality results", "Clean Quality Guaranteed: if something is missed, we come back and put it right."),
]

TRAINING = [  # from the company profile
    ("Proper communication", "Clear, courteous with clients, staff and residents."),
    ("Equipment use", "Machines, mops and tools used correctly and safely."),
    ("Chemical handling", "Right product, right dilution, stored and labelled."),
    ("Grooming and PPE", "Uniformed, presentable, protected on every job."),
    ("Teamwork", "Supervised teams that cover for each other."),
    ("Code of conduct", "Honesty, confidentiality and respect for your premises."),
]

SCHEDULES = ["One-time clean", "Daily or weekly contract", "Quarterly", "Semi-annual",
             "Annual", "Comprehensive programme"]

GROUPS = [  # 13 services, grouped. Fumigation omitted — not licensed yet.
    ("Commercial & institutional", "/services#commercial", [
        ("Commercial cleaning", "/commercial-cleaning"),
        ("Office carpet cleaning", None),
        ("School cleaning", None),
        ("Church cleaning", None),
    ]),
    ("Homes & apartments", "/services#residential", [
        ("Residential cleaning", "/residential-apartment-cleaning"),
        ("Apartment cleaning", "/residential-apartment-cleaning"),
        ("Move in / move out cleaning", None),
        ("Sofa set & upholstery cleaning", None),
        ("Toilet bowl & sink cleaning", None),
    ]),
    ("Specialist cleans", "/services#specialist", [
        ("Post-construction cleaning", "/post-construction-cleaning"),
        ("Deep cleaning", None),
        ("One-time cleaning", None),
    ]),
    ("Outdoor", "/services#outdoor", [
        ("Landscaping", None),
    ]),
]

SERVICE_COPY = {  # DRAFT for client approval — one line, three inclusions, who it is for
    "Commercial cleaning": ("Scheduled cleaning for offices, banks and complexes, run by a supervised team that knows your premises.",
        ["Floors, desks and touchpoints", "Washrooms and kitchens", "Waste cleared and segregated"], "Offices, banks, complexes"),
    "Office carpet cleaning": ("Deep cleaning that lifts embedded dirt and stains from office carpets and rugs.",
        ["Stain pre-treatment", "Shampoo clean", "Dried and vacuumed"], "Offices, boardrooms, lounges"),
    "School cleaning": ("Classrooms, washrooms and dining halls kept clean and safe, timed around the school day.",
        ["Classrooms and corridors", "Washrooms sanitised", "Dining and staff areas"], "Schools and colleges"),
    "Church cleaning": ("Sanctuary, halls and washrooms made ready for services and events, week after week.",
        ["Pews and sanctuary", "Halls and washrooms", "After-event cleans"], "Churches and fellowship halls"),
    "Residential cleaning": ("Regular or one-off house cleaning by trained, vetted cleaners who treat your home with care.",
        ["Living areas and bedrooms", "Kitchen and bathrooms", "Floors throughout"], "Homes and families"),
    "Apartment cleaning": ("Apartment and Airbnb cleaning, including turnovers between guests and block common areas.",
        ["Unit cleans and turnovers", "Linen changed on request", "Common areas and stairwells"], "Residents, Airbnb hosts, landlords"),
    "Move in / move out cleaning": ("A top-to-bottom clean so a house is ready to hand over or to move straight into.",
        ["Inside cupboards and appliances", "Kitchen and bathrooms descaled", "Walls spot-cleaned, floors finished"], "Tenants, landlords, agents"),
    "Sofa set & upholstery cleaning": ("On-site cleaning of sofa sets, chairs and upholstery that lifts stains and refreshes fabric.",
        ["Stain pre-treatment", "Fabric shampoo", "Cushions and crevices"], "Homes, offices, lounges"),
    "Toilet bowl & sink cleaning": ("Descaling and sanitising that removes the stains routine cleaning leaves behind.",
        ["Limescale and stains removed", "Bowls, seats and taps sanitised", "Drains and overflows cleaned"], "Homes, offices, schools"),
    "Post-construction cleaning": ("Builders' dust, splatter and debris cleared so a new or renovated space is ready for handover.",
        ["Dust off every surface", "Paint and cement splatter removed", "Debris cleared from site"], "Contractors, developers, owners"),
    "Deep cleaning": ("An intensive clean of the places routine cleaning cannot reach — behind, under and inside.",
        ["Behind and under furniture", "Inside cupboards and appliances", "Grout, vents and high ledges"], "Homes, offices, kitchens"),
    "One-time cleaning": ("A single clean for an event, an inspection or a fresh start, with no contract required.",
        ["Scope agreed in advance", "Team arrives equipped", "Walk-through before we leave"], "Any home or premises"),
    "Landscaping": ("Lawns, hedges and compounds kept neat, so the outside of your property matches the inside.",
        ["Lawn mowing and edging", "Hedge and shrub trimming", "Compound cleared, waste removed"], "Homes, estates, institutions"),
}

CLIENTS = [  # from the company profile; publishing depends on client permission
    ("Jewel Complex", "Commercial complex"),
    ("Uwezo Microfinance Bank", "Banking"),
    ("Richland Pointe Apartments", "Residential"),
    ("ACK St Paul's Mukuyuini, Ruiru", "Church"),
    ("St Christopher's International School", "Education"),
    ("Canon Kimani's House Airbnbs", "Short-stay"),
    ("Pataya Properties Apartments", "Residential"),
    ("Seven Point Apartments", "Residential"),
    ("Steph Underground Lounge", "Hospitality"),
]

QUOTE_STEPS = [  # two steps: the job first (low commitment), then contact details
    ("Step 1 of 2 · The job", [
        "Service needed * — 13 options, pre-filled from ?service=",
        "Property type * — office / home / apartment / school / church / site / other",
        "Location / estate *", "How often — one-time … annual", "Preferred date"]),
    ("Step 2 of 2 · You", [
        "Full name *", "Phone (WhatsApp) *", "Email", "Organisation (optional)",
        "Anything we should know", "Consent to be contacted (Data Protection Act 2019) *"]),
]

NEEDS_PHOTOS = "Real job photographs"
NEEDS_PERMISSION = "Permission to name clients"
NEEDS_TESTIMONIALS = "3–5 testimonials with name and title"
NEEDS_HOURS = "Working hours and reply-time commitment"
NEEDS_AREAS = "Confirmed service areas"
NEEDS_FAQ = "Client answers to the FAQ questions"
NEEDS_PRICES = "Decision: show starting prices or quote-only"
NEEDS_SOCIAL = "Social media handles (Facebook, Instagram, LinkedIn, TikTok)"
NEEDS_PROOF = "Sign-off on the one-line proofs under each reason (they are draft commitments, incl. the re-clean promise)"


# ------------------------------------------------------------------ global
GLOBAL = [
    {"id": "G-01", "name": "Utility bar", "type": "utility",
     "what": "Phone, email, hours and service area above the header — the details a facility manager looks for first.",
     "mobile": "Hidden. Its job moves to the mobile action bar.", "needs": [NEEDS_HOURS]},
    {"id": "G-02", "name": "Header", "type": "header",
     "what": "Logo left; Home · About · Services ▾ · Clients · Contact; brass Request a quote button right. Sticky, compacts to 64px after 80px of scroll.",
     "mobile": "Logo, call icon, menu button. 64px tall.", "needs": []},
    {"id": "G-03", "name": "Services mega menu", "type": "mega",
     "what": "Four columns, one per service group, every service listed and linked. Opens on hover and on focus; Esc closes.",
     "mobile": "Becomes an accordion inside the drawer.", "needs": []},
    {"id": "G-04", "name": "Mobile drawer", "type": "drawer",
     "what": "Full-height panel from the right: nav, services accordion, phone, WhatsApp, quote button.",
     "mobile": "Mobile only. Focus trapped while open; body scroll locked.", "needs": []},
    {"id": "G-05", "name": "Mobile action bar", "type": "actionbar",
     "what": "Sticky bottom bar: Call · WhatsApp · Get a quote. The single most-used element on a phone.",
     "mobile": "Mobile only, 60px, respects the iPhone safe-area inset.", "needs": []},
    {"id": "G-06", "name": "WhatsApp button", "type": "wa",
     "what": "Floating bottom-right on desktop, opens a pre-filled chat: “Hello Smartline, I’d like a quote for…”.",
     "mobile": "Replaced by the action bar.", "needs": ["Which WhatsApp number"]},
    {"id": "G-07", "name": "CTA band", "type": "cta",
     "what": "Shared closing band on every page: Book your clean today, phone in large type, quote button.",
     "mobile": "Stacked, buttons full width.", "needs": []},
    {"id": "G-08", "name": "Footer", "type": "footer",
     "what": "Four columns — brand and tagline · services · company, careers and profile PDF · contact and hours. Social icons. Bottom bar: \u00a9 2026, privacy notice, cookie settings.",
     "mobile": "Columns become accordions; contact column stays open.", "needs": [NEEDS_SOCIAL]},
    {"id": "G-09", "name": "Cookie notice", "type": "cookie",
     "what": "Slim bar: “We use analytics cookies to improve this site.” Accept / Decline. GA4 loads only after Accept; the choice is kept 12 months. Needed for analytics under the Data Protection Act 2019.",
     "mobile": "Sits above the action bar; never covers the Call button.", "needs": []},
]


# ------------------------------------------------------------------ pages
def service_detail(prefix, slug, nav, h1, keyword, sub, who, included, process, faqs,
                   related, proof, extra_needs=()):
    return {
        "slug": slug, "nav": nav, "h1": h1, "keyword": keyword,
        "sections": [
            {"id": prefix + "-01", "name": "Page hero", "type": "hero_split",
             "p": {"eyebrow": "SERVICES  ·  " + nav.upper(), "h1": h1, "sub": sub,
                   "ctas": ["Request a quote", "WhatsApp us"], "trust": [], "crumb": "Home / Services / " + nav,
                   "image": "Photo: this service, on a real site", "seal": False},
             "what": "Keyword H1, one-line promise, quote button, a photo of this exact service.",
             "mobile": "Text first, image 4:3 under it, buttons full width.", "needs": []},
            {"id": prefix + "-02", "name": "Who it is for", "type": "chips",
             "p": {"heading": "Who we do this for", "items": who},
             "what": "Sector chips so a visitor recognises themselves in two seconds.",
             "mobile": "Chips wrap; horizontal scroll if more than two rows.", "needs": []},
            {"id": prefix + "-03", "name": "What is included", "type": "checklist",
             "p": {"heading": "What is included", "groups": included},
             "what": "The scope, by area, as a checklist — what the client is actually buying.",
             "mobile": "One column; each area is an expandable group, first one open.", "needs": []},
            {"id": prefix + "-04", "name": "How it runs", "type": "steps",
             "p": {"heading": "How it runs", "items": process},
             "what": "The working method for this service, step by step.",
             "mobile": "Vertical timeline with a brass spine.", "needs": []},
            {"id": prefix + "-05", "name": "The standard", "type": "standard",
             "p": {"heading": "What finished looks like",
                   "items": proof,
                   "body": "Every visit is worked against the written scope and checked by a named supervisor "
                           "before the team leaves. If something is missed, tell us within 24 hours and we come "
                           "back to it."},
             "what": "Ships now with a sourced photograph and the written standard. A stock before/after pair would "
                     "be passing off someone else's job as ours, so the drag-to-compare slider waits for REAL-03\u201305 "
                     "and drops into this same slot when they exist \u2014 no layout change needed.",
             "mobile": "Image, then the standard, then the two checkpoints.", "needs": []},
            {"id": prefix + "-06", "name": "Schedule options", "type": "chips",
             "p": {"heading": "Once, or on a schedule", "items": SCHEDULES},
             "what": "Frequencies offered, pushing visitors from a one-off job toward a contract.",
             "mobile": "Two-column chip grid.", "needs": []},
            {"id": prefix + "-07", "name": "Questions", "type": "faq",
             "p": {"heading": "Questions", "items": faqs},
             "what": "Four page-specific questions, marked up as FAQPage.",
             "mobile": "Accordion, unchanged.", "needs": [NEEDS_FAQ]},
            {"id": prefix + "-08", "name": "Related services", "type": "cards",
             "p": {"cols": 3, "items": [(r, [SERVICE_COPY[r][0]], "Learn more") for r in related]},
             "what": "Three related services to keep the visitor moving through the site.",
             "mobile": "Horizontal swipe row, one and a half cards visible.", "needs": []},
            {"id": prefix + "-09", "name": "Quick quote", "type": "quickquote",
             "p": {"heading": "Get a quote for " + nav.lower(), "service": nav},
             "what": "Short form — name, phone, location — with this service pre-selected. Same handler as the contact page.",
             "mobile": "Fields stacked, submit full width.", "needs": []},
        ] + [],
        "extra_needs": list(extra_needs),
    }


PAGES = [
    # ============================================================== HOME
    {"slug": "/", "nav": "Home", "h1": "Where cleanliness meets excellence.",
     "keyword": "cleaning services Nairobi",
     "title": "Cleaning Services in Nairobi | Smartline Point Cleaning Hub",
     "desc": "Reliable, affordable, professional cleaning for offices, homes, churches and new builds in Nairobi. Trained, supervised teams since 2018.",
     "schema": "CleaningService (LocalBusiness), WebSite, FAQPage",
     "sections": [
        {"id": "H-01", "name": "Hero", "type": "hero_split",
         "p": {"eyebrow": "SMARTLINE POINT CLEANING HUB LTD  ·  EST. 2018",
               "h1": "Where cleanliness meets excellence.",
               "sub": "Reliable, affordable, professional cleaning for homes, offices, churches and commercial spaces across Nairobi.",
               "ctas": ["Request a quote", "WhatsApp us"],
               "trust": ["Trained and vetted", "Supervised teams", "Since 2018", "Reply within one working day"],
               "image": "Photo: a finished commercial clean, people-free, daylight",
               "seal": True, "float": "Book your clean today  ·  " + PHONE},
         "what": "Client's own headline, the promise in one line, two actions, three trust points; the Clean Quality Guaranteed seal sits on the photo.",
         "mobile": "Headline and buttons first, photo 4:5 below, seal shrinks to 64px, float card hidden.",
         "needs": []},
        {"id": "H-02", "name": "Proof strip", "type": "stats",
         "p": {"items": [("2018", "Trading since"), ("9+", "Sites served"), ("13", "Services"),
                         ("Daily \u2192 annual", "Schedules")],
               "trusted": [n for n, _ in CLIENTS[:6]]},
         "what": "Four facts, then a quiet \u201cTrusted by\u201d row of client names \u2014 social proof in the first scroll, not the ninth.",
         "mobile": "Facts 2 \u00d7 2; names scroll sideways.", "needs": [NEEDS_PERMISSION]},
        {"id": "H-03", "name": "Welcome", "type": "two_col",
         "p": {"label": "WELCOME", "heading": "A single point of contact for every clean.",
               "body": WELCOME, "link": "About Smartline \u2192"},
         "what": "The client's welcome statement, edited for the web, set large beside a short heading.",
         "mobile": "Heading above, body below.", "needs": []},
        {"id": "H-04", "name": "Services", "type": "cards",
         "p": {"heading": "What we clean", "cols": 4,
               "items": [(g, [s for s, _ in items], "See all \u2192") for g, _, items in GROUPS],
               "schedules": SCHEDULES},
         "what": "Four group cards listing all 13 services, closed by the schedule options (one-time to annual) on one line.",
         "mobile": "Cards stacked; each shows three services and \u201c+ n more\u201d.", "needs": []},
        {"id": "H-05", "name": "Why Smartline", "type": "icon_grid",
         "p": {"heading": "Why clients stay with Smartline", "items": WHY, "image": True},
         "what": "The client's six reasons, each with a one-line proof, beside a photograph of cleaners at work. "
                 "While that photograph is stock the caption stays generic \u2014 \u201cTrained, supervised teams\u201d \u2014 and never "
                 "claims to be Smartline staff.",
         "mobile": "Photo on top, reasons in one column.", "needs": [NEEDS_PROOF]},
        {"id": "H-06", "name": "How we work", "type": "steps",
         "p": {"heading": "How we work",
               "items": [("Site visit", "We see the space before we price it."),
                         ("Scope and quote", "Written scope, clear price, agreed schedule."),
                         ("Team assigned", "A trained team and a named supervisor."),
                         ("Supervised clean", "Checked against the scope on every visit."),
                         ("Review", "Regular check-ins; the schedule adjusts with you.")]},
         "what": "Five-step method, numbered, joined by a hairline.",
         "mobile": "Vertical timeline.", "needs": []},
        {"id": "H-07", "name": "Trained cleaners", "type": "band",
         "p": {"heading": "Every Smartline cleaner is trained in", "items": [t for t, _ in TRAINING], "image": True},
         "what": "Ink-navy band listing the six training areas \u2014 the differentiator in a tender.",
         "mobile": "Photo first, list in two columns.", "needs": []},
        {"id": "H-08", "name": "Testimonials", "type": "testimonials",
         "p": {"heading": "In their words", "n": 3},
         "what": "Three testimonials with name, title and sector, placed after the method and training they vouch for.",
         "mobile": "Swipe carousel.", "needs": [NEEDS_TESTIMONIALS]},
        {"id": "H-09", "name": "Clean Quality Guaranteed", "type": "guarantee",
         "p": {"heading": "Clean Quality Guaranteed",
               "promise": "If something is missed, tell us within 24 hours and we come back and re-clean it \u2014 no argument, no extra charge.",
               "points": ["One named supervisor on your account",
                          "Work checked against the written scope on every visit",
                          "Monthly review; the schedule changes when your premises do"]},
         "what": "The seal, written out as a promise with a time limit on it. Both large Nairobi competitors publish a "
                 "24-hour re-clean guarantee \u2014 this is parity, and it answers the trust question that stops people booking.",
         "mobile": "Seal above, promise, then the three points.", "needs": [NEEDS_PROOF]},
        {"id": "H-10", "name": "FAQ", "type": "faq",
         "p": {"heading": "Questions we are asked",
               "items": ["Do you bring your own equipment and chemicals?",
                         "Do you charge for a site visit?",
                         "Can you clean outside working hours?",
                         "Are your cleaners vetted?",
                         "Which areas do you cover?"]},
         "what": "Five questions, marked up as FAQPage for search.",
         "mobile": "Accordion.", "needs": [NEEDS_FAQ]},
        {"id": "H-11", "name": "Closing CTA", "type": "cta",
         "p": {"heading": "Book your clean today", "sub": PHONE},
         "what": "Shared CTA band (G-07).", "mobile": "Stacked.", "needs": []},
     ]},

    # ============================================================== ABOUT
    {"slug": "/about", "nav": "About", "h1": "About Smartline",
     "keyword": "professional cleaning company Nairobi",
     "title": "About Our Cleaning Company in Nairobi | Smartline",
     "desc": "Since 2018, Smartline has kept Nairobi offices, homes, schools and churches clean with trained, supervised teams and a single point of contact.",
     "schema": "AboutPage, Organization, BreadcrumbList",
     "sections": [
        {"id": "A-01", "name": "Page hero", "type": "page_hero",
         "p": {"crumb": "Home / About", "h1": "About Smartline",
               "sub": "A professional cleaning company in Nairobi — one point of contact for every clean, since 2018.", "image": True},
         "what": "Compact hero with breadcrumb and a team photograph.",
         "mobile": "Image becomes a 16:9 band under the title.", "needs": []},
        {"id": "A-02", "name": "Our story", "type": "split_media",
         "p": {"heading": "Founded to take cleaning off your list",
               "body": "Smartline was established in 2018 to let businesses focus on their core work while hygiene and cleaning are handled through a single point of contact. Our staff are trained all round, well groomed and experienced enough to take on any cleaning task.",
               "image_left": False},
         "what": "The company's origin and purpose, from the About Us in the profile.",
         "mobile": "Text then image.", "needs": []},
        {"id": "A-03", "name": "Vision and mission", "type": "cards",
         "p": {"cols": 2, "items": [
             ("Vision", ["To become a leading cleaning services provider while contributing to the community through job creation and corporate social responsibility."], ""),
             ("Mission", ["Simplifying the lives of our clients — so they concentrate on the work that earns, not on cleaners and facility problems."], "")]},
         "what": "The two statements from the profile, set as a matched pair.",
         "mobile": "Stacked.", "needs": []},
        {"id": "A-04", "name": "How we work with you", "type": "two_col",
         "p": {"label": "OUR APPROACH", "heading": "We learn your business before we clean it.",
               "body": "We take time to understand each client's culture and ethics, and align our cleaners' training to your standards. We support and equip our teams to make a visible difference, and we customise the programme — comprehensive, quarterly, semi-annual or annual — to how your premises actually run.",
               "link": ""},
         "what": "The culture-fit argument from the profile — why Smartline is a partner, not a contractor.",
         "mobile": "Stacked.", "needs": []},
        {"id": "A-05", "name": "Training standards", "type": "icon_grid",
         "p": {"heading": "How our cleaners are trained", "items": TRAINING, "image": False},
         "what": "The six training areas, each with a line on what it means on site.",
         "mobile": "One column.", "needs": []},
        {"id": "A-06", "name": "Vetting, insurance and compliance", "type": "facts",
         "p": {"heading": "Vetting, insurance and compliance",
               "rows": [("Staff vetting", "ID checked, referenced, and known to a named supervisor"),
                        ("Employment", "Directly employed, not day labour"),
                        ("Statutory", "NSSF and SHIF compliant; KRA registered"),
                        ("Insurance", "Public liability cover \u2014 certificate on request"),
                        ("Products", "Approved cleaning chemicals, correctly diluted and labelled"),
                        ("Waste", "Segregated and taken to the agreed collection point")],
               "download": "Request our compliance pack"},
         "what": "The questions a facility manager or school asks before awarding a contract, answered in one table. "
                 "Every premium commercial cleaner researched puts vetting in the main navigation; none of the Nairobi "
                 "sites answer it at all.",
         "mobile": "Two-column key/value list.",
         "needs": ["Confirm which of these are true today, with documents \u2014 publish nothing we cannot evidence"]},
        {"id": "A-07", "name": "Community", "type": "split_media",
         "p": {"heading": "Jobs, and a cleaner community",
               "body": "Growing Smartline means employing and training more people. Corporate social responsibility is written into our vision, not added to it.",
               "image_left": True},
         "what": "Job creation and CSR, from the vision statement.",
         "mobile": "Image then text.", "needs": ["Any CSR activity or photographs to show"]},
        {"id": "A-08", "name": "Work with us", "type": "two_col",
         "p": {"label": "CAREERS", "heading": "We are always training the next team.",
               "body": "Growing Smartline means hiring and training more people \u2014 it is written into our vision, not "
                       "added to it. If you are reliable, teachable and want to be trained properly, send your details "
                       "and we will call you when the next intake opens.",
               "link": "Apply to join the team \u2192"},
         "what": "Recruitment is a standing need in this trade \u2014 Cleanology puts \u201cApply for a job\u201d in the header, ISS has "
                 "a whole \u201cGrow with us\u201d section. It also makes the job-creation claim in the vision visible rather than "
                 "stated. Applications go to operations@ via the same form handler.",
         "mobile": "Stacked; the apply button is full width.", "needs": []},
        {"id": "A-09", "name": "Company details", "type": "facts",
         "p": {"heading": "Company details",
               "rows": [("Registered name", "Smartline Point Cleaning Hub Ltd"), ("Established", "2018"),
                        ("Office", "ICIPE Road, Sports Drive, Suite 8, Kasarani"),
                        ("Postal", "P.O. Box 48018-00100, Nairobi"), ("Phone", PHONE), ("Email", EMAIL)],
               "download": "Download the company profile (PDF)"},
         "what": "The facts a procurement officer copies into a supplier form, plus the profile PDF.",
         "mobile": "Two-column key/value list.", "needs": []},
        {"id": "A-10", "name": "Closing CTA", "type": "cta",
         "p": {"heading": "Book your clean today", "sub": PHONE},
         "what": "Shared CTA band.", "mobile": "Stacked.", "needs": []},
     ]},

    # ============================================================== SERVICES HUB
    {"slug": "/services", "nav": "Services", "h1": "Our services",
     "keyword": "cleaning services Nairobi commercial residential",
     "title": "Office, Home & Post-Construction Cleaning | Smartline",
     "desc": "Thirteen services, one contract: offices, carpets, schools, churches, homes, apartments, move-outs, sofas, new builds, deep cleans and landscaping.",
     "schema": "CollectionPage, Service × 13, BreadcrumbList",
     "sections": [
        {"id": "S-01", "name": "Page hero", "type": "page_hero",
         "p": {"crumb": "Home / Services", "h1": "Our services",
               "sub": "Thirteen services, one point of contact, one invoice.", "image": False,
               "chips": [g for g, _, _ in GROUPS]},
         "what": "Compact hero with four jump chips, one per group.",
         "mobile": "Chips scroll horizontally.", "needs": []},
        {"id": "S-02", "name": "Group navigation", "type": "subnav",
         "p": {"items": [g for g, _, _ in GROUPS]},
         "what": "Sticky sub-navigation under the header; highlights the group in view.",
         "mobile": "Horizontal scroll strip, sticky.", "needs": []},
    ] + [
        {"id": "S-0%d" % (3 + i), "name": g, "type": "service_rows",
         "p": {"heading": g, "items": items},
         "what": "Each service as a row: photo, name, one-line description, three inclusions, who it is for, and Get a quote (pre-fills the form). Services with their own page link through.",
         "mobile": "Rows become cards, image on top.", "needs": [NEEDS_PRICES] if i == 0 else []}
        for i, (g, _, items) in enumerate(GROUPS)
    ] + [
        {"id": "S-07", "name": "Guide prices", "type": "pricing",
         "p": {"heading": "What it costs",
               "note": "Guide prices so you can budget. The final figure comes after a site visit \u2014 size, frequency "
                       "and access change it.",
               "tiers": [("Per clean", "One-time, deep and move-out work", "From KES \u2014 per visit"),
                         ("Monthly contract", "Daily or weekly cleaning, one invoice", "From KES \u2014 per month"),
                         ("By area", "Offices and large floors", "From KES \u2014 per m\u00b2")],
               "foot": "VAT where applicable. Contract rates are lower than one-off rates."},
         "what": "Both large Nairobi competitors publish KES price tables; a site with no numbers at all now reads as "
                 "the least transparent of the three. Guide prices with \u201cfinal price after a site visit\u201d keeps the site "
                 "visit in the process while still answering the first question every visitor has.",
         "mobile": "Three stacked cards; the figure stays large.",
         "needs": [NEEDS_PRICES, "Three guide figures from the client, or a decision to show none"]},
        {"id": "S-08", "name": "Sectors we know", "type": "chips",
         "p": {"heading": "Premises we already clean",
               "items": ["Offices", "Banks", "Schools", "Churches", "Apartment blocks", "Airbnb and short-stay",
                         "Lounges and hospitality", "New builds and sites"],
               "sub": "Every chip links to the clients page filtered to that sector."},
         "what": "The premium commercial cleaners researched organise by sector, not by task \u2014 a facility manager "
                 "looks for their own building type first. This is the cheap version of that: one chip row, no new pages.",
         "mobile": "Chip grid, two columns.", "needs": []},
        {"id": "S-09", "name": "Schedules", "type": "chips",
         "p": {"heading": "Once, or on a schedule", "items": SCHEDULES},
         "what": "Shared frequency band.", "mobile": "Two-column chip grid.", "needs": []},
        {"id": "S-10", "name": "Not sure what you need?", "type": "cta",
         "p": {"heading": "Not sure what you need?", "sub": "Book a site visit — we will scope it with you."},
         "what": "Routes undecided visitors to a site visit instead of losing them.",
         "mobile": "Stacked.", "needs": []},
     ]},

    # ============================================================== SERVICE DETAIL x3
    dict(service_detail(
        "CC", "/commercial-cleaning", "Commercial cleaning",
        "Commercial and office cleaning in Nairobi", "commercial cleaning Nairobi",
        "Offices, banks, schools, churches and complexes — cleaned on a schedule, by a supervised team.",
        ["Offices", "Banks", "Schools", "Churches", "Malls and complexes", "Lounges and hospitality"],
        [("Floors and carpets", ["Vacuum and mop", "Office carpet shampoo", "Scrub and polish hard floors"]),
         ("Washrooms", ["Toilet bowls and sinks descaled", "Sanitised touchpoints", "Consumables restocked"]),
         ("Work areas", ["Desks and surfaces dusted", "Phones and switches sanitised", "Partitions and glass"]),
         ("Kitchens and breakrooms", ["Counters and sinks", "Appliance exteriors", "Floors"]),
         ("Waste", ["Bins emptied and relined", "Waste segregated", "Removed to collection point"])],
        [("Site survey", "We walk the premises with you."),
         ("Scope and schedule", "Daily, weekly or programme — in writing."),
         ("Team placed", "Trained cleaners, a named supervisor."),
         ("Monthly review", "Standards checked, schedule adjusted.")],
        ["Can you clean outside office hours?", "Do you supply equipment and chemicals?",
         "Can the same cleaners stay on our site?", "What happens if a cleaner is absent?"],
        ["Office carpet cleaning", "School cleaning", "Church cleaning"],
        ["Office floor", "Washroom"]),
        title="Commercial & Office Cleaning in Nairobi | Smartline",
        desc="Scheduled commercial and office cleaning in Nairobi by trained, supervised teams: floors, carpets, washrooms, kitchens and waste. Request a site visit.",
        schema="Service, FAQPage, BreadcrumbList"),

    dict(service_detail(
        "RA", "/residential-apartment-cleaning", "Homes & apartments",
        "Home, apartment and Airbnb cleaning in Nairobi", "apartment cleaning Nairobi",
        "Weekly cleans, Airbnb turnovers, move-ins and move-outs — your home, done properly.",
        ["Homes", "Apartments", "Airbnb hosts", "Moving in or out", "Landlords and agents"],
        [("Living areas", ["Dusting high and low", "Floors vacuumed and mopped", "Glass and mirrors"]),
         ("Kitchen", ["Counters, sink and splashback", "Appliance exteriors", "Cupboard fronts"]),
         ("Bathrooms", ["Toilet bowl and sink descaled", "Shower and tiles", "Fittings polished"]),
         ("Bedrooms", ["Surfaces dusted", "Beds made on request", "Floors"]),
         ("Add-ons", ["Sofa sets and upholstery", "Move in / move out deep clean", "Inside cupboards"])],
        [("Book", "By form, call or WhatsApp."),
         ("Confirm", "Scope, time and price agreed."),
         ("Clean", "The team arrives equipped."),
         ("Walk-through", "You check it before we leave.")],
        ["Do I need to be home?", "Do you do Airbnb turnovers between guests?",
         "Can you clean sofas on site?", "How long does a move-out clean take?"],
        ["Move in / move out cleaning", "Sofa set & upholstery cleaning", "Deep cleaning"],
        ["Sofa set", "Bathroom"]),
        title="Home, Apartment & Airbnb Cleaning in Nairobi | Smartline",
        desc="House and apartment cleaning in Nairobi: regular cleans, Airbnb turnovers, move in / move out and sofa cleaning by trained, vetted cleaners.",
        schema="Service, FAQPage, BreadcrumbList"),

    dict(service_detail(
        "PC", "/post-construction-cleaning", "Post-construction",
        "Post-construction cleaning in Nairobi", "post construction cleaning Nairobi",
        "From builders' dust to handover-ready — phased, to your handover date.",
        ["Contractors", "Developers", "New homeowners", "Renovated offices", "Property managers"],
        [("Dust", ["Builders' dust off every surface", "High-level ledges and fittings", "Vents and fans"]),
         ("Splatter", ["Paint and cement removed", "Sticker and tape residue", "Grout haze"]),
         ("Glass", ["Windows inside and out", "Frames and tracks", "Glass partitions"]),
         ("Floors", ["Scrubbed", "Polished or sealed", "Skirting boards"]),
         ("Debris", ["Construction debris cleared", "Waste bagged", "Removed from site"])],
        [("Site walk", "With the contractor or owner."),
         ("Phased plan", "Rough clean, final clean, touch-up."),
         ("Clean", "Worked to your handover date."),
         ("Inspection", "Handover-ready, signed off.")],
        ["When in the build should we book?", "Do you remove construction debris?",
         "Can you work to a handover date?", "Do you clean occupied buildings after renovation?"],
        ["Deep cleaning", "Commercial cleaning", "Landscaping"],
        ["Before handover", "Floor finish"]),
        title="Post-Construction Cleaning in Nairobi | Smartline",
        desc="Post-construction cleaning in Nairobi: builders' dust, paint and cement splatter, glass, floors and debris cleared, phased to your handover date.",
        schema="Service, FAQPage, BreadcrumbList"),

    # ============================================================== CLIENTS
    {"slug": "/clients", "nav": "Clients", "h1": "Who we clean for",
     "keyword": "cleaning company Nairobi clients",
     "title": "Our Clients & Work | Smartline Point Cleaning Hub",
     "desc": "Banks, schools, churches, apartment blocks, short-stay hosts and lounges across Nairobi trust Smartline with their cleaning. See the work.",
     "schema": "CollectionPage, BreadcrumbList",
     "sections": [
        {"id": "C-01", "name": "Page hero", "type": "page_hero",
         "p": {"crumb": "Home / Clients", "h1": "Who we clean for",
               "sub": "Banks, schools, churches, apartments, short-stay and hospitality.", "image": False},
         "what": "Compact hero.", "mobile": "Unchanged.", "needs": []},
        {"id": "C-02", "name": "Client list", "type": "logos",
         "p": {"heading": "Clients served", "items": CLIENTS, "testimonials": False},
         "what": "Every named client with sector — or, without permission, the same grid by sector only.",
         "mobile": "One column list.", "needs": [NEEDS_PERMISSION]},
        {"id": "C-03", "name": "Sectors", "type": "chips",
         "p": {"heading": "Sectors", "items": ["Banking", "Education", "Churches", "Residential complexes",
                                               "Short-stay and Airbnb", "Hospitality", "Construction"]},
         "what": "Sector band — tells a new prospect their kind of premises is familiar ground.",
         "mobile": "Chip grid.", "needs": []},
        {"id": "C-04", "name": "Testimonials", "type": "testimonials",
         "p": {"heading": "In their words", "n": 3},
         "what": "Three testimonials, name and title, sector tag.",
         "mobile": "Swipe carousel.", "needs": [NEEDS_TESTIMONIALS]},
        {"id": "C-05", "name": "Spaces we look after", "type": "gallery",
         "p": {"heading": "Spaces we look after", "n": 9},
         "what": "Masonry grid with a keyboard-accessible lightbox. Ships with the sourced set under a heading that "
                 "is true of stock \u2014 these are the kinds of premises, not photographs of our jobs. Real job photos "
                 "replace them one at a time, and the heading becomes \u201cThe work\u201d on the day they do.",
         "mobile": "Two-column grid.", "needs": []},
        {"id": "C-06", "name": "Closing CTA", "type": "cta",
         "p": {"heading": "Book your clean today", "sub": PHONE},
         "what": "Shared CTA band.", "mobile": "Stacked.", "needs": []},
     ]},

    # ============================================================== CONTACT
    {"slug": "/contact", "nav": "Contact", "h1": "Book your clean",
     "keyword": "book cleaning services Nairobi",
     "title": "Cleaning Services Quote, Nairobi | Smartline",
     "desc": "Request a quote or book a site visit with Smartline Point Cleaning Hub, Kasarani, Nairobi. Call or WhatsApp +254 711 128736.",
     "schema": "ContactPage, CleaningService, BreadcrumbList",
     "sections": [
        {"id": "K-01", "name": "Page hero", "type": "page_hero",
         "p": {"crumb": "Home / Contact", "h1": "Book your clean",
               "sub": "Request a cleaning quote anywhere in Nairobi. Tell us about the space and we reply within one working day.", "image": False},
         "what": "Compact hero; the reply-time promise is the subheading.",
         "mobile": "Unchanged.", "needs": [NEEDS_HOURS]},
        {"id": "K-02", "name": "Quote form and contact card", "type": "form",
         "p": {"heading": "Request a quote", "steps": QUOTE_STEPS,
               "aside": ["Call  " + PHONE, "WhatsApp  " + PHONE, "Email  " + EMAIL,
                         "ICIPE Road, Sports Drive, Suite 8, Kasarani",
                         "P.O. Box 48018-00100, Nairobi", "Hours: to confirm"],
               "proof": ["\u201cReliable, and the same team every week.\u201d \u2014 testimonial, short",
                         "Clean Quality Guaranteed \u00b7 24-hour re-clean",
                         "Trained, vetted, directly employed"]},
         "what": "Two-step form \u2014 the job, then you \u2014 beside the contact card, with a testimonial and the guarantee "
                 "directly under the submit button (every conversion source researched puts proof next to the form). "
                 "Six required fields in all. Pre-filled from ?service= on every service page. PHP handler: honeypot, time-trap, rate limit, server-side validation; mails info@; success goes to /thank-you.",
         "mobile": "Call and WhatsApp buttons first, then the form, then the address.", "needs": []},
        {"id": "K-03", "name": "Map", "type": "map",
         "p": {"heading": "Find us",
               "body": "ICIPE Road, Sports Drive, Suite 8, Kasarani. Static map image linking to Google Maps — no third-party iframe, so the CSP stays tight and the page stays fast."},
         "what": "Static map with an Open in Google Maps link.",
         "mobile": "Full-width map, 4:3.", "needs": []},
        {"id": "K-04", "name": "Areas we serve", "type": "chips",
         "p": {"heading": "Areas we serve",
               "items": ["Kasarani", "Roysambu", "Ruiru", "Thika Road", "Nairobi CBD", "Westlands", "Kiambu"]},
         "what": "Service areas — also feeds areaServed in the schema.",
         "mobile": "Chip grid.", "needs": [NEEDS_AREAS]},
        {"id": "K-05", "name": "Questions", "type": "faq",
         "p": {"heading": "Before you book",
               "items": ["How fast will you reply?", "Is the site visit free?",
                         "Do you bring equipment and chemicals?"]},
         "what": "Three pre-booking questions.",
         "mobile": "Accordion.", "needs": [NEEDS_FAQ]},
     ]},
]

# utility pages: built and wireframed, not counted in the eight content pages
UTILITY_PAGES = [
    {"slug": "/thank-you", "key": "thankyou", "nav": "Thank you", "h1": "Thank you \u2014 we have your request",
     "keyword": "(noindex)", "title": "Thank You | Smartline Point Cleaning Hub",
     "desc": "Your request has reached Smartline. Here is what happens next.", "schema": "noindex",
     "why": "Form success page; fires the GA4 generate_lead conversion. noindex.",
     "sections": [
        {"id": "T-01", "name": "Confirmation", "type": "page_hero",
         "p": {"crumb": "", "h1": "Thank you \u2014 we have your request",
               "sub": "A copy is on its way to your email if you gave us one.", "image": False},
         "what": "Plain confirmation; the visitor knows it worked.", "mobile": "Unchanged.", "needs": []},
        {"id": "T-02", "name": "What happens next", "type": "steps",
         "p": {"heading": "What happens next",
               "items": [("We call or WhatsApp", "Within one working day."),
                         ("Site visit", "If the job needs one, at a time that suits you."),
                         ("Written quote", "Scope, price and schedule, in writing.")]},
         "what": "Sets expectations so the client does not chase, or go elsewhere.",
         "mobile": "Vertical timeline.", "needs": [NEEDS_HOURS]},
        {"id": "T-03", "name": "Need us sooner", "type": "cta",
         "p": {"heading": "Need us sooner?", "sub": PHONE},
         "what": "Call and WhatsApp for urgent jobs.", "mobile": "Stacked.", "needs": []},
     ]},
    {"slug": "/privacy", "key": "privacy", "nav": "Privacy", "h1": "Privacy notice",
     "keyword": "(utility)", "title": "Privacy Notice | Smartline Point Cleaning Hub",
     "desc": "How Smartline Point Cleaning Hub Ltd collects, uses and protects your personal data under Kenya's Data Protection Act 2019.",
     "schema": "WebPage",
     "why": "Required by the Data Protection Act 2019: the quote form collects names and phone numbers, and analytics sets cookies.",
     "sections": [
        {"id": "P-01", "name": "Notice", "type": "doc",
         "p": {"heading": "Privacy notice", "items": [
             "Who we are \u2014 Smartline Point Cleaning Hub Ltd, Kasarani, and how to reach us",
             "What we collect \u2014 name, phone, email, location and job details from the quote form",
             "Why \u2014 to reply, visit, quote and deliver the service you asked for",
             "Cookies \u2014 analytics only, and only after you accept",
             "How long we keep it, and who we share it with (no one, except to deliver the job)",
             "Your rights \u2014 access, correction, deletion, objection; how to exercise them",
             "Last updated date"]},
         "what": "Single readable column, headed sections, last-updated date.",
         "mobile": "Unchanged.", "needs": ["A named contact for data requests"]},
     ]},
    {"slug": "/404", "key": "notfound", "nav": "404", "h1": "This page has moved",
     "keyword": "(noindex)", "title": "Page Not Found | Smartline Point Cleaning Hub",
     "desc": "The page you were looking for is not here. Find our cleaning services or contact us.", "schema": "noindex",
     "why": "Branded dead-end recovery. noindex.",
     "sections": [
        {"id": "N-01", "name": "Not found", "type": "page_hero",
         "p": {"crumb": "", "h1": "This page has moved",
               "sub": "Or it never existed. Here is where to go instead.", "image": False},
         "what": "Honest, short.", "mobile": "Unchanged.", "needs": []},
        {"id": "N-02", "name": "Ways back", "type": "cards",
         "p": {"cols": 4, "items": [(g, [s for s, _ in items][:3], "See all \u2192") for g, _, items in GROUPS]},
         "what": "The four service groups, so a lost visitor is one click from what they wanted.",
         "mobile": "Stacked.", "needs": []},
        {"id": "N-03", "name": "Contact", "type": "cta",
         "p": {"heading": "Or just ask us", "sub": PHONE},
         "what": "Shared CTA band.", "mobile": "Stacked.", "needs": []},
     ]},
]

# ------------------------------------------------------------------ design system (web)
PALETTE = [
    ("Ink", "#0E1430", "Text, header on scroll, dark bands, footer"),
    ("Indigo", "#241E63", "Links, secondary buttons, icon strokes"),
    ("Brass", "#B8862F", "Primary buttons (ink text), rules, seal, accents on ink"),
    ("Brass text", "#7F5B17", "Brass when it has to be small text on paper or white"),
    ("Paper", "#FAF8F4", "Page background"),
    ("White", "#FFFFFF", "Cards, form fields"),
    ("Stone", "#E7E3DA", "Hairlines, dividers, card borders"),
    ("Muted", "#5F5B55", "Secondary text, captions"),
]

CONTRAST_PAIRS = [  # (foreground, background, use, minimum)
    ("#0E1430", "#FAF8F4", "Body text on paper", 7.0),
    ("#5F5B55", "#FAF8F4", "Muted text on paper", 4.5),
    ("#241E63", "#FAF8F4", "Links on paper", 4.5),
    ("#7F5B17", "#FAF8F4", "Brass text on paper", 4.5),
    ("#0E1430", "#B8862F", "Button label on brass", 4.5),
    ("#B8862F", "#0E1430", "Brass on ink band", 4.5),
    ("#FFFFFF", "#0E1430", "White on ink band", 7.0),
    ("#FAF8F4", "#241E63", "Paper on indigo button", 4.5),
]

TYPE_SCALE = [  # (role, family, desktop px, mobile px, notes)
    ("Display / H1", "Bodoni Moda 500", 60, 38, "line-height 1.05, tracking -0.01em"),
    ("H2", "Bodoni Moda 500", 42, 30, "line-height 1.12"),
    ("H3", "Manrope 600", 22, 19, "line-height 1.3"),
    ("Eyebrow", "Manrope 600, uppercase", 12, 11, "tracking 0.18em, brass on ink / brass-text on paper"),
    ("Body", "Manrope 400", 17, 16, "line-height 1.65, max 68ch"),
    ("Small / caption", "Manrope 500", 14, 13, "line-height 1.5"),
    ("Button", "Manrope 600", 15, 15, "tracking 0.04em, 48px min height"),
]


IMAGE_SLOTS = [  # (slot, aspect, source size, notes)
    ("Home hero", "4:5 portrait", "1600 \u00d7 2000", "Finished commercial clean, people-free, daylight; WebP \u2264 180 KB"),
    ("Service page hero", "4:3", "1600 \u00d7 1200", "The exact service on a real site"),
    ("About hero", "16:9", "1920 \u00d7 1080", "The team in uniform"),
    ("Service row", "4:3", "800 \u00d7 600", "One per service \u2014 13 in all"),
    ("Why \u2014 team (H-05)", "3:4", "1200 \u00d7 1600", "Cleaners at work, PPE visible"),
    ("Training band (H-07)", "4:3", "1200 \u00d7 900", "Hands, gloves, product \u2014 close and disciplined"),
    ("Before / after", "4:3, a matched pair", "1600 \u00d7 1200 each", "Same spot, same angle, same light \u2014 or it is not proof"),
    ("Gallery", "Free", "1200 long edge", "9\u201312 real jobs"),
    ("Share image (Open Graph)", "1.91:1", "1200 \u00d7 630", "One per content page, built from the brand template"),
    ("Icons", "1:1", "32 / 180 / 192 / 512", "From the chosen logo; favicon.svg plus PNGs"),
]

BUILD_STANDARDS = [
    ("Accessibility", [
        "Skip-to-content link; one H1 per page; lang=\"en-GB\"",
        "Visible focus ring on everything interactive: 2px brass outline, 2px offset",
        "Touch targets \u2265 44 \u00d7 44px",
        "Mega menu: Enter/Space opens, arrow keys move, Esc closes and returns focus",
        "Mobile drawer traps focus while open; body scroll locked",
        "Before/after slider is a labelled range input \u2014 keyboard operable",
        "Form: visible labels, errors tied to fields with aria-describedby, announced on submit",
        "Alt text written per image, not generated; decorative images get empty alt",
        "All motion off under prefers-reduced-motion",
    ]),
    ("Performance budget", [
        "Home page \u2264 1 MB on first load; images above the fold \u2264 200 KB",
        "Two font families, WOFF2 subsets, \u2264 120 KB total; the two critical files preloaded; font-display: swap",
        "JavaScript \u2264 30 KB, no framework; analytics only after consent",
        "Responsive images with srcset and explicit width/height on every img",
        "LCP < 2.0s on 4G \u00b7 CLS < 0.05 \u00b7 INP < 200ms \u00b7 Lighthouse \u2265 95 mobile on all four scores",
    ]),
    ("SEO, technical", [
        "Canonical on every page: https apex, no trailing slash, no index.html",
        "Open Graph and Twitter cards on every content page, 1200 \u00d7 630 image",
        "sitemap.xml with lastmod; robots.txt points to it; /thank-you and /404 noindex",
        "CleaningService schema: address, geo, telephone, openingHours, areaServed, sameAs (socials)",
        "Phone links tel:+254711128736; WhatsApp links https://wa.me/254711128736?text=\u2026 (no plus, no spaces)",
        "Search Console verified by DNS TXT; Google Business Profile linked both ways",
    ]),
    ("Security and hosting", [
        ".htaccess: HTTPS and www \u2192 apex 301s, clean URLs, gzip, long cache on versioned assets",
        "Headers: CSP default-src self (Google Analytics allowed only for the consented script), HSTS, X-Content-Type-Options, Referrer-Policy, Permissions-Policy, frame-ancestors none",
        "Form handler: honeypot, minimum fill time, per-IP rate limit, server-side validation, authenticated SMTP to info@",
        "No third-party embeds: static map image, no iframes",
    ]),
]


ROADMAP = [  # (what, why, when)
    ("Area pages \u2014 Kasarani, Ruiru, Roysambu, Westlands, CBD",
     "Local-search guidance is consistent: one blanket \u201careas we serve\u201d page rarely ranks, while a page per area does. "
     "Five short pages, each with the services, a local job and the same quote form.",
     "Phase 2, after launch \u2014 outside the quoted eight pages"),
    ("Sector pages \u2014 schools, churches, apartment blocks",
     "Every premium commercial cleaner researched sells by sector, because a facility manager searches for their own "
     "building type. The chip row on /services is the cheap version; real pages are the full one.",
     "Phase 2, by demand"),
    ("Case notes \u2014 three one-paragraph results",
     "A Nairobi competitor runs \u201cWestlands law firm, 30% fewer sick days\u201d. One honest result per sector beats any "
     "amount of adjectives \u2014 but it waits for real numbers from real jobs.",
     "Once REAL-03\u201306 photographs and a client agrees to be quoted"),
    ("Client area \u2014 schedules, visit reports, invoices",
     "Both London firms researched run a client portal. For Smartline the useful first version is a per-client page "
     "with the cleaning schedule and the last visit report.",
     "Phase 3, if contracts grow"),
    ("Recruitment intake form",
     "The careers block on About starts as a mailto. If applications become regular, make it a real form to "
     "operations@ with a simple pipeline.",
     "When the careers block earns its keep"),
    ("Instant estimate",
     "Justlife in Dubai publishes an hourly rate and books in under a minute; both Nairobi competitors publish tables. "
     "If Smartline settles its rate card, the guide-price block becomes a three-field estimator.",
     "Once the rate card is fixed"),
]
