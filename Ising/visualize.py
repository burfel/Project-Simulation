import main
import main_wolff
import matplotlib.pyplot as plt
import sys
import profile

def plot(H,step,T,extraTitle):
    fig = plt.figure(figsize=(6, 3.2))

    ax = fig.add_subplot(111)
    ax.set_title('Ising Model '+extraTitle+' Step '+str(step)+' at T='+str(temp))
    plt.imshow(H)
    ax.set_aspect('equal')

    cax = fig.add_axes([0.12, 0.1, 0.78, 0.8])
    cax.get_xaxis().set_visible(False)
    cax.get_yaxis().set_visible(False)
    cax.patch.set_alpha(0)
    cax.set_frame_on(False)
    cbar = plt.colorbar(ticks=[-1, 1])
    cbar.ax.set_yticklabels(['-1', '1'])# vertically oriented colorbar
    plt.draw()
    plt.show(block=False)
            
if len(sys.argv) == 4:
    size = int(sys.argv[1])
    steps = int(sys.argv[2])
    temp = float(sys.argv[3])
else:
    print("Usage: python2.7 visualize.py [Lattice Size/int] [Steps/int] [Temperature/float]")
    print("Using standard: Lattice Size = 64, Steps = 100000, Temperature = 2.2691853")
    size = 64
    steps = 100000
    temp = 2.2691853

#main.init(size,temp)
#main.run(steps)
#print main.getSystemAtStep(0)
#plot(main.getSystemAtStep(0),0,temp)    
#plot(main.getSystemAtStep(steps),steps,temp)

main.init(size,temp)
profile.run('main.run(steps)')
plot(main.getSystemAtStep(steps),steps,temp,"")

main_wolff.init(size,temp)
profile.run('main_wolff.run(steps)')
plot(main_wolff.getSystemAtStep(steps),steps,temp,"Wolff")

plt.show()

#   Hier mal meine Laufzeitergebnisse
#   python visualize.py 128 1000000 1
#
#   Normal
#
#   8925891 function calls in 49.311 seconds
#
#   Ordered by: standard name
#
#   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
#  1000000    2.181    0.000    2.181    0.000 :0(append)
#   925886    2.368    0.000    2.368    0.000 :0(rand)
#  2000000    6.131    0.000    6.131    0.000 :0(randint)
#        1    0.022    0.022    0.022    0.022 :0(range)
#        1    0.001    0.001    0.001    0.001 :0(setprofile)
#        1    0.000    0.000   49.310   49.310 <string>:1(<module>)
#        1   16.278   16.278   49.310   49.310 main.py:22(run)
#  4000000    8.330    0.000    8.330    0.000 main.py:35(bc)
#  1000000   14.000    0.000   22.330    0.000 main.py:43(energy)
#        1    0.000    0.000   49.311   49.311 profile:0(main.run(steps))
#        0    0.000             0.000          profile:0(profiler)
#
#  Wolff
#
#  9051221 function calls in 48.606 seconds
#
#   Ordered by: standard name
#
#   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
#  1000000    2.566    0.000    2.566    0.000 :0(append)
#    17036    0.043    0.000    0.043    0.000 :0(rand)
#  2000000    6.233    0.000    6.233    0.000 :0(randint)
#        1    0.011    0.011    0.011    0.011 :0(range)
#        1    0.000    0.000    0.000    0.000 :0(setprofile)
#        1    0.000    0.000   48.606   48.606 <string>:1(<module>)
#  4000000    8.242    0.000    8.242    0.000 main_wolff.py:24(bc)
#  1000000   10.676    0.000   45.999    0.000 main_wolff.py:41(oneClusterStep)
#  1000000   18.043    0.000   29.090    0.000 main_wolff.py:47(growCluster)
#    34180    0.196    0.000    0.239    0.000 main_wolff.py:69(tryAdd)
#        1    2.595    2.595   48.606   48.606 main_wolff.py:85(run)
#        1    0.000    0.000   48.606   48.606 profile:0(main_wolff.run(steps))
#        0    0.000             0.000          profile:0(profiler)