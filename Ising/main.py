# coding=utf-8

import time
import numpy as np
from boto.dynamodb.condition import NULL
from copy import deepcopy
import sys

SIZE = NULL
STEPS = NULL
TEMP = NULL
system = []
initial_system = []
delta = []

def init(latticeSize, temp):
    """Initialisiert ein 2D-grid mit latticeSize*latticeSize zufälligen Spins +-1, und setzt die Temperatur(0-100) auf temp. Diese Funktion muss als erste und insbesondere vor run(numberOfSteps) aufgerufen werden."""
    global SIZE, TEMP, system
    SIZE=latticeSize
    TEMP=float(temp)
    if not (0 < temp < 100):
        sys.exit("Temperature should be greater than 0 and less than 100")
    build_system()

def run(numberOfSteps): # The Main monte carlo loop
    """Führt numberOfSteps viele Schritte aus, d.h. bis zu numberOfSteps viele flips."""
    if(SIZE == NULL):
        sys.exit("Grid wurde noch nicht initialisiert. init(latticeSize, temp) muss zuerst aufgerufen werden.");
    for step in range(numberOfSteps):
        M = np.random.randint(0,SIZE)
        N = np.random.randint(0,SIZE)
        E = 2. * energy(N, M)
        # laut wiki flippen wir bei E >= 0, also wenn die neue Energie <= 0
        if E <= 0. or np.exp(-E/TEMP) > np.random.rand():
            system[N,M] *= -1
            delta.append([N,M])
        else:
            delta.append([-1,-1])

def bc(i): # Check periodic boundary conditions
    if i+1 > SIZE-1:
        return 0
    if i-1 < 0:
        return SIZE-1
    else:
        return i

def energy(N, M): # Calculate internal energy
    return -1 * system[N,M] * (system[bc(N-1), M] + system[bc(N+1), M] + system[N, bc(M-1)] + system[N, bc(M+1)])

def getSystemAtStep(step):
    """Gibt den Zustand des Modells nach step vielen Schritten(flips) aus.
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
                sysState[delta[i][0],delta[i][1]]*=-1;
    return sysState

def build_system(): # Build the system with random values of -1,1
    global system, initial_system
    initial_system=np.random.random_integers(0,1,(SIZE,SIZE))*2 - 1
    system=deepcopy(initial_system)

def print_system(system):
    # konvertiere -1,1 -> 0,1 und gib die matrix reihenweise aus
    for x in range(SIZE):
        print ''.join(str(z) for z in ((y+1)/2 for y in system[x,:]))
