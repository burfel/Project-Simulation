__author__ = 'arno'
from dbscan import Dbscan
from numpy import ndarray
from numpy import array
from numpy import random
from numpy import loadtxt
import plotting
#some dummy data
number, x_coordinate, y_coordinate      = loadtxt('testdata/eps2-minpts3-cluster1-noise0.dat', unpack = True)
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
