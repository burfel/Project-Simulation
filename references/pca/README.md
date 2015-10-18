Basic Algorithm
---------------
See 14_Shlens_PCA-Tutorial.pdf for an overview 

Algorithmic Improvements
------------------------
1. The computation of the covariance matrix is numerically poorly conditioned
   (find out why). A better approach is to use singular value decomposition (SVD)
   on the data matrix (see overview article and
   https://en.wikipedia.org/wiki/Singular_value_decomposition )
2. Suppose that the data matrix X is so large that it cannot be stored in memory.
   We must stream it from disc, i.e. read it in chunks. Devise a way to compute
   PCA using such chunked data. This is easy to do when using eigenvalue decomposition
   of covariance matrices to solve the problem. When using SVD, it's a little trickier
   and you need to reimplement a chunked version of the SVD algorithm
   (use Householder bidiagonalization)
3. kernel PCA: Nonlinear features can be extracted using kernel PCA. See:
   https://en.wikipedia.org/wiki/Kernel_principal_component_analysis
   If you define your kernel functions such that they can be truncated after a certain
   distance, you can use the nearest-neighbor tricks by the density-based-clustering
   team in order to speed up the algorithm.


