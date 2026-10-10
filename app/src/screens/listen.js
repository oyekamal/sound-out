// Listen & Talk: the passage is read TO the learner; a picture appears AFTER each chunk.
// Then one Tier-2 word with its English meaning, then 2 spoken questions. The questions have no authored answer options, so nothing is graded or praised:
// the learner talks about it out loud and taps the arrow.
import { play, wait, mark } from '../audio.js';
import { h, speaker, picture, icon } from '../ui.js';
import { teacher } from '../teacher.js';
import { tilo } from '../tilo.js';

const ICON_MIC = icon('mic').innerHTML;

export async function listen(ctx) {
  const li = ctx.lesson.listen; const lid = ctx.lesson.id;
  const s = ctx.stage({ beat: "Let's listen to a story!" });
  const pics = h('div', { class: 'pics story' });
  // the first scene fills the room under the title while Tilo introduces the story (no dead space); it hands over to the story grid below
  const first = picture(`scene:${lid}:0`); const hero = first ? h('div', { class: 'intro-hero' }, first) : null;
  s.append(h('h2', {}, li.title || 'Listen'), h('p', { class: 'muted' }, 'You don\'t need to read this. Just listen.'), ...(hero ? [hero] : []), pics);
  await ctx.instruct('ui:listenIntro', { nudge: 'ui:idleTap' });
  ctx.endBeat();   // Tilo's intro is done; the story pictures need the room, so he goes back to the header
  if (ctx.hasClip(`lt:${lid}:title`)) await play(`lt:${lid}:title`);
  for (let i = 0; ctx.hasClip(`lt:${lid}:${i}`); i++) {
    await play(`lt:${lid}:${i}`);
    const pc = picture(`scene:${lid}:${i}`, { n: i }); if (pc) pics.append(pc);
    hero?.remove();
    mark('picture', { chunk: i });
    await wait(300);
  }
  await ctx.next();
  const t2 = li.tier2?.[0];
  if (t2) {
    const s2 = ctx.stage();
    s2.append(h('h2', {}, 'A new word'), h('div', { class: 'tier2' }, h('b', {}, t2.word), h('p', {}, t2.def)), speaker(`t2:${lid}:0`, { big: true, label: 'Hear the word and its meaning' }));
    await ctx.instruct('ui:listenWord', { stim: () => play(`t2:${lid}:0`), nudge: 'ui:idleTap' });
    await ctx.next();
  }
  for (let j = 0; j < 2 && ctx.hasClip(`q:${lid}:${j}`); j++) {
    const s3 = ctx.stage();
    const q = li.questions[j];
    // the story's scene sits up top under the heading; Tilo LISTENS here (the learner answers out loud), never the speaking pose.
    // The big mic is the non-reading cue for "say it out loud": nothing is graded or recorded.
    const scene = picture(`scene:${lid}:${j}`) || picture(`scene:${lid}:0`);
    s3.append(h('h2', {}, `Question ${j + 1}`), ...(scene ? [h('div', { class: 'pics one scene' }, scene)] : []), h('p', { class: 'question' }, q), speaker(`q:${lid}:${j}`, { label: 'Hear the question' }),
      h('div', { class: 'talk', 'aria-label': 'Say your answer out loud' }, h('span', { class: 'talk-mic', html: ICON_MIC }), h('span', { class: 'talk-say' }, 'Say your answer out loud.')));
    tilo.pin('listening');
    mark('listen-talk', { q: j });
    await ctx.instruct([`q:${lid}:${j}`, 'ui:idleSay'], { nudge: 'ui:idleArrow' });   // no right answer exists: talk, then the arrow. No praise.
    await ctx.next();
    await wait(300);
  }
}
