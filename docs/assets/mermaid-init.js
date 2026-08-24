/* Render ```mermaid fences on site pages.
 *
 * Decks render mermaid through decks/deck.js. Site pages render it here, from
 * the same vendored copy of mermaid, so a module page works in a classroom with
 * no network (DECISION-mermaid-diagrams).
 *
 * The fence is compiled to <pre class="diagram"><code>...</code></pre> by the
 * superfences custom fence in mkdocs.yml. The class is "diagram" rather than
 * "mermaid" on purpose: it keeps Material's own Mermaid integration, which
 * fetches from a CDN, from firing.
 */
(function () {
  "use strict";

  function isDark() {
    return document.body.getAttribute("data-md-color-scheme") === "slate";
  }

  function renderAll() {
    if (typeof window.mermaid === "undefined") return;
    var nodes = document.querySelectorAll("pre.diagram");
    if (!nodes.length) return;

    window.mermaid.initialize({
      startOnLoad: false,
      securityLevel: "loose",
      theme: isDark() ? "dark" : "default",
      flowchart: { useMaxWidth: true },
      fontFamily: getComputedStyle(document.body).fontFamily
    });

    Array.prototype.forEach.call(nodes, function (pre, i) {
      /* Keep the source, so a palette switch can re-render from it. */
      var src = pre.getAttribute("data-src");
      if (src === null) {
        src = pre.textContent;
        pre.setAttribute("data-src", src);
      }
      var id = "mermaid-" + i + "-" + Math.random().toString(36).slice(2, 8);
      window.mermaid
        .render(id, src)
        .then(function (result) {
          pre.innerHTML = result.svg;
        })
        .catch(function () {
          pre.textContent = src;
        });
    });
  }

  /* Material swaps this attribute when the reader toggles light/dark. */
  var observer = new MutationObserver(function (records) {
    for (var i = 0; i < records.length; i++) {
      if (records[i].attributeName === "data-md-color-scheme") {
        renderAll();
        return;
      }
    }
  });
  observer.observe(document.body, { attributes: true });

  /* navigation.instant swaps pages without a reload, so hook Material's
     document observable when it exists and fall back to a plain load. */
  if (typeof window.document$ !== "undefined") {
    window.document$.subscribe(renderAll);
  } else {
    document.addEventListener("DOMContentLoaded", renderAll);
  }
})();
