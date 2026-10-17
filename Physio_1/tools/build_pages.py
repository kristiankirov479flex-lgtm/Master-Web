"""Builds index.html (Bulgarian), en/index.html (English), js/config.js and css/style.css for Motus (a physiotherapy clinic).
Edit the values in this file (visits, prices, areas, therapists, credentials, hours, texts), then run:  python tools/build_pages.py && python tools/build_privacy.py
Everything about the clinic is an example (names, diplomas, numbers, prices): replace it for a real clinic."""
import json, os
from html import escape as esc
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BRAND = 'Motus'

# ---------------- settings you will change for a real clinic ----------------
HOURS = {'weekday': ['08:00', '20:00'], 'weekend': ['09:00', '14:00']}
CAPACITY = 2          # therapists working at the same time
SLOT_MINUTES = 30
LEAD_MINUTES = 120
PHONE, PHONE_HREF, EMAIL = '+359 88 000 0000', '+359880000000', 'clinic@example.com'
ADDRESS = {'bg': 'ул. Примерна 33, Пловдив', 'en': '33 Primer St., Plovdiv'}

# visits you can book: id, minutes, price in euro, (bg name, en name), (bg text, en text), [(bg line, en line), ...]
VISITS = [
 ('first', 60, 45, ('Първа оценка', 'First assessment'), ('Разговор, преглед, диагноза и писмен план', 'A talk, an exam, a diagnosis and a written plan'),
  [('60 минути с терапевт', '60 minutes with a therapist'), ('Писмен план: брой посещения и цена', 'A written plan: number of visits and price'), ('Първите упражнения за вкъщи', 'Your first home exercises')]),
 ('therapy', 45, 35, ('Терапия', 'Therapy session'), ('Ръчна терапия и упражнения', 'Manual therapy and exercises'),
  [('45 минути работа с терапевта', '45 minutes with the therapist'), ('Измерваме напредъка всеки път', 'We measure progress every time'), ('Листове с упражнения със снимки', 'Exercise sheets with pictures')]),
 ('shock', 30, 30, ('Ударно-вълнова терапия', 'Shockwave therapy'), ('За сухожилия и пета, по преценка на терапевта', 'For tendons and the heel, if the therapist advises'),
  [('30 минути', '30 minutes'), ('Само ако терапевтът я препоръча', 'Only if the therapist recommends it'), ('Може да се комбинира с терапия', 'Can be combined with therapy')]),
]
PACK = (('Пакет от 8 терапии', 'Pack of 8 sessions'), 260, ('Платен предварително, валиден 3 месеца. Спестяваш 20 €.', 'Paid in advance, valid for 3 months. You save €20.'),
        [('8 терапии по 45 минути', '8 therapy sessions of 45 minutes'), ('Можеш да ги споделиш с член на семейството', 'You can share them with a family member'), ('Часът се записва, когато ти е удобно', 'Book each visit when it suits you')])
EXTRA_PRICES = [(('Кинезио тейп', 'Kinesiology tape'), ('10 €', '€10')), (('Листове с упражнения', 'Exercise sheets'), (None, None))]
# areas of the body: id, (bg name, en name), (bg examples, en examples)
AREAS = [('back', ('Гръб и кръст', 'Back and lower back'), ('Дискови проблеми, ишиас, схващане след седене', 'Disc problems, sciatica, stiffness after sitting')),
         ('neck', ('Врат', 'Neck'), ('Напрежение, главоболие, болка след дълго пред компютър', 'Tension, headaches, pain after long hours at a computer')),
         ('shoulder', ('Рамо', 'Shoulder'), ('Замръзнало рамо, ротаторен маншет, болка при вдигане на ръка', 'Frozen shoulder, rotator cuff, pain when lifting the arm')),
         ('knee', ('Коляно', 'Knee'), ('Връзки, менискус, болка по стълби и при бягане', 'Ligaments, meniscus, pain on stairs and when running')),
         ('hip', ('Таз и бедро', 'Hip and thigh'), ('Бурсит, схващане в седалището, болка при ходене', 'Bursitis, a tight buttock, pain when walking')),
         ('foot', ('Стъпало и глезен', 'Foot and ankle'), ('Навяхване, петна шпора, ахилесово сухожилие', 'Sprains, heel pain, the Achilles tendon')),
         ('post', ('След операция или травма', 'After surgery or an injury'), ('Протези на коляно и таз, счупвания, възстановяване на връзки', 'Knee and hip replacements, fractures, ligament recovery')),
         ('other', ('Друго / не знам', 'Other / not sure'), ('Опиши ни проблема, а ние ще преценим кой терапевт е подходящ', 'Describe the problem and we will decide which therapist suits you'))]
# cards in "What we can help with": area id, (bg title, en title), (bg text, en text)
CONDS = [AREAS[0], AREAS[1], AREAS[2], AREAS[3],
         ('hip', ('Таз, бедро и стъпало', 'Hip, thigh and foot'), ('Бурсит, болка при ходене, навяхване на глезен, петна шпора', 'Bursitis, pain when walking, ankle sprains, heel pain')),
         AREAS[6]]
