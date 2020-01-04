import sys
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import pyqtSignal, QObject, QTimer
from F3FChrono.gui.simulate_base_ui import Ui_MainWindow
from F3FChrono.chrono.UDPBeep import udpbeep

class SimulateBase (QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()
        self.MainWindow = QtWidgets.QMainWindow()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.MainWindow)
        self.MainWindow.show()

        self.ui.btn_send_A.clicked.connect(self.send_base_A)
        self.ui.btn_send_B.clicked.connect(self.send_base_B)

        self.udpbeep=udpbeep("255.255.255.255", 4445)

    def send_base_A(self):
        print("base A")
        self.udpbeep.sendData("simulate "+self.ui.ip_A.text()+" "+self.ui.data_A.text())




    def send_base_B(self):
        print("base B")
        self.udpbeep.sendData("simulate "+self.ui.ip_B.text()+" "+self.ui.data_B.text())

def main ():

    app = QtWidgets.QApplication(sys.argv)
    ui=SimulateBase()



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