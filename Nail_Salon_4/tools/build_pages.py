import os, re, json
from html import escape

SHOP = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ---- Edit these placeholders for each salon -------------------------------------------------
OPEN_WEEKDAY = '09:00-20:00'      # opening and closing time, Mon - Fri
OPEN_WEEKEND = '10:00-18:00'      # opening and closing time, Sat - Sun
PHONE_DISPLAY = '+359 000 000 000'
PHONE_HREF = '+359000000000'
EMAIL = 'email@example.com'
# Request system. 'demo' = the booking form talks to a mock server that keeps requests in the visitor's browser.
# 'live' = it sends real HTTP requests to API_BASE (see docs/API.md). Written to js/config.js.
MODE = 'demo'
API_BASE = '/api'
CAPACITY = 2                      # visits that can run at the same time (number of technicians)
SLOT_MINUTES = 15                 # gap between start times
LEAD_MINUTES = 60                 # a same-day request needs this much notice
BRAND = 'Glossy'
# ---------------------------------------------------------------------------------------------

SKINS = [  # key, colours for the swatch (background, accent), names
    ('bubblegum', '#FFF3F7', '#D6246E', 'Bubblegum',      'Дъвка'),
    ('lilac',     '#F4EFFF', '#6D3FD1', 'Lilac Dream',    'Люлякова мечта'),
    ('peach',     '#FFF1E8', '#C2410C', 'Peach Fizz',     'Прасковен физ'),
    ('mint',      '#E9FBF4', '#0A7C62', 'Mint Chip',      'Мента'),
    ('berry',     '#EAF2FF', '#1F5FE0', 'Blueberry',      'Боровинка'),
]
DEFAULT_SKIN = SKINS[0]

# Services used by the set builder (the same prices as the other nail studios):
# id, name EN, name BG, minutes (longest), price min, price max, kind
ITEMS = [
    ('gel_mani',  'Gel polish manicure', 'Маникюр с гел лак', 90, 25, 25, 'fixed'),
    ('ext_short', 'Gel extensions, short', 'Изграждане с гел, къси нокти', 90, 40, 40, 'fixed'),
    ('ext_med',   'Gel extensions, medium', 'Изграждане с гел, средни нокти', 105, 45, 45, 'fixed'),
    ('ext_long',  'Gel extensions, long', 'Изграждане с гел, дълги нокти', 120, 50, 50, 'fixed'),
    ('art',       'Nail art, French tips, chrome', 'Нейл арт, френски връхчета, хром', 60, 0, 0, 'request'),
    ('removal',   'Gel polish removal', 'Сваляне на гел лак', 30, 10, 10, 'fixed'),
    ('gel_pedi',  'Gel polish pedicure', 'Педикюр с гел лак', 90, 25, 30, 'fixed'),
]
# Builder choices. base: value, service id, label EN, label BG, hint EN, hint BG
BASES = [
    ('nat',   'gel_mani',  'My own nails', 'Моите нокти', 'gel polish', 'гел лак'),
    ('short', 'ext_short', 'Short', 'Къси', 'extensions', 'изграждане'),
    ('med',   'ext_med',   'Medium', 'Средни', 'extensions', 'изграждане'),
    ('long',  'ext_long',  'Long', 'Дълги', 'extensions', 'изграждане'),
]
SHAPES = [('round', 'Round', 'Овална'), ('square', 'Square', 'Квадратна'), ('almond', 'Almond', 'Бадем'), ('coffin', 'Coffin', 'Ковчег'), ('stiletto', 'Stiletto', 'Стилето')]
COLOURS = [  # hex, name EN, name BG
    ('#E9C5B5', 'Nude', 'Нюд'), ('#F4B6C2', 'Blush', 'Руж'), ('#D6246E', 'Berry', 'Малина'), ('#C8102E', 'Cherry', 'Череша'),
    ('#FF7A6B', 'Coral', 'Корал'), ('#FFC49B', 'Peach', 'Праскова'), ('#FFE08A', 'Butter', 'Масло'), ('#A8E6CF', 'Mint', 'Мента'),
    ('#9EC9FF', 'Sky', 'Небе'), ('#C7B2F5', 'Lilac', 'Люляк'), ('#5B2A6B', 'Plum', 'Слива'), ('#1A1A1A', 'Black', 'Черно'), ('#FFFFFF', 'Milk', 'Мляко'),
]
FINISHES = [('gloss', 'Gloss', 'Гланц', False), ('matte', 'Matte', 'Мат', False), ('chrome', 'Chrome', 'Хром', True), ('glitter', 'Glitter', 'Брокат', True)]
# extras: value, service id, label EN, label BG
EXTRAS = [
    ('french', 'art',      'French tips', 'Френски връхчета'),
    ('accent', 'art',      'Accent nail art', 'Арт на един нокът'),
    ('removal', 'removal', 'Remove old gel', 'Сваляне на стар гел'),
    ('pedi',   'gel_pedi', 'Add a pedicure', 'Добави педикюр'),
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
    ('manicure-closeup',    'natural', 1600, 2400, 'Close-up of a fresh manicure', 'Близък план на свеж маникюр'),
]


