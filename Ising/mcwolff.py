from lib import ising
from lib import plot
#import profile

system = ising.Wolff(128,1)

initialConfig, delta, flipcount = system.run(4000)
      
show = plot.show(initialConfig, delta, flipcount)
#show.saveVideo()
print "Render Plot"
show.showPlot()