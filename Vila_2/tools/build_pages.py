import os, re, json
from html import escape

SHOP = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ---- Edit these placeholders for each guest house --------------------------------------------
BRAND_EN = 'Linden House'
BRAND_BG = 'Къща Липа'
PHONE_DISPLAY = '+359 000 000 000'
PHONE_HREF = '+359000000000'
EMAIL = 'email@example.com'
CHECKIN = '14:00'
CHECKOUT = '11:00'
# Enquiry system. 'demo' = the booking form talks to a mock server that keeps enquiries in the visitor's browser.
# 'live' = it sends real HTTP requests to API_BASE (see docs/API.md). Written to js/config.js.
MODE = 'demo'
API_BASE = '/api'
MAX_NIGHTS = 30
# ---------------------------------------------------------------------------------------------

# Rooms (all names, sizes and prices are examples): id, name EN, name BG, m2, guests, bed EN, bed BG, price per night (EUR), photo, width, height
ROOMS = [
    ('orchard', 'Garden Room', 'Стая „Градина“', 22, 2, '1 double bed', '1 двойно легло', 65, 'bedroom-large-window', 1600, 2133),
    ('attic',   'The Attic',    'Мансардата',      18, 2, '1 iron-frame bed', '1 легло с метална рамка', 55, 'vintage-bedroom', 1600, 1200),
    ('blue',    'The Blue Room (family)', 'Синята стая (семейна)', 30, 4, '1 double bed and a sofa bed', '1 двойно легло и разтегателен диван', 95, 'cozy-bedroom', 1600, 1067),
]
ROOM_TEXT = {  # id: (description EN, description BG, [amenities EN], [amenities BG])
    'orchard': ('A bright double room with a deep window over the garden. Linen curtains, a reading chair and soft morning light.',
                'Светла двойна стая с дълбок прозорец към градината. Ленени завеси, кресло за четене и мека сутрешна светлина.',
                ['Garden view', 'Private bathroom', 'Wi-Fi', 'Heating'], ['Гледка към градината', 'Собствена баня', 'Wi-Fi', 'Отопление']),
    'attic': ('A cosy room under the roof, with a sloping ceiling, an old iron bed and a small window full of treetops.',
              'Уютна стая под покрива, със скосен таван, старо желязно легло и малък прозорец, пълен с корони на дървета.',
              ['Treetop view', 'Shower room', 'Wi-Fi', 'Quiet floor'], ['Гледка към дърветата', 'Баня с душ', 'Wi-Fi', 'Тих етаж']),
    'blue': ('Our largest room, with deep blue panelling, a round table by the window and space for a family of four.',
             'Най-голямата ни стая, с тъмносиня ламперия, кръгла маса и място за семейство от четирима.',
             ['Sleeps four', 'Private bathroom', 'Wi-Fi', 'Table for two'], ['За четирима', 'Собствена баня', 'Wi-Fi', 'Маса за двама']),
}
# A day here: time, title EN, title BG, text EN, text BG, photo, width, height
DAY = [
    ('08:30', 'Breakfast', 'Закуска', 'Pastries, jam, eggs and fruit on the long table. Coffee as long as you like.', 'Питки, сладко, яйца и плодове на дългата маса. Кафе, докато поискате.', 'pastries', 1600, 1067),
    ('14:00', 'Arrive and unwind', 'Пристигане и почивка', 'Check in, leave your bags and take a coffee on the terrace under the vines.', 'Настанявате се, оставяте багажа и пиете кафе на терасата под лозницата.', 'patio-vines', 1600, 1067),
    ('19:00', 'By the stove', 'До печката', 'A wood fire in the lounge, tea and a board game while the valley goes dark.', 'Огън в камината, чай и настолна игра, докато долината притъмнява.', 'stove-cabin', 1600, 1067),
]
SEASONS = {
    'summer': ('hills-fences', 1600, 1200, ['Meadow walks from the front door', 'Cool evenings on the terrace', 'Berries and honey at breakfast'],
               ['Разходки по поляните от входната врата', 'Прохладни вечери на терасата', 'Горски плодове и мед на закуска']),
    'winter': ('snow-cabin', 1600, 2400, ['The wood stove is lit all day', 'Snow trails, with a ski lift a short drive away', 'Hot tea and thick blankets'],
               ['Печката гори през целия ден', 'Пътеки в снега и ски лифт на няколко минути с кола', 'Горещ чай и дебели одеяла']),
}
# Places around (examples): name EN, name BG, minutes, mode (foot | car)
PLACES = [
    ('Village square and bakery', 'Селски площад и пекарна', 4, 'foot'),
    ('Old stone bridge', 'Старият каменен мост', 12, 'foot'),
    ('Forest trail to the waterfall', 'Горска пътека до водопада', 25, 'foot'),
    ('Meadow viewpoint', 'Поляна с гледка', 40, 'foot'),
    ('Ski lift', 'Ски лифт', 12, 'car'),
    ('Thermal spa', 'Термален спа център', 25, 'car'),
    ('Monastery', 'Манастир', 35, 'car'),
]
# Gallery: photo, class, width, height, caption EN, caption BG
GALLERY = [
    ('cabin-trees', 'g1', 1600, 2000, 'The house, early morning', 'Къщата, рано сутринта'),
    ('rustic-bed', 'g2', 1600, 2400, 'A bed made of branches', 'Легло от клони'),
    ('breakfast-spread', 'g3', 1600, 1067, 'Breakfast for everyone', 'Закуска за всички'),
    ('wooden-houses-valley', 'g4', 1600, 1065, 'The valley from the trail', 'Долината от пътеката'),
    ('coffee-cups', 'g5', 1600, 1065, 'Coffee on the terrace', 'Кафе на терасата'),
    ('cabin-night-snow', 'g6', 1600, 1200, 'Winter evening', 'Зимна вечер'),
    ('pergola', 'g7', 1600, 2400, 'The pergola in the garden', 'Асмата в градината'),
    ('stone-houses-valley', 'g8', 1600, 2133, 'Stone houses in autumn', 'Каменни къщи наесен'),
    ('room-table-windows', 'g9', 1600, 1068, 'A reading corner', 'Кът за четене'),
]
REVIEWS = [  # quote EN, quote BG, name EN, name BG, stay EN, stay BG
    ('Warm, quiet and the breakfast was a feast. We slept with the window open and woke to birdsong.', 'Топло, тихо, а закуската беше истински пир. Спахме с отворен прозорец и се събудихме с птичи песни.', 'Maria and Ivo', 'Мария и Иво', 'Stayed in June', 'Отседнали през юни'),
    ('The wood stove, the blankets, the snow outside. We did not want to leave.', 'Печката, одеялата, снегът навън. Не ни се тръгваше.', 'Desi', 'Деси', 'Stayed in January', 'Отседнала през януари'),
    ('Our kids ran around the garden all day. The Blue Room was spacious and spotless.', 'Децата тичаха из градината цял ден. Синята стая беше просторна и безупречна.', 'The Petrov family', 'Семейство Петрови', 'Stayed in August', 'Отседнали през август'),
    ('Easy to book, a quick answer, and a host who told us the best trails.', 'Лесно запазване, бърз отговор и домакин, който ни показа най-хубавите пътеки.', 'Georgi', 'Георги', 'Stayed in October', 'Отседнал през октомври'),
]

