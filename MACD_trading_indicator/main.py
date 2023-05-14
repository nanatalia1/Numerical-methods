import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime


class Calculator:
    def results(self, file):
        time_values, data_values=Data.getData(Data)
        macd=MACD.calculateMACD(MACD,data_values)
        signal=MACD.calculateSignal(MACD, macd)
        intersections, intersection_times=MACD.calculateIntersections(MACD,macd,signal,data_values)
        #Diagrams.drawData(Diagrams, time_values, data_values)
        Diagrams.drawMACD(Diagrams,time_values,macd, signal, intersections, intersection_times)

class BuySell:
    def simulate(self, file):
        money=10000
        gold = 0
        time_values, data_values = Data.getData(Data)
        macd = MACD.calculateMACD(MACD, data_values)
        signal = MACD.calculateSignal(MACD, macd)
        for time in range(len(time_values)):
            if time>0:
                if macd[time]>=signal[time] and macd[time-1]<signal[time-1]:
                    money, gold = self.sell(money, time, data_values, gold)
                elif macd[time]<=signal[time] and macd[time-1]>signal[time-1]:
                    money, gold = self.buy(money, time, data_values, gold)
        money, gold = self.sell(money, time, data_values, gold) #sprzedanie na koniec
        money = str(round(money, 2)) #zaokraglanie
        print("Final money: ", money)

    def buy(self, money, day, data_values, gold):
        price=data_values[day]
        while money>=price:
            money-=price
            gold+=1
        return money, gold
    def sell(self, money, day, data_values, gold):
        price=data_values[day]
        while gold>0:
            money+=price
            gold-=1
        return money, gold

class Data:
    def getData(self):
        data_csv = pd.read_csv('data.csv').values
        data_values = data_csv[:, -1]  # dane z zamkniecia
        data_values = list(data_values)
        data_values.reverse()

        time_values=data_csv[:, 0]
        time_values=list(time_values)
        time_values.reverse()

        return time_values, data_values
class Diagrams:
    __times = []
    __int_times=[]
    __daty = []
    def drawMACD(self, time_val, macd, signal, intersections, intersection_times):
        for time in  range(len(time_val)):
            date=datetime.strptime(time_val[time], '%Y-%m-%d')
            #x=datetime(time_values)
            self.__times.append(date)

        plt.title('MACD dla złota')
        plt.plot(self.__times, macd, label="MACD", color='blue')
        plt.plot(self.__times, signal, label="Signal", color='green')
        for i in range(len(intersection_times)):
            intersection_times[i]=time_val[intersection_times[i]]
        for time in range(len(intersection_times)):
            date = datetime.strptime(intersection_times[time], '%Y-%m-%d')
            self.__int_times.append(date)
        ypoints = intersections

        plt.plot(self.__int_times, ypoints, 'o', label="Intersections", color='red')
        plt.legend()
        plt.xlabel('Rok, miesiac')
        plt.show()

    def drawData(self, time_val, data):
        for time in  range(len(time_val)):
            date=datetime.strptime(time_val[time], '%Y-%m-%d')
            self.__daty.append(date)
        plt.title('Złoto - wartości zamknięcia')
        plt.plot(self.__daty, data, label="Złoto", color='yellow')
        plt.legend()
        plt.xlabel('Rok, miesiac')
        plt.show()

class MACD:
    __macd = []
    __signal=[]
    __intersections=[]
    __intersection_times=[]

    def __init__(self, data_values):
        self.calculateMACD(data_values)

    def calculateEMA(self, data_values, day, N):
        alpha = 2 / (N + 1)
        __p = data_values[day: day + N + 1]
        a = __p[0]  # licznik
        b = 1.0  # mianownik
        k = 1
        while k <= N:
            if k < len(__p):
                a += (1 - alpha) ** k * __p[k]
                b += (1 - alpha) ** k
            else:
                break
            k += 1

        return a / b

    def calculateMACD(self, data_values):
        for i in range(len(data_values)):
                ema12=self.calculateEMA(self,data_values, i, 12)
                ema26=self.calculateEMA(self,data_values, i, 26)
                self.__macd.append(ema12-ema26)

        return self.__macd

    def calculateSignal(self, data_values):
        for i in range(len(data_values)):
                ema9=self.calculateEMA(self,data_values, i, 9)
                self.__signal.append(ema9)

        return self.__signal

    def calculateIntersections(self, macd, signal,data_values):
        for i in range(len(data_values)):
            if i >0:
                if macd[i] >= signal[i] and macd[i-1] < signal[i - 1]:
                    self.__intersections.append(macd[i])
                    self.__intersection_times.append(i)
                elif macd[i] <= signal[i] and macd[i - 1] > signal[i - 1]:
                    self.__intersections.append(macd[i])
                    self.__intersection_times.append(i)

        return self.__intersections, self.__intersection_times

if __name__ == '__main__':
    Calculator.results(Calculator(),'dane.csv')
    BuySell.simulate(BuySell(), 'dane.csv')
