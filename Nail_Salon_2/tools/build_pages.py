import os, re
from html import escape

SHOP = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ---- Edit these placeholders for each salon -------------------------------------------------
OPEN_WEEKDAY = '09:00-19:00'      # opening and closing time, Mon - Fri
OPEN_WEEKEND = '10:00-18:00'      # opening and closing time, Sat - Sun
PHONE_DISPLAY = '+359 000 000 000'
PHONE_HREF = '+359000000000'
EMAIL = 'email@example.com'
# Request system. 'demo' = the form talks to a mock server that keeps requests in the visitor's browser.
# 'live' = it sends real HTTP requests to API_BASE (see docs/API.md). Written to js/config.js.
MODE = 'demo'
API_BASE = '/api'
CAPACITY = 1                      # visits that can run at the same time (number of technicians)
SLOT_MINUTES = 15                 # gap between start times
LEAD_MINUTES = 60                 # a same-day request needs this much notice
BRAND = 'Lumi'
# ---------------------------------------------------------------------------------------------

SKINS = [  # key, colours for the swatch, names
    ('rose',     '#F4F2EE', '#96445A', 'Cloud & Rosewater',     'Облак и роза'),
    ('sage',     '#F3F4EF', '#3E5F4F', 'Sage & Stone',          'Шалфей и камък'),
    ('espresso', '#F8F2EA', '#6B3F2B', 'Espresso & Cream',      'Еспресо и сметана'),
    ('oxblood',  '#FBF4F2', '#7B1E2E', 'Oxblood & Blush',       'Бордо и руж'),
    ('midnight', '#F7F4EE', '#14213D', 'Midnight & Champagne',  'Полунощ и шампанско'),
]

# file, cat, width, height, alt_en, alt_bg
GALLERY = [
    ('hero-light-pink',     'natural', 1600, 2553, 'Soft nude pink gel nails on a white fur surface', 'Нежни телесно-розови гел нокти върху бяла пухкава повърхност'),
    ('black-tortoiseshell', 'bold',    1600, 2400, 'Black and tortoiseshell nails with a gold ring', 'Черни нокти с костенурков принт и златен пръстен'),
    ('blue-white-tree',     'art',     1600, 1244, 'Blue and white nails with a winter tree design', 'Сини и бели нокти със зимно дърво'),
    ('pink-on-white',       'natural', 1600, 2133, 'Soft pink almond nails on white textile', 'Нежни розови бадемови нокти върху бял текстил'),
    ('navy-gold-white',     'art',     1600, 2000, 'Navy, gold and white nail art on both hands', 'Нейл арт в тъмносиньо, златно и бяло на двете ръце'),
    ('hand-with-flower',    'natural', 1600, 2400, 'Metallic nude nails held among orange flowers', 'Металикови нюд нокти сред оранжеви цветя'),
    ('black-silver-ring',   'bold',    1600, 1067, 'Glossy black manicure with a silver ring', 'Лъскав черен маникюр със сребърен пръстен'),
    ('mauve-glitter',       'art',     1600, 1601, 'Mauve, white and silver glitter nails on a knit sweater', 'Люляково-розови, бели и сребристи брокатени нокти'),
    ('pink-selective-focus','art',     1600, 1067, 'Pink and red nails with love lettering', 'Розови и червени нокти с надпис love'),
    ('hand-on-pink',        'natural', 1600, 2400, 'Rose pink nails against a pink background', 'Розови нокти на розов фон'),
]

