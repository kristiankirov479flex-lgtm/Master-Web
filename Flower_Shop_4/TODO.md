# Atelier Aubade – flower shop design 4 (weddings and events)

Status (2026-10-17): **built.** A florist website for **weddings and events**, a different customer journey from the other flower shops: instead of buying a bouquet, the visitor **plans the flowers, sees a price range and books a free consultation**. **New made-up content** ("Atelier Aubade", Plovdiv). Bulgarian (`/`) and English (`/en/`). The other flower shops were not changed. The Plovdiv sample prices and the checklist for a real shop are in `../Flower_Shop/TODO.md`.

**Everything about the studio is an example**: name, prices, packages, stories, texts, reviews, address and hours. Replace it for a real studio.

## Research behind the design (2026-10-17)

Roundups of florist websites (Colorlib's 2026 list, Webcitz, My Codeless Website, Wix, Zarla, Clover) agree on:

- **Strong, editorial photography and event galleries** ("inspiration portfolio", seasonal showcases, a four-column portfolio grid). Used: a contact-sheet hero and a **stories rail** of past events.
- **Testimonials as trust** (Petals by Cam). Used: three large quotes.
- **Wedding and event florists sell through consultations**, not a basket. I found no specific wedding-florist layout study; the planner and the packages are **my own choice**, built on that logic.
- The sources are vendor and agency articles; they are opinions, not data.

## What is different

| Area | Flower_Shop (1) | Flower_Shop_2 | Flower_Shop_4 (this one) |
|---|---|---|---|
| Customer | someone buying a bouquet | someone buying a bouquet | **a couple or host planning an event** |
| First screen | split, arched photo | full-width photo | **contact sheet** of six photos with a framed card in the middle |
| Header | logo left | centred logo, links split | centred italic logo, links on the left, button on the right |
| Browsing | gallery and price list | catalog with filters | **stories rail** (swipe or arrows) and **three packages** |
| Choosing | order estimator | cards with "Choose" | **planner in five steps**: event and guests, up to three styles, pieces with counts, consultation time, details; a **brief card** shows the price range |
| Process | three promises | numbered steps with photos | **vertical timeline** next to a sticky heading |
| Look | light, Cormorant | light, Playfair | **dark and gold by default**, Alegreya italic, thin square buttons |
| Colour schemes | 5 | the same 5 | **5 new**: Evergreen and Gold, Ivory and Clay, Blush and Rouge (light), Midnight and Rose Gold, Plum and Petal |

## How the planner works

- `PIECES` (main bouquet, smaller bouquets, buttonholes, arch, aisle arrangements, table centrepieces, cake flowers, car decoration) have a minimum and maximum sample price. The brief card adds them up as a range. Table centrepieces start at one per eight guests.
- `PACKS` presets fill the planner. Change prices and presets in `tools/build_pages.py`.
- The consultation is 45 minutes (`CONSULT_MINUTES`), booked through the same mock server as the other sites (`fulfil: "pickup"` = in the studio). The request carries the plan summary, the styles and the estimate.

## The request system (mock server, replaceable by a real backend)

- `js/api.js` (`AubadeAPI`) is a mock server using `js/config.js` (one consultation at a time). A request can answer 409 `slot_taken`. References look like `AU-0001`. `mode: "demo"` keeps data in this browser only and sends nothing. See `docs/API.md`. `admin.html` is a demo back office (no login).

## Colour schemes

The five round buttons at the bottom switch the site (`data-skin` on `<html>`); the choice is remembered (`aubadeSkin`) and works as `?skin=blush`.

## Checked (2026-10-17)

- axe-core 4.10.2: no violations on the BG and EN home pages in all five colour schemes (1280 and 375 px), the admin page and the privacy pages (one landmark finding fixed).
- No horizontal overflow at 360, 768 and 1440 px; no requests to other sites.
- Flow tested: the Ceremony package, three styles (a fourth is refused), 120 guests, a price range of 612 € – 1,273 €, a consultation request with reference AU-0001.

## Not done / to do before real use

- Not tested on real phones, Safari (uses `:has()`) or screen readers.
- The "stories" and styles use stock photos, not real events; replace them with real event photos and captions. Photos: `images/CREDITS.md`.
- Replace prices, texts, address, phone, email and hours. Privacy page: fill in the yellow fields and get it reviewed.
- Add canonical/hreflang and `og:image` when the domain is known (comment in the page head).
