import numpy as np
import matplotlib.pyplot as plt
import main_wolff

def bc(i): # Check periodic boundary conditions 
    if i+1 > SIZE-1:
        return 0
    if i-1 < 0:
        return SIZE-1
    else:
        return i

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

def measure():
    global nt, N
    nt    = 32
    N     = 4
    steps = 50
    
    global Energy, Magnetization, SpecificHeat, Susceptibility, T
    Energy = np.zeros(nt)
    Magnetization = np.zeros(nt)
    SpecificHeat = np.zeros(nt)
    Susceptibility = np.zeros(nt)

    T  = np.linspace(1, 3, nt) #temperature

    for m in range(len(T)):
        E1 = M1 = E2 = M2 = 0
        main_wolff.init(nt,T[m])
        main_wolff.run(steps)
    ## This part does the main calculations and the measurements
        mcSteps = len(main_wolff.delta)/2 # This is to equilibrate the system, Start measure after delta/2 steps
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

measure()

# plot the energy and Magnetization
f = plt.figure(figsize=(18, 10), dpi=80, facecolor='w', edgecolor='k');    

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