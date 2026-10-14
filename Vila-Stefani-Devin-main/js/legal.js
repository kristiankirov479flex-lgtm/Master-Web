/* Езиково превключване за страницата „Поверителност“. Ползва същия избор като основния сайт. */
(function () {
  "use strict";
  var TEXT = {
    bg: { title: "Политика за поверителност – Вила Стефани", skip: "Към съдържанието", back: "← Към сайта", name: "Вила Стефани", btn: "EN", btnLang: "en", label: "Switch to English" },
    en: { title: "Privacy notice – Vila Stefani", skip: "Skip to content", back: "← Back to the site", name: "Vila Stefani", btn: "БГ", btnLang: "bg", label: "Превключи на български" }
  };
  var btn = document.getElementById("lang");

  function setLang(lang) {
    var t = TEXT[lang];
    document.documentElement.lang = lang;
    document.querySelectorAll("article[data-lang]").forEach(function (a) { a.hidden = a.dataset.lang !== lang; });
    document.title = t.title;
    document.getElementById("skip").textContent = t.skip;
    document.getElementById("back").textContent = t.back;
    document.getElementById("logo").textContent = t.name;
    document.getElementById("fname").textContent = t.name;
    btn.textContent = t.btn;
    btn.lang = t.btnLang;
    btn.setAttribute("aria-label", t.label);
    try { localStorage.setItem("lang", lang); } catch (e) {}
  }

  btn.addEventListener("click", function () { setLang(document.documentElement.lang === "bg" ? "en" : "bg"); });
  document.getElementById("y").textContent = new Date().getFullYear();

  var saved = null;
  try { saved = localStorage.getItem("lang"); } catch (e) {}
  var start = saved || ((navigator.language || "").toLowerCase().indexOf("bg") === 0 ? "bg" : "en");
  if (start === "en") setLang("en");
})();
