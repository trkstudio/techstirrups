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

## Struttura SEO

Gerarchia heading pulita per la SEO on-page:

- **1× H1** — *Handcrafted Italian Putters, CNC-Milled in Brescia* (hero)
- **7× H2** — Why players choose our putters · About us · Shop Our Putters ·
  Optional Accessories · Fitters & Official Dealers · Contact Us · Join the Newsletter
- **H3** — singole feature, accessori, schede dealer/contatti

Inoltre:

- `pageSettings.metaDescription` e `pageTitle` precompilati.
- **Dati strutturati JSON-LD** (`Organization`, `WebSite`, `Product` con prezzi €52 / €21)
  iniettati via `customScriptsBodyFooter`.
- `customCss` con `scroll-behavior: smooth` e color selection brand.
- Ancore di sezione (`#shop`, `#about`, `#accessories`, `#dealers`, `#contact`, `#newsletter`).
- Testi `alt` descrittivi sui segnaposto immagine e `aria-label` sui pulsanti.

## Rigenerare il JSON

```bash
python3 generate_template.py
```
