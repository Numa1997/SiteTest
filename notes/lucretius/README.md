# Lucretius, *De rerum natura* I 146–224: the text kept for the site

Numa, 5 November 2026: the opening passage (lines 146–158, the terror of the mind dispelled not by daylight but by nature's law;
nothing comes from nothing by divine power; things happen without the gods) stands on the home page; the rest of the passage is to
be scattered over other pages later. A standalone page that carried all of it was published and removed again the same day at
Numa's word. On 10 November 2026 Numa asked for one again: `public/lucretius.html` (lines 146–224 in English, German and Arabic; no Latin column since
11 November 2026, the Latin stands on the home page), linked from the home band.

| File | What it is |
|---|---|
| `poem-146-224.json` | The passage in 20 Latin sentences: line numbers, Latin, Leonard's English, Diels' German, per sentence. |
| `extract.py` | Cuts the passage out of the downloaded sources by first and last words, so nothing is retyped (paths point at the scratch folder where the sources were downloaded; download them again to rerun). |
| `poem-ar-146-158.json`, `poem-ar-159-224.json` | The Arabic, per sentence, made from the Latin for this site (not published, not reviewed by a second reader). |
| `make_page.py` | Writes `public/lucretius.html`, the whole passage as 20 verses in English, German and Arabic (10 November 2026, rebuilt 11 November 2026). |
| `make_home.py` | Writes the home page band (between `<!--LUCRETIUS-->` markers in `index.html`) from the first four sentences of the JSON. |

**Sources.** Latin: [The Latin Library](https://www.thelatinlibrary.com/lucretius/lucretius1.shtml), Book I, in the manuscripts'
order (line 155 after 158), checked at lines 149, 155–158 and 218 against Hermann Diels' edition, vol. 1 (Berlin: Weidmann, 1923;
[scan](https://archive.org/details/dererumnaturalat01lucr)). English: William Ellery Leonard, *Of the Nature of Things: A Metrical
Translation* (1916; [Project Gutenberg 785](https://www.gutenberg.org/ebooks/785)), public domain; 100 lines for these 79, with
208–214 before 205–207. German: Hermann Diels, *Lukrez: Von der Natur* (Berlin: Weidmann, 1924, ed. J. Mewaldt, foreword by Albert
Einstein), line for line, from [textlog.de](https://www.textlog.de/lukrez-natur-dinge.html), compared with the excerpt in
[Falter](https://www.falter.at/heureka/20131015/gedicht); corrected there: "wild" → "wird" (line 156), and the break of line 147
("leuchtende Helle / Scheuchen", the online copy has "leuchtende / Helle Scheuchen"; `make_home.py` applies it); line 173 ("…tut jedes
gesondert die Kraft ruht") is as printed online and unchecked against the print. Arabic: the only published translation found
(المركز القومي للترجمة, Cairo 2018) is under copyright and was not used; the Arabic on the site (`poem-ar-146-158.json`, 10 November
2026) is a translation made from the Latin for this site, read against Leonard and Diels, not reviewed by a second reader, and labelled so on the cards.

**What Numa first had** (from Gemini): lines 149 and 218 misquoted, an English text attributed to Leonard that is not his, lines
192–214 missing.

**Which Arabic is on the site, and why.** The Arabic on the site is the **fifth version** (11 November 2026), written at Numa's word as
majestic modern literary Arabic. Four versions came before it, and the reasons they were rejected are the rules for any later change:

1. First (10 Nov, bea5607 and 9120b8d): close to the Latin, case vowels everywhere. Numa called it "Gulf and Peninsula Arabic" and,
   after the three that followed, "the least bad". It was restored for a few hours on 11 November (78c4e89) and is in git.
2. Second (10 Nov, 868d8f6): corrected after the review; used «لا شيء» for *nihilum*. Rejected: «العدم» is the word (Numa).
3. Third (11 Nov, 8ebf821): sentence by sentence, with archaic ornament («تجلوها», «نواميسها», «أنّى»). Rejected as Quranic Arabic.
4. Fourth (11 Nov, c1e93c5): modern Levantine literary prose, almost no vowels. Rejected as thin, "fragile and weak", "a second grader
   from Damascus".
5. Fifth (11 Nov, the page now): his request, after restoring the first: "more Arabic and more majestically Arabic", not Quranic, "that
   beautiful Arabic that you read and you just feel so smooth while reading it, strong as well". It keeps the first version's weight and
   fidelity, the Levantine strong plain verbs and the chaining with و and ف, and a measured, balanced cadence (paired clauses: «حين
   نتأمّله، وقانونها حين نفقهه», «أصل ما نقيم عليه الحجّة»), with the argumentative stress Numa named in Mahdi Amel («لا بدّ أن», «إنّ…»,
   «ليس… إلا…»); no archaic particles, case vowels unmarked, marks only where a word could be misread. It corrects the three misreadings
   of the first version (lines 162, 173, 181). Its verdict is not yet known.

Rules that hold for every version: *nihilum* is «العدم»; darkness is «ظلام» (never «عتمة»); no calques («لا يُولَد شيءٌ من العدم بفعل
الآلهة أبدًا» was rejected as word for word); no archaic particles; no Quranic ornament.

**What the first version got wrong** (corrected in 868d8f6 and again in the fifth version). The review of 10 November (Opus) found, among others, *erumpere* (line 162) rendered «تنفلق», *secreta facultas* (line 173) rendered «قدرةً
خاصّةً مستترة», and *alienis partibus anni* (line 181) rendered «من أجزاءِ السنة التي لا تناسبها». The fifth version has no second reader. The page
note (`i18n/ar/lucretius.html.json`, key 4f631a71eff5) says so in the reader's words.

**Sources read for the Arabic voice** (11 November 2026): Felix Fares' translation of Nietzsche's Zarathustra as serialised in الرسالة,
1937 ([Wikisource](https://ar.wikisource.org/wiki/مجلة_الرسالة/العدد_211/هكذا_قال_زرادشت)), Gibran's prose
([Hindawi](https://www.hindawi.org/books/59729251/24/)), and the Arabic quotations of the atomists in
[نشأة العالم في المذهب الذري](https://altanweeri.net/8838/). The Arabic column is set in Noto Naskh Arabic, the site's Arabic text face.
The Cairo 2018 translation (المركز القومي للترجمة) was not read and is not to be copied onto the site; a short credited quotation would
fall under the right of quotation (§ 51 UrhG), a whole column would need the publisher's licence.
