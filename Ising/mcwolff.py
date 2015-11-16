from lib import ising
from lib import plot

system = ising.Wolff(64,1)

initialConfig, delta, flipcount = system.run(20)
      
show = plot.show(initialConfig, delta, flipcount)
#show.saveVideo()
show.showPlot()