def hours_text(lang):
    wd, we = OPEN_WEEKDAY.replace('-', ' – '), OPEN_WEEKEND.replace('-', ' – ')
    return ('Mon – Fri %s · Sat – Sun %s' % (wd, we)) if lang == 'en' else ('Пон – Пет %s · Съб – Нед %s' % (wd, we))


L = {
 'en': dict(
  lang='en', root='../', script='latin', other_href='../index.html', other_lang='bg', other_label='БГ', other_aria='Превключи на български',
  privacy_href='privacy.html', home_href='index.html',
  title='Glossy – nail studio in Plovdiv: design your set',
  desc='Design your nail set online: pick the shape, length, colour and finish, see the price and the time, and book a free slot at a nail studio in Plovdiv.',
  skip='Skip to content', tagline='nail studio', nav_label='Main navigation', menu_btn='Menu',
  nav=[('#design', 'Design a set'), ('#gallery', 'Inspo'), ('#book', 'Book'), ('#visit', 'Visit')],
  cta='Book now',
  hero_label='Nail studio · Plovdiv', h1='Your nails. <em>Your rules.</em>',
  lead='Play with shapes, colours and finishes, watch your set come to life, and book it in a minute. The price shows up before you decide.',
  cta1='Design my set', cta2='Get inspired', loading='Checking…', alt1='Pink and red nails with love lettering', alt2='Mauve, white and silver glitter nails', alt3='Rose pink nails against a pink background', sticker='Try it live',
  marquee=['Gel polish', 'Extensions', 'Nail art', 'French tips', 'Chrome', 'Glitter', 'Pedicure'],
  k_design='Set builder', design_h='Design your set, see it live.', design_p='Pick a length, a shape, a colour and a finish. The hand on the left updates as you go, and the price and time add up on the right.',
  prev_label='Preview of your nail set', o_base='Length', o_shape='Shape', o_colour='Colour', o_finish='Finish', o_extras='Extras',
  sum_h='Your set', sum_price='Price', sum_time='Time', sum_book='Book this set', sum_fine='Sample prices. We confirm the final price and time when we reply.',
  from_l='from', on_request='on request', about='About', art_note='Nail art is priced on request, depending on the design.', design_word='Set',
  k_gallery='Inspo', gal_h='Need ideas?', gal_p='Real sets from the studio. Press a photo, then press I want this look and it travels with your booking.',
  gal_filter='Filter photos', f_all='All', f_natural='Natural', f_art='Nail art', f_bold='Bold', shown='Photos shown: {n}', open_photo='Open photo',
  k_rev='Love notes', rev_h='What clients say',
  reviews=[('Perfect gel manicure. It lasted three weeks without a single chip.', 'Gel polish manicure'),
           ('I brought a photo and they made exactly that design.', 'Nail art'),
           ('A calm studio, everything spotless, and the price was clear before I booked.', 'Gel polish pedicure')],
  rev_by='Example client', rev_note='Example reviews. Replace them with real Google reviews.',
  k_book='Book', book_h='Pick your day and time.', book_p='Your set is ready. Choose a day, a free time, and tell us who you are.',
  change_set='Change my set', chip_look='Look you like', chip_remove='Remove', s_day='Pick a day', s_time='Pick a time', s_you='About you', checking='Checking free times…',
  f_time='Time', f_name='Name', f_phone='Phone', f_msg='Message (optional)', f_send='Send the request', f_note='We use your details only to answer your request.', f_priv='Privacy notice',
  k_visit='Visit', visit_h='Find the studio', addr_l='Address', addr='Primer St. 1, Plovdiv', hours_l='Hours', phone_l='Phone', email_l='Email',
  map_t='The map is from OpenStreetMap and loads only if you choose.', map_btn='Show the map',
  k_faq='Questions', faq_h='Good to know',
  faq=[('How long does a visit take?', 'A gel polish manicure takes about 1 to 1.5 hours, and extensions 2 to 3 hours. The builder adds the time up for you.'),
       ('Can I bring a photo of the design I want?', 'Yes. Pick a photo in the inspo gallery, or bring or send your own, and we will tell you how close we can get.'),
       ('Is removing my old gel included?', 'Removal is a separate service. Tick Remove old gel in the builder so the old gel comes off safely.'),
       ('What if I need to cancel or I am late?', 'Please tell us at least 24 hours ahead so we can offer your time to someone else. If you are more than 15 minutes late, the service may need to be shortened.'),
       ('Do I need to pay a deposit?', 'For extensions and longer visits we may ask for a small deposit, which is deducted from the price.')],
  foot_tag='Nail studio in Plovdiv', foot_priv='Privacy notice', admin_t='Demo back office', admin_href='../admin.html?lang=en', quick_label='Quick contact', q_call='Call', q_book='Book',
  dock_label='Colour scheme',
  lb_label='Photo', lb_close='Close', lb_prev='Previous photo', lb_next='Next photo', lb_request='I want this look',
 ),
 'bg': dict(
  lang='bg', root='', script='cyrillic', other_href='en/index.html', other_lang='en', other_label='EN', other_aria='Switch to English',
  privacy_href='privacy.html', home_href='index.html',
  title='Glossy – студио за нокти в Пловдив: създай своя комплект',
  desc='Създай своя комплект нокти онлайн: избери форма, дължина, цвят и финиш, виж цената и времето и запази свободен час в студио за нокти в Пловдив.',
  skip='Към съдържанието', tagline='студио за нокти', nav_label='Основна навигация', menu_btn='Меню',
  nav=[('#design', 'Създай комплект'), ('#gallery', 'Идеи'), ('#book', 'Час'), ('#visit', 'Адрес')],
  cta='Запази час',
  hero_label='Студио за нокти · Пловдив', h1='Твоите нокти. <em>Твоите правила.</em>',
  lead='Поиграй си с форми, цветове и финиши, гледай как комплектът оживява и го запази за минута. Цената се вижда, преди да решиш.',
  cta1='Създай моя комплект', cta2='Вдъхнови се', loading='Проверяваме…', alt1='Розови и червени нокти с надпис love', alt2='Люляково-розови, бели и сребристи брокатени нокти', alt3='Розови нокти на розов фон', sticker='Пробвай на живо',
  marquee=['Гел лак', 'Изграждане', 'Нейл арт', 'Френски връхчета', 'Хром', 'Брокат', 'Педикюр'],
  k_design='Конструктор', design_h='Създай комплекта си и го виж на живо.', design_p='Избери дължина, форма, цвят и финиш. Ръката отляво се променя в движение, а цената и времето се събират отдясно.',
  prev_label='Преглед на твоя комплект нокти', o_base='Дължина', o_shape='Форма', o_colour='Цвят', o_finish='Финиш', o_extras='Допълнения',
  sum_h='Твоят комплект', sum_price='Цена', sum_time='Време', sum_book='Запази този комплект', sum_fine='Примерни цени. Крайната цена и времето се потвърждават, когато ти отговорим.',
  from_l='от', on_request='по запитване', about='Около', art_note='Нейл артът се оценява по запитване, според дизайна.', design_word='Комплект',
  k_gallery='Идеи', gal_h='Търсиш идеи?', gal_p='Истински комплекти от студиото. Натисни снимка, после „Искам този стил“ и той тръгва с твоето запазване.',
  gal_filter='Филтър на снимките', f_all='Всички', f_natural='Естествени', f_art='Нейл арт', f_bold='Смели', shown='Показани снимки: {n}', open_photo='Отвори снимката',
  k_rev='Бележки с любов', rev_h='Какво казват клиентите',
  reviews=[('Идеален гел маникюр. Издържа три седмици без нито една цепнатина.', 'Маникюр с гел лак'),
           ('Занесох снимка и ми направиха точно такъв дизайн.', 'Нейл арт'),
           ('Спокойно студио, всичко беше чисто, а цената беше ясна още преди да си запазя час.', 'Педикюр с гел лак')],
  rev_by='Примерен клиент', rev_note='Примерни отзиви. Заменете ги с истински отзиви от Google.',
  k_book='Час', book_h='Избери ден и час.', book_p='Комплектът ти е готов. Избери ден, свободен час и ни кажи кой си.',
  change_set='Промени комплекта', chip_look='Стил, който ти харесва', chip_remove='Премахни', s_day='Избери ден', s_time='Избери час', s_you='За теб', checking='Проверяваме свободните часове…',
  f_time='Час', f_name='Име', f_phone='Телефон', f_msg='Съобщение (по желание)', f_send='Изпрати заявката', f_note='Ползваме данните ти само за да отговорим на заявката ти.', f_priv='Политика за поверителност',
  k_visit='Посети ни', visit_h='Намери студиото', addr_l='Адрес', addr='ул. Примерна 1, Пловдив', hours_l='Работно време', phone_l='Телефон', email_l='Имейл',
  map_t='Картата е от OpenStreetMap и се зарежда само ако поискаш.', map_btn='Покажи картата',
  k_faq='Въпроси', faq_h='Добре е да знаеш',
  faq=[('Колко време отнема посещението?', 'Маникюр с гел лак отнема около 1 до 1,5 часа, а изграждане на нокти – 2 до 3 часа. Конструкторът събира времето вместо теб.'),
       ('Мога ли да донеса снимка на дизайна, който искам?', 'Да. Избери снимка от галерията с идеи, или донеси или изпрати своя, и ще ти кажем доколко можем да я пресъздадем.'),
       ('Свалянето на стар гел включено ли е?', 'Свалянето е отделна услуга. Отбележи „Сваляне на стар гел“ в конструктора, за да се махне старият гел безопасно.'),
       ('Какво става, ако трябва да отменя или закъснея?', 'Предупреди ни поне 24 часа предварително, за да предложим часа на друг клиент. При закъснение над 15 минути може да се наложи услугата да бъде съкратена.'),
       ('Нужен ли е депозит?', 'За изграждане на нокти и по-дълги посещения можем да поискаме малък депозит, който се приспада от цената.')],
  foot_tag='Студио за нокти в Пловдив', foot_priv='Политика за поверителност', admin_t='Демо админ панел', admin_href='admin.html', quick_label='Бърза връзка', q_call='Обади се', q_book='Запази',
  dock_label='Цветова схема',
  lb_label='Снимка', lb_close='Затвори', lb_prev='Предишна снимка', lb_next='Следваща снимка', lb_request='Искам този стил',
 ),
}

