#import smbus
import time
from datetime import datetime
import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QTimer

class chronoStatus():
    InWait=0
    WaitLaunch=1
    Launched=2
    InStart=3
    InProgress=4
    Finished=5
    

# This is the address we setup in the Arduino Program
#anemoaddress = 0x04
chronoaddress = 0x05

class i2c_register():
    setstatus = 0x01
    setStatus_InStart = 0x01
    getStatus = 0x02
    getLapCount = 0x03
    reset = 0x04
    getTime = 0x10
    getVoltage = 0x100
    setBuzzerTime = 0x101

class arduino_com():
    def __init__(self):
        super().__init__()
        # for RPI version 1, use “bus = smbus.SMBus(0)”
        self.bus = smbus.SMBus(1)
        self.addresschrono = chronoaddress
        self.lastrequest=0

    def set_status(self, status):
        self.checki2ctime()
        self.bus.write_byte_data(self.addresschrono, i2c_register.setstatus, status)

        return 0

    def set_buzzerTime(self, time):
        self.checki2ctime()
        self.bus.write_word_data(self.addresschrono, i2c_register.setBuzzerTime, time)
        return 0

    def reset(self):
        self.checki2ctime()
        number = self.bus.read_i2c_block_data(self.addresschrono, i2c_register.reset, 1)
        return number[0]
        
    def get_status(self):
        self.checki2ctime()
        number = self.bus.read_i2c_block_data(self.addresschrono, i2c_register.getStatus, 2)
        return number[1]
        
    def get_allLap(self):
        self.checki2ctime()
        nbLap = self.get_nbLap()
        lap = []
        for lapCount in range(0, nbLap-1):
            lap.append(self.__get_timeLap(lapCount))
        return lap

    def get_nbLap(self):
        self.checki2ctime()
        number=self.bus.read_i2c_block_data(self.addresschrono, i2c_register.getLapCount, 2)
        return number[1]

    def get_timeLap(self, lap):
        self.checki2ctime()
        lap = self.bus.read_i2c_block_data(self.addresschrono, i2c_register.getTime+lap, 5)
        return lap[4] << 24 | lap[3] << 16 | lap[2] << 8 | lap[1]


    def get_voltage(self):
        self.checki2ctime()
        number = self.bus.read_i2c_block_data(self.addresschrono, i2c_register.getVoltage, 3)
        return (number[2] << 8 | number[1])*5/1024/self.voltageCoef

    def checki2ctime(self):
        if (datetime.now()-self.lastrequest) > 0.01:
            self.lastrequest=datetime.now()
        else:
            self.i2cdelay()

    @staticmethod
    def i2cdelay():
        time.sleep(0.01)
    
if __name__=='__main__':

    app = QApplication(sys.argv)
    print("Chrono Arduino I2C Mode")
    chrono=arduino_com(0.354)
    end=False
    while not end:
        cmdline=sys.stdin.readline()
        if cmdline=="s\n":
            print(chrono.set_status_launched())
        if cmdline=="g\n":
            print(chrono.get_status())
        if cmdline=="t\n":
            nbLap = chrono.get_nbLap()
            print(nbLap)
            for i in range(0,nbLap[1]):
                time.sleep(0.01)
                lap = chrono.get_timeLap(i)
                print (i, lap)
        if cmdline=="r\n":
            print("reset ", chrono.reset())

        if cmdline=="v\n":
            print (chrono.get_voltage())