L = {
 'en': dict(
  lang='en', root='../', script='latin', other_href='../index.html', other_lang='bg', other_label='БГ', other_aria='Превключи на български',
  privacy_href='privacy.html', home_href='index.html', brand=BRAND_EN,
  title='Linden House – a mountain guest house with a wood stove',
  desc='Three rooms, a long breakfast table and a wood stove in a quiet mountain house. See the rooms, check free dates and send an enquiry.',
  skip='Skip to content', tagline='mountain guest house', side_label='Site menu', nav_label='Main navigation', menu_btn='Menu',
  nav=[('#stay', 'Stay'), ('#rooms', 'Rooms'), ('#day', 'A day here'), ('#around', 'Around'), ('#gallery', 'Gallery'), ('#reviews', 'Reviews'), ('#book', 'Book'), ('#visit', 'Visit')],
  cta='Book', hero_kicker='Mountain guest house',
  h1='A quiet house, a warm stove, a <em>long</em> breakfast.',
  lead='Three rooms, a garden terrace and a wood stove. Come for a weekend or stay the week, and wake up to the mountain.',
  hero_cta1='See the rooms', hero_cta2='Check dates', hero_alt='A wooden house on a mountain meadow with peaks behind it',
  postcard_t='Good to know', postcard_l1='Check-in from ' + CHECKIN, postcard_l2='Check-out until ' + CHECKOUT,
  avail_h='Check free dates', avail_btn='Check free rooms', f_in='Arrival', f_out='Departure', f_guests='Guests', guest_word='guest', guests_word='guests',
  facts_label='The house in numbers',
  facts=[('3', 'rooms'), ('8', 'guests at most'), ('8 €', 'breakfast, per person'), ('Free', 'parking at the door')],
  k_rooms='Rooms', rooms_h='Three rooms, three moods', rooms_p='Each room has its own bathroom. The prices below are per night for the whole room.',
  guests_up='Up to {n} guests', from_price='from', per_night='per night', book_room='Book this room',
  k_day='A day here', day_h='How a day goes', day_p='No schedule, but this is how most guests spend it.',
  seasons_h='Seasons', summer='Summer', winter='Winter',
  k_around='Around', around_h='What is close', around_p='The distance ladder: the shorter the line, the closer the place.', around_filter='Filter by how you get there',
  m_all='All', m_foot='On foot', m_car='By car', min_foot='{m} min on foot', min_car='{m} min by car',
  around_note='Example places and times. Replace them with your own.', around_alt='A forest path with tall trees',
  k_gallery='Gallery', gal_h='The house in pictures', gal_p='Press a picture to see it larger.', open_photo='Open photo',
  k_rev='Reviews', rev_h='What guests say', rev_p='Example rating. Replace it with your real rating.', rev_note='Example reviews. Replace them with real guest reviews.', rev_prev='Previous review', rev_next='Next review',
  k_book='Book', book_h='Tell us when you would like to come', book_p='Pick your dates and a free room. We reply to confirm; nothing is charged online.',
  b_dates='Your dates', b_room='Choose a room', pick_dates='Pick your arrival and departure dates to see which rooms are free.',
  free='Free', taken='Taken', too_small='Too small', night_one='{n} night', night_many='{n} nights',
  sum_h='Your stay', sum_note='Estimated total at the example prices above. We confirm the final price when we reply.',
  f_name='Your name', f_phone='Phone', f_email='Email (optional)', f_msg='Message (optional)', f_send='Send enquiry',
  f_note='We use your details only to answer your enquiry.', f_priv='Privacy notice',
  k_visit='Visit', visit_h='Find the house', addr_l='Address', addr='Primer St. 1, Rhodope Mountains', times_l='Check-in and check-out', times='Check-in from ' + CHECKIN + ', check-out until ' + CHECKOUT,
  phone_l='Phone', email_l='Email', map_t='The map is from OpenStreetMap and loads only if you choose.', map_btn='Show the map',
  faq_h='Good to know',
  faq=[('What time is check-in and check-out?', 'Check-in is from ' + CHECKIN + ' and check-out until ' + CHECKOUT + '. If you arrive early, we will keep your bags.'),
       ('Is breakfast included?', 'Breakfast is served from 08:30 and costs 8 € per person. Tell us about allergies when you book.'),
       ('Do you accept children and pets?', 'Children are very welcome. Small dogs can stay in the Attic on request.'),
       ('Is there parking?', 'Yes, free parking at the door for up to three cars.'),
       ('How do I pay, and what if my plans change?', 'You pay on arrival, by cash or card. Tell us at least three days ahead if you need to change or cancel, and there is no charge.'),
       ('How do I get there?', 'We send exact directions when we confirm. The last part of the road is a short gravel track.')],
  foot_priv='Privacy notice', admin_t='Demo back office', admin_href='../admin.html?lang=en', quick_label='Quick contact', q_call='Call', q_book='Book',
  lb_label='Photo', lb_close='Close', lb_prev='Previous photo', lb_next='Next photo',
 ),
 'bg': dict(
  lang='bg', root='', script='cyrillic', other_href='en/index.html', other_lang='en', other_label='EN', other_aria='Switch to English',
  privacy_href='privacy.html', home_href='index.html', brand=BRAND_BG,
  title='Къща Липа – планинска къща за гости с печка на дърва',
  desc='Три стаи, дълга маса за закуска и печка на дърва в тиха планинска къща. Разгледайте стаите, проверете свободните дати и изпратете запитване.',
  skip='Към съдържанието', tagline='планинска къща за гости', side_label='Меню на сайта', nav_label='Основна навигация', menu_btn='Меню',
  nav=[('#stay', 'Настаняване'), ('#rooms', 'Стаи'), ('#day', 'Един ден тук'), ('#around', 'Наоколо'), ('#gallery', 'Галерия'), ('#reviews', 'Отзиви'), ('#book', 'Резервация'), ('#visit', 'Посетете ни')],
  cta='Резервирайте', hero_kicker='Планинска къща за гости',
  h1='Тиха къща, топла печка и <em>дълга</em> закуска.',
  lead='Три стаи, градинска тераса и печка на дърва. Елате за уикенд или останете цяла седмица и се събудете с планината.',
  hero_cta1='Вижте стаите', hero_cta2='Проверете дати', hero_alt='Дървена къща на планинска поляна с върхове зад нея',
  postcard_t='Добре е да знаете', postcard_l1='Настаняване от ' + CHECKIN, postcard_l2='Освобождаване до ' + CHECKOUT,
  avail_h='Проверете свободни дати', avail_btn='Проверете свободните стаи', f_in='Пристигане', f_out='Заминаване', f_guests='Гости', guest_word='гост', guests_word='гости',
  facts_label='Къщата в числа',
  facts=[('3', 'стаи'), ('8', 'гости най-много'), ('8 €', 'закуска, на човек'), ('Безплатен', 'паркинг пред вратата')],
  k_rooms='Стаи', rooms_h='Три стаи, три настроения', rooms_p='Всяка стая има собствена баня. Цените по-долу са на нощ за цялата стая.',
  guests_up='До {n} гости', from_price='от', per_night='на нощ', book_room='Резервирайте тази стая',
  k_day='Един ден тук', day_h='Как минава денят', day_p='Без график, но така го прекарват повечето гости.',
  seasons_h='Сезони', summer='Лято', winter='Зима',
  k_around='Наоколо', around_h='Какво е близо', around_p='Стълбата на разстоянията: колкото по-къса е линията, толкова по-близо е мястото.', around_filter='Филтър по начин на придвижване',
  m_all='Всички', m_foot='Пеша', m_car='С кола', min_foot='{m} мин пеша', min_car='{m} мин с кола',
  around_note='Примерни места и времена. Заменете ги със свои.', around_alt='Горска пътека с високи дървета',
  k_gallery='Галерия', gal_h='Къщата в снимки', gal_p='Натиснете снимка, за да я видите по-голяма.', open_photo='Отвори снимката',
  k_rev='Отзиви', rev_h='Какво казват гостите', rev_p='Примерна оценка. Заменете я с истинската.', rev_note='Примерни отзиви. Заменете ги с истински отзиви от гости.', rev_prev='Предишен отзив', rev_next='Следващ отзив',
  k_book='Резервация', book_h='Кажете ни кога искате да дойдете', book_p='Изберете дати и свободна стая. Ще ви отговорим, за да потвърдим; онлайн нищо не се плаща.',
  b_dates='Вашите дати', b_room='Изберете стая', pick_dates='Изберете дати на пристигане и заминаване, за да видите кои стаи са свободни.',
  free='Свободна', taken='Заета', too_small='Твърде малка', night_one='{n} нощ', night_many='{n} нощувки',
  sum_h='Вашият престой', sum_note='Ориентировъчна обща сума по примерните цени. Крайната цена потвърждаваме, когато ви отговорим.',
  f_name='Вашето име', f_phone='Телефон', f_email='Имейл (по желание)', f_msg='Съобщение (по желание)', f_send='Изпрати запитване',
  f_note='Ползваме данните ви само за да отговорим на запитването.', f_priv='Политика за поверителност',
  k_visit='Посетете ни', visit_h='Намерете къщата', addr_l='Адрес', addr='ул. Примерна 1, Родопите', times_l='Настаняване и освобождаване', times='Настаняване от ' + CHECKIN + ', освобождаване до ' + CHECKOUT,
  phone_l='Телефон', email_l='Имейл', map_t='Картата е от OpenStreetMap и се зарежда само ако поискате.', map_btn='Покажи картата',
  faq_h='Добре е да знаете',
  faq=[('Кога е настаняването и освобождаването?', 'Настаняване от ' + CHECKIN + ' и освобождаване до ' + CHECKOUT + '. Ако пристигнете по-рано, ще пазим багажа ви.'),
       ('Включена ли е закуската?', 'Закуската е от 08:30 и струва 8 € на човек. Кажете ни за алергии при резервацията.'),
       ('Приемате ли деца и домашни любимци?', 'Децата са много добре дошли. Малки кучета могат да отседнат в Мансардата по заявка.'),
       ('Има ли паркинг?', 'Да, безплатен паркинг пред вратата за до три коли.'),
       ('Как се плаща и какво ако плановете ми се променят?', 'Плаща се на място, в брой или с карта. Кажете ни поне три дни по-рано, ако трябва да промените или отмените, и няма такса.'),
       ('Как да стигна?', 'Изпращаме точни упътвания при потвърждението. Последният участък е кратък чакълен път.')],
  foot_priv='Политика за поверителност', admin_t='Демо админ панел', admin_href='admin.html', quick_label='Бърза връзка', q_call='Обадете се', q_book='Резервирайте',
  lb_label='Снимка', lb_close='Затвори', lb_prev='Предишна снимка', lb_next='Следваща снимка',
 ),
}

