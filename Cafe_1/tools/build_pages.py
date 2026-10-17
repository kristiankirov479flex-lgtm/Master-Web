"""Builds index.html (Bulgarian), en/index.html (English), js/config.js and css/style.css for Little Moka.
Edit the values in this file (menu, prices, hours, texts), then run:  python tools/build_pages.py && python tools/build_privacy.py
Everything about the café is an example: replace it for a real café."""
import json, os
from html import escape as esc
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BRAND = 'Little Moka'

# ---------------- settings you will change for a real café ----------------
HOURS = {'weekday': ['07:30', '18:00'], 'weekend': ['08:30', '17:00']}
CAPACITY = 3          # orders that can be picked up at the same time
SLOT_MINUTES = 10     # gap between pick-up times
LEAD_MINUTES = 15     # a same-day order needs this much notice
MILK = [('whole', 0.0), ('oat', 0.6), ('almond', 0.6), ('lf', 0.3)]
PHONE, PHONE_HREF, EMAIL = '+359 88 000 0000', '+359880000000', 'hello@example.com'
ADDRESS = {'bg': 'ул. Примерна 12, Пловдив', 'en': '12 Primer St., Plovdiv'}

# id, category, price, drink-with-milk, tags, (bg name, en name), (bg desc, en desc)
MENU = [
 ('espresso', 'coffee', 2.2, False, '', ('Еспресо', 'Espresso'), ('Къс и плътен, от нашата смес', 'Short and dense, from our house blend')),
 ('doppio', 'coffee', 3.2, False, '', ('Двойно еспресо', 'Double espresso'), ('Два шота, за по-дълго утро', 'Two shots, for a longer morning')),
 ('americano', 'coffee', 2.9, False, '', ('Американо', 'Americano'), ('Еспресо с гореща вода', 'Espresso with hot water')),
 ('flat-white', 'coffee', 4.2, True, '', ('Флат уайт', 'Flat white'), ('Двойно еспресо и копринено мляко', 'Double espresso and silky milk')),
 ('cappuccino', 'coffee', 3.9, True, '', ('Капучино', 'Cappuccino'), ('Равни части кафе, мляко и пяна', 'Equal parts coffee, milk and foam')),
 ('latte', 'coffee', 4.2, True, '', ('Лате', 'Latte'), ('Меко, с много мляко', 'Soft, with plenty of milk')),
 ('mocha', 'coffee', 4.6, True, '', ('Мока', 'Mocha'), ('Еспресо, тъмен шоколад и мляко', 'Espresso, dark chocolate and milk')),
 ('v60', 'coffee', 4.5, False, 'VG', ('Филтър V60', 'V60 filter coffee'), ('Ръчно приготвено, светло изпечено', 'Hand-brewed, light roast')),
 ('hot-choc', 'drinks', 4.4, True, 'V', ('Топъл шоколад', 'Hot chocolate'), ('Гъст, с истински шоколад', 'Thick, made with real chocolate')),
 ('matcha', 'drinks', 4.8, True, 'V', ('Матча лате', 'Matcha latte'), ('Японска матча и мляко', 'Japanese matcha and milk')),
 ('chai', 'drinks', 4.6, True, 'V', ('Чай лате', 'Chai latte'), ('Подправен чай с мляко', 'Spiced tea with milk')),
 ('orange', 'drinks', 4.5, False, 'VG', ('Пресен портокал', 'Fresh orange juice'), ('Изцеден на момента', 'Squeezed to order')),
 ('iced-tea', 'drinks', 3.8, False, 'VG', ('Леден чай', 'Iced tea'), ('Домашен, с лимон и мента', 'Homemade, with lemon and mint')),
 ('cold-brew', 'drinks', 4.6, False, 'VG', ('Колд брю', 'Cold brew'), ('18 часа бавно запарено', 'Slowly brewed for 18 hours')),
 ('croissant', 'bakery', 2.8, False, 'V', ('Кроасан с масло', 'Butter croissant'), ('Печен всяка сутрин от 6:30', 'Baked every morning from 6:30')),
 ('pain-choc', 'bakery', 3.2, False, 'V', ('Кроасан с шоколад', 'Pain au chocolat'), ('Две ленти тъмен шоколад', 'Two bars of dark chocolate')),
 ('cinnamon', 'bakery', 3.6, False, 'V', ('Руло с канела', 'Cinnamon roll'), ('Топло, със сметанов крем', 'Warm, with cream icing')),
 ('banana', 'bakery', 3.4, False, 'V', ('Банан хляб', 'Banana bread'), ('Влажен, с орехи', 'Moist, with walnuts')),
 ('pastry', 'bakery', 3.5, False, '', ('Пастет със сирене и шунка', 'Ham and cheese pastry'), ('Хрупкаво тесто, топъл пълнеж', 'Crisp dough, warm filling')),
 ('cheesecake', 'bakery', 5.2, False, 'V', ('Чийзкейк', 'Cheesecake slice'), ('Класически, с плодов сос', 'Classic, with fruit sauce')),
 ('avo', 'brunch', 8.9, False, 'V', ('Тост с авокадо', 'Avocado toast'), ('Ръжен хляб, авокадо, лимон, чили', 'Rye bread, avocado, lemon, chilli')),
 ('eggs', 'brunch', 7.9, False, 'V', ('Яйца на тост', 'Eggs on toast'), ('Две яйца по избор на хляб със заквасена сметана', 'Two eggs your way on sourdough')),
 ('granola', 'brunch', 6.9, False, 'V', ('Купа с гранола', 'Granola bowl'), ('Кисело мляко, гранола, сезонни плодове', 'Yoghurt, granola, seasonal fruit')),
 ('toastie', 'brunch', 6.5, False, '', ('Тост с шунка и сирене', 'Ham and cheese toastie'), ('Топъл, с горчица и корнишон', 'Hot, with mustard and gherkin')),
 ('soup', 'brunch', 5.5, False, '', ('Супа на деня', 'Soup of the day'), ('Със своя хляб, от 11:00', 'With bread, from 11:00')),
]
CATS = [('all', 'Всичко', 'All'), ('coffee', 'Кафе', 'Coffee'), ('drinks', 'Други напитки', 'Other drinks'), ('bakery', 'Пекарна', 'Bakery'), ('brunch', 'Брънч', 'Brunch')]

