// Trace: finger-trace the letter over a faint guide. Score = share of the guide covered by the stroke.
import { h } from '../ui.js';
import { mark, play } from '../audio.js';
import { teacher } from '../teacher.js';

const SIZE = 300, PEN = 30;
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
  };
  const coverage = () => {
    const d = ig.getImageData(0, 0, SIZE, SIZE).data;
    let hit = 0; for (const [x, y] of guidePts) if (d[(y * SIZE + x) * 4 + 3] > 0) hit++;
    return guidePts.length ? hit / guidePts.length : 0;
  };
  ig.strokeStyle = '#2f6f8f'; ig.lineWidth = PEN; ig.lineCap = ig.lineJoin = 'round';
  let down = false, last = null;
  const pt = e => { const r = cv.getBoundingClientRect(); return [(e.clientX - r.left) * SIZE / r.width, (e.clientY - r.top) * SIZE / r.height]; };
  cv.addEventListener('pointerdown', e => { down = true; last = pt(e); cv.setPointerCapture(e.pointerId); });
  cv.addEventListener('pointermove', e => { if (!down) return; const p = pt(e); ig.beginPath(); ig.moveTo(...last); ig.lineTo(...p); ig.stroke(); last = p; redraw(); meter.firstChild.style.width = Math.round(coverage() * 100) + '%'; });
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
  redraw();
  await ctx.instruct('ui:traceIntro', { nudge: 'ui:idleTrace', hint: () => teacher.point(cv) });
  await ctx.next({ waitFor: finished, skippable: true });
  return { scores };
}
