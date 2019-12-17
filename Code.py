import random
from tkinter import *
import math

def detect(event):
        data = event.widget.get()
        if not data.isdigit() and data != '':
            result = ''
            for i in event.widget.get():
                if i.isdigit() or i == ".":
                    result += i
                
            event.widget.delete(0, END)
            event.widget.insert(0, result)

# линейный распределенный закон для T = (Tmax - Tmin) * x[i] - Tmin
def getTimeLinar(Tmin, Tmax, randNum):
    "linear distribution law for time"
    T = (Tmax - Tmin) * randNum + Tmin
    #print(f'rand number = {randNum}')
    return T

def getTimeExpon(lamb, randNum):
    x = -(math.log(randNum) / lamb)
    return x

def getTimeExponWork(tobr, randNum):
    T = round (1 / tobr, 3)
    T = getTimeExpon(T, randNum)
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

def colculation(simulation_time, Tzmin, Tzmax, Tsmin, Tsmax, ServersCount, bufferSize, var_dis, lamb, tobr):
    "функция расчета"
    #   время прихода программ
    TimeIn = []
    
    #   время обработки программ
    WorkTime = []
    if var_dis.get() == 0:
        TimeIn.append(round(getTimeLinar(Tzmin, Tzmax, random.random()), 3))
        WorkTime.append(round(getTimeLinar(Tsmin, Tsmax, random.random()), 3))
        
        while TimeIn[-1]< simulation_time:
            TimeIn.append(round(getTimeLinar(Tzmin, Tzmax, random.random()) + TimeIn[-1], 3))
            WorkTime.append(round(getTimeLinar(Tsmin, Tsmax, random.random()), 3))
    else:
        TimeIn.append(round(getTimeExpon(lamb, random.random()), 3))
        WorkTime.append(round(getTimeExponWork(tobr, random.random()), 3))
        
        while TimeIn[-1]< simulation_time:
            TimeIn.append(round(getTimeExpon(lamb, random.random()) + TimeIn[-1], 3))
            WorkTime.append(round(getTimeExponWork(tobr, random.random()), 3))

    
    #не превышаем время симуляции TODO
    #TimeIn.pop(-1)
    #WorkTime.pop(-1)

    print(f'len = {len(TimeIn)}')
    print(TimeIn)
    print("===============")
    print(WorkTime)
    wtCheck = 0
    for u in range(len(WorkTime)):
        wtCheck += WorkTime[u]
    print (f"======================>{wtCheck / len(WorkTime)}")

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
    TimeFreeSystem_begin = 0
    #   счетчик программ не обработанные Вычислительной Системой
    leaveProg = 0
    AllServersAreFree = True
    TimeProgInCS = []
    #======================================#
    #   основной цикл внутри симмуляции    #
    #======================================#
    for i in range(len(TimeIn)):
        currentTime = TimeIn[i]
        emptyServer = -1 # if -1 then all servers are busy
        isOneServerFree = False 
        
        for j in range(len(Servers)):
            if Servers[j].EmploymentStatus == 'free':
                if isOneServerFree == True:
                    continue
                emptyServer = j
                isOneServerFree = True
            else:
                AllServersAreFree = False
        
        #   Корректный расчет времени простоя системы        
        if AllServersAreFree == True:
            TimeFreeSystem += TimeIn[i] - TimeFreeSystem_begin
        
        if emptyServer != -1 and isOneServerFree:    

            t = getCurrentCountWorksServer(Servers) - 1

            if t >= 0:
                sameTimeServersWork[t] += round(TimeIn[i] - sameTimeServersWork_begin[t] ,3 )

            Servers[emptyServer].EmploymentStatus = 'busy'
            Servers[emptyServer].InTime = round(TimeIn[i] , 3)
            Servers[emptyServer].workTime = round(WorkTime[i] , 3)
            Servers[emptyServer].OutTime = round(Servers[emptyServer].InTime + Servers[emptyServer].workTime , 3)
            Servers[emptyServer].procCount += 1

            TimeProgInCS.append(round(WorkTime[i],3)) 
            
            sameTimeServersWork_begin[getCurrentCountWorksServer(Servers) - 1] = round(TimeIn[i] , 3)
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
                        TimeProgInCS.append(round(TimeIn[i] - getBuff.TimeIn + getBuff.WorkTime,3))

                        if len(buffer) == 0:
                            sameTimeServersWork_begin[getCurrentCountWorksServer(Servers) - 1] = round(Servers[j].OutTime , 3)
                        
                        TimeBuffersWork[len(buffer)] += round(Servers[j].OutTime - TimeBuffersWork_begin[len(buffer)], 3)

                        if len(buffer) > 0:
                            TimeBuffersWork_begin[len(buffer) - 1] = round(Servers[j].OutTime, 3)
                        else:
                            TimeFreeSystem_begin = Servers[j].OutTime
                            

                        Servers[j].InTime = round(Servers[j].OutTime, 3)
                        Servers[j].EmploymentStatus = 'busy'
                        Servers[j].workTime = round(getBuff.WorkTime , 3)
                        Servers[j].OutTime = round(Servers[j].InTime + Servers[j].workTime , 3)
                        Servers[j].procCount += 1
                        
                    else:
                        sameTimeServersWork[getCurrentCountWorksServer(Servers) - 1] += round(Servers[j].OutTime - sameTimeServersWork_begin[getCurrentCountWorksServer(Servers) - 1] , 3)
                        if busyFreeServer == False:

                            Servers[j].EmploymentStatus = 'free'
                            if getCurrentCountWorksServer(Servers) == 0:
                                TimeFreeSystem += TimeIn[i] - Servers[j].OutTime 

                            sameTimeServersWork[getCurrentCountWorksServer(Servers) - 2] += round(TimeIn[i] - Servers[j].OutTime, 3)
                            Servers[j].InTime = round( TimeIn[i] , 3)
                            Servers[j].workTime = round(WorkTime[i], 3)
                            Servers[j].EmploymentStatus = 'busy'
                            Servers[j].OutTime = round(Servers[j].InTime + Servers[j].workTime, 3)
                            Servers[j].procCount += 1
                            busyFreeServer = True
                            sameTimeServersWork_begin[getCurrentCountWorksServer(Servers) - 1] = round(TimeIn[i], 3)

                        else:
                            Servers[j].EmploymentStatus = 'free'
                            Servers[j].ReleaseTime = Servers[j].OutTime
                            sameTimeServersWork_begin[getCurrentCountWorksServer(Servers) - 1] =round( Servers[j].OutTime, 3)
                            if getCurrentCountWorksServer(Servers) == 0:
                                TimeFreeSystem_begin = TimeIn[i]

            if isOutTimeBeforeTimeIn == False:
                if len(buffer) < bufferSize:
                    
                    buffer.append(Buff())
                    buffer[-1].TimeIn = TimeIn[i]
                    buffer[-1].WorkTime = WorkTime[i]

                    if len(buffer) == 1:
                        TimeBuffersWork_begin[0] = round(TimeIn[i], 3)
                        sameTimeServersWork[-1] += round(TimeIn[i] - sameTimeServersWork_begin[-1], 3)
                       
                    elif len(buffer) > 1:
                        TimeBuffersWork_begin[len(buffer) - 1] = round(TimeIn[i], 3)
                        TimeBuffersWork[len(buffer) - 2] += round(TimeIn[i] - TimeBuffersWork_begin[len(buffer) - 2], 3)
                    else:
                        for i in range(1000):
                            print('ERROR <= ОБРАТИ ВНИМАНИЕ') # не ну а вдруг
                else:
                    leaveProg += 1
                    TimeBuffersWork[len(buffer) - 1] += round(TimeIn[i] - TimeBuffersWork_begin[len(buffer) - 1],3)
                    TimeBuffersWork_begin[len(buffer) - 1] = round(TimeIn[i], 3)
                    TimeProgInCS.append(0)

            
    #======================================#
    #   основной цикл внутри симмуляции    #
    #======================================#

    #       p0              p1  ... pn (Server) pn+1 ... pm (buffer)
    return TimeFreeSystem, sameTimeServersWork, TimeBuffersWork,    Servers, TimeIn, leaveProg, TimeProgInCS

