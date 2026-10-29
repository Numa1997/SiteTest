// Start-up order, and nothing else: load the list and the marks, render,
// then re-read every minute. When loading fails, say why in the reader's
// language: sign-in not set up, no access, session expired, or no answer.
// Sign-in itself happens before this page loads, at Cloudflare Access.
import { readDossier, loadMarks, watchData, SIGN_OUT_URL } from './api.js';
import { renderPage } from './page.js';
import { t, applyDocument } from './i18n.js';

const mount = document.getElementById('app');
applyDocument();
const bootMsg = document.getElementById('boot-msg');
if (bootMsg) bootMsg.textContent = t('boot.loading');
const slow = setTimeout(() => {
  const m = document.getElementById('boot-msg');
  if (m) m.textContent = t('boot.slow');
}, 20000);

function card({ title, text, button, href, onClick }) {
  const gate = document.createElement('div');
  gate.className = 'gate';
  const box = document.createElement('div');
  box.className = 'gate__card';
  const kicker = document.createElement('p');
  kicker.className = 'gate__kicker';
  kicker.textContent = t('app.kicker');
  const h = document.createElement('h1');
  h.className = 'gate__title';
  h.textContent = title;
  const p = document.createElement('p');
  p.className = 'gate__text';
  p.textContent = text;
  box.append(kicker, h, p);
  if (button) {
    const b = document.createElement(href ? 'a' : 'button');
    b.className = 'gate__btn';
    b.textContent = button;
    if (href) b.href = href; else { b.type = 'button'; b.onclick = onClick; }
    box.append(b);
  }
  gate.append(box);
  mount.replaceChildren(gate);
}

async function main() {
  try {
    const [dossier, marks] = await Promise.all([readDossier(), loadMarks()]);
    clearTimeout(slow);
    const page = renderPage(mount, { ...dossier, marks });
    const stop = watchData(next => page.updateData(next));
    addEventListener('pagehide', stop, { once: true });
  } catch (error) {
    clearTimeout(slow);
    const code = error?.data?.error;
    if (code === 'not_configured') return card({ title: t('setup.title'), text: t('setup.text') });
    if (code === 'no_access') {
      return card({ title: t('noaccess.title'), text: t('noaccess.text', { email: error.data.email || t('noaccess.someone') }),
        button: t('util.sign_out'), href: SIGN_OUT_URL });
    }
    if (error?.status === 401) return card({ title: t('session.title'), text: t('session.text'), button: t('session.reload'), onClick: () => location.reload() });
    card({ title: t('fatal.title'), text: t('fatal.text'), button: t('fatal.retry'), onClick: main });
  }
}
main();
