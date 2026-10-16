# Blue Heron – a fourth guest house design (Vila_4)

Status (2026-10-16): **built.** A guest house website in a **fourth design**, with **new made-up content**: a fictional lake-shore guest house ("Blue Heron" / "Синя чапла").
Bulgarian (`/`) and English (`/en/`). The other guest house sites were not changed.

**Everything about the house is an example**: name, places to sleep, sizes, prices, routes, guest notes and the address. Replace it for a real guest house.

## What is different

- **Look**: bright and playful. Lake blue, sky, sand and coral; Nunito; a blob-shaped hero photo and a wave divider; rounded cards.
- **Navigation**: a floating logo and language flag, and a **dock at the bottom** that highlights the section you are in.
- **The grounds**: an **illustrated map** with numbered hotspots. Press one (or a chip under the map) and the panel shows a photo and text.
- **Rooms**: four cards with a "Book this room" button that pre-selects the room and the next Friday for two nights.
- **Booking**: a **timeline**, one row per place and one column per night (28 days, move by two weeks). Press the arrival night, then the departure day.
  Striped nights are taken; a taken day can still be a departure morning; a place too small for the chosen guests is dimmed; a range with a booked night inside is refused.
- **Plan your days**: tabs for three kinds of guest (quiet, active, family) with a short day plan each.
- **Guest notes** as chat bubbles; **sunrise and sunset** for today, calculated in the browser (no request).

## The enquiry system (mock server, replaceable by a real backend)

- `js/api.js` (`LakeAPI`) is a mock server using `js/config.js`. `timeline(from, to)` returns the taken nights per place; `availability`, `createEnquiry` (409 `room_taken`), list/status/remove for the demo back office. References look like `BH-0001`.
- Stays occupy nights from arrival up to, not including, departure; declined enquiries free the place.
- `mode: "demo"` keeps data in this browser only and sends nothing. See `docs/API.md` for the real endpoints.
- `admin.html` is a demo back office (no login). A real one needs a login.

## Checked (2026-10-16)

- axe-core 4.10.2: no violations on the BG and EN home pages (including the form error state and the open tab), the admin page and the privacy page.
- No horizontal overflow at 375 px; no requests to other sites (the map loads only after a click).
- Flow tested: timeline selection, back-to-back stays, blocked range, booking, the new stay appearing as taken.

## Not done / to do before real use

- Not tested on real phones, Safari or screen readers. The timeline is a grid of buttons with labels; check it with real assistive technology.
- Replace photos (see `images/CREDITS.md`; photographer pairs should be re-checked), texts, prices, address, phone, email and the map position.
- Privacy page and legal details are templates with yellow placeholders; get them reviewed.
- Add canonical/hreflang links and `og:image` when the domain is known (comment in the page head).
