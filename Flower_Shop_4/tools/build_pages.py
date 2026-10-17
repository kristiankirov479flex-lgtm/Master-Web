import os, re, json
from html import escape

SHOP = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ---- Edit these placeholders for each studio ------------------------------------------------
OPEN_WEEKDAY = '10:00-18:00'      # consultation hours, Mon - Fri (by appointment)
OPEN_WEEKEND = '10:00-14:00'      # consultation hours, Sat - Sun
PHONE_DISPLAY = '+359 000 000 000'
PHONE_HREF = '+359000000000'
EMAIL = 'email@example.com'
# Request system. 'demo' = the form talks to a mock server that keeps requests in the visitor's browser.
# 'live' = it sends real HTTP requests to API_BASE (see docs/API.md). Written to js/config.js.
MODE = 'demo'
API_BASE = '/api'
CAPACITY = 1                      # consultations that can run at the same time
SLOT_MINUTES = 30                 # gap between start times
LEAD_MINUTES = 0
CONSULT_MINUTES = 45              # length of a consultation
BRAND = 'Atelier Aubade'
# ---------------------------------------------------------------------------------------------

SKINS = [  # key, colours for the swatch (background, accent), names
    ('evergreen', '#0F1F19', '#D8B56A', 'Evergreen and Gold',  'Горско зелено и злато'),
    ('ivory',     '#F8F3EA', '#8A5A44', 'Ivory and Clay',      'Слонова кост и глина'),
    ('blush',     '#F9ECEA', '#9A3F55', 'Blush and Rouge',     'Руж и пудра'),
    ('midnight',  '#0E1426', '#E3B7A0', 'Midnight and Rose Gold', 'Полунощ и розово злато'),
    ('plum',      '#1E0F1F', '#E6A9C5', 'Plum and Petal',      'Слива и венчелистче'),
]
DEFAULT_SKIN = SKINS[0]


def dims(f):
    try:
        from PIL import Image
        return Image.open(os.path.join(SHOP, 'images', 'stock', f + '.jpg')).size
    except Exception:
        return (1600, 1067)


