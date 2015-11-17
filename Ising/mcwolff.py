from lib import ising
from lib import plot
import sys

if len(sys.argv) != 3:
    N = 64
    T = 2.26
else:
    N = sys.argv[1]
    T = sys.argv[2]

def systemrun():
    system = ising.Wolff(N,T)
    initialConfig, delta, flipcount = system.run()

    show = plot.show(initialConfig, delta, flipcount)
    #show.saveVideo()
    show.showPlot()

systemrun()