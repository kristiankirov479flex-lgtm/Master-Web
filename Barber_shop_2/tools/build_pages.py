import os, re
from html import escape

SHOP = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ---- Edit these placeholders for each barbershop ---------------------------------------------
OPEN_WEEKDAY = '09:00-20:00'      # opening and closing time, Mon - Fri
OPEN_WEEKEND = '10:00-18:00'      # opening and closing time, Sat - Sun
PHONE_DISPLAY = '+359 000 000 000'
PHONE_HREF = '+359000000000'
EMAIL = 'email@example.com'
# Booking system. 'demo' = the booking drawer talks to a mock server that keeps bookings in the visitor's browser.
# 'live' = it sends real HTTP requests to API_BASE (see docs/API.md). Written to js/config.js.
MODE = 'demo'
API_BASE = '/api'
SLOT_MINUTES = 30                 # gap between start times
BRAND = 'Foundry'
# ---------------------------------------------------------------------------------------------

SKINS = [  # key, colours for the swatch (background, accent), names
    ('brass',    '#0F0F0F', '#C8A24A', 'Black & Brass',          'Черно и месинг'),
    ('navy',     '#0E1A2B', '#D08A55', 'Midnight & Copper',      'Нощно синьо и мед'),
    ('forest',   '#12261F', '#D2A857', 'Forest & Gold',          'Гора и злато'),
    ('heritage', '#F4EFE6', '#B3261E', 'Barber Pole Heritage',   'Класика с червено'),
    ('graphite', '#1C1D1F', '#FF6A2B', 'Graphite & Orange',      'Графит и оранжево'),
]

