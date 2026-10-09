// L1.13 review: letter NAME vs letter SOUND (§3), and the b/d/p/q mirror set with the course's two anchor tricks.
import { play, wait, mark } from '../audio.js';
import { h, speaker } from '../ui.js';
import { g2p } from '../content.js';
import { choose, shuffle } from './l1steps.js';
import { teacher } from '../teacher.js';

const ALL = 'abcdefghijklmnopqrstuvwxyz'.split('');
const soundOf = l => `ph:${g2p[l] || g2p[l + 'u']}`;           // q -> /kw/ (qu)

function stageFor(ctx, step) { ctx.step = step; mark('step', { key: ctx.sitting.key, step }); return ctx.stage(); }

export async function names(ctx) {
  // meet it: name and sound side by side for b d p q (the letters the course quizzes by name), then a mixed quiz
  for (const l of ['b', 'd', 'p', 'q']) {
    const s = stageFor(ctx, 'names');
    let heard = 0; const mark1 = () => { heard++; ctx.enableNext(); };
    const nameBtn = speaker(`name:${l}`, { label: `Hear the name of ${l}` }), soundBtn = speaker(soundOf(l), { label: `Hear the sound of ${l}` });
    nameBtn.addEventListener('click', mark1); soundBtn.addEventListener('click', mark1);
    s.append(h('h2', {}, 'Name and sound'), h('div', { class: 'lettercard small' }, l === 'q' ? 'qu' : l),
      h('div', { class: 'row' }, h('div', { class: 'opt' }, nameBtn, h('b', {}, 'its name')), h('div', { class: 'opt' }, soundBtn, h('b', {}, 'its sound'))),
      h('p', { class: 'muted' }, l === 'q' ? 'q is called "cue". With its u it says /kw/.' : `When we read, we use the sound, not the name.`));
    // "Every letter has a name and a sound." name, sound, then the rule (q: "The letter q is called cue. With u, it says /kw/")
    await ctx.instruct('ui:l1Names', { nudge: 'ui:idleTap', stim: async () => {
      if ((await play(`name:${l}`)) === false) return false; await wait(350);
      if ((await play(soundOf(l))) === false) return false; await wait(300);
      if (l === 'q') return teacher.seq(['ui:qNote', 'ph:kw'], 150);
      return teacher.say('ui:nameSoundNote');
    } });
    await ctx.next({ disabledUntil: () => true });
  }
  // quiz: was that the name or the sound?
  const quiz = shuffle(ALL.filter(l => !'qxw'.includes(l))).slice(0, 6).map((l, i) => ({ l, as: i % 2 ? 'name' : 'sound' }));
  for (const { l, as } of shuffle(quiz)) {
    const s = stageFor(ctx, 'names-quiz');
    const key = as === 'name' ? `name:${l}` : soundOf(l);
    s.append(h('h2', {}, 'Name or sound?'), h('div', { class: 'lettercard small' }, l), speaker(key, { big: true, label: 'Hear it again' }));
    await ctx.instruct('ui:l1NameOrSound', { stim: () => play(key), nudge: 'ui:idlePick' });
    const r = await choose(s, [{ label: 'Its name', say: 'ui:itsName', icon: 'book', ok: as === 'name', id: 'name' }, { label: 'Its sound', say: 'ui:itsSound', icon: 'speaker', ok: as === 'sound', id: 'sound' }], { autoplay: false, model: [as === 'name' ? 'ui:itsName' : 'ui:itsSound'] });
    await ctx.record(`namesound:${l}`, 'namesound', r);
  }
}

const TIPS = {
  b: "b: the bat comes first, then the ball. b's belly points right.",
  d: "d: the drum comes first, then the stick. d's belly points left.",
  p: 'p hangs down, its loop at the top on the right.',
  q: 'q hangs down too, and always needs its u.',
};
export async function bdpq(ctx) {
  const s0 = stageFor(ctx, 'bdpq');
  s0.append(h('h2', {}, 'b d p q'), h('div', { class: 'printed' }, ...'bdpq'.split('').map(l => h('span', { class: 'g' }, l))),
    h('div', { class: 'cue' }, h('b', {}, 'The bed trick: '), 'make two fists, thumbs up, side by side. Your left hand is b, your right hand is d: together they make "bed".'),
    h('ul', { class: 'cue' }, ...Object.values(TIPS).map(t => h('li', {}, t))));
  await ctx.instruct('ui:l1Bdpq', { nudge: 'ui:idleArrow' });
  // the bed trick and the four tips are spoken; Next is already on screen, so a learner who has heard enough can move on
  await ctx.next({}, () => teacher.seq(['ui:tipBedTrick', 'ui:tipB', 'ui:tipD', 'ui:tipP', 'ui:tipQ'], 300));
  for (const l of shuffle(['b', 'd', 'p', 'q', 'b', 'd', 'p', 'q'])) {
    const s = stageFor(ctx, 'bdpq-pick');
    s.append(h('h2', {}, 'Which letter makes this sound?'), speaker(soundOf(l), { big: true, label: 'Hear the sound' }));
    await ctx.instruct('ui:spellLetter', { stim: () => play(soundOf(l)), nudge: 'ui:idlePick' });
    const r = await choose(s, shuffle(['b', 'd', 'p', 'q']).map(x => ({ body: h('span', { class: 'tilebtn as-label' }, x), label: 'This one', ok: x === l, id: x })), { autoplay: false, model: [soundOf(l)] });
    await ctx.record(`bdpq:${l}`, 'bdpq', r);
    if (!r.correct) { const tip = h('p', { class: 'cue' }, TIPS[l]); s.append(tip); await teacher.seq(['ui:lookCloser', `ui:tip${l.toUpperCase()}`], 200); await wait(300); }
  }
}
