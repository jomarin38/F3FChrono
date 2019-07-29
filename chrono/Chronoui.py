import sys
from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import QObject, pyqtSignal, pyqtSlot
from .Qtchronoui import Ui_MainWindow



class MyForm (QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__ (self, parent)
        self.init()
        
    def init(self):
        self.ui = Ui_MainWindow ()
        self.ui.setupUi (self)
        self.setGeometry(0, 0, 480, 300)
        self.uiHome = uiHome (self.ui)
        self.uiPiCAM = uiPiCAM (self.ui)
        self.uiChrono = uiChrono (self.ui)
        self.uiPractice = uiPractice (self.ui)
        self.connectEvents ()
        self.BaseEvent= BaseEvent()

    def connectEvents (self):
        self.uiHome.connectEvents ()
        self.uiPiCAM.connectEvents ()
        self.uiChrono.connectEvents ()
        self.uiPractice.connectEvents ()

    def GetBaseEventID (self):
        return self.BaseEvent
    
    def UpdateHMI (self, msg):
        self.ui.listWidget.insertItem (0, msg)

class BaseEvent(QObject):
    signalID=pyqtSignal(str)
            
    def __init__(self):
        QObject.__init__(self)
  
    def Event(self):
        self.signalID.emit ("")


class uiHome (QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__ (self, None)
        self.ui=parent
        
    def connectEvents (self):
        QtCore.QObject.connect(self.ui.Btn_Practice, QtCore.SIGNAL("clicked()"), self.PracticeBtn)
        QtCore.QObject.connect(self.ui.Btn_Chrono, QtCore.SIGNAL("clicked()"), self.ChronoBtn)
        QtCore.QObject.connect(self.ui.Btn_CheckPICAM, QtCore.SIGNAL("clicked()"), self.CheckPiCamBtn)       
      
    def CheckPiCamBtn (self):
        print ("CheckBtn")
        self.ui.stackedWidget.setCurrentIndex (1)

    def PracticeBtn (self):
        print ("NextBtn")
        self.ui.stackedWidget.setCurrentIndex (2)

    def ChronoBtn (self):
        print ("NextBtn")
        self.ui.stackedWidget.setCurrentIndex (3)
        



class uiPractice (QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__ (self, None)
        self.ui=parent
        
    def connectEvents (self):
        QtCore.QObject.connect(self.ui.Btn_InStart, QtCore.SIGNAL("clicked()"), self.InStart)
        QtCore.QObject.connect(self.ui.Btn_ResetChrono, QtCore.SIGNAL("clicked()"), self.ResetChrono)
        QtCore.QObject.connect(self.ui.Btn_Save, QtCore.SIGNAL("clicked()"), self.Save)
        QtCore.QObject.connect(self.ui.Btn_Back, QtCore.SIGNAL("clicked()"), self.HomeBtn)

    def HomeBtn (self):
        print ("HomeBtn")
        self.ui.stackedWidget.setCurrentIndex (0)
    
    def InStart (self):
        print("InStart")
        self.ui.listWidget.addItem ("InStart")
        
    def ResetChrono (self):
        print ("RAZ")
        self.ui.listWidget.clear ()
        
    def Save (self):
        print ("TODO Save")
        self.ui.listWidget.clear ()


class uiPiCAM (QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__ (self, None)
        self.ui=parent
    
    def connectEvents(self):
        QtCore.QObject.connect(self.ui.Btn_PiCam_Home, QtCore.SIGNAL("clicked()"), self.HomeBtn)
        QtCore.QObject.connect(self.ui.Btn_PiCam_Refresh, QtCore.SIGNAL("clicked()"), self.RefreshBtn)
       
    def HomeBtn (self):
        print ("HomeBtn")
        self.ui.stackedWidget.setCurrentIndex (0)

    def RefreshBtn (self):
        print ("RefreshBtn")
        
    

class uiChrono (QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__ (self, None)
        self.ui=parent
        
    def connectEvents (self):
        QtCore.QObject.connect(self.ui.Btn_ChronoInStart, QtCore.SIGNAL("clicked()"), self.InStart)
        QtCore.QObject.connect(self.ui.Btn_ChronoReset, QtCore.SIGNAL("clicked()"), self.ResetChrono)
        QtCore.QObject.connect(self.ui.Btn_ChronoSave, QtCore.SIGNAL("clicked()"), self.Save)
        QtCore.QObject.connect(self.ui.Btn_ChronoBack, QtCore.SIGNAL("clicked()"), self.HomeBtn)

    def HomeBtn (self):
        print ("HomeBtn")
        self.ui.stackedWidget.setCurrentIndex (0)
    
    def InStart (self):
        print("TODO InStart")
        
    def ResetChrono (self):
        print ("TODO Reset")
        
    def Save (self):
        print ("TODO Save")

if __name__ == '__main__':
    app=QtGui.QApplication(sys.argv)
    myapp = MyForm ()
    myapp.show()
    
    signal=myapp.GetBaseEventID ()
    signal.Event()
    sys.exit(app.exec_())
    
