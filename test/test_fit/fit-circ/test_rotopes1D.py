#!/usr/bin/env python3

import sys

import numpy as np
from scipy import interpolate
import matplotlib.pyplot as plt

if __name__ == '__main__':
    data = np.loadtxt(sys.argv[1])


    f = np.load('rotoPES_1D.npy', allow_pickle=True).item()

    def f_wrap(x):
        return f(x % 60)

    plt.plot(data[:,0]*0.005, -data[:,16], '.', label='rigid LAMMPS')
    #plt.plot(data[:,0]*0.005, data[:,6], '.', label='rigid LAMMPS')

    #xx = np.linspace(-370, 130, 30000)
    xx = np.linspace(-61, 121, 20000)
    plt.plot(xx, f_wrap(xx), '-', label='analytical linear fit')
    plt.plot(xx, f_wrap(xx), ',', label='analytical linear fit', zorder=10)
    plt.xlim(xx[0], xx[-1])
    plt.legend()
    plt.xlabel(r'$\theta$ [degree]')
    plt.ylabel(r'torque')
    plt.tight_layout()
    plt.show()
