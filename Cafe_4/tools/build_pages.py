"""Builds index.html (Bulgarian), en/index.html (English), js/config.js and css/style.css for Kettle & Co (a traditional coffee house).
Edit the values in this file (menu, prices, hours, texts), then run:  python tools/build_pages.py && python tools/build_privacy.py
Everything about the café is an example: replace it for a real café."""
import json, os
from html import escape as esc
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BRAND = 'Kettle & Co'

# ---------------- settings you will change for a real café ----------------
HOURS = {'weekday': ['07:30', '18:00'], 'weekend': ['08:00', '18:00']}
CAPACITY = 6          # tables that can be booked at the same time
SLOT_MINUTES = 30
LEAD_MINUTES = 60     # a same-day booking needs this much notice
BOOKING_MINUTES = 90
MAX_PARTY = 8
PHONE, PHONE_HREF, EMAIL = '+359 88 000 0000', '+359880000000', 'hello@example.com'
ADDRESS = {'bg': 'ул. Примерна 14, Пловдив', 'en': '14 Primer St., Plovdiv'}

# menu groups: (id, bg title, en title, note bg, note en, items); an item is (bg name, en name, bg text, en text, price)
MENU = [
 ('coffee', 'Кафе', 'Coffee', 'Овесено или соево мляко: +0,50 €', 'Oat or soya milk: +€0.50', [
  ('Еспресо', 'Espresso', '', '', 2.2), ('Двойно еспресо', 'Double espresso', '', '', 3.2), ('Американо', 'Americano', '', '', 2.8),
  ('Капучино', 'Cappuccino', '', '', 3.6), ('Флат уайт', 'Flat white', '', '', 4.0), ('Лате', 'Latte', '', '', 4.0),
  ('Филтър кафе', 'Filter coffee', 'Чаша от каната', 'A cup from the pot', 3.0), ('Виенско кафе', 'Viennese coffee', 'С разбита сметана', 'With whipped cream', 4.5)]),
 ('other', 'Чай и други напитки', 'Tea and other drinks', '', '', [
  ('Чай', 'Tea', 'Чайник за една чаша, няколко вида', 'A small pot, several kinds', 3.5), ('Топъл шоколад', 'Hot chocolate', '', '', 4.2),
  ('Пресен портокал', 'Fresh orange juice', '', '', 4.5), ('Домашна лимонада', 'Homemade lemonade', 'Лимон и мента', 'Lemon and mint', 3.8), ('Минерална вода', 'Mineral water', '0,5 л', '0.5 l', 2.0)]),
 ('cakes', 'Торти и сладки', 'Cakes and pastries', 'Всичко се прави тук, всяка сутрин', 'Everything is made here every morning', [
  ('Шоколадова торта', 'Chocolate cake', '', '', 5.5), ('Чийзкейк с горски плодове', 'Cheesecake with berries', '', '', 5.2), ('Ябълков щрудел', 'Apple strudel', 'Топъл, с ванилов сос', 'Warm, with vanilla sauce', 4.8),
  ('Орехова торта', 'Walnut cake', '', '', 5.0), ('Кроасан', 'Croissant', 'С масло, или с конфитюр', 'With butter, or with jam', 3.0)]),
 ('light', 'Закуска и лека храна', 'Breakfast and light lunch', 'Закуска до 11:00', 'Breakfast until 11:00', [
  ('Бъркани яйца на тост', 'Scrambled eggs on toast', '', '', 6.5), ('Баница с кисело мляко', 'Banitsa with yoghurt', '', '', 4.5), ('Тост с шунка и кашкавал', 'Ham and cheese toastie', '', '', 5.5),
  ('Супа на деня', 'Soup of the day', 'С хляб', 'With bread', 5.0), ('Салата с козе сирене', 'Goat cheese salad', '', '', 7.5)]),
]

