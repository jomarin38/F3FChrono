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
from time import *
from datetime import datetime
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import pyqtSignal, QObject, QTimer
from F3FChrono.chrono import ConfigReader
from F3FChrono.gui.WWind_ui import Ui_WWind
from F3FChrono.gui.WPilot_ui import Ui_WPilot
from F3FChrono.gui.WChrono_ui import Ui_WChrono
from F3FChrono.gui.WChronoTraining_ui import Ui_WTraining
from F3FChrono.gui.WChronoBtn_ui import Ui_WChronoBtn
from F3FChrono.gui.WChronoBtn_cancel_ui import Ui_WChronoBtn_Cancel
from F3FChrono.gui.WChronoBtn_GS_Validate_ui import Ui_WChronoGSEnable
from F3FChrono.gui.WTrainingBtn_ui import Ui_WTrainingBtn
from F3FChrono.gui.WConfig_ui import Ui_WConfig
from F3FChrono.gui.WSettings_ui import Ui_WSettings
from F3FChrono.gui.WSettingsConnectedDevices_ui import Ui_WSettingsConnectedDevices
from F3FChrono.gui.WSettingsAdvanced_ui import Ui_WSettingsAdvanced
from F3FChrono.gui.WSettingsBase_ui import Ui_WSettingsBase
from F3FChrono.gui.WSettingsBase_item_ui import Ui_WSettingBase_item
from F3FChrono.gui.WSettingswBtn_ui import Ui_WSettingswBtn
from F3FChrono.gui.WSettingswBtn_item_ui import Ui_WSettingwBtn_item
from F3FChrono.gui.WSettingsSound_ui import Ui_WSettingsSound
from F3FChrono.gui.WSettingsQrCode_ui import Ui_WSettingsQrCode
from F3FChrono.chrono.Chrono import *
from F3FChrono.data.web.Utils import Utils

director_btn_stylesheet = 'background-color:#ff6666;border-radius: 10px;'
refly_btn_stylesheet = 'background-color:#66ccff;border-radius: 10px;'
penalty100_btn_stylesheet = 'background-color:#ffd633;border-radius: 10px;'
penalty1000_btn_stylesheet = 'background-color:#db4dff;border-radius: 10px;'
clear_penalty_btn_stylesheet = 'background-color:#aaff80;border-radius: 10px;'

class WRoundCtrl(QObject):
    btn_next_sig = pyqtSignal()
    cancel_round_sig = pyqtSignal()
    btn_home_sig = pyqtSignal()
    btn_gscoring_sig = pyqtSignal()
    widgetList = []

    def __init__(self, name, parent, vocal_elapsedTime_sig):
        super().__init__()
        self.wPilotCtrl = WPilotCtrl("PilotCtrl", parent)
        self.wChronoCtrl = WChronoCtrl("ChronoCtrl", parent, vocal_elapsedTime_sig)
        self.wBtnCtrl = Ui_WChronoBtn()
        self.wBtnCancel = Ui_WChronoBtn_Cancel()
        self.wBtnGS = Ui_WChronoGSEnable()
        self.name = name
        self.parent = parent
        self.widgetBtn = QtWidgets.QWidget(parent)
        self.widgetBtnCancel = QtWidgets.QWidget(parent)
        self.widgetBtnGS = QtWidgets.QWidget(parent)
        self.wBtnCtrl.setupUi(self.widgetBtn)
        self.wBtnCancel.setupUi(self.widgetBtnCancel)
        self.wBtnGS.setupUi(self.widgetBtnGS)
        self.widgetList.append(self.wPilotCtrl.get_widget())
        self.widgetList.append(self.wChronoCtrl.get_widget())
        self.widgetList.append(self.widgetBtn)
        self.widgetList.append(self.widgetBtnCancel)
        self.widgetList.append(self.widgetBtnGS)
        self.set_cancelmode(False)
        self.widgetBtnGS.hide()
        for widget in self.widgetList:
            widget.setStyleSheet("QPushButton{border: 1px solid black;border-radius: 10px;}")
        # Event connect
        self.wBtnCtrl.Btn_Home.clicked.connect(self.btn_home_sig.emit)
        self.wBtnCtrl.Btn_Next.clicked.connect(self.btn_next_sig.emit)
        self.wBtnCtrl.Btn_gscoring.clicked.connect(self.gs_continue)
        self.wBtnCancel.Btn_Next.clicked.connect(self.cancel_next)
        self.wBtnCancel.Btn_Home.clicked.connect(self.cancel_home)
        self.wBtnGS.Btn_Next.clicked.connect(self.gs_next)
        self.wBtnGS.Btn_Home.clicked.connect(self.gs_cancel)

    def get_widget(self):
        return (self.widgetList)

    def show(self):
        self.widgetBtn.show()
        self.wPilotCtrl.show()
        self.wChronoCtrl.show()

    def is_show(self):
        return self.widgetBtn.isVisible()

    def hide(self):
        self.widgetBtn.hide()
        self.wPilotCtrl.hide()
        self.wChronoCtrl.hide()

    def set_cancelmode(self, cancel):
        if cancel:
            self.widgetBtn.hide()
            self.widgetBtnCancel.show()
        else:
            self.widgetBtnCancel.hide()
            self.widgetBtn.show()

    def cancel_next(self):
        self.set_cancelmode(False)
        self.cancel_round_sig.emit()

    def cancel_home(self):
        self.set_cancelmode(False)

    def gs_continue(self):
        self.widgetBtn.hide()
        self.widgetBtnGS.show()

    def gs_next(self):
        self.widgetBtnGS.hide()
        self.widgetBtn.show()
        self.btn_gscoring_sig.emit()

    def gs_cancel(self):
        self.widgetBtnGS.hide()
        self.widgetBtn.show()

    def isalarm_enable(self):
        return self.wPilotCtrl.isalarm_enable()

    def get_alarm_sig(self):
        return self.wPilotCtrl.btn_alarm_sig

    def handle_group_scoring_enabled(self, enabled):
        _translate = QtCore.QCoreApplication.translate
        self.wPilotCtrl.handle_group_scoring_enabled(enabled)
        if enabled:
            self.wBtnCtrl.Btn_gscoring.setText(_translate("WChronoBtn", "GS Enabled"))
            self.wBtnCtrl.Btn_gscoring.setEnabled(False)
            self.wBtnCancel.label_cancelround.setText(_translate("WChronoCancelBtn", "Cancel Group ?"))
        else:
            self.wBtnCtrl.Btn_gscoring.setText(_translate("WChronoBtn", "G Scoring"))
            self.wBtnCtrl.Btn_gscoring.setEnabled(True)
            self.wBtnCancel.label_cancelround.setText(_translate("WChronoCancelBtn", "Cancel Round ?"))


class WTrainingCtrl(QObject):
    btn_next_sig = pyqtSignal()
    btn_home_sig = pyqtSignal()
    btn_reset_sig = pyqtSignal()
    widgetList = []

    def __init__(self, name, parent, speech_interval):
        super().__init__()
        self.wChronoCtrl = WChronoTrainingCtrl("TrainingCtrl", parent, speech_interval)
        self.wBtnCtrl = Ui_WTrainingBtn()
        self.name = name
        self.parent = parent
        self.widget = QtWidgets.QWidget(parent)
        self.wBtnCtrl.setupUi(self.widget)
        self.widgetList.append(self.wChronoCtrl.get_widget())
        self.widgetList.append(self.widget)

        # Event connect
        self.wBtnCtrl.Btn_Home.clicked.connect(self.btn_home)
        self.wBtnCtrl.Btn_Next.clicked.connect(self.btn_next)
        self.wBtnCtrl.Btn_reset.clicked.connect(self.btn_reset)

    def get_widget(self):
        return (self.widgetList)

    def show(self):
        self.widget.show()
        self.wChronoCtrl.show()

    def is_show(self):
        return self.widget.isVisible()

    def hide(self):
        self.widget.hide()
        self.wChronoCtrl.hide()

    def btn_next(self):
        self.btn_next_sig.emit()

    def btn_home(self):
        self.btn_home_sig.emit()

    def btn_reset(self):
        self.wChronoCtrl.reset()
        self.btn_reset_sig.emit()


