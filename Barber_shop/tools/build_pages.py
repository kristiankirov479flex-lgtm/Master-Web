import os, re, json
from html import escape

SHOP = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ---- Edit these placeholders for each barbershop ---------------------------------------------
OPEN_WEEKDAY = '09:00-20:00'      # opening and closing time, Mon - Fri
OPEN_WEEKEND = '10:00-18:00'      # opening and closing time, Sat - Sun
PHONE_DISPLAY = '+359 000 000 000'
PHONE_HREF = '+359000000000'
EMAIL = 'email@example.com'
# Request system. 'demo' = the form talks to a mock server that stores requests in the visitor's browser.
# 'live' = it sends real HTTP requests to API_BASE (see docs/API.md). Written to js/config.js.
MODE = 'demo'
API_BASE = '/api'
CAPACITY = 2                      # visits that can run at the same time (number of chairs / barbers)
SLOT_MINUTES = 30                 # gap between start times
BRAND = 'Ironwood'
# ---------------------------------------------------------------------------------------------

SKINS = [  # key, colours for the swatch (background, accent), names
    ('brass',    '#0F0F0F', '#C8A24A', 'Black & Brass',          'Черно и месинг'),
    ('navy',     '#0E1A2B', '#D08A55', 'Midnight & Copper',      'Нощно синьо и мед'),
    ('forest',   '#12261F', '#D2A857', 'Forest & Gold',          'Гора и злато'),
    ('heritage', '#F4EFE6', '#B3261E', 'Barber Pole Heritage',   'Класика с червено'),
    ('graphite', '#1C1D1F', '#FF6A2B', 'Graphite & Orange',      'Графит и оранжево'),
]

# file, cat, width, height, alt_en, alt_bg   (photos: images/stock, see images/CREDITS.md)
GALLERY = [
    ('haircut-barber',    'cuts',   1600, 2400, 'A barber in a hat and suspenders cutting a client\'s hair', 'Бръснар с шапка и тиранти подстригва клиент'),
    ('beard-trim',        'beards', 1600, 2400, 'A barber shaping a bearded client with scissors and a comb', 'Бръснар оформя брада с ножица и гребен'),
    ('pendant-lamps',     'shop',   1600, 2400, 'A row of barber chairs under warm hanging lamps', 'Редица бръснарски столове под топли висящи лампи'),
    ('haircut-focus',     'cuts',   1600, 2400, 'Close-up of clippers fading the back of a client\'s head', 'Close-up на машинка, която оформя преход отзад на главата'),
    ('shaving',           'beards', 1600, 1067, 'Black and white photo of a client with shaving foam on his beard', 'Черно-бяла снимка на клиент с пяна за бръснене по брадата'),
    ('bearded-man',       'beards', 1600, 2400, 'Side view of a man with a full groomed beard and a styled quiff', 'Мъж в профил с оформена гъста брада и стилна прическа'),
    ('leather-chair-brick','shop',  1600, 1063, 'Leather barber chairs in front of a brick wall and mirrors', 'Кожени бръснарски столове пред тухлена стена и огледала'),
    ('thinning-shears',   'cuts',   1600, 2400, 'A barber thinning dark hair with a comb and shears', 'Бръснар изтънява тъмна коса с гребен и ножица'),
    ('beard-scissors',    'beards', 1600, 2409, 'Black and white photo of a barber trimming a tattooed client\'s beard', 'Черно-бяла снимка на бръснар, който подрязва брадата на татуиран клиент'),
    ('haircut-shop-2',    'cuts',   1600, 2400, 'A barber in a cap cutting a young man\'s hair', 'Бръснар с шапка подстригва млад мъж'),
    ('clippers-tools',    'shop',   1600, 1067, 'Clippers, scissors, comb and grooming products on a dark mat', 'Машинки, ножици, гребен и продукти за грижа върху тъмна подложка'),
    ('white-shirt-cut',   'cuts',   1600, 1067, 'A barber in a white shirt giving a client a short fade', 'Бръснар в бяла риза прави къс преход на клиент'),
    ('chair-man',         'beards', 1600, 1067, 'A client leaning back in a barber chair while his beard is trimmed', 'Клиент се обляга назад в бръснарския стол, докато му подрязват брадата'),
    ('black-silver-chair','shop',   1600, 2000, 'Black and silver vintage barber chairs in a dim shop', 'Черни и сребристи винтидж бръснарски столове в приглушено осветление'),
    ('straight-razor',    'cuts',   1600, 2397, 'A tattooed hand cleaning a neckline with a straight razor', 'Татуирана ръка почиства линията на врата с бръснач'),
    ('haircut-shop',      'beards', 1600, 1067, 'A barber in black gloves shaping a client\'s beard in a dark shop', 'Бръснар с черни ръкавици оформя брада на клиент в тъмен салон'),
    ('scissors-cut',      'cuts',   1600, 2000, 'A barber cutting a client\'s hair with scissors', 'Бръснар подстригва клиент с ножица'),
]

