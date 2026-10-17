# Hollis & Dane Barbers – barbershop design 3 (the gazette)

Status (2026-10-17): **built.** A barbershop website in a third design with **new made-up content** ("Hollis & Dane", Plovdiv). Bulgarian (`/`) and English (`/en/`).
`Barber_shop` and `Barber_shop_2` were not changed. The research on what a barbershop site needs and the checklist for a real shop are in `../Barber_shop/TODO.md`.

**Everything about the shop is an example**: name, barbers, prices, texts, reviews, address and hours. Replace it for a real shop.

## What is different

| Area | Barber_shop (1) | Barber_shop_2 | Barber_shop_3 (this one) |
|---|---|---|---|
| Look | dark, classic | condensed caps, drawer | **newspaper front page**: Playfair Display, double rules, masthead with today's date |
| Colour schemes | 5 (brass, navy, forest, heritage, graphite) | the same 5 | **5 new**: Newsprint, Night Edition, Sage and Cream, Dusty Rose, Cobalt Blue |
| Navigation | header bar | header bar | masthead plus a sticky link bar |
| Prices | two-column list | tabs | **price list in columns with dotted leaders**, a Book link on every row |
| Booking | form at the bottom | drawer, four steps | **chair board** in the page: pick a service and a day, then press a free square (one column per barber, one row per start time) |
| Work | masonry with filters | swipe rail | **wall** of photos (columns); each opens in a viewer with "Book this cut" |
| Reviews | cards | banner | **"Letters to the editor"** |

## Colour schemes

The five round buttons at the bottom of the page switch the whole site (`data-skin` on `<html>`, variables at the top of `css/style.css`).
The choice is remembered in the browser (`hollisSkin`) and also works as `?skin=ink`. To add a scheme: add a `html[data-skin="..."]` block, one entry in `SKINS` in `tools/build_pages.py`, and the key in `SKINS` in `js/main.js`.

## The request system (mock server, replaceable by a real backend)

- `js/api.js` (`HollisAPI`) is a mock server using `js/config.js`. Each barber can do one visit at a time; the board asks `availability(date, minutes, barber)` once per barber. Creating a booking can answer 409 `slot_taken`. References look like `HD-0001`.
- `mode: "demo"` keeps data in this browser only and sends nothing. See `docs/API.md` for the real endpoints.
- `admin.html` is a demo back office (no login). A real one needs a login.

## Checked (2026-10-17)

- axe-core 4.10.2: no violations on the BG and EN home pages in all five colour schemes (at 375 and 1280 px), the admin page and the privacy pages.
- No horizontal overflow at 360, 768 and 1440 px; no requests to other sites (the map loads only after a click).
- Flow tested: board, booking, reference number, the booking showing in the demo back office.

## Not done / to do before real use

- Not tested on real phones, Safari or screen readers. The board is a grid of buttons with labels; check it with real assistive technology.
- Photos are the same free Unsplash placeholders as the other barbershops (`images/CREDITS.md`; photographer pairs should be re-checked). Replace them with the shop's own.
- Replace texts, prices, address, phone, email, hours and the map position.
- Privacy page and legal details are templates with yellow placeholders; get them reviewed.
- Add canonical/hreflang links and `og:image` when the domain is known (comment in the page head).
