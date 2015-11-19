import numpy

__author__ = 'janek'

class Neighbor(object):
    def __init__(self, d):
        self.d = d

    def nearestneigh(self, p, eps):
        """
        gibt die Nachbarn einer Punktes P in der Umgebung eps aus
        :param p:
            Der Punkt dessen Nachbarn ermittelt werden sollen
        :param eps:
            Ein Punkt ist ein Nachbar wenn er im angegebenen Epsilon-Radius liegt
        :return: neighbors
            Die Liste von benachbarten Punkten

        """
        # sqd ist eine Liste mitEntfernungen hoch2 vom Punkt P zu jedem anderem Punkt in der Liste
        sqd = []
        # neighbors ist eine Liste mit den Nachbarn, die innerhalb von eps liegen
        neighbors = []
        for x, y in self.d:
            sqdakt = (x - p[0]) ** 2 + (y - p[1]) ** 2
            sqd.append(sqdakt)
        idx = numpy.argsort(sqd)
        i = 0
        for x in idx[1:]:
            if sqd[x] < eps ** 2:
                neighbors.append(self.d[x])

        neighbors = numpy.array(neighbors)
        return neighbors


    def nnPca(self, p, eps):
        """
        gibt die Nachbarn einer Punktes P in der Umgebung eps aus bricht fruehzeitig ab wenn die bedingung erfuellt ist
        :param p:
            Der Punkt dessen Nachbarn ermittelt werden sollen
        :param eps:
            Ein Punkt ist ein Nachbar wenn er im angegebenen Epsilon-Radius liegt
        :return: neighbors
            Die Liste von benachbarten Punkten
        """
        # sqd ist eine Liste mitEntfernungen hoch2 vom Punkt P zu jedem anderem Punkt in der Liste
        sqd = []
        # neighbors ist eine Liste mit den Nachbarn, die innerhalb von eps liegen
        neighbors = []
        for x in self.d:
            sqdakt = 0
            for i in range(0, p.shape[0]):
                sqdakt = sqdakt + (x[i] - p[i]) ** 2
                if sqdakt > eps ** 2:
                    break
            sqd.append(sqdakt)
        idx = numpy.argsort(sqd)
        i = 0
        for x in idx[1:]:
            if sqd[x] < eps ** 2:
                neighbors.append(self.d[x])
        neighbors = numpy.array(neighbors)
        return neighbors
