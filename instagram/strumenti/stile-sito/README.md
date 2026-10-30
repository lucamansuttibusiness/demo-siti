# Stile sito (da novembre 2026)

Caroselli e copertine nello stile del sito nuovo: bianco e nero, Switzer stretto, marchio INKASA con riga,
numeri giganti. Nel feed il **colore pieno (nero) sta solo nella colonna centrale**: un carosello su tre
ha la copertina nera col numero, gli altri foto piena luminosa (contando anche i reel che finiscono in griglia).

Preparazione (una volta): `npm i playwright @carrot-kpi/switzer-font @fontsource-variable/archivo` in questa cartella.

- `copertine3.js` — copertine (`k: 'black'` con numero, oppure `k: 'photo'`), output in `out3/<data>.jpg`.
- `carosello-sito.js slides.json copertina.jpg cartella/` — slide interne dagli stessi `slides.json`
  (tipi: stake, err/step, myth, faq, check, recap, compare, photo, quote, cta). La prima slide è la copertina.
  `"swap": {"vecchia.jpg": "nuova.jpg"}` nello slides.json sostituisce una foto senza toccare il resto.
- `highlight.js` + `storie-in-evidenza/` — copertine delle storie in evidenza (Servizi, Metodo, Stima, FAQ, Contatti).

Ritmo interno: copertina → slide nera d'impatto → contenuto su bianco → CTA nera con bottone VALUTAZIONE.
Su ogni foto stock resta "Immagine illustrativa".
