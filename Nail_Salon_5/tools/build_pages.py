import os, re, json
from html import escape

SHOP = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ---- Edit these placeholders for each salon -------------------------------------------------
OPEN_WEEKDAY = '12:00-22:00'      # opening and closing time, Mon - Fri (a late studio)
OPEN_WEEKEND = '12:00-20:00'      # opening and closing time, Sat - Sun
PHONE_DISPLAY = '+359 000 000 000'
PHONE_HREF = '+359000000000'
EMAIL = 'email@example.com'
# Request system. 'demo' = the booking form talks to a mock server that keeps requests in the visitor's browser.
# 'live' = it sends real HTTP requests to API_BASE (see docs/API.md). Written to js/config.js.
MODE = 'demo'
API_BASE = '/api'
CAPACITY = 2                      # visits that can run at the same time (number of technicians)
SLOT_MINUTES = 30                 # gap between start times
LEAD_MINUTES = 60                 # a same-day request needs this much notice
BRAND = 'Nocturne'
# ---------------------------------------------------------------------------------------------

SKINS = [  # key, colours for the swatch (background, accent), names
    ('orchid', '#0C0710', '#FF3DCB', 'Orchid Night',   'Орхидея нощем'),
    ('acid',   '#0A0D08', '#C8FF2E', 'Acid Lime',      'Кисел лайм'),
    ('ember',  '#100806', '#FF6A3D', 'Ember',          'Жарава'),
    ('ice',    '#060D12', '#5CE1FF', 'Ice Blue',       'Леденосиньо'),
    ('pearl',  '#EEEAF3', '#5B2EFF', 'Pearl Day',      'Перлен ден'),
]
DEFAULT_SKIN = SKINS[0]

# Services behind the set finder (same sample prices as the other nail studios):
# id, name EN, name BG, minutes (longest), price min, price max, kind
ITEMS = [
    ('gel_mani',  'Gel polish manicure', 'Маникюр с гел лак', 90, 25, 25, 'fixed'),
    ('ext_short', 'Gel extensions, short', 'Изграждане с гел, къси нокти', 90, 40, 40, 'fixed'),
    ('ext_med',   'Gel extensions, medium', 'Изграждане с гел, средни нокти', 105, 45, 45, 'fixed'),
    ('ext_long',  'Gel extensions, long', 'Изграждане с гел, дълги нокти', 120, 50, 50, 'fixed'),
    ('art',       'Nail art, French tips, chrome', 'Нейл арт, френски връхчета, хром', 60, 0, 0, 'request'),
    ('gel_pedi',  'Gel polish pedicure', 'Педикюр с гел лак', 90, 25, 30, 'fixed'),
]
# The four looks the set finder can end with: key, file, width, height, name EN, name BG, alt EN, alt BG
LOOKS = {
    'nude':   ('hero-light-pink', 1600, 2553, 'Soft Nude', 'Нежен нюд', 'Soft nude pink gel nails on a white fur surface', 'Нежни телесно-розови гел нокти върху бяла пухкава повърхност'),
    'colour': ('hand-on-pink', 1600, 2400, 'Candy Gloss', 'Бонбонен гланц', 'Rose pink nails against a pink background', 'Розови нокти на розов фон'),
    'chrome': ('mauve-glitter', 1600, 1601, 'Chrome Mirror', 'Хромирано огледало', 'Mauve, white and silver glitter nails on a knit sweater', 'Люляково-розови, бели и сребристи брокатени нокти'),
    'art':    ('navy-gold-white', 1600, 2000, 'Art Piece', 'Арт творба', 'Navy, gold and white nail art on both hands', 'Нейл арт в тъмносиньо, златно и бяло на двете ръце'),
}
# The moving photo columns on the first screen: file, width, height
REEL = [
    [('pink-selective-focus', 1600, 1067), ('black-tortoiseshell', 1600, 2400), ('hand-with-flower', 1600, 2400)],
    [('hero-light-pink', 1600, 2553), ('blue-white-tree', 1600, 1244), ('black-silver-ring', 1600, 1067)],
    [('navy-gold-white', 1600, 2000), ('mauve-glitter', 1600, 1601), ('pink-on-white', 1600, 2133)],
]


def hours_text(lang):
    wd, we = OPEN_WEEKDAY.replace('-', ' – '), OPEN_WEEKEND.replace('-', ' – ')
    return ('Mon – Fri %s · Sat – Sun %s' % (wd, we)) if lang == 'en' else ('Пон – Пет %s · Съб – Нед %s' % (wd, we))


