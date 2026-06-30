#!/usr/bin/env python3
"""Generate a Bricks Builder 2.3.6 template-export JSON for the GG Putters
GEO/SEO-optimized landing page. Run: python3 generate_template.py
Content is sourced from the official shop.ggputters.com extraction and follows
the GEO "Regola d'Oro" (one-sentence definitions, concrete data, inverted
pyramid, AI-preferred formats: lists, comparison table, FAQ + JSON-LD schema).
"""
import json

# ----------------------------------------------------------------------------
# Design tokens (luxury / metalworking feel)
# ----------------------------------------------------------------------------
INK      = "#11110f"
CHARCOAL = "#1b1b18"
GOLD     = "#b8924f"
GOLD_LT  = "#d8b87a"
CREAM    = "#f7f4ed"
CREAM_AL = "#efe9db"
WHITE    = "#ffffff"
INK_TXT  = "#1c1b18"
MUTED    = "#5d5a52"
MUTED_D  = "#b6b1a5"

SERIF = "Playfair Display"
SANS  = "Inter"

SHOP = "https://shop.ggputters.com"

# ----------------------------------------------------------------------------
# ID generator
# ----------------------------------------------------------------------------
_counter = 0
def nid():
    global _counter
    _counter += 1
    return f"e{_counter:05d}"

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
# Element helpers
# ----------------------------------------------------------------------------
def heading(text, tag, settings=None, classes=None, label=None):
    s = {"text": text, "tag": tag}
    if classes:
        s["_cssGlobalClasses"] = classes
    if settings:
        s.update(settings)
    return El("heading", s, label=label or f"{tag}: {text[:24]}")

def para(text, settings=None, classes=None, label=None):
    s = {"text": text, "tag": "p"}
    if classes:
        s["_cssGlobalClasses"] = classes
    if settings:
        s.update(settings)
    return El("text-basic", s, label=label or "Paragraph")

def rich(text, settings=None, classes=None, label=None):
    s = {"text": text}
    if classes:
        s["_cssGlobalClasses"] = classes
    if settings:
        s.update(settings)
    return El("text", s, label=label or "Rich text")

def icon(ti, settings=None):
    s = {"icon": {"library": "themify", "icon": ti}}
    if settings:
        s.update(settings)
    return El("icon", s, label="Icon")

def button(text, url, classes, settings=None, new_tab=True, aria=None):
    link = {"type": "external", "url": url}
    if new_tab:
        link["newTab"] = True
    if aria:
        link["ariaLabel"] = aria
    s = {"text": text, "link": link, "_cssGlobalClasses": classes}
    if settings:
        s.update(settings)
    return El("button", s, label=f"Button: {text}")

def image_ph(alt, settings=None, label=None):
    s = {"image": {"url": "", "alt": alt}, "altText": alt}
    if settings:
        s.update(settings)
    return El("image", s, label=label or f"Image: {alt[:24]}")

def container(children, settings=None, label=None):
    s = {"_widthMax": "1180px"}
    if settings:
        s.update(settings)
    return El("container", s, children=children, label=label or "Container")

def block(children, settings=None, label=None, classes=None):
    s = {}
    if classes:
        s["_cssGlobalClasses"] = classes
    if settings:
        s.update(settings)
    return El("block", s, children=children, label=label or "Block")

def section(children, settings=None, label=None, css_id=None):
    s = {}
    if css_id:
        s["_cssId"] = css_id
    if settings:
        s.update(settings)
    return El("section", s, children=children, label=label or "Section")

def header_block(eyebrow, title, lead, on_dark=False, css=None):
    title_color = WHITE if on_dark else INK_TXT
    children = [heading(eyebrow, "div", classes=["ggeyeb"]),
                heading(title, "h2", classes=["gghttl"],
                        settings={"_typography": {"color": {"hex": title_color},
                                                   "text-align": "center"}})]
    if lead:
        lead_set = {"_typography": {"text-align": "center"},
                    "_margin": {"left": "auto", "right": "auto", "bottom": "52px"}}
        if on_dark:
            lead_set["_typography"]["color"] = {"hex": MUTED_D}
        children.append(para(lead, classes=["gglead"], settings=lead_set))
    return container(settings={"_display": "flex", "_direction": "column",
                               "_alignItems": "center"}, children=children,
                     label="Section Header")

