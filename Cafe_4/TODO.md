# Kettle & Co – café design 4 (a traditional coffee house)

Status (2026-10-17, reworked): **built.** A plain, traditional website for a **neighbourhood coffee house**: a big photo, a short story, a menu that reads like a printed card, a few photos, opening hours, a simple table reservation and the address. **Made-up content** ("Kettle & Co", Plovdiv). Bulgarian (`/`) and English (`/en/`). The first version of this design was a coffee-catering site with a quote calculator; it was replaced because it felt too busy and too clever. The other cafés (`Cafe_1` to `Cafe_3`) are unchanged.

**Everything about the café is an example**: name, story, menu, prices, hours, address and phone. Replace it for a real café.

## Research behind the design (2026-10-17)

The café-website roundups used for `Cafe_1` (Insidea, Freshy Sites, B12, Achi Systems, Emergent) agree on the basics, and this design follows only those:

- **Hours, address and a phone number near the top** (a dark bar under the photo).
- **A readable HTML menu with prices**, not a PDF (the menu reads like a printed card with dotted price lines).
- **One main action and few sections** (see the menu, or reserve a table).
- **Real photos build trust.** The photos here are Unsplash placeholders; a real café should use its own.
- The sources are vendor and agency articles; they are opinions, not data. Choosing to keep this one **plain on purpose** is the owner's request, not a research finding.

## What is deliberately plain

No animation on scroll, no moving or live widgets, no cards that update, no sticky bars, no emoji, square-ish buttons, serif headings (Alegreya) and one hero photo. The only interactive part is the reservation form (a date, a time chosen from the free times, the details). The colour schemes at the bottom (required for every site) are the only extra.

## How the reservation works

- The menu, hours, capacity and story are set at the top of `tools/build_pages.py` (`MENU`, `HOURS`, `CAPACITY`, `BOOKING_MINUTES`, `MAX_PARTY`).
- The form uses a normal date field and a time list. Free times come from the mock server (`availability`): half-hour starts, a table is kept for 90 minutes, six tables at the same time, one hour of notice for a same-day booking. The page opens on the first day that still has a free table.
- **Demo limitation:** the mock server counts bookings, not real tables. A real café needs a table plan.
- The request carries the party size (`plan`). No payment, no deposit.

## The request system (mock server, replaceable by a real backend)

- `js/api.js` (`KettleAPI`) is a mock server using `js/config.js`. A request can answer 409 `slot_taken`. References look like `KC-0001`. `mode: "demo"` keeps data in this browser only and sends nothing. See `docs/API.md`. `admin.html` is a demo back office (no login).

## Colour schemes

The five round buttons at the bottom switch the site (`data-skin` on `<html>`): Linen and green (default), Wine, Harbour (navy), Dark roast and Clay. The choice is remembered (`kettleSkin`) and works as `?skin=wine`.

## Checked (2026-10-17)

- axe-core 4.10.2: no violations on the BG and EN home pages in all five colour schemes (1280 and 375 px), the admin page and the privacy pages.
- No horizontal overflow at 360, 375, 768, 1280 and 1440 px; no requests to other sites (the map loads only after a click).
- Flow tested: a table for four on the first free day, a request with a reference number, visible in the demo back office.

## Not done / to do before real use

- Not tested on real phones, Safari or screen readers.
- The story ("eleven years ago", "farm in the Rhodope mountains", "roaster in the city") is invented; the owner must write the real one.
- Photos are free Unsplash placeholders (`images/CREDITS.md`); replace them with the café's own. Replace prices, texts, address, phone, email and hours. Privacy page: fill in the yellow fields and get it reviewed.
- Add canonical/hreflang and `og:image` when the domain is known (comment in the page head).
