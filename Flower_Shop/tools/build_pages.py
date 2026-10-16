import os, re, json
from html import escape

SHOP = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ---- Edit these placeholders for each flower shop --------------------------------------------
OPEN_WEEKDAY = '09:00-19:00'      # opening and closing time, Mon - Fri
OPEN_WEEKEND = '09:00-16:00'      # opening and closing time, Sat - Sun
PHONE_DISPLAY = '+359 000 000 000'
PHONE_HREF = '+359000000000'
EMAIL = 'email@example.com'
# Order system. 'demo' = the form talks to a mock server that stores orders in the visitor's browser.
# 'live' = it sends real HTTP requests to API_BASE (see docs/API.md). Written to js/config.js.
MODE = 'demo'
API_BASE = '/api'
CAPACITY = 3                      # orders that can be prepared at the same time (number of florists)
SLOT_MINUTES = 30                 # gap between pick-up / delivery times
LEAD_MINUTES = 120                # a same-day order must be placed at least this long before the time chosen
CUTOFF = '15:00'                  # same-day delivery orders close at this time
BRAND = 'Mimosa'
# ---------------------------------------------------------------------------------------------

SKINS = [  # key, colours for the swatch (background, accent), names
    ('sage',       '#F5F3EC', '#4A6B54', 'Sage & Linen',          'Шалфей и лен'),
    ('rose',       '#FBF5F2', '#A23A5B', 'Rosewater & Cream',     'Розова вода и сметана'),
    ('terracotta', '#F6F0E7', '#97402A', 'Terracotta & Linen',    'Теракота и лен'),
    ('lavender',   '#F5F3F9', '#6A4C9C', 'Lavender & Mist',       'Лавандула и мъгла'),
    ('botanical',  '#14201A', '#EDA9B6', 'Evening Botanical',     'Вечерна ботаника'),
]

# file, cat, width, height, alt_en, alt_bg   (photos: images/stock, see images/CREDITS.md)
GALLERY = [
    ('beige-bouquet',        'bouquets', 1600, 2133, 'A hand holding a bouquet of white roses wrapped in beige paper', 'Ръка държи букет от бели рози, увит в бежова хартия'),
    ('mixed-glass-vase',     'vases',    1600, 2400, 'A peach and orange bouquet in a glass vase', 'Прасковен и оранжев букет в стъклена ваза'),
    ('shop-entrance-flowers','shop',     1600, 2400, 'A flower shop front with ribbons and flowers outside', 'Витрина на цветарница с панделки и цветя отпред'),
    ('hand-colorful-bouquet','bouquets', 1600, 1601, 'A hand holding a colourful bouquet with ranunculus and roses', 'Ръка държи цветен букет с ранункулуси и рози'),
    ('pink-grey-vase',       'vases',    1600, 2400, 'Pink peonies in a stone vase', 'Розови божури в каменна ваза'),
    ('holding-bouquet',      'bouquets', 1600, 2400, 'A hand holding a small bouquet in kraft paper with a sunflower', 'Ръка държи малък букет в амбалажна хартия със слънчоглед'),
    ('tulips',               'shop',     1600, 1067, 'Bunches of pink, yellow and purple tulips ready to sell', 'Китки розови, жълти и лилави лалета, готови за продажба'),
    ('pink-white-roses',     'bouquets', 1600, 2133, 'A bouquet of pink roses and small flowers in white paper', 'Букет от розови рози и дребни цветя в бяла хартия'),
    ('poppies-amber-vase',   'vases',    1600, 2400, 'White poppies in an amber glass vase', 'Бели макове в кехлибарена стъклена ваза'),
    ('roses-hydrangeas',     'bouquets', 1600, 2133, 'A bouquet of orange and pink roses with hydrangeas', 'Букет от оранжеви и розови рози с хортензии'),
    ('arranging-in-shop',    'shop',     1600, 2400, 'A florist arranging flowers at the shop counter', 'Флорист аранжира цветя на щанда в магазина'),
    ('red-arrangement',      'vases',    1600, 2400, 'A red and orange bouquet in a glass jar', 'Червен и оранжев букет в стъклен буркан'),
    ('vibrant-bouquet',      'bouquets', 1600, 1093, 'A pastel spring bouquet with snapdragons and daisies', 'Пастелен пролетен букет с лъвски зев и маргаритки'),
    ('white-purple-black-vase','vases',  1600, 2400, 'Wild garden flowers in a black vase', 'Диви градински цветя в черна ваза'),
    ('rose-bouquet',         'bouquets', 1600, 1600, 'A large bouquet of roses, berries and eucalyptus', 'Голям букет от рози, горски плодове и евкалипт'),
    ('shop-facade',          'shop',     1600, 2098, 'The front of a flower shop with plants and crates outside', 'Фасада на цветарница с растения и щайги отпред'),
    ('pink-glass-vase',      'vases',    1600, 2400, 'Pink tulips in a glass vase', 'Розови лалета в стъклена ваза'),
    ('red-white-bouquet',    'bouquets', 1600, 2400, 'A florist holding a mixed bouquet of roses and wildflowers', 'Флорист държи смесен букет от рози и полски цветя'),
    ('dried-peach-paper',    'bouquets', 1600, 2400, 'A small dried flower bouquet in peach paper', 'Малък букет от сухи цветя в прасковена хартия'),
    ('arranging-vase',       'vases',    1600, 1067, 'A florist arranging hydrangeas and peonies in a vase', 'Флорист аранжира хортензии и божури във ваза'),
    ('pink-roses',           'bouquets', 1600, 2844, 'Close-up of pink garden roses', 'Close-up на розови градински рози'),
    ('shop-entrance-blooms', 'shop',     1600, 2631, 'A flower shop entrance in the evening, full of blooms', 'Вход на цветарница вечер, пълен с цветя'),
]

