import unittest
import ising
import numpy as np

class TestIsingMethods(unittest.TestCase):

  def test_init(self):
      # lambda verhindert, dass die exception geworfen wird
      
      self.assertRaises(ValueError, lambda: ising.Wolff(-3,2.26))
      self.assertRaises(ValueError, lambda: ising.Wolff(5,0))
      self.assertRaises(ValueError, lambda: ising.Wolff(5,200))
      
  def test_get_functions(self):
      wolff=ising.Wolff(32,50)
      metropolis=ising.Metropolis(32,50)
      
      self.assertTrue(wolff.getBeta()==1.0/50)
      self.assertTrue(wolff.getTemp()==50)
      self.assertTrue(wolff.getSize()==32)
      
      self.assertTrue(metropolis.getBeta()==1.0/50)
      self.assertTrue(metropolis.getTemp()==50)
      self.assertTrue(metropolis.getSize()==32)
      
  def test_energy_function(self):
      wolff=ising.Wolff(32,50)
      metropolis=ising.Metropolis(32,50)
      
      self.assertRaises(ValueError, lambda: wolff.getEnergy(np.zeros((4))))
      self.assertTrue(wolff.getEnergy(np.zeros((32,32))+1)==-1*2*32*32*wolff.getJ())
      self.assertTrue(wolff.getEnergy(np.zeros((32,32))-1)==-1*2*32*32*wolff.getJ())
      
      self.assertRaises(ValueError, lambda: metropolis.getEnergy(np.zeros((4))))
      self.assertTrue(metropolis.getEnergy(np.zeros((32,32))+1)==-1*2*32*32*metropolis.getJ())
      self.assertTrue(metropolis.getEnergy(np.zeros((32,32))-1)==-1*2*32*32*metropolis.getJ())
      
      self.assertTrue(metropolis.getEnergy(np.matrix([[1,1,1],[1,-1,1],[1,1,1]]))==-2*(9-4)*metropolis.getJ())
      self.assertTrue(metropolis.getEnergy(np.matrix([[-1,1,1],[1,1,1],[1,1,1]]))==-2*(9-4)*metropolis.getJ())
      self.assertTrue(metropolis.getEnergy(np.matrix([[-1,1,-1],[1,-1,-1],[1,-1,1]]))==6*metropolis.getJ())
      
      
if __name__ == '__main__':
    unittest.main()