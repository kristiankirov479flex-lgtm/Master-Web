/* Atelier Nude (design 3): page behaviour.
   Colour schemes, menu, lookbook filter and photo viewer, "add to my visit" on the menu, live "open now" and "next free time",
   and the booking (your visit, a day, a free time, your details).
   The booking talks to AtelierAPI (js/api.js): a mock server now, a real backend later (docs/API.md). */
(function () {
  "use strict";

  var CFG = window.ATELIER_CONFIG || {};
  var API = window.AtelierAPI;
  var html = document.documentElement;
  var lang = html.lang === "bg" ? "bg" : "en";
  var reduceMotion = window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches;
  function $(id) { return document.getElementById(id); }

  var T = {
    bg: {
      mapTitle: "Карта на студиото", locale: "bg-BG", hUnit: "ч", mUnit: "мин",
      opensNow: "Отворено · до {t}", openLater: "Затворено · отваря днес в {t}", openTomorrow: "Затворено · отваря утре в {t}",
      nextFree: "Следващ свободен час:", todayAt: "днес в {t}", tomorrowAt: "утре в {t}", dayAt: "{d} в {t}",
      pickFirst: "Избери дизайн или услуга, за да видиш свободните часове.", checking: "Проверяваме свободните часове…", noSlots: "Няма свободни часове този ден. Избери друг ден.",
      slotsHint: "Свободни часове: {n}. Работим до {c}.", availError: "Не успяхме да проверим часовете. Опитай пак.",
      shown: "Показани дизайни: {n}", onRequest: "по запитване", from: "от", plusArt: "плюс нейл арт, цена по запитване", about: "Около", gift: "Подаръчна карта: запитване",
      errPick: "Избери дизайн или поне една услуга.", errTime: "Избери ден и час.", errName: "Въведи име и телефон.",
      errTaken: "Съжаляваме, този час току-що беше зает. Избери друг.", errInvalid: "Провери данните и опитай пак.", errGeneric: "Нещо се обърка. Опитай пак или ни се обади.",
      sending: "Изпращане…", demoLine: "Демо режим: заявките се пазят само в този браузър и нищо не се изпраща.",
      doneH: "Заявката е получена", doneRef: "Номер", statusPending: "Чака потвърждение",
      doneNext: "Ще се свържем с теб по телефона, за да потвърдим часа. Запази номера.",
      doneDemo: "Демо режим: нищо не беше изпратено. Заявката е записана само в този браузър.",
      adminLink: "Виж я в демо админ панела", again: "Нова заявка", send: "Изпрати заявката", remove: "Премахни",
      lines: { service: "Услуги", date: "Дата", time: "Час", total: "Общо", name: "Име", phone: "Телефон", msg: "Съобщение", look: "Дизайн" }
    },
    en: {
      mapTitle: "Map of the studio", locale: "en-GB", hUnit: "h", mUnit: "min",
      opensNow: "Open now · until {t}", openLater: "Closed · opens today at {t}", openTomorrow: "Closed · opens tomorrow at {t}",
      nextFree: "Next free time:", todayAt: "today at {t}", tomorrowAt: "tomorrow at {t}", dayAt: "{d} at {t}",
      pickFirst: "Pick a look or a service to see free times.", checking: "Checking free times…", noSlots: "No free times on this day. Please pick another day.",
      slotsHint: "{n} free times. We close at {c}.", availError: "We could not check the free times. Please try again.",
      shown: "Looks shown: {n}", onRequest: "on request", from: "from", plusArt: "plus nail art, price on request", about: "About", gift: "Gift card enquiry",
      errPick: "Please pick a look or at least one service.", errTime: "Please pick a day and a time.", errName: "Please enter your name and phone.",
      errTaken: "Sorry, that time was just taken. Please choose another.", errInvalid: "Please check your details and try again.", errGeneric: "Something went wrong. Please try again or call us.",
      sending: "Sending…", demoLine: "Demo mode: requests are kept in this browser only and nothing is sent.",
      doneH: "Request received", doneRef: "Reference", statusPending: "Waiting for confirmation",
      doneNext: "We will contact you by phone to confirm your time. Keep your reference handy.",
      doneDemo: "Demo mode: nothing was sent. The request is saved only in this browser.",
      adminLink: "See it in the demo back office", again: "New request", send: "Send the request", remove: "Remove",
      lines: { service: "Services", date: "Date", time: "Time", total: "Total", name: "Name", phone: "Phone", msg: "Message", look: "Look" }
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
  var SKINS = ["bone", "blush", "mocha", "noir", "mint"];
  var skinBtns = document.querySelectorAll(".sw[data-skin]");
  var skinName = $("skinName");
  var animTimer;
  function setSkin(skin, save) {
    if (SKINS.indexOf(skin) === -1) skin = "bone";
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
    if (save) { try { localStorage.setItem("atelierSkin", skin); } catch (e) {} }
  }
  skinBtns.forEach(function (b) { b.addEventListener("click", function () { setSkin(b.dataset.skin, true); }); });
  var startSkin = null;
  try { startSkin = new URLSearchParams(location.search).get("skin") || localStorage.getItem("atelierSkin"); } catch (e) {}
  setSkin(startSkin || "bone", false);
  var yEl = $("year"); if (yEl) yEl.textContent = new Date().getFullYear();

  /* ---------- Menu ---------- */
  var nav = $("nav"), burger = $("burger");
  burger.addEventListener("click", function () {
    var open = nav.classList.toggle("open");
    burger.setAttribute("aria-expanded", open ? "true" : "false");
  });
  nav.addEventListener("click", function (e) {
    if (e.target.closest("a") && nav.classList.contains("open")) { nav.classList.remove("open"); burger.setAttribute("aria-expanded", "false"); }
  });
  document.addEventListener("click", function (e) {
    var b = e.target.closest("[data-go]");
    if (b) { e.preventDefault(); scrollToEl($(b.dataset.go)); }
  });

  /* ---------- Scroll reveal ---------- */
  if (html.classList.contains("js-reveal")) {
    var groups = [[".sec-head", 0], [".look", 0.06], [".mn-col", 0.08], [".quote", 0.1], [".visit-grid > div", 0.1], [".gift", 0]];
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
        n.style.setProperty("--d", ((i % 4) * g[1]).toFixed(2) + "s");
        io.observe(n);
      });
    });
  }

  /* ---------- Lookbook: filter and photo viewer ---------- */
  var looks = Array.prototype.slice.call(document.querySelectorAll(".look"));
  var filterBtns = Array.prototype.slice.call(document.querySelectorAll("[data-filter]"));
  filterBtns.forEach(function (b) {
    b.addEventListener("click", function () {
      var f = b.dataset.filter, n = 0;
      filterBtns.forEach(function (x) { x.setAttribute("aria-pressed", x === b ? "true" : "false"); });
      looks.forEach(function (l) { var show = f === "all" || l.dataset.cat === f; l.hidden = !show; if (show) n++; });
      $("shown").textContent = T.shown.replace("{n}", n);
    });
  });
  var box = $("lightbox"), lbImg = $("lbImg"), current = 0;
  function visibleLooks() { return looks.filter(function (l) { return !l.hidden; }); }
  function showPhoto(i) {
    var list = visibleLooks();
    current = (i + list.length) % list.length;
    var l = list[current], img = l.querySelector("img");
    lbImg.src = l.querySelector("[data-full]").dataset.full;
    lbImg.alt = img.alt;
    lbImg.dataset.look = l.querySelector("[data-look]").dataset.look;
    lbImg.classList.remove("swap"); void lbImg.offsetWidth; lbImg.classList.add("swap");
  }
  looks.forEach(function (l) {
    l.querySelector("[data-full]").addEventListener("click", function () { var list = visibleLooks(); showPhoto(list.indexOf(l)); box.showModal(); });
  });
  $("lbClose").addEventListener("click", function () { box.close(); });
  $("lbPrev").addEventListener("click", function () { showPhoto(current - 1); });
  $("lbNext").addEventListener("click", function () { showPhoto(current + 1); });
  box.addEventListener("click", function (e) { if (e.target === box || e.target.className === "lb-inner") box.close(); });
  box.addEventListener("keydown", function (e) { if (e.key === "ArrowLeft") showPhoto(current - 1); if (e.key === "ArrowRight") showPhoto(current + 1); });
  $("lbRequest").addEventListener("click", function () {
    var btn = document.querySelector('[data-look="' + lbImg.dataset.look + '"]');
    box.close();
    if (btn) chooseLook(btn);
  });

  /* ---------- Map ---------- */
  var mapBox = $("mapBox");
  $("mapLoad").addEventListener("click", function () {
    var f = document.createElement("iframe");
    f.src = mapBox.dataset.src; f.title = T.mapTitle; f.loading = "lazy"; f.referrerPolicy = "no-referrer";
    mapBox.textContent = ""; mapBox.appendChild(f);
  });

  /* ---------- Open now ---------- */
  function updateOpen() {
    var now = new Date(), h = dayHours(now), m = now.getHours() * 60 + now.getMinutes(), text, open = false;
    if (m >= toMinutes(h[0]) && m < toMinutes(h[1])) { open = true; text = T.opensNow.replace("{t}", h[1]); }
    else if (m < toMinutes(h[0])) text = T.openLater.replace("{t}", h[0]);
    else text = T.openTomorrow.replace("{t}", dayHours(new Date(now.getTime() + 864e5))[0]);
    var n = $("openNow"); n.textContent = text; n.classList.toggle("off", !open);
  }
  updateOpen(); setInterval(updateOpen, 60000);

  /* ================= Booking ================= */
  var form = $("bookForm"), strip = $("dayStrip"), tchips = $("tchips"), slotHint = $("slotHint");
  var errEl = $("bkError"), sendBtn = $("bkSend"), done = $("bkDone");
  var today = new Date(); today = new Date(today.getFullYear(), today.getMonth(), today.getDate());
  var basket = [], look = null, giftMode = false, date = ymd(today), stripStart = today, tick = 0, busy = false, finished = false;
  var menuBtns = Array.prototype.slice.call(document.querySelectorAll(".mn-add"));
  function btnFor(id) { return document.querySelector('.mn-add[data-svc="' + id + '"]'); }

  function totals() {
    var t = { pmin: 0, pmax: 0, mmax: 0, from: false, request: false, names: [] };
    basket.forEach(function (id) {
      var d = btnFor(id).dataset;
      t.pmin += +d.p0; t.pmax += +d.p1; t.mmax += +d.min;
      if (d.kind === "from" || d.kind === "per") t.from = true;
      if (d.kind === "request") t.request = true;
      t.names.push(d.name);
    });
    return t;
  }
  function priceText(t) {
    if (t.request && t.pmax === 0) return T.onRequest;
    var txt = t.pmin === t.pmax ? t.pmin + " €" : t.pmin + " – " + t.pmax + " €";
    return (t.from || t.request) ? T.from + " " + txt : txt;
  }
  function minutes() { return basket.length ? totals().mmax : (giftMode ? 15 : 0); }

  function renderBasket() {
    var list = $("basket"), t = totals();
    list.textContent = "";
    basket.forEach(function (id) {
      var d = btnFor(id).dataset, li = el("li");
      li.appendChild(el("span", "", d.name));
      var x = el("button", "x", "×"); x.type = "button"; x.setAttribute("aria-label", T.remove + ": " + d.name); x.dataset.remove = id;
      li.appendChild(x); list.appendChild(li);
    });
    if (giftMode && !basket.length) {
      var gi = el("li"); gi.appendChild(el("span", "", T.gift));
      var gx = el("button", "x", "×"); gx.type = "button"; gx.setAttribute("aria-label", T.remove + ": " + T.gift); gx.dataset.remove = "gift";
      gi.appendChild(gx); list.appendChild(gi);
    }
    menuBtns.forEach(function (b) {
      var on = basket.indexOf(b.dataset.svc) !== -1;
      b.setAttribute("aria-pressed", on ? "true" : "false");
      b.firstChild.textContent = on ? "✓" : "+";
    });
    var has = basket.length > 0;
    $("empty").hidden = has || giftMode;
    $("totals").hidden = !has;
    if (has) {
      $("tPrice").textContent = priceText(t);
      if (t.request && t.pmax > 0) $("tPrice").appendChild(el("small", "", T.plusArt));
      $("tTime").textContent = T.about + " " + fmtMin(t.mmax);
    }
    $("lookBox").hidden = !look;
    if (look) { $("lookImg").src = look.thumb || ""; $("lookName").textContent = look.name; }
    loadSlots();
  }
  menuBtns.forEach(function (b) {
    b.addEventListener("click", function () {
      var id = b.dataset.svc, i = basket.indexOf(id);
      if (i === -1) basket.push(id); else basket.splice(i, 1);
      giftMode = false;
      renderBasket();
    });
  });
  $("basket").addEventListener("click", function (e) {
    var x = e.target.closest("[data-remove]");
    if (!x) return;
    if (x.dataset.remove === "gift") giftMode = false; else basket.splice(basket.indexOf(x.dataset.remove), 1);
    if (!basket.length) look = null;
    renderBasket();
  });

  function chooseLook(btn) {
    var card = btn.closest(".look"), img = card.querySelector("img");
    basket = btn.dataset.svcs.split(",");
    giftMode = false;
    look = { name: btn.dataset.name, alt: img.alt, url: new URL(card.querySelector("[data-full]").dataset.full, location.href).href, thumb: img.currentSrc || img.src };
    if (finished) resetAfterDone();
    renderBasket();
    scrollToEl($("book"));
  }
  document.addEventListener("click", function (e) {
    var b = e.target.closest("[data-look]");
    if (b && !b.closest(".lightbox")) chooseLook(b);
  });
  $("giftBtn").addEventListener("click", function () {
    if (finished) resetAfterDone();
    basket = []; look = null; giftMode = true;
    $("f-msg").value = T.lines && lang === "bg" ? "Искам да попитам за подаръчна карта." : "I would like to ask about a gift card.";
    renderBasket(); scrollToEl($("book"));
  });

  /* days */
  function renderStrip() {
    strip.textContent = "";
    for (var i = 0; i < 7; i++) {
      var d = addDays(stripStart, i), v = ymd(d);
      var b = el("button", "day"); b.type = "button"; b.dataset.date = v;
      b.setAttribute("aria-pressed", v === date ? "true" : "false"); b.setAttribute("aria-label", longDate(v));
      b.appendChild(el("small", "", d.toLocaleDateString(T.locale, { weekday: "short" })));
      b.appendChild(el("b", "", String(d.getDate())));
      strip.appendChild(b);
    }
    $("dayPrev").disabled = stripStart <= today;
  }
  strip.addEventListener("click", function (e) {
    var b = e.target.closest(".day"); if (!b) return;
    date = b.dataset.date; renderStrip(); loadSlots();
  });
  $("dayPrev").addEventListener("click", function () { stripStart = addDays(stripStart, -7); if (stripStart < today) stripStart = today; renderStrip(); });
  $("dayNext").addEventListener("click", function () { stripStart = addDays(stripStart, 7); renderStrip(); });

  /* free times as chips */
  function loadSlots() {
    var token = ++tick, m = minutes(), keep = (form.querySelector('input[name="slot"]:checked') || {}).value;
    if (!m) { tchips.textContent = ""; slotHint.textContent = T.pickFirst; return; }
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

  /* next free time (looks at the next 14 days for a one-hour visit) */
  var nextBox = $("nextFree");
  function findNext() {
    var start = new Date();
    function tryDay(i) {
      if (i > 13) return;
      var d = addDays(start, i);
      API.availability(ymd(d), 60).then(function (res) {
        if (!res.slots.length) return tryDay(i + 1);
        var when = i === 0 ? T.todayAt : i === 1 ? T.tomorrowAt : T.dayAt;
        nextBox.textContent = ""; nextBox.appendChild(document.createTextNode(T.nextFree + " "));
        var b = el("button", "", when.replace("{t}", res.slots[0]).replace("{d}", shortDate(d))); b.type = "button";
        b.addEventListener("click", function () { date = ymd(d); stripStart = d < today ? today : d; renderStrip(); loadSlots(); scrollToEl($("book")); });
        nextBox.appendChild(b); nextBox.hidden = false;
      }, function () {});
    }
    tryDay(0);
  }
  findNext();

  /* send */
  function fail(msg, f) { errEl.textContent = msg; errEl.hidden = false; if (f) f.focus(); }
  function buildPayload() {
    var t = totals(), slot = form.querySelector('input[name="slot"]:checked').value;
    var names = giftMode && !basket.length ? [T.gift] : t.names;
    return {
      name: $("f-name").value.trim(), phone: $("f-phone").value.trim(), service: names.join(", "),
      plan: { summary: names.join(" + ") + (basket.length ? ". " + T.about + " " + fmtMin(t.mmax) + ", " + priceText(t) : ""),
              minPrice: t.pmin, maxPrice: t.pmax, minMinutes: 0, maxMinutes: minutes(), extras: names.slice(1), priceOnRequest: t.request },
      date: date, time: slot, durationMinutes: minutes(),
      look: look ? { alt: look.alt, url: look.url } : null,
      message: $("f-msg").value.trim(), lang: lang
    };
  }
  function setBusy(on) { busy = on; sendBtn.disabled = on; sendBtn.classList.toggle("is-busy", on); sendBtn.textContent = on ? T.sending : T.send; form.setAttribute("aria-busy", on ? "true" : "false"); }
  form.addEventListener("submit", function (e) {
    e.preventDefault();
    if (busy) return;
    if (!basket.length && !giftMode) { fail(T.errPick); scrollToEl($("looks")); return; }
    if (!form.querySelector('input[name="slot"]:checked')) { fail(T.errTime, tchips.querySelector("input") || strip.querySelector("button")); return; }
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
    finished = true;
    done.textContent = "";
    done.appendChild(el("h3", "", T.doneH));
    var ref = el("p", "done-ref"); ref.appendChild(el("span", "", T.doneRef)); ref.appendChild(el("strong", "", rec.id)); done.appendChild(ref);
    var st = el("p", "done-status"); st.appendChild(el("span", "pill", T.statusPending)); done.appendChild(st);
    var dl = el("dl", "done-list");
    function row(k, v) { if (!v) return; dl.appendChild(el("dt", "", k)); dl.appendChild(el("dd", "", v)); }
    row(L.name, p.name); row(L.phone, p.phone); row(L.service, p.plan.summary); row(L.date, longDate(p.date)); row(L.time, p.time);
    if (p.look) row(L.look, p.look.alt);
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
    again.addEventListener("click", function () { resetAfterDone(); scrollToEl($("looks")); });
    actions.appendChild(again); done.appendChild(actions);
    form.hidden = true; done.hidden = false; done.focus({ preventScroll: true }); scrollToEl(done);
    findNext();
  }
  function resetAfterDone() {
    form.reset(); basket = []; look = null; giftMode = false; finished = false;
    done.hidden = true; form.hidden = false; errEl.hidden = true;
    renderBasket();
  }

  if (API.mode === "demo") { $("demoNote").hidden = false; $("demoNote").textContent = T.demoLine; }
  renderStrip(); renderBasket();
})();
