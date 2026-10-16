/* Lumi Nail Studio (design 2): page behaviour.
   Colour schemes, the visit builder (tick services, see price and time), gallery filter and viewer, live "next free time",
   quick time picks and the request form. The form talks to LumiAPI (js/api.js): a mock server now, a real backend later (docs/API.md). */
(function () {
  "use strict";

  var CFG = window.LUMI_CONFIG || {};
  var API = window.LumiAPI;
  var html = document.documentElement;
  var lang = html.lang === "bg" ? "bg" : "en";
  var reduceMotion = window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches;
  function $(id) { return document.getElementById(id); }

  var T = {
    bg: {
      locale: "bg-BG", hUnit: "ч", mUnit: "мин", about: "Около", mapTitle: "Карта на студиото", shown: "Показани снимки: {n}",
      from: "от", onRequest: "по запитване", sumRequest: "Плюс нейл арт, цената се уточнява при потвърждение.", remove: "Премахни",
      todayAt: "Днес {t}", tomorrowAt: "Утре {t}", dayAt: "{d} {t}", openUntil: "Отворено до {t}", closedLater: "Затворено · отваря в {t}", closedTomorrow: "Затворено · отваря утре в {t}",
      checking: "Проверяваме свободните часове…", noSlots: "Няма начален час, който се събира този ден. Избери друга дата.",
      hint: "Начални часове от {a} до {b} за посещение от около {d}. Затваряме в {c}.", hintNoDate: "Показани са часове за делнични дни и посещение от около {d}. Избери дата, за да видиш конкретния ден.",
      someTaken: "Някои часове вече са заети.", availError: "Не успяхме да проверим свободните часове. Опитай пак.",
      quickNone: "Няма свободни часове в следващите дни. Избери дата по-долу.", quickHint: "Натисни час, за да го сложиш във формата.",
      lookAdded: "Снимката е добавена към заявката ти.", picked: "Часът е избран във формата.",
      errPick: "Избери поне една услуга, за да изпратиш заявката.", errFields: "Попълни име, телефон, дата и час.",
      sending: "Изпращане…", demoLine: "Демо режим: заявките се пазят само в този браузър и нищо не се изпраща.",
      errTaken: "Съжаляваме, този час току-що беше зает. Избери друг час.", errInvalid: "Провери данните във формата и опитай пак.", errGeneric: "Нещо се обърка. Опитай пак или ни се обади.",
      doneH: "Заявката е получена", doneRef: "Номер на заявката", doneStatus: "Статус", statusPending: "Чака потвърждение",
      doneNext: "Ще се свържем с теб по телефона, за да потвърдим часа. Запази номера на заявката.",
      doneDemo: "Демо режим: нищо не беше изпратено. Заявката е записана само в този браузър.",
      again: "Направи нова заявка", adminLink: "Виж я в демо админ панела",
      lines: { name: "Име", phone: "Телефон", service: "Услуги", date: "Удобна дата", time: "Удобен час", look: "Желан стил", msg: "Съобщение" }
    },
    en: {
      locale: "en-GB", hUnit: "h", mUnit: "min", about: "About", mapTitle: "Map of the studio", shown: "Photos shown: {n}",
      from: "from", onRequest: "on request", sumRequest: "Plus nail art, priced when we confirm.", remove: "Remove",
      todayAt: "Today {t}", tomorrowAt: "Tomorrow {t}", dayAt: "{d} {t}", openUntil: "Open until {t}", closedLater: "Closed · opens at {t}", closedTomorrow: "Closed · opens tomorrow at {t}",
      checking: "Checking free times…", noSlots: "No start time fits on this day. Please pick another date.",
      hint: "Start times from {a} to {b} for a visit of about {d}. We close at {c}.", hintNoDate: "Weekday times for a visit of about {d} are shown. Pick a date to see that day.",
      someTaken: "Some times are already taken.", availError: "We could not check the free times. Please try again.",
      quickNone: "No free times in the next days. Pick a date below.", quickHint: "Press a time to put it in the form.",
      lookAdded: "The photo was added to your request.", picked: "The time was selected in the form.",
      errPick: "Choose at least one service to send the request.", errFields: "Please fill in name, phone, date and time.",
      sending: "Sending…", demoLine: "Demo mode: requests are kept in this browser only and nothing is sent.",
      errTaken: "Sorry, that time was just taken. Please choose another time.", errInvalid: "Please check the form and try again.", errGeneric: "Something went wrong. Please try again or call us.",
      doneH: "Request received", doneRef: "Reference", doneStatus: "Status", statusPending: "Waiting for confirmation",
      doneNext: "We will contact you by phone to confirm your time. Keep your reference handy.",
      doneDemo: "Demo mode: nothing was sent. The request is saved only in this browser.",
      again: "Make another request", adminLink: "See it in the demo back office",
      lines: { name: "Name", phone: "Phone", service: "Services", date: "Preferred date", time: "Preferred time", look: "Look I like", msg: "Message" }
    }
  }[lang];

  /* ---------- Small helpers ---------- */
  function pad(n) { return (n < 10 ? "0" : "") + n; }
  function ymd(d) { return d.getFullYear() + "-" + pad(d.getMonth() + 1) + "-" + pad(d.getDate()); }
  function toDate(v) { var p = v.split("-"); return new Date(+p[0], +p[1] - 1, +p[2]); }
  function toMinutes(hhmm) { var p = hhmm.split(":"); return +p[0] * 60 + +p[1]; }
  function fmtMin(m) {
    var h = Math.floor(m / 60), r = m % 60, out = [];
    if (h) out.push(h + " " + T.hUnit);
    if (r) out.push(r + " " + T.mUnit);
    return out.join(" ");
  }
  function fmtRange(a, b, f) { return a === b ? f(a) : f(a) + " – " + f(b); }
  function longDate(v) { return toDate(v).toLocaleDateString(T.locale, { weekday: "long", day: "numeric", month: "long", year: "numeric" }); }
  function shortDate(d) { return d.toLocaleDateString(T.locale, { weekday: "short", day: "numeric", month: "short" }); }
  function el(tag, cls, text) { var n = document.createElement(tag); if (cls) n.className = cls; if (text !== undefined) n.textContent = text; return n; }
  function scrollToEl(n) { n.scrollIntoView({ behavior: reduceMotion ? "auto" : "smooth", block: "start" }); }
  function dayHours(d) { var w = d.getDay(); return w === 0 || w === 6 ? CFG.hours.weekend : CFG.hours.weekday; }
  function whenText(i, d, t) { return (i === 0 ? T.todayAt : i === 1 ? T.tomorrowAt : T.dayAt).replace("{t}", t).replace("{d}", shortDate(d)); }

  /* ---------- Colour scheme (skin) ---------- */
  var SKINS = ["rose", "sage", "espresso", "oxblood", "midnight"];
  var skinBtns = document.querySelectorAll(".sw[data-skin]");
  var skinName = $("skinName");
  var animTimer;
  function setSkin(skin, save) {
    if (SKINS.indexOf(skin) === -1) skin = "rose";
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
    if (save) { try { localStorage.setItem("lumiSkin", skin); } catch (e) {} }
  }
  skinBtns.forEach(function (b) { b.addEventListener("click", function () { setSkin(b.dataset.skin, true); }); });
  var startSkin = null;
  try { startSkin = new URLSearchParams(location.search).get("skin") || localStorage.getItem("lumiSkin"); } catch (e) {}
  setSkin(startSkin || "rose", false);

  /* ---------- Menu ---------- */
  var nav = $("nav"), burger = $("burger");
  burger.addEventListener("click", function () {
    var open = nav.classList.toggle("open");
    burger.setAttribute("aria-expanded", open ? "true" : "false");
  });
  nav.addEventListener("click", function (e) {
    if (e.target.closest("a") && nav.classList.contains("open")) {
      nav.classList.remove("open");
      burger.setAttribute("aria-expanded", "false");
    }
  });
  var yEl = $("year"); if (yEl) yEl.textContent = new Date().getFullYear();

  /* ---------- Scroll reveal ---------- */
  if (html.classList.contains("js-reveal")) {
    var groups = [[".sec-head", 0], [".build-main", 0], [".build-sum", 0.1], [".gal-item", 0.06, true], [".faq-grid details", 0.05], [".book-intro", 0], [".request-col", 0.1], [".info-tile", 0.08]];
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (!en.isIntersecting) return;
        io.unobserve(en.target);
        en.target.classList.add("in");
        setTimeout(function () { en.target.classList.remove("rv", "in"); en.target.style.removeProperty("--d"); }, 1300);
      });
    }, { threshold: 0.1, rootMargin: "0px 0px -6% 0px" });
    groups.forEach(function (g) {
      document.querySelectorAll(g[0]).forEach(function (n, i) {
        n.classList.add("rv");
        n.style.setProperty("--d", ((g[2] ? i % 4 : i) * g[1]).toFixed(2) + "s");
        io.observe(n);
      });
    });
  }

  /* ---------- Map: loads only when the visitor asks ---------- */
  var mapBox = $("mapBox");
  $("mapLoad").addEventListener("click", function () {
    var f = document.createElement("iframe");
    f.src = mapBox.dataset.src; f.title = T.mapTitle; f.loading = "lazy"; f.referrerPolicy = "no-referrer";
    mapBox.textContent = "";
    mapBox.appendChild(f);
  });

  /* ---------- Request form: shared state ---------- */
  var form = $("requestForm");
  var dateEl = $("f-date"), timeEl = $("f-time"), hint = $("timeHint");
  var look = null;
  var live = $("formLive");
  function announce(msg) { live.textContent = ""; setTimeout(function () { live.textContent = msg; }, 30); }

  /* ---------- Services: tabs ---------- */
  var tabs = Array.prototype.slice.call(document.querySelectorAll(".tab"));
  function selectTab(t, focus) {
    tabs.forEach(function (x) {
      var on = x === t;
      x.setAttribute("aria-selected", on ? "true" : "false");
      x.tabIndex = on ? 0 : -1;
      $(x.getAttribute("aria-controls")).hidden = !on;
    });
    if (focus) t.focus();
  }
  tabs.forEach(function (t, i) {
    t.addEventListener("click", function () { selectTab(t, false); });
    t.addEventListener("keydown", function (e) {
      var n = tabs.length;
      if (e.key === "ArrowRight") { e.preventDefault(); selectTab(tabs[(i + 1) % n], true); }
      else if (e.key === "ArrowLeft") { e.preventDefault(); selectTab(tabs[(i - 1 + n) % n], true); }
    });
  });

  /* ---------- Visit builder: tick services, see the total ---------- */
  var svcInputs = Array.prototype.slice.call(document.querySelectorAll('input[name="svc"]'));
  function chosen() { return svcInputs.filter(function (c) { return c.checked; }); }
  function totals() {
    var t = { pmin: 0, pmax: 0, mmin: 0, mmax: 0, from: false, request: false, names: [] };
    chosen().forEach(function (c) {
      t.pmin += +c.dataset.pmin; t.pmax += +c.dataset.pmax; t.mmin += +c.dataset.min; t.mmax += +c.dataset.max;
      if (c.dataset.kind === "from" || c.dataset.kind === "per") t.from = true;
      if (c.dataset.kind === "request") t.request = true;
      t.names.push(c.dataset.name);
    });
    return t;
  }
  function priceText(t) {
    if (t.request && t.pmax === 0) return T.onRequest;
    var txt = t.pmin === t.pmax ? t.pmin + " €" : t.pmin + " – " + t.pmax + " €";
    return t.from ? T.from + " " + txt : txt;
  }
  function visitMinutes() { var t = totals(); return t.names.length ? t.mmax : 60; }
  function bump(node, text) {
    if (node.textContent === text) return;
    node.textContent = text;
    node.classList.remove("bump"); void node.offsetWidth; node.classList.add("bump");
  }
  var tick = 0, quickTimer;
  function renderBuilder() {
    var t = totals(), sel = chosen(), list = $("sumList"), planList = $("planList");
    list.textContent = ""; planList.textContent = "";
    sel.forEach(function (c) {
      var li = el("li"); li.appendChild(el("span", "", c.dataset.name));
      var x = el("button", "", "×"); x.type = "button"; x.setAttribute("aria-label", T.remove + ": " + c.dataset.name);
      x.addEventListener("click", function () { c.checked = false; onSelectionChange(); });
      li.appendChild(x); list.appendChild(li);
      planList.appendChild(el("li", "", c.dataset.name));
    });
    $("sumEmpty").hidden = sel.length > 0;
    $("sumOut").hidden = sel.length === 0;
    $("planNeed").hidden = sel.length > 0;
    $("sumNote").hidden = !t.request || t.pmax === 0;
    $("sumNote").textContent = T.sumRequest;
    if (sel.length) {
      bump($("sumPrice"), priceText(t));
      bump($("sumTime"), fmtRange(t.mmin, t.mmax, fmtMin));
    }
    tabs.forEach(function (tab) {
      var panel = $(tab.getAttribute("aria-controls")), n = panel.querySelectorAll('input:checked').length, c = tab.querySelector(".count");
      c.hidden = n === 0; c.textContent = n;
    });
  }
  function onSelectionChange() {
    renderBuilder();
    updateTimes();
    clearTimeout(quickTimer);
    quickTimer = setTimeout(renderQuick, 250);
  }
  svcInputs.forEach(function (c) { c.addEventListener("change", onSelectionChange); });
  $("sumBook").addEventListener("click", function (e) {
    if (!chosen().length) { e.preventDefault(); scrollToEl($("services")); }
  });

  /* ---------- Gallery: filter, viewer, "Request this look" ---------- */
  var items = Array.prototype.slice.call(document.querySelectorAll(".gal-item"));
  var chips = document.querySelectorAll(".chip[data-filter]");
  var galStatus = $("galStatus");
  chips.forEach(function (chip) {
    chip.addEventListener("click", function () {
      var f = chip.dataset.filter, n = 0;
      chips.forEach(function (c) { c.setAttribute("aria-pressed", c === chip ? "true" : "false"); });
      items.forEach(function (it) {
        var show = f === "all" || it.dataset.cat === f;
        it.hidden = !show;
        if (show) {
          it.classList.remove("rv", "in");
          it.style.setProperty("--d", (n % 4 * 0.05).toFixed(2) + "s");
          it.classList.remove("pop"); void it.offsetWidth; it.classList.add("pop");
          n++;
        }
      });
      galStatus.textContent = T.shown.replace("{n}", n);
    });
  });
  var box = $("lightbox"), lbImg = $("lbImg"), current = 0;
  function visible() { return items.filter(function (it) { return !it.hidden; }); }
  function show(i) {
    var list = visible();
    if (!list.length) return;
    current = (i + list.length) % list.length;
    var it = list[current], img = it.querySelector("img");
    lbImg.src = it.dataset.full; lbImg.alt = img.alt;
    lbImg.classList.remove("swap"); void lbImg.offsetWidth; lbImg.classList.add("swap");
  }
  items.forEach(function (it) { it.addEventListener("click", function () { show(visible().indexOf(it)); box.showModal(); }); });
  $("lbClose").addEventListener("click", function () { box.close(); });
  $("lbPrev").addEventListener("click", function () { show(current - 1); });
  $("lbNext").addEventListener("click", function () { show(current + 1); });
  box.addEventListener("click", function (e) { if (e.target === box || e.target.className === "lb-inner") box.close(); });
  box.addEventListener("keydown", function (e) {
    if (e.key === "ArrowLeft") show(current - 1);
    if (e.key === "ArrowRight") show(current + 1);
  });
  var lookChip = $("lookChip");
  function setLook(item) {
    var img = item.querySelector("img");
    look = { alt: img.alt, url: new URL(item.dataset.full, location.href).href };
    $("lookImg").src = img.currentSrc || img.src;
    $("lookText").textContent = img.alt;
    lookChip.hidden = false;
  }
  function clearLook() { look = null; lookChip.hidden = true; }
  $("lbRequest").addEventListener("click", function () {
    var it = visible()[current];
    if (!it) return;
    setLook(it);
    box.close();
    scrollToEl($("book"));
    announce(T.lookAdded);
    setTimeout(function () { $("f-name").focus({ preventScroll: true }); }, reduceMotion ? 0 : 600);
  });
  $("lookRemove").addEventListener("click", clearLook);

  /* ---------- Time list (24-hour start times, asked from the mock server) ---------- */
  var hintDefault = hint.textContent;
  var pickText = timeEl.options[0].textContent;
  var SLOT = CFG.slotMinutes || 15;
  dateEl.min = ymd(new Date());
  function fillTimes(slots, keep) {
    timeEl.textContent = "";
    var first = document.createElement("option");
    first.value = ""; first.textContent = pickText;
    timeEl.appendChild(first);
    slots.forEach(function (s) { var o = document.createElement("option"); o.value = o.textContent = s; timeEl.appendChild(o); });
    timeEl.value = keep;
  }
  function label(m) { return pad(Math.floor(m / 60)) + ":" + pad(m % 60); }
  function updateTimes() {
    var keep = timeEl.value, dur = visitMinutes(), token = ++tick, known = chosen().length > 0;
    if (!dateEl.value) {
      var h = CFG.hours.weekday, slots = [];
      for (var m = toMinutes(h[0]); m + dur <= toMinutes(h[1]); m += SLOT) slots.push(label(m));
      fillTimes(slots, keep);
      hint.textContent = known ? T.hintNoDate.replace("{d}", fmtMin(dur)) : hintDefault;
      return Promise.resolve();
    }
    hint.textContent = T.checking;
    return API.availability(dateEl.value, dur).then(function (res) {
      if (token !== tick) return;
      fillTimes(res.slots, keep);
      if (!res.slots.length) { hint.textContent = T.noSlots; return; }
      var all = Math.floor((toMinutes(res.close) - toMinutes(res.open) - dur) / SLOT) + 1;
      hint.textContent = T.hint.replace("{a}", res.slots[0]).replace("{b}", res.slots[res.slots.length - 1])
        .replace("{d}", fmtMin(dur)).replace("{c}", res.close) + (res.slots.length < all ? " " + T.someTaken : "");
    }, function () { if (token === tick) hint.textContent = T.availError; });
  }
  dateEl.addEventListener("input", updateTimes);
  dateEl.addEventListener("change", updateTimes);
  updateTimes();

  /* ---------- Quick picks: the next free times, across the next days ---------- */
  var quickList = $("quickList"), quickHint = $("quickHint"), quickToken = 0;
  function pickSlot(date, time) {
    dateEl.value = date;
    updateTimes().then(function () {
      timeEl.value = time;
      Array.prototype.forEach.call(quickList.children, function (b) { b.setAttribute("aria-pressed", b.dataset.date === date && b.dataset.time === time ? "true" : "false"); });
      announce(T.picked);
    });
  }
  function renderQuick() {
    var token = ++quickToken, dur = visitMinutes(), start = new Date(), found = [];
    quickHint.textContent = T.checking;
    function tryDay(i) {
      if (token !== quickToken) return;
      if (found.length >= 6 || i > 13) return finish();
      var d = new Date(start.getFullYear(), start.getMonth(), start.getDate() + i);
      API.availability(ymd(d), dur).then(function (res) {
        if (token !== quickToken) return;
        var s = res.slots;
        if (s.length) {
          var pick = [s[0]];
          if (s.length > 6) pick.push(s[Math.floor(s.length / 2)]);
          pick.forEach(function (t) { if (found.length < 6) found.push({ i: i, d: d, t: t }); });
        }
        tryDay(i + 1);
      }, finish);
    }
    function finish() {
      if (token !== quickToken) return;
      quickList.textContent = "";
      found.forEach(function (f) {
        var b = el("button", "", whenText(f.i, f.d, f.t)); b.type = "button";
        b.dataset.date = ymd(f.d); b.dataset.time = f.t; b.setAttribute("aria-pressed", "false");
        b.addEventListener("click", function () { pickSlot(b.dataset.date, b.dataset.time); });
        quickList.appendChild(b);
      });
      quickHint.textContent = found.length ? T.quickHint : T.quickNone;
    }
    tryDay(0);
  }
  renderQuick();

  /* ---------- Hero tiles: open today, next free time ---------- */
  function updateOpen() {
    var now = new Date(), h = dayHours(now), m = now.getHours() * 60 + now.getMinutes(), big = $("openBig"), text, open = false;
    if (m >= toMinutes(h[0]) && m < toMinutes(h[1])) { open = true; text = T.openUntil.replace("{t}", h[1]); }
    else if (m < toMinutes(h[0])) text = T.closedLater.replace("{t}", h[0]);
    else text = T.closedTomorrow.replace("{t}", dayHours(new Date(now.getTime() + 864e5))[0]);
    big.textContent = text; big.classList.toggle("off", !open);
  }
  updateOpen();
  setInterval(updateOpen, 60000);
  var nextSlot = null;
  function findNext() {
    var start = new Date();
    function tryDay(i) {
      if (i > 13) { $("nextBig").textContent = "–"; return; }
      var d = new Date(start.getFullYear(), start.getMonth(), start.getDate() + i);
      API.availability(ymd(d), 60).then(function (res) {
        if (!res.slots.length) return tryDay(i + 1);
        nextSlot = { date: ymd(d), time: res.slots[0] };
        $("nextBig").textContent = whenText(i, d, res.slots[0]);
        $("nextBtn").hidden = false;
      }, function () { $("nextBig").textContent = "–"; });
    }
    tryDay(0);
  }
  $("nextBtn").addEventListener("click", function () {
    if (!nextSlot) return;
    scrollToEl($("book"));
    pickSlot(nextSlot.date, nextSlot.time);
  });
  findNext();

  /* ---------- Sending the request (talks to LumiAPI: a mock server now, a real backend later) ---------- */
  var submitBtn = $("submitBtn"), sendLabel = submitBtn.querySelector(".btn-label").textContent;
  var formError = $("formError"), formDone = $("formDone"), demoNote = $("demoNote");
  var busy = false;
  if (API.mode === "demo") { demoNote.hidden = false; demoNote.textContent = T.demoLine; }
  function setBusy(on) {
    busy = on;
    submitBtn.disabled = on;
    submitBtn.classList.toggle("is-busy", on);
    form.setAttribute("aria-busy", on ? "true" : "false");
    submitBtn.querySelector(".btn-label").textContent = on ? T.sending : sendLabel;
  }
  function buildPayload() {
    var t = totals(), d = new FormData(form);
    return {
      name: String(d.get("name")).trim(), phone: String(d.get("phone")).trim(), service: t.names.join(", "),
      plan: { summary: t.names.join(" + ") + ". " + T.about + " " + fmtRange(t.mmin, t.mmax, fmtMin) + ", " + priceText(t),
              minPrice: t.pmin, maxPrice: t.pmax, minMinutes: t.mmin, maxMinutes: t.mmax, extras: t.names.slice(1), priceOnRequest: t.request },
      date: d.get("date"), time: d.get("time"), durationMinutes: visitMinutes(),
      look: look ? { alt: look.alt, url: look.url } : null,
      message: String(d.get("msg") || "").trim(), lang: lang
    };
  }
  function showError(msg) { formError.textContent = msg; formError.hidden = false; }
  function showForm() { formDone.hidden = true; form.hidden = false; }
  function showDone(rec, p) {
    var L = T.lines;
    formDone.textContent = "";
    formDone.appendChild(el("h3", "", T.doneH));
    var ref = el("p", "done-ref");
    ref.appendChild(el("span", "", T.doneRef));
    ref.appendChild(el("strong", "", rec.id));
    formDone.appendChild(ref);
    var st = el("p", "done-status");
    st.appendChild(el("span", "", T.doneStatus + ": "));
    st.appendChild(el("span", "pill", T.statusPending));
    formDone.appendChild(st);
    var dl = el("dl", "done-list");
    function row(k, v) { if (!v) return; dl.appendChild(el("dt", "", k)); dl.appendChild(el("dd", "", v)); }
    row(L.name, p.name); row(L.phone, p.phone); row(L.service, p.plan.summary);
    row(L.date, longDate(p.date)); row(L.time, p.time);
    if (p.look) row(L.look, p.look.alt);
    row(L.msg, p.message);
    formDone.appendChild(dl);
    formDone.appendChild(el("p", "", T.doneNext));
    var actions = el("div", "done-actions");
    if (API.mode === "demo") {
      formDone.appendChild(el("p", "demo-note", T.doneDemo));
      var link = el("a", "btn btn-main btn-sm", T.adminLink);
      var adm = document.querySelector('.foot a[href*="admin"]');
      link.href = adm ? adm.href : "admin.html";
      actions.appendChild(link);
    }
    var again = el("button", "btn btn-line btn-sm", T.again); again.type = "button";
    again.addEventListener("click", resetForm);
    actions.appendChild(again);
    formDone.appendChild(actions);
    form.hidden = true; formDone.hidden = false;
    scrollToEl(formDone);
    formDone.focus({ preventScroll: true });
    renderQuick(); findNext();
  }
  function resetForm() {
    form.reset();
    clearLook();
    svcInputs.forEach(function (c) { c.checked = false; });
    formError.hidden = true;
    showForm();
    renderBuilder(); updateTimes(); renderQuick();
    $("f-name").focus();
  }
  form.addEventListener("submit", function (e) {
    e.preventDefault();
    if (busy) return;
    formError.hidden = true;
    if (!chosen().length) { showError(T.errPick); return; }
    var name = $("f-name"), phone = $("f-phone");
    var missing = [name, phone, dateEl, timeEl].filter(function (n) { return !String(n.value).trim(); })[0];
    if (missing) { showError(T.errFields); missing.focus(); return; }
    var payload = buildPayload();
    setBusy(true);
    API.createRequest(payload).then(function (rec) {
      setBusy(false);
      showDone(rec, payload);
    }, function (er) {
      setBusy(false);
      if (er && er.code === "slot_taken") { showError(T.errTaken); timeEl.value = ""; updateTimes(); renderQuick(); }
      else showError(er && er.code === "invalid" ? T.errInvalid : T.errGeneric);
    });
  });

  renderBuilder();
})();
