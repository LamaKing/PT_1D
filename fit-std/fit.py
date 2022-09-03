#!/usr/bin/env python3

import sys

import numpy as np
from numpy import pi
from scipy import interpolate


if __name__ == '__main__':
    data = np.loadtxt(sys.argv[1])

    mask = np.logical_and(data[:,0]>-0.5, data[:,0]<2*pi+0.5)
    x, y = data[mask,0], data[mask,2] # force
    #x, y = data[mask,0], data[mask,1] # energy

    #x_smooth = np.zeros(2*len(x))
    #y_smooth = np.zeros(2*len(x))
    #x_smooth[len(x):] = 30+x
    #x_smooth[:len(x)] = x
    #y_smooth[:len(x)] = y
    #y_smooth[len(x):] = -np.flip(y)


    x_smooth = x
    y_smooth = y

    #tmp = np.hstack([[0], x_smooth])
    #tmp = np.hstack([tmp, [60]])
    #x_smooth = tmpb
    #tmp = np.hstack([y_smooth[0], y_smooth])
    #tmp = np.hstack([tmp, y_smooth[-1]])
    #
    #y_smooth = tmp.copy()

    #interp_f = 'slinear'
    interp_f = 'linear'
    #interp_f = 'cubic'
    f = interpolate.interp1d(x_smooth, y_smooth, kind=interp_f)
    np.save('rotoPES_1D', f)
