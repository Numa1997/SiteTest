"""The sensor node's power need, from the two datasheets' typical values.

Run: python3 -I sensor.py   (writes sensor.json)
Node: an ADXL362 accelerometer sampling continuously, and a CC2652R radio chip that sleeps in standby and once per second wakes
for 1 ms of computing and 1 ms of sending.
  ADXL362 (Analog Devices, Rev. D (2015), Table 1; dossier-sensor.md: Rev. G could not be opened): measurement mode, 100 Hz output data rate, 1.8 uA at V_S = 2.0 V.
  CC2652R (Texas Instruments, SWRS207J, sections 8.5 and 8.6, V_DDS = 3.0 V): standby 0.94 uA (RTC on, RAM and CPU retention);
  MCU active 3.39 mA; radio transmit at 0 dBm 7.0 mA.
Left out: the radio's start-up and receive windows and the losses of a power converter.
"""
import json, os

acc = 1.8e-6*2.0                                  # W
standby = 0.94e-6*3.0                             # W
period = 1.0                                      # s between reports
burst = (3.39e-3*3.0*1e-3 + 7.0e-3*3.0*1e-3)/period   # 1 ms computing + 1 ms sending, J per period -> W
need = acc + standby + burst
print(f'accelerometer {acc*1e6:.2f} uW, standby {standby*1e6:.2f} uW, compute and send {burst*1e6:.2f} uW: need {need*1e6:.1f} uW')
json.dump(dict(acc_uW=acc*1e6, standby_uW=standby*1e6, burst_uW=burst*1e6, need_uW=need*1e6),
          open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sensor.json'), 'w'), indent=1)
ok = abs(need*1e6 - 37.59) < 0.01
print(('PASS' if ok else 'FAIL') + ' need = 3.6 + 2.82 + 31.17 uW'); raise SystemExit(0 if ok else 1)
