(function(){
  "use strict";
  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  var burger = document.querySelector(".burger"), menu = document.getElementById("menu");
  burger.addEventListener("click", function () {
    var open = menu.classList.toggle("open");
    burger.setAttribute("aria-expanded", String(open));
    burger.textContent = open ? "Close" : "Menu";
  });
  menu.addEventListener("click", function (e) {
    if (e.target.tagName === "A") {
      menu.classList.remove("open");
      burger.setAttribute("aria-expanded", "false");
      burger.textContent = "Menu";
    }
  });

  /* ---- Gallery lightbox ----
     Works for any container holding .gitem buttons. The list is read at the
     moment it opens, so a filtered gallery only steps through what is showing. */
  var lb = document.getElementById("lightbox");
  if (lb) {
    var lbImg = document.getElementById("lb-img"),
        lbCap = document.getElementById("lb-cap"),
        lbCount = document.getElementById("lb-count"),
        list = [], idx = 0, opener = null;

    var show = function (i) {
      idx = (i + list.length) % list.length;
      var img = list[idx].querySelector("img"),
          cap = list[idx].querySelector(".cap");
      lbImg.src = img.getAttribute("data-full") || img.currentSrc || img.src;
      lbImg.alt = img.alt;
      lbCap.textContent = cap ? cap.textContent : "";
      lbCount.textContent = (idx + 1) + " / " + list.length;
    };
    var openLb = function (el) {
      var box = el.closest("[data-gallery]") || document;
      list = Array.prototype.slice.call(box.querySelectorAll(".gitem"))
               .filter(function (n) { return !n.hidden && !n.hasAttribute("data-clone"); });
      var i = list.indexOf(el);
      if (i < 0) { list = [el]; i = 0; }
      opener = el;
      show(i);
      lb.hidden = false;
      lb.classList.add("open");
      document.body.style.overflow = "hidden";
      lb.querySelector(".lb-close").focus();
    };
    var closeLb = function () {
      lb.classList.remove("open");
      lb.hidden = true;
      lbImg.removeAttribute("src");
      document.body.style.overflow = "";
      if (opener) opener.focus();
    };

    document.addEventListener("click", function (e) {
      var el = e.target.closest ? e.target.closest(".gitem") : null;
      if (!el) return;
      if (el.getAttribute("data-suppress-click") === "1") {
        el.removeAttribute("data-suppress-click");
        return;
      }
      openLb(el);
    });
    lb.querySelector(".lb-close").addEventListener("click", closeLb);
    lb.querySelector(".lb-prev").addEventListener("click", function () { show(idx - 1); });
    lb.querySelector(".lb-next").addEventListener("click", function () { show(idx + 1); });
    lb.addEventListener("click", function (e) { if (e.target === lb) closeLb(); });
    document.addEventListener("keydown", function (e) {
      if (lb.hidden) return;
      if (e.key === "Escape") closeLb();
      else if (e.key === "ArrowLeft") show(idx - 1);
      else if (e.key === "ArrowRight") show(idx + 1);
    });
    lb.addEventListener("keydown", function (e) {
      if (e.key !== "Tab") return;
      var f = lb.querySelectorAll("button"), first = f[0], last = f[f.length - 1];
      if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
      else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
    });

    /* swipe between photographs on touch */
    var sx = 0, sy = 0, tracking = false;
    lb.addEventListener("touchstart", function (e) {
      if (e.touches.length !== 1) return;
      tracking = true; sx = e.touches[0].clientX; sy = e.touches[0].clientY;
    }, { passive: true });
    lb.addEventListener("touchend", function (e) {
      if (!tracking) return;
      tracking = false;
      var dx = e.changedTouches[0].clientX - sx,
          dy = e.changedTouches[0].clientY - sy;
      if (Math.abs(dx) > 45 && Math.abs(dx) > Math.abs(dy)) show(idx + (dx < 0 ? 1 : -1));
      else if (dy > 90 && Math.abs(dy) > Math.abs(dx)) closeLb();
    }, { passive: true });
  }

  /* ---- Gallery filters ---- */
  document.querySelectorAll("[data-gallery-filters]").forEach(function (bar) {
    var gallery = document.getElementById(bar.getAttribute("data-gallery-filters"));
    if (!gallery) return;
    var items = Array.prototype.slice.call(gallery.querySelectorAll(".gitem"));
    var count = document.getElementById(bar.getAttribute("data-count") || "");
    bar.addEventListener("click", function (e) {
      var btn = e.target.closest("button");
      if (!btn) return;
      var cat = btn.getAttribute("data-cat");
      bar.querySelectorAll("button").forEach(function (b) {
        b.setAttribute("aria-pressed", String(b === btn));
      });
      var shown = 0;
      items.forEach(function (it) {
        var match = cat === "all" || it.getAttribute("data-cat") === cat;
        it.hidden = !match;
        if (match) shown++;
      });
      if (count) count.textContent = shown + " photograph" + (shown === 1 ? "" : "s");
    });
  });

  var revealables = document.querySelectorAll(".rv");
  if (reduce || !("IntersectionObserver" in window)) {
    revealables.forEach(function (el) { el.classList.add("in"); });
  } else {
    var io = new IntersectionObserver(function (en) {
      en.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add("in"); io.unobserve(e.target); } });
    }, { rootMargin: "0px 0px -12% 0px" });
    revealables.forEach(function (el) { io.observe(el); });
  }
})();

