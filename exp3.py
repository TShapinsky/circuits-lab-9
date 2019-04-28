#!/usr/bin/env python3
# coding=utf-8
import csv
import numpy as np
import matplotlib.pyplot as plt

"""
Is the response symmetrical? Does the amplifier exhibit approximately
linear behavior? Extract a time constant both for the up-going and for the down-going
output transitions. How do these compare with that which you compute from the measured
values of the load capacitance and the differential-mode transconductance gain that you
found in Experiment 2? In your report, include a single plot showing both scope traces
along with the extracted time constants.

[...]

Is the response symmetrical? [...] Extract a slew rate for both for
the up-going and for the down-going output transitions. How do these compare with those
which you compute from the load capacitance and the limiting values of the output current?
In your report, include a single plot showing both scope traces along with the extracted slew
rates.
"""

"""
Square wave has amplitude 50mV, offset 3V, freq 5kHz, 50% duty cycle, goes high at t=0
"""

# Import data
T, Vout = [], []
with open("lab-9-small-waves.csv") as f:
    c = csv.reader(f, delimiter=",")
    for _ in range(23):  # Throw away 23 lines of header
        next(c)
    for row in c:
        T += [float(row[0])]
        Vout += [float(row[1])]

# Generate square wave
Vin = [(3 - 0.05) if np.ceil(t * 5000) % 2 == 0 else (3 + 0.05) for t in T]

# Extract a pair of up- and down-slopes
T_up, Vout_up, T_down, Vout_down = [], [], [], []
upper_thresh = 3.00
lower_thresh = 2.93

# TODO: Refactor this?
i = 0
while T[i] < 0:
    i += 1

while Vout[i] < lower_thresh:
    i += 1

while Vout[i] < upper_thresh:
    T_up += [T[i]]
    Vout_up += [Vout[i]]
    i += 1

i += 10  # to avoid jitter causing another trigger

while Vout[i] > upper_thresh:
    i += 1

while Vout[i] > lower_thresh:
    T_down += [T[i]]
    Vout_down += [Vout[i]]
    i += 1

plt.plot(T, Vin)
plt.plot(T_up, Vout_up)
plt.plot(T_down, Vout_down)
plt.show()
