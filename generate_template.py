#!/usr/bin/env python3
"""Generate a Bricks Builder 2.3.6 template-export JSON for the GG Putters
landing page.

Design goals (per feedback):
- NO colors anywhere — the site's theme styles own all colors and typography.
- Fully fluid responsive layout built ONLY with Flexbox (wrap + flex-basis),
  no fragile media-query breakpoints.
- Minimal, reusable global classes; almost no inline styling.
- Accessibility kept (semantic headings, alt text, aria-hidden icons,
  aria-labels, keyboard focus, reduced-motion).
Run: python3 generate_template.py  ->  gg-putters-landing.json
"""
import json

SHOP = "https://shop.ggputters.com"

# ----------------------------------------------------------------------------
# ID helpers
# ----------------------------------------------------------------------------
_counter = 0
def nid():
    global _counter
    _counter += 1
    return f"e{_counter:05d}"

_attr = 0
def attr_id():
    global _attr
    _attr += 1
    return f"a{_attr:05d}"

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
# Element builders (layout-only settings, no colors)
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

def row(children, classes=None, label=None):
    return El("block", cls(*(["gg-row"] + (classes or []))), children=children, label=label or "Row")

def col(children, wide=False, label=None):
    return El("block", cls("gg-col-wide" if wide else "gg-col"), children=children,
              label=label or "Column")

# ----------------------------------------------------------------------------
# Global classes — layout only, fluid, NO colors
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
    {"id": "gglead", "name": "gg-lead", "settings": {
        "_widthMax": "65ch"}},
    {"id": "ggimg", "name": "gg-img", "settings": {
        "_width": "100%"}},
    {"id": "gglink", "name": "gg-link", "settings": {
        "_typography": {"text-decoration": "underline"}}},
    {"id": "ggbtn", "name": "gg-btn", "settings": {
        "_width:mobile_portrait": "100%", "_justifyContent:mobile_portrait": "center"}},
    {"id": "ggh", "name": "gg-h", "settings": {
        "_typography": {"text-wrap": "balance"}}},
]

# Note on classes: real names live in `name`; elements reference them by id via
# `_cssGlobalClasses`. Map helper for readability.
NAME2ID = {c["name"]: c["id"] for c in global_classes}
def _remap(names):
    return [NAME2ID.get(n, n) for n in names]

# ============================================================================
# CONTENT
# ============================================================================
# 1. HERO
hero = section(css_id="top", label="Hero", children=[
    container(children=[
        El("block", cls("gg-header"), children=[
            eyebrow("GG Putters · Made in Italy"),
            heading("Custom Milled Putters — Antares &amp; Orion, Handcrafted in Italy", "h1",
                    classes=["gg-h"], label="H1"),
            para("Light years ahead. Designed to win.", classes=["gg-lead"], label="Tagline"),
            para("GG Putters are precision golf putters milled from a single block of aluminum and steel in Brescia, Italy, with a 3-position adjustable weight system and interchangeable faces for a straighter, more confident roll.",
                 classes=["gg-lead"]),
            El("block", cls("gg-cta-row"), children=[
                button("Shop Putters", f"{SHOP}/putters/", aria="Shop GG Putters"),
                button("Download 2025 Catalog", f"{SHOP}/", aria="Download the GG Putters 2025 catalog"),
            ], label="Hero CTAs"),
        ], label="Hero Content"),
    ]),
])

# 2. FEATURES
def feature(ti, title, definition, body):
    return col([icon(ti), heading(title, "h3", classes=["gg-h"]),
                para(definition), para(body)], label=f"Feature: {title}")

features = section(css_id="features", label="Features", children=[
    container(children=[
        header_block("Performance by design", "Why players choose our putters",
                     "Billet milling, adjustable weighting and interchangeable faces combine for a cleaner, more repeatable stroke."),
        row([
            feature("ti-ruler-pencil", "Milled from a single block",
                    "A milled putter is machined from one solid metal block for tighter tolerances and a more consistent face.",
                    "Each head is milled from a single billet of aluminum with steel components, worked by turning and milling without heating to preserve elasticity and strength."),
            feature("ti-settings", "3-position adjustable weighting",
                    "An adjustable weighting system lets you reposition the three head weights to match your stroke arc.",
                    "Move the three weights across three dedicated points; light and heavy options help compensate for stroke tendencies."),
            feature("ti-layers", "Interchangeable faces &amp; necks",
                    "Interchangeable face inserts and necks let you tune feel, loft and alignment without changing putter.",
                    "Choose clubfaces from 1° to 3° and necks with different lie and offset for any green speed."),
        ]),
    ]),
])

