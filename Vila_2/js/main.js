/* Linden House (design 2): page behaviour.
   Side menu, seasons, distance filter, photo viewer, review slider, and the stay enquiry (dates -> free rooms -> price -> send).
   The enquiry talks to LindenAPI (js/api.js): a mock server now, a real backend later (docs/API.md). */
(function () {
  "use strict";

  var CFG = window.LINDEN_CONFIG || {};
  var API = window.LindenAPI;
  var html = document.documentElement;
  var lang = html.lang === "bg" ? "bg" : "en";
  var reduceMotion = window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches;
  function $(id) { return document.getElementById(id); }

  var T = {
    bg: {
      locale: "bg-BG", mapTitle: "Карта на къщата",
      night1: "{n} нощ", nightN: "{n} нощувки", free: "Свободна", taken: "Заета", small: "Твърде малка",
      found: "{nights} · свободни стаи: {r} от {t}", none: "Няма свободна стая за тези дати. Опитайте други дати.",
      pickDates: "Изберете дати на пристигане и заминаване, за да видите кои стаи са свободни.", checking: "Проверяваме свободните стаи…",
      availError: "Не успяхме да проверим стаите. Опитайте пак.", badDates: "Заминаването трябва да е след пристигането.",
      sumDates: "Дати", sumGuests: "Гости", sumRoom: "Стая", sumPrice: "Цена", guestsN1: "1 гост", guestsN: "{n} гости", pickRoom: "Изберете стая",
      total: "Общо около {t} €", perNight: "{p} € × {n}",
      errRoom: "Изберете свободна стая.", errDates: "Изберете валидни дати.", errName: "Въведете име и телефон.",
      errTaken: "Съжаляваме, стаята току-що беше заета за тези дати. Изберете друга.", errInvalid: "Проверете данните и опитайте пак.", errGeneric: "Нещо се обърка. Опитайте пак или ни се обадете.",
      sending: "Изпращане…", demoLine: "Демо режим: запитванията се пазят само в този браузър и нищо не се изпраща.",
      doneH: "Запитването е получено", doneRef: "Номер на запитването", statusPending: "Чака потвърждение",
      doneNext: "Ще се свържем с вас по телефона или имейла, за да потвърдим. Запазете номера. Нищо не е платено онлайн.",
      doneDemo: "Демо режим: нищо не беше изпратено. Запитването е записано само в този браузър.",
      adminLink: "Вижте го в демо админ панела", again: "Ново запитване",
      lines: { name: "Име", phone: "Телефон", email: "Имейл", room: "Стая", dates: "Дати", guests: "Гости", total: "Общо", msg: "Съобщение" },
      minFoot: "{m} мин пеша", minCar: "{m} мин с кола"
    },
    en: {
      locale: "en-GB", mapTitle: "Map of the house",
      night1: "{n} night", nightN: "{n} nights", free: "Free", taken: "Taken", small: "Too small",
      found: "{nights} · free rooms: {r} of {t}", none: "No room is free for these dates. Please try other dates.",
      pickDates: "Pick your arrival and departure dates to see which rooms are free.", checking: "Checking free rooms…",
      availError: "We could not check the rooms. Please try again.", badDates: "Departure must be after arrival.",
      sumDates: "Dates", sumGuests: "Guests", sumRoom: "Room", sumPrice: "Price", guestsN1: "1 guest", guestsN: "{n} guests", pickRoom: "Choose a room",
      total: "About {t} € in total", perNight: "{p} € × {n}",
      errRoom: "Please choose a free room.", errDates: "Please choose valid dates.", errName: "Please enter your name and phone.",
      errTaken: "Sorry, the room was just taken for these dates. Please choose another.", errInvalid: "Please check your details and try again.", errGeneric: "Something went wrong. Please try again or call us.",
      sending: "Sending…", demoLine: "Demo mode: enquiries are kept in this browser only and nothing is sent.",
      doneH: "Enquiry received", doneRef: "Reference", statusPending: "Waiting for confirmation",
      doneNext: "We will contact you by phone or email to confirm. Keep your reference handy. Nothing was paid online.",
      doneDemo: "Demo mode: nothing was sent. The enquiry is saved only in this browser.",
      adminLink: "See it in the demo back office", again: "Make another enquiry",
      lines: { name: "Name", phone: "Phone", email: "Email", room: "Room", dates: "Dates", guests: "Guests", total: "Total", msg: "Message" },
      minFoot: "{m} min on foot", minCar: "{m} min by car"
    }
  }[lang];

  /* ---------- Small helpers ---------- */
  function pad(n) { return (n < 10 ? "0" : "") + n; }
  function ymd(d) { return d.getFullYear() + "-" + pad(d.getMonth() + 1) + "-" + pad(d.getDate()); }
  function toDate(v) { var p = v.split("-"); return new Date(+p[0], +p[1] - 1, +p[2]); }
  function nights(a, b) { return Math.round((toDate(b) - toDate(a)) / 864e5); }
  function dayText(v) { return toDate(v).toLocaleDateString(T.locale, { weekday: "short", day: "numeric", month: "short" }); }
  function longDate(v) { return toDate(v).toLocaleDateString(T.locale, { weekday: "long", day: "numeric", month: "long", year: "numeric" }); }
  function nightsText(n) { return (n === 1 ? T.night1 : T.nightN).replace("{n}", n); }
  function guestsText(n) { return n === 1 ? T.guestsN1 : T.guestsN.replace("{n}", n); }
  function el(tag, cls, text) { var n = document.createElement(tag); if (cls) n.className = cls; if (text !== undefined) n.textContent = text; return n; }
  function scrollToEl(n) { n.scrollIntoView({ behavior: reduceMotion ? "auto" : "smooth", block: "start" }); }
  var yEl = $("year"); if (yEl) yEl.textContent = new Date().getFullYear();

  /* ---------- Side menu (small screens) and the current section ---------- */
  var side = $("side"), burger = $("burger");
  function setMenu(open) {
    side.classList.toggle("open", open);
    burger.setAttribute("aria-expanded", open ? "true" : "false");
  }
  burger.addEventListener("click", function () { setMenu(!side.classList.contains("open")); });
  side.addEventListener("click", function (e) { if (e.target.closest("a") && side.classList.contains("open")) setMenu(false); });
  document.addEventListener("keydown", function (e) { if (e.key === "Escape" && side.classList.contains("open")) { setMenu(false); burger.focus(); } });
  document.querySelectorAll("[data-goto]").forEach(function (b) {
    b.addEventListener("click", function () { var t = $(b.dataset.goto); if (t) scrollToEl(t); });
  });
  var links = Array.prototype.slice.call(document.querySelectorAll(".side-nav a"));
  var secs = links.map(function (a) { return $(a.getAttribute("href").slice(1)); });
  if ("IntersectionObserver" in window) {
    var seen = {};
    var spy = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) { seen[en.target.id] = en.isIntersecting ? en.intersectionRatio : 0; });
      var best = null, bestV = 0;
      secs.forEach(function (s) { if ((seen[s.id] || 0) > bestV) { best = s.id; bestV = seen[s.id]; } });
      links.forEach(function (a) { if (a.getAttribute("href") === "#" + best) a.setAttribute("aria-current", "true"); else a.removeAttribute("aria-current"); });
    }, { rootMargin: "-20% 0px -45% 0px", threshold: [0, .1, .3, .6, 1] });
    secs.forEach(function (s) { spy.observe(s); });
  }

  /* ---------- Scroll reveal ---------- */
  if (html.classList.contains("js-reveal")) {
    var groups = [[".sec-head", 0], [".room", 0], [".day-grid li", 0.1], [".seasons", 0], [".ladder li", 0.05], [".g", 0.05], [".rev-box", 0], [".stay-left", 0], [".stay-right", 0.1], [".visit > div", 0.1]];
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (!en.isIntersecting) return;
        io.unobserve(en.target);
        en.target.classList.add("in");
        setTimeout(function () { en.target.classList.remove("rv", "in"); en.target.style.removeProperty("--d"); }, 1300);
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

  /* ---------- Seasons ---------- */
  var stabs = Array.prototype.slice.call(document.querySelectorAll(".stab"));
  function pickSeason(tab, focus) {
    stabs.forEach(function (t) {
      var on = t === tab;
      t.setAttribute("aria-selected", on ? "true" : "false"); t.tabIndex = on ? 0 : -1;
      $(t.getAttribute("aria-controls")).hidden = !on;
    });
    if (focus) tab.focus();
  }
  stabs.forEach(function (t, i) {
    t.addEventListener("click", function () { pickSeason(t, false); });
    t.addEventListener("keydown", function (e) {
      if (e.key === "ArrowRight" || e.key === "ArrowLeft") { e.preventDefault(); pickSeason(stabs[(i + 1) % stabs.length], true); }
    });
  });

  /* ---------- Around: filter the distance ladder ---------- */
  var modeChips = document.querySelectorAll(".chip[data-mode]");
  modeChips.forEach(function (chip) {
    chip.addEventListener("click", function () {
      var m = chip.dataset.mode;
      modeChips.forEach(function (c) { c.setAttribute("aria-pressed", c === chip ? "true" : "false"); });
      document.querySelectorAll("#ladder li").forEach(function (li) { li.hidden = !(m === "all" || li.dataset.mode === m); });
    });
  });

  /* ---------- Gallery viewer ---------- */
  var tiles = Array.prototype.slice.call(document.querySelectorAll(".g"));
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

  /* ---------- Reviews: one at a time ---------- */
  var slides = Array.prototype.slice.call(document.querySelectorAll(".slide")), dotsEl = $("revDots"), si = 0;
  slides.forEach(function () { dotsEl.appendChild(el("i")); });
  function showSlide(i) {
    si = (i + slides.length) % slides.length;
    slides.forEach(function (s, k) { s.hidden = k !== si; });
    Array.prototype.forEach.call(dotsEl.children, function (d, k) { d.classList.toggle("on", k === si); });
  }
  $("revPrev").addEventListener("click", function () { showSlide(si - 1); });
  $("revNext").addEventListener("click", function () { showSlide(si + 1); });
  showSlide(0);

  /* ---------- Map: loads only when the visitor asks ---------- */
  var mapBox = $("mapBox");
  $("mapLoad").addEventListener("click", function () {
    var f = document.createElement("iframe");
    f.src = mapBox.dataset.src; f.title = T.mapTitle; f.loading = "lazy"; f.referrerPolicy = "no-referrer";
    mapBox.textContent = ""; mapBox.appendChild(f);
  });

  /* ================= Stay enquiry ================= */
  var form = $("stayForm"), inEl = $("b-in"), outEl = $("b-out"), guestsEl = $("b-guests");
  var hint = $("nightsHint"), rcs = Array.prototype.slice.call(document.querySelectorAll(".rc"));
  var sumList = $("sumList"), sumTotal = $("sumTotal");
  var formError = $("formError"), done = $("stayDone"), demoNote = $("demoNote"), submitBtn = $("submitBtn");
  var sendLabel = submitBtn.querySelector(".btn-label").textContent;
  var tick = 0, busy = false, last = null;   /* last = the latest availability answer */
  var todayStr = ymd(new Date());
  [inEl, outEl, $("q-in"), $("q-out")].forEach(function (n) { n.min = todayStr; });
  if (API.mode === "demo") { demoNote.hidden = false; demoNote.textContent = T.demoLine; }

  function chosenRoom() { return form.querySelector('input[name="room"]:checked'); }
  function setTag(rc, text) { rc.querySelector("[data-tag]").textContent = text; }

  /* free rooms for the dates, asked from the (mock) server */
  function search() {
    var a = inEl.value, b = outEl.value, token = ++tick;
    last = null;
    if (!a || !b) { hint.textContent = T.pickDates; rcs.forEach(function (rc) { rc.classList.remove("off"); rc.querySelector("input").disabled = false; setTag(rc, ""); }); renderSummary(); return Promise.resolve(); }
    if (nights(a, b) < 1) { hint.textContent = T.badDates; renderSummary(); return Promise.resolve(); }
    hint.textContent = T.checking;
    return API.availability(a, b, +guestsEl.value).then(function (res) {
      if (token !== tick) return;
      last = res;
      var freeCount = 0;
      res.rooms.forEach(function (r) {
        var rc = form.querySelector('.rc[data-room="' + r.id + '"]'), inp = rc.querySelector("input");
        rc.classList.toggle("off", !r.free);
        inp.disabled = !r.free;
        if (!r.free && inp.checked) inp.checked = false;
        setTag(rc, r.free ? T.free : r.reason === "size" ? T.small : T.taken);
        if (r.free) freeCount++;
      });
      hint.textContent = freeCount ? T.found.replace("{nights}", nightsText(res.nights)).replace("{r}", freeCount).replace("{t}", res.rooms.length) : T.none;
      renderSummary();
    }, function () { if (token === tick) hint.textContent = T.availError; });
  }

  function renderSummary() {
    var room = chosenRoom(), a = inEl.value, b = outEl.value;
    sumList.textContent = ""; sumTotal.textContent = "";
    function row(k, v) { sumList.appendChild(el("dt", "", k)); sumList.appendChild(el("dd", "", v)); }
    if (a && b && nights(a, b) > 0) row(T.sumDates, dayText(a) + " → " + dayText(b) + " (" + nightsText(nights(a, b)) + ")");
    row(T.sumGuests, guestsText(+guestsEl.value));
    row(T.sumRoom, room ? room.dataset.name : T.pickRoom);
    if (room && a && b && nights(a, b) > 0) {
      var n = nights(a, b), p = +room.dataset.price;
      row(T.sumPrice, T.perNight.replace("{p}", p).replace("{n}", n));
      sumTotal.textContent = T.total.replace("{t}", p * n);
    }
  }
  form.addEventListener("change", function (e) {
    if (e.target === inEl) { outEl.min = inEl.value || todayStr; if (outEl.value && outEl.value <= inEl.value) outEl.value = ""; }
    if (e.target === inEl || e.target === outEl || e.target === guestsEl) search(); else renderSummary();
    formError.hidden = true;
  });

  /* quick form in the hero: copy the dates down, search and scroll to the rooms */
  $("quickForm").addEventListener("submit", function (e) {
    e.preventDefault();
    inEl.value = $("q-in").value; outEl.value = $("q-out").value; guestsEl.value = $("q-guests").value;
    outEl.min = inEl.value || todayStr;
    search();
    scrollToEl($("book"));
  });
  $("q-in").addEventListener("change", function () { $("q-out").min = this.value || todayStr; if ($("q-out").value <= this.value) $("q-out").value = ""; });

  /* "Book this room" on a room card: choose it, fill sensible dates if there are none, and go to the form */
  document.querySelectorAll("button[data-room]").forEach(function (btn) {
    btn.addEventListener("click", function () {
      if (!inEl.value || !outEl.value) {
        var d = new Date(); d.setDate(d.getDate() + ((5 - d.getDay() + 7) % 7 || 7));   /* the next Friday */
        var e = new Date(d.getTime() + 2 * 864e5);
        inEl.value = ymd(d); outEl.value = ymd(e); outEl.min = inEl.value;
      }
      var id = btn.dataset.room;
      scrollToEl($("book"));
      search().then(function () {   /* after the server answered, choose the room if it is free */
        var inp = form.querySelector('.rc[data-room="' + id + '"] input');
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
    var ref = el("p", "done-ref"); ref.appendChild(el("span", "", T.doneRef)); ref.appendChild(el("strong", "", rec.id));
    done.appendChild(ref);
    var st = el("p"); st.appendChild(el("span", "pill", T.statusPending)); done.appendChild(st);
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
      var link = el("a", "btn btn-main btn-sm", T.adminLink);
      var adm = document.querySelector('.foot a[href*="admin"]'); link.href = adm ? adm.href : "admin.html";
      actions.appendChild(link);
    }
    var again = el("button", "btn btn-line btn-sm", T.again); again.type = "button";
    again.addEventListener("click", function () { form.reset(); outEl.min = todayStr; done.hidden = true; form.hidden = false; search(); scrollToEl($("book")); });
    actions.appendChild(again); done.appendChild(actions);
    form.hidden = true; done.hidden = false;
    scrollToEl(done); done.focus({ preventScroll: true });
  }

  form.addEventListener("submit", function (e) {
    e.preventDefault();
    if (busy) return;
    formError.hidden = true;
    var a = inEl.value, b = outEl.value, room = chosenRoom();
    if (!a || !b || nights(a, b) < 1) { showError(T.errDates, inEl.value ? outEl : inEl); return; }
    if (!room) { showError(T.errRoom); return; }
    var nm = $("b-name"), ph = $("b-phone");
    if (!nm.value.trim()) { showError(T.errName, nm); return; }
    if (!ph.value.trim()) { showError(T.errName, ph); return; }
    var payload = { name: nm.value.trim(), phone: ph.value.trim(), email: $("b-email").value.trim(), room: room.value, checkin: a, checkout: b, guests: +guestsEl.value, message: $("b-msg").value.trim(), lang: lang };
    setBusy(true);
    API.createEnquiry(payload).then(function (rec) {
      setBusy(false); showDone(rec, payload, room);
    }, function (er) {
      setBusy(false);
      if (er && er.code === "room_taken") { showError(T.errTaken); search(); }
      else showError(er && er.code === "invalid" ? T.errInvalid : T.errGeneric);
    });
  });
  renderSummary();
})();