# therapists: id, photo, (bg name, en name), (bg role, en role), (bg bio, en bio), credentials, interests
THERAPISTS = [('petrov', 'th-man', ('Николай Петров', 'Nikolay Petrov'), ('Физиотерапевт, 14 години опит', 'Physiotherapist, 14 years of experience'),
               ('Работи с гръб, врат и кръст. Често с хора, които седят цял ден, и с бегачи.', 'Works with the back, neck and lower back. Often with people who sit all day, and with runners.'),
               [('Бакалавър по рехабилитация, 2011 г.', 'Bachelor in Rehabilitation, 2011'), ('Сертификат по мануална терапия', 'Manual therapy certificate'), ('Член на асоциацията на физиотерапевтите, № 0000', 'Member of the physiotherapists’ association, no. 0000')],
               [('Гръб', 'Back'), ('Врат', 'Neck'), ('Бягане', 'Running')]),
              ('stoyanova', 'th-woman', ('Елена Стоянова', 'Elena Stoyanova'), ('Физиотерапевт, 9 години опит', 'Physiotherapist, 9 years of experience'),
               ('Рамо, коляно и възстановяване след операция или спорт. Обяснява всяко упражнение, докато го покаже.', 'Shoulder, knee and recovery after surgery or sport. She explains every exercise until you can do it.'),
               [('Магистър по кинезитерапия, 2015 г.', 'Master in Kinesitherapy, 2015'), ('Обучение по следоперативна рехабилитация', 'Post-surgery rehabilitation training'), ('Член на асоциацията на физиотерапевтите, № 0000', 'Member of the physiotherapists’ association, no. 0000')],
               [('Рамо', 'Shoulder'), ('Коляно', 'Knee'), ('След операция', 'After surgery')])]

SKINS = [('ocean', 'Океан', 'Ocean', '#F4F7FA', '#0B7285'), ('ember', 'Жарава', 'Ember', '#FBF6F2', '#B3410F'), ('forest', 'Гора', 'Forest', '#F3F8F5', '#2F6B4F'),
         ('indigo', 'Индиго', 'Indigo', '#F5F5FB', '#4338CA'), ('night', 'Нощ', 'Night', '#0B1220', '#5CD6E0')]


def dims(name):
    with Image.open(os.path.join(ROOT, 'images', 'stock', name + '.jpg')) as im:
        return im.size


def img(root, name, alt, sizes, cls='', eager=False):
    w, h = dims(name)
    attrs = ' loading="eager" fetchpriority="high"' if eager else ' loading="lazy" decoding="async"'
    c = ' class="%s"' % cls if cls else ''
    u = root + 'images/stock/' + name
    return '<img%s src="%s-800.jpg" srcset="%s-800.jpg 800w, %s.jpg 1600w" sizes="%s" width="%d" height="%d" alt="%s"%s>' % (c, u, u, u, sizes, w, h, esc(alt), attrs)


