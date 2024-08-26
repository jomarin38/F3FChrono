import json, serial, time
from PyQt5.QtCore import QObject, pyqtSignal, QTimer, QThread, QCoreApplication
from PyQt5 import QtWidgets
import threading

from PyQt5.QtWidgets import QApplication

from debugdisplay import Ui_MainWindow

from unidecode import unidecode

class nanoDCDisplay(QThread):
    msgsig = pyqtSignal(bool, str) #send : True, data

    def __init__(self, ):
        super().__init__()
        self.bus = None
        self.__debug = True
        self.asGateway = False

    def startseq(self, asgateway):
        self.bus = serial.Serial(port='/dev/ttyUSB1', baudrate=19200, parity=serial.PARITY_NONE,
                                 stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS, timeout=0.2)
        self.asGateway = asgateway
        self.terminated = False
        self.start()

    def stopseq(self):
        self.terminated = True
        if self.bus is not None:
            self.bus.close()
            self.bus = None

    def send(self, data):
        if self.bus is not None:
            try:
                self.bus.write(data.encode())
                self.msgsig.emit(True, data)
            except serial.SerialException as e:
                if self.__debug:
                    print("nano_Send serial exception : ", e)
            except TypeError as e:
                if self.__debug:
                    print("nano_Send error : ", e)
                self.terminated = True
                self.bus.close()
                self.bus = None

    def wemosMsg(self, send, data):
        if self.asGateway:
            if not send:
                self.send(data)

    def run(self):
        while not self.terminated:
            try:
                if self.bus.inWaiting() > 0:
                    data = self.bus.readline().decode(encoding='utf-8', errors='ignore')
                    self.msgsig.emit(False, data)
                    if self.__debug:
                        print("nano receive:", data)
            except serial.SerialException as e:
                if self.__debug:
                    print("nano Receive serial exception : ", e)
                return None
            except TypeError as e:
                if self.__debug:
                    print("nano Receive error : ", e)
                self.bus.close()
                self.bus = None
                return None
            time.sleep(0.002)

class wemosDCDisplay(QThread):
    msgsig = pyqtSignal(bool, str) #send : True, data

    def __init__(self, ):
        super().__init__()
        self.bus = None
        self.__debug = True
        self.asGateway = False

    def startseq(self, asgateway):
        self.bus = serial.Serial(port='/dev/ttyUSB2', baudrate=19200, parity=serial.PARITY_NONE,
                                 stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS, timeout=0.2)
        self.asGateway = asgateway
        self.terminated = False
        self.start()

    def stopseq(self):
        self.terminated = True
        if self.bus is not None:
            self.bus.close()
            self.bus = None

    def send(self, data):
        if self.bus is not None:
            try:
                self.bus.write(data.encode())
                self.msgsig.emit(True, data)
            except serial.SerialException as e:
                if self.__debug:
                    print("wemos_Send serial exception : ", e)
            except TypeError as e:
                if self.__debug:
                    print("wemos_Send error : ", e)
                self.terminated = True
                self.bus.close()
                self.bus = None
    def nanoMsg(self, send, data):
        if self.asGateway:
            if not send:
                self.send(data)

    def run(self):
        while not self.terminated:
            try:
                if self.bus.inWaiting() > 0:
                    data = self.bus.readline().decode(encoding='utf-8', errors='ignore')
                    self.msgsig.emit(False, data)
                    if not self.asGateway:
                        self.send('1')
                    if self.__debug:
                        print("wemos receive:",data)
            except serial.SerialException as e:
                if self.__debug:
                    print("wemos Receive serial exception : ", e)
                return None
            except TypeError as e:
                if self.__debug:
                    print("wemos Receive error : ", e)
                self.bus.close()
                self.bus = None
                return None
            time.sleep(0.002)

class mainWindow(QObject):
    startSig = pyqtSignal(bool)
    stopSig = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.MainWindow = QtWidgets.QMainWindow()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.MainWindow)
        self.MainWindow.show()
        self.ui.startBtn.clicked.connect(self.startfct)
        self.ui.stopBtn.clicked.connect(self.stopSig.emit)


    def startfct(self):
        self.startSig.emit(self.ui.asGateway.isChecked())

    def addWemosMsg(self, send, data):
        if send :
            msg = "Send:"
        else:
            msg="receive:"
        self.ui.wemosText.append(msg + data)

        msg = data.split(':')
        if len(msg)>0:
            if msg[0]=='D':
                if msg[1]=='C':
                    self.ui.displayline0.setText("")
                    self.ui.displayline1.setText("")
                    self.ui.displayline2.setText("")
                    self.ui.displayline3.setText("")
                if msg[1]=='L':
                    if msg[2]=='0':
                        self.ui.displayline0.setText(msg[3])
                    if msg[2]=='1':
                        self.ui.displayline1.setText(msg[3])
                    if msg[2]=='2':
                        self.ui.displayline2.setText(msg[3])
                    if msg[2]=='3':
                        self.ui.displayline3.setText(msg[3])

    def addNanoMsg(self, send, data):
        if send :
            msg = "Send:"
        else:
            msg="receive:"
        self.ui.nanoText.append(msg + data)

if __name__ == '__main__':
    import os
    import sys
    #app = QtWidgets.QApplication(sys.argv)
    app = QApplication(sys.argv)
    abspath = os.path.abspath(__file__)
    dname = os.path.dirname(abspath)

    wemosDisplay = wemosDCDisplay()
    nanoDisplay = nanoDCDisplay()
    ui = mainWindow()
    wemosDisplay.msgsig.connect(ui.addWemosMsg)
    wemosDisplay.msgsig.connect(nanoDisplay.wemosMsg)
    nanoDisplay.msgsig.connect(ui.addNanoMsg)
    nanoDisplay.msgsig.connect(wemosDisplay.nanoMsg)
    ui.startSig.connect(wemosDisplay.startseq)
    ui.startSig.connect(nanoDisplay.startseq)
    ui.stopSig.connect(wemosDisplay.stopseq)
    ui.stopSig.connect(nanoDisplay.stopseq)

    sys.exit(app.exec_())
