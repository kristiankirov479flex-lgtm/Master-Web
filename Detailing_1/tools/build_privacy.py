import os
NAIL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

PAGE = '''<!doctype html>
<html lang="[[lang]]" data-skin="graphite">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="theme-color" content="#F2F3F4">
<title>[[title]]</title>
<!-- Remove the line below once every yellow field on this page is filled in. -->
<meta name="robots" content="noindex">
<link rel="preload" href="[[root]]fonts/onest-[[script]].woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="[[root]]fonts/unbounded-[[script]].woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="[[root]]fonts/fonts.css">
<link rel="stylesheet" href="[[root]]css/style.css">
<script>
  try { var s = new URLSearchParams(location.search).get("skin") || localStorage.getItem("kristalSkin"); if (s) document.documentElement.dataset.skin = s; } catch (e) {}
</script>
</head>
<body>
<a class="skip" href="#main">[[skip]]</a>
<header class="top scrolled static">
  <div class="wrap">
    <a class="logo" href="[[home_href]]"><b>Kristal</b><span>[[tagline]]</span></a>
    <nav class="nav nav-static" aria-label="[[nav_label]]">
      <a href="[[home_href]]">[[back]]</a>
      <a class="lang" href="[[other_href]]" lang="[[other_lang]]" hreflang="[[other_lang]]" aria-label="[[other_aria]]">[[other_label]]</a>
    </nav>
  </div>
</header>
<main id="main" class="legal">
  <div class="wrap">
[[body]]
  </div>
</main>
<footer class="foot dark">
  <div class="wrap foot-row">
    <span>© 2026 Kristal Detailing</span>
    <a href="[[home_href]]">[[back]]</a>
  </div>
</footer>
</body>
</html>
'''

EN = '''    <h1>Privacy notice</h1>
    <p class="meta">Last updated: <span class="todo">[date]</span></p>
    <p>This page explains in plain language what personal data is handled when you visit this website or contact us, and what your rights are.</p>

    <h2>1. Who is responsible</h2>
    <p><span class="todo">[name of the owner or company]</span>, company number <span class="todo">[company number, if any]</span>, address: <span class="todo">[registered address]</span>.<br>
    Email: <a href="mailto:email@example.com">email@example.com</a> · Phone: <a href="tel:+359000000000">+359 000 000 000</a></p>

    <h2>2. What is handled and why</h2>
    <h3>Visiting the website</h3>
    <p>When you open the site, the hosting provider automatically records technical data: your IP address, the date and time, the page requested and your browser type. This is for security and for the site to work. Legal basis: legitimate interest (Article 6(1)(f) of Regulation (EU) 2016/679, the “GDPR”). We do not use this data for advertising or profiling.</p>

    <h3>When you contact us</h3>
    <p><strong>Demo mode.</strong> When you press “Send the request”, the details are saved only in your own browser (in “localStorage”) so the page can show you a confirmation and a reference number. Nothing is sent to us or to any server. <span class="todo">[When the site is connected to a real request system, replace this sentence: say that the request is sent to our server, which database and provider hold it, who can see it, how long it is kept and the legal basis.]</span> If you call or write to us, we handle what you give us: name, phone number, your car make and model, its size, the package and extras you choose, the day and time and your notes. We use it to reply and prepare an offer. Legal basis: steps taken at your request before a contract, and performing the contract (Article 6(1)(b) GDPR). We keep it until your enquiry is dealt with and for <span class="todo">[period, e.g. 12 months]</span> after the last contact. Some data is kept longer where the law requires it (for example accounting records).</p>

    <h3>Choices remembered in your browser</h3>
    <p>The site can save choices on your device: the colour scheme you picked and, in demo mode, the requests you send (so the confirmation, the free times and the demo back office page can show them). They stay with you (in “localStorage”) and are not sent to us. What you pick in “Book your car in” stays on the page only until you close or reload it, and is not saved. The language is set by the page address. We do not use cookies for tracking, analytics or advertising, and the site does not load fonts, scripts or images from other companies.</p>

    <h3>Map from OpenStreetMap</h3>
    <p>The map in the Contact section loads only if you press “Show the map”. Your browser then connects to OpenStreetMap servers, which receive your IP address and browser details. Legal basis: your consent (Article 6(1)(a) GDPR), which you give by pressing the button. Nothing is saved, so the map will ask again on your next visit. More about OpenStreetMap: <a href="https://wiki.osmfoundation.org/wiki/Privacy_Policy" target="_blank" rel="noopener">OpenStreetMap Foundation privacy policy</a>.</p>

    <h3>Links to other services</h3>
    <p>When you tap a phone number or an email address, your phone or email app opens and its own rules apply.</p>

    <h2>3. Who data is shared with</h2>
    <p>With the website's hosting provider (<span class="todo">[e.g. GitHub Pages / other provider]</span>), with our email provider, and, only if you press the map button, with OpenStreetMap. Data is not sold. If a provider uses servers outside the EU (for example in the USA), the transfer relies on safeguards under Articles 44–49 GDPR, such as the EU–US Data Privacy Framework or standard contractual clauses. <span class="todo">[Confirm for the chosen host and email provider.]</span></p>

    <h2>4. Your rights</h2>
    <p>You can ask for access to your data, correction, erasure, restriction of processing and portability, and you can object to processing based on legitimate interest. You can withdraw consent at any time. To use your rights, email us at <a href="mailto:email@example.com">email@example.com</a>.</p>
    <p>If you think your rights have been breached, you can complain to the Bulgarian Commission for Personal Data Protection (КЗЛД): <a href="https://www.cpdp.bg" target="_blank" rel="noopener">www.cpdp.bg</a>, or to the data protection authority in your own country.</p>

    <h2>5. Automated decisions</h2>
    <p>We do not make decisions based solely on automated processing or profiling.</p>

    <h2>6. Changes</h2>
    <p>If this notice changes, the new version will be published on this page and the date above will be updated.</p>'''

