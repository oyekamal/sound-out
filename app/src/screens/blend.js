// E5 Blend it: tap each letter left to right (its sound plays AFTER the tap), say the word
// (self-report: the app does not hear you), then the tap gate on the same word.
import { play, wait, mark } from '../audio.js';
import { h } from '../ui.js';
import { entry } from '../content.js';
import { gate, printedWord } from '../gate.js';
import { teacher } from '../teacher.js';
import { btn } from '../ui.js';

export async function blendOne(ctx, item, { model = false } = {}) {
  const e = entry(item.w);
  const s = ctx.stage();
  const box = printedWord(item.w, item.kind === 'syllable' ? null : item.kind, ctx.track);
  box.classList.add('tiles');
  const spans = [...box.querySelectorAll('.g')];
  s.append(h('h2', {}, item.kind === 'syllable' ? 'A practice sound (not a word yet)' : 'Blend it'), box);
  if (model) {
    await ctx.instruct('ui:blendModel');
    for (let i = 0; i < spans.length; i++) { spans.slice(0, i + 1).forEach(x => x.classList.add('hl')); if ((await play(`ph:${e.p[i]}`)) === false) break; await wait(200); }
    spans.forEach(x => x.classList.remove('hl'));
    await teacher.say('ui:yourTurn');
  }
  const hint = h('p', { class: 'prompt' }, 'Say each sound, then tap its letter. Left to right.');
  s.append(hint);
  const pulse = () => teacher.point(box.querySelector('.g.next'));
  await ctx.instruct('ui:blendIntro', { nudge: 'ui:idleTap', hint: pulse });
  spans.forEach(x => x.classList.add('tap'));
  // a tile tapped out of order: "Start at the first letter." (only before it has been done)
  box.addEventListener('click', ev => { const g = ev.target.closest('.g'); if (g && !g.classList.contains('next') && !g.classList.contains('done')) { mark('wrong-tile', { word: item.w }); teacher.say('ui:wrongTile'); } });
  for (let i = 0; i < spans.length; i++) {
    spans[i].classList.add('next');
    await new Promise(r => spans[i].addEventListener('click', r, { once: true }));
    spans[i].classList.remove('next'); spans[i].classList.add('done');
    mark('tile', { word: item.w, i });
    await play(`ph:${e.p[i]}`);
  }
  hint.textContent = 'Now slide the sounds together and say it out loud.';
  const said = btn('I said it', 'mic', { class: 'btn primary saidit', say: 'ui:saidIt' });
  s.append(said, h('p', { class: 'selfreport' }, 'self-report: the app does not hear you'));
  await ctx.instruct('ui:blendSay', { nudge: 'ui:idleSay', hint: () => teacher.point(said) });
  await new Promise(r => said.addEventListener('click', r, { once: true }));
  mark('said-it', { word: item.w });
  await teacher.ack('sound');   // a self-report cannot be checked: acknowledge it, then the tap gate checks for real
  if (item.kind === 'syllable') return { judged: false };
  const r = await gate(ctx, item.w, item.kind);
  await ctx.record(item.w, item.kind, r);
  return r;
}
export async function blend(ctx, items) {
  const out = [];
  for (let i = 0; i < items.length; i++) out.push(await blendOne(ctx, items[i], { model: i === 0 && ctx.sitting.new?.length > 0 }));
  return out;
}
