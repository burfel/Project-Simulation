import numpy as np
import math

class PCA:
    """ NEED TO BE UPDATED
    Example usage:

                from pca import PCA         # Import class 'PCA' from module 'pca'
                projData = PCA.pca(X, k)    # Project some data on its k most
                                            # important principle components

    """


    def __init__(self, X, k):
        self.data = X
        self.request = k

    def check(self):
        """
        Parameters
        ----------
        X: 2-dimensional numpy.array
            Data matrix of dimension MxN with M being the number of features
            and N being the number of samples. It must hold that N >= M.

        k: int
            Project data on first k features with greatest variances. It must hold
            that k <= M.

        Returns
        -------
        pX: 2-dimensional numpy.array
            Data matrix of dimension kxN

        Raises
        ------
        PCADimException
            If X is no 2-dimensional numpy.array.
            If N < M.
            If k > M.
        """

        # Determine object type
        if not(type(self.data) is np.ndarray):
            raise PCADimException("X is not an numpy.ndarray.")

        # Determine shape of X
        if 2 != len(self.data.shape):
            raise PCADimException("X is not a 2-dimensional numpy.ndarray.")

        # Dimensions of data matrix
        self.dimensions = self.data.shape[0]
        self.samples = self.data.shape[1]

        # Raise exceptions, when constraints are being violated
        if self.samples < self.dimensions:
            raise PCADimException("Number of samples is smaller than number of features.")

        if self.request > self.dimensions:
            raise PCADimException("Parameter k exceeds number of features.")



    def substractMean(self):
        mean = np.mean(self.data, axis=0)
        self.meanData = self.data - mean


    def fit(self):
        pass


    def project(self):
        # Project data on principal components
        self.transData = self.transMat.T.dot(self.meanData)

        # Return kxN matrix of projected data
        return self.transData[0:self.request,:]



class PCASVD(PCA):
    def fit(self):
        """
        Apply principal component analysis on given data set using singular
           value decomposition.

        """


        # Construct magic helper matrix
        Y = self.meanData.T / math.sqrt(self.dimensions - 1)

        # Apply singular value decomposition, while ignoring the first two return values;
        # equivalent to "_, _, self.transMat = np.linalg.svd(Y)"
        self.transMat = np.linalg.svd(Y)[2]

class PCACOV(PCA):

    
    def fit(self):
        """


        """

        # Calculate Covariance Matrix
        self.covMat = 1. / ( self.samples - 1 ) * np.dot ( self.meanData, np.transpose (self.meanData)  ) 


        # Determine eigenvalues and eigenvectors
        eig_val, eig_vec = np.linalg.eig(self.covMat)



        # MAKE EIGENVECTOR AND EIGENVALUE PAIRS AND SORT
        eig_pairs = [ ( np.abs( eig_val[i] ) , eig_vec[:,i] ) for i in range( len(eig_val) ) ]

        #!!! sort() does not work !!!
        eig_pairs.sort()

        self.eig_pairs = eig_pairs.reverse()
        print self.eig_pairs


        # MAKE TRANSFORMATIONMATRIX
        transMat = np.zeros ( (self.dimensions , self.dimensions) )

        for i in range ( self.dimensions ):
            for j in range ( self.dimensions ):
                self.transMat[i,j] = self.eig_pairs[i][1][j]





class PCADimException(Exception):
    """Exception class for handling PCA errors."""

    def __init__(self, err):
        self.err = err

    def __str__(self):
        return repr(self.err)



X = np.array( [[1,2,3], [4,5,6], [7,8,9]] )
k = 3



def pca(X, k, mode="svd"):
    """


    """

    if mode == "svd":
        p = PCASVD(X, k)


    elif mode == "cov":
        p = PCACOV(X, k)

    else:
        raise PCADimException("You choosed not a valid mode. Valid modes are: svd and cov")


    p.check()
    p.substractMean()
    p.fit()
    return p.project()



#print pca(X, k, mode="svd")
print pca(X, k, mode="cov")
print pca(X, k, mode="a")