# colour schemes: key, bg name, en name, swatch 1, swatch 2
SKINS = [('latte', 'Лате', 'Latte', '#FBF3E8', '#B5472A'), ('matcha', 'Матча', 'Matcha', '#F2F4E8', '#4C6B2A'),
         ('berry', 'Малина', 'Berry', '#FFF1F2', '#B8264F'), ('espresso', 'Еспресо', 'Espresso', '#1E1511', '#E8A15D'),
         ('blueberry', 'Боровинка', 'Blueberry', '#EEF1FA', '#3B4FBF')]


def dims(name):
    with Image.open(os.path.join(ROOT, 'images', 'stock', name + '.jpg')) as im:
        return im.size


def img(name, alt, sizes, cls='', eager=False, ratio=None):
    w, h = dims(name)
    attrs = ' loading="eager" fetchpriority="high"' if eager else ' loading="lazy" decoding="async"'
    c = ' class="%s"' % cls if cls else ''
    return ('<img%s src="images/stock/%s-800.jpg" srcset="images/stock/%s-800.jpg 800w, images/stock/%s.jpg 1600w" sizes="%s" width="%d" height="%d" alt="%s"%s>'
            % (c, name, name, name, sizes, w, h, esc(alt), attrs))


def build(lang):
    bg = lang == 'bg'
    t = lambda a, b: a if bg else b
    root = '' if bg else '../'
    I = lambda *a, **k: img(*a, **k).replace('src="images', 'src="' + root + 'images').replace('srcset="images', 'srcset="' + root + 'images').replace(', images', ', ' + root + 'images')
    home = 'index.html'
    other_href = 'en/index.html' if bg else '../index.html'
    privacy_href = 'privacy.html'
    script = 'cyrillic' if bg else 'latin'

    def money(v):
        return ('%.2f' % v).replace('.', ',' if bg else '.') + ' €'

    cats = ''.join('<button class="chip" type="button" data-cat="%s" aria-pressed="%s">%s</button>' % (k, 'true' if k == 'all' else 'false', b if bg else e) for k, b, e in CATS)
    groups = []
    for k, b, e in CATS[1:]:
        items = []
        for iid, cat, price, milk, tags, nm, ds in [m for m in MENU if m[1] == k]:
            tg = ''.join('<span class="tag" title="%s">%s</span>' % (t('Вегетарианско', 'Vegetarian') if x == 'V' else t('Веган', 'Vegan'), x) for x in ([tags] if tags else []))
            items.append('''<li class="item" data-id="%s" data-cat="%s">
            <div class="item-t"><h4>%s%s</h4><p>%s</p></div>
            <b class="price">%s</b>
            <button class="add" type="button" data-id="%s" aria-label="%s"><span aria-hidden="true">+</span><span class="add-n" hidden></span></button>
          </li>''' % (iid, cat, esc(nm[0] if bg else nm[1]), (' ' + tg) if tg else '', esc(ds[0] if bg else ds[1]), money(price), iid,
                      esc(t('Добави ', 'Add ') + (nm[0] if bg else nm[1]))))
        groups.append('<div class="mgroup" data-cat="%s"><h3>%s</h3><ul class="items">%s</ul></div>' % (k, b if bg else e, ''.join(items)))
    menu_html = '\n        '.join(groups)

    hours_rows = [(t('Понеделник – петък', 'Monday – Friday'), HOURS['weekday'], 'wd'), (t('Събота и неделя', 'Saturday and Sunday'), HOURS['weekend'], 'we')]
    hours_html = ''.join('<div data-hrs="%s"><dt>%s</dt><dd>%s – %s</dd></div>' % (k, n, h[0], h[1]) for n, h, k in hours_rows)
    hours_ld = '"Mo-Fr %s-%s","Sa-Su %s-%s"' % (HOURS['weekday'][0], HOURS['weekday'][1], HOURS['weekend'][0], HOURS['weekend'][1])

    swatches = ''.join('<button class="sw" type="button" data-skin="%s" style="--s1:%s;--s2:%s" aria-pressed="false" aria-label="%s"></button>' % (k, s1, s2, b if bg else e) for k, b, e, s1, s2 in SKINS)
    nav = [('#order', t('Меню и поръчка', 'Menu and order')), ('#bakery', t('Пекарна', 'Bakery')), ('#card', t('Карта', 'Loyalty card')), ('#visit', t('Адрес', 'Visit'))]
    nav_html = ''.join('<a href="%s">%s</a>' % nav_i for nav_i in nav)

    data = {'menu': [{'id': m[0], 'cat': m[1], 'price': m[2], 'milk': m[3], 'name': m[5][0 if bg else 1]} for m in MENU],
            'milk': [{'id': k, 'add': a, 'name': n} for (k, a), n in zip(MILK, t(['Пълномаслено', 'Овесено (+0,60 €)', 'Бадемово (+0,60 €)', 'Безлактозно (+0,30 €)'],
                                                                             ['Whole milk', 'Oat (+0.60 €)', 'Almond (+0.60 €)', 'Lactose-free (+0.30 €)']))]}

    stamps = ''.join('<li class="stamp%s" aria-hidden="true">%s</li>' % (' free' if i == 9 else '', '✓' if i < 9 else '★') for i in range(10))

    title = t('Little Moka – кафене и пекарна в Пловдив. Поръчай напред и вземи без опашка', 'Little Moka – café and bakery in Plovdiv. Order ahead and skip the queue')
    desc = t('Little Moka е кафене и пекарна с печени всяка сутрин кроасани и кафе от собствена смес. Избери от менюто, избери час и вземи поръчката си без опашка.',
             'Little Moka is a café and bakery with croissants baked every morning and coffee from our own blend. Choose from the menu, pick a time and collect without queuing.')

    return '''<!doctype html>
<html lang="%(lang)s" data-skin="latte">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="theme-color" content="#FBF3E8">
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
     and an og:image (images/stock/latte-croissants.jpg is a placeholder) -->
<link rel="preload" href="%(root)sfonts/onest-%(script)s.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="%(root)sfonts/nunito-%(script)s.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="%(root)sfonts/fonts.css">
<link rel="stylesheet" href="%(root)scss/style.css">
<script>
  /* Scroll animations only run when the browser supports them and the visitor has not asked for less motion. */
  if ("IntersectionObserver" in window && !matchMedia("(prefers-reduced-motion: reduce)").matches) document.documentElement.classList.add("js-reveal");
</script>
<script>
  /* Apply the saved colour scheme before the page paints, so it does not flash. */
  try { var s = new URLSearchParams(location.search).get("skin") || localStorage.getItem("mokaSkin"); if (s) document.documentElement.dataset.skin = s; } catch (e) {}
</script>
<script type="application/ld+json">
{"@context":"https://schema.org","@type":"CafeOrCoffeeShop","name":"%(brand)s","inLanguage":"%(lang)s","telephone":"%(phone_href)s","email":"%(email)s",
 "address":{"@type":"PostalAddress","streetAddress":"Primer St. 12","addressLocality":"Plovdiv","addressCountry":"BG"},
 "servesCuisine":"Coffee, bakery, brunch","openingHours":[%(hours_ld)s]}
</script>
</head>
<body>
<a class="skip" href="#main">%(skip)s</a>

<header class="top" id="top">
  <div class="top-in">
    <a class="logo" href="%(home)s"><svg viewBox="0 0 32 32" width="30" height="30" aria-hidden="true" focusable="false"><path d="M5 12h19v7a8 8 0 0 1-8 8h-3a8 8 0 0 1-8-8z" fill="currentColor"/><path d="M24 14h2.5a3.5 3.5 0 0 1 0 7H24" fill="none" stroke="currentColor" stroke-width="2.2"/><path d="M11 3c-1.5 2 1.5 3 0 6M17 3c-1.5 2 1.5 3 0 6" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/></svg><b>%(brand)s</b></a>
    <nav class="nav" id="nav" aria-label="%(nav_label)s">%(nav_html)s</nav>
    <div class="top-r">
      <span class="open-pill" data-state="unknown"><i aria-hidden="true"></i><span class="open-text">%(hours_short)s</span></span>
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
        <div class="hero-actions">
          <a class="btn btn-main" href="#order">%(cta1)s</a>
          <a class="btn btn-line" href="#visit">%(cta2)s</a>
        </div>
        <p class="open-pill open-pill-m" data-state="unknown"><i aria-hidden="true"></i><span class="open-text">%(hours_short)s</span></p>
        <p class="next" id="nextSlot" role="status"><span class="next-dot" aria-hidden="true"></span><span id="nextText">%(next_check)s</span></p>
      </div>
      <div class="hero-photos">
        <figure class="ph ph-main">%(ph_main)s</figure>
        <figure class="ph ph-a">%(ph_a)s<figcaption>%(cap_a)s</figcaption></figure>
        <figure class="ph ph-b">%(ph_b)s<figcaption>%(cap_b)s</figcaption></figure>
        <p class="sticker" aria-hidden="true"><b>%(sticker_b)s</b><span>%(sticker_s)s</span></p>
      </div>
    </div>
  </section>

  <!-- ============ Today's board ============ -->
  <section class="board-sec" aria-labelledby="bd-h">
    <div class="wrap board">
      <div class="board-head">
        <p class="kicker kicker-dark">%(k_board)s</p>
        <h2 id="bd-h">%(board_h)s</h2>
        <p>%(board_p)s</p>
      </div>
      <ul class="board-list">
        <li><span>%(b1_k)s</span><b>%(b1_v)s</b></li>
        <li><span>%(b2_k)s</span><b>%(b2_v)s</b></li>
        <li><span>%(b3_k)s</span><b>%(b3_v)s</b></li>
        <li><span>%(b4_k)s</span><b>%(b4_v)s</b></li>
      </ul>
    </div>
  </section>

  <!-- ============ Menu and order ============ -->
  <section class="block" id="order" aria-labelledby="or-h">
    <div class="wrap">
      <header class="sec-head">
        <p class="kicker">%(k_order)s</p>
        <h2 id="or-h">%(order_h)s</h2>
        <p>%(order_p)s</p>
      </header>
      <div class="order-grid">
        <div class="menu">
          <div class="chips" id="cats" role="group" aria-label="%(cat_label)s">%(cats)s</div>
          <p class="legend"><span class="tag">V</span> %(v)s &nbsp; <span class="tag">VG</span> %(vg)s</p>
          %(menu_html)s
        </div>

        <section class="tray" id="tray" aria-labelledby="tray-h">
          <form id="orderForm" novalidate>
            <h3 id="tray-h">%(tray_h)s</h3>
            <p class="tray-empty" id="trayEmpty">%(tray_empty)s</p>
            <ul class="lines" id="lines"></ul>
            <p class="total" id="totalRow" hidden><span>%(total_l)s</span><b id="total">0,00 €</b></p>

            <fieldset class="pick">
              <legend>%(pick_h)s</legend>
              <div class="dchips" id="dchips" role="radiogroup" aria-label="%(pick_day)s"></div>
              <p class="hint" id="slotHint" role="status">%(checking)s</p>
              <div class="tchips" id="tchips" role="radiogroup" aria-label="%(f_time)s"></div>
            </fieldset>

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

  <!-- ============ Bakery ============ -->
  <section class="block bakery" id="bakery" aria-labelledby="bk-h">
    <div class="wrap bakery-in">
      <div class="bakery-copy">
        <p class="kicker">%(k_bakery)s</p>
        <h2 id="bk-h">%(bakery_h)s</h2>
        <p>%(bakery_p)s</p>
        <ul class="ticks">
          <li>%(bk1)s</li><li>%(bk2)s</li><li>%(bk3)s</li>
        </ul>
      </div>
      <div class="bakery-photos">
        <figure class="bp bp-1">%(bp1)s</figure>
        <figure class="bp bp-2">%(bp2)s</figure>
        <figure class="bp bp-3">%(bp3)s</figure>
      </div>
    </div>
  </section>

  <!-- ============ Loyalty ============ -->
  <section class="block soft" id="card" aria-labelledby="cd-h">
    <div class="wrap card-in">
      <header class="sec-head">
        <p class="kicker">%(k_card)s</p>
        <h2 id="cd-h">%(card_h)s</h2>
        <p>%(card_p)s</p>
      </header>
      <div class="stampcard">
        <p class="stamp-t">%(card_t)s</p>
        <ol class="stamps">%(stamps)s</ol>
        <p class="stamp-f">%(card_f)s</p>
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
        <ul class="good">
          <li>%(g1)s</li><li>%(g2)s</li><li>%(g3)s</li><li>%(g4)s</li>
        </ul>
      </div>
      <div class="visit-side">
        <figure class="visit-ph">%(ph_visit)s</figure>
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
    <span>© <span id="year">2026</span> Little Moka. %(foot_demo)s</span>
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

<script type="application/json" id="mokaData">%(data)s</script>
<script src="%(root)sjs/config.js"></script>
<script src="%(root)sjs/api.js"></script>
<script src="%(root)sjs/main.js"></script>
</body>
</html>
''' % dict(
        lang=lang, title=esc(title), desc=esc(desc), root=root, script=script, brand=BRAND, phone_href=PHONE_HREF, email=EMAIL, hours_ld=hours_ld,
        skip=t('Към съдържанието', 'Skip to content'), home=home, nav_label=t('Навигация', 'Navigation'), nav_html=nav_html,
        hours_short=t('Часове за работа', 'Opening hours'), other_href=other_href, other_lang='en' if bg else 'bg', other_label='EN' if bg else 'БГ',
        other_aria='Switch to English' if bg else 'Превключи на български', menu_btn=t('Меню', 'Menu'),
        eyebrow=t('Кафене и пекарна · Пловдив', 'Café and bakery · Plovdiv'),
        h1=t('Хубаво кафе. <em>Без опашка.</em>', 'Good coffee. <em>No queue.</em>'),
        lead=t('Избери от менюто, избери час и вземи поръчката си топла от плота. Кафето е от собствена смес, а кроасаните се пекат тук всяка сутрин.',
               'Pick from the menu, choose a time and collect your order warm from the counter. The coffee is our own blend and the croissants are baked here every morning.'),
        cta1=t('Поръчай напред', 'Order ahead'), cta2=t('Адрес и часове', 'Address and hours'), next_check=t('Проверяваме първия свободен час…', 'Checking the first free time…'),
        ph_main=I('latte-croissants', t('Лате с рисунка до пресни кроасани', 'A latte with latte art next to fresh croissants'), '(min-width: 960px) 560px, 92vw', eager=True),
        ph_a=I('hall-tiles', t('Салонът с плочки на пода и високи маси', 'The café hall with tiled floor and high tables'), '(min-width: 960px) 260px, 44vw'),
        ph_b=I('croissants-tray', t('Поднос с току-що изпечени кроасани', 'A tray of freshly baked croissants'), '(min-width: 960px) 260px, 44vw'),
        cap_a=t('Салонът', 'The hall'), cap_b=t('От фурната', 'From the oven'), sticker_b=t('от 6:30', 'from 6:30'), sticker_s=t('прясна пекарна', 'fresh bakery'),
        k_board=t('Днес на плота', 'Today at the counter'), board_h=t('Дъската на деня', "Today's board"),
        board_p=t('Примерни неща от дъската. В истинско кафене ги сменяте всеки ден.', 'Sample items from the board. A real café changes them every day.'),
        b1_k=t('Кафе на деня', 'Coffee of the day'), b1_v=t('Етиопия, филтър · 4,80 €', 'Ethiopia, filter · €4.80'),
        b2_k=t('От фурната', 'From the oven'), b2_v=t('Кроасан с бадеми · 3,60 €', 'Almond croissant · €3.60'),
        b3_k=t('Брънч', 'Brunch'), b3_v=t('Тост с авокадо и яйце · 9,40 €', 'Avocado and egg toast · €9.40'),
        b4_k=t('Сезонна напитка', 'Seasonal drink'), b4_v=t('Тиквено лате · 4,90 €', 'Pumpkin latte · €4.90'),
        k_order=t('Меню и поръчка', 'Menu and order'), order_h=t('Събери поръчката си и избери час', 'Build your order and pick a time'),
        order_p=t('Натисни „+“ до нещата, които искаш. Вдясно виждаш сметката и избираш кога да дойдеш. Плащаш на касата.',
                  'Tap “+” next to what you want. On the right you see the bill and choose when to come. You pay at the counter.'),
        cat_label=t('Категория', 'Category'), cats=cats, v=t('вегетарианско', 'vegetarian'), vg=t('веган', 'vegan'), menu_html=menu_html,
        tray_h=t('Твоята поръчка', 'Your order'), tray_empty=t('Още няма нищо тук. Добави нещо от менюто.', 'Nothing here yet. Add something from the menu.'),
        total_l=t('Общо', 'Total'), pick_h=t('Кога идваш?', 'When are you coming?'), pick_day=t('Ден', 'Day'), checking=t('Проверяваме свободните часове…', 'Checking free times…'),
        f_time=t('Час за вземане', 'Pick-up time'), f_name=t('Име', 'Name'), f_phone=t('Телефон', 'Phone'), f_msg=t('Бележка (по желание)', 'Note (optional)'),
        f_send=t('Изпрати поръчката', 'Send the order'),
        f_note=t('Плащаш при вземане. Само името и телефонът ни трябват.', 'You pay when you collect. We only need your name and phone.'),
        f_priv=t('Поверителност', 'Privacy'), privacy_href=privacy_href,
        k_bakery=t('Пекарна', 'Bakery'), bakery_h=t('Печем тук, всяка сутрин', 'Baked here, every morning'),
        bakery_p=t('Тестото се меси вечерта, а в 6:30 първите кроасани излизат от фурната. Когато нещо свърши, го маркираме на дъската.',
                   'The dough is made the evening before and the first croissants leave the oven at 6:30. When something sells out, we mark it on the board.'),
        bk1=t('Масло, а не маргарин', 'Butter, not margarine'), bk2=t('Хлябът е на квас', 'Sourdough bread'), bk3=t('Веган и безглутенови опции всеки ден', 'Vegan and gluten-free options daily'),
        bp1=I('croissants-paper', t('Кроасани върху хартия', 'Croissants on paper'), '(min-width: 900px) 580px, 92vw'),
        bp2=I('bakery-case', t('Витрина с кроасани', 'A display case with croissants'), '(min-width: 900px) 285px, 45vw'),
        bp3=I('beans-latte', t('Лате върху кафеени зърна', 'A latte on coffee beans'), '(min-width: 900px) 285px, 45vw'),
        k_card=t('Карта за лоялност', 'Loyalty card'), card_h=t('Деветото кафе е от нас', 'The ninth coffee is on us'),
        card_p=t('Всяко кафе дава печат. На десетия печат получаваш напитка по избор безплатно. Картата е хартиена, без приложение и без регистрация.',
                 'Every coffee earns a stamp. On the tenth stamp you get a drink of your choice free. The card is paper: no app, no sign-up.'),
        card_t=t('Примерна карта', 'Sample card'), stamps=stamps, card_f=t('Безплатна напитка', 'A free drink'),
        k_visit=t('Адрес', 'Visit'), visit_h=t('Заповядай при нас', 'Come and see us'), hours_html=hours_html,
        l_addr=t('Адрес', 'Address'), address=ADDRESS['bg' if bg else 'en'], l_phone=t('Телефон', 'Phone'), phone=PHONE, l_email=t('Имейл', 'Email'),
        g1=t('Работим с лаптоп', 'Laptop friendly'), g2=t('Приемаме кучета', 'Dogs welcome'), g3=t('Безжичен интернет', 'Free Wi-Fi'), g4=t('Достъпен вход', 'Step-free entrance'),
        ph_visit=I('hall-industrial', t('Кафенето отвътре с високи тавани и големи прозорци', 'Inside the café, with high ceilings and big windows'), '(min-width: 960px) 520px, 92vw'),
        map_t=t('Картата се зарежда от OpenStreetMap едва когато я поискаш.', 'The map loads from OpenStreetMap only when you ask for it.'), map_btn=t('Покажи картата', 'Show the map'),
        foot_demo=t('Всичко тук е пример.', 'Everything here is an example.'), admin_href='admin.html' if bg else '../admin.html?lang=en',
        admin_l=t('Демо админ панел', 'Demo back office'), bar_cta=t('Виж поръчката', 'View order'),
        dock_label=t('Цветова схема', 'Colour scheme'), skin_name=t('Лате', 'Latte'), swatches=swatches,
        data=json.dumps(data, ensure_ascii=False).replace('</', '<\\/'),
    )