# ----------------------------------------------------------------------------
# Global classes
# ----------------------------------------------------------------------------
global_classes = [
    {"id": "ggeyeb", "name": "gg-eyebrow", "settings": {
        "_display": "inline-block",
        "_typography": {"text-transform": "uppercase", "letter-spacing": "0.28em",
                         "font-size": "0.8rem", "font-weight": "600",
                         "font-family": SANS, "color": {"hex": GOLD}},
        "_margin": {"bottom": "18px"}}},
    {"id": "gghttl", "name": "gg-title", "settings": {
        "_typography": {"font-family": SERIF, "font-size": "clamp(2rem, 4vw, 3.1rem)",
                         "font-weight": "600", "line-height": "1.12"},
        "_margin": {"bottom": "22px"}}},
    {"id": "gglead", "name": "gg-lead", "settings": {
        "_typography": {"font-family": SANS, "font-size": "1.15rem",
                         "line-height": "1.75", "color": {"hex": MUTED}},
        "_widthMax": "680px"}},
    {"id": "ggbody", "name": "gg-body", "settings": {
        "_typography": {"font-family": SANS, "font-size": "1rem",
                         "line-height": "1.7", "color": {"hex": MUTED}},
        "_margin": {"bottom": "16px"}}},
    {"id": "ggdefn", "name": "gg-definition", "settings": {
        "_typography": {"font-family": SANS, "font-size": "1rem", "font-weight": "600",
                         "line-height": "1.6", "color": {"hex": INK_TXT}},
        "_margin": {"bottom": "12px"}}},
    {"id": "ggcard", "name": "gg-card", "settings": {
        "_background": {"color": {"hex": WHITE}},
        "_border": {"width": {"top": "1px", "right": "1px", "bottom": "1px", "left": "1px"},
                     "style": "solid", "color": {"rgb": "rgba(17,17,15,0.08)"},
                     "radius": {"top": "16px", "right": "16px", "bottom": "16px", "left": "16px"}},
        "_padding": {"top": "38px", "right": "32px", "bottom": "38px", "left": "32px"},
        "_boxShadow": {"values": {"offsetX": "0", "offsetY": "18", "blur": "40", "spread": "-24"},
                        "color": {"rgb": "rgba(17,17,15,0.18)"}},
        "_height": "100%", "_display": "flex", "_direction": "column"}},
    {"id": "gggrd3", "name": "gg-grid-3", "settings": {
        "_display": "grid", "_gridTemplateColumns": "repeat(3, minmax(0, 1fr))",
        "_gridGap": "28px",
        "_gridTemplateColumns:tablet_portrait": "repeat(2, minmax(0, 1fr))",
        "_gridTemplateColumns:mobile_portrait": "1fr"}},
    {"id": "gggrd2", "name": "gg-grid-2", "settings": {
        "_display": "grid", "_gridTemplateColumns": "repeat(2, minmax(0, 1fr))",
        "_gridGap": "48px", "_alignItemsGrid": "center",
        "_gridTemplateColumns:mobile_landscape": "1fr"}},
    {"id": "ggbtnp", "name": "gg-btn-primary", "settings": {
        "_background": {"color": {"hex": GOLD}},
        "_typography": {"font-family": SANS, "font-weight": "600", "font-size": "0.9rem",
                         "text-transform": "uppercase", "letter-spacing": "0.08em",
                         "color": {"hex": INK}},
        "_padding": {"top": "16px", "right": "32px", "bottom": "16px", "left": "32px"},
        "_border": {"radius": {"top": "8px", "right": "8px", "bottom": "8px", "left": "8px"}},
        "_cssTransition": "background-color 0.3s ease, transform 0.3s ease",
        "_background:hover": {"color": {"hex": GOLD_LT}},
        "_transform:hover": {"translateY": "-2"}}},
    {"id": "ggbtno", "name": "gg-btn-outline", "settings": {
        "_background": {"color": {"rgb": "rgba(0,0,0,0)"}},
        "_typography": {"font-family": SANS, "font-weight": "600", "font-size": "0.9rem",
                         "text-transform": "uppercase", "letter-spacing": "0.08em",
                         "color": {"hex": WHITE}},
        "_padding": {"top": "16px", "right": "32px", "bottom": "16px", "left": "32px"},
        "_border": {"width": {"top": "1px", "right": "1px", "bottom": "1px", "left": "1px"},
                     "style": "solid", "color": {"rgb": "rgba(255,255,255,0.45)"},
                     "radius": {"top": "8px", "right": "8px", "bottom": "8px", "left": "8px"}},
        "_cssTransition": "all 0.3s ease",
        "_background:hover": {"color": {"hex": GOLD}},
        "_border:hover": {"color": {"hex": GOLD}},
        "_typography:hover": {"color": {"hex": INK}}}},
    {"id": "ggfico", "name": "gg-feature-icon", "settings": {
        "_typography": {"font-size": "2rem", "color": {"hex": GOLD}},
        "_margin": {"bottom": "22px"}}},
    {"id": "ggclnk", "name": "gg-contact-link", "settings": {
        "_typography": {"font-family": SANS, "font-weight": "600", "color": {"hex": GOLD}},
        "_cssTransition": "color 0.25s ease",
        "_typography:hover": {"color": {"hex": GOLD_LT}}}},
    {"id": "ggprice", "name": "gg-price", "settings": {
        "_typography": {"font-family": SERIF, "font-size": "1.9rem", "font-weight": "600",
                         "color": {"hex": GOLD}}}},
]

# ----------------------------------------------------------------------------
# Section presets
# ----------------------------------------------------------------------------
def sec_pad():
    return {"_padding": {"top": "112px", "right": "24px", "bottom": "112px", "left": "24px"},
            "_padding:mobile_portrait": {"top": "68px", "right": "20px", "bottom": "68px", "left": "20px"}}

