// stills at fixed fractions of the chapter 4 -> 5 takeover (and into the dusk), for checking before video
const { chromium, devices } = require('playwright');
(async () => {
  const [mode, out] = [process.argv[2], process.argv[3]];
  const b = await chromium.launch();
  const ctx = mode === 'phone' ? await b.newContext({ ...devices['iPhone 13'] }) : await b.newContext({ viewport: { width: 1440, height: 900 }, deviceScaleFactor: 1 });
  const p = await ctx.newPage();
  await p.goto('http://127.0.0.1:8770/local.html', { waitUntil: 'networkidle' });
  await p.waitForTimeout(500);
  const g = await p.evaluate(() => { const s5 = document.getElementById('winter'); return { vh: innerHeight, s5: s5.offsetTop, H: document.documentElement.scrollHeight,
      sup: CSS.supports('animation-timeline: view()') }; });
  console.log(JSON.stringify(g));
  // entry of chapter 5 runs from scroll = s5top - vh to s5top
  const marks = [0, .2, .4, .6, .8, 1].map(t => Math.round(g.s5 - g.vh + t * g.vh));
  const shots = [];
  for (const [i, y] of marks.entries()) {
    await p.evaluate(y => scrollTo(0, y), y); await p.waitForTimeout(350);
    await p.screenshot({ path: `${out}-${i}.png` }); shots.push(y);
  }
  console.log('scroll marks', shots.join(','));
  await b.close();
})();