# group title, [(name, time text, price text, (min minutes, max minutes))], selectable in the form (default yes)
# Minutes = preparation time; they drive the time list in the form.
MENU_EN = [
    ('Bouquets', [
        ('Roses, 5 stems', '20 min', '20 €', (20, 20)),
        ('Roses, 7 stems', '20 min', '26 €', (20, 20)),
        ('Roses, 11 stems', '25 min', '38 €', (25, 25)),
        ('Roses, 21 stems', '30 min', '70 €', (30, 30)),
        ('Seasonal mixed bouquet', '30 – 40 min', '30 – 55 €', (30, 40)),
        ('Tulip bouquet, 15 stems', '20 min', '28 €', (20, 20)),
        ('Dried flower bouquet', '30 min', '35 €', (30, 30))]),
    ('Arrangements', [
        ('Flower basket', '40 – 60 min', 'from 45 €', (40, 60)),
        ('Flower box', '30 min', '40 €', (30, 30)),
        ('Orchid in a pot', '10 min', '30 €', (10, 10)),
        ('Wedding and event flowers', 'consultation', 'on request', (30, 60))]),
    ('Extras', [
        ('Vase', '', 'from 8 €', (5, 5)),
        ('Chocolates or a small gift', '', 'from 6 €', (5, 5)),
        ('Gift wrapping', '', '3 €', (5, 5))], False),
    ('Delivery in Plovdiv', [
        ('Pick up in the shop', '', 'free', (0, 0)),
        ('Delivery on a chosen day', '', '7 €', (0, 0)),
        ('Express delivery within 2 hours', '', '12 €', (0, 0))], False),
]
MENU_BG = [
    ('Букети', [
        ('Рози, 5 стръка', '20 мин', '20 €', (20, 20)),
        ('Рози, 7 стръка', '20 мин', '26 €', (20, 20)),
        ('Рози, 11 стръка', '25 мин', '38 €', (25, 25)),
        ('Рози, 21 стръка', '30 мин', '70 €', (30, 30)),
        ('Сезонен микс букет', '30 – 40 мин', '30 – 55 €', (30, 40)),
        ('Букет от лалета, 15 стръка', '20 мин', '28 €', (20, 20)),
        ('Букет от сухи цветя', '30 мин', '35 €', (30, 30))]),
    ('Аранжировки', [
        ('Кошница с цветя', '40 – 60 мин', 'от 45 €', (40, 60)),
        ('Кутия с цветя', '30 мин', '40 €', (30, 30)),
        ('Орхидея в саксия', '10 мин', '30 €', (10, 10)),
        ('Цветя за сватби и събития', 'консултация', 'по запитване', (30, 60))]),
    ('Допълнения', [
        ('Ваза', '', 'от 8 €', (5, 5)),
        ('Шоколад или малък подарък', '', 'от 6 €', (5, 5)),
        ('Подаръчна опаковка', '', '3 €', (5, 5))], False),
    ('Доставка в Пловдив', [
        ('Вземане от магазина', '', 'безплатно', (0, 0)),
        ('Доставка в избран ден', '', '7 €', (0, 0)),
        ('Експресна доставка до 2 часа', '', '12 €', (0, 0))], False),
]

