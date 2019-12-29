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
    btn_refly_sig = pyqtSignal()
    btn_cancel_flight_sig = pyqtSignal()
    widgetList = []

    def __init__(self, name, parent):
        super(QObject, self).__init__()
        self.wPilotCtrl = WPilotCtrl("PilotCtrl", parent)
        self.wChronoCtrl = WChronoCtrl("ChronoCtrl", parent)
        self.wBtnCtrl = Ui_WChronoBtn()
        self.name = name
        self.parent = parent
        self.widget=QtWidgets.QWidget(parent)
        self.wBtnCtrl.setupUi(self.widget)
        self.widgetList.append(self.wPilotCtrl.get_widget())
        self.widgetList.append(self.wChronoCtrl.get_widget())
        self.widgetList.append(self.widget)

        # Event connect
        self.wBtnCtrl.Btn_Home.clicked.connect(self.btn_home)
        self.wBtnCtrl.Btn_Next.clicked.connect(self.btn_next_pilot)
        self.wBtnCtrl.Btn_reflight.clicked.connect(self.btn_refly)
        self.wBtnCtrl.Btn_CancelRound.clicked.connect(self.btn_cancel_flight)

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

    def btn_cancel_flight(self):
        self.btn_cancel_flight_sig.emit()

    def btn_refly(self):
        self.btn_refly_sig.emit()

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

    def set_data(self, competitor, round):
        self.view.pilotName.setText(competitor.display_name())
        self.view.bib.setText("BIB : "+str(competitor.get_bib_number()))
        self.view.round.setText("Round : "+str(round))

class WChronoCtrl(QTimer, QObject):
    btn_null_flight_sig = pyqtSignal()
    btn_penalty_100_sig = pyqtSignal()
    btn_penalty_1000_sig = pyqtSignal()
    btn_clear_penalty_sig = pyqtSignal()

    def __init__(self, name, parent):
        super(WChronoCtrl, self).__init__()

        self.view = Ui_WChrono()
        self.name = name
        self.parent = parent
        self.widget = QtWidgets.QWidget(parent)

        _translate = QtCore.QCoreApplication.translate
        self.statusText = []
        self.statusText.append(_translate("chronoStatus_WaitNewRun", "Wait New Run"))
        self.statusText.append(_translate("chronoStatus_WaitToLaunch", "Wait To Launch"))
        self.statusText.append(_translate("chronoStatus_Launched", "Launched"))
        self.statusText.append(_translate("chronoStatus_InStart", "In Start"))
        self.statusText.append(_translate("chronoStatus_InProgress", "In Progress"))
        self.statusText.append(_translate("chronoStatus_Finished", "Finished"))

        #initialize labels for lap time
        self.lap = []
        #initialize labels for status
        self.current_lap = 0
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

        self.view.nullFlight.clicked.connect(self.null_flight)
        self.view.btn_penalty_100.clicked.connect(self.penalty_100)
        self.view.btn_penalty_1000.clicked.connect(self.penalty_1000)
        self.view.btn_clear_penalty.clicked.connect(self.clear_penalty)

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
        self.view.Status.setText(self.statusText[status])

    def set_laptime(self, laptime):
        #self.view.Time_label.setText("{:0>6.3f}".format(time)
        print ("current lap : "+str(self.current_lap))
        if self.current_lap<len(self.lap):
            self.lap[self.current_lap].setText("{:d} : {:0>6.2f}".format(self.current_lap+1, laptime))
            self.current_lap += 1

    def set_finaltime(self, time):
        self.view.Time_label.setText("{:0>6.2f}".format(time))

    def reset_ui(self):
        #self.view.Time_label.setText("{:0>6.3f}".format(0.0))
        for lap in self.lap:
            lap.setText("")
        #for ctrl in self.lap_list:
        #    ctrl.setText("")
        self.current_lap = 0
        self.set_penalty_value(0)
        self.set_null_flight(False)

    def settime(self, setTime, count_up, starttimer=True):
        self.time=setTime
        self.view.Time_label.setText("{:0>6.2f}".format(self.time / 1000))
        self.time_up=count_up
        self.startTime=time.time()
        if(starttimer):
            self.timerEvent.start(self.duration)

    def stoptime(self):
        self.timerEvent.stop()

    def run(self):
        if (self.time_up==True):
            self.view.Time_label.setText("{:0>6.2f}".format(time.time() - self.startTime))
        else:
            self.view.Time_label.setText("{:0>6.2f}".format(self.time / 1000 - (time.time()-self.startTime)))

    def penalty_100(self):
        self.btn_penalty_100_sig.emit()

    def penalty_1000(self):
        self.btn_penalty_1000_sig.emit()

    def clear_penalty(self):
        self.btn_clear_penalty_sig.emit()

    def set_penalty_value(self,value):
        self.view.penalty_value.setText(str(value))

    def null_flight(self):
        self.btn_null_flight_sig.emit()

    def set_null_flight(self, value=False):
        if(value):
            self.view.nullFlightLabel.setText("Null Flight")
        else:
            self.view.nullFlightLabel.setText("")


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