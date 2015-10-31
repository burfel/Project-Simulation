import main
import matplotlib.pyplot as plt
import sys
import profile

def plot(H,step,T):
    fig = plt.figure(figsize=(6, 3.2))

    ax = fig.add_subplot(111)
    ax.set_title('Ising Model Step '+str(step)+' at T='+str(T))
    plt.imshow(H)
    ax.set_aspect('equal')

    cax = fig.add_axes([0.12, 0.1, 0.78, 0.8])
    cax.get_xaxis().set_visible(False)
    cax.get_yaxis().set_visible(False)
    cax.patch.set_alpha(0)
    cax.set_frame_on(False)
    cbar = plt.colorbar(ticks=[-1, 1])
    cbar.ax.set_yticklabels(['-1', '1'])# vertically oriented colorbar
    plt.show()
    
    
if len(sys.argv) == 4:
    size = int(sys.argv[1])
    steps = int(sys.argv[2])
    temp = float(sys.argv[3])
else:
    print("Usage: python2.7 visualize.py [Lattice Size/int] [Steps/int] [Temperature/float]")
    print("Using standard: Lattice Size = 128, Steps = 100000, Temperature = 1")
    size = 128
    steps = 100000
    temp = 1

#main.init(size,temp)
#main.run(steps)
#print main.getSystemAtStep(0)
#plot(main.getSystemAtStep(0),0,temp)    
#plot(main.getSystemAtStep(steps),steps,temp)

profile.run('main.init(size,temp)')
profile.run('main.run(steps)')
plot(main.getSystemAtStep(steps),steps,temp)


#   Hier mal meine Laufzeitergebnisse
#   python visualize.py 128 1000000 1
#         16 function calls in 0.001 seconds
#
#   Ordered by: standard name
#
#   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
#        1    0.000    0.000    0.000    0.000 :0(__deepcopy__)
#        2    0.000    0.000    0.000    0.000 :0(get)
#        1    0.000    0.000    0.000    0.000 :0(getattr)
#        3    0.000    0.000    0.000    0.000 :0(id)
#        1    0.000    0.000    0.000    0.000 :0(issubclass)
#        1    0.000    0.000    0.000    0.000 :0(random_integers)
#        1    0.001    0.001    0.001    0.001 :0(setprofile)
#        1    0.000    0.000    0.000    0.000 <string>:1(<module>)
#        1    0.000    0.000    0.000    0.000 copy.py:145(deepcopy)
#        1    0.000    0.000    0.000    0.000 copy.py:267(_keep_alive)
#        1    0.000    0.000    0.000    0.000 main.py:15(init)
#        1    0.000    0.000    0.000    0.000 main.py:58(build_system)
#        1    0.000    0.000    0.001    0.001 profile:0(main.init(size,temp))
#        0    0.000             0.000          profile:0(profiler)
#
#
#         8926885 function calls in 48.378 seconds
#
#   Ordered by: standard name
#
#   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
#  1000000    2.146    0.000    2.146    0.000 :0(append)
#   926880    2.330    0.000    2.330    0.000 :0(rand)
#  2000000    5.956    0.000    5.956    0.000 :0(randint)
#        1    0.023    0.023    0.023    0.023 :0(range)
#        1    0.000    0.000    0.000    0.000 :0(setprofile)
#        1    0.000    0.000   48.378   48.378 <string>:1(<module>)
#        1   16.009   16.009   48.378   48.378 main.py:23(run)
#  4000000    8.136    0.000    8.136    0.000 main.py:38(bc)
#  1000000   13.778    0.000   21.914    0.000 main.py:46(energy)
#        1    0.000    0.000   48.378   48.378 profile:0(main.run(steps))
#        0    0.000             0.000          profile:0(profiler)