def dark_sec(bg=INK):
    s = {"_background": {"color": {"hex": bg}}}
    s.update(sec_pad())
    return s

def light_sec(bg=CREAM):
    s = {"_background": {"color": {"hex": bg}}}
    s.update(sec_pad())
    return s

# ============================================================================
# 1. HERO
# ============================================================================
hero = section(css_id="top", settings=dark_sec(INK), label="Hero", children=[
    container(settings={"_widthMax": "900px", "_display": "flex", "_direction": "column",
                         "_alignItems": "center"}, label="Hero Inner", children=[
        heading("GG Putters · Made in Italy", "div", classes=["ggeyeb"]),
        heading("Custom Milled Putters — Antares &amp; Orion, Handcrafted in Italy", "h1",
                classes=["gghttl"],
                settings={"_typography": {"font-family": SERIF, "color": {"hex": WHITE},
                                           "font-size": "clamp(2.4rem, 5vw, 3.9rem)",
                                           "font-weight": "600", "line-height": "1.08",
                                           "text-align": "center"},
                           "_margin": {"bottom": "20px"}}, label="H1"),
        heading("Light years ahead. Designed to win.", "div",
                settings={"_typography": {"font-family": SERIF, "font-style": "italic",
                                           "font-size": "1.4rem", "color": {"hex": GOLD_LT},
                                           "line-height": "1.4", "text-align": "center"},
                           "_margin": {"bottom": "26px"}}, label="Tagline"),
        para("GG Putters are precision golf putters milled from a single block of aluminum and steel in Brescia, Italy, featuring a 3-position adjustable weight system and interchangeable faces for a straighter, more confident roll.",
             classes=["gglead"],
             settings={"_typography": {"color": {"hex": MUTED_D}, "text-align": "center"},
                        "_margin": {"left": "auto", "right": "auto", "bottom": "38px"}}),
        block(settings={"_display": "flex", "_justifyContent": "center", "_gap": "16px",
                         "_flexWrap": "wrap"}, label="Hero CTAs", children=[
            button("Shop Putters", f"{SHOP}/putters/", ["ggbtnp"], aria="Shop GG Putters"),
            button("Download 2025 Catalog", f"{SHOP}/", ["ggbtno"], aria="Download the GG Putters 2025 catalog"),
        ]),
    ]),
])

# ============================================================================
# 2. FEATURES — definitions + concrete data
# ============================================================================
def feature_card(ti, title, definition, body):
    return block(classes=["ggcard"], children=[
        icon(ti, settings={"_cssGlobalClasses": ["ggfico"]}),
        heading(title, "h3", settings={
            "_typography": {"font-family": SERIF, "font-size": "1.4rem", "font-weight": "600",
                             "color": {"hex": INK_TXT}}, "_margin": {"bottom": "12px"}}),
        para(definition, classes=["ggdefn"]),
        para(body, classes=["ggbody"], settings={"_margin": {"bottom": "0px"}}),
    ], label=f"Feature: {title}")

features = section(css_id="features", settings=light_sec(CREAM), label="Features", children=[
    header_block("Performance by design", "Why players choose our putters",
                 "Three engineering choices — billet milling, adjustable weighting and interchangeable faces — combine to deliver a cleaner, more repeatable stroke."),
    block(classes=["gggrd3"], settings={"_widthMax": "1180px",
                                         "_margin": {"left": "auto", "right": "auto"}},
          label="Feature Grid", children=[
        feature_card("ti-ruler-pencil", "Milled from a single block",
                     "A milled putter is machined from one solid metal block for tighter tolerances and a more consistent face.",
                     "Each head is milled from a single billet of aluminum, combined with steel components and worked by turning and milling without heating to preserve the metal's natural elasticity and strength."),
        feature_card("ti-settings", "3-position adjustable weighting",
                     "An adjustable weighting system lets you reposition the three head weights to match your stroke arc and balance.",
                     "Move the three weights across three dedicated points to fine-tune the arc and balance — light and heavy options let you compensate for individual stroke tendencies."),
        feature_card("ti-layers", "Interchangeable faces &amp; necks",
                     "Interchangeable face inserts and necks let you tune feel, loft and alignment without changing putter.",
                     "Choose clubfaces from 1° to 3° and necks with different lie and offset to optimize feel and responsiveness for any green speed."),
    ]),
])

