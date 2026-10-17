"""Builds index.html (Bulgarian), en/index.html (English), js/config.js and css/style.css for Fornello (a classic pizzeria).
Edit the values in this file (menu, prices, hours, texts), then run:  python tools/build_pages.py && python tools/build_privacy.py
Everything about the pizzeria is an example: replace it for a real pizzeria."""
import json, os
from html import escape as esc
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BRAND = 'Fornello'

# ---------------- settings you will change for a real pizzeria ----------------
HOURS = {'weekday': ['12:00', '22:30'], 'weekend': ['12:00', '23:00']}
CAPACITY = 8          # tables that can be booked at the same time
SLOT_MINUTES = 30
LEAD_MINUTES = 45
BOOKING_MINUTES = 75
MAX_PARTY = 10
PHONE, PHONE_HREF, EMAIL = '+359 88 000 0000', '+359880000000', 'ciao@example.com'
ADDRESS = {'bg': 'ул. Примерна 16, Пловдив', 'en': '16 Primer St., Plovdiv'}
SIZES = ('25 cm', '32 cm', '42 cm')

# pizzas: (bg name, en name, bg ingredients, en ingredients, price small, medium, large, vegetarian)
PIZZAS = [
 ('Маргарита', 'Margherita', 'домати, моцарела, босилек', 'tomato, mozzarella, basil', 7.5, 9.5, 13.5, True),
 ('Пеперони', 'Pepperoni', 'домати, моцарела, пикантен салам', 'tomato, mozzarella, spicy salami', 9.0, 11.5, 16.0, False),
 ('Четири сирена', 'Four cheeses', 'моцарела, горгонзола, пармезан, кашкавал', 'mozzarella, gorgonzola, parmesan, kashkaval', 10.0, 13.0, 18.0, True),
 ('Капричоза', 'Capricciosa', 'шунка, гъби, артишок, маслини', 'ham, mushrooms, artichoke, olives', 10.0, 13.0, 18.0, False),
 ('Прошуто и гъби', 'Prosciutto and mushrooms', 'шунка, гъби, моцарела', 'ham, mushrooms, mozzarella', 9.5, 12.5, 17.0, False),
 ('Вегетариана', 'Vegetariana', 'чушки, гъби, царевица, лук, маслини', 'peppers, mushrooms, sweetcorn, onion, olives', 9.0, 11.5, 16.0, True),
 ('Дяволска', 'Diavola', 'лют пипер, салам, лук, моцарела', 'hot pepper, salami, onion, mozzarella', 9.5, 12.5, 17.0, False),
 ('Българска', 'Bulgarian', 'кашкавал, сирене, чушки, домати', 'kashkaval, white cheese, peppers, tomatoes', 9.0, 11.5, 16.0, True),
]
# other groups: (bg title, en title, items (bg, en, bg text, en text, price))
OTHER = [
 ('Паста', 'Pasta', [('Спагети карбонара', 'Spaghetti carbonara', 'пансета, яйце, пармезан', 'pancetta, egg, parmesan', 9.5), ('Лазаня', 'Lasagne', 'със сос болонезе и бешамел', 'with bolognese and béchamel', 10.0),
                     ('Пене арабиата', 'Penne arrabbiata', 'лют доматен сос', 'hot tomato sauce', 8.5), ('Ньоки с четири сирена', 'Gnocchi with four cheeses', '', '', 11.0)]),
 ('Салати', 'Salads', [('Капрезе', 'Caprese', 'домати, моцарела, босилек', 'tomato, mozzarella, basil', 8.0), ('Рукола', 'Rocket salad', 'пармезан и балсамов оцет', 'parmesan and balsamic', 8.0), ('Гръцка', 'Greek salad', '', '', 7.5)]),
 ('Десерти', 'Desserts', [('Тирамису', 'Tiramisu', '', '', 5.5), ('Панакота', 'Panna cotta', 'с горски плодове', 'with wild berries', 5.0), ('Сладолед', 'Gelato', 'две топки', 'two scoops', 4.0)]),
 ('Напитки', 'Drinks', [('Газирана напитка', 'Soft drink', '0,33 л', '0.33 l', 2.5), ('Бира', 'Beer', 'Местна, 0,5 л', 'Local, 0.5 l', 3.5), ('Вино на чаша', 'Wine by the glass', 'червено или бяло', 'red or white', 4.0), ('Еспресо', 'Espresso', '', '', 2.2)]),
]

