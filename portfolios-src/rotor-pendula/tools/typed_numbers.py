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
SET = 'input: the winds, pivots and settings chosen for these notes (section 0.3)'
SEN = 'input: sensor datasheets, ADXL362 Rev. G Table 1 and CC2652R SWRS207J sections 8.5-8.6 (sensor.py)'
SIZE = 'def: the mass series of the sizing rule (design.py)'
GEN = 'input: maxon catalogue, RE 25 page 153 / GP 32 C pages 430-431 (dossier-generator.md)'
NREL = 'input: Jonkman et al. 2009, NREL/TP-500-38060, and the OpenFAST r-test blade file (dossier-turbine.md)'

TYPED = {
'00': {
    '60': 'input: blade length of large turbines, order of magnitude (NREL 5 MW blade 61.5 m)', '50': 'def: illustration, 50 m out along a blade',
    '20': 'def: illustration, 20 years of service; and the box size, 20 cm', '30': SET, '60': SET, '90': SET, '100': 'def: tip vibration of the range (chapter 6) and the sampling rate 100 Hz',
    '63': NREL, '6.9': NREL + ' (cut-in rotor speed, Table 1-1)', '12.1': NREL + ' (rated rotor speed, Table 1-1)',
    '0.41': ('calc', '0.180*(2.313 + 0.25*(2.086 - 2.313))', 0.02, 'thickness at 90 %: NACA64 18 % of the 2.256 m chord (dossier-turbine.md)'),
    '2.26': ('calc', '2.313 + 0.25*(2.086 - 2.313)', 0.01, 'chord at 90 %, interpolated from Table 3-1'),
    '0.01': SIZE, '0.02': SIZE, '0.05': SIZE, '0.1': SIZE, '0.2': SIZE, '0.5': SIZE,
    '1.8': SEN, '2.0': SEN, '0.94': SEN, '3.0': SEN, '3.39': SEN, '7.0': SEN,
    '9.80665': 'input: standard gravity',
},
'01': {
    '30': SET, '90': SET,
},
'02': {
    '45': ('calc', 'math.degrees(math.atan(1))', 1e-9, 'lag at kappa = |R-1|'), '90': 'def: right angle', '30': SET, '60': SET,
},
'03': {
    '30': ('calc', '2**5', 0.1, 'error ratio of a fifth-order method when the step halves'), '16': 'def: count, 8 starts x 2 brakes',
    '0.01': 'def: chaos threshold chosen in the notes (per radian)', '0.1': 'def: grid limit chosen for the map',
    '200': 'def: grid limit chosen for the map', '600': 'def: grid limit chosen for the map',
},
'04': {
    '0.2': 'def: damping ratio chosen for the experiment', '40': 'def: window length chosen',
    '1000': 'def: count of runs', '1.08': ('calc', '1.0793', 0.01, ''), '1.0793': NREL, '2009': 'def: year of the reference',
    '126': NREL, '500': 'def: report number', '38060': 'def: report number', '4.38': NREL,
    '9.07': ('calc', 'json.load(open(D/"L2_run_nrel.json"))["Om0"]*60/(2*math.pi)', 0.002, 'rotor speed at 8 m/s'),
    '61400': 'def: standard number', '1.86': ('calc', '0.16*(0.75*8 + 5.6)', 0.01, 'IEC sigma_1, class A, 8 m/s'),
    '10 000': 'def: unit (parts in 10 000)', '30': 'def: pivot fraction', '60': 'def: pivot fraction', '90': 'def: pivot fraction',
    '63': NREL, '61.5': NREL, '8.98': ('calc', '871.0/97', 0.002, 'region 1.5/2 boundary, generator 871 rpm through the 97:1 gearbox'), '20': 'input: chosen tip shaking level', '100': 'input: chosen tip shaking level',
    '0.5': 'input: blade damping chosen (0.5 and 3 %)', '45': ('calc', 'math.degrees(math.atan(1))', 1e-9, 'lag at the best brake (2.4)'), '2.3': NREL + ' (chord near the root)',
},
'05': {
    '0.12': ('calc', '0.186e-3/1.53*1e3', 0.02, 'L/R of the coil, ms'), '25': GEN, '20': GEN, '24': GEN, '339152': GEN,
    '1.53': GEN, '20.8': GEN, '30.4': GEN, '0.01': 'def: floor of the smoothing band, rad', '460': GEN, '60': 'def: seconds per minute', '0.02076': ('calc', '60/(2*math.pi*460)', 1e-3, ''),
    '30': SET, '90': SET, '14.7': GEN, '32': GEN, '0.7': GEN, '1.5': GEN, '51': GEN, '111': GEN, '40.2': GEN, '10 900': GEN,
    '80': GEN, '75': GEN, '70': GEN, '100': 'def: turns to settle', '8000': GEN,
    '0.5': 'def: swing limit chosen for the small-swing equations', '50': 'input: pessimistic efficiency chosen for the sensitivity test',
},
}
