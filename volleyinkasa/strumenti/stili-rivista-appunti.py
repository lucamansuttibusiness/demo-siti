# Settimana 16-22 nov @volleyinkasa: due stili nuovi.
# A = "rivista sportiva" (foto a tutta pagina, Anton maiuscolo), B = "appunti dell'allenatore" (quaderno, scritto a mano)
import base64, os, sys
from playwright.sync_api import sync_playwright
from PIL import Image
W = '/home/claude/work/set4/'; R = '/home/claude/demo-siti/volleyinkasa/'
M = R + 'media/prata-trentino-2026-11-01/'
def b64(p, m): return f'data:{m};base64,' + base64.b64encode(open(p, 'rb').read()).decode()
F = W + 'fonts/node_modules/@fontsource/'
FONTS = ''.join(f"@font-face{{font-family:'{n}';src:url({b64(F+p,'font/woff2')}) format('woff2');font-weight:{w}}}" for n, p, w in [
    ('Anton', 'anton/files/anton-latin-400-normal.woff2', 400),
    ('Caveat', 'caveat/files/caveat-latin-700-normal.woff2', 700),
    ('Marker', 'permanent-marker/files/permanent-marker-latin-400-normal.woff2', 400)])
LOGO = b64(R + 'strumenti/logo.png', 'image/png')
NAVY = '#000080'; Y = '#FFC61A'   # giallo provvisorio: sostituire con l'esadecimale del logo
PAPER = '#F5F2EA'
def ph(name): return b64(W + 'ball.jpg' if name == 'ball' else M + name + '.jpg', 'image/jpeg')

