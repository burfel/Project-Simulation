import numpy as np
class Ising:
    def __init__(self, size, temperature):
        """ Initializes Values """
        self.J           = 1
        self.size        = size
        self.temperature = temperature
        self.beta        = 1/self.temperature
        
    def makeConfig(self):
        """Generates a random spin config."""
        self.initial_config = [[np.random.choice([-1,1]) for i in range(self.size)] for j in range(self.size)]
        print self.initial_config
        return self.initial_config
        
    # def makeCluster(self):
        # """Generates a Cluster."""
        # self.cluster        = np.zeros((self.size,self.size), dtype=bool)
        # return self.cluster
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
        self.steps       = int(steps)
        self.size        = int(size)
        self.temperature = float(temperature)
        self.delta       = []
        self.init        = Ising(self.size, self.temperature)
        self.config      = self.init.makeConfig()
        self.J           = self.init.getJ()
        self.beta        = self.init.getTemp()
        
    def oneClusterStep(self):
        self.x       = np.random.randint(0, self.init.getSize())
        self.y       = np.random.randint(0, self.init.getSize())
        self.oldSpin = self.config[self.x][self.y]
        self.growCluster(self.x, self.y)

    def growCluster(self, x, y):
        self.cluster.append([x,y])
        self.delta.append([x,y])

        self.xprev = self.init.bc(x-1)
        self.xnext = self.init.bc(x+1)
        self.yprev = self.init.bc(y-1)
        self.ynext = self.init.bc(y+1)
        
        if ([self.xprev,y] not in self.cluster) and self.config[self.xprev][y] == self.oldSpin and 1-np.exp(-2.*self.J*self.beta) > np.random.rand():
            self.growCluster(self.xprev, y)

        if ([self.xnext,y] not in self.cluster) and self.config[self.xnext][y] == self.oldSpin and 1-np.exp(-2.*self.J*self.beta) > np.random.rand():
            self.growCluster(self.xnext, y)

        if ([x,self.yprev] not in self.cluster) and self.config[x][self.yprev] == self.oldSpin and 1-np.exp(-2.*self.J*self.beta) > np.random.rand():
            self.growCluster(x, self.yprev)

        if ([x,self.ynext] not in self.cluster) and self.config[x][self.ynext] == self.oldSpin and 1-np.exp(-2.*self.J*self.beta) > np.random.rand():
            self.growCluster(x, self.ynext)

    def flipCluster(self):
        for site in self.cluster:
            self.config[site[0]][site[1]] *= -1

    def run(self):
        for i in range(self.steps):
            self.cluster     = [] #self.init.makeCluster()
            self.oneClusterStep()
            self.flipCluster()
        return self.config, self.delta