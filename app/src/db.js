// IndexedDB: profiles, per-profile progress, Leitner review cards, days practised. Nothing leaves the phone.
const NAME = 'sound-out', VERSION = 1;
let dbp;
function open() {
  if (dbp) return dbp;
  dbp = new Promise((res, rej) => {
    const r = indexedDB.open(NAME, VERSION);
    r.onupgradeneeded = () => {
      const d = r.result;
      d.createObjectStore('settings', { keyPath: 'key' });
      d.createObjectStore('profiles', { keyPath: 'id' });
      d.createObjectStore('progress', { keyPath: 'id' });            // {id: profileId, sittings:{key:{done, mini, at}}, lessons:{id:{state, score}}, stickers, village, days:[]}
      const c = d.createObjectStore('cards', { keyPath: 'id' });       // {id: profileId+':'+item, profileId, item, kind, box, due}
      c.createIndex('profileId', 'profileId');
    };
    r.onsuccess = () => res(r.result);
    r.onerror = () => rej(r.error);
  });
  return dbp;
}
async function tx(store, mode, fn) {
  const d = await open();
  return new Promise((res, rej) => {
    const t = d.transaction(store, mode), st = t.objectStore(store);
    let out; const r = fn(st);
    if (r) r.onsuccess = () => { out = r.result; };
    t.oncomplete = () => res(out); t.onerror = () => rej(t.error);
  });
}
export const get = (s, k) => tx(s, 'readonly', st => st.get(k));
export const put = (s, v) => tx(s, 'readwrite', st => st.put(v));
export const all = s => tx(s, 'readonly', st => st.getAll());
export const byProfile = (s, pid) => tx(s, 'readonly', st => st.index('profileId').getAll(pid));
export async function setting(key, value) {
  if (value === undefined) return (await get('settings', key))?.value;
  return put('settings', { key, value });
}
export async function progress(pid) {
  return (await get('progress', pid)) || { id: pid, sittings: {}, lessons: {}, stickers: [], village: [], days: [], sittingCount: 0 };
}
export const saveProgress = p => put('progress', p);