CSS = FONTS + f'''
*{{margin:0;padding:0;box-sizing:border-box}}
section{{width:1080px;height:1350px;position:relative;overflow:hidden;font-family:Inter}}
.logo{{position:absolute;left:84px;top:70px;width:132px;height:114px;-webkit-mask:url({LOGO}) 0 0/132px 114px no-repeat}}
.foot{{position:absolute;left:90px;right:90px;bottom:62px;display:flex;justify-content:space-between;align-items:center;font-weight:700;font-size:30px;letter-spacing:.02em}}
/* ---------- A: rivista ---------- */
.a .tag{{position:absolute;right:90px;top:96px;font-weight:800;font-size:28px;letter-spacing:.16em;text-transform:uppercase;padding:14px 22px}}
.a h1,.a h2,.a .num,.a .word{{font-family:Anton;font-weight:400;text-transform:uppercase;letter-spacing:.005em}}
.a.cover{{color:#fff;background-size:cover}}
.a.cover .ov{{position:absolute;inset:0;background:linear-gradient(to bottom,rgba(0,0,128,.35) 0%,rgba(0,0,128,.15) 30%,rgba(0,0,128,.88) 72%,rgba(0,0,110,.97) 100%)}}
.a.cover .logo{{background:#fff}} .a.cover .tag{{background:{Y};color:{NAVY}}}
.a.cover h1{{position:absolute;left:90px;right:90px;bottom:300px;font-size:196px;line-height:.95}}
.a.cover h1 em{{font-style:normal;color:{Y}}}
.a.cover .sub{{position:absolute;left:90px;right:120px;bottom:160px;font-weight:600;font-size:42px;line-height:1.25}}
.a.page{{background:{PAPER};color:#0b0b3a}} .a.page .logo{{background:{NAVY}}}
.a.page .tag{{border:4px solid {NAVY};color:{NAVY}}}
.a.page .bar{{position:absolute;left:0;top:0;width:100%;height:22px;background:{NAVY}}}
.a.page .num{{position:absolute;left:84px;top:215px;font-size:300px;line-height:1;color:{Y};-webkit-text-stroke:5px {NAVY}}}
.a.page .blk{{position:absolute;left:90px;right:90px;bottom:230px}}
.a.page h2{{font-size:168px;line-height:.98;color:{NAVY}}}
.a.page p{{margin-top:36px;font-weight:500;font-size:52px;line-height:1.28}}
.a.page p b{{font-weight:800;background:linear-gradient(transparent 58%,{Y} 58%)}}
.a.page .ref{{position:absolute;left:90px;bottom:140px;font-weight:800;font-size:26px;letter-spacing:.14em;color:{NAVY};opacity:.7}}
.a.page .foot{{color:{NAVY}}}
.a.stake{{background:{NAVY};color:#fff}} .a.stake .logo{{background:#fff}} .a.stake .tag{{border:4px solid #fff}}
.a.stake h2{{position:absolute;left:90px;right:90px;top:290px;font-size:168px;line-height:1}} .a.stake h2 em{{font-style:normal;color:{Y}}}
.a.stake p{{position:absolute;left:90px;right:120px;top:1000px;font-weight:600;font-size:52px;line-height:1.3}}
.a.list{{background:{Y};color:{NAVY}}} .a.list .logo{{background:{NAVY}}} .a.list .tag{{border:4px solid {NAVY}}}
.a.list h2{{position:absolute;left:90px;top:250px;font-size:112px}}
.a.list ol{{position:absolute;left:90px;right:90px;top:420px;list-style:none}}
.a.list li{{display:flex;gap:30px;align-items:baseline;border-top:5px solid {NAVY};padding:22px 0 24px}} .a.list.five h2{{top:215px}} .a.list.five ol{{top:370px}} .a.list.five li{{padding:10px 0 14px}}
.a.list li:last-child{{border-bottom:5px solid {NAVY}}}
.a.list li i{{font-family:Anton;font-style:normal;font-size:64px;min-width:84px}}
.a.list li span{{font-weight:800;font-size:50px;line-height:1.12}} .a.list li small{{display:block;font-weight:500;font-size:38px;margin-top:6px}}
.a.dict{{background:{NAVY};color:#fff}} .a.dict .logo{{background:#fff}} .a.dict .tag{{border:4px solid {Y};color:{Y}}}
.a.dict .cat{{position:absolute;left:90px;top:330px;font-weight:800;font-size:30px;letter-spacing:.2em;color:#fff;opacity:.75}}
.a.dict .word{{position:absolute;left:84px;right:60px;top:380px;font-size:250px;line-height:1.02;color:{Y}}}
.a.dict .word.s{{font-size:176px;top:400px}} .a.dict .word.xs{{font-size:150px;top:420px;white-space:nowrap}}
.a.dict .rule{{position:absolute;left:90px;top:745px;width:900px;height:5px;background:#fff;opacity:.35}}
.a.dict p{{position:absolute;left:90px;right:100px;top:795px;font-weight:600;font-size:54px;line-height:1.28}}
.a.dict .ex{{position:absolute;left:90px;right:100px;bottom:150px;font-weight:500;font-style:italic;font-size:42px;color:{Y}}}
.a.cta{{background:{NAVY};color:#fff}} .a.cta .logo{{background:#fff}}
.a.cta h2{{position:absolute;left:90px;right:90px;top:300px;font-size:164px;line-height:1}} .a.cta h2 em{{font-style:normal;color:{Y}}}
.a.cta .btn{{position:absolute;left:90px;top:1060px;background:{Y};color:{NAVY};font-weight:800;font-size:44px;padding:26px 40px}}
.a.big{{color:#fff;background-size:cover}}
.a.big .ov{{position:absolute;inset:0;background:linear-gradient(to bottom,rgba(0,0,128,.6),rgba(0,0,128,.45) 35%,rgba(0,0,128,.93) 62%,rgba(0,0,110,.97))}}
.a.big .logo{{background:#fff}} .a.big .tag{{background:{Y};color:{NAVY}}}
.a.big .n{{position:absolute;left:78px;top:330px;font-family:Anton;font-size:400px;line-height:1;color:{Y}}}
.a.big .n small{{font-size:170px;margin-left:14px}}
.a.big h2{{position:absolute;left:90px;top:800px;font-size:104px;line-height:1}}
.a.big p{{position:absolute;left:90px;right:120px;top:960px;font-weight:600;font-size:46px;line-height:1.3}}
/* ---------- B: appunti ---------- */
.b{{background:#FBFAF4;background-image:linear-gradient(rgba(0,0,128,.11) 2px,transparent 2px),linear-gradient(90deg,rgba(0,0,128,.11) 2px,transparent 2px);background-size:54px 54px;background-position:-2px 26px;color:{NAVY}}}
.b .logo{{background:{NAVY};left:auto;right:84px;top:64px;width:110px;height:95px;-webkit-mask-size:110px 95px}}
.b .foot{{font-size:28px}} .b .foot span:first-child{{background:#FBFAF4;padding:4px 10px 4px 0}} .b .foot span:last-child{{background:#FBFAF4;padding:4px 0 4px 10px}}
.b .mk{{font-family:Marker;font-weight:400;line-height:1.04}}
.b .hw{{font-family:Caveat;font-weight:700;line-height:1.08}}
.b .hl{{background:linear-gradient(transparent 46%,{Y} 46%,{Y} 92%,transparent 92%);padding:0 10px;margin:0 -6px}}
.b .lab{{position:absolute;left:90px;top:92px;font-family:Caveat;font-weight:700;font-size:58px;transform:rotate(-2deg)}}
.b .pol{{position:absolute;background:#fff;padding:26px 26px 110px;box-shadow:0 18px 40px rgba(0,0,60,.28)}}
.b .pol div{{background-size:cover}}
.b .pol span{{position:absolute;left:0;right:0;bottom:22px;text-align:center;font-family:Caveat;font-weight:700;font-size:52px}}
.b .tape{{position:absolute;width:210px;height:62px;background:{Y};opacity:.82}}
.b .circ{{position:absolute;left:84px;top:210px;width:190px;height:190px;border:9px solid {NAVY};border-radius:53% 47% 50% 50%/48% 52% 48% 52%;display:flex;align-items:center;justify-content:center;font-family:Marker;font-size:120px;transform:rotate(-4deg)}}
.b h2{{position:absolute;left:90px;right:90px;top:440px;font-family:Marker;font-weight:400;font-size:150px;line-height:1.05}}
.b .txt{{position:absolute;left:90px;right:90px;top:660px;font-family:Caveat;font-weight:700;font-size:100px;line-height:1.08}}
.b .no{{position:absolute;left:90px;right:90px;bottom:150px;font-family:Caveat;font-weight:700;font-size:78px;border-top:6px dashed {NAVY};padding-top:22px}}
.b .stamp{{position:absolute;font-family:Anton;font-size:150px;letter-spacing:.04em;padding:6px 40px 0;transform:rotate(-7deg)}}
.b .stamp.f{{border:12px solid {NAVY};color:{NAVY}}} .b .stamp.v{{background:{NAVY};color:{Y};border:12px solid {NAVY}}}
.b .q{{position:absolute;left:90px;right:90px;top:240px;font-family:Marker;font-size:108px;line-height:1.1}}
.b .why{{position:absolute;left:90px;right:90px;top:960px;font-family:Caveat;font-weight:700;font-size:86px;line-height:1.05;line-height:1.1}}
.b ul{{position:absolute;left:90px;right:90px;list-style:none;font-family:Caveat;font-weight:700}}
.b li{{display:flex;gap:28px;align-items:flex-start;font-size:86px;line-height:1.02;margin-bottom:44px}}
.b li i{{flex:none;width:56px;height:56px;border:7px solid {NAVY};margin-top:16px;font-style:normal;font-family:Marker;font-size:64px;line-height:36px;text-align:center}}
.b .wk{{position:absolute;left:90px;top:200px;font-family:Marker;font-size:112px}}
.b .goal{{position:absolute;left:90px;right:90px;top:350px;font-family:Caveat;font-weight:700;font-size:80px;line-height:1.1}}
.b table{{position:absolute;left:90px;top:370px;width:900px;border-collapse:collapse;font-family:Caveat;font-weight:700;font-size:70px;background:#FBFAF4}}
.b td{{border:6px solid {NAVY};padding:30px 24px;line-height:1.05;vertical-align:middle}} .b td:first-child{{font-family:Marker;font-size:52px;width:215px;background:{Y}}}
'''
def foot(i, n): return f'<div class="foot"><span>@volleyinkasa</span><span>{i}/{n}</span></div>'
# ---- A
def a_cover(photo, pos, tag, title, sub, i, n):
    return f'<section class="a cover" style="background-image:url({ph(photo)});background-position:{pos}"><div class="ov"></div><div class="logo"></div><div class="tag">{tag}</div><h1>{title}</h1><div class="sub">{sub}</div>{foot(i,n)}</section>'
