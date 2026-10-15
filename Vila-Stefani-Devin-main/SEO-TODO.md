# SEO / AI-search fixes still to do – Vila Stefani

Google says there is no special "AI optimization": appearing in AI Overviews and AI Mode takes the same
fundamentals as normal search (the page must be indexed and eligible to show with a snippet).
Source: <https://developers.google.com/search/docs/appearance/ai-features>

Nothing here guarantees a place in AI answers. These four items are the gaps found in the current site.

**Blocked until known:** the real site address (needed for hreflang, canonical, sitemap), the real photos,
and the facts from the owner (for the FAQ).

---

## 1. A real English version  (biggest gap)

**Problem.** The English text only appears when a visitor presses the language button. Both languages share
one address, and the English is injected by JavaScript. Google only sees the Bulgarian page, so someone
searching in English will not find the English text.

**Fix.** Separate pages per language, linked with `hreflang`.

- [ ] Create a static English page, e.g. `en/index.html`, with the English text written in the HTML
      (not injected by `js/i18n.js`). Keep `index.html` as the Bulgarian page.
- [ ] Set `<html lang="en">`, an English `<title>`, meta description and Open Graph tags on the English page.
- [ ] Add `hreflang` tags on **both** pages, using full addresses once the domain is known:
      `bg`, `en` and `x-default` (for example `x-default` pointing at the Bulgarian page).
- [ ] Add a self-referencing `<link rel="canonical">` on each page.
- [ ] Turn the language button into a normal link between the two pages (keep the flag styling).
      Do not redirect visitors automatically based on browser language; let them choose.
- [ ] Do the same for the privacy page (`en/privacy.html`).
- [ ] Make the "Nearby" cards and the reviews present in the HTML of each language (today they are built by
      `js/main.js` from `js/data.js`); either pre-render them or generate each language page from the data.
- [ ] Add both pages to `sitemap.xml`, with `xhtml:link` alternates.
- [ ] Update structured data (`LodgingBusiness`) on the English page (name, description, `inLanguage`).
- [ ] After launch: in Google Search Console, submit the sitemap and use URL Inspection on both pages.

**Check.** View source on the English page and confirm the English headings and paragraphs are in the raw HTML.

---

## 2. Questions guests actually ask (FAQ)

**Why.** Clear, direct answers help visitors and are easy for search and AI answers to quote.

**Do not invent facts.** The owner must provide every answer. Ask them:

- [ ] Parking: is there any, free or paid, how many cars, is the road narrow or steep?
- [ ] Check-in and check-out times; is late arrival possible?
- [ ] Pets allowed?
- [ ] How to get there from Devin and from the main road; public transport; winter road conditions.
- [ ] How many guests does the room take; extra bed or cot; children?
- [ ] Breakfast: not offered, or available nearby (shop, bakery, restaurant)?
- [ ] Wi-Fi, heating, air conditioning, towels and linens, hairdryer.
- [ ] Payment methods, deposit, cancellation rules, minimum stay.
- [ ] Smoking policy, quiet hours.
- [ ] Languages the host speaks.
- [ ] Nearest ATM, pharmacy, supermarket; distances.
- [ ] Best seasons, and what is open in winter.

**Build.**

- [ ] Add a visible FAQ section (collapsible questions, plain text answers) in both languages.
- [ ] Keep each answer short and factual (1–3 sentences), with the question as a real heading or button label.
- [ ] Optional: FAQ structured data is not needed. Google limits FAQ rich results, so the visible text is what matters.
- [ ] Any structured data added (price range, amenities, check-in times) must match the visible text exactly.

---

## 3. Image alt text

**Current state.** Photo `alt` attributes are intentionally empty (`alt=""`) because each picture already has a
visible caption, and a screen reader would otherwise read it twice. The lightbox uses the caption as its text.
That is fine for accessibility but wastes search value once real photos are in.

- [ ] When the real photos arrive, write a short descriptive `alt` for the **key** photos in both languages
      (view, room, balcony, kitchen, yard). Describe what is shown, e.g.
      "Room with a double bed and a balcony facing the mountain", not "photo 1".
- [ ] Keep `alt=""` only for purely decorative images.
- [ ] Do not repeat the caption word for word; add information the caption does not give.
- [ ] Use descriptive file names: `staya-s-balkon.jpg`, not `IMG_4821.jpg`.
- [ ] Alt text for each language page (the English page gets English alt text).
- [ ] Alt text for `og.jpg` is not needed, but it must be a good 1200×630 picture.

---

## 4. Photo speed

**Why.** Slow pages hurt search and visitors. Core Web Vitals targets: LCP under 2.5 s, CLS under 0.1,
INP under 200 ms.

- [ ] Resize before upload: about 1600 px on the long side for the hero and gallery, smaller for cards.
- [ ] Compress: aim for about **150–300 KB** per photo (hero up to ~300 KB) and well under ~2 MB in total for the first screen.
      Tools: squoosh.app, or `sharp` / ImageMagick in a script.
- [ ] Offer modern formats (WebP or AVIF) with a JPEG fallback using `<picture>`, plus `srcset`/`sizes`
      so phones download smaller files.
- [ ] Add `width` and `height` to every `<img>` so the layout does not jump while images load.
- [ ] **Hero image:** today `js/main.js` probes `images/hero.jpg` and applies it after load. That delays the
      largest picture on the page. When the real photo is added, load it directly (a real `<img>` with
      `fetchpriority="high"`, or a `<link rel="preload">`) and drop the JavaScript probe.
- [ ] Keep `loading="lazy"` on all below-the-fold images (already in place) and do not lazy-load the hero.
- [ ] After launch, run PageSpeed Insights / Lighthouse on mobile for both pages and fix what it reports.

---

## Also (small, same theme)

- [ ] Verify the site in Google Search Console and submit the sitemap once the address is known.
- [ ] Link the Google Business Profile to the site and keep phone, address and hours identical everywhere.
- [ ] Replace the placeholders (`YOUR-DOMAIN`, phone, email) before relying on structured data.
- [ ] Do not add `llms.txt` or other special AI files; Google says new machine-readable files are not needed.
