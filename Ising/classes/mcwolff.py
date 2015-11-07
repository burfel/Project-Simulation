import init
import plot

system = init.Wolff(8,100,1)
initialConfig, delta = system.run()
show = plot.show(initialConfig, delta)
show.showPlot()