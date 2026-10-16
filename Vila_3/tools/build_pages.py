import os, re
from html import escape

SHOP = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ---- Edit these placeholders for each guest house --------------------------------------------
BRAND_EN = 'The Stone Cellar'
BRAND_BG = 'Каменната изба'
PHONE_DISPLAY = '+359 000 000 000'
PHONE_HREF = '+359000000000'
EMAIL = 'email@example.com'
CHECKIN = '15:00'
CHECKOUT = '11:00'
# Enquiry system. 'demo' = the booking form talks to a mock server that keeps enquiries in the visitor's browser.
# 'live' = it sends real HTTP requests to API_BASE (see docs/API.md). Written to js/config.js.
MODE = 'demo'
API_BASE = '/api'
MAX_NIGHTS = 30
# ---------------------------------------------------------------------------------------------

# Units to sleep in (all names, sizes and prices are examples):
# id, name EN, name BG, m2, guests, bed EN, bed BG, price per night (EUR), photo, width, height
UNITS = [
    ('stone',   'The Stone Room',       'Каменната стая',        24, 2, '1 double bed', '1 двойно легло', 70, 'bedroom-stone-wall', 1600, 2400),
    ('cellar',  'The Cellar Room',      'Стаята в избата',       20, 2, '1 double bed', '1 двойно легло', 60, 'wood-headboard', 1600, 2175),
    ('hearth',  'The Hearth Suite',     'Сюит „Камината“',       42, 4, '1 king bed and a sofa bed', '1 голямо легло и разтегателен диван', 120, 'bedroom-fireplace', 1600, 1067),
    ('cottage', 'The Vineyard Cottage', 'Къщичката сред лозята', 30, 2, '1 double bed', '1 двойно легло', 95, 'white-house-vineyard', 1600, 2070),
]
UNIT_TEXT = {  # id: (description EN, description BG, [amenities EN], [amenities BG])
    'stone': ('A calm room with one bare stone wall, linen sheets and a deep bath.', 'Спокойна стая с една гола каменна стена, ленено бельо и дълбока вана.',
              ['Stone wall', 'Bath', 'Wi-Fi', 'Heating'], ['Каменна стена', 'Вана', 'Wi-Fi', 'Отопление']),
    'cellar': ('The coolest room in summer: a wooden headboard, a reading lamp and thick walls that keep the quiet.', 'Най-прохладната стая през лятото: дървена табла, лампа за четене и дебели стени, които пазят тишината.',
               ['Cool in summer', 'Shower room', 'Wi-Fi', 'Reading lamp'], ['Прохладна през лятото', 'Баня с душ', 'Wi-Fi', 'Лампа за четене']),
    'hearth': ('A large suite with a fireplace, a sitting area and space for a family of four.', 'Голям сюит с камина, кът за сядане и място за семейство от четирима.',
               ['Fireplace', 'Sitting area', 'Wi-Fi', 'Sleeps four'], ['Камина', 'Кът за сядане', 'Wi-Fi', 'За четирима']),
    'cottage': ('A small white house of your own at the edge of the vines, with a terrace and a view down the slope.', 'Малка бяла къщичка само за вас в края на лозята, с тераса и гледка надолу по склона.',
                ['Own terrace', 'Vineyard view', 'Wi-Fi', 'Private entrance'], ['Собствена тераса', 'Гледка към лозята', 'Wi-Fi', 'Собствен вход']),
}
# Things to do (examples): title EN, title BG, text EN, text BG, photo, width, height
DO = [
    ('Wine tasting', 'Дегустация на вино', 'Five wines from the slope and a board of local cheese, on the terrace.', 'Пет вина от склона и дъска с местно сирене, на терасата.', 'wine-tasting', 1600, 2134),
    ('Harvest days', 'Гроздобер', 'Pick grapes with us in September and join the first press.', 'През септември берете грозде с нас и участвайте в първото пресоване.', 'grapes-vine', 1600, 2360),
    ('Walks through the vines', 'Разходки сред лозята', 'Marked paths between the rows and up to the viewpoint.', 'Маркирани пътеки между редовете и до гледката.', 'vineyard-rows-sun', 1600, 2400),
    ('Long table dinners', 'Вечери на дългата маса', 'A shared dinner under the old tree, a few evenings a month.', 'Обща вечеря под старото дърво, няколко вечери в месеца.', 'courtyard-tree', 1600, 1067),
]
# Gallery: photo, width, height, caption EN, caption BG
GALLERY = [
    ('stone-arch-stairs', 1600, 2400, 'The stone house and its outside stairs', 'Каменната къща с външното стълбище'),
    ('stone-fireplace-living', 1600, 1067, 'The living room with its fireplace', 'Дневната с камина'),
    ('terraced-vines', 1600, 1200, 'The terraces below the house', 'Терасите под къщата'),
    ('tables-vineyard', 1600, 2400, 'The pavilion in the vines', 'Павилионът сред лозите'),
    ('barrels-courtyard', 1600, 1067, 'The courtyard with the old barrels', 'Дворът със старите бъчви'),
    ('stone-wood-windows', 1600, 2400, 'A balcony over the slope', 'Балкон над склона'),
    ('wine-cheese-table', 1600, 1067, 'Wine and cheese in the evening', 'Вино и сирене вечер'),
    ('vine-rows-mountains', 1600, 1067, 'Rows of vines and the hills behind', 'Редове лози и хълмовете зад тях'),
]
NOTES = [  # quote EN, quote BG, name EN, name BG, stay EN, stay BG
    ('We woke up to the rows of vines and a table already set. Slow mornings, and the wine is very good.', 'Събудихме се с редове лози и вече наредена маса. Бавни утрини, а виното е много добро.', 'Ana and Petar', 'Ана и Петър', 'September', 'септември'),
    ('The fireplace suite was perfect for our family. The kids loved the old press.', 'Сюитът с камината беше идеален за семейството ни. Децата обикнаха старата преса.', 'The Georgievs', 'Семейство Георгиеви', 'November', 'ноември'),
    ('Pick grapes in the morning, eat under the tree at night. We will come back for next year\'s harvest.', 'Берем грозде сутрин, вечеряме под дървото вечер. Ще се върнем за следващия гроздобер.', 'Elena', 'Елена', 'October', 'октомври'),
    ('Thick walls, cool rooms and the quiet of the hills. Booking was easy and the answer was quick.', 'Дебели стени, прохладни стаи и тишина от хълмовете. Резервацията беше лесна, а отговорът бърз.', 'Nikolay', 'Николай', 'July', 'юли'),
]

