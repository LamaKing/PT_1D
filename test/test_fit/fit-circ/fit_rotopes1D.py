#!/usr/bin/env python3

import sys

import numpy as np
from scipy import interpolate


if __name__ == '__main__':
    data = np.loadtxt(sys.argv[1])

    mask = np.logical_and(data[:,0]*0.005>60, data[:,0]*0.005<90)
    x, y = data[mask,0]*0.005-60, -data[mask,16] # Torque
    #x, y = data[mask,0]*0.005-60, data[mask,6] # Energy

    x_smooth = np.zeros(2*len(x))
    y_smooth = np.zeros(2*len(x))
    x_smooth[len(x):] = 30+x
    x_smooth[:len(x)] = x
    y_smooth[:len(x)] = y
    y_smooth[len(x):] = -np.flip(y)
    #y_smooth[len(x):] = np.flip(y)

    tmp = np.hstack([[0], x_smooth])
    tmp = np.hstack([tmp, [60]])
    x_smooth = tmp.copy()

    tmp = np.hstack([y_smooth[0], y_smooth])
    tmp = np.hstack([tmp, y_smooth[-1]])

    y_smooth = tmp.copy()

    #interp_f = 'slinear'
    interp_f = 'linear'
    #interp_f = 'cubic'
    f = interpolate.interp1d(x_smooth, y_smooth, kind=interp_f)
    np.save('rotoPES_1D', f)
