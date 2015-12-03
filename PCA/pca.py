import numpy as np
import math
from scipy.spatial.distance import pdist, squareform

class PCA:
    """ Apply principal component analysis on a given data set
        for dimensionality reduction. """

    def __init__(self, X, k):
        """ Constructor. """

        # Raise exceptions, where needed
        if not(type(self.data) is np.ndarray):
            raise PCADimException("X is not an numpy.ndarray.")
        if not(type(self.request) is int):
            raise PCADimException("k is not an integer.")
        if 2 != len(self.data.shape):
            raise PCADimException("X is not a 2-dimensional numpy.ndarray.")

        # Pass data and k-first components
        self.data = X
        self.request = k

        # Dimensions of data matrix; TODO: Check for functional constistency
        self.samples = self.data.shape[0]
        self.dimensions = self.data.shape[1]

        # Raise exceptions, when constraints are being violated
        if self.samples < self.dimensions:
            raise PCADimException("Number of samples is smaller than number of features.")
        if self.request > self.dimensions:
            raise PCADimException("Parameter k exceeds number of features.")
        if self.request < 1:
            raise PCADimException("Parameter k need to be bigger than zero.")


    def substractMean(self):
        # TODO: Check for functional constistency
        self.meanData = self.data - np.mean(self.data, axis=0)


    def fit(self):
        pass


    def project(self):
        """ Project data on principal components. """
        self.transData = np.dot(self.transMat, self.meanData.T)


    def dimensionReduction(self):
        """ Return kxN matrix of projected data. """
        return self.transData[0:self.request,:]


    def kPCA(self, sigma):
        """ Process data into kernel space.

        Parameters
        ----------
        sigma:
            Variance of Gaussian radial basis function
        """

        # Compute distances between data points and store them within a (quadratic) matrix
        dist = pdist(self.data.T, "sqeuclidean")
        m = squareform(dist)

        # Build kernel
        k = np.exp((1. / 2. * sigma * sigma) * -m)

        # Center kernel
        s = np.ones(k.shape) / k.shape[0]
        k = k - ones.dot(s) - k.dot(s) + s.dot(k).dot(s)

        # Ascending eigenvectors
        vec = np.linalg.eigh(k)[1]

        # Move data into kernel space
        self.data = np.column_stack((vec[:, -i] for i in range(1, self.samples + 1))).T



class PCASVD(PCA):
    """ Apply PCA using singular value decomposition. """

    def fit(self):

        # Construct magic helper matrix
        Y = self.meanData.T / math.sqrt(self.dimensions - 1)

        # TODO: Check for functional constistency
        # We want to have the dimension x dimension matrix
        self.transMat = np.linalg.svd(Y)[0]



class PCACOV(PCA):
    """ Apply PCA using covariance matrix and eigenvectors. """

    def fit(self):

        # Calculate Covariance Matrix; TODO: Use numpy implementation
        covMat = 1. / (self.samples - 1) * np.dot (np.transpose(self.meanData), self.meanData)

        # Determine eigenvalues and eigenvectors
        eigVal, eigVec = np.linalg.eig(covMat)

        # TODO: We don't need pairs, since the output of eig() is already sorted by default
        # Make eigenvalue and eigenvector pairs
        self.eig_pairs = [(np.fabs(self.eig_val[i]), self.eig_vec[:,i]) for i in range(len(self.eig_val))]
        self.eig_pairs.sort()
        self.eig_pairs.reverse()

        # TODO: Avoid for-loops as much as possible, since this can be done otherwise
        # Make transformation matrix
        self.transMat = np.zeros((self.dimensions, self.dimensions))
        for i in range (self.dimensions):
            for j in range (self.dimensions):
                self.transMat[i,j] = self.eig_pairs[i][1][j]



def pca(X, k, mode="svd"):
    """ Static method for use with module.

    Parameters
    ----------
    X: 2-dimensional numpy-array
        Data matrix of form MxN with M features and N samples.

    k: int
        Project data on first k features with greatest variances. It must hold
        that k <= M.

    mode: string
        Specify method to use with PCA.

    Returns
    -------
    2-dimensional numpy-array
        Projected data matrix of form kxN with k features and N samples.

    """

    # Check parameters
    if "svd" == mode:
        p = PCASVD(X, k)
    elif "cov" == mode:
        p = PCACOV(X, k)
    else:
        raise PCADimException("You did not choose a valid mode. Valid modes are: svd and cov")

    # TODO: Maybe redesign handling of intermediate data due to possible memory issues
    p.substractMean()
    p.fit()
    p.project()
    return p.dimensionReduction()



class PCADimException(Exception):
    """Exception class for handling PCA errors."""

    def __init__(self, err):
        self.err = err

    def __str__(self):
        return repr(self.err)

