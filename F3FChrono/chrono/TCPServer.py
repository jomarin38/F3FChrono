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


    def init(self):
        self.status = displayStatus.Init
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
    def init(self):
        self.status = displayStatus.Init
        self.currentData = collections.OrderedDict()
        self.connection = None
        self.bp_p100Sig = None
        self.bp_p1000Sig = None
        self.bp_validSig = None
        self.bp_cancelSig = None
        self.bp_nullFlightSig = None
        self.bp_reflySig = None
        self.initCurrentData()

    def initCurrentData(self):
        self.DCDisplay = False
        self.currentData["contestInProgress"] = False
        self.currentData["round"] = "0"
        self.currentData["pilot"] = "pilotTest"
        self.currentData["bib"] = "0"
        self.currentData["group"] = "1"
        self.currentData["weatherdir"] = -1
        self.currentData["weatherspeed"] = -1
        self.currentData["weatherrain"] = False
        self.currentData["weatherstatus"] = ""
        self.clearRunData()

    def clearRunData(self):
        self.currentData["runstatus"] = chronoStatus.InWait
        self.currentData["runbasenb"] = 0
        self.currentData["basetime"] = 0.00
        self.currentData["runtime"] = 0.00
        self.currentData["penalty"] = 0
        self.currentData["refly"] = False
        self.currentData["nullflight"] = False
        self.currentData["runvalidated"] = False

    def setConnectionhandle(self, connection, display, client_address):
        self.connection = connection
        self.displayHandle = display
        self.client_address = client_address

    def setSignal(self, p100, p1000, valid, cancel, nullFlight, refly):
        self.bp_p100Sig = p100
        self.bp_p1000Sig = p1000
        self.bp_nullFlightSig = nullFlight
        self.bp_reflySig = refly
        self.bp_validSig = valid
        self.bp_cancelSig = cancel


    def run(self):
        print("DCDisplay worker running")
        while self.status != displayStatus.Close and self.connection is not None:
            if self.status == displayStatus.Init:
                print("DCDisplay - status init")
                try:
                    self.connection.sendall(bytes("F3FDCDisplayServerStarted", "utf-8"))
                except socket.error as e:
                    print(str(e))
                self.status = displayStatus.InProgress
                self.displayCreateLines()
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
                        F3FDCDisplayList.remove((self.connection, self.displayHandle, self.client_address))
                else:
                    self.datareceived(data)

        self.finished.emit()
        del self.displayHandle

    def datareceived(self, data):
        print(data)
        m = data.decode("utf-8").split()
        if len(m) > 0:
            if self.DCDisplay:
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
            if m[0] == "analog":
                print("DCDisplay - Accu : " + m[2] + "V")
        else:
            print(data)

    def displayCreateLines(self):
        lines = ["", "", "", ""]
        if self.connection is not None and self.status == displayStatus.InProgress:
            if self.currentData["contestInProgress"]:
                self.displayCreateLineRoundInfo(send=True)
                self.displayCreateLineWeatherInfo(send=True)
                self.displayCreateLineRunInfo(send=True)
                self.displayCreateLineRunStatus(send=True)

            else:
                self.displayCreateLineAwaitingContest(send=True)

    def displayCreateLineAwaitingContest(self, send=False):
        if self.connection is not None and self.status == displayStatus.InProgress and send:
            try:
                self.connection.sendall(bytes("CLEAR:\n", "utf-8"))
                if self.DCDisplay:
                    self.connection.sendall(bytes("line:0:" + "DC Display" + "\n", "utf-8"))
                else:
                    self.connection.sendall(bytes("line:0:" + "JUDGE Display" + "\n", "utf-8"))

                self.connection.sendall(bytes("line:2:" + "AWAITING CONTEST" + "\n", "utf-8"))
                self.connection.sendall(bytes("line:3:" + self.client_address[0] + "\n", "utf-8"))
            except socket.error as e:
                print(str(e))
            self.displayCreateLineWeatherInfo(send=True)

    def displayCreateLineRoundInfo(self, send=False):
        line = ("R" + self.currentData["round"] + " G" + self.currentData["group"] + " B" + self.currentData["bib"] +
                " " + self.currentData["pilot"])
        if self.connection is not None and self.status == displayStatus.InProgress and send:
            try:
                self.connection.sendall(bytes("line:0:" + line + "\n", "utf-8"))
            except socket.error as e:
                print(str(e))
        return line

    def displayCreateLineWeatherInfo(self, send=False):
        line = ("{:+3.0f}".format(self.currentData["weatherdir"]) + " - " +
                "{:+5.1f}".format(self.currentData["weatherspeed"]) + "m/s " +
                self.currentData["weatherstatus"])
        if self.connection is not None and self.status == displayStatus.InProgress and send:
            try:
                self.connection.sendall(bytes("line:1:" + line + "\n", "utf-8"))
            except socket.error as e:
                print(str(e))
        return line

    def displayCreateLineRunInfo(self, send=False):
        line = self.getStatusString() + "  "
        if (self.currentData["runstatus"] == chronoStatus.InProgressA or
                self.currentData["runstatus"] == chronoStatus.InProgressB or
                self.currentData["runstatus"] == chronoStatus.WaitAltitude):
            line = line + "{:0>.2f}".format(self.currentData["basetime"]) + " B" + str(self.currentData["runbasenb"])

        if self.connection is not None and self.status == displayStatus.InProgress and send:
            try:
                self.connection.sendall(bytes("line:2:" + line + "\n", "utf-8"))
            except socket.error as e:
                print(str(e))
        return line

    def displayCreateLineRunStatus(self, send=False):
        acceptanceStr = ""
        if self.currentData["nullflight"]:
            acceptanceStr = "NULLFLIGHT"
        if self.currentData["refly"]:
            acceptanceStr = "REFLY"

        line = ("Time " + "{:0>.2f}".format(self.currentData["runtime"]) + " P" + str(self.currentData["penalty"])
                + " " + acceptanceStr)
        print(line)
        if self.connection is not None and self.status == displayStatus.InProgress and send:
            try:
                self.connection.sendall(bytes("line:3:" + line + "\n", "utf-8"))
            except socket.error as e:
                print(str(e))
        return line

    def getStatusString(self):
        if self.currentData["runstatus"] == chronoStatus.InWait:
            return "InWait"
        if self.currentData["runstatus"] == chronoStatus.WaitLaunch:
            return "WaitLaunch"
        if self.currentData["runstatus"] == chronoStatus.Launched:
            return "Launched"
        if self.currentData["runstatus"] == chronoStatus.Late:
            return ""
        if self.currentData["runstatus"] == chronoStatus.InStart:
            return "InStart"
        if self.currentData["runstatus"] == chronoStatus.InStartLate:
            return "InStartLate"
        if (self.currentData["runstatus"] == chronoStatus.InProgressA or
                self.currentData["runstatus"] == chronoStatus.InProgressB):
            return "InProgress"
        if self.currentData["runstatus"] == chronoStatus.WaitAltitude:
            return "WaitAltitude"
        if self.currentData["runstatus"] == chronoStatus.Finished:
            return "Finished"

    def slot_roundInfo(self, contestInProgress, competitor, round):
        self.currentData["contestInProgress"] = contestInProgress
        if contestInProgress:
            self.currentData["round"] = str(len(round.event.valid_rounds) + 1)
            self.currentData["bib"] = str(competitor.get_bib_number())
            self.currentData["pilot"] = competitor.display_name()
            self.currentData["group"] = str(round.find_group(competitor).group_number)
            self.clearRunData()
            self.displayCreateLineRoundInfo(send=True)
            self.displayCreateLineRunStatus(send=True)
            self.displayCreateLineRunInfo(send=True)
        else:
            self.displayCreateLines()

    def slot_weatherInfo(self, speed, dir, rain, status):
        self.currentData["weatherdir"] = dir
        self.currentData["weatherspeed"] = speed
        self.currentData["weatherrain"] = rain
        self.currentData["weatherstatus"] = status
        self.displayCreateLineWeatherInfo(send=True)

    def slot_runStatus(self, status):
        self.currentData["runstatus"] = status
        #if (self.currentData["runstatus"] != chronoStatus.InProgressA and
        #        self.currentData["runstatus"] != chronoStatus.InProgressB and
        #        self.currentData["runstatus"] != chronoStatus.WaitAltitude):
        self.displayCreateLineRunInfo(send=True)

    def slot_runLap(self, lap, laptime):
        self.currentData["runbasenb"] = lap
        self.currentData["basetime"] = self.currentData["basetime"] + laptime
        self.displayCreateLineRunInfo(send=True)

    def slot_penalty(self, penalty):
        self.currentData["penalty"] = self.currentData["penalty"] + penalty
        self.displayCreateLineRunStatus(send=True)

    def slot_runtime(self, runtime):
        self.currentData["runtime"] = runtime
        self.displayCreateLineRunStatus(send=True)

    def slot_clearPenalty(self):
        self.currentData["penalty"] = 0
        self.displayCreateLineRunStatus(send=True)

    def slot_refly(self):
        self.currentData["refly"] = True
        self.displayCreateLineRunStatus(send=True)

    def slot_nullflight(self):
        self.currentData["nullflight"] = True
        self.displayCreateLineRunStatus(send=True)

    def slot_runvalidated(self):
        self.currentData["runvalidated"] = True
        self.displayCreateLineRunStatus(send=True)

    def slot_setDCDisplay(self, dc):
        self.DCDisplay=dc
        self.slot_roundInfo(False, 0, 0)
    def isDCDisplay(self):
        return self.DCDisplay

