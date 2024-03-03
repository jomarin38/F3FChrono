#
# This file is part of the F3FChrono distribution (https://github.com/jomarin38/F3FChrono).
# Copyright (c) 2021 Sylvain DAVIET, Joel MARIN.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#


import socket
import collections
from PyQt5.QtCore import QObject, QThread, pyqtSignal
from F3FChrono.chrono.Chrono import chronoStatus


class displayStatus():
    Init = 0
    InProgress = 1
    Close = 4

class serverStatus():
    Init = 0
    InProgress = 1

tcpPort = 10000
F3FDisplayList = list()
F3FDCDisplayList = list()


class tcpF3FDisplayWorker(QThread):
    finished = pyqtSignal()
    status = displayStatus.Init

    def init(self):
        self.connection = None
        self.contestRunningSig = None
        self.pilotRequestSig = None

    def setConnectionhandle(self, connection, display):
        self.connection = connection
        self.displayHandle = display

    def setSignal(self, contestRunning, pilotReqSig):
        self.contestRunningSig = contestRunning
        self.pilotRequestSig = pilotReqSig


    def slot_contestInRun(self, status):
        print("tcp F3FDisplay Thread slot_contestInRun")
        self.connection.sendall(bytes("ContestRunning? " + str(status), "utf-8"))

    def slot_orderData(self, data):
        self.connection.sendall(bytes("ContestData " + str(data), "utf-8"))
    def run(self):
        print("display worker running")
        while self.status != displayStatus.Close and self.connection is not None:
            if self.status == displayStatus.Init:
                print("display status init")
                try:
                    self.connection.sendall(bytes("F3FDisplayServerStarted", "utf-8"))
                except socket.error as e:
                    print(str(e))
                self.status = displayStatus.InProgress
            else:
                try:
                    data = self.connection.recv(1024)
                except socket.error as e:
                    print(str(e))
                if data == b'':
                    try:
                        self.connection.sendall(bytes("Test", "utf-8"))
                    except socket.error as e:
                        print(str(e))
                        self.connection.close()
                        self.status = displayStatus.Close
                        F3FDisplayList.remove((self.connection, self.displayHandle))
                else:
                    self.datareceived(data)

        self.finished.emit()
        del self.displayHandle
    def datareceived(self, data):
        m = data.decode("utf-8").split()
        if m[0] == "ContestRunning?":
            print("ContestRunning?")
            if self.contestRunningSig is not None:
                self.contestRunningSig.emit()
        elif m[0] == "getPilotList":
            print("getPilotList Request")
            if self.pilotRequestSig is not None:
                self.pilotRequestSig.emit()
        else:
            print(data)

class tcpF3FDCDisplayWorker(QThread):
    finished = pyqtSignal()
    status = displayStatus.Init
    currentData = collections.OrderedDict()

    def init(self):
        self.connection = None
        self.bp_p100Sig = None
        self.bp_p1000Sig = None
        self.bp_validSig = None
        self.bp_cancelSig = None
        self.bp_nullFlightSig = None
        self.bp_reflySig = None
        self.initCurrentData()

    def initCurrentData(self):
        self.currentData["round"] = 0
        self.currentData["pilot"] = ""
        self.currentData["bib"] = 0
        self.currentData["weatherdir"] = 0
        self.currentData["weatherspeed"] = 10
        self.currentData["runstatus"] = chronoStatus.InWait
        self.currentData["runbasenb"] = 0
        self.currentData["runtime"] = 00.00
        self.currentData["runAcceptance"] = "refly"

    def setConnectionhandle(self, connection, display):
        self.connection = connection
        self.displayHandle = display

    def setSignal(self, p100, p1000, valid, cancel, nullFlight, refly):
        self.bp_p100Sig = p100
        self.bp_p1000Sig = p1000
        self.bp_nullFlightSig = nullFlight
        self.bp_reflySig = refly
        self.bp_validSig = valid
        self.bp_cancelSig = cancel

    def slot_conteststatus(self, status):
        print("DCDisplay - contest status" + status)

    def slot_winddata(self, speed, dir):
        print("DCDisplay - wind data - vitesse : " + "{:0>.1f}".format(speed) + ", dir : " + "{:0>.1f}".format(dir))

    def slot_pilotchanged(self, bib, name):
        print("DCDisplay - pilot bib : " + bib + " - " + name)

    def slot_roundchanged(self, value):
        print("DCDisplay - round : " + value)

    def slot_penalty(self, value):
        print ("DCDisplay - penalty : " + value)

    def slot_nullflight(self):
        print("DCDisplay - null flight")
    def run(self):
        print("DCDisplay worker running")
        while self.status != displayStatus.Close and self.connection is not None:
            if self.status == displayStatus.Init:
                print("DCDisplay - status init")
                try:
                    self.connection.sendall(bytes("F3FDCDisplayServerStarted", "utf-8"))
                except socket.error as e:
                    print(str(e))
                try:
                    msgdisplay = ("line1:RND:5 BIB:3 DUPONT\n" + "line2:Dir:-3   Speed:13\n" +
                                "line3:Started    Base:07\n" + "line4:Time:55.66   VALID\n")
                    self.connection.sendall(bytes(msgdisplay, "utf-8"))
                except socket.error as e:
                    print(str(e))
                self.status = displayStatus.InProgress
            else:
                try:
                    data = self.connection.recv(1024)
                except socket.error as e:
                    print(str(e))
                if data == b'':
                    try:
                        self.connection.sendall(bytes("Test", "utf-8"))
                    except socket.error as e:
                        print(str(e))
                        self.connection.close()
                        self.status = displayStatus.Close
                        F3FDCDisplayList.remove((self.connection, self.displayHandle))
                else:
                    self.datareceived(data)

        self.finished.emit()
        del self.displayHandle

    def datareceived(self, data):
        print(data)
        m = data.decode("utf-8").split()
        if len(m) > 0:
            if m[0] == "P100" and self.bp_p100Sig is not None:
                print("DCDisplay - BP P100 request")
                self.bp_p100Sig.emit()
            elif m[0] == "P1000" and self.bp_p1000Sig is not None:
                print("DCDisplay - BP P1000 request")
                self.bp_p1000Sig.emit()
            elif m[0] == "Refly" and self.bp_reflySig is not None:
                print("DCDisplay - BP Refly request")
                self.bp_reflySig.emit()
            elif m[0] == "NullFlight" and self.bp_nullFlightSig is not None:
                print("DCDisplay - BP NullFlight request")
                self.bp_nullFlightSig.emit()
            elif m[0] == "Valid" and self.bp_validSig is not None:
                print("DCDisplay - BP Valid request")
                self.bp_validSig.emit()
            elif m[0] == "Cancel" and self.bp_cancelSig is not None:
                print("DCDisplay - BP Cancel request")
                self.bp_cancelSig.emit()
            elif m[0] == "analog":
                print("DCDisplay - Accu : " + m[2] + "V")
        else:
            print(data)

