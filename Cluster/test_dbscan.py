__author__ = 'janek'

import numpy as np
from dbscan import Dbscan
import unittest
import plotting
import pytest
import matplotlib.pyplot as plt
from numpy import array
from numpy import random
from numpy import loadtxt
from nearestneighbour import Neighbor
import plotting

class TestClass(unittest.TestCase):

    @unittest.skip("test_dbscan1")
    def test_dbscan1(self):
        testdata='testdata/eps2-minpts3-cluster1-noise0.dat'
        number, x_coordinate, y_coordinate      = np.loadtxt(testdata, unpack = True)
        D=[None]*len(x_coordinate)
        for ii in range(len(x_coordinate)):
            D[ii]=[x_coordinate[ii],y_coordinate[ii]]
        D=np.array(D)
        epsilon=2
        minNeighbors=3
        dbscanner = Dbscan()
        test1 = dbscanner.run(D, epsilon, minNeighbors)
        datennoise=test1[len(test1)-1]
        Dresultall=[]
        for daten in test1[:len(test1)-1]:
            Dresult=[]
            for item in daten:
                Dresult.append(item)
            Dresultall.append(Dresult)  #
        #assert D==a
        Dr=np.array(Dresultall)
        a=[]
        assert datennoise==a
        assert D.all()==Dr.all()

    @unittest.skip("test_dbscan2")
    def test_dbscan2(self):
        testdata2='testdata/eps0p01-minpts1-cluster0-noise100.dat'
        number, x_coordinate, y_coordinate      = np.loadtxt(testdata2, unpack = True)
        D=[None]*len(x_coordinate)
        for ii in range(len(x_coordinate)):
            D[ii]=[x_coordinate[ii],y_coordinate[ii]]
        D=np.array(D)
        dbscanner = Dbscan()
        epsilon=0.01
        minNeighbors=1
        test1 = dbscanner.run(D, epsilon, minNeighbors)
        datennoise=test1[len(test1)-1]
        datennoise=np.array(datennoise)
        b=[]
        cluster1=test1[:len(test1)-1]
        assert cluster1[0]==b
        assert datennoise.all()==D.all()

    @unittest.skip("test_plotting")
    def test_plotting(self):
        #some dummy data
        number, x_coordinate, y_coordinate = loadtxt('testdata/eps2-minpts3-cluster1-noise0.dat', unpack = True)
        D=[None]*len(x_coordinate)
        for ii in range(len(x_coordinate)):
            D[ii]=[x_coordinate[ii],y_coordinate[ii]]
        #put in the data we want to use
        minNeighbors = 3
        epsilon = 2.
        data = array(D)
        # use dbscan
        dbscanner = Dbscan()
        result = dbscanner.run(data, epsilon, minNeighbors)
        # use plotting
        plotting.plotting(result)

    def test_cython(self):
        pass

    @unittest.skip("test_neighbor_2d")
    def test_neighbor_2d(self):
        #create simple data:
        a = range(0, 11)
        d = []
        for i in a:
            for j in a:
                d.append([i, j])
        n = Neighbor(array(d), 1.01)
        neighbors = n.nnPca(array([5,5]))
        print "neighbors of [5, 5] with eps = 1.01: " + str(neighbors)
        assert neighbors.shape == (4,2)