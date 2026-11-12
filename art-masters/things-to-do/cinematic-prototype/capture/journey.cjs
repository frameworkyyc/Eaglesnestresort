// The complete scroll, hero to the end of chapter 5, captured frame by frame and assembled with ffmpeg.
// usage: node journey.cjs <desk|tablet|phone> <framesdir>    (the prototype served at 127.0.0.1:8771/local.html)
const { chromium } = require('playwright');
(async () => {
  const [mode, dir] = process.argv.slice(2);
  const o = { desk: { viewport: { width: 1440, height: 900 }, deviceScaleFactor: 1 },
    tablet: { viewport: { width: 820, height: 1180 }, deviceScaleFactor: 1, isMobile: true, hasTouch: true },
    phone: { viewport: { width: 390, height: 844 }, deviceScaleFactor: 2, isMobile: true, hasTouch: true } }[mode];
  const b = await chromium.launch(); const p = await (await b.newContext(o)).newPage();
  await p.goto('http://127.0.0.1:8771/local.html', { waitUntil: 'networkidle' });
  await p.evaluate(() => document.querySelector('.bar').style.display = 'none');
  // load every lazy layer first, then return to the top
  const H = await p.evaluate(() => document.documentElement.scrollHeight);
  for (let y = 0; y < H; y += 400) { await p.evaluate(v => scrollTo(0, v), y); await p.waitForTimeout(30); }
  await p.evaluate(() => scrollTo(0, 0)); await p.waitForTimeout(600);
  const g = await p.evaluate(() => ({ vh: innerHeight, max: document.documentElement.scrollHeight - innerHeight,
    rest: [...document.querySelectorAll('.scene')].map(s => s.offsetTop) }));
  // waypoints: hold on the hero, then each chapter's rest; chapter 1 on phones also scrolls through its long content
  const pts = [0, ...g.rest.slice(0, 5)]; const content1 = await p.evaluate(() => document.querySelector('.s1 .content').offsetHeight);
  if (content1 > g.vh * 1.1) pts.splice(2, 0, g.rest[0] + content1 - g.vh);
  pts.push(Math.min(g.max, g.rest[5]));
  const fps = 25, ease = t => t < .5 ? 2 * t * t : 1 - Math.pow(-2 * t + 2, 2) / 2;
  let n = 0;
  const shot = async () => { await p.evaluate(() => new Promise(r => requestAnimationFrame(() => requestAnimationFrame(r))));
    await p.screenshot({ path: `${dir}/${String(n++).padStart(5, '0')}.png` }); };
  const hold = async s => { for (let i = 0; i < Math.round(s * fps); i++) await shot(); };
  await hold(1.4);
  for (let i = 1; i < pts.length; i++) {
    const a = pts[i - 1], z = pts[i], sec = Math.max(1.6, 3.4 * Math.abs(z - a) / g.vh), k = Math.round(sec * fps);
    for (let j = 1; j <= k; j++) { await p.evaluate(v => scrollTo(0, v), a + (z - a) * ease(j / k)); await shot(); }
    await hold(i === pts.length - 1 ? 1.2 : 1.5);
  }
  console.log(mode, 'frames', n, JSON.stringify(g)); await b.close();
})();
