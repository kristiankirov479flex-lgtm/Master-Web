"""Builds index.html (Bulgarian), en/index.html (English), js/config.js and css/style.css for VetDoma (a licensed vet who visits animals at home).
Edit the values in this file (services, prices, zones, vets, credentials, hours, texts), then run:  python tools/build_pages.py && python tools/build_privacy.py
Everything about the practice is an example (names, diplomas, registration numbers, prices): replace it for a real vet."""
import json, os
from html import escape as esc
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BRAND = 'VetDoma'

# ---------------- settings you will change for a real practice ----------------
HOURS = {'weekday': ['09:00', '18:00'], 'weekend': ['10:00', '14:00']}
CAPACITY = 2          # vets on the road at the same time
SLOT_MINUTES = 30
LEAD_MINUTES = 180    # a visit needs planning: three hours of notice
PHONE, PHONE_HREF, EMAIL = '+359 88 000 0000', '+359880000000', 'vet@example.com'
NIGHT_PHONE, NIGHT_HREF = '+359 88 000 0001', '+359880000001'     # a 24-hour clinic you refer to (example)
ADDRESS = {'bg': 'ул. Примерна 7, Пловдив (кабинет, само по уговорка)', 'en': '7 Primer St., Plovdiv (office, by appointment only)'}

# services at home: id, minutes, price in euro (None = decided at the visit), "from" price?, (bg name, en name), (bg text, en text)
SERVICES = [
 ('exam', 45, 30, False, ('Преглед у дома', 'Home check-up'), ('Преглед, съвет и план за лечение', 'An exam, advice and a treatment plan')),
 ('vacc', 40, 20, False, ('Ваксина у дома', 'Vaccination at home'), ('За едно животно. Второто е 15 €', 'For one animal. The second is €15')),
 ('senior', 60, 50, False, ('Преглед на възрастно животно', 'Senior animal check-up'), ('По-дълъг, без бързане, с разговор', 'Longer, unhurried, with a talk')),
 ('blood', 30, 25, False, ('Кръвна проба', 'Blood sample'), ('Взимаме у дома, резултат на следващия ден', 'Taken at home, result the next day')),
 ('wound', 45, 20, True, ('Превръзка и рани', 'Bandage and wounds'), ('Почистване, шев или превръзка', 'Cleaning, a stitch or a bandage')),
 ('drip', 60, 40, True, ('Инфузия и лечение у дома', 'Drip and treatment at home'), ('Когато е трудно да се пътува', 'When travelling is hard')),
 ('goodbye', 60, 60, True, ('Сбогуване у дома', 'Saying goodbye at home'), ('Спокойно и без бързане, на любимото място', 'Calm and unhurried, in the favourite place')),
 ('other', 45, None, False, ('Друго / не съм сигурен', 'Something else / not sure'), ('Опиши в бележката и ще се обадим', 'Describe it in the note and we will call')),
]
# zones: id, travel fee in euro, (bg name, en name), (bg places, en places)
ZONES = [
 ('z1', 15, ('Пловдив', 'Plovdiv'), ('В рамките на града', 'Within the city')),
 ('z2', 25, ('До 10 км от града', 'Up to 10 km from the city'), ('Марково, Брестник, Кукленско шосе', 'Markovo, Brestnik, Kuklen road')),
 ('z3', 40, ('До 25 км от града', 'Up to 25 km from the city'), ('Раковски, Първомай по уговорка', 'Rakovski, others by arrangement')),
]
SPECIES = [('dog', ('куче', 'dog'), ('Куче', 'Dog')), ('cat', ('котка', 'cat'), ('Котка', 'Cat')), ('other', ('друго', 'other'), ('Друго (заек, птица…)', 'Other (rabbit, bird…)'))]
# vets: photo, (bg title, en title), (bg name, en name), (bg role, en role), (bg bio, en bio), credentials [(bg, en), ...]
VETS = [('vet-woman', ('Д-р', 'Dr.'), ('Теодора Маринова', 'Teodora Marinova'), ('Ветеринарен лекар, 12 години опит', 'Veterinarian, 12 years of experience'),
         ('Работи с възрастни и уплашени животни. Идва без бързане и казва какво и защо прави.', 'Works with older and nervous animals. She comes without hurrying and says what she does and why.'),
         [('Магистър по ветеринарна медицина, 2012 г.', 'Master of Veterinary Medicine, 2012'), ('Член на ветеринарната колегия, рег. № 0000', 'Member of the veterinary chamber, reg. no. 0000'), ('Обучение по грижа за възрастни животни', 'Trained in care for older animals')]),
        ('vet-man', ('Д-р', 'Dr.'), ('Борис Андонов', 'Boris Andonov'), ('Ветеринарен лекар, 10 години опит', 'Veterinarian, 10 years of experience'),
         ('Ваксини, превръзки, кръвни проби и лечение у дома. Преди това е работил в клиника за спешни случаи.', 'Vaccines, bandages, blood samples and treatment at home. He previously worked in an emergency clinic.'),
         [('Магистър по ветеринарна медицина, 2014 г.', 'Master of Veterinary Medicine, 2014'), ('Член на ветеринарната колегия, рег. № 0000', 'Member of the veterinary chamber, reg. no. 0000'), ('Застраховка „професионална отговорност“', 'Professional liability insurance')])]

