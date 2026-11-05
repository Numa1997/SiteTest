# Cut the passage Book I 146-224 out of the downloaded sources, sentence by sentence (Latin sentence = one group),
# without retyping: every string below is located in the source files by its first and last words.
import re, html, json, io
D = '/tmp/claude-0/-home-user-SiteTest/9d768e8a-f3c3-577b-b0b8-5569ed1470f1/scratchpad/luc/'

# Latin: The Latin Library, book 1, lines 146-224 (with the manuscripts' order 156-158, 155)
lat = []
for l in io.open(D + 'latin1.html', encoding='latin-1').read().split('\n')[163:242]:
    s = html.unescape(re.sub(r'<[^>]+>', '', l)).replace('\xa0', ' ')
    s = re.sub(r'\s+\d+\s*$', '', s).strip(); lat.append(s)
nums = list(range(146, 155)) + [156, 157, 158, 155] + list(range(159, 225))
assert len(lat) == len(nums) == 79, len(lat)

# Leonard 1916 (Project Gutenberg #785), Book I
leo = io.open(D + 'leonard.txt', encoding='utf-8').read().replace('\r', '')
i0 = leo.index('This terror, then, this darkness of the mind,'); leo = leo[i0:leo.index('Dissolve it down.', i0) + len('Dissolve it down.')]
leo = ' / '.join(x.strip() for x in leo.split('\n') if x.strip())

# Diels 1924 (textlog.de), two chapters, decoded from Latin-1
def diels(f):
    t = io.open(D + f, encoding='latin-1').read(); t = re.sub(r'(?i)<br\s*/?>|</p>', '\n', t); t = html.unescape(re.sub(r'<[^>]+>', '', t)).replace('\xa0', ' ')
    return t
dz = diels('naturforschung.html'); d1 = diels('lehrsatz-nichts.html'); d2 = diels('natur-nichts.html')
def lines(t, a, b):
    i = t.index(a); j = t.index(b, i) + len(b); return [x.strip() for x in t[i:j].split('\n') if x.strip()]
dl = lines(dz, 'Jene Gemütsangst', 'obersten Leitsatz;') + lines(d1, 'Nichts kann je', 'besser gedeihen.') + lines(d2, 'Dazu kommt, daß Mutter Natur', 'die Bindungen lockert.')
die = ' / '.join(dl)

# sentence groups: (first line, last line, Leonard start ... end, Diels start ... end)
G = [((146, 148), ('This terror, then,', "and her law,"), ('Jene Gemütsangst', 'Naturanschauung und Forschung.')),
     ((149, 150), ('Which, teaching us,', 'ever yet was born.'), ('Sie muß füglich', 'göttliche Schöpfung.')),
     ((151, 154), ('Fear holds dominion', 'are working there.'), ('Denn nur darum', 'göttlichen Macht zu.')),
     ((156, 155), ('Meantime, when once', 'no tool of Gods.'), ('Haben wir also', 'Hilfe der Götter.')),
     ((159, 160), ('Suppose all sprang', 'No fixed seed required.'), ('Gäb\' es Entstehung', 'bedürfte des Samens.')),
     ((161, 166), ('Men from the sea', 'By chance and change.'), ('So könnt\' erstlich', 'erzeugte da alles.')),
     ((167, 168), ('Indeed, and were there not', 'unalterable mother old?'), ('Hätte fürwahr', 'Ursprung bestehen?')),
     ((169, 173), ('But, since produced', 'a secret power its own.'), ('Doch weil jegliches', 'die Kraft ruht.')),
     ((174, 179), ('Again, why see we', 'Her tender progenies?'), ('Weshalb sehen wir', 'Lichtes emporführt.')),
     ((180, 183), ('But if from naught', 'at an adverse hour.'), ('Kämen aus Nichts', 'Zeugung könnte verhindern.')),
     ((184, 187), ('Nor on the mingling', 'a branching tree--'), ('Auch für das Wachstum', 'Bäume dem Boden.')),
     ((188, 191), ('Wonders unheard of;', 'From out their proper matter.'), ('Aber dergleichen', 'mehrt jedes und nährt sich.')),
     ((192, 198), ('Thus it comes', 'without its origins.'), ('Hierzu kommt, daß ohne', 'Urelemente beraubt sei.')),
     ((199, 204), ('Moreover, why should Nature', 'Is fixed forevermore?'), ('Schließlich warum', 'wirklich entstehn kann?')),
     ((205, 207), ('Confess then,', 'the gentle fields of air.'), ('Also: Nichts entsteht', 'dünne Gefilde.')),
     ((208, 214), ('Lastly we see', 'Spontaneous generations, fairer forms.'), ('Endlich sehen wir doch', 'besser gedeihen.')),
     ((215, 216), ('Hence too it comes', 'to annihilation.'), ('Dazu kommt, daß Mutter', 'Nichts wird vernichtet.')),
     ((217, 218), ('For, were aught mortal', 'Unto destruction;'), ('Denn wär\' irgendein', 'der Tod trifft.')),
     ((219, 220), ('since no force were needed', 'undo its bands.'), ('Denn dann braucht', 'Verbände zu lösen.')),
     ((221, 224), ('Whereas, of truth,', 'Dissolve it down.'), ('Doch nun ist ja', 'die Bindungen lockert.'))]
def cut(t, a, b):
    i = t.index(a); j = t.index(b, i) + len(b); return t[i:j].strip(' /')
out = []; pos = 0
for (l0, l1), (la, lb), (da, db) in G:
    k0 = nums.index(l0); k1 = nums.index(l1); assert k1 >= k0
    out.append({'lines': nums[k0:k1 + 1], 'la': lat[k0:k1 + 1], 'en': cut(leo, la, lb).split(' / '), 'de': cut(die, da, db).split(' / ')})
assert sum(len(g['la']) for g in out) == 79
# the Diels misprint confirmed by Falter's reprint: "wild geschaffen" -> "wird geschaffen"
for g in out: g['de'] = [x.replace('aus dem Nichts wild geschaffen', 'aus dem Nichts wird geschaffen') for x in g['de']]
json.dump(out, io.open(D + 'poem.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
for g in out: print(g['lines'][0], '-', g['lines'][-1], '|', g['la'][0][:30], '|', g['en'][0][:30], '...', g['en'][-1][-25:], '|', g['de'][0][:25], '...', g['de'][-1][-25:])
