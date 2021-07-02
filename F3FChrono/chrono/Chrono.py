#
# This file is part of the F3FChrono distribution (https://github.com/jomarin38/F3FChrono).
# Copyright (c) 2021 Sylvain DAVIET, Joel MARIN.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#

import os
from datetime import datetime
import collections
from PyQt5.QtCore import pyqtSignal, QObject, QTimer
from F3FChrono.chrono.UDPBeep import *
from F3FChrono.chrono.UDPReceive import *
from F3FChrono.chrono import ConfigReader
from F3FChrono.chrono.rs232_arduino import rs232_arduino
from F3FChrono.chrono.weather import Weather


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
    Late = 3
    InStart = 4
    InStartLate = 5
    InProgressA = 6
    InProgressB = 7
    WaitAltitude = 8
    Finished = 9



class ChronoHard(QObject):
    status_changed = pyqtSignal(int)
    run_started = pyqtSignal()
    climbout = pyqtSignal(float)
    lap_finished = pyqtSignal(int, float)
    run_finished = pyqtSignal(float)
    run_validated = pyqtSignal()
    run_training = pyqtSignal(int, float)
    buzzer_validated = pyqtSignal()
    chrono_signal = pyqtSignal(str, str, str)
    accu_signal = pyqtSignal(float, float)
    rssi_signal = pyqtSignal(int, int)
    altitude_finished = pyqtSignal(float)

    def __init__(self, signal_btnnext):
        super().__init__()
        self.penalty = 0.0
        self.startTime = None
        self.endTime = None
        self.climbout_time = 0
        self.signal_btnnext = signal_btnnext
        self.chronoLap = []
        self.timelost = []
        self.weather = Weather()
        self.udpReceive = udpreceive(UDPPORT, self.chrono_signal, self.signal_btnnext, self.weather.windspeed_signal,
                                     self.weather.winddir_signal, self.weather.rain_signal, self.accu_signal,
                                     self.rssi_signal)
        self.udpBeep = udpbeep(IPUDPBEEP, UDPPORT)
        self.valid = True
        self.refly = False
        self.__debug = False

    def addPenalty(self, value):
        self.penalty += value
        return (self.penalty)

    def clearPenalty(self):
        self.penalty = 0.0
        return (self.penalty)

    def getPenalty(self):
        return (self.penalty)

    def get_status(self):
        return self.status

    def reset(self):
        self.chronoLap.clear()
        self.timelost.clear()
        self.set_status(chronoStatus.InWait)
        self.lastBase = -2
        self.penalty = 0.0
        self.reset_wind()
        self.valid = True
        self.refly = False

    def getLastLapTime(self):
        if self.getLapCount() > 0:
            return self.chronoLap[self.getLapCount() - 1]
        else:
            return 0

    def get_climbout_time(self):
        return (self.climbout_time)

    def get_time(self):
        time = 0
        for i in range(self.getLapCount()):
            time = time + self.chronoLap[i]
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
        result = os.linesep + "Chrono Data : " + os.linesep + "\tStart Time : " + str(self.startTime) + \
                 os.linesep + "\tEnd Time : " + str(self.endTime) + os.linesep + "\tRun Time : " + \
                 "{:0>6.3f}".format(self.get_time()) + os.linesep + "\tLapTime : "
        for lap in self.getLaps():
            result += "{:0>6.3f}".format(lap) + ","
        result += os.linesep + "\tPenalty : " + str(self.penalty) + os.linesep
        result += "Wind Speed :" + os.linesep + "\tMean : " + "{:0>6.1f}".format(self.getMeanWindSpeed()) + os.linesep + \
                  "\tMin : " + "{:0>6.1f}".format(self.getMinWindSpeed()) + os.linesep + \
                  "\tMax : " + "{:0>6.1f}".format(self.getMaxWindSpeed()) + os.linesep + \
                  "Wind Orientation : " + "{:0>6.1f}".format(self.getMaxWindSpeed()) + os.linesep + \
                  "rain : " + str(self.getRain()) + os.linesep
        return (result)

    def setrefly(self):
        self.refly = True

    def isRefly(self):
        return (self.refly)


