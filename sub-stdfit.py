import numpy as np
# Fitted function
# !!! NORMALISED and SINGLE PERIOD: we add U0 here and wrap according to spacing a
print("Fitted sin function")

Usfname = 'fit-std/en.npy'
print("Load energy from %s" % Usfname)
f1 = np.load(Usfname, allow_pickle=True).item()
def fen(x):
    return f1(x)

Fsfname = 'fit-std/F.npy'
print("Load force from %s" % Fsfname)
f2 = np.load(Fsfname, allow_pickle=True).item()
def ff(x):
    return f2(x)
