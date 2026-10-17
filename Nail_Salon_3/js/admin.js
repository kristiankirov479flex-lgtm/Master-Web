/* Demo back office: shows the requests kept by the mock server (js/api.js). A real system would sit behind a login. */
(function () {
  "use strict";

  var API = window.AtelierAPI;
  var $ = function (id) { return document.getElementById(id); };
  var lang = "bg";
  try { lang = new URLSearchParams(location.search).get("lang") === "en" ? "en" : "bg"; } catch (e) {}
  document.documentElement.lang = lang;

  var T = {
    bg: {
      title: "Демо админ панел – Atelier Nude", h1: "Демо админ панел", tagline: "студио за нокти", skip: "Към съдържанието",
      back: "← Към сайта", backHref: "index.html", other: "EN", otherLang: "en", otherAria: "Switch to English", otherHref: "admin.html?lang=en",
      note: "Това е демонстрация. Заявките се пазят само в този браузър. В истинска система тази страница ще е защитена с парола и ще чете данните от база данни. Отказана заявка освобождава часа.",
      filters: { all: "Всички", pending: "Чакат", confirmed: "Потвърдени", declined: "Отказани" },
      cols: { ref: "Заявка", when: "Кога", client: "Клиент", what: "Услуга", status: "Статус", act: "Действие" },
      statuses: { pending: "Чака потвърждение", confirmed: "Потвърдена", declined: "Отказана" },
      del: "Изтрий", seed: "Добави примерни заявки", reset: "Изтрий всички демо данни", resetSure: "Натисни отново, за да изтриеш всичко",
      empty: "Още няма заявки. Изпрати една от сайта или добави примерни.", received: "Получена",
      saved: "Статусът е променен.", deleted: "Заявката е изтрита.", seeded: "Добавени са примерни заявки.", cleared: "Демо данните са изтрити.",
      filterLabel: "Филтър по статус", locale: "bg-BG", hUnit: "ч", mUnit: "мин", live: "Тази страница работи само в демо режим.",
      sampleSvc: ["Маникюр с гел лак", "Изграждане с гел, средни нокти", "Педикюр с гел лак"],
      sampleNames: ["Мария Иванова", "Елена Петрова", "Ивана Георгиева"]
    },
    en: {
      title: "Demo back office – Atelier Nude", h1: "Demo back office", tagline: "nail studio", skip: "Skip to content",
      back: "← Back to the site", backHref: "en/index.html", other: "БГ", otherLang: "bg", otherAria: "Превключи на български", otherHref: "admin.html",
      note: "This is a demonstration. Requests are kept in this browser only. In a real system this page would be protected by a password and read from a database. Declining a request frees the time.",
      filters: { all: "All", pending: "Waiting", confirmed: "Confirmed", declined: "Declined" },
      cols: { ref: "Request", when: "When", client: "Client", what: "Service", status: "Status", act: "Action" },
      statuses: { pending: "Waiting for confirmation", confirmed: "Confirmed", declined: "Declined" },
      del: "Delete", seed: "Add sample requests", reset: "Delete all demo data", resetSure: "Click again to delete everything",
      empty: "No requests yet. Send one from the site, or add samples.", received: "Received",
      saved: "Status changed.", deleted: "Request deleted.", seeded: "Sample requests added.", cleared: "Demo data deleted.",
      filterLabel: "Filter by status", locale: "en-GB", hUnit: "h", mUnit: "min", live: "This page works in demo mode only.",
      sampleSvc: ["Gel polish manicure", "Gel extensions, medium", "Gel polish pedicure"],
      sampleNames: ["Maria Ivanova", "Elena Petrova", "Ivana Georgieva"]
    }
  }[lang];

  document.title = T.title;
  $("h1").textContent = T.h1;
  $("tagline").textContent = T.tagline;
  $("skip").textContent = T.skip;
  $("backLink").textContent = T.back; $("backLink").href = T.backHref;
  $("footBack").textContent = T.back; $("footBack").href = T.backHref;
  var ll = $("langLink");
  ll.textContent = T.other; ll.lang = T.otherLang; ll.hreflang = T.otherLang; ll.href = T.otherHref; ll.setAttribute("aria-label", T.otherAria);
  $("note").textContent = T.note;
  $("seedBtn").textContent = T.seed;
  $("resetBtn").textContent = T.reset;
  $("year").textContent = new Date().getFullYear();
  $("filters").setAttribute("aria-label", T.filterLabel);

  function pad(n) { return (n < 10 ? "0" : "") + n; }
  function iso(d) { return d.getFullYear() + "-" + pad(d.getMonth() + 1) + "-" + pad(d.getDate()); }
  function toDate(v) { var p = v.split("-"); return new Date(+p[0], +p[1] - 1, +p[2]); }
  function fmtMin(m) { var h = Math.floor(m / 60), r = m % 60, o = []; if (h) o.push(h + " " + T.hUnit); if (r) o.push(r + " " + T.mUnit); return o.join(" "); }
  function el(tag, cls, text) { var n = document.createElement(tag); if (cls) n.className = cls; if (text !== undefined) n.textContent = text; return n; }
  function say(msg) { var s = $("status"); s.textContent = ""; setTimeout(function () { s.textContent = msg; }, 30); }

  var all = [], filter = "all";

  function renderFilters() {
    var box = $("filters");
    box.textContent = "";
    ["all", "pending", "confirmed", "declined"].forEach(function (k) {
      var n = k === "all" ? all.length : all.filter(function (r) { return r.status === k; }).length;
      var b = el("button", "chip", T.filters[k] + " (" + n + ")");
      b.type = "button";
      b.setAttribute("aria-pressed", k === filter ? "true" : "false");
      b.addEventListener("click", function () { filter = k; render(); });
      box.appendChild(b);
    });
  }

  function render() {
    renderFilters();
    var list = $("list");
    list.textContent = "";
    var rows = all.filter(function (r) { return filter === "all" || r.status === filter; });
    if (!rows.length) { list.appendChild(el("p", "adm-empty", T.empty)); return; }

    var table = el("table", "adm-t");
    var thead = el("thead"), hr = el("tr");
    ["ref", "when", "client", "what", "status", "act"].forEach(function (k) { var th = el("th", "", T.cols[k]); th.scope = "col"; hr.appendChild(th); });
    thead.appendChild(hr); table.appendChild(thead);
    var tbody = el("tbody");
    rows.forEach(function (r) {
      var tr = el("tr");
      function cell(key) { var td = el("td"); td.dataset.label = T.cols[key]; tr.appendChild(td); return td; }

      var c1 = cell("ref");
      c1.appendChild(el("span", "adm-ref", r.id));
      c1.appendChild(el("span", "adm-sub", T.received + " " + new Date(r.createdAt).toLocaleString(T.locale, { day: "numeric", month: "short", hour: "2-digit", minute: "2-digit" })));

      var c2 = cell("when");
      c2.appendChild(el("strong", "", toDate(r.date).toLocaleDateString(T.locale, { weekday: "short", day: "numeric", month: "short" }) + ", " + r.time));
      c2.appendChild(el("span", "adm-sub", fmtMin(r.duration)));

      var c3 = cell("client");
      c3.appendChild(el("strong", "", r.name));
      var tel = el("a", "adm-sub", r.phone); tel.href = "tel:" + r.phone.replace(/[^\d+]/g, ""); c3.appendChild(tel);

      var c4 = cell("what");
      c4.appendChild(el("span", "", r.service));
      if (r.plan && r.plan.summary) c4.appendChild(el("span", "adm-sub", r.plan.summary));
      if (r.look && r.look.alt) c4.appendChild(el("span", "adm-sub", "📷 " + r.look.alt));
      if (r.message) c4.appendChild(el("span", "adm-sub", "“" + r.message + "”"));

      var c5 = cell("status");
      var sel = el("select"); sel.dataset.status = r.status;
      sel.setAttribute("aria-label", T.cols.status + " " + r.id);
      ["pending", "confirmed", "declined"].forEach(function (k) { var o = el("option", "", T.statuses[k]); o.value = k; if (k === r.status) o.selected = true; sel.appendChild(o); });
      sel.addEventListener("change", function () {
        API.setStatus(r.id, sel.value).then(function () { say(T.saved); return reload(); });
      });
      c5.appendChild(sel);

      var c6 = cell("act");
      var del = el("button", "adm-del", T.del); del.type = "button";
      del.setAttribute("aria-label", T.del + " " + r.id);
      del.addEventListener("click", function () { API.removeRequest(r.id).then(function () { say(T.deleted); return reload(); }); });
      c6.appendChild(del);
      tbody.appendChild(tr);
    });
    table.appendChild(tbody);
    list.appendChild(table);
  }

  function reload() {
    return API.listRequests().then(function (rows) { all = rows; render(); });
  }

  /* sample data for showing the screen to a customer */
  function nextDay(from, weekend) {
    var d = new Date(); d.setHours(0, 0, 0, 0);
    for (var i = from; i < from + 14; i++) {
      var x = new Date(d.getFullYear(), d.getMonth(), d.getDate() + i), g = x.getDay(), isWe = g === 0 || g === 6;
      if (isWe === weekend) return iso(x);
    }
  }
  $("seedBtn").addEventListener("click", function () {
    API.seedDemo([
      { name: T.sampleNames[0], phone: "+359 888 000 001", service: T.sampleSvc[0], date: nextDay(1, false), time: "10:00", duration: 90, status: "pending", message: "" },
      { name: T.sampleNames[1], phone: "+359 888 000 002", service: T.sampleSvc[1], date: nextDay(2, false), time: "13:30", duration: 105, status: "confirmed", message: "" },
      { name: T.sampleNames[2], phone: "+359 888 000 003", service: T.sampleSvc[2], date: nextDay(1, true), time: "11:00", duration: 90, status: "pending", message: "" }
    ]).then(function () { say(T.seeded); return reload(); });
  });

  var resetTimer, armed = false;
  $("resetBtn").addEventListener("click", function () {
    var b = $("resetBtn");
    if (!armed) {
      armed = true; b.textContent = T.resetSure;
      clearTimeout(resetTimer);
      resetTimer = setTimeout(function () { armed = false; b.textContent = T.reset; }, 4000);
      return;
    }
    armed = false; clearTimeout(resetTimer); b.textContent = T.reset;
    API.resetDemo().then(function () { say(T.cleared); return reload(); });
  });

  if (API.mode !== "demo") {
    $("seedBtn").hidden = true; $("resetBtn").hidden = true;
  }
  reload();
})();