def build(lang):
    bg = lang == 'bg'
    t = lambda a, b: a if bg else b
    root = '' if bg else '../'
    I = lambda *a, **k: img(root, *a, **k)
    i = 0 if bg else 1
    other_href = 'en/index.html' if bg else '../index.html'
    script = 'cyrillic' if bg else 'latin'
    nb = ' '

    def money(v):
        return ('%d%s€' % (v, nb)) if bg else ('€%d' % v)

    svc_opts = ''.join('<option value="%s" data-min="%d">%s · %s %s · %s</option>' % (s[0], s[1], esc(s[3][i]), s[1], t('мин', 'min'), money(s[2])) for s in VISITS)
    area_opts = ''.join('<option value="%s">%s</option>' % (a[0], a[1][i]) for a in AREAS)
    area_tiles = ''.join('<li><a href="#book" data-area="%s">%s</a></li>' % (a[0], a[1][i]) for a in AREAS)
    cond_cards = ''.join('<li><h3>%s</h3><p>%s</p><a class="more" href="#book" data-area="%s">%s<span class="sr-only"> %s</span></a></li>' % (c[1][i], c[2][i], c[0], t('Запази час', 'Book a visit'), c[1][i]) for c in CONDS)
    ther_opts = '<option value="any">%s</option>' % t('Няма значение', 'No preference') + ''.join('<option value="%s">%s</option>' % (x[0], x[2][i]) for x in THERAPISTS)
    ther_cards = ''.join('<li><figure>%s</figure><div><h3>%s</h3><p class="role">%s</p><p>%s</p><ul class="creds">%s</ul><ul class="tags">%s</ul></div></li>' % (
        I(x[1], x[2][i], '(min-width: 560px) 200px, calc(100vw - 82px)'), x[2][i], x[3][i], x[4][i], ''.join('<li>%s</li>' % c[i] for c in x[5]), ''.join('<li>%s</li>' % g[i] for g in x[6])) for x in THERAPISTS)
    facts = [('60\'', t('първа оценка', 'first assessment')), ('14 %s' % t('г.', 'yrs'), t('опит на водещия терапевт', 'of experience, lead therapist')), ('8', t('области, с които работим', 'areas of the body we treat')), ('0', t('нужни направления', 'referrals needed'))]
    facts_html = ''.join('<li><b>%s</b><span>%s</span></li>' % f for f in facts)
    pillars = [('manual', t('Ръчна терапия', 'Hands-on therapy'), t('Работим с ръце върху мускули, стави и сухожилия, за да намалим болката и да върнем подвижността.', 'We work with our hands on muscles, joints and tendons to reduce pain and restore movement.')),
               ('band', t('Упражнения', 'Exercise'), t('Всеки получава програма, която може да прави. Показваме я, оправяме техниката и я правим по-трудна, когато си готов.', 'Everyone gets a programme they can actually do. We show it, fix the technique and make it harder when you are ready.')),
               ('care', t('Разбиране', 'Understanding'), t('Обясняваме какво е станало и какво е нормално. Когато разбереш болката си, тя по-често си отива.', 'We explain what happened and what is normal. When you understand your pain, it tends to go away sooner.'))]
    pill_alt = {'manual': t('Ръце на терапевт върху гърба на пациент', 'A therapist’s hands on a patient’s back'), 'band': t('Терапевт показва упражнение с зелена ластична лента', 'A therapist showing an exercise with a green resistance band'), 'care': t('Лекар държи ръката на пациент', 'A doctor holding a patient’s hand')}
    pillars_html = ''.join('<li><figure>%s</figure><h3>%s</h3><p>%s</p></li>' % (I(k, pill_alt[k], '(min-width: 900px) 364px, calc(100vw - 40px)'), a, b) for k, a, b in pillars)
    steps = [(t('Оценка', 'Assessment'), t('60 минути разговор и преглед. Казваме какво се е случило и защо боли.', '60 minutes of talking and examination. We tell you what happened and why it hurts.')),
             (t('План', 'Plan'), t('Получаваш писмен план: колко посещения, колко често и колко ще струва.', 'You get a written plan: how many visits, how often and what it will cost.')),
             (t('Терапия', 'Therapy'), t('Ръчна работа и упражнения. На всяко посещение мерим дали има напредък.', 'Manual work and exercises. At every visit we check whether you are improving.')),
             (t('Сам вкъщи', 'On your own'), t('Получаваш няколко прости упражнения със снимки, за да не се връща болката.', 'You get a few simple exercises with pictures so the pain does not return.'))]
    steps_html = ''.join('<li><b>%d</b><div><h3>%s</h3><p>%s</p></div></li>' % (n + 1, a, b) for n, (a, b) in enumerate(steps))
    cards = ''
    for v in VISITS[:2]:
        cards += '<li class="pcard"><h3>%s</h3><p class="pmin">%s %s</p><p class="pprice">%s</p><p class="ptxt">%s</p><ul class="ticks">%s</ul><a class="btn btn-line" href="#book" data-visit="%s">%s</a></li>' % (
            v[3][i], v[1], t('минути', 'minutes'), money(v[2]), v[4][i], ''.join('<li>%s</li>' % l[i] for l in v[5]), v[0], t('Запази', 'Book'))
    cards += '<li class="pcard best"><span class="flag">%s</span><h3>%s</h3><p class="pmin">8 × 45 %s</p><p class="pprice">%s</p><p class="ptxt">%s</p><ul class="ticks">%s</ul><a class="btn btn-main" href="#book" data-visit="therapy">%s</a></li>' % (
        t('Най-изгодно', 'Best value'), PACK[0][i], t('минути', 'minutes'), money(PACK[1]), PACK[2][i], ''.join('<li>%s</li>' % l[i] for l in PACK[3]), t('Започни с терапия', 'Start with a session'))
    extras = ''.join('<li><span>%s</span><b>%s</b></li>' % (e[0][i], (e[1][i] or t('включено', 'included'))) for e in EXTRA_PRICES) + '<li><span>%s</span><b>%s</b></li>' % (VISITS[2][3][i], money(VISITS[2][2]))
    flags = [t('Внезапна силна болка след падане или удар', 'Sudden severe pain after a fall or a blow'), t('Изтръпване или слабост в крак или ръка, които се влошават', 'Numbness or weakness in a leg or arm that is getting worse'),
             t('Болка в гърдите, задух или треска заедно с болката', 'Chest pain, shortness of breath or a fever together with the pain'), t('Проблеми с пикочния мехур или червата заедно с болка в кръста', 'Bladder or bowel problems together with lower back pain')]
    flags_html = ''.join('<li>%s</li>' % f for f in flags)
    faq = [(t('Нужно ли е направление?', 'Do I need a referral?'), t('Не. Можеш да дойдеш директно. Ако имаш снимки, ЯМР или епикриза, носи ги.', 'No. You can come directly. If you have X-rays, an MRI or a hospital report, bring them.')),
           (t('Боли ли по време на терапия?', 'Does therapy hurt?'), t('Понякога усещаш натиск или опъване, но не трябва да е непоносимо. Кажи, и ще го намалим.', 'Sometimes you feel pressure or a stretch, but it should not be unbearable. Say so and we ease off.')),
           (t('Колко посещения ще ми трябват?', 'How many visits will I need?'), t('Зависи от проблема. Казваме ти след първата оценка. Често е между 4 и 10 посещения.', 'It depends on the problem. We tell you after the first assessment. It is often between 4 and 10 visits.')),
           (t('Какво да облека?', 'What should I wear?'), t('Удобни дрехи, в които можеш да се движиш. За рамо или кръст: потник или къси панталони.', 'Comfortable clothes you can move in. For a shoulder or the lower back: a vest or shorts.')),
           (t('Ако не се подобря?', 'What if I do not improve?'), t('След две-три посещения проверяваме напредъка. Ако няма промяна, казваме го честно и те насочваме към лекар за допълнителни изследвания.', 'After two or three visits we check progress. If nothing changes, we say so honestly and send you to a doctor for further tests.'))]
    faq_html = ''.join('<details class="qa"><summary>%s</summary><p>%s</p></details>' % f for f in faq)
    hours_rows = [(t('Понеделник – петък', 'Monday – Friday'), HOURS['weekday'], 'wd'), (t('Събота и неделя', 'Saturday and Sunday'), HOURS['weekend'], 'we')]
    hours_html = ''.join('<div data-hrs="%s"><dt>%s</dt><dd>%s – %s</dd></div>' % (k, n, h[0], h[1]) for n, h, k in hours_rows)
    hours_ld = '"Mo-Fr %s-%s","Sa-Su %s-%s"' % (HOURS['weekday'][0], HOURS['weekday'][1], HOURS['weekend'][0], HOURS['weekend'][1])
    swatches = ''.join('<button class="sw" type="button" data-skin="%s" style="--s1:%s;--s2:%s" aria-pressed="false" aria-label="%s"></button>' % (k, s1, s2, b if bg else e) for k, b, e, s1, s2 in SKINS)
    nav = [('#conditions', t('Какво лекуваме', 'What we treat')), ('#how', t('Как работим', 'How we work')), ('#team', t('Терапевти', 'Therapists')), ('#prices', t('Цени', 'Prices')), ('#visit', t('Контакти', 'Contact'))]
    nav_html = ''.join('<a href="%s">%s</a>' % n for n in nav)
    data = {'services': {s[0]: s[3][i] for s in VISITS}, 'areas': {a[0]: a[1][i] for a in AREAS}, 'therapists': {x[0]: x[2][i] for x in THERAPISTS}}
    after = [t('Получаваш отговор в рамките на работния ден.', 'You get an answer within the working day.'), t('Звъним, за да потвърдим часа и да отговорим на въпросите ти.', 'We call to confirm the time and answer your questions.'), t('Не плащаш предварително. Плащаш след посещението.', 'You do not pay in advance. You pay after the visit.')]
    after_html = ''.join('<li>%s</li>' % a for a in after)
    gal = [('room', t('Кабинет за терапия със светъл прозорец', 'A treatment room with a bright window'), t('Кабинет за терапия', 'Treatment room')), ('parallel', t('Терапевт и пациентка до успоредка за ходене', 'A therapist and a patient at the walking bars'), t('Зала за рехабилитация', 'Rehabilitation area')),
           ('equipment', t('Оборудване за упражнения, подредено на дървена стена', 'Exercise equipment arranged on a wooden wall'), t('Оборудване за упражнения', 'Exercise equipment')), ('gym', t('Просторна зала с уреди за кардио', 'A spacious hall with cardio machines'), t('Зала за по-тежки упражнения', 'Hall for stronger exercise'))]
    gal_html = ''.join('<li><figure>%s<figcaption>%s</figcaption></figure></li>' % (I(g[0], g[1], '(min-width: 900px) 364px, (min-width: 560px) calc(50vw - 27px), calc(100vw - 40px)'), g[2]) for g in gal)

    title = t('Motus – физиотерапия в Пловдив. Запази час онлайн', 'Motus – physiotherapy in Plovdiv. Book an appointment online')
    desc = t('Motus е кабинет по физиотерапия в Пловдив: болка в гърба, врата, рамото и коляното, възстановяване след операция. Писмен план още след първата оценка. Запази час.',
             'Motus is a physiotherapy clinic in Plovdiv: pain in the back, neck, shoulder and knee, and recovery after surgery. A written plan after the first assessment. Book an appointment.')

    return '''<!doctype html>
<html lang="%(lang)s" data-skin="ocean">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="theme-color" content="#F4F7FA">
<title>%(title)s</title>
<meta name="description" content="%(desc)s">
<meta property="og:type" content="website">
<meta property="og:title" content="%(title)s">
<meta property="og:description" content="%(desc)s">
<meta property="og:locale" content="%(lang)s">
<!-- When the real address is known add, on BOTH language pages:
     <link rel="canonical" href="https://YOUR-DOMAIN/ (or /en/)">
     <link rel="alternate" hreflang="bg" href="https://YOUR-DOMAIN/">
     <link rel="alternate" hreflang="en" href="https://YOUR-DOMAIN/en/">
     <link rel="alternate" hreflang="x-default" href="https://YOUR-DOMAIN/">
     and an og:image (images/stock/hero.jpg is a placeholder) -->
<link rel="preload" href="%(root)sfonts/onest-%(script)s.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="%(root)sfonts/fonts.css">
<link rel="stylesheet" href="%(root)scss/style.css">
<script>
  /* Apply the saved colour scheme before the page paints, so it does not flash. */
  try { var s = new URLSearchParams(location.search).get("skin") || localStorage.getItem("motusSkin"); if (s) document.documentElement.dataset.skin = s; } catch (e) {}
</script>
<script type="application/ld+json">
{"@context":"https://schema.org","@type":"Physiotherapy","name":"%(brand)s","inLanguage":"%(lang)s","telephone":"%(phone_href)s","email":"%(email)s",
 "address":{"@type":"PostalAddress","streetAddress":"Primer St. 33","addressLocality":"Plovdiv","addressCountry":"BG"},"openingHours":[%(hours_ld)s]}
</script>
</head>
<body>
<a class="skip" href="#main">%(skip)s</a>

<header class="top" id="top">
  <div class="top-in">
    <a class="logo" href="index.html">%(brand_html)s</a>
    <nav class="nav" id="nav" aria-label="%(nav_label)s">%(nav_html)s</nav>
    <div class="top-r">
      <a class="call" href="tel:%(phone_href)s"><span class="call-l">%(call_l)s</span> <b>%(phone)s</b></a>
      <a class="lang" href="%(other_href)s" lang="%(other_lang)s" hreflang="%(other_lang)s" aria-label="%(other_aria)s">%(other_label)s</a>
      <button class="burger" id="burger" type="button" aria-controls="nav" aria-expanded="false" aria-label="%(menu_btn)s"><span></span></button>
    </div>
  </div>
</header>

<main id="main">

  <!-- ============ Hero ============ -->
  <section class="hero" aria-labelledby="h1">
    <div class="wrap hero-in">
      <div class="hero-copy">
        <p class="eyebrow">%(eyebrow)s</p>
        <h1 id="h1">%(h1)s</h1>
        <p class="lead">%(lead)s</p>
        <p class="hero-links"><a class="btn btn-light" href="#book">%(cta1)s</a> <a class="btn btn-ghost" href="tel:%(phone_href)s">%(cta2)s</a></p>
        <ul class="proof"><li>%(pf1)s</li><li>%(pf2)s</li><li>%(pf3)s</li></ul>
      </div>
      <figure class="hero-ph">%(hero_img)s</figure>
    </div>
  </section>

  <!-- ============ Where does it hurt ============ -->
  <section class="finder-wrap" aria-labelledby="fd-h">
    <div class="wrap">
      <div class="finder">
        <h2 id="fd-h">%(where_h)s</h2>
        <ul class="areas">%(area_tiles)s</ul>
      </div>
    </div>
  </section>

  <!-- ============ Facts ============ -->
  <section class="facts-wrap" aria-label="%(facts_l)s">
    <ul class="wrap facts">%(facts_html)s</ul>
  </section>

  <!-- ============ What we treat ============ -->
  <section class="block" id="conditions" aria-labelledby="cd-h">
    <div class="wrap">
      <header class="sec-head"><h2 id="cd-h">%(cond_h)s</h2><p>%(cond_p)s</p></header>
      <ul class="conds">%(cond_cards)s</ul>
    </div>
  </section>

  <!-- ============ How we work ============ -->
  <section class="block dark-sec" id="how" aria-labelledby="hw-h">
    <div class="wrap how">
      <figure class="how-ph">%(how_img)s</figure>
      <div>
        <header class="sec-head"><h2 id="hw-h">%(how_h)s</h2><p>%(how_p)s</p></header>
        <ol class="steps4">%(steps_html)s</ol>
      </div>
    </div>
  </section>

  <!-- ============ Pillars ============ -->
  <section class="block" aria-labelledby="pl-h">
    <div class="wrap">
      <header class="sec-head center"><h2 id="pl-h">%(pill_h)s</h2><p>%(pill_p)s</p></header>
      <ul class="pillars">%(pillars_html)s</ul>
    </div>
  </section>

  <!-- ============ Therapists ============ -->
  <section class="block soft" id="team" aria-labelledby="tm-h">
    <div class="wrap">
      <header class="sec-head"><h2 id="tm-h">%(team_h)s</h2><p>%(team_p)s</p></header>
      <ul class="team">%(ther_cards)s</ul>
      <p class="p-note">%(team_note)s</p>
    </div>
  </section>

  <!-- ============ Clinic ============ -->
  <section class="block" id="clinic" aria-labelledby="cl-h">
    <div class="wrap">
      <header class="sec-head"><h2 id="cl-h">%(clinic_h)s</h2><p>%(clinic_p)s</p></header>
      <ul class="gallery">%(gal_html)s</ul>
    </div>
  </section>

  <!-- ============ Prices ============ -->
  <section class="block soft" id="prices" aria-labelledby="pr-h">
    <div class="wrap">
      <header class="sec-head center"><h2 id="pr-h">%(prices_h)s</h2><p>%(prices_p)s</p></header>
      <ul class="pcards">%(cards)s</ul>
      <div class="extras">
        <h3>%(extras_h)s</h3>
        <ul>%(extras)s</ul>
      </div>
      <p class="p-note center-note">%(sv_note)s</p>
    </div>
  </section>

  <!-- ============ Doctor first ============ -->
  <section class="block" aria-labelledby="fl-h">
    <div class="wrap flags">
      <div>
        <h2 id="fl-h">%(flags_h)s</h2>
        <p>%(flags_p)s</p>
      </div>
      <ul class="ticks warn">%(flags_html)s</ul>
    </div>
  </section>

  <!-- ============ Book ============ -->
  <section class="block dark-sec" id="book" aria-labelledby="bk-h">
    <div class="wrap book">
      <div class="book-side">
        <h2 id="bk-h">%(book_h)s</h2>
        <p>%(book_p)s</p>
        <ul class="after">%(after_html)s</ul>
        <p class="book-tel"><span>%(or_call)s</span> <a href="tel:%(phone_href)s">%(phone)s</a></p>
      </div>
      <div class="book-card">
        <form class="res" id="apptForm" novalidate>
          <div class="row2">
            <div class="field"><label for="f-service">%(f_service)s</label><select id="f-service" name="service">%(svc_opts)s</select></div>
            <div class="field"><label for="f-area">%(f_area)s</label><select id="f-area" name="area">%(area_opts)s</select></div>
          </div>
          <div class="field"><label for="f-ther">%(f_ther)s</label><select id="f-ther" name="therapist">%(ther_opts)s</select></div>
          <div class="row2">
            <div class="field"><label for="f-date">%(f_date)s</label><input id="f-date" name="date" type="date" required></div>
            <div class="field"><label for="f-time">%(f_time)s</label><select id="f-time" name="time" required></select></div>
          </div>
          <p class="hint" id="timeHint" role="status">%(checking)s</p>
          <div class="row2">
            <div class="field"><label for="f-name">%(f_name)s</label><input id="f-name" name="name" type="text" autocomplete="name" required></div>
            <div class="field"><label for="f-phone">%(f_phone)s</label><input id="f-phone" name="phone" type="tel" autocomplete="tel" required></div>
          </div>
          <div class="field"><label for="f-msg">%(f_msg)s</label><textarea id="f-msg" name="msg" rows="3"></textarea><p class="hint">%(f_msg_h)s</p></div>
          <p class="demo-note" id="demoNote" hidden></p>
          <p class="form-error" id="aError" role="alert" hidden></p>
          <button class="btn btn-main" type="submit" id="aSend">%(f_send)s</button>
          <small class="fine">%(f_note)s <a href="%(privacy_href)s">%(f_priv)s</a></small>
        </form>
        <div class="done" id="aDone" hidden tabindex="-1"></div>
      </div>
    </div>
  </section>

  <!-- ============ FAQ ============ -->
  <section class="block" aria-labelledby="fq-h">
    <div class="wrap narrow">
      <header class="sec-head"><h2 id="fq-h">%(faq_h)s</h2></header>
      <div class="qas">%(faq_html)s</div>
    </div>
  </section>

  <!-- ============ Contact ============ -->
  <section class="block soft" id="visit" aria-labelledby="vs-h">
    <div class="wrap visit">
      <div class="visit-copy">
        <h2 id="vs-h">%(visit_h)s</h2>
        <dl class="hours" id="hours">%(hours_html)s</dl>
        <ul class="info">
          <li><b>%(l_addr)s</b><span>%(address)s</span></li>
          <li><b>%(l_phone)s</b><a href="tel:%(phone_href)s">%(phone)s</a></li>
          <li><b>%(l_email)s</b><a href="mailto:%(email)s">%(email)s</a></li>
        </ul>
        <p class="visit-note">%(visit_note)s</p>
      </div>
      <div class="visit-side">
        <div class="map-box" id="mapBox" data-src="https://www.openstreetmap.org/export/embed.html?bbox=24.7353%%2C42.1304%%2C24.7553%%2C42.1404&amp;layer=mapnik&amp;marker=42.1354%%2C24.7453">
          <div class="map-ph">
            <p>%(map_t)s</p>
            <button class="btn btn-line btn-sm" type="button" id="mapLoad">%(map_btn)s</button>
          </div>
        </div>
      </div>
    </div>
  </section>

</main>

<footer class="foot dark">
  <div class="wrap foot-row">
    <span>© <span id="year">2026</span> Motus. %(foot_demo)s</span>
    <span class="foot-links"><a href="%(privacy_href)s">%(f_priv)s</a> <a href="%(admin_href)s">%(admin_l)s</a></span>
  </div>
</footer>

<aside class="dock" aria-label="%(dock_label)s">
  <div class="dock-label"><small>%(dock_label)s</small><b id="skinName">%(skin_name)s</b></div>
  <div class="swatches">%(swatches)s</div>
</aside>

<script type="application/json" id="motusData">%(data)s</script>
<script src="%(root)sjs/config.js"></script>
<script src="%(root)sjs/api.js"></script>
<script src="%(root)sjs/main.js"></script>
</body>
</html>
''' % dict(
        lang=lang, title=esc(title), desc=esc(desc), root=root, script=script, brand=BRAND, brand_html='Motus', phone_href=PHONE_HREF, phone=PHONE, email=EMAIL, hours_ld=hours_ld,
        skip=t('Към съдържанието', 'Skip to content'), nav_label=t('Навигация', 'Navigation'), nav_html=nav_html, call_l=t('Обади се', 'Call'),
        other_href=other_href, other_lang='en' if bg else 'bg', other_label='EN' if bg else 'БГ', other_aria='Switch to English' if bg else 'Превключи на български', menu_btn=t('Меню', 'Menu'),
        eyebrow=t('Физиотерапия · Пловдив', 'Physiotherapy · Plovdiv'),
        h1=t('Върни се към движението без болка', 'Get back to moving without pain'),
        lead=t('Двама опитни физиотерапевти, 60-минутна първа оценка и писмен план с брой посещения и цена. Без направление и без излишни посещения.', 'Two experienced physiotherapists, a 60-minute first assessment and a written plan with the number of visits and the price. No referral and no unnecessary visits.'),
        cta1=t('Запази час', 'Book an appointment'), cta2=t('Обади се', 'Call us'),
        pf1=t('Без направление', 'No referral needed'), pf2=t('Писмен план след първата оценка', 'A written plan after the first assessment'), pf3=t('Плащаш след посещението', 'Pay after the visit'),
        hero_img=I('hero', t('Физиотерапевт мобилизира рамото и гърба на пациентка на масата за терапия', 'A physiotherapist mobilising a patient’s shoulder and back on the treatment couch'), '(min-width: 900px) 560px, calc(100vw - 40px)', eager=True),
        where_h=t('Къде те боли? Избери и запази час', 'Where does it hurt? Choose and book'), area_tiles=area_tiles,
        facts_l=t('Накратко', 'In short'), facts_html=facts_html,
        cond_h=t('С какво можем да помогнем', 'What we can help with'), cond_p=t('Най-честите проблеми, с които идват при нас. Ако твоят не е тук, опиши го във формата.', 'The most common problems people come to us with. If yours is not here, describe it in the form.'), cond_cards=cond_cards,
        how_h=t('Как работим', 'How we work'), how_p=t('Целта е да се върнеш към това, което правиш, и да не идваш повече от нужното.', 'The aim is to get you back to what you do, and not to see you more often than needed.'), steps_html=steps_html,
        how_img=I('consult', t('Лекар показва на пациент образно изследване на таблет', 'A doctor showing a patient a scan on a tablet'), '(min-width: 900px) 515px, calc(100vw - 40px)'),
        pill_h=t('Три неща, които правим при всеки', 'Three things we do with everyone'), pill_p=t('Добрата физиотерапия не е само масаж. Съчетаваме ръчна работа, упражнения и обяснение.', 'Good physiotherapy is not just a massage. We combine hands-on work, exercise and explanation.'), pillars_html=pillars_html,
        team_h=t('Терапевтите', 'The therapists'), team_p=t('Двама терапевти. Знаеш при кого идваш и какъв е опитът му.', 'Two therapists. You know whom you are seeing and what experience they have.'), ther_cards=ther_cards,
        team_note=t('Имена, дипломи и номера на членство са примерни.', 'Names, diplomas and membership numbers are examples.'),
        clinic_h=t('Кабинетът', 'The clinic'), clinic_p=t('Светло, тихо и подредено. Има отделен кабинет за терапия и зала за упражнения.', 'Bright, quiet and tidy. There is a separate treatment room and an exercise hall.'), gal_html=gal_html,
        prices_h=t('Цени', 'Prices'), prices_p=t('Цените са в евро и са ясни предварително. Първата оценка включва писмен план. Не взимаме пари за посещения, които не са нужни.', 'Prices are in euros and clear beforehand. The first assessment includes a written plan. We do not charge for visits that are not needed.'), cards=cards,
        extras_h=t('Допълнително', 'Extras'), extras=extras, sv_note=t('Плащане в брой или с карта след посещението.', 'Payment by cash or card after the visit.'),
        flags_h=t('Първо при лекар, ако има:', 'See a doctor first if you have:'), flags_p=t('Физиотерапията не е за всичко. Тези знаци означават, че първо трябва да те види лекар.', 'Physiotherapy is not for everything. These signs mean a doctor should see you first.'), flags_html=flags_html,
        book_h=t('Запази час', 'Book an appointment'), book_p=t('Избери посещение, област, ден и час. Ще ти се обадим само ако трябва да променим нещо.', 'Choose a visit, an area, a day and a time. We only call you if something has to change.'),
        after_html=after_html, or_call=t('Предпочиташ да се обадиш?', 'Prefer to call?'),
        f_service=t('Посещение', 'Visit'), svc_opts=svc_opts, f_area=t('Къде те боли?', 'Where does it hurt?'), area_opts=area_opts, f_ther=t('Терапевт', 'Therapist'), ther_opts=ther_opts, f_date=t('Дата', 'Date'), f_time=t('Час', 'Time'),
        checking=t('Избери посещение и дата, за да видиш свободните часове.', 'Choose a visit and a date to see the free times.'),
        f_name=t('Име', 'Name'), f_phone=t('Телефон', 'Phone'), f_msg=t('Бележка (по желание)', 'Note (optional)'), f_msg_h=t('Не пиши подробна медицинска информация тук. Кажи я на терапевта при посещението.', 'Please do not write detailed medical information here. Tell the therapist at the visit.'),
        f_send=t('Заяви час', 'Request the appointment'), f_note=t('Не е нужно да плащаш предварително.', 'You do not have to pay in advance.'), f_priv=t('Поверителност', 'Privacy'), privacy_href='privacy.html',
        faq_h=t('Често задавани въпроси', 'Common questions'), faq_html=faq_html,
        visit_h=t('Контакти', 'Contact'), hours_html=hours_html, address=ADDRESS['bg' if bg else 'en'], l_addr=t('Адрес', 'Address'), l_phone=t('Телефон', 'Phone'), l_email=t('Имейл', 'Email'),
        visit_note=t('Входът е на първия етаж, без стъпала. Паркирането е безплатно пред сградата.', 'The entrance is on the ground floor, without steps. Parking is free in front of the building.'),
        map_t=t('Картата се зарежда от OpenStreetMap едва когато я поискаш.', 'The map loads from OpenStreetMap only when you ask for it.'), map_btn=t('Покажи картата', 'Show the map'),
        foot_demo=t('Всичко тук е пример.', 'Everything here is an example.'), admin_href='admin.html' if bg else '../admin.html?lang=en', admin_l=t('Демо админ панел', 'Demo back office'),
        dock_label=t('Цветова схема', 'Colour scheme'), skin_name=t('Океан', 'Ocean'), swatches=swatches,
        data=json.dumps(data, ensure_ascii=False).replace('</', '<\\/'),
    )