/* ---- Carousels: native scroll-snap, with buttons and dots ---- */
(function(){
  "use strict";
  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  document.querySelectorAll("[data-carousel]").forEach(function (root) {
    var track  = root.querySelector(".carousel-track");
    var slides = Array.prototype.slice.call(track.querySelectorAll(".cslide"));
    var dots   = Array.prototype.slice.call(root.querySelectorAll(".cdot"));
    var prev   = root.querySelector(".cprev");
    var next   = root.querySelector(".cnext");
    if (slides.length < 2) return;

    var index = 0;

    function mark(i) {
      index = i;
      dots.forEach(function (d, n) { d.setAttribute("aria-current", n === i ? "true" : "false"); });
      slides.forEach(function (s, n) { s.setAttribute("aria-hidden", n === i ? "false" : "true"); });
    }
    function go(i) {
      i = (i + slides.length) % slides.length;
      track.scrollTo({ left: track.clientWidth * i, behavior: reduce ? "auto" : "smooth" });
      mark(i);
    }

    prev.addEventListener("click", function () { go(index - 1); });
    next.addEventListener("click", function () { go(index + 1); });
    dots.forEach(function (d, n) { d.addEventListener("click", function () { go(n); }); });

    track.addEventListener("keydown", function (e) {
      if (e.key === "ArrowLeft")  { e.preventDefault(); go(index - 1); }
      if (e.key === "ArrowRight") { e.preventDefault(); go(index + 1); }
    });

    /* keep the dots honest when the person swipes or drags instead */
    var t;
    track.addEventListener("scroll", function () {
      clearTimeout(t);
      t = setTimeout(function () {
        var i = Math.round(track.scrollLeft / track.clientWidth);
        if (i !== index) mark(Math.max(0, Math.min(slides.length - 1, i)));
      }, 90);
    }, { passive: true });

    mark(0);
  });
})();