# ---- "Build your order" estimator (numbers are sample values based on Plovdiv florists) --------------
# opt = the menu item the form selects (must match a selectable menu name above). Minutes = preparation time.
PLAN_GROUPS = [('bouquets', 'Bouquets', 'Букети'), ('arrangements', 'Arrangements', 'Аранжировки')]
PLAN_SERVICES = [
    dict(id='roses', group='bouquets', addons=['vase', 'choc', 'wrap'],
         label=('Roses', 'Рози'),
         lengths=[dict(id='r5', price=20, minutes=20, label=('5 stems', '5 стръка'), opt=('Roses, 5 stems', 'Рози, 5 стръка')),
                  dict(id='r7', price=26, minutes=20, label=('7 stems', '7 стръка'), opt=('Roses, 7 stems', 'Рози, 7 стръка')),
                  dict(id='r11', price=38, minutes=25, label=('11 stems', '11 стръка'), opt=('Roses, 11 stems', 'Рози, 11 стръка')),
                  dict(id='r21', price=70, minutes=30, label=('21 stems', '21 стръка'), opt=('Roses, 21 stems', 'Рози, 21 стръка'))]),
    dict(id='mixed', group='bouquets', pmin=30, pmax=55, mmin=30, mmax=40, addons=['vase', 'choc', 'wrap'],
         label=('Seasonal mixed bouquet', 'Сезонен микс букет'), opt=('Seasonal mixed bouquet', 'Сезонен микс букет')),
    dict(id='tulips', group='bouquets', pmin=28, pmax=28, mmin=20, mmax=20, addons=['vase', 'choc'],
         label=('Tulip bouquet', 'Букет от лалета'), opt=('Tulip bouquet, 15 stems', 'Букет от лалета, 15 стръка')),
    dict(id='dried', group='bouquets', pmin=35, pmax=35, mmin=30, mmax=30, addons=['choc'],
         label=('Dried flower bouquet', 'Букет от сухи цветя'), opt=('Dried flower bouquet', 'Букет от сухи цветя')),
    dict(id='basket', group='arrangements', pmin=45, pmax=60, mmin=40, mmax=60, addons=['choc'],
         label=('Flower basket', 'Кошница с цветя'), opt=('Flower basket', 'Кошница с цветя')),
    dict(id='box', group='arrangements', pmin=40, pmax=40, mmin=30, mmax=30, addons=['choc'],
         label=('Flower box', 'Кутия с цветя'), opt=('Flower box', 'Кутия с цветя')),
    dict(id='orchid', group='arrangements', pmin=30, pmax=30, mmin=10, mmax=10, addons=['choc', 'wrap'],
         label=('Orchid in a pot', 'Орхидея в саксия'), opt=('Orchid in a pot', 'Орхидея в саксия')),
]
PLAN_ADDONS = [
    dict(id='vase', price=10, minutes=5, label=('Add a vase', 'Ваза')),
    dict(id='choc', price=6, minutes=5, label=('Chocolates or a small gift', 'Шоколад или малък подарък')),
    dict(id='wrap', price=3, minutes=5, label=('Gift wrapping', 'Подаръчна опаковка')),
]


