Basic Algorithm
---------------
Monte Carlo Simulation of the Ising Model - see https://en.wikipedia.org/wiki/Ising_model

Algorithmic Improvements
------------------------
- Instead of single-flip trials use larger trials in order to speed up the mixing in the
  Monte-Carlo algorithm. Examples are the Swendsen-Wang algorithm or the Wolff algorithm
	(see 89_PRL_Wolff_CollectiveMove.pdf) 
- Find a way to visualize the results. Play with the parameters in the Ising model
  Hamiltonian (energy function) in order to find different behaviors

Implementation Improvements
---------------------------
- You will see that a direct Python implementation of the algorithm is unacceptably
  slow. Implement the algorithm in C and use cython in order to connect it to python calls
- Use CUDA (or OpenCL if you don't have an NVIDIA GPU) in order to speed the simulation
  up even more
 
