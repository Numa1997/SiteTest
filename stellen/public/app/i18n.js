// Every word the page shows, in German (the default) and in English.
// Both columns are written as originals, not machine translations: the German
// uses the terms of German job ads and of the Agentur für Arbeit
// (Stellenrecherche, Bewerbung, Eingangsbestätigung, Absage), the English
// those of British job ads. Data (job titles, notes, rules) carries its own
// language; this file holds only the interface.
//
// t('key') returns the text in the current language; t('key', { n: 3 })
// fills {n}. A key missing in one language falls back to the other, so a
// forgotten line shows English or German, never a raw key.

const TEXT = {
  de: {
    'app.title': 'Stellenrecherche',
    'app.doc_title': 'Stellenrecherche · Numa Koudsie',
    'app.kicker': 'Stellenrecherche · nicht öffentlich',
    'boot.loading': 'Wird geladen …',
    'boot.slow': 'Nach 20 Sekunden noch nicht geladen. Bitte die Verbindung prüfen oder die Seite neu laden.',

    'util.group': 'Alle Abschnitte öffnen oder schließen',
    'util.expand_all': 'Alle öffnen',
    'util.collapse_all': 'Alle schließen',
    'util.sign_out': 'Abmelden',
    'util.absagen': 'Absagen',
    'util.lang_switch': 'English',
    'util.lang_title': 'Sprache: Deutsch. Klicken für Englisch.',
    'theme.auto': 'Automatisch',
    'theme.light': 'Hell',
    'theme.dark': 'Dunkel',
    'theme.auto_title': 'Das Farbschema folgt dem System. Klicken für hell.',
    'theme.light_title': 'Helles Farbschema. Klicken für dunkel.',
    'theme.dark_title': 'Dunkles Farbschema. Klicken, um dem System zu folgen.',

    'board.group': 'Suchgebiet',
    'head.open_de': 'Offene Stellen',
    'head.open_eu': 'Offen in Europa',
    'tally.open': 'Offen',
    'tally.applied': 'Beworben',
    'tally.not_relevant': 'Nicht passend',

    'filter.button': 'Filter',
    'filter.none': 'Alles wird angezeigt',
    'filter.area': 'Region',
    'filter.all_areas': 'Alle Regionen',
    'filter.category': 'Bereich · einen wählen, um nur diesen zu zeigen',
    'filter.all_categories': 'Alle Bereiche',
    'filter.clear_area': 'Wieder alle Regionen zeigen',
    'filter.clear_category': 'Wieder alle Bereiche zeigen',

    'sec.expand': '{name} aufklappen',
    'sec.collapse': '{name} zuklappen',
    'sec.open_count': '{n} offen',
    'sec.add': '+ Stelle hinzufügen',
    'area.empty': 'Hier ist noch nichts offen.',

    'card.added_by_you': 'selbst hinzugefügt',
    'card.number': 'Nr. {n}',
    'card.in_short': 'Kurz',
    'card.salary': 'Gehalt',
    'card.contract': 'Vertrag',
    'card.added': 'Aufgenommen',
    'card.open': 'Zur Anzeige ↗',
    'card.more': 'Mehr',
    'card.less': 'Weniger',
    'card.show_details': 'Details zeigen',
    'card.hide_details': 'Details ausblenden',
    'card.remove': 'Entfernen',
    'card.remove_because': 'Entfernen, weil …',
    'card.remove_group': 'Warum diese Stelle entfernen?',
    'card.applied': 'Beworben',
    'card.not_relevant': 'Nicht passend',
    'card.cancel': 'Abbrechen',
    'card.mistake': 'Versehentlich hinzugefügt: löschen, ohne zu zählen',
    'card.confirm_delete': '„{title}“ löschen? Die Stelle wird nirgends gezählt.',
    'card.note_lang': 'Anmerkung (nur auf Englisch vorhanden)',

    'employment.EMPLOYEE': 'Festanstellung',
    'employment.CONTRACT': 'Befristeter Vertrag',
    'employment.TRAINEE': 'Traineeprogramm',
    'employment.TEMPORARY': 'Befristet',

    'form.title': 'Stelle hinzufügen: {category}',
    'form.link': 'Link zur Anzeige',
    'form.job_title': 'Stellentitel, wie ausgeschrieben',
    'form.company': 'Unternehmen (freiwillig)',
    'form.city': 'Ort',
    'form.area': 'Region',
    'form.save': 'Stelle hinzufügen',
    'form.saving': 'Wird gespeichert …',
    'form.cancel': 'Abbrechen',
    'form.err_link': 'Bitte den vollständigen Link einfügen, beginnend mit https://',
    'form.err_title': 'Bitte den Stellentitel so eingeben, wie er ausgeschrieben ist.',
    'form.err_city': 'Bitte den Ort eingeben.',
    'form.err_area': 'Bitte die Region wählen.',
    'form.err_duplicate': 'Dieser Link steht schon auf der Liste.',

    'stage.applied': 'Beworben',
    'stage.rejected': 'Absage',
    'stage.confirmed': 'Eingangsbestätigung erhalten · Entscheidung offen',
    'stage.interview': 'Vorstellungsgespräch',
    'stage.offer': 'Angebot',
    'stage.withdrawn': 'Zurückgezogen',
    'stage.portal_invitation': 'Einladung ins Bewerberportal · Bewerbung nicht bestätigt',
    'stage.unclear': 'Unklar · nichts geändert',

    'record.title': 'Bewerbungsnachweis',
    'record.label': 'Bewerbungsnachweis',
    'record.counts': '{applied} beworben · {notrel} nicht passend',
    'record.applied': 'Beworben',
    'record.not_relevant': 'Nicht passend',
    'record.empty': 'Noch nichts.',
    'record.undo': 'Rückgängig',
    'record.undo_title': 'Diese Stelle wieder auf die Liste setzen',
    'record.earlier_posting': 'Stelle Nr. {n} (frühere Liste)',
    'record.earlier_record': 'Früherer Eintrag {key}',

    'log.title': 'Bewerbungs-E-Mails',
    'log.label': 'Bewerbungs-E-Mails',
    'log.counts': '{n} Einträge',
    'log.counts_dated': '{n} Einträge · Stand {date}',
    'log.intro': 'Zusammengestellt aus den E-Mails, die auf Bewerbungen geantwortet haben. Enthalten sind auch Bewerbungen auf Stellen, die nie auf dieser Liste standen. Unklare Einträge ändern weder Karten noch gespeicherte Vermerke.',
    'log.untitled': 'Stelle nicht genannt',
    'log.off_list': 'Nicht auf der Liste',

    'footer.updated': 'Liste aktualisiert am {date}',

    'fatal.title': 'Die Liste konnte nicht geladen werden',
    'fatal.text': 'Der Dienst hat nicht geantwortet. Gespeicherte Einträge bleiben erhalten.',
    'fatal.retry': 'Erneut versuchen',
    'session.title': 'Sitzung abgelaufen',
    'session.text': 'Die Anmeldung ist abgelaufen. Nach dem Neuladen meldet die Seite neu an; nichts geht verloren.',
    'session.reload': 'Neu laden',
    'noaccess.title': 'Kein Zugang',
    'noaccess.text': '{email} hat keinen Zugang zu dieser Liste. Bitte abmelden und mit dem berechtigten Konto anmelden.',
    'noaccess.someone': 'Dieses Konto',
    'setup.title': 'Anmeldung noch nicht eingerichtet',
    'setup.text': 'Der Server lässt niemanden herein, solange die Anmeldung (Cloudflare Access) nicht eingerichtet ist. Es ist nichts kaputt; die Daten sind sicher.',

    'err.save': 'Speichern fehlgeschlagen. Es wurde nichts geändert. Bitte die Verbindung prüfen und es noch einmal versuchen.',
    'err.save_form': 'Speichern fehlgeschlagen. Bitte die Verbindung prüfen und es noch einmal versuchen.',
    'err.delete': 'Löschen fehlgeschlagen. Bitte noch einmal versuchen.',
    'err.invalid_posting.url': 'Der Link muss eine vollständige Webadresse sein, beginnend mit https://',
    'err.invalid_posting.title': 'Bitte den Stellentitel eingeben (höchstens 300 Zeichen).',
    'err.invalid_posting.company': 'Der Name des Unternehmens ist zu lang.',
    'err.invalid_posting.city': 'Bitte den Ort eingeben (höchstens 120 Zeichen).',
    'err.invalid_posting.area': 'Bitte die Region wählen.',
    'err.invalid_posting.category': 'Unbekannter Bereich.',
    'err.capacity': 'Die Liste ist voll. Bitte erst alte Einträge entfernen.',
    'err.forbidden_origin': 'Anfrage von einer fremden Seite abgelehnt.',
  },

  en: {
    'app.title': 'Job search',
    'app.doc_title': 'Job search · Numa Koudsie',
    'app.kicker': 'Job search · private',
    'boot.loading': 'Loading…',
    'boot.slow': 'Still loading after 20 seconds. Check the connection or reload the page.',

    'util.group': 'Open or close all sections',
    'util.expand_all': 'Expand all',
    'util.collapse_all': 'Collapse all',
    'util.sign_out': 'Sign out',
    'util.absagen': 'Rejections',
    'util.lang_switch': 'Deutsch',
    'util.lang_title': 'Language: English. Click for German.',
    'theme.auto': 'Auto',
    'theme.light': 'Light',
    'theme.dark': 'Dark',
    'theme.auto_title': 'Theme follows your system. Click for light.',
    'theme.light_title': 'Light theme. Click for dark.',
    'theme.dark_title': 'Dark theme. Click to follow your system.',

    'board.group': 'Search area',
    'head.open_de': 'Open postings',
    'head.open_eu': 'Open in Europe',
    'tally.open': 'Open',
    'tally.applied': 'Applied',
    'tally.not_relevant': 'Not relevant',

    'filter.button': 'Filter',
    'filter.none': 'Showing everything',
    'filter.area': 'Area',
    'filter.all_areas': 'All areas',
    'filter.category': 'Category · pick one to show only that',
    'filter.all_categories': 'All categories',
    'filter.clear_area': 'Show all areas',
    'filter.clear_category': 'Show all categories',

    'sec.expand': 'Expand {name}',
    'sec.collapse': 'Collapse {name}',
    'sec.open_count': '{n} open',
    'sec.add': '+ Add posting',
    'area.empty': 'Nothing open here yet.',

    'card.added_by_you': 'added by you',
    'card.number': '#{n}',
    'card.in_short': 'In short',
    'card.salary': 'Salary',
    'card.contract': 'Contract',
    'card.added': 'Added',
    'card.open': 'Open posting ↗',
    'card.more': 'More',
    'card.less': 'Less',
    'card.show_details': 'Show details',
    'card.hide_details': 'Hide details',
    'card.remove': 'Remove',
    'card.remove_because': 'Remove because…',
    'card.remove_group': 'Why remove this posting?',
    'card.applied': 'Applied',
    'card.not_relevant': 'Not relevant',
    'card.cancel': 'Cancel',
    'card.mistake': 'Added by mistake: delete without counting',
    'card.confirm_delete': 'Delete "{title}"? It will not be counted anywhere.',
    'card.note_lang': 'Note',

    'employment.EMPLOYEE': 'Permanent',
    'employment.CONTRACT': 'Fixed-term contract',
    'employment.TRAINEE': 'Graduate programme',
    'employment.TEMPORARY': 'Temporary',

    'form.title': 'Add a posting to {category}',
    'form.link': 'Link',
    'form.job_title': 'Job title, as advertised',
    'form.company': 'Company (optional)',
    'form.city': 'City',
    'form.area': 'Area',
    'form.save': 'Add posting',
    'form.saving': 'Saving…',
    'form.cancel': 'Cancel',
    'form.err_link': 'Paste the full link, starting with https://',
    'form.err_title': 'Enter the job title as it is advertised.',
    'form.err_city': 'Enter the city.',
    'form.err_area': 'Choose the area.',
    'form.err_duplicate': 'This link is already on the list.',

    'stage.applied': 'Applied',
    'stage.rejected': 'Rejected',
    'stage.confirmed': 'Confirmation received · pending',
    'stage.interview': 'Interview',
    'stage.offer': 'Offer',
    'stage.withdrawn': 'Withdrawn',
    'stage.portal_invitation': 'Portal invitation · application not confirmed',
    'stage.unclear': 'Unclear · left unchanged',

    'record.title': 'Application record',
    'record.label': 'application record',
    'record.counts': '{applied} applied · {notrel} not relevant',
    'record.applied': 'Applied',
    'record.not_relevant': 'Not relevant',
    'record.empty': 'Nothing yet.',
    'record.undo': 'Undo',
    'record.undo_title': 'Put this posting back on the list',
    'record.earlier_posting': 'Posting #{n} (earlier list)',
    'record.earlier_record': 'Earlier record {key}',

    'log.title': 'Application e-mails',
    'log.label': 'application e-mails',
    'log.counts': '{n} entries',
    'log.counts_dated': '{n} entries · updated {date}',
    'log.intro': 'Compiled from the e-mails that answered applications. It also includes applications to postings that were never on this list. Unclear entries change neither cards nor saved marks.',
    'log.untitled': 'Job not named',
    'log.off_list': 'Not on the list',

    'footer.updated': 'List updated {date}',

    'fatal.title': 'Could not load the list',
    'fatal.text': 'The service did not answer. Your saved records are preserved.',
    'fatal.retry': 'Try again',
    'session.title': 'Session expired',
    'session.text': 'The sign-in has expired. Reloading signs you in again; nothing is lost.',
    'session.reload': 'Reload',
    'noaccess.title': 'No access',
    'noaccess.text': '{email} has no access to this list. Sign out, then sign in with the account it belongs to.',
    'noaccess.someone': 'This account',
    'setup.title': 'Sign-in not set up yet',
    'setup.text': 'The server lets nobody in until sign-in (Cloudflare Access) is set up. Nothing is broken; the data is safe.',

    'err.save': 'Could not save. Nothing was changed. Check the connection and try again.',
    'err.save_form': 'Could not save. Check the connection and try again.',
    'err.delete': 'Could not delete. Try again.',
    'err.invalid_posting.url': 'The link must be a full web address starting with https://',
    'err.invalid_posting.title': 'Enter the job title (up to 300 characters).',
    'err.invalid_posting.company': 'The company name is too long.',
    'err.invalid_posting.city': 'Enter the city (up to 120 characters).',
    'err.invalid_posting.area': 'Choose the area.',
    'err.invalid_posting.category': 'Unknown category.',
    'err.capacity': 'The list is full. Remove old entries first.',
    'err.forbidden_origin': 'Request from another site refused.',
  },
};