def a_stake(tag, title, text, i, n):
    return f'<section class="a stake"><div class="logo"></div><div class="tag">{tag}</div><h2>{title}</h2><p>{text}</p>{foot(i,n)}</section>'
def a_page(tag, num, title, text, ref, i, n):
    return f'<section class="a page"><div class="bar"></div><div class="logo"></div><div class="tag">{tag}</div><div class="num">{num}</div><div class="blk"><h2>{title}</h2><p>{text}</p></div><div class="ref">{ref}</div>{foot(i,n)}</section>'
def a_list(tag, title, items, i, n):
    li = ''.join(f'<li><i>{k+1}</i><span>{t}<small>{s}</small></span></li>' for k, (t, s) in enumerate(items))
    return f'<section class="a list{" five" if len(items)>4 else ""}"><div class="logo"></div><div class="tag">{tag}</div><h2>{title}</h2><ol>{li}</ol>{foot(i,n)}</section>'
def a_dict(tag, cat, word, text, ex, i, n, small=False):
    return f'<section class="a dict"><div class="logo"></div><div class="tag">{tag}</div><div class="cat">{cat}</div><div class="word{" "+small if small else ""}">{word}</div><div class="rule"></div><p>{text}</p><div class="ex">{ex}</div>{foot(i,n)}</section>'
