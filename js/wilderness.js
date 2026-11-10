/* Wilderness field-guide layer — Things To Do prototype.
   Feature branch: feature/wilderness-redesign. Loaded only by things-to-do.html.
   Progressive enhancement: the page is complete without it. */
(function () {
  "use strict";

  var root = document.documentElement;
  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var $ = function (s, c) { return (c || document).querySelector(s); };
  var $$ = function (s, c) { return Array.prototype.slice.call((c || document).querySelectorAll(s)); };
  var rand = function (a, b) { return a + Math.random() * (b - a); };
  if (!reduce) root.classList.add("wr-motion");

  /* ---------- 1. characters: clone the drawn templates into their slots ---------- */
  $$("[data-critter]").forEach(function (slot) {
    var tpl = document.getElementById("tpl-" + slot.getAttribute("data-critter"));
    if (!tpl) return;
    slot.appendChild(tpl.content.cloneNode(true));
  });

  /* ---------- 2. hero stage: sit exactly on the engraving, whatever the crop ---------- */
  var heroArt = $("[data-hero-art]");
  var heroImg = heroArt && $("img", heroArt);
  var stage = heroArt && $("[data-stage]", heroArt);
  var NW = 1536, NH = 1024;

  function fitStage() {
    if (!stage || !heroImg) return;
    var w = heroImg.clientWidth, h = heroImg.clientHeight;
    if (!w || !h) return;
    var pos = (getComputedStyle(heroImg).objectPosition || "50% 50%").split(" ");
    var px = parseFloat(pos[0]) / 100, py = parseFloat(pos[1]) / 100;
    if (isNaN(px)) px = .5; if (isNaN(py)) py = .5;
    var s = Math.max(w / NW, h / NH), iw = NW * s, ih = NH * s;
    stage.style.width = iw + "px"; stage.style.height = ih + "px";
    stage.style.left = (w - iw) * px + "px"; stage.style.top = (h - ih) * py + "px";
    stage.style.setProperty("--s", s);
    stage.classList.add("is-fit");
  }
  if (stage) {
    var canoe = $(".hs-canoe", stage);
    if (canoe) canoe.style.backgroundImage = "url(" + heroImg.getAttribute("src") + ")";
    fitStage();
    window.addEventListener("resize", fitStage);
    if (heroImg.complete) fitStage(); else heroImg.addEventListener("load", fitStage);
    if (window.ResizeObserver) new ResizeObserver(fitStage).observe(heroImg);
  }

  /* ---------- 3. what is on screen is what animates ---------- */
  var liveTargets = $$("[data-stage], section.ttd, .cta-eagle, .stay-hero-in");
  if ("IntersectionObserver" in window) {
    var liveIO = new IntersectionObserver(function (en) {
      en.forEach(function (e) { e.target.classList.toggle("is-live", e.isIntersecting); });
    }, { rootMargin: "120px 0px" });
    liveTargets.forEach(function (t) { liveIO.observe(t); });
  } else liveTargets.forEach(function (t) { t.classList.add("is-live"); });

  /* things that play once when they arrive */
  var onceSel = [".say", ".t-worth", ".a-canoe", ".a-trout", ".a-skates", ".sled-art", ".t-signpost",
    ".ttd-shot", ".shot-route", ".crit-slot", ".hand-reveal"].join(",");
  var onceEls = $$(onceSel);
  $$(".shot-route").forEach(function (svg) {
    var p = $("path", svg), d = p ? p.getAttribute("d") : "";
    var x = parseFloat((d.match(/M\s*(-?[\d.]+)/) || [0, 0])[1]);
    if (x > 100) svg.setAttribute("data-from", "r");
  });
  if (reduce || !("IntersectionObserver" in window)) {
    onceEls.forEach(function (el) { el.classList.add("wr-in"); });
  } else {
    var onceIO = new IntersectionObserver(function (en) {
      en.forEach(function (e) {
        if (!e.isIntersecting) return;
        var el = e.target;
        el.classList.add("wr-in");
        if (el.classList.contains("a-trout")) { el.classList.add("leap"); }
        onceIO.unobserve(el);
      });
    }, { threshold: .35, rootMargin: "0px 0px -6% 0px" });
    onceEls.forEach(function (el) { onceIO.observe(el); });
  }

  /* ---------- 4. weather & water, built here so the HTML stays clean ---------- */
  function el(tag, cls, css, parent) {
    var n = document.createElement(tag);
    if (cls) n.className = cls;
    if (css) n.style.cssText = css;
    if (parent) parent.appendChild(n);
    return n;
  }
  function fxLayer(sectionSel, sheetSel) {
    var sec = $(sectionSel), sheet = sec && $(sheetSel, sec);
    if (!sec || !sheet) return null;
    var layer = el("div", "fx-layer");
    layer.setAttribute("aria-hidden", "true");
    sheet.insertAdjacentElement("afterend", layer);
    return layer;
  }
  if (!reduce) {
    var small = window.matchMedia("(max-width: 700px)").matches;

    /* hero: sun-path glints and bow ripples */
    if (stage) {
      var gl = $(".hs-glints", stage);
      if (gl) {
        for (var g = 0; g < 14; g++) {
          el("i", "", "--x:" + rand(9, 15).toFixed(1) + "%;--y:" + (66 + g * 2.1 + rand(0, 1.2)).toFixed(1) +
            "%;--w:" + rand(2, 6.5).toFixed(1) + "%;--d:" + (g * .45).toFixed(2) + "s", gl);
        }
      }
    }

    /* falls: rising mist at the foot of each drop */
    var fl = fxLayer(".ttd-forested", ".forest-sheet");
    if (fl) {
      [[36.4, 43], [60.2, 43.4]].forEach(function (p, i) {
        for (var k = 0; k < 3; k++) {
          el("i", "fx-mist", "left:" + (p[0] + rand(-1.5, 1.5)) + "%;top:" + p[1] + "%;--d:" + (k * 2 + i * .8) + "s", fl);
        }
      });
    }

    /* glade: fireflies drifting between the trunks */
    var gd = fxLayer(".ttd-glade", ".glade-sheet");
    if (gd) {
      for (var m = 0; m < (small ? 7 : 14); m++) {
        el("i", "fx-mote", "left:" + rand(6, 94).toFixed(1) + "%;top:" + rand(22, 62).toFixed(1) +
          "%;--d:" + rand(0, 9).toFixed(1) + "s;--dx:" + rand(-30, 30).toFixed(0) + "px", gd);
      }
    }

    /* basin: rings where fish are rising */
    var bs = fxLayer(".ttd-basin", ".basin-sheet");
    if (bs) {
      [[49, 33.5], [64, 36.5], [38, 36]].forEach(function (p, i) {
        el("i", "fx-ring loop", "left:" + p[0] + "%;top:" + p[1] + "%;width:5%;--d:" + (i * 2.4) + "s", bs);
      });
    }

    /* the two winter sections: snow */
    ["section.ttd-ridge", "section.ttd-snow"].forEach(function (sel) {
      var sec = $(sel); if (!sec) return;
      var f = el("div", "fx-snow", "", sec); f.setAttribute("aria-hidden", "true");
      var sheet = $(".ridge-sheet,.snow-sheet", sec); if (sheet) sheet.insertAdjacentElement("afterend", f);
      for (var s = 0; s < (small ? 14 : 30); s++) {
        el("i", "", "--x:" + rand(1, 99).toFixed(1) + "%;--s:" + rand(3, 7.5).toFixed(1) + "px;--t:" +
          rand(11, 22).toFixed(1) + "s;--d:-" + rand(0, 20).toFixed(1) + "s", f);
      }
    });
  }

  /* ---------- 5. the trout that jumps out of the hero lake ---------- */
  function ring(parent, x, y) {
    var r = el("i", "hs-ring splash", "left:" + x + "%;top:" + y + "%", parent);
    r.addEventListener("animationend", function () { r.remove(); });
  }
  function leap() {
    var fish = stage && $(".hs-trout", stage);
    if (!fish || reduce || document.hidden || !stage.classList.contains("is-live") || !stage.classList.contains("is-fit")) return;
    var W = stage.clientWidth, s = W / NW;
    var x0 = rand(300, 560), dx = rand(70, 120) * (Math.random() < .5 ? 1 : -1), h = rand(55, 95);
    var y0 = rand(790, 850);
    var n = 18, frames = [];
    for (var i = 0; i <= n; i++) {
      var t = i / n, x = x0 + dx * t, y = y0 - 4 * h * t * (1 - t);
      var vy = -4 * h * (1 - 2 * t);
      var ang = (dx > 0 ? Math.atan2(vy, dx) : Math.atan2(-vy, -dx)) * 180 / Math.PI;
      frames.push({
        transform: "translate(" + (x * s) + "px," + (y * s) + "px) " + "rotate(" + ang + "deg)" + (dx < 0 ? " scaleX(-1)" : ""),
        opacity: (i === 0 || i === n) ? 0 : 1, offset: t
      });
    }
    ring(stage, x0 / NW * 100, y0 / NH * 100);
    var a = fish.animate(frames, { duration: 1050, easing: "linear" });
    a.onfinish = function () { ring(stage, (x0 + dx) / NW * 100, y0 / NH * 100); fish.style.opacity = 0; };
  }
  if (stage && !reduce) {
    (function loop() { setTimeout(function () { leap(); loop(); }, rand(8000, 15000)); })();
    setTimeout(leap, 4500);
  }

  /* ---------- 6. parallax + progress, one rAF, no layout reads in the loop ---------- */
  var par = [];
  function collectParallax() {
    par = [];
    if (reduce || window.innerWidth < 900) { $$("[data-par]").forEach(function (n) { n.style.removeProperty("--py"); }); return; }
    $$(".ttd-shot, .say, .t-signpost, .a-trout, .a-canoe, .sled-art, .a-skates, .eye-out").forEach(function (n) {
      var k = n.classList.contains("ttd-shot") ? .07 : -.045;
      n.setAttribute("data-par", "");
      par.push({ n: n, k: k });
    });
  }
  var chapters = [];
  var rail = $(".journey"), railLinks = $$(".j-list a", rail || document), now = $(".j-now");
  function collectChapters() {
    chapters = railLinks.map(function (a) {
      var t = document.getElementById(a.getAttribute("href").slice(1));
      return { a: a, t: t, name: a.getAttribute("data-name") || a.textContent };
    }).filter(function (c) { return c.t; });
  }
  var ticking = false, lastActive = -1;
  function frame() {
    ticking = false;
    var vh = window.innerHeight, y = window.pageYOffset;
    /* hero parallax: image drifts slower than the page */
    if (heroArt && !reduce && y < vh * 1.3) {
      var hh = heroArt.offsetHeight;
      heroArt.style.translate = "0 " + Math.min(y * .12, hh * .06) + "px";
    }
    /* depth: photographs drift a touch faster than the handwriting */
    for (var i = 0; i < par.length; i++) {
      var r = par[i].n.getBoundingClientRect();
      if (r.bottom < -80 || r.top > vh + 80) continue;
      var off = (r.top + r.height / 2 - vh / 2);
      par[i].n.style.setProperty("--py", (off * par[i].k).toFixed(1) + "px");
    }
    /* chapter rail */
    if (rail && chapters.length) {
      var doc = document.documentElement, max = doc.scrollHeight - vh;
      var prog = max > 0 ? Math.min(1, Math.max(0, y / max)) : 0;
      rail.style.setProperty("--pf", prog.toFixed(3));
      var line = y + vh * .4, active = 0;
      for (var c = 0; c < chapters.length; c++) {
        if (chapters[c].t.getBoundingClientRect().top + y <= line) active = c;
      }
      var footTop = $(".foot") ? $(".foot").getBoundingClientRect().top : 9e9;
      rail.classList.toggle("is-on", y > vh * .55 && footTop > vh * .5);
      if (active !== lastActive) {
        chapters.forEach(function (ch, idx) {
          ch.a.classList.toggle("done", idx < active);
          if (idx === active) ch.a.setAttribute("aria-current", "true"); else ch.a.removeAttribute("aria-current");
        });
        if (now) now.firstChild.nodeValue = (active ? (active >= 7 ? "Epilogue" : "Ch. " + toRoman(active)) + " \u00b7 " : "") + chapters[active].name;
        lastActive = active;
      }
      if (now) now.style.setProperty("--p", (prog * 100).toFixed(1) + "%");
    }
  }
  function toRoman(n) { return ["", "I", "II", "III", "IV", "V", "VI", "VII"][n] || n; }
  function onScroll() { if (!ticking) { ticking = true; requestAnimationFrame(frame); } }
  collectParallax(); collectChapters(); frame();
  window.addEventListener("scroll", onScroll, { passive: true });
  window.addEventListener("resize", function () { collectParallax(); collectChapters(); onScroll(); });
  window.addEventListener("load", function () { collectChapters(); frame(); });

  /* ---------- 7. the characters have personality ---------- */
  var pointer = null, pTick = false;
  var watchers = $$(".crit-fox, .crit-hare");
  if (!reduce && window.matchMedia("(pointer: fine)").matches) {
    window.addEventListener("pointermove", function (e) {
      pointer = e;
      if (pTick) return; pTick = true;
      requestAnimationFrame(function () {
        pTick = false;
        watchers.forEach(function (c) {
          var r = c.getBoundingClientRect();
          if (r.bottom < 0 || r.top > window.innerHeight) return;
          var dx = pointer.clientX - (r.left + r.width / 2), dy = pointer.clientY - (r.top + r.height * .45);
          var d = Math.hypot(dx, dy) || 1, k = Math.min(1, d / 260);
          $$(".pupil", c).forEach(function (p) {
            p.style.setProperty("--px", (dx / d * 3.2 * k).toFixed(2) + "px");
            p.style.setProperty("--py", (dy / d * 2.6 * k).toFixed(2) + "px");
          });
        });
      });
    }, { passive: true });
  }
  var sounds = { fox: "Yip!", hare: "…!", eagle: "Skree!" };
  document.addEventListener("click", function (e) {
    var c = e.target.closest && e.target.closest(".crit");
    if (!c || reduce) return;
    var kind = c.classList.contains("crit-fox") ? "fox" : c.classList.contains("crit-hare") ? "hare" : "eagle";
    c.classList.remove("is-poked"); void c.getBoundingClientRect().width; c.classList.add("is-poked");
    var host = c.parentNode, say = $(".crit-say", host) || el("p", "crit-say hand", "left:55%;top:-.4em", host);
    say.textContent = sounds[kind]; say.classList.remove("is-on"); void say.offsetWidth; say.classList.add("is-on");
  });

  /* rail: anchor jumps respect the sticky nav */
  $$(".j-list a, .trail-cue").forEach(function (a) {
    a.addEventListener("click", function () {
      var t = document.getElementById(a.getAttribute("href").slice(1));
      if (t) t.setAttribute("tabindex", "-1");
    });
  });
})();
