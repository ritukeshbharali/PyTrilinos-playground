# 03-EpetraDistVector.py: demonstrates how Epetra
# distributed Vector is created. The Epetra map
# from 02-EpetraMaps.py is modified to create a
# non-overlapping map (i.e., elements of vector
# are uniquely assigned to MPi ranks). Thereafter,
# an Epetra Vector is defined using the Epetra map,
# and then random values are assigned and printed
# to the terminal.

# Import Epetra module from PyTrilinos
from PyTrilinos import Epetra

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

# Create an Epetra Vector based on the non-overlapping
# Epetra map
X = Epetra.Vector(EMap)

# Assign some random values
X.Random()

# Print the Epetra Vector X
print(X)