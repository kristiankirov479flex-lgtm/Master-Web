import os, re
from html import escape

SHOP = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ---- Edit these placeholders for each salon -------------------------------------------------
OPEN_WEEKDAY = '09:00-19:00'      # opening and closing time, Mon - Fri
OPEN_WEEKEND = '10:00-18:00'      # opening and closing time, Sat - Sun
PHONE_DISPLAY = '+359 000 000 000'
PHONE_HREF = '+359000000000'
EMAIL = 'email@example.com'
# Request system. 'demo' = the booking form talks to a mock server that keeps requests in the visitor's browser.
# 'live' = it sends real HTTP requests to API_BASE (see docs/API.md). Written to js/config.js.
MODE = 'demo'
API_BASE = '/api'
CAPACITY = 1                      # visits that can run at the same time (number of technicians)
SLOT_MINUTES = 15                 # gap between start times
LEAD_MINUTES = 60                 # a same-day request needs this much notice
BRAND = 'Atelier Nude'
# ---------------------------------------------------------------------------------------------

SKINS = [  # key, colours for the swatch (background, accent), names
    ('bone',  '#F3EEE7', '#1C1A18', 'Bone and Ink',      'Слонова кост и мастило'),
    ('blush', '#F7E9E6', '#8F3B4A', 'Blush and Rouge',   'Руж и пудра'),
    ('mocha', '#EFE6DA', '#7A4A2B', 'Mocha and Cream',   'Мока и сметана'),
    ('noir',  '#141313', '#D9B99B', 'Noir and Nude',     'Черно и нюд'),
    ('mint',  '#E8EFEA', '#2C5B48', 'Mint and Forest',   'Мента и гора'),
]
DEFAULT_SKIN = SKINS[0]

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
BYID = {i[0]: i for i in ITEMS}

# Looks: id, file, width, height, category, name EN, name BG, services (ids), alt EN, alt BG
LOOKS = [
    ('milk',     'hero-light-pink',     1600, 2553, 'natural', 'Milk Bath', 'Млечна баня', ['gel_mani'], 'Soft nude pink gel nails on a white fur surface', 'Нежни телесно-розови гел нокти върху бяла пухкава повърхност'),
    ('tortoise', 'black-tortoiseshell', 1600, 2400, 'bold',    'Tortoise Noir', 'Костенурка нуар', ['gel_art', 'art'], 'Black and tortoiseshell nails with a gold ring', 'Черни нокти с костенурков принт и златен пръстен'),
    ('tree',     'blue-white-tree',     1600, 1244, 'art',     'Winter Tree', 'Зимно дърво', ['gel_art', 'art'], 'Blue and white nails with a winter tree design', 'Сини и бели нокти със зимно дърво'),
    ('almond',   'pink-on-white',       1600, 2133, 'natural', 'Soft Almond', 'Нежен бадем', ['overlay'], 'Soft pink almond nails on white textile', 'Нежни розови бадемови нокти върху бял текстил'),
    ('gold',     'navy-gold-white',     1600, 2000, 'art',     'Midnight Gold', 'Полунощно злато', ['ext_med', 'art'], 'Navy, gold and white nail art on both hands', 'Нейл арт в тъмносиньо, златно и бяло на двете ръце'),
    ('metal',    'hand-with-flower',    1600, 2400, 'natural', 'Metallic Nude', 'Метален нюд', ['gel_mani'], 'Metallic nude nails held among orange flowers', 'Металикови нюд нокти сред оранжеви цветя'),
    ('black',    'black-silver-ring',   1600, 1067, 'bold',    'Gloss Black', 'Лъскаво черно', ['gel_mani'], 'Glossy black manicure with a silver ring', 'Лъскав черен маникюр със сребърен пръстен'),
    ('mauve',    'mauve-glitter',       1600, 1601, 'art',     'Mauve Glitter', 'Люляков брокат', ['ext_short', 'art'], 'Mauve, white and silver glitter nails on a knit sweater', 'Люляково-розови, бели и сребристи брокатени нокти'),
    ('love',     'pink-selective-focus',1600, 1067, 'art',     'Love Letters', 'Любовни писма', ['gel_art', 'art'], 'Pink and red nails with love lettering', 'Розови и червени нокти с надпис love'),
    ('rose',     'hand-on-pink',        1600, 2400, 'natural', 'Rose Pink', 'Розов тон', ['gel_mani'], 'Rose pink nails against a pink background', 'Розови нокти на розов фон'),
]