class WWindCtrl():
    widgetList = []

    def __init__(self, name, parent):
        self.view = Ui_WWind()
        self.name = name
        self.parent = parent
        self.widget = QtWidgets.QWidget(parent)
        self.view.setupUi(self.widget)
        self.view.btn_clear.clicked.connect(self.clear_alarm)
        self.widgetList.append(self.widget)
        self.voltagestylesheet = "background-color:rgba( 255, 255, 255, 0% );"
        self.windstylesheet = "background-color:rgba( 255, 255, 255, 0% );"
        self.lowVoltage_sig = None
        self._translate = QtCore.QCoreApplication.translate

    def get_widget(self):
        return (self.widgetList)

    def show(self):
        self.widget.show()
        self.view.Elapsedtime.setVisible(False)
        self.view.btn_clear.setVisible(False)

    def is_show(self):
        return self.widget.isVisible()

    def hide(self):
        self.widget.hide()

    def display_wind_info(self, wind_speed, wind_speed_unit,  wind_dir, rain, alarm):
        if rain:
            strrain = self._translate("Rain", "Rain")
        else:
            strrain = self._translate("No Rain", "No Rain")
        self.view.WindInfo.setText(self._translate("Wind : ", "Wind : ") + '{:.1f}'.format(wind_speed) +
                                   wind_speed_unit + self._translate(", Angle : ", ", Angle : ") +
                                   str(wind_dir) + '°' + ', ' + strrain)

        if alarm:
            self.view.WindInfo.setStyleSheet('background-color:red;')
        else:
            self.view.WindInfo.setStyleSheet('background-color:rgba( 255, 255, 255, 0% );')


    def clear_alarm(self):
        self.rules['alarm'] = False
        self.view.Elapsedtime.setVisible(False)
        self.view.btn_clear.setVisible(False)

    def cancelroundtostr(self):
        cancelstr = ""
        if self.rules['alarm']:
            # cancelstr=', Cancel Round'
            cancelstr = ""
        return cancelstr

    def set_signal(self, voltage_sig):
        self.lowVoltage_sig = voltage_sig

    def set_voltage(self, voltage1, voltage2):
        self.view.voltage.setText("{:0>3.1f}V, {:0>3.1f}V".format(voltage1, voltage2))
        if voltage1 <= ConfigReader.config.conf['voltage_min_Accu1'] and \
                voltage2 <= ConfigReader.config.conf['voltage_min_Accu2'] and \
                self.voltagestylesheet == "background-color:rgba( 255, 255, 255, 0% );":
            self.voltagestylesheet = "background-color:red;"
            self.view.voltage.setStyleSheet(self.voltagestylesheet)
            if self.lowVoltage_sig is not None:
                self.lowVoltage_sig.emit()
        elif (voltage1 > ConfigReader.config.conf['voltage_min_Accu1'] or
              voltage2 > ConfigReader.config.conf['voltage_min_Accu2']) and \
                self.voltagestylesheet == "background-color:red;":
            self.voltagestylesheet = "background-color:rgba( 255, 255, 255, 0% );"
            self.view.voltage.setStyleSheet(self.voltagestylesheet)

    def set_picam(self, accu, rssi):
        self.view.rssi.setText(str(accu) + "V, " + str(rssi) + "%")


class WPilotCtrl(QObject):
    btn_cancel_flight_sig = pyqtSignal()
    btn_alarm_sig = pyqtSignal()

    def __init__(self, name, parent):
        super().__init__()
        self.view = Ui_WPilot()
        self.name = name
        self.parent = parent
        self.widget = QtWidgets.QWidget(parent)


        self.view.setupUi(self.widget)
        self._translate = QtCore.QCoreApplication.translate
        self.view.cancelRound.mousePressEvent = self.btn_cancel_flight
        self.view.cancelRound.setStyleSheet(director_btn_stylesheet)
        self.view.Btn_Alarm.clicked.connect(self.btn_alarm)
        #self.view.Btn_Alarm.setStyleSheet("border: 1px solid black;border-radius: 10px;")
        self.str_alarm_enable = self._translate("Enable Alarm", "Enable Alarm")
        self.str_alarm_disable = self._translate("Disable Alarm", "Disable Alarm")
        self.view.Btn_Alarm.setText(self.str_alarm_disable)
        self.alarm_enable = True

    def get_widget(self):
        return (self.widget)

    def show(self):
        self.widget.show()

    def is_show(self):
        return self.widget.isVisible()

    def hide(self):
        self.widget.hide()

    def btn_alarm(self):
        self.alarm_enable = not self.alarm_enable
        if self.alarm_enable:
            self.view.Btn_Alarm.setText(self.str_alarm_disable)
        else:
            self.view.Btn_Alarm.setText(self.str_alarm_enable)
        self.btn_alarm_sig.emit()

    def isalarm_enable(self):
        return self.alarm_enable

    def btn_cancel_flight(self, event):
        self.btn_cancel_flight_sig.emit()

    def set_data(self, competitor, round):
        self.view.pilotName.setText(competitor.display_name())
        self.view.bib.setText(self._translate("BIB : ", "BIB : ")
                              + str(competitor.get_bib_number()))
        self.view.round.setText(self._translate("Round : ", "Round : ")
                                + str(len(round.event.valid_rounds) + 1))
        self.view.group.setText(self._translate("Group : ", "Group : ") +
                                str(round.find_group(competitor).group_number))

    def handle_group_scoring_enabled(self, enabled):
        if enabled:
            self.view.cancelRound.setText(self._translate("Cancel Group", "Cancel Group"))
        else:
            self.view.cancelRound.setText(self._translate("Cancel Round", "Cancel Round"))


