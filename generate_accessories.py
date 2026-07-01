#!/usr/bin/env python3
"""Generate the GG Putters ACCESSORIES + FITTER KIT page for Bricks 2.3.6,
matching the aesthetics/structure of the user's edited `gg-home` template.

- Reuses the ALREADY-IMPORTED global classes (ggsect, gghead, ggrow, ggcol,
  ggcolw, ggcta, ggeyeb, gglead, ggimg, gglink, ggbtn, ggh) — classes are NOT
  redefined with different settings, only referenced by id.
- Uses the site color palette variables (var(--champagne), var(--kachi-iro*),
  var(--platinum), var(--slate-bright)) and the same card styling
  (box-shadow champagne + radius/padding 14), icons (ionicons/themify),
  FAQ as an `accordion` element with faqSchema, section backgrounds/gradients.
- Keeps the DEDICATED, unique SEO/GEO content for Accessories + Fitter Kit and
  a Head (canonical, Open Graph/Twitter, JSON-LD) via pageSettings.
Output: gg-accessories-page.json
"""
import json

SHOP = "https://shop.ggputters.com"
PAGE_URL = f"{SHOP}/accessories/"
UP = "https://ggputters.com/shop/wp-content/uploads/2026/06"

# ----------------------------------------------------------------------------
# Site color palette (same ids/vars as the edited gg-home)
# ----------------------------------------------------------------------------
SLATE     = {"id": "gyxxbr", "name": "", "raw": "var(--slate-bright)", "light": "hsl(218 30.79% 76.77%)"}
PLATINUM  = {"id": "oiksff", "raw": "var(--platinum)", "light": "#f7f6f8"}
CHAMPAGNE = {"id": "daywbl", "raw": "var(--champagne)", "light": "#d4af37"}
KACHI     = {"id": "rhefaq", "raw": "var(--kachi-iro)", "light": "#1f2b51"}
KACHI2    = {"id": "nndbjg", "name": "", "raw": "var(--kachi-iro-2)", "light": "hsl(226 44.63% 33.48%)"}
KACHI3    = {"id": "oehxwa", "name": "", "raw": "var(--kachi-iro-3)", "light": "hsl(226 44.63% 45%)"}
KACHI4    = {"id": "tplylp", "name": "", "raw": "var(--kachi-iro-4)", "light": "hsl(226 58.04% 56.53%)"}
KACHI6    = {"id": "ivivyf", "name": "", "raw": "var(--kachi-iro-6)", "light": "hsl(226 44.63% 10.43%)",
             "darkModeEnabled": True, "dark": "hsl(226 44.62% 89.57%)"}
KACHI6T3  = {"id": "ukqcoe", "raw": "var(--kachi-iro-6-t-3)", "light": "hsla(226, 45%, 10%, 0.6)"}
KACHI6L4  = {"id": "fdwsdc", "raw": "var(--kachi-iro-6-l-4)", "light": "hsl(227, 5%, 82%)"}

TEXT_M = "var(--text-m)"
TEXT_S = "var(--text-s)"
TEXT_L = "var(--text-l)"

BG_SQUARE = {"id": 71, "filename": "bg-square-gg.jpg", "size": "large",
             "full": f"{UP}/bg-square-gg.jpg", "url": f"{UP}/bg-square-gg-1024x1024.jpg"}
LOGO_GOLD = {"id": 79, "filename": "logo-gg-gold.svg", "size": "full",
             "full": f"{UP}/logo-gg-gold.svg", "url": f"{UP}/logo-gg-gold.svg"}

CARD = {
    "_boxShadow": {"color": CHAMPAGNE, "values": {"blur": TEXT_S}},
    "_border": {"radius": {"top": "14", "right": "14", "bottom": "14", "left": "14"}},
    "_padding": {"top": "14", "right": "14", "bottom": "14", "left": "14"},
}

