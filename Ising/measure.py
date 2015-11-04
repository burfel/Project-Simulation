import numpy as np
import matplotlib.pyplot as plt
import main as main_wolff
import sys
import time

if len(sys.argv) == 4:
    points  = int(sys.argv[1])
    N     = int(sys.argv[3])
    steps = int(sys.argv[2])
else:
    points  = 64
    N     = 16
    steps = 10000
    print("Usage: python2.7 measure.py [Lattice Size/int] [Steps/int] [Measured points/int]")
    print "Using standard: Lattice Size = ",N,", Steps = ",steps,", Points = ",points

def bc(i): # Check periodic boundary conditions 
    if i+1 > N-1:
        return 0
    if i-1 < 0:
        return N-1
    else:
        return i

# Energy calculation
def calcEnergy(config):
    energy = 0
    for i in range(len(config)):
        for j in range(len(config)):
            S = config[i,j]
            nb = config[bc(i+1), j] + config[i,bc(j+1)] + config[bc(i-1), j] + config[i,bc(j-1)]
            energy += -nb*S
    return energy/4.

# magnetization of  the configuration
def calcMag(config):
    mag = np.sum(config)
    return mag

def measure():
    global Energy, Magnetization, SpecificHeat, Susceptibility, T

    Energy = np.zeros(points)
    Magnetization = np.zeros(points)
    SpecificHeat = np.zeros(points)
    Susceptibility = np.zeros(points)

    T  = np.linspace(1, 4, points) #temperature

    for m in range(len(T)):
        E1 = M1 = E2 = M2 = 0
        E1 = np.float64(E1)
        M1 = np.float64(M1)
        E2 = np.float64(E2)
        M2 = np.float64(M2)
        
        main_wolff.init(N,T[m])
        main_wolff.run(steps)
    ## This part does the main calculations and the measurements
        mcSteps = len(main_wolff.delta)/2 # This is to equilibrate the system, start measure after delta/2 steps
        for i in range(mcSteps):
            config = main_wolff.getSystemAtStep(len(main_wolff.delta)/2 + i)
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
    plt.suptitle('Lattice Size = '+str(N)+', Steps = '+str(steps)+', Points = '+str(points), fontsize=24)
    
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
    plt.savefig('measure-'+str(int(time.time()))+'-'+str(N)+'-'+str(steps)+'.png')
    plt.show(block=False)

measure()

plt.show()

print T
print Energy
print abs(Magnetization)
print SpecificHeat
print Susceptibility