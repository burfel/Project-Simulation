__author__ = 'arno'
from dbscan import Dbscan
from numpy import ndarray
from numpy import array
from numpy import random
import plotting
#some dummy data
dummydaten = array([[1, 1.5], [1, 1.2], [0.9, 1.2], [8.2, 1.0], [8.3, 0.7], [9.2, 0.7], [-3.3, 5], [4.3, 0.7], [6.2, 0.7], [-2.3, 5]])
#put in the data we want to use
minNeighbors = 2
epsilon = 3
data = dummydaten
# use dbscan
dbscanner = Dbscan()
result = dbscanner.run(data, epsilon, minNeighbors)
# use plotting
plotting.plotting(result)
