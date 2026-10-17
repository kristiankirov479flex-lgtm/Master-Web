import os, re, json
from html import escape

SHOP = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ---- Edit these placeholders for each shop ---------------------------------------------------
OPEN_WEEKDAY = '09:00-19:00'      # opening and closing time, Mon - Fri (delivery windows start in these hours)
OPEN_WEEKEND = '10:00-16:00'      # opening and closing time, Sat - Sun
PHONE_DISPLAY = '+359 000 000 000'
PHONE_HREF = '+359000000000'
EMAIL = 'email@example.com'
# Request system. 'demo' = the form talks to a mock server that keeps requests in the visitor's browser.
# 'live' = it sends real HTTP requests to API_BASE (see docs/API.md). Written to js/config.js.
MODE = 'demo'
API_BASE = '/api'
CAPACITY = 6                      # deliveries that can start in the same time window
SLOT_MINUTES = 60                 # gap between delivery windows
LEAD_MINUTES = 0                  # (the first delivery is at least two days ahead, see js/main.js)
BRAND = 'Sunday Stems'
# ---------------------------------------------------------------------------------------------

SKINS = [  # key, colours for the swatch (background, accent), names
    ('tulip', '#FFF6EE', '#C93A1F', 'Tulip Red',     'Лале червено'),
    ('lemon', '#FFFBE6', '#1B6B45', 'Lemon and Leaf', 'Лимон и листо'),
    ('peony', '#FFF1F5', '#B8236B', 'Peony Pink',    'Божур розово'),
    ('iris',  '#F3F0FF', '#5A33C9', 'Iris Purple',   'Ирис лилаво'),
    ('sage',  '#F1F5EC', '#2F6B3F', 'Sage Green',    'Шалфей зелено'),
]
DEFAULT_SKIN = SKINS[0]


def dims(f):
    try:
        from PIL import Image
        return Image.open(os.path.join(SHOP, 'images', 'stock', f + '.jpg')).size
    except Exception:
        return (1600, 1067)