# ============================================================================
# 3. MODELS / SHOP — Antares & Orion (real products + prices)
# ============================================================================
def model_card(name, model_type, definition, price, ch_price, url, specs):
    spec_items = "".join(f"<li>{s}</li>" for s in specs)
    return block(classes=["ggcard"], children=[
        image_ph(f"GG {name} {model_type.lower()} putter, milled in Italy",
                 settings={"_border": {"radius": {"top": "12px", "right": "12px", "bottom": "12px", "left": "12px"}},
                            "_aspectRatio": "16/10", "_objectFit": "cover",
                            "_margin": {"bottom": "24px"}}),
        block(settings={"_display": "flex", "_justifyContent": "space-between",
                         "_alignItems": "baseline", "_gap": "12px", "_flexWrap": "wrap"}, children=[
            heading(name, "h3", settings={
                "_typography": {"font-family": SERIF, "font-size": "1.7rem", "font-weight": "600",
                                 "color": {"hex": INK_TXT}}}),
            heading(price, "div", classes=["ggprice"]),
        ], label="Title + Price"),
        heading(model_type, "div", settings={
            "_typography": {"font-family": SANS, "font-size": "0.8rem", "font-weight": "700",
                             "text-transform": "uppercase", "letter-spacing": "0.16em",
                             "color": {"hex": GOLD}}, "_margin": {"top": "4px", "bottom": "14px"}}),
        para(definition, classes=["ggdefn"]),
        rich(f"<ul>{spec_items}</ul>", classes=["ggbody"],
             settings={"_margin": {"bottom": "22px"}}, label="Specs"),
        para(f"Clubhead only available at {ch_price}.", classes=["ggbody"],
             settings={"_typography": {"font-size": "0.9rem", "color": {"hex": MUTED}},
                        "_margin": {"bottom": "24px"}}),
        block(settings={"_margin": {"top": "auto"}}, children=[
            button(f"View {name}", url, ["ggbtnp"],
                   settings={"_typography": {"color": {"hex": INK}}, "_width": "fit-content"},
                   aria=f"View the GG {name} putter"),
        ], label="Buy"),
    ], label=f"Model: {name}")

models = section(css_id="shop", settings=light_sec(WHITE), label="Models / Shop", children=[
    header_block("Our products", "Choose your putter: Antares or Orion",
                 "Two milled putters, both €353: the Antares blade for feel and the Orion mallet for stability. Clubhead-only options start at €285."),
    block(classes=["gggrd2"], settings={"_widthMax": "960px",
                                         "_margin": {"left": "auto", "right": "auto"},
                                         "_alignItemsGrid": "stretch"}, label="Models Grid", children=[
        model_card("Antares", "Blade Putter",
                   "The Antares is a blade putter for golfers who favour feel and an arc-style stroke.",
                   "€353", "€285", f"{SHOP}/putters/antares/",
                   ["Milled aluminum + steel head", "3-position adjustable weights",
                    "Interchangeable faces 1°–3°", "Lie &amp; offset necks available"]),
        model_card("Orion", "Mallet Putter",
                   "The Orion is a mallet putter engineered for stability and higher forgiveness (MOI).",
                   "€353", "€285", f"{SHOP}/putters/orion/",
                   ["Milled aluminum + steel head", "3-position adjustable weights",
                    "Interchangeable faces 1°–3°", "Straighter, immediate roll"]),
    ]),
])

# ============================================================================
# 4. COMPARISON TABLE — Antares vs Orion
# ============================================================================
def table_block(headers, rows):
    n = len(headers)
    cells = []
    for i, h in enumerate(headers):
        cells.append(heading(h, "div", settings={
            "_background": {"color": {"hex": INK}},
            "_typography": {"font-family": SANS, "font-size": "0.85rem", "font-weight": "700",
                             "text-transform": "uppercase", "letter-spacing": "0.08em",
                             "color": {"hex": GOLD_LT},
                             "text-align": "left" if i == 0 else "center"},
            "_padding": {"top": "16px", "right": "20px", "bottom": "16px", "left": "20px"}},
            label="TH"))
    for row in rows:
        for i, c in enumerate(row):
            cells.append(para(c, settings={
                "_typography": {"font-family": SANS, "font-size": "0.98rem",
                                 "color": {"hex": INK_TXT if i == 0 else MUTED},
                                 "font-weight": "600" if i == 0 else "400",
                                 "text-align": "left" if i == 0 else "center"},
                "_padding": {"top": "14px", "right": "20px", "bottom": "14px", "left": "20px"},
                "_border": {"width": {"bottom": "1px"}, "style": "solid",
                             "color": {"rgb": "rgba(17,17,15,0.08)"}},
                "_margin": {"bottom": "0px"}}, label="TD"))
    grid = block(children=cells, settings={
        "_display": "grid", "_gridTemplateColumns": "1.4fr 1fr 1fr",
        "_widthMin": "560px",
        "_background": {"color": {"hex": WHITE}},
        "_border": {"width": {"top": "1px", "right": "1px", "bottom": "1px", "left": "1px"},
                     "style": "solid", "color": {"rgb": "rgba(17,17,15,0.10)"},
                     "radius": {"top": "14px", "right": "14px", "bottom": "14px", "left": "14px"}},
        "_overflow": "hidden"}, label="Table Grid")
    return block(children=[grid], settings={"_overflow": "auto", "_widthMax": "860px",
                                             "_margin": {"left": "auto", "right": "auto"}},
                 label="Table Wrapper")

