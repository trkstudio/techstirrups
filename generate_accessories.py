#!/usr/bin/env python3
"""Generate a Bricks Builder 2.3.6 template-export JSON for the GG Putters
ACCESSORIES + FITTER KIT page  ->  gg-accessories-page.json

Same style as the landing template:
- NO colors (theme owns colors & typography).
- Fully fluid responsive layout with Flexbox only (wrap + flex-basis).
- Minimal, reusable global classes; almost no inline styling.
- Accessibility kept (semantic headings, alt, aria-hidden icons, aria-labels,
  focus, reduced-motion).
- GEO ("Regola d'Oro"): one-sentence definitions, concrete data, inverted
  pyramid, lists, FAQ + rich <head> structured data (Breadcrumb, Product/Offer,
  HowTo, FAQPage) and Open Graph / Twitter meta.
"""
import json

SHOP = "https://shop.ggputters.com"
PAGE_URL = f"{SHOP}/accessories/"

# ----------------------------------------------------------------------------
# ID helpers
# ----------------------------------------------------------------------------
_counter = 0
def nid():
    global _counter
    _counter += 1
    return f"a{_counter:05d}"

_attr = 0
def attr_id():
    global _attr
    _attr += 1
    return f"t{_attr:05d}"

def attrs(pairs):
    return [{"id": attr_id(), "name": k, "value": v} for k, v in pairs]

elements = []

class El:
    def __init__(self, name, settings=None, label=None, children=None):
        self.name = name
        self.settings = settings or {}
        self.label = label
        self.children = children or []

def flatten(el, parent_id):
    eid = nid()
    node = {"id": eid, "name": el.name, "parent": parent_id,
            "children": [], "settings": el.settings}
    if el.label:
        node["label"] = el.label
    elements.append(node)
    for child in el.children:
        node["children"].append(flatten(child, eid))
    return eid

# ----------------------------------------------------------------------------
# Builders
# ----------------------------------------------------------------------------
def cls(*names):
    return {"_cssGlobalClasses": list(names)}

def heading(text, tag, classes=None, label=None):
    s = {"text": text, "tag": tag}
    if classes:
        s["_cssGlobalClasses"] = classes
    return El("heading", s, label=label or f"{tag}: {text[:24]}")

def para(text, classes=None, label=None):
    s = {"text": text, "tag": "p"}
    if classes:
        s["_cssGlobalClasses"] = classes
    return El("text-basic", s, label=label or "Text")

def rich(text, classes=None, label=None):
    s = {"text": text}
    if classes:
        s["_cssGlobalClasses"] = classes
    return El("text", s, label=label or "Rich text")

def eyebrow(text):
    return heading(text, "p", classes=["gg-eyebrow"], label=f"Eyebrow: {text[:18]}")

def icon(ti):
    return El("icon", {"icon": {"library": "themify", "icon": ti},
                       "_attributes": attrs([("aria-hidden", "true")])}, label="Icon")

def button(text, url, aria=None, new_tab=True):
    link = {"type": "external", "url": url}
    if new_tab:
        link["newTab"] = True
    if aria:
        link["ariaLabel"] = aria
    return El("button", {"text": text, "link": link, "_cssGlobalClasses": ["gg-btn"]},
              label=f"Button: {text}")

def text_link(text, url, label="Link"):
    return El("text-link", {"text": text, "link": {"type": "external", "url": url},
                            "_cssGlobalClasses": ["gg-link"]}, label=label)

def image_ph(alt, ratio="16/10", label=None):
    return El("image", {"image": {"url": "", "alt": alt}, "altText": alt,
                        "_aspectRatio": ratio, "_cssGlobalClasses": ["gg-img"]},
              label=label or f"Image: {alt[:22]}")

def section(children, classes=None, css_id=None, label=None):
    s = {"_cssGlobalClasses": ["gg-section"] + (classes or [])}
    if css_id:
        s["_cssId"] = css_id
    return El("section", s, children=children, label=label or "Section")

