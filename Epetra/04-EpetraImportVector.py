# 04-EpetraImportVector.py: demonstrates how Epetra
# distributed Vector is imported using arbitrary 
# Epetra maps. 03-EpetraDistVector.py contains an
# Epetra map (EMap) and a Vector X. A new Epetra
# (target) map (TMap) is created and values from X
# are imported into a new Vector Y using the
# Epetra.Import functionality.

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

# Create a Epetra Int Vector that stores global
# elements required on each rank
globalTargetElems = Epetra.IntSerialDenseVector()

# Rank zero and one sets up owned global elements
# (non-overlapping map)
if rank == 0:
    globalTargetElems.Size(4)
    globalTargetElems[0]  = 0
    globalTargetElems[1]  = 1
    globalTargetElems[2]  = 2
    globalTargetElems[3]  = 4
elif rank == 1:
    globalTargetElems.Size(3)
    globalTargetElems[0]  = 5
    globalTargetElems[1]  = 1
    globalTargetElems[2]  = 3

# Create the Epetra map using globalTargetElems vector
ETargetMap = Epetra.Map ( -1, globalTargetElems, 0, comm )

# Create an Epetra Vector based on the Epetra target map
Y = Epetra.Vector(ETargetMap)

# Create an Importer
Importer = Epetra.Import(ETargetMap,EMap)

# Import values from X to Y
Y.Import(X, Importer, Epetra.Insert)

# Print the Epetra Vector Y
print(Y)