comparison = section(css_id="compare", settings=light_sec(CREAM_AL), label="Comparison", children=[
    header_block("Blade vs mallet", "Antares vs Orion: which putter is right for you?",
                 "Quick answer: choose the Antares blade for feel and arc strokes, the Orion mallet for stability and forgiveness. Both cost €353."),
    table_block(["Feature", "Antares (Blade)", "Orion (Mallet)"], [
        ["Head style", "Blade", "Mallet"],
        ["Forgiveness (MOI)", "Medium", "High"],
        ["Best for", "Feel &amp; arc stroke", "Stability &amp; straight stroke"],
        ["Weight system", "3 positions", "3 positions"],
        ["Full putter", "€353", "€353"],
        ["Clubhead only", "€285", "€285"],
    ]),
])

# ============================================================================
# 5. ABOUT — real story
# ============================================================================
about_text = block(children=[
    heading("About us", "div", classes=["ggeyeb"]),
    heading("Italian Craft, Brescia Engineering — Made in Italy, Game-Ready", "h2",
            classes=["gghttl"], settings={"_typography": {"color": {"hex": WHITE}}}),
    para("GG Putters is a golf brand by GM PRODUCTION srl, born in a garage in the 1980s in the Oglio river valley near Brescia, Italy — a region with a centuries-old metalworking tradition.",
         classes=["ggbody"], settings={"_typography": {"color": {"hex": MUTED_D}}}),
    para("Every putter is milled in-house from premium materials, turned and milled without heating to preserve the metal's original elasticity and strength. The fusion of decades of metalworking expertise and a love for golf gives life to a genuinely unique, fully customizable product.",
         classes=["ggbody"], settings={"_typography": {"color": {"hex": MUTED_D}}, "_margin": {"bottom": "0px"}}),
], label="About Text")
about_img = image_ph("GG Putters CNC milling in the Brescia workshop, Italy",
                     settings={"_border": {"radius": {"top": "16px", "right": "16px", "bottom": "16px", "left": "16px"}},
                                "_height": "100%", "_objectFit": "cover", "_aspectRatio": "4/5"},
                     label="About Image")

about = section(css_id="about", settings=dark_sec(CHARCOAL), label="About", children=[
    container(children=[
        block(classes=["gggrd2"], children=[about_text, about_img], label="About Grid"),
    ], label="About Inner"),
])

# ============================================================================
# 6. ACCESSORIES — real range + prices
# ============================================================================
def acc_card(name, price, desc):
    return block(classes=["ggcard"], settings={"_padding": {"top": "28px", "right": "26px",
                                                             "bottom": "28px", "left": "26px"}}, children=[
        block(settings={"_display": "flex", "_justifyContent": "space-between",
                         "_alignItems": "baseline", "_gap": "10px"}, children=[
            heading(name, "h3", settings={
                "_typography": {"font-family": SERIF, "font-size": "1.2rem", "font-weight": "600",
                                 "color": {"hex": INK_TXT}}}),
            heading(price, "div", settings={
                "_typography": {"font-family": SERIF, "font-size": "1.2rem", "font-weight": "600",
                                 "color": {"hex": GOLD}}}),
        ], label="Name + Price"),
        para(desc, classes=["ggbody"], settings={"_typography": {"font-size": "0.92rem"},
                                                  "_margin": {"top": "8px", "bottom": "0px"}}),
    ], label=f"Accessory: {name}")

accessories = section(css_id="accessories", settings=light_sec(CREAM), label="Accessories", children=[
    header_block("Optional accessories", "Accessories &amp; Spare Parts",
                 "Make your putter unique: extra weights, interchangeable clubfaces, covers and tools — priced from €21 to €149."),
    block(classes=["gggrd3"], settings={"_widthMax": "1080px",
                                         "_margin": {"left": "auto", "right": "auto", "bottom": "44px"}},
          label="Accessories Grid", children=[
        acc_card("Clubfaces 1°–3°", "€52", "Interchangeable face inserts to tune loft and feel."),
        acc_card("Extra Weights", "€21", "Heavy &amp; light weights for the 3-position system."),
        acc_card("Putter Cover", "€32", "Protective headcover for your GG putter."),
        acc_card("Spare Parts Kit", "€149", "Replacement components to keep your putter game-ready."),
        acc_card("Torque Wrench", "€63", "Precision tool to set weights and faces correctly."),
    ]),
    block(settings={"_display": "flex", "_justifyContent": "center"}, children=[
        button("Shop All Accessories", f"{SHOP}/accessories/", ["ggbtnp"],
               settings={"_typography": {"color": {"hex": INK}}}, aria="Shop all GG Putters accessories"),
    ], label="Accessories CTA"),
])

# ============================================================================
# 6b. TRUST BAND — shipping, warranty, returns, payments (transactional)
# ============================================================================
def trust_item(ti, title, text):
    return block(settings={"_display": "flex", "_direction": "column", "_alignItems": "center"}, children=[
        icon(ti, settings={"_typography": {"font-size": "1.6rem", "color": {"hex": GOLD}},
                            "_margin": {"bottom": "12px"}}),
        heading(title, "h3", settings={
            "_typography": {"font-family": SANS, "font-size": "1rem", "font-weight": "700",
                             "color": {"hex": INK_TXT}, "text-align": "center"},
            "_margin": {"bottom": "6px"}}),
        para(text, settings={
            "_typography": {"font-family": SANS, "font-size": "0.88rem", "line-height": "1.6",
                             "color": {"hex": MUTED}, "text-align": "center"},
            "_margin": {"bottom": "0px"}}),
    ], label=f"Trust: {title}")

