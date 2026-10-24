/* AiEngineered: live estimate panel, "build my free preview" form and the contact form. */
(function () {
  'use strict';
  var TRADES_URL = 'https://instant-quote-engine.vercel.app/';
  var CLINIC_URL = 'https://instant-clinic-quote.vercel.app/';
  var CONTACT_HOOK = 'https://uk-trade-engine.app.n8n.cloud/webhook/aiengineered-contact';
  function $(id) { return document.getElementById(id); }
  function money(n) { return '£' + Math.round(n).toLocaleString('en-GB'); }
  function lc(s) { return s.charAt(0).toLowerCase() + s.slice(1); }

  /* ---------- Live estimate ---------- */
  var dataEl = $('est-data');
  if (dataEl) {
    var D = JSON.parse(dataEl.textContent);
    var byKey = {}; D.niches.forEach(function (n) { byKey[n.key] = n; });
    var st = { key: D.current, job: 0, size: 1 };
    var nicheSel = $('est-niche'), jobsEl = $('est-jobs'), sizesEl = $('est-sizes');
    var lo = $('est-lo'), hi = $('est-hi'), cap = $('est-cap'), note = $('est-note'), req = $('est-req');
    var fill = $('est-fill'), smin = $('est-min'), smax = $('est-max');

    function chip(text, pressed, onClick) {
      var b = document.createElement('button');
      b.type = 'button'; b.className = 'chip'; b.textContent = text;
      b.setAttribute('aria-pressed', pressed ? 'true' : 'false');
      b.addEventListener('click', onClick);
      return b;
    }
    function render() {
      var n = byKey[st.key], job = n.jobs[st.job], sizes = job.sizes || n.sizes, r = job.r[st.size];
      jobsEl.textContent = '';
      n.jobs.forEach(function (j, i) { jobsEl.appendChild(chip(j.name, i === st.job, function () { st.job = i; render(); })); });
      sizesEl.textContent = '';
      sizes.forEach(function (s, i) { sizesEl.appendChild(chip(s, i === st.size, function () { st.size = i; render(); })); });
      lo.textContent = money(r[0]); hi.textContent = money(r[1]);
      var min = job.r[0][0], max = job.r[2][1], span = Math.max(1, max - min);
      fill.style.left = ((r[0] - min) / span * 100) + '%';
      fill.style.width = Math.max(4, (r[1] - r[0]) / span * 100) + '%';
      smin.textContent = money(min); smax.textContent = money(max);
      cap.textContent = job.name + ', ' + lc(sizes[st.size]) + '. ' + (n.kind === 'trade' ? 'Typical UK rates, before they are matched to yours.' : 'Typical UK prices, before you set your own.');
      note.hidden = true;
    }
    if (nicheSel) {
      nicheSel.addEventListener('change', function () {
        st.key = nicheSel.value; st.job = 0; st.size = 1; render();
        var bf = $('bf-niche'); if (bf) { bf.value = nicheSel.value; }
      });
    }
    req.addEventListener('click', function () {
      note.textContent = 'Here your ' + byKey[st.key].people + ' add their name, phone and email. On your calculator, the request goes straight to your inbox with one-tap call and WhatsApp buttons.';
      note.hidden = false;
    });
    render();
  }

  /* ---------- Build my free preview ---------- */
  var form = $('build-form');
  if (form) {
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var err = $('bf-err');
      var name = $('bf-name').value.replace(/\s+/g, ' ').trim().slice(0, 60);
      var city = $('bf-city').value.replace(/\s+/g, ' ').trim().slice(0, 40);
      var pick = $('bf-niche').value, cc = $('bf-country').value;
      if (name.length < 2) { err.textContent = 'Add your business name.'; $('bf-name').focus(); return; }
      if (city.length < 2) { err.textContent = 'Add your town or city.'; $('bf-city').focus(); return; }
      if (!pick) { err.textContent = 'Choose what your business does.'; $('bf-niche').focus(); return; }
      err.textContent = '';
      var kind = form.querySelector('option[value="' + pick + '"]').getAttribute('data-kind');
      window.location.href = (kind === 'trade' ? TRADES_URL : CLINIC_URL) +
        '?name=' + encodeURIComponent(name) + '&city=' + encodeURIComponent(city) + '&niche=' + encodeURIComponent(pick) + '&cc=' + cc;
    });
  }

  /* ---------- Contact form ---------- */
  var cf = $('contact-form');
  if (cf) {
    cf.addEventListener('submit', function (e) {
      e.preventDefault();
      var err = $('cf-err'), ok = $('cf-ok'), btn = cf.querySelector('button[type=submit]');
      var body = { name: $('cf-name').value.trim(), email: $('cf-email').value.trim(), business: $('cf-business').value.trim(), message: $('cf-message').value.trim(), website: $('cf-hp').value };
      if (body.name.length < 2) { err.textContent = 'Add your name.'; return; }
      if (!/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(body.email)) { err.textContent = 'Add an email address we can reply to.'; return; }
      if (body.message.length < 5) { err.textContent = 'Add a message.'; return; }
      err.textContent = ''; btn.disabled = true; btn.textContent = 'Sending…';
      fetch(CONTACT_HOOK, { method: 'POST', mode: 'cors', credentials: 'omit', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(body) })
        .then(function (res) {
          if (!res.ok) { throw new Error(String(res.status)); }
          cf.reset(); ok.hidden = false; btn.textContent = 'Message sent';
        })
        .catch(function () { err.textContent = 'That didn’t send. Please try again in a minute.'; btn.disabled = false; btn.textContent = 'Send message'; });
    });
  }
})();
