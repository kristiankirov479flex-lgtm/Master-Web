"""Builds index.html (Bulgarian), en/index.html (English), js/config.js and css/style.css for Kristal (a car detailing studio).
Edit the values in this file (packages, prices, hours, texts), then run:  python tools/build_pages.py && python tools/build_privacy.py
Everything about the studio is an example: replace it for a real studio."""
import json, os
from html import escape as esc
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BRAND = 'Kristal'

# ---------------- settings you will change for a real studio ----------------
HOURS = {'weekday': ['08:00', '18:00'], 'weekend': ['09:00', '14:00']}
CAPACITY = 2          # cars worked on at the same time (bays)
SLOT_MINUTES = 30
LEAD_MINUTES = 120
ADDON_MINUTES = 20    # each add-on makes the job this much longer
PHONE, PHONE_HREF, EMAIL = '+359 88 000 0000', '+359880000000', 'studio@example.com'
ADDRESS = {'bg': 'ул. Примерна 70, Пловдив', 'en': '70 Primer St., Plovdiv'}
MAKES = ['Audi', 'BMW', 'Citroën', 'Dacia', 'Fiat', 'Ford', 'Honda', 'Hyundai', 'Kia', 'Mazda', 'Mercedes-Benz', 'Nissan', 'Opel', 'Peugeot', 'Renault', 'Seat', 'Škoda', 'Toyota', 'Volkswagen', 'Volvo']

SIZES = [('s', 'Малък', 'Small', 'Градски автомобил', 'City car'), ('m', 'Среден', 'Medium', 'Седан, комби', 'Saloon, estate'), ('l', 'SUV', 'SUV', 'Джип, кросоувър', 'Crossover, 4x4'), ('v', 'Бус', 'Van', 'Ван, миниван', 'Van, minivan')]
# packages: id, minutes, prices small/medium/SUV/van, is "from" price, photo, (bg name, en name), (bg lines, en lines)
PACKAGES = [
 ('wash', 90, (35, 45, 55, 65), False, 'suds-black', ('Външно измиване', 'Exterior wash'), (['Ръчно измиване с пяна', 'Почистване на джанти и гуми', 'Подсушаване и защитен восък'], ['Hand wash with foam', 'Wheels and tyres cleaned', 'Dried and sealed with a protective wax'])),
 ('interior', 180, (70, 90, 110, 130), False, 'interior', ('Вътрешно почистване', 'Interior clean'), (['Изсмукване и прахосмукачка по шевовете', 'Табло, врати и пластмаси', 'Стъкла отвътре и почистване на седалки'], ['Vacuum, including the seams', 'Dashboard, doors and plastics', 'Windows inside and seats cleaned'])),
 ('full', 360, (160, 200, 250, 300), False, 'red-car', ('Пълен детайлинг', 'Full detail'), (['Всичко от външното и вътрешното', 'Глинен препарат и полиране на фаровете', 'Защита на боята за шест месеца'], ['Everything in the exterior and interior packages', 'Clay bar and headlight polish', 'Six months of paint protection'])),
 ('polish', 300, (220, 280, 350, 420), True, 'polish-hood', ('Полиране на боята', 'Paint correction'), (['Премахване на фини драскотини', 'Машинно полиране на цялата кола', 'Възвръща блясъка на боята'], ['Fine scratches removed', 'Machine polish of the whole car', 'Brings back the shine of the paint'])),
 ('ceramic', 480, (450, 550, 700, 800), True, 'white-foam', ('Керамично покритие', 'Ceramic coating'), (['Включва полиране на боята', 'Защита до три години', 'Водата се стича, мръсотията се държи по-малко'], ['Includes paint correction', 'Protection for up to three years', 'Water runs off and dirt sticks less'])),
]
# add-ons: id, price, (bg name, en name)
ADDONS = [('lights', 40, ('Реставрация на фарове', 'Headlight restoration')), ('pet', 30, ('Премахване на животински косми', 'Pet hair removal')), ('engine', 35, ('Почистване на двигателното отделение', 'Engine bay clean')), ('odour', 25, ('Озониране срещу миризми', 'Ozone odour treatment'))]

