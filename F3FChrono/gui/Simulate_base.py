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

import sys
import collections
import random
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import pyqtSignal, QObject, QTimer
from F3FChrono.gui.simulate_base_ui import Ui_MainWindow
from F3FChrono.gui.simulate_base_widget_ui import Ui_base_widget
from F3FChrono.gui.simulate_wBtn_widget_ui import Ui_wBtn_widget
from F3FChrono.chrono.UDPSend import udpsend


class SimulateBase(QtWidgets.QMainWindow, QTimer):
    close_signal = pyqtSignal()
    baseAList = []
    baseBList = []
    wBtnList = []
 #   viewbaseAList = []
    viewbaseBList = []
#    widgetBaseList = []

    def __init__(self):
        super().__init__()
        self.MainWindow = QtWidgets.QMainWindow()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.MainWindow)
        self.MainWindow.closeEvent = self.closeEvent
        self.MainWindow.show()

        self.ui.btn_gpio_A.clicked.connect(self.send_gpio_A)
        self.ui.btn_gpio_B.clicked.connect(self.send_gpio_B)
        self.ui.btn_send_Info.clicked.connect(self.send_info)
        self.udpsend = udpsend("255.255.255.255", 4445)

        self.timerEvent = QTimer()
        self.timerEvent.timeout.connect(self.run)
        self.duration = 1000

        self.timerEventLimit = QTimer()
        self.timerEventLimit.timeout.connect(self.EventLimit)
        self.timerEventLimit.start(20000)

        self.__addbase_List(self.baseAList, self.ui.listBaseA, 3, 20, self.send_base_A)
        self.__addbase_List(self.baseBList, self.ui.listBaseB, 5, 50, self.send_base_B)
        self.__addwBtn_List(self.wBtnList, self.ui.listWBtn, 3, 70, self.send_wbtnClicked, self.send_wbtnSP, self.send_wbtnLP)


    def send_base_A(self):
        self.__sendbase(self.udpsend,
                        self.__getWidgetinQlistWidget(self.baseAList, self.ui.listBaseA, self.sender().parent().pos()))

    def send_base_B(self):
        self.__sendbase(self.udpsend,
                        self.__getWidgetinQlistWidget(self.baseBList, self.ui.listBaseB, self.sender().parent().pos()))

    def send_wbtnClicked(self):
        self.__sendwBtn(self.udpsend,
                        self.__getWidgetinQlistWidget(self.wBtnList, self.ui.listWBtn, self.sender().parent().pos()),
                        '2')

    def send_wbtnSP(self):
        self.__sendwBtn(self.udpsend,
                        self.__getWidgetinQlistWidget(self.wBtnList, self.ui.listWBtn, self.sender().parent().pos()),
                        '1')

    def send_wbtnLP(self):
        self.__sendwBtn(self.udpsend,
                        self.__getWidgetinQlistWidget(self.wBtnList, self.ui.listWBtn, self.sender().parent().pos()),
                        '0')

    def send_gpio_A(self):
        self.udpsend.sendData("simulate GPIO baseA")

    def send_gpio_B(self):
        self.udpsend.sendData("simulate GPIO baseB")

    def send_gpio_next(self):
        self.udpsend.sendData("simulate GPIO btnnext")

    def send_info(self):
        if self.timerEvent.isActive() == False:
            self.timerEvent.start(self.duration)
            self.ui.btn_send_Info.setText("info Processing...")
        else:
            self.ui.btn_send_Info.setText("Send info")
            self.timerEvent.stop()

    def run(self):
        if self.ui.speedProcessing.isChecked():
            windspeed = self.ui.wind_speed.value()
            if self.ui.windRandomVar.isChecked():
                var = self.ui.wind_var_speed.value()
                windspeed = random.uniform(int(windspeed-var/2), int(windspeed+var/2))
            self.udpsend.sendData("wind_speed " + str(windspeed) + " m/s")
        if self.ui.dirProcessing.isChecked():
            self.udpsend.sendData("wind_dir " + str(self.ui.wind_dir.value()) + " " + str(self.ui.wind_dirVoltage.value()))
        if self.ui.rainProcessing.isChecked():
            self.udpsend.sendData("rain " + str(self.ui.rain.isChecked()))
        if self.ui.picam1Processing.isChecked():
            self.udpsend.sendData("simulate info " + str(self.ui.AccuPicam1.value()) + " " + \
                            str(self.ui.rssi_picam1.value()))
        if self.ui.picam2Processing.isChecked():
            self.udpsend.sendData("simulate info " + str(self.ui.AccuPicam2.value()) + " " + \
                            str(self.ui.rssi_picam2.value()))

    def EventLimit(self):
        if self.ui.windRandomLimit.isChecked():
            windspeed = self.ui.wind_speed.value()
            var = self.ui.wind_var_limit.value()
            high = int(windspeed + var / 2)
            if high > 25:
                high = 25
            low = int(windspeed - var/2)
            if low < 3:
                low = 15
                if low >= high:
                    high = low + 5

            windspeed = random.randint(low, high)
            var = random.randint(1, var)
            self.ui.wind_speed.setValue(windspeed)
            self.ui.wind_var_speed.setValue(var)
    def closeEvent(self, event):
        self.close_signal.emit()
        event.accept()

    @staticmethod
    def __sendbase(udp, item):
        msg="simulate base " + item.ipAddress.text() + " " + item.event.text()
        print(msg)
        udp.sendData(msg)

    @staticmethod
    def __sendwBtn(udp, item, shortpush):
        msg="simulate wBtn " + item.ipAddress.text() + " " + str(shortpush)
        print(msg)
        udp.sendData(msg)

    @staticmethod
    def __addbase_List (list, uilist, nb, ip_base, event):
        for i in range(nb):
            collect = collections.OrderedDict()
            collect['QlistWidgetItem'] = QtWidgets.QListWidgetItem()
            collect['QWidget'] = QtWidgets.QWidget()
            collect['ui_widget'] = Ui_base_widget()
            list.append(collect)
            uilist.addItem(list[-1]['QlistWidgetItem'])

            list[-1]['ui_widget'].setupUi(list[-1]['QWidget'])
            list[-1]['ui_widget'].ipAddress.setText("192.168.1."+str(i+ip_base))
            list[-1]['ui_widget'].event.setText("Event")
            list[-1]['ui_widget'].buttonSend.clicked.connect(event)
            uilist.setItemWidget(list[-1]['QlistWidgetItem'], list[-1]['QWidget'])

    @staticmethod
    def __addwBtn_List (list, uilist, nb, ip_base, eventClicked, eventSP, eventLP):
        for i in range(nb):
            collect = collections.OrderedDict()
            collect['QlistWidgetItem'] = QtWidgets.QListWidgetItem()
            collect['QWidget'] = QtWidgets.QWidget()
            collect['ui_widget'] = Ui_wBtn_widget()
            list.append(collect)
            uilist.addItem(list[-1]['QlistWidgetItem'])

            list[-1]['ui_widget'].setupUi(list[-1]['QWidget'])
            list[-1]['ui_widget'].ipAddress.setText("192.168.1."+str(i+ip_base))
            list[-1]['ui_widget'].buttonSendClicked.clicked.connect(eventClicked)
            list[-1]['ui_widget'].buttonSendSP.clicked.connect(eventSP)
            list[-1]['ui_widget'].buttonSendLP.clicked.connect(eventLP)
            uilist.setItemWidget(list[-1]['QlistWidgetItem'], list[-1]['QWidget'])

    @staticmethod
    def __getWidgetinQlistWidget (list, uilist, pos):
        item = uilist.itemAt(pos)
        for index in list:
            if index['QlistWidgetItem'] == item:
                return index['ui_widget']


def main():
    app = QtWidgets.QApplication(sys.argv)
    ui = SimulateBase()

    try:
        # writer.setupDecoder()
        print("lancement IHM")
        sys.exit(app.exec_())

    except KeyboardInterrupt:
        pass
    finally:
        pass


if __name__ == '__main__':
    main()
