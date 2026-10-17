# Request API: how to replace the demo with a real backend

The site never talks to a server by itself. It calls one small object, `MotusAPI` (`js/api.js`).

- **Demo mode (today):** `MotusAPI` is a *mock server* that runs in the browser. It validates requests, checks
  availability, gives out reference numbers and keeps the list in `localStorage`. Nothing leaves the visitor's device.
- **Live mode (later):** the same five calls become real HTTP requests to your backend. **The pages do not change.**

## Switching to a real backend

1. Build the endpoints below (any language / framework / database).
2. In `tools/build_pages.py` set `MODE = 'live'` and `API_BASE = 'https://your-domain/api'`, then run
   `python tools/build_pages.py` (it rewrites `js/config.js`). Or edit `js/config.js` by hand.
3. In live mode the "Demo mode" notices and the demo buttons disappear by themselves.
4. Replace `admin.html` with a real back office behind a login (the demo page calls the same endpoints
   `GET /requests`, `PATCH /requests/:id`, `DELETE /requests/:id`, but must never be public).
5. Update the privacy notice (the yellow text in the "When you contact us" paragraph) and the contact wording on the
   confirmation ("We will contact you by phone...") to match what really happens.

If the API is on another domain, enable **CORS** for the site's address.

## Settings (`js/config.js`)

| Key | Meaning |
|---|---|
| `mode` | `"demo"` or `"live"` |
| `apiBase` | base address of the API, no trailing slash |
| `hours` | opening and closing time, weekdays and weekends (used by the demo server and for the default time list) |
| `capacity` | therapists working at the same time (2) |
| `slotMinutes` | gap between start times in minutes (30) |
| `leadMinutes` | notice a same-day appointment needs in minutes (120). The demo offers no time earlier than now + this |

In a real system **opening hours, capacity and availability belong to the server**; the page only displays what it returns.

## Endpoints

All bodies are JSON (`Content-Type: application/json`). Errors use the shape
`{ "error": { "code": "slot_taken", "message": "..." } }` with the HTTP status shown.

### `GET /availability?date=YYYY-MM-DD&duration=MINUTES`

Free start times for a visit of `duration` minutes on that day. Return an empty `slots` list when closed or full.

```json
{ "date": "2026-10-24", "open": "10:00", "close": "18:00", "duration": 70,
  "slots": ["10:00", "10:30", "13:00"] }
```

Rule used by the demo (copy it): a start time `s` is free if `s + duration <= close` and fewer than `capacity` existing
requests with status `pending` or `confirmed` overlap `[s, s + duration)`. **Declined requests do not block time.**

### `POST /requests`

Creates a request with status `pending`. Request body:

```json
{
  "name": "Elena Koleva",
  "phone": "+359 888 123 456",
  "service": "First assessment",
  "plan": { "summary": "First assessment - Knee - Elena Stoyanova", "visit": "first", "area": "knee", "therapist": "stoyanova" },
  "date": "2026-10-24",
  "time": "09:00",
  "fulfil": "pickup",
  "durationMinutes": 60,
  "message": "",
  "lang": "en"
}
```

`plan` may be `null`. The fields `address`, `card` and `look` are not used on this site. Success, `201`:

```json
{ "id": "MT-0042", "status": "pending", "createdAt": "2026-10-16T08:27:11.000Z" }
```

Errors the page already handles:

| Status | `code` | When | What the visitor sees |
|---|---|---|---|
| 409 | `slot_taken` | the time is no longer free (someone else booked it) | "Sorry, that time was just taken", and the time list refreshes |
| 422 | `invalid` | a required field is missing, the date is in the past, bad format | "Please check the form and try again" |
| anything else | any | server problem | "Something went wrong. Please try again or call us." |

**Always re-check availability inside the same database transaction as the insert** (to avoid two people getting the same slot).

### Back office endpoints (need login, never public)

| Call | Purpose |
|---|---|
| `GET /requests` | list requests, newest or by date |
| `PATCH /requests/:id` with `{ "status": "confirmed" }` | change status: `pending`, `confirmed`, `declined` |
| `DELETE /requests/:id` | delete a request |

## Suggested database table

```sql
CREATE TABLE requests (
  id            VARCHAR(12) PRIMARY KEY,           -- MT-0042
  created_at    TIMESTAMP NOT NULL DEFAULT now(),
  status        VARCHAR(12) NOT NULL DEFAULT 'pending',  -- pending | confirmed | declined
  name          VARCHAR(120) NOT NULL,
  phone         VARCHAR(40)  NOT NULL,
  service       VARCHAR(160) NOT NULL,
  plan          JSON,                              -- summary and the details of this site (see the example above)
  visit_date    DATE NOT NULL,
  start_time    TIME NOT NULL,
  duration_min  INTEGER NOT NULL,
  fulfil        VARCHAR(10) NOT NULL DEFAULT 'pickup',  -- always pickup on this site
  address       TEXT,                              -- not used on this site
  card_text     TEXT,                              -- not used on this site
  look_url      TEXT,
  look_alt      TEXT,
  message       TEXT,
  lang          VARCHAR(2)
);
CREATE INDEX requests_day ON requests (visit_date, start_time);
```

## Things a real system needs that the demo does not do

- **Notifications:** email (and/or SMS or Viber) to the salon when a request arrives, and a message to the client when it is confirmed or declined. Add reminders before the visit.
- **Login** for the back office, and rate limiting / spam protection on `POST /requests` (for example a honeypot field or a captcha that respects privacy).
- **Validation** on the server (the demo repeats the checks, but a browser can be tampered with).
- **Time zones:** keep dates and times as salon local time.
- **Privacy (GDPR):** the request holds personal data. Update the privacy notice (what is stored, where, who can see it, how long), delete old requests on a schedule, sign a data processing agreement with the host, and keep the back office behind a login.
- **Payment / deposit:** not included; would be a separate step with a payment provider.
- **Backups.**

## Where things live in the code

| File | Role |
|---|---|
| `js/config.js` | settings (generated) |
| `js/api.js` | `MotusAPI`: demo (mock server) and live (fetch) implementations |
| `js/main.js` | the page: time list, planner, form, confirmation |
| `js/admin.js`, `admin.html` | demo back office |
