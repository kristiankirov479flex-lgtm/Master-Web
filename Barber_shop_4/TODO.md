# Bolt Barbers – barbershop design 4 (split screen and ticket)

Status (2026-10-17): **built.** A barbershop website in a fourth design with **new made-up content** ("Bolt", Plovdiv). Bulgarian (`/`) and English (`/en/`).
The other barbershop sites were not changed. The research on what a barbershop site needs and the checklist for a real shop are in `../Barber_shop/TODO.md`.

**Everything about the shop is an example**: name, barbers, prices, texts, reviews, address and hours. Replace it for a real shop.

## What is different

| Area | Barber_shop (1) | Barber_shop_2 | Barber_shop_4 (this one) |
|---|---|---|---|
| Look | dark, classic | condensed caps, drawer | **bold and rounded**: Unbounded + Onest, big stacked headline, sticker, rounded cards |
| Colour schemes | 5 (brass, navy, forest, heritage, graphite) | the same 5 | **5 new**: Volt Lime, Ultra Pink, Sunny Orange, Ice Cyan, Mono and Red |
| Navigation | header bar | header bar | **left rail** on wide screens (highlights the section you are in), top bar with a menu button on phones |
| Booking | form at the bottom | drawer, four steps | **ticket builder**: tap services (you can combine them), pick a barber, a day and a time; a **printed ticket** on the right adds it up (sticky on wide screens, a "Ticket" bar on phones) |
| Prices | two-column list | tabs | **tiles** inside the builder, with time and price |
| Work | masonry with filters | swipe rail | rounded photo wall; each opens in a viewer with "Book this cut" |
| Reviews | cards | banner | slightly tilted notes |

## Colour schemes

The five round buttons at the bottom of the page switch the whole site (`data-skin` on `<html>`, variables at the top of `css/style.css`).
The choice is remembered in the browser (`boltSkin`) and also works as `?skin=sun`. To add a scheme: add a `html[data-skin="..."]` block, one entry in `SKINS` in `tools/build_pages.py`, and the key in `SKINS` in `js/main.js`.
The ticket is drawn in the accent colour, so pick an accent whose text colour (`--on-accent`) has enough contrast on it.

## The request system (mock server, replaceable by a real backend)

- `js/api.js` (`BoltAPI`) is a mock server using `js/config.js`. Each barber can do one visit at a time; the time chips come from `availability(date, minutes, barber)` using the **total** length of all chosen services. Creating a booking can answer 409 `slot_taken`. References look like `BT-0001`.
- Several services are sent as one booking: `service` is the first main service, `plan.summary` lists all of them with the total time and price.
- `mode: "demo"` keeps data in this browser only and sends nothing. See `docs/API.md` for the real endpoints.
- `admin.html` is a demo back office (no login). A real one needs a login.

## Checked (2026-10-17)

- axe-core 4.10.2: no violations on the BG and EN home pages in all five colour schemes (at 375 and 1280 px), the admin page and the privacy pages.
- No horizontal overflow at 360, 768 and 1440 px; no requests to other sites (the map loads only after a click).
- Flow tested: several services, barber, day and time, ticket total, booking, reference number, the booking showing in the demo back office.

## Not done / to do before real use

- Not tested on real phones, Safari or screen readers.
- Photos are the same free Unsplash placeholders as the other barbershops (`images/CREDITS.md`; photographer pairs should be re-checked). Replace them with the shop's own.
- Replace texts, prices, address, phone, email, hours and the map position.
- Privacy page and legal details are templates with yellow placeholders; get them reviewed.
- Add canonical/hreflang links and `og:image` when the domain is known (comment in the page head).
