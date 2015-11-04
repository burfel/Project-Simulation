# -*- coding: utf-8 -*-

from numpy import *
import operator
from os import listdir
import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
import urllib2
from numpy.linalg import *
from scipy.stats.stats import pearsonr
from numpy import linalg as la

 
# load data points

#data = urllib2.urlopen("https://archive.ics.uci.edu/ml/machine-learning-databases/iris/iris.data").read() 
#raw_data = data.split("\n")

raw_data = loadtxt('iris.data', usecols=[0,1,2,3], delimiter=',',skiprows=1)
samples,features = shape(raw_data)

 
# normalize and remove mean
data = mat(raw_data[:,:4])

def svd(data, S=2):

    # calculate SVD
    U, s, V = linalg.svd( data )
    Sig = mat(eye(S)*s[:S])

    #take out columns that are not needed
    newdata = U[:,:S]

    # line used to retrieve dataset 
    #~ new = U[:,:2]*Sig*V[:2,:]

    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)
    colors = ['blue','red','black']
    
    for i in xrange(samples):

        ax.scatter(newdata[i,0],newdata[i,1], color= colors[int(raw_data[i,-1])])

    plt.title('SVD')
    plt.xlabel('SVD1')
    plt.ylabel('SVD2')
    plt.show()

         
svd(data,2)

svd