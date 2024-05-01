# 02-EpetraMaps.py: demonstrates how Epetra map is
# created. The map distributes the global elements
# among the different MPI ranks.

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
if rank == 0:
    globalElems.Size(3)
    globalElems[0]  = 0
    globalElems[1]  = 1
    globalElems[2]  = 2
elif rank == 1:
    globalElems.Size(3)
    globalElems[0]  = 2
    globalElems[1]  = 3
    globalElems[2]  = 4

# Create the Epetra map using globalElems vector
# Note that vector contains different values 
# depending on the MPI rank
EMap = Epetra.Map ( -1, globalElems, 0, comm )

# Print the Epetra map
print(EMap)