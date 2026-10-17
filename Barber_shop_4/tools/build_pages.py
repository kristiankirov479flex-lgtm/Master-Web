import os, re
from html import escape

SHOP = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ---- Edit these placeholders for each barbershop ---------------------------------------------
OPEN_WEEKDAY = '09:00-21:00'      # opening and closing time, Mon - Fri
OPEN_WEEKEND = '10:00-19:00'      # opening and closing time, Sat - Sun
PHONE_DISPLAY = '+359 000 000 000'
PHONE_HREF = '+359000000000'
EMAIL = 'email@example.com'
# Booking system. 'demo' = the ticket builder talks to a mock server that keeps bookings in the visitor's browser.
# 'live' = it sends real HTTP requests to API_BASE (see docs/API.md). Written to js/config.js.
MODE = 'demo'
API_BASE = '/api'
SLOT_MINUTES = 15                 # gap between start times
BRAND = 'Bolt'
# ---------------------------------------------------------------------------------------------

SKINS = [  # key, colours for the swatch (background, accent), names
    ('volt',  '#0B0B0C', '#C6F432', 'Volt Lime',          'Електрик лайм'),
    ('ultra', '#15123B', '#FF5C9A', 'Ultra Pink',         'Ултра розово'),
    ('sun',   '#FFF1D6', '#C93A00', 'Sunny Orange',       'Слънчево оранжево'),
    ('ice',   '#0A1C26', '#4FE0F0', 'Ice Cyan',           'Ледено синьо'),
    ('mono',  '#F4F4F0', '#D6001C', 'Mono and Red',       'Черно-бяло и червено'),
]
DEFAULT_SKIN = SKINS[0]

# Barbers (names and photos are examples). id, name, photo file, width, height
BARBERS = [
    ('niko', 'Niko', 'haircut-barber', 1600, 2400),
    ('stan', 'Stan', 'scissors-cut',   1600, 2000),
    ('lex',  'Lex',  'haircut-focus',  1600, 2400),
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
]
EXTRAS = [  # id, minutes, price, name EN, name BG   (add-ons: can be added to anything)
    ('wash', 10, 5,  'Hair wash and styling', 'Измиване и стилизиране'),
    ('trim', 10, 5,  'Eyebrow, ear and nose trim', 'Вежди, уши и нос'),
    ('grey', 30, 15, 'Grey blending (colour)', 'Прикриване на бели коси'),
]
GROUPS = [('hair', 'Hair', 'Коса'), ('beard', 'Beard and shave', 'Брада и бръснене')]

# Work wall: file, width, height, category, alt EN, alt BG   (category "shop" = the shop itself, no "book this cut" button)
WORK = [
    ('beard-trim',         1600, 2400, 'cut',  'A barber trimming a client\'s beard with clippers', 'Бръснар подрязва брадата на клиент с машинка'),
    ('pendant-lamps',      1600, 2400, 'shop', 'A row of barber chairs under warm hanging lamps', 'Редица бръснарски столове под топли висящи лампи'),
    ('white-shirt-cut',    1600, 1067, 'cut',  'A barber in a white shirt cutting a client\'s hair', 'Бръснар в бяла риза подстригва клиент'),
    ('black-silver-chair', 1600, 2000, 'shop', 'Black and silver vintage barber chairs in a dim shop', 'Черни и сребристи винтидж бръснарски столове в приглушено осветление'),
    ('bearded-man',        1600, 2400, 'cut',  'Side view of a man with a full groomed beard and a styled quiff', 'Мъж в профил с оформена гъста брада и стилна прическа'),
    ('shaving',            1600, 1067, 'cut',  'Black and white photo of a client with shaving foam on his beard', 'Черно-бяла снимка на клиент с пяна за бръснене по брадата'),
    ('leather-chair-brick',1600, 1063, 'shop', 'Leather barber chairs in front of a brick wall and mirrors', 'Кожени бръснарски столове пред тухлена стена и огледала'),
    ('haircut-shop',       1600, 1067, 'cut',  'A barber in black gloves shaping a client\'s beard in a dark shop', 'Бръснар с черни ръкавици оформя брада на клиент в тъмен салон'),
]

