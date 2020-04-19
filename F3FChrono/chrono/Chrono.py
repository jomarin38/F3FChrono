import time
import os
from datetime import datetime
import collections
from PyQt5.QtCore import pyqtSignal, QObject, QTimer
from F3FChrono.chrono.UDPBeep import *
from F3FChrono.chrono.UDPReceive import *
from F3FChrono.chrono import ConfigReader
from F3FChrono.chrono.rs232_arduino import rs232_arduino

IPUDPBEEP = '255.255.255.255'
UDPPORT = 4445

class chronoType():
    wire = 0
    wireless = 1
    none = 2

class chronoStatus():
    InWait = 0
    WaitLaunch = 1
    Launched = 2
    InStart = 3
    InProgressA = 4
    InProgressB = 5
    WaitAltitude = 6
    Finished = 7

class ChronoHard(QObject):
    status_changed = pyqtSignal(int)
    run_started = pyqtSignal()
    lap_finished = pyqtSignal(int, float)
    run_finished = pyqtSignal(float)
    run_validated = pyqtSignal()
    buzzer_validated = pyqtSignal()
    chrono_signal = pyqtSignal(str, str, str)
    wind_signal = pyqtSignal(int, int, bool)
    accu_signal = pyqtSignal(float)
    rssi_signal = pyqtSignal(int, int)
    altitude_finished = pyqtSignal()
    
    def __init__(self, signal_btnnext):
        super().__init__()
        self.penalty = 0.0
        self.startTime=None
        self.endTime=None
        self.signal_btnnext=signal_btnnext
        self.wind_signal.connect(self.wind_info)
        self.wind= collections.OrderedDict()
        self.reset_wind()
        self.chronoLap = []
        self.timelost = []


    def addPenalty(self, value):
        self.penalty += value
        return (self.penalty)

    def clearPenalty(self):
        self.penalty=0.0
        return (self.penalty)

    def getPenalty(self):
        return (self.penalty)

    def wind_info(self, speed, orientation, rain):
        print("wind_info")
        self.wind['speed_nb']+=1
        self.wind['speed_sum']+=speed

        if speed<self.wind['speed_min']:
            self.wind['speed_min']=speed
        if speed>self.wind['speed_max']:
            self.wind['speed_max'] = speed

        self.wind['orientation_sum']+=orientation
        self.wind['orientation_nb']+=1
        if rain:
            self.wind['rain']=True

    def getMaxWindSpeed(self):
        return self.wind['speed_max']

    def getMinWindSpeed(self):
        return self.wind['speed_min']

    def getMeanWindSpeed(self):
        if (self.wind['speed_nb']!=0):
            return self.wind['speed_sum']/self.wind['speed_nb']
        else:
            return 0

    def getWindDir(self):
        if (self.wind['orientation_nb']!=0):
            return self.wind['orientation_sum']/self.wind['orientation_nb']
        else:
            return 0

    def getRain(self):
        return self.wind['rain']

    def reset_wind(self):
        self.wind['speed_sum'] = 0
        self.wind['speed_nb'] = 0
        self.wind['speed_min']=0
        self.wind['speed_max']=0
        self.wind['orientation_sum']=0
        self.wind['orientation_nb']=0

        self.wind['rain']=False

    def get_status(self):
        return self.status

    def set_status(self, value):
        if (self.status!=value):
            self.status=value
            self.status_changed.emit(self.get_status())
        return self.status

    def reset(self):
        self.chronoLap.clear()
        self.timelost.clear()
        self.set_status(chronoStatus.InWait)
        self.lastBase=-2
        self.penalty=0.0
        self.reset_wind()






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
        return self.chronoLap

    def getStartTime(self):
        return self.startTime

    def getEndTime(self):
        return self.endTime

    def getLapCount(self):
        return len(self.chronoLap)

    def to_string(self):
        result=os.linesep+"Chrono Data : "+os.linesep+"\tStart Time : "+ str(self.startTime)+\
               os.linesep+"\tEnd Time : "+str(self.endTime)+os.linesep+"\tRun Time : "+\
               "{:0>6.3f}".format(self.get_time())+os.linesep+"\tLapTime : "
        for lap in self.getLaps():
            result+="{:0>6.3f}".format(lap)+","
        result+=os.linesep+"\tPenalty : "+str(self.penalty)+os.linesep
        result+="Wind Speed :"+os.linesep+"\tMean : "+"{:0>6.1f}".format(self.getMeanWindSpeed())+os.linesep+\
                "\tMin : "+"{:0>6.1f}".format(self.getMinWindSpeed())+os.linesep+\
                "\tMax : " + "{:0>6.1f}".format(self.getMaxWindSpeed()) + os.linesep +\
                "Wind Orientation : " + "{:0>6.1f}".format(self.getMaxWindSpeed()) + os.linesep +\
                "rain : " + str(self.getRain()) + os.linesep
        return (result)




