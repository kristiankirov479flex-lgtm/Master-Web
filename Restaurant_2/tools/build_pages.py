"""Builds index.html (Bulgarian), en/index.html (English), js/config.js and css/style.css for Bashta (a traditional Bulgarian tavern).
Edit the values in this file (menu, prices, hours, texts), then run:  python tools/build_pages.py && python tools/build_privacy.py
Everything about the tavern is an example: replace it for a real restaurant."""
import json, os
from html import escape as esc
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BRAND = 'Bashta'

# ---------------- settings you will change for a real restaurant ----------------
HOURS = {'weekday': ['11:30', '21:30'], 'weekend': ['12:00', '21:30']}   # kitchen hours: first and last start of a delivery or pick-up window
CAPACITY = 4          # orders per time window
SLOT_MINUTES = 30
LEAD_MINUTES = 45     # a same-day order needs this much notice
MIN_DELIVERY = 12     # minimum order for delivery, euro
DELIVERY_FEE, FREE_DELIVERY_FROM = 2.0, 25
PHONE, PHONE_HREF, EMAIL = '+359 88 000 0000', '+359880000000', 'hello@example.com'
ADDRESS = {'bg': 'ул. Примерна 8, Пловдив', 'en': '8 Primer St., Plovdiv'}

# groups: id, bg title, en title, photo (or None); items: id, price, tag, (bg name, en name), (bg text, en text)
MENU = [
 ('salads', 'Салати', 'Salads', 'salad-greek', [
  ('shopska', 6.5, 'V', ('Шопска салата', 'Shopska salad'), ('Домати, краставици, чушки, сирене', 'Tomatoes, cucumbers, peppers, white cheese')),
  ('snezhanka', 6.0, 'V', ('Снежанка', 'Snezhanka'), ('Кисело мляко, краставици, орехи, копър', 'Yoghurt, cucumber, walnuts, dill')),
  ('peppers', 7.0, 'V', ('Печени чушки с чесън', 'Roasted peppers with garlic'), ('С орехи и магданоз', 'With walnuts and parsley')),
  ('tarator', 5.0, 'V', ('Таратор', 'Tarator'), ('Студена супа от кисело мляко и краставици', 'Cold yoghurt and cucumber soup'))]),
 ('soups', 'Супи', 'Soups', None, [
  ('chicken', 4.5, '', ('Пилешка супа', 'Chicken soup'), ('По домашна рецепта', 'A home recipe')),
  ('beans', 4.5, 'V', ('Боб чорба', 'Bean soup'), ('С чубрица и сушена чушка', 'With savory and dried pepper'))]),
 ('grill', 'От скарата', 'From the grill', 'grill-platter', [
  ('kebapche', 4.0, '', ('Кебапче (2 бр.)', 'Kebapche (2 pieces)'), ('', '')), ('kyufte', 4.4, '', ('Кюфте (2 бр.)', 'Kyufte (2 pieces)'), ('', '')),
  ('chop', 9.5, '', ('Свински котлет', 'Pork chop'), ('С печен лук', 'With roasted onion')), ('skewer', 8.5, '', ('Пилешки шиш', 'Chicken skewer'), ('С чушка и лук', 'With pepper and onion')),
  ('lamb', 16.0, '', ('Агнешки ребра', 'Lamb chops'), ('Четири парчета', 'Four pieces')), ('grill2', 24.0, '', ('Скара за двама', 'Grill for two'), ('Кебапче, кюфте, котлет, шиш, гарнитура', 'Kebapche, kyufte, chop, skewer and sides'))]),
 ('pots', 'Ястия от гювеч', 'Pot dishes', 'clay-pot', [
  ('gyuvech', 9.5, '', ('Гювеч', 'Gyuvech'), ('Свинско, зеленчуци, яйце, сирене', 'Pork, vegetables, egg and cheese')), ('kavarma', 10.5, '', ('Кавърма', 'Kavarma'), ('Бавно готвено свинско с лук и вино', 'Slow-cooked pork with onion and wine')),
  ('sarmi', 9.0, '', ('Сарми', 'Sarmi'), ('Зелеви листа с кайма и ориз', 'Cabbage rolls with mince and rice')), ('moussaka', 8.5, '', ('Мусака', 'Moussaka'), ('С картофи и кайма, запечена', 'Baked, with potatoes and mince')),
  ('lambrice', 12.5, '', ('Агнешко с ориз', 'Lamb with rice'), ('Печено в гювеч', 'Baked in a clay pot'))]),
 ('sides', 'Гарнитури', 'Sides', None, [
  ('fries', 3.5, 'V', ('Пържени картофи', 'French fries'), ('', '')), ('baked', 4.0, 'V', ('Печени картофи с чубрица', 'Baked potatoes with savory'), ('', '')),
  ('pickles', 4.5, 'V', ('Туршия', 'Pickled vegetables'), ('', '')), ('bread', 1.0, 'V', ('Хляб', 'Bread'), ('', ''))]),
 ('desserts', 'Десерти', 'Desserts', None, [
  ('baklava', 4.5, 'V', ('Баклава', 'Baklava'), ('С орехи и сироп', 'With walnuts and syrup')), ('pumpkin', 4.0, 'V', ('Тиквеник', 'Pumpkin pastry'), ('С орехи и канела', 'With walnuts and cinnamon')),
  ('honey', 4.0, 'V', ('Кисело мляко с мед и орехи', 'Yoghurt with honey and walnuts'), ('', ''))]),
 ('drinks', 'Напитки', 'Drinks', None, [
  ('ayran', 2.5, 'V', ('Айрян', 'Ayran'), ('', '')), ('lemonade', 3.5, 'V', ('Домашна лимонада', 'Homemade lemonade'), ('', '')), ('water', 2.0, 'V', ('Минерална вода', 'Mineral water'), ('0,5 л', '0.5 l')),
  ('beer', 3.5, 'V', ('Бира', 'Beer'), ('Местна, 0,5 л', 'Local, 0.5 l')), ('wine', 4.0, 'V', ('Вино на чаша', 'Wine by the glass'), ('Червено или бяло', 'Red or white'))]),
]