# group title, [(name, time text, price text, (min minutes, max minutes))]   Minutes drive the time list in the form.
MENU_EN = [
    ('Hair', [
        ('Haircut', '40 min', '15 €', (40, 40)),
        ('Skin fade or detailed cut', '50 min', '18 €', (50, 50)),
        ('Buzz cut, one length', '25 min', '10 €', (25, 25)),
        ('Kids haircut, under 12', '30 min', '12 €', (30, 30))]),
    ('Beard and shave', [
        ('Beard trim and shape', '30 min', '10 €', (30, 30)),
        ('Hot towel shave with a straight razor', '40 min', '15 €', (40, 40)),
        ('Head shave', '30 min', '15 €', (30, 30))]),
    ('Combinations', [
        ('Haircut and beard', '1 h', '22 €', (60, 60)),
        ('Skin fade and beard', '1 h 10', '25 €', (70, 70)),
        ('Haircut and hot towel shave', '1 h 15', '28 €', (75, 75))]),
    ('Extras', [
        ('Hair wash and styling', '10 min', '5 €', (10, 10)),
        ('Eyebrow, ear and nose trim', '10 min', '5 €', (10, 10)),
        ('Grey blending (colour)', '30 – 45 min', 'from 15 €', (30, 45))]),
]
MENU_BG = [
    ('Коса', [
        ('Подстригване', '40 мин', '15 €', (40, 40)),
        ('Преход до кожа или детайлно оформяне', '50 мин', '18 €', (50, 50)),
        ('Машинка, една дължина', '25 мин', '10 €', (25, 25)),
        ('Детско подстригване, до 12 г.', '30 мин', '12 €', (30, 30))]),
    ('Брада и бръснене', [
        ('Подстригване и оформяне на брада', '30 мин', '10 €', (30, 30)),
        ('Бръснене с гореща кърпа и бръснач', '40 мин', '15 €', (40, 40)),
        ('Бръснене на глава', '30 мин', '15 €', (30, 30))]),
    ('Комбинации', [
        ('Подстригване и брада', '1 ч', '22 €', (60, 60)),
        ('Преход до кожа и брада', '1 ч 10 мин', '25 €', (70, 70)),
        ('Подстригване и бръснене с гореща кърпа', '1 ч 15 мин', '28 €', (75, 75))]),
    ('Допълнения', [
        ('Измиване и стилизиране', '10 мин', '5 €', (10, 10)),
        ('Оформяне на вежди, уши и нос', '10 мин', '5 €', (10, 10)),
        ('Прикриване на бели коси (боя)', '30 – 45 мин', 'от 15 €', (30, 45))]),
]

