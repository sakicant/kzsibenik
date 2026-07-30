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
    var btn = drop.querySelector(".nav-drop-btn");
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

  /* ------------------------------------------------------------ footer year */
  doc.querySelectorAll("[data-year]").forEach(function (el) {
    el.textContent = String(new Date().getFullYear());
  });
})();
