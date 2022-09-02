import numpy as np
import matplotlib.pyplot as plt


lss = ['-', '--', '-.'] * 100

v = 0.01
fig, (axp, axen, axF) = plt.subplots(3,1, sharex=True)
#fig.suptitle("K=%6.3g" % k)
for i, k in enumerate([0.1, 0.3, 0.5, 0.7, 0.9, 1.1, 1.3, 2, 7, 12, 17]):

    dat = np.loadtxt("K_%s/out.dat"%k)
    axp.set_ylabel(r'tip pos $x$')
    axp.plot(dat[:,0]*v, dat[:,5], label='K=%6.3g' % k, ls=lss[i])
    #axp.plot(dat[:,0]*v, dat[:,5])

    axen.set_ylabel('En tot')
    axen.plot(dat[:,0]*v, dat[:,1]+dat[:,2], ls=lss[i])

    axF.set_ylabel('Friction')
    axF.plot(dat[:,0]*v, k*(v*dat[:,0]-dat[:,5]), ls=lss[i])
    axF.set_xlabel(r'$vt$')

axp.legend(ncol=4)
plt.tight_layout()
plt.show()
