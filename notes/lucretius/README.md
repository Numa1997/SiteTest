# Lucretius, *De rerum natura* I 146–224: the text kept for the site

Numa, 5 November 2026: the opening passage (lines 146–158, the terror of the mind dispelled not by daylight but by nature's law;
nothing comes from nothing by divine power; things happen without the gods) stands on the home page; the rest of the passage is to
be scattered over other pages later. A standalone page that carried all of it was published and removed again the same day at
Numa's word.

| File | What it is |
|---|---|
| `poem-146-224.json` | The passage in 20 Latin sentences: line numbers, Latin, Leonard's English, Diels' German, per sentence. |
| `extract.py` | Cuts the passage out of the downloaded sources by first and last words, so nothing is retyped (paths point at the scratch folder where the sources were downloaded; download them again to rerun). |
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
(المركز القومي للترجمة, Cairo 2018) is under copyright; no free one exists, so the Arabic pages show Leonard's English.

**What Numa first had** (from Gemini): lines 149 and 218 misquoted, an English text attributed to Leonard that is not his, lines
192–214 missing.
