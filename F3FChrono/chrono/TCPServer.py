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
from PyQt5.QtCore import QObject, QThread, pyqtSignal


class displayStatus():
    Init = 0
    InProgress = 1
    Close = 4


tcpPort = 10000
F3FDisplayList = list()


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


class tcpServer(QThread):
    contestRunning = pyqtSignal()
    contestInRunSig = pyqtSignal(bool)
    pilotRequestSig = pyqtSignal()
    orderDataSig = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.__debug = True
        self.connection = None
        self.client_address = None
        self.port = tcpPort
        self.contestInRunSig.connect(self.slot_contestInRun)
        self.orderDataSig.connect(self.slot_orderData)
        self.ServerSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.ServerSocket.bind((str(socket.INADDR_ANY), self.port))
        except socket.error as e:
            print(str(e))
        if self.__debug:
            print(f'Server is listing on the port {self.port}...')
        self.start()

    def slot_contestInRun(self, status):
        for i in F3FDisplayList:
            i[1].slot_contestInRun(status)

    def slot_orderData(self, data):
        for i in F3FDisplayList:
            i[1].slot_orderData(data)

    def run(self):
        while not self.isFinished():
            self.ServerSocket.listen(1)
            try:
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
            except socket.error as e:
                print("tcp server run error:" + str(e))

        self.ServerSocket.close()