# 3. MODELS / SHOP
def model(name, model_type, definition, price, url, specs):
    spec_items = "".join(f"<li>{s}</li>" for s in specs)
    return col([
        image_ph(f"GG {name} {model_type.lower()} putter, milled in Italy"),
        heading(name, "h3", classes=["gg-h"]),
        para(f"{model_type} · {price} (clubhead only €285)"),
        para(definition),
        rich(f"<ul>{spec_items}</ul>", label="Specs"),
        button(f"View {name}", url, aria=f"View the GG {name} putter"),
    ], label=f"Model: {name}")

models = section(css_id="shop", label="Models / Shop", children=[
    container(children=[
        header_block("Our products", "Choose your putter: Antares or Orion",
                     "Two milled putters, both €353: the Antares blade for feel and arc strokes, the Orion mallet for stability and higher forgiveness."),
        row([
            model("Antares", "Blade Putter",
                  "The Antares is a blade putter for golfers who favour feel and an arc-style stroke.",
                  "€353", f"{SHOP}/putters/antares/",
                  ["Milled aluminum + steel head", "3-position adjustable weights",
                   "Interchangeable faces 1°–3°", "Lie &amp; offset necks available"]),
            model("Orion", "Mallet Putter",
                  "The Orion is a mallet putter engineered for stability and higher forgiveness (MOI).",
                  "€353", f"{SHOP}/putters/orion/",
                  ["Milled aluminum + steel head", "3-position adjustable weights",
                   "Interchangeable faces 1°–3°", "Straighter, immediate roll"]),
        ]),
    ]),
])

# 4. ABOUT
about = section(css_id="about", label="About", children=[
    container(children=[
        row([
            col([
                eyebrow("About us"),
                heading("Italian Craft, Brescia Engineering — Made in Italy, Game-Ready", "h2",
                        classes=["gg-h"]),
                para("GG Putters is a golf brand by GM PRODUCTION srl, born in a garage in the 1980s in the Oglio river valley near Brescia, Italy — a region with a centuries-old metalworking tradition."),
                para("Every putter is milled in-house from premium materials, turned and milled without heating to preserve the metal's original elasticity and strength — a genuinely unique, fully customizable product."),
            ], wide=True, label="About Text"),
            col([image_ph("GG Putters CNC milling in the Brescia workshop, Italy", ratio="4/5")],
                wide=True, label="About Image"),
        ]),
    ]),
])

# 5. ACCESSORIES
def acc(name, price, desc):
    return col([heading(name, "h3", classes=["gg-h"]), para(price), para(desc)],
               label=f"Accessory: {name}")

accessories = section(css_id="accessories", label="Accessories", children=[
    container(children=[
        header_block("Optional accessories", "Accessories &amp; Spare Parts",
                     "Make your putter unique: weights, clubfaces, covers and tools, priced from €21 to €149."),
        row([
            acc("Clubfaces 1°–3°", "€52", "Interchangeable face inserts to tune loft and feel."),
            acc("Extra Weights", "€21", "Heavy &amp; light weights for the 3-position system."),
            acc("Putter Cover", "€32", "Protective headcover for your GG putter."),
            acc("Spare Parts Kit", "€149", "Replacement components to keep your putter game-ready."),
            acc("Torque Wrench", "€63", "Precision tool to set weights and faces correctly."),
        ]),
        El("block", cls("gg-cta-row"), children=[
            button("Shop All Accessories", f"{SHOP}/accessories/", aria="Shop all accessories"),
        ], label="Accessories CTA"),
    ]),
])

# 6. TRUST
def trust_item(ti, title, text):
    return col([icon(ti), heading(title, "h3", classes=["gg-h"]), para(text)],
               label=f"Trust: {title}")

trust = section(label="Trust", children=[
    container(children=[
        row([
            trust_item("ti-truck", "Worldwide shipping",
                       "BRT in Italy, FedEx worldwide — shipped within 5–6 business days."),
            trust_item("ti-shield", "2-year warranty", "Covered against conformity defects and failures."),
            trust_item("ti-reload", "14-day returns", "Right of withdrawal within 14 days; refund within 30 days."),
            trust_item("ti-credit-card", "Secure payments", "Visa, Mastercard, Amex, PayPal &amp; Klarna. Prices include VAT."),
        ]),
    ]),
])

# 7. FITTER KIT
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

