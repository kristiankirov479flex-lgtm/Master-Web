/* The Stone Cellar (design 3): page behaviour.
   Full-screen menu, photo viewer, a booking bar that steps aside, and the stay enquiry with a calendar that shows which days are busy.
   The enquiry talks to CellarAPI (js/api.js): a mock server now, a real backend later (docs/API.md). */
(function () {
  "use strict";

  var CFG = window.CELLAR_CONFIG || {};
  var API = window.CellarAPI;
  var html = document.documentElement;
  var lang = html.lang === "bg" ? "bg" : "en";
  var reduceMotion = window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches;
  function $(id) { return document.getElementById(id); }

  var T = {
    bg: {
      locale: "bg-BG", mapTitle: "Карта на къщата",
      night1: "{n} нощ", nightN: "{n} нощувки", free: "Свободно", taken: "Заето", small: "Твърде малко",
      found: "{nights} · свободни места: {r} от {t}", none: "Нищо не е свободно за тези дати. Опитайте други дати.",
      pickDates: "Изберете дни на пристигане и заминаване, за да видите какво е свободно.", checking: "Проверяваме…",
      availError: "Не успяхме да проверим. Опитайте пак.",
      calPickIn: "Изберете ден на пристигане", calPickOut: "Пристигане {a} · изберете ден на заминаване", calBoth: "{a} → {b} · {n}",
      dayLabel: "{d}, свободни места: {f} от {t}", dayFull: "{d}, изцяло заето",
      sumDates: "Дати", sumGuests: "Гости", sumRoom: "Място", sumPrice: "Цена", guestsN1: "1 гост", guestsN: "{n} гости", pickRoom: "Изберете място",
      total: "Общо около {t} €", perNight: "{p} € × {n}",
      errRoom: "Изберете свободно място.", errDates: "Изберете дни на пристигане и заминаване.", errName: "Въведете име и телефон.",
      errTaken: "Съжаляваме, мястото току-що беше заето за тези дати. Изберете друго.", errInvalid: "Проверете данните и опитайте пак.", errGeneric: "Нещо се обърка. Опитайте пак или ни се обадете.",
      sending: "Изпращане…", demoLine: "Демо режим: запитванията се пазят само в този браузър и нищо не се изпраща.",
      doneH: "Запитването е получено", doneRef: "Номер на запитването", statusPending: "Чака потвърждение",
      doneNext: "Ще се свържем с вас по телефона или имейла, за да потвърдим. Запазете номера. Нищо не е платено онлайн.",
      doneDemo: "Демо режим: нищо не беше изпратено. Запитването е записано само в този браузър.",
      adminLink: "Вижте го в демо админ панела", again: "Ново запитване",
      lines: { name: "Име", phone: "Телефон", email: "Имейл", room: "Място", dates: "Дати", guests: "Гости", total: "Общо", msg: "Съобщение" }
    },
    en: {
      locale: "en-GB", mapTitle: "Map of the house",
      night1: "{n} night", nightN: "{n} nights", free: "Free", taken: "Taken", small: "Too small",
      found: "{nights} · free places: {r} of {t}", none: "Nothing is free for these dates. Please try other dates.",
      pickDates: "Pick your arrival and departure days to see what is free.", checking: "Checking…",
      availError: "We could not check. Please try again.",
      calPickIn: "Pick your arrival day", calPickOut: "Arrival {a} · now pick your departure day", calBoth: "{a} → {b} · {n}",
      dayLabel: "{d}, {f} of {t} places free", dayFull: "{d}, fully booked",
      sumDates: "Dates", sumGuests: "Guests", sumRoom: "Place", sumPrice: "Price", guestsN1: "1 guest", guestsN: "{n} guests", pickRoom: "Choose a place",
      total: "About {t} € in total", perNight: "{p} € × {n}",
      errRoom: "Please choose a free place.", errDates: "Please pick your arrival and departure days.", errName: "Please enter your name and phone.",
      errTaken: "Sorry, that place was just taken for these dates. Please choose another.", errInvalid: "Please check your details and try again.", errGeneric: "Something went wrong. Please try again or call us.",
      sending: "Sending…", demoLine: "Demo mode: enquiries are kept in this browser only and nothing is sent.",
      doneH: "Enquiry received", doneRef: "Reference", statusPending: "Waiting for confirmation",
      doneNext: "We will contact you by phone or email to confirm. Keep your reference handy. Nothing was paid online.",
      doneDemo: "Demo mode: nothing was sent. The enquiry is saved only in this browser.",
      adminLink: "See it in the demo back office", again: "Make another enquiry",
      lines: { name: "Name", phone: "Phone", email: "Email", room: "Place", dates: "Dates", guests: "Guests", total: "Total", msg: "Message" }
    }
  }[lang];

  /* ---------- Small helpers ---------- */
  function pad(n) { return (n < 10 ? "0" : "") + n; }
  function ymd(d) { return d.getFullYear() + "-" + pad(d.getMonth() + 1) + "-" + pad(d.getDate()); }
  function toDate(v) { var p = v.split("-"); return new Date(+p[0], +p[1] - 1, +p[2]); }
  function nights(a, b) { return Math.round((toDate(b) - toDate(a)) / 864e5); }
  function shortDay(v) { return toDate(v).toLocaleDateString(T.locale, { weekday: "short", day: "numeric", month: "short" }); }
  function longDay(v) { return toDate(v).toLocaleDateString(T.locale, { weekday: "long", day: "numeric", month: "long" }); }
  function longDate(v) { return toDate(v).toLocaleDateString(T.locale, { weekday: "long", day: "numeric", month: "long", year: "numeric" }); }
  function nightsText(n) { return (n === 1 ? T.night1 : T.nightN).replace("{n}", n); }
  function guestsText(n) { return n === 1 ? T.guestsN1 : T.guestsN.replace("{n}", n); }
  function el(tag, cls, text) { var n = document.createElement(tag); if (cls) n.className = cls; if (text !== undefined) n.textContent = text; return n; }
  function scrollToEl(n) { n.scrollIntoView({ behavior: reduceMotion ? "auto" : "smooth", block: "start" }); }
  var yEl = $("year"); if (yEl) yEl.textContent = new Date().getFullYear();

  /* ---------- Top bar: solid after the cover ---------- */
  var hud = $("hud");
  function onScroll() { hud.classList.toggle("solid", window.scrollY > 40); }
  onScroll();
  addEventListener("scroll", onScroll, { passive: true });

  /* ---------- Full-screen menu ---------- */
  var menu = $("menu");
  $("menuBtn").addEventListener("click", function () { menu.showModal(); });
  $("menuClose").addEventListener("click", function () { menu.close(); });
  menu.addEventListener("click", function (e) { if (e.target.closest("a")) menu.close(); });

  /* ---------- Scroll reveal ---------- */
  if (html.classList.contains("js-reveal")) {
    var groups = [[".ch-head", 0], [".story-text", 0], [".story-photo", 0.1], [".do-grid li", 0.08], [".sq", 0.04], [".note", 0.1], [".cal", 0], [".pick", 0.1], [".visit > div", 0.1]];
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (!en.isIntersecting) return;
        io.unobserve(en.target);
        en.target.classList.add("in");
        setTimeout(function () { en.target.classList.remove("rv", "in"); en.target.style.removeProperty("--d"); }, 1400);
      });
    }, { threshold: 0.08, rootMargin: "0px 0px -6% 0px" });
    groups.forEach(function (g) {
      document.querySelectorAll(g[0]).forEach(function (n, i) {
        n.classList.add("rv");
        n.style.setProperty("--d", (Math.min(i, 6) * g[1]).toFixed(2) + "s");
        io.observe(n);
      });
    });
  }

  /* ---------- The booking bar steps aside while the booking section is on screen ---------- */
  var bar = $("bar");
  if ("IntersectionObserver" in window) {
    new IntersectionObserver(function (en) { bar.classList.toggle("away", en[0].isIntersecting); }, { threshold: 0.12 }).observe($("book"));
  }

  /* ---------- Gallery viewer ---------- */
  var tiles = Array.prototype.slice.call(document.querySelectorAll(".sq"));
  var box = $("lightbox"), lbImg = $("lbImg"), lbCap = $("lbCap"), current = 0;
  function showPhoto(i) {
    current = (i + tiles.length) % tiles.length;
    var t = tiles[current];
    lbImg.src = t.dataset.full; lbImg.alt = t.dataset.cap; lbCap.textContent = t.dataset.cap;
    lbImg.classList.remove("swap"); void lbImg.offsetWidth; lbImg.classList.add("swap");
  }
  tiles.forEach(function (t, i) { t.addEventListener("click", function () { showPhoto(i); box.showModal(); }); });
  $("lbClose").addEventListener("click", function () { box.close(); });
  $("lbPrev").addEventListener("click", function () { showPhoto(current - 1); });
  $("lbNext").addEventListener("click", function () { showPhoto(current + 1); });
  box.addEventListener("click", function (e) { if (e.target === box || e.target.className === "lb-inner") box.close(); });
  box.addEventListener("keydown", function (e) {
    if (e.key === "ArrowLeft") showPhoto(current - 1);
    if (e.key === "ArrowRight") showPhoto(current + 1);
  });

  /* ---------- Map: loads only when the visitor asks ---------- */
  var mapBox = $("mapBox");
  $("mapLoad").addEventListener("click", function () {
    var f = document.createElement("iframe");
    f.src = mapBox.dataset.src; f.title = T.mapTitle; f.loading = "lazy"; f.referrerPolicy = "no-referrer";
    mapBox.textContent = ""; mapBox.appendChild(f);
  });

  /* ================= Stay enquiry with a calendar ================= */
  var form = $("stayForm"), guestsEl = $("b-guests"), hint = $("nightsHint");
  var ucs = Array.prototype.slice.call(document.querySelectorAll(".uc"));
  var sumList = $("sumList"), sumTotal = $("sumTotal"), formError = $("formError"), done = $("stayDone"), demoNote = $("demoNote"), submitBtn = $("submitBtn");
  var sendLabel = submitBtn.querySelector(".btn-label").textContent;
  var today = new Date(); today = new Date(today.getFullYear(), today.getMonth(), today.getDate());
  var todayStr = ymd(today);
  var st = { a: "", b: "", first: new Date(today.getFullYear(), today.getMonth(), 1), occ: {}, places: (CFG.rooms || []).length };
  var tick = 0, busy = false;
  if (API.mode === "demo") { demoNote.hidden = false; demoNote.textContent = T.demoLine; }

  var wide = window.matchMedia ? matchMedia("(min-width: 640px)") : { matches: true };
  function monthsShown() { return wide.matches ? 2 : 1; }

  /* ----- the calendar ----- */
  function dayClass(k) {
    var f = st.occ[k];
    if (f === undefined || f >= st.places) return "";
    return f === 0 ? "full" : "part";
  }
  function renderCal() {
    var wrap = $("months"), n = monthsShown();
    wrap.textContent = "";
    for (var m = 0; m < n; m++) {
      var first = new Date(st.first.getFullYear(), st.first.getMonth() + m, 1);
      var month = el("div", "month");
      month.appendChild(el("h3", "", first.toLocaleDateString(T.locale, { month: "long", year: "numeric" })));
      var grid = el("div", "grid"); grid.setAttribute("role", "group"); grid.setAttribute("aria-label", first.toLocaleDateString(T.locale, { month: "long", year: "numeric" }));
      for (var w = 0; w < 7; w++) {
        var ref = new Date(2024, 0, 1 + w);   /* a Monday first */
        var h = el("span", "wd", ref.toLocaleDateString(T.locale, { weekday: "short" }).slice(0, 2)); h.setAttribute("aria-hidden", "true"); grid.appendChild(h);
      }
      for (var p = 0; p < (first.getDay() + 6) % 7; p++) grid.appendChild(el("span", "day pad"));
      var days = new Date(first.getFullYear(), first.getMonth() + 1, 0).getDate();
      for (var d = 1; d <= days; d++) {
        var date = new Date(first.getFullYear(), first.getMonth(), d), k = ymd(date);
        var cls = dayClass(k), past = date < today;
        var asArrival = !st.a || (st.a && st.b);
        var btn = el("button", "day" + (cls ? " " + cls : ""), String(d)); btn.type = "button"; btn.dataset.date = k;
        btn.disabled = past || (cls === "full" && (asArrival || k <= st.a));
        var f = st.occ[k];
        btn.setAttribute("aria-label", cls === "full" ? T.dayFull.replace("{d}", longDay(k)) : T.dayLabel.replace("{d}", longDay(k)).replace("{f}", f === undefined ? st.places : f).replace("{t}", st.places));
        if (k === st.a || k === st.b) { btn.classList.add("sel"); btn.setAttribute("aria-pressed", "true"); }
        else if (st.a && st.b && k > st.a && k < st.b) btn.classList.add("inr");
        grid.appendChild(btn);
      }
      month.appendChild(grid); wrap.appendChild(month);
    }
    $("calPrev").disabled = st.first <= new Date(today.getFullYear(), today.getMonth(), 1);
    var sel = $("calSel");
    sel.textContent = !st.a ? T.calPickIn : !st.b ? T.calPickOut.replace("{a}", shortDay(st.a)) : T.calBoth.replace("{a}", shortDay(st.a)).replace("{b}", shortDay(st.b)).replace("{n}", nightsText(nights(st.a, st.b)));
  }
  var occTick = 0;
  function loadOccupancy() {
    var t = ++occTick, n = monthsShown();
    var from = ymd(st.first), to = ymd(new Date(st.first.getFullYear(), st.first.getMonth() + n, 1));
    API.occupancy(from, to).then(function (res) {
      if (t !== occTick) return;
      st.places = res.places || st.places;
      Object.keys(res.free).forEach(function (k) { st.occ[k] = res.free[k]; });
      renderCal();
    }, function () {});
  }
  function moveMonth(delta) {
    st.first = new Date(st.first.getFullYear(), st.first.getMonth() + delta, 1);
    renderCal(); loadOccupancy();
  }
  $("calPrev").addEventListener("click", function () { moveMonth(-1); });
  $("calNext").addEventListener("click", function () { moveMonth(1); });
  $("months").addEventListener("click", function (e) {
    var b = e.target.closest("button.day"); if (!b || b.disabled) return;
    var k = b.dataset.date;
    if (!st.a || (st.a && st.b)) { st.a = k; st.b = ""; }
    else if (k > st.a) st.b = k;
    else { st.a = k; st.b = ""; }
    formError.hidden = true;
    renderCal(); search();
  });
  if (wide.addEventListener) wide.addEventListener("change", function () { renderCal(); loadOccupancy(); });

  /* ----- free places for the chosen days, asked from the (mock) server ----- */
  function chosenUnit() { return form.querySelector('input[name="room"]:checked'); }
  function setTag(uc, text) { uc.querySelector("[data-tag]").textContent = text; }
  function search() {
    var token = ++tick;
    if (!st.a || !st.b) {
      hint.textContent = T.pickDates;
      ucs.forEach(function (uc) { uc.classList.remove("off"); uc.querySelector("input").disabled = false; setTag(uc, ""); });
      renderSummary(); return Promise.resolve();
    }
    hint.textContent = T.checking;
    return API.availability(st.a, st.b, +guestsEl.value).then(function (res) {
      if (token !== tick) return;
      var free = 0;
      res.rooms.forEach(function (r) {
        var uc = form.querySelector('.uc[data-room="' + r.id + '"]'), inp = uc.querySelector("input");
        uc.classList.toggle("off", !r.free); inp.disabled = !r.free;
        if (!r.free && inp.checked) inp.checked = false;
        setTag(uc, r.free ? T.free : r.reason === "size" ? T.small : T.taken);
        if (r.free) free++;
      });
      hint.textContent = free ? T.found.replace("{nights}", nightsText(res.nights)).replace("{r}", free).replace("{t}", res.rooms.length) : T.none;
      renderSummary();
    }, function (er) { if (token === tick) hint.textContent = er && er.code === "invalid" ? er.message : T.availError; });
  }
  function renderSummary() {
    var room = chosenUnit();
    sumList.textContent = ""; sumTotal.textContent = "";
    function row(k, v) { sumList.appendChild(el("dt", "", k)); sumList.appendChild(el("dd", "", v)); }
    if (st.a && st.b) row(T.sumDates, shortDay(st.a) + " → " + shortDay(st.b) + " (" + nightsText(nights(st.a, st.b)) + ")");
    row(T.sumGuests, guestsText(+guestsEl.value));
    row(T.sumRoom, room ? room.dataset.name : T.pickRoom);
    if (room && st.a && st.b) { var n = nights(st.a, st.b), p = +room.dataset.price; row(T.sumPrice, T.perNight.replace("{p}", p).replace("{n}", n)); sumTotal.textContent = T.total.replace("{t}", p * n); }
  }
  form.addEventListener("change", function (e) { if (e.target === guestsEl) search(); else renderSummary(); formError.hidden = true; });

  /* "Choose dates for this room" on a card: choose it, set sensible days if there are none, and go to the calendar */
  document.querySelectorAll("button[data-unit]").forEach(function (btn) {
    btn.addEventListener("click", function () {
      if (!st.a || !st.b) {
        var d = new Date(today); d.setDate(d.getDate() + ((5 - d.getDay() + 7) % 7 || 7));   /* the next Friday */
        st.a = ymd(d); st.b = ymd(new Date(d.getTime() + 2 * 864e5)); st.first = new Date(d.getFullYear(), d.getMonth(), 1);
        renderCal(); loadOccupancy();
      }
      scrollToEl($("book"));
      search().then(function () {
        var inp = form.querySelector('.uc[data-room="' + btn.dataset.unit + '"] input');
        if (inp && !inp.disabled) { inp.checked = true; renderSummary(); }
      });
    });
  });

  function setBusy(on) {
    busy = on; submitBtn.disabled = on; submitBtn.classList.toggle("is-busy", on);
    form.setAttribute("aria-busy", on ? "true" : "false");
    submitBtn.querySelector(".btn-label").textContent = on ? T.sending : sendLabel;
  }
  function showError(msg, focusEl) { formError.textContent = msg; formError.hidden = false; if (focusEl) focusEl.focus(); }
  function showDone(rec, p, room) {
    var L = T.lines;
    done.textContent = "";
    done.appendChild(el("h3", "", T.doneH));
    var ref = el("p", "done-ref"); ref.appendChild(el("span", "", T.doneRef)); ref.appendChild(el("strong", "", rec.id)); done.appendChild(ref);
    var s = el("p"); s.appendChild(el("span", "pill", T.statusPending)); done.appendChild(s);
    var dl = el("dl", "done-list");
    function row(k, v) { if (!v) return; dl.appendChild(el("dt", "", k)); dl.appendChild(el("dd", "", v)); }
    row(L.name, p.name); row(L.phone, p.phone); row(L.email, p.email); row(L.room, room.dataset.name);
    row(L.dates, longDate(p.checkin) + " → " + longDate(p.checkout) + " (" + nightsText(nights(p.checkin, p.checkout)) + ")");
    row(L.guests, guestsText(p.guests));
    row(L.total, T.total.replace("{t}", +room.dataset.price * nights(p.checkin, p.checkout)));
    row(L.msg, p.message);
    done.appendChild(dl);
    done.appendChild(el("p", "", T.doneNext));
    var actions = el("div", "done-actions");
    if (API.mode === "demo") {
      done.appendChild(el("p", "demo-note", T.doneDemo));
      var link = el("a", "btn btn-wine btn-sm", T.adminLink);
      var adm = document.querySelector('.foot a[href*="admin"]'); link.href = adm ? adm.href : "admin.html";
      actions.appendChild(link);
    }
    var again = el("button", "btn btn-line btn-sm", T.again); again.type = "button";
    again.addEventListener("click", function () { form.reset(); st.a = ""; st.b = ""; done.hidden = true; form.hidden = false; renderCal(); search(); scrollToEl($("book")); });
    actions.appendChild(again); done.appendChild(actions);
    form.hidden = true; done.hidden = false;
    scrollToEl(done); done.focus({ preventScroll: true });
    loadOccupancy();   /* the calendar now shows the new stay */
  }

  form.addEventListener("submit", function (e) {
    e.preventDefault();
    if (busy) return;
    formError.hidden = true;
    var room = chosenUnit();
    if (!st.a || !st.b) { showError(T.errDates); return; }
    if (!room) { showError(T.errRoom); return; }
    var nm = $("b-name"), ph = $("b-phone");
    if (!nm.value.trim()) { showError(T.errName, nm); return; }
    if (!ph.value.trim()) { showError(T.errName, ph); return; }
    var payload = { name: nm.value.trim(), phone: ph.value.trim(), email: $("b-email").value.trim(), room: room.value, checkin: st.a, checkout: st.b, guests: +guestsEl.value, message: $("b-msg").value.trim(), lang: lang };
    setBusy(true);
    API.createEnquiry(payload).then(function (rec) {
      setBusy(false); showDone(rec, payload, room);
    }, function (er) {
      setBusy(false);
      if (er && er.code === "room_taken") { showError(T.errTaken); search(); loadOccupancy(); }
      else showError(er && er.code === "invalid" ? T.errInvalid : T.errGeneric);
    });
  });

  renderCal(); loadOccupancy(); renderSummary();
})();
