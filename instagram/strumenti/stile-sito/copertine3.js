// Copertine allineate al sito nuovo (inkasa-two.vercel.app): bianco/nero, Switzer stretto, numeri giganti,
// colonna centrale nera con numero, colonne laterali foto piena luminosa.
const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');
const STOCK = path.resolve(__dirname, '../../media/stock') + '/';
const SW = 'file://' + path.resolve(__dirname, 'node_modules/@carrot-kpi/switzer-font/files/switzer-latin');
const AR = 'file://' + path.resolve(__dirname, 'node_modules/@fontsource-variable/archivo/files/archivo-latin-wdth-normal.woff2');
const covers = [
  { d: '2026-11-27', k: 'photo', h: 'La tua casa è pronta<br>per gli affitti brevi?', img: '31817156.jpg', pos: '50% 50%' },
  { d: '2026-11-23', k: 'black', n: '5.', h: 'Dettagli che gli ospiti<br>notano subito' },
  { d: '2026-11-20', k: 'photo', h: 'La casa lavora.<br>Tu no.', img: '19836798.jpg', pos: '50% 50%' },
  { d: '2026-11-16', k: 'photo', h: 'Da solo o con Inkasa?', img: '22469110.jpg', pos: '50% 50%' },
  { d: '2026-11-13', k: 'black', n: '3.', h: 'Falsi miti sugli<br>affitti brevi' },
  { d: '2026-11-09', k: 'photo', h: 'Checklist prima<br>di affittare', img: '6920614.jpg', pos: '50% 50%' },
  { d: '2026-11-06', k: 'photo', h: 'La tua casa,<br>gestita da noi', img: '2227832.jpg', pos: '50% 50%' },
  { d: '2026-11-02', k: 'black', n: '5.', h: 'Errori che ti<br>costano soldi' },
];
const html = c => `<!DOCTYPE html><html><head><style>
@font-face{font-family:Sw;src:url(${SW}-500-normal.woff2);font-weight:500}
@font-face{font-family:Sw;src:url(${SW}-600-normal.woff2);font-weight:600}
@font-face{font-family:Sw;src:url(${SW}-700-normal.woff2);font-weight:700}
@font-face{font-family:Ar;src:url(${AR});font-weight:100 900;font-stretch:62% 125%}
*{margin:0;padding:0;box-sizing:border-box}
body{width:1080px;height:1350px;position:relative;overflow:hidden;font-family:Sw;color:#fff;background:#000}
.ph{position:absolute;inset:0;background:url('file://${STOCK}${c.img}') ${c.pos}/cover;filter:saturate(.9) contrast(1.03)}
.g1{position:absolute;left:0;right:0;top:0;height:260px;background:linear-gradient(rgba(0,0,0,.35),rgba(0,0,0,0))}
.g2{position:absolute;left:0;right:0;bottom:0;height:620px;background:linear-gradient(rgba(0,0,0,0),rgba(0,0,0,.62))}
.top{position:absolute;top:70px;left:90px;right:90px}
.wm{font-family:Ar;font-stretch:125%;font-weight:800;font-size:46px;letter-spacing:-.01em;line-height:1}
.rule{height:2px;background:currentColor;margin-top:22px;opacity:.9}
.photo h1{position:absolute;left:90px;right:90px;bottom:120px;font-weight:500;font-size:96px;line-height:.9;letter-spacing:-.07em}
.black .rule{opacity:1}
.black h1{position:absolute;left:90px;right:90px;top:180px;font-weight:500;font-size:104px;line-height:.88;letter-spacing:-.07em}
.num{position:absolute;left:78px;bottom:70px;font-weight:700;font-size:560px;line-height:.78;letter-spacing:-.065em}
.ill{position:absolute;right:90px;bottom:62px;font:500 17px Sw;letter-spacing:.1em;text-transform:uppercase;color:rgba(255,255,255,.65)}
</style></head><body class="${c.k}">
${c.k === 'photo' ? `<div class="ph"></div><div class="g1"></div><div class="g2"></div>` : ''}
<div class="top"><div class="wm">INKASA</div><div class="rule"></div></div>
<h1>${c.h}</h1>
${c.k === 'black' ? `<div class="num">${c.n}</div>` : '<div class="ill">Immagine illustrativa</div>'}
</body></html>`;
(async () => {
  fs.mkdirSync(path.join(__dirname, 'out3'), { recursive: true });
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1080, height: 1350 } });
  for (const c of covers) {
    fs.writeFileSync(path.join(__dirname, 'tmp.html'), html(c));
    await p.goto('file://' + path.join(__dirname, 'tmp.html'));
    await p.evaluate(() => document.fonts.ready);
    await p.screenshot({ path: path.join(__dirname, 'out3', c.d + '.jpg'), type: 'jpeg', quality: 92 });
  }
  await b.close();
})();
