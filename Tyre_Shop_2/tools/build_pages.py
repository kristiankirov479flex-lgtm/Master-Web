"""Builds index.html (Bulgarian), en/index.html (English), js/config.js and css/style.css for Stoyanov Tyres (a family tyre workshop).
Edit the values in this file (prices, hours, texts), then run:  python tools/build_pages.py && python tools/build_privacy.py
Everything about the workshop is an example: replace it for a real workshop."""
import json, os
from html import escape as esc
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BRAND = 'Stoyanov Tyres'

# ---------------- settings you will change for a real workshop ----------------
HOURS = {'weekday': ['08:00', '18:00'], 'weekend': ['08:00', '14:00']}
CAPACITY = 2          # cars handled at the same time
SLOT_MINUTES = 30
LEAD_MINUTES = 30
VISIT_MINUTES = 45
PHONE, PHONE_HREF, EMAIL = '+359 88 000 0000', '+359880000000', 'info@example.com'
ADDRESS = {'bg': 'ул. Примерна 40, Пловдив', 'en': '40 Primer St., Plovdiv'}
MAKES = ['Audi', 'BMW', 'Citroën', 'Dacia', 'Fiat', 'Ford', 'Honda', 'Hyundai', 'Kia', 'Mazda', 'Mercedes-Benz', 'Nissan', 'Opel', 'Peugeot', 'Renault', 'Seat', 'Škoda', 'Toyota', 'Volkswagen', 'Volvo']

# price list: (bg name, en name, bg note, en note, price in euro or None for "free")
SERVICES = [
 ('Ремонт на спукана гума', 'Puncture repair', 'Без записване, около 20 минути', 'No booking, about 20 minutes', 10),
 ('Преместване на колелата на колата', 'Swapping wheels on the car', 'Колелата вече са на джанти', 'Wheels already on rims', 14),
 ('Баланс на едно колело', 'Balancing one wheel', '', '', 5),
 ('Сходимост', 'Wheel alignment', 'Компютърна', 'Computer alignment', 35),
 ('Съхранение на комплект гуми', 'Storing a set of tyres', 'За един сезон', 'For one season', 25),
 ('Вентил', 'Valve', 'Гумен, за едно колело', 'Rubber, per wheel', 1.5),
 ('Проверка на налягане и протектор', 'Pressure and tread check', 'Винаги безплатно', 'Always free', None),
]
# changing tyres on rims, 4 wheels, with balancing: (bg rim, en rim, price)
CHANGE = [('до 15″', 'up to 15″', 24), ('16″', '16″', 28), ('17″', '17″', 34), ('18″', '18″', 40), ('19″ и повече', '19″ and up', 48)]
# kinds of new tyres: (id, bg title, en title, bg text, en text, photo, price for a typical 16″ tyre)
KINDS = [('budget', 'Икономични', 'Budget', 'За малко километри и градско шофиране. Добра цена и достатъчно сцепление.', 'For low mileage and town driving. A good price and enough grip.', 'tyre-pile', 55),
         ('mid', 'Средна класа', 'Mid-range', 'Най-често избираните. Тихи, дълготрайни и с добро сцепление на мокро.', 'The most popular choice. Quiet, long-lasting and good on wet roads.', 'tread', 80),
         ('premium', 'Премиум', 'Premium', 'Най-къс спирачен път и най-дълъг живот. Струват повече, но се връщат.', 'The shortest braking and the longest life. They cost more but pay back.', 'tyre-stack', 120)]

