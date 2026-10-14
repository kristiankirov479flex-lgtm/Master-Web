/* Съдържание, което се добавя лесно: места наоколо и отзиви. */
window.VILA = {

  /* Начална точка за маршрутите (координати на вилата). */
  origin: "41.7110104,24.418726",

  /*
   * Места наоколо.
   *  id        – име на снимката: images/places/<id>.jpg (по желание)
   *  cat       – "nature" (природа) или "places" (села и градове)
   *  featured  – показва се веднага; останалите са зад „Покажи всички“
   *  km        – разстояние по пътя; без km се показва текстът в kmText
   *  dest      – къде да води бутонът „Маршрут от вилата“ (липсва = няма бутон)
   *  info      – външна страница за повече информация (всички са на английски)
   */
  places: [
    { id: "trigradsko-zhdrelo", cat: "nature", featured: true, km: 24,
      dest: "Триградско ждрело, България",
      info: "https://bulguides.com/trigrad-gorge-and-devils-throat-cave/",
      bg: { name: "Триградско ждрело", text: "Дълбок скален пролом, дълъг около 7 км, с отвесни стени до 300 м. Пътят през него е еднолентов и води към село Триград." },
      en: { name: "Trigrad Gorge", text: "A deep rock canyon about 7 km long, with sheer walls up to 300 m. The single-lane road through it leads to the village of Trigrad." } },

    { id: "dyavolskoto-garlo", cat: "nature", featured: true, km: 25,
      dest: "Дяволското гърло, Триград, България",
      info: "https://welcome.bg/en/listing/the-devils-throat-cave/",
      bg: { name: "Пещера Дяволското гърло", text: "Тук е най-високият подземен водопад на Балканите – 42 м. От паркинга тръгва и пътека към Харамийската пещера." },
      en: { name: "Devil's Throat Cave", text: "Home to the highest underground waterfall in the Balkans, at 42 m. A trail to the Haramiyska Cave also starts from the car park." } },

    { id: "yagodinska-peshtera", cat: "nature", featured: true, km: 22,
      dest: "Ягодинска пещера, България",
      info: "https://showcaves.com/english/bg/showcaves/Iagodinska.html",
      bg: { name: "Ягодинска пещера", text: "Седеметажна пещера с галерии близо 10 км, най-дългата в Родопите. Обиколките са с екскурзовод." },
      en: { name: "Yagodina Cave", text: "A seven-level cave with almost 10 km of galleries, the longest in the Rhodopes. Tours are with a guide." } },

    { id: "buynovsko-zhdrelo", cat: "nature", featured: true, km: 22,
      dest: "Буйновско ждрело, България",
      info: "https://www.showcaves.com/english/bg/gorges/Buynovsko.html",
      bg: { name: "Буйновско ждрело", text: "Едно от най-дългите ждрела в България и природен резерват от 1971 г. Минава се пеша или с кола по тесния път под скалите." },
      en: { name: "Buynovo Gorge", text: "One of the longest gorges in Bulgaria and a nature reserve since 1971. You can walk or drive the narrow road beneath the cliffs." } },

    { id: "shiroka-laka", cat: "places", featured: true, km: 21,
      dest: "Широка лъка, България",
      info: "https://en.wikipedia.org/wiki/Shiroka_Laka",
      bg: { name: "Широка лъка", text: "Архитектурен и фолклорен резерват с възрожденски къщи, подредени амфитеатрално по двата бряга на реката. Всяка първа неделя на март има маскарадния празник Песпонеделник." },
      en: { name: "Shiroka Laka", text: "An architectural and folklore reserve of Revival-period houses stacked like an amphitheatre along both banks of the river. The Pesponedelnik masquerade festival is held on the first Sunday of March." } },

    { id: "devin", cat: "places", featured: true, km: 5,
      dest: "Девин, България",
      info: "https://visitbulgaria.com/devin/",
      bg: { name: "Девин и минералните му извори", text: "Градът е балнеоложки център, известен с лековитите си минерални води. Добро място за релакс след преход." },
      en: { name: "Devin and its mineral springs", text: "The town is a spa centre known for its healing mineral waters. A good place to relax after a hike." } },

    { id: "samodivsko-praskalo", cat: "nature", featured: false, kmText: { bg: "с водач от Девин", en: "with a guide from Devin" },
      info: "https://bnr.bg/en/post/100119754/devins-eight-wonders",
      bg: { name: "Водопад Самодивско пръскало", text: "Висок 55 м – вторият по височина водопад в Родопите. Трудно достъпен, затова е най-добре да се ходи с местен водач." },
      en: { name: "Samodivsko Prskalo Waterfall", text: "At 55 m, the second-highest waterfall in the Rhodopes. It is hard to reach, so it is best to go with a local guide." } },

    { id: "yagodina", cat: "places", featured: false, km: 24,
      dest: "Ягодина, България",
      info: "https://bnr.bg/en/post/101158648/to-loose-oneself-in-yagodina",
      bg: { name: "Село Ягодина", text: "Автентично родопско село с традиционна кухня от местни продукти. В началото на септември се провежда селски събор." },
      en: { name: "Yagodina village", text: "An authentic Rhodope village with traditional cuisine made from local produce. A village fair is held in early September." } },

    { id: "trigrad", cat: "places", featured: false, km: 26,
      dest: "Триград, България",
      info: "https://welcome.bg/en/listing_location/devin/",
      bg: { name: "Село Триград", text: "Малко планинско село в края на ждрелото – изходна точка за Дяволското гърло и Харамийската пещера. Тихо място за обяд и разходка." },
      en: { name: "Trigrad village", text: "A small mountain village at the end of the gorge, the starting point for the Devil's Throat and the Haramiyska Cave. A quiet spot for lunch and a stroll." } },

    { id: "muzey-devin", cat: "places", featured: false, km: 5,
      dest: "Девин, България",
      info: "https://visitbulgaria.com/devin/",
      bg: { name: "Музеят в Девин", text: "Показва находки от разкопки в града и региона, инструменти и експонати за бита на родопчани. Подходящ за дъждовен ден." },
      en: { name: "Devin Museum", text: "Shows finds from excavations in the town and region, plus tools and exhibits about everyday Rhodope life. Good for a rainy day." } }
  ],

  /* Обобщение от Google Карти – обновявайте тези два реда, когато се променят. */
  rating: { score: 5.0, count: 17 },

  /*
   * Отзиви от Google Карти.
   * Текстовете са дословни. За да добавите отзив, копирайте блок и сменете текста.
   *  featured – показва се в цяла ширина
   *  bg/en    – оригиналът е на български; английският е превод
   */
  reviews: [
    { featured: true,
      name: { bg: "Гост", en: "Guest" },
      bg: "Мястото е високо над селото, с красива открита гледка към планините и към селото в краката ни. На няколко минути пеша има магазини, ресторант и добра пекарна. Стаята беше просторна и чиста, с балкон, собствена баня и тоалетна, голямо удобно легло, фотьойл, маса и столове. На етажа има и дневна с още един балкон. Долу в двора има напълно оборудвана кухня, в която си приготвихме вкусни ястия. Селото е зелено и красиво, с много възможности за разходки в гората. Горещо препоръчваме!",
      en: "The place is high above the village, with a beautiful open view of the mountains and the village at our feet. There are shops, a restaurant and a good bakery a few minutes' walk away. The room was spacious and clean, with a balcony, its own bathroom and toilet, a big comfortable bed, an armchair, a table and chairs. The floor also has a living room with another balcony. Downstairs in the yard there is a fully equipped kitchen where we cooked delicious meals. The village is green and beautiful, with lots of opportunities for walks in the forest. We highly recommend it!" },

    { name: { bg: "Емил Н.", en: "Emil N." },
      bg: "Това е едно невероятно красиво и уютно място с изключително топли и мили домакини. За мен това е любимо място и го препоръчвам от цялото си сърце.",
      en: "This is an incredibly beautiful and cozy place with exceptionally warm and kind hosts. For me it is a favorite place and I recommend it with all my heart." },

    { name: { bg: "Стела М.", en: "Stela M." },
      bg: "Уютно и спокойно място! Домакина е истински гостоприемен Човек! Природата е уникална!",
      en: "A cozy and peaceful place! The host is a truly hospitable person! The nature is unique!" }
  ]
};
