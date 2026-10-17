"""Builds index.html (Bulgarian), en/index.html (English), js/config.js and css/style.css for Lapa Vet (a veterinary clinic that looks like a doctor's practice).
Edit the values in this file (services, prices, vets, credentials, hours, texts), then run:  python tools/build_pages.py && python tools/build_privacy.py
Everything about the clinic is an example (names, diplomas, registration numbers, prices): replace it for a real clinic."""
import json, os
from html import escape as esc
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BRAND = 'Lapa Vet'

# ---------------- settings you will change for a real clinic ----------------
HOURS = {'weekday': ['09:00', '19:00'], 'weekend': ['10:00', '14:00']}
CAPACITY = 2          # vets seeing animals at the same time
SLOT_MINUTES = 30
LEAD_MINUTES = 60
PHONE, PHONE_HREF, EMAIL = '+359 88 000 0000', '+359880000000', 'clinic@example.com'
NIGHT_PHONE, NIGHT_HREF = '+359 88 000 0001', '+359880000001'     # a 24-hour clinic you refer to (example)
ADDRESS = {'bg': 'ул. Примерна 21, Пловдив', 'en': '21 Primer St., Plovdiv'}

# services: id, group, minutes, price in euro (None = decided at the exam), "from" price?, (bg name, en name), (bg text, en text)
SERVICES = [
 ('exam', 'prev', 30, 25, False, ('Преглед', 'Check-up'), ('Куче или коте, с разговор и съвет', 'Dog or cat, with a talk and advice')),
 ('vdog', 'prev', 30, 20, False, ('Ваксина за куче', 'Dog vaccination'), ('Комплексна ваксина и ваксина срещу бяс', 'Combined vaccine and rabies vaccine')),
 ('vcat', 'prev', 30, 18, False, ('Ваксина за коте или котка', 'Cat vaccination'), ('Комплексна ваксина, по желание и срещу бяс', 'Combined vaccine, rabies on request')),
 ('chip', 'prev', 30, 15, False, ('Чип и паспорт', 'Microchip and passport'), ('Поставяне на чип и регистрация', 'Chip implant and registration')),
 ('worm', 'prev', 30, 12, False, ('Обезпаразитяване', 'Parasite treatment'), ('Препарат според теглото', 'A product chosen for the weight')),
 ('scan', 'diag', 30, 30, False, ('Ехография', 'Ultrasound scan'), ('Корем, сърце или бременност', 'Abdomen, heart or pregnancy')),
 ('blood', 'diag', 30, 35, True, ('Кръвни изследвания', 'Blood tests'), ('Резултат в същия ден, в нашата лаборатория', 'Result the same day, in our own lab')),
 ('dental', 'surg', 60, 60, True, ('Почистване на зъбен камък', 'Dental cleaning'), ('Под седация, с преглед преди това', 'Under sedation, with an exam before')),
 ('neuter', 'surg', 60, 70, True, ('Кастрация или стерилизация', 'Neutering'), ('Предварителен преглед и кръвни изследвания', 'A pre-visit exam and blood tests')),
 ('other', None, 30, None, False, ('Друго / не съм сигурен', 'Something else / not sure'), ('Опиши в бележката, ние ще преценим', 'Describe it in the note and we will decide')),
]
GROUPS = [('prev', ('Профилактика', 'Prevention')), ('diag', ('Диагностика', 'Diagnostics')), ('surg', ('Зъби и хирургия', 'Dental and surgery'))]
SPECIES = [('dog', ('куче', 'dog'), ('Куче', 'Dog')), ('cat', ('котка', 'cat'), ('Котка', 'Cat')), ('other', ('друго', 'other'), ('Друго (заек, птица…)', 'Other (rabbit, bird…)'))]
# vets: photo, (bg title, en title), (bg name, en name), (bg role, en role), (bg bio, en bio), credentials [(bg, en), ...]
VETS = [('vet-woman', ('Д-р', 'Dr.'), ('Мария Георгиева', 'Maria Georgieva'), ('Ветеринарен лекар, 11 години опит', 'Veterinarian, 11 years of experience'),
         ('Котки, кучета, ваксини и профилактика. Обяснява всичко простичко и не бърза.', 'Cats, dogs, vaccines and prevention. She explains everything simply and never hurries.'),
         [('Магистър по ветеринарна медицина, 2013 г.', 'Master of Veterinary Medicine, 2013'), ('Член на ветеринарната колегия, рег. № 0000', 'Member of the veterinary chamber, reg. no. 0000'), ('Обучение за спокойна работа с животни', 'Trained in calm, low-stress handling')]),
        ('vet-man', ('Д-р', 'Dr.'), ('Стефан Колев', 'Stefan Kolev'), ('Ветеринарен хирург, 9 години опит', 'Veterinary surgeon, 9 years of experience'),
         ('Кастрации, зъби, рани и ехография. Работи бавно и обяснява плана преди операция.', 'Neutering, teeth, wounds and ultrasound. He works slowly and explains the plan before surgery.'),
         [('Магистър по ветеринарна медицина, 2015 г.', 'Master of Veterinary Medicine, 2015'), ('Член на ветеринарната колегия, рег. № 0000', 'Member of the veterinary chamber, reg. no. 0000'), ('Следдипломно обучение по мека тъканна хирургия', 'Postgraduate training in soft tissue surgery')])]
