import './style.css';
import * as db from './db.js';
import { onboarding } from './onboarding.js';
import { home } from './home.js';
import { runSitting } from './session.js';
import { nextOpen, allSittings } from './path.js';
import { stop } from './audio.js';
import { initNative } from './native.js';
import { teacher } from './teacher.js';
import { tilo } from './tilo.js';
import { privacyScreen } from './privacy.js';
import './screens/session/index.js'; // Levels 5-7 practice (Library + session screens)

const root = document.getElementById('app');
let profile = null;
const app = {
  mount(el) { tilo.setHome(null); root.replaceChildren(el); window.scrollTo(0, 0); teacher.newScreen(); },
  async boot() {
    const id = await db.setting('active');
    profile = id ? await db.get('profiles', id) : null;
    if (!profile) { tilo.setTrack(null); return onboarding(app); }
    teacher.track(profile.track);
    return home(app, profile);
  },
  home() { stop(); return home(app, profile); },
  privacyInfo() { stop(); return privacyScreen(app); },
  onboarding() { stop(); teacher.track(null); return onboarding(app); },
  async firstSitting(p) { profile = p; teacher.track(p.track); return app.sitting(allSittings(p.track)[0].key); },
  async sitting(key) { stop(); try { await runSitting(app, profile, key); } catch (e) { console.error(e); app.home(); } },
  nextOpen: (prog, track, key) => nextOpen(prog, track, key),
};
window.__so = window.__so || { trace: [], missing: [] };
window.__so.app = app;
teacher.start();
initNative(app);
app.boot();
