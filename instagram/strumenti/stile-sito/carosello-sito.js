// Slide interne dei caroselli nello stile del sito nuovo (inkasa-two.vercel.app):
// bianco/nero, Switzer stretto, marchio INKASA con riga, numeri giganti, foto piene.
// Uso: node carosello-sito.js slides.json copertina.jpg cartella-uscita
const { chromium } = require('playwright');
const fs = require('fs'), path = require('path');
const [, , SLIDES, COVER, OUT] = process.argv;
const deck = JSON.parse(fs.readFileSync(SLIDES, 'utf8'));
const base = path.dirname(path.resolve(SLIDES));
const SW = 'file://' + path.resolve(__dirname, 'node_modules/@carrot-kpi/switzer-font/files/switzer-latin');
const AR = 'file://' + path.resolve(__dirname, 'node_modules/@fontsource-variable/archivo/files/archivo-latin-wdth-normal.woff2');
const esc = s => String(s ?? '').replace(/&/g, '&amp;').replace(/</g, '&lt;');
const img = p => 'file://' + path.resolve(base, p);
const swap = deck.swap || {};
const pic = p => img(swap[path.basename(p)] ? '../../../media/stock/' + swap[path.basename(p)] : p);
let slides = deck.slides.slice();
// la prima slide è la copertina nuova (già renderizzata)
slides[0] = { t: '__cover' };
const N = slides.length;
const ILL = '<div class="ill">Immagine illustrativa</div>';
const head = (i, dark) => `<div class="top"><div class="row"><span class="wm">INKASA</span><span class="pg">${i + 1}/${N}</span></div><div class="rule"></div></div>`;
const num = n => `${parseInt(n, 10)}.`;

function body(s, i) {
  switch (s.t) {
    case 'stake':
      return { dark: true, html: (s.img ? `<div class="hero" style="background-image:url('${pic(s.img)}')"></div><div class="veil"></div>` : '') +
        `${head(i)}<div class="mid"><h2 class="xl">${esc(s.h)}</h2><p class="lead">${esc(s.p)}</p></div>${s.img ? ILL : ''}` };
    case 'err': case 'step':
      return { dark: false, html: `${head(i)}<div class="label">${esc(s.label || '')}</div><h2>${esc(s.h)}</h2><p class="txt">${esc(s.p)}</p>` +
        (s.img ? `<div class="side" style="background-image:url('${pic(s.img)}')"></div>${ILL}` : '') + `<div class="num${s.img ? '' : ' big'}">${num(s.n)}</div>` };
    case 'myth':
      return { dark: false, html: `${head(i)}<div class="label">Mito</div><h2 class="myth">${esc(s.myth)}</h2><div class="label mt">Realtà</div><h2 class="truth">${esc(s.truth)}</h2><div class="num big">${i}.</div>` };
    case 'faq':
      return { dark: false, html: `${head(i)}<div class="label">Domanda</div><h2>${esc(s.q)}</h2><p class="txt">${esc(s.a)}</p>` +
        (s.img ? `<div class="side" style="background-image:url('${pic(s.img)}')"></div>${ILL}` : '') + `<div class="num${s.img ? '' : ' big'}">${i}.</div>` };
    case 'check':
      return { dark: false, html: `${head(i)}<h2>${esc(s.h)}</h2><ul class="list">${s.items.map((x, k) => `<li><span>${String(k + 1).padStart(2, '0')}</span>${esc(x)}</li>`).join('')}</ul>` +
        (s.img ? `<div class="strip" style="background-image:url('${pic(s.img)}')"></div>${ILL}` : '') };
    case 'recap':
      return { dark: false, html: `${head(i)}<div class="label">Da salvare</div><h2>${esc(s.h)}</h2><ul class="list">${s.items.map((x, k) => `<li><span>${String(k + 1).padStart(2, '0')}</span>${esc(x)}</li>`).join('')}</ul>` };
    case 'compare':
      const col = (c, cls) => `<div class="cc ${cls}"><div class="ct">${esc(c.t)}</div>${c.items.map(x => `<div class="ci">${esc(x)}</div>`).join('')}</div>`;
      return { dark: false, html: `${head(i)}<h2>${esc(s.h)}</h2><div class="cmp">${col(s.left, 'l')}${col(s.right, 'r')}</div>` };
    case 'photo':
      return { dark: true, html: `<div class="hero" style="background-image:url('${pic(s.image)}')"></div><div class="grad"></div>${head(i)}<div class="bot"><h2 class="xl">${esc(s.h)}</h2><p class="lead">${esc(s.p)}</p></div>${ILL}` };
    case 'quote':
      return { dark: true, html: (s.img ? `<div class="hero" style="background-image:url('${pic(s.img)}')"></div><div class="grad"></div>` : '') +
        `${head(i)}<div class="${s.img ? 'bot' : 'mid'}"><h2 class="xxl">${esc(s.q)}</h2></div>${s.img ? ILL : ''}` };
    case 'cta':
      return { dark: true, html: `${head(i)}<div class="mid up"><h2 class="xl">${esc(s.h)}</h2><p class="lead">${esc(s.p)}</p><div class="btn">${esc(s.kw || 'VALUTAZIONE')}</div></div><div class="foot">INKASA</div>` };
  }
  throw new Error('tipo sconosciuto ' + s.t);
}

