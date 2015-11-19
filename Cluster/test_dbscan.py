__author__ = 'janek'

import numpy as np
from dbscan import Dbscan
import unittest
import plotting
import pytest
import matplotlib.pyplot as plt

class TestClass:

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





