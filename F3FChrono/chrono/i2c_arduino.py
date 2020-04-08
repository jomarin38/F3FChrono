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
    getData = 0x00
    reset = 0x01
    setBuzzerTime = 0x101

class arduino_com():
    def __init__(self, voltageCoef):
        super().__init__()

        self.bus=None
        if ConfigReader.config.conf['arduino']:
            # for RPI version 1, use “bus = smbus.SMBus(0)”
            self.bus = smbus.SMBus(1)

        self.addresschrono = chronoaddress
        self.lastrequest=0.0
        self.voltageCoef=voltageCoef
        self.status=0
        self.voltage=0.0
        self.nbLap=0
        self.lap=[]
        for count in range(10):
            self.lap.append(0)
        
    def set_status(self, status):
        if self.bus is not None:
            self.checki2ctime()
            self.bus.write_byte_data(self.addresschrono, 0, status)
        else:
            self.status=status
        return 0

    def set_buzzerTime(self, time):
        if self.bus is not None:
            self.checki2ctime()
            self.bus.write_word_data(self.addresschrono, 1, time & 0xffff)
        return 0

    def reset(self):
        if self.bus is not None:
            self.checki2ctime()
            number = self.bus.read_i2c_block_data(self.addresschrono, 4, 1)
            for lap in self.lap:
                lap=0
        return 0
        
    def get_data(self):
        if self.bus is not None:
            self.checki2ctime()
            number = self.bus.read_i2c_block_data(self.addresschrono, 2, 16)

            self.status = number[0]
            self.voltage = (number[2] << 8 | number[1])*5/1024/self.voltageCoef
            self.nbLap = number[3]
            indexlap=0
            for count in range(4,15,4):
                self.lap[indexlap] = number[count+3] << 24 | number[count+2] << 16 | number[count+1] << 8 | number[count]
                indexlap+=1

    def get_data1(self):
        if self.bus is not None:
            self.checki2ctime()
            number = self.bus.read_i2c_block_data(self.addresschrono, 3, 28)
            indexlap=3
            for count in range(0,23,4):
                self.lap[indexlap] = number[count+3] << 24 | number[count+2] << 16 | number[count+1] << 8 | number[count]
                indexlap+=1
    def get_time(self):
        time=0
        for count in self.lap:
            time+=count
        return time
    '''    
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
        print (number)
        voltage = (number[2] << 8 | number[1])*5/1024/self.voltageCoef
        return voltage
    '''
    def checki2ctime(self):
        if (time.time()-self.lastrequest) < 0.02:
            self.i2cdelay()
            
        self.lastrequest=time.time()

    @staticmethod
    def i2cdelay():
        time.sleep(0.05)
    
if __name__=='__main__':

    print("Chrono Arduino I2C Mode")
    chrono=arduino_com(0.354)
    end=False
    while not end:
        cmdline=sys.stdin.readline()
        if cmdline=="s\n":
            print(chrono.set_status(1))
            print(chrono.set_buzzerTime(5000))
        if cmdline=="g\n":
            chrono.get_data()
            chrono.get_data1()
            print (chrono.status, chrono.voltage, chrono.nbLap, chrono.lap)

        if cmdline=="t\n":
            nbLap = chrono.get_data1()
            print(nbLap)
        if cmdline=="r\n":
            print("reset ", chrono.reset())

        if cmdline=="v\n":
            print (chrono.get_voltage())