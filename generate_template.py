#!/usr/bin/env python3
"""Generate a Bricks Builder 2.3.6 template-export JSON for the GG Putters
SEO landing page. Run: python3 generate_template.py  -> gg-putters-landing.json
"""
import json

# ----------------------------------------------------------------------------
# Design tokens (luxury / metalworking feel)
# ----------------------------------------------------------------------------
INK      = "#11110f"   # near-black background
CHARCOAL = "#1b1b18"   # alt dark
GOLD     = "#b8924f"   # brass accent
GOLD_LT  = "#d8b87a"   # lighter brass (hover)
CREAM    = "#f7f4ed"   # warm light background
CREAM_AL = "#efe9db"   # alt light background
WHITE    = "#ffffff"
INK_TXT  = "#1c1b18"   # body text on light
MUTED    = "#5d5a52"   # muted text on light
MUTED_D  = "#b6b1a5"   # muted text on dark
LINE_D   = "rgba(255,255,255,0.12)"
LINE_L   = "rgba(17,17,15,0.10)"

SERIF = "Playfair Display"
SANS  = "Inter"

# ----------------------------------------------------------------------------
# ID generator (6-char alphanumeric, unique)
# ----------------------------------------------------------------------------
_counter = 0
def nid(prefix="e"):
    global _counter
    _counter += 1
    return f"{prefix}{_counter:05d}"

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
# Helper element builders
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

def icon(ti, settings=None, label=None):
    s = {"icon": {"library": "themify", "icon": ti}}
    if settings:
        s.update(settings)
    return El("icon", s, label=label or "Icon")

