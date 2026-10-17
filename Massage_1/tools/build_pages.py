"""Builds index.html (Bulgarian), en/index.html (English), js/config.js and css/style.css for Tishina (a massage studio).
Edit the values in this file (massages, lengths and prices, therapists, hours, texts), then run:  python tools/build_pages.py && python tools/build_privacy.py
Everything about the studio is an example: replace it for a real studio."""
import json, os
from html import escape as esc
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BRAND = 'Tishina'

# ---------------- settings you will change for a real studio ----------------
HOURS = {'weekday': ['10:00', '21:00'], 'weekend': ['10:00', '18:00']}
CAPACITY = 2          # treatment rooms
SLOT_MINUTES = 30
LEAD_MINUTES = 120
PHONE, PHONE_HREF, EMAIL = '+359 88 000 0000', '+359880000000', 'studio@example.com'
ADDRESS = {'bg': 'ул. Примерна 12, Пловдив', 'en': '12 Primer St., Plovdiv'}

# massages: id, photo, {minutes: price in euro}, default minutes, (bg name, en name), (bg text, en text)
MASSAGES = [
 ('relax', 'oil', {30: 28, 60: 48, 90: 68}, 60, ('Релаксиращ масаж', 'Relaxing massage'), ('Бавни движения с топло масло, за цялото тяло. За умора и напрежение.', 'Slow strokes with warm oil, for the whole body. For tiredness and tension.')),
 ('deep', 'deep', {60: 55, 90: 78}, 60, ('Дълбок масаж', 'Deep tissue massage'), ('По-силен натиск за схванати врат, рамене и гръб. Казваш ни кога е достатъчно.', 'Firmer pressure for a stiff neck, shoulders and back. You tell us when it is enough.')),
 ('back', 'back-warm', {30: 30}, 30, ('Гръб и врат', 'Back and neck'), ('Кратък масаж за хора, които седят цял ден пред компютър.', 'A short massage for people who sit at a computer all day.')),
 ('stones', 'stones', {60: 60, 90: 85}, 60, ('Масаж с топли камъни', 'Hot stone massage'), ('Гладки топли камъни по гърба и дълбока топлина в мускулите.', 'Smooth warm stones on the back and deep warmth in the muscles.')),
 ('herbal', 'herbal', {60: 58, 90: 82}, 60, ('Билкови торбички', 'Herbal pouches'), ('Топли торбички с билки и масло. Бавен и ароматен.', 'Warm pouches with herbs and oil. Slow and fragrant.')),
]
THERAPISTS = [('mila', ('Мила Тодорова', 'Mila Todorova'), ('Масажист, 10 години опит', 'Massage therapist, 10 years of experience'), ('Релаксиращ масаж, билкови торбички и масаж с камъни.', 'Relaxing massage, herbal pouches and hot stones.')),
              ('georgi', ('Георги Янков', 'Georgi Yankov'), ('Масажист, 8 години опит', 'Massage therapist, 8 years of experience'), ('Дълбок масаж, гръб и врат. Работи с хора, които спортуват.', 'Deep tissue, back and neck. Works with people who play sport.'))]

