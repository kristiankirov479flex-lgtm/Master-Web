# Verbena Flowers – template notes and to-do (flower shop, version 2)

Status (2026-10-16): **built.** A second flower-shop template with the **same five colour schemes and the same order system** as `Flower_Shop`,
but a different structure and look, so the portfolio does not show the same page twice. Bulgarian (`/`) and English (`/en/`). Brand "Verbena" is a placeholder.

Everything not listed here (prices, order system, back office, privacy notice, API) is the same as in `../Flower_Shop/TODO.md`; read that file for the research on
what a flower shop site must do, the Plovdiv sample prices (section 5a) and the checklist for a real shop (section 8).

---

## What changed compared with `Flower_Shop`

| Area | Flower_Shop (v1) | Flower_Shop_2 (this one) |
|---|---|---|
| First screen | split: headline left, arched photo right | **full-width photo** with the headline on it, header on top of the photo |
| Header | logo left, links right | **centred logo**, links split left and right, phone number in the header; turns solid when scrolling, **hides when scrolling down and returns when scrolling up** |
| Cut-off countdown | pill in the hero | **announcement bar above the header** (always visible at the top of the page) |
| Choosing | gallery and a separate price list | **one catalog**: photo, name, price, preparation time and a "Choose" button on every card |
| Navigation by need | none | **Shop by occasion** (arched photo tiles) and filters by occasion and by budget |
| Extras and delivery | rows in the price list | two short lists under the catalog |
| Steps | three promises in a strip | **numbered steps** next to two overlapping shop photos |
| Reviews | three equal cards | **one large pull quote** and two smaller |
| FAQ | heading left, list right | two-column list under the heading |
| Order section | details left, form right | **form first**, details and map in a sticky column beside it |
| Footer | one line | **big wordmark** and a line of links |
| Headline font | Cormorant Garamond | **Playfair Display** (with italic accent words) |

Kept: the five colour schemes (names, colours and the buttons at the bottom), BG/EN, the order estimator ("Make it yours"), pick-up or delivery with address and card
message, same-day cut-off, mock server with reference numbers (`VB-0001`), demo back office, privacy notice, accessibility, no outside requests.

## Inspiration (research, 2026-10-16)

There is **no single authoritative ranking of "the best flower shop website in the world"**; the roundups I found are blogs and vendor lists.
What they keep praising, and what was used:

- **Big, bold photography first**, with a sticky menu that changes from transparent to solid on scroll (Floral Ink, Fine Blooms, Gosha). Used: full-width hero and header.
- **Menu that hides when scrolling down and shows when scrolling up** (The Botanist). Used.
- **Shop by occasion, plus a finder by occasion and budget** (FTD, Flower Chimp, Juniper Flowers). Used: occasion tiles and two filters.
- **Delivery cost or cut-off in a banner above the menu** (Tonic Blooms). Used: announcement bar.
- **Clickable phone number in the header** (Scotts Flowers, Bloomex). Used.
- **Hover effect on bouquets with prices** (The Unlikely Florist, Teleflora). Used: photo zoom and price under every photo.
- **Editorial feel: serif type, overlapping images, generous white space, dark and light sections** (Gypsy Floral, Jordan Flowers & Events, Gosha, Young Flowers).
  Used: Playfair Display, overlapping photos, big wordmark in the footer.
- **Reviews and clear prices as trust signals** (Arena Flowers). Used: large quote.
- **Subscriptions and a "daily flower menu"** (Native Poppy): not built, see ideas below.

Sources: vandelaydesign.com/florist-websites, colorlib.com/wp/florist-websites, zarla.com (florist website examples), wix.com/blog/florist-websites,
awwwards.com (florist examples), curate.co (best florist website design). I could not open the named brands (McQueens, Bloom & Wild, Moyses Stevens) and did not
copy any layout; only general patterns were used.

## Font

**Playfair Display** (SIL Open Font License), self-hosted in `fonts/` (Latin + Cyrillic, upright and italic, about 96 KB with Onest). Downloaded from Google Fonts on
2026-10-16 with the owner's permission; the site makes no requests to Google. Body text stays Onest.

## How it is built

- Same generator approach: `python tools/build_pages.py` writes `index.html`, `en/index.html`, `js/config.js` from `tools/page_template.html` and the text in
  `tools/build_pages.py`; `python tools/build_privacy.py` writes the privacy pages. Settings at the top of `build_pages.py` (hours, capacity, `LEAD_MINUTES`, `CUTOFF`, brand).
- Catalog cards come from the first two menu groups (`MENU_EN` / `MENU_BG`) plus `CAT_META` (occasions and photo per item, same order). Extras and delivery
  (the menu groups marked "not selectable") become the two lists under the catalog. Add an item = add a menu row and a `CAT_META` row.
- Occasion tiles: `OCCASIONS`. Budget filter: under 25 €, 25 – 45 €, over 45 € (items "on request" show only under "Any budget").
- "Choose" puts the item and its photo into the order form (and the photo viewer has the same button).
- Header on the privacy and back office pages is a plain bar (`class="top scrolled static"`).

**Verified (2026-10-16):** BG and EN main page, back office and privacy pages pass axe (WCAG 2.2 AA + best practice) in all 5 colour schemes (two findings were fixed:
a decorative footer word and the announcement bar not being in a landmark); filters (occasion, budget, empty state), occasion tiles, "Choose", photo viewer and the full
order flow with a reference number; 390 px layout without horizontal scroll; no outside requests.
**Not tested:** real phones, Safari, screen readers, the header hide-on-scroll on a touch device.

## Before using with a real flower shop

Same as `../Flower_Shop/TODO.md` section 8, plus:

- [ ] Replace the 19 placeholder photos (`images/CREDITS.md`). The catalog needs **one real photo per item**; some placeholders are only the closest match
  (the basket, the flower box and the orchid use other arrangements, and the dried bouquet and tulip photos are approximate).
- [ ] The hero photo is the first thing visitors see: use a bright, sharp photo of the shop's own work, wide format (at least 1600 px).
- [ ] Check legibility of the headline over the real hero photo in all five colour schemes (the dark overlay follows the scheme).
- [ ] Remove the colour-scheme buttons (the `dock` block) when the shop has chosen a scheme.

## Ideas not built yet

| # | Idea | Why |
|---|---|---|
| 1 | **Subscription** (flowers every week or month) and a **flower of the day** | Repeat income (Native Poppy does this) |
| 2 | **Hover quick view** with a second photo of each bouquet | More photos per item = more trust |
| 3 | **Search by recipient** ("for her", "for mum", "for the office") | Another way into the catalog |
| 4 | **Peak-day mode** (8 March, 14 February) with a banner and different hours | Peaks are most of the year's income |
| 5 | **Online payment or deposit** | Fewer unconfirmed orders |
