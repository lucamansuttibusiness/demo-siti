---
name: inkasa-reel
description: Crea reel Instagram animati per Inkasa Property Management (immagini generate su Gemini + montaggio animato col kit), sempre diversi per formato, stile, testi e immagini.
---

# Reel animati Inkasa

Obiettivo: un reel verticale 1080×1920 (20–35 s) per @inkasaproperty che parla ai **proprietari di casa** (affitti brevi), pronto da pubblicare. Ogni reel deve essere **diverso dai precedenti**: argomento, formato, stile grafico, testi, immagini e animazioni.

## 0. Prima di tutto: varietà
1. Leggi `instagram/registro.md` e `instagram/linee-guida.md` nel repo demo-siti, e in memoria la sezione **Registro reel** di `/areas/inkasa-instagram.md` (argomento, formato, stile, text_style, animazioni dei reel già fatti).
2. Scegli una combinazione nuova:
   - **argomento** mai trattato;
   - **formato** e **stile grafico** diversi dagli ultimi 3 reel;
   - `text_style`, `caption_style`, `badge_style`, `font` e il mix di `entry`/animazioni diversi dall'ultimo reel;
   - **immagini sempre nuove**: non riusare mai immagini di reel precedenti;
   - hook e CTA diversi dagli ultimi 3.
3. Se l'utente indica argomento o stile, rispettalo e varia il resto.
4. Comunica in una riga la combinazione scelta, poi procedi senza chiedere conferma.

## 1. Cataloghi

**Formati (struttura del testo)**
- I N tipi di… (proprietario, ospite, annuncio)
- N errori che ti costano soldi
- Mito vs realtà (scena mito → scena realtà)
- Prima / Dopo (annuncio, foto, calendario, recensioni)
- Una giornata del proprietario fai-da-te (timeline con orari)
- POV: sei un proprietario e…
- Domande che ci fanno sempre (FAQ veloci)
- I numeri (dati/percentuali, uno per scena — solo dati verificati o forniti dall'utente)
- Checklist prima del primo ospite
- Cosa facciamo noi in 24 ore (dietro le quinte Inkasa)
- Tu da solo vs con Inkasa (confronto scena per scena)
- Quiz: indovina quanto… (risposta nella scena dopo)
- Stagionale: countdown all'estate / alla stagione sciistica (Lignano, Sauze d'Oulx)
- Storia di un cliente (problema → soluzione → risultato), solo con dati reali forniti dall'utente

**Stili grafici (prompt Gemini)** — l'oro Inkasa `#B8853C` dev'essere l'**unico colore saturo** e va messo sugli oggetti da animare.
- `collage-halftone`: foto B/N con retino tipografico, ritagliata con bordo bianco a sticker su carta crema strappata (`#F2ECE0`). → layout `card`
- `clean-tipo-airbnb`: interni luminosi e accoglienti, luce naturale, foto in scheda con angoli molto arrotondati e ombra morbida su sfondo bianco caldo `#F7F1E8`, piccole icone 3D morbide (stile clay) dorate. Nessun logo, nome o colore Airbnb: deve sembrare Inkasa. → layout `card` (se lo sfondo esce bianco puro il kit passa da solo a `full`)
- `riso-print`: illustrazione risograph a due colori (inchiostro nero + oro), grana visibile, carta avorio. → `full`
- `paper-cut`: diorama di carta ritagliata a strati, ombre morbide, toni neutri + oggetti oro. → `full`
- `blueprint`: disegno tecnico architettonico a linee bianche su blu notte, dettagli oro. → `full`, palette `paper` blu notte
- `clay-3d`: miniature 3D in plastilina opaca, colori neutri, oggetti oro, sfondo tinta unita. → `full`
- `scrapbook`: polaroid e ritagli su sughero, nastro adesivo oro. → `card`
- `noir`: foto notturne cinematografiche B/N con dettagli oro luminosi. → `card` o `full`
- `editorial-duotone`: foto stile rivista in bicromia nero/oro. → `full`
- `line-art`: illustrazione a inchiostro con tratto unico su carta, campiture oro. → `full`

**Testi**: `text_style` box · marker · underline · sticker — `caption_style` stroke · pill · plain — `font` sans · serif · mono — `badge_style` square · circle · outline (o nessun numero).

**Ingressi**: slap · slide_left · slide_right · drop · zoom · spin · rise — **Idle**: float · sway · breathe · drift — **Oggetti**: swing · jingle · buzz · drop · pop · slide_in · spin · float · pulse. Alterna gli ingressi tra scene consecutive. Per oggetti grandi preferisci swing/float/pulse/buzz.

**CTA (ruotale)**: scrivi il numero nei commenti · salva per quando ti serve · manda a chi affitta casa · scrivici "INFO" in DM · stima gratuita su inkasa.casa · lascia fare a noi.

