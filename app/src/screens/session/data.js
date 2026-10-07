// Level 5-7 practice content: content/sessions/*.json from tools/parse_sessions.py, loaded per lesson on demand.
import index from '../../../../content/sessions/index.json';
const files = import.meta.glob('../../../../content/sessions/L*.json', { import: 'default' });
export const SESSIONS = index;
export const LEVELS = [...new Set(index.map(x => x.level))].sort();
export async function loadSession(id) {
  const k = Object.keys(files).find(p => p.endsWith(`/${id}.json`));
  if (!k) throw new Error(`no session ${id}`);
  return files[k]();
}
// The passages a learner reads: Level 5 has Track A (child) and Track B (teen/adult) texts; Levels 6-7 have one set.
export function passagesFor(S, track) {
  const ps = S.text?.passages || [];
  const mine = ps.filter(p => !p.track || p.track === track);
  return mine.length ? mine : ps;
}
