(() => {
  const root = document.documentElement
  root.classList.add('js')
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches
  addEventListener('load', () => requestAnimationFrame(() => root.classList.add('loaded')))
  // se le immagini tardano, l'otturatore si apre comunque
  setTimeout(() => root.classList.add('loaded'), 2500)

  // Filmstrip delle case: bottoni avanti/indietro
  const film = document.querySelector('.film')
  document.querySelectorAll('[data-film]').forEach(b => b.addEventListener('click', () => {
    const slide = film.querySelector('.slide')
    film.scrollBy({ left: (+b.dataset.film) * (slide.offsetWidth + 20), behavior: reduce ? 'auto' : 'smooth' })
  }))

  // Fila dei momenti: bottoni e barra di avanzamento
  const row = document.querySelector('.row')
  const bar = document.querySelector('.bar span')
  const syncBar = () => {
    const max = row.scrollWidth - row.clientWidth
    const p = max > 0 ? row.scrollLeft / max : 1
    bar.style.transform = `scaleX(${0.12 + p * 0.88})`
  }
  row.addEventListener('scroll', syncBar, { passive: true })
  addEventListener('resize', syncBar)
  syncBar()
  document.querySelectorAll('[data-row]').forEach(b => b.addEventListener('click', () => {
    row.scrollBy({ left: (+b.dataset.row) * 312 * 2, behavior: reduce ? 'auto' : 'smooth' })
  }))

  // Servizi: il servizio a metà schermo accende la sua foto
  const items = [...document.querySelectorAll('.svc-item')]
  const shots = [...document.querySelectorAll('.svc-shot')]
  const setActive = i => {
    items.forEach((li, k) => li.classList.toggle('is-active', k === i))
    shots.forEach((f, k) => f.classList.toggle('on', k === i))
  }
  const io = new IntersectionObserver(entries => {
    entries.forEach(e => { if (e.isIntersecting) setActive(+e.target.dataset.i) })
  }, { rootMargin: '-45% 0px -45% 0px' })
  items.forEach(li => io.observe(li))

  // Effetti (ShaderGradient + Liquid Logo): caricati solo quando la sezione servizi si avvicina
  const svc = document.getElementById('servizi')
  const mark = document.querySelector('.svc-mark')
  let fx = null, near = false
  const syncFx = () => { if (fx) fx.forEach(f => f && f.setAnimate(near && !reduce && !document.hidden)) }
  const loadFx = () => {
    if (fx) return
    fx = []
    import('./fx/fx.js?v=6').then(async m => {
      const grad = m.mountGradient(document.getElementById('fx-gradient'))
      let logo = null
      try { logo = await m.mountLiquidLogo(document.getElementById('fx-logo'), new URL('img/logo-mask.svg', document.baseURI).href) } catch (e) { console.warn(e) }
      if (!logo) mark.classList.add('no-gl')
      fx = [grad, logo]
      syncFx()
    }).catch(() => mark.classList.add('no-gl'))
  }
  new IntersectionObserver(([e]) => {
    near = e.isIntersecting
    if (near) loadFx()
    syncFx()
  }, { rootMargin: '600px 0px' }).observe(svc)
  document.addEventListener('visibilitychange', syncFx)

  // Entrate: titolo, testo, immagine, scaglionati
  if (!reduce) {
    const groups = [
      '.work-head', '.film-nav', '.svc-intro', '.how-head', '.about', '.mosaic', '.card', '.f-side'
    ]
    const targets = []
    groups.forEach(sel => document.querySelectorAll(sel).forEach(g => {
      [...g.children].forEach((c, k) => {
        if (c.getBoundingClientRect().top < innerHeight) return
        c.classList.add('reveal'); c.style.setProperty('--d', `${k * 75}ms`); targets.push(c)
      })
    }))
    document.querySelectorAll('.slide, .moment').forEach((c, k) => {
      if (c.getBoundingClientRect().top < innerHeight) return
      c.classList.add('reveal'); c.style.setProperty('--d', `${(k % 4) * 70}ms`); targets.push(c)
    })
    const rio = new IntersectionObserver(es => es.forEach(e => {
      if (e.isIntersecting) { e.target.classList.add('in'); rio.unobserve(e.target) }
    }), { rootMargin: '0px 0px -8% 0px' })
    targets.forEach(t => rio.observe(t))
  }

  // Scheda immobile: compone il messaggio WhatsApp
  const f = document.getElementById('scheda')
  const out = document.getElementById('anteprima')
  const luca = document.getElementById('wa-luca')
  const andrea = document.getElementById('wa-andrea')
  const article = { Appartamento: 'un appartamento', Villa: 'una villa', 'Casa indipendente': 'una casa indipendente', 'Baita o chalet': 'una baita' }
  const libera = { "Tutto l'anno": "È libera tutto l'anno.", "Solo d'estate": "È libera solo d'estate.", "Solo d'inverno": "È libera solo d'inverno.", 'Non lo so ancora': 'Non so ancora quando sarà libera.' }
  const compose = () => {
    const dove = f.dove.value.trim()
    const cam = f.camere.value === '1' ? '1 camera' : `${f.camere.value} camere`
    const txt = `Ciao, ho ${article[f.tipo.value]} con ${cam}${dove ? ` a ${dove}` : ''}. ${libera[f.quando.value]} Mi fate una valutazione?`
    out.textContent = txt
    const q = '?text=' + encodeURIComponent(txt)
    luca.href = 'https://wa.me/393319419162' + q
    andrea.href = 'https://wa.me/393519080306' + q
  }
  f.addEventListener('input', compose)
  f.addEventListener('submit', e => e.preventDefault())
  compose()
})()
