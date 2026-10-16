# Lumi Nail Studio – template notes and to-do (nail studio, version 2)

Status (2026-10-16): **built.** A second nail studio template with the **same five colour schemes** as `Nail_Salon_1`, but a different structure, a different
headline font and a different way to choose services. Bulgarian (`/`) and English (`/en/`). The original `Nail_Salon_1` was not changed. Brand "Lumi" is a placeholder.

For the research on what a nail studio site must do, the Plovdiv sample prices (section 5a), the photos and the checklist for a real salon (section 8), read
`../Nail_Salon_1/TODO.md`; everything not listed here is the same.

---

## What changed compared with `Nail_Salon_1`

| Area | Nail_Salon_1 (v1) | Nail_Salon_2 (this one) |
|---|---|---|
| Layout idea | one long page of full-width sections | **bento**: the first screen and the closing sections are made of rounded tiles of different sizes |
| Header | bar across the page | **floating pill** that stays near the top |
| First screen | headline and one arched photo | six tiles: headline, big photo, **"next free time"** (asked from the server), **"open today"** with live status, second photo |
| Choosing services | price list, then a separate "Plan your visit" estimator | **one visit builder**: tabs (Hands, Extensions, Feet, Extras), **tick several services**, a card on the right adds up price and time; a badge on each tab shows how many are ticked |
| Free times | date, then a dropdown | **"Next free times" chips** over the next 14 days for the length of the visit; pick a chip or choose the date yourself |
| Gallery | masonry with filters | **grid of squares** with a "Request this look" label on hover, same filters and photo viewer |
| Reviews | three cards in a band | **cards drifting sideways** (pause on hover; still and wrapped when motion is reduced) |
| Questions | list | **cards** that open |
| Booking | contact details left, form right | **dark booking band** with the quick times and the form; address, hours and map move to three tiles below |
| Font | Cormorant Garamond headings | **Unbounded** (wide, rounded, modern) |

Kept: five colour schemes (names, colours, buttons at the bottom), BG/EN, "request this look", the mock server with reference numbers (`LU-0001`), the demo back office,
privacy notice, accessibility, no outside requests.

## Inspiration (research, 2026-10-16)

Roundups of nail salon websites (colorlib.com, hubspot.com, mycodelesswebsite.com, moneris.com, cyberoptik.net) name these patterns:

- **Minimal layouts with plenty of white space and large photos** (Artiva Nails, Nail Garden, The Best Nails Miami).
- **Animated marquee banners and review marquees** (Varnish Nail Shoppe, Tropical Popical, DBCN). Used: word strip and sideways reviews.
- **Pastel gradients and circular or soft shapes** (NAF! Salon, Sugarcoat Beauty). Used: gradient headline tile, pill shapes, large corner radius.
- **Colour blocks and split layouts** (Ama The Salon). Used: dark booking band against light sections.
- **Transparent pricing, also for memberships** (UL Nails & Spa, Nail Garden). Used: every service shows time and price, and the visit card shows the total.
- **A visible booking button near the top** (Park Slope Nails). Used: pill header and hero buttons.
- A **bento grid** was **not** named in any of these sources; I used it because it is a current layout trend for single-page sites. Treat it as my choice, not as research.

## Font

**Unbounded** (SIL Open Font License), self-hosted in `fonts/` (Latin + Cyrillic, one variable file for weights 500 – 700, about 82 KB). Downloaded from Google Fonts on
2026-10-16 with the owner's permission; the site makes no requests to Google. Body text stays Onest.

## How it is built

- `python tools/build_pages.py` writes `index.html`, `en/index.html` and `js/config.js`; `python tools/build_privacy.py` writes the privacy pages. Data at the top of
  `build_pages.py`: `ITEMS` (services with minutes, price range and kind: fixed, from, per nail, on request), `GALLERY`, hours, capacity, `LEAD_MINUTES`, brand. Texts in `L`.
- The visit builder is plain checkboxes (`js/main.js`: `totals()`, `renderBuilder()`). Price shows "from" when a ticked service has a minimum price and "plus nail art" when
  one is on request. The length of the visit is the **longest** time of each ticked service added together, and it drives the free-time list.
- The "next free time" tile and the quick-pick chips ask `LumiAPI.availability(date, duration)` for the next days. Same-day times in the past are never offered
  (`leadMinutes` in `js/config.js` adds notice).
- Order system: the same mock server as `Nail_Salon_1` (`js/api.js`, `docs/API.md`, `js/admin.js`); names `LumiAPI`, `lumi.requests`, reference `LU-0001`.

**Verified (2026-10-16):** main page (BG and EN), back office and privacy pages pass axe (WCAG 2.2 AA + best practice) in all 5 colour schemes (one finding fixed: the visit
card was a nested `<aside>`); ticking, removing, tab badges, price "from/range/on request", quick times, a full request with reference LU-0001; 390 px layout without
horizontal scroll; no outside requests.
**Not tested:** real phones, Safari (uses `:has()`), screen readers.

## Before using with a real salon

Same as `../Nail_Salon_1/TODO.md` section 8, plus:

- [ ] Replace the 10 placeholder photos (`images/CREDITS.md`). Tiles crop to squares, so each photo needs a clear centre.
- [ ] Check the "Next free time" tile and the quick times with the real opening hours and number of technicians (`CAPACITY`).
- [ ] The review cards loop; with only three real reviews, remove the duplicate row or add more.
- [ ] Remove the colour-scheme buttons (the `dock` block) when the salon has chosen a scheme.

## Ideas not built yet

| # | Idea | Why |
|---|---|---|
| 1 | **Technician choice** (see Barber_shop_2) | Clients are loyal to a person |
| 2 | **Gift vouchers and a rewards stamp card** (AKIKO Nails) | Repeat visits |
| 3 | **Instagram feed** in the gallery | Fresh photos without editing the site |
| 4 | **Add to calendar** (.ics) on the confirmation | Fewer no-shows |
| 5 | **Shop for polish and care products** | Extra income, bigger project |
