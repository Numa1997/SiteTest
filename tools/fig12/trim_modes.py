"""Trim the mode data file: drop the angular Fourier components of a mode's surface shape and field that are below
2e-3 of its dominant component (the sculpted panels mix in the k = m +- 2 components at that level or less: see the note,
section 5), and round the field to 4 digits. python3 tools/fig12/trim_modes.py in.js out.js"""
import sys, json, numpy as np
s = open(sys.argv[1]).read(); head = s[:s.index('window.SLOSH_MODES = ')]; d = json.loads(s[s.index('{'):s.rindex('}') + 1])
n0 = n1 = 0
for F in d['fills']:
    for md in F['modes']:
        dom = str(md['m']); amp = {k: float(np.abs(np.array(md['psi'][k])).max()) for k in md['psi']}
        keep = [k for k in md['psi'] if amp[k] >= 2e-3 * amp[dom]] or [dom]
        n0 += len(md['psi']); n1 += len(keep)
        md['psi'] = {k: md['psi'][k] for k in keep}
        if 'field' in md:
            famp = {k: float(np.abs(np.array(md['field'][k])).max()) for k in md['field']}
            fkeep = [k for k in md['field'] if famp[k] >= 2e-3 * famp[dom]] or [dom]
            md['field'] = {k: np.round(np.array(md['field'][k]), 4).tolist() for k in fkeep}
d['trimmed'] = 'components below 2e-3 of the dominant one dropped (tools/fig12/trim_modes.py)'
out = head + 'window.SLOSH_MODES = ' + json.dumps(d, separators=(',', ':')) + ';\n'
open(sys.argv[2], 'w').write(out); print(f'kept {n1}/{n0} shape components; {len(out)} bytes')
