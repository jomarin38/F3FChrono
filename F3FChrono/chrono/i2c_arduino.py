import smbus
import time
import sys
from F3FChrono.chrono import ConfigReader

class chronoStatus():
    InWait=0
    WaitLaunch=1
    Launched=2
    InStart=3
    InProgress=4
    WaitAltitude=5
    Finished=6
    

# This is the address we setup in the Arduino Program
#anemoaddress = 0x04
chronoaddress = 0x05

class i2c_register():
    setStatus = 1
    setBuzzerTime = 2
    setRebundBtn = 3
    eventBaseA = 4
    reset = 5
    getData = 6
    getData1 = 7


class arduino_com():
    def __init__(self, voltageCoef, rebundTimeBtn):
        super().__init__()

        self.bus = None
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
        self.set_RebundBtn(rebundTimeBtn)


        
    def set_status(self, status):
        self.__sendrequest__(self.addresschrono, i2c_register.setStatus, status, read=False)
#        self.bus.write_byte_data(self.addresschrono, 0, status)
        self.status = status
        print ("I2CSet_Status : ", self.status)
        return 0

    def set_buzzerTime(self, time):
        self.__sendrequest__(self.addresschrono, i2c_register.setBuzzerTime, time, read=False)
#        self.bus.write_word_data(self.addresschrono, 1, time & 0xffff)
        return 0

    def set_RebundBtn(self, time):
        self.__sendrequest__(self.addresschrono, i2c_register.setRebundBtn, time, read=False)
        return 0

    def event_BaseA(self):
        self.__sendrequest__(self.addresschrono, i2c_register.eventBaseA, time, read=False)
        return 0

    def reset(self):
        self.__sendrequest__(self.addresschrono, i2c_register.reset, 1, read=False)
#        self.bus.read_i2c_block_data(self.addresschrono, 4, 1)
        self.status = 0
        self.nbLap = 0
        for lap in self.lap:
            lap=0
        return 0
        
    def get_data(self):
        data = self.__sendrequest__(self.addresschrono, i2c_register.getData, nbdata=16, read=True)
#       number = self.bus.read_i2c_block_data(self.addresschrono, 2, 16)
        if len(data) == 16:
            self.status = data[0]
            self.voltage = (data[2] << 8 | data[1])*5/1024/self.voltageCoef
            if data[3]<11:
                self.nbLap = data[3]
            indexlap = 0
            for count in range(4, 15, 4):
                self.lap[indexlap] = (data[count+3] << 24 | data[count+2] << 16 | data[count+1] << 8 | data[count])/1000
                indexlap += 1
        return 0

    def get_data1(self):
        data = self.__sendrequest__(self.addresschrono, i2c_register.getData1, nbdata=32, read=True)
#        number = self.bus.read_i2c_block_data(self.addresschrono, 3, 28)
        if len(data) == 32:
            indexlap = 3
            for count in range(0, 27, 4):
                self.lap[indexlap] = (data[count+3] << 24 | data[count+2] << 16 | data[count+1] << 8 | data[count])/1000
                indexlap += 1
        return 0

    def checki2ctime(self):
        if (time.time()-self.lastrequest) < 0.02:
            time.sleep(0.05)
            
        self.lastrequest=time.time()

    def __sendrequest__(self, address, cmd, data=None, nbdata=0, read=False):
        response = []
        for x in range(2):
            try:
                if self.bus is not None:
                    self.checki2ctime()
                    if read:
                        response = self.bus.read_i2c_block_data(address, cmd, nbdata)
                    else:
                        response = self.bus.write_byte_data(address, cmd, data)
                    break
            except IOError:
                print("error I2C", x)

        return response



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