def button(text, url, classes, settings=None, new_tab=False, rel=None, aria=None):
    link = {"type": "external", "url": url}
    if new_tab:
        link["newTab"] = True
    if rel:
        link["rel"] = rel
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
        "_widthMax": "640px"}},
    {"id": "ggbody", "name": "gg-body", "settings": {
        "_typography": {"font-family": SANS, "font-size": "1rem",
                         "line-height": "1.7", "color": {"hex": MUTED}},
        "_margin": {"bottom": "16px"}}},
    {"id": "ggcard", "name": "gg-card", "settings": {
        "_background": {"color": {"hex": WHITE}},
        "_border": {"width": {"top": "1px", "right": "1px", "bottom": "1px", "left": "1px"},
                     "style": "solid", "color": {"rgb": "rgba(17,17,15,0.08)"},
                     "radius": {"top": "16px", "right": "16px", "bottom": "16px", "left": "16px"}},
        "_padding": {"top": "40px", "right": "34px", "bottom": "40px", "left": "34px"},
        "_boxShadow": {"values": {"offsetX": "0", "offsetY": "18", "blur": "40", "spread": "-24"},
                        "color": {"rgb": "rgba(17,17,15,0.18)"}},
        "_height": "100%",
        "_display": "flex", "_direction": "column"}},
    {"id": "gggrd3", "name": "gg-grid-3", "settings": {
        "_display": "grid",
        "_gridTemplateColumns": "repeat(3, minmax(0, 1fr))",
        "_gridGap": "28px",
        "_gridTemplateColumns:tablet_portrait": "repeat(2, minmax(0, 1fr))",
        "_gridTemplateColumns:mobile_portrait": "1fr"}},
    {"id": "gggrd2", "name": "gg-grid-2", "settings": {
        "_display": "grid",
        "_gridTemplateColumns": "repeat(2, minmax(0, 1fr))",
        "_gridGap": "56px",
        "_alignItemsGrid": "center",
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
# Section style presets
# ----------------------------------------------------------------------------
def sec_pad():
    return {"_padding": {"top": "120px", "right": "24px", "bottom": "120px", "left": "24px"},
            "_padding:mobile_portrait": {"top": "72px", "right": "20px", "bottom": "72px", "left": "20px"}}

def dark_sec(extra=None, **kw):
    s = {"_background": {"color": {"hex": kw.get("bg", INK)}}}
    s.update(sec_pad())
    if extra:
        s.update(extra)
    return s

def light_sec(bg=CREAM, extra=None):
    s = {"_background": {"color": {"hex": bg}}}
    s.update(sec_pad())
    if extra:
        s.update(extra)
    return s

WHITE_TXT = {"_typography": {"color": {"hex": WHITE}}}
DARK_LEAD = {"_typography": {"color": {"hex": MUTED_D}}}

# ============================================================================
# 1. HERO (dark)  — single H1
# ============================================================================
hero = section(css_id="top", settings=dark_sec(extra={
        "_background": {"color": {"hex": INK}},
    }), label="Hero", children=[
    container(settings={"_widthMax": "880px", "_display": "flex", "_direction": "column",
                         "_alignItems": "center"}, label="Hero Inner", children=[
        heading("GG Putters", "div", classes=["ggeyeb"], label="Eyebrow"),
        heading("Handcrafted Italian Putters, CNC-Milled in Brescia", "h1",
                classes=["gghttl"],
                settings={"_typography": {"font-family": SERIF, "color": {"hex": WHITE},
                                           "font-size": "clamp(2.4rem, 5vw, 4rem)",
                                           "font-weight": "600", "line-height": "1.08",
                                           "text-align": "center"},
                           "_margin": {"bottom": "22px"}}, label="H1"),
        heading("Customization, innovation and peak performance on every green.", "div",
                settings={"_typography": {"font-family": SERIF, "font-style": "italic",
                                           "font-size": "1.4rem", "color": {"hex": GOLD_LT},
                                           "line-height": "1.4", "text-align": "center"},
                           "_margin": {"bottom": "26px"}}, label="Tagline"),
        para("Every GG putter combines Italian craftsmanship with expert CNC milling to deliver a soft, responsive feel and a consistently straighter roll.",
             classes=["gglead"],
             settings={"_typography": {"color": {"hex": MUTED_D}, "text-align": "center"},
                        "_margin": {"left": "auto", "right": "auto", "bottom": "38px"}}),
        block(classes=None, settings={"_display": "flex", "_justifyContent": "center",
                                       "_gap": "16px", "_flexWrap": "wrap"}, label="Hero CTAs", children=[
            button("Shop Putters", "#shop", ["ggbtnp"], aria="Shop GG Putters"),
            button("Discover the Craft", "#about", ["ggbtno"], aria="Learn about GG Putters"),
        ]),
    ]),
])

# ============================================================================
# 2. FEATURES (light) — H2 + 3x H3
# ============================================================================
def feature_card(ti, title, body):
    return block(classes=["ggcard"], children=[
        icon(ti, settings={"_cssGlobalClasses": ["ggfico"]}),
        heading(title, "h3", settings={
            "_typography": {"font-family": SERIF, "font-size": "1.45rem", "font-weight": "600",
                             "color": {"hex": INK_TXT}}, "_margin": {"bottom": "14px"}}),
        para(body, classes=["ggbody"], settings={"_margin": {"bottom": "0px"}}),
    ], label=f"Feature: {title}")

features = section(css_id="features", settings=light_sec(CREAM), label="Features", children=[
    container(settings={"_display": "flex", "_direction": "column", "_alignItems": "center",
                         }, label="Features Header", children=[
        heading("Performance by design", "div", classes=["ggeyeb"]),
        heading("Why players choose our putters", "h2", classes=["gghttl"],
                settings={"_typography": {"color": {"hex": INK_TXT}, "text-align": "center"}}),
        para("Engineered to perform, refined to last — every detail is built around a cleaner, more confident stroke.",
             classes=["gglead"], settings={"_typography": {"text-align": "center"},
                                            "_margin": {"left": "auto", "right": "auto", "bottom": "56px"}}),
    ]),
    block(classes=["gggrd3"], settings={"_widthMax": "1180px", "_margin": {"left": "auto", "right": "auto"}},
          label="Feature Grid", children=[
        feature_card("ti-target", "Stability & straighter roll",
                     "A lighter aluminum central structure paired with heavier stainless steel perimeter weighting creates exceptional stability at impact, reducing unwanted vibration and promoting a cleaner, straighter roll."),
        feature_card("ti-settings", "Adjustable weighting system",
                     "Designed to adapt to the player, the adjustable weighting system allows complete balance customization to fine-tune performance and help compensate for stroke tendencies."),
        feature_card("ti-layers", "Interchangeable face inserts",
                     "Interchangeable face inserts let golfers optimize feel and responsiveness for different green speeds and playing conditions."),
    ]),
])

# ============================================================================
# 3. ABOUT (dark) — H2 + image, 2 columns
# ============================================================================
about_text = block(settings={}, label="About Text", children=[
    heading("About us", "div", classes=["ggeyeb"]),
    heading("Italian Craft, Brescia Engineering — Putters With a Metalworking Soul", "h2",
            classes=["gghttl"], settings={"_typography": {"color": {"hex": WHITE}}}),
    para("Deeply rooted in Brescia’s historic legacy of precision engineering, our putters are born from generations of manufacturing expertise. Drawing on our expertise in luxury and design, we create one-of-a-kind putters.",
         classes=["ggbody"], settings={"_typography": {"color": {"hex": MUTED_D}}}),
    para("Milled from a solid billet of premium metal using advanced CNC technology, our putters blend high-precision engineering with meticulous artistry. Every micro-feature is sculpted with obsessive attention to detail, ensuring a club that delivers unrivaled balance, control and feel on every stroke.",
         classes=["ggbody"], settings={"_typography": {"color": {"hex": MUTED_D}}}),
    para("Hand-finished with absolute care and built to last, our exclusive putters combine high performance with timeless Italian workmanship to elevate both your game and your collection.",
         classes=["ggbody"], settings={"_typography": {"color": {"hex": MUTED_D}}, "_margin": {"bottom": "0px"}}),
])
about_img = image_ph("GG Putters CNC milling process in the Brescia workshop, Italy",
                     settings={"_border": {"radius": {"top": "16px", "right": "16px", "bottom": "16px", "left": "16px"}},
                                "_height": "100%", "_objectFit": "cover", "_aspectRatio": "4/5"},
                     label="About Image")

about = section(css_id="about", settings=dark_sec(extra={"_background": {"color": {"hex": CHARCOAL}}}),
                label="About", children=[
    container(settings={}, label="About Inner", children=[
        block(classes=["gggrd2"], children=[about_text, about_img], label="About Grid"),
    ]),
])

# ============================================================================
# 4. PRODUCTS / SHOP (light) — H2 + gallery + CTA
# ============================================================================
def shop_thumb(alt):
    return El("image", {"image": {"url": "", "alt": alt}, "altText": alt,
                         "link": {"type": "external", "url": "#shop", "ariaLabel": alt},
                         "_border": {"radius": {"top": "12px", "right": "12px", "bottom": "12px", "left": "12px"}},
                         "_aspectRatio": "1", "_objectFit": "cover", "_cursor": "pointer",
                         "_cssTransition": "transform 0.3s ease",
                         "_transform:hover": {"scaleX": "1.03", "scaleY": "1.03"}},
              label=f"Product photo: {alt[:20]}")

products = section(css_id="shop", settings=light_sec(WHITE), label="Products / Shop", children=[
    container(settings={"_display": "flex", "_direction": "column", "_alignItems": "center",
                         }, label="Products Header", children=[
        heading("Our products", "div", classes=["ggeyeb"]),
        heading("Shop Our Putters", "h2", classes=["gghttl"],
                settings={"_typography": {"color": {"hex": INK_TXT}, "text-align": "center"}}),
        para("Explore the collection — click any image to view the putter from every angle and add it to your bag.",
             classes=["gglead"], settings={"_typography": {"text-align": "center"},
                                            "_margin": {"left": "auto", "right": "auto", "bottom": "50px"}}),
    ]),
    block(classes=["gggrd3"], settings={"_widthMax": "1100px",
                                         "_gridTemplateColumns": "repeat(4, minmax(0, 1fr))",
                                         "_gridTemplateColumns:tablet_portrait": "repeat(2, minmax(0, 1fr))",
                                         "_gridTemplateColumns:mobile_portrait": "repeat(2, minmax(0, 1fr))",
                                         "_margin": {"left": "auto", "right": "auto", "bottom": "48px"}},
          label="Product Gallery", children=[
        shop_thumb("GG milled putter — address view"),
        shop_thumb("GG milled putter — toe profile"),
        shop_thumb("GG milled putter — cavity back detail"),
        shop_thumb("GG milled putter — face insert close-up"),
    ]),
    block(settings={"_display": "flex", "_justifyContent": "center"}, label="Shop CTA", children=[
        button("Shop Clubs", "#shop", ["ggbtnp"],
               settings={"_typography": {"color": {"hex": INK}}}, aria="Shop GG Putter clubs"),
    ]),
])

# ============================================================================
# 5. ACCESSORIES (cream alt) — H2 + 2 product cards
# ============================================================================
def accessory_card(alt, title, price, opt_label, opt_value):
    return block(classes=["ggcard"], children=[
        image_ph(alt, settings={"_border": {"radius": {"top": "12px", "right": "12px", "bottom": "12px", "left": "12px"}},
                                 "_aspectRatio": "16/10", "_objectFit": "cover",
                                 "_margin": {"bottom": "24px"}}),
        heading(title, "h3", settings={
            "_typography": {"font-family": SERIF, "font-size": "1.45rem", "font-weight": "600",
                             "color": {"hex": INK_TXT}}, "_margin": {"bottom": "8px"}}),
        heading(price, "div", classes=["ggprice"], settings={"_margin": {"bottom": "18px"}}),
        para(f"<strong>{opt_label}:</strong> {opt_value}", classes=["ggbody"]),
        para("Choose your option and quantity at checkout.", classes=["ggbody"],
             settings={"_typography": {"font-size": "0.9rem", "color": {"hex": MUTED}}, "_margin": {"bottom": "26px"}}),
        block(settings={"_margin": {"top": "auto"}}, label="Buy", children=[
            button("Buy Now", "#shop", ["ggbtnp"],
                   settings={"_typography": {"color": {"hex": INK}}, "_width": "fit-content"},
                   aria=f"Buy {title}"),
        ]),
    ], label=f"Accessory: {title}")

accessories = section(css_id="accessories", settings=light_sec(CREAM_AL), label="Accessories", children=[
    container(settings={"_display": "flex", "_direction": "column", "_alignItems": "center",
                         }, label="Accessories Header", children=[
        heading("Optional accessories", "div", classes=["ggeyeb"]),
        heading("Optional Accessories", "h2", classes=["gghttl"],
                settings={"_typography": {"color": {"hex": INK_TXT}, "text-align": "center"}}),
        para("Fine-tune feel and balance with interchangeable plates and weights — selectable by specification and quantity.",
             classes=["gglead"], settings={"_typography": {"text-align": "center"},
                                            "_margin": {"left": "auto", "right": "auto", "bottom": "52px"}}),
    ]),
    block(classes=["gggrd2"], settings={"_widthMax": "920px",
                                         "_margin": {"left": "auto", "right": "auto"},
                                         "_alignItemsGrid": "stretch"}, label="Accessories Grid", children=[
        accessory_card("GG putter interchangeable face insert plate", "Face Insert Plate",
                       "€52,00", "Plate", "2°, 3°, 4°"),
        accessory_card("GG putter adjustable weights set", "Adjustable Weights",
                       "€21,00", "Weights", "Light (1.19 oz), Medium (1.48 oz), Heavy (1.97 oz)"),
    ]),
])

# ============================================================================
# 6. DEALERS (dark) — H2 + dealer info + become partner
# ============================================================================
dealers = section(css_id="dealers", settings=dark_sec(extra={"_background": {"color": {"hex": INK}}}),
                  label="Dealers", children=[
    container(settings={}, label="Dealers Inner", children=[
        block(settings={"_display": "flex", "_direction": "column",
                         "_alignItems": "center"}, label="Dealers Header", children=[
            heading("Where to find us", "div", classes=["ggeyeb"]),
            heading("Fitters & Official Dealers", "h2", classes=["gghttl"],
                    settings={"_typography": {"color": {"hex": WHITE}, "text-align": "center"},
                               "_margin": {"bottom": "48px"}}),
        ]),
        block(classes=["gggrd2"], settings={"_alignItemsGrid": "start"}, label="Dealers Grid", children=[
            block(settings={}, label="Dealer List", children=[
                heading("USA", "h3", settings={
                    "_typography": {"font-family": SANS, "font-size": "0.85rem", "font-weight": "700",
                                     "text-transform": "uppercase", "letter-spacing": "0.18em",
                                     "color": {"hex": GOLD}}, "_margin": {"bottom": "14px"}}),
                para("<strong>Ohio</strong> — TSH Golf", classes=["ggbody"],
                     settings={"_typography": {"color": {"hex": WHITE}}, "_margin": {"bottom": "6px"}}),
                El("text-link", {"text": "www.tshgolf.com",
                                  "link": {"type": "external", "url": "https://www.tshgolf.com", "newTab": True},
                                  "_cssGlobalClasses": ["ggclnk"]}, label="Dealer link"),
                heading("Sales Representatives", "h3", settings={
                    "_typography": {"font-family": SANS, "font-size": "0.85rem", "font-weight": "700",
                                     "text-transform": "uppercase", "letter-spacing": "0.18em",
                                     "color": {"hex": GOLD}},
                    "_margin": {"top": "34px", "bottom": "10px"}}),
                para("Coverage is expanding worldwide. Contact us to find a representative near you.",
                     classes=["ggbody"], settings={"_typography": {"color": {"hex": MUTED_D}}, "_margin": {"bottom": "0px"}}),
            ]),
            block(classes=["ggcard"], settings={"_background": {"color": {"hex": CHARCOAL}},
                                                 "_border": {"width": {"top": "1px", "right": "1px", "bottom": "1px", "left": "1px"},
                                                              "style": "solid", "color": {"rgb": "rgba(184,146,79,0.35)"},
                                                              "radius": {"top": "16px", "right": "16px", "bottom": "16px", "left": "16px"}}},
                  label="Partner Card", children=[
                heading("Become an Official Partner", "h3", settings={
                    "_typography": {"font-family": SERIF, "font-size": "1.6rem", "font-weight": "600",
                                     "color": {"hex": WHITE}}, "_margin": {"bottom": "16px"}}),
                para("We are seeking qualified agents, fitters and distributors to represent our brand in uncovered regions. If you share our passion for precision and luxury, contact us today to explore partnership opportunities.",
                     classes=["ggbody"], settings={"_typography": {"color": {"hex": MUTED_D}}, "_margin": {"bottom": "26px"}}),
                button("Become a Partner", "mailto:info@ggputters.com", ["ggbtnp"],
                       settings={"_typography": {"color": {"hex": INK}}, "_width": "fit-content"},
                       aria="Email GG Putters to become an official partner"),
            ]),
        ]),
    ]),
])

# ============================================================================
# 7. CONTACT (light) — H2 + 3 contact cards
# ============================================================================
def contact_card(title, lines):
    children = [heading(title, "h3", settings={
        "_typography": {"font-family": SANS, "font-size": "0.85rem", "font-weight": "700",
                         "text-transform": "uppercase", "letter-spacing": "0.16em",
                         "color": {"hex": GOLD}}, "_margin": {"bottom": "16px"}})]
    for label_txt, email, phone in lines:
        children.append(El("text-link", {"text": email,
                            "link": {"type": "external", "url": f"mailto:{email}"},
                            "_cssGlobalClasses": ["ggclnk"],
                            "_display": "block", "_margin": {"bottom": "6px"}},
                           label="Email"))
        if phone:
            children.append(El("text-link", {"text": phone,
                                "link": {"type": "external", "url": f"tel:{phone.replace(' ', '')}"},
                                "_typography": {"font-family": SANS, "color": {"hex": MUTED}},
                                "_display": "block", "_margin": {"bottom": "0px"}},
                               label="Phone"))
    return block(classes=["ggcard"], settings={"_alignItems": "center"},
                 children=children, label=f"Contact: {title}")

contact = section(css_id="contact", settings=light_sec(CREAM), label="Contact", children=[
    container(settings={"_display": "flex", "_direction": "column", "_alignItems": "center",
                         }, label="Contact Header", children=[
        heading("Get in touch", "div", classes=["ggeyeb"]),
        heading("Contact Us", "h2", classes=["gghttl"],
                settings={"_typography": {"color": {"hex": INK_TXT}, "text-align": "center"}}),
        para("Questions about a build, an order or a partnership? Our team is here to help.",
             classes=["gglead"], settings={"_typography": {"text-align": "center"},
                                            "_margin": {"left": "auto", "right": "auto", "bottom": "52px"}}),
    ]),
    block(classes=["gggrd3"], settings={"_widthMax": "1100px",
                                         "_margin": {"left": "auto", "right": "auto"}},
          label="Contact Grid", children=[
        contact_card("Sales", [("Sales", "info@ggputters.com", "+39 349 880 0268")]),
        contact_card("Customer Service", [("Customer Service", "customerservice@ggputters.com", "+39 375 794 2431")]),
        contact_card("Dealers / Agents", [("Dealers", "office@ggputters.com", None)]),
    ]),
])

# ============================================================================
# 8. NEWSLETTER (gold/dark) — H2 + form
# ============================================================================
newsletter = section(css_id="newsletter", settings={
        "_background": {"color": {"hex": INK}},
        "_padding": {"top": "96px", "right": "24px", "bottom": "96px", "left": "24px"},
        "_padding:mobile_portrait": {"top": "64px", "right": "20px", "bottom": "64px", "left": "20px"}},
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
            "fields": [
                {"type": "email", "label": "Email", "placeholder": "Enter your email address",
                 "required": True, "id": "newslttr", "width": "100"}
            ],
            "showLabels": False,
            "submitButtonText": "Subscribe",
            "actions": ["email"],
            "emailSubject": "New newsletter subscription — GG Putters",
            "emailTo": "info@ggputters.com",
            "emailFromName": "GG Putters Website",
            "successMessage": "Thank you for subscribing!",
            "_widthMax": "480px",
            "_margin": {"left": "auto", "right": "auto"}
        }, label="Newsletter Form"),
    ]),
])

