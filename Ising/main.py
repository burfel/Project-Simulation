
# coding: utf-8

# In[ ]:

import time
import numpy as np
import matplotlib as ml
import matplotlib.pyplot as plt
#%matplotlib inline

SIZE = 100
STEPS = 10000

def bc(i): # Check periodic boundary conditions 
    if i+1 > SIZE-1:
        return 0
    if i-1 < 0:
        return SIZE-1
    else:
        return i

def energy(system, N, M): # Calculate internal energy
    return -1 * system[N,M] * (system[bc(N-1), M] + system[bc(N+1), M] + system[N, bc(M-1)] + system[N, bc(M+1)])

def build_system(): # Build the system with random values of -1,1
    system = np.random.random_integers(0,1,(SIZE,SIZE))*2 - 1 
    #system[system==0] =-1
    
    return system

def plot(H,step,T):
    fig = plt.figure(figsize=(6, 3.2))

    ax = fig.add_subplot(111)
    ax.set_title('Ising Model Step '+str(step)+' at T='+str(T))
    plt.imshow(H)
    ax.set_aspect('equal')

    cax = fig.add_axes([0.12, 0.1, 0.78, 0.8])
    cax.get_xaxis().set_visible(False)
    cax.get_yaxis().set_visible(False)
    cax.patch.set_alpha(0)
    cax.set_frame_on(False)
    cbar = plt.colorbar(ticks=[-1, 1])
    cbar.ax.set_yticklabels(['-1', '1'])# vertically oriented colorbar
    plt.show()
    
def print_system(system):
    # konvertiere -1,1 -> 0,1 und gib die matrix reihenweise aus
    for x in range(SIZE):
        print ''.join(str(z) for z in ((y+1)/2 for y in system[x,:]))
        

def main(T): # The Main monte carlo loop
    system = build_system()
    
    for step in range(STEPS):
        M = np.random.randint(0,SIZE)
        N = np.random.randint(0,SIZE)

        E = -2. * energy(system, N, M)

        # laut wiki flippen wir bei E >= 0, also wenn die neue Energie <= 0
        if E <= 0.:
            system[N,M] *= -1
        elif np.exp(-1./T*E) > np.random.rand():
            system[N,M] *= -1
        
        if step % 1000 == 0:
            plot(system, step, T)
            
    return system
    
def run(): # Run the menu for the monte carlo simulation and Plot result
    print '='*70
    
    print '\tMonte Carlo Statistics for an ising model with'
    print '\t\tperiodic boundary conditions'
    print '='*70

    print "Choose the temperature for your run (0.1-100)"
    
    T = float(raw_input())
    start = time.time()    
    system = main(T)
    print time.time() - start
    print_system(system)

run()


# In[ ]:



