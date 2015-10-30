__author__ = 'janek'
import dbscan
from numpy import ndarray
from numpy import array
import matplotlib.pyplot as plt

"""
this method plots the data in differnet colors

"""

def plotting(dbscan):
    #plot some data
    int=-1
    for daten in dbscan[:len(dbscan)-1]:
        xclusterneu={}
        yclusterneu={}
        for item in daten:
            int+=1
            x_cluster=[]
            y_cluster=[]
            for elements in item:
                x_cluster.append(elements[0])
                y_cluster.append(elements[1])
                xclusterneu[int]=[x_cluster]
                yclusterneu[int]=[y_cluster]

    datennoise=dbscan[len(dbscan)-1]
    x_clusternoise=[]
    y_clusternoise=[]
    for item in datennoise:
        x_clusternoise.append(item[0])
        y_clusternoise.append(item[1])


    plt.plot(x_clusternoise,y_clusternoise,'mx')
    colours=['ro','bo','go','ko','co','wo','bo','ro','go','bo','ko','co','wo','bo','ro','go','bo','ko','co','wo','bo','ro','go','bo','ko','co','wo','bo']
    for plotindex in range(len(xclusterneu)):
        plt.plot(xclusterneu[plotindex],yclusterneu[plotindex],colours[plotindex])
    plt.xlabel('x')
    plt.ylabel('y')
    plt.show()