# Lapa Vet – veterinary design 1 (a friendly neighbourhood clinic)

Status (2026-10-17): **built.** A website for a **veterinary clinic for dogs and cats** designed to look like a **doctor's practice**, so that an owner feels safe: a top bar with today's hours and the night emergency number, **two named vets with portraits and credentials**, a trust bar, an emergency box, prices in groups, **what the clinic has on site** (operating room, lab, ultrasound), a calm first-visit section and an **appointment form**. **Made-up content** ("Lapa Vet", Plovdiv). Bulgarian (`/`) and English (`/en/`).

**Everything about the clinic is an example**: name, vets, prices, hours, address, phones (including the "24-hour clinic" number). The vet portraits are stock photos of people in scrubs (placeholders), and the diplomas and registration numbers are invented. A real clinic must use its own vets, their real photos (with consent) and real credentials. Replace all of it.

## Research behind the design (2026-10-17)

Vet-website guides (1 Digital Agency, Vetstoria, BeoHosting, Emulent, Freshysites, Lucid Crew, Vet Marketing Services) agree on:

- **Hours and emergency information up front.** Owners cannot tell within seconds whether the clinic is open. Used: today's hours in a bar under the first screen, and an "An emergency?" box with the clinic phone and the number of a 24-hour clinic.
- **A clear emergency policy.** A clinic that is not open 24/7 should say so and name a referral. Used: the box says "we are not a 24-hour clinic" and names the referral; the FAQ repeats it.
- **Booking that is easy to reach.** Used: a "Book" button in the first screen and the navigation, and one short form.
- **Services stated plainly: species, services, prices.** Used: a price list with minutes, and a species choice in the form.
- **Real staff, bios and credentials build trust** over stock imagery. Used: two vet cards with a portrait, experience and three credentials each (all examples). Real photos must replace the stock ones.
- The sources are agency and vendor blogs with a commercial interest; no pet-owner survey data was found. They are opinions, not data.

## Why it looks like a doctor's website (2026-10-17 rework)

The first version looked playful (round, mint, rounded font) and the owner asked for something trustworthy, like a doctor's site. The rework follows the usual medical-site pattern: white and calm, serif headings (Alegreya), square-ish corners, a trust bar (experience, equipment, price before treatment, written summary), the vets first with their qualifications, facts a worried owner needs (consent before procedures, sterile instruments, cats and dogs apart), and the emergency policy shown twice. No cartoon elements.

## What is deliberately plain

No animation, no live widgets, no sticky bars. The only interactive part is the appointment form. The five colour schemes at the bottom are required for every site.

## How the booking works

- Services (minutes and prices), vaccine ages, vets and hours are set at the top of `tools/build_pages.py` (`SERVICES`, `VACC`, `VETS`, `HOURS`, `CAPACITY`, `NIGHT_PHONE`).
- Free times are asked from the mock server (`availability`) for the length of the chosen reason: half-hour starts, two vets at the same time, one hour of notice.
- **Demo limitation:** the mock server counts vets, not each vet's calendar, and the form has no vet choice. A real system needs one calendar per vet and per room (surgery days).
- The request carries species, pet name and reason (`plan`). No payment.
- The vaccination guide is only a rough guide; the vet must confirm the schedule and the local rules (for example for rabies) before it is published.

## The request system (mock server, replaceable by a real backend)

- `js/api.js` (`LapaAPI`) is a mock server using `js/config.js`. A request can answer 409 `slot_taken`. References look like `LP-0001`. `mode: "demo"` keeps data in this browser only and sends nothing. See `docs/API.md`. `admin.html` is a demo back office (no login).

## Colour schemes

The five round buttons at the bottom switch the site (`data-skin` on `<html>`): Teal (default), Navy, Forest, Burgundy and Night (dark). The choice is remembered (`lapaSkin`) and works as `?skin=navy`.

## Checked (2026-10-17)

- axe-core 4.10.2: no violations on the BG and EN home pages in all five colour schemes (1280 and 375 px), the admin page and the privacy pages.
- No horizontal overflow at 345, 360, 375, 768, 1280 and 1440 px (the price tables fit a phone); no requests to other sites (the map loads only after a click).
- Flow tested: an ultrasound scan for the dog "Рекс", a request with reference LP-0001, visible in the demo back office.

## Not done / to do before real use

- Not tested on real phones, Safari or screen readers.
- No per-vet calendars, reminders, online new-client forms or consent forms; no online pharmacy.
- The vets, diplomas, registration numbers, prices, vaccine ages and the 24-hour clinic number are examples. The claims in the trust bar and on "Clean and sterile" (single-use needles, a lab, ultrasound, separate waiting for cats) must be true for the real clinic or be removed. Check any wording about treatments and vaccines with a vet.
- Photos are free Unsplash placeholders (`images/CREDITS.md`); replace them with photos of the real clinic and staff. Replace texts, address, phone, email and hours. Privacy page: fill in the yellow fields and get it reviewed.
- Add canonical/hreflang and `og:image` when the domain is known (comment in the page head).
