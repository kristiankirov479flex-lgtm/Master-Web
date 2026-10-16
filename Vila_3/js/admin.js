/* Demo back office for The Stone Cellar. It shows the enquiries kept by the mock server (CellarAPI).
   Demo only: no login, and the data lives in this browser. A real one needs a login and a database (docs/API.md). */
(function () {
  "use strict";
  var API = window.CellarAPI;
  var lang = "bg";
  try { lang = new URLSearchParams(location.search).get("lang") === "en" ? "en" : "bg"; } catch (e) {}
  document.documentElement.lang = lang;
  function $(id) { return document.getElementById(id); }

  var T = {
    bg: {
      title: "Демо админ панел – Каменната изба", h1: "Демо админ панел", skip: "Към съдържанието", back: "← Към сайта", backHref: "index.html",
      other: "EN", otherLang: "en", otherAria: "Switch to English", otherHref: "admin.html?lang=en",
      note: "Това е демонстрация. Запитванията се пазят само в този браузър. В истинска система тази страница ще е защитена с парола и ще чете данните от база данни. Отказано запитване освобождава стаята за тези дати.",
      filters: { all: "Всички", pending: "Чакат", confirmed: "Потвърдени", declined: "Отказани" },
      cols: { ref: "Запитване", stay: "Престой", guest: "Гост", room: "Стая", total: "Общо", status: "Статус", act: "Действие" },
      statuses: { pending: "Чака потвърждение", confirmed: "Потвърдено", declined: "Отказано" },
      del: "Изтрий", seed: "Добави примерни запитвания", reset: "Изтрий всички демо данни", resetSure: "Натисни отново, за да изтриеш всичко",
      empty: "Още няма запитвания. Изпрати едно от сайта или добави примерни.", received: "Получено",
      saved: "Статусът е променен.", deleted: "Запитването е изтрито.", seeded: "Добавени са примерни запитвания.", cleared: "Демо данните са изтрити.",
      filterLabel: "Филтър по статус", locale: "bg-BG", nights: ["нощ", "нощувки"], guests: ["гост", "гости"], live: "Тази страница работи само в демо режим.",
      rooms: { stone: "Каменната стая", cellar: "Стаята в избата", hearth: "Сюит „Камината“", cottage: "Къщичката сред лозята" }, names: ["Ана Петрова", "Георги Иванов", "Семейство Димитрови"]
    },
    en: {
      title: "Demo back office – The Stone Cellar", h1: "Demo back office", skip: "Skip to content", back: "← Back to the site", backHref: "en/index.html",
      other: "БГ", otherLang: "bg", otherAria: "Превключи на български", otherHref: "admin.html",
      note: "This is a demonstration. Enquiries are kept in this browser only. In a real system this page would be protected by a password and read from a database. Declining an enquiry frees the room for those dates.",
      filters: { all: "All", pending: "Waiting", confirmed: "Confirmed", declined: "Declined" },
      cols: { ref: "Enquiry", stay: "Stay", guest: "Guest", room: "Room", total: "Total", status: "Status", act: "Action" },
      statuses: { pending: "Waiting for confirmation", confirmed: "Confirmed", declined: "Declined" },
      del: "Delete", seed: "Add sample enquiries", reset: "Delete all demo data", resetSure: "Click again to delete everything",
      empty: "No enquiries yet. Send one from the site, or add samples.", received: "Received",
      saved: "Status changed.", deleted: "Enquiry deleted.", seeded: "Sample enquiries added.", cleared: "Demo data deleted.",
      filterLabel: "Filter by status", locale: "en-GB", nights: ["night", "nights"], guests: ["guest", "guests"], live: "This page works in demo mode only.",
      rooms: { stone: "The Stone Room", cellar: "The Cellar Room", hearth: "The Hearth Suite", cottage: "The Vineyard Cottage" }, names: ["Ana Petrova", "Georgi Ivanov", "The Dimitrov family"]
    }
  }[lang];

  document.title = T.title; $("h1").textContent = T.h1; $("skip").textContent = T.skip; $("note").textContent = T.note;
  $("backLink").textContent = T.back; $("backLink").href = T.backHref; $("footBack").textContent = T.back; $("footBack").href = T.backHref;
  var ll = $("langLink"); ll.textContent = T.other; ll.lang = T.otherLang; ll.hreflang = T.otherLang; ll.href = T.otherHref; ll.setAttribute("aria-label", T.otherAria);
  var brand = lang === "bg" ? "Каменната изба" : "The Stone Cellar"; document.querySelector("#logo b").textContent = brand; document.querySelector(".foot span span").nextSibling.textContent = " " + brand;
  $("seedBtn").textContent = T.seed; $("resetBtn").textContent = T.reset;
  $("filters").setAttribute("aria-label", T.filterLabel);

  var filter = "all", list = [], armed = false;
  function el(tag, cls, text) { var n = document.createElement(tag); if (cls) n.className = cls; if (text !== undefined) n.textContent = text; return n; }
  function pad(n) { return (n < 10 ? "0" : "") + n; }
  function ymd(d) { return d.getFullYear() + "-" + pad(d.getMonth() + 1) + "-" + pad(d.getDate()); }
  function dayText(v) { var p = v.split("-"); return new Date(+p[0], +p[1] - 1, +p[2]).toLocaleDateString(T.locale, { weekday: "short", day: "numeric", month: "short" }); }
  function say(msg) { var l = $("live"); l.textContent = ""; setTimeout(function () { l.textContent = msg; }, 30); }

  function renderFilters() {
    var box = $("filters"); box.textContent = "";
    ["all", "pending", "confirmed", "declined"].forEach(function (k) {
      var n = k === "all" ? list.length : list.filter(function (r) { return r.status === k; }).length;
      var b = el("button", "chip", T.filters[k] + " (" + n + ")"); b.type = "button"; b.setAttribute("aria-pressed", filter === k ? "true" : "false");
      b.addEventListener("click", function () { filter = k; render(); });
      box.appendChild(b);
    });
  }
  function render() {
    renderFilters();
    var out = $("out"), rows = list.filter(function (r) { return filter === "all" || r.status === filter; });
    out.textContent = "";
    if (!rows.length) { out.appendChild(el("p", "adm-empty", T.empty)); return; }
    var tb = el("table", "adm-t"), th = el("thead"), tr = el("tr");
    ["ref", "stay", "guest", "room", "total", "status", "act"].forEach(function (k) { var c = el("th", "", T.cols[k]); c.scope = "col"; tr.appendChild(c); });
    th.appendChild(tr); tb.appendChild(th);
    var body = el("tbody");
    rows.forEach(function (r) {
      var row = el("tr");
      function cell(k) { var c = el("td"); c.dataset.label = T.cols[k]; row.appendChild(c); return c; }
      var c1 = cell("ref"); c1.appendChild(el("span", "adm-ref", r.id)); c1.appendChild(el("span", "adm-sub", T.received + " " + new Date(r.createdAt).toLocaleString(T.locale, { day: "numeric", month: "short", hour: "2-digit", minute: "2-digit" })));
      var c2 = cell("stay"); c2.appendChild(el("b", "", dayText(r.checkin) + " → " + dayText(r.checkout))); c2.appendChild(el("span", "adm-sub", r.nights + " " + (r.nights === 1 ? T.nights[0] : T.nights[1]) + " · " + r.guests + " " + (r.guests === 1 ? T.guests[0] : T.guests[1])));
      var c3 = cell("guest"); c3.appendChild(el("b", "", r.name)); c3.appendChild(el("span", "adm-sub", r.phone)); if (r.email) c3.appendChild(el("span", "adm-sub", r.email));
      if (r.message) c3.appendChild(el("span", "adm-sub", "“" + r.message + "”"));
      cell("room").appendChild(document.createTextNode(T.rooms[r.room] || r.room));
      cell("total").appendChild(document.createTextNode(r.total + " €"));
      var c6 = cell("status"), sel = el("select"); sel.setAttribute("aria-label", T.cols.status + " " + r.id); sel.dataset.status = r.status;
      ["pending", "confirmed", "declined"].forEach(function (s) { var o = el("option", "", T.statuses[s]); o.value = s; if (s === r.status) o.selected = true; sel.appendChild(o); });
      sel.addEventListener("change", function () { API.setStatus(r.id, sel.value).then(function () { say(T.saved); refresh(); }); });
      c6.appendChild(sel);
      var c7 = cell("act"), del = el("button", "adm-del", T.del); del.type = "button";
      del.addEventListener("click", function () { API.removeEnquiry(r.id).then(function () { say(T.deleted); refresh(); }); });
      c7.appendChild(del);
      body.appendChild(row);
    });
    tb.appendChild(body); out.appendChild(tb);
  }
  function refresh() { return API.listEnquiries().then(function (l) { list = l; render(); }); }

  $("seedBtn").addEventListener("click", function () {
    var d = new Date(), a = new Date(d.getFullYear(), d.getMonth(), d.getDate() + 9), b = new Date(a.getTime() + 2 * 864e5), c = new Date(a.getTime() + 21 * 864e5);
    API.seedDemo([
      { name: T.names[0], phone: "+359 888 000 001", email: "maria@example.com", room: "stone", checkin: ymd(a), checkout: ymd(b), guests: 2, status: "pending" },
      { name: T.names[1], phone: "+359 888 000 002", room: "cellar", checkin: ymd(a), checkout: ymd(new Date(a.getTime() + 3 * 864e5)), guests: 2, status: "confirmed" },
      { name: T.names[2], phone: "+359 888 000 003", room: "hearth", checkin: ymd(c), checkout: ymd(new Date(c.getTime() + 4 * 864e5)), guests: 4, status: "pending" }
    ]).then(function () { say(T.seeded); refresh(); }, function () { say(T.live); });
  });
  $("resetBtn").addEventListener("click", function () {
    var b = $("resetBtn");
    if (!armed) { armed = true; b.textContent = T.resetSure; setTimeout(function () { armed = false; b.textContent = T.reset; }, 4000); return; }
    armed = false; b.textContent = T.reset;
    API.resetDemo().then(function () { say(T.cleared); refresh(); }, function () { say(T.live); });
  });
  refresh();
})();