/* ---- Filmstrip: passive drift, drag, seamless loop ---- */
(function(){
  "use strict";
  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  document.querySelectorAll("[data-strip]").forEach(function (strip) {
    var track = strip.querySelector(".strip-track");
    var items = Array.prototype.slice.call(track.children);
    if (!items.length) return;

    items.forEach(function (el, i) { el.setAttribute("data-i", String(i)); });

    /* Clone the whole set once and park it after the originals. The seam
       falls between the last original and the first clone, so what repeats
       is never adjacent to itself — it reads as a continuous strip. */
    var loopWidth = 0, pos = 0;
    items.forEach(function (el) {
      var c = el.cloneNode(true);
      c.setAttribute("data-clone", "1");
      c.setAttribute("aria-hidden", "true");
      c.setAttribute("tabindex", "-1");
      track.appendChild(c);
    });
    function measure() {
      var first = items[0], firstClone = track.children[items.length];
      loopWidth = firstClone ? firstClone.offsetLeft - first.offsetLeft : track.scrollWidth / 2;
    }
    measure();
    window.addEventListener("resize", measure);
    if (window.ResizeObserver) new ResizeObserver(measure).observe(track);

    function normalise() {
      if (!loopWidth) return;
      if (track.scrollLeft >= loopWidth) { track.scrollLeft -= loopWidth; pos = track.scrollLeft; }
      else if (track.scrollLeft < 0)     { track.scrollLeft += loopWidth; pos = track.scrollLeft; }
    }

    /* ---- passive drift ----
       scrollLeft reports whole pixels, so nudging it by a fraction each frame
       rounds straight back and nothing moves. Keep the true position in a
       float and write that instead. */
    var SPEED = 0.28;            // px per frame ≈ 17px/sec. A slow pan, not a slideshow.
    var IDLE  = 2200;            // how long after the last touch before it resumes
    var paused = false, timer = null, raf = null;
    pos = track.scrollLeft;

    function sync() { pos = track.scrollLeft; }

    function hold() {
      paused = true;
      sync();
      clearTimeout(timer);
      timer = setTimeout(function () { sync(); paused = false; }, IDLE);
    }
    function tick() {
      if (!paused && !document.hidden) {
        pos += SPEED;
        if (loopWidth && pos >= loopWidth) pos -= loopWidth;
        track.scrollLeft = pos;
      }
      raf = requestAnimationFrame(tick);
    }

    ["pointerenter","pointerdown","wheel","touchstart","focusin"].forEach(function (ev) {
      track.addEventListener(ev, hold, { passive: true });
    });
    track.addEventListener("pointerleave", function () {
      clearTimeout(timer);
      timer = setTimeout(function () { sync(); paused = false; }, 600);
    });
    track.addEventListener("scroll", function () {
      normalise();
      if (paused) sync();          // the person is driving; follow them
    }, { passive: true });

    /* ---- click-drag for mouse and trackpad ---- */
    var down = false, startX = 0, startLeft = 0, moved = 0;
    track.addEventListener("pointerdown", function (e) {
      if (e.pointerType === "touch") return;      // native scrolling already handles touch
      down = true; moved = 0;
      startX = e.clientX; startLeft = track.scrollLeft;
      track.classList.add("is-dragging");
      track.setPointerCapture(e.pointerId);
    });
    track.addEventListener("pointermove", function (e) {
      if (!down) return;
      var dx = e.clientX - startX;
      moved = Math.max(moved, Math.abs(dx));
      track.scrollLeft = startLeft - dx;
      normalise();
    });
    ["pointerup","pointercancel"].forEach(function (ev) {
      track.addEventListener(ev, function (e) {
        if (!down) return;
        down = false;
        track.classList.remove("is-dragging");
        if (moved > 6) {
          var el = e.target.closest ? e.target.closest(".gitem") : null;
          if (el) el.setAttribute("data-suppress-click", "1");   // don't open the lightbox
        }
        hold();
      });
    });

    if (!reduce) {
      raf = requestAnimationFrame(tick);
      document.addEventListener("visibilitychange", function () {
        if (document.hidden) { cancelAnimationFrame(raf); raf = null; }
        else if (!raf) { raf = requestAnimationFrame(tick); }
      });
    }
  });
})();


