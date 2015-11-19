import matplotlib.pyplot as plt
import matplotlib.animation as animation
import copy
import time
import sys

class figure:
    def __init__(self, initialConfig, delta, flipcount):
        self.initialConfig = initialConfig
        self.delta         = delta
        self.imageList     = []
        self.fig           = plt.figure()
        self.flipcount     = flipcount
        self.animationLength = 20000
    
    def makeImageList(self):
        print "Make ImageList ..."
        print self.flipcount
        self.imageList.append(self.initialConfig)
        self.tmp = copy.deepcopy(self.initialConfig)
        for i, site in enumerate(self.delta):
            # sys.stdout.write("\r%d%%" % i)
            # sys.stdout.flush()
            self.tmp[site[0]][site[1]] *= -1
            if i in self.flipcount:
                tmp = copy.deepcopy(self.tmp)
                self.imageList.append(tmp)
        return
    
    def makeImageListMetropolis(self):
        self.imageList.append(self.initialConfig)
        self.tmp = copy.deepcopy(self.initialConfig)
        # partition delta such that we only calculate a frame for every 50ms
        self.flipsPerFrame = 1+int(20*len(self.delta)/self.animationLength)
        for i, site in enumerate(self.delta):
            if(site[0] != -1): self.tmp[site[0]][site[1]] *= -1
            if (i+1) % self.flipsPerFrame == 0 or i+1 == len(self.delta):
                tmp = copy.deepcopy(self.tmp)
                self.imageList.append(tmp)
        return
        
    def init(self):
        self.im = plt.imshow(self.imageList[0], interpolation="nearest")
        self.tit = plt.title('Step ', fontsize=24)
        return self.im,
        
    def updatefig(self, j):
        self.im.set_array(self.imageList[j])
        if(len(self.flipcount) > 0): self.tit.set_text('Step '+str(j+1) +' of '+str(len(self.flipcount)))
        else: self.tit.set_text('Step ~' +str((j+1)*self.flipsPerFrame) +' of '+str(len(self.delta)))
        plt.draw()
        return self.im,
    
    def animate(self):
        if(len(self.flipcount) > 0): self.makeImageList()
        else: self.makeImageListMetropolis()
        self.ani = animation.FuncAnimation(self.fig, self.updatefig, init_func=self.init, frames=len(self.imageList), interval=int(self.animationLength/len(self.imageList)), blit=True, repeat_delay=5000)
        return self.ani

class show:
    def __init__(self, initialConfig, delta, flipcount):
        self.figure = figure(initialConfig, delta, flipcount)
        self.ani = self.figure.animate()
      
    def showPlot(self):
        plt.show()

    def saveVideo(self):
        plt.rcParams['animation.ffmpeg_path'] ='C:\\Program Files\\ffmpeg-20151103-git-6df2c94-win64-static\\bin\\ffmpeg.exe'
        FFwriter = animation.FFMpegWriter(fps=25,bitrate=26000)
        self.ani.save('output/animation-'+str(int(time.time()))+'.mp4', writer=FFwriter, fps=50, extra_args=['-vcodec', 'libx264'])