// Before/after capture for Story (references/roles/evidence.md, "Before/after comparison").
// Copy into a git-excluded folder, fill in STEPS, then run it once per side with the same data:
//   sed -e "s#__OUT__#<screenshots>/before#" -e "s#__MODE__#before#" -e "s#__BASE_URL__#http://localhost:5173#" \
//     capture-template.js > capture.js
//   playwright-cli -s=<session> run-code --filename=capture.js
// Sign the session in first (log in, or `playwright-cli state-load <file>`); for several users,
// open one context per user from a saved storage state with page.context().browser().newContext().
async page => {
  const OUT = '__OUT__';
  const MODE = '__MODE__'; // before | after
  const BASE_URL = '__BASE_URL__';

  const open = async (url) => {
    await page.goto(`${BASE_URL}${url}`, { waitUntil: 'networkidle' });
    await page.waitForTimeout(500);
  };
  const snap = async (name) => {
    await page.waitForTimeout(600);
    await page.screenshot({ path: `${OUT}/${name}.png`, fullPage: true });
  };

  // Full-page shot with a red ring on every match and one numbered note per target, in
  // `${OUT}/marked/`. Targets: [{ loc, note, fit, skip }]. Locators must match both sides, so
  // select by stable label, structure or role, never by the value that changed.
  //   fit:  shrink a full-width block's ring to its text and put the note beside it
  //   skip: leave out matches whose parent's text contains this string
  const marked = async (name, targets) => {
    await page.waitForTimeout(600);
    for (const [i, t] of targets.entries()) {
      await t.loc.evaluateAll((all, { n, note, skip, fit }) => all
        .filter((el) => !skip || !el.parentElement.textContent.includes(skip))
        .forEach((el, k) => {
          if (fit) el.style.width = 'fit-content';
          el.style.outline = '3px solid #d32f2f';
          el.style.outlineOffset = '3px';
          el.dataset.storyMark = '1';
          if (k > 0) return; // one note per target, on its first match
          const r = el.getBoundingClientRect();
          const tag = document.createElement('div');
          tag.className = 'story-ann';
          tag.textContent = `${n}. ${note}`;
          Object.assign(tag.style, {
            position: 'absolute',
            left: `${Math.max(4, (fit ? r.right + 12 : r.left) + window.scrollX)}px`,
            top: `${(fit ? r.top - 3 : r.bottom + 6) + window.scrollY}px`,
            background: '#d32f2f', color: '#fff', font: '600 13px sans-serif', padding: '2px 8px',
            borderRadius: '4px', zIndex: 2147483647, pointerEvents: 'none', whiteSpace: 'nowrap',
          });
          document.body.appendChild(tag);
          // Right-aligned targets: pull the note back inside the page.
          const maxLeft = document.documentElement.clientWidth - tag.offsetWidth - 8;
          if (parseFloat(tag.style.left) > maxLeft) tag.style.left = `${maxLeft}px`;
        }), { n: i + 1, note: t.note, skip: t.skip, fit: !!t.fit });
    }
    await page.screenshot({ path: `${OUT}/marked/${name}.png`, fullPage: true });
    await page.evaluate(() => {
      document.querySelectorAll('.story-ann').forEach((tag) => tag.remove());
      document.querySelectorAll('[data-story-mark]').forEach((el) => {
        el.style.outline = '';
        el.style.outlineOffset = '';
        el.style.width = '';
        delete el.dataset.storyMark;
      });
    });
  };

  // STEPS: identical on both sides. For example:
  // await open('/orders');
  // await snap('01-order-list');
  // await marked('01-order-list', [
  //   { loc: page.getByText(/^Total:/), note: 'total', fit: true },
  //   { loc: page.getByRole('cell', { name: /^\d+(\.\d+)?$/ }), note: 'line amount' },
  // ]);
  // if (MODE === 'after') { /* AC annotations whose notes quote the new values */ }

  return `captured ${MODE}`;
}
