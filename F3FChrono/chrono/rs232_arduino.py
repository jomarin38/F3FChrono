import serial


class arduino_com:
    def __init__(self, voltageCoef, rebundTimeBtn):
        super().__init__()

        self.bus = serial.Serial(port='/dev/ttyS0', baudrate = 57600, parity=serial.PARITY_NONE,
                                 stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS, timeout=1)

        self.lastrequest = 0.0
        self.voltageCoef = voltageCoef
        self.status = 0
        self.voltage = 0.0
        self.nbLap = 0
        self.lap = []
        self.nb_data = 32
        for count in range(10):
            self.lap.append(0.0)

    def set_status(self, status):
        arduino_com.lock.acquire()
        print("I2CSet_Status : ", self.__sendrequest__(self.addresschrono, i2c_register.setStatus, status, read=False))
        #        self.bus.write_byte_data(self.addresschrono, 0, status)
        self.status = status
        arduino_com.lock.release()

        return 0

    def set_buzzerTime(self, time):
        arduino_com.lock.acquire()
        self.__sendrequest__(self.addresschrono, i2c_register.setBuzzerTime, time, read=False)
        #        self.bus.write_word_data(self.addresschrono, 1, time & 0xffff)
        arduino_com.lock.release()
        return 0

    def set_RebundBtn(self, time):
        arduino_com.lock.acquire()
        self.__sendrequest__(self.addresschrono, i2c_register.setRebundBtn, time, read=False)
        arduino_com.lock.release()
        return 0

    def event_BaseA(self):
        arduino_com.lock.acquire()
        self.__sendrequest__(self.addresschrono, i2c_register.eventBaseA, 0, read=False)
        arduino_com.lock.release()
        return 0

    def resetChrono(self):
        arduino_com.lock.acquire()
        self.__sendrequest__(self.addresschrono, i2c_register.reset, 1, read=False)
        #        self.bus.read_i2c_block_data(self.addresschrono, 4, 1)
        self.status = 0
        self.nbLap = 0
        for lap in self.lap:
            lap = 0
        arduino_com.lock.release()
        return 0

    def reboot(self):
        arduino_com.lock.acquire()
        self.__sendrequest__(self.addresschrono, i2c_register.reboot, 0, read=False)
        #        self.bus.read_i2c_block_data(self.addresschrono, 4, 1)
        time.sleep(0.2)
        arduino_com.lock.release()
        return 0

    def get_data(self):
        arduino_com.lock.acquire()
        data = self.__sendrequest__(self.addresschrono, i2c_register.getData, nbdata=self.nb_data, read=True)
        #       number = self.bus.read_i2c_block_data(self.addresschrono, 2, 16)
        if len(data) == self.nb_data:
            self.status = data[0]
            self.voltage = (data[2] << 8 | data[1]) * 5 / 1024 / self.voltageCoef
            if data[3] < 11:
                self.nbLap = data[3]
            indexlap = 0
            for count in range(4, 15, 4):
                self.lap[indexlap] = (data[count + 3] << 24 | data[count + 2] << 16 | data[count + 1] << 8 | data[
                    count]) / 1000
                indexlap += 1
        arduino_com.lock.release()
        return 0

    def get_data1(self):
        arduino_com.lock.acquire()
        data = self.__sendrequest__(self.addresschrono, i2c_register.getData1, nbdata=self.nb_data, read=True)
        #        number = self.bus.read_i2c_block_data(self.addresschrono, 3, 28)
        if len(data) == self.nb_data:
            indexlap = 3
            for count in range(0, 27, 4):
                self.lap[indexlap] = (data[count + 3] << 24 | data[count + 2] << 16 | data[count + 1] << 8 | data[
                    count]) / 1000
                indexlap += 1
        arduino_com.lock.release()
        return 0

    def __sendrequest__(self, data=None, read=False):

        response = []

        try:
            if self.bus is not None:
                if read:
                    response = self.bus.read()
                else:
                    response = self.bus.write(data)
                break
        except IOError:
            print("error RS232", x)
        return response


if __name__ == '__main__':

    print("Chrono Arduino RS232 Mode")
    chrono = arduino_com(0.354, 500)
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