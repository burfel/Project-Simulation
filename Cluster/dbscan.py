__author__ = 'arno'

import numpy as np
from nearestneighbour import Neighbor
import pytest

class Dbscan:

    def __init__(self):
        pass

    def run(self, D, eps, minPts):
        """
        Der DBSCAN Algorithmus wird durchgefuehrt
        :param D:
            eine Liste an Datenpunkten
        :param eps:
            Ein Punkt ist ein Nachbar wenn er im angegebenen Epsilon-Radius liegt
        :param minPts
            Ein Punkt ist ein Cluster-Punkt, wenn er mindestens diese Anzahl Nachbarn hat
        :return: clusterList,noise
            Eine Liste von Clustern, das ist ein Liste von Listen von Datenpunkten
            und eine Liste der Noise, das ist eine Liste von Datenpunkten
        """
        print "start dbscan with episilon = %d and minPts = %d" % (eps, minPts)
        clusterList = []
        visitedPoints = []
        noise = []
        near = Neighbor(D)
        for point in D:
            if not self.visited(point, visitedPoints):
                visitedPoints.append(point)
                #select the neighbors by the parameter eps
                N = near.nnPca(point, eps)
                #if not enough neigbors are found, the point is "noise", else proceed
                if N.shape[0] < (minPts):
                    noise.append(point)
                else:
                    #create a new cluster and put the point in it
                    C = []
                    C.append(point)
                    #now check every neighbor p' of p
                    for pointPrime in N:
                        if not self.visited(pointPrime, visitedPoints):
                            visitedPoints.append(pointPrime)
                            NPrime = near.nnPca(pointPrime, eps)
                            #if the point is not noise, then merge both neighborhoods
                            if NPrime.shape[0] >= (minPts):
                                N = np.concatenate((N, NPrime), axis=0)
                        #if the point does not already belong to a cluster, put it this one
                        if not self.inCluster(pointPrime, clusterList):
                            C.append(pointPrime)
                    #and save the cluster in our list of clusters
                    clusterList.append(C)
        print "Cluster List:"
        for cl in clusterList:
            print cl
        print "Noise:"
        print noise
        return clusterList,noise

    def visited(self, point, visitedPoints):
        """
        ueberpruefe, ob der Datenpunkt point in der Datenpunkt-Liste visitedPoints ist
        :param point:
            ein Datenpunkt
        :param visitedPoints:
            eine Liste von Datenpunkten
        :return: bool
            True <=> point in vistedPoints
        """
        for v in visitedPoints:
            if all(np.equal(point, v)):
                return True
        return False

    def inCluster(self, point, clusterList):
        """
        ueberpruefe, ob der Datenpunkt point in einem der Datenpunkt-Listen von clusterList ist
        :param point:
            ein Datenpunkt
        :param clusterList:
            eine Liste von Listen von Datenpunkten
        :return: bool
            True <=> point in einer Liste in clusterList
        """
        for cluster in clusterList:
            for clusterPoint in cluster:
                if all(np.equal(point, clusterPoint)):
                    return True
        return False





