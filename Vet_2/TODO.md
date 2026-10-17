# VetDoma – veterinary design 2 (a vet who visits at home)

Status (2026-10-17): **built.** A website for a **licensed vet who comes to the animal's home**, designed to look like a **doctor's practice** so that the owner feels safe: a top bar, **two named vets with portraits and credentials**, a dark trust band, who a home visit is for, **what the vet brings**, how it works, a **price made of the visit plus the travel for the area**, and a request form with an **address and a live estimate**. in Plovdiv and the area: who a home visit is for, how it works in three steps, a **price made of the visit plus the travel for the area**, and a request form with an **address and a live estimate**. **Made-up content** ("VetDoma", Plovdiv). Bulgarian (`/`) and English (`/en/`). (The first version was a plain, sandy design that the owner found untrustworthy; this rework uses a medical look: white and green, Source Sans, credentials first.) It does a different job from `Vet_1` (the animal comes to a clinic): here the vet goes to the animal, so the form takes an address and the price includes travel.

**Everything about the practice is an example**: name, prices, travel zones, hours, phones (including the "24-hour clinic" number). The vet portraits are stock photos of people (placeholders); the diplomas, registration numbers and insurance line are invented. A real vet must use real photos (with consent) and real credentials.

## Research behind the design (2026-10-17)

The same vet-website guides as for `Vet_1` (1 Digital Agency, Vetstoria, BeoHosting, Emulent, Freshysites) were used, plus common sense for a mobile service:

- **A big, visible phone number and clear emergency policy.** Used: the phone number is the largest text in the first screen; a bar says "we are not 24 hours" and the 24-hour clinic is in the contact block and the FAQ.
- **Say who the service is for.** Used: four short cards (older animals, nervous animals, several animals, owners without a car).
- **Show prices plainly.** Used: a travel table by area and a visit list, and a one-line estimate in the form ("Travel €25 + visit €40 = from €65").
- **Say what cannot be done at home** (ultrasound, X-rays, surgery). Used: an FAQ answer.
- The sources are agency and vendor blogs with a commercial interest. They are opinions, not data.

## What is deliberately plain

No animation, no live widgets, no sticky bars. Source Sans, white and green, square-ish corners, a dark trust band. The only interactive part is the request form. The five colour schemes at the bottom are required for every site.

## How the request works

- Services (minutes and prices), travel zones (fee per zone), hours and the lead time are set at the top of `tools/build_pages.py` (`SERVICES`, `ZONES`, `HOURS`, `CAPACITY`, `LEAD_MINUTES`, `NIGHT_PHONE`).
- Estimate = the travel fee of the chosen area + the price of the chosen reason. Reasons marked "from" (and "something else") say that the exact sum is confirmed by phone. A "choose" link in the travel table picks the area in the form.
- Free times come from the mock server (`availability`) for the length of the reason: half-hour starts, two vets on the road, three hours of notice.
- The request has `fulfil: "delivery"` and an **address** (required); `plan` carries species, pet, reason, area and the estimate.
- **Demo limitation:** the mock server counts vets, not routes. A real system needs a map or a route plan, so that two visits at the same time are not 20 km apart. The area is chosen by the owner and the vet checks it.
- "Saying goodbye at home" (euthanasia) is on the list because it is a common home-visit request; the wording must be written by the vet.

## The request system (mock server, replaceable by a real backend)

- `js/api.js` (`VetDomaAPI`) is a mock server using `js/config.js`. A request can answer 409 `slot_taken`. References look like `VD-0001`. `mode: "demo"` keeps data in this browser only and sends nothing. See `docs/API.md`. `admin.html` is a demo back office (no login) that shows the address.

## Colour schemes

The five round buttons at the bottom switch the site (`data-skin` on `<html>`): Forest (default), Navy, Copper, Plum and Night (dark). The choice is remembered (`vetdomaSkin`) and works as `?skin=navy`.

## Checked (2026-10-17)

- axe-core 4.10.2: no violations on the BG and EN home pages in all five colour schemes (1280 and 375 px), the admin page and the privacy pages.
- No horizontal overflow at 345, 360, 375, 768, 1280 and 1440 px; no requests to other sites (the map loads only after a click).
- Flow tested: a dog, "Senior animal check-up", area up to 25 km: estimate "€90" (travel €40 + visit €50), address entered, a request with reference VD-0001, visible in the demo back office.

## Not done / to do before real use

- Not tested on real phones, Safari or screen readers.
- No route planning, no live location, no payment and no reminders.
- The credentials, the "licensed and insured" claims and the contents of the mobile kit are examples and must be true for the real vet.
- The travel zones, villages and prices are examples; a real vet must set them from fuel, time and the area covered.
- The home address is personal data: the privacy page says so, but a lawyer must review it, and the real back office needs a login and access rules.
- Photos are free Unsplash placeholders (`images/CREDITS.md`). Replace texts, address, phone, email and hours. Privacy page: fill in the yellow fields.
- Add canonical/hreflang and `og:image` when the domain is known (comment in the page head).