trust = section(settings={
        "_background": {"color": {"hex": CREAM_AL}},
        "_padding": {"top": "56px", "right": "24px", "bottom": "56px", "left": "24px"},
        "_padding:mobile_portrait": {"top": "44px", "right": "20px", "bottom": "44px", "left": "20px"}},
        label="Trust Band", children=[
    container(children=[
        block(classes=["gggrd3"], settings={
            "_gridTemplateColumns": "repeat(4, minmax(0, 1fr))",
            "_gridTemplateColumns:tablet_portrait": "repeat(2, minmax(0, 1fr))",
            "_gridTemplateColumns:mobile_portrait": "repeat(2, minmax(0, 1fr))"}, children=[
            trust_item("ti-truck", "Worldwide shipping",
                       "BRT in Italy, FedEx worldwide — shipped within 5–6 business days."),
            trust_item("ti-shield", "2-year warranty",
                       "Covered against conformity defects and failures."),
            trust_item("ti-reload", "14-day returns",
                       "Right of withdrawal within 14 days; refund within 30 days."),
            trust_item("ti-credit-card", "Secure payments",
                       "Visa, Mastercard, Amex, PayPal &amp; Klarna. Prices include VAT."),
        ], label="Trust Grid"),
    ], label="Trust Inner"),
])

# ============================================================================
# 7. FITTER KIT — B2B
# ============================================================================
fitter = section(css_id="fitters", settings=dark_sec(INK), label="Fitter Kit", children=[
    container(children=[
        block(classes=["gggrd2"], settings={"_alignItemsGrid": "center"}, children=[
            block(children=[
                heading("For fitters", "div", classes=["ggeyeb"]),
                heading("The GG Putters Fitter Kit", "h2", classes=["gghttl"],
                        settings={"_typography": {"color": {"hex": WHITE}}}),
                para("The Fitter Kit is a modular fitting system that lets professionals test every putter configuration with a client in a single session.",
                     classes=["ggdefn"], settings={"_typography": {"color": {"hex": WHITE}}}),
                para("Handcrafted in Italy and fully modular — from head shape to insert, feel and balance — so each player leaves with a putter that is uniquely theirs.",
                     classes=["ggbody"], settings={"_typography": {"color": {"hex": MUTED_D}}}),
                button("Request the Fitter Kit", f"{SHOP}/for-fitters/", ["ggbtnp"],
                       settings={"_typography": {"color": {"hex": INK}}, "_width": "fit-content"},
                       aria="Request the GG Putters Fitter Kit"),
            ], label="Fitter Text"),
            block(classes=["ggcard"], settings={"_background": {"color": {"hex": CHARCOAL}},
                                                 "_border": {"width": {"top": "1px", "right": "1px", "bottom": "1px", "left": "1px"},
                                                              "style": "solid", "color": {"rgb": "rgba(184,146,79,0.35)"},
                                                              "radius": {"top": "16px", "right": "16px", "bottom": "16px", "left": "16px"}}},
                  children=[
                heading("What's inside the Fitter Kit", "h3", settings={
                    "_typography": {"font-family": SERIF, "font-size": "1.35rem", "font-weight": "600",
                                     "color": {"hex": WHITE}}, "_margin": {"bottom": "16px"}}),
                rich("<ul><li>2 heads — one Antares and one Orion</li><li>3 lofts (1°, 2°, 3°)</li><li>Weights kit — 2 heavy and 2 light (bullet or flat)</li><li>Necks (lie and offset)</li><li>Screws and hex screwdriver</li></ul>",
                     classes=["ggbody"],
                     settings={"_typography": {"color": {"hex": MUTED_D}}, "_margin": {"bottom": "0px"}}, label="Kit list"),
            ], label="Fitter Kit Card"),
        ], label="Fitter Grid"),
    ], label="Fitter Inner"),
])

# ============================================================================
# 8. FAQ — visible Q/A + FAQPage schema
# ============================================================================
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
     "Yes. You can exercise the right of withdrawal within 14 days of receipt; once the returned product is verified, the refund is issued within 30 days to your original payment method."),
]

def faq_block(q, a):
    return block(settings={"_padding": {"top": "24px", "right": "0px", "bottom": "24px", "left": "0px"},
                            "_border": {"width": {"bottom": "1px"}, "style": "solid",
                                         "color": {"rgb": "rgba(17,17,15,0.10)"}}}, children=[
        heading(q, "h3", settings={
            "_typography": {"font-family": SERIF, "font-size": "1.25rem", "font-weight": "600",
                             "color": {"hex": INK_TXT}}, "_margin": {"bottom": "10px"}}),
        para(a, classes=["ggbody"], settings={"_margin": {"bottom": "0px"}}),
    ], label=f"FAQ: {q[:24]}")

