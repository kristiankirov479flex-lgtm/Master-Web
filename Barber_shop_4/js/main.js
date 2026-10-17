/* Bolt Barbers (design 4): page behaviour.
   Colour schemes, rail menu with section highlight, work wall viewer, live "open now" and "next free chair", and the ticket builder
   (tap services, pick a barber, a day and a time; the ticket adds it up).
   The builder talks to BoltAPI (js/api.js): a mock server now, a real backend later (docs/API.md). */
(function () {
  "use strict";

  var CFG = window.BOLT_CONFIG || {};
  var API = window.BoltAPI;
  var html = document.documentElement;
  var lang = html.lang === "bg" ? "bg" : "en";
  var reduceMotion = window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches;
  function $(id) { return document.getElementById(id); }

  var T = {
    bg: {
      mapTitle: "Карта на бръснарницата", locale: "bg-BG", hUnit: "ч", mUnit: "мин",
      opensNow: "Отворено · до {t}", openLater: "Затворено · отваря днес в {t}", openTomorrow: "Затворено · отваря утре в {t}",
      nextFree: "Първи свободен стол:", todayAt: "днес в {t}", tomorrowAt: "утре в {t}", dayAt: "{d} в {t}",
      pickSvc: "Избери услуги, за да видиш свободните часове.", checking: "Проверяваме свободните часове…", noSlots: "Няма свободни часове този ден. Избери друг ден.",
      slotsHint: "Свободни часове: {n}. Работим до {c}.", availError: "Не успяхме да проверим часовете. Опитай пак.",
      emptyTk: "Още нищо. Натисни услуга, за да я добавиш.", today: "днес",
      errSvc: "Избери поне една услуга.", errTime: "Избери ден и час.", errName: "Въведи име и телефон.",
      errTaken: "Съжаляваме, този час току-що беше зает. Избери друг.", errInvalid: "Провери данните и опитай пак.", errGeneric: "Нещо се обърка. Опитай пак или ни се обади.",
      sending: "Изпращане…", demoLine: "Демо режим: заявките се пазят само в този браузър и нищо не се изпраща.",
      doneH: "Билетът е готов", doneRef: "Номер", statusPending: "Чака потвърждение",
      doneNext: "Ще се свържем с теб по телефона, за да потвърдим часа. Запази номера.",
      doneDemo: "Демо режим: нищо не беше изпратено. Заявката е записана само в този браузър.",
      adminLink: "Виж я в демо админ панела", again: "Нов билет", send: "Отпечатай билета", draft: "Чернова",
      lines: { service: "Услуги", barber: "Бръснар", date: "Ден", time: "Час", name: "Име", phone: "Телефон", msg: "Съобщение", look: "Прическа" },
      about: "Около"
    },
    en: {
      mapTitle: "Map of the barbershop", locale: "en-GB", hUnit: "h", mUnit: "min",
      opensNow: "Open now · until {t}", openLater: "Closed · opens today at {t}", openTomorrow: "Closed · opens tomorrow at {t}",
      nextFree: "Next free chair:", todayAt: "today at {t}", tomorrowAt: "tomorrow at {t}", dayAt: "{d} at {t}",
      pickSvc: "Pick services to see free times.", checking: "Checking free times…", noSlots: "No free times on this day. Please pick another day.",
      slotsHint: "{n} free times. We close at {c}.", availError: "We could not check the free times. Please try again.",
      emptyTk: "Nothing yet. Tap a service to add it.", today: "today",
      errSvc: "Please choose at least one service.", errTime: "Please pick a day and a time.", errName: "Please enter your name and phone.",
      errTaken: "Sorry, that time was just taken. Please choose another.", errInvalid: "Please check your details and try again.", errGeneric: "Something went wrong. Please try again or call us.",
      sending: "Sending…", demoLine: "Demo mode: bookings are kept in this browser only and nothing is sent.",
      doneH: "Your ticket is ready", doneRef: "Reference", statusPending: "Waiting for confirmation",
      doneNext: "We will contact you by phone to confirm your time. Keep your reference handy.",
      doneDemo: "Demo mode: nothing was sent. The booking is saved only in this browser.",
      adminLink: "See it in the demo back office", again: "New ticket", send: "Print my ticket", draft: "Draft",
      lines: { service: "Services", barber: "Barber", date: "Day", time: "Time", name: "Name", phone: "Phone", msg: "Message", look: "Cut" },
      about: "About"
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
  var SKINS = ["volt", "ultra", "sun", "ice", "mono"];
  var skinBtns = document.querySelectorAll(".sw[data-skin]");
  var skinName = $("skinName");
  var animTimer;
  function setSkin(skin, save) {
    if (SKINS.indexOf(skin) === -1) skin = "volt";
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
    if (save) { try { localStorage.setItem("boltSkin", skin); } catch (e) {} }
  }
  skinBtns.forEach(function (b) { b.addEventListener("click", function () { setSkin(b.dataset.skin, true); }); });
  var startSkin = null;
  try { startSkin = new URLSearchParams(location.search).get("skin") || localStorage.getItem("boltSkin"); } catch (e) {}
  setSkin(startSkin || "volt", false);
  var yEl = $("year"); if (yEl) yEl.textContent = new Date().getFullYear();

  /* ---------- Menu (phones) and the highlighted section (wide screens) ---------- */
  var rail = $("top"), burger = $("burger"), navLinks = Array.prototype.slice.call(document.querySelectorAll(".side-nav a"));
  burger.addEventListener("click", function () {
    var open = rail.classList.toggle("open");
    burger.setAttribute("aria-expanded", open ? "true" : "false");
  });
  rail.addEventListener("click", function (e) {
    if (e.target.closest(".side-nav a") && rail.classList.contains("open")) {
      rail.classList.remove("open");
      burger.setAttribute("aria-expanded", "false");
    }
  });
  if ("IntersectionObserver" in window) {
    var spy = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (!en.isIntersecting) return;
        navLinks.forEach(function (a) { a.setAttribute("aria-current", a.getAttribute("href") === "#" + en.target.id ? "true" : "false"); });
      });
    }, { rootMargin: "-35% 0px -55% 0px" });
    navLinks.forEach(function (a) { var s = document.querySelector(a.getAttribute("href")); if (s) spy.observe(s); });
  }

  /* ---------- Scroll reveal ---------- */
  if (html.classList.contains("js-reveal")) {
    var groups = [[".sec-head", 0], [".crew-card", 0.1], [".note", 0.1], [".w-item", 0.05], [".visit-grid > div", 0.1]];
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
  var items = Array.prototype.slice.call(document.querySelectorAll(".w-item"));
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
    openBuild({ look: { alt: img.alt, url: new URL(it.dataset.full, location.href).href, thumb: img.currentSrc || img.src } });
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
        nextBox.textContent = "";
        nextBox.appendChild(document.createTextNode(T.nextFree + " "));
        var b = el("button", "", when.replace("{t}", res.slots[0]).replace("{d}", shortDate(d)));
        b.type = "button";
        b.addEventListener("click", function () { openBuild({ date: ymd(d) }); });
        nextBox.appendChild(b);
        nextBox.hidden = false;
      }, function () {});
    }
    tryDay(0);
  }
  findNext();

  /* ================= Ticket builder ================= */
  var form = $("bookForm"), dchips = $("dchips"), tchips = $("tchips"), slotHint = $("slotHint");
  var errEl = $("bkError"), sendBtn = $("bkSend"), done = $("bkDone"), ticket = $("ticket");
  var today = new Date(); today = new Date(today.getFullYear(), today.getMonth(), today.getDate());
  var date = "", look = null, tick = 0, busy = false, finished = false, pendingTime = "";

  function svcs() { return Array.prototype.slice.call(form.querySelectorAll('input[name="svc"]:checked')); }
  function barber() { return form.querySelector('input[name="barber"]:checked'); }
  function totals() {
    var price = 0, min = 0;
    svcs().forEach(function (x) { price += +x.dataset.price; min += +x.dataset.min; });
    return { price: price, min: min };
  }

  /* the ticket on the right */
  function renderTicket() {
    var t = totals(), list = $("tkLines"), meta = $("tkMeta"), b = barber(), slot = form.querySelector('input[name="slot"]:checked');
    list.textContent = "";
    var sv = svcs();
    if (!sv.length) list.appendChild(el("li", "tk-empty", T.emptyTk));
    sv.forEach(function (x) {
      var li = el("li");
      li.appendChild(el("span", "", x.dataset.name));
      li.appendChild(el("span", "", (x.dataset.extra ? "+ " : "") + x.dataset.price + " €"));
      list.appendChild(li);
    });
    meta.textContent = "";
    function row(k, v) { if (!v) return; meta.appendChild(el("dt", "", k)); meta.appendChild(el("dd", "", v)); }
    row(T.lines.barber, b ? b.dataset.name : "");
    row(T.lines.date, date ? shortDate(toDate(date)) : "");
    row(T.lines.time, slot ? slot.value : "");
    $("tkTotal").textContent = t.price + " €";
    $("tkTime").textContent = t.min ? T.about + " " + fmtMin(t.min) : "";
    $("qTotal").textContent = t.price + " €";
    if (!reduceMotion) { ticket.classList.remove("bump"); void ticket.offsetWidth; ticket.classList.add("bump"); }
  }

  /* 14 day chips */
  function buildDays() {
    dchips.textContent = "";
    for (var i = 0; i < 14; i++) {
      var d = addDays(today, i), v = ymd(d);
      var lab = el("label", "dc"), inp = el("input");
      inp.type = "radio"; inp.name = "day"; inp.value = v; inp.checked = v === date;
      lab.appendChild(inp);
      lab.appendChild(el("small", "", d.toLocaleDateString(T.locale, { weekday: "short" })));
      lab.appendChild(el("b", "", String(d.getDate())));
      lab.title = longDate(v);
      dchips.appendChild(lab);
    }
  }
  function setDate(v) {
    date = v;
    var r = dchips.querySelector('input[value="' + v + '"]');
    if (r) { r.checked = true; r.parentNode.scrollIntoView({ block: "nearest", inline: "center", behavior: "auto" }); }
  }

  /* free times as chips, asked from the server for the chosen day, barber and total length */
  function loadSlots() {
    var token = ++tick, t = totals(), b = barber();
    var keep = (form.querySelector('input[name="slot"]:checked') || {}).value || pendingTime;
    if (!t.min) { tchips.textContent = ""; slotHint.textContent = T.pickSvc; renderTicket(); return; }
    slotHint.textContent = T.checking;
    API.availability(date, t.min, b ? b.value : "any").then(function (res) {
      if (token !== tick) return;
      tchips.textContent = "";
      res.slots.forEach(function (s) {
        var lab = el("label", "tc"), inp = el("input");
        inp.type = "radio"; inp.name = "slot"; inp.value = s;
        if (s === keep) inp.checked = true;
        lab.appendChild(inp); lab.appendChild(document.createTextNode(s));
        tchips.appendChild(lab);
      });
      pendingTime = "";
      slotHint.textContent = res.slots.length ? T.slotsHint.replace("{n}", res.slots.length).replace("{c}", res.close) : T.noSlots;
      renderTicket();
    }, function () { if (token === tick) slotHint.textContent = T.availError; });
  }
  form.addEventListener("change", function (e) {
    var n = e.target.name;
    if (n === "svc" || n === "barber") { renderTicket(); loadSlots(); }
    else if (n === "day") { date = e.target.value; loadSlots(); renderTicket(); }
    else if (n === "slot") { errEl.hidden = true; renderTicket(); }
  });

  $("lookRemove").addEventListener("click", function () { look = null; $("lookChip").hidden = true; });
  function showLook() {
    $("lookChip").hidden = !look;
    if (look) { $("lookImg").src = look.thumb || ""; $("lookText").textContent = look.alt; }
  }

  function fail(msg, focusEl) { errEl.textContent = msg; errEl.hidden = false; if (focusEl) focusEl.focus(); }
  function buildPayload() {
    var sv = svcs(), t = totals(), b = barber(), names = sv.map(function (x) { return x.dataset.name; });
    var main = sv.filter(function (x) { return !x.dataset.extra; });
    var primary = (main[0] || sv[0]).dataset.name;
    return {
      name: $("b-name").value.trim(), phone: $("b-phone").value.trim(), service: primary,
      plan: { summary: names.join(" + ") + ". " + T.about + " " + fmtMin(t.min) + ", " + t.price + " €",
              minPrice: t.price, maxPrice: t.price, minMinutes: t.min, maxMinutes: t.min, extras: names.slice(1), priceOnRequest: false },
      barber: b ? b.value : "any", barberName: b ? b.dataset.name : "",
      date: date, time: form.querySelector('input[name="slot"]:checked').value, durationMinutes: t.min,
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
    if (!svcs().length) { fail(T.errSvc); scrollToEl($("build")); return; }
    if (!form.querySelector('input[name="slot"]:checked')) { fail(T.errTime, tchips.querySelector("input") || dchips.querySelector("input")); return; }
    if (!$("b-name").value.trim()) { fail(T.errName, $("b-name")); return; }
    if (!$("b-phone").value.trim()) { fail(T.errName, $("b-phone")); return; }
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
    again.addEventListener("click", function () { resetBuild(); scrollToEl($("build")); });
    actions.appendChild(again);
    done.appendChild(actions);
    form.hidden = true; done.hidden = false;
    done.focus({ preventScroll: true });
    scrollToEl(done);
    findNext();
  }
  function resetBuild() {
    form.reset();
    look = null; finished = false; showLook();
    done.hidden = true; form.hidden = false; errEl.hidden = true;
    setDate(initialDate());
    renderTicket(); loadSlots();
  }
  function initialDate() {
    var now = new Date(), h = dayHours(now), late = now.getHours() * 60 + now.getMinutes() > toMinutes(h[1]) - 30;
    return ymd(late ? addDays(today, 1) : today);
  }

  /* opens the builder; opts may preselect a barber, a day or a photo */
  function openBuild(opts) {
    opts = opts || {};
    if (finished) resetBuild();
    if (opts.barber) { var r = form.querySelector('input[name="barber"][value="' + opts.barber + '"]'); if (r) r.checked = true; }
    if (opts.date) setDate(opts.date);
    if (opts.look) look = opts.look;
    showLook(); renderTicket(); loadSlots();
    scrollToEl($("build"));
  }
  document.addEventListener("click", function (e) {
    var b = e.target.closest("[data-book]");
    if (!b) return;
    e.preventDefault();
    openBuild({ barber: b.dataset.barber });
  });

  if (API.mode === "demo") { $("demoNote").hidden = false; $("demoNote").textContent = T.demoLine; }
  buildDays(); setDate(initialDate());
  renderTicket(); loadSlots();
})();
