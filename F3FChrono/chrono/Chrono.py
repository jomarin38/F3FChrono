from enum import Enum
import time


class chronoType(Enum):
    wire = 0
    wireless = 1
    none = 2

class chronoStatus(Enum):
    WaitLaunch=0
    Lunched=1
    InStart=2
    InProgress=3
    Finished=4

class chrono():
    def __init__(self):
        self.chronoLaunch = 30
        self.chronoFisrtBase = 30
        self.chronoRun = 0
        self.chronoLap=[]
        self.timelost=[]
        self.lastBaseChangeTime =0
        self.last10BasesTime = 0.0
        self.last10BasesTimeLost = 0.0
        self.lastBase=0
        self.inStart = False
        self.mode=chronoType.none.value

        print('Chrono F3F Initialisation ')

    def set_mode(self, mode):
        self.mode=mode

    def start(self):
        self.lastBaseChangeTime = time.time ()
        self.lastDetectionTime = self.lastBaseChangeTime
        return 0
        
    def reset(self):
        self.last10BasesTime = 0.0
        self.last10BasesTimeLost = 0.0
        self.chronoLap.clear()
        self.timelost.clear()
        
    def startRace(self):
        self.last10BasesTime = 0.0
        self.last10BasesTimelost = 0.0
        self.inStart = True
        self.lastBase = -1
        self.chronoLap.clear()
        self.timelost.clear()
        
    def isInStart (self):
        return self.inStart
    
    
    def declareBase (self, base):
        now = time.time ();
        if (self.inStart):
            self.lastBaseChangeTime = now;
            self.last10BasesTime = 0.0;
            self.last10BasesTimelost = 0.0;
            self.chronoLap.clear();
            self.timelost.clear();
            self.inStart = False;

        if (base!=self.lastBase):
            elapsedTime = ((now- self.lastBaseChangeTime));
            self.lastBaseChangeTime = now;
            self.lastDetectionTime = now;
            if (self.getLapCount()>1):
                self.last10BasesTimeLost += self.timelost[self.getLapCount() - 1]
            
            self.chronoLap.append(elapsedTime);
            self.timelost.append(0.0);
            self.last10BasesTime+=elapsedTime;
            print (self.getLapCount())
            if (self.getLapCount()>10):
                self.last10BasesTime-= self.chronoLap[self.getLapCount()-11]
                self.last10BasesTimeLost-=self.timelost[self.getLapCount()-11]
            
            self.lastBase =base;
            return True;
        elif (self.getLapCount()>1):#Base declaration is the same
                elapsedTime = ((now - self.lastDetectionTime));
                self.lastDetectionTime = now;
                self.timelost[self.getLapCount() - 1] = self.timelost[self.getLapCount() - 1] + elapsedTime

        return False;

    def getLast10BasesTime(self):
        return self.last10BasesTime;
    
    def getLast10BasesLostTime(self):
        return self.last10BasesTimeLost;

    def getLastLapTime(self):
        if self.getLapCount()>0:
            return self.chronoLap[self.getLapCount()-1]
        else:
            return 0
    
    def getLapCount(self):
        return len(self.chronoLap)
    
if __name__ == '__main__':
    print ('Chrono Test')
    Chrono = chrono(chronoMode.Practice)
    Chrono.reset ()
    Chrono.startRace ()
    print (Chrono.getLapCount ())
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