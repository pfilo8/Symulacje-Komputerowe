# -*- coding: utf-8 -*-
"""
Created on Fri Jun  8 15:51:23 2018

@author: Patryk
"""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation

bok = 1.2
eps = 0.025
n = 20
dt = 10**(-3)

boki_x = np.array([1]*n + [-(2*i/(n+1)-1) for i in range(1,n+1)] + [-1]*n + [(2*i/(n+1)-1) for i in range(1,n+1)])
boki_y = np.array([(2*i/(n+1)-1) for i in range(1,n+1)] + [1]*n + [-(2*i/(n+1)-1) for i in range(1,n+1)] + [-1]*n)
alfa = np.arctan(boki_y/boki_x)

normaSi = np.sqrt(boki_x**2 + boki_y**2)
unormowany_dryf_x = -boki_x/normaSi
unormowany_dryf_y = -boki_y/normaSi

 # Create new Figure and an Axes which fills it.
fig = plt.figure(figsize=(5, 5))
ax = fig.add_axes([0, 0, 1, 1], frameon=False)
ax.set_xlim(-bok, bok), ax.set_xticks([])
ax.set_ylim(-bok, bok), ax.set_yticks([])

x = np.linspace(-1,1,100)
for a in alfa:
    ax.plot(x, np.tan(a)*x,'k')
    
phi = np.linspace(0,2*np.pi,100)
ax.plot((1+eps)*np.cos(phi), (1+eps)*np.sin(phi),'r')
ax.plot((1-eps)*np.cos(phi), (1-eps)*np.sin(phi),'r')

scat = ax.scatter(boki_x, boki_y)

def update(frame_number):
    global boki_x, boki_y
    
    random = dt*np.random.randn(4*n)
    new_x = random*np.cos(alfa)
    new_y = random*np.sin(alfa)
    
    normaXi = np.sqrt(boki_x**2 + boki_y**2)
    kierunek_dryfu = np.float64(normaXi < 1)*2 - 1
    
    boki_x += new_x - dt*kierunek_dryfu*unormowany_dryf_x
    boki_y += new_y - dt*kierunek_dryfu*unormowany_dryf_y
    
    scat.set_offsets(np.vstack([boki_x, boki_y]).T)


# Construct the animation, using the update function as the animation
# director.
animation = FuncAnimation(fig, update, interval=10)
plt.show()
