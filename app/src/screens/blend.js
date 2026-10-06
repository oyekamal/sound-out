// E5 Blend it: tap each letter left to right (its sound plays AFTER the tap), say the word
// (self-report: the app does not hear you), then the tap gate on the same word.
import { play, wait, mark } from '../audio.js';
import { h } from '../ui.js';
import { entry } from '../content.js';
import { gate, printedWord } from '../gate.js';

export async function blendOne(ctx, item, { model = false } = {}) {
  const e = entry(item.w);
  const s = ctx.stage();
  const box = printedWord(item.w, item.kind === 'syllable' ? null : item.kind, ctx.track);
  box.classList.add('tiles');
  const spans = [...box.querySelectorAll('.g')];
  s.append(h('h2', {}, item.kind === 'syllable' ? 'A practice sound (not a word yet)' : 'Blend it'), box);
  if (model) {
    await ctx.instruct('ui:blendModel');
    for (let i = 0; i < spans.length; i++) { spans.slice(0, i + 1).forEach(x => x.classList.add('hl')); await play(`ph:${e.p[i]}`); await wait(200); }
    spans.forEach(x => x.classList.remove('hl'));
  }
  const hint = h('p', { class: 'prompt' }, 'Say each sound, then tap its letter. Left to right.');
  s.append(hint);
  await ctx.instruct('ui:blendIntro');
  spans.forEach(x => x.classList.add('tap'));
  for (let i = 0; i < spans.length; i++) {
    spans[i].classList.add('next');
    await new Promise(r => spans[i].addEventListener('click', r, { once: true }));
    spans[i].classList.remove('next'); spans[i].classList.add('done');
    mark('tile', { word: item.w, i });
    await play(`ph:${e.p[i]}`);
  }
  hint.textContent = 'Now slide the sounds together and say it out loud.';
  await ctx.instruct('ui:blendSay');
  const said = h('button', { class: 'btn primary saidit' }, 'I said it');
  s.append(said, h('p', { class: 'selfreport' }, 'self-report: the app does not hear you'));
  await new Promise(r => said.addEventListener('click', r, { once: true }));
  mark('said-it', { word: item.w });
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