# ============================================================================
# 9. FOOTER (deep dark)
# ============================================================================
footer = section(settings={
        "_background": {"color": {"hex": "#0b0b0a"}},
        "_padding": {"top": "44px", "right": "24px", "bottom": "44px", "left": "24px"},
        "_border": {"width": {"top": "1px"}, "style": "solid",
                     "color": {"rgb": "rgba(255,255,255,0.08)"}}}, label="Footer", children=[
    container(settings={"_display": "flex", "_direction": "column", "_alignItems": "center"},
              label="Footer Inner", children=[
        heading("GG Putters", "div", settings={
            "_typography": {"font-family": SERIF, "font-size": "1.4rem", "font-weight": "600",
                             "letter-spacing": "0.12em", "color": {"hex": GOLD}},
            "_margin": {"bottom": "10px"}}),
        para("Italian craft, Brescia engineering. Putters with a metalworking soul.",
             settings={"_typography": {"font-family": SANS, "font-size": "0.9rem",
                                        "color": {"hex": MUTED_D}, "text-align": "center"},
                        "_margin": {"bottom": "16px"}}),
        para("© 2026 GG Putters. All rights reserved.",
             settings={"_typography": {"font-family": SANS, "font-size": "0.8rem",
                                        "color": {"rgb": "rgba(255,255,255,0.4)"}, "text-align": "center"},
                        "_margin": {"bottom": "0px"}}),
    ]),
])

