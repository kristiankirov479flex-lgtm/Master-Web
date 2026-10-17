# Sunday Stems – flower shop design 3 (a weekly subscription)

Status (2026-10-17): **built.** A flower shop website with a **different business idea** from `Flower_Shop` and `Flower_Shop_2`: instead of choosing a single bouquet, the customer **subscribes** (every week, every two weeks or once a month). **New made-up content** ("Sunday Stems", Plovdiv). Bulgarian (`/`) and English (`/en/`). The other flower shops were not changed. The Plovdiv sample prices and the checklist for a real shop are in `../Flower_Shop/TODO.md`.

**Everything about the shop is an example**: name, prices, bouquets, texts, reviews, address and hours. Replace it for a real shop.

## Research behind the design (2026-10-17)

Roundups of florist websites (Colorlib's 2026 list, Webcitz, My Codeless Website, CyberOptik, Wix, Zarla, Clover) and a florist-software description agree on:

- **Strong photography and a clear path to buy.** Used: a big photo and one main button.
- **Filters by occasion, price or flower type** (Teleflora). Not used here (that is `Flower_Shop_2`).
- **A delivery date and time-window picker, same-day cut-offs, and add-ons** such as vases and cards (the florist-software pitch). Used: first-delivery dates, delivery windows, a vase add-on, a gift card, and a cut-off line ("Order by Thursday 12:00").
- **A rotating hero that follows holidays and seasons** (Clover merchant). Used: "this week's bouquet" changes by the week of the year.
- **Subscriptions** appeared only in a Squarespace template description, with no independent data. The subscription as the main idea is **my own choice**, not a finding.
- The sources are vendor and agency articles; they are opinions, not data.

## What is different

| Area | Flower_Shop (1) | Flower_Shop_2 | Flower_Shop_3 (this one) |
|---|---|---|---|
| Idea | order a bouquet | catalog by occasion and budget | **a flower subscription** with a price per delivery and per month |
| Look | arched photo, serif | full-width photo, serif | **two big colour blocks**, heavy Unbounded headlines, thick outlines and offset shadows |
| Home screen | headline and photo | photo with announcement bar | red (or green, pink, purple) block next to a photo, with a sticker showing this week's bouquet |
| Choosing | order estimator | cards with "Choose" | **five steps**: size, rhythm and length, extras (vase, gift), when and where, your details, and a **price slip** that updates |
| Calendar | none | none | **season calendar**: what is in bloom each month |
| Colour schemes | 5 | the same 5 | **5 new**: Tulip Red, Lemon and Leaf, Peony Pink, Iris Purple, Sage Green |

## How the builder works

- Prices (sample): Petite 18 €, Classic 28 €, Grand 42 € per delivery; 12 deliveries = 10% off, "until I stop" = 5% off; a vase is 12 € once; delivery in Plovdiv is free. Change them in `SIZES`, `LENS`, `VASE_PRICE` in `tools/build_pages.py`.
- The first delivery is at least two days ahead, on a Friday or Saturday. Delivery windows come from the mock server (`availability`).
- The request carries the plan summary, price per delivery, monthly cost, the address and the card message (`fulfil`, `address`, `card`).
- `WEEKLY` (six bouquets) and `MONTHS` (flowers in season) hold the content of "this week" and the calendar.

## The request system (mock server, replaceable by a real backend)

- `js/api.js` (`SundayAPI`) is a mock server using `js/config.js`. A request can answer 409 `slot_taken`. References look like `SS-0001`. `mode: "demo"` keeps data in this browser only and sends nothing. See `docs/API.md`. `admin.html` is a demo back office (no login).

## Colour schemes

The five round buttons at the bottom switch the site (`data-skin` on `<html>`); the choice is remembered (`sundaySkin`) and works as `?skin=iris`.

## Checked (2026-10-17)

- axe-core 4.10.2: no violations on the BG and EN home pages in all five colour schemes (1280 and 375 px), the admin page and the privacy pages (one contrast finding fixed).
- No horizontal overflow at 360, 768 and 1440 px; no requests to other sites.
- Flow tested: Grand size, 12 deliveries, vase, gift, delivery windows, a request with reference SS-0001 (37.80 € per delivery, 465.60 € in total).

## Not done / to do before real use

- Not tested on real phones, Safari (uses `:has()`) or screen readers.
- The deadline line assumes Saturday delivery and a Thursday 12:00 cut-off; adjust `nextDelivery` in `js/main.js` for the real rhythm.
- Subscriptions need real payment and pause/skip handling in a real backend; the demo only records the request.
- Photos are the free Unsplash placeholders (`images/CREDITS.md`); replace them with the shop's own. Replace prices, texts, address, phone, email and hours. Privacy page: fill in the yellow fields and get it reviewed.
- Add canonical/hreflang and `og:image` when the domain is known (comment in the page head).
