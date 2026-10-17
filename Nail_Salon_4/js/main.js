/* Glossy (design 4): page behaviour.
   Colour schemes, menu, the live "design your set" builder (an SVG hand redrawn as you choose), gallery filter and viewer,
   live "open now" and "next free time", and the booking (a day, a free time, your details).
   The booking talks to GlossyAPI (js/api.js): a mock server now, a real backend later (docs/API.md). */
(function () {
  "use strict";

  var CFG = window.GLOSSY_CONFIG || {};
  var API = window.GlossyAPI;
  var html = document.documentElement;
  var lang = html.lang === "bg" ? "bg" : "en";
  var reduceMotion = window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches;
  function $(id) { return document.getElementById(id); }
  var SVC = JSON.parse($("svcData").textContent);

  var T = {
    bg: {
      mapTitle: "Карта на студиото", locale: "bg-BG", hUnit: "ч", mUnit: "мин",
      opensNow: "Отворено · до {t}", openLater: "Затворено · отваря днес в {t}", openTomorrow: "Затворено · отваря утре в {t}",
      nextFree: "Следващ свободен час:", todayAt: "днес в {t}", tomorrowAt: "утре в {t}", dayAt: "{d} в {t}",
      checking: "Проверяваме свободните часове…", noSlots: "Няма свободни часове този ден. Избери друг ден.",
      slotsHint: "Свободни часове: {n}. Работим до {c}.", availError: "Не успяхме да проверим часовете. Опитай пак.",
      shown: "Показани снимки: {n}", onRequest: "по запитване", from: "от", about: "Около", artNote: "Нейл артът се оценява по запитване, според дизайна.",
      errTime: "Избери ден и час.", errName: "Въведи име и телефон.",
      errTaken: "Съжаляваме, този час току-що беше зает. Избери друг.", errInvalid: "Провери данните и опитай пак.", errGeneric: "Нещо се обърка. Опитай пак или ни се обади.",
      sending: "Изпращане…", demoLine: "Демо режим: заявките се пазят само в този браузър и нищо не се изпраща.",
      doneH: "Заявката е получена", doneRef: "Номер", statusPending: "Чака потвърждение",
      doneNext: "Ще се свържем с теб по телефона, за да потвърдим часа. Запази номера.",
      doneDemo: "Демо режим: нищо не беше изпратено. Заявката е записана само в този браузър.",
      adminLink: "Виж я в демо админ панела", again: "Нов комплект", send: "Изпрати заявката",
      setWord: "Комплект", lines: { service: "Услуги", set: "Комплект", date: "Дата", time: "Час", name: "Име", phone: "Телефон", msg: "Съобщение", look: "Стил" }
    },
    en: {
      mapTitle: "Map of the studio", locale: "en-GB", hUnit: "h", mUnit: "min",
      opensNow: "Open now · until {t}", openLater: "Closed · opens today at {t}", openTomorrow: "Closed · opens tomorrow at {t}",
      nextFree: "Next free time:", todayAt: "today at {t}", tomorrowAt: "tomorrow at {t}", dayAt: "{d} at {t}",
      checking: "Checking free times…", noSlots: "No free times on this day. Please pick another day.",
      slotsHint: "{n} free times. We close at {c}.", availError: "We could not check the free times. Please try again.",
      shown: "Photos shown: {n}", onRequest: "on request", from: "from", about: "About", artNote: "Nail art is priced on request, depending on the design.",
      errTime: "Please pick a day and a time.", errName: "Please enter your name and phone.",
      errTaken: "Sorry, that time was just taken. Please choose another.", errInvalid: "Please check your details and try again.", errGeneric: "Something went wrong. Please try again or call us.",
      sending: "Sending…", demoLine: "Demo mode: requests are kept in this browser only and nothing is sent.",
      doneH: "Request received", doneRef: "Reference", statusPending: "Waiting for confirmation",
      doneNext: "We will contact you by phone to confirm your time. Keep your reference handy.",
      doneDemo: "Demo mode: nothing was sent. The request is saved only in this browser.",
      adminLink: "See it in the demo back office", again: "New set", send: "Send the request",
      setWord: "Set", lines: { service: "Services", set: "Set", date: "Date", time: "Time", name: "Name", phone: "Phone", msg: "Message", look: "Look" }
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
  function mix(a, b, t) {
    function c(h) { h = h.replace("#", ""); return [0, 2, 4].map(function (i) { return parseInt(h.substr(i, 2), 16); }); }
    var x = c(a), y = c(b);
    return "#" + x.map(function (v, i) { var m = Math.round(v + (y[i] - v) * t); return (m < 16 ? "0" : "") + m.toString(16); }).join("");
  }

  /* ---------- Colour scheme (skin) ---------- */
  var SKINS = ["bubblegum", "lilac", "peach", "mint", "berry"];
  var skinBtns = document.querySelectorAll(".sw[data-skin]");
  var skinName = $("skinName");
  var animTimer;
  function setSkin(skin, save) {
    if (SKINS.indexOf(skin) === -1) skin = "bubblegum";
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
    if (save) { try { localStorage.setItem("glossySkin", skin); } catch (e) {} }
  }
  skinBtns.forEach(function (b) { b.addEventListener("click", function () { setSkin(b.dataset.skin, true); }); });
  var startSkin = null;
  try { startSkin = new URLSearchParams(location.search).get("skin") || localStorage.getItem("glossySkin"); } catch (e) {}
  setSkin(startSkin || "bubblegum", false);
  var yEl = $("year"); if (yEl) yEl.textContent = new Date().getFullYear();

  /* ---------- Menu and scrolling ---------- */
  var nav = $("nav"), burger = $("burger");
  burger.addEventListener("click", function () {
    var open = nav.classList.toggle("open");
    burger.setAttribute("aria-expanded", open ? "true" : "false");
  });
  nav.addEventListener("click", function (e) {
    if (e.target.closest("a, button") && nav.classList.contains("open")) { nav.classList.remove("open"); burger.setAttribute("aria-expanded", "false"); }
  });
  document.addEventListener("click", function (e) {
    var b = e.target.closest("[data-go]");
    if (b) { e.preventDefault(); scrollToEl($(b.dataset.go)); }
  });
  var topbar = $("top");
  function onScroll() { topbar.classList.toggle("scrolled", window.scrollY > 8); }
  window.addEventListener("scroll", onScroll, { passive: true }); onScroll();

  /* ---------- Scroll reveal ---------- */
  if (html.classList.contains("js-reveal")) {
    var groups = [[".sec-head", 0], [".rev", 0.1], [".g-item", 0.05], [".visit-grid > div", 0.1]];
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

  /* ================= The set builder ================= */
  var NAIL_LEN = { nat: 40, short: 48, med: 62, long: 78 };
  function nailD(shape, cx, yb, w, L) {
    var x0 = cx - w / 2, x1 = cx + w / 2, top = yb - L, r = function (n) { return Math.round(n * 10) / 10; };
    var bottom = " Q " + cx + " " + (yb + 6) + " " + x0 + " " + yb + " Z";
    switch (shape) {
      case "square": return "M" + x0 + " " + yb + " L" + x0 + " " + r(top + 3) + " Q" + x0 + " " + top + " " + r(x0 + 3) + " " + top + " L" + r(x1 - 3) + " " + top + " Q" + x1 + " " + top + " " + x1 + " " + r(top + 3) + " L" + x1 + " " + yb + bottom;
      case "almond": return "M" + x0 + " " + yb + " C" + x0 + " " + r(top + L * 0.5) + " " + r(cx - w * 0.22) + " " + r(top + L * 0.12) + " " + cx + " " + top + " C" + r(cx + w * 0.22) + " " + r(top + L * 0.12) + " " + x1 + " " + r(top + L * 0.5) + " " + x1 + " " + yb + bottom;
      case "coffin": return "M" + x0 + " " + yb + " L" + r(cx - w * 0.3) + " " + r(top + 2) + " Q" + cx + " " + r(top - 2) + " " + r(cx + w * 0.3) + " " + r(top + 2) + " L" + x1 + " " + yb + bottom;
      case "stiletto": return "M" + x0 + " " + yb + " C" + x0 + " " + r(top + L * 0.55) + " " + r(cx - 3) + " " + r(top + L * 0.2) + " " + cx + " " + top + " C" + r(cx + 3) + " " + r(top + L * 0.2) + " " + x1 + " " + r(top + L * 0.55) + " " + x1 + " " + yb + bottom;
      default: return "M" + x0 + " " + yb + " L" + x0 + " " + r(top + w / 2) + " A" + w / 2 + " " + w / 2 + " 0 0 1 " + x1 + " " + r(top + w / 2) + " L" + x1 + " " + yb + bottom;
    }
  }
  /* small nail icons on the shape buttons */
  Array.prototype.forEach.call(document.querySelectorAll("svg[data-shape]"), function (s) {
    s.innerHTML = '<path d="' + nailD(s.dataset.shape, 30, 76, 34, 66) + '" fill="currentColor"/>';
  });

  var hand = $("hand");
  var FINGERS = [{ x: 62, w: 48, h: 150, s: 1 }, { x: 118, w: 48, h: 172, s: 1 }, { x: 174, w: 48, h: 158, s: 1 }, { x: 230, w: 44, h: 124, s: 0.86 }];
  var GLITTER = [[.2, .2], [.7, .15], [.45, .3], [.3, .5], [.75, .45], [.5, .65], [.2, .75], [.68, .8], [.4, .9], [.8, .65], [.12, .45], [.55, .1]];
  function nailSvg(id, shape, cx, yb, w, L, st, ring) {
    var d = nailD(shape, cx, yb, w, L), top = yb - L, body = st.colour, g = "";
    if (st.french) body = mix(st.colour, "#F3DCD2", 0.55);
    var fill = body;
    if (st.finish === "chrome") fill = "url(#chr" + id + ")";
    var defs = '<clipPath id="cp' + id + '"><path d="' + d + '"/></clipPath>';
    if (st.finish === "chrome") defs += '<linearGradient id="chr' + id + '" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="' + mix(body, "#ffffff", 0.2) + '"/><stop offset=".35" stop-color="#ffffff" stop-opacity=".95"/><stop offset=".6" stop-color="' + body + '"/><stop offset="1" stop-color="' + mix(body, "#000000", 0.35) + '"/></linearGradient>';
    g += '<path d="' + d + '" fill="' + fill + '" class="nail"/>';
    g += '<g clip-path="url(#cp' + id + ')">';
    if (st.french) g += '<path d="M' + (cx - w) + " " + (top - 4) + " H" + (cx + w) + " V" + (top + L * 0.32) + " Q" + cx + " " + (top + L * 0.5) + " " + (cx - w) + " " + (top + L * 0.32) + ' Z" fill="#fff"/>';
    if (st.finish === "glitter") GLITTER.forEach(function (p, i) { g += '<circle cx="' + (cx - w / 2 + p[0] * w) + '" cy="' + (top + p[1] * L) + '" r="' + (1.2 + (i % 3) * 0.7) + '" fill="' + (i % 4 === 0 ? "#FFD76A" : "#ffffff") + '" opacity=".92"/>'; });
    if (st.finish === "matte") g += '<path d="' + d + '" fill="#8a8a8a" opacity=".16"/>';
    if (st.finish === "gloss" || st.finish === "chrome") g += '<rect x="' + (cx - w / 2 + 5) + '" y="' + (top + L * 0.18) + '" width="5" height="' + (L * 0.5) + '" rx="2.5" fill="#fff" opacity="' + (st.finish === "chrome" ? ".75" : ".5") + '"/>';
    if (ring) g += '<path d="M' + cx + " " + (top + L * 0.42) + " l6 7 l-6 7 l-6 -7 z" + '" fill="#fff" stroke="#E0B84A" stroke-width="1.5"/><circle cx="' + (cx - 9) + '" cy="' + (top + L * 0.7) + '" r="1.6" fill="#E0B84A"/><circle cx="' + (cx + 9) + '" cy="' + (top + L * 0.28) + '" r="1.6" fill="#E0B84A"/>';
    g += "</g>";
    return { defs: defs, body: g };
  }
  function drawHand(st) {
    var skin = "#EBC3AB", skin2 = "#E1B49A", L0 = NAIL_LEN[st.base], defs = "", out = "";
    out += '<path d="M56 242 H280 V336 Q280 412 168 418 Q58 412 56 336 Z" fill="' + skin + '"/>';
    out += '<g transform="rotate(-30 40 340)"><rect x="12" y="252" width="46" height="132" rx="23" fill="' + skin + '"/>';
    var th = nailSvg("t", st.shape, 35, 292, 36, L0 * 0.9, st, false); defs += th.defs; out += th.body + "</g>";
    FINGERS.forEach(function (f, i) {
      var y = 250 - f.h;
      out += '<rect x="' + f.x + '" y="' + y + '" width="' + f.w + '" height="' + (f.h + 24) + '" rx="' + f.w / 2 + '" fill="' + skin + '"/>';
      out += '<path d="M' + (f.x + f.w) + " " + (y + 30) + ' v' + f.h + '" stroke="' + skin2 + '" stroke-width="2" opacity=".5"/>';
      var n = nailSvg(String(i), st.shape, f.x + f.w / 2, y + 34, f.w - 10, L0 * f.s, st, st.accent && i === 2);
      defs += n.defs; out += n.body;
    });
    hand.innerHTML = '<svg viewBox="0 0 330 440" role="presentation" focusable="false"><defs>' + defs + "</defs>" + out + "</svg>";
  }

  var form = $("bookForm");
  var controls = $("controls");
  function chk(name) { return controls.querySelector('input[name="' + name + '"]:checked'); }
  function state() {
    var base = chk("base"), shape = chk("shape"), colour = chk("colour"), finish = chk("finish");
    var extras = Array.prototype.slice.call(controls.querySelectorAll('input[name="extra"]:checked')).map(function (x) { return x.value; });
    return { base: base.value, shape: shape.value, colour: colour.value, finish: finish.value, french: extras.indexOf("french") !== -1, accent: extras.indexOf("accent") !== -1,
             removal: extras.indexOf("removal") !== -1, pedi: extras.indexOf("pedi") !== -1,
             labels: [shape.dataset.label, base.dataset.label + (base.value === "nat" ? "" : " " + base.nextElementSibling.querySelector("small").textContent), colour.dataset.label, finish.dataset.label]
                .concat(Array.prototype.slice.call(controls.querySelectorAll('input[name="extra"]:checked')).map(function (x) { return x.dataset.label; })),
             svcs: serviceIds(base, finish, extras) };
  }
  function serviceIds(base, finish, extras) {
    var ids = [base.dataset.svc];
    if (finish.dataset.art === "1" || extras.indexOf("french") !== -1 || extras.indexOf("accent") !== -1) ids.push("art");
    if (extras.indexOf("removal") !== -1) ids.push("removal");
    if (extras.indexOf("pedi") !== -1) ids.push("gel_pedi");
    return ids;
  }
  function totals(ids) {
    var t = { pmin: 0, pmax: 0, mmax: 0, from: false, request: false, names: [] };
    ids.forEach(function (id) {
      var s = SVC[id]; t.pmin += s.p0; t.pmax += s.p1; t.mmax += s.min; t.names.push(s.name);
      if (s.kind === "request") t.request = true;
    });
    return t;
  }
  function priceText(t) {
    if (t.request && t.pmax === 0) return T.onRequest;
    var txt = t.pmin === t.pmax ? t.pmin + " €" : t.pmin + " – " + t.pmax + " €";
    return t.request ? T.from + " " + txt : txt;
  }
  var cur = null, look = null;
  function renderBuilder() {
    cur = state();
    drawHand(cur);
    var t = totals(cur.svcs), desc = cur.labels.join(" · ");
    $("prevCap").textContent = desc;
    function lines(ul) { ul.textContent = ""; cur.svcs.forEach(function (id) { var li = el("li"); li.appendChild(el("span", "", SVC[id].name)); li.appendChild(el("span", "", SVC[id].kind === "request" ? T.onRequest : (SVC[id].p0 === SVC[id].p1 ? SVC[id].p0 + " €" : SVC[id].p0 + " – " + SVC[id].p1 + " €"))); ul.appendChild(li); }); }
    lines($("sumLines")); lines($("bkLines"));
    var pt = priceText(t), tm = T.about + " " + fmtMin(t.mmax);
    $("sumPrice").textContent = pt; $("bkPrice").textContent = pt; $("sumTime").textContent = tm; $("bkTime").textContent = tm;
    $("qTotal").textContent = pt;
    $("sumNote").textContent = t.request ? T.artNote : "";
    $("bkDesc").textContent = T.setWord + ": " + desc;
    loadSlots();
  }
  controls.addEventListener("change", renderBuilder);
  function setRadio(name, value) { var r = controls.querySelector('input[name="' + name + '"][value="' + value + '"]'); if (r) r.checked = true; }

  /* ---------- Gallery: filter and photo viewer ---------- */
  var items = Array.prototype.slice.call(document.querySelectorAll(".g-item"));
  var filterBtns = Array.prototype.slice.call(document.querySelectorAll("[data-filter]"));
  filterBtns.forEach(function (b) {
    b.addEventListener("click", function () {
      var f = b.dataset.filter, n = 0;
      filterBtns.forEach(function (x) { x.setAttribute("aria-pressed", x === b ? "true" : "false"); });
      items.forEach(function (l) { var show = f === "all" || l.dataset.cat === f; l.hidden = !show; if (show) n++; });
      $("shown").textContent = T.shown.replace("{n}", n);
    });
  });
  var box = $("lightbox"), lbImg = $("lbImg"), current = 0;
  function vis() { return items.filter(function (i) { return !i.hidden; }); }
  function showPhoto(i) {
    var list = vis(); current = (i + list.length) % list.length;
    var it = list[current], img = it.querySelector("img");
    lbImg.src = it.dataset.full; lbImg.alt = img.alt;
    lbImg.classList.remove("swap"); void lbImg.offsetWidth; lbImg.classList.add("swap");
  }
  items.forEach(function (it) { it.addEventListener("click", function () { showPhoto(vis().indexOf(it)); box.showModal(); }); });
  $("lbClose").addEventListener("click", function () { box.close(); });
  $("lbPrev").addEventListener("click", function () { showPhoto(current - 1); });
  $("lbNext").addEventListener("click", function () { showPhoto(current + 1); });
  box.addEventListener("click", function (e) { if (e.target === box || e.target.className === "lb-inner") box.close(); });
  box.addEventListener("keydown", function (e) { if (e.key === "ArrowLeft") showPhoto(current - 1); if (e.key === "ArrowRight") showPhoto(current + 1); });
  $("lbRequest").addEventListener("click", function () {
    var it = vis()[current], img = it.querySelector("img");
    box.close();
    look = { alt: img.alt, url: new URL(it.dataset.full, location.href).href, thumb: img.currentSrc || img.src };
    showLook(); scrollToEl($("design"));
  });
  $("lookRemove").addEventListener("click", function () { look = null; showLook(); });
  function showLook() { $("lookBox").hidden = !look; if (look) { $("lookImg").src = look.thumb || ""; $("lookText").textContent = look.alt; } }

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

  /* ================= Booking ================= */
  var dchips = $("dchips"), tchips = $("tchips"), slotHint = $("slotHint");
  var errEl = $("bkError"), sendBtn = $("bkSend"), done = $("bkDone");
  var today = new Date(); today = new Date(today.getFullYear(), today.getMonth(), today.getDate());
  var date = "", tick = 0, busy = false, finished = false;
  function initialDate() {
    var now = new Date(), h = dayHours(now), late = now.getHours() * 60 + now.getMinutes() > toMinutes(h[1]) - 120;
    return ymd(late ? addDays(today, 1) : today);
  }
  function buildDays() {
    dchips.textContent = "";
    for (var i = 0; i < 14; i++) {
      var d = addDays(today, i), v = ymd(d), lab = el("label", "dc"), inp = el("input");
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
    if (r) r.checked = true;
  }
  function loadSlots() {
    if (!cur) return;
    var token = ++tick, m = totals(cur.svcs).mmax, keep = (form.querySelector('input[name="slot"]:checked') || {}).value;
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
  form.addEventListener("change", function (e) {
    if (e.target.name === "day") { date = e.target.value; loadSlots(); }
    if (e.target.name === "slot") errEl.hidden = true;
  });

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
        b.addEventListener("click", function () { setDate(ymd(d)); loadSlots(); scrollToEl($("book")); });
        nextBox.appendChild(b); nextBox.hidden = false;
      }, function () {});
    }
    tryDay(0);
  }
  findNext();

  function fail(msg, f) { errEl.textContent = msg; errEl.hidden = false; if (f) f.focus(); }
  function buildPayload() {
    var t = totals(cur.svcs), slot = form.querySelector('input[name="slot"]:checked').value, desc = cur.labels.join(" · ");
    return {
      name: $("f-name").value.trim(), phone: $("f-phone").value.trim(), service: t.names.join(", "),
      plan: { summary: T.setWord + ": " + desc + ". " + t.names.join(" + ") + ". " + T.about + " " + fmtMin(t.mmax) + ", " + priceText(t),
              minPrice: t.pmin, maxPrice: t.pmax, minMinutes: 0, maxMinutes: t.mmax, extras: t.names.slice(1), priceOnRequest: t.request },
      date: date, time: slot, durationMinutes: t.mmax,
      look: look ? { alt: look.alt, url: look.url } : null,
      message: $("f-msg").value.trim(), lang: lang
    };
  }
  function setBusy(on) { busy = on; sendBtn.disabled = on; sendBtn.classList.toggle("is-busy", on); sendBtn.textContent = on ? T.sending : T.send; form.setAttribute("aria-busy", on ? "true" : "false"); }
  form.addEventListener("submit", function (e) {
    e.preventDefault();
    if (busy) return;
    if (!form.querySelector('input[name="slot"]:checked')) { fail(T.errTime, tchips.querySelector("input") || dchips.querySelector("input")); return; }
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
    again.addEventListener("click", function () { resetAfterDone(); scrollToEl($("design")); });
    actions.appendChild(again); done.appendChild(actions);
    form.hidden = true; done.hidden = false; done.focus({ preventScroll: true }); scrollToEl(done);
    findNext();
  }
  function resetAfterDone() {
    form.reset(); look = null; showLook(); finished = false;
    done.hidden = true; form.hidden = false; errEl.hidden = true;
    setDate(initialDate()); renderBuilder();
  }

  if (API.mode === "demo") { $("demoNote").hidden = false; $("demoNote").textContent = T.demoLine; }
  date = initialDate(); buildDays(); setDate(date);
  renderBuilder();
})();
