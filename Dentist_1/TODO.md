# Dent Plus – dentist design 1 (a calm clinic)

Status (2026-10-17): **built.** A plain website for a **dental clinic**: a price list, two doctor profiles, what happens at the first visit, a few photos of the clinic, a short FAQ and an **appointment form** where the free times fit the length of the chosen treatment. **Made-up content** ("Dent Plus", Plovdiv). Bulgarian (`/`) and English (`/en/`).

**Everything about the clinic is an example**: name, doctors, prices, services, hours, address and phone. The doctor photos are stock portraits and the names are invented. Replace all of it for a real clinic.

## Research behind the design (2026-10-17)

Dental-website guides (DentistryIQ, Priority Pixels, BeoHosting, Azuro Digital, SchedulingKit, Software Pundit) agree on:

- **Show prices or price ranges**; hiding them erodes trust and causes price-check calls. Used: a price list with "from" prices and the length of each treatment, and a note on payment and instalments.
- **Online booking is expected.** Recommended fields: service, dentist, date and time, contact details and a notes field. Used: all of them, plus a new/returning patient choice (new patients need different time blocks).
- **Doctor profiles with photos and experience** build trust. Used: two profiles. Real credentials and registration numbers must be added.
- **Plain-language treatment information and a "first visit" page.** Used: a four-step first-visit section and a short FAQ ("Does it hurt?").
- **Automatic confirmations and reminders** reduce no-shows. Not built here (needs a real backend).
- The sources are agency and vendor articles; some figures are unverified. They are opinions, not data.

## What is deliberately plain

No animation, no live widgets, no sticky bars. A light split first screen (text and a photo), rounded corners and Source Sans for headings and text. The only interactive part is the appointment form. The five colour schemes at the bottom are required for every site.

## How the booking works

- Services (with minutes and prices), doctors and hours are set at the top of `tools/build_pages.py` (`SERVICES`, `DOCTORS`, `HOURS`, `CAPACITY`).
- Free times are asked from the mock server (`availability`) for the length of the chosen service: half-hour starts, three chairs at the same time, two hours of notice for a same-day visit. Changing the service refreshes the times.
- **Demo limitation:** the mock server counts chairs, not each doctor's calendar, so the doctor choice is only a request. A real system needs one calendar per doctor.
- The request carries the patient type, service and doctor (`plan`). No payment.
- **Health data:** the note field warns the patient not to write detailed medical information, and the privacy text says so. A real clinic must handle patient data under the GDPR and local health-data rules; get the privacy page and any intake form reviewed by a lawyer.

## The request system (mock server, replaceable by a real backend)

- `js/api.js` (`DentAPI`) is a mock server using `js/config.js`. A request can answer 409 `slot_taken`. References look like `DP-0001`. `mode: "demo"` keeps data in this browser only and sends nothing. See `docs/API.md`. `admin.html` is a demo back office (no login).

## Colour schemes

The five round buttons at the bottom switch the site (`data-skin` on `<html>`): Teal (default), Blue, Green, Coral and Night (dark). The choice is remembered (`dentSkin`) and works as `?skin=blue`.

## Checked (2026-10-17)

- axe-core 4.10.2: no violations on the BG and EN home pages in all five colour schemes (1280 and 375 px), the admin page and the privacy pages.
- No horizontal overflow at 360, 375, 768, 1280 and 1440 px; no requests to other sites (the map loads only after a click).
- Flow tested: a root canal with Dr. Ivanov (60 minutes), a request with reference DP-0001, visible in the demo back office.

## Not done / to do before real use

- Not tested on real phones, Safari or screen readers.
- No doctor calendars, reminders, online intake forms or X-ray upload.
- Doctors, their experience and photos are placeholders; use real, consented photos and real credentials. Prices are examples and must match the clinic's list and VAT status.
- Medical claims ("no pain", "painless") must be avoided or checked against local advertising rules for health services.
- Photos are free Unsplash placeholders (`images/CREDITS.md`). Replace texts, address, phone, email and hours. Privacy page: fill in the yellow fields and get it reviewed.
- Add canonical/hreflang and `og:image` when the domain is known (comment in the page head).
