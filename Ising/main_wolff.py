# coding=utf-8

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
    """Initialisiert ein 2D-grid mit latticeSize*latticeSize zufälligen Spins +-1, und setzt die Temperatur(0-100) auf temp. Diese Funktion muss als erste und insbesondere vor run(numberOfSteps) aufgerufen werden."""
    global SIZE, TEMP, system
    SIZE=latticeSize
    sys.setrecursionlimit(SIZE*SIZE*SIZE)
    if not (0 < temp < 100):
        sys.exit("Temperature should be greater than 0 and less than 100")
    else:
        TEMP=float(temp)
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
    
    if (not cluster[Nprev, M]) and system[Nprev, M] == D and (1 - np.exp(-2*J/TEMP)) < np.random.rand():
        growCluster(Nprev,M,D)
    if (not cluster[Nnext, M]) and system[Nnext, M] == D and (1 - np.exp(-2*J/TEMP)) < np.random.rand():
        growCluster(Nnext,M,D)
    if (not cluster[N, Mprev]) and system[N, Mprev] == D and (1 - np.exp(-2*J/TEMP)) < np.random.rand():
        growCluster(N,Mprev,D)
    if (not cluster[N, Mnext]) and system[N, Mnext] == D and (1 - np.exp(-2*J/TEMP)) < np.random.rand():
        growCluster(N,Mnext,D)

# alternative implementierung(von https://statmechalgcomp.wikispaces.com/Spin+systems+Enumeration+Cluster) mit schleife statt rekursion, ist genauso langsam
def oneClusterStep2():
    N = np.random.randint(0,SIZE)
    M = np.random.randint(0,SIZE)
    cluster = [(N,M)]
    unchecked_cluster_sites = [(N,M)]
    while unchecked_cluster_sites != []:
        random_site=unchecked_cluster_sites[0]
        for nb in [((random_site[0]+1) % SIZE,random_site[1]),((random_site[0]-1) % SIZE,random_site[1]),(random_site[0],(random_site[1]+1) % SIZE),(random_site[0],(random_site[1]-1) % SIZE)]:
            if(system[nb]==system[N,M] and nb not in cluster and (1 - np.exp(-2*J/TEMP)) > np.random.rand()):
                cluster.append(nb)
                unchecked_cluster_sites.append(nb)
        unchecked_cluster_sites.remove(random_site)
    for site in cluster:
        system[site]*=-1
        delta.append(site)

def getSystemAtStep(step):
    """Gibt den Zustand des Modells nach step vielen Schritten (flips) aus.
    Der Zustand ist eine +-1 Matrix der Gräße latticeSize*latticeSize. Beispiel:
    
    [[-1 1 -1]
    [1 1 -1]
    [-1 -1 -1]]
    
    Die Funktion ist momentan naiv implementiert und sehr langsam."""
    
    if(initial_system==[]):
        sys.exit("Grid wurde noch nicht initialisiert. init(latticeSize, temp) muss zuerst aufgerufen werden.");
    if(step > len(delta)):
        sys.exit("getSystemAtStep(" +repr(step) +") kann nicht ausgeführt werden, da erst " +repr(len(delta)) +" Schritte berechnet wurden.");
        
    sysState=deepcopy(initial_system)
    if(step > 0):
        for i in range(step-1):
            if delta[i][0] != -1:
                sysState[delta[i][0],delta[i][1]] *= -1
    return sysState

def plotSys():
    return system

def run(numberOfSteps): # The Main monte carlo loop 
    """Führt numberOfSteps viele Schritte aus, d.h. numberOfSteps viele rekursive growcluster(). Das bedeutet, dass die Gesamtzahl der Schritt im allgemeinen größer ist."""
    if(SIZE == NULL):
        sys.exit("Grid wurde noch nicht initialisiert. init(latticeSize, temp) muss zuerst aufgerufen werden.");
    while len(delta) < numberOfSteps:
        #print "One Cluster Step" #Debug
        #print cluster #Debug
        build_cluster()
        oneClusterStep()