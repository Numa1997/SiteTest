// The Access token check, against a key pair made here (no network).
import test from 'node:test';
import assert from 'node:assert/strict';
import { verifyAccessToken, requireOwner } from '../src/access.js';

const TEAM = 'https://numa-test.cloudflareaccess.com';
const AUD = 'aud-tag-123';
const b64url = buf => Buffer.from(buf).toString('base64url');

async function setup() {
  const pair = await crypto.subtle.generateKey({ name: 'RSASSA-PKCS1-v1_5', modulusLength: 2048, publicExponent: new Uint8Array([1, 0, 1]), hash: 'SHA-256' }, true, ['sign', 'verify']);
  const jwk = { ...(await crypto.subtle.exportKey('jwk', pair.publicKey)), kid: 'k1' };
  const fetcher = async url => { assert.equal(url, TEAM + '/cdn-cgi/access/certs'); return new Response(JSON.stringify({ keys: [jwk] })); };
  const sign = async (payload, header = { alg: 'RS256', kid: 'k1' }) => {
    const head = b64url(JSON.stringify(header)) + '.' + b64url(JSON.stringify(payload));
    return head + '.' + b64url(await crypto.subtle.sign('RSASSA-PKCS1-v1_5', pair.privateKey, new TextEncoder().encode(head)));
  };
  return { fetcher, sign };
}

test('Access token: valid passes; wrong audience, issuer, expiry or signature fail', async () => {
  const { fetcher, sign } = await setup();
  const now = Math.floor(Date.now() / 1000);
  const good = { iss: TEAM, aud: [AUD], email: 'Owner@Example.test', exp: now + 600, nbf: now - 10 };
  assert.equal((await verifyAccessToken(await sign(good), { team: TEAM, aud: AUD, fetcher })).email, 'Owner@Example.test');
  for (const bad of [{ ...good, aud: ['other'] }, { ...good, iss: 'https://evil.cloudflareaccess.com' }, { ...good, exp: now - 600 }]) {
    await assert.rejects(verifyAccessToken(await sign(bad), { team: TEAM, aud: AUD, fetcher }), e => e.status === 401);
  }
  const forged = (await sign(good)).replace(/\.[^.]+$/, '.' + b64url(new Uint8Array(256)));
  await assert.rejects(verifyAccessToken(forged, { team: TEAM, aud: AUD, fetcher }), e => e.status === 401);
  await assert.rejects(verifyAccessToken(await sign(good, { alg: 'none', kid: 'k1' }), { team: TEAM, aud: AUD, fetcher }), e => e.status === 401);
  await assert.rejects(verifyAccessToken(undefined, { team: TEAM, aud: AUD, fetcher }), e => e.status === 401);
});

test('owner check: nobody in when not configured; the local shortcut only on localhost', async () => {
  const req = (host, headers = {}) => new Request('https://' + host + '/api/marks', { headers });
  await assert.rejects(requireOwner(req('stellen.phyeinusul.com'), {}), e => e.status === 503 && e.code === 'not_configured');
  await assert.rejects(requireOwner(req('stellen.phyeinusul.com'), { DEV_OWNER_EMAIL: 'a@b.test' }), e => e.status === 503);
  assert.equal(await requireOwner(new Request('http://localhost:8787/api/marks'), { DEV_OWNER_EMAIL: 'A@b.test' }), 'a@b.test');
  const env = { ACCESS_TEAM_DOMAIN: TEAM, ACCESS_AUD: AUD, OWNER_EMAILS: 'owner@example.test' };
  await assert.rejects(requireOwner(req('stellen.phyeinusul.com'), env), e => e.status === 401);
});
