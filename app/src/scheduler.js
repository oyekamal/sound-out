// Leitner review, scheduled in sittings (not days): boxes 1-5 come back after 1, 2, 4, 8, 16 sittings.
import * as db from './db.js';
const GAP = [0, 1, 2, 4, 8, 16];
export async function review(pid, item, kind, correct, sittingCount) {
  const id = `${pid}:${item}`;
  const c = (await db.get('cards', id)) || { id, profileId: pid, item, kind, box: 1, wrongRun: 0 };
  if (correct) { c.box = Math.min(5, c.box + 1); c.wrongRun = 0; }
  else { c.wrongRun = (c.wrongRun || 0) + 1; c.box = c.wrongRun >= 2 ? 1 : Math.max(1, c.box - 1); }
  c.due = sittingCount + GAP[c.box];
  await db.put('cards', c);
}
export async function due(pid, sittingCount, max) {
  const cs = (await db.byProfile('cards', pid)).filter(c => c.due <= sittingCount);
  return cs.sort((a, b) => a.box - b.box || a.due - b.due).slice(0, max);
}
