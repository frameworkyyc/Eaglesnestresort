// screen recording of the real scroll: hold on chapter 4, the takeover, hold on chapter 5, on into the dusk
const { chromium, devices } = require('playwright'); const fs = require('fs');
(async () => {
  const mode = process.argv[2];
  const b = await chromium.launch();
  const base = mode === 'phone' ? { ...devices['iPhone 13'] } : { viewport: { width: 1440, height: 900 }, deviceScaleFactor: 1 };
  const size = mode === 'phone' ? { width: 780, height: 1688 } : { width: 1440, height: 900 };
  const ctx = await b.newContext({ ...base, recordVideo: { dir: 'video/tmp-' + mode, size } });
  const p = await ctx.newPage();
  await p.goto('http://127.0.0.1:8770/local.html', { waitUntil: 'networkidle' });
  await p.waitForTimeout(800);
  const g = await p.evaluate(() => ({ s5: document.getElementById('winter').offsetTop, max: document.documentElement.scrollHeight - innerHeight }));
  // smooth scroll in the page: ease-in-out between waypoints
  await p.evaluate(async ({ s5, max }) => {
    const ease = t => t < .5 ? 2 * t * t : 1 - Math.pow(-2 * t + 2, 2) / 2;
    const go = (a, z, ms) => new Promise(res => { const t0 = performance.now();
      const f = now => { const t = Math.min(1, (now - t0) / ms); scrollTo(0, a + (z - a) * ease(t)); t < 1 ? requestAnimationFrame(f) : res(); };
      requestAnimationFrame(f); });
    const wait = ms => new Promise(r => setTimeout(r, ms));
    await wait(1200); await go(0, s5, 5200); await wait(1600); await go(s5, max, 3600); await wait(1200);
  }, g);
  const v = p.video(); await ctx.close(); fs.renameSync(await v.path(), `video/${mode}.webm`); await b.close();
  console.log(mode, JSON.stringify(g));
})();
