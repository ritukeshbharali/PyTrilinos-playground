# 02-Amesos.py: demonstrates the use of direct sparse
# linear solver for the 1D bar problem defined in
# 05-EpetraFECrsMatrix.py. Additionally, we set dof 0
# to zero and dof 5 to 1. In this way, the bar is
# constrained on one end and pulled from the other
# end. The solution vector should be:
# [0,1,2] on rank 0, and [3,4,5] on rank 1.

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

# Print empty A (for debugging)
# print(A)

elemMat = Epetra.SerialDenseMatrix(2,2)
elemMat[0,0] =  1.0
elemMat[0,1] = -1.0
elemMat[1,0] = -1.0
elemMat[1,1] =  1.0

# Print the element matrix (for debugging)
#if rank == 0:
#    print('elemMat: {}'.format(elemMat))

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

# Create an Epetra Vector based on the non-overlapping
# Epetra map
B = Epetra.Vector(EMap)
B.PutScalar(0.0)

# Create an Epetra Vector based on the non-overlapping
# Epetra map
X = Epetra.Vector(EMap)
X.PutScalar(0.0)

# Create the dof constraints
if rank == 0:
    cdofs = [0]
    cvals = [0.0]
elif rank == 1:
    cdofs = [5]
    cvals = [5.0]

# Prepare some Epetra stuff
inds   = Epetra.IntSerialDenseVector(1)
vals   = Epetra.SerialDenseVector(1)

# Apply the constraints
for dof,val in zip(cdofs,cvals):

    # Fill in values
    vals[0] = val

    # Loop over the rows
    for irow in range(A.NumGlobalRows()):

        # Check whether this rank holds irow
        if A.MyGlobalRow(irow):

            # Extract column indices of the irow
            cols = A.ExtractGlobalRowCopy ( irow )

            # Fill in the column indices
            inds[0] = irow

            # Update the Epetra Vector B
            if irow == dof:
                B.ReplaceGlobalValues(inds,vals)
            else:
                # Check if dof column exists in irow
                if dof in cols[1]:
                    vals[0]  = -A[irow,dof] * val
                    B.SumIntoGlobalValues(vals,inds)
                    A[irow,dof] = 0.0

            # Set all column values in irow to zero
            cols[0][:] = 0.0
            A.ReplaceGlobalValues(dof,cols[0],cols[1])

            # Set the diagonal entry to one
            A[dof,dof] = 1.0

# Finalize matrix A
A.FillComplete()

# Create a linear problem
problem = Epetra.LinearProblem( A, X, B )

# Create an Amesos factory
factory = Amesos.Factory()

# We pick a solver type
stype = "Amesos_Lapack"

# Check whether the chosen solver is available in factory
if factory.Query(stype) == False:
    raise NotImplementedError("Selected solver (%s) not supported" % (stype))

# Create the solver for the linear problem
solver = factory.Create(stype, problem)

# Set up some solver parameters
params = {"PrintTiming" : False,
          "PrintStatus" : False }
solver.SetParameters(params)

# Perform the factorizations
solver.SymbolicFactorization()
solver.NumericFactorization()

# Solve the problem
ierr = solver.Solve()

# Print solution (Epetra Vector) X 
print('X = ',X, 'on rank: ', comm.MyPID())