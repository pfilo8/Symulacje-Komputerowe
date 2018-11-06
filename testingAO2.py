import math
import time
import numpy as np

def optymalnyAO():
    M = 1/math.sqrt(3)
    while True:
        u1 = uniform_generator(0,math.pi)
        u2 = uniform_generator(0,M)
        if u2 <= f(u1):
            return u1 

def generation(x_vector, a_vector, p_vector, m, value=1):
    if value == 1:
        x_n = x_vector[0]
        for i in range(1, len(x_vector) - 1):
            x_n += a_vector[i]*x_vector[i]**p_vector[i]
        return int(x_n % m)
    result = []
    for _ in range(value):
        x_n = x_vector[0]
        for i in range(1, len(x_vector) - 1):
            x_n += a_vector[i]*x_vector[i]**p_vector[i]
        x_n = int(x_n % m)
        result.append(x_n)
        for i in range(len(x_vector)-1):
            x_vector[i] = x_vector[i+1]
        x_vector[-1] = x_n
    
    return result

def uniform_generator(a=0, b=1, value=1):
    out = []
    m = 1/(5**(-303))
    a_vector = [m*2**87, m*3**64, m*5**76]
    p_vector = [0.05738, 1.5646, 1.23456]
    for _ in range(value):
        x_n = [time.clock()%400, time.clock() % 400, time.time()]
        if value == 1:
            return a + generation(x_n, a_vector, p_vector, m)/(m-1)*(b-a)
        out.append(a + generation(x_n, a_vector, p_vector, m)/(m-1)*(b-a))
    return out

def opt(n = 1000):
    M = math.ceil(math.sqrt(3))
    losoweU1 = np.array(uniform_generator(0, math.pi, M*n))
    losoweU2 = np.array(uniform_generator(0, 1/M, M*n))
    data = losoweU1[losoweU2 <= f(losoweU1)]
    length = len(data)
    if length >= n:
        return data[:n]
    else:
        toAppend = []
        print('Zabrakło')
        for _ in range(length - n):
            toAppend.append(optymalnyAO())
        return list(data).extend(toAppend)
    
def f(x):
    return 3*np.sin(x)*(np.cos(x))**2/2

opt(10**5)
