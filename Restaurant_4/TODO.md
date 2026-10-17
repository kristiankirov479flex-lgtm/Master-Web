# Fornello – restaurant design 4 (a classic pizzeria)

Status (2026-10-17): **built.** A plain website for a **neighbourhood pizzeria**: a photo of the wood-fired oven, a menu with prices for three sizes, a short story about the dough and the oven, and a simple table reservation. **Made-up content** ("Fornello", Plovdiv). Bulgarian (`/`) and English (`/en/`). Takeaway is by phone (said on the page). It differs from `Restaurant_1` (an elegant restaurant with a booking bar) in look and in what it sells: pizza by size, in capitals, with a red top border.

**Everything about the pizzeria is an example**: name, pizzas, prices, hours, address and phone. Replace it for a real pizzeria.

## Research behind the design (2026-10-17)

Pizzeria-website guides (Pizza Today, Speedline Solutions, BeoHosting, CrowdSpring, Marketing360) agree on:

- **Location, phone number and hours visible without scrolling.** Used: a red call button in the header and a dark bar under the photo with today's hours, the address and the takeaway line.
- **A menu grouped into clear categories, with sizes and prices** (a menu without prices makes customers suspicious). Used: a table with three size columns for pizzas and plain lists for pasta, salads, desserts and drinks, with vegetarian marks.
- **Real photos of the food rather than stock images** (these are stock placeholders; replace them).
- **Reservations are optional for pizzerias; if offered, keep them visible.** Used: a simple reservation form and a link in the header and hero.
- The sources are practitioner articles; they are opinions, not data. Keeping the page **plain** follows the owner's request.

## What is deliberately plain

No animation, no live widgets, no sticky bars. One hero photo, Oswald headings in capitals, square-ish buttons. The only interactive part is the reservation form. The five colour schemes at the bottom are required for every site.

## How the reservation works

- The menu and prices are set at the top of `tools/build_pages.py` (`PIZZAS`, `OTHER`, `SIZES`, `HOURS`, `CAPACITY`, `BOOKING_MINUTES`, `MAX_PARTY`).
- The form uses a normal date field and a time list. Free times come from the mock server (`availability`): half-hour starts, a table is kept for 75 minutes, eight tables at the same time, 45 minutes of notice for a same-day booking. The page opens on the first day with a free table. A seating choice (inside or outside) is carried in the request.
- **Demo limitation:** the mock server counts bookings, not real tables. A real pizzeria needs a table plan.
- No online ordering; the page says to call for takeaway.

## The request system (mock server, replaceable by a real backend)

- `js/api.js` (`FornelloAPI`) is a mock server using `js/config.js`. A request can answer 409 `slot_taken`. References look like `FN-0001`. `mode: "demo"` keeps data in this browser only and sends nothing. See `docs/API.md`. `admin.html` is a demo back office (no login).

## Colour schemes

The five round buttons at the bottom switch the site (`data-skin` on `<html>`): Margherita (default), Diavola, Basil, Oven (dark) and Napoli. The choice is remembered (`fornelloSkin`) and works as `?skin=basil`.

## Checked (2026-10-17)

- axe-core 4.10.2: no violations on the BG and EN home pages in all five colour schemes (1280 and 375 px), the admin page and the privacy pages (the pizza table was reshaped so it fits a 360 px phone without scrolling sideways).
- No horizontal overflow at 360, 375, 768, 1280 and 1440 px; no requests to other sites (the map loads only after a click).
- Flow tested: a table for four outside, a request with reference FN-0001, visible in the demo back office.

## Not done / to do before real use

- Not tested on real phones, Safari or screen readers.
- No online ordering, no delivery and no table plan.
- The story ("built nine years ago", "oak wood", "48 hours") is invented; the owner must write the real one. Check allergen wording before publishing.
- Photos are free Unsplash placeholders (`images/CREDITS.md`); replace them with the pizzeria's own. Replace prices, texts, address, phone, email and hours. Privacy page: fill in the yellow fields and get it reviewed.
- Add canonical/hreflang and `og:image` when the domain is known (comment in the page head).