# ---- "Plan your visit" estimator (numbers are sample values based on Plovdiv barbershops) ----------
# opt = the menu item the form selects (must match a menu name above)
PLAN_GROUPS = [('hair', 'Hair', 'Коса'), ('beard', 'Beard and shave', 'Брада и бръснене'), ('combo', 'Combinations', 'Комбинации')]
PLAN_SERVICES = [
    dict(id='haircut', group='hair', addons=['wash', 'trim', 'grey'],
         label=('Haircut', 'Подстригване'),
         lengths=[dict(id='classic', price=15, minutes=40, label=('Classic cut', 'Класическа'), opt=('Haircut', 'Подстригване')),
                  dict(id='fade', price=18, minutes=50, label=('Skin fade or detailed', 'Преход до кожа или детайлна'), opt=('Skin fade or detailed cut', 'Преход до кожа или детайлно оформяне'))]),
    dict(id='buzz', group='hair', pmin=10, pmax=10, mmin=25, mmax=25, addons=['wash', 'trim'],
         label=('Buzz cut', 'Машинка'), opt=('Buzz cut, one length', 'Машинка, една дължина')),
    dict(id='kids', group='hair', pmin=12, pmax=12, mmin=30, mmax=30, addons=[],
         label=('Kids haircut', 'Детско подстригване'), opt=('Kids haircut, under 12', 'Детско подстригване, до 12 г.')),
    dict(id='beard', group='beard', pmin=10, pmax=10, mmin=30, mmax=30, addons=['trim'],
         label=('Beard trim', 'Оформяне на брада'), opt=('Beard trim and shape', 'Подстригване и оформяне на брада')),
    dict(id='shave', group='beard', pmin=15, pmax=15, mmin=40, mmax=40, addons=['trim'],
         label=('Hot towel shave', 'Бръснене с гореща кърпа'), opt=('Hot towel shave with a straight razor', 'Бръснене с гореща кърпа и бръснач')),
    dict(id='head', group='beard', pmin=15, pmax=15, mmin=30, mmax=30, addons=[],
         label=('Head shave', 'Бръснене на глава'), opt=('Head shave', 'Бръснене на глава')),
    dict(id='hair_beard', group='combo', pmin=22, pmax=22, mmin=60, mmax=60, addons=['wash', 'trim', 'grey'],
         label=('Haircut and beard', 'Подстригване и брада'), opt=('Haircut and beard', 'Подстригване и брада')),
    dict(id='fade_beard', group='combo', pmin=25, pmax=25, mmin=70, mmax=70, addons=['wash', 'trim', 'grey'],
         label=('Skin fade and beard', 'Преход и брада'), opt=('Skin fade and beard', 'Преход до кожа и брада')),
    dict(id='hair_shave', group='combo', pmin=28, pmax=28, mmin=75, mmax=75, addons=['wash', 'trim'],
         label=('Haircut and hot towel shave', 'Подстригване и бръснене'), opt=('Haircut and hot towel shave', 'Подстригване и бръснене с гореща кърпа')),
]
PLAN_ADDONS = [
    dict(id='wash', price=5, minutes=10, label=('Hair wash and styling', 'Измиване и стилизиране')),
    dict(id='trim', price=5, minutes=10, label=('Eyebrow, ear and nose trim', 'Вежди, уши и нос')),
    dict(id='grey', price=15, minutes=30, label=('Grey blending (colour)', 'Прикриване на бели коси')),
]


def hours_text(lang):
    wd, we = OPEN_WEEKDAY.replace('-', ' – '), OPEN_WEEKEND.replace('-', ' – ')
    return ('Mon – Fri %s · Sat – Sun %s' % (wd, we)) if lang == 'en' else ('Пон – Пет %s · Съб – Нед %s' % (wd, we))