def container(children, label=None):
    return El("container", {}, children=children, label=label or "Container")

def header_block(eye, title, lead=None, tag="h2"):
    kids = [eyebrow(eye), heading(title, tag, classes=["gg-h"])]
    if lead:
        kids.append(para(lead, classes=["gg-lead"]))
    return El("block", cls("gg-header"), children=kids, label="Header")

def row(children, label=None):
    return El("block", cls("gg-row"), children=children, label=label or "Row")

def col(children, wide=False, label=None):
    return El("block", cls("gg-col-wide" if wide else "gg-col"), children=children,
              label=label or "Column")

# ----------------------------------------------------------------------------
# Global classes — identical to the landing template (layout only, no colors)
# ----------------------------------------------------------------------------
global_classes = [
    {"id": "ggsect", "name": "gg-section", "settings": {
        "_padding": {"top": "clamp(3.5rem, 7vw, 7rem)", "bottom": "clamp(3.5rem, 7vw, 7rem)",
                      "left": "clamp(1rem, 4vw, 2rem)", "right": "clamp(1rem, 4vw, 2rem)"}}},
    {"id": "gghead", "name": "gg-header", "settings": {
        "_display": "flex", "_direction": "column", "_alignItems": "center",
        "_rowGap": "0.9rem", "_widthMax": "720px",
        "_margin": {"left": "auto", "right": "auto", "bottom": "clamp(2rem, 4vw, 3.5rem)"},
        "_typography": {"text-align": "center"}}},
    {"id": "ggrow", "name": "gg-row", "settings": {
        "_display": "flex", "_flexWrap": "wrap", "_justifyContent": "center",
        "_alignItems": "stretch", "_rowGap": "clamp(1.5rem, 3vw, 2.5rem)",
        "_columnGap": "clamp(1.5rem, 3vw, 2.5rem)", "_width": "100%"}},
    {"id": "ggcol", "name": "gg-col", "settings": {
        "_flexGrow": "1", "_flexShrink": "1", "_flexBasis": "300px", "_widthMin": "0",
        "_display": "flex", "_direction": "column", "_rowGap": "0.75rem"}},
    {"id": "ggcolw", "name": "gg-col-wide", "settings": {
        "_flexGrow": "1", "_flexShrink": "1", "_flexBasis": "400px", "_widthMin": "0",
        "_display": "flex", "_direction": "column", "_rowGap": "1rem",
        "_justifyContent": "center"}},
    {"id": "ggcta", "name": "gg-cta-row", "settings": {
        "_display": "flex", "_flexWrap": "wrap", "_justifyContent": "center",
        "_rowGap": "1rem", "_columnGap": "1rem"}},
    {"id": "ggeye", "name": "gg-eyebrow", "settings": {
        "_typography": {"text-transform": "uppercase", "letter-spacing": "0.18em",
                         "font-weight": "600"}}},
    {"id": "gglead", "name": "gg-lead", "settings": {"_widthMax": "65ch"}},
    {"id": "ggimg", "name": "gg-img", "settings": {"_width": "100%"}},
    {"id": "gglink", "name": "gg-link", "settings": {
        "_typography": {"text-decoration": "underline"}}},
    {"id": "ggbtn", "name": "gg-btn", "settings": {
        "_width:mobile_portrait": "100%", "_justifyContent:mobile_portrait": "center"}},
    {"id": "ggh", "name": "gg-h", "settings": {
        "_typography": {"text-wrap": "balance"}}},
]
NAME2ID = {c["name"]: c["id"] for c in global_classes}
def _remap(names):
    return [NAME2ID.get(n, n) for n in names]

