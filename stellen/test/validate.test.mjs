// node --test test/*.test.mjs
import test from 'node:test';
import assert from 'node:assert/strict';
import { validPatch, validItem, cleanPosting, ApiError } from '../src/validate.js';
import { toSql } from '../tools/to-sql.mjs';
import { readFileSync } from 'node:fs';

test('marks: accepted and refused patches', () => {
  assert.ok(validPatch({ outcome: 'applied', outcome_at: '2026-10-20T10:00:00.000Z' }));
  assert.ok(validPatch({ outcome: null, outcome_at: null }));
  assert.ok(validPatch({ snapshot: { title: 'x', n: 3 } }));
  assert.ok(!validPatch({ outcome: 'hired' }));
  assert.ok(!validPatch({ evil: 1 }));
  assert.ok(!validPatch({ snapshot: { title: 'x', script: '<b>' } }));
  assert.ok(!validPatch({ note: 'x'.repeat(5001) }));
  assert.ok(!validPatch([]));
  assert.ok(validItem('j12') && validItem('a1792000000000') && !validItem('x1') && !validItem("j1' or 1=1"));
});

test('added postings: cleaned, and the first bad field is named', () => {
  const p = cleanPosting({ url: 'https://example.com/a', title: '  Physiker  (m/w/d) ', city: 'Leipzig', area: 'leipzig', category: 'physiker' });
  assert.equal(p.title, 'Physiker (m/w/d)');
  const field = input => { try { cleanPosting(input); } catch (e) { assert.ok(e instanceof ApiError); return e.extra.field; } };
  assert.equal(field({ url: 'javascript:alert(1)', title: 't', city: 'c', area: 'berlin', category: 'pm' }), 'url');
  assert.equal(field({ url: 'https://u:p@example.com', title: 't', city: 'c', area: 'berlin', category: 'pm' }), 'url');
  assert.equal(field({ url: 'https://example.com', title: '', city: 'c', area: 'berlin', category: 'pm' }), 'title');
  assert.equal(field({ url: 'https://example.com', title: 't', city: 'c', area: 'mars', category: 'pm' }), 'area');
});

test('importer: invented seed turns into SQL; older marks get an outcome; bad input stops it', () => {
  const seed = JSON.parse(readFileSync(new URL('./seed.json', import.meta.url), 'utf8'));
  const sql = toSql(seed);
  assert.match(sql, /insert or ignore into marks .*'j5', 'applied'/);
  assert.doesNotMatch(sql, /delete from|into application_log|into postings|into meta/, 'the default import leaves the list and the e-mail log alone');
  const full = toSql(seed, { replaceList: true });
  assert.match(full, /'rule_de'/);
  assert.match(full, /delete from application_log;/);
  assert.throws(() => toSql({ ...seed, postings: [...seed.postings, { ...seed.postings[0] }] }), /duplicate n/);
  assert.throws(() => toSql({ ...seed, postings: [{ ...seed.postings[0], category: 'astrology' }] }), /unknown category/);
  assert.throws(() => toSql({ ...seed, applicationLog: [{ ...seed.applicationLog[0], cards: [999] }] }), /card numbers/);
  const quoted = toSql({ ...seed, postings: [{ ...seed.postings[0], company: "O'Neill & Söhne" }, ...seed.postings.slice(1)] }, { replaceList: true });
  assert.match(quoted, /'O''Neill & Söhne'/);
});