# ----------------------------------------------------------------------------
# Global classes reused verbatim (same ids/settings as already imported)
# ----------------------------------------------------------------------------
GLOBAL_CLASSES = [
    {"id": "ggeyeb", "name": "gg-eyebrow", "settings": {"_typography": {"text-transform": "uppercase", "letter-spacing": "0.18em", "font-weight": "600"}}},
    {"id": "gglead", "name": "gg-lead", "settings": {"_widthMax": "65ch"}},
    {"id": "ggsect", "name": "gg-section", "settings": {"_padding": {"top": "clamp(3.5rem, 7vw, 7rem)", "bottom": "clamp(3.5rem, 7vw, 7rem)", "left": "clamp(1rem, 4vw, 2rem)", "right": "clamp(1rem, 4vw, 2rem)"}}},
    {"id": "gghead", "name": "gg-header", "settings": {"_display": "flex", "_direction": "column", "_alignItems": "center", "_rowGap": "0.9rem", "_widthMax": "720px", "_margin": {"left": "auto", "right": "auto", "bottom": "clamp(2rem, 4vw, 3.5rem)"}, "_typography": {"text-align": "center"}}},
    {"id": "ggrow", "name": "gg-row", "settings": {"_display": "flex", "_flexWrap": "wrap", "_justifyContent": "center", "_alignItems": "stretch", "_rowGap": "clamp(1.5rem, 3vw, 2.5rem)", "_columnGap": "clamp(1.5rem, 3vw, 2.5rem)", "_width": "100%"}},
    {"id": "ggcol", "name": "gg-col", "settings": {"_flexGrow": "1", "_flexShrink": "1", "_flexBasis": "300px", "_widthMin": "0", "_display": "flex", "_direction": "column", "_rowGap": "0.75rem"}},
    {"id": "ggcolw", "name": "gg-col-wide", "settings": {"_flexGrow": "1", "_flexShrink": "1", "_flexBasis": "400px", "_widthMin": "0", "_display": "flex", "_direction": "column", "_rowGap": "1rem", "_justifyContent": "center"}},
    {"id": "ggcta", "name": "gg-cta-row", "settings": {"_display": "flex", "_flexWrap": "wrap", "_justifyContent": "center", "_rowGap": "1rem", "_columnGap": "1rem"}},
    {"id": "ggimg", "name": "gg-img", "settings": {"_width": "100%"}},
    {"id": "gglink", "name": "gg-link", "settings": {"_typography": {"text-decoration": "underline"}}},
    {"id": "ggbtn", "name": "gg-btn", "settings": {"_width:mobile_portrait": "100%", "_justifyContent:mobile_portrait": "center"}},
    {"id": "ggh", "name": "gg-h", "settings": {"_typography": {"text-wrap": "balance"}}},
]

# ----------------------------------------------------------------------------
# ID helpers + tree
# ----------------------------------------------------------------------------
_c = 0
def nid():
    global _c
    _c += 1
    return f"c{_c:05d}"

_a = 0
def aid():
    global _a
    _a += 1
    return f"t{_a:05d}"

elements = []

class El:
    def __init__(self, name, settings=None, label=None, children=None):
        self.name, self.settings, self.label, self.children = name, settings or {}, label, children or []

def flatten(el, parent):
    eid = nid()
    node = {"id": eid, "name": el.name, "parent": parent, "children": [], "settings": el.settings}
    if el.label:
        node["label"] = el.label
    elements.append(node)
    for ch in el.children:
        node["children"].append(flatten(ch, eid))
    return eid

def typo(color=None, size=None, **extra):
    t = {}
    if color:
        t["color"] = color
    if size:
        t["font-size"] = size
    t.update(extra)
    return t

def heading(text, tag, classes=None, color=None, size=None, extra=None, label=None):
    s = {"text": text, "tag": tag}
    if classes:
        s["_cssGlobalClasses"] = classes
    t = typo(color, size, **(extra or {}))
    if t:
        s["_typography"] = t
    return El("heading", s, label=label or f"{tag}: {text[:22]}")

def eyebrow(text, color=None):
    return heading(text, "p", ["ggeyeb"], color=color, label=f"Eyebrow: {text[:16]}")

def textp(text, classes=None, color=None, label=None):
    s = {"text": text, "tag": "p"}
    if classes:
        s["_cssGlobalClasses"] = classes
    if color:
        s["_typography"] = {"color": color}
    return El("text-basic", s, label=label or "Text")

def richhtml(html, label="Rich text"):
    return El("text", {"text": html}, label=label)

def icon(lib, ic, color=CHAMPAGNE, size=None):
    s = {"icon": {"library": lib, "icon": ic},
         "_attributes": [{"id": aid(), "name": "aria-hidden", "value": "true"}],
         "iconColor": color}
    if size:
        s["iconSize"] = size
    return El("icon", s, label="Icon")

