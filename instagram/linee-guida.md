# Linee guida Instagram — Inkasa Property Management

Profilo: **@inkasaproperty** · Sito: **inkasa.casa** · Metricool brand id: **7743456** (timezone Europe/Rome)

## A chi parliamo
Proprietari di seconde case e immobili in Italia che potrebbero affittarli con gli affitti brevi
e non vogliono occuparsene. Inkasa gestisce l'immobile per conto del proprietario
(property management): annuncio, prezzi, ospiti, pulizie. Non affittiamo case nostre.

## Obiettivo di ogni contenuto
Portare proprietari a scrivere **VALUTAZIONE** in DM (stima gratuita). Una sola richiesta per post.

## Regole fisse
- Lingua: italiano, tono premium, chiaro, mai urlato. Niente slang da "guru".
- **Mai inventare numeri, clienti, recensioni o risultati.** Se serve un dato vero e non c'è,
  scrivere `{{dato da confermare}}` e segnalarlo nel riepilogo.
- Niente claim legali o fiscali specifici senza fonte verificata.
- Una sola idea per post. Un solo invito all'azione.
- Didascalia: prima riga = gancio (resta visibile prima del "... altro"), corpo breve,
  invito a scrivere VALUTAZIONE, 3-5 hashtag (#affittibrevi #propertymanagement #casevacanza + 1-2 locali/di formato).

## Stile grafico (caroselli e grafiche)
> **Da novembre 2026 vale lo stile del sito** (bianco/nero, Switzer, colore pieno solo nella colonna centrale): vedi `strumenti/stile-sito/README.md`. Le regole qui sotto (navy/oro, temi dark/cream/gold) restano solo come storico.

- 1080x1350, sfondo navy (#0E1A2B → #1C2D47), accento oro (#C9A24A / #E2C77E), testo crema (#F2ECE0).
- Titoli in Cormorant Garamond 600, testo in Inter. Bordo oro sottile, numerazione "3/9" in alto,
  "INKASA.CASA" in basso.
- Struttura: copertina (max 6 parole) → perché conta → un'idea per slide → riepilogo da salvare → CTA.
- Generatore: `strumenti/carosello.js slides.json cartella` (vedi README).

## Stile dei reel (montaggio)
Riferimento approvato: scritte **dietro la persona** (ritaglio con u2net_human_seg),
composizioni tipografiche con pesi diversi (Montserrat 900 corsivo + etichette maiuscole spaziate),
una parola alla volta al centro alternando minuscolo/MAIUSCOLO con ingresso da sfocato,
arco animato attorno a numeri o parole forti, sfondo leggermente sfocato.
Suoni: pochi, morbidi, **tutti diversi tra loro** (mai lo stesso effetto ripetuto). Niente emoji.
Durata 15-30 s. Apertura forte nei primi 2 secondi.

## Varietà — regole di rotazione (obbligatorie)
L'obiettivo è che il profilo non sembri mai lo stesso post ripetuto.

**Temi grafici dei caroselli** (`theme` in slides.json): `dark` (navy e oro), `cream` (crema e oro scuro),
`gold` (oro pieno e testo navy), `photo` (foto vera a tutto schermo, solo con foto in `media/`). Mai lo stesso tema due caroselli di fila. Se in `media/` ci sono
foto nuove di case gestite, almeno un carosello su due usa `photo`. Finché non ci sono, si possono usare
le foto stock di `media/stock/` (ville e interni di design) con `"stock": true`: compare "Immagine illustrativa"
e la didascalia non deve mai far credere che sia una casa gestita da Inkasa.

**Foto in ogni carosello** (qualsiasi tema): copertina sempre con foto (`img` nella copertina) e almeno
2 slide con foto. Nei temi dark/cream/gold si usa `img` (foto nella metà alta, testo sotto); nel tema photo
le slide `photo`. Non usare la stessa foto stock in due caroselli della stessa settimana.

**Modelli di carosello** (scegliere il tipo di slide in base al modello):
| modello | slide principali |
| --- | --- |
| errori / consigli | step (label "Errore" o "Consiglio") |
| come lavoriamo | step (label "Passo") |
| mito vs realtà | myth |
| checklist da salvare | check |
| domande frequenti | faq |
| da solo vs con Inkasa | compare |
| dietro le quinte / casa gestita | photo |
| frase manifesto (anche carosello corto da 3-4 slide) | quote |
Mai lo stesso modello due volte nello stesso mese. Lunghezza variabile: da 4 a 10 slide.

**Formati dei reel** (a rotazione, mai lo stesso due volte di fila):
parlato in camera · tour veloce di una casa · dietro le quinte senza parlato (clip + scritte + musica) ·
POV ("POV: sei un proprietario e…") · risposta a una domanda arrivata in DM o nei commenti ·
prima/dopo di una casa preparata.

**Reel animati senza riprese** (immagini generate su Gemini + `strumenti/reel-kit/`, skill `inkasa-reel`):
contano come formato a sé nella rotazione. Ogni reel animato cambia argomento, formato del testo, stile grafico
(collage, tipo Airbnb, risograph, carta ritagliata, blueprint, clay 3D…), stile delle scritte e animazioni rispetto
ai precedenti; immagini sempre nuove. Oro `#B8853C` unico colore saturo, chiusura con logo e inkasa.casa.

**Frase d'attacco dei reel**: usare le formule in `ig-reel/hooks.json` del plugin instagram-agent;
la stessa formula non torna prima di 4 settimane (annotarla nel registro).

**Ricerca mensile**: la prima domenica di ogni mese guardare cosa funziona negli account del settore
(anche USA/UK, property management, short-term rental, luxury real estate) e proporre 2-3 formati nuovi
da provare, annotati in fondo a questo file nella sezione "Formati da provare".

**Contenuti reali**: foto e video di case gestite, numeri e storie vere hanno sempre la precedenza
sui contenuti generici. Si trovano in `media/` (vedi `media/README.md`).

## Orizzonte
Il calendario resta sempre pronto **4 settimane in anticipo**: ogni domenica si aggiunge la settimana successiva
all'ultima già presente e si possono ritoccare le settimane future in base ai risultati.

## Mix settimanale (4 post)
| tipo | quanti | formato |
| --- | --- | --- |
| Consiglio pratico (errori, come fare) | 1 | carosello |
| Offerta / come lavoriamo / perché noi | 1 ogni 2 settimane | carosello |
| Opinione netta o falso mito | 1 | reel |
| Dietro le quinte / storia / caso vero | 1 | reel |
| Rotazione libera (FAQ, confronto, checklist) | 1 ogni 2 settimane | carosello |

Mai due post dello stesso tipo uno dopo l'altro. Un tema non torna prima di 6 settimane
con la stessa angolazione (controllare `registro.md`).

## Formati da provare
_(aggiornato ogni mese dalla ricerca)_