class ChronoRpi(ChronoHard):
    def __init__(self, signal_btnnext):
        super().__init__(signal_btnnext)
        self.lastBase = -2
        self.lastBaseChangeTime = 0.0
        self.lastDetectionTime = 0.0
        self.status = chronoStatus.InWait
        self.startAltitude = 0.0
        self.chrono_signal.connect(self.handle_chrono_event)
        self.udpReceive = udpreceive(UDPPORT, self.chrono_signal, self.signal_btnnext, self.wind_signal, self.accu_signal, self.rssi_signal)
        self.udpBeep = udpbeep(IPUDPBEEP, UDPPORT)
        self.timer = QTimer()
        self.timer.timeout.connect(self.timerEvent)
        self.status=0
        self.status_changed.connect(self.slot_status)

    def __del__(self):
        self.udpBeep.terminate()
        del self.udpBeep
        del self.udpReceive

    def handle_chrono_event(self, caller, data, address):
        if not caller.lower() == "btnnext" and not self.status == chronoStatus.InProgressA \
                and not self.status == chronoStatus.InProgressB:
            self.buzzer_validated.emit()
        if ((self.status == chronoStatus.Launched or self.status == chronoStatus.InStart or
             self.status == chronoStatus.InProgressA or self.status == chronoStatus.InProgressB)
            and caller.lower() == "udpreceive" or caller.lower() == "btnnext") \
                and data.lower() == "event":
            self.__declareBase(address)

    def slot_status(self, status):
        self.status=status

    def timerEvent(self):
        self.__declareBase("Altitude")
        
    def __declareBase (self, base):
        print (base, self.status)
        now = time.time()
        if self.status == chronoStatus.InWait or self.status == chronoStatus.WaitLaunch:
            self.set_status(self.status+1)
            return True

        if self.status == chronoStatus.WaitAltitude and now>=(self.startAltitude + 5.0):
            self.altitude_finished.emit()
            self.set_status(self.status+1)
            self.timer.stop()
            return True

        if self.status == chronoStatus.Finished:
            self.run_validated.emit()
            return True

        if self.status == chronoStatus.Launched and (base == "btnnext" or base == "baseA"):
            self.lastBase=base
            self.set_status(self.status+1)
            return True

        if self.status == chronoStatus.InStart and (base == "btnnext" or base == "baseA"):
            self.lastBaseChangeTime = now
            self.startTime = datetime.now()
            self.chronoLap.clear()
            self.timelost.clear()
            self.set_status(self.status+1)
            self.lastBase = base
            self.run_started.emit()
            return True

        if self.status==chronoStatus.InProgressA and (base == "baseA" or base == "btnnext"):
            elapsedTime = (now - self.lastBaseChangeTime)
            self.lastBaseChangeTime = now
            self.lastDetectionTime = now
            self.lastBase = base

            self.status = chronoStatus.InProgressB
            self.chronoLap.append(elapsedTime)
            self.timelost.append(0.0)
            self.lap_finished.emit(self.getLapCount(), elapsedTime)

            if self.getLapCount()==10:
                self.endTime=datetime.now()
                self.set_status(chronoStatus.WaitAltitude)
                self.startAltitude = now
                self.run_finished.emit(self.get_time())
                self.timer.start(100)
            return True
        elif self.status==chronoStatus.InProgressB and (base=="baseB" or base=="btnnext"):
            elapsedTime = ((now- self.lastBaseChangeTime))
            self.lastBaseChangeTime = now
            self.lastDetectionTime = now
            self.lastBase = base

            self.status = chronoStatus.InProgressA
            self.chronoLap.append(elapsedTime)
            self.timelost.append(0.0)
            self.lap_finished.emit(self.getLapCount(), elapsedTime)
            return True
        elif self.getLapCount() > 1:    #Base declaration is the same
                elapsedTime = now - self.lastDetectionTime
                self.lastDetectionTime = now
                self.timelost[self.getLapCount() - 1] = self.timelost[self.getLapCount() - 1] + elapsedTime
                return False

class ChronoArduino(ChronoHard):
    def __init__(self, signal_btnnext):
        super().__init__(signal_btnnext)
        print("chronoArduino init")
        self.chrono_signal.connect(self.handle_chrono_event)
        self.arduino = rs232_arduino(ConfigReader.config.conf['voltage_coef'], ConfigReader.config.conf['rebound_btn_time'],
                                   ConfigReader.config.conf['buzzer_duration'], self.status_changed, self.run_started,
                                     self.lap_finished, self.run_finished, self.accu_signal)
        self.reset()


    def handle_chrono_event(self, caller, data, address):
        if not caller.lower() == "btnnext":
            self.buzzer_validated.emit()
        status = self.arduino.get_status()
        if caller.lower() == "btnnext" and \
                (status == chronoStatus.WaitLaunch or status == chronoStatus.InWait):
            self.set_status(status+1)
        if caller.lower() == "btnnext" and data == "event" and address == "baseA" and\
                (status == chronoStatus.InStart or status == chronoStatus.Launched):
            self.arduino.event_BaseA()
        if caller.lower() == "btnnext" and status == chronoStatus.Finished:
            self.run_validated.emit()

    def reset(self):
        self.arduino.reset()



''' 

def main ():

    print ('Chrono Test')
    chronoRpi=ChronoRpi()
    chronoRpi.reset()
    chronoRpi.chrono_signal.emit("test","test1","test2")


if __name__ == '__main__':
    main()
'''