# Little Moka – café design 1 (order ahead, pick up without a queue)

Status (2026-10-17): **built.** A website for a **café and bakery** whose main idea is **ordering ahead**: the visitor builds an order from the menu, chooses a pick-up time and pays at the counter. **Made-up content** ("Little Moka", Plovdiv). Bulgarian (`/`) and English (`/en/`).

**Everything about the café is an example**: name, menu, prices, hours, texts, address and phone. Replace it for a real café.

## Research behind the design (2026-10-17)

Café-website roundups (Insidea, Freshy Sites, B12, Achi Systems, Emergent) agree on:

- **Hours and location near the top**, plus click-to-call and a map. Used: a live "Open until 17:00" pill in the header and an hours table that highlights today.
- **A mobile-first ordering path** with clear pick-up times. Used: the menu is the order builder, with a sticky order bar on phones.
- **An HTML menu with short descriptions, visible prices and dietary tags** (not a PDF). Used: a filterable menu with V / VG tags and a milk choice for milk drinks.
- **One main action per page, few pages, fast loading.** Used: one page, one big button ("Order ahead"), no scripts or fonts from other companies.
- The sources are vendor and agency articles; the numbers they quote have no primary source. They are opinions, not data. The "next free pick-up" line, the loyalty card and the chalkboard are **my own choices**.

## How the order builder works

- `MENU` in `tools/build_pages.py` holds every item (id, category, price, vegetarian/vegan tag, whether it takes milk). Milk choices and their surcharges are in `MILK`.
- Tapping "+" adds an item to the tray. Drinks with milk get a milk selector per line. The total updates live.
- Pick-up times come from the mock server (`availability`): every 10 minutes (`SLOT_MINUTES`), three orders per slot (`CAPACITY`), 15 minutes of notice for a same-day order (`LEAD_MINUTES`). The page picks the first day with a free time and shows it in the hero.
- The request carries the summary line, the total and the items (`plan`). Payment is at the counter; there is no online payment.
- Hours and capacity are set at the top of `tools/build_pages.py`; run `python tools/build_pages.py && python tools/build_privacy.py` after changing them.

## The request system (mock server, replaceable by a real backend)

- `js/api.js` (`MokaAPI`) is a mock server using `js/config.js`. A request can answer 409 `slot_taken`. References look like `LM-0001`. `mode: "demo"` keeps data in this browser only and sends nothing. See `docs/API.md`. `admin.html` is a demo back office (no login).

## Colour schemes

The five round buttons at the bottom switch the site (`data-skin` on `<html>`): Latte (default), Matcha, Berry, Espresso (dark), Blueberry. The choice is remembered (`mokaSkin`) and works as `?skin=matcha`.

## Checked (2026-10-17)

- axe-core 4.10.2: no violations on the BG and EN home pages in all five colour schemes (1280 and 375 px), the admin page and the privacy pages.
- No horizontal overflow at 360, 375, 768, 1280 and 1440 px; no requests to other sites (the map loads only after a click).
- Flow tested: two flat whites, a croissant and an avocado toast, a free time, a request with reference LM-0001 (20.10 €), visible in the demo back office.

## Not done / to do before real use

- Not tested on real phones, Safari or screen readers.
- No online payment, no order tracking, no stock control ("sold out"). A real system needs those on the server.
- Open/closed and the first free time are computed in the visitor's browser clock; a real system should use the café's time zone and holidays.
- The board ("Today at the counter") is static text; the café must update it or connect it to the back office.
- Photos are free Unsplash placeholders (`images/CREDITS.md`); replace them with the café's own. Replace prices, texts, address, phone, email and hours. Privacy page: fill in the yellow fields and get it reviewed.
- Add canonical/hreflang and `og:image` when the domain is known (comment in the page head).
