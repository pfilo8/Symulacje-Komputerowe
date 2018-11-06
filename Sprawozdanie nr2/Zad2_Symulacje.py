from date import Date
import random as rn
import numpy as np
import matplotlib.pyplot as plt


def y_generator(value=8):
    for i in range(value):
        y = int(value*rn.random())
        return y


def c_generator(li_1, y_p):
    c = li_1[0]/y_p
    for i in range(1, len(li_1)):
        if c < li_1[i]/y_p:
            c = li_1[i]/y_p
    return c


def variable(x_p=[1/10, 2/10, 1/20, 2/10, 1/20, 2/15, 2/15, 2/15], n=[0, 1, 2, 3, 4, 5, 6, 7]):
    x = []
    while True:
        u = rn.random()
        y = y_generator(len(x_p))
        y_p = 1/len(x_p)
        c = c_generator(x_p, y_p)
        if u <= x_p[y]/(y_p*c):
            x = y
            return n[x]


def pareto(k, x_m, n):
    if n > 1:
        out= []
        for _ in range(n):
            u = rn.random()
            out.append(x_m/((1-u)**(1/k)))
        return out
    elif n == 1:
        u = rn.random()
        return [x_m/((1-u)**(1/k))]
    else:
        return []


def cycles(start_year, end_year):
    x = range(start_year, end_year+1)
    out = []
    for i in x:
        if abs(i - 2016) % 4 == 0:
            out.append(366)
        else:
            out.append(365)
    return sum(out)


def check_days(month, year):
    months_30 = [4, 6, 9, 11]
    months_31 = [1, 3, 5, 7, 8, 10, 12]

    if month in months_31:
        return 31
    elif month in months_30:
        return 30
    else:
        if abs(2016 - year) % 4 == 0:
            return 29
        else:
            return 28


def clients_growth(n, oc, m_oc, m, ac, m_ac, mi, s_oc, repeat):
    ac_growth = []
    oc_growth = []
    for i in range(repeat):
        N = variable([0.5, 0.3, 0.2], [n, int(0.9 * n), int(n / 2)])
        Z = np.random.normal(0, 1)
        M = variable([0.1, 0.1, 0.4, 0.4], [n / 2, n / 3, n / 5, 50])

        new_clients_oc = np.random.poisson(mi * np.sqrt(M / oc) + s_oc / oc)

        if (oc / m_oc) ** 2.5 >= 1:
            client_lost_oc = np.random.binomial(N, 1)
        else:
            client_lost_oc = np.random.binomial(N, (oc / m_oc) ** 2.5)

        if n == 0:
            new_clients_ac = 0
        elif m / (n * ac) > 1:
            new_clients_ac = np.random.binomial(n, 1)
        else:
            new_clients_ac = np.random.binomial(n, m / (n * ac))

        if abs(Z) * ac / m_ac >= 1:
            client_lost_ac = np.random.binomial(m, 1)
        else:
            client_lost_ac = np.random.binomial(m, abs(Z) * ac / m_ac)

        oc_growth.append(new_clients_oc - client_lost_oc)
        ac_growth.append(new_clients_ac - client_lost_ac)
    return np.mean(oc_growth), np.mean(ac_growth)


def end_of_month(n, oc, m_oc, m, ac, m_ac, mi, s_oc):
    N = variable([0.5, 0.3, 0.2], [n, int(0.9 * n), int(n / 2)])
    Z = np.random.normal(0, 1)
    M = variable([0.1, 0.1, 0.4, 0.4], [n / 2, n / 3, n / 5, 50])

    new_clients_oc = np.random.poisson(mi * np.sqrt(M / oc) + s_oc / oc)

    if (oc/m_oc)**2.5 >= 1:
        client_lost_oc = np.random.binomial(N, 1)
    else:
        client_lost_oc = np.random.binomial(N, (oc / m_oc) ** 2.5)

    if n == 0:
        new_clients_ac = 0
    elif m/(n * ac) > 1:
        new_clients_ac = np.random.binomial(n, 1)
    else:
        new_clients_ac = np.random.binomial(n, m / (n * ac))

    if abs(Z) * ac / m_ac >= 1:
        client_lost_ac = np.random.binomial(m, 1)
    else:
        client_lost_ac = np.random.binomial(m, abs(Z) * ac / m_ac)

    n = n - client_lost_oc + new_clients_oc
    m = m - client_lost_ac + new_clients_ac

    if n < 0:
        n = 0
    if m < 0:
        m = 0

    return n, m


def poisson_process(f, T):
    t = 0
    i = 0
    times = []
    #M = max(0, f(fminbound(lambda x: -f(x), 0, T)))
    S = []
    varriable1 = rn.random()
    while True:
        t = t - (1/0.8)*np.log(varriable1)
        if t > T:
            return times
        if rn.random() <= 0.8/0.8:
            i += 1
            S.append(i)
            times.append(t)


def ac_pay_moments(T, m):
    times = []
    for i in range(m):
        t = 0
        flag = True
        while flag:
            helper = np.random.uniform(5, 5 + np.random.rayleigh(100))
            t = t + helper
            if t > T:
                flag = False
            if flag:
                times.append(np.ceil(t))
    return sorted(times)


