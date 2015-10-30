import main_v2
import matplotlib.pyplot as plt


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
    
    

steps=100000
main_v2.init(100,30)
main_v2.run(steps)
print main_v2.getSystemAtStep(0)
plot(main_v2.getSystemAtStep(0),0,30)    
plot(main_v2.getSystemAtStep(steps),steps,30)