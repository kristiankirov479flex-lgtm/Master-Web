/* Bashta (restaurant design 2, a traditional tavern with online ordering): page behaviour.
   Colour schemes, menu button, today's hours, the order (dishes to an order list, delivery or pick-up, a day and a free time, details) and the map.
   The order talks to BashtaAPI (js/api.js): a mock server now, a real backend later (docs/API.md). */
(function () {
  "use strict";

  var CFG = window.BASHTA_CONFIG || {};
  var API = window.BashtaAPI;
  var html = document.documentElement;
  var lang = html.lang === "bg" ? "bg" : "en";
  var reduceMotion = window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches;
  function $(id) { return document.getElementById(id); }
  var D = JSON.parse($("bashtaData").textContent);
  var SLOT = CFG.slotMinutes || 30;

  var T = {
    bg: {
      locale: "bg-BG", mapTitle: "Карта на механата", today: "Днес", tomorrow: "Утре", pick: "Избери час", items: "{n} бр.",
      hintDeliver: "Минимална поръчка за доставка: {min}. Доставка {fee}, безплатна над {free}.", hintPickup: "Вземането е безплатно. Готови сме в избрания час.", free: "безплатна",
      slotsHint: "Свободни часове: {n}.", noSlots: "Няма свободни часове този ден. Избери друг ден.", availError: "Не успяхме да проверим часовете. Опитай пак.", checking: "Проверяваме свободните часове…",
      errItems: "Добави поне едно ястие.", errMin: "Минималната поръчка за доставка е {min}.", errAddr: "Въведи адрес за доставка.", errTime: "Избери ден и час.", errName: "Въведи име и телефон.", errTaken: "Съжаляваме, този час току-що беше зает. Избери друг.", errInvalid: "Провери данните и опитай пак.", errGeneric: "Нещо се обърка. Опитай пак или ни се обади.",
      sending: "Изпращане…", demoLine: "Демо режим: поръчките се пазят само в този браузър и нищо не се изпраща.",
      doneH: "Поръчката е приета", doneRef: "Номер", statusPending: "Чака потвърждение", doneNext: "Ще ти се обадим, ако трябва да потвърдим нещо. Плащаш при получаване. Запази номера.",
      doneDemo: "Демо режим: нищо не беше изпратено. Поръчката е записана само в този браузър.", adminLink: "Виж я в демо админ панела", again: "Нова поръчка",
      lines: { when: "Кога", order: "Поръчка", how: "Как", total: "Общо", name: "Име" }, deliver: "Доставка", pickup: "Вземане от механата", svcDeliver: "Поръчка за доставка", svcPickup: "Поръчка за вземане", plus: "Още един", minus: "Един по-малко", count: "брой"
    },
    en: {
      locale: "en-GB", mapTitle: "Map of the tavern", today: "Today", tomorrow: "Tomorrow", pick: "Choose a time", items: "{n} items",
      hintDeliver: "Minimum order for delivery: {min}. Delivery {fee}, free over {free}.", hintPickup: "Pick-up is free. We are ready at the time you choose.", free: "free",
      slotsHint: "{n} free times.", noSlots: "No free times on this day. Please pick another day.", availError: "We could not check the times. Please try again.", checking: "Checking free times…",
      errItems: "Please add at least one dish.", errMin: "The minimum order for delivery is {min}.", errAddr: "Please enter a delivery address.", errTime: "Please pick a day and a time.", errName: "Please enter your name and phone.", errTaken: "Sorry, that time was just taken. Please choose another.", errInvalid: "Please check your details and try again.", errGeneric: "Something went wrong. Please try again or call us.",
      sending: "Sending…", demoLine: "Demo mode: orders are kept in this browser only and nothing is sent.",
      doneH: "Order received", doneRef: "Reference", statusPending: "Waiting for confirmation", doneNext: "We will call you if we need to confirm anything. You pay on receipt. Keep your reference.",
      doneDemo: "Demo mode: nothing was sent. The order is saved only in this browser.", adminLink: "See it in the demo back office", again: "New order",
      lines: { when: "When", order: "Order", how: "How", total: "Total", name: "Name" }, deliver: "Delivery", pickup: "Pick up at the tavern", svcDeliver: "Delivery order", svcPickup: "Pick-up order", plus: "One more", minus: "One fewer", count: "count"
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
  var SKINS = ["oak", "olive", "indigo", "night", "pomegranate"];
  var skinBtns = document.querySelectorAll(".sw[data-skin]");
  var skinName = $("skinName");
  var animTimer;
  function setSkin(skin, save) {
    if (SKINS.indexOf(skin) === -1) skin = "oak";
    if (save && !reduceMotion) { html.classList.add("skin-anim"); clearTimeout(animTimer); animTimer = setTimeout(function () { html.classList.remove("skin-anim"); }, 400); }
    html.dataset.skin = skin;
    skinBtns.forEach(function (b) {
      var on = b.dataset.skin === skin;
      b.setAttribute("aria-pressed", on ? "true" : "false");
      if (on && skinName) skinName.textContent = b.getAttribute("aria-label");
    });
    var meta = document.querySelector('meta[name="theme-color"]');
    if (meta) meta.content = getComputedStyle(html).getPropertyValue("--bg").trim() || meta.content;
    if (save) { try { localStorage.setItem("bashtaSkin", skin); } catch (e) {} }
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

  /* ---------- The order ---------- */
  var byId = {}; D.menu.forEach(function (m) { byId[m.id] = m; });
  var lines = [];   /* { id, n } */
  var form = $("orderForm");
  function fulfil() { return form.querySelector('input[name="fulfil"]:checked').value; }
  function sub() { return lines.reduce(function (s, l) { return s + byId[l.id].price * l.n; }, 0); }
  function fee() { return fulfil() === "delivery" && sub() > 0 && sub() < D.free ? D.fee : 0; }
  function total() { return sub() + fee(); }
  function count() { return lines.reduce(function (s, l) { return s + l.n; }, 0); }
  function summary() { return lines.map(function (l) { return l.n + " × " + byId[l.id].name; }).join(", "); }

  function render() {
    var ul = $("lines"); ul.textContent = "";
    lines.forEach(function (l, idx) {
      var m = byId[l.id], li = el("li", "line");
      li.appendChild(el("b", "", m.name)); li.appendChild(el("span", "line-p", eur(m.price * l.n)));
      var st = el("div", "step");
      var minus = el("button", "", "−"); minus.type = "button"; minus.setAttribute("aria-label", T.minus + ": " + m.name);
      var plus = el("button", "", "+"); plus.type = "button"; plus.setAttribute("aria-label", T.plus + ": " + m.name);
      var out = el("span", "", String(l.n)); out.setAttribute("aria-label", T.count);
      minus.addEventListener("click", function () { l.n--; if (l.n < 1) lines.splice(idx, 1); render(); });
      plus.addEventListener("click", function () { l.n++; render(); });
      st.appendChild(minus); st.appendChild(out); st.appendChild(plus); li.appendChild(st); ul.appendChild(li);
    });
    $("trayEmpty").hidden = lines.length > 0;
    $("sums").hidden = lines.length === 0;
    $("sumSub").textContent = eur(sub());
    $("sumFee").textContent = fulfil() === "delivery" ? (fee() ? eur(fee()) : T.free) : T.free;
    $("sumTotal").textContent = eur(total());
    $("addrRow").hidden = fulfil() !== "delivery";
    $("howHint").textContent = fulfil() === "delivery" ? fill(T.hintDeliver, { min: eur(D.min), fee: eur(D.fee), free: eur(D.free) }) : T.hintPickup;
    var perId = {}; lines.forEach(function (l) { perId[l.id] = l.n; });
    document.querySelectorAll(".add").forEach(function (b) { var n = perId[b.dataset.id] || 0, bd = b.querySelector(".add-n"); bd.hidden = !n; bd.textContent = n ? "×" + n : ""; });
    var bar = $("bar");
    if (lines.length) { $("barTxt").textContent = fill(T.items, { n: count() }) + " · " + eur(total()); bar.hidden = false; } else bar.hidden = true;
  }
  document.querySelectorAll(".add").forEach(function (b) {
    b.addEventListener("click", function () {
      var l = lines.filter(function (x) { return x.id === b.dataset.id; })[0];
      if (l) l.n++; else lines.push({ id: b.dataset.id, n: 1 });
      render();
    });
  });
  form.addEventListener("change", function (e) { if (e.target.name === "fulfil") render(); });
  if ("IntersectionObserver" in window) {
    new IntersectionObserver(function (es) { $("bar").style.visibility = es[0].isIntersecting ? "hidden" : ""; }, { threshold: .25 }).observe($("tray"));
  }

  /* ---------- Day and time ---------- */
  var dateSel = $("f-date"), timeSel = $("f-time"), hint = $("timeHint");
  var DAYS = [0, 1, 2].map(function (i) { return ymd(addDays(new Date(), i)); });
  DAYS.forEach(function (v, i) { dateSel.appendChild(new Option((i === 0 ? T.today : i === 1 ? T.tomorrow : toDate(v).toLocaleDateString(T.locale, { weekday: "long" })) + " · " + toDate(v).toLocaleDateString(T.locale, { day: "numeric", month: "short" }), v)); });
  function setTimes(r) {
    timeSel.textContent = "";
    if (!r.slots.length) { hint.textContent = T.noSlots; return; }
    timeSel.appendChild(new Option(T.pick, ""));
    r.slots.forEach(function (s) { timeSel.appendChild(new Option(s, s)); });
    hint.textContent = fill(T.slotsHint, { n: r.slots.length });
  }
  function loadTimes() {
    var v = dateSel.value; hint.textContent = T.checking;
    return API.availability(v, SLOT).then(function (r) { if (dateSel.value === v) setTimes(r); }).catch(function () { hint.textContent = T.availError; });
  }
  dateSel.addEventListener("change", loadTimes);
  (function find(i) {
    if (i >= DAYS.length) { dateSel.value = DAYS[0]; loadTimes(); return; }
    API.availability(DAYS[i], SLOT).then(function (r) { if (r.slots.length) { dateSel.value = DAYS[i]; setTimes(r); } else find(i + 1); }).catch(function () { loadTimes(); });
  })(0);
  render();

  /* ---------- Send ---------- */
  var errBox = $("orError"), sendBtn = $("send"), doneBox = $("done");
  function showError(msg) { errBox.textContent = msg; errBox.hidden = false; }
  if (API.mode === "demo") { var dn = $("demoNote"); dn.textContent = T.demoLine; dn.hidden = false; }
  form.addEventListener("submit", function (e) {
    e.preventDefault(); errBox.hidden = true;
    if (!lines.length) return showError(T.errItems);
    var how = fulfil(), addr = form.elements.address.value.trim();
    if (how === "delivery" && sub() < D.min) return showError(fill(T.errMin, { min: eur(D.min) }));
    if (how === "delivery" && !addr) { form.elements.address.focus(); return showError(T.errAddr); }
    if (!dateSel.value || !timeSel.value) return showError(T.errTime);
    var name = form.elements.name.value.trim(), phone = form.elements.phone.value.trim();
    if (!name || phone.replace(/\D/g, "").length < 6) return showError(T.errName);
    var payload = {
      name: name, phone: phone, service: how === "delivery" ? T.svcDeliver : T.svcPickup, date: dateSel.value, time: timeSel.value, durationMinutes: SLOT,
      fulfil: how, address: how === "delivery" ? addr : "", message: form.elements.msg.value.trim(), lang: lang,
      plan: { summary: summary(), total: Math.round(total() * 100) / 100, items: lines.map(function (l) { return { id: l.id, n: l.n }; }) }
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
    [[T.lines.when, longDate(p.date) + ", " + p.time], [T.lines.order, p.plan.summary], [T.lines.how, p.fulfil === "delivery" ? T.deliver + ": " + p.address : T.pickup], [T.lines.total, eur(p.plan.total)], [T.lines.name, p.name]]
      .forEach(function (r) { dl.appendChild(el("dt", "", r[0])); dl.appendChild(el("dd", "", r[1])); });
    doneBox.appendChild(dl);
    doneBox.appendChild(el("p", "", T.doneNext));
    if (API.mode === "demo") doneBox.appendChild(el("p", "demo-note", T.doneDemo));
    var act = el("div", "done-actions");
    if (API.mode === "demo") { var a = el("a", "btn btn-line", T.adminLink); a.href = (lang === "bg" ? "" : "../") + "admin.html" + (lang === "en" ? "?lang=en" : ""); act.appendChild(a); }
    var again = el("button", "btn btn-main", T.again); again.type = "button";
    again.addEventListener("click", function () { lines = []; form.reset(); form.hidden = false; doneBox.hidden = true; render(); loadTimes(); scrollToEl($("order")); });
    act.appendChild(again); doneBox.appendChild(act);
    doneBox.focus(); scrollToEl($("tray"));
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
