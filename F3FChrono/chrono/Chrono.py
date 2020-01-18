import time
import os
from datetime import datetime


class chronoType():
    wire = 0
    wireless = 1
    none = 2

class chronoStatus():
    InWait=0
    WaitLaunch=1
    Launched=2
    InStart=3
    InProgress=4
    Finished=5

class ChronoRpi(ChronoHard):
    def __init__(self):
        self.chronoLaunch = 30
        self.chronoFisrtBase = 30
        self.startTime=None
        self.endTime=None
        self.chronoLap=[]
        self.timelost=[]
        self.lastBaseChangeTime =0
        self.last10BasesTime = 0.0
        self.last10BasesTimeLost = 0.0
        self.lastBase=0
        self.inStart = False
        self.mode=chronoType.none
        self.status=chronoStatus.InWait


        print('Chrono F3F Initialisation ')

    def set_mode(self, mode):
        self.mode=mode

    def get_status(self):
        return self.status

    def next_status(self):
        if (self.status<chronoStatus.Finished):
            self.status=self.status+1
        return self.status

    def set_status(self, value):
        self.status=value
        return self.status
    def start(self):
        self.lastBaseChangeTime = time.time ()
        self.lastDetectionTime = self.lastBaseChangeTime
        return 0
        
    def reset(self):
        self.last10BasesTime = 0.0
        self.last10BasesTimeLost = 0.0
        self.chronoLap.clear()
        self.timelost.clear()
        self.status=chronoStatus.InWait
        self.penalty=0.0

    def startRace(self):
        self.last10BasesTime = 0.0
        self.last10BasesTimelost = 0.0
        self.inStart = True
        self.lastBase = -10
        self.chronoLap.clear()
        self.timelost.clear()
        
    def isInStart (self):
        return self.inStart
    
    def declareBase (self, base):
        now = time.time()
        if (self.status==chronoStatus.InStart):
            self.lastBaseChangeTime = now
            self.startTime=datetime.now()
            self.last10BasesTime = 0.0
            self.last10BasesTimelost = 0.0
            self.chronoLap.clear()
            self.timelost.clear()
            self.inStart = False

        if (self.status==chronoStatus.InStart or self.status==chronoStatus.InProgress and base!=self.lastBase or base=="btnnext"):
            elapsedTime = ((now- self.lastBaseChangeTime))
            self.lastBaseChangeTime = now
            self.lastDetectionTime = now
            #print("chrono status : "+str(self.status)+", Nb Lap : "+str(self.getLapCount()))
            if (self.getLapCount()>1):
                self.last10BasesTimeLost += self.timelost[self.getLapCount() - 1]
            
            if (self.status!=chronoStatus.InStart):
                self.chronoLap.append(elapsedTime)
                self.timelost.append(0.0)
            self.last10BasesTime+=elapsedTime
            if (self.getLapCount()>10):
                self.last10BasesTime-= self.chronoLap[self.getLapCount()-11]
                self.last10BasesTimeLost-=self.timelost[self.getLapCount()-11]

            if (self.getLapCount()==10):
                self.endTime=datetime.now()

            if self.status==chronoStatus.InStart:
                self.lastBase = ""
            else:
                self.lastBase = base
            return True
        elif (self.getLapCount()>1):#Base declaration is the same
                elapsedTime = ((now - self.lastDetectionTime))
                self.lastDetectionTime = now;
                self.timelost[self.getLapCount() - 1] = self.timelost[self.getLapCount() - 1] + elapsedTime

        return False

    def getLast10BasesTime(self):
        return self.last10BasesTime
    
    def getLast10BasesLostTime(self):
        return self.last10BasesTimeLost

    def getLastLapTime(self):
        if self.getLapCount()>0:
            return self.chronoLap[self.getLapCount()-1]
        else:
            return 0

    def get_time(self):
        time=0
        for i in range(self.getLapCount()):
            time=time+self.chronoLap[i]
        return time

    def getLaps(self):
        return (self.chronoLap)

    def getStartTime(self):
        return (self.startTime)

    def getEndTime(self):
        return (self.endTime)

    def getLapCount(self):
        return len(self.chronoLap)



    def getMaxWindSpeed(self):
        return None

    def getMinWindSpeed(self):
        return None

    def getWindDir(self):
        return None

    def to_string(self):
        result=os.linesep+"Chrono Data : "+os.linesep+"\tStart Time : "+ str(self.startTime)+\
               os.linesep+"\tEnd Time : "+str(self.endTime)+os.linesep+"\tRun Time : "+\
               "{:0>6.3f}".format(self.get_time())+os.linesep+"\tLapTime : "
        for lap in self.getLaps():
            result+="{:0>6.3f}".format(lap)+","
        result+=os.linesep+"\tPenalty : "+str(self.penalty)+os.linesep
        return (result)

class ChronoArduino(ChronoHard):
    def __init__(self):

    def reset(self):

    def get_status(self):

    def set_status(self):


class ChronoHard():
    def __init__(self):
        self.penalty = 0.0

    def reset(self):

    def addPenalty(self, value):
        self.penalty += value
        return (self.penalty)

    def clearPenalty(self):
        self.penalty=0.0
        return (self.penalty)

    def getPenalty(self):
        return (self.penalty)

    def getStatus(self):

    def set_status(self, status):

    def next_status(self):



if __name__ == '__main__':
    print ('Chrono Test')
    Chrono = ChronoHard()
    Chrono.reset ()
    Chrono.startRace ()
    Chrono.next_status()
    Chrono.next_status()
    Chrono.next_status()

    print(Chrono.getLapCount ())
    Chrono.declareBase (1)
    time.sleep(0.5)
    Chrono.declareBase (2)
    time.sleep(0.1)
    Chrono.declareBase (2)
    time.sleep(0.5)
    Chrono.declareBase (1)
    time.sleep (0.5)
    Chrono.declareBase (2)
    print ('Numero de base : ', Chrono.getLapCount ())
    print ('Last Lap : ', Chrono.getLastLapTime ())
    print ('10LastLap : ', Chrono.getLast10BasesTime())
    print ('10LastLapLost : ', Chrono.getLast10BasesLostTime())
    print(Chrono.to_string())