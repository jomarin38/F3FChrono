import os
import re
import serial
import sys
import time
from PyQt5.QtCore import QObject, pyqtSignal
import threading
from F3FChrono.chrono import Chrono
from F3FChrono.Utils import is_running_on_pi


class rs232_arduino (QObject):
    reset_arduino_sig = pyqtSignal()

    def __init__(self, voltageCoef, rebundTimeBtn, buzzerTime, status_changed, run_started, climbout_time, lap_finished,
                 run_finished, run_training, wait_alt_sig, accu_sig):
        super().__init__()
        self.bus = serial.Serial(port=rs232_arduino.get_serial_port(), baudrate = 57600, parity=serial.PARITY_NONE,
                                 stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS, timeout=0.2)

        self.status_changed_sig = status_changed
        self.run_started_sig = run_started
        self.lap_finished_sig = lap_finished
        self.run_finished_sig = run_finished
        self.run_training_sig = run_training
        self.climbout_time_sig = climbout_time
        self.wait_alt_sig = wait_alt_sig
        self.accu_sig = accu_sig
        self.status=0
        self.lastrequest=0.0
        self.rebundTime = rebundTimeBtn
        self.buzzerTime = buzzerTime
        self.lastrequest = 0.0
        self.voltageCoef = voltageCoef
        self.reset_arduino_sig.connect(self.slot_arduino_reset)
        self.terminated = False
        self.event = threading.Thread(target=self.receive)
        self.event.daemon = True
        self.event.start()
        self.inRun = False
        self.kill_aduino()
        self.training = False
        self.__debug = False
        self.finaltime = 0.0

    @staticmethod
    def get_serial_port():
        if is_running_on_pi():
            return '/dev/ttyS0'
        else:
            return '/dev/ttyUSB0'

    def slot_arduino_reset(self):
        self.set_RebundBtn(self.rebundTime)
        self.set_buzzerTime(self.buzzerTime)
        #self.debug()
        self.set_mode(training=False)
        self.finaltime = 0.0

    def receive(self):
        while not self.terminated:
            try:
                if self.bus.inWaiting() > 0:
                    data = self.bus.readline().decode().split(',')
                    if (self.__debug):
                        print(data)
                    if data[0] == "status":
                        self.status = int(data[1])
                        self.status_changed_sig.emit(self.status)
                        if self.status == Chrono.chronoStatus.InWait:
                            self.inRun = False
                        if self.status == Chrono.chronoStatus.Late or self.status == Chrono.chronoStatus.InStartLate:
                            if not self.inRun:
                                self.finaltime = 0.0
                                self.run_started_sig.emit()
                                self.set_inRun()

                        if self.status == Chrono.chronoStatus.InProgressB or self.status == Chrono.chronoStatus.InProgressA:
                            if not self.inRun:
                                self.finaltime = 0.0
                                self.run_started_sig.emit()
                                self.set_inRun()

                        if self.status == Chrono.chronoStatus.Finished:
                            self.wait_alt_sig.emit(self.finaltime)
                    if data[0] == "lap":
                        if self.training:
                            if int(data[1]) >= 10:
                                tmp = 0.
                                for i in range(2, 11):
                                    tmp += int(data[i]) / 1000
                                self.run_training_sig.emit(int(data[1]), tmp)
                            else:
                                self.run_training_sig.emit(int(data[1]), 0.0)
                        else:
                            if 1 <= int(data[1]) <= 10:
                                self.lap_finished_sig.emit(int(data[1]), int(data[int(data[1])+1])/1000)
                            if int(data[1]) == 10:
                                tmp = 0.
                                for i in range(2, int(data[1])+2):
                                    tmp += int(data[i])/1000
                                self.finaltime = tmp
                                self.run_finished_sig.emit(self.finaltime)
                    if data[0] == "climbout_time":
                        self.climbout_time_sig.emit(int(data[1])/1000)
                    if data[0] == "voltage":
                        self.accu_sig.emit(int(data[1])*5/1024/self.voltageCoef)
                    if data[0] == "resetµc":
                        self.reset_arduino_sig.emit()
            except serial.SerialException as e:
                if self.__debug:
                    print("serial exception")
                return None
            except TypeError as e:
                if self.__debug:
                    print("bus close : ", e)
                self.bus.close()
                self.bus = None
                return None
            time.sleep(0.002)

    def set_mode(self, training=True):
        self.check_request_time()
        chaine = "m1\n" if training else "m0\n"
        self.bus.write(chaine.encode())
        self.training = training
        return 0

    def set_inRun(self):
        self.inRun = True
        #self.event_Base('a')

    def debug(self):
        self.check_request_time()
        self.bus.write("d\n".encode())
        self.__debug = True
        return 0

    def set_status(self, status):
        self.check_request_time()
        self.bus.write(("s"+str(status)+"\n").encode())
        return 0

    def set_buzzerTime(self, time):
        self.check_request_time()
        self.bus.write(("t"+str(time)+"\n").encode())
        return 0

    def set_RebundBtn(self, time):
        self.check_request_time()
        self.bus.write(("b"+str(time)+"\n").encode())
        return 0

    def event_Base(self, base='a'):
        if self.__debug:
            print("force base : ", base)
        self.check_request_time()
        self.bus.write(("e"+base+"\n").encode())
        return 0

    def kill_aduino(self):
        self.check_request_time()
        self.bus.write(("k\n").encode())
        self.__debug = False

    def reset(self):
        self.check_request_time()
        self.bus.write(("r\n").encode())
        return 0

    def reset_training(self):
        self.reset()
        self.set_status(Chrono.chronoStatus.InStart)

    def get_voltage(self):
        self.check_request_time()
        self.bus.write(("v\n").encode())
        return 0

    def get_status(self):
        return self.status

    def stop(self):
        self.terminated = True
        self.event.join(timeout=1.0)

    def check_request_time(self):
        if (time.time() - self.lastrequest) < 0.1:
            time.sleep(0.1)
        self.lastrequest = time.time()

if __name__ == '__main__':

    status_changed = pyqtSignal(int)
    lap_finished = pyqtSignal(int, float)
    run_finished = pyqtSignal(float)
    run_started = pyqtSignal()
    accu_signal = pyqtSignal(float)
    print("Chrono Arduino RS232 Mode")
    chrono = rs232_arduino(0.354, 500, 300, status_changed, run_started, lap_finished, run_finished, accu_signal)
    end = False
    while not end:
        cmdline = sys.stdin.readline()
        if cmdline == "d\n":
            chrono.debug()
            #print(chrono.set_buzzerTime(5000))
        
        if cmdline == "s\n":
            chrono.set_status(2)
            #print(chrono.set_buzzerTime(5000))
        if cmdline == "g\n":
            chrono.get_data()
            chrono.get_data1()
            print(chrono.status, chrono.voltage, chrono.nbLap, chrono.lap)

        if cmdline == "t\n":
            chrono.set_buzzerTime(500)
        if cmdline == "r\n":
            print("reset ", chrono.reset())

        if cmdline == "v\n":
            print(chrono.get_voltage())
        if cmdline == "a\n":
            print(chrono.readlines())
