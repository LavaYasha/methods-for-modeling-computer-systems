import numpy as np
import random
# линейный распределенный закон для T = (Tmax - Tmin) * x[i] - Tmin
def getTime(Tmin = 1, Tmax = 5, randNum = random.random()):
    T = (Tmax - Tmin) * randNum - Tmin
    return T

# Генерация рандомных чисел 
def getRandNum(xi = 1.0, a = 17, M = 1000, b = 1):
    xi = (a * xi - b) % M
    rand = xi / M
    return xi, rand


class Buffer(object):
    def __init__(self, size = 3):
        self.bufferSize = size
        self.storage = list(range(size))
        for i in range():
            self.storage[i] = 0

    def isEmpty(self):
        for i in range(self.storage):
            if self.storage[i] != 0:
                return False
        return True
                

class Server(object):
    def __init__(self):
        self.busy = False
        self.OperationTime = 0

    def isBusy(self):
        return self.busy
    
    def getOperationTime(self):
        return self.OperationTime

    def SetBusyServer(self, busy):
        self.busy = busy

    def OperationTimeSet(self, T):
        self.OperationTime = T    

if __name__ == "__main__":
    

    Server1 = True
    Server2 = True
    
    print ("Время прихода программ (линейный закон)")
    Tzmin = float(input("Tzmin = "))
    Tzmax = float(input("Tzmax = "))
    
    print ("Время обработки задач (линейный закон)")
    Tsmin = int(input("Tsmin = "))
    Tsmax = int(input("Tsmax = "))

    print ("Настройка рандомайзера")
    a = int(input("a = "))
    x0 = int(input("x0 = "))
    M = int(input("M = "))
    b = int(input("b = "))

    ServerWorkTime = 3600

    for i in range(ServerWorkTime):
        xi, randNum = getRandNum(x0, a, M, b)
        Ts = getTime(Tsmin, Tsmax, randNum)
        
    pass
