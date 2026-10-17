"""Builds index.html (Bulgarian), en/index.html (English), js/config.js and css/style.css for Ember Roasters.
Edit the values in this file (coffees, prices, hours, texts), then run:  python tools/build_pages.py && python tools/build_privacy.py
Everything about the roastery is an example: replace it for a real roastery."""
import json, os
from html import escape as esc
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BRAND = 'Ember Roasters'

# ---------------- settings you will change for a real roastery ----------------
HOURS = {'weekday': ['10:00', '18:00'], 'weekend': ['10:00', '14:00']}   # roastery shop: pick-up and delivery windows
CAPACITY = 6          # orders handled in the same time slot
SLOT_MINUTES = 30
LEAD_MINUTES = 120    # a same-day order needs this much notice
SIZES = [('250', 250, 1.0), ('1000', 1000, 3.6)]   # id, grams, price multiplier (1 kg is cheaper per gram)
SUB_DISCOUNT = 0.08   # subscribe and save
DELIVERY_FEE, FREE_DELIVERY_FROM = 4.5, 35
ROAST_DAYS = (1, 4)   # Tuesday and Friday (0 = Sunday)
PHONE, PHONE_HREF, EMAIL = '+359 88 000 0000', '+359880000000', 'beans@example.com'
ADDRESS = {'bg': 'ул. Примерна 21, Пловдив', 'en': '21 Primer St., Plovdiv'}

# id, method (filter / espresso / both), roast 1-5, price for 250 g, photo, (bg name, en name), (bg origin, en origin), (bg notes, en notes), process
COFFEES = [
 ('guji', 'filter', 2, 11.9, 'bowl-beans', ('Етиопия Гуджи', 'Ethiopia Guji'), ('Гуджи, Етиопия · 2000 м', 'Guji, Ethiopia · 2000 m'), (['Праскова', 'Жасмин', 'Мед'], ['Peach', 'Jasmine', 'Honey']), ('Натурална', 'Natural')),
 ('huila', 'both', 3, 10.5, 'beans-trail', ('Колумбия Уила', 'Colombia Huila'), ('Уила, Колумбия · 1800 м', 'Huila, Colombia · 1800 m'), (['Карамел', 'Червена ябълка', 'Какао'], ['Caramel', 'Red apple', 'Cocoa']), ('Измита', 'Washed')),
 ('cerrado', 'espresso', 4, 9.5, 'beans-dark', ('Бразилия Серадо', 'Brazil Cerrado'), ('Серадо, Бразилия · 1100 м', 'Cerrado, Brazil · 1100 m'), (['Лешник', 'Шоколад', 'Бадем'], ['Hazelnut', 'Chocolate', 'Almond']), ('Натурална', 'Natural')),
 ('ember', 'espresso', 4, 8.9, 'steam-cup', ('Смес Ember', 'Ember house blend'), ('Бразилия и Колумбия', 'Brazil and Colombia'), (['Тъмен шоколад', 'Сладък тютюн', 'Цитрус'], ['Dark chocolate', 'Sweet tobacco', 'Citrus']), ('Смес', 'Blend')),
 ('decaf', 'both', 3, 11.2, 'flat-lay', ('Без кофеин Мексико', 'Decaf Mexico'), ('Чиапас, Мексико', 'Chiapas, Mexico'), (['Млечен шоколад', 'Портокал'], ['Milk chocolate', 'Orange']), ('Захарна тръстика', 'Sugarcane process')),
]
GRINDS = [('whole', 'На зърна', 'Whole bean'), ('espresso', 'За еспресо', 'Espresso'), ('moka', 'За мока', 'Moka pot'), ('filter', 'За филтър (V60)', 'Filter (V60)'), ('press', 'За преса', 'French press')]
FREQS = [('once', 'Само веднъж', 'Just once'), ('14', 'На всеки 2 седмици', 'Every 2 weeks'), ('30', 'Всеки месец', 'Every month')]
# brew guide: id, bg, en, ratio (g of water per g of coffee), temperature, time, grind bg, grind en
METHODS = [('v60', 'Филтър V60', 'V60 pour-over', 16, '94 °C', '3:00', 'средно ситно', 'medium-fine'), ('espresso', 'Еспресо', 'Espresso', 2, '93 °C', '0:28', 'ситно', 'fine'),
           ('moka', 'Мока', 'Moka pot', 10, '90 °C', '4:00', 'средно ситно', 'medium-fine'), ('press', 'Френска преса', 'French press', 15, '95 °C', '4:00', 'едро', 'coarse'),
           ('aero', 'AeroPress', 'AeroPress', 14, '85 °C', '2:00', 'средно', 'medium')]

