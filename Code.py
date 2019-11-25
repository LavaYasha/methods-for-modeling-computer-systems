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
        self.downTime = 0
        self.workTime = 0
        self.procCount = 0
        self.InTime = 0
        self.OutTime = 0

class Buff(object):
    def __init__(self):
        self.TimeIn = 0
        self.TimeOut = 0
        self.WorkTime = 0
        self.BufferTime = 0


def colculation(simulation_time, Tzmin, Tzmax, Tsmin, Tsmax, ServersCount, bufferSize):
    "функция расчета"
    #   время прихода программ
    TimeIn = []
    
    #   время обработки программ
    WorkTime = []
    
    TimeIn.append(round(getTime(Tzmin, Tzmax, random.random()), 3))
    WorkTime.append(round(getTime(Tsmin, Tsmax, random.random()), 3))
    
    while TimeIn[-1] < simulation_time:
        TimeIn.append(round(getTime(Tzmin, Tzmax, random.random()) + TimeIn[-1], 3))
        WorkTime.append(round(getTime(Tsmin, Tsmax, random.random()), 3))
     
    #   Время для расчетов
    Current_time = TimeIn[0]

    #   Инициализация серверов
    Servers = []
    for k in range(ServersCount):
        Servers.append(Server())
        Servers[k].downTime += Current_time

    #  Инициализация буфера
    buffer = [Buff() for i in range(bufferSize)]

    #   Флаг работы серверов
    isWork = False

    #   Время без использования буфера
    TimeWithoutBuffer = 0
    #   основной цикл внутри симмуляции
    for i in range(len(TimeIn)):
        
        emptyServer = -1 # if -1 then all servers are busy
        isOneServerFree = False 

        for j in range(len(Servers)):
            if Servers[j].EmploymentStatus == 'free':
                isOneServerFree = True
                emptyServer = j 
                break
        
        if (isOneServerFree) and (emptyServer != -1):
            WorkTime.append(round(getTime(Tsmin, Tsmax, random.random()), 3))
            Servers[emptyServer].EmploymentStatus = 'busy'
            Servers[emptyServer].TimeIn = TimeIn[i]
            Servers[emptyServer].workTime = WorkTime[i]
            Servers[emptyServer].OutTime = TimeIn[i] + WorkTime[i]
        else:
            isOutTimeBeforeTimeIn = False
            for k in range(len(Servers)):
                if Servers[k].OutTime < TimeIn:
                    isOutTimeBeforeTimeIn = True
                    if len(buffer) > 0:
                        buffer.pop(0)
            
            if isOutTimeBeforeTimeIn == False:
                if len(buffer) < bufferSize:
                    buffer.append(Buff())
                    buffer[-1].WorkTime = WorkTime[i]
                    for k in range(len(buffer)):
                        if k == 0:
                            buffer[k].TimeIn = TimeIn[i]
                            #TimeWithoutBuffer +=  TimeIn[i] - TODO - не очень понятно как отсчитывать время начала работы без буффера
                        else:
                            buffer[k].TimeIn = TimeIn[i]
                            buffer[k - 1].TimeOut = buffer[k].TimeIn
                            buffer[k - 1].BufferTime += buffer[k - 1].TimeOut - buffer[k - 1].TimeIn
                
                
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