# Services: id, group, name EN, name BG, time EN, time BG, (min minutes, max minutes), price min, price max, kind, price text EN, price text BG
#   kind: fixed | from (price is a minimum) | per (per nail) | request (price on request)
ITEMS = [
    ('mani',      'hands', 'Classic manicure, no polish', 'Класически маникюр, без лак', '45 min', '45 мин', (45, 45), 12, 12, 'fixed', '12 €', '12 €'),
    ('gel_mani',  'hands', 'Gel polish manicure', 'Маникюр с гел лак', '1 h – 1 h 30', '1 ч – 1 ч 30 мин', (60, 90), 25, 25, 'fixed', '25 €', '25 €'),
    ('gel_art',   'hands', 'Gel manicure with French tips or nail art', 'Гел лак с френски връхчета или нейл арт', '1 h 30', '1 ч 30 мин', (90, 90), 28, 28, 'fixed', '28 €', '28 €'),
    ('overlay',   'hands', 'Gel overlay on natural nails', 'Гел върху естествени нокти', '2 h', '2 ч', (120, 120), 30, 30, 'fixed', '30 €', '30 €'),
    ('removal',   'hands', 'Gel polish removal', 'Сваляне на гел лак', '20 – 30 min', '20 – 30 мин', (20, 30), 10, 10, 'fixed', '10 €', '10 €'),
    ('repair',    'hands', 'Broken nail repair', 'Ремонт на счупен нокът', '', '', (10, 10), 2, 2, 'per', '2 € per nail', '2 € на нокът'),
    ('ext_short', 'ext', 'Gel extensions, short', 'Изграждане с гел, къси нокти', '1 h 30', '1 ч 30 мин', (90, 90), 40, 40, 'fixed', '40 €', '40 €'),
    ('ext_med',   'ext', 'Gel extensions, medium', 'Изграждане с гел, средни нокти', '1 h 45', '1 ч 45 мин', (105, 105), 45, 45, 'fixed', '45 €', '45 €'),
    ('ext_long',  'ext', 'Gel extensions, long', 'Изграждане с гел, дълги нокти', '2 h', '2 ч', (120, 120), 50, 50, 'fixed', '50 €', '50 €'),
    ('refill',    'ext', 'Refill', 'Корекция', '1 h 30 – 2 h', '1 ч 30 мин – 2 ч', (90, 120), 30, 30, 'from', 'from 30 €', 'от 30 €'),
    ('pedi',      'feet', 'Classic pedicure, no polish', 'Класически педикюр, без лак', '45 min', '45 мин', (45, 45), 20, 20, 'fixed', '20 €', '20 €'),
    ('gel_pedi',  'feet', 'Gel polish pedicure', 'Педикюр с гел лак', '1 h – 1 h 30', '1 ч – 1 ч 30 мин', (60, 90), 25, 30, 'fixed', '25 – 30 €', '25 – 30 €'),
    ('spa_pedi',  'feet', 'SPA pedicure with gel polish', 'СПА педикюр с гел лак', '2 h', '2 ч', (120, 120), 30, 30, 'fixed', '30 €', '30 €'),
    ('art',       'extras', 'Nail art, French tips, chrome', 'Нейл арт, френски връхчета, хром', '30 – 60 min', '30 – 60 мин', (30, 60), 0, 0, 'request', 'on request', 'по запитване'),
]
GROUPS = ['hands', 'ext', 'feet', 'extras']


def hours_text(lang):
    wd, we = OPEN_WEEKDAY.replace('-', ' – '), OPEN_WEEKEND.replace('-', ' – ')
    return ('Mon – Fri %s · Sat – Sun %s' % (wd, we)) if lang == 'en' else ('Пон – Пет %s · Съб – Нед %s' % (wd, we))


