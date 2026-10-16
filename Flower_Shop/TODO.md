# Mimosa Flowers – template notes and to-do

Status (2026-10-16): **version 1 built.** One-page site in Bulgarian (`/`) and English (`/en/`), 5 colour schemes with buttons at the bottom,
bouquet and price list, "Build your order" estimator, "Order something like this" from the gallery, **pick-up or delivery** with address and card message,
a **same-day cut-off countdown**, and the same **backend-style request system** as the other templates (mock server in the browser, confirmation with
reference number, availability, demo back office). Brand name "Mimosa" (the national flower of March 8 in Bulgaria) is a placeholder.

This is a **template to sell to different flower shops**. No client asked for it yet; it is portfolio work. Photos are free stock photos, prices are
sample prices from Plovdiv. Nothing is sent to anyone in demo mode.

---

## 1. What a flower shop site must do (research summary)

A flower shop sells **an occasion**, usually in a hurry. The visitor wants: see it, choose it, know the price, know it will arrive on time.

1. **Photos sell.** Real bouquets, well lit, not over-edited. Gallery with a viewer is the main tool.
2. **Price visible for every item**, and the **delivery cost shown before the order is sent** (compare the total, not only the bouquet price).
3. **Same-day cut-off stated clearly** ("order before 15:00 for delivery today"). Here it is calculated live in the browser from the opening hours.
4. **Choose a date and a time window**, also for later days (birthdays, anniversaries, 8 March).
5. **Greeting card text and delivery notes** (recipient, address, what if nobody is home).
6. **Mobile first.** Most orders come from a phone, often late and in a hurry.
7. **Seasons and peaks** (8 March, Valentine's Day, 1 September, Easter): extra stock and a clear note that flowers change with the season.
8. Updates after the order (confirmation, "on the way", delivered, ideally with a photo): needs a backend.

Colour research: restrained palette with one or two accents so **the flowers provide the colour**; green (sage) as anchor works with every flower colour;
warm neutrals as background; avoid a loud brand colour that competes with the flowers. No conversion studies for florists were found; the choice is judgment.
Pages used: bluewhalemedia.co.uk (florist colour palette), blog.clover.com (florist website design tips), lovart.ai (florist brand kit),
beohosting.com (online florist site), colorwhistle.com (florist website features and cost), merchants.doordash.com (online flower delivery tips).
Many of these are vendor blogs, so figures were not used.

## 5a. Plovdiv sample prices (EUR, from online listings, 2026-10-16)

Sources (florists with Plovdiv delivery): flowerroom.bg, vanillabg.com, цветя-вазов listing, mireya.bg, e-cvetia.com, samorozi.com. Converted from BGN at 1.95583 where needed.
Listings are from different dates and shops; treat as a **range**.

| Item | Seen | Used in template |
|---|---|---|
| Roses (3 / 5 / 7 / 11 stems) | 25 / 36 / 50 / 72 BGN = about 13 / 18 / 26 / 37 € | 5: 20 €, 7: 26 €, 11: 38 €, 21: 70 € |
| Premium roses (35 stems) | 235 € (about 6.7 € per stem) | not used |
| Mixed / small bouquets | 59 BGN (about 30 €) "Нежност"; 79 BGN (about 40 €) 7 roses with gypsophila | 30 – 55 € |
| Basket of red roses | 60 € | basket from 45 € |
| Custom gypsophila bouquet | 30 € | – |
| Delivery in Plovdiv | next day 15 BGN (about 7.7 €), express 25 BGN (about 12.8 €); another site from 15.47 € | 7 € chosen day, 12 € express |

Not found in sources (**estimates**, marked "sample" on the page): tulip bouquet, dried bouquet, flower box, orchid in a pot, vase, chocolates, gift wrapping.

## 5c. Photos

22 free photos from Unsplash (Unsplash License: free for commercial use, attribution not required, may be modified, may not be sold unaltered).
Only photos marked **Free** were used (Getty / "Unsplash+" ones need a paid licence). One museum painting from the search was **not** used.
See `images/CREDITS.md`. Downloaded at 1600 px wide and recompressed, plus 800 px versions. **All are placeholders**: the real shop uses its own photos.

## 5d. The five colour schemes (switch buttons at the bottom of the page)

All pairs contrast-checked (WCAG AA). Axe audit passes in all five on both language pages, the back office and the privacy page.
Terracotta's accent was darkened to `#97402A` after the audit found `#A64B2E` too pale on the soft section background.

| Key | Name (EN / BG) | Background | Text | Accent | Mood | Best for |
|---|---|---|---|---|---|---|
| `sage` (default) | Sage & Linen / Шалфей и лен | `#F5F3EC` | `#232B25` | `#4A6B54` | natural, calm, goes with every flower | almost any shop (most likely sale) |
| `rose` | Rosewater & Cream / Розова вода и сметана | `#FBF5F2` | `#2E2024` | `#A23A5B` | romantic, classic | wedding and gift florists |
| `terracotta` | Terracotta & Linen / Теракота и лен | `#F6F0E7` | `#2C211B` | `#97402A` | warm, modern, earthy | dried flowers, boho, plants |
| `lavender` | Lavender & Mist / Лавандула и мъгла | `#F5F3F9` | `#231F33` | `#6A4C9C` | soft, creative | boutique studios |
| `botanical` (dark) | Evening Botanical / Вечерна ботаника | `#14201A` | `#EDF1EA` | `#EDA9B6` | moody, luxury | premium and event florists |

The choice is saved in the browser (`localStorage` key `flowerSkin`); `?skin=rose` forces one. The switch is a **template preview feature**:
remove the `<aside class="dock">` block once a shop has chosen.

## 5e. How the site is built

- Static files, no build tools. `tools/build_pages.py` writes `index.html`, `en/index.html` and `js/config.js` from one template and two text dictionaries
  (`tools/build_privacy.py` does the privacy pages). Constants at the top: hours, phone, email, capacity (3 orders prepared at once), slot gap (30 min),
  `LEAD_MINUTES` (same-day notice, 120), `CUTOFF` (15:00), brand, mode.
- Fonts self-hosted (Cormorant Garamond and Onest, Latin + Cyrillic). No third-party requests; the map loads only after a click.
- Look: arched photos, soft round shapes (same family as the nail template, but greens and a dark "botanical" scheme).
- Gallery filter Bouquets / In a vase / The shop; "Order something like this" in the viewer (hidden for shop photos).
- Build your order: choose a bouquet (roses have a stem count), extras; shows estimated price and **preparation time**; "Add to my order" fills the form
  and limits times to those that fit before closing. The delivery fee is not in the estimate; the note says it is added on confirmation.
- Form: pick-up or delivery (address required only for delivery), date, time, card message, notes.
- Same-day cut-off badge in the hero: "Order within 4 h for delivery today" or "Today's delivery orders are closed. Order now for tomorrow."
  Uses the browser clock, the opening hours and `cutoff` / `leadMinutes` from `js/config.js`.
- Order system: `docs/API.md` (names `MimosaAPI`, `mimosa.requests`, reference `MI-0001`). Same-day times start at "now + lead time"; capacity 3.
  Delivery orders without an address get HTTP 422.
- Demo back office `admin.html` (English `?lang=en`) shows pick-up or delivery, address and card message. Demo only: no login.

**Verified (2026-10-16):** BG and EN pages, back office and privacy pages pass axe (WCAG 2.2 AA + best practice) in all 5 schemes; full order flow with real form
values (reference MI-0001, delivery address required, card message, availability); same-day lead time and cut-off badge checked with a simulated clock
(11:00 gives "4 h" and first time 13:00); 390 px layout without horizontal scroll; no outside requests.
**Not tested:** real phones, Safari, screen readers.

## 8. Before using with a real flower shop

- [ ] Replace placeholders: name (Mimosa), address, hours, phone, email, prices, delivery fees and areas, cut-off time, FAQ answers, example reviews.
- [ ] Check the promises in the text are true for the shop ("made when you order", "flowers of that day").
- [ ] Replace all photos with the shop's own and update `alt` texts in `GALLERY`; remove `images/stock` and `images/CREDITS.md` if unused.
- [ ] Fill the yellow fields in the privacy notices (they must cover recipient names, addresses and card messages), then remove `noindex`.
- [ ] Real domain: canonical and hreflang links, `og:image`, sitemap, robots.
- [ ] Decide: connect a real backend (`MODE = 'live'`, `docs/API.md`) or replace the form. **In demo mode nothing reaches the shop.**
- [ ] Delivery zones (villages around Plovdiv have different fees), delivery windows, holidays (8 March, 14 February) with different hours.
- [ ] Remove the colour-scheme buttons (the `dock` block) when the shop has chosen a scheme.
- [ ] Test on real phones and with a screen reader.
- [ ] Google Business Profile, review link / QR code, Instagram link.

## 9. Ideas not built yet

| # | Idea | Why |
|---|---|---|
| 1 | **Online payment** (card, or deposit) | Fewer unconfirmed orders; needs a payment provider |
| 2 | **Delivery status messages** (confirmed, on the way, delivered with a photo) | Gives the sender peace of mind; needs a backend |
| 3 | **Occasion shortcuts** (birthday, 8 March, wedding, sympathy) | Many visitors start from the occasion, not the flower |
| 4 | **Subscription** (fresh flowers every week or month for homes and offices) | Repeat income |
| 5 | **Reminders** (send me a message a week before an anniversary) | Needs a backend; very strong retention |
| 6 | **Stock for peak days** (show what is still available on 8 March) | Needs live data |
| 7 | **Review button + printable QR code** | Reviews drive "flower shop near me" ranking |
