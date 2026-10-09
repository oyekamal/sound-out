// Hear it: the new sound, twice, then a word that starts with it. Mouth cue as text.
import { play, wait } from '../audio.js';
import { h, speaker, pebble } from '../ui.js';
import { g2p } from '../content.js';

export async function hear(ctx, letter) {
  const pid = g2p[letter];
  const src = ctx.lessonSitting(letter);
  const s = ctx.stage();
  const exKey = `ex:${ctx.lesson.id}:${src?.id}`;
  const cue = src?.meet?.mouthCue;
  s.append(
    ctx.track === 'A' ? pebble('wave') : null,
    h('h2', {}, 'Listen to this sound'),
    speaker(`ph:${pid}`, { big: true, label: 'Play the sound' }),
    cue ? h('div', { class: 'cue' }, h('b', {}, 'Your mouth: '), cue) : null,
    h('div', { class: 'row' }, speaker(exKey, { label: 'Hear the example word' }), h('span', { class: 'muted' }, 'a word that starts with it')),
  );
  // the sound twice, then "you can hear it at the start of this word": the ear button plays all of it again
  const model = async () => {
    for (let i = 0; i < 2; i++) { if ((await play(`ph:${pid}`)) === false) return false; await wait(400); }
    if ((await play('ui:hearExample')) === false) return false;
    return play(exKey);
  };
  await ctx.instruct('ui:hearIntro', { stim: model, nudge: 'ui:idleTap' });
  await ctx.next();
}
