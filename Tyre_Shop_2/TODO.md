# Stoyanov Tyres – tyre shop design 2 (a family workshop)

Status (2026-10-17): **built.** A plain, practical website for a **family tyre workshop**: a big phone number, a clear price list, the kinds of new tyres, short advice on when to change, and a simple "ask for a price" form. **Made-up content** ("Stoyanov Tyres", Plovdiv). Bulgarian (`/`) and English (`/en/`). It does a different job from `Tyre_Shop_1` (Gripline): there a visitor books a job and sees a live price; here a visitor sees the prices on a list and asks for a quote.

**Everything about the workshop is an example**: name, story, prices, hours, address and phone. Replace it for a real workshop.

## Research behind the design (2026-10-17)

Tyre-shop website guides (Tire Review, NetDriven, Website Studio, SellMoreTyres) agree on:

- **Phone number, address and hours easy to find, with one-tap calling.** Used: a call button in the header on every screen size, a dark bar with today's hours under the photo.
- **A "request a quote" form** that pre-qualifies the customer. Used: the "Ask for a price" form (car, size, season, class, a day and time).
- **A clear service menu with prices builds trust and saves calls.** Used: a price list and a table of tyre-change prices by rim size. Net Driven notes that some shops prefer **not** to publish prices; this design publishes them and says so in the notes.
- **Storefront and workshop photos for first-time visitors, and reviews.** Photos are Unsplash placeholders; no reviews are included (add real ones only).
- The sources are vendor and magazine pieces; Tire Review is the most neutral. They are opinions, not data. Keeping the page **plain** follows the owner's request.

## What is deliberately plain

No animation, no live widgets, no sticky bars, no emoji. One hero photo with a white card, square-ish buttons, Nunito headings. The only interactive part is the form. The five colour schemes at the bottom are required for every site.

## How the request works

- Prices, rim table, tyre classes, hours and the story are set at the top of `tools/build_pages.py` (`SERVICES`, `CHANGE`, `KINDS`, `HOURS`).
- The form uses a normal date field and a time list. Free times come from the mock server (`availability`): half-hour starts, 45 minutes per visit, two cars at the same time, 30 minutes of notice for a same-day visit.
- The request carries the car, tyre size (optional), season, class and the summary (`plan`). No payment; the shop calls back with a price.
- **Demo limitation:** the page does not calculate a price. The "typical price of a 16″ tyre" on the cards is a fixed example.

## The request system (mock server, replaceable by a real backend)

- `js/api.js` (`StoyanovAPI`) is a mock server using `js/config.js`. A request can answer 409 `slot_taken`. References look like `ST-0001`. `mode: "demo"` keeps data in this browser only and sends nothing. See `docs/API.md`. `admin.html` is a demo back office (no login).

## Colour schemes

The five round buttons at the bottom switch the site (`data-skin` on `<html>`): Blue (default), Red, Green, Graphite (dark) and Amber. The choice is remembered (`stoyanovSkin`) and works as `?skin=red`.

## Checked (2026-10-17)

- axe-core 4.10.2: no violations on the BG and EN home pages in all five colour schemes (1280 and 375 px), the admin page and the privacy pages (a header that overflowed on phones and some image sizes fixed).
- No horizontal overflow at 360, 375, 768, 1280 and 1440 px; no requests to other sites (the map loads only after a click).
- Flow tested: a Toyota Yaris, 185/65 R15, winter, mid-range, a request with reference ST-0001, visible in the demo back office.

## Not done / to do before real use

- Not tested on real phones, Safari or screen readers.
- The story ("since 2008", "we do not sell what you do not need") is invented; the owner must write the real one.
- Prices and tyre classes are examples. A real shop should check them against its own list and VAT status.
- Photos are free Unsplash placeholders (`images/CREDITS.md`); replace them with the workshop's own. Replace texts, address, phone, email and hours. Privacy page: fill in the yellow fields and get it reviewed.
- Add canonical/hreflang and `og:image` when the domain is known (comment in the page head).
