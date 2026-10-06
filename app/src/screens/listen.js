// Listen & Talk: the passage is read TO the learner; a picture appears AFTER each chunk.
// Then one Tier-2 word with its English meaning, then 2 spoken questions with picture answers (placeholders).
import { play, wait, mark } from '../audio.js';
import { h, speaker, picture } from '../ui.js';

export async function listen(ctx) {
  const li = ctx.lesson.listen; const lid = ctx.lesson.id;
  const s = ctx.stage();
  const pics = h('div', { class: 'pics' });
  s.append(h('h2', {}, li.title || 'Listen'), h('p', { class: 'muted' }, 'You don\'t need to read this. Just listen.'), pics);
  await ctx.instruct('ui:listenIntro');
  if (ctx.hasClip(`lt:${lid}:title`)) await play(`lt:${lid}:title`);
  for (let i = 0; ctx.hasClip(`lt:${lid}:${i}`); i++) {
    await play(`lt:${lid}:${i}`);
    pics.append(picture(i, 'picture placeholder'));
    mark('picture', { chunk: i });
    await wait(300);
  }
  await ctx.next();
  const t2 = li.tier2?.[0];
  if (t2) {
    const s2 = ctx.stage();
    s2.append(h('h2', {}, 'A new word'), h('div', { class: 'tier2' }, h('b', {}, t2.word), h('p', {}, t2.def)), speaker(`t2:${lid}:0`, { big: true, label: 'Hear the word and its meaning' }));
    await ctx.instruct('ui:listenWord');
    await play(`t2:${lid}:0`);
    await ctx.next();
  }
  for (let j = 0; j < 2 && ctx.hasClip(`q:${lid}:${j}`); j++) {
    const s3 = ctx.stage();
    const q = li.questions[j];
    let pick; const picked = new Promise(r => { pick = r; });
    const answers = h('div', { class: 'answers' }, ...[0, 1, 2].map(k => { const b = h('button', { class: 'answer' }, picture(k + 3 + j, `answer ${k + 1}`)); b.addEventListener('click', () => { b.classList.add('chosen'); mark('listen-answer', { q: j, k }); pick(k); }); return b; }));
    s3.append(h('h2', {}, `Question ${j + 1}`), h('p', { class: 'question' }, q), speaker(`q:${lid}:${j}`, { label: 'Hear the question' }), answers,
      h('p', { class: 'muted small' }, 'Picture answers are placeholders in this prototype.'));
    await ctx.instruct('ui:listenQ');
    await play(`q:${lid}:${j}`);
    await picked; await wait(500);
  }
}