# Sizes: id, price per delivery (EUR), photo, name EN, name BG, stems EN, stems BG
SIZES = [
    ('petite',  18, 'pink-glass-vase',       'Petite',  'Малък',  'About 12 stems in a small vase wrap', 'Около 12 стръка в малка опаковка'),
    ('classic', 28, 'hand-colorful-bouquet', 'Classic', 'Класик', 'About 20 stems, our everyday bouquet', 'Около 20 стръка, нашият всекидневен букет'),
    ('grand',   42, 'roses-hydrangeas',      'Grand',   'Голям',  'About 35 stems for a statement', 'Около 35 стръка за впечатляващ ефект'),
]
# Rhythm: id, days between deliveries, deliveries per month, name EN, name BG
FREQS = [
    ('weekly',   7,  4.33, 'Every week', 'Всяка седмица'),
    ('biweekly', 14, 2.17, 'Every 2 weeks', 'На 2 седмици'),
    ('monthly',  28, 1.0,  'Once a month', 'Веднъж месечно'),
]
# Length: id, number of deliveries (0 = until I stop), discount percent, name EN, name BG
LENS = [
    ('4',    4,  0,  'Try 4 deliveries', 'Пробвай с 4 доставки'),
    ('12',   12, 10, '12 deliveries', '12 доставки'),
    ('open', 0,  5,  'Until I stop', 'Докато спра'),
]
VASE_PRICE = 12
# This week's bouquets (the page shows one by the week of the year): name EN, name BG, stems EN, stems BG, photo
WEEKLY = [
    ('Peach Parade', 'Прасковен парад', 'Ranunculus, spray roses, eucalyptus', 'Ранункулуси, дребни рози, евкалипт', 'pink-roses'),
    ('Garden Walk', 'Разходка в градината', 'Sweet peas, snapdragons, green fern', 'Сладък грах, лъвски зев, зелена папрат', 'mixed-glass-vase'),
    ('Tulip Tuesday', 'Лалета във вторник', 'Tulips, ranunculus, tulip foliage', 'Лалета, ранункулуси, листа от лале', 'tulips'),
    ('Poppy Fields', 'Макови поля', 'Poppies, wild grasses, chamomile', 'Макове, диви треви, лайка', 'poppies-amber-vase'),
    ('Rose and Hydrangea', 'Роза и хортензия', 'Roses, hydrangea, lisianthus', 'Рози, хортензия, лизиантус', 'roses-hydrangeas'),
    ('Dried and Dreamy', 'Сухо и нежно', 'Dried grasses, strawflower, preserved eucalyptus', 'Сухи треви, сламено цвете, консервиран евкалипт', 'beige-bouquet'),
]
# What is in season: 12 months, each with three flowers (EN, BG) and three colours
MONTHS = [
    (('Anemones', 'Hellebores', 'Ranunculus'), ('Анемонии', 'Хелебори', 'Ранункулуси'), ('#F4B6C2', '#E8D9F5', '#FFD08A')),
    (('Tulips', 'Daffodils', 'Anemones'), ('Лалета', 'Нарциси', 'Анемонии'), ('#FF8A7A', '#FFE066', '#C9A7F5')),
    (('Daffodils', 'Hyacinths', 'Tulips'), ('Нарциси', 'Зюмбюли', 'Лалета'), ('#FFE066', '#9EC9FF', '#FF9CC4')),
    (('Tulips', 'Lilac', 'Peonies'), ('Лалета', 'Люляк', 'Божури'), ('#FF6F61', '#C9A7F5', '#FFB3C7')),
    (('Peonies', 'Lilac', 'Sweet peas'), ('Божури', 'Люляк', 'Сладък грах'), ('#FF9CC4', '#C9A7F5', '#FFD3E0')),
    (('Roses', 'Delphinium', 'Peonies'), ('Рози', 'Делфиниум', 'Божури'), ('#E5446D', '#6C8CFF', '#FFB3C7')),
    (('Sunflowers', 'Zinnias', 'Lavender'), ('Слънчогледи', 'Цинии', 'Лавандула'), ('#FFC21A', '#FF7A59', '#9B7BD8')),
    (('Dahlias', 'Zinnias', 'Gladioli'), ('Далии', 'Цинии', 'Гладиоли'), ('#E5446D', '#FF9A3D', '#FF9CC4')),
    (('Dahlias', 'Asters', 'Chrysanthemums'), ('Далии', 'Астри', 'Хризантеми'), ('#B3261E', '#9B7BD8', '#FFC21A')),
    (('Chrysanthemums', 'Rose hips', 'Dried grasses'), ('Хризантеми', 'Шипки', 'Сухи треви'), ('#FF9A3D', '#E5446D', '#D9C7A0')),
    (('Chrysanthemums', 'Eucalyptus', 'Berries'), ('Хризантеми', 'Евкалипт', 'Горски плодове'), ('#FFFFFF', '#8FB8A0', '#B3261E')),
    (('Amaryllis', 'Pine', 'Eucalyptus'), ('Амарилис', 'Бор', 'Евкалипт'), ('#C8102E', '#2F6B3F', '#8FB8A0')),
]
MONTH_NAMES = (['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'],
               ['Януари', 'Февруари', 'Март', 'Април', 'Май', 'Юни', 'Юли', 'Август', 'Септември', 'Октомври', 'Ноември', 'Декември'])


def hours_text(lang):
    wd, we = OPEN_WEEKDAY.replace('-', ' – '), OPEN_WEEKEND.replace('-', ' – ')
    return ('Mon – Fri %s · Sat – Sun %s' % (wd, we)) if lang == 'en' else ('Пон – Пет %s · Съб – Нед %s' % (wd, we))


