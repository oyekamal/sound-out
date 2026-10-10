// E8 Tricky word (Track B: "word to remember"): map it, don't flash it. Tap the irregular part.
import { play, wait, mark } from '../audio.js';
import { h, icon } from '../ui.js';
import { entry } from '../content.js';
import { teacher } from '../teacher.js';

export async function tricky(ctx, w) {
  const e = entry(w);
  const s = ctx.stage();
  const label = ctx.track === 'A' ? 'Tricky word' : 'Word to remember';
  const word = h('div', { class: 'printed tricky' });
  const spans = e.g.map((g, i) => h('button', { class: 'g', 'data-i': i }, h('span', { class: 'heartmark', html: '' }), w === 'I' ? 'I' : g));
  word.append(...spans);
  const msg = h('p', { class: 'prompt' });
  s.append(h('h2', {}, label), word, msg);
  await ctx.instruct(ctx.track === 'A' ? 'ui:trickyIntroA' : 'ui:trickyIntroB');
  await play(`w:${w}`);
  const heart = new Set(e.heartIdx || []);
  if (!heart.size) {
    msg.textContent = 'Good news: this one sounds out. No tricky part.';
    await teacher.say('ui:trickyRegular');
    for (let i = 0; i < spans.length; i++) { spans[i].classList.add('hl'); await play(`ph:${e.p[i]}`); await wait(250); spans[i].classList.remove('hl'); }
    await ctx.next();
    return;
  }
  msg.textContent = 'Tap the part that is different.';
  const pointHeart = () => teacher.point(...[...heart].map(i => spans[i]));
  const found = new Set();
  const finished = new Promise(resolve => spans.forEach((sp, i) => sp.addEventListener('click', async () => {
    if (heart.has(i)) {
      found.add(i); sp.classList.add('heart'); sp.querySelector('.heartmark').innerHTML = icon('heart').innerHTML;
      mark('tricky-tap', { word: w, i, heart: true });
      if (found.size === heart.size) { await teacher.right({ kind: 'pick' }); resolve(); }
    } else {
      mark('tricky-tap', { word: w, i, heart: false });
      sp.classList.add('regular'); teacher.miss(); await play(`ph:${e.p[i]}`); await teacher.say('ui:notThatPart');
    }
  })));
  await ctx.instruct('ui:trickyTap', { nudge: 'ui:idleTap', hint: pointHeart });   // taps are live while the teacher speaks
  await finished;
  ctx.rememberWord(w);
  await ctx.next();
}
