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

SET = 'input: a setting chosen for these notes (chapter 1)'
NREL = 'input: Jonkman, Butterfield, Musial and Scott 2009, NREL/TP-500-38060 (the NREL 5 MW reference turbine)'
GEN = 'input: maxon catalogue, RE 25 part 339152 and GP 32 C gearhead (chapter 5, sources)'
MC = 'input: setting of the Monte Carlo run of the earlier point and double pendulum study (power_theorem_mc.py, mc_full.log)'
YEAR = 'def: year of a cited source'

_OLD = {
'00': {
    '13': ('calc', "100*(1 - json.load(open(D/'L2_steady.json'))[0]['nrel']['P_ratio'])", 0.05, 'loss at 6 m/s with the real control, %'),
    '6.9': ('calc', '670/97', 0.01, NREL + ': region 1.5 starts at 670 generator rpm, through 97:1'),
    '1920': YEAR, '61.5': ('calc', "S['R_ROT'] - S['R_HUB']", 1e-9, 'blade length = rotor radius - hub radius'),
    '1.5': ('calc', "S['R_HUB']", 1e-9, NREL + ' (hub radius)'), '17.7': 'input: blade mass 17 740 kg (' + NREL + ', Table 2-1)',
    '60': 'def: order of magnitude of a large blade (NREL 5 MW blade 61.5 m), and the illustration "60 m out along a blade"',
    '63': ('calc', "S['R_ROT']", 1e-9, 'rotor radius of the NREL 5 MW turbine'),
    '7.55': ('calc', "S['LAM_STAR']", 1e-9, NREL), '0.482': ('calc', "S['CP_STAR']", 1e-9, NREL),
    '2009': YEAR, '9.80665': 'input: standard gravity (CGPM 1901)',
    '100': 'def: the largest tip vibration tried in chapter 6 (100 mm)',
    '50': ('calc', '0.5*10**2', 1e-9, 'kinetic energy per kilogram at 10 m/s, J/kg (warm-up of section 0.1)'),
    '16': 'def: numerator of the Betz limit 16/27', '27': 'def: denominator of the Betz limit 16/27',
    '90': NREL + ' (hub height)', '12': NREL + ' (rated rotor speed 12.1 rpm, "at most about 12 turns a minute")', '97': NREL + ' (gearbox ratio 97:1)',
    '12 m/s': 'def: the storm wind of problem 1', '31.5': ('calc', "S['R_ROT']/2", 1e-9, 'halfway out along the rotor radius (problem 4)'),
    '11.4': NREL + ' (rated wind speed)', '33600': 'def: battery model name, Saft LS 33600 (D-size lithium cell)',
    '1.8': 'input: ADXL362 datasheet, measurement mode 100 Hz, 1.8 uA (sensor.py)', '2.0': 'input: ADXL362 supply voltage 2.0 V (sensor.py)',
    '3.6': ('calc', '1.8*2.0', 1e-9, 'accelerometer power, uW; also the Saft LS 33600 cell voltage, 3.6 V'),
    '0.94': 'input: CC2652R standby current, uA (SWRS207J, sensor.py)', '3.0': 'input: CC2652R supply voltage (sensor.py)',
    '2.8': ('calc', '0.94*3.0', 0.01, 'standby power, uW'), '3.39': 'input: CC2652R MCU active current, mA (sensor.py)',
    '7.0': 'input: CC2652R radio transmit current at 0 dBm, mA (sensor.py)', '10.2': ('calc', '3.39*3.0', 0.01, 'computing energy per second, uJ'),
    '21.0': ('calc', '7.0*3.0', 1e-9, 'sending energy per second, uJ'), '31.2': ('calc', '3.39*3.0 + 7.0*3.0', 0.01, 'burst energy per second, uJ'),
    '61': ('calc', '17*3.6', 0.02, 'energy of a Saft LS 33600 D cell, Wh'), '17': 'input: Saft LS 33600 datasheet, 17 Ah nominal',
    '45': ('calc', "S['LAM_STAR']*6", 0.01, 'tip speed at 6 m/s'), '76': ('calc', "S['LAM_STAR']*10", 0.01, 'tip speed at 10 m/s'),
    '20': ('calc', '2*1*10', 1e-9, 'volume of air through the 2 m x 1 m doorway in one second at 10 m/s, m^3'),
    '126': ('calc', "2*S['R_ROT']", 1e-9, 'rotor diameter: the tip rises from the bottom of its circle to the top'),
},
'01': {
    '9.81': ('calc', "S['G0']", 0.001, 'standard gravity, rounded'), '126': ('calc', "2*S['R_ROT']", 1e-9, 'rotor diameter: the height the tip climbs each turn'),
    '90': 'def: angle in degrees (a rod hanging straight down)',
    '45': ('calc', 'math.degrees(math.atan(1))', 1e-9, 'lag at the best brake, tan delta = 1 (chapter 2)'),
    '63': ('calc', "S['R_ROT']/S['L_B']", 1e-9, 'r_p, and r_p over l'),
},
'02': {
    '12': 'input: the battery voltage of the warm-up (V)', '16': ('calc', '12**2*1/(2+1)**2', 1e-9, 'lamp power at 1 ohm and at 4 ohm, W'),
    '18': ('calc', '12**2*2/(2+2)**2', 1e-9, 'lamp power at 2 ohm, W'), '80': ('calc', '100*2*2/(1+2**2)', 1e-9, 'power at twice or half the best brake, % of P*'),
    '0.05': 'input: the lightest brake of the comparison sweep, in units of kappa* (tools/compare.js)',
    '45': ('calc', 'math.degrees(math.atan(1))', 1e-9, 'lag at kappa = |R-1|'), '90': 'def: right angle',
    '63': ('calc', "S['R_ROT']/S['L_B']", 1e-9, 'r_p, and r_p over l'),
},
'03': {
    '0.5': ('calc', "S['M_B']*S['L_B']/2", 1e-9, 'first moment of the uniform rod, kg m (problem 4)'),
    '240': 'input: steps per turn of the runs (L1_blade.py)', '60': 'input: turns let pass before measuring (L1_blade.py)',
},
'04': {
    '7.55': ('calc', "S['LAM_STAR']", 1e-9, NREL), '6.87': ('calc', "S['LAM_STAR']*6/S['R_ROT']*60/(2*math.pi)", 0.001, 'rotor speed at lambda* and 6 m/s, rpm'),
    '6.9': ('calc', '670/97', 0.01, NREL + ': region 1.5 starts at 670 rpm of the generator, through the 97:1 gearbox'),
    '23': ('calc', '100*1.86/8', 0.02, 'turbulence intensity at 8 m/s, %'),
    '0.1': MC, '0.2': MC, '0.028': MC, '48': MC, '0.05': MC, '1000': MC, '40': MC,
    '1.0793': ('calc', "META['f_e']", 1e-9, NREL + ', first edgewise blade mode'),
    '1.08': ('calc', "META['f_e']", 0.005, 'the same frequency, rounded'),
    '4.38': 'input: rotor plus drivetrain inertia at the rotor, 4.38e7 kg m^2 (' + NREL + ')',
    '8.98': 'input: the generator torque law of the NREL 5 MW controller, region 2 to 2.5 (' + NREL + ')',
    '1.86': ('calc', '0.16*(0.75*8 + 5.6)', 0.003, 'IEC 61400-1 ed. 3 normal turbulence, class A, at 8 m/s'),
    '61400': 'def: name of the standard IEC 61400-1', '2009': YEAR, '61.5': 'input: blade length (' + NREL + ')',
    '10 000': 'def: unit of the share (parts in 10 000)', '45': 'def: lag at the best brake (section 3.3)',
    '20': 'input: tip vibration tried in chapter 6 (mm)', '100': 'input: tip vibration tried in chapter 6 (mm)',
    '0.5': 'input: blade damping ratio tried in chapter 6 (%)',
},
'05': {
    '63': ('calc', "S['R_ROT']", 1e-9, 'rotor radius, m'), '64': ('calc', "S['R_ROT'] + S['L_B']", 1e-9, 'end of the second blade, m'),
    '13': ('calc', "100*(1 - json.load(open(D/'L2_steady.json'))[0]['nrel']['P_ratio'])", 0.05, 'loss at 6 m/s with the real control, %'),
    '12.7': ('calc', "2*math.sqrt(S['M_B']/S['L_B']/7850/math.pi)*1000", 0.005, 'diameter of a 1 kg, 1 m steel rod, mm (steel 7850 kg/m^3)'),
    '34': ('calc', "abs(json.load(open(D/'L5_air.json'))['runs']['a3']['cases']['rod']['Ft'])", 0.02, 'drag of the bare rod, N'), '9.8': ('calc', "S['G0']*S['M_B']", 0.01, 'weight of 1 kg, N'),
    '1.2': 'input: drag coefficient of a round rod near Reynolds number 5e4 (textbook value); also the 1.2 of section 7.1 if any',
    '31': ('calc', "abs(json.load(open(D/'L5_air.json'))['runs']['a3']['cases']['rod']['lean_deg'])", 0.02, 'lean of the bare rod, deg'), '135': ('calc', "abs(json.load(open(D/'L5_air.json'))['runs']['a3']['cases']['sym']['P_rotor'])", 0.01, 'power the streamlined blade costs the rotor, W'),
    '17': ('calc', "json.load(open(D/'L5_air.json'))['runs']['a3']['cases']['wing']['lean_deg']", 0.03, 'lean of the small wing, deg'),
    '27': ('calc', "90 - S['R_ROT']", 1e-9, 'lowest height of the tip, m (hub 90 m)'), '153': ('calc', "90 + S['R_ROT']", 1e-9, 'highest height of the tip, m'),
    '4.5': ('calc', "2*abs(json.load(open(D/'L5_air.json'))['runs']['a3']['cases']['sym']['Ft'])", 0.01, 'drag of the streamlined blade at twice the chord, N'),
    '4.4': ('calc', "math.degrees(math.atan(2*abs(json.load(open(D/'L5_air.json'))['runs']['a3']['cases']['sym']['Ft'])/(S['M_B']*(S['LAM_STAR']*8/S['R_ROT'])**2*S['R_ROT'])))", 0.01, 'its lean, deg'),
    '270': ('calc', "2*abs(json.load(open(D/'L5_air.json'))['runs']['a3']['cases']['sym']['P_rotor'])", 0.01, 'its cost to the rotor, W'),
    '0.01': 'def: series of masses', '0.02': 'def: series of masses', '0.05': 'def: series of masses', '0.1': 'def: series of masses',
    '0.2': 'def: series of masses', '0.5': 'def: series of masses; and the swing limit chosen for the sizing (rad)',
    '25': GEN + ' (name and diameter)', '32': GEN + ' (name)', '339152': GEN, '20': GEN + ' (rated power, W); and the upper end of 5 to 20 % for tip brakes (US 8 403 641)', '24': GEN + ' (winding, V)',
    '1.53': GEN, '20.8': GEN, '460': GEN, '14.7': GEN, '40.2': GEN, '10 900': GEN, '30.4': GEN, '0.7': GEN, '1.5': GEN,
    '80': GEN, '75': GEN, '70': GEN, '60': GEN + ' (gear efficiency per stage count; and 60 in k_e = 60/(2 pi K_n))',
    '8000': GEN, '492': GEN + ' (largest ratio)', '0.12': GEN + ' (terminal inductance over resistance)',
    '0.02076': ('calc', '60/(2*math.pi*460)', 1e-4, 'k_e from the speed constant'),
    '50': 'input: pessimistic gear efficiency of the sensitivity test (L4_sensitivity.py)',
    '26': 'def: journal volume (source list)', '307': 'def: page (source list)', '309': 'def: page (source list)', '1920': YEAR,
    '30': 'input: the heaviest mass density of the range of sizes, kg per metre (sizes.py, section 7.6)',
    '10 927 809': 'def: US patent number (source list)', '8 403 641': 'def: US patent number (source list)',
    '100': 'def: the largest tip vibration tried in chapter 6 (100 mm)',
},
}

