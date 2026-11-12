// The scroll from chapter 2 at rest, through chapter 3, to chapter 4 at rest, captured frame by frame.
// usage: node transitions.cjs <desk|tablet|phone> <framesdir>   (prototype served at 127.0.0.1:8771/local.html)
const { chromium } = require('playwright');
(async () => {
  const [mode, dir] = process.argv.slice(2);
  const o = { desk: { viewport: { width: 1440, height: 900 }, deviceScaleFactor: 1 },
    tablet: { viewport: { width: 820, height: 1180 }, deviceScaleFactor: 1, isMobile: true, hasTouch: true },
    phone: { viewport: { width: 390, height: 844 }, deviceScaleFactor: 2, isMobile: true, hasTouch: true } }[mode];
  const b = await chromium.launch(); const p = await (await b.newContext(o)).newPage();
  await p.goto('http://127.0.0.1:8771/local.html', { waitUntil: 'networkidle' });
  await p.evaluate(() => document.querySelector('.bar').style.display = 'none');
  const H = await p.evaluate(() => document.documentElement.scrollHeight);
  for (let y = 0; y < H; y += 400) { await p.evaluate(v => scrollTo(0, v), y); await p.waitForTimeout(25); }
  const g = await p.evaluate(() => ({ vh: innerHeight, rest: [...document.querySelectorAll('.scene')].map(s => s.offsetTop) }));
  // warm-up: visit every chapter and decode every image, so the frame-by-frame capture never shows an undecoded layer
  for (const y of g.rest) { await p.evaluate(v => scrollTo(0, v), y); await p.waitForTimeout(400); }
  await p.evaluate(() => Promise.race([Promise.all([...document.querySelectorAll('.ly img')].map(i => i.decode().catch(() => {}))), new Promise(r => setTimeout(r, 8000))]));
  const [r2, r3, r4] = [g.rest[1], g.rest[2], g.rest[3]];
  for (let k = 1; k <= 10; k++) { await p.evaluate(v => scrollTo(0, v), Math.round(r2 * k / 10)); await p.waitForTimeout(30); }
  await p.waitForTimeout(500);
  const fps = 25, ease = t => t < .5 ? 2 * t * t : 1 - Math.pow(-2 * t + 2, 2) / 2; let n = 0;
  const shot = async () => { await p.evaluate(() => new Promise(r => requestAnimationFrame(() => requestAnimationFrame(r))));
    await p.screenshot({ path: `${dir}/${String(n++).padStart(5, '0')}.png` }); };
  const hold = async s => { for (let i = 0; i < Math.round(s * fps); i++) await shot(); };
  const go = async (a, z, s) => { const k = Math.round(s * fps); for (let j = 1; j <= k; j++) { await p.evaluate(v => scrollTo(0, v), a + (z - a) * ease(j / k)); await shot(); } };
  await hold(1.2); await go(r2, r3, 4.4); await hold(1.8); await go(r3, r4, 4.4); await hold(1.4);
  console.log(mode, 'frames', n, JSON.stringify({ r2, r3, r4 })); await b.close();
})();
