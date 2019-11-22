import random

# линейный распределенный закон для T = (Tmax - Tmin) * x[i] - Tmin
def getTime(Tmin, Tmax, randNum):
    "linear distribution law for time"
    T = (Tmax - Tmin) * randNum + Tmin
    #print(f'rand number = {randNum}')
    return T

# Генерация рандомных чисел  // Usless //
def getRandNum(xi = 1.0, a = 17, M = 1000, b = 1):
    "gen pseudo random numbers"
    xi = (a * xi - b) % M
    rand = xi / M
    return xi, rand

class Server(object):
    "TODO: discription"
    def __init__(self):
        self.EmploymentStatus = 'free' # free - свободен busy - занят
        self.CurrentOperationTime = 0 
        self.downtime = 0
        self.workTime = 0
        self.procCount = 0

def colculation(simulation_time, Tzmin, Tzmax, Tsmin, Tsmax, ServersCount, bufferSize):
    "функция расчета"
    #   время прихода программ
    TimeIn = []
    
    #   время обработки программ
    WorkTime = []
    
    TimeIn.append(round(getTime(Tzmin, Tzmax, random.random()), 3))
    
    while TimeIn[-1] < simulation_time:
        TimeIn.append(round(getTime(Tzmin, Tzmax, random.random()) + TimeIn[-1], 3))
     

    Current_time = TimeIn[0]
    #   Настройки серверов
    Servers = []
    for k in range(ServersCount):
        Servers.append(Server())

    buffer = [0 for i in range(bufferSize)]

    #   основной цикл внутри симмуляции
    for i in range(len(TimeIn)):
        
        emptyServer = -1 # if -1 then all servers are busy
        isOneServerFree = False 

        for j in range(len(Servers)):
            if Servers[j].EmploymentStatus == 'free':
                isOneServerFree = True
                emptyServer = j 
                break
        
        if isOneServerFree and emptyServer != -1:
            if False:
                #TODO buffer check
                pass
            else:
                Servers[emptyServer].EmploymentStatus = 'busy'
                Servers[emptyServer].workTime = WorkTime[i]
                
        pass
    pass


if __name__ == "__main__":
    #   время симуляции впоследствии можно будет задать в часовом диапозоне
    SimulationTime = 60 * 60 

    #   время прихода программы (линейный закон)
    Tzmin = 1 / 2
    Tzmax = 5 / 6

    #  время обработки программы сервером программы (линейный закон)
    Tsmin = 1
    Tsmax = 5

    colculation(SimulationTime, Tzmin, Tzmax, Tsmin, Tsmax, 2, 3)
    pass