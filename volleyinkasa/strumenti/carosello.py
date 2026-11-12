# Caroselli @volleyinkasa: palette navy / arancio / crema, Inter black italic, logo e casa ritagliati dai caroselli esistenti.
# Uso: python3 strumenti/carosello.py settimane/<data>/<carosello>/slides.json
import json, sys, os, base64
from playwright.sync_api import sync_playwright
HERE = os.path.dirname(os.path.abspath(__file__))
B64 = lambda p: 'data:image/png;base64,' + base64.b64encode(open(os.path.join(HERE, p), 'rb').read()).decode()
LOGO, HOUSE = B64('logo.png'), B64('house.png')
C = {'navy': '#010080', 'orange': '#EDA93C', 'cream': '#FFF1D2'}
SCHEMES = {  # bg, testo, accento, logo
  'cream': (C['cream'], C['navy'], C['orange'], C['navy']),
  'orange': (C['orange'], C['navy'], C['cream'], C['navy']),
  'navy': (C['navy'], '#FFFFFF', C['orange'], C['orange']),
}
src = sys.argv[1]; deck = json.load(open(src)); out = os.path.dirname(os.path.abspath(src))
N = len(deck['slides'])
def slide(s, i):
    bg, fg, acc, lg = SCHEMES[s.get('bg', 'cream')]
    h = ''
    if s.get('kicker'): h += f'<div class="kick" style="color:{fg}">{s["kicker"]}</div>'
    if s.get('big'): h += f'<div class="big" style="color:{s.get("bigc", acc if s.get("bg")=="navy" else fg)}">{s["big"]}</div>'
    if s.get('h'): h += f'<h1 class="{s.get("hc","")}">{s["h"]}</h1>'
    if s.get('rule'): h += f'<div class="rule" style="background:{acc if s.get("bg")=="navy" else fg}"></div>'
    if s.get('sub'): h += f'<div class="sub" style="color:{acc if s.get("bg")=="navy" else fg}">{s["sub"]}</div>'
    if s.get('p'): h += f'<p>{s["p"]}</p>'
    if s.get('list'): h += '<ul>' + ''.join(f'<li><span style="color:{acc if s.get("bg")=="navy" else fg};opacity:.55">{k+1:02d}</span>{x}</li>' for k, x in enumerate(s['list'])) + '</ul>'
    if s.get('svg'): h += s['svg'].replace('FG', fg).replace('ACC', acc)
    if s.get('link'): h += f'<div class="link" style="color:{acc if s.get("bg")=="navy" else fg}">link in bio &rarr;</div>'
    deco = ''
    if s.get('house'): deco = f'<div class="house" style="background:{acc if s.get("bg")=="navy" else C["navy"]}"></div>'
    if s.get('ghost'): deco = f'<div class="ghost" style="background:{fg}"></div>'
    handle = '<div class="handle">@volleyinkasa</div>' if (i == N - 1 or s.get('handle')) else ''
    return f'''<section style="background:{bg};color:{fg}">{deco}
<div class="logo" style="background:{lg}"></div><div class="pg">{i+1}/{N}</div>
<div class="body {s.get('pos','top')}">{h}</div>{handle}</section>'''
css = f'''*{{margin:0;padding:0;box-sizing:border-box}}
body{{font-family:Inter}}
section{{width:1080px;height:1350px;position:relative;overflow:hidden}}
.logo{{position:absolute;left:80px;top:72px;width:180px;height:155px;-webkit-mask:url({LOGO}) 0 0/180px 155px no-repeat}}
.pg{{position:absolute;right:86px;top:82px;font-weight:700;font-size:30px;letter-spacing:.02em;opacity:.75}}
.body{{position:absolute;left:84px;right:90px}}
.body.top{{top:250px}} .body.bottom{{bottom:120px}} .body.mid{{top:50%;transform:translateY(-45%)}}
.kick{{font-weight:800;font-style:italic;font-size:44px;margin-bottom:10px}}
.big{{font-weight:900;font-style:italic;font-size:250px;line-height:.95;letter-spacing:-.04em}}
h1{{font-weight:900;font-style:italic;font-size:104px;line-height:.98;letter-spacing:-.035em;margin-top:6px}}
h1.xl{{font-size:132px}}
.rule{{width:190px;height:6px;margin:34px 0 24px}}
.sub{{font-weight:800;font-style:italic;font-size:44px}}
p{{font-weight:500;font-size:40px;line-height:1.3;margin-top:28px;max-width:880px}}
ul{{list-style:none;margin-top:44px}}
li{{display:flex;gap:34px;font-weight:800;font-style:italic;font-size:50px;line-height:1.1;padding:26px 0;border-top:4px solid currentColor}}
li:last-child{{border-bottom:4px solid currentColor}}
.link{{font-weight:800;font-style:italic;font-size:42px;margin-top:10px}}
.house{{position:absolute;left:584px;top:880px;width:520px;height:490px;-webkit-mask:url({HOUSE}) 0 0/520px 490px no-repeat}}
.ghost{{position:absolute;left:470px;top:180px;width:780px;height:735px;opacity:.07;-webkit-mask:url({HOUSE}) 0 0/780px 735px no-repeat}}
.handle{{position:absolute;left:84px;bottom:66px;font-weight:700;font-size:28px}}'''
with sync_playwright() as pw:
    b = pw.chromium.launch(); pg = b.new_page(viewport={'width': 1080, 'height': 1350})
    for i, s in enumerate(deck['slides']):
        pg.set_content(f'<!doctype html><html><head><meta charset="utf-8"><style>{css}</style></head><body>{slide(s, i)}</body></html>')
        pg.evaluate('document.fonts.ready')
        over = pg.evaluate('[...document.querySelectorAll(".body")].some(e=>e.getBoundingClientRect().bottom>1290||e.scrollWidth>e.clientWidth+2)')
        if over: print('ATTENZIONE testo fuori dai bordi: slide', i + 1)
        pg.screenshot(path=os.path.join(out, f'{i+1:02d}.jpg'), type='jpeg', quality=92)
    b.close()
