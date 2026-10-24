# Dossier: sensor and radio supply currents (ADXL362, CC2652R)

Checked 2026-10-24. Datasheet text was extracted with pdftotext from the PDFs themselves; no distributor summary was used for any value.

## Claim 1: ADXL362, 100 Hz ODR, 1.8 uA typ at V_S = 2.0 V

- Reference: Analog Devices, "Micropower, 3-Axis, +-2 g/+-4 g/+-8 g Digital Output MEMS Accelerometer", ADXL362 Data Sheet. The copy I could open is **Rev. D** (Rev. C to Rev. D change dated 11/15; footer date 05-07-2015-C; (c) 2012-2015).
- URL opened: https://hades.mech.northwestern.edu/images/5/58/ADXL362.pdf (university mirror of the ADI PDF; PDF metadata title "ADXL362 (Rev. D)", author Analog Devices, Inc.).
- Road taken: the manufacturer's own PDF (https://www.analog.com/media/en/technical-documentation/data-sheets/ADXL362.pdf, also lowercase `adxl362.pdf` and the ADI host wcm-cce.cldnet.analog.com) could not be opened. curl failed (HTTP/2 INTERNAL_ERROR, empty reply, connection reset), WebFetch returned 503, and the Firecrawl scrape had no credits. Other mirrors: alldatasheet.net returned 403, radiolocman.com returned an empty body. **Rev. G was therefore not read.**
- Location: page 4-5, "SPECIFICATIONS", Table 1, block "POWER SUPPLY", row "Supply Current / Measurement Mode / 100 Hz ODR (50 Hz bandwidth) / Normal Operation".
- Value: 1.8 uA typ (no min or max printed). Neighbouring rows: Low Noise Mode 3.3 uA, Ultralow Noise Mode 13 uA, Wake-Up Mode 0.27 uA, Standby 0.01 uA. Footnote 6: refer to Figure 30 for current at other bandwidth settings.
- Printed conditions (Table 1 header): "TA = 25 C, VS = 2.0 V, VDD I/O = 2.0 V, 100 Hz ODR, HALF_BW = 0, +-2 g range, acceleration = 0 g, default settings for other registers". The first page also prints "1.8 uA at 100 Hz ODR, 2.0 V supply". Operating voltage range V_S: min 1.6, typ 2.0, max 3.5 V.
- Verdict: **CONFIRMED on Rev. D** (1.8 uA typ, V_S = 2.0 V). Not confirmed against Rev. G text itself; a web-search snippet said Rev. G prints the same 1.8 uA at 100 Hz, 2.0 V, but I did not open it. Treat Rev. G as unverified by me.

## Claims 2 and 3 and 4: TI CC2652R

- Reference: Texas Instruments, "CC2652R SimpleLink(TM) Multiprotocol 2.4 GHz Wireless MCU", data sheet **SWRS207J**, **Revision J**, January 2018, revised November 2023 (PDF metadata: "datasheet (Rev. J)", 61 pages).
- URL opened: https://www.ti.com/lit/ds/symlink/cc2652r.pdf (HTTP 200, downloaded and read whole by pdftotext).
- Common conditions printed for 8.5 and 8.6: "When measured on the CC26x2REM-7ID reference design with Tc = 25 C, VDDS = 3.0 V with DC/DC enabled unless otherwise noted."

### Claim 2: standby 0.94 uA typ (RTC on, RAM and CPU retention) at V_DDS = 3.0 V

- Location: section 8.5 "Power Consumption - Power Modes" (printed page 10), "Core Current Consumption", Icore, row "Standby without cache retention".
- Printed test condition: "RTC running, CPU, 80 kB RAM and (partial) register retention. RCOSC_LF". Value 0.94 uA typ. The XOSC_LF row of the same group prints 1.09 uA. "Standby with cache retention" prints 3.2 uA (RCOSC_LF) and 3.3 uA (XOSC_LF). The features list says "Standby: 0.94 uA (RTC on, 80 kB RAM and CPU retention)".
- Verdict: **CONFIRMED** (0.94 uA applies to the RCOSC_LF, no-cache-retention row; V_DDS = 3.0 V).

### Claim 3: MCU active 3.39 mA

- Location: section 8.5, Icore, row "Active".
- Printed test condition: "MCU running CoreMark at 48 MHz, RCOSC_HF". Value 3.39 mA typ. Features list rounds it: "Active mode MCU 48 MHz (CoreMark): 3.4 mA (71 uA/MHz)". Idle row for comparison: 675 uA ("Supply Systems and RAM powered, RCOSC_HF").
- Verdict: **CONFIRMED** (3.39 mA, CoreMark at 48 MHz, V_DDS = 3.0 V, DC/DC on).

### Claim 4: radio transmit 0 dBm, 7.0 mA

- Location: section 8.6 "Power Consumption - Radio Modes" (printed page 11), row "Radio transmit current, 2.4 GHz PA (BLE)".
- Printed test condition: "2440 MHz, 0 dBm output power setting". Value 7.0 mA typ. Same row group: +5 dBm output power setting, 2440 MHz, 9.2 mA. Radio receive current at 2440 MHz is 6.9 mA. Revision J history says the typical Tx currents in 8.6 were updated, so older revisions may print different values.
- Verdict: **CONFIRMED** (7.0 mA at 0 dBm, 2440 MHz, V_DDS = 3.0 V, DC/DC enabled).

## Claim 5: supply voltages

- ADXL362: the Table 1 header prints V_S = 2.0 V (and VDD I/O = 2.0 V); the 1.8 uA figure applies at 2.0 V. Allowed V_S range is 1.6 to 3.5 V (absolute maximum -0.3 to +3.6 V). **CONFIRMED** (2.0 V), read in Rev. D.
- CC2652R: sections 8.5 and 8.6 print V_DDS = 3.0 V with DC/DC enabled. **CONFIRMED** (3.0 V).

## Summary table

| # | Claim | Verdict |
|---|-------|---------|
| 1 | ADXL362, 100 Hz, 1.8 uA, 2.0 V | CONFIRMED on Rev. D (Rev. G not opened) |
| 2 | CC2652R standby 0.94 uA, 3.0 V | CONFIRMED |
| 3 | CC2652R active 3.39 mA (CoreMark, 48 MHz) | CONFIRMED |
| 4 | CC2652R TX 0 dBm 7.0 mA | CONFIRMED |
| 5 | Supply voltages 2.0 V and 3.0 V | CONFIRMED |

Revisions actually read: ADXL362 data sheet **Rev. D** (2015), a mirror of the ADI PDF, which is **not** the current revision (Rev. G is stated as current in the claim; I could not open it). CC2652R data sheet **SWRS207 Rev. J** (November 2023), read at ti.com, which is the revision the TI product page lists as the latest (SWRS207J).
