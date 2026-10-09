// Levels 2-4 checks.
//   check       "Show what you know" with the lesson's stated bar (tap gate; dictation through Spell it)
//   mastery     the level mastery check (L2.14 L3.18 L4.16): every component at its own threshold opens the next level
//   attackcheck L4.15: the unknown-word protocol on 3 words (the attack routine), bar 2 of 3
// A word with no tap-gate options (logged in content/options_unbuildable_L<N>.json) is read aloud and self-checked:
// the learner hears the word after saying it and taps "I read it right" / "Not quite" (judged, flagged selfReport).
import { play, mark } from '../audio.js';
import { h, speaker, btn } from '../ui.js';
import { teacher } from '../teacher.js';
import { options, entry } from '../content.js';
import { gate, printedWord } from '../gate.js';
import { spellWord } from './spell.js';

export async function selfCheck(ctx, w, kind) {
  const s = ctx.stage();
  const box = printedWord(w, kind === 'pseudo' ? 'pseudo' : null, ctx.track);
  let pick; const picked = new Promise(r => { pick = r; });
  const row = h('div', { class: 'selfrow', hidden: true },
    btn('I read it right', 'check', { class: 'btn primary selfok', say: 'ui:readRight', onclick: () => pick(true) }),
    btn('Not quite', 'question', { class: 'btn ghost selfno', say: 'ui:notQuiteBtn', onclick: () => pick(false) }));
  const hear = btn('I said it. Let me hear it', 'speaker', { class: 'btn selfhear', say: 'ui:saidIt' });
  // the word plays only after "Let me hear it"; then the learner is asked "Did you read it right?" and the two answers appear
  hear.addEventListener('click', async () => { hear.hidden = true; await play(`w:${w}`); row.hidden = false; await ctx.instruct('ui:selfJudge', { nudge: 'ui:idlePick', hint: () => teacher.point(row.querySelector('.selfok')) }); }, { once: true });
  s.append(box, h('p', { class: 'prompt' }, 'Read it out loud. Then check.'), hear, row, h('p', { class: 'selfreport' }, 'self-check: the app does not hear you'));
  mark('selfcheck-show', { word: w, kind });
  const note = kind === 'pseudo' && !ctx.toldMadeUp ? [ctx.track === 'A' ? 'ui:alienWord' : 'ui:madeUpWord'] : [];
  if (note.length) ctx.toldMadeUp = true;
  await ctx.instruct([...note, 'ui:selfRead'], { nudge: 'ui:idleSay', hint: () => teacher.point(hear.hidden ? null : hear) });
  const ok = await picked;
  if (!ctx.test) await (ok ? teacher.right({ kind: 'read' }) : teacher.say('ui:gateReview')); else if (!ok) teacher.miss();
  mark('selfcheck-answer', { word: w, correct: ok });
  return { judged: true, correct: ok, selfReport: true };
}

async function runItem(ctx, it) {
  if (it.kind === 'dictation') return spellWord(ctx, it.w, ctx.known());
  const kind = it.kind === 'pseudo' ? 'pseudo' : 'real';
  const r = options[it.w.toLowerCase()] ? await gate(ctx, it.w, kind) : await selfCheck(ctx, it.w, kind);
  await ctx.record(it.w, kind, r);
  return r;
}

const barOf = (b, n) => b?.pass ? { pass: b.pass, of: b.of } : { pass: Math.ceil((b?.ratio || 0.9) * n), of: n };

export async function check(ctx) {
  const c = ctx.lesson.check || {};
  const real = (c.real || []).filter(w => entry(w)), pseudo = (c.pseudo || []).filter(w => entry(w)), dict = (c.dictation || []).filter(w => entry(w));
  const items = [];
  for (let i = 0; i < Math.max(real.length, pseudo.length); i++) { if (real[i]) items.push({ w: real[i], kind: 'real' }); if (pseudo[i]) items.push({ w: pseudo[i], kind: 'pseudo' }); }
  dict.forEach(w => items.push({ w, kind: 'dictation' }));
  const spare = [...(ctx.lesson.blendList?.pseudo || []), ...(ctx.lesson.blendList?.real || [])].filter(w => options[w] && !items.some(x => x.w === w));
  const bar = barOf(c.bar, items.length);
  const s0 = ctx.stage();
  s0.append(h('h2', {}, 'Show what you know'), h('p', { class: 'prompt' }, 'Some are made-up words. Just sound them out.'), h('p', { class: 'muted small' }, `Bar: ${bar.pass} of ${bar.of} on the first try`));
  await ctx.instruct('ui:checkIntro', { nudge: 'ui:idleArrow' });
  await ctx.next();
  mark('check-start', { lesson: ctx.lesson.id, items: items.map(i => i.w), bar });
  let correct = 0, judged = 0, timeouts = 0, n = 0; const queue = [...items];
  ctx.test = true;
  while (queue.length) {
    const it = queue.shift(); if (n++) await teacher.nextItem(); const r = await runItem(ctx, it);
    if (!r.judged) {
      if (++timeouts > 2) { mark('check-end', { result: 'unfinished' }); return finish(ctx, 'unfinished', correct, judged, bar); }
      const f = spare.shift(); if (f) queue.push({ w: f, kind: entry(f)?.kind === 'pseudo' ? 'pseudo' : 'real' });
      continue;
    }
    judged++; if (r.correct) correct++;
  }
  const pass = judged > 0 && correct / judged >= bar.pass / bar.of;
  mark('check-end', { result: pass ? 'checked' : 'miss', correct, judged, bar });
  return finish(ctx, pass ? 'checked' : 'miss', correct, judged, bar);
}

