import unittest
import ising
import numpy as np

class TestIsingMethods(unittest.TestCase):

  def test_init(self):
      # lambda verhindert, dass die exception geworfen wird
      
      self.assertRaises(ValueError, lambda: ising.Wolff(-3,2.26))
      self.assertRaises(ValueError, lambda: ising.Wolff(5,0))
      self.assertRaises(ValueError, lambda: ising.Wolff(5,200))
      
      wolff=ising.Wolff(32,50)
      wolff.makeConfig()
      
      self.assertTrue(wolff.getBeta()==1.0/50)
      self.assertTrue(wolff.getTemp()==50)
      self.assertTrue(wolff.getSize()==32)
      
      self.assertRaises(ValueError, lambda: wolff.getEnergy(np.zeros((3,4))))
      self.assertTrue(wolff.getEnergy(np.zeros((32,32))+1)==-1*2*32*32*wolff.getJ())
      self.assertTrue(wolff.getEnergy(np.zeros((32,32))-1)==-1*2*32*32*wolff.getJ())
      # vll noch ein paar konkrete konfigurationen
      
      
      
      #print wolff.getTemp()
if __name__ == '__main__':
    unittest.main()