SKINS = [('forest', 'Гора', 'Forest', '#F3F8F5', '#2F6B4F'), ('navy', 'Синьо', 'Navy', '#F4F6FA', '#1F3F73'), ('copper', 'Мед', 'Copper', '#FBF6F1', '#8F4A22'),
         ('plum', 'Слива', 'Plum', '#FAF6FA', '#6F3A78'), ('night', 'Нощ', 'Night', '#101612', '#86D1A6')]


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
    nb = ' '

    def money(v, frm=False):
        if v is None:
            return t('по уговорка', 'by arrangement')
        s = ('%d' % v)
        pre = (t('от' + nb, 'from' + nb) if frm else '')
        return (pre + s + nb + '€') if bg else (pre + '€' + s)

    rows = ''.join('<tr><th scope="row">%s<small>%s · %s %s</small></th><td>%s</td></tr>' % (esc(s[4][i]), esc(s[5][i]), s[1], t('мин', 'min'), money(s[2], s[3])) for s in SERVICES)
    svc_opts = ''.join('<option value="%s" data-min="%d" data-price="%d" data-from="%d">%s</option>' % (s[0], s[1], s[2] or 0, 1 if (s[3] or s[2] is None) else 0, esc(s[4][i])) for s in SERVICES)
    zone_rows = ''.join('<tr><th scope="row">%s<small>%s</small></th><td>%s</td><td><a class="zlink" href="#book" data-zone="%s">%s</a></td></tr>' % (z[2][i], z[3][i], money(z[1]), z[0], t('Избери', 'Choose')) for z in ZONES)
    zone_opts = ''.join('<option value="%s" data-fee="%d">%s · %s</option>' % (z[0], z[1], z[2][i], money(z[1])) for z in ZONES)
    sp_radios = ''.join('<label class="opt"><input type="radio" name="species" value="%s"%s><span>%s</span></label>' % (s[0], ' checked' if n == 0 else '', s[2][i]) for n, s in enumerate(SPECIES))
    vets_html = ''.join('<li><figure>%s</figure><div><h3>%s %s</h3><p class="role">%s</p><p>%s</p><ul class="creds">%s</ul></div></li>' % (
        I(v[0], '%s %s' % (v[1][i], v[2][i]), '(min-width: 521px) 170px, calc(100vw - 82px)'), v[1][i], v[2][i], v[3][i], v[4][i], ''.join('<li>%s</li>' % c[i] for c in v[5])) for v in VETS)
    trust = [(t('Лицензирани лекари', 'Licensed vets'), t('Двама ветеринарни лекари с регистрация и застраховка. Идва лекар, не помощник.', 'Two registered, insured vets. A vet comes, not an assistant.')),
             (t('Мобилен кабинет', 'A mobile practice'), t('Носим ваксини в хладилна чанта, оборудване за кръвни проби, превръзки и стерилни инструменти.', 'We bring vaccines in a cold bag, blood-sample equipment, dressings and sterile instruments.')),
             (t('Цена предварително', 'The price beforehand'), t('Преглед плюс пътуване: сумата е известна преди да дойдем. Ако трябва още нещо, питаме първо.', 'The visit plus travel: the sum is known before we come. If something more is needed, we ask first.')),
             (t('Резюме и план', 'A summary and a plan'), t('След посещението получаваш писмено резюме и кога да се обадиш отново.', 'After the visit you get a written summary and when to call again.'))]
    trust_html = ''.join('<li><h3>%s</h3><p>%s</p></li>' % x for x in trust)
    who = [(t('Възрастни животни', 'Older animals'), t('Пътуването е уморително и болезнено. Прегледът у дома е по-кратък за тях.', 'Travel is tiring and painful for them. A check-up at home is gentler.')),
           (t('Уплашени животни', 'Nervous animals'), t('Кабинетът е шумен и непознат. У дома животното е спокойно и лекуването е по-безопасно.', 'A practice is noisy and unfamiliar. At home the animal is calm and treatment is safer.')),
           (t('Много животни', 'Several animals'), t('Три котки или две кучета? Идваме веднъж и ги преглеждаме всички.', 'Three cats or two dogs? We come once and see them all.')),
           (t('Стопани без кола', 'Owners without a car'), t('Или с малко дете, или в болест. Не е нужно да мислиш как да пътуваш.', 'Or with a small child, or when ill. You do not need to think about how to travel.'))]
    who_html = ''.join('<li><h3>%s</h3><p>%s</p></li>' % w for w in who)
    kit = [t('Стетоскоп, отоскоп и термометър', 'A stethoscope, otoscope and thermometer'), t('Ваксини в хладилна чанта', 'Vaccines in a cold bag'), t('Оборудване за кръвни проби, резултат на следващия ден', 'Blood-sample equipment, result the next day'),
           t('Превръзки, шевове и стерилни инструменти', 'Dressings, stitches and sterile instruments'), t('Ръкавици, игли и подложки за еднократна употреба', 'Single-use gloves, needles and mats'), t('Лекарства за най-честите случаи', 'Medicines for the most common cases')]
    kit_html = ''.join('<li>%s</li>' % k for k in kit)
    steps = [(t('Обаждаш се или заявяваш', 'You call or book'), t('Казваш какво се е случило и къде живееш. Получаваш цена с пътуването.', 'You tell us what happened and where you live. You get a price with the travel.')),
             (t('Идваме в уговорения час', 'We come at the agreed time'), t('Идва лекарят, който си избрал или който е свободен. Носи всичко необходимо.', 'The vet you chose or the one who is free comes. They bring everything needed.')),
             (t('Оставаме колкото трябва', 'We stay as long as needed'), t('Обясняваме, показваме как да даваш лекарството и казваме кога да се обадиш пак.', 'We explain, show you how to give the medicine and say when to call again.'))]
    steps_html = ''.join('<li><b>%d</b><div><h3>%s</h3><p>%s</p></div></li>' % (n + 1, a, b) for n, (a, b) in enumerate(steps))
    faq = [(t('Идвате ли при спешен случай?', 'Do you come in an emergency?'), t('Не сме денонощна служба. През деня се опитваме да дойдем възможно най-бързо, ако се обадиш. През нощта се обади на денонощната клиника, чийто телефон е в горната част на страницата.', 'We are not a 24-hour service. During the day we try to come as fast as we can if you call. At night call the 24-hour clinic whose number is at the top of the page.')),
           (t('Колко струва, ако не знам какво е?', 'What does it cost if I do not know what it is?'), t('Цената на прегледа и пътуването е известна предварително. Ако е нужно още нещо, казваме цената преди да го направим.', 'The price of the exam and the travel is known beforehand. If something more is needed we tell you the price before we do it.')),
           (t('Има ли неща, които не може да се направят у дома?', 'Are there things that cannot be done at home?'), t('Да: ехография, рентген, операции. Тогава те насочваме към клиника и казваме на кого да се обадиш.', 'Yes: ultrasound, X-rays, surgery. Then we send you to a clinic and tell you whom to call.')),
           (t('Имате ли селскостопански животни?', 'Do you treat farm animals?'), t('Не по правило. Обади се и ще те насочим към ветеринар за селскостопански животни в твоя район.', 'Not as a rule. Call and we will point you to a farm-animal vet in your area.'))]
    faq_html = ''.join('<details class="qa"><summary>%s</summary><p>%s</p></details>' % f for f in faq)
    hours_rows = [(t('Понеделник – петък', 'Monday – Friday'), HOURS['weekday'], 'wd'), (t('Събота и неделя', 'Saturday and Sunday'), HOURS['weekend'], 'we')]
    hours_html = ''.join('<div data-hrs="%s"><dt>%s</dt><dd>%s – %s</dd></div>' % (k, n, h[0], h[1]) for n, h, k in hours_rows)
    hours_ld = '"Mo-Fr %s-%s","Sa-Su %s-%s"' % (HOURS['weekday'][0], HOURS['weekday'][1], HOURS['weekend'][0], HOURS['weekend'][1])
    swatches = ''.join('<button class="sw" type="button" data-skin="%s" style="--s1:%s;--s2:%s" aria-pressed="false" aria-label="%s"></button>' % (k, s1, s2, b if bg else e) for k, b, e, s1, s2 in SKINS)
    nav = [('#team', t('Лекари', 'Our vets')), ('#how', t('Как става', 'How it works')), ('#prices', t('Цени', 'Prices')), ('#book', t('Заяви посещение', 'Ask for a visit')), ('#visit', t('Контакти', 'Contact'))]
    nav_html = ''.join('<a href="%s">%s</a>' % n for n in nav)
    data = {'services': {s[0]: s[4][i] for s in SERVICES}, 'species': {s[0]: s[1][i] for s in SPECIES}, 'zones': {z[0]: z[2][i] for z in ZONES}}

    title = t('VetDoma – ветеринарен лекар у дома в Пловдив. Заяви посещение онлайн', 'VetDoma – a licensed vet who comes to your home in Plovdiv. Ask for a visit online')
    desc = t('VetDoma: лицензирани ветеринарни лекари, които идват у дома в Пловдив и района. Преглед, ваксини, кръвни проби и грижа за възрастни животни. Цената е известна предварително.',
             'VetDoma: licensed vets who come to your home in Plovdiv and the area. Check-ups, vaccines, blood samples and care for older animals. The price is known beforehand.')

    return '''<!doctype html>
<html lang="%(lang)s" data-skin="forest">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="theme-color" content="#F3F8F5">
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
     and an og:image (images/stock/cat-home.jpg is a placeholder) -->
<link rel="preload" href="%(root)sfonts/source-sans-3-400-600-%(script)s.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="%(root)sfonts/fonts.css">
<link rel="stylesheet" href="%(root)scss/style.css">
<script>
  /* Apply the saved colour scheme before the page paints, so it does not flash. */
  try { var s = new URLSearchParams(location.search).get("skin") || localStorage.getItem("vetdomaSkin"); if (s) document.documentElement.dataset.skin = s; } catch (e) {}
</script>
<script type="application/ld+json">
{"@context":"https://schema.org","@type":"VeterinaryCare","name":"%(brand)s","inLanguage":"%(lang)s","telephone":"%(phone_href)s","email":"%(email)s",
 "areaServed":"Plovdiv","address":{"@type":"PostalAddress","streetAddress":"Primer St. 7","addressLocality":"Plovdiv","addressCountry":"BG"},"openingHours":[%(hours_ld)s]}
</script>
</head>
<body>
<a class="skip" href="#main">%(skip)s</a>

<aside class="topbar" aria-label="%(topbar_l)s">
  <ul class="wrap topbar-in">
    <li><b>%(ib1_k)s</b> <span id="todayHours">09:00 – 18:00</span></li>
    <li><b>%(ib2_k)s</b> <span>%(ib2_v)s</span></li>
    <li><b>%(ib3_k)s</b> <a href="tel:%(night_href)s">%(night_phone)s</a></li>
  </ul>
</aside>
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
    <div class="wrap hero-in">
      <figure class="hero-ph">%(hero_img)s</figure>
      <div class="hero-copy">
        <p class="eyebrow">%(eyebrow)s</p>
        <h1 id="h1">%(h1)s</h1>
        <p class="lead">%(lead)s</p>
        <p class="hero-links"><a class="btn btn-main" href="#book">%(cta1)s</a> <a class="btn btn-line" href="tel:%(phone_href)s">%(cta2)s</a></p>
        <p class="hero-note">%(hero_note)s</p>
      </div>
    </div>
  </section>

  <!-- ============ Why trust us ============ -->
  <section class="trustbar" aria-labelledby="tr-h">
    <div class="wrap">
      <h2 id="tr-h" class="sr-only">%(trust_h)s</h2>
      <ul class="trust">%(trust_html)s</ul>
    </div>
  </section>

  <!-- ============ Vets ============ -->
  <section class="block" id="team" aria-labelledby="tm-h">
    <div class="wrap">
      <header class="sec-head">
        <h2 id="tm-h">%(team_h)s</h2>
        <p>%(team_p)s</p>
      </header>
      <ul class="vets">%(vets_html)s</ul>
      <p class="p-note">%(team_note)s</p>
    </div>
  </section>

  <!-- ============ Who ============ -->
  <section class="block soft" id="who" aria-labelledby="wh-h">
    <div class="wrap">
      <header class="sec-head"><h2 id="wh-h">%(who_h)s</h2><p>%(who_p)s</p></header>
      <ul class="who">%(who_html)s</ul>
    </div>
  </section>

  <!-- ============ Kit ============ -->
  <section class="block" aria-labelledby="kt-h">
    <div class="wrap kit">
      <div>
        <header class="sec-head"><h2 id="kt-h">%(kit_h)s</h2><p>%(kit_p)s</p></header>
        <ul class="ticks">%(kit_html)s</ul>
      </div>
      <figure class="kit-ph">%(kit_img)s</figure>
    </div>
  </section>

  <!-- ============ How ============ -->
  <section class="block soft" id="how" aria-labelledby="hw-h">
    <div class="wrap how">
      <div>
        <header class="sec-head"><h2 id="hw-h">%(how_h)s</h2><p>%(how_p)s</p></header>
        <ol class="steps3">%(steps_html)s</ol>
      </div>
      <figure class="how-ph">%(how_img)s</figure>
    </div>
  </section>

  <!-- ============ Prices ============ -->
  <section class="block" id="prices" aria-labelledby="pr-h">
    <div class="wrap">
      <header class="sec-head"><h2 id="pr-h">%(prices_h)s</h2><p>%(prices_p)s</p></header>
      <div class="prices">
        <div>
          <h3>%(zones_h)s</h3>
          <table class="plist zones"><caption class="sr-only">%(zones_h)s</caption><tbody>%(zone_rows)s</tbody></table>
        </div>
        <div>
          <h3>%(svc_h)s</h3>
          <table class="plist"><caption class="sr-only">%(svc_h)s</caption><tbody>%(rows)s</tbody></table>
          <p class="p-note sv-note">%(sv_note)s</p>
        </div>
      </div>
    </div>
  </section>

  <!-- ============ Book ============ -->
  <section class="block soft" id="book" aria-labelledby="bk-h">
    <div class="wrap narrow">
      <header class="sec-head">
        <h2 id="bk-h">%(book_h)s</h2>
        <p>%(book_p)s</p>
      </header>
      <form class="res" id="apptForm" novalidate>
        <fieldset class="group"><legend>%(f_species)s</legend>
          <div class="opts">%(sp_radios)s</div>
        </fieldset>
        <div class="row2">
          <div class="field"><label for="f-pet">%(f_pet)s</label><input id="f-pet" name="pet" type="text" autocomplete="off"></div>
          <div class="field"><label for="f-service">%(f_service)s</label><select id="f-service" name="service">%(svc_opts)s</select></div>
        </div>
        <div class="row2">
          <div class="field"><label for="f-zone">%(f_zone)s</label><select id="f-zone" name="zone">%(zone_opts)s</select></div>
          <div class="field"><label for="f-address">%(f_address)s</label><input id="f-address" name="address" type="text" autocomplete="street-address" required></div>
        </div>
        <p class="estimate" id="estimate" role="status"></p>
        <div class="row2">
          <div class="field"><label for="f-date">%(f_date)s</label><input id="f-date" name="date" type="date" required></div>
          <div class="field"><label for="f-time">%(f_time)s</label><select id="f-time" name="time" required></select></div>
        </div>
        <p class="hint" id="timeHint" role="status">%(checking)s</p>
        <div class="row2">
          <div class="field"><label for="f-name">%(f_name)s</label><input id="f-name" name="name" type="text" autocomplete="name" required></div>
          <div class="field"><label for="f-phone">%(f_phone)s</label><input id="f-phone" name="phone" type="tel" autocomplete="tel" required></div>
        </div>
        <div class="field"><label for="f-msg">%(f_msg)s</label><textarea id="f-msg" name="msg" rows="3"></textarea><p class="hint">%(f_msg_h)s</p></div>
        <p class="demo-note" id="demoNote" hidden></p>
        <p class="form-error" id="aError" role="alert" hidden></p>
        <button class="btn btn-main" type="submit" id="aSend">%(f_send)s</button>
        <small class="fine">%(f_note)s <a href="%(privacy_href)s">%(f_priv)s</a></small>
      </form>
      <div class="done" id="aDone" hidden tabindex="-1"></div>
    </div>
  </section>

  <!-- ============ FAQ ============ -->
  <section class="block" aria-labelledby="fq-h">
    <div class="wrap narrow">
      <header class="sec-head"><h2 id="fq-h">%(faq_h)s</h2></header>
      <div class="qas">%(faq_html)s</div>
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
          <li><b>%(l_night)s</b><a href="tel:%(night_href)s">%(night_phone)s</a></li>
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
    <span>© <span id="year">2026</span> VetDoma. %(foot_demo)s</span>
    <span class="foot-links"><a href="%(privacy_href)s">%(f_priv)s</a> <a href="%(admin_href)s">%(admin_l)s</a></span>
  </div>
</footer>

<aside class="dock" aria-label="%(dock_label)s">
  <div class="dock-label"><small>%(dock_label)s</small><b id="skinName">%(skin_name)s</b></div>
  <div class="swatches">%(swatches)s</div>
</aside>

<script type="application/json" id="vetdomaData">%(data)s</script>
<script src="%(root)sjs/config.js"></script>
<script src="%(root)sjs/api.js"></script>
<script src="%(root)sjs/main.js"></script>
</body>
</html>
''' % dict(
        lang=lang, title=esc(title), desc=esc(desc), root=root, script=script, brand=BRAND, brand_html='Vet<span>Doma</span>', phone_href=PHONE_HREF, phone=PHONE, email=EMAIL, hours_ld=hours_ld,
        night_href=NIGHT_HREF, night_phone=NIGHT_PHONE,
        skip=t('Към съдържанието', 'Skip to content'), nav_label=t('Навигация', 'Navigation'), nav_html=nav_html, call_l=t('Обади се', 'Call'),
        other_href=other_href, other_lang='en' if bg else 'bg', other_label='EN' if bg else 'БГ', other_aria='Switch to English' if bg else 'Превключи на български', menu_btn=t('Меню', 'Menu'),
        topbar_l=t('Работно време и спешни случаи', 'Opening hours and emergencies'), ib1_k=t('Посещения днес', 'Visits today'), ib2_k=t('Район', 'Area'), ib2_v=t('Пловдив и до 25 км', 'Plovdiv and up to 25 km'), ib3_k=t('Нощем:', 'At night:'),
        eyebrow=t('Ветеринарен лекар у дома · Пловдив', 'A vet at your home · Plovdiv'),
        h1=t('Лекар за животното ти, у дома, без стрес', 'A doctor for your animal, at home, without stress'),
        lead=t('Лицензирани ветеринарни лекари идват при теб в Пловдив и района. Мобилен кабинет, цена с пътуването предварително и писмено резюме след посещението.', 'Licensed vets come to you in Plovdiv and the area. A mobile practice, a price with travel beforehand and a written summary after the visit.'),
        cta1=t('Заяви посещение', 'Ask for a visit'), cta2=t('Обади се', 'Call us'),
        hero_note=t('Не сме денонощна служба. При спешен случай през нощта се обади на денонощната клиника.', 'We are not a 24-hour service. In a night emergency call the 24-hour clinic.'),
        hero_img=I('cat-home', t('Ветеринарка гали котка у дома до прозорец', 'A vet stroking a tabby cat at home by a window'), '(min-width: 900px) 540px, calc(100vw - 40px)', eager=True),
        trust_h=t('Защо ни се доверяват', 'Why owners trust us'), trust_html=trust_html,
        team_h=t('Лекарите, които ще дойдат при теб', 'The vets who will come to you'), team_p=t('Два лица, една практика. Знаеш кой ще почука на вратата и какъв е опитът му.', 'Two faces, one practice. You know who will knock on your door and what experience they have.'), vets_html=vets_html,
        team_note=t('Имена, дипломи и регистрационни номера са примерни.', 'Names, diplomas and registration numbers are examples.'),
        who_h=t('Кога посещението у дома е най-добро', 'When a home visit is best'), who_p=t('Не за всяко животно е добре да пътува. Ето кога да ни повикаш.', 'Not every animal should travel. This is when to call us.'), who_html=who_html,
        kit_h=t('Какво носим', 'What we bring'), kit_p=t('Повечето неща, които се правят в кабинета, можем да направим и у вас.', 'Most things that are done in a practice we can do at your home.'), kit_html=kit_html,
        kit_img=I('corgi', t('Ветеринарен лекар с маска до коргито', 'A vet in a mask beside a corgi'), '(min-width: 900px) 530px, calc(100vw - 40px)'),
        how_h=t('Как става', 'How it works'), how_p=t('Три стъпки, без чакалня.', 'Three steps, no waiting room.'), steps_html=steps_html,
        how_img=I('puppy-floor', t('Кученце лежи на пода, а ръка му дава лакомство', 'A puppy lying on the floor while a hand offers a treat'), '(min-width: 900px) 460px, calc(100vw - 40px)'),
        prices_h=t('Цени', 'Prices'), prices_p=t('Цената е посещението плюс пътуването според района. Всичко е в евро. Ако не си сигурен къде си, питай по телефона.', 'The price is the visit plus the travel for your area. Everything is in euros. If you are not sure which area you are in, ask by phone.'),
        zones_h=t('Пътуване', 'Travel'), svc_h=t('Посещения', 'Visits'), zone_rows=zone_rows, rows=rows,
        sv_note=t('Плащане в брой или с карта след посещението. Лекарствата се плащат отделно.', 'Payment by cash or card after the visit. Medicines are paid separately.'),
        book_h=t('Заяви посещение', 'Ask for a visit'), book_p=t('Избери животно, повод, район, ден и час. Виждаш ориентировъчна цена. Ще ти се обадим, за да потвърдим.', 'Choose the animal, the reason, the area, a day and a time. You see an estimated price. We will call you to confirm.'),
        f_species=t('Кое животно?', 'Which animal?'), sp_radios=sp_radios, f_pet=t('Име на животното', 'Animal’s name'), f_service=t('Повод', 'Reason'), svc_opts=svc_opts, f_zone=t('Район', 'Area'), zone_opts=zone_opts,
        f_address=t('Адрес', 'Address'), f_date=t('Дата', 'Date'), f_time=t('Час', 'Time'),
        checking=t('Избери повод и дата, за да видиш свободните часове.', 'Choose a reason and a date to see the free times.'),
        f_name=t('Твоето име', 'Your name'), f_phone=t('Телефон', 'Phone'), f_msg=t('Бележка (по желание)', 'Note (optional)'), f_msg_h=t('Например: възраст, от кога е проблемът, етаж, вход, кодът на входа.', 'For example: age, how long the problem has lasted, floor, entrance, door code.'),
        f_send=t('Заяви посещение', 'Request the visit'), f_note=t('Не е нужно да плащаш предварително.', 'You do not have to pay in advance.'), f_priv=t('Поверителност', 'Privacy'), privacy_href='privacy.html',
        faq_h=t('Често задавани въпроси', 'Common questions'), faq_html=faq_html,
        visit_h=t('Контакти', 'Contact'), hours_html=hours_html, l_addr=t('Кабинет', 'Office'), l_phone=t('Телефон', 'Phone'), l_night=t('Денонощна клиника', '24-hour clinic'), l_email=t('Имейл', 'Email'), address=ADDRESS['bg' if bg else 'en'],
        visit_note=t('Приемаме заявки всеки ден. Посещения: делнични дни 09:00 – 18:00, събота и неделя 10:00 – 14:00.', 'We take requests every day. Visits: weekdays 09:00 – 18:00, Saturday and Sunday 10:00 – 14:00.'),
        map_t=t('Картата се зарежда от OpenStreetMap едва когато я поискаш.', 'The map loads from OpenStreetMap only when you ask for it.'), map_btn=t('Покажи картата', 'Show the map'),
        foot_demo=t('Всичко тук е пример.', 'Everything here is an example.'), admin_href='admin.html' if bg else '../admin.html?lang=en', admin_l=t('Демо админ панел', 'Demo back office'),
        dock_label=t('Цветова схема', 'Colour scheme'), skin_name=t('Гора', 'Forest'), swatches=swatches,
        data=json.dumps(data, ensure_ascii=False).replace('</', '<\\/'),
    )


def main():
    cfg = ('/* Generated by tools/build_pages.py. Edit the values at the top of that file, then run it again. */\n'
           'window.VETDOMA_CONFIG = {\n  mode: "demo",            /* "demo" = requests are kept in this browser only; "live" = real API at apiBase (docs/API.md) */\n'
           '  apiBase: "/api",\n  hours: { weekday: ["%s", "%s"], weekend: ["%s", "%s"] },\n  capacity: %d,             /* vets on the road at the same time */\n'
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
