import smbus
import time
import sys

class chronoStatus():
    InWait=0
    WaitLaunch=1
    Launched=2
    InStart=3
    InProgress=4
    Finished=5
    

# This is the address we setup in the Arduino Program
#anemoaddress = 0x04
#chronoaddress = 0x05

class chronoArduino():
    def __init__(self):
        # for RPI version 1, use “bus = smbus.SMBus(0)”
        self.bus = smbus.SMBus(1)
        self.address = 0x05
        self.data=[0]

    def set_status_inStart(self):
        number=self.bus.read_i2c_block_data(self.address, 0, 2)
        return number

    def set_status_launched(self):
        number=self.bus.read_i2c_block_data(self.address, 0, 1)
        return number
 
    def reset(self):
        number=self.bus.read_i2c_block_data(self.address, 3, 1)
        return number
        
    def get_status(self):
        number=self.bus.read_i2c_block_data(self.address, 1, 2)
        return number
        
    def get_nbLap(self):
        number=self.bus.read_i2c_block_data(self.address, 2, 2) 
        return number

    def get_timeLap(self, lap):
        number=[0,0]
        lap=self.bus.read_i2c_block_data(self.address, 10+lap, 5)
        number[0]=lap[0]
        number[1]=(lap[4]<<24 | lap[3]<<16 | lap[2]<<8 | lap[1])
        return number
    
    
if __name__=='__main__':

    print("Chrono Arduino I2C Mode")
    chrono=chronoArduino()
    end=False
    while not end:
        cmdline=sys.stdin.readline()
        if cmdline=="setstatus\n":
            print(chrono.set_status_launched())
        if cmdline=="getstatus\n":
            print(chrono.get_status())
        if cmdline=="gettime\n":
            nbLap = chrono.get_nbLap()
            print(nbLap)
            for i in range(0,nbLap[1]):
                time.sleep(0.01)
                lap = chrono.get_timeLap(i)
                print (i, lap)
        if cmdline=="reset\n":
            print("reset ", chrono.reset())
    