def JustDoIt():
    simulation_time = int(SimulationTime_Entry.get())
    Tzmin = float(Tzmin_Entry.get())
    Tzmax = float(Tzmax_Entry.get())
    Tsmin = int(Tsmin_Entry.get())
    Tsmax = int(Tsmax_Entry.get())
    ServersCount = int(CountServer_Entry.get())
    bufferSize = int(BufferSize_Entry.get())
    _var_dis = var_dis
    lamb = float(lamb_Entry.get())
    tobr = int(Tobr_Entry.get())
    
    output = colculation(simulation_time, Tzmin, Tzmax, Tsmin, Tsmax, ServersCount, bufferSize, _var_dis, lamb, tobr)
    p0 = output[0]
    pServer = output[1]
    pBuff = output[2]
    Server = output[3]
    AllProc = output[4]
    leaveProg = output[5]
    TimeProgInCS = output[6]

    print (p0)
    print (pServer)
    print (pBuff)
    print (f'TimeProgInCS = {len(TimeProgInCS)} len tin = {len(AllProc)}')
    for i in range(len(Server)):
        print(Server[i].procCount)

    p0 = round(p0 / simulation_time,7)               #   вероятность бездействия системы во время симуляции
    p1 = round(pServer[0] / simulation_time,3)       #   вероятность работы одного сервера 
    p2 = round(pServer[1] /simulation_time,3)       #   вероятность работы двух серверов
    p3 = round(pBuff[0] / simulation_time,6)         #   вероятность работы с одним 
    p4 = round(pBuff[1] / simulation_time,6)         #                        двумя
    p5 = round(pBuff[2] / simulation_time,6)         #                        тремя буфферами

    DoneProc = 0
    for i in range(len(Server)):
        DoneProc += Server[i].procCount

    Q = round(DoneProc / len(AllProc),3)            #   среднее кол-во программ обработанных серверами
    S = round(DoneProc / simulation_time,3)          #   абсолютная пропускная способность – среднее число программ, обработанных в единицу времени
    Potk = round(leaveProg / simulation_time,3)      #   вероятность отказа, т.е. того, что программа будет не обработанной

    K = 'TODO'                                      #  не уверен что так вычитывается данная вероятность (среднее число занятых серверов) TODO
    Nprog = 'TODO'                                  #  тоже не очень понятно (среднее число программ в ВС)                                TODO
    Tprog = round(sum(TimeProgInCS) / simulation_time, 3)    # Debug
    Nbuf = 'TODO'                                           # TODO

    AllTimeInBuffer = sum(pBuff)
    Tbuf =round( AllTimeInBuffer / simulation_time,3)

    outPutText = (f'p0 = {p0}\n' +
                f'p1 = {p1}\n' + 
                f'p2 = {p2}\n' +
                f'p3 = {p3}\n' + 
                f'p4 = {p4}\n' + 
                f'p5 = {p5}\n' + 
                f'sum P = {round(p1 + p2 + p3 + p4 + p5, 7) }\n' + 
                f'Q = {Q}\n' + 
                f'S = {S}\n' + 
                f'P отк = {Potk}\n' + 
                f'K = {K}\n' + 
                f'N прог = {Nprog}\n' +
                f'T прог = {Tprog}\n' + 
                f'N буф = {Nbuf}\n' +
                f'T буф = {Tbuf}')

    output_textField.delete(1.0,END)
    output_textField.insert(END,outPutText)
    pass

