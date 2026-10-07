// Discussion: reciprocal roles (Predictor, Questioner, Clarifier, Summarizer) as self-check practice.
import { h } from '../../ui.js';
import { mark } from '../../audio.js';
import { voice, reveal, selfMark } from './kit.js';

const GOOD = {
  Predictor: 'A good prediction names what the next part will explain, using a clue from the title or first sentence.',
  Questioner: 'A good question is one the text can answer (why, how, what would happen if), not a yes/no question.',
  Clarifier: 'A good clarify names the hard word or sentence, then works out its meaning from the words around it or its word parts.',
  Summarizer: 'A good summary gives the main point in one or two sentences, in your own words, with no small details.',
};

export async function discuss(ctx, S) {
  const id = S.id; const roles = S.discuss.roles;
  const s = ctx.stage();
  s.append(h('h2', {}, 'Talk about it'), h('p', { class: 'ss-instr' }, 'Take each role. Think (or say it to someone), then tap to see a good answer. Practice only.'));
  roles.forEach((r, i) => {
    s.append(h('div', { class: 'ss-card ss-role', 'data-role': r.role },
      h('p', { class: 'ss-label' }, r.role),
      h('div', { class: 'ss-qrow' }, h('p', { class: 'ss-q' }, r.prompt || GOOD[r.role] || ''), r.prompt ? voice(`ss:${id}:disc:${i}`, 'Hear the prompt') : null),
      reveal(r.model, { fallback: GOOD[r.role] || 'A good answer points to a sentence in the text.' }), selfMark(m => mark('ss-self', { block: 'discuss', i, m }))));
  });
  await ctx.next();
}