class WChronoCtrl(QTimer):
    btn_null_flight_sig = pyqtSignal()
    btn_penalty_100_sig = pyqtSignal()
    btn_penalty_1000_sig = pyqtSignal()
    btn_clear_penalty_sig = pyqtSignal()
    time_elapsed_sig = pyqtSignal()
    btn_refly_sig = pyqtSignal()

    def __init__(self, name, parent, vocal_elapsedTime_sig):
        super().__init__()

        self.view = Ui_WChrono()
        self.name = name
        self.parent = parent
        self.widget = QtWidgets.QWidget(parent)

        self._translate = QtCore.QCoreApplication.translate
        self.statusText = []
        self.statusText.append(self._translate("chronoStatus_WaitNewRun", "Wait New Run"))
        self.statusText.append(self._translate("chronoStatus_WaitToLaunch", "Wait To Launch"))
        self.statusText.append(self._translate("chronoStatus_Launched", "Launched"))
        self.statusText.append(self._translate("chronoStatus_L30s_reached", "30s reached"))
        self.statusText.append(self._translate("chronoStatus_InStart", "In Start"))
        self.statusText.append(self._translate("chronoStatus_I30s_reached", "In Start 30s reached"))
        self.statusText.append(self._translate("chronoStatus_InProgress", "In Progress"))
        self.statusText.append(self._translate("chronoStatus_InProgress", "In Progress"))
        self.statusText.append(self._translate("chronoStatus_WaitAltitude", "Wait Altitude"))
        self.statusText.append(self._translate("chronoStatus_Finished", "Finished"))

        self.vocal_elapsedTime_sig = vocal_elapsedTime_sig
        # initialize labels for lap time
        self.lap = []
        # initialize labels for status
        self.current_lap = 0
        self.current_status = 0
        self.view.setupUi(self.widget)

        # connect event btn
        self.view.nullFlight.mousePressEvent = self.null_flight
        self.view.penalty_100.mousePressEvent = self.penalty_100
        self.view.penalty_1000.mousePressEvent = self.penalty_1000
        self.view.btn_clear_penalty.clicked.connect(self.clear_penalty)
        self.view.reflight.mousePressEvent = self.btn_refly

        # change background color for important buttons

        self.view.penalty_100.setStyleSheet(penalty100_btn_stylesheet)
        self.view.penalty_1000.setStyleSheet(penalty1000_btn_stylesheet)
        self.view.reflight.setStyleSheet(refly_btn_stylesheet)
        self.view.nullFlight.setStyleSheet(director_btn_stylesheet)
        self.view.btn_clear_penalty.setStyleSheet(clear_penalty_btn_stylesheet)

        self.timerEvent = QTimer()
        self.timerEvent.timeout.connect(self.run)
        self.duration = 100
        self.startTime = time.time()
        self.time = 0
        self.time_up = True
        self.to_launch = False

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
            self.current_status = status
            self.view.Status.setText(self.statusText[status])

    def set_laptime(self, laptime):
        self.current_lap += 1
        if self.current_lap<10:
            self.view.Status.setText(self.statusText[self.current_status]+"  {:d}".format(self.current_lap))

    def set_finaltime(self, data_time):
        print("Widget chrono set final time : ", time.time())
        self.view.Time_label.setText("{:0.2f}".format(data_time))

    def reset_ui(self):
        self.stoptime()
        self.current_lap = 0
        self.set_penalty_value(0)
        self.set_null_flight(False)

    def settime(self, settime, count_up, starttimer=True, to_launch=False):
        self.to_launch = to_launch
        self.time = settime
        self.view.Time_label.setText("{:>6.0f}".format(self.time / 1000))
        self.time_up = count_up
        self.startTime = time.time()
        if starttimer:
            self.timerEvent.start(self.duration)

    def stoptime(self):
        self.timerEvent.stop()

    def run(self):
        if self.time_up:
            self.view.Time_label.setText("{:>6.0f}".format(time.time() - self.startTime))
        else:
            self.view.Time_label.setText("{:>6.0f}".format(self.time / 1000 - (time.time() - self.startTime)))
            timeval = self.time / 1000 - (time.time() - self.startTime)
            if timeval >= 29.5:
                self.vocal_elapsedTime_sig.emit(30, self.to_launch)
            if 25.5 <= timeval <= 26:
                self.vocal_elapsedTime_sig.emit(25, self.to_launch)
            if 20.5 <= timeval <= 21:
                self.vocal_elapsedTime_sig.emit(20, self.to_launch)
            if 15.5 <= timeval <= 16:
                self.vocal_elapsedTime_sig.emit(15, self.to_launch)
            if 10.5 <= timeval <= 11:
                self.vocal_elapsedTime_sig.emit(10, self.to_launch)
            '''
            if 9 <= timeval <= 10:
                self.vocal_elapsedTime_sig.emit(9, self.to_launch)
            if 8.9 <= timeval <= 9:
                self.vocal_elapsedTime_sig.emit(8, self.to_launch)
            if 7.9 <= timeval <= 8:
                self.vocal_elapsedTime_sig.emit(7, self.to_launch)
            if 6.9 <= timeval <= 7:
                self.vocal_elapsedTime_sig.emit(6, self.to_launch)
            if 5.9 <= timeval <= 6:
                self.vocal_elapsedTime_sig.emit(5, self.to_launch)
            if 4.9 <= timeval <= 5:
                self.vocal_elapsedTime_sig.emit(4, self.to_launch)
            if 3.9 <= timeval <= 4:
                self.vocal_elapsedTime_sig.emit(3, self.to_launch)
            if 2.9 <= timeval <= 3:
                self.vocal_elapsedTime_sig.emit(2, self.to_launch)
            if 1.9 <= timeval <= 2:
                self.vocal_elapsedTime_sig.emit(1, self.to_launch)
            '''
            if timeval < 0:
                self.vocal_elapsedTime_sig.emit(0, self.to_launch)
                self.time_elapsed_sig.emit()
                self.stoptime()

    def btn_refly(self, event):
        self.btn_refly_sig.emit()

    def penalty_100(self, event):
        self.btn_penalty_100_sig.emit()

    def penalty_1000(self, event):
        self.btn_penalty_1000_sig.emit()

    def clear_penalty(self):
        self.btn_clear_penalty_sig.emit()

    def set_penalty_value(self, value):
        self.view.penalty_value.setText(str(value))

    def null_flight(self, event):
        self.btn_null_flight_sig.emit()

    def set_null_flight(self, value=False):
        if (value):
            self.view.nullFlightLabel.setText(self._translate("Null Flight", "Null Flight"))
        else:
            self.view.nullFlightLabel.setText("")

    def set_refly(self, value=False):
        if (value):
            self.view.nullFlightLabel.setText(self._translate("Refly", "Refly"))
        else:
            self.view.nullFlightLabel.setText("")

    def display_wind_info(self, wind_speed, wind_speed_unit,  wind_dir, rain, alarm):
        self.view.WindInfo.setText('{:.1f}'.format(wind_speed) + wind_speed_unit + ', '+ str(wind_dir) + '°')

        if alarm:
            self.view.WindInfo.setStyleSheet('background-color:red;')
        else:
            self.view.WindInfo.setStyleSheet('background-color:rgba( 255, 255, 255, 0% );')


