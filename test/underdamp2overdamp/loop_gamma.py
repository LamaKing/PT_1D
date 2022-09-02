#!/usr/bin/env python3
from driver import drive
import os, shutil, json
from os.path import join as pjoin
from time import time
import sys

import numpy as np


def gamma_loop(gamma0, gamma1, dgamma, params):
    """ Loop over values of damping gamma form gamma0 to gamma1 in steps dgamma

    If update_config is true, use the last position and velocity as starting point of the next step"""

    t0 = time() # Start the clock

    # Get force range from command line
    print("Start gamma0=%.4g end gamma1=%.4g stpe dgamma=%.4g (%i runs)" % (gamma0, gamma1, dgamma, 1+np.floor((gamma1-gamma0-1e-5)/dgamma)))
    pwd =  os.environ['PWD']
    print('Working in ', pwd)
    move_fname = ['out.dat']

    for gamma in np.arange(gamma0, gamma1, dgamma):

        print('--------- ON gamma=%15.8g -----------' % gamma)
        params['gamma'] = float(gamma)
        drive(params) # Run PT model

        # Organise run data in sub-folder
        cdir = 'GAMMA_%.4g' % gamma
        os.makedirs(cdir, exist_ok=True)
        # Move output files in run folder
        for cfname in move_fname:
            shutil.move(pjoin(pwd, cfname), pjoin(pwd, cdir, cfname))
        # Copy input in folder
        with open(pjoin(pwd, cdir, 'params.json'), 'w') as outj:
            json.dump(params, outj)
        print('-' * 80, '\n')

    t1=time()
    print('Done in %is (%.2fmin)' % (t1-t0, (t1-t0)/60))

if __name__ == "__main__":
    # Get
    gamma0, gamma1, dgamma = float(sys.argv[1]), float(sys.argv[2]), float(sys.argv[3])
    # Read params
    params_fname = 'params.json'
    if len(sys.argv) > 4: params_fname = sys.argv[4]
    with open(params_fname, 'r') as inj:
        params = json.load(inj)
    update_config = False
    gamma_loop(gamma0, gamma1, dgamma, params)
