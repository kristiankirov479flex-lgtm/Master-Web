import os, re
from html import escape

SHOP = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ---- Edit these placeholders for each guest house --------------------------------------------
BRAND_EN = 'Blue Heron'
BRAND_BG = 'Синя чапла'
PHONE_DISPLAY = '+359 000 000 000'
PHONE_HREF = '+359000000000'
EMAIL = 'email@example.com'
CHECKIN = '15:00'
CHECKOUT = '11:00'
LAT, LON = 42.13, 24.74          # used only to calculate today's sunrise and sunset in the browser (placeholder: use the real place)
# Enquiry system. 'demo' = the booking form talks to a mock server that keeps enquiries in the visitor's browser.
# 'live' = it sends real HTTP requests to API_BASE (see docs/API.md). Written to js/config.js.
MODE = 'demo'
API_BASE = '/api'
MAX_NIGHTS = 30
# ---------------------------------------------------------------------------------------------

# Places to sleep (all names, sizes and prices are examples): id, name EN, name BG, m2, guests, bed EN, bed BG, price per night (EUR), photo, width, height
UNITS = [
    ('heron',  'The Heron Room',        'Стая „Чапла“',               26, 2, '1 double bed', '1 двойно легло', 72, 'bedroom-bright-wood', 1600, 1067),
    ('loft',   'The Glass Loft',        'Стъкленото таванско',         34, 2, '1 king bed', '1 голямо легло', 95, 'bedroom-misty', 1600, 900),
    ('family', 'The Family Suite',      'Семейният сюит',              48, 4, '1 double bed and 2 single beds', '1 двойно легло и 2 единични', 140, 'bedroom-seating', 1600, 1067),
    ('boat',   'The Boathouse Studio',  'Студиото в лодкарницата',    22, 2, '1 double bed', '1 двойно легло', 62, 'bedroom-window', 1600, 1067),
]
UNIT_TEXT = {  # id: (description EN, description BG, [amenities EN], [amenities BG])
    'heron': ('A bright room with warm wood panelling, a sofa and tall windows onto the garden.', 'Светла стая с топла дървена ламперия, диван и високи прозорци към градината.',
              ['Garden view', 'Sofa', 'Wi-Fi', 'Ceiling fan'], ['Гледка към градината', 'Диван', 'Wi-Fi', 'Вентилатор']),
    'loft': ('Our most dramatic room: a high ceiling and a wall of glass that frames the water.', 'Най-впечатляващата ни стая: висок таван и стена от стъкло, която обрамчва водата.',
             ['Lake view', 'Glass wall', 'Wi-Fi', 'Bathtub'], ['Гледка към езерото', 'Стъклена стена', 'Wi-Fi', 'Вана']),
    'family': ('A large suite with a sitting area and room for four. Quiet, with soft light all day.', 'Голям сюит с кът за сядане и място за четирима. Тих, с мека светлина през целия ден.',
               ['Sleeps four', 'Sitting area', 'Wi-Fi', 'Extra bed on request'], ['За четирима', 'Кът за сядане', 'Wi-Fi', 'Допълнително легло по заявка']),
    'boat': ('A small white studio above the boathouse. Simple, calm and a few steps from the dock.', 'Малко бяло студио над лодкарницата. Семпло, спокойно и на няколко крачки от пристана.',
             ['Next to the dock', 'Shower room', 'Wi-Fi', 'Kettle'], ['До пристана', 'Баня с душ', 'Wi-Fi', 'Чайник']),
}
# The grounds (map hotspots): id, x, y (in map units 800 x 520), title EN, title BG, text EN, text BG, photo, width, height
GROUNDS = [
    ('house', 315, 172, 'The main house', 'Главната къща', 'Three of the four places to sleep, the long breakfast table and a bright living room with a view of the water.',
     'Три от четирите места за нощувка, дългата маса за закуска и светла дневна с гледка към водата.', 'house-lake-white', 1600, 1067),
    ('terrace', 400, 236, 'The terrace', 'Терасата', 'Breakfast and dinner outside with the lake in front of you. Shaded when the sun is high.',
     'Закуска и вечеря навън, с езерото пред вас. На сянка, когато слънцето е високо.', 'deck-dining', 1600, 1067),
    ('garden', 130, 160, 'Garden and hammocks', 'Градина и хамаци', 'Lawn, fruit trees and four hammocks. Nobody minds if you read here all afternoon.',
     'Морава, плодни дървета и четири хамака. Никой не възразява, ако четете тук цял следобед.', 'hammock-mountains', 1600, 1067),
    ('sauna', 505, 212, 'The sauna', 'Сауната', 'A wood-heated sauna with a window to the water. Ask at the house for an evening slot.',
     'Сауна на дърва с прозорец към водата. Попитайте в къщата за вечерен час.', 'sauna-bench', 1600, 1200),
    ('boathouse', 179, 282, 'Boathouse and kayaks', 'Лодкарница и каяци', 'Two kayaks and a rowing boat. The Boathouse Studio is the room above them.',
     'Два каяка и гребна лодка. Студиото в лодкарницата е стаята отгоре.', 'yellow-kayak', 1600, 2398),
    ('dock', 406, 430, 'The dock', 'Пристанът', 'A wooden dock for a swim at sunrise and a long look at the sunset.',
     'Дървен пристан за плуване на изгрев и дълъг поглед към залеза.', 'dock-day', 1600, 1067),
]
PERSONAS = [  # id, label EN, label BG, photo, w, h, [(day EN, text EN, text BG) ...]
    ('quiet', 'Quiet', 'Спокойно', 'egg-chair', 1600, 2400, [
        ('Arrive, swim off the dock and have the sauna in the evening.', 'Пристигнете, поплувайте от пристана и вечерта влезте в сауната.'),
        ('A slow breakfast, a book in the hammock and the sunset from the dock.', 'Бавна закуска, книга в хамака и залез от пристана.'),
        ('One more swim, coffee on the terrace and a late check-out.', 'Още едно плуване, кафе на терасата и късно освобождаване.')]),
    ('active', 'Active', 'Активно', 'kayak-mist', 1600, 1067, [
        ('Kayak across the lake before breakfast, when the water is still.', 'С каяк през езерото преди закуска, когато водата е спокойна.'),
        ('Walk the shore trail to the viewpoint and back, about three hours.', 'Разходка по бреговата пътека до гледката и обратно, около три часа.'),
        ('Rowing boat to the far bank, a picnic and a last swim.', 'С гребна лодка до отсрещния бряг, пикник и последно плуване.')]),
    ('family', 'With kids', 'С деца', 'lake-and-dock', 1600, 1067, [
        ('Arrive, find the hammocks and have ice cream by the water.', 'Пристигнете, намерете хамаците и хапнете сладолед до водата.'),
        ('Kayaks for the kids, with an adult, and a picnic on the lawn.', 'Каяци за децата, с възрастен, и пикник на моравата.'),
        ('A treasure hunt in the garden and a last swim at the dock.', 'Търсене на съкровище в градината и последно плуване на пристана.')]),
]
BUBBLES = [  # quote EN, quote BG, name EN, name BG, stay EN, stay BG
    ('We swam off the dock before anyone was awake. Best breakfast we had all summer.', 'Плувахме от пристана, преди някой да се е събудил. Най-хубавата закуска това лято.', 'Mira and Dan', 'Мира и Дан', 'Stayed in July', 'отседнали през юли'),
    ('The glass loft at night, with the lake going dark. We did not want to leave.', 'Вечерта в стъкленото таванско, докато езерото притъмнява. Не ни се тръгваше.', 'Iva', 'Ива', 'Stayed in September', 'отседнала през септември'),
    ('The kids lived on the dock and in the kayaks. We will be back next summer.', 'Децата живееха на пристана и в каяците. Ще се върнем и следващото лято.', 'The Kolevs', 'Семейство Колеви', 'Stayed in August', 'отседнали през август'),
    ('Quiet, clean and very kind hosts. The sauna after a cold morning swim is a gift.', 'Тихо, чисто и много мили домакини. Сауната след студено сутрешно плуване е подарък.', 'Stefan', 'Стефан', 'Stayed in May', 'отседнал през май'),
]
ROUTES = [  # id, title EN, title BG, text EN, text BG
    ('car', 'By car', 'С кола', 'Free parking at the house. The last 800 metres are a gravel road along the shore.', 'Безплатен паркинг при къщата. Последните 800 метра са чакълен път покрай брега.'),
    ('bus', 'By bus', 'С автобус', 'The nearest stop is 15 minutes on foot. Call us and we can pick you up.', 'Най-близката спирка е на 15 минути пеша. Обадете ни се и можем да ви вземем.'),
    ('bike', 'By bike', 'С колело', 'A flat path along the lake leads to the house. There is a place to lock bikes.', 'Равна пътека покрай езерото води до къщата. Има място за заключване на колела.'),
]

