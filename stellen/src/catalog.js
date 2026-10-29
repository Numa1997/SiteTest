// The eleven categories, the two search areas (boards) and their regions,
// in English and German. The server validates against these and sends them
// to the page with the list, so a card can only ever sit in one of them.
// Each region belongs to one board; both boards show the same categories.
// Order matters: it is the order on the page.

export const CATEGORIES = [
  { key: 'content', en: 'Content creation (not school teaching)', de: 'Content-Erstellung (kein Schulunterricht)' },
  { key: 'ai', en: 'AI training on physics & maths', de: 'KI-Training in Physik und Mathematik' },
  { key: 'data', en: 'Data analyst', de: 'Datenanalyse' },
  { key: 'computational', en: 'Computational scientist', de: 'Wissenschaftliches Rechnen' },
  { key: 'numerical', en: 'Numerical methods', de: 'Numerische Methoden' },
  { key: 'systems', en: 'Systems engineer', de: 'Systemingenieurwesen' },
  { key: 'physiker', en: '“Physiker” in the job title', de: '„Physiker“ im Stellentitel' },
  { key: 'pm', en: 'Project management', de: 'Projektmanagement' },
  { key: 'production', en: 'Production supervisor', de: 'Produktionsleitung' },
  { key: 'energy', en: 'Energy sector', de: 'Energiebranche' },
  { key: 'testing', en: 'Device testing & measurement (test, calibrate, qualify, build test rigs)',
    de: 'Prüf- und Messtechnik (prüfen, kalibrieren, qualifizieren, Prüfstände bauen)' },
];

export const BOARDS = [
  { key: 'de', en: 'Germany', de: 'Deutschland' },
  { key: 'eu', en: 'Europe', de: 'Europa' },
];

export const AREAS = [
  { key: 'berlin', board: 'de', en: 'Berlin', de: 'Berlin' },
  { key: 'leipzig', board: 'de', en: 'Leipzig area', de: 'Raum Leipzig' },
  { key: 'de', board: 'de', en: 'Rest of Germany', de: 'Übriges Deutschland' },
  { key: 'benelux', board: 'eu', en: 'Benelux', de: 'Benelux' },
  { key: 'nordics', board: 'eu', en: 'Nordics', de: 'Nordeuropa' },
  { key: 'europe', board: 'eu', en: 'Rest of Europe', de: 'Übriges Europa' },
];

export const CATEGORY_KEYS = CATEGORIES.map(c => c.key);
export const AREA_KEYS = AREAS.map(a => a.key);
