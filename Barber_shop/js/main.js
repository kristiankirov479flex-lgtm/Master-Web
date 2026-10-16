(function () {
  "use strict";

  var html = document.documentElement;
  var lang = html.lang === "bg" ? "bg" : "en";
  var $ = function (id) { return document.getElementById(id); };
  var reduceMotion = window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches;
  var CFG = window.IRONWOOD_CONFIG || {};
  var API = window.IronwoodAPI;

  var T = {
    bg: {
      shown: "Показани снимки: {n}",
      mapTitle: "Карта на студиото",
      hint: "Начални часове от {a} до {b} за посещение от около {d}. Затваряме в {c}.",
      hintNoDate: "Показани са часове за делнични дни и посещение от около {d}. Избери дата, за да видиш конкретния ден.",
      checking: "Проверяваме свободните часове…",
      someTaken: "Някои часове вече са заети.",
      noSlots: "Няма начален час, който се събира този ден. Избери друга дата.",
      availError: "Не успяхме да проверим свободните часове. Опитай пак.",
      locale: "bg-BG",
      lines: { name: "Име", phone: "Телефон", service: "Услуга", plan: "Избор", date: "Удобна дата", time: "Удобен час", look: "Желана прическа", msg: "Съобщение" },
      hUnit: "ч", mUnit: "мин", about: "Около",
      lookAdded: "Снимката е добавена към заявката ти.",
      planAdded: "Изборът ти е добавен към заявката.",
      sending: "Изпращане…",
      demoLine: "Демо режим: заявките се пазят само в този браузър и нищо не се изпраща.",
      errTaken: "Съжаляваме, този час току-що беше зает. Избери друг час.",
      errInvalid: "Провери данните във формата и опитай пак.",
      errGeneric: "Нещо се обърка. Опитай пак или ни се обади.",
      doneH: "Заявката е получена", doneRef: "Номер на заявката", doneStatus: "Статус", statusPending: "Чака потвърждение",
      doneNext: "Ще се свържем с теб по телефона, за да потвърдим часа. Запази номера на заявката.",
      doneDemo: "Демо режим: нищо не беше изпратено. Заявката е записана само в този браузър.",
      again: "Направи нова заявка", adminLink: "Виж я в демо админ панела"
    },
    en: {
      shown: "Photos shown: {n}",
      mapTitle: "Map of the studio",
      hint: "Start times from {a} to {b} for a visit of about {d}. We close at {c}.",
      hintNoDate: "Weekday times for a visit of about {d} are shown. Pick a date to see that day.",
      checking: "Checking free times…",
      someTaken: "Some times are already taken.",
      noSlots: "No start time fits on this day. Please pick another date.",
      availError: "We could not check the free times. Please try again.",
      locale: "en-GB",
      lines: { name: "Name", phone: "Phone", service: "Service", plan: "Plan", date: "Preferred date", time: "Preferred time", look: "Cut I like", msg: "Message" },
      hUnit: "h", mUnit: "min", about: "About",
      lookAdded: "The photo was added to your request.",
      planAdded: "Your plan was added to the request.",
      sending: "Sending…",
      demoLine: "Demo mode: requests are kept in this browser only and nothing is sent.",
      errTaken: "Sorry, that time was just taken. Please choose another time.",
      errInvalid: "Please check the form and try again.",
      errGeneric: "Something went wrong. Please try again or call us.",
      doneH: "Request received", doneRef: "Reference", doneStatus: "Status", statusPending: "Waiting for confirmation",
      doneNext: "We will contact you by phone to confirm your time. Keep your reference handy.",
      doneDemo: "Demo mode: nothing was sent. The request is saved only in this browser.",
      again: "Make another request", adminLink: "See it in the demo back office"
    }
  }[lang];

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
    if (save) { try { localStorage.setItem("barberSkin", skin); } catch (e) {} }
  }
  skinBtns.forEach(function (b) { b.addEventListener("click", function () { setSkin(b.dataset.skin, true); }); });

  var startSkin = null;
  try { startSkin = new URLSearchParams(location.search).get("skin") || localStorage.getItem("barberSkin"); } catch (e) {}
  setSkin(startSkin || "brass", false);

  /* ---------- Header and menu ---------- */
  var top = $("top"), nav = $("nav"), burger = $("burger");
  function onScroll() { top.classList.toggle("scrolled", window.scrollY > 8); }
  onScroll();
  addEventListener("scroll", onScroll, { passive: true });
  burger.addEventListener("click", function () {
    var open = nav.classList.toggle("open");
    burger.setAttribute("aria-expanded", open);
  });
  nav.addEventListener("click", function (e) {
    if (e.target.closest("a") && nav.classList.contains("open")) {
      nav.classList.remove("open");
      burger.setAttribute("aria-expanded", "false");
    }
  });
  var y = $("year"); if (y) y.textContent = new Date().getFullYear();

  /* ---------- Scroll reveal: sections ease in as they come into view ---------- */
  if (html.classList.contains("js-reveal")) {
    var groups = [
      [".promise li", 0.1, false], [".sec-head > div", 0.08, false], [".menu-side > *", 0.08, false], [".menu-group", 0.1, false],
      [".plan-intro > *", 0.08, false], [".plan-card", 0, false], [".rev", 0.1, false], [".faq-grid h2", 0, false],
      [".faq-list details", 0.06, false], [".contact-info > *", 0.07, false], [".request-col", 0, false], [".gal-item", 0.08, true]
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
        n.style.setProperty("--d", ((g[2] ? i % 3 : i) * g[1]).toFixed(2) + "s");   /* gallery tiles cascade by column */
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

  /* ---------- Gallery: filter, viewer, "Request this cut" ---------- */
  var items = Array.prototype.slice.call(document.querySelectorAll(".gal-item"));
  var chips = document.querySelectorAll(".chip[data-filter]");
  var status = $("galStatus");
  chips.forEach(function (chip) {
    chip.addEventListener("click", function () {
      var f = chip.dataset.filter, n = 0;
      chips.forEach(function (c) { c.setAttribute("aria-pressed", c === chip ? "true" : "false"); });
      items.forEach(function (it) {
        var show = f === "all" || it.dataset.cat === f;
        it.hidden = !show;
        if (show) {
          it.classList.remove("rv", "in");   /* a tile shown by the filter should never stay hidden */
          it.style.setProperty("--d", (n % 3 * 0.05).toFixed(2) + "s");
          it.classList.remove("pop"); void it.offsetWidth; it.classList.add("pop");
          n++;
        }
      });
      status.textContent = T.shown.replace("{n}", n);
    });
  });

  var box = $("lightbox"), lbImg = $("lbImg"), current = 0;
  function visible() { return items.filter(function (it) { return !it.hidden; }); }
  function show(i) {
    var list = visible();
    if (!list.length) return;
    current = (i + list.length) % list.length;
    var it = list[current], img = it.querySelector("img");
    lbImg.src = it.dataset.full;
    lbImg.alt = img.alt;
    lbImg.classList.remove("swap"); void lbImg.offsetWidth; lbImg.classList.add("swap");
    $("lbRequest").hidden = it.dataset.cat === "shop";   /* photos of the shop itself are not a cut to request */
  }
  items.forEach(function (it) {
    it.addEventListener("click", function () { show(visible().indexOf(it)); box.showModal(); });
  });
  $("lbClose").addEventListener("click", function () { box.close(); });
  $("lbPrev").addEventListener("click", function () { show(current - 1); });
  $("lbNext").addEventListener("click", function () { show(current + 1); });
  box.addEventListener("click", function (e) { if (e.target === box || e.target.className === "lb-inner") box.close(); });
  box.addEventListener("keydown", function (e) {
    if (e.key === "ArrowLeft") show(current - 1);
    if (e.key === "ArrowRight") show(current + 1);
  });

  var lookChip = $("lookChip");
  function setLook(item) {
    var img = item.querySelector("img");
    look = { alt: img.alt, url: new URL(item.dataset.full, location.href).href };
    $("lookImg").src = img.currentSrc || img.src;
    $("lookText").textContent = img.alt;
    lookChip.hidden = false;
  }
  function clearLook() { look = null; lookChip.hidden = true; }
  $("lbRequest").addEventListener("click", function () {
    var it = visible()[current];
    if (!it) return;
    setLook(it);
    box.close();
    showForm();
    scrollToEl(form);
    announce(T.lookAdded);
    setTimeout(function () { $("f-name").focus({ preventScroll: true }); }, reduceMotion ? 0 : 500);
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

  /* ---------- Sending the request (talks to IronwoodAPI: a mock server now, a real backend later) ---------- */
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
    clearLook();
    plan = null; planChip.hidden = true;
    formError.hidden = true;
    showForm();
    updateTimes();
    $("f-name").focus();
  }

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
