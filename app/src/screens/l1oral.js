// L1.01 "Sounds in Words": oral phonemic awareness, NO letters on screen (real pictures, none for ambiguous words),
// except the 60-second preview of s and a at the very end. Words come from the course lesson (§2a-c).
import { play, wait, mark } from '../audio.js';
import { h, safePicture, speaker, ICON } from '../ui.js';
import { entry, g2p } from '../content.js';
import { choose, choice, shuffle, sounds } from './l1steps.js';
import { teacher } from '../teacher.js';

const FIRST = ['sun', 'top', 'mat', 'pig', 'dog'];          // a) first sound
const BLEND = ['at', 'sat', 'it', 'on', 'mat'];               // b) blending
const SEGMENT = ['up', 'at', 'sat', 'dog'];                   // c) segmenting
const CHECK = ['sat', 'top', 'pig', 'dog', 'mat'];            // check: hear the sounds, pick the word
const ph = w => entry(w).p.map(p => `ph:${p}`);
const pic = (w, i) => safePicture(w, { n: i });                // the real picture, never the printed word; null for ambiguous words (at, it, on, up, sat)

function stageFor(ctx, step) { ctx.step = step; mark('step', { key: ctx.sitting.key, step }); return ctx.stage(); }

async function firstSound(ctx, w, i) {
  const s = stageFor(ctx, 'oral-first');
  s.append(h('h2', {}, 'What sound does it start with?'), ...(pic(w, i) ? [h('div', { class: 'pics one' }, pic(w, i))] : []), speaker(`w:${w}`, { big: true, label: 'Hear the word' }));
  const t = entry(w).p[0];
  const others = shuffle(['s', 'a', 't', 'p', 'i', 'n', 'm', 'd', 'g', 'o'].filter(p => p !== t)).slice(0, 2);
  const c = choice(s, shuffle([t, ...others]).map(p => ({ key: `ph:${p}`, ok: p === t, id: p })), { cls: 'three', model: [`ph:${t}`] });   // mounted hidden: no reflow when the voice ends
  await ctx.instruct('ui:l1OralFirst', { stim: () => play(`w:${w}`), nudge: 'ui:idlePick' });
  const r = await c.start();
  await ctx.record(`oral:first:${w}`, 'oral', r);
}

async function blendWord(ctx, w, pool, { test = false } = {}) {
  const s = stageFor(ctx, test ? 'oral-check' : 'oral-blend');
  s.append(h('h2', {}, 'Which word do the sounds make?'), speaker(null, { big: true, label: 'Hear the sounds again', onplay: () => sounds(ph(w)) }));
  const opts = shuffle([w, ...shuffle(pool.filter(x => x !== w)).slice(0, 2)]);
  const c = choice(s, opts.map((o, i) => ({ key: `w:${o}`, body: pic(o, i) || h('div', { class: 'picture-gap', 'aria-hidden': 'true', html: ICON.speaker }), ok: o === w, id: o })), { cls: 'three', test, model: [...ph(w), `w:${w}`] });
  await ctx.instruct(test ? 'ui:l1OralCheck' : 'ui:l1OralBlend', { stim: () => sounds(ph(w)), nudge: 'ui:idlePick' });
  const r = await c.start();
  await ctx.record(`oral:blend:${w}`, 'oral', r);
  return r;
}

async function segment(ctx, w) {
  const s = stageFor(ctx, 'oral-count');
  const n = entry(w).p.length;
  const dots = h('div', { class: 'dots big' }, ...Array.from({ length: n }, () => h('i')));
  s.append(h('h2', {}, 'How many sounds?'), speaker(`w:${w}`, { big: true, label: 'Hear the word' }));
  await ctx.instruct('ui:l1OralCount', { stim: () => play(`w:${w}`), nudge: 'ui:idlePick' });
  const r = await choose(s, [2, 3, 4].map(k => ({ body: h('div', { class: 'dots' }, ...Array.from({ length: k }, () => h('i', { class: 'on' }))), label: 'This many', ok: k === n, id: String(k) })), { cls: 'three', autoplay: false, model: [`w:${w}`] });
  // show it: one dot lights per sound
  s.append(dots);
  const ds = [...dots.children];
  for (let i = 0; i < n; i++) { ds[i].classList.add('on'); await play(`ph:${entry(w).p[i]}`); await wait(300); }
  await ctx.record(`oral:count:${w}`, 'oral', r);
}

// A dimmed, inert preview of the answer cards under a worked example, so the lower part of the screen is never empty while the teacher talks.
function ghostCards(s, body) {
  const row = h('div', { class: 'options l1-opts three pending ghost', 'aria-hidden': 'true' }, ...[0, 1, 2].map(i => h('div', { class: 'opt' }, body(i), h('span', { class: 'opt-pick ghost-pick', html: ICON.check }))));
  row.inert = true; s.append(row);
}

