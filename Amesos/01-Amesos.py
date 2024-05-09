# 01-AztecOO.py: 

# Import Amesos modules from PyTrilinos
from PyTrilinos import Amesos

# Amesos solver factory
factory = Amesos.Factory()

# Creates the solver using the Amesos' factory
stypes    = []
stypes.append("Amesos_Lapack")
stypes.append("Amesos_Scalapack")
stypes.append("Amesos_Klu")
stypes.append("Amesos_Umfpack")
stypes.append("Amesos_Pardiso")
stypes.append("Amesos_Taucs")
stypes.append("Amesos_Superlu")
stypes.append("Amesos_Superludist")
stypes.append("Amesos_Dscpack")
stypes.append("Amesos_Mumps")

for itype in stypes:
    if factory.Query(itype) is True:
        print("Solver (%s) is supported" % (itype))