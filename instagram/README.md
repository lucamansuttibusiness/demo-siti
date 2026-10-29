# Instagram Inkasa — sistema settimanale

Questa cartella è la memoria permanente dei contenuti Instagram di **@inkasaproperty**.

- `linee-guida.md` — pubblico, regole, stile grafico e dei reel, mix settimanale. **Leggere sempre per primo.**
- `registro.md` — ogni post preparato o pubblicato, con i risultati. Serve a non ripetersi.
- `settimane/AAAA-MM-GG/` — una cartella per settimana (data del lunedì): `piano.md`,
  e una sottocartella per ogni carosello con `slides.json` e le immagini `01.jpg` … `09.jpg`.
- `strumenti/carosello.js` — genera le slide 1080x1350 da un `slides.json` (3 temi, 11 tipi di slide: istruzioni in testa al file).
- `strumenti/reel-kit/` — motore per i reel animati da immagini (`python3 engine.py reel.json`, istruzioni nel suo README e in `SKILL.md`).
- `media/` — foto e video veri delle case gestite, da usare con priorità.

## Routine della domenica
1. Leggere `linee-guida.md`, `registro.md` e il piano della settimana precedente.
2. Leggere da Metricool (brand 7743456) i risultati dei post degli ultimi 7 giorni e aggiornarli in `registro.md`.
3. Decidere i 4 post della settimana seguente rispettando il mix e le **regole di rotazione** delle linee guida
   (temi grafici, modelli, formati reel, formule d'attacco) e senza ripetere temi delle ultime 6 settimane.
   Prima domenica del mese: fare anche la ricerca mensile dei formati.
4. Creare i 2 caroselli: `slides.json` → `node strumenti/carosello.js` → convertire in JPG.
5. Fare commit e push su `main`. Le immagini sono pubbliche a
   `https://raw.githubusercontent.com/lucamansuttibusiness/demo-siti/main/instagram/settimane/<data>/<carosello>/01.jpg`.
6. Caricare i caroselli su Metricool come **bozze** (draft: true) con data e ora, didascalia e immagini.
7. Scrivere `piano.md` con gli script dei 2 reel e aggiornare `registro.md`.
8. Mandare il riepilogo a Luca: risultati, cosa è in bozza, script da girare, dati da confermare.

Generatore: `NODE_PATH=$(npm root -g):<cartella con node_modules> node strumenti/carosello.js slides.json out/`
(serve `npm i @fontsource/cormorant-garamond`; Playwright e Inter sono già nell'ambiente).