async function finish(ctx, result, correct, judged, bar) {
  ctx.test = false;
  const s = ctx.stage();
  const msg = { checked: 'You did it! The next part is open.', miss: "We'll practise these again. The next part is still open.", unfinished: "Let's finish this tomorrow." }[result];
  s.append(h('h2', {}, result === 'checked' ? 'Checked by tapping' : 'Show what you know'),
    h('div', { class: 'dots' }, ...Array.from({ length: judged }, (_, i) => h('i', { class: i < correct ? 'on' : '' }))),
    h('p', { class: 'score' }, `${correct} of ${judged} on the first try · bar ${bar.pass}/${bar.of}`), h('p', { class: 'prompt' }, msg));
  await ctx.instruct({ checked: 'ui:checkPass', miss: 'ui:checkMiss', unfinished: 'ui:finishTomorrow' }[result], { nudge: 'ui:idleArrow' });
  await ctx.next();
  return { result, correct, judged, bar };
}

export async function mastery(ctx) {
  const c = ctx.lesson.check; const lvl = ctx.lesson.level;
  const s0 = ctx.stage();
  s0.append(h('h2', {}, `Level ${lvl} check`), h('p', { class: 'prompt' }, 'This checks the whole level. Pass every part to open the next level.'),
    h('div', { class: 'comps' }, ...c.components.map(k => h('div', { class: 'comp' }, h('span', {}, k.label), h('span', { class: 'muted' }, `${k.bar.pass} of ${k.bar.of}`)))));
  await ctx.instruct('ui:masteryIntro', { nudge: 'ui:idleArrow' });
  await ctx.next();
  ctx.test = true;
  mark('mastery-start', { lesson: ctx.lesson.id, components: c.components.map(k => [k.id, k.items.length, k.bar]) });
  const res = [];
  for (const k of c.components) {
    const s = ctx.stage(); s.append(h('h2', {}, k.label), h('p', { class: 'muted' }, `${k.items.length} items · pass ${k.bar.pass}`));
    await ctx.instruct('ui:nextPart', { nudge: 'ui:idleArrow' });
    await ctx.next();
    let correct = 0, judged = 0, n = 0;
    for (const w of k.items) {
      if (!entry(w)) continue;
      if (n++) await teacher.nextItem();
      const r = await runItem(ctx, { w, kind: k.kind === 'heart' ? 'real' : k.kind });
      judged++; if (r.judged && r.correct) correct++;
    }
    const need = Math.ceil(k.bar.pass / k.bar.of * judged);
    res.push({ id: k.id, label: k.label, correct, judged, need, pass: correct >= need });
    mark('mastery-part', { id: k.id, correct, judged, need });
  }
  const ok = res.every(r => r.pass);
  ctx.test = false;
  const s = ctx.stage();
  s.append(h('h2', {}, ok ? `Level ${lvl} passed` : 'Not yet'),
    h('div', { class: 'comps' }, ...res.map(r => h('div', { class: `comp ${r.pass ? 'pass' : 'miss'}` }, h('span', {}, r.label), h('b', {}, `${r.correct} / ${r.judged}`))),
      ...(c.offline || []).map(t => h('div', { class: 'comp offline' }, h('span', {}, t), h('span', {}, 'with your tutor')))),
    h('p', { class: 'prompt' }, ok ? `Level ${lvl + 1} is open.` : 'Practise the parts that were hard, then try this check again.'));
  mark('mastery-end', { result: ok ? 'checked' : 'miss', parts: res });
  await ctx.instruct(ok ? 'ui:masteryPass' : 'ui:masteryMiss', { nudge: 'ui:idleArrow' });
  await ctx.next();
  const correct = res.reduce((a, r) => a + r.correct, 0), judged = res.reduce((a, r) => a + r.judged, 0);
  return { result: ok ? 'checked' : 'miss', correct, judged, mastery: true, parts: res };
}

export async function attackcheck(ctx) {
  const { attackWord } = await import('./attack.js');
  const c = ctx.lesson.check; const words = (c.attack || []).filter(w => entry(w));
  const bar = barOf(c.bar, words.length);
  const s0 = ctx.stage();
  s0.append(h('h2', {}, 'Show what you know'), h('p', { class: 'prompt' }, 'Use the five steps on words you have never practised.'), h('p', { class: 'muted small' }, `Bar: ${bar.pass} of ${bar.of}`));
  await ctx.instruct('ui:attackCheckIntro', { nudge: 'ui:idleArrow' });
  await ctx.next();
  let correct = 0, judged = 0;
  ctx.test = true;
  for (const w of words) {
    await attackWord(ctx, w, { judge: false });
    const r = await selfCheck(ctx, w, 'real');
    judged++; if (r.correct) correct++;
  }
  const pass = judged > 0 && correct / judged >= bar.pass / bar.of;
  return finish(ctx, pass ? 'checked' : 'miss', correct, judged, bar);
}
