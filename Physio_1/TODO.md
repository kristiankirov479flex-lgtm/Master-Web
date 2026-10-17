# Motus – physiotherapy design 1 (a plain clinic)

Status (2026-10-17): **built, and reworked once** (the first version was too thin to sell). A premium website for a **physiotherapy clinic**: a deep navy hero with a photo, a floating **"Where does it hurt?"** card (eight areas that pre-select the booking form), four big facts, six condition cards with typical problems, a four-step method on a dark band, three pillars (hands-on therapy, exercise, understanding), **two named therapists with portraits, credentials and tags**, a photo gallery of the clinic, **three price cards** (first assessment, therapy session, pack of 8 as "best value"), a "see a doctor first" notice, a dark **booking panel** with a form, an FAQ with an honest "what if I do not improve?" answer and a contact block. **Made-up content** ("Motus", Plovdiv). Bulgarian (`/`) and English (`/en/`).

**Everything about the clinic is an example**: name, therapists, diplomas, membership numbers, prices, hours, address and phone. The therapist portraits and all photos are stock placeholders. Replace all of it for a real clinic.

## Research behind the design (2026-10-17)

Physiotherapy-site guides and clinic pages (Qreative Themes, a Framer template page, a clinic's "first visit" page, an NHS Wales FAQ) agree on:

- **Patients search by symptom, not clinic name**, so the first screen should say what you treat. Used: a headline about back, shoulder and knee pain, and eight area tiles.
- **A booking form pre-filled from a condition page** reduces friction (a template vendor's claim, not independent evidence). Used: each area tile selects that area in the form.
- **Homepage answers three questions fast:** can you help, are you near, how do I book. Used: the headline, the address bar and a call button in the header.
- **Say what the first visit is like** (a longer assessment, a history, an exam, a plan). Used: four steps and a 60-minute first assessment priced separately.
- **Practical prep:** loose clothing, bring scans. Used in the FAQ.
- The sources are mostly template and clinic pages; they are opinions, not data.

## Design (2026-10-17 rework)

Why the first version failed: a white page with small tiles, no people, no photos in the first screen and nothing that said "this clinic is good". The rework adds the things people pay for: a strong first screen with a photo, **named therapists with portraits and credentials**, real-looking photos of the treatment room and exercise hall, clear price cards, a visible method, a safety notice and a confident booking panel. Typeface: Onest (large, tight headings). Skins: Ocean (default, navy and teal), Ember, Forest, Indigo and Night. There is still no animation or live widget; the only interactive parts are the area tiles and the form. A 3-column row of cards and a dark band alternate with light sections so the page has rhythm.

## How the booking works

- Visits (minutes, prices, what is included), the pack, extras, areas, condition cards, therapists and hours are set at the top of `tools/build_pages.py` (`VISITS`, `PACK`, `EXTRA_PRICES`, `AREAS`, `CONDS`, `THERAPISTS`, `HOURS`, `CAPACITY`).
- Free times are asked from the mock server (`availability`) for the length of the chosen visit (60 minutes for the first assessment, 45 for therapy, 30 for shockwave): half-hour starts, two therapists at the same time, two hours of notice.
- **Demo limitation:** the mock server counts therapists, not each person's calendar, so the therapist choice is only a request. A real system needs one calendar per therapist.
- The request carries visit, area and therapist (`plan`). No payment; a pack of 8 sessions is only on the price list.
- **Health data:** the note field warns patients not to write detailed medical information; the privacy text says so. A real clinic must handle patient data under the GDPR and local health-data rules; get the privacy page reviewed.
- The "see a doctor first" list is a generic safety notice. A physiotherapist or doctor must approve the real wording.

## The request system (mock server, replaceable by a real backend)

- `js/api.js` (`MotusAPI`) is a mock server using `js/config.js`. A request can answer 409 `slot_taken`. References look like `MT-0001`. `mode: "demo"` keeps data in this browser only and sends nothing. See `docs/API.md`. `admin.html` is a demo back office (no login).

## Colour schemes

The five round buttons at the bottom switch the site (`data-skin` on `<html>`): Ocean (default), Ember, Forest, Indigo and Night (dark). The choice is remembered (`motusSkin`) and works as `?skin=ember`.

## Checked (2026-10-17)

- axe-core 4.10.2: no violations on the BG and EN home pages in all five colour schemes (1280 and 375 px), the admin page and the privacy pages.
- No horizontal overflow at 345, 360, 375, 768, 1280 and 1440 px; no requests to other sites (the map loads only after a click).
- Flow tested: the "Shoulder" condition card selected the area and the "Pack of 8" card selected the therapy visit in the form, a request with Elena Stoyanova, a request with reference MT-0001, visible in the demo back office.

## Not done / to do before real use

- Not tested on real phones, Safari or screen readers.
- The "14 yrs" fact and the diplomas are examples and must match the real lead therapist.
- No therapist calendars, reminders, exercise videos, online intake forms or payment for packs. No patient reviews: none are real, so none are shown; a real clinic should add real ones with consent.
- Prices, therapists and their experience are placeholders. Avoid claims about treatment results unless the clinic can support them.
- Photos are free Unsplash placeholders (`images/CREDITS.md`); replace them with photos of the real clinic. Replace texts, address, phone, email and hours. Privacy page: fill in the yellow fields.
- Add canonical/hreflang and `og:image` when the domain is known (comment in the page head).