def button(text, url, aria=None):
    link = {"type": "external", "url": url, "newTab": True}
    if aria:
        link["ariaLabel"] = aria
    return El("button", {"text": text, "link": link, "_cssGlobalClasses": ["ggbtn"]},
              label=f"Button: {text}")

def tlink(text, url, label="Link"):
    return El("text-link", {"text": text, "link": {"type": "external", "url": url},
                            "_cssGlobalClasses": ["gglink"]}, label=label)

def image(media, alt=None, extra=None, label=None):
    s = {"image": media, "_cssGlobalClasses": ["ggimg"]}
    if alt:
        s["image"] = dict(media)
        s["altText"] = alt
    if extra:
        s.update(extra)
    return El("image", s, label=label or "Image")

def block(children, classes=None, extra=None, label=None):
    s = {}
    if classes:
        s["_cssGlobalClasses"] = classes
    if extra:
        s.update(extra)
    return El("block", s, children=children, label=label or "Block")

def col(children, wide=False, extra=None, label=None):
    return block(children, ["ggcolw" if wide else "ggcol"], extra=extra, label=label or "Column")

def row(children, extra=None, label=None):
    e = {"_direction": "row"}
    if extra:
        e.update(extra)
    return block(children, ["ggrow"], extra=e, label=label or "Row")

def container(children, extra=None, label=None):
    return El("container", extra or {}, children=children, label=label or "Container")

_grad_i = 0
def gradient(colors):
    global _grad_i
    stops = []
    for c in colors:
        _grad_i += 1
        stops.append({"id": f"g{_grad_i:04d}", "color": c})
    return {"_gradient": {"colors": stops}}

def section(children, css_id=None, bg=None, image_bg=False, grad=None, shape=None, extra=None, label=None):
    s = {"_cssGlobalClasses": ["ggsect"]}
    if css_id:
        s["_cssId"] = css_id
    if image_bg:
        s["_background"] = {"image": BG_SQUARE, "attachment": "fixed", "position": "center center"}
    elif bg is not None:
        s["_background"] = {"color": bg}
    if grad:
        s.update(gradient(grad))
    if shape:
        s["_shapeDividers"] = shape
    if extra:
        s.update(extra)
    return El("section", s, children=children, label=label or "Section")

def header(eye, title, lead, eye_color, title_color, lead_color, tag="h2"):
    return block([
        eyebrow(eye, color=eye_color),
        heading(title, tag, ["ggh"], color=title_color),
        textp(lead, ["gglead"], color=lead_color),
    ], ["gghead"], label="Header")

# ============================================================================
# DATA (dedicated, unique)
# ============================================================================
# name, price, url, price_num, (lib,icon), definition, body, specs, glance_what, glance_options
ACCESSORIES = [
    ("Clubfaces", "€52", f"{SHOP}/putters/clubfaces/", "52.00", ("ionicons", "ion-ios-albums"),
     "Clubfaces are interchangeable milled face inserts that change the loft and feel of a GG putter.",
     "Swap the insert to tune roll and sound without buying a new putter: a higher degree adds forward loft for slower greens, a lower degree keeps the ball firmer on fast surfaces.",
     ["Lofts: 1°, 2°, 3°", "Milled to the GG face standard", "Fits Antares and Orion"],
     "Set loft &amp; feel", "1°–3°"),
    ("Extra Weights", "€21", f"{SHOP}/putters/extra-weights/", "21.00", ("ionicons", "ion-ios-options"),
     "Extra weights are swappable head weights for the three-position balance system.",
     "Moving weight changes the balance point and the natural arc of your stroke: heavier weights add stability, lighter weights increase feel. Bullet and flat shapes suit different placements.",
     ["Light 1.19 oz · Medium 1.48 oz · Heavy 1.97 oz", "Bullet or flat", "3 dedicated weight points"],
     "Set balance &amp; arc", "1.19 / 1.48 / 1.97 oz"),
    ("Putter Cover", "€32", f"{SHOP}/putters/putter-covers/", "32.00", ("ionicons", "ion-ios-umbrella"),
     "A putter cover is a fitted headcover that protects the milled head in the bag and in storage.",
     "It shields the face insert and the head edges from knocks, bag rash and moisture, preserving the anodized finish between rounds.",
     ["Shaped to the GG head", "Protects face and edges", "Everyday carry protection"],
     "Protect the head", "GG head shape"),
    ("Spare Parts Kit", "€149", f"{SHOP}/putters/spare-parts-kit/", "149.00", ("ionicons", "ion-ios-construct"),
     "The spare parts kit is a complete set of replacement hardware for your GG putter.",
     "It bundles the small components most likely to wear or get lost, so your putter stays serviceable for years and you are never off the green waiting on a single screw.",
     ["Screws, weights and hardware", "For long-term maintenance", "Fits Antares and Orion"],
     "Maintain &amp; replace", "Screws / weights / hardware"),
    ("Torque Wrench", "€63", f"{SHOP}/putters/torque-wrench/", "63.00", ("ionicons", "ion-ios-build"),
     "The torque wrench is a precision tool that tightens weights and faces to the correct, repeatable spec.",
     "Setting each component to the right torque prevents loosening during play and protects the threads, so every adjustment is secure and consistent.",
     ["Pre-set, repeatable torque", "For weights and clubfaces", "Protects the threads"],
     "Adjust to spec", "Pre-set torque"),
]

