# Import Epetra module from PyTrilinos
from PyTrilinos import Epetra

# Setup the communicator
comm = Epetra.PyComm()

# Get the rank of this process
rank = comm.MyPID()

# Print a message on root process
iAmRoot = rank == 0
if iAmRoot:
	print('I am the root process {}'.format(rank))