SKINS = [('ember', 'Жарава', 'Ember', '#17110D', '#FF6A2B'), ('paper', 'Хартия', 'Paper', '#F4EEE4', '#C2410C'),
         ('moss', 'Мъх', 'Moss', '#0F1812', '#A6E06A'), ('midnight', 'Полунощ', 'Midnight', '#101522', '#F2C14E'),
         ('blush', 'Руж', 'Blush', '#FBEFF0', '#9D2A5B')]


def dims(name):
    with Image.open(os.path.join(ROOT, 'images', 'stock', name + '.jpg')) as im:
        return im.size


def img(root, name, alt, sizes, cls='', eager=False):
    w, h = dims(name)
    attrs = ' loading="eager" fetchpriority="high"' if eager else ' loading="lazy" decoding="async"'
    c = ' class="%s"' % cls if cls else ''
    u = root + 'images/stock/' + name
    return '<img%s src="%s-800.jpg" srcset="%s-800.jpg 800w, %s.jpg 1600w" sizes="%s" width="%d" height="%d" alt="%s"%s>' % (c, u, u, u, sizes, w, h, esc(alt), attrs)


def build(lang):
    bg = lang == 'bg'
    t = lambda a, b: a if bg else b
    root = '' if bg else '../'
    I = lambda *a, **k: img(root, *a, **k)
    i = 0 if bg else 1
    other_href = 'en/index.html' if bg else '../index.html'
    script = 'cyrillic' if bg else 'latin'

    def money(v):
        return ('%.2f' % v).replace('.', ',' if bg else '.') + ' €'

    meth_label = {'filter': t('Филтър', 'Filter'), 'espresso': t('Еспресо', 'Espresso'), 'both': t('Филтър и еспресо', 'Filter and espresso')}
    cards = []
    for cid, meth, roast, price, photo, nm, org, notes, proc in COFFEES:
        dots = ''.join('<i%s></i>' % (' class="on"' if k < roast else '') for k in range(5))
        nt = ''.join('<li>%s</li>' % esc(n) for n in notes[i])
        cards.append('''<li class="coffee" data-id="%s" data-method="%s">
          <figure>%s<span class="m-tag">%s</span></figure>
          <div class="c-body">
            <h3>%s</h3>
            <p class="c-org">%s · %s</p>
            <ul class="c-notes">%s</ul>
            <p class="roast"><span>%s</span><span class="dots" role="img" aria-label="%s %d/5">%s</span></p>
            <div class="c-foot"><b>%s</b><small>/ 250 г</small><button class="choose" type="button" data-id="%s" aria-pressed="false">%s</button></div>
          </div>
        </li>''' % (cid, meth, I(photo, nm[i], '(min-width: 1180px) 380px, (min-width: 960px) calc((100vw - 84px) / 3), (min-width: 600px) calc(50vw - 31px), calc(100vw - 40px)'), meth_label[meth], esc(nm[i]), esc(org[i]), esc(proc[i]), nt,
                    t('Изпичане', 'Roast'), t('Изпичане', 'Roast level'), roast, dots, money(price).replace(' €', ' €'), cid, t('Избери', 'Choose')))
    cards_html = ''.join(cards)
    chips = ''.join('<button class="chip" type="button" data-method="%s" aria-pressed="%s">%s</button>' % (k, 'true' if k == 'all' else 'false', l)
                    for k, l in (('all', t('Всички', 'All')), ('filter', t('За филтър', 'For filter')), ('espresso', t('За еспресо', 'For espresso'))))
    grind_html = ''.join('<option value="%s">%s</option>' % (k, b if bg else e) for k, b, e in GRINDS)
    size_html = ''.join('<label class="opt"><input type="radio" name="size" value="%s"%s><span><b>%s</b><small class="size-p" data-size="%s"></small></span></label>'
                        % (k, ' checked' if k == '250' else '', ('250 г' if k == '250' else '1 кг') if bg else ('250 g' if k == '250' else '1 kg'), k) for k, g, m in SIZES)
    freq_html = ''.join('<label class="opt"><input type="radio" name="freq" value="%s"%s><span><b>%s</b>%s</span></label>'
                        % (k, ' checked' if k == 'once' else '', b if bg else e, '' if k == 'once' else '<small>%s</small>' % t('−8 %', '−8%')) for k, b, e in FREQS)
    meth_opts = ''.join('<option value="%s">%s</option>' % (m[0], m[1 + i]) for m in METHODS)
    swatches = ''.join('<button class="sw" type="button" data-skin="%s" style="--s1:%s;--s2:%s" aria-pressed="false" aria-label="%s"></button>' % (k, s1, s2, b if bg else e) for k, b, e, s1, s2 in SKINS)
    hours_rows = [(t('Понеделник – петък', 'Monday – Friday'), HOURS['weekday'], 'wd'), (t('Събота и неделя', 'Saturday and Sunday'), HOURS['weekend'], 'we')]
    hours_html = ''.join('<div data-hrs="%s"><dt>%s</dt><dd>%s – %s</dd></div>' % (k, n, h[0], h[1]) for n, h, k in hours_rows)
    hours_ld = '"Mo-Fr %s-%s","Sa-Su %s-%s"' % (HOURS['weekday'][0], HOURS['weekday'][1], HOURS['weekend'][0], HOURS['weekend'][1])
    nav = [('#beans', t('Кафета', 'Coffees')), ('#build', t('Поръчай', 'Order')), ('#brew', t('Приготвяне', 'Brewing')), ('#roastery', t('Пържилнята', 'Roastery')), ('#visit', t('Адрес', 'Visit'))]
    nav_html = ''.join('<a href="%s">%s</a>' % n for n in nav)
    notes_all = [n for c in COFFEES for n in c[7][i]]
    marquee = ''.join('<span>%s</span>' % esc(n) for n in notes_all * 2)

    data = {'coffees': [{'id': c[0], 'method': c[1], 'price': c[3], 'name': c[5][i], 'roast': c[2]} for c in COFFEES],
            'sizes': [{'id': k, 'g': g, 'mult': m} for k, g, m in SIZES], 'grinds': {k: (b if bg else e) for k, b, e in GRINDS}, 'freqs': {k: (b if bg else e) for k, b, e in FREQS},
            'subDiscount': SUB_DISCOUNT, 'fee': DELIVERY_FEE, 'freeFrom': FREE_DELIVERY_FROM, 'roastDays': list(ROAST_DAYS),
            'methods': [{'id': m[0], 'name': m[1 + i], 'ratio': m[3], 'temp': m[4], 'time': m[5], 'grind': m[6 + i]} for m in METHODS]}

    title = t('Ember Roasters – пържилня за кафе в Пловдив. Прясно изпечено кафе до вратата ти', 'Ember Roasters – coffee roasters in Plovdiv. Freshly roasted coffee to your door')
    desc = t('Ember Roasters е малка пържилня за специално кафе в Пловдив. Избери зърна, размер и мелене, а ние ги изпичаме във вторник и петък и ги доставяме или ги вземаш от нас.',
             'Ember Roasters is a small specialty coffee roastery in Plovdiv. Choose beans, size and grind; we roast on Tuesdays and Fridays and deliver, or you collect from us.')

    return '''<!doctype html>
<html lang="%(lang)s" data-skin="ember">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="theme-color" content="#17110D">
<title>%(title)s</title>
<meta name="description" content="%(desc)s">
<meta property="og:type" content="website">
<meta property="og:title" content="%(title)s">
<meta property="og:description" content="%(desc)s">
<meta property="og:locale" content="%(lang)s">
<!-- When the real address is known add, on BOTH language pages:
     <link rel="canonical" href="https://YOUR-DOMAIN/ (or /en/)">
     <link rel="alternate" hreflang="bg" href="https://YOUR-DOMAIN/">
     <link rel="alternate" hreflang="en" href="https://YOUR-DOMAIN/en/">
     <link rel="alternate" hreflang="x-default" href="https://YOUR-DOMAIN/">
     and an og:image (images/stock/roaster-pour.jpg is a placeholder) -->
<link rel="preload" href="%(root)sfonts/onest-%(script)s.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="%(root)sfonts/unbounded-%(script)s.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="%(root)sfonts/fonts.css">
<link rel="stylesheet" href="%(root)scss/style.css">
<script>
  /* Scroll animations only run when the browser supports them and the visitor has not asked for less motion. */
  if ("IntersectionObserver" in window && !matchMedia("(prefers-reduced-motion: reduce)").matches) document.documentElement.classList.add("js-reveal");
</script>
<script>
  /* Apply the saved colour scheme before the page paints, so it does not flash. */
  try { var s = new URLSearchParams(location.search).get("skin") || localStorage.getItem("emberSkin"); if (s) document.documentElement.dataset.skin = s; } catch (e) {}
</script>
<script type="application/ld+json">
{"@context":"https://schema.org","@type":"CafeOrCoffeeShop","name":"%(brand)s","inLanguage":"%(lang)s","telephone":"%(phone_href)s","email":"%(email)s",
 "address":{"@type":"PostalAddress","streetAddress":"Primer St. 21","addressLocality":"Plovdiv","addressCountry":"BG"},
 "servesCuisine":"Coffee","openingHours":[%(hours_ld)s]}
</script>
</head>
<body>
<a class="skip" href="#main">%(skip)s</a>

<header class="top" id="top">
  <div class="top-in">
    <a class="logo" href="index.html"><svg viewBox="0 0 32 32" width="28" height="28" aria-hidden="true" focusable="false"><path d="M16 2c1 5 7 8 7 15a7 7 0 0 1-14 0c0-3 1.5-4.5 3-6 .3 2 1.2 3 2.2 3.4C13.500 9 15 6 16 2z" fill="currentColor"/><ellipse cx="16" cy="22" rx="3.2" ry="4.6" fill="var(--bg)" opacity=".55" transform="rotate(20 16 22)"/></svg><b>%(brand)s</b></a>
    <nav class="nav" id="nav" aria-label="%(nav_label)s">%(nav_html)s</nav>
    <div class="top-r">
      <a class="bag-pill" href="#build" id="bagPill"><span class="bag-n" id="bagN">0</span><span class="bag-t" id="bagT">%(bag_empty)s</span></a>
      <a class="lang" href="%(other_href)s" lang="%(other_lang)s" hreflang="%(other_lang)s" aria-label="%(other_aria)s">%(other_label)s</a>
      <button class="burger" id="burger" type="button" aria-controls="nav" aria-expanded="false" aria-label="%(menu_btn)s"><span></span></button>
    </div>
  </div>
</header>

<main id="main">

  <!-- ============ Hero ============ -->
  <section class="hero" aria-labelledby="h1">
    <div class="wrap hero-in">
      <div class="hero-copy">
        <p class="eyebrow">%(eyebrow)s</p>
        <h1 id="h1">%(h1)s</h1>
        <p class="lead">%(lead)s</p>
        <div class="hero-actions">
          <a class="btn btn-main" href="#beans">%(cta1)s</a>
          <a class="btn btn-ghost" href="#brew">%(cta2)s</a>
        </div>
        <dl class="roast-facts">
          <div><dt>%(f1_k)s</dt><dd id="lastRoast">–</dd></div>
          <div><dt>%(f2_k)s</dt><dd>%(f2_v)s</dd></div>
          <div><dt>%(f3_k)s</dt><dd>%(f3_v)s</dd></div>
        </dl>
      </div>
      <figure class="hero-ph">%(hero_img)s<figcaption>%(hero_cap)s</figcaption></figure>
    </div>
  </section>
  <div class="marquee" aria-hidden="true"><div class="marquee-in">%(marquee)s</div></div>

  <!-- ============ Step 1: coffees ============ -->
  <section class="block" id="beans" aria-labelledby="bn-h">
    <div class="wrap">
      <header class="sec-head">
        <p class="kicker">%(k_beans)s</p>
        <h2 id="bn-h">%(beans_h)s</h2>
        <p>%(beans_p)s</p>
      </header>
      <div class="chips" id="methods" role="group" aria-label="%(method_label)s">%(chips)s</div>
      <ul class="coffees" id="coffees">%(cards_html)s</ul>
    </div>
  </section>

  <!-- ============ Steps 2 and 3: build the bag ============ -->
  <section class="block soft" id="build" aria-labelledby="bd-h">
    <div class="wrap">
      <header class="sec-head">
        <p class="kicker">%(k_build)s</p>
        <h2 id="bd-h">%(build_h)s</h2>
        <p>%(build_p)s</p>
      </header>
      <form class="build" id="buildForm" novalidate>
        <div class="b-grid">
          <fieldset class="step">
            <legend><b>1</b> %(s1)s</legend>
            <p class="picked" id="picked" role="status">%(picked_none)s</p>
            <div class="grid2">
              <fieldset class="sub"><legend>%(f_size)s</legend><div class="opts">%(size_html)s</div></fieldset>
              <div class="field"><label for="f-grind">%(f_grind)s</label><select id="f-grind" name="grind">%(grind_html)s</select></div>
            </div>
            <div class="qty-row">
              <span class="qty-l" id="qtyL">%(f_qty)s</span>
              <div class="stepper" role="group" aria-labelledby="qtyL"><button type="button" id="qMinus" aria-label="%(q_less)s">−</button><output id="qOut">1</output><button type="button" id="qPlus" aria-label="%(q_more)s">+</button></div>
            </div>
            <fieldset class="sub"><legend>%(f_freq)s</legend><div class="opts">%(freq_html)s</div></fieldset>
          </fieldset>
          <fieldset class="step">
            <legend><b>2</b> %(s2)s</legend>
            <div class="opts" role="radiogroup" aria-label="%(s2)s">
              <label class="opt"><input type="radio" name="fulfil" value="delivery" checked><span><b>%(o_deliver)s</b><small id="feeNote"></small></span></label>
              <label class="opt"><input type="radio" name="fulfil" value="pickup"><span><b>%(o_pickup)s</b><small>%(o_pickup_s)s</small></span></label>
            </div>
            <div class="field" id="addrRow"><label for="f-addr">%(f_addr)s</label><input id="f-addr" name="address" type="text" autocomplete="street-address"></div>
            <p class="sub-h" id="whenH">%(when_deliver)s</p>
            <div class="dchips" id="dchips" role="radiogroup" aria-label="%(f_day)s"></div>
            <p class="hint" id="slotHint" role="status">%(checking)s</p>
            <div class="tchips" id="tchips" role="radiogroup" aria-label="%(f_time)s"></div>
          </fieldset>
          <fieldset class="step">
            <legend><b>3</b> %(s3)s</legend>
            <div class="grid2">
              <div class="field"><label for="f-name">%(f_name)s</label><input id="f-name" name="name" type="text" autocomplete="name" required></div>
              <div class="field"><label for="f-phone">%(f_phone)s</label><input id="f-phone" name="phone" type="tel" autocomplete="tel" required></div>
            </div>
            <div class="field"><label for="f-msg">%(f_msg)s</label><textarea id="f-msg" name="msg" rows="2"></textarea></div>
            <p class="demo-note" id="demoNote" hidden></p>
            <p class="form-error" id="bkError" role="alert" hidden></p>
          </fieldset>
        </div>
        <div class="checkout" id="checkout">
          <div class="co-sum">
            <p class="co-line" id="coLine">%(co_none)s</p>
            <p class="co-sub" id="coSub"></p>
          </div>
          <p class="co-total"><span id="coTotalL">%(total_l)s</span><b id="coTotal">0,00 €</b></p>
          <button class="btn btn-main" type="submit" id="bkSend">%(f_send)s</button>
        </div>
        <small class="fine">%(f_note)s <a href="%(privacy_href)s">%(f_priv)s</a></small>
      </form>
      <div class="done" id="bkDone" hidden tabindex="-1"></div>
    </div>
  </section>

  <!-- ============ Brew calculator ============ -->
  <section class="block" id="brew" aria-labelledby="br-h">
    <div class="wrap brew">
      <div class="brew-copy">
        <header class="sec-head">
          <p class="kicker">%(k_brew)s</p>
          <h2 id="br-h">%(brew_h)s</h2>
          <p>%(brew_p)s</p>
        </header>
        <form class="calc" id="calc" aria-label="%(brew_h)s" onsubmit="return false">
          <div class="field"><label for="c-method">%(c_method)s</label><select id="c-method">%(meth_opts)s</select></div>
          <div class="field"><label for="c-cups"><span id="cupsLbl">%(c_cups)s</span>: <b id="cupsOut">2</b></label><input id="c-cups" type="range" min="1" max="8" value="2"></div>
          <dl class="calc-out" aria-live="polite">
            <div><dt>%(c_coffee)s</dt><dd id="cCoffee">–</dd></div>
            <div><dt>%(c_water)s</dt><dd id="cWater">–</dd></div>
            <div><dt>%(c_temp)s</dt><dd id="cTemp">–</dd></div>
            <div><dt>%(c_time)s</dt><dd id="cTime">–</dd></div>
            <div><dt>%(c_grind)s</dt><dd id="cGrind">–</dd></div>
          </dl>
        </form>
      </div>
      <div class="brew-photos">
        <figure class="bpx bpx-1">%(brew_img1)s</figure>
        <figure class="bpx bpx-2">%(brew_img2)s</figure>
        <figure class="bpx bpx-3">%(brew_img3)s</figure>
      </div>
    </div>
  </section>

  <!-- ============ Roastery ============ -->
  <section class="block roastery" id="roastery" aria-labelledby="ro-h">
    <div class="wrap">
      <header class="sec-head">
        <p class="kicker kicker-dark">%(k_roastery)s</p>
        <h2 id="ro-h">%(roastery_h)s</h2>
        <p>%(roastery_p)s</p>
      </header>
      <div class="steps3">
        <figure class="r-ph">%(ro_img1)s</figure>
        <ol class="r-steps">
          <li><b>%(rs1_t)s</b><span>%(rs1_p)s</span></li>
          <li><b>%(rs2_t)s</b><span>%(rs2_p)s</span></li>
          <li><b>%(rs3_t)s</b><span>%(rs3_p)s</span></li>
        </ol>
        <figure class="r-ph r-ph2">%(ro_img2)s</figure>
      </div>
      <p class="cupping"><b>%(cup_b)s</b> %(cup_p)s</p>
    </div>
  </section>

  <!-- ============ Visit ============ -->
  <section class="block" id="visit" aria-labelledby="vs-h">
    <div class="wrap visit">
      <div class="visit-copy">
        <p class="kicker">%(k_visit)s</p>
        <h2 id="vs-h">%(visit_h)s</h2>
        <dl class="hours" id="hours">%(hours_html)s</dl>
        <ul class="info">
          <li><b>%(l_addr)s</b><span>%(address)s</span></li>
          <li><b>%(l_phone)s</b><a href="tel:%(phone_href)s">%(phone)s</a></li>
          <li><b>%(l_email)s</b><a href="mailto:%(email)s">%(email)s</a></li>
        </ul>
      </div>
      <div class="visit-side">
        <figure class="visit-ph">%(visit_img)s</figure>
        <div class="map-box" id="mapBox" data-src="https://www.openstreetmap.org/export/embed.html?bbox=24.7353%%2C42.1304%%2C24.7553%%2C42.1404&amp;layer=mapnik&amp;marker=42.1354%%2C24.7453">
          <div class="map-ph">
            <p>%(map_t)s</p>
            <button class="btn btn-line btn-sm" type="button" id="mapLoad">%(map_btn)s</button>
          </div>
        </div>
      </div>
    </div>
  </section>

</main>

<footer class="foot dark">
  <div class="wrap foot-row">
    <span>© <span id="year">2026</span> Ember Roasters. %(foot_demo)s</span>
    <span class="foot-links"><a href="%(privacy_href)s">%(f_priv)s</a> <a href="%(admin_href)s">%(admin_l)s</a></span>
  </div>
</footer>

<aside class="dock" aria-label="%(dock_label)s">
  <div class="dock-label"><small>%(dock_label)s</small><b id="skinName">%(skin_name)s</b></div>
  <div class="swatches">%(swatches)s</div>
</aside>

<script type="application/json" id="emberData">%(data)s</script>
<script src="%(root)sjs/config.js"></script>
<script src="%(root)sjs/api.js"></script>
<script src="%(root)sjs/main.js"></script>
</body>
</html>
''' % dict(
        lang=lang, title=esc(title), desc=esc(desc), root=root, script=script, brand=BRAND, phone_href=PHONE_HREF, phone=PHONE, email=EMAIL, hours_ld=hours_ld,
        skip=t('Към съдържанието', 'Skip to content'), nav_label=t('Навигация', 'Navigation'), nav_html=nav_html, bag_empty=t('Торбата е празна', 'Your bag is empty'),
        other_href=other_href, other_lang='en' if bg else 'bg', other_label='EN' if bg else 'БГ', other_aria='Switch to English' if bg else 'Превключи на български', menu_btn=t('Меню', 'Menu'),
        eyebrow=t('Пържилня за кафе · Пловдив', 'Coffee roasters · Plovdiv'),
        h1=t('Изпечено във вторник. <em>В чашата ти</em> в петък.', 'Roasted on Tuesday. <em>In your cup</em> by Friday.'),
        lead=t('Малка пържилня за специално кафе. Избираш зърна, размер и мелене, а ние ги изпичаме на малки партиди и ги доставяме или ги вземаш от нас.',
               'A small specialty coffee roastery. You choose beans, size and grind; we roast in small batches and deliver, or you collect from us.'),
        cta1=t('Избери кафе', 'Choose a coffee'), cta2=t('Как се приготвя', 'How to brew'),
        f1_k=t('Последно изпичане', 'Last roast'), f2_k=t('Дни за изпичане', 'Roast days'), f2_v=t('вторник и петък', 'Tuesday and Friday'), f3_k=t('Доставка', 'Delivery'), f3_v=t('Пловдив, безплатна над 35 €', 'Plovdiv, free over €35'),
        hero_img=I('roaster-beans', t('Изпечени зърна в барабана на пържилнята', 'Freshly roasted beans in the roaster drum'), '(min-width: 960px) 480px, 90vw', eager=True), hero_cap=t('Партида от вторник', "Tuesday's batch"), marquee=marquee,
        k_beans=t('Стъпка 1', 'Step 1'), beans_h=t('Какво ще пием тази седмица', 'What we are roasting this week'), beans_p=t('Пет кафета от малки ферми. Избери едно и продължи надолу.', 'Five coffees from small farms. Choose one and carry on down the page.'),
        method_label=t('Начин на приготвяне', 'Brew method'), chips=chips, cards_html=cards_html,
        k_build=t('Стъпки 2 и 3', 'Steps 2 and 3'), build_h=t('Събери торбата си', 'Build your bag'), build_p=t('Размер, мелене, колко често. После кога и къде. Сметката е винаги на долната лента.', 'Size, grind, how often. Then when and where. The total is always on the bar at the bottom.'),
        s1=t('Твоята торба', 'Your bag'), picked_none=t('Още не си избрал кафе. Върни се горе и натисни „Избери“.', 'You have not chosen a coffee yet. Go up and press “Choose”.'),
        f_size=t('Размер', 'Size'), size_html=size_html, f_grind=t('Мелене', 'Grind'), grind_html=grind_html, f_qty=t('Брой торби', 'Number of bags'), q_less=t('Една торба по-малко', 'One bag fewer'), q_more=t('Една торба повече', 'One bag more'),
        f_freq=t('Колко често?', 'How often?'), freq_html=freq_html,
        s2=t('Доставка или вземане', 'Delivery or pick-up'), o_deliver=t('Доставка до адрес', 'Delivery to an address'), o_pickup=t('Вземане от пържилнята', 'Pick up at the roastery'), o_pickup_s=t('Безплатно', 'Free'),
        f_addr=t('Адрес за доставка', 'Delivery address'), when_deliver=t('Кога да доставим?', 'When should we deliver?'), f_day=t('Ден', 'Day'), f_time=t('Час', 'Time'), checking=t('Проверяваме свободните часове…', 'Checking free times…'),
        s3=t('Данни за връзка', 'Your details'), f_name=t('Име', 'Name'), f_phone=t('Телефон', 'Phone'), f_msg=t('Бележка (по желание)', 'Note (optional)'),
        co_none=t('Торбата е празна', 'Your bag is empty'), total_l=t('Общо', 'Total'), f_send=t('Изпрати поръчката', 'Place the order'),
        f_note=t('Плащаш при получаване. Без регистрация.', 'You pay on receipt. No account needed.'), f_priv=t('Поверителност', 'Privacy'), privacy_href='privacy.html',
        k_brew=t('Приготвяне', 'Brewing'), brew_h=t('Колко кафе за колко вода?', 'How much coffee for how much water?'),
        brew_p=t('Избери метод и колко чаши искаш. Калкулаторът ти казва грамовете, температурата и времето.', 'Choose a method and how many cups you want. The calculator gives you grams, temperature and time.'),
        c_method=t('Метод', 'Method'), meth_opts=meth_opts, c_cups=t('Чаши (по 250 мл)', 'Cups (250 ml each)'), c_coffee=t('Кафе', 'Coffee'), c_water=t('Вода', 'Water'), c_temp=t('Температура', 'Temperature'), c_time=t('Време', 'Time'), c_grind=t('Мелене', 'Grind'),
        brew_img1=I('pour-over', t('Наливане на вода във V60', 'Water poured into a V60'), '(min-width: 900px) 260px, 45vw'), brew_img2=I('drip-bag', t('Филтърна торбичка в чаша', 'A drip bag in a cup'), '(min-width: 900px) 260px, 45vw'), brew_img3=I('portafilters', t('Два портафилтъра със зърна и мляно кафе', 'Two portafilters with beans and ground coffee'), '(min-width: 900px) 260px, 45vw'),
        k_roastery=t('Пържилнята', 'The roastery'), roastery_h=t('Малки партиди, ясно изпичане', 'Small batches, clear roasting'),
        roastery_p=t('Изпичаме по 12 кг наведнъж и записваме всяка партида. Така знаем какво пращаме и можем да го повторим.', 'We roast 12 kg at a time and log every batch. That way we know what we send and can repeat it.'),
        ro_img1=I('roaster-drum', t('Барабанът на пържилнята, пълен със зърна', 'The roaster drum full of beans'), '(min-width: 900px) 420px, 90vw'), ro_img2=I('roaster-scoop', t('Лопатка за проба от зърната', 'A scoop taking a sample of the beans'), '(min-width: 900px) 420px, 90vw'),
        rs1_t=t('1 · Зелено зърно', '1 · Green coffee'), rs1_p=t('Купуваме директно от малки ферми и пазим всяка партида отделно.', 'We buy straight from small farms and keep every lot separate.'),
        rs2_t=t('2 · Изпичане', '2 · Roasting'), rs2_p=t('Вторник и петък сутрин. Следим температурата през цялото време.', 'Tuesday and Friday mornings. We watch the temperature the whole time.'),
        rs3_t=t('3 · Почивка и пакет', '3 · Rest and pack'), rs3_p=t('Две дни почивка, после пакет с датата на изпичане върху него.', 'Two days of rest, then a bag with the roast date printed on it.'),
        cup_b=t('Всяка събота в 11:00:', 'Every Saturday at 11:00:'), cup_p=t('безплатна дегустация (cupping) в пържилнята. Просто елате.', 'a free cupping at the roastery. Just come along.'),
        k_visit=t('Адрес', 'Visit'), visit_h=t('Намери пържилнята', 'Find the roastery'), hours_html=hours_html,
        l_addr=t('Адрес', 'Address'), address=ADDRESS['bg' if bg else 'en'], l_phone=t('Телефон', 'Phone'), l_email=t('Имейл', 'Email'),
        visit_img=I('board-latte', t('Дъска с мляно кафе, зърна и лате', 'A board with ground coffee, beans and a latte'), '(min-width: 900px) 520px, 90vw'),
        map_t=t('Картата се зарежда от OpenStreetMap едва когато я поискаш.', 'The map loads from OpenStreetMap only when you ask for it.'), map_btn=t('Покажи картата', 'Show the map'),
        foot_demo=t('Всичко тук е пример.', 'Everything here is an example.'), admin_href='admin.html' if bg else '../admin.html?lang=en', admin_l=t('Демо админ панел', 'Demo back office'),
        dock_label=t('Цветова схема', 'Colour scheme'), skin_name=t('Жарава', 'Ember'), swatches=swatches,
        data=json.dumps(data, ensure_ascii=False).replace('</', '<\\/'),
    )


