__author__ = 'arno'

import numpy as np
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
        if not visited(point, visitedPoints):
            visitedPoints.append(point)
            #select the neighbors by the parameter eps
            N = near.nnPca(D, point, eps)
            #if not enough neigbors are found, the point is "noise", else proceed
            if N.shape[0] < (minPts):
                noise.append(point)
            else:
                #create a new cluster and put the point in it
                C = []
                C.append(point)
                #now check every neighbor p' of p
                for pointPrime in N:
                    if not visited(pointPrime, visitedPoints):
                        visitedPoints.append(pointPrime)
                        NPrime = near.nnPca(D, pointPrime, eps)
                        #if the point is not noise, then merge both neighborhoods
                        if NPrime.shape[0] >= (minPts):
                            N = np.concatenate((N, NPrime), axis=0)
                    #if the point does not already belong to a cluster, put it this one
                    if not inCluster(pointPrime, clusterList):
                        C.append(pointPrime)
                #and save the cluster in our list of clusters
                clusterList.append(C)
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