def main():
    # config for the mock server
    cfg = ('/* Generated by tools/build_pages.py. Edit the values at the top of that file, then run it again. */\n'
           'window.MOKA_CONFIG = {\n  mode: "demo",            /* "demo" = requests are kept in this browser only; "live" = real API at apiBase (docs/API.md) */\n'
           '  apiBase: "/api",\n  hours: { weekday: ["%s", "%s"], weekend: ["%s", "%s"] },\n  capacity: %d,             /* orders that can be picked up at the same time */\n'
           '  slotMinutes: %d,\n  leadMinutes: %d,\n  latency: [600, 1100]      /* demo only: pretend network delay in milliseconds */\n};\n'
           % (HOURS['weekday'][0], HOURS['weekday'][1], HOURS['weekend'][0], HOURS['weekend'][1], CAPACITY, SLOT_MINUTES, LEAD_MINUTES))
    open(os.path.join(ROOT, 'js', 'config.js'), 'w', encoding='utf-8').write(cfg)
    for lang, path in (('bg', 'index.html'), ('en', os.path.join('en', 'index.html'))):
        os.makedirs(os.path.dirname(os.path.join(ROOT, path)), exist_ok=True)
        html = build(lang)
        open(os.path.join(ROOT, path), 'w', encoding='utf-8').write(html)
    # stylesheet = shared pieces + this design
    shared = open(os.path.join(ROOT, 'tools', 'shared.css'), encoding='utf-8').read()
    design = open(os.path.join(ROOT, 'tools', 'design.css'), encoding='utf-8').read()
    os.makedirs(os.path.join(ROOT, 'css'), exist_ok=True)
    open(os.path.join(ROOT, 'css', 'style.css'), 'w', encoding='utf-8').write(shared + '\n' + design)
    print('built')


if __name__ == '__main__':
    main()
