# Atelier Nude – nail studio design 3 (the lookbook)

Status (2026-10-17): **built.** A nail studio website in a third design with **new made-up content** ("Atelier Nude", Plovdiv). Bulgarian (`/`) and English (`/en/`).
`Nail_Salon_1` and `Nail_Salon_2` were not changed. The Plovdiv sample prices and the checklist for a real salon are in `../Nail_Salon_1/TODO.md`.

**Everything about the studio is an example**: name, looks, prices, texts, reviews, address and hours. Replace it for a real salon.

## Research behind the design (2026-10-17)

Roundups of nail salon websites (Colorlib's 2026 list, HubSpot, My Codeless Website, Moneris) and guides to salon website features agree on:

- **Clients buy with their eyes**: large, real photos of finished sets, and a gallery that leads to booking. Used: a **lookbook** where every look has a "Book this look" button that fills in the visit.
- **Prices shown before booking**; transparent price lists (UL Nails & Spa, Nail Garden). Used: a typeset menu with time and price, and a total that adds up.
- **A booking button always in reach** and online booking inside the site. Used: header button, phone bar, one-step booking.
- **Editorial, minimal layouts with serif type and lots of white space** (Paintbox, Artiva Nails, QQ Nails). Used: Playfair Display, a "lookbook" cover, hairline rules.
- **Gift cards** (Varnish Nail Shoppe) and memberships (Nail Garden). Used: a gift card band (it opens the booking form with a message).
- The sources are vendor and agency articles; they are opinions, not data.

## What is different

| Area | Nail_Salon_1 | Nail_Salon_2 | Nail_Salon_3 (this one) |
|---|---|---|---|
| Idea | one long page, arched photos | bento tiles, visit builder | **lookbook**: pick a look, we book the services it needs |
| Colour schemes | 5 | the same 5 | **5 new**: Bone and Ink, Blush and Rouge, Mocha and Cream, Noir and Nude, Mint and Forest |
| Services | price list + estimator | tabs with ticks | **menu** with dotted leaders; a plus button adds a service to your visit |
| Booking | form | next-free-time chips | **your visit** card (look, services, total), a week strip, free-time chips, details |
| Font | Cormorant Garamond | Unbounded | **Playfair Display** + Onest |

## The request system (mock server, replaceable by a real backend)

- `js/api.js` (`AtelierAPI`) is a mock server using `js/config.js`; free times come from `availability(date, minutes)` (one visit at a time). A request can answer 409 `slot_taken`. References look like `AN-0001`.
- A look sets its services (for example Midnight Gold = medium extensions + nail art). Nail art has no fixed price, so the total says "from" and "plus nail art".
- `mode: "demo"` keeps data in this browser only and sends nothing. See `docs/API.md`.
- `admin.html` is a demo back office (no login).

## Colour schemes

The five round buttons at the bottom switch the site (`data-skin` on `<html>`; variables at the top of `css/style.css`); the choice is remembered (`atelierSkin`) and works as `?skin=noir`.

## Checked (2026-10-17)

- axe-core 4.10.2: no violations on the BG and EN home pages in all five colour schemes (1280 and 375 px), the admin page and the privacy pages.
- No horizontal overflow at 360, 768 and 1440 px; no requests to other sites (the map loads only after a click).
- Flow tested: choosing a look, the visit card and total, a day and a time, a request with reference AN-0001.

## Not done / to do before real use

- Not tested on real phones, Safari (uses `:has()`) or screen readers.
- Photos are the same free Unsplash placeholders as the other nail studios (`images/CREDITS.md`; photographer pairs should be re-checked). Replace them with the studio's own.
- Replace texts, prices, address, phone, email, hours and the map position. Privacy page: fill in the yellow fields and get it reviewed.
- Add canonical/hreflang and `og:image` when the domain is known (comment in the page head).
