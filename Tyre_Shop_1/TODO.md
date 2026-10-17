# Gripline – tyre shop design 1 (size finder, price slip and booked time)

Status (2026-10-17): **built.** A website for a **tyre and service workshop** whose main idea is that the visitor **enters the tyre size, sees the price straight away and books a time** for the work. **Made-up content** ("Gripline", Plovdiv). Bulgarian (`/`) and English (`/en/`).

**Everything about the workshop is an example**: name, prices, services, hours, texts, address and phone. Replace it for a real workshop.

## Research behind the design (2026-10-17)

Tyre-shop marketing and website guides (NetDriven, Podium, SellMoreTyres, Brandignity, Qquote, Website Studio) agree on:

- **A tyre-size or vehicle lookup that turns an urgent search into a booking.** Used: a tyre-size finder in the first screen, styled like a tyre sidewall (width / profile R rim), that shows the price of a swap at once.
- **Slot-based online booking with instant confirmation** instead of "call us". Used: a five-step visit builder with free times from the mock server.
- **Showing starting-at prices or a list of what is included** when exact prices cannot be posted. Used: a price board and a live price slip that says "estimate".
- **Seasonal changeovers are predictable demand spikes**; invite visitors to book early, and keep the message accurate. Used: a ribbon on top (example text) and a short "which tyres when" guide.
- **Mobile first, one-tap calling.** Used: a phone button in the header and a Call / Book bar on phones.
- The sources are vendor and agency articles; some give statistics without a primary source. They are opinions, not data. The live "In the workshop now" card, the hazard-stripe look and the FAQ are **my own choices**.

## How the booking works

- Prices are set at the top of `tools/build_pages.py`: `BASE` and `PER_INCH` (a swap of 4 wheels costs `BASE` up to 15″ and `PER_INCH` more for each inch above), `VEHICLES` (SUV and van surcharges), `JOBS` (one is chosen) and `ADDONS` (any number). The same numbers drive the hero finder, the option prices and the slip.
- Time needed = the sum of the minutes of the chosen job and add-ons (capped at 180). Free start times come from the mock server for exactly that length (`availability`): every 15 minutes (`SLOT_MINUTES`), two bays (`CAPACITY`), 30 minutes of notice for a same-day visit (`LEAD_MINUTES`).
- "In the workshop now" shows open/closed, the first free time for a 45-minute job and the number of free start times today, all from the same mock server.
- The request carries the car (make, model, plate, vehicle type), the tyre size, the job, the add-ons, the estimate and the minutes (`plan`).
- Hours and bays are set in `tools/build_pages.py`; run `python tools/build_pages.py && python tools/build_privacy.py` after changing them.

## The request system (mock server, replaceable by a real backend)

- `js/api.js` (`GriplineAPI`) is a mock server using `js/config.js`. A request can answer 409 `slot_taken`. References look like `GR-0001`. `mode: "demo"` keeps data in this browser only and sends nothing. See `docs/API.md`. `admin.html` is a demo back office (no login).

## Colour schemes

The five round buttons at the bottom switch the site (`data-skin` on `<html>`): Hazard (default, yellow on charcoal), Redline, Cobalt, Forest and Concrete (light). The choice is remembered (`griplineSkin`) and works as `?skin=cobalt`. The first screen stays dark in every scheme.

## Checked (2026-10-17)

- axe-core 4.10.2: no violations on the BG and EN home pages in all five colour schemes (1280 and 375 px), the admin page and the privacy pages (one landmark finding fixed).
- No horizontal overflow at 360, 375, 768, 1280 and 1440 px; no requests to other sites (the map loads only after a click).
- Flow tested: 225/45 R17 on an SUV with alignment and storage: 44 € + 35 € + 30 € = 109 €, 1 h 35 min, a request with reference GR-0001, visible in the demo back office.

## Not done / to do before real use

- Not tested on real phones, Safari (uses `:has()`) or screen readers.
- The price is a **formula for demonstration**. A real workshop has price lists by tyre, brand and rim; connect them to a real catalogue. New tyres are quoted separately here.
- No tyre catalogue, no stock and no online payment. A number-plate lookup (as some vendors offer) needs a paid service and is not included.
- The ribbon text ("book before 15 November") is an example and must be kept accurate by the workshop.
- Photos are free Unsplash placeholders (`images/CREDITS.md`); replace them with the workshop's own. Replace prices, texts, address, phone, email and hours. Privacy page: fill in the yellow fields and get it reviewed.
- Add canonical/hreflang and `og:image` when the domain is known (comment in the page head).