export const LANGS = ['de', 'en'];
const KEY = 'stellen.lang';

let lang = (() => {
  try { const v = localStorage.getItem(KEY); return LANGS.includes(v) ? v : 'de'; } catch { return 'de'; }
})();

export const getLang = () => lang;

export function setLang(next) {
  if (!LANGS.includes(next)) return;
  lang = next;
  try { localStorage.setItem(KEY, next); } catch { /* private mode */ }
  applyDocument();
}

/** Sets <html lang> and the tab title to the current language. */
export function applyDocument() {
  document.documentElement.lang = lang;
  document.title = t('app.doc_title');
}

export function t(key, vars) {
  const other = lang === 'de' ? 'en' : 'de';
  const text = TEXT[lang][key] ?? TEXT[other][key] ?? key;
  return vars ? text.replace(/\{(\w+)\}/g, (m, k) => (k in vars ? String(vars[k]) : m)) : text;
}

/** 2026-10-07 → "7. Okt. 2026" (de) or "7 Oct 2026" (en). */
export function dateLabel(iso) {
  const ms = Date.parse(iso);
  if (!Number.isFinite(ms)) return '';
  return new Date(ms).toLocaleDateString(lang === 'de' ? 'de-DE' : 'en-GB',
    { day: 'numeric', month: 'short', year: 'numeric', timeZone: 'Europe/Berlin' });
}

/** A label from the server's catalogue entry { en, de }. */
export const label = entry => (entry ? entry[lang] ?? entry.en ?? entry.key : '');
