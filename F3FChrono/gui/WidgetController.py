import sys
from time import *
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import pyqtSignal, QObject, QTimer

from F3FChrono.gui.WWind_UI import Ui_WWind
from F3FChrono.gui.WPilot_UI import Ui_WPilot
from F3FChrono.gui.WChrono_ui import Ui_WChrono
from F3FChrono.gui.WChronoBtn_ui import Ui_WChronoBtn
from F3FChrono.gui.WConfig_ui import Ui_WConfig
from F3FChrono.chrono.Chrono import *


class WRoundCtrl(QObject):
    btn_next_sig = pyqtSignal()
    btn_home_sig = pyqtSignal()
    btn_null_flight_sig = pyqtSignal()
    btn_refly_sig = pyqtSignal()
    btn_penalty_sig = pyqtSignal()

    widgetList = []

    def __init__(self, name, parent):
        super(QObject, self).__init__(parent)
        self.wPilotCtrl = WPilotCtrl("PilotCtrl", parent)
        self.wChronoCtrl = WChronoCtrl("ChronoCtrl", parent)
        self.view = Ui_WChronoBtn()
        self.name = name
        self.parent = parent
        self.widget=QtWidgets.QWidget(parent)
        self.view.setupUi(self.widget)
        self.widgetList.append(self.wPilotCtrl.get_widget())
        self.widgetList.append(self.wChronoCtrl.get_widget())
        self.widgetList.append(self.widget)
        # Event connect
        self.view.Btn_Home.clicked.connect(self.btn_home)
        self.view.Btn_Next.clicked.connect(self.btn_next_pilot)
        self.view.Btn_NullFlight.clicked.connect(self.btn_null_flight)
        self.view.Btn_reflight.clicked.connect(self.btn_refly)
        self.view.Btn_Penalty.clicked.connect(self.btn_penalty)

    def get_widget(self):
        return (self.widgetList)

    def show(self):
        self.widget.show()
        self.wPilotCtrl.show()
        self.wChronoCtrl.show()

    def hide(self):
        self.widget.hide()
        self.wPilotCtrl.hide()
        self.wChronoCtrl.hide()

    def btn_next_pilot(self):
        self.btn_next_sig.emit()

    def btn_home(self):
        self.btn_home_sig.emit()

    def btn_null_flight(self):
        self.btn_null_flight_sig.emit()

    def btn_refly(self):
        self.btn_refly_sig.emit()

    def btn_penalty(self):
        self.btn_penalty_sig.emit()

    def set_data(self):
        """
            TODO: roundCtrl.set_data
        """

class WWindCtrl:
    widgetList = []

    def __init__(self, name, parent):
        self.view = Ui_WWind()
        self.name = name
        self.parent = parent
        self.widget = QtWidgets.QWidget(parent)
        self.view.setupUi(self.widget)
        self.widgetList.append(self.widget)
    def get_widget(self):
        return(self.widgetList)

    def show(self):
        self.widget.show()

    def hide(self):
        self.widget.hide()

    def set_data(self, wind, angle):
        self.view.WindInfo.setText('Wind : '+str(wind)+'m.s, Angle : '+str(angle)+'°')

class WPilotCtrl:
    def __init__(self, name, parent):
        self.view = Ui_WPilot()
        self.name = name
        self.parent = parent
        self.widget = QtWidgets.QWidget(parent)
        self.view.setupUi(self.widget)

    def get_widget(self):
        return(self.widget)

    def show(self):
        self.widget.show()

    def hide(self):
        self.widget.hide()

    def set_data(self, competitor):
        self.view.pilotName.setText(competitor.display_name())
        self.view.bib.setText(str(competitor.get_bib_number()))

