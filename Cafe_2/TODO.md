# Ember Roasters – café design 2 (a roastery that sells beans)

Status (2026-10-17): **built.** A website for a **small coffee roastery**: the visitor chooses a coffee, a bag size, a grind and how often, then picks **delivery or pick-up** with a free time. **Made-up content** ("Ember Roasters", Plovdiv). Bulgarian (`/`) and English (`/en/`). This is a different idea from `Cafe_1` (drinks ordered for pick-up).

**Everything about the roastery is an example**: name, coffees, prices, roast days, texts, address and phone. Replace it for a real roastery.

## Research behind the design (2026-10-17)

Roaster e-commerce and agency write-ups (Roaster Tools, Wapiti Digital, Shero Commerce, Sonder Digital, Ecomm Design) agree on:

- **Product pages that show origin, roast level, process, tasting notes and roast date**, not just a name and a price. Used: coffee cards with origin and altitude, process, three tasting notes, a five-dot roast level and the "last roast" day in the first screen.
- **Subscribe-and-save built into the product choice**, with skip/pause/cancel kept easy to reach. Used: "How often?" (once, every 2 weeks, every month) with a clear −8 % on the checkout bar. Skip/pause is **not** built (needs a real backend).
- **Clear delivery and pick-up choices.** Used: free delivery over 35 €, free pick-up, a day and a time.
- The sources are agency and vendor case studies; their conversion figures come from the vendors themselves. They are opinions, not data. The brew calculator, the tasting-note marquee and the stepped page with a sticky checkout bar are **my own choices**.

## How the order works

- Coffees, sizes, grinds, frequencies, delivery fee and subscription discount are set at the top of `tools/build_pages.py` (`COFFEES`, `SIZES`, `GRINDS`, `FREQS`, `DELIVERY_FEE`, `FREE_DELIVERY_FROM`, `SUB_DISCOUNT`). 1 kg costs 3.6 × the 250 g price (about 10 % less per gram).
- The page shows the bag as the visitor builds it: the header pill and the **checkout bar** (always on screen while ordering) show the line, the delivery note and the total.
- Delivery or pick-up uses the same mock server (`availability`): half-hour windows (`SLOT_MINUTES`), six orders per window (`CAPACITY`), two hours of notice for a same-day order (`LEAD_MINUTES`). A delivery needs an address (the server answers 422 without one).
- The **brew calculator** gives grams of coffee, water, temperature, time and grind for five methods (`METHODS`). Espresso counts double shots.
- The request carries the summary, the total and the items (`plan`). Payment is on receipt; there is no online payment.

## The request system (mock server, replaceable by a real backend)

- `js/api.js` (`EmberAPI`) is a mock server using `js/config.js`. A request can answer 409 `slot_taken`. References look like `ER-0001`. `mode: "demo"` keeps data in this browser only and sends nothing. See `docs/API.md`. `admin.html` is a demo back office (no login) and shows the delivery address.

## Colour schemes

The five round buttons at the bottom switch the site (`data-skin` on `<html>`): Ember (default, dark), Paper (light), Moss (dark green), Midnight (navy and gold), Blush (light pink). The choice is remembered (`emberSkin`) and works as `?skin=moss`. The first screen and the roastery section stay dark in every scheme.

## Checked (2026-10-17)

- axe-core 4.10.2: no violations on the BG and EN home pages in all five colour schemes (1280 and 375 px), the admin page and the privacy pages.
- No horizontal overflow at 360, 375, 768, 1280 and 1440 px; no requests to other sites (the map loads only after a click).
- Flow tested: Colombia Huila, 1 kg, filter grind, two bags, every two weeks, delivery to an address: 2 × 37.80 € − 8 % = 69.55 € (free delivery), a request with reference ER-0001, visible in the demo back office.

## Not done / to do before real use

- Not tested on real phones, Safari (uses `:has()`) or screen readers.
- No customer accounts, no skip/pause/cancel of a subscription, no payment and no stock ("sold out"). A real shop needs these on the server.
- The roast day shown ("last roast") is computed from `ROAST_DAYS` in the visitor's browser; a real roastery should show the real batch date per bag.
- Photos are free Unsplash placeholders (`images/CREDITS.md`); replace them with the roastery's own. Replace prices, texts, address, phone, email and hours. Privacy page: fill in the yellow fields and get it reviewed.
- Add canonical/hreflang and `og:image` when the domain is known (comment in the page head).
