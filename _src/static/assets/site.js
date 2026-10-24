/* AiEngineered: the live estimate on each page, and the "build my free preview" form. */
(function () {
  'use strict';
  var TRADES_URL = 'https://instant-quote-engine.vercel.app/';
  var CLINIC_URL = 'https://instant-clinic-quote.vercel.app/';
  function $(id) { return document.getElementById(id); }
  function money(n) { return '£' + Math.round(n).toLocaleString('en-GB'); }

  /* ---------- Live estimate ---------- */
  var dataEl = $('est-data');
  if (dataEl) {
    var D = JSON.parse(dataEl.textContent);
    var byKey = {}; D.niches.forEach(function (n) { byKey[n.key] = n; });
    var st = { key: D.current, job: 0, size: 1 };
    var nicheSel = $('est-niche'), jobsEl = $('est-jobs'), sizesEl = $('est-sizes');
    var lo = $('est-lo'), hi = $('est-hi'), cap = $('est-cap'), note = $('est-note'), req = $('est-req');

    function chip(text, pressed, onClick) {
      var b = document.createElement('button');
      b.type = 'button'; b.className = 'chip'; b.textContent = text;
      b.setAttribute('aria-pressed', pressed ? 'true' : 'false');
      b.addEventListener('click', onClick);
      return b;
    }
    function swipe(el) { el.classList.remove('swipe'); void el.offsetWidth; el.classList.add('swipe'); }
    function render(animate) {
      var n = byKey[st.key], job = n.jobs[st.job], sizes = job.sizes || n.sizes, r = job.r[st.size];
      jobsEl.textContent = '';
      n.jobs.forEach(function (j, i) { jobsEl.appendChild(chip(j.name, i === st.job, function () { st.job = i; render(true); })); });
      sizesEl.textContent = '';
      sizes.forEach(function (s, i) { sizesEl.appendChild(chip(s, i === st.size, function () { st.size = i; render(true); })); });
      lo.textContent = money(r[0]); hi.textContent = money(r[1]);
      cap.textContent = 'Guide price for ' + job.name.charAt(0).toLowerCase() + job.name.slice(1) + ', ' + sizes[st.size].charAt(0).toLowerCase() + sizes[st.size].slice(1) + '. ' + (n.kind === 'trade' ? 'Typical UK rates, before they are matched to yours.' : 'Typical UK prices, before you set your own.');
      if (animate) { swipe(lo); swipe(hi); }
      note.hidden = true;
    }
    if (nicheSel) {
      nicheSel.addEventListener('change', function () {
        st.key = nicheSel.value; st.job = 0; st.size = 1; render(true);
        var bf = $('bf-niche'); if (bf) { bf.value = nicheSel.value; }
      });
    }
    req.addEventListener('click', function () {
      var n = byKey[st.key];
      note.textContent = 'This is where your ' + n.people + ' would type their name, phone and email. In your version, the request goes straight to your inbox with one-tap call and WhatsApp buttons.';
      note.hidden = false;
    });
    render(false);
  }

  /* ---------- Build my free preview ---------- */
  var form = $('build-form');
  if (form) {
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var err = $('bf-err');
      var name = $('bf-name').value.replace(/\s+/g, ' ').trim().slice(0, 60);
      var city = $('bf-city').value.replace(/\s+/g, ' ').trim().slice(0, 40);
      var pick = $('bf-niche').value;
      var cc = $('bf-country').value;
      if (name.length < 2) { err.textContent = 'Add your business name.'; $('bf-name').focus(); return; }
      if (city.length < 2) { err.textContent = 'Add your town or city.'; $('bf-city').focus(); return; }
      if (!pick) { err.textContent = 'Choose what your business does.'; $('bf-niche').focus(); return; }
      err.textContent = '';
      var kind = form.querySelector('option[value="' + pick + '"]').getAttribute('data-kind');
      var url = (kind === 'trade' ? TRADES_URL : CLINIC_URL) +
        '?name=' + encodeURIComponent(name) + '&city=' + encodeURIComponent(city) + '&niche=' + encodeURIComponent(pick) + '&cc=' + cc;
      window.location.href = url;
    });
  }
})();
