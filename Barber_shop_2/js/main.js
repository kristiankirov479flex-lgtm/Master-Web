/* Foundry Barbers (design 2): page behaviour.
   Colour schemes, tabs, work rail, photo viewer, live "open now" and "next free chair", and the four-step booking drawer.
   The drawer talks to FoundryAPI (js/api.js): a mock server now, a real backend later (docs/API.md). */
(function () {
  "use strict";

  var CFG = window.FOUNDRY_CONFIG || {};
  var API = window.FoundryAPI;
  var html = document.documentElement;
  var lang = html.lang === "bg" ? "bg" : "en";
  var reduceMotion = window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches;
  function $(id) { return document.getElementById(id); }

  var T = {
    bg: {
      mapTitle: "Карта на бръснарницата", locale: "bg-BG", hUnit: "ч", mUnit: "мин",
      opensNow: "Отворено · до {t}", openLater: "Затворено · отваря днес в {t}", openTomorrow: "Затворено · отваря утре в {t}",
      nextFree: "Първи свободен стол:", todayAt: "днес в {t}", tomorrowAt: "утре в {t}", dayAt: "{d} в {t}",
      checking: "Проверяваме свободните часове…", noSlots: "Няма свободни часове този ден. Избери друга дата.",
      slotsHint: "Свободни часове: {n}. Работим до {c}.", availError: "Не успяхме да проверим часовете. Опитай пак.",
      errService: "Избери услуга, за да продължиш.", errTime: "Избери дата и час, за да продължиш.", errName: "Въведи име и телефон.",
      errTaken: "Съжаляваме, този час току-що беше зает. Избери друг час.", errInvalid: "Провери данните и опитай пак.", errGeneric: "Нещо се обърка. Опитай пак или ни се обади.",
      next: "Напред", confirm: "Потвърди", sending: "Изпращане…", step: "Стъпка {n} от 4: {name}",
      demoLine: "Демо режим: заявките се пазят само в този браузър и нищо не се изпраща.",
      doneH: "Заявката е получена", doneRef: "Номер", statusPending: "Чака потвърждение",
      doneNext: "Ще се свържем с теб по телефона, за да потвърдим часа. Запази номера.",
      doneDemo: "Демо режим: нищо не беше изпратено. Заявката е записана само в този браузър.",
      adminLink: "Виж я в демо админ панела", again: "Запази още един час", close: "Затвори",
      lines: { service: "Услуга", extras: "Допълнения", barber: "Бръснар", date: "Дата", time: "Час", total: "Общо", name: "Име", phone: "Телефон", msg: "Съобщение", look: "Прическа" },
      about: "Около"
    },
    en: {
      mapTitle: "Map of the barbershop", locale: "en-GB", hUnit: "h", mUnit: "min",
      opensNow: "Open now · until {t}", openLater: "Closed · opens today at {t}", openTomorrow: "Closed · opens tomorrow at {t}",
      nextFree: "Next free chair:", todayAt: "today at {t}", tomorrowAt: "tomorrow at {t}", dayAt: "{d} at {t}",
      checking: "Checking free times…", noSlots: "No free times on this day. Please pick another date.",
      slotsHint: "{n} free times. We close at {c}.", availError: "We could not check the free times. Please try again.",
      errService: "Choose a service to continue.", errTime: "Pick a date and a time to continue.", errName: "Please enter your name and phone.",
      errTaken: "Sorry, that time was just taken. Please choose another time.", errInvalid: "Please check your details and try again.", errGeneric: "Something went wrong. Please try again or call us.",
      next: "Next", confirm: "Confirm", sending: "Sending…", step: "Step {n} of 4: {name}",
      demoLine: "Demo mode: bookings are kept in this browser only and nothing is sent.",
      doneH: "Booking received", doneRef: "Reference", statusPending: "Waiting for confirmation",
      doneNext: "We will contact you by phone to confirm your time. Keep your reference handy.",
      doneDemo: "Demo mode: nothing was sent. The booking is saved only in this browser.",
      adminLink: "See it in the demo back office", again: "Book another time", close: "Close",
      lines: { service: "Service", extras: "Extras", barber: "Barber", date: "Date", time: "Time", total: "Total", name: "Name", phone: "Phone", msg: "Message", look: "Cut" },
      about: "About"
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
  function longDate(v) { return toDate(v).toLocaleDateString(T.locale, { weekday: "long", day: "numeric", month: "long", year: "numeric" }); }
  function shortDate(d) { return d.toLocaleDateString(T.locale, { weekday: "short", day: "numeric", month: "short" }); }
  function el(tag, cls, text) { var n = document.createElement(tag); if (cls) n.className = cls; if (text !== undefined) n.textContent = text; return n; }
  function scrollToEl(n) { n.scrollIntoView({ behavior: reduceMotion ? "auto" : "smooth", block: "start" }); }
  function dayHours(d) { var w = d.getDay(); return w === 0 || w === 6 ? CFG.hours.weekend : CFG.hours.weekday; }

  /* ---------- Colour scheme (skin) ---------- */
  var SKINS = ["brass", "navy", "forest", "heritage", "graphite"];
  var skinBtns = document.querySelectorAll(".sw[data-skin]");
  var skinName = $("skinName");
  var animTimer;
  function setSkin(skin, save) {
    if (SKINS.indexOf(skin) === -1) skin = "brass";
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
    if (save) { try { localStorage.setItem("foundrySkin", skin); } catch (e) {} }
  }
  skinBtns.forEach(function (b) { b.addEventListener("click", function () { setSkin(b.dataset.skin, true); }); });
  var startSkin = null;
  try { startSkin = new URLSearchParams(location.search).get("skin") || localStorage.getItem("foundrySkin"); } catch (e) {}
  setSkin(startSkin || "brass", false);

  /* ---------- Menu ---------- */
  var nav = $("nav"), burger = $("burger");
  burger.addEventListener("click", function () {
    var open = nav.classList.toggle("open");
    burger.setAttribute("aria-expanded", open ? "true" : "false");
  });
  nav.addEventListener("click", function (e) {
    if (e.target.closest("a, button") && nav.classList.contains("open")) {
      nav.classList.remove("open");
      burger.setAttribute("aria-expanded", "false");
    }
  });
  var yEl = $("year"); if (yEl) yEl.textContent = new Date().getFullYear();

  /* ---------- Scroll reveal ---------- */
  if (html.classList.contains("js-reveal")) {
    var groups = [[".sec-head > div", 0.08], [".bcard", 0.1], [".plan", 0.1], [".rev", 0.1], [".visit-grid > div", 0.1], [".rating", 0]];
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
        n.style.setProperty("--d", (i * g[1]).toFixed(2) + "s");
        io.observe(n);
      });
    });
  }

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
      var k = e.key, n = tabs.length;
      if (k === "ArrowRight") { e.preventDefault(); selectTab(tabs[(i + 1) % n], true); }
      else if (k === "ArrowLeft") { e.preventDefault(); selectTab(tabs[(i - 1 + n) % n], true); }
      else if (k === "Home") { e.preventDefault(); selectTab(tabs[0], true); }
      else if (k === "End") { e.preventDefault(); selectTab(tabs[n - 1], true); }
    });
  });

  /* ---------- Work rail ---------- */
  var rail = $("rail");
  function railBy(dir) { rail.scrollBy({ left: dir * Math.max(240, rail.clientWidth * 0.8), behavior: reduceMotion ? "auto" : "smooth" }); }
  $("railPrev").addEventListener("click", function () { railBy(-1); });
  $("railNext").addEventListener("click", function () { railBy(1); });

  /* ---------- Photo viewer for the work rail ---------- */
  var items = Array.prototype.slice.call(document.querySelectorAll(".rail-item"));
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
    openDrawer({ look: { alt: img.alt, url: new URL(it.dataset.full, location.href).href, thumb: img.currentSrc || img.src } });
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
  var nextBox = $("nextFree"), nextSlot = null;
  function findNext() {
    var start = new Date();
    function tryDay(i) {
      if (i > 6) return;
      var d = new Date(start.getFullYear(), start.getMonth(), start.getDate() + i);
      API.availability(ymd(d), 40, "any").then(function (res) {
        if (!res.slots.length) return tryDay(i + 1);
        var when = i === 0 ? T.todayAt : i === 1 ? T.tomorrowAt : T.dayAt;
        nextSlot = { date: ymd(d), time: res.slots[0] };
        nextBox.textContent = "";
        nextBox.appendChild(document.createTextNode(T.nextFree + " "));
        var b = el("button", "", when.replace("{t}", res.slots[0]).replace("{d}", shortDate(d)));
        b.type = "button";
        b.addEventListener("click", function () { openDrawer({ slot: nextSlot }); });
        nextBox.appendChild(b);
        nextBox.hidden = false;
      }, function () {});
    }
    tryDay(0);
  }
  findNext();

  /* ================= Booking drawer ================= */
  var drawer = $("drawer"), form = $("bookForm"), stepsEl = $("drSteps");
  var panels = Array.prototype.slice.call(form.querySelectorAll(".dr-panel"));
  var btnBack = $("drBack"), btnNext = $("drNext"), drError = $("drError"), drLive = $("drLive");
  var dateEl = $("b-date"), slotsEl = $("slots"), slotHint = $("slotHint");
  var stepNames = [T.lines.service, T.lines.barber, T.lines.time, T.lines.name];
  var stepNo = 1, look = null, pref = null, tick = 0, busy = false, finished = false;
  var nextLabel = btnNext.textContent;

  dateEl.min = ymd(new Date());

  function checkedSvc() { return form.querySelector('input[name="service"]:checked'); }
  function checkedExtras() { return Array.prototype.slice.call(form.querySelectorAll('input[name="extra"]:checked')); }
  function checkedBarber() { return form.querySelector('input[name="barber"]:checked'); }
  function totals() {
    var s = checkedSvc(), price = 0, min = 0;
    if (s) { price += +s.dataset.price; min += +s.dataset.min; }
    checkedExtras().forEach(function (x) { price += +x.dataset.price; min += +x.dataset.min; });
    return { price: price, min: min };
  }
  function renderTotals() {
    var t = totals();
    $("drTotal").textContent = t.price + " €";
    $("drTime").textContent = t.min ? T.about + " " + fmtMin(t.min) : "";
  }
  form.addEventListener("change", function (e) {
    if (e.target.name === "service" || e.target.name === "extra") { renderTotals(); if (stepNo === 3) loadSlots(); }
    if (e.target.name === "barber" && stepNo === 3) loadSlots();
    if (e.target.name === "slot") drError.hidden = true;
  });

  function showStep(n) {
    stepNo = n;
    panels.forEach(function (p) { p.hidden = +p.dataset.panel !== n; });
    Array.prototype.forEach.call(stepsEl.children, function (li, i) {
      li.classList.toggle("on", i + 1 === n);
      li.classList.toggle("done", i + 1 < n);
    });
    btnBack.hidden = n === 1;
    btnNext.textContent = n === 4 ? T.confirm : nextLabel;
    drError.hidden = true;
    $("drBody").scrollTop = 0;
    if (n === 3) {
      if (!dateEl.value) {
        var now = new Date(), h = dayHours(now), later = now.getHours() * 60 + now.getMinutes() < toMinutes(h[1]) - 30;
        dateEl.value = ymd(later ? now : new Date(now.getTime() + 864e5));
      }
      loadSlots();
    }
    if (n === 4) renderSummary();
    drLive.textContent = "";
    setTimeout(function () { drLive.textContent = T.step.replace("{n}", n).replace("{name}", stepNames[n - 1]); }, 30);
    var focusTarget = n === 4 ? $("b-name") : null;
    if (focusTarget) focusTarget.focus({ preventScroll: true });
  }

  /* free times as chips, asked from the server for the chosen date, barber and visit length */
  function loadSlots() {
    var token = ++tick, keep = (form.querySelector('input[name="slot"]:checked') || {}).value || (pref && pref.date === dateEl.value ? pref.time : "");
    var t = totals(), b = checkedBarber();
    if (!dateEl.value) { slotsEl.textContent = ""; slotHint.textContent = $("slotHint").dataset.default || slotHint.textContent; return; }
    slotHint.textContent = T.checking;
    API.availability(dateEl.value, t.min || 40, b ? b.value : "any").then(function (res) {
      if (token !== tick) return;
      slotsEl.textContent = "";
      res.slots.forEach(function (s) {
        var lab = el("label", "slot"), inp = el("input"), sp = el("span", "", s);
        inp.type = "radio"; inp.name = "slot"; inp.value = s;
        if (s === keep) inp.checked = true;
        lab.appendChild(inp); lab.appendChild(sp);
        slotsEl.appendChild(lab);
      });
      slotHint.textContent = res.slots.length ? T.slotsHint.replace("{n}", res.slots.length).replace("{c}", res.close) : T.noSlots;
    }, function () { if (token === tick) slotHint.textContent = T.availError; });
  }
  dateEl.addEventListener("input", loadSlots);
  dateEl.addEventListener("change", loadSlots);

  function renderSummary() {
    var s = checkedSvc(), t = totals(), b = checkedBarber(), slot = form.querySelector('input[name="slot"]:checked');
    var dl = $("sum"), L = T.lines;
    dl.textContent = "";
    function row(k, v) { if (!v) return; dl.appendChild(el("dt", "", k)); dl.appendChild(el("dd", "", v)); }
    row(L.service, s ? s.dataset.name : "");
    row(L.extras, checkedExtras().map(function (x) { return x.dataset.name; }).join(", "));
    row(L.barber, b ? b.dataset.name : "");
    row(L.date, dateEl.value ? longDate(dateEl.value) : "");
    row(L.time, slot ? slot.value : "");
    row(L.total, t.price + " € · " + T.about.toLowerCase() + " " + fmtMin(t.min));
    var chip = $("lookChip");
    chip.hidden = !look;
    if (look) { $("lookImg").src = look.thumb || ""; $("lookText").textContent = look.alt; }
  }
  $("lookRemove").addEventListener("click", function () { look = null; $("lookChip").hidden = true; });

  function fail(msg, focusEl) {
    drError.textContent = msg;
    drError.hidden = false;
    if (focusEl) focusEl.focus();
  }
  function validate(n) {
    if (n === 1 && !checkedSvc()) { fail(T.errService); return false; }
    if (n === 3 && !(dateEl.value && form.querySelector('input[name="slot"]:checked'))) { fail(T.errTime, dateEl); return false; }
    if (n === 4) {
      var nm = $("b-name"), ph = $("b-phone");
      if (!nm.value.trim()) { fail(T.errName, nm); return false; }
      if (!ph.value.trim()) { fail(T.errName, ph); return false; }
    }
    return true;
  }
  btnBack.addEventListener("click", function () { if (stepNo > 1) showStep(stepNo - 1); });
  btnNext.addEventListener("click", function () {
    if (busy || !validate(stepNo)) return;
    if (stepNo < 4) showStep(stepNo + 1); else submit();
  });
  form.addEventListener("submit", function (e) { e.preventDefault(); btnNext.click(); });

  function buildPayload() {
    var s = checkedSvc(), t = totals(), b = checkedBarber(), ex = checkedExtras().map(function (x) { return x.dataset.name; });
    return {
      name: $("b-name").value.trim(), phone: $("b-phone").value.trim(), service: s.dataset.name,
      plan: { summary: s.dataset.name + (ex.length ? " + " + ex.join(" + ") : "") + ". " + T.about + " " + fmtMin(t.min) + ", " + t.price + " €",
              minPrice: t.price, maxPrice: t.price, minMinutes: t.min, maxMinutes: t.min, extras: ex, priceOnRequest: false },
      barber: b ? b.value : "any", barberName: b ? b.dataset.name : "",
      date: dateEl.value, time: form.querySelector('input[name="slot"]:checked').value, durationMinutes: t.min,
      look: look ? { alt: look.alt, url: look.url } : null,
      message: $("b-msg").value.trim(), lang: lang
    };
  }
  function setBusy(on) {
    busy = on;
    btnNext.disabled = on;
    btnNext.classList.toggle("is-busy", on);
    btnNext.textContent = on ? T.sending : T.confirm;
    form.setAttribute("aria-busy", on ? "true" : "false");
  }
  function submit() {
    var payload = buildPayload();
    setBusy(true);
    API.createRequest(payload).then(function (rec) {
      setBusy(false);
      showDone(rec, payload);
    }, function (er) {
      setBusy(false);
      if (er && er.code === "slot_taken") { showStep(3); fail(T.errTaken); loadSlots(); }
      else fail(er && er.code === "invalid" ? T.errInvalid : T.errGeneric);
    });
  }

  function showDone(rec, p) {
    var L = T.lines, done = $("drDone");
    finished = true;
    done.textContent = "";
    done.appendChild(el("h3", "", T.doneH));
    var ref = el("p", "done-ref");
    ref.appendChild(el("span", "", T.doneRef));
    ref.appendChild(el("strong", "", rec.id));
    done.appendChild(ref);
    var st = el("p", "done-status");
    st.appendChild(el("span", "pill", T.statusPending));
    done.appendChild(st);
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
    again.addEventListener("click", function () { resetBooking(); showStep(1); });
    var close = el("button", "btn btn-line btn-sm", T.close); close.type = "button";
    close.addEventListener("click", function () { drawer.close(); });
    actions.appendChild(again); actions.appendChild(close);
    done.appendChild(actions);
    form.hidden = true; stepsEl.hidden = true;
    done.hidden = false;
    done.focus({ preventScroll: true });
    findNext();
  }

  function resetBooking() {
    form.reset();
    look = null; pref = null; finished = false; stepNo = 1;
    slotsEl.textContent = "";
    dateEl.value = "";
    drError.hidden = true;
    $("drDone").hidden = true; form.hidden = false; stepsEl.hidden = false;
    renderTotals();
  }

  /* opens the drawer; opts may preselect a service, a barber, a time slot or a photo */
  function openDrawer(opts) {
    opts = opts || {};
    if (finished) resetBooking();
    if (opts.service) { var r = form.querySelector('input[name="service"][value="' + opts.service + '"]'); if (r) r.checked = true; }
    if (opts.barber) { var b = form.querySelector('input[name="barber"][value="' + opts.barber + '"]'); if (b) b.checked = true; }
    if (opts.slot) { pref = opts.slot; dateEl.value = opts.slot.date; }
    if (opts.look) look = opts.look;
    renderTotals();
    if (API.mode === "demo") { $("demoNote").hidden = false; $("demoNote").textContent = T.demoLine; }
    if (!drawer.open) drawer.showModal();
    showStep(opts.service ? (opts.barber ? 3 : 2) : (opts.slot || opts.look || opts.barber ? 1 : stepNo));
  }
  document.addEventListener("click", function (e) {
    var b = e.target.closest("[data-book]");
    if (!b) return;
    e.preventDefault();
    openDrawer({ service: b.dataset.service, barber: b.dataset.barber });
  });
  $("drClose").addEventListener("click", function () { drawer.close(); });
  drawer.addEventListener("click", function (e) { if (e.target === drawer) drawer.close(); });
  renderTotals();
})();