# ============================================================================
# DATA
# ============================================================================
ACCESSORIES = [
    ("Clubfaces", "€52", f"{SHOP}/putters/clubfaces/", "52.00", "ti-layers",
     "Clubfaces are interchangeable face inserts that set the loft and feel of your putter.",
     "Available from 1° to 3°. Compatible with both Antares and Orion."),
    ("Extra Weights", "€21", f"{SHOP}/putters/extra-weights/", "21.00", "ti-control-shuffle",
     "Extra weights are swappable head weights for the 3-position weighting system.",
     "Light 1.19 oz, medium 1.48 oz, heavy 1.97 oz — bullet or flat."),
    ("Putter Cover", "€32", f"{SHOP}/putters/putter-covers/", "32.00", "ti-shield",
     "A putter cover is a protective headcover that shields the milled head from impacts and scratches.",
     "Tailored to the GG head shape."),
    ("Spare Parts Kit", "€149", f"{SHOP}/putters/spare-parts-kit/", "149.00", "ti-package",
     "The spare parts kit is a set of replacement components to keep your putter game-ready.",
     "Includes screws, weights and hardware."),
    ("Torque Wrench", "€63", f"{SHOP}/putters/torque-wrench/", "63.00", "ti-wand",
     "The torque wrench is a precision tool to tighten weights and faces to the correct spec.",
     "Ensures repeatable, secure adjustments."),
]

HOWTO = [
    ("Loosen the weight screws",
     "Loosen the three weight screws using the GG torque wrench."),
    ("Position the three weights",
     "Place the weights across the three points to match your stroke arc — light 1.19 oz, medium 1.48 oz, heavy 1.97 oz."),
    ("Set loft and feel",
     "Swap the clubface insert (1°–3°) to dial in your preferred loft and feel."),
    ("Tighten to spec",
     "Tighten everything back to the correct torque with the wrench."),
]

FAQ = [
    ("Are GG Putters accessories compatible with both Antares and Orion?",
     "Yes. GG Putters use a modular system, so weights, clubfaces and necks fit both the Antares blade and the Orion mallet."),
    ("What weights are available and how heavy are they?",
     "Three weights are available — light 1.19 oz, medium 1.48 oz and heavy 1.97 oz — in bullet or flat shape, priced at €21."),
    ("What clubface lofts can I choose?",
     "Interchangeable clubfaces are available from 1° to 3° and cost €52, letting you tune loft and feel."),
    ("Do I need the torque wrench to change weights or faces?",
     "It is recommended: the GG torque wrench (€63) sets every weight and face to the correct, repeatable torque spec."),
    ("What is included in the Spare Parts Kit?",
     "The Spare Parts Kit (€149) includes replacement screws, weights and hardware to keep your putter game-ready."),
    ("What's inside the Fitter Kit?",
     "The Fitter Kit contains 2 heads (one Antares and one Orion), 3 lofts (1°, 2°, 3°), a weights kit (2 heavy + 2 light), necks (lie and offset), plus screws and a hex screwdriver."),
    ("How much do GG Putters accessories cost?",
     "Accessories range from €21 (extra weights) to €149 (spare parts kit); clubfaces €52, putter cover €32, torque wrench €63."),
]

# ============================================================================
# CONTENT
# ============================================================================
# 1. HEAD / HERO
hero = section(css_id="top", label="Head / Hero", children=[
    container(children=[
        El("block", cls("gg-header"), children=[
            eyebrow("Accessories &amp; Fitter Kit"),
            heading("GG Putters Accessories, Spare Parts &amp; Fitter Kit", "h1",
                    classes=["gg-h"], label="H1"),
            para("Customize and maintain your GG putter with milled accessories — interchangeable clubfaces, adjustable weights, covers and tools — priced from €21 to €149 and compatible with both Antares and Orion.",
                 classes=["gg-lead"]),
            El("block", cls("gg-cta-row"), children=[
                button("Shop Accessories", PAGE_URL, aria="Shop GG Putters accessories"),
                button("Request the Fitter Kit", f"{SHOP}/for-fitters/", aria="Request the GG Putters Fitter Kit"),
            ], label="Hero CTAs"),
        ], label="Hero Content"),
    ]),
])