class ChronoArduino(ChronoHard, QTimer):
    _lock = threading.Lock()
    _last_event_time = 0

    def __init__(self, signal_btnnext):
        super().__init__(signal_btnnext)
        self.__debug = False
        self.status = chronoStatus.InWait
        self.chrono_signal.connect(self.handle_chrono_event)
        self.lap_finished.connect(self.handle_lap_finished)
        self.run_started.connect(self.handle_run_started)
        self.run_finished.connect(self.handle_run_finished)

        self.arduino = rs232_arduino(ConfigReader.config.conf['voltage_coef_Accu1'],
                                     ConfigReader.config.conf['voltage_coef_Accu2'],
                                     ConfigReader.config.conf['rebound_btn_time'],
                                     ConfigReader.config.conf['buzzer_duration'], self.status_changed, self.run_started,
                                     self.climbout,
                                     self.lap_finished, self.run_finished, self.run_training, self.altitude_finished,
                                     self.accu_signal)

        self.status_changed.connect(self.slot_status)
        self.climbout.connect(self.handle_climbout_time)
        self.timer = QTimer()
        self.timer.timeout.connect(self.event_voltage)
        self.timer.start(30000)
        self.reset()
        self.in_start_blackout_enabled = ConfigReader.config.conf['inStartBlackOut']
        self.in_start_blackout_second = ConfigReader.config.conf['inStartBlackOut_second']
        self.competition_mode = ConfigReader.config.conf['competition_mode']

    def slot_status(self, status):
        self.status = status
        if status == chronoStatus.Launched:
            self.weather.setInRun(True)
        elif status == chronoStatus.WaitAltitude:
            self.weather.setInRun(False)

    def event_voltage(self):
        self.arduino.get_voltage()

    def set_status(self, value):
        if (self.status != value):
            self.arduino.set_status(value)

    def handle_chrono_event(self, caller, data, address):
        ChronoArduino._lock.acquire()
        if caller.lower() == "btnnext" and \
                (self.status == chronoStatus.WaitLaunch or self.status == chronoStatus.InWait):
            self.arduino.set_status(self.status + 1)
        elif caller.lower() == "btnnext" and self.status == chronoStatus.InStart:
            if not self.competition_mode:
                self.arduino.event_Base('n')
        elif caller.lower() == "btnnext" and self.status == chronoStatus.Finished:
            self.run_validated.emit()
        elif caller.lower() == "btnnext":
            if not self.competition_mode:
                if self.__debug:
                    print("demande event btn Next")
                self.arduino.event_Base('n')

        if caller.lower() == "udpreceive" and data == "event" and address == "baseA":
            if not self.competition_mode:
                if not self.in_start_blackout_enabled or self.status > chronoStatus.InStart or \
                        ChronoArduino._last_event_time + self.in_start_blackout_second < time.time():
                    self.arduino.event_Base('a')
            else:
                self.arduino.event_Base('a')
            if self.in_start_blackout_enabled:
                ChronoArduino._last_event_time = time.time()

        if caller.lower() == "udpreceive" and data == "event" and address == "baseB":
            if self.__debug:
                print("demande event base B")
            self.arduino.event_Base('b')
        ChronoArduino._lock.release()

    def handle_run_started(self):
        self.startTime = datetime.now()
        self.arduino.set_inRun()

    def handle_climbout_time(self, time):
        self.climbout_time = time
        if self.__debug:
            print("climbout Time : ", time)

    def handle_lap_finished(self, lap, time):
        self.chronoLap.append(time)

    def handle_run_finished(self, time):
        self.endTime = datetime.now()

    def reset(self):
        self.arduino.reset()
        self.chronoLap.clear()
        self.weather.reset_wind()
        self.clearPenalty()
        self.valid = True
        self.refly = False

    def set_buzzer_time(self, time):
        self.arduino.set_buzzerTime(time)

    def stop(self):
        self.arduino.stop()

    def set_mode(self, training=True):
        self.arduino.set_mode(training)


'''
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
'''


def main():
    print('Chrono Test')
    chrono = ChronoArduino()
    chrono.reset()
    chrono.chrono_signal.emit("test", "test1", "test2")


if __name__ == '__main__':
    main()