HOWTO = [
    ("Loosen the weight screws", "Loosen the three weight screws using the GG torque wrench."),
    ("Position the three weights", "Place the weights across the three points to match your stroke arc — light 1.19 oz, medium 1.48 oz, heavy 1.97 oz."),
    ("Set loft and feel", "Swap the clubface insert (1°–3°) to dial in your preferred loft and feel."),
    ("Tighten to spec", "Tighten everything back to the correct torque with the wrench."),
]

FAQ = [
    ("Which GG accessory should I buy first?",
     "For most players, extra weights (€21) give the biggest change to balance and feel; add clubfaces (€52) to adjust loft, and the torque wrench (€63) if you plan to adjust the putter yourself."),
    ("How do the three weights change my putter?",
     "The weights sit in three points and shift the head's balance: the 1.97 oz heavy weight adds stability for a straighter stroke, while the 1.19 oz light weight increases feel; the 1.48 oz medium sits in between."),
    ("How many clubface lofts are available and why do they matter?",
     "Clubfaces come in 1°, 2° and 3° (€52). A higher loft helps lift the ball into a smooth roll on slower greens; a lower loft keeps it firmer on fast surfaces."),
    ("Can I adjust the putter myself, or do I need a fitter?",
     "You can adjust weights and faces at home with the GG torque wrench (€63): loosen, reposition, swap the face, then tighten to spec. For a full fitting across models, use the Fitter Kit."),
    ("Do the accessories fit both the Antares and the Orion?",
     "Yes. The GG system is modular, so weights, clubfaces and necks are interchangeable between the Antares blade and the Orion mallet."),
    ("What does the Fitter Kit include and who is it for?",
     "The Fitter Kit is aimed at fitters, pro shops and club builders. It carries two heads (Antares and Orion), three lofts (1°–3°), a weights kit (2 heavy, 2 light), necks (lie and offset) and the tools to build any configuration."),
    ("Are accessories under warranty and how fast do they ship?",
     "GG accessories carry the same 2-year warranty as the putters and ship with BRT in Italy and FedEx worldwide, usually within 5–6 business days."),
]

# ============================================================================
# SECTIONS
# ============================================================================
# 1. HERO (bg image, light text)
hero = section(css_id="top", image_bg=True, label="Head / Hero", children=[
    container(children=[
        block([
            eyebrow("Accessories &amp; Fitter Kit", color=SLATE),
            image(LOGO_GOLD, extra={"_width": "12rem"}, label="Logo"),
            heading("GG Putters Accessories, Spare Parts &amp; Fitter Kit", "h1", ["ggh"],
                    color=PLATINUM, size=TEXT_L, label="H1"),
            textp("Customize and maintain your GG putter with milled accessories — interchangeable clubfaces, adjustable weights, covers and tools — priced from €21 to €149 and compatible with both Antares and Orion.",
                  ["gglead"], color=PLATINUM),
            block([
                button("Shop Accessories", PAGE_URL, aria="Shop GG Putters accessories"),
                button("Request the Fitter Kit", f"{SHOP}/for-fitters/", aria="Request the GG Putters Fitter Kit"),
            ], ["ggcta"], label="Hero CTAs"),
        ], ["gghead"], label="Hero Content"),
    ]),
])