# 2. ACCESSORIES GRID
def acc_card(name, price, url, ti, definition, data):
    return col([
        icon(ti),
        heading(name, "h3", classes=["gg-h"]),
        para(price),
        para(definition),
        para(data),
        text_link("View product", url, label=f"View {name}"),
    ], label=f"Accessory: {name}")

accessories = section(css_id="accessories", label="Accessories", children=[
    container(children=[
        header_block("Optional accessories", "Accessories &amp; Spare Parts",
                     "Every accessory is milled to match the GG system. Quick guide: clubfaces set loft, weights set balance, the wrench sets everything to spec."),
        row([acc_card(n, p, u, ti, d, data) for (n, p, u, _pr, ti, d, data) in ACCESSORIES],
            label="Accessories Grid"),
    ]),
])

# 3. COMPATIBILITY / TRUST BAND
def trust_item(ti, title, text):
    return col([icon(ti), heading(title, "h3", classes=["gg-h"]), para(text)],
               label=f"Trust: {title}")

trust = section(label="Compatibility band", children=[
    container(children=[
        row([
            trust_item("ti-check-box", "Fits Antares &amp; Orion",
                       "All accessories are compatible with both GG putter models."),
            trust_item("ti-settings", "Set to spec",
                       "Use the torque wrench for repeatable, secure adjustments."),
            trust_item("ti-shield", "2-year warranty",
                       "GG products are covered against conformity defects."),
            trust_item("ti-truck", "Fast shipping",
                       "BRT in Italy, FedEx worldwide — within 5–6 business days."),
        ]),
    ]),
])

# 4. HOW TO (customize)
howto = section(css_id="setup", label="How to", children=[
    container(children=[
        header_block("Setup guide", "How to customize your GG putter",
                     "In four steps you can rebalance the head and change the face — no specialist tools beyond the GG torque wrench."),
        El("block", {"_cssGlobalClasses": ["gg-col"], "_widthMax": "760px",
                     "_margin": {"left": "auto", "right": "auto"}, "_rowGap": "0.5rem"},
           children=[rich(
               "<ol>" + "".join(f"<li><strong>{t}.</strong> {d}</li>" for t, d in HOWTO) + "</ol>",
               label="Steps")], label="HowTo Steps"),
    ]),
])

# 5. FITTER KIT
fitter = section(css_id="fitters", label="Fitter Kit", children=[
    container(children=[
        row([
            col([
                eyebrow("For fitters"),
                heading("The GG Putters Fitter Kit", "h2", classes=["gg-h"]),
                para("The Fitter Kit is a modular fitting system that lets professionals test every putter configuration with a client in a single session."),
                para("Handcrafted in Italy and fully modular — from head shape to insert, feel and balance — so each player leaves with a putter that is uniquely theirs."),
                El("block", cls("gg-cta-row"), children=[
                    button("Request the Fitter Kit", f"{SHOP}/for-fitters/", aria="Request the Fitter Kit"),
                ], label="Fitter CTA"),
            ], wide=True, label="Fitter Text"),
            col([
                heading("What's inside the Fitter Kit", "h3", classes=["gg-h"]),
                rich("<ul><li>2 heads — one Antares and one Orion</li><li>3 lofts (1°, 2°, 3°)</li><li>Weights kit — 2 heavy and 2 light (bullet or flat)</li><li>Necks (lie and offset)</li><li>Screws and hex screwdriver</li></ul>",
                     label="Kit list"),
            ], wide=True, label="Fitter Kit List"),
        ]),
    ]),
])

# 6. FAQ
faq = section(css_id="faq", label="FAQ", children=[
    container(children=[
        header_block("FAQ", "Accessories &amp; Fitter Kit — FAQ",
                     "Quick answers about compatibility, weights, lofts, tools, pricing and the Fitter Kit."),
        El("block", {"_cssGlobalClasses": ["gg-col"], "_widthMax": "780px",
                     "_margin": {"left": "auto", "right": "auto"}, "_rowGap": "1.5rem"},
           children=[El("block", cls("gg-col"), children=[
               heading(q, "h3", classes=["gg-h"]), para(a)], label=f"FAQ: {q[:22]}")
               for q, a in FAQ], label="FAQ List"),
    ]),
])

