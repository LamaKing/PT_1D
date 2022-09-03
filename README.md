# Prandtl-Tomlinson model

Simple python implementation of the 1D Prandtl-Tomlinson model.
This model is used to rationalise dry friction model and mechanical instabilities (https://en.wikipedia.org/wiki/Tomlinson_model).

To see details of the model and references used for testing see:
- Analytical expressions for the kinetic friction in the Prandtl-Tomlinson model Enrico Gnecco, Raphael Roth, and Alexis Baratoff Phys. Rev. B 86, 035443 (2012)
- Velocity dependence of kinetic friction in the Prandtl-Tomlinson model Martin H. Müser Phys. Rev. B 84, 125419 (2011)
- Popov, V.L. (2010). The Prandtl-Tomlinson Model for Dry Friction. In: Contact Mechanics and Friction. Springer, Berlin, Heidelberg.

To use the standard PT sinusoidal substrate potential with $2\pi$ period, leave out "submod_fname" from the parameters file.

Otherwise, the substrate potential is imported from a module, specified in the driver. The module must contain a function fen(x) and ff(x) returning the energy and force at the required position over a single period. The amplitude $U_0$ and the periodicity a are enforced in the driver.py code.
To test this feature, a numerical fitted version of the standard PT substrate is found in "sub-stdfit". The functions are interpolated over the datapoint in "fit-std".
With this approach one can evaluated the minimum energy path in an arbitrary 2D crystalline interface, fit an analytical function to it (and its force) and run the 1D PT model on it.