L = {
 'en': dict(
  lang='en', root='../', script='latin', other_href='../index.html', other_lang='bg', other_label='БГ', other_aria='Превключи на български',
  privacy_href='privacy.html', home_href='index.html', brand=BRAND_EN,
  title='The Stone Cellar – a guest house among the vines',
  desc='Four places to sleep in a restored stone barn among the vines. Wine tasting, harvest days and long table dinners. Pick your dates and send an enquiry.',
  skip='Skip to content', tagline='vineyard guest house', nav_label='Site menu', menu_btn='Menu',
  nav=[('#top', 'The place'), ('#story', 'Our story'), ('#stay', 'Stay'), ('#book', 'Book'), ('#do', 'Activities'), ('#gallery', 'Gallery'), ('#guests', 'Guestbook'), ('#visit', 'Visit')],
  cover_kicker='Vineyard guest house', h1='Sleep inside the old <em>cellar</em>.',
  lead='Four places to stay in a restored stone barn among the vines. Wake up to the rows, taste the wine and stay as long as you like.',
  cta1='Choose your dates', cta2='See the rooms', scroll='Scroll', cover_alt='An old stone house with a large tree in front, under a warm sky',
  k_story='Our story', story_h='A cellar that learned to host.',
  story_p1='The stone walls were laid by hand for a family press house. We kept the beams, the old wine press and the thick walls that stay cool in summer.',
  story_p2='Then we added warm floors, soft beds and a long table, so that you can sleep where the wine used to rest.',
  stats=[('4', 'places to sleep'), ('1200', 'vines growing around the house'), ('8', 'guests at most')],
  story_note='Example numbers and story. Replace them with your own.', story_alt='The old wooden wine press inside the stone barn', story_cap='The old press, still in its place',
  k_stay='Stay', stay_h='Four ways to stay', stay_p='Each place has its own bathroom. Prices are per night for the whole room or house.',
  guests_up='Up to {n} guests', from_price='from', per_night='per night', choose_dates='Choose dates for this room',
  k_book='Book', book_h='When are you coming?', book_p='Press your arrival day, then your departure day. Darker days are busier. We reply to confirm; nothing is charged online.',
  cal_prev='Previous month', cal_next='Next month', cal_pick='Pick your arrival day', lg_free='Free', lg_part='Partly booked', lg_full='Fully booked', lg_sel='Your stay',
  f_guests='Guests', guest_word='guest', guests_word='guests',
  b_room='Choose a place to stay', pick_dates='Pick your arrival and departure days to see what is free.', sum_h='Your stay',
  sum_note='Estimated total at the example prices. We confirm the final price when we reply.',
  f_name='Your name', f_phone='Phone', f_email='Email (optional)', f_msg='Message (optional)', f_send='Send enquiry',
  f_note='We use your details only to answer your enquiry.', f_priv='Privacy notice',
  k_do='Activities', do_h='Spend the days like this', do_p='All of these are on request, and most are small and personal.',
  k_gallery='Gallery', gal_h='The house and the hill', gal_p='Press a picture to see it larger.', open_photo='Open photo',
  k_guests='Guestbook', gb_h='Notes from our guests', gb_p='A few lines left on the long table.', rev_note='Example notes. Replace them with real guest reviews.',
  k_visit='Visit', visit_h='Find the house', addr_l='Address', addr='Primer St. 1, wine country', times_l='Check-in and check-out', times='Check-in from ' + CHECKIN + ', check-out until ' + CHECKOUT,
  phone_l='Phone', email_l='Email', map_t='The map is from OpenStreetMap and loads only if you choose.', map_btn='Show the map',
  faq_h='Good to know',
  faq=[('What time is check-in and check-out?', 'Check-in is from ' + CHECKIN + ' and check-out until ' + CHECKOUT + '. If you arrive early, we will keep your bags.'),
       ('Can we taste the wine?', 'Yes. Tastings are on request, on the terrace, for guests and for visitors. Tell us when you book.'),
       ('Is breakfast included?', 'Breakfast is served at the long table and costs 9 € per person. Tell us about allergies.'),
       ('Do you accept children and pets?', 'Children are very welcome. Dogs are welcome in the Vineyard Cottage.'),
       ('How do I pay, and what if my plans change?', 'You pay on arrival, by cash or card. Tell us at least five days ahead if you need to change or cancel, and there is no charge.'),
       ('How do I get there?', 'We send exact directions when we confirm. The last kilometre is a gravel road between the vines.')],
  bar_label='Booking', bar_from='From', bar_price='60 €', foot_priv='Privacy notice', admin_t='Demo back office', admin_href='../admin.html?lang=en',
  lb_label='Photo', lb_close='Close', lb_prev='Previous photo', lb_next='Next photo',
 ),
 'bg': dict(
  lang='bg', root='', script='cyrillic', other_href='en/index.html', other_lang='en', other_label='EN', other_aria='Switch to English',
  privacy_href='privacy.html', home_href='index.html', brand=BRAND_BG,
  title='Каменната изба – къща за гости сред лозята',
  desc='Четири места за нощувка в обновена каменна плевня сред лозята. Дегустация на вино, гроздобер и вечери на дългата маса. Изберете дати и изпратете запитване.',
  skip='Към съдържанието', tagline='къща за гости сред лозята', nav_label='Меню на сайта', menu_btn='Меню',
  nav=[('#top', 'Мястото'), ('#story', 'Нашата история'), ('#stay', 'Настаняване'), ('#book', 'Резервация'), ('#do', 'Какво да правите'), ('#gallery', 'Галерия'), ('#guests', 'Книга на гостите'), ('#visit', 'Посетете ни')],
  cover_kicker='Къща за гости сред лозята', h1='Нощувка в старата <em>изба</em>.',
  lead='Четири места за нощувка в обновена каменна плевня сред лозята. Събудете се с редовете лози, опитайте виното и останете колкото искате.',
  cta1='Изберете дати', cta2='Вижте стаите', scroll='Надолу', cover_alt='Стара каменна къща с голямо дърво отпред под топло небе',
  k_story='Нашата история', story_h='Изба, която се научи да посреща.',
  story_p1='Каменните стени са зидани на ръка за семейна изба. Запазихме гредите, старата преса за грозде и дебелите стени, които са прохладни през лятото.',
  story_p2='После добавихме топли подове, меки легла и дълга маса, за да спите там, където някога е почивало виното.',
  stats=[('4', 'места за нощувка'), ('1200', 'лози около къщата'), ('8', 'гости най-много')],
  story_note='Примерни числа и история. Заменете ги със свои.', story_alt='Старата дървена преса за грозде в каменната плевня', story_cap='Старата преса, все още на мястото си',
  k_stay='Настаняване', stay_h='Четири начина да отседнете', stay_p='Всяко място има собствена баня. Цените са на нощ за цялата стая или къща.',
  guests_up='До {n} гости', from_price='от', per_night='на нощ', choose_dates='Изберете дати за тази стая',
  k_book='Резервация', book_h='Кога ще дойдете?', book_p='Натиснете деня на пристигане, после деня на заминаване. По-тъмните дни са по-заети. Ще ви отговорим, за да потвърдим; онлайн нищо не се плаща.',
  cal_prev='Предишен месец', cal_next='Следващ месец', cal_pick='Изберете ден на пристигане', lg_free='Свободно', lg_part='Частично заето', lg_full='Изцяло заето', lg_sel='Вашият престой',
  f_guests='Гости', guest_word='гост', guests_word='гости',
  b_room='Изберете къде да отседнете', pick_dates='Изберете дни на пристигане и заминаване, за да видите какво е свободно.', sum_h='Вашият престой',
  sum_note='Ориентировъчна обща сума по примерните цени. Крайната цена потвърждаваме, когато ви отговорим.',
  f_name='Вашето име', f_phone='Телефон', f_email='Имейл (по желание)', f_msg='Съобщение (по желание)', f_send='Изпрати запитване',
  f_note='Ползваме данните ви само за да отговорим на запитването.', f_priv='Политика за поверителност',
  k_do='Какво да правите', do_h='Прекарайте дните така', do_p='Всичко това е по заявка, а повечето неща са малки и лични.',
  k_gallery='Галерия', gal_h='Къщата и хълмът', gal_p='Натиснете снимка, за да я видите по-голяма.', open_photo='Отвори снимката',
  k_guests='Книга на гостите', gb_h='Бележки от нашите гости', gb_p='Няколко реда, оставени на дългата маса.', rev_note='Примерни бележки. Заменете ги с истински отзиви от гости.',
  k_visit='Посетете ни', visit_h='Намерете къщата', addr_l='Адрес', addr='ул. Примерна 1, лозарски край', times_l='Настаняване и освобождаване', times='Настаняване от ' + CHECKIN + ', освобождаване до ' + CHECKOUT,
  phone_l='Телефон', email_l='Имейл', map_t='Картата е от OpenStreetMap и се зарежда само ако поискате.', map_btn='Покажи картата',
  faq_h='Добре е да знаете',
  faq=[('Кога е настаняването и освобождаването?', 'Настаняване от ' + CHECKIN + ' и освобождаване до ' + CHECKOUT + '. Ако пристигнете по-рано, ще пазим багажа ви.'),
       ('Може ли да опитаме виното?', 'Да. Дегустациите са по заявка, на терасата, за гости и за посетители. Кажете ни при резервацията.'),
       ('Включена ли е закуската?', 'Закуската е на дългата маса и струва 9 € на човек. Кажете ни за алергии.'),
       ('Приемате ли деца и домашни любимци?', 'Децата са много добре дошли. Кучета са добре дошли в Къщичката сред лозята.'),
       ('Как се плаща и какво ако плановете ми се променят?', 'Плаща се на място, в брой или с карта. Кажете ни поне пет дни по-рано, ако трябва да промените или отмените, и няма такса.'),
       ('Как да стигна?', 'Изпращаме точни упътвания при потвърждението. Последният километър е чакълен път между лозите.')],
  bar_label='Резервация', bar_from='От', bar_price='60 €', foot_priv='Политика за поверителност', admin_t='Демо админ панел', admin_href='admin.html',
  lb_label='Снимка', lb_close='Затвори', lb_prev='Предишна снимка', lb_next='Следваща снимка',
 ),
}

