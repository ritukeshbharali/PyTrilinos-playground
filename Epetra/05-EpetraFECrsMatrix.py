# 05-EpetraFECrsMatrix.py: demonstrates how Epetra
# distributed FECrs Matrix is used. Non-overlapping
# Epetra maps from 03-EpetraDistVector.py is adopted
# for initializing the matrix. Compared to the Epetra
# Crs Matrix, the FE Crs Matrix allows filling the
# matrix rows components from process that does not
# own the rows.

# Say, we have a 1D elastic bar problem (1 dof per node)
#           
# 0-----1-----2-----3-----4-----5 (nodes/dofs)
#   [0]   [1]   [2]   [3]   [4]   (elems)
#
# Proc 0 handles elems 0,1,2, owns nodes/dofs 0,1,2
# Proc 1 handles elems 3,4,   owns nodes/dofs 3,4
#
# Element matrix looks like [1 -1]
#                           [-1 1]
#
# So when element [2] matrix is assembled into the
# global matrix A from proc 0, the communications
# are handled behind-the-scenes with a call to 
# 'GlobalAssemble'. This is the convenient feature
# of Epetra FECrsMatrix from a finite element
# method perspective.

# Import Epetra module from PyTrilinos
from PyTrilinos import Epetra

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
# Synchronize
A.GlobalAssemble()
A.FillComplete()

print(A)