class WChronoTrainingCtrl(QObject):
    training_voice_sig = pyqtSignal(float, bool)

    def __init__(self, name, parent, speech_interval):
        super().__init__()

        self.view = Ui_WTraining()
        self.name = name
        self.parent = parent
        self.widget = QtWidgets.QWidget(parent)

        self._translate = QtCore.QCoreApplication.translate
        self.statusText = []
        self.statusText.append(self._translate("chronoStatus_WaitNewRun", "Wait New Run"))
        self.statusText.append(self._translate("chronoStatus_WaitToLaunch", "Wait To Launch"))
        self.statusText.append(self._translate("chronoStatus_Launched", "Launched"))
        self.statusText.append(self._translate("chronoStatus_L30s_reached", "30s reached"))
        self.statusText.append(self._translate("chronoStatus_InStart", "In Start"))
        self.statusText.append(self._translate("chronoStatus_I30s_reached", "In Start 30s reached"))
        self.statusText.append(self._translate("chronoStatus_InProgress", "In Progress"))
        self.statusText.append(self._translate("chronoStatus_InProgress", "In Progress"))
        self.statusText.append(self._translate("chronoStatus_WaitAltitude", "Wait Altitude"))
        self.statusText.append(self._translate("chronoStatus_Finished", "Finished"))

        # initialize labels for lap time
        self.run = []
        # initialize labels for status
        self.view.setupUi(self.widget)
        self.run.append(self.view.Lap1)
        self.run.append(self.view.Lap2)
        self.run.append(self.view.Lap3)
        self.run.append(self.view.Lap4)
        self.run.append(self.view.Lap5)
        self.run.append(self.view.Lap6)
        self.run.append(self.view.Lap7)
        self.run.append(self.view.Lap8)
        self.run.append(self.view.Lap9)
        self.run.append(self.view.Lap10)

        self.run_time = []
        self.min = 2000.0
        self.mean = 0.0
        self.max = 0.0

        self.training_speech_interval = speech_interval

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

    def set_time(self, lapcount, finaltime):
        self.view.lapNumber.setText(self._translate("Total Laps : ", "Total Laps : ") + "{:d}".format(lapcount))
        if lapcount >= 10:
            if lapcount % 2 == 0:
                self.run_time.append(finaltime)
                self.mean += finaltime
                self.view.runMean.setText(self._translate("Mean : ", "Mean : ")+"{:0>6.2f}".format(self.mean / ((lapcount - 10) / 2 + 1)))
                if finaltime < self.min:
                    self.min = finaltime
                    self.view.runMin.setText(self._translate("Min : ", "Min : ")+"{:0>6.2f}".format(self.min))
                if finaltime > self.max:
                    self.max = finaltime
                    self.view.runMax.setText(self._translate("Max : ", "Max : ")+"{:0>6.2f}".format(self.max))

            if len(self.run_time) > 10:
                del self.run_time[0]
            for i in range(len(self.run_time)):
                self.run[i].setText("{:d} : {:0>6.2f}".format(i + 1, self.run_time[i]))

            if (lapcount - 10) / 2 % self.training_speech_interval == 0:
                self.training_voice_sig.emit(finaltime, True)

    def reset(self):
        for run in self.run:
            run.setText("")
        self.view.runMin.setText(self._translate("Min : ", "Min : "))
        self.view.runMean.setText(self._translate("Mean : ", "Mean : "))
        self.view.runMax.setText(self._translate("Max : ", "Max : "))
        self.view.lapNumber.setText(self._translate("Total Laps : ", "Total Laps : "))
        self.run_time.clear()
        self.min = 2000.0
        self.mean = 0.0
        self.max = 0.0


class WConfigCtrl(QObject):
    btn_next_sig = pyqtSignal()
    contest_sig = pyqtSignal()
    contest_valuechanged_sig = pyqtSignal()
    chrono_sig = pyqtSignal()
    btn_settings_sig = pyqtSignal()
    btn_random_sig = pyqtSignal()
    btn_day_1_sig = pyqtSignal()
    btn_quitapp_sig = pyqtSignal()
    btn_shutdown_sig = pyqtSignal()
    widgetList = []

    def __init__(self, name, parent):
        super().__init__(parent)
        self.view = Ui_WConfig()
        self.name = name
        self.parent = parent
        self.widget = QtWidgets.QWidget(parent)
        self.view.setupUi(self.widget)
        self.widgetList.append(self.widget)
        self._translate = QtCore.QCoreApplication.translate

        # Event connect
        self.view.StartBtn.clicked.connect(self.btn_next)
        self.view.ContestList.currentIndexChanged.connect(self.contest_sig.emit)
        self.view.btn_settings.clicked.connect(self.btn_settings_sig.emit)
        self.view.WindMinValue.valueChanged.connect(self.contest_valuechanged_sig.emit)
        self.view.WindMaxValue.valueChanged.connect(self.contest_valuechanged_sig.emit)
        self.view.OrientationValue.valueChanged.connect(self.contest_valuechanged_sig.emit)
        self.view.RevolValue.valueChanged.connect(self.contest_valuechanged_sig.emit)
        self.view.bib_start.valueChanged.connect(self.bib_start_changed)
        self.view.bib_startslider.valueChanged.connect(self.bib_start_slider_changed)
        self.view.MaxInterruptValue.valueChanged.connect(self.contest_valuechanged_sig.emit)
        self.view.daydurationvalue.valueChanged.connect(self.contest_valuechanged_sig.emit)
        self.view.groups_number_value.valueChanged.connect(self.contest_valuechanged_sig.emit)

        self.view.randombtn.clicked.connect(self.btn_random_sig.emit)
        self.view.day_1btn.clicked.connect(self.btn_day_1_sig.emit)
        self.view.closebtn.clicked.connect(self.btn_quitapp_sig.emit)
        self.view.shutdownbtn.clicked.connect(self.btn_shutdown_sig.emit)


    def get_widget(self):
        return (self.widgetList)

    def show(self):
        self.widget.show()

    def is_show(self):
        return self.widget.isVisible()

    def hide(self):
        self.widget.hide()

    def btn_next(self):
        self.btn_next_sig.emit()

    def bib_start_changed(self):
        self.view.bib_startslider.setValue(self.view.bib_start.value())
        self.contest_valuechanged_sig.emit()

    def bib_start_slider_changed(self):
        self.view.bib_start.setValue(self.view.bib_startslider.value())

    def set_data(self, event):
        self.view.WindMinValue.setValue(event.min_allowed_wind_speed)
        self.view.WindMaxValue.setValue(event.max_allowed_wind_speed)
        self.view.OrientationValue.setValue(event.max_wind_dir_dev)
        self.view.RevolValue.setValue(event.flights_before_refly)
        self.view.bib_startslider.setMaximum(event.get_nb_competitors())
        self.view.bib_start.setValue(event.bib_start)
        self.view.MaxInterruptValue.setValue(event.max_interruption_time / 60)
        self.view.daydurationvalue.setValue(event.dayduration)
        self.view.groups_number_value.setValue(event.groups_number)

    def set_contest(self, contest_list):
        _translate = QtCore.QCoreApplication.translate
        self.chrono_sig.emit()
        self.view.ContestList.removeItem(0)
        self.view.ContestList.addItem(_translate("contest_training", "Training"), userData=None)
        for contest in contest_list:
            self.view.ContestList.addItem(contest.name, userData=contest)

        self.view.ContestList.setCurrentIndex(len(contest_list))

    def get_data(self):
        self.min_allowed_wind_speed = self.view.WindMinValue.value()
        self.max_allowed_wind_speed = self.view.WindMaxValue.value()
        self.max_wind_dir_dev = self.view.OrientationValue.value()
        self.max_interruption_time = self.view.MaxInterruptValue.value() * 60
        self.flights_before_refly = self.view.RevolValue.value()
        self.bib_start = self.view.bib_start.value()
        self.dayduration = self.view.daydurationvalue.value()
        self.contest = self.view.ContestList.currentIndex()
        self.groups_number = self.view.groups_number_value.value()


