from lib import ising
from lib import plot
import sys

if len(sys.argv) != 3:
    N = 100
    T = 1.8
else:
    N = sys.argv[1]
    T = sys.argv[2]

def systemrun():
    sys = ising.Wolff(N,T)
    initialConfig, delta, flipcount = sys.run()

    show = plot.show(initialConfig, delta, flipcount)
    #show.saveVideo()
    show.showPlot()

systemrun()