import numpy as np
import math
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d import proj3d



# GENERATE SOME DATASETS

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



def getCovMat (dataset):
    # DEBUG SETTINGS
    debug_covMat = False

    # GENERAL VARIABLES
    n = dataset.shape[1] - 1 
    
    # DEBUG
    if debug_covMat:
        print "Multiplicator for normalisation = " + "1/" + str(n)

    # GET COVARAIANCE MATRIX
    covMat = 1. / n * np.dot ( dataset, np.transpose (dataset)  ) 

    # DEBUG
    if debug_covMat:
        print "Covariance Matrix: \n" , covMat , "\n"
        print "Control Covariance Matrix (numpy): \n" , np.cov(np.transpose (dataset)) , "\n" 

    return covMat


def meanFreeData (dataset):

    mean = np.mean(dataset, axis=0)
    meanData = dataset - mean

    return meanData


def pcaWithCovMat (dataset, inputDimension, meanFreeDatapoints = True):

    #DEBUG SETTINGS
    testing_values = True
    debug_PCA = False
    show_transformation_matrix = False

    #GET DATA AND EIGENVECTORS

    if meanFreeDatapoints:
        meanFreeDataset = meanFreeData (dataset)
        covMat = getCovMat (meanFreeDataset)

    else:
        covMat = getCovMat (dataset)

    eig_val, eig_vec = np.linalg.eig(covMat)


    # TESTS
    if testing_values:
        for i in range( len(eig_val) ):
            eigv = eig_vec[:,i].reshape(1 , inputDimension).T
            np.testing.assert_array_almost_equal( covMat.dot( eigv ) , eig_val[i] * eigv , decimal=6 , err_msg = "Eigen-Equation not fullfilled!" , verbose=True )

        for ev in eig_vec:
            np.testing.assert_array_almost_equal( 1.0 , np.linalg.norm(ev) , err_msg = "Eigenvectors are not normalized")


    # MAKE EIGENVECTOR AND EIGENVALUE PAIRS AND SORT
    eig_pairs = [ ( np.abs( eig_val[i] ) , eig_vec[:,i] ) for i in range( len(eig_val) ) ]

    eig_pairs.sort()
    eig_pairs.reverse()


    # DEBUG
    if debug_PCA:
        for i in range( len(eig_val) ):
            eigVec = eig_vec[:,i].reshape(1,3).T
            print "Eigenvector {}: \n{}".format( i+1 , eigVec ) , "\n"
            print "Eigenvalue {}: {}".format( i+1 , eig_val[i] ) , "\n"
            print 40 * "-"


        for i in eig_pairs:
            print "Eigenvalue: " , i[0]
            print "Eigenvector : " , i[1] , "\n"


    # MAKE TRANSFORMATIONMATRIX
    transMat = np.zeros ( (inputDimension , inputDimension) )

    for i in range ( inputDimension ):
        for j in range ( inputDimension ):
                transMat[i,j] = eig_pairs[i][1][j]

    if debug_PCA or show_transformation_matrix:
        print "Transformationmatrix: \n" , transMat , "\n"

    # TRANSFORM DATASET

    if meanFreeDatapoints:
        transformed_dataset = transMat.dot( meanFreeDataset )

    else:
        transformed_dataset = transMat.dot( dataset )


    # DEBUG
    if debug_PCA:
        print "Transformed Dataset: \n" , transformed_dataset , "\n"
        print "Covariance Matrix of X" , covMat , "\n"
        print "Covariance Matrix of Y" , getCovMat (transformed_dataset.T) , "\n"


    # RETURN
    return transformed_dataset


###################################################################################################


def pcaWithSVD (dataset, inputDimension):

    # DEBUG SETTINGS
    debug_PCA = False
    show_transformation_matrix = False

    # GET MEANFREE DATA

    meanFreeDataset = meanFreeData (dataset)

    # CONSTRUCT the Y-MATRIX
    
    n = dataset.shape[1] - 1

    if debug_PCA:
        print "n: " , n , "\n"
    
    newDatasetMatrix = 1. / math.sqrt ( n ) * dataset.T

    # DO SVD
    measurementDimensionMatrix, singularValues, principleComponents = np.linalg.svd(newDatasetMatrix)

    if debug_PCA:
        print "Measurement Dimension Matrix: \n" , "Shape: " , measurementDimensionMatrix.shape , "\n" , measurementDimensionMatrix , "\n"
        print "singularValues: \n" , "Shape: " , singularValues.shape , "\n" , singularValues , "\n"
        print "Principal Components: \n" , "Shape: " , principleComponents.shape , "\n" , principleComponents , "\n"


    # CALCULATE THE VARIANCES

    varianace = singularValues * singularValues 

    if debug_PCA:
        print "varianace: \n" , varianace , "\n"


    # TRANSFORM THE DATA

    transformed_dataset = principleComponents.T.dot(meanFreeDataset)

    if debug_PCA:
      print "transformed_dataset: \n" , transformed_dataset , "\n"



    # RETURN
    return transformed_dataset
  

###################################################################################################


# EVALUATION

## SETTINGS:
measurementDimension = 3
numberOfDatapoints = 5

## ROUTINE
datasetCov = generateDataset (measurementDimension, numberOfDatapoints , generateRandomCovMatrix = False)
datasetSVD = np.copy(datasetCov)
 
print "PCA with covariance Matrix: \n"
print "Dataset tranformed mean free: \n" , pcaWithCovMat (datasetCov, measurementDimension) , "\n"
# print "Dataset tranformed: \n" , pcaWithCovMat (datasetCov, measurementDimension, outputDimension, meanFreeDatapoints = False)


print "\n PCA with SVD: \n"
print "Dataset transformed: \n" , pcaWithSVD (datasetSVD, measurementDimension)


# COMMENTS:
## covMat and SVD have roughly the same Eigenvalues but the same Eigenvectors of the covMat are not equal to the collums of the PCA of the SVD. Therefore we get also different transformationresults!
