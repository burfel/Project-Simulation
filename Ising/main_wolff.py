import numpy as np
from boto.dynamodb.condition import NULL
from copy import deepcopy
import sys

J = 1. #Ferromagnetic Coupling
SIZE = NULL
STEPS = NULL
TEMP = NULL
system = []
initial_system = []
delta = []
cluster = []

def init(latticeSize, temp):
    global SIZE, TEMP, system
    SIZE=latticeSize
    sys.setrecursionlimit(SIZE*SIZE*SIZE)
    TEMP=float(temp)
    if not (0 < temp < 100): #if(TEMP <= 0 or TEMP > 100) ~error?
        sys.exit("Temperature should be greater than 0 and less than 100")
    build_system()
    build_cluster()

def bc(i): # Check periodic boundary conditions 
    if i+1 > SIZE-1:
        return 0
    if i-1 < 0:
        return SIZE-1
    else:
        return i
      
def build_system(): # Build the system with random values of -1,1
    global system, initial_system
    initial_system=np.random.random_integers(0,1,(SIZE,SIZE))*2 - 1
    system=deepcopy(initial_system)    
    
def build_cluster():
    global cluster
    cluster=np.zeros((SIZE,SIZE), dtype=bool)

def oneClusterStep():
    N = np.random.randint(0,SIZE)
    M = np.random.randint(0,SIZE)
    D = system[N,M]
    growCluster(N,M,D)
    
def growCluster(N,M,D):
    cluster[N,M] = 1
    system[N,M] = -D
    #print "Grow Cluster" #Debug
    
    delta.append([N,M])
    #print "Print Delta" #Debug
    #print delta #Debug
    
    Nprev = bc(N-1)
    Nnext = bc(N+1)
    Mprev = bc(M-1)
    Mnext = bc(M+1)
    
    if (not cluster[Nprev, M]) and system[Nprev, M] == D and (1 - np.exp(-2*J/TEMP)) > np.random.rand():
        growCluster(Nprev,M,D)
    if (not cluster[Nnext, M]) and system[Nnext, M] == D and (1 - np.exp(-2*J/TEMP)) > np.random.rand():
        growCluster(Nnext,M,D)
    if (not cluster[N, Mprev]) and system[N, Mprev] == D and (1 - np.exp(-2*J/TEMP)) > np.random.rand():
        growCluster(N,Mprev,D)
    if (not cluster[N, Mnext]) and system[N, Mnext] == D and (1 - np.exp(-2*J/TEMP)) > np.random.rand():
        growCluster(N,Mnext,D)

def tryAdd(N,M,D):
    if system[N,M] == D:
        if (1 - np.exp(-2*J/TEMP)) > np.random.rand():
            #print "Add success" #Debug
            growCluster(N,M,D)

def energy(N, M): # Calculate internal energy
    return -J * system[N,M] * (system[bc(N-1), M] + system[bc(N+1), M] + system[N, bc(M-1)] + system[N, bc(M+1)])

def getSystemAtStep(step):
    sys=deepcopy(initial_system)
    if(step > 0):
        for i in range(step-1):
            if delta[i][0] != -1:
                sys[delta[i][0],delta[i][1]] *= -1
    return sys

def plotSys():
    return system

def run(numberOfSteps): # The Main monte carlo loop 
    while len(delta) < numberOfSteps:
        #print "One Cluster Step" #Debug
        #print cluster #Debug
        build_cluster()
        oneClusterStep()     