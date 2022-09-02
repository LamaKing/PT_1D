# Prandtl-Tomlinson model

Simple python implementation of the 1D Prandtl-Tomlinson model.
To see details of the model and references used for testing see:
- Analytical expressions for the kinetic friction in the Prandtl-Tomlinson model Enrico Gnecco, Raphael Roth, and Alexis Baratoff Phys. Rev. B 86, 035443 (2012)
- Velocity dependence of kinetic friction in the Prandtl-Tomlinson model Martin H. Müser Phys. Rev. B 84, 125419 (2011)
- Popov, V.L. (2010). The Prandtl-Tomlinson Model for Dry Friction. In: Contact Mechanics and Friction. Springer, Berlin, Heidelberg.

The substrate potential is imported from a module, specified in the driver. The module must contain a function fen(x) and ff(x) returning the energy and force at the required position. The amplitude U0 and the periodicity a are enforced in the driver.py code.

To run the standard -cos(x) model, use sub-std.py module.

An interesting feature of the code is to run the model on an arbitrary substrate potential by simply changing the module. E.g. you could fit with numpy the -cos potential and the relative force and run the model on the interpolated PES.
With this approach one can evaluated the minimum energy path in an arbitrary 2D crystalline interface, fit an analytical function to it (and its force) and run the 1D PT model on it.
