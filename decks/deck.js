/* ============================================================
   COSC 40943 deck runtime
   Keyboard-driven presenter for decks built by slides/build.py.
   No framework. Everything here is generic; nothing is per-deck.
   ============================================================ */

(function () {
  "use strict";

  var stage    = document.getElementById("stage");
  var slides   = Array.prototype.slice.call(document.querySelectorAll(".slide"));
  var notesEl  = document.getElementById("notes");
  var notesTxt = document.getElementById("notestxt");
  var notesWho = document.getElementById("noteswho");
  var barFill  = document.querySelector("#bar span");
  var blackout = document.getElementById("blackout");
  var help     = document.getElementById("help");
  var grid     = document.getElementById("grid");

  var i = 0;          /* current slide      */
  var j = 0;          /* current step       */
  var notesOpen = false;

  /* ---------- fit the 1280x720 canvas to the projector ---------- */
  function fit() {
    var w = window.innerWidth, h = window.innerHeight;
    var k = Math.min(w / 1280, h / 720);
    slides.forEach(function (s) { s.style.transform = "scale(" + k + ")"; });
  }

  /* ---------- steps ---------- */
  function stepsOf(slide) {
    return Array.prototype.slice.call(slide.querySelectorAll("[data-step]"));
  }
  function maxStep(slide) {
    var st = stepsOf(slide);
    if (!st.length) return 0;
    return st.reduce(function (m, el) {
      return Math.max(m, parseInt(el.getAttribute("data-step"), 10) || 0);
    }, 0);
  }

  /* ---------- render ---------- */
  function render(pushHash) {
    slides.forEach(function (s, n) { s.classList.toggle("live", n === i); });

    var slide = slides[i];
    stepsOf(slide).forEach(function (el) {
      var n = parseInt(el.getAttribute("data-step"), 10) || 0;
      el.classList.toggle("shown", n <= j);
    });

    var note = slide.getAttribute("data-note") || "";
    notesTxt.innerHTML = note;
    notesWho.textContent = "Slide " + (i + 1) + " of " + slides.length +
      (maxStep(slide) ? "  ·  step " + (j + 1) + " of " + (maxStep(slide) + 1) : "");

    barFill.style.width = ((i + 1) / slides.length * 100) + "%";

    if (pushHash !== false) {
      try { history.replaceState(null, "", "#" + (i + 1)); } catch (e) {}
    }
    renderMermaid(slide);
  }

  function next() {
    if (j < maxStep(slides[i])) { j++; render(); return; }
    if (i < slides.length - 1) { i++; j = 0; render(); }
  }
  function prev() {
    if (j > 0) { j--; render(); return; }
    if (i > 0) { i--; j = maxStep(slides[i]); render(); }
  }
  function skipSlide() {
    if (i < slides.length - 1) { i++; j = 0; render(); }
  }
  function goTo(n) {
    i = Math.max(0, Math.min(slides.length - 1, n));
    j = 0; render();
  }

  /* ---------- mermaid, rendered lazily per slide ---------- */
  var mermaidReady = false;
  function initMermaid() {
    if (mermaidReady || typeof window.mermaid === "undefined") return;
    var css = getComputedStyle(document.documentElement);
    var v = function (name, fallback) {
      return (css.getPropertyValue(name) || fallback).trim();
    };
    window.mermaid.initialize({
      startOnLoad: false,
      securityLevel: "loose",
      fontFamily: v("--font-body", "sans-serif"),
      theme: "base",
      themeVariables: {
        darkMode: true,
        background: v("--bg", "#0F1420"),
        primaryColor: v("--surface-2", "#1E273A"),
        primaryTextColor: v("--ink", "#F2EDE3"),
        primaryBorderColor: v("--accent", "#9B6BD6"),
        lineColor: v("--ink-dim", "#9AA3B5"),
        secondaryColor: v("--surface", "#171E2E"),
        tertiaryColor: v("--surface", "#171E2E"),
        fontSize: "18px",
        nodeBorder: v("--accent", "#9B6BD6"),
        clusterBkg: v("--surface", "#171E2E"),
        clusterBorder: v("--rule", "#2C374E"),
        titleColor: v("--ink", "#F2EDE3"),
        edgeLabelBackground: v("--bg", "#0F1420"),
        actorBkg: v("--surface-2", "#1E273A"),
        actorBorder: v("--accent", "#9B6BD6"),
        actorTextColor: v("--ink", "#F2EDE3"),
        signalColor: v("--ink-dim", "#9AA3B5"),
        signalTextColor: v("--ink", "#F2EDE3"),
        labelBoxBkgColor: v("--surface", "#171E2E"),
        labelTextColor: v("--ink", "#F2EDE3"),
        noteBkgColor: v("--accent-deep", "#4D1979"),
        noteTextColor: v("--ink", "#F2EDE3")
      }
    });
    mermaidReady = true;
  }

  function renderMermaid(slide) {
    if (typeof window.mermaid === "undefined") return;
    initMermaid();
    var pending = slide.querySelectorAll(".mermaid:not([data-done])");
    if (!pending.length) return;
    Array.prototype.forEach.call(pending, function (el) {
      el.setAttribute("data-done", "1");
    });
    try {
      window.mermaid.run({ nodes: pending });
    } catch (e) {
      Array.prototype.forEach.call(pending, function (el) {
        el.innerHTML = '<p class="small">Diagram failed to render. Check the mermaid block.</p>';
      });
    }
  }

  /* ---------- overview grid ---------- */
  function buildGrid() {
    slides.forEach(function (s, n) {
      var h = s.querySelector("h1, h2");
      var b = document.createElement("button");
      b.className = "thumb";
      b.innerHTML = '<div class="n">' + (n + 1) + "</div><div class=\"t\"></div>";
      b.querySelector(".t").textContent = h ? h.textContent : "(slide " + (n + 1) + ")";
      b.addEventListener("click", function () {
        grid.classList.remove("on");
        goTo(n);
      });
      grid.appendChild(b);
    });
  }

  /* ---------- keys ---------- */
  document.addEventListener("keydown", function (e) {
    if (e.ctrlKey || e.metaKey || e.altKey) return;
    var k = e.key;

    if (grid.classList.contains("on") && (k === "Escape" || k === "o" || k === "O")) {
      grid.classList.remove("on"); e.preventDefault(); return;
    }

    switch (k) {
      case "ArrowRight": case " ": case "PageDown": case "Enter":
        next(); e.preventDefault(); break;
      case "ArrowLeft": case "PageUp": case "Backspace":
        prev(); e.preventDefault(); break;
      case "ArrowDown":
        skipSlide(); e.preventDefault(); break;
      case "ArrowUp":
        if (i > 0) { i--; j = 0; render(); } e.preventDefault(); break;
      case "s": case "S":
        skipSlide(); e.preventDefault(); break;
      case "Home":
        goTo(0); e.preventDefault(); break;
      case "End":
        goTo(slides.length - 1); e.preventDefault(); break;
      case "n": case "N":
        notesOpen = !notesOpen; notesEl.classList.toggle("open", notesOpen); e.preventDefault(); break;
      case "b": case "B":
        blackout.classList.toggle("on"); e.preventDefault(); break;
      case "o": case "O":
        grid.classList.toggle("on"); e.preventDefault(); break;
      case "?": case "/":
        help.classList.toggle("on"); e.preventDefault(); break;
      case "Escape":
        help.classList.remove("on"); blackout.classList.remove("on"); grid.classList.remove("on"); break;
    }
  });

  stage.addEventListener("click", function (e) {
    if (e.target.closest("a")) return;
    if (e.clientX < window.innerWidth * 0.2) prev(); else next();
  });

  var hc = document.querySelector("#help .close");
  if (hc) hc.addEventListener("click", function () { help.classList.remove("on"); });
  help.addEventListener("click", function (e) { if (e.target === help) help.classList.remove("on"); });

  window.addEventListener("resize", fit);
  window.addEventListener("beforeprint", function () {
    slides.forEach(function (s) {
      stepsOf(s).forEach(function (el) { el.classList.add("shown"); });
      renderMermaid(s);
    });
  });

  /* ---------- boot ---------- */
  buildGrid();
  fit();
  var start = parseInt((location.hash || "").replace("#", ""), 10);
  if (start && start >= 1 && start <= slides.length) i = start - 1;
  render(false);
})();
