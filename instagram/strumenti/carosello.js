const { chromium } = require('playwright');
const path = require('path');
const F = 'file://' + path.resolve(require.resolve('@fontsource/cormorant-garamond/package.json'), '..', 'files/cormorant-garamond-latin');

// Uso: node carosello.js slides.json cartella-output
// Richiede: npm i playwright @fontsource/cormorant-garamond  (font Inter installato nel sistema)
const [,, SLIDES, OUT] = process.argv;
const slides = JSON.parse(require('fs').readFileSync(SLIDES, 'utf8'));
require('fs').mkdirSync(OUT, { recursive: true });
const N = slides.length;

function body(s) {
  switch (s.t) {
    case 'cover': return `<div class="kicker">${s.kicker}</div><h1 class="cover">${s.h}</h1><div class="rule"></div><p class="sub">${s.sub}</p><div class="swipe">Scorri &rarr;</div>`;
    case 'stake': return `<h2 class="big">${s.h}</h2><div class="rule"></div><p>${s.p}</p>`;
    case 'err': return `<div class="num">${s.n}</div><div class="label">${s.label || "Errore"}</div><h2>${s.h}</h2><div class="rule"></div><p>${s.p}</p>`;
    case 'recap': return `<div class="label">Salva questo post</div><h2>${s.h}</h2><ul>${s.items.map((x,i)=>`<li><span>${String(i+1).padStart(2,'0')}</span>${x}</li>`).join('')}</ul>`;
    case 'cta': return `<h2 class="big">${s.h}</h2><div class="rule"></div><p>${s.p}</p><div class="kw">VALUTAZIONE</div>`;
  }
}

const html = `<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{font-family:Corm;src:url(${F}-600-normal.woff2);font-weight:600}
@font-face{font-family:Corm;src:url(${F}-500-normal.woff2);font-weight:500}
*{margin:0;padding:0;box-sizing:border-box;font-variant-numeric:lining-nums}
body{background:#0E1A2B}
section{width:1080px;height:1350px;position:relative;overflow:hidden;
  background:radial-gradient(ellipse at 85% 0%,#1C2D47 0%,#0E1A2B 60%);color:#F2ECE0;font-family:Inter;
  padding:150px 130px;display:flex;flex-direction:column;justify-content:center}
section::before{content:"";position:absolute;inset:48px;border:1.5px solid rgba(201,162,74,.35);pointer-events:none}
.top,.foot{position:absolute;left:130px;right:130px;font-size:28px;letter-spacing:.18em;text-transform:uppercase;color:#C9A24A;display:flex;justify-content:space-between}
.top{top:92px}.foot{bottom:92px;color:rgba(242,236,224,.6)}
.kicker,.label{font-size:32px;letter-spacing:.2em;text-transform:uppercase;color:#C9A24A;margin-bottom:36px;font-weight:500}
h1.cover{font-family:Corm;font-weight:600;font-size:150px;line-height:.98;letter-spacing:-.01em}
h2{font-family:Corm;font-weight:600;font-size:96px;line-height:1.02}
h2.big{font-size:104px}
.rule{width:120px;height:3px;background:#C9A24A;margin:52px 0}
p,.sub{font-size:42px;line-height:1.45;color:rgba(242,236,224,.85);font-weight:300;max-width:780px}
.sub{font-size:46px}
.num{font-family:Corm;font-size:260px;line-height:.8;color:rgba(201,162,74,.22);position:absolute;top:150px;right:120px;font-weight:600}
.swipe{position:absolute;bottom:170px;right:130px;font-size:32px;letter-spacing:.15em;text-transform:uppercase;color:#C9A24A}
ul{list-style:none;margin-top:56px}
li{font-size:44px;padding:26px 0;border-bottom:1px solid rgba(201,162,74,.3);display:flex;gap:34px;font-weight:400}
li span{color:#C9A24A;font-family:Corm;font-weight:600;font-size:46px;min-width:60px}
.kw{margin-top:30px;align-self:flex-start;border:2px solid #C9A24A;color:#C9A24A;padding:22px 44px;font-size:40px;letter-spacing:.22em;font-weight:600}
</style></head><body>
${slides.map((s,i)=>`<section><div class="top"><span>Inkasa Property Management</span><span>${i+1}/${N}</span></div>${body(s)}<div class="foot"><span>inkasa.casa</span></div></section>`).join('')}
</body></html>`;

(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1080, height: 1350 } });
  require('fs').writeFileSync(OUT + '/_c.html', html); await p.goto('file://' + path.resolve(OUT + '/_c.html'));
  await p.evaluate(() => document.fonts.ready);
  const secs = await p.$$('section');
  for (let i = 0; i < secs.length; i++) await secs[i].screenshot({ path: `${OUT}/${String(i+1).padStart(2,'0')}.png` });
  await b.close();
})();
