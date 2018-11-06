from scipy.optimize import fmin, fminbound
import numpy as np
import random
import time
import math
from scipy.stats import norm
import matplotlib.pyplot as plt

def akceptacjaOdrzucenieCiagla(f, a, b, *args):
    M = f(fminbound(lambda x: -f(x, *args),a,b), *args)
    while True:
        u1 = random.uniform(a,b)
        u2 = random.uniform(0,M)
        if u2 <= f(u1, *args):
            return u1    
        
def generujAOC(f, a, b, n = 1000, *args):
    return [akceptacjaOdrzucenieCiagla(f, a, b, *args) for _ in range(n)]

def f2(x):
    return 3*np.sin(x)*(np.cos(x))**2/2

def f(x):
    return (3*np.cos(x)*(np.sin(x))**2)/2

def optymalnyAO():
    pass
        
def generujProbke(n = 1000):
    M = 1/math.sqrt(3)
    toReturn = []
    i = 0
    while i<=n:
        u1 = math.pi*random.random()
        u2 = random.uniform(0,M)
        if u2 <= f(u1):
            toReturn.append(u1)
            i += 1
    return toReturn

def generujProbke2():
    c = 1.04582
    mu = 2*math.atan(math.sqrt(2-math.sqrt(3)))
    while True:
        y = random.gauss(mu,1/4)
        u = random.random()
        if u <= f(y)/(c*norm.pdf(y, loc = mu, scale = 1/4)):
            return np.sign(random.random() - 0.5)*y + math.pi/2
        
def opt(n = 1000):
    M = math.ceil(math.sqrt(3))
    losoweU1 = np.pi*np.random.rand(M*n)
    losoweU2 = np.random.rand(M*n)/M
    data = losoweU1[losoweU2 <= f2(losoweU1)]
    length = len(data)
    if length >= n:
        return data[:n]
    else:
        toAppend = []
        print('Zabrakło')
        for _ in range(length - n):
            toAppend.append(optymalnyAO())
        return list(data).extend(toAppend)

a = 0
b = np.pi
"""
start = time.time()
data = generujAOC(f, a, b, 10**4)
print(time.time() - start)
"""
start = time.time()
data = opt(10**6)
print(time.time() - start)