def a_cta(title, btn, i, n):
    return f'<section class="a cta"><div class="logo"></div><h2>{title}</h2><div class="btn">{btn}</div>{foot(i,n)}</section>'
# ---- B
def b_cover(photo, pos, lab, title, cap, i, n, top=250):
    return f'''<section class="b"><div class="logo"></div><div class="lab">{lab}</div>
<div class="pol" style="left:150px;top:{top}px;transform:rotate(-3deg)"><div style="width:660px;height:560px;background-image:url({ph(photo)});background-position:{pos}"></div><span>{cap}</span></div>
<div class="tape" style="left:110px;top:{top-18}px;transform:rotate(-38deg)"></div><div class="tape" style="left:735px;top:{top-30}px;transform:rotate(31deg)"></div>
<div class="mk" style="position:absolute;left:90px;right:60px;top:{top+740}px;font-size:118px">{title}</div>{foot(i,n)}</section>'''
def b_text(lab, big, text, i, n):
    return f'<section class="b"><div class="logo"></div><div class="lab">{lab}</div><div class="mk" style="position:absolute;left:90px;right:90px;top:240px;font-size:128px">{big}</div><div class="hw" style="position:absolute;left:90px;right:90px;top:900px;font-size:96px">{text}</div>{foot(i,n)}</section>'
def b_note(lab, num, title, text, no, i, n):
    return f'<section class="b"><div class="logo"></div><div class="lab">{lab}</div><div class="circ">{num}</div><h2>{title}</h2><div class="txt">{text}</div><div class="no">{no}</div>{foot(i,n)}</section>'
def b_quiz(lab, q, verdict, why, i, n):
    cls = 'v' if verdict == 'VERO' else 'f'
    return f'<section class="b"><div class="logo"></div><div class="lab">{lab}</div><div class="q">&laquo;{q}&raquo;</div><div class="stamp {cls}" style="left:{250 if cls=="f" else 300}px;top:680px">{verdict}</div><div class="why">{why}</div>{foot(i,n)}</section>'
def b_check(lab, title, items, i, n, mark='', top=430, sub=''):
    li = ''.join(f'<li><i>{mark}</i><span>{t}</span></li>' for t in items)
    return f'<section class="b"><div class="logo"></div><div class="lab">{lab}</div><div class="wk">{title}</div>{f"<div class=goal>{sub}</div>" if sub else ""}<ul style="top:{top}px">{li}</ul>{foot(i,n)}</section>'