class tcpServer(QThread):
    contestRunning = pyqtSignal()
    contestInRunSig = pyqtSignal(bool)
    pilotRequestSig = pyqtSignal()
    orderDataSig = pyqtSignal(str)
    bp_P100Sig = pyqtSignal()
    bp_P1000Sig = pyqtSignal()
    bp_ReflySig = pyqtSignal()
    bp_NullFlightSig = pyqtSignal()
    bp_ValidSig = pyqtSignal()
    bp_CancelSig = pyqtSignal()
    newDCDisplaySig = pyqtSignal()
    dcDisplayListSig = pyqtSignal(list)

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

    def slot_orderData(self, data):
        for i in F3FDisplayList:
            i[1].slot_orderData(data)

    def slot_roundInfo(self, contestInProgress, competitor, round):
        for i in F3FDCDisplayList:
            i[1].slot_roundInfo(contestInProgress, competitor, round)

    def slot_weatherInfo(self, wind_speed, wind_speed_unit, wind_dir, rain, alarm, status):
        for i in F3FDCDisplayList:
            i[1].slot_weatherInfo(wind_speed, wind_dir, rain, status)

    def slot_runStatus(self, status):
        print(status)
        for i in F3FDCDisplayList:
            i[1].slot_runStatus(status)

    def slot_runLap(self, lap, laptime):
        for i in F3FDCDisplayList:
            i[1].slot_runLap(lap, laptime)

    def slot_runtime(self, runtime):
        for i in F3FDCDisplayList:
            i[1].slot_runtime(runtime)

    def slot_penalty(self, penalty):
        for i in F3FDCDisplayList:
            i[1].slot_penalty(penalty)

    def slot_clearPenalty(self):
        for i in F3FDCDisplayList:
            i[1].slot_clearPenalty()

    def slot_refly(self):
        for i in F3FDCDisplayList:
            i[1].slot_refly()

    def slot_nullflight(self):
        for i in F3FDCDisplayList:
            i[1].slot_nullflight()

    def slot_runvalidated(self):
        for i in F3FDCDisplayList:
            i[1].slot_runvalidated()

    def getDcDisplayList(self):
        temp = list()
        for i in F3FDCDisplayList:
             temp.append((i[2], i[1].isDCDisplay()))
        self.dcDisplayListSig.emit(temp)

    def setDcDisplayAsDc(self, data):
        for i in F3FDCDisplayList:
            if i[2][0] == data:
                i[1].slot_setDCDisplay(True)
            else:
                i[1].slot_setDCDisplay(False)
        self.getDcDisplayList()
    def run(self):
        while not self.isFinished():
            if self.status == serverStatus.Init:
                try:
                    self.ServerSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    self.ServerSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
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
                        F3FDCDisplayList.append((self.connection, DCdisplayHandle, self.client_address))

                        DCdisplayHandle.finished.connect(DCdisplayHandle.quit)
                        DCdisplayHandle.finished.connect(DCdisplayHandle.deleteLater)
                        DCdisplayHandle.setConnectionhandle(self.connection, DCdisplayHandle, self.client_address)
                        DCdisplayHandle.setSignal(self.bp_P100Sig, self.bp_P1000Sig, self.bp_ValidSig,
                                                  self.bp_CancelSig,
                                                  self.bp_NullFlightSig, self.bp_ReflySig)
                        DCdisplayHandle.start()
                        print("F3FDC_Display tcp client thread start")
                        haveDCDisplay = False
                        for i in F3FDCDisplayList:
                            if i[1].isDCDisplay():
                                haveDCDisplay = True

                        if haveDCDisplay == False:
                            print("DC Display : ", self.connection, self.client_address)
                            DCdisplayHandle.slot_setDCDisplay(True)
                        else:
                            print("Judge Display : ", self.connection, self.client_address)
                            DCdisplayHandle.slot_setDCDisplay(False)
                        self.newDCDisplaySig.emit()

                except socket.error as e:
                    del self.ServerSocket
                    self.ServerSocket = None
                    self.status = serverStatus.Init
                    print("tcp server run error:" + str(e))

        self.ServerSocket.close()