# ----------------------------------------------------------------------------
# Flatten all root sections
# ----------------------------------------------------------------------------
roots = [hero, features, about, products, accessories, dealers, contact, newsletter, footer]
for r in roots:
    flatten(r, 0)

# ----------------------------------------------------------------------------
# Page settings: SEO custom CSS + JSON-LD structured data
# ----------------------------------------------------------------------------
json_ld = {
    "@context": "https://schema.org",
    "@graph": [
        {
            "@type": "Organization",
            "@id": "https://www.ggputters.com/#organization",
            "name": "GG Putters",
            "url": "https://www.ggputters.com/",
            "description": "Handcrafted, CNC-milled luxury golf putters made in Brescia, Italy.",
            "email": "info@ggputters.com",
            "telephone": "+39 349 880 0268",
            "address": {"@type": "PostalAddress", "addressLocality": "Brescia",
                         "addressCountry": "IT"},
            "contactPoint": [
                {"@type": "ContactPoint", "contactType": "sales", "email": "info@ggputters.com",
                 "telephone": "+39 349 880 0268"},
                {"@type": "ContactPoint", "contactType": "customer service",
                 "email": "customerservice@ggputters.com", "telephone": "+39 375 794 2431"},
                {"@type": "ContactPoint", "contactType": "dealers", "email": "office@ggputters.com"}
            ]
        },
        {
            "@type": "WebSite",
            "@id": "https://www.ggputters.com/#website",
            "url": "https://www.ggputters.com/",
            "name": "GG Putters",
            "publisher": {"@id": "https://www.ggputters.com/#organization"}
        },
        {
            "@type": "Product",
            "name": "GG Handcrafted CNC-Milled Putter",
            "brand": {"@type": "Brand", "name": "GG Putters"},
            "description": "Italian handcrafted putter milled from a solid billet using advanced CNC technology, with adjustable perimeter weighting and interchangeable face inserts for a soft feel and straighter roll.",
            "material": "Aluminum, Stainless Steel"
        },
        {
            "@type": "Product",
            "name": "Face Insert Plate",
            "brand": {"@type": "Brand", "name": "GG Putters"},
            "description": "Interchangeable face insert plate for GG putters. Available in 2°, 3° and 4°.",
            "offers": {"@type": "Offer", "price": "52.00", "priceCurrency": "EUR",
                        "availability": "https://schema.org/InStock"}
        },
        {
            "@type": "Product",
            "name": "Adjustable Weights",
            "brand": {"@type": "Brand", "name": "GG Putters"},
            "description": "Adjustable weights for GG putters. Light (1.19 oz), medium (1.48 oz) and heavy (1.97 oz).",
            "offers": {"@type": "Offer", "price": "21.00", "priceCurrency": "EUR",
                        "availability": "https://schema.org/InStock"}
        }
    ]
}

custom_css = (
    "html{scroll-behavior:smooth;}"
    "::selection{background:#b8924f;color:#11110f;}"
    "body{font-family:'Inter',sans-serif;}"
)

ld_script = '<script type="application/ld+json">' + json.dumps(json_ld, ensure_ascii=False) + '</script>'

page_settings = {
    "pageTitle": "Handcrafted Italian Putters | CNC-Milled in Brescia — GG Putters",
    "metaDescription": "GG Putters: luxury Italian putters CNC-milled in Brescia. Adjustable weighting, interchangeable face inserts and a soft, responsive feel for a straighter roll.",
    "customCss": custom_css,
    "customScriptsBodyFooter": ld_script,
}

# ----------------------------------------------------------------------------
# Assemble template export object
# ----------------------------------------------------------------------------
template = {
    "name": "gg-putters-landing",
    "title": "GG Putters — SEO Landing Page",
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

print(f"Generated {len(elements)} elements, {len(global_classes)} global classes.")
