# Nocturne Nail Bar – nail studio design 5 (after dark)

Status (2026-10-17): **built.** A nail studio website that is deliberately **unlike the other four**, with **new made-up content** ("Nocturne", a late-night nail bar in Plovdiv). Bulgarian (`/`) and English (`/en/`).
The other nail sites were not changed. The Plovdiv sample prices and the checklist for a real salon are in `../Nail_Salon_1/TODO.md`.

**Everything about the bar is an example**: name, prices, texts, reviews, address and hours. Replace it for a real salon.

## Why it is different

| Area | Nail_Salon_1 / 3 | Nail_Salon_2 | Nail_Salon_4 | Nail_Salon_5 (this one) |
|---|---|---|---|---|
| Mood | light, calm, serif | light, bento tiles | pastel, playful | **dark, neon, "after dark"**; huge condensed headline (Oswald) |
| Page | long scrolling page | long scrolling page | long scrolling page | **four full screens**; on desktop the page snaps from screen to screen; dots on the right show where you are |
| How you choose | price list / lookbook | tick services | drag-free builder with a drawn hand | **a chat**: the "set finder" asks four questions (occasion, length, finish, pedicure) and ends with a set, a photo, a price and a time |
| Photos | grid or gallery | grid | collage | **three endless vertical photo columns** on the first screen, plus one photo with your result |
| Day picker | week strip / chips | chips | day chips | **month calendar** (90 days ahead) |
| Colour schemes | 5 | 5 | 5 | **5 new**: Orchid Night, Acid Lime, Ember, Ice Blue (all dark) and Pearl Day (light) |

## Research behind it

The earlier research (Colorlib's 2026 nail salon roundup, HubSpot, My Codeless Website, Moneris, salon-feature guides) found bold dark editorial brands (UL Nails & Spa, Paintbox), moving marquee banners and transparent prices. This design takes the dark, bold direction and replaces the usual price list with a **guided choice**. The chat idea is my own, not a pattern named in those sources.

## How the set finder works

- `tools/build_pages.py`: `ITEMS` (the six services), `LOOKS` (the four result photos), the questions and texts in `L[...]['quiz']`. All of it is written into the page as JSON.
- `js/main.js`: `startQuiz`, `ask`, `choose`, `showResult`. Length picks the service (own nails = gel manicure, short, medium, long = extensions); Chrome and Nail art add "nail art" (price on request); "Yes" adds a gel pedicure. The occasion is added to the request message.
- "Skip" books a plain gel manicure without the chat. Everything the chat decides can be changed by pressing Start over.

## The request system (mock server, replaceable by a real backend)

- `js/api.js` (`NocturneAPI`) is a mock server using `js/config.js` (open until 22:00 on weekdays; two technicians can work at the same time). A request can answer 409 `slot_taken`. References look like `NC-0001`.
- `mode: "demo"` keeps data in this browser only and sends nothing. See `docs/API.md`. `admin.html` is a demo back office (no login).

## Colour schemes

The five round buttons at the bottom switch the site (`data-skin` on `<html>`; variables at the top of `css/style.css`, with a second accent `--accent2` for the gradient); the choice is remembered (`nocturneSkin`) and works as `?skin=acid`.

## Checked (2026-10-17)

- axe-core 4.10.2: no violations on the BG and EN home pages in all five colour schemes (1280 and 375 px), on the result screen, the admin page and the privacy pages.
- No horizontal overflow at 360, 768 and 1440 px; no requests to other sites (the map loads only after a click).
- Flow tested: four answers, the result (Chrome Mirror, medium extensions + nail art + pedicure, from 70 – 75 €, 4 h 15), a calendar day and time, a request with reference NC-0001.

## Not done / to do before real use

- Not tested on real phones, Safari (uses `:has()` and `scroll-snap`) or screen readers. The chat is a live region with real buttons; check it with a screen reader.
- Moving photo columns and the word ticker stop when the visitor asks for reduced motion.
- Photos are the same free Unsplash placeholders as the other nail studios (`images/CREDITS.md`). Replace them with the studio's own.
- Replace texts, prices, address, phone, email, hours and the map position. Privacy page: fill in the yellow fields and get it reviewed.
- Add canonical/hreflang and `og:image` when the domain is known (comment in the page head).