TEMPLATE = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'page_template.html'), encoding='utf-8').read()


def build(lang):
    d = L[lang]
    e = lambda s: escape(s, quote=True)
    root = d['root']
    bg = lang == 'bg'
    out = {'lang': lang, 'root': root, 'script': d['script']}
    keys = ['title', 'desc', 'skip', 'nav_label', 'menu_btn', 'cta', 'hero_label', 'lead', 'cta1', 'cta2', 'loading', 'alt1', 'alt2', 'alt3', 'sticker',
            'k_design', 'design_h', 'design_p', 'prev_label', 'o_base', 'o_shape', 'o_colour', 'o_finish', 'o_extras', 'sum_h', 'sum_price', 'sum_time', 'sum_book', 'sum_fine',
            'k_gallery', 'gal_h', 'gal_p', 'gal_filter', 'f_all', 'f_natural', 'f_art', 'f_bold', 'k_rev', 'rev_h', 'rev_note',
            'k_book', 'book_h', 'book_p', 'change_set', 'chip_look', 'chip_remove', 's_day', 's_time', 's_you', 'checking', 'f_time', 'f_name', 'f_phone', 'f_msg', 'f_send', 'f_note', 'f_priv',
            'k_visit', 'visit_h', 'addr_l', 'addr', 'hours_l', 'phone_l', 'email_l', 'map_t', 'map_btn', 'k_faq', 'faq_h',
            'foot_tag', 'foot_priv', 'admin_t', 'quick_label', 'q_call', 'q_book', 'dock_label', 'lb_label', 'lb_close', 'lb_prev', 'lb_next', 'lb_request']
    for k in keys:
        out[k] = e(d[k])
    out['h1'] = d['h1']   # contains <em>
    out['other_href'] = d['other_href']; out['other_lang'] = d['other_lang']; out['other_label'] = d['other_label']; out['other_aria'] = e(d['other_aria'])
    out['privacy_href'] = d['privacy_href']; out['home_href'] = d['home_href']; out['admin_href'] = d['admin_href']
    out['nav_links'] = '\n      '.join('<a href="%s">%s</a>' % (h, e(t)) for h, t in d['nav'])
    out['marquee'] = '<li>' + '</li><li>'.join(e(w) for w in d['marquee']) + '</li>'

    # builder controls
    out['base_opts'] = ''.join(
        '<label class="pl"><input type="radio" name="base" value="%s" data-svc="%s" data-label="%s"%s><span>%s<small>%s</small></span></label>'
        % (v, svc, e(en if not bg else bgn), ' checked' if v == 'nat' else '', e(bgn if bg else en), e(hbg if bg else hen)) for v, svc, en, bgn, hen, hbg in BASES)
    out['shape_opts'] = ''.join(
        '<label class="shp"><input type="radio" name="shape" value="%s" data-label="%s"%s><svg viewBox="0 0 60 84" data-shape="%s" aria-hidden="true"></svg><span>%s</span></label>'
        % (v, e(bgn if bg else en), ' checked' if v == 'almond' else '', v, e(bgn if bg else en)) for v, en, bgn in SHAPES)
    out['colour_opts'] = ''.join(
        '<label class="clr"><input type="radio" name="colour" value="%s" data-label="%s"%s><span class="dot" style="--c:%s" aria-hidden="true"></span><span class="sr-only">%s</span></label>'
        % (hx, e(bgn if bg else en), ' checked' if hx == '#D6246E' else '', hx, e(bgn if bg else en)) for hx, en, bgn in COLOURS)
    out['finish_opts'] = ''.join(
        '<label class="pl"><input type="radio" name="finish" value="%s" data-label="%s" data-art="%d"%s><span>%s</span></label>'
        % (v, e(bgn if bg else en), 1 if art else 0, ' checked' if v == 'gloss' else '', e(bgn if bg else en)) for v, en, bgn, art in FINISHES)
    out['extra_opts'] = ''.join(
        '<label class="pl"><input type="checkbox" name="extra" value="%s" data-svc="%s" data-label="%s"><span>%s</span></label>'
        % (v, svc, e(bgn if bg else en), e(bgn if bg else en)) for v, svc, en, bgn in EXTRAS)
    out['svc_json'] = json.dumps(
        {i[0]: {'name': i[2] if bg else i[1], 'min': i[3], 'p0': i[4], 'p1': i[5], 'kind': i[6]} for i in ITEMS}, ensure_ascii=False)

    gal = []
    for photo, cat, w, h, alt_en, alt_bg in GALLERY:
        alt = e(alt_bg if bg else alt_en)
        gal.append('<button class="g-item" type="button" data-cat="%s" data-full="%simages/stock/%s.jpg" aria-label="%s: %s">'
                   '<img src="%simages/stock/%s-800.jpg" width="800" height="%d" alt="%s" loading="lazy" decoding="async"></button>'
                   % (cat, root, photo, e(d['open_photo']), alt, root, photo, round(800 * h / w), alt))
    out['gallery'] = '\n        '.join(gal)
    out['reviews'] = '\n        '.join('<figure class="rev"><blockquote>%s</blockquote><figcaption><b>%s</b> · %s</figcaption></figure>' % (e(q), e(s), e(d['rev_by'])) for q, s in d['reviews'])
    out['faq'] = '\n          '.join('<details><summary>%s</summary><p>%s</p></details>' % (e(q), e(a)) for q, a in d['faq'])

    out['hours'] = e(hours_text(lang))
    out['phone'] = PHONE_DISPLAY; out['phone_href'] = PHONE_HREF; out['email'] = EMAIL; out['brand'] = e(BRAND)
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
    'window.GLOSSY_CONFIG = {\n'
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