TEMPLATE = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'page_template.html'), encoding='utf-8').read()


def build(lang):
    d = L[lang]
    e = lambda s: escape(s, quote=True)
    root = d['root']
    bg = lang == 'bg'
    out = {'lang': lang, 'root': root, 'script': d['script']}
    keys = ['title', 'desc', 'skip', 'tagline', 'nav_label', 'menu_btn', 'cover_kicker', 'lead', 'cta1', 'cta2', 'scroll', 'cover_alt',
            'k_story', 'story_h', 'story_p1', 'story_p2', 'story_note', 'story_alt', 'story_cap', 'k_stay', 'stay_h', 'stay_p',
            'k_book', 'book_h', 'book_p', 'cal_prev', 'cal_next', 'cal_pick', 'lg_free', 'lg_part', 'lg_full', 'lg_sel', 'f_guests', 'b_room', 'pick_dates', 'sum_h', 'sum_note',
            'f_name', 'f_phone', 'f_email', 'f_msg', 'f_send', 'f_note', 'f_priv', 'k_do', 'do_h', 'do_p', 'k_gallery', 'gal_h', 'gal_p', 'k_guests', 'gb_h', 'gb_p', 'rev_note',
            'k_visit', 'visit_h', 'addr_l', 'addr', 'times_l', 'times', 'phone_l', 'email_l', 'map_t', 'map_btn', 'faq_h', 'bar_label', 'bar_from', 'bar_price', 'per_night',
            'foot_priv', 'admin_t', 'lb_label', 'lb_close', 'lb_prev', 'lb_next', 'brand']
    for k in keys:
        out[k] = e(d[k])
    out['h1'] = d['h1']   # contains <em>
    out['other_href'] = d['other_href']; out['other_lang'] = d['other_lang']; out['other_label'] = d['other_label']; out['other_aria'] = e(d['other_aria'])
    out['privacy_href'] = d['privacy_href']; out['home_href'] = d['home_href']; out['admin_href'] = d['admin_href']
    out['nav_links'] = '\n        '.join('<li><a href="%s"><i>%02d</i>%s</a></li>' % (h, n + 1, e(t)) for n, (h, t) in enumerate(d['nav']))
    out['guest_options'] = ''.join('<option value="%d"%s>%d %s</option>' % (n, ' selected' if n == 2 else '', n, d['guest_word'] if n == 1 else d['guests_word']) for n in range(1, 9))
    out['stats'] = '\n          '.join('<li><b>%s</b><span>%s</span></li>' % (e(n), e(t)) for n, t in d['stats'])

    units, uopts = [], []
    for n, (uid, en, bgn, m2, cap, bed_en, bed_bg, price, photo, w, h) in enumerate(UNITS):
        name = bgn if bg else en
        de, db, ae, ab = UNIT_TEXT[uid]
        units.append(
            '<article class="card" style="--i:%d"><figure><img src="%simages/stock/%s-800.jpg" width="800" height="%d" alt="" loading="lazy" decoding="async"></figure>'
            '<div class="card-body"><p class="card-no" aria-hidden="true">%02d</p><h3>%s</h3><ul class="meta"><li>%d m²</li><li>%s</li><li>%s</li></ul><p>%s</p>'
            '<ul class="am">%s</ul><p class="card-price">%s <b>%d €</b> %s</p><button class="btn btn-gold" type="button" data-unit="%s">%s</button></div></article>'
            % (n, root, photo, round(800 * h / w), n + 1, e(name), m2, e(d['guests_up'].replace('{n}', str(cap))), e(bed_bg if bg else bed_en),
               e(db if bg else de), ''.join('<li>%s</li>' % e(x) for x in (ab if bg else ae)), e(d['from_price']), price, e(d['per_night']), uid, e(d['choose_dates'])))
        uopts.append(
            '<label class="uc" data-room="%s"><input type="radio" name="room" value="%s" data-price="%d" data-cap="%d" data-name="%s">'
            '<img src="%simages/stock/%s-800.jpg" alt="" width="84" height="84" loading="lazy"><span class="uc-main"><b>%s</b><small>%s</small></span>'
            '<span class="uc-price"><b>%d €</b> <small>%s</small></span><span class="tag" data-tag></span></label>'
            % (uid, uid, price, cap, e(name), root, photo, e(name), e('%d m² · %s' % (m2, d['guests_up'].replace('{n}', str(cap)))), price, e(d['per_night'])))
    out['units'] = '\n        '.join(units)
    out['unit_options'] = '\n            '.join(uopts)

    out['todo'] = '\n        '.join(
        '<li><img src="%simages/stock/%s-800.jpg" width="800" height="%d" alt="" loading="lazy" decoding="async"><div><h3>%s</h3><p>%s</p></div></li>'
        % (root, photo, round(800 * h / w), e(tbg if bg else ten), e(xbg if bg else xen)) for ten, tbg, xen, xbg, photo, w, h in DO)
    out['gallery'] = '\n        '.join(
        '<button class="sq" type="button" data-full="%simages/stock/%s.jpg" data-cap="%s" aria-label="%s: %s"><img src="%simages/stock/%s-800.jpg" width="800" height="%d" alt="%s" loading="lazy" decoding="async"></button>'
        % (root, photo, e(cb if bg else ce), e(d['open_photo']), e(cb if bg else ce), root, photo, round(800 * h / w), e(cb if bg else ce)) for photo, w, h, ce, cb in GALLERY)
    out['notes'] = '\n        '.join(
        '<li class="note" style="--r:%s"><p>“%s”</p><b>%s</b><span>%s</span></li>' % (['-2deg', '1.5deg', '-1deg', '2deg'][n % 4], e(r[1] if bg else r[0]), e(r[3] if bg else r[2]), e(r[5] if bg else r[4]))
        for n, r in enumerate(NOTES))
    out['faq'] = '\n          '.join('<details><summary>%s</summary><p>%s</p></details>' % (e(q), e(a)) for q, a in d['faq'])
    out['phone'] = PHONE_DISPLAY; out['phone_href'] = PHONE_HREF; out['email'] = EMAIL
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
rooms_js = ', '.join('{ id: "%s", guests: %d, price: %d }' % (r[0], r[4], r[7]) for r in UNITS)
cfg = (
    '/* Generated by tools/build_pages.py. Edit the values at the top of that file, then run it again. */\n'
    'window.CELLAR_CONFIG = {\n'
    '  mode: "%s",            /* "demo" = enquiries are kept in this browser only; "live" = real API at apiBase (docs/API.md) */\n'
    '  apiBase: "%s",\n'
    '  rooms: [%s],\n'
    '  maxNights: %d,\n'
    '  latency: [600, 1100]      /* demo only: pretend network delay in milliseconds */\n'
    '};\n'
) % (MODE, API_BASE, rooms_js, MAX_NIGHTS)
os.makedirs(os.path.join(SHOP, 'js'), exist_ok=True)
open(os.path.join(SHOP, 'js', 'config.js'), 'w', encoding='utf-8').write(cfg)
print('config.js written')
