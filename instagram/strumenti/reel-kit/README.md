# Inkasa Reel Kit

Motore per montare reel verticali 1080×1920 animati partendo da immagini (generate su Gemini) e da un file `reel.json`.

## Uso
```bash
pip install pillow numpy opencv-python-headless   # serve anche ffmpeg
python3 engine.py cartella/reel.json --sheet          # un fotogramma per scena (controllo veloce)
python3 engine.py cartella/reel.json --preview 1.5 6  # fotogrammi ai secondi indicati
python3 engine.py cartella/reel.json                  # MP4 finale
```
Le immagini vanno nella stessa cartella del `reel.json`. Esempio completo: `examples/proprietari/`.

## Opzioni globali
| chiave | valori |
|---|---|
| `palette` | `accent` (oro Inkasa `#B8853C`), `ink`, `paper`, `caption`, `on_accent` |
| `font` | `sans` (Inter) · `serif` (Caladea) · `mono` (macchina da scrivere) |
| `text_style` (parole tra `[ ]`) | `box` riquadro pieno · `marker` evidenziatore · `underline` sottolineato · `sticker` etichetta nera storta |
| `caption_style` | `stroke` bianco con contorno · `pill` su pillola scura · `plain` testo scuro |
| `badge_style` | `square` · `circle` · `outline` |
| `grain` | `true`/`false` grana pellicola |
| `paper_fill` | `true` = sfondo a tinta unita (`palette.paper`) invece della carta dell'immagine |
| `sfx` | `{"whoosh":true,"pop":true,"ticks":true,"rip":true}` |
| `voice` | file audio (es. `voce.m4a`) mixato sopra gli effetti |
| `logo` | percorso logo (default `assets/logo.png`) |

## Scene
Ogni scena può sovrascrivere `font`, `text_style`, `caption_style`, `badge_style` per variare all'interno dello stesso reel.

```json
{"img":"img1.png","dur":4.4,
 "layout":"card",            // card = foto ritagliata su carta (collage) · full = immagine a tutto schermo
 "entry":"slap",             // slap · slide_left · slide_right · drop · zoom · spin · rise · none
 "idle":"float",             // float · sway · breathe · drift · still
 "badge":1, "title":["Titolo con [parola]"], "title_y":360,
 "objects":{"anim":"swing","pivot":[0.35,0.06],"amp":1,"stagger":0.22},
 "texts":[{"text":"Didascalia","y":1560,"at":0.9,"until":2.35,"role":"caption"}],
 "extras":[...]}
```
**Oggetti animati** = parti dell'immagine nel colore `accent` (oro). Animazioni: `swing` dondola · `jingle` tintinnio · `buzz` vibrazione · `drop` cade e rimbalza · `pop` attaccati uno a uno · `slide_in` entrano di lato · `spin` girano entrando · `float` galleggiano · `pulse` pulsano · `none`.
Per oggetti grandi usare `swing/float/pulse/buzz` (quelli che compaiono dopo lasciano vedere la zona ricostruita sotto).

**Ruoli testo**: `title` (scuro), `caption` (didascalia), `pill`.

**Extra**: `stamp` (testo stampato su un oggetto: `text,obj,pos,rot,at`) · `glow` (`pos:"auto"|"auto_object"|[x,y]`, `color`, `radius`, `flicker`) · `sparkles` (`n`,`seed`) · `dust` · `logo_pill` (`y`,`at`,`name`,`sub`) · `pill` (`text`,`y`,`at`).

## Zone sicure Instagram
Testi importanti tra y 220 e y 1600 (sotto 1650 ci sono didascalia e pulsanti dell'app).