def when_pay_ac(day, list_of_times):
    accidents = 0
    for i in range(len(list_of_times)):
        if day == list_of_times[0]:
            accidents += 1
            list_of_times.pop(0)
        else:
            return accidents, list_of_times


def five_sigmas(data):
    quilty = []
    std = np.std(data)
    for i in data:
        if i >= 5 * std:
            quilty.append(i)
    return quilty


def lambdas():
    '''Dla dni'''
    days = [4894, 4815, 4831, 4945, 5675, 4625, 3879]
    x = np.mean(days)
    '''Najbliżej średniej 4809.143, jest wtorek 4815 zatem lambda = 1.'''
    for i in range(len(days)):
        days[i] = round(days[i]/4815, 3)
    '''Dla miesięcy.'''
    months = [2195, 1896, 2168, 2318, 3108, 3375, 3646, 3645, 3590, 3645, 3059, 3202]
    '''Nie mamy dostatecznie bliskiej wartości wypadków w stosunku do średniej 2987.25 zatem to dale niej 
    nasza lambda2 będzie równa 1.'''
    for i in range(len(months)):
        months[i] = round(months[i]/2987.25, 3)
    return days, months


def oc_strategy(oc, m_oc, n, paid_last_month):
    paid = sum(paid_last_month)
    if n <= 1500:
        oc = 1/2 * oc
    else:
        oc = paid/n * 6/5

    if n <= 1500:
        mi = 150 * oc
    else:
        mi = 40 * oc

    while oc/m_oc >= 1:
        oc = oc * 7/10

    return oc, mi


def ac_strategy(ac, m_ac, m, paid_last_month):
    paid = sum(paid_last_month)
    if m <= 100:
        ac = 1/4 * ac
    else:
        ac = paid/m * m_ac
    if ac < 10:
        ac = 10
    while ac/m_ac > 1/4:
        ac = ac/2
    return ac


def paris_ruin(k, n, oc, m_oc, m, ac, m_ac, mi, s_oc, start_year, end_year, flag=False, text=False, strategy=False):
    '''  k_0 - kapitał początkowy, n - liczba początkowych sprzedanych polis oc, oc- cena jednej polisy oc,
    m - liczba początkowo sprzedanyh polis ac, ac - cena jednej policy ac, m_oc, m_ac - są to odpowienio popyt
    na polisy oc i ac, mi - nakłady przeznaczane na marketing, s_oc - stała związana z popytem na polisy oc '''

    lambda_days = [1.016, 1.0, 1.003, 1.027, 1.179, 0.961, 0.806]

    lambda_months = [0.735, 0.635, 0.726, 0.776, 1.04, 1.13, 1.221, 1.22, 1.202, 1.22, 1.024, 1.072]

    lambd_month = lambda_months[0]

    date = Date(1, 1, start_year)

    k_0 = k

    W_i = sum(np.random.exponential(0.05, n))

    count_oc_accidents = 0

    ac_accidents = ac_pay_moments(check_days(date.month, date.year), m)

    days = cycles(start_year, end_year)

    it = 1

    n_list = [n]
    m_list = [m]

    credit = 0
    is_credit = False
    bankruptcy_time = 0
    credit_time = 0

    kapital = []
    t = []

    holder = []

    paid_per_month = []
    paid_ac_per_month = []

    while days >= it:
        kapital.append(k)
        t.append(it)

        '''Warunki bankructwa'''
        if k < -2*k_0 - n*ac:
            quilty = five_sigmas(holder)
            return 0, kapital, t, quilty, n_list, m_list, count_oc_accidents

        if k < 0:
            bankruptcy_time += 1
        else:
            bankruptcy_time = 0

        if bankruptcy_time == 730:
            quilty = five_sigmas(holder)
            return 0, kapital, t, quilty, n_list, m_list, count_oc_accidents

        '''Podstawowe intensywności dla różnych rodzajów dni'''
        if date.holiday:
            lambd = lambda_months[7] * lambda_days[4]
        else:
            lambd_day = lambda_days[date.weekday]
            lambd = lambd_day * lambd_month

        '''Codzienne wypłaty.'''
        if W_i == 0:
            accidents = []
        else:
            accidents = poisson_process(lambd * W_i, 1)

        count_oc_accidents += len(accidents)/n

        if len(accidents) != 0:
            to_pay_oc = sum(pareto(8.26, 200, len(accidents)))
        else:
            to_pay_oc = 0

        ac_accidents_now = ac_accidents.count(date.day)

        if ac_accidents_now != 0:
            li_ac = []
            for i in range(ac_accidents_now):
                li_ac.append(min(abs(np.random.standard_cauchy(1)[0])/2, 500*ac))
                to_pay_ac = sum(li_ac)
        else:
            to_pay_ac = 0

        k = k - to_pay_oc - to_pay_ac
        paid_ac_per_month.append(to_pay_ac * ac_accidents_now)
        paid_per_month.append(to_pay_oc)
        holder.append(to_pay_oc)


        '''Kredyt.'''
        if is_credit:
            credit_time += 1

        if k < 0 and not is_credit:
            credit = 120*n
            credit_0 = credit
            k += credit
            is_credit = True

        if credit_time > 182 and (credit_time - 182) % 30 == 0:
            credit = credit - 1/12 * credit_0
            if credit == -8/12 * credit_0:
                is_credit = False
                credit_time = 0

        date.next_day()
        '''Sprawdzamy czy dzień jest ostatnim w miesiącu. '''
        if 1 == date.day:

            if strategy:
                hold_this = oc_strategy(oc, m_oc, n, paid_per_month)
                oc = hold_this[0]
                ac = ac_strategy(ac, m_ac, m, paid_ac_per_month)
                mi = hold_this[1]

            k -= mi
            helper = end_of_month(n, oc, m_oc, m, ac, m_ac, mi, s_oc)
            n = helper[0]
            m = helper[1]
            ac_accidents = ac_pay_moments(check_days(date.month, date.year), m)
            W_i = sum(np.random.exponential(0.05, n))

            n_list.append(n)
            m_list.append(m)

            if text:
                print(n, m, oc, ac)

            lambd_month = lambda_months[date.month - 1]

            k = k + n * oc + m * ac
            #print(sum(paid_per_month), n*oc, n)
            paid_ac_per_month = []
            paid_per_month = []

        if k >= 10**6 and flag:
            quilty = five_sigmas(holder)
            return 1, kapital, t, quilty, n_list, m_list

        it += 1

    quilty = five_sigmas(holder)

    if flag:
        return 0, kapital, t, quilty, n_list, m_list
    else:
        return 1, kapital, t, quilty, n_list, m_list, count_oc_accidents


