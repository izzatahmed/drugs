'use strict';
// Voice search (v0.22): a mic button in the search box, shown only where the browser offers speech recognition.
// Speech is handled by the browser's own speech service (in Chrome this is usually Google's servers); nothing starts until the mic is tapped.
const VoiceSearch = (() => {
  const nrm = s => String(s).normalize('NFKD').replace(/[̀-ͯ]/g, '').toLowerCase().replace(/[^a-z0-9]+/g, ' ').trim();
  const ph = w => w.replace(/ph/g, 'f').replace(/ck/g, 'k').replace(/y/g, 'i').replace(/(.)\1/g, '$1');
  function lev(a, b) {
    a = ph(a); b = ph(b);
    if (Math.abs(a.length - b.length) > 3) return 9;
    let prev = Array.from({length: b.length + 1}, (_, i) => i);
    for (let i = 1; i <= a.length; i++) { const cur = [i]; for (let j = 1; j <= b.length; j++) cur[j] = Math.min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (a[i - 1] === b[j - 1] ? 0 : 1)); prev = cur; }
    return prev[b.length];
  }
  let vocab = null;
  function words(drugs) {
    if (vocab) return vocab;
    const set = new Set();
    for (const d of drugs) for (const t of [d.name, ...(d.aliases || [])]) for (const w of nrm(t).split(' ')) if (w.length >= 4) set.add(w);
    return (vocab = [...set]);
  }
  // Choose the recognised alternative that names a medicine; otherwise correct its first word to the nearest medicine word.
  function best(alts, drugs) {
    const clean = alts.map(nrm).filter(Boolean); if (!clean.length) return '';
    const hay = drugs.map(d => nrm([d.name, ...(d.aliases || [])].join(' ')));
    const direct = clean.find(a => hay.some(x => (' ' + x).includes(' ' + a)));
    if (direct) return direct;
    const vs = words(drugs); let found = null;
    for (const a of clean) {
      const w = a.split(' ').sort((p, q) => q.length - p.length)[0]; if (!w || w.length < 4) continue;
      let top = null, dist = 9; for (const v of vs) { const d = lev(w, v); if (d < dist) { dist = d; top = v; } }
      if (top && dist <= Math.max(1, Math.floor(w.length / 4))) { found = top; break; }
    }
    return found || clean[0];
  }
  function setup() {
    const btn = document.getElementById('voice-search'), input = document.getElementById('search');
    const SR = typeof window !== 'undefined' && (window.SpeechRecognition || window.webkitSpeechRecognition);
    if (!btn || !input) return; if (!SR) { btn.hidden = true; return; }
    btn.hidden = false; let rec = null;
    const done = () => { rec = null; btn.classList.remove('listening'); btn.setAttribute('aria-pressed', 'false'); btn.setAttribute('aria-label', 'Voice search'); };
    btn.addEventListener('click', () => {
      if (rec) { rec.stop(); return; }
      rec = new SR(); rec.lang = 'en-US'; rec.interimResults = false; rec.maxAlternatives = 5;
      btn.classList.add('listening'); btn.setAttribute('aria-pressed', 'true'); btn.setAttribute('aria-label', 'Listening… tap to stop');
      rec.onresult = e => {
        const alts = [...e.results[0]].map(a => a.transcript);
        const q = best(alts, typeof db !== 'undefined' && db ? db.drugs : []);
        if (!q) return; input.value = q; input.dispatchEvent(new Event('input', {bubbles: true})); input.focus();
      };
      rec.onerror = e => { btn.title = e.error === 'not-allowed' ? 'Microphone access was blocked. Allow it in the browser settings to use voice search.' : 'Voice search could not hear a medicine name. Try again or type it.'; };
      rec.onend = done;
      try { rec.start(); } catch (err) { done(); }
    });
  }
  if (typeof document !== 'undefined') setup();
  return {best, lev, nrm};
})();
