// Picture-card option sets for the oral (no-reading) answer screens. Pure: no DOM, no imports, so a Node script can audit it
// (tools/count_speaker_only.mjs). The caller injects what the app knows (pictures, ambiguity, audio, lexicon).
//
// A set is three cards: the target and two distractors. Rules, in order:
//  1. A distractor must have a clear picture (a file, not `ambiguous`) AND a whole-word clip (the card plays it).
//  2. A distractor that fails is swapped for another word that follows the same item rule: a different word whose sounds differ,
//     preferably with a different first sound, close in length, and the two distractors differing from each other.
//     Candidates come from the lesson's own pool first, then Level 1 words, then any real word. Order is a hash of the target,
//     so the same item always gets the same cards.
//  3. An ambiguous TARGET keeps its picture and the small printed word goes under it (labels on EVERY card of that set, so the
//     target is not the odd one out).
//  4. Speaker-only is the last resort: fewer than two valid distractors, or the target has no picture file at all.

// small stable string hash -> uint32 (FNV-1a)
export const hash = s => { let x = 2166136261; for (let i = 0; i < s.length; i++) { x ^= s.charCodeAt(i); x = Math.imul(x, 16777619); } return x >>> 0; };
// deterministic shuffle: the order depends only on the seed string
export const seededShuffle = (arr, seed) => arr.map(v => [hash(`${seed}|${v}`), v]).sort((a, b) => a[0] - b[0]).map(x => x[1]);

// env = { hasPic(w), isAmb(w), hasClip(w), phones(w) -> array|null, isReal(w), level1(w), universe: [words] }
export function buildSet(target, pool, env, { seed = target } = {}) {
  const tp = env.phones(target) || [];
  const clear = w => env.hasPic(w) && !env.isAmb(w) && env.hasClip(w);
  const valid = w => w !== target && clear(w) && env.isReal(w) && env.phones(w)
    && env.phones(w).join(' ') !== tp.join(' ');
  const seen = new Set();
  const tier = (words, name) => seededShuffle(words.filter(w => valid(w) && !seen.has(w) && seen.add(w)), `${seed}|${name}`);
  // original pool first (the words this lesson already uses), then Level 1 words, then everything else
  const cands = [...tier(pool, 'pool'), ...tier(env.universe.filter(env.level1), 'l1'), ...tier(env.universe, 'all')];
  const picked = [];
  const fits = (w, strict) => {
    const p = env.phones(w);
    if (strict) {
      if (p[0] === tp[0]) return false;                              // same first sound as the target is a different, harder task
      if (Math.abs(p.length - tp.length) > 1) return false;
      if (picked.some(x => env.phones(x)[0] === p[0])) return false; // distractors differ from each other
    }
    return true;
  };
  for (const strict of [true, false]) {
    for (const w of cands) { if (picked.length >= 2) break; if (!picked.includes(w) && fits(w, strict)) picked.push(w); }
  }
  if (picked.length < 2 || !env.hasPic(target)) {
    const rest = seededShuffle(pool.filter(w => w !== target && !picked.includes(w)), `${seed}|rest`);
    return { words: seededShuffle([target, ...picked, ...rest].slice(0, 3), `${seed}|order`), pictured: false, labelled: false, swapped: 0, speakerOnly: true }; }
  const words = seededShuffle([target, ...picked], `${seed}|order`);
  const inPool = new Set(pool);
  return { words, pictured: true, labelled: env.isAmb(target) || !clear(target), swapped: picked.filter(w => !inPool.has(w)).length, speakerOnly: false };
}
