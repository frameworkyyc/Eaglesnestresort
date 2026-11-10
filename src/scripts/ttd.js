/* Things To Do: review tools for Phase 1, plus small layout helpers.
   ?slots  outlines every empty artwork slot with its code.
   ?ref    lays the approved reference image over the page (?ref=0.4 sets opacity; a slider adjusts it). */
(() => {
  const main = document.querySelector(".fg");
  if (!main) return;
  const q = new URLSearchParams(location.search);

  if (q.has("slots")) main.classList.add("fg-showslots");

  if (q.has("ref")) {
    const img = new Image();
    img.src = "/assets/ttd/reference.jpg";
    img.alt = "";
    img.setAttribute("aria-hidden", "true");
    const op = parseFloat(q.get("ref")) || 0.5;
    const place = () => {
      const rp = Math.min(innerWidth, 1920) / 729;
      const top = main.getBoundingClientRect().top + scrollY - 62 * rp; // the reference includes its own 62 px nav
      Object.assign(img.style, { position: "absolute", left: "0", top: `${top}px`, width: `${729 * rp}px`,
        opacity: String(op), zIndex: "9999", pointerEvents: "none" });
    };
    document.body.appendChild(img);
    place();
    addEventListener("resize", place);
    const s = document.createElement("input");
    Object.assign(s, { type: "range", min: "0", max: "1", step: "0.05", value: String(op), className: "fg-refslider" });
    s.setAttribute("aria-label", "Reference overlay opacity");
    s.addEventListener("input", () => { img.style.opacity = s.value; });
    document.body.appendChild(s);
  }

  // phones: open the pannable map centred on the lake
  const ms = main.querySelector(".fg-mapscroll");
  if (ms && ms.scrollWidth > ms.clientWidth) ms.scrollLeft = (ms.scrollWidth - ms.clientWidth) / 2;
})();
