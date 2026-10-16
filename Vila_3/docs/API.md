# Enquiry API: how to replace the demo with a real backend

The site never talks to a server by itself. It calls one small object, `CellarAPI` (`js/api.js`).

- **Demo mode (today):** `CellarAPI` is a *mock server* that runs in the browser. It checks which rooms are free for the dates, validates enquiries, gives out reference
  numbers (`SC-0001`) and keeps the list in `localStorage`. Nothing leaves the visitor's device.
- **Live mode (later):** the same calls become real HTTP requests to your backend. **The pages do not change.**

## Switching to a real backend

1. Build the endpoints below (any language, framework and database).
2. In `tools/build_pages.py` set `MODE = 'live'` and `API_BASE = 'https://your-domain/api'`, then run `python tools/build_pages.py` (it rewrites `js/config.js`).
3. Replace `admin.html` with a real back office behind a login (the demo page uses `GET /enquiries`, `PATCH /enquiries/:id`, `DELETE /enquiries/:id`; never make it public).
4. Update the privacy notice (the yellow text in "When you contact us") and the confirmation text to match what really happens.

If the API is on another domain, enable **CORS** for the site's address.

## Settings (`js/config.js`)

| Key | Meaning |
|---|---|
| `mode` | `"demo"` or `"live"` |
| `apiBase` | base address of the API, no trailing slash |
| `rooms` | `[{ id, guests, price }]`: the rooms, how many guests each sleeps and the price per night in EUR |
| `maxNights` | longest stay accepted (30) |

In a real system rooms, prices and availability belong to the server; the page only shows what it returns.

## Endpoints

JSON everywhere. Errors use `{ "error": { "code": "room_taken", "message": "..." } }` with the HTTP status shown. Dates are `YYYY-MM-DD`.

### `GET /availability?checkin=...&checkout=...&guests=N`

```json
{ "checkin": "2026-11-06", "checkout": "2026-11-09", "nights": 3, "guests": 3,
  "rooms": [ { "id": "orchard", "free": false, "reason": "size",  "price": 65, "total": 195 },
             { "id": "blue",    "free": true,  "reason": "",      "price": 95, "total": 285 } ] }
```

A room is **free** when it sleeps at least `guests` and no `pending` or `confirmed` stay overlaps the nights. A stay occupies the nights from `checkin` up to, **not including**,
`checkout`, so one guest can arrive the day another leaves: overlap means `existing.checkin < checkout && checkin < existing.checkout`. Declined stays do not block.
`reason` is `"size"` (too small) or `"taken"`. `422 invalid` when the dates are missing, in the past, `checkout <= checkin` or longer than the maximum.

### `GET /occupancy?from=YYYY-MM-DD&to=YYYY-MM-DD` (new in this design)

Colours the calendar: for each **night** from `from` up to, not including, `to`, how many places are still free.

```json
{ "from": "2026-11-01", "to": "2026-12-01", "places": 4, "free": { "2026-11-01": 4, "2026-11-02": 2, "2026-11-03": 0 } }
```

`4` = free (a plain day), `1` to `3` = partly booked, `0` = fully booked. A fully booked day can still be a **departure** day.

### `POST /enquiries`

```json
{ "name": "Maria Ivanova", "phone": "+359 888 123 456", "email": "maria@example.com", "room": "blue",
  "checkin": "2026-11-06", "checkout": "2026-11-09", "guests": 3, "message": "Arriving late", "lang": "en" }
```

`201`: `{ "id": "SC-0042", "status": "pending", "createdAt": "..." }`. Errors the page handles: `409 room_taken` (re-check inside the same database transaction as the insert),
`422 invalid`, anything else shows a generic message. The server computes the total from the room price and the number of nights.

### Back office (needs login, never public)

`GET /enquiries`, `PATCH /enquiries/:id` with `{ "status": "confirmed" }` (`pending`, `confirmed`, `declined`), `DELETE /enquiries/:id`.

## Suggested database table

```sql
CREATE TABLE enquiries (
  id         VARCHAR(12) PRIMARY KEY,                 -- SC-0042
  created_at TIMESTAMP NOT NULL DEFAULT now(),
  status     VARCHAR(12) NOT NULL DEFAULT 'pending',  -- pending | confirmed | declined
  name       VARCHAR(120) NOT NULL,
  phone      VARCHAR(40)  NOT NULL,
  email      VARCHAR(160),
  room       VARCHAR(20)  NOT NULL,
  checkin    DATE NOT NULL,
  checkout   DATE NOT NULL,
  nights     INTEGER NOT NULL,
  guests     INTEGER NOT NULL,
  total_eur  INTEGER NOT NULL,
  message    TEXT,
  lang       VARCHAR(2)
);
CREATE INDEX enquiries_room_dates ON enquiries (room, checkin, checkout);
```

## A real system also needs

Email to the host and to the guest (confirmation, reminder), login and spam protection (honeypot or a privacy-friendly captcha), server-side validation, seasonal prices and
minimum stays, an iCal feed to sync other platforms, privacy (GDPR) text covering what is stored and for how long, and backups.
