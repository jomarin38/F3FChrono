import sys
import collections
from time import *
from datetime import datetime
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import pyqtSignal, QObject, QTimer
from F3FChrono.chrono import ConfigReader
from F3FChrono.gui.WWind_UI import Ui_WWind
from F3FChrono.gui.WPilot_UI import Ui_WPilot
from F3FChrono.gui.WChrono_ui import Ui_WChrono
from F3FChrono.gui.WChronoBtn_ui import Ui_WChronoBtn
from F3FChrono.gui.WConfig_ui import Ui_WConfig
from F3FChrono.gui.WSettings_ui import Ui_WSettings
from F3FChrono.gui.WSettingsAdvanced_ui import Ui_WSettingsAdvanced
from F3FChrono.chrono.Chrono import *



class WRoundCtrl(QObject):
    btn_next_sig = pyqtSignal()
    btn_home_sig = pyqtSignal()
    btn_refly_sig = pyqtSignal()
    btn_cancel_flight_sig = pyqtSignal()
    widgetList = []

    def __init__(self, name, parent):
        super().__init__()
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

class WWindCtrl():
    widgetList=[]
    def __init__(self, name, parent):
        self.view = Ui_WWind()
        self.name = name
        self.parent = parent
        self.widget = QtWidgets.QWidget(parent)
        self.view.setupUi(self.widget)
        self.view.btn_clear.clicked.connect(self.clear_alarm)
        self.widgetList.append(self.widget)
        self.rules = collections.OrderedDict()
        self.rules['dir'] = 0
        self.rules['speed'] = 0
        self.rules['rain'] = 0
        self.rules['starttime'] = datetime.now()
        self.rules['time(s)'] = time.time()
        self.rules['detected'] = False
        self.rules['alarm']=False

    def get_widget(self):
        return(self.widgetList)

    def show(self):
        self.widget.show()
        self.view.Elapsedtime.setVisible(False)
        self.view.btn_clear.setVisible(False)

    def hide(self):
        self.widget.hide()

    def set_data(self, speed, angle, rain):
        if rain:
            strrain = 'Rain'
        else:
            strrain = 'No Rain'
        self.view.WindInfo.setText('Wind : '+str(speed)+'m/s, Angle : '+str(angle)+'°'+', '+strrain)
        self.rules['dir'] = angle
        self.rules['speed'] = speed
        self.rules['rain']=rain

    def check_rules(self, limit_angle, speed_min, speed_max, time_limit):
        if abs(self.rules['dir']) > limit_angle or self.rules['speed'] < speed_min or self.rules['speed'] > speed_max \
                or self.rules['rain']:
            if self.rules['detected']==False:
                self.rules['starttime'] = datetime.now()
                self.rules['time(s)'] = time.time()
                self.rules['detected']=True
            else:
                if ((time.time()-self.rules['time(s)'])>20):
                    self.view.WindInfo.setStyleSheet('color: red')
                    self.view.Elapsedtime.setVisible(True)
                    if (time.time()-self.rules['time(s)'])>(time_limit*60):
                        self.view.Elapsedtime.setStyleSheet('color: red')
                        self.view.btn_clear.setVisible(True)
                        self.rules['alarm']=True

                    self.view.Elapsedtime.setText("time : "+\
                                time.strftime("%H:%M:%S", time.gmtime(time.time()-self.rules['time(s)']))\
                                +self.cancelroundtostr())

        else:
            self.view.WindInfo.setStyleSheet('color: black')
            self.rules['detected']=False
            if not self.rules['alarm']:
                self.view.Elapsedtime.setStyleSheet('color: black')
                self.view.Elapsedtime.setVisible(False)

    def clear_alarm(self):
        self.rules['alarm']=False
        self.view.Elapsedtime.setVisible(False)
        self.view.btn_clear.setVisible(False)

    def cancelroundtostr(self):
        cancelstr=''
        if self.rules['alarm']:
            #cancelstr=', Cancel Round'
            cancelstr =''
        return cancelstr

    def set_voltage(self, voltage):
        self.view.voltage.setText(str(voltage)+" V")

    def set_rssi(self, rssi1, rssi2):
        self.view.rssi.setText("rssi1, 2 : "+str(rssi1) + "%, "+str(rssi2)+"%")


class WPilotCtrl():
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

class WChronoCtrl(QTimer):
    btn_null_flight_sig = pyqtSignal()
    btn_penalty_100_sig = pyqtSignal()
    btn_penalty_1000_sig = pyqtSignal()
    btn_clear_penalty_sig = pyqtSignal()

    def __init__(self, name, parent):
        super().__init__()

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
    chrono_sig = pyqtSignal()
    btn_settings_sig = pyqtSignal()
    widgetList = []

    def __init__(self, name, parent):
        super().__init__(parent)
        self.view = Ui_WConfig()
        self.name = name
        self.parent = parent
        self.widget = QtWidgets.QWidget(parent)
        self.view.setupUi(self.widget)
        self.widgetList.append(self.widget)
        self.piCamA_config=False
        self.piCamB_config = False

        # Event connect
        self.view.StartBtn.clicked.connect(self.btn_next)
        self.view.ContestList.currentIndexChanged.connect(self.contest_changed)
        self.view.ChronoType.currentIndexChanged.connect(self.chrono_changed)
        self.view.btn_settings.clicked.connect(self.btn_settings)

    def get_widget(self):
        return(self.widgetList)

    def show(self):
        self.widget.show()

    def hide(self):
        self.widget.hide()

    def btn_settings(self):
        self.btn_settings_sig.emit()
    def chrono_changed(self):
        self.chrono_sig.emit()


    def contest_changed(self):
        self.contest_sig.emit()

    def btn_piCamA(self):
        self.piCamA_config=True
        self.set_piCamA("Wait Detection")

    def set_piCamA(self, value):
        self.view.PICamA_Value.setText(value)

    def is_piCamA_onConfig(self):
        return (self.piCamA_config)

    def btn_piCamB(self):
        self.piCamB_config=True
        self.set_piCamB("Wait Detection")

    def set_piCamB(self, value):
        self.view.PICamB_Value.setText(value)

    def is_piCamB_onConfig(self):
        return (self.piCamB_config)

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

