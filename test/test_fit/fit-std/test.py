#!/usr/bin/env python3

import sys

import numpy as np
from numpy import pi
import matplotlib.pyplot as plt

if __name__ == '__main__':
    data = np.loadtxt(sys.argv[1])


    f = np.load('rotoPES_1D.npy', allow_pickle=True).item()

    a = 2*pi
    def f_wrap(x):
        return f(x%a)

    plt.plot(data[:,0], data[:,1], '.', label='reference') # energy
    plt.ylabel(r'en')
    #plt.plot(data[:,0], data[:,2], '.', label='reference') # force
    #plt.ylabel(r'F')

    xx = np.linspace(-4*pi, 4*pi, 20000)

    plt.plot(xx, f_wrap(xx), '-', label='analytical linear fit')
    plt.plot(xx, f_wrap(xx), ',', label='analytical linear fit', zorder=10)
    plt.xlim(xx[0], xx[-1])
    plt.legend()
    plt.xlabel(r'$x$')

    plt.tight_layout()
    plt.show()
