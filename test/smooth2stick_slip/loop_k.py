#!/usr/bin/env python3
from driver import drive
import os, shutil, json
from os.path import join as pjoin
from time import time
import sys

import numpy as np

def handle_run(params, c_key, c_val):
    params[c_key] = c_val
    pwd =  os.environ['PWD']
    print('Working in ', pwd)

    # Run PT model
    drive(params)

    # Organise run data in sub-folder
    cdir = '%s_%.4g' % (c_key, c_val)
    os.makedirs(cdir, exist_ok=True)
    # Move output files in run folder
    move_fname = ['out.dat']
    for cfname in move_fname:
        shutil.move(pjoin(pwd, cfname), pjoin(pwd, cdir, cfname))
    # Copy input in folder
    with open(pjoin(pwd, cdir, 'params.json'), 'w') as outj:
        json.dump(params, outj)

def k_loop(k0, k1, dk, params):
    """ Loop over values of spring constant K form k0 to k1 in steps dk

    If update_config is true, use the last position and velocity as starting point of the next step"""

    t0 = time() # Start the clock

    # Get force range from command line
    print("Start k0=%.4g end k1=%.4g stpe dk=%.4g (%i runs)" % (k0, k1, dk, 1+np.floor((k1-k0)/dk)))
    pwd =  os.environ['PWD']
    print('Working in ', pwd)
    move_fname = ['out.dat']

    for k in np.arange(k0, k1, dk):
        print('--------- ON K=%15.8g -----------' % k)
        handle_run(params, 'K', float(k)) # for json cannot be numpy
        print('-' * 80, '\n')

    t1=time()
    print('Done in %is (%.2fmin)' % (t1-t0, (t1-t0)/60))

if __name__ == "__main__":
    # Get
    k0, k1, dk = float(sys.argv[1]), float(sys.argv[2]), float(sys.argv[3])
    # Read params
    params_fname = 'params.json'
    if len(sys.argv) > 4: params_fname = sys.argv[4]
    with open(params_fname, 'r') as inj:
        params = json.load(inj)
    update_config = False
    k_loop(k0, k1, dk, params)
