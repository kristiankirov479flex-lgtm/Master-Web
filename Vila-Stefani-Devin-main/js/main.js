(function () {
  "use strict";

  var DATA = window.VILA;
  var I18N = window.VILA_I18N;
  var $ = function (id) { return document.getElementById(id); };

  var lang = "bg";
  var filter = "all";
  var expanded = false;

  /* ---------- Горна лента и меню ---------- */
  var bar = $("bar"), menu = $("menu"), burger = $("burger");
  function onScroll() { bar.classList.toggle("solid", window.scrollY > 40); }
  onScroll();
  addEventListener("scroll", onScroll, { passive: true });
  burger.addEventListener("click", function () {
    var open = menu.classList.toggle("open");
    burger.setAttribute("aria-expanded", open);
  });
  menu.addEventListener("click", function (e) {
    if (e.target.tagName === "A") {
      menu.classList.remove("open");
      burger.setAttribute("aria-expanded", "false");
    }
  });
  $("y").textContent = new Date().getFullYear();

  /* ---------- Снимки: показват се само ако файлът съществува ---------- */
  function imgOk(img) { img.parentNode.classList.add("has-img"); }
  function imgFail(img) {
    var holder = img.closest(".poi-img");
    (holder || img).remove();
  }
  document.addEventListener("error", function (e) {
    if (e.target.tagName === "IMG" && e.target.id !== "lbImg") imgFail(e.target);
  }, true);
  document.addEventListener("load", function (e) {
    if (e.target.tagName === "IMG" && e.target.id !== "lbImg") imgOk(e.target);
  }, true);
  function checkImages(root) {
    root.querySelectorAll("img").forEach(function (img) {
      if (img.id === "lbImg" || !img.complete) return;
      if (img.naturalWidth > 0) imgOk(img); else imgFail(img);
    });
  }
  checkImages(document);

  /* Голяма снимка в началото, ако има images/hero.jpg */
  var probe = new Image();
  probe.onload = function () {
    var hero = $("hero");
    hero.style.setProperty("--hero-photo", 'url("images/hero.jpg")');
    hero.classList.add("has-photo");
  };
  probe.src = "images/hero.jpg";

  /* ---------- Език ---------- */
  var nodes = document.querySelectorAll("[data-i18n], [data-i18n-attr]");
  nodes.forEach(function (el) {
    if (el.dataset.i18n) el._bg = el.textContent;
    if (el.dataset.i18nAttr) {
      el._bgAttr = {};
      el.dataset.i18nAttr.split(";").forEach(function (pair) {
        var attr = pair.split(":")[0];
        el._bgAttr[attr] = el.getAttribute(attr);
      });
    }
  });
  var metaDesc = $("meta-desc");
  var BG = { title: document.title, desc: metaDesc.content };
  var langBtn = $("lang");

  function applyStatic() {
    var en = lang === "en";
    document.documentElement.lang = lang;
    nodes.forEach(function (el) {
      if (el.dataset.i18n) el.textContent = en ? I18N.en[el.dataset.i18n] : el._bg;
      if (el.dataset.i18nAttr) {
        el.dataset.i18nAttr.split(";").forEach(function (pair) {
          var p = pair.split(":");
          el.setAttribute(p[0], en ? I18N.en[p[1]] : el._bgAttr[p[0]]);
        });
      }
    });
    document.title = en ? I18N.en.title : BG.title;
    metaDesc.content = en ? I18N.en.desc : BG.desc;
    /* Бутонът показва езика, на който ще превключите. */
    langBtn.textContent = en ? "БГ" : "EN";
    langBtn.lang = en ? "bg" : "en";
    langBtn.setAttribute("aria-label", en ? "Превключи на български" : "Switch to English");
    var mf = $("mapWrap").querySelector("iframe");
    if (mf) mf.title = en ? I18N.en["c.maptitle"] : $("mapWrap").dataset.title;
  }

  function setLang(next) {
    lang = next;
    applyStatic();
    renderPlaces();
    renderReviews();
    try { localStorage.setItem("lang", lang); } catch (e) {}
  }

  langBtn.addEventListener("click", function () { setLang(lang === "bg" ? "en" : "bg"); });

  /* ---------- Наоколо ---------- */
  function esc(s) {
    return String(s).replace(/[&<>"]/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c];
    });
  }
  function fmt(tpl, vars) {
    return tpl.replace(/\{(\w+)\}/g, function (_, k) { return vars[k]; });
  }
  function routeUrl(dest) {
    return "https://www.google.com/maps/dir/?api=1&origin=" + DATA.origin +
      "&destination=" + encodeURIComponent(dest) + "&travelmode=driving";
  }

  function renderPlaces() {
    var ui = I18N.ui[lang];
    var list = DATA.places.filter(function (p) { return filter === "all" || p.cat === filter; });
    var hidden = list.filter(function (p) { return !p.featured; }).length;
    var shown = expanded ? list : list.filter(function (p) { return p.featured; });

    $("pois").innerHTML = shown.map(function (p) {
      var t = p[lang];
      var dist = p.km ? fmt(ui.km, { n: p.km }) : p.kmText[lang];
      var route = p.dest
        ? '<a href="' + esc(routeUrl(p.dest)) + '" target="_blank" rel="noopener" aria-label="' +
          esc(fmt(ui.route_aria, { name: t.name })) + '">' + esc(ui.route) + "</a>"
        : "";
      return '<article class="poi">' +
        '<div class="poi-img"><img src="images/places/' + p.id + '.jpg" alt="" loading="lazy"></div>' +
        '<div class="poi-body"><h4>' + esc(t.name) + '</h4><span class="km">' + esc(dist) + "</span>" +
        "<p>" + esc(t.text) + "</p>" +
        '<div class="lk"><a href="' + esc(p.info) + '" target="_blank" rel="noopener">' + esc(ui.info) + "</a>" + route + "</div>" +
        "</div></article>";
    }).join("");
    checkImages($("pois"));
    $("poiStatus").textContent = fmt(ui.shown, { n: shown.length });

    var more = $("more");
    more.hidden = hidden === 0;
    $("moreBtn").textContent = expanded ? ui.less : fmt(ui.more, { n: list.length });
  }

  document.querySelectorAll(".chip").forEach(function (chip) {
    chip.addEventListener("click", function () {
      filter = chip.dataset.filter;
      document.querySelectorAll(".chip").forEach(function (c) {
        c.setAttribute("aria-pressed", c === chip ? "true" : "false");
      });
      renderPlaces();
    });
  });
  $("moreBtn").addEventListener("click", function () { expanded = !expanded; renderPlaces(); });

  /* ---------- Отзиви ---------- */
  function renderReviews() {
    var ui = I18N.ui[lang];
    $("revs").innerHTML = DATA.reviews.map(function (r, i) {
      var long = r[lang].length > 260;
      return '<figure class="review' + (long ? " clamp" : "") + '">' +
        '<div class="stars" role="img" aria-label="' + (lang === "bg" ? "5 от 5" : I18N.en["v.stars"]) + '">★★★★★</div>' +
        "<blockquote>" + esc(r[lang]) + "</blockquote>" +
        (long ? '<button class="rmore" type="button" aria-expanded="false">' + esc(ui.rmore) + "</button>" : "") +
        "<footer><b>" + esc(r.name[lang]) + "</b> · Google Maps</footer></figure>";
    }).join("");
    var score = DATA.rating.score.toFixed(1);
    $("ratingNum").textContent = lang === "bg" ? score.replace(".", ",") : score;
    $("ratingCount").textContent = fmt(ui.rating, { n: DATA.rating.count });
    var note = $("revnote");
    note.textContent = ui.noteTr;
    note.hidden = !ui.noteTr;
  }
  $("revs").addEventListener("click", function (e) {
    var btn = e.target.closest(".rmore");
    if (!btn) return;
    var card = btn.closest(".review");
    var open = card.classList.toggle("clamp") === false;
    btn.setAttribute("aria-expanded", open);
    btn.textContent = I18N.ui[lang][open ? "rless" : "rmore"];
  });

  /* ---------- Галерия (увеличаване) ---------- */
  var box = $("lightbox"), lbImg = $("lbImg"), lbCap = $("lbCap");
  var current = 0;
  function items() { return Array.prototype.slice.call(document.querySelectorAll("#gal .ph.has-img")); }
  function show(i) {
    var list = items();
    if (!list.length) return;
    current = (i + list.length) % list.length;
    var fig = list[current];
    lbImg.src = fig.querySelector("img").currentSrc || fig.querySelector("img").src;
    lbImg.alt = fig.querySelector("span").textContent;
    lbCap.textContent = fig.querySelector("span").textContent;
  }
  $("gal").addEventListener("click", function (e) {
    var fig = e.target.closest(".ph.has-img");
    if (!fig) return;
    show(items().indexOf(fig));
    box.showModal();
  });
  $("gal").addEventListener("keydown", function (e) {
    var fig = e.target.closest(".ph.has-img");
    if (fig && (e.key === "Enter" || e.key === " ")) { e.preventDefault(); fig.click(); }
  });
  /* Снимките в галерията са достъпни и с клавиатура */
  new MutationObserver(function () {
    items().forEach(function (f) { f.tabIndex = 0; f.setAttribute("role", "button"); });
  }).observe($("gal"), { attributes: true, subtree: true, attributeFilter: ["class"] });
  $("lbClose").addEventListener("click", function () { box.close(); });
  $("lbPrev").addEventListener("click", function () { show(current - 1); });
  $("lbNext").addEventListener("click", function () { show(current + 1); });
  box.addEventListener("click", function (e) { if (e.target === box || e.target.className === "lightbox-inner") box.close(); });
  box.addEventListener("keydown", function (e) {
    if (e.key === "ArrowLeft") show(current - 1);
    if (e.key === "ArrowRight") show(current + 1);
  });

  /* ---------- Появяване при превъртане ---------- */
  if (document.documentElement.classList.contains("js-reveal")) {
    var groups = [
      ["#nachalo h2", ""], ["#nachalo .lead", ""], ["#nachalo .amen a", ""],
      ["#staya .txt > *", ""], ["#staya .tiles .ph", "rv-r"],
      ["#kuhnya .txt > *", ""], ["#kuhnya .tiles .ph", "rv-l"]
    ];
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (!en.isIntersecting) return;
        io.unobserve(en.target);
        en.target.classList.add("in");
        /* След края на анимацията се връщат нормалните стилове (напр. ефектите при посочване). */
        setTimeout(function () { en.target.classList.remove("rv", "rv-l", "rv-r", "in"); en.target.style.removeProperty("--d"); }, 1200);
      });
    }, { threshold: 0.15, rootMargin: "0px 0px -6% 0px" });
    groups.forEach(function (g) {
      document.querySelectorAll(g[0]).forEach(function (el, i) {
        el.classList.add("rv");
        if (g[1]) el.classList.add(g[1]);
        el.style.setProperty("--d", (i * 0.08).toFixed(2) + "s");
        io.observe(el);
      });
    });
  }

  /* ---------- Поверителност: външната карта се зарежда само със съгласие ---------- */
  var consentBox = $("consent"), mapWrap = $("mapWrap");
  function getConsent() { try { return localStorage.getItem("consent"); } catch (e) { return null; } }
  function setConsent(v) { try { localStorage.setItem("consent", v); } catch (e) {} }
  function loadMap() {
    if (mapWrap.querySelector("iframe")) return;
    var f = document.createElement("iframe");
    f.className = "map";
    f.src = mapWrap.dataset.src;
    f.title = lang === "en" ? I18N.en["c.maptitle"] : mapWrap.dataset.title;
    f.loading = "lazy";
    mapWrap.textContent = "";
    mapWrap.appendChild(f);
  }
  function showBanner() { consentBox.hidden = false; $("cbAccept").focus({ preventScroll: true }); }
  $("cbAccept").addEventListener("click", function () { setConsent("granted"); consentBox.hidden = true; loadMap(); });
  $("cbDecline").addEventListener("click", function () { setConsent("denied"); consentBox.hidden = true; });
  $("privacyBtn").addEventListener("click", showBanner);
  /* Бутонът на мястото на картата зарежда само нея, без да запазва избор. */
  $("mapLoad").addEventListener("click", loadMap);
  var savedConsent = getConsent();
  if (savedConsent === "granted") loadMap();
  /* Не показваме банера, когато сайтът е във вградена преглед-рамка (напр. в портфолиото). */
  else if (savedConsent === null && window.self === window.top) consentBox.hidden = false;

  /* ---------- Старт ---------- */
  var saved = null;
  try { saved = localStorage.getItem("lang"); } catch (e) {}
  var start = saved || ((navigator.language || "").toLowerCase().indexOf("bg") === 0 ? "bg" : "en");
  /* Първоначално рисуване на българската версия, после превключване при нужда. */
  applyStatic();
  renderPlaces();
  renderReviews();
  if (start !== "bg") setLang(start);
})();
