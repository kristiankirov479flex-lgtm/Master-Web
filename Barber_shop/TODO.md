# Ironwood Barbershop – template notes and to-do

Status (2026-10-16): **version 1 built.** One-page site in Bulgarian (`/`) and English (`/en/`), 5 colour schemes with buttons at the bottom,
price list, "Plan your visit" estimator, "Request this cut" from the gallery, and the same **backend-style request system** as the nail template
(mock server in the browser, confirmation with a reference number, availability, demo back office). Brand name "Ironwood" is a placeholder.

This is a **template to sell to different barbershops**. No client asked for it yet; it is portfolio work. Demo photos are free stock photos,
prices are sample prices from Plovdiv. Nothing is sent to anyone in demo mode.

---

## 1. What a barbershop site must do (research summary)

The aim of the site is one thing: **a visitor books a chair.** Everything else supports that.

1. **Booking above the fold, always reachable.** Sticky "Book a chair" button in the header, a Call + Book bar on phones.
2. **Prices and times visible.** Men compare prices before they choose; showing price and duration for every service removes the main doubt.
3. **Proof of skill = photos.** Close-up cuts and beards, not stock-looking lifestyle shots. A gallery with a viewer is the main trust signal.
4. **Proof of other people's trust = reviews.** Google rating and a few short quotes. (Here: example text, to be replaced.)
5. **Mobile first.** Most visitors arrive from Google Maps or Instagram on a phone.
6. **Location and hours clear** (Google Business Profile matters more than the site for "barber near me").
7. **Personality.** Dark, warm, "club" feel with a brass accent; the barber-pole stripe is the only decoration.

Colour research: dark base + one warm metal accent (brass, copper, gold) reads premium; deep blue or green reads established and trustworthy;
one strong accent colour for the booking button. I found **no barber-specific conversion studies**, so the ranking below is judgment, not data.
Pages used: sliderrevolution.com (barbershop website examples), webflow.com/list/barber, lovart.ai (barber brand kit),
minervabeauty.com (barbershop design), purespadirect.com (colour psychology for salons), AISeL pilot study (blue = most trust, black = least),
site2b.ua (warning: all-blue palettes weaken buttons).

## 5a. Plovdiv sample prices (EUR, from online listings, 2026-10-16)

Source: Fresha listings for Plovdiv barbershops (Studio Exit, Studio 38, Barber Studio 1 and 2, Studio 22, Hairshot, Medusa, Barbershop 4004,
FITBARBER, MODE | Hair Aesthetics, Above Cutz) and studio24.bg Plovdiv listings. The listings are partly inconsistent ("from" prices, some "€0"
placeholders, mixed BGN), so the table is a **range**, not an exact market price. Confirm with the real shop.

| Service | Range seen in Plovdiv | Used in template |
|---|---|---|
| Haircut | 11 – 20 € (short hair about 12 – 15, long 15 – 18, premium 18 – 20) | 15 € |
| Fade / detailed | about 10 – 18 € | 18 € |
| Buzz cut | 5 – 11 € | 10 € |
| Beard trim | 5 – 10 € | 10 € |
| Haircut + beard | 15 – 25 € (most 18 – 22) | 22 € |
| Skin fade + beard | no clear listing | 25 € (estimate) |
| Hot towel / straight-razor shave, head shave | not listed in sources | 15 € (estimate, mark as sample) |
| Kids, extras (wash, brows, grey blending) | not listed | 12 € / 5 € / from 15 € (estimates) |

Rows marked "estimate" are **not from a source**. The page says "Sample prices". Replace with the real shop's list.

## 5c. Photos

17 free photos from Unsplash (Unsplash License: free for commercial use, attribution not required, may be modified, may not be sold unaltered).
All 17 are used; see `images/CREDITS.md` for photographer and link. Downloaded at 1600 px wide and recompressed, plus 800 px versions.
Only photos marked **Free** were used (Getty-labelled "Unsplash+" photos need a paid licence and were skipped).
**All are placeholders**: the real shop replaces them with its own photos (the shop, the team, real cuts, with permission of the clients).

## 5d. The five colour schemes (the switch buttons at the bottom of the page)

All pairs contrast-checked (WCAG AA, 4.5:1 or higher for text). Axe audit passes in all five on both language pages and the back office.

