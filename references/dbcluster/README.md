Basic Algorithm
---------------
DBSCAN - https://en.wikipedia.org/wiki/DBSCAN

Algorithmic Improvements
------------------------
1. Neighbor search: the most expensive operation in density-based clustering
   is neighbor search - see https://en.wikipedia.org/wiki/Fixed-radius_near_neighbors
   and Lecture 2 in http://www.cs.wustl.edu/~pless/546/lectures/Lecture2.pdf 
   * In a low-dimensional space (e.g. obtained using PCA)
     a regular grid partitioning can be used for neighbor searching: a grid size
     of D is fixed, where D is equal to or larger than the largest distance for
     neighborhood. The boxes are stored in multidimensional arrays. Each array element
     keeps a list of data points associated to this box. When searching for neighbors
     within radius D, only the data points in the current box and in neighbor boxes
     need to be checked. In most cases, this approach reduces the search time for 
     neighbors for a given data point from O(n) to O(log n) or even O(1).
   * Such a lattice search can be improved when PCA has been employed to the data before.
     Firstly, we can use a lattice in the first three dimensions even if there are more
     than three dimensions (it might however loose efficiency compared to three-dimensional
     data). Secondly, the distance check can be written
	D^2 <= dx^2 + dy^2 + dz^2 + ...
     and this sum can be truncated whenever the right hand side violates the inequality.
     When ordering dimensions by variance using PCA there is a good chance that far-away
     points can be rejected early.
   * Established algorithms for neighbor search include
     k-d tree: https://en.wikipedia.org/wiki/K-d_tree and
     ball tree: https://en.wikipedia.org/wiki/Ball_tree

2. OPTICS Clustering algorithm - https://en.wikipedia.org/wiki/OPTICS_algorithm

3. DeLiClu Clustering algorithm - http://www.dbs.ifi.lmu.de/~kroegerp/papers/PAKDD06-DeLiClu.pdf