# Hero contact sheet photos, in grid order
SHEET = ['red-white-bouquet', 'rose-bouquet', 'pink-white-roses', 'holding-bouquet', 'arranging-vase', 'roses-hydrangeas']
# Stories: photo, place + kind EN, BG, style EN, BG, guests
STORIES = [
    ('beige-bouquet',          'Wedding, Plovdiv Old Town', 'Сватба, Старият Пловдив', 'Soft and neutral', 'Нежно и неутрално'),
    ('pink-grey-vase',         'Birthday dinner, Hisarya', 'Рожден ден, Хисаря', 'Pastel dream', 'Пастелна мечта'),
    ('poppies-amber-vase',     'Garden wedding, Brestovitsa', 'Градинска сватба, Брестовица', 'Garden wild', 'Градинско и диво'),
    ('red-arrangement',        'Anniversary, Plovdiv', 'Годишнина, Пловдив', 'Romantic', 'Романтично'),
    ('white-purple-black-vase','Corporate evening, Sofia', 'Фирмена вечер, София', 'Moody', 'Тъмно и драматично'),
    ('tulips',                 'Spring brunch, Plovdiv', 'Пролетен брънч, Пловдив', 'Minimal', 'Семпло'),
]
# Styles for the moodboard step: id, photo, name EN, BG
STYLES = [
    ('romantic', 'pink-roses',          'Romantic',    'Романтично'),
    ('wild',     'hand-colorful-bouquet', 'Garden wild', 'Градинско и диво'),
    ('minimal',  'beige-bouquet',       'Minimal',     'Семпло'),
    ('rustic',   'dried-peach-paper',   'Rustic',      'Селско'),
    ('moody',    'white-purple-black-vase', 'Moody',   'Тъмно и драматично'),
    ('pastel',   'pink-glass-vase',     'Pastel dream', 'Пастелна мечта'),
]
EVENTS = [('wedding', 'Wedding', 'Сватба'), ('birthday', 'Birthday', 'Рожден ден'), ('corporate', 'Corporate event', 'Фирмено събитие'), ('other', 'Something else', 'Нещо друго')]
# Pieces: id, name EN, name BG, min price, max price, per item?, max count, default count
PIECES = [
    ('bouquet', 'Main bouquet', 'Основен букет', 90, 160, False, 1, 1),
    ('small',   'Smaller bouquets', 'По-малки букети', 40, 65, True, 8, 0),
    ('button',  'Buttonholes', 'Бутониери', 8, 12, True, 12, 0),
    ('arch',    'Welcome arch or backdrop', 'Арка или фон при входа', 250, 650, False, 1, 0),
    ('aisle',   'Aisle or entrance arrangements', 'Аранжировки за пътеката или входа', 30, 55, True, 10, 0),
    ('tables',  'Table centrepieces', 'Центрове за маси', 30, 65, True, 30, 0),
    ('cake',    'Cake flowers', 'Цветя за торта', 25, 45, False, 1, 0),
    ('car',     'Car decoration', 'Украса за кола', 45, 80, False, 1, 0),
]
# Packages: id, name EN, name BG, text EN, text BG, includes EN, includes BG, preset counts ('tables' = one per 8 guests at 80 guests)
PACKS = [
    ('bridal', 'The Bouquet', 'Букетът', 'For small ceremonies or a registry office.', 'За малки церемонии или за граждански брак.',
     ['Main bouquet', '2 buttonholes', 'Delivery to the venue'], ['Основен букет', '2 бутониери', 'Доставка до мястото'], {'bouquet': 1, 'button': 2}),
    ('ceremony', 'The Ceremony', 'Церемонията', 'The ceremony dressed in flowers.', 'Церемонията, облечена в цветя.',
     ['Main bouquet and 3 smaller ones', '4 buttonholes', 'Welcome arch or backdrop', '4 aisle arrangements', 'Setup at the venue'], ['Основен букет и 3 по-малки', '4 бутониери', 'Арка или фон при входа', '4 аранжировки за пътеката', 'Подреждане на мястото'],
     {'bouquet': 1, 'small': 3, 'button': 4, 'arch': 1, 'aisle': 4}),
    ('full', 'The Whole Day', 'Целият ден', 'From the first bouquet to the last table.', 'От първия букет до последната маса.',
     ['Everything in The Ceremony, plus', '10 table centrepieces', 'Cake flowers and car decoration', 'A planning visit to the venue'], ['Всичко от „Церемонията“, плюс', '10 центъра за маси', 'Цветя за торта и украса за кола', 'Оглед на мястото'],
     {'bouquet': 1, 'small': 4, 'button': 6, 'arch': 1, 'aisle': 6, 'tables': 10, 'cake': 1, 'car': 1}),
]


def pack_from(preset):
    P = {p[0]: p for p in PIECES}
    return sum(P[k][3] * v for k, v in preset.items())


def hours_text(lang):
    wd, we = OPEN_WEEKDAY.replace('-', ' – '), OPEN_WEEKEND.replace('-', ' – ')
    return ('Mon – Fri %s · Sat – Sun %s' % (wd, we)) if lang == 'en' else ('Пон – Пет %s · Съб – Нед %s' % (wd, we))


