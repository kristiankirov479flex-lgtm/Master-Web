"""Builds index.html (Bulgarian), en/index.html (English), js/config.js and css/style.css for Desk & Drip.
Edit the values in this file (zones, prices, hours, texts), then run:  python tools/build_pages.py && python tools/build_privacy.py
Everything about the café is an example: replace it for a real café."""
import json, os
from html import escape as esc
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BRAND = 'Desk & Drip'

# ---------------- settings you will change for a real café ----------------
HOURS = {'weekday': ['08:00', '20:00'], 'weekend': ['09:00', '17:00']}
CAPACITY = 12         # bookings that can run at the same time (one per seat; a meeting table counts as one booking)
SLOT_MINUTES = 30
LEAD_MINUTES = 15
MAX_HOURS = 8
COFFEE_FROM_HOURS = 2  # a drink is included from this many hours
PHONE, PHONE_HREF, EMAIL = '+359 88 000 0000', '+359880000000', 'hello@example.com'
ADDRESS = {'bg': 'ул. Примерна 33, Пловдив', 'en': '33 Primer St., Plovdiv'}

# id, seats, price per hour, price for the day, photo, (bg name, en name), (bg short, en short), grid area in the floor plan
ZONES = [
 ('window', 4, 3.5, 16, 'window-seat', ('Бар до прозореца', 'Window bar'), ('Светло, с гледка към улицата', 'Bright, with a view of the street')),
 ('long', 6, 3.0, 14, 'long-table', ('Дълга маса', 'Long table'), ('Споделена маса, контакт при всяко място', 'A shared table, a socket at every seat')),
 ('quiet', 3, 4.0, 18, 'laptop-mug', ('Тиха зона', 'Quiet corner'), ('Без разговори и без обаждания', 'No talking and no calls')),
 ('meeting', 6, 12.0, 70, 'talking', ('Маса за срещи', 'Meeting table'), ('Цяла маса за до 6 души, с екран', 'A whole table for up to 6, with a screen')),
]
NEEDS = [('power', 'Контакт', 'Power socket'), ('screen', 'Втори екран', 'Second screen'), ('calls', 'Ще говоря по телефона', 'I will take calls'), ('dog', 'Идвам с куче', 'I am bringing a dog')]
EVENTS = [('1', '18:30', ('Кафе и код', 'Coffee and code'), ('Свободна вечер за разработчици и всички, които учат.', 'An open evening for developers and anyone learning.')),
          ('3', '18:00', ('Английски клуб', 'English club'), ('Разговор на английски на чаша кафе. Всички нива.', 'Conversation in English over coffee. All levels.')),
          ('4', '09:00', ('Тиха сутрин', 'Silent morning'), ('Три часа без разговори. Само клавиатури.', 'Three hours without talking. Only keyboards.')),
          ('6', '11:00', ('Работилница за латте арт', 'Latte art workshop'), ('Малка група, всеки прави свое сърце. 15 €.', 'A small group, everyone pours a heart. €15.'))]
WEEKDAY = {'1': ('Понеделник', 'Monday'), '3': ('Сряда', 'Wednesday'), '4': ('Четвъртък', 'Thursday'), '6': ('Събота', 'Saturday')}

