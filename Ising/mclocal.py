import init

from __future__ import division
import numpy as np
from numpy.random import rand
import matplotlib.pyplot as plt


delta = []

## monte carlo moves
def mcmove(config, beta):
    for i in range(N):
        for j in range(N):
                a = np.random.randint(0, N)
                b = np.random.randint(0, N)
                s =  config[a, b]
                nb = config[(a+1)%N,b] + config[a,(b+1)%N] + config[(a-1)%N,b] + config[a,(b-1)%N]
                cost = 2*s*nb
                if cost < 0 or rand() < np.exp(-cost*beta):
                    s *= -1
                    delta.append([a,b])
                else:
                    delta.append([-1,-1])
                config[a, b] = s
    return config

## Energy calculation
def calcEnergy(config):
    energy = 0
    for i in range(len(config)):
        for j in range(len(config)):
            S = config[i,j]
            nb = config[(i+1)%N, j] + config[i,(j+1)%N] + config[(i-1)%N, j] + config[i,(j-1)%N]
            energy += -nb*S
    return energy/4.

## magnetization of  the configuration
def calcMag(config):
    mag = np.sum(config)
    return mag

##  MAIN PART OF THE CODE
nt    = 100
N     = 16

Energy = np.zeros(nt)
Magnetization = np.zeros(nt)
SpecificHeat = np.zeros(nt)
Susceptibility = np.zeros(nt)

T  = np.linspace(1, 3, nt)        #temperature

for m in range(len(T)):
    E1 = M1 = E2 = M2 = 0
    E1 = np.float64(E1)
    M1 = np.float64(M1)
    E2 = np.float64(E2)
    M2 = np.float64(M2)
    
    init(100,1)

## This is to equilibrate the system
    eqSteps = 2000
    config = initialstate(N)
    config_init = deepcopy(config)
    
    for i in range(eqSteps):
        mcmove(config, 1.0/T[m])

## This part does the main calculations and the measurements
    mcSteps = 2000
    for i in range(mcSteps):
        mcmove(config, 1.0/T[m])   # monte carlo moves
        Ene = calcEnergy(config)        # calculate the energy
        Mag = calcMag(config)           # calculate the magnetisation

        E1 = E1 + Ene
        M1 = M1 + Mag
        M2 = M2   + Mag*Mag ;
        E2 = E2   + Ene*Ene;

        Energy[m]         = E1/(mcSteps*N*N)
        Magnetization[m]  = M1/(mcSteps*N*N)
        SpecificHeat[m]   = ( E2/mcSteps - E1*E1/(mcSteps*mcSteps) )/(N*T[m]*T[m]);
        Susceptibility[m] = ( M2/mcSteps - M1*M1/(mcSteps*mcSteps) )/(N*T[m]*T[m]);

# plot the energy and Magnetization
f = plt.figure(figsize=(18, 10), dpi=80, facecolor='w', edgecolor='k');    
plt.suptitle('Lattice Size = '+str(N)+', Steps = '+str(eqSteps+mcSteps)+', Points = '+str(nt), fontsize=24)

sp =  f.add_subplot(2, 2, 1 );
plt.plot(T, Energy, 'o', color="#A60628", label=' Energy');
plt.xlabel("Temperature (T)", fontsize=20);
plt.ylabel("Energy ", fontsize=20);

sp =  f.add_subplot(2, 2, 2 );
plt.plot(T, abs(Magnetization), '*', label='Magnetization');
plt.xlabel("Temperature (T)", fontsize=20);
plt.ylabel("Magnetization ", fontsize=20);


sp =  f.add_subplot(2, 2, 3 );
plt.plot(T, SpecificHeat, 'd', color="black", label='Specific Heat');
plt.xlabel("Temperature (T)", fontsize=20);
plt.ylabel("Specific Heat ", fontsize=20);


sp =  f.add_subplot(2, 2, 4 );
plt.plot(T, Susceptibility, '+', color="green", label='Specific Heat');
plt.xlabel("Temperature (T)", fontsize=20);
plt.ylabel("Susceptibility", fontsize=20);

plt.draw()
plt.savefig('output/measure-'+str(int(time.time()))+'-'+str(N)+'-'+str(eqSteps+mcSteps)+'.png')
plt.show()