L = {
 'en': dict(
  lang='en', root='../', script='latin', other_href='../index.html', other_lang='bg', other_label='БГ', other_aria='Превключи на български',
  privacy_href='privacy.html', home_href='index.html',
  title='Atelier Aubade – wedding and event florist in Plovdiv',
  desc='A florist for weddings and events in Plovdiv. Plan your flowers online, see a price range, and book a free consultation.',
  skip='Skip to content', tagline='wedding and event florist', nav_label='Main navigation', menu_btn='Menu',
  nav=[('#stories', 'Stories'), ('#packages', 'Packages'), ('#plan', 'Plan'), ('#process', 'Process'), ('#contact', 'Studio')],
  cta='Book a consultation',
  eyebrow='Plovdiv · weddings and events', h1='Flowers for the day <em>you will remember.</em>',
  lead='We design and arrange flowers for weddings, birthdays and company evenings. Plan yours below, see a price range, and talk to us for free.',
  cta1='Plan my flowers', cta2='See our stories', kinds=['Weddings', 'Birthdays', 'Corporate'],
  k_stories='Stories', stories_h='Days we have dressed in flowers.', stories_p='A few recent events, with the style we chose together. Swipe or use the arrows.', rail_prev='Previous stories', rail_next='Next stories',
  k_packages='Packages', packages_h='Three places to start.', packages_p='Every event is different, so these are starting points. Press one and the planner below fills itself in.', from_l='from', add_pack='Start with this',
  k_plan='Planner', plan_h='Plan your flowers. See what it costs.', plan_p='Choose the event, the style and the pieces. You get a price range straight away, and a free consultation to make it real.',
  o_event='What are we celebrating?', o_guests='Guests', o_style='Your style', o_style_h='Pick up to three that feel like you.', o_pieces='What do you need?', o_consult='Book a free consultation', consult_p='Forty-five minutes, in the studio. Bring photos, fabric swatches and questions.',
  checking='Pick a day to see free times.', f_time='Time', o_you='About you and the day', f_name='Your name', f_phone='Phone', f_event_date='Date of the event', f_venue='Venue (if you know)', f_msg='Anything else? (optional)',
  tables_hint='About {n} tables of 8', brief_h='Your plan', est_l='Estimated range', est_fine='A first estimate from sample prices. The real proposal follows the consultation.', none_yet='Pick the pieces you need.', styles_none='No style picked yet',
  f_send='Book the consultation', f_note='We use your details only to answer your request.', f_priv='Privacy notice', pcs='×', each='each',
  k_process='Process', process_h='From the first chat to the last petal.', process_p='Clear steps, so nothing is left to chance.',
  steps=[('Free consultation', '45 minutes in the studio. We hear the story, the venue and the budget.'), ('Proposal and moodboard', 'Within three days you get a written proposal with a moodboard.'), ('Date secured', 'A deposit confirms your date. Sample prices: 30% of the proposal.'), ('The day', 'We arrange, deliver and set up at the venue, and take care of the details.')],
  k_rev='Kind words', rev_h='What couples and hosts say',
  reviews=[('They listened, then made something better than the picture I had in my head.', 'Wedding, 90 guests'), ('Every table looked different and every one was beautiful. Guests asked who did the flowers.', 'Birthday dinner'), ('Calm, punctual and tidy. The venue manager asked for their number.', 'Corporate evening')],
  rev_by='Example client', rev_note='Example reviews. Replace them with real reviews.',
  k_faq='Questions', faq_h='Good to know',
  faq=[('How far ahead should I book?', 'For weddings, three to six months ahead is comfortable, and peak weekends go first. For smaller events, a few weeks is usually fine.'), ('Is the consultation really free?', 'Yes. It takes 45 minutes in the studio and does not oblige you to anything.'), ('Do you deliver and set up?', 'Yes. Delivery and setup at your venue are part of the proposal. Travel outside Plovdiv is priced separately.'), ('How does the deposit work?', 'A deposit (sample: 30%) secures your date and is deducted from the final price.'), ('Can I see flowers before I decide?', 'In the consultation we show seasonal stems and sample arrangements.')],
  k_visit='Studio', visit_h='Visit the studio', addr_l='Address', addr='Primer St. 1, Plovdiv', hours_l='Consultations', phone_l='Phone', email_l='Email',
  map_t='The map is from OpenStreetMap and loads only if you choose.', map_btn='Show the map',
  foot_tag='Wedding and event florist in Plovdiv', foot_priv='Privacy notice', admin_t='Demo back office', admin_href='../admin.html?lang=en', quick_label='Quick contact', q_call='Call', q_plan='Plan',
  dock_label='Colour scheme',
 ),
 'bg': dict(
  lang='bg', root='', script='cyrillic', other_href='en/index.html', other_lang='en', other_label='EN', other_aria='Switch to English',
  privacy_href='privacy.html', home_href='index.html',
  title='Atelier Aubade – цветарка за сватби и събития в Пловдив',
  desc='Цветарка за сватби и събития в Пловдив. Планирай цветята си онлайн, виж ценови диапазон и запази безплатна консултация.',
  skip='Към съдържанието', tagline='цветарка за сватби и събития', nav_label='Основна навигация', menu_btn='Меню',
  nav=[('#stories', 'Истории'), ('#packages', 'Пакети'), ('#plan', 'Планиране'), ('#process', 'Процес'), ('#contact', 'Ателие')],
  cta='Запази консултация',
  eyebrow='Пловдив · сватби и събития', h1='Цветя за деня, <em>който ще помните.</em>',
  lead='Проектираме и подреждаме цветя за сватби, рождени дни и фирмени вечери. Планирай своите по-долу, виж ценови диапазон и говори с нас безплатно.',
  cta1='Планирай цветята ми', cta2='Виж историите ни', kinds=['Сватби', 'Рождени дни', 'Фирмени събития'],
  k_stories='Истории', stories_h='Дни, които облякохме в цветя.', stories_p='Няколко скорошни събития със стила, който избрахме заедно. Плъзни или ползвай стрелките.', rail_prev='Предишни истории', rail_next='Следващи истории',
  k_packages='Пакети', packages_h='Три места, от които да тръгнеш.', packages_p='Всяко събитие е различно, затова това са отправни точки. Натисни един и планерът по-долу се попълва сам.', from_l='от', add_pack='Започни с този',
  k_plan='Планер', plan_h='Планирай цветята си. Виж колко струва.', plan_p='Избери събитието, стила и елементите. Получаваш ценови диапазон веднага и безплатна консултация, за да го направим истински.',
  o_event='Какво празнуваме?', o_guests='Гости', o_style='Твоят стил', o_style_h='Избери до три, които ти приличат.', o_pieces='Какво ти трябва?', o_consult='Запази безплатна консултация', consult_p='Четиридесет и пет минути в ателието. Носи снимки, мостри от плат и въпроси.',
  checking='Избери ден, за да видиш свободните часове.', f_time='Час', o_you='За теб и за деня', f_name='Твоето име', f_phone='Телефон', f_event_date='Дата на събитието', f_venue='Място (ако го знаеш)', f_msg='Нещо друго? (по желание)',
  tables_hint='Около {n} маси по 8', brief_h='Твоят план', est_l='Приблизителен диапазон', est_fine='Първа оценка по примерни цени. Истинското предложение идва след консултацията.', none_yet='Избери елементите, от които имаш нужда.', styles_none='Още няма избран стил',
  f_send='Запази консултацията', f_note='Ползваме данните ти само за да отговорим на заявката ти.', f_priv='Политика за поверителност', pcs='×', each='всеки',
  k_process='Процес', process_h='От първия разговор до последното венчелистче.', process_p='Ясни стъпки, за да не остава нищо на случайността.',
  steps=[('Безплатна консултация', '45 минути в ателието. Чуваме историята, мястото и бюджета.'), ('Предложение и мудборд', 'До три дни получаваш писмено предложение с мудборд.'), ('Запазена дата', 'Депозит потвърждава датата ти. Примерно: 30% от предложението.'), ('Денят', 'Подреждаме, доставяме и монтираме на мястото и се грижим за детайлите.')],
  k_rev='Добри думи', rev_h='Какво казват младоженците и домакините',
  reviews=[('Изслушаха ни и направиха нещо по-хубаво от картинката в главата ми.', 'Сватба, 90 гости'), ('Всяка маса изглеждаше различно и всяка беше красива. Гостите питаха кой е правил цветята.', 'Вечеря за рожден ден'), ('Спокойни, точни и подредени. Управителят на залата поиска телефона им.', 'Фирмена вечер')],
  rev_by='Примерен клиент', rev_note='Примерни отзиви. Заменете ги с истински.',
  k_faq='Въпроси', faq_h='Добре е да знаеш',
  faq=[('Колко рано да запазя?', 'За сватби е удобно три до шест месеца напред, а най-търсените събота и неделя си отиват първи. За по-малки събития обикновено стигат няколко седмици.'), ('Наистина ли е безплатна консултацията?', 'Да. Отнема 45 минути в ателието и не те задължава за нищо.'), ('Доставяте ли и подреждате ли на мястото?', 'Да. Доставката и подреждането на мястото са част от предложението. Пътуване извън Пловдив се оценява отделно.'), ('Как работи депозитът?', 'Депозит (примерно 30%) запазва датата ти и се приспада от крайната цена.'), ('Мога ли да видя цветята, преди да реша?', 'На консултацията показваме сезонни цветя и примерни аранжировки.')],
  k_visit='Ателие', visit_h='Посети ателието', addr_l='Адрес', addr='ул. Примерна 1, Пловдив', hours_l='Консултации', phone_l='Телефон', email_l='Имейл',
  map_t='Картата е от OpenStreetMap и се зарежда само ако поискаш.', map_btn='Покажи картата',
  foot_tag='Цветарка за сватби и събития в Пловдив', foot_priv='Политика за поверителност', admin_t='Демо админ панел', admin_href='admin.html', quick_label='Бърза връзка', q_call='Обади се', q_plan='Планирай',
  dock_label='Цветова схема',
 ),
}

