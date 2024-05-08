# 01-AztecOO.py: demonstrates how a direct linear solver 
# is used. The matrix from 05-EpetraFECrsMatrix.py is used,
# and the lhs (X) and rhs (B) vectors are defined using the
# same map. 

# Import Epetra and Amesos modules from PyTrilinos
from PyTrilinos import Epetra, Amesos

import numpy as np

# Setup the communicator
comm = Epetra.PyComm()

# Get the rank of this process
rank = comm.MyPID()

# Create a Epetra Int Vector that stores global
# elements owned by each rank
globalElems = Epetra.IntSerialDenseVector()

# Rank zero and one sets up owned global elements
# (non-overlapping map)
if rank == 0:
    globalElems.Size(3)
    globalElems[0]  = 0
    globalElems[1]  = 1
    globalElems[2]  = 2
elif rank == 1:
    globalElems.Size(3)
    globalElems[0]  = 3
    globalElems[1]  = 4
    globalElems[2]  = 5

# Create the Epetra map using globalElems vector
# Note that vector contains different values 
# depending on the MPI rank
EMap = Epetra.Map ( -1, globalElems, 0, comm )

# Create an Epetra FECrsMatrix based on the 
# non-overlapping Epetra map
A = Epetra.FECrsMatrix(Epetra.Copy,EMap,1)

# Print empty A
# print(A)

elemMat = Epetra.SerialDenseMatrix(2,2)
elemMat[0,0] =  1.0
elemMat[0,1] = -1.0
elemMat[1,0] = -1.0
elemMat[1,1] =  1.0

# Print the element matrix
if rank == 0:
    print('elemMat: {}'.format(elemMat))

# Element partitioning
if rank == 0:
    elems = np.array([0,1,2])
    nodes = np.array([[0,1],[1,2],[2,3]])
elif rank == 1:
    elems = np.array([3,4])
    nodes = np.array([[3,4],[4,5]])

# Assemble the matrix
for ielem in range(len(elems)):
    dofs    = nodes[ielem]
    indices = Epetra.IntSerialDenseVector(2)
    values  = Epetra.SerialDenseVector(2)

    indices[:] = dofs[:]

    for idof in range(len(dofs)):
        values[:] = elemMat[idof][:]
        A.InsertGlobalValues(dofs[idof], 2,
                             values, indices)

# Modify the matrix to make it non-singular
A[0,1] = 0.0

# Synchronize
A.GlobalAssemble()
A.FillComplete()

# Create an Epetra Vector based on the non-overlapping
# Epetra map
B = Epetra.Vector(EMap)
B.Random()

# Create an Epetra Vector based on the non-overlapping
# Epetra map
X = Epetra.Vector(EMap)
X.PutScalar(0.0)

print(B)
print(X)

problem = Epetra.LinearProblem( A, X, B )
factory = Amesos.Factory()

# Creates the solver using the Amesos' factory
stype = "Amesos_Lapack"
if factory.Query(stype) == False:
    raise NotImplementedError("Selected solver (%s) not supported" % (stype))
solver = factory.Create(stype, problem)

# Setting parameters using a Python dictionary. The list of supported
# parameters can be found on the user's guide.
amesosList = {"PrintTiming" : True,
              "PrintStatus" : True
             }
solver.SetParameters(amesosList)

# Note: we don't check here the return parameters for brevity. 
solver.SymbolicFactorization()
solver.NumericFactorization()
ierr = solver.Solve()

print(X)