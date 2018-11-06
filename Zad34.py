from date import Date
import random as rn
import math


def poisson_process(f, T):
    t = 0
    times = []
    #M = max(0, f(fminbound(lambda x: -f(x), 0, T)))
    varriable1 = rn.random()
    while True:
        t = t - (1/0.8)*math.log(varriable1)
        if t > T:
            return times
        times.append(t)

def exponential_variables(number, lambd=2):
    return [rn.expovariate(lambd) for _ in range(number)]

def paris_ruin(year):

    k = 0
    fund = 3
    lose_iterator = 0
    it = 0
    p = 1/3  # zamiast funkcji t/3 bo i tak badamy przyrosty co t=1.
    date = Date(1, 1, year)

    # Jeżeli pierwszy rok będzie rokiem przestępnym to ostatni także w innym wypadku mamy tylko 1 rok przestępny.
    #  Rok 2016 był rokiem przestępnym stąd warunek.
    if abs(year - 2016) % 4 == 0:
        days = 1827
    else:
        days = 1826

    while days > it:
        if date.holiday or date.weekday == 5 or date.weekday == 6:
            lambd = 1.3
        elif date.month == 7 or date.month == 8:
            lambd = 1
        else:
            lambd = 0.8

        quantity_of_compensation = poisson_process(lambd, 1)
        number_of_pays = len(quantity_of_compensation)
        pay = sum(exponential_variables(number_of_pays))
        fund = fund + p - pay

        if fund < 0:
            lose_iterator += 1
            p = p * 0.9
            if fund < -10:
                return 0
        if lose_iterator == 4:
            return 0

        if fund > 20 * k:
            p = p * 1.05
            fund = fund - 10 * k

        date.next_day()
        it += 1
    return 1


if __name__ == '__main__':
    s = 0
    for i in range(10000):
        s += paris_ruin(2017)
    print(s/10000)