# 7. CONTACT / CTA
contact = section(css_id="contact", label="Contact", children=[
    container(children=[
        El("block", cls("gg-header"), children=[
            eyebrow("Need help choosing?"),
            heading("Talk to the GG Putters team", "h2", classes=["gg-h"]),
            para("Not sure which weights or face you need? Our team in Brescia will help you set up your putter.",
                 classes=["gg-lead"]),
            El("block", cls("gg-cta-row"), children=[
                text_link("info@ggputters.com", "mailto:info@ggputters.com", label="Email"),
                text_link("+39 331 1099739", "tel:+393311099739", label="Phone"),
            ], label="Contact links"),
        ], label="Contact Content"),
    ]),
])

# 8. FOOTER
footer = section(label="Footer", children=[
    container(children=[
        El("block", cls("gg-header"), children=[
            heading("GG Putters", "p", classes=["gg-eyebrow"], label="Brand"),
            para("Italian craft, Brescia engineering. Putters with a metalworking soul."),
            para("GG PUTTERS is a brand of GM PRODUCTION srl · VAT IT03351530989 · Palazzolo sull'Oglio (BS), Italy"),
            para("© 2026 GG Putters. All rights reserved."),
        ], label="Footer Content"),
    ]),
])

roots = [hero, accessories, trust, howto, fitter, faq, contact, footer]
for r in roots:
    flatten(r, 0)

# Normalize class names -> ids
for node in elements:
    g = node["settings"].get("_cssGlobalClasses")
    if g:
        node["settings"]["_cssGlobalClasses"] = _remap(g)

# ----------------------------------------------------------------------------
# SAFETY SANITIZER — no colors, no paint, no font-family
# ----------------------------------------------------------------------------
PAINT_KEYS = ("_background", "_border", "_boxShadow", "_gradient", "_cssFilters")
TYPO_DROP = ("color", "background-color", "border-color", "font-family",
             "text-shadow", "-webkit-text-fill-color")

def sanitize(settings):
    for k in list(settings.keys()):
        if k.startswith(("_background", "_border", "_boxShadow", "_gradient")) or k in PAINT_KEYS:
            del settings[k]
            continue
        if k == "_typography" or k.startswith("_typography:"):
            typo = settings[k]
            if isinstance(typo, dict):
                for dk in TYPO_DROP:
                    typo.pop(dk, None)
                if not typo:
                    del settings[k]

for node in elements:
    sanitize(node["settings"])
for c in global_classes:
    sanitize(c["settings"])

# ----------------------------------------------------------------------------
# HEAD: SEO meta + Open Graph/Twitter + JSON-LD (Breadcrumb, Products, HowTo,
# FAQPage). Injected into the document <head> via customScriptsHeader.
# ----------------------------------------------------------------------------
PAGE_TITLE = "Putter Accessories, Spare Parts & Fitter Kit | GG Putters"
PAGE_DESC = ("GG Putters accessories: interchangeable clubfaces (1°–3°), adjustable weights "
             "(1.19–1.97 oz), covers, spare parts and the torque wrench, from €21 to €149. "
             "Compatible with Antares and Orion. Professional Fitter Kit available.")
