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
      gm.dataset.src = t.dataset.src; gm.querySelector('img').src = t.dataset.src;
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