# The notes were reordered into one story on 28 October 2026 (01 double pendulum, 02 the tip, 03 brake, 04 swings, 05 watts,
# 06 wind, 07 air, 08 shaking, 09 answer). Each new file takes the entries of the old files its text came from, plus its own.
def _merge(*parts):
    out = {}
    for p in parts:
        out.update(_OLD[p] if isinstance(p, str) else p)
    return out

DP = 'input: the site\'s double pendulum, Fig. 2 (public/simulations/Double Pendulum.html), as run by tools/double_pendulum.js'
WIND = 'input: the wind model of section 6.4 (IEC 61400-1 ed. 3 as in the TurbSim User\'s Guide 1.50; notes/rotor-pendula/derive/L6_wind.py)'
TYPED = {
    '01': _merge('00', '01', {
        '120': DP + ' (starting angle, deg)', '150': DP + ' (starting angle, deg)', '600': DP + ' (steps per second)',
        '4.4': 'input: rotor and drivetrain inertia, 4.38e7 kg m^2, rounded (' + NREL + ')',
        '0.02': 'def: threshold of a chaotic start, per turn (tools/double_pendulum.js)', '400': 'def: turns measured (tools/double_pendulum.js)',
        '0.1': 'def: lowest Gamma of the sweep (tools/double_pendulum.js)', '30': 'def: highest Gamma of the sweep, rounded (31.6)',
        '20': 'def: turns of the reduction check (tools/double_pendulum.js)', '18': 'input: blade mass 17 740 kg, rounded (' + NREL + ')',
        '1.0': 'def: arm length of the site\'s double pendulum, m',
        '1000': 'def: the factor of the example after (1.9)', '49': 'def: section of Landau and Lifshitz, Mechanics (adiabatic invariants)',
        '51': 'def: section of Landau and Lifshitz, Mechanics (accuracy of the adiabatic invariant)',
    }),
    '02': _merge('01', {'3': 'def', '7': 'input: deceleration of the braking car in the problem, m/s^2'}),
    '03': _merge('02', {'2': 'def'}),
    '04': _merge('03', {'20': 'input: the start-up check of notes/rotor-pendula/derive/L1_blade.py runs 20 turns from rest (eng20)', '2.8': 'input: stability limit of the classical Runge-Kutta method on the negative real axis, h|mu| < 2.785 (textbook value)'}),
    '05': _merge('05'),
    '06': _merge('00', '04', {
        '0.16': 'input: I_ref of turbulence class A (IEC 61400-1 ed. 3)', '0.75': WIND, '5.6': WIND, '0.8': WIND, '0.5': WIND,
        '340': ('calc', '8.1*42', 0.001, 'L_u = 8.1 Lambda_1, m'), '113': ('calc', '2.7*42', 0.005, 'L_v, m'), '28': ('calc', '0.66*42', 0.02, 'L_w, m'),
        '0.12': WIND + ' (coherence offset)', '0.2': WIND + ' (shear exponent)', '12.6': ('calc', '126/10', 1e-9, 'grid step, m'),
        '121': ('calc', '11*11', 1e-9, 'grid points'), '81': 'def: grid points on the disc (L6_wind.py)', '256': WIND + ' (record length, s)',
        '0.01': 'def: lower edge of the spectrum check, Hz', '0.32': 'def: upper edge of the spectrum check, Hz', '1938': YEAR, '1988': YEAR,
        '153': ('calc', '90 + 63', 1e-9, 'highest height of the tip, m'), '27': ('calc', '90 - 63', 1e-9, 'lowest height of the tip, m'),
        '40': 'def: records of the ensemble check (L6_wind.py)', '4.38': 'input: rotor plus drivetrain inertia (' + NREL + ')',
        '-5/3': 'def', '0.6': 'input: upper frequency of the coherence figure', '0.466': 'input: peak of the ROSCO C_p table at pitch 0, Catmull-Rom on its grid (nrel5mw.cp_table, turbulence.cp)',
        '7.64': 'input: tip-speed ratio of that peak (same source)', '255': 'def: frequencies of a 256 s record below 1 Hz', '1 to': 'def', '17': ('calc', '12*12.6/math.log(2)/12.6', 0.03, 'eddy length over separation'),
    }),
    '07': _merge('05', {
        '60': 'def: apparent wind at the tip, rounded (section 6.3)', '0.6': ('calc', "math.degrees((2/3)*math.cos(math.radians(5))/math.hypot(60.4, 5.31))", 0.05, 'inflow change for 1 m/s, deg'),
        '7': ('calc', "100*2*math.pi*math.radians(0.63)", 0.05, 'lift change for 1 m/s, %'), '1': 'def', '256': WIND + ' (record length, s)', '2': 'def',
        '90': 'def: angle in degrees (the mother blade pointing up, section 7.2)',
        '126': ('calc', "2*S['R_ROT']", 1e-9, 'rotor diameter: the circle the tip runs round (section 7.4)'),
        '1.81': 'input: dynamic viscosity of air, 1.81e-5 Pa s, as notes/rotor-pendula/derive/L5_air.py uses it (Reynolds number, section 7.1)',
    }),
    '08': _merge('04', '05', {'5': 'def', '3': 'def'}),
    '09': _merge('05', '00', {'1976': YEAR, '1938': YEAR, '1941': YEAR, '1988': YEAR}),
}
