// Stills of the prototype: each chapter at rest and the midpoint of each transition.
// usage: node rest.js <desk|tablet|phone|landscape> <outdir> [reduce]
const { chromium, devices } = require('playwright');
(async () => {
  const [mode, out, reduce] = process.argv.slice(2);
  const ctxo = { desk: { viewport: { width: 1440, height: 900 } }, wide: { viewport: { width: 1920, height: 1080 } },
    small: { viewport: { width: 1280, height: 800 } },
    tablet: { viewport: { width: 820, height: 1180 }, deviceScaleFactor: 1, isMobile: true, hasTouch: true },
    phone: { viewport: { width: 390, height: 844 }, deviceScaleFactor: 2, isMobile: true, hasTouch: true },
    landscape: { viewport: { width: 844, height: 390 }, deviceScaleFactor: 2, isMobile: true, hasTouch: true } }[mode];
  const b = await chromium.launch(); const ctx = await b.newContext({ ...ctxo, reducedMotion: reduce ? 'reduce' : 'no-preference' });
  const p = await ctx.newPage();
  await p.goto('http://127.0.0.1:8771/local.html', { waitUntil: 'networkidle' });
  await p.evaluate(() => document.querySelector('.bar').style.display = 'none');
  const g = await p.evaluate(() => ({ vh: innerHeight, max: document.documentElement.scrollHeight - innerHeight,
    tops: [...document.querySelectorAll('.scene')].map(s => s.offsetTop), hs: [...document.querySelectorAll('.scene .content')].map(c => c.offsetHeight) }));
  console.log(mode, JSON.stringify(g), 'screens', ((g.max + g.vh) / g.vh).toFixed(2));
  const shots = [['0-hero', 0]];
  g.tops.forEach((t, i) => { shots.push([`${i + 1}-rest`, t]); if (i) shots.push([`${i}to${i + 1}-mid`, Math.round(t - g.vh * 0.5)]); });
  for (const [name, y] of shots.sort((a, c) => a[1] - c[1])) {
    // step there so every scroll timeline passes through its range
    const cur = await p.evaluate(() => scrollY);
    for (let k = 1; k <= 6; k++) await p.evaluate(v => scrollTo(0, v), Math.round(cur + (y - cur) * k / 6));
    await p.waitForTimeout(350); await p.screenshot({ path: `${out}/${mode}${reduce ? '-rm' : ''}-${name}.png` });
  }
  await b.close();
})();
