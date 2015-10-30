__author__ = 'arno'

import numpy as np
from pylab import plot,show
import nearestneighbour as near

def dbscan(D, eps, minPts):
    """
    This method will use DBSCAN
    """
    print "start dbscan with episilon = %d and minPts = %d" % (eps, minPts)
    clusterList = []
    visitedPoints = []
    noise = []
    for point in D:
        # isVisited()
        if not visited(point, visitedPoints):
            visitedPoints.append(point)
            N = near.nearestneigh(D, point, eps)
            print point
            print N
            print N.shape[0]
            if N.shape[0] < (minPts):
                noise.append(point)
            else:
                C = []
                C.append(point)
                for pointPrime in N:
                    if visited(pointPrime, visitedPoints) == False:
                        visitedPoints.append(pointPrime)
                        NPrime = near.nearestneigh(D, pointPrime, eps)
                        if NPrime.shape[1] >= (minPts * 2):
                            N = np.concatenate((N, NPrime), axis=0)
                    if not inCluster(pointPrime, clusterList):
                        C.append(pointPrime)
                clusterList.append(C);
    print "Cluster List:"
    for cl in clusterList:
        print cl
    print "Noise:"
    print noise
    return clusterList,noise

def visited(point, visitedPoints):
    for v in visitedPoints:
        if all(np.equal(point, v)):
            return True
    return False

def inCluster(pointPrime, clusterList):
    for cluster in clusterList:
        for clusterPoint in cluster:
            if all(np.equal(pointPrime, clusterPoint)):
                return True
    return False
"""
def regionQuery(D, P, eps):
    if np.array_equal(P, [1.0, 1.5]):
        return np.array([[1.0, 1.2], [0.9, 1.2]])
    if np.array_equal(P, [0.9, 1.2]):
        return np.array([[1.0, 1.5], [0.9, 1.2]])
    if np.array_equal(P, [0.9, 1.2]):
        return np.array([[1.0, 1.5], [1.0, 1.2]])
    if np.array_equal(P, [8.2, 1.0]):
        return np.array([[8.3, 0.7]])
    if np.array_equal(P, [8.3, 0.7]):
        return np.array([[8.2, 1.0]])

    return np.array([[]])
"""
