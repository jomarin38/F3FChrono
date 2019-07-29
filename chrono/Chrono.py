from enum import Enum
import time


class chronoMode (Enum):
    Test=0
    Run=1
    Practice=2

class chrono():
    def __init__ (self, mode):
        if mode==chronoMode.Test:
            self.chronoLaunch = -1
            self.chronoFisrtBase = -1
            self.chronoRun = -1
        elif mode==chronoMode.Run:
            self.chronoLaunch = 30
            self.chronoFisrtBase = 30
            self.chronoRun = 0
        elif mode==chronoMode.Practice:
            self.chronoLaunch = -1
            self.chronoFisrtBase = -1
            self.chronoRun = 0
        else:
            self.chronoLaunch = -1
            self.chronoFisrtBase = -1
            self.chronoRun = -1
            
        self.chronoLap=[]
        self.timelost=[]
        self.lastBaseChangeTime =0
        self.last10BasesTime = 0.0
        self.last10BasesTimeLost = 0.0
        self.lastBase=0
        self.inStart = False
        
        print ('F3F Initialisation ', mode)
        return None;
    
    def start (self, mode):
        self.lastBaseChangeTime = time.time ()
        self.lastDetectionTime = self.lastBaseChangeTime
        return 0
        
    def reset (self):
        self.last10BasesTime = 0.0
        self.last10BasesTimeLost = 0.0
        self.chronoLap.clear ()
        self.timelost.clear ()
        
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

    