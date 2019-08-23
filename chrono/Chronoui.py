import sys
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import QObject, pyqtSignal
from chrono.GUI.Qt5chrono import Ui_MainWindow


class MyForm(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.init()

    def init(self):
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setGeometry(0, 0, 480, 300)
        self.uiHome = uiHome(self.ui)
        self.uiPiCAM = uiPiCAM(self.ui)
        self.uiChrono = uiChrono(self.ui)
        self.uiPractice = uiPractice(self.ui)
        self.connectEvents()
        self.BaseEvent = BaseEvent()

    def connectEvents(self):
        self.uiHome.connectEvents()
        self.uiPiCAM.connectEvents()
        self.uiChrono.connectEvents()
        self.uiPractice.connectEvents()

    def GetBaseEventID(self):
        return self.BaseEvent

    def UpdateHMI(self, msg):
        self.ui.listWidget.insertItem(0, msg)


class BaseEvent(QObject):
    signalID = pyqtSignal(str)

    def __init__(self):
        QObject.__init__(self)

    def Event(self):
        self.signalID.emit("")


class uiHome(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, None)
        self.ui = parent

    def connectEvents(self):
        self.ui.Btn_Practice.clicked.connect(self.PracticeBtn)
        self.ui.Btn_Chrono.clicked.connect(self.ChronoBtn)
        self.ui.Btn_CheckPICAM.clicked.connect(self.CheckPiCamBtn)

    def CheckPiCamBtn(self):
        print("CheckBtn")
        self.ui.stackedWidget.setCurrentIndex(1)

    def PracticeBtn(self):
        print("NextBtn")
        self.ui.stackedWidget.setCurrentIndex(2)

    def ChronoBtn(self):
        print("NextBtn")
        self.ui.stackedWidget.setCurrentIndex(3)


class uiPractice(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, None)
        self.ui = parent

    def connectEvents(self):
        self.ui.Btn_InStart.clicked.connect(self.InStart)
        self.ui.Btn_ResetChrono.clicked.connect(self.ResetChrono)
        self.ui.Btn_Save.clicked.connect(self.Save)
        self.ui.Btn_Back.clicked.connect(self.HomeBtn)

    def HomeBtn(self):
        print("HomeBtn")
        self.ui.stackedWidget.setCurrentIndex(0)

    def InStart(self):
        print("InStart")
        self.ui.listWidget.addItem("InStart")

    def ResetChrono(self):
        print("RAZ")
        self.ui.listWidget.clear()

    def Save(self):
        print("TODO Save")
        self.ui.listWidget.clear()


class uiPiCAM(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, None)
        self.ui = parent

    def connectEvents(self):
        self.ui.Btn_PiCam_Home.clicked.connect(self.HomeBtn)
        self.ui.Btn_PiCam_Refresh.clicked.connect(self.RefreshBtn)

    def HomeBtn(self):
        print("HomeBtn")
        self.ui.stackedWidget.setCurrentIndex(0)

    def RefreshBtn(self):
        print("RefreshBtn")


class uiChrono(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, None)
        self.ui = parent

    def connectEvents(self):
        self.ui.Btn_ChronoInStart.clicked.connect(self.InStart)
        self.ui.Btn_ChronoReset.clicked.connect(self.ResetChrono)
        self.ui.Btn_ChronoSave.clicked.connect(self.Save)
        self.ui.Btn_ChronoBack.clicked.connect(self.HomeBtn)

    def HomeBtn(self):
        print("HomeBtn")
        self.ui.stackedWidget.setCurrentIndex(0)

    def InStart(self):
        print("TODO InStart")

    def ResetChrono(self):
        print("TODO Reset")

    def Save(self):
        print("TODO Save")


if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)
    myapp = MyForm()
    myapp.show()

    signal = myapp.GetBaseEventID()
    signal.Event()
    sys.exit(app.exec_())