# 8. FAQ
faq_items = [
    ("What makes GG Putters different from other putters?",
     "GG Putters are milled in Brescia, Italy from a single block of aluminum and steel, with a 3-position adjustable weight system and interchangeable faces (1°–3°) and necks for full customization."),
    ("Should I choose the Antares or the Orion?",
     "Choose the Antares blade if you favour feel and an arc stroke; choose the Orion mallet for higher stability and forgiveness. Both are priced at €353."),
    ("Are GG Putters customizable?",
     "Yes. You can adjust the three weights, swap clubfaces from 1° to 3°, and change necks (lie and offset) to match your stroke."),
    ("How much does a GG Putter cost?",
     "A full GG Putter costs €353; the clubhead-only version is €285. Accessories range from €21 (extra weights) to €149 (spare parts kit)."),
    ("Where are GG Putters made and what warranty applies?",
     "GG Putters are made in Palazzolo sull'Oglio (Brescia), Italy by GM PRODUCTION srl, milled without heating, and covered by a 2-year warranty; orders ship within 5–6 business days."),
    ("How can I pay and how is my order shipped?",
     "You can pay by credit card (Visa, Mastercard, American Express), PayPal or Klarna; prices include VAT. Orders ship with BRT in Italy and FedEx worldwide, usually within 5–6 business days."),
    ("Can I return a GG Putter?",
     "Yes. You can exercise the right of withdrawal within 14 days of receipt; once the returned product is verified, the refund is issued within 30 days."),
]

faq = section(css_id="faq", label="FAQ", children=[
    container(children=[
        header_block("FAQ", "Frequently Asked Questions",
                     "Quick answers about models, customization, pricing, shipping and returns."),
        El("block", {"_cssGlobalClasses": ["gg-col"], "_widthMax": "780px",
                     "_margin": {"left": "auto", "right": "auto"}, "_rowGap": "1.5rem"},
           children=[El("block", cls("gg-col"), children=[
               heading(q, "h3", classes=["gg-h"]), para(a)], label=f"FAQ: {q[:22]}")
               for q, a in faq_items], label="FAQ List"),
    ]),
])

# 9. CONTACT
def contact_card(title, links):
    kids = [heading(title, "h3", classes=["gg-h"])]
    kids += [text_link(v, h, label=k) for k, v, h in links]
    return col(kids, label=f"Contact: {title}")

contact = section(css_id="contact", label="Contact", children=[
    container(children=[
        header_block("Get in touch", "Contact Us",
                     "Questions about a build, an order or a partnership? Our team in Brescia is here to help."),
        row([
            contact_card("Info &amp; Sales", [("Email", "info@ggputters.com", "mailto:info@ggputters.com"),
                                              ("Phone", "+39 331 1099739", "tel:+393311099739")]),
            contact_card("Office &amp; Dealers", [("Email", "office@ggputters.com", "mailto:office@ggputters.com")]),
            contact_card("Headquarters", [("Address", "Palazzolo sull'Oglio (BS), Italy", f"{SHOP}/contact/")]),
        ]),
    ]),
])

# 10. NEWSLETTER
newsletter = section(css_id="newsletter", label="Newsletter", children=[
    container(children=[
        El("block", cls("gg-header"), children=[
            eyebrow("Stay in the loop"),
            heading("Join the Newsletter", "h2", classes=["gg-h"]),
            para("Be the first to hear about new releases, limited editions and craftsmanship stories.",
                 classes=["gg-lead"]),
            El("form", {
                "fields": [{"type": "email", "label": "Email",
                            "placeholder": "Enter your email address",
                            "required": True, "id": "newslttr", "width": "100"}],
                "showLabels": True, "submitButtonText": "Subscribe", "actions": ["email"],
                "emailSubject": "New newsletter subscription — GG Putters",
                "emailTo": "info@ggputters.com", "emailFromName": "GG Putters Website",
                "successMessage": "Thank you for subscribing!",
                "_width": "100%", "_widthMax": "480px"}, label="Newsletter Form"),
        ], label="Newsletter Content"),
    ]),
])

# 11. FOOTER
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

roots = [hero, features, models, about, accessories, trust, fitter, faq,
         contact, newsletter, footer]
for r in roots:
    flatten(r, 0)

# ----------------------------------------------------------------------------
# Remap class names -> ids in element settings (we authored using ids already,
# but eyebrow/gg-h etc. were passed by NAME in `classes=[...]`). Normalize all
# `_cssGlobalClasses` entries to ids.
# ----------------------------------------------------------------------------
for node in elements:
    g = node["settings"].get("_cssGlobalClasses")
    if g:
        node["settings"]["_cssGlobalClasses"] = _remap(g)

# ----------------------------------------------------------------------------
# SAFETY SANITIZER — guarantee: no colors, no decorative paint, no font-family.
# Removes background/border/box-shadow/gradient/filter entirely and strips
# color-ish + font-family keys from every _typography* object.
# ----------------------------------------------------------------------------
PAINT_KEYS = ("_background", "_border", "_boxShadow", "_gradient", "_cssFilters",
              "_backgroundColor", "_borderColor")
TYPO_DROP = ("color", "background-color", "border-color", "font-family",
             "text-shadow", "-webkit-text-fill-color")