TEMPLATE = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'page_template.html'), encoding='utf-8').read()


def build(lang):
    d = L[lang]
    e = lambda s: escape(s, quote=True)
    root = d['root']
    bg = lang == 'bg'
    i = 1 if bg else 0
    out = {'lang': lang, 'root': root, 'script': d['script']}
    keys = ['title', 'desc', 'skip', 'tagline', 'side_label', 'nav_label', 'menu_btn', 'cta', 'hero_kicker', 'lead', 'hero_cta1', 'hero_cta2', 'hero_alt',
            'postcard_t', 'postcard_l1', 'postcard_l2', 'avail_h', 'avail_btn', 'f_in', 'f_out', 'f_guests', 'facts_label',
            'k_rooms', 'rooms_h', 'rooms_p', 'k_day', 'day_h', 'day_p', 'seasons_h', 'summer', 'winter', 'k_around', 'around_h', 'around_p', 'around_filter', 'm_all', 'm_foot', 'm_car',
            'around_note', 'around_alt', 'k_gallery', 'gal_h', 'gal_p', 'k_rev', 'rev_h', 'rev_p', 'rev_note', 'rev_prev', 'rev_next',
            'k_book', 'book_h', 'book_p', 'b_dates', 'b_room', 'pick_dates', 'sum_h', 'sum_note', 'f_name', 'f_phone', 'f_email', 'f_msg', 'f_send', 'f_note', 'f_priv',
            'k_visit', 'visit_h', 'addr_l', 'addr', 'times_l', 'times', 'phone_l', 'email_l', 'map_t', 'map_btn', 'faq_h', 'foot_priv', 'admin_t', 'quick_label', 'q_call', 'q_book',
            'lb_label', 'lb_close', 'lb_prev', 'lb_next', 'brand']
    for k in keys:
        out[k] = e(d[k])
    out['h1'] = d['h1']   # contains <em>
    out['other_href'] = d['other_href']; out['other_lang'] = d['other_lang']; out['other_label'] = d['other_label']; out['other_aria'] = e(d['other_aria'])
    out['privacy_href'] = d['privacy_href']; out['home_href'] = d['home_href']; out['admin_href'] = d['admin_href']
    out['nav_links'] = '\n      '.join('<li><a href="%s"><i>%02d</i>%s</a></li>' % (h, n + 1, e(t)) for n, (h, t) in enumerate(d['nav']))
    out['guest_options'] = ''.join('<option value="%d"%s>%d %s</option>' % (n, ' selected' if n == 2 else '', n, d['guest_word'] if n == 1 else d['guests_word']) for n in range(1, 9))
    out['facts'] = '\n    '.join('<li><b>%s</b><span>%s</span></li>' % (e(n), e(t)) for n, t in d['facts'])

    rooms, ropts = [], []
    for n, (rid, en, bgn, m2, cap, bed_en, bed_bg, price, photo, w, h) in enumerate(ROOMS):
        name = bgn if bg else en
        de, db, ae, ab = ROOM_TEXT[rid]
        rooms.append(
            '<article class="room%s"><figure><img src="%simages/stock/%s-800.jpg" width="800" height="%d" alt="" loading="lazy" decoding="async"><span class="room-no" aria-hidden="true">%02d</span></figure>'
            '<div class="room-body"><h3>%s</h3><ul class="meta"><li>%d m²</li><li>%s</li><li>%s</li></ul><p>%s</p><ul class="am">%s</ul>'
            '<p class="room-price">%s <b>%d €</b> %s</p><button class="btn btn-main" type="button" data-room="%s">%s</button></div></article>'
            % (' rev' if n % 2 else '', root, photo, round(800 * h / w), n + 1, e(name), m2, e(d['guests_up'].replace('{n}', str(cap))), e(bed_bg if bg else bed_en),
               e(db if bg else de), ''.join('<li>%s</li>' % e(x) for x in (ab if bg else ae)), e(d['from_price']), price, e(d['per_night']), rid, e(d['book_room'])))
        ropts.append(
            '<label class="rc" data-room="%s"><input type="radio" name="room" value="%s" data-price="%d" data-cap="%d" data-name="%s">'
            '<img src="%simages/stock/%s-800.jpg" alt="" width="96" height="80" loading="lazy"><span class="rc-main"><b>%s</b><small>%s</small></span>'
            '<span class="rc-price"><b>%d €</b> <small>%s</small></span><span class="tag" data-tag></span></label>'
            % (rid, rid, price, cap, e(name), root, photo, e(name), e('%d m² · %s' % (m2, d['guests_up'].replace('{n}', str(cap)))), price, e(d['per_night'])))
    out['rooms'] = '\n      '.join(rooms)
    out['room_options'] = '\n            '.join(ropts)

    day = []
    for t, ten, tbg, xen, xbg, photo, w, h in DAY:
        day.append('<li><img src="%simages/stock/%s-800.jpg" width="800" height="%d" alt="" loading="lazy" decoding="async"><div><time>%s</time><h3>%s</h3><p>%s</p></div></li>'
                   % (root, photo, round(800 * h / w), t, e(tbg if bg else ten), e(xbg if bg else xen)))
    out['day'] = '\n        '.join(day)

    sp = []
    for key in ('summer', 'winter'):
        photo, w, h, a_en, a_bg = SEASONS[key]
        sp.append('<div class="spanel" id="sp-%s" role="tabpanel" aria-labelledby="st-%s"%s><img src="%simages/stock/%s-800.jpg" width="800" height="%d" alt="" loading="lazy" decoding="async"><ul>%s</ul></div>'
                  % (key, key, '' if key == 'summer' else ' hidden', root, photo, round(800 * h / w), ''.join('<li>%s</li>' % e(x) for x in (a_bg if bg else a_en))))
    out['season_panels'] = '\n        '.join(sp)

    places = []
    for en, bgn, m, mode in PLACES:
        txt = (d['min_foot'] if mode == 'foot' else d['min_car']).replace('{m}', str(m))
        places.append('<li data-mode="%s" style="--w:%d%%"><span class="pl-name">%s</span><span class="pl-time">%s</span><span class="bar" aria-hidden="true"><i></i></span></li>'
                      % (mode, min(100, round(m / 45 * 100)), e(bgn if bg else en), e(txt)))
    out['places'] = '\n          '.join(places)

    gal = []
    for photo, cls, w, h, c_en, c_bg in GALLERY:
        cap = c_bg if bg else c_en
        gal.append('<button class="g %s" type="button" data-full="%simages/stock/%s.jpg" data-cap="%s" aria-label="%s: %s"><img src="%simages/stock/%s-800.jpg" width="800" height="%d" alt="%s" loading="lazy" decoding="async"></button>'
                   % (cls, root, photo, e(cap), e(d['open_photo']), e(cap), root, photo, round(800 * h / w), e(cap)))
    out['gallery'] = '\n        '.join(gal)

    out['reviews'] = '\n          '.join(
        '<figure class="slide"%s><blockquote>%s</blockquote><figcaption><b>%s</b> · %s</figcaption></figure>' % ('' if n == 0 else ' hidden', e(r[1] if bg else r[0]), e(r[3] if bg else r[2]), e(r[5] if bg else r[4]))
        for n, r in enumerate(REVIEWS))
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
rooms_js = ', '.join('{ id: "%s", guests: %d, price: %d }' % (r[0], r[4], r[7]) for r in ROOMS)
cfg = (
    '/* Generated by tools/build_pages.py. Edit the values at the top of that file, then run it again. */\n'
    'window.LINDEN_CONFIG = {\n'
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
