"""Builds index.html (Bulgarian), en/index.html (English), js/config.js and css/style.css for Lozeta (a restaurant for weddings, birthdays and company events).
Edit the values in this file (halls, packages, prices, hours, texts), then run:  python tools/build_pages.py && python tools/build_privacy.py
Everything about the restaurant is an example: replace it for a real restaurant."""
import json, os
from html import escape as esc
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BRAND = 'Lozeta'

# ---------------- settings you will change for a real restaurant ----------------
HOURS = {'weekday': ['11:00', '23:00'], 'weekend': ['11:00', '23:00']}   # earliest start and latest end of an event
CAPACITY = 2          # events at the same time (halls)
SLOT_MINUTES = 60
LEAD_MINUTES = 1440
EVENT_MINUTES = 360   # a booking blocks the hall for this long (6 hours)
MIN_GUESTS, MAX_GUESTS = 10, 140
SMALL_EVENT_FEE, FEE_BELOW = 150, 40   # hall fee in euro below this number of guests
PHONE, PHONE_HREF, EMAIL = '+359 88 000 0000', '+359880000000', 'events@example.com'
ADDRESS = {'bg': 'ул. Примерна 25, Пловдив', 'en': '25 Primer St., Plovdiv'}

# halls: id, capacity, photo, (bg name, en name), (bg text, en text)
HALLS = [('vineyard', 140, 'hall-white', ('Зала „Лозе“', 'The Vineyard hall'), ('Голямата ни зала с кристални полилеи и място за танци. Подходяща за сватби и големи тържества.', 'Our large hall with crystal chandeliers and a dance floor. Right for weddings and big celebrations.')),
         ('garden', 60, 'table-outdoor', ('Градинска тераса', 'The garden terrace'), ('Покрита тераса към градината, от май до септември. За кръщенета, годежи и летни рождени дни.', 'A covered terrace facing the garden, May to September. For christenings, engagements and summer birthdays.')),
         ('small', 40, 'hall-wood', ('Малката зала', 'The small room'), ('Дървена зала с една дълга маса. За семейни вечери и фирмени обеди.', 'A wood-panelled room with one long table. For family dinners and company lunches.'))]
# packages: id, price per guest, (bg name, en name), (bg lines, en lines)
PACKAGES = [('standard', 28, ('Стандартен', 'Standard'), (['Салата за добре дошли и мезета', 'Основно ястие по избор', 'Десерт', 'Безалкохолни за 4 часа'], ['A welcome salad and starters', 'A main course of your choice', 'Dessert', 'Soft drinks for 4 hours'])),
            ('full', 38, ('Пълен', 'Full'), (['Три мезета и две салати', 'Основно ястие и гарнитури', 'Десерт и кафе', 'Безалкохолни и вино за 4 часа'], ['Three starters and two salads', 'A main course and sides', 'Dessert and coffee', 'Soft drinks and wine for 4 hours'])),
            ('premium', 52, ('Премиум', 'Premium'), (['Студено и топло мезе на блок маса', 'Две основни ястия и гарнитури', 'Торта, десерти и кафе', 'Пълен бар за 5 часа'], ['A cold and hot starter buffet', 'Two main courses and sides', 'Cake, desserts and coffee', 'A full bar for 5 hours']))]
EVENTS = [('wedding', 'Сватба', 'Wedding'), ('birthday', 'Рожден ден', 'Birthday'), ('christening', 'Кръщене', 'Christening'), ('company', 'Фирмено събитие', 'Company event'), ('other', 'Друго', 'Something else')]

