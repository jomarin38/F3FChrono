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
from F3FChrono.gui.WPicamPair_ui import Ui_WPicamPair
from F3FChrono.chrono.Chrono import *
from F3FChrono.data.web.Utils import Utils



class WRoundCtrl(QObject):
    btn_next_sig = pyqtSignal()
    btn_home_sig = pyqtSignal()
    btn_refly_sig = pyqtSignal()
    btn_cancel_flight_sig = pyqtSignal()
    widgetList = []

    def __init__(self, name, parent, vocal_elapsedTime_sig):
        super().__init__()
        self.wPilotCtrl = WPilotCtrl("PilotCtrl", parent)
        self.wChronoCtrl = WChronoCtrl("ChronoCtrl", parent, vocal_elapsedTime_sig)
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

    def is_show(self):
        return self.widget.isVisible()

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
        self.rules['alarm'] = False
        self.voltagestylesheet = "background-color:rgba( 255, 255, 255, 0% );"
        self.windstylesheet = "background-color:rgba( 255, 255, 255, 0% );"

    def get_widget(self):
        return(self.widgetList)

    def show(self):
        self.widget.show()
        self.view.Elapsedtime.setVisible(False)
        self.view.btn_clear.setVisible(False)

    def is_show(self):
        return self.widget.isVisible()

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
        self.rules['rain'] = rain

    def check_rules(self, limit_angle, speed_min, speed_max, time_limit):
        if abs(self.rules['dir']) > limit_angle or self.rules['speed'] < speed_min or self.rules['speed'] > speed_max \
                or self.rules['rain']:
            if self.rules['detected'] == False:
                self.rules['starttime'] = datetime.now()
                self.rules['time(s)'] = time.time()
                self.rules['detected'] = True
            else:
                if ((time.time()-self.rules['time(s)']) > 20):
                    self.view.WindInfo.setStyleSheet('background-color:red;')
                    self.view.Elapsedtime.setVisible(True)
                    if (time.time()-self.rules['time(s)']) > (time_limit*60):
                        self.view.Elapsedtime.setStyleSheet('background-color:red;')
                        self.view.btn_clear.setVisible(True)
                        self.rules['alarm']=True

                    self.view.Elapsedtime.setText("time : "+\
                                time.strftime("%H:%M:%S", time.gmtime(time.time()-self.rules['time(s)']))\
                                +self.cancelroundtostr())

        else:
            self.view.WindInfo.setStyleSheet('background-color:rgba( 255, 255, 255, 0% );')
            self.rules['detected']=False
            if not self.rules['alarm']:
                self.view.Elapsedtime.setStyleSheet('background-color:rgba( 255, 255, 255, 0% );')
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
        self.view.voltage.setText("{:0>3.1f}".format(voltage)+" V")
        if voltage <= ConfigReader.config.conf['voltage_min'] and\
                self.voltagestylesheet == "background-color:rgba( 255, 255, 255, 0% );":
            self.voltagestylesheet = "background-color:red;"
            self.view.voltage.setStyleSheet(self.voltagestylesheet)
        elif voltage > ConfigReader.config.conf['voltage_min'] and self.voltagestylesheet == "background-color:red;":
            self.voltagestylesheet = "background-color:rgba( 255, 255, 255, 0% );"
            self.view.voltage.setStyleSheet(self.voltagestylesheet)

    def set_rssi(self, rssi1, rssi2):
        self.view.rssi.setText(str(rssi1) + "%, "+str(rssi2)+"%")

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

    def is_show(self):
        return self.widget.isVisible()

    def hide(self):
        self.widget.hide()

    def set_data(self, competitor, round):
        self.view.pilotName.setText(competitor.display_name())
        self.view.bib.setText("BIB : "+str(competitor.get_bib_number()))
        self.view.round.setText("Round : "+str(len(round.event.valid_rounds)+1))

