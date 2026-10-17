/* Desk & Drip (café design 3): page behaviour.
   Colour schemes, menu, opening status, the floor plan (pick a zone), the booking builder (zone, hours, a day and a free start time,
   needs, a live price that never goes above the day price) and the map.
   The booking talks to DeskAPI (js/api.js): a mock server now, a real backend later (docs/API.md). */
(function () {
  "use strict";

  var CFG = window.DESK_CONFIG || {};
  var API = window.DeskAPI;
  var html = document.documentElement;
  var lang = html.lang === "bg" ? "bg" : "en";
  var reduceMotion = window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches;
  function $(id) { return document.getElementById(id); }
  var D = JSON.parse($("deskData").textContent);

  var T = {
    bg: {
      locale: "bg-BG", mapTitle: "Карта на кафенето", today: "Днес", tomorrow: "Утре", h: "ч", seats: "места", people: "души",
      openNow: "Отворено до {t}", closedOpens: "Затворено · отваря в {t}", closedTomorrow: "Затворено · отваря утре в {t}",
      planCap: "<b>{name}</b> · {seats} {unit} · {rate} на час · дневна цена {day}", perHour: "{r} / ч", freeToday: "{t}", freeTomorrow: "утре {t}", freeNone: "няма",
      slotsHint: "Свободни начални часове: {n}.", noSlots: "Няма свободно място за толкова часа този ден. Опитай по-малко часове или друг ден.", availError: "Не успяхме да проверим часовете. Опитай пак.", checking: "Проверяваме свободните часове…",
      hrsHint: "{n} ч", coffeeIn: "напитка", coffeeIn2: "две напитки", bottomless: "кафе без дъно", none: "–", dayPass: "дневна цена", rateLine: "{r} × {n} ч", saveLine: "С дневната цена спестяваш {s}.",
      errTime: "Избери ден и начален час.", errName: "Въведи име и телефон.", errTaken: "Съжаляваме, мястото току-що беше заето. Избери друг час.", errInvalid: "Провери данните и опитай пак.", errGeneric: "Нещо се обърка. Опитай пак или ни се обади.",
      sending: "Изпращане…", demoLine: "Демо режим: резервациите се пазят само в този браузър и нищо не се изпраща.",
      doneH: "Мястото е запазено", doneRef: "Номер", statusPending: "Чака потвърждение", doneNext: "Очакваме те в избрания час. Плащаш на място. Запази номера.",
      doneDemo: "Демо режим: нищо не беше изпратено. Резервацията е записана само в този браузър.", adminLink: "Виж я в демо админ панела", again: "Нова резервация",
      lines: { when: "Кога", zone: "Място", total: "Общо", name: "Име", needs: "Нужди" }, svc: "{zone} за {n} ч", peopleOpt: "{n} души", person: "1 човек"
    },
    en: {
      locale: "en-GB", mapTitle: "Map of the café", today: "Today", tomorrow: "Tomorrow", h: "h", seats: "seats", people: "people",
      openNow: "Open until {t}", closedOpens: "Closed · opens at {t}", closedTomorrow: "Closed · opens tomorrow at {t}",
      planCap: "<b>{name}</b> · {seats} {unit} · {rate} per hour · day price {day}", perHour: "{r} / h", freeToday: "{t}", freeTomorrow: "tomorrow {t}", freeNone: "none",
      slotsHint: "{n} free start times.", noSlots: "No free seat for that many hours on this day. Try fewer hours or another day.", availError: "We could not check the times. Please try again.", checking: "Checking free times…",
      hrsHint: "{n} h", coffeeIn: "a drink", coffeeIn2: "two drinks", bottomless: "bottomless filter", none: "–", dayPass: "day price", rateLine: "{r} × {n} h", saveLine: "The day price saves you {s}.",
      errTime: "Please pick a day and a start time.", errName: "Please enter your name and phone.", errTaken: "Sorry, that seat was just taken. Please choose another time.", errInvalid: "Please check your details and try again.", errGeneric: "Something went wrong. Please try again or call us.",
      sending: "Sending…", demoLine: "Demo mode: bookings are kept in this browser only and nothing is sent.",
      doneH: "Seat booked", doneRef: "Reference", statusPending: "Waiting for confirmation", doneNext: "We look forward to seeing you. You pay on site. Keep your reference.",
      doneDemo: "Demo mode: nothing was sent. The booking is saved only in this browser.", adminLink: "See it in the demo back office", again: "New booking",
      lines: { when: "When", zone: "Seat", total: "Total", name: "Name", needs: "Needs" }, svc: "{zone} for {n} h", peopleOpt: "{n} people", person: "1 person"
    }
  }[lang];

  /* ---------- Helpers ---------- */
  function pad(n) { return (n < 10 ? "0" : "") + n; }
  function ymd(d) { return d.getFullYear() + "-" + pad(d.getMonth() + 1) + "-" + pad(d.getDate()); }
  function toDate(v) { var p = v.split("-"); return new Date(+p[0], +p[1] - 1, +p[2]); }
  function addDays(d, n) { return new Date(d.getFullYear(), d.getMonth(), d.getDate() + n); }
  function el(tag, cls, text) { var n = document.createElement(tag); if (cls) n.className = cls; if (text !== undefined) n.textContent = text; return n; }
  function fill(s, o) { return s.replace(/\{(\w+)\}/g, function (m, k) { return o[k] !== undefined ? o[k] : m; }); }
  function eur(n) { return lang === "bg" ? n.toFixed(2).replace(".", ",") + " €" : "€" + n.toFixed(2); }
  function shortDate(v) { return toDate(v).toLocaleDateString(T.locale, { weekday: "short", day: "numeric", month: "short" }); }
  function scrollToEl(n) { n.scrollIntoView({ behavior: reduceMotion ? "auto" : "smooth", block: "start" }); }
  function hoursFor(d) { var g = d.getDay(); return g === 0 || g === 6 ? CFG.hours.weekend : CFG.hours.weekday; }
  function toMin(h) { var p = h.split(":"); return +p[0] * 60 + +p[1]; }
  function toHHMM(m) { return pad(Math.floor(m / 60)) + ":" + pad(m % 60); }

  /* ---------- Colour scheme (skin) ---------- */
  var SKINS = ["paper", "ultra", "sage", "charcoal", "plum"];
  var skinBtns = document.querySelectorAll(".sw[data-skin]");
  var skinName = $("skinName");
  var animTimer;
  function setSkin(skin, save) {
    if (SKINS.indexOf(skin) === -1) skin = "paper";
    if (save && !reduceMotion) { html.classList.add("skin-anim"); clearTimeout(animTimer); animTimer = setTimeout(function () { html.classList.remove("skin-anim"); }, 500); }
    html.dataset.skin = skin;
    skinBtns.forEach(function (b) {
      var on = b.dataset.skin === skin;
      b.setAttribute("aria-pressed", on ? "true" : "false");
      if (on && skinName) skinName.textContent = b.getAttribute("aria-label");
    });
    var meta = document.querySelector('meta[name="theme-color"]');
    if (meta) meta.content = getComputedStyle(html).getPropertyValue("--bg").trim() || meta.content;
    if (save) { try { localStorage.setItem("deskSkin", skin); } catch (e) {} }
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

  /* ---------- State ---------- */
  var zoneBy = {}; D.zones.forEach(function (z) { zoneBy[z.id] = z; });
  var DAYS = [0, 1, 2, 3, 4, 5, 6].map(function (i) { return ymd(addDays(new Date(), i)); });
  var state = { zone: "window", hours: 3, date: "", time: "" };
  var form = $("bookForm");

  /* ---------- Floor plan ---------- */
  var zoneBtns = document.querySelectorAll(".zone");
  function syncPlan(selected) {
    zoneBtns.forEach(function (b) { b.setAttribute("aria-pressed", selected && b.dataset.zone === state.zone ? "true" : "false"); });
  }
  zoneBtns.forEach(function (b) {
    b.addEventListener("click", function () {
      var z = zoneBy[b.dataset.zone]; state.zone = z.id;
      var radio = form.querySelector('input[name="zone"][value="' + z.id + '"]'); radio.checked = true;
      syncPlan(true);
      $("planCap").innerHTML = fill(T.planCap, { name: z.name, seats: z.seats, unit: z.id === "meeting" ? T.people : T.seats, rate: eur(z.rate), day: eur(z.day) });
      $("planGo").hidden = false; refresh();
    });
  });
  $("planGo").addEventListener("click", function () { refresh(); });
  form.addEventListener("change", function (e) {
    if (e.target.name === "zone") { state.zone = e.target.value; syncPlan(!$("planGo").hidden); refresh(); }
  });

  /* ---------- Hours and price ---------- */
  function price() { var z = zoneBy[state.zone], raw = z.rate * state.hours; return { raw: raw, total: Math.min(raw, z.day), capped: raw > z.day }; }
  function endTime() { return state.time ? toHHMM(toMin(state.time) + state.hours * 60) : ""; }
  function included() {
    var out = [];
    if (state.hours >= D.coffeeFrom) out.push(state.zone === "meeting" ? T.coffeeIn2 : T.coffeeIn);
    if (state.hours >= 4) out.push(T.bottomless);
    return out.length ? out.join(" + ") : T.none;
  }
  function needsList() { return Array.prototype.slice.call(form.querySelectorAll('input[name="need"]:checked')).map(function (c) { return c.dataset.name; }); }
  function render() {
    var z = zoneBy[state.zone], p = price();
    $("hOut").textContent = state.hours;
    $("hrsHint").textContent = state.hours >= D.coffeeFrom ? included() : "";
    $("peopleRow").hidden = state.zone !== "meeting";
    $("slipZone").textContent = z.name;
    $("slWhen").textContent = state.date ? shortDate(state.date) + (state.time ? ", " + state.time + "–" + endTime() : "") : T.none;
    $("slLen").textContent = state.hours + " " + T.h;
    $("slRate").textContent = p.capped ? T.dayPass + " " + eur(z.day) : fill(T.rateLine, { r: eur(z.rate), n: state.hours });
    $("slExtra").textContent = included();
    $("slTotal").textContent = eur(p.total);
    var sv = $("slSave"); sv.hidden = !p.capped; if (p.capped) sv.textContent = fill(T.saveLine, { s: eur(p.raw - p.total) });
  }
  var availTimer;
  function refresh() {
    render();
    clearTimeout(availTimer);
    availTimer = setTimeout(function () { if (state.date) pickDay(state.date, true); }, 200);
  }
  $("hMinus").addEventListener("click", function () { if (state.hours > 1) { state.hours--; refresh(); } });
  $("hPlus").addEventListener("click", function () { if (state.hours < D.maxHours) { state.hours++; refresh(); } });
  var people = $("f-people");
  for (var n = 1; n <= 6; n++) { var o = el("option", "", n === 1 ? T.person : fill(T.peopleOpt, { n: n })); o.value = n; if (n === 4) o.selected = true; people.appendChild(o); }
  form.addEventListener("input", function () { render(); });

  /* ---------- Day and time ---------- */
  var dayBox = $("dchips"), timeBox = $("tchips"), slotHint = $("slotHint");
  function dayLabel(v, i) { return i === 0 ? T.today : i === 1 ? T.tomorrow : toDate(v).toLocaleDateString(T.locale, { weekday: "short", day: "numeric" }); }
  function renderDays() {
    dayBox.textContent = "";
    DAYS.forEach(function (v, i) {
      var b = el("button", "dchip", dayLabel(v, i)); b.type = "button"; b.setAttribute("role", "radio");
      b.setAttribute("aria-checked", state.date === v ? "true" : "false");
      b.addEventListener("click", function () { state.time = ""; pickDay(v, false); render(); });
      dayBox.appendChild(b);
    });
  }
  function pickDay(v, keep) {
    state.date = v; renderDays(); timeBox.textContent = ""; slotHint.textContent = T.checking;
    return API.availability(v, state.hours * 60).then(function (r) {
      if (state.date !== v) return;
      if (state.time && r.slots.indexOf(state.time) === -1) state.time = "";
      showSlots(r); render();
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
        render();
      });
      timeBox.appendChild(b);
    });
  }
  renderDays(); render();
  (function find(i) {
    if (i >= DAYS.length) { pickDay(DAYS[0], false); return; }
    API.availability(DAYS[i], 60).then(function (r) {
      if (i === 0 || r.slots.length) {
        $("nextFree").textContent = r.slots.length ? (i === 0 ? fill(T.freeToday, { t: r.slots[0] }) : fill(T.freeTomorrow, { t: r.slots[0] })) : T.freeNone;
      }
      if (r.slots.length) { state.date = DAYS[i]; renderDays(); API.availability(DAYS[i], state.hours * 60).then(function (r2) { showSlots(r2); render(); }); }
      else find(i + 1);
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
    var z = zoneBy[state.zone], p = price(), needs = needsList();
    var ppl = state.zone === "meeting" ? +people.value : 1;
    var summary = z.name + " · " + state.hours + " " + T.h + " · " + state.time + "–" + endTime() + (state.zone === "meeting" ? " · " + (ppl === 1 ? T.person : fill(T.peopleOpt, { n: ppl })) : "") + (needs.length ? " · " + needs.join(", ") : "");
    var payload = {
      name: name, phone: phone, service: fill(T.svc, { zone: z.name, n: state.hours }), date: state.date, time: state.time, durationMinutes: state.hours * 60, fulfil: "pickup", lang: lang,
      message: form.elements.msg.value.trim(),
      plan: { summary: summary, zone: state.zone, hours: state.hours, total: p.total, people: ppl, needs: needs, included: included() }
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
    var rows = [[T.lines.when, shortDate(p.date) + ", " + p.time + "–" + toHHMM(toMin(p.time) + p.durationMinutes)], [T.lines.zone, p.plan.summary.split(" · ")[0]], [T.lines.total, eur(p.plan.total)]];
    if (p.plan.needs.length) rows.push([T.lines.needs, p.plan.needs.join(", ")]);
    rows.push([T.lines.name, p.name]);
    rows.forEach(function (r) { dl.appendChild(el("dt", "", r[0])); dl.appendChild(el("dd", "", r[1])); });
    doneBox.appendChild(dl);
    doneBox.appendChild(el("p", "", T.doneNext));
    if (API.mode === "demo") doneBox.appendChild(el("p", "demo-note", T.doneDemo));
    var act = el("div", "done-actions");
    if (API.mode === "demo") { var a = el("a", "btn btn-line", T.adminLink); a.href = (lang === "bg" ? "" : "../") + "admin.html" + (lang === "en" ? "?lang=en" : ""); act.appendChild(a); }
    var again = el("button", "btn btn-main", T.again); again.type = "button";
    again.addEventListener("click", function () { form.reset(); form.hidden = false; doneBox.hidden = true; state.time = ""; state.zone = "window"; state.hours = 3; refresh(); pickDay(state.date || DAYS[0], false); scrollToEl($("book")); });
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

  /* ---------- Book bar on phones: shown after the first screen, hidden while the form is on screen ---------- */
  if ("IntersectionObserver" in window) {
    var seen = { hero: true, book: false }, bar = $("bar");
    var upd = function () { bar.classList.toggle("show", !seen.hero && !seen.book); };
    new IntersectionObserver(function (es) { seen.hero = es[0].isIntersecting; upd(); }).observe(document.querySelector(".hero"));
    new IntersectionObserver(function (es) { seen.book = es[0].isIntersecting; upd(); }, { threshold: .08 }).observe($("book"));
  }

  /* ---------- Scroll reveal ---------- */
  if (html.classList.contains("js-reveal")) {
    var targets = document.querySelectorAll(".sec-head, .pl, .step, .amen li, .events li, .comm-photos, .visit-copy, .visit-side");
    var io = new IntersectionObserver(function (es) { es.forEach(function (x) { if (x.isIntersecting) { x.target.classList.add("in"); io.unobserve(x.target); } }); }, { rootMargin: "0px 0px -8% 0px" });
    targets.forEach(function (t, i) { t.classList.add("rv"); t.style.setProperty("--d", (i % 3) * 0.06 + "s"); io.observe(t); });
  }
})();