faq = section(css_id="faq", settings=light_sec(WHITE), label="FAQ", children=[
    header_block("FAQ", "Frequently Asked Questions",
                 "Quick answers about models, customization, pricing and where GG Putters are made."),
    block(settings={"_widthMax": "780px", "_margin": {"left": "auto", "right": "auto"}},
          children=[faq_block(q, a) for q, a in faq_items], label="FAQ List"),
])

# ============================================================================
# 9. CONTACT
# ============================================================================
def contact_card(title, rows):
    children = [heading(title, "h3", settings={
        "_typography": {"font-family": SANS, "font-size": "0.85rem", "font-weight": "700",
                         "text-transform": "uppercase", "letter-spacing": "0.16em",
                         "color": {"hex": GOLD}}, "_margin": {"bottom": "16px"}})]
    for kind, value, href in rows:
        s = {"text": value, "link": {"type": "external", "url": href},
             "_typography": {"font-family": SANS,
                              "color": {"hex": GOLD if href.startswith("mailto") else MUTED}},
             "_display": "block", "_margin": {"bottom": "6px"}}
        if href.startswith("mailto"):
            s["_cssGlobalClasses"] = ["ggclnk"]
        children.append(El("text-link", s, label=kind))
    children[-1].settings["_margin"]["bottom"] = "0px"
    return block(classes=["ggcard"], settings={"_alignItems": "center"}, children=children,
                 label=f"Contact: {title}")

contact = section(css_id="contact", settings=light_sec(CREAM), label="Contact", children=[
    header_block("Get in touch", "Contact Us",
                 "Questions about a build, an order or becoming a partner? Our team in Brescia is here to help."),
    block(classes=["gggrd3"], settings={"_widthMax": "1040px",
                                         "_margin": {"left": "auto", "right": "auto"}},
          label="Contact Grid", children=[
        contact_card("Info &amp; Sales", [("Email", "info@ggputters.com", "mailto:info@ggputters.com"),
                                          ("Phone", "+39 331 1099739", "tel:+393311099739")]),
        contact_card("Office &amp; Dealers", [("Email", "office@ggputters.com", "mailto:office@ggputters.com")]),
        contact_card("Headquarters", [("Address", "Palazzolo sull'Oglio (BS), Italy", f"{SHOP}/contact/")]),
    ]),
])

# ============================================================================
# 10. NEWSLETTER
# ============================================================================
newsletter = section(css_id="newsletter", settings={
        "_background": {"color": {"hex": INK}},
        "_padding": {"top": "92px", "right": "24px", "bottom": "92px", "left": "24px"},
        "_padding:mobile_portrait": {"top": "62px", "right": "20px", "bottom": "62px", "left": "20px"}},
        label="Newsletter", children=[
    container(settings={"_widthMax": "640px", "_display": "flex", "_direction": "column",
                         "_alignItems": "center"}, label="Newsletter Inner", children=[
        heading("Stay in the loop", "div", classes=["ggeyeb"]),
        heading("Join the Newsletter", "h2", classes=["gghttl"],
                settings={"_typography": {"color": {"hex": WHITE}, "text-align": "center"}}),
        para("Be the first to hear about new releases, limited editions and craftsmanship stories.",
             classes=["gglead"], settings={"_typography": {"color": {"hex": MUTED_D}, "text-align": "center"},
                                            "_margin": {"left": "auto", "right": "auto", "bottom": "32px"}}),
        El("form", {
            "fields": [{"type": "email", "label": "Email", "placeholder": "Enter your email address",
                        "required": True, "id": "newslttr", "width": "100"}],
            "showLabels": False, "submitButtonText": "Subscribe", "actions": ["email"],
            "emailSubject": "New newsletter subscription — GG Putters",
            "emailTo": "info@ggputters.com", "emailFromName": "GG Putters Website",
            "successMessage": "Thank you for subscribing!",
            "_widthMax": "480px", "_margin": {"left": "auto", "right": "auto"}
        }, label="Newsletter Form"),
    ]),
])

# ============================================================================
# 11. FOOTER
# ============================================================================
footer = section(settings={
        "_background": {"color": {"hex": "#0b0b0a"}},
        "_padding": {"top": "44px", "right": "24px", "bottom": "44px", "left": "24px"},
        "_border": {"width": {"top": "1px"}, "style": "solid",
                     "color": {"rgb": "rgba(255,255,255,0.08)"}}}, label="Footer", children=[
    container(settings={"_display": "flex", "_direction": "column", "_alignItems": "center"},
              children=[
        heading("GG Putters", "div", settings={
            "_typography": {"font-family": SERIF, "font-size": "1.4rem", "font-weight": "600",
                             "letter-spacing": "0.12em", "color": {"hex": GOLD}},
            "_margin": {"bottom": "10px"}}),
        para("Italian craft, Brescia engineering. Putters with a metalworking soul.",
             settings={"_typography": {"font-family": SANS, "font-size": "0.9rem",
                                        "color": {"hex": MUTED_D}, "text-align": "center"},
                        "_margin": {"bottom": "14px"}}),
        para("GG PUTTERS is a brand of GM PRODUCTION srl · VAT IT03351530989 · Palazzolo sull'Oglio (BS), Italy",
             settings={"_typography": {"font-family": SANS, "font-size": "0.82rem",
                                        "color": {"rgb": "rgba(255,255,255,0.5)"}, "text-align": "center"},
                        "_margin": {"bottom": "8px"}}),
        para("© 2026 GG Putters. All rights reserved.",
             settings={"_typography": {"font-family": SANS, "font-size": "0.78rem",
                                        "color": {"rgb": "rgba(255,255,255,0.38)"}, "text-align": "center"},
                        "_margin": {"bottom": "0px"}}),
    ], label="Footer Inner"),
])

