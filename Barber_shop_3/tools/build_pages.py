import os, re
from html import escape

SHOP = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ---- Edit these placeholders for each barbershop ---------------------------------------------
OPEN_WEEKDAY = '09:00-20:00'      # opening and closing time, Mon - Fri
OPEN_WEEKEND = '10:00-18:00'      # opening and closing time, Sat - Sun
PHONE_DISPLAY = '+359 000 000 000'
PHONE_HREF = '+359000000000'
EMAIL = 'email@example.com'
# Booking system. 'demo' = the chair board talks to a mock server that keeps bookings in the visitor's browser.
# 'live' = it sends real HTTP requests to API_BASE (see docs/API.md). Written to js/config.js.
MODE = 'demo'
API_BASE = '/api'
SLOT_MINUTES = 30                 # gap between start times
BRAND = 'Hollis & Dane'
# ---------------------------------------------------------------------------------------------

SKINS = [  # key, colours for the swatch (background, accent), names
    ('paper',  '#F2ECDD', '#8C1D18', 'Newsprint',          'Вестникарска хартия'),
    ('ink',    '#14161C', '#E2B34B', 'Night Edition',      'Нощно издание'),
    ('sage',   '#E6ECE0', '#2F6B4F', 'Sage and Cream',     'Градински зелен'),
    ('rose',   '#F5E4DF', '#A33B55', 'Dusty Rose',         'Прашна роза'),
    ('cobalt', '#E4EBF7', '#1F4BC2', 'Cobalt Blue',        'Кобалтово синьо'),
]
DEFAULT_SKIN = SKINS[0]

# Barbers (names and photos are examples). id, name, photo file, width, height
BARBERS = [
    ('theo',  'Theo',  'bearded-man',     1600, 2400),
    ('ivan',  'Ivan',  'haircut-shop-2',  1600, 2400),
    ('marco', 'Marco', 'white-shirt-cut', 1600, 1067),
]

# Services: id, group, minutes, price (EUR), name EN, name BG
SERVICES = [
    ('haircut',    'hair',  40, 15, 'Haircut', 'Подстригване'),
    ('fade',       'hair',  50, 18, 'Skin fade or detailed cut', 'Преход до кожа или детайлно оформяне'),
    ('buzz',       'hair',  25, 10, 'Buzz cut, one length', 'Машинка, една дължина'),
    ('kids',       'hair',  30, 12, 'Kids haircut, under 12', 'Детско подстригване, до 12 г.'),
    ('beard',      'beard', 30, 10, 'Beard trim and shape', 'Подстригване и оформяне на брада'),
    ('shave',      'beard', 40, 15, 'Hot towel shave with a straight razor', 'Бръснене с гореща кърпа и бръснач'),
    ('head',       'beard', 30, 15, 'Head shave', 'Бръснене на глава'),
    ('hair_beard', 'combo', 60, 22, 'Haircut and beard', 'Подстригване и брада'),
    ('fade_beard', 'combo', 70, 25, 'Skin fade and beard', 'Преход до кожа и брада'),
    ('hair_shave', 'combo', 75, 28, 'Haircut and hot towel shave', 'Подстригване и бръснене с гореща кърпа'),
]
EXTRAS = [  # id, minutes, price, name EN, name BG
    ('wash', 10, 5,  'Hair wash and styling', 'Измиване и стилизиране'),
    ('trim', 10, 5,  'Eyebrow, ear and nose trim', 'Вежди, уши и нос'),
    ('grey', 30, 15, 'Grey blending (colour)', 'Прикриване на бели коси'),
]
GROUPS = [('hair', 'Hair', 'Коса'), ('beard', 'Beard and shave', 'Брада и бръснене'), ('combo', 'Combos', 'Комбинации')]
MINI = ['haircut', 'hair_beard', 'shave']   # the three prices shown on the front page

