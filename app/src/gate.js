// E6d, the tap gate: "Read it, pick what it says."
// Options follow decision (11): a 2x2 grid {target, onset-change, vowel-change, onset+vowel-change}
// (final instead of onset for words with no onset). Options are spoken, never printed.
// Repair after a first wrong pick replays the PRINTED word's sounds one at a time under a highlighter;
// the whole target word is never played inside a repair. Two wrongs -> review; no whole-word reveal.
import { options, entry } from './content.js';
import { play, wait, mark, stop, isFast } from './audio.js';
import { h, icon } from './ui.js';

const shuffle = a => { const b = [...a]; for (let i = b.length - 1; i > 0; i--) { const j = Math.floor(Math.random() * (i + 1)); [b[i], b[j]] = [b[j], b[i]]; } return b; };

export function printedWord(w, kind, track) {
  const e = entry(w);
  const box = h('div', { class: 'printed', 'data-word': w });
  (e?.g || [...w]).forEach((g, i) => box.append(h('span', { class: 'g', 'data-i': i }, g)));
  if (kind === 'pseudo') box.append(h('span', { class: 'tag' }, track === 'A' ? 'alien word' : 'made-up word'));
  return box;
}

async function soundOut(box, w) {
  const e = entry(w);
  const spans = [...box.querySelectorAll('.g')];
  for (let i = 0; i < spans.length; i++) {
    spans.forEach(s => s.classList.remove('hl'));
    spans[i].classList.add('hl');
    await play(`ph:${e.p[i]}`);
    await wait(350);
  }
  spans.forEach(s => s.classList.remove('hl'));
}

export async function gate(ctx, w, kind, { windowMs = 12000 } = {}) {
  const o = options[w.toLowerCase()];
  if (!o) throw new Error('no tap-gate options for ' + w);
  const all = [o.target, ...o.foils];
  mark('gate-show', { word: w, kind, options: all.map(x => ({ w: x.w, cell: x.cell, p: x.p, ipa: x.ipa })) });
  const stage = ctx.stage();
  const box = printedWord(w, kind, ctx.track);
  const say = h('p', { class: 'prompt' }, 'Read it to yourself. Say it.');
  stage.append(box, say);
  await ctx.instruct('ui:gateRead');
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
        h('button', { class: 'opt-pick', disabled: true, onclick: () => pick(opt) }, 'This one'));
      return card;
    });
    grid.append(...cards);
    stage.querySelector('.options')?.remove();
    say.textContent = 'Listen to all four. Tap the one that matches the word.';
    stage.append(grid);
    await ctx.instruct('ui:gatePick');
    for (const c of cards) { c.classList.add('hl'); await play(`ipa:${c.dataset.ipa}`); c.classList.remove('hl'); await wait(250); }
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
      await ctx.instruct('ui:gateTimeout');
      return { judged: attempt > 1, correct: first ?? false, timeout: true };
    }
    const ok = res.cell === 'target';
    mark('gate-answer', { word: w, n: attempt, cell: res.cell, correct: ok });
    if (attempt === 1) first = ok;
    const card = cards.find(c => c.dataset.w === res.w);
    card.classList.add(ok ? 'right' : 'wrong');
    if (ok) {
      say.textContent = 'Yes!';
      await play('ui:good');
      return { judged: true, correct: first, attempts: attempt };
    }
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
