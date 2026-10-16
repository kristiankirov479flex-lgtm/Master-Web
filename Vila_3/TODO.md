# The Stone Cellar – a third guest house design (Vila_3)

Status (2026-10-16): **built.** A guest house website in a **third design**, different from `Vila-Stefani-Devin-main` and from `Vila_2`, with **new made-up content**:
a fictional guest house in a restored stone barn among vineyards ("The Stone Cellar" / "Каменната изба"). Bulgarian (`/`) and English (`/en/`).
The other two guest house sites were not changed, and none of their text, data or images were reused.

**Everything about the house is an example**: name, story, places to sleep, sizes, prices, activities, notes and the address. Replace it for a real guest house.

---

## What is different

| Area | Vila Stefani (original) | Vila_2 (Linden House) | Vila_3 (The Stone Cellar) |
|---|---|---|---|
| Layout idea | one page, top bar | side bar, journal feel | **full-screen chapters**: a big photo cover, then alternating night and cream chapters |
| Menu | top bar | fixed side bar | **full-screen menu** with large numbered links (a native `<dialog>`) |
| Colours | brown and terracotta | forest green, linen, clay | **night brown, cream, wine red and gold** |
| Type | Cormorant Garamond | Playfair Display | **Alegreya** (calligraphic serif, italic accent words) |
| Places to sleep | one room | three rooms in rows | four places as **cards that stack on top of each other while you scroll** |
| Booking | hidden form | date fields and free-room tags | a **calendar**: press the arrival day, then the departure day; days are coloured **free, partly booked, fully booked**; two months side by side (one on phones) |
| Booking bar | – | – | an **always-there bar** ("From 60 € per night" and a button) that steps aside while the booking section is on screen |
| Experiences | – | A day here, seasons | **Do**: four photo tiles (tasting, harvest, walks, dinners), all "on request" |
| Gallery | grid | mosaic | **contact sheet** of squares with captions in the viewer |
| Reviews | Google reviews | one at a time | a **guestbook**: paper notes, slightly turned, with tape |

## The enquiry system (mock server, replaceable by a real backend)

- `js/api.js` (`CellarAPI`) is a mock server. It knows the places from `js/config.js`, answers `availability(checkin, checkout, guests)` (each place free, taken or too small),
  `occupancy(from, to)` (how many places are free each night; used to colour the calendar) and creates enquiries with reference numbers `SC-0001`.
- A stay occupies the **nights** from arrival up to (not including) departure, so a guest can arrive the day another leaves. Declined enquiries free the place again.
- Rules: arrival not in the past, departure after arrival, at most `MAX_NIGHTS` (30), guests not more than the place sleeps, no double booking (HTTP 409 `room_taken`).
  Totals are estimates at the example prices; the page says the host confirms the final price.
- A fully booked day cannot be picked as an arrival day, but can be the departure day.
- In demo mode enquiries live in the visitor's browser and **nothing is sent to anyone**. See `docs/API.md` (it includes the new `occupancy` endpoint and the SQL table).

## Photos

18 free Unsplash photos (Unsplash License), only ones marked **Free**. Placeholders; see `images/CREDITS.md` (photographer names come from the search listings, so check the links).
One file name is misleading: `old-wooden-bed.jpg` is really an old wine press (the original Unsplash title said "old wooden bed").

## Font

**Alegreya** (SIL Open Font License), self-hosted in `fonts/` (Latin + Cyrillic, upright and italic, about 105 KB with Onest). Downloaded from Google Fonts on 2026-10-16 with the owner's
permission; the site makes no requests to Google. Body text is Onest.

## How it is built

- Static files. `python tools/build_pages.py` writes `index.html`, `en/index.html` and `js/config.js`; `python tools/build_privacy.py` writes the privacy pages. Data at the top of
  `build_pages.py`: `UNITS`, `UNIT_TEXT`, `DO`, `GALLERY`, `NOTES`, times, contact placeholders; both languages in `L`.
- No cookies, no analytics, no third-party requests (the map loads only after a click), so no cookie banner is needed.

**Verified (2026-10-16):** main page in both languages including the error state, the full-screen menu and the photo viewer; the back office and both privacy pages: all pass axe
(WCAG 2.2 AA + best practice; one finding fixed: the booking bar is now a labelled landmark). A full enquiry with real clicks on the calendar (SC-0001): the days turn partly booked, then
fully booked and disabled when all four places are taken, while the departure day stays free; the guest count disables places that are too small; 390 px layout with one month and no horizontal
scroll; no outside requests. **Not tested:** real phones, Safari (uses `<dialog>`, `:has()` and `position: sticky`), screen readers.

## Before using for a real guest house

- [ ] Replace name, story, numbers, address, phone, email, places (sizes, beds, prices, amenities), breakfast price, FAQ answers and times.
- [ ] Replace all photos and their texts and captions; replace the guestbook notes with real reviews (with permission).
- [ ] Fill the yellow fields in the privacy notices, then remove `noindex`. Tastings and dinners may need food and alcohol permits: check with the owner.
- [ ] Real domain: canonical and hreflang links, `og:image`, sitemap.
- [ ] Decide how enquiries reach the host (in demo mode they do not). Connect a backend (`MODE = 'live'`, `docs/API.md`) with email to the host and the guest.
- [ ] Seasonal prices (harvest season), minimum stays, a deposit, and an iCal feed to sync Booking.com or Airbnb.

## Ideas not built yet

| # | Idea | Why |
|---|---|---|
| 1 | **Gift vouchers** (a night, a tasting) | Wine and stays are popular gifts |
| 2 | **Tasting booking** with its own calendar and group size | Visitors who do not stay overnight |
| 3 | **Harvest sign-up** with dates and places | Limited spaces, repeat guests |
| 4 | **Wine shop** or a "take a bottle home" request | Extra income |
| 5 | **Guest photo wall** (with permission) | Social proof |