def sanitize(settings):
    for k in list(settings.keys()):
        if k in PAINT_KEYS or k.startswith(("_background", "_border", "_boxShadow", "_gradient")):
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
# Page settings: SEO meta + minimal a11y CSS + JSON-LD (no colors in CSS)
# ----------------------------------------------------------------------------
def product(name, desc, price, url, rich_offer=False):
    offer = {"@type": "Offer", "price": price, "priceCurrency": "EUR",
             "availability": "https://schema.org/InStock", "url": url,
             "priceValidUntil": "2026-12-31"}
    if rich_offer:
        offer["shippingDetails"] = {"@type": "OfferShippingDetails",
            "shippingDestination": {"@type": "DefinedRegion", "addressCountry": "IT"},
            "deliveryTime": {"@type": "ShippingDeliveryTime",
                "handlingTime": {"@type": "QuantitativeValue", "minValue": 5, "maxValue": 6,
                                  "unitCode": "DAY"}}}
        offer["hasMerchantReturnPolicy"] = {"@type": "MerchantReturnPolicy",
            "applicableCountry": "IT",
            "returnPolicyCategory": "https://schema.org/MerchantReturnFiniteReturnWindow",
            "merchantReturnDays": 14, "returnMethod": "https://schema.org/ReturnByMail",
            "refundType": "https://schema.org/FullRefund"}
    return {"@type": "Product", "name": f"GG {name}",
            "brand": {"@type": "Brand", "name": "GG Putters"}, "category": "Golf Putter",
            "material": "Aluminum, Steel", "description": desc, "url": url, "offers": offer}

graph = [
    {"@type": "Organization", "@id": f"{SHOP}/#organization", "name": "GG Putters",
     "legalName": "GM PRODUCTION srl", "url": f"{SHOP}/",
     "description": "Handcrafted, CNC-milled custom golf putters made in Brescia, Italy.",
     "email": "info@ggputters.com", "telephone": "+39 331 1099739", "vatID": "IT03351530989",
     "address": {"@type": "PostalAddress", "streetAddress": "Via Taranto, 7",
                  "addressLocality": "Palazzolo sull'Oglio", "addressRegion": "BS",
                  "postalCode": "25036", "addressCountry": "IT"}},
    {"@type": "WebSite", "@id": f"{SHOP}/#website", "url": f"{SHOP}/", "name": "GG Putters",
     "publisher": {"@id": f"{SHOP}/#organization"}},
    product("Antares", "Milled blade putter for feel and arc strokes, with a 3-position adjustable weight system.", "353.00", f"{SHOP}/putters/antares/", rich_offer=True),
    product("Orion", "Milled mallet putter engineered for stability and higher forgiveness (MOI).", "353.00", f"{SHOP}/putters/orion/", rich_offer=True),
    product("Clubfaces", "Interchangeable face inserts (1°–3°) to tune loft and feel.", "52.00", f"{SHOP}/putters/clubfaces/"),
    product("Extra Weights", "Heavy and light weights for the 3-position weighting system.", "21.00", f"{SHOP}/putters/extra-weights/"),
    {"@type": "FAQPage", "@id": f"{SHOP}/#faq",
     "mainEntity": [{"@type": "Question", "name": q,
                      "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq_items]},
]
json_ld = {"@context": "https://schema.org", "@graph": graph}

# Minimal accessibility CSS only — no colors (focus uses currentColor).
custom_css = (
    ":where(a,button,input,textarea,select,summary,[tabindex]):focus-visible"
    "{outline:3px solid currentColor;outline-offset:3px;}"
    "[id]{scroll-margin-top:1.5rem;}"
    "img{max-width:100%;height:auto;}"
    "@media(prefers-reduced-motion:reduce){*,*::before,*::after"
    "{animation-duration:.01ms!important;transition-duration:.01ms!important;scroll-behavior:auto!important;}}"
)

page_settings = {
    "pageTitle": "Custom Milled Putters Made in Italy | Antares &amp; Orion — GG Putters",
    "metaDescription": "GG Putters: custom milled golf putters made in Brescia, Italy. Antares blade and Orion mallet from €353, 3-position adjustable weights and interchangeable faces.",
    "customCss": custom_css,
    "customScriptsBodyFooter": '<script type="application/ld+json">' + json.dumps(json_ld, ensure_ascii=False) + '</script>',
}

template = {
    "name": "gg-putters-landing",
    "title": "GG Putters — Landing Page",
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

with open("gg-putters-landing.json", "w", encoding="utf-8") as f:
    json.dump(template, f, ensure_ascii=False, indent=2)

print(f"Generated {len(elements)} elements, {len(global_classes)} global classes, {len(faq_items)} FAQ.")
