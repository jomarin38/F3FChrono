import sys
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import pyqtSignal, QObject, QTimer
from F3FChrono.gui.simulate_base_ui import Ui_MainWindow
from F3FChrono.chrono.UDPBeep import udpbeep


class SimulateBase(QtWidgets.QMainWindow, QTimer):
    close_signal = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.MainWindow = QtWidgets.QMainWindow()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.MainWindow)
        self.MainWindow.closeEvent=self.closeEvent
        self.MainWindow.show()

        self.ui.btn_send_A.clicked.connect(self.send_base_A)
        self.ui.btn_send_B.clicked.connect(self.send_base_B)
        self.ui.btn_send_wind.clicked.connect(self.send_weather)
        self.udpbeep = udpbeep("255.255.255.255", 4445)

        self.timerEvent = QTimer()
        self.timerEvent.timeout.connect(self.run)
        self.duration = 1000


    def send_base_A(self):
        self.udpbeep.sendData("simulate base " + self.ui.ip_A.text() + " " + self.ui.data_A.text())

    def send_base_B(self):
        self.udpbeep.sendData("simulate base " + self.ui.ip_B.text() + " " + self.ui.data_B.text())

    def send_weather(self):
        if self.timerEvent.isActive() == False:
            self.timerEvent.start(self.duration)
            self.ui.btn_send_wind.setText("info Processing...")
        else:
            self.ui.btn_send_wind.setText("Send info")
            self.timerEvent.stop()

    def run(self):
        self.udpbeep.sendData("simulate weather " + str(self.ui.wind_dir.value()) + " " + \
                              str(self.ui.wind_speed.value()) + " " + str(self.ui.rain.isChecked()))
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
