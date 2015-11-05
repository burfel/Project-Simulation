import sys
import numpy as np
import numpy.matlib
import matplotlib.pyplot as plt
from scipy.stats import multivariate_normal as mn
import math

class Bayes:

    def __init__(self, k):
        self.means = np.zeros(1)
        self.covs = np.zeros(1)
        self.dim = k

    def setDim(self, k):
        self.dim = k

    def train(self, training):

        # Seperate data into samples (X) and classes (Y)
        X = training[:, 0:self.dim] # [0,16)
        Y = training[:, 16]   # Class of each sample

        # For every class, of which we have 10, determine covariance and mean of training set
        self.means = np.zeros((10, self.dim))
        self.covs = np.zeros((10, self.dim, self.dim))
        for classIdx in range(10):
            data = X[Y[:] == classIdx, :]
            self.means[classIdx] = np.mean(data, axis=0)
            self.covs[classIdx] = np.cov(data.T)

    def classify(self, test):

        # Dig through test set and estimate class of each sample
        confusion = np.zeros((10,10))
        for row in test:
            maxP = 0.
            classEstimate = 0
            for classIdx in range(10):
                p = mn.pdf(row[0:self.dim], self.means[classIdx], self.covs[classIdx])
                if p > maxP:
                    maxP = p
                    classEstimate = classIdx

            confusion[classEstimate, row[16]] += 1

        # Gather accuracy for each class
        accuracy = 0.
        sums = confusion.sum(axis=0)
        for i in range(10):
            correct = confusion[i,i]
            accuracy += correct / sums[i]

        print confusion
        print "First", self.dim, "Dimension(s):", accuracy / 10.; print


def pca(training, test, svd=0):

    # Get specific values into submatrices
    X = training[:, 0:16] # Our samples, where each column represents a feature
    Y = training[:, 16]   # Class of each sample
    XT = test[:, 0:16]
    YT = test[:, 16]

    # Obtain mean along the columns and center data accordingly
    mean = np.mean(X, axis=0)
    mX = X - mean
    meanT = np.mean(XT, axis=0)
    mXT = XT - mean

    # Use svd instead of covariance
    if 0 < svd:

        # Construct magic matrix, whose nature escapes me
        m = mX / math.sqrt(16 - 1)

        # Apply SVD
        u, s, pc = np.linalg.svd(m)

        # Show some variances
        print s; print

        # Project data on principal components
        pX = mX.dot(pc)
        pXT = mXT.dot(pc)

    else:

        # Calculate covariance and eigenvector of training set
        cov = np.cov(mX.T)
        val, vec = np.linalg.eig(cov)

        # Have a look at normalized eigenvalues
        print val / np.sum(val); print

        # Sort eigenvectors from largest to smallest
        idx = val.argsort()[::-1]
        val = val[idx]
        vec = vec[idx]

        # Project data on principal components
        pX = mX.dot(vec)
        pXT = mXT.dot(vec)

    # Append class information
    pX = np.hstack((pX, np.reshape(Y, (Y.size, 1))))
    pXT = np.hstack((pXT, np.reshape(YT, (YT.size, 1))))

    return pX, pXT


def main(k, m):

    # Load training set into matrix
    training = np.genfromtxt("./pendigits-training.txt")
    testing = np.genfromtxt("./pendigits-testing.txt")

    # Train our classifier with untransformed data
    bayes = Bayes(16)
    bayes.train(training)
    bayes.classify(testing)

    # Transform data using pca
    trainT, testT = pca(training, testing, svd=m)

    # Train again with transformed data
    if k > 0:
        bayes.setDim(k)
        bayes.train(trainT)
        bayes.classify(testT)
    else:
        for k in range(1,17):
            bayes.setDim(k)
            bayes.train(trainT)
            bayes.classify(testT)


# Read commandline option
if len(sys.argv) != 3:
    sys.exit("Usage: python2.7 pca.py [PCA method] [k dimensions]\nPCA method: cov - PCA using eigenvectors\n            svd - PCA using single value decomposition\nk-dimensions: k - First k dimensions will be used for classifying\n              all - Compare over all dimensions\nExample: python2.7 pca.py cov 6")

method = 1 if "svd" == str(sys.argv[1]) else 0
k      = 0 if "all" == str(sys.argv[2]) else int(sys.argv[2])
main(k, method)