L = {
 'en': dict(
  lang='en', root='../', script='latin', other_href='../index.html', other_lang='bg', other_label='БГ', other_aria='Превключи на български',
  privacy_href='privacy.html', home_href='index.html',
  title='Lumi – nail studio in Plovdiv',
  desc='Gel polish, nail extensions and nail art in a bright studio in Plovdiv. Build your visit, see the total and the time, and send a request.',
  skip='Skip to content', tagline='nail studio', nav_label='Main navigation', menu_btn='Menu',
  nav=[('#services', 'Services'), ('#gallery', 'Gallery'), ('#reviews', 'Reviews'), ('#faq', 'Questions')],
  cta='Book a time',
  hero_label='Nail studio · Plovdiv', h1='Nails that feel like you.',
  lead='Gel polish, extensions and nail art. Build your visit, see the price and time, and pick a free slot.',
  hero_cta1='Build your visit', hero_cta2='Book a time', hero_chip='Gel · Extensions · Nail art',
  hero_alt='Soft nude pink gel nails on a white fur surface', tile2_alt='Navy, gold and white nail art on both hands', tile2_label='Nail art',
  next_h='Next free time', next_btn='Book it', open_h='Today', loading='Checking…',
  marquee=['Gel polish', 'Extensions', 'Nail art', 'French tips', 'Pedicure', 'Chrome'],
  k_services='Services', svc_h='Build your visit', svc_p='Tick everything you want today. We add up the price and the time, so you know before you book.',
  tab=dict(hands='Hands', ext='Extensions', feet='Feet', extras='Extras'),
  price_note='Sample prices in euro, based on salons in Plovdiv.',
  sum_h='Your visit', sum_empty='Nothing yet. Pick a service on the left.', sum_price='Price', sum_time='Time', sum_book='Book this visit',
  sum_fine='Sample prices. We confirm the final price and time when we reply.', sum_from='from', sum_request='plus nail art, price on request', remove='Remove',
  k_gallery='Gallery', gal_h='Recent work', gal_p='A few sets we are proud of. Filter by style and press a photo to request that look.', gal_filter='Filter photos',
  f_all='All', f_natural='Natural', f_art='Nail art', f_bold='Bold', shown='Photos shown: {n}', open_photo='Open photo', gal_cta='Request this look',
  lb_label='Photo', lb_close='Close', lb_prev='Previous photo', lb_next='Next photo', lb_request='Request this look',
  k_rev='Reviews', rev_h='What clients say', rev_p='Short notes from people who book with us.',
  reviews=[('Perfect gel manicure. It lasted three weeks without a single chip.', 'Gel polish manicure'),
           ('I brought a photo and they made exactly that design.', 'Nail art'),
           ('A calm studio, everything spotless, and the price was clear before I booked.', 'Gel polish pedicure'),
           ('Gentle with my weak nails, and the shape is perfect.', 'Gel overlay'),
           ('Quick, calm and exactly what I asked for.', 'Classic manicure')],
  rev_by='Example client', rev_note='Example reviews. Replace them with real Google reviews.',
  k_faq='Questions', faq_h='Good to know',
  faq=[('How long does a visit take?', 'A gel polish manicure takes about 1 to 1.5 hours, and extensions 2 to 3 hours. The list shows the time for each service.'),
       ('Can I bring a photo of the design I want?', 'Yes. Press any photo in the gallery to request that look, or bring or send your own photo, and we will tell you how close we can get.'),
       ('Is removing my old gel included?', 'Removal is a separate service and is on the list. That way the old gel comes off safely, without harming your nails.'),
       ('What if I need to cancel or I am late?', 'Please tell us at least 24 hours ahead so we can offer your time to someone else. If you are more than 15 minutes late, the service may need to be shortened.'),
       ('Do I need to pay a deposit?', 'For extensions and longer visits we may ask for a small deposit, which is deducted from the price.')],
  k_book='Book', book_h='Pick a time that suits you.', book_p='Choose a free time below, or pick a date yourself. We will reply to confirm.',
  quick_h='Next free times', form_h='Send a request', need_pick='No services chosen yet.', need_link='Choose services', chip_plan='Your visit', chip_look='Look you like', chip_remove='Remove',
  f_name='Name', f_phone='Phone', f_date='Preferred date', f_time='Preferred time', f_time_pick='Choose a time', f_hint='Weekday times are shown. Pick a date to see the times for that day.', f_msg='Message (optional)',
  f_send='Send request', f_note='We use your details only to answer your request.', f_priv='Privacy notice',
  k_visit='Visit', visit_h='Find the studio', addr_l='Address', addr='Primer St. 1, Plovdiv', contact_l='Contact', hours_l='Hours', phone_l='Phone', email_l='Email',
  map_t='The map is from OpenStreetMap and loads only if you choose.', map_btn='Show the map',
  foot_priv='Privacy notice', admin_t='Demo back office', admin_href='../admin.html?lang=en', quick_label='Quick contact', q_call='Call', q_book='Book a time',
  dock_label='Colour scheme',
 ),
 'bg': dict(
  lang='bg', root='', script='cyrillic', other_href='en/index.html', other_lang='en', other_label='EN', other_aria='Switch to English',
  privacy_href='privacy.html', home_href='index.html',
  title='Lumi – студио за нокти в Пловдив',
  desc='Гел лак, изграждане на нокти и нейл арт в светло студио в Пловдив. Събери посещението си, виж цената и времето и изпрати заявка.',
  skip='Към съдържанието', tagline='студио за нокти', nav_label='Основна навигация', menu_btn='Меню',
  nav=[('#services', 'Услуги'), ('#gallery', 'Галерия'), ('#reviews', 'Отзиви'), ('#faq', 'Въпроси')],
  cta='Запази час',
  hero_label='Студио за нокти · Пловдив', h1='Нокти, които ти приличат.',
  lead='Гел лак, изграждане и нейл арт. Събери посещението си, виж цената и времето и избери свободен час.',
  hero_cta1='Събери посещението', hero_cta2='Запази час', hero_chip='Гел лак · Изграждане · Нейл арт',
  hero_alt='Нежни телесно-розови гел нокти върху бяла пухкава повърхност', tile2_alt='Нейл арт в тъмносиньо, златно и бяло на двете ръце', tile2_label='Нейл арт',
  next_h='Следващ свободен час', next_btn='Запази го', open_h='Днес', loading='Проверяваме…',
  marquee=['Гел лак', 'Изграждане', 'Нейл арт', 'Френски връхчета', 'Педикюр', 'Хром'],
  k_services='Услуги', svc_h='Събери посещението си', svc_p='Отбележи всичко, което искаш днес. Ще съберем цената и времето, за да знаеш преди да запазиш.',
  tab=dict(hands='Ръце', ext='Изграждане', feet='Крака', extras='Допълнения'),
  price_note='Примерни цени в евро, по салони в Пловдив.',
  sum_h='Твоето посещение', sum_empty='Още нищо. Избери услуга отляво.', sum_price='Цена', sum_time='Време', sum_book='Запази това посещение',
  sum_fine='Примерни цени. Крайната цена и времето се потвърждават, когато ти отговорим.', sum_from='от', sum_request='плюс нейл арт, цена по запитване', remove='Премахни',
  k_gallery='Галерия', gal_h='Последни работи', gal_p='Няколко комплекта, с които се гордеем. Филтрирай по стил и натисни снимка, за да заявиш този стил.', gal_filter='Филтър на снимките',
  f_all='Всички', f_natural='Естествени', f_art='Нейл арт', f_bold='Смели', shown='Показани снимки: {n}', open_photo='Отвори снимката', gal_cta='Заяви този стил',
  lb_label='Снимка', lb_close='Затвори', lb_prev='Предишна снимка', lb_next='Следваща снимка', lb_request='Заяви този стил',
  k_rev='Отзиви', rev_h='Какво казват клиентите', rev_p='Кратки бележки от хора, които си запазват час при нас.',
  reviews=[('Идеален гел маникюр. Издържа три седмици без нито една цепнатина.', 'Маникюр с гел лак'),
           ('Занесох снимка и ми направиха точно такъв дизайн.', 'Нейл арт'),
           ('Спокойно студио, всичко беше чисто, а цената беше ясна още преди да си запазя час.', 'Педикюр с гел лак'),
           ('Внимателни със слабите ми нокти, а формата е перфектна.', 'Гел върху естествени нокти'),
           ('Бързо, спокойно и точно каквото поисках.', 'Класически маникюр')],
  rev_by='Примерен клиент', rev_note='Примерни отзиви. Заменете ги с истински отзиви от Google.',
  k_faq='Въпроси', faq_h='Добре е да знаеш',
  faq=[('Колко време отнема посещението?', 'Маникюр с гел лак отнема около 1 до 1,5 часа, а изграждане на нокти – 2 до 3 часа. В списъка е посочено времето за всяка услуга.'),
       ('Мога ли да донеса снимка на дизайна, който искам?', 'Да. Натисни коя да е снимка в галерията, за да заявиш този стил, или донеси или изпрати своя снимка, и ще ти кажем доколко можем да я пресъздадем.'),
       ('Свалянето на стар гел включено ли е?', 'Свалянето е отделна услуга и е в списъка. Така старият гел се маха безопасно, без да се вреди на ноктите.'),
       ('Какво става, ако трябва да отменя или закъснея?', 'Предупреди ни поне 24 часа предварително, за да предложим часа на друг клиент. При закъснение над 15 минути може да се наложи услугата да бъде съкратена.'),
       ('Нужен ли е депозит?', 'За изграждане на нокти и по-дълги посещения можем да поискаме малък депозит, който се приспада от цената.')],
  k_book='Запази', book_h='Избери час, който ти подхожда.', book_p='Избери свободен час отдолу или избери дата сама. Ще ти отговорим, за да потвърдим.',
  quick_h='Следващи свободни часове', form_h='Изпрати заявка', need_pick='Още няма избрани услуги.', need_link='Избери услуги', chip_plan='Твоето посещение', chip_look='Стил, който ти харесва', chip_remove='Премахни',
  f_name='Име', f_phone='Телефон', f_date='Удобна дата', f_time='Удобен час', f_time_pick='Избери час', f_hint='Показани са часовете за делнични дни. Избери дата, за да видиш часовете за конкретния ден.', f_msg='Съобщение (по желание)',
  f_send='Изпрати заявката', f_note='Ползваме данните ти само за да отговорим на заявката ти.', f_priv='Политика за поверителност',
  k_visit='Посети ни', visit_h='Намери студиото', addr_l='Адрес', addr='ул. Примерна 1, Пловдив', contact_l='Контакти', hours_l='Работно време', phone_l='Телефон', email_l='Имейл',
  map_t='Картата е от OpenStreetMap и се зарежда само ако поискаш.', map_btn='Покажи картата',
  foot_priv='Политика за поверителност', admin_t='Демо админ панел', admin_href='admin.html', quick_label='Бърза връзка', q_call='Обади се', q_book='Запази час',
  dock_label='Цветова схема',
 ),
}

