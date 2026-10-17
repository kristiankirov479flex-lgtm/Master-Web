/* Little Moka (café design 1): page behaviour.
   Colour schemes, menu, opening status, the order builder (menu to tray, milk choice, a pick-up day and time) and the map.
   The order talks to MokaAPI (js/api.js): a mock server now, a real backend later (docs/API.md). */
(function () {
  "use strict";

  var CFG = window.MOKA_CONFIG || {};
  var API = window.MokaAPI;
  var html = document.documentElement;
  var lang = html.lang === "bg" ? "bg" : "en";
  var reduceMotion = window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches;
  function $(id) { return document.getElementById(id); }
  var D = JSON.parse($("mokaData").textContent);
  var SLOT = CFG.slotMinutes || 10;

  var T = {
    bg: {
      locale: "bg-BG", mapTitle: "Карта на кафенето", today: "Днес", tomorrow: "Утре", items: "{n} бр.", openNow: "Отворено до {t}", closedOpens: "Затворено · отваря в {t}", closedTomorrow: "Затворено · отваря утре в {t}",
      nextToday: "Първи свободен час днес: {t}", nextDay: "Първи свободен час: {d}, {t}", nextNone: "Няма свободни часове скоро. Обади ни се.", checking: "Проверяваме свободните часове…",
      slotsHint: "Свободни часове: {n}. Избери кога да дойдеш.", noSlots: "Няма свободни часове този ден. Избери друг ден.", availError: "Не успяхме да проверим часовете. Опитай пак.",
      errItems: "Добави поне нещо от менюто.", errTime: "Избери ден и час за вземане.", errName: "Въведи име и телефон.", errTaken: "Съжаляваме, този час току-що беше зает. Избери друг.", errInvalid: "Провери данните и опитай пак.", errGeneric: "Нещо се обърка. Опитай пак или ни се обади.",
      sending: "Изпращане…", demoLine: "Демо режим: поръчките се пазят само в този браузър и нищо не се изпраща.",
      doneH: "Поръчката е приета", doneRef: "Номер", statusPending: "Чака потвърждение", doneNext: "Ще те чакаме на плота в избрания час. Плащаш на касата. Запази номера.",
      doneDemo: "Демо режим: нищо не беше изпратено. Поръчката е записана само в този браузър.", adminLink: "Виж я в демо админ панела", again: "Нова поръчка",
      lines: { when: "Вземане", items: "Поръчка", total: "Общо", name: "Име" }, remove: "Махни", plus: "Още един", minus: "Един по-малко", milk: "Мляко", count: "брой", service: "Поръчка за вземане", inBag: "в поръчката"
    },
    en: {
      locale: "en-GB", mapTitle: "Map of the café", today: "Today", tomorrow: "Tomorrow", items: "{n} items", openNow: "Open until {t}", closedOpens: "Closed · opens at {t}", closedTomorrow: "Closed · opens tomorrow at {t}",
      nextToday: "First free pick-up today: {t}", nextDay: "First free pick-up: {d}, {t}", nextNone: "No free times soon. Please call us.", checking: "Checking free times…",
      slotsHint: "{n} free times. Choose when you will come.", noSlots: "No free times on this day. Please pick another day.", availError: "We could not check the times. Please try again.",
      errItems: "Please add something from the menu.", errTime: "Please pick a day and a pick-up time.", errName: "Please enter your name and phone.", errTaken: "Sorry, that time was just taken. Please choose another.", errInvalid: "Please check your details and try again.", errGeneric: "Something went wrong. Please try again or call us.",
      sending: "Sending…", demoLine: "Demo mode: orders are kept in this browser only and nothing is sent.",
      doneH: "Order received", doneRef: "Reference", statusPending: "Waiting for confirmation", doneNext: "We will have it ready at the counter at your time. You pay at the till. Keep your reference.",
      doneDemo: "Demo mode: nothing was sent. The order is saved only in this browser.", adminLink: "See it in the demo back office", again: "New order",
      lines: { when: "Pick-up", items: "Order", total: "Total", name: "Name" }, remove: "Remove", plus: "One more", minus: "One fewer", milk: "Milk", count: "count", service: "Pick-up order", inBag: "in your order"
    }
  }[lang];

  /* ---------- Helpers ---------- */
  function pad(n) { return (n < 10 ? "0" : "") + n; }
  function ymd(d) { return d.getFullYear() + "-" + pad(d.getMonth() + 1) + "-" + pad(d.getDate()); }
  function toDate(v) { var p = v.split("-"); return new Date(+p[0], +p[1] - 1, +p[2]); }
  function addDays(d, n) { return new Date(d.getFullYear(), d.getMonth(), d.getDate() + n); }
  function el(tag, cls, text) { var n = document.createElement(tag); if (cls) n.className = cls; if (text !== undefined) n.textContent = text; return n; }
  function fill(s, o) { return s.replace(/\{(\w+)\}/g, function (m, k) { return o[k] !== undefined ? o[k] : m; }); }
  function eur(n) { return n.toFixed(2).replace(".", lang === "bg" ? "," : ".") + " €"; }
  function longDate(v) { return toDate(v).toLocaleDateString(T.locale, { weekday: "long", day: "numeric", month: "long" }); }
  function scrollToEl(n) { n.scrollIntoView({ behavior: reduceMotion ? "auto" : "smooth", block: "start" }); }
  function hoursFor(d) { var g = d.getDay(); return g === 0 || g === 6 ? CFG.hours.weekend : CFG.hours.weekday; }
  function toMin(h) { var p = h.split(":"); return +p[0] * 60 + +p[1]; }

  /* ---------- Colour scheme (skin) ---------- */
  var SKINS = ["latte", "matcha", "berry", "espresso", "blueberry"];
  var skinBtns = document.querySelectorAll(".sw[data-skin]");
  var skinName = $("skinName");
  var animTimer;
  function setSkin(skin, save) {
    if (SKINS.indexOf(skin) === -1) skin = "latte";
    if (save && !reduceMotion) { html.classList.add("skin-anim"); clearTimeout(animTimer); animTimer = setTimeout(function () { html.classList.remove("skin-anim"); }, 500); }
    html.dataset.skin = skin;
    skinBtns.forEach(function (b) {
      var on = b.dataset.skin === skin;
      b.setAttribute("aria-pressed", on ? "true" : "false");
      if (on && skinName) skinName.textContent = b.getAttribute("aria-label");
    });
    var meta = document.querySelector('meta[name="theme-color"]');
    if (meta) meta.content = getComputedStyle(html).getPropertyValue("--bg").trim() || meta.content;
    if (save) { try { localStorage.setItem("mokaSkin", skin); } catch (e) {} }
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
    var now = new Date(), h = hoursFor(now), m = now.getHours() * 60 + now.getMinutes();
    var state, text;
    if (m >= toMin(h[0]) && m < toMin(h[1])) { state = "open"; text = fill(T.openNow, { t: h[1] }); }
    else if (m < toMin(h[0])) { state = "closed"; text = fill(T.closedOpens, { t: h[0] }); }
    else { state = "closed"; text = fill(T.closedTomorrow, { t: hoursFor(addDays(now, 1))[0] }); }
    document.querySelectorAll(".open-pill").forEach(function (p) { p.dataset.state = state; p.querySelector(".open-text").textContent = text; });
    var g = now.getDay(), key = g === 0 || g === 6 ? "we" : "wd";
    document.querySelectorAll("#hours [data-hrs]").forEach(function (r) { r.classList.toggle("today", r.dataset.hrs === key); });
  }
  updateOpen(); setInterval(updateOpen, 60000);

  /* ---------- Menu filter ---------- */
  var catBtns = document.querySelectorAll("#cats .chip");
  catBtns.forEach(function (b) {
    b.addEventListener("click", function () {
      catBtns.forEach(function (x) { x.setAttribute("aria-pressed", x === b ? "true" : "false"); });
      document.querySelectorAll(".mgroup").forEach(function (g) { g.hidden = b.dataset.cat !== "all" && g.dataset.cat !== b.dataset.cat; });
    });
  });

  /* ---------- Order tray ---------- */
  var byId = {}; D.menu.forEach(function (m) { byId[m.id] = m; });
  var milkBy = {}; D.milk.forEach(function (m) { milkBy[m.id] = m; });
  var lines = [];   /* { id, milk, n } */
  var state = { date: "", time: "" };
  function unit(l) { var m = byId[l.id]; return m.price + (m.milk ? milkBy[l.milk].add : 0); }
  function total() { return lines.reduce(function (s, l) { return s + unit(l) * l.n; }, 0); }
  function count() { return lines.reduce(function (s, l) { return s + l.n; }, 0); }
  function lineName(l) { var m = byId[l.id]; return m.name + (m.milk && l.milk !== "whole" ? " (" + milkBy[l.milk].name.replace(/ \(.*$/, "").toLowerCase() + ")" : ""); }
  function summary() { return lines.map(function (l) { return l.n + " × " + lineName(l); }).join(", "); }

  function addItem(id) {
    var l = lines.filter(function (x) { return x.id === id && x.milk === "whole"; })[0];
    if (l) l.n++; else lines.push({ id: id, milk: "whole", n: 1 });
    renderTray();
  }
  function renderTray() {
    var ul = $("lines"); ul.textContent = "";
    lines.forEach(function (l, idx) {
      var m = byId[l.id], li = el("li", "line");
      li.appendChild(el("b", "", m.name));
      li.appendChild(el("span", "line-p", eur(unit(l) * l.n)));
      if (m.milk) {
        var sel = el("select"); sel.setAttribute("aria-label", T.milk + ": " + m.name);
        D.milk.forEach(function (o) { var op = el("option", "", o.name); op.value = o.id; if (o.id === l.milk) op.selected = true; sel.appendChild(op); });
        sel.addEventListener("change", function () {
          l.milk = sel.value;
          var twin = lines.filter(function (x, j) { return j !== idx && x.id === l.id && x.milk === l.milk; })[0];
          if (twin) { twin.n += l.n; lines.splice(idx, 1); }
          renderTray();
        });
        li.appendChild(sel);
      } else li.appendChild(el("span"));
      var st = el("div", "step");
      var minus = el("button", "", "−"); minus.type = "button"; minus.setAttribute("aria-label", T.minus + ": " + m.name);
      var plus = el("button", "", "+"); plus.type = "button"; plus.setAttribute("aria-label", T.plus + ": " + m.name);
      var out = el("span", "", String(l.n)); out.setAttribute("aria-label", T.count);
      minus.addEventListener("click", function () { l.n--; if (l.n < 1) lines.splice(idx, 1); renderTray(); });
      plus.addEventListener("click", function () { l.n++; renderTray(); });
      st.appendChild(minus); st.appendChild(out); st.appendChild(plus);
      li.appendChild(st);
      ul.appendChild(li);
    });
    $("trayEmpty").hidden = lines.length > 0;
    $("totalRow").hidden = lines.length === 0;
    $("total").textContent = eur(total());
    var perId = {}; lines.forEach(function (l) { perId[l.id] = (perId[l.id] || 0) + l.n; });
    document.querySelectorAll(".add").forEach(function (b) {
      var n = perId[b.dataset.id] || 0, badge = b.querySelector(".add-n");
      badge.hidden = n === 0; badge.textContent = n ? "×" + n : "";
    });
    var bar = $("bar");
    if (lines.length) { $("barTxt").textContent = fill(T.items, { n: count() }) + " · " + eur(total()); bar.hidden = false; } else bar.hidden = true;
  }
  document.querySelectorAll(".add").forEach(function (b) { b.addEventListener("click", function () { addItem(b.dataset.id); }); });
  /* the order bar hides when the order panel itself is on screen */
  if ("IntersectionObserver" in window) {
    new IntersectionObserver(function (es) { $("bar").classList.toggle("away", es[0].isIntersecting); $("bar").style.visibility = es[0].isIntersecting ? "hidden" : ""; }, { threshold: .25 }).observe($("tray"));
  }

  /* ---------- Pick-up day and time ---------- */
  var dayBox = $("dchips"), timeBox = $("tchips"), slotHint = $("slotHint");
  var DAYS = [0, 1, 2, 3].map(function (i) { return ymd(addDays(new Date(), i)); });
  function dayLabel(v, i) { return i === 0 ? T.today : i === 1 ? T.tomorrow : toDate(v).toLocaleDateString(T.locale, { weekday: "short", day: "numeric" }); }
  function renderDays() {
    dayBox.textContent = "";
    DAYS.forEach(function (v, i) {
      var b = el("button", "dchip", dayLabel(v, i)); b.type = "button"; b.setAttribute("role", "radio");
      b.setAttribute("aria-checked", state.date === v ? "true" : "false"); b.dataset.date = v;
      b.addEventListener("click", function () { pickDay(v); });
      dayBox.appendChild(b);
    });
  }
  function pickDay(v) {
    state.date = v; state.time = ""; renderDays(); timeBox.textContent = ""; slotHint.textContent = T.checking;
    return API.availability(v, SLOT).then(function (r) { if (state.date !== v) return; showSlots(r); return r; })
      .catch(function () { slotHint.textContent = T.availError; });
  }
  function showSlots(r) {
    timeBox.textContent = "";
    if (!r.slots.length) { slotHint.textContent = T.noSlots; return; }
    slotHint.textContent = fill(T.slotsHint, { n: r.slots.length });
    r.slots.forEach(function (s) {
      var b = el("button", "tchip", s); b.type = "button"; b.setAttribute("role", "radio"); b.setAttribute("aria-checked", state.time === s ? "true" : "false");
      b.addEventListener("click", function () {
        state.time = s;
        timeBox.querySelectorAll(".tchip").forEach(function (x) { x.setAttribute("aria-checked", x === b ? "true" : "false"); });
      });
      timeBox.appendChild(b);
    });
  }
  /* find the first day with a free time: used for the day chips and for the line in the hero */
  function firstFree(i) {
    if (i >= DAYS.length) return Promise.resolve(null);
    return API.availability(DAYS[i], SLOT).then(function (r) { return r.slots.length ? { i: i, r: r } : firstFree(i + 1); });
  }
  renderDays();
  firstFree(0).then(function (f) {
    var nt = $("nextText");
    if (!f) { nt.textContent = T.nextNone; pickDay(DAYS[0]); return; }
    nt.textContent = f.i === 0 ? fill(T.nextToday, { t: f.r.slots[0] }) : fill(T.nextDay, { d: dayLabel(DAYS[f.i], f.i).toLowerCase(), t: f.r.slots[0] });
    state.date = DAYS[f.i]; renderDays(); showSlots(f.r);
  }).catch(function () { $("nextText").textContent = T.availError; pickDay(DAYS[0]); });

  /* ---------- Send ---------- */
  var form = $("orderForm"), errBox = $("orError"), sendBtn = $("send"), doneBox = $("done");
  function showError(msg) { errBox.textContent = msg; errBox.hidden = false; }
  if (API.mode === "demo") { var dn = $("demoNote"); dn.textContent = T.demoLine; dn.hidden = false; }
  form.addEventListener("submit", function (e) {
    e.preventDefault(); errBox.hidden = true;
    if (!lines.length) return showError(T.errItems);
    if (!state.date || !state.time) return showError(T.errTime);
    var name = form.elements.name.value.trim(), phone = form.elements.phone.value.trim();
    if (!name || phone.replace(/\D/g, "").length < 6) return showError(T.errName);
    var payload = {
      name: name, phone: phone, service: T.service, date: state.date, time: state.time, durationMinutes: SLOT, fulfil: "pickup", lang: lang,
      message: form.elements.msg.value.trim(),
      plan: { summary: summary(), total: Math.round(total() * 100) / 100, items: lines.map(function (l) { return { id: l.id, n: l.n, milk: l.milk }; }) }
    };
    sendBtn.disabled = true; sendBtn.classList.add("is-busy"); var label = sendBtn.textContent; sendBtn.textContent = T.sending;
    API.createRequest(payload).then(function (res) { showDone(res, payload); })
      .catch(function (err) {
        if (err && err.code === "slot_taken") { showError(T.errTaken); state.time = ""; pickDay(state.date); }
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
    [[T.lines.when, longDate(p.date) + ", " + p.time], [T.lines.items, p.plan.summary], [T.lines.total, eur(p.plan.total)], [T.lines.name, p.name]].forEach(function (r) { dl.appendChild(el("dt", "", r[0])); dl.appendChild(el("dd", "", r[1])); });
    doneBox.appendChild(dl);
    doneBox.appendChild(el("p", "", T.doneNext));
    if (API.mode === "demo") doneBox.appendChild(el("p", "demo-note", T.doneDemo));
    var act = el("div", "done-actions");
    if (API.mode === "demo") { var a = el("a", "btn btn-line", T.adminLink); a.href = (lang === "bg" ? "" : "../") + "admin.html" + (lang === "en" ? "?lang=en" : ""); act.appendChild(a); }
    var again = el("button", "btn btn-main", T.again); again.type = "button";
    again.addEventListener("click", function () {
      lines = []; renderTray(); form.reset(); form.hidden = false; doneBox.hidden = true; state.time = "";
      pickDay(state.date || DAYS[0]); scrollToEl($("order"));
    });
    act.appendChild(again); doneBox.appendChild(act);
    doneBox.focus(); scrollToEl($("tray"));
  }
  renderTray();

  /* ---------- Map (loads only after a click, see the privacy page) ---------- */
  var mapBox = $("mapBox");
  $("mapLoad").addEventListener("click", function () {
    var f = document.createElement("iframe");
    f.src = mapBox.dataset.src; f.title = T.mapTitle; f.loading = "lazy"; f.referrerPolicy = "no-referrer";
    mapBox.textContent = ""; mapBox.appendChild(f);
  });

  $("year").textContent = new Date().getFullYear();

  /* ---------- Scroll reveal ---------- */
  if (html.classList.contains("js-reveal")) {
    var targets = document.querySelectorAll(".sec-head, .board, .bakery-in, .stampcard, .visit-copy, .visit-side, .menu .mgroup");
    var io = new IntersectionObserver(function (es) { es.forEach(function (x) { if (x.isIntersecting) { x.target.classList.add("in"); io.unobserve(x.target); } }); }, { rootMargin: "0px 0px -8% 0px" });
    targets.forEach(function (t, i) { t.classList.add("rv"); t.style.setProperty("--d", (i % 3) * 0.06 + "s"); io.observe(t); });
  }
})();
