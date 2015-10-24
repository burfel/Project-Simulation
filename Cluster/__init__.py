__author__ = 'arno'
import dbscan
from numpy import ndarray
from numpy import array

#some dummy data
dummydaten = array([[1, 1.5], [1, 1.2], [0.9, 1.2], [8.2, 1.0], [8.3, 0.7], [9.2, 0.7], [-3.3, 5]])

#put in the data we want to use
minNeighbors = 1
epsilon = 0.85

data = dummydaten

#use dbscan
dbscan.dbscan(data, epsilon, minNeighbors)