SKINS = [('oak', 'Дъб', 'Oak', '#F6EFE2', '#8E2A1F'), ('olive', 'Маслина', 'Olive', '#F3F1E4', '#4A5A2A'), ('indigo', 'Индиго', 'Indigo', '#F2F3F7', '#243B6B'),
         ('night', 'Нощ', 'Night', '#1E1712', '#E0A458'), ('pomegranate', 'Нар', 'Pomegranate', '#FBF1F2', '#8A1F44')]


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

    alts = {'salad-greek': t('Салата с домати, краставици, маслини и сирене', 'A salad with tomatoes, cucumbers, olives and white cheese'),
            'grill-platter': t('Голяма чиния със скара и гарнитури', 'A large plate of grilled meats and sides'), 'clay-pot': t('Ястие в глинен гювеч със капаче', 'A dish in a clay pot with a lid')}
    groups = []
    for gid, gb, ge, photo, items in MENU:
        rows = []
        for iid, price, tag, nm, ds in items:
            tg = '<span class="tag" title="%s">V</span>' % t('Вегетарианско', 'Vegetarian') if tag else ''
            rows.append('<li class="item"><div class="item-t"><h4>%s %s</h4>%s</div><b class="price">%s</b><button class="add" type="button" data-id="%s" aria-label="%s"><span aria-hidden="true">+</span><span class="add-n" hidden></span></button></li>'
                        % (esc(nm[i]), tg, ('<p>%s</p>' % esc(ds[i])) if ds[i] else '', money(price), iid, esc(t('Добави ', 'Add ') + nm[i])))
        fig = ('<figure class="g-ph">%s</figure>' % I(photo, alts[photo], '(min-width: 960px) 600px, calc(100vw - 40px)')) if photo else ''
        groups.append('<section class="m-group" aria-labelledby="mg-%s"><h3 id="mg-%s">%s</h3>%s<ul class="items">%s</ul></section>' % (gid, gid, gb if bg else ge, fig, ''.join(rows)))
    menu_html = ''.join(groups)
    hours_rows = [(t('Понеделник – петък', 'Monday – Friday'), HOURS['weekday'], 'wd'), (t('Събота и неделя', 'Saturday and Sunday'), HOURS['weekend'], 'we')]
    hours_html = ''.join('<div data-hrs="%s"><dt>%s</dt><dd>%s – %s</dd></div>' % (k, n, h[0], h[1]) for n, h, k in hours_rows)
    hours_ld = '"Mo-Fr %s-%s","Sa-Su %s-%s"' % (HOURS['weekday'][0], HOURS['weekday'][1], HOURS['weekend'][0], HOURS['weekend'][1])
    swatches = ''.join('<button class="sw" type="button" data-skin="%s" style="--s1:%s;--s2:%s" aria-pressed="false" aria-label="%s"></button>' % (k, s1, s2, b if bg else e) for k, b, e, s1, s2 in SKINS)
    nav = [('#order', t('Меню и поръчка', 'Menu and order')), ('#about', t('За нас', 'About us')), ('#gallery', t('Снимки', 'Photos')), ('#visit', t('Контакти', 'Contact'))]
    nav_html = ''.join('<a href="%s">%s</a>' % n for n in nav)
    data = {'menu': [{'id': it[0], 'price': it[1], 'name': it[3][i]} for g in MENU for it in g[4]], 'min': MIN_DELIVERY, 'fee': DELIVERY_FEE, 'free': FREE_DELIVERY_FROM}

    title = t('Bashta – традиционна механа в Пловдив. Поръчай за вкъщи', 'Bashta – a traditional Bulgarian tavern in Plovdiv. Order online')
    desc = t('Bashta е семейна механа в Пловдив с гювеч, кавърма, скара и шопска салата. Хапни при нас или поръчай за доставка или за вземане.',
             'Bashta is a family tavern in Plovdiv with gyuvech, kavarma, grill and shopska salad. Eat with us or order for delivery or pick-up.')

    return '''<!doctype html>
<html lang="%(lang)s" data-skin="oak">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="theme-color" content="#F6EFE2">
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
     and an og:image (images/stock/table-feast.jpg is a placeholder) -->
<link rel="preload" href="%(root)sfonts/onest-%(script)s.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="%(root)sfonts/playfair-%(script)s.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="%(root)sfonts/fonts.css">
<link rel="stylesheet" href="%(root)scss/style.css">
<script>
  /* Apply the saved colour scheme before the page paints, so it does not flash. */
  try { var s = new URLSearchParams(location.search).get("skin") || localStorage.getItem("bashtaSkin"); if (s) document.documentElement.dataset.skin = s; } catch (e) {}
</script>
<script type="application/ld+json">
{"@context":"https://schema.org","@type":"Restaurant","name":"%(brand)s","inLanguage":"%(lang)s","telephone":"%(phone_href)s","email":"%(email)s",
 "address":{"@type":"PostalAddress","streetAddress":"Primer St. 8","addressLocality":"Plovdiv","addressCountry":"BG"},
 "servesCuisine":"Bulgarian","openingHours":[%(hours_ld)s]}
</script>
</head>
<body>
<a class="skip" href="#main">%(skip)s</a>

<header class="top" id="top">
  <div class="top-in">
    <a class="logo" href="index.html">%(brand)s</a>
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
      <p class="hero-links"><a class="btn btn-main" href="#order">%(cta1)s</a> <a class="btn btn-light" href="#visit">%(cta2)s</a></p>
    </div>
  </section>
  <div class="cloth" aria-hidden="true"></div>
  <div class="info-bar">
    <ul class="wrap info-row">
      <li><b>%(ib1_k)s</b> <span id="todayHours">11:30 – 21:30</span></li>
      <li><b>%(ib2_k)s</b> <span>%(ib2_v)s</span></li>
      <li><b>%(ib3_k)s</b> <a href="tel:%(phone_href)s">%(phone)s</a></li>
    </ul>
  </div>

  <!-- ============ Menu and order ============ -->
  <section class="block" id="order" aria-labelledby="or-h">
    <div class="wrap">
      <header class="sec-head">
        <h2 id="or-h">%(order_h)s</h2>
        <p>%(order_p)s</p>
      </header>
      <div class="order-grid">
        <div class="menu">%(menu_html)s
          <p class="legend"><span class="tag">V</span> %(v)s</p>
        </div>

        <section class="tray" id="tray" aria-labelledby="tray-h">
          <form id="orderForm" novalidate>
            <h3 id="tray-h">%(tray_h)s</h3>
            <p class="tray-empty" id="trayEmpty">%(tray_empty)s</p>
            <ul class="lines" id="lines"></ul>
            <dl class="sums" id="sums" hidden>
              <div><dt>%(sum_l)s</dt><dd id="sumSub">0,00 €</dd></div>
              <div id="feeRow"><dt>%(fee_l)s</dt><dd id="sumFee">0,00 €</dd></div>
              <div class="grand"><dt>%(total_l)s</dt><dd id="sumTotal">0,00 €</dd></div>
            </dl>
            <fieldset class="group"><legend>%(f_how)s</legend>
              <div class="opts">
                <label class="opt"><input type="radio" name="fulfil" value="delivery" checked><span>%(o_deliver)s</span></label>
                <label class="opt"><input type="radio" name="fulfil" value="pickup"><span>%(o_pickup)s</span></label>
              </div>
              <p class="hint" id="howHint"></p>
            </fieldset>
            <div class="field" id="addrRow"><label for="f-addr">%(f_addr)s</label><input id="f-addr" name="address" type="text" autocomplete="street-address"></div>
            <div class="row2">
              <div class="field"><label for="f-date">%(f_date)s</label><select id="f-date" name="date"></select></div>
              <div class="field"><label for="f-time">%(f_time)s</label><select id="f-time" name="time"></select></div>
            </div>
            <p class="hint" id="timeHint" role="status">%(checking)s</p>
            <div class="field"><label for="f-name">%(f_name)s</label><input id="f-name" name="name" type="text" autocomplete="name" required></div>
            <div class="field"><label for="f-phone">%(f_phone)s</label><input id="f-phone" name="phone" type="tel" autocomplete="tel" required></div>
            <div class="field"><label for="f-msg">%(f_msg)s</label><textarea id="f-msg" name="msg" rows="2"></textarea></div>
            <p class="demo-note" id="demoNote" hidden></p>
            <p class="form-error" id="orError" role="alert" hidden></p>
            <button class="btn btn-main btn-block" type="submit" id="send">%(f_send)s</button>
            <small class="fine">%(f_note)s <a href="%(privacy_href)s">%(f_priv)s</a></small>
          </form>
          <div class="done" id="done" hidden tabindex="-1"></div>
        </section>
      </div>
    </div>
  </section>

  <!-- ============ About ============ -->
  <section class="block soft" id="about" aria-labelledby="ab-h">
    <div class="wrap about">
      <div class="about-text">
        <h2 id="ab-h">%(about_h)s</h2>
        <p>%(about_p1)s</p>
        <p>%(about_p2)s</p>
        <ul class="ticks"><li>%(t1)s</li><li>%(t2)s</li><li>%(t3)s</li></ul>
      </div>
      <figure class="about-ph">%(about_img)s</figure>
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
    <span>© <span id="year">2026</span> Bashta. %(foot_demo)s</span>
    <span class="foot-links"><a href="%(privacy_href)s">%(f_priv)s</a> <a href="%(admin_href)s">%(admin_l)s</a></span>
  </div>
</footer>

<div class="actionbar" id="bar" hidden>
  <span id="barTxt"></span>
  <a class="btn btn-main btn-sm" href="#tray">%(bar_cta)s</a>
</div>

<aside class="dock" aria-label="%(dock_label)s">
  <div class="dock-label"><small>%(dock_label)s</small><b id="skinName">%(skin_name)s</b></div>
  <div class="swatches">%(swatches)s</div>
</aside>

<script type="application/json" id="bashtaData">%(data)s</script>
<script src="%(root)sjs/config.js"></script>
<script src="%(root)sjs/api.js"></script>
<script src="%(root)sjs/main.js"></script>
</body>
</html>
''' % dict(
        lang=lang, title=esc(title), desc=esc(desc), root=root, script=script, brand=BRAND, phone_href=PHONE_HREF, phone=PHONE, email=EMAIL, hours_ld=hours_ld,
        skip=t('Към съдържанието', 'Skip to content'), nav_label=t('Навигация', 'Navigation'), nav_html=nav_html,
        other_href=other_href, other_lang='en' if bg else 'bg', other_label='EN' if bg else 'БГ', other_aria='Switch to English' if bg else 'Превключи на български', menu_btn=t('Меню', 'Menu'),
        hero_img=I('table-feast', t('Маса, пълна с традиционни български ястия', 'A table full of traditional Bulgarian dishes'), '100vw', eager=True),
        eyebrow=t('Механа · Пловдив', 'Tavern · Plovdiv'), h1=t('Традиционна българска кухня, сготвена бавно', 'Traditional Bulgarian food, cooked slowly'),
        lead=t('Гювеч, кавърма и скара, както ги правеше баба. Хапни при нас или поръчай за вкъщи.', 'Gyuvech, kavarma and grill, the way grandmother made them. Eat with us or order to take home.'),
        cta1=t('Поръчай онлайн', 'Order online'), cta2=t('Как да ни намериш', 'How to find us'),
        ib1_k=t('Днес', 'Today'), ib2_k=t('Доставка', 'Delivery'), ib2_v=t('В Пловдив, 2 € · безплатна над 25 €', 'In Plovdiv, €2 · free over €25'), ib3_k=t('Маси', 'Tables'),
        order_h=t('Меню и поръчка', 'Menu and order'), order_p=t('Натисни „+“ до ястията, които искаш. Вдясно избираш доставка или вземане и час. Плащаш при получаване. За маса при нас се обади по телефона.', 'Press “+” next to the dishes you want. On the right you choose delivery or pick-up and a time. You pay on receipt. To book a table here, please call us.'),
        v=t('вегетарианско', 'vegetarian'), menu_html=menu_html,
        tray_h=t('Твоята поръчка', 'Your order'), tray_empty=t('Още няма нищо тук. Добави ястия от менюто.', 'Nothing here yet. Add dishes from the menu.'),
        sum_l=t('Ястия', 'Dishes'), fee_l=t('Доставка', 'Delivery'), total_l=t('Общо', 'Total'), f_how=t('Как да го получиш?', 'How do you want it?'), o_deliver=t('Доставка', 'Delivery'), o_pickup=t('Вземане от механата', 'Pick up at the tavern'),
        f_addr=t('Адрес за доставка', 'Delivery address'), f_date=t('Ден', 'Day'), f_time=t('Час', 'Time'), checking=t('Проверяваме свободните часове…', 'Checking free times…'),
        f_name=t('Име', 'Name'), f_phone=t('Телефон', 'Phone'), f_msg=t('Бележка (по желание)', 'Note (optional)'),
        f_send=t('Изпрати поръчката', 'Place the order'), f_note=t('Плащаш в брой или с карта при получаване.', 'You pay cash or card on receipt.'), f_priv=t('Поверителност', 'Privacy'), privacy_href='privacy.html',
        about_h=t('За нас', 'About us'),
        about_p1=t('Бащата на Иван, който държи механата, строи къщата преди повече от седемдесет години. Днес в нея има две зали с дървен таван и двор с асма.', 'Ivan, who runs the tavern, had his father build this house more than seventy years ago. Today it has two rooms with wooden ceilings and a yard with a grapevine.'),
        about_p2=t('Готвим по рецептите на семейството: гювечът се пече в глинени съдове, кавърмата се готви два часа, а месото за скарата идва от месар в града.', 'We cook the family recipes: the gyuvech is baked in clay pots, the kavarma cooks for two hours and the meat for the grill comes from a butcher in town.'),
        t1=t('Глинени гювечи, печени на фурна', 'Clay pots baked in the oven'), t2=t('Зеленчуци от пазара всяка сутрин', 'Vegetables from the market every morning'), t3=t('Доставка и вземане до 21:30', 'Delivery and pick-up until 21:30'),
        about_img=I('table-friends', t('Приятели около маса с много ястия', 'Friends around a table full of dishes'), '(min-width: 900px) 500px, calc(100vw - 40px)'),
        gallery_h=t('В механата', 'At the tavern'), gallery_p=t('Двете зали, дворът и част от кухнята.', 'The two rooms, the yard and part of the kitchen.'),
        g1=I('room-checkered', t('Зала с дървен таван и червено-бели покривки', 'A room with a wooden ceiling and red and white tablecloths'), '(min-width: 900px) 350px, 45vw'), g2=I('room-wood', t('Дървена зала с маси', 'A wood-panelled room with tables'), '(min-width: 900px) 350px, 45vw'), g3=I('room-garden', t('Двор с растения и маси', 'A yard with plants and tables'), '(min-width: 900px) 350px, 45vw'),
        g4=I('lamb-chops', t('Агнешки ребра с колбаси', 'Lamb chops with sausages'), '(min-width: 900px) 350px, 45vw'), g5=I('kebabs', t('Шишчета и сосове', 'Skewers and sauces'), '(min-width: 900px) 350px, 45vw'), g6=I('easter-table', t('Празнична трапеза', 'A festive table'), '(min-width: 900px) 350px, 45vw'),
        visit_h=t('Контакти', 'Contact'), hours_html=hours_html, l_addr=t('Адрес', 'Address'), address=ADDRESS['bg' if bg else 'en'], l_phone=t('Телефон', 'Phone'), l_email=t('Имейл', 'Email'),
        visit_note=t('Резервации за маса приемаме само по телефона. За групи над 10 души се обадете поне ден по-рано.', 'We take table reservations by phone only. For groups of more than 10 please call at least a day ahead.'),
        map_t=t('Картата се зарежда от OpenStreetMap едва когато я поискаш.', 'The map loads from OpenStreetMap only when you ask for it.'), map_btn=t('Покажи картата', 'Show the map'),
        foot_demo=t('Всичко тук е пример.', 'Everything here is an example.'), admin_href='admin.html' if bg else '../admin.html?lang=en', admin_l=t('Демо админ панел', 'Demo back office'),
        bar_cta=t('Виж поръчката', 'View order'), dock_label=t('Цветова схема', 'Colour scheme'), skin_name=t('Дъб', 'Oak'), swatches=swatches,
        data=json.dumps(data, ensure_ascii=False).replace('</', '<\\/'),
    )


def main():
    cfg = ('/* Generated by tools/build_pages.py. Edit the values at the top of that file, then run it again. */\n'
           'window.BASHTA_CONFIG = {\n  mode: "demo",            /* "demo" = requests are kept in this browser only; "live" = real API at apiBase (docs/API.md) */\n'
           '  apiBase: "/api",\n  hours: { weekday: ["%s", "%s"], weekend: ["%s", "%s"] },\n  capacity: %d,             /* orders per time window */\n'
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