SKINS = [('margherita', 'Маргарита', 'Margherita', '#FFF9F0', '#B3261E'), ('diavola', 'Дяволска', 'Diavola', '#FBF3EE', '#8F1D14'), ('basil', 'Босилек', 'Basil', '#F5F8F0', '#2E6B34'),
         ('oven', 'Пещ', 'Oven', '#1D1511', '#F08A3C'), ('napoli', 'Неапол', 'Napoli', '#F4F7FB', '#1E4E8C')]


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

    rows = ''.join('<tr><th scope="row">%s%s<small>%s</small></th><td>%s</td><td>%s</td><td>%s</td></tr>'
                   % (esc(p[i]), ' <span class="tag" title="%s">V</span>' % t('Вегетарианска', 'Vegetarian') if p[7] else '', esc(p[2 + i]), money(p[4]), money(p[5]), money(p[6])) for p in PIZZAS)
    pizza_table = '<table class="plist pz"><caption>%s</caption><thead><tr><th scope="col">%s</th><th scope="col">%s</th><th scope="col">%s</th><th scope="col">%s</th></tr></thead><tbody>%s</tbody></table>' % (
        t('Пици', 'Pizzas'), t('Пица', 'Pizza'), SIZES[0], SIZES[1], SIZES[2], rows)
    others = ''
    for gb, ge, items in OTHER:
        li = ''.join('<li><div class="m-top"><h4>%s</h4><i aria-hidden="true"></i><b>%s</b></div>%s</li>' % (esc(it[i]), money(it[4]), ('<p>%s</p>' % esc(it[2 + i])) if it[2 + i] else '') for it in items)
        others += '<section class="m-group"><h3>%s</h3><ul class="m-list">%s</ul></section>' % (gb if bg else ge, li)
    seat_html = ''.join('<label class="opt"><input type="radio" name="seat" value="%s"%s><span>%s</span></label>' % (k, ' checked' if k == 'any' else '', b if bg else e) for k, b, e in (('any', 'Без значение', 'No preference'), ('inside', 'Вътре', 'Inside'), ('outside', 'Навън', 'Outside')))
    party_opts = ''.join('<option value="%d"%s>%s</option>' % (n, ' selected' if n == 2 else '', (str(n) + t(' души', ' people')) if n > 1 else t('1 човек', '1 person')) for n in range(1, MAX_PARTY + 1))
    hours_rows = [(t('Понеделник – петък', 'Monday – Friday'), HOURS['weekday'], 'wd'), (t('Събота и неделя', 'Saturday and Sunday'), HOURS['weekend'], 'we')]
    hours_html = ''.join('<div data-hrs="%s"><dt>%s</dt><dd>%s – %s</dd></div>' % (k, n, h[0], h[1]) for n, h, k in hours_rows)
    hours_ld = '"Mo-Fr %s-%s","Sa-Su %s-%s"' % (HOURS['weekday'][0], HOURS['weekday'][1], HOURS['weekend'][0], HOURS['weekend'][1])
    swatches = ''.join('<button class="sw" type="button" data-skin="%s" style="--s1:%s;--s2:%s" aria-pressed="false" aria-label="%s"></button>' % (k, s1, s2, b if bg else e) for k, b, e, s1, s2 in SKINS)
    nav = [('#menu', t('Меню', 'Menu')), ('#oven', t('Нашата пещ', 'Our oven')), ('#reserve', t('Резервация', 'Reservations')), ('#visit', t('Адрес', 'Find us'))]
    nav_html = ''.join('<a href="%s">%s</a>' % n for n in nav)
    data = {'booking': BOOKING_MINUTES, 'seats': {k: (b if bg else e) for k, b, e in (('any', 'Без значение', 'No preference'), ('inside', 'Вътре', 'Inside'), ('outside', 'Навън', 'Outside'))}}

    title = t('Fornello – пицария с дървена пещ в Пловдив', 'Fornello – a wood-fired pizzeria in Plovdiv')
    desc = t('Fornello е пицария в Пловдив с дървена пещ и тесто, което втасва 48 часа. Виж менюто с цени за три размера и резервирай маса.',
             'Fornello is a pizzeria in Plovdiv with a wood-fired oven and dough that rests for 48 hours. See the menu with prices for three sizes and reserve a table.')

    return '''<!doctype html>
<html lang="%(lang)s" data-skin="margherita">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="theme-color" content="#FFF9F0">
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
     and an og:image (images/stock/oven-pizza.jpg is a placeholder) -->
<link rel="preload" href="%(root)sfonts/onest-%(script)s.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="%(root)sfonts/oswald-%(script)s.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="%(root)sfonts/fonts.css">
<link rel="stylesheet" href="%(root)scss/style.css">
<script>
  /* Apply the saved colour scheme before the page paints, so it does not flash. */
  try { var s = new URLSearchParams(location.search).get("skin") || localStorage.getItem("fornelloSkin"); if (s) document.documentElement.dataset.skin = s; } catch (e) {}
</script>
<script type="application/ld+json">
{"@context":"https://schema.org","@type":"Restaurant","name":"%(brand)s","inLanguage":"%(lang)s","telephone":"%(phone_href)s","email":"%(email)s",
 "address":{"@type":"PostalAddress","streetAddress":"Primer St. 16","addressLocality":"Plovdiv","addressCountry":"BG"},"servesCuisine":"Pizza, Italian","acceptsReservations":"True","openingHours":[%(hours_ld)s]}
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
      <p class="hero-links"><a class="btn btn-main" href="#menu">%(cta1)s</a> <a class="btn btn-light" href="#reserve">%(cta2)s</a></p>
    </div>
  </section>
  <div class="info-bar">
    <ul class="wrap info-row">
      <li><b>%(ib1_k)s</b> <span id="todayHours">12:00 – 22:30</span></li>
      <li><b>%(ib2_k)s</b> <span>%(address)s</span></li>
      <li><b>%(ib3_k)s</b> <span>%(ib3_v)s</span></li>
    </ul>
  </div>

  <!-- ============ Menu ============ -->
  <section class="block" id="menu" aria-labelledby="mn-h">
    <div class="wrap">
      <header class="sec-head">
        <h2 id="mn-h">%(menu_h)s</h2>
        <p>%(menu_p)s</p>
      </header>
      <div class="pz-wrap">%(pizza_table)s</div>
      <p class="p-note"><span class="tag">V</span> %(v)s</p>
      <div class="menu-cols">%(others)s</div>
      <div class="menu-ph"><figure>%(mp1)s</figure><figure>%(mp2)s</figure><figure>%(mp3)s</figure></div>
    </div>
  </section>

  <!-- ============ Our oven ============ -->
  <section class="block soft" id="oven" aria-labelledby="ov-h">
    <div class="wrap oven">
      <div class="oven-text">
        <h2 id="ov-h">%(oven_h)s</h2>
        <p>%(oven_p1)s</p>
        <p>%(oven_p2)s</p>
        <ul class="facts4"><li><b>48 %(h)s</b><span>%(f1)s</span></li><li><b>450 °C</b><span>%(f2)s</span></li><li><b>90 %(s)s</b><span>%(f3)s</span></li></ul>
      </div>
      <div class="oven-ph"><figure>%(o1)s</figure><figure>%(o2)s</figure></div>
    </div>
  </section>

  <!-- ============ Reservations ============ -->
  <section class="block" id="reserve" aria-labelledby="rs-h">
    <div class="wrap narrow">
      <header class="sec-head">
        <h2 id="rs-h">%(res_h)s</h2>
        <p>%(res_p)s</p>
      </header>
      <form class="res" id="resForm" novalidate>
        <div class="row3">
          <div class="field"><label for="f-people">%(f_people)s</label><select id="f-people" name="people">%(party_opts)s</select></div>
          <div class="field"><label for="f-date">%(f_date)s</label><input id="f-date" name="date" type="date" required></div>
          <div class="field"><label for="f-time">%(f_time)s</label><select id="f-time" name="time" required></select></div>
        </div>
        <p class="hint" id="timeHint" role="status">%(checking)s</p>
        <fieldset class="group"><legend>%(f_seat)s</legend><div class="opts">%(seat_html)s</div></fieldset>
        <div class="row2">
          <div class="field"><label for="f-name">%(f_name)s</label><input id="f-name" name="name" type="text" autocomplete="name" required></div>
          <div class="field"><label for="f-phone">%(f_phone)s</label><input id="f-phone" name="phone" type="tel" autocomplete="tel" required></div>
        </div>
        <div class="field"><label for="f-msg">%(f_msg)s</label><textarea id="f-msg" name="msg" rows="3"></textarea></div>
        <p class="demo-note" id="demoNote" hidden></p>
        <p class="form-error" id="resError" role="alert" hidden></p>
        <button class="btn btn-main" type="submit" id="resSend">%(f_send)s</button>
        <small class="fine">%(f_note)s <a href="%(privacy_href)s">%(f_priv)s</a></small>
      </form>
      <div class="done" id="resDone" hidden tabindex="-1"></div>
    </div>
  </section>

  <!-- ============ Find us ============ -->
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
    <span>© <span id="year">2026</span> Fornello. %(foot_demo)s</span>
    <span class="foot-links"><a href="%(privacy_href)s">%(f_priv)s</a> <a href="%(admin_href)s">%(admin_l)s</a></span>
  </div>
</footer>

<aside class="dock" aria-label="%(dock_label)s">
  <div class="dock-label"><small>%(dock_label)s</small><b id="skinName">%(skin_name)s</b></div>
  <div class="swatches">%(swatches)s</div>
</aside>

<script type="application/json" id="fornelloData">%(data)s</script>
<script src="%(root)sjs/config.js"></script>
<script src="%(root)sjs/api.js"></script>
<script src="%(root)sjs/main.js"></script>
</body>
</html>
''' % dict(
        lang=lang, title=esc(title), desc=esc(desc), root=root, script=script, brand=BRAND, phone_href=PHONE_HREF, phone=PHONE, email=EMAIL, hours_ld=hours_ld,
        skip=t('Към съдържанието', 'Skip to content'), nav_label=t('Навигация', 'Navigation'), nav_html=nav_html, call_l=t('Обади се', 'Call'),
        other_href=other_href, other_lang='en' if bg else 'bg', other_label='EN' if bg else 'БГ', other_aria='Switch to English' if bg else 'Превключи на български', menu_btn=t('Меню', 'Menu'),
        hero_img=I('oven-pizza', t('Пица, която излиза от дървена пещ с огън', 'A pizza coming out of a wood-fired oven with flames'), '100vw', eager=True),
        eyebrow=t('Пицария · Пловдив', 'Pizzeria · Plovdiv'), h1=t('Пица от дървена пещ', 'Pizza from a wood-fired oven'),
        lead=t('Тестото втасва 48 часа, а пицата се пече 90 секунди при 450 градуса. Хапни при нас или се обади за вземане.', 'The dough rests for 48 hours and the pizza bakes for 90 seconds at 450 degrees. Eat with us or call to collect.'),
        cta1=t('Виж менюто', 'See the menu'), cta2=t('Резервирай маса', 'Reserve a table'),
        ib1_k=t('Днес', 'Today'), ib2_k=t('Адрес', 'Address'), address=ADDRESS['bg' if bg else 'en'], ib3_k=t('За вкъщи', 'Takeaway'), ib3_v=t('Обади се и пицата е готова за 20 минути', 'Call us and the pizza is ready in 20 minutes'),
        menu_h=t('Меню', 'Menu'), menu_p=t('Три размера: малка 25 см, средна 32 см и голяма 42 см. Цените са в евро.', 'Three sizes: small 25 cm, medium 32 cm and large 42 cm. Prices are in euros.'), pizza_table=pizza_table, v=t('вегетарианска', 'vegetarian'), others=others,
        mp1=I('slice-pull', t('Парче пица с разтеглено сирене', 'A slice of pizza with stretching cheese'), '(min-width: 900px) 352px, calc(100vw - 40px)'), mp2=I('pizza-board', t('Пица върху дървена дъска', 'A pizza on a wooden board'), '(min-width: 900px) 352px, calc(100vw - 40px)'), mp3=I('slice-spatula', t('Парче пица, вдигнато с лопатка', 'A slice of pizza lifted with a spatula'), '(min-width: 900px) 352px, calc(100vw - 40px)'),
        oven_h=t('Нашата пещ', 'Our oven'), oven_p1=t('Пещта е зидана преди девет години и се пали всяка сутрин в десет. Печем на дъбови дърва, затова коричката е тънка и леко опушена.', 'The oven was built nine years ago and is lit every morning at ten. We bake on oak wood, so the crust is thin and lightly smoky.'),
        oven_p2=t('Тестото замесваме с малко мая и го оставяме да почива два дни. Така пицата е лека и не тежи.', 'We knead the dough with very little yeast and let it rest for two days. That keeps the pizza light.'),
        h=t('ч', 'h'), s=t('сек', 'sec'), f1=t('почива тестото', 'the dough rests'), f2=t('е пещта', 'is the oven'), f3=t('се пече пицата', 'the pizza bakes'),
        o1=I('dough', t('Ръце, които месят тесто', 'Hands kneading dough'), '(min-width: 900px) 360px, calc(100vw - 40px)'), o2=I('oven-fire', t('Огън в дървената пещ', 'Fire in the wood-fired oven'), '(min-width: 900px) 360px, calc(100vw - 40px)'),
        res_h=t('Резервация на маса', 'Reserve a table'), res_p=t('Приемаме и без резервация, но в петък и събота вечер е добре да запазиш маса. За повече от %d души ни се обади.' % MAX_PARTY, 'We also take walk-ins, but on Friday and Saturday evenings it is wise to book. For more than %d people please call us.' % MAX_PARTY),
        f_people=t('Колко души', 'How many people'), party_opts=party_opts, f_date=t('Дата', 'Date'), f_time=t('Час', 'Time'), checking=t('Избери дата, за да видиш свободните часове.', 'Choose a date to see the free times.'),
        f_seat=t('Къде да седнете', 'Where to sit'), seat_html=seat_html, f_name=t('Име', 'Name'), f_phone=t('Телефон', 'Phone'), f_msg=t('Бележка (по желание)', 'Note (optional)'),
        f_send=t('Резервирай масата', 'Reserve the table'), f_note=t('Ще ти се обадим само ако трябва да променим нещо.', 'We only call you if something has to change.'), f_priv=t('Поверителност', 'Privacy'), privacy_href='privacy.html',
        visit_h=t('Намери ни', 'Find us'), hours_html=hours_html, l_addr=t('Адрес', 'Address'), l_phone=t('Телефон', 'Phone'), l_email=t('Имейл', 'Email'),
        visit_note=t('Има безплатно паркиране зад сградата след 18:00.', 'There is free parking behind the building after 18:00.'),
        visit_img=I('street', t('Улица с маси на пицарията и червено-бели покривки', 'A street with the pizzeria tables and red and white tablecloths'), '(min-width: 900px) 360px, calc(100vw - 40px)'),
        map_t=t('Картата се зарежда от OpenStreetMap едва когато я поискаш.', 'The map loads from OpenStreetMap only when you ask for it.'), map_btn=t('Покажи картата', 'Show the map'),
        foot_demo=t('Всичко тук е пример.', 'Everything here is an example.'), admin_href='admin.html' if bg else '../admin.html?lang=en', admin_l=t('Демо админ панел', 'Demo back office'),
        dock_label=t('Цветова схема', 'Colour scheme'), skin_name=t('Маргарита', 'Margherita'), swatches=swatches,
        data=json.dumps(data, ensure_ascii=False).replace('</', '<\\/'),
    )


def main():
    cfg = ('/* Generated by tools/build_pages.py. Edit the values at the top of that file, then run it again. */\n'
           'window.FORNELLO_CONFIG = {\n  mode: "demo",            /* "demo" = requests are kept in this browser only; "live" = real API at apiBase (docs/API.md) */\n'
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