def hours_text(lang):
    wd, we = OPEN_WEEKDAY.replace('-', ' – '), OPEN_WEEKEND.replace('-', ' – ')
    return ('Mon – Fri %s · Sat – Sun %s' % (wd, we)) if lang == 'en' else ('Пон – Пет %s · Съб – Нед %s' % (wd, we))


L = {
 'en': dict(
  lang='en', root='../', script='latin', other_href='../index.html', other_lang='bg', other_label='БГ', other_aria='Превключи на български',
  privacy_href='privacy.html', home_href='index.html',
  title='Mimosa Flowers – fresh bouquets and delivery in Plovdiv',
  desc='Fresh bouquets, roses and flower arrangements made to order in Plovdiv. See the photos and prices, and send an order for pick-up or delivery.',
  skip='Skip to content', tagline='flower shop', nav_label='Main navigation', menu_btn='Menu',
  nav=[('#prices', 'Prices'), ('#gallery', 'Gallery'), ('#reviews', 'Reviews'), ('#faq', 'Questions'), ('#contact', 'Contact')],
  cta='Order flowers',
  h1='Say it with fresh flowers.',
  lead='Bouquets, roses and arrangements made to order in Plovdiv. See the work, choose a bouquet, and send an order for pick-up or delivery.',
  hero_cta2='See bouquets and prices', hero_meta='Plovdiv · open every day', hero_chip='Bouquets · Roses · Gifts',
  hero_alt='A hand holding a bouquet of white roses wrapped in beige paper', hero_side_alt='A flower shop front with ribbons and flowers outside',
  promise_h='What to expect',
  promise=[('Made when you order', 'Every bouquet is arranged by hand after you order, from the flowers we have that day.'),
           ('Delivery on time', 'Choose a day and a time. Order before the cut-off to get your flowers the same day.'),
           ('Clear prices', 'Every item has a price and a preparation time, and the delivery fee is shown before you send.')],
  gal_h='Our flowers', gal_p='Bouquets, vases and the shop. Filter by type, and press a photo to ask for something like it.', gal_filter='Filter photos',
  f_all='All', f_bouquets='Bouquets', f_vases='In a vase', f_shop='The shop', shown='Photos shown: 22', open_photo='Open photo',
  lb_label='Photo', lb_close='Close', lb_prev='Previous photo', lb_next='Next photo', lb_request='Order something like this',
  price_h='Bouquets and prices', price_p='Every item has a price and a preparation time. Not sure what to choose? Tell us the occasion and your budget, and we will suggest.',
  price_cta='Build your order',
  price_note='Sample prices in euro, based on florists in Plovdiv. Flowers change with the season, so a bouquet may differ a little from the photo.',
  menu_alt='A hand holding a small bouquet wrapped in kraft paper', menu=MENU_EN,
  plan_h='Build your order', plan_p='Choose a bouquet and extras to see an estimated price and how long it takes to prepare. Then add it to your order, and we will only offer times that fit before closing.',
  plan_l_service='What would you like?', plan_l_length='Number of roses', plan_l_addons='Add something',
  plan_empty='Choose a bouquet to see the estimate.', plan_price='Estimated price', plan_time='Preparation time',
  plan_req_note='Plus extras priced on request.', plan_add='Add to my order',
  plan_fine='Sample prices. Delivery (7 €) is added when we confirm your order.', plan_on_request='price on request',
  rev_h='What customers say', rev_p='Short notes from people who order from us.', rev_note='Example reviews. Replace them with real Google reviews.',
  reviews=[('The bouquet was exactly what I described, and it arrived on time for the birthday.', 'Mixed bouquet'),
           ('Beautiful roses, nicely wrapped. They stayed fresh for more than a week.', 'Roses'),
           ('Easy to order, a clear price, and a kind message on the card.', 'Delivery')],
  rev_by='Example customer',
  faq_h='Good to know',
  faq=[('Can I order for today?', 'Yes, if you order before the cut-off time shown at the top of the page. Later orders are delivered the next day.'),
       ('How much is delivery?', 'Delivery inside Plovdiv is 7 € on a chosen day and 12 € for express delivery within two hours. Picking up in the shop is free.'),
       ('Can I choose the exact flowers and colours?', 'Yes. Write your wishes in the notes and we will confirm what is possible. Some flowers change with the season.'),
       ('Can you add a card with my message?', 'Yes. Write the text in the form and we will add it to the bouquet.'),
       ('What if the person is not at home?', 'Our courier will call the phone number you give. If nobody answers, we will call you.'),
       ('Do you make wedding and event flowers?', 'Yes. Send a request with the date and a few ideas, and we will arrange a consultation.')],
  contact_h='Order flowers', contact_p='Tell us what you would like and when. We will reply to confirm your order.',
  addr_l='Address', addr='Primer St. 1, Plovdiv', hours_l='Hours',
  phone_l='Phone', email_l='Email',
  map_t='The map is from OpenStreetMap and loads only if you choose.', map_btn='Show the map',
  form_h='Send an order', f_name='Your name', f_phone='Phone', f_service='Bouquet', f_pick='Choose a bouquet',
  f_fulfil='How do you want to receive it?', f_pickup='Pick up in the shop', f_delivery='Delivery in Plovdiv', f_addr='Delivery address and recipient',
  f_date='Date', f_time='Time', f_time_pick='Choose a time', f_hint='Weekday times are shown. Pick a date to see the times for that day.',
  f_card='Card message (optional)', f_msg='Notes for the florist (optional)',
  f_send='Send order',
  chip_look='Photo you like', chip_plan='Your choice', chip_remove='Remove',
  f_note='We use your details only to answer your order.', f_priv='Privacy notice',
  foot_priv='Privacy notice', admin_t='Demo back office', admin_href='../admin.html?lang=en', quick_label='Quick contact', q_call='Call', q_book='Order flowers',
  dock_label='Colour scheme',
 ),
 'bg': dict(
  lang='bg', root='', script='cyrillic', other_href='en/index.html', other_lang='en', other_label='EN', other_aria='Switch to English',
  privacy_href='privacy.html', home_href='index.html',
  title='Mimosa – цветарница в Пловдив: свежи букети и доставка',
  desc='Свежи букети, рози и аранжировки по поръчка в Пловдив. Разгледайте снимките и цените и изпратете поръчка за вземане от магазина или доставка.',
  skip='Към съдържанието', tagline='цветарница', nav_label='Основна навигация', menu_btn='Меню',
  nav=[('#prices', 'Цени'), ('#gallery', 'Галерия'), ('#reviews', 'Отзиви'), ('#faq', 'Въпроси'), ('#contact', 'Контакти')],
  cta='Поръчай цветя',
  h1='Кажи го със свежи цветя.',
  lead='Букети, рози и аранжировки по поръчка в Пловдив. Разгледай работата, избери букет и изпрати поръчка за вземане от магазина или доставка.',
  hero_cta2='Виж букетите и цените', hero_meta='Пловдив · работим всеки ден', hero_chip='Букети · Рози · Подаръци',
  hero_alt='Ръка държи букет от бели рози, увит в бежова хартия', hero_side_alt='Витрина на цветарница с панделки и цветя отпред',
  promise_h='Какво да очакваш',
  promise=[('Направен, когато го поръчаш', 'Всеки букет се подрежда на ръка след поръчката, от цветята, с които разполагаме този ден.'),
           ('Доставка навреме', 'Избери ден и час. Поръчай преди крайния час, за да получиш цветята още днес.'),
           ('Ясни цени', 'До всеки артикул има цена и време за приготвяне, а таксата за доставка се вижда преди да изпратиш.')],
  gal_h='Нашите цветя', gal_p='Букети, вази и магазинът. Филтрирай по вид и натисни снимка, за да поискаш нещо подобно.', gal_filter='Филтър на снимките',
  f_all='Всички', f_bouquets='Букети', f_vases='Във ваза', f_shop='Магазинът', shown='Показани снимки: 22', open_photo='Отвори снимката',
  lb_label='Снимка', lb_close='Затвори', lb_prev='Предишна снимка', lb_next='Следваща снимка', lb_request='Поръчай нещо подобно',
  price_h='Букети и цени', price_p='До всеки артикул има цена и време за приготвяне. Ако не си сигурен какво да избереш, кажи ни повода и бюджета и ще ти предложим.',
  price_cta='Събери поръчката',
  price_note='Примерни цени в евро, по цветарници в Пловдив. Цветята се сменят със сезона, така че букетът може леко да се различава от снимката.',
  menu_alt='Ръка държи малък букет, увит в амбалажна хартия', menu=MENU_BG,
  plan_h='Събери поръчката', plan_p='Избери букет и допълнения и виж ориентировъчна цена и време за приготвяне. После го добави към поръчката си и ще ти предложим само часове, които се събират преди затваряне.',
  plan_l_service='Какво искаш?', plan_l_length='Брой рози', plan_l_addons='Добави нещо',
  plan_empty='Избери букет, за да видиш оценка.', plan_price='Ориентировъчна цена', plan_time='Време за приготвяне',
  plan_req_note='Плюс допълнения, цена по запитване.', plan_add='Добави към поръчката',
  plan_fine='Примерни цени. Доставката (7 €) се добавя, когато потвърдим поръчката.', plan_on_request='цена по запитване',
  rev_h='Какво казват клиентите', rev_p='Кратки бележки от хора, които поръчват от нас.', rev_note='Примерни отзиви. Заменете ги с истински отзиви от Google.',
  reviews=[('Букетът беше точно какъвто го описах и пристигна навреме за рождения ден.', 'Микс букет'),
           ('Красиви рози, хубаво опаковани. Останаха свежи повече от седмица.', 'Рози'),
           ('Лесна поръчка, ясна цена и мило послание на картичката.', 'Доставка')],
  rev_by='Примерен клиент',
  faq_h='Добре е да знаеш',
  faq=[('Мога ли да поръчам за днес?', 'Да, ако поръчаш преди крайния час, показан най-горе на страницата. По-късните поръчки се доставят на следващия ден.'),
       ('Колко струва доставката?', 'Доставката в Пловдив е 7 € в избран ден и 12 € за експресна доставка до два часа. Вземането от магазина е безплатно.'),
       ('Мога ли да избера точните цветя и цветове?', 'Да. Напиши желанията си в бележките и ще потвърдим какво е възможно. Някои цветя се сменят със сезона.'),
       ('Можете ли да добавите картичка с моето послание?', 'Да. Напиши текста във формата и ще го добавим към букета.'),
       ('Какво става, ако човекът не е вкъщи?', 'Куриерът ни ще се обади на телефона, който посочиш. Ако никой не отговори, ще се обадим на теб.'),
       ('Правите ли цветя за сватби и събития?', 'Да. Изпрати запитване с датата и няколко идеи и ще уговорим консултация.')],
  contact_h='Поръчай цветя', contact_p='Кажи ни какво искаш и кога. Ще ти отговорим, за да потвърдим поръчката.',
  addr_l='Адрес', addr='ул. Примерна 1, Пловдив', hours_l='Работно време',
  phone_l='Телефон', email_l='Имейл',
  map_t='Картата е от OpenStreetMap и се зарежда само ако поискаш.', map_btn='Покажи картата',
  form_h='Изпрати поръчка', f_name='Твоето име', f_phone='Телефон', f_service='Букет', f_pick='Избери букет',
  f_fulfil='Как искаш да го получиш?', f_pickup='Вземане от магазина', f_delivery='Доставка в Пловдив', f_addr='Адрес за доставка и получател',
  f_date='Дата', f_time='Час', f_time_pick='Избери час', f_hint='Показани са часовете за делнични дни. Избери дата, за да видиш часовете за конкретния ден.',
  f_card='Послание за картичката (по желание)', f_msg='Бележки за флориста (по желание)',
  f_send='Изпрати поръчката',
  chip_look='Снимка, която ти харесва', chip_plan='Твоят избор', chip_remove='Премахни',
  f_note='Ползваме данните ти само за да отговорим на поръчката ти.', f_priv='Политика за поверителност',
  foot_priv='Политика за поверителност', admin_t='Демо админ панел', admin_href='admin.html', quick_label='Бърза връзка', q_call='Обади се', q_book='Поръчай цветя',
  dock_label='Цветова схема',
 ),
}

