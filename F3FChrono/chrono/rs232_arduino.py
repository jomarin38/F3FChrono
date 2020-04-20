import serial
import sys
import time
from PyQt5.QtCore import QTimer, pyqtSignal
import threading
from F3FChrono.chrono import Chrono



class rs232_arduino (threading.Thread):
    def __init__(self, voltageCoef, rebundTimeBtn, buzzerTime, status_changed, run_started, lap_finished,
                 run_finished, wait_alt_sig, accu_sig):
        super().__init__()
        self.bus=serial.Serial(port=rs232_arduino.get_serial_port(), baudrate = 57600, parity=serial.PARITY_NONE,
                                 stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS, timeout=0.2)
        print(self.bus)

        self.status_changed_sig = status_changed
        self.run_started_sig = run_started
        self.lap_finished_sig = lap_finished
        self.run_finished_sig = run_finished
        self.wait_alt_sig = wait_alt_sig
        self.accu_sig = accu_sig
        self.status=0
        self.lastrequest=0.0;
        self.set_RebundBtn(rebundTimeBtn)
        self.set_buzzerTime(buzzerTime)
        self.lastrequest = 0.0
        self.voltageCoef = voltageCoef
        self.terminated = False
        self.event = threading.Thread(target = self.receive)
        self.event.daemon = True
        self.event.start()
        self.inRun=False

    @staticmethod
    def get_serial_port():
        rev_file = '/sys/firmware/devicetree/base/model'
        info = {'pi': '', 'model': '', 'rev': ''}
        raspi = model = revision = ''
        try:
            fd = os.open(rev_file, os.O_RDONLY)
            line = os.read(fd, 256)
            os.close(fd)
            print(line)
            m = re.split(r'\s', line.decode('utf-8'))
            if m:
                info['pi'] = m[3]
                info['model'] = m[5]
        except:
            pass

        if info['pi'] == '':
            return '/dev/ttyUSB0'
        else:
            return '/dev/ttyS0'

    def receive(self):
        while not self.terminated:
            try:
                if self.bus.inWaiting()>0:
                    data = self.bus.readline().decode().split(',')
                    print(data)
                    if data[0] == "status":
                        self.status = int(data[1])
                        self.status_changed_sig.emit(self.status)
                        if self.status == Chrono.chronoStatus.InWait:
                            self.inRun=False
                        if self.status == Chrono.chronoStatus.InProgressB or self.status == Chrono.chronoStatus.InProgressA:
                            if not self.inRun:
                                self.run_started_sig.emit()
                                self.inRun=True
                        if self.status == Chrono.chronoStatus.Finished:
                            self.wait_alt_sig.emit()
                    if data[0] == "lap":
                        if 1 <= int(data[1]) <= 10:
                            self.lap_finished_sig.emit(int(data[1])-1, int(data[int(data[1])+1])/1000)
                        if int(data[1]) == 10:
                            tmp=0.
                            for i in range(2, int(data[1])+2):
                                tmp+=int(data[i])/1000
                                print("lap time : ", int(data[i])/1000, i)
                            self.run_finished_sig.emit(tmp)
                    if data[0] == "voltage":
                        self.accu_sig.emit(int(data[1])*5/1024/self.voltageCoef)

            except serial.SerialException as e:
                print("serial exception")
                return None
            except TypeError as e:
                print("bus close")
                self.bus.close()
                self.bus = None
                return None
            time.sleep(0.01)

    def debug(self):
        self.check_request_time()
        self.bus.write("d.".encode())
        for i in range(nbline):
            print(self.bus.readline())
        
    def set_status(self, status):
        self.check_request_time()
        self.bus.write(("s"+str(status)+".").encode())

        return 0

    def set_buzzerTime(self, time):
        self.check_request_time()
        self.bus.write(("t"+str(time)+".").encode())
        print(self.bus.readline().decode().split(','))
        return 0

    def set_RebundBtn(self, time):
        self.check_request_time()
        self.bus.write(("b"+str(time)+".").encode())
        print(self.bus.readline().decode().split(','))
        return 0

    def event_BaseA(self):
        self.check_request_time()
        self.bus.write(("e.").encode())
        print("arduino event e.")
        return 0

    def reset(self):
        self.check_request_time()
        self.bus.write(("r.").encode())
        return 0
    def get_voltage(self):
        self.check_request_time()
        self.bus.write(("v.").encode())
        print("arduino request voltage")
        return 0

    def readlines(self):
        print(self.bus.readlines())

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

    status_changed=pyqtSignal(int)
    lap_finished=pyqtSignal(int, float)
    run_finished=pyqtSignal(float)
    run_started=pyqtSignal()
    accu_signal=pyqtSignal(float)
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
