# Linden House – a second guest house design (Vila_2)

Status (2026-10-16): **built.** A guest house website in a **different design** from `Vila-Stefani-Devin-main`, with **different, made-up content**:
a fictional guest house ("Linden House" / "Къща Липа") in the mountains, its own rooms, prices, places, reviews and photos. Bulgarian (`/`) and English (`/en/`).
The original `Vila-Stefani-Devin-main` was not changed and none of its texts, data, images or code were reused.

**Everything about the house is an example**: name, rooms, sizes, prices, distances, reviews, rating, rules and the address. Replace it for a real guest house.

---

## What is different from the original Vila site

| Area | Vila Stefani (original) | Linden House (this one) |
|---|---|---|
| Navigation | top bar with a menu | **fixed side bar** on wide screens with numbered sections and the current section highlighted; slim top bar and slide-in menu on small screens |
| Type | Cormorant Garamond and Source Sans | **Playfair Display** (with italic accent words) and Onest |
| Colours | warm brown and terracotta, dark nearby band | **forest green, linen and clay** |
| First screen | one hero | headline with a framed photo and a "postcard" (check-in and check-out), and a **date and guests search** right under it |
| Rooms | one room section | **three rooms**, one large row each, with size, guests, bed, amenities and a "Book this room" button |
| Booking | form hidden for now | **enquiry form with live availability**: pick dates, see which rooms are free, see the total, send an enquiry, get a reference number |
| Nearby | cards that open | **distance ladder**: a bar per place, filter by "on foot" or "by car" |
| Extra content | – | **A day here** (morning, afternoon, evening), **Summer / Winter** switch, rating with one review at a time |
| Gallery | grid | **mosaic** with captions in the viewer |
| Back office | none | **demo back office** (`admin.html`) listing enquiries with dates, nights, room and total |

## The enquiry system (mock server, replaceable by a real backend)

- `js/api.js` (`LindenAPI`) is a mock server. It knows the rooms from `js/config.js`, answers `availability(checkin, checkout, guests)` with each room free, taken or too small,
  and creates enquiries with reference numbers `LN-0001`.
- A stay occupies the **nights** from check-in up to (not including) check-out, so a guest can arrive the day another leaves. Declined enquiries free the room again.
- Rules: arrival not in the past, departure after arrival, at most `MAX_NIGHTS` (30), guests not more than the room sleeps, and a room cannot be double-booked
  (HTTP 409 `room_taken`). Dates and totals are estimates at the example prices; the page says the final price is confirmed by the host.
- In demo mode enquiries live in the visitor's browser and **nothing is sent to anyone**. See `docs/API.md` for the endpoints and the SQL table needed to go live.

## Photos

19 free Unsplash photos (Unsplash License). Only photos marked **Free** were used. They are **placeholders**; see `images/CREDITS.md` for the photographers and links
(photographer names come from the search listings, so check the links before publishing real credits). Photos of other people's houses must be replaced with the real house.

## Font

**Playfair Display** and **Onest**, self-hosted in `fonts/` (the same files as in `Flower_Shop_2`; the Playfair download was approved earlier). No requests to Google.

## How it is built

- Static files. `python tools/build_pages.py` writes `index.html`, `en/index.html` and `js/config.js`; `python tools/build_privacy.py` writes the privacy pages.
  Data at the top of `build_pages.py`: `ROOMS`, `ROOM_TEXT`, `DAY`, `SEASONS`, `PLACES`, `GALLERY`, `REVIEWS`, times, contact placeholders; texts of both languages in `L`.
- The map loads only after a click (OpenStreetMap). No cookies, no analytics, no third-party requests; so no cookie banner is needed.

**Verified (2026-10-16):** main page (BG and EN) including the error state, the photo viewer, seasons, the distance filter and the review slider; the back office; both privacy
pages. All pass axe (WCAG 2.2 AA + best practice). Full enquiry with real values (LN-0001); a taken room shows "Taken" for overlapping dates but is free for back-to-back stays;
a second enquiry for a taken room is refused (409). 390 px layout without horizontal scroll (a date field overflowing its cell was fixed); no outside requests.
**Not tested:** real phones, Safari (uses `<dialog>` and `:has()`), screen readers.

## Before using for a real guest house

- [ ] Replace name, address, phone, email, rooms (sizes, beds, prices, amenities), breakfast price, FAQ answers, house rules and check-in times.
- [ ] Replace the places and times in "Around" with real ones (the page says they are examples).
- [ ] Replace all photos and their `alt` texts/captions; remove the example rating and reviews (or use real guest reviews with permission).
- [ ] Fill the yellow fields in the privacy notices, then remove `noindex`. If guests give ID details later, the notice must cover that.
- [ ] Real domain: canonical and hreflang links, `og:image`, sitemap.
- [ ] Decide how enquiries reach the host: in demo mode they do not. Connect a backend (`MODE = 'live'`, `docs/API.md`) with email notification to the host and the guest.
- [ ] Consider seasonal prices, minimum nights on weekends, a deposit and an iCal feed so the calendar matches Booking.com or Airbnb.

## Ideas not built yet

| # | Idea | Why |
|---|---|---|
| 1 | **Seasonal prices and minimum stay** | Weekends and holidays are priced differently |
| 2 | **iCal import and export** | Stops double bookings with Booking.com and Airbnb |
| 3 | **Automatic emails** (confirmation, reminder before arrival, thank you) | Fewer calls, better reviews |
| 4 | **Add-ons in the form** (breakfast, extra bed, airport pickup) | More income per stay |
| 5 | **Guest book / review button** | Reviews drive Google Maps ranking |
