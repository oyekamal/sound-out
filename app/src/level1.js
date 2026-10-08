// Level 1 wiring: sittings for the Level 1 lessons the course writes as ONE sitting (no appSittings from parse_course),
// and the Level-1-only exercise steps (oral games, letter names vs sounds, b/d/p/q, the Level 1 mastery check).
// Data only here; the step screens live in screens/l1*.js and are registered in session.js via L1_STEPS.
const R = { id: 'R', steps: ['read'] }, L = { id: 'L', steps: ['listen'] }, X = { id: 'X', steps: ['check'] };
const SITTINGS = {
  // oral sound games, no letters until a preview of s and a at the end; its own check (bar 4/5 from the lesson)
  'L1.01': { A: [{ id: 'A', label: 'Sound games', steps: ['oral'] }, L, { id: 'X', steps: ['oralCheck'] }],
             B: [{ id: 'A', label: 'Sound games', steps: ['oral'] }, { id: 'L', label: 'Listen', steps: ['listen'] }, { id: 'X', steps: ['oralCheck'] }] },
  // FLOSS + plural: no new letter-sound, one sitting of words
  'L1.10': { A: [{ id: 'D', new: [], steps: ['warm', 'blend', 'tricky', 'spell'] }, R, L, X],
             B: [{ id: 'D', steps: ['warm', 'blend', 'tricky', 'read', 'listen'] }, X] },
  // review: all letters, names vs sounds, b/d/p/q; then words, tricky words (no, so), read, listen, check
  'L1.13': { A: [{ id: 'A', label: 'Names and sounds', steps: ['warm', 'names', 'bdpq'] }, { id: 'D', new: [], steps: ['blend', 'tricky', 'spell'] }, R, L, X],
             B: [{ id: 'A', label: 'Names and sounds', steps: ['warm', 'names', 'bdpq', 'blend'] }, { id: 'D', steps: ['tricky', 'read', 'listen'] }, X] },
  // Level 1 mastery check: its own bars; passing it (not just finishing it) opens Level 2
  'L1.14': { A: [L, { id: 'X', label: 'Level 1 check', steps: ['mastery'] }],
             B: [{ id: 'L', label: 'Listen', steps: ['listen'] }, { id: 'X', label: 'Level 1 check', steps: ['mastery'] }] },
};
export const fillL1 = l => (l.appSittings || !SITTINGS[l.id] ? l : { ...l, appSittings: SITTINGS[l.id] });
