{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 35,
   "metadata": {
    "collapsed": false,
    "slideshow": {
     "slide_type": "-"
    }
   },
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "======================================================================\n",
      "\tMonte Carlo Statistics for an ising model with\n",
      "\t\tperiodic boundary conditions\n",
      "======================================================================\n",
      "Choose the temperature for your run (0.1-100)\n",
      "1\n",
      "0.330257177353\n"
     ]
    }
   ],
   "source": [
    "import time\n",
    "import numpy as np\n",
    "import matplotlib as ml\n",
    "import matplotlib.pyplot as plt\n",
    "#%matplotlib inline\n",
    "\n",
    "SIZE = 100\n",
    "STEPS = 10000\n",
    "\n",
    "def bc(i): # Check periodic boundary conditions \n",
    "    if i+1 > SIZE-1:\n",
    "        return 0\n",
    "    if i-1 < 0:\n",
    "        return SIZE-1\n",
    "    else:\n",
    "        return i\n",
    "\n",
    "def energy(system, N, M): # Calculate internal energy\n",
    "    return -1 * system[N,M] * (system[bc(N-1), M] + system[bc(N+1), M] + system[N, bc(M-1)] + system[N, bc(M+1)])\n",
    "\n",
    "def build_system(): # Build the system \n",
    "    system = np.random.random_integers(0,1,(SIZE,SIZE))\n",
    "    #system[system==0] =-1\n",
    "    \n",
    "    return system\n",
    "\n",
    "def plot(H,step,T):\n",
    "    fig = plt.figure(figsize=(6, 3.2))\n",
    "\n",
    "    ax = fig.add_subplot(111)\n",
    "    ax.set_title('Ising Model Step '+str(step)+' at T='+str(T))\n",
    "    plt.imshow(H)\n",
    "    ax.set_aspect('equal')\n",
    "\n",
    "    cax = fig.add_axes([0.12, 0.1, 0.78, 0.8])\n",
    "    cax.get_xaxis().set_visible(False)\n",
    "    cax.get_yaxis().set_visible(False)\n",
    "    cax.patch.set_alpha(0)\n",
    "    cax.set_frame_on(False)\n",
    "    cbar = plt.colorbar(ticks=[-1, 1])\n",
    "    cbar.ax.set_yticklabels(['-1', '1'])# vertically oriented colorbar\n",
    "    plt.show()\n",
    "\n",
    "def main(T): # The Main monte carlo loop\n",
    "    system = build_system()\n",
    "    \n",
    "    for step, x in enumerate(range(STEPS)):\n",
    "        M = np.random.randint(0,SIZE)\n",
    "        N = np.random.randint(0,SIZE)\n",
    "\n",
    "        E = -2. * energy(system, N, M)\n",
    "\n",
    "        if E <= 0.:\n",
    "            system[N,M] *= -1\n",
    "        elif np.exp(-1./T*E) > np.random.rand():\n",
    "            system[N,M] *= -1\n",
    "        \n",
    "        #if step % 1000 == 0:\n",
    "        #    plot(system, step, T)\n",
    "            \n",
    "    return system\n",
    "    \n",
    "def run(): # Run the menu for the monte carlo simulation and Plot result\n",
    "    print '='*70\n",
    "    print '\\tMonte Carlo Statistics for an ising model with'\n",
    "    print '\\t\\tperiodic boundary conditions'\n",
    "    print '='*70\n",
    "\n",
    "    print \"Choose the temperature for your run (0.1-100)\"\n",
    "    \n",
    "    T = float(raw_input())\n",
    "    start = time.time()\n",
    "    main(T)\n",
    "    print time.time() - start\n",
    "\n",
    "run()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {
    "collapsed": true
   },
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 2",
   "language": "python2",
   "name": "python2"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 2
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython2",
   "version": "2.7.10"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 0
}