SKINS = [('paper', 'Хартия', 'Paper', '#F6F2EA', '#D2381E'), ('ultra', 'Ултрамарин', 'Ultramarine', '#EEF1FB', '#2742C7'),
         ('sage', 'Градина', 'Sage', '#EEF2EA', '#3F6B34'), ('charcoal', 'Въглен', 'Charcoal', '#17181A', '#FFB84D'),
         ('plum', 'Слива', 'Plum', '#F8EFF3', '#8A2D6B')]


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
        return (('%.2f' % v).replace('.', ',') + ' €') if bg else ('€' + '%.2f' % v)

    def money0(v):
        return ('%d €' % v) if bg else ('€%d' % v)

    plan_btns = ''.join('<button class="zone zone-%s" type="button" data-zone="%s" aria-pressed="false"><b>%s</b><span>%d %s</span>%s</button>'
                        % (z[0], z[0], z[5][i], z[1], t('места', 'seats') if z[0] != 'meeting' else t('души', 'people'),
                           '<i class="seats" aria-hidden="true">%s</i>' % ''.join('<u></u>' for _ in range(min(z[1], 6)))) for z in ZONES)
    zone_cards = ''.join('<label class="zcard"><input type="radio" name="zone" value="%s"%s><figure>%s</figure><span class="zc-t"><b>%s</b><small>%s</small></span><em>%s</em></label>'
                         % (z[0], ' checked' if z[0] == 'window' else '', I(z[4], z[5][i], '(min-width: 900px) 130px, 30vw'), z[5][i], z[6][i],
                            (money(z[2]) + t(' / час', ' / h')))
                         for z in ZONES)
    need_html = ''.join('<label class="opt"><input type="checkbox" name="need" value="%s" data-name="%s"><span>%s</span></label>' % (k, b if bg else e, b if bg else e) for k, b, e in NEEDS)
    events = ''.join('<li><span class="ev-d">%s</span><span class="ev-t">%s</span><div><h3>%s</h3><p>%s</p></div></li>' % (WEEKDAY[d][i], tm, nm[i], ds[i]) for d, tm, nm, ds in EVENTS)
    amen = [(t('Бърз интернет', 'Fast Wi-Fi'), t('500 Mbit/s, без парола за гости', '500 Mbit/s, no guest password')), (t('Контакти', 'Sockets'), t('По един при всяко място', 'One at every seat')),
            (t('Печат и скенер', 'Printing and scanning'), t('Първите 5 страници са безплатни', 'The first 5 pages are free')), (t('Телефонна кабина', 'Phone booth'), t('За разговори, без да пречите', 'For calls without disturbing anyone')),
            (t('Парковка за велосипеди', 'Bike parking'), t('Под наем зад кафенето', 'Behind the café')), (t('Кафе без дъно', 'Bottomless filter'), t('От 4 часа нагоре', 'From 4 hours up'))]
    amen_html = ''.join('<li><b>%s</b><span>%s</span></li>' % a for a in amen)
    rules = [t('В тихата зона не се говори и не се звъни.', 'No talking and no calls in the quiet corner.'), t('Купуваш напитка поне на два часа.', 'Buy a drink at least every two hours.'),
             t('Не заемай място с чанта, ако не седиш.', 'Do not hold a seat with a bag if you are not sitting there.'), t('Слушалки на разговорните маси, моля.', 'Headphones at the talking tables, please.')]
    rules_html = ''.join('<li>%s</li>' % r for r in rules)
    swatches = ''.join('<button class="sw" type="button" data-skin="%s" style="--s1:%s;--s2:%s" aria-pressed="false" aria-label="%s"></button>' % (k, s1, s2, b if bg else e) for k, b, e, s1, s2 in SKINS)
    hours_rows = [(t('Понеделник – петък', 'Monday – Friday'), HOURS['weekday'], 'wd'), (t('Събота и неделя', 'Saturday and Sunday'), HOURS['weekend'], 'we')]
    hours_html = ''.join('<div data-hrs="%s"><dt>%s</dt><dd>%s – %s</dd></div>' % (k, n, h[0], h[1]) for n, h, k in hours_rows)
    hours_ld = '"Mo-Fr %s-%s","Sa-Su %s-%s"' % (HOURS['weekday'][0], HOURS['weekday'][1], HOURS['weekend'][0], HOURS['weekend'][1])
    nav = [('#plan', t('Места', 'Seats')), ('#prices', t('Цени', 'Prices')), ('#book', t('Резервирай', 'Book')), ('#community', t('Общност', 'Community')), ('#visit', t('Адрес', 'Visit'))]
    nav_html = ''.join('<a href="%s">%s</a>' % n for n in nav)

    data = {'zones': [{'id': z[0], 'seats': z[1], 'rate': z[2], 'day': z[3], 'name': z[5][i]} for z in ZONES], 'maxHours': MAX_HOURS, 'coffeeFrom': COFFEE_FROM_HOURS,
            'needs': {k: (b if bg else e) for k, b, e in NEEDS}}

    title = t('Desk & Drip – кафене за работа в Пловдив. Резервирай бюро на час или за деня', 'Desk & Drip – a work-friendly café in Plovdiv. Book a desk by the hour or for the day')
    desc = t('Desk & Drip е кафене за работа с бърз интернет, контакти и тиха зона. Избери място на плана, виж цената и резервирай час.',
             'Desk & Drip is a café for working, with fast Wi-Fi, sockets and a quiet corner. Pick a spot on the plan, see the price and book a time.')

    return '''<!doctype html>
<html lang="%(lang)s" data-skin="paper">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="theme-color" content="#F6F2EA">
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
     and an og:image (images/stock/lounge-bright.jpg is a placeholder) -->
<link rel="preload" href="%(root)sfonts/onest-%(script)s.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="%(root)sfonts/playfair-%(script)s.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="%(root)sfonts/fonts.css">
<link rel="stylesheet" href="%(root)scss/style.css">
<script>
  /* Scroll animations only run when the browser supports them and the visitor has not asked for less motion. */
  if ("IntersectionObserver" in window && !matchMedia("(prefers-reduced-motion: reduce)").matches) document.documentElement.classList.add("js-reveal");
</script>
<script>
  /* Apply the saved colour scheme before the page paints, so it does not flash. */
  try { var s = new URLSearchParams(location.search).get("skin") || localStorage.getItem("deskSkin"); if (s) document.documentElement.dataset.skin = s; } catch (e) {}
</script>
<script type="application/ld+json">
{"@context":"https://schema.org","@type":"CafeOrCoffeeShop","name":"%(brand)s","inLanguage":"%(lang)s","telephone":"%(phone_href)s","email":"%(email)s",
 "address":{"@type":"PostalAddress","streetAddress":"Primer St. 33","addressLocality":"Plovdiv","addressCountry":"BG"},
 "servesCuisine":"Coffee","amenityFeature":[{"@type":"LocationFeatureSpecification","name":"Wi-Fi","value":true}],"openingHours":[%(hours_ld)s]}
</script>
</head>
<body>
<a class="skip" href="#main">%(skip)s</a>

<header class="top" id="top">
  <div class="top-in">
    <a class="logo" href="index.html"><svg viewBox="0 0 32 32" width="28" height="28" aria-hidden="true" focusable="false"><rect x="3" y="3" width="11" height="11" rx="2" fill="currentColor"/><rect x="18" y="3" width="11" height="11" rx="5.500" fill="none" stroke="currentColor" stroke-width="2.500"/><rect x="3" y="18" width="11" height="11" rx="5.500" fill="none" stroke="currentColor" stroke-width="2.500"/><rect x="18" y="18" width="11" height="11" rx="2" fill="currentColor"/></svg><b>%(brand)s</b></a>
    <nav class="nav" id="nav" aria-label="%(nav_label)s">%(nav_html)s</nav>
    <div class="top-r">
      <span class="open-pill" id="openPill" data-state="unknown"><i aria-hidden="true"></i><span id="openText">%(hours_short)s</span></span>
      <a class="lang" href="%(other_href)s" lang="%(other_lang)s" hreflang="%(other_lang)s" aria-label="%(other_aria)s">%(other_label)s</a>
      <a class="btn btn-main btn-sm top-cta" href="#book">%(cta)s</a>
      <button class="burger" id="burger" type="button" aria-controls="nav" aria-expanded="false" aria-label="%(menu_btn)s"><span></span></button>
    </div>
  </div>
</header>

<main id="main">

  <!-- ============ Hero with the floor plan ============ -->
  <section class="hero" id="plan" aria-labelledby="h1">
    <div class="wrap hero-in">
      <div class="hero-copy">
        <p class="eyebrow">%(eyebrow)s</p>
        <h1 id="h1">%(h1)s</h1>
        <p class="lead">%(lead)s</p>
        <div class="hero-actions">
          <a class="btn btn-main" href="#book">%(cta1)s</a>
          <a class="btn btn-line" href="#prices">%(cta2)s</a>
        </div>
        <ul class="facts">
          <li><b>500</b><span>Mbit/s</span></li>
          <li><b>13</b><span>%(f_sockets)s</span></li>
          <li><b id="nextFree">–</b><span>%(f_next)s</span></li>
        </ul>
      </div>
      <div class="planbox">
        <p class="plan-h">%(plan_h)s</p>
        <div class="plan" role="group" aria-label="%(plan_h)s">
          <span class="plan-door" aria-hidden="true">%(door)s</span>
          <span class="plan-bar" aria-hidden="true">%(bar)s</span>
          %(plan_btns)s
        </div>
        <div class="plan-cap" id="planCap" role="status">%(plan_hint)s</div>
        <a class="btn btn-main btn-sm plan-go" id="planGo" href="#book" hidden>%(plan_go)s</a>
      </div>
    </div>
  </section>
  <figure class="strip">%(strip_img)s</figure>

  <!-- ============ Prices ============ -->
  <section class="block" id="prices" aria-labelledby="pr-h">
    <div class="wrap">
      <header class="sec-head">
        <p class="kicker">%(k_prices)s</p>
        <h2 id="pr-h">%(prices_h)s</h2>
        <p>%(prices_p)s</p>
      </header>
      <ul class="plans">
        <li class="pl"><h3>%(pl1_h)s</h3><p class="pl-p"><b>%(pl1_p)s</b><span>%(pl1_u)s</span></p><p>%(pl1_t)s</p></li>
        <li class="pl pl-main"><h3>%(pl2_h)s</h3><p class="pl-p"><b>%(pl2_p)s</b><span>%(pl2_u)s</span></p><p>%(pl2_t)s</p></li>
        <li class="pl"><h3>%(pl3_h)s</h3><p class="pl-p"><b>%(pl3_p)s</b><span>%(pl3_u)s</span></p><p>%(pl3_t)s</p></li>
      </ul>
      <p class="prices-note">%(prices_note)s</p>
    </div>
  </section>

  <!-- ============ Book ============ -->
  <section class="block soft" id="book" aria-labelledby="bk-h">
    <div class="wrap">
      <header class="sec-head">
        <p class="kicker">%(k_book)s</p>
        <h2 id="bk-h">%(book_h)s</h2>
        <p>%(book_p)s</p>
      </header>
      <form class="book-form" id="bookForm" novalidate>
        <div class="steps">
          <fieldset class="step">
            <legend><b>1</b> %(s1)s</legend>
            <div class="zcards" role="radiogroup" aria-label="%(s1)s">%(zone_cards)s</div>
          </fieldset>
          <fieldset class="step">
            <legend><b>2</b> %(s2)s</legend>
            <div class="hours-row">
              <span class="qty-l" id="hrsL">%(f_hours)s</span>
              <div class="stepper" role="group" aria-labelledby="hrsL"><button type="button" id="hMinus" aria-label="%(h_less)s">−</button><output id="hOut">3</output><button type="button" id="hPlus" aria-label="%(h_more)s">+</button></div>
              <span class="hint" id="hrsHint"></span>
            </div>
            <div class="field" id="peopleRow" hidden><label for="f-people">%(f_people)s</label><select id="f-people" name="people"></select></div>
            <p class="sub-h">%(f_day)s</p>
            <div class="dchips" id="dchips" role="radiogroup" aria-label="%(f_day)s"></div>
            <p class="sub-h">%(f_start)s</p>
            <p class="hint" id="slotHint" role="status">%(checking)s</p>
            <div class="tchips" id="tchips" role="radiogroup" aria-label="%(f_start)s"></div>
          </fieldset>
          <fieldset class="step">
            <legend><b>3</b> %(s3)s</legend>
            <div class="opts">%(need_html)s</div>
            <div class="grid2">
              <div class="field"><label for="f-name">%(f_name)s</label><input id="f-name" name="name" type="text" autocomplete="name" required></div>
              <div class="field"><label for="f-phone">%(f_phone)s</label><input id="f-phone" name="phone" type="tel" autocomplete="tel" required></div>
            </div>
            <div class="field"><label for="f-msg">%(f_msg)s</label><textarea id="f-msg" name="msg" rows="2"></textarea></div>
          </fieldset>
        </div>

        <section class="slip" aria-labelledby="slip-h">
          <h3 id="slip-h">%(slip_h)s</h3>
          <p class="slip-zone" id="slipZone"></p>
          <dl class="slip-list">
            <div><dt>%(sl_when)s</dt><dd id="slWhen">–</dd></div>
            <div><dt>%(sl_len)s</dt><dd id="slLen">–</dd></div>
            <div><dt>%(sl_rate)s</dt><dd id="slRate">–</dd></div>
            <div><dt>%(sl_extra)s</dt><dd id="slExtra">–</dd></div>
          </dl>
          <p class="slip-total"><span>%(total_l)s</span><b id="slTotal">–</b></p>
          <p class="slip-save" id="slSave" hidden></p>
          <p class="demo-note" id="demoNote" hidden></p>
          <p class="form-error" id="bkError" role="alert" hidden></p>
          <button class="btn btn-main btn-block" type="submit" id="bkSend">%(f_send)s</button>
          <small class="fine">%(f_note)s <a href="%(privacy_href)s">%(f_priv)s</a></small>
        </section>
      </form>
      <div class="done" id="bkDone" hidden tabindex="-1"></div>
    </div>
  </section>

  <!-- ============ Included ============ -->
  <section class="block" id="included" aria-labelledby="in-h">
    <div class="wrap included">
      <header class="sec-head">
        <p class="kicker">%(k_in)s</p>
        <h2 id="in-h">%(in_h)s</h2>
        <p>%(in_p)s</p>
        <ul class="rules">%(rules_html)s</ul>
      </header>
      <ul class="amen">%(amen_html)s</ul>
    </div>
  </section>

  <!-- ============ Community ============ -->
  <section class="block community" id="community" aria-labelledby="cm-h">
    <div class="wrap comm">
      <div>
        <header class="sec-head">
          <p class="kicker kicker-dark">%(k_comm)s</p>
          <h2 id="cm-h">%(comm_h)s</h2>
          <p>%(comm_p)s</p>
        </header>
        <ul class="events">%(events)s</ul>
      </div>
      <div class="comm-photos">
        <figure class="cp cp-1">%(cp1)s</figure>
        <figure class="cp cp-2">%(cp2)s</figure>
      </div>
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
    <span>© <span id="year">2026</span> Desk &amp; Drip. %(foot_demo)s</span>
    <span class="foot-links"><a href="%(privacy_href)s">%(f_priv)s</a> <a href="%(admin_href)s">%(admin_l)s</a></span>
  </div>
</footer>

<div class="actionbar" id="bar">
  <span id="barTxt">%(bar_txt)s</span>
  <a class="btn btn-main btn-sm" href="#book">%(bar_book)s</a>
</div>

<aside class="dock" aria-label="%(dock_label)s">
  <div class="dock-label"><small>%(dock_label)s</small><b id="skinName">%(skin_name)s</b></div>
  <div class="swatches">%(swatches)s</div>
</aside>

<script type="application/json" id="deskData">%(data)s</script>
<script src="%(root)sjs/config.js"></script>
<script src="%(root)sjs/api.js"></script>
<script src="%(root)sjs/main.js"></script>
</body>
</html>
''' % dict(
        lang=lang, title=esc(title), desc=esc(desc), root=root, script=script, brand=BRAND, phone_href=PHONE_HREF, phone=PHONE, email=EMAIL, hours_ld=hours_ld,
        skip=t('Към съдържанието', 'Skip to content'), nav_label=t('Навигация', 'Navigation'), nav_html=nav_html, hours_short=t('Работно време', 'Opening hours'),
        other_href=other_href, other_lang='en' if bg else 'bg', other_label='EN' if bg else 'БГ', other_aria='Switch to English' if bg else 'Превключи на български',
        cta=t('Резервирай', 'Book'), menu_btn=t('Меню', 'Menu'),
        eyebrow=t('Кафене и място за работа · Пловдив', 'Café and workspace · Plovdiv'),
        h1=t('Бюро за деня, <em>кафето е включено.</em>', 'A desk for the day, <em>coffee included.</em>'),
        lead=t('Бърз интернет, контакт при всяко място и тиха зона. Избери място на плана, виж цената и резервирай за час или за целия ден.', 'Fast Wi-Fi, a socket at every seat and a quiet corner. Pick a spot on the plan, see the price and book for an hour or the whole day.'),
        cta1=t('Резервирай място', 'Book a seat'), cta2=t('Виж цените', 'See prices'), f_sockets=t('контакта', 'sockets'), f_next=t('първи свободен час', 'first free hour'),
        plan_h=t('Планът на кафенето', 'The café plan'), door=t('вход', 'entrance'), bar=t('бар', 'bar'), plan_btns=plan_btns, plan_hint=t('Натисни зона, за да видиш местата и цената.', 'Press a zone to see the seats and the price.'), plan_go=t('Резервирай тази зона', 'Book this zone'),
        strip_img=I('lounge-bright', t('Светъл салон с дълги маси, растения и големи прозорци', 'A bright room with long tables, plants and big windows'), '100vw', eager=False),
        k_prices=t('Цени', 'Prices'), prices_h=t('На час или за деня', 'By the hour or for the day'),
        prices_p=t('Плащаш на място. Ако останеш повече, цената не надвишава дневната.', 'You pay on site. If you stay longer, the price never goes above the day price.'),
        pl1_h=t('На час', 'By the hour'), pl1_p=t('от 3 €', 'from €3'), pl1_u=t('на час', 'per hour'), pl1_t=t('За кратка работа. Напитка при 2 и повече часа.', 'For short jobs. A drink from 2 hours.'),
        pl2_h=t('За деня', 'Day pass'), pl2_p=t('от 14 €', 'from €14'), pl2_u=t('до 8 часа', 'up to 8 hours'), pl2_t=t('Най-изгодно. Кафе без дъно от 4 часа.', 'Best value. Bottomless filter from 4 hours.'),
        pl3_h=t('Седмица или месец', 'Week or month'), pl3_p=t('питай ни', 'ask us'), pl3_u=t('постоянно място', 'a regular seat'), pl3_t=t('Не се резервира онлайн. Пиши ни и ще ти предложим.', 'Not booked online. Write to us and we will make an offer.'),
        prices_note=t('Масата за срещи е цена за цялата маса, до 6 души.', 'The meeting table is priced for the whole table, up to 6 people.'),
        k_book=t('Резервирай', 'Book'), book_h=t('Избери зона, ден и час', 'Choose a zone, a day and a time'),
        book_p=t('Картата вдясно показва точната цена и кога свършваш.', 'The card on the right shows the exact price and when you finish.'),
        s1=t('Къде да седнеш', 'Where to sit'), zone_cards=zone_cards,
        s2=t('Кога и за колко часа', 'When and for how long'), f_hours=t('Часове', 'Hours'), h_less=t('Един час по-малко', 'One hour fewer'), h_more=t('Един час повече', 'One hour more'), f_people=t('Колко души?', 'How many people?'),
        f_day=t('Ден', 'Day'), f_start=t('Начален час', 'Start time'), checking=t('Проверяваме свободните часове…', 'Checking free times…'),
        s3=t('Нужди и данни за връзка', 'Needs and your details'), need_html=need_html, f_name=t('Име', 'Name'), f_phone=t('Телефон', 'Phone'), f_msg=t('Бележка (по желание)', 'Note (optional)'),
        slip_h=t('Твоята резервация', 'Your booking'), sl_when=t('Кога', 'When'), sl_len=t('Продължителност', 'Length'), sl_rate=t('Цена', 'Pricing'), sl_extra=t('Включено', 'Included'), total_l=t('Общо', 'Total'),
        f_send=t('Резервирай мястото', 'Book the seat'), f_note=t('Плащаш на място. Безплатно отмяна до 2 часа преди.', 'You pay on site. Free cancellation up to 2 hours before.'), f_priv=t('Поверителност', 'Privacy'), privacy_href='privacy.html',
        k_in=t('Включено', 'Included'), in_h=t('Всичко, което ти трябва за работа', 'Everything you need to work'),
        in_p=t('Малко правила, за да е удобно на всички.', 'A few house rules so it works for everyone.'), rules_html=rules_html, amen_html=amen_html,
        k_comm=t('Общност', 'Community'), comm_h=t('Не само за работа', 'Not only for work'), comm_p=t('Седмични срещи в кафенето. Свободни са за всички.', 'Weekly meetups at the café. Free for everyone.'), events=events,
        cp1=I('notes-latte', t('Бележник, лаптоп и лате върху дървена маса', 'A notebook, a laptop and a latte on a wooden table'), '(min-width: 900px) 420px, 90vw'), cp2=I('sunlit-room', t('Слънчева стая с хора, които работят', 'A sunlit room with people working'), '(min-width: 900px) 420px, 90vw'),
        k_visit=t('Адрес', 'Visit'), visit_h=t('Намери ни', 'Find us'), hours_html=hours_html,
        l_addr=t('Адрес', 'Address'), address=ADDRESS['bg' if bg else 'en'], l_phone=t('Телефон', 'Phone'), l_email=t('Имейл', 'Email'),
        visit_img=I('glass-hall', t('Салон със стъклени стени и дълга маса', 'A hall with glass walls and a long table'), '(min-width: 900px) 520px, 90vw'),
        map_t=t('Картата се зарежда от OpenStreetMap едва когато я поискаш.', 'The map loads from OpenStreetMap only when you ask for it.'), map_btn=t('Покажи картата', 'Show the map'),
        foot_demo=t('Всичко тук е пример.', 'Everything here is an example.'), admin_href='admin.html' if bg else '../admin.html?lang=en', admin_l=t('Демо админ панел', 'Demo back office'),
        bar_txt=t('Работиш днес?', 'Working today?'), bar_book=t('Резервирай място', 'Book a seat'),
        dock_label=t('Цветова схема', 'Colour scheme'), skin_name=t('Хартия', 'Paper'), swatches=swatches,
        data=json.dumps(data, ensure_ascii=False).replace('</', '<\\/'),
    )


def main():
    cfg = ('/* Generated by tools/build_pages.py. Edit the values at the top of that file, then run it again. */\n'
           'window.DESK_CONFIG = {\n  mode: "demo",            /* "demo" = requests are kept in this browser only; "live" = real API at apiBase (docs/API.md) */\n'
           '  apiBase: "/api",\n  hours: { weekday: ["%s", "%s"], weekend: ["%s", "%s"] },\n  capacity: %d,            /* bookings that can run at the same time */\n'
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
