import os, re, json
from html import escape

NAIL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ---- Edit these placeholders for each salon -------------------------------------------------
OPEN_WEEKDAY = '09:00-19:00'      # opening and closing time, Mon - Fri
OPEN_WEEKEND = '10:00-18:00'      # opening and closing time, Sat - Sun
PHONE_DISPLAY = '+359 000 000 000'
PHONE_HREF = '+359000000000'
EMAIL = 'email@example.com'
# Request system. 'demo' = the form talks to a mock server that stores requests in the visitor's browser.
# 'live' = it sends real HTTP requests to API_BASE (see docs/API.md). Written to js/config.js.
MODE = 'demo'
API_BASE = '/api'
CAPACITY = 1                      # visits that can run at the same time (number of technicians)
SLOT_MINUTES = 15                 # gap between start times
BRAND = 'Nuance'
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

# group title, [(name, time text, price text, (min minutes, max minutes))]   Minutes drive the time list in the form.
MENU_EN = [
    ('Hands', [
        ('Classic manicure, no polish', '45 min', '12 €', (45, 45)),
        ('Gel polish manicure', '1 h – 1 h 30', '25 €', (60, 90)),
        ('Gel manicure with French tips or nail art', '1 h 30', '28 €', (90, 90)),
        ('Gel overlay on natural nails', '2 h', '30 €', (120, 120)),
        ('Gel polish removal', '20 – 30 min', '10 €', (20, 30)),
        ('Broken nail repair', '', '2 € per nail', (10, 10))]),
    ('Extensions', [
        ('Gel extensions, short', '1 h 30', '40 €', (90, 90)),
        ('Gel extensions, medium', '1 h 45', '45 €', (105, 105)),
        ('Gel extensions, long', '2 h', '50 €', (120, 120)),
        ('Refill', '1 h 30 – 2 h', 'from 30 €', (90, 120))]),
    ('Feet', [
        ('Classic pedicure, no polish', '45 min', '20 €', (45, 45)),
        ('Gel polish pedicure', '1 h – 1 h 30', '25 – 30 €', (60, 90)),
        ('SPA pedicure with gel polish', '2 h', '30 €', (120, 120))]),
    ('Extras', [
        ('Nail art, French tips, chrome', '', 'on request', (30, 60))]),
]
MENU_BG = [
    ('Ръце', [
        ('Класически маникюр, без лак', '45 мин', '12 €', (45, 45)),
        ('Маникюр с гел лак', '1 ч – 1 ч 30 мин', '25 €', (60, 90)),
        ('Гел лак с френски връхчета или нейл арт', '1 ч 30 мин', '28 €', (90, 90)),
        ('Гел върху естествени нокти', '2 ч', '30 €', (120, 120)),
        ('Сваляне на гел лак', '20 – 30 мин', '10 €', (20, 30)),
        ('Ремонт на счупен нокът', '', '2 € на нокът', (10, 10))]),
    ('Изграждане', [
        ('Изграждане с гел, къси нокти', '1 ч 30 мин', '40 €', (90, 90)),
        ('Изграждане с гел, средни нокти', '1 ч 45 мин', '45 €', (105, 105)),
        ('Изграждане с гел, дълги нокти', '2 ч', '50 €', (120, 120)),
        ('Корекция', '1 ч 30 мин – 2 ч', 'от 30 €', (90, 120))]),
    ('Крака', [
        ('Класически педикюр, без лак', '45 мин', '20 €', (45, 45)),
        ('Педикюр с гел лак', '1 ч – 1 ч 30 мин', '25 – 30 €', (60, 90)),
        ('СПА педикюр с гел лак', '2 ч', '30 €', (120, 120))]),
    ('Допълнения', [
        ('Нейл арт, френски връхчета, хром', '', 'по запитване', (30, 60))]),
]

