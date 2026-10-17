/* Gripline (tyre shop design 1): page behaviour.
   Colour schemes, menu, the tyre size finder, live workshop status, the visit builder (car, size, job, add-ons, a day and a free time,
   a live price slip) and the map. The visit talks to GriplineAPI (js/api.js): a mock server now, a real backend later (docs/API.md). */
(function () {
  "use strict";

  var CFG = window.GRIPLINE_CONFIG || {};
  var API = window.GriplineAPI;
  var html = document.documentElement;
  var lang = html.lang === "bg" ? "bg" : "en";
  var reduceMotion = window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches;
  function $(id) { return document.getElementById(id); }
  var D = JSON.parse($("gripData").textContent);
  var SLOT = CFG.slotMinutes || 15;

  var T = {
    bg: {
      locale: "bg-BG", mapTitle: "Карта на сервиза", today: "Днес", tomorrow: "Утре", hUnit: "ч", mUnit: "мин", free: "безплатно", from: "от",
      openNow: "Отворено до {t}", closedOpens: "Затворено · отваря в {t}", closedTomorrow: "Затворено · отваря утре в {t}", closedDay: "Затворено",
      finderOut: "{size}: {job} от <b>{price}</b>", slotsHint: "Свободни часове: {n}. Избери кога да дойдеш.", noSlots: "Няма свободни часове този ден. Избери друг ден.", availError: "Не успяхме да проверим часовете. Опитай пак.", checking: "Проверяваме свободните часове…",
      liveNone: "няма скоро", liveCount: "{n}", carDash: "Избери марка и размер",
      errMake: "Избери марка на автомобила.", errTime: "Избери ден и час.", errName: "Въведи име и телефон.", errTaken: "Съжаляваме, този час току-що беше зает. Избери друг.", errInvalid: "Провери данните и опитай пак.", errGeneric: "Нещо се обърка. Опитай пак или ни се обади.",
      sending: "Изпращане…", demoLine: "Демо режим: заявките се пазят само в този браузър и нищо не се изпраща.",
      doneH: "Заявката е приета", doneRef: "Номер", statusPending: "Чака потвърждение", doneNext: "Ще те потърсим по телефона, за да потвърдим часа. Плащаш на място. Запази номера.",
      doneDemo: "Демо режим: нищо не беше изпратено. Заявката е записана само в този браузър.", adminLink: "Виж я в демо админ панела", again: "Нова заявка",
      lines: { when: "Час", car: "Автомобил", size: "Размер", work: "Работа", total: "Ориентировъчно", name: "Име" }, otherMake: "Друга марка", tyresQuoted: "гумите се оферират отделно"
    },
    en: {
      locale: "en-GB", mapTitle: "Map of the workshop", today: "Today", tomorrow: "Tomorrow", hUnit: "h", mUnit: "min", free: "free", from: "from",
      openNow: "Open until {t}", closedOpens: "Closed · opens at {t}", closedTomorrow: "Closed · opens tomorrow at {t}", closedDay: "Closed",
      finderOut: "{size}: {job} from <b>{price}</b>", slotsHint: "{n} free times. Choose when you will come.", noSlots: "No free times on this day. Please pick another day.", availError: "We could not check the times. Please try again.", checking: "Checking free times…",
      liveNone: "none soon", liveCount: "{n}", carDash: "Choose a make and size",
      errMake: "Please choose your car make.", errTime: "Please pick a day and a time.", errName: "Please enter your name and phone.", errTaken: "Sorry, that time was just taken. Please choose another.", errInvalid: "Please check your details and try again.", errGeneric: "Something went wrong. Please try again or call us.",
      sending: "Sending…", demoLine: "Demo mode: requests are kept in this browser only and nothing is sent.",
      doneH: "Request received", doneRef: "Reference", statusPending: "Waiting for confirmation", doneNext: "We will call you to confirm the time. You pay on site. Keep your reference.",
      doneDemo: "Demo mode: nothing was sent. The request is saved only in this browser.", adminLink: "See it in the demo back office", again: "New request",
      lines: { when: "Time", car: "Car", size: "Size", work: "Work", total: "Estimate", name: "Name" }, otherMake: "Other make", tyresQuoted: "tyres quoted separately"
    }
  }[lang];

  /* ---------- Helpers ---------- */
  function pad(n) { return (n < 10 ? "0" : "") + n; }
  function ymd(d) { return d.getFullYear() + "-" + pad(d.getMonth() + 1) + "-" + pad(d.getDate()); }
  function toDate(v) { var p = v.split("-"); return new Date(+p[0], +p[1] - 1, +p[2]); }
  function addDays(d, n) { return new Date(d.getFullYear(), d.getMonth(), d.getDate() + n); }
  function el(tag, cls, text) { var n = document.createElement(tag); if (cls) n.className = cls; if (text !== undefined) n.textContent = text; return n; }
  function fill(s, o) { return s.replace(/\{(\w+)\}/g, function (m, k) { return o[k] !== undefined ? o[k] : m; }); }
  function eur(n) { n = Math.round(n * 100) / 100; return (n % 1 ? n.toFixed(2).replace(".", lang === "bg" ? "," : ".") : String(n)) + " €"; }
  function longDate(v) { return toDate(v).toLocaleDateString(T.locale, { weekday: "long", day: "numeric", month: "long" }); }
  function fmtMin(m) { var h = Math.floor(m / 60), r = m % 60, o = []; if (h) o.push(h + " " + T.hUnit); if (r) o.push(r + " " + T.mUnit); return o.join(" "); }
  function scrollToEl(n) { n.scrollIntoView({ behavior: reduceMotion ? "auto" : "smooth", block: "start" }); }
  function hoursFor(d) { var g = d.getDay(); return g === 0 || g === 6 ? CFG.hours.weekend : CFG.hours.weekday; }
  function toMin(h) { var p = h.split(":"); return +p[0] * 60 + +p[1]; }

  /* ---------- Colour scheme (skin) ---------- */
  var SKINS = ["hazard", "redline", "cobalt", "forest", "concrete"];
  var skinBtns = document.querySelectorAll(".sw[data-skin]");
  var skinName = $("skinName");
  var animTimer;
  function setSkin(skin, save) {
    if (SKINS.indexOf(skin) === -1) skin = "hazard";
    if (save && !reduceMotion) { html.classList.add("skin-anim"); clearTimeout(animTimer); animTimer = setTimeout(function () { html.classList.remove("skin-anim"); }, 500); }
    html.dataset.skin = skin;
    skinBtns.forEach(function (b) {
      var on = b.dataset.skin === skin;
      b.setAttribute("aria-pressed", on ? "true" : "false");
      if (on && skinName) skinName.textContent = b.getAttribute("aria-label");
    });
    var meta = document.querySelector('meta[name="theme-color"]');
    if (meta) meta.content = getComputedStyle(html).getPropertyValue("--bg").trim() || meta.content;
    if (save) { try { localStorage.setItem("griplineSkin", skin); } catch (e) {} }
  }
  skinBtns.forEach(function (b) { b.addEventListener("click", function () { setSkin(b.dataset.skin, true); }); });
  setSkin(html.dataset.skin, false);

  /* ---------- Menu (mobile) ---------- */
  var burger = $("burger"), nav = $("nav");
  function setMenu(open) { nav.classList.toggle("open", open); burger.setAttribute("aria-expanded", open ? "true" : "false"); }
  burger.addEventListener("click", function () { setMenu(!nav.classList.contains("open")); });
  nav.addEventListener("click", function (e) { if (e.target.closest("a")) setMenu(false); });
  document.addEventListener("keydown", function (e) { if (e.key === "Escape" && nav.classList.contains("open")) { setMenu(false); burger.focus(); } });

  /* ---------- Pricing ---------- */
  function vehicleAdd() { var v = document.querySelector('input[name="veh"]:checked'); var f = D.vehicles.filter(function (x) { return x.id === (v && v.value); })[0]; return f ? f.add : 0; }
  function rimNow() { return +$("s-rim").value; }
  function priceOf(item, rim, vAdd) {
    if (item.kind === "size") return item.price + Math.max(0, rim - 15) * D.perInch + vAdd;
    if (item.kind === "storage") return item.price + (rim >= 18 ? 10 : 0);
    return item.price;
  }
  function byId(list, id) { return list.filter(function (x) { return x.id === id; })[0]; }
  function priceText(item, rim, vAdd) { var p = priceOf(item, rim, vAdd); return p ? (item.kind === "size" ? T.from + " " : "") + eur(p) : T.free; }

  /* ---------- Opening status and live card ---------- */
  var DAYS = [0, 1, 2, 3, 4, 5].map(function (i) { return ymd(addDays(new Date(), i)); });
  function dayLabel(v, i) { return i === 0 ? T.today : i === 1 ? T.tomorrow : toDate(v).toLocaleDateString(T.locale, { weekday: "short", day: "numeric" }); }
  function updateOpen() {
    var now = new Date(), h = hoursFor(now), m = now.getHours() * 60 + now.getMinutes(), state, text;
    if (m >= toMin(h[0]) && m < toMin(h[1])) { state = "open"; text = fill(T.openNow, { t: h[1] }); }
    else if (m < toMin(h[0])) { state = "closed"; text = fill(T.closedOpens, { t: h[0] }); }
    else { state = "closed"; text = fill(T.closedTomorrow, { t: hoursFor(addDays(now, 1))[0] }); }
    $("liveState").dataset.state = state; $("liveText").textContent = text;
    $("liveHours").textContent = h[0] + " – " + h[1];
    var g = now.getDay(), key = g === 0 || g === 6 ? "we" : "wd";
    document.querySelectorAll("#hours [data-hrs]").forEach(function (r) { r.classList.toggle("today", r.dataset.hrs === key); });
  }
  updateOpen(); setInterval(updateOpen, 60000);
  function firstFree(i, minutes) {
    if (i >= DAYS.length) return Promise.resolve(null);
    return API.availability(DAYS[i], minutes).then(function (r) { return r.slots.length ? { i: i, r: r } : firstFree(i + 1, minutes); });
  }
  API.availability(DAYS[0], 45).then(function (r) {
    $("liveFree").textContent = fill(T.liveCount, { n: r.slots.length });
  }).catch(function () {});
  firstFree(0, 45).then(function (f) {
    $("liveNext").textContent = f ? (dayLabel(DAYS[f.i], f.i).toLowerCase() + ", " + f.r.slots[0]) : T.liveNone;
  }).catch(function () { $("liveNext").textContent = "–"; });

  /* ---------- Size finder and the slip ---------- */
  var form = $("bookForm"), state = { date: "", time: "" };
  function sizeText() { return $("s-width").value + "/" + $("s-profile").value + " R" + $("s-rim").value; }
  function finderUpdate() {
    var rim = +$("h-rim").value, size = $("h-width").value + "/" + $("h-profile").value + " R" + rim;
    var job = byId(D.jobs, "swap");
    $("fndOut").innerHTML = fill(T.finderOut, { size: size, job: job.name.toLowerCase(), price: eur(priceOf(job, rim, 0)) });
  }
  ["h-width", "h-profile", "h-rim"].forEach(function (id) { $(id).addEventListener("change", finderUpdate); });
  finderUpdate();
  $("fndGo").addEventListener("click", function () {
    $("s-width").value = $("h-width").value; $("s-profile").value = $("h-profile").value; $("s-rim").value = $("h-rim").value;
    refresh();
  });

  function chosenJob() { var j = form.querySelector('input[name="job"]:checked'); return byId(D.jobs, j ? j.value : "swap"); }
  function chosenAddons() { return Array.prototype.slice.call(form.querySelectorAll('input[name="addon"]:checked')).map(function (c) { return byId(D.addons, c.value); }); }
  function items() { return [chosenJob()].concat(chosenAddons()); }
  function minutes() { return Math.min(180, items().reduce(function (s, x) { return s + x.min; }, 0)); }
  function total() { var rim = rimNow(), v = vehicleAdd(); return items().reduce(function (s, x) { return s + priceOf(x, rim, v); }, 0); }
  function carText() {
    var mk = $("f-make").value, model = $("f-model").value.trim(), v = form.querySelector('input[name="veh"]:checked');
    var veh = byId(D.vehicles, v ? v.value : "car");
    var name = (mk === "other" ? T.otherMake : mk) + (model ? " " + model : "");
    return (name ? name + " · " : "") + sizeText() + " · " + veh.name;
  }
  function renderPrices() {
    var rim = rimNow(), v = vehicleAdd();
    form.querySelectorAll(".opt-p").forEach(function (n) {
      var it = byId(D.jobs, n.dataset.price) || byId(D.addons, n.dataset.price);
      n.textContent = priceText(it, rim, v);
    });
  }
  var slotTimer;
  function renderSlip() {
    var rim = rimNow(), v = vehicleAdd(), ul = $("slipLines");
    ul.textContent = "";
    items().forEach(function (x) {
      var li = el("li"); li.appendChild(el("span", "", x.name)); li.appendChild(el("span", "", priceOf(x, rim, v) ? eur(priceOf(x, rim, v)) : T.free)); ul.appendChild(li);
    });
    $("slipCar").textContent = carText();
    $("slipTotal").textContent = total() ? eur(total()) : T.free;
    $("slipTime").textContent = fmtMin(minutes());
  }
  function refresh() {
    renderPrices(); renderSlip();
    clearTimeout(slotTimer);
    slotTimer = setTimeout(function () { if (state.date) pickDay(state.date, true); }, 250);
  }
  form.addEventListener("change", function (e) { if (e.target.closest(".dchips, .tchips")) return; refresh(); });
  $("f-model").addEventListener("input", renderSlip);

  /* ---------- Day and time ---------- */
  var dayBox = $("dchips"), timeBox = $("tchips"), slotHint = $("slotHint");
  function renderDays() {
    dayBox.textContent = "";
    DAYS.forEach(function (v, i) {
      var b = el("button", "dchip", dayLabel(v, i)); b.type = "button"; b.setAttribute("role", "radio");
      b.setAttribute("aria-checked", state.date === v ? "true" : "false");
      b.addEventListener("click", function () { state.time = ""; pickDay(v, false); });
      dayBox.appendChild(b);
    });
  }
  function pickDay(v, keepTime) {
    var prev = keepTime ? state.time : "";
    state.date = v; if (!keepTime) state.time = ""; renderDays(); timeBox.textContent = ""; slotHint.textContent = T.checking;
    return API.availability(v, minutes()).then(function (r) {
      if (state.date !== v) return;
      if (prev && r.slots.indexOf(prev) === -1) state.time = "";
      showSlots(r);
    }).catch(function () { slotHint.textContent = T.availError; });
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
  renderDays(); renderPrices(); renderSlip();
  firstFree(0, minutes()).then(function (f) {
    if (!f) { pickDay(DAYS[0], false); return; }
    state.date = DAYS[f.i]; renderDays(); showSlots(f.r);
  }).catch(function () { pickDay(DAYS[0], false); });

  /* ---------- Send ---------- */
  var errBox = $("bkError"), sendBtn = $("bkSend"), doneBox = $("bkDone");
  function showError(msg) { errBox.textContent = msg; errBox.hidden = false; }
  if (API.mode === "demo") { var dn = $("demoNote"); dn.textContent = T.demoLine; dn.hidden = false; }
  form.addEventListener("submit", function (e) {
    e.preventDefault(); errBox.hidden = true;
    if (!$("f-make").value) { $("f-make").focus(); return showError(T.errMake); }
    if (!state.date || !state.time) return showError(T.errTime);
    var name = form.elements.name.value.trim(), phone = form.elements.phone.value.trim();
    if (!name || phone.replace(/\D/g, "").length < 6) return showError(T.errName);
    var job = chosenJob(), adds = chosenAddons(), mins = minutes();
    var summary = carText() + " · " + job.name + (adds.length ? " + " + adds.map(function (a) { return a.name; }).join(", ") : "");
    var payload = {
      name: name, phone: phone, service: job.name, date: state.date, time: state.time, durationMinutes: mins, fulfil: "pickup", lang: lang,
      message: form.elements.msg.value.trim(),
      plan: { summary: summary, total: Math.round(total() * 100) / 100, minutes: mins, size: sizeText(), job: job.id, addons: adds.map(function (a) { return a.id; }),
              car: { make: $("f-make").value, model: $("f-model").value.trim(), plate: $("f-plate").value.trim(), vehicle: form.querySelector('input[name="veh"]:checked').value } }
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
    [[T.lines.when, longDate(p.date) + ", " + p.time + " (" + fmtMin(p.durationMinutes) + ")"], [T.lines.car, carText()], [T.lines.work, p.plan.summary.split(" · ").slice(-1)[0]],
     [T.lines.total, p.plan.total ? eur(p.plan.total) : T.free], [T.lines.name, p.name]].forEach(function (r) { dl.appendChild(el("dt", "", r[0])); dl.appendChild(el("dd", "", r[1])); });
    doneBox.appendChild(dl);
    doneBox.appendChild(el("p", "", T.doneNext));
    if (API.mode === "demo") doneBox.appendChild(el("p", "demo-note", T.doneDemo));
    var act = el("div", "done-actions");
    if (API.mode === "demo") { var a = el("a", "btn btn-line", T.adminLink); a.href = (lang === "bg" ? "" : "../") + "admin.html" + (lang === "en" ? "?lang=en" : ""); act.appendChild(a); }
    var again = el("button", "btn btn-main", T.again); again.type = "button";
    again.addEventListener("click", function () { form.reset(); form.hidden = false; doneBox.hidden = true; state.time = ""; finderUpdate(); refresh(); pickDay(state.date || DAYS[0], false); scrollToEl($("book")); });
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

  /* ---------- Call / Book bar on phones: shown after the first screen, hidden while the form is on screen ---------- */
  if ("IntersectionObserver" in window) {
    var seen = { hero: true, book: false }, bar = $("bar");
    var upd = function () { bar.classList.toggle("show", !seen.hero && !seen.book); };
    new IntersectionObserver(function (es) { seen.hero = es[0].isIntersecting; upd(); }).observe(document.querySelector(".hero"));
    new IntersectionObserver(function (es) { seen.book = es[0].isIntersecting; upd(); }, { threshold: .08 }).observe($("book"));
  }

  /* ---------- Scroll reveal ---------- */
  if (html.classList.contains("js-reveal")) {
    var targets = document.querySelectorAll(".sec-head, .board, .seasons li, .tread, .qa, .visit-copy, .visit-side, .step");
    var io = new IntersectionObserver(function (es) { es.forEach(function (x) { if (x.isIntersecting) { x.target.classList.add("in"); io.unobserve(x.target); } }); }, { rootMargin: "0px 0px -8% 0px" });
    targets.forEach(function (t, i) { t.classList.add("rv"); t.style.setProperty("--d", (i % 3) * 0.06 + "s"); io.observe(t); });
  }
})();
