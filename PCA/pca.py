import numpy as np
import math

class PCA:

    @staticmethod # Allow 'static' use of method, i.e. instance-less
    def pca(X, k):
        """Apply principal component analysis on given data set using singular
           value decomposition.

           Example usage:

                from pca import PCA         # Import class 'PCA' from module 'pca'
                projData = PCA.pca(X, k)    # Project some data on its k most
                                            # important principal components

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
        if not(type(X) is np.ndarray):
            raise PCADimException("X is not an numpy.ndarray.")

        # Determine shape of X
        if 2 != len(X.shape):
            raise PCADimException("X is not a 2-dimensional numpy.ndarray.")

        # Dimensions of data matrix
        m = X.shape[0]
        n = X.shape[1]

        # Raise exceptions, when constraints are being violated
        if n < m:
            raise PCADimException("Number of samples is smaller than number of samples.")

        if k > m:
            raise PCADimException("Parameter k exceeds number of features.")

        # Subtract mean off of X
        mean = np.mean(X, axis=0)
        mX = X - mean

        # Construct magic helper matrix
        Y = mX.T / math.sqrt(m - 1)

        # Apply singular value decomposition, while ignoring the first two return values;
        # equivalent to "_, _, pc = np.linalg.svd(Y)"
        pc = np.linalg.svd(Y)[2]

        # Project data on principal components
        pX = pc.T.dot(mX)

        # Return kxN matrix of projected data
        return pX[0:k,:]


class PCADimException(Exception):
    """Exception class for handling PCA errors."""

    def __init__(self, err):
        self.err = err

    def __str__(self):
        return repr(self.err)
