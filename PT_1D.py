import numpy as np
from numpy import pi
from numpy.random import normal

global t_eps
t_eps = 1 # Set to 0: turn off the substrate potential for debug purposes

def derivs(t, y, params): # here is all the physics: the left side of the equation

    Fs = params['Fs'] # Substrate force function of form f(x), x position of tip
    v_dummy, K, tip0 = params['v_dummy'], params['K'], params['tip0'] # Moving stage
    gamma, brand = params['gamma'], params['brand'] # Thermostat

    # Initialise arrays
    neq = len(y) # = Number of equations
    neq2 = int(neq/2) # = Number of particles
    deriv = np.zeros(neq)  # the accelleration array
    noise = normal(0, 1, size=neq2) # Gaussian numbers

    #### POSITIONS DOT #####
    for i in range(neq2):  # the second half of y is velocities
        deriv[i] = y[i+neq2] # this enables the mapping of Newton to 1st order

    #### VELOCITIES DOT ####
    #------- Chain bulk
    for i in range(0, neq2):
        deriv[i+neq2] =  t_eps*Fs(y[i]) - K*(y[i]-(v_dummy*t+tip0)) - gamma*y[i+neq2] + brand*noise[i]
    return deriv

def sub_en(t, y, params):
    Us = params['Us'] # Substrate force function of form f(x), x position of tip
    return np.sum(t_eps*Us(y))

def spring_en(t, y, params):
    v_dummy, K = params['v_dummy'], params['K']
    return np.sum(K/2*(y-v_dummy*t)**2)
