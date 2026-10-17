/* Sunday Stems (design 3): page behaviour.
   Colour schemes, menu, "this week's bouquet" with the order deadline, the season calendar, and the subscription builder
   (size, rhythm, length, extras, first delivery and window, details) with a price slip that updates as you choose.
   The builder talks to SundayAPI (js/api.js): a mock server now, a real backend later (docs/API.md). */
(function () {
  "use strict";

  var CFG = window.SUNDAY_CONFIG || {};
  var API = window.SundayAPI;
  var html = document.documentElement;
  var lang = html.lang === "bg" ? "bg" : "en";
  var reduceMotion = window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches;
  function $(id) { return document.getElementById(id); }
  var D = JSON.parse($("sundayData").textContent);

  var T = {
    bg: {
      locale: "bg-BG", mapTitle: "Карта на магазина",
      slotsHint: "Свободни прозорци: {n}.", noSlots: "Няма свободни прозорци този ден. Избери друга дата.", checking: "Проверяваме свободните прозорци…", pickFirst: "Избери първа доставка, за да видиш часовете.", availError: "Не успяхме да проверим часовете. Опитай пак.",
      sizeL: "Размер", rhythmL: "Ритъм", lengthL: "Продължителност", extrasL: "Допълнения", deliveryL: "Доставка", pickupL: "Взимане от магазина", firstL: "Първа доставка", windowL: "Прозорец",
      vase: "ваза", gift: "подарък за {n}", none: "няма", save: "Спестяваш {p} % на всяка доставка.", per: "{p} на доставка", open: "до спиране", deliveries: "{n} доставки",
      errTime: "Избери първа доставка и прозорец.", errName: "Въведи име и телефон.", errAddr: "Въведи адрес за доставка.", errTo: "Кажи ни за кого е подаръкът.",
      errTaken: "Съжаляваме, този прозорец току-що беше зает. Избери друг.", errInvalid: "Провери данните и опитай пак.", errGeneric: "Нещо се обърка. Опитай пак или ни се обади.",
      sending: "Изпращане…", demoLine: "Демо режим: заявките се пазят само в този браузър и нищо не се изпраща.",
      doneH: "Абонаментът е заявен", doneRef: "Номер", statusPending: "Чака потвърждение",
      doneNext: "Ще се свържем с теб по телефона, за да потвърдим първата доставка. Запази номера.",
      doneDemo: "Демо режим: нищо не беше изпратено. Заявката е записана само в този браузър.",
      adminLink: "Виж я в демо админ панела", again: "Нов абонамент", send: "Започни абонамента",
      sub: "Абонамент", lines: { name: "Име", phone: "Телефон", service: "Абонамент", date: "Първа доставка", time: "Прозорец", addr: "Адрес", card: "Картичка", msg: "Съобщение" }
    },
    en: {
      locale: "en-GB", mapTitle: "Map of the shop",
      slotsHint: "{n} free windows.", noSlots: "No free windows on this day. Please pick another date.", checking: "Checking free windows…", pickFirst: "Pick a first delivery to see delivery windows.", availError: "We could not check the windows. Please try again.",
      sizeL: "Size", rhythmL: "Rhythm", lengthL: "Length", extrasL: "Extras", deliveryL: "Delivery", pickupL: "Pick up in the shop", firstL: "First delivery", windowL: "Window",
      vase: "vase", gift: "gift for {n}", none: "none", save: "You save {p}% on every delivery.", per: "{p} per delivery", open: "until you stop", deliveries: "{n} deliveries",
      errTime: "Please pick a first delivery and a window.", errName: "Please enter your name and phone.", errAddr: "Please enter a delivery address.", errTo: "Please tell us who the gift is for.",
      errTaken: "Sorry, that window was just taken. Please choose another.", errInvalid: "Please check your details and try again.", errGeneric: "Something went wrong. Please try again or call us.",
      sending: "Sending…", demoLine: "Demo mode: requests are kept in this browser only and nothing is sent.",
      doneH: "Subscription requested", doneRef: "Reference", statusPending: "Waiting for confirmation",
      doneNext: "We will contact you by phone to confirm the first delivery. Keep your reference handy.",
      doneDemo: "Demo mode: nothing was sent. The request is saved only in this browser.",
      adminLink: "See it in the demo back office", again: "New subscription", send: "Start my subscription",
      sub: "Subscription", lines: { name: "Name", phone: "Phone", service: "Subscription", date: "First delivery", time: "Window", addr: "Address", card: "Card", msg: "Message" }
    }
  }[lang];

  /* ---------- Small helpers ---------- */
  function pad(n) { return (n < 10 ? "0" : "") + n; }
  function ymd(d) { return d.getFullYear() + "-" + pad(d.getMonth() + 1) + "-" + pad(d.getDate()); }
  function toDate(v) { var p = v.split("-"); return new Date(+p[0], +p[1] - 1, +p[2]); }
  function addDays(d, n) { return new Date(d.getFullYear(), d.getMonth(), d.getDate() + n); }
  function el(tag, cls, text) { var n = document.createElement(tag); if (cls) n.className = cls; if (text !== undefined) n.textContent = text; return n; }
  function scrollToEl(n) { n.scrollIntoView({ behavior: reduceMotion ? "auto" : "smooth", block: "start" }); }
  function money(n) { return n.toLocaleString(T.locale, { minimumFractionDigits: n % 1 ? 2 : 0, maximumFractionDigits: 2 }) + " €"; }
  function longDate(v) { return toDate(v).toLocaleDateString(T.locale, { weekday: "long", day: "numeric", month: "long", year: "numeric" }); }
  function chipDate(d) { return d.toLocaleDateString(T.locale, { weekday: "short", day: "numeric", month: "short" }); }
  function weekday(d, style) { return d.toLocaleDateString(T.locale, { weekday: style || "long" }); }

  /* ---------- Colour scheme (skin) ---------- */
  var SKINS = ["tulip", "lemon", "peony", "iris", "sage"];
  var skinBtns = document.querySelectorAll(".sw[data-skin]");
  var skinName = $("skinName");
  var animTimer;
  function setSkin(skin, save) {
    if (SKINS.indexOf(skin) === -1) skin = "tulip";
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
    if (save) { try { localStorage.setItem("sundaySkin", skin); } catch (e) {} }
  }
  skinBtns.forEach(function (b) { b.addEventListener("click", function () { setSkin(b.dataset.skin, true); }); });
  var startSkin = null;
  try { startSkin = new URLSearchParams(location.search).get("skin") || localStorage.getItem("sundaySkin"); } catch (e) {}
  setSkin(startSkin || "tulip", false);
  var yEl = $("year"); if (yEl) yEl.textContent = new Date().getFullYear();

  /* ---------- Menu ---------- */
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
    document.querySelectorAll(".sec-head, .week-pic, .week-text, .mo, .steps li, .rev, .visit-grid > div").forEach(function (n, i) {
      n.classList.add("rv"); n.style.setProperty("--d", ((i % 4) * 0.07).toFixed(2) + "s"); io.observe(n);
    });
  }

  /* ---------- Map ---------- */
  var mapBox = $("mapBox");
  $("mapLoad").addEventListener("click", function () {
    var f = document.createElement("iframe");
    f.src = mapBox.dataset.src; f.title = T.mapTitle; f.loading = "lazy"; f.referrerPolicy = "no-referrer";
    mapBox.textContent = ""; mapBox.appendChild(f);
  });

  /* ---------- Season calendar: mark this month ---------- */
  var nowMonth = new Date().getMonth();
  Array.prototype.forEach.call(document.querySelectorAll(".mo"), function (m) {
    if (+m.dataset.m === nowMonth) { m.classList.add("is-now"); m.querySelector(".now").hidden = false; }
  });

  /* ---------- This week's bouquet and the order deadline ---------- */
  function weekNumber(d) {
    var t = new Date(Date.UTC(d.getFullYear(), d.getMonth(), d.getDate())), day = t.getUTCDay() || 7;
    t.setUTCDate(t.getUTCDate() + 4 - day);
    return Math.ceil(((t - new Date(Date.UTC(t.getUTCFullYear(), 0, 1))) / 864e5 + 1) / 7);
  }
  /* the next Saturday delivery whose Thursday 12:00 deadline has not passed */
  function nextDelivery(now) {
    var d = new Date(now.getFullYear(), now.getMonth(), now.getDate());
    var add = (6 - d.getDay() + 7) % 7;
    d = addDays(d, add);
    var cut = new Date(d.getFullYear(), d.getMonth(), d.getDate() - 2, 12, 0);
    if (cut <= now) { d = addDays(d, 7); cut = new Date(d.getFullYear(), d.getMonth(), d.getDate() - 2, 12, 0); }
    return { date: d, cut: cut };
  }
  function renderWeek() {
    var now = new Date(), nd = nextDelivery(now), idx = weekNumber(nd.date) % D.weekly.length, w = D.weekly[idx];
    $("weekImg").src = w.src; $("weekImg").alt = w.name;
    $("weekName").textContent = w.name; $("weekStems").textContent = w.stems;
    $("stickName").textContent = w.name;
    var left = nd.cut - now, hours = Math.floor(left / 36e5), mins = Math.floor((left % 36e5) / 6e4), line;
    if (left < 48 * 36e5) line = D.cutIn.replace("{x}", hours + " " + D.hUnit + " " + mins + " " + D.mUnit).replace("{s}", weekday(nd.date));
    else line = D.cutBy.replace("{d}", weekday(nd.cut)).replace("{t}", pad(nd.cut.getHours()) + ":" + pad(nd.cut.getMinutes())).replace("{s}", weekday(nd.date));
    $("cutLine").textContent = line; $("stickCut").textContent = line;
    var ul = $("upNext"); ul.textContent = "";
    for (var k = 1; k <= 3; k++) {
      var dd = addDays(nd.date, 7 * k), nw = D.weekly[weekNumber(dd) % D.weekly.length];
      var li = el("li"); li.appendChild(el("span", "", dd.toLocaleDateString(T.locale, { day: "numeric", month: "short" }))); li.appendChild(el("b", "", nw.name)); ul.appendChild(li);
    }
  }
  renderWeek(); setInterval(renderWeek, 60000);

  /* ================= The subscription builder ================= */
  var form = $("subForm"), dates = $("dates"), tchips = $("tchips"), slotHint = $("slotHint");
  var errEl = $("bkError"), sendBtn = $("bkSend"), done = $("bkDone");
  var today = new Date(); today = new Date(today.getFullYear(), today.getMonth(), today.getDate());
  var tick = 0, busy = false, firstDate = "";
  function chk(name) { return form.querySelector('input[name="' + name + '"]:checked'); }
  function state() {
    var s = chk("size"), f = chk("freq"), l = chk("len");
    var per = +s.dataset.price * (1 - (+l.dataset.off) / 100), n = +l.dataset.n, vase = form.querySelector('input[name="vase"]').checked;
    return { size: s, freq: f, len: l, per: Math.round(per * 100) / 100, n: n, month: Math.round(per * (+f.dataset.pm) * 100) / 100,
             total: n ? Math.round((per * n + (vase ? D.vase : 0)) * 100) / 100 : 0, vase: vase, gift: form.querySelector('input[name="gift"]').checked,
             delivery: chk("fulfil").value === "delivery", day: +chk("day").value };
  }
  function planName(st) { return T.sub + ": " + st.size.dataset.name + " · " + st.freq.dataset.name + " · " + (st.n ? T.deliveries.replace("{n}", st.n) : T.open); }

  function renderDates() {
    var st = state(), keep = firstDate, list = [];
    dates.textContent = "";
    var d = addDays(today, 2);
    while (d.getDay() !== st.day) d = addDays(d, 1);
    for (var i = 0; i < 4; i++) list.push(addDays(d, 7 * i));
    if (!keep || list.map(ymd).indexOf(keep) === -1) keep = ymd(list[0]);
    firstDate = keep;
    list.forEach(function (x) {
      var lab = el("label", "dc"), inp = el("input"), v = ymd(x);
      inp.type = "radio"; inp.name = "first"; inp.value = v; inp.checked = v === firstDate;
      lab.appendChild(inp);
      lab.appendChild(el("small", "", x.toLocaleDateString(T.locale, { weekday: "short" })));
      lab.appendChild(el("b", "", String(x.getDate())));
      lab.appendChild(el("small", "", x.toLocaleDateString(T.locale, { month: "short" })));
      lab.title = longDate(v); dates.appendChild(lab);
    });
  }
  function loadSlots() {
    var token = ++tick, keep = (form.querySelector('input[name="slot"]:checked') || {}).value;
    if (!firstDate) { tchips.textContent = ""; slotHint.textContent = T.pickFirst; return; }
    slotHint.textContent = T.checking;
    API.availability(firstDate, 30).then(function (res) {
      if (token !== tick) return;
      tchips.textContent = "";
      res.slots.forEach(function (s) {
        var lab = el("label", "tc"), inp = el("input");
        inp.type = "radio"; inp.name = "slot"; inp.value = s; if (s === keep) inp.checked = true;
        lab.appendChild(inp); lab.appendChild(document.createTextNode(s)); tchips.appendChild(lab);
      });
      slotHint.textContent = res.slots.length ? T.slotsHint.replace("{n}", res.slots.length) : T.noSlots;
      renderSlip();
    }, function () { if (token === tick) slotHint.textContent = T.availError; });
  }

  function renderSlip() {
    var st = state(), rows = $("slipRows"), slot = chk("slot");
    $("slipName").textContent = planName(st);
    rows.textContent = "";
    function row(k, v) { rows.appendChild(el("dt", "", k)); rows.appendChild(el("dd", "", v)); }
    row(T.sizeL, st.size.dataset.name + " · " + money(+st.size.dataset.price));
    row(T.rhythmL, st.freq.dataset.name);
    row(T.lengthL, st.n ? T.deliveries.replace("{n}", st.n) : T.open);
    row(T.extrasL, [st.vase ? T.vase : "", st.gift ? T.gift.replace("{n}", ($("f-to").value.trim() || "…")) : ""].filter(Boolean).join(", ") || T.none);
    row(T.deliveryL, st.delivery ? weekday(toDate(firstDate)) : T.pickupL);
    if (firstDate) row(T.firstL, chipDate(toDate(firstDate)) + (slot ? " · " + slot.value : ""));
    $("slipPer").textContent = money(st.per);
    $("slipMonth").textContent = money(st.month);
    $("slipTotalL").textContent = st.n ? D.totalL.replace("{n}", st.n) : D.totalOpen;
    $("slipTotal").textContent = st.n ? money(st.total) : "—";
    var off = +st.len.dataset.off;
    $("slipSave").textContent = off ? T.save.replace("{p}", off) : "";
    $("qTotal").textContent = money(st.per);
    $("giftBox").hidden = !st.gift;
    $("addrBox").hidden = !st.delivery;
    $("dayOpts").hidden = false;
  }
  form.addEventListener("change", function (e) {
    var n = e.target.name;
    if (n === "day") { firstDate = ""; renderDates(); loadSlots(); }
    else if (n === "first") { firstDate = e.target.value; loadSlots(); }
    else if (n === "slot") errEl.hidden = true;
    renderSlip();
  });
  $("f-to").addEventListener("input", renderSlip);

  function fail(msg, f) { errEl.textContent = msg; errEl.hidden = false; if (f) f.focus(); }
  function buildPayload() {
    var st = state(), slot = chk("slot").value, msgParts = [];
    if (st.gift) msgParts.push(T.gift.replace("{n}", $("f-to").value.trim()));
    if ($("f-msg").value.trim()) msgParts.push($("f-msg").value.trim());
    var summary = planName(st) + ". " + money(st.per) + " / " + (lang === "bg" ? "доставка" : "delivery") + ", " + money(st.month) + " / " + (lang === "bg" ? "месец" : "month") +
      (st.n ? ", " + (lang === "bg" ? "общо " : "total ") + money(st.total) : "") + (st.vase ? " (+ " + T.vase + ")" : "") + ".";
    return {
      name: $("f-name").value.trim(), phone: $("f-phone").value.trim(), service: planName(st),
      plan: { summary: summary, minPrice: st.per, maxPrice: st.per, minMinutes: 30, maxMinutes: 30, extras: [st.vase ? T.vase : ""].filter(Boolean), priceOnRequest: false },
      fulfil: st.delivery ? "delivery" : "pickup", address: st.delivery ? $("f-addr").value.trim() : "", card: $("f-card").value.trim(),
      date: firstDate, time: slot, durationMinutes: 30, look: null, message: msgParts.join(" · "), lang: lang
    };
  }
  function setBusy(on) { busy = on; sendBtn.disabled = on; sendBtn.classList.toggle("is-busy", on); sendBtn.textContent = on ? T.sending : T.send; form.setAttribute("aria-busy", on ? "true" : "false"); }
  form.addEventListener("submit", function (e) {
    e.preventDefault();
    if (busy) return;
    var st = state();
    if (!firstDate || !chk("slot")) { fail(T.errTime, tchips.querySelector("input") || dates.querySelector("input")); return; }
    if (!$("f-name").value.trim()) { fail(T.errName, $("f-name")); return; }
    if (!$("f-phone").value.trim()) { fail(T.errName, $("f-phone")); return; }
    if (st.gift && !$("f-to").value.trim()) { fail(T.errTo, $("f-to")); return; }
    if (st.delivery && !$("f-addr").value.trim()) { fail(T.errAddr, $("f-addr")); return; }
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
    row(L.name, p.name); row(L.phone, p.phone); row(L.service, p.plan.summary); row(L.date, longDate(p.date)); row(L.time, p.time); row(L.addr, p.address); row(L.card, p.card); row(L.msg, p.message);
    done.appendChild(dl);
    done.appendChild(el("p", "", T.doneNext));
    var actions = el("div", "done-actions");
    if (API.mode === "demo") {
      done.appendChild(el("p", "demo-note", T.doneDemo));
      var link = el("a", "btn btn-light btn-sm", T.adminLink);
      var adm = document.querySelector('.foot a[href*="admin"]'); link.href = adm ? adm.href : "admin.html";
      actions.appendChild(link);
    }
    var again = el("button", "btn btn-ghost btn-sm", T.again); again.type = "button";
    again.addEventListener("click", function () { form.reset(); firstDate = ""; done.hidden = true; form.hidden = false; errEl.hidden = true; renderDates(); loadSlots(); renderSlip(); scrollToEl($("plan")); });
    actions.appendChild(again); done.appendChild(actions);
    form.hidden = true; done.hidden = false; done.focus({ preventScroll: true }); scrollToEl(done);
  }

  if (API.mode === "demo") { $("demoNote").hidden = false; $("demoNote").textContent = T.demoLine; }
  renderDates(); renderSlip(); loadSlots();
})();
