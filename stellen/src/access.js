// Who is asking. Sign-in is done by Cloudflare Access in front of the
// Worker: a visitor without a valid Access session never reaches it. Access
// then adds a signed token (a JWT) to every request in the header
// Cf-Access-Jwt-Assertion. This file checks that token again, so the Worker
// trusts nothing it cannot verify itself:
//   1. the signature, with Access's public keys from <team>/cdn-cgi/access/certs (RS256);
//   2. the issuer (the team domain), the audience (this application's AUD tag), the expiry;
//   3. the e-mail address, against OWNER_EMAILS.
// https://developers.cloudflare.com/cloudflare-one/identity/authorization-cookie/validating-json/
//
// Configuration (Worker variables): ACCESS_TEAM_DOMAIN (https://<team>.cloudflareaccess.com),
// ACCESS_AUD, OWNER_EMAILS (comma-separated). If any is missing, every API
// request is refused (503 not_configured): the safe failure is "nobody in".
//
// Local development only: with DEV_OWNER_EMAIL set (in .dev.vars, which is
// never uploaded) and the request addressed to localhost, that e-mail is
// taken as signed in. Both conditions must hold.
//
// The Gmail script (the only machine caller) signs in with an Access SERVICE
// TOKEN instead of an e-mail. Access then puts the token's Client ID into the
// JWT claim common_name and leaves email empty. requireService() accepts only
// that one Client ID (INGEST_CLIENT_ID) and only on the ingest routes;
// requireOwner() refuses it everywhere else, because it carries no e-mail.
import { ApiError } from './validate.js';

let keyCache = { team: '', at: 0, keys: new Map() };
const KEY_TTL_MS = 60 * 60 * 1000;

const b64urlBytes = s => {
  const b = atob(s.replace(/-/g, '+').replace(/_/g, '/') + '==='.slice((s.length + 3) % 4));
  return Uint8Array.from(b, c => c.charCodeAt(0));
};
const b64urlJson = s => JSON.parse(new TextDecoder().decode(b64urlBytes(s)));

async function publicKey(team, kid, fetcher) {
  const fresh = keyCache.team === team && Date.now() - keyCache.at < KEY_TTL_MS;
  if (!fresh || !keyCache.keys.has(kid)) {
    // Unknown key id: Access rotates keys about every six weeks, so fetch again.
    const res = await fetcher(team + '/cdn-cgi/access/certs');
    if (!res.ok) throw new ApiError(503, 'access_keys_unavailable');
    const { keys = [] } = await res.json();
    const map = new Map();
    for (const jwk of keys) {
      if (jwk.kty !== 'RSA' || !jwk.kid) continue;
      map.set(jwk.kid, await crypto.subtle.importKey('jwk', jwk, { name: 'RSASSA-PKCS1-v1_5', hash: 'SHA-256' }, false, ['verify']));
    }
    keyCache = { team, at: Date.now(), keys: map };
  }
  return keyCache.keys.get(kid) ?? null;
}

/** Verifies an Access token; returns its payload or throws ApiError(401). */
export async function verifyAccessToken(token, { team, aud, now = Date.now() / 1000, fetcher = fetch }) {
  const parts = typeof token === 'string' ? token.split('.') : [];
  if (parts.length !== 3) throw new ApiError(401, 'unauthenticated');
  let header, payload;
  try { header = b64urlJson(parts[0]); payload = b64urlJson(parts[1]); } catch { throw new ApiError(401, 'unauthenticated'); }
  if (header.alg !== 'RS256' || !header.kid) throw new ApiError(401, 'unauthenticated');
  const key = await publicKey(team, header.kid, fetcher);
  if (!key) throw new ApiError(401, 'unauthenticated');
  const ok = await crypto.subtle.verify('RSASSA-PKCS1-v1_5', key, b64urlBytes(parts[2]),
    new TextEncoder().encode(parts[0] + '.' + parts[1]));
  if (!ok) throw new ApiError(401, 'unauthenticated');
  const auds = Array.isArray(payload.aud) ? payload.aud : [payload.aud];
  if (payload.iss !== team || !auds.includes(aud)) throw new ApiError(401, 'unauthenticated');
  if (typeof payload.exp !== 'number' || payload.exp < now - 30) throw new ApiError(401, 'unauthenticated');
  if (typeof payload.nbf === 'number' && payload.nbf > now + 30) throw new ApiError(401, 'unauthenticated');
  return payload;
}

const owners = env => String(env.OWNER_EMAILS ?? '').split(',').map(s => s.trim().toLowerCase()).filter(Boolean);

/** Returns the signed-in owner's e-mail, or throws ApiError 401 / 403 / 503. */
export async function requireOwner(request, env) {
  const url = new URL(request.url);
  const local = url.hostname === 'localhost' || url.hostname === '127.0.0.1';
  if (env.DEV_OWNER_EMAIL && local) return String(env.DEV_OWNER_EMAIL).toLowerCase();

  const team = String(env.ACCESS_TEAM_DOMAIN ?? '').replace(/\/+$/, '');
  const aud = String(env.ACCESS_AUD ?? '');
  const allowed = owners(env);
  if (!/^https:\/\/[a-z0-9-]+\.cloudflareaccess\.com$/.test(team) || !aud || !allowed.length) {
    throw new ApiError(503, 'not_configured');
  }
  const payload = await verifyAccessToken(request.headers.get('Cf-Access-Jwt-Assertion'), { team, aud });
  const email = String(payload.email ?? '').toLowerCase();
  if (!email || !allowed.includes(email)) throw new ApiError(403, 'no_access', { email });
  return email;
}

/** Returns the Client ID of the Gmail script's service token, or throws ApiError 401 / 403 / 503. */
export async function requireService(request, env) {
  const url = new URL(request.url);
  const local = url.hostname === 'localhost' || url.hostname === '127.0.0.1';
  if (env.DEV_SERVICE_ID && local && request.headers.get('X-Dev-Service') === env.DEV_SERVICE_ID) return String(env.DEV_SERVICE_ID);

  const team = String(env.ACCESS_TEAM_DOMAIN ?? '').replace(/\/+$/, '');
  const aud = String(env.ACCESS_AUD ?? '');
  const id = String(env.INGEST_CLIENT_ID ?? '').trim();
  if (!/^https:\/\/[a-z0-9-]+\.cloudflareaccess\.com$/.test(team) || !aud || !/^[0-9a-f]{32}\.access$/.test(id)) {
    throw new ApiError(503, 'not_configured');
  }
  const payload = await verifyAccessToken(request.headers.get('Cf-Access-Jwt-Assertion'), { team, aud });
  if (payload.email || payload.common_name !== id) throw new ApiError(403, 'no_access');
  return id;
}