OG_IMAGE = f"{SHOP}/wp-content/uploads/gg-accessories-og.jpg"  # replace with a real image

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
     "name": PAGE_TITLE, "description": PAGE_DESC,
     "isPartOf": {"@id": f"{SHOP}/#organization"}},
    {"@type": "ItemList", "name": "GG Putters Accessories",
     "itemListElement": [
        {"@type": "ListItem", "position": i + 1,
         "item": product_ld(n, f"{d} {data}", pr, u)}
        for i, (n, _p, u, pr, _ti, d, data) in enumerate(ACCESSORIES)]},
    {"@type": "Product", "name": "GG Putters Fitter Kit",
     "brand": {"@type": "Brand", "name": "GG Putters"},
     "category": "Golf Fitting Kit", "url": f"{SHOP}/for-fitters/",
     "description": "Modular fitting kit for professionals: 2 heads (Antares and Orion), 3 lofts (1°–3°), weights kit, necks (lie/offset) and tools."},
    {"@type": "HowTo", "name": "How to customize your GG putter",
     "description": "Rebalance the head and change the face of a GG putter using the torque wrench, weights and clubfaces.",
     "tool": [{"@type": "HowToTool", "name": "GG torque wrench"}],
     "supply": [{"@type": "HowToSupply", "name": "GG weights (1.19/1.48/1.97 oz)"},
                 {"@type": "HowToSupply", "name": "GG clubfaces (1°–3°)"}],
     "step": [{"@type": "HowToStep", "position": i + 1, "name": t, "text": d}
              for i, (t, d) in enumerate(HOWTO)]},
    {"@type": "FAQPage", "@id": f"{PAGE_URL}#faq",
     "mainEntity": [{"@type": "Question", "name": q,
                      "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ]},
]
json_ld = {"@context": "https://schema.org", "@graph": graph}

head_meta = (
    f'<link rel="canonical" href="{PAGE_URL}">'
    '<meta name="robots" content="index,follow,max-image-preview:large">'
    f'<meta name="description" content="{PAGE_DESC}">'
    '<meta property="og:type" content="website">'
    '<meta property="og:site_name" content="GG Putters">'
    f'<meta property="og:title" content="{PAGE_TITLE}">'
    f'<meta property="og:description" content="{PAGE_DESC}">'
    f'<meta property="og:url" content="{PAGE_URL}">'
    f'<meta property="og:image" content="{OG_IMAGE}">'
    '<meta property="og:locale" content="en_US">'
    '<meta name="twitter:card" content="summary_large_image">'
    f'<meta name="twitter:title" content="{PAGE_TITLE}">'
    f'<meta name="twitter:description" content="{PAGE_DESC}">'
    f'<meta name="twitter:image" content="{OG_IMAGE}">'
)
head = head_meta + '<script type="application/ld+json">' + json.dumps(json_ld, ensure_ascii=False) + '</script>'

# Minimal accessibility CSS only — no colors.
custom_css = (
    ":where(a,button,input,textarea,select,summary,[tabindex]):focus-visible"
    "{outline:3px solid currentColor;outline-offset:3px;}"
    "[id]{scroll-margin-top:1.5rem;}"
    "img{max-width:100%;height:auto;}"
    "@media(prefers-reduced-motion:reduce){*,*::before,*::after"
    "{animation-duration:.01ms!important;transition-duration:.01ms!important;scroll-behavior:auto!important;}}"
)

page_settings = {
    "pageTitle": PAGE_TITLE,
    "metaDescription": PAGE_DESC,
    "customCss": custom_css,
    "customScriptsHeader": head,
}

template = {
    "name": "gg-accessories-page",
    "title": "GG Putters — Accessories & Fitter Kit",
    "type": "content",
    "content": elements,
    "pageSettings": page_settings,
    "templateSettings": {"templateConditions": [{"main": "any"}]},
    "global_classes": global_classes,
    "globalElements": [],
    "globalVariables": [],
    "globalVariablesCategories": [],
    "version": "2.3.6",
}

with open("gg-accessories-page.json", "w", encoding="utf-8") as f:
    json.dump(template, f, ensure_ascii=False, indent=2)

print(f"Generated {len(elements)} elements, {len(global_classes)} classes, "
      f"{len(ACCESSORIES)} accessories, {len(HOWTO)} steps, {len(FAQ)} FAQ.")