# 2. ACCESSORIES (platinum bg, dark text) — cards with champagne shadow
def acc_card(name, price, url, ib, definition, body, specs):
    lib, ic = ib
    spec = "".join(f"<li>{s}</li>" for s in specs)
    return col([
        icon(lib, ic, color=CHAMPAGNE, size="36"),
        heading(name, "h3", ["ggh"], color=KACHI4, size=TEXT_M),
        heading(price, "p", color=CHAMPAGNE),
        textp(definition, color=KACHI),
        textp(body, color=KACHI),
        richhtml(f"<ul>{spec}</ul>", label="Specs"),
        tlink("View product", url, label=f"View {name}"),
    ], extra=dict(CARD), label=f"Accessory: {name}")

glance = "".join(
    f'<tr><th scope="row">{n}</th><td>{gw}</td><td>{go}</td><td>{p}</td></tr>'
    for (n, p, _u, _pr, _ib, _d, _b, _s, gw, go) in ACCESSORIES)
glance_table = richhtml(
    '<table><caption>GG Putters accessories at a glance</caption>'
    '<thead><tr><th scope="col">Accessory</th><th scope="col">What it does</th>'
    '<th scope="col">Options</th><th scope="col">Price</th></tr></thead>'
    f'<tbody>{glance}</tbody></table>', label="At-a-glance table")

accessories = section(css_id="accessories", bg=PLATINUM, label="Accessories", children=[
    container(children=[
        header("Milled accessories", "Accessories &amp; Spare Parts for GG Putters",
               "Fine-tune loft with clubfaces, dial in balance with weights, protect the head with a cover, and keep everything serviceable with the spare parts kit and torque wrench — all milled to the GG standard and priced from €21 to €149.",
               KACHI, KACHI3, KACHI),
        row([acc_card(n, p, u, ib, d, b, s)
             for (n, p, u, _pr, ib, d, b, s, _gw, _go) in ACCESSORIES], label="Accessories Grid"),
        block([
            heading("Accessories at a glance", "h3", ["ggh"], color=KACHI3),
            glance_table,
        ], ["ggcol"], extra={"_widthMax": "820px", "_margin": {"left": "auto", "right": "auto", "top": "clamp(2rem,4vw,3rem)"}, "_rowGap": "1rem"}, label="At a glance"),
    ]),
])

# 3. BUYING GUIDE (slate-bright bg, dark text)
buying = section(css_id="guide", bg=SLATE, label="Buying guide", children=[
    container(children=[
        header("Buying guide", "Which accessory do you need?",
               "Match the upgrade to your goal — here is the fastest way to decide.",
               KACHI, KACHI3, KACHI),
        block([richhtml(
            "<ul>"
            "<li><strong>Want more stability?</strong> Fit the heavy 1.97 oz weight (from €21).</li>"
            "<li><strong>Struggling on slow greens?</strong> Try a higher-degree clubface, up to 3° (€52).</li>"
            "<li><strong>Adjusting at home?</strong> The torque wrench sets weights and faces to spec (€63).</li>"
            "<li><strong>Protecting your investment?</strong> Add the fitted putter cover (€32).</li>"
            "<li><strong>Fitting clients?</strong> The Fitter Kit covers every head, loft and weight combination.</li>"
            "</ul>", label="Guide list")],
            ["ggcol"], extra={"_widthMax": "760px", "_margin": {"left": "auto", "right": "auto"}}, label="Guide"),
    ]),
])

# 4. TRUST (kachi-iro-6-l-4 bg) — platinum cards
def trust_card(lib, ic, title, text):
    return col([
        icon(lib, ic, color=CHAMPAGNE, size="36"),
        heading(title, "h3", ["ggh"], color=KACHI3),
        textp(text, color=KACHI),
    ], extra={**CARD, "_alignItems": "flex-start", "_margin": {"top": "15", "bottom": "30"},
              "_background": {"color": PLATINUM}}, label=f"Trust: {title}")