# Barbers (names and photos are examples). id, name, photo file, width, height
BARBERS = [
    ('alex',  'Alex',  'white-shirt-cut', 1600, 1067),
    ('boris', 'Boris', 'haircut-barber',  1600, 2400),
    ('vlad',  'Vlad',  'haircut-shop-2',  1600, 2400),
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
# Extras: id, minutes, price, name EN, name BG   (shown in the price list and as options in the booking drawer)
EXTRAS = [
    ('wash', 10, 5,  'Hair wash and styling', 'Измиване и стилизиране'),
    ('trim', 10, 5,  'Eyebrow, ear and nose trim', 'Вежди, уши и нос'),
    ('grey', 30, 15, 'Grey blending (colour)', 'Прикриване на бели коси'),
]
GROUPS = [('hair', 'Hair', 'Коса'), ('beard', 'Beard and shave', 'Брада и бръснене'), ('combo', 'Combos', 'Комбинации')]

# Work rail: file, width, height, category, alt EN, alt BG   (category "shop" = the shop itself, no "book this cut" button)
WORK = [
    ('beard-scissors',     1600, 2409, 'cut',  'Black and white photo of a barber trimming a tattooed client\'s beard', 'Черно-бяла снимка на бръснар, който подрязва брадата на татуиран клиент'),
    ('haircut-focus',      1600, 2400, 'cut',  'Close-up of clippers fading the back of a client\'s head', 'Close-up на машинка, която оформя преход отзад на главата'),
    ('pendant-lamps',      1600, 2400, 'shop', 'A row of barber chairs under warm hanging lamps', 'Редица бръснарски столове под топли висящи лампи'),
    ('thinning-shears',    1600, 2400, 'cut',  'A barber thinning dark hair with a comb and shears', 'Бръснар изтънява тъмна коса с гребен и ножица'),
    ('shaving',            1600, 1067, 'cut',  'Black and white photo of a client with shaving foam on his beard', 'Черно-бяла снимка на клиент с пяна за бръснене по брадата'),
    ('straight-razor',     1600, 2397, 'cut',  'A tattooed hand cleaning a neckline with a straight razor', 'Татуирана ръка почиства линията на врата с бръснач'),
    ('leather-chair-brick',1600, 1063, 'shop', 'Leather barber chairs in front of a brick wall and mirrors', 'Кожени бръснарски столове пред тухлена стена и огледала'),
    ('scissors-cut',       1600, 2000, 'cut',  'A barber cutting a client\'s hair with scissors', 'Бръснар подстригва клиент с ножица'),
    ('chair-man',          1600, 1067, 'cut',  'A client leaning back in a barber chair while his beard is trimmed', 'Клиент се облегнал назад в бръснарския стол, докато му подрязват брадата'),
    ('clippers-tools',     1600, 1067, 'shop', 'Clippers, scissors, comb and grooming products on a dark mat', 'Машинки, ножици, гребен и продукти за грижа върху тъмна подложка'),
    ('haircut-shop',       1600, 1067, 'cut',  'A barber in black gloves shaping a client\'s beard in a dark shop', 'Бръснар с черни ръкавици оформя брада на клиент в тъмен салон'),
    ('black-silver-chair', 1600, 2000, 'shop', 'Black and silver vintage barber chairs in a dim shop', 'Черни и сребристи винтидж бръснарски столове в приглушено осветление'),
]

# Plans: name EN, name BG, price, [lines EN], [lines BG], popular
PLANS = [
    ('Regular', 'Редовен', 28, ['2 haircuts a month', 'Book any weekday', 'Pause any time'], ['2 подстригвания на месец', 'Запази час в кой да е делничен ден', 'Спри по всяко време'], False),
    ('Plus', 'Плюс', 42, ['2 haircuts and 2 beard trims', 'Priority booking', '10% off extras'], ['2 подстригвания и 2 оформяния на брада', 'Приоритетно записване', '10% отстъпка за допълнения'], True),
    ('Fresh', 'Свеж', 60, ['4 skin fades a month', 'Hot towel finish', 'Priority booking'], ['4 прехода до кожа на месец', 'Финиш с гореща кърпа', 'Приоритетно записване'], False),
]

BARBER_TEXT = {  # id: (role EN, role BG, bio EN, bio BG)
    'alex':  ('Skin fades and detail', 'Преходи до кожа и детайли', 'Clean lines and sharp edges. Brings a photo? He will match it.', 'Чисти линии и остри краища. Носиш снимка? Ще я пресъздаде.'),
    'boris': ('Classic cuts and beards', 'Класически прически и бради', 'Scissor work, beard shaping and a calm chair.', 'Работа с ножица, оформяне на брада и спокоен стол.'),
    'vlad':  ('Straight razor and hot towel', 'Бръснач и гореща кърпа', 'The slow, careful shave. Book extra time and relax.', 'Бавното, внимателно бръснене. Запази повече време и се отпусни.'),
}


def hours_text(lang):
    wd, we = OPEN_WEEKDAY.replace('-', ' – '), OPEN_WEEKEND.replace('-', ' – ')
    return ('Mon – Fri %s · Sat – Sun %s' % (wd, we)) if lang == 'en' else ('Пон – Пет %s · Съб – Нед %s' % (wd, we))


L = {
 'en': dict(
  lang='en', root='../', script='latin', other_href='../index.html', other_lang='bg', other_label='БГ', other_aria='Превключи на български',
  privacy_href='privacy.html', home_href='index.html',
  title='Foundry Barbers – haircuts, fades and beard care in Plovdiv',
  desc='Pick your barber, pick a time, and sit down. Haircuts, fades, beard trims and hot towel shaves in Plovdiv. Book online in four steps.',
  skip='Skip to content', tagline='barbers', nav_label='Main navigation', menu_btn='Menu',
  nav=[('#services', 'Services'), ('#barbers', 'Barbers'), ('#work', 'Work'), ('#plans', 'Plans'), ('#reviews', 'Reviews'), ('#visit', 'Visit')],
  cta='Book a chair',
  hero_est='Plovdiv', hero_kicker='Barbers and hot towel shaves',
  h1='Sharp cuts.<em>Clean lines.</em>',
  lead='Choose your barber, pick a time and sit down. Haircuts, fades, beard trims and hot towel shaves.',
  hero_cta2='See prices', open_loading='Checking opening hours…',
  tri_a='A barber shaping a bearded client with scissors and a comb', tri_b='Side view of a man with a full groomed beard and a styled quiff', tri_c='Close-up of clippers fading the back of a client\'s head',
  marquee=['Skin fades', 'Beards', 'Hot towel shaves', 'Kids cuts', 'Classic cuts', 'Straight razor'],
  k_services='Services', svc_h='Services and prices', svc_p='Every service shows its time and price. Press Book to start.',
  tab=dict(hair='Hair', beard='Beard and shave', combo='Combos', extras='Extras'), book='Book', ask='Ask about this plan',
  price_note='Sample prices in euro, based on barbershops in Plovdiv.',
  k_team='Barbers', team_h='Pick your barber', team_p='Names and photos are examples. Book with the person you like, or take the first free chair.', book_with='Book with {n}',
  k_work='Work', work_h='Recent work', work_p='Swipe through cuts, beards and the shop. Press a photo to book that cut.', rail_prev='Previous photos', rail_next='Next photos', open_photo='Open photo',
  k_plans='Plans', plans_h='Monthly plans', plans_p='Sample plans for regulars. Replace them with the shop\'s real offers.', per_month='/ month', popular='Most popular',
  k_rev='Reviews', rev_h='What clients say', rev_p='Example rating. Replace it with your real Google rating.',
  reviews=[('Best fade I have had in years. Clean work, and it still looked sharp three weeks later.', 'Skin fade'),
           ('I came with a photo and left with exactly that cut. Friendly, and no long waiting.', 'Haircut and beard'),
           ('The hot towel shave is worth it. Spotless shop and the price was clear before I booked.', 'Hot towel shave')],
  rev_by='Example client', rev_note='Example reviews. Replace them with real Google reviews.',
  k_visit='Visit', visit_h='Find the shop', addr_l='Address', addr='Primer St. 1, Plovdiv', hours_l='Hours', phone_l='Phone', email_l='Email',
  map_t='The map is from OpenStreetMap and loads only if you choose.', map_btn='Show the map',
  k_faq='Questions', faq_h='Good to know',
  faq=[('Do I need an appointment?', 'We recommend one, so you do not have to wait. Press Book a chair and choose a time. Walk-ins are welcome when a chair is free.'),
       ('How long does a visit take?', 'A haircut takes about 40 minutes, and a haircut with a beard about an hour. The price list shows the time for each service.'),
       ('Can I bring a photo of the cut I want?', 'Yes. Press a photo in the Work section to book that cut, or show your own photo to your barber.'),
       ('Do you cut children\'s hair?', 'Yes. Children under 12 have their own price.'),
       ('What if I need to cancel or I am late?', 'Please tell us as early as you can, so we can offer your time to someone else. If you are more than 10 minutes late, the service may need to be shortened.'),
       ('Can I pay by card?', 'Yes, we accept cash and card.')],
  foot_tag='Barbers in Plovdiv', foot_priv='Privacy notice', admin_t='Demo back office', admin_href='../admin.html?lang=en',
  quick_label='Quick contact', q_call='Call', q_book='Book',
  dock_label='Colour scheme',
  dr_title='Book a chair', dr_steps='Booking steps', s1='Service', s2='Barber', s3='Time', s4='Details',
  p1_h='Choose a service', extras_h='Add extras', p2_h='Choose a barber', p3_h='Pick a day and time', p4_h='Your details',
  any_b='Any barber', any_s='The first free chair', b_back='Back', b_next='Next', slot_pick_date='Pick a date to see free times.',
  f_date='Date', f_time='Time', f_name='Your name', f_phone='Phone', f_msg='Message (optional)', f_note='We use your details only to answer your booking.', f_priv='Privacy notice',
  chip_look='Cut you like', chip_remove='Remove',
  lb_label='Photo', lb_close='Close', lb_prev='Previous photo', lb_next='Next photo', lb_request='Book this cut',
 ),
 'bg': dict(
  lang='bg', root='', script='cyrillic', other_href='en/index.html', other_lang='en', other_label='EN', other_aria='Switch to English',
  privacy_href='privacy.html', home_href='index.html',
  title='Foundry – бръснарница в Пловдив: подстригване, преходи и брада',
  desc='Избери бръснар, избери час и седни. Подстригване, преходи, оформяне на брада и бръснене с гореща кърпа в Пловдив. Запази час онлайн в четири стъпки.',
  skip='Към съдържанието', tagline='бръснарница', nav_label='Основна навигация', menu_btn='Меню',
  nav=[('#services', 'Услуги'), ('#barbers', 'Бръснари'), ('#work', 'Работи'), ('#plans', 'Абонаменти'), ('#reviews', 'Отзиви'), ('#visit', 'Посети ни')],
  cta='Запази стол',
  hero_est='Пловдив', hero_kicker='Бръснарница и бръснене с гореща кърпа',
  h1='Остри линии.<em>Чист вид.</em>',
  lead='Избери бръснар, избери час и седни. Подстригване, преходи, оформяне на брада и бръснене с гореща кърпа.',
  hero_cta2='Виж цените', open_loading='Проверяваме работното време…',
  tri_a='Бръснар оформя брадата на клиент с ножица и гребен', tri_b='Мъж в профил с оформена гъста брада и стилна прическа', tri_c='Close-up на машинка, която оформя преход отзад на главата',
  marquee=['Преходи до кожа', 'Бради', 'Бръснене с гореща кърпа', 'Детски прически', 'Класически прически', 'Бръснач'],
  k_services='Услуги', svc_h='Услуги и цени', svc_p='До всяка услуга има време и цена. Натисни Запази, за да започнеш.',
  tab=dict(hair='Коса', beard='Брада и бръснене', combo='Комбинации', extras='Допълнения'), book='Запази', ask='Попитай за абонамента',
  price_note='Примерни цени в евро, по бръснарници в Пловдив.',
  k_team='Бръснари', team_h='Избери бръснар', team_p='Имената и снимките са примерни. Запази при този, който ти харесва, или вземи първия свободен стол.', book_with='Запази при {n}',
  k_work='Работи', work_h='Последни работи', work_p='Прелисти прически, бради и салона. Натисни снимка, за да запазиш такава прическа.', rail_prev='Предишни снимки', rail_next='Следващи снимки', open_photo='Отвори снимката',
  k_plans='Абонаменти', plans_h='Месечни абонаменти', plans_p='Примерни абонаменти за редовни клиенти. Заменете ги с истинските оферти на салона.', per_month='/ месец', popular='Най-избиран',
  k_rev='Отзиви', rev_h='Какво казват клиентите', rev_p='Примерна оценка. Заменете я с истинската си оценка в Google.',
  reviews=[('Най-добрият преход от години. Чиста работа, а след три седмици още изглеждаше остро.', 'Преход до кожа'),
           ('Дойдох със снимка и излязох точно с такава прическа. Приятелска атмосфера и без дълго чакане.', 'Подстригване и брада'),
           ('Бръсненето с гореща кърпа си заслужава. Безупречен салон и цената беше ясна още преди да си запазя час.', 'Бръснене с гореща кърпа')],
  rev_by='Примерен клиент', rev_note='Примерни отзиви. Заменете ги с истински отзиви от Google.',
  k_visit='Посети ни', visit_h='Намери салона', addr_l='Адрес', addr='ул. Примерна 1, Пловдив', hours_l='Работно време', phone_l='Телефон', email_l='Имейл',
  map_t='Картата е от OpenStreetMap и се зарежда само ако поискаш.', map_btn='Покажи картата',
  k_faq='Въпроси', faq_h='Добре е да знаеш',
  faq=[('Нужен ли е час?', 'Препоръчваме да запазиш час, за да не чакаш. Натисни Запази стол и избери час. Приемаме и без час, когато има свободен стол.'),
       ('Колко време отнема посещението?', 'Подстригването отнема около 40 минути, а подстригване с брада – около час. В ценовата листа е посочено времето за всяка услуга.'),
       ('Мога ли да донеса снимка на прическата, която искам?', 'Да. Натисни снимка в раздел Работи, за да запазиш такава прическа, или покажи своя снимка на бръснаря.'),
       ('Подстригвате ли деца?', 'Да. Децата до 12 години имат собствена цена.'),
       ('Какво става, ако трябва да отменя или закъснея?', 'Предупреди ни възможно най-рано, за да предложим часа на друг клиент. При закъснение над 10 минути може да се наложи услугата да бъде съкратена.'),
       ('Мога ли да платя с карта?', 'Да, приемаме плащане в брой и с карта.')],
  foot_tag='Бръснарница в Пловдив', foot_priv='Политика за поверителност', admin_t='Демо админ панел', admin_href='admin.html',
  quick_label='Бърза връзка', q_call='Обади се', q_book='Запази',
  dock_label='Цветова схема',
  dr_title='Запази стол', dr_steps='Стъпки на запазването', s1='Услуга', s2='Бръснар', s3='Час', s4='Данни',
  p1_h='Избери услуга', extras_h='Добави допълнения', p2_h='Избери бръснар', p3_h='Избери ден и час', p4_h='Твоите данни',
  any_b='Всеки бръснар', any_s='Първият свободен стол', b_back='Назад', b_next='Напред', slot_pick_date='Избери дата, за да видиш свободните часове.',
  f_date='Дата', f_time='Час', f_name='Твоето име', f_phone='Телефон', f_msg='Съобщение (по желание)', f_note='Ползваме данните ти само за да отговорим на заявката ти.', f_priv='Политика за поверителност',
  chip_look='Прическа, която ти харесва', chip_remove='Премахни',
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
    keys = ['title', 'desc', 'skip', 'tagline', 'nav_label', 'menu_btn', 'cta', 'hero_est', 'hero_kicker', 'lead', 'hero_cta2', 'open_loading', 'tri_a', 'tri_b', 'tri_c',
            'k_services', 'svc_h', 'svc_p', 'price_note', 'k_team', 'team_h', 'team_p', 'k_work', 'work_h', 'work_p', 'rail_prev', 'rail_next',
            'k_plans', 'plans_h', 'plans_p', 'k_rev', 'rev_h', 'rev_p', 'rev_note', 'k_visit', 'visit_h', 'addr_l', 'addr', 'hours_l', 'phone_l', 'email_l', 'map_t', 'map_btn',
            'k_faq', 'faq_h', 'foot_tag', 'foot_priv', 'admin_t', 'quick_label', 'q_call', 'q_book', 'dock_label',
            'dr_title', 'dr_steps', 's1', 's2', 's3', 's4', 'p1_h', 'extras_h', 'p2_h', 'p3_h', 'p4_h', 'b_back', 'b_next', 'slot_pick_date',
            'f_date', 'f_time', 'f_name', 'f_phone', 'f_msg', 'f_note', 'f_priv', 'chip_look', 'chip_remove', 'lb_label', 'lb_close', 'lb_prev', 'lb_next', 'lb_request']
    for k in keys:
        out[k] = e(d[k])
    out['h1'] = d['h1']   # contains <em>
    out['other_href'] = d['other_href']; out['other_lang'] = d['other_lang']; out['other_label'] = d['other_label']; out['other_aria'] = e(d['other_aria'])
    out['privacy_href'] = d['privacy_href']; out['home_href'] = d['home_href']; out['admin_href'] = d['admin_href']
    out['nav_links'] = '\n        '.join('<a href="%s">%s</a>' % (h, e(t)) for h, t in d['nav'])
    word = '<li>' + '</li><li>'.join(e(w) for w in d['marquee']) + '</li>'
    out['marquee'] = word

    # services: tabs + panels
    gname = {g: (b if bg else a) for g, a, b in GROUPS}
    tabs, panels = [], []
    order = [g for g, _a, _b in GROUPS] + ['extras']
    for n, g in enumerate(order):
        label = d['tab'][g]
        tabs.append('<button class="tab" type="button" role="tab" id="tab-%s" aria-controls="panel-%s" aria-selected="%s" tabindex="%s">%s</button>'
                    % (g, g, 'true' if n == 0 else 'false', '0' if n == 0 else '-1', e(label)))
        rows = []
        if g == 'extras':
            for xid, m, pr, en, bgn in EXTRAS:
                rows.append('<article class="svc"><div><h3>%s</h3><small>%s</small></div><span class="svc-price">%d €</span></article>' % (e(bgn if bg else en), e(fm(m)), pr))
        else:
            for sid, sg, m, pr, en, bgn in SERVICES:
                if sg != g:
                    continue
                rows.append('<article class="svc"><div><h3>%s</h3><small>%s</small></div><span class="svc-price">%d €</span>'
                            '<button class="btn btn-line btn-sm" type="button" data-book data-service="%s" aria-label="%s: %s">%s</button></article>'
                            % (e(bgn if bg else en), e(fm(m)), pr, sid, e(d['book']), e(bgn if bg else en), e(d['book'])))
        panels.append('<div class="svc-grid" role="tabpanel" id="panel-%s" aria-labelledby="tab-%s"%s>\n        %s\n      </div>'
                      % (g, g, '' if n == 0 else ' hidden', '\n        '.join(rows)))
    out['tabs'] = '\n        '.join(tabs)
    out['panels'] = '\n      '.join(panels)

    # team
    team = []
    for bid, name, photo, w, h in BARBERS:
        role_en, role_bg, bio_en, bio_bg = BARBER_TEXT[bid]
        team.append('<article class="bcard"><img src="%simages/stock/%s-800.jpg" width="800" height="%d" alt="" loading="lazy" decoding="async">'
                    '<div class="bcard-body"><h3>%s</h3><p class="role">%s</p><p>%s</p>'
                    '<button class="btn btn-main btn-sm" type="button" data-book data-barber="%s">%s</button></div></article>'
                    % (root, photo, round(800 * h / w), e(name), e(role_bg if bg else role_en), e(bio_bg if bg else bio_en), bid, e(d['book_with'].replace('{n}', name))))
    out['team'] = '\n        '.join(team)

    # work rail
    rail = []
    for photo, w, h, cat, alt_en, alt_bg in WORK:
        alt = e(alt_bg if bg else alt_en)
        rail.append('<button class="rail-item" type="button" data-cat="%s" data-full="%simages/stock/%s.jpg" aria-label="%s: %s">'
                    '<img src="%simages/stock/%s-800.jpg" width="800" height="%d" alt="%s" loading="lazy" decoding="async"></button>'
                    % (cat, root, photo, e(d['open_photo']), alt, root, photo, round(800 * h / w), alt))
    out['rail'] = '\n        '.join(rail)

    # plans
    plans = []
    for en, bgn, price, lines_en, lines_bg, pop in PLANS:
        lines = lines_bg if bg else lines_en
        plans.append('<article class="plan%s">%s<h3>%s</h3><p class="plan-price">%d €<small>%s</small></p><ul>%s</ul>'
                     '<a class="btn %s" href="tel:%s">%s</a></article>'
                     % (' pop' if pop else '', '<span class="plan-tag">%s</span>' % e(d['popular']) if pop else '', e(bgn if bg else en), price, e(d['per_month']),
                        ''.join('<li>%s</li>' % e(x) for x in lines), 'btn-main' if pop else 'btn-line', PHONE_HREF, e(d['ask'])))
    out['plans'] = '\n        '.join(plans)

    out['reviews'] = '\n        '.join(
        '<figure class="rev"><blockquote>%s</blockquote><figcaption><b>%s</b> · %s</figcaption></figure>' % (e(q), e(s), e(d['rev_by'])) for q, s in d['reviews'])
    out['faq'] = '\n          '.join('<details><summary>%s</summary><p>%s</p></details>' % (e(q), e(a)) for q, a in d['faq'])

    # booking drawer options
    opts = []
    for g, ga, gb in GROUPS:
        opts.append('<p class="dr-group">%s</p>' % e(gb if bg else ga))
        for sid, sg, m, pr, en, bgn in SERVICES:
            if sg != g:
                continue
            nm = bgn if bg else en
            opts.append('<label class="oc"><input type="radio" name="service" value="%s" data-name="%s" data-min="%d" data-price="%d"><span><b>%s</b><small>%s</small></span><span class="pr">%d €</span></label>'
                        % (sid, e(nm), m, pr, e(nm), e(fm(m)), pr))
    out['svc_options'] = '\n        '.join(opts)
    out['extra_options'] = '\n        '.join(
        '<label class="oc chk"><input type="checkbox" name="extra" value="%s" data-name="%s" data-min="%d" data-price="%d"><span><b>%s</b><small>+ %s</small></span><span class="pr">+ %d €</span></label>'
        % (xid, e(bgn if bg else en), m, pr, e(bgn if bg else en), e(fm(m)), pr) for xid, m, pr, en, bgn in EXTRAS)
    bopts = ['<label class="oc bar"><input type="radio" name="barber" value="any" data-name="%s" checked><span class="any" aria-hidden="true">?</span><span><b>%s</b><small>%s</small></span></label>'
             % (e(d['any_b']), e(d['any_b']), e(d['any_s']))]
    for bid, name, photo, w, h in BARBERS:
        role_en, role_bg, _a, _b = BARBER_TEXT[bid]
        bopts.append('<label class="oc bar"><input type="radio" name="barber" value="%s" data-name="%s"><img src="%simages/stock/%s-800.jpg" alt="" width="64" height="64" loading="lazy"><span><b>%s</b><small>%s</small></span></label>'
                     % (bid, e(name), root, photo, e(name), e(role_bg if bg else role_en)))
    out['barber_options'] = '\n        '.join(bopts)

    out['hours'] = e(hours_text(lang))
    out['phone'] = PHONE_DISPLAY; out['phone_href'] = PHONE_HREF; out['email'] = EMAIL; out['brand'] = BRAND
    sw = []
    for key, c1, c2, n_en, n_bg in SKINS:
        name = n_bg if bg else n_en
        sw.append('<button class="sw" type="button" data-skin="%s" data-name="%s" aria-label="%s: %s" title="%s" aria-pressed="%s" style="--s1:%s;--s2:%s"></button>'
                  % (key, e(name), e(d['dock_label']), e(name), e(name), 'true' if key == 'brass' else 'false', c1, c2))
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
    'window.FOUNDRY_CONFIG = {\n'
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