SKINS = [('clay', 'Глина', 'Clay', '#F7F1E8', '#9C4A2F'), ('sage', 'Градина', 'Sage', '#F2F5EF', '#4C6B4E'), ('sand', 'Пясък', 'Sand', '#F8F4EC', '#8A6A2E'),
         ('ink', 'Мастило', 'Ink', '#F1F2F6', '#3B4570'), ('night', 'Нощ', 'Night', '#17120F', '#D8A27E')]


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

    alts = {'oil': t('Ръце наливат масло върху гърба на жена на масажна маса', 'Hands pouring oil on the back of a woman on a massage table'),
            'deep': t('Ръце масажират гръб с дълбок натиск', 'Hands giving a back massage with firm pressure'),
            'back-warm': t('Две ръце масажират гръб на топла светлина', 'Two hands massaging a back in warm light'),
            'stones': t('Черни гладки камъни върху гърба на жена, с бели цветя', 'Smooth black stones on a woman’s back with white flowers'),
            'herbal': t('Билкови торбички върху гърдите и раменете на мъж', 'Herbal pouches on a man’s chest and shoulders')}
    cards = ''
    for m in MASSAGES:
        prices = ''.join('<li><span>%d %s</span> <b>%s</b></li>' % (k, t('мин', 'min'), money(v)) for k, v in m[2].items())
        cards += ('<li class="mcard"><figure>%s</figure><div><h3>%s</h3><p>%s</p><ul class="mprices">%s</ul>'
                  '<a class="mlink" href="#book" data-massage="%s">%s</a></div></li>') % (
            I(m[1], alts[m[1]], '(min-width: 1000px) 357px, (min-width: 640px) 45vw, calc(100vw - 40px)'), m[4][i], m[5][i], prices, m[0], t('Резервирай', 'Book this'))
    cards += ('<li class="mcard gift"><div><h3>%s</h3><p>%s</p><a class="mlink" href="#book" data-gift="1">%s</a></div></li>'
              % (t('Подаръчен ваучер', 'Gift voucher'), t('Подари масаж. Избираш масажа и колко време, а ние подготвяме ваучер с името на получателя. Валиден е 6 месеца.', 'Give a massage. You choose the massage and its length and we prepare a voucher with the recipient’s name. It is valid for 6 months.'), t('Поръчай ваучер', 'Order a voucher')))
    svc_opts = ''.join('<option value="%s">%s</option>' % (m[0], esc(m[4][i])) for m in MASSAGES)
    ther_opts = '<option value="any">%s</option>' % t('Няма значение', 'No preference') + ''.join('<option value="%s">%s</option>' % (x[0], x[1][i]) for x in THERAPISTS)
    ther_cards = ''.join('<li><span class="ini" aria-hidden="true">%s</span><div><h3>%s</h3><p class="role">%s</p><p>%s</p></div></li>' % (x[1][i][0], x[1][i], x[2][i], x[3][i]) for x in THERAPISTS)
    before = [t('Дойди 10 минути по-рано. Има чай и тих ъгъл за изчакване.', 'Come 10 minutes early. There is tea and a quiet corner to wait in.'), t('Не е нужно да носиш нищо. Даваме халат, чехли и кърпа.', 'You do not need to bring anything. We give you a robe, slippers and a towel.'),
              t('Кажи ни за болки, алергии към масла или бременност преди масажа.', 'Tell us about pain, allergies to oils or pregnancy before the massage.'), t('Свали телефона на тих режим. Стаята е тиха и топла.', 'Put your phone on silent. The room is quiet and warm.')]
    before_html = ''.join('<li>%s</li>' % b for b in before)
    faq = [(t('Ще бъда ли гол/гола?', 'Will I be undressed?'), t('Събличаш се до комфорта си. Покрит си с кърпа през цялото време и откриваме само частта, върху която работим.', 'You undress to your comfort. You are covered with a towel the whole time and only the part we work on is uncovered.')),
           (t('Боли ли дълбокият масаж?', 'Does a deep tissue massage hurt?'), t('Усещаш натиск, понякога неприятен, но не болка. Кажи, и намаляваме. Следващите дни е нормално да усещаш мускулите си.', 'You feel pressure, sometimes uncomfortable, but not pain. Say so and we ease off. It is normal to feel your muscles for a few days.')),
           (t('Кога не бива да правя масаж?', 'When should I not have a massage?'), t('При температура, остра инфекция, скорошна операция, тромбоза или рак. При съмнение попитай лекаря си първо.', 'With a fever, an acute infection, recent surgery, thrombosis or cancer. If in doubt ask your doctor first.')),
           (t('Как се плаща?', 'How do I pay?'), t('В студиото след масажа, в брой или с карта. Не е нужно да плащаш предварително.', 'At the studio after the massage, by cash or card. You do not have to pay in advance.'))]
    faq_html = ''.join('<details class="qa"><summary>%s</summary><p>%s</p></details>' % f for f in faq)
    hours_rows = [(t('Понеделник – петък', 'Monday – Friday'), HOURS['weekday'], 'wd'), (t('Събота и неделя', 'Saturday and Sunday'), HOURS['weekend'], 'we')]
    hours_html = ''.join('<div data-hrs="%s"><dt>%s</dt><dd>%s – %s</dd></div>' % (k, n, h[0], h[1]) for n, h, k in hours_rows)
    hours_ld = '"Mo-Fr %s-%s","Sa-Su %s-%s"' % (HOURS['weekday'][0], HOURS['weekday'][1], HOURS['weekend'][0], HOURS['weekend'][1])
    swatches = ''.join('<button class="sw" type="button" data-skin="%s" style="--s1:%s;--s2:%s" aria-pressed="false" aria-label="%s"></button>' % (k, s1, s2, b if bg else e) for k, b, e, s1, s2 in SKINS)
    nav = [('#massages', t('Масажи и цени', 'Massages and prices')), ('#before', t('Преди да дойдеш', 'Before you come')), ('#team', t('Терапевти', 'Therapists')), ('#book', t('Резервирай', 'Book')), ('#visit', t('Контакти', 'Contact'))]
    nav_html = ''.join('<a href="%s">%s</a>' % n for n in nav)
    data = {'massages': {m[0]: {'name': m[4][i], 'prices': {str(k): v for k, v in m[2].items()}, 'def': str(m[3])} for m in MASSAGES}, 'therapists': {x[0]: x[1][i] for x in THERAPISTS}}

    title = t('Tishina – масажно студио в Пловдив. Резервирай онлайн', 'Tishina – massage studio in Plovdiv. Book online')
    desc = t('Tishina е тихо масажно студио в Пловдив: релаксиращ и дълбок масаж, топли камъни и подаръчни ваучери. Виж цените и резервирай час.',
             'Tishina is a quiet massage studio in Plovdiv: relaxing and deep tissue massage, hot stones and gift vouchers. See the prices and book a time.')

    return '''<!doctype html>
<html lang="%(lang)s" data-skin="clay">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="theme-color" content="#F7F1E8">
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
     and an og:image (images/stock/face-warm.jpg is a placeholder) -->
<link rel="preload" href="%(root)sfonts/cormorant-garamond-600-%(script)s.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="%(root)sfonts/fonts.css">
<link rel="stylesheet" href="%(root)scss/style.css">
<script>
  /* Apply the saved colour scheme before the page paints, so it does not flash. */
  try { var s = new URLSearchParams(location.search).get("skin") || localStorage.getItem("tishinaSkin"); if (s) document.documentElement.dataset.skin = s; } catch (e) {}
</script>
<script type="application/ld+json">
{"@context":"https://schema.org","@type":"DaySpa","name":"%(brand)s","inLanguage":"%(lang)s","telephone":"%(phone_href)s","email":"%(email)s",
 "address":{"@type":"PostalAddress","streetAddress":"Primer St. 12","addressLocality":"Plovdiv","addressCountry":"BG"},"openingHours":[%(hours_ld)s]}
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
    <figure class="hero-bg">%(hero_img)s</figure>
    <div class="wrap hero-in">
      <h1 id="h1">%(h1)s</h1>
      <p class="lead">%(lead)s</p>
      <p class="hero-links"><a class="btn btn-light" href="#book">%(cta1)s</a> <a class="btn btn-ghost" href="#massages">%(cta2)s</a></p>
    </div>
  </section>
  <div class="info-bar">
    <ul class="wrap info-row">
      <li><b>%(ib1_k)s</b> <span id="todayHours">10:00 – 21:00</span></li>
      <li><b>%(ib2_k)s</b> <span>%(address)s</span></li>
      <li><b>%(ib3_k)s</b> <span>%(ib3_v)s</span></li>
    </ul>
  </div>

  <!-- ============ Massages and prices ============ -->
  <section class="block" id="massages" aria-labelledby="ms-h">
    <div class="wrap">
      <header class="sec-head center"><h2 id="ms-h">%(ms_h)s</h2><p>%(ms_p)s</p></header>
      <ul class="mgrid">%(cards)s</ul>
    </div>
  </section>

  <!-- ============ Before you come ============ -->
  <section class="block soft" id="before" aria-labelledby="bf-h">
    <div class="wrap before">
      <div>
        <header class="sec-head"><h2 id="bf-h">%(bf_h)s</h2></header>
        <ul class="ticks">%(before_html)s</ul>
      </div>
      <figure class="bf-ph">%(bf_img)s</figure>
    </div>
  </section>

  <!-- ============ Therapists ============ -->
  <section class="block" id="team" aria-labelledby="tm-h">
    <div class="wrap">
      <header class="sec-head center"><h2 id="tm-h">%(team_h)s</h2><p>%(team_p)s</p></header>
      <ul class="vets">%(ther_cards)s</ul>
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
        <div class="row2">
          <div class="field"><label for="f-service">%(f_service)s</label><select id="f-service" name="service">%(svc_opts)s</select></div>
          <div class="field"><label for="f-length">%(f_length)s</label><select id="f-length" name="length"></select></div>
        </div>
        <p class="estimate" id="estimate" role="status"></p>
        <div class="field"><label for="f-ther">%(f_ther)s</label><select id="f-ther" name="therapist">%(ther_opts)s</select></div>
        <div class="row2">
          <div class="field"><label for="f-date">%(f_date)s</label><input id="f-date" name="date" type="date" required></div>
          <div class="field"><label for="f-time">%(f_time)s</label><select id="f-time" name="time" required></select></div>
        </div>
        <p class="hint" id="timeHint" role="status">%(checking)s</p>
        <div class="row2">
          <div class="field"><label for="f-name">%(f_name)s</label><input id="f-name" name="name" type="text" autocomplete="name" required></div>
          <div class="field"><label for="f-phone">%(f_phone)s</label><input id="f-phone" name="phone" type="tel" autocomplete="tel" required></div>
        </div>
        <label class="check"><input type="checkbox" name="gift" id="f-gift"><span>%(f_gift)s</span></label>
        <div class="field"><label for="f-msg">%(f_msg)s</label><textarea id="f-msg" name="msg" rows="3"></textarea><p class="hint">%(f_msg_h)s</p></div>
        <p class="demo-note" id="demoNote" hidden></p>
        <p class="form-error" id="aError" role="alert" hidden></p>
        <button class="btn btn-main" type="submit" id="aSend">%(f_send)s</button>
        <small class="fine">%(f_note)s <a href="%(privacy_href)s">%(f_priv)s</a></small>
      </form>
      <div class="done" id="aDone" hidden tabindex="-1"></div>
    </div>
  </section>

  <!-- ============ Photos and FAQ ============ -->
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
    <span>© <span id="year">2026</span> Tishina. %(foot_demo)s</span>
    <span class="foot-links"><a href="%(privacy_href)s">%(f_priv)s</a> <a href="%(admin_href)s">%(admin_l)s</a></span>
  </div>
</footer>

<aside class="dock" aria-label="%(dock_label)s">
  <div class="dock-label"><small>%(dock_label)s</small><b id="skinName">%(skin_name)s</b></div>
  <div class="swatches">%(swatches)s</div>
</aside>

<script type="application/json" id="tishinaData">%(data)s</script>
<script src="%(root)sjs/config.js"></script>
<script src="%(root)sjs/api.js"></script>
<script src="%(root)sjs/main.js"></script>
</body>
</html>
''' % dict(
        lang=lang, title=esc(title), desc=esc(desc), root=root, script=script, brand=BRAND, brand_html='Tishina', phone_href=PHONE_HREF, phone=PHONE, email=EMAIL, hours_ld=hours_ld,
        skip=t('Към съдържанието', 'Skip to content'), nav_label=t('Навигация', 'Navigation'), nav_html=nav_html, call_l=t('Обади се', 'Call'),
        other_href=other_href, other_lang='en' if bg else 'bg', other_label='EN' if bg else 'БГ', other_aria='Switch to English' if bg else 'Превключи на български', menu_btn=t('Меню', 'Menu'),
        h1=t('Час тишина за тялото ти', 'An hour of quiet for your body'),
        lead=t('Масажно студио в Пловдив. Топла стая, бавни ръце и цена, която знаеш предварително.', 'A massage studio in Plovdiv. A warm room, unhurried hands and a price you know beforehand.'),
        cta1=t('Резервирай час', 'Book a time'), cta2=t('Масажи и цени', 'Massages and prices'),
        hero_img=I('face-warm', t('Ръце масажират лице на топла приглушена светлина', 'Hands massaging a face in warm, dim light'), '100vw', eager=True),
        ib1_k=t('Днес', 'Today'), ib2_k=t('Адрес', 'Address'), address=ADDRESS['bg' if bg else 'en'], ib3_k=t('Плащане', 'Payment'), ib3_v=t('След масажа, в студиото.', 'After the massage, at the studio.'),
        ms_h=t('Масажи и цени', 'Massages and prices'), ms_p=t('Цените са в евро и важат за целия сеанс. Масло и кърпи са включени.', 'Prices are in euros and cover the whole session. Oil and towels are included.'), cards=cards,
        bf_h=t('Преди да дойдеш', 'Before you come'), before_html=before_html,
        bf_img=I('diffuser', t('Дифузер с пръчици, навита бяла кърпа и две свещи', 'A reed diffuser, a rolled white towel and two candles'), '(min-width: 900px) 490px, calc(100vw - 40px)'),
        team_h=t('Терапевтите', 'The therapists'), team_p=t('Можеш да избереш при кого да дойдеш или да оставиш на нас.', 'You can choose whom to see or leave it to us.'), ther_cards=ther_cards,
        book_h=t('Резервирай', 'Book a time'), book_p=t('Избери масаж и продължителност, ден и час. Виждаш цената. Ще ти се обадим, за да потвърдим.', 'Choose a massage and its length, a day and a time. You see the price. We will call you to confirm.'),
        f_service=t('Масаж', 'Massage'), svc_opts=svc_opts, f_length=t('Продължителност и цена', 'Length and price'), f_ther=t('Терапевт', 'Therapist'), ther_opts=ther_opts, f_date=t('Дата', 'Date'), f_time=t('Час', 'Time'),
        checking=t('Избери масаж и дата, за да видиш свободните часове.', 'Choose a massage and a date to see the free times.'),
        f_name=t('Име', 'Name'), f_phone=t('Телефон', 'Phone'), f_gift=t('Това е подарък за друг човек (ще подготвим ваучер)', 'This is a gift for someone else (we will prepare a voucher)'),
        f_msg=t('Бележка (по желание)', 'Note (optional)'), f_msg_h=t('Не пиши подробна медицинска информация тук. Кажи я на терапевта преди масажа.', 'Please do not write detailed medical information here. Tell the therapist before the massage.'),
        f_send=t('Заяви резервация', 'Request the booking'), f_note=t('Не е нужно да плащаш предварително.', 'You do not have to pay in advance.'), f_priv=t('Поверителност', 'Privacy'), privacy_href='privacy.html',
        faq_h=t('Често задавани въпроси', 'Common questions'), faq_html=faq_html,
        cl1=I('drops', t('Ръце капят етерично масло от стъклена бутилка', 'Hands dropping essential oil from a glass bottle'), '(min-width: 900px) 364px, calc(100vw - 40px)'), cl2=I('sauna', t('Дървена пейка в сауна с кофа и жълта кърпа', 'A wooden sauna bench with a bucket and a yellow towel'), '(min-width: 900px) 364px, calc(100vw - 40px)'), cl3=I('stones-room', t('Жена лежи на масажна маса с камъни по гърба в топла стая', 'A woman lying on a massage table with stones on her back in a warm room'), '(min-width: 900px) 364px, calc(100vw - 40px)'),
        visit_h=t('Контакти', 'Contact'), hours_html=hours_html, l_addr=t('Адрес', 'Address'), l_phone=t('Телефон', 'Phone'), l_email=t('Имейл', 'Email'),
        visit_note=t('Последният час започва един час и половина преди затваряне.', 'The last session starts an hour and a half before closing.'),
        map_t=t('Картата се зарежда от OpenStreetMap едва когато я поискаш.', 'The map loads from OpenStreetMap only when you ask for it.'), map_btn=t('Покажи картата', 'Show the map'),
        foot_demo=t('Всичко тук е пример.', 'Everything here is an example.'), admin_href='admin.html' if bg else '../admin.html?lang=en', admin_l=t('Демо админ панел', 'Demo back office'),
        dock_label=t('Цветова схема', 'Colour scheme'), skin_name=t('Глина', 'Clay'), swatches=swatches,
        data=json.dumps(data, ensure_ascii=False).replace('</', '<\\/'),
    )


def main():
    cfg = ('/* Generated by tools/build_pages.py. Edit the values at the top of that file, then run it again. */\n'
           'window.TISHINA_CONFIG = {\n  mode: "demo",            /* "demo" = requests are kept in this browser only; "live" = real API at apiBase (docs/API.md) */\n'
           '  apiBase: "/api",\n  hours: { weekday: ["%s", "%s"], weekend: ["%s", "%s"] },\n  capacity: %d,             /* treatment rooms */\n'
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
