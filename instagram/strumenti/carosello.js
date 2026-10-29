// Generatore caroselli Inkasa — 4 temi x 11 tipi di slide, 1080x1350.
// Uso:   NODE_PATH=$(npm root -g):<cartella node_modules> node carosello.js slides.json cartella-output
// Serve: npm i @fontsource/cormorant-garamond   (Playwright e il font Inter sono già nell'ambiente)
//
// slides.json:
// { "theme": "dark" | "cream" | "gold" | "photo",
//   "photo": "percorso/o/url foto di sfondo (solo tema photo, opzionale per slide)",
//   "stock": true  → foto non di Inkasa: aggiunge "Immagine illustrativa" sulle slide con foto,
//   "slides": [ { "t": "<tipo>", ... } ] }
// Tipi (campi):
//   cover   kicker, h, sub                 — copertina, max 6 parole in h
//   stake   h, p                           — perché conta
//   step    n, label, h, p                 — passo / errore numerato (label es. "Passo", "Errore")
//   myth    myth, truth                    — mito barrato + realtà
//   check   h, items[]                     — checklist con caselle spuntate
//   faq     q, a                           — domanda e risposta
//   quote   q, by                          — frase grande (by opzionale)
//   compare h, left{t,items[]}, right{t,items[]} — prima/dopo, da solo/con Inkasa
//   photo   image, h, p                    — foto a tutto schermo con didascalia
//   recap   h, items[]                     — riepilogo da salvare
//   cta     h, p, kw                       — invito finale (kw default VALUTAZIONE)
// Un vecchio slides.json che è un array semplice vale come { theme: "dark", slides: [...] }; "err" = "step".
const { chromium } = require('playwright');
const fs = require('fs'), path = require('path');
const [,, SLIDES, OUT] = process.argv;
let deck = JSON.parse(fs.readFileSync(SLIDES, 'utf8'));
if (Array.isArray(deck)) deck = { theme: 'dark', slides: deck };
const theme = deck.theme || 'dark', slides = deck.slides, N = slides.length;
fs.mkdirSync(OUT, { recursive: true });
const F = 'file://' + path.resolve(require.resolve('@fontsource/cormorant-garamond/package.json'), '..', 'files/cormorant-garamond-latin');
const img = p => !p ? '' : /^https?:/.test(p) ? p : 'file://' + path.resolve(path.dirname(SLIDES), p);
const esc = s => String(s ?? '').replace(/&/g, '&amp;').replace(/</g, '&lt;');

const T = {
  dark:  { bg: 'radial-gradient(ellipse at 85% 0%,#1C2D47 0%,#0E1A2B 60%)', fg: '#F2ECE0', soft: 'rgba(242,236,224,.82)', acc: '#C9A24A', line: 'rgba(201,162,74,.35)', num: 'rgba(201,162,74,.22)', foot: 'rgba(242,236,224,.6)' },
  cream: { bg: 'linear-gradient(160deg,#F7F2E9 0%,#EFE7DA 100%)', fg: '#0E1A2B', soft: 'rgba(14,26,43,.75)', acc: '#A9812F', line: 'rgba(169,129,47,.45)', num: 'rgba(169,129,47,.20)', foot: 'rgba(14,26,43,.55)' },
  gold:  { bg: 'linear-gradient(160deg,#DDBB66 0%,#C49A45 100%)', fg: '#0E1A2B', soft: 'rgba(14,26,43,.82)', acc: '#0E1A2B', line: 'rgba(14,26,43,.35)', num: 'rgba(14,26,43,.14)', foot: 'rgba(14,26,43,.62)' },
  photo: { bg: '#0E1A2B', fg: '#FFFFFF', soft: 'rgba(255,255,255,.88)', acc: '#E2C77E', line: 'rgba(226,199,126,.5)', num: 'rgba(226,199,126,.3)', foot: 'rgba(255,255,255,.7)' },
}[theme];

