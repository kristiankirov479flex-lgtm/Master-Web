# Lozeta – restaurant design 3 (a restaurant for events)

Status (2026-10-17): **built.** A plain website for a **restaurant that hosts weddings, christenings, birthdays and company events**: three halls with capacities, three menus priced per guest, photos, how it works, and an event request with a simple estimate. **Made-up content** ("Lozeta", Plovdiv). Bulgarian (`/`) and English (`/en/`). It does a different job from `Restaurant_1` (table reservation) and `Restaurant_2` (online food order): the visitor asks for an event and gets an offer.

**Everything about the restaurant is an example**: name, halls, capacities, menus, prices, hours, address and phone. Replace it for a real restaurant.

## Research behind the design (2026-10-17)

Private-dining and event guides (FSR Magazine, Tripleseat, Paperform templates, a catering lead-page guide) agree on:

- **Reply speed is the main lever**, and each enquiry should have one named owner. This is a process point, not a website feature; the TODO below says so.
- **Capture the right details up front** (date, guests, occasion, budget or menu, dietary needs). Used: an event form with those fields.
- **Be transparent about prices and what is included**, and publish logistics (minimums, lead time). Used: three menus with a price per guest, the hall fee below 40 guests and a note about dietary dishes.
- **Show each room with its capacity and what it suits.** Used: a card per hall with a photo and a guest limit.
- The sources are mostly software vendors and template sites; they are opinions, not data. Keeping the page **plain** follows the owner's request.

## What is deliberately plain

No animation, no live widgets, no sticky bars. One hero photo, centred headings in Cormorant, square-ish buttons. The only interactive part is the request form (with a one-line estimate). The five colour schemes at the bottom are required for every site.

## How the request works

- Halls, menus and prices, the hall fee, the minimum and maximum guests and the hours are set at the top of `tools/build_pages.py` (`HALLS`, `PACKAGES`, `SMALL_EVENT_FEE`, `FEE_BELOW`, `MIN_GUESTS`, `MAX_GUESTS`).
- Estimate = guests × the price of the chosen menu, plus the hall fee below 40 guests. It is a plain line of text, not a quote; "Not sure yet" shows no estimate.
- The date picker starts tomorrow. Free start times come from the mock server (`availability`) for a six-hour block (`EVENT_MINUTES`), with hourly starts and two events at the same time (one per hall, `CAPACITY`).
- **Demo limitation:** the mock server counts events, not which hall is free. A real system needs a calendar per hall.
- The request carries the occasion, guests, hall, menu and estimate (`plan`).

## The request system (mock server, replaceable by a real backend)

- `js/api.js` (`LozetaAPI`) is a mock server using `js/config.js`. A request can answer 409 `slot_taken`. References look like `LZ-0001`. `mode: "demo"` keeps data in this browser only and sends nothing. See `docs/API.md`. `admin.html` is a demo back office (no login).

## Colour schemes

The five round buttons at the bottom switch the site (`data-skin` on `<html>`): Ivory (default), Sage, Rose, Navy (dark) and Stone. The choice is remembered (`lozetaSkin`) and works as `?skin=sage`.

## Checked (2026-10-17)

- axe-core 4.10.2: no violations on the BG and EN home pages in all five colour schemes (1280 and 375 px), the admin page and the privacy pages.
- No horizontal overflow at 360, 375, 768, 1280 and 1440 px; no requests to other sites (the map loads only after a click).
- Flow tested: a wedding for 90 guests with the Premium menu: 90 × 52 € = 4,680 €, a request with reference LZ-0001, visible in the demo back office.

## Not done / to do before real use

- Not tested on real phones, Safari or screen readers.
- Someone must answer requests within a day and own each one; the website cannot do that.
- Deposits, contracts and a hall calendar are not included.
- Prices and the hall fee are examples. Photos are free Unsplash placeholders (`images/CREDITS.md`); replace them with photos of the real halls. Replace texts, address, phone, email and hours. Privacy page: fill in the yellow fields and get it reviewed.
- Add canonical/hreflang and `og:image` when the domain is known (comment in the page head).
