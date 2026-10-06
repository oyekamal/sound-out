// The path: every sitting of the playable lessons, in order. Sittings are on demand:
// the next one opens when the previous mini check passed. A missed "Show what you know" still opens the next lesson.
import { LESSONS, sittingsFor } from './content.js';
export function allSittings(track) { return LESSONS.flatMap(l => sittingsFor(l, track)); }
export function states(prog, track) {
  const list = allSittings(track);
  let open = true;
  return list.map(s => {
    const rec = prog.sittings[s.key];
    const st = rec?.passed ? 'done' : open ? 'open' : 'locked';
    open = !!(rec?.passed || (rec?.done && s.steps.includes('check')));
    return { ...s, state: st, rec };
  });
}
export function nextOpen(prog, track, afterKey) {
  const st = states(prog, track);
  const i = st.findIndex(s => s.key === afterKey);
  const n = st[i + 1];
  return n && n.state !== 'locked' ? n.key : null;
}
export const LABEL = {
  A: { A: null, B: null, C: null, D: 'Words', R: 'Read', L: 'Listen', X: 'Show what you know' },
  B: { D: 'Words and reading', X: 'Check' },
};
