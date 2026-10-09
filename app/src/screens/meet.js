// Meet it: the letter card. Tap the letter to hear its sound (its name is a separate, smaller button).
import { play } from '../audio.js';
import { teacher } from '../teacher.js';
import { h, speaker } from '../ui.js';
import { g2p } from '../content.js';

export async function meet(ctx, letter) {
  const pid = g2p[letter];
  const s = ctx.stage();
  let tapped = 0;
  const card = h('button', { class: 'lettercard', 'aria-label': `Letter ${letter}, tap to hear its sound` }, letter);
  card.addEventListener('click', async () => { card.classList.add('pop'); await play(`ph:${pid}`); card.classList.remove('pop'); tapped++; ctx.enableNext(); });
  s.append(h('h2', {}, 'This letter makes that sound'), card,
    h('div', { class: 'row small' }, speaker(`name:${letter}`, { label: 'Hear its name' }), h('span', { class: 'muted' }, `its name — when we read, we use its sound`)));
  // model first: "This letter is <name> and it says <sound>", then "tap it to hear it" (nothing is asked before it is shown)
  await ctx.instruct(['ui:thisLetterIs', `name:${letter}`, 'ui:andSays', `ph:${pid}`, 'ui:meetIntro'], { nudge: 'ui:idleTap', hint: () => teacher.point(card) });
  await ctx.next({ disabledUntil: () => tapped > 0 });
}
