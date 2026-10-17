# Bashta – restaurant design 2 (a traditional tavern with online ordering)

Status (2026-10-17): **built.** A plain website for a **traditional Bulgarian tavern (механа)**: a big photo of the food, a menu with prices and photos, and an **online order for delivery or pick-up**. **Made-up content** ("Bashta", Plovdiv). Bulgarian (`/`) and English (`/en/`). It does a different job from `Restaurant_1` (Maslina): there a guest reserves a table; here a customer orders food to take home. Table reservations are by phone only (said on the page).

**Everything about the tavern is an example**: name, story, dishes, prices, hours, delivery terms, address and phone. Replace it for a real restaurant.

## Research behind the design (2026-10-17)

Restaurant-ordering guides (Sauce, Toast, Square, ChowNow) agree on:

- **Ordering on your own website avoids marketplace commissions** (quoted as roughly 15 to 30 % per order; one source says up to 40 %). These are vendor numbers, not independent data. Used: the order is placed on the page itself, with no link to any delivery app.
- **Clear descriptions, good photos and simple choices, and fewer dishes that do not travel well.** Used: a short menu of dishes that travel (grill, pot dishes, salads), photos for three groups and short descriptions.
- **Tell visitors about the delivery fee and the pick-up option up front.** Used: a delivery line in the info bar, a minimum order, a free-delivery threshold and free pick-up.
- The sources are written by companies that sell ordering software; treat the figures with care. Keeping the page **plain** follows the owner's request.

## What is deliberately plain

No animation, no live widgets, no cards that move. One hero photo, serif headings (Playfair Display), square-ish buttons, a thin red-and-white "tablecloth" strip under the photo and dotted price lines. The only interactive part is the order. The five colour schemes at the bottom are required for every site.

## How the order works

- The menu, hours, capacity, minimum order and delivery fee are set at the top of `tools/build_pages.py` (`MENU`, `HOURS`, `CAPACITY`, `MIN_DELIVERY`, `DELIVERY_FEE`, `FREE_DELIVERY_FROM`).
- Pressing "+" adds a dish. The order list shows the dishes, the delivery fee (2 €, free from 25 €) and the total. Delivery needs a minimum of 12 € and an address; pick-up is free.
- Times come from the mock server (`availability`): half-hour windows, four orders per window, 45 minutes of notice for a same-day order. The page opens on the first day with a free window.
- The request carries the dishes, the total and the address (`plan`, `address`). Payment is on receipt; there is no online payment.
- **Demo limitation:** the mock server counts orders per window, not the kitchen's real capacity or a delivery map.

## The request system (mock server, replaceable by a real backend)

- `js/api.js` (`BashtaAPI`) is a mock server using `js/config.js`. A request can answer 409 `slot_taken`. References look like `TB-0001`. `mode: "demo"` keeps data in this browser only and sends nothing. See `docs/API.md`. `admin.html` is a demo back office (no login) and shows the address.

## Colour schemes

The five round buttons at the bottom switch the site (`data-skin` on `<html>`): Oak (default), Olive, Indigo, Night (dark) and Pomegranate. The choice is remembered (`bashtaSkin`) and works as `?skin=olive`.

## Checked (2026-10-17)

- axe-core 4.10.2: no violations on the BG and EN home pages in all five colour schemes (1280 and 375 px), the admin page and the privacy pages.
- No horizontal overflow at 360, 375, 768, 1280 and 1440 px; no requests to other sites (the map loads only after a click).
- Flow tested: two gyuvech, a shopska salad and an ayran for delivery: 28 € (free delivery), a request with reference TB-0001, visible in the demo back office.

## Not done / to do before real use

- Not tested on real phones, Safari or screen readers.
- No online payment, no delivery zones or driver tracking, no stock ("sold out"). A real system needs these on the server.
- The story ("seventy years ago", "family recipes") is invented; the owner must write the real one. Allergy information on a restaurant website has legal rules; check the wording before publishing.
- Photos are free Unsplash placeholders (`images/CREDITS.md`); replace them with the tavern's own. Replace prices, texts, address, phone, email and hours. Privacy page: fill in the yellow fields and get it reviewed.
- Add canonical/hreflang and `og:image` when the domain is known (comment in the page head).
