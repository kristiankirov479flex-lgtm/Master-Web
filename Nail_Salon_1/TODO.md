# Nail Salon 1 – research notes and build plan

Working file. Notes first, decisions in the middle, build checklist at the end.
Update the **Decisions** section as questions get answered, then build from this file.

Status (2026-10-16): **version 3 built**: one-page site (Bulgarian + English, 5 colour schemes), "Plan your visit" estimator, "Request this look", and a **request system that mimics a backend** (mock server, confirmation with reference number, availability, demo back office). Messaging buttons (Viber / Messenger / Instagram) were removed at the owner's request. See sections 5f and 5g.

---

## 1. What the research says

Confidence: **High** = named survey with a stated sample. **Medium** = consistent across several sources, but vendors or agencies.
**Low** = single vendor claim, unverified. Almost everything is US/UK data; **no Bulgarian data was found.**

### Clients still want to call (High)
- Zenoti survey, 1,000+ US salon/spa clients: **64% of nail regulars** say phone calls are the easiest way to manage appointments (highest of any beauty group).
- **83%+** of nail regulars have skipped a booking because they couldn't get through or online booking was too hard.
- 57% are much more likely to book with a salon that offers 24-hour access; 43% often need to call after hours.
- Top three things they value in a front desk: accuracy (56%), friendliness (54%), speed (51%).
- Source: <https://www.zenoti.com/en-uk/thecheckin/2026-nail-salon-trends>

### How people choose a salon (High, US, salons in general, not nail-only)
- Square survey, 1,800 US consumers: about two-thirds ask friends/family first; online reviews are second.
- **77%** say it is very or extremely important that a review names the specific service.
- 28% name Google Reviews as their favourite review source.
- About **50%** say a photo posted on Facebook or Instagram made them interested in a salon.
- Source: <https://squareup.com/gb/en/the-bottom-line/reaching-customers/attract-salon-customers>

### What a nail salon site should contain (Medium)
- A **price menu with starting prices**, grouped as hands / feet / add-ons. Cuts price-only calls.
- A **gallery of real work**, grouped by style (gel, acrylic, nail art, pedicure). Photos are the main way people judge a nail salon.
- Short **service descriptions with duration**.
- **Trust section**: reviews that name the service, the team, a short hygiene section.
- One clear call to action per page/service; booking possible in very few taps on a phone.
- Group bookings (parties, brides) mentioned by vendors; revenue claims unverified (Low).

### Booking, deposits, reminders (Low–Medium, vendor figures)
- Deposits and automatic reminders are widely linked to fewer no-shows.
- Claims seen: no-show rate 10–25%; with deposit ~90% show vs ~70% without; reminders at confirmation, 48 h and 24 h before. **Unverified.**
- ~40% of online bookings happen outside opening hours (vendor claim).
- Typical deposit suggested: 25–50% of the service price.

### Local search (Medium, agency sources; verify with Google's own docs)
- Google Business Profile is the main lever for "near me": correct **primary category** ("Nail salon"), secondary categories, listed services, real photos, hours, reviews, replies to reviews.
- Name, address and phone must match everywhere.
- Service-specific wording helps (e.g. gel, dip powder) once the salon really offers it.

### Not found / unknown
- **Bulgarian market:** which platforms salons and clients use (Booksy, Fresha, Anolla, Instagram, Viber, Facebook), and what a local booking flow looks like.
  - To do: look at 5–10 local competitor salons and note how they take bookings, their price format and their photo style.
  - To do: ask the owner how clients contact them today.
- Hygiene section and before/after galleries: no sourced guidance found; treat as a suggestion and use only facts the owner confirms.

---

## 2. What the page has to do (priority order)

1. **Show real work immediately.** Strong first photo, gallery sorted by style.
2. **Answer "how much and how long".** Price menu with starting prices and durations.
3. **Make contact effortless.** Booking path **plus** call and Viber buttons; a bar that stays on screen on phones.
4. **Build trust.** Reviews naming the service, the team, a short hygiene section (confirmed facts only).
5. **Be found locally.** Google Business Profile, hours, map, short FAQ.

Most visitors will likely arrive from Instagram on a phone, so **design phone first**.

---

## 3. Proposed page structure

- [ ] **Header:** logo, language switch (BG/EN), "Book" button, call button.
- [ ] **Hero:** one strong photo of finished nails, headline about the result, two buttons (Book / Call).
- [ ] **Popular services with prices:** 4–6 services, "from" prices, durations.
- [ ] **Gallery:** filter by style; opens large; real photos only; descriptive alt text.
- [ ] **Full price menu:** hands / feet / add-ons; removal, repairs, nail art priced per nail.
- [ ] **Why this salon / hygiene:** a few confirmed facts (e.g. sterilisation, single-use files). Nothing invented.
- [ ] **Reviews:** Google reviews that name the service; show rating and count; label the source.
- [ ] **Team:** photo and a line about each technician (if the owner agrees).
- [ ] **FAQ:** how long it takes, bring a reference photo?, removal, late/cancellation policy, deposit, payment, gift vouchers.
- [ ] **Booking / contact:** form or booking tool, phone, Viber, address, hours, map (map only after consent).
- [ ] **Gift voucher** request (simple form), optional.
- [ ] **Sticky mobile bar:** Book · Call · Viber.
- [ ] **Footer:** address, hours, Instagram/Facebook links, privacy notice, privacy settings.

