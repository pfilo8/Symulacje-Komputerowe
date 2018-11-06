import pygame
import matplotlib.pyplot as plt
import math
import random

pygame.mixer.init()
pygame.mixer.set_num_channels(1)
sound = pygame.mixer.Sound('pop.wav')

plt.ion()
plt.xlabel('t')
plt.ylabel('N(t)')

T = 1000
lam = 1/20

plt.xlim([0,T])
plt.ylim([0,T*lam*1.1])

tSkoku = 0
tCurrent = 0
t = [0]
N = [0]

line, = plt.plot(t, N , color = 'k')

while tCurrent <= T:
    u = random.random()
    tSkoku -= math.log(u)/lam
    while tCurrent <= tSkoku:
        tCurrent += 1
        t.append(tCurrent)
        N.append(N[-1])
        line.set_xdata(t)
        line.set_ydata(N)
        plt.draw()
        plt.pause(0.001)
    sound.play()
    tCurrent += 1
    t.append(tCurrent)
    N.append(N[-1] + 1)
    plt.draw()
    plt.pause(0.001)
