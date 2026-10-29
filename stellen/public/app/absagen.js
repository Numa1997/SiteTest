// The /absagen page: the board's colour theme (same stored choice as the board), loading the mails in portions
// of 20 (each portion is a small request, which keeps the server inside Cloudflare's free-plan limits), and the
// print button, which waits until every mail is on the page. The page itself is written by the server (src/absagen.js);
// this file is the only script it may run, and it inserts only HTML from this site's own /absagen/part.
let theme = 'auto';
try { theme = JSON.parse(localStorage.getItem('radar.theme')) || 'auto'; } catch { /* private mode */ }
if (!['auto', 'light', 'dark'].includes(theme)) theme = 'auto';
document.documentElement.setAttribute('data-theme', theme);

document.addEventListener('DOMContentLoaded', () => {
  const root = document.querySelector('.absagen');
  const mails = document.getElementById('mails');
  const progress = document.getElementById('progress');
  const btn = document.getElementById('print');
  const total = Number(root.dataset.count) || 0;
  let wantPrint = false;
  let done = total === 0;

  const show = shown => { progress.textContent = shown >= total ? root.dataset.loaded + ' (' + total + ')' : root.dataset.loading + ' … ' + shown + ' / ' + total; };

  async function load() {
    let offset = 0;
    while (offset < total) {
      show(offset);
      const res = await fetch('/absagen/part?offset=' + offset + '&lang=' + encodeURIComponent(root.dataset.lang), { credentials: 'same-origin' });
      if (!res.ok) throw new Error('part ' + offset + ': ' + res.status);
      const got = Number(res.headers.get('X-Part-Count')) || 0;
      mails.insertAdjacentHTML('beforeend', await res.text());
      // Each mail body arrives inside a <template>, so the browser parses it on its own and nothing in it can
      // close the box around it; then it is moved into its box.
      for (const tpl of mails.querySelectorAll('template.mbt')) tpl.replaceWith(tpl.content);
      if (!got) break;
      offset += got;
    }
    show(total);
    done = true;
    document.getElementById('incomplete')?.remove();
    if (location.hash) document.getElementById(location.hash.slice(1))?.scrollIntoView();
    if (wantPrint) window.print();
  }
  if (!total) document.getElementById('incomplete')?.remove();
  if (total) load().catch(() => { progress.textContent = root.dataset.failed; progress.classList.add('bad'); });

  btn?.addEventListener('click', () => {
    if (done) window.print();
    else { wantPrint = true; btn.disabled = true; }
  });
});
