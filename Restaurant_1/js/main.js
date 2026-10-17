/* Maslina (restaurant design 1): page behaviour.
   Colour schemes, menu filters, opening status, the quick booking bar, the reservation builder (guests, day, free time, occasion,
   seating, allergies, details, a live reservation card) and the map. The reservation talks to MaslinaAPI (js/api.js):
   a mock server now, a real backend later (docs/API.md). */
(function () {
  "use strict";

  var CFG = window.MASLINA_CONFIG || {};
  var API = window.MaslinaAPI;
  var html = document.documentElement;
  var lang = html.lang === "bg" ? "bg" : "en";
  var reduceMotion = window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches;
  function $(id) { return document.getElementById(id); }
  var D = JSON.parse($("masData").textContent);
  var SLOT = CFG.slotMinutes || 30;

  var T = {
    bg: {
      locale: "bg-BG", mapTitle: "Карта на ресторанта", today: "Днес", tomorrow: "Утре", hUnit: "ч", mUnit: "мин",
      openNow: "Отворено до {t}", closedOpens: "Затворено · отваря в {t}", closedTomorrow: "Затворено · отваря утре в {t}",
      guests1: "1 гост", guestsN: "{n} гости", table: "Маса за {n}", lunchLabel: "Обяд", dinnerLabel: "Вечеря",
      slotsHint: "Свободни часове: {n}. Избери кога да дойдете.", noSlots: "Няма свободни маси този ден. Избери друг ден.", availError: "Не успяхме да проверим масите. Опитай пак.", checking: "Проверяваме свободните маси…",
      bigGroup: "За групи над {n} души ни се обадете.", mediumGroup: "При по-голяма група може да ви се обадим за потвърждение.",
      errTime: "Избери ден и час.", errName: "Въведи име и телефон.", errTaken: "Съжаляваме, този час току-що беше зает. Избери друг.", errInvalid: "Провери данните и опитай пак.", errGeneric: "Нещо се обърка. Опитай пак или ни се обади.",
      sending: "Изпращане…", demoLine: "Демо режим: резервациите се пазят само в този браузър и нищо не се изпраща.",
      doneH: "Масата е запазена", doneRef: "Номер", statusPending: "Чака потвърждение", doneNext: "Очакваме ви в избрания час. Пазим масата 15 минути. Запази номера.",
      doneDemo: "Демо режим: нищо не беше изпратено. Резервацията е записана само в този браузър.", adminLink: "Виж я в демо админ панела", again: "Нова резервация",
      lines: { when: "Кога", party: "Гости", table: "Маса", notes: "Бележки", name: "Име" }, none: "–", noMenu: "Няма ястия с тези филтри."
    },
    en: {
      locale: "en-GB", mapTitle: "Map of the restaurant", today: "Today", tomorrow: "Tomorrow", hUnit: "h", mUnit: "min",
      openNow: "Open until {t}", closedOpens: "Closed · opens at {t}", closedTomorrow: "Closed · opens tomorrow at {t}",
      guests1: "1 guest", guestsN: "{n} guests", table: "Table for {n}", lunchLabel: "Lunch", dinnerLabel: "Dinner",
      slotsHint: "{n} free times. Choose when you will come.", noSlots: "No free tables on this day. Please pick another day.", availError: "We could not check the tables. Please try again.", checking: "Checking free tables…",
      bigGroup: "For groups of more than {n} please call us.", mediumGroup: "For a larger group we may call to confirm.",
      errTime: "Please pick a day and a time.", errName: "Please enter your name and phone.", errTaken: "Sorry, that time was just taken. Please choose another.", errInvalid: "Please check your details and try again.", errGeneric: "Something went wrong. Please try again or call us.",
      sending: "Sending…", demoLine: "Demo mode: reservations are kept in this browser only and nothing is sent.",
      doneH: "Table reserved", doneRef: "Reference", statusPending: "Waiting for confirmation", doneNext: "We look forward to seeing you. We hold the table for 15 minutes. Keep your reference.",
      doneDemo: "Demo mode: nothing was sent. The reservation is saved only in this browser.", adminLink: "See it in the demo back office", again: "New reservation",
      lines: { when: "When", party: "Guests", table: "Table", notes: "Notes", name: "Name" }, none: "–", noMenu: "No dishes match these filters."
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
  function shortDate(v) { return toDate(v).toLocaleDateString(T.locale, { weekday: "short", day: "numeric", month: "short" }); }
  function scrollToEl(n) { n.scrollIntoView({ behavior: reduceMotion ? "auto" : "smooth", block: "start" }); }
  function hoursFor(d) { var g = d.getDay(); return g === 0 || g === 6 ? CFG.hours.weekend : CFG.hours.weekday; }
  function toMin(h) { var p = h.split(":"); return +p[0] * 60 + +p[1]; }
  function guestsText(n) { return n === 1 ? T.guests1 : fill(T.guestsN, { n: n }); }
  function duration(n) { return n <= 4 ? 90 : n <= 6 ? 105 : 120; }

  /* ---------- Colour scheme (skin) ---------- */
  var SKINS = ["olive", "bordeaux", "terracotta", "sea", "brass"];
  var skinBtns = document.querySelectorAll(".sw[data-skin]");
  var skinName = $("skinName");
  var animTimer;
  function setSkin(skin, save) {
    if (SKINS.indexOf(skin) === -1) skin = "olive";
    if (save && !reduceMotion) { html.classList.add("skin-anim"); clearTimeout(animTimer); animTimer = setTimeout(function () { html.classList.remove("skin-anim"); }, 500); }
    html.dataset.skin = skin;
    skinBtns.forEach(function (b) {
      var on = b.dataset.skin === skin;
      b.setAttribute("aria-pressed", on ? "true" : "false");
      if (on && skinName) skinName.textContent = b.getAttribute("aria-label");
    });
    var meta = document.querySelector('meta[name="theme-color"]');
    if (meta) meta.content = getComputedStyle(html).getPropertyValue("--bg").trim() || meta.content;
    if (save) { try { localStorage.setItem("maslinaSkin", skin); } catch (e) {} }
  }
  skinBtns.forEach(function (b) { b.addEventListener("click", function () { setSkin(b.dataset.skin, true); }); });
  setSkin(html.dataset.skin, false);

  /* ---------- Menu (mobile) ---------- */
  var burger = $("burger"), nav = $("nav");
  function setMenu(open) { nav.classList.toggle("open", open); burger.setAttribute("aria-expanded", open ? "true" : "false"); }
  burger.addEventListener("click", function () { setMenu(!nav.classList.contains("open")); });
  nav.addEventListener("click", function (e) { if (e.target.closest("a")) setMenu(false); });
  document.addEventListener("keydown", function (e) { if (e.key === "Escape" && nav.classList.contains("open")) { setMenu(false); burger.focus(); } });

  /* ---------- Opening status ---------- */
  function updateOpen() {
    var now = new Date(), h = hoursFor(now), m = now.getHours() * 60 + now.getMinutes(), state, text;
    if (m >= toMin(h[0]) && m < toMin(h[1])) { state = "open"; text = fill(T.openNow, { t: h[1] }); }
    else if (m < toMin(h[0])) { state = "closed"; text = fill(T.closedOpens, { t: h[0] }); }
    else { state = "closed"; text = fill(T.closedTomorrow, { t: hoursFor(addDays(now, 1))[0] }); }
    $("openPill").dataset.state = state; $("openText").textContent = text;
    var g = now.getDay(), key = g === 0 || g === 6 ? "we" : "wd";
    document.querySelectorAll("#hours [data-hrs]").forEach(function (r) { r.classList.toggle("today", r.dataset.hrs === key); });
  }
  updateOpen(); setInterval(updateOpen, 60000);

  /* ---------- Menu filters ---------- */
  var catBtns = document.querySelectorAll("#cats .chip"), dietBtns = document.querySelectorAll("#diets .chip");
  var cat = "all", diets = {};
  function applyMenu() {
    var shown = 0;
    document.querySelectorAll(".m-group").forEach(function (g) {
      var any = 0;
      g.querySelectorAll(".m-item").forEach(function (it) {
        var tags = it.dataset.tags.split(" ");
        var ok = (cat === "all" || it.dataset.cat === cat) &&
          (!diets.V || tags.indexOf("V") > -1 || tags.indexOf("VG") > -1) && (!diets.VG || tags.indexOf("VG") > -1) && (!diets.GF || tags.indexOf("GF") > -1);
        it.hidden = !ok; if (ok) any++;
      });
      g.hidden = !any; shown += any;
    });
    $("menuEmpty").hidden = shown > 0;
  }
  catBtns.forEach(function (b) { b.addEventListener("click", function () { cat = b.dataset.cat; catBtns.forEach(function (x) { x.setAttribute("aria-pressed", x === b ? "true" : "false"); }); applyMenu(); }); });
  dietBtns.forEach(function (b) {
    b.addEventListener("click", function () { var on = b.getAttribute("aria-pressed") !== "true"; b.setAttribute("aria-pressed", on ? "true" : "false"); diets[b.dataset.diet] = on; applyMenu(); });
  });

  /* ---------- Reservation state ---------- */
  var DAYS = [0, 1, 2, 3, 4, 5, 6, 7].map(function (i) { return ymd(addDays(new Date(), i)); });
  var state = { party: 2, date: DAYS[0], time: "" };
  function dayLabel(v, i) { return i === 0 ? T.today : i === 1 ? T.tomorrow : toDate(v).toLocaleDateString(T.locale, { weekday: "short", day: "numeric" }); }

  /* quick bar in the first screen */
  var qDate = $("qDate");
  DAYS.forEach(function (v, i) { var o = el("option", "", dayLabel(v, i) + (i > 1 ? "" : " · " + shortDate(v))); o.value = v; qDate.appendChild(o); });
  $("quick").addEventListener("submit", function (e) {
    e.preventDefault();
    state.party = +$("qParty").value; state.date = qDate.value; state.time = "";
    syncAll(); pickDay(state.date, false); scrollToEl($("reserve"));
  });

  /* ---------- Reservation form ---------- */
  var form = $("resForm"), dayBox = $("dchips"), timeBox = $("tchips"), slotHint = $("slotHint");
  function syncAll() {
    $("partyOut").textContent = state.party; $("qParty").value = String(state.party); qDate.value = state.date;
    var hint = $("partyHint");
    hint.textContent = state.party >= D.maxParty ? fill(T.bigGroup, { n: D.maxParty }) : state.party >= 7 ? T.mediumGroup : "";
    renderDays(); renderTicket();
  }
  $("pMinus").addEventListener("click", function () { if (state.party > 1) { state.party--; state.time = ""; syncAll(); pickDay(state.date, true); } });
  $("pPlus").addEventListener("click", function () { if (state.party < D.maxParty) { state.party++; state.time = ""; syncAll(); pickDay(state.date, true); } });
  function renderDays() {
    dayBox.textContent = "";
    DAYS.forEach(function (v, i) {
      var b = el("button", "dchip", dayLabel(v, i)); b.type = "button"; b.setAttribute("role", "radio");
      b.setAttribute("aria-checked", state.date === v ? "true" : "false");
      b.addEventListener("click", function () { state.date = v; state.time = ""; qDate.value = v; pickDay(v, false); renderTicket(); });
      dayBox.appendChild(b);
    });
  }
  function pickDay(v, keep) {
    state.date = v; renderDays(); timeBox.textContent = ""; slotHint.textContent = T.checking;
    return API.availability(v, duration(state.party)).then(function (r) { if (state.date !== v) return; showSlots(r); renderTicket(); })
      .catch(function () { slotHint.textContent = T.availError; });
  }
  function group(label, slots) {
    var g = el("div", "t-group"); g.appendChild(el("p", "t-label", label));
    var box = el("div", "t-chips"); box.setAttribute("role", "radiogroup"); box.setAttribute("aria-label", label);
    slots.forEach(function (s) {
      var b = el("button", "tchip", s); b.type = "button"; b.setAttribute("role", "radio"); b.setAttribute("aria-checked", state.time === s ? "true" : "false");
      b.addEventListener("click", function () {
        state.time = s;
        timeBox.querySelectorAll(".tchip").forEach(function (x) { x.setAttribute("aria-checked", x === b ? "true" : "false"); });
        renderTicket();
      });
      box.appendChild(b);
    });
    g.appendChild(box); return g;
  }
  function showSlots(r) {
    timeBox.textContent = "";
    if (state.time && r.slots.indexOf(state.time) === -1) state.time = "";
    if (!r.slots.length) { slotHint.textContent = T.noSlots; return; }
    slotHint.textContent = fill(T.slotsHint, { n: r.slots.length });
    var lunch = r.slots.filter(function (s) { return toMin(s) < 16 * 60; }), dinner = r.slots.filter(function (s) { return toMin(s) >= 16 * 60; });
    if (lunch.length) timeBox.appendChild(group(T.lunchLabel, lunch));
    if (dinner.length) timeBox.appendChild(group(T.dinnerLabel, dinner));
  }
  function allergies() { return Array.prototype.slice.call(form.querySelectorAll('input[name="allergy"]:checked')).map(function (c) { return c.dataset.name; }); }
  function notesText() {
    var n = [], occ = form.elements.occ.value;
    if (occ !== "none") n.push(D.occasions[occ]);
    var a = allergies(); if (a.length) n.push(a.join(", "));
    return n.length ? n.join(" · ") : T.none;
  }
  function renderTicket() {
    $("tkParty").textContent = guestsText(state.party);
    $("tkWhen").textContent = state.date ? shortDate(state.date) + (state.time ? ", " + state.time : "") : T.none;
    $("tkTable").textContent = D.seating[form.elements.seat.value];
    $("tkNotes").textContent = notesText();
  }
  form.addEventListener("change", function (e) { if (e.target.closest(".dchips, .t-chips")) return; renderTicket(); });
  syncAll();
  /* open on the first day with a free time */
  (function find(i) {
    if (i >= DAYS.length) { pickDay(DAYS[0], false); return; }
    API.availability(DAYS[i], duration(state.party)).then(function (r) {
      if (r.slots.length) { state.date = DAYS[i]; syncAll(); showSlots(r); } else find(i + 1);
    }).catch(function () { pickDay(DAYS[0], false); });
  })(0);

  /* ---------- Send ---------- */
  var errBox = $("bkError"), sendBtn = $("bkSend"), doneBox = $("bkDone");
  function showError(msg) { errBox.textContent = msg; errBox.hidden = false; }
  if (API.mode === "demo") { var dn = $("demoNote"); dn.textContent = T.demoLine; dn.hidden = false; }
  form.addEventListener("submit", function (e) {
    e.preventDefault(); errBox.hidden = true;
    if (!state.date || !state.time) return showError(T.errTime);
    var name = form.elements.name.value.trim(), phone = form.elements.phone.value.trim();
    if (!name || phone.replace(/\D/g, "").length < 6) return showError(T.errName);
    var summary = guestsText(state.party) + " · " + D.seating[form.elements.seat.value] + (notesText() !== T.none ? " · " + notesText() : "");
    var payload = {
      name: name, phone: phone, service: fill(T.table, { n: state.party }), date: state.date, time: state.time, durationMinutes: duration(state.party), fulfil: "pickup", lang: lang,
      message: form.elements.msg.value.trim(),
      plan: { summary: summary, party: state.party, seating: form.elements.seat.value, occasion: form.elements.occ.value, allergies: allergies() }
    };
    sendBtn.disabled = true; sendBtn.classList.add("is-busy"); var label = sendBtn.textContent; sendBtn.textContent = T.sending;
    API.createRequest(payload).then(function (res) { showDone(res, payload); })
      .catch(function (err) {
        if (err && err.code === "slot_taken") { showError(T.errTaken); state.time = ""; pickDay(state.date, false); }
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
    [[T.lines.when, longDate(p.date) + ", " + p.time], [T.lines.party, guestsText(p.plan.party)], [T.lines.table, D.seating[p.plan.seating]], [T.lines.notes, notesText()], [T.lines.name, p.name]].forEach(function (r) { dl.appendChild(el("dt", "", r[0])); dl.appendChild(el("dd", "", r[1])); });
    doneBox.appendChild(dl);
    doneBox.appendChild(el("p", "", T.doneNext));
    if (API.mode === "demo") doneBox.appendChild(el("p", "demo-note", T.doneDemo));
    var act = el("div", "done-actions");
    if (API.mode === "demo") { var a = el("a", "btn btn-line", T.adminLink); a.href = (lang === "bg" ? "" : "../") + "admin.html" + (lang === "en" ? "?lang=en" : ""); act.appendChild(a); }
    var again = el("button", "btn btn-main", T.again); again.type = "button";
    again.addEventListener("click", function () { form.reset(); form.hidden = false; doneBox.hidden = true; state.time = ""; syncAll(); pickDay(state.date, false); scrollToEl($("reserve")); });
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

  /* ---------- Call / Reserve bar on phones: shown after the first screen, hidden while the form is on screen ---------- */
  if ("IntersectionObserver" in window) {
    var seen = { hero: true, book: false }, bar = $("bar");
    var upd = function () { bar.classList.toggle("show", !seen.hero && !seen.book); };
    new IntersectionObserver(function (es) { seen.hero = es[0].isIntersecting; upd(); }).observe(document.querySelector(".hero"));
    new IntersectionObserver(function (es) { seen.book = es[0].isIntersecting; upd(); }, { threshold: .08 }).observe($("reserve"));
  }

  /* ---------- Scroll reveal ---------- */
  if (html.classList.contains("js-reveal")) {
    var targets = document.querySelectorAll(".sec-head, .sig, .m-group, .lunch-in, .step, .mo, .visit-copy, .visit-side");
    var io = new IntersectionObserver(function (es) { es.forEach(function (x) { if (x.isIntersecting) { x.target.classList.add("in"); io.unobserve(x.target); } }); }, { rootMargin: "0px 0px -8% 0px" });
    targets.forEach(function (t, i) { t.classList.add("rv"); t.style.setProperty("--d", (i % 3) * 0.06 + "s"); io.observe(t); });
  }
})();