def hours_text(lang):
    wd, we = OPEN_WEEKDAY.replace('-', ' – '), OPEN_WEEKEND.replace('-', ' – ')
    return ('Mon – Fri %s · Sat – Sun %s' % (wd, we)) if lang == 'en' else ('Пон – Пет %s · Съб – Нед %s' % (wd, we))


def mins(m):
    return '%d min' % m if m < 60 else ('%d h' % (m // 60) if m % 60 == 0 else '%d h %d' % (m // 60, m % 60))


def mins_bg(m):
    return '%d мин' % m if m < 60 else ('%d ч' % (m // 60) if m % 60 == 0 else '%d ч %d мин' % (m // 60, m % 60))


L = {
 'en': dict(
  lang='en', root='../', script='latin', other_href='../index.html', other_lang='bg', other_label='БГ', other_aria='Превключи на български',
  privacy_href='privacy.html', home_href='index.html',
  title='Atelier Nude – nail studio in Plovdiv',
  desc='A nail studio in Plovdiv with a lookbook: pick a look you love, see the price and the time, and book a free slot. Gel polish, extensions and nail art.',
  skip='Skip to content', tagline='nail studio', nav_label='Main navigation', menu_btn='Menu',
  nav=[('#looks', 'Lookbook'), ('#menu', 'Menu'), ('#book', 'Book'), ('#visit', 'Visit')],
  cta='Book a look',
  issue='Plovdiv · Lookbook No. 1', h1='Nails, <em>tailored</em> to you.',
  lead='Browse the lookbook, pick the set you love and we book it for you: the right services, the right time, the price up front.',
  cta1='Browse the lookbook', cta2='See the menu', loading='Checking…',
  hero_alt='Soft nude pink gel nails on a white fur surface', cover_cap='Look 01 · Milk Bath',
  k_looks='The lookbook', looks_h='Pick a look. We do the rest.', looks_p='Every look comes with the services it needs. Press Book this look and your visit is ready, or open the photo for a closer view.',
  gal_filter='Filter looks', f_all='All', f_natural='Natural', f_art='Nail art', f_bold='Bold', shown='Looks shown: {n}', open_photo='Open photo', from_l='from', plus_art='plus art', book_look='Book this look',
  k_menu='The menu', menu_h='Prices, in plain sight.', menu_p='Add any service to your visit with the plus button. Each one shows its time and its price.',
  tab=dict(hands='Hands', ext='Extensions', feet='Feet', extras='Extras'), add='Add', added='Added', price_note='Sample prices in euro, based on salons in Plovdiv.',
  gift_h='Gift cards', gift_p='Give someone a manicure they will remember. Ask us for a gift card in any amount.', gift_btn='Ask about a gift card', gift_msg='I would like to ask about a gift card.',
  k_book='Book', book_h='Your visit, your time.', book_p='Check your visit, pick a day and a free time, and send the request. We reply to confirm.',
  sum_h='Your visit', look_label='Your look', sum_empty='Nothing yet.', need_link='Pick a look', sum_price='Price', sum_time='Time', sum_fine='Sample prices. We confirm the final price and time when we reply.',
  sum_from='from', sum_request='plus nail art, price on request', remove='Remove',
  s_day='Pick a day', s_time='Pick a time', s_you='Your details', day_prev='Earlier days', day_next='Later days', f_hint='Pick services and a day to see free times.',
  f_time='Time', f_name='Name', f_phone='Phone', f_msg='Message (optional)', f_send='Send the request', f_note='We use your details only to answer your request.', f_priv='Privacy notice',
  k_rev='Praise', rev_h='What clients say', rev_p='Short notes from people who book with us.',
  reviews=[('Perfect gel manicure. It lasted three weeks without a single chip.', 'Gel polish manicure'),
           ('I brought a photo and they made exactly that design.', 'Nail art'),
           ('A calm studio, everything spotless, and the price was clear before I booked.', 'Gel polish pedicure')],
  rev_by='Example client', rev_note='Example reviews. Replace them with real Google reviews.',
  k_visit='Visit', visit_h='Find the studio', addr_l='Address', addr='Primer St. 1, Plovdiv', hours_l='Hours', phone_l='Phone', email_l='Email',
  map_t='The map is from OpenStreetMap and loads only if you choose.', map_btn='Show the map',
  k_faq='Questions', faq_h='Good to know',
  faq=[('How long does a visit take?', 'A gel polish manicure takes about 1 to 1.5 hours, and extensions 2 to 3 hours. The menu shows the time for each service.'),
       ('Can I bring a photo of the design I want?', 'Yes. Pick any look in the lookbook, or bring or send your own photo, and we will tell you how close we can get.'),
       ('Is removing my old gel included?', 'Removal is a separate service and is on the menu. That way the old gel comes off safely, without harming your nails.'),
       ('What if I need to cancel or I am late?', 'Please tell us at least 24 hours ahead so we can offer your time to someone else. If you are more than 15 minutes late, the service may need to be shortened.'),
       ('Do I need to pay a deposit?', 'For extensions and longer visits we may ask for a small deposit, which is deducted from the price.')],
  foot_tag='Nail studio in Plovdiv', foot_priv='Privacy notice', admin_t='Demo back office', admin_href='../admin.html?lang=en', quick_label='Quick contact', q_call='Call', q_book='Book',
  dock_label='Colour scheme',
  lb_label='Photo', lb_close='Close', lb_prev='Previous photo', lb_next='Next photo', lb_request='Book this look',
 ),
 'bg': dict(
  lang='bg', root='', script='cyrillic', other_href='en/index.html', other_lang='en', other_label='EN', other_aria='Switch to English',
  privacy_href='privacy.html', home_href='index.html',
  title='Atelier Nude – студио за нокти в Пловдив',
  desc='Студио за нокти в Пловдив с лукбук: избери дизайн, който обичаш, виж цената и времето и запази свободен час. Гел лак, изграждане и нейл арт.',
  skip='Към съдържанието', tagline='студио за нокти', nav_label='Основна навигация', menu_btn='Меню',
  nav=[('#looks', 'Лукбук'), ('#menu', 'Меню'), ('#book', 'Час'), ('#visit', 'Адрес')],
  cta='Запази дизайн',
  issue='Пловдив · Лукбук № 1', h1='Нокти, <em>ушити по мярка</em> за теб.',
  lead='Разгледай лукбука, избери комплекта, който обичаш, и ние го запазваме: правилните услуги, правилното време и цената предварително.',
  cta1='Разгледай лукбука', cta2='Виж менюто', loading='Проверяваме…',
  hero_alt='Нежни телесно-розови гел нокти върху бяла пухкава повърхност', cover_cap='Дизайн 01 · Млечна баня',
  k_looks='Лукбукът', looks_h='Избери дизайн. Останалото е наша грижа.', looks_p='Всеки дизайн идва с услугите, които са му нужни. Натисни „Запази този дизайн“ и посещението ти е готово, или отвори снимката за по-близък поглед.',
  gal_filter='Филтър на дизайните', f_all='Всички', f_natural='Естествени', f_art='Нейл арт', f_bold='Смели', shown='Показани дизайни: {n}', open_photo='Отвори снимката', from_l='от', plus_art='плюс арт', book_look='Запази този дизайн',
  k_menu='Менюто', menu_h='Цените – на видно място.', menu_p='Добави всяка услуга към посещението си с бутона плюс. Всяка показва времето и цената си.',
  tab=dict(hands='Ръце', ext='Изграждане', feet='Крака', extras='Допълнения'), add='Добави', added='Добавено', price_note='Примерни цени в евро, по салони в Пловдив.',
  gift_h='Подаръчни карти', gift_p='Подари на някого маникюр, който ще помни. Поискай подаръчна карта на всякаква стойност.', gift_btn='Попитай за подаръчна карта', gift_msg='Искам да попитам за подаръчна карта.',
  k_book='Час', book_h='Твоето посещение, твоето време.', book_p='Провери посещението си, избери ден и свободен час и изпрати заявката. Ще ти отговорим, за да потвърдим.',
  sum_h='Твоето посещение', look_label='Твоят дизайн', sum_empty='Още нищо.', need_link='Избери дизайн', sum_price='Цена', sum_time='Време', sum_fine='Примерни цени. Крайната цена и времето се потвърждават, когато ти отговорим.',
  sum_from='от', sum_request='плюс нейл арт, цена по запитване', remove='Премахни',
  s_day='Избери ден', s_time='Избери час', s_you='Твоите данни', day_prev='По-ранни дни', day_next='По-късни дни', f_hint='Избери услуги и ден, за да видиш свободните часове.',
  f_time='Час', f_name='Име', f_phone='Телефон', f_msg='Съобщение (по желание)', f_send='Изпрати заявката', f_note='Ползваме данните ти само за да отговорим на заявката ти.', f_priv='Политика за поверителност',
  k_rev='Похвали', rev_h='Какво казват клиентите', rev_p='Кратки бележки от хора, които си запазват час при нас.',
  reviews=[('Идеален гел маникюр. Издържа три седмици без нито една цепнатина.', 'Маникюр с гел лак'),
           ('Занесох снимка и ми направиха точно такъв дизайн.', 'Нейл арт'),
           ('Спокойно студио, всичко беше чисто, а цената беше ясна още преди да си запазя час.', 'Педикюр с гел лак')],
  rev_by='Примерен клиент', rev_note='Примерни отзиви. Заменете ги с истински отзиви от Google.',
  k_visit='Посети ни', visit_h='Намери студиото', addr_l='Адрес', addr='ул. Примерна 1, Пловдив', hours_l='Работно време', phone_l='Телефон', email_l='Имейл',
  map_t='Картата е от OpenStreetMap и се зарежда само ако поискаш.', map_btn='Покажи картата',
  k_faq='Въпроси', faq_h='Добре е да знаеш',
  faq=[('Колко време отнема посещението?', 'Маникюр с гел лак отнема около 1 до 1,5 часа, а изграждане на нокти – 2 до 3 часа. В менюто е посочено времето за всяка услуга.'),
       ('Мога ли да донеса снимка на дизайна, който искам?', 'Да. Избери който и да е дизайн от лукбука, или донеси или изпрати своя снимка, и ще ти кажем доколко можем да я пресъздадем.'),
       ('Свалянето на стар гел включено ли е?', 'Свалянето е отделна услуга и е в менюто. Така старият гел се маха безопасно, без да се вреди на ноктите.'),
       ('Какво става, ако трябва да отменя или закъснея?', 'Предупреди ни поне 24 часа предварително, за да предложим часа на друг клиент. При закъснение над 15 минути може да се наложи услугата да бъде съкратена.'),
       ('Нужен ли е депозит?', 'За изграждане на нокти и по-дълги посещения можем да поискаме малък депозит, който се приспада от цената.')],
  foot_tag='Студио за нокти в Пловдив', foot_priv='Политика за поверителност', admin_t='Демо админ панел', admin_href='admin.html', quick_label='Бърза връзка', q_call='Обади се', q_book='Запази',
  dock_label='Цветова схема',
  lb_label='Снимка', lb_close='Затвори', lb_prev='Предишна снимка', lb_next='Следваща снимка', lb_request='Запази този дизайн',
 ),
}

TEMPLATE = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'page_template.html'), encoding='utf-8').read()


def build(lang):
    d = L[lang]
    e = lambda s: escape(s, quote=True)
    root = d['root']
    bg = lang == 'bg'
    fm = mins_bg if bg else mins
    out = {'lang': lang, 'root': root, 'script': d['script']}
    keys = ['title', 'desc', 'skip', 'nav_label', 'menu_btn', 'cta', 'issue', 'lead', 'cta1', 'cta2', 'loading', 'hero_alt', 'cover_cap',
            'k_looks', 'looks_h', 'looks_p', 'gal_filter', 'f_all', 'f_natural', 'f_art', 'f_bold', 'k_menu', 'menu_h', 'menu_p', 'price_note',
            'gift_h', 'gift_p', 'gift_btn', 'k_book', 'book_h', 'book_p', 'sum_h', 'look_label', 'sum_empty', 'need_link', 'sum_price', 'sum_time', 'sum_fine',
            's_day', 's_time', 's_you', 'day_prev', 'day_next', 'f_hint', 'f_time', 'f_name', 'f_phone', 'f_msg', 'f_send', 'f_note', 'f_priv',
            'k_rev', 'rev_h', 'rev_note', 'k_visit', 'visit_h', 'addr_l', 'addr', 'hours_l', 'phone_l', 'email_l', 'map_t', 'map_btn', 'k_faq', 'faq_h',
            'foot_tag', 'foot_priv', 'admin_t', 'quick_label', 'q_call', 'q_book', 'dock_label', 'lb_label', 'lb_close', 'lb_prev', 'lb_next', 'lb_request']
    for k in keys:
        out[k] = e(d[k])
    out['h1'] = d['h1']   # contains <em>
    out['other_href'] = d['other_href']; out['other_lang'] = d['other_lang']; out['other_label'] = d['other_label']; out['other_aria'] = e(d['other_aria'])
    out['privacy_href'] = d['privacy_href']; out['home_href'] = d['home_href']; out['admin_href'] = d['admin_href']
    out['nav_links'] = '\n      '.join('<a href="%s">%s</a>' % (h, e(t)) for h, t in d['nav'])

    def name(iid):
        it = BYID[iid]
        return it[3] if bg else it[2]

    # lookbook cards
    cards = []
    for lid, photo, w, h, cat, n_en, n_bg, svcs, alt_en, alt_bg in LOOKS:
        alt = e(alt_bg if bg else alt_en)
        price = sum(BYID[s][7] for s in svcs)
        minutes = sum(BYID[s][6][1] for s in svcs)
        art = any(BYID[s][9] == 'request' for s in svcs)
        pt = '%s %d €' % (d['from_l'], price) + (' · ' + d['plus_art'] if art else '')
        cards.append(
            '<article class="look" data-cat="%s">'
            '<button class="look-img" type="button" data-full="%simages/stock/%s.jpg" aria-label="%s: %s">'
            '<img src="%simages/stock/%s-800.jpg" width="800" height="%d" alt="%s" loading="lazy" decoding="async"></button>'
            '<div class="look-body"><h3>%s</h3><p class="look-svc">%s</p><p class="look-meta"><b>%s</b> · %s</p>'
            '<button class="btn btn-main btn-sm" type="button" data-look="%s" data-svcs="%s" data-name="%s">%s</button></div></article>'
            % (cat, root, photo, e(d['open_photo']), alt, root, photo, round(800 * h / w), alt, e(n_bg if bg else n_en),
               e(' + '.join(name(s) for s in svcs)), e(pt), e(fm(minutes)), lid, ','.join(svcs), e(n_bg if bg else n_en), e(d['book_look'])))
    out['looks'] = '\n        '.join(cards)

    # menu: one column per group, dotted leaders and an add button
    cols = []
    for g in GROUPS:
        rows = []
        for iid, ig, en, bgn, ten, tbg, (m0, m1), p0, p1, kind, pten, ptbg in ITEMS:
            if ig != g:
                continue
            nm = bgn if bg else en
            rows.append('<li><span class="mn-name">%s<small>%s</small></span><i class="dots" aria-hidden="true"></i><b class="mn-price">%s</b>'
                        '<button class="mn-add" type="button" aria-pressed="false" data-svc="%s" data-name="%s" data-min="%d" data-p0="%d" data-p1="%d" data-kind="%s" data-add="%s" data-added="%s" aria-label="%s: %s">'
                        '<span aria-hidden="true">+</span></button></li>'
                        % (e(nm), e(tbg if bg else ten), e(ptbg if bg else pten), iid, e(nm), m1, p0, p1, kind, e(d['add']), e(d['added']), e(d['add']), e(nm)))
        cols.append('<section class="mn-col"><h3>%s</h3><ul>%s</ul></section>' % (e(d['tab'][g]), ''.join(rows)))
    out['menu'] = '\n        '.join(cols)

    out['reviews'] = '\n        '.join('<figure class="quote"><blockquote>%s</blockquote><figcaption><b>%s</b> · %s</figcaption></figure>' % (e(q), e(s), e(d['rev_by'])) for q, s in d['reviews'])
    out['faq'] = '\n          '.join('<details><summary>%s</summary><p>%s</p></details>' % (e(q), e(a)) for q, a in d['faq'])

    out['hours'] = e(hours_text(lang))
    out['phone'] = PHONE_DISPLAY; out['phone_href'] = PHONE_HREF; out['email'] = EMAIL; out['brand'] = e(BRAND); out['brand_json'] = BRAND
    sw = []
    for key, c1, c2, n_en, n_bg in SKINS:
        nm = n_bg if bg else n_en
        sw.append('<button class="sw" type="button" data-skin="%s" data-name="%s" aria-label="%s: %s" title="%s" aria-pressed="%s" style="--s1:%s;--s2:%s"></button>'
                  % (key, e(nm), e(d['dock_label']), e(nm), e(nm), 'true' if key == DEFAULT_SKIN[0] else 'false', c1, c2))
    out['swatches'] = '\n        '.join(sw)
    out['skin_name'] = e(DEFAULT_SKIN[4] if bg else DEFAULT_SKIN[3])
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
    'window.ATELIER_CONFIG = {\n'
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
