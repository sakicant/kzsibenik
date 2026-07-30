/* Kršćanska zajednica Šibenik - site behaviour.
   Small and dependency-free: sticky header state, mobile menu, the "O nama"
   dropdown, scroll reveals, and the footer year. */
(function () {
  "use strict";

  var doc = document;

  /* ---------------------------------------------------------------- header */
  var header = doc.getElementById("siteHeader");
  if (header) {
    var onScroll = function () {
      header.classList.toggle("is-stuck", window.scrollY > 12);
    };
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });
  }

  /* ----------------------------------------------------------- mobile menu */
  var toggle = doc.getElementById("navToggle");
  var mobileNav = doc.getElementById("mobileNav");
  if (toggle && mobileNav) {
    var setMenu = function (open) {
      toggle.classList.toggle("is-open", open);
      toggle.setAttribute("aria-expanded", String(open));
      mobileNav.classList.toggle("is-open", open);
      // `hidden` keeps the links out of the tab order while the menu is shut.
      if (open) { mobileNav.removeAttribute("hidden"); }
      else { mobileNav.setAttribute("hidden", ""); }
    };

    toggle.addEventListener("click", function () {
      setMenu(!toggle.classList.contains("is-open"));
    });

    // Any tap inside the menu navigates away, so close it first.
    mobileNav.addEventListener("click", function (e) {
      if (e.target.closest("a")) { setMenu(false); }
    });

    doc.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && toggle.classList.contains("is-open")) {
        setMenu(false);
        toggle.focus();
      }
    });

    // Back on desktop the mobile menu is hidden by CSS anyway; reset its
    // state so it does not reappear open when the viewport shrinks again.
    window.addEventListener("resize", function () {
      if (window.innerWidth > 860 && toggle.classList.contains("is-open")) {
        setMenu(false);
      }
    });
  }

  /* -------------------------------------------------------------- dropdown */
  var drops = Array.prototype.slice.call(doc.querySelectorAll("[data-drop]"));
  drops.forEach(function (drop) {
    // Two shapes of trigger: a lone button that only opens the menu, or a link
    // to a real page next to a small caret button that opens it. The caret
    // wins when both are present, so the link keeps navigating on click.
    var btn = drop.querySelector(".nav-drop-toggle") || drop.querySelector("button.nav-drop-btn");
    if (!btn) { return; }

    // A page inside this section marks the parent as current too.
    if (drop.querySelector('[aria-current="page"]')) {
      drop.classList.add("is-current");
    }

    var setDrop = function (open) {
      drop.classList.toggle("is-open", open);
      btn.setAttribute("aria-expanded", String(open));
    };

    btn.addEventListener("click", function (e) {
      e.preventDefault();
      e.stopPropagation();
      setDrop(!drop.classList.contains("is-open"));
    });
    drop.addEventListener("mouseenter", function () { setDrop(true); });
    drop.addEventListener("mouseleave", function () { setDrop(false); });
    drop.addEventListener("focusout", function (e) {
      if (!drop.contains(e.relatedTarget)) { setDrop(false); }
    });
    doc.addEventListener("click", function (e) {
      if (!drop.contains(e.target)) { setDrop(false); }
    });
    doc.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && drop.classList.contains("is-open")) {
        setDrop(false);
        btn.focus();
      }
    });
  });

  /* --------------------------------------------------------------- reveals */
  var revealables = doc.querySelectorAll(".reveal");
  if (revealables.length) {
    var showAll = function () {
      revealables.forEach(function (el) { el.classList.add("is-visible"); });
    };

    if (!("IntersectionObserver" in window)) {
      // No observer support: show everything rather than hide it forever.
      showAll();
    } else {
      var io = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            entry.target.classList.add("is-visible");
            io.unobserve(entry.target);
          }
        });
      }, { rootMargin: "0px 0px -8% 0px", threshold: 0.06 });
      revealables.forEach(function (el) { io.observe(el); });

      // Backstop: in any environment where the observer never fires (a page
      // that is not compositing, an odd embedded browser), show the content
      // anyway rather than leave the site looking empty.
      window.setTimeout(showAll, 2500);
    }
  }

  /* -------------------------------------------------------------- carousel */
  doc.querySelectorAll("[data-carousel]").forEach(function (root) {
    var track = root.querySelector(".carousel-track");
    var prev = root.querySelector(".carousel-btn.prev");
    var next = root.querySelector(".carousel-btn.next");
    if (!track || !prev || !next) { return; }

    var step = function () {
      var tile = track.firstElementChild;
      if (!tile) { return track.clientWidth; }
      // One tile plus the gap between tiles.
      var gap = parseFloat(getComputedStyle(track).columnGap || "0") || 0;
      return tile.getBoundingClientRect().width + gap;
    };

    var sync = function () {
      // 2px of slack: fractional scroll widths otherwise leave "next" enabled
      // forever at the right-hand end.
      var max = track.scrollWidth - track.clientWidth - 2;
      prev.disabled = track.scrollLeft <= 2;
      next.disabled = track.scrollLeft >= max;
    };

    var go = function (dir) {
      track.scrollBy({ left: dir * step(), behavior: "smooth" });
      // The scroll event drives sync normally, but smooth scrolling can finish
      // without one in some browsers, which would strand a button disabled.
      window.setTimeout(sync, 450);
    };

    prev.addEventListener("click", function () { go(-1); });
    next.addEventListener("click", function () { go(1); });
    track.addEventListener("scroll", sync, { passive: true });
    window.addEventListener("resize", sync);
    sync();
  });

  /* ------------------------------------------------------- gathering countdown
     Counts down to the next Saturday 19:00 *in Zagreb*, not in whatever zone
     the visitor happens to be in, so someone watching from abroad sees the
     real time remaining. Rolls over on its own every week. */
  var countdowns = doc.querySelectorAll("[data-countdown]");
  if (countdowns.length) {
    var ZONE = "Europe/Zagreb";
    var HOUR = 19;          // gathering starts at 19:00
    var RUNS_FOR = 2 * 3600e3;  // treat it as under way for two hours

    // How far ahead of UTC the zone is at this instant, in ms.
    var zoneOffset = function (date) {
      var parts = new Intl.DateTimeFormat("en-US", {
        timeZone: ZONE, hour12: false,
        year: "numeric", month: "2-digit", day: "2-digit",
        hour: "2-digit", minute: "2-digit", second: "2-digit"
      }).formatToParts(date);
      var p = {};
      parts.forEach(function (part) { if (part.type !== "literal") { p[part.type] = part.value; } });
      // Some engines report midnight as hour 24.
      var hour = p.hour === "24" ? 0 : Number(p.hour);
      var asUTC = Date.UTC(Number(p.year), Number(p.month) - 1, Number(p.day),
                           hour, Number(p.minute), Number(p.second));
      return asUTC - date.getTime();
    };

    // Real instant of a Zagreb wall-clock time. Resolved twice because the
    // offset can differ between now and the target across a DST change.
    var instantOf = function (y, m, d, h) {
      var wall = Date.UTC(y, m, d, h, 0, 0);
      var guess = wall - zoneOffset(new Date(wall));
      return wall - zoneOffset(new Date(guess));
    };

    var nextGathering = function (now) {
      var zagreb = new Date(now.getTime() + zoneOffset(now));
      var y = zagreb.getUTCFullYear(), m = zagreb.getUTCMonth(), d = zagreb.getUTCDate();
      // 6 = Saturday. Wind back to this week's Saturday, then step forward.
      var start = instantOf(y, m, d + ((6 - zagreb.getUTCDay() + 7) % 7), HOUR);
      if (now.getTime() >= start + RUNS_FOR) {
        start = instantOf(y, m, d + ((6 - zagreb.getUTCDay() + 7) % 7) + 7, HOUR);
      }
      return start;
    };

    var render = function (el) {
      var out = el.querySelector("[data-countdown-value]");
      if (!out) { return; }
      var now = new Date();
      var start = nextGathering(now);
      var left = start - now.getTime();

      if (left <= 0) {
        out.textContent = el.getAttribute("data-live");
        return;
      }
      var s = Math.floor(left / 1000);
      var d = Math.floor(s / 86400);
      var h = Math.floor((s % 86400) / 3600);
      var m = Math.floor((s % 3600) / 60);
      var sec = s % 60;
      var pad = function (n) { return n < 10 ? "0" + n : String(n); };

      var bits = [];
      if (d) { bits.push(d + " " + el.getAttribute("data-unit-d")); }
      if (d || h) { bits.push(pad(h) + " " + el.getAttribute("data-unit-h")); }
      bits.push(pad(m) + " " + el.getAttribute("data-unit-m"));
      bits.push(pad(sec) + " " + el.getAttribute("data-unit-s"));

      out.textContent = el.getAttribute("data-lead") + " " + bits.join(" ");
    };

    countdowns.forEach(function (el) {
      // Only take over the fallback text once we know Intl can do the zone
      // maths; otherwise the static "every Saturday" sentence stays put.
      try {
        new Intl.DateTimeFormat("en-US", { timeZone: ZONE }).format(new Date());
      } catch (e) {
        return;
      }
      el.classList.add("is-live");
      render(el);
      window.setInterval(function () { render(el); }, 1000);
    });
  }

  /* ------------------------------------------------------------ footer year */
  doc.querySelectorAll("[data-year]").forEach(function (el) {
    el.textContent = String(new Date().getFullYear());
  });
})();
