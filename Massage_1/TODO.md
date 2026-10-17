# Tishina – massage design 1 (a quiet studio)

Status (2026-10-17): **built.** A plain website for a **massage studio**: a dark, quiet first screen, a menu of five massages with **a price for each length**, a **gift voucher** card, what to know before you come, two therapists, FAQ and a **booking form** (massage, length with its price, therapist, gift option, a day and a free time that fits the length). **Made-up content** ("Tishina", Plovdiv). Bulgarian (`/`) and English (`/en/`). It differs from `Physio_1`: relaxation and a menu with gifts, not treatment of a complaint.

**Everything about the studio is an example**: name, massages, prices, therapists, hours, address and phone. The therapists are text cards with initials. Replace all of it for a real studio.

## Research behind the design (2026-10-17)

Massage-website guides (MassageBook, Fresha, Zenoti, WPAstra, a massage-insurance blog) agree on:

- **A menu grouped so clients can choose alone, with duration and price for each service**, and plain wording instead of jargon. Used: five massages, each with its lengths and prices.
- **Packages for repeat visits.** Not built here (see the list below).
- **Gift certificates are a standard part of the services page.** Used: a voucher card in the menu and a "this is a gift" box in the form.
- **A booking form that collects service, session length and preferred date.** Used: massage, length, therapist, day and time.
- **Calm colours, mobile-friendly, client reviews.** Used: warm tones, Cormorant headings and a phone-first layout. Reviews are not included because none are real.
- The sources are mostly vendor blogs; a claim that booking adds 25–50% more appointments is unverified. They are opinions, not data.

## What is deliberately plain

No animation, no live widgets, no sticky bars. One dark photo with centred text, serif headings in Cormorant, square corners. The only interactive part is the booking form. The five colour schemes at the bottom are required for every site.

## How the booking works

- Massages (photo, lengths and prices), therapists and hours are set at the top of `tools/build_pages.py` (`MASSAGES`, `THERAPISTS`, `HOURS`, `CAPACITY`).
- The length list follows the chosen massage (for example "Back and neck" has only 30 minutes). The price is shown in one line under the form fields. The "Book this" links in the menu select that massage in the form; the voucher card ticks the gift box.
- Free times are asked from the mock server (`availability`) for the chosen length: half-hour starts, two rooms at the same time, two hours of notice.
- **Demo limitation:** the mock server counts rooms, not each therapist's calendar, so the therapist choice is only a request.
- The request carries massage, length, therapist, gift flag and price (`plan`). No payment: the client pays at the studio. A gift only tells the studio to prepare a voucher; there is no online voucher purchase.
- **Health data:** the note field warns clients not to write detailed medical information; the FAQ lists when not to have a massage. The wording must be reviewed by a professional.

## The request system (mock server, replaceable by a real backend)

- `js/api.js` (`TishinaAPI`) is a mock server using `js/config.js`. A request can answer 409 `slot_taken`. References look like `TS-0001`. `mode: "demo"` keeps data in this browser only and sends nothing. See `docs/API.md`. `admin.html` is a demo back office (no login).

## Colour schemes

The five round buttons at the bottom switch the site (`data-skin` on `<html>`): Clay (default), Sage, Sand, Ink and Night (dark). The choice is remembered (`tishinaSkin`) and works as `?skin=sage`.

## Checked (2026-10-17)

- axe-core 4.10.2: no violations on the BG and EN home pages in all five colour schemes (1280 and 375 px), the admin page and the privacy pages.
- No horizontal overflow at 345, 360, 375, 768, 1280 and 1440 px; no requests to other sites (the map loads only after a click).
- Flow tested: a click on the hot stone card selected the massage, 90 minutes showed "€85", the gift box was ticked from the voucher link, a booking with reference TS-0001, visible in the demo back office.

## Not done / to do before real use

- Not tested on real phones, Safari or screen readers.
- No packs of sessions, memberships, online voucher purchase or payment, therapist calendars or reminders.
- Prices and therapists are examples. Photos are free Unsplash placeholders (`images/CREDITS.md`); replace them with the studio's own. Replace texts, address, phone, email and hours. Privacy page: fill in the yellow fields and get it reviewed.
- Add canonical/hreflang and `og:image` when the domain is known (comment in the page head).
