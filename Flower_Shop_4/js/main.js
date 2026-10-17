/* Atelier Aubade (design 4): page behaviour.
   Colour schemes, menu, the stories rail, the planner (event, guests, up to three styles, pieces with counts, a live price range)
   and the free consultation booking (a day, a free time, details).
   The planner talks to AubadeAPI (js/api.js): a mock server now, a real backend later (docs/API.md). */
(function () {
  "use strict";

  var CFG = window.AUBADE_CONFIG || {};
  var API = window.AubadeAPI;
  var html = document.documentElement;
  var lang = html.lang === "bg" ? "bg" : "en";
  var reduceMotion = window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches;
  function $(id) { return document.getElementById(id); }
  var D = JSON.parse($("aubadeData").textContent);

  var T = {
    bg: {
      locale: "bg-BG", mapTitle: "Карта на ателието", hUnit: "ч", mUnit: "мин",
      slotsHint: "Свободни часове: {n}. Консултациите са до {c}.", noSlots: "Няма свободни часове този ден. Избери друг ден.", checking: "Проверяваме свободните часове…", availError: "Не успяхме да проверим часовете. Опитай пак.", pickDay: "Избери ден, за да видиш свободните часове.",
      guests: "{n} гости", event: "Събитие", styles: "Стил", remove: "Премахни", plus: "Още", minus: "По-малко", count: "брой",
      errPieces: "Избери поне един елемент.", errTime: "Избери ден и час за консултацията.", errName: "Въведи име и телефон.",
      errTaken: "Съжаляваме, този час току-що беше зает. Избери друг.", errInvalid: "Провери данните и опитай пак.", errGeneric: "Нещо се обърка. Опитай пак или ни се обади.",
      sending: "Изпращане…", demoLine: "Демо режим: заявките се пазят само в този браузър и нищо не се изпраща.",
      doneH: "Консултацията е заявена", doneRef: "Номер", statusPending: "Чака потвърждение",
      doneNext: "Ще се свържем с теб по телефона, за да потвърдим часа. Запази номера.",
      doneDemo: "Демо режим: нищо не беше изпратено. Заявката е записана само в този браузър.",
      adminLink: "Виж я в демо админ панела", again: "Нов план", send: "Запази консултацията", consult: "Консултация",
      eventDate: "Дата на събитието", venue: "Място",
      lines: { name: "Име", phone: "Телефон", service: "План", date: "Консултация", time: "Час", msg: "Съобщение" }
    },
    en: {
      locale: "en-GB", mapTitle: "Map of the studio", hUnit: "h", mUnit: "min",
      slotsHint: "{n} free times. Consultations end at {c}.", noSlots: "No free times on this day. Please pick another day.", checking: "Checking free times…", availError: "We could not check the free times. Please try again.", pickDay: "Pick a day to see free times.",
      guests: "{n} guests", event: "Event", styles: "Style", remove: "Remove", plus: "More", minus: "Fewer", count: "count",
      errPieces: "Please pick at least one piece.", errTime: "Please pick a day and a time for the consultation.", errName: "Please enter your name and phone.",
      errTaken: "Sorry, that time was just taken. Please choose another.", errInvalid: "Please check your details and try again.", errGeneric: "Something went wrong. Please try again or call us.",
      sending: "Sending…", demoLine: "Demo mode: requests are kept in this browser only and nothing is sent.",
      doneH: "Consultation requested", doneRef: "Reference", statusPending: "Waiting for confirmation",
      doneNext: "We will contact you by phone to confirm your time. Keep your reference handy.",
      doneDemo: "Demo mode: nothing was sent. The request is saved only in this browser.",
      adminLink: "See it in the demo back office", again: "New plan", send: "Book the consultation", consult: "Consultation",
      eventDate: "Event date", venue: "Venue",
      lines: { name: "Name", phone: "Phone", service: "Plan", date: "Consultation", time: "Time", msg: "Message" }
    }
  }[lang];

  /* ---------- Small helpers ---------- */
  function pad(n) { return (n < 10 ? "0" : "") + n; }
  function ymd(d) { return d.getFullYear() + "-" + pad(d.getMonth() + 1) + "-" + pad(d.getDate()); }
  function toDate(v) { var p = v.split("-"); return new Date(+p[0], +p[1] - 1, +p[2]); }
  function addDays(d, n) { return new Date(d.getFullYear(), d.getMonth(), d.getDate() + n); }
  function el(tag, cls, text) { var n = document.createElement(tag); if (cls) n.className = cls; if (text !== undefined) n.textContent = text; return n; }
  function scrollToEl(n) { n.scrollIntoView({ behavior: reduceMotion ? "auto" : "smooth", block: "start" }); }
  function longDate(v) { return toDate(v).toLocaleDateString(T.locale, { weekday: "long", day: "numeric", month: "long", year: "numeric" }); }
  function eur(n) { return n.toLocaleString(T.locale) + " €"; }

  /* ---------- Colour scheme (skin) ---------- */
  var SKINS = ["evergreen", "ivory", "blush", "midnight", "plum"];
  var skinBtns = document.querySelectorAll(".sw[data-skin]");
  var skinName = $("skinName");
  var animTimer;
  function setSkin(skin, save) {
    if (SKINS.indexOf(skin) === -1) skin = "evergreen";
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
    if (save) { try { localStorage.setItem("aubadeSkin", skin); } catch (e) {} }
  }
  skinBtns.forEach(function (b) { b.addEventListener("click", function () { setSkin(b.dataset.skin, true); }); });
  var startSkin = null;
  try { startSkin = new URLSearchParams(location.search).get("skin") || localStorage.getItem("aubadeSkin"); } catch (e) {}
  setSkin(startSkin || "evergreen", false);
  var yEl = $("year"); if (yEl) yEl.textContent = new Date().getFullYear();

  /* ---------- Menu and header ---------- */
  var nav = $("nav"), burger = $("burger"), topbar = $("top");
  burger.addEventListener("click", function () {
    var open = nav.classList.toggle("open");
    burger.setAttribute("aria-expanded", open ? "true" : "false");
  });
  nav.addEventListener("click", function (e) {
    if (e.target.closest("a") && nav.classList.contains("open")) { nav.classList.remove("open"); burger.setAttribute("aria-expanded", "false"); }
  });
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
    }, { threshold: 0.1, rootMargin: "0px 0px -6% 0px" });
    document.querySelectorAll(".sec-head, .pack, .timeline li, .rev, .visit-grid > div").forEach(function (n, i) {
      n.classList.add("rv"); n.style.setProperty("--d", ((i % 4) * 0.08).toFixed(2) + "s"); io.observe(n);
    });
  }

  /* ---------- Stories rail ---------- */
  var rail = $("rail");
  function railBy(dir) { rail.scrollBy({ left: dir * Math.max(260, rail.clientWidth * 0.7), behavior: reduceMotion ? "auto" : "smooth" }); }
  $("railPrev").addEventListener("click", function () { railBy(-1); });
  $("railNext").addEventListener("click", function () { railBy(1); });

  /* ---------- Map ---------- */
  var mapBox = $("mapBox");
  $("mapLoad").addEventListener("click", function () {
    var f = document.createElement("iframe");
    f.src = mapBox.dataset.src; f.title = T.mapTitle; f.loading = "lazy"; f.referrerPolicy = "no-referrer";
    mapBox.textContent = ""; mapBox.appendChild(f);
  });

  /* ================= The planner ================= */
  var form = $("planForm"), guestsEl = $("guests"), piecesEl = $("pieces");
  var counts = {}, tablesTouched = false;
  D.pieces.forEach(function (p) { counts[p.id] = p.def; });
  function tables() { return Math.max(1, Math.ceil(+guestsEl.value / 8)); }

  function renderPieces() {
    piecesEl.textContent = "";
    D.pieces.forEach(function (p) {
      var li = el("li", "piece"), info = el("div", "pc-info");
      info.appendChild(el("b", "", p.name));
      info.appendChild(el("small", "", p.min + " – " + p.max + " €" + (p.per ? " " + D.each : "")));
      li.appendChild(info);
      var ctl = el("div", "pc-ctl");
      if (p.cap === 1) {
        var t = el("button", "pc-toggle", counts[p.id] ? "✓" : "+"); t.type = "button";
        t.setAttribute("aria-pressed", counts[p.id] ? "true" : "false"); t.setAttribute("aria-label", p.name);
        t.addEventListener("click", function () { counts[p.id] = counts[p.id] ? 0 : 1; renderPieces(); renderBrief(); });
        ctl.appendChild(t);
      } else {
        var minus = el("button", "pc-step", "−"); minus.type = "button"; minus.setAttribute("aria-label", T.minus + ": " + p.name); minus.disabled = counts[p.id] <= 0;
        var out = el("output", "pc-n", String(counts[p.id])); out.setAttribute("aria-label", p.name + ", " + T.count);
        var plus = el("button", "pc-step", "+"); plus.type = "button"; plus.setAttribute("aria-label", T.plus + ": " + p.name); plus.disabled = counts[p.id] >= p.cap;
        minus.addEventListener("click", function () { counts[p.id]--; if (p.id === "tables") tablesTouched = true; renderPieces(); renderBrief(); });
        plus.addEventListener("click", function () { counts[p.id]++; if (p.id === "tables") tablesTouched = true; renderPieces(); renderBrief(); });
        ctl.appendChild(minus); ctl.appendChild(out); ctl.appendChild(plus);
      }
      li.appendChild(ctl);
      piecesEl.appendChild(li);
    });
  }

  function totals() {
    var min = 0, max = 0, lines = [];
    D.pieces.forEach(function (p) {
      var n = counts[p.id]; if (!n) return;
      min += p.min * n; max += p.max * n;
      lines.push({ name: p.name, n: n, per: p.per, min: p.min * n, max: p.max * n });
    });
    return { min: min, max: max, lines: lines };
  }
  function chosenStyles() { return Array.prototype.slice.call(form.querySelectorAll('input[name="style"]:checked')).map(function (x) { return x.dataset.name; }); }
  function eventName() { return form.querySelector('input[name="event"]:checked').dataset.name; }

  function renderBrief() {
    var t = totals(), st = chosenStyles(), ul = $("briefLines");
    $("guestsOut").textContent = guestsEl.value;
    $("tablesHint").textContent = D.tablesHint.replace("{n}", tables());
    $("briefSub").textContent = eventName() + " · " + T.guests.replace("{n}", guestsEl.value) + " · " + (st.length ? st.join(", ") : D.stylesNone);
    ul.textContent = "";
    if (!t.lines.length) ul.appendChild(el("li", "none", D.noneYet));
    t.lines.forEach(function (l) {
      var li = el("li"); li.appendChild(el("span", "", (l.per || l.n > 1 ? l.n + " × " : "") + l.name));
      li.appendChild(el("span", "", l.min === l.max ? eur(l.min) : eur(l.min) + " – " + eur(l.max))); ul.appendChild(li);
    });
    $("briefRange").textContent = t.lines.length ? eur(t.min) + " – " + eur(t.max) : "—";
  }

  form.addEventListener("change", function (e) {
    var n = e.target.name;
    if (n === "style") {
      var checked = form.querySelectorAll('input[name="style"]:checked');
      if (checked.length > 3) e.target.checked = false;
    }
    if (n === "guests") { if (!tablesTouched && counts.tables) counts.tables = Math.min(30, tables()); renderPieces(); }
    if (n === "slot") errEl.hidden = true;
    if (n === "day") { date = e.target.value; loadSlots(); }
    renderBrief();
  });
  guestsEl.addEventListener("input", function () { if (!tablesTouched && counts.tables) counts.tables = Math.min(30, tables()); renderPieces(); renderBrief(); });

  /* packages fill the planner */
  Array.prototype.forEach.call(document.querySelectorAll("[data-pack]"), function (b) {
    b.addEventListener("click", function () {
      var preset = D.packs[b.dataset.pack];
      D.pieces.forEach(function (p) { counts[p.id] = preset[p.id] || 0; });
      if (counts.tables) { tablesTouched = true; }
      renderPieces(); renderBrief(); scrollToEl($("plan"));
    });
  });

  /* ================= Consultation ================= */
  var dchips = $("dchips"), tchips = $("tchips"), slotHint = $("slotHint");
  var errEl = $("bkError"), sendBtn = $("bkSend"), done = $("bkDone");
  var today = new Date(); today = new Date(today.getFullYear(), today.getMonth(), today.getDate());
  var date = "", tick = 0, busy = false;
  function buildDays() {
    dchips.textContent = "";
    for (var i = 0; i < 21; i++) {
      var d = addDays(today, i), v = ymd(d), lab = el("label", "dc"), inp = el("input");
      inp.type = "radio"; inp.name = "day"; inp.value = v;
      lab.appendChild(inp);
      lab.appendChild(el("small", "", d.toLocaleDateString(T.locale, { weekday: "short" })));
      lab.appendChild(el("b", "", String(d.getDate())));
      lab.appendChild(el("small", "", d.toLocaleDateString(T.locale, { month: "short" })));
      lab.title = longDate(v); dchips.appendChild(lab);
    }
  }
  function loadSlots() {
    var token = ++tick, keep = (form.querySelector('input[name="slot"]:checked') || {}).value;
    if (!date) { tchips.textContent = ""; slotHint.textContent = T.pickDay; return; }
    slotHint.textContent = T.checking;
    API.availability(date, D.consult).then(function (res) {
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

  function fail(msg, f) { errEl.textContent = msg; errEl.hidden = false; if (f) f.focus(); }
  function buildPayload() {
    var t = totals(), st = chosenStyles(), slot = form.querySelector('input[name="slot"]:checked').value;
    var parts = [];
    if ($("f-date").value) parts.push(T.eventDate + ": " + longDate($("f-date").value));
    if ($("f-venue").value.trim()) parts.push(T.venue + ": " + $("f-venue").value.trim());
    if ($("f-msg").value.trim()) parts.push($("f-msg").value.trim());
    var pieces = t.lines.map(function (l) { return (l.per || l.n > 1 ? l.n + " × " : "") + l.name; }).join(", ");
    return {
      name: $("f-name").value.trim(), phone: $("f-phone").value.trim(), service: T.consult + ": " + eventName() + " (" + T.guests.replace("{n}", guestsEl.value) + ")",
      plan: { summary: eventName() + ", " + T.guests.replace("{n}", guestsEl.value) + ". " + T.styles + ": " + (st.join(", ") || "—") + ". " + pieces + ". " + eur(t.min) + " – " + eur(t.max) + ".",
              minPrice: t.min, maxPrice: t.max, minMinutes: D.consult, maxMinutes: D.consult, extras: st, priceOnRequest: false },
      fulfil: "pickup", address: "", card: "", date: date, time: slot, durationMinutes: D.consult, look: null, message: parts.join(" · "), lang: lang
    };
  }
  function setBusy(on) { busy = on; sendBtn.disabled = on; sendBtn.classList.toggle("is-busy", on); sendBtn.textContent = on ? T.sending : T.send; form.setAttribute("aria-busy", on ? "true" : "false"); }
  form.addEventListener("submit", function (e) {
    e.preventDefault();
    if (busy) return;
    if (!totals().lines.length) { fail(T.errPieces); return; }
    if (!date || !form.querySelector('input[name="slot"]:checked')) { fail(T.errTime, tchips.querySelector("input") || dchips.querySelector("input")); return; }
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
    var again = el("button", "btn btn-line btn-sm", T.again); again.type = "button";
    again.addEventListener("click", function () {
      form.reset(); D.pieces.forEach(function (p) { counts[p.id] = p.def; }); tablesTouched = false; date = "";
      done.hidden = true; form.hidden = false; errEl.hidden = true; renderPieces(); renderBrief(); loadSlots(); scrollToEl($("plan"));
    });
    actions.appendChild(again); done.appendChild(actions);
    form.hidden = true; done.hidden = false; done.focus({ preventScroll: true }); scrollToEl(done);
  }

  if (API.mode === "demo") { $("demoNote").hidden = false; $("demoNote").textContent = T.demoLine; }
  buildDays(); renderPieces(); renderBrief(); loadSlots();
})();