SKINS = [('ivory', 'Слонова кост', 'Ivory', '#FAF6EF', '#6B4A2B'), ('sage', 'Градина', 'Sage', '#F1F4EE', '#3F5E3C'), ('rose', 'Роза', 'Rose', '#FBF2F1', '#8A3A4A'),
         ('navy', 'Нощ', 'Navy', '#14192B', '#D9BE7A'), ('stone', 'Камък', 'Stone', '#F3F2F0', '#4A4A52')]


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
        return ('%d €' % v) if bg else ('€%d' % v)

    halls = ''.join('<li><figure>%s</figure><div><h3>%s</h3><p class="cap">%s</p><p>%s</p></div></li>'
                    % (I(h[2], h[3][i], '(min-width: 900px) 352px, calc(100vw - 40px)'), h[3][i], t('до %d гости' % h[1], 'up to %d guests' % h[1]), h[4][i]) for h in HALLS)
    pk = ''.join('<li class="pkg%s"><h3>%s</h3><p class="pkg-p"><b>%s</b> <span>%s</span></p><ul>%s</ul></li>'
                 % (' pkg-main' if p[0] == 'full' else '', p[2][i], money(p[1]), t('на гост', 'per guest'), ''.join('<li>%s</li>' % esc(x) for x in p[3][i])) for p in PACKAGES)
    ev_opts = ''.join('<option value="%s">%s</option>' % (k, b if bg else e) for k, b, e in EVENTS)
    hall_opts = '<option value="any">%s</option>' % t('Ще изберем заедно', 'We will choose together') + ''.join('<option value="%s">%s</option>' % (h[0], h[3][i]) for h in HALLS)
    pkg_html = ''.join('<label class="opt"><input type="radio" name="pkg" value="%s"%s><span>%s · %s</span></label>' % (p[0], ' checked' if p[0] == 'full' else '', p[2][i], money(p[1])) for p in PACKAGES) + \
               '<label class="opt"><input type="radio" name="pkg" value="unsure"><span>%s</span></label>' % t('Още не знам', 'Not sure yet')
    steps = [(t('Пишеш ни', 'You write to us'), t('Датата, броят гости и какво празнувате.', 'The date, the number of guests and what you are celebrating.')), (t('Звъним ти', 'We call you'), t('До един работен ден с оферта и свободна дата.', 'Within one working day with an offer and a free date.')),
             (t('Дегустация', 'Tasting'), t('За сватби дегустираме менюто заедно, без пари.', 'For weddings we taste the menu together, free of charge.')), (t('Празнувате', 'You celebrate'), t('Ние сме там от подготовката до последната чиния.', 'We are there from the setup to the last plate.'))]
    steps_html = ''.join('<li><b>%d</b><h3>%s</h3><p>%s</p></li>' % (n + 1, a, b) for n, (a, b) in enumerate(steps))
    hours_rows = [(t('Ресторант, всеки ден', 'Restaurant, every day'), ['11:00', '23:00'], 'wd')]
    hours_html = ''.join('<div data-hrs="wd"><dt>%s</dt><dd>%s – %s</dd></div><div data-hrs="we"><dt>%s</dt><dd>%s</dd></div>' % (n, h[0], h[1], t('Събития', 'Events'), t('по договаряне', 'by arrangement')) for n, h, k in hours_rows)
    hours_ld = '"Mo-Su 11:00-23:00"'
    swatches = ''.join('<button class="sw" type="button" data-skin="%s" style="--s1:%s;--s2:%s" aria-pressed="false" aria-label="%s"></button>' % (k, s1, s2, b if bg else e) for k, b, e, s1, s2 in SKINS)
    nav = [('#halls', t('Залите', 'Halls')), ('#packages', t('Менюта', 'Menus')), ('#gallery', t('Снимки', 'Photos')), ('#plan', t('Заявка', 'Request')), ('#visit', t('Контакти', 'Contact'))]
    nav_html = ''.join('<a href="%s">%s</a>' % n for n in nav)
    data = {'event': EVENT_MINUTES, 'min': MIN_GUESTS, 'max': MAX_GUESTS, 'fee': SMALL_EVENT_FEE, 'feeBelow': FEE_BELOW,
            'packages': {p[0]: {'price': p[1], 'name': p[2][i]} for p in PACKAGES}, 'events': {k: (b if bg else e) for k, b, e in EVENTS}, 'halls': {h[0]: h[3][i] for h in HALLS}}

    title = t('Lozeta – ресторант за сватби, рождени дни и фирмени събития в Пловдив', 'Lozeta – a restaurant for weddings, birthdays and company events in Plovdiv')
    desc = t('Lozeta е ресторант в Пловдив с три зали за сватби, кръщенета, рождени дни и фирмени събития от 10 до 140 гости. Менюта на човек, дегустация и заявка онлайн.',
             'Lozeta is a restaurant in Plovdiv with three halls for weddings, christenings, birthdays and company events for 10 to 140 guests. Menus per guest, a tasting and an online request.')

    return '''<!doctype html>
<html lang="%(lang)s" data-skin="ivory">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="theme-color" content="#FAF6EF">
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
     and an og:image (images/stock/hall-white.jpg is a placeholder) -->
<link rel="preload" href="%(root)sfonts/onest-%(script)s.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="%(root)sfonts/cormorant-garamond-600-%(script)s.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="%(root)sfonts/fonts.css">
<link rel="stylesheet" href="%(root)scss/style.css">
<script>
  /* Apply the saved colour scheme before the page paints, so it does not flash. */
  try { var s = new URLSearchParams(location.search).get("skin") || localStorage.getItem("lozetaSkin"); if (s) document.documentElement.dataset.skin = s; } catch (e) {}
</script>
<script type="application/ld+json">
{"@context":"https://schema.org","@type":"Restaurant","name":"%(brand)s","inLanguage":"%(lang)s","telephone":"%(phone_href)s","email":"%(email)s",
 "address":{"@type":"PostalAddress","streetAddress":"Primer St. 25","addressLocality":"Plovdiv","addressCountry":"BG"},"servesCuisine":"Bulgarian","openingHours":[%(hours_ld)s]}
</script>
</head>
<body>
<a class="skip" href="#main">%(skip)s</a>

<header class="top" id="top">
  <div class="top-in">
    <a class="logo" href="index.html">%(brand)s</a>
    <nav class="nav" id="nav" aria-label="%(nav_label)s">%(nav_html)s</nav>
    <div class="top-r">
      <a class="call" href="tel:%(phone_href)s"><span class="call-l">%(call_l)s</span> <b>%(phone)s</b></a>
      <a class="lang" href="%(other_href)s" lang="%(other_lang)s" hreflang="%(other_lang)s" aria-label="%(other_aria)s">%(other_label)s</a>
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
      <p class="hero-links"><a class="btn btn-main" href="#plan">%(cta1)s</a> <a class="btn btn-light" href="#halls">%(cta2)s</a></p>
    </div>
  </section>
  <div class="info-bar">
    <ul class="wrap info-row">
      <li><b>%(ib1_k)s</b> <span>%(ib1_v)s</span></li>
      <li><b>%(ib2_k)s</b> <span>%(ib2_v)s</span></li>
      <li><b>%(ib3_k)s</b> <a href="tel:%(phone_href)s">%(phone)s</a></li>
    </ul>
  </div>

  <!-- ============ Halls ============ -->
  <section class="block" id="halls" aria-labelledby="hl-h">
    <div class="wrap">
      <header class="sec-head sec-center">
        <h2 id="hl-h">%(halls_h)s</h2>
        <p>%(halls_p)s</p>
      </header>
      <ul class="halls">%(halls)s</ul>
    </div>
  </section>

  <!-- ============ Menus ============ -->
  <section class="block soft" id="packages" aria-labelledby="pk-h">
    <div class="wrap">
      <header class="sec-head sec-center">
        <h2 id="pk-h">%(pk_h)s</h2>
        <p>%(pk_p)s</p>
      </header>
      <ul class="pkgs">%(pk)s</ul>
      <p class="p-note pk-note">%(pk_note)s</p>
    </div>
  </section>

  <!-- ============ How it works ============ -->
  <section class="block" aria-labelledby="hw-h">
    <div class="wrap">
      <header class="sec-head sec-center"><h2 id="hw-h">%(how_h)s</h2></header>
      <ol class="steps4">%(steps_html)s</ol>
    </div>
  </section>

  <!-- ============ Photos ============ -->
  <section class="block soft" id="gallery" aria-labelledby="gl-h">
    <div class="wrap">
      <header class="sec-head sec-center">
        <h2 id="gl-h">%(gallery_h)s</h2>
      </header>
      <div class="gallery">
        <figure>%(g1)s</figure><figure>%(g2)s</figure><figure>%(g3)s</figure>
        <figure>%(g4)s</figure><figure>%(g5)s</figure><figure>%(g6)s</figure>
      </div>
    </div>
  </section>

  <!-- ============ Request ============ -->
  <section class="block" id="plan" aria-labelledby="pl-h">
    <div class="wrap narrow">
      <header class="sec-head sec-center">
        <h2 id="pl-h">%(plan_h)s</h2>
        <p>%(plan_p)s</p>
      </header>
      <form class="res" id="planForm" novalidate>
        <div class="row2">
          <div class="field"><label for="f-type">%(f_type)s</label><select id="f-type" name="type">%(ev_opts)s</select></div>
          <div class="field"><label for="f-guests">%(f_guests)s</label><input id="f-guests" name="guests" type="number" min="%(min)d" max="%(max)d" value="50" inputmode="numeric" required></div>
        </div>
        <div class="row2">
          <div class="field"><label for="f-hall">%(f_hall)s</label><select id="f-hall" name="hall">%(hall_opts)s</select></div>
          <div class="field"><label for="f-date">%(f_date)s</label><input id="f-date" name="date" type="date" required></div>
        </div>
        <div class="field"><label for="f-time">%(f_time)s</label><select id="f-time" name="time" required></select><p class="hint" id="timeHint" role="status">%(checking)s</p></div>
        <fieldset class="group"><legend>%(f_pkg)s</legend><div class="opts">%(pkg_html)s</div></fieldset>
        <p class="est" id="est" role="status"></p>
        <div class="row2">
          <div class="field"><label for="f-name">%(f_name)s</label><input id="f-name" name="name" type="text" autocomplete="name" required></div>
          <div class="field"><label for="f-phone">%(f_phone)s</label><input id="f-phone" name="phone" type="tel" autocomplete="tel" required></div>
        </div>
        <div class="field"><label for="f-msg">%(f_msg)s</label><textarea id="f-msg" name="msg" rows="3"></textarea></div>
        <p class="demo-note" id="demoNote" hidden></p>
        <p class="form-error" id="pError" role="alert" hidden></p>
        <button class="btn btn-main" type="submit" id="pSend">%(f_send)s</button>
        <small class="fine">%(f_note)s <a href="%(privacy_href)s">%(f_priv)s</a></small>
      </form>
      <div class="done" id="pDone" hidden tabindex="-1"></div>
    </div>
  </section>

  <!-- ============ Contact ============ -->
  <section class="block soft" id="visit" aria-labelledby="vs-h">
    <div class="wrap visit">
      <div class="visit-copy">
        <h2 id="vs-h">%(visit_h)s</h2>
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
    <span>© <span id="year">2026</span> Lozeta. %(foot_demo)s</span>
    <span class="foot-links"><a href="%(privacy_href)s">%(f_priv)s</a> <a href="%(admin_href)s">%(admin_l)s</a></span>
  </div>
</footer>

<aside class="dock" aria-label="%(dock_label)s">
  <div class="dock-label"><small>%(dock_label)s</small><b id="skinName">%(skin_name)s</b></div>
  <div class="swatches">%(swatches)s</div>
</aside>

<script type="application/json" id="lozetaData">%(data)s</script>
<script src="%(root)sjs/config.js"></script>
<script src="%(root)sjs/api.js"></script>
<script src="%(root)sjs/main.js"></script>
</body>
</html>
''' % dict(
        lang=lang, title=esc(title), desc=esc(desc), root=root, script=script, brand=BRAND, phone_href=PHONE_HREF, phone=PHONE, email=EMAIL, hours_ld=hours_ld, min=MIN_GUESTS, max=MAX_GUESTS,
        skip=t('Към съдържанието', 'Skip to content'), nav_label=t('Навигация', 'Navigation'), nav_html=nav_html, call_l=t('Обади се', 'Call'),
        other_href=other_href, other_lang='en' if bg else 'bg', other_label='EN' if bg else 'БГ', other_aria='Switch to English' if bg else 'Превключи на български', menu_btn=t('Меню', 'Menu'),
        hero_img=I('hall-ornate', t('Голяма зала с полилеи и подредени маси', 'A large hall with chandeliers and laid tables'), '100vw', eager=True),
        eyebrow=t('Ресторант за събития · Пловдив', 'A restaurant for events · Plovdiv'), h1=t('Сватби, рождени дни и фирмени събития', 'Weddings, birthdays and company events'),
        lead=t('Три зали за от 10 до 140 гости. Менюта на човек, дегустация за сватби и екип, който се грижи за всичко.', 'Three halls for 10 to 140 guests. Menus per guest, a tasting for weddings and a team that takes care of everything.'),
        cta1=t('Заяви събитие', 'Request an event'), cta2=t('Виж залите', 'See the halls'),
        ib1_k=t('Гости', 'Guests'), ib1_v=t('от 10 до 140', 'from 10 to 140'), ib2_k=t('Дегустация', 'Tasting'), ib2_v=t('безплатна за сватби', 'free for weddings'), ib3_k=t('Телефон', 'Phone'),
        halls_h=t('Три зали', 'Three halls'), halls_p=t('Всички зали са с климатик, озвучаване и собствена кухня. Залата е безплатна от 40 гости.', 'All halls have air conditioning, a sound system and their own kitchen. The hall is free from 40 guests.'), halls=halls,
        pk_h=t('Менюта на човек', 'Menus per guest'), pk_p=t('Цената е на гост и включва салон, сервиране и обслужване. Менюто променяме по ваше желание.', 'The price is per guest and includes the hall, serving and service. We change the menu to your wishes.'), pk=pk,
        pk_note=t('За вегетарианци, вегани и алергии правим отделни ястия без доплащане. Под %d гости залата струва %d €.' % (FEE_BELOW, SMALL_EVENT_FEE), 'We make separate dishes for vegetarians, vegans and allergies at no extra cost. Under %d guests the hall costs €%d.' % (FEE_BELOW, SMALL_EVENT_FEE)),
        how_h=t('Как протича', 'How it works'), steps_html=steps_html,
        gallery_h=t('Снимки от събития', 'Photos from events'),
        g1=I('table-lights', t('Маса със светлини и свещи в голяма зала', 'A table with lights and candles in a large hall'), '(min-width: 900px) 352px, 45vw'), g2=I('table-formal', t('Празнично подредена маса', 'A formally laid table'), '(min-width: 900px) 352px, 45vw'), g3=I('table-flowers', t('Маса с цветя и чаши', 'A table with flowers and glasses'), '(min-width: 900px) 352px, 45vw'),
        g4=I('table-long', t('Дълга маса с розови салфетки', 'A long table with pink napkins'), '(min-width: 900px) 352px, 45vw'), g5=I('hall-modern', t('Светла зала с кръгли маси', 'A bright hall with round tables'), '(min-width: 900px) 352px, 45vw'), g6=I('buffet', t('Блок маса в залата с големи прозорци', 'A buffet in the hall with large windows'), '(min-width: 900px) 352px, 45vw'),
        plan_h=t('Заяви събитие', 'Request an event'), plan_p=t('Кажи ни повода, броя гости и датата. Ще ти се обадим до един работен ден с оферта. Не е нужно да си сигурен във всичко: изберете заедно по телефона.', 'Tell us the occasion, the number of guests and the date. We will call you within one working day with an offer. You do not need to be sure of everything: we can decide together on the phone.'),
        f_type=t('Повод', 'Occasion'), ev_opts=ev_opts, f_guests=t('Брой гости', 'Number of guests'), f_hall=t('Зала', 'Hall'), hall_opts=hall_opts, f_date=t('Дата', 'Date'), f_time=t('Начален час', 'Start time'),
        checking=t('Избери дата, за да видиш свободните часове.', 'Choose a date to see the free start times.'), f_pkg=t('Меню', 'Menu'), pkg_html=pkg_html,
        f_name=t('Име', 'Name'), f_phone=t('Телефон', 'Phone'), f_msg=t('Какво още да знаем? (по желание)', 'Anything else we should know? (optional)'),
        f_send=t('Изпрати заявката', 'Send the request'), f_note=t('Без ангажимент. Ще ти се обадим с оферта.', 'No obligation. We will call you with an offer.'), f_priv=t('Поверителност', 'Privacy'), privacy_href='privacy.html',
        visit_h=t('Контакти', 'Contact'), hours_html=hours_html, l_addr=t('Адрес', 'Address'), address=ADDRESS['bg' if bg else 'en'], l_phone=t('Телефон', 'Phone'), l_email=t('Имейл', 'Email'),
        visit_note=t('Можеш да дойдеш да видиш залите всеки ден от 11:00 до 18:00. Обади се преди това.', 'You can come and see the halls every day from 11:00 to 18:00. Please call first.'),
        map_t=t('Картата се зарежда от OpenStreetMap едва когато я поискаш.', 'The map loads from OpenStreetMap only when you ask for it.'), map_btn=t('Покажи картата', 'Show the map'),
        foot_demo=t('Всичко тук е пример.', 'Everything here is an example.'), admin_href='admin.html' if bg else '../admin.html?lang=en', admin_l=t('Демо админ панел', 'Demo back office'),
        dock_label=t('Цветова схема', 'Colour scheme'), skin_name=t('Слонова кост', 'Ivory'), swatches=swatches,
        data=json.dumps(data, ensure_ascii=False).replace('</', '<\\/'),
    )


def main():
    cfg = ('/* Generated by tools/build_pages.py. Edit the values at the top of that file, then run it again. */\n'
           'window.LOZETA_CONFIG = {\n  mode: "demo",            /* "demo" = requests are kept in this browser only; "live" = real API at apiBase (docs/API.md) */\n'
           '  apiBase: "/api",\n  hours: { weekday: ["%s", "%s"], weekend: ["%s", "%s"] },\n  capacity: %d,             /* events at the same time (halls) */\n'
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