L = {
 'en': dict(
  lang='en', root='../', script='latin', other_href='../index.html', other_lang='bg', other_label='БГ', other_aria='Превключи на български',
  privacy_href='privacy.html', home_href='index.html',
  title='Ironwood Barbershop – haircuts and beard care in Plovdiv',
  desc='Haircuts, fades, beard trims and hot towel shaves in a classic barbershop in Plovdiv. See the work and prices, and send a request for a time.',
  skip='Skip to content', tagline='barbershop', nav_label='Main navigation', menu_btn='Menu',
  nav=[('#prices', 'Prices'), ('#gallery', 'Gallery'), ('#reviews', 'Reviews'), ('#faq', 'Questions'), ('#contact', 'Contact')],
  cta='Book a chair',
  h1='Sharp cuts. Clean lines.',
  lead='Haircuts, fades, beard trims and hot towel shaves in a classic barbershop in Plovdiv. See the work, check the prices, send a request.',
  hero_cta2='See prices', hero_meta='Plovdiv · open every day', hero_chip='Cuts · Fades · Beards',
  hero_alt='A barber shaping a bearded client with scissors and a comb', hero_side_alt='Barber chairs under warm hanging lamps',
  promise_h='What to expect',
  promise=[('Sharp and clean', 'Tools are cleaned and disinfected between clients, and every shave starts with a fresh blade.'),
           ('On time', 'You book a time, and your barber is ready at that time. No long waiting.'),
           ('Clear prices', 'Every service has a price and a time, so there are no surprises.')],
  gal_h='Recent work', gal_p='Cuts, beards and the shop. Filter by type, and press a photo to ask for that cut.', gal_filter='Filter photos',
  f_all='All', f_cuts='Cuts', f_beards='Beards', f_shop='The shop', shown='Photos shown: 17', open_photo='Open photo',
  lb_label='Photo', lb_close='Close', lb_prev='Previous photo', lb_next='Next photo', lb_request='Request this cut',
  price_h='Services and prices', price_p='Every service has a time and a price. Not sure what you need? Send us a photo and we will help.',
  price_cta='Plan your visit',
  price_note='Sample prices in euro, based on barbershops in Plovdiv.', menu_alt='Clippers, scissors, a comb and grooming products on a dark mat', menu=MENU_EN,
  plan_h='Plan your visit', plan_p='Choose what you need to see an estimated price and time. Then add it to your request, and we will only offer start times that fit before closing.',
  plan_l_service='What do you need?', plan_l_length='Style', plan_l_addons='Extras',
  plan_empty='Choose a service to see the estimate.', plan_price='Estimated price', plan_time='Estimated time',
  plan_req_note='Plus extras priced on request.', plan_add='Add to my request',
  plan_fine='Sample prices. We confirm the final price and time when we reply.', plan_on_request='price on request',
  rev_h='What clients say', rev_p='Short notes from people who book with us.', rev_note='Example reviews. Replace them with real Google reviews.',
  reviews=[('Best fade I have had in years. Clean work, and it still looked sharp three weeks later.', 'Skin fade'),
           ('I came with a photo and left with exactly that cut. Friendly, and no long waiting.', 'Haircut and beard'),
           ('The hot towel shave is worth it. Spotless shop and the price was clear before I booked.', 'Hot towel shave')],
  rev_by='Example client',
  faq_h='Good to know',
  faq=[('Do I need an appointment?', 'We recommend one, so you do not have to wait. Send a request here and we will confirm your time. Walk-ins are welcome when a chair is free.'),
       ('How long does a visit take?', 'A haircut takes about 40 minutes, and a haircut with a beard about an hour. The price list shows the time for each service.'),
       ('Can I bring a photo of the cut I want?', 'Yes. Press any photo in the gallery to request that cut, or show us your own photo. Your barber will tell you what suits your hair.'),
       ('Do you cut children\'s hair?', 'Yes. Children under 12 have their own price.'),
       ('What if I need to cancel or I am late?', 'Please tell us as early as you can, so we can offer your time to someone else. If you are more than 10 minutes late, the service may need to be shortened.'),
       ('Can I pay by card?', 'Yes, we accept cash and card.')],
  contact_h='Book a chair', contact_p='Tell us what you would like and when. We will reply to confirm your time.',
  addr_l='Address', addr='Primer St. 1, Plovdiv', hours_l='Hours',
  phone_l='Phone', email_l='Email',
  map_t='The map is from OpenStreetMap and loads only if you choose.', map_btn='Show the map',
  form_h='Send a request', f_name='Name', f_phone='Phone', f_service='Service', f_date='Preferred date', f_time='Preferred time', f_time_pick='Choose a time', f_hint='Weekday times are shown. Pick a date to see the times for that day.', f_msg='Message (optional)',
  f_send='Send request', f_pick='Choose a service',
  chip_look='Cut you like', chip_plan='Your plan', chip_remove='Remove',
  f_note='We use your details only to answer your request.', f_priv='Privacy notice',
  foot_priv='Privacy notice', admin_t='Demo back office', admin_href='../admin.html?lang=en', quick_label='Quick contact', q_call='Call', q_book='Book a chair',
  dock_label='Colour scheme',
 ),
 'bg': dict(
  lang='bg', root='', script='cyrillic', other_href='en/index.html', other_lang='en', other_label='EN', other_aria='Switch to English',
  privacy_href='privacy.html', home_href='index.html',
  title='Ironwood – бръснарница в Пловдив: подстригване и грижа за брада',
  desc='Подстригване, преходи, оформяне на брада и бръснене с гореща кърпа в класическа бръснарница в Пловдив. Разгледайте работата и цените и изпратете запитване за час.',
  skip='Към съдържанието', tagline='бръснарница', nav_label='Основна навигация', menu_btn='Меню',
  nav=[('#prices', 'Цени'), ('#gallery', 'Галерия'), ('#reviews', 'Отзиви'), ('#faq', 'Въпроси'), ('#contact', 'Контакти')],
  cta='Запази стол',
  h1='Остри линии. Чист вид.',
  lead='Подстригване, преходи, оформяне на брада и бръснене с гореща кърпа в класическа бръснарница в Пловдив. Разгледай работата, виж цените и изпрати запитване.',
  hero_cta2='Виж цените', hero_meta='Пловдив · работим всеки ден', hero_chip='Подстригване · Преходи · Брада',
  hero_alt='Бръснар оформя брадата на клиент с ножица и гребен', hero_side_alt='Бръснарски столове под топли висящи лампи',
  promise_h='Какво да очакваш',
  promise=[('Остро и чисто', 'Инструментите се почистват и дезинфекцират между клиентите, а всяко бръснене започва с нова самобръсначка.'),
           ('Точно навреме', 'Запазваш час и бръснарят те очаква в този час. Без дълго чакане.'),
           ('Ясни цени', 'До всяка услуга има цена и време, така че няма изненади.')],
  gal_h='Последни работи', gal_p='Прически, бради и салонът. Филтрирай по вид и натисни снимка, за да поискаш такава прическа.', gal_filter='Филтър на снимките',
  f_all='Всички', f_cuts='Прически', f_beards='Бради', f_shop='Салонът', shown='Показани снимки: 17', open_photo='Отвори снимката',
  lb_label='Снимка', lb_close='Затвори', lb_prev='Предишна снимка', lb_next='Следваща снимка', lb_request='Заяви тази прическа',
  price_h='Услуги и цени', price_p='До всяка услуга има време и цена. Ако се колебаеш какво ти трябва, изпрати ни снимка и ще те насочим.',
  price_cta='Планирай посещението',
  price_note='Примерни цени в евро, по бръснарници в Пловдив.', menu_alt='Машинки, ножици, гребен и продукти за грижа върху тъмна подложка', menu=MENU_BG,
  plan_h='Планирай посещението', plan_p='Избери какво ти трябва и виж ориентировъчна цена и време. После го добави към заявката си и ще ти предложим само начални часове, които се събират преди затваряне.',
  plan_l_service='Какво ти трябва?', plan_l_length='Стил', plan_l_addons='Допълнения',
  plan_empty='Избери услуга, за да видиш оценка.', plan_price='Ориентировъчна цена', plan_time='Ориентировъчно време',
  plan_req_note='Плюс допълнения, цена по запитване.', plan_add='Добави към заявката',
  plan_fine='Примерни цени. Крайната цена и времето се потвърждават, когато ти отговорим.', plan_on_request='цена по запитване',
  rev_h='Какво казват клиентите', rev_p='Кратки бележки от хора, които си запазват час при нас.', rev_note='Примерни отзиви. Заменете ги с истински отзиви от Google.',
  reviews=[('Най-добрият преход от години. Чиста работа, а след три седмици още изглеждаше остро.', 'Преход до кожа'),
           ('Дойдох със снимка и излязох точно с такава прическа. Приятелска атмосфера и без дълго чакане.', 'Подстригване и брада'),
           ('Бръсненето с гореща кърпа си заслужава. Безупречен салон и цената беше ясна още преди да си запазя час.', 'Бръснене с гореща кърпа')],
  rev_by='Примерен клиент',
  faq_h='Добре е да знаеш',
  faq=[('Нужен ли е час?', 'Препоръчваме да запазиш час, за да не чакаш. Изпрати заявка тук и ще потвърдим часа. Приемаме и без час, когато има свободен стол.'),
       ('Колко време отнема посещението?', 'Подстригването отнема около 40 минути, а подстригване с брада – около час. В ценовата листа е посочено времето за всяка услуга.'),
       ('Мога ли да донеса снимка на прическата, която искам?', 'Да. Натисни коя да е снимка в галерията, за да заявиш тази прическа, или ни покажи своя снимка. Бръснарят ще ти каже какво отива на косата ти.'),
       ('Подстригвате ли деца?', 'Да. Децата до 12 години имат собствена цена.'),
       ('Какво става, ако трябва да отменя или закъснея?', 'Предупреди ни възможно най-рано, за да предложим часа на друг клиент. При закъснение над 10 минути може да се наложи услугата да бъде съкратена.'),
       ('Мога ли да платя с карта?', 'Да, приемаме плащане в брой и с карта.')],
  contact_h='Запази стол', contact_p='Кажи ни какво искаш и кога. Ще ти отговорим, за да потвърдим часа.',
  addr_l='Адрес', addr='ул. Примерна 1, Пловдив', hours_l='Работно време',
  phone_l='Телефон', email_l='Имейл',
  map_t='Картата е от OpenStreetMap и се зарежда само ако поискаш.', map_btn='Покажи картата',
  form_h='Изпрати заявка', f_name='Име', f_phone='Телефон', f_service='Услуга', f_date='Удобна дата', f_time='Удобен час', f_time_pick='Избери час', f_hint='Показани са часовете за делнични дни. Избери дата, за да видиш часовете за конкретния ден.', f_msg='Съобщение (по желание)',
  f_send='Изпрати заявката', f_pick='Избери услуга',
  chip_look='Прическа, която ти харесва', chip_plan='Твоят избор', chip_remove='Премахни',
  f_note='Ползваме данните ти само за да отговорим на заявката ти.', f_priv='Политика за поверителност',
  foot_priv='Политика за поверителност', admin_t='Демо админ панел', admin_href='admin.html', quick_label='Бърза връзка', q_call='Обади се', q_book='Запази стол',
  dock_label='Цветова схема',
 ),
}