BG = '''    <h1>Политика за поверителност</h1>
    <p class="meta">Последна промяна: <span class="todo">[дата]</span></p>
    <p>Тук обясняваме просто и ясно какви лични данни се обработват, когато посещавате този сайт или се свързвате с нас, и какви са правата ви.</p>

    <h2>1. Кой е администраторът</h2>
    <p><span class="todo">[име на собственика или фирмата]</span>, ЕИК <span class="todo">[ЕИК, ако има]</span>, адрес: <span class="todo">[адрес по регистрация]</span>.<br>
    Имейл: <a href="mailto:email@example.com">email@example.com</a> · Телефон: <a href="tel:+359000000000">+359 000 000 000</a></p>

    <h2>2. Какво се обработва и защо</h2>
    <h3>Посещение на сайта</h3>
    <p>Когато отворите сайта, хостинг доставчикът автоматично записва технически данни: IP адрес, дата и час, заявена страница и тип браузър. Целта е сигурност и нормална работа на сайта. Основание: легитимен интерес (чл. 6, пар. 1, б. „е“ от Регламент (ЕС) 2016/679, „ОРЗД“). Не използваме тези данни за реклама или профилиране.</p>

    <h3>Когато се свържете с нас</h3>
    <p><strong>Демо режим.</strong> Когато натиснете „Изпрати заявката“, данните се записват само във вашия браузър (в „localStorage“), за да може страницата да ви покаже потвърждение и номер на заявката. Нищо не се изпраща към нас или към друг сървър. <span class="todo">[Когато сайтът бъде свързан с истинска система за заявки, заменете това изречение: посочете, че заявката се изпраща към нашия сървър, коя база данни и кой доставчик я пазят, кой има достъп, колко време се пази и какво е правното основание.]</span> Ако ни се обадите или пишете, обработваме това, което ни дадете: име, телефон, марката и модела на автомобила, размера му, избрания пакет и допълнения, деня и часа и бележките ви. Използваме го, за да ви отговорим и да подготвим оферта. Основание: стъпки по ваше искане преди сключване на договор и изпълнение на договор (чл. 6, пар. 1, б. „б“ ОРЗД). Пазим го, докато обработим запитването, и до <span class="todo">[срок, напр. 12 месеца]</span> след последния контакт. Част от данните се пазят по-дълго, когато това се изисква от закона (например счетоводни документи).</p>

    <h3>Избори, запомнени във вашия браузър</h3>
    <p>Сайтът може да запише във вашето устройство: цветовата схема, която сте избрали, и, в демо режим, заявките, които изпращате (за да ги покажат потвърждението, свободните часове и демо админ панелът). Те се пазят само при вас (в „localStorage“) и не се изпращат към нас. Това, което изберете в „Запази час за колата“, остава на страницата само докато я затворите или презаредите и не се запазва. Езикът се определя от адреса на страницата. Не използваме бисквитки за проследяване, анализи или реклама и не зареждаме шрифтове, скриптове или снимки от други компании.</p>

    <h3>Карта от OpenStreetMap</h3>
    <p>Картата в раздел „Контакти“ се зарежда само ако натиснете „Покажи картата“. Тогава браузърът ви се свързва със сървъри на OpenStreetMap, които получават вашия IP адрес и данни за браузъра. Основание: вашето съгласие (чл. 6, пар. 1, б. „а“ ОРЗД), което давате с натискането на бутона. Нищо не се запазва, затова при следващо посещение картата ще попита отново. Повече за OpenStreetMap: <a href="https://wiki.osmfoundation.org/wiki/Privacy_Policy" target="_blank" rel="noopener">политика за поверителност на OpenStreetMap Foundation</a>.</p>

    <h3>Връзки към други услуги</h3>
    <p>Когато натиснете телефонен номер или имейл адрес, се отваря приложението за обаждания или имейл на вашето устройство и важат неговите собствени правила.</p>

    <h2>3. С кого се споделят данни</h2>
    <p>С хостинг доставчика на сайта (<span class="todo">[напр. GitHub Pages / друг доставчик]</span>), с нашия имейл доставчик и, само ако натиснете бутона за картата, с OpenStreetMap. Данни не се продават. Ако доставчик използва сървъри извън ЕС (например в САЩ), прехвърлянето се основава на гаранции по чл. 44–49 ОРЗД, например Рамката ЕС–САЩ за поверителност на данните или стандартни договорни клаузи. <span class="todo">[Потвърдете според избрания хостинг и имейл доставчик.]</span></p>

    <h2>4. Вашите права</h2>
    <p>Имате право да поискате достъп до данните си, коригиране, изтриване, ограничаване на обработката и преносимост и да възразите срещу обработка, основана на легитимен интерес. Можете да оттеглите съгласие по всяко време. За да упражните права, пишете ни на <a href="mailto:email@example.com">email@example.com</a>.</p>
    <p>Ако смятате, че правата ви са нарушени, можете да подадете жалба до Комисията за защита на личните данни (КЗЛД): <a href="https://www.cpdp.bg" target="_blank" rel="noopener">www.cpdp.bg</a>.</p>

    <h2>5. Автоматизирани решения</h2>
    <p>Не вземаме решения, които се основават само на автоматизирана обработка или профилиране.</p>

    <h2>6. Промени</h2>
    <p>Ако тази политика се промени, новата версия ще бъде публикувана на тази страница и датата отгоре ще бъде обновена.</p>'''

CFG = {
 'bg': dict(lang='bg', root='', script='cyrillic', title='Политика за поверителност – Kristal', skip='Към съдържанието', home_href='index.html',
            tagline='детайлинг студио', nav_label='Навигация', back='← Към сайта', other_href='en/privacy.html', other_lang='en', other_label='EN', other_aria='Switch to English', body=BG,
            path=os.path.join(NAIL, 'privacy.html')),
 'en': dict(lang='en', root='../', script='latin', title='Privacy notice – Kristal', skip='Skip to content', home_href='index.html',
            tagline='detailing studio', nav_label='Navigation', back='← Back to the site', other_href='../privacy.html', other_lang='bg', other_label='БГ', other_aria='Превключи на български', body=EN,
            path=os.path.join(NAIL, 'en', 'privacy.html')),
}
for k, c in CFG.items():
    html = PAGE
    for key, v in c.items():
        if key != 'path':
            html = html.replace('[[%s]]' % key, v)
    assert '[[' not in html
    os.makedirs(os.path.dirname(c['path']), exist_ok=True)
    open(c['path'], 'w', encoding='utf-8').write(html)
    print(k, c['path'])
