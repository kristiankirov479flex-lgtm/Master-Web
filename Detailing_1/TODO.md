# Kristal – auto detailing design 1 (a detailing studio)

Status (2026-10-17): **built.** A plain website for a **car detailing studio**: five packages with what each includes, a **price table by car size**, add-ons, how the studio works, a photo gallery and a booking form that shows an **estimated price and the time the job takes**. **Made-up content** ("Kristal", Plovdiv). Bulgarian (`/`) and English (`/en/`).

**Everything about the studio is an example**: name, packages, prices, hours, address and phone. Replace it for a real studio.

## Research behind the design (2026-10-17)

Detailing-website guides and booking templates (B12, Paperform, Framer, SchedulingKit, Servicify, a detailing-site agency) agree on:

- **Pricing by vehicle size is the core feature**, because a small car and an SUV need different time and products. Used: a price table with four sizes and a size choice in the form.
- **Packages shown side by side with clear inclusions.** Used: five package cards, each with three lines of what is included.
- **Add-ons offered at the point of booking** (headlight restoration, pet hair, odour). Used: four add-ons in the form and in the table beside it.
- **A prominent before/after gallery.** Used: a photo gallery. These are stock photos, not before/after pairs; the studio must add its own.
- **Booking asks for vehicle, size and service.** Used: make, model, size, package and add-ons.
- The sources are mostly vendors of website builders and booking software; their conversion claims are unverified and their price ranges are one vendor's estimates. They are opinions, not data.

## What is deliberately plain

No animation, no live widgets, no sticky bars. A dark first screen with one photo, sharp corners, Unbounded headings in moderate sizes and a red accent. The only interactive part is the booking form. The five colour schemes at the bottom are required for every site.

## How the booking works

- Packages (minutes and prices per size), add-ons and hours are set at the top of `tools/build_pages.py` (`SIZES`, `PACKAGES`, `ADDONS`, `ADDON_MINUTES`, `HOURS`, `CAPACITY`).
- Estimated price = the package price for the chosen size + the add-ons. Packages marked "from" (paint correction, ceramic coating) say that the exact price follows an inspection. Time needed = the package time + 20 minutes per add-on.
- Free drop-off times come from the mock server (`availability`) for exactly that length: half-hour starts, two bays at the same time, two hours of notice. A ceramic coating (8 hours) fits only early starts.
- On phones the price table turns into one block per package so it never scrolls sideways.
- The request carries the car, size, package, add-ons and the estimate (`plan`). No payment.

## The request system (mock server, replaceable by a real backend)

- `js/api.js` (`KristalAPI`) is a mock server using `js/config.js`. A request can answer 409 `slot_taken`. References look like `KR-0001`. `mode: "demo"` keeps data in this browser only and sends nothing. See `docs/API.md`. `admin.html` is a demo back office (no login).

## Colour schemes

The five round buttons at the bottom switch the site (`data-skin` on `<html>`): Graphite (default, light with red), Steel, Pearl, Noir (dark) and Racing. The choice is remembered (`kristalSkin`) and works as `?skin=noir`.

## Checked (2026-10-17)

- axe-core 4.10.2: no violations on the BG and EN home pages in all five colour schemes (1280 and 375 px), the admin page and the privacy pages (the price table was reshaped for phones).
- No horizontal overflow at 360, 375, 768, 1280 and 1440 px; no requests to other sites (the map loads only after a click).
- Flow tested: a BMW 3 Series, SUV size, ceramic coating plus headlight restoration: 700 € + 40 € = from 740 €, about 8 h 20 min, a request with reference KR-0001, visible in the demo back office.

## Not done / to do before real use

- Not tested on real phones, Safari or screen readers.
- No before/after photos, no photo upload at booking and no mobile (come-to-you) service.
- Prices and times are examples; a real studio must price from its own products and labour.
- Photos are free Unsplash placeholders (`images/CREDITS.md`); replace them with the studio's own work. Replace texts, address, phone, email and hours. Privacy page: fill in the yellow fields and get it reviewed.
- Add canonical/hreflang and `og:image` when the domain is known (comment in the page head).