## 2. Script
- Italiano, tono diretto e ironico, dai del tu, parla del dolore del proprietario e mai degli ospiti in modo offensivo.
- Hook entro 1,5 s; 5–7 scene da 3,5–5 s; una parola chiave per riga tra `[ ]`.
- Niente numeri o promesse inventate su Inkasa: se servono dati, chiedili o usa formulazioni qualitative.
- Chiusura sempre con logo Inkasa (`logo_pill`) + `inkasa.casa`.

## 3. Immagini
Modalità di default: genero io su **Gemini nel Chrome dell'utente** (serve Claude in Chrome e l'utente collegato a Google). Se l'utente preferisce risparmiare, gli do i prompt e lui allega le immagini.

Prompt della prima immagine (poi per le altre: "Same exact style, format and palette again (…riassunto stile…). Scene: …"):
```
Create an image. Vertical 9:16 format. <STILE in inglese>. The key object is rendered in warm gold ochre (#B8853C), the only saturated colour in the image. Leave the top third mostly empty for text. No text, no letters, no numbers, no logos. Scene: <scena>
```
Ogni scena deve avere un oggetto dorato chiaro e animabile (chiavi, cartellino, telefono, tazza, valigia, calendario…), possibilmente non enorme.

**Catturare le immagini da Gemini** (le immagini restano nel browser, quindi si catturano con zoom):
1. Una sola chat Gemini per reel. Dopo ogni generazione, in `javascript_tool` definisci una volta:
```js
window.showCap=(off)=>{const imgs=[...document.querySelectorAll('img')].filter(i=>i.naturalWidth>300&&!i.closest('#capov'));const src=imgs[imgs.length-1];let ov=document.getElementById('capov');if(!ov){ov=document.createElement('div');ov.id='capov';document.body.appendChild(ov);}ov.style.cssText='position:fixed;inset:0;background:#000;z-index:2147483647';ov.replaceChildren();const im=document.createElement('img');im.src=src.src;im.style.cssText=`position:absolute;left:0;top:${-off}px;width:${src.naturalWidth}px;height:${src.naturalHeight}px`;ov.appendChild(im);return [src.naturalWidth,src.naturalHeight]};window.hideCap=()=>document.getElementById('capov')?.remove();
```
2. `showCap(0)` → `zoom` regione `[0,0,naturalWidth,720]` con `save_to_disk:true` e **scala 1**; poi `showCap(naturalHeight-720)` → stessa zoom. Poi `hideCap()`.
3. Unisci le due fette con `stitch.py` del kit (`python3 stitch.py out.png fetta_alta.png fetta_bassa.png W H`) usando i due PNG più recenti in `/tmp/claude-tool-results/`.
4. Controlla ogni immagine: se l'oro non c'è, c'è testo o lo stile devia, rigenerala.

## 4. Montaggio (kit)
1. Il kit è nel repo GitHub `lucamansuttibusiness/demo-siti`, cartella `instagram/strumenti/reel-kit/` (aggiungi il repo alla sessione e clonalo con `--depth 1`; se non è possibile, chiedi all'utente lo zip). Dipendenze: `pip install --break-system-packages pillow numpy opencv-python-headless`, ffmpeg.
2. Crea `reels/<slug>/` con le immagini e un `reel.json` (vedi README del kit ed `examples/proprietari/reel.json`). Applica la combinazione scelta al punto 0.
3. `python3 engine.py reels/<slug>/reel.json --sheet` → guarda il foglio; controlla che i testi non coprano il soggetto, che il testo stia tra y 220 e 1600 e che gli oggetti dorati siano stati riconosciuti. Correggi e ripeti.
4. Render finale, poi estrai 6–8 fotogrammi con ffmpeg (anche durante gli ingressi) e controllali. Nessun bordo nero, nessuna scritta tagliata, nessun residuo dorato fermo dove l'oggetto si è spostato.
5. Invia l'MP4 con SendUserFile e proponi la didascalia (usa la skill `instagram-agent:ig-caption` se disponibile). Audio: solo effetti; suggerisci di aggiungere un audio di tendenza su Instagram, oppure mixa la voce dell'utente con `"voice"`.

## 5. Dopo la consegna
Aggiungi una riga a `instagram/registro.md` (commit e push su `main`) e alla sezione **Registro reel** di `/areas/inkasa-instagram.md`. Se migliori il kit, fai commit anche delle modifiche in `strumenti/reel-kit/`. Riga di memoria:
`- [stated] reel AAAA-MM-GG: <argomento> | formato <…> | stile <…> | testo <text_style/caption_style/font> | animazioni <entry/oggetti>`

## Risparmio di utilizzo
Una chat nuova per ogni reel. Prima di generare chiedi solo ciò che manca davvero. Usa `--sheet` invece di tante anteprime singole. Screenshot del browser a scala ridotta, tranne le catture finali (scala 1).
