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

    #   Флаг работы серверов
    #isWork = False

    #   Время простоя всей системы
    TimeFreeSystem = 0

    #   Время без использования буфера
    TimeWithoutBuffer = 0
    TimeWithoutBuffer_begin = 0

    #   счетчик программ не обработанные Вычислительной Системой
    leaveProg = 0
    AllServersAreFree = True

    #======================================#
    #   основной цикл внутри симмуляции    #
    #======================================#
    for i in range(len(TimeIn)):
        
        emptyServer = -1 # if -1 then all servers are busy
        isOneServerFree = False 

        if AllServersAreFree == True:
            if i > 0:
                TimeFreeSystem += TimeIn[i] - TimeIn[i - 1]
            else:
                TimeFreeSystem += TimeIn[i]

        workServersCount = 0
        for j in range(len(Servers)):
            if Servers[j].EmploymentStatus == 'free':
                isOneServerFree = True
                emptyServer = j 
                break
            else:
                workServersCount += 1

        if (isOneServerFree) and (emptyServer != -1):

            AllServersAreFree = False

            Servers[emptyServer].EmploymentStatus = 'busy'
            Servers[emptyServer].InTime = TimeIn[i]
            Servers[emptyServer].workTime = WorkTime[i]
            Servers[emptyServer].OutTime = TimeIn[i] + WorkTime[i]
            Servers[emptyServer].procCount += 1

            workServersCount = 0
            for j in range(len(Servers)):
                if Servers[j].EmploymentStatus == 'busy':
                    workServersCount += 1
            
            sameTimeServersWork_begin[workServersCount - 1] = TimeIn[i]
            if workServersCount - 2 >= 0:
                sameTimeServersWork[workServersCount - 2] += TimeIn[i] - sameTimeServersWork_begin[workServersCount - 2] 

            if TimeWithoutBuffer_begin == 0:
                TimeWithoutBuffer_begin = TimeIn[i]
        else:
            #   если ко времени прихода программы какие то сервера закончат обработку предыдущих программ
            #   то либо забираем первую в очереди на обработку программу из буффера 
            #   либо включаем таймер бездействия
            isOutTimeBeforeTimeIn = False
            for k in range(len(Servers)):
                if Servers[k].OutTime < TimeIn[i]:
                    isOutTimeBeforeTimeIn = True
                    #   если севрер освободился и в буфере есть программа, 
                    #   забираем программу из буффера в свободный сервер
                    if len(buffer) > 0:
                        
                        TimeBuffersWork[len(buffer)-1] += Servers[k].OutTime - buffer[-1].TimeIn   
                        
                        takedBuffer = buffer.pop(0)
                        Servers[k].EmploymentStatus = 'busy'
                        Servers[k].workTime = takedBuffer.WorkTime
                        Servers[k].InTime =  Servers[k].OutTime
                        Servers[k].OutTime = Servers[k].InTime + Servers[k].workTime
                        Servers[k].procCount += 1

                    #   если сервер освободился и в буффере нет программ,
                    #   устанавливаем статус сервера в "свободен" и включаем счетчик простоя
                    else:
                        workServersCount = 0 
                        for j in range(len(Servers)):
                            if Servers[j].EmploymentStatus == 'busy':
                                workServersCount += 1
                            if workServersCount - 1 >= 0:
                                sameTimeServersWork[workServersCount - 1] += TimeIn[i] - sameTimeServersWork_begin[workServersCount - 1] 
                        Servers[k].EmploymentStatus = 'free'
                        Servers[k].ReleaseTime = Servers[k].OutTime

            workServersCount = 0
            for j in range(len(Servers)):
                if Servers[j].EmploymentStatus == 'busy':
                    workServersCount += 1


            AllServersAreFree = True
            for g in range(len(Servers)):
                if Servers[g].EmploymentStatus == 'busy':
                    AllServersAreFree = False

            if AllServersAreFree == True:
                MaxOutTime = 0
                for g in range(len(Servers)):
                    if Servers[g].OutTime > MaxOutTime:
                        MaxOutTime = Servers[g].OutTime
                TimeFreeSystem += TimeIn[i] - MaxOutTime

            #   если все сервера в работе мы добавляем программу в буффер 
            #   (если все буфферы заняты программа не обрабатывается)
            if isOutTimeBeforeTimeIn == False:

                if len(buffer) == 0:
                    workServersCount = 0
                    for j in range(len(Servers)):
                        if Servers[j].EmploymentStatus == 'busy':
                            workServersCount += 1
                    if workServersCount - 1 >= 0:
                        sameTimeServersWork[workServersCount - 1] += TimeIn[i] - sameTimeServersWork_begin[workServersCount - 1] 
                
                
                sameTimeServersWork_begin[workServersCount - 1] = TimeIn[i]  

                if len(buffer) < bufferSize:
                    buffer.append(Buff())
                    buffer[-1].WorkTime = WorkTime[i]
                    buffer[-1].TimeIn = TimeIn[i]
                    if len(buffer) == 1:
                        TimeWithoutBuffer += TimeIn[i] - TimeWithoutBuffer_begin
                        TimeWithoutBuffer_begin = 0
                    
                
                else:
                    leaveProg += 1
                    continue
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