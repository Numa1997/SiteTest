"""The numbers typed by hand in theory/*.src.html, each with its reason.  Read by tools/check_numbers.py.

Every other number in the lecture notes comes from tools/make_numbers.py through a {{n:key}} or {{table:key}} placeholder.
A number typed by hand is allowed only if it is listed here for its file, as one of:
  'input: ...'   a model input or a cited value (source given), or a setting chosen for the study;
  'def: ...'     part of a definition, a name, a date, a catalogue number, a count, or a cross-reference;
  ('calc', expr, rel_tol, why)   a derived or result number: check_numbers.py evaluates expr (Python, with math, json, the
                 data folder D, numbers N from numbers.json and the names in ENV) and requires agreement within rel_tol.
Integers from 0 to 10 without a decimal point are allowed everywhere (counts, small factors, exponents); section and
equation numbers in headings and \\tag{} are skipped.
"""
import json, pathlib
_D = pathlib.Path(__file__).resolve().parents[1] / 'data'
_S = json.load(open(_D / 'setup.json'))
_M = json.load(open(_D / 'L3_shake2.json'))['meta']
ENV = {'S': _S, 'META': _M}

SET = 'input: a setting chosen for these notes (chapter 0)'
NREL = 'input: Jonkman, Butterfield, Musial and Scott 2009, NREL/TP-500-38060 (the NREL 5 MW reference turbine)'
GEN = 'input: maxon catalogue, RE 25 part 339152 and GP 32 C gearhead (chapter 7, sources)'
MC = 'input: setting of the Monte Carlo run of the earlier point and double pendulum study (power_theorem_mc.py, mc_full.log)'
YEAR = 'def: year of a cited source'

TYPED = {
'00': {
    '60': 'def: order of magnitude of a large blade (NREL 5 MW blade 61.5 m), and the illustration "60 m out along a blade"',
    '63': ('calc', "S['R_ROT']", 1e-9, 'rotor radius of the NREL 5 MW turbine'),
    '7.55': ('calc', "S['LAM_STAR']", 1e-9, NREL), '0.482': ('calc', "S['CP_STAR']", 1e-9, NREL),
    '2009': YEAR, '9.80665': 'input: standard gravity (CGPM 1901)',
    '100': 'def: the largest tip vibration tried in chapter 6 (100 mm)',
},
'01': {
    '63': ('calc', "S['R_ROT']/S['L_B']", 1e-9, 'r_p, and r_p over l'),
},
'02': {
    '45': ('calc', 'math.degrees(math.atan(1))', 1e-9, 'lag at kappa = |R-1|'), '90': 'def: right angle',
    '63': ('calc', "S['R_ROT']/S['L_B']", 1e-9, 'r_p, and r_p over l'),
},
'03': {
    '240': 'input: steps per turn of the runs (L1_blade.py)', '60': 'input: turns let pass before measuring (L1_blade.py)',
},
'04': {
    '0.1': MC, '0.2': MC, '0.028': MC, '48': MC, '0.05': MC, '1000': MC, '40': MC,
    '1.0793': ('calc', "META['f_e']", 1e-9, NREL + ', first edgewise blade mode'),
    '1.08': ('calc', "META['f_e']", 0.005, 'the same frequency, rounded'),
    '4.38': 'input: rotor plus drivetrain inertia at the rotor, 4.38e7 kg m^2 (' + NREL + ')',
    '8.98': 'input: the generator torque law of the NREL 5 MW controller, region 2 to 2.5 (' + NREL + ')',
    '1.86': ('calc', '0.16*(0.75*8 + 5.6)', 0.003, 'IEC 61400-1 ed. 3 normal turbulence, class A, at 8 m/s'),
    '61400': 'def: name of the standard IEC 61400-1', '2009': YEAR, '61.5': 'input: blade length (' + NREL + ')',
    '10 000': 'def: unit of the share (parts in 10 000)', '45': 'def: lag at the best brake (section 2.3)',
    '20': 'input: tip vibration tried in chapter 6 (mm)', '100': 'input: tip vibration tried in chapter 6 (mm)',
    '0.5': 'input: blade damping ratio tried in chapter 6 (%)',
},
'05': {
    '0.01': 'def: series of masses', '0.02': 'def: series of masses', '0.05': 'def: series of masses', '0.1': 'def: series of masses',
    '0.2': 'def: series of masses', '0.5': 'def: series of masses; and the swing limit chosen for the sizing (rad)',
    '25': GEN + ' (name and diameter)', '32': GEN + ' (name)', '339152': GEN, '20': GEN + ' (rated power, W)', '24': GEN + ' (winding, V)',
    '1.53': GEN, '20.8': GEN, '460': GEN, '14.7': GEN, '40.2': GEN, '10 900': GEN, '30.4': GEN, '0.7': GEN, '1.5': GEN,
    '80': GEN, '75': GEN, '70': GEN, '60': GEN + ' (gear efficiency per stage count; and 60 in k_e = 60/(2 pi K_n))',
    '8000': GEN, '492': GEN + ' (largest ratio)', '0.12': GEN + ' (terminal inductance over resistance)',
    '0.02076': ('calc', '60/(2*math.pi*460)', 1e-4, 'k_e from the speed constant'),
    '50': 'input: pessimistic gear efficiency of the sensitivity test (L4_sensitivity.py)',
    '100': 'def: the largest tip vibration tried in chapter 6 (100 mm)',
},
}