# ---- "Plan your visit" estimator (numbers are sample values based on Plovdiv salons) --------------
# opt = the menu item the form selects (must match a menu name above)
PLAN_SERVICES = [
    dict(id='classic_mani', group='hands', pmin=12, pmax=12, mmin=45, mmax=45, addons=[],
         label=('Classic manicure', 'Класически маникюр'), opt=('Classic manicure, no polish', 'Класически маникюр, без лак')),
    dict(id='gel_mani', group='hands', pmin=25, pmax=25, mmin=60, mmax=90, addons=['remove_gel', 'french_art', 'repair'],
         label=('Gel polish manicure', 'Маникюр с гел лак'), opt=('Gel polish manicure', 'Маникюр с гел лак')),
    dict(id='overlay', group='hands', pmin=30, pmax=30, mmin=120, mmax=120, addons=['remove_gel', 'french_art', 'repair'],
         label=('Gel overlay on natural nails', 'Гел върху естествени нокти'), opt=('Gel overlay on natural nails', 'Гел върху естествени нокти')),
    dict(id='extensions', group='hands', addons=['remove_ext', 'art_request', 'repair'],
         label=('Gel extensions', 'Изграждане с гел'),
         lengths=[dict(id='short', price=40, minutes=90, label=('Short', 'Къси'), opt=('Gel extensions, short', 'Изграждане с гел, къси нокти')),
                  dict(id='medium', price=45, minutes=105, label=('Medium', 'Средни'), opt=('Gel extensions, medium', 'Изграждане с гел, средни нокти')),
                  dict(id='long', price=50, minutes=120, label=('Long', 'Дълги'), opt=('Gel extensions, long', 'Изграждане с гел, дълги нокти'))]),
    dict(id='classic_pedi', group='feet', pmin=20, pmax=20, mmin=45, mmax=45, addons=[],
         label=('Classic pedicure', 'Класически педикюр'), opt=('Classic pedicure, no polish', 'Класически педикюр, без лак')),
    dict(id='gel_pedi', group='feet', pmin=25, pmax=30, mmin=60, mmax=90, addons=['remove_gel', 'french_art'],
         label=('Gel polish pedicure', 'Педикюр с гел лак'), opt=('Gel polish pedicure', 'Педикюр с гел лак')),
    dict(id='spa_pedi', group='feet', pmin=30, pmax=30, mmin=120, mmax=120, addons=['remove_gel'],
         label=('SPA pedicure with gel polish', 'СПА педикюр с гел лак'), opt=('SPA pedicure with gel polish', 'СПА педикюр с гел лак')),
]
PLAN_ADDONS = [
    dict(id='remove_gel', price=10, minutes=30, label=('Remove old gel polish', 'Сваляне на стар гел лак')),
    dict(id='remove_ext', price=15, minutes=45, label=('Remove old extensions', 'Сваляне на стари нокти (изграждане)')),
    dict(id='french_art', price=3, minutes=15, label=('French tips or simple art on a few nails', 'Френски връхчета или лек дизайн на няколко нокътя')),
    dict(id='art_request', price=None, minutes=30, label=('Detailed nail art (price on request)', 'Подробен нейл арт (цена по запитване)')),
    dict(id='repair', price=2, minutes=10, label=('Repair one broken nail', 'Ремонт на един счупен нокът')),
]


def hours_text(lang):
    wd, we = OPEN_WEEKDAY.replace('-', ' – '), OPEN_WEEKEND.replace('-', ' – ')
    return ('Mon – Fri %s · Sat – Sun %s' % (wd, we)) if lang == 'en' else ('Пон – Пет %s · Съб – Нед %s' % (wd, we))