def b_table(lab, rows, i, n):
    tr = ''.join(f'<tr><td>{a}</td><td>{b}</td></tr>' for a, b in rows)
    return f'<section class="b"><div class="logo"></div><div class="lab">{lab}</div><div class="mk" style="position:absolute;left:90px;top:200px;font-size:100px">Il piano intero</div><table>{tr}</table>{foot(i,n)}</section>'
def b_cta(lab, title, text, i, n):
    return f'<section class="b"><div class="logo"></div><div class="lab">{lab}</div><div class="mk" style="position:absolute;left:90px;right:90px;top:300px;font-size:170px">{title}</div><div class="hw" style="position:absolute;left:90px;right:90px;top:860px;font-size:100px">{text}</div>{foot(i,n)}</section>'

D = {}
# 1 — A — 4 falli
t = 'Regole'; n = 8
D['2026-11-16/carosello-4-falli'] = [
 a_cover('panchine', 'center 85%', 'Regole · 01', '4 falli<br>che vedi<br><em>sempre</em>', 'E che dopo queste slide riconosci prima del fischio.', 1, n),
 a_stake(t, 'Fischio.<br>Punto<br>agli altri.<br><em>Perché?</em>', 'Quasi sempre è uno di questi quattro falli.', 2, n),
 a_page(t, '01', 'Quattro<br>tocchi', 'Hai <b>al massimo 3 tocchi</b> per mandare la palla di là. Il muro non conta.', 'REGOLE FIVB 9.1 · 14.4.1', 3, n),
 a_page(t, '02', 'Doppia', 'Lo stesso giocatore <b>non tocca la palla due volte di fila</b>. Dopo un muro, invece, può.', 'REGOLE FIVB 9.1.1 · 14.4.2', 4, n),
 a_page(t, '03', 'Invasione<br>a rete', 'Toccare la rete <b>tra le antenne</b> mentre giochi la palla è fallo.', 'REGOLA FIVB 11.3.1', 5, n),
 a_page(t, '04', 'Piede<br>in battuta', 'Quando colpisci la palla al servizio <b>non puoi toccare la linea di fondo</b> né il campo.', 'REGOLA FIVB 12.4.3', 6, n),
 a_list(t, 'In breve', [('Quattro tocchi', 'massimo 3, il muro non conta'), ('Doppia', 'mai due tocchi di fila'), ('Invasione a rete', 'non si tocca tra le antenne'), ('Piede in battuta', 'dietro la linea di fondo')], 7, n),
 a_cta('Quale fischio<br>ti fa<br><em>arrabbiare</em><br>di più?', 'Scrivilo nei commenti', 8, n)]
# 2 — B — bagher
l = 'Appunti di tecnica'; n = 8
D['2026-11-16/carosello-bagher'] = [
 b_cover('palazzetto-vista', 'center 75%', 'Appunti di tecnica n.1', 'Il bagher<br>in <span class="hl">4 appunti</span>', 'visto da bordo campo', 1, n),
 b_text(l, 'È il primo tocco di quasi ogni azione.', 'Se la ricezione esce male, <span class="hl">l’attacco non parte</span>.', 2, n),
 b_note(l, '1', 'Le mani', 'Una mano dentro l’altra, <span class="hl">pollici vicini</span> e paralleli.', 'NO: dita intrecciate', 3, n),
 b_note(l, '2', 'Le braccia', 'Tese, gomiti chiusi. La palla tocca <span class="hl">gli avambracci</span>.', 'NO: colpire con mani o polsi', 4, n),
 b_note(l, '3', 'Le gambe', 'Piegate, un piede poco più avanti. <span class="hl">La spinta parte da lì</span>.', 'NO: gambe dritte e busto piegato', 5, n),
 b_note(l, '4', 'Le spalle', 'Girale verso dove vuoi mandare la palla. <span class="hl">Braccia ferme</span>.', 'NO: “sventolare” le braccia', 6, n),
 b_check(l, 'Da ricordare', ['mani unite, pollici paralleli', 'braccia tese, palla sugli avambracci', 'gambe piegate, spingi da lì', 'spalle verso il bersaglio'], 7, n, mark='✓', top=400),
 b_cta(l, 'Provalo<br>stasera.', '10 bagher di fila, da fermo.<br><span class="hl">Salva il post</span>.', 8, n)]