TEMPLATE = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'page_template.html'), encoding='utf-8').read()


def build(lang):
    d = L[lang]
    e = lambda s: escape(s, quote=True)
    root = d['root']
    bg = lang == 'bg'
    out = {'lang': lang, 'root': root, 'script': d['script']}
    keys = ['title', 'desc', 'skip', 'tagline', 'nav_label', 'menu_btn', 'cta', 'hero_label', 'h1', 'lead', 'hero_cta1', 'hero_cta2', 'hero_chip', 'hero_alt', 'tile2_alt', 'tile2_label',
            'next_h', 'next_btn', 'open_h', 'loading', 'k_services', 'svc_h', 'svc_p', 'price_note', 'sum_h', 'sum_empty', 'sum_price', 'sum_time', 'sum_book', 'sum_fine',
            'k_gallery', 'gal_h', 'gal_p', 'gal_filter', 'f_all', 'f_natural', 'f_art', 'f_bold', 'shown', 'lb_label', 'lb_close', 'lb_prev', 'lb_next', 'lb_request',
            'k_rev', 'rev_h', 'rev_p', 'rev_note', 'k_faq', 'faq_h', 'k_book', 'book_h', 'book_p', 'quick_h', 'form_h', 'need_pick', 'need_link', 'chip_plan', 'chip_look', 'chip_remove',
            'f_name', 'f_phone', 'f_date', 'f_time', 'f_time_pick', 'f_hint', 'f_msg', 'f_send', 'f_note', 'f_priv',
            'k_visit', 'visit_h', 'addr_l', 'addr', 'contact_l', 'hours_l', 'phone_l', 'email_l', 'map_t', 'map_btn', 'foot_priv', 'admin_t', 'quick_label', 'q_call', 'q_book', 'dock_label']
    for k in keys:
        out[k] = e(d[k])
    out['other_href'] = d['other_href']; out['other_lang'] = d['other_lang']; out['other_label'] = d['other_label']; out['other_aria'] = e(d['other_aria'])
    out['privacy_href'] = d['privacy_href']; out['home_href'] = d['home_href']; out['admin_href'] = d['admin_href']
    out['nav_links'] = '\n      '.join('<a href="%s">%s</a>' % (h, e(t)) for h, t in d['nav'])
    out['marquee'] = '<li>' + '</li><li>'.join(e(w) for w in d['marquee']) + '</li>'

    # services: tabs + panels of tick-able rows
    tabs, panels = [], []
    for n, g in enumerate(GROUPS):
        tabs.append('<button class="tab" type="button" role="tab" id="tab-%s" aria-controls="panel-%s" aria-selected="%s" tabindex="%s">%s<span class="count" hidden></span></button>'
                    % (g, g, 'true' if n == 0 else 'false', '0' if n == 0 else '-1', e(d['tab'][g])))
        rows = []
        for iid, ig, en, bgn, ten, tbg, (m0, m1), p0, p1, kind, pten, ptbg in ITEMS:
            if ig != g:
                continue
            nm = bgn if bg else en
            small = tbg if bg else ten
            rows.append('<label class="item"><input type="checkbox" name="svc" value="%s" data-name="%s" data-min="%d" data-max="%d" data-pmin="%d" data-pmax="%d" data-kind="%s">'
                        '<span><b>%s</b>%s</span><span class="item-price">%s</span><span class="item-add" aria-hidden="true"></span></label>'
                        % (iid, e(nm), m0, m1, p0, p1, kind, e(nm), '<small>%s</small>' % e(small) if small else '', e(ptbg if bg else pten)))
        panels.append('<div class="items" role="tabpanel" id="panel-%s" aria-labelledby="tab-%s"%s>\n            %s\n          </div>'
                      % (g, g, '' if n == 0 else ' hidden', '\n            '.join(rows)))
    out['tabs'] = '\n            '.join(tabs)
    out['panels'] = '\n          '.join(panels)

    items = []
    for name, cat, w, h, alt_en, alt_bg in GALLERY:
        alt = e(alt_bg if bg else alt_en)
        items.append('<button class="gal-item" type="button" data-cat="%s" data-full="%simages/stock/%s.jpg" aria-label="%s: %s">'
                     '<img src="%simages/stock/%s-800.jpg" width="800" height="%d" alt="%s" loading="lazy" decoding="async"><span aria-hidden="true">%s</span></button>'
                     % (cat, root, name, e(d['open_photo']), alt, root, name, round(800 * h / w), alt, e(d['gal_cta'])))
    out['gallery'] = '\n        '.join(items)

    revs = ['<figure class="rev"><span class="stars" aria-hidden="true">★★★★★</span><blockquote>%s</blockquote><figcaption><b>%s</b> · %s</figcaption></figure>' % (e(q), e(s), e(d['rev_by'])) for q, s in d['reviews']]
    out['reviews'] = '\n          '.join(revs)
    # the copy that makes the loop seamless is hidden from screen readers
    out['reviews_dup'] = '\n          '.join(r.replace('<figure class="rev">', '<figure class="rev" aria-hidden="true">') for r in revs)
    out['faq'] = '\n        '.join('<details><summary>%s</summary><p>%s</p></details>' % (e(q), e(a)) for q, a in d['faq'])
    out['hours'] = e(hours_text(lang))
    out['phone'] = PHONE_DISPLAY; out['phone_href'] = PHONE_HREF; out['email'] = EMAIL; out['brand'] = BRAND
    sw = []
    for key, c1, c2, n_en, n_bg in SKINS:
        name = n_bg if bg else n_en
        sw.append('<button class="sw" type="button" data-skin="%s" data-name="%s" aria-label="%s: %s" title="%s" aria-pressed="%s" style="--s1:%s;--s2:%s"></button>'
                  % (key, e(name), e(d['dock_label']), e(name), e(name), 'true' if key == 'rose' else 'false', c1, c2))
    out['swatches'] = '\n        '.join(sw)
    out['skin_name'] = e(SKINS[0][4] if bg else SKINS[0][3])
    out['hours_ld'] = '"Mo-Fr %s", "Sa-Su %s"' % (OPEN_WEEKDAY, OPEN_WEEKEND)
    out['year'] = '2026'
    html = TEMPLATE
    for k, v in out.items():
        html = html.replace('[[%s]]' % k, v)
    left = re.findall(r'\[\[(\w+)\]\]', html)
    assert not left, left
    return html


