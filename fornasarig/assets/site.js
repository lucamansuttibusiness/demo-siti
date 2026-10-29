(function () {
  // menu su telefono
  var b = document.getElementById('burger'), m = document.getElementById('menu');
  if (b && m) b.addEventListener('click', function () {
    var o = m.classList.toggle('open'); b.setAttribute('aria-expanded', o); b.textContent = o ? 'Chiudi' : 'Menu';
  });

  // ingrandimento immagini e disegni tecnici
  var lb = document.getElementById('lb'), li = document.getElementById('lbimg'), lc = document.getElementById('lbcap'), lx = document.getElementById('lbx'), last = null;
  function openLb(src, cap) { last = document.activeElement; li.src = src; li.alt = cap || ''; lc.textContent = cap || ''; lb.hidden = false; lx.focus(); document.body.style.overflow = 'hidden'; }
  function closeLb() { lb.hidden = true; li.src = ''; document.body.style.overflow = ''; if (last) last.focus(); }
  document.addEventListener('click', function (e) {
    var z = e.target.closest('.zoom');
    if (z && z.dataset.src) { e.preventDefault(); openLb(z.dataset.src, z.dataset.cap); }
  });
  if (lb) { lx.addEventListener('click', closeLb); lb.addEventListener('click', function (e) { if (e.target === lb) closeLb(); }); }
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && lb && !lb.hidden) closeLb(); });

  // galleria della scheda prodotto
  var gm = document.querySelector('.gmain .zoom');
  document.querySelectorAll('.gthumb').forEach(function (t) {
    t.addEventListener('click', function () {
      document.querySelectorAll('.gthumb').forEach(function (x) { x.setAttribute('aria-pressed', 'false'); });
      t.setAttribute('aria-pressed', 'true');
      gm.dataset.src = t.dataset.src; if (matchMedia('(prefers-reduced-motion: reduce)').matches) gm.querySelector('img').src = t.dataset.src;
    });
  });

  // filtri del catalogo: linea (barra con le sagome) + caratteristiche
  var grid = document.getElementById('pgrid');
  if (grid) {
    var f = { linea: '', flag: '' }, count = document.getElementById('count');
    var btns = document.querySelectorAll('#filters button, .feat-filter button');
    var params = new URLSearchParams(location.search);
    ['linea', 'flag'].forEach(function (k) { if (params.get(k)) f[k] = params.get(k); });
    if (location.hash.length > 1) f.linea = location.hash.slice(1);
    function has(c, k) { return !f[k] || (' ' + c.dataset[k] + ' ').indexOf(' ' + f[k] + ' ') > -1; }
    function apply() {
      var n = 0;
      grid.querySelectorAll('.pcard').forEach(function (c) { var ok = has(c, 'linea') && has(c, 'flag'); c.hidden = !ok; if (ok) n++; });
      count.textContent = n === 1 ? '1 prodotto' : n + ' prodotti';
      btns.forEach(function (x) { x.setAttribute('aria-pressed', f[x.dataset.f] === x.dataset.v ? 'true' : 'false'); });
    }
    btns.forEach(function (x) {
      x.addEventListener('click', function () {
        f[x.dataset.f] = x.dataset.v; apply();
        if (x.dataset.f === 'linea') history.replaceState(null, '', x.dataset.v ? '#' + x.dataset.v : location.pathname + location.search);
      });
    });
    apply();
  }

  // schede dei tessuti
  document.querySelectorAll('.ttab').forEach(function (t) {
    t.addEventListener('click', function () {
      document.querySelectorAll('.ttab').forEach(function (x) { x.setAttribute('aria-pressed', 'false'); });
      document.querySelectorAll('.tpanel').forEach(function (p) { p.hidden = true; });
      t.setAttribute('aria-pressed', 'true'); document.getElementById(t.dataset.t).hidden = false;
    });
  });

  // modulo contatti (demo: nessun invio reale)
  var form = document.getElementById('form');
  if (form) {
    var q = new URLSearchParams(location.search).get('prodotto'), sel = document.getElementById('f-prod');
    if (q && sel) { for (var i = 0; i < sel.options.length; i++) if (sel.options[i].text === q) sel.selectedIndex = i; }
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var bad = [];
      form.querySelectorAll('[required]').forEach(function (el) {
        var ok = el.type === 'checkbox' ? el.checked : el.value.trim() !== '' && (el.type !== 'email' || /.+@.+\..+/.test(el.value));
        el.classList.toggle('invalid', !ok); if (!ok) bad.push(el);
      });
      var msg = document.getElementById('formmsg'); msg.hidden = false;
      if (bad.length) { msg.textContent = 'Compila i campi evidenziati: nome, email valida, tipo di attività, paese e consenso privacy.'; bad[0].focus(); return; }
      msg.textContent = 'Questa è una versione dimostrativa del sito: la richiesta non è stata inviata. Nel sito definitivo arriverà direttamente all’ufficio commerciale. Per ora chiama il +39 0432 750057.';
    });
  }
})();

