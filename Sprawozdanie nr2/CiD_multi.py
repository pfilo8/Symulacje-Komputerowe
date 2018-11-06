import numpy as np
from multiprocessing import Pool
import multiprocessing as mp

def podpunktC():
    dt = 10**(-4)
    T = 10**6
    data = np.zeros(2)
    t = 0
    
    while t <= T:
        data += np.sqrt(dt)*np.random.randn(2)
        if np.sum((data - 5)**2) <= 1:
            return 1
        t += dt
    return 0

def podpunktD():
    dt = 10**(-4)
    T = 10**6
    data = np.zeros(2)
    t = 0
    kulaNr3 = np.array([-1,3])

    trafilW2 = False

    while t <= T:
        data += np.sqrt(dt)*np.random.randn(2)
        if not trafilW2:
            if np.sum((data - 2)**2) <= 1:
                trafilW2 = True
                #print('Wszedl w kule o srodku (2,2).')
        elif np.sum((data - 3)**2) <= 0.5:
            #print('Wszedl w kule o srodku (3,3).')
            return 0
        elif trafilW2 and np.sum((data - kulaNr3)**2) <= 1.6:
            #print('Wszedl w kule o srodku (-1,3).')
            return 1    
        t += dt
    return 0

def podpunktCwrapper(r):
    with open('PodpunktC.txt', 'a') as f:
        score = podpunktC()
        f.write(str(score) + '\n')
    return score

def podpunktDwrapper(r):
    with open('PodpunktD.txt', 'a') as f:
        score = podpunktD()
        f.write(str(score) + '\n')
    return score

def get_mean_for_monte_carlo_simulation(f, MCS):
    #sprawdzam ile mam rdzeni
    num_workers = mp.cpu_count()
    #mowi uzyj mi wszystkiego co masz do mojego zadania (mozesz zrobic num_workers-1 jak masz zamiar robic cos wiecej na komputerze)
    px = Pool(num_workers)
    #tworzymy sobie wektor "petli" dla n powtorzen
    r = np.linspace(0, 1, MCS)
    #i tutaj to wywolujemy funkcje get_mean_from_random_vector z argumentem r (dajemu mu cala liste)
    vel = px.map(f, r)
    px.close()
    px.join()
    return vel

if __name__ == '__main__':
    MCS = 1000
    results = get_mean_for_monte_carlo_simulation(podpunktCwrapper, MCS)
    print('Podpunkt C: ', sum(results)/MCS)
    results = get_mean_for_monte_carlo_simulation(podpunktDwrapper, MCS)
    print('Podpunkt D: ', sum(results)/MCS)