"""Builds index.html (Bulgarian), en/index.html (English), js/config.js and css/style.css for Maslina.
Edit the values in this file (menu, prices, hours, texts), then run:  python tools/build_pages.py && python tools/build_privacy.py
Everything about the restaurant is an example: replace it for a real restaurant."""
import json, os
from html import escape as esc
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BRAND = 'Maslina'

# ---------------- settings you will change for a real restaurant ----------------
HOURS = {'weekday': ['12:00', '22:00'], 'weekend': ['12:00', '23:00']}
CAPACITY = 8          # tables that can be booked at the same time
SLOT_MINUTES = 30
LEAD_MINUTES = 60     # a same-day booking needs this much notice
MAX_PARTY = 10        # bigger groups are asked to call
PHONE, PHONE_HREF, EMAIL = '+359 88 000 0000', '+359880000000', 'tables@example.com'
ADDRESS = {'bg': 'ул. Примерна 8, Пловдив', 'en': '8 Primer St., Plovdiv'}
LUNCH_PRICE = 14

# id, category, price, tags (V vegetarian, VG vegan, GF gluten-free), (bg name, en name), (bg desc, en desc)
MENU = [
 ('burrata', 'starters', 11.5, 'V GF', ('Бурата с печени домати', 'Burrata with roasted tomatoes'), ('Босилек, студено пресовано зехтин', 'Basil and cold-pressed olive oil')),
 ('shopska', 'starters', 8.5, 'V GF', ('Шопска с козе сирене', 'Shopska with goat cheese'), ('Домати, краставици, печени чушки', 'Tomato, cucumber, roasted peppers')),
 ('carpaccio', 'starters', 13.5, 'GF', ('Карпачо от телешко', 'Beef carpaccio'), ('Рукола, пармезан, каперси', 'Rocket, parmesan, capers')),
 ('pumpkin', 'starters', 7.5, 'VG GF', ('Крем супа от печена тиква', 'Roast pumpkin soup'), ('Тиквено семе и мащерка', 'Pumpkin seeds and thyme')),
 ('octopus', 'starters', 16, 'GF', ('Октопод на скара', 'Grilled octopus'), ('Картофи, лимон, пушена чушка', 'Potatoes, lemon, smoked paprika')),
 ('steak', 'mains', 28, 'GF', ('Телешко филе', 'Beef fillet'), ('Чубрица и сос от червено вино', 'Savory and red wine sauce')),
 ('salmon', 'mains', 22, 'GF', ('Сьомга с резене', 'Salmon with fennel'), ('Лимонов сос, печени зеленчуци', 'Lemon sauce and roasted vegetables')),
 ('lamb', 'mains', 24.5, 'GF', ('Агнешко печено', 'Roast lamb'), ('Картофи с розмарин, сос от мента', 'Rosemary potatoes and mint sauce')),
 ('chicken', 'mains', 17.5, 'GF', ('Пилешко със зеленчуци', 'Chicken with vegetables'), ('Градински зеленчуци и картофено пюре', 'Garden vegetables and mashed potato')),
 ('risotto', 'mains', 16.5, 'V GF', ('Ризото с гъби', 'Mushroom risotto'), ('Пармезан и пресен магданоз', 'Parmesan and fresh parsley')),
 ('veg', 'mains', 14.5, 'VG GF', ('Печени зеленчуци с хумус', 'Roast vegetables with hummus'), ('Сумак, лимон, тахан', 'Sumac, lemon, tahini')),
 ('spaghetti', 'pasta', 12.5, 'VG', ('Спагети помодоро', 'Spaghetti pomodoro'), ('Доматен сос и босилек', 'Tomato sauce and basil')),
 ('penne', 'pasta', 14, '', ('Пене болонезе', 'Penne bolognese'), ('Бавно готвен телешки сос', 'Slow-cooked beef ragù')),
 ('pesto', 'pasta', 13.5, 'V', ('Фарфале с песто', 'Farfalle with pesto'), ('Сушени домати и бадеми', 'Sun-dried tomatoes and almonds')),
 ('truffle', 'pasta', 18, 'V', ('Таляталe с трюфел', 'Tagliatelle with truffle'), ('Сметана и пармезан', 'Cream and parmesan')),
 ('seafood', 'pasta', 19.5, '', ('Лингуини с морски дарове', 'Linguine with seafood'), ('Миди, скариди, чери домати', 'Mussels, prawns, cherry tomatoes')),
 ('tiramisu', 'desserts', 7.5, 'V', ('Тирамису', 'Tiramisu'), ('Маскарпоне и еспресо', 'Mascarpone and espresso')),
 ('pannacotta', 'desserts', 7, 'V GF', ('Панакота', 'Panna cotta'), ('Горски плодове', 'Wild berries')),
 ('baklava', 'desserts', 6.5, 'V', ('Баклава', 'Baklava'), ('Орехи и мед', 'Walnuts and honey')),
 ('souffle', 'desserts', 8.5, 'V', ('Шоколадово суфле', 'Chocolate soufflé'), ('Топло, със сладолед от ванилия', 'Warm, with vanilla ice cream')),
 ('sorbet', 'desserts', 5.5, 'VG GF', ('Сорбе от сезонни плодове', 'Seasonal fruit sorbet'), ('Две топки', 'Two scoops')),
]
CATS = [('all', 'Всичко', 'All'), ('starters', 'Предястия', 'Starters'), ('mains', 'Основни', 'Mains'), ('pasta', 'Паста', 'Pasta'), ('desserts', 'Десерти', 'Desserts')]
DIETS = [('V', 'Вегетарианско', 'Vegetarian'), ('VG', 'Веган', 'Vegan'), ('GF', 'Без глутен', 'Gluten-free')]
OCCASIONS = [('none', 'Без повод', 'No occasion'), ('birthday', 'Рожден ден', 'Birthday'), ('anniversary', 'Годишнина', 'Anniversary'), ('business', 'Бизнес вечеря', 'Business dinner'), ('other', 'Друг повод', 'Other')]
ALLERGIES = [('gluten', 'Глутен', 'Gluten'), ('lactose', 'Лактоза', 'Lactose'), ('nuts', 'Ядки', 'Nuts'), ('shellfish', 'Морски дарове', 'Shellfish'), ('veg', 'Вегетарианец', 'Vegetarian'), ('vegan', 'Веган', 'Vegan')]