SKINS = [('linen', 'Лен и зелено', 'Linen and green', '#FAF6EE', '#2F5D3A'), ('wine', 'Вино', 'Wine', '#FBF4F1', '#7A2434'),
         ('harbour', 'Пристанище', 'Harbour', '#F4F6F8', '#1F4468'), ('roast', 'Печено кафе', 'Dark roast', '#1C1612', '#D9B26B'),
         ('clay', 'Глина', 'Clay', '#F8EEE4', '#9A4426')]


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

    groups = []
    for gid, gb, ge, nb, ne, items in MENU:
        rows = ''.join('<li><div class="m-top"><h4>%s</h4><i aria-hidden="true"></i><b>%s</b></div>%s</li>'
                       % (esc(it[i]), money(it[4]), ('<p>%s</p>' % esc(it[2 + i])) if it[2 + i] else '') for it in items)
        note = (nb if bg else ne)
        groups.append('<section class="m-group" aria-labelledby="mg-%s"><h3 id="mg-%s">%s</h3>%s<ul class="m-list">%s</ul></section>'
                      % (gid, gid, gb if bg else ge, ('<p class="m-note">%s</p>' % esc(note)) if note else '', rows))
    menu_html = ''.join(groups)

    hours_rows = [(t('Понеделник – петък', 'Monday – Friday'), HOURS['weekday'], 'wd'), (t('Събота и неделя', 'Saturday and Sunday'), HOURS['weekend'], 'we')]
    hours_html = ''.join('<div data-hrs="%s"><dt>%s</dt><dd>%s – %s</dd></div>' % (k, n, h[0], h[1]) for n, h, k in hours_rows)
    hours_ld = '"Mo-Fr %s-%s","Sa-Su %s-%s"' % (HOURS['weekday'][0], HOURS['weekday'][1], HOURS['weekend'][0], HOURS['weekend'][1])
    swatches = ''.join('<button class="sw" type="button" data-skin="%s" style="--s1:%s;--s2:%s" aria-pressed="false" aria-label="%s"></button>' % (k, s1, s2, b if bg else e) for k, b, e, s1, s2 in SKINS)
    nav = [('#menu', t('Меню', 'Menu')), ('#about', t('За нас', 'About us')), ('#gallery', t('Снимки', 'Photos')), ('#reserve', t('Резервация', 'Reservations')), ('#visit', t('Адрес', 'Find us'))]
    nav_html = ''.join('<a href="%s">%s</a>' % n for n in nav)
    party_opts = ''.join('<option value="%d"%s>%s</option>' % (n, ' selected' if n == 2 else '', (str(n) + t(' души', ' people')) if n > 1 else t('1 човек', '1 person')) for n in range(1, MAX_PARTY + 1))
    data = {'maxParty': MAX_PARTY, 'booking': BOOKING_MINUTES}

    title = t('Kettle & Co – кафене в Пловдив. Кафе, торти и спокойна маса', 'Kettle & Co – coffee house in Plovdiv. Coffee, cake and a quiet table')
    desc = t('Kettle & Co е семейно кафене в Пловдив. Прясно кафе, домашни торти и закуска всеки ден от 7:30. Виж менюто и резервирай маса.',
             'Kettle & Co is a family-run coffee house in Plovdiv. Fresh coffee, home-baked cakes and breakfast every day from 7:30. See the menu and reserve a table.')

    return '''<!doctype html>
<html lang="%(lang)s" data-skin="linen">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="theme-color" content="#FAF6EE">
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
     and an og:image (images/stock/street.jpg is a placeholder) -->
<link rel="preload" href="%(root)sfonts/onest-%(script)s.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="%(root)sfonts/alegreya-%(script)s.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="%(root)sfonts/fonts.css">
<link rel="stylesheet" href="%(root)scss/style.css">
<script>
  /* Apply the saved colour scheme before the page paints, so it does not flash. */
  try { var s = new URLSearchParams(location.search).get("skin") || localStorage.getItem("kettleSkin"); if (s) document.documentElement.dataset.skin = s; } catch (e) {}
</script>
<script type="application/ld+json">
{"@context":"https://schema.org","@type":"CafeOrCoffeeShop","name":"%(brand)s","inLanguage":"%(lang)s","telephone":"%(phone_href)s","email":"%(email)s",
 "address":{"@type":"PostalAddress","streetAddress":"Primer St. 14","addressLocality":"Plovdiv","addressCountry":"BG"},
 "servesCuisine":"Coffee, cakes, breakfast","acceptsReservations":"True","openingHours":[%(hours_ld)s]}
</script>
</head>
<body>
<a class="skip" href="#main">%(skip)s</a>

<header class="top" id="top">
  <div class="top-in">
    <a class="logo" href="index.html">%(brand_html)s</a>
    <nav class="nav" id="nav" aria-label="%(nav_label)s">%(nav_html)s</nav>
    <div class="top-r">
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
      <li><b>%(ib1_k)s</b> <span id="todayHours">%(ib1_v)s</span></li>
      <li><b>%(ib2_k)s</b> <span>%(address)s</span></li>
      <li><b>%(ib3_k)s</b> <a href="tel:%(phone_href)s">%(phone)s</a></li>
    </ul>
  </div>

  <!-- ============ About ============ -->
  <section class="block" id="about" aria-labelledby="ab-h">
    <div class="wrap about">
      <div class="about-text">
        <h2 id="ab-h">%(about_h)s</h2>
        <p>%(about_p1)s</p>
        <p>%(about_p2)s</p>
        <ul class="ticks">
          <li>%(t1)s</li><li>%(t2)s</li><li>%(t3)s</li>
        </ul>
      </div>
      <figure class="about-ph">%(about_img)s</figure>
    </div>
  </section>

  <!-- ============ Menu ============ -->
  <section class="block soft" id="menu" aria-labelledby="mn-h">
    <div class="wrap">
      <header class="sec-head">
        <h2 id="mn-h">%(menu_h)s</h2>
        <p>%(menu_p)s</p>
      </header>
      <div class="menu-cols">%(menu_html)s</div>
      <div class="from-counter">
        <figure>%(fc1)s</figure><figure>%(fc2)s</figure><figure>%(fc3)s</figure>
      </div>
    </div>
  </section>

  <!-- ============ Photos ============ -->
  <section class="block" id="gallery" aria-labelledby="gl-h">
    <div class="wrap">
      <header class="sec-head">
        <h2 id="gl-h">%(gallery_h)s</h2>
        <p>%(gallery_p)s</p>
      </header>
      <div class="gallery">
        <figure>%(g1)s</figure><figure>%(g2)s</figure><figure>%(g3)s</figure>
        <figure>%(g4)s</figure><figure>%(g5)s</figure><figure>%(g6)s</figure>
      </div>
    </div>
  </section>

  <!-- ============ Reservations ============ -->
  <section class="block soft" id="reserve" aria-labelledby="rs-h">
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
  <section class="block" id="visit" aria-labelledby="vs-h">
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
    <span>© <span id="year">2026</span> Kettle &amp; Co. %(foot_demo)s</span>
    <span class="foot-links"><a href="%(privacy_href)s">%(f_priv)s</a> <a href="%(admin_href)s">%(admin_l)s</a></span>
  </div>
</footer>

<aside class="dock" aria-label="%(dock_label)s">
  <div class="dock-label"><small>%(dock_label)s</small><b id="skinName">%(skin_name)s</b></div>
  <div class="swatches">%(swatches)s</div>
</aside>

<script type="application/json" id="kettleData">%(data)s</script>
<script src="%(root)sjs/config.js"></script>
<script src="%(root)sjs/api.js"></script>
<script src="%(root)sjs/main.js"></script>
</body>
</html>
''' % dict(
        lang=lang, title=esc(title), desc=esc(desc), root=root, script=script, brand=BRAND, brand_html='Kettle <span>&amp;</span> Co', phone_href=PHONE_HREF, phone=PHONE, email=EMAIL, hours_ld=hours_ld,
        skip=t('Към съдържанието', 'Skip to content'), nav_label=t('Навигация', 'Navigation'), nav_html=nav_html,
        other_href=other_href, other_lang='en' if bg else 'bg', other_label='EN' if bg else 'БГ', other_aria='Switch to English' if bg else 'Превключи на български', menu_btn=t('Меню', 'Menu'),
        hero_img=I('street', t('Улица с маси на кафенето пред сградата и черна дъска с менюто', 'A street with the café tables in front of the building and a chalkboard menu'), '100vw', eager=True),
        eyebrow=t('Семейно кафене · Пловдив', 'Family-run coffee house · Plovdiv'),
        h1=t('Кафе, торта и спокойна маса', 'Coffee, cake and a quiet table'),
        lead=t('Отворено всеки ден от 7:30. Кафето е от пловдивска пържилня, а тортите правим тук.', 'Open every day from 7:30. The coffee comes from a Plovdiv roaster and we bake the cakes here.'),
        cta1=t('Виж менюто', 'See the menu'), cta2=t('Резервирай маса', 'Reserve a table'),
        ib1_k=t('Днес', 'Today'), ib1_v='07:30 – 18:00', ib2_k=t('Адрес', 'Address'), address=ADDRESS['bg' if bg else 'en'], ib3_k=t('Телефон', 'Phone'),
        about_h=t('За нас', 'About us'),
        about_p1=t('Отворихме кафенето преди единайсет години в къща на тиха уличка в Пловдив. Искахме място, където можеш да седнеш с вестник, с книга или просто с приятел и никой да не те пита дали ще поръчваш пак.', 'We opened the café eleven years ago in a house on a quiet Plovdiv street. We wanted a place where you can sit with a newspaper, a book or just a friend and nobody asks whether you will order again.'),
        about_p2=t('Всяка сутрин в шест започваме с тестото. Кафето купуваме от малка пържилня в града, а млякото и яйцата от стопанство в Родопите.', 'Every morning at six we start with the dough. We buy the coffee from a small roaster in the city, and the milk and eggs from a farm in the Rhodope mountains.'),
        t1=t('Торти и сладки, правени тук', 'Cakes and pastries baked here'), t2=t('Овесено и соево мляко срещу 0,50 €', 'Oat and soya milk for €0.50 extra'), t3=t('Кучета са добре дошли на терасата', 'Dogs are welcome on the terrace'),
        about_img=I('interior-sunny', t('Слънчева зала с дървени столове и маси', 'A sunny room with wooden chairs and tables'), '(min-width: 900px) 460px, calc(100vw - 40px)'),
        menu_h=t('Меню', 'Menu'), menu_p=t('Цените са в евро. Питай за алергени, ако имаш нужда.', 'Prices are in euros. Ask about allergens if you need to.'), menu_html=menu_html,
        fc1=I('cake-latte', t('Лате и парче торта', 'A latte and a slice of cake'), '(min-width: 900px) 370px, calc(100vw - 40px)'), fc2=I('flat-lay-cake', t('Кафе, парче торта и лайм върху маса', 'Coffee, a slice of cake and a lime on a table'), '(min-width: 900px) 370px, calc(100vw - 40px)'), fc3=I('cocoa-cake', t('Какао и парче торта върху дървена маса', 'Cocoa and a slice of cake on a wooden table'), '(min-width: 900px) 370px, calc(100vw - 40px)'),
        gallery_h=t('Нашето място', 'Our place'), gallery_p=t('Две зали, тераса и барът с кафе машината.', 'Two rooms, a terrace and the bar with the coffee machine.'),
        g1=I('interior-wood', t('Дървена ламперия и картини в малката зала', 'Wood panelling and pictures in the small room'), '(min-width: 900px) 370px, 45vw'), g2=I('interior-plants', t('Маса сред растения до прозорец', 'A table among plants by a window'), '(min-width: 900px) 370px, 45vw'), g3=I('interior-books', t('Етажерка с книги и малка маса', 'A shelf of books and a small table'), '(min-width: 900px) 370px, 45vw'),
        g4=I('terrace', t('Тераса с маси и чадъри', 'A terrace with tables and umbrellas'), '(min-width: 900px) 370px, 45vw'), g5=I('interior-grand', t('Голямата зала вечер', 'The large room in the evening'), '(min-width: 900px) 370px, 45vw'), g6=I('machine', t('Кафе машината на бара', 'The coffee machine at the bar'), '(min-width: 900px) 370px, 45vw'),
        res_h=t('Резервация на маса', 'Reserve a table'), res_p=t('Не е задължителна, но в събота и неделя сутрин е полезна. За повече от %d души ни се обадете.' % MAX_PARTY, 'Not required, but useful on Saturday and Sunday mornings. For more than %d people please call us.' % MAX_PARTY),
        f_people=t('Колко души', 'How many people'), party_opts=party_opts, f_date=t('Дата', 'Date'), f_time=t('Час', 'Time'), checking=t('Избери дата, за да видиш свободните часове.', 'Choose a date to see the free times.'),
        f_name=t('Име', 'Name'), f_phone=t('Телефон', 'Phone'), f_msg=t('Бележка (по желание)', 'Note (optional)'),
        f_send=t('Резервирай масата', 'Reserve the table'), f_note=t('Ще ти се обадим само ако трябва да променим нещо.', 'We only call you if something has to change.'), f_priv=t('Поверителност', 'Privacy'), privacy_href='privacy.html',
        visit_h=t('Намери ни', 'Find us'), hours_html=hours_html, l_addr=t('Адрес', 'Address'), l_phone=t('Телефон', 'Phone'), l_email=t('Имейл', 'Email'),
        visit_note=t('Има платено паркиране на съседната улица.', 'There is paid parking on the next street.'),
        visit_img=I('cheesecake-table', t('Маса с кафе, чийзкейк и ледено кафе до прозореца', 'A table with coffee, cheesecake and iced coffee by the window'), '(min-width: 900px) 520px, calc(100vw - 40px)'),
        map_t=t('Картата се зарежда от OpenStreetMap едва когато я поискаш.', 'The map loads from OpenStreetMap only when you ask for it.'), map_btn=t('Покажи картата', 'Show the map'),
        foot_demo=t('Всичко тук е пример.', 'Everything here is an example.'), admin_href='admin.html' if bg else '../admin.html?lang=en', admin_l=t('Демо админ панел', 'Demo back office'),
        dock_label=t('Цветова схема', 'Colour scheme'), skin_name=t('Лен и зелено', 'Linen and green'), swatches=swatches,
        data=json.dumps(data, ensure_ascii=False).replace('</', '<\\/'),
    )


def main():
    cfg = ('/* Generated by tools/build_pages.py. Edit the values at the top of that file, then run it again. */\n'
           'window.KETTLE_CONFIG = {\n  mode: "demo",            /* "demo" = requests are kept in this browser only; "live" = real API at apiBase (docs/API.md) */\n'
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
