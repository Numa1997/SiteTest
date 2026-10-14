# Primary sources and provenance

Access date: 2026-10-14. No datasheet PDFs are included.

## ADXL362 Rev. G, May 2023

URL: https://www.analog.com/media/en/technical-documentation/data-sheets/adxl362.pdf

SHA-256: `895468ab604df0a02c9f9c9cee31531eac764980f8ebc1812fbe61d9d6b1172b`

Downloaded bytes: 1728067; HTTP 200. Derived budget uses the stated typical currents. Pages 4–5: 1.8 µA typical at 100 Hz ODR and 2.0 V; selectable ±2/±4/±8 times g ranges.

## CC2652R SWRS207J, revised November 2023

URL: https://www.ti.com/lit/ds/symlink/cc2652r.pdf

SHA-256: `99122846e9347996e9ceca17f096a73f9a9ec4d4ceea2f3c40e32e14d8b96f49`

Downloaded bytes: 2540109; HTTP 200. Derived budget uses the stated typical currents. Sections 8.5–8.6, pages 10–11: VDDS=3.0 V, DC/DC enabled, Tc=25 °C. 7.0 mA TX at setting 0 dBm (1 mW RF); 3.39 mA CPU CoreMark at 48 MHz; 0.94 µA standby with RCOSC_LF and retained RAM.

## Assumed schedule

Continuous 100 Hz sensing; each second 1 ms transmission, 1 ms CPU operation, 998 ms standby. Assumed 1000 total on-air bits at 1 Mbit/s, sending features rather than all raw tri-axis samples. Converter efficiency 0.5. Derived typical-current reference: 37.58436 µW electrical and 75.16872 µW mechanical at that efficiency. Radio/CPU startup, receive/retry windows, peripheral power, converter leakage and storage losses are excluded. An optional 1 mW electrical planning allowance is an assumption, not a sourced specification.

## Fonts

Instrument Serif Regular from https://github.com/Instrument/instrument-serif (included OTF and OFL). IBM Plex Sans Regular from release https://github.com/IBM/plex/releases/tag/%40ibm%2Fplex-sans%401.1.0 ; IBM Plex Mono Regular from release https://github.com/IBM/plex/releases/tag/%40ibm%2Fplex-mono%402.5.0 . Font bytes were retrieved from their tagged Git objects on github.com; no external asset host was accessed. OFL licenses included.

- IBMPlexSans-Regular.otf: `6b17a35a31ded2e81b3ed19e5eb532d22b9a0b5a76833b0d757a5c71ab5e0f6c`
- Instrument-OFL.txt: `129ed7618959716959f2941fdd5b49e0ad6e6c1d78726761786a00253d865521`
- InstrumentSerif-Regular.otf: `8299613dc56e9530d6a416cf8b9b24c209457f9ea66a7c118a024c7714c01cd6`
- IBMPlexMono-Regular.otf: `372fe8f8a459baef84ee346b0a478084e80c46bd299a0c27bcb0f3412f5a9d28`
- IBM-OFL.txt: `7e6b2818edbd8f6a01ae80641cc8f16a51080d08fb4e532be3a0b6f74adb07da`

## Local study provenance

The lite archive contains original code, manifests and report fragments, not the lost report or the original damaged delivery. The mechanics were reproduced from those files. C1 historical damage, C6 survivor statistics and C7 original missing block values cannot be independently verified from this attachment; fresh results replace them. The aerodynamic statement tying C_p to a universally necessary tip-speed interval is unproved without a blade model. All turbine parameters in this report are illustrative assumptions.
