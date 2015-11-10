import numpy as np
import sys
import copy

class Ising:
    def __init__(self, size, temperature):
        """ Initializes Values """
        self.J           = 1.
        self.size        = size
        self.temperature = temperature
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
    def __init__(self, size, steps, temperature):
        """ """
        self.steps         = int(steps)
        self.size          = int(size)
        self.temperature   = float(temperature)
        self.delta         = []
        self.init          = Ising(self.size, self.temperature)
        self.config        = self.init.makeConfig()
        self.initialConfig = copy.deepcopy(self.config)
        self.J             = self.init.getJ()
        self.beta          = self.init.getTemp()

    def oneClusterStep(self):
        self.x       = np.random.randint(0, self.init.getSize())
        self.y       = np.random.randint(0, self.init.getSize())
        self.oldSpin = self.config[self.x][self.y]
        self.growCluster(self.x, self.y)

    def growCluster(self, x, y):
        self.cluster.append([x,y])
        self.delta.append([x,y])

        xprev = self.init.bc(x-1)
        xnext = self.init.bc(x+1)
        yprev = self.init.bc(y-1)
        ynext = self.init.bc(y+1)
        
        if ([xprev,y] not in self.cluster) and self.config[xprev][y] == self.oldSpin:
            self.growCluster(xprev, y)

        if ([xnext,y] not in self.cluster) and self.config[xnext][y] == self.oldSpin:
            self.growCluster(xnext, y)

        if ([x,yprev] not in self.cluster) and self.config[x][yprev] == self.oldSpin:
            self.growCluster(x, yprev)

        if ([x,ynext] not in self.cluster) and self.config[x][ynext] == self.oldSpin:
            self.growCluster(x, ynext) 

        if ([xprev,y] not in self.cluster) and self.config[xprev][y] == -self.oldSpin and 1-np.exp(-2.*self.J*self.beta) > np.random.rand():
            self.growCluster(xprev, y)

        if ([xnext,y] not in self.cluster) and self.config[xnext][y] == -self.oldSpin and 1-np.exp(-2.*self.J*self.beta) > np.random.rand():
            self.growCluster(xnext, y)

        if ([x,yprev] not in self.cluster) and self.config[x][yprev] == -self.oldSpin and 1-np.exp(-2.*self.J*self.beta) > np.random.rand():
            self.growCluster(x, yprev)

        if ([x,ynext] not in self.cluster) and self.config[x][ynext] == -self.oldSpin and 1-np.exp(-2.*self.J*self.beta) > np.random.rand():
            self.growCluster(x, ynext)
                    

    def flipCluster(self):
        for site in self.cluster:
            self.config[site[0]][site[1]] *= -1

    def run(self):
        
        for i in range(self.steps):
            self.cluster = [] #self.init.makeCluster()
            self.oneClusterStep()
            self.flipCluster()
        return self.initialConfig, self.delta