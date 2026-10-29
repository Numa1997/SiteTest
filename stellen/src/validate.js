// What the server accepts from the page. Pure functions, no database, so
// they can be tested with plain Node (test/validate.test.mjs).
// Carried over from the AppDeploy version (backend/marks-store.mjs and
// backend/added-store.mjs); the one-time migrations there (legacy marks,
// the renumbering of 9 October 2026, the e-mail outcomes) were finished on
// AppDeploy and are not repeated here: the export carries their result.
import { CATEGORY_KEYS, AREA_KEYS } from './catalog.js';

export class ApiError extends Error {
  constructor(status, code, extra = {}) { super(code); this.status = status; this.code = code; this.extra = extra; }
}

// 'j<n>' a listed posting, 'c<n>' a company (older marks), 'a<timestamp>' a posting Numa added.
export const validItem = v => typeof v === 'string' && /^(?:[jc]\d{1,10}|a\d{13,16})$/.test(v);
export const validAddedId = v => typeof v === 'string' && /^a\d{13,16}$/.test(v);

export const MARK_FIELDS = ['outcome', 'outcome_at', 'stage', 'stage_at', 'round', 'removed', 'note', 'snapshot'];
const SNAPSHOT_KEYS = ['title', 'company', 'city', 'area', 'category', 'url', 'n'];
const STAGES = ['applied', 'confirmed', 'interview', 'offer', 'rejected', 'withdrawn'];
const OUTCOMES = ['applied', 'not_relevant'];
const own = (o, k) => Object.hasOwn(o, k);
const isDate = v => typeof v === 'string' && v.length <= 40 && Number.isFinite(Date.parse(v));

function validSnapshot(v) {
  if (v === null) return true;
  if (!v || typeof v !== 'object' || Array.isArray(v)) return false;
  return Object.entries(v).every(([k, x]) => SNAPSHOT_KEYS.includes(k) &&
    (x === null || (k === 'n' ? Number.isSafeInteger(x) : typeof x === 'string' && x.length <= (k === 'url' ? 2000 : 300))));
}

/** A change to one mark, as the page sends it. Unknown fields are refused, not ignored. */
export function validPatch(p) {
  return !!p && typeof p === 'object' && !Array.isArray(p) &&
    Object.keys(p).every(k => MARK_FIELDS.includes(k)) &&
    (!own(p, 'outcome') || p.outcome === null || OUTCOMES.includes(p.outcome)) &&
    (!own(p, 'outcome_at') || p.outcome_at === null || isDate(p.outcome_at)) &&
    (!own(p, 'stage') || p.stage === null || STAGES.includes(p.stage)) &&
    (!own(p, 'stage_at') || p.stage_at === null || isDate(p.stage_at)) &&
    (!own(p, 'round') || p.round === null || (Number.isInteger(p.round) && p.round >= 0 && p.round <= 100)) &&
    (!own(p, 'removed') || p.removed === null || typeof p.removed === 'boolean') &&
    (!own(p, 'note') || p.note === null || (typeof p.note === 'string' && p.note.length <= 5000)) &&
    (!own(p, 'snapshot') || validSnapshot(p.snapshot));
}

const text = (value, max, required) => {
  if (value === undefined || value === null) value = '';
  if (typeof value !== 'string') return null;
  value = value.trim().replace(/\s+/g, ' ');
  if (required && !value) return null;
  return value.length <= max ? value : null;
};

/** A posting Numa adds by hand. Throws ApiError(400, 'invalid_posting', { field }) naming the first bad field. */
export function cleanPosting(input) {
  const bad = field => new ApiError(400, 'invalid_posting', { field });
  if (!input || typeof input !== 'object' || Array.isArray(input)) throw bad('url');
  const url = text(input.url, 2000, true);
  let parsed = null;
  try { parsed = url && new URL(url); } catch { parsed = null; }
  if (!parsed || !['https:', 'http:'].includes(parsed.protocol) || parsed.username || parsed.password) throw bad('url');
  const posting = {
    url: parsed.href,
    title: text(input.title, 300, true),
    company: text(input.company, 200, false),
    city: text(input.city, 120, true),
    area: input.area,
    category: input.category,
  };
  if (posting.title === null) throw bad('title');
  if (posting.company === null) throw bad('company');
  if (posting.city === null) throw bad('city');
  if (!AREA_KEYS.includes(posting.area)) throw bad('area');
  if (!CATEGORY_KEYS.includes(posting.category)) throw bad('category');
  return posting;
}
