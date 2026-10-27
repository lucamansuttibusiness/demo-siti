(() => {
  const root = document.documentElement
  root.classList.add('js')
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches
  const wide = () => matchMedia('(min-width: 901px)').matches
  // Liquid Glass fotografa la pagina all'avvio: deve partire dall'alto
  if ('scrollRestoration' in history) history.scrollRestoration = 'manual'
  if (!location.hash) scrollTo(0, 0)

  addEventListener('load', () => requestAnimationFrame(() => root.classList.add('loaded')))
  setTimeout(() => root.classList.add('loaded'), 2500)

  // ---------- Un solo ciclo di scroll per tutte le scene ----------
  const onScroll = []
  let ticking = false
  const tick = () => { ticking = false; onScroll.forEach(fn => fn()) }
  addEventListener('scroll', () => { if (!ticking) { ticking = true; requestAnimationFrame(tick) } }, { passive: true })
  addEventListener('resize', () => requestAnimationFrame(tick))

  // ---------- Apertura: la foto scorre più lenta della pagina ----------
  const hero = document.querySelector('.hero')
  if (!reduce) onScroll.push(() => {
    const y = scrollY
    if (y > hero.offsetHeight) return
    root.classList.toggle('scrolled', y > 4)
    root.style.setProperty('--hy', `${y * 0.35}px`)
    root.style.setProperty('--hs', `${1 + y / hero.offsetHeight * 0.08}`)
  })

  // ---------- Case: lo scroll verticale fa scorrere le case di lato ----------
  const work = document.querySelector('.work')
  const film = document.querySelector('.film')
  const slides = [...film.querySelectorAll('.slide')]
  const workBar = document.querySelector('.work-bar span')
  const setupWork = () => {
    const pin = wide() && !reduce
    work.classList.toggle('is-pinned', pin)
    if (pin) {
      const travel = film.scrollWidth - film.clientWidth
      work.style.setProperty('--pin-h', `${innerHeight + travel * 1.15}px`)
    } else work.style.removeProperty('--pin-h')
  }
  const syncWork = () => {
    if (!work.classList.contains('is-pinned')) return
    const r = work.getBoundingClientRect()
    const total = work.offsetHeight - innerHeight
    const p = Math.min(1, Math.max(0, -r.top / total))
    film.scrollLeft = p * (film.scrollWidth - film.clientWidth)
    workBar.style.transform = `scaleX(${p})`
    const mid = innerWidth / 2
    slides.forEach(sl => {
      const b = sl.getBoundingClientRect()
      sl.querySelector('img').style.setProperty('--px', `${((b.left + b.width / 2) - mid) * -0.08}px`)
    })
  }
  setupWork()
  addEventListener('resize', setupWork)
  onScroll.push(syncWork)
  document.querySelectorAll('[data-film]').forEach(b => b.addEventListener('click', () => {
    film.scrollBy({ left: (+b.dataset.film) * (slides[0].offsetWidth + 20), behavior: reduce ? 'auto' : 'smooth' })
  }))

  // ---------- Servizi: il servizio a metà schermo accende la sua foto ----------
  const items = [...document.querySelectorAll('.svc-item')]
  const shots = [...document.querySelectorAll('.svc-shot')]
  const io = new IntersectionObserver(entries => entries.forEach(e => {
    if (!e.isIntersecting) return
    const i = +e.target.dataset.i
    items.forEach((li, k) => li.classList.toggle('is-active', k === i))
    shots.forEach((f, k) => f.classList.toggle('on', k === i))
  }), { rootMargin: '-45% 0px -45% 0px' })
  items.forEach(li => io.observe(li))

  // ---------- Come funziona: un passaggio ogni tratto di scroll ----------
  const build = document.querySelector('.build')
  const steps = [...build.querySelectorAll('.b-step')]
  const now = build.querySelector('.b-now')
  const bBar = build.querySelector('.b-bar span')
  let step = -1, terraces = null
  const syncBuild = () => {
    const r = build.getBoundingClientRect()
    const total = build.offsetHeight - innerHeight
    const p = Math.min(0.999, Math.max(0, -r.top / total))
    const i = Math.floor(p * steps.length)
    if (i === step) return
    step = i
    steps.forEach((s, k) => s.classList.toggle('is-on', k === i))
    now.textContent = i + 1
    bBar.style.transform = `scaleX(${(i + 1) / steps.length})`
    if (terraces) terraces.setStep(i)
  }
  onScroll.push(syncBuild)
  syncBuild()

  // ---------- Effetti WebGL: caricati quando servono, fermi fuori schermo ----------
  let fxModule = null
  const loadFx = () => fxModule || (fxModule = import('./fx/fx.js?v=9'))
  const scene = (el, start) => {
    let inst = null, visible = false, loading = false
    const sync = () => inst && inst.setAnimate(visible && !document.hidden)
    new IntersectionObserver(([e]) => {
      visible = e.isIntersecting
      if (visible && !inst && !loading) {
        loading = true
        loadFx().then(m => start(m)).then(x => { inst = x; sync() }).catch(err => console.warn(err))
      }
      sync()
    }, { rootMargin: '400px 0px' }).observe(el)
    document.addEventListener('visibilitychange', sync)
  }
  const mask = new URL('img/logo-mask.svg', document.baseURI).href
  const liquid = (wrap, canvas) => async m => {
    const l = await m.mountLiquidLogo(canvas, mask).catch(() => null)
    if (!l) { wrap.classList.add('no-gl'); return null }
    return { setAnimate: on => l.setAnimate(on && !reduce) }
  }
  scene(document.getElementById('servizi'), m => {
    const g = m.mountGradient(document.getElementById('fx-gradient'))
    return { setAnimate: on => g.setAnimate(on && !reduce) }
  })
  scene(document.querySelector('.svc-mark'), liquid(document.querySelector('.svc-mark'), document.getElementById('fx-logo')))
  scene(document.querySelector('.f-mark'), liquid(document.querySelector('.f-mark'), document.getElementById('fx-logo-foot')))
  scene(build, m => {
    terraces = m.mountTerraces(document.getElementById('fx-terraces'), { reduce })
    terraces.setStep(Math.max(0, step))
    return terraces
  })

  // ---------- Chi siamo: i dati in vetro liquido sopra la mappa ----------
  const buildGlass = () => {
    const holder = document.querySelector('.m-glass')
    if (!holder || !window.Container || !window.html2canvas || scrollY > 40 || !wide()) return
    document.querySelectorAll('.m-facts > div').forEach(d => {
      const c = new Container({ borderRadius: 18, type: 'rounded', tintOpacity: 0.32 })
      const inner = document.createElement('div')
      inner.className = 'g-in'
      inner.innerHTML = `<span>${d.querySelector('dt').textContent}</span><b>${d.querySelector('dd').textContent}</b>`
      c.element.appendChild(inner)
      holder.appendChild(c.element)
      c.updateSizeFromDOM()
    })
    document.querySelector('.m-side').classList.add('glass-ready')
  }
  ;(document.fonts ? document.fonts.ready : Promise.resolve()).then(() => setTimeout(buildGlass, 400))

  // ---------- Entrate: titolo, testo, immagine, scaglionati ----------
  if (!reduce) {
    const targets = []
    ;['.svc-intro', '.about > .h2', '.about > .lead', '.card', '.f-side'].forEach(sel => document.querySelectorAll(sel).forEach(g => {
      const kids = g.matches('.about > *') ? [g] : [...g.children]
      kids.forEach((c, k) => {
        if (c.getBoundingClientRect().top < innerHeight) return
        c.classList.add('reveal'); c.style.setProperty('--d', `${k * 75}ms`); targets.push(c)
      })
    }))
    const rio = new IntersectionObserver(es => es.forEach(e => {
      if (e.isIntersecting) { e.target.classList.add('in'); rio.unobserve(e.target) }
    }), { rootMargin: '0px 0px -8% 0px' })
    targets.forEach(t => rio.observe(t))
  }

  // ---------- Scheda immobile: compone il messaggio WhatsApp ----------
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

  tick()
})()
