"""Builds index.html (Bulgarian), en/index.html (English), js/config.js and css/style.css for Dent Plus (a dental clinic).
Edit the values in this file (services, prices, doctors, hours, texts), then run:  python tools/build_pages.py && python tools/build_privacy.py
Everything about the clinic is an example: replace it for a real clinic."""
import json, os
from html import escape as esc
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BRAND = 'Dent Plus'

# ---------------- settings you will change for a real clinic ----------------
HOURS = {'weekday': ['08:00', '19:00'], 'weekend': ['09:00', '13:00']}
CAPACITY = 3          # chairs working at the same time
SLOT_MINUTES = 30
LEAD_MINUTES = 120
PHONE, PHONE_HREF, EMAIL = '+359 88 000 0000', '+359880000000', 'clinic@example.com'
ADDRESS = {'bg': 'ул. Примерна 52, Пловдив', 'en': '52 Primer St., Plovdiv'}

# services: id, minutes, price in euro (or None = free), "from" price?, (bg name, en name), (bg text, en text)
SERVICES = [
 ('check', 30, 35, False, ('Профилактичен преглед', 'Check-up'), ('Преглед, съвет и план за лечение', 'An examination, advice and a treatment plan')),
 ('clean', 45, 55, False, ('Почистване на зъбен камък и полиране', 'Scale and polish'), ('Ултразвуково почистване и полиране', 'Ultrasonic cleaning and polishing')),
 ('filling', 45, 60, True, ('Лечение на кариес (пломба)', 'Filling'), ('С местна упойка, ако е нужно', 'With a local anaesthetic if needed')),
 ('root', 60, 140, True, ('Лечение на коренов канал', 'Root canal treatment'), ('Когато нервът на зъба е възпален', 'When the nerve of a tooth is inflamed')),
 ('white', 60, 220, True, ('Избелване на зъби', 'Teeth whitening'), ('Едно посещение, видим резултат', 'One visit, a visible result')),
 ('implant', 30, None, False, ('Консултация за импланти', 'Implant consultation'), ('Безплатна, с рентгенов снимка', 'Free, with an X-ray picture')),
 ('child', 30, 25, False, ('Преглед на дете', 'Child check-up'), ('За деца до 12 години', 'For children up to 12')),
 ('pain', 30, 30, True, ('Спешно: болка', 'Urgent: pain'), ('В същия ден, без записване', 'The same day, no booking needed')),
]
DOCTORS = [('petrova', 'portrait-woman', ('д-р Елена Петрова', 'Dr. Elena Petrova'), ('Общ стоматолог, 15 години опит', 'General dentist, 15 years of experience'), ('Лечение на кариес, профилактика и деца. Обяснява всичко, преди да започне.', 'Fillings, prevention and children. She explains everything before she starts.')),
           ('ivanov', 'portrait-man', ('д-р Николай Иванов', 'Dr. Nikolay Ivanov'), ('Орален хирург, 12 години опит', 'Oral surgeon, 12 years of experience'), ('Импланти, премахване на зъби и коренови канали.', 'Implants, tooth removal and root canals.'))]