class WSettingsAdvanced(QObject):
    btn_settings_sig = pyqtSignal()
    btn_valid_sig = pyqtSignal()
    btn_cancel_sig = pyqtSignal()
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
        self.view.btn_cancel.clicked.connect(self.btn_cancel_sig.emit)
        self.view.btn_valid.clicked.connect(self.btn_valid_sig.emit)
        self._translate = QtCore.QCoreApplication.translate

    def get_widget(self):
        return (self.widgetList)

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
        self.view.port_buzzer.setValue(ConfigReader.config.conf['buzzer'])
        self.view.buzzer_duration.setValue(ConfigReader.config.conf['buzzer_duration'])
        self.view.port_buzzer_next.setValue(ConfigReader.config.conf['buzzer_next'])
        self.view.buzzer_next_duration.setValue(ConfigReader.config.conf['buzzer_next_duration'])
        self.view.udp_port.setValue(ConfigReader.config.conf['udpport'])
        self.view.voltagemin_1.setValue(ConfigReader.config.conf['voltage_min_Accu1'])
        self.view.voltagecoef_1.setValue(ConfigReader.config.conf['voltage_coef_Accu1'])
        self.view.voltagemin_2.setValue(ConfigReader.config.conf['voltage_min_Accu2'])
        self.view.voltagecoef_2.setValue(ConfigReader.config.conf['voltage_coef_Accu2'])

    def get_data(self):
        ConfigReader.config.conf['btn_baseA'] = self.view.port_btn_baseA.value()
        ConfigReader.config.conf['btn_baseB'] = self.view.port_btn_baseB.value()
        ConfigReader.config.conf['btn_next'] = self.view.port_btn_next.value()
        ConfigReader.config.conf['buzzer'] = self.view.port_buzzer.value()
        ConfigReader.config.conf['buzzer_duration'] = self.view.buzzer_duration.value()
        ConfigReader.config.conf['buzzer_next'] = self.view.port_buzzer_next.value()
        ConfigReader.config.conf['buzzer_next_duration'] = self.view.buzzer_next_duration.value()
        ConfigReader.config.conf['udpport'] = self.view.udp_port.value()
        ConfigReader.config.conf['voltage_min_Accu1'] = self.view.voltagemin_1.value()
        ConfigReader.config.conf['voltage_coef_Accu1'] = self.view.voltagecoef_1.value()
        ConfigReader.config.conf['voltage_min_Accu2'] = self.view.voltagemin_2.value()
        ConfigReader.config.conf['voltage_coef_Accu2'] = self.view.voltagecoef_2.value()

class WSettingsQrCode(QObject):
    btn_back_sig = pyqtSignal()
    widgetList = []

    def __init__(self, name, parent):
        super().__init__()
        self.view = Ui_WSettingsQrCode()
        self.name = name
        self.parent = parent
        self.widget = QtWidgets.QWidget(parent)
        self.view.setupUi(self.widget)
        self.widgetList.append(self.widget)
        self.view.btn_back.clicked.connect(self.btn_back_sig.emit)
        self.view.btn_AdminQRCode.clicked.connect(self.displayAdminQrCode)
        self._translate = QtCore.QCoreApplication.translate

    def get_widget(self):
        return (self.widgetList)

    def show(self):
        self.widget.show()

    def is_show(self):
        return self.widget.isVisible()

    def hide(self):
        self.widget.hide()

    def displayF3FRankingQrCode(self):
        import pyqrcode
        import qrcode
        import png
        from PyQt5 import QtCore
        from PyQt5.QtGui import QPixmap, QImage
        import io
        from pyqrcode import QRCode
        from PIL.ImageQt import ImageQt

        # Generate QR code
        url = pyqrcode.create(Utils.get_base_url())
        buffer = io.BytesIO()
        url.png(buffer, scale=5)

        image = QImage()
        image.loadFromData(buffer.getvalue())

        # Create and save the png file naming "saved_qr.png"
        #url.png('saved_qr.png', scale=5)
        pixmap01 = QPixmap(image)
        self.view.label_2.setPixmap(pixmap01)
        self.view.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.view.label_2.setScaledContents(False)
        self.view.label_2.setMinimumSize(1, 1)

    def displayAdminQrCode(self):
        import pyqrcode
        import qrcode
        import png
        from PyQt5 import QtCore
        from PyQt5.QtGui import QPixmap, QImage
        import io
        from pyqrcode import QRCode
        from PIL.ImageQt import ImageQt

        self.view.label.setText(self._translate("Admin QR Code", "Admin QR Code"))
        # Generate QR code
        url = pyqrcode.create(Utils.get_administrator_url())
        buffer = io.BytesIO()
        url.png(buffer, scale=5, module_color=[255, 0, 0])

        image = QImage()
        image.loadFromData(buffer.getvalue())

        # Create and save the png file naming "saved_qr.png"
        #url.png('saved_qr.png', scale=5)
        pixmap01 = QPixmap(image)
        self.view.label_2.setPixmap(pixmap01)
        self.view.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.view.label_2.setScaledContents(False)
        self.view.label_2.setMinimumSize(1, 1)