L = {
 'en': dict(
  lang='en', root='../', script='latin', other_href='../index.html', other_lang='bg', other_label='БГ', other_aria='Превключи на български',
  privacy_href='privacy.html', home_href='index.html',
  title='Sunday Stems – fresh flowers delivered every week in Plovdiv',
  desc='A flower subscription in Plovdiv: choose a size and a rhythm, and fresh seasonal flowers arrive at your door every week, every two weeks or once a month.',
  skip='Skip to content', nav_label='Main navigation', menu_btn='Menu',
  nav=[('#week', 'This week'), ('#plan', 'Subscribe'), ('#season', 'Seasons'), ('#visit', 'Visit')],
  cta='Start my flowers',
  hero_tag='Flower subscription · Plovdiv', h1='Fresh flowers. <em>Every week.</em>',
  lead='Pick a size and a rhythm. A new seasonal bouquet arrives at your door, wrapped that morning. Pause or skip whenever you like.',
  cta1='Build my subscription', cta2='See this week\'s bouquet',
  perks=['Free delivery in Plovdiv', 'Pause or skip any time', 'Seasonal and fresh'], hero_alt='A vibrant mixed bouquet', sticker_k='This week',
  k_week='This week', week_h='What is blooming now.', next_h='Coming up', cut_by='Order by {d} {t} for delivery on {s}', cut_in='Order within {x} for delivery on {s}', cut_left_h='h', cut_left_m='min',
  k_plan='Subscribe', plan_h='Build your subscription.', plan_p='Five choices, one price per delivery. You see the monthly cost before you send the request.',
  o_size='Pick a size', o_rhythm='How often?', o_length='How long?', o_extras='Extras', o_when='When and where?', o_first='First delivery', o_window='Delivery window starts at', o_you='Your details',
  vase_l='Add a vase', vase_s='+ 12 € once', gift_l='This is a gift', gift_s='We add a card',
  f_to='Who is it for?', f_name='Your name', f_phone='Phone', f_addr='Delivery address', f_card='Card message (optional)', f_msg='Anything else? (optional)',
  fulfil_d='Deliver to me', fulfil_p='I will pick up', day_f='Fridays', day_s='Saturdays', checking='Pick a first delivery to see delivery windows.',
  slip_h='Your subscription', per_delivery='Per delivery', per_month='About per month', total_l='Total for {n} deliveries', total_open='Until you stop', f_send='Start my subscription', f_note='We use your details only to answer your request.', f_priv='Privacy notice',
  k_season='Seasons', season_h='What is in season, month by month.', season_p='Your bouquet follows the flower calendar, so it is always fresh and never flown halfway round the world.', now='Now',
  how_h='How it works', steps=[('Choose', 'Pick a size, a rhythm and a day. You see the price per delivery and per month.'), ('We arrange', 'The morning of your delivery we pick the best of the week and wrap it.'), ('It arrives', 'At your door, in Plovdiv, free of charge. Pause or skip any time.')],
  k_rev='Happy subscribers', rev_h='What subscribers say',
  reviews=[('Every Saturday is a small celebration now. The flowers last more than a week.', 'Classic, weekly'), ('I gave it to my mum for her birthday and she has not stopped talking about it.', 'Gift subscription'), ('It is the easiest way I know to make the flat feel alive.', 'Petite, every 2 weeks')],
  rev_by='Example subscriber', rev_note='Example reviews. Replace them with real reviews.',
  k_faq='Questions', faq_h='Good to know',
  faq=[('Can I pause or skip a delivery?', 'Yes. Tell us by phone or message at least two days before the delivery and we skip it.'), ('Which flowers will I get?', 'Whatever is best that week. The page shows this week\'s bouquet, and the calendar shows what is in season.'), ('Is delivery included?', 'Delivery in Plovdiv is free. We also deliver nearby for a small fee; ask us.'), ('How do I pay?', 'You pay on the first delivery, by cash or card. Then each delivery or each month, as you prefer.'), ('Can I give it as a gift?', 'Yes. Tick “This is a gift”, tell us who it is for and we add a card with your message.')],
  k_visit='Visit', visit_h='The shop', addr_l='Address', addr='Primer St. 1, Plovdiv', hours_l='Hours', phone_l='Phone', email_l='Email',
  map_t='The map is from OpenStreetMap and loads only if you choose.', map_btn='Show the map',
  foot_tag='Flower subscriptions in Plovdiv', foot_priv='Privacy notice', admin_t='Demo back office', admin_href='../admin.html?lang=en', quick_label='Quick contact', q_call='Call', q_plan='Subscribe',
  dock_label='Colour scheme',
 ),
 'bg': dict(
  lang='bg', root='', script='cyrillic', other_href='en/index.html', other_lang='en', other_label='EN', other_aria='Switch to English',
  privacy_href='privacy.html', home_href='index.html',
  title='Sunday Stems – свежи цветя всяка седмица в Пловдив',
  desc='Абонамент за цветя в Пловдив: избери размер и ритъм и свежи сезонни цветя пристигат до вратата ти всяка седмица, на две седмици или веднъж месечно.',
  skip='Към съдържанието', nav_label='Основна навигация', menu_btn='Меню',
  nav=[('#week', 'Тази седмица'), ('#plan', 'Абонамент'), ('#season', 'Сезони'), ('#visit', 'Адрес')],
  cta='Започни с цветя',
  hero_tag='Абонамент за цветя · Пловдив', h1='Свежи цветя. <em>Всяка седмица.</em>',
  lead='Избери размер и ритъм. Нов сезонен букет пристига до вратата ти, опакован същата сутрин. Спри го или пропусни, когато поискаш.',
  cta1='Подреди абонамента', cta2='Виж букета за седмицата',
  perks=['Безплатна доставка в Пловдив', 'Пауза или пропускане по всяко време', 'Сезонни и свежи'], hero_alt='Ярък смесен букет', sticker_k='Тази седмица',
  k_week='Тази седмица', week_h='Какво цъфти сега.', next_h='Предстои', cut_by='Поръчай до {d} {t} за доставка в {s}', cut_in='Поръчай до {x} за доставка в {s}', cut_left_h='ч', cut_left_m='мин',
  k_plan='Абонамент', plan_h='Подреди своя абонамент.', plan_p='Пет избора, една цена на доставка. Виждаш месечната сума, преди да изпратиш заявката.',
  o_size='Избери размер', o_rhythm='Колко често?', o_length='За колко време?', o_extras='Допълнения', o_when='Кога и къде?', o_first='Първа доставка', o_window='Доставката започва в', o_you='Твоите данни',
  vase_l='Добави ваза', vase_s='+ 12 € веднъж', gift_l='Това е подарък', gift_s='Добавяме картичка',
  f_to='За кого е?', f_name='Твоето име', f_phone='Телефон', f_addr='Адрес за доставка', f_card='Текст на картичката (по желание)', f_msg='Нещо друго? (по желание)',
  fulfil_d='Доставете ми', fulfil_p='Ще си го взимам', day_f='В петък', day_s='В събота', checking='Избери първа доставка, за да видиш часовете.',
  slip_h='Твоят абонамент', per_delivery='На доставка', per_month='Около на месец', total_l='Общо за {n} доставки', total_open='Докато спреш', f_send='Започни абонамента', f_note='Ползваме данните ти само за да отговорим на заявката ти.', f_priv='Политика за поверителност',
  k_season='Сезони', season_h='Какво е в сезон – месец по месец.', season_p='Букетът ти следва цветния календар, така че винаги е свеж и не е пътувал през половин свят.', now='Сега',
  how_h='Как работи', steps=[('Избираш', 'Избери размер, ритъм и ден. Виждаш цената на доставка и на месец.'), ('Подреждаме', 'Сутринта на доставката избираме най-доброто от седмицата и го опаковаме.'), ('Пристига', 'До вратата ти в Пловдив, безплатно. Пауза или пропускане по всяко време.')],
  k_rev='Доволни абонати', rev_h='Какво казват абонатите',
  reviews=[('Всяка събота вече е малък празник. Цветята издържат повече от седмица.', 'Класик, всяка седмица'), ('Подарих го на мама за рождения ден и тя още говори за него.', 'Подаръчен абонамент'), ('Най-лесният начин да оживя дома си.', 'Малък, на 2 седмици')],
  rev_by='Примерен абонат', rev_note='Примерни отзиви. Заменете ги с истински.',
  k_faq='Въпроси', faq_h='Добре е да знаеш',
  faq=[('Мога ли да спра или пропусна доставка?', 'Да. Кажи ни по телефона или в съобщение поне два дни преди доставката и я пропускаме.'), ('Какви цветя ще получавам?', 'Най-хубавото за седмицата. На страницата виждаш букета за тази седмица, а календарът показва какво е в сезон.'), ('Включена ли е доставката?', 'Доставката в Пловдив е безплатна. Доставяме и наблизо срещу малка такса; попитай ни.'), ('Как се плаща?', 'Плащаш при първата доставка, в брой или с карта. После при всяка доставка или всеки месец, както предпочиташ.'), ('Мога ли да го подаря?', 'Да. Отбележи „Това е подарък“, кажи ни за кого е и добавяме картичка с твоето послание.')],
  k_visit='Посети ни', visit_h='Магазинът', addr_l='Адрес', addr='ул. Примерна 1, Пловдив', hours_l='Работно време', phone_l='Телефон', email_l='Имейл',
  map_t='Картата е от OpenStreetMap и се зарежда само ако поискаш.', map_btn='Покажи картата',
  foot_tag='Абонаменти за цветя в Пловдив', foot_priv='Политика за поверителност', admin_t='Демо админ панел', admin_href='admin.html', quick_label='Бърза връзка', q_call='Обади се', q_plan='Абонамент',
  dock_label='Цветова схема',
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
    keys = ['title', 'desc', 'skip', 'nav_label', 'menu_btn', 'cta', 'hero_tag', 'lead', 'cta1', 'cta2', 'hero_alt', 'sticker_k', 'k_week', 'week_h', 'next_h',
            'k_plan', 'plan_h', 'plan_p', 'o_size', 'o_rhythm', 'o_length', 'o_extras', 'o_when', 'o_first', 'o_window', 'o_you', 'vase_l', 'vase_s', 'gift_l', 'gift_s',
            'f_to', 'f_name', 'f_phone', 'f_addr', 'f_card', 'f_msg', 'checking', 'slip_h', 'per_delivery', 'per_month', 'f_send', 'f_note', 'f_priv',
            'k_season', 'season_h', 'season_p', 'how_h', 'k_rev', 'rev_h', 'rev_note', 'k_faq', 'faq_h', 'k_visit', 'visit_h', 'addr_l', 'addr', 'hours_l', 'phone_l', 'email_l', 'map_t', 'map_btn',
            'foot_tag', 'foot_priv', 'admin_t', 'quick_label', 'q_call', 'q_plan', 'dock_label']
    for k in keys:
        out[k] = e(d[k])
    out['total_l'] = e(d['total_l'].replace('{n}', '12'))
    out['h1'] = d['h1']
    out['other_href'] = d['other_href']; out['other_lang'] = d['other_lang']; out['other_label'] = d['other_label']; out['other_aria'] = e(d['other_aria'])
    out['privacy_href'] = d['privacy_href']; out['home_href'] = d['home_href']; out['admin_href'] = d['admin_href']
    out['nav_links'] = '\n      '.join('<a href="%s">%s</a>' % (h, e(t)) for h, t in d['nav'])
    out['perks'] = '\n        '.join('<li>%s</li>' % e(p) for p in d['perks'])
    hw, hh = dims('vibrant-bouquet')
    out['hero_img'] = 'vibrant-bouquet.jpg'; out['hero_img_s'] = 'vibrant-bouquet-800.jpg'; out['hero_w'] = str(hw); out['hero_h'] = str(hh)

    # size cards
    sizes = []
    for sid, price, photo, nen, nbg, sen, sbg in SIZES:
        sizes.append('<label class="sz"><input type="radio" name="size" value="%s" data-price="%d" data-name="%s"%s><img src="%simages/stock/%s-800.jpg" alt="" width="400" height="400" loading="lazy" decoding="async">'
                     '<span class="sz-t"><b>%s</b><small>%s</small></span><span class="sz-p">%d €</span></label>'
                     % (sid, price, e(nbg if bg else nen), ' checked' if sid == 'classic' else '', root, photo, e(nbg if bg else nen), e(sbg if bg else sen), price))
    out['size_opts'] = ''.join(sizes)
    out['freq_opts'] = ''.join('<label class="pl"><input type="radio" name="freq" value="%s" data-days="%d" data-pm="%s" data-name="%s"%s><span>%s</span></label>'
                               % (fid, days, pm, e(nbg if bg else nen), ' checked' if fid == 'weekly' else '', e(nbg if bg else nen)) for fid, days, pm, nen, nbg in FREQS)
    save_txt = {'0': '', '10': ' · −10 %', '5': ' · −5 %'}
    out['len_opts'] = ''.join('<label class="pl"><input type="radio" name="len" value="%s" data-n="%d" data-off="%d" data-name="%s"%s><span>%s<small>%s</small></span></label>'
                              % (lid, n, off, e(nbg if bg else nen), ' checked' if lid == '12' else '', e(nbg if bg else nen), ('−%d %%' % off) if off else '&nbsp;')
                              for lid, n, off, nen, nbg in LENS)
    out['fulfil_opts'] = ('<label class="pl"><input type="radio" name="fulfil" value="delivery" checked><span>%s</span></label>'
                          '<label class="pl"><input type="radio" name="fulfil" value="pickup"><span>%s</span></label>') % (e(d['fulfil_d']), e(d['fulfil_p']))
    out['day_opts'] = ('<label class="pl"><input type="radio" name="day" value="5" checked><span>%s</span></label>'
                       '<label class="pl"><input type="radio" name="day" value="6"><span>%s</span></label>') % (e(d['day_f']), e(d['day_s']))

    out['months'] = '\n        '.join(
        '<li class="mo" data-m="%d"><b>%s</b><span class="now" hidden>%s</span><ul>%s</ul></li>'
        % (n, e(MONTH_NAMES[i][n]), e(d['now']), ''.join('<li><i style="--c:%s"></i>%s</li>' % (col, e(fl)) for fl, col in zip(MONTHS[n][i], MONTHS[n][2])))
        for n in range(12))
    out['steps'] = '\n        '.join('<li><h3>%s</h3><p>%s</p></li>' % (e(t), e(p)) for t, p in d['steps'])
    out['reviews'] = '\n        '.join('<figure class="rev"><blockquote>%s</blockquote><figcaption><b>%s</b> · %s</figcaption></figure>' % (e(q), e(s), e(d['rev_by'])) for q, s in d['reviews'])
    out['faq'] = '\n          '.join('<details><summary>%s</summary><p>%s</p></details>' % (e(q), e(a)) for q, a in d['faq'])

    data = {
        'weekly': [{'name': n[1] if bg else n[0], 'stems': n[3] if bg else n[2], 'src': '%simages/stock/%s-800.jpg' % (root, n[4])} for n in WEEKLY],
        'cutBy': d['cut_by'], 'cutIn': d['cut_in'], 'hUnit': d['cut_left_h'], 'mUnit': d['cut_left_m'], 'totalL': d['total_l'], 'totalOpen': d['total_open'],
        'vase': VASE_PRICE,
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
    'window.SUNDAY_CONFIG = {\n'
    '  mode: "%s",            /* "demo" = requests are kept in this browser only; "live" = real API at apiBase (docs/API.md) */\n'
    '  apiBase: "%s",\n'
    '  hours: { weekday: ["%s", "%s"], weekend: ["%s", "%s"] },\n'
    '  capacity: %d,             /* deliveries that can start in the same window */\n'
    '  slotMinutes: %d,\n'
    '  leadMinutes: %d,\n'
    '  latency: [600, 1100]      /* demo only: pretend network delay in milliseconds */\n'
    '};\n'
) % (MODE, API_BASE, OPEN_WEEKDAY.split('-')[0], OPEN_WEEKDAY.split('-')[1], OPEN_WEEKEND.split('-')[0], OPEN_WEEKEND.split('-')[1], CAPACITY, SLOT_MINUTES, LEAD_MINUTES)
os.makedirs(os.path.join(SHOP, 'js'), exist_ok=True)
open(os.path.join(SHOP, 'js', 'config.js'), 'w', encoding='utf-8').write(cfg)
print('config.js written')