class tcpServer(QThread):
    contestRunning = pyqtSignal()
    contestInRunSig = pyqtSignal(bool)
    pilotRequestSig = pyqtSignal()
    orderDataSig = pyqtSignal(str)
    bp_P100Sig = pyqtSignal()
    bp_P1000Sig  = pyqtSignal()
    bp_ReflySig  = pyqtSignal()
    bp_NullFlightSig  = pyqtSignal()
    bp_ValidSig  = pyqtSignal()
    bp_CancelSig  = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.__debug = True
        self.connection = None
        self.client_address = None
        self.port = tcpPort
        self.contestInRunSig.connect(self.slot_contestInRun)
        self.orderDataSig.connect(self.slot_orderData)
        self.ServerSocket = None
        self.status = serverStatus.Init
        self.start()

    def slot_contestInRun(self, status):
        for i in F3FDisplayList:
            i[1].slot_contestInRun(status)
        for i in F3FDCDisplayList:
            i[1].slot_contestInRun(status)

    def slot_orderData(self, data):
        for i in F3FDisplayList:
            i[1].slot_orderData(data)

    def run(self):
        while not self.isFinished():
            if self.status == serverStatus.Init:
                try:
                    self.ServerSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    self.ServerSocket.bind((str(socket.INADDR_ANY), self.port))
                except socket.error as e:
                    print(str(e))
                    del self.ServerSocket
                    self.ServerSocket = None
                else:
                    self.status = serverStatus.InProgress
                    if self.__debug:
                        print(f'Server is listening on the port {self.port}...')
            elif self.status == serverStatus.InProgress:
                try:
                    self.ServerSocket.listen(1)
                    self.connection, self.client_address = self.ServerSocket.accept()
                    data = ''
                    try:
                        data = str(self.connection.recv(1024), "utf-8")
                    except socket.error as e:
                        print(str(e))
                    if self.__debug:
                        print(f'{self.client_address}-data received : {data}')

                    if data == "F3FDisplay":
                        displayHandle = tcpF3FDisplayWorker()
                        displayHandle.init()
                        F3FDisplayList.append((self.connection, displayHandle))


                        displayHandle.finished.connect(displayHandle.quit)
                        displayHandle.finished.connect(displayHandle.deleteLater)
                        displayHandle.setConnectionhandle(self.connection, displayHandle)
                        displayHandle.setSignal(self.contestRunning, self.pilotRequestSig)
                        displayHandle.start()
                        print("F3FDisplay tcp client thread start")
                    if data == "F3FDCDisplay":
                        DCdisplayHandle = tcpF3FDCDisplayWorker()
                        DCdisplayHandle.init()
                        F3FDCDisplayList.append((self.connection, DCdisplayHandle))


                        DCdisplayHandle.finished.connect(DCdisplayHandle.quit)
                        DCdisplayHandle.finished.connect(DCdisplayHandle.deleteLater)
                        DCdisplayHandle.setConnectionhandle(self.connection, DCdisplayHandle)
                        DCdisplayHandle.setSignal(self.bp_P100Sig, self.bp_P1000Sig, self.bp_ValidSig, self.bp_CancelSig,
                                                  self.bp_NullFlightSig, self.bp_ReflySig)
                        DCdisplayHandle.start()
                        print("F3FDC_Display tcp client thread start")

                except socket.error as e:
                    del self.ServerSocket
                    self.ServerSocket = None
                    self.status = serverStatus.Init
                    print("tcp server run error:" + str(e))

        self.ServerSocket.close()