class WSettingsAdvanced(QObject):
    btn_settings_sig = pyqtSignal()
    widgetList=[]
    def __init__(self, name, parent):
        super().__init__()
        self.view = Ui_WSettingsAdvanced()
        self.name = name
        self.parent = parent
        self.widget = QtWidgets.QWidget(parent)
        self.view.setupUi(self.widget)
        self.widgetList.append(self.widget)
        self.view.btn_back.clicked.connect(self.settings)
    def get_widget(self):
        return(self.widgetList)

    def show(self):
        self.widget.show()

    def hide(self):
        self.widget.hide()

    def settings(self):
        self.btn_settings_sig.emit()

    def set_data(self):
        self.view.port_btn_baseA.setValue(ConfigReader.config.conf['btn_baseA'])
        self.view.port_btn_baseB.setValue(ConfigReader.config.conf['btn_baseB'])
        self.view.port_btn_next.setValue(ConfigReader.config.conf['btn_next'])
        self.view.port_ledA.setValue(ConfigReader.config.conf['ledA'])
        self.view.port_ledB.setValue(ConfigReader.config.conf['ledB'])
        self.view.port_buzzer.setValue(ConfigReader.config.conf['buzzer'])
        self.view.buzzer_duration.setValue(ConfigReader.config.conf['buzzer_duration'])
        self.view.port_buzzer_next.setValue(ConfigReader.config.conf['buzzer_next'])
        self.view.buzzer_next_duration.setValue(ConfigReader.config.conf['buzzer_next_duration'])
        self.view.udp_port.setValue(ConfigReader.config.conf['udpport'])

    def get_data(self):
        ConfigReader.config.conf['btn_baseA'] = self.view.port_btn_baseA.value()
        ConfigReader.config.conf['btn_baseB'] = self.view.port_btn_baseB.value()
        ConfigReader.config.conf['btn_next'] = self.view.port_btn_next.value()
        ConfigReader.config.conf['ledA'] = self.view.port_ledA.value()
        ConfigReader.config.conf['ledB'] = self.view.port_ledB.value()
        ConfigReader.config.conf['buzzer'] = self.view.port_buzzer.value()
        ConfigReader.config.conf['buzzer_duration'] = self.view.buzzer_duration.value()
        ConfigReader.config.conf['buzzer_next'] = self.view.port_buzzer_next.value()
        ConfigReader.config.conf['buzzer_next_duration'] = self.view.buzzer_next_duration.value()
        ConfigReader.config.conf['udpport'] = self.view.udp_port.value()

class WSettings(QObject):
    btn_settingsadvanced_sig = pyqtSignal()
    btn_cancel_sig = pyqtSignal()
    btn_valid_sig = pyqtSignal()
    widgetList = []

    def __init__(self, name, parent):
        super().__init__()
        self.view = Ui_WSettings()
        self.name = name
        self.parent = parent
        self.widget = QtWidgets.QWidget(parent)
        self.view.setupUi(self.widget)
        self.widgetList.append(self.widget)
        self.view.btn_advanced_settings.clicked.connect(self.settingsadvanced)
        self.view.btn_cancel.clicked.connect(self.cancel)
        self.view.btn_valid.clicked.connect(self.valid)

    def get_widget(self):
        return(self.widgetList)

    def show(self):
        self.widget.show()

    def hide(self):
        self.widget.hide()

    def settingsadvanced(self):
        self.btn_settingsadvanced_sig.emit()

    def cancel(self):
        self.btn_cancel_sig.emit()

    def valid(self):
        self.btn_valid_sig.emit()

    def set_data(self):
        self.view.sound.setChecked(ConfigReader.config.conf['sound'])
        self.view.voice.setChecked(ConfigReader.config.conf['voice'])
        self.view.anemometer.setChecked(ConfigReader.config.conf['anemometer'])
        self.view.arduino.setChecked(ConfigReader.config.conf['arduino'])
        self.view.simulate_mode.setChecked(ConfigReader.config.conf['simulatemode'])
        self.view.voltagemin.setValue(ConfigReader.config.conf['voltage_min'])
        self.view.fullscreen.setChecked(ConfigReader.config.conf['fullscreen'])

    def get_data(self):
        ConfigReader.config.conf['sound'] = self.view.sound.isChecked()
        ConfigReader.config.conf['voice'] = self.view.voice.isChecked()
        ConfigReader.config.conf['anemometer'] = self.view.anemometer.isChecked()
        ConfigReader.config.conf['arduino'] = self.view.arduino.isChecked()
        ConfigReader.config.conf['simulatemode'] = self.view.simulate_mode.isChecked()
        ConfigReader.config.conf['fullscreen'] = self.view.fullscreen.isChecked()
        ConfigReader.config.conf['voltage_min'] = self.view.voltagemin.value()