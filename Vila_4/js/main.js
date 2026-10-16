/* Blue Heron (design 4): page behaviour.
   Map and place list, a booking timeline (one row per place, one column per night), persona tabs, sunrise and sunset, a dock that follows the scroll.
   The enquiry talks to LakeAPI (js/api.js): a mock server now, a real backend later (docs/API.md). */
(function () {
  "use strict";

  var CFG = window.LAKE_CONFIG || {};
  var API = window.LakeAPI;
  var html = document.documentElement;
  var lang = html.lang === "bg" ? "bg" : "en";
  var reduceMotion = window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches;
  function $(id) { return document.getElementById(id); }

  var T = {
    bg: {
      locale: "bg-BG", mapTitle: "Карта на езерото",
      night1: "{n} нощ", nightN: "{n} нощувки", guestsN1: "1 гост", guestsN: "{n} гости",
      sunrise: "Изгрев", sunset: "залез днес",
      pick: "Изберете нощ на пристигане", pickOut: "Пристигане {a} · изберете нощ на заминаване", both: "{a} → {b} · {n}",
      hintPick: "Натиснете свободна клетка в реда на мястото, което искате. Второ натискане избира деня на заминаване.",
      hintOut: "Сега натиснете деня на заминаване в същия ред.", hintBlocked: "Между двете дати има заета нощ. Изберете наново.",
      hintDone: "Готово. Попълнете данните по-долу.", hintSmall: "Това място е твърде малко за {n}.", loadErr: "Не успяхме да заредим заетостта. Опитайте пак.",
      cellFree: "{p}, {d}: свободно", cellTaken: "{p}, {d}: заето", cellSmall: "{p}, {d}: твърде малко за избрания брой гости",
      upTo: "до {n} гости", perNight: "{p} € / нощ", pickRoom: "Изберете място и дати",
      sumPlace: "Място", sumDates: "Дати", sumGuests: "Гости", sumPrice: "Цена", total: "Общо около {t} €", pn: "{p} € × {n}",
      errPick: "Изберете място и дати в графика.", errName: "Въведете име и телефон.",
      errTaken: "Съжаляваме, мястото току-що беше заето за тези дати. Изберете друго.", errInvalid: "Проверете данните и опитайте пак.", errGeneric: "Нещо се обърка. Опитайте пак или ни се обадете.",
      sending: "Изпращане…", demoLine: "Демо режим: запитванията се пазят само в този браузър и нищо не се изпраща.",
      doneH: "Запитването е получено", doneRef: "Номер на запитването", statusPending: "Чака потвърждение",
      doneNext: "Ще се свържем с вас по телефона или имейла, за да потвърдим. Запазете номера. Нищо не е платено онлайн.",
      doneDemo: "Демо режим: нищо не беше изпратено. Запитването е записано само в този браузър.",
      adminLink: "Вижте го в демо админ панела", again: "Ново запитване",
      prev: "Предишни дни", lines: { name: "Име", phone: "Телефон", email: "Имейл", room: "Място", dates: "Дати", guests: "Гости", total: "Общо", msg: "Съобщение" }
    },
    en: {
      locale: "en-GB", mapTitle: "Map of the lake",
      night1: "{n} night", nightN: "{n} nights", guestsN1: "1 guest", guestsN: "{n} guests",
      sunrise: "Sunrise", sunset: "sunset today",
      pick: "Pick your arrival night", pickOut: "Arrival {a} · now pick your departure day", both: "{a} → {b} · {n}",
      hintPick: "Press a free cell in the row of the place you want. A second press picks the departure day.",
      hintOut: "Now press the departure day in the same row.", hintBlocked: "There is a booked night in between. Please pick again.",
      hintDone: "Done. Fill in your details below.", hintSmall: "That place is too small for {n}.", loadErr: "We could not load the bookings. Please try again.",
      cellFree: "{p}, {d}: free", cellTaken: "{p}, {d}: booked", cellSmall: "{p}, {d}: too small for the chosen guests",
      upTo: "up to {n} guests", perNight: "{p} € / night", pickRoom: "Choose a place and dates",
      sumPlace: "Place", sumDates: "Dates", sumGuests: "Guests", sumPrice: "Price", total: "About {t} € in total", pn: "{p} € × {n}",
      errPick: "Please choose a place and dates on the timeline.", errName: "Please enter your name and phone.",
      errTaken: "Sorry, that place was just taken for these dates. Please choose another.", errInvalid: "Please check your details and try again.", errGeneric: "Something went wrong. Please try again or call us.",
      sending: "Sending…", demoLine: "Demo mode: enquiries are kept in this browser only and nothing is sent.",
      doneH: "Enquiry received", doneRef: "Reference", statusPending: "Waiting for confirmation",
      doneNext: "We will contact you by phone or email to confirm. Keep your reference handy. Nothing was paid online.",
      doneDemo: "Demo mode: nothing was sent. The enquiry is saved only in this browser.",
      adminLink: "See it in the demo back office", again: "Make another enquiry",
      prev: "Earlier days", lines: { name: "Name", phone: "Phone", email: "Email", room: "Place", dates: "Dates", guests: "Guests", total: "Total", msg: "Message" }
    }
  }[lang];

  /* ---------- Helpers ---------- */
  function pad(n) { return (n < 10 ? "0" : "") + n; }
  function ymd(d) { return d.getFullYear() + "-" + pad(d.getMonth() + 1) + "-" + pad(d.getDate()); }
  function toDate(v) { var p = v.split("-"); return new Date(+p[0], +p[1] - 1, +p[2]); }
  function addDays(d, n) { return new Date(d.getFullYear(), d.getMonth(), d.getDate() + n); }
  function nights(a, b) { return Math.round((toDate(b) - toDate(a)) / 864e5); }
  function shortDay(v) { return toDate(v).toLocaleDateString(T.locale, { weekday: "short", day: "numeric", month: "short" }); }
  function longDay(v) { return toDate(v).toLocaleDateString(T.locale, { weekday: "long", day: "numeric", month: "long" }); }
  function longDate(v) { return toDate(v).toLocaleDateString(T.locale, { weekday: "long", day: "numeric", month: "long", year: "numeric" }); }
  function nightsText(n) { return (n === 1 ? T.night1 : T.nightN).replace("{n}", n); }
  function guestsText(n) { return n === 1 ? T.guestsN1 : T.guestsN.replace("{n}", n); }
  function el(tag, cls, text) { var n = document.createElement(tag); if (cls) n.className = cls; if (text !== undefined) n.textContent = text; return n; }
  function scrollToEl(n) { n.scrollIntoView({ behavior: reduceMotion ? "auto" : "smooth", block: "start" }); }
  var yEl = $("year"); if (yEl) yEl.textContent = new Date().getFullYear();

  /* ---------- Sunrise and sunset (NOAA formula, local time of the visitor's browser) ---------- */
  function sunTimes(date, lat, lon) {
    var rad = Math.PI / 180;
    var start = new Date(date.getFullYear(), 0, 0);
    var doy = Math.floor((date - start) / 864e5);
    var g = (2 * Math.PI / 365) * (doy - 1);
    var eqt = 229.18 * (0.000075 + 0.001868 * Math.cos(g) - 0.032077 * Math.sin(g) - 0.014615 * Math.cos(2 * g) - 0.040849 * Math.sin(2 * g));
    var decl = 0.006918 - 0.399912 * Math.cos(g) + 0.070257 * Math.sin(g) - 0.006758 * Math.cos(2 * g) + 0.000907 * Math.sin(2 * g) - 0.002697 * Math.cos(3 * g) + 0.00148 * Math.sin(3 * g);
    var cosH = Math.cos(90.833 * rad) / (Math.cos(lat * rad) * Math.cos(decl)) - Math.tan(lat * rad) * Math.tan(decl);
    if (cosH > 1 || cosH < -1) return null;
    var ha = Math.acos(cosH) / rad;
    var utcOff = -date.getTimezoneOffset();
    function at(h) { var m = 720 - 4 * (lon + h) - eqt + utcOff; return new Date(date.getFullYear(), date.getMonth(), date.getDate(), 0, Math.round(m)); }
    return { rise: at(ha), set: at(-ha) };
  }
  (function () {
    var node = $("sun"), p = CFG.place;
    if (!node || !p) return;
    var s = sunTimes(new Date(), p.lat, p.lon);
    if (!s) return;
    function f(d) { return d.toLocaleTimeString(T.locale, { hour: "2-digit", minute: "2-digit" }); }
    node.appendChild(document.createTextNode("☀ " + T.sunrise + " "));
    node.appendChild(el("b", "", f(s.rise)));
    node.appendChild(document.createTextNode(" · "));
    node.appendChild(el("b", "", f(s.set)));
    node.appendChild(document.createTextNode(" " + T.sunset));
  })();

  /* ---------- Dock: highlight the section on screen ---------- */
  var dockLinks = Array.prototype.slice.call(document.querySelectorAll("#dock a"));
  if ("IntersectionObserver" in window && dockLinks.length) {
    var secs = dockLinks.map(function (a) { return document.getElementById(a.getAttribute("href").replace("#", "")); }).filter(Boolean);
    var spy = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (!en.isIntersecting) return;
        dockLinks.forEach(function (a) {
          if (a.getAttribute("href") === "#" + en.target.id) a.setAttribute("aria-current", "true"); else a.removeAttribute("aria-current");
        });
      });
    }, { rootMargin: "-45% 0px -50% 0px" });
    secs.forEach(function (s) { spy.observe(s); });
  }

  /* ---------- Scroll reveal ---------- */
  if (html.classList.contains("js-reveal")) {
    var groups = [[".sec-head", 0], [".explore", 0], [".places", 0.1], [".room", 0.08], [".board-wrap", 0], [".form-side", 0.1], [".persona-tabs", 0], [".bub", 0.1], [".visit > div", 0.1]];
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (!en.isIntersecting) return;
        io.unobserve(en.target);
        en.target.classList.add("in");
        setTimeout(function () { en.target.classList.remove("rv", "in"); en.target.style.removeProperty("--d"); }, 1400);
      });
    }, { threshold: 0.06, rootMargin: "0px 0px -5% 0px" });
    groups.forEach(function (g) {
      document.querySelectorAll(g[0]).forEach(function (n, i) {
        n.classList.add("rv");
        n.style.setProperty("--d", (Math.min(i, 5) * g[1]).toFixed(2) + "s");
        io.observe(n);
      });
    });
  }

  /* ---------- The map and the place list share one panel ---------- */
  var hots = Array.prototype.slice.call(document.querySelectorAll(".hot"));
  var places = Array.prototype.slice.call(document.querySelectorAll(".place"));
  function showPlace(i) {
    var p = places[i]; if (!p) return;
    var img = $("panelImg");
    img.src = p.dataset.photo; img.height = +p.dataset.h || 533;
    $("panelNo").textContent = String(i + 1);
    $("panelH").textContent = p.dataset.title;
    $("panelP").textContent = p.dataset.text;
    hots.forEach(function (h, k) { var on = k === i; h.classList.toggle("on", on); h.setAttribute("aria-pressed", on ? "true" : "false"); });
    places.forEach(function (b, k) { var on = k === i; b.classList.toggle("on", on); b.setAttribute("aria-pressed", on ? "true" : "false"); });
  }
  hots.forEach(function (h) { h.addEventListener("click", function () { showPlace(+h.dataset.i); }); });
  places.forEach(function (b) { b.addEventListener("click", function () { showPlace(+b.dataset.i); }); });

  /* ---------- Persona tabs ---------- */
  var ptabs = Array.prototype.slice.call(document.querySelectorAll(".ptab"));
  function selectTab(t, focus) {
    ptabs.forEach(function (x) {
      var on = x === t;
      x.setAttribute("aria-selected", on ? "true" : "false"); x.tabIndex = on ? 0 : -1;
      $(x.getAttribute("aria-controls")).hidden = !on;
    });
    if (focus) t.focus();
  }
  ptabs.forEach(function (t, i) {
    t.addEventListener("click", function () { selectTab(t); });
    t.addEventListener("keydown", function (e) {
      var n = e.key === "ArrowRight" ? i + 1 : e.key === "ArrowLeft" ? i - 1 : e.key === "Home" ? 0 : e.key === "End" ? ptabs.length - 1 : null;
      if (n === null) return;
      e.preventDefault(); selectTab(ptabs[(n + ptabs.length) % ptabs.length], true);
    });
  });

  /* ---------- Map: loads only when the visitor asks ---------- */
  var mapBox = $("mapBox");
  $("mapLoad").addEventListener("click", function () {
    var f = document.createElement("iframe");
    f.src = mapBox.dataset.src; f.title = T.mapTitle; f.loading = "lazy"; f.referrerPolicy = "no-referrer";
    mapBox.textContent = ""; mapBox.appendChild(f);
  });

  /* ================= Booking timeline ================= */
  var DAYS = 28;
  var form = $("stayForm"), guestsEl = $("b-guests"), board = $("board"), hint = $("boardHint"), selEl = $("boardSel");
  var sumList = $("sumList"), sumTotal = $("sumTotal"), formError = $("formError"), done = $("stayDone"), demoNote = $("demoNote"), submitBtn = $("submitBtn");
  var sendLabel = submitBtn.querySelector(".btn-label").textContent;
  var today = new Date(); today = new Date(today.getFullYear(), today.getMonth(), today.getDate());
  var names = {};
  document.querySelectorAll("button[data-unit]").forEach(function (b) {
    var h = b.closest(".room").querySelector("h3");
    names[b.dataset.unit] = h ? h.textContent : b.dataset.unit;
  });
  var rooms = (CFG.rooms || []).map(function (r) { return { id: r.id, guests: r.guests, price: r.price, name: names[r.id] || r.id }; });
  var st = { start: today, taken: {}, room: "", a: "", b: "" };   /* taken[roomId][date] = true */
  var busy = false, loadTick = 0;
  if (API.mode === "demo") { demoNote.hidden = false; demoNote.textContent = T.demoLine; }

  function roomById(id) { for (var i = 0; i < rooms.length; i++) if (rooms[i].id === id) return rooms[i]; return null; }
  function isTaken(id, k) { return !!(st.taken[id] && st.taken[id][k]); }
  function tooSmall(r) { return +guestsEl.value > r.guests; }
  /* Nights a..b (b not included) are all free in this room? */
  function rangeFree(id, a, b) {
    for (var d = toDate(a); ymd(d) < b; d = addDays(d, 1)) if (isTaken(id, ymd(d))) return false;
    return true;
  }

  function renderBoard() {
    board.textContent = "";
    board.style.setProperty("--n", DAYS);
    var todayK = ymd(today);
    /* month labels over the first day of each month */
    var prevM = -1;
    for (var i = 0; i < DAYS; i++) {
      var d = addDays(st.start, i);
      if (d.getMonth() !== prevM || i === 0) {
        prevM = d.getMonth();
        var m = el("span", "b-month", d.toLocaleDateString(T.locale, { month: "long", year: "numeric" }));
        var left = Math.min(DAYS - i, new Date(d.getFullYear(), d.getMonth() + 1, 0).getDate() - d.getDate() + 1);
        m.style.gridArea = "1 / " + (i + 2) + " / 2 / span " + left;
        board.appendChild(m);
      }
    }
    var corner = el("span", "b-corner"); corner.style.gridArea = "2 / 1"; board.appendChild(corner);
    for (var j = 0; j < DAYS; j++) {
      var dd = addDays(st.start, j), we = dd.getDay() === 0 || dd.getDay() === 6;
      var h = el("span", "b-head" + (we ? " we" : ""));
      h.appendChild(document.createTextNode(dd.toLocaleDateString(T.locale, { weekday: "short" }).slice(0, 2)));
      h.appendChild(el("b", "", String(dd.getDate())));
      h.style.gridArea = "2 / " + (j + 2);
      board.appendChild(h);
    }
    rooms.forEach(function (r, ri) {
      var small = tooSmall(r), row = ri + 3;
      var nm = el("div", "b-name"); nm.appendChild(el("b", "", r.name));
      nm.appendChild(el("small", "", T.upTo.replace("{n}", r.guests) + " · " + T.perNight.replace("{p}", r.price)));
      nm.style.gridArea = row + " / 1";
      board.appendChild(nm);
      for (var k = 0; k < DAYS; k++) {
        var day = addDays(st.start, k), key = ymd(day);
        var c = el("button", "c"); c.type = "button"; c.dataset.room = r.id; c.dataset.date = key; c.style.gridArea = row + " / " + (k + 2);
        var past = key < todayK, taken = isTaken(r.id, key);
        var label = shortDay(key);
        if (past) { c.className += " past"; c.disabled = true; c.setAttribute("aria-label", r.name + ", " + label); }
        else if (taken) {
          c.className += " taken";
          /* the second click may still land on a booked day: that is a departure morning */
          c.setAttribute("aria-label", T.cellTaken.replace("{p}", r.name).replace("{d}", label));
        } else if (small) { c.className += " dim"; c.setAttribute("aria-label", T.cellSmall.replace("{p}", r.name).replace("{d}", label)); }
        else c.setAttribute("aria-label", T.cellFree.replace("{p}", r.name).replace("{d}", label));
        if (r.id === st.room && st.a) {
          if (key === st.a || (st.b && key === st.b)) { c.className += " sel"; c.setAttribute("aria-pressed", "true"); }
          else if (st.b && key > st.a && key < st.b) c.className += " inr";
        }
        board.appendChild(c);
      }
    });
    $("boardPrev").disabled = ymd(st.start) <= ymd(today);
    selEl.textContent = !st.a ? T.pick : !st.b ? T.pickOut.replace("{a}", shortDay(st.a)) : T.both.replace("{a}", shortDay(st.a)).replace("{b}", shortDay(st.b)).replace("{n}", nightsText(nights(st.a, st.b)));
    renderSummary();
  }

  function loadBoard() {
    var t = ++loadTick;
    API.timeline(ymd(st.start), ymd(addDays(st.start, DAYS + 1))).then(function (res) {
      if (t !== loadTick) return;
      st.taken = {};
      res.places.forEach(function (p) { var m = st.taken[p.id] = {}; p.taken.forEach(function (k) { m[k] = true; }); });
      /* a chosen range that has just become busy is dropped */
      if (st.room && st.a && st.b && !rangeFree(st.room, st.a, st.b)) { st.a = ""; st.b = ""; st.room = ""; }
      renderBoard();
    }, function () { hint.textContent = T.loadErr; });
  }

  function shift(delta) {
    var s = addDays(st.start, delta);
    if (ymd(s) < ymd(today)) s = today;
    st.start = s; renderBoard(); loadBoard();
  }
  $("boardPrev").addEventListener("click", function () { shift(-14); });
  $("boardNext").addEventListener("click", function () { shift(14); });

  board.addEventListener("click", function (e) {
    var c = e.target.closest("button.c"); if (!c || c.disabled) return;
    var id = c.dataset.room, k = c.dataset.date, r = roomById(id);
    formError.hidden = true;
    if (tooSmall(r)) { hint.textContent = T.hintSmall.replace("{n}", guestsText(+guestsEl.value)); return; }
    var second = st.a && !st.b && st.room === id && k > st.a;
    if (second) {
      if (rangeFree(id, st.a, k) && nights(st.a, k) <= (CFG.maxNights || 30)) { st.b = k; hint.textContent = T.hintDone; }
      else { hint.textContent = T.hintBlocked; st.a = ""; st.b = ""; st.room = ""; }
    } else if (c.classList.contains("taken")) {
      return;   /* a booked night cannot be the arrival night */
    } else { st.room = id; st.a = k; st.b = ""; hint.textContent = T.hintOut; }
    renderBoard();
    var cell = board.querySelector('button.c[data-room="' + id + '"][data-date="' + k + '"]'); if (cell) cell.focus({ preventScroll: true });
  });

  function renderSummary() {
    var r = st.room ? roomById(st.room) : null;
    sumList.textContent = ""; sumTotal.textContent = "";
    function row(k, v) { sumList.appendChild(el("dt", "", k)); sumList.appendChild(el("dd", "", v)); }
    row(T.sumPlace, r ? r.name : T.pickRoom);
    if (st.a && st.b) row(T.sumDates, shortDay(st.a) + " → " + shortDay(st.b) + " (" + nightsText(nights(st.a, st.b)) + ")");
    row(T.sumGuests, guestsText(+guestsEl.value));
    if (r && st.a && st.b) { var n = nights(st.a, st.b); row(T.sumPrice, T.pn.replace("{p}", r.price).replace("{n}", n)); sumTotal.textContent = T.total.replace("{t}", r.price * n); }
  }
  guestsEl.addEventListener("change", function () {
    var r = st.room ? roomById(st.room) : null;
    if (r && tooSmall(r)) { st.a = ""; st.b = ""; st.room = ""; }
    hint.textContent = T.hintPick; formError.hidden = true; renderBoard();
  });

  /* "Book this room" on a card: pick the next Friday for two nights, or the nearest free ones, and go to the timeline */
  document.querySelectorAll("button[data-unit]").forEach(function (btn) {
    btn.addEventListener("click", function () {
      var r = roomById(btn.dataset.unit);
      if (r && tooSmall(r)) guestsEl.value = String(Math.min(r.guests, +guestsEl.options[guestsEl.options.length - 1].value));
      var d = addDays(today, (5 - today.getDay() + 7) % 7 || 7);
      for (var tries = 0; tries < 20; tries++) {   /* skip weekends that are already taken */
        if (rangeFree(r.id, ymd(d), ymd(addDays(d, 2)))) break;
        d = addDays(d, 7);
      }
      st.start = today; st.room = r.id; st.a = ymd(d); st.b = ymd(addDays(d, 2));
      if (nights(ymd(today), st.b) > DAYS - 1) st.start = addDays(d, -3);
      hint.textContent = T.hintDone;
      renderBoard(); scrollToEl($("book"));
      loadBoard();
    });
  });

  function setBusy(on) {
    busy = on; submitBtn.disabled = on; submitBtn.classList.toggle("is-busy", on);
    form.setAttribute("aria-busy", on ? "true" : "false");
    submitBtn.querySelector(".btn-label").textContent = on ? T.sending : sendLabel;
  }
  function showError(msg, focusEl) { formError.textContent = msg; formError.hidden = false; if (focusEl) focusEl.focus(); }
  function showDone(rec, p, r) {
    var L = T.lines;
    done.textContent = "";
    done.appendChild(el("h3", "", T.doneH));
    var ref = el("p", "done-ref"); ref.appendChild(el("span", "", T.doneRef)); ref.appendChild(el("strong", "", rec.id)); done.appendChild(ref);
    var s = el("p"); s.appendChild(el("span", "pill", T.statusPending)); done.appendChild(s);
    var dl = el("dl", "done-list");
    function row(k, v) { if (!v) return; dl.appendChild(el("dt", "", k)); dl.appendChild(el("dd", "", v)); }
    row(L.name, p.name); row(L.phone, p.phone); row(L.email, p.email); row(L.room, r.name);
    row(L.dates, longDate(p.checkin) + " → " + longDate(p.checkout) + " (" + nightsText(nights(p.checkin, p.checkout)) + ")");
    row(L.guests, guestsText(p.guests));
    row(L.total, T.total.replace("{t}", r.price * nights(p.checkin, p.checkout)));
    row(L.msg, p.message);
    done.appendChild(dl);
    done.appendChild(el("p", "", T.doneNext));
    var actions = el("div", "done-actions");
    if (API.mode === "demo") {
      done.appendChild(el("p", "demo-note", T.doneDemo));
      var link = el("a", "btn btn-coral btn-sm", T.adminLink);
      var adm = document.querySelector('.foot a[href*="admin"]'); link.href = adm ? adm.href : "admin.html";
      actions.appendChild(link);
    }
    var again = el("button", "btn btn-line btn-sm", T.again); again.type = "button";
    again.addEventListener("click", function () {
      form.reset(); st.a = ""; st.b = ""; st.room = ""; done.hidden = true; form.hidden = false;
      hint.textContent = T.hintPick; renderBoard(); loadBoard(); scrollToEl($("book"));
    });
    actions.appendChild(again); done.appendChild(actions);
    form.hidden = true; done.hidden = false;
    scrollToEl(done); done.focus({ preventScroll: true });
    loadBoard();   /* the timeline now shows the new stay */
  }

  form.addEventListener("submit", function (e) {
    e.preventDefault();
    if (busy) return;
    formError.hidden = true;
    var r = st.room ? roomById(st.room) : null;
    if (!r || !st.a || !st.b) { showError(T.errPick); return; }
    var nm = $("b-name"), ph = $("b-phone");
    if (!nm.value.trim()) { showError(T.errName, nm); return; }
    if (!ph.value.trim()) { showError(T.errName, ph); return; }
    var payload = { name: nm.value.trim(), phone: ph.value.trim(), email: $("b-email").value.trim(), room: r.id, checkin: st.a, checkout: st.b, guests: +guestsEl.value, message: $("b-msg").value.trim(), lang: lang };
    setBusy(true);
    API.createEnquiry(payload).then(function (rec) {
      setBusy(false); showDone(rec, payload, r);
    }, function (er) {
      setBusy(false);
      if (er && er.code === "room_taken") { showError(T.errTaken); st.a = ""; st.b = ""; st.room = ""; loadBoard(); }
      else showError(er && er.code === "invalid" ? T.errInvalid : T.errGeneric);
    });
  });

  hint.textContent = T.hintPick;
  renderBoard(); loadBoard();
})();