L = {
 'en': dict(
  lang='en', root='../', script='latin', other_href='../index.html', other_lang='bg', other_label='БГ', other_aria='Превключи на български',
  privacy_href='privacy.html', home_href='index.html',
  title='Nocturne – a late-night nail bar in Plovdiv',
  desc='Open until 10 pm. Answer four quick questions, get the nail set that suits you with the price and time, and book a free slot at a late-night nail bar in Plovdiv.',
  skip='Skip to content', tagline='nail bar', nav_label='Page sections', cta='Find my set',
  d1='Start', d2='Find your set', d3='Book', d4='Visit',
  eyebrow='Plovdiv · open until 10 pm', h1='Nails <em>after dark.</em>',
  lead='A late-night nail bar. Tell us your mood in four taps, and we will match you with a set, a price and a time.',
  cta1='Find my set · 60 seconds', cta2='Skip to booking', loading='Checking…',
  ticker=['“It lasted three weeks without a single chip.”', '“I brought a photo and they made exactly that.”', '“A calm studio and the price was clear before I booked.”', '“Gentle with my weak nails.”'],
  ticker_sr='Example reviews: it lasted three weeks without a single chip; I brought a photo and they made exactly that; a calm studio and the price was clear before I booked.', rev_label='Client quotes',
  k_find='Set finder', find_h='Four taps. One set.', find_p='Chat with our set finder. It picks the services, the price and the time for you, and you can still change everything.',
  bot_name='Set finder', bot_role='Four quick questions', restart='Start over', chat_label='Conversation with the set finder',
  res_k='Your set', sum_price='Price', sum_time='Time', res_book='Book this set', skip_quiz='Not in the mood to chat? Book a simple gel manicure instead.',
  k_book='Book', book_h='Pick the night.', book_p='Choose a day on the calendar, a free time, and tell us who you are.',
  sum_h='Your set', need_set='Nothing chosen yet.', need_link='Find my set', change_set='Change my set', cal_prev='Previous month', cal_next='Next month',
  s_day='Pick a day', s_time='Pick a time', s_you='About you', f_hint='Pick a day to see free times.', f_time='Time',
  f_name='Name', f_phone='Phone', f_msg='Message (optional)', f_send='Send the request', f_note='We use your details only to answer your request.', f_priv='Privacy notice',
  k_visit='Visit', visit_h='Find the bar', addr_l='Address', addr='Primer St. 1, Plovdiv', hours_l='Hours', phone_l='Phone', email_l='Email',
  map_t='The map is from OpenStreetMap and loads only if you choose.', map_btn='Show the map',
  k_faq='Questions', faq_h='Good to know',
  faq=[('How long does a visit take?', 'A gel polish manicure takes about 1 to 1.5 hours, and extensions 2 to 3 hours. The set finder adds the time up for you.'),
       ('Can I bring a photo of the design I want?', 'Yes. Bring or send your own photo, and we will tell you how close we can get. Nail art is priced on request.'),
       ('Is removing my old gel included?', 'Removal is a separate service. Tell us in your message and we will add it to your visit.'),
       ('What if I need to cancel or I am late?', 'Please tell us at least 24 hours ahead so we can offer your time to someone else. If you are more than 15 minutes late, the service may need to be shortened.'),
       ('Do I need to pay a deposit?', 'For extensions and longer visits we may ask for a small deposit, which is deducted from the price.')],
  foot_tag='Nail bar in Plovdiv', foot_priv='Privacy notice', admin_t='Demo back office', admin_href='../admin.html?lang=en', quick_label='Quick contact', q_call='Call', q_find='Find my set',
  dock_label='Colour scheme',
  quiz=dict(
    intro='Hi! I am the set finder. Four quick questions and I will find your set.',
    qs=[('occasion', 'What is the occasion?', [('everyday', 'Everyday'), ('date', 'Date night'), ('event', 'A big event'), ('me', 'Just for me')]),
        ('length', 'How long do you like your nails?', [('nat', 'My own nails'), ('short', 'Short'), ('med', 'Medium'), ('long', 'Long')]),
        ('style', 'Pick your finish.', [('nude', 'Soft nude'), ('colour', 'Glossy colour'), ('chrome', 'Chrome and shimmer'), ('art', 'Nail art')]),
        ('pedi', 'A pedicure too?', [('yes', 'Yes, add one'), ('no', 'Not today')])],
    done='Done! Here is your set.',
    occ={'everyday': 'for every day', 'date': 'for a date night', 'event': 'for a big event', 'me': 'just for you'},
  ),
 ),
 'bg': dict(
  lang='bg', root='', script='cyrillic', other_href='en/index.html', other_lang='en', other_label='EN', other_aria='Switch to English',
  privacy_href='privacy.html', home_href='index.html',
  title='Nocturne – нощно студио за нокти в Пловдив',
  desc='Отворено до 22:00. Отговори на четири бързи въпроса, получи комплекта нокти, който ти отива, с цената и времето, и запази свободен час в нощно студио за нокти в Пловдив.',
  skip='Към съдържанието', tagline='студио за нокти', nav_label='Раздели на страницата', cta='Намери комплекта',
  d1='Начало', d2='Намери комплекта', d3='Час', d4='Адрес',
  eyebrow='Пловдив · отворено до 22:00', h1='Нокти <em>след мръкване.</em>',
  lead='Нощно студио за нокти. Кажи ни настроението си с четири докосвания и ще ти намерим комплект, цена и час.',
  cta1='Намери комплекта · 60 секунди', cta2='Към запазването', loading='Проверяваме…',
  ticker=['„Издържа три седмици без нито една цепнатина.“', '„Занесох снимка и направиха точно такъв дизайн.“', '„Спокойно студио, а цената беше ясна още преди да запазя.“', '„Внимателни със слабите ми нокти.“'],
  ticker_sr='Примерни отзиви: издържа три седмици без нито една цепнатина; занесох снимка и направиха точно такъв дизайн; спокойно студио, а цената беше ясна още преди да запазя.', rev_label='Цитати от клиенти',
  k_find='Търсач на комплект', find_h='Четири докосвания. Един комплект.', find_p='Поговори с нашия търсач на комплекти. Той избира услугите, цената и времето вместо теб, а ти можеш да промениш всичко.',
  bot_name='Търсач на комплект', bot_role='Четири бързи въпроса', restart='Започни отначало', chat_label='Разговор с търсача на комплекти',
  res_k='Твоят комплект', sum_price='Цена', sum_time='Време', res_book='Запази този комплект', skip_quiz='Не ти се говори? Запази простичък маникюр с гел лак.',
  k_book='Час', book_h='Избери вечерта.', book_p='Избери ден от календара, свободен час и ни кажи кой си.',
  sum_h='Твоят комплект', need_set='Още нищо не е избрано.', need_link='Намери комплекта', change_set='Промени комплекта', cal_prev='Предишен месец', cal_next='Следващ месец',
  s_day='Избери ден', s_time='Избери час', s_you='За теб', f_hint='Избери ден, за да видиш свободните часове.', f_time='Час',
  f_name='Име', f_phone='Телефон', f_msg='Съобщение (по желание)', f_send='Изпрати заявката', f_note='Ползваме данните ти само за да отговорим на заявката ти.', f_priv='Политика за поверителност',
  k_visit='Посети ни', visit_h='Намери студиото', addr_l='Адрес', addr='ул. Примерна 1, Пловдив', hours_l='Работно време', phone_l='Телефон', email_l='Имейл',
  map_t='Картата е от OpenStreetMap и се зарежда само ако поискаш.', map_btn='Покажи картата',
  k_faq='Въпроси', faq_h='Добре е да знаеш',
  faq=[('Колко време отнема посещението?', 'Маникюр с гел лак отнема около 1 до 1,5 часа, а изграждане на нокти – 2 до 3 часа. Търсачът на комплекти събира времето вместо теб.'),
       ('Мога ли да донеса снимка на дизайна, който искам?', 'Да. Донеси или изпрати своя снимка и ще ти кажем доколко можем да я пресъздадем. Нейл артът се оценява по запитване.'),
       ('Свалянето на стар гел включено ли е?', 'Свалянето е отделна услуга. Кажи ни в съобщението и ще го добавим към посещението ти.'),
       ('Какво става, ако трябва да отменя или закъснея?', 'Предупреди ни поне 24 часа предварително, за да предложим часа на друг клиент. При закъснение над 15 минути може да се наложи услугата да бъде съкратена.'),
       ('Нужен ли е депозит?', 'За изграждане на нокти и по-дълги посещения можем да поискаме малък депозит, който се приспада от цената.')],
  foot_tag='Студио за нокти в Пловдив', foot_priv='Политика за поверителност', admin_t='Демо админ панел', admin_href='admin.html', quick_label='Бърза връзка', q_call='Обади се', q_find='Намери комплекта',
  dock_label='Цветова схема',
  quiz=dict(
    intro='Здравей! Аз съм търсачът на комплекти. Четири бързи въпроса и ще намеря твоя комплект.',
    qs=[('occasion', 'Какъв е поводът?', [('everyday', 'За всеки ден'), ('date', 'Вечер навън'), ('event', 'Голямо събитие'), ('me', 'Просто за мен')]),
        ('length', 'Колко дълги обичаш ноктите си?', [('nat', 'Моите нокти'), ('short', 'Къси'), ('med', 'Средни'), ('long', 'Дълги')]),
        ('style', 'Избери финиш.', [('nude', 'Нежен нюд'), ('colour', 'Лъскав цвят'), ('chrome', 'Хром и блясък'), ('art', 'Нейл арт')]),
        ('pedi', 'И педикюр?', [('yes', 'Да, добави'), ('no', 'Не днес')])],
    done='Готово! Ето твоя комплект.',
    occ={'everyday': 'за всеки ден', 'date': 'за вечер навън', 'event': 'за голямо събитие', 'me': 'просто за теб'},
  ),
 ),
}