# ----------------------------------------------------------------------------
# Flatten
# ----------------------------------------------------------------------------
roots = [hero, features, models, comparison, about, accessories, trust, fitter, faq,
         contact, newsletter, footer]
for r in roots:
    flatten(r, 0)

# ----------------------------------------------------------------------------
# Page settings: SEO meta, custom CSS, JSON-LD (Organization, WebSite,
# Products, FAQPage)
# ----------------------------------------------------------------------------
def product(name, desc, price, url, rich_offer=False):
    offer = {"@type": "Offer", "price": price, "priceCurrency": "EUR",
             "availability": "https://schema.org/InStock", "url": url,
             "priceValidUntil": "2026-12-31"}
    if rich_offer:
        offer["shippingDetails"] = {
            "@type": "OfferShippingDetails",
            "shippingDestination": {"@type": "DefinedRegion", "addressCountry": "IT"},
            "deliveryTime": {"@type": "ShippingDeliveryTime",
                              "handlingTime": {"@type": "QuantitativeValue", "minValue": 5,
                                                "maxValue": 6, "unitCode": "DAY"}}}
        offer["hasMerchantReturnPolicy"] = {
            "@type": "MerchantReturnPolicy",
            "applicableCountry": "IT",
            "returnPolicyCategory": "https://schema.org/MerchantReturnFiniteReturnWindow",
            "merchantReturnDays": 14,
            "returnMethod": "https://schema.org/ReturnByMail",
            "refundType": "https://schema.org/FullRefund"}
    return {"@type": "Product", "name": f"GG {name}",
            "brand": {"@type": "Brand", "name": "GG Putters"},
            "category": "Golf Putter", "material": "Aluminum, Steel",
            "description": desc, "url": url, "offers": offer}

graph = [
    {"@type": "Organization", "@id": f"{SHOP}/#organization", "name": "GG Putters",
     "legalName": "GM PRODUCTION srl", "url": f"{SHOP}/",
     "description": "Handcrafted, CNC-milled custom golf putters made in Brescia, Italy.",
     "email": "info@ggputters.com", "telephone": "+39 331 1099739",
     "vatID": "IT03351530989",
     "address": {"@type": "PostalAddress", "streetAddress": "Via Taranto, 7",
                  "addressLocality": "Palazzolo sull'Oglio", "addressRegion": "BS",
                  "postalCode": "25036", "addressCountry": "IT"},
     "contactPoint": [
        {"@type": "ContactPoint", "contactType": "sales", "email": "info@ggputters.com",
         "telephone": "+39 331 1099739"},
        {"@type": "ContactPoint", "contactType": "customer service", "email": "office@ggputters.com"}]},
    {"@type": "WebSite", "@id": f"{SHOP}/#website", "url": f"{SHOP}/", "name": "GG Putters",
     "publisher": {"@id": f"{SHOP}/#organization"}},
    product("Antares", "Milled blade putter for feel and arc strokes, with a 3-position adjustable weight system and interchangeable faces.", "353.00", f"{SHOP}/putters/antares/", rich_offer=True),
    product("Orion", "Milled mallet putter engineered for stability and higher forgiveness (MOI), with a 3-position adjustable weight system.", "353.00", f"{SHOP}/putters/orion/", rich_offer=True),
    product("Clubfaces", "Interchangeable face inserts (1°–3°) to tune loft and feel.", "52.00", f"{SHOP}/putters/clubfaces/"),
    product("Extra Weights", "Heavy and light weights for the 3-position weighting system.", "21.00", f"{SHOP}/putters/extra-weights/"),
    {"@type": "FAQPage", "@id": f"{SHOP}/#faq",
     "mainEntity": [{"@type": "Question", "name": q,
                      "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq_items]},
]
json_ld = {"@context": "https://schema.org", "@graph": graph}

custom_css = ("html{scroll-behavior:smooth;}"
              "::selection{background:#b8924f;color:#11110f;}"
              "body{font-family:'Inter',sans-serif;}")

page_settings = {
    "pageTitle": "Custom Milled Putters Made in Italy | Antares &amp; Orion — GG Putters",
    "metaDescription": "GG Putters: custom milled golf putters made in Brescia, Italy. Antares blade and Orion mallet from €353, 3-position adjustable weights and interchangeable faces.",
    "customCss": custom_css,
    "customScriptsBodyFooter": '<script type="application/ld+json">' + json.dumps(json_ld, ensure_ascii=False) + '</script>',
}

template = {
    "name": "gg-putters-landing",
    "title": "GG Putters — SEO/GEO Landing Page",
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
