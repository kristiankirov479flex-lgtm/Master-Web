"""Builds index.html (Bulgarian), en/index.html (English), js/config.js and css/style.css for Gripline.
Edit the values in this file (prices, jobs, hours, texts), then run:  python tools/build_pages.py && python tools/build_privacy.py
Everything about the workshop is an example: replace it for a real tyre shop."""
import json, os
from html import escape as esc
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BRAND = 'Gripline'

# ---------------- settings you will change for a real workshop ----------------
HOURS = {'weekday': ['08:00', '18:00'], 'weekend': ['09:00', '14:00']}
CAPACITY = 2          # bays working at the same time
SLOT_MINUTES = 15
LEAD_MINUTES = 30     # a same-day visit needs this much notice
PHONE, PHONE_HREF, EMAIL = '+359 88 000 0000', '+359880000000', 'service@example.com'
ADDRESS = {'bg': 'ул. Примерна 40, Пловдив', 'en': '40 Primer St., Plovdiv'}

# Price of "swap and balance" for 4 wheels: BASE for rims up to 15", plus PER_INCH for every inch above 15; vehicle surcharges.
BASE, PER_INCH = 28, 4
VEHICLES = [('car', 'Лек автомобил', 'Car', 0), ('suv', 'SUV / джип', 'SUV / 4x4', 8), ('van', 'Бус / ван', 'Van', 10)]
# jobs (pick one): id, bg, en, desc bg, desc en, price kind, base price, minutes
JOBS = [
 ('swap', 'Смяна на сезонни гуми', 'Seasonal tyre swap', 'Сваляне, монтаж и баланс на 4 ваши колела', 'Remove, fit and balance 4 of your own wheels', 'size', BASE, 45),
 ('new', 'Нови гуми', 'New tyres', 'Монтаж и баланс на 4 нови гуми (гумите се оферират отделно)', 'Mounting and balancing 4 new tyres (tyres quoted separately)', 'size', 40, 60),
 ('repair', 'Ремонт на спукана гума', 'Puncture repair', 'Проверка, ремонт отвътре и баланс на 1 гума', 'Inspection, internal repair and balance of 1 tyre', 'fixed', 10, 25),
 ('check', 'Проверка и съвет', 'Check-up and advice', 'Безплатен преглед на протектора и налягането', 'Free tread and pressure check', 'fixed', 0, 15),
]
# add-ons (any): id, bg, en, desc bg, desc en, price kind, price, minutes
ADDONS = [
 ('align', 'Сходимост на колелата', 'Wheel alignment', 'Компютърна проверка и настройка', 'Computer check and adjustment', 'fixed', 35, 40),
 ('storage', 'Съхранение на гумите', 'Tyre storage', 'Един сезон, подредени и етикетирани', 'One season, stacked and labelled', 'storage', 30, 10),
 ('tpms', 'Проверка на датчиците (TPMS)', 'TPMS sensor check', 'Четене и нулиране на 4 датчика', 'Read and reset 4 sensors', 'fixed', 12, 10),
 ('valves', 'Нови вентили', 'New valves', 'Комплект от 4 гумени вентила', 'Set of 4 rubber valves', 'fixed', 8, 5),
]
WIDTHS = [155, 165, 175, 185, 195, 205, 215, 225, 235, 245, 255, 265, 275, 285, 295]
PROFILES = [30, 35, 40, 45, 50, 55, 60, 65, 70, 75]
RIMS = list(range(13, 22))
MAKES = ['Audi', 'BMW', 'Citroën', 'Dacia', 'Fiat', 'Ford', 'Honda', 'Hyundai', 'Kia', 'Mazda', 'Mercedes-Benz', 'Nissan', 'Opel', 'Peugeot', 'Renault', 'Seat', 'Škoda', 'Toyota', 'Volkswagen', 'Volvo']