SKINS = [('teal', 'Тюркоаз', 'Teal', '#F4F9FA', '#0E7C86'), ('blue', 'Синьо', 'Blue', '#F4F7FB', '#1F5FA8'), ('green', 'Зелено', 'Green', '#F3F8F5', '#2D7A4F'),
         ('coral', 'Корал', 'Coral', '#FCF6F3', '#B5472A'), ('night', 'Нощ', 'Night', '#101B20', '#5CC8D3')]


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

    def money(v, frm=False):
        if v is None:
            return t('безплатно', 'free')
        s = ('%d' % v)
        return ((t('от ', 'from ') if frm else '') + s + ' €') if bg else ((t('от ', 'from ') if frm else '') + '€' + s)

    rows = ''.join('<tr><th scope="row">%s<small>%s · %s %s</small></th><td>%s</td></tr>' % (esc(s[4][i]), esc(s[5][i]), s[1], t('мин', 'min'), money(s[2], s[3])) for s in SERVICES)
    svc_opts = ''.join('<option value="%s" data-min="%d">%s</option>' % (s[0], s[1], esc(s[4][i])) for s in SERVICES)
    doc_cards = ''.join('<li><figure>%s</figure><div><h3>%s</h3><p class="role">%s</p><p>%s</p></div></li>' % (I(d[1], d[2][i], '(min-width: 900px) 220px, 40vw'), d[2][i], d[3][i], d[4][i]) for d in DOCTORS)
    doc_opts = '<option value="any">%s</option>' % t('Няма значение', 'No preference') + ''.join('<option value="%s">%s</option>' % (d[0], d[2][i]) for d in DOCTORS)
    steps = [(t('Разговор', 'A talk'), t('Питаме какво те тревожи и какви лекарства взимаш.', 'We ask what worries you and which medicines you take.')), (t('Преглед', 'Examination'), t('Оглеждаме зъбите и, ако трябва, правим снимка.', 'We look at your teeth and, if needed, take an X-ray picture.')),
             (t('План и цена', 'Plan and price'), t('Получаваш плана и цената на хартия, преди да решиш.', 'You get the plan and the price on paper before you decide.')), (t('Лечение', 'Treatment'), t('Започваме веднага, ако искаш, или си уговаряме друг час.', 'We start right away if you like, or book another time.'))]
    steps_html = ''.join('<li><b>%d</b><h3>%s</h3><p>%s</p></li>' % (n + 1, a, b) for n, (a, b) in enumerate(steps))
    faq = [(t('Боли ли?', 'Does it hurt?'), t('Използваме местна упойка и работим бавно. Ако искаш почивка, вдигни ръка и спираме.', 'We use a local anaesthetic and work slowly. If you want a break, raise your hand and we stop.')),
           (t('На колко време да идвам на преглед?', 'How often should I come for a check-up?'), t('Два пъти в годината. При проблеми с венците или много кариеси: на всеки четири месеца.', 'Twice a year. With gum problems or many cavities: every four months.')),
           (t('Приемате ли деца?', 'Do you treat children?'), t('Да, от три години. Първото посещение е само за запознанство и няма да ги лекуваме насила.', 'Yes, from three years old. The first visit is only to get to know us and we never treat a child by force.')),
           (t('Как се плаща?', 'How do I pay?'), t('В брой или с карта след лечението. За по-голямо лечение предлагаме разсрочено плащане. Попитай за застраховки.', 'Cash or card after the treatment. For larger treatment we offer payment in instalments. Ask about insurance.'))]
    faq_html = ''.join('<details class="qa"><summary>%s</summary><p>%s</p></details>' % f for f in faq)
    hours_rows = [(t('Понеделник – петък', 'Monday – Friday'), HOURS['weekday'], 'wd'), (t('Събота и неделя', 'Saturday and Sunday'), HOURS['weekend'], 'we')]
    hours_html = ''.join('<div data-hrs="%s"><dt>%s</dt><dd>%s – %s</dd></div>' % (k, n, h[0], h[1]) for n, h, k in hours_rows)
    hours_ld = '"Mo-Fr %s-%s","Sa-Su %s-%s"' % (HOURS['weekday'][0], HOURS['weekday'][1], HOURS['weekend'][0], HOURS['weekend'][1])
    swatches = ''.join('<button class="sw" type="button" data-skin="%s" style="--s1:%s;--s2:%s" aria-pressed="false" aria-label="%s"></button>' % (k, s1, s2, b if bg else e) for k, b, e, s1, s2 in SKINS)
    nav = [('#services', t('Услуги и цени', 'Services and prices')), ('#doctors', t('Лекари', 'Doctors')), ('#first', t('Първо посещение', 'First visit')), ('#book', t('Запази час', 'Book')), ('#visit', t('Контакти', 'Contact'))]
    nav_html = ''.join('<a href="%s">%s</a>' % n for n in nav)
    data = {'doctors': {d[0]: d[2][i] for d in DOCTORS}, 'services': {s[0]: s[4][i] for s in SERVICES}}

    title = t('Dent Plus – стоматологична клиника в Пловдив. Запази час онлайн', 'Dent Plus – dental clinic in Plovdiv. Book an appointment online')
    desc = t('Dent Plus е стоматологична клиника в Пловдив: прегледи, лечение, импланти и избелване. Виж цените, запознай се с лекарите и запази час.',
             'Dent Plus is a dental clinic in Plovdiv: check-ups, fillings, implants and whitening. See the prices, meet the doctors and book an appointment.')

    return '''<!doctype html>
<html lang="%(lang)s" data-skin="teal">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="theme-color" content="#F4F9FA">
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
     and an og:image (images/stock/office-orange.jpg is a placeholder) -->
<link rel="preload" href="%(root)sfonts/source-sans-3-400-600-%(script)s.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="%(root)sfonts/fonts.css">
<link rel="stylesheet" href="%(root)scss/style.css">
<script>
  /* Apply the saved colour scheme before the page paints, so it does not flash. */
  try { var s = new URLSearchParams(location.search).get("skin") || localStorage.getItem("dentSkin"); if (s) document.documentElement.dataset.skin = s; } catch (e) {}
</script>
<script type="application/ld+json">
{"@context":"https://schema.org","@type":"Dentist","name":"%(brand)s","inLanguage":"%(lang)s","telephone":"%(phone_href)s","email":"%(email)s",
 "address":{"@type":"PostalAddress","streetAddress":"Primer St. 52","addressLocality":"Plovdiv","addressCountry":"BG"},"openingHours":[%(hours_ld)s]}
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
    <div class="wrap hero-in">
      <div class="hero-copy">
        <h1 id="h1">%(h1)s</h1>
        <p class="lead">%(lead)s</p>
        <ul class="hero-list"><li>%(hl1)s</li><li>%(hl2)s</li><li>%(hl3)s</li></ul>
        <p class="hero-links"><a class="btn btn-main" href="#book">%(cta1)s</a> <a class="btn btn-line" href="tel:%(phone_href)s">%(cta2)s</a></p>
      </div>
      <figure class="hero-ph">%(hero_img)s</figure>
    </div>
  </section>
  <div class="info-bar">
    <ul class="wrap info-row">
      <li><b>%(ib1_k)s</b> <span id="todayHours">08:00 – 19:00</span></li>
      <li><b>%(ib2_k)s</b> <span>%(address)s</span></li>
      <li><b>%(ib3_k)s</b> <span>%(ib3_v)s</span></li>
    </ul>
  </div>

  <!-- ============ Services and prices ============ -->
  <section class="block" id="services" aria-labelledby="sv-h">
    <div class="wrap services">
      <header class="sec-head">
        <h2 id="sv-h">%(services_h)s</h2>
        <p>%(services_p)s</p>
        <figure class="sv-ph">%(sv_img)s</figure>
      </header>
      <div>
        <table class="plist"><caption class="sr-only">%(services_h)s</caption><tbody>%(rows)s</tbody></table>
        <p class="p-note sv-note">%(sv_note)s</p>
      </div>
    </div>
  </section>

  <!-- ============ Doctors ============ -->
  <section class="block soft" id="doctors" aria-labelledby="dc-h">
    <div class="wrap">
      <header class="sec-head">
        <h2 id="dc-h">%(doctors_h)s</h2>
        <p>%(doctors_p)s</p>
      </header>
      <ul class="docs">%(doc_cards)s</ul>
    </div>
  </section>

  <!-- ============ First visit ============ -->
  <section class="block" id="first" aria-labelledby="fv-h">
    <div class="wrap first">
      <div>
        <header class="sec-head">
          <h2 id="fv-h">%(first_h)s</h2>
          <p>%(first_p)s</p>
        </header>
        <ol class="steps4">%(steps_html)s</ol>
      </div>
      <figure class="first-ph">%(first_img)s</figure>
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
        <fieldset class="group"><legend>%(f_patient)s</legend>
          <div class="opts">
            <label class="opt"><input type="radio" name="patient" value="new" checked><span>%(o_new)s</span></label>
            <label class="opt"><input type="radio" name="patient" value="returning"><span>%(o_ret)s</span></label>
          </div>
        </fieldset>
        <div class="row2">
          <div class="field"><label for="f-service">%(f_service)s</label><select id="f-service" name="service">%(svc_opts)s</select></div>
          <div class="field"><label for="f-doctor">%(f_doctor)s</label><select id="f-doctor" name="doctor">%(doc_opts)s</select></div>
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

  <!-- ============ Clinic and FAQ ============ -->
  <section class="block" aria-labelledby="fq-h">
    <div class="wrap">
      <header class="sec-head"><h2 id="fq-h">%(faq_h)s</h2></header>
      <div class="qas">%(faq_html)s</div>
      <div class="clinic">
        <figure>%(cl1)s</figure><figure>%(cl2)s</figure><figure>%(cl3)s</figure>
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
    <span>© <span id="year">2026</span> Dent Plus. %(foot_demo)s</span>
    <span class="foot-links"><a href="%(privacy_href)s">%(f_priv)s</a> <a href="%(admin_href)s">%(admin_l)s</a></span>
  </div>
</footer>

<aside class="dock" aria-label="%(dock_label)s">
  <div class="dock-label"><small>%(dock_label)s</small><b id="skinName">%(skin_name)s</b></div>
  <div class="swatches">%(swatches)s</div>
</aside>

<script type="application/json" id="dentData">%(data)s</script>
<script src="%(root)sjs/config.js"></script>
<script src="%(root)sjs/api.js"></script>
<script src="%(root)sjs/main.js"></script>
</body>
</html>
''' % dict(
        lang=lang, title=esc(title), desc=esc(desc), root=root, script=script, brand=BRAND, brand_html='Dent <span>Plus</span>', phone_href=PHONE_HREF, phone=PHONE, email=EMAIL, hours_ld=hours_ld,
        skip=t('Към съдържанието', 'Skip to content'), nav_label=t('Навигация', 'Navigation'), nav_html=nav_html, call_l=t('Обади се', 'Call'),
        other_href=other_href, other_lang='en' if bg else 'bg', other_label='EN' if bg else 'БГ', other_aria='Switch to English' if bg else 'Превключи на български', menu_btn=t('Меню', 'Menu'),
        h1=t('Спокойна стоматология в Пловдив', 'Calm dentistry in Plovdiv'),
        lead=t('Преглед, лечение и профилактика за цялото семейство. Казваме ти цената предварително и обясняваме всяка стъпка.', 'Check-ups, treatment and prevention for the whole family. We tell you the price beforehand and explain every step.'),
        hl1=t('Спешна болка: в същия ден', 'Urgent pain: the same day'), hl2=t('План и цена на хартия, преди да започнем', 'A plan and price on paper before we start'), hl3=t('Деца от три години', 'Children from three years old'),
        cta1=t('Запази час', 'Book an appointment'), cta2=t('Обади се', 'Call us'),
        hero_img=I('office-orange', t('Светъл кабинет с оранжев стоматологичен стол', 'A bright surgery with an orange dental chair'), '(min-width: 900px) 520px, calc(100vw - 40px)', eager=True),
        ib1_k=t('Днес', 'Today'), ib2_k=t('Адрес', 'Address'), address=ADDRESS['bg' if bg else 'en'], ib3_k=t('Болка?', 'In pain?'), ib3_v=t('Обади се и те приемаме днес.', 'Call and we see you today.'),
        services_h=t('Услуги и цени', 'Services and prices'), services_p=t('Цените са в евро. „От“ означава, че точната цена зависи от зъба и казваме предварително. Първият преглед на нов пациент включва и снимка, ако е нужна.', 'Prices are in euros. “From” means the exact price depends on the tooth and we tell you beforehand. A new patient’s first check-up includes an X-ray picture if one is needed.'),
        sv_img=I('exam', t('Лекар, който прави преглед на зъби с огледало', 'A dentist examining teeth with a mirror'), '(min-width: 900px) 420px, calc(100vw - 40px)'), rows=rows,
        sv_note=t('Плащане в брой или с карта. За по-голямо лечение има разсрочено плащане.', 'Payment by cash or card. For larger treatment there is payment in instalments.'),
        doctors_h=t('Нашите лекари', 'Our doctors'), doctors_p=t('Малък екип, при който винаги знаеш кой ще те лекува.', 'A small team where you always know who will treat you.'), doc_cards=doc_cards,
        first_h=t('Първото посещение', 'Your first visit'), first_p=t('Отнема около 40 минути. Не е нужно да носиш нищо, освен лична карта и стари снимки, ако имаш.', 'It takes about 40 minutes. You do not need to bring anything except an ID and old X-rays if you have them.'), steps_html=steps_html,
        first_img=I('consult', t('Лекар разговаря с пациентка в кабинета', 'A dentist talking with a patient in the surgery'), '(min-width: 900px) 420px, calc(100vw - 40px)'),
        book_h=t('Запази час', 'Book an appointment'), book_p=t('Избери услуга, ден и час. Ще ти се обадим само ако трябва да променим нещо. При силна болка ни се обади по телефона.', 'Choose a service, a day and a time. We only call you if something has to change. If you are in severe pain, please call us.'),
        f_patient=t('Бил ли си при нас?', 'Have you been to us before?'), o_new=t('Нов пациент', 'New patient'), o_ret=t('Вече съм пациент', 'Returning patient'),
        f_service=t('Услуга', 'Service'), svc_opts=svc_opts, f_doctor=t('Лекар', 'Doctor'), doc_opts=doc_opts, f_date=t('Дата', 'Date'), f_time=t('Час', 'Time'), checking=t('Избери услуга и дата, за да видиш свободните часове.', 'Choose a service and a date to see the free times.'),
        f_name=t('Име', 'Name'), f_phone=t('Телефон', 'Phone'), f_msg=t('Бележка (по желание)', 'Note (optional)'), f_msg_h=t('Не пиши подробна медицинска информация тук. Кажи я на лекаря при посещението.', 'Please do not write detailed medical information here. Tell the dentist at the visit.'),
        f_send=t('Заяви час', 'Request the appointment'), f_note=t('Не е нужно да плащаш предварително.', 'You do not have to pay in advance.'), f_priv=t('Поверителност', 'Privacy'), privacy_href='privacy.html',
        faq_h=t('Често задавани въпроси', 'Common questions'), faq_html=faq_html,
        cl1=I('office-modern', t('Модерен кабинет с оборудване', 'A modern surgery with equipment'), '(min-width: 900px) 352px, calc(100vw - 40px)'), cl2=I('chair-blue', t('Кабинет със син стол', 'A surgery with a blue chair'), '(min-width: 900px) 352px, calc(100vw - 40px)'), cl3=I('waiting', t('Чакалня със столове и растение', 'A waiting room with chairs and a plant'), '(min-width: 900px) 352px, calc(100vw - 40px)'),
        visit_h=t('Контакти', 'Contact'), hours_html=hours_html, l_addr=t('Адрес', 'Address'), l_phone=t('Телефон', 'Phone'), l_email=t('Имейл', 'Email'),
        visit_note=t('В събота и неделя приемаме само спешни случаи, след обаждане.', 'On Saturday and Sunday we see urgent cases only, after a phone call.'),
        map_t=t('Картата се зарежда от OpenStreetMap едва когато я поискаш.', 'The map loads from OpenStreetMap only when you ask for it.'), map_btn=t('Покажи картата', 'Show the map'),
        foot_demo=t('Всичко тук е пример.', 'Everything here is an example.'), admin_href='admin.html' if bg else '../admin.html?lang=en', admin_l=t('Демо админ панел', 'Demo back office'),
        dock_label=t('Цветова схема', 'Colour scheme'), skin_name=t('Тюркоаз', 'Teal'), swatches=swatches,
        data=json.dumps(data, ensure_ascii=False).replace('</', '<\\/'),
    )


def main():
    cfg = ('/* Generated by tools/build_pages.py. Edit the values at the top of that file, then run it again. */\n'
           'window.DENT_CONFIG = {\n  mode: "demo",            /* "demo" = requests are kept in this browser only; "live" = real API at apiBase (docs/API.md) */\n'
           '  apiBase: "/api",\n  hours: { weekday: ["%s", "%s"], weekend: ["%s", "%s"] },\n  capacity: %d,             /* chairs working at the same time */\n'
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
