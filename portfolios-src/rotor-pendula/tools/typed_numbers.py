"""The numbers typed by hand in theory/*.src.html, each with its reason.  Read by tools/check_numbers.py.

Every other number in the lecture note comes from tools/make_numbers.py through a {{n:key}} or {{table:key}} placeholder.
A number typed by hand is allowed only if it is listed here for its file, as one of:
  'input: ...'   a model input or a cited value (source given), or a setting chosen for the study;
  'def: ...'     part of a definition, a name, a date, a catalogue number, a count, or a cross-reference;
  ('calc', expr, rel_tol, why)   a derived or result number: check_numbers.py evaluates expr (Python, with math, json, the
                 data folder D and numbers N from numbers.json) and requires agreement within rel_tol.
Integers from 0 to 10 without a decimal point are allowed everywhere (counts, small factors, exponents); section and
equation numbers in headings and \\tag{} are skipped.
"""
SOL = 'input: the study\'s chosen mountings, pendulum and settings'
GEN = 'input: maxon catalogue, RE 25 page 153 / GP 32 C pages 430-431 (dossier-generator.md)'
NREL = 'input: Jonkman et al. 2009, NREL/TP-500-38060, and the OpenFAST r-test blade file (dossier-turbine.md)'
r = lambda rpm: 56.0/(rpm*2*3.141592653589793/60)          # rotor radius at tip-speed ratio 7, 8 m/s

TYPED = {
'00': {
    '60': 'input: blade length of large turbines, order of magnitude (NREL 5 MW blade 61.5 m)', '50': 'def: illustration, 50 m out along a blade',
    '100': SOL, '20': SOL, '100 000': 'def: unit of the share (parts in 100 000)', '14': SOL, 
    '18': SOL, '36': 'def: count, 18 mountings x 2 pendula', '400': SOL, '200': SOL, '30': SOL, '90': SOL,
    '1.3': ('calc', 'r(400)', 0.03, 'smallest rotor radius'), '5.3': ('calc', 'r(100)', 0.03, ''),
    '27': ('calc', 'r(20)', 0.03, ''), '67': ('calc', 'r(8)', 0.03, ''),
    '9.80665': 'input: standard gravity', '41.9': ('calc', '400*2*math.pi/60', 0.002, ''), '1.34': ('calc', 'r(400)', 0.005, ''),
},
'01': {
    '67': ('calc', 'r(8)', 0.03, ''), '30': SOL, '1.3': ('calc', 'r(400)', 0.03, ''), '400': SOL, '90': SOL, '18': SOL,
    '300': ('calc', '0.9*r(8)/0.2', 0.01, 'largest R'),
},
'02': {
    '45': ('calc', 'math.degrees(math.atan(1))', 1e-9, 'lag at kappa = |R-1|'), '90': 'def: right angle', '30': SOL, '60': SOL,
    '18': SOL, '400': SOL,
},
'03': {
    '30': ('calc', '2**5', 0.1, 'error ratio of a fifth-order method when the step halves'), '36': 'def: count of runs',
    '0.05': SOL, '0.1': SOL, '0.2': SOL, '0.01': 'def: chaos threshold chosen in the notes (per radian)',
    '3.06': ('calc', '9.80665/(4**2*0.2)', 0.01, 'G of the chaos case'), '0.030': SOL, '0.022': SOL, '0.045': SOL,
    '0.006': SOL, '300': ('calc', '0.9*r(8)/0.2', 0.01, ''), '70': 'def: grid limit chosen for the map',
    '16': 'def: count, 8 starts x 2 brakes', '40': ('calc', '0.3*r(20)/0.2', 0.01, 'smallest R on a large turbine'),
},
'04': {
    '0.2': 'def: damping ratio and rod length chosen for the experiment', '0.1': SOL, '0.028': 'input: chosen noise strength',
    '0.05': 'def: illustration of the swing size', '48': 'input: chosen noise strength', '40': 'def: window length chosen',
    '1000': 'def: count of runs', '1.08': ('calc', '1.0793', 0.01, ''), '1.0793': NREL, '2009': 'def: year of the reference',
    '126': NREL, '500': 'def: report number', '38060': 'def: report number', '4.38': NREL,
    '9.07': ('calc', 'json.load(open(D/"L2_run_nrel.json"))["Om0"]*60/(2*math.pi)', 0.002, 'rotor speed at 8 m/s'),
    '61400': 'def: standard number', '1.86': ('calc', '0.16*(0.75*8 + 5.6)', 0.01, 'IEC sigma_1, class A, 8 m/s'),
    '10 000': 'def: unit (parts in 10 000)', '30': 'def: pivot fraction', '60': 'def: pivot fraction', '90': 'def: pivot fraction',
    '63': NREL, '61.5': NREL, '8.98': ('calc', '871.0/97', 0.002, 'region 1.5/2 boundary, generator 871 rpm through the 97:1 gearbox'), '20': 'input: chosen tip shaking level', '100': 'input: chosen tip shaking level',
    '280': ('calc', '0.9*63.0/0.2', 0.02, 'R at 90 % of the 63 m rotor'),
    '2.4': ('calc', 'math.sqrt(0.9*63.0/0.2)*0.9494/(2*math.pi)/1.0793', 0.03, 'rod frequency over blade frequency'),
    '0.5': 'input: blade damping chosen (0.5 and 3 %)', '45': ('calc', 'math.degrees(math.atan(1))', 1e-9, 'lag at the best brake (2.4)'), '2.3': NREL + ' (chord near the root)',
},
'05': {
    '0.12': ('calc', '0.186e-3/1.53*1e3', 0.02, 'L/R of the coil, ms'), '25': GEN, '20': GEN, '24': GEN, '339152': GEN,
    '1.53': GEN, '20.8': GEN, '30.4': GEN, '0.01': 'def: floor of the smoothing band, rad', '460': GEN, '60': 'def: seconds per minute', '0.02076': ('calc', '60/(2*math.pi*460)', 1e-3, ''),
    '400': SOL, '30': SOL, '14.7': GEN, '32': GEN, '0.7': GEN, '1.5': GEN, '51': GEN, '100': SOL, '40.2': GEN, '10 900': GEN,
    '80': GEN, '75': GEN, '70': GEN, '190': GEN, '246': GEN, '492': GEN, '14': GEN, '33': GEN, '111': GEN,
    '0.5': 'def: swing limit chosen for the small-swing equations', '8000': GEN, '18': SOL,
    '50': 'input: pessimistic efficiency chosen for the sensitivity test', '300': ('calc', '0.9*r(8)/0.2', 0.01, ''),
    '40': ('calc', '0.3*r(20)/0.2', 0.01, ''),
},
}