if __name__ == "__main__":
    root = Tk()
    
    var_dis = BooleanVar()
    var_dis.set(0) 
    
    #Left Frame
    left_frame = LabelFrame(root)

    SimulationTime_LabelFrame = LabelFrame(left_frame)
    SimulationTime_label = Label(SimulationTime_LabelFrame, text="Время симуляции (сек)")
    SimulationTime_label.pack(side=LEFT, padx=10, pady=10)
    SimulationTime_Entry = Entry(SimulationTime_LabelFrame)
    SimulationTime_Entry.bind("<Any-KeyRelease>", detect)
    SimulationTime_Entry.insert(END, 3600)
    SimulationTime_Entry.pack(side=RIGHT, padx=10, pady =10)
    SimulationTime_LabelFrame.pack(anchor=W, padx=10, pady=10, fill=X)

    CountServer_LabelFrame = LabelFrame(left_frame)
    CountServer_label = Label(CountServer_LabelFrame, text="Колличество серверов")
    CountServer_label.pack(side=LEFT, padx=10, pady=10)
    CountServer_Entry = Entry(CountServer_LabelFrame)
    CountServer_Entry.bind("<Any-KeyRelease>", detect)
    CountServer_Entry.insert(END, 2)
    CountServer_Entry.pack(side=RIGHT, padx=10, pady =10)
    CountServer_LabelFrame.pack(anchor=W, padx=10, pady=10, fill=X)

    BufferSize_LabelFrame = LabelFrame(left_frame)
    BufferSize_label = Label(BufferSize_LabelFrame, text="Размер буфера")
    BufferSize_label.pack(side=LEFT, padx=10, pady=10)
    BufferSize_Entry = Entry(BufferSize_LabelFrame)
    BufferSize_Entry.bind("<Any-KeyRelease>", detect)
    BufferSize_Entry.insert(END, 3)
    BufferSize_Entry.pack(side=RIGHT, padx=10, pady =10)
    BufferSize_LabelFrame.pack(anchor=W, padx=10, pady=10, fill=X)

    Exp_LabelFrame = LabelFrame(left_frame)
    lamb_label = Label(Exp_LabelFrame, text="Лямбда")
    lamb_label.pack(side=LEFT, padx=10, pady=10)
    lamb_Entry = Entry(Exp_LabelFrame)
    lamb_Entry.bind("<Any-KeyRelease>", detect)
    lamb_Entry.insert(END, 1.5)
    lamb_Entry.pack(side=LEFT, padx=10, pady =10)
    Tobr_label = Label(Exp_LabelFrame, text="Среднее время обработки")
    Tobr_label.pack(side=LEFT, padx=10, pady=10)
    Tobr_Entry = Entry(Exp_LabelFrame)
    Tobr_Entry.bind("<Any-KeyRelease>", detect)
    Tobr_Entry.insert(END, 2)
    Tobr_Entry.pack(side=RIGHT, padx=10, pady =10)
    Exp_LabelFrame.pack(anchor=W, padx=10, pady=10, fill=X)

    Tz_LabelFrame = LabelFrame(left_frame)
    Tzmin_label = Label(Tz_LabelFrame, text="Tz min ")
    Tzmin_label.pack(side=LEFT, padx=10, pady=10)
    Tzmin_Entry = Entry(Tz_LabelFrame)
    Tzmin_Entry.bind("<Any-KeyRelease>", detect)
    Tzmin_Entry.insert(END, 0.5)
    Tzmin_Entry.pack(side=LEFT, padx=10, pady =10)

    Tzmax_label = Label(Tz_LabelFrame, text="Tz max ")
    Tzmax_label.pack(side=LEFT, padx=10, pady=10)
    Tzmax_Entry = Entry(Tz_LabelFrame)
    Tzmax_Entry.bind("<Any-KeyRelease>", detect)
    Tzmax_Entry.insert(END, 0.833)
    Tzmax_Entry.pack(side=RIGHT, padx=10, pady =10)
    Tz_LabelFrame.pack(anchor=W, padx=10, pady=10, fill=X)

    Ts_LabelFrame = LabelFrame(left_frame)
    Tsmin_label = Label(Ts_LabelFrame, text="Tz min ")
    Tsmin_label.pack(side=LEFT, padx=10, pady=10)
    Tsmin_Entry = Entry(Ts_LabelFrame)
    Tsmin_Entry.bind("<Any-KeyRelease>", detect)
    Tsmin_Entry.insert(END, 1)
    Tsmin_Entry.pack(side=LEFT, padx=10, pady =10)

    Tsmax_label = Label(Ts_LabelFrame, text="Tz max ")
    Tsmax_label.pack(side=LEFT, padx=10, pady=10)
    Tsmax_Entry = Entry(Ts_LabelFrame)
    Tsmax_Entry.bind("<Any-KeyRelease>", detect)
    Tsmax_Entry.insert(END, 5)
    Tsmax_Entry.pack(side=RIGHT, padx=10, pady =10)
    Ts_LabelFrame.pack(anchor=W, padx=10, pady=10, fill=X)

    process_LabelFrame = LabelFrame(left_frame)
    learningStart_button = Button(process_LabelFrame, text="Начать симуляцию", command= JustDoIt)
    learningStart_button.pack(side=LEFT, padx=10, pady=10)
    
    process_LabelFrame.pack(side=BOTTOM, anchor=W, padx=10, pady=10, fill=X)

    
    Distribution_LabelFrame = LabelFrame(left_frame)
    DistributionLinar_label = Label(Distribution_LabelFrame, text="Линейное распределение")
    DistributionLinar_label.pack(side=LEFT, padx=10, pady=10)
    DistributionLinar_Radiobutton = Radiobutton(Distribution_LabelFrame, variable=var_dis, value = 0)
    DistributionLinar_Radiobutton.pack(side=LEFT, padx=10, pady =10)

    DistributionExp_label = Label(Distribution_LabelFrame, text="Экспоненциальноe распределение")
    DistributionExp_label.pack(side=LEFT, padx=10, pady=10)
    DistributionExp_Radiobutton = Radiobutton(Distribution_LabelFrame, variable=var_dis, value = 1)
    DistributionExp_Radiobutton.pack(side=RIGHT, padx=10, pady =10)
    Distribution_LabelFrame.pack(anchor=W, padx=10, pady=10, fill=X)

    left_frame.pack(side=LEFT, padx=5, pady=10, fill=Y)
    #Left Frame

    #Right Frame
    right_frame = LabelFrame(root)

    output_textField = Text(right_frame, height=40)
    output_textField.pack(padx=10, pady=10, side=TOP)

    right_frame.pack(side=RIGHT, padx=5, pady=10, fill=Y)
    #Right Frame
    

    root.mainloop()
    pass