# 3 — A — glossario
t = 'Glossario · 01'; n = 8
D['2026-11-16/carosello-parole-del-volley'] = [
 a_cover('palloni-in-aria-tribuna', 'center 70%', 'Glossario · 01', 'Parole<br>del <em>volley</em>', '5 termini che senti in ogni telecronaca.', 1, n),
 a_dict(t, 'IN BATTUTA', 'Ace', 'La battuta che fa punto da sola: cade a terra o la ricezione non riesce a tenerla in gioco.', '«Due ace di fila e il set è chiuso.»', 2, n),
 a_dict(t, 'IN ATTACCO', 'Pipe', 'L’attacco di seconda linea dal centro del campo. Chi schiaccia stacca dietro la linea dei 3 metri.', '«Palla alta al centro: pipe.»', 3, n),
 a_dict(t, 'IN DIFESA', 'Free ball', 'La palla che gli avversari rimandano senza attaccare. Facile da ricevere: occasione da non sprecare.', '«Free ball! Costruiamo.»', 4, n, small='s'),
 a_dict(t, 'IN ATTACCO', 'Mani-out', 'L’attacco tirato apposta contro le mani del muro, per far finire la palla fuori.', '«Non passava, ha cercato il mani-out.»', 5, n, small='s'),
 a_dict(t, 'IN RICEZIONE', 'Cambio palla', 'Fare punto quando batte l’altra squadra. Così ti riprendi il servizio.', '«Serve un cambio palla, subito.»', 6, n, small='xs'),
 a_list('Glossario', 'In breve', [('Ace', 'punto diretto in battuta'), ('Pipe', 'attacco di seconda linea dal centro'), ('Free ball', 'palla facile, senza attacco'), ('Mani-out', 'attacco sulle mani del muro'), ('Cambio palla', 'punto quando batte l’altro')], 7, n),
 a_cta('Quale parola<br>spieghiamo<br>la <em>prossima</em><br>volta?', 'Scrivila nei commenti', 8, n)]
# 4 — A — dato gigante (post singolo)
D['2026-11-16/post-rete-243'] = [
 f'<section class="a big" style="background-image:url({ph("squadre-rete")});background-position:center 30%"><div class="ov"></div><div class="logo"></div><div class="tag">Il numero</div><div class="n">2,43<small>m</small></div><h2>La rete degli uomini</h2><p>Quella delle donne è a 2,24 m. Si misura al centro del campo.</p><div class="foot"><span>@volleyinkasa</span><span>Regola FIVB 2.1.1</span></div></section>']
# 5 — B — vero o falso
l = 'Vero o falso?'; n = 8
D['2026-11-16/carosello-vero-o-falso'] = [
 b_cover('tribuna-pubblico', 'center 80%', 'Quiz da palestra', '<span class="hl">Vero</span> o falso?', '5 cose che si sentono dire', 1, n),
 b_quiz(l + ' 1/5', 'Non si può colpire la palla con i piedi.', 'FALSO', 'La palla può toccare <span class="hl">qualsiasi parte del corpo</span>. Anche il piede.', 2, n),
 b_quiz(l + ' 2/5', 'Se la palla tocca la riga è fuori.', 'FALSO', 'Basta che <span class="hl">una parte della palla</span> tocchi la linea: è dentro.', 3, n),
 b_quiz(l + ' 3/5', 'Il quinto set finisce a 15.', 'VERO', 'A 15 punti, ma servono sempre <span class="hl">due punti di scarto</span>.', 4, n),
 b_quiz(l + ' 4/5', 'Il libero può andare in battuta.', 'FALSO', 'Il libero <span class="hl">non serve e non mura</span>.', 5, n),
 b_quiz(l + ' 5/5', 'Il muro conta come primo tocco.', 'FALSO', 'Dopo il muro la squadra ha ancora <span class="hl">tre tocchi</span>.', 6, n),
 b_check('Le soluzioni', 'Com’è andata?', ['Piedi: si può', 'Riga: è dentro', 'Quinto set: a 15', 'Libero: niente battuta', 'Muro: non conta'], 7, n, mark='✓', top=400),
 b_cta('Vero o falso?', 'Quante ne hai prese?', 'Scrivi il tuo punteggio <span class="hl">nei commenti</span>.', 8, n)]
