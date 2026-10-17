# Glossy Nail Studio – nail studio design 4 (play with your set)

Status (2026-10-17): **built.** A nail studio website in a fourth design with **new made-up content** ("Glossy", Plovdiv). Bulgarian (`/`) and English (`/en/`).
`Nail_Salon_1` and `Nail_Salon_2` were not changed. The Plovdiv sample prices and the checklist for a real salon are in `../Nail_Salon_1/TODO.md`.

**Everything about the studio is an example**: name, prices, texts, reviews, address and hours. Replace it for a real salon.

## Research behind the design (2026-10-17)

Roundups of nail salon websites (Colorlib's 2026 list, HubSpot, My Codeless Website, Moneris) and guides to salon website features name:

- **Playful, colourful brands with pastel gradients and animated marquees** (NAF! Salon, Sugarcoat Beauty, Cute Nail Studio, Tropical Popical, DBCN). Used: pastel gradients, a sliding word strip, stickers, big rounded shapes.
- **Clients buy with their eyes; transparent prices before booking.** Used: a live preview of the set and a price and time that add up as you choose.
- **Online booking inside the site, with a booking button always in reach.** Used: a floating header button and, on phones, a bottom bar showing the running total.
- **Inspiration galleries** (Instagram-style grids). Used: a photo gallery where "I want this look" travels with the booking.
- The **set builder** (shape, length, colour, finish drawn on a hand) is my own idea, not a pattern named in those sources. The sources are vendor and agency articles; they are opinions, not data.

## What is different

| Area | Nail_Salon_1 | Nail_Salon_2 | Nail_Salon_4 (this one) |
|---|---|---|---|
| Idea | one long page, arched photos | bento tiles, visit builder | **"design your set"**: an SVG hand redrawn as you pick length, shape, colour, finish and extras |
| Colour schemes | 5 | the same 5 | **5 new**: Bubblegum, Lilac Dream, Peach Fizz, Mint Chip, Blueberry |
| Services | price list + estimator | tabs with ticks | chosen through the builder: length sets the service; chrome, glitter, French tips and accent art add nail art; plus gel removal and a pedicure |
| Booking | form | next-free-time chips | 14 day chips, free-time chips and details; the summary card keeps your set |
| Header | bar / pill | floating pill | floating rounded bar with an outline |
| Font | Cormorant Garamond | Unbounded | **Nunito** (rounded) |

## How the builder works

- `tools/build_pages.py` holds the choices (`BASES`, `SHAPES`, `COLOURS`, `FINISHES`, `EXTRAS`) and the services they map to (`ITEMS`, written into the page as JSON).
- `js/main.js` draws the hand (`drawHand`, `nailD` for each shape) and works out services, price and time (`serviceIds`, `totals`). The visit length drives the free times.
- Nail art is priced on request, so any set with chrome, glitter, French tips or accent art shows "from" and a note.

## The request system (mock server, replaceable by a real backend)

- `js/api.js` (`GlossyAPI`) is a mock server using `js/config.js`; two technicians can work at the same time (`capacity: 2`). A request can answer 409 `slot_taken`. References look like `GL-0001`.
- `mode: "demo"` keeps data in this browser only and sends nothing. See `docs/API.md`. `admin.html` is a demo back office (no login).

## Colour schemes

The five round buttons at the bottom switch the site (`data-skin` on `<html>`); the choice is remembered (`glossySkin`) and works as `?skin=lilac`.

## Checked (2026-10-17)

- axe-core 4.10.2: no violations on the BG and EN home pages in all five colour schemes (1280 and 375 px), the admin page and the privacy pages.
- No horizontal overflow at 360, 768 and 1440 px; no requests to other sites (the map loads only after a click).
- Flow tested: medium extensions with accent art, price and time, a day and a time, a request with reference GL-0001.

## Not done / to do before real use

- Not tested on real phones, Safari (uses `:has()`) or screen readers. The preview hand is an illustration, not a promise of the result.
- Photos are the same free Unsplash placeholders as the other nail studios (`images/CREDITS.md`). Replace them with the studio's own.
- Replace texts, prices, address, phone, email, hours and the map position. Privacy page: fill in the yellow fields and get it reviewed.
- Add canonical/hreflang and `og:image` when the domain is known (comment in the page head).