TEMPLATE = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'page_template.html'), encoding='utf-8').read()


def build(lang):
    d = L[lang]
    e = lambda s: escape(s, quote=True)
    root = d['root']
    bg = lang == 'bg'
    out = {'lang': lang, 'root': root, 'script': d['script']}
    keys = ['title', 'desc', 'skip', 'tagline', 'nav_label', 'cta', 'd1', 'd2', 'd3', 'd4', 'eyebrow', 'lead', 'cta1', 'cta2', 'loading', 'ticker_sr', 'rev_label',
            'k_find', 'find_h', 'find_p', 'bot_name', 'bot_role', 'restart', 'chat_label', 'res_k', 'sum_price', 'sum_time', 'res_book', 'skip_quiz',
            'k_book', 'book_h', 'book_p', 'sum_h', 'need_set', 'need_link', 'change_set', 'cal_prev', 'cal_next', 's_day', 's_time', 's_you', 'f_hint', 'f_time',
            'f_name', 'f_phone', 'f_msg', 'f_send', 'f_note', 'f_priv', 'k_visit', 'visit_h', 'addr_l', 'addr', 'hours_l', 'phone_l', 'email_l', 'map_t', 'map_btn',
            'k_faq', 'faq_h', 'foot_tag', 'foot_priv', 'admin_t', 'quick_label', 'q_call', 'q_find', 'dock_label']
    for k in keys:
        out[k] = e(d[k])
    out['h1'] = d['h1']   # contains <em>
    out['other_href'] = d['other_href']; out['other_lang'] = d['other_lang']; out['other_label'] = d['other_label']; out['other_aria'] = e(d['other_aria'])
    out['privacy_href'] = d['privacy_href']; out['home_href'] = d['home_href']; out['admin_href'] = d['admin_href']
    out['ticker'] = '<li>' + '</li><li>'.join(e(t) for t in d['ticker']) + '</li>'

    cols = []
    for n, col in enumerate(REEL):
        imgs = ''.join('<img src="%simages/stock/%s-800.jpg" width="800" height="%d" alt="" loading="%s" decoding="async">' % (root, f, round(800 * h / w), 'eager' if n == 0 and i == 0 else 'lazy')
                       for i, (f, w, h) in enumerate(col))
        dup = ''.join('<img src="%simages/stock/%s-800.jpg" width="800" height="%d" alt="" loading="lazy" decoding="async">' % (root, f, round(800 * h / w)) for f, w, h in col)
        cols.append('<div class="rcol c%d"><div class="rtrack">%s%s</div></div>' % (n + 1, imgs, dup))
    out['reel'] = '\n      '.join(cols)

    q = d['quiz']
    quiz = {
        'intro': q['intro'], 'done': q['done'], 'occ': q['occ'],
        'qs': [{'key': k, 'q': t, 'opts': [{'v': v, 'label': lab} for v, lab in opts]} for k, t, opts in q['qs']],
        'looks': {k: {'src': '%simages/stock/%s-800.jpg' % (root, v[0]), 'w': 800, 'h': round(800 * v[2] / v[1]), 'name': v[4] if bg else v[3], 'alt': v[6] if bg else v[5]} for k, v in LOOKS.items()},
        'svc': {i[0]: {'name': i[2] if bg else i[1], 'min': i[3], 'p0': i[4], 'p1': i[5], 'kind': i[6]} for i in ITEMS},
    }
    out['quiz_json'] = json.dumps(quiz, ensure_ascii=False)
    out['faq'] = '\n          '.join('<details><summary>%s</summary><p>%s</p></details>' % (e(qq), e(a)) for qq, a in d['faq'])
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
    # the quiz data goes in as a JSON script right before the other scripts
    html = html.replace('<script src="[[root]]js/config.js"></script>', '<script type="application/json" id="quizData">[[quiz_json]]</script>\n<script src="[[root]]js/config.js"></script>')
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
    'window.NOCTURNE_CONFIG = {\n'
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