# Work wall: file, width, height, category, alt EN, alt BG   (category "shop" = the shop itself, no "book this cut" button)
WORK = [
    ('beard-scissors',     1600, 2409, 'cut',  'Black and white photo of a barber trimming a tattooed client\'s beard', 'Черно-бяла снимка на бръснар, който подрязва брадата на татуиран клиент'),
    ('leather-chair-brick',1600, 1063, 'shop', 'Leather barber chairs in front of a brick wall and mirrors', 'Кожени бръснарски столове пред тухлена стена и огледала'),
    ('haircut-focus',      1600, 2400, 'cut',  'Close-up of clippers fading the back of a client\'s head', 'Close-up на машинка, която оформя преход отзад на главата'),
    ('shaving',            1600, 1067, 'cut',  'Black and white photo of a client with shaving foam on his beard', 'Черно-бяла снимка на клиент с пяна за бръснене по брадата'),
    ('pendant-lamps',      1600, 2400, 'shop', 'A row of barber chairs under warm hanging lamps', 'Редица бръснарски столове под топли висящи лампи'),
    ('thinning-shears',    1600, 2400, 'cut',  'A barber thinning dark hair with a comb and shears', 'Бръснар изтънява тъмна коса с гребен и ножица'),
    ('straight-razor',     1600, 2397, 'cut',  'A tattooed hand cleaning a neckline with a straight razor', 'Татуирана ръка почиства линията на врата с бръснач'),
    ('clippers-tools',     1600, 1067, 'shop', 'Clippers, scissors, comb and grooming products on a dark mat', 'Машинки, ножици, гребен и продукти за грижа върху тъмна подложка'),
    ('scissors-cut',       1600, 2000, 'cut',  'A barber cutting a client\'s hair with scissors', 'Бръснар подстригва клиент с ножица'),
]

BARBER_TEXT = {  # id: (role EN, role BG, bio EN, bio BG)
    'theo':  ('Beards and straight razor', 'Бради и бръснач', 'Slow, careful work on beards and the hot towel shave. Book extra time and settle in.', 'Бавна, внимателна работа по брадите и бръсненето с гореща кърпа. Запази повече време и се отпусни.'),
    'ivan':  ('Skin fades and detail', 'Преходи до кожа и детайли', 'Clean lines and sharp edges. Bring a photo and he will match it.', 'Чисти линии и остри краища. Носиш снимка? Ще я пресъздаде.'),
    'marco': ('Classic cuts and scissors', 'Класически прически и ножица', 'Scissor work, short back and sides, and a calm chair.', 'Работа с ножица, класическо късо отзад и отстрани и спокоен стол.'),
}


def hours_text(lang):
    wd, we = OPEN_WEEKDAY.replace('-', ' – '), OPEN_WEEKEND.replace('-', ' – ')
    return ('Mon – Fri %s · Sat – Sun %s' % (wd, we)) if lang == 'en' else ('Пон – Пет %s · Съб – Нед %s' % (wd, we))