class WChronoCtrl(QTimer):
    btn_null_flight_sig = pyqtSignal()
    btn_penalty_100_sig = pyqtSignal()
    btn_penalty_1000_sig = pyqtSignal()
    btn_clear_penalty_sig = pyqtSignal()
    time_elapsed_sig = pyqtSignal()

    def __init__(self, name, parent, vocal_elapsedTime_sig):
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
        self.statusText.append(_translate("chronoStatus_InProgress", "In Progress"))
        self.statusText.append(_translate("chronoStatus_WaitAltitude", "Wait Altitude"))
        self.statusText.append(_translate("chronoStatus_Finished", "Finished"))

        self.vocal_elapsedTime_sig = vocal_elapsedTime_sig
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

    def is_show(self):
        return self.widget.isVisible()

    def set_status(self, status):
        if status < len(self.statusText):
            self.view.Status.setText(self.statusText[status])

    def set_laptime(self, laptime):
        #self.view.Time_label.setText("{:0>6.3f}".format(time)
        print("current lap : "+str(self.current_lap))
        if self.current_lap<len(self.lap):
            self.lap[self.current_lap].setText("{:d} : {:0>6.1f}".format(self.current_lap+1, laptime))
            self.current_lap += 1

    def set_finaltime(self, data_time):
        print("Widget chrono set final time : ", time.time())
        self.view.Time_label.setText("{:0>6.2f}".format(data_time))

    def reset_ui(self):
        #self.view.Time_label.setText("{:0>6.3f}".format(0.0))
        for lap in self.lap:
            lap.setText("")
        #for ctrl in self.lap_list:
        #    ctrl.setText("")
        self.current_lap = 0
        self.set_penalty_value(0)
        self.set_null_flight(False)

    def settime(self, settime, count_up, starttimer=True):
        self.time = settime
        self.view.Time_label.setText("{:0>6.2f}".format(self.time / 1000))
        self.time_up = count_up
        self.startTime = time.time()
        if starttimer:
            self.timerEvent.start(self.duration)
            self.vocal_elapsedTime_sig.emit('end')

    def stoptime(self):
        self.timerEvent.stop()

    def run(self):
        if self.time_up:
            self.view.Time_label.setText("{:0>6.2f}".format(time.time() - self.startTime))
        else:
            self.view.Time_label.setText("{:0>6.2f}".format(self.time / 1000 - (time.time()-self.startTime)))
            timeval = self.time / 1000 - (time.time()-self.startTime)
            if timeval >= 29.8:
                self.vocal_elapsedTime_sig.emit('30s')
            if 25.9 <= timeval <= 26.1:
                self.vocal_elapsedTime_sig.emit('25s')
            if 20.9 <= timeval <= 21.1:
                self.vocal_elapsedTime_sig.emit('20s')
            if 15.9 <= timeval <= 16.1:
                self.vocal_elapsedTime_sig.emit('15s')
            if 10.9 <= timeval <= 11.1:
                self.vocal_elapsedTime_sig.emit('10s')
            if timeval < 0:
                self.vocal_elapsedTime_sig.emit('end')
                self.time_elapsed_sig.emit()

    def penalty_100(self):
        self.btn_penalty_100_sig.emit()

    def penalty_1000(self):
        self.btn_penalty_1000_sig.emit()

    def clear_penalty(self):
        self.btn_clear_penalty_sig.emit()

    def set_penalty_value(self, value):
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
    btn_random_sig = pyqtSignal()
    btn_day_1_sig = pyqtSignal()
    widgetList = []

    def __init__(self, name, parent):
        super().__init__(parent)
        self.view = Ui_WConfig()
        self.name = name
        self.parent = parent
        self.widget = QtWidgets.QWidget(parent)
        self.view.setupUi(self.widget)
        self.widgetList.append(self.widget)

        # Event connect
        self.view.StartBtn.clicked.connect(self.btn_next)
        self.view.ContestList.currentIndexChanged.connect(self.contest_sig.emit)
        self.view.btn_settings.clicked.connect(self.btn_settings_sig.emit)
        self.view.randombtn.clicked.connect(self.btn_random_sig.emit)
        self.view.day_1btn.clicked.connect(self.btn_day_1_sig.emit)

    def get_widget(self):
        return(self.widgetList)

    def show(self):
        self.widget.show()

    def is_show(self):
        return self.widget.isVisible()

    def hide(self):
        self.widget.hide()

    def btn_next(self):
        self.btn_next_sig.emit()

    def set_data(self, event):
        self.view.WindMinValue.setValue(event.min_allowed_wind_speed)
        self.view.WindMaxValue.setValue(event.max_allowed_wind_speed)
        self.view.OrientationValue.setValue(event.max_wind_dir_dev)
        self.view.RevolValue.setValue(event.flights_before_refly)
        self.view.bib_start.setValue(event.bib_start)
        self.view.MaxInterruptValue.setValue(event.max_interruption_time/60)
        self.view.daydurationvalue.setValue(event.dayduration)

    def set_contest(self, contest_list):
        self.chrono_sig.emit()
        for contest in contest_list:
            self.view.ContestList.addItem(contest.name, userData=contest)

        self.view.ContestList.setCurrentIndex(1)

    def get_data(self):
        self.min_allowed_wind_speed = self.view.WindMinValue.value()
        self.max_allowed_wind_speed = self.view.WindMaxValue.value()
        self.max_wind_dir_dev = self.view.OrientationValue.value()
        self.max_interruption_time = self.view.MaxInterruptValue.value()*60
        self.flights_before_refly=self.view.RevolValue.value()
        self.bib_start=self.view.bib_start.value()
        self.dayduration=self.view.daydurationvalue.value()
        self.contest=self.view.ContestList.currentIndex()