for lang in ('bg', 'en'):
    html = build(lang)
    path = os.path.join(SHOP, 'index.html') if lang == 'bg' else os.path.join(SHOP, 'en', 'index.html')
    os.makedirs(os.path.dirname(path), exist_ok=True)
    open(path, 'w', encoding='utf-8').write(html)
    print(lang, len(html), 'bytes ->', path)

# ---- js/config.js: the settings the page and the mock server read -------------------------------
cfg = (
    '/* Generated by tools/build_pages.py. Edit the values at the top of that file, then run it again. */\n'
    'window.LUMI_CONFIG = {\n'
    '  mode: "%s",            /* "demo" = requests are kept in this browser only; "live" = real API at apiBase (docs/API.md) */\n'
    '  apiBase: "%s",\n'
    '  hours: { weekday: ["%s", "%s"], weekend: ["%s", "%s"] },\n'
    '  capacity: %d,             /* visits that can run at the same time */\n'
    '  slotMinutes: %d,\n'
    '  leadMinutes: %d,         /* same-day requests need this much notice */\n'
    '  latency: [600, 1100]      /* demo only: pretend network delay in milliseconds */\n'
    '};\n'
) % (MODE, API_BASE, OPEN_WEEKDAY.split('-')[0], OPEN_WEEKDAY.split('-')[1], OPEN_WEEKEND.split('-')[0], OPEN_WEEKEND.split('-')[1], CAPACITY, SLOT_MINUTES, LEAD_MINUTES)
os.makedirs(os.path.join(SHOP, 'js'), exist_ok=True)
open(os.path.join(SHOP, 'js', 'config.js'), 'w', encoding='utf-8').write(cfg)
print('config.js written')