TEMPLATE = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'page_template.html'), encoding='utf-8').read()


def build_plan(lang, e):
    """Return (html of the estimator card, json for the script)."""
    i = 1 if lang == 'bg' else 0
    d = L[lang]
    all_opts = {n for g in d['menu'] for n, *_ in g[1]}
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
              'promise_h', 'gal_h', 'gal_p', 'gal_filter', 'f_all', 'f_bouquets', 'f_vases', 'f_shop', 'f_fulfil', 'f_pickup', 'f_delivery', 'f_addr', 'f_card', 'shown', 'lb_label', 'lb_close', 'lb_prev', 'lb_next', 'lb_request',
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
    for g in d['menu']:
        gt, rows = g[0], g[1]
        selectable = len(g) < 3 or g[2]
        rs = []
        for name, time, price, (mn, mx) in rows:
            small = '<small>%s</small>' % e(time) if time else ''
            rs.append('<div class="menu-row"><span class="menu-name">%s%s</span><span class="menu-price">%s</span></div>' % (e(name), small, e(price)))
            if selectable:
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
                  % (key, e(name), e(d['dock_label']), e(name), e(name), 'true' if key == 'sage' else 'false', c1, c2))
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
    'window.MIMOSA_CONFIG = {\n'
    '  mode: "%s",            /* "demo" = requests are kept in this browser only; "live" = real API at apiBase (docs/API.md) */\n'
    '  apiBase: "%s",\n'
    '  hours: { weekday: ["%s", "%s"], weekend: ["%s", "%s"] },\n'
    '  capacity: %d,             /* visits that can run at the same time */\n'
    '  slotMinutes: %d,\n'
    '  leadMinutes: %d,         /* same-day orders need this much notice */\n'
    '  cutoff: "%s",          /* same-day delivery orders close at this time */\n'
    '  latency: [600, 1100]      /* demo only: pretend network delay in milliseconds */\n'
    '};\n'
) % (MODE, API_BASE, OPEN_WEEKDAY.split('-')[0], OPEN_WEEKDAY.split('-')[1], OPEN_WEEKEND.split('-')[0], OPEN_WEEKEND.split('-')[1], CAPACITY, SLOT_MINUTES, LEAD_MINUTES, CUTOFF)
os.makedirs(os.path.join(SHOP, 'js'), exist_ok=True)
open(os.path.join(SHOP, 'js', 'config.js'), 'w', encoding='utf-8').write(cfg)
print('config.js written')
