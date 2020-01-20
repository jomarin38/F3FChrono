import time
import os
from datetime import datetime
from PyQt5.QtCore import pyqtSignal, QObject, QTimer

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

class ChronoHard(QObject):
    status_changed = pyqtSignal(int)
    lap_finished = pyqtSignal(int, float)
    run_finished = pyqtSignal(float)
    chrono_signal = pyqtSignal(str, str, str)

    def __init__(self):
        super().__init__()
        self.penalty = 0.0
        self.chronoLaunch = 30
        self.chronoFisrtBase = 30
        self.startTime=None
        self.endTime=None

    def reset(self):
        print("reset")

    def addPenalty(self, value):
        self.penalty += value
        return (self.penalty)

    def clearPenalty(self):
        self.penalty=0.0
        return (self.penalty)

    def getPenalty(self):
        return (self.penalty)

    def get_status(self):
        print("getstatus")

    def set_status(self, status):
        print("setstatus")


    def wind_info(self):
        print("wind_info")

class ChronoRpi(ChronoHard):
    def __init__(self):
        super().__init__()
        self.chronoLap=[]
        self.timelost=[]
        self.lastBase=-2
        self.status=chronoStatus.InWait
        self.chrono_signal.connect(self.handle_chrono_event)

    def get_status(self):
        return self.status

    def set_status(self, value):
        self.status=value
        return self.status

    def reset(self):
        self.chronoLap.clear()
        self.timelost.clear()
        self.status=chronoStatus.InWait
        self.lastBase=-2
        self.penalty=0.0

    def handle_chrono_event(self, caller, data, address):
        print("handle_chrono_event")

    @staticmethod
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
        super().__init__()
        print ("chronoArduino init")

    def reset(self):
        print ("chronoArduino reset")

    def get_status(self):
        print ("chronoArduino get_status")

    def set_status(self):
        print ("chronoArduino set_status")

def main ():

    print ('Chrono Test')
    chronoRpi=ChronoRpi()
    chronoRpi.reset()
    chronoRpi.chrono_signal.emit("test","test1","test2")


if __name__ == '__main__':
    main()