SKINS = [('olive', 'Маслина', 'Olive', '#F5F0E4', '#4F5B2A'), ('bordeaux', 'Бордо', 'Bordeaux', '#1C1013', '#E0B07A'),
         ('terracotta', 'Теракота', 'Terracotta', '#F8EEE4', '#A34A2B'), ('sea', 'Море', 'Sea', '#EEF3F2', '#176B72'),
         ('brass', 'Месинг', 'Brass', '#14161A', '#C7A24A')]


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

    cats = ''.join('<button class="chip" type="button" data-cat="%s" aria-pressed="%s">%s</button>' % (k, 'true' if k == 'all' else 'false', b if bg else e) for k, b, e in CATS)
    diets = ''.join('<button class="chip chip-d" type="button" data-diet="%s" aria-pressed="false">%s</button>' % (k, b if bg else e) for k, b, e in DIETS)
    groups = []
    for k, b, e in CATS[1:]:
        rows = []
        for mid, cat, price, tags, nm, ds in [m for m in MENU if m[1] == k]:
            tg = ''.join('<span class="tag" title="%s">%s</span>' % ({'V': t('Вегетарианско', 'Vegetarian'), 'VG': t('Веган', 'Vegan'), 'GF': t('Без глутен', 'Gluten-free')}[x], x) for x in tags.split())
            rows.append('<li class="m-item" data-cat="%s" data-tags="%s"><div class="m-top"><h4>%s</h4><i aria-hidden="true"></i><b>%s</b></div><p>%s %s</p></li>'
                        % (cat, tags, esc(nm[i]), money(price), esc(ds[i]), tg))
        groups.append('<section class="m-group" data-cat="%s" aria-labelledby="mg-%s"><h3 id="mg-%s">%s</h3><ul class="m-list">%s</ul></section>' % (k, k, k, b if bg else e, ''.join(rows)))
    menu_html = ''.join(groups)

    sig = [('spaghetti', t('Спагети помодоро', 'Spaghetti pomodoro'), t('Доматите са от нашата градина.', 'The tomatoes come from our own garden.'), '12,50 €' if bg else '€12.50'),
           ('salmon', t('Сьомга с резене', 'Salmon with fennel'), t('Печена на тих огън, със свеж лимон.', 'Slow-roasted, with fresh lemon.'), '22,00 €' if bg else '€22.00'),
           ('pesto-pasta', t('Фарфале с песто', 'Farfalle with pesto'), t('Босилек, бадеми и малко пармезан.', 'Basil, almonds and a little parmesan.'), '13,50 €' if bg else '€13.50')]
    sig_html = ''.join('<li class="sig"><figure>%s</figure><div><h3>%s</h3><p>%s</p><b>%s</b></div></li>' % (I(n, a, '(min-width: 800px) 380px, calc(100vw - 40px)'), a, d, p) for n, a, d, p in sig)

    hours_rows = [(t('Понеделник – петък', 'Monday – Friday'), HOURS['weekday'], 'wd'), (t('Събота и неделя', 'Saturday and Sunday'), HOURS['weekend'], 'we')]
    hours_html = ''.join('<div data-hrs="%s"><dt>%s</dt><dd>%s – %s</dd></div>' % (k, n, h[0], h[1]) for n, h, k in hours_rows)
    hours_ld = '"Mo-Fr %s-%s","Sa-Su %s-%s"' % (HOURS['weekday'][0], HOURS['weekday'][1], HOURS['weekend'][0], HOURS['weekend'][1])
    swatches = ''.join('<button class="sw" type="button" data-skin="%s" style="--s1:%s;--s2:%s" aria-pressed="false" aria-label="%s"></button>' % (k, s1, s2, b if bg else e) for k, b, e, s1, s2 in SKINS)
    nav = [('#menu', t('Меню', 'Menu')), ('#lunch', t('Обяд', 'Lunch')), ('#atmosphere', t('Атмосфера', 'Atmosphere')), ('#visit', t('Адрес', 'Visit'))]
    nav_html = ''.join('<a href="%s">%s</a>' % n for n in nav)
    occ_html = ''.join('<option value="%s">%s</option>' % (k, b if bg else e) for k, b, e in OCCASIONS)
    all_html = ''.join('<label class="opt"><input type="checkbox" name="allergy" value="%s" data-name="%s"><span>%s</span></label>' % (k, b if bg else e, b if bg else e) for k, b, e in ALLERGIES)
    party_opts = ''.join('<option value="%d"%s>%s</option>' % (n, ' selected' if n == 2 else '', n) for n in range(1, MAX_PARTY + 1))

    data = {'maxParty': MAX_PARTY, 'seating': {'any': t('Без значение', 'No preference'), 'inside': t('Вътре', 'Inside'), 'terrace': t('На терасата', 'On the terrace')},
            'occasions': {k: (b if bg else e) for k, b, e in OCCASIONS}}

    title = t('Maslina – ресторант в Пловдив. Резервирай маса онлайн', 'Maslina – restaurant in Plovdiv. Reserve a table online')
    desc = t('Maslina е ресторант в Пловдив със средиземноморска кухня, сезонни продукти и ежедневно обедно меню. Виж менюто и резервирай маса за минута.',
             'Maslina is a restaurant in Plovdiv with Mediterranean cooking, seasonal produce and a daily lunch menu. See the menu and reserve a table in a minute.')

    return '''<!doctype html>
<html lang="%(lang)s" data-skin="olive">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="theme-color" content="#F5F0E4">
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
     and an og:image (images/stock/hall-light.jpg is a placeholder) -->
<link rel="preload" href="%(root)sfonts/onest-%(script)s.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="%(root)sfonts/cormorant-garamond-600-%(script)s.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="%(root)sfonts/fonts.css">
<link rel="stylesheet" href="%(root)scss/style.css">
<script>
  /* Scroll animations only run when the browser supports them and the visitor has not asked for less motion. */
  if ("IntersectionObserver" in window && !matchMedia("(prefers-reduced-motion: reduce)").matches) document.documentElement.classList.add("js-reveal");
</script>
<script>
  /* Apply the saved colour scheme before the page paints, so it does not flash. */
  try { var s = new URLSearchParams(location.search).get("skin") || localStorage.getItem("maslinaSkin"); if (s) document.documentElement.dataset.skin = s; } catch (e) {}
</script>
<script type="application/ld+json">
{"@context":"https://schema.org","@type":"Restaurant","name":"%(brand)s","inLanguage":"%(lang)s","telephone":"%(phone_href)s","email":"%(email)s",
 "address":{"@type":"PostalAddress","streetAddress":"Primer St. 8","addressLocality":"Plovdiv","addressCountry":"BG"},
 "servesCuisine":"Mediterranean","acceptsReservations":"True","openingHours":[%(hours_ld)s]}
</script>
</head>
<body>
<a class="skip" href="#main">%(skip)s</a>

<header class="top" id="top">
  <div class="top-in">
    <nav class="nav" id="nav" aria-label="%(nav_label)s">%(nav_html)s</nav>
    <a class="logo" href="index.html"><svg viewBox="0 0 32 32" width="26" height="26" aria-hidden="true" focusable="false"><path d="M4 26C10 14 18 8 28 5" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/><path d="M11 20c-4 .5-6-2-6.5-5 3.5-.5 6 1 6.5 5zM15 15c-3.5-.6-4.6-3.4-4.5-6.3 3.4.6 4.9 3 4.5 6.3zM21 11c-3-.8-3.6-3.4-3-6 3.2.9 3.9 3.2 3 6zM17 21c3.5-1.2 6.3-.3 8.6 2-2.7 2.2-6.3 1.8-8.6-2z" fill="currentColor"/></svg><b>%(brand)s</b></a>
    <div class="top-r">
      <a class="lang" href="%(other_href)s" lang="%(other_lang)s" hreflang="%(other_lang)s" aria-label="%(other_aria)s">%(other_label)s</a>
      <a class="btn btn-main btn-sm" href="#reserve">%(cta)s</a>
      <button class="burger" id="burger" type="button" aria-controls="nav" aria-expanded="false" aria-label="%(menu_btn)s"><span></span></button>
    </div>
  </div>
</header>

<main id="main">

  <!-- ============ Hero ============ -->
  <section class="hero" aria-labelledby="h1">
    <div class="hero-bg" aria-hidden="true">%(hero_img)s</div>
    <div class="wrap hero-in">
      <p class="eyebrow">%(eyebrow)s</p>
      <h1 id="h1">%(h1)s</h1>
      <p class="lead">%(lead)s</p>
    </div>
    <form class="quick wrap" id="quick" aria-labelledby="q-h">
      <h2 id="q-h" class="quick-h">%(q_h)s</h2>
      <label class="q-f"><span>%(q_party)s</span><select id="qParty">%(party_opts)s</select></label>
      <label class="q-f"><span>%(q_date)s</span><select id="qDate"></select></label>
      <button class="btn btn-main" type="submit">%(q_btn)s</button>
    </form>
  </section>

  <!-- ============ Signature dishes ============ -->
  <section class="block sigs" id="signature" aria-labelledby="sg-h">
    <div class="wrap">
      <header class="sec-head sec-center">
        <p class="kicker">%(k_sig)s</p>
        <h2 id="sg-h">%(sig_h)s</h2>
        <p>%(sig_p)s</p>
      </header>
      <ul class="sig-list">%(sig_html)s</ul>
    </div>
  </section>

  <!-- ============ Menu ============ -->
  <section class="block soft" id="menu" aria-labelledby="mn-h">
    <div class="wrap">
      <header class="sec-head sec-center">
        <p class="kicker">%(k_menu)s</p>
        <h2 id="mn-h">%(menu_h)s</h2>
        <p>%(menu_p)s</p>
      </header>
      <div class="filters">
        <div class="chips" id="cats" role="group" aria-label="%(cat_label)s">%(cats)s</div>
        <div class="chips" id="diets" role="group" aria-label="%(diet_label)s">%(diets)s</div>
      </div>
      <p class="m-empty" id="menuEmpty" role="status" hidden>%(empty)s</p>
      <div class="menu-cols" id="menuBox">%(menu_html)s</div>
      <p class="m-note">%(allergy_note)s</p>
    </div>
  </section>

  <!-- ============ Lunch ============ -->
  <section class="block lunch" id="lunch" aria-labelledby="ln-h">
    <div class="wrap lunch-in">
      <figure class="lunch-ph">%(lunch_img)s</figure>
      <div class="lunch-card">
        <p class="kicker">%(k_lunch)s</p>
        <h2 id="ln-h">%(lunch_h)s</h2>
        <p class="lunch-when" id="lunchWhen">%(lunch_when)s</p>
        <ul class="lunch-menu">
          <li><span>%(lc1)s</span><b>%(lc1v)s</b></li>
          <li><span>%(lc2)s</span><b>%(lc2v)s</b></li>
          <li><span>%(lc3)s</span><b>%(lc3v)s</b></li>
        </ul>
        <p class="lunch-price"><b>%(lunch_price)s</b> <span>%(lunch_inc)s</span></p>
      </div>
    </div>
  </section>

  <!-- ============ Reserve ============ -->
  <section class="block soft" id="reserve" aria-labelledby="rs-h">
    <div class="wrap">
      <header class="sec-head sec-center">
        <p class="kicker">%(k_res)s</p>
        <h2 id="rs-h">%(res_h)s</h2>
        <p>%(res_p)s</p>
      </header>
      <form class="res-form" id="resForm" novalidate>
        <div class="steps">
          <fieldset class="step">
            <legend><b>1</b> %(s1)s</legend>
            <div class="party-row">
              <div class="stepper" role="group" aria-label="%(f_party)s">
                <button type="button" id="pMinus" aria-label="%(f_fewer)s">−</button>
                <output id="partyOut" aria-live="polite">2</output>
                <button type="button" id="pPlus" aria-label="%(f_more)s">+</button>
              </div>
              <p class="hint" id="partyHint"></p>
            </div>
            <div class="dchips" id="dchips" role="radiogroup" aria-label="%(f_day)s"></div>
          </fieldset>
          <fieldset class="step">
            <legend><b>2</b> %(s2)s</legend>
            <p class="hint" id="slotHint" role="status">%(checking)s</p>
            <div id="tchips"></div>
          </fieldset>
          <fieldset class="step">
            <legend><b>3</b> %(s3)s</legend>
            <div class="grid2">
              <div class="field"><label for="f-occ">%(f_occ)s</label><select id="f-occ" name="occ">%(occ_html)s</select></div>
              <div class="field"><label for="f-seat">%(f_seat)s</label><select id="f-seat" name="seat"><option value="any">%(seat_any)s</option><option value="inside">%(seat_in)s</option><option value="terrace">%(seat_out)s</option></select></div>
            </div>
            <p class="sub-h">%(f_allergy)s</p>
            <div class="opts">%(all_html)s</div>
          </fieldset>
          <fieldset class="step">
            <legend><b>4</b> %(s4)s</legend>
            <div class="grid2">
              <div class="field"><label for="f-name">%(f_name)s</label><input id="f-name" name="name" type="text" autocomplete="name" required></div>
              <div class="field"><label for="f-phone">%(f_phone)s</label><input id="f-phone" name="phone" type="tel" autocomplete="tel" required></div>
            </div>
            <div class="field"><label for="f-msg">%(f_msg)s</label><textarea id="f-msg" name="msg" rows="3"></textarea></div>
          </fieldset>
        </div>

        <section class="ticket" aria-labelledby="tk-h">
          <h3 id="tk-h">%(tk_h)s</h3>
          <dl class="tk-list">
            <div><dt>%(tk_party)s</dt><dd id="tkParty">2</dd></div>
            <div><dt>%(tk_when)s</dt><dd id="tkWhen">–</dd></div>
            <div><dt>%(tk_table)s</dt><dd id="tkTable">–</dd></div>
            <div><dt>%(tk_notes)s</dt><dd id="tkNotes">–</dd></div>
          </dl>
          <p class="tk-fine">%(tk_fine)s</p>
          <p class="demo-note" id="demoNote" hidden></p>
          <p class="form-error" id="bkError" role="alert" hidden></p>
          <button class="btn btn-main btn-block" type="submit" id="bkSend">%(f_send)s</button>
          <small class="fine">%(f_note)s <a href="%(privacy_href)s">%(f_priv)s</a></small>
        </section>
      </form>
      <div class="done" id="bkDone" hidden tabindex="-1"></div>
    </div>
  </section>

  <!-- ============ Atmosphere ============ -->
  <section class="block" id="atmosphere" aria-labelledby="at-h">
    <div class="wrap">
      <header class="sec-head sec-center">
        <p class="kicker">%(k_atm)s</p>
        <h2 id="at-h">%(atm_h)s</h2>
        <p>%(atm_p)s</p>
      </header>
      <div class="mosaic">
        <figure class="mo mo-1">%(mo1)s</figure>
        <figure class="mo mo-2">%(mo2)s</figure>
        <figure class="mo mo-3">%(mo3)s</figure>
        <figure class="mo mo-4">%(mo4)s</figure>
        <figure class="mo mo-5">%(mo5)s</figure>
      </div>
    </div>
  </section>

  <!-- ============ Visit ============ -->
  <section class="block soft" id="visit" aria-labelledby="vs-h">
    <div class="wrap visit">
      <div class="visit-copy">
        <p class="kicker">%(k_visit)s</p>
        <h2 id="vs-h">%(visit_h)s</h2>
        <p class="status-line"><span class="open-pill" id="openPill" data-state="unknown"><i aria-hidden="true"></i><span id="openText">%(hours_short)s</span></span></p>
        <dl class="hours" id="hours">%(hours_html)s</dl>
        <ul class="info">
          <li><b>%(l_addr)s</b><span>%(address)s</span></li>
          <li><b>%(l_phone)s</b><a href="tel:%(phone_href)s">%(phone)s</a></li>
          <li><b>%(l_email)s</b><a href="mailto:%(email)s">%(email)s</a></li>
        </ul>
        <p class="visit-note">%(visit_note)s</p>
      </div>
      <div class="visit-side">
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
    <span>© <span id="year">2026</span> Maslina. %(foot_demo)s</span>
    <span class="foot-links"><a href="%(privacy_href)s">%(f_priv)s</a> <a href="%(admin_href)s">%(admin_l)s</a></span>
  </div>
</footer>

<div class="actionbar" id="bar">
  <a class="btn btn-line btn-sm" href="tel:%(phone_href)s">%(bar_call)s</a>
  <a class="btn btn-main btn-sm" href="#reserve">%(bar_book)s</a>
</div>

<aside class="dock" aria-label="%(dock_label)s">
  <div class="dock-label"><small>%(dock_label)s</small><b id="skinName">%(skin_name)s</b></div>
  <div class="swatches">%(swatches)s</div>
</aside>

<script type="application/json" id="masData">%(data)s</script>
<script src="%(root)sjs/config.js"></script>
<script src="%(root)sjs/api.js"></script>
<script src="%(root)sjs/main.js"></script>
</body>
</html>
''' % dict(
        lang=lang, title=esc(title), desc=esc(desc), root=root, script=script, brand=BRAND, phone_href=PHONE_HREF, phone=PHONE, email=EMAIL, hours_ld=hours_ld,
        skip=t('Към съдържанието', 'Skip to content'), nav_label=t('Навигация', 'Navigation'), nav_html=nav_html,
        other_href=other_href, other_lang='en' if bg else 'bg', other_label='EN' if bg else 'БГ', other_aria='Switch to English' if bg else 'Превключи на български',
        cta=t('Резервирай', 'Reserve'), menu_btn=t('Меню', 'Menu'),
        hero_img=I('hall-light', t('Светлият салон на ресторанта с големи прозорци и растения', 'The bright dining room with large windows and plants'), '100vw', eager=True),
        eyebrow=t('Ресторант · Пловдив', 'Restaurant · Plovdiv'),
        h1=t('Бавна храна, <em>дълги вечери</em>', 'Slow food, <em>long evenings</em>'),
        lead=t('Средиземноморска кухня със сезонни продукти. Избери маса за минута, а ние ще се погрижим за останалото.', 'Mediterranean cooking with seasonal produce. Choose a table in a minute and we will take care of the rest.'),
        q_h=t('Резервирай маса', 'Reserve a table'), q_party=t('Гости', 'Guests'), q_date=t('Дата', 'Date'), q_btn=t('Виж свободните часове', 'See free times'), party_opts=party_opts,
        k_sig=t('От кухнята', 'From the kitchen'), sig_h=t('Три ястия, с които започваме', 'Three dishes we start with'),
        sig_p=t('Примерни ястия. Менюто се сменя със сезоните.', 'Sample dishes. The menu changes with the seasons.'), sig_html=sig_html,
        k_menu=t('Меню', 'Menu'), menu_h=t('Менюто', 'The menu'), menu_p=t('Избери категория или филтрирай по хранителен режим.', 'Choose a category or filter by diet.'),
        cat_label=t('Категория', 'Category'), diet_label=t('Хранителен режим', 'Diet'), cats=cats, diets=diets, menu_html=menu_html,
        empty=t('Няма ястия с тези филтри. Свали един от тях.', 'No dishes match these filters. Remove one of them.'),
        allergy_note=t('V вегетарианско · VG веган · GF без глутен. Кажи ни за алергии преди да поръчаш: кухнята работи с ядки, млечни продукти и глутен.', 'V vegetarian · VG vegan · GF gluten-free. Tell us about allergies before you order: the kitchen handles nuts, dairy and gluten.'),
        lunch_img=I('steak-sauce', t('Сервиране на телешко филе със сос', 'A beef fillet being sauced at the pass'), '(min-width: 900px) 520px, 92vw'),
        k_lunch=t('Обедно меню', 'Lunch menu'), lunch_h=t('Обяд с три хода', 'Three-course lunch'), lunch_when=t('Понеделник – петък, 12:00 – 15:00', 'Monday – Friday, 12:00 – 15:00'),
        lc1=t('Предястие', 'Starter'), lc1v=t('Крем супа от печена тиква', 'Roast pumpkin soup'), lc2=t('Основно', 'Main'), lc2v=t('Пилешко със зеленчуци', 'Chicken with vegetables'), lc3=t('Десерт', 'Dessert'), lc3v=t('Панакота с горски плодове', 'Panna cotta with wild berries'),
        lunch_price=money(LUNCH_PRICE), lunch_inc=t('с хляб и вода', 'with bread and water'),
        k_res=t('Резервация', 'Reservation'), res_h=t('Запази маса', 'Reserve your table'),
        res_p=t('Четири кратки стъпки. Картата вдясно показва какво сме записали.', 'Four short steps. The card on the right shows what we have noted.'),
        s1=t('Гости и ден', 'Guests and day'), f_party=t('Брой гости', 'Number of guests'), f_fewer=t('Един гост по-малко', 'One guest fewer'), f_more=t('Един гост повече', 'One guest more'), f_day=t('Ден', 'Day'),
        s2=t('Час', 'Time'), checking=t('Проверяваме свободните маси…', 'Checking free tables…'),
        s3=t('Повод и предпочитания', 'Occasion and preferences'), f_occ=t('Повод', 'Occasion'), occ_html=occ_html, f_seat=t('Къде да седнете', 'Where to sit'), seat_any=t('Без значение', 'No preference'), seat_in=t('Вътре', 'Inside'), seat_out=t('На терасата', 'On the terrace'),
        f_allergy=t('Алергии и хранителен режим', 'Allergies and diet'), all_html=all_html,
        s4=t('Данни за връзка', 'Your details'), f_name=t('Име', 'Name'), f_phone=t('Телефон', 'Phone'), f_msg=t('Бележка (по желание)', 'Note (optional)'),
        tk_h=t('Твоята резервация', 'Your reservation'), tk_party=t('Гости', 'Guests'), tk_when=t('Кога', 'When'), tk_table=t('Маса', 'Table'), tk_notes=t('Бележки', 'Notes'),
        tk_fine=t('Пазим масата 15 минути след часа. Ако закъснявате, обадете се.', 'We hold the table for 15 minutes. If you are running late, please call.'),
        f_send=t('Резервирай масата', 'Book the table'), f_note=t('Без предплащане. Ще се свържем само ако трябва да потвърдим.', 'No deposit. We will contact you only if we need to confirm.'),
        f_priv=t('Поверителност', 'Privacy'), privacy_href='privacy.html',
        k_atm=t('Атмосфера', 'Atmosphere'), atm_h=t('Място за разговор', 'A place to talk'),
        atm_p=t('Светъл салон, бар и тераса. Подходящо за вечеря за двама и за маса с приятели.', 'A bright dining room, a bar and a terrace. Good for dinner for two or a table of friends.'),
        mo1=I('hall-dark', t('Вечерният салон със светлини и дървени маси', 'The evening dining room with lights and wooden tables'), '(min-width: 900px) 600px, 92vw'),
        mo2=I('terrace-lake', t('Тераса с маси на брега на езеро', 'A terrace with tables by the lake'), '(min-width: 900px) 360px, 46vw'),
        mo3=I('table-wine', t('Подредена маса с чаши за вино', 'A laid table with wine glasses'), '(min-width: 900px) 360px, 46vw'),
        mo4=I('bar-brown', t('Барът с тъмно дърво и висящи лампи', 'The bar with dark wood and hanging lamps'), '(min-width: 900px) 420px, 92vw'),
        mo5=I('street-terrace', t('Малка улична тераса пред ресторанта', 'A small street terrace in front of the restaurant'), '(min-width: 900px) 300px, 46vw'),
        k_visit=t('Адрес', 'Visit'), visit_h=t('Заповядай при нас', 'Come and see us'), hours_short=t('Работно време', 'Opening hours'), hours_html=hours_html,
        l_addr=t('Адрес', 'Address'), address=ADDRESS['bg' if bg else 'en'], l_phone=t('Телефон', 'Phone'), l_email=t('Имейл', 'Email'),
        visit_note=t('За групи над %d души ни се обадете.' % MAX_PARTY, 'For groups of more than %d please call us.' % MAX_PARTY),
        map_t=t('Картата се зарежда от OpenStreetMap едва когато я поискаш.', 'The map loads from OpenStreetMap only when you ask for it.'), map_btn=t('Покажи картата', 'Show the map'),
        foot_demo=t('Всичко тук е пример.', 'Everything here is an example.'), admin_href='admin.html' if bg else '../admin.html?lang=en', admin_l=t('Демо админ панел', 'Demo back office'),
        bar_call=t('Обади се', 'Call'), bar_book=t('Резервирай', 'Reserve'), dock_label=t('Цветова схема', 'Colour scheme'), skin_name=t('Маслина', 'Olive'), swatches=swatches,
        data=json.dumps(data, ensure_ascii=False).replace('</', '<\\/'),
    )


def main():
    cfg = ('/* Generated by tools/build_pages.py. Edit the values at the top of that file, then run it again. */\n'
           'window.MASLINA_CONFIG = {\n  mode: "demo",            /* "demo" = requests are kept in this browser only; "live" = real API at apiBase (docs/API.md) */\n'
           '  apiBase: "/api",\n  hours: { weekday: ["%s", "%s"], weekend: ["%s", "%s"] },\n  capacity: %d,             /* tables that can be booked at the same time */\n'
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
