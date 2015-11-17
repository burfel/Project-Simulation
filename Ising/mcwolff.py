from lib import ising
from lib import plot

def systemrun():
    system = ising.Wolff(64,1)
    initialConfig, delta, flipcount = system.run()

    show = plot.show(initialConfig, delta, flipcount)
    #show.saveVideo()
    show.showPlot()

systemrun()