def main():
    cfg = ('/* Generated by tools/build_pages.py. Edit the values at the top of that file, then run it again. */\n'
           'window.MOTUS_CONFIG = {\n  mode: "demo",            /* "demo" = requests are kept in this browser only; "live" = real API at apiBase (docs/API.md) */\n'
           '  apiBase: "/api",\n  hours: { weekday: ["%s", "%s"], weekend: ["%s", "%s"] },\n  capacity: %d,             /* therapists working at the same time */\n'
           '  slotMinutes: %d,\n  leadMinutes: %d,\n  latency: [600, 1100]      /* demo only: pretend network delay in milliseconds */\n};\n'
           % (HOURS['weekday'][0], HOURS['weekday'][1], HOURS['weekend'][0], HOURS['weekend'][1], CAPACITY, SLOT_MINUTES, LEAD_MINUTES))
    open(os.path.join(ROOT, 'js', 'config.js'), 'w', encoding='utf-8').write(cfg)
    for lang, path in (('bg', 'index.html'), ('en', os.path.join('en', 'index.html'))):
        os.makedirs(os.path.dirname(os.path.join(ROOT, path)), exist_ok=True)
        open(os.path.join(ROOT, path), 'w', encoding='utf-8').write(build(lang))
    shared = open(os.path.join(ROOT, 'tools', 'shared.css'), encoding='utf-8').read()
    design = open(os.path.join(ROOT, 'tools', 'design.css'), encoding='utf-8').read()
    os.makedirs(os.path.join(ROOT, 'css'), exist_ok=True)
    open(os.path.join(ROOT, 'css', 'style.css'), 'w', encoding='utf-8').write(shared + '\n' + design)
    print('built')


if __name__ == '__main__':
    main()
