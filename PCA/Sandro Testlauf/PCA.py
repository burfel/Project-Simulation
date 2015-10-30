import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d import proj3d




# GENERAL SETTINGS
generate_datasets = True


# GENERATE SOME DATASETS

## DEBUG SETTINGS
print_debug_datasets = True
plot_debug_datasets = False 

if generate_datasets :

    # SETTINGS
    dimension = 3
    number_of_datapoints = 5
    generate_random_covMatrix = False 
    generate_random_mu = False
    mu_value = 0

    # GENERATE
    mu_generate = np.zeros( (dimension) )
    cov_mat_generate = np.zeros ( ( dimension , dimension ) )

    if generate_random_covMatrix:
        symm_counter = 1
        for i in range (dimension):
            for j in range (symm_counter):
                cov_mat_generate[i,j] = np.random.randint(10)
                cov_mat_generate[j,i] = cov_mat_generate[i,j]
            symm_counter = symm_counter + 1
     

    else:
        for i in range (dimension):
            cov_mat_generate[i,i] = 1


    if generate_random_mu:
        for i in range (dimension):
            mu_generate[i] = np.random.randint(10)

    else:
        if mu_value != 0:
            for i in range (dimension):
                mu_generate[i] = mu_value
    

    datasets = np.random.multivariate_normal(mu_generate, cov_mat_generate, number_of_datapoints).T

    # DEBUG
    if print_debug_datasets:
        print "Covariance Matrix: \n" , cov_mat_generate 
        print "mu: \n" , mu_generate
        print "Dataset: \n" , datasets , "\n"
        print "Shape dataset: " + str(datasets.shape)

    if plot_debug_datasets:
        if dimension == 2:
            plt.plot (datasets [0,:], datasets [1,:], "ro")
            plt.show ()

        if dimension == 3:
            fig = plt.figure(figsize=(8,8))
            ax = fig.add_subplot(111, projection='3d')
            plt.rcParams['legend.fontsize'] = 10
            ax.plot(datasets [0,:], datasets [1,:], datasets [2,:], 'o', markersize=8, color='blue', alpha=0.5, label='Dataset 1')
            
            plt.title('Samples for Dataset 1')
            ax.legend(loc='upper right')
            plt.show()

        else:
            print "Can't Plot! Check your Dimensions!"


#############################################
# BAUSTELLE!

def getMean (dataset , inputDimension):

    ## DEBUG SETTINGS:
    print_debug_getMean = True

    mean = np.zeros ( inputDimension )

    for i in range ( inputDimension ):
        mean[i] = np.mean ( dataset [i , :] )

    print mean

getMean (datasets , dimension)

############################################

def getCovMat (dataset):
    # DEBUG SETTINGS
    debug_covMat = False

    # GENERAL VARIABLES
    n = datasets.shape[1] - 1 
    
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


def PCA_with_COV (dataset, inputDimension , outputDimension):

    #DEBUG SETTINGS
    testing_values = True
    debug_PCA = False

    #GET DATA AND EIGENVECTORS
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
    transMat = np.zeros ( (outputDimension , inputDimension) )

    for i in range ( outputDimension ):
        for j in range ( inputDimension ):
                transMat[i,j] = eig_pairs[i][1][j]

    if debug_PCA:
        print "Transformationmatrix: \n" , transMat , "\n"

    # TRANSFORM DATASET
    transformed_dataset = transMat.dot( dataset )


    # DEBUG
    if debug_PCA:
        print "Transformed Dataset: \n" , transformed_dataset , "\n"
        print "Covariance Matrix of X" , covMat , "\n"
        print "Covariance Matrix of Y" , getCovMat (transformed_dataset.T) , "\n"


    # RETURN
    return transformed_dataset


    

PCA_with_COV (datasets, dimension, 2)
