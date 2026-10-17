/* Ember Roasters (café design 2): page behaviour.
   Colour schemes, menu, coffee filter and choice, the bag builder (size, grind, quantity, subscription, delivery or pick-up,
   a day and a free time, a live total on the checkout bar), the brew calculator and the map.
   The order talks to EmberAPI (js/api.js): a mock server now, a real backend later (docs/API.md). */
(function () {
  "use strict";

  var CFG = window.EMBER_CONFIG || {};
  var API = window.EmberAPI;
  var html = document.documentElement;
  var lang = html.lang === "bg" ? "bg" : "en";
  var reduceMotion = window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches;
  function $(id) { return document.getElementById(id); }
  var D = JSON.parse($("emberData").textContent);
  var SLOT = CFG.slotMinutes || 30;

  var T = {
    bg: {
      locale: "bg-BG", mapTitle: "Карта на пържилнята", today: "Днес", tomorrow: "Утре", gram: "г", kg: "кг",
      bagEmpty: "Торбата е празна", bags: "{n} бр. · {t}", lastToday: "днес", lastDay: "{d}",
      picked: "{name} · {size} · {grind}", coNone: "Торбата е празна", coLine: "{n} × {name}, {size}, {grind}",
      subNote: "{freq}, −8 %", feeNote: "Доставка {fee}", freeNote: "безплатна доставка", pickupNote: "вземане без такса", feeFree: "Безплатна над {n} €", feeLine: "Доставка: {fee}",
      whenDeliver: "Кога да доставим?", whenPickup: "Кога идваш да вземеш?",
      slotsHint: "Свободни часове: {n}. Избери кога.", noSlots: "Няма свободни часове този ден. Избери друг ден.", availError: "Не успяхме да проверим часовете. Опитай пак.",
      errCoffee: "Избери кафе от списъка горе.", errAddr: "Въведи адрес за доставка.", errTime: "Избери ден и час.", errName: "Въведи име и телефон.", errTaken: "Съжаляваме, този час току-що беше зает. Избери друг.", errInvalid: "Провери данните и опитай пак.", errGeneric: "Нещо се обърка. Опитай пак или ни се обади.",
      sending: "Изпращане…", demoLine: "Демо режим: поръчките се пазят само в този браузър и нищо не се изпраща.",
      doneH: "Поръчката е приета", doneRef: "Номер", statusPending: "Чака потвърждение", doneNext: "Ще ти се обадим, за да потвърдим доставката. Плащаш при получаване. Запази номера.",
      doneDemo: "Демо режим: нищо не беше изпратено. Поръчката е записана само в този браузър.", adminLink: "Виж я в демо админ панела", again: "Нова поръчка",
      lines: { when: "Кога", order: "Поръчка", how: "Как", total: "Общо", name: "Име" }, deliver: "Доставка", pickup: "Вземане от пържилнята", svcOrder: "Кафе на зърна", svcSub: "Абонамент",
      checking: "Проверяваме свободните часове…", cupsLbl: "Чаши (по 250 мл)", doublesLbl: "Двойни еспресо", gramsOut: "{n} г", mlOut: "{n} мл", espOut: "{n} г в чашата"
    },
    en: {
      locale: "en-GB", mapTitle: "Map of the roastery", today: "Today", tomorrow: "Tomorrow", gram: "g", kg: "kg",
      bagEmpty: "Your bag is empty", bags: "{n} · {t}", lastToday: "today", lastDay: "{d}",
      picked: "{name} · {size} · {grind}", coNone: "Your bag is empty", coLine: "{n} × {name}, {size}, {grind}",
      subNote: "{freq}, −8%", feeNote: "Delivery {fee}", freeNote: "free delivery", pickupNote: "pick-up is free", feeFree: "Free over €{n}", feeLine: "Delivery: {fee}",
      whenDeliver: "When should we deliver?", whenPickup: "When will you collect?",
      slotsHint: "{n} free times. Choose when.", noSlots: "No free times on this day. Please pick another day.", availError: "We could not check the times. Please try again.",
      errCoffee: "Please choose a coffee from the list above.", errAddr: "Please enter a delivery address.", errTime: "Please pick a day and a time.", errName: "Please enter your name and phone.", errTaken: "Sorry, that time was just taken. Please choose another.", errInvalid: "Please check your details and try again.", errGeneric: "Something went wrong. Please try again or call us.",
      sending: "Sending…", demoLine: "Demo mode: orders are kept in this browser only and nothing is sent.",
      doneH: "Order received", doneRef: "Reference", statusPending: "Waiting for confirmation", doneNext: "We will call you to confirm the delivery. You pay on receipt. Keep your reference.",
      doneDemo: "Demo mode: nothing was sent. The order is saved only in this browser.", adminLink: "See it in the demo back office", again: "New order",
      lines: { when: "When", order: "Order", how: "How", total: "Total", name: "Name" }, deliver: "Delivery", pickup: "Pick up at the roastery", svcOrder: "Coffee beans", svcSub: "Subscription",
      checking: "Checking free times…", cupsLbl: "Cups (250 ml each)", doublesLbl: "Double espressos", gramsOut: "{n} g", mlOut: "{n} ml", espOut: "{n} g in the cup"
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

  /* ---------- Colour scheme (skin) ---------- */
  var SKINS = ["ember", "paper", "moss", "midnight", "blush"];
  var skinBtns = document.querySelectorAll(".sw[data-skin]");
  var skinName = $("skinName");
  var animTimer;
  function setSkin(skin, save) {
    if (SKINS.indexOf(skin) === -1) skin = "ember";
    if (save && !reduceMotion) { html.classList.add("skin-anim"); clearTimeout(animTimer); animTimer = setTimeout(function () { html.classList.remove("skin-anim"); }, 500); }
    html.dataset.skin = skin;
    skinBtns.forEach(function (b) {
      var on = b.dataset.skin === skin;
      b.setAttribute("aria-pressed", on ? "true" : "false");
      if (on && skinName) skinName.textContent = b.getAttribute("aria-label");
    });
    var meta = document.querySelector('meta[name="theme-color"]');
    if (meta) meta.content = getComputedStyle(html).getPropertyValue("--bg").trim() || meta.content;
    if (save) { try { localStorage.setItem("emberSkin", skin); } catch (e) {} }
  }
  skinBtns.forEach(function (b) { b.addEventListener("click", function () { setSkin(b.dataset.skin, true); }); });
  setSkin(html.dataset.skin, false);

  /* ---------- Menu (mobile) ---------- */
  var burger = $("burger"), nav = $("nav");
  function setMenu(open) { nav.classList.toggle("open", open); burger.setAttribute("aria-expanded", open ? "true" : "false"); }
  burger.addEventListener("click", function () { setMenu(!nav.classList.contains("open")); });
  nav.addEventListener("click", function (e) { if (e.target.closest("a")) setMenu(false); });
  document.addEventListener("keydown", function (e) { if (e.key === "Escape" && nav.classList.contains("open")) { setMenu(false); burger.focus(); } });

  /* ---------- Hours and the last roast day ---------- */
  function hoursFor(d) { var g = d.getDay(); return g === 0 || g === 6 ? CFG.hours.weekend : CFG.hours.weekday; }
  (function () {
    var now = new Date(), g = now.getDay(), key = g === 0 || g === 6 ? "we" : "wd";
    document.querySelectorAll("#hours [data-hrs]").forEach(function (r) { r.classList.toggle("today", r.dataset.hrs === key); });
    for (var i = 0; i < 7; i++) {
      var d = addDays(now, -i);
      if (D.roastDays.indexOf(d.getDay()) > -1) {
        $("lastRoast").textContent = i === 0 ? T.lastToday : d.toLocaleDateString(T.locale, { weekday: "long", day: "numeric", month: "short" });
        return;
      }
    }
  })();

  /* ---------- Coffee filter and choice ---------- */
  var byId = {}; D.coffees.forEach(function (c) { byId[c.id] = c; });
  var methodBtns = document.querySelectorAll("#methods .chip");
  methodBtns.forEach(function (b) {
    b.addEventListener("click", function () {
      methodBtns.forEach(function (x) { x.setAttribute("aria-pressed", x === b ? "true" : "false"); });
      var m = b.dataset.method;
      document.querySelectorAll(".coffee").forEach(function (c) { c.hidden = !(m === "all" || c.dataset.method === m || c.dataset.method === "both"); });
    });
  });
  var state = { coffee: "", size: "250", qty: 1, freq: "once", fulfil: "delivery", date: "", time: "" };
  document.querySelectorAll(".choose").forEach(function (b) {
    b.addEventListener("click", function () {
      state.coffee = b.dataset.id; render(); scrollToEl($("build"));
    });
  });

  /* ---------- The bag ---------- */
  var form = $("buildForm");
  function sizeOf(id) { return D.sizes.filter(function (s) { return s.id === id; })[0]; }
  function sizeLabel(id) { var s = sizeOf(id); return s.g >= 1000 ? (s.g / 1000) + " " + T.kg : s.g + " " + T.gram; }
  function unit() { var c = byId[state.coffee]; return c ? c.price * sizeOf(state.size).mult : 0; }
  function sub() { var s = unit() * state.qty; return state.freq === "once" ? s : s * (1 - D.subDiscount); }
  function fee() { return state.fulfil === "delivery" && sub() > 0 && sub() < D.freeFrom ? D.fee : 0; }
  function total() { return sub() + fee(); }
  function grindName() { return D.grinds[form.elements.grind.value]; }
  function summary() { var c = byId[state.coffee]; return state.qty + " × " + c.name + ", " + sizeLabel(state.size) + ", " + grindName().toLowerCase(); }

  function render() {
    var c = byId[state.coffee];
    document.querySelectorAll(".coffee").forEach(function (n) { n.classList.toggle("on", n.dataset.id === state.coffee); });
    document.querySelectorAll(".choose").forEach(function (b) { b.setAttribute("aria-pressed", b.dataset.id === state.coffee ? "true" : "false"); });
    var picked = $("picked");
    picked.classList.toggle("has", !!c);
    picked.textContent = c ? fill(T.picked, { name: c.name, size: sizeLabel(state.size), grind: grindName() }) : picked.dataset.none;
    document.querySelectorAll(".size-p").forEach(function (n) { var s = sizeOf(n.dataset.size); n.textContent = c ? eur(c.price * s.mult) : ""; });
    $("qOut").textContent = state.qty;
    $("feeNote").textContent = sub() >= D.freeFrom ? T.freeNote : fill(T.feeFree, { n: D.freeFrom }) + " · " + fill(T.feeNote, { fee: eur(D.fee) });
    $("addrRow").hidden = state.fulfil !== "delivery";
    $("whenH").textContent = state.fulfil === "delivery" ? T.whenDeliver : T.whenPickup;
    var line = $("coLine"), subl = $("coSub");
    if (c) {
      line.textContent = fill(T.coLine, { n: state.qty, name: c.name, size: sizeLabel(state.size), grind: grindName().toLowerCase() });
      var bits = [];
      if (state.freq !== "once") bits.push(fill(T.subNote, { freq: D.freqs[state.freq] }));
      bits.push(state.fulfil === "delivery" ? (fee() ? fill(T.feeLine, { fee: eur(fee()) }) : T.freeNote) : T.pickupNote);
      subl.textContent = bits.join(" · ");
    } else { line.textContent = T.coNone; subl.textContent = ""; }
    $("coTotal").textContent = eur(total());
    $("bagN").textContent = c ? state.qty : 0;
    $("bagT").textContent = c ? eur(total()) : T.bagEmpty;
  }
  $("picked").dataset.none = $("picked").textContent;
  form.addEventListener("change", function (e) {
    var n = e.target;
    if (n.name === "size") state.size = n.value;
    else if (n.name === "freq") state.freq = n.value;
    else if (n.name === "fulfil") { state.fulfil = n.value; }
    render();
  });
  $("qMinus").addEventListener("click", function () { if (state.qty > 1) { state.qty--; render(); } });
  $("qPlus").addEventListener("click", function () { if (state.qty < 8) { state.qty++; render(); } });

  /* ---------- Day and time ---------- */
  var DAYS = [0, 1, 2, 3, 4, 5, 6].map(function (i) { return ymd(addDays(new Date(), i)); });
  var dayBox = $("dchips"), timeBox = $("tchips"), slotHint = $("slotHint");
  function dayLabel(v, i) { return i === 0 ? T.today : i === 1 ? T.tomorrow : toDate(v).toLocaleDateString(T.locale, { weekday: "short", day: "numeric" }); }
  function renderDays() {
    dayBox.textContent = "";
    DAYS.forEach(function (v, i) {
      var b = el("button", "dchip", dayLabel(v, i)); b.type = "button"; b.setAttribute("role", "radio");
      b.setAttribute("aria-checked", state.date === v ? "true" : "false");
      b.addEventListener("click", function () { state.time = ""; pickDay(v); });
      dayBox.appendChild(b);
    });
  }
  function pickDay(v) {
    state.date = v; renderDays(); timeBox.textContent = ""; slotHint.textContent = T.checking;
    return API.availability(v, SLOT).then(function (r) { if (state.date === v) showSlots(r); })
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
  renderDays();
  (function find(i) {
    if (i >= DAYS.length) { pickDay(DAYS[0]); return; }
    API.availability(DAYS[i], SLOT).then(function (r) { if (r.slots.length) { state.date = DAYS[i]; renderDays(); showSlots(r); } else find(i + 1); })
      .catch(function () { pickDay(DAYS[0]); });
  })(0);
  render();

  /* ---------- Send ---------- */
  var errBox = $("bkError"), sendBtn = $("bkSend"), doneBox = $("bkDone");
  function showError(msg) { errBox.textContent = msg; errBox.hidden = false; errBox.scrollIntoView({ block: "nearest" }); }
  if (API.mode === "demo") { var dn = $("demoNote"); dn.textContent = T.demoLine; dn.hidden = false; }
  form.addEventListener("submit", function (e) {
    e.preventDefault(); errBox.hidden = true;
    if (!state.coffee) return showError(T.errCoffee);
    var addr = form.elements.address.value.trim();
    if (state.fulfil === "delivery" && !addr) { form.elements.address.focus(); return showError(T.errAddr); }
    if (!state.date || !state.time) return showError(T.errTime);
    var name = form.elements.name.value.trim(), phone = form.elements.phone.value.trim();
    if (!name || phone.replace(/\D/g, "").length < 6) return showError(T.errName);
    var payload = {
      name: name, phone: phone, service: state.freq === "once" ? T.svcOrder : T.svcSub, date: state.date, time: state.time, durationMinutes: SLOT,
      fulfil: state.fulfil, address: state.fulfil === "delivery" ? addr : "", message: form.elements.msg.value.trim(), lang: lang,
      plan: { summary: summary() + (state.freq !== "once" ? " · " + D.freqs[state.freq] : ""), total: Math.round(total() * 100) / 100,
              items: [{ id: state.coffee, size: state.size, grind: form.elements.grind.value, qty: state.qty, freq: state.freq }] }
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
    [[T.lines.when, longDate(p.date) + ", " + p.time], [T.lines.order, p.plan.summary], [T.lines.how, p.fulfil === "delivery" ? T.deliver + ": " + p.address : T.pickup], [T.lines.total, eur(p.plan.total)], [T.lines.name, p.name]]
      .forEach(function (r) { dl.appendChild(el("dt", "", r[0])); dl.appendChild(el("dd", "", r[1])); });
    doneBox.appendChild(dl);
    doneBox.appendChild(el("p", "", T.doneNext));
    if (API.mode === "demo") doneBox.appendChild(el("p", "demo-note", T.doneDemo));
    var act = el("div", "done-actions");
    if (API.mode === "demo") { var a = el("a", "btn btn-line", T.adminLink); a.href = (lang === "bg" ? "" : "../") + "admin.html" + (lang === "en" ? "?lang=en" : ""); act.appendChild(a); }
    var again = el("button", "btn btn-main", T.again); again.type = "button";
    again.addEventListener("click", function () {
      form.reset(); form.hidden = false; doneBox.hidden = true; state.coffee = ""; state.size = "250"; state.qty = 1; state.freq = "once"; state.fulfil = "delivery"; state.time = "";
      render(); pickDay(state.date || DAYS[0]); scrollToEl($("beans"));
    });
    act.appendChild(again); doneBox.appendChild(act);
    doneBox.focus(); scrollToEl(doneBox);
  }

  /* ---------- Brew calculator ---------- */
  var calc = $("calc"), cups = $("c-cups");
  var mById = {}; D.methods.forEach(function (m) { mById[m.id] = m; });
  function brew() {
    var m = mById[$("c-method").value], n = +cups.value, esp = m.id === "espresso";
    $("cupsLbl").textContent = esp ? T.doublesLbl : T.cupsLbl;
    $("cupsOut").textContent = n;
    if (esp) { $("cCoffee").textContent = fill(T.gramsOut, { n: n * 18 }); $("cWater").textContent = fill(T.espOut, { n: n * 36 }); }
    else { var water = n * 250; $("cWater").textContent = fill(T.mlOut, { n: water }); $("cCoffee").textContent = fill(T.gramsOut, { n: Math.round(water / m.ratio) }); }
    $("cTemp").textContent = m.temp; $("cTime").textContent = m.time; $("cGrind").textContent = m.grind;
  }
  $("c-method").addEventListener("change", brew); cups.addEventListener("input", brew); brew();

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
    var targets = document.querySelectorAll(".sec-head, .coffee, .step, .calc, .brew-photos, .r-steps li, .r-ph, .visit-copy, .visit-side");
    var io = new IntersectionObserver(function (es) { es.forEach(function (x) { if (x.isIntersecting) { x.target.classList.add("in"); io.unobserve(x.target); } }); }, { rootMargin: "0px 0px -8% 0px" });
    targets.forEach(function (t, i) { t.classList.add("rv"); t.style.setProperty("--d", (i % 3) * 0.06 + "s"); io.observe(t); });
  }
})();