// Model before ask: one worked item (on a word that is NOT in the real items) before the first real item of a type.
async function worked(ctx, type) {
  const s = stageFor(ctx, type === 'first' ? 'oral-first' : type === 'count' ? 'oral-count' : 'oral-blend');
  if (type === 'count') {
    const w = 'pig', n = entry(w).p.length;
    const dots = h('div', { class: 'dots big' }, ...Array.from({ length: n }, () => h('i')));
    s.append(h('h2', {}, 'How many sounds?'), speaker(`w:${w}`, { big: true, label: 'Hear the word' }), dots);
    ghostCards(s, i => h('div', { class: 'dots' }, ...Array.from({ length: i + 2 }, () => h('i', { class: 'on' }))));
    mark('oral-demo', { type });
    await ctx.instruct(['ui:letsDoOne'], { stim: async () => { if ((await play(`w:${w}`)) === false) return false; await wait(300); for (let i = 0; i < n; i++) { dots.children[i].classList.add('on'); if ((await play(`ph:${entry(w).p[i]}`)) === false) return false; await wait(300); } return teacher.say('ui:yourTurn'); }, nudge: 'ui:idleTap' });
  } else if (type === 'first') {
    s.append(h('h2', {}, 'What sound does it start with?'), ...(pic('sock', 0) ? [h('div', { class: 'pics one' }, pic('sock', 0))] : []), speaker('w:sock', { big: true, label: 'Hear the word' }));
    ghostCards(s, () => h('div', { class: 'picture-gap', html: ICON.speaker }));
    mark('oral-demo', { type });
    await ctx.instruct(['ui:letsDoOne', 'w:sock', 'ph:s', 'ui:yourTurn'], { nudge: 'ui:idleTap' });
  } else {
    s.append(h('h2', {}, 'Which word do the sounds make?'), speaker(null, { big: true, label: 'Hear the sounds', onplay: () => sounds(ph('dog')) }));
    ghostCards(s, () => h('div', { class: 'picture-gap', html: ICON.speaker }));
    mark('oral-demo', { type });
    await ctx.instruct(['ui:letsDoOne'], { stim: async () => { if ((await sounds(ph('dog'))) === false) return false; await wait(300); await play('w:dog'); return teacher.say('ui:yourTurn'); }, nudge: 'ui:idleTap' });
  }
}

export async function oral(ctx) {
  await worked(ctx, 'first');
  for (const [i, w] of FIRST.entries()) await firstSound(ctx, w, i);
  await worked(ctx, 'blend');
  for (const w of BLEND) await blendWord(ctx, w, BLEND.concat(FIRST));
  await worked(ctx, 'count');
  for (const w of SEGMENT) await segment(ctx, w);
  // the only letters in L1.01: a preview of s and a (taught properly in L1.02)
  const s = stageFor(ctx, 'preview');
  let tapped = 0;
  const card = l => { const b = h('button', { class: 'lettercard small', 'data-letter': l }, l); b.addEventListener('click', async () => { tapped++; await play(`ph:${g2p[l]}`); ctx.enableNext(); }); return b; };
  s.append(h('h2', {}, 'Two letters for next time'), h('div', { class: 'row' }, card('s'), card('a')),
    h('p', { class: 'muted' }, 'Tap a letter to hear its sound. You will learn them properly in the next lesson.'));
  await ctx.instruct('ui:l1OralPreview', { stim: async () => { if ((await play('ph:s')) === false) return false; await wait(300); return play('ph:a'); }, nudge: 'ui:idleTap', hint: () => teacher.point(...s.querySelectorAll('button.lettercard')) });
  await ctx.next({ disabledUntil: () => tapped > 0 });
}

// Show what you know for L1.01: hear the sounds, pick the word. Bar from the lesson JSON (4/5).
export async function oralCheck(ctx) {
  const bar = ctx.lesson.check?.bar?.pass ? { pass: ctx.lesson.check.bar.pass, of: ctx.lesson.check.bar.of } : { pass: 4, of: 5 };
  const s0 = stageFor(ctx, 'oral-check');
  s0.append(h('h2', {}, 'Show what you know'), h('p', { class: 'prompt' }, 'Listen to the sounds. Pick the word they make.'));
  await ctx.instruct('ui:l1OralCheck', { nudge: 'ui:idleArrow' }); await ctx.next();
  let correct = 0, judged = 0;
  ctx.test = true;
  for (const w of CHECK) { if (judged) await teacher.nextItem(); const r = await blendWord(ctx, w, CHECK.concat(BLEND), { test: true }); judged++; if (r.correct) correct++; }
  ctx.test = false;
  const result = correct / judged >= bar.pass / bar.of ? 'checked' : 'miss';
  mark('check-end', { result, correct, judged, bar });
  const s = ctx.stage();
  s.append(h('h2', {}, result === 'checked' ? 'Checked by tapping' : 'Show what you know'),
    h('div', { class: 'dots' }, ...Array.from({ length: judged }, (_, i) => h('i', { class: i < correct ? 'on' : '' }))),
    h('p', { class: 'score' }, `${correct} of ${judged} on the first try · bar ${bar.pass}/${bar.of}`));
  await ctx.instruct(result === 'checked' ? 'ui:checkPass' : 'ui:checkMiss', { nudge: 'ui:idleArrow' });
  await ctx.next();
  return { result, correct, judged, bar };
}
