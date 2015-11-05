import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import main as main_wolff
import time
import sys

plt.rcParams['animation.ffmpeg_path'] ='C:\\Program Files\\ffmpeg-20151103-git-6df2c94-win64-static\\bin\\ffmpeg.exe'
FFwriter = animation.FFMpegWriter(fps=80,bitrate=1000)
off = 0

if len(sys.argv) == 5:
    size = int(sys.argv[1])
    steps = int(sys.argv[2])
    temp = float(sys.argv[3])
    offset = int(sys.argv[4])
else:
    size = 32
    steps = 10000
    #temp = 2.2691853
    temp = 3
    offset = 1
    print("Usage: python2.7 animate.py [Lattice Size/int] [Steps/int] [Temperature/float] [offset/int]")
    print "Using standard: Lattice Size = ",size,", Steps = ",steps,", Temperature = ",temp,", Offset = ",offset

main_wolff.init(size,temp)
main_wolff.run(steps)
imagelist = [ main_wolff.getSystemAtStep(i) for i in range(len(main_wolff.delta)) ]

if offset == 1:
    imagelist = imagelist[len(imagelist)*4/5:]
    off = len(imagelist)*4/5

fig = plt.figure() # make figure

# make axesimage object
# the vmin and vmax here are very important to get the color map correct
def init():
    global im, tit
    im = plt.imshow(imagelist[0], interpolation="nearest")
    tit = plt.title('', fontsize=24)
    return im,

# function to update figure
def updatefig(j):
    # set the data in the axesimage object
    im.set_array(imagelist[j])
    tit.set_text('Wolff at Temp: '+str(temp)+', Step '+str(j+off))
    plt.draw()
    # return the artists set
    return im,
# kick off the animation
ani = animation.FuncAnimation(fig, updatefig, init_func=init, frames=len(imagelist), interval=0, blit=True, repeat_delay=0)

# save the animation as an mp4.  This requires ffmpeg or mencoder to be
# installed.  The extra_args ensure that the x264 codec is used, so that
# the video can be embedded in html5.  You may need to adjust this for
# your system: for more information, see
# http://matplotlib.sourceforge.net/api/animation_api.html
ani.save('output/animation-'+str(int(time.time()))+'-'+str(size)+'-'+str(steps)+'-'+str(temp)+'.mp4', writer=FFwriter, fps=50, extra_args=['-vcodec', 'libx264'])

#plt.show()