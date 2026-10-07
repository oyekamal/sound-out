// Level 1 wiring: sittings for the Level 1 lessons the course writes as ONE sitting (no appSittings from parse_course),
const R = { id: 'R', steps: ['read'] }, L = { id: 'L', steps: ['listen'] }, X = { id: 'X', steps: ['check'] };
const SITTINGS = {
  'L1.10': { A: [{ id: 'D', new: [], steps: ['warm', 'blend', 'tricky', 'spell'] }, R, L, X],
             B: [{ id: 'D', steps: ['warm', 'blend', 'tricky', 'read', 'listen'] }, X] },
};
export const fillL1 = l => (l.appSittings || !SITTINGS[l.id] ? l : { ...l, appSittings: SITTINGS[l.id] });
