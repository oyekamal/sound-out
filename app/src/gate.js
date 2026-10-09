// E6d, the tap gate: "Read it, pick what it says."
// Options follow decision (11): a 2x2 grid {target, onset-change, vowel-change, onset+vowel-change}
// (final instead of onset for words with no onset). Early-check items (L1.02-L1.04, `early: true`) have 3 options in a chain.
// Options are spoken, never printed.
// Repair after a first wrong pick replays the PRINTED word's sounds one at a time under a highlighter;
// the whole target word is never played inside a repair. Two wrongs -> review; no whole-word reveal.
import { options, entry } from './content.js';
import { play, wait, mark, stop, isFast, has } from './audio.js';
import { h, icon, btn } from './ui.js';
import { teacher } from './teacher.js';
import { decorate } from './screens/tiles.js';

const shuffle = a => { const b = [...a]; for (let i = b.length - 1; i > 0; i--) { const j = Math.floor(Math.random() * (i + 1)); [b[i], b[j]] = [b[j], b[i]]; } return b; };

export function printedWord(w, kind, track) {
  const e = entry(w);
  const box = h('div', { class: 'printed', 'data-word': w });
  (e?.g || [...w]).forEach((g, i) => box.append(h('span', { class: 'g', 'data-i': i }, g)));
  if (kind === 'pseudo') box.append(h('span', { class: 'tag' }, track === 'A' ? 'alien word' : 'made-up word'));
  return decorate(box, e);   // Levels 2-4: split vowels, suffix tiles, syllable chunks
}

async function soundOut(box, w) {
  const e = entry(w);
  const spans = [...box.querySelectorAll('.g')];
  for (let i = 0; i < spans.length; i++) {
    spans.forEach(s => s.classList.remove('hl'));
    spans[i].classList.add('hl');
    if ((await play(`ph:${e.p[i]}`)) === false) break;
    await wait(350);
  }
  spans.forEach(s => s.classList.remove('hl'));
}

// Model before ask: the first tap gate a learner ever meets is shown first on ANOTHER word they can already read:
// "Let's do one together", the sounds one at a time under a highlighter, the word, "Now you try". One time per profile.
async function demo(ctx, w) {
  const key = `so-gate-demo-${ctx.profile?.id}`;
  try { if (localStorage.getItem(key)) return; } catch { /* no storage: demo every time */ }
  const known = new Set(ctx.known());
  const cand = Object.keys(options).find(k => k !== w.toLowerCase() && entry(k)?.kind === 'real' && entry(k).g.every(g => known.has(g)) && has(`w:${k}`));
  try { localStorage.setItem(key, '1'); } catch { /* ignore */ }
  if (!cand) return;
  const stage = ctx.stage();
  const box = printedWord(cand, 'real', ctx.track);
  stage.append(h('p', { class: 'prompt' }, "Let's do one together."), box);
  mark('gate-demo', { word: cand });
  await ctx.instruct('ui:letsDoOne');
  await wait(600);
  await soundOut(box, cand);
  await play(`w:${cand}`);
  await wait(500);
  await teacher.say('ui:yourTurn');
}

