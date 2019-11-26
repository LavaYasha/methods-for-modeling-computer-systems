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
        #self.downTime = 0
        self.workTime = 0
        self.procCount = 0
        self.InTime = 0
        self.OutTime = 0
        self.ReleaseTime = 0

class Buff(object):
    def __init__(self):
        self.TimeIn = 0
        self.TimeOut = 0
        self.WorkTime = 0

def getCurrentCountWorksServer(Servers):
    count = 0
    for i in range(len(Servers)):
        if Servers[i].EmploymentStatus == 'busy':
            count += 1
    
    return count

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
    #Current_time = TimeIn[0]

    #   Инициализация серверов
    Servers = []
    for k in range(ServersCount):
        Servers.append(Server())
        #Servers[k].downTime += TimeIn[0]

    sameTimeServersWork = [0 for i in range(ServersCount)]
    sameTimeServersWork_begin = [0 for i in range(ServersCount)]
    #  Инициализация буфера
    buffer = []
    TimeBuffersWork = [0 for i in range(bufferSize)]
    TimeBuffersWork_begin = [0 for i in range(bufferSize)]

    #   Флаг работы серверов
    #isWork = False

    #   Время простоя всей системы
    TimeFreeSystem = 0

    #   счетчик программ не обработанные Вычислительной Системой
    leaveProg = 0
    AllServersAreFree = True

    #======================================#
    #   основной цикл внутри симмуляции    #
    #======================================#
    for i in range(len(TimeIn)):
        
        emptyServer = -1 # if -1 then all servers are busy
        isOneServerFree = False 
        
        for j in range(len(Servers)):
            if Servers[j].EmploymentStatus == 'free':
                emptyServer = j
                isOneServerFree = True
                break
        
        if emptyServer != -1 and isOneServerFree:
            
            t = getCurrentCountWorksServer(Servers) - 1
            #while t < getCurrentCountWorksServer(Servers):
            sameTimeServersWork[t] += TimeIn[i] - sameTimeServersWork_begin[t]
                # t += 1

            Servers[emptyServer].EmploymentStatus = 'busy'
            Servers[emptyServer].InTime = TimeIn[i]
            Servers[emptyServer].workTime = WorkTime[i]
            Servers[emptyServer].OutTime = Servers[emptyServer].InTime + Servers[emptyServer].workTime
            Servers[emptyServer].procCount += 1

            sameTimeServersWork_begin[getCurrentCountWorksServer(Servers) - 1] = TimeIn[i]
        else:
            #   если ко времени прихода программы какие то сервера закончат обработку предыдущих программ
            #   то либо забираем первую в очереди на обработку программу из буффера 
            #   либо включаем таймер бездействия
            isOutTimeBeforeTimeIn = False
            busyFreeServer = False
            for j in range(len(Servers)):
                if Servers[j].OutTime < TimeIn[i]:
                    isOutTimeBeforeTimeIn = True
                    if len(buffer) > 0:
                        getBuff = buffer.pop(0)
                        Servers[j].InTime = Servers[j].OutTime
                        Servers[j].EmploymentStatus = 'busy'
                        Servers[j].workTime = getBuff.WorkTime
                        Servers[j].OutTime = Servers[j].InTime + Servers[j].workTime
                        Servers[j].procCount += 1

                        sameTimeServersWork_begin[getCurrentCountWorksServer(Servers) - 1] = Servers[j].OutTime

                        if len(buffer) == bufferSize - 1:
                            TimeBuffersWork_begin[len(buffer) - 2] = Servers[j].OutTime
                        elif len(buffer) < bufferSize - 1:
                            TimeBuffersWork_begin[len(buffer) - 1] = Servers[j].OutTime
                            TimeBuffersWork[len(buffer)] = TimeIn[i] - TimeBuffersWork_begin[len(buffer)]
                    else:
                        sameTimeServersWork[getCurrentCountWorksServer(Servers) - 1] += Servers[j].OutTime - sameTimeServersWork_begin[getCurrentCountWorksServer(Servers) - 1]
                        if busyFreeServer == False:

                            Servers[j].EmploymentStatus = 'free'
                            if getCurrentCountWorksServer(Servers) == 0:
                                TimeFreeSystem += TimeIn[i] - Servers[j].OutTime 

                            sameTimeServersWork[getCurrentCountWorksServer(Servers) - 2] += TimeIn[i] - Servers[j].OutTime
                            Servers[j].InTime = TimeIn[i] 
                            Servers[j].workTime = WorkTime[i]
                            Servers[j].EmploymentStatus = 'busy'
                            Servers[j].OutTime = Servers[j].InTime + Servers[j].workTime
                            Servers[j].procCount += 1
                            busyFreeServer = True
                            sameTimeServersWork_begin[getCurrentCountWorksServer(Servers) - 1] = TimeIn[i]

                        else:
                            Servers[j].EmploymentStatus = 'free'
                            Servers[j].ReleaseTime = Servers[j].OutTime
                            sameTimeServersWork_begin[getCurrentCountWorksServer(Servers) - 1] = Servers[j].OutTime

            if isOutTimeBeforeTimeIn == False:
                if len(buffer) < bufferSize:
                    buffer.append(Buff())
                
                    if len(buffer) == 1:
                        TimeBuffersWork_begin[0] = TimeIn[i]
                        sameTimeServersWork[-1] += TimeIn[i] - sameTimeServersWork_begin[-1]
                    else:
                        TimeBuffersWork_begin[len(buffer) - 1] = TimeIn[i]
                        TimeBuffersWork[len(buffer) - 2] = TimeIn[i] - TimeBuffersWork_begin[len(buffer) - 2]
                else:
                    leaveProg += 1
                    TimeBuffersWork[len(buffer) - 1] = TimeIn[i] - TimeBuffersWork_begin[len(buffer) - 1]

    #======================================#
    #   основной цикл внутри симмуляции    #
    #======================================#

    #       p0              p1  ... pn (Server) pn+1 ... pm (buffer)
    return TimeFreeSystem, sameTimeServersWork, TimeBuffersWork,    Servers


if __name__ == "__main__":
    #   время симуляции впоследствии можно будет задать в часовом диапозоне
    SimulationTime = 60 * 60 

    #   время прихода программы (линейный закон)
    Tzmin = 1 / 2
    Tzmax = 5 / 6

    #  время обработки программы сервером программы (линейный закон)
    Tsmin = 1
    Tsmax = 5

    output = colculation(SimulationTime, Tzmin, Tzmax, Tsmin, Tsmax, 2, 3)
    p0 = output[0]
    pServer = output[1]
    pBuff = output[2]
    Server = output[3]

    print (p0)
    print (pServer)
    print (pBuff)
    for i in range(len(Server)):
        print(Server[i].procCount)

    p0 = p0 / SimulationTime
    p1 = pServer[0] / SimulationTime
    p2 = pServer[1] / SimulationTime
    p3 = pBuff[0] / SimulationTime
    p4 = pBuff[1] / SimulationTime
    p5 = pBuff[2] / SimulationTime


    print('===')
    print(f'p0 = {p0}, p1 = {p1}, p2 = {p2}, p3 = {p3}, p4 = {p4}, p5 = {p5}, sum P = {p1 + p2 + p3 + p4 + p5}')
    pass