| Key | Name (EN / BG) | Background | Surface | Text | Accent | Mood | Best for |
|---|---|---|---|---|---|---|---|
| `brass` (default) | Black & Brass / Черно и месинг | `#0F0F0F` | `#1A1A1A` | `#F2EDE4` | `#C8A24A` | premium, classic | almost any shop (most likely sale) |
| `navy` | Midnight & Copper / Нощно синьо и мед | `#0E1A2B` | `#16263B` | `#EEF1F5` | `#D08A55` | trustworthy, polished | shops that want to look established |
| `forest` | Forest & Gold / Гора и злато | `#12261F` | `#1B3329` | `#F1EBDD` | `#D2A857` | heritage, calm | traditional "old town" shops |
| `heritage` | Barber Pole Heritage / Класика с червено | `#F4EFE6` | `#FFFFFF` | `#1B1B1B` | `#B3261E` | friendly, family | neighbourhood shops, daylight feel (only light scheme) |
| `graphite` | Graphite & Orange / Графит и оранжево | `#1C1D1F` | `#26282B` | `#F3F2EF` | `#FF6A2B` | modern, streetwear | fade and beard specialists, young clients |

Contrast (text on background / accent on background / button text on accent): brass 16.4 / 8.0 / 7.8, navy 15.4 / 6.2 / 6.2,
forest 13.4 / 7.2 / 7.2, heritage 15.0 / 5.7 / 6.5, graphite 15.1 / 5.9 / 5.9.
Choice is saved in the browser (`localStorage` key `barberSkin`) and can be forced with `?skin=navy`.
The switch buttons are a **template preview feature**: remove the `<aside class="dock">` block from the template once a shop has chosen its scheme.

## 5e. How the site is built

- Static files, no build tools. `tools/build_pages.py` writes `index.html`, `en/index.html` and `js/config.js` from one template and two text dictionaries
  (`tools/build_privacy.py` does the privacy pages). Constants at the top: hours, phone, email, capacity (2 chairs), slot gap (30 min), brand, mode.
- Fonts self-hosted (Cormorant Garamond 600/700 and Onest, Latin + Cyrillic). No third-party requests; the map loads only after a click.
- Differences from the nail template: squarer shapes, uppercase headings, barber-pole stripe (above the promise strip and the footer),
  framed hero photo, dotted price leaders, dark colour schemes (`color-scheme` set per skin so the date picker matches).
- Gallery: filter Cuts / Beards / The shop; the photo viewer offers "Request this cut" (hidden for photos of the shop itself).
- Plan your visit: choose a service (haircut has a style choice: classic or skin fade), extras; shows estimated price and time; "Add to my request"
  fills the form and limits start times to those that fit before closing.
- Request system: see `docs/API.md` (same as the nail template; names `IronwoodAPI`, `ironwood.requests`, reference `IW-0001`).
  Capacity 2 means two visits can overlap; the third gets "that time was just taken" (HTTP 409 `slot_taken`).
- Demo back office: `admin.html` (English `?lang=en`). Demo only: no login, data lives in the browser.

**Verified (2026-10-16):** BG and EN pages and back office pass axe (WCAG 2.2 AA + best practice) in all 5 colour schemes; full request flow with real
form data (reference IW-0001, availability, capacity 2 blocking the third request); 390 px layout without horizontal scroll; no outside requests.
**Not tested:** real phones, Safari, screen readers.

## 8. Before using with a real barbershop

- [ ] Replace placeholders: name (Ironwood), address (`Primer St. 1`), hours, phone, email, prices, FAQ answers (payment, cancellation, walk-ins), example reviews.
- [ ] Replace all photos with the shop's own (and update `alt` texts in `GALLERY` in `build_pages.py`); delete `images/stock` and `images/CREDITS.md` if unused.
- [ ] Fill the yellow fields in the privacy notices, then remove `noindex` from them.
- [ ] Real domain: canonical and hreflang links, `og:image`, sitemap, robots (see the comment in `tools/page_template.html`).
- [ ] Decide: connect a real backend (`MODE = 'live'`, see `docs/API.md`) or replace the form. **In demo mode nothing reaches the shop.**
- [ ] Remove the colour-scheme buttons (the `dock` block) when the shop has chosen a scheme.
- [ ] Test on real phones (iPhone Safari, Android Chrome) and with a screen reader.
- [ ] Google Business Profile, review link / QR code on the counter, Instagram link.
- [ ] Richer structured data (price list, opening hours exceptions, `sameAs` links).

## 9. Ideas not built yet (barbershop-specific edge)

| # | Idea | Why |
|---|---|---|
| 1 | **Choose your barber** (photo, speciality, own availability) | Clients are loyal to a person; needs per-barber capacity in the API |
| 2 | **Reminder message** the day before (SMS / Viber / email) | Fewer no-shows; needs a backend |
| 3 | **Memberships and gift vouchers** | Repeat visits, a gift for Christmas and Father's Day |
| 4 | **Loyalty stamp** (every 10th cut free) | Simple to show, easy to sell |
| 5 | **Walk-in wait time** ("2 chairs free now") | Needs live data |
| 6 | **Review button + printable QR code** | Reviews drive "barber near me" ranking |
| 7 | **Product shop** (pomade, beard oil) | Extra income; larger project |
