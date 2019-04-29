#!/usr/bin/env python3
# coding=utf-8
import csv
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize, curve_fit

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


def fit(xs, ys, model, initial_params):
    def err_f(params):
        # return np.mean(np.power(np.log(ys) - np.log(model(xs, params)), 2))
        return np.mean(np.power(ys - model(xs, params), 2))

    res = minimize(
        err_f,
        x0=initial_params,
        method="Nelder-Mead",
        tol=1e-7,
        options={"maxiter": 10000, "disp": False},
    )
    print(res)
    print("Residual error:", err_f(res.x))
    return res.x


# Import data
T, Vout = [], []
with open("lab-9-small-waves.csv") as f:
    c = csv.reader(f, delimiter=",")
    for _ in range(23):  # Throw away 23 lines of header
        next(c)
    for row in c:
        T += [float(row[0]) * 1000]  # seconds to ms
        Vout += [float(row[1])]

# Generate square wave
Vin = [(3 - 0.05) if np.ceil(t * 10) % 2 == 0 else (3 + 0.05) for t in T]

# Extract a pair of up- and down-slopes
T_up, Vout_up, T_down, Vout_down = [], [], [], []
upper_thresh = 3.01
lower_thresh = 2.92
# lower_thresh = 2.98

# TODO: Refactor this?
i = 0
while T[i] < 0:
    i += 1

while Vout[i] < lower_thresh:
    i += 1

while Vout[i] < upper_thresh:
    # while T[i] < 0.045:
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


# Do curve fits.
def model(x, params):
    return np.exp((np.array(x) * params[0]) + params[1]) + params[2]


p_up = fit(T_up, Vout_up, model, [-1.5, 0, -3.01])
p_down = fit(T_down, Vout_down, model, [1, 0, 2.91])


def model_split(x, a, b, c):
    return model(x, [a, b, c])


# print(curve_fit(model_split, T_up, Vout_up))


def model_less(x, params):
    return model(x, [params[0], params[1], 3.02])


fit(T_up, Vout_up, model_less, [1, 0])

# Plot things
fig = plt.figure(figsize=(8, 6))
ax = plt.subplot(111)

ax.plot(T, Vin, "-", label="Input voltage")
ax.plot(T, Vout, ".", markersize=2, label="Output voltage")
ax.plot(
    T_up,
    model(T_up, p_up),
    "-",
    label="Theoretical fit (upward swing, τ=%g ms)" % (-1 / p_up[0]),
)
ax.plot(
    T_down,
    model(T_down, p_down),
    "-",
    label="Theoretical fit (downward swing, τ=%g ms)" % (-1 / p_down[0]),
)
plt.xlim(-0.03, 0.15)
plt.title("Small-Amplitude Voltage Follower Step Response")
plt.xlabel("Time (ms)")
plt.ylabel("Voltage (V)")
plt.grid(True)
ax.legend()
plt.savefig("exp3_small.pdf")
plt.cla()


# Next, the larger amplitude.
# Import data
T, Vout = [], []
with open("lab-9-large-waves.csv") as f:
    c = csv.reader(f, delimiter=",")
    for _ in range(23):  # Throw away 23 lines of header
        next(c)
    for row in c:
        T += [float(row[0]) * 1000]  # seconds to ms
        Vout += [float(row[1])]

# Generate square wave
Vin = [(3 - 1) if np.ceil(t * 1) % 2 == 0 else (3 + 1) for t in T]

# Extract a pair of up- and down-slopes
T_up, Vout_up, T_down, Vout_down = [], [], [], []
upper_thresh = 3.8
lower_thresh = 2.1

# TODO: Refactor this?
i = 0
while T[i] < 0:
    i += 1

while Vout[i] < lower_thresh:
    i += 1

while Vout[i] < upper_thresh:
    # while T[i] < 0.045:
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

m_up, b_up = np.polyfit(T_up, Vout_up, 1)
m_down, b_down = np.polyfit(T_down, Vout_down, 1)

# Plot things
ax.plot(T, Vin, "-", label="Input voltage")
ax.plot(T, Vout, ".", markersize=2, label="Output voltage")
ax.plot(
    T_up,
    (np.array(T_up) * m_up) + b_up,
    "-",
    label="Theoretical fit (upward swing, slope=%g V/ms)" % m_up,
)
ax.plot(
    T_down,
    (np.array(T_down) * m_down) + b_down,
    "-",
    label="Theoretical fit (downward swing, slope=%g V/ms)" % m_down,
)
plt.xlim(-0.3, 1.5)
plt.title("Large-Amplitude Voltage Follower Step Response")
plt.xlabel("Time (ms)")
plt.ylabel("Voltage (V)")
plt.grid(True)
ax.legend()
plt.savefig("exp3_large.pdf")
plt.cla()