L = {
 'en': dict(
  lang='en', root='../', script='latin', other_href='../index.html', other_lang='bg', other_label='БГ', other_aria='Превключи на български',
  privacy_href='privacy.html', home_href='index.html',
  title='Hollis & Dane Barbers – cuts, shaves and beards in Plovdiv',
  desc='A barbershop in Plovdiv. See the chair board, pick the barber and the time that suits you, and book online. Haircuts, fades, beards and hot towel shaves.',
  skip='Skip to content', tagline='Barbers and hot towel shaves', nav_label='Main navigation', menu_btn='Menu',
  nav=[('#services', 'Prices'), ('#barbers', 'Barbers'), ('#book', 'Book'), ('#work', 'Work'), ('#reviews', 'Letters'), ('#visit', 'Visit')],
  cta='Book a chair',
  mast_edition='Plovdiv edition', mast_motto='Sharp cuts since the first customer',
  hero_kicker='Front page · Today\'s news from the chair',
  h1='Fresh cut.<em> Good news.</em>',
  lead='A neighbourhood barbershop with three chairs. See who is free on the chair board, pick your barber and your time, and sit down.',
  hero_cta2='See prices', open_loading='Checking opening hours…',
  photo_alt='A client leaning back in a barber chair while his beard is trimmed', photo_cap='A beard trim at chair two. Photo: example.',
  today_h='Today at the shop', popular_h='Most asked for',
  k_services='Price list', svc_h='What a visit costs', svc_p='Every service shows its time and its price. Press Book and the board opens with that service ready.',
  tab=dict(hair='Hair', beard='Beard and shave', combo='Combos', extras='Extras'), book='Book',
  price_note='Sample prices in euro, based on barbershops in Plovdiv.',
  k_team='The staff', team_h='Meet the barbers', team_p='Names and photos are examples. Book with the person you like, or take the first free chair on the board.', book_with='Book with {n}',
  k_book='Chair board', book_h='Pick a chair and a time', book_p='Choose a service and a day. Every column is a barber and every row a start time. Press a free square to take it.',
  s1='Your service', s2='Your day', s3='Free chairs', s4='Your details',
  f_service='Service', extras_h='Add extras', day_prev='Earlier days', day_next='Later days', checking='Checking free times…',
  board_label='Free chairs by barber and time', lg_free='Free', lg_taken='Taken', lg_sel='Your pick',
  pick_slot='Press a free square on the board to choose a chair.',
  f_name='Your name', f_phone='Phone', f_msg='Message (optional)', f_note='We use your details only to answer your booking.', f_priv='Privacy notice',
  chip_look='Cut you like', chip_remove='Remove', b_send='Book this chair',
  k_work='The wall', work_h='Recent work', work_p='A wall of cuts, beards and the shop. Press a photo to see it larger, or to book that cut.', open_photo='Open photo',
  k_rev='Letters', rev_h='Letters to the editor', rev_p='Example rating. Replace it with your real Google rating.',
  reviews=[('Best fade I have had in years. Clean work, and it still looked sharp three weeks later.', 'Skin fade'),
           ('I came with a photo and left with exactly that cut. Friendly, and no long waiting.', 'Haircut and beard'),
           ('The hot towel shave is worth it. Spotless shop and the price was clear before I booked.', 'Hot towel shave')],
  rev_by='Example client', rev_note='Example letters. Replace them with real Google reviews.',
  k_visit='Visit', visit_h='Find the shop', addr_l='Address', addr='Primer St. 1, Plovdiv', hours_l='Hours', phone_l='Phone', email_l='Email',
  map_t='The map is from OpenStreetMap and loads only if you choose.', map_btn='Show the map',
  k_faq='Questions', faq_h='Good to know',
  faq=[('Do I need an appointment?', 'We recommend one, so you do not have to wait. Choose a free square on the chair board. Walk-ins are welcome when a chair is free.'),
       ('How long does a visit take?', 'A haircut takes about 40 minutes, and a haircut with a beard about an hour. The price list shows the time for each service.'),
       ('Can I bring a photo of the cut I want?', 'Yes. Press a photo on the wall to book that cut, or show your own photo to your barber.'),
       ('Do you cut children\'s hair?', 'Yes. Children under 12 have their own price.'),
       ('What if I need to cancel or I am late?', 'Please tell us as early as you can, so we can offer your time to someone else. If you are more than 10 minutes late, the service may need to be shortened.'),
       ('Can I pay by card?', 'Yes, we accept cash and card.')],
  foot_tag='Barbers in Plovdiv', foot_priv='Privacy notice', admin_t='Demo back office', admin_href='../admin.html?lang=en',
  quick_label='Quick contact', q_call='Call', q_book='Book',
  dock_label='Colour scheme',
  lb_label='Photo', lb_close='Close', lb_prev='Previous photo', lb_next='Next photo', lb_request='Book this cut',
 ),
 'bg': dict(
  lang='bg', root='', script='cyrillic', other_href='en/index.html', other_lang='en', other_label='EN', other_aria='Switch to English',
  privacy_href='privacy.html', home_href='index.html',
  title='Hollis & Dane – бръснарница в Пловдив: подстригване, бръснене и брада',
  desc='Бръснарница в Пловдив. Виж таблото със столовете, избери бръснар и час и запази онлайн. Подстригване, преходи, брада и бръснене с гореща кърпа.',
  skip='Към съдържанието', tagline='Бръснарница и бръснене с гореща кърпа', nav_label='Основна навигация', menu_btn='Меню',
  nav=[('#services', 'Цени'), ('#barbers', 'Бръснари'), ('#book', 'Час'), ('#work', 'Работи'), ('#reviews', 'Писма'), ('#visit', 'Адрес')],
  cta='Запази стол',
  mast_edition='Пловдивско издание', mast_motto='Остри прически от първия клиент',
  hero_kicker='Първа страница · Новините от стола днес',
  h1='Свежа прическа.<em> Добри новини.</em>',
  lead='Квартална бръснарница с три стола. Виж кой е свободен на таблото, избери бръснар и час и седни.',
  hero_cta2='Виж цените', open_loading='Проверяваме работното време…',
  photo_alt='Клиент се е облегнал в бръснарския стол, докато му подрязват брадата', photo_cap='Оформяне на брада на втори стол. Снимка: пример.',
  today_h='Днес в салона', popular_h='Най-търсени',
  k_services='Ценова листа', svc_h='Колко струва едно посещение', svc_p='До всяка услуга има време и цена. Натисни Запази и таблото се отваря с избраната услуга.',
  tab=dict(hair='Коса', beard='Брада и бръснене', combo='Комбинации', extras='Допълнения'), book='Запази',
  price_note='Примерни цени в евро, по бръснарници в Пловдив.',
  k_team='Екипът', team_h='Запознай се с бръснарите', team_p='Имената и снимките са примерни. Запази при този, който ти харесва, или вземи първия свободен стол от таблото.', book_with='Запази при {n}',
  k_book='Табло със столове', book_h='Избери стол и час', book_p='Избери услуга и ден. Всяка колона е бръснар, всеки ред е начален час. Натисни свободно квадратче, за да го заемеш.',
  s1='Твоята услуга', s2='Твоят ден', s3='Свободни столове', s4='Твоите данни',
  f_service='Услуга', extras_h='Добави допълнения', day_prev='По-ранни дни', day_next='По-късни дни', checking='Проверяваме свободните часове…',
  board_label='Свободни столове по бръснар и час', lg_free='Свободно', lg_taken='Заето', lg_sel='Твоят избор',
  pick_slot='Натисни свободно квадратче на таблото, за да избереш стол.',
  f_name='Твоето име', f_phone='Телефон', f_msg='Съобщение (по желание)', f_note='Ползваме данните ти само за да отговорим на заявката ти.', f_priv='Политика за поверителност',
  chip_look='Прическа, която ти харесва', chip_remove='Премахни', b_send='Запази този стол',
  k_work='Стената', work_h='Последни работи', work_p='Стена от прически, бради и салона. Натисни снимка, за да я видиш по-голяма или да запазиш такава прическа.', open_photo='Отвори снимката',
  k_rev='Писма', rev_h='Писма до редактора', rev_p='Примерна оценка. Заменете я с истинската си оценка в Google.',
  reviews=[('Най-добрият преход от години. Чиста работа, а след три седмици още изглеждаше остро.', 'Преход до кожа'),
           ('Дойдох със снимка и излязох точно с такава прическа. Приятелска атмосфера и без дълго чакане.', 'Подстригване и брада'),
           ('Бръсненето с гореща кърпа си заслужава. Безупречен салон и цената беше ясна още преди да си запазя час.', 'Бръснене с гореща кърпа')],
  rev_by='Примерен клиент', rev_note='Примерни писма. Заменете ги с истински отзиви от Google.',
  k_visit='Адрес', visit_h='Намери салона', addr_l='Адрес', addr='ул. Примерна 1, Пловдив', hours_l='Работно време', phone_l='Телефон', email_l='Имейл',
  map_t='Картата е от OpenStreetMap и се зарежда само ако поискаш.', map_btn='Покажи картата',
  k_faq='Въпроси', faq_h='Добре е да знаеш',
  faq=[('Нужен ли е час?', 'Препоръчваме да запазиш час, за да не чакаш. Избери свободно квадратче на таблото. Приемаме и без час, когато има свободен стол.'),
       ('Колко време отнема посещението?', 'Подстригването отнема около 40 минути, а подстригване с брада – около час. В ценовата листа е посочено времето за всяка услуга.'),
       ('Мога ли да донеса снимка на прическата, която искам?', 'Да. Натисни снимка на стената, за да запазиш такава прическа, или покажи своя снимка на бръснаря.'),
       ('Подстригвате ли деца?', 'Да. Децата до 12 години имат собствена цена.'),
       ('Какво става, ако трябва да отменя или закъснея?', 'Предупреди ни възможно най-рано, за да предложим часа на друг клиент. При закъснение над 10 минути може да се наложи услугата да бъде съкратена.'),
       ('Мога ли да платя с карта?', 'Да, приемаме плащане в брой и с карта.')],
  foot_tag='Бръснарница в Пловдив', foot_priv='Политика за поверителност', admin_t='Демо админ панел', admin_href='admin.html',
  quick_label='Бърза връзка', q_call='Обади се', q_book='Запази',
  dock_label='Цветова схема',
  lb_label='Снимка', lb_close='Затвори', lb_prev='Предишна снимка', lb_next='Следваща снимка', lb_request='Запази тази прическа',
 ),
}

