import smbus
import time
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

class arduino_com(QTimer):
    def __init__(self, voltageCoef):
        super().__init__()
        # for RPI version 1, use “bus = smbus.SMBus(0)”
        self.bus = smbus.SMBus(1)
        self.addresschrono = chronoaddress
        self.data=[0]
        self.voltageCoef = voltageCoef
        self.lapTimerEvent = QTimer()
        self.lapTimerEvent.timeout.connect(self.runlaprequest)
        self.lapTimerEvent.start(50)
        self.currentlap=0
        self.oldlap=0
        self.voltage=0
        self.voltageDelay=5000
        self.voltageCount=0
        
    def runlaprequest(self):
        self.currentlap = self.get_nbLap()
        if (self.currentlap!=self.oldlap):
            print("lap ", self.oldlap, " : ", self.get_timeLap(self.oldlap))
            time.sleep(0.01)
            self.old_nb_lap=self.currentlap
            
        if (self.voltageCount>=self.voltageDelay):
            time.sleep(0.01)
            self.voltage=self.get_voltage()
            print("volage : ", self.voltage)
            self.voltageCount=0
        
        self.voltageCount+=50
    
    def set_status_inStart(self):
        number=self.bus.read_i2c_block_data(self.addresschrono, 0, 2)
        return number[1]

    def set_status_launched(self):
        number=self.bus.read_i2c_block_data(self.addresschrono, 0, 1)
        return number[0]
 
    def reset(self):
        number=self.bus.read_i2c_block_data(self.addresschrono, 3, 1)
        return number[0]
        
    def get_status(self):
        number=self.bus.read_i2c_block_data(self.addresschrono, 1, 2)
        return number[1]
        
    def get_nbLap(self):
        number=self.bus.read_i2c_block_data(self.addresschrono, 2, 2)
        return number[1]

    def get_timeLap(self, lap):
        number=[0,0]
        lap=self.bus.read_i2c_block_data(self.addresschrono, 10+lap, 5)
        number[0]=lap[0]
        number[1]=(lap[4]<<24 | lap[3]<<16 | lap[2]<<8 | lap[1])
        return number[1]

    def get_voltage(self):
        number=self.bus.read_i2c_block_data(self.addresschrono, 100, 3)
        
        return (number[2]<<8 | number[1])*5/1024/self.voltageCoef
    
if __name__=='__main__':

    app = QApplication(sys.argv)
    print("Chrono Arduino I2C Mode")
    chrono=arduino_com(0.354)
    sys.exit(app.exec())
    
'''    end=False
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
'''