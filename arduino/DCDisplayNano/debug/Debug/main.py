import json, serial, time
from PyQt5.QtCore import QObject, pyqtSignal, QTimer, QThread, QCoreApplication
from PyQt5 import QtWidgets
import threading

from PyQt5.QtWidgets import QApplication

from debugdisplay import Ui_MainWindow

from unidecode import unidecode


class config:
    def __init__(self, file_name=None):
        self.conf = ""
        self.configFileName = file_name
        if file_name is not None:
            self.read(file_name)


    def read(self, config_file):
        try:
            self.conf = json.load(open(config_file,'r'))
            self.configFileName = config_file
        except IOError:
            pass
        except:
            raise

class serialDCDisplay(QThread):
    rs232msgok = pyqtSignal()
    rs232msgnok = pyqtSignal()
    msgsig = pyqtSignal(str)

    def __init__(self, conf):
        super().__init__()
        self.bus = None
        self.conf = conf
        self.__debug = False
        self.rs232msgok.connect(self.slot_nextseq)
        self.timer = QTimer()
        self.timer.timeout.connect(self.slot_timer)

    def startseq(self):
        self.bus = serial.Serial(port='/dev/ttyUSB1', baudrate=19200, parity=serial.PARITY_NONE,
                                 stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS, timeout=0.2)
        self.terminated = False
        self.start()
        self.seqindex = 0
        self.timer.singleShot(2000, self.slot_timer)

    def stopseq(self):
        self.terminated = True
        self.timer.stop()
        if self.bus is not None:
            self.bus.close()
            self.bus = None

    def slot_timer(self):
        msg = self.conf.conf['msg'][self.conf.conf['sequencer'][self.seqindex]['msg']]
        msg = unidecode(msg)
        self.msgsig.emit(msg)
        if self.__debug:
            print (msg)

        self.sendmessage(msg)
        #self.slot_nextseq()


    def slot_nextseq(self):
        self.timer.singleShot(self.conf.conf['sequencer'][self.seqindex]['timer'], self.slot_timer)
        self.seqindex += 1
        if self.seqindex>=len(self.conf.conf['sequencer']):
            self.seqindex = 0

    def sendmessage(self, data):
        try:
            if self.bus is not None:
                self.bus.write(data.encode())
        except serial.SerialException as e:
            if self.__debug:
                print("RS232_Send serial exception : ", e)
        except TypeError as e:
            if self.__debug:
                print("RS232_Send error : ", e)
            self.terminated = True
            self.bus.close()
            self.bus = None

    def run(self):
        while not self.terminated:
            try:
                if self.bus.inWaiting() > 0:
                    data = self.bus.readline().decode()
                    if data[0]=='1':
                        self.rs232msgok.emit()
                    else:
                        self.rs232msgnok.emit()
                    self.msgsig.emit("Receive : " + data)
                    if self.__debug:
                        print("rs232 receive : ",data)
            except serial.SerialException as e:
                if self.__debug:
                    print("RS232 Receive serial exception : ", e)
                return None
            except TypeError as e:
                if self.__debug:
                    print("RS232 Receive error : ", e)
                self.bus.close()
                self.bus = None
                return None
            time.sleep(0.002)

class mainWindow(QObject):
    def __init__(self, startfct, stopfct, msgsig):
        super().__init__()
        self.MainWindow = QtWidgets.QMainWindow()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.MainWindow)
        self.MainWindow.show()
        if startfct is not None:
            self.ui.startBtn.clicked.connect(startfct)
        if stopfct is not None:
            self.ui.stopBtn.clicked.connect(stopfct)
        if msgsig is not None :
            msgsig.connect(self.addStringMsg)

    def addStringMsg(self, data):
        print("ui", data)
        self.ui.textSequence.append(data)

if __name__ == '__main__':
    import os
    import sys
    #app = QtWidgets.QApplication(sys.argv)
    app = QApplication(sys.argv)
    abspath = os.path.abspath(__file__)
    dname = os.path.dirname(abspath)

    conf = config("config.json")
    dcDisplay = serialDCDisplay(conf)
    ui = mainWindow(dcDisplay.startseq, dcDisplay.stopseq, dcDisplay.msgsig)

    sys.exit(app.exec_())
