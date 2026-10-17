/* Lozeta (restaurant design 3, a restaurant for events): page behaviour.
   Colour schemes, menu, the event request (occasion, guests, hall, date, a free start time, menu, a simple estimate, details) and the map.
   The request talks to LozetaAPI (js/api.js): a mock server now, a real backend later (docs/API.md). */
(function () {
  "use strict";

  var CFG = window.LOZETA_CONFIG || {};
  var API = window.LozetaAPI;
  var html = document.documentElement;
  var lang = html.lang === "bg" ? "bg" : "en";
  var reduceMotion = window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches;
  function $(id) { return document.getElementById(id); }
  var D = JSON.parse($("lozetaData").textContent);

  var T = {
    bg: {
      locale: "bg-BG", mapTitle: "Карта на ресторанта", pick: "Избери час", guests: "{n} гости",
      est: "Ориентировъчно: <b>{t}</b> ({n} гости × {p}){fee}", estFee: " + такса за залата {f}", estNone: "Избери меню, за да видиш ориентировъчна цена.", estGuests: "Въведи от {min} до {max} гости.",
      slotsHint: "Свободни начални часове: {n}.", noSlots: "Няма свободна зала този ден. Избери друга дата.", availError: "Не успяхме да проверим датите. Опитай пак.", checking: "Избери дата, за да видиш свободните часове.", checkingNow: "Проверяваме…",
      errGuests: "Въведи от {min} до {max} гости.", errTime: "Избери дата и начален час.", errName: "Въведи име и телефон.", errTaken: "Съжаляваме, тази дата току-що беше заета. Избери друга.", errInvalid: "Провери данните и опитай пак.", errGeneric: "Нещо се обърка. Опитай пак или ни се обади.",
      sending: "Изпращане…", demoLine: "Демо режим: заявките се пазят само в този браузър и нищо не се изпраща.",
      doneH: "Заявката е приета", doneRef: "Номер", statusPending: "Чака оферта", doneNext: "Ще ти се обадим до един работен ден с оферта. Запази номера.",
      doneDemo: "Демо режим: нищо не беше изпратено. Заявката е записана само в този браузър.", adminLink: "Виж я в демо админ панела", again: "Нова заявка",
      lines: { when: "Кога", what: "Събитие", est: "Ориентировъчно", name: "Име" }, notSure: "меню: още не знаем", hallAny: "зала по избор"
    },
    en: {
      locale: "en-GB", mapTitle: "Map of the restaurant", pick: "Choose a time", guests: "{n} guests",
      est: "Estimate: <b>{t}</b> ({n} guests × {p}){fee}", estFee: " + hall fee {f}", estNone: "Choose a menu to see an estimate.", estGuests: "Enter {min} to {max} guests.",
      slotsHint: "{n} free start times.", noSlots: "No free hall on this day. Please pick another date.", availError: "We could not check the dates. Please try again.", checking: "Choose a date to see the free start times.", checkingNow: "Checking…",
      errGuests: "Please enter {min} to {max} guests.", errTime: "Please pick a date and a start time.", errName: "Please enter your name and phone.", errTaken: "Sorry, that date was just taken. Please choose another.", errInvalid: "Please check your details and try again.", errGeneric: "Something went wrong. Please try again or call us.",
      sending: "Sending…", demoLine: "Demo mode: requests are kept in this browser only and nothing is sent.",
      doneH: "Request received", doneRef: "Reference", statusPending: "Waiting for an offer", doneNext: "We will call you within one working day with an offer. Keep your reference.",
      doneDemo: "Demo mode: nothing was sent. The request is saved only in this browser.", adminLink: "See it in the demo back office", again: "New request",
      lines: { when: "When", what: "Event", est: "Estimate", name: "Name" }, notSure: "menu: not sure yet", hallAny: "hall to be chosen"
    }
  }[lang];

  /* ---------- Helpers ---------- */
  function pad(n) { return (n < 10 ? "0" : "") + n; }
  function ymd(d) { return d.getFullYear() + "-" + pad(d.getMonth() + 1) + "-" + pad(d.getDate()); }
  function toDate(v) { var p = v.split("-"); return new Date(+p[0], +p[1] - 1, +p[2]); }
  function addDays(d, n) { return new Date(d.getFullYear(), d.getMonth(), d.getDate() + n); }
  function el(tag, cls, text) { var n = document.createElement(tag); if (cls) n.className = cls; if (text !== undefined) n.textContent = text; return n; }
  function fill(s, o) { return s.replace(/\{(\w+)\}/g, function (m, k) { return o[k] !== undefined ? o[k] : m; }); }
  function eur(n) { var r = Math.round(n); return lang === "bg" ? r.toLocaleString("bg-BG") + " €" : "€" + r.toLocaleString("en-GB"); }
  function longDate(v) { return toDate(v).toLocaleDateString(T.locale, { weekday: "long", day: "numeric", month: "long", year: "numeric" }); }
  function scrollToEl(n) { n.scrollIntoView({ behavior: reduceMotion ? "auto" : "smooth", block: "start" }); }

  /* ---------- Colour scheme (skin) ---------- */
  var SKINS = ["ivory", "sage", "rose", "navy", "stone"];
  var skinBtns = document.querySelectorAll(".sw[data-skin]");
  var skinName = $("skinName");
  var animTimer;
  function setSkin(skin, save) {
    if (SKINS.indexOf(skin) === -1) skin = "ivory";
    if (save && !reduceMotion) { html.classList.add("skin-anim"); clearTimeout(animTimer); animTimer = setTimeout(function () { html.classList.remove("skin-anim"); }, 400); }
    html.dataset.skin = skin;
    skinBtns.forEach(function (b) {
      var on = b.dataset.skin === skin;
      b.setAttribute("aria-pressed", on ? "true" : "false");
      if (on && skinName) skinName.textContent = b.getAttribute("aria-label");
    });
    var meta = document.querySelector('meta[name="theme-color"]');
    if (meta) meta.content = getComputedStyle(html).getPropertyValue("--bg").trim() || meta.content;
    if (save) { try { localStorage.setItem("lozetaSkin", skin); } catch (e) {} }
  }
  skinBtns.forEach(function (b) { b.addEventListener("click", function () { setSkin(b.dataset.skin, true); }); });
  setSkin(html.dataset.skin, false);

  /* ---------- Menu (mobile) ---------- */
  var burger = $("burger"), nav = $("nav");
  function setMenu(open) { nav.classList.toggle("open", open); burger.setAttribute("aria-expanded", open ? "true" : "false"); }
  burger.addEventListener("click", function () { setMenu(!nav.classList.contains("open")); });
  nav.addEventListener("click", function (e) { if (e.target.closest("a")) setMenu(false); });
  document.addEventListener("keydown", function (e) { if (e.key === "Escape" && nav.classList.contains("open")) { setMenu(false); burger.focus(); } });
  document.querySelectorAll("#hours [data-hrs]").forEach(function (r) { r.classList.toggle("today", r.dataset.hrs === "wd"); });

  /* ---------- Request ---------- */
  var form = $("planForm"), dateIn = $("f-date"), timeSel = $("f-time"), hint = $("timeHint");
  dateIn.min = ymd(addDays(new Date(), 1)); dateIn.max = ymd(addDays(new Date(), 540));
  function guests() { return parseInt(form.elements.guests.value, 10) || 0; }
  function pkgId() { var c = form.querySelector('input[name="pkg"]:checked'); return c ? c.value : "unsure"; }
  function estimate() {
    var g = guests(), box = $("est");
    if (g < D.min || g > D.max) { box.textContent = fill(T.estGuests, { min: D.min, max: D.max }); return null; }
    var id = pkgId();
    if (id === "unsure") { box.textContent = T.estNone; return null; }
    var p = D.packages[id].price, fee = g < D.feeBelow ? D.fee : 0, total = g * p + fee;
    box.innerHTML = fill(T.est, { t: eur(total), n: g, p: eur(p), fee: fee ? fill(T.estFee, { f: eur(fee) }) : "" });
    return total;
  }
  form.addEventListener("input", estimate); form.addEventListener("change", estimate); estimate();
  function setTimes(r) {
    timeSel.textContent = "";
    if (!r.slots.length) { hint.textContent = T.noSlots; return; }
    timeSel.appendChild(new Option(T.pick, ""));
    r.slots.forEach(function (s) { timeSel.appendChild(new Option(s, s)); });
    hint.textContent = fill(T.slotsHint, { n: r.slots.length });
  }
  function loadTimes() {
    var v = dateIn.value;
    if (!v) { hint.textContent = T.checking; timeSel.textContent = ""; return Promise.resolve(); }
    hint.textContent = T.checkingNow;
    return API.availability(v, D.event).then(function (r) { if (dateIn.value === v) setTimes(r); }).catch(function () { hint.textContent = T.availError; });
  }
  dateIn.addEventListener("change", loadTimes);

  var errBox = $("pError"), sendBtn = $("pSend"), doneBox = $("pDone");
  function showError(msg) { errBox.textContent = msg; errBox.hidden = false; }
  if (API.mode === "demo") { var dn = $("demoNote"); dn.textContent = T.demoLine; dn.hidden = false; }
  form.addEventListener("submit", function (e) {
    e.preventDefault(); errBox.hidden = true;
    var g = guests();
    if (g < D.min || g > D.max) { form.elements.guests.focus(); return showError(fill(T.errGuests, { min: D.min, max: D.max })); }
    if (!dateIn.value || !timeSel.value) return showError(T.errTime);
    var name = form.elements.name.value.trim(), phone = form.elements.phone.value.trim();
    if (!name || phone.replace(/\D/g, "").length < 6) return showError(T.errName);
    var type = form.elements.type.value, hall = form.elements.hall.value, id = pkgId(), est = estimate();
    var summary = D.events[type] + " · " + fill(T.guests, { n: g }) + " · " + (id === "unsure" ? T.notSure : D.packages[id].name) + " · " + (hall === "any" ? T.hallAny : D.halls[hall]);
    var payload = {
      name: name, phone: phone, service: D.events[type], date: dateIn.value, time: timeSel.value, durationMinutes: D.event, fulfil: "pickup", lang: lang,
      message: form.elements.msg.value.trim(),
      plan: { summary: summary, type: type, guests: g, hall: hall, package: id, estimate: est }
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
    var rows = [[T.lines.when, longDate(p.date) + ", " + p.time], [T.lines.what, p.plan.summary]];
    if (p.plan.estimate) rows.push([T.lines.est, eur(p.plan.estimate)]);
    rows.push([T.lines.name, p.name]);
    rows.forEach(function (r) { dl.appendChild(el("dt", "", r[0])); dl.appendChild(el("dd", "", r[1])); });
    doneBox.appendChild(dl);
    doneBox.appendChild(el("p", "", T.doneNext));
    if (API.mode === "demo") doneBox.appendChild(el("p", "demo-note", T.doneDemo));
    var act = el("div", "done-actions");
    if (API.mode === "demo") { var a = el("a", "btn btn-line", T.adminLink); a.href = (lang === "bg" ? "" : "../") + "admin.html" + (lang === "en" ? "?lang=en" : ""); act.appendChild(a); }
    var again = el("button", "btn btn-main", T.again); again.type = "button";
    again.addEventListener("click", function () { form.reset(); form.hidden = false; doneBox.hidden = true; timeSel.textContent = ""; hint.textContent = T.checking; estimate(); scrollToEl($("plan")); });
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
