# Desk & Drip – café design 3 (a café for working)

Status (2026-10-17): **built.** A website for a **work-friendly café**: the visitor picks a spot on a **floor plan**, chooses the hours and a free start time, and sees a price that **never goes above the day price**. **Made-up content** ("Desk & Drip", Plovdiv). Bulgarian (`/`) and English (`/en/`). This is a different idea from `Cafe_1` (order drinks) and `Cafe_2` (buy beans).

**Everything about the café is an example**: name, zones, prices, hours, events, texts, address and phone. Replace it for a real café.

## Research behind the design (2026-10-17)

Coworking directories and café-coworking examples (Coworking Cafe listings, The Albany, The Local) point to:

- **Hourly and day prices side by side.** Used: a price section with "by the hour", "day pass" and "week or month (ask us)".
- **Availability that is clear by place**, and support for both "buy a drink and sit" and paid desk time. Used: four zones with their own price and free times, and a drink included from two hours.
- **Many listings say "contact for pricing"** for regular seats. Used: a "week or month" card that says "ask us" and is not booked online.
- The sources are directories and listings, not usability studies; I found no independent data. The interactive floor plan, the day-price cap and the community timetable are **my own choices**.

## How the booking works

- Zones, seats, prices per hour and per day, events and amenities are set at the top of `tools/build_pages.py` (`ZONES`, `EVENTS`, `MAX_HOURS`, `COFFEE_FROM_HOURS`).
- Price = `min(price per hour × hours, day price)`. The slip shows the saving when the day price applies. A drink is included from two hours (two for the meeting table) and a bottomless filter from four hours.
- Pressing a zone on the plan selects it in the form. Free start times come from the mock server for exactly the chosen length (`availability`): every 30 minutes (`SLOT_MINUTES`), twelve bookings at the same time (`CAPACITY`), 15 minutes of notice for a same-day booking (`LEAD_MINUTES`).
- **Demo limitation:** the mock server counts *bookings*, not seats per zone. A real system needs seats per zone and a whole table for the meeting zone. Replace `freeSlots` on the server.
- The request carries the zone, hours, people (meeting table), needs (socket, second screen, calls, dog), the total and what is included (`plan`).

## The request system (mock server, replaceable by a real backend)

- `js/api.js` (`DeskAPI`) is a mock server using `js/config.js`. A request can answer 409 `slot_taken`. References look like `DD-0001`. `mode: "demo"` keeps data in this browser only and sends nothing. See `docs/API.md`. `admin.html` is a demo back office (no login).

## Colour schemes

The five round buttons at the bottom switch the site (`data-skin` on `<html>`): Paper (default, light), Ultramarine, Sage, Charcoal (dark) and Plum. The choice is remembered (`deskSkin`) and works as `?skin=ultra`.

## Checked (2026-10-17)

- axe-core 4.10.2: no violations on the BG and EN home pages in all five colour schemes (1280 and 375 px), the admin page and the privacy pages (one checkbox shrinking on a narrow phone fixed).
- No horizontal overflow at 360, 375, 768, 1280 and 1440 px; no requests to other sites (the map loads only after a click).
- Flow tested: the Quiet corner from the plan, 7 hours at 4 € = 28 € capped to the 18 € day price (saving 10 €), a drink and a bottomless filter included, a socket, a request with reference DD-0001, visible in the demo back office.

## Not done / to do before real use

- Not tested on real phones, Safari (uses `:has()`) or screen readers.
- No memberships, no passes bought online, no payment and no door or Wi-Fi access control.
- The plan is a drawing, not a map of the real room. Redraw the areas in `tools/design.css` (`.zone-*`) for the real layout.
- "13 sockets" in the first screen is a fixed example.
- Photos are free Unsplash placeholders (`images/CREDITS.md`); replace them with the café's own. Replace prices, texts, address, phone, email and hours. Privacy page: fill in the yellow fields and get it reviewed.
- Add canonical/hreflang and `og:image` when the domain is known (comment in the page head).
