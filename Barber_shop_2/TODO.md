# Foundry Barbers – template notes and to-do (barbershop, version 2)

Status (2026-10-16): **built.** A second barbershop template with the **same five colour schemes** as `Barber_shop`, but a different structure, a different
headline font and a different way to book. Bulgarian (`/`) and English (`/en/`). The original `Barber_shop` was not changed. Brand "Foundry" is a placeholder.

For the research on what a barbershop site must do, the Plovdiv sample prices (section 5a) and the checklist for a real shop (section 8), read
`../Barber_shop/TODO.md`; everything not listed here is the same.

---

## What changed compared with `Barber_shop`

| Area | Barber_shop (v1) | Barber_shop_2 (this one) |
|---|---|---|
| Booking | form at the bottom of the page, estimator section | **booking drawer** that slides in from the right on every "Book" button: **service → barber → time → details** |
| Barbers | none | **"Pick your barber"** cards; each has "Book with ..." and the drawer lets you choose a barber or "any" |
| Free times | dropdown of times | **time chips** asked from the server for the chosen date, barber and visit length |
| Availability | capacity (number of chairs) | **per barber**: a barber can do one visit at a time; "any" picks the first free barber |
| Prices | two-column menu list | **tabs** (Hair, Beard and shave, Combos, Extras) with ticket-style rows, price and a Book button on every row |
| Gallery | masonry with filters | **horizontal rail** you can swipe, arrows, photo viewer with "Book this cut" |
| First screen | text left, framed photo | **huge stacked headline** (Oswald) and a **triptych** of three tall photos; live "open now" and "next free chair" under the buttons |
| Extra sections | none | **Monthly plans** (sample), a scrolling word strip, rating banner |
| Questions and contact | separate sections | one section: **hours with live "open now" status**, map and FAQ side by side |
| Header | wrap with centred links | solid bar, brass line under it, diamond mark in the logo |
| Font | Cormorant Garamond headings | **Oswald** (condensed, uppercase) |

Kept: five colour schemes (names, colours, buttons at the bottom), BG/EN, mock server with reference numbers (`FD-0001`), demo back office (it now shows the barber),
privacy notice, accessibility, no outside requests.

## Inspiration (research, 2026-10-16)

Roundups of barbershop websites (nanoglobals.com, cyberoptik.net, sliderrevolution.com, ueni.com, mycodelesswebsite.com, booknetic.com) agree on:

- **Booking at the top of every page and kept on the site** (an inline modal or embed, not a redirect). Used: the drawer, opened from the header, the hero, every price row and the phone bar.
- **Choose your barber** (Avenue Barbershop, Kutinfed: service → barber → time) and **barber profiles** (Church Barber & Apothecary). Used: team cards and the barber step.
- **Price and duration shown before choosing a time** (Heritage Barbershop, Entourage). Used: every row and every drawer option shows both, and the drawer shows a running total.
- **Dark, editorial look with strong type** (Barber & Co, Argyle League). Used: Oswald, big headline, dark schemes.
- **Memberships near the booking button** (Master Class Barber). Used: sample monthly plans.
- **Real reviews, a clear concept, a phone number in the header.** Used: rating banner, "Barbers and hot towel shaves" kicker, phone in the header.
- Not used: video hero (needs real footage), Facebook booking redirects (lost conversions according to the roundups).

## Font

**Oswald** (SIL Open Font License), self-hosted in `fonts/` (Latin + Cyrillic, one variable file for weights 500 – 700, about 33 KB). Downloaded from Google Fonts on
2026-10-16 with the owner's permission; the site makes no requests to Google. Body text stays Onest.

## How it is built

- `python tools/build_pages.py` writes `index.html`, `en/index.html` and `js/config.js`; `python tools/build_privacy.py` writes the privacy pages. Data at the top of
  `build_pages.py`: `BARBERS`, `SERVICES`, `EXTRAS`, `WORK` (photos), `PLANS`, hours, brand. The texts of both languages are in `L`.
- The drawer is in `tools/page_template.html` (`<dialog id="drawer">`) and `js/main.js` (state, validation per step, summary, confirmation). Any element with
  `data-book` opens it; `data-service="haircut"` and `data-barber="boris"` preselect and skip steps.
- `js/api.js` (`FoundryAPI`) now takes a barber: `availability(date, duration, barber)` and `createRequest({... barber})`. See `docs/API.md` ("Differences" at the top).
  Same-day times in the past are never offered.
- Live "open now" and "next free chair" are calculated in the browser from `js/config.js` and the mock server.

**Verified (2026-10-16):** main page (BG and EN), the drawer on steps 1 – 4, the back office and the privacy pages pass axe (WCAG 2.2 AA + best practice) in all 5 colour
schemes; full booking with real clicks and values (reference FD-0001); the barber rule (a booked barber disappears from his own list but "any" still offers the time until
all three are busy, then HTTP 409 `slot_taken`); 390 px layout without horizontal scroll; no outside requests.
**Not tested:** real phones, Safari (the drawer uses `<dialog>` and `:has()`), screen readers.

## Before using with a real barbershop

Same as `../Barber_shop/TODO.md` section 8, plus:

- [ ] Replace the barber names, photos, specialities and short texts with the real team (the three photos are stock photos of other people).
- [ ] The monthly plans are **invented sample plans**: replace them or delete the section (`#plans`) and its link in the menu.
- [ ] The rating banner says 5.0 as an example: replace it with the real Google rating or remove it.
- [ ] Decide how bookings are confirmed (demo mode sends nothing) and set `MODE = 'live'` with a backend that understands the `barber` field.
- [ ] Remove the colour-scheme buttons (the `dock` block) when the shop has chosen a scheme.

## Ideas not built yet

| # | Idea | Why |
|---|---|---|
| 1 | **Per-barber working hours and days off** | The mock server treats every barber as available during opening hours |
| 2 | **Add to calendar** (.ics) on the confirmation | One tap, fewer no-shows |
| 3 | **Reminder message** the day before | Needs a backend |
| 4 | **Online payment or deposit** for long services | Fewer no-shows |
| 5 | **Waiting list** when all chairs are taken | Fills cancelled times |
