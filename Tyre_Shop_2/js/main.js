/* Stoyanov Tyres (tyre shop design 2, a family workshop): page behaviour.
   Colour schemes, menu, today's hours, the "ask for a price" form (car, size, season, class, a day and a free time, details) and the map.
   The request talks to StoyanovAPI (js/api.js): a mock server now, a real backend later (docs/API.md). */
(function () {
  "use strict";

  var CFG = window.STOYANOV_CONFIG || {};
  var API = window.StoyanovAPI;
  var html = document.documentElement;
  var lang = html.lang === "bg" ? "bg" : "en";
  var reduceMotion = window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches;
  function $(id) { return document.getElementById(id); }
  var D = JSON.parse($("stoyData").textContent);

  var T = {
    bg: {
      locale: "bg-BG", mapTitle: "Карта на сервиза", pick: "Избери час", otherMake: "Друга марка",
      slotsHint: "Свободни часове: {n}.", noSlots: "Няма свободни часове този ден. Избери друг ден.", availError: "Не успяхме да проверим часовете. Опитай пак.", checking: "Проверяваме свободните часове…", chooseDate: "Избери дата, за да видиш свободните часове.",
      errMake: "Избери марка на автомобила.", errTime: "Избери дата и час.", errName: "Въведи име и телефон.", errTaken: "Съжаляваме, този час току-що беше зает. Избери друг.", errInvalid: "Провери данните и опитай пак.", errGeneric: "Нещо се обърка. Опитай пак или ни се обади.",
      sending: "Изпращане…", demoLine: "Демо режим: заявките се пазят само в този браузър и нищо не се изпраща.",
      doneH: "Заявката е приета", doneRef: "Номер", statusPending: "Чака оферта", doneNext: "Ще ти се обадим с цена и ще потвърдим часа. Запази номера.",
      doneDemo: "Демо режим: нищо не беше изпратено. Заявката е записана само в този браузър.", adminLink: "Виж я в демо админ панела", again: "Нова заявка",
      lines: { when: "Кога", car: "Автомобил", size: "Размер", what: "Търси", name: "Име" }, svc: "Оферта за гуми", unknown: "не е посочен"
    },
    en: {
      locale: "en-GB", mapTitle: "Map of the workshop", pick: "Choose a time", otherMake: "Other make",
      slotsHint: "{n} free times.", noSlots: "No free times on this day. Please pick another day.", availError: "We could not check the times. Please try again.", checking: "Checking free times…", chooseDate: "Choose a date to see the free times.",
      errMake: "Please choose your car make.", errTime: "Please pick a date and a time.", errName: "Please enter your name and phone.", errTaken: "Sorry, that time was just taken. Please choose another.", errInvalid: "Please check your details and try again.", errGeneric: "Something went wrong. Please try again or call us.",
      sending: "Sending…", demoLine: "Demo mode: requests are kept in this browser only and nothing is sent.",
      doneH: "Request received", doneRef: "Reference", statusPending: "Waiting for an offer", doneNext: "We will call you with a price and confirm the time. Keep your reference.",
      doneDemo: "Demo mode: nothing was sent. The request is saved only in this browser.", adminLink: "See it in the demo back office", again: "New request",
      lines: { when: "When", car: "Car", size: "Size", what: "Looking for", name: "Name" }, svc: "Tyre quote", unknown: "not given"
    }
  }[lang];

  /* ---------- Helpers ---------- */
  function pad(n) { return (n < 10 ? "0" : "") + n; }
  function ymd(d) { return d.getFullYear() + "-" + pad(d.getMonth() + 1) + "-" + pad(d.getDate()); }
  function toDate(v) { var p = v.split("-"); return new Date(+p[0], +p[1] - 1, +p[2]); }
  function addDays(d, n) { return new Date(d.getFullYear(), d.getMonth(), d.getDate() + n); }
  function el(tag, cls, text) { var n = document.createElement(tag); if (cls) n.className = cls; if (text !== undefined) n.textContent = text; return n; }
  function fill(s, o) { return s.replace(/\{(\w+)\}/g, function (m, k) { return o[k] !== undefined ? o[k] : m; }); }
  function longDate(v) { return toDate(v).toLocaleDateString(T.locale, { weekday: "long", day: "numeric", month: "long" }); }
  function scrollToEl(n) { n.scrollIntoView({ behavior: reduceMotion ? "auto" : "smooth", block: "start" }); }

  /* ---------- Colour scheme (skin) ---------- */
  var SKINS = ["blue", "red", "green", "graphite", "amber"];
  var skinBtns = document.querySelectorAll(".sw[data-skin]");
  var skinName = $("skinName");
  var animTimer;
  function setSkin(skin, save) {
    if (SKINS.indexOf(skin) === -1) skin = "blue";
    if (save && !reduceMotion) { html.classList.add("skin-anim"); clearTimeout(animTimer); animTimer = setTimeout(function () { html.classList.remove("skin-anim"); }, 400); }
    html.dataset.skin = skin;
    skinBtns.forEach(function (b) {
      var on = b.dataset.skin === skin;
      b.setAttribute("aria-pressed", on ? "true" : "false");
      if (on && skinName) skinName.textContent = b.getAttribute("aria-label");
    });
    var meta = document.querySelector('meta[name="theme-color"]');
    if (meta) meta.content = getComputedStyle(html).getPropertyValue("--bg").trim() || meta.content;
    if (save) { try { localStorage.setItem("stoyanovSkin", skin); } catch (e) {} }
  }
  skinBtns.forEach(function (b) { b.addEventListener("click", function () { setSkin(b.dataset.skin, true); }); });
  setSkin(html.dataset.skin, false);

  /* ---------- Menu (mobile) ---------- */
  var burger = $("burger"), nav = $("nav");
  function setMenu(open) { nav.classList.toggle("open", open); burger.setAttribute("aria-expanded", open ? "true" : "false"); }
  burger.addEventListener("click", function () { setMenu(!nav.classList.contains("open")); });
  nav.addEventListener("click", function (e) { if (e.target.closest("a")) setMenu(false); });
  document.addEventListener("keydown", function (e) { if (e.key === "Escape" && nav.classList.contains("open")) { setMenu(false); burger.focus(); } });

  /* ---------- Today's hours ---------- */
  function hoursFor(d) { var g = d.getDay(); return g === 0 || g === 6 ? CFG.hours.weekend : CFG.hours.weekday; }
  (function () {
    var now = new Date(), g = now.getDay(), key = g === 0 || g === 6 ? "we" : "wd", h = hoursFor(now);
    document.querySelectorAll("#hours [data-hrs]").forEach(function (r) { r.classList.toggle("today", r.dataset.hrs === key); });
    $("todayHours").textContent = h[0] + " – " + h[1];
  })();

  /* ---------- Request form ---------- */
  var form = $("quoteForm"), dateIn = $("f-date"), timeSel = $("f-time"), hint = $("timeHint");
  dateIn.min = ymd(new Date()); dateIn.max = ymd(addDays(new Date(), 60));
  function setTimes(r) {
    timeSel.textContent = "";
    if (!r.slots.length) { hint.textContent = T.noSlots; return; }
    timeSel.appendChild(new Option(T.pick, ""));
    r.slots.forEach(function (s) { timeSel.appendChild(new Option(s, s)); });
    hint.textContent = fill(T.slotsHint, { n: r.slots.length });
  }
  function loadTimes() {
    var v = dateIn.value;
    if (!v) { hint.textContent = T.chooseDate; timeSel.textContent = ""; return Promise.resolve(); }
    hint.textContent = T.checking;
    return API.availability(v, D.visit).then(function (r) { if (dateIn.value === v) setTimes(r); }).catch(function () { hint.textContent = T.availError; });
  }
  dateIn.addEventListener("change", loadTimes);
  (function find(i) {
    if (i > 7) return;
    var d = ymd(addDays(new Date(), i));
    API.availability(d, D.visit).then(function (r) { if (r.slots.length) { dateIn.value = d; setTimes(r); } else find(i + 1); }).catch(function () {});
  })(0);

  var errBox = $("qError"), sendBtn = $("qSend"), doneBox = $("qDone");
  function showError(msg) { errBox.textContent = msg; errBox.hidden = false; }
  if (API.mode === "demo") { var dn = $("demoNote"); dn.textContent = T.demoLine; dn.hidden = false; }
  function checked(name) { var c = form.querySelector('input[name="' + name + '"]:checked'); return c ? c.value : "unsure"; }
  function carText() {
    var mk = form.elements.make.value, model = form.elements.model.value.trim();
    return ((mk === "other" ? T.otherMake : mk) + (model ? " " + model : "")).trim();
  }
  form.addEventListener("submit", function (e) {
    e.preventDefault(); errBox.hidden = true;
    if (!form.elements.make.value) { form.elements.make.focus(); return showError(T.errMake); }
    if (!dateIn.value || !timeSel.value) return showError(T.errTime);
    var name = form.elements.name.value.trim(), phone = form.elements.phone.value.trim();
    if (!name || phone.replace(/\D/g, "").length < 6) return showError(T.errName);
    var size = form.elements.size.value.trim(), season = checked("season"), budget = checked("budget");
    var summary = carText() + " · " + (size || T.unknown) + " · " + D.seasons[season] + " · " + D.budgets[budget];
    var payload = {
      name: name, phone: phone, service: T.svc, date: dateIn.value, time: timeSel.value, durationMinutes: D.visit, fulfil: "pickup", lang: lang,
      message: form.elements.msg.value.trim(),
      plan: { summary: summary, car: { make: form.elements.make.value, model: form.elements.model.value.trim() }, size: size, season: season, budget: budget }
    };
    sendBtn.disabled = true; sendBtn.classList.add("is-busy"); var label = sendBtn.textContent; sendBtn.textContent = T.sending;
    API.createRequest(payload).then(function (res) { showDone(res, payload); })
      .catch(function (err) {
        if (err && err.code === "slot_taken") { showError(T.errTaken); loadTimes(); }
        else if (err && err.code === "invalid") showError(T.errInvalid); else showError(T.errGeneric);
      })
      .then(function () { sendBtn.disabled = false; sendBtn.classList.remove("is-busy"); sendBtn.textContent = label; });
  });
  function showDone(res, p) {
    form.hidden = true; doneBox.hidden = false; doneBox.textContent = "";
    doneBox.appendChild(el("h3", "", T.doneH));
    var ref = el("p", "done-ref"); ref.appendChild(el("span", "", T.doneRef)); ref.appendChild(el("strong", "", res.id)); doneBox.appendChild(ref);
    var ps = el("p", "done-status"); ps.appendChild(el("span", "pill", T.statusPending)); doneBox.appendChild(ps);
    var dl = el("dl", "done-list");
    [[T.lines.when, longDate(p.date) + ", " + p.time], [T.lines.car, carText()], [T.lines.size, p.plan.size || T.unknown], [T.lines.what, D.seasons[p.plan.season] + ", " + D.budgets[p.plan.budget]], [T.lines.name, p.name]]
      .forEach(function (r) { dl.appendChild(el("dt", "", r[0])); dl.appendChild(el("dd", "", r[1])); });
    doneBox.appendChild(dl);
    doneBox.appendChild(el("p", "", T.doneNext));
    if (API.mode === "demo") doneBox.appendChild(el("p", "demo-note", T.doneDemo));
    var act = el("div", "done-actions");
    if (API.mode === "demo") { var a = el("a", "btn btn-line", T.adminLink); a.href = (lang === "bg" ? "" : "../") + "admin.html" + (lang === "en" ? "?lang=en" : ""); act.appendChild(a); }
    var again = el("button", "btn btn-main", T.again); again.type = "button";
    again.addEventListener("click", function () { form.reset(); form.hidden = false; doneBox.hidden = true; loadTimes(); scrollToEl($("quote")); });
    act.appendChild(again); doneBox.appendChild(act);
    doneBox.focus(); scrollToEl(doneBox);
  }

  /* ---------- Map (loads only after a click, see the privacy page) ---------- */
  var mapBox = $("mapBox");
  $("mapLoad").addEventListener("click", function () {
    var f = document.createElement("iframe");
    f.src = mapBox.dataset.src; f.title = T.mapTitle; f.loading = "lazy"; f.referrerPolicy = "no-referrer";
    mapBox.textContent = ""; mapBox.appendChild(f);
  });
  $("year").textContent = new Date().getFullYear();
})();
