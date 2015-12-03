import pca
import numpy as np
import unittest 
import numpy.testing as npt
import math


# Unit tests

class TestPCA(unittest.TestCase):

    def test_init(self):
        testDataArray = np.array( [ [1, 2, 3], [4.5, 7.3, 1.2], [4, 5, 9], [7, 8, 9] ] )
        testK = 2
        testP = pca.PCA(testDataArray, testK)
        
        # Test array equality
        npt.assert_array_max_ulp(testP.data, testDataArray, maxulp = 0)

        # Test requested dimension equality
        self.assertTrue(testP.request ==  testK)


    def test_initExceptions(self):
        ''' tests exception functions '''
        testingList = [1,2,3]
        testingString = "test"
        testingInteger = 1
        testingFloat = 1.5
        testingLowerDimArray = np.array( [1,2,3] )
        testRightDimArray = np.array( [ [1,2,3], [4,5,6] , [7,8,9] ] )
        testSamplesLowerThanFeatures = np.array( [ [1,2,3], [4,5,6] ] )
        testRightK = 1
        testHigherK = 4
        testnegativeK = -1


        # Throwing Exceptions

        ## "X is not an numpy.ndarray."

        self.assertFalse( type(testingList) is np.ndarray )
        self.assertRaises( pca.PCADimException, lambda: pca.PCA(data, testRightK) )

        self.assertFalse( type(testingString) is np.ndarray )
        self.assertRaises( pca.PCADimException, lambda: pca.PCA(testingString, testRightK) )

        self.assertFalse( type(testingInteger) is np.ndarray )
        self.assertRaises( pca.PCADimException, lambda: pca.PCA(testingInteger, testRightK) )

        self.assertFalse( type(testingFloat) is np.ndarray )
        self.assertRaises( pca.PCADimException, lambda: pca.PCA(testingFloat, testRightK) )
        
        
        ## "X is not a 2-dimensional numpy.ndarray."
        self.assertFalse(2 == len(testingLowerDimArray.shape))
        self.assertRaises( pca.PCADimException, lambda: pca.PCA(testingLowerDimArray, testRightK) )


        ## "k has to be an integer."
        self.assertFalse( type(testingList) is int )
        self.assertRaises( pca.PCADimException, lambda: pca.PCA(testRightDimArray, testingList) )

        self.assertFalse( type(testingString) is int )
        self.assertRaises( pca.PCADimException, lambda: pca.PCA(testRightDimArray, testingString) )

        self.assertFalse( type(testRightDimArray) is int ) 
        self.assertRaises( pca.PCADimException, lambda: pca.PCA(testRightDimArray, testRightDimArray) )

        self.assertFalse( type(testingFloat) is int )
        self.assertRaises( pca.PCADimException, lambda: pca.PCA(testRightDimArray, testingFloat) )
        
        ## "k has to be greater than zero."
        self.assertFalse(testnegativeK > 1)
        self.assertRaises( pca.PCADimException, lambda: pca.PCA(testRightDimArray, testnegativeK) )
        

        ## "Number of samples is smaller than number of features."
        dimensions = testSamplesLowerThanFeatures.shape[0]
        samples = testSamplesLowerThanFeatures.shape[1]
        self.assertTrue(samples < dimensions)
        self.assertRaises( pca.PCADimException, lambda: pca.PCA(testSamplesLowerThanFeatures, testRightK) )

        ## "Parameter k exceeds number of features."
        self.assertTrue(testHigherK  > dimensions)
        self.assertRaises( pca.PCADimException, lambda: pca.PCA(testRightDimArray, testHigherK ) )


    def test_substractMean(self):
        '''  '''
        testDataArray = np.array( [ [1, 2, 3], [4.5, 7.3, 1.2], [4, 5, 9], [7, 8, 9] ] )
        p = pca.PCA(testDataArray, 2)
        p.substractMean()
        maximumDeviationInLastDigit = 1

        # Test mean calculation
        meanControl1 = (1 + 4.5 + 4 + 7)  / 4.
        meanControl2 = (2 + 7.3 + 5 + 8) / 4.
        meanControl3 = (3 + 1.2 + 9 + 9) / 4.
        meanControl = np.array( [meanControl1, meanControl2, meanControl3] ) 
        npt.assert_array_max_ulp(meanControl, p.mean, maxulp = maximumDeviationInLastDigit)

        # Test mean free data
        meanFreeTestDataArray = testDataArray - meanControl
        npt.assert_array_max_ulp(meanFreeTestDataArray, p.meanData, maxulp = maximumDeviationInLastDigit)
         

    def test_fit(self):
        ''' '''
        testRequestetDim = 1
        testDataSet = np.array( [ [0, 0], [1, 0], [2, 0], [3, 0], [4, 0], [0, 1], [0, -1] ] )
        meanFreeTestDataSet = testDataSet - np.mean(testDataSet, axis=0)

        # Test PCA with covariance matrix
        p = pca.PCACOV(testDataSet, testRequestetDim)
        p.substractMean()
        p.fit()

        ## Test covariance matrix
        controlCovMat = 1. / 6 * np.dot ( np.transpose (meanFreeTestDataSet), meanFreeTestDataSet )
        npt.assert_array_max_ulp(controlCovMat, p.covMat, maxulp = 0)

        ## Test eigenvalue and eigenvector calculation
        eigVal, eigVec = np.linalg.eig(p.covMat)
        for i in range( len(eigVal) ):
            eigVal[i] = math.fabs(eigVal[i])

        controlEigPairs = [ [ eigVal[0], eigVec[0] ], [ eigVal[1], eigVec[1] ] ]

        for i in range ( len(controlEigPairs) ):
            self.assertTrue(controlEigPairs[i][0] == p.eig_pairs[i][0])
            npt.assert_array_max_ulp(controlEigPairs[i][1], p.eig_pairs[i][1], maxulp = 0)

        ## Test transformation matrix
        controlTransformationMatrix = np.array( [ [1,0], [0,1] ] )
        npt.assert_array_max_ulp(controlTransformationMatrix, p.transMat, maxulp = 0)

        # Test PCA with SVD
        p = pca.PCASVD(testDataSet, testRequestetDim)
        p.substractMean()
        p.fit()

        ## Test transformation matrix
        controlTransformationMatrix = np.array( [ [1,0], [0,1] ] )
        npt.assert_array_max_ulp(controlTransformationMatrix, p.transMat, maxulp = 0)


    def test_project(self):
        ''' '''
        testRequestetDim = 1
        testDataSet = np.array( [ [0, 0], [1, 0], [2, 0], [3, 0], [4, 0], [0, 1], [0, -1] ] )

        # Test for PCA with covariance matrix

        ## Test dimensions of transformation matrix
        pCov = pca.PCACOV(testDataSet, testRequestetDim)
        pCov.substractMean()
        pCov.fit()
        pCov.project()
        self.assertTrue( pCov.dimensions == pCov.transMat.shape[0])
        self.assertTrue( pCov.dimensions == pCov.transMat.shape[1])


        # Test for PCA with SVD

        ## Test dimensions of transformation matrix
        pSvd = pca.PCASVD(testDataSet, testRequestetDim)
        pSvd.substractMean()
        pSvd.fit()
        pSvd.project()
        self.assertTrue( pSvd.dimensions == pSvd.transMat.shape[0])
        self.assertTrue( pSvd.dimensions == pSvd.transMat.shape[1])

        
    def test_pcaDataTransformation(self):
        ''' '''
        testRequestetDim = 1
        testDataSet = np.array( [ [0, 0], [1, 0], [2, 0], [3, 0], [4, 0], [0, 1], [0, -1] ] )

        pCov = pca.PCACOV(testDataSet, testRequestetDim)
        pCov.substractMean()
        pCov.fit()
        pCov.project()

        pSvd = pca.PCASVD(testDataSet, testRequestetDim)
        pSvd.substractMean()
        pSvd.fit()
        pSvd.project()

        npt.assert_array_max_ulp(pCov.transData, pSvd.transData, maxulp = 0)


    def test_dimensionReduction(self):
        ''' '''
        testRequestetDim = 1
        testDataSet = np.array( [ [0, 0], [1, 0], [2, 0], [3, 0], [4, 0], [0, 1], [0, -1] ] )

        p = pca.PCA(testDataSet, testRequestetDim)
        p.substractMean()

        transformedTestDataSet = np.zeros( ( 1, len(testDataSet) ) )
        for i in range ( len(testDataSet) ):
            transformedTestDataSet[0][i] = p.meanData[i][0]

        # Test for PCA with covariance matrix
        pCov = pca.PCACOV(testDataSet, testRequestetDim)
        pCov.substractMean()
        pCov.fit()
        pCov.project()
        pCov.dimensionReduction()

        print transformedTestDataSet
        print pCov.reducedTransData

        npt.assert_array_max_ulp(transformedTestDataSet, pCov.reducedTransData, maxulp = 0)

        # Test for PCA with SVD
        pSvd = pca.PCASVD(testDataSet, testRequestetDim)
        pSvd.substractMean()
        pSvd.fit()
        pSvd.project()
        pSvd.dimensionReduction()
        
        npt.assert_array_max_ulp(transformedTestDataSet, pSvd.reducedTransData, maxulp = 0)


if __name__ == '__main__':
    unittest.main()