SKINS = [('blue', 'Синьо', 'Blue', '#F5F7FA', '#0B5CAD'), ('red', 'Червено', 'Red', '#FAF5F4', '#B3261E'), ('green', 'Зелено', 'Green', '#F3F7F3', '#1F6B3A'),
         ('graphite', 'Графит', 'Graphite', '#17191C', '#F0B429'), ('amber', 'Кехлибар', 'Amber', '#FBF6F0', '#A04A07')]


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
        if v is None:
            return t('безплатно', 'free')
        s = ('%.2f' % v) if v % 1 else ('%d' % v)
        return (s.replace('.', ',') + ' €') if bg else ('€' + s)

    rows = ''.join('<tr><th scope="row">%s%s</th><td>%s</td></tr>' % (esc(s[i]), ('<small>%s</small>' % esc(s[2 + i])) if s[2 + i] else '', money(s[4])) for s in SERVICES)
    change_rows = ''.join('<tr><th scope="row">%s</th><td>%s</td></tr>' % (c[i], money(c[2])) for c in CHANGE)
    kinds = ''.join('<li><figure>%s</figure><div><h3>%s</h3><p>%s</p><p class="k-price">%s <b>%s</b></p></div></li>'
                    % (I(k[5], k[1 + i], '(min-width: 1140px) 352px, (min-width: 860px) calc((100vw - 80px) / 3), calc(100vw - 40px)'), k[1 + i], k[3 + i], t('Типична цена на гума 16″:', 'Typical price per 16″ tyre:'), t('от ', 'from ') + money(k[6])) for k in KINDS)
    make_opts = '<option value="">%s</option>' % t('Избери марка', 'Choose a make') + ''.join('<option>%s</option>' % m for m in MAKES) + '<option value="other">%s</option>' % t('Друга', 'Other')
    seasons = [('summer', 'Летни', 'Summer'), ('winter', 'Зимни', 'Winter'), ('all', 'Всесезонни', 'All-season'), ('unsure', 'Не съм сигурен', 'Not sure')]
    budgets = [('budget', 'Икономични', 'Budget'), ('mid', 'Средна класа', 'Mid-range'), ('premium', 'Премиум', 'Premium'), ('unsure', 'Не съм сигурен', 'Not sure')]
    season_html = ''.join('<label class="opt"><input type="radio" name="season" value="%s"%s><span>%s</span></label>' % (k, ' checked' if k == 'unsure' else '', b if bg else e) for k, b, e in seasons)
    budget_html = ''.join('<label class="opt"><input type="radio" name="budget" value="%s"%s><span>%s</span></label>' % (k, ' checked' if k == 'unsure' else '', b if bg else e) for k, b, e in budgets)
    hours_rows = [(t('Понеделник – петък', 'Monday – Friday'), HOURS['weekday'], 'wd'), (t('Събота и неделя', 'Saturday and Sunday'), HOURS['weekend'], 'we')]
    hours_html = ''.join('<div data-hrs="%s"><dt>%s</dt><dd>%s – %s</dd></div>' % (k, n, h[0], h[1]) for n, h, k in hours_rows)
    hours_ld = '"Mo-Fr %s-%s","Sa-Su %s-%s"' % (HOURS['weekday'][0], HOURS['weekday'][1], HOURS['weekend'][0], HOURS['weekend'][1])
    swatches = ''.join('<button class="sw" type="button" data-skin="%s" style="--s1:%s;--s2:%s" aria-pressed="false" aria-label="%s"></button>' % (k, s1, s2, b if bg else e) for k, b, e, s1, s2 in SKINS)
    nav = [('#prices', t('Цени', 'Prices')), ('#tyres', t('Нови гуми', 'New tyres')), ('#season', t('Кога', 'When')), ('#quote', t('Поискай цена', 'Ask for a price')), ('#visit', t('Контакти', 'Contact'))]
    nav_html = ''.join('<a href="%s">%s</a>' % n for n in nav)
    data = {'visit': VISIT_MINUTES, 'makes': {}, 'seasons': {k: (b if bg else e) for k, b, e in seasons}, 'budgets': {k: (b if bg else e) for k, b, e in budgets}}

    title = t('Stoyanov Tyres – гуми и сервиз в Пловдив. Ремонт, смяна и нови гуми', 'Stoyanov Tyres – tyres and service in Plovdiv. Repairs, changes and new tyres')
    desc = t('Семеен гумаджийски сервиз в Пловдив. Ремонт на гуми без записване, смяна и баланс, сходимост, съхранение и нови гуми. Виж цените и поискай оферта.',
             'A family tyre workshop in Plovdiv. Puncture repair without booking, tyre changes and balancing, alignment, storage and new tyres. See the prices and ask for a quote.')

    return '''<!doctype html>
<html lang="%(lang)s" data-skin="blue">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="theme-color" content="#F5F7FA">
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
     and an og:image (images/stock/workshop-bright.jpg is a placeholder) -->
<link rel="preload" href="%(root)sfonts/onest-%(script)s.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="%(root)sfonts/nunito-%(script)s.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="%(root)sfonts/fonts.css">
<link rel="stylesheet" href="%(root)scss/style.css">
<script>
  /* Apply the saved colour scheme before the page paints, so it does not flash. */
  try { var s = new URLSearchParams(location.search).get("skin") || localStorage.getItem("stoyanovSkin"); if (s) document.documentElement.dataset.skin = s; } catch (e) {}
</script>
<script type="application/ld+json">
{"@context":"https://schema.org","@type":"AutoRepair","name":"%(brand)s","inLanguage":"%(lang)s","telephone":"%(phone_href)s","email":"%(email)s",
 "address":{"@type":"PostalAddress","streetAddress":"Primer St. 40","addressLocality":"Plovdiv","addressCountry":"BG"},"openingHours":[%(hours_ld)s]}
</script>
</head>
<body>
<a class="skip" href="#main">%(skip)s</a>

<header class="top" id="top">
  <div class="top-in">
    <a class="logo" href="index.html">%(brand_html)s</a>
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
      <div class="hero-card">
        <h1 id="h1">%(h1)s</h1>
        <ul class="hero-list"><li>%(hl1)s</li><li>%(hl2)s</li><li>%(hl3)s</li></ul>
        <p class="hero-links"><a class="btn btn-main" href="tel:%(phone_href)s">%(cta1)s</a> <a class="btn btn-line" href="#quote">%(cta2)s</a></p>
      </div>
    </div>
  </section>
  <div class="info-bar">
    <ul class="wrap info-row">
      <li><b>%(ib1_k)s</b> <span id="todayHours">08:00 – 18:00</span></li>
      <li><b>%(ib2_k)s</b> <span>%(address)s</span></li>
      <li><b>%(ib3_k)s</b> <span>%(ib3_v)s</span></li>
    </ul>
  </div>

  <!-- ============ Prices ============ -->
  <section class="block" id="prices" aria-labelledby="pr-h">
    <div class="wrap prices">
      <header class="sec-head">
        <h2 id="pr-h">%(prices_h)s</h2>
        <p>%(prices_p)s</p>
        <figure class="pr-ph">%(pr_img)s</figure>
      </header>
      <div class="tables">
        <table class="plist">
          <caption>%(cap1)s</caption>
          <tbody>%(rows)s</tbody>
        </table>
        <table class="plist">
          <caption>%(cap2)s</caption>
          <tbody>%(change_rows)s</tbody>
        </table>
        <p class="p-note">%(p_note)s</p>
      </div>
    </div>
  </section>

  <!-- ============ New tyres ============ -->
  <section class="block soft" id="tyres" aria-labelledby="ty-h">
    <div class="wrap">
      <header class="sec-head">
        <h2 id="ty-h">%(tyres_h)s</h2>
        <p>%(tyres_p)s</p>
      </header>
      <ul class="kinds">%(kinds)s</ul>
      <p class="p-note">%(kinds_note)s</p>
    </div>
  </section>

  <!-- ============ When to change ============ -->
  <section class="block" id="season" aria-labelledby="se-h">
    <div class="wrap season">
      <div class="season-text">
        <h2 id="se-h">%(season_h)s</h2>
        <p>%(season_p1)s</p>
        <p>%(season_p2)s</p>
        <h3>%(read_h)s</h3>
        <p>%(read_p)s</p>
        <p class="sidewall-ex"><b>205 / 55 R 16</b> <span>%(read_ex)s</span></p>
      </div>
      <div class="season-ph">
        <figure>%(se_img1)s</figure>
        <figure>%(se_img2)s</figure>
      </div>
    </div>
  </section>

  <!-- ============ Ask for a price ============ -->
  <section class="block soft" id="quote" aria-labelledby="qu-h">
    <div class="wrap narrow">
      <header class="sec-head">
        <h2 id="qu-h">%(quote_h)s</h2>
        <p>%(quote_p)s</p>
      </header>
      <form class="res" id="quoteForm" novalidate>
        <div class="row2">
          <div class="field"><label for="f-make">%(f_make)s</label><select id="f-make" name="make">%(make_opts)s</select></div>
          <div class="field"><label for="f-model">%(f_model)s</label><input id="f-model" name="model" type="text" autocomplete="off"></div>
        </div>
        <div class="field"><label for="f-size">%(f_size)s</label><input id="f-size" name="size" type="text" autocomplete="off" placeholder="205/55 R16"><p class="hint">%(size_hint)s</p></div>
        <fieldset class="group"><legend>%(f_season)s</legend><div class="opts">%(season_html)s</div></fieldset>
        <fieldset class="group"><legend>%(f_budget)s</legend><div class="opts">%(budget_html)s</div></fieldset>
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
        <p class="form-error" id="qError" role="alert" hidden></p>
        <button class="btn btn-main" type="submit" id="qSend">%(f_send)s</button>
        <small class="fine">%(f_note)s <a href="%(privacy_href)s">%(f_priv)s</a></small>
      </form>
      <div class="done" id="qDone" hidden tabindex="-1"></div>
    </div>
  </section>

  <!-- ============ About ============ -->
  <section class="block" id="about" aria-labelledby="ab-h">
    <div class="wrap about">
      <div class="about-text">
        <h2 id="ab-h">%(about_h)s</h2>
        <p>%(about_p1)s</p>
        <p>%(about_p2)s</p>
      </div>
      <div class="about-ph">
        <figure>%(ab_img1)s</figure>
        <figure>%(ab_img2)s</figure>
        <figure>%(ab_img3)s</figure>
      </div>
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
    <span>© <span id="year">2026</span> Stoyanov Tyres. %(foot_demo)s</span>
    <span class="foot-links"><a href="%(privacy_href)s">%(f_priv)s</a> <a href="%(admin_href)s">%(admin_l)s</a></span>
  </div>
</footer>

<aside class="dock" aria-label="%(dock_label)s">
  <div class="dock-label"><small>%(dock_label)s</small><b id="skinName">%(skin_name)s</b></div>
  <div class="swatches">%(swatches)s</div>
</aside>

<script type="application/json" id="stoyData">%(data)s</script>
<script src="%(root)sjs/config.js"></script>
<script src="%(root)sjs/api.js"></script>
<script src="%(root)sjs/main.js"></script>
</body>
</html>
''' % dict(
        lang=lang, title=esc(title), desc=esc(desc), root=root, script=script, brand=BRAND, brand_html='Stoyanov <span>Tyres</span>', phone_href=PHONE_HREF, phone=PHONE, email=EMAIL, hours_ld=hours_ld,
        skip=t('Към съдържанието', 'Skip to content'), nav_label=t('Навигация', 'Navigation'), nav_html=nav_html, call_l=t('Обади се', 'Call'),
        other_href=other_href, other_lang='en' if bg else 'bg', other_label='EN' if bg else 'БГ', other_aria='Switch to English' if bg else 'Превключи на български', menu_btn=t('Меню', 'Menu'),
        hero_img=I('workshop-bright', t('Светъл сервиз с подемници и автомобили', 'A bright workshop with lifts and cars'), '100vw', eager=True),
        h1=t('Гуми, вулканизиране и сервиз в Пловдив', 'Tyres, puncture repair and wheel service in Plovdiv'),
        hl1=t('Ремонт на спукана гума без записване', 'Puncture repair without booking'), hl2=t('Смяна и баланс от 24 €', 'Tyre change and balancing from €24'), hl3=t('Съхраняваме гумите ви между сезоните', 'We store your tyres between seasons'),
        cta1=t('Обади се', 'Call us'), cta2=t('Поискай цена', 'Ask for a price'),
        ib1_k=t('Днес', 'Today'), ib2_k=t('Адрес', 'Address'), address=ADDRESS['bg' if bg else 'en'], ib3_k=t('Спукана гума?', 'Flat tyre?'), ib3_v=t('Просто елате, не е нужно да звъните.', 'Just drive in, no need to call first.'),
        prices_h=t('Ценоразпис', 'Price list'), prices_p=t('Цените са в евро, с ДДС. Важат за леки автомобили. За джипове и бусове цената е малко по-висока.', 'Prices are in euros, including VAT. They apply to cars. For SUVs and vans the price is a little higher.'),
        pr_img=I('impact-wrench', t('Пневматичен ключ на колело', 'An impact wrench on a wheel'), '(min-width: 900px) 460px, calc(100vw - 40px)'),
        cap1=t('Услуги', 'Services'), cap2=t('Смяна на гуми на джанти (4 колела, с баланс)', 'Changing tyres on rims (4 wheels, with balancing)'), rows=rows, change_rows=change_rows,
        p_note=t('Точната цена казваме, преди да започнем работа.', 'We tell you the exact price before we start work.'),
        tyres_h=t('Нови гуми', 'New tyres'), tyres_p=t('Продаваме гуми от три класа. Кажи ни колата и размера и ще предложим две-три възможности.', 'We sell tyres in three classes. Tell us the car and the size and we will suggest two or three options.'),
        kinds=kinds, kinds_note=t('Цените са за 16″ и се променят с размера и сезона. За точна цена поискай оферта по-долу.', 'Prices are for 16″ and change with size and season. For an exact price ask for a quote below.'),
        season_h=t('Кога се сменят гумите', 'When to change tyres'),
        season_p1=t('Зимните гуми се слагат, когато денонощната температура падне трайно под 7 °C, обикновено в края на октомври. Лятните се връщат през април.', 'Winter tyres go on when the temperature stays below 7 °C, usually in late October. Summer tyres come back in April.'),
        season_p2=t('Законовият минимум за протектора е 1,6 mm. Много шофьори сменят лятните гуми при 3 mm и зимните при 4 mm, защото сцеплението пада бързо.', 'The legal minimum tread is 1.6 mm. Many drivers replace summer tyres at 3 mm and winter tyres at 4 mm, because grip falls quickly.'),
        read_h=t('Как се чете размерът', 'How to read the size'), read_p=t('Размерът е написан отстрани на гумата: широчина в милиметри, профил в проценти и диаметър на джантата в инчове.', 'The size is printed on the side of the tyre: width in millimetres, profile in percent and rim diameter in inches.'),
        read_ex=t('широчина 205 mm, профил 55 %, джанта 16″', 'width 205 mm, profile 55%, rim 16″'),
        se_img1=I('car-snow-blue', t('Син автомобил под сняг', 'A blue car under snow'), '(min-width: 900px) 360px, calc(100vw - 40px)'), se_img2=I('winter-tyre', t('Зимна гума в снега', 'A winter tyre in the snow'), '(min-width: 900px) 360px, calc(100vw - 40px)'),
        quote_h=t('Поискай цена', 'Ask for a price'), quote_p=t('Кажи ни колата и размера. Ще ти се обадим с цена и ще предложим удобен час. Не е нужно да знаеш размера: напиши модела на колата.', 'Tell us the car and the size. We will call you with a price and suggest a convenient time. You do not need to know the size: write the car model.'),
        f_make=t('Марка', 'Make'), make_opts=make_opts, f_model=t('Модел', 'Model'), f_size=t('Размер на гумите (по желание)', 'Tyre size (optional)'), size_hint=t('Например 205/55 R16. Ако не го знаеш, остави празно.', 'For example 205/55 R16. If you do not know it, leave it empty.'),
        f_season=t('Какви гуми търсиш?', 'What tyres are you looking for?'), season_html=season_html, f_budget=t('Какъв клас?', 'Which class?'), budget_html=budget_html,
        f_date=t('Кога можеш да дойдеш?', 'When can you come?'), f_time=t('Час', 'Time'), checking=t('Избери дата, за да видиш свободните часове.', 'Choose a date to see the free times.'),
        f_name=t('Име', 'Name'), f_phone=t('Телефон', 'Phone'), f_msg=t('Бележка (по желание)', 'Note (optional)'),
        f_send=t('Изпрати заявката', 'Send the request'), f_note=t('Ще ти се обадим с цена. Плащаш на място.', 'We will call you with a price. You pay on site.'), f_priv=t('Поверителност', 'Privacy'), privacy_href='privacy.html',
        about_h=t('За сервиза', 'About the workshop'),
        about_p1=t('Семеен сервиз сме от 2008 година. Работим с гуми, джанти и баланс, а в натоварените седмици на смяната започваме по-рано.', 'We have been a family workshop since 2008. We work with tyres, rims and balancing, and in the busy weeks of the changeover we start earlier.'),
        about_p2=t('Не продаваме това, което не ти трябва. Ако гумата може да се ремонтира, ремонтираме я. Ако трябва да се смени, казваме защо.', 'We do not sell what you do not need. If a tyre can be repaired we repair it. If it has to be replaced we tell you why.'),
        ab_img1=I('hands-tyre', t('Ръце, които държат гума на колата', 'Hands holding a tyre on a car'), '(min-width: 900px) 220px, calc(33vw - 14px)'), ab_img2=I('lift-red', t('Автомобил на подемник', 'A car on a lift'), '(min-width: 900px) 220px, calc(33vw - 14px)'), ab_img3=I('workshop-cars', t('Автомобили в сервиза', 'Cars in the workshop'), '(min-width: 900px) 220px, calc(33vw - 14px)'),
        visit_h=t('Контакти', 'Contact'), hours_html=hours_html, l_addr=t('Адрес', 'Address'), l_phone=t('Телефон', 'Phone'), l_email=t('Имейл', 'Email'),
        visit_note=t('Паркирането пред сервиза е безплатно за клиенти.', 'Parking in front of the workshop is free for customers.'),
        map_t=t('Картата се зарежда от OpenStreetMap едва когато я поискаш.', 'The map loads from OpenStreetMap only when you ask for it.'), map_btn=t('Покажи картата', 'Show the map'),
        foot_demo=t('Всичко тук е пример.', 'Everything here is an example.'), admin_href='admin.html' if bg else '../admin.html?lang=en', admin_l=t('Демо админ панел', 'Demo back office'),
        dock_label=t('Цветова схема', 'Colour scheme'), skin_name=t('Синьо', 'Blue'), swatches=swatches,
        data=json.dumps(data, ensure_ascii=False).replace('</', '<\\/'),
    )


def main():
    cfg = ('/* Generated by tools/build_pages.py. Edit the values at the top of that file, then run it again. */\n'
           'window.STOYANOV_CONFIG = {\n  mode: "demo",            /* "demo" = requests are kept in this browser only; "live" = real API at apiBase (docs/API.md) */\n'
           '  apiBase: "/api",\n  hours: { weekday: ["%s", "%s"], weekend: ["%s", "%s"] },\n  capacity: %d,             /* cars handled at the same time */\n'
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
