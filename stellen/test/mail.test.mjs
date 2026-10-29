// The Gmail script's sign-in (service token) and what the server accepts from it. No network.
import test from 'node:test';
import assert from 'node:assert/strict';
import { requireService, requireOwner } from '../src/access.js';
import { cleanMessage, validIds, companyMatches, titleScore, sender, planLog } from '../src/mail.js';

const TEAM = 'https://numa-test.cloudflareaccess.com';
const AUD = 'aud-tag-123';
const CLIENT = '0123456789abcdef0123456789abcdef.access';
const b64url = buf => Buffer.from(buf).toString('base64url');

async function signer() {
  const pair = await crypto.subtle.generateKey({ name: 'RSASSA-PKCS1-v1_5', modulusLength: 2048, publicExponent: new Uint8Array([1, 0, 1]), hash: 'SHA-256' }, true, ['sign', 'verify']);
  const jwk = { ...(await crypto.subtle.exportKey('jwk', pair.publicKey)), kid: 'k-svc' };
  globalThis.fetch = async () => new Response(JSON.stringify({ keys: [jwk] }));   // the Access certs endpoint, faked
  return async payload => {
    const head = b64url(JSON.stringify({ alg: 'RS256', kid: 'k-svc' })) + '.' + b64url(JSON.stringify(payload));
    return head + '.' + b64url(await crypto.subtle.sign('RSASSA-PKCS1-v1_5', pair.privateKey, new TextEncoder().encode(head)));
  };
}

test('service token: only the configured Client ID gets in; an e-mail session does not; nothing configured = nobody', async () => {
  const sign = await signer();
  const now = Math.floor(Date.now() / 1000);
  const env = { ACCESS_TEAM_DOMAIN: TEAM, ACCESS_AUD: AUD, INGEST_CLIENT_ID: CLIENT, OWNER_EMAILS: 'owner@example.test' };
  const req = token => new Request('https://stellen.phyeinusul.com/api/ingest/known', { method: 'POST', headers: { 'Cf-Access-Jwt-Assertion': token } });
  const svc = { type: 'app', iss: TEAM, aud: [AUD], common_name: CLIENT, sub: '', exp: now + 600 };
  assert.equal(await requireService(req(await sign(svc)), env), CLIENT);
  await assert.rejects(requireService(req(await sign({ ...svc, common_name: 'ffffffffffffffffffffffffffffffff.access' })), env), e => e.status === 403);
  await assert.rejects(requireService(req(await sign({ ...svc, email: 'owner@example.test' })), env), e => e.status === 403);
  await assert.rejects(requireService(req(await sign({ ...svc, aud: ['other'] })), env), e => e.status === 401);
  await assert.rejects(requireService(req(await sign(svc)), { ...env, INGEST_CLIENT_ID: '' }), e => e.status === 503);
  // the service token cannot open the owner's routes (it has no e-mail)
  await assert.rejects(requireOwner(req(await sign(svc)), env), e => e.status === 403);
  // the local shortcut needs localhost AND the header
  const local = new Request('http://localhost:8787/api/ingest/known', { method: 'POST', headers: { 'X-Dev-Service': 'dev-svc' } });
  assert.equal(await requireService(local, { DEV_SERVICE_ID: 'dev-svc' }), 'dev-svc');
  await assert.rejects(requireService(new Request('https://stellen.phyeinusul.com/x', { headers: { 'X-Dev-Service': 'dev-svc' } }), { DEV_SERVICE_ID: 'dev-svc' }), e => e.status === 503);
});

const good = {
  gmail_id: '1a186e357d62d917', thread_id: '1a186e357d62d917', received_at: '2026-10-29T09:12:00Z',
  from: '"Linamar" <notifications@app.softgarden.io>', to: 'numa@example.test', subject: 'Ihre Bewerbung bei Linamar',
  labels: ['Absagen'], snippet: 'Guten Tag', text: 'Leider müssen wir Ihnen mitteilen …',
  html: '<p onclick="x()">Leider müssen wir Ihnen mitteilen, dass wir Sie nicht berücksichtigen.</p><img src="cid:logo">', attachments: [],
  images: [{ cid: 'logo', mime: 'image/png', b64: 'iVBORw0KGgo=' }, { cid: 'evil', mime: 'text/html', b64: 'PGI+' }],
};

