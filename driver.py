#!/usr/bin/env python3
import json, sys, importlib
from time import time
import numpy as np
from numpy import pi, sqrt, cos, sin
# Custom fix-step ODE integrator (Langeving compatible) from scipy
from RK45_lang import RK45_lang
# Module implementing the equation of motion
from PT_1D import derivs, sub_en, spring_en

def drive(params):

    # Start the clock
    t0 = time()

    # Read parameters
    print('-'*10, "Params file", '-'*5)
    for k, v in params.items():
        print("%20s :" % k, v)
    print('-'*(10+1+len("Params file")+1+5))
    name = '' # Not usually needed, use folders
    if 'name' in params.keys(): name = params['name']

    # Init system
    x0, v0, tip0 = 0, 0, 0
    if 'x0' in params.keys(): x0 = params['x0']
    if 'v0' in params.keys(): v0 = params['v0']
    if 'tip0' in params.keys(): tip0 = params['tip0']
    xvec, vvec, mvec = x0*np.ones(1), v0*np.ones(1), params['m']*np.ones(1)
    Np = len(xvec)
    # MD integration params
    dt = params['dt'] # time-step
    nstep = params['nstep'] # length of simulation
    nskip = params['nskip'] # print every

    # Spring potential
    v_dummy, K = params['v_dummy'], params['K']

    # Substrate potential
    a, U0 = params['a'], params['U0']
    if 'submod_fname' in params.keys():
        # --- Fitted function ---
        # !!! NORMALISED and SINGLE PERIOD: we add U0 here and wrap according to spacing a
        #submod_fname = 'sub-stdfit'
        #submod_fname = 'sub-circfit'
        submod_fname = params['submod_fname']
        print("Fitted function from", submod_fname)
        submod = importlib.import_module(submod_fname)
        fen, ff = submod.fen, submod.ff
        def Us(x):
            return U0*fen(x%a)
        def Fs(x):
            return U0*(ff(x%a))
    else:
        # --- Analytic function ---
        print("Analytic function of standard PT")
        def Us(x):
            return -U0*np.cos(2*pi*x/a)
        def Fs(x):
            return -2*pi*U0/a*np.sin(2*pi*x/a)

    # Langevin thermostat
    gamma, T = params['gamma'], params['T'] # [gamma]=???, [T]=energy
    corr = np.sqrt(4/3.) # 1 # !!! AMPLITUDE CORRECTION. Without this the temperature is wrong... scipy RK45 requires 3/4 dt?
    brand = corr*np.sqrt(2*T*gamma/dt)

    # Parameters for the PT module
    dparams = {'v_dummy': v_dummy, 'K': K, 'tip0': tip0,
               'Fs': Fs, 'Us': Us,
               'gamma': gamma, 'brand': brand
               }

    # Setup the equation array, combine position and velocity
    eqvec = np.concatenate((xvec, vvec))  # First half is position second half is velocity
    neq = len(eqvec)
    neq2 = int(neq/2) # useful shortcut for division between pos and velox

    # ------------------- PRINT SYSTEM INFO -------------------- #
    header = ' SYSTEM INFO '
    eta = ((2*pi)**2*U0)/(K*a**2) # Smooth sliding or stick-slip?
    print('-'*20 + header + '-'*20)
    print('Tip moving to v*t_end=%.4g (%.4g periodes)' % (dt*nstep*v_dummy, (dt*nstep*v_dummy)/a))
    print('Standard PT eta=%6.3g. ' % eta, "Sliding is %s" % ('smooth' if eta<1 else 'stick-slip'))
    print('Damping gamma=%6.3g. ' % gamma, "Dynamics is %s-damped?" % ('over' if gamma>=1 else 'under'))
    print('-'*20 + '-'*len(header) + '-'*20)
    # ---------------------------------------------------------- #

    #-------- OUTPUT SETUP -----------
    outfname = 'out%s.dat' % name
    outstream = open(outfname, 'w')

    # !! Labels and print_status data structures must be coherent !!
    num_space, indlab_space= 30, 2  # Width printed numerical values and Header index width
    lab_space = num_space-indlab_space-1 # Match width of printed number, including parenthesis
    header_labels = ['sub_en', 'spring_en', 'ekin', 'kBT', 'pos_cm[0]', 'Vcm[0]']
    # Gnuplot-compatible (leading #) fix-width output file
    first = '#{i:0{ni}d}){s: <{n}}'.format(i=0, s='t', ni=indlab_space, n=lab_space-1,c=' ')
    print(first+"".join(['{i:0{ni}d}){s: <{n}}'.format(i=il+1, s=lab, ni=indlab_space, n=lab_space,c=' ')
                         for il, lab in zip(range(len(header_labels)), header_labels)]), file=outstream)
    # Inner-scope shortcut for printing
    def print_status(data):
        print("".join(['{n:<{nn}.16g}'.format(n=val, nn=num_space) for val in data]), file=outstream)
    # Update status string
    status_str = "%8i) t=%12.4g (%6.2f%%) xcm=%20.10g (%8.2g) vcm=%20.10g kBT=%20.10g etot=%30.16g"

    #----------------- MD --------------------
    #### INIT
    t, tf = 0, dt*nstep
    it = 0
    # Solve equations with RK45 FIX STEP for Langevin. See module here and SciPy.
    # Wrap parameters (should not change from now on...) for the solver
    fun = lambda t, y: derivs(t, y, dparams)
    solver = RK45_lang(fun, t, eqvec, tf)
    solver.set_step(dt) # Set FIXED time step of intergration
    solver.set_nskip(nskip) # Set number of step done inside the function, not printed

    # Save FIRST STEP
    c_sub_en, c_spring_en, c_ekin = np.sum(sub_en(t, xvec, dparams)), np.sum(spring_en(t, xvec, dparams)), np.sum(1/2*vvec**2)
    c_kBT = 2*c_ekin/Np
    xcm, vcm = np.average(xvec), np.average(vvec)
    print(status_str % (it, t, t/tf*100, xcm, xcm/2/pi, vcm , c_kBT, c_sub_en+c_spring_en+c_ekin))
    print_status([t, c_sub_en, c_spring_en, c_ekin, c_kBT, xcm, vcm])

    ##### TIME LOOP --------------------------
    while t<tf:
        solver.step() # Advance one step
        eqvec = solver.y # get updated solution
        t = solver.t # set new time in solver

        # Save step
        xvec, vvec = eqvec[:neq2], eqvec[neq2:]
        c_sub_en, c_spring_en, c_ekin = np.sum(sub_en(t, xvec, dparams)), np.sum(spring_en(t, xvec, dparams)), np.sum(1/2*vvec**2)
        c_kBT = 2*c_ekin/Np
        xcm, vcm = np.average(xvec), np.average(vvec)
        print_status([t, c_sub_en, c_spring_en, c_ekin, c_kBT, xcm, vcm])

        # Print status update
        if it % int(nstep/nskip/10+1) == 0:
            print(status_str % (it, t, t/tf*100, xcm, xcm/2/pi, vcm , c_kBT, c_sub_en+c_spring_en+c_ekin))
        it+=1
    ##### ------------------------------------

    # Save LAST STEP
    xvec, vvec = eqvec[:neq2], eqvec[neq2:]
    c_sub_en, c_spring_en, c_ekin = np.sum(sub_en(t, xvec, dparams)), np.sum(spring_en(t, xvec, dparams)), np.sum(1/2*vvec**2)
    c_kBT = 2*c_ekin/Np
    xcm, vcm = np.average(xvec), np.average(vvec)
    print(status_str % (it, t, t/tf*100, xcm, xcm/2/pi, vcm , c_kBT, c_sub_en+c_spring_en+c_ekin))
    print_status([t, c_sub_en, c_spring_en, c_ekin, c_kBT, xcm, vcm])

    # DONE
    print("Finished after %i solver calls." % solver.ncalls,  "Solver status:", solver.status)
    t1=time()
    print('Done in %is (%.2fmin).' % (t1-t0, (t1-t0)/60))

    return 0

if __name__ == "__main__":
    # Read params
    params_fname = sys.argv[1]
    with open(params_fname, 'r') as inj: params = json.load(inj)
    drive(params)
