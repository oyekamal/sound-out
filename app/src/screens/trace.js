// Trace: finger-trace the letter over a faint guide. Score = share of the guide covered by the stroke.
import { h } from '../ui.js';
import { mark, play, wait, isFast } from '../audio.js';
import { teacher } from '../teacher.js';

const SIZE = 300, PEN = 30;

// A centre-line of the letter (Zhang-Suen thinning of the guide, 2x down-sampled) as ordered strokes: [[x, y], ...] in canvas pixels.
// Components (the dot of i and j) are separate strokes; a branch is walked and walked back so the finger never jumps inside a stroke.
function strokesOf(guide) {
  const N = SIZE / 2, d = guide.getContext('2d').getImageData(0, 0, SIZE, SIZE).data;
  const b = new Uint8Array(N * N);
  for (let y = 0; y < N; y++) for (let x = 0; x < N; x++) b[y * N + x] = d[((y * 2) * SIZE + x * 2) * 4 + 3] > 128 ? 1 : 0;
  const at = (x, y) => b[y * N + x];
  for (let changed = true; changed;) {
    changed = false;
    for (let pass = 0; pass < 2; pass++) {
      const del = [];
      for (let y = 1; y < N - 1; y++) for (let x = 1; x < N - 1; x++) {
        if (!at(x, y)) continue;
        const p = [at(x, y - 1), at(x + 1, y - 1), at(x + 1, y), at(x + 1, y + 1), at(x, y + 1), at(x - 1, y + 1), at(x - 1, y), at(x - 1, y - 1)];
        const B = p.reduce((a, v) => a + v, 0); if (B < 2 || B > 6) continue;
        let A = 0; for (let k = 0; k < 8; k++) if (!p[k] && p[(k + 1) % 8]) A++;
        if (A !== 1) continue;
        if (pass === 0 ? (p[0] * p[2] * p[4] || p[2] * p[4] * p[6]) : (p[0] * p[2] * p[6] || p[0] * p[4] * p[6])) continue;
        del.push(y * N + x);
      }
      for (const i of del) b[i] = 0;
      if (del.length) changed = true;
    }
  }
  const seen = new Uint8Array(N * N), strokes = [];
  const nb = i => { const x = i % N, y = (i / N) | 0, o = []; for (const [dx, dy] of [[1, 0], [-1, 0], [0, 1], [0, -1], [1, 1], [-1, 1], [1, -1], [-1, -1]]) { const X = x + dx, Y = y + dy; if (X >= 0 && Y >= 0 && X < N && Y < N && b[Y * N + X]) o.push(Y * N + X); } return o; };
  const starts = []; for (let i = 0; i < N * N; i++) if (b[i]) starts.push(i);   // top to bottom, left to right
  const endpoints = starts.filter(i => nb(i).length === 1);
  for (const s0 of [...endpoints, ...starts]) {
    if (seen[s0]) continue;
    const path = []; const stack = [[s0, null]]; seen[s0] = 1;
    // iterative DFS that records the walk and the walk back
    const walk = [s0]; const it = [[s0, nb(s0).filter(n => !seen[n])]];
    while (it.length) {
      const [cur, rest] = it[it.length - 1];
      const nxt = rest.find(n => !seen[n]);
      if (nxt === undefined) { it.pop(); if (it.length) walk.push(it[it.length - 1][0]); continue; }
      seen[nxt] = 1; walk.push(nxt); it.push([nxt, nb(nxt).filter(n => !seen[n])]);
    }
    for (const i of walk) path.push([(i % N) * 2 + 1, ((i / N) | 0) * 2 + 1]);
    if (path.length > 3) strokes.push(path);
  }
  // draw the biggest stroke first (the dot of an i comes last), keep the order stable otherwise
  return strokes.sort((a, c) => c.length - a.length);
}
export async function trace(ctx, letter) {
  const s = ctx.stage();
  const cv = h('canvas', { class: 'trace', width: SIZE, height: SIZE, 'aria-label': `Trace the letter ${letter}` });
  const meter = h('div', { class: 'meter' }, h('i'));
  const status = h('p', { class: 'muted' }, 'Trace 1 of 2');
  s.append(h('h2', {}, 'Trace the letter'), cv, meter, status);
  const g = cv.getContext('2d');
  const guide = document.createElement('canvas'); guide.width = guide.height = SIZE;
  const gg = guide.getContext('2d');
  gg.font = `600 ${SIZE * 0.8}px "Andika", "Comic Neue", "Trebuchet MS", sans-serif`;
  gg.textAlign = 'center'; gg.textBaseline = 'alphabetic';
  gg.fillStyle = '#000'; gg.fillText(letter, SIZE / 2, SIZE * 0.75);
  const gd = gg.getImageData(0, 0, SIZE, SIZE).data;
  const guidePts = [];
  for (let y = 0; y < SIZE; y += 4) for (let x = 0; x < SIZE; x += 4) if (gd[(y * SIZE + x) * 4 + 3] > 128) guidePts.push([x, y]);
  window.__so.traceGuide = { letter, box: (() => { const xs = guidePts.map(p => p[0]), ys = guidePts.map(p => p[1]); return [Math.min(...xs), Math.min(...ys), Math.max(...xs), Math.max(...ys)]; })() };
  const ink = document.createElement('canvas'); ink.width = ink.height = SIZE;
  const ig = ink.getContext('2d');
  const redraw = () => {
    g.clearRect(0, 0, SIZE, SIZE);
    g.globalAlpha = 0.18; g.drawImage(guide, 0, 0); g.globalAlpha = 1;
    g.drawImage(ink, 0, 0);
    g.drawImage(demoInk, 0, 0);
    if (finger) { g.fillStyle = '#e0794a'; g.beginPath(); g.arc(finger.x, finger.y, PEN * 0.6, 0, 7); g.fill(); g.strokeStyle = '#fff'; g.lineWidth = 4; g.stroke(); }
  };
  const coverage = () => {
    const d = ig.getImageData(0, 0, SIZE, SIZE).data;
    let hit = 0; for (const [x, y] of guidePts) if (d[(y * SIZE + x) * 4 + 3] > 0) hit++;
    return guidePts.length ? hit / guidePts.length : 0;
  };
  ig.strokeStyle = '#2f6f8f'; ig.lineWidth = PEN; ig.lineCap = ig.lineJoin = 'round';
  let down = false, last = null, demoing = false;
  const demoInk = document.createElement('canvas'); demoInk.width = demoInk.height = SIZE;
  let finger = null;   // {x, y} while the demonstration runs
  const pt = e => { const r = cv.getBoundingClientRect(); return [(e.clientX - r.left) * SIZE / r.width, (e.clientY - r.top) * SIZE / r.height]; };
  cv.addEventListener('pointerdown', e => { if (demoing) return; down = true; last = pt(e); cv.setPointerCapture(e.pointerId); });
  cv.addEventListener('pointermove', e => { if (!down || demoing) return; const p = pt(e); ig.beginPath(); ig.moveTo(...last); ig.lineTo(...p); ig.stroke(); last = p; redraw(); meter.firstChild.style.width = Math.round(coverage() * 100) + '%'; });
  const scores = [];
  let round = 1, done;
  const finished = new Promise(r => { done = r; });
  let helpAt = 0, drew = 0;
  cv.addEventListener('pointermove', () => { if (down) drew++; });
  cv.addEventListener('pointerup', async () => {
    down = false;
    const c = coverage();
    if (c < 0.7) {   // a stroke that stops short: say how to do it, never "wrong" (at most once every 6 s, and only after a real stroke)
      if (drew > 6 && Date.now() - helpAt > 6000) { helpAt = Date.now(); drew = 0; mark('trace-help', { letter, coverage: c }); teacher.miss(); await teacher.say('ui:traceHelp'); }
      return;
    }
    scores.push(Math.round(c * 100) / 100);
    mark('trace', { letter, coverage: c, round });
    await play('ui:traceGood');
    if (round >= 2) return done();
    round++; status.textContent = 'Trace 2 of 2';
    ig.clearRect(0, 0, SIZE, SIZE); redraw(); meter.firstChild.style.width = '0%';
    await teacher.say('ui:traceAgain');
  });
  // "Watch me first": a finger draws the letter once over the faint guide, then "Trace the letter with your finger."
  const demo = async () => {
    if (demoing) return true;
    demoing = true; mark('trace-demo', { letter });
    const dg = demoInk.getContext('2d'); dg.clearRect(0, 0, SIZE, SIZE); dg.strokeStyle = 'rgba(224,121,74,.55)'; dg.lineWidth = PEN * 0.7; dg.lineCap = dg.lineJoin = 'round';
    try {
      const total = strokesOf(guide).map(st => st.filter((_, i) => i % 3 === 0 || i === st.length - 1));
      const frames = isFast ? 1 : 2200 / 16, reduce = window.matchMedia?.('(prefers-reduced-motion: reduce)').matches;
      const pts = total.reduce((a, st) => a + st.length, 0);
      if (reduce || isFast) { for (const st of total) { dg.beginPath(); st.forEach(([x, y], i) => i ? dg.lineTo(x, y) : dg.moveTo(x, y)); dg.stroke(); } redraw(); if (!isFast) await wait(1400); }
      else for (const st of total) {
        const per = Math.max(2, Math.round(frames * st.length / pts / (st.length - 1)) );
        for (let i = 1; i < st.length; i++) {
          for (let k = 1; k <= per; k++) {
            const t = k / per, x = st[i - 1][0] + (st[i][0] - st[i - 1][0]) * t, y = st[i - 1][1] + (st[i][1] - st[i - 1][1]) * t;
            finger = { x, y }; dg.beginPath(); dg.moveTo(st[i - 1][0] + (st[i][0] - st[i - 1][0]) * (k - 1) / per, st[i - 1][1] + (st[i][1] - st[i - 1][1]) * (k - 1) / per); dg.lineTo(x, y); dg.stroke(); redraw();
            await new Promise(r => requestAnimationFrame(r));
          }
        }
        finger = null; redraw(); await wait(120);
      }
    } finally { finger = null; demoInk.getContext('2d').clearRect(0, 0, SIZE, SIZE); redraw(); demoing = false; }
    return true;
  };
  window.__so.traceDemo = demo; window.__so.traceStrokes = () => strokesOf(guide);   // test hooks
  redraw();
  await ctx.instruct('ui:watchMe', { stim: async () => { if ((await demo()) === false) return false; return teacher.say('ui:traceIntro'); }, nudge: 'ui:idleTrace', hint: () => teacher.point(cv) });
  await ctx.next({ waitFor: finished, skippable: true });
  return { scores };
}
