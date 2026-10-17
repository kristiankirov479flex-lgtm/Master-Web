/* Nocturne (design 5): page behaviour.
   Colour schemes, section dots, a chat-style "set finder" (four questions in, a set with price and time out),
   a calendar for the day, free-time chips, live "open now" and "next free time", and the booking request.
   The booking talks to NocturneAPI (js/api.js): a mock server now, a real backend later (docs/API.md). */
(function () {
  "use strict";

  var CFG = window.NOCTURNE_CONFIG || {};
  var API = window.NocturneAPI;
  var html = document.documentElement;
  var lang = html.lang === "bg" ? "bg" : "en";
  var reduceMotion = window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches;
  function $(id) { return document.getElementById(id); }
  var Q = JSON.parse($("quizData").textContent);

  var T = {
    bg: {
      mapTitle: "Карта на студиото", locale: "bg-BG", hUnit: "ч", mUnit: "мин",
      opensNow: "Отворено · до {t}", openLater: "Затворено · отваря днес в {t}", openTomorrow: "Затворено · отваря утре в {t}",
      nextFree: "Следващ свободен час:", todayAt: "днес в {t}", tomorrowAt: "утре в {t}", dayAt: "{d} в {t}",
      pickFirst: "Първо намери комплекта си, за да видиш свободните часове.", pickDay: "Избери ден, за да видиш свободните часове.", checking: "Проверяваме свободните часове…", noSlots: "Няма свободни часове този ден. Избери друг ден.",
      slotsHint: "Свободни часове: {n}. Работим до {c}.", availError: "Не успяхме да проверим часовете. Опитай пак.",
      onRequest: "по запитване", from: "от", about: "Около", artNote: "Нейл артът се оценява по запитване, според дизайна.", step: "Въпрос {n} от {t}", you: "Ти", simple: "Маникюр с гел лак",
      errSet: "Първо намери комплекта си.", errTime: "Избери ден и час.", errName: "Въведи име и телефон.",
      errTaken: "Съжаляваме, този час току-що беше зает. Избери друг.", errInvalid: "Провери данните и опитай пак.", errGeneric: "Нещо се обърка. Опитай пак или ни се обади.",
      sending: "Изпращане…", demoLine: "Демо режим: заявките се пазят само в този браузър и нищо не се изпраща.",
      doneH: "Заявката е получена", doneRef: "Номер", statusPending: "Чака потвърждение",
      doneNext: "Ще се свържем с теб по телефона, за да потвърдим часа. Запази номера.",
      doneDemo: "Демо режим: нищо не беше изпратено. Заявката е записана само в този браузър.",
      adminLink: "Виж я в демо админ панела", again: "Нов комплект", send: "Изпрати заявката", occ: "Повод",
      lines: { service: "Услуги", date: "Дата", time: "Час", name: "Име", phone: "Телефон", msg: "Съобщение" }
    },
    en: {
      mapTitle: "Map of the studio", locale: "en-GB", hUnit: "h", mUnit: "min",
      opensNow: "Open now · until {t}", openLater: "Closed · opens today at {t}", openTomorrow: "Closed · opens tomorrow at {t}",
      nextFree: "Next free time:", todayAt: "today at {t}", tomorrowAt: "tomorrow at {t}", dayAt: "{d} at {t}",
      pickFirst: "Find your set first to see free times.", pickDay: "Pick a day to see free times.", checking: "Checking free times…", noSlots: "No free times on this day. Please pick another day.",
      slotsHint: "{n} free times. We close at {c}.", availError: "We could not check the free times. Please try again.",
      onRequest: "on request", from: "from", about: "About", artNote: "Nail art is priced on request, depending on the design.", step: "Question {n} of {t}", you: "You", simple: "Gel polish manicure",
      errSet: "Please find your set first.", errTime: "Please pick a day and a time.", errName: "Please enter your name and phone.",
      errTaken: "Sorry, that time was just taken. Please choose another.", errInvalid: "Please check your details and try again.", errGeneric: "Something went wrong. Please try again or call us.",
      sending: "Sending…", demoLine: "Demo mode: requests are kept in this browser only and nothing is sent.",
      doneH: "Request received", doneRef: "Reference", statusPending: "Waiting for confirmation",
      doneNext: "We will contact you by phone to confirm your time. Keep your reference handy.",
      doneDemo: "Demo mode: nothing was sent. The request is saved only in this browser.",
      adminLink: "See it in the demo back office", again: "New set", send: "Send the request", occ: "Occasion",
      lines: { service: "Services", date: "Date", time: "Time", name: "Name", phone: "Phone", msg: "Message" }
    }
  }[lang];

  /* ---------- Small helpers ---------- */
  function pad(n) { return (n < 10 ? "0" : "") + n; }
  function ymd(d) { return d.getFullYear() + "-" + pad(d.getMonth() + 1) + "-" + pad(d.getDate()); }
  function toDate(v) { var p = v.split("-"); return new Date(+p[0], +p[1] - 1, +p[2]); }
  function toMinutes(hhmm) { var p = hhmm.split(":"); return +p[0] * 60 + +p[1]; }
  function addDays(d, n) { return new Date(d.getFullYear(), d.getMonth(), d.getDate() + n); }
  function fmtMin(m) {
    var h = Math.floor(m / 60), r = m % 60, out = [];
    if (h) out.push(h + " " + T.hUnit);
    if (r) out.push(r + " " + T.mUnit);
    return out.join(" ");
  }
  function longDate(v) { return toDate(v).toLocaleDateString(T.locale, { weekday: "long", day: "numeric", month: "long", year: "numeric" }); }
  function shortDate(d) { return d.toLocaleDateString(T.locale, { weekday: "short", day: "numeric", month: "short" }); }
  function el(tag, cls, text) { var n = document.createElement(tag); if (cls) n.className = cls; if (text !== undefined) n.textContent = text; return n; }
  function scrollToEl(n) { n.scrollIntoView({ behavior: reduceMotion ? "auto" : "smooth", block: "start" }); }
  function dayHours(d) { var w = d.getDay(); return w === 0 || w === 6 ? CFG.hours.weekend : CFG.hours.weekday; }

  /* ---------- Colour scheme (skin) ---------- */
  var SKINS = ["orchid", "acid", "ember", "ice", "pearl"];
  var skinBtns = document.querySelectorAll(".sw[data-skin]");
  var skinName = $("skinName");
  var animTimer;
  function setSkin(skin, save) {
    if (SKINS.indexOf(skin) === -1) skin = "orchid";
    if (!reduceMotion) {
      html.classList.add("skin-anim");
      clearTimeout(animTimer);
      animTimer = setTimeout(function () { html.classList.remove("skin-anim"); }, 500);
    }
    html.dataset.skin = skin;
    skinBtns.forEach(function (b) {
      var on = b.dataset.skin === skin;
      b.setAttribute("aria-pressed", on ? "true" : "false");
      if (on && skinName) skinName.textContent = b.dataset.name;
    });
    var meta = document.querySelector('meta[name="theme-color"]');
    if (meta) meta.content = getComputedStyle(html).getPropertyValue("--bg").trim() || meta.content;
    if (save) { try { localStorage.setItem("nocturneSkin", skin); } catch (e) {} }
  }
  skinBtns.forEach(function (b) { b.addEventListener("click", function () { setSkin(b.dataset.skin, true); }); });
  var startSkin = null;
  try { startSkin = new URLSearchParams(location.search).get("skin") || localStorage.getItem("nocturneSkin"); } catch (e) {}
  setSkin(startSkin || "orchid", false);
  var yEl = $("year"); if (yEl) yEl.textContent = new Date().getFullYear();

  /* ---------- Section dots ---------- */
  var dots = Array.prototype.slice.call(document.querySelectorAll("#dots a"));
  if ("IntersectionObserver" in window) {
    var spy = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (!en.isIntersecting) return;
        dots.forEach(function (a) { a.setAttribute("aria-current", a.getAttribute("href") === "#" + en.target.id ? "true" : "false"); });
      });
    }, { rootMargin: "-45% 0px -45% 0px" });
    dots.forEach(function (a) { var s = document.querySelector(a.getAttribute("href")); if (s) spy.observe(s); });
  }
  var topbar = $("topbar");
  function onScroll() { topbar.classList.toggle("scrolled", window.scrollY > 8); }
  window.addEventListener("scroll", onScroll, { passive: true }); onScroll();

  /* ---------- Scroll reveal ---------- */
  if (html.classList.contains("js-reveal")) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (!en.isIntersecting) return;
        io.unobserve(en.target);
        en.target.classList.add("in");
        setTimeout(function () { en.target.classList.remove("rv", "in"); en.target.style.removeProperty("--d"); }, 1300);
      });
    }, { threshold: 0.12, rootMargin: "0px 0px -6% 0px" });
    document.querySelectorAll(".head, .phone, .bk-set, .cal, .bk-side, .visit-grid > div").forEach(function (n, i) {
      n.classList.add("rv"); n.style.setProperty("--d", ((i % 3) * 0.08).toFixed(2) + "s"); io.observe(n);
    });
  }

  /* ---------- Map and open now ---------- */
  var mapBox = $("mapBox");
  $("mapLoad").addEventListener("click", function () {
    var f = document.createElement("iframe");
    f.src = mapBox.dataset.src; f.title = T.mapTitle; f.loading = "lazy"; f.referrerPolicy = "no-referrer";
    mapBox.textContent = ""; mapBox.appendChild(f);
  });
  function updateOpen() {
    var now = new Date(), h = dayHours(now), m = now.getHours() * 60 + now.getMinutes(), text, open = false;
    if (m >= toMinutes(h[0]) && m < toMinutes(h[1])) { open = true; text = T.opensNow.replace("{t}", h[1]); }
    else if (m < toMinutes(h[0])) text = T.openLater.replace("{t}", h[0]);
    else text = T.openTomorrow.replace("{t}", dayHours(new Date(now.getTime() + 864e5))[0]);
    var n = $("openNow"); n.textContent = text; n.classList.toggle("off", !open);
  }
  updateOpen(); setInterval(updateOpen, 60000);

  /* ================= The set finder (a chat) ================= */
  var SVC = Q.svc, chat = $("chat"), choices = $("choices"), answers = {}, current = null, set = null, qi = 0;
  var BASE = { nat: "gel_mani", short: "ext_short", med: "ext_med", long: "ext_long" };
  var typingTimer;

  function bubble(who, text) {
    var b = el("div", "msg " + who);
    if (who === "user") b.appendChild(el("span", "sr-only", T.you + ": "));
    b.appendChild(document.createTextNode(text));
    chat.appendChild(b);
    chat.scrollTop = chat.scrollHeight;
    return b;
  }
  function typing(then) {
    var t = el("div", "msg bot typing"); t.setAttribute("aria-hidden", "true");
    t.innerHTML = "<i></i><i></i><i></i>";
    chat.appendChild(t); chat.scrollTop = chat.scrollHeight;
    clearTimeout(typingTimer);
    typingTimer = setTimeout(function () { t.remove(); then(); }, reduceMotion ? 0 : 520);
  }
  function startQuiz() {
    answers = {}; qi = 0; set = null;
    clearTimeout(typingTimer);
    chat.textContent = ""; choices.textContent = "";
    $("restart").hidden = true; $("quiz").hidden = false; $("result").hidden = true;
    $("quizStep").textContent = $("quiz").dataset.role || $("quizStep").textContent;
    bubble("bot", Q.intro);
    ask(0, false);
  }
  function ask(i, focus) {
    qi = i;
    $("quizStep").textContent = T.step.replace("{n}", i + 1).replace("{t}", Q.qs.length);
    typing(function () {
      var q = Q.qs[i];
      bubble("bot", q.q);
      choices.textContent = "";
      q.opts.forEach(function (o) {
        var b = el("button", "choice", o.label); b.type = "button";
        b.addEventListener("click", function () { choose(i, o); });
        choices.appendChild(b);
      });
      if (focus) choices.firstChild.focus({ preventScroll: true });
    });
  }
  function choose(i, o) {
    answers[Q.qs[i].key] = o.v;
    choices.textContent = "";
    bubble("user", o.label);
    $("restart").hidden = false;
    if (i + 1 < Q.qs.length) ask(i + 1, true);
    else typing(function () { bubble("bot", Q.done); setTimeout(showResult, reduceMotion ? 0 : 450); });
  }
  $("restart").addEventListener("click", startQuiz);
  $("resAgain").addEventListener("click", function () { startQuiz(); scrollToEl($("find")); });

  function totals(ids) {
    var t = { pmin: 0, pmax: 0, mmax: 0, request: false, names: [] };
    ids.forEach(function (id) { var s = SVC[id]; t.pmin += s.p0; t.pmax += s.p1; t.mmax += s.min; t.names.push(s.name); if (s.kind === "request") t.request = true; });
    return t;
  }
  function priceText(t) {
    if (t.request && t.pmax === 0) return T.onRequest;
    var txt = t.pmin === t.pmax ? t.pmin + " €" : t.pmin + " – " + t.pmax + " €";
    return t.request ? T.from + " " + txt : txt;
  }
  function lineText(id) { var s = SVC[id]; return s.kind === "request" ? T.onRequest : (s.p0 === s.p1 ? s.p0 + " €" : s.p0 + " – " + s.p1 + " €"); }
  function fillLines(ul, ids) {
    ul.textContent = "";
    ids.forEach(function (id) { var li = el("li"); li.appendChild(el("span", "", SVC[id].name)); li.appendChild(el("span", "", lineText(id))); ul.appendChild(li); });
  }
  function showResult() {
    var a = answers, ids = [BASE[a.length]];
    if (a.style === "chrome" || a.style === "art") ids.push("art");
    if (a.pedi === "yes") ids.push("gel_pedi");
    var look = Q.looks[a.style], lenLabel = Q.qs[1].opts.filter(function (o) { return o.v === a.length; })[0].label;
    var styleLabel = Q.qs[2].opts.filter(function (o) { return o.v === a.style; })[0].label;
    var desc = [lenLabel, styleLabel, Q.occ[a.occasion]].join(" · ");
    set = { ids: ids, desc: desc, title: look.name, look: look, occasion: Q.qs[0].opts.filter(function (o) { return o.v === a.occasion; })[0].label };
    var t = totals(ids);
    $("resImg").src = look.src; $("resImg").alt = look.alt; $("resImg").width = look.w; $("resImg").height = look.h;
    $("res-h").textContent = look.name; $("resDesc").textContent = desc;
    fillLines($("resLines"), ids);
    $("resPrice").textContent = priceText(t); $("resTime").textContent = T.about + " " + fmtMin(t.mmax);
    $("resNote").textContent = t.request ? T.artNote : "";
    $("quiz").hidden = true; $("result").hidden = false;
    $("result").focus({ preventScroll: true });
    renderSet();
  }
  $("skipQuiz").addEventListener("click", function () {
    set = { ids: ["gel_mani"], desc: T.simple, title: T.simple, look: null, occasion: "" };
    renderSet(); scrollToEl($("book"));
  });

  /* the set on the booking screen */
  function renderSet() {
    var has = !!set;
    $("bkEmpty").hidden = has; $("bkSet").hidden = !has;
    if (has) {
      var t = totals(set.ids);
      $("bkDesc").textContent = set.desc;
      fillLines($("bkLines"), set.ids);
      $("bkPrice").textContent = priceText(t); $("bkTime").textContent = T.about + " " + fmtMin(t.mmax);
    }
    loadSlots();
  }

  /* ================= Calendar and booking ================= */
  var form = $("bookForm"), tchips = $("tchips"), slotHint = $("slotHint");
  var errEl = $("bkError"), sendBtn = $("bkSend"), done = $("bkDone");
  var today = new Date(); today = new Date(today.getFullYear(), today.getMonth(), today.getDate());
  var maxDay = addDays(today, 90), month = new Date(today.getFullYear(), today.getMonth(), 1), date = "", tick = 0, busy = false;

  var dow = $("calDow");
  for (var i = 0; i < 7; i++) dow.appendChild(el("span", "", new Date(2024, 0, 1 + i).toLocaleDateString(T.locale, { weekday: "short" })));

  function renderCal() {
    var grid = $("calGrid"); grid.textContent = "";
    $("calTitle").textContent = month.toLocaleDateString(T.locale, { month: "long", year: "numeric" });
    var lead = (month.getDay() + 6) % 7, days = new Date(month.getFullYear(), month.getMonth() + 1, 0).getDate();
    for (var k = 0; k < lead; k++) grid.appendChild(el("span", "blank"));
    for (var n = 1; n <= days; n++) {
      var d = new Date(month.getFullYear(), month.getMonth(), n), v = ymd(d);
      var b = el("button", "cd", String(n)); b.type = "button"; b.dataset.date = v;
      b.setAttribute("aria-label", longDate(v));
      b.setAttribute("aria-pressed", v === date ? "true" : "false");
      if (d < today || d > maxDay) b.disabled = true;
      if (v === ymd(today)) b.classList.add("today");
      grid.appendChild(b);
    }
    $("calPrev").disabled = month <= new Date(today.getFullYear(), today.getMonth(), 1);
    $("calNext").disabled = new Date(month.getFullYear(), month.getMonth() + 1, 1) > maxDay;
  }
  $("calGrid").addEventListener("click", function (e) {
    var b = e.target.closest(".cd"); if (!b || b.disabled) return;
    date = b.dataset.date; renderCal(); loadSlots();
  });
  $("calPrev").addEventListener("click", function () { month = new Date(month.getFullYear(), month.getMonth() - 1, 1); renderCal(); });
  $("calNext").addEventListener("click", function () { month = new Date(month.getFullYear(), month.getMonth() + 1, 1); renderCal(); });

  function loadSlots() {
    var token = ++tick, keep = (form.querySelector('input[name="slot"]:checked') || {}).value;
    if (!set) { tchips.textContent = ""; slotHint.textContent = T.pickFirst; return; }
    if (!date) { tchips.textContent = ""; slotHint.textContent = T.pickDay; return; }
    var m = totals(set.ids).mmax;
    slotHint.textContent = T.checking;
    API.availability(date, m).then(function (res) {
      if (token !== tick) return;
      tchips.textContent = "";
      res.slots.forEach(function (s) {
        var lab = el("label", "tc"), inp = el("input");
        inp.type = "radio"; inp.name = "slot"; inp.value = s; if (s === keep) inp.checked = true;
        lab.appendChild(inp); lab.appendChild(document.createTextNode(s)); tchips.appendChild(lab);
      });
      slotHint.textContent = res.slots.length ? T.slotsHint.replace("{n}", res.slots.length).replace("{c}", res.close) : T.noSlots;
    }, function () { if (token === tick) slotHint.textContent = T.availError; });
  }
  form.addEventListener("change", function (e) { if (e.target.name === "slot") errEl.hidden = true; });

  var nextBox = $("nextFree");
  function findNext() {
    var start = new Date();
    function tryDay(i) {
      if (i > 13) return;
      var d = addDays(start, i);
      API.availability(ymd(d), 90).then(function (res) {
        if (!res.slots.length) return tryDay(i + 1);
        var when = i === 0 ? T.todayAt : i === 1 ? T.tomorrowAt : T.dayAt;
        nextBox.textContent = ""; nextBox.appendChild(document.createTextNode(T.nextFree + " "));
        var b = el("button", "", when.replace("{t}", res.slots[0]).replace("{d}", shortDate(d))); b.type = "button";
        b.addEventListener("click", function () { date = ymd(d); month = new Date(d.getFullYear(), d.getMonth(), 1); renderCal(); loadSlots(); scrollToEl($("book")); });
        nextBox.appendChild(b); nextBox.hidden = false;
      }, function () {});
    }
    tryDay(0);
  }
  findNext();

  function fail(msg, f) { errEl.textContent = msg; errEl.hidden = false; if (f) f.focus(); }
  function buildPayload() {
    var t = totals(set.ids), slot = form.querySelector('input[name="slot"]:checked').value;
    var msg = $("f-msg").value.trim();
    if (set.occasion) msg = (msg ? msg + " " : "") + "(" + T.occ + ": " + set.occasion + ")";
    return {
      name: $("f-name").value.trim(), phone: $("f-phone").value.trim(), service: t.names.join(", "),
      plan: { summary: set.title + " – " + set.desc + ". " + t.names.join(" + ") + ". " + T.about + " " + fmtMin(t.mmax) + ", " + priceText(t),
              minPrice: t.pmin, maxPrice: t.pmax, minMinutes: 0, maxMinutes: t.mmax, extras: t.names.slice(1), priceOnRequest: t.request },
      date: date, time: slot, durationMinutes: t.mmax,
      look: set.look ? { alt: set.look.alt, url: new URL(set.look.src, location.href).href.replace("-800.jpg", ".jpg") } : null,
      message: msg, lang: lang
    };
  }
  function setBusy(on) { busy = on; sendBtn.disabled = on; sendBtn.classList.toggle("is-busy", on); sendBtn.textContent = on ? T.sending : T.send; form.setAttribute("aria-busy", on ? "true" : "false"); }
  form.addEventListener("submit", function (e) {
    e.preventDefault();
    if (busy) return;
    if (!set) { fail(T.errSet); scrollToEl($("find")); return; }
    if (!form.querySelector('input[name="slot"]:checked')) { fail(T.errTime, tchips.querySelector("input") || $("calGrid").querySelector(".cd:not(:disabled)")); return; }
    if (!$("f-name").value.trim()) { fail(T.errName, $("f-name")); return; }
    if (!$("f-phone").value.trim()) { fail(T.errName, $("f-phone")); return; }
    errEl.hidden = true;
    var payload = buildPayload();
    setBusy(true);
    API.createRequest(payload).then(function (rec) { setBusy(false); showDone(rec, payload); }, function (er) {
      setBusy(false);
      if (er && er.code === "slot_taken") { fail(T.errTaken); loadSlots(); }
      else fail(er && er.code === "invalid" ? T.errInvalid : T.errGeneric);
    });
  });
  function showDone(rec, p) {
    var L = T.lines;
    done.textContent = "";
    done.appendChild(el("h3", "", T.doneH));
    var ref = el("p", "done-ref"); ref.appendChild(el("span", "", T.doneRef)); ref.appendChild(el("strong", "", rec.id)); done.appendChild(ref);
    var st = el("p", "done-status"); st.appendChild(el("span", "pill", T.statusPending)); done.appendChild(st);
    var dl = el("dl", "done-list");
    function row(k, v) { if (!v) return; dl.appendChild(el("dt", "", k)); dl.appendChild(el("dd", "", v)); }
    row(L.name, p.name); row(L.phone, p.phone); row(L.service, p.plan.summary); row(L.date, longDate(p.date)); row(L.time, p.time); row(L.msg, p.message);
    done.appendChild(dl);
    done.appendChild(el("p", "", T.doneNext));
    var actions = el("div", "done-actions");
    if (API.mode === "demo") {
      done.appendChild(el("p", "demo-note", T.doneDemo));
      var link = el("a", "btn btn-main btn-sm", T.adminLink);
      var adm = document.querySelector('.foot a[href*="admin"]'); link.href = adm ? adm.href : "admin.html";
      actions.appendChild(link);
    }
    var again = el("button", "btn btn-ghost btn-sm", T.again); again.type = "button";
    again.addEventListener("click", function () { form.reset(); date = ""; set = null; done.hidden = true; form.hidden = false; errEl.hidden = true; renderCal(); renderSet(); startQuiz(); scrollToEl($("find")); });
    actions.appendChild(again); done.appendChild(actions);
    form.hidden = true; done.hidden = false; done.focus({ preventScroll: true }); scrollToEl(done);
    findNext();
  }

  if (API.mode === "demo") { $("demoNote").hidden = false; $("demoNote").textContent = T.demoLine; }
  renderCal(); renderSet(); startQuiz();
})();