function body(s) {
  const kw = esc(s.kw || 'VALUTAZIONE');
  switch (s.t === 'err' ? 'step' : s.t) {
    case 'cover': return `<div class="kicker">${esc(s.kicker)}</div><h1 class="cover">${esc(s.h)}</h1><div class="rule"></div><p class="sub">${esc(s.sub)}</p><div class="swipe">Scorri &rarr;</div>`;
    case 'stake': return `<h2 class="big">${esc(s.h)}</h2><div class="rule"></div><p>${esc(s.p)}</p>`;
    case 'step': return `<div class="num">${esc(s.n)}</div><div class="label">${esc(s.label || 'Passo')}</div><h2>${esc(s.h)}</h2><div class="rule"></div><p>${esc(s.p)}</p>`;
    case 'myth': return `<div class="label">Mito</div><h2 class="myth">${esc(s.myth)}</h2><div class="label" style="margin-top:70px">Realtà</div><h2>${esc(s.truth)}</h2>`;
    case 'check': return `<h2>${esc(s.h)}</h2><ul class="chk">${s.items.map(x => `<li><span class="box">&#10003;</span>${esc(x)}</li>`).join('')}</ul>`;
    case 'faq': return `<div class="qmark">?</div><div class="label">Domanda</div><h2>${esc(s.q)}</h2><div class="rule"></div><p>${esc(s.a)}</p>`;
    case 'quote': return `<div class="qq">&ldquo;</div><h2 class="quote">${esc(s.q)}</h2>${s.by ? `<div class="label" style="margin-top:44px">${esc(s.by)}</div>` : ''}`;
    case 'compare': return `<h2>${esc(s.h)}</h2><div class="cmp"><div class="col"><div class="label">${esc(s.left.t)}</div>${s.left.items.map(x => `<div class="ci no">${esc(x)}</div>`).join('')}</div><div class="col yes"><div class="label">${esc(s.right.t)}</div>${s.right.items.map(x => `<div class="ci">${esc(x)}</div>`).join('')}</div></div>`;
    case 'photo': return `<div class="ph-cap"><h2>${esc(s.h)}</h2>${s.p ? `<p>${esc(s.p)}</p>` : ''}</div>`;
    case 'recap': return `<div class="label">Salva questo post</div><h2>${esc(s.h)}</h2><ul class="rc">${s.items.map((x, i) => `<li><span>${String(i + 1).padStart(2, '0')}</span>${esc(x)}</li>`).join('')}</ul>`;
    case 'cta': return `<h2 class="big">${esc(s.h)}</h2><div class="rule"></div><p>${esc(s.p)}</p><div class="kw">${kw}</div>`;
    default: throw new Error('tipo di slide sconosciuto: ' + s.t);
  }
}
function hasPhoto(s) { return !!(s.image || (theme === 'photo' && (s.t === 'photo' || s.t === 'cover') && deck.photo)); }
function sectionStyle(s) {
  const ph = s.image || (theme === 'photo' && (s.t === 'photo' || s.t === 'cover') ? deck.photo : '');
  if (!ph) return '';
  const grad = s.t === 'photo' ? 'linear-gradient(180deg,rgba(8,14,26,.15) 35%,rgba(8,14,26,.88) 100%)' : 'linear-gradient(180deg,rgba(8,14,26,.35) 0%,rgba(8,14,26,.8) 100%)';
  return ` style="background:${grad},url('${img(ph)}') center/cover"`;
}
const html = `<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{font-family:Corm;src:url(${F}-600-normal.woff2);font-weight:600}
@font-face{font-family:Corm;src:url(${F}-500-normal.woff2);font-weight:500}
*{margin:0;padding:0;box-sizing:border-box;font-variant-numeric:lining-nums}
section{width:1080px;height:1350px;position:relative;overflow:hidden;background:${T.bg};color:${T.fg};font-family:Inter;
  padding:150px 130px;display:flex;flex-direction:column;justify-content:center}
section::before{content:"";position:absolute;inset:48px;border:1.5px solid ${T.line};pointer-events:none}
section.t-photo{justify-content:flex-end;padding-bottom:190px}
section.t-photo::before{border-color:rgba(255,255,255,.35)}
.top,.foot{position:absolute;left:130px;right:130px;font-size:28px;letter-spacing:.18em;text-transform:uppercase;color:${T.acc};display:flex;justify-content:space-between}
.top{top:92px}.foot{bottom:92px;color:${T.foot}}
.kicker,.label{font-size:32px;letter-spacing:.2em;text-transform:uppercase;color:${T.acc};margin-bottom:36px;font-weight:500}
h1.cover{font-family:Corm;font-weight:600;font-size:150px;line-height:.98}
h2{font-family:Corm;font-weight:600;font-size:96px;line-height:1.02}
h2.big{font-size:104px}
h2.myth{text-decoration:line-through;text-decoration-color:${T.acc};text-decoration-thickness:6px;opacity:.55;font-size:84px}
h2.quote{font-size:110px;font-style:italic;font-weight:500;line-height:1.02}
.qq{font-family:Corm;font-size:300px;line-height:.5;color:${T.acc};height:120px}
.qmark{font-family:Corm;font-size:300px;line-height:.8;color:${T.num};position:absolute;top:130px;right:120px;font-weight:600}
.rule{width:120px;height:3px;background:${T.acc};margin:52px 0}
p,.sub{font-size:42px;line-height:1.45;color:${T.soft};font-weight:300;max-width:800px}
.sub{font-size:46px}
.num{font-family:Corm;font-size:260px;line-height:.8;color:${T.num};position:absolute;top:150px;right:120px;font-weight:600}
.swipe{position:absolute;bottom:170px;right:130px;font-size:32px;letter-spacing:.15em;text-transform:uppercase;color:${T.acc}}
ul{list-style:none;margin-top:56px}
ul.rc li{font-size:44px;padding:26px 0;border-bottom:1px solid ${T.line};display:flex;gap:34px}
ul.rc li span{color:${T.acc};font-family:Corm;font-weight:600;font-size:46px;min-width:60px}
ul.chk li{font-size:44px;padding:22px 0;display:flex;align-items:center;gap:30px}
.box{width:56px;height:56px;border:2.5px solid ${T.acc};border-radius:10px;display:inline-flex;align-items:center;justify-content:center;color:${T.acc};font-size:36px;flex:none}
.cmp{display:flex;gap:40px;margin-top:60px}
.col{flex:1;border:1.5px solid ${T.line};padding:40px 34px}
.col.yes{border-color:${T.acc};background:${theme === 'cream' ? 'rgba(169,129,47,.07)' : theme === 'gold' ? 'rgba(14,26,43,.07)' : 'rgba(201,162,74,.08)'}}
.ci{font-size:36px;line-height:1.3;padding:16px 0;border-bottom:1px solid ${T.line}}
.ci.no{opacity:.6;text-decoration:line-through;text-decoration-color:${T.acc}}
.ph-cap h2{font-size:92px;text-shadow:0 4px 30px rgba(0,0,0,.35)}
.ph-cap p{margin-top:24px}
.ill{position:absolute;right:130px;bottom:94px;font-size:20px;letter-spacing:.12em;text-transform:uppercase;color:rgba(255,255,255,.6)}
.kw{margin-top:30px;align-self:flex-start;border:2px solid ${T.acc};color:${T.acc};padding:22px 44px;font-size:40px;letter-spacing:.22em;font-weight:600}
</style></head><body>
${slides.map((s, i) => `<section class="t-${s.t}"${sectionStyle(s)}><div class="top"><span>Inkasa Property Management</span><span>${i + 1}/${N}</span></div>${body(s)}<div class="foot"><span>inkasa.casa</span></div>${deck.stock && hasPhoto(s) ? '<div class="ill">Immagine illustrativa</div>' : ''}</section>`).join('\n')}
</body></html>`;

(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1080, height: 1350 } });
  fs.writeFileSync(OUT + '/_c.html', html);
  await p.goto('file://' + path.resolve(OUT + '/_c.html'), { waitUntil: 'networkidle' });
  await p.evaluate(() => document.fonts.ready);
  const secs = await p.$$('section');
  for (let i = 0; i < secs.length; i++) await secs[i].screenshot({ path: `${OUT}/${String(i + 1).padStart(2, '0')}.png` });
  await b.close();
  fs.unlinkSync(OUT + '/_c.html');
  console.log('slide', secs.length, 'tema', theme);
})();