TEMPLATE = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'page_template.html'), encoding='utf-8').read()


def mins(m):
    return '%d min' % m if m < 60 else ('%d h' % (m // 60) if m % 60 == 0 else '%d h %d' % (m // 60, m % 60))


def mins_bg(m):
    return '%d мин' % m if m < 60 else ('%d ч' % (m // 60) if m % 60 == 0 else '%d ч %d мин' % (m // 60, m % 60))


def build(lang):
    d = L[lang]
    e = lambda s: escape(s, quote=True)
    root = d['root']
    bg = lang == 'bg'
    fm = mins_bg if bg else mins
    out = {'lang': lang, 'root': root, 'script': d['script']}
    keys = ['title', 'desc', 'skip', 'tagline', 'nav_label', 'menu_btn', 'cta', 'mast_edition', 'mast_motto', 'hero_kicker', 'lead', 'hero_cta2', 'open_loading',
            'photo_alt', 'photo_cap', 'today_h', 'popular_h', 'k_services', 'svc_h', 'svc_p', 'price_note', 'k_team', 'team_h', 'team_p',
            'k_book', 'book_h', 'book_p', 's1', 's2', 's3', 's4', 'f_service', 'extras_h', 'day_prev', 'day_next', 'checking', 'board_label', 'lg_free', 'lg_taken', 'lg_sel',
            'pick_slot', 'f_name', 'f_phone', 'f_msg', 'f_note', 'f_priv', 'chip_look', 'chip_remove', 'b_send',
            'k_work', 'work_h', 'work_p', 'k_rev', 'rev_h', 'rev_p', 'rev_note', 'k_visit', 'visit_h', 'addr_l', 'addr', 'hours_l', 'phone_l', 'email_l', 'map_t', 'map_btn',
            'k_faq', 'faq_h', 'foot_tag', 'foot_priv', 'admin_t', 'quick_label', 'q_call', 'q_book', 'dock_label',
            'lb_label', 'lb_close', 'lb_prev', 'lb_next', 'lb_request']
    for k in keys:
        out[k] = e(d[k])
    out['h1'] = d['h1']   # contains <em>
    out['other_href'] = d['other_href']; out['other_lang'] = d['other_lang']; out['other_label'] = d['other_label']; out['other_aria'] = e(d['other_aria'])
    out['privacy_href'] = d['privacy_href']; out['home_href'] = d['home_href']; out['admin_href'] = d['admin_href']
    out['nav_links'] = '\n      '.join('<a href="%s">%s</a>' % (h, e(t)) for h, t in d['nav'])

    sname = {sid: (b if bg else a) for sid, _g, _m, _p, a, b in SERVICES}
    # front page: three most asked-for prices
    out['mini_prices'] = '\n        '.join(
        '<li><span>%s <small>%s</small></span><b>%d €</b></li>' % (e(sname[sid]), e(fm(m)), p)
        for sid, _g, m, p, _a, _b in SERVICES if sid in MINI)

    # price list: one column per group, dotted leaders, a Book button on every row
    cols = []
    for g, ga, gb in GROUPS:
        rows = []
        for sid, sg, m, pr, en, bgn in SERVICES:
            if sg != g:
                continue
            nm = bgn if bg else en
            rows.append('<li><span class="pl-name">%s<small>%s</small></span><i class="dots" aria-hidden="true"></i><b class="pl-price">%d €</b>'
                        '<button class="pl-book" type="button" data-book data-service="%s" aria-label="%s: %s">%s</button></li>'
                        % (e(nm), e(fm(m)), pr, sid, e(d['book']), e(nm), e(d['book'])))
        cols.append('<section class="pl-col"><h3>%s</h3><ul>%s</ul></section>' % (e(gb if bg else ga), ''.join(rows)))
    xrows = ''.join('<li><span class="pl-name">%s<small>%s</small></span><i class="dots" aria-hidden="true"></i><b class="pl-price">%d €</b></li>'
                    % (e(bgn if bg else en), e(fm(m)), pr) for _x, m, pr, en, bgn in EXTRAS)
    cols.append('<section class="pl-col"><h3>%s</h3><ul>%s</ul></section>' % (e(d['tab']['extras']), xrows))
    out['pricelist'] = '\n        '.join(cols)

    # staff
    team = []
    for bid, name, photo, w, h in BARBERS:
        role_en, role_bg, bio_en, bio_bg = BARBER_TEXT[bid]
        team.append('<article class="bcard"><img src="%simages/stock/%s-800.jpg" width="800" height="%d" alt="" loading="lazy" decoding="async">'
                    '<div class="bcard-body"><h3>%s</h3><p class="role">%s</p><p>%s</p>'
                    '<button class="btn btn-line btn-sm" type="button" data-book data-barber="%s">%s</button></div></article>'
                    % (root, photo, round(800 * h / w), e(name), e(role_bg if bg else role_en), e(bio_bg if bg else bio_en), bid, e(d['book_with'].replace('{n}', name))))
    out['team'] = '\n        '.join(team)

    # work wall
    wall = []
    for photo, w, h, cat, alt_en, alt_bg in WORK:
        alt = e(alt_bg if bg else alt_en)
        wall.append('<button class="clip-item" type="button" data-cat="%s" data-full="%simages/stock/%s.jpg" aria-label="%s: %s">'
                    '<img src="%simages/stock/%s-800.jpg" width="800" height="%d" alt="%s" loading="lazy" decoding="async"></button>'
                    % (cat, root, photo, e(d['open_photo']), alt, root, photo, round(800 * h / w), alt))
    out['rail'] = '\n        '.join(wall)

    out['reviews'] = '\n        '.join(
        '<figure class="letter"><blockquote>%s</blockquote><figcaption><b>%s</b> · %s</figcaption></figure>' % (e(q), e(s), e(d['rev_by'])) for q, s in d['reviews'])
    out['faq'] = '\n          '.join('<details><summary>%s</summary><p>%s</p></details>' % (e(q), e(a)) for q, a in d['faq'])

    # booking form options
    opts = []
    for g, ga, gb in GROUPS:
        items = []
        for sid, sg, m, pr, en, bgn in SERVICES:
            if sg != g:
                continue
            nm = bgn if bg else en
            items.append('<option value="%s" data-name="%s" data-min="%d" data-price="%d"%s>%s · %s · %d €</option>'
                         % (sid, e(nm), m, pr, ' selected' if sid == 'haircut' else '', e(nm), e(fm(m)), pr))
        opts.append('<optgroup label="%s">%s</optgroup>' % (e(gb if bg else ga), ''.join(items)))
    out['svc_options'] = '\n                '.join(opts)
    out['extra_options'] = '\n              '.join(
        '<label class="xc"><input type="checkbox" name="extra" value="%s" data-name="%s" data-min="%d" data-price="%d"><span>%s <small>+ %s · + %d €</small></span></label>'
        % (xid, e(bgn if bg else en), m, pr, e(bgn if bg else en), e(fm(m)), pr) for xid, m, pr, en, bgn in EXTRAS)

    out['hours'] = e(hours_text(lang))
    out['phone'] = PHONE_DISPLAY; out['phone_href'] = PHONE_HREF; out['email'] = EMAIL; out['brand'] = e(BRAND); out['brand_json'] = BRAND.replace('&', '\u0026')
    sw = []
    for key, c1, c2, n_en, n_bg in SKINS:
        name = n_bg if bg else n_en
        sw.append('<button class="sw" type="button" data-skin="%s" data-name="%s" aria-label="%s: %s" title="%s" aria-pressed="%s" style="--s1:%s;--s2:%s"></button>'
                  % (key, e(name), e(d['dock_label']), e(name), e(name), 'true' if key == DEFAULT_SKIN[0] else 'false', c1, c2))
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
    'window.HOLLIS_CONFIG = {\n'
    '  mode: "%s",            /* "demo" = bookings are kept in this browser only; "live" = real API at apiBase (docs/API.md) */\n'
    '  apiBase: "%s",\n'
    '  hours: { weekday: ["%s", "%s"], weekend: ["%s", "%s"] },\n'
    '  barbers: [%s],        /* each barber can do one visit at a time */\n'
    '  slotMinutes: %d,\n'
    '  latency: [600, 1100]      /* demo only: pretend network delay in milliseconds */\n'
    '};\n'
) % (MODE, API_BASE, OPEN_WEEKDAY.split('-')[0], OPEN_WEEKDAY.split('-')[1], OPEN_WEEKEND.split('-')[0], OPEN_WEEKEND.split('-')[1],
     ', '.join('"%s"' % b[0] for b in BARBERS), SLOT_MINUTES)
os.makedirs(os.path.join(SHOP, 'js'), exist_ok=True)
open(os.path.join(SHOP, 'js', 'config.js'), 'w', encoding='utf-8').write(cfg)
print('config.js written')