L = {
 'en': dict(
  lang='en', root='../', script='latin', other_href='../index.html', other_lang='bg', other_label='БГ', other_aria='Превключи на български',
  privacy_href='privacy.html', home_href='index.html', brand=BRAND_EN,
  title='Blue Heron – a guest house on the lake shore',
  desc='Four places to sleep by a quiet lake: a dock for swimming, kayaks, a wood sauna and hammocks. Explore the grounds, pick your dates on the timeline and send an enquiry.',
  skip='Skip to content', tagline='lake house', nav_label='Site menu',
  nav=[('#top', 'Home'), ('#grounds', 'Grounds'), ('#rooms', 'Rooms'), ('#book', 'Book'), ('#plan', 'Plan'), ('#visit', 'Visit')],
  kicker='A guest house on the lake', h1='Wake up with the <em>lake</em>.',
  lead='Four places to sleep, a dock for the first swim, kayaks by the shore and a sauna with a window to the water.',
  cta1='Find a free week', cta2='Explore the grounds', top_alt='A white house with a red roof on the shore of a calm lake, surrounded by green trees',
  badge_t='Good to know', badge_l='Check-in from ' + CHECKIN + ' · check-out until ' + CHECKOUT,
  sun_rise='Sunrise', sun_set='Sunset', sun_gold='golden hour from', sun_today='Today at the lake',
  k_grounds='The grounds', grounds_h='Walk around before you arrive', grounds_p='Press a number on the map to see what is there.', map_alt='An illustrated map of the grounds: the house, the terrace, the garden, the sauna, the boathouse and the dock by the lake',
  k_rooms='Rooms', rooms_h='Four places to sleep', rooms_p='Each has its own bathroom. Prices are per night for the whole room.',
  guests_up='Up to {n} guests', from_price='from', per_night='per night', pick_on_board='Pick dates for this room',
  k_book='Book', book_h='Find your free days', book_p='Each row is a place to sleep, each column a night. Press the day you arrive, then the day you leave. Striped nights are taken.',
  f_guests='Guests', guest_word='guest', guests_word='guests', board_prev='Earlier days', board_next='Later days', board_pick='Press your arrival night', board_label='Availability by place and night',
  lg_free='Free', lg_taken='Taken', lg_sel='Your stay', board_hint='Scroll sideways to see more days. Places that are too small for your group are dimmed.',
  sum_h='Your stay', sum_note='Estimated total at the example prices. We confirm the final price when we reply.',
  f_name='Your name', f_phone='Phone', f_email='Email (optional)', f_msg='Message (optional)', f_send='Send enquiry',
  f_note='We use your details only to answer your enquiry.', f_priv='Privacy notice',
  k_plan='Plan', plan_h='Plan your days', plan_p='Pick the kind of stay you want and see how three days could go.', day_word='Day',
  k_talk='Guests', talk_h='What guests tell us', talk_p='A few lines from the visitors book.', rev_note='Example messages. Replace them with real guest reviews.',
  k_visit='Visit', visit_h='Getting here', addr_l='Address', addr='Primer St. 1, on the lake shore', times_l='Check-in and check-out', times='Check-in from ' + CHECKIN + ', check-out until ' + CHECKOUT,
  phone_l='Phone', email_l='Email', map_t='The map is from OpenStreetMap and loads only if you choose.', map_btn='Show the map',
  faq_h='Good to know',
  faq=[('What time is check-in and check-out?', 'Check-in is from ' + CHECKIN + ' and check-out until ' + CHECKOUT + '. If you arrive early, swim first: we will keep your bags.'),
       ('Is the lake safe for swimming?', 'The water is calm and shallow near the dock. Children must be with an adult. There is no lifeguard.'),
       ('Is breakfast included?', 'Breakfast is served on the terrace and costs 9 € per person. Tell us about allergies when you book.'),
       ('Do you accept children and pets?', 'Children are very welcome. Dogs can stay in the Boathouse Studio on request.'),
       ('How do I pay, and what if my plans change?', 'You pay on arrival, by cash or card. Tell us at least five days ahead if you need to change or cancel, and there is no charge.'),
       ('Can I use the kayaks and the sauna?', 'Yes, both are free for guests. Ask at the house for an evening sauna slot.')],
  foot_priv='Privacy notice', admin_t='Demo back office', admin_href='../admin.html?lang=en',
 ),
 'bg': dict(
  lang='bg', root='', script='cyrillic', other_href='en/index.html', other_lang='en', other_label='EN', other_aria='Switch to English',
  privacy_href='privacy.html', home_href='index.html', brand=BRAND_BG,
  title='Синя чапла – къща за гости на брега на езеро',
  desc='Четири места за нощувка край тихо езеро: пристан за плуване, каяци, сауна на дърва и хамаци. Разгледайте двора, изберете дати върху лентата и изпратете запитване.',
  skip='Към съдържанието', tagline='къща до езерото', nav_label='Меню на сайта',
  nav=[('#top', 'Начало'), ('#grounds', 'Двор'), ('#rooms', 'Стаи'), ('#book', 'Заявка'), ('#plan', 'План'), ('#visit', 'Адрес')],
  kicker='Къща за гости на езерото', h1='Събудете се с <em>езерото</em>.',
  lead='Четири места за нощувка, пристан за първото плуване, каяци на брега и сауна с прозорец към водата.',
  cta1='Намерете свободна седмица', cta2='Разгледайте двора', top_alt='Бяла къща с червен покрив на брега на спокойно езеро, сред зелени дървета',
  badge_t='Добре е да знаете', badge_l='Настаняване от ' + CHECKIN + ' · освобождаване до ' + CHECKOUT,
  sun_rise='Изгрев', sun_set='Залез', sun_gold='златен час от', sun_today='Днес при езерото',
  k_grounds='Дворът', grounds_h='Разходете се, преди да пристигнете', grounds_p='Натиснете число върху картата, за да видите какво има там.', map_alt='Илюстрирана карта на двора: къщата, терасата, градината, сауната, лодкарницата и пристанът до езерото',
  k_rooms='Стаи', rooms_h='Четири места за нощувка', rooms_p='Всяко има собствена баня. Цените са на нощ за цялата стая.',
  guests_up='До {n} гости', from_price='от', per_night='на нощ', pick_on_board='Изберете дати за тази стая',
  k_book='Резервация', book_h='Намерете свободните си дни', book_p='Всеки ред е място за нощувка, всяка колона – нощ. Натиснете деня на пристигане, после деня на заминаване. Раираните нощи са заети.',
  f_guests='Гости', guest_word='гост', guests_word='гости', board_prev='По-ранни дни', board_next='По-късни дни', board_pick='Натиснете нощта на пристигане', board_label='Свободни места по стая и нощ',
  lg_free='Свободно', lg_taken='Заето', lg_sel='Вашият престой', board_hint='Плъзнете настрани, за да видите още дни. Местата, които са твърде малки за групата ви, са приглушени.',
  sum_h='Вашият престой', sum_note='Ориентировъчна обща сума по примерните цени. Крайната цена потвърждаваме, когато ви отговорим.',
  f_name='Вашето име', f_phone='Телефон', f_email='Имейл (по желание)', f_msg='Съобщение (по желание)', f_send='Изпрати запитване',
  f_note='Ползваме данните ви само за да отговорим на запитването.', f_priv='Политика за поверителност',
  k_plan='План', plan_h='Планирайте дните си', plan_p='Изберете вида почивка и вижте как биха минали три дни.', day_word='Ден',
  k_talk='Отзиви', talk_h='Какво ни казват гостите', talk_p='Няколко реда от книгата за гости.', rev_note='Примерни съобщения. Заменете ги с истински отзиви от гости.',
  k_visit='Посетете ни', visit_h='Как да стигнете', addr_l='Адрес', addr='ул. Примерна 1, на брега на езерото', times_l='Настаняване и освобождаване', times='Настаняване от ' + CHECKIN + ', освобождаване до ' + CHECKOUT,
  phone_l='Телефон', email_l='Имейл', map_t='Картата е от OpenStreetMap и се зарежда само ако поискате.', map_btn='Покажи картата',
  faq_h='Добре е да знаете',
  faq=[('Кога е настаняването и освобождаването?', 'Настаняване от ' + CHECKIN + ' и освобождаване до ' + CHECKOUT + '. Ако пристигнете по-рано, първо поплувайте: ще пазим багажа ви.'),
       ('Безопасно ли е плуването в езерото?', 'Водата е спокойна и плитка близо до пристана. Децата трябва да са с възрастен. Няма спасител.'),
       ('Включена ли е закуската?', 'Закуската е на терасата и струва 9 € на човек. Кажете ни за алергии при резервацията.'),
       ('Приемате ли деца и домашни любимци?', 'Децата са много добре дошли. Кучета могат да отседнат в Студиото в лодкарницата по заявка.'),
       ('Как се плаща и какво ако плановете ми се променят?', 'Плаща се на място, в брой или с карта. Кажете ни поне пет дни по-рано, ако трябва да промените или отмените, и няма такса.'),
       ('Мога ли да ползвам каяците и сауната?', 'Да, и двете са безплатни за гости. Попитайте в къщата за вечерен час в сауната.')],
  foot_priv='Политика за поверителност', admin_t='Демо админ панел', admin_href='admin.html',
 ),
}

