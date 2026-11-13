# Lucretius, *De rerum natura* I 146–224: the text kept for the site

Numa, 5 November 2026: the opening passage (lines 146–158, the terror of the mind dispelled not by daylight but by nature's law;
nothing comes from nothing by divine power; things happen without the gods) stands on the home page; the rest of the passage is to
be scattered over other pages later. A standalone page that carried all of it was published and removed again the same day at
Numa's word. On 10 November 2026 Numa asked for one again: `public/lucretius.html`, linked from the home band; since 11 November 2026 one language per
page (English, with `/de/` and `/ar/` made by the site's generator), only the poem, no Latin. On 13 November 2026 Numa reversed that:
all four languages (Latin, English, German, Arabic) side by side in four columns, separated beautifully and subtly; the phone was left to
me (one language at a time, chosen with four buttons; tablets show two by two).

| File | What it is |
|---|---|
| `poem-146-224.json` | The passage in 20 Latin sentences: line numbers, Latin, Leonard's English, Diels' German, per sentence. |
| `extract.py` | Cuts the passage out of the downloaded sources by first and last words, so nothing is retyped (paths point at the scratch folder where the sources were downloaded; download them again to rerun). |
| `poem-ar-146-224.json` | The Arabic (seventh version, 13 November 2026), 20 groups of lines, one per sentence of the Latin (`lines` = first and last Latin line); free verse in modern literary Arabic, with rhyme only here and there, made from Leonard's English for this site (not published, not reviewed by a second reader). The first four groups are the home band. |
| `make_page.py` | Writes `public/lucretius.html`: 20 verses in four columns (Latin with its line numbers, Leonard, Diels, the Arabic). The verses stand in the page itself, marked `translate="no"` with their own `lang`, so the i18n tables hold only the words around them (rebuilt 13 November 2026). |
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
(المركز القومي للترجمة, Cairo 2018) is under copyright and was not used; the Arabic on the site (`poem-ar-146-224.json`, 13 November
2026) is a translation made from Leonard's English for this site, read against Leonard and Diels, not reviewed by a second reader, and labelled so on the cards.

**What Numa first had** (from Gemini): lines 149 and 218 misquoted, an English text attributed to Leonard that is not his, lines
192–214 missing.

**Which Arabic is on the site, and why.** The Arabic on the site is the **seventh version** (13 November 2026). Numa's rule for it: it
must say what the English says. So it follows Leonard's English verse by verse, in lines, not word for word, in strong modern literary
Arabic. Five versions came before it, and the reasons they were rejected are the rules for any later change:

1. First (10 Nov, bea5607 and 9120b8d): close to the Latin, case vowels everywhere. Numa called it "Gulf and Peninsula Arabic" and,
   after the three that followed, "the least bad". It was restored for a few hours on 11 November (78c4e89) and is in git.
2. Second (10 Nov, 868d8f6): corrected after the review; used «لا شيء» for *nihilum*. Rejected: «العدم» is the word (Numa).
3. Third (11 Nov, 8ebf821): sentence by sentence, with archaic ornament («تجلوها», «نواميسها», «أنّى»). Rejected as Quranic Arabic.
4. Fourth (11 Nov, c1e93c5): modern Levantine literary prose, almost no vowels. Rejected as thin, "fragile and weak", "a second grader
   from Damascus".
5. Fifth (11 Nov, b8e45ea): made from the Latin in a "majestic" register, with clauses added for balance («حين نتأمّله… حين نفقهه»).
   Rejected within minutes: next to Leonard's English it "is not what the English is saying".
6. Sixth (11 Nov, the page now): from Leonard's English, verse by verse and in lines, nothing added and nothing left out. Where Leonard
   leaves the Latin, the Arabic goes with Leonard: line 150 has no "by divine power" (*divinitus*), line 159 reads "from all things"
   where the Latin has "from nothing". Replaced two days later, on Numa's complaint that the Arabic was "some texts neatly put on top of
   one another" and not poetry.
7. Seventh (13 Nov, the page now): the sixth version's content (still Leonard's English, still «العدم» and «ظلام») rewritten as free verse
   with melody: balanced half-lines and parallel clauses, no classical metre. End rhyme is rare: a mechanical check of the last two letters
   finds it in only four of the 20 groups (159–160, 174–179, 192–198, 199–204). So it is better called rhythmic free verse than rhymed
   poetry, and the page says "rhyme only here and there". No second reader has checked it. Whether it is poetry enough is for Numa to
   judge; the layout does part of the work (the Arabic stands in its own column, its couplets spaced). Its verdict is not yet known.

Rules that hold for every version: the Arabic says what the English says, no more and no less; *nihilum* is «العدم»; darkness is «ظلام» (never «عتمة»); no calques («لا يُولَد شيءٌ من العدم بفعل
الآلهة أبدًا» was rejected as word for word); no archaic particles; no Quranic ornament.

**What the first version got wrong** (corrected in 868d8f6; the sixth version follows Leonard there). The review of 10 November (Opus) found, among others, *erumpere* (line 162) rendered «تنفلق», *secreta facultas* (line 173) rendered «قدرةً
خاصّةً مستترة», and *alienis partibus anni* (line 181) rendered «من أجزاءِ السنة التي لا تناسبها». The seventh version has no second reader. The page
note (`i18n/ar/lucretius.html.json`, key d11ce3c93aa4) says so in the reader's words.

**Sources read for the Arabic voice** (11 November 2026): Felix Fares' translation of Nietzsche's Zarathustra as serialised in الرسالة,
1937 ([Wikisource](https://ar.wikisource.org/wiki/مجلة_الرسالة/العدد_211/هكذا_قال_زرادشت)), Gibran's prose
([Hindawi](https://www.hindawi.org/books/59729251/24/)), and the Arabic quotations of the atomists in
[نشأة العالم في المذهب الذري](https://altanweeri.net/8838/). The Arabic column is set in Noto Naskh Arabic, the site's Arabic text face.
The Cairo 2018 translation (المركز القومي للترجمة) was not read and is not to be copied onto the site; a short credited quotation would
fall under the right of quotation (§ 51 UrhG), a whole column would need the publisher's licence.
