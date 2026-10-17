/*
 * Maslina – request API (mock server in the browser).
 *
 * The page talks to this object only. In "demo" mode it behaves like a small server: it validates requests,
 * checks availability, assigns reference numbers and keeps a list in the visitor's own browser (localStorage).
 * In "live" mode the same calls become real HTTP requests to a backend (see docs/API.md), so the page does not change.
 *
 * Settings come from js/config.js.
 */
(function () {
  "use strict";

  var CFG = window.MASLINA_CONFIG || {};
  var MODE = CFG.mode === "live" ? "live" : "demo";
  var BASE = (CFG.apiBase || "/api").replace(/\/$/, "");
  var HOURS = CFG.hours || { weekday: ["09:00", "19:00"], weekend: ["10:00", "18:00"] };
  var CAPACITY = CFG.capacity || 1;      /* how many visits can run at the same time */
  var SLOT = CFG.slotMinutes || 15;      /* gap between start times */
  var LATENCY = CFG.latency || [600, 1100];
  var LEAD = CFG.leadMinutes || 0;       /* a same-day order needs this much notice */

  var KEY = "maslina.requests", SEQ = "maslina.seq";
  var memory = { list: [], seq: 0 };     /* used if the browser blocks localStorage */

  /* ---------- tiny helpers ---------- */
  function pad(n) { return (n < 10 ? "0" : "") + n; }
  function toMin(hhmm) { var p = hhmm.split(":"); return +p[0] * 60 + +p[1]; }
  function toHHMM(m) { return pad(Math.floor(m / 60)) + ":" + pad(m % 60); }
  function parseDate(v) { var p = v.split("-"); return new Date(+p[0], +p[1] - 1, +p[2]); }
  function wait(ms) { return new Promise(function (res) { setTimeout(res, ms); }); }
  function delay(range) { return wait(range[0] + Math.random() * (range[1] - range[0])); }
  function fail(status, code, message) { var e = new Error(message || code); e.status = status; e.code = code; return e; }

  /* ---------- the stored "database" ---------- */
  function load() {
    try { return JSON.parse(localStorage.getItem(KEY) || "[]"); } catch (e) { return memory.list; }
  }
  function save(list) {
    memory.list = list;
    try { localStorage.setItem(KEY, JSON.stringify(list)); } catch (e) {}
  }
  function nextRef() {
    var n;
    try { n = (+localStorage.getItem(SEQ) || 0) + 1; localStorage.setItem(SEQ, n); } catch (e) { n = ++memory.seq; }
    return "MS-" + ("000" + n).slice(-4);
  }

  /* ---------- business rules (a real backend owns these) ---------- */
  function hoursFor(date) {
    var d = parseDate(date).getDay();
    return d === 0 || d === 6 ? HOURS.weekend : HOURS.weekday;
  }
  function freeSlots(date, duration, ignoreId) {
    var h = hoursFor(date), open = toMin(h[0]), close = toMin(h[1]);
    var busy = load().filter(function (r) { return r.date === date && r.status !== "declined" && r.id !== ignoreId; });
    var slots = [];
    var now = new Date(), isToday = date === now.getFullYear() + "-" + pad(now.getMonth() + 1) + "-" + pad(now.getDate());
    var earliest = isToday ? now.getHours() * 60 + now.getMinutes() + LEAD : 0;   /* no times in the past, and some notice for same-day orders */
    for (var m = open; m + duration <= close; m += SLOT) {
      if (m < earliest) continue;
      var overlaps = busy.filter(function (r) { return m < r.start + r.duration && r.start < m + duration; }).length;
      if (overlaps < CAPACITY) slots.push(toHHMM(m));
    }
    return { date: date, open: h[0], close: h[1], duration: duration, slots: slots };
  }

  /* ---------- demo implementation ---------- */
  var demo = {
    availability: function (date, duration) {
      return wait(120 + Math.random() * 180).then(function () { return freeSlots(date, duration); });
    },
    create: function (p) {
      return delay(LATENCY).then(function () {
        var missing = ["name", "phone", "service", "date", "time"].filter(function (k) { return !p[k]; });
        if (missing.length) throw fail(422, "invalid", "Missing: " + missing.join(", "));
        var today = new Date(); today = new Date(today.getFullYear(), today.getMonth(), today.getDate());
        if (parseDate(p.date) < today) throw fail(422, "invalid", "The date is in the past");
        if (p.fulfil === "delivery" && !p.address) throw fail(422, "invalid", "Missing: address");
        var duration = +p.durationMinutes || 60;
        if (freeSlots(p.date, duration).slots.indexOf(p.time) === -1) throw fail(409, "slot_taken", "That time is no longer available");
        var rec = {
          id: nextRef(), createdAt: new Date().toISOString(), status: "pending",
          name: p.name, phone: p.phone, service: p.service, plan: p.plan || null,
          date: p.date, time: p.time, start: toMin(p.time), duration: duration,
          fulfil: p.fulfil === "delivery" ? "delivery" : "pickup", address: p.address || "", card: p.card || "",
          look: p.look || null, message: p.message || "", lang: p.lang || ""
        };
        var list = load(); list.push(rec); save(list);
        return { id: rec.id, status: rec.status, createdAt: rec.createdAt };
      });
    },
    list: function () {
      return wait(150).then(function () {
        return load().sort(function (a, b) { return (a.date + a.time).localeCompare(b.date + b.time); });
      });
    },
    setStatus: function (id, status) {
      return wait(150).then(function () {
        if (["pending", "confirmed", "declined"].indexOf(status) === -1) throw fail(422, "invalid", "Unknown status");
        var list = load(), r = list.filter(function (x) { return x.id === id; })[0];
        if (!r) throw fail(404, "not_found", "No such request");
        r.status = status; save(list); return r;
      });
    },
    remove: function (id) {
      return wait(150).then(function () { save(load().filter(function (x) { return x.id !== id; })); return {}; });
    },
    reset: function () {
      return wait(150).then(function () { save([]); try { localStorage.removeItem(SEQ); } catch (e) {} memory.seq = 0; return {}; });
    },
    seed: function (samples) {
      return wait(150).then(function () {
        var list = load();
        samples.forEach(function (s) {
          var r = {
            id: nextRef(), createdAt: new Date().toISOString(), status: s.status || "pending",
            name: s.name, phone: s.phone, service: s.service, plan: s.plan || null,
            date: s.date, time: s.time, start: toMin(s.time), duration: s.duration || 60,
            fulfil: s.fulfil || "pickup", address: s.address || "", card: s.card || "",
            look: null, message: s.message || "", lang: ""
          };
          list.push(r);
        });
        save(list); return {};
      });
    }
  };

  /* ---------- live implementation (needs a backend, see docs/API.md) ---------- */
  function http(method, path, body) {
    return fetch(BASE + path, {
      method: method,
      headers: body ? { "Content-Type": "application/json", "Accept": "application/json" } : { "Accept": "application/json" },
      body: body ? JSON.stringify(body) : undefined
    }).then(function (res) {
      return res.json().catch(function () { return {}; }).then(function (data) {
        if (!res.ok) {
          var er = data && data.error ? data.error : {};
          throw fail(res.status, er.code || "error", er.message || "Request failed");
        }
        return data;
      });
    });
  }
  var live = {
    availability: function (date, duration) { return http("GET", "/availability?date=" + encodeURIComponent(date) + "&duration=" + encodeURIComponent(duration)); },
    create: function (p) { return http("POST", "/requests", p); },
    list: function () { return http("GET", "/requests"); },
    setStatus: function (id, status) { return http("PATCH", "/requests/" + encodeURIComponent(id), { status: status }); },
    remove: function (id) { return http("DELETE", "/requests/" + encodeURIComponent(id)); },
    reset: function () { return Promise.reject(fail(405, "not_allowed", "Not available on a live system")); },
    seed: function () { return Promise.reject(fail(405, "not_allowed", "Not available on a live system")); }
  };

  var impl = MODE === "live" ? live : demo;
  window.MaslinaAPI = {
    mode: MODE,
    hours: HOURS,
    availability: impl.availability,
    createRequest: impl.create,
    listRequests: impl.list,
    setStatus: impl.setStatus,
    removeRequest: impl.remove,
    resetDemo: impl.reset,
    seedDemo: impl.seed
  };
})();
