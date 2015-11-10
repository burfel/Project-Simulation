from lib import ising
from lib import plot

system = ising.Wolff(64,1000,1)
initialConfig, delta = system.run()
show = plot.show(initialConfig, delta)
show.showPlot()