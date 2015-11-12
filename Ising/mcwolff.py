from lib import ising
from lib import plot
#import profile

system = ising.Wolff(128,1)

initialConfig, delta, flipcount = system.run(100)
      
show = plot.show(initialConfig, delta, flipcount)
show.saveVideo()
show.showPlot()