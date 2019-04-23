#!/usr/bin/env python2
# coding=utf-8
import smu
import numpy as np

s = smu.smu()

v = np.linspace(-.1, .1, 1000)

filename = "data/exp2_part1_v2=3.499.csv"
measuring = "Vout"

f = open(filename, 'w')
f.write("V1, {!s}\n".format(measuring))

s.set_voltage(1,0)
s.autorange(1)
s.set_current(2,0)
s.set_vrange(2, 0)
#s.autorange(2)

for val in v:
    s.set_voltage(1,val)
    s.autorange(1)
    s.set_current(2,0)
    #s.autorange(2)
    f.write('{!s},{!s}\n'.format(val, s.get_voltage(2)))

s.set_current(1,0)
f.close()
