# GG Putters — Landing Page per Bricks 2.3.6

Template della landing page **GG Putters** (putter di lusso fresati CNC, artigianato
italiano di Brescia) pronto da importare in Bricks Builder 2.3.6.

## File

- `gg-putters-landing.json` — template nel formato *Template Export* di Bricks, pronto all'import.
- `generate_template.py` — generatore Python che produce il JSON (sorgente di verità, riproducibile).

## Come importare in Bricks

1. WordPress → **Bricks → Templates**.
2. Clic su **Import Templates**.
3. Seleziona/trascina `gg-putters-landing.json` e conferma.
4. Crea/apri una pagina, **Edit with Bricks** → **Templates** → inserisci
   *“GG Putters — SEO Landing Page”* (tipo *content*).

> All'import Bricks rigenera gli ID elemento, unisce le classi globali e (per i
> template) scarica eventuali immagini remote. I segnaposto immagine vanno
> sostituiti con le foto reali dei prodotti.

## Struttura SEO / GEO

Contenuti basati sui dati reali di `shop.ggputters.com` e ottimizzati per i motori
generativi (AI Overviews, Perplexity, ecc.) secondo la *Regola d'Oro* in
`.cursor/rules/regola-doro-geo-seo.mdc`.

Gerarchia heading pulita:

- **1× H1** — *Custom Milled Putters — Antares & Orion, Handcrafted in Italy* (hero)
- **8× H2** — Features · Models (Antares/Orion) · About · Accessories ·
  Fitter Kit · FAQ · Contact · Newsletter
- **H3** — feature con definizioni, schede prodotto, accessori, trust band, FAQ, contatti

Tecniche GEO applicate:

- **Definizioni in una frase** per i termini chiave (milled putter, adjustable weighting…).
- **Dati concreti**: modelli, prezzi reali (€353 / €285 / €52 / €21 / €32 / €149 / €63),
  garanzia 2 anni, spedizione 5–6 giorni lavorativi, lofts 1°–3°.
- **Trust band** transazionale: spedizioni (BRT/FedEx, 5–6 gg), garanzia 2 anni,
  reso 14 gg (rimborso 30 gg), pagamenti (Visa/Mastercard/Amex/PayPal/Klarna, IVA inclusa).
- **Blocco FAQ** (7 Q/A) + **`FAQPage` JSON-LD** per i featured snippet.
- **JSON-LD**: `Organization` (GM PRODUCTION srl, P.IVA, indirizzo), `WebSite`,
  4× `Product` (Antares/Orion con `shippingDetails` e `hasMerchantReturnPolicy`), `FAQPage`.
- `pageTitle` + `metaDescription` precompilati.
- Ancore di sezione (`#shop`, `#about`, `#accessories`, `#fitters`, `#faq`, `#contact`, `#newsletter`).
- **Link interni** ai prodotti/categorie reali dello shop (topic cluster), `alt` descrittivi e `aria-label`.

## Layout, responsive e accessibilità

Il template è volutamente **minimale e neutro**: nessun colore e nessuna tipografia
forzata nel JSON — **colori e font sono ereditati dai theme styles del sito**.

- **Layout 100% Flexbox fluido**: ogni riga è `display:flex; flex-wrap:wrap` e le colonne
  usano `flex: 1 1 <basis>` (es. 300–400px) con `min-width:0`, così si adattano e vanno
  a capo da sole **senza media query**. Spaziature fluide con `clamp()`.
- **Poche classi globali** riutilizzabili (`gg-section`, `gg-row`, `gg-col`, `gg-header`…),
  quasi nessuno stile inline → CSS pulito e prevedibile dopo l'import.
- **Accessibilità**: heading semantici, `alt` sulle immagini, icone decorative
  `aria-hidden="true"`, `aria-label` sui pulsanti, link sottolineati, **focus tastiera**
  (`:focus-visible`), **`prefers-reduced-motion`**, `scroll-margin` sulle ancore,
  `img{max-width:100%}`. (Il contrasto colore dipende dal tema del sito.)

## Rigenerare il JSON

```bash
python3 generate_template.py
```
