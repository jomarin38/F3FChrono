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


class tcpF3FDisplayWorker(QObject):
    finished = pyqtSignal()
    status = displayStatus.Init

    def init(self):
        self.connection = None
        self.contestRunningSig = None
        self.pilotRequestSig = None

    def setConnectionhandle(self, connection):
        self.connection = connection

    def setSignal(self, contestRunning, pilotReqSig):
        self.contestRunningSig = contestRunning
        self.pilotRequestSig = pilotReqSig

    def run(self):
        print("display worker running")
        while self.status != displayStatus.Close and self.connection is not None:
            if self.status == displayStatus.Init:
                try:
                    self.connection.sendall(bytes("F3FDisplayServerStarted", "utf-8"))
                except socket.error as e:
                    print(str(e))
                self.status = displayStatus.InProgress
            else:
                try:
                    data = str(self.connection.recv(1024), "utf-8")
                except socket.error as e:
                    print(str(e))
                if data == "ContestRunning?":
                    print("ContestRunning?")
                    if self.contestRunningSig is not None:
                        self.contestRunningSig.emit()
                elif data == "getPilotList":
                    print("getPilotList Request")
                    if self.pilotRequestSig is not None:
                        self.pilotRequestSig.emit()

        self.finished.emit()



class tcpServer(QThread):
    contestRunning = pyqtSignal()
    pilotRequestSig = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.__debug = True
        self.connection = None
        self.client_address = None
        self.port = tcpPort
        self.ServerSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.ServerSocket.bind((str(socket.INADDR_ANY), self.port))
        except socket.error as e:
            print(str(e))
        if self.__debug:
            print(f'Server is listing on the port {self.port}...')
        self.start()

    def contestInRun(self, status):
        if len(F3FDisplayList)>0:
            F3FDisplayList[-1][0].sendall(bytes("ContestRunning? "+str(status),"utf-8"))

    def sendOrderData(self, data):
        if len(F3FDisplayList)>0:
            F3FDisplayList[-1][0].sendall(bytes("ContestData " + str(data), "utf-8"))

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
                    threadHandle = QThread()
                    displayHandle = tcpF3FDisplayWorker()
                    displayHandle.init()
                    F3FDisplayList.append((self.connection, threadHandle, displayHandle))
                    displayHandle.moveToThread(threadHandle)
                    threadHandle.started.connect(displayHandle.run)
                    displayHandle.finished.connect(threadHandle.quit)
                    displayHandle.finished.connect(displayHandle.deleteLater)
                    threadHandle.finished.connect(threadHandle.deleteLater)
                    displayHandle.setConnectionhandle(self.connection)
                    displayHandle.setSignal(self.contestRunning, self.pilotRequestSig)
                    threadHandle.start()
            except socket.error as e:
                print(str(e))
            if self.__debug:
                print(f'Connection address {self.client_address}')
        self.ServerSocket.close()
