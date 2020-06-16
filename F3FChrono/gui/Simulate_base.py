import sys
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import pyqtSignal, QObject, QTimer
from F3FChrono.gui.simulate_base_ui import Ui_MainWindow
from F3FChrono.gui.simulate_base_widget_ui import Ui_base_widget
from F3FChrono.chrono.UDPBeep import udpbeep


class SimulateBase(QtWidgets.QMainWindow, QTimer):
    close_signal = pyqtSignal()
    baseAList = []
    baseBList = []
    viewbaseAList = []
    viewbaseBList = []
    widgetBaseList = []

    def __init__(self):
        super().__init__()
        self.MainWindow = QtWidgets.QMainWindow()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.MainWindow)
        self.MainWindow.closeEvent=self.closeEvent
        self.MainWindow.show()

        self.ui.btn_gpio_A.clicked.connect(self.send_gpio_A)
        self.ui.btn_gpio_B.clicked.connect(self.send_gpio_B)
        self.ui.btn_next.clicked.connect(self.send_gpio_next)
        self.ui.btn_send_wind.clicked.connect(self.send_weather)
        self.udpbeep = udpbeep("255.255.255.255", 4445)

        self.timerEvent = QTimer()
        self.timerEvent.timeout.connect(self.run)
        self.duration = 1000

        for i in range(3):
            self.baseAList.append(QtWidgets.QListWidgetItem())
            self.ui.listBaseA.addItem(self.baseAList[-1])
            self.widgetBaseList.append(QtWidgets.QWidget())
            self.viewbaseAList.append(Ui_base_widget())
            self.viewbaseAList[-1].setupUi(self.widgetBaseList[-1])
            self.viewbaseAList[-1].ipAddress.setText("192.168.1."+str(i+20))
            self.viewbaseAList[-1].event.setText("Event")
            self.viewbaseAList[-1].buttonSend.clicked.connect(self.send_base_A)
            self.ui.listBaseA.setItemWidget(self.baseAList[-1], self.widgetBaseList[-1])

        for i in range(5):
            self.baseBList.append(QtWidgets.QListWidgetItem())
            self.ui.listBaseB.addItem(self.baseBList[-1])
            self.widgetBaseList.append(QtWidgets.QWidget())
            self.viewbaseBList.append(Ui_base_widget())
            self.viewbaseBList[-1].setupUi(self.widgetBaseList[-1])
            self.viewbaseBList[-1].ipAddress.setText("192.168.1."+str(i+50))
            self.viewbaseBList[-1].event.setText("Event")
            self.viewbaseBList[-1].buttonSend.clicked.connect(self.send_base_B)
            self.ui.listBaseB.setItemWidget(self.baseBList[-1], self.widgetBaseList[-1])

    def send_base_A(self):
        p = self.sender().parent()
        item = self.ui.listBaseA.itemAt(p.pos())
        widget = self.ui.listBaseA.itemWidget(item)

        #self.udpbeep.sendData("simulate base " + widget.children()[1].text() + " " + widget.children()[3].text())
        print("simulate base " + widget.children()[1].text() + " " + widget.children()[3].text())

    def send_base_B(self):
        p = self.sender().parent()
        item = self.ui.listBaseB.itemAt(p.pos())
        widget = self.ui.listBaseB.itemWidget(item)

        # self.udpbeep.sendData("simulate base " + widget.children()[1].text() + " " + widget.children()[3].text())
        print("simulate base " + widget.children()[1].text() + " " + widget.children()[3].text())

    def send_gpio_A(self):
        self.udpbeep.sendData("simulate GPIO baseA")

    def send_gpio_B(self):
        self.udpbeep.sendData("simulate GPIO baseB")
    def send_gpio_next(self):
        self.udpbeep.sendData("simulate GPIO btnnext")

    def send_weather(self):
        if self.timerEvent.isActive() == False:
            self.timerEvent.start(self.duration)
            self.ui.btn_send_wind.setText("info Processing...")
        else:
            self.ui.btn_send_wind.setText("Send info")
            self.timerEvent.stop()

    def run(self):
        self.udpbeep.sendData("wind " + str(self.ui.wind_dir.value()) + " " + \
                              str(self.ui.wind_speed.value()))
        self.udpbeep.sendData("rain " + str(self.ui.rain.isChecked()))
        self.udpbeep.sendData("simulate info " + str(self.ui.AccuRace.value()) + " " + \
                              str(self.ui.rssi_picam1.value()) + " " + str(self.ui.rssi_picam2.value()))

    def closeEvent(self, event):
        self.close_signal.emit()
        event.accept()

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