TEMPLATE = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'page_template.html'), encoding='utf-8').read()


def build(lang):
    d = L[lang]
    e = lambda s: escape(s, quote=True)
    root = d['root']
    bg = lang == 'bg'
    out = {'lang': lang, 'root': root, 'script': d['script']}
    keys = ['title', 'desc', 'skip', 'tagline', 'nav_label', 'kicker', 'lead', 'cta1', 'cta2', 'top_alt', 'badge_t', 'badge_l',
            'k_grounds', 'grounds_h', 'grounds_p', 'map_alt', 'k_rooms', 'rooms_h', 'rooms_p', 'k_book', 'book_h', 'book_p', 'f_guests', 'board_prev', 'board_next', 'board_pick', 'board_label',
            'lg_free', 'lg_taken', 'lg_sel', 'board_hint', 'sum_h', 'sum_note', 'f_name', 'f_phone', 'f_email', 'f_msg', 'f_send', 'f_note', 'f_priv', 'k_plan', 'plan_h', 'plan_p',
            'k_talk', 'talk_h', 'talk_p', 'rev_note', 'k_visit', 'visit_h', 'addr_l', 'addr', 'times_l', 'times', 'phone_l', 'email_l', 'map_t', 'map_btn', 'faq_h', 'foot_priv', 'admin_t', 'brand']
    for k in keys:
        out[k] = e(d[k])
    out['h1'] = d['h1']   # contains <em>
    out['other_href'] = d['other_href']; out['other_lang'] = d['other_lang']; out['other_label'] = d['other_label']; out['other_aria'] = e(d['other_aria'])
    out['privacy_href'] = d['privacy_href']; out['home_href'] = d['home_href']; out['admin_href'] = d['admin_href']
    out['nav_links'] = '\n    '.join('<li><a href="%s">%s</a></li>' % (h, e(t)) for h, t in d['nav'])
    out['guest_options'] = ''.join('<option value="%d"%s>%d %s</option>' % (n, ' selected' if n == 2 else '', n, d['guest_word'] if n == 1 else d['guests_word']) for n in range(1, 9))

    first = GROUNDS[0]
    out['first_h'] = e(first[4] if bg else first[3]); out['first_p'] = e(first[6] if bg else first[5])
    hs, pl = [], []
    for n, (gid, x, y, ten, tbg, xen, xbg, photo, w, h) in enumerate(GROUNDS):
        title, text = (tbg, xbg) if bg else (ten, xen)
        hs.append('<button class="hot%s" type="button" style="left:%.2f%%;top:%.2f%%" data-i="%d" aria-pressed="%s" aria-label="%s"><span>%d</span></button>'
                  % (' on' if n == 0 else '', x / 8, y / 5.2, n, 'true' if n == 0 else 'false', e(title), n + 1))
        pl.append('<li><button class="place%s" type="button" data-i="%d" data-photo="%simages/stock/%s-800.jpg" data-h="%d" data-title="%s" data-text="%s" aria-pressed="%s"><i>%d</i>%s</button></li>'
                  % (' on' if n == 0 else '', n, root, photo, round(800 * h / w), e(title), e(text), 'true' if n == 0 else 'false', n + 1, e(title)))
    out['hotspots'] = '\n          '.join(hs)
    out['place_list'] = '\n        '.join(pl)

    rooms = []
    for uid, en, bgn, m2, cap, bed_en, bed_bg, price, photo, w, h in UNITS:
        name = bgn if bg else en
        de, db, ae, ab = UNIT_TEXT[uid]
        rooms.append(
            '<article class="room"><figure><img src="%simages/stock/%s-800.jpg" width="800" height="%d" alt="" loading="lazy" decoding="async"></figure>'
            '<div class="room-body"><h3>%s</h3><ul class="meta"><li>%d m²</li><li>%s</li><li>%s</li></ul><p>%s</p><ul class="am">%s</ul>'
            '<p class="room-price">%s <b>%d €</b> %s</p><button class="btn btn-coral btn-sm" type="button" data-unit="%s">%s</button></div></article>'
            % (root, photo, round(800 * h / w), e(name), m2, e(d['guests_up'].replace('{n}', str(cap))), e(bed_bg if bg else bed_en), e(db if bg else de),
               ''.join('<li>%s</li>' % e(x) for x in (ab if bg else ae)), e(d['from_price']), price, e(d['per_night']), uid, e(d['pick_on_board'])))
    out['rooms'] = '\n        '.join(rooms)

    tabs, panels = [], []
    for n, (pid, len_, lbg, photo, w, h, days) in enumerate(PERSONAS):
        tabs.append('<button class="ptab" type="button" role="tab" id="pt-%s" aria-controls="pp-%s" aria-selected="%s" tabindex="%s">%s</button>' % (pid, pid, 'true' if n == 0 else 'false', '0' if n == 0 else '-1', e(lbg if bg else len_)))
        panels.append('<div class="ppanel" id="pp-%s" role="tabpanel" aria-labelledby="pt-%s"%s><img src="%simages/stock/%s-800.jpg" width="800" height="%d" alt="" loading="lazy" decoding="async"><ol>%s</ol></div>'
                      % (pid, pid, '' if n == 0 else ' hidden', root, photo, round(800 * h / w),
                         ''.join('<li><b>%s %d</b><span>%s</span></li>' % (e(d['day_word']), i + 1, e(t_bg if bg else t_en)) for i, (t_en, t_bg) in enumerate(days))))
    out['ptabs'] = '\n        '.join(tabs)
    out['ppanels'] = '\n      '.join(panels)

    out['bubbles'] = '\n        '.join(
        '<li class="bub %s"><span class="av" aria-hidden="true">%s</span><div><p>%s</p><b>%s</b> <span>· %s</span></div></li>'
        % ('r' if n % 2 else 'l', e((r[3] if bg else r[2])[0]), e(r[1] if bg else r[0]), e(r[3] if bg else r[2]), e(r[5] if bg else r[4])) for n, r in enumerate(BUBBLES))
    out['routes'] = '\n          '.join('<li><b>%s</b><span>%s</span></li>' % (e(tbg if bg else ten), e(xbg if bg else xen)) for _id, ten, tbg, xen, xbg in ROUTES)
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
rooms_js = ', '.join('{ id: "%s", guests: %d, price: %d }' % (r[0], r[4], r[7]) for r in UNITS)
cfg = (
    '/* Generated by tools/build_pages.py. Edit the values at the top of that file, then run it again. */\n'
    'window.LAKE_CONFIG = {\n'
    '  mode: "%s",            /* "demo" = enquiries are kept in this browser only; "live" = real API at apiBase (docs/API.md) */\n'
    '  apiBase: "%s",\n'
    '  rooms: [%s],\n'
    '  maxNights: %d,\n'
    '  place: { lat: %s, lon: %s },   /* used only for today\'s sunrise and sunset */\n'
    '  latency: [600, 1100]      /* demo only: pretend network delay in milliseconds */\n'
    '};\n'
) % (MODE, API_BASE, rooms_js, MAX_NIGHTS, LAT, LON)
os.makedirs(os.path.join(SHOP, 'js'), exist_ok=True)
open(os.path.join(SHOP, 'js', 'config.js'), 'w', encoding='utf-8').write(cfg)
print('config.js written')
