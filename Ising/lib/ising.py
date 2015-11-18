import numpy as np
import sys
import copy
import time

class Ising:
    def __init__(self, size, temperature):
        """ Initializes Values """
        self.J           = 1.
        self.size        = int(size)
        self.temperature = float(temperature)
        #self.kb          = 1.3806488e-23
        self.beta        = 1./(self.temperature)
        sys.setrecursionlimit(self.size*self.size)

    def makeConfig(self):
        """Generates a random spin config."""
        self.initial_config = np.random.random_integers(0,1,(self.size,self.size))*2 - 1        
        print self.initial_config
        return self.initial_config
        
    def getJ(self):
        return self.J

    def getSize(self):
        return self.size

    def getTemp(self):
        return self.temperature

    def getBeta(self):
        return self.beta

    def bc(self, i):
        """Check periodic boundary conditions."""
        if i+1 > self.size-1:
            return 0
        if i-1 < 0:
            return self.size-1
        else:
            return i
    def getMag(self, config):
        return np.sum(config)

class Wolff(Ising):
    def __init__(self, size, temperature):
        """ """
        Ising.__init__(self, size, temperature)
        self.delta         = []
        self.config        = self.makeConfig()
        self.initialConfig = copy.deepcopy(self.config)
        self.p             = float(1-np.exp(-2.*self.J*self.beta))
        self.counter       = 0
        self.flipCount     = []
        self.times         = []

    def oneClusterStep(self):
        self.x       = np.random.randint(0, self.getSize()-1)
        self.y       = np.random.randint(0, self.getSize()-1)
        self.oldSpin = self.config[self.x][self.y]
        self.growCluster(self.x, self.y)
        self.flipCount.append(self.counter)

    def growCluster(self, x, y):
        self.counter += 1
        self.config[x,y] *= -1
        self.delta.append([x,y])

        xprev = self.bc(x-1)
        xnext = self.bc(x+1)
        yprev = self.bc(y-1)
        ynext = self.bc(y+1)
               
        for site in [[xprev,y],[xnext,y],[x,yprev],[x,ynext]]:
             if self.config[site[0]][site[1]] == self.oldSpin and np.random.rand() < self.p:
                self.growCluster(site[0], site[1])

    def run(self):
        print "p =",self.p
        starttime = time.time()        
        while abs(self.getMag(self.config)) < (self.size*self.size*0.98):
            self.oneClusterStep()
        print self.getMag(self.config)
        print "Finished calculation at",self.counter,"elementary steps in", time.time()-starttime,"s."
        return self.initialConfig, self.delta, self.flipCount