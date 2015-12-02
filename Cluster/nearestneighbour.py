import numpy
import itertools

__author__ = 'janek'

class Neighbor(object):

    def __init__(self, d, eps):
        self.d = d
        self.epssquare = eps ** 2

    def nnPca(self, p):
        """
        gibt die Nachbarn einer Punktes P in der Umgebung eps aus bricht fruehzeitig ab wenn die bedingung erfuellt ist
        :param p:
            Der Punkt (numpy-array) dessen Nachbarn ermittelt werden sollen
        :param eps:
            Ein Punkt ist ein Nachbar wenn er im angegebenen Epsilon-Radius liegt
        :return: neighbors
            Die Liste von benachbarten Punkten
        """
        # neighbors ist eine Liste mit den Nachbarn, die innerhalb von eps liegen
        neighbors = []
        for x in self.d:
            if self.isNeighbor(p, x):
                neighbors.append(x)
        neighbors = numpy.array(neighbors)
        return neighbors

    def isNeighbor(self, p, x):
        sqdakt = 0
        for i in range(0, p.shape[0]):
            sqdakt = sqdakt + (x[i] - p[i]) ** 2
            if sqdakt > self.epssquare:
                break
        return (sqdakt <= self.epssquare) and (sqdakt > 0)

def estimate_eps(D):
    nearest_distance = []
    print D[1]
    print D[2]
    print abs(D[1]-D[2])
    for i in range(len(D)):
        d= float("inf")
        for ii in range(len(D)):
            #print len(D)
            if i != ii:
                dneu=(abs(D[i]-D[ii]))
                #print dneu
                dneu=numpy.linalg.norm(dneu)
                if dneu<d:
                    d=dneu
        nearest_distance.append(d)
    nearest_distance=numpy.array(nearest_distance)
    print nearest_distance.mean()
    return nearest_distance.mean()*2