---

## 4. Ideas to stand out

- **Shade picker (the one memorable move):** a row of polish colours that changes the page's accent colour live. Fits the subject. Must work with keyboard, respect reduced motion, and not break contrast (check each shade).
- **Instagram as entrance:** link to Instagram, don't embed it (an embed is a third party and needs consent). Use the salon's own photos on the site.
- **Group/bride booking** note in the services section if the salon offers it.
- **Deposit and reminders** story in the FAQ ("how booking works"), if a booking tool is added later.
- **Avoid clichés:** no pink-and-gold script-font template look unless the brand really is that. Let the photos carry the colour.

Style options to choose from (see Decisions):
- **A. Soft editorial:** very large photography, calm neutral palette, refined type.
- **B. Bold colour-block:** one strong colour per section, playful, graphic.
- **C. Clean boutique:** minimal, lots of white space, one precise accent.

---

## 5. Decisions (fill in before building)

| # | Question | Answer |
|---|---|---|
| 1 | Template to sell to several salons, or built for one real salon? | **Template to sell to different salons**, but with personality so a buyer gets a feel for it. No real client yet. |
| 2 | Booking: real online booking, or a request form to start with? | No client has asked yet; the goal is **portfolio examples**. Build a good **request form + call/Viber** first; design the page so a real booking tool can be added later. |
| 3 | If real booking: ready-made tool (name?) or custom? Deposits? | |
| 4 | Style direction: A, B or C (or mix)? | **Chosen: A, soft editorial + shade picker**, built so palette and fonts can be swapped per salon (see section 5b). |
| 5 | Photos available? Who shoots them? | None. **12 free Unsplash photos downloaded** (owner approved the list). See section 5c. |
| 6 | Price list and service list from the owner? | None. Use **sample prices based on Plovdiv salons**. See section 5a. |
| 7 | Contact channels the salon actually uses: phone, Viber, WhatsApp, Instagram, Facebook? | |
| 8 | Languages: Bulgarian + English? Others? | |
| 9 | Salon name, address, hours, team? (placeholders until known) | |
| 10 | Gift vouchers: yes/no? | |
| 11 | Existing Google Business Profile and reviews? | |

---

## 5a. Plovdiv price research (for the sample price menu)