BARBER_TEXT = {  # id: (role EN, role BG, bio EN, bio BG)
    'niko': ('Skin fades and detail', 'Преходи до кожа и детайли', 'Clean lines and sharp edges. Bring a photo and he will match it.', 'Чисти линии и остри краища. Носиш снимка? Ще я пресъздаде.'),
    'stan': ('Classic cuts and scissors', 'Класически прически и ножица', 'Scissor work, short back and sides, and a calm chair.', 'Работа с ножица, класическо късо отзад и отстрани и спокоен стол.'),
    'lex':  ('Beards and straight razor', 'Бради и бръснач', 'The slow, careful shave. Book extra time and relax.', 'Бавното, внимателно бръснене. Запази повече време и се отпусни.'),
}


def hours_text(lang):
    wd, we = OPEN_WEEKDAY.replace('-', ' – '), OPEN_WEEKEND.replace('-', ' – ')
    return ('Mon – Fri %s · Sat – Sun %s' % (wd, we)) if lang == 'en' else ('Пон – Пет %s · Съб – Нед %s' % (wd, we))


L = {
 'en': dict(
  lang='en', root='../', script='latin', other_href='../index.html', other_lang='bg', other_label='БГ', other_aria='Превключи на български',
  privacy_href='privacy.html', home_href='index.html',
  title='Bolt Barbers – fast fades and clean shaves in Plovdiv',
  desc='Build your visit in one minute: pick the services, the barber, the day and the time, and print your ticket. Fades, haircuts, beards and hot towel shaves in Plovdiv.',
  skip='Skip to content', tagline='Barbers · Plovdiv', nav_label='Main navigation', menu_btn='Menu',
  nav=[('#build', 'Book'), ('#barbers', 'Crew'), ('#work', 'Work'), ('#reviews', 'Notes'), ('#visit', 'Visit')],
  cta='Build my visit',
  hero_kicker='Open seven days',
  h1='Cut.<br>Book.<br><em>Go.</em>',
  lead='Fast fades, clean lines and hot towel shaves. Build your visit in a minute and walk out looking sharp.',
  hero_cta2='Meet the crew', open_loading='Checking opening hours…',
  stats_label='Quick facts', stats=[('3', 'chairs'), ('7', 'days a week'), ('40', 'min for a cut')],
  pic_a='A tattooed hand cleaning a neckline with a straight razor', pic_b='A barber thinning dark hair with a comb and shears', sticker='Walk-ins welcome',
  k_build='Book', build_h='Build your visit', build_p='Tap what you need. Your ticket on the right adds it up as you go.',
  a_h='Pick your services', b_h='Pick your barber', c_h='Pick a day and a time', d_h='Who is coming?',
  any_b='Any barber', any_s='The first free chair',
  checking='Pick services to see free times.', f_time='Time',
  f_name='Your name', f_phone='Phone', f_msg='Message (optional)', f_note='We use your details only to answer your booking.', f_priv='Privacy notice',
  chip_look='Cut you like', chip_remove='Remove',
  tk_h='Your ticket', tk_draft='Draft', total_l='Total', b_send='Print my ticket', addons='Add-ons',
  k_team='Crew', team_h='Meet the crew', team_p='Names and photos are examples. Pick a barber and your ticket remembers.', pick='Pick {n}',
  k_work='Work', work_h='Fresh out of the chair', work_p='Press a photo to see it larger, or to book that cut.', open_photo='Open photo',
  k_rev='Notes', rev_h='What clients say', rev_p='Example rating. Replace it with your real Google rating.',
  reviews=[('Best fade I have had in years. Clean work, and it still looked sharp three weeks later.', 'Skin fade'),
           ('I came with a photo and left with exactly that cut. Friendly, and no long waiting.', 'Haircut and beard'),
           ('The hot towel shave is worth it. Spotless shop and the price was clear before I booked.', 'Hot towel shave')],
  rev_by='Example client', rev_note='Example notes. Replace them with real Google reviews.',
  k_visit='Visit', visit_h='Find the shop', addr_l='Address', addr='Primer St. 1, Plovdiv', hours_l='Hours', phone_l='Phone', email_l='Email',
  map_t='The map is from OpenStreetMap and loads only if you choose.', map_btn='Show the map',
  k_faq='Questions', faq_h='Good to know',
  faq=[('Do I need an appointment?', 'We recommend one, so you do not have to wait. Build your visit above and print your ticket. Walk-ins are welcome when a chair is free.'),
       ('How long does a visit take?', 'A haircut takes about 40 minutes, and a haircut with a beard about an hour. Each tile shows its time, and your ticket adds them up.'),
       ('Can I bring a photo of the cut I want?', 'Yes. Press a photo in the Work section to book that cut, or show your own photo to your barber.'),
       ('Do you cut children\'s hair?', 'Yes. Children under 12 have their own price.'),
       ('What if I need to cancel or I am late?', 'Please tell us as early as you can, so we can offer your time to someone else. If you are more than 10 minutes late, the service may need to be shortened.'),
       ('Can I pay by card?', 'Yes, we accept cash and card.')],
  foot_tag='Barbers in Plovdiv', foot_priv='Privacy notice', admin_t='Demo back office', admin_href='../admin.html?lang=en',
  quick_label='Quick contact', q_call='Call', q_ticket='Ticket',
  dock_label='Colour scheme',
  lb_label='Photo', lb_close='Close', lb_prev='Previous photo', lb_next='Next photo', lb_request='Book this cut',
 ),
 'bg': dict(
  lang='bg', root='', script='cyrillic', other_href='en/index.html', other_lang='en', other_label='EN', other_aria='Switch to English',
  privacy_href='privacy.html', home_href='index.html',
  title='Bolt – бръснарница в Пловдив: бързи преходи и чисто бръснене',
  desc='Направи си посещението за минута: избери услугите, бръснаря, деня и часа и отпечатай билета си. Преходи, подстригване, брада и бръснене с гореща кърпа в Пловдив.',
  skip='Към съдържанието', tagline='Бръснарница · Пловдив', nav_label='Основна навигация', menu_btn='Меню',
  nav=[('#build', 'Час'), ('#barbers', 'Екип'), ('#work', 'Работи'), ('#reviews', 'Отзиви'), ('#visit', 'Адрес')],
  cta='Подреди посещението',
  hero_kicker='Отворено всеки ден',
  h1='Подстрижи.<br>Запази.<br><em>Тръгвай.</em>',
  lead='Бързи преходи, чисти линии и бръснене с гореща кърпа. Подреди посещението си за минута и излез с остър вид.',
  hero_cta2='Запознай се с екипа', open_loading='Проверяваме работното време…',
  stats_label='Накратко', stats=[('3', 'стола'), ('7', 'дни в седмицата'), ('40', 'мин за подстригване')],
  pic_a='Татуирана ръка почиства линията на врата с бръснач', pic_b='Бръснар изтънява тъмна коса с гребен и ножица', sticker='Приемаме и без час',
  k_build='Час', build_h='Подреди посещението си', build_p='Натисни каквото ти трябва. Билетът отдясно събира сметката в движение.',
  a_h='Избери услуги', b_h='Избери бръснар', c_h='Избери ден и час', d_h='Кой идва?',
  any_b='Всеки бръснар', any_s='Първият свободен стол',
  checking='Избери услуги, за да видиш свободните часове.', f_time='Час',
  f_name='Твоето име', f_phone='Телефон', f_msg='Съобщение (по желание)', f_note='Ползваме данните ти само за да отговорим на заявката ти.', f_priv='Политика за поверителност',
  chip_look='Прическа, която ти харесва', chip_remove='Премахни',
  tk_h='Твоят билет', tk_draft='Чернова', total_l='Общо', b_send='Отпечатай билета', addons='Допълнения',
  k_team='Екип', team_h='Запознай се с екипа', team_p='Имената и снимките са примерни. Избери бръснар и билетът ти ще го запомни.', pick='Избери {n}',
  k_work='Работи', work_h='Току-що от стола', work_p='Натисни снимка, за да я видиш по-голяма или да запазиш такава прическа.', open_photo='Отвори снимката',
  k_rev='Отзиви', rev_h='Какво казват клиентите', rev_p='Примерна оценка. Заменете я с истинската си оценка в Google.',
  reviews=[('Най-добрият преход от години. Чиста работа, а след три седмици още изглеждаше остро.', 'Преход до кожа'),
           ('Дойдох със снимка и излязох точно с такава прическа. Приятелска атмосфера и без дълго чакане.', 'Подстригване и брада'),
           ('Бръсненето с гореща кърпа си заслужава. Безупречен салон и цената беше ясна още преди да си запазя час.', 'Бръснене с гореща кърпа')],
  rev_by='Примерен клиент', rev_note='Примерни отзиви. Заменете ги с истински отзиви от Google.',
  k_visit='Адрес', visit_h='Намери салона', addr_l='Адрес', addr='ул. Примерна 1, Пловдив', hours_l='Работно време', phone_l='Телефон', email_l='Имейл',
  map_t='Картата е от OpenStreetMap и се зарежда само ако поискаш.', map_btn='Покажи картата',
  k_faq='Въпроси', faq_h='Добре е да знаеш',
  faq=[('Нужен ли е час?', 'Препоръчваме да запазиш час, за да не чакаш. Подреди посещението по-горе и отпечатай билета си. Приемаме и без час, когато има свободен стол.'),
       ('Колко време отнема посещението?', 'Подстригването отнема около 40 минути, а подстригване с брада – около час. Всяка плочка показва времето си, а билетът ги събира.'),
       ('Мога ли да донеса снимка на прическата, която искам?', 'Да. Натисни снимка в раздел Работи, за да запазиш такава прическа, или покажи своя снимка на бръснаря.'),
       ('Подстригвате ли деца?', 'Да. Децата до 12 години имат собствена цена.'),
       ('Какво става, ако трябва да отменя или закъснея?', 'Предупреди ни възможно най-рано, за да предложим часа на друг клиент. При закъснение над 10 минути може да се наложи услугата да бъде съкратена.'),
       ('Мога ли да платя с карта?', 'Да, приемаме плащане в брой и с карта.')],
  foot_tag='Бръснарница в Пловдив', foot_priv='Политика за поверителност', admin_t='Демо админ панел', admin_href='admin.html',
  quick_label='Бърза връзка', q_call='Обади се', q_ticket='Билет',
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
    keys = ['title', 'desc', 'skip', 'tagline', 'nav_label', 'menu_btn', 'cta', 'hero_kicker', 'lead', 'hero_cta2', 'open_loading', 'stats_label',
            'pic_a', 'pic_b', 'sticker', 'k_build', 'build_h', 'build_p', 'a_h', 'b_h', 'c_h', 'd_h', 'checking', 'f_time',
            'f_name', 'f_phone', 'f_msg', 'f_note', 'f_priv', 'chip_look', 'chip_remove', 'tk_h', 'tk_draft', 'total_l', 'b_send',
            'k_team', 'team_h', 'team_p', 'k_work', 'work_h', 'work_p', 'k_rev', 'rev_h', 'rev_p', 'rev_note', 'k_visit', 'visit_h', 'addr_l', 'addr', 'hours_l', 'phone_l', 'email_l', 'map_t', 'map_btn',
            'k_faq', 'faq_h', 'foot_tag', 'foot_priv', 'admin_t', 'quick_label', 'q_call', 'q_ticket', 'dock_label',
            'lb_label', 'lb_close', 'lb_prev', 'lb_next', 'lb_request']
    for k in keys:
        out[k] = e(d[k])
    out['h1'] = d['h1']   # contains <br> and <em>
    out['other_href'] = d['other_href']; out['other_lang'] = d['other_lang']; out['other_label'] = d['other_label']; out['other_aria'] = e(d['other_aria'])
    out['privacy_href'] = d['privacy_href']; out['home_href'] = d['home_href']; out['admin_href'] = d['admin_href']
    out['nav_links'] = '\n      '.join('<a href="%s"><b>%02d</b>%s</a>' % (h, i + 1, e(t)) for i, (h, t) in enumerate(d['nav']))
    out['stats'] = '\n          '.join('<li><b>%s</b><span>%s</span></li>' % (e(a), e(b)) for a, b in d['stats'])

    # service tiles: toggles you can combine
    tiles = []
    for g, ga, gb in GROUPS:
        items = []
        for sid, sg, m, pr, en, bgn in SERVICES:
            if sg != g:
                continue
            nm = bgn if bg else en
            items.append('<label class="tile"><input type="checkbox" name="svc" value="%s" data-name="%s" data-min="%d" data-price="%d"><span class="t-name">%s</span><span class="t-meta">%s</span><b class="t-price">%d €</b></label>'
                         % (sid, e(nm), m, pr, e(nm), e(fm(m)), pr))
        tiles.append('<p class="g-h">%s</p><div class="tiles">%s</div>' % (e(gb if bg else ga), ''.join(items)))
    items = []
    for xid, m, pr, en, bgn in EXTRAS:
        nm = bgn if bg else en
        items.append('<label class="tile small"><input type="checkbox" name="svc" value="%s" data-name="%s" data-min="%d" data-price="%d" data-extra="1"><span class="t-name">%s</span><span class="t-meta">+ %s</span><b class="t-price">+ %d €</b></label>'
                     % (xid, e(nm), m, pr, e(nm), e(fm(m)), pr))
    tiles.append('<p class="g-h">%s</p><div class="tiles">%s</div>' % (e(d['addons']), ''.join(items)))
    out['svc_tiles'] = '\n            '.join(tiles)

    # barber picker
    bopts = ['<label class="pk"><input type="radio" name="barber" value="any" data-name="%s" checked><span class="any" aria-hidden="true">?</span><span class="pk-t"><b>%s</b><small>%s</small></span></label>'
             % (e(d['any_b']), e(d['any_b']), e(d['any_s']))]
    for bid, name, photo, w, h in BARBERS:
        role_en, role_bg, _a, _b = BARBER_TEXT[bid]
        bopts.append('<label class="pk"><input type="radio" name="barber" value="%s" data-name="%s"><img src="%simages/stock/%s-800.jpg" alt="" width="56" height="56" loading="lazy"><span class="pk-t"><b>%s</b><small>%s</small></span></label>'
                     % (bid, e(name), root, photo, e(name), e(role_bg if bg else role_en)))
    out['barber_options'] = '\n              '.join(bopts)

    # crew
    team = []
    for bid, name, photo, w, h in BARBERS:
        role_en, role_bg, bio_en, bio_bg = BARBER_TEXT[bid]
        team.append('<article class="crew-card"><img src="%simages/stock/%s-800.jpg" width="800" height="%d" alt="" loading="lazy" decoding="async">'
                    '<div class="crew-body"><h3>%s</h3><p class="role">%s</p><p>%s</p>'
                    '<button class="btn btn-main btn-sm" type="button" data-book data-barber="%s">%s</button></div></article>'
                    % (root, photo, round(800 * h / w), e(name), e(role_bg if bg else role_en), e(bio_bg if bg else bio_en), bid, e(d['pick'].replace('{n}', name))))
    out['team'] = '\n        '.join(team)

    # work wall
    wall = []
    for photo, w, h, cat, alt_en, alt_bg in WORK:
        alt = e(alt_bg if bg else alt_en)
        wall.append('<button class="w-item" type="button" data-cat="%s" data-full="%simages/stock/%s.jpg" aria-label="%s: %s">'
                    '<img src="%simages/stock/%s-800.jpg" width="800" height="%d" alt="%s" loading="lazy" decoding="async"></button>'
                    % (cat, root, photo, e(d['open_photo']), alt, root, photo, round(800 * h / w), alt))
    out['rail'] = '\n        '.join(wall)

    out['reviews'] = '\n        '.join(
        '<figure class="note"><blockquote>%s</blockquote><figcaption><b>%s</b> · %s</figcaption></figure>' % (e(q), e(s), e(d['rev_by'])) for q, s in d['reviews'])
    out['faq'] = '\n          '.join('<details><summary>%s</summary><p>%s</p></details>' % (e(q), e(a)) for q, a in d['faq'])

    out['hours'] = e(hours_text(lang))
    out['phone'] = PHONE_DISPLAY; out['phone_href'] = PHONE_HREF; out['email'] = EMAIL; out['brand'] = e(BRAND)
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
    'window.BOLT_CONFIG = {\n'
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