TEMPLATE = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'page_template.html'), encoding='utf-8').read()


def build(lang):
    d = L[lang]
    e = lambda s: escape(s, quote=True)
    root = d['root']
    bg = lang == 'bg'
    out = {'lang': lang, 'root': root, 'script': d['script']}
    keys = ['title', 'desc', 'skip', 'tagline', 'nav_label', 'menu_btn', 'cta', 'eyebrow', 'lead', 'cta1', 'cta2', 'k_stories', 'stories_h', 'stories_p', 'rail_prev', 'rail_next',
            'k_packages', 'packages_h', 'packages_p', 'k_plan', 'plan_h', 'plan_p', 'o_event', 'o_guests', 'o_style', 'o_style_h', 'o_pieces', 'o_consult', 'consult_p', 'checking', 'f_time',
            'o_you', 'f_name', 'f_phone', 'f_event_date', 'f_venue', 'f_msg', 'brief_h', 'est_l', 'est_fine', 'f_send', 'f_note', 'f_priv',
            'k_process', 'process_h', 'process_p', 'k_rev', 'rev_h', 'rev_note', 'k_faq', 'faq_h', 'k_visit', 'visit_h', 'addr_l', 'addr', 'hours_l', 'phone_l', 'email_l', 'map_t', 'map_btn',
            'foot_tag', 'foot_priv', 'admin_t', 'quick_label', 'q_call', 'q_plan', 'dock_label']
    for k in keys:
        out[k] = e(d[k])
    out['h1'] = d['h1']
    out['other_href'] = d['other_href']; out['other_lang'] = d['other_lang']; out['other_label'] = d['other_label']; out['other_aria'] = e(d['other_aria'])
    out['privacy_href'] = d['privacy_href']; out['home_href'] = d['home_href']; out['admin_href'] = d['admin_href']
    out['nav_links'] = '\n      '.join('<a href="%s">%s</a>' % (h, e(t)) for h, t in d['nav'])
    out['kinds'] = ''.join('<li>%s</li>' % e(k) for k in d['kinds'])

    cls = ['s1', 's2', 's3', 's4', 's5', 's6']
    out['sheet'] = '\n      '.join('<img class="%s" src="%simages/stock/%s%s.jpg" width="%d" height="%d" alt="" loading="%s" decoding="async">'
                                 % (cls[i], root, f, '' if i in (3, 4) else '-800', 1600 if i in (3, 4) else 800, dims(f)[1] if i in (3, 4) else round(800 * dims(f)[1] / dims(f)[0]), 'eager' if i == 0 else 'lazy') for i, f in enumerate(SHEET))
    out['stories'] = '\n      '.join(
        '<figure class="story"><img src="%simages/stock/%s-800.jpg" width="800" height="%d" alt="" loading="lazy" decoding="async"><figcaption><b>%s</b><span>%s</span></figcaption></figure>'
        % (root, f, round(800 * dims(f)[1] / dims(f)[0]), e(pbg if bg else pen), e(sbg if bg else sen)) for f, pen, pbg, sen, sbg in STORIES)

    packs = []
    for pid, nen, nbg, ten, tbg, inen, inbg, preset in PACKS:
        packs.append('<article class="pack"><h3>%s</h3><p class="pack-t">%s</p><ul>%s</ul><p class="pack-p"><small>%s</small> <b>%d €</b></p>'
                     '<button class="btn btn-line" type="button" data-pack="%s">%s</button></article>'
                     % (e(nbg if bg else nen), e(tbg if bg else ten), ''.join('<li>%s</li>' % e(x) for x in (inbg if bg else inen)),
                        e(d['from_l']), pack_from(preset), pid, e(d['add_pack'])))
    out['packs'] = '\n        '.join(packs)
    out['event_opts'] = ''.join('<label class="pl"><input type="radio" name="event" value="%s" data-name="%s"%s><span>%s</span></label>'
                                % (v, e(nbg if bg else nen), ' checked' if v == 'wedding' else '', e(nbg if bg else nen)) for v, nen, nbg in EVENTS)
    out['style_opts'] = ''.join('<label class="sty"><input type="checkbox" name="style" value="%s" data-name="%s"><img src="%simages/stock/%s-800.jpg" alt="" width="400" height="%d" loading="lazy" decoding="async"><span>%s</span></label>'
                                % (sid, e(nbg if bg else nen), root, f, round(400 * dims(f)[1] / dims(f)[0]), e(nbg if bg else nen)) for sid, f, nen, nbg in STYLES)

    out['timeline'] = '\n        '.join('<li><h3>%s</h3><p>%s</p></li>' % (e(t), e(p)) for t, p in d['steps'])
    out['reviews'] = '\n        '.join('<figure class="rev"><blockquote>%s</blockquote><figcaption><b>%s</b> · %s</figcaption></figure>' % (e(q), e(s), e(d['rev_by'])) for q, s in d['reviews'])
    out['faq'] = '\n          '.join('<details><summary>%s</summary><p>%s</p></details>' % (e(q), e(a)) for q, a in d['faq'])

    data = {
        'pieces': [{'id': p[0], 'name': p[2] if bg else p[1], 'min': p[3], 'max': p[4], 'per': p[5], 'cap': p[6], 'def': p[7]} for p in PIECES],
        'packs': {p[0]: p[7] for p in PACKS}, 'consult': CONSULT_MINUTES,
        'tablesHint': d['tables_hint'], 'noneYet': d['none_yet'], 'stylesNone': d['styles_none'], 'each': d['each'],
    }
    out['data_json'] = json.dumps(data, ensure_ascii=False)
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
    'window.AUBADE_CONFIG = {\n'
    '  mode: "%s",            /* "demo" = requests are kept in this browser only; "live" = real API at apiBase (docs/API.md) */\n'
    '  apiBase: "%s",\n'
    '  hours: { weekday: ["%s", "%s"], weekend: ["%s", "%s"] },\n'
    '  capacity: %d,             /* consultations that can run at the same time */\n'
    '  slotMinutes: %d,\n'
    '  leadMinutes: %d,\n'
    '  latency: [600, 1100]      /* demo only: pretend network delay in milliseconds */\n'
    '};\n'
) % (MODE, API_BASE, OPEN_WEEKDAY.split('-')[0], OPEN_WEEKDAY.split('-')[1], OPEN_WEEKEND.split('-')[0], OPEN_WEEKEND.split('-')[1], CAPACITY, SLOT_MINUTES, LEAD_MINUTES)
os.makedirs(os.path.join(SHOP, 'js'), exist_ok=True)
open(os.path.join(SHOP, 'js', 'config.js'), 'w', encoding='utf-8').write(cfg)
print('config.js written')