class WChronoCtrl(QTimer):

    def __init__(self, name, parent):
        super(WChronoCtrl, self).__init__()

        self.view = Ui_WChrono()
        self.name = name
        self.parent = parent
        self.widget = QtWidgets.QWidget(parent)

        self.lap=[]
        self.current_lap=0
        self.view.setupUi(self.widget)
        self.lap.append(self.view.Lap1)
        self.lap.append(self.view.Lap2)
        self.lap.append(self.view.Lap3)
        self.lap.append(self.view.Lap4)
        self.lap.append(self.view.Lap5)
        self.lap.append(self.view.Lap6)
        self.lap.append(self.view.Lap7)
        self.lap.append(self.view.Lap8)
        self.lap.append(self.view.Lap9)
        self.lap.append(self.view.Lap10)

        self.timerEvent = QTimer()
        self.timerEvent.timeout.connect(self.run)
        self.duration=10
        self.startTime = time.time()
        self.time=0
        self.time_up = True

    def get_widget(self):
        return (self.widget)

    def show(self):
        self.widget.show()

    def hide(self):
        self.widget.hide()

    def set_status(self, status):
        self.view.comboBox.setCurrentIndex(status)

    def set_laptime(self, laptime):
        #self.view.Time_label.setText("{:0>6.3f}".format(time)
        print ("current lap : "+str(self.current_lap))
        self.lap[self.current_lap].setText("{:d} : {:0>6.3f}".format(self.current_lap+1, laptime))

        #self.lap_list[self.current_lap].setText("{0} : {1:.3f}".format(self.current_lap, laptime))
        self.current_lap += 1

    def reset_ui(self):
        #self.view.Time_label.setText("{:0>6.3f}".format(0.0))
        for lap in self.lap:
            lap.setText("")
        #for ctrl in self.lap_list:
        #    ctrl.setText("")
        self.current_lap = 0


    def settime(self, setTime, count_up):
        self.time=setTime
        self.time_up=count_up
        self.startTime=time.time()
        self.timerEvent.start(self.duration)

    def stoptime(self):
        self.timerEvent.stop()

    def run(self):
        if (self.time_up==True):
            self.view.Time_label.setText("{:0>6.3f}".format(time.time() - self.startTime))
        else:
            self.view.Time_label.setText("{:0>6.3f}".format(self.time / 1000 - (time.time()-self.startTime)))


class WConfigCtrl(QObject):
    btn_next_sig = pyqtSignal()
    contest_sig = pyqtSignal()
    widgetList = []

    def __init__(self, name, parent):
        super(QObject, self).__init__(parent)
        self.view = Ui_WConfig()
        self.name = name
        self.parent = parent
        self.widget = QtWidgets.QWidget(parent)
        self.view.setupUi(self.widget)
        self.widgetList.append(self.widget)

        # Event connect
        self.view.StartBtn.clicked.connect(self.btn_next)
        self.view.PICamA_Btn.clicked.connect(self.btn_piCamA)
        self.view.PICamB_Btn.clicked.connect(self.btn_piCamB)
        self.view.ContestList.currentIndexChanged.connect(self.contest_changed)
        self.view.ChronoType.currentIndexChanged.connect(self.chrono_changed)

    def get_widget(self):
        return(self.widgetList)

    def show(self):
        self.widget.show()

    def hide(self):
        self.widget.hide()


    def chrono_changed(self):
        if (self.view.ChronoType.currentIndex()==chronoType.wire):
            self.view.PICamA_Btn.setDisabled(True)
            self.view.PICamA_Value.setDisabled(True)
            self.view.PICamB_Btn.setDisabled(True)
            self.view.PICamB_Value.setDisabled(True)
        else:
            self.view.PICamA_Btn.setDisabled(False)
            self.view.PICamA_Value.setDisabled(False)
            self.view.PICamB_Btn.setDisabled(False)
            self.view.PICamB_Value.setDisabled(False)


    def contest_changed(self):
        print(self.contest_changed)
        self.contest_sig.emit()

    def btn_piCamA(self):
        print(self.btn_piCamA)

    def btn_piCamB(self):
        print(self.btn_piCamB)

    def btn_next(self):
        self.get_data()
        self.btn_next_sig.emit()

    def set_data(self, min_speed, max_speed, dir_dev, max_interrupt, revol=5):
        self.view.WindMinValue.setValue(min_speed)
        self.view.WindMaxValue.setValue(max_speed)
        self.view.OrientationValue.setValue(dir_dev)
        self.view.RevolValue.setValue(revol)
        self.view.MaxInterruptValue.setValue(max_interrupt/60)

    def set_contest(self, contest):
        self.view.ChronoType.setCurrentIndex(0)
        self.chrono_changed()
        for temp in contest:
            self.view.ContestList.addItem(temp.name)
        self.view.ContestList.setCurrentText(contest[0].name)

    def get_data(self):
        self.wind_speed_min=self.view.WindMinValue.value()
        self.wind_speed_max=self.view.WindMaxValue.value()
        self.wind_orientation=self.view.OrientationValue.value()
        self.interruption_time_max=self.view.MaxInterruptValue.value()
        self.revol=self.view.RevolValue.value()
        self.chrono_type=self.view.ChronoType.currentIndex()
        self.contest=self.view.ContestList.currentIndex()