trust = section(bg=KACHI6L4, label="Trust", children=[
    container(children=[
        row([
            trust_card("ionicons", "ion-ios-checkmark-circle", "Fits Antares &amp; Orion",
                       "All accessories are compatible with both GG putter models."),
            trust_card("ionicons", "ion-ios-settings", "Set to spec",
                       "Use the torque wrench for repeatable, secure adjustments."),
        ], label="Trust Row 1"),
        row([
            trust_card("themify", "ti-shield", "2-year warranty",
                       "GG products are covered against conformity defects."),
            trust_card("themify", "ti-truck", "Fast shipping",
                       "BRT in Italy, FedEx worldwide — within 5–6 business days."),
        ], label="Trust Row 2"),
    ]),
])

# 5. HOW TO (platinum bg)
howto = section(css_id="setup", bg=PLATINUM, label="How to", children=[
    container(children=[
        header("Setup guide", "How to customize your GG putter",
               "In four steps you can rebalance the head and change the face — no specialist tools beyond the GG torque wrench.",
               KACHI, KACHI3, KACHI),
        block([richhtml(
            "<ol>" + "".join(f"<li><strong>{t}.</strong> {d}</li>" for t, d in HOWTO) + "</ol>",
            label="Steps")],
            ["ggcol"], extra={"_widthMax": "760px", "_margin": {"left": "auto", "right": "auto"}}, label="HowTo Steps"),
    ]),
])

# 6. FITTER KIT (kachi-iro dark bg, light text)
fitter = section(css_id="fitters", bg=KACHI, label="Fitter Kit", children=[
    container(children=[
        header("For fitters, pro shops &amp; club builders", "The GG Putters Fitter Kit",
               "A professional fitting system that builds and tests every head, loft, weight and neck combination in a single appointment.",
               CHAMPAGNE, PLATINUM, SLATE),
        row([
            col([
                heading("Fit by feel, not by guesswork", "h3", ["ggh"], color=CHAMPAGNE, size=TEXT_M),
                textp("With the kit on the bench, a player can compare changes back to back — blade against mallet, loft against loft, light weight against heavy — and immediately feel which setup rolls the ball best for their stroke.", color=PLATINUM),
                textp("A putter dialled in during fitting is genuinely made-to-measure, which typically means happier customers, fewer returns and a stronger case for a premium custom build.", color=PLATINUM),
                block([button("Request the Fitter Kit or book a demo", f"{SHOP}/for-fitters/",
                              aria="Request the GG Putters Fitter Kit or book a demo")], ["ggcta"], label="Fitter CTA"),
            ], wide=True, label="Fitter Text"),
            col([
                heading("What's inside the Fitter Kit", "h3", ["ggh"], color=CHAMPAGNE, size=TEXT_M),
                richhtml("<ul>"
                         "<li>2 heads — one Antares (blade) and one Orion (mallet)</li>"
                         "<li>3 lofts to swap — 1°, 2° and 3°</li>"
                         "<li>Weights kit — 2 heavy and 2 light (bullet or flat)</li>"
                         "<li>Necks — lie and offset options</li>"
                         "<li>Screws and a hex screwdriver to reconfigure on the spot</li>"
                         "</ul>", label="Kit list"),
                textp("Everything needed to demonstrate the full GG system to a client in one sitting.", color=SLATE),
            ], wide=True, extra={**CARD, "_background": {"color": KACHI6T3},
                                 "_typography": {"color": KACHI6L4}}, label="Fitter Kit Card"),
        ]),
    ]),
])

# 7. FAQ (platinum bg + shape divider) — accordion with faqSchema
accordion = El("accordion", {
    "accordions": [{"title": q, "content": f"<p>{a}</p>", "id": aid()} for q, a in FAQ],
    "titleTag": "h3",
    "icon": {"icon": "ion-ios-arrow-forward", "library": "ionicons"},
    "iconExpanded": {"icon": "ion-ios-arrow-down", "library": "ionicons"},
    "transition": "333", "titlePadding": {"left": "15", "right": "15"}, "faqSchema": True,
    "iconTypography": {"color": CHAMPAGNE, "font-size": TEXT_L},
    "contentTypography": {"color": KACHI}, "contentPadding": {"left": "30", "right": "30"},
    "contentBorder": {"style": "solid", "color": CHAMPAGNE, "width": {"top": "1", "right": "1", "bottom": "1", "left": "1"}},
    "titleActiveBorder": {"width": {"top": "2", "right": "2", "bottom": "2", "left": "2"}, "style": "solid",
                           "color": CHAMPAGNE, "radius": {"top": "7", "right": "7", "bottom": "7", "left": "7"}},
    "titleActiveTypography": {"color": KACHI3},
    "titleTypography": {"color": KACHI2, "text-align": "left", "font-weight": "600"},
    "iconPosition": "left", "_typography": {"font-size": TEXT_S},
}, label="FAQ Accordion")