/* ---- Card rails: arrows for a native scroll-snap row ---- */
(function(){
  "use strict";
  document.querySelectorAll("[data-rail]").forEach(function (rail) {
    var track = rail.querySelector(".stays");
    var prev  = rail.querySelector(".rail-prev");
    var next  = rail.querySelector(".rail-next");
    if (!track || !prev || !next) return;

    function step() {
      var card = track.querySelector(".stay-card");
      if (!card) return track.clientWidth;
      var gap = parseFloat(getComputedStyle(track).columnGap || getComputedStyle(track).gap) || 0;
      return card.getBoundingClientRect().width + gap;
    }
    function sync() {
      var max = track.scrollWidth - track.clientWidth - 2;
      prev.disabled = track.scrollLeft <= 2;
      next.disabled = track.scrollLeft >= max;
    }
    prev.addEventListener("click", function () { track.scrollBy({ left: -step(), behavior: "smooth" }); });
    next.addEventListener("click", function () { track.scrollBy({ left:  step(), behavior: "smooth" }); });
    track.addEventListener("scroll", sync, { passive: true });
    window.addEventListener("resize", sync);
    sync();
  });
})();


/* ---- Enquiry form ----
   Cloudflare Pages serves static files; it does not process form posts. So
   unless an endpoint has been configured on the form, submitting composes a
   pre-filled email instead of silently throwing the message away. Set
   data-endpoint on the form to POST to a real service later. */
(function(){
  "use strict";
  var form = document.getElementById("enquiry");
  if (!form) return;

  var msg  = document.getElementById("form-msg");
  var mail = form.getAttribute("data-mailto");

  function say(html, bad) {
    msg.innerHTML = html;
    msg.classList.toggle("bad", !!bad);
    msg.hidden = false;
    msg.scrollIntoView({ block: "nearest", behavior: "smooth" });
  }

  var FIELDS = ["name", "email", "phone", "dates", "guests", "message"];
  var LABELS = { name:"Name", email:"Email", phone:"Phone",
                 dates:"Dates", guests:"Guests", message:"Message" };

  function asEmail(fd) {
    var lines = [];
    FIELDS.forEach(function (k) {
      var v = (fd.get(k) || "").toString().trim();
      if (v) lines.push(LABELS[k] + ": " + v);
    });
    return "mailto:" + mail +
           "?subject=" + encodeURIComponent("Booking enquiry — Eagle's Nest Resort") +
           "&body=" + encodeURIComponent(lines.join("\n\n"));
  }

  form.addEventListener("submit", function (e) {
    e.preventDefault();
    if (!form.reportValidity()) return;

    var fd = new FormData(form);
    if ((fd.get("company") || "").toString().trim()) return;   // honeypot tripped

    // read at submit time, so the endpoint can be set without touching the script
    var endpoint = (form.getAttribute("data-endpoint") || "").trim();

    if (!endpoint) {
      window.location.href = asEmail(fd);
      say("<b>Nearly there</b>Your email app should have opened with the details filled in &mdash; press send and it reaches us. If nothing opened, email <a href=\"mailto:" + mail + "\">" + mail + "</a> or ring 250-742-3707.");
      return;
    }

    var btn = form.querySelector("button[type=submit]");
    var label = btn.textContent;
    btn.disabled = true;
    btn.textContent = "Sending\u2026";

    fetch(endpoint, {
      method: "POST",
      headers: { "Content-Type": "application/x-www-form-urlencoded" },
      body: new URLSearchParams(fd).toString()
    }).then(function (r) {
      if (!r.ok) throw new Error(r.status);
      form.reset();
      say("<b>Thank you</b>We&rsquo;ve got your message and will come back to you shortly. If it&rsquo;s urgent, ring us on 250-742-3707.");
    }).catch(function () {
      say("<b>That didn&rsquo;t send</b>We&rsquo;ve opened an email with your details instead &mdash; press send and it reaches us. Or ring 250-742-3707.", true);
      window.location.href = asEmail(fd);
    }).then(function () {
      btn.disabled = false;
      btn.textContent = label;
    });
  });
})();