SKINS = [('hazard', 'Жълт', 'Hazard', '#15171A', '#FFC400'), ('redline', 'Червен', 'Redline', '#17110F', '#FF4B3E'),
         ('cobalt', 'Син', 'Cobalt', '#0E1626', '#4DA3FF'), ('forest', 'Зелен', 'Forest', '#0F1A14', '#7BE08C'),
         ('concrete', 'Бетон', 'Concrete', '#ECEDEA', '#FFC400')]


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
    other_href = 'en/index.html' if bg else '../index.html'
    script = 'cyrillic' if bg else 'latin'
    i = 0 if bg else 1

    def opts(values, sel):
        return ''.join('<option value="%s"%s>%s</option>' % (v, ' selected' if v == sel else '', v) for v in values)

    make_opts = '<option value="">%s</option>' % t('Избери марка', 'Choose a make') + ''.join('<option>%s</option>' % m for m in MAKES) + '<option value="other">%s</option>' % t('Друга', 'Other')
    veh_html = ''.join('<label class="opt"><input type="radio" name="veh" value="%s"%s><span>%s</span></label>' % (k, ' checked' if k == 'car' else '', b if bg else e) for k, b, e, _ in VEHICLES)
    job_html = ''.join('<label class="opt opt-card"><input type="radio" name="job" value="%s"%s><span><b>%s</b><small>%s</small></span><em class="opt-p" data-price="%s"></em></label>'
                       % (j[0], ' checked' if j[0] == 'swap' else '', j[1 + i], j[3 + i], j[0]) for j in JOBS)
    addon_html = ''.join('<label class="opt opt-card"><input type="checkbox" name="addon" value="%s"><span><b>%s</b><small>%s</small></span><em class="opt-p" data-price="%s"></em></label>'
                         % (a[0], a[1 + i], a[3 + i], a[0]) for a in ADDONS)

    board_rows = [(t('Смяна на 4 колела, до 15″', 'Swap of 4 wheels, up to 15″'), t('с баланс', 'with balancing'), BASE),
                  (t('Смяна на 4 колела, 16″', 'Swap of 4 wheels, 16″'), t('с баланс', 'with balancing'), BASE + PER_INCH),
                  (t('Смяна на 4 колела, 17″', 'Swap of 4 wheels, 17″'), t('с баланс', 'with balancing'), BASE + 2 * PER_INCH),
                  (t('Смяна на 4 колела, 18″ и повече', 'Swap of 4 wheels, 18″ and up'), t('с баланс', 'with balancing'), BASE + 3 * PER_INCH),
                  (t('Ремонт на спукана гума', 'Puncture repair'), t('на гума', 'per tyre'), 10), (t('Сходимост', 'Wheel alignment'), t('компютърна', 'computer'), 35),
                  (t('Съхранение на комплект', 'Tyre storage, set'), t('един сезон', 'one season'), 30), (t('Проверка на налягане и протектор', 'Pressure and tread check'), t('винаги', 'always'), 0)]
    board_html = ''.join('<li><div><b>%s</b><small>%s</small></div><span class="bp">%s</span></li>' % (a, b, (t('от ', 'from ') + str(c) + ' €') if c else t('безплатно', 'free')) for a, b, c in board_rows)

    seasons = [(t('Лятни', 'Summer'), t('над 7 °C', 'above 7 °C'), t('Най-добро сцепление и къс спирачен път на сухо и мокро при топло време.', 'Best grip and shortest braking on dry and wet roads in warm weather.')),
               (t('Зимни', 'Winter'), t('под 7 °C', 'below 7 °C'), t('Мека гума и ламели, които държат в студ, сняг и киша.', 'Soft rubber and sipes that hold in cold, snow and slush.')),
               (t('Всесезонни', 'All-season'), t('компромис', 'compromise'), t('Удобни, ако карате малко и в градски условия. Не са най-добрите нито лятото, нито зимата.', 'Convenient if you drive little in town. Not the best in summer or winter.'))]
    season_html = ''.join('<li><h3>%s</h3><p class="chip-t">%s</p><p>%s</p></li>' % s for s in seasons)
    faq = [(t('Трябва ли да си запазя час?', 'Do I need to book?'), t('Не е задължително. Приемаме и без час, когато има свободна площадка, но с час не чакате. Най-натоварено е в края на октомври и в началото на април.', 'Not required. We take walk-ins when a bay is free, but with a booking you do not wait. The busiest times are late October and early April.')),
           (t('Колко време отнема смяната?', 'How long does a swap take?'), t('Около 45 минути за четири колела. Показваме очакваното време, докато избирате услугите.', 'About 45 minutes for four wheels. We show the expected time while you choose services.')),
           (t('Пазите ли гумите ни?', 'Do you store our tyres?'), t('Да. Комплектът се подрежда и етикетира с номера на колата и се връща при следващата смяна.', 'Yes. The set is stacked and labelled with your plate and handed back at the next swap.')),
           (t('Как се плаща?', 'How do I pay?'), t('На място, в брой или с карта, след като работата е готова. Цената, която виждате тук, е ориентировъчна, а крайната я казваме преди да започнем.', 'On site, cash or card, when the work is done. The price you see here is an estimate; we confirm the final price before we start.')),
           (t('Работите ли с гуми Run-Flat и с датчици?', 'Do you handle run-flat tyres and sensors?'), t('Да, с подходящата машина. Напишете го в бележката, за да отделим повече време.', 'Yes, with the right machine. Mention it in the note so we reserve extra time.'))]
    faq_html = ''.join('<details class="qa"><summary>%s</summary><p>%s</p></details>' % f for f in faq)

    hours_rows = [(t('Понеделник – петък', 'Monday – Friday'), HOURS['weekday'], 'wd'), (t('Събота и неделя', 'Saturday and Sunday'), HOURS['weekend'], 'we')]
    hours_html = ''.join('<div data-hrs="%s"><dt>%s</dt><dd>%s – %s</dd></div>' % (k, n, h[0], h[1]) for n, h, k in hours_rows)
    hours_ld = '"Mo-Fr %s-%s","Sa-Su %s-%s"' % (HOURS['weekday'][0], HOURS['weekday'][1], HOURS['weekend'][0], HOURS['weekend'][1])
    swatches = ''.join('<button class="sw" type="button" data-skin="%s" style="--s1:%s;--s2:%s" aria-pressed="false" aria-label="%s"></button>' % (k, s1, s2, b if bg else e) for k, b, e, s1, s2 in SKINS)
    nav = [('#services', t('Цени', 'Prices')), ('#book', t('Запази час', 'Book')), ('#guide', t('Гуми', 'Tyre guide')), ('#faq', t('Въпроси', 'FAQ')), ('#visit', t('Адрес', 'Visit'))]
    nav_html = ''.join('<a href="%s">%s</a>' % n for n in nav)

    data = {'base': BASE, 'perInch': PER_INCH, 'vehicles': [{'id': v[0], 'add': v[3], 'name': v[1 + i]} for v in VEHICLES],
            'jobs': [{'id': j[0], 'name': j[1 + i], 'kind': j[5], 'price': j[6], 'min': j[7]} for j in JOBS],
            'addons': [{'id': a[0], 'name': a[1 + i], 'kind': a[5], 'price': a[6], 'min': a[7]} for a in ADDONS]}

    title = t('Gripline – гуми и сервиз в Пловдив. Смяна на гуми с час и ясна цена', 'Gripline – tyres and service in Plovdiv. Tyre swaps with a booked time and a clear price')
    desc = t('Gripline е гуми и сервиз в Пловдив: смяна и баланс, ремонт, сходимост и съхранение. Въведи размера на гумите, виж цената и запази час онлайн.',
             'Gripline is a tyre and service workshop in Plovdiv: swaps and balancing, repairs, alignment and storage. Enter your tyre size, see the price and book a time online.')

    return '''<!doctype html>
<html lang="%(lang)s" data-skin="hazard">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="theme-color" content="#15171A">
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
     and an og:image (images/stock/workshop-lift.jpg is a placeholder) -->
<link rel="preload" href="%(root)sfonts/onest-%(script)s.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="%(root)sfonts/oswald-%(script)s.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="%(root)sfonts/fonts.css">
<link rel="stylesheet" href="%(root)scss/style.css">
<script>
  /* Scroll animations only run when the browser supports them and the visitor has not asked for less motion. */
  if ("IntersectionObserver" in window && !matchMedia("(prefers-reduced-motion: reduce)").matches) document.documentElement.classList.add("js-reveal");
</script>
<script>
  /* Apply the saved colour scheme before the page paints, so it does not flash. */
  try { var s = new URLSearchParams(location.search).get("skin") || localStorage.getItem("griplineSkin"); if (s) document.documentElement.dataset.skin = s; } catch (e) {}
</script>
<script type="application/ld+json">
{"@context":"https://schema.org","@type":"AutoRepair","name":"%(brand)s","inLanguage":"%(lang)s","telephone":"%(phone_href)s","email":"%(email)s",
 "address":{"@type":"PostalAddress","streetAddress":"Primer St. 40","addressLocality":"Plovdiv","addressCountry":"BG"},
 "openingHours":[%(hours_ld)s]}
</script>
</head>
<body>
<a class="skip" href="#main">%(skip)s</a>

<aside class="ribbon" aria-label="%(ribbon_l)s">%(ribbon)s</aside>
<header class="top" id="top">
  <div class="top-in">
    <a class="logo" href="index.html"><svg viewBox="0 0 32 32" width="30" height="30" aria-hidden="true" focusable="false"><circle cx="16" cy="16" r="13" fill="none" stroke="currentColor" stroke-width="4" stroke-dasharray="5 2.5"/><circle cx="16" cy="16" r="5" fill="currentColor"/></svg><b>%(brand)s</b></a>
    <nav class="nav" id="nav" aria-label="%(nav_label)s">%(nav_html)s</nav>
    <div class="top-r">
      <a class="phone-btn" href="tel:%(phone_href)s" aria-label="%(call_aria)s"><svg viewBox="0 0 24 24" width="20" height="20" aria-hidden="true" focusable="false"><path fill="currentColor" d="M6.6 10.8a15 15 0 0 0 6.6 6.6l2.2-2.2a1 1 0 0 1 1-.25 11.4 11.4 0 0 0 3.6.57 1 1 0 0 1 1 1V20a1 1 0 0 1-1 1A17 17 0 0 1 3 4a1 1 0 0 1 1-1h3.5a1 1 0 0 1 1 1c0 1.25.2 2.45.57 3.6a1 1 0 0 1-.25 1z"/></svg><span>%(phone)s</span></a>
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
      <div class="hero-copy">
        <p class="eyebrow">%(eyebrow)s</p>
        <h1 id="h1">%(h1)s</h1>
        <p class="lead">%(lead)s</p>
        <form class="finder" id="finder" aria-labelledby="fnd-h">
          <h2 id="fnd-h">%(fnd_h)s</h2>
          <div class="sidewall">
            <label class="sw-f"><span>%(l_width)s</span><select id="h-width" aria-label="%(l_width)s">%(w_opts)s</select></label>
            <i aria-hidden="true">/</i>
            <label class="sw-f"><span>%(l_profile)s</span><select id="h-profile" aria-label="%(l_profile)s">%(p_opts)s</select></label>
            <i aria-hidden="true">R</i>
            <label class="sw-f"><span>%(l_rim)s</span><select id="h-rim" aria-label="%(l_rim)s">%(r_opts)s</select></label>
          </div>
          <p class="fnd-out" id="fndOut" role="status"></p>
          <div class="fnd-actions"><a class="btn btn-main" href="#book" id="fndGo">%(fnd_btn)s</a><span class="fnd-hint">%(fnd_hint)s</span></div>
        </form>
      </div>
      <section class="live" aria-labelledby="lv-h">
        <h2 id="lv-h" class="live-h">%(live_h)s</h2>
        <p class="live-state" id="liveState" data-state="unknown"><i aria-hidden="true"></i><span id="liveText">%(live_check)s</span></p>
        <dl class="live-list">
          <div><dt>%(live_next)s</dt><dd id="liveNext">–</dd></div>
          <div><dt>%(live_today)s</dt><dd id="liveFree">–</dd></div>
          <div><dt>%(live_hours)s</dt><dd id="liveHours">–</dd></div>
        </dl>
        <a class="btn btn-main btn-block" href="#book">%(live_cta)s</a>
        <p class="live-fine">%(live_fine)s</p>
      </section>
    </div>
  </section>

  <!-- ============ Promises ============ -->
  <section class="promises" aria-label="%(prom_label)s">
    <ul class="wrap prom">
      <li><b>%(pr1_b)s</b><span>%(pr1_s)s</span></li>
      <li><b>%(pr2_b)s</b><span>%(pr2_s)s</span></li>
      <li><b>%(pr3_b)s</b><span>%(pr3_s)s</span></li>
      <li><b>%(pr4_b)s</b><span>%(pr4_s)s</span></li>
    </ul>
  </section>

  <!-- ============ Price board ============ -->
  <section class="block" id="services" aria-labelledby="sv-h">
    <div class="wrap services">
      <header class="sec-head">
        <p class="kicker">%(k_services)s</p>
        <h2 id="sv-h">%(services_h)s</h2>
        <p>%(services_p)s</p>
        <figure class="sv-photo">%(sv_img)s</figure>
      </header>
      <ul class="board" aria-label="%(services_h)s">%(board_html)s</ul>
    </div>
  </section>

  <!-- ============ Book a visit ============ -->
  <section class="block book" id="book" aria-labelledby="bk-h">
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
            <div class="grid2">
              <div class="field"><label for="f-make">%(f_make)s</label><select id="f-make" name="make">%(make_opts)s</select></div>
              <div class="field"><label for="f-model">%(f_model)s</label><input id="f-model" name="model" type="text" autocomplete="off" placeholder="%(ph_model)s"></div>
            </div>
            <div class="vehicle" role="radiogroup" aria-label="%(f_vehicle)s">%(veh_html)s</div>
          </fieldset>
          <fieldset class="step">
            <legend><b>2</b> %(s2)s</legend>
            <p class="hint">%(s2_hint)s</p>
            <div class="sidewall sidewall-form">
              <label class="sw-f"><span>%(l_width)s</span><select id="s-width" name="width">%(w_opts)s</select></label>
              <i aria-hidden="true">/</i>
              <label class="sw-f"><span>%(l_profile)s</span><select id="s-profile" name="profile">%(p_opts)s</select></label>
              <i aria-hidden="true">R</i>
              <label class="sw-f"><span>%(l_rim)s</span><select id="s-rim" name="rim">%(r_opts)s</select></label>
            </div>
          </fieldset>
          <fieldset class="step">
            <legend><b>3</b> %(s3)s</legend>
            <div class="opts" role="radiogroup" aria-label="%(s3)s">%(job_html)s</div>
            <p class="sub-h">%(addons_h)s</p>
            <div class="opts">%(addon_html)s</div>
          </fieldset>
          <fieldset class="step">
            <legend><b>4</b> %(s4)s</legend>
            <div class="dchips" id="dchips" role="radiogroup" aria-label="%(f_day)s"></div>
            <p class="hint" id="slotHint" role="status">%(checking)s</p>
            <div class="tchips" id="tchips" role="radiogroup" aria-label="%(f_time)s"></div>
          </fieldset>
          <fieldset class="step">
            <legend><b>5</b> %(s5)s</legend>
            <div class="grid2">
              <div class="field"><label for="f-name">%(f_name)s</label><input id="f-name" name="name" type="text" autocomplete="name" required></div>
              <div class="field"><label for="f-phone">%(f_phone)s</label><input id="f-phone" name="phone" type="tel" autocomplete="tel" required></div>
              <div class="field"><label for="f-plate">%(f_plate)s</label><input id="f-plate" name="plate" type="text" autocomplete="off" placeholder="PB 0000 XX"></div>
            </div>
            <div class="field"><label for="f-msg">%(f_msg)s</label><textarea id="f-msg" name="msg" rows="3"></textarea></div>
          </fieldset>
        </div>

        <section class="slip" aria-labelledby="slip-h">
          <h3 id="slip-h">%(slip_h)s</h3>
          <p class="slip-car" id="slipCar"></p>
          <ul class="slip-lines" id="slipLines"></ul>
          <p class="slip-total"><span>%(est_l)s</span><b id="slipTotal"></b></p>
          <p class="slip-time"><span>%(time_l)s</span><b id="slipTime"></b></p>
          <p class="slip-fine" id="slipFine">%(est_fine)s</p>
          <p class="demo-note" id="demoNote" hidden></p>
          <p class="form-error" id="bkError" role="alert" hidden></p>
          <button class="btn btn-main btn-block" type="submit" id="bkSend">%(f_send)s</button>
          <small class="fine">%(f_note)s <a href="%(privacy_href)s">%(f_priv)s</a></small>
        </section>
      </form>
      <div class="done" id="bkDone" hidden tabindex="-1"></div>
    </div>
  </section>

  <!-- ============ Guide ============ -->
  <section class="block" id="guide" aria-labelledby="gd-h">
    <div class="wrap">
      <header class="sec-head">
        <p class="kicker">%(k_guide)s</p>
        <h2 id="gd-h">%(guide_h)s</h2>
        <p>%(guide_p)s</p>
      </header>
      <ul class="seasons">%(season_html)s</ul>
      <div class="tread">
        <div class="tread-copy"><h3>%(tread_h)s</h3><p>%(tread_p)s</p></div>
        <figure class="tread-ph">%(tread_img)s</figure>
        <figure class="tread-ph tread-ph2">%(tread_img2)s</figure>
      </div>
    </div>
  </section>

  <!-- ============ FAQ ============ -->
  <section class="block soft" id="faq" aria-labelledby="fq-h">
    <div class="wrap faq">
      <header class="sec-head">
        <p class="kicker">%(k_faq)s</p>
        <h2 id="fq-h">%(faq_h)s</h2>
      </header>
      <div class="qas">%(faq_html)s</div>
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
    <span>© <span id="year">2026</span> Gripline. %(foot_demo)s</span>
    <span class="foot-links"><a href="%(privacy_href)s">%(f_priv)s</a> <a href="%(admin_href)s">%(admin_l)s</a></span>
  </div>
</footer>

<div class="actionbar" id="bar">
  <a class="btn btn-line btn-sm" href="tel:%(phone_href)s">%(bar_call)s</a>
  <a class="btn btn-main btn-sm" href="#book">%(bar_book)s</a>
</div>

<aside class="dock" aria-label="%(dock_label)s">
  <div class="dock-label"><small>%(dock_label)s</small><b id="skinName">%(skin_name)s</b></div>
  <div class="swatches">%(swatches)s</div>
</aside>

<script type="application/json" id="gripData">%(data)s</script>
<script src="%(root)sjs/config.js"></script>
<script src="%(root)sjs/api.js"></script>
<script src="%(root)sjs/main.js"></script>
</body>
</html>
''' % dict(
        lang=lang, title=esc(title), desc=esc(desc), root=root, script=script, brand=BRAND, phone_href=PHONE_HREF, phone=PHONE, email=EMAIL, hours_ld=hours_ld,
        skip=t('Към съдържанието', 'Skip to content'), ribbon_l=t('Съобщение', 'Notice'), ribbon=t('Зимни гуми: запази смяната си до 15 ноември. Приемаме и без час, когато има място.', 'Winter tyres: book your swap before 15 November. Walk-ins welcome when a bay is free.'),
        nav_label=t('Навигация', 'Navigation'), nav_html=nav_html, call_aria=t('Обади се', 'Call us'),
        other_href=other_href, other_lang='en' if bg else 'bg', other_label='EN' if bg else 'БГ', other_aria='Switch to English' if bg else 'Превключи на български', menu_btn=t('Меню', 'Menu'),
        hero_img=I('workshop-lift', t('Сервизът отвътре: автомобил на подемник и стена с инструменти', 'Inside the workshop: a car on a lift and a wall of tools'), '100vw', eager=True),
        eyebrow=t('Гуми и сервиз · Пловдив', 'Tyres and service · Plovdiv'),
        h1=t('Гуми. <em>Бързо.</em> Честно.', 'Tyres. <em>Fast.</em> Fair.'),
        lead=t('Смяна, баланс, ремонт и съхранение. Кажи ни размера и услугата, а цената и свободния час виждаш веднага, без да звъниш.',
               'Swaps, balancing, repairs and storage. Tell us your size and the job, and you see the price and a free time straight away, without calling.'),
        fnd_h=t('Какъв е размерът на гумите ти?', 'What is your tyre size?'), l_width=t('Широчина', 'Width'), l_profile=t('Профил', 'Profile'), l_rim=t('Джанта', 'Rim'),
        w_opts=opts(WIDTHS, 205), p_opts=opts(PROFILES, 55), r_opts=opts(RIMS, 16),
        fnd_btn=t('Запази час за този размер', 'Book a time for this size'), fnd_hint=t('Размерът е написан отстрани на гумата.', 'The size is printed on the side of the tyre.'),
        live_h=t('Сега в сервиза', 'In the workshop now'), live_check=t('Проверяваме…', 'Checking…'), live_next=t('Първи свободен час', 'First free time'), live_today=t('Свободни часове днес', 'Free times today'),
        live_hours=t('Работно време днес', 'Hours today'), live_cta=t('Запази час', 'Book a time'), live_fine=t('Данните са примерни и идват от демо сървъра.', 'The data is an example and comes from the demo server.'),
        prom_label=t('Какво обещаваме', 'What we promise'),
        pr1_b=t('Цена преди работа', 'Price before work'), pr1_s=t('Казваме я предварително', 'We tell you up front'),
        pr2_b=t('Около 45 минути', 'About 45 minutes'), pr2_s=t('за смяна на 4 колела', 'to swap 4 wheels'),
        pr3_b=t('Часове по 15 минути', '15-minute times'), pr3_s=t('Два работни бокса', 'Two working bays'),
        pr4_b=t('Съхранение', 'Storage'), pr4_s=t('Подредени и етикетирани', 'Stacked and labelled'),
        k_services=t('Цени', 'Prices'), services_h=t('Ценова дъска', 'Price board'),
        services_p=t('Ориентировъчни цени за лек автомобил. SUV и бусове са малко по-скъпи. Точната сума казваме преди да започнем.', 'Estimated prices for a car. SUVs and vans cost a little more. We confirm the exact amount before we start.'),
        sv_img=I('wheel-wrench', t('Пневматичен ключ на гайките на джанта', 'An impact wrench on the wheel nuts'), '(min-width: 900px) 520px, 92vw'), board_html=board_html,
        k_book=t('Запази час', 'Book a time'), book_h=t('Запази час за автомобила си', 'Book your car in'),
        book_p=t('Пет кратки стъпки. Ценовата сметка вдясно се променя, докато избираш, и показва колко време ще отнеме.', 'Five short steps. The price slip on the right updates as you choose and shows how long it will take.'),
        s1=t('Автомобилът', 'Your car'), f_make=t('Марка', 'Make'), f_model=t('Модел', 'Model'), ph_model=t('напр. Golf', 'e.g. Golf'), f_vehicle=t('Вид автомобил', 'Vehicle type'),
        make_opts=make_opts, veh_html=veh_html, s2=t('Размер на гумите', 'Tyre size'), s2_hint=t('Като на страничната стена на гумата: широчина / профил R джанта.', 'As on the tyre sidewall: width / profile R rim.'),
        s3=t('Какво трябва да се направи?', 'What needs doing?'), job_html=job_html, addons_h=t('Добави към посещението', 'Add to the visit'), addon_html=addon_html,
        s4=t('Кога?', 'When?'), f_day=t('Ден', 'Day'), f_time=t('Час', 'Time'), checking=t('Проверяваме свободните часове…', 'Checking free times…'),
        s5=t('Данни за връзка', 'Your details'), f_name=t('Име', 'Name'), f_phone=t('Телефон', 'Phone'), f_plate=t('Регистрационен номер (по желание)', 'Number plate (optional)'), f_msg=t('Бележка (по желание)', 'Note (optional)'),
        slip_h=t('Сметка за посещението', 'Price slip'), est_l=t('Ориентировъчно общо', 'Estimated total'), time_l=t('Време', 'Time'),
        est_fine=t('Ориентировъчна цена. Крайната я потвърждаваме преди да започнем.', 'An estimate. We confirm the final price before we start.'),
        f_send=t('Изпрати заявката', 'Send the request'), f_note=t('Плащаш на място. Трябват ни само име, телефон и колата.', 'You pay on site. We only need your name, phone and your car.'),
        f_priv=t('Поверителност', 'Privacy'), privacy_href='privacy.html',
        k_guide=t('Гуми', 'Tyre guide'), guide_h=t('Кои гуми кога', 'Which tyres when'),
        guide_p=t('Правилото е просто: под 7 °C зимни, над 7 °C лятни. Ето разликата с две думи.', 'The rule is simple: winter tyres below 7 °C, summer above. Here is the difference in a few words.'),
        season_html=season_html, tread_h=t('Колко протектор е достатъчно?', 'How much tread is enough?'),
        tread_p=t('Законовият минимум е 1,6 mm. Много шофьори сменят летните гуми при 3 mm, а зимните при 4 mm, защото сцеплението пада бързо. Ако се съмняваш, донеси колата: проверката е безплатна.',
                  'The legal minimum is 1.6 mm. Many drivers change summer tyres at 3 mm and winter tyres at 4 mm, because grip falls quickly. If in doubt, bring the car: the check is free.'),
        tread_img=I('tyre-tread', t('Близък план на протектора на гума', 'A close-up of a tyre tread'), '(min-width: 900px) 300px, 45vw'),
        tread_img2=I('alloy-wheel', t('Алуминиева джанта върху купчина гуми', 'An alloy wheel on a stack of tyres'), '(min-width: 900px) 220px, 40vw'),
        k_faq=t('Въпроси', 'FAQ'), faq_h=t('Често задавани въпроси', 'Common questions'), faq_html=faq_html,
        k_visit=t('Адрес', 'Visit'), visit_h=t('Намери ни', 'Find us'), hours_html=hours_html,
        l_addr=t('Адрес', 'Address'), address=ADDRESS['bg' if bg else 'en'], l_phone=t('Телефон', 'Phone'), l_email=t('Имейл', 'Email'),
        visit_img=I('garage-tyres', t('Гуми и джанти, подредени по стената на сервиза', 'Tyres and wheels stacked along the workshop wall'), '(min-width: 900px) 520px, 92vw'),
        map_t=t('Картата се зарежда от OpenStreetMap едва когато я поискаш.', 'The map loads from OpenStreetMap only when you ask for it.'), map_btn=t('Покажи картата', 'Show the map'),
        foot_demo=t('Всичко тук е пример.', 'Everything here is an example.'), admin_href='admin.html' if bg else '../admin.html?lang=en', admin_l=t('Демо админ панел', 'Demo back office'),
        bar_call=t('Обади се', 'Call'), bar_book=t('Запази час', 'Book'), dock_label=t('Цветова схема', 'Colour scheme'), skin_name=t('Жълт', 'Hazard'), swatches=swatches,
        data=json.dumps(data, ensure_ascii=False).replace('</', '<\\/'),
    )


def main():
    cfg = ('/* Generated by tools/build_pages.py. Edit the values at the top of that file, then run it again. */\n'
           'window.GRIPLINE_CONFIG = {\n  mode: "demo",            /* "demo" = requests are kept in this browser only; "live" = real API at apiBase (docs/API.md) */\n'
           '  apiBase: "/api",\n  hours: { weekday: ["%s", "%s"], weekend: ["%s", "%s"] },\n  capacity: %d,             /* bays working at the same time */\n'
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