class WSettingsBase(QObject):
    btn_settings_sig = pyqtSignal()
    btn_valid_sig = pyqtSignal()
    btn_cancel_sig = pyqtSignal()
    widgetList = []
    baseAList = []
    baseBList = []
    viewbaseAList = []
    viewbaseBList = []
    widgetBaseList = []

    def __init__(self, name, parent):
        super().__init__()
        self.view = Ui_WSettingsBase()
        self.name = name
        self.parent = parent
        self.widget = QtWidgets.QWidget(parent)
        self.view.setupUi(self.widget)
        self.widgetList.append(self.widget)
        self.view.buttonBaseADetect.clicked.connect(self.baseA_detect)
        self.view.buttonBaseBDetect.clicked.connect(self.baseB_detect)
        self.view.buttonClearA.clicked.connect(self.clearA)
        self.view.buttonClearB.clicked.connect(self.clearB)
        self.view.buttonInvert.clicked.connect(self.moveAll)
        self.view.btn_back.clicked.connect(self.btn_settings_sig.emit)
        self.view.btn_cancel.clicked.connect(self.btn_cancel_sig.emit)
        self.view.btn_valid.clicked.connect(self.btn_valid_sig.emit)
        self._translate = QtCore.QCoreApplication.translate
        self.udp_sig = None
        self.ipset_sig = None
        self.ipbaseclear_sig = None
        self.udp_sig_connected = False
        self.ipbaseinvert_sig = None
        self.baseInProgress = None
        self.Detect_label = self._translate("Detect", "Detect")
        self.inprogress_label = self._translate("In Progress...", "In Progress...")

    def get_widget(self):
        return (self.widgetList)

    def show(self):
        self.widget.show()

    def is_show(self):
        return self.widget.isVisible()

    def hide(self):
        self.widget.hide()

    def set_data(self):
        self.view.inStartBlackOut.setChecked(ConfigReader.config.conf['inStartBlackOut'])
        self.view.inStartBlackOut_second.setValue(ConfigReader.config.conf['inStartBlackOut_second'])

    def get_data(self):
        ConfigReader.config.conf['inStartBlackOut'] = self.view.inStartBlackOut.isChecked()
        ConfigReader.config.conf['inStartBlackOut_second'] = self.view.inStartBlackOut_second.value()

    def set_udp_sig(self, udp, set, clear, invert):
        self.udp_sig = udp
        self.ipset_sig = set
        self.ipbaseclear_sig = clear
        self.ipbaseinvert_sig = invert

    def baseA_detect(self):
        self.__baseB_release()
        if self.udp_sig is not None and self.ipbaseclear_sig is not None and self.baseInProgress == None:
            self.udp_sig.connect(self.slot_udp)
            self.ipbaseclear_sig.emit()
            self.view.buttonBaseADetect.setText(self.inprogress_label)
            self.udp_sig_connected = True
            self.baseInProgress = 'A'
        else:
            self.__baseA_release()

    def baseB_detect(self):
        self.__baseA_release()
        if self.udp_sig is not None and self.ipbaseclear_sig is not None and self.baseInProgress == None:
            self.udp_sig.connect(self.slot_udp)
            self.ipbaseclear_sig.emit()
            self.view.buttonBaseBDetect.setText(self.inprogress_label)
            self.udp_sig_connected = True
            self.baseInProgress = 'B'
        else:
            self.__baseB_release()

    def slot_udp(self, address):
        print(address)
        if self.baseInProgress == 'A' and self.__ipNotPresent(self.baseAList, address) \
                and self.__ipNotPresent(self.baseBList, address):
            self.__addbase_List(self.baseAList, self.view.listWidget_baseA, address, self.deleteItemBaseA,
                                self.moveItemBaseA)
        elif self.baseInProgress == 'B' and self.__ipNotPresent(self.baseAList, address) \
                and self.__ipNotPresent(self.baseBList, address):
            self.__addbase_List(self.baseBList, self.view.listWidget_baseB, address, self.deleteItemBaseB,
                                self.moveItemBaseB)

    def clearA(self):
        self.view.listWidget_baseA.clear()
        self.baseAList.clear()

    def deleteItemBaseA(self):
        self.__deleteWidgetinQlistWidget(self.baseAList, self.view.listWidget_baseA, self.sender().parent().pos())

    def clearB(self):
        self.view.listWidget_baseB.clear()
        self.baseBList.clear()

    def deleteItemBaseB(self):
        self.__deleteWidgetinQlistWidget(self.baseBList, self.view.listWidget_baseB, self.sender().parent().pos())

    def moveItemBaseA(self):
        ip = self.__deleteWidgetinQlistWidget(self.baseAList, self.view.listWidget_baseA, self.sender().parent().pos())
        self.__addbase_List(self.baseBList, self.view.listWidget_baseB, ip, self.deleteItemBaseB,
                            self.moveItemBaseB)

    def moveItemBaseB(self):
        ip = self.__deleteWidgetinQlistWidget(self.baseBList, self.view.listWidget_baseB, self.sender().parent().pos())
        self.__addbase_List(self.baseAList, self.view.listWidget_baseA, ip, self.deleteItemBaseA,
                            self.moveItemBaseA)

    def moveAll(self):
        ipA=self.__getAllIp(self.baseAList)
        ipB=self.__getAllIp(self.baseBList)

        self.clearA()
        for ip in ipB:
            self.__addbase_List(self.baseAList, self.view.listWidget_baseA, ip, self.deleteItemBaseA,
                                self.moveItemBaseA)
        self.clearB()
        for ip in ipA:
            self.__addbase_List(self.baseBList, self.view.listWidget_baseB, ip, self.deleteItemBaseB,
                                self.moveItemBaseB)

    def get_ipbaseA(self):
        return self.__getAllIp(self.baseAList)

    def get_ipbaseB(self):
        return self.__getAllIp(self.baseBList)

    def btn_cancel(self):
        self.__baseA_release()
        self.__baseB_release()
        if self.udp_sig is not None and self.udp_sig_connected:
            self.udp_sig.disconnect(self.slot_udp)
            self.udp_sig_connected = False
        '''if self.ipbaseclear_sig is not None:
            self.ipbaseclear_sig.emit()
            self.clearA()
            self.clearB()
        '''

    def btn_valid(self):
        self.__baseA_release()
        self.__baseB_release()
        if self.udp_sig is not None and self.udp_sig_connected:
            self.udp_sig.disconnect(self.slot_udp)
            self.udp_sig_connected = False
        if self.ipset_sig is not None:
            self.ipset_sig.emit(self.get_ipbaseA(), self.get_ipbaseB())

    def __baseA_release(self):
        if self.baseInProgress == 'A':
            self.baseInProgress = None
            self.udp_sig.disconnect(self.slot_udp)
            self.udp_sig_connected = False
            self.view.buttonBaseADetect.setText(self.Detect_label)

    def __baseB_release(self):
        if self.baseInProgress == 'B':
            self.baseInProgress = None
            self.udp_sig.disconnect(self.slot_udp)
            self.udp_sig_connected = False
            self.view.buttonBaseBDetect.setText(self.Detect_label)

    @staticmethod
    def __addbase_List (list, uilist, ip, deleteEvent, moveEvent):
        collect = collections.OrderedDict()
        collect['QlistWidgetItem'] = QtWidgets.QListWidgetItem()
        collect['QWidget'] = QtWidgets.QWidget()
        collect['ui_widget'] = Ui_WSettingBase_item()
        list.append(collect)
        uilist.addItem(list[-1]['QlistWidgetItem'])

        list[-1]['ui_widget'].setupUi(list[-1]['QWidget'])
        list[-1]['ui_widget'].ipAddress.setText(ip)
        list[-1]['ui_widget'].buttonDelete.clicked.connect(deleteEvent)
        list[-1]['ui_widget'].buttonMove.clicked.connect(moveEvent)
        uilist.setItemWidget(list[-1]['QlistWidgetItem'], list[-1]['QWidget'])

    @staticmethod
    def __getWidgetinQlistWidget (list, uilist, pos):
        item = uilist.itemAt(pos)
        for index in list:
            if index['QlistWidgetItem'] == item:
                return index['ui_widget']

    @staticmethod
    def __deleteWidgetinQlistWidget (list, uilist, pos):
        ip=""
        item = uilist.itemAt(pos)
        itemdelete = None
        for i in range(len(list)):
            if list[i]['QlistWidgetItem'] == item:
                itemdelete = i
        if itemdelete is not None:
            ip = list[itemdelete]['ui_widget'].ipAddress.text()
            del(list[itemdelete])
            uilist.takeItem(itemdelete)
        return ip

    @staticmethod
    def __ipNotPresent(list, ip):
        for i in range(len(list)):
            if list[i]['ui_widget'].ipAddress.text()==ip:
                return False
        return True

    @staticmethod
    def __getAllIp(list):
        ip = []
        for i in list:
            ip.append(i['ui_widget'].ipAddress.text())
        return ip