// ---- movimento: comparse allo scorrimento, menu interno, parallasse ----
(function () {
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  document.documentElement.classList.add('js');
  var groups = ['.psec h2', '.psec .lead', '.feats > *', '.mosaic > *', '.variants-img > li', '.vars > .var', '.fin', '.dl', '.designer-box > *',
    '.pgrid > .pcard', '#pgrid > .pcard', '.ambs > *', '.three > *', '.refs4 > *', '.ncards > *', '.timeline > *', '.facts > *', '.band h2', '.band .lead', '.split > *', '.des', '.places > *', 'details'];
  var items = [];
  groups.forEach(function (sel) {
    document.querySelectorAll(sel).forEach(function (el) {
      if (el.closest('.phero') || el.classList.contains('rv')) return;
      var sib = el.parentElement ? Array.prototype.indexOf.call(el.parentElement.children, el) : 0;
      el.style.setProperty('--d', Math.min(sib % 4, 3) * 90 + 'ms');
      el.classList.add('rv'); items.push(el);
    });
  });
  document.querySelectorAll('figure.wide, .hero-img, .art-hero').forEach(function (el) { el.classList.add('rv-img'); items.push(el); });
  if (reduce || !('IntersectionObserver' in window)) { items.forEach(function (el) { el.classList.add('in'); }); }
  else {
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.08 });
    items.forEach(function (el) { io.observe(el); });
    // sicurezza: se qualcosa non è entrato in 4 s (stampa, salto di pagina) lo mostra comunque
    setTimeout(function () { items.forEach(function (el) { var r = el.getBoundingClientRect(); if (r.top < innerHeight) el.classList.add('in'); }); }, 4000);
  }

  // galleria: dissolvenza al cambio immagine
  var gmImg = document.querySelector('.gmain img');
  if (gmImg) document.querySelectorAll('.gthumb').forEach(function (t) {
    t.addEventListener('click', function () {
      if (reduce) return;
      gmImg.classList.add('swap');
      var src = t.dataset.src, pre = new Image(); pre.onload = pre.onerror = function () { gmImg.src = src; requestAnimationFrame(function () { gmImg.classList.remove('swap'); }); }; pre.src = src;
    }, true);
  });

  // menu interno della scheda: compare dopo l'apertura e segue la sezione in vista
  var sub = document.querySelector('.psubnav'), hero = document.querySelector('.phero');
  var links = sub ? Array.prototype.slice.call(sub.querySelectorAll('a')) : [];
  var targets = links.map(function (a) { return document.getElementById(a.getAttribute('href').slice(1)); });
  var top = document.querySelector('.top'), lastY = scrollY, ticking = false;
  var wides = Array.prototype.slice.call(document.querySelectorAll('figure.wide .zoom img'));
  function frame() {
    ticking = false; var y = scrollY;
    if (sub && hero) {
      sub.classList.toggle('on', y > hero.offsetTop + hero.offsetHeight * 0.6);
      var cur = 0; targets.forEach(function (t, i) { if (t && t.getBoundingClientRect().top < 160) cur = i; });
      links.forEach(function (a, i) { a.classList.toggle('cur', i === cur); });
      var c = links[cur]; if (c && sub.classList.contains('on')) { var ul = c.parentElement.parentElement; var l = c.offsetLeft - 24; if (l < ul.scrollLeft || l + c.offsetWidth > ul.scrollLeft + ul.clientWidth) ul.scrollTo({ left: l, behavior: 'smooth' }); }
    }
    if (top && !sub) top.classList.toggle('away', y > 400 && y > lastY + 4 && !(document.getElementById('menu') || {}).classList?.contains('open'));
    if (top && (y < lastY - 4 || y < 400)) top.classList.remove('away');
    if (!reduce) wides.forEach(function (im) { var r = im.parentElement.getBoundingClientRect(); if (r.bottom < 0 || r.top > innerHeight) return; var p = (r.top + r.height / 2 - innerHeight / 2) / innerHeight; im.style.transform = 'scale(1.08) translateY(' + (p * -5).toFixed(2) + '%)'; });
    lastY = y;
  }
  addEventListener('scroll', function () { if (!ticking) { ticking = true; requestAnimationFrame(frame); } }, { passive: true });
  frame();
  links.forEach(function (a) { a.addEventListener('click', function (e) { var t = document.getElementById(a.getAttribute('href').slice(1)); if (!t) return; e.preventDefault(); scrollTo({ top: t.getBoundingClientRect().top + scrollY - 128, behavior: reduce ? 'auto' : 'smooth' }); history.replaceState(null, '', a.getAttribute('href')); }); });

  // numeri che contano fino al valore
  if (!reduce && 'IntersectionObserver' in window) {
    var nio = new IntersectionObserver(function (es) {
      es.forEach(function (e) {
        if (!e.isIntersecting) return; nio.unobserve(e.target);
        var el = e.target, m = el.textContent.match(/^(\D*)(\d+)(.*)$/); if (!m) return;
        var end = +m[2], t0 = null; if (end < 10) return;
        function step(ts) { if (!t0) t0 = ts; var k = Math.min(1, (ts - t0) / 1400), v = Math.round(end * (1 - Math.pow(1 - k, 3))); el.textContent = m[1] + v + m[3]; if (k < 1) requestAnimationFrame(step); }
        requestAnimationFrame(step);
      });
    }, { threshold: 0.6 });
    document.querySelectorAll('.facts b').forEach(function (b) { if (/^\D*\d+\D*$/.test(b.textContent.trim())) nio.observe(b); });
  }
})();