if __name__ == '__main__':
    date = Date(17, 1, 2019)
    n = 500
    x = []
    flag = 3
    s = 0
    if flag == 1:
        ar = []
        kapitaly = []
        repeat = 250
        for i in range(repeat):
            holder = paris_ruin(k=500000, n=1, oc=1200000, m_oc=2400000, m=200, ac=120, m_ac=240, mi=30000, s_oc=0, start_year=2000,
                       end_year=2009, text=False, strategy=True)
            s += holder[0]
            kapitaly.append(max(holder[1]))

            print(100*(i+1)/repeat)
        print(s/repeat)
        print(np.mean(kapitaly))

    if flag == 2:
        mi = np.arange(10, 200000, 100)
        j = 1
        li = []
        for i in mi:
            li.append(np.mean(clients_growth(n=2000, oc=120, m_oc=240, m=2000, ac=36, m_ac=240, mi=i, repeat=10000, s_oc=0)[0]))
            print(j/len(mi)*100)
            j += 1
        plt.figure()
        plt.xlabel('Pieniądze wydane na marketing')
        plt.ylabel('Przyrost klientów')
        plt.plot(mi, li)
        plt.show()

    if flag == 3:
        s = 0


        x = paris_ruin(k=500000, n=1, oc=120000, m_oc=240000, m=100, ac=40, m_ac=2000, mi=25, s_oc=0, start_year=2000,
                           end_year=2004, flag=False, text=False, strategy=True)
        '''paris_ruin()[3] daje nam wszystkie wartości które przekraczają pięciokrotnie estymator wariancji'''

        plt.figure(2)
        plt.hist(x[-2])
        plt.figure(1)
        plt.plot(x[2], x[1])
        
        plt.show()

    if flag == 4:
        x = np.random.pareto(1, 10000)+1000
        plt.figure(1)
        plt.hist(x, bins=100)
        plt.show()
    '''Szukam odpowiedniego parametru rozkładu Pareto'''
    if flag == 5:
        print(np.mean(pareto(8.26, 200, 10000)))
    if flag == 6:
        k = 500000
        q = [k]
        p = [0]

        x = paris_ruin(k=k, n=200, oc=120, m_oc=3000, m=2000, ac=130, m_ac=800, mi=300, s_oc=2, start_year=2000,
                       end_year=2009)

        line, = plt.plot(p, q, color='k')
        plt.xlim([0, max(x[2])+10])
        plt.ylim([min(x[1]), max(x[1])+k])
        tCurrent = 0
        scale = 10
        i = 0
        while i < 1:
            for i in range(int((len(x[2])-1)/scale)):
                line.set_xdata(x[2][:scale*(i+1)])
                line.set_ydata(x[1][:scale*(i+1)])
                plt.draw()
                plt.pause(0.01)
            x[1].append(x[1][-1])
            x[2].append(x[2][-1])
            line.set_xdata(x[2][:-1])
            line.set_ydata(x[1][:-1])
            plt.pause(1)
            i = i+1

    if flag == 7:
        n = np.arange(200, 100000, 100)
        j = 1
        li = []
        for i in n:
            li.append(np.mean(
                clients_growth(n=i, oc=120, m_oc=240, m=100000, ac=10
                               , m_ac=360, mi=1, repeat=10000, s_oc=0)[1]))
            print(j / len(n) * 100)
            j += 1
        plt.figure()
        plt.xlabel('n')
        plt.ylabel('Przyrost klientów ac')
        plt.plot(n, li)
        plt.show()