def main():
    cfg = ('/* Generated by tools/build_pages.py. Edit the values at the top of that file, then run it again. */\n'
           'window.EMBER_CONFIG = {\n  mode: "demo",            /* "demo" = requests are kept in this browser only; "live" = real API at apiBase (docs/API.md) */\n'
           '  apiBase: "/api",\n  hours: { weekday: ["%s", "%s"], weekend: ["%s", "%s"] },\n  capacity: %d,             /* orders handled in the same time slot */\n'
           '  slotMinutes: %d,\n  leadMinutes: %d,\n  latency: [600, 1100]      /* demo only: pretend network delay in milliseconds */\n};\n'
           % (HOURS['weekday'][0], HOURS['weekday'][1], HOURS['weekend'][0], HOURS['weekend'][1], CAPACITY, SLOT_MINUTES, LEAD_MINUTES))
    open(os.path.join(ROOT, 'js', 'config.js'), 'w', encoding='utf-8').write(cfg)
    for lang, path in (('bg', 'index.html'), ('en', os.path.join('en', 'index.html'))):
        os.makedirs(os.path.dirname(os.path.join(ROOT, path)), exist_ok=True)
        open(os.path.join(ROOT, path), 'w', encoding='utf-8').write(build(lang))
    shared = open(os.path.join(ROOT, 'tools', 'shared.css'), encoding='utf-8').read()
    design = open(os.path.join(ROOT, 'tools', 'design.css'), encoding='utf-8').read()
    os.makedirs(os.path.join(ROOT, 'css'), exist_ok=True)
    open(os.path.join(ROOT, 'css', 'style.css'), 'w', encoding='utf-8').write(shared + '\n' + design)
    print('built')


if __name__ == '__main__':
    main()
