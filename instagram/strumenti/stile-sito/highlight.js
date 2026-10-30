const { chromium } = require('playwright');
const path = require('path'), fs = require('fs');
const SW = 'file://' + path.resolve(__dirname, 'node_modules/@carrot-kpi/switzer-font/files/switzer-latin');
const S = 'fill="none" stroke="#fff" stroke-width="9" stroke-linecap="round" stroke-linejoin="round"';
const items = [
  ['01-servizi', 'Servizi', `<svg viewBox="0 0 200 200" ${S}><path d="M30 170h140"/><path d="M45 170V95l55-40 55 40v75"/><path d="M85 170v-40h30v40"/></svg>`],
  ['02-come-lavoriamo', 'Come lavoriamo', `<svg viewBox="0 0 200 200" ${S}><path d="M40 35l120 130"/><path d="M20 35h20"/><path d="M80 78h20"/><path d="M120 121h20"/><circle cx="160" cy="165" r="3" fill="#fff"/></svg>`],
  ['03-valutazione', 'Valutazione', `<svg viewBox="0 0 200 200" ${S}><path d="M30 165h140"/><path d="M45 165v-40"/><path d="M85 165V95"/><path d="M125 165V65"/><path d="M40 85l45-30 35 15 45-40"/><path d="M145 30h20v20"/></svg>`],
  ['04-faq', 'FAQ', `<svg viewBox="0 0 200 200" ${S}><path d="M70 72a30 30 0 1 1 42 28c-8 4-12 10-12 18v12"/><circle cx="100" cy="160" r="4" fill="#fff"/></svg>`],
  ['05-contatti', 'Contatti', `<svg viewBox="0 0 200 200" ${S}><rect x="28" y="52" width="144" height="100" rx="10"/><path d="M32 58l68 52 68-52"/></svg>`],
];
(async () => {
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1080, height: 1920 } });
  for (const [f, , svg] of items) {
    fs.writeFileSync(path.join(__dirname, 'tmp-hl.html'), `<!DOCTYPE html><html><body style="margin:0;width:1080px;height:1920px;background:#000;display:flex;align-items:center;justify-content:center"><div style="width:360px;height:360px">${svg.replace('<svg', '<svg width="360" height="360"')}</div></body></html>`);
    await p.goto('file://' + path.join(__dirname, 'tmp-hl.html'));
    await p.screenshot({ path: path.join(__dirname, 'hl', f + '.png') });
  }
  await b.close();
  fs.writeFileSync(path.join(__dirname, 'hl', 'labels.json'), JSON.stringify(items.map(([f, l]) => [f, l])));
})();
