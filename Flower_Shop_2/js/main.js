(function () {
  "use strict";

  var html = document.documentElement;
  var lang = html.lang === "bg" ? "bg" : "en";
  var $ = function (id) { return document.getElementById(id); };
  var reduceMotion = window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches;
  var CFG = window.VERBENA_CONFIG || {};
  var API = window.VerbenaAPI;

  var T = {
    bg: {
      shown: "Показани артикули: {n}",
      mapTitle: "Карта на цветарницата",
      hint: "Часове от {a} до {b}. Поръчката се приготвя около {d}. Затваряме в {c}.",
      hintNoDate: "Показани са часовете за делнични дни. Поръчката се приготвя около {d}. Избери дата, за да видиш конкретния ден.",
      cutoffOpen: "Поръчай до {t} за доставка днес", cutoffClosed: "Доставките за днес са затворени. Поръчай сега за утре.",
      pickup: "Вземане от магазина", delivery: "Доставка",
      checking: "Проверяваме свободните часове…",
      someTaken: "Някои часове вече са заети.",
      noSlots: "Няма начален час, който се събира този ден. Избери друга дата.",
      availError: "Не успяхме да проверим свободните часове. Опитай пак.",
      locale: "bg-BG",
      lines: { name: "Име", phone: "Телефон", service: "Букет", plan: "Избор", fulfil: "Получаване", addr: "Адрес", card: "Картичка", date: "Дата", time: "Час", look: "Харесана снимка", msg: "Бележки" },
      hUnit: "ч", mUnit: "мин", about: "Около",
      lookAdded: "Избраният артикул е добавен към поръчката ти.",
      planAdded: "Изборът ти е добавен към поръчката.",
      sending: "Изпращане…",
      demoLine: "Демо режим: поръчките се пазят само в този браузър и нищо не се изпраща.",
      errTaken: "Съжаляваме, този час току-що беше зает. Избери друг час.",
      errInvalid: "Провери данните във формата и опитай пак.",
      errGeneric: "Нещо се обърка. Опитай пак или ни се обади.",
      doneH: "Поръчката е получена", doneRef: "Номер на поръчката", doneStatus: "Статус", statusPending: "Чака потвърждение",
      doneNext: "Ще се свържем с теб по телефона, за да потвърдим поръчката и доставката. Запази номера на поръчката.",
      doneDemo: "Демо режим: нищо не беше изпратено. Поръчката е записана само в този браузър.",
      again: "Направи нова поръчка", adminLink: "Виж я в демо админ панела"
    },
    en: {
      shown: "Items shown: {n}",
      mapTitle: "Map of the flower shop",
      hint: "Times from {a} to {b}. Your order needs about {d} to prepare. We close at {c}.",
      hintNoDate: "Weekday times are shown. Your order needs about {d} to prepare. Pick a date to see that day.",
      cutoffOpen: "Order within {t} for delivery today", cutoffClosed: "Today's delivery orders are closed. Order now for tomorrow.",
      pickup: "Pick up in the shop", delivery: "Delivery",
      checking: "Checking free times…",
      someTaken: "Some times are already taken.",
      noSlots: "No start time fits on this day. Please pick another date.",
      availError: "We could not check the free times. Please try again.",
      locale: "en-GB",
      lines: { name: "Name", phone: "Phone", service: "Bouquet", plan: "Your choice", fulfil: "Receive", addr: "Address", card: "Card message", date: "Date", time: "Time", look: "Photo I like", msg: "Notes" },
      hUnit: "h", mUnit: "min", about: "About",
      lookAdded: "The item was added to your order.",
      planAdded: "Your choice was added to the order.",
      sending: "Sending…",
      demoLine: "Demo mode: orders are kept in this browser only and nothing is sent.",
      errTaken: "Sorry, that time was just taken. Please choose another time.",
      errInvalid: "Please check the form and try again.",
      errGeneric: "Something went wrong. Please try again or call us.",
      doneH: "Order received", doneRef: "Reference", doneStatus: "Status", statusPending: "Waiting for confirmation",
      doneNext: "We will contact you by phone to confirm your order and delivery. Keep your reference handy.",
      doneDemo: "Demo mode: nothing was sent. The order is saved only in this browser.",
      again: "Make another order", adminLink: "See it in the demo back office"
    }
  }[lang];

  /* ---------- Same-day cut-off: "order within 2 h 10 min for delivery today" (calculated from the opening hours) ---------- */
  var cutEl = $("cutoff");
  function updateCutoff() {
    if (!cutEl || !API.hours) return;
    var now = new Date(), day = now.getDay(), h = day === 0 || day === 6 ? API.hours.weekend : API.hours.weekday;
    var cut = Math.min(toMinutes(CFG.cutoff || "15:00"), toMinutes(h[1]) - (CFG.leadMinutes || 0));
    var nowM = now.getHours() * 60 + now.getMinutes();
    var open = nowM < cut;
    cutEl.textContent = open ? T.cutoffOpen.replace("{t}", nowM < toMinutes(h[0]) ? label(cut) : fmtMin(cut - nowM)) : T.cutoffClosed;
    cutEl.classList.toggle("closed", !open);
    cutEl.hidden = false;
  }

  /* ---------- Colour scheme (skin) ---------- */
  var SKINS = ["sage", "rose", "terracotta", "lavender", "botanical"];
  var skinBtns = document.querySelectorAll(".sw[data-skin]");
  var skinName = $("skinName");
  var animTimer;

  function setSkin(skin, save) {
    if (SKINS.indexOf(skin) === -1) skin = "sage";
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
    if (save) { try { localStorage.setItem("verbenaSkin", skin); } catch (e) {} }
  }
  skinBtns.forEach(function (b) { b.addEventListener("click", function () { setSkin(b.dataset.skin, true); }); });

  var startSkin = null;
  try { startSkin = new URLSearchParams(location.search).get("skin") || localStorage.getItem("verbenaSkin"); } catch (e) {}
  setSkin(startSkin || "sage", false);

  /* ---------- Header and menu ---------- */
  var top = $("top"), nav = $("nav"), burger = $("burger");
  var lastY = window.scrollY;
  function onScroll() {
    var y = window.scrollY, menuOpen = nav.classList.contains("open");
    top.classList.toggle("scrolled", y > 60);
    /* hide the bar while reading downwards, bring it back as soon as the visitor scrolls up */
    if (!menuOpen && y > 360 && y > lastY + 6) top.classList.add("hide");
    else if (y < lastY - 6 || y <= 360 || menuOpen) top.classList.remove("hide");
    lastY = y;
  }
  onScroll();
  addEventListener("scroll", onScroll, { passive: true });
  function setMenu(open) {
    nav.classList.toggle("open", open);
    top.classList.toggle("menu-open", open);
    burger.setAttribute("aria-expanded", open ? "true" : "false");
  }
  burger.addEventListener("click", function () { setMenu(!nav.classList.contains("open")); });
  nav.addEventListener("click", function (e) {
    if (e.target.closest("a") && nav.classList.contains("open")) setMenu(false);
  });
  var y = $("year"); if (y) y.textContent = new Date().getFullYear();

  /* ---------- Scroll reveal: sections ease in as they come into view ---------- */
  if (html.classList.contains("js-reveal")) {
    var groups = [
      [".strip li", 0.06, false], [".sec-head > div", 0.08, false], [".occ-tile", 0.08, false], [".prod", 0.07, true], [".plist", 0.1, false],
      [".plan-intro > *", 0.08, false], [".plan-card", 0, false], [".how-media", 0, false], [".how-text > *", 0.07, false], [".steps li", 0.1, false],
      [".rev", 0.1, false], [".faq-list details", 0.05, false], [".contact-info > *", 0.07, false], [".request-col", 0, false]
    ];
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (!en.isIntersecting) return;
        io.unobserve(en.target);
        en.target.classList.add("in");
        /* After the animation the normal styles come back (hover effects, etc.). */
        setTimeout(function () { en.target.classList.remove("rv", "in"); en.target.style.removeProperty("--d"); }, 1300);
      });
    }, { threshold: 0.12, rootMargin: "0px 0px -6% 0px" });
    groups.forEach(function (g) {
      document.querySelectorAll(g[0]).forEach(function (n, i) {
        n.classList.add("rv");
        n.style.setProperty("--d", ((g[2] ? i % 4 : i) * g[1]).toFixed(2) + "s");   /* catalog cards cascade by column */
        io.observe(n);
      });
    });
  }

  /* ---------- Small helpers ---------- */
  function pad(n) { return (n < 10 ? "0" : "") + n; }
  function toDate(v) { var p = v.split("-"); return new Date(+p[0], +p[1] - 1, +p[2]); }
  function toMinutes(hhmm) { var p = hhmm.split(":"); return +p[0] * 60 + +p[1]; }
  function label(m) { return pad(Math.floor(m / 60)) + ":" + pad(m % 60); }
  function fmtMin(m) {
    var h = Math.floor(m / 60), r = m % 60, out = [];
    if (h) out.push(h + " " + T.hUnit);
    if (r) out.push(r + " " + T.mUnit);
    return out.join(" ");
  }
  function fmtRange(a, b, f) { return a === b ? f(a) : f(a) + " – " + f(b); }
  function longDate(v) { return toDate(v).toLocaleDateString(T.locale, { weekday: "long", day: "numeric", month: "long", year: "numeric" }); }
  function scrollToEl(el) { el.scrollIntoView({ behavior: reduceMotion ? "auto" : "smooth", block: "start" }); }
  function el(tag, cls, text) { var n = document.createElement(tag); if (cls) n.className = cls; if (text !== undefined) n.textContent = text; return n; }

  /* ---------- Request form: shared state ---------- */
  var form = $("requestForm");
  var serviceEl = $("f-service"), dateEl = $("f-date"), timeEl = $("f-time"), hint = $("timeHint");
  var plan = null;   /* chosen in "Plan your visit" */
  var look = null;   /* photo picked in the gallery viewer */
  var live = $("formLive");
  function announce(msg) { live.textContent = ""; setTimeout(function () { live.textContent = msg; }, 30); }

  /* ---------- Catalog: occasion and budget filters, photo viewer, "Choose" ---------- */
  var cards = Array.prototype.slice.call(document.querySelectorAll(".prod"));
  var occChips = document.querySelectorAll("[data-occ-filter]");
  var budChips = document.querySelectorAll("[data-budget-filter]");
  var status = $("catStatus"), catEmpty = $("catEmpty");
  var occ = "all", budget = "all";

  function inBudget(price, b) {
    if (b === "all") return true;
    if (!price) return false;   /* "on request" items have no price to compare */
    return b === "u25" ? price < 25 : b === "m" ? price >= 25 && price <= 45 : price > 45;
  }
  function applyFilter() {
    var n = 0;
    cards.forEach(function (c) {
      var ok = (occ === "all" || c.dataset.occ.split(" ").indexOf(occ) !== -1) && inBudget(+c.dataset.price, budget);
      c.hidden = !ok;
      if (ok) {
        c.classList.remove("rv", "in", "pop");   /* a card shown by the filter should never stay hidden */
        c.style.setProperty("--d", (n % 4 * 0.05).toFixed(2) + "s");
        void c.offsetWidth; c.classList.add("pop");
        n++;
      }
    });
    status.textContent = T.shown.replace("{n}", n);
    catEmpty.hidden = n > 0;
  }
  function pressed(list, attr, value) {
    list.forEach(function (c) { c.setAttribute("aria-pressed", c.getAttribute(attr) === value ? "true" : "false"); });
  }
  occChips.forEach(function (c) {
    c.addEventListener("click", function () { occ = c.dataset.occFilter; pressed(occChips, "data-occ-filter", occ); applyFilter(); });
  });
  budChips.forEach(function (c) {
    c.addEventListener("click", function () { budget = c.dataset.budgetFilter; pressed(budChips, "data-budget-filter", budget); applyFilter(); });
  });
  document.querySelectorAll(".occ-tile").forEach(function (t) {
    t.addEventListener("click", function () {
      occ = t.dataset.occ; budget = "all";
      pressed(occChips, "data-occ-filter", occ); pressed(budChips, "data-budget-filter", budget);
      applyFilter();
      scrollToEl($("catalog"));
    });
  });

  var box = $("lightbox"), lbImg = $("lbImg"), current = 0;
  function visible() { return cards.filter(function (c) { return !c.hidden; }); }
  function show(i) {
    var list = visible();
    if (!list.length) return;
    current = (i + list.length) % list.length;
    var c = list[current], img = c.querySelector("img");
    lbImg.src = c.dataset.full;
    lbImg.alt = img.alt;
    lbImg.classList.remove("swap"); void lbImg.offsetWidth; lbImg.classList.add("swap");
  }
  cards.forEach(function (c) {
    c.querySelector(".prod-img").addEventListener("click", function () { show(visible().indexOf(c)); box.showModal(); });
  });
  $("lbClose").addEventListener("click", function () { box.close(); });
  $("lbPrev").addEventListener("click", function () { show(current - 1); });
  $("lbNext").addEventListener("click", function () { show(current + 1); });
  box.addEventListener("click", function (e) { if (e.target === box || e.target.className === "lb-inner") box.close(); });
  box.addEventListener("keydown", function (e) {
    if (e.key === "ArrowLeft") show(current - 1);
    if (e.key === "ArrowRight") show(current + 1);
  });

  /* "Choose": puts the item (and its photo) into the order form */
  var lookChip = $("lookChip");
  function setLook(card) {
    var img = card.querySelector("img");
    look = { alt: img.alt, url: new URL(card.dataset.full, location.href).href };
    $("lookImg").src = img.currentSrc || img.src;
    $("lookText").textContent = card.dataset.name;
    lookChip.hidden = false;
  }
  function clearLook() { look = null; lookChip.hidden = true; }
  function choose(card) {
    setLook(card);
    serviceEl.value = card.dataset.name;
    if (plan && serviceEl.value !== plan.opt) clearPlan();
    updateTimes();
    showForm();
    scrollToEl(form);
    announce(T.lookAdded);
    setTimeout(function () { $("f-name").focus({ preventScroll: true }); }, reduceMotion ? 0 : 500);
  }
  cards.forEach(function (c) { c.querySelector(".prod-add").addEventListener("click", function () { choose(c); }); });
  $("lbRequest").addEventListener("click", function () {
    var c = visible()[current];
    if (!c) return;
    box.close();
    choose(c);
  });
  $("lookRemove").addEventListener("click", clearLook);

  /* ---------- Map: loads only when the visitor asks ---------- */
  var mapBox = $("mapBox");
  $("mapLoad").addEventListener("click", function () {
    var f = document.createElement("iframe");
    f.src = mapBox.dataset.src;
    f.title = T.mapTitle;
    f.loading = "lazy";
    mapBox.textContent = "";
    mapBox.appendChild(f);
  });

  /* ---------- Time list: 24-hour start times, asked from the (mock) server ---------- */
  var hintDefault = hint.textContent;
  var pickText = timeEl.options[0].textContent;
  var SLOT = CFG.slotMinutes || 15;
  var tick = 0;
  var today = new Date();
  dateEl.min = today.getFullYear() + "-" + pad(today.getMonth() + 1) + "-" + pad(today.getDate());

  function visitMinutes() {
    if (plan) return plan.maxMinutes;
    var o = serviceEl.options[serviceEl.selectedIndex];
    if (o && o.dataset.max) return +o.dataset.max;
    return 60;
  }
  function fillTimes(slots, keep) {
    timeEl.textContent = "";
    var first = document.createElement("option");
    first.value = ""; first.textContent = pickText;
    timeEl.appendChild(first);
    slots.forEach(function (s) {
      var o = document.createElement("option");
      o.value = o.textContent = s;
      timeEl.appendChild(o);
    });
    timeEl.value = keep;   /* keeps the chosen time if it is still available */
  }
  function updateTimes() {
    var keep = timeEl.value, dur = visitMinutes(), token = ++tick;
    var opt = serviceEl.options[serviceEl.selectedIndex];
    var known = !!plan || !!(opt && opt.dataset.max);   /* a service (or plan) is chosen, so the visit length is known */
    if (!dateEl.value) {
      /* No date yet: show the usual weekday times so the list is never empty or greyed out. */
      var h = API.hours.weekday, slots = [];
      for (var m = toMinutes(h[0]); m + dur <= toMinutes(h[1]); m += SLOT) slots.push(label(m));
      fillTimes(slots, keep);
      hint.textContent = known ? T.hintNoDate.replace("{d}", fmtMin(dur)) : hintDefault;
      return;
    }
    hint.textContent = T.checking;
    API.availability(dateEl.value, dur).then(function (res) {
      if (token !== tick) return;   /* a newer request replaced this one */
      fillTimes(res.slots, keep);
      if (!res.slots.length) { hint.textContent = T.noSlots; return; }
      var all = Math.floor((toMinutes(res.close) - toMinutes(res.open) - dur) / SLOT) + 1;
      hint.textContent = T.hint.replace("{a}", res.slots[0]).replace("{b}", res.slots[res.slots.length - 1])
        .replace("{d}", fmtMin(dur)).replace("{c}", res.close) + (res.slots.length < all ? " " + T.someTaken : "");
    }, function () { if (token === tick) hint.textContent = T.availError; });
  }
  updateTimes();
  dateEl.addEventListener("input", updateTimes);
  dateEl.addEventListener("change", updateTimes);
  serviceEl.addEventListener("change", function () {
    if (plan && serviceEl.value !== plan.opt) clearPlan();
    updateTimes();
  });

  /* ---------- Plan your visit (estimator) ---------- */
  var planData = JSON.parse($("planData").textContent);
  var svcById = {}, addById = {};
  planData.services.forEach(function (s) { svcById[s.id] = s; });
  planData.addons.forEach(function (a) { addById[a.id] = a; });
  var svcRadios = document.querySelectorAll('input[name="svc"]');
  var lenRadios = document.querySelectorAll('input[name="len"]');
  var addLabels = document.querySelectorAll("#planAddons .opt");
  var planLength = $("planLength"), planAddons = $("planAddons");
  var planAdd = $("planAdd");

  function priceText(a, b) { return a === b ? a + " €" : a + " – " + b + " €"; }

  function computePlan() {
    var sel = document.querySelector('input[name="svc"]:checked');
    if (!sel) return null;
    var s = svcById[sel.value];
    var pmin = s.pmin, pmax = s.pmax, mmin = s.mmin, mmax = s.mmax, opt = s.opt, label = s.label;
    if (s.lengths) {
      var l = document.querySelector('input[name="len"]:checked');
      var len = s.lengths.filter(function (x) { return x.id === (l && l.value); })[0] || s.lengths[0];
      pmin = pmax = len.price; mmin = mmax = len.minutes; opt = len.opt; label = s.label + ", " + len.label.toLowerCase();
    }
    var adds = [], onRequest = false;
    document.querySelectorAll('input[name="addon"]:checked').forEach(function (b) {
      if (b.closest("[hidden]") || b.closest(".opt").hidden) return;
      var a = addById[b.value];
      adds.push(a.label);
      if (a.price === null) onRequest = true; else { pmin += a.price; pmax += a.price; }
      mmin += a.minutes; mmax += a.minutes;
    });
    return { opt: opt, label: label, adds: adds, pmin: pmin, pmax: pmax, mmin: mmin, mmax: mmax, onRequest: onRequest };
  }

  /* Show a new estimate with a small fade so the change is noticeable. */
  function setResult(node, text) {
    if (node.textContent === text) return;
    node.textContent = text;
    node.classList.remove("bump"); void node.offsetWidth; node.classList.add("bump");
  }

  function renderPlan() {
    var sel = document.querySelector('input[name="svc"]:checked');
    var s = sel ? svcById[sel.value] : null;
    planLength.hidden = !(s && s.lengths);
    planAddons.hidden = !(s && s.addons.length);
    addLabels.forEach(function (lab) {
      var ok = !!(s && lab.dataset.for.split(" ").indexOf(s.id) !== -1);
      lab.hidden = !ok;
      if (!ok) lab.querySelector("input").checked = false;
    });
    var c = computePlan();
    $("planEmpty").hidden = !!c;
    $("planOut").hidden = !c;
    $("planNote").hidden = !(c && c.onRequest);
    planAdd.disabled = !c;
    if (!c) return;
    setResult($("planPrice"), priceText(c.pmin, c.pmax));
    setResult($("planTime"), fmtRange(c.mmin, c.mmax, fmtMin));
    $("planNote").textContent = planData.names.req;
  }
  svcRadios.forEach(function (r) { r.addEventListener("change", renderPlan); });
  lenRadios.forEach(function (r) { r.addEventListener("change", renderPlan); });
  document.querySelectorAll('input[name="addon"]').forEach(function (r) { r.addEventListener("change", renderPlan); });
  renderPlan();

  var planChip = $("planChip");
  function clearPlan() { plan = null; planChip.hidden = true; updateTimes(); }
  planAdd.addEventListener("click", function () {
    var c = computePlan();
    if (!c) return;
    var summary = c.label + (c.adds.length ? " + " + c.adds.join(" + ") : "") + ". " +
      T.about + " " + fmtRange(c.mmin, c.mmax, fmtMin) + ", " + priceText(c.pmin, c.pmax);
    plan = { opt: c.opt, summary: summary, maxMinutes: c.mmax, minMinutes: c.mmin, minPrice: c.pmin, maxPrice: c.pmax, extras: c.adds, priceOnRequest: c.onRequest };
    serviceEl.value = c.opt;
    $("planChipText").textContent = summary;
    planChip.hidden = false;
    showForm();
    updateTimes();
    scrollToEl(form);
    announce(T.planAdded);
  });
  $("planRemove").addEventListener("click", clearPlan);

  /* ---------- Pick-up or delivery: the address is needed only for delivery ---------- */
  var addrField = $("addrField"), addrInput = $("f-addr");
  function syncFulfil() {
    var del = form.elements.fulfil.value === "delivery";
    addrField.hidden = !del;
    addrInput.required = del;
  }
  document.querySelectorAll('input[name="fulfil"]').forEach(function (r) { r.addEventListener("change", syncFulfil); });

  /* ---------- Sending the request (talks to VerbenaAPI: a mock server now, a real backend later) ---------- */
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
    var d = new FormData(form);
    return {
      name: String(d.get("name")).trim(), phone: String(d.get("phone")).trim(), service: d.get("service"),
      plan: plan ? { summary: plan.summary, minPrice: plan.minPrice, maxPrice: plan.maxPrice, minMinutes: plan.minMinutes, maxMinutes: plan.maxMinutes, extras: plan.extras, priceOnRequest: plan.priceOnRequest } : null,
      fulfil: d.get("fulfil"), address: String(d.get("addr") || "").trim(), card: String(d.get("card") || "").trim(),
      date: d.get("date"), time: d.get("time"), durationMinutes: visitMinutes(),
      look: look ? { alt: look.alt, url: look.url } : null,
      message: String(d.get("msg") || "").trim(), lang: lang
    };
  }
  function showError(er) {
    var msg = er && er.code === "slot_taken" ? T.errTaken : er && er.code === "invalid" ? T.errInvalid : T.errGeneric;
    formError.textContent = msg;
    formError.hidden = false;
    if (er && er.code === "slot_taken") { timeEl.value = ""; updateTimes(); }
  }
  function showForm() { formDone.hidden = true; form.hidden = false; }

  function showDone(rec, p) {
    var L = T.lines;
    formDone.textContent = "";
    var h = el("h3", "", T.doneH);
    var ref = el("p", "done-ref");
    ref.appendChild(el("span", "", T.doneRef));
    ref.appendChild(el("strong", "", rec.id));
    var st = el("p", "done-status");
    st.appendChild(el("span", "", T.doneStatus + ": "));
    st.appendChild(el("span", "pill", T.statusPending));
    var dl = el("dl", "done-list");
    function row(k, v) { if (!v) return; dl.appendChild(el("dt", "", k)); dl.appendChild(el("dd", "", v)); }
    row(L.name, p.name); row(L.phone, p.phone); row(L.service, p.service);
    if (p.plan) row(L.plan, p.plan.summary);
    row(L.fulfil, p.fulfil === "delivery" ? T.delivery : T.pickup); row(L.addr, p.address); row(L.card, p.card);
    row(L.date, longDate(p.date)); row(L.time, p.time);
    if (p.look) row(L.look, p.look.alt);
    row(L.msg, p.message);
    var next = el("p", "", T.doneNext);
    var actions = el("div", "done-actions");
    var again = el("button", "btn btn-line", T.again);
    again.type = "button";
    again.addEventListener("click", resetForm);
    actions.appendChild(again);
    formDone.appendChild(h); formDone.appendChild(ref); formDone.appendChild(st); formDone.appendChild(dl); formDone.appendChild(next);
    if (API.mode === "demo") {
      formDone.appendChild(el("p", "demo-note", T.doneDemo));
      var link = el("a", "btn btn-main", T.adminLink);
      var adm = document.querySelector('.foot a[href*="admin"]');
      link.href = adm ? adm.href : "admin.html";
      actions.insertBefore(link, again);
    }
    formDone.appendChild(actions);
    form.hidden = true;
    formDone.hidden = false;
    scrollToEl(formDone);
    formDone.focus({ preventScroll: true });
  }
  function resetForm() {
    form.reset();
    syncFulfil();
    clearLook();
    plan = null; planChip.hidden = true;
    formError.hidden = true;
    showForm();
    updateTimes();
    $("f-name").focus();
  }

  syncFulfil();
  updateCutoff();
  setInterval(updateCutoff, 30000);

  form.addEventListener("submit", function (e) {
    e.preventDefault();
    if (busy) return;
    formError.hidden = true;
    var payload = buildPayload();
    setBusy(true);
    API.createRequest(payload).then(function (rec) {
      setBusy(false);
      showDone(rec, payload);
    }, function (er) {
      setBusy(false);
      showError(er);
    });
  });
})();