SKINS = [('graphite', 'Графит', 'Graphite', '#F2F3F4', '#C1121F'), ('steel', 'Стомана', 'Steel', '#F2F5F8', '#1F4E79'), ('pearl', 'Перла', 'Pearl', '#F3F7F7', '#0E7C86'),
         ('noir', 'Ноар', 'Noir', '#121316', '#E5B84B'), ('racing', 'Рали', 'Racing', '#FAF5F0', '#B84A07')]


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

    def hm(m):
        h, r = divmod(m, 60)
        return (('%d %s' % (h, t('ч', 'h'))) if h else '') + ((' %d %s' % (r, t('мин', 'min'))) if r else '')

    def money(v, frm=False):
        s = str(v)
        return ((t('от ', 'from ') if frm else '') + s + ' €') if bg else ((t('от ', 'from ') if frm else '') + '€' + s)

    cards = ''.join('<li class="pk"><figure>%s</figure><div><h3>%s</h3><p class="pk-t">%s</p><ul>%s</ul><p class="pk-from">%s <b>%s</b></p></div></li>'
                    % (I(p[4], p[5][i], '(min-width: 1100px) 340px, (min-width: 760px) 45vw, calc(100vw - 40px)'), p[5][i], t('Около ', 'About ') + hm(p[1]), ''.join('<li>%s</li>' % esc(x) for x in p[6][i]),
                       t('Малък автомобил:', 'Small car:'), money(p[2][0], p[3])) for p in PACKAGES)
    head = '<tr><th scope="col">%s</th>%s</tr>' % (t('Пакет', 'Package'), ''.join('<th scope="col">%s</th>' % s[1 + i] for s in SIZES))
    body = ''.join('<tr><th scope="row">%s<small>%s</small></th>%s</tr>' % (p[5][i], hm(p[1]), ''.join('<td data-label="%s">%s</td>' % (SIZES[k][1 + i], money(v, p[3])) for k, v in enumerate(p[2]))) for p in PACKAGES)
    matrix = '<table class="plist matrix"><caption class="sr-only">%s</caption><thead>%s</thead><tbody>%s</tbody></table>' % (t('Цени по размер на автомобила', 'Prices by car size'), head, body)
    addon_rows = ''.join('<li><span>%s</span><b>%s</b></li>' % (a[2][i], money(a[1])) for a in ADDONS)
    size_html = ''.join('<label class="opt"><input type="radio" name="size" value="%s"%s><span><b>%s</b> <small>%s</small></span></label>' % (s[0], ' checked' if s[0] == 'm' else '', s[1 + i], s[3 + i]) for s in SIZES)
    pkg_html = ''.join('<label class="opt"><input type="radio" name="pkg" value="%s"%s><span><b>%s</b> <small>%s</small></span></label>' % (p[0], ' checked' if p[0] == 'full' else '', p[5][i], hm(p[1])) for p in PACKAGES)
    addon_html = ''.join('<label class="opt"><input type="checkbox" name="addon" value="%s"><span>%s <small>+%s</small></span></label>' % (a[0], a[2][i], money(a[1])) for a in ADDONS)
    make_opts = '<option value="">%s</option>' % t('Избери марка', 'Choose a make') + ''.join('<option>%s</option>' % m for m in MAKES) + '<option value="other">%s</option>' % t('Друга', 'Other')
    steps = [(t('Приемане', 'Drop-off'), t('Оглеждаме колата заедно и записваме състоянието на боята.', 'We inspect the car together and note the condition of the paint.')), (t('Работа', 'The work'), t('Правим всичко на ръка, на закрито, с чисти кърпи за всяка кола.', 'We do it all by hand, indoors, with clean cloths for every car.')),
             (t('Проверка', 'Check'), t('Преди да ти се обадим, проверяваме всеки панел на светло.', 'Before we call you, we check every panel in good light.')), (t('Предаване', 'Hand-over'), t('Показваме какво е направено и как да го пазиш.', 'We show you what was done and how to look after it.'))]
    steps_html = ''.join('<li><b>%d</b><h3>%s</h3><p>%s</p></li>' % (n + 1, a, b) for n, (a, b) in enumerate(steps))
    hours_rows = [(t('Понеделник – петък', 'Monday – Friday'), HOURS['weekday'], 'wd'), (t('Събота и неделя', 'Saturday and Sunday'), HOURS['weekend'], 'we')]
    hours_html = ''.join('<div data-hrs="%s"><dt>%s</dt><dd>%s – %s</dd></div>' % (k, n, h[0], h[1]) for n, h, k in hours_rows)
    hours_ld = '"Mo-Fr %s-%s","Sa-Su %s-%s"' % (HOURS['weekday'][0], HOURS['weekday'][1], HOURS['weekend'][0], HOURS['weekend'][1])
    swatches = ''.join('<button class="sw" type="button" data-skin="%s" style="--s1:%s;--s2:%s" aria-pressed="false" aria-label="%s"></button>' % (k, s1, s2, b if bg else e) for k, b, e, s1, s2 in SKINS)
    nav = [('#packages', t('Пакети', 'Packages')), ('#prices', t('Цени', 'Prices')), ('#process', t('Как работим', 'Process')), ('#gallery', t('Снимки', 'Photos')), ('#book', t('Запази час', 'Book')), ('#visit', t('Контакти', 'Contact'))]
    nav_html = ''.join('<a href="%s">%s</a>' % n for n in nav)
    data = {'addon': ADDON_MINUTES, 'sizes': [s[0] for s in SIZES], 'sizeNames': {s[0]: s[1 + i] for s in SIZES},
            'packages': {p[0]: {'min': p[1], 'prices': list(p[2]), 'from': p[3], 'name': p[5][i]} for p in PACKAGES}, 'addons': {a[0]: {'price': a[1], 'name': a[2][i]} for a in ADDONS}}

    title = t('Kristal – детайлинг студио в Пловдив. Измиване, полиране и керамично покритие', 'Kristal – a car detailing studio in Plovdiv. Washing, polishing and ceramic coating')
    desc = t('Kristal е детайлинг студио в Пловдив: външно и вътрешно почистване, полиране на боята и керамично покритие. Виж цените по размер на колата и запази час.',
             'Kristal is a detailing studio in Plovdiv: exterior and interior cleaning, paint correction and ceramic coating. See the prices by car size and book a time.')

    return '''<!doctype html>
<html lang="%(lang)s" data-skin="graphite">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="theme-color" content="#F2F3F4">
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
     and an og:image (images/stock/sedan-dark.jpg is a placeholder) -->
<link rel="preload" href="%(root)sfonts/onest-%(script)s.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="%(root)sfonts/unbounded-%(script)s.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="%(root)sfonts/fonts.css">
<link rel="stylesheet" href="%(root)scss/style.css">
<script>
  /* Apply the saved colour scheme before the page paints, so it does not flash. */
  try { var s = new URLSearchParams(location.search).get("skin") || localStorage.getItem("kristalSkin"); if (s) document.documentElement.dataset.skin = s; } catch (e) {}
</script>
<script type="application/ld+json">
{"@context":"https://schema.org","@type":"AutoRepair","name":"%(brand)s","description":"Car detailing studio","inLanguage":"%(lang)s","telephone":"%(phone_href)s","email":"%(email)s",
 "address":{"@type":"PostalAddress","streetAddress":"Primer St. 70","addressLocality":"Plovdiv","addressCountry":"BG"},"openingHours":[%(hours_ld)s]}
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
      <p class="hero-links"><a class="btn btn-main" href="#book">%(cta1)s</a> <a class="btn btn-light" href="#prices">%(cta2)s</a></p>
    </div>
  </section>
  <div class="info-bar">
    <ul class="wrap info-row">
      <li><b>%(ib1_k)s</b> <span id="todayHours">08:00 – 18:00</span></li>
      <li><b>%(ib2_k)s</b> <span>%(address)s</span></li>
      <li><b>%(ib3_k)s</b> <span>%(ib3_v)s</span></li>
    </ul>
  </div>

  <!-- ============ Packages ============ -->
  <section class="block" id="packages" aria-labelledby="pk-h">
    <div class="wrap">
      <header class="sec-head">
        <h2 id="pk-h">%(pk_h)s</h2>
        <p>%(pk_p)s</p>
      </header>
      <ul class="pks">%(cards)s</ul>
    </div>
  </section>

  <!-- ============ Prices ============ -->
  <section class="block soft" id="prices" aria-labelledby="pr-h">
    <div class="wrap">
      <header class="sec-head">
        <h2 id="pr-h">%(pr_h)s</h2>
        <p>%(pr_p)s</p>
      </header>
      <div class="pr-grid">
        <div class="mx-wrap">%(matrix)s</div>
        <div class="addons"><h3>%(ad_h)s</h3><ul>%(addon_rows)s</ul></div>
      </div>
      <p class="p-note pr-note">%(pr_note)s</p>
    </div>
  </section>

  <!-- ============ Process ============ -->
  <section class="block" id="process" aria-labelledby="pc-h">
    <div class="wrap">
      <header class="sec-head"><h2 id="pc-h">%(pc_h)s</h2><p>%(pc_p)s</p></header>
      <ol class="steps4">%(steps_html)s</ol>
    </div>
  </section>

  <!-- ============ Photos ============ -->
  <section class="block soft" id="gallery" aria-labelledby="gl-h">
    <div class="wrap">
      <header class="sec-head"><h2 id="gl-h">%(gl_h)s</h2></header>
      <div class="gallery">
        <figure>%(g1)s</figure><figure>%(g2)s</figure><figure>%(g3)s</figure><figure>%(g4)s</figure>
        <figure>%(g5)s</figure><figure>%(g6)s</figure><figure>%(g7)s</figure><figure>%(g8)s</figure>
      </div>
    </div>
  </section>

  <!-- ============ Book ============ -->
  <section class="block" id="book" aria-labelledby="bk-h">
    <div class="wrap narrow">
      <header class="sec-head">
        <h2 id="bk-h">%(bk_h)s</h2>
        <p>%(bk_p)s</p>
      </header>
      <form class="res" id="bookForm" novalidate>
        <div class="row2">
          <div class="field"><label for="f-make">%(f_make)s</label><select id="f-make" name="make">%(make_opts)s</select></div>
          <div class="field"><label for="f-model">%(f_model)s</label><input id="f-model" name="model" type="text" autocomplete="off"></div>
        </div>
        <fieldset class="group"><legend>%(f_size)s</legend><div class="opts">%(size_html)s</div></fieldset>
        <fieldset class="group"><legend>%(f_pkg)s</legend><div class="opts">%(pkg_html)s</div></fieldset>
        <fieldset class="group"><legend>%(f_addon)s</legend><div class="opts">%(addon_html)s</div></fieldset>
        <p class="est" id="est" role="status"></p>
        <div class="row2">
          <div class="field"><label for="f-date">%(f_date)s</label><input id="f-date" name="date" type="date" required></div>
          <div class="field"><label for="f-time">%(f_time)s</label><select id="f-time" name="time" required></select></div>
        </div>
        <p class="hint" id="timeHint" role="status">%(checking)s</p>
        <div class="row2">
          <div class="field"><label for="f-name">%(f_name)s</label><input id="f-name" name="name" type="text" autocomplete="name" required></div>
          <div class="field"><label for="f-phone">%(f_phone)s</label><input id="f-phone" name="phone" type="tel" autocomplete="tel" required></div>
        </div>
        <div class="field"><label for="f-msg">%(f_msg)s</label><textarea id="f-msg" name="msg" rows="3"></textarea></div>
        <p class="demo-note" id="demoNote" hidden></p>
        <p class="form-error" id="bError" role="alert" hidden></p>
        <button class="btn btn-main" type="submit" id="bSend">%(f_send)s</button>
        <small class="fine">%(f_note)s <a href="%(privacy_href)s">%(f_priv)s</a></small>
      </form>
      <div class="done" id="bDone" hidden tabindex="-1"></div>
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
    <span>© <span id="year">2026</span> Kristal. %(foot_demo)s</span>
    <span class="foot-links"><a href="%(privacy_href)s">%(f_priv)s</a> <a href="%(admin_href)s">%(admin_l)s</a></span>
  </div>
</footer>

<aside class="dock" aria-label="%(dock_label)s">
  <div class="dock-label"><small>%(dock_label)s</small><b id="skinName">%(skin_name)s</b></div>
  <div class="swatches">%(swatches)s</div>
</aside>

<script type="application/json" id="kristalData">%(data)s</script>
<script src="%(root)sjs/config.js"></script>
<script src="%(root)sjs/api.js"></script>
<script src="%(root)sjs/main.js"></script>
</body>
</html>
''' % dict(
        lang=lang, title=esc(title), desc=esc(desc), root=root, script=script, brand=BRAND, phone_href=PHONE_HREF, phone=PHONE, email=EMAIL, hours_ld=hours_ld,
        skip=t('Към съдържанието', 'Skip to content'), nav_label=t('Навигация', 'Navigation'), nav_html=nav_html, call_l=t('Обади се', 'Call'),
        other_href=other_href, other_lang='en' if bg else 'bg', other_label='EN' if bg else 'БГ', other_aria='Switch to English' if bg else 'Превключи на български', menu_btn=t('Меню', 'Menu'),
        hero_img=I('sedan-dark', t('Черен седан в тъмно студио с отражения по каросерията', 'A black saloon in a dark studio with reflections on the body'), '100vw', eager=True),
        eyebrow=t('Детайлинг студио · Пловдив', 'Detailing studio · Plovdiv'), h1=t('Колата ти, като нова', 'Your car, like new'),
        lead=t('Ръчно измиване, полиране на боята и керамично покритие. Цената зависи от размера на колата и я виждаш предварително.', 'Hand washing, paint correction and ceramic coating. The price depends on the size of the car and you see it beforehand.'),
        cta1=t('Запази час', 'Book a time'), cta2=t('Виж цените', 'See the prices'),
        ib1_k=t('Днес', 'Today'), ib2_k=t('Адрес', 'Address'), address=ADDRESS['bg' if bg else 'en'], ib3_k=t('Приемане', 'Drop-off'), ib3_v=t('Оставяш колата сутрин, взимаш я следобед.', 'Leave the car in the morning, collect it in the afternoon.'),
        pk_h=t('Пакети', 'Packages'), pk_p=t('Пет пакета, от бързо измиване до защита за три години. Не знаеш кой ти трябва? Обади се и ще те посъветваме.', 'Five packages, from a quick wash to three years of protection. Not sure which one you need? Call us and we will advise you.'), cards=cards,
        pr_h=t('Цени по размер на колата', 'Prices by car size'), pr_p=t('Цените са в евро, с ДДС. „От“ означава, че точната цена зависи от състоянието на боята и я казваме след оглед.', 'Prices are in euros, including VAT. “From” means the exact price depends on the condition of the paint and we tell you after an inspection.'),
        matrix=matrix, ad_h=t('Допълнения', 'Add-ons'), addon_rows=addon_rows, pr_note=t('За мръсни автомобили, косми или петна може да има доплащане. Казваме го преди да започнем.', 'Very dirty cars, hair or stains may cost extra. We tell you before we start.'),
        pc_h=t('Как работим', 'How we work'), pc_p=t('Малък екип и една кола наведнъж в бокса.', 'A small team and one car at a time in the bay.'), steps_html=steps_html,
        gl_h=t('Снимки от студиото', 'Photos from the studio'),
        g1=I('polish-light', t('Полиране на фар с машина', 'Polishing a headlight with a machine'), '(min-width: 900px) 260px, 45vw'), g2=I('foam-sports', t('Спортен автомобил, покрит с пяна', 'A sports car covered in foam'), '(min-width: 900px) 260px, 45vw'), g3=I('wheel-wash', t('Измиване на джанта с четка', 'Washing a wheel with a brush'), '(min-width: 900px) 260px, 45vw'), g4=I('dashboard', t('Почистване на табло с четка', 'Cleaning a dashboard with a brush'), '(min-width: 900px) 260px, 45vw'),
        g5=I('wash-coupe', t('Измиване на черно купе до тухлена сграда', 'Washing a black coupe beside a brick building'), '(min-width: 900px) 260px, 45vw'), g6=I('tyre-brush', t('Почистване на гума с четка и ръкавици', 'Cleaning a tyre with a brush and gloves'), '(min-width: 900px) 260px, 45vw'), g7=I('blue-foam', t('Син автомобил, измит с пяна', 'A blue car washed with foam'), '(min-width: 900px) 260px, 45vw'), g8=I('sponge', t('Ръчно измиване с гъба', 'Hand washing with a sponge'), '(min-width: 900px) 260px, 45vw'),
        bk_h=t('Запази час за колата', 'Book your car in'), bk_p=t('Избери размер и пакет. Виждаш ориентировъчна цена и колко време ще отнеме. Ще ти се обадим, ако трябва да променим нещо.', 'Choose the size and the package. You see an estimated price and how long it will take. We will call you if something has to change.'),
        f_make=t('Марка', 'Make'), make_opts=make_opts, f_model=t('Модел', 'Model'), f_size=t('Размер на колата', 'Size of the car'), size_html=size_html, f_pkg=t('Пакет', 'Package'), pkg_html=pkg_html, f_addon=t('Допълнения (по желание)', 'Add-ons (optional)'), addon_html=addon_html,
        f_date=t('Дата', 'Date'), f_time=t('Час за приемане', 'Drop-off time'), checking=t('Избери дата, за да видиш свободните часове.', 'Choose a date to see the free times.'),
        f_name=t('Име', 'Name'), f_phone=t('Телефон', 'Phone'), f_msg=t('Бележка (по желание)', 'Note (optional)'),
        f_send=t('Изпрати заявката', 'Send the request'), f_note=t('Плащаш при получаване на колата.', 'You pay when you collect the car.'), f_priv=t('Поверителност', 'Privacy'), privacy_href='privacy.html',
        visit_h=t('Контакти', 'Contact'), hours_html=hours_html, l_addr=t('Адрес', 'Address'), l_phone=t('Телефон', 'Phone'), l_email=t('Имейл', 'Email'),
        visit_note=t('Работим само със записан час, за да можем да отделим цялото време на твоята кола.', 'We work by appointment only, so we can give your car our full attention.'),
        map_t=t('Картата се зарежда от OpenStreetMap едва когато я поискаш.', 'The map loads from OpenStreetMap only when you ask for it.'), map_btn=t('Покажи картата', 'Show the map'),
        foot_demo=t('Всичко тук е пример.', 'Everything here is an example.'), admin_href='admin.html' if bg else '../admin.html?lang=en', admin_l=t('Демо админ панел', 'Demo back office'),
        dock_label=t('Цветова схема', 'Colour scheme'), skin_name=t('Графит', 'Graphite'), swatches=swatches,
        data=json.dumps(data, ensure_ascii=False).replace('</', '<\\/'),
    )


def main():
    cfg = ('/* Generated by tools/build_pages.py. Edit the values at the top of that file, then run it again. */\n'
           'window.KRISTAL_CONFIG = {\n  mode: "demo",            /* "demo" = requests are kept in this browser only; "live" = real API at apiBase (docs/API.md) */\n'
           '  apiBase: "/api",\n  hours: { weekday: ["%s", "%s"], weekend: ["%s", "%s"] },\n  capacity: %d,             /* cars worked on at the same time (bays) */\n'
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