Read on 2026-10-16 from salon pages on the **studio24.bg** directory (not the salons' own sites; may be out of date).
Prices are in **euro** (Bulgaria uses the euro). Some pages show prices with the decimal point missing
(for example `2301 €` = **€23.01**, a conversion from 45 лв); those were read as value ÷ 100.

| Service | Aurea Nails | DarLiNails | Pearl Nails | Geri Style |
|---|---|---|---|---|
| Gel polish manicure | 25 € (1 h 30, with rubber base) | 25 € (1 h) | 23.01 € short · 25.56 € medium · 30.68 € long | 17.90 € (1 h 30) |
| French / ombre / nail art manicure | 28 € (2 h) | 28 € (1 h 30) | 25.56 € (1 h 40) | – |
| Gel polish pedicure | 25 € (2 h) | 30 € (1 h) · 33 € with French | 30.68 € (1 h 45) | 23.01 € (1 h 30) |
| SPA pedicure with gel polish | 30 € (2 h) | – | – | – |
| Gel nail extensions | 45 € (3 h) | 40 € short · 45 € medium · 50 € long | 33.23 € short · 51.13 € medium · 61.36 € long | 40.90 € (2 h) |
| Gel refill | 30 € (2 h 30) | 30 € short · 35 € medium · 40 € long | 33.23 € – 61.36 € by length | – |
| Gel overlay on natural nails | 30 € (2 h) | – | – | 20.45 € (with gel polish, 1 h 50) |
| Gel polish removal | 10 € (20 min) | – | 12.78 € (with shaping) | 10.23 € (30 min) |
| Classic manicure, no polish | – | 12 € (45 min) | – | – |
| Classic pedicure, no polish | – | 20 € (45 min) | – | – |
| Broken nail repair | 2 € | – | – | 2.56 € per nail |

Read of the market: gel manicure about **€18–25**, gel pedicure **€23–30**, extensions **€40–50** (up to ~€60 for long),
refill **€30–40**, removal about **€10**. Durations: manicure 1–1.5 h, pedicure 1–2 h, extensions 2–3 h.
Also seen: working hours typically 09:00–19:00, some weekend and shorter days.
One search summary mentioned a cheaper salon (IVALI/Emaart, about €9–10 for a gel manicure); not checked on the page.

**Sample price menu for the template** (placeholder values, clearly marked as sample; owner replaces):

- **Hands:** classic manicure 12 € · 45 min; gel polish manicure 25 € · 1 h–1 h 30; gel manicure with French or nail art 28 € · 1 h 30; gel overlay on natural nails 30 € · 2 h; gel removal 10 € · 20–30 min; repair 2 € per nail.
- **Extensions:** short from 40 € · medium 45 € · long 50 €; refill from 30 €.
- **Feet:** classic pedicure 20 € · 45 min; gel polish pedicure 25–30 € · 1 h–1 h 30; SPA pedicure with gel polish 30 € · 2 h.
- **Add-ons:** nail art per nail, French tips, chrome/glitter (prices TBD; none sourced).

Sources: studio24.bg pages for
[Aurea Nails](https://studio24.bg/en/aurea-nails-salon-s12161),
[DarLiNails](https://studio24.bg/en/darlinails-art-studio-s11347),
[Pearl Nails](https://studio24.bg/en/pearl-nails-studio-s10748),
[Geri Style](https://studio24.bg/en/geri-style-beauty-salon-s2779).

---

## 5b. Style: chosen direction

The template must feel distinct but be easy to re-skin for each buyer.

- **Base:** A, soft editorial. Large close-up photos of hands on calm backgrounds, plenty of space, refined type.
- **Personality:** the shade picker (colour swatches that re-colour the accent), plus confident, warm copy.
- **Re-skinning:** put palette, fonts and the salon's name/contact in a few variables/one data file so a new salon is a quick change.
  Offer 2–3 ready "skins" for the portfolio (for example a warm neutral, a cool mauve, a deep green).
- **Check:** every shade must keep text contrast; test each skin with axe.

---

## 5c. Free stock photos plan

**Licences (read 2026-10-16):**

- **Unsplash License:** free for commercial and non-commercial use; attribution **not required** (appreciated); may modify;
  **may not be sold without significant modification**; may not compile photos to build a competing service.
  Nothing said about model releases or trademarks. <https://unsplash.com/license>
- **Pexels License:** free to use on websites, ads, social media; attribution **not required**; may modify;
  no unaltered resale; identifiable people must not appear in a bad light; do not imply endorsement by people or brands;
  no redistribution on other stock sites. <https://www.pexels.com/license/>

**Rules for this project:**

- Stock photos are **demo content only**. The offer to a salon should say they are replaced with the salon's own photos.
  Do not hand a buyer the stock photos as a product.
- Prefer **hands and close-ups with no identifiable faces** (no model-release guarantee on Unsplash).
- Avoid photos showing brand logos or trademarks.
- **Host locally** in `images/` (no hotlinking), compressed to about 150–300 KB, about 1600 px wide.
- Keep a `images/CREDITS.md` listing each photo's page URL, photographer and licence.
- Descriptive alt text for each photo (Bulgarian and English).
- **Downloading needs the owner's approval of the exact list first.**

**Downloaded 2026-10-16** (owner approved the list): 12 JPEGs, **about 2.5 MB total**, in `Nail_Salon_1/images/stock/`,
resized to 1600 px wide, each at most about 310 KB. Credits and licence are in `Nail_Salon_1/images/CREDITS.md`.
Raw downloads were kept outside the project (scratch folder) and are not part of the site.

| File | Orientation | Notes |
|---|---|---|
| `hero-light-pink.jpg` | portrait (1600×2553) | soft light pink on a white fur surface; hero candidate for a split layout |
| `black-tortoiseshell.jpg` | portrait | dark, moody; gold ring |
| `mauve-glitter.jpg` | square | mauve, white and silver glitter on white knit |
| `navy-gold-white.jpg` | portrait | ornate navy, gold and white; two hands |
| `blue-white-tree.jpg` | landscape-ish (1600×1244) | winter tree nail art |
| `black-silver-ring.jpg` | landscape (1600×1067) | black manicure, grey knit |
| `pink-selective-focus.jpg` | landscape (1600×1067) | pink on grey, "love" art |
| `hand-with-flower.jpg` | portrait | warm, orange flowers background |
| `pink-on-white.jpg` | portrait | soft pink nudes on white textile |
| `manicure-closeup.jpg` | portrait | colourful abstract nails. **Shows the lower part of a face (chin and neck): keep out of prominent places, or replace.** |
| `hand-on-pink.jpg` | portrait | flat-lay of nails on pink; good for a colour/shade section |
| `polish-bottles-shelves.jpg` | portrait | polish bottles on shelves; colour/shop section |

Design notes from the contact sheet:
- Most photos are **portrait**, so use editorial split layouts, tall gallery tiles and a masonry/mixed-size grid; only 3 are landscape.
- Several are warm/neutral with soft pinks, which suits the chosen direction; two are dark and moody (good contrast tiles).
- `hero-light-pink.jpg` plus `pink-on-white.jpg` set the default palette (warm nude/pink); the shade picker moves away from it.
- Still missing: salon interior, tools/hygiene, and a team photo (use a neutral graphic or leave blank).

**Candidates before download (for reference):**

Search page: <https://unsplash.com/s/photos/nail-art>. All are hands or product close-ups (no faces).
Page URL = `https://unsplash.com` + the path.

| Use | Path |
|---|---|
| Hero candidate (light pink, soft surface) | `/photos/hand-with-light-pink-manicured-nails-vtQHwU4F13s` |
| Gallery: black and tortoiseshell with gold ring | `/photos/hand-with-black-and-tortoiseshell-nails-tXwBDZS2JxQ` |
| Gallery: mauve, white and silver glitter | `/photos/hand-with-mauve-and-glitter-nails-Y14F-1vzVds` |
| Gallery: ornate navy, gold and white | `/photos/womans-hands-with-ornate-navy-gold-and-white-nails-v9agFscJCIE` |
| Gallery: blue and white with a tree design | `/photos/a-person-with-a-blue-and-white-manicure-with-a-tree-on-it-zZ6Y78ANoEI` |
| Gallery: black manicure, silver ring | `/photos/person-wearing-silver-ring-with-black-manicure-KZKbGgQPCtU` |
| Gallery: pink manicure, selective focus | `/photos/selective-focus-photography-of-womans-pink-manicure-r-Ej0NQmFlQ` |
| Gallery: hand holding a flower | `/photos/a-womans-hand-with-a-manicure-holding-a-flower-OIEU0eopPT4` |
| Gallery: pink manicure on white textile | `/photos/person-with-pink-manicure-on-white-textile-hvqHtZqNMeI` |
| Gallery: manicure, close-up | `/photos/womans-nails-with-manicure-jRXxNpA6d_k` |
| Gallery: hand on pink surface | `/photos/persons-hand-on-pink-surface--4iMX-4MIZ8` |
| Colour / shade section | `/photos/nail-polish-bottles-on-gold-shelves-OpjlRo-31SI` |

Skipped on purpose: photos with identifiable faces (woman at a nail salon, woman with nail art on her face, etc.).
Need still: a "salon interior / tools" photo, and a photo for the team section (use a neutral illustration or leave blank).

---

## 5d. Colour schemes: top 5 shortlist (2026-10-16)

**What the research supports (and what it doesn't).** No study proves one palette "sells best". Facts used:

- Pantone's 2026 Colour of the Year is **Cloud Dancer (PANTONE 11-4201), a white**, announced 4 Dec 2025 (the first white in the programme, framed as calm). Sources: [Smithsonian](https://www.smithsonianmag.com/smart-news/pantones-color-of-the-year-for-2026-is-a-blank-canvas-called-cloud-dancer-or-in-other-words-white-180987805/), [Global Cosmetics News](https://www.globalcosmeticsnews.com/pantone-introduces-cloud-dancer-as-the-2026-color-of-the-year/).
- Fall/winter 2026 nail trends: **chocolate/espresso browns, oxblood and burgundy reds, deep moody greens, smoky greys, midnight navy**, plus chrome/jelly finishes. Sources: [Marie Claire](https://www.marieclaire.com/beauty/nails/best-fall-2026-nail-colors), [Bustle](https://www.bustle.com/beauty/winter-2026-nail-polish-color-trends) (trend articles; treat as editorial opinion).
- Salon-branding advice (low-quality sources): soft neutrals plus **one accent**, keep the palette small, and **check local competitors**: if they use pink and white, choose something that contrasts (the example given was navy and amber).
- Calm, cool tones are a common association with trust and relaxation, but that is convention, not tested conversion data. Consistent contrast on call-to-action buttons matters more than the hue.

So the five are **curated picks**, chosen for: fit with our photos (nude/pink plus a few dark ones), 2026 trend support, difference from pink-and-white salons, and readable contrast.

**Preview with the real photos and live contrast ratios:** `Nail_Salon_1/docs/palettes.html`
(open via the local preview server: `http://localhost:5180/Nail_Salon_1/docs/palettes.html`).

All values below pass WCAG AA (4.5 or higher) for every pairing checked: text on page, grey text on page and on tinted band, button text, accent links on page and on tinted band, text on dark band, button on dark band (35 of 35 pass).

| # | Name | bg | surface | ink | muted | accent | on-accent | soft | dark | on-dark | dark-accent |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | **Cloud & Rosewater** (default) | `#F4F2EE` | `#FFFFFF` | `#2A2326` | `#5E5559` | `#96445A` | `#FFFFFF` | `#EBDCD6` | `#3A2430` | `#F4E9E6` | `#E6B8B8` |
| 2 | **Sage & Stone** | `#F3F4EF` | `#FFFFFF` | `#1F2A25` | `#55615B` | `#3E5F4F` | `#FFFFFF` | `#DCE4D8` | `#24352D` | `#EAF0E8` | `#C7D8BD` |
| 3 | **Espresso & Cream** | `#F8F2EA` | `#FFFFFF` | `#2B1D18` | `#665349` | `#6B3F2B` | `#FFFFFF` | `#EADBCB` | `#3A2620` | `#F6ECE2` | `#E2B98E` |
| 4 | **Oxblood & Blush** | `#FBF4F2` | `#FFFFFF` | `#2B1519` | `#6A5055` | `#7B1E2E` | `#FFFFFF` | `#F0D9D8` | `#3B141C` | `#FBEDEA` | `#E8B7A8` |
| 5 | **Midnight & Champagne** | `#F7F4EE` | `#FFFFFF` | `#14213D` | `#4F5A70` | `#14213D` | `#FFFFFF` | `#E7E1D3` | `#101B2D` | `#EEF0F4` | `#D4B27A` |

Why each, and the risk:

1. **Cloud & Rosewater:** warm off-white (nod to Cloud Dancer) with dusty rose; matches the nude/pink photos. *Risk:* pink and white is what many salons already use.
2. **Sage & Stone:** calm deep green; green is on the 2026 trend list, reads calm/trustworthy, differs from pink salons, and complements the pink photos. *Risk:* less obviously "nails".
3. **Espresso & Cream:** chocolate brown on cream, the headline shade for fall/winter 2026; grown-up and editorial; suits the moody photos. *Risk:* can feel heavy if overused.
4. **Oxblood & Blush:** burgundy on blush; glamorous and feminine; wine reds lead trend lists. *Risk:* strongest "seasonal" feel; may date.
5. **Midnight & Champagne:** navy with champagne gold on ivory; premium, trustworthy, strongest contrast to local pink-and-white. *Risk:* least playful; champagne is used only on dark areas (on ivory it would fail contrast).

**Recommended order:** 1 → 2 → 3 → 4 → 5. Use **#1 as the default skin** and ship **#2 and #5** as extra skins for the portfolio (three clearly different looks).

**Build notes:**

- Put these in CSS variables (`--bg`, `--ink`, `--accent` ...) so a skin is one class on `<html>` (e.g. `data-skin="sage"`).
- The **shade picker** changes only the accent family; recheck contrast for each shade it offers (accent on bg, button text on accent, accent on soft).
- Never put champagne/rose "dark-accent" colours on the light background (they are for dark bands and buttons on dark).
- Photos stay unfiltered; do not tint the stock photos to match a palette.

---

## 5e. Built: version 1 (2026-10-16)

One-page site, no backend, plain static files. **Name "Nuance Nail Studio" is a placeholder.** All text is sample copy.

- Pages: `index.html` (Bulgarian), `en/index.html` (English), `privacy.html`, `en/privacy.html`.
- Files: `css/style.css`, `js/main.js`, `fonts/` (Cormorant Garamond + Onest, reused from other projects, Latin + Cyrillic), `images/stock/` (12 photos + 800 px versions), `images/CREDITS.md`, `docs/palettes.html`, `tools/` (optional page generator).
- Sections: header with language link, hero (arch photo), 3 promise points, gallery (filter: all / natural / nail art / bold, with viewer), services and prices (sample, Plovdiv-based), example reviews (clearly labelled), FAQ, request form + contact + map on click.
- **Colour scheme buttons at the bottom (dock):** 5 schemes (Cloud & Rosewater default, Sage & Stone, Espresso & Cream, Oxblood & Blush, Midnight & Champagne). The choice is remembered in the browser; `?skin=sage` in the address also works.
- **Request form:** no server. Pressing the button opens the visitor's email app with the details filled in (`mailto:`), plus call and Viber links.
  The day and time are a **date picker and a time dropdown** (not free text). The dropdown is always **24-hour** and never greyed out (before a date is chosen it shows the weekday times) (a native time input follows the visitor's system and can show AM/PM, so it was replaced). The earliest date is today, and the list holds the start times for that day every 15 minutes (sample: Mon-Fri 09:00-18:00, Sat-Sun 10:00-17:00; edit `START_WEEKDAY` / `START_WEEKEND` at the top of `tools/build_pages.py` together with the opening hours; `SLOT_MINUTES` in `js/main.js` sets the gap). The date field still follows the visitor's system format (for example dd.mm.yyyy in Bulgaria). The email shows the date in words, for example "Saturday, 17 October 2026". A mobile bar at the bottom has Call / Viber / Request.
- Map: OpenStreetMap, loads only after the visitor presses the button (no consent banner needed because nothing is saved).
- Checked: axe accessibility audit passes (0 violations) on all 4 pages, the two main pages in **all 5 colour schemes**; no requests to other sites; no broken images; tested at 1440 px and 390 px.
- Default skin = #1 Cloud & Rosewater. The shade picker idea became these colour scheme buttons.

---

## 5f. Edge features built (2026-10-16)

1. **"Request this look":** the photo viewer has a "Request this look" button. It closes the viewer, adds the photo (thumbnail, description, link) to the request form and moves the cursor to the Name field. A chip in the form shows it and can be removed.
2. **Plan your visit:** section after the price list. Pick a service (and length for extensions), tick extras, see an estimated **price range and time**, press "Add to my request". It fills the Service field, shows a chip, and the time list only offers start times that fit before closing.
3. **Removed on request:** the Viber / Messenger / Instagram buttons, links and copy-to-clipboard flow, and the "send by email" flow. The mobile bar is now Call + Request.

## 5g. Request system that mimics a backend (2026-10-16)

The owner may add a real backend with a database for a customer later, so the form behaves like it talks to one.

- `js/api.js` is a **mock server** (`NuanceAPI`). The page only calls it; in demo mode it keeps requests in the visitor's browser (`localStorage`), in live mode the same calls become HTTP requests (see `docs/API.md`). Switch with `MODE` / `API_BASE` at the top of `tools/build_pages.py` (writes `js/config.js`).
- **Form flow:** "Sending..." state with a locked button, then a **confirmation card** with a reference number (NU-0001...), status "Waiting for confirmation", a summary and a "Make another request" button. A clear "Demo mode" notice is shown while in demo mode.
- **Availability:** the time list is asked from the server for the chosen date and visit length. Times already requested are removed (capacity = 1 visit at a time; change `CAPACITY`). If someone takes the time while you fill in the form, you get "Sorry, that time was just taken" and the list refreshes (HTTP 409 `slot_taken`). Invalid or past dates are rejected (422).
- **Demo back office:** `admin.html` (linked in the footer as "Demo back office"; English with `?lang=en`). Lists requests, lets you set Waiting / Confirmed / Declined, delete, add sample requests and reset. **Declining frees the time again.** Demo only: stored in this browser, no login.
- `docs/API.md` describes the endpoints, JSON, errors, database table and the things a real system still needs (notifications, login, spam protection, privacy notice, backups).
- Privacy notices describe the demo mode; they contain a yellow note to rewrite that sentence when a real backend is connected.

**Verified:** real clicks for the whole flow; sending/busy state; confirmation; availability blocking and freeing; 409 race; 422 validation; back office status, filter, delete, seed, reset (BG and EN); axe audit passes in all 5 colour schemes for the public page (form, error and confirmation states) and the back office; 390 px layout; no outside requests.

**Before using with a real salon:** either connect a real backend (and set `MODE = 'live'`) **or** replace the form with something that really reaches the salon. In demo mode nothing is sent to anyone.

---

## 5h. Motion (2026-10-16)

Short, smooth animations (0.25-0.9 s), all off for visitors who prefer reduced motion.

- **Page load:** one hero sequence: headline, text, buttons and meta fade up in turn; the arch photo rises and its image settles; the small photo and the chip follow; the colour dock slides up last.
- **Scroll:** sections, price groups, plan card, reviews, FAQ rows, contact blocks and gallery tiles ease in as they come into view (gallery tiles cascade by column). After the animation the normal styles come back. Elements only start hidden when the browser supports it and motion is allowed (class `js-reveal` set in the page head), so nothing is lost without scripting.
- **Actions:** gallery filter pops tiles in; the photo viewer fades open and cross-fades between photos; the planner fades in extras and pulses the new price/time; chips slide in; the confirmation card lands and the reference number "stamps" in; errors slide in; FAQ answers fade down; buttons lift slightly on hover.
- **Not animated on purpose:** the sending spinner keeps turning (it is a progress indicator).
- **Where:** the motion block in `css/style.css` ("Motion: short and smooth") and the "Scroll reveal" block in `js/main.js`.

---

## 6. Standards to reuse from the Vila Stefani and Master Web projects

Do these **from the start** this time.

- **Structure:** `index.html`, `css/`, `js/`, `images/`, `fonts/`, `docs/`. Keep content/data in a `js/data.js`-style file where it helps.
- **Languages:** build **separate static pages per language** with `hreflang` from day one (e.g. `/` and `/en/`), not a JavaScript swap. See `Vila-Stefani-Devin-main/SEO-TODO.md` for why.
- **Fonts:** self-host (Latin **and Cyrillic** support is required; check before choosing a font). No Google Fonts requests.
- **No third parties before consent:** map and any embed load only after consent. Use the same consent banner pattern as the Vila site. Photos hosted locally.
- **Privacy notice** page in both languages, linked from the footer; fill owner details; `noindex` until filled.
- **Contact placeholders in one place** (phone `+359 000 000 000`, email `email@example.com`) so they are easy to replace.
- **Accessibility:** skip link, landmarks, visible focus, reduced motion, alt text strategy, contrast checked for every colour (including each shade in the picker). Run axe before showing it.
- **Avoid CSS class name clashes** (an earlier `.rev` clash broke a layout); prefix or use distinct names per component.
- **Performance:** compress photos (~150–300 KB), `width`/`height` on images, `loading="lazy"` below the fold, load the hero image directly (not via a script).
- **SEO basics:** titles/descriptions per language, structured data (`HealthAndBeautyBusiness` / `NailSalon` type), sitemap, robots, `og` image, Google Business Profile link.
- **FAQ:** visible text, answers supplied by the owner; no invented facts.
- **Test at 390 px and 1440 px**, in Bulgarian and English, before saying it's done.

---

## 7. Build checklist (after decisions)

1. [x] Prices: Plovdiv sample menu collected (5a). [x] Style direction: A + shade picker. [x] 12 photos downloaded (5c).
2. [ ] Look at more Bulgarian competitor salons (4 price lists done; still note booking method, photo style, what their own sites look like).
3. [x] Style direction chosen; [x] colour shortlist (5d). [ ] Pick the default skin; write a short design plan (type, layout, shade picker).
4. [ ] Pick and self-host fonts (Latin + Cyrillic).
5. [ ] Build the Bulgarian page, phone first.
6. [ ] Build the English page; add `hreflang`.
7. [ ] Gallery with filter and viewer; price menu; FAQ.
8. [ ] Booking path (form first; tool later) and the sticky mobile bar.
9. [ ] Shade picker (if kept), with contrast checks.
10. [ ] Consent banner, map gating, privacy pages.
11. [ ] Meta tags, structured data, sitemap, robots.
12. [ ] Accessibility audit, mobile and desktop screenshots, speed check.
13. [ ] Add the project to the Master Web portfolio page (card, sitemap entry).

---

## Sources

- Zenoti, 2026 nail salon trends: <https://www.zenoti.com/en-uk/thecheckin/2026-nail-salon-trends>
- Square, how consumers discover salons: <https://squareup.com/gb/en/the-bottom-line/reaching-customers/attract-salon-customers>
- SchedulingKit, nail salon booking pages (vendor): <https://schedulingkit.com/booking-page/nail-salons>
- SimplyBook.me, online booking statistics (vendor): <https://simplybook.me/blog/online-booking-statistics>
- Ranktracker, nail salon SEO (agency): <https://www.ranktracker.com/blog/nail-salon-seo/>
- Anolla, salon booking software, Bulgarian (vendor): <https://anolla.com/bg/softuer-za-saloni-za-krasota>


---

## 8. Open items after version 1

**Replace before showing to a real salon (all placeholders):**

- [ ] Salon name (`Nuance`), tagline, address (`Primer St. 1, Plovdiv`), hours, phone `+359 000 000 000`, Viber number, email `email@example.com`. Search both languages; `tools/build_pages.py` has them at the top.
- [ ] Prices (sample, from Plovdiv salons), services, FAQ answers (sample policies: 24 h cancellation, 15 min late, deposit).
- [ ] Promise section claims ("tools are sterilised between clients") must be true for that salon.
- [ ] **Example reviews** are placeholders and labelled "Example". Replace with real Google reviews (with the service named) or remove the section.
- [ ] Photos: replace stock photos with the salon's own (keep file names or update the lists). `manicure-closeup.jpg` (shows part of a face) is **not used** on the page.
- [ ] Privacy pages: fill the yellow fields, then remove the `noindex` line.

**Not built yet (ideas from research):**

- [ ] Real online booking (tool or custom), deposits, reminders. Today: request form + call/Viber.
- [ ] Instagram / Facebook links (add the salon's real accounts; link, don't embed).
- [ ] Team section (needs real photos), hygiene photos, interior photos.
- [ ] Gift vouchers request.
- [ ] Per-service pages / extra SEO pages (gel, extensions, pedicure) for local search.
- [ ] Google Business Profile setup; structured data is in place but uses placeholder address and phone.

**Before publishing:**

- [ ] Real web address, then add `canonical`, `hreflang` (bg / en / x-default) and `og:image` (comments are in the page head), and add both pages to a sitemap.
- [ ] Speed check on mobile (Lighthouse). Photos are already resized; the hero is loaded directly.
- [ ] Test in Safari and on a real phone (photo viewer, `color-mix` colours, sticky header).
- [ ] Screen reader pass (NVDA or VoiceOver); automated checks are done, manual ones are not.
- [ ] Add the project to the Master Web portfolio page (card, preview, sitemap entry).
- [ ] The colour scheme dock is a **demo feature for showing buyers**. For a real salon, remove the dock and keep one skin (set `data-skin` on `<html>` and delete the `.dock` block and the skin code in `js/main.js`).


---

## 9. What is still missing, and the edge (research 2026-10-16)

### 9a. Evidence gathered

**Contact habits (what the site must serve):**
- 64% of nail regulars say calling is the easiest way to manage appointments; 83%+ skipped a booking because they couldn't get through or online booking was too hard; 43% often need to call after hours (Zenoti, US survey of 1,000+). <https://www.zenoti.com/en-uk/thecheckin/2026-nail-salon-trends>
- Bulgaria (DataReportal, Digital 2026): 5.84 M internet users (87.1%); 4.50 M social media user identities (67.1% of the population). <https://datareportal.com/reports/digital-2026-bulgaria>
- Facebook: about 4.7 M users in Bulgaria, about 70% of the population (NapoleonCat, from Meta ad estimates, June 2026); Messenger about 3.8 M, about 57% (Dec 2025). <https://stats.napoleoncat.com/facebook-users-in-bulgaria/2026/06/>
- Chat widgets installed on Bulgarian sites: Messenger 41.7%, Viber 39.6%, WhatsApp 19.4% (wmtips). This shows what businesses install, not what people use. <https://www.wmtips.com/technologies/instant-messaging/country/bg/>
- **Not found:** Instagram and TikTok numbers for Bulgaria; how Plovdiv nail clients actually book (to check by looking at competitors and asking the owner).

**What is technically possible without a backend (prefilled messages):**
- **WhatsApp:** `https://wa.me/<number>?text=<url-encoded text>` opens a chat with the text typed in (secondary sources; Meta's page not reached; confirm the limit of about 140 characters).
- **Messenger:** Meta documents `m.me/<PAGE>?text=...` (prefilled text) and `?ref=...` (tracking). <https://developers.facebook.com/docs/messenger-platform/discovery/m-me-links>
- **Viber:** `viber://chat?number=` opens a chat; a prefilled `text` is **not confirmed** for normal numbers (only documented for bot links). So for Viber use "copy the request text, then open Viber". Test on a real phone.
- Email (`mailto:`) already works.

**Local search:**
- Google Business Profile has an **appointment link** (can point to your own page) and a Booking Button (needs a Google-partner scheduler). Google now expects links to let people complete the action, so the link must lead to something that works. <https://whitespark.ca/google-business-profile-guide/bookings/>
- Reviews matter most when they name the service (77% in the Square survey).

**Retention (vendor-sourced, treat with care):** top salons rebook about 69% of clients vs about 40% average (Zenoti). Referral and loyalty programmes are widely recommended but usually need a backend or paper cards.

### 9b. Gaps in the current page

1. The gallery and the request form are not connected (people can't say "I want this look").
2. The form ignores how long a service takes (a long service can be requested too late in the day).
3. Price list is static: no way to see the cost of a combination (length + finish + art + removal).
4. Only call / Viber / email: no Messenger or WhatsApp, no social links.
5. No review prompt (Google review link / QR); no "what to expect" or hygiene proof; no seasonal content.
6. Structured data does not list the services and prices.
7. No measurement of what works (calls, clicks, requests).

### 9c. The edge: ideas ranked

| # | Idea | Why it should help | Effort | Needs from the salon |
|---|---|---|---|---|
| 1 | **DONE (v2)** **"Plan your visit" estimator**: pick service, length, finish, art level, removal; see a price range and time; it fills the request. The time list then only offers start times that finish before closing. | Price transparency; removes phone back-and-forth; fits the 83% who skip hard booking flows. Competitors' directory pages show only a fixed list. | Medium | Price and duration rules |
| 2 | **DONE (v2)** **"Book this look" on every gallery photo**: adds the photo as a reference in the request. | Photos drive the decision; clients bring reference photos. Turns the gallery into a booking funnel. | Low | Real photos |
| 3 | **REMOVED (owner decision; replaced by the backend-style request system)** **Send the request where clients are**: WhatsApp and Messenger with the text prefilled, Viber and email with copy-and-open, plus call. | Matches the 64% who like to call and Bulgaria's Facebook/Messenger/Viber habits; works after hours. | Low | Which channels the salon uses |
| 4 | **Review engine**: "Leave a review" button + printable QR for the counter; prompt asks which service they had. | Reviews are the strongest decision factor; specific reviews convince. Feeds local search. | Low | Google review link |
| 5 | **Seasonal "Now trending" block** (e.g. espresso, oxblood, deep green, smoky grey, midnight navy) with "book this look". | Fresh content, shows expertise, links to the colour schemes already built. | Low–medium | Salon's own versions; seasonal updates |
| 6 | **Add to calendar (.ics)** after sending a request, plus an optional "remind me to rebook in 3 weeks" file. | Cheap retention nudge without a backend. | Low | none |
| 7 | **"What to expect" strip** (first visit steps, hygiene, aftercare) and a short **team** section. | Trust; answers hesitation; hygiene claims must be true. | Low | Real facts and photos |
| 8 | **Richer structured data** (services and prices, social profiles, review link) and a Google appointment link to the estimator. | Local and AI search readiness. | Low | Real details |
| 9 | **Privacy-friendly click counts** (call / message / request) with a short monthly summary. | Proves the site pays for itself; supports a care-plan offer. Needs disclosure in the privacy notice. | Medium | Consent decision |

Business angles for the freelancer (not site features): seasonal refresh as a paid retainer; review QR cards as a print add-on; monthly report; photo shoot upsell.

### 9d. Recommendation

Build in this order: **#2 and #3 first (quick, visible)**, then **#1 (the headline feature that makes the template memorable)**, then **#4 and #8**. Keep #5-#7 as content the salon provides, and #9 as an optional paid extra.

### 9e. Caveats

- No independent study was found that measures the conversion lift of an estimator, gallery-to-request links or prefilled messages. The case rests on the surveys above plus reasoning; the Zenoti and loyalty figures are vendor-sourced.
- Local competitors' own websites were not audited; the Plovdiv listings seen were directory pages, which suggests many salons may rely on directories and social media (to verify before using as a selling point).
- Viber prefill is unconfirmed; test on a real phone.
- Everything above must keep the privacy rules from section 6 (no third-party scripts before consent; links only).
