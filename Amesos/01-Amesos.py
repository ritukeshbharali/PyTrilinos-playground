# 01-Amesos.py: demonstrates how the linear solver
# can be safely selected from the Amesos factory.
# All possible Amesos solver types are listed in
# stypes, however, depending on the Trilinos 
# configuration and installation, not all solvers
# are available.

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

# Loop over all possible types and check for availability
for itype in stypes:
    if factory.Query(itype) is True:
        print("Solver (%s) is supported" % (itype))