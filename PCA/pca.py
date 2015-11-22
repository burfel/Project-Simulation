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
        self.eig_pairs = [ ( np.abs( eig_val[i] ) , eig_vec[:,i] ) for i in range( len(eig_val) ) ]

        self.eig_pairs.sort()

        self.eig_pairs.reverse()


        # MAKE TRANSFORMATIONMATRIX
        self.transMat = np.zeros ( (self.dimensions , self.dimensions) )

        for i in range ( self.dimensions ):
            for j in range ( self.dimensions ):
                self.transMat[i,j] = self.eig_pairs[i][1][j]





class PCADimException(Exception):
    """Exception class for handling PCA errors."""

    def __init__(self, err):
        self.err = err

    def __str__(self):
        return repr(self.err)



# TESTS

def generateDataset (measurementDimension, numberOfDatapoints, valueMu = 0, generateRandomMu = False, generateRandomCovMatrix = False, symmetricMatrix = True):

    # DEBUG SETTINGS
    print_debug_dataset = False
    plot_debug_dataset = False 


    # GENERATE
    mu_generate = np.zeros( (measurementDimension) )
    cov_mat_generate = np.zeros ( ( measurementDimension , measurementDimension ) )

    if generateRandomCovMatrix:
        if symmetricMatrix:
            symm_counter = 1
            for i in range (measurementDimension):
                for j in range (symm_counter):
                    cov_mat_generate[i,j] = np.random.randint(10)
                    cov_mat_generate[j,i] = cov_mat_generate[i,j]
                symm_counter = symm_counter + 1
        else: 
            for i in range (measurementDimension):
                for j in range (measurementDimension):
                    cov_mat_generate[i,j] = np.random.randint(10)
     

    else:
        for i in range (measurementDimension):
            cov_mat_generate[i,i] = 1


    if generateRandomMu:
        for i in range (measurementDimension):
            mu_generate[i] = np.random.randint(10)

    else:
        if valueMu != 0:
            for i in range (measurementDimension):
                mu_generate[i] = valueMu
    

    dataset = np.random.multivariate_normal(mu_generate, cov_mat_generate, numberOfDatapoints).T

    # DEBUG
    if print_debug_dataset:
        print "Covariance Matrix: \n" , cov_mat_generate 
        print "mu: \n" , mu_generate
        print "Dataset: \n" , dataset , "\n"
        print "Shape dataset: " + str(dataset.shape)

    if plot_debug_dataset:
        if measurementDimension == 2:
            plt.plot (dataset [0,:], dataset [1,:], "ro")
            plt.show ()

        if measurementDimension == 3:
            fig = plt.figure(figsize=(8,8))
            ax = fig.add_subplot(111, projection='3d')
            plt.rcParams['legend.fontsize'] = 10
            ax.plot(dataset [0,:], dataset [1,:], dataset [2,:], 'o', markersize=8, color='blue', alpha=0.5, label='Dataset 1')
            
            plt.title('Samples for Dataset 1')
            ax.legend(loc='upper right')
            plt.show()

        else:
            print "Can't Plot! Check your Dimensions!"

    # RETURN
    return dataset


X = generateDataset (3, 5 , generateRandomCovMatrix = False)
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



print pca(X, k, mode="svd")
print pca(X, k, mode="cov")
print pca(X, k, mode="a")
