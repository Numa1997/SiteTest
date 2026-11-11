# Lucretius, *De rerum natura* I 146–224: the text kept for the site

Numa, 5 November 2026: the opening passage (lines 146–158, the terror of the mind dispelled not by daylight but by nature's law;
nothing comes from nothing by divine power; things happen without the gods) stands on the home page; the rest of the passage is to
be scattered over other pages later. A standalone page that carried all of it was published and removed again the same day at
Numa's word. On 10 November 2026 Numa asked for one again: `public/lucretius.html` (lines 146–224 in Latin, English, German and Arabic),
linked from the home band.

| File | What it is |
|---|---|
| `poem-146-224.json` | The passage in 20 Latin sentences: line numbers, Latin, Leonard's English, Diels' German, per sentence. |
| `extract.py` | Cuts the passage out of the downloaded sources by first and last words, so nothing is retyped (paths point at the scratch folder where the sources were downloaded; download them again to rerun). |
| `poem-ar-146-158.json`, `poem-ar-159-224.json` | The Arabic, per sentence, made from the Latin for this site (not published, not reviewed by a second reader). |
| `make_page.py` | Writes `public/lucretius.html`, the whole passage in four languages (10 November 2026). |
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

**How the Arabic is written** (fourth version, 11 November 2026). Numa rejected three versions, and the reasons are the rule for any
later change. (1) Word for word («لا يُولَد شيءٌ من العدم بفعل الآلهة أبدًا»): "no one says that in standard Arabic". (2) Classical
ornament («تجلوها», «نواميسها», «أنّى», «لا مناص», «الجبال الشُّمّ», case vowels on every noun): "Quran Arabic, too old, a Gulf or
Bedouin voice". (3) Plain modern («العتمة», short flat sentences): "fragile and weak"; darkness is «ظلام». What he wants is the voice
of Levantine literary prose, strong and with a melody, between (2) and (3). The model is the prose of the Levantine Nahda and Mahjar and
its translations of philosophical poetry: sentences that open on «إن», «لكنّ», «ومن هنا», clauses chained with و and ف, balanced pairs
and repetition («هذا الرعب… وهذا الظلام…», «يرون… ولا يرون…», «كل ما يجري»), strong plain verbs («يسكن», «يخيّم», «يقبض», «تنبثق»,
«تروّض», «تُسلم»), questions answered by «أليس لأن…», living images kept («شواطئ النور», «سهام النهار», «يد الآلهة»). Vowel marks only
where a word could be misread (the passive: «يُخلق», «حُرمت»), plus shadda and tanwin, as modern Levantine books print. *nihilum* is
«العدم» (Numa). Set in Noto Naskh Arabic, the site's Arabic text face, not Amiri. Read for the voice on 11 November 2026: Felix Fares'
translation of Nietzsche's Zarathustra as serialised in الرسالة, 1937
([Wikisource](https://ar.wikisource.org/wiki/مجلة_الرسالة/العدد_211/هكذا_قال_زرادشت)), Gibran's prose
([Hindawi](https://www.hindawi.org/books/59729251/24/)), and the Arabic quotations of the atomists in
[نشأة العالم في المذهب الذري](https://altanweeri.net/8838/). The sentences are this site's own.