const css = `
@font-face{font-family:Sw;src:url(${SW}-400-normal.woff2);font-weight:400}
@font-face{font-family:Sw;src:url(${SW}-500-normal.woff2);font-weight:500}
@font-face{font-family:Sw;src:url(${SW}-700-normal.woff2);font-weight:700}
@font-face{font-family:Ar;src:url(${AR});font-weight:100 900;font-stretch:62% 125%}
*{margin:0;padding:0;box-sizing:border-box}
body{width:1080px;height:1350px;position:relative;overflow:hidden;font-family:Sw;background:#fff;color:#000;display:flow-root}
body.dark{background:#000;color:#fff}
.top{position:absolute;top:70px;left:90px;right:90px;z-index:3}
.row{display:flex;justify-content:space-between;align-items:flex-end}
.wm{font-family:Ar;font-stretch:125%;font-weight:800;font-size:46px;line-height:1;letter-spacing:-.01em}
.pg{font-weight:500;font-size:30px;letter-spacing:-.03em}
.rule{height:2px;background:currentColor;margin-top:22px}
.label{position:relative;z-index:2;margin:220px 90px 0;font-weight:500;font-size:30px;letter-spacing:-.02em;color:#808080}
.label.mt{margin-top:60px}
h2{position:relative;z-index:2;margin:18px 90px 0;font-weight:500;font-size:96px;line-height:.9;letter-spacing:-.07em}
body > h2:first-of-type{}
.top + h2{margin-top:220px}
h2.myth{color:#9a9a9a;text-decoration:line-through;text-decoration-thickness:5px;font-size:82px}
h2.truth{font-size:82px}
.txt{position:relative;z-index:2;margin:44px 90px 0;font-size:38px;line-height:1.22;letter-spacing:-.03em;max-width:820px}
.num{position:absolute;left:78px;bottom:70px;font-weight:700;font-size:330px;line-height:.78;letter-spacing:-.065em;z-index:2}
.num.big{font-size:520px}
.side{position:absolute;right:0;bottom:0;width:560px;height:620px;background:center/cover}
.side + .ill, .strip + .ill{color:rgba(255,255,255,.75)}
.strip{position:absolute;left:0;right:0;bottom:0;height:380px;background:center/cover}
.hero{position:absolute;inset:0;background:center/cover}
.veil{position:absolute;inset:0;background:rgba(0,0,0,.6)}
.grad{position:absolute;inset:0;background:linear-gradient(rgba(0,0,0,.35) 0,rgba(0,0,0,0) 22%,rgba(0,0,0,0) 45%,rgba(0,0,0,.7) 100%)}
.mid{position:absolute;left:0;right:0;top:50%;transform:translateY(-50%);z-index:2}
.mid.up{transform:translateY(-62%)}
.bot{position:absolute;left:0;right:0;bottom:130px;z-index:2}
.mid h2,.bot h2{margin-top:0}
h2.xl{font-size:110px;line-height:.88}
h2.xxl{font-size:132px;line-height:.86}
.lead{margin:44px 90px 0;font-size:40px;line-height:1.22;letter-spacing:-.03em;max-width:840px;opacity:.9}
.list{list-style:none;margin:60px 90px 0;position:relative;z-index:2}
.list li{display:flex;gap:40px;font-weight:500;font-size:48px;letter-spacing:-.05em;padding:26px 0;border-top:2px solid #000;line-height:1.05}
.list li:last-child{border-bottom:2px solid #000}
.list li span{color:#808080;min-width:60px}
.strip ~ .list li, .list li{}
.cmp{display:grid;grid-template-columns:1fr 1fr;gap:0;margin:70px 90px 0;border-top:2px solid #000}
.cc{padding:30px 0}
.cc.l{padding-right:30px;border-right:2px solid #000;color:#808080}
.cc.r{padding-left:36px}
.ct{font-weight:700;font-size:40px;letter-spacing:-.05em;margin-bottom:30px;color:#000}
.cc.l .ct{color:#808080}
.ci{font-weight:500;font-size:40px;letter-spacing:-.05em;line-height:1.08;padding:20px 0;border-bottom:1px solid #ccc}
.btn{display:inline-block;margin:60px 90px 0;background:#fff;color:#000;border-radius:8px;padding:22px 40px;font-weight:500;font-size:40px;letter-spacing:-.04em}
.foot{position:absolute;left:-40px;right:-40px;bottom:-52px;white-space:nowrap;font-family:Ar;font-stretch:125%;font-weight:900;font-size:228px;line-height:1;text-align:center;letter-spacing:-.03em;
  background:linear-gradient(#fff,rgba(255,255,255,.08));-webkit-background-clip:text;color:transparent}
.ill{position:absolute;right:90px;bottom:62px;font-size:17px;letter-spacing:.1em;text-transform:uppercase;color:rgba(255,255,255,.65);z-index:3;font-weight:500}
`;

(async () => {
  fs.mkdirSync(OUT, { recursive: true });
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1080, height: 1350 } });
  for (let i = 0; i < N; i++) {
    const out = path.join(OUT, String(i + 1).padStart(2, '0') + '.jpg');
    if (slides[i].t === '__cover') { fs.copyFileSync(COVER, out); continue; }
    const r = body(slides[i], i);
    const tmp = path.join(__dirname, 'tmp-slide.html');
    fs.writeFileSync(tmp, `<!DOCTYPE html><html><head><meta charset="utf-8"><style>${css}</style></head><body class="${r.dark ? 'dark' : ''}">${r.html}</body></html>`);
    await p.goto('file://' + tmp);
    await p.evaluate(() => document.fonts.ready);
    const over = await p.evaluate(() => [...document.querySelectorAll('h2,.txt,.list,.cmp,.lead')].some(e => e.getBoundingClientRect().bottom > 1290));
    if (over) console.log('ATTENZIONE testo lungo:', OUT, i + 1);
    await p.screenshot({ path: out, type: 'jpeg', quality: 90 });
  }
  await b.close();
})();
