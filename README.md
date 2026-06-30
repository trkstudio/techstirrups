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
- **9× H2** — Features · Models (Antares/Orion) · Comparison · About · Accessories ·
  Fitter Kit · FAQ · Contact · Newsletter
- **19× H3** — feature con definizioni, schede prodotto, accessori, FAQ, contatti

Tecniche GEO applicate:

- **Definizioni in una frase** per i termini chiave (milled putter, adjustable weighting…).
- **Dati concreti**: modelli, prezzi reali (€353 / €285 / €52 / €21 / €32 / €149 / €63),
  garanzia 2 anni, spedizione 5–6 giorni lavorativi, lofts 1°–3°.
- **Tabella di confronto** Antares (blade) vs Orion (mallet).
- **Trust band** transazionale: spedizioni (BRT/FedEx, 5–6 gg), garanzia 2 anni,
  reso 14 gg (rimborso 30 gg), pagamenti sicuri (Visa/Mastercard/Amex/PayPal/Klarna, IVA inclusa).
- **Blocco FAQ** (7 Q/A) + **`FAQPage` JSON-LD** per i featured snippet.
- **Offer** Antares/Orion arricchite con `shippingDetails` e `hasMerchantReturnPolicy`.
- **Dati strutturati JSON-LD**: `Organization` (GM PRODUCTION srl, P.IVA, indirizzo),
  `WebSite`, 4× `Product` con `Offer` in EUR, `FAQPage` — iniettati via `customScriptsBodyFooter`.
- `pageTitle` + `metaDescription` precompilati; `customCss` (smooth scroll, selection brand).
- Ancore di sezione (`#shop`, `#compare`, `#about`, `#accessories`, `#fitters`, `#faq`, `#contact`, `#newsletter`).
- **Link interni** ai prodotti/categorie reali dello shop (topic cluster), `alt` descrittivi e `aria-label`.

## Rigenerare il JSON

```bash
python3 generate_template.py
```
