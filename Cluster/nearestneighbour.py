__author__ = 'janek'

import numpy
# knn_search test

def nearestneigh(D,P,eps):
    """
    gibt die Nachbarn einer Punktes P in der Umgebung eps aus
    :param D:
    :param P:
    :param eps:
    :return: neighbors

    """
    #sqd ist eine Liste mitEntfernungen hoch2 vom Punkt P zu jedem anderem Punkt in der Liste
    sqd=[]
    #neighbors ist eine Liste mit den Nachbarn, die innerhalb von eps liegen
    neighbors=[]
    for x,y in D:
        sqdakt=(x-P[0])**2+(y-P[1])**2
        sqd.append(sqdakt)
    idx=numpy.argsort(sqd)
    i=0
    for x in idx[1:]:
        if sqd[x] < eps**2:

            neighbors.append(D[x])

    neighbors=numpy.array(neighbors)
    return neighbors
