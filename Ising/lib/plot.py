import matplotlib.pyplot as plt
import matplotlib.animation as animation
import copy
import time

class figure:
    def __init__(self, initialConfig, delta):
        self.initialConfig = initialConfig
        self.delta         = delta
        self.imageList     = [self.initialConfig]
        self.fig           = plt.figure()
    
    def makeImageList(self):
        for i, site in enumerate(self.delta):
            tmp = copy.deepcopy(self.imageList[i])
            tmp[site[0]][site[1]] *= -1
            self.imageList.append(tmp)
        return
        
    def init(self):
        self.im = plt.imshow(self.imageList[0], interpolation="nearest")
        self.tit = plt.title('Step ', fontsize=24)
        return self.im,
        
    def updatefig(self, j):
        self.im.set_array(self.imageList[j])
        self.tit.set_text('Step '+str(j))
        plt.draw()
        return self.im,
    
    def animate(self):
        self.makeImageList()
        self.ani = animation.FuncAnimation(self.fig, self.updatefig, init_func=self.init, frames=len(self.imageList), interval=1, blit=True, repeat_delay=0)
        return self.ani
    
class show:
    def __init__(self, initialConfig, delta):
        self.figure = figure(initialConfig, delta)
        self.ani = self.figure.animate()
        
    def showPlot(self):
        plt.show()

    def saveVideo(self):
        plt.rcParams['animation.ffmpeg_path'] ='C:\\Program Files\\ffmpeg-20151103-git-6df2c94-win64-static\\bin\\ffmpeg.exe'
        self.FFwriter = animation.FFMpegWriter(fps=100,bitrate=600)
        self.ani.save('../output/animation-'+str(int(time.time()))+'.mp4', writer=self.FFwriter, fps=50, extra_args=['-vcodec', 'libx264'])
