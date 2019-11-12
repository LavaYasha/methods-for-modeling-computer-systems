import numpy as np

# линейный распределенный закон для T = (Tmax - Tmin) * x[i] - Tmin
def getTime(Tmin = 1, Tmax = 5, randNum = 1.0):
    T = (Tmax - Tmin) * randNum - Tmin
    return T

# Генерация рандомных чисел 
def getRandNum(xi = 1.0, a = 17, M = 1000, b = 1):
    xi = (a * xi - b) % M
    rand = xi / M
    return xi, rand


if __name__ == "__main__":
    
    Server1 = True
    Server2 = True


    pass