L = {
 'en': dict(
  lang='en', root='../', script='latin', other_href='../index.html', other_lang='bg', other_label='БГ', other_aria='Превключи на български',
  privacy_href='privacy.html', home_href='index.html',
  title='Nuance – nail studio in Plovdiv',
  desc='Gel polish, nail extensions and nail art in a calm studio in Plovdiv. See the gallery and prices, and send a request for an appointment.',
  skip='Skip to content', tagline='nail studio', nav_label='Main navigation', menu_btn='Menu',
  nav=[('#prices', 'Prices'), ('#gallery', 'Gallery'), ('#reviews', 'Reviews'), ('#faq', 'Questions'), ('#contact', 'Contact')],
  cta='Request a time',
  h1='Nails that feel like you.',
  lead='Gel polish, extensions and nail art in a calm, clean studio in Plovdiv. See the work, check the prices, send a request.',
  hero_cta2='See prices', hero_meta='Plovdiv · open every day', hero_chip='Gel · Extensions · Nail art',
  hero_alt='Soft nude pink gel nails on a white fur surface', hero_side_alt='Black and tortoiseshell nails with a gold ring',
  promise_h='What to expect',
  promise=[('Clean and calm', 'Tools are cleaned and sterilised between clients, in a quiet, tidy studio.'),
           ('Your design, done properly', 'Bring a photo or an idea. We tell you what is possible before we start.'),
           ('Clear prices', 'Every service has a price and a time, so there are no surprises.')],
  gal_h='Recent work', gal_p='A few sets we are proud of. Filter by style, and press a photo to request that look.', gal_filter='Filter photos',
  f_all='All', f_natural='Natural', f_art='Nail art', f_bold='Bold', shown='Photos shown: 10', open_photo='Open photo',
  lb_label='Photo', lb_close='Close', lb_prev='Previous photo', lb_next='Next photo', lb_request='Request this look',
  price_h='Services and prices', price_p='Every service has a time and a price. Not sure what you need? Send us a photo and we will help.',
  price_cta='Plan your visit',
  price_note='Sample prices in euro, based on salons in Plovdiv.', menu_alt='Rows of nail polish bottles on shelves', menu=MENU_EN,
  plan_h='Plan your visit', plan_p='Choose what you need to see an estimated price and time. Then add it to your request, and we will only offer start times that fit before closing.',
  plan_l_service='What do you need?', plan_l_length='Nail length', plan_l_addons='Extras', plan_g_hands='Hands', plan_g_feet='Feet',
  plan_empty='Choose a service to see the estimate.', plan_price='Estimated price', plan_time='Estimated time',
  plan_req_note='Plus detailed nail art, priced on request.', plan_add='Add to my request',
  plan_fine='Sample prices. We confirm the final price and time when we reply.', plan_on_request='price on request',
  rev_h='What clients say', rev_p='Short notes from people who book with us.', rev_note='Example reviews. Replace them with real Google reviews.',
  reviews=[('Perfect gel manicure. It lasted three weeks without a single chip.', 'Gel polish manicure'),
           ('I brought a photo and they made exactly that design.', 'Nail art'),
           ('A calm studio, everything spotless, and the price was clear before I booked.', 'Gel polish pedicure')],
  rev_by='Example client',
  faq_h='Good to know',
  faq=[('How long does a visit take?', 'A gel polish manicure takes about 1 to 1.5 hours, and extensions 2 to 3 hours. The price list shows the time for each service.'),
       ('Can I bring a photo of the design I want?', 'Yes. Press any photo in the gallery to request that look, or bring or send your own photo, and we will tell you how close we can get and whether it changes the price.'),
       ('Is removing my old gel included?', 'Removal is a separate service and is on the price list. That way the old gel comes off safely, without harming your nails.'),
       ('What if I need to cancel or I am late?', 'Please tell us at least 24 hours ahead so we can offer your time to someone else. If you are more than 15 minutes late, the service may need to be shortened.'),
       ('Do I need to pay a deposit?', 'For extensions and longer visits we may ask for a small deposit, which is deducted from the price.')],
  contact_h='Request a time', contact_p='Tell us what you would like and when. We will reply to confirm your time.',
  addr_l='Address', addr='Primer St. 1, Plovdiv', hours_l='Hours',
  phone_l='Phone', email_l='Email',
  map_t='The map is from OpenStreetMap and loads only if you choose.', map_btn='Show the map',
  form_h='Send a request', f_name='Name', f_phone='Phone', f_service='Service', f_date='Preferred date', f_time='Preferred time', f_time_pick='Choose a time', f_hint='Weekday times are shown. Pick a date to see the times for that day.', f_msg='Message (optional)',
  f_send='Send request', f_pick='Choose a service',
  chip_look='Look you like', chip_plan='Your plan', chip_remove='Remove',
  f_note='We use your details only to answer your request.', f_priv='Privacy notice',
  foot_priv='Privacy notice', admin_t='Demo back office', admin_href='../admin.html?lang=en', quick_label='Quick contact', q_call='Call', q_book='Request a time',
  dock_label='Colour scheme',
 ),
 'bg': dict(
  lang='bg', root='', script='cyrillic', other_href='en/index.html', other_lang='en', other_label='EN', other_aria='Switch to English',
  privacy_href='privacy.html', home_href='index.html',
  title='Nuance – студио за нокти в Пловдив',
  desc='Гел лак, изграждане на нокти и нейл арт в спокойно студио в Пловдив. Разгледайте галерията и цените и изпратете запитване за час.',
  skip='Към съдържанието', tagline='студио за нокти', nav_label='Основна навигация', menu_btn='Меню',
  nav=[('#prices', 'Цени'), ('#gallery', 'Галерия'), ('#reviews', 'Отзиви'), ('#faq', 'Въпроси'), ('#contact', 'Контакти')],
  cta='Заяви час',
  h1='Нокти, които ти приличат.',
  lead='Гел лак, изграждане и нейл арт в спокойно и чисто студио в Пловдив. Разгледай работата, виж цените и изпрати запитване.',
  hero_cta2='Виж цените', hero_meta='Пловдив · работим всеки ден', hero_chip='Гел лак · Изграждане · Нейл арт',
  hero_alt='Нежни телесно-розови гел нокти върху бяла пухкава повърхност', hero_side_alt='Черни нокти с костенурков принт и златен пръстен',
  promise_h='Какво да очакваш',
  promise=[('Чисто и спокойно', 'Инструментите се почистват и стерилизират между клиентите, в тихо и подредено студио.'),
           ('Твоят дизайн, направен както трябва', 'Донеси снимка или идея. Преди да започнем, ще ти кажем какво е възможно.'),
           ('Ясни цени', 'До всяка услуга има цена и време, така че няма изненади.')],
  gal_h='Последни работи', gal_p='Няколко комплекта, с които се гордеем. Филтрирай по стил и натисни снимка, за да заявиш този стил.', gal_filter='Филтър на снимките',
  f_all='Всички', f_natural='Естествени', f_art='Нейл арт', f_bold='Смели', shown='Показани снимки: 10', open_photo='Отвори снимката',
  lb_label='Снимка', lb_close='Затвори', lb_prev='Предишна снимка', lb_next='Следваща снимка', lb_request='Заяви този стил',
  price_h='Услуги и цени', price_p='До всяка услуга има време и цена. Ако се колебаеш какво ти трябва, изпрати ни снимка и ще те насочим.',
  price_cta='Планирай посещението',
  price_note='Примерни цени в евро, по салони в Пловдив.', menu_alt='Редици лакове за нокти на рафтове', menu=MENU_BG,
  plan_h='Планирай посещението', plan_p='Избери какво ти трябва и виж ориентировъчна цена и време. После го добави към заявката си и ще ти предложим само начални часове, които се събират преди затваряне.',
  plan_l_service='Какво ти трябва?', plan_l_length='Дължина на ноктите', plan_l_addons='Допълнения', plan_g_hands='Ръце', plan_g_feet='Крака',
  plan_empty='Избери услуга, за да видиш оценка.', plan_price='Ориентировъчна цена', plan_time='Ориентировъчно време',
  plan_req_note='Плюс подробен нейл арт, цена по запитване.', plan_add='Добави към заявката',
  plan_fine='Примерни цени. Крайната цена и времето се потвърждават, когато ти отговорим.', plan_on_request='цена по запитване',
  rev_h='Какво казват клиентите', rev_p='Кратки бележки от хора, които си запазват час при нас.', rev_note='Примерни отзиви. Заменете ги с истински отзиви от Google.',
  reviews=[('Идеален гел маникюр. Издържа три седмици без нито една цепнатина.', 'Маникюр с гел лак'),
           ('Занесох снимка и ми направиха точно такъв дизайн.', 'Нейл арт'),
           ('Спокойно студио, всичко беше чисто, а цената беше ясна още преди да си запазя час.', 'Педикюр с гел лак')],
  rev_by='Примерен клиент',
  faq_h='Добре е да знаеш',
  faq=[('Колко време отнема посещението?', 'Маникюр с гел лак отнема около 1 до 1,5 часа, а изграждане на нокти – 2 до 3 часа. В ценовата листа е посочено времето за всяка услуга.'),
       ('Мога ли да донеса снимка на дизайна, който искам?', 'Да. Натисни коя да е снимка в галерията, за да заявиш този стил, или донеси или изпрати своя снимка, и ще ти кажем доколко можем да я пресъздадем и дали това променя цената.'),
       ('Свалянето на стар гел включено ли е?', 'Свалянето е отделна услуга и е в ценовата листа. Така старият гел се маха безопасно, без да се вреди на ноктите.'),
       ('Какво става, ако трябва да отменя или закъснея?', 'Предупреди ни поне 24 часа предварително, за да предложим часа на друг клиент. При закъснение над 15 минути може да се наложи услугата да бъде съкратена.'),
       ('Нужен ли е депозит?', 'За изграждане на нокти и по-дълги посещения можем да поискаме малък депозит, който се приспада от цената.')],
  contact_h='Заяви час', contact_p='Кажи ни какво искаш и кога. Ще ти отговорим, за да потвърдим часа.',
  addr_l='Адрес', addr='ул. Примерна 1, Пловдив', hours_l='Работно време',
  phone_l='Телефон', email_l='Имейл',
  map_t='Картата е от OpenStreetMap и се зарежда само ако поискаш.', map_btn='Покажи картата',
  form_h='Изпрати заявка', f_name='Име', f_phone='Телефон', f_service='Услуга', f_date='Удобна дата', f_time='Удобен час', f_time_pick='Избери час', f_hint='Показани са часовете за делнични дни. Избери дата, за да видиш часовете за конкретния ден.', f_msg='Съобщение (по желание)',
  f_send='Изпрати заявката', f_pick='Избери услуга',
  chip_look='Стил, който ти харесва', chip_plan='Твоят избор', chip_remove='Премахни',
  f_note='Ползваме данните ти само за да отговорим на заявката ти.', f_priv='Политика за поверителност',
  foot_priv='Политика за поверителност', admin_t='Демо админ панел', admin_href='admin.html', quick_label='Бърза връзка', q_call='Обади се', q_book='Заяви час',
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
    html.append('          <span class="opt-gl">%s</span><div class="opt-row">\n            %s\n          </div>' % (e(d['plan_g_hands']), radios('hands')))
    html.append('          <span class="opt-gl">%s</span><div class="opt-row">\n            %s\n          </div>' % (e(d['plan_g_feet']), radios('feet')))
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
              'promise_h', 'gal_h', 'gal_p', 'gal_filter', 'f_all', 'f_natural', 'f_art', 'f_bold', 'shown', 'lb_label', 'lb_close', 'lb_prev', 'lb_next', 'lb_request',
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
                  % (key, e(name), e(d['dock_label']), e(name), e(name), 'true' if key == 'rose' else 'false', c1, c2))
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
    path = os.path.join(NAIL, 'index.html') if lang == 'bg' else os.path.join(NAIL, 'en', 'index.html')
    os.makedirs(os.path.dirname(path), exist_ok=True)
    open(path, 'w', encoding='utf-8').write(html)
    print(lang, len(html), 'bytes ->', path)


# ---- js/config.js: the settings the page and the mock server read -------------------------------
cfg = (
    '/* Generated by tools/build_pages.py. Edit the values at the top of that file, then run it again. */\n'
    'window.NUANCE_CONFIG = {\n'
    '  mode: "%s",            /* "demo" = requests are kept in this browser only; "live" = real API at apiBase (docs/API.md) */\n'
    '  apiBase: "%s",\n'
    '  hours: { weekday: ["%s", "%s"], weekend: ["%s", "%s"] },\n'
    '  capacity: %d,             /* visits that can run at the same time */\n'
    '  slotMinutes: %d,\n'
    '  latency: [600, 1100]      /* demo only: pretend network delay in milliseconds */\n'
    '};\n'
) % (MODE, API_BASE, OPEN_WEEKDAY.split('-')[0], OPEN_WEEKDAY.split('-')[1], OPEN_WEEKEND.split('-')[0], OPEN_WEEKEND.split('-')[1], CAPACITY, SLOT_MINUTES)
os.makedirs(os.path.join(NAIL, 'js'), exist_ok=True)
open(os.path.join(NAIL, 'js', 'config.js'), 'w', encoding='utf-8').write(cfg)
print('config.js written')
