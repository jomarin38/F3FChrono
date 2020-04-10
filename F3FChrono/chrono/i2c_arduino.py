import smbus
import time
from datetime import datetime
import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QTimer
from F3FChrono.chrono import ConfigReader

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
    setStatus = 0
    setBuzzerTime = 1
    setRebundBtn = 2
    reset = 3
    getData = 4
    getData1 = 5


class arduino_com():
    def __init__(self, voltageCoef):
        super().__init__()

        self.bus=None
        if ConfigReader.config.conf['arduino']:
            # for RPI version 1, use “bus = smbus.SMBus(0)”
            self.bus = smbus.SMBus(1)

        self.addresschrono = chronoaddress
        self.lastrequest = 0.0
        self.voltageCoef = voltageCoef
        self.status = 0
        self.voltage = 0.0
        self.nbLap = 0
        self.lap = []
        for count in range(10):
            self.lap.append(0.0)
        self._data = []


        
    def set_status(self, status):
        self.__sendrequest__(self.addresschrono, i2c_register.setStatus, status, read=False)
#        self.bus.write_byte_data(self.addresschrono, 0, status)
        self.status = status
        return 0

    def set_buzzerTime(self, time):
        self.__sendrequest__(self.addresschrono, i2c_register.setBuzzerTime, time, read=False)
#        self.bus.write_word_data(self.addresschrono, 1, time & 0xffff)
        return 0

    def set_RebundBtn(self, time):
        self.__sendrequest__(self.addresschrono, i2c_register.setRebundBtn, time, read=False)
        return 0
    def reset(self):
        self.__sendrequest__(self.addresschrono, i2c_register.reset, 1, read=False)
#        self.bus.read_i2c_block_data(self.addresschrono, 4, 1)
        self.status=0
        self.nbLap=0
        for lap in self.lap:
            lap=0
        return 0
        
    def get_data(self):
        self.__sendrequest__(self.addresschrono, i2c_register.getData, nbdata=16, read=True)
#       number = self.bus.read_i2c_block_data(self.addresschrono, 2, 16)

        self.status = self._data[0]
        self.voltage = (self._data[2] << 8 | self._data[1])*5/1024/self.voltageCoef
        self.nbLap = self._data[3]
        indexlap=0
        for count in range(4, 15, 4):
            self.lap[indexlap] = (self._data[count+3] << 24 | self._data[count+2] << 16 | self._data[count+1] << 8 | self._data[count])/1000
            indexlap+=1
        return 0

    def get_data1(self):
        self.__sendrequest__(self.addresschrono, i2c_register.getData1, nbdata=32, read=True)
#        number = self.bus.read_i2c_block_data(self.addresschrono, 3, 28)
        indexlap = 3
        for count in range(0, 27, 4):
            self.lap[indexlap] = (self._data[count+3] << 24 | self._data[count+2] << 16 | self._data[count+1] << 8 | self._data[count])/1000
            indexlap += 1
        return 0

    def get_time(self):
        time=0
        for count in self.lap:
            time+=count
        return time

    def checki2ctime(self):
        if (time.time()-self.lastrequest) < 0.02:
            time.sleep(0.05)
            
        self.lastrequest=time.time()

    def __sendrequest__(self, address, cmd, data=None, nbdata=0, read=False):
        for x in range(2):
            try:
                if self.bus is not None:
                    self.checki2ctime()
                    if read:
                        self._data = self.bus.read_i2c_block_data(address, cmd, nbdata)
                    else:
                        print(address, cmd, data)
                        self._data = self.bus.write_byte_data(address, cmd, data)
                    break
            except IOError:
                print("error I2C", x)

        return 0



if __name__ == '__main__':

    print("Chrono Arduino I2C Mode")
    chrono = arduino_com(0.354)
    end = False
    while not end:
        cmdline = sys.stdin.readline()
        if cmdline == "s\n":
            print(chrono.set_status(1))
            print(chrono.set_buzzerTime(5000))
        if cmdline == "g\n":
            chrono.get_data()
            chrono.get_data1()
            print(chrono.status, chrono.voltage, chrono.nbLap, chrono.lap)

        if cmdline == "t\n":
            nbLap = chrono.get_data1()
            print(nbLap)
        if cmdline == "r\n":
            print("reset ", chrono.reset())

        if cmdline == "v\n":
            print(chrono.get_voltage())