TEMPLATE = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'page_template.html'), encoding='utf-8').read()


def build_plan(lang, e):
    """Return (html of the estimator card, json for the script)."""
    i = 1 if lang == 'bg' else 0
    d = L[lang]
    all_opts = {n for _, rows in d['menu'] for n, *_ in rows}
    for s in PLAN_SERVICES:
        names = [s['opt'][i]] if 'opt' in s else [l['opt'][i] for l in s['lengths']]
        for n in names:
            assert n in all_opts, ('plan option not in menu', lang, n)
    price_fmt = lambda p: ('+%s €' % p) if p is not None else d['plan_on_request']

    def radios(group):
        out = []
        for s in PLAN_SERVICES:
            if s['group'] == group:
                out.append('<label class="opt"><input type="radio" name="svc" value="%s"><span>%s</span></label>' % (s['id'], e(s['label'][i])))
        return '\n            '.join(out)

    html = []
    html.append('<fieldset class="opts"><legend>%s</legend>' % e(d['plan_l_service']))
    for gid, g_en, g_bg in PLAN_GROUPS:
        html.append('          <span class="opt-gl">%s</span><div class="opt-row">\n            %s\n          </div>' % (e(g_bg if lang == 'bg' else g_en), radios(gid)))
    html.append('        </fieldset>')
    ext = [s for s in PLAN_SERVICES if 'lengths' in s][0]
    lens = []
    for n, l in enumerate(ext['lengths']):
        lens.append('<label class="opt"><input type="radio" name="len" value="%s"%s><span>%s</span></label>' % (l['id'], ' checked' if n == 0 else '', e(l['label'][i])))
    html.append('        <fieldset class="opts" id="planLength" hidden><legend>%s</legend><div class="opt-row">\n          %s\n        </div></fieldset>' % (e(d['plan_l_length']), '\n          '.join(lens)))
    adds = []
    for a in PLAN_ADDONS:
        used = ' '.join(s['id'] for s in PLAN_SERVICES if a['id'] in s['addons'])
        adds.append('<label class="opt" data-for="%s"><input type="checkbox" name="addon" value="%s"><span>%s <em>%s</em></span></label>'
                    % (used, a['id'], e(a['label'][i]), e(price_fmt(a['price']))))
    html.append('        <fieldset class="opts" id="planAddons" hidden><legend>%s</legend><div class="opt-row">\n          %s\n        </div></fieldset>' % (e(d['plan_l_addons']), '\n          '.join(adds)))

    data = {
        'services': [], 'addons': [],
        'names': {'req': d['plan_req_note']},
    }
    for s in PLAN_SERVICES:
        x = {'id': s['id'], 'label': s['label'][i], 'addons': s['addons']}
        if 'lengths' in s:
            x['lengths'] = [{'id': l['id'], 'price': l['price'], 'minutes': l['minutes'], 'label': l['label'][i], 'opt': l['opt'][i]} for l in s['lengths']]
        else:
            x.update(pmin=s['pmin'], pmax=s['pmax'], mmin=s['mmin'], mmax=s['mmax'], opt=s['opt'][i])
        data['services'].append(x)
    for a in PLAN_ADDONS:
        data['addons'].append({'id': a['id'], 'price': a['price'], 'minutes': a['minutes'], 'label': a['label'][i]})
    js = json.dumps(data, ensure_ascii=False).replace('</', '<\\/')
    return '\n        '.join(html), js