faq = section(css_id="faq", bg=PLATINUM,
              shape=[{"id": aid(), "shape": "stroke-2", "fill": {"raw": "rgba(212, 175, 55, 0.12)"}, "flipVertical": True}],
              label="FAQ", children=[
    container(children=[
        header("FAQ", "Accessories &amp; Fitter Kit — FAQ",
               "Quick answers about compatibility, weights, lofts, tools, pricing and the Fitter Kit.",
               KACHI, KACHI3, KACHI),
        block([accordion], ["ggcol"],
              extra={"_widthMax": "780px", "_margin": {"left": "auto", "right": "auto"}, "_rowGap": "1.5rem"},
              label="FAQ List"),
    ]),
])

# 8. CONTACT (gradient slate -> platinum)
def contact_col(title, links):
    kids = [heading(title, "h3", ["ggh"], color=KACHI2)]
    kids += [tlink(v, h, label=k) for k, v, h in links]
    return col(kids, label=f"Contact: {title}")

contact = section(css_id="contact", grad=[SLATE, PLATINUM], label="Contact", children=[
    container(children=[
        header("Need help choosing?", "Talk to the GG Putters team",
               "Not sure which weights or face you need? Our team in Brescia will help you set up your putter.",
               KACHI, KACHI2, KACHI),
        row([
            contact_col("Info &amp; Sales", [("Email", "info@ggputters.com", "mailto:info@ggputters.com"),
                                             ("Phone", "+39 331 1099739", "tel:+393311099739")]),
            contact_col("Office &amp; Dealers", [("Email", "office@ggputters.com", "mailto:office@ggputters.com")]),
            contact_col("Headquarters", [("Address", "Palazzolo sull'Oglio (BS), Italy", f"{SHOP}/contact/")]),
        ]),
    ]),
])

# 9. FOOTER (gradient, champagne text)
footer = section(grad=[KACHI6, KACHI, KACHI6], label="Footer", children=[
    container(extra={"_typography": {"color": PLATINUM}}, children=[
        block([
            heading("GG Putters", "p", ["ggeyeb"], color=CHAMPAGNE, label="Brand"),
            image(LOGO_GOLD, extra={"_heightMax": "7vh"}, label="Footer Logo"),
            textp("Italian craft, Brescia engineering. Putters with a metalworking soul.", color=CHAMPAGNE),
            textp("GG PUTTERS is a brand of GM PRODUCTION srl · VAT IT03351530989 · Palazzolo sull'Oglio (BS), Italy", color=CHAMPAGNE),
            textp("© 2026 GG Putters. All rights reserved.", color=CHAMPAGNE),
        ], ["gghead"], label="Footer Content"),
    ]),
])

roots = [hero, accessories, buying, trust, howto, fitter, faq, contact, footer]
for r in roots:
    flatten(r, 0)

# ============================================================================
# HEAD (SEO/GEO): canonical + OG/Twitter + JSON-LD (FAQ handled by accordion)
# ============================================================================
PAGE_TITLE = "Putter Accessories, Spare Parts & Fitter Kit | GG Putters"
PAGE_DESC = ("GG Putters accessories: interchangeable clubfaces (1°–3°), adjustable weights "
             "(1.19–1.97 oz), covers, spare parts and the torque wrench, from €21 to €149. "
             "Compatible with Antares and Orion. Professional Fitter Kit available.")
OG_IMAGE = f"{UP}/logo-gg-gold.svg"

def product_ld(name, desc, price, url):
    return {"@type": "Product", "name": f"GG {name}",
            "brand": {"@type": "Brand", "name": "GG Putters"},
            "category": "Golf Putter Accessory", "description": desc, "url": url,
            "isAccessoryOrSparePartFor": [
                {"@type": "Product", "name": "GG Antares", "url": f"{SHOP}/putters/antares/"},
                {"@type": "Product", "name": "GG Orion", "url": f"{SHOP}/putters/orion/"}],
            "offers": {"@type": "Offer", "price": price, "priceCurrency": "EUR",
                        "availability": "https://schema.org/InStock", "url": url,
                        "priceValidUntil": "2026-12-31"}}

graph = [
    {"@type": "Organization", "@id": f"{SHOP}/#organization", "name": "GG Putters",
     "legalName": "GM PRODUCTION srl", "url": f"{SHOP}/", "vatID": "IT03351530989",
     "email": "info@ggputters.com", "telephone": "+39 331 1099739",
     "address": {"@type": "PostalAddress", "streetAddress": "Via Taranto, 7",
                  "addressLocality": "Palazzolo sull'Oglio", "addressRegion": "BS",
                  "postalCode": "25036", "addressCountry": "IT"}},
    {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{SHOP}/"},
        {"@type": "ListItem", "position": 2, "name": "Accessories", "item": PAGE_URL}]},
    {"@type": "CollectionPage", "@id": f"{PAGE_URL}#webpage", "url": PAGE_URL,
     "name": PAGE_TITLE, "description": PAGE_DESC, "isPartOf": {"@id": f"{SHOP}/#organization"}},
    {"@type": "ItemList", "name": "GG Putters Accessories",
     "itemListElement": [{"@type": "ListItem", "position": i + 1,
                           "item": product_ld(n, f"{d} {b}", pr, u)}
                          for i, (n, _p, u, pr, _ib, d, b, _s, _gw, _go) in enumerate(ACCESSORIES)]},
    {"@type": "Product", "name": "GG Putters Fitter Kit",
     "brand": {"@type": "Brand", "name": "GG Putters"}, "category": "Golf Fitting Kit",
     "url": f"{SHOP}/for-fitters/",
     "description": "Modular fitting kit for professionals: 2 heads (Antares and Orion), 3 lofts (1°–3°), weights kit, necks (lie/offset) and tools."},
    {"@type": "HowTo", "name": "How to customize your GG putter",
     "description": "Rebalance the head and change the face of a GG putter using the torque wrench, weights and clubfaces.",
     "tool": [{"@type": "HowToTool", "name": "GG torque wrench"}],
     "supply": [{"@type": "HowToSupply", "name": "GG weights (1.19/1.48/1.97 oz)"},
                 {"@type": "HowToSupply", "name": "GG clubfaces (1°–3°)"}],
     "step": [{"@type": "HowToStep", "position": i + 1, "name": t, "text": d}
              for i, (t, d) in enumerate(HOWTO)]},
]
json_ld = {"@context": "https://schema.org", "@graph": graph}

head = (
    f'<link rel="canonical" href="{PAGE_URL}">'
    '<meta name="robots" content="index,follow,max-image-preview:large">'
    f'<meta name="description" content="{PAGE_DESC}">'
    '<meta property="og:type" content="website">'
    '<meta property="og:site_name" content="GG Putters">'
    f'<meta property="og:title" content="{PAGE_TITLE}">'
    f'<meta property="og:description" content="{PAGE_DESC}">'
    f'<meta property="og:url" content="{PAGE_URL}">'
    f'<meta property="og:image" content="{OG_IMAGE}">'
    '<meta name="twitter:card" content="summary_large_image">'
    f'<meta name="twitter:title" content="{PAGE_TITLE}">'
    f'<meta name="twitter:description" content="{PAGE_DESC}">'
    '<script type="application/ld+json">' + json.dumps(json_ld, ensure_ascii=False) + '</script>'
)

template = {
    "name": "gg-accessories",
    "title": "gg-accessories",
    "type": "section",
    "content": elements,
    "templateType": "section",
    "pageSettings": {"pageTitle": PAGE_TITLE, "metaDescription": PAGE_DESC,
                     "customScriptsHeader": head},
    "global_classes": GLOBAL_CLASSES,
}

with open("gg-accessories-page.json", "w", encoding="utf-8") as f:
    json.dump(template, f, ensure_ascii=False, indent=2)

print(f"Generated {len(elements)} elements, {len(GLOBAL_CLASSES)} classes reused, "
      f"{len(ACCESSORIES)} accessories, {len(FAQ)} FAQ (accordion).")
