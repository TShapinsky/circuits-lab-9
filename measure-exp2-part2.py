#!/usr/bin/env python2
# coding=utf-8
import smu
import numpy as np

s = smu.smu()

v = np.linspace(0, 5, 500)

filename = "data/exp2_part2_v2=3.499.csv"
measuring = "Iout"

f = open(filename, 'w')
f.write("V1, {!s}\n".format(measuring))

s.set_voltage(1,0)
s.autorange(1)
s.set_voltage(2,0)
#s.set_vrange(2, 0)
s.autorange(2)

for val in v:
    s.set_voltage(1,0)
    s.autorange(1)
    s.set_voltage(2,val)
    s.autorange(2)
    f.write('{!s},{!s}\n'.format(val, s.get_current(2)))

s.set_current(1,0)
f.close()
