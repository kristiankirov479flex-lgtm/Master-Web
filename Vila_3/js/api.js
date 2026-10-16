/*
 * The Stone Cellar – enquiry API (mock server in the browser).
 *
 * The page talks to this object only. In "demo" mode it behaves like a small server: it checks which rooms are free for the
 * dates, validates enquiries, assigns reference numbers and keeps a list in the visitor's own browser (localStorage).
 * In "live" mode the same calls become real HTTP requests to a backend (see docs/API.md), so the page does not change.
 *
 * Settings come from js/config.js. Dates are "YYYY-MM-DD"; a stay occupies the nights from check-in up to (not including) check-out.
 */
(function () {
  "use strict";

  var CFG = window.CELLAR_CONFIG || {};
  var MODE = CFG.mode === "live" ? "live" : "demo";
  var BASE = (CFG.apiBase || "/api").replace(/\/$/, "");
  var ROOMS = CFG.rooms || [];
  var MAXN = CFG.maxNights || 30;
  var LATENCY = CFG.latency || [600, 1100];

  var KEY = "cellar.stays", SEQ = "cellar.seq";
  var memory = { list: [], seq: 0 };     /* used if the browser blocks localStorage */

  function pad(n) { return (n < 10 ? "0" : "") + n; }
  function parseDate(v) { var p = String(v).split("-"); return new Date(+p[0], +p[1] - 1, +p[2]); }
  function nightsBetween(a, b) { return Math.round((parseDate(b) - parseDate(a)) / 864e5); }
  function wait(ms) { return new Promise(function (res) { setTimeout(res, ms); }); }
  function delay(range) { return wait(range[0] + Math.random() * (range[1] - range[0])); }
  function fail(status, code, message) { var e = new Error(message || code); e.status = status; e.code = code; return e; }
  function roomById(id) { return ROOMS.filter(function (r) { return r.id === id; })[0]; }
  function today() { var t = new Date(); return new Date(t.getFullYear(), t.getMonth(), t.getDate()); }

  function load() { try { return JSON.parse(localStorage.getItem(KEY) || "[]"); } catch (e) { return memory.list; } }
  function save(list) { memory.list = list; try { localStorage.setItem(KEY, JSON.stringify(list)); } catch (e) {} }
  function nextRef() {
    var n;
    try { n = (+localStorage.getItem(SEQ) || 0) + 1; localStorage.setItem(SEQ, n); } catch (e) { n = ++memory.seq; }
    return "SC-" + ("000" + n).slice(-4);
  }

  /* ---------- business rules (a real backend owns these) ---------- */
  /* Dates must be real, in the future and not too long. Returns an error message or "". */
  function checkDates(checkin, checkout) {
    if (!checkin || !checkout) return "Missing dates";
    var a = parseDate(checkin), b = parseDate(checkout);
    if (isNaN(a) || isNaN(b)) return "Bad date";
    if (a < today()) return "The arrival date is in the past";
    var n = nightsBetween(checkin, checkout);
    if (n < 1) return "Departure must be after arrival";
    if (n > MAXN) return "At most " + MAXN + " nights";
    return "";
  }
  /* A room is taken when a pending or confirmed stay overlaps the nights. Declined stays do not block. */
  function isTaken(roomId, checkin, checkout, list) {
    return list.some(function (s) { return s.room === roomId && s.status !== "declined" && s.checkin < checkout && checkin < s.checkout; });
  }
  function availability(checkin, checkout, guests) {
    var err = checkDates(checkin, checkout);
    if (err) throw fail(422, "invalid", err);
    var list = load(), nights = nightsBetween(checkin, checkout);
    return {
      checkin: checkin, checkout: checkout, nights: nights, guests: guests || 1,
      rooms: ROOMS.map(function (r) {
        var small = (guests || 1) > r.guests, taken = isTaken(r.id, checkin, checkout, list);
        return { id: r.id, free: !small && !taken, reason: small ? "size" : taken ? "taken" : "", price: r.price, total: r.price * nights };
      })
    };
  }

  /* For each night from "from" up to (not including) "to": how many places are free. Used to colour the calendar. */
  function occupancy(from, to) {
    var list = load().filter(function (s) { return s.status !== "declined"; }), days = {}, d = parseDate(from), end = parseDate(to);
    while (d < end) {
      var k = d.getFullYear() + "-" + pad(d.getMonth() + 1) + "-" + pad(d.getDate()), nxt = new Date(d.getFullYear(), d.getMonth(), d.getDate() + 1);
      var nk = nxt.getFullYear() + "-" + pad(nxt.getMonth() + 1) + "-" + pad(nxt.getDate());
      days[k] = ROOMS.filter(function (r) { return !isTaken(r.id, k, nk, list); }).length;
      d = nxt;
    }
    return { from: from, to: to, places: ROOMS.length, free: days };
  }

  /* ---------- demo implementation ---------- */
  var demo = {
    occupancy: function (from, to) { return wait(100 + Math.random() * 120).then(function () { return occupancy(from, to); }); },
    availability: function (checkin, checkout, guests) {
      return wait(120 + Math.random() * 180).then(function () { return availability(checkin, checkout, guests); });
    },
    create: function (p) {
      return delay(LATENCY).then(function () {
        var missing = ["name", "phone", "room", "checkin", "checkout"].filter(function (k) { return !p[k]; });
        if (missing.length) throw fail(422, "invalid", "Missing: " + missing.join(", "));
        var room = roomById(p.room);
        if (!room) throw fail(422, "invalid", "Unknown room");
        var err = checkDates(p.checkin, p.checkout);
        if (err) throw fail(422, "invalid", err);
        var guests = +p.guests || 1;
        if (guests > room.guests) throw fail(422, "invalid", "Too many guests for this room");
        var list = load();
        if (isTaken(p.room, p.checkin, p.checkout, list)) throw fail(409, "room_taken", "That room is no longer free for these dates");
        var nights = nightsBetween(p.checkin, p.checkout);
        var rec = {
          id: nextRef(), createdAt: new Date().toISOString(), status: "pending",
          name: p.name, phone: p.phone, email: p.email || "", room: p.room, checkin: p.checkin, checkout: p.checkout, nights: nights,
          guests: guests, total: room.price * nights, message: p.message || "", lang: p.lang || ""
        };
        list.push(rec); save(list);
        return { id: rec.id, status: rec.status, createdAt: rec.createdAt };
      });
    },
    list: function () {
      return wait(150).then(function () { return load().sort(function (a, b) { return a.checkin.localeCompare(b.checkin); }); });
    },
    setStatus: function (id, status) {
      return wait(150).then(function () {
        if (["pending", "confirmed", "declined"].indexOf(status) === -1) throw fail(422, "invalid", "Unknown status");
        var list = load(), r = list.filter(function (x) { return x.id === id; })[0];
        if (!r) throw fail(404, "not_found", "No such enquiry");
        r.status = status; save(list); return r;
      });
    },
    remove: function (id) { return wait(150).then(function () { save(load().filter(function (x) { return x.id !== id; })); return {}; }); },
    reset: function () { return wait(150).then(function () { save([]); try { localStorage.removeItem(SEQ); } catch (e) {} memory.seq = 0; return {}; }); },
    seed: function (samples) {
      return wait(150).then(function () {
        var list = load();
        samples.forEach(function (s) {
          var room = roomById(s.room) || ROOMS[0], nights = nightsBetween(s.checkin, s.checkout);
          list.push({ id: nextRef(), createdAt: new Date().toISOString(), status: s.status || "pending", name: s.name, phone: s.phone, email: s.email || "",
            room: room.id, checkin: s.checkin, checkout: s.checkout, nights: nights, guests: s.guests || 2, total: room.price * nights, message: s.message || "", lang: "" });
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
        if (!res.ok) { var er = data && data.error ? data.error : {}; throw fail(res.status, er.code || "error", er.message || "Request failed"); }
        return data;
      });
    });
  }
  var live = {
    occupancy: function (from, to) { return http("GET", "/occupancy?from=" + encodeURIComponent(from) + "&to=" + encodeURIComponent(to)); },
    availability: function (checkin, checkout, guests) { return http("GET", "/availability?checkin=" + encodeURIComponent(checkin) + "&checkout=" + encodeURIComponent(checkout) + "&guests=" + encodeURIComponent(guests || 1)); },
    create: function (p) { return http("POST", "/enquiries", p); },
    list: function () { return http("GET", "/enquiries"); },
    setStatus: function (id, status) { return http("PATCH", "/enquiries/" + encodeURIComponent(id), { status: status }); },
    remove: function (id) { return http("DELETE", "/enquiries/" + encodeURIComponent(id)); },
    reset: function () { return Promise.reject(fail(405, "not_allowed", "Not available on a live system")); },
    seed: function () { return Promise.reject(fail(405, "not_allowed", "Not available on a live system")); }
  };

  var impl = MODE === "live" ? live : demo;
  window.CellarAPI = {
    mode: MODE, rooms: ROOMS, maxNights: MAXN,
    occupancy: impl.occupancy, availability: impl.availability, createEnquiry: impl.create, listEnquiries: impl.list,
    setStatus: impl.setStatus, removeEnquiry: impl.remove, resetDemo: impl.reset, seedDemo: impl.seed
  };
})();