class WSettingswBtn(QObject):
    btn_settings_sig = pyqtSignal()
    btn_valid_sig = pyqtSignal()
    btn_cancel_sig = pyqtSignal()
    widgetList = []
    wBtnList = []
    viewwBtnList = []
    widgetwBtnList = []

    def __init__(self, name, parent):
        super().__init__()
        self.view = Ui_WSettingswBtn()
        self.name = name
        self.parent = parent
        self.widget = QtWidgets.QWidget(parent)
        self.view.setupUi(self.widget)
        self.widgetList.append(self.widget)
        self.view.buttonDetect.clicked.connect(self.wBtn_detect)
        self.view.buttonClear.clicked.connect(self.clearwBtn)
        self.view.btn_back.clicked.connect(self.btn_settings_sig.emit)
        self.view.btn_cancel.clicked.connect(self.btn_cancel_sig.emit)
        self.view.btn_valid.clicked.connect(self.btn_valid_sig.emit)
        self._translate = QtCore.QCoreApplication.translate
        self.udp_sig = None
        self.ipset_sig = None
        self.ipwBtnclear_sig = None
        self.udp_sig_connected = False
        self.wBtnInProgress = None
        self.Detect_label = self._translate("Detect", "Detect")
        self.inprogress_label = self._translate("In Progress...", "In Progress...")

    def get_widget(self):
        return (self.widgetList)

    def show(self):
        self.widget.show()

    def is_show(self):
        return self.widget.isVisible()

    def hide(self):
        self.widget.hide()

    def set_data(self):
        print("Settings wBtn set_data")

    def get_data(self):
        print("Settings wBtn get_data")

    def set_udp_sig(self, udp, set, clear):
        self.udp_sig = udp
        self.ipset_sig = set
        self.ipwBtnclear_sig = clear


    def wBtn_detect(self):
        if self.udp_sig is not None and self.ipwBtnclear_sig is not None and self.wBtnInProgress == None:
            self.udp_sig.connect(self.slot_udp)
            self.ipwBtnclear_sig.emit()
            self.view.buttonDetect.setText(self.inprogress_label)
            self.udp_sig_connected = True
            self.wBtnInProgress = True
        else:
            self.__release_detect()

    def slot_udp(self, address):
        if self.wBtnInProgress and self.__ipNotPresent(self.wBtnList, address):
            self.__addwBtn_List(self.wBtnList, self.view.listWidget_wBtn, address, self.deleteItemwBtn)

    def clearwBtn(self):
        self.view.listWidget_wBtn.clear()
        self.wBtnList.clear()
        if self.ipwBtnclear_sig is not None:
            self.ipwBtnclear_sig.emit()

    def deleteItemwBtn(self):
        self.__deleteWidgetinQlistWidget(self.wBtnList, self.view.listWidget_wBtn, self.sender().parent().pos())

    def get_ipwBtn(self):
        return self.__getAllIp(self.wBtnList)


    def btn_cancel(self):
        self.__release_detect()
        #self.clearwBtn()

    def btn_valid(self):
        self.__release_detect()
        if self.ipset_sig is not None:
            ip = self.get_ipwBtn()
            self.ipset_sig.emit(ip[0], ip[1], ip[2], ip[3], ip[4])

    def __release_detect(self):
        if self.wBtnInProgress:
            self.wBtnInProgress = None
            self.udp_sig.disconnect(self.slot_udp)
            self.udp_sig_connected = False
            self.view.buttonDetect.setText(self.Detect_label)

    @staticmethod
    def __addwBtn_List (list, uilist, ip, deleteEvent):
        collect = collections.OrderedDict()
        collect['QlistWidgetItem'] = QtWidgets.QListWidgetItem()
        collect['QWidget'] = QtWidgets.QWidget()
        collect['ui_widget'] = Ui_WSettingwBtn_item()
        list.append(collect)
        uilist.addItem(list[-1]['QlistWidgetItem'])

        list[-1]['ui_widget'].setupUi(list[-1]['QWidget'])
        list[-1]['ui_widget'].ipAddress.setText(ip)
        list[-1]['ui_widget'].buttonDelete.clicked.connect(deleteEvent)
        uilist.setItemWidget(list[-1]['QlistWidgetItem'], list[-1]['QWidget'])

    @staticmethod
    def __getWidgetinQlistWidget (list, uilist, pos):
        item = uilist.itemAt(pos)
        for index in list:
            if index['QlistWidgetItem'] == item:
                return index['ui_widget']

    @staticmethod
    def __deleteWidgetinQlistWidget (list, uilist, pos):
        ip = ""
        item = uilist.itemAt(pos)
        itemdelete = None
        for i in range(len(list)):
            if list[i]['QlistWidgetItem'] == item:
                itemdelete = i
        if itemdelete is not None:
            ip = list[itemdelete]['ui_widget'].ipAddress.text()
            del(list[itemdelete])
            uilist.takeItem(itemdelete)
        return ip

    @staticmethod
    def __ipNotPresent(list, ip):
        for i in range(len(list)):
            if list[i]['ui_widget'].ipAddress.text() == ip:
                return False
        return True

    @staticmethod
    def __getAllIp(list):
        baseA = [[], [], []]
        baseB = [[], [], []]
        btn_next = [[], [], []]
        switchMode = [[], [], []]
        penalty = [[], [], []]
        for i in list:
            index = i['ui_widget'].comboBox_LP.currentIndex()
            if index == 1:
                baseA[0].append(i['ui_widget'].ipAddress.text())
            elif index == 2:
                baseB[0].append(i['ui_widget'].ipAddress.text())
            elif index == 3:
                btn_next[0].append(i['ui_widget'].ipAddress.text())
            elif index == 4:
                switchMode[0].append(i['ui_widget'].ipAddress.text())
            elif index == 5:
                penalty[0].append(i['ui_widget'].ipAddress.text())

            index = i['ui_widget'].comboBox_SP.currentIndex()
            if index == 1:
                baseA[1].append(i['ui_widget'].ipAddress.text())
            elif index == 2:
                baseB[1].append(i['ui_widget'].ipAddress.text())
            elif index == 3:
                btn_next[1].append(i['ui_widget'].ipAddress.text())
            elif index == 4:
                switchMode[1].append(i['ui_widget'].ipAddress.text())
            elif index == 5:
                penalty[1].append(i['ui_widget'].ipAddress.text())

            index = i['ui_widget'].comboBox_CL.currentIndex()
            if index == 1:
                baseA[2].append(i['ui_widget'].ipAddress.text())
            elif index == 2:
                baseB[2].append(i['ui_widget'].ipAddress.text())
            elif index == 3:
                btn_next[2].append(i['ui_widget'].ipAddress.text())
            elif index == 4:
                switchMode[2].append(i['ui_widget'].ipAddress.text())
            elif index == 5:
                penalty[2].append(i['ui_widget'].ipAddress.text())

        return baseA, baseB, btn_next, switchMode, penalty

class WSettingsSound(QObject):
    btn_settings_sig = pyqtSignal()
    btn_valid_sig = pyqtSignal()
    btn_cancel_sig = pyqtSignal()
    widgetList = []

    def __init__(self, name, parent):
        super().__init__()
        self.view = Ui_WSettingsSound()
        self.name = name
        self.parent = parent
        self.widget = QtWidgets.QWidget(parent)
        self.view.setupUi(self.widget)
        self.widgetList.append(self.widget)
        self.view.btn_back.clicked.connect(self.btn_settings_sig.emit)
        self._translate = QtCore.QCoreApplication.translate
        self.view.btn_cancel.clicked.connect(self.btn_cancel_sig.emit)
        self.view.btn_valid.clicked.connect(self.btn_valid_sig.emit)
        self.view.soundslider.valueChanged.connect(self.soundslider_changed)
        self.view.soundvolume.valueChanged.connect(self.soundvolume_changed)
        self.view.noiseslider.valueChanged.connect(self.noiseslider_changed)
        self.view.noisevolume.valueChanged.connect(self.noisevolume_changed)

    def get_widget(self):
        return (self.widgetList)

    def show(self):
        self.widget.show()

    def is_show(self):
        return self.widget.isVisible()

    def hide(self):
        self.widget.hide()

    def soundvolume_changed(self):
        self.view.soundslider.setValue(self.view.soundvolume.value())

    def soundslider_changed(self):
        self.view.soundvolume.setValue(self.view.soundslider.value())

    def noisevolume_changed(self):
        self.view.noiseslider.setValue(self.view.noisevolume.value())

    def noiseslider_changed(self):
        self.view.noisevolume.setValue(self.view.noiseslider.value())

    def set_data(self):
        self.view.sound.setChecked(ConfigReader.config.conf['sound'])
        self.view.soundvolume.setValue(ConfigReader.config.conf['soundvolume']*100)
        self.view.buzzer.setChecked(ConfigReader.config.conf['buzzer_valid'])
        self.view.buzzernext.setChecked(ConfigReader.config.conf['buzzer_next_valid'])
        self.view.lowVoltage.setChecked(ConfigReader.config.conf['lowvoltage_sound'])
        self.view.noiseSound.setChecked(ConfigReader.config.conf['noisesound'])
        self.view.noisevolume.setValue(ConfigReader.config.conf['noisevolume']*100)


    def get_data(self):
        ConfigReader.config.conf['sound'] = self.view.sound.isChecked()
        ConfigReader.config.conf['soundvolume'] = self.view.soundvolume.value() / 100
        ConfigReader.config.conf['buzzer_valid'] = self.view.buzzer.isChecked()
        ConfigReader.config.conf['buzzer_next_valid'] = self.view.buzzernext.isChecked()
        ConfigReader.config.conf['lowvoltage_sound'] = self.view.lowVoltage.isChecked()
        ConfigReader.config.conf['noisesound'] = self.view.noiseSound.isChecked()
        ConfigReader.config.conf['noisevolume'] = self.view.noisevolume.value()/100

