#!/usr/bin/env python3
# coding=utf-8
import csv
import sys
import numpy as np
import matplotlib.pyplot as plt

xs, ys = [], []
with open(sys.argv[1]) as f:
    c = csv.reader(f, delimiter=",")
    next(c) # Throw away the header
    for row in c:
      xs += [float(row[0])]
      ys += [float(row[1])] 


plt.plot(xs, ys, '.')
plt.show()
