---
name: local-business-site
description: Build a bilingual (Bulgarian + English) static showcase website for a small local business (barber, nail studio, flower shop, guest house) with a mock-backend request system, demo back office, privacy pages, and an entry on the Master-Web landing page. Use when asked to make a new site, a new design variation, or "one more" of an existing type.
---

# Local business showcase site (Master-Web pattern)

Produces one folder inside `Master-Web/` (e.g. `Vila_5/`, `Barber_shop_3/`). Static HTML/CSS/vanilla JS only. No frameworks, no build tools beyond small Python generators, no third-party requests.

## 0. Before you start

1. Read the closest existing site of the same business type (`Barber_shop*`, `Nail_Salon_*`, `Flower_Shop*`, `Vila_2/3/4`) and copy its structure. Never edit existing sites: variations go in NEW folders.
2. Ask only if blocked (e.g. a font needs downloading and the user hasn't agreed). Otherwise pick sensible defaults and say so.
3. If the user wants "a different design": change layout idea, navigation, type, palette, booking UI AND the made-up content (name, rooms, prices, story). Do not reuse text, data or images from other sites.
4. Content is fictional unless the user gives real data. Flag it as example content everywhere (TODO.md, placeholders in privacy page).

## 1. Folder layout

```
<Folder>/
  index.html            BG (generated)
  en/index.html         EN (generated)
  privacy.html, en/privacy.html
  admin.html            demo back office
  css/style.css
  js/config.js (generated) api.js main.js admin.js
  fonts/fonts.css + *.woff2   self-hosted, latin + cyrillic subsets
  images/stock/*.jpg + *-800.jpg   + images/CREDITS.md
  tools/page_template.html build_pages.py build_privacy.py README.md
  docs/API.md
  TODO.md
```

## 2. Generator pattern

- `tools/page_template.html` uses `[[placeholder]]` tokens (`[[lang]] [[root]] [[brand]] [[nav_links]]` ...). `build_pages.py` holds constants (brand EN/BG, check-in times, lat/lon, MODE `"demo"`), data lists (units/services/prices), and `L['bg']` / `L['en']` dictionaries; it writes both pages and `js/config.js`. `build_privacy.py` writes both privacy pages. Run: `python tools/build_pages.py && python tools/build_privacy.py`.
- BG is the root page (`/`), EN is `/en/`. Language switch is a link with a flag background (dark wash so the label stays readable). Page `<head>`: title, description, og tags, a comment explaining canonical/hreflang to add once the domain is known, JSON-LD for the business type, preload for the font subset.
- Write files with the Write tool, not shell heredocs (apostrophes break quoting).

## 3. Mock backend (the "request system")

`js/api.js` exposes one global (`LakeAPI`, `CellarAPI`, `XxxAPI`) with `mode: "demo" | "live"`.
- **Demo**: state in `localStorage` (keys like `xxx.stays`, `xxx.seq`), fake latency from `config.js`, references with a prefix (`BH-0001`), memory fallback if storage throws.
- **Live**: same methods over `fetch` to `apiBase` (`/api`). Document endpoints in `docs/API.md`.
- Methods: `availability`, `createEnquiry`/`createBooking`, `listEnquiries`, `setStatus` (pending/confirmed/declined), `removeEnquiry`, `resetDemo`, `seedDemo(samples)`.
- Errors carry `{status, code, message}`: **422 `invalid`**, **409 `*_taken`** (race: someone took it), 404 `not_found`.
- Guest houses: a stay occupies nights `[checkin, checkout)`, so back-to-back stays are allowed; declined stays free the room; `guests > capacity` rejected. Calendar/timeline helpers: `occupancy(from,to)` (free count per night) or `timeline(from,to)` (taken nights per place).
- Barbers/nails: per-person availability, server assigns the person, same-day past times blocked. Flowers: lead time, cut-off, delivery address validation.
- UI flow: validate -> busy state -> success card with reference + "demo mode, nothing sent" note + link to the admin page -> "make another".
- `admin.html` + `admin.js`: filter chips, status select, delete, seed/reset buttons, a visible "demo, no login" note. Table collapses to labelled cards under 760px.

## 4. Design rules

- Colour tokens on `:root`; palette switching (barber/flower/nail) via `html[data-skin=...]` variables. All text pairs must pass WCAG AA (the usual failures: coral/terracotta accent on tinted backgrounds, light text on photos, links on sky/sand). Use the deep brand colour for links on tinted sections.
- Fonts: self-host variable fonts with Latin + Cyrillic subsets (Playfair Display, Oswald, Unbounded, Alegreya, Nunito, Onest, Cormorant, Source Sans 3 were used). Download needs the user's OK. No Google Fonts requests.
- Native `<dialog>` for menu/drawer/lightbox, `IntersectionObserver` for reveal + scroll-spy, CSS grid with explicit `grid-area` for timelines/boards, `:has()`, `color-mix()`.
- Motion: all animation inside `@media (prefers-reduced-motion: no-preference)`; reveal class `js-reveal` only added when IO exists and motion is allowed.
- Layout gotchas learned: grid items with `aspect-ratio` + `align-items: stretch` overflow their column (add `align-self:start; width:100%`); `.field{min-width:0}` so date inputs don't overflow on phones; give each page a `[hidden]{display:none!important}`; don't reuse generic class names like `.pill` across header and status chips; decorative text goes in `::before` content, not the DOM; extra banners go in `<aside aria-label>`, never nested asides.
- Map embed: click-to-load OpenStreetMap iframe (`data-src`), nothing loads before the click.
- One distinguishing idea per design, e.g.: side-bar journal (Vila_2), full-screen chapters + calendar + stacking cards (Vila_3), illustrated map + bottom dock + timeline (Vila_4).

## 5. Photos

- Unsplash only (free licence). Download via `https://unsplash.com/photos/<ID>/download?force=true&w=1600`. IDs truncated by a fetch tool will 404: drop those photos.
- Recompress with Pillow: 1600px wide (quality ~80, progressive) plus `-800` variant. Delete unused downloads. Write `images/CREDITS.md` (file, photographer, Unsplash URL) and note that photographer pairings come from search listings and must be rechecked before publishing.
- Hero `<img>` gets `fetchpriority="high"`, `srcset`, width/height; others `loading="lazy"`.

## 6. Verification (do not skip)

Use the browser pane (`preview_start master-web` serves `Master-Web/` on port 5180).
1. Inject `*{animation:none!important;transition:none!important}` and `html{scroll-behavior:auto!important}` before screenshots (animations freeze mid-way otherwise).
2. Stale CSS/JS: `fetch(url,{cache:'reload'})` then `location.reload()`.
3. axe-core 4.10.2 from cdnjs on BG and EN, every skin, plus error / menu / lightbox / done states, admin and privacy pages. Fix all violations.
4. Viewports: 1440x900 and 375x812 (`resize_window` mobile); check `documentElement.scrollWidth === innerWidth`. Reset to desktop afterwards.
5. Functional test with real values: full booking flow, race/taken error, back-to-back logic, status changes in admin. Seed with `API.seedDemo([...])` using dates relative to today; `localStorage.clear()` between runs.
6. Network: `performance.getEntriesByType('resource')` shows no external hosts.
7. Be honest in the report: not tested on real phones, Safari or screen readers; demo mode sends nothing; prices partly estimated; content is example content.

## 7. Register on Master-Web

`Master-Web/index.html` has a tabbed showcase: `.sc-tabs` (`t-guest`, `t-nail`, `t-barber`, `t-flower`), one `.sc-panel` per type, `.seg` design buttons with `data-folder`, `data-admin` (omit for single-page sites), `data-note-key`, `data-note-en`, `aria-label="Design N: Name"`. For a new design:
1. Add a `.seg` button in the right panel; update the tab count `<small data-i18n="sc.N">` and add the BG key (`"sc.four": "4 дизайна"`).
2. Add BG note `"guest.nN"` to the BG dictionary; adjust the type's description/chips if capabilities changed.
3. Add `Folder/` and `Folder/en/` to `sitemap.xml` with hreflang alternates (`https://YOUR-DOMAIN/...`).
4. Verify the panel switches, iframe src updates, axe clean on the Master page.
(See `scratchpad/master_v3.py`-style one-off Python edit scripts: assert each replacement matches exactly once.)

## 8. TODO.md for every site

Status + date; what is different from other designs (table or list); the enquiry system and how to swap to a real backend; what was checked; what is NOT done (real devices, real photos/content, legal review, canonical/hreflang/og:image, login for the back office).

## 9. Final report to the user

Short: what the site is, what makes it different, how the request system behaves, what was verified, caveats, link to TODO.md.
