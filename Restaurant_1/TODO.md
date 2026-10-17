# Maslina – restaurant design 1 (menu, lunch and table reservation)

Status (2026-10-17): **built.** A website for a **restaurant** whose main idea is **reserving a table in a minute**: a booking bar in the first screen, a menu with category and diet filters, a daily lunch menu, and a reservation builder that shows free times for the party size. **Made-up content** ("Maslina", Plovdiv). Bulgarian (`/`) and English (`/en/`).

**Everything about the restaurant is an example**: name, dishes, prices, hours, texts, address and phone. Replace it for a real restaurant.

## Research behind the design (2026-10-17)

Restaurant-website guides (Azuro Digital, Gourmet Marketing, DoorDash for Merchants, Sauce, Network Solutions, StudioMeyer) agree on:

- **A booking call to action that is always visible**, not hidden in a contact form. Used: a booking bar at the bottom of the first screen, a "Reserve" button in the header, and a Reserve bar on phones that appears after the first screen.
- **A readable HTML menu (not a PDF), grouped clearly, with dietary filters.** Used: a two-column menu with dotted price leaders, category chips and Vegetarian / Vegan / Gluten-free toggles.
- **Hours, address and click-to-call without scrolling.** Used: an open/closed pill, a today-highlighted hours table, a phone link and a map that loads only after a click.
- **Real photos build trust; mobile first; fast pages.** Used: large photography, responsive images and no scripts or fonts from other companies.
- The sources are vendor and agency articles; the percentages they quote have no primary source. They are opinions, not data. The lunch menu, the signature dishes and the ticket-style reservation card are **my own choices**.

## How the reservation works

- `MENU`, `CATS`, `DIETS`, `OCCASIONS`, `ALLERGIES` and the lunch menu live in `tools/build_pages.py`. `V` includes vegan dishes when the vegetarian filter is on.
- The booking length depends on the party: up to 4 guests 90 min, up to 6 guests 105 min, more 120 min (`duration()` in `js/main.js`). Free times come from the mock server (`availability`): every 30 minutes (`SLOT_MINUTES`), eight tables (`CAPACITY`), one hour of notice for a same-day booking (`LEAD_MINUTES`). Times are split into lunch and dinner.
- The request carries the party size, seating (any / inside / terrace), occasion, allergies and a summary line (`plan`). Parties above `MAX_PARTY` are asked to call.
- A real restaurant needs a **table plan** (which table fits how many guests, joined tables, turn times). The demo only counts parallel bookings. Replace `freeSlots` on the server.
- Hours and capacity are set at the top of `tools/build_pages.py`; run `python tools/build_pages.py && python tools/build_privacy.py` after changing them.

## The request system (mock server, replaceable by a real backend)

- `js/api.js` (`MaslinaAPI`) is a mock server using `js/config.js`. A request can answer 409 `slot_taken`. References look like `MS-0001`. `mode: "demo"` keeps data in this browser only and sends nothing. See `docs/API.md`. `admin.html` is a demo back office (no login).

## Colour schemes

The five round buttons at the bottom switch the site (`data-skin` on `<html>`): Olive (default, light), Bordeaux (dark), Terracotta, Sea and Brass (dark). The choice is remembered (`maslinaSkin`) and works as `?skin=sea`.

## Checked (2026-10-17)

- axe-core 4.10.2: no violations on the BG and EN home pages in all five colour schemes (1280 and 375 px), the admin page and the privacy pages (heading order, tap targets, one contrast finding and a mobile overflow on the static header fixed).
- No horizontal overflow at 360, 375, 768, 1280 and 1440 px; no requests to other sites (the map loads only after a click).
- Flow tested: menu filters (Mains + Vegan shows one dish), the booking bar, 4 guests on the terrace, a birthday, gluten-free, a request with reference MS-0001, visible in the demo back office.

## Not done / to do before real use

- Not tested on real phones, Safari (uses `:has()`) or screen readers.
- No table plan, no deposits and no confirmation emails or SMS. A real system needs them on the server.
- The lunch menu and the signature dishes are static text; change them in `tools/build_pages.py` or connect them to the back office.
- Allergy information on a restaurant website has legal rules; check the wording with the restaurant before publishing.
- Photos are free Unsplash placeholders (`images/CREDITS.md`); replace them with the restaurant's own. Replace prices, texts, address, phone, email and hours. Privacy page: fill in the yellow fields and get it reviewed.
- Add canonical/hreflang and `og:image` when the domain is known (comment in the page head).