class WSettingsWirelessDevices(QObject):
    btn_settingsbase_sig = pyqtSignal()
    btn_settingswBtn_sig = pyqtSignal()
    btn_AnemometerGetList_sig = pyqtSignal()
    btn_AnemometerConnect_sig = pyqtSignal(str)
    btn_settingsback_sig = pyqtSignal()
    btn_cancel_sig = pyqtSignal()
    btn_valid_sig = pyqtSignal()
    widgetList = []

    def __init__(self, name, parent):
        super().__init__()
        self.view = Ui_WSettingsConnectedDevices()
        self.name = name
        self.parent = parent
        self.widget = QtWidgets.QWidget(parent)
        self._translate = QtCore.QCoreApplication.translate
        self.view.setupUi(self.widget)
        self.widgetList.append(self.widget)
        self.view.btn_AnemometerConnect.clicked.connect(self.anemometerconnect)
        self.view.btn_AnemometerGetList.clicked.connect(self.btn_AnemometerGetList_sig.emit)
        self.view.btn_base_settings.clicked.connect(self.btn_settingsbase_sig.emit)
        self.view.wbtn_settings.clicked.connect(self.btn_settingswBtn_sig.emit)
        self.view.btn_back.clicked.connect(self.btn_settingsback_sig.emit)
        self.view.btn_cancel.clicked.connect(self.btn_cancel_sig.emit)
        self.view.btn_valid.clicked.connect(self.btn_valid_sig.emit)
        self.view.AnemometerComboBox.clear()


    def get_widget(self):
        return (self.widgetList)

    def show(self):
        self.widget.show()

    def is_show(self):
        return self.widget.isVisible()

    def hide(self):
        self.widget.hide()

    def set_data(self):
        self.view.display.setChecked(ConfigReader.config.conf['F3FDisplay'])

    def get_data(self):
        ConfigReader.config.conf['F3FDisplay'] = self.view.display.isChecked()

    def anemometerSetData(self, datalist):
        self.view.AnemometerComboBox.clear()
        for i in datalist:
            self.view.AnemometerComboBox.addItem(i)

    def anemometerconnect(self):
        self.btn_AnemometerConnect_sig.emit(self.view.AnemometerComboBox.currentText())

    def weatherStation_display(self, wind_speed, wind_speed_unit, wind_speed_ispresent,
                               wind_dir, wind_dir_voltage, wind_dir_voltage_alarm, wind_dir_ispresent,
                               rain, rain_ispresent):
        if wind_speed_ispresent:
            self.view.WeatherStation_Speed.setText("WindSpeed : "+"{:0>.1f}".format(wind_speed) + wind_speed_unit)
            self.view.WeatherStation_Speed.setStyleSheet("background-color:rgba( 255, 255, 255, 0% );")
        else:
            self.view.WeatherStation_Speed.setText("WindSpeed : --")
            self.view.WeatherStation_Speed.setStyleSheet("background-color:red;")
        if wind_dir_ispresent:
            self.view.WeatherStation_Dir.setText("Dir : " + "{:0>.1f}".format(wind_dir)+ ", " +
                                                 "{:0>.1f}".format(wind_dir_voltage)+"V")
            if wind_dir_voltage_alarm:
                self.view.WeatherStation_Dir.setStyleSheet("background-color:red;")
            else:
                self.view.WeatherStation_Dir.setStyleSheet("background-color:rgba( 255, 255, 255, 0% );")
        else:
            self.view.WeatherStation_Dir.setText("Dir : --")
            self.view.WeatherStation_Dir.setStyleSheet("background-color:red;")
        if rain_ispresent:
            if rain:
                self.view.WeatherStation_Rain.setText("rain : Yes")
            else:
                self.view.WeatherStation_Rain.setText("rain : No")
            self.view.WeatherStation_Rain.setStyleSheet("background-color:rgba( 255, 255, 255, 0% );")
        else:
            self.view.WeatherStation_Rain.setText("rain : --")
            self.view.WeatherStation_Rain.setStyleSheet("background-color:red;")

class WSettings(QObject):
    btn_settingsadvanced_sig = pyqtSignal()
    btn_settingswDevices_sig = pyqtSignal()
    btn_settingssound_sig = pyqtSignal()
    btn_cancel_sig = pyqtSignal()
    btn_valid_sig = pyqtSignal()
    qrcode_sig = pyqtSignal(str)
    widgetList = []

    def __init__(self, name, parent):
        super().__init__()
        self.view = Ui_WSettings()
        self.name = name
        self.parent = parent
        self.widget = QtWidgets.QWidget(parent)
        self._translate = QtCore.QCoreApplication.translate
        self.view.setupUi(self.widget)
        self.widgetList.append(self.widget)
        self.view.btn_advanced_settings.clicked.connect(self.btn_settingsadvanced_sig.emit)
        self.view.btn_wDevices_settings.clicked.connect(self.btn_settingswDevices_sig.emit)
        self.view.btn_sound_settings.clicked.connect(self.btn_settingssound_sig.emit)
        self.view.webserverUrl.clicked.connect(self.qrCode)

        self.view.btn_cancel.clicked.connect(self.btn_cancel_sig.emit)
        self.view.btn_valid.clicked.connect(self.btn_valid_sig.emit)

        self.languages_available = []

        for dI in os.listdir('Languages'):
            if os.path.isdir(os.path.join('Languages', dI)):
                self.languages_available.append(dI)
        self.view.language.clear()
        for item in self.languages_available:
            self.view.language.addItem(item, item)

    def get_widget(self):
        return (self.widgetList)

    def show(self):
        if Utils.server_alive():
            self.view.webserverUrl.setText(Utils.get_base_url())
        self.widget.show()

    def is_show(self):
        return self.widget.isVisible()

    def hide(self):
        self.widget.hide()

    def set_data(self):
        self.view.simulate_mode.setChecked(ConfigReader.config.conf['simulatemode'])
        self.view.fullscreen.setChecked(ConfigReader.config.conf['fullscreen'])
        self.view.webserver.setChecked(ConfigReader.config.conf['run_webserver'])
        self.view.mode.setCurrentIndex(ConfigReader.config.conf['competition_mode'])
        index=0
        if ConfigReader.config.conf['language'] in self.languages_available:
            index=self.languages_available.index(ConfigReader.config.conf['language'])
        self.view.language.setCurrentIndex(index)

    def get_data(self):
        ConfigReader.config.conf['simulatemode'] = self.view.simulate_mode.isChecked()
        ConfigReader.config.conf['fullscreen'] = self.view.fullscreen.isChecked()
        ConfigReader.config.conf['run_webserver'] = self.view.webserver.isChecked()
        ConfigReader.config.conf['competition_mode'] = self.view.mode.currentIndex()
        ConfigReader.config.conf['language']=self.languages_available[self.view.language.currentIndex()]

    def qrCode(self):
        self.qrcode_sig.emit(self.view.webserverUrl.text())