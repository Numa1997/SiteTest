"""L3: the blade-mode numbers that chapter 6.2 quotes for its shaking model (first edgewise mode of the NREL 5-MW blade, from
nrel5mw.py: modal mass, frequency, and the mode shape and slope at the pivot at 90 % of the rotor radius).
Run: python3 -I L3_shake_model.py   (writes L3_shake_model.json)"""
import json, math, os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import nrel5mw as T5
tab = T5.blade_table(); Lb = T5.R_TIP - T5.R_HUB; x = tab[:, 0]; mu = tab[:, 2]*T5.ADJ_BL_MS
ph = T5.edge_shape(x); m_e = float(np.trapezoid(mu*ph**2, x*Lb))
xs = (0.9*T5.R_TIP - T5.R_HUB)/Lb
dshape = lambda xx: sum(cc*(k + 2)*xx**(k + 1) for k, cc in enumerate(T5.EDGE_SHAPE))
out = dict(m_e=m_e, f_e=T5.F_EDGE_SYS, Phi_p=float(T5.edge_shape(xs)), dPhi_p=float(dshape(xs)/Lb), r_p=0.9*T5.R_TIP)
print(out)
json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'L3_shake_model.json'), 'w'), indent=1)
