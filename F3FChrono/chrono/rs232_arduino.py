import serial
import sys
import threading
import time


class arduino_com:
    lock = threading.Lock()
    def __init__(self, voltageCoef, rebundTimeBtn):
        super().__init__()

        self.bus = serial.Serial(port='/dev/ttyS0', baudrate = 57600, parity=serial.PARITY_NONE,
                                 stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS, timeout=1)
        print(self.bus)
        
        self.lastrequest = 0.0
        self.voltageCoef = voltageCoef
        self.status = 0
        self.voltage = 0.0
        self.nbLap = 0
        self.lap = []
        self.nb_data = 32
        for count in range(10):
            self.lap.append(0.0)

    def debug (self):
        self.bus.write("d.".encode())
        for i in range(10):
            print(self.bus.readline())
        
    def set_status(self, status):
        self.bus.write(("s"+str(status)+".").encode())
        for i in range(4):
            print(self.bus.readline())
        #        self.bus.write_byte_data(self.addresschrono, 0, status)
        self.status = status

        return 0

    def set_buzzerTime(self, time):
        self.bus.write(("t"+str(time)+".").encode())
        for i in range(4):
            print(self.bus.readline())
        return 0

    def set_RebundBtn(self, time):
        self.bus.write(("b"+str(time)+".").encode())
        for i in range(4):
            print(self.bus.readline())
        return 0

    def event_BaseA(self):
        self.bus.write(("e.").encode())
        for i in range(4):
            print(self.bus.readline())
        return 0

    def resetChrono(self):
        self.bus.write(("r.").encode())
        for i in range(4):
            print(self.bus.readline())
        return 0
        self.status = 0
        self.nbLap = 0
        for lap in self.lap:
            lap = 0
        return 0


if __name__ == '__main__':

    print("Chrono Arduino RS232 Mode")
    chrono = arduino_com(0.354, 500)
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