export async function gate(ctx, w, kind, { windowMs = 40000 } = {}) {   // 40 s: the idle ladder (8 / 16 / 28 s) speaks first, then "that's okay, let's try another one"
  const o = options[w.toLowerCase()];
  if (!o) throw new Error('no tap-gate options for ' + w);
  if (!ctx.test) await demo(ctx, w);
  const all = [o.target, ...o.foils];
  mark('gate-show', { word: w, kind, early: !!o.early, options: all.map(x => ({ w: x.w, cell: x.cell, p: x.p, ipa: x.ipa })) });
  const stage = ctx.stage();
  const box = printedWord(w, kind, ctx.track);
  const say = h('p', { class: 'prompt' }, 'Read it to yourself. Say it.');
  stage.append(box, say);
  // a made-up word is explained once per sitting ("This is an alien word. Sound it out.") before the usual prompt
  const note = kind === 'pseudo' && !ctx.toldMadeUp ? [ctx.track === 'A' ? 'ui:alienWord' : 'ui:madeUpWord'] : [];
  if (note.length) ctx.toldMadeUp = true;
  await ctx.instruct([...note, 'ui:gateRead'], { nudge: 'ui:idleSay' });
  await wait(2000); // the printed word stays alone on screen for 2 s
  let first = null;
  for (let attempt = 1; attempt <= 2; attempt++) {
    mark('attempt', { word: w, n: attempt });
    const grid = h('div', { class: 'options' });
    const order = shuffle(all);
    let pick;
    const picked = new Promise(r => { pick = r; });
    const cards = order.map((opt, i) => {
      const card = h('div', { class: 'opt', 'data-cell': opt.cell, 'data-w': opt.w, 'data-ipa': opt.ipa },
        h('button', { class: 'opt-play', 'aria-label': `Option ${i + 1}: play`, onclick: () => play(`ipa:${opt.ipa}`) }, icon('speaker'), h('span', { class: 'n' }, String(i + 1))),
        btn('This one', 'check', { class: 'opt-pick', disabled: true, say: 'ui:thisOne', onclick: () => pick(opt) }));
      return card;
    });
    grid.append(...cards);
    stage.querySelector('.options')?.remove();
    say.textContent = `Listen to all ${all.length === 3 ? 'three' : 'four'}. Tap the one that matches the word.`;
    stage.append(grid);
    const hearAll = async () => {   // "Tap the one that matches the word", then each option once, lit in turn
      for (const c of cards) { c.classList.add('hl'); const ok = await play(`ipa:${c.dataset.ipa}`); c.classList.remove('hl'); if (ok === false) return false; await wait(250); }
      return true;
    };
    // a stall for 16 s models the READING (the printed word's sounds under the highlighter), never the answer
    await ctx.instruct('ui:gatePick', { stim: hearAll, nudge: 'ui:idlePick', hint: () => soundOut(box, w) });
    cards.forEach(c => c.querySelector('.opt-pick').disabled = false);
    mark('gate-open', { word: w, n: attempt });
    const timer = h('div', { class: 'timer' }, h('i', { style: `animation-duration:${isFast ? 1 : windowMs / 1000}s` }));
    stage.append(timer);
    const res = await Promise.race([picked, new Promise(r => setTimeout(() => r(null), isFast ? 4000 : windowMs))]);
    timer.remove(); stop();
    cards.forEach(c => c.querySelector('.opt-pick').disabled = true);
    if (!res) {
      mark('gate-timeout', { word: w, n: attempt });
      say.textContent = "That's okay. Let's try another one.";
      await teacher.say('ui:gateTimeout');
      return { judged: attempt > 1, correct: first ?? false, timeout: true };
    }
    const ok = res.cell === 'target';
    mark('gate-answer', { word: w, n: attempt, cell: res.cell, correct: ok });
    if (attempt === 1) first = ok;
    const card = cards.find(c => c.dataset.w === res.w);
    card.classList.add(ok ? 'right' : 'wrong');
    if (ok) {
      say.textContent = 'Yes!';
      if (ctx.test) await play('ui:good'); else await teacher.right({ kind: 'read', tries: attempt });
      return { judged: true, correct: first, attempts: attempt };
    }
    teacher.miss();
    if (attempt === 1) {
      mark('repair-start', { word: w });
      say.textContent = "Let's look again, sound by sound.";
      await play('ui:gateRepair');
      grid.classList.add('dim');
      await soundOut(box, w);
      mark('repair-end', { word: w });
    }
  }
  say.textContent = 'We will practise this one again later.';
  await play('ui:gateReview');
  mark('gate-review', { word: w });
  return { judged: true, correct: false, review: true, attempts: 2 };
}