# 6 — B — piano 4 settimane
l = 'Piano di allenamento'; n = 8
def wk(k, name, goal, items, i): return b_check(l, f'Settimana {k}', items, i, n, top=640, sub=f'Obiettivo: <span class="hl">{name}</span><br>{goal}')
D['2026-11-16/carosello-piano-4-settimane'] = [
 b_cover('pallone-inkasa-mani', '100% 30%', 'Piano di allenamento', '4 settimane,<br><span class="hl">10 minuti</span>', 'da fare in casa', 1, n, top=230),
 b_text(l, 'Il tocco si costruisce con poco, ma spesso.', '10 minuti, 3 volte a settimana. <span class="hl">Da fermo, senza saltare</span>.', 2, n),
 wk(1, 'controllo', 'palla sempre sopra di te', ['palleggio sopra la testa, 3&nbsp;×&nbsp;30 sec', 'bagher da fermo, 3&nbsp;×&nbsp;10', 'palleggio da seduto, 2 min'], 3),
 wk(2, 'continuità', 'non farla cadere', ['palleggio e bagher alternati, 3&nbsp;×&nbsp;1 min', 'palleggio basso e alto, 20 volte', 'bagher da fermo, 3&nbsp;×&nbsp;15'], 4),
 wk(3, 'movimento', 'piedi che si spostano', ['palleggio con passi laterali, 3&nbsp;×&nbsp;1 min', 'bagher facendo un passo, 3&nbsp;×&nbsp;10', 'palleggio da seduto, 3 min'], 5),
 wk(4, 'record', 'conta e scrivi il numero', ['palleggi di fila: quanti?', 'bagher di fila: quanti?', 'palleggio e bagher alternati: quanti?'], 6),
 b_table(l, [('Sett. 1', 'Controllo: palleggio, bagher, da seduto'), ('Sett. 2', 'Continuità: alternati, basso e alto'), ('Sett. 3', 'Movimento: passi laterali, avanti e indietro'), ('Sett. 4', 'Record: conta i tocchi di fila')], 7, n),
 b_cta(l, 'Inizia<br>lunedì.', '<span class="hl">Salva il piano</span> e spunta la prima casella.', 8, n)]

only = sys.argv[1:]
with sync_playwright() as pw:
    br = pw.chromium.launch(); pg = br.new_page(viewport={'width': 1080, 'height': 1350})
    for name, slides in D.items():
        short = name.split('/')[1]
        if only and short not in only: continue
        out = W + 'out/' + short; os.makedirs(out, exist_ok=True)
        for k, s in enumerate(slides):
            pg.set_content(f'<!doctype html><meta charset="utf-8"><style>{CSS}</style>{s}'); pg.evaluate('document.fonts.ready'); pg.wait_for_timeout(120)
            bad = pg.evaluate('''[...document.querySelectorAll("section *")].filter(e=>{const r=e.getBoundingClientRect();return r.width&&(r.right>1082||r.left<-2)&&!e.classList.contains("ov")&&!e.classList.contains("bar")}).map(e=>e.className||e.tagName)''')
            if bad: print('FUORI BORDO', short, k + 1, bad)
            pg.screenshot(path=f'{out}/{k+1:02d}.jpg', type='jpeg', quality=92)
        ims = [Image.open(f'{out}/{k+1:02d}.jpg').resize((432, 540)) for k in range(len(slides))]
        cols = min(4, len(ims)); rows = -(-len(ims) // cols)
        sheet = Image.new('RGB', (cols * 444 + 12, rows * 552 + 12), '#222')
        for k, im in enumerate(ims): sheet.paste(im, (12 + (k % cols) * 444, 12 + (k // cols) * 552))
        sheet.save(W + f'out/anteprima-{short}.jpg', quality=88)
    br.close()
