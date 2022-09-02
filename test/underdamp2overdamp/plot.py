import numpy as np
import matplotlib.pyplot as plt


lss = ['-', '--', '-.'] * 100

v, k = 0.01, 0.5
fig, (axp, axen, axF) = plt.subplots(3,1, sharex=True)

for i, gamma in enumerate([0.1, 0.3, 0.5, 1.1, 1.9]):

    dat = np.loadtxt("GAMMA_%s/out.dat"%gamma)
    axp.set_ylabel(r'tip pos $x$')
    axp.plot(dat[:,0]*v, dat[:,5], label=r'$\gamma$=%6.3g' % gamma, ls=lss[i])

    axen.set_ylabel('En tot')
    axen.plot(dat[:,0]*v, dat[:,1]+dat[:,2], ls=lss[i])

    axF.set_ylabel('Friction')
    axF.plot(dat[:,0]*v, k*(v*dat[:,0]-dat[:,5]), ls=lss[i])
    axF.set_xlabel(r'$vt$')

axp.legend(ncol=4)
plt.tight_layout()
plt.show()

fig, (axp, axen, axF) = plt.subplots(3,1, sharex=True)
for i, gamma in enumerate([0.05, 1.9]):

    dat = np.loadtxt("GAMMA_%s/out.dat"%gamma)
    axp.set_ylabel(r'tip pos $x$')
    axp.plot(dat[:,0]*v, dat[:,5], label=r'$\gamma$=%6.3g' % gamma, ls=lss[i])

    axen.set_ylabel('En tot')
    axen.plot(dat[:,0]*v, dat[:,1]+dat[:,2], ls=lss[i])

    axF.set_ylabel('Friction')
    axF.plot(dat[:,0]*v, k*(v*dat[:,0]-dat[:,5]), ls=lss[i])
    axF.set_xlabel(r'$vt$')

axp.legend(ncol=4)
plt.tight_layout()
plt.show()