VACC = [(('Куче', 'Dog'), [(('6–8 седмици', '6–8 weeks'), ('Първа комплексна ваксина', 'First combined vaccine')), (('10–12 седмици', '10–12 weeks'), ('Втора комплексна ваксина', 'Second combined vaccine')),
                          (('14–16 седмици', '14–16 weeks'), ('Трета ваксина и ваксина срещу бяс', 'Third vaccine and rabies')), (('Всяка година', 'Every year'), ('Ревакцинация', 'Booster'))]),
        (('Коте', 'Cat'), [(('8–9 седмици', '8–9 weeks'), ('Първа комплексна ваксина', 'First combined vaccine')), (('12 седмици', '12 weeks'), ('Втора ваксина, по желание и срещу бяс', 'Second vaccine, rabies on request')),
                           (('Всяка година', 'Every year'), ('Ревакцинация', 'Booster'))])]

SKINS = [('teal', 'Тюркоаз', 'Teal', '#F4F8F8', '#116466'), ('navy', 'Синьо', 'Navy', '#F4F6FA', '#1F3F73'), ('forest', 'Гора', 'Forest', '#F4F8F4', '#2F6B4F'),
         ('burgundy', 'Бордо', 'Burgundy', '#FAF5F5', '#7A2433'), ('night', 'Нощ', 'Night', '#0F1A1B', '#6FC9CB')]


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
            return t('по преглед', 'after the exam')
        s = ('%d' % v)
        pre = (t('от' + nb, 'from' + nb) if frm else '')
        return (pre + s + nb + '€') if bg else (pre + '€' + s)

    def srow(s):
        return '<tr><th scope="row">%s<small>%s · %s %s</small></th><td>%s</td></tr>' % (esc(s[5][i]), esc(s[6][i]), s[2], t('мин', 'min'), money(s[3], s[4]))
    groups_html = ''.join('<div class="sgroup"><h3>%s</h3><table class="plist"><caption class="sr-only">%s</caption><tbody>%s</tbody></table></div>' % (g[1][i], g[1][i], ''.join(srow(s) for s in SERVICES if s[1] == g[0])) for g in GROUPS)
    svc_opts = ''.join('<option value="%s" data-min="%d">%s</option>' % (s[0], s[2], esc(s[5][i])) for s in SERVICES)
    sp_radios = ''.join('<label class="opt"><input type="radio" name="species" value="%s"%s><span>%s</span></label>' % (s[0], ' checked' if n == 0 else '', s[2][i]) for n, s in enumerate(SPECIES))
    vets_html = ''.join('<li><figure>%s</figure><div><h3>%s %s</h3><p class="role">%s</p><p>%s</p><ul class="creds">%s</ul></div></li>' % (
        I(v[0], '%s %s' % (v[1][i], v[2][i]), '(min-width: 521px) 150px, calc(100vw - 82px)'), v[1][i], v[2][i], v[3][i], v[4][i], ''.join('<li>%s</li>' % c[i] for c in v[5])) for v in VETS)
    trust = [(t('2 лекари', '2 vets'), t('11 и 9 години опит. При всяко посещение знаеш кой ще прегледа животното.', '11 and 9 years of experience. At every visit you know who will see the animal.')),
             (t('Всичко на място', 'Everything on site'), t('Лаборатория, ехограф и операционна. Не те пращаме на друго място за основните неща.', 'A lab, an ultrasound machine and an operating room. We do not send you elsewhere for the basics.')),
             (t('Цена преди лечение', 'Price before treatment'), t('Казваме цената преди да започнем и не добавяме нищо без твоето съгласие.', 'We tell you the price before we start and add nothing without your consent.')),
             (t('Писмено резюме', 'A written summary'), t('След всяко посещение получаваш кратко резюме: какво намерихме и какво да правиш.', 'After every visit you get a short summary: what we found and what to do.'))]
    trust_html = ''.join('<li><h3>%s</h3><p>%s</p></li>' % x for x in trust)
    care = [(t('Първо разговор', 'A talk first'), t('Питаме какво си забелязал и от кога. Едва след това преглеждаме.', 'We ask what you noticed and since when. Only then do we examine.')),
            (t('Съгласие преди процедура', 'Consent before a procedure'), t('Обясняваме какво ще правим, колко струва и какви са рисковете. Започваме, когато кажеш „да“.', 'We explain what we will do, what it costs and the risks. We begin when you say yes.')),
            (t('Чисто и стерилно', 'Clean and sterile'), t('Игли и ръкавици за еднократна употреба. Масата се дезинфекцира след всяко животно.', 'Single-use needles and gloves. The table is disinfected after every animal.')),
            (t('Котки и кучета отделно', 'Cats and dogs apart'), t('Котките имат свой час за изчакване, далеч от лаещите кучета. Попитай при записване.', 'Cats have their own waiting time, away from barking dogs. Ask when you book.'))]
    care_html = ''.join('<li><h3>%s</h3><p>%s</p></li>' % x for x in care)
    bring = [t('Ваксинационната книжка или паспорта', 'The vaccination booklet or passport'), t('Стари изследвания, ако има', 'Old test results, if you have any'), t('Пресен проба от урина или изпражнения, ако е за това', 'A fresh urine or stool sample, if it is for that'),
             t('Каишка за кучето, транспортна чанта за котката', 'A lead for the dog, a carrier for the cat'), t('Кога за последно е ял и пил', 'When it last ate and drank')]
    bring_html = ''.join('<li>%s</li>' % b for b in bring)
    vacc_html = ''.join('<div class="vcard"><h3>%s</h3><ol>%s</ol></div>' % (grp[i], ''.join('<li><b>%s</b><span>%s</span></li>' % (a[i], b[i]) for a, b in steps)) for grp, steps in VACC)
    faq = [(t('Приемате ли без час?', 'Do you see animals without an appointment?'), t('Да, ако има свободен лекар. Със запазен час не чакаш. При спешен случай ни се обади и те чакаме.', 'Yes, if a vet is free. With an appointment you do not wait. In an emergency call us and we expect you.')),
           (t('Колко е първият преглед?', 'How much is a first visit?'), t('25 €. Ако е нужно още нещо (изследване, лекарство), казваме цената преди да го направим.', '€25. If something more is needed (a test, a medicine) we tell you the price before we do it.')),
           (t('Работите ли нощем?', 'Are you open at night?'), t('Не. През нощта и в неделя те пренасочваме към денонощна клиника, чийто телефон е в горната част на страницата.', 'No. At night and on Sundays we send you to a 24-hour clinic whose phone number is at the top of the page.')),
           (t('Лекувате ли екзотични животни?', 'Do you treat exotic animals?'), t('Зайци и морски свинчета: да. Птици и влечуги: обади се първо, за да кажем дали можем да помогнем.', 'Rabbits and guinea pigs: yes. Birds and reptiles: please call first and we will say whether we can help.'))]
    faq_html = ''.join('<details class="qa"><summary>%s</summary><p>%s</p></details>' % f for f in faq)
    hours_rows = [(t('Понеделник – петък', 'Monday – Friday'), HOURS['weekday'], 'wd'), (t('Събота и неделя', 'Saturday and Sunday'), HOURS['weekend'], 'we')]
    hours_html = ''.join('<div data-hrs="%s"><dt>%s</dt><dd>%s – %s</dd></div>' % (k, n, h[0], h[1]) for n, h, k in hours_rows)
    hours_ld = '"Mo-Fr %s-%s","Sa-Su %s-%s"' % (HOURS['weekday'][0], HOURS['weekday'][1], HOURS['weekend'][0], HOURS['weekend'][1])
    swatches = ''.join('<button class="sw" type="button" data-skin="%s" style="--s1:%s;--s2:%s" aria-pressed="false" aria-label="%s"></button>' % (k, s1, s2, b if bg else e) for k, b, e, s1, s2 in SKINS)
    nav = [('#team', t('Лекари', 'Our vets')), ('#services', t('Услуги и цени', 'Services and prices')), ('#care', t('Първо посещение', 'First visit')), ('#book', t('Запази час', 'Book')), ('#visit', t('Контакти', 'Contact'))]
    nav_html = ''.join('<a href="%s">%s</a>' % n for n in nav)
    data = {'services': {s[0]: s[5][i] for s in SERVICES}, 'species': {s[0]: s[1][i] for s in SPECIES}}

    title = t('Lapa Vet – ветеринарна клиника в Пловдив. Запази час онлайн', 'Lapa Vet – veterinary clinic in Plovdiv. Book an appointment online')
    desc = t('Lapa Vet е ветеринарна клиника за кучета и котки в Пловдив: двама опитни лекари, лаборатория, ехограф и операционна на място. Виж цените и запази час.',
             'Lapa Vet is a veterinary clinic for dogs and cats in Plovdiv: two experienced vets, with a lab, ultrasound and operating room on site. See the prices and book an appointment.')

    return '''<!doctype html>
<html lang="%(lang)s" data-skin="teal">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="theme-color" content="#F4F8F8">
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
     and an og:image (images/stock/dachshund.jpg is a placeholder) -->
<link rel="preload" href="%(root)sfonts/alegreya-%(script)s.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="%(root)sfonts/fonts.css">
<link rel="stylesheet" href="%(root)scss/style.css">
<script>
  /* Apply the saved colour scheme before the page paints, so it does not flash. */
  try { var s = new URLSearchParams(location.search).get("skin") || localStorage.getItem("lapaSkin"); if (s) document.documentElement.dataset.skin = s; } catch (e) {}
</script>
<script type="application/ld+json">
{"@context":"https://schema.org","@type":"VeterinaryCare","name":"%(brand)s","inLanguage":"%(lang)s","telephone":"%(phone_href)s","email":"%(email)s",
 "address":{"@type":"PostalAddress","streetAddress":"Primer St. 21","addressLocality":"Plovdiv","addressCountry":"BG"},"openingHours":[%(hours_ld)s]}
</script>
</head>
<body>
<a class="skip" href="#main">%(skip)s</a>

<aside class="topbar" aria-label="%(topbar_l)s">
  <ul class="wrap topbar-in">
    <li><b>%(ib1_k)s</b> <span id="todayHours">09:00 – 19:00</span></li>
    <li><span>%(address)s</span></li>
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
      <div class="hero-copy">
        <p class="eyebrow">%(eyebrow)s</p>
        <h1 id="h1">%(h1)s</h1>
        <p class="lead">%(lead)s</p>
        <p class="hero-links"><a class="btn btn-main" href="#book">%(cta1)s</a> <a class="btn btn-line" href="tel:%(phone_href)s">%(cta2)s</a></p>
        <p class="hero-note">%(hero_note)s</p>
      </div>
      <figure class="hero-ph">%(hero_img)s</figure>
    </div>
  </section>

  <!-- ============ Why trust us ============ -->
  <section class="trustbar" aria-labelledby="tr-h">
    <div class="wrap">
      <h2 id="tr-h" class="sr-only">%(trust_h)s</h2>
      <ul class="trust">%(trust_html)s</ul>
    </div>
  </section>

  <!-- ============ Emergency ============ -->
  <section class="emerg" aria-labelledby="em-h">
    <div class="wrap emerg-in">
      <div>
        <h2 id="em-h">%(em_h)s</h2>
        <p>%(em_p)s</p>
      </div>
      <p class="emerg-tel"><a class="btn btn-main" href="tel:%(phone_href)s">%(em_b1)s %(phone)s</a> <a class="btn btn-line" href="tel:%(night_href)s">%(em_b2)s %(night_phone)s</a></p>
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

  <!-- ============ Services and prices ============ -->
  <section class="block soft" id="services" aria-labelledby="sv-h">
    <div class="wrap">
      <header class="sec-head">
        <h2 id="sv-h">%(services_h)s</h2>
        <p>%(services_p)s</p>
      </header>
      <div class="sgroups">%(groups_html)s</div>
      <p class="p-note sv-note">%(sv_note)s</p>
    </div>
  </section>

  <!-- ============ Equipment ============ -->
  <section class="block" aria-labelledby="eq-h">
    <div class="wrap">
      <header class="sec-head">
        <h2 id="eq-h">%(eq_h)s</h2>
        <p>%(eq_p)s</p>
      </header>
      <ul class="equip">
        <li><figure>%(eq1)s</figure><p>%(eq1_t)s</p></li>
        <li><figure>%(eq2)s</figure><p>%(eq2_t)s</p></li>
        <li><figure>%(eq3)s</figure><p>%(eq3_t)s</p></li>
      </ul>
    </div>
  </section>

  <!-- ============ First visit and care ============ -->
  <section class="block soft" id="care" aria-labelledby="cr-h">
    <div class="wrap care">
      <div>
        <header class="sec-head"><h2 id="cr-h">%(care_h)s</h2><p>%(care_p)s</p></header>
        <ul class="care-list">%(care_html)s</ul>
      </div>
      <div class="bring">
        <h3>%(bring_h)s</h3>
        <ul class="ticks">%(bring_html)s</ul>
        <figure>%(bring_img)s</figure>
      </div>
    </div>
  </section>

  <!-- ============ Vaccines ============ -->
  <section class="block" id="vaccines" aria-labelledby="vc-h">
    <div class="wrap">
      <header class="sec-head">
        <h2 id="vc-h">%(vacc_h)s</h2>
        <p>%(vacc_p)s</p>
      </header>
      <div class="vgrid">%(vacc_html)s</div>
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
          <div class="field"><label for="f-pet">%(f_pet)s</label><input id="f-pet" name="pet" type="text" autocomplete="off" required></div>
          <div class="field"><label for="f-service">%(f_service)s</label><select id="f-service" name="service">%(svc_opts)s</select></div>
        </div>
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
    <span>© <span id="year">2026</span> Lapa Vet. %(foot_demo)s</span>
    <span class="foot-links"><a href="%(privacy_href)s">%(f_priv)s</a> <a href="%(admin_href)s">%(admin_l)s</a></span>
  </div>
</footer>

<aside class="dock" aria-label="%(dock_label)s">
  <div class="dock-label"><small>%(dock_label)s</small><b id="skinName">%(skin_name)s</b></div>
  <div class="swatches">%(swatches)s</div>
</aside>

<script type="application/json" id="lapaData">%(data)s</script>
<script src="%(root)sjs/config.js"></script>
<script src="%(root)sjs/api.js"></script>
<script src="%(root)sjs/main.js"></script>
</body>
</html>
''' % dict(
        lang=lang, title=esc(title), desc=esc(desc), root=root, script=script, brand=BRAND, brand_html='Lapa <span>Vet</span>', phone_href=PHONE_HREF, phone=PHONE, email=EMAIL, hours_ld=hours_ld,
        night_href=NIGHT_HREF, night_phone=NIGHT_PHONE,
        skip=t('Към съдържанието', 'Skip to content'), nav_label=t('Навигация', 'Navigation'), nav_html=nav_html, call_l=t('Обади се', 'Call'),
        other_href=other_href, other_lang='en' if bg else 'bg', other_label='EN' if bg else 'БГ', other_aria='Switch to English' if bg else 'Превключи на български', menu_btn=t('Меню', 'Menu'),
        topbar_l=t('Работно време и спешни случаи', 'Opening hours and emergencies'), ib1_k=t('Днес', 'Today'), address=ADDRESS['bg' if bg else 'en'], ib3_k=t('Денонощно:', '24 hours:'),
        eyebrow=t('Ветеринарна клиника · Пловдив', 'Veterinary clinic · Plovdiv'),
        h1=t('Ветеринарна клиника, на която можеш да се довериш', 'A veterinary clinic you can trust'),
        lead=t('Двама опитни лекари, собствена лаборатория, ехограф и операционна. Обясняваме всичко и казваме цената, преди да започнем.', 'Two experienced vets, our own lab, ultrasound and operating room. We explain everything and tell you the price before we begin.'),
        cta1=t('Запази час', 'Book an appointment'), cta2=t('Обади се', 'Call us'),
        hero_note=t('Приемаме кучета, котки и дребни домашни животни.', 'We see dogs, cats and small pets.'),
        hero_img=I('dachshund', t('Ветеринарен лекар прави преглед на куче такса', 'A veterinarian examining a dachshund'), '(min-width: 900px) 490px, calc(100vw - 40px)', eager=True),
        trust_h=t('Защо ни се доверяват', 'Why owners trust us'), trust_html=trust_html,
        em_h=t('Спешен случай?', 'An emergency?'), em_p=t('В работно време ни се обади и дойди веднага. Не сме денонощна клиника: през нощта и в неделя се обади на клиниката, която препоръчваме.', 'During opening hours call us and come right away. We are not a 24-hour clinic: at night and on Sundays call the clinic we recommend.'),
        em_b1=t('Клиника:', 'Clinic:'), em_b2=t('Денонощно:', '24 hours:'),
        team_h=t('Лекарите, които ще се грижат за животното ти', 'The vets who will look after your animal'), team_p=t('Малък екип. Знаеш кой ще прегледа животното ти и какъв е опитът му.', 'A small team. You know who will see your animal and what experience they have.'), vets_html=vets_html,
        team_note=t('Имена, дипломи и регистрационни номера са примерни.', 'Names, diplomas and registration numbers are examples.'),
        services_h=t('Услуги и цени', 'Services and prices'), services_p=t('Цените са в евро. „От“ означава, че точната цена зависи от животното и я казваме предварително.', 'Prices are in euros. “From” means the exact price depends on the animal and we tell you beforehand.'),
        groups_html=groups_html, sv_note=t('Плащане в брой или с карта след прегледа. Лекарствата се плащат отделно.', 'Payment by cash or card after the visit. Medicines are paid separately.'),
        eq_h=t('Какво имаме на място', 'What we have on site'), eq_p=t('Не е нужно да обикаляш за изследвания. Повечето неща правим тук, в деня на прегледа.', 'You do not need to go elsewhere for tests. We do most things here, on the day of the visit.'),
        eq1=I('surgery', t('Светла операционна с хирургична маса и лампа', 'A bright operating room with a surgical table and lamp'), '(min-width: 900px) 364px, calc(100vw - 40px)'), eq1_t=t('Операционна за кастрации, зъби и рани', 'An operating room for neutering, teeth and wounds'),
        eq2=I('lab', t('Лаборатория с микроскоп и апаратура', 'A laboratory with a microscope and equipment'), '(min-width: 900px) 364px, calc(100vw - 40px)'), eq2_t=t('Лаборатория: кръв, урина и проби в същия ден', 'A lab: blood, urine and samples the same day'),
        eq3=I('scan-room', t('Куче в кабинета с ехограф', 'A dog in the room with the ultrasound machine'), '(min-width: 900px) 364px, calc(100vw - 40px)'), eq3_t=t('Ехограф за корем, сърце и бременност', 'Ultrasound for abdomen, heart and pregnancy'),
        care_h=t('Първото посещение', 'Your first visit'), care_p=t('Знаеш какво ще се случи и защо. Нищо не правим без да обясним.', 'You know what will happen and why. We do nothing without explaining.'), care_html=care_html,
        bring_h=t('Какво да носиш', 'What to bring'), bring_html=bring_html,
        bring_img=I('kitten', t('Бяло коте на преглед', 'A white kitten at a check-up'), '(min-width: 900px) 400px, calc(100vw - 40px)'),
        vacc_h=t('Ваксини: кога?', 'Vaccines: when?'), vacc_p=t('Това е само ориентир. Лекарят определя графика според животното, ваксините от по-рано и къде живее.', 'This is only a guide. The vet sets the schedule for the animal, its earlier vaccines and where it lives.'), vacc_html=vacc_html,
        book_h=t('Запази час', 'Book an appointment'), book_p=t('Избери животно, повод, ден и час. Ще ти се обадим само ако трябва да променим нещо. При спешен случай ни се обади.', 'Choose the animal, the reason, a day and a time. We only call you if something has to change. In an emergency, please call.'),
        f_species=t('Кое животно?', 'Which animal?'), sp_radios=sp_radios, f_pet=t('Име на животното', 'Animal’s name'), f_service=t('Повод', 'Reason'), svc_opts=svc_opts, f_date=t('Дата', 'Date'), f_time=t('Час', 'Time'),
        checking=t('Избери повод и дата, за да видиш свободните часове.', 'Choose a reason and a date to see the free times.'),
        f_name=t('Твоето име', 'Your name'), f_phone=t('Телефон', 'Phone'), f_msg=t('Бележка (по желание)', 'Note (optional)'), f_msg_h=t('Например: възраст, порода, от кога е проблемът.', 'For example: age, breed, how long the problem has lasted.'),
        f_send=t('Заяви час', 'Request the appointment'), f_note=t('Не е нужно да плащаш предварително.', 'You do not have to pay in advance.'), f_priv=t('Поверителност', 'Privacy'), privacy_href='privacy.html',
        faq_h=t('Често задавани въпроси', 'Common questions'), faq_html=faq_html,
        visit_h=t('Контакти', 'Contact'), hours_html=hours_html, l_addr=t('Адрес', 'Address'), l_phone=t('Телефон', 'Phone'), l_email=t('Имейл', 'Email'),
        visit_note=t('В събота и неделя приемаме по-кратко. Извън работно време: денонощната клиника на %s.' % NIGHT_PHONE, 'On Saturday and Sunday we are open for fewer hours. Outside opening hours: the 24-hour clinic on %s.' % NIGHT_PHONE),
        map_t=t('Картата се зарежда от OpenStreetMap едва когато я поискаш.', 'The map loads from OpenStreetMap only when you ask for it.'), map_btn=t('Покажи картата', 'Show the map'),
        foot_demo=t('Всичко тук е пример.', 'Everything here is an example.'), admin_href='admin.html' if bg else '../admin.html?lang=en', admin_l=t('Демо админ панел', 'Demo back office'),
        dock_label=t('Цветова схема', 'Colour scheme'), skin_name=t('Тюркоаз', 'Teal'), swatches=swatches,
        data=json.dumps(data, ensure_ascii=False).replace('</', '<\\/'),
    )


def main():
    cfg = ('/* Generated by tools/build_pages.py. Edit the values at the top of that file, then run it again. */\n'
           'window.LAPA_CONFIG = {\n  mode: "demo",            /* "demo" = requests are kept in this browser only; "live" = real API at apiBase (docs/API.md) */\n'
           '  apiBase: "/api",\n  hours: { weekday: ["%s", "%s"], weekend: ["%s", "%s"] },\n  capacity: %d,             /* vets seeing animals at the same time */\n'
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