test('a mail from the script: cleaned on arrival, long headers cut, structural errors refused', () => {
  const row = cleanMessage(good);
  assert.equal(row.gmail_id, good.gmail_id);
  assert.equal(row.received_at, '2026-10-29T09:12:00.000Z');
  assert.equal(row.body_html, '<p>Leider müssen wir Ihnen mitteilen, dass wir Sie nicht berücksichtigen.</p><img src="/absagen/img/1a186e357d62d917/0">');
  assert.equal(row.images.length, 1, 'only real images are kept');
  assert.equal(cleanMessage({ ...good, subject: 'x'.repeat(5000) }).subject.length, 1000);
  assert.equal(cleanMessage({ ...good, to: 'a@b.c, '.repeat(2000) }).to_header.length, 2000);
  assert.equal(cleanMessage({ ...good, html: '<p>' + 'x'.repeat(500_000) + '</p>' }).body_html, '', 'too long: shown as text');
  for (const bad of [{ ...good, gmail_id: '../x' }, { ...good, labels: ['uncertain rejection'] }, { ...good, received_at: 'yesterday' }, { ...good, extra: 1 }]) {
    assert.throws(() => cleanMessage(bad), e => e.status === 400);
  }
  assert.deepEqual(validIds({ gmail_ids: ['1a186e357d62d917', '1a186e357d62d917'] }), ['1a186e357d62d917']);
  assert.throws(() => validIds({ gmail_ids: ['x'] }), e => e.status === 400);
});

test('matching a mail to the e-mail log: sender and subject only, reference numbers decide', () => {
  assert.equal(sender('"Linamar" <notifications@app.softgarden.io>').orgLabel, '');
  assert.equal(sender('jobs@ferchau.com').orgLabel, 'ferchau');
  assert.ok(sender('rulemapping-jobs@m.personio.com').tokens.includes('rulemapping'));
  assert.ok(companyMatches('Linamar Casting Solutions Leipzig GmbH', { from_header: good.from, subject: good.subject, body_text: '' }));
  assert.ok(companyMatches('rulemapping', { from_header: 'rulemapping-jobs@m.personio.com', subject: 'Deine Bewerbung als Automation Engineer', body_text: '' }));
  assert.ok(companyMatches('ZEISS', { from_header: 'zeissgroup@myworkday.com', subject: 'Your application', body_text: '' }));
  assert.ok(!companyMatches('ZEISS', { from_header: 'jobs@fraunhofer.example', subject: 'Ihre Bewerbung', body_text: 'Wie bei ZEISS üblich …' }), 'a body mention is not a match');
  const se = { from_header: 'talent-acquisition.hr@siemens-energy.com', subject: 'An update on your Siemens Energy application',
    body_text: 'Thank you for applying for the role of Data Analytics Engineer (f/m/d) (305686) at Siemens Energy.' };
  assert.ok(titleScore('Data Analytics Engineer (f/m/d) (305686)', se) > titleScore('Field Service Engineer (w/m/d) substation automation (297978)', se));
});

// A stand-in for D1 that records what would be written.
const fakeDb = { prepare: sql => ({ bind: (...args) => ({ sql, args }) }) };
const mailOf = (o = {}) => ({ gmail_id: 'bbbb000000000001', received_at: '2026-10-20T08:00:00.000Z', from_header: 'jobs@zeissgroup.example',
  subject: 'Your application at ZEISS', body_text: '', ...o });

test('the log: open row closed with old values kept; interviews never closed; unclear cases get their own row', () => {
  const at = '2026-10-29T12:00:00.000Z';
  let p = planLog(fakeDb, [{ id: 'z1', company: 'ZEISS', title: 'Physiker', status: 'confirmed', date: '2026-10-01', note: 'n', source: 's' }], mailOf(), at);
  assert.equal(p.logId, 'z1');
  assert.match(p.statements[0].sql, /^update application_log/);
  assert.deepEqual(JSON.parse(p.statements[1].args[3]).before, { status: 'confirmed', date: '2026-10-01', note: 'n', source: 's' });
  p = planLog(fakeDb, [{ id: 'z1', company: 'ZEISS', title: 'Physiker', status: 'interview', date: '2026-10-01', note: '', source: '' }], mailOf(), at);
  assert.equal(p.logId, 'mail-bbbb000000000001', 'interview untouched, own row instead');
  assert.match(p.statements[0].sql, /^insert into application_log/);
  p = planLog(fakeDb, [{ id: 'z1', company: 'ZEISS', title: 'Physiker', status: 'rejected', date: '2026-10-19', note: '', source: '' }], mailOf(), at);
  assert.equal(p.logId, 'z1');
  assert.equal(p.statements.length, 1, 'already rejected: linked only');
  p = planLog(fakeDb, [], mailOf({ received_at: '2024-11-29T08:00:00.000Z' }), at);
  assert.equal(p.logId, null, 'before the log began: no log change');
});
