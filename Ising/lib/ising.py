import numpy as np
import sys
import copy
import time

class Ising:
    def __init__(self, size, temperature):
        """ Initializes Values """
        self.J           = 1.
        self.size        = size
        self.temperature = temperature
        #self.kb          = 1.3806488e-23
        self.beta        = 1./(self.temperature)
        sys.setrecursionlimit(self.size*self.size*self.size)

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

class Wolff:
    def __init__(self, size, temperature):
        """ """
        self.size          = int(size)
        self.temperature   = float(temperature)
        self.delta         = []
        self.init          = Ising(self.size, self.temperature)
        self.config        = self.init.makeConfig()
        self.initialConfig = copy.deepcopy(self.config)
        self.J             = self.init.getJ()
        self.beta          = self.init.getBeta()
        self.p             = float(1-np.exp(-2.*self.J*self.beta))
        self.counter       = 0
        self.flipCount     = []
        self.times         = []

    def oneClusterStep(self):
        self.x       = np.random.randint(0, self.init.getSize())
        self.y       = np.random.randint(0, self.init.getSize())
        self.oldSpin = self.config[self.x][self.y]
        self.growCluster(self.x, self.y)
        self.flipCount.append(self.counter)

    def growCluster(self, x, y):
        self.counter += 1
        self.cluster.append([x,y])
        self.delta.append([x,y])

        xprev = self.init.bc(x-1)
        xnext = self.init.bc(x+1)
        yprev = self.init.bc(y-1)
        ynext = self.init.bc(y+1)
               
        for site in [[xprev,y],[xnext,y],[x,yprev],[x,ynext]]:
            if site not in self.cluster and self.config[site[0]][site[1]] == self.oldSpin and self.p > np.random.rand():
                self.growCluster(site[0], site[1])

    def flipCluster(self):
        for site in self.cluster:
            self.config[site[0]][site[1]] *= -1

    def run(self, steps):
        print self.p
        for i in range(steps):
            self.cluster = []
            start_time = time.time()
            self.oneClusterStep()
            self.flipCluster()
            print i, self.counter
            print time.time() - start_time
            print (time.time() - start_time)/self.counter
            self.times.append((time.time() - start_time)/self.counter)
            if (time.time() - start_time)/self.counter > 0.00025:
                break
                print "Exit Loop"
        print self.times
        return self.initialConfig, self.delta, self.flipCount