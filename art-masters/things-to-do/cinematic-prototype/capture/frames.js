// phone: the real page scrolled step by step and captured each frame at 2x (390 x 844 CSS px)
const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch();
  const ctx = await b.newContext({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 2, isMobile: true, hasTouch: true });
  const p = await ctx.newPage();
  await p.goto('http://127.0.0.1:8770/local.html', { waitUntil: 'networkidle' }); await p.waitForTimeout(600);
  const g = await p.evaluate(() => ({ s5: document.getElementById('winter').offsetTop, max: document.documentElement.scrollHeight - innerHeight }));
  const fps = 25, ease = t => t < .5 ? 2 * t * t : 1 - Math.pow(-2 * t + 2, 2) / 2;
  const plan = [[0, 0, 1.2], [0, g.s5, 5.2], [g.s5, g.s5, 1.6], [g.s5, g.max, 3.6], [g.max, g.max, 1.2]];
  let n = 0;
  for (const [a, z, sec] of plan) {
    const k = Math.round(sec * fps);
    for (let i = 0; i < k; i++) {
      const y = a + (z - a) * ease(k > 1 ? i / (k - 1) : 1);
      await p.evaluate(y => scrollTo(0, y), y);
      await p.evaluate(() => new Promise(r => requestAnimationFrame(() => requestAnimationFrame(r))));
      await p.screenshot({ path: `video/pf/${String(n++).padStart(4, '0')}.png` });
    }
  }
  console.log('frames', n, JSON.stringify(g)); await b.close();
})();
