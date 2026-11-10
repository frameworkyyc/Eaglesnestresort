/* Eagle's Nest: one small script. Every feature is an enhancement; the page reads and works without it. */
const reduce = matchMedia("(prefers-reduced-motion: reduce)").matches;
const $ = (s, c = document) => c.querySelector(s);
const $$ = (s, c = document) => [...c.querySelectorAll(s)];

/* ---- Quiet mode: a visible switch, remembered on this device ---- */
(() => {
  const btn = $("[data-quiet-toggle]");
  const set = (on) => {
    document.body.toggleAttribute("data-quiet", on);
    if (btn) btn.setAttribute("aria-pressed", String(on));
    try { localStorage.setItem("en-quiet", on ? "1" : "0"); } catch {}
  };
  let saved = false;
  try { saved = localStorage.getItem("en-quiet") === "1"; } catch {}
  if (saved) set(true);
  btn?.addEventListener("click", () => set(btn.getAttribute("aria-pressed") !== "true"));
})();

/* ---- Only what is on screen animates ---- */
(() => {
  const els = $$("[data-live]");
  if (!("IntersectionObserver" in window)) return els.forEach((e) => e.classList.add("is-live"));
  const io = new IntersectionObserver((en) => en.forEach((e) => e.target.classList.toggle("is-live", e.isIntersecting)), { rootMargin: "120px 0px" });
  els.forEach((e) => io.observe(e));
})();

/* ---- Season switch: the landscape changes, every activity stays on the page ---- */
(() => {
  const root = $("[data-season-root]");
  if (!root) return;
  const btns = $$("[data-season-btn]", root);
  const snow = $("[data-snow]", root);
  if (snow && !reduce) {
    const n = innerWidth < 700 ? 16 : 30;
    for (let i = 0; i < n; i++) {
      const f = document.createElement("i");
      f.style.cssText = `--x:${(Math.random() * 100).toFixed(1)}%;--s:${(3 + Math.random() * 5).toFixed(1)}px;--t:${(9 + Math.random() * 10).toFixed(1)}s;--d:-${(Math.random() * 14).toFixed(1)}s;--dx:${(Math.random() * 60 - 30).toFixed(0)}px`;
      snow.appendChild(f);
    }
    snow.style.containerType = "size";
  }
  const set = (season) => {
    root.dataset.season = season;
    btns.forEach((b) => b.setAttribute("aria-pressed", String(b.dataset.seasonBtn === season)));
  };
  btns.forEach((b) => b.addEventListener("click", () => set(b.dataset.seasonBtn)));
})();

/* ---- Highway 20 map: pins, and an eagle that flies the road as you scroll ---- */
(() => {
  const map = $("[data-map]");
  if (!map) return;
  const inner = $(".map__inner", map), path = $("#route-path", map), eagle = $("[data-map-eagle]", map);
  const pins = $$(".pin", map), cards = $$("[data-stop-card]");
  const stops = { bella: 0, home: 136 / 456, williams: 1 };
  const len = path.getTotalLength();
  const place = (t) => {
    t = Math.min(1, Math.max(0, t));
    const a = path.getPointAtLength(len * t), b = path.getPointAtLength(Math.min(len, len * t + 4));
    const k = inner.clientWidth / 1000, kv = inner.clientHeight / 430;
    const ang = Math.max(-18, Math.min(18, Math.atan2((b.y - a.y) * kv, (b.x - a.x) * k) * 180 / Math.PI));
    const ew = eagle.offsetWidth;
    eagle.style.left = "0"; eagle.style.top = "0";
    eagle.style.transform = `translate(${a.x * k - ew / 2}px, ${a.y * kv - ew * 1.35}px) rotate(${ang}deg)`;
  };
  const activate = (key) => {
    pins.forEach((p) => p.setAttribute("aria-pressed", String(p.dataset.stop === key)));
    cards.forEach((c) => c.classList.toggle("is-active", c.dataset.stopCard === key));
    place(stops[key]);
  };
  pins.forEach((p) => p.addEventListener("click", () => activate(p.dataset.stop)));
  cards.forEach((c) => c.addEventListener("click", () => activate(c.dataset.stopCard)));
  place(stops.home);
  if (reduce) return;
  let ticking = false;
  const onScroll = () => {
    if (ticking) return; ticking = true;
    requestAnimationFrame(() => {
      ticking = false;
      const r = map.getBoundingClientRect(), vh = innerHeight;
      if (r.bottom < -50 || r.top > vh + 50) return;
      const p = Math.min(1, Math.max(0, (vh - r.top) / (vh + r.height))); // 0 entering, 1 leaving
      place(1 - p); // flies west, from Williams Lake toward Bella Coola, as you scroll down
    });
  };
  addEventListener("scroll", onScroll, { passive: true });
  addEventListener("resize", onScroll);
  onScroll();
})();

/* ---- The fox peeks toward your pointer ---- */
(() => {
  const fox = $("[data-tilt]");
  if (!fox || reduce || !matchMedia("(pointer: fine)").matches) return;
  let raf = 0;
  addEventListener("pointermove", (e) => {
    if (raf) return;
    raf = requestAnimationFrame(() => {
      raf = 0;
      const r = fox.getBoundingClientRect();
      if (r.bottom < 0 || r.top > innerHeight) return;
      const dx = (e.clientX - (r.left + r.width / 2)) / innerWidth;
      fox.style.translate = `${(dx * 14).toFixed(1)}px 0`;
      fox.style.rotate = `${Math.max(-6, Math.min(6, dx * 16)).toFixed(1)}deg`;
    });
  }, { passive: true });
})();
