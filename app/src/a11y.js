// Screen-change accessibility, in one place.
//   screenChanged()  after every new screen (teacher.newScreen): move focus to the screen's heading, keep ONE h1,
//                    set document.title, tidy the ear button's DOM spot so tab order matches its look.
//   announce(text)   a short status in the single visually hidden live region (#live). #app itself is NOT live.
const BRAND = 'Sound Out';
let timer = null, tries = 0;

export function announce(text) {
  const el = document.getElementById('live');
  if (!el || !text) return;
  el.textContent = '';
  setTimeout(() => { el.textContent = text; }, 40);
}

// the ear button is fixed top-right: put it last in the screen's header (right end of the row) so Tab follows the picture
export function placeEar(ear) {
  if (!ear) return;
  const root = document.getElementById('app');
  const hdr = root?.querySelector('header');
  if (hdr) { if (ear.parentElement !== hdr) hdr.append(ear); }
  else if (ear.parentElement !== document.body || ear.nextElementSibling !== root) document.body.insertBefore(ear, root);
}

function settle() {
  const root = document.getElementById('app');
  if (!root) return;
  let head = root.querySelector('h1, h2');
  if (!head && tries++ < 1) { timer = setTimeout(settle, 250); return; }
  if (!head) {   // a screen with no heading of its own: keep focus on the screen itself so Tab starts from here, not from the top of the page
    head = root.querySelector('.screen') || root.firstElementChild;
    if (!head || document.querySelector('.gu-wrap, #teacher-start')) return;
    head.setAttribute('tabindex', '-1'); try { head.focus({ preventScroll: true }); } catch { /* gone */ }
    return;
  }
  if (!root.querySelector('h1')) { head.setAttribute('role', 'heading'); head.setAttribute('aria-level', '1'); }   // one h1 per screen
  const name = head.textContent.trim();
  if (name) document.title = `${name} - ${BRAND}`;
  if (document.querySelector('.gu-wrap, #teacher-start')) return;   // a dialog owns focus right now
  head.setAttribute('tabindex', '-1');
  try { head.focus({ preventScroll: true }); } catch { /* gone */ }
}

export function screenChanged() {
  clearTimeout(timer); tries = 0;
  timer = setTimeout(settle, 90);
}