def build(lang):
    d = L[lang]
    e = lambda s: escape(s, quote=True)
    root = d['root']
    out = {}
    out['lang'] = lang
    out['root'] = root
    out['script'] = d['script']
    for k in ['title', 'desc', 'skip', 'tagline', 'nav_label', 'menu_btn', 'cta', 'h1', 'lead', 'hero_cta2', 'hero_meta', 'hero_chip', 'hero_alt', 'hero_side_alt',
              'promise_h', 'gal_h', 'gal_p', 'gal_filter', 'f_all', 'f_cuts', 'f_beards', 'f_shop', 'shown', 'lb_label', 'lb_close', 'lb_prev', 'lb_next', 'lb_request',
              'price_h', 'price_p', 'price_cta', 'price_note', 'menu_alt', 'plan_h', 'plan_p', 'plan_empty', 'plan_price', 'plan_time', 'plan_add', 'plan_fine',
              'rev_h', 'rev_p', 'rev_note', 'faq_h', 'contact_h', 'contact_p',
              'addr_l', 'addr', 'hours_l', 'phone_l', 'email_l', 'map_t', 'map_btn',
              'form_h', 'f_name', 'f_phone', 'f_service', 'f_date', 'f_time', 'f_time_pick', 'f_hint', 'f_msg', 'f_send', 'f_pick',
              'chip_look', 'chip_plan', 'chip_remove', 'f_note', 'f_priv',
              'foot_priv', 'admin_t', 'quick_label', 'q_call', 'q_book', 'dock_label']:
        out[k] = e(d[k])
    out['other_href'] = d['other_href']; out['other_lang'] = d['other_lang']; out['other_label'] = d['other_label']; out['other_aria'] = e(d['other_aria'])
    out['privacy_href'] = d['privacy_href']; out['home_href'] = d['home_href']; out['admin_href'] = d['admin_href']
    out['nav_links'] = '\n      '.join('<a href="%s">%s</a>' % (h, e(t)) for h, t in d['nav'])
    out['promise'] = '\n        '.join('<li><h3>%s</h3><p>%s</p></li>' % (e(t), e(p)) for t, p in d['promise'])
    items = []
    for name, cat, w, h, alt_en, alt_bg in GALLERY:
        alt = e(alt_bg if lang == 'bg' else alt_en)
        items.append(
            '<button class="gal-item" type="button" data-cat="%s" data-full="%simages/stock/%s.jpg" aria-label="%s: %s">'
            '<img src="%simages/stock/%s-800.jpg" srcset="%simages/stock/%s-800.jpg 800w" sizes="(min-width: 900px) 30vw, 46vw" width="800" height="%d" alt="%s" loading="lazy" decoding="async">'
            '</button>' % (cat, root, name, e(d['open_photo']), alt, root, name, root, name, round(800 * h / w), alt))
    out['gallery'] = '\n        '.join(items)
    groups, options = [], []
    for gt, rows in d['menu']:
        rs = []
        for name, time, price, (mn, mx) in rows:
            small = '<small>%s</small>' % e(time) if time else ''
            rs.append('<div class="menu-row"><span class="menu-name">%s%s</span><span class="menu-price">%s</span></div>' % (e(name), small, e(price)))
            options.append('<option data-min="%d" data-max="%d">%s</option>' % (mn, mx, e(name)))
        groups.append('<div class="menu-group"><h3>%s</h3>\n          %s\n        </div>' % (e(gt), '\n          '.join(rs)))
    out['menu'] = '\n        '.join(groups)
    out['service_options'] = '\n          '.join(options)
    out['plan_card'], out['plan_json'] = build_plan(lang, e)
    out['reviews'] = '\n        '.join(
        '<figure class="rev"><blockquote>%s</blockquote><figcaption><b>%s</b> · %s</figcaption></figure>' % (e(q), e(s), e(d['rev_by']))
        for q, s in d['reviews'])
    out['faq'] = '\n          '.join('<details><summary>%s</summary><p>%s</p></details>' % (e(q), e(a)) for q, a in d['faq'])
    out['hours'] = e(hours_text(lang))
    out['phone'] = PHONE_DISPLAY; out['phone_href'] = PHONE_HREF; out['email'] = EMAIL; out['brand'] = BRAND
    sw = []
    for key, c1, c2, n_en, n_bg in SKINS:
        name = n_bg if lang == 'bg' else n_en
        sw.append('<button class="sw" type="button" data-skin="%s" data-name="%s" aria-label="%s: %s" title="%s" aria-pressed="%s" style="--s1:%s;--s2:%s"></button>'
                  % (key, e(name), e(d['dock_label']), e(name), e(name), 'true' if key == 'brass' else 'false', c1, c2))
    out['swatches'] = '\n        '.join(sw)
    out['skin_name'] = e(SKINS[0][4] if lang == 'bg' else SKINS[0][3])
    wd_days = 'Mo-Fr %s' % OPEN_WEEKDAY
    we_days = 'Sa-Su %s' % OPEN_WEEKEND
    out['hours_ld'] = '"%s", "%s"' % (wd_days, we_days)
    out['open_wd'] = OPEN_WEEKDAY
    out['open_we'] = OPEN_WEEKEND
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
    'window.IRONWOOD_CONFIG = {\n'
    '  mode: "%s",            /* "demo" = requests are kept in this browser only; "live" = real API at apiBase (docs/API.md) */\n'
    '  apiBase: "%s",\n'
    '  hours: { weekday: ["%s", "%s"], weekend: ["%s", "%s"] },\n'
    '  capacity: %d,             /* visits that can run at the same time */\n'
    '  slotMinutes: %d,\n'
    '  latency: [600, 1100]      /* demo only: pretend network delay in milliseconds */\n'
    '};\n'
) % (MODE, API_BASE, OPEN_WEEKDAY.split('-')[0], OPEN_WEEKDAY.split('-')[1], OPEN_WEEKEND.split('-')[0], OPEN_WEEKEND.split('-')[1], CAPACITY, SLOT_MINUTES)
os.makedirs(os.path.join(SHOP, 'js'), exist_ok=True)
open(os.path.join(SHOP, 'js', 'config.js'), 'w', encoding='utf-8').write(cfg)
print('config.js written')
