/* Kristal (detailing design 1): page behaviour.
   Colour schemes, menu, today's hours, the booking form (car, size, package, add-ons, a live price estimate and time needed, a day and a free
   drop-off time that fits the job, details) and the map. The request talks to KristalAPI (js/api.js): a mock server now, a real backend later (docs/API.md). */
(function () {
  "use strict";

  var CFG = window.KRISTAL_CONFIG || {};
  var API = window.KristalAPI;
  var html = document.documentElement;
  var lang = html.lang === "bg" ? "bg" : "en";
  var reduceMotion = window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches;
  function $(id) { return document.getElementById(id); }
  var D = JSON.parse($("kristalData").textContent);

  var T = {
    bg: {
      locale: "bg-BG", mapTitle: "Карта на студиото", pick: "Избери час", h: "ч", m: "мин", from: "от", otherMake: "Друга марка",
      est: "Ориентировъчно: <b>{p}</b> · около {t}", estSure: "Точната цена казваме след оглед на боята.",
      slotsHint: "Свободни часове: {n}.", noSlots: "Няма свободно място този ден за толкова време. Избери друг ден.", availError: "Не успяхме да проверим часовете. Опитай пак.", checking: "Проверяваме свободните часове…", chooseDate: "Избери дата, за да видиш свободните часове.",
      errMake: "Избери марка на автомобила.", errTime: "Избери дата и час.", errName: "Въведи име и телефон.", errTaken: "Съжаляваме, този час току-що беше зает. Избери друг.", errInvalid: "Провери данните и опитай пак.", errGeneric: "Нещо се обърка. Опитай пак или ни се обади.",
      sending: "Изпращане…", demoLine: "Демо режим: заявките се пазят само в този браузър и нищо не се изпраща.",
      doneH: "Заявката е приета", doneRef: "Номер", statusPending: "Чака потвърждение", doneNext: "Ще ти се обадим, за да потвърдим часа и цената. Запази номера.",
      doneDemo: "Демо режим: нищо не беше изпратено. Заявката е записана само в този браузър.", adminLink: "Виж я в демо админ панела", again: "Нова заявка",
      lines: { when: "Кога", car: "Автомобил", what: "Пакет", est: "Ориентировъчно", name: "Име" }
    },
    en: {
      locale: "en-GB", mapTitle: "Map of the studio", pick: "Choose a time", h: "h", m: "min", from: "from", otherMake: "Other make",
      est: "Estimate: <b>{p}</b> · about {t}", estSure: "We tell you the exact price after inspecting the paint.",
      slotsHint: "{n} free times.", noSlots: "No free place this day for that long. Please pick another day.", availError: "We could not check the times. Please try again.", checking: "Checking free times…", chooseDate: "Choose a date to see the free times.",
      errMake: "Please choose your car make.", errTime: "Please pick a date and a time.", errName: "Please enter your name and phone.", errTaken: "Sorry, that time was just taken. Please choose another.", errInvalid: "Please check your details and try again.", errGeneric: "Something went wrong. Please try again or call us.",
      sending: "Sending…", demoLine: "Demo mode: requests are kept in this browser only and nothing is sent.",
      doneH: "Request received", doneRef: "Reference", statusPending: "Waiting for confirmation", doneNext: "We will call you to confirm the time and the price. Keep your reference.",
      doneDemo: "Demo mode: nothing was sent. The request is saved only in this browser.", adminLink: "See it in the demo back office", again: "New request",
      lines: { when: "When", car: "Car", what: "Package", est: "Estimate", name: "Name" }
    }
  }[lang];

  /* ---------- Helpers ---------- */
  function pad(n) { return (n < 10 ? "0" : "") + n; }
  function ymd(d) { return d.getFullYear() + "-" + pad(d.getMonth() + 1) + "-" + pad(d.getDate()); }
  function toDate(v) { var p = v.split("-"); return new Date(+p[0], +p[1] - 1, +p[2]); }
  function addDays(d, n) { return new Date(d.getFullYear(), d.getMonth(), d.getDate() + n); }
  function el(tag, cls, text) { var n = document.createElement(tag); if (cls) n.className = cls; if (text !== undefined) n.textContent = text; return n; }
  function fill(s, o) { return s.replace(/\{(\w+)\}/g, function (m, k) { return o[k] !== undefined ? o[k] : m; }); }
  function eur(n) { return lang === "bg" ? Math.round(n) + " €" : "€" + Math.round(n); }
  function hm(m) { var h = Math.floor(m / 60), r = m % 60; return (h ? h + " " + T.h : "") + (r ? (h ? " " : "") + r + " " + T.m : ""); }
  function longDate(v) { return toDate(v).toLocaleDateString(T.locale, { weekday: "long", day: "numeric", month: "long" }); }
  function scrollToEl(n) { n.scrollIntoView({ behavior: reduceMotion ? "auto" : "smooth", block: "start" }); }

  /* ---------- Colour scheme (skin) ---------- */
  var SKINS = ["graphite", "steel", "pearl", "noir", "racing"];
  var skinBtns = document.querySelectorAll(".sw[data-skin]");
  var skinName = $("skinName");
  var animTimer;
  function setSkin(skin, save) {
    if (SKINS.indexOf(skin) === -1) skin = "graphite";
    if (save && !reduceMotion) { html.classList.add("skin-anim"); clearTimeout(animTimer); animTimer = setTimeout(function () { html.classList.remove("skin-anim"); }, 400); }
    html.dataset.skin = skin;
    skinBtns.forEach(function (b) {
      var on = b.dataset.skin === skin;
      b.setAttribute("aria-pressed", on ? "true" : "false");
      if (on && skinName) skinName.textContent = b.getAttribute("aria-label");
    });
    var meta = document.querySelector('meta[name="theme-color"]');
    if (meta) meta.content = getComputedStyle(html).getPropertyValue("--bg").trim() || meta.content;
    if (save) { try { localStorage.setItem("kristalSkin", skin); } catch (e) {} }
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

  /* ---------- Booking ---------- */
  var form = $("bookForm"), dateIn = $("f-date"), timeSel = $("f-time"), hint = $("timeHint");
  dateIn.min = ymd(new Date()); dateIn.max = ymd(addDays(new Date(), 90));
  function checked(name) { return form.querySelector('input[name="' + name + '"]:checked').value; }
  function addons() { return Array.prototype.slice.call(form.querySelectorAll('input[name="addon"]:checked')).map(function (c) { return c.value; }); }
  function sizeIdx() { return D.sizes.indexOf(checked("size")); }
  function minutes() { return D.packages[checked("pkg")].min + addons().length * D.addon; }
  function price() { var p = D.packages[checked("pkg")]; return p.prices[sizeIdx()] + addons().reduce(function (s, a) { return s + D.addons[a].price; }, 0); }
  function estimate() {
    var p = D.packages[checked("pkg")];
    $("est").innerHTML = fill(T.est, { p: (p.from ? T.from + " " : "") + eur(price()), t: hm(minutes()) }) + (p.from ? " · " + T.estSure : "");
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
  var t0;
  form.addEventListener("change", function (e) {
    estimate();
    if (e.target.name === "pkg" || e.target.name === "addon") { clearTimeout(t0); t0 = setTimeout(loadTimes, 150); }
  });
  dateIn.addEventListener("change", loadTimes);
  estimate();
  (function find(i) {
    if (i > 10) return;
    var d = ymd(addDays(new Date(), i));
    API.availability(d, minutes()).then(function (r) { if (r.slots.length) { dateIn.value = d; setTimes(r); } else find(i + 1); }).catch(function () {});
  })(0);

  var errBox = $("bError"), sendBtn = $("bSend"), doneBox = $("bDone");
  function showError(msg) { errBox.textContent = msg; errBox.hidden = false; }
  if (API.mode === "demo") { var dn = $("demoNote"); dn.textContent = T.demoLine; dn.hidden = false; }
  function carText() { var mk = form.elements.make.value, model = form.elements.model.value.trim(); return ((mk === "other" ? T.otherMake : mk) + (model ? " " + model : "")).trim() + " · " + D.sizeNames[checked("size")]; }
  form.addEventListener("submit", function (e) {
    e.preventDefault(); errBox.hidden = true;
    if (!form.elements.make.value) { form.elements.make.focus(); return showError(T.errMake); }
    if (!dateIn.value || !timeSel.value) return showError(T.errTime);
    var name = form.elements.name.value.trim(), phone = form.elements.phone.value.trim();
    if (!name || phone.replace(/\D/g, "").length < 6) return showError(T.errName);
    var pid = checked("pkg"), p = D.packages[pid], ad = addons();
    var summary = carText() + " · " + p.name + (ad.length ? " + " + ad.map(function (a) { return D.addons[a].name; }).join(", ") : "");
    var payload = {
      name: name, phone: phone, service: p.name, date: dateIn.value, time: timeSel.value, durationMinutes: minutes(), fulfil: "pickup", lang: lang,
      message: form.elements.msg.value.trim(),
      plan: { summary: summary, car: { make: form.elements.make.value, model: form.elements.model.value.trim(), size: checked("size") }, package: pid, addons: ad, estimate: price(), estimateFrom: p.from }
    };
    sendBtn.disabled = true; sendBtn.classList.add("is-busy"); var label = sendBtn.textContent; sendBtn.textContent = T.sending;
    API.createRequest(payload).then(function (res) { showDone(res, payload, summary); })
      .catch(function (err) {
        if (err && err.code === "slot_taken") { showError(T.errTaken); loadTimes(); }
        else if (err && err.code === "invalid") showError(T.errInvalid); else showError(T.errGeneric);
      })
      .then(function () { sendBtn.disabled = false; sendBtn.classList.remove("is-busy"); sendBtn.textContent = label; });
  });
  function showDone(res, p, summary) {
    form.hidden = true; doneBox.hidden = false; doneBox.textContent = "";
    doneBox.appendChild(el("h3", "", T.doneH));
    var ref = el("p", "done-ref"); ref.appendChild(el("span", "", T.doneRef)); ref.appendChild(el("strong", "", res.id)); doneBox.appendChild(ref);
    var ps = el("p", "done-status"); ps.appendChild(el("span", "pill", T.statusPending)); doneBox.appendChild(ps);
    var dl = el("dl", "done-list");
    [[T.lines.when, longDate(p.date) + ", " + p.time + " (" + hm(p.durationMinutes) + ")"], [T.lines.car, carText()], [T.lines.what, summary.split(" · ").slice(2).join(" · ")], [T.lines.est, (p.plan.estimateFrom ? T.from + " " : "") + eur(p.plan.estimate)], [T.lines.name, p.name]]
      .forEach(function (r) { dl.appendChild(el("dt", "", r[0])); dl.appendChild(el("dd", "", r[1])); });
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
