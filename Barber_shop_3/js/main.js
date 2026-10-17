/* Hollis & Dane Barbers (design 3): page behaviour.
   Colour schemes, menu, work wall viewer, live "open now" and "next free chair", and the chair board (service, day, free squares by barber, details).
   The board talks to HollisAPI (js/api.js): a mock server now, a real backend later (docs/API.md). */
(function () {
  "use strict";

  var CFG = window.HOLLIS_CONFIG || {};
  var API = window.HollisAPI;
  var html = document.documentElement;
  var lang = html.lang === "bg" ? "bg" : "en";
  var reduceMotion = window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches;
  function $(id) { return document.getElementById(id); }

  var T = {
    bg: {
      mapTitle: "Карта на бръснарницата", locale: "bg-BG", hUnit: "ч", mUnit: "мин",
      opensNow: "Отворено · до {t}", openLater: "Затворено · отваря днес в {t}", openTomorrow: "Затворено · отваря утре в {t}",
      nextFree: "Първи свободен стол:", todayAt: "днес в {t}", tomorrowAt: "утре в {t}", dayAt: "{d} в {t}",
      checking: "Проверяваме свободните часове…", noSlots: "Няма свободни часове този ден. Избери друг ден.",
      boardHint: "{n} свободни квадратчета. Работим до {c}.", availError: "Не успяхме да проверим часовете. Опитай пак.",
      pickSlot: "Натисни свободно квадратче на таблото, за да избереш стол.", picked: "{b} · {d} · {t}",
      cellFree: "{b}, {t}: свободно", cellTaken: "{b}, {t}: заето",
      errSlot: "Избери свободно квадратче на таблото.", errName: "Въведи име и телефон.",
      errTaken: "Съжаляваме, този час току-що беше зает. Избери друг.", errInvalid: "Провери данните и опитай пак.", errGeneric: "Нещо се обърка. Опитай пак или ни се обади.",
      sending: "Изпращане…", demoLine: "Демо режим: заявките се пазят само в този браузър и нищо не се изпраща.",
      doneH: "Столът е запазен", doneRef: "Номер", statusPending: "Чака потвърждение",
      doneNext: "Ще се свържем с теб по телефона, за да потвърдим часа. Запази номера.",
      doneDemo: "Демо режим: нищо не беше изпратено. Заявката е записана само в този браузър.",
      adminLink: "Виж я в демо админ панела", again: "Запази още един час", send: "Запази този стол",
      lines: { service: "Услуга", extras: "Допълнения", barber: "Бръснар", date: "Дата", time: "Час", total: "Общо", name: "Име", phone: "Телефон", msg: "Съобщение", look: "Прическа" },
      about: "Около"
    },
    en: {
      mapTitle: "Map of the barbershop", locale: "en-GB", hUnit: "h", mUnit: "min",
      opensNow: "Open now · until {t}", openLater: "Closed · opens today at {t}", openTomorrow: "Closed · opens tomorrow at {t}",
      nextFree: "Next free chair:", todayAt: "today at {t}", tomorrowAt: "tomorrow at {t}", dayAt: "{d} at {t}",
      checking: "Checking free times…", noSlots: "No free times on this day. Please pick another day.",
      boardHint: "{n} free squares. We close at {c}.", availError: "We could not check the free times. Please try again.",
      pickSlot: "Press a free square on the board to choose a chair.", picked: "{b} · {d} · {t}",
      cellFree: "{b}, {t}: free", cellTaken: "{b}, {t}: taken",
      errSlot: "Please choose a free square on the board.", errName: "Please enter your name and phone.",
      errTaken: "Sorry, that time was just taken. Please choose another.", errInvalid: "Please check your details and try again.", errGeneric: "Something went wrong. Please try again or call us.",
      sending: "Sending…", demoLine: "Demo mode: bookings are kept in this browser only and nothing is sent.",
      doneH: "Your chair is booked", doneRef: "Reference", statusPending: "Waiting for confirmation",
      doneNext: "We will contact you by phone to confirm your time. Keep your reference handy.",
      doneDemo: "Demo mode: nothing was sent. The booking is saved only in this browser.",
      adminLink: "See it in the demo back office", again: "Book another time", send: "Book this chair",
      lines: { service: "Service", extras: "Extras", barber: "Barber", date: "Date", time: "Time", total: "Total", name: "Name", phone: "Phone", msg: "Message", look: "Cut" },
      about: "About"
    }
  }[lang];

  /* ---------- Small helpers ---------- */
  function pad(n) { return (n < 10 ? "0" : "") + n; }
  function ymd(d) { return d.getFullYear() + "-" + pad(d.getMonth() + 1) + "-" + pad(d.getDate()); }
  function toDate(v) { var p = v.split("-"); return new Date(+p[0], +p[1] - 1, +p[2]); }
  function toMinutes(hhmm) { var p = hhmm.split(":"); return +p[0] * 60 + +p[1]; }
  function toHHMM(m) { return pad(Math.floor(m / 60)) + ":" + pad(m % 60); }
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
  var SKINS = ["paper", "ink", "sage", "rose", "cobalt"];
  var skinBtns = document.querySelectorAll(".sw[data-skin]");
  var skinName = $("skinName");
  var animTimer;
  function setSkin(skin, save) {
    if (SKINS.indexOf(skin) === -1) skin = "paper";
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
    if (save) { try { localStorage.setItem("hollisSkin", skin); } catch (e) {} }
  }
  skinBtns.forEach(function (b) { b.addEventListener("click", function () { setSkin(b.dataset.skin, true); }); });
  var startSkin = null;
  try { startSkin = new URLSearchParams(location.search).get("skin") || localStorage.getItem("hollisSkin"); } catch (e) {}
  setSkin(startSkin || "paper", false);

  /* ---------- Masthead date ---------- */
  var mastDate = $("mastDate");
  if (mastDate) mastDate.textContent = mastDate.textContent + " · " + new Date().toLocaleDateString(T.locale, { weekday: "long", day: "numeric", month: "long", year: "numeric" });
  var yEl = $("year"); if (yEl) yEl.textContent = new Date().getFullYear();

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

  /* ---------- Scroll reveal ---------- */
  if (html.classList.contains("js-reveal")) {
    var groups = [[".sec-head", 0], [".pl-col", 0.08], [".bcard", 0.1], [".letter", 0.1], [".visit-grid > div", 0.1], [".clip-item", 0.05]];
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (!en.isIntersecting) return;
        io.unobserve(en.target);
        en.target.classList.add("in");
        setTimeout(function () { en.target.classList.remove("rv", "in"); en.target.style.removeProperty("--d"); }, 1300);
      });
    }, { threshold: 0.12, rootMargin: "0px 0px -6% 0px" });
    groups.forEach(function (g) {
      document.querySelectorAll(g[0]).forEach(function (n, i) {
        n.classList.add("rv");
        n.style.setProperty("--d", ((i % 4) * g[1]).toFixed(2) + "s");
        io.observe(n);
      });
    });
  }

  /* ---------- Photo viewer for the work wall ---------- */
  var items = Array.prototype.slice.call(document.querySelectorAll(".clip-item"));
  var box = $("lightbox"), lbImg = $("lbImg"), current = 0;
  function showPhoto(i) {
    current = (i + items.length) % items.length;
    var it = items[current], img = it.querySelector("img");
    lbImg.src = it.dataset.full;
    lbImg.alt = img.alt;
    lbImg.classList.remove("swap"); void lbImg.offsetWidth; lbImg.classList.add("swap");
    $("lbRequest").hidden = it.dataset.cat === "shop";   /* a photo of the shop itself is not a cut to book */
  }
  items.forEach(function (it, i) { it.addEventListener("click", function () { showPhoto(i); box.showModal(); }); });
  $("lbClose").addEventListener("click", function () { box.close(); });
  $("lbPrev").addEventListener("click", function () { showPhoto(current - 1); });
  $("lbNext").addEventListener("click", function () { showPhoto(current + 1); });
  box.addEventListener("click", function (e) { if (e.target === box || e.target.className === "lb-inner") box.close(); });
  box.addEventListener("keydown", function (e) {
    if (e.key === "ArrowLeft") showPhoto(current - 1);
    if (e.key === "ArrowRight") showPhoto(current + 1);
  });
  $("lbRequest").addEventListener("click", function () {
    var it = items[current], img = it.querySelector("img");
    box.close();
    openBoard({ look: { alt: img.alt, url: new URL(it.dataset.full, location.href).href, thumb: img.currentSrc || img.src } });
  });

  /* ---------- Map: loads only when the visitor asks ---------- */
  var mapBox = $("mapBox");
  $("mapLoad").addEventListener("click", function () {
    var f = document.createElement("iframe");
    f.src = mapBox.dataset.src; f.title = T.mapTitle; f.loading = "lazy";
    f.referrerPolicy = "no-referrer";
    mapBox.textContent = "";
    mapBox.appendChild(f);
  });

  /* ---------- Open now (from the opening hours) ---------- */
  function updateOpen() {
    var now = new Date(), h = dayHours(now), m = now.getHours() * 60 + now.getMinutes(), text, open = false;
    if (m >= toMinutes(h[0]) && m < toMinutes(h[1])) { open = true; text = T.opensNow.replace("{t}", h[1]); }
    else if (m < toMinutes(h[0])) text = T.openLater.replace("{t}", h[0]);
    else text = T.openTomorrow.replace("{t}", dayHours(new Date(now.getTime() + 864e5))[0]);
    [$("openNow"), $("statusBox")].forEach(function (n) { n.textContent = text; n.classList.toggle("off", !open); });
  }
  updateOpen();
  setInterval(updateOpen, 60000);

  /* ---------- Next free chair (asks the server, looks at the next 7 days) ---------- */
  var nextBox = $("nextFree");
  function findNext() {
    var start = new Date();
    function tryDay(i) {
      if (i > 6) return;
      var d = addDays(start, i);
      API.availability(ymd(d), 40, "any").then(function (res) {
        if (!res.slots.length) return tryDay(i + 1);
        var when = i === 0 ? T.todayAt : i === 1 ? T.tomorrowAt : T.dayAt;
        var slot = { date: ymd(d), time: res.slots[0] };
        nextBox.textContent = "";
        nextBox.appendChild(document.createTextNode(T.nextFree + " "));
        var b = el("button", "", when.replace("{t}", res.slots[0]).replace("{d}", shortDate(d)));
        b.type = "button";
        b.addEventListener("click", function () { openBoard({ date: slot.date }); });
        nextBox.appendChild(b);
        nextBox.hidden = false;
      }, function () {});
    }
    tryDay(0);
  }
  findNext();

  /* ================= Chair board ================= */
  var form = $("bookForm"), svcEl = $("b-svc"), board = $("board"), hint = $("boardHint"), strip = $("dayStrip");
  var chosenEl = $("chosen"), errEl = $("bkError"), sendBtn = $("bkSend"), done = $("bkDone");
  var today = new Date(); today = new Date(today.getFullYear(), today.getMonth(), today.getDate());
  var staff = Array.prototype.slice.call(document.querySelectorAll(".bcard")).map(function (c) {
    return { id: c.querySelector("[data-barber]").dataset.barber, name: c.querySelector("h3").textContent, img: c.querySelector("img").getAttribute("src") };
  });
  var barberIds = CFG.barbers && CFG.barbers.length ? CFG.barbers : staff.map(function (s) { return s.id; });
  var stripStart = today, date = ymd(today), sel = null, look = null, prefBarber = null, tick = 0, busy = false, finished = false;

  function opt() { return svcEl.options[svcEl.selectedIndex]; }
  function extras() { return Array.prototype.slice.call(form.querySelectorAll('input[name="extra"]:checked')); }
  function totals() {
    var o = opt(), price = +o.dataset.price, min = +o.dataset.min;
    extras().forEach(function (x) { price += +x.dataset.price; min += +x.dataset.min; });
    return { price: price, min: min };
  }
  function renderTotals() {
    var t = totals();
    var n = $("bkTotal");
    n.textContent = t.price + " €";
    n.appendChild(el("small", "", T.about + " " + fmtMin(t.min)));
  }

  function renderStrip() {
    strip.textContent = "";
    for (var i = 0; i < 7; i++) {
      var d = addDays(stripStart, i), v = ymd(d);
      var b = el("button", "day"); b.type = "button";
      b.setAttribute("aria-pressed", v === date ? "true" : "false");
      b.dataset.date = v;
      b.setAttribute("aria-label", longDate(v));
      b.appendChild(el("small", "", d.toLocaleDateString(T.locale, { weekday: "short" })));
      b.appendChild(el("b", "", String(d.getDate())));
      strip.appendChild(b);
    }
    $("dayPrev").disabled = stripStart <= today;
  }
  strip.addEventListener("click", function (e) {
    var b = e.target.closest(".day");
    if (!b) return;
    date = b.dataset.date; sel = null; renderStrip(); renderChosen(); loadBoard();
  });
  $("dayPrev").addEventListener("click", function () { stripStart = addDays(stripStart, -7); if (stripStart < today) stripStart = today; renderStrip(); });
  $("dayNext").addEventListener("click", function () { stripStart = addDays(stripStart, 7); renderStrip(); });

  /* free squares: one availability request per barber for the chosen day and visit length */
  function loadBoard() {
    var token = ++tick, t = totals(), d = toDate(date), h = dayHours(d), step = CFG.slotMinutes || 30;
    board.setAttribute("aria-busy", "true");
    hint.textContent = T.checking;
    Promise.all(barberIds.map(function (id) { return API.availability(date, t.min, id); })).then(function (all) {
      if (token !== tick) return;
      var free = {}, count = 0;
      all.forEach(function (r, i) { free[barberIds[i]] = r.slots; });
      var rows = [];
      for (var m = toMinutes(h[0]); m + t.min <= toMinutes(h[1]); m += step) rows.push(toHHMM(m));
      var firstFree = rows.findIndex(function (r) { return barberIds.some(function (id) { return free[id].indexOf(r) !== -1; }); });
      if (firstFree > 0) rows = rows.slice(firstFree);   /* today: skip the times that have already passed */
      board.textContent = "";
      board.style.setProperty("--n", barberIds.length);
      board.appendChild(el("div", "b-head"));
      barberIds.forEach(function (id) {
        var s = staff.filter(function (x) { return x.id === id; })[0] || { name: id, img: "" };
        var hd = el("div", "b-head" + (prefBarber === id ? " pref" : ""));
        if (s.img) { var im = el("img"); im.src = s.img; im.alt = ""; im.width = 38; im.height = 38; hd.appendChild(im); }
        hd.appendChild(el("span", "", s.name));
        board.appendChild(hd);
      });
      rows.forEach(function (time) {
        board.appendChild(el("div", "b-time", time));
        barberIds.forEach(function (id) {
          var s = staff.filter(function (x) { return x.id === id; })[0] || { name: id };
          var ok = free[id].indexOf(time) !== -1;
          var b = el("button", "cell", ok ? time : ""); b.type = "button";
          b.dataset.barber = id; b.dataset.time = time; b.disabled = !ok;
          b.setAttribute("aria-label", (ok ? T.cellFree : T.cellTaken).replace("{b}", s.name).replace("{t}", time));
          if (ok) count++;
          var on = sel && sel.barber === id && sel.time === time;
          b.setAttribute("aria-pressed", on ? "true" : "false");
          board.appendChild(b);
        });
      });
      if (sel && !board.querySelector('.cell[aria-pressed="true"]')) { sel = null; renderChosen(); }
      board.setAttribute("aria-busy", "false");
      hint.textContent = count ? T.boardHint.replace("{n}", count).replace("{c}", h[1]) : T.noSlots;
    }, function () { if (token === tick) { hint.textContent = T.availError; board.setAttribute("aria-busy", "false"); } });
  }
  board.addEventListener("click", function (e) {
    var b = e.target.closest(".cell");
    if (!b || b.disabled) return;
    sel = { barber: b.dataset.barber, time: b.dataset.time };
    Array.prototype.forEach.call(board.querySelectorAll(".cell"), function (c) { c.setAttribute("aria-pressed", c === b ? "true" : "false"); });
    if (!reduceMotion) { b.classList.remove("pop"); void b.offsetWidth; b.classList.add("pop"); }
    errEl.hidden = true;
    renderChosen();
    if (window.matchMedia("(max-width: 999px)").matches) scrollToEl($("bkMe"));
  });
  function barberName(id) { var s = staff.filter(function (x) { return x.id === id; })[0]; return s ? s.name : id; }
  function renderChosen() {
    chosenEl.textContent = sel ? T.picked.replace("{b}", barberName(sel.barber)).replace("{d}", longDate(date)).replace("{t}", sel.time) : T.pickSlot;
  }
  form.addEventListener("change", function (e) {
    if (e.target === svcEl || e.target.name === "extra") { renderTotals(); loadBoard(); }
  });

  $("lookRemove").addEventListener("click", function () { look = null; $("lookChip").hidden = true; });
  function showLook() {
    $("lookChip").hidden = !look;
    if (look) { $("lookImg").src = look.thumb || ""; $("lookText").textContent = look.alt; }
  }

  function fail(msg, focusEl) { errEl.textContent = msg; errEl.hidden = false; if (focusEl) focusEl.focus(); }
  function buildPayload() {
    var o = opt(), t = totals(), ex = extras().map(function (x) { return x.dataset.name; });
    return {
      name: $("b-name").value.trim(), phone: $("b-phone").value.trim(), service: o.dataset.name,
      plan: { summary: o.dataset.name + (ex.length ? " + " + ex.join(" + ") : "") + ". " + T.about + " " + fmtMin(t.min) + ", " + t.price + " €",
              minPrice: t.price, maxPrice: t.price, minMinutes: t.min, maxMinutes: t.min, extras: ex, priceOnRequest: false },
      barber: sel.barber, barberName: barberName(sel.barber),
      date: date, time: sel.time, durationMinutes: t.min,
      look: look ? { alt: look.alt, url: look.url } : null,
      message: $("b-msg").value.trim(), lang: lang
    };
  }
  function setBusy(on) {
    busy = on; sendBtn.disabled = on; sendBtn.classList.toggle("is-busy", on);
    sendBtn.textContent = on ? T.sending : T.send;
    form.setAttribute("aria-busy", on ? "true" : "false");
  }
  form.addEventListener("submit", function (e) {
    e.preventDefault();
    if (busy) return;
    if (!sel) { fail(T.errSlot, board.querySelector(".cell:not(:disabled)")); return; }
    if (!$("b-name").value.trim()) { fail(T.errName, $("b-name")); return; }
    if (!$("b-phone").value.trim()) { fail(T.errName, $("b-phone")); return; }
    errEl.hidden = true;
    var payload = buildPayload();
    setBusy(true);
    API.createRequest(payload).then(function (rec) { setBusy(false); showDone(rec, payload); }, function (er) {
      setBusy(false);
      if (er && er.code === "slot_taken") { sel = null; renderChosen(); fail(T.errTaken); loadBoard(); }
      else fail(er && er.code === "invalid" ? T.errInvalid : T.errGeneric);
    });
  });

  function showDone(rec, p) {
    var L = T.lines;
    finished = true;
    done.textContent = "";
    done.appendChild(el("h3", "", T.doneH));
    var ref = el("p", "done-ref");
    ref.appendChild(el("span", "", T.doneRef));
    ref.appendChild(el("strong", "", rec.id));
    done.appendChild(ref);
    var st = el("p", "done-status"); st.appendChild(el("span", "pill", T.statusPending)); done.appendChild(st);
    var dl = el("dl", "done-list");
    function row(k, v) { if (!v) return; dl.appendChild(el("dt", "", k)); dl.appendChild(el("dd", "", v)); }
    row(L.name, p.name); row(L.phone, p.phone); row(L.service, p.plan.summary); row(L.barber, p.barberName);
    row(L.date, longDate(p.date)); row(L.time, p.time);
    if (p.look) row(L.look, p.look.alt);
    row(L.msg, p.message);
    done.appendChild(dl);
    done.appendChild(el("p", "", T.doneNext));
    var actions = el("div", "done-actions");
    if (API.mode === "demo") {
      done.appendChild(el("p", "demo-note", T.doneDemo));
      var link = el("a", "btn btn-main btn-sm", T.adminLink);
      var adm = document.querySelector('.foot a[href*="admin"]');
      link.href = adm ? adm.href : "admin.html";
      actions.appendChild(link);
    }
    var again = el("button", "btn btn-line btn-sm", T.again); again.type = "button";
    again.addEventListener("click", function () { resetBooking(); scrollToEl($("book")); });
    actions.appendChild(again);
    done.appendChild(actions);
    form.hidden = true; done.hidden = false;
    done.focus({ preventScroll: true });
    scrollToEl(done);
    findNext();
  }
  function resetBooking() {
    form.reset();
    sel = null; look = null; finished = false; showLook();
    done.hidden = true; form.hidden = false; errEl.hidden = true;
    renderTotals(); renderChosen(); loadBoard();
  }

  /* opens the board; opts may preselect a service, a barber, a day or a photo */
  function openBoard(opts) {
    opts = opts || {};
    if (finished) resetBooking();
    if (opts.service) { svcEl.value = opts.service; renderTotals(); }
    prefBarber = opts.barber || prefBarber;
    if (opts.date) { date = opts.date; var d = toDate(date); stripStart = d < today ? today : d; sel = null; renderStrip(); renderChosen(); }
    if (opts.look) look = opts.look;
    showLook();
    if (API.mode === "demo") { $("demoNote").hidden = false; $("demoNote").textContent = T.demoLine; }
    loadBoard();
    scrollToEl($("book"));
  }
  document.addEventListener("click", function (e) {
    var b = e.target.closest("[data-book]");
    if (!b) return;
    e.preventDefault();
    openBoard({ service: b.dataset.service, barber: b.dataset.barber });
  });

  if (API.mode === "demo") { $("demoNote").hidden = false; $("demoNote").textContent = T.demoLine; }
  renderTotals(); renderStrip(); renderChosen(); loadBoard();
})();
