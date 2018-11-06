import datetime


class Date:
    def __init__(self, day, month, year):
        self.day = day
        self.month = month
        self.year = year
        self.weekday = datetime.datetime(self.year, self.month, self.day).weekday()  # 0 - monday, 6 - saturday !!!!!
        self.holiday = self.check_holiday(self.day, self.month, self.year)

    def easter(self, year):
        A = 24
        B = 5
        a = year % 19
        b = year % 4
        c = year % 7
        d = (a * 19 + A) % 30
        e = (2 * b + 4 * c + 6 * d + B) % 7
        day = 22 + d + e
        if day > 31:
            day = day - 31
            month = 4
        else:
            month = 3
        return month, day

    def check_holiday(self, day, month, year):
        '''Format przyjmowanej daty: [rok, miesiąc, dzień]. Funkcja zwraca True gdy dzień jest świętem natomiast False gdzy dzień jest powszedni.'''
        holiday = [[1, 1], [1, 6], [5, 1], [5, 3], [5, 20], [5, 31], [11, 1], [11, 11], [12, 25], [12, 26]]
        x = self.easter(year)
        y = []

        if x[1] == 31:
            y.append(x[0]+1)
            y.append(1)
        else:
            y.append(x[0])
            y.append(x[1]+1)
        holiday.append(list(x))
        holiday.append(y)
        if [month, day] in holiday:
            return True
        else:
            return False

    def next_day(self):
        months_30 = [4, 6, 9, 11]
        months_31 = [1, 3, 5, 7, 8, 10, 12]
        if abs(2016 - self.year)%4 == 0:
            feb = 29
        else:
            feb = 28

        self.day += 1
        if self.day > 27:
            if self.month in months_30:
                if self.day > 30:
                    self.day = 1
                    self.month += 1
            elif self.month in months_31:
                if self.day > 31:
                    self.day = 1
                    self.month += 1
                    if self.month == 13:
                        self.month = 1
                        self.year += 1
            else:
                if self.day > feb:
                    self.day = 1
                    self.month += 1
        self.weekday += 1
        if self.weekday > 6:
            self.weekday = 0
        self.holiday = self.check_holiday(self.day, self.month, self.year)

    def __str__(self):
        return '%d.%d.%d' % (self.day, self.month, self.year)


if __name__ == '__main__':
    date = Date(1, 3, 2016)
    for i in range(31):
        date.next_day()
        print(date.holiday)
    print(date)
    print(date.holiday)