class WSettingsAdvanced(QObject):
    btn_settings_sig = pyqtSignal()
    widgetList = []
    def __init__(self, name, parent):
        super().__init__()
        self.view = Ui_WSettingsAdvanced()
        self.name = name
        self.parent = parent
        self.widget = QtWidgets.QWidget(parent)
        self.view.setupUi(self.widget)
        self.widgetList.append(self.widget)
        self.view.btn_back.clicked.connect(self.btn_settings_sig.emit)
    def get_widget(self):
        return(self.widgetList)

    def show(self):
        self.widget.show()

    def is_show(self):
        return self.widget.isVisible()

    def hide(self):
        self.widget.hide()

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
    btn_quitapp_sig = pyqtSignal()
    widgetList = []

    def __init__(self, name, parent):
        super().__init__()
        self.view = Ui_WSettings()
        self.name = name
        self.parent = parent
        self.widget = QtWidgets.QWidget(parent)
        self.view.setupUi(self.widget)
        self.widgetList.append(self.widget)
        self.view.btn_advanced_settings.clicked.connect(self.btn_settingsadvanced_sig.emit)
        self.view.wbase_detect_btn.clicked.connect(self.base_detect)
        self.view.wbase_invert_btn.clicked.connect(self.base_invert)
        self.view.btn_cancel.clicked.connect(self.btn_cancel)
        self.view.btn_valid.clicked.connect(self.btn_valid)
        self.view.closebtn.clicked.connect(self.btn_quitapp_sig.emit)
        self.udp_sig = None

    def get_widget(self):
        return(self.widgetList)

    def show(self):
        if Utils.server_alive():
            self.view.webserverUrl.setText(Utils.get_base_url())
        self.widget.show()

    def is_show(self):
        return self.widget.isVisible()

    def hide(self):
        self.widget.hide()

    def set_data(self):
        self.view.sound.setChecked(ConfigReader.config.conf['sound'])
        self.view.voice.setChecked(ConfigReader.config.conf['voice'])
        self.view.anemometer.setChecked(ConfigReader.config.conf['anemometer'])
        self.view.arduino.setChecked(ConfigReader.config.conf['arduino'])
        self.view.simulate_mode.setChecked(ConfigReader.config.conf['simulatemode'])
        self.view.voltagemin.setValue(ConfigReader.config.conf['voltage_min'])
        self.view.fullscreen.setChecked(ConfigReader.config.conf['fullscreen'])
        self.view.buzzer.setChecked(ConfigReader.config.conf['buzzer_valid'])
        self.view.buzzernext.setChecked(ConfigReader.config.conf['buzzer_next_valid'])
        self.view.webserver.setChecked(ConfigReader.config.conf['run_webserver'])

    def get_data(self):
        ConfigReader.config.conf['sound'] = self.view.sound.isChecked()
        ConfigReader.config.conf['voice'] = self.view.voice.isChecked()
        ConfigReader.config.conf['anemometer'] = self.view.anemometer.isChecked()
        ConfigReader.config.conf['arduino'] = self.view.arduino.isChecked()
        ConfigReader.config.conf['simulatemode'] = self.view.simulate_mode.isChecked()
        ConfigReader.config.conf['fullscreen'] = self.view.fullscreen.isChecked()
        ConfigReader.config.conf['buzzer_valid'] = self.view.buzzer.isChecked()
        ConfigReader.config.conf['buzzer_next_valid'] = self.view.buzzernext.isChecked()
        ConfigReader.config.conf['run_webserver'] = self.view.webserver.isChecked()
        ConfigReader.config.conf['voltage_min'] = self.view.voltagemin.value()
        ConfigReader.config.conf['run_webserver'] = self.view.webserver.isChecked()

    def btn_cancel(self):
        if self.udp_sig is not None:
            self.udp_sig.disconnect(self.slot_udp)
        self.btn_cancel_sig.emit()

    def btn_valid(self):
        if self.udp_sig is not None:
            self.udp_sig.disconnect(self.slot_udp)
        self.btn_valid_sig.emit()

    def set_udp_sig(self, udp_sig):
        self.udp_sig = udp_sig

    def base_detect(self):
        if self.udp_sig is not None:
            self.udp_sig.connect(self.slot_udp)
            self.view.baseA_IP.setText("None")
            self.view.baseB_IP.setText("None")

    def slot_udp(self, caller, data, address):
        print(caller, data, address)
        if caller.lower() == "udpreceive" and data.lower() == "event" and self.view.baseA_IP.toPlainText() == "None":
            self.view.baseA_IP.setText(address)
        elif caller.lower() == "udpreceive" and data.lower() == "event" and self.view.baseB_IP.toPlainText() == "None" and\
                address != self.view.baseA_IP.toPlainText():
            self.view.baseB_IP.setText(address)

    def base_invert(self):
        tmp=self.view.baseA_IP.toPlainText()
        self.view.baseA_IP.setText(self.view.baseB_IP.toPlainText())
        self.view.baseB_IP.setText(tmp)

    def get_ipbaseA(self):
        return self.view.baseA_IP.toPlainText()

    def get_ipbaseB(self):
        return self.view.baseB_IP.toPlainText()


class WPiCamPair(QObject):
    btn_cancel_sig = pyqtSignal()
    btn_valid_sig = pyqtSignal()
    widgetList = []

    def __init__(self, name, parent):
        super().__init__()
        self.view = Ui_WPicamPair()
        self.name = name
        self.parent = parent
        self.widget = QtWidgets.QWidget(parent)
        self.view.setupUi(self.widget)
        self.widgetList.append(self.widget)
        self.view.btn_cancel.clicked.connect(self.btn_cancel_sig.emit)
        self.view.btn_valid.clicked.connect(self.btn_valid_sig.emit)

    def get_widget(self):
        return(self.widgetList)

    def show(self):
        self.widget.show()

    def is_show(self):
        return self.widget.isVisible()

    def hide(self):
        self.widget.hide()

    def set_data(self):
        print ("todo PiCamPair - set data")
    def get_data(self):
        print("todo PiCamPair - get data")