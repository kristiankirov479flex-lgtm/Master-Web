/* VetDoma (home-visit vet design 2): page behaviour.
   Colour schemes, menu, today's hours, the visit request (species, reason, address and zone with a price estimate, a day and a free time that fits the visit, details) and the map.
   The request talks to VetDomaAPI (js/api.js): a mock server now, a real backend later (docs/API.md). */
(function () {
  "use strict";

  var CFG = window.VETDOMA_CONFIG || {};
  var API = window.VetDomaAPI;
  var html = document.documentElement;
  var lang = html.lang === "bg" ? "bg" : "en";
  var reduceMotion = window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches;
  function $(id) { return document.getElementById(id); }
  var D = JSON.parse($("vetdomaData").textContent);

  var T = {
    bg: {
      locale: "bg-BG",
      pick: "Избери час",
      min: "мин",
      slotsHint: "Свободни часове: {n}.",
      noSlots: "Няма свободни часове този ден. Избери друг ден.",
      availError: "Не успяхме да проверим часовете. Опитай пак.",
      checking: "Проверяваме свободните часове…",
      errTime: "Избери дата и час.",
      errTaken: "Съжаляваме, този час току-що беше зает. Избери друг.",
      errInvalid: "Провери данните и опитай пак.",
      errGeneric: "Нещо се обърка. Опитай пак или ни се обади.",
      sending: "Изпращане…",
      demoLine: "Демо режим: заявките се пазят само в този браузър и нищо не се изпраща.",
      doneRef: "Номер",
      statusPending: "Чака потвърждение",
      doneDemo: "Демо режим: нищо не беше изпратено. Заявката е записана само в този браузър.",
      adminLink: "Виж я в демо админ панела",
      mapTitle: "Карта на района",
      chooseDate: "Избери повод и дата, за да видиш свободните часове.",
      errName: "Въведи име и телефон.",
      doneH: "Посещението е заявено",
      doneNext: "Ще ти се обадим, за да потвърдим часа и да уточним адреса. Запази номера. Ако животното е в опасност, не чакай: обади се веднага.",
      again: "Ново посещение",
      estimate: "Пътуване {fee} + преглед {price} = {total}. Точната сума казваме по телефона.",
      fromw: "от",
      errAddr: "Напиши адреса, на който да дойдем.",
      lines: {"when": "Кога", "what": "Повод", "pet": "Животно", "where": "Адрес", "cost": "Ориентировъчно", "name": "Име"}
    },
    en: {
      locale: "en-GB",
      pick: "Choose a time",
      min: "min",
      slotsHint: "{n} free times.",
      noSlots: "No free times on this day. Please pick another day.",
      availError: "We could not check the times. Please try again.",
      checking: "Checking free times…",
      errTime: "Please pick a date and a time.",
      errTaken: "Sorry, that time was just taken. Please choose another.",
      errInvalid: "Please check your details and try again.",
      errGeneric: "Something went wrong. Please try again or call us.",
      sending: "Sending…",
      demoLine: "Demo mode: requests are kept in this browser only and nothing is sent.",
      doneRef: "Reference",
      statusPending: "Waiting for confirmation",
      doneDemo: "Demo mode: nothing was sent. The request is saved only in this browser.",
      adminLink: "See it in the demo back office",
      mapTitle: "Map of the area",
      chooseDate: "Choose a reason and a date to see the free times.",
      errName: "Please enter your name and phone.",
      doneH: "Visit requested",
      doneNext: "We will call you to confirm the time and the address. Keep your reference. If the animal is in danger, do not wait: call us right away.",
      again: "New visit",
      estimate: "Travel {fee} + visit {price} = {total}. We confirm the exact sum by phone.",
      fromw: "from",
      errAddr: "Please write the address we should come to.",
      lines: {"when": "When", "what": "Reason", "pet": "Pet", "where": "Address", "cost": "Estimate", "name": "Name"}
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
  function money(v) { return lang === "bg" ? v + " €" : "€" + v; }

  /* ---------- Colour scheme (skin) ---------- */
  var SKINS = ["forest", "navy", "copper", "plum", "night"];
  var skinBtns = document.querySelectorAll(".sw[data-skin]");
  var skinName = $("skinName");
  var animTimer;
  function setSkin(skin, save) {
    if (SKINS.indexOf(skin) === -1) skin = SKINS[0];
    if (save && !reduceMotion) { html.classList.add("skin-anim"); clearTimeout(animTimer); animTimer = setTimeout(function () { html.classList.remove("skin-anim"); }, 400); }
    html.dataset.skin = skin;
    skinBtns.forEach(function (b) {
      var on = b.dataset.skin === skin;
      b.setAttribute("aria-pressed", on ? "true" : "false");
      if (on && skinName) skinName.textContent = b.getAttribute("aria-label");
    });
    var meta = document.querySelector('meta[name="theme-color"]');
    if (meta) meta.content = getComputedStyle(html).getPropertyValue("--bg").trim() || meta.content;
    if (save) { try { localStorage.setItem("vetdomaSkin", skin); } catch (e) {} }
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
    var th = $("todayHours"); if (th) th.textContent = h[0] + " – " + h[1];
  })();

  /* ---------- Form ---------- */
  var form = $("apptForm"), dateIn = $("f-date"), timeSel = $("f-time"), hint = $("timeHint"), svcSel = $("f-service");
  dateIn.min = ymd(new Date()); dateIn.max = ymd(addDays(new Date(), 90));
  var zoneSel = $("f-zone"), estBox = $("estimate"), addrIn = $("f-address");
  function minutes() { return +svcSel.options[svcSel.selectedIndex].dataset.min; }
  function estimate() {
    var o = svcSel.options[svcSel.selectedIndex], z = zoneSel.options[zoneSel.selectedIndex];
    var price = +o.dataset.price, fee = +z.dataset.fee, total = price + fee;
    var from = o.dataset.from === "1";
    estBox.textContent = fill(T.estimate, { fee: money(fee), price: price ? money(price) : "—", total: (from ? T.fromw + " " : "") + money(total) });
    return { fee: fee, price: price, total: total, from: from };
  }
  function setTimes(r) {
    var keep = timeSel.value;
    timeSel.textContent = "";
    if (!r.slots.length) { hint.textContent = T.noSlots; return; }
    timeSel.appendChild(new Option(T.pick, ""));
    r.slots.forEach(function (s) { timeSel.appendChild(new Option(s, s)); });
    if (keep && r.slots.indexOf(keep) > -1) timeSel.value = keep;
    hint.textContent = fill(T.slotsHint, { n: r.slots.length });
  }
  function loadTimes() {
    var v = dateIn.value;
    if (!v) { hint.textContent = T.chooseDate; timeSel.textContent = ""; return Promise.resolve(); }
    hint.textContent = T.checking;
    return API.availability(v, minutes()).then(function (r) { if (dateIn.value === v) setTimes(r); }).catch(function () { hint.textContent = T.availError; });
  }
  dateIn.addEventListener("change", loadTimes);
  svcSel.addEventListener("change", function () { estimate(); loadTimes(); });
  zoneSel.addEventListener("change", estimate);
  estimate();
  document.querySelectorAll("[data-zone]").forEach(function (a) { a.addEventListener("click", function () { zoneSel.value = a.dataset.zone; estimate(); }); });
  (function find(i) {
    if (i > 10) return;
    var d = ymd(addDays(new Date(), i));
    API.availability(d, minutes()).then(function (r) { if (r.slots.length) { dateIn.value = d; setTimes(r); } else find(i + 1); }).catch(function () {});
  })(0);

  var errBox = $("aError"), sendBtn = $("aSend"), doneBox = $("aDone");
  function showError(msg) { errBox.textContent = msg; errBox.hidden = false; }
  if (API.mode === "demo") { var dn = $("demoNote"); dn.textContent = T.demoLine; dn.hidden = false; }
  form.addEventListener("submit", function (e) {
    e.preventDefault(); errBox.hidden = true;
    if (!dateIn.value || !timeSel.value) return showError(T.errTime);
    var name = form.elements.name.value.trim(), phone = form.elements.phone.value.trim();
    if (!name || phone.replace(/\D/g, "").length < 6) return showError(T.errName);
    var sid = svcSel.value, sp = form.querySelector('input[name="species"]:checked').value, pet = form.elements.pet.value.trim(), addr = addrIn.value.trim();
    if (!addr) return showError(T.errAddr);
    var est = estimate(), zid = zoneSel.value;
    var petLine = D.species[sp] + (pet ? " " + pet : "");
    var payload = {
      name: name, phone: phone, service: D.services[sid], date: dateIn.value, time: timeSel.value, durationMinutes: minutes(), fulfil: "delivery", address: addr, lang: lang,
      message: form.elements.msg.value.trim(), plan: { summary: petLine + " · " + D.services[sid] + " · " + D.zones[zid], species: sp, pet: pet, service: sid, zone: zid, estimate: est.total, estimateFrom: est.from }
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
    [[T.lines.when, longDate(p.date) + ", " + p.time], [T.lines.what, p.service + " (" + p.durationMinutes + " " + T.min + ")"], [T.lines.pet, D.species[p.plan.species] + (p.plan.pet ? " " + p.plan.pet : "")], [T.lines.where, p.address], [T.lines.cost, (p.plan.estimateFrom ? T.fromw + " " : "") + money(p.plan.estimate)], [T.lines.name, p.name]].forEach(function (r) { dl.appendChild(el("dt", "", r[0])); dl.appendChild(el("dd", "", r[1])); });
    doneBox.appendChild(dl);
    doneBox.appendChild(el("p", "", T.doneNext));
    if (API.mode === "demo") doneBox.appendChild(el("p", "demo-note", T.doneDemo));
    var act = el("div", "done-actions");
    if (API.mode === "demo") { var a = el("a", "btn btn-line", T.adminLink); a.href = (lang === "bg" ? "" : "../") + "admin.html" + (lang === "en" ? "?lang=en" : ""); act.appendChild(a); }
    var again = el("button", "btn btn-main", T.again); again.type = "button";
    again.addEventListener("click", function () { form.reset(); form.hidden = false; doneBox.hidden = true; estimate(); loadTimes(); scrollToEl($("book")); });
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
