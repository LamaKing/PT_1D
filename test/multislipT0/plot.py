import numpy as np
import matplotlib.pyplot as plt
from numpy import pi

lss = ['-', '--', '-.'] * 100

v = 0.01
fig, (axp, axen, axF) = plt.subplots(3,1, sharex=True)
for i, k in enumerate([0.03, 0.05, 0.1, 0.5]):

    dat = np.loadtxt("K_%s/out.dat"%k)
    axp.set_ylabel(r'tip pos $x$')
    axp.plot(dat[:,0]*v, dat[:,5]/(2*pi), label='K=%6.3g' % k, ls=lss[i])
    axp.hlines([1,2,3,4], *axp.get_xlim(), ls=':', color='gray', lw=0.5)
    #axp.plot(dat[:,0]*v, dat[:,5])

    axen.set_ylabel('En tot')
    axen.plot(dat[:,0]*v, dat[:,1]+dat[:,2], ls=lss[i])

    axF.set_ylabel('Friction')
    axF.plot(dat[:,0]*v, k*(v*dat[:,0]-dat[:,5]), ls=lss[i])
    axF.set_xlabel(r'$vt$')

axp.legend(ncol=4)
plt.tight_layout()
plt.show()
