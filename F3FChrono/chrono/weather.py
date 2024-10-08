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

import time
import collections
from PyQt5.QtCore import pyqtSignal, QObject, QTimer
from F3FChrono.chrono.UDPSend import *
from F3FChrono.chrono import ConfigReader
from F3FChrono.Utils import get_ip
from F3FChrono.chrono import Chrono

class alarm():
    Release = 0,
    Alarm=1,
    Waiting=2

class weatherState():
    init = 0,
    Nominal = 1,
    condNok = 2,
    condMarginal = 3,
    Stabilizing = 4



class anemometer(QObject):
    list_sig = pyqtSignal(list)
    status_sig = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        ip, broadcast = get_ip()
        self.udpSend = udpsend(broadcast, ConfigReader.config.conf['udpport'])

    def GetList(self):
        self.udpSend.sendData("anemometerGetList")

    def Connect(self, index):
        self.udpSend.sendData("anemometerConnect " + index)

class Weather(QTimer):
    #parameters : value, unit
    windspeed_signal = pyqtSignal(float, str)
    #parameters : direction, accu voltage
    winddir_signal = pyqtSignal(float, float)
    rain_signal = pyqtSignal(bool)
    # gui_weather_signal parameters wind_speed, wind_speed_unit,  wind_dir, rain, alarm, status
    gui_weather_signal = pyqtSignal(float, str, float, float, bool, str)
    #parameters : wind_speed, wind_speed_unit, wind_speed_ispresent, wind_dir, wind_dir_voltage, wind_dir_voltage_alarme,
    #wind_dir_ispresent, rain, rain_ispresent
    gui_wind_speed_dir_signal = pyqtSignal(float, str, bool, float, float, bool, bool, bool, bool)
    beep_signal = pyqtSignal(str, int, int)

    weather_lowVoltage_signal = pyqtSignal()
    weather_sensor_lost = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.anemometer = anemometer()
        self.handleSpeed = None
        self.handleDir = None
        self.handleRain = None
        self.weather = collections.OrderedDict()
        self.rules = collections.OrderedDict()
        self.reset_weather(first=True)
        self.__debug = False
        self.windDirVoltage = 20.0
        self.windDir_isPresent = True
        self.windSpeed_isPresent = True
        self.rain_isPresent = True
        self.windDir_enable = ConfigReader.config.conf['enableSensorDir']
        self.windSpeed_enable = ConfigReader.config.conf['enableSensorSpeed']
        self.rain_enable = ConfigReader.config.conf['enableSensorRain']
        self.rules['speed_limit_min'] = -1.0
        self.rules['speed_limit_max'] = -1.0
        self.rules['dir_limit'] = -1.0
        self.rules['wind_dir_voltage_min'] = ConfigReader.config.conf['voltage_min_windDir']
        self.rules['wind_dir_voltage_alarm'] = alarm.Release
        self.rules['sensor_voltage_alarm'] = alarm.Release
        self.rules['sensor_lost_alarm'] = alarm.Release
        self.rules['state'] = weatherState.init
        self.rules['MCInRun'] = False
        self.chronostatus = Chrono.chronoStatus.InWait
        self.__rules_enable = False
        self.timeout.connect(self.refresh_gui)
        self.start(2000)
        self.weatherBeep = ConfigReader.config.conf['weather_Beep']
        self.weatherSound = True
        self.sensorAlarmTimeOut = ConfigReader.config.conf['SensorAlarmTimeout']
        self.weatherTimeOutOkDc = ConfigReader.config.conf['weather_TimeOut_OkDC']
        self.weatherTimeOutMarginalcond = ConfigReader.config.conf['weather_TimeOut_MarginalCond']
        self.weatherBeepNok = ConfigReader.config.conf['weather_beep_nok']
        self.weatherBeepOkDc = ConfigReader.config.conf['weather_beep_okDC']
        self.timerOkDC = QTimer()
        self.timerMarginal = QTimer()
        self.timerDir = QTimer()
        self.timerSpeed = QTimer()
        self.timerRain = QTimer()
        self.timerOkDC.timeout.connect(self.slot_okDC)
        self.timerMarginal.timeout.connect(self.slot_Marginal)
        self.timerDir.timeout.connect(self.timeoutDir)
        self.timerSpeed.timeout.connect(self.timeoutSpeed)
        self.timerRain.timeout.connect(self.timeoutRain)
        self.setConfig()
        self.status = "Init"
        self.vocal = weatherVocal(ConfigReader.config.conf['weather_vocal_blank_ms'])

    def setConfig(self):
        self.windDir_enable = ConfigReader.config.conf['enableSensorDir']
        self.windSpeed_enable = ConfigReader.config.conf['enableSensorSpeed']
        self.rain_enable = ConfigReader.config.conf['enableSensorRain']

        if self.windSpeed_enable:
            self.handleSpeed = self.windspeed_signal.connect(self.slot_wind_speed)
            self.timerSpeed.start(self.sensorAlarmTimeOut)
        else:
            if self.handleSpeed is not None:
                self.windspeed_signal.disconnect()
                self.handleSpeed = None
                self.timerSpeed.stop()

        if self.windDir_enable:
            self.handleDir = self.winddir_signal.connect(self.slot_wind_dir)
            self.timerDir.start(self.sensorAlarmTimeOut)
        else:
            if self.handleDir is not None:
                self.winddir_signal.disconnect()
                self.handleDir = None
                self.timerDir.stop()
        if self.rain_enable:
            self.handleRain = self.rain_signal.connect(self.rain_info)
            self.timerRain.start(self.sensorAlarmTimeOut)
        else:
            if self.handleRain is not None:
                self.rain_signal.disconnect()
                self.handleRain = None
                self.timerRain.stop()
        self.rules['wind_dir_voltage_min'] = ConfigReader.config.conf['voltage_min_windDir']
        self.weatherBeep = ConfigReader.config.conf['weather_Beep']
        self.sensorAlarmTimeOut = ConfigReader.config.conf['SensorAlarmTimeout']
        self.weatherTimeOutOkDc = ConfigReader.config.conf['weather_TimeOut_OkDC']
        self.weatherTimeOutMarginalcond = ConfigReader.config.conf['weather_TimeOut_MarginalCond']
        self.weatherBeepNok = ConfigReader.config.conf['weather_beep_nok']
        self.weatherBeepOkDc = ConfigReader.config.conf['weather_beep_okDC']


    def __checkrules(self):
        #check voltage alarm
        if self.rules['sensor_voltage_alarm'] == alarm.Release and self.windDirVoltage <  self.rules['wind_dir_voltage_min']:
            self.rules['sensor_voltage_alarm'] = alarm.Alarm
            self.weather_lowVoltage_signal.emit()
            if self.__debug:
                print("Weather Sensor voltage alarm")
        if self.rules['sensor_voltage_alarm'] == alarm.Alarm and self.windDirVoltage > self.rules['wind_dir_voltage_min']+0.2:
            if self.__debug:
                print("Weather voltage alarm release")
            self.rules['sensor_voltage_alarm'] = alarm.Release
        #check rules speed, orientation, rain
        if (abs(self.weather['orientation']) > self.rules['dir_limit'] and self.windDir_isPresent or \
            ((self.weather['speed'] < self.rules['speed_limit_min'] or \
            self.weather['speed'] > self.rules['speed_limit_max']) and self.windSpeed_isPresent) \
            or self.weather['rain'] > 0.0 and self.rain_isPresent):
            self.slot_weatherNotCondition()
        else:
            self.slot_weatherCondition()

    def enable_rules(self, enable=True):
        self.__rules_enable = enable
        if self.__rules_enable:
            self.rules['wind_dir_voltage_alarm'] = alarm.Release
            self.rules['sensor_voltage_alarm'] = alarm.Release
            self.rules['sensor_lost_alarm'] = alarm.Release
            #self.rules['state'] = weatherState.init
        else:
            self.beep_signal.emit("stop", -1, 1000)
        
    def refresh_gui(self):
        self.gui_weather_signal.emit(self.weather['speed'], self.weather['unit'], self.weather['orientation'],
                                     self.weather['rain'], self.rules['state'] == weatherState.condNok or \
                                     self.rules['state'] == weatherState.condMarginal, self.status)
        self.gui_wind_speed_dir_signal.emit(self.weather['speed'], self.weather['unit'], self.windSpeed_isPresent,
                                            self.weather['orientation'], self.windDirVoltage,
                                            self.rules['wind_dir_voltage_alarm'] == alarm.Alarm,
                                            self.windDir_isPresent, int(self.weather['rain']), self.rain_isPresent)

    def slot_wind_speed(self, speed, unit):
        self.weather['speed'] = speed
        self.weather['unit'] = unit
        self.windSpeed_isPresent = True
        self.timerSpeed.stop()
        self.timerSpeed.start(self.sensorAlarmTimeOut)
        self.__checkrules()
        if self.inRun:
            self.weather['speed_nb'] += 1
            self.weather['speed_sum'] += speed

            if speed < self.weather['speed_min'] or self.weather['speed_min'] == -1:
                self.weather['speed_min'] = speed
            if speed > self.weather['speed_max'] or self.weather['speed_max'] == -1:
                self.weather['speed_max'] = speed

    def slot_wind_dir(self, orientation, voltage):
        self.weather['orientation'] = orientation
        self.windDirVoltage = voltage
        self.windDir_isPresent = True
        self.timerDir.stop()
        self.__checkrules()
        if self.inRun:
            self.weather['orientation_sum'] += orientation
            self.weather['orientation_nb'] += 1
        self.timerDir.start(self.sensorAlarmTimeOut)

    def setWeatherSound(self, enable=True):
        self.weatherSound = enable

    def setInRun(self, inRun):
        if inRun:
            self.inRun = True
            self.weather['speed_sum'] = 0.0
            self.weather['speed_nb'] = 0.0
            self.weather['speed_min'] = -1.0
            self.weather['speed_max'] = -1.0
            self.weather['orientation_sum'] = 0.0
            self.weather['orientation_nb'] = 0.0
            self.enable_rules(self.__rules_enable)
            self.rules['MCInRun'] = (self.rules['state'] == weatherState.condMarginal)
            if self.__debug:
                print("Wind InRun")
        else:
            self.inRun = False
            if self.__debug:
                print("Wind not InRun")

    def getMaxWindSpeed(self):
        return self.weather['speed_max']

    def getMinWindSpeed(self):
        return self.weather['speed_min']

    def getMeanWindSpeed(self):
        if (self.weather['speed_nb'] != 0):
            return self.weather['speed_sum'] / self.weather['speed_nb']
        else:
            return 0

    def getWindDir(self):
        if (self.weather['orientation_nb'] != 0):
            return self.weather['orientation_sum'] / self.weather['orientation_nb']
        else:
            return 0

    def rain_info(self, rain):
        if rain:
            self.weather['rain'] = 1.0
        else:
            self.weather['rain'] = 0.0
        self.__checkrules()
        self.timerRain.stop()
        self.timerRain.start(self.sensorAlarmTimeOut)
        self.rain_isPresent = True

    def getRain(self):
        return self.rain

    def set_rules_limit(self, speed_min, speed_max, dir):
        self.rules['speed_limit_min'] = speed_min
        self.rules['speed_limit_max'] = speed_max
        self.rules['dir_limit'] = dir

    def set_minVoltageWindDir(self, min):
        self.rules['wind_dir_voltage_min'] = min

    def reset_weather(self, first=False):
        if first:
            self.weather['speed'] = -1.0
            self.weather['unit'] = "m/s"
            self.weather['orientation'] = -1.0
            self.status = "Init"

        self.weather['speed_sum'] = 0.0
        self.weather['speed_nb'] = 0.0
        self.weather['speed_min'] = -1.0
        self.weather['speed_max'] = -1.0
        self.weather['orientation_sum'] = 0.0
        self.weather['orientation_nb'] = 0.0
        self.weather['rain'] = 0.0
        self.inRun = False


    def timeoutDir(self):
        if self.__debug:
            print("weather timeout orientation")
        self.weather['orientation'] = -1.0
        self.timerDir.stop()
        if self.__rules_enable and (
                self.windDir_isPresent and self.windDir_enable or not self.windDir_enable) and \
                (self.rain_isPresent and self.rain_enable or not self.rain_enable) and \
                (self.windSpeed_isPresent and self.windSpeed_enable or not self.windSpeed_enable):
            self.weather_sensor_lost.emit()
        self.windDir_isPresent=False

    def timeoutSpeed(self):
        if self.__debug:
            print("weather timeout speed")
        self.weather['speed'] = -1.0
        self.timerSpeed.stop()
        if self.__rules_enable and (
                self.windDir_isPresent and self.windDir_enable or not self.windDir_enable) and \
                (self.rain_isPresent and self.rain_enable or not self.rain_enable) and \
                (self.windSpeed_isPresent and self.windSpeed_enable or not self.windSpeed_enable):
            self.weather_sensor_lost.emit()
        self.windSpeed_isPresent=False

    def timeoutRain(self):
        if self.__debug:
            print("weather timeout rain")
        self.weather['rain'] = -1.0
        self.timerRain.stop()
        if self.__rules_enable and (
                self.windDir_isPresent and self.windDir_enable or not self.windDir_enable) and \
                (self.rain_isPresent and self.rain_enable or not self.rain_enable) and \
                (self.windSpeed_isPresent and self.windSpeed_enable or not self.windSpeed_enable):
            self.weather_sensor_lost.emit()
        self.rain_isPresent = False

    def slot_okDC(self):
        if self.__debug:
            print("slot_okDC")
        self.timerOkDC.stop()
        self.rules['state'] = weatherState.Nominal
        self.status = "OKDC"
        if self.__rules_enable:
            if self.weatherBeep:
                self.beep_signal.emit("blink", 5, self.weatherBeepOkDc)
            if self.weatherSound or self.chronostatus == Chrono.chronoStatus.InWait \
                    or self.chronostatus == Chrono.chronoStatus.Finished:
                self.vocal.append("windok")
                #self.weather_sound_signal.emit("windok")

    def slot_weatherNotCondition(self):
        if self.__debug:
            print("slot weather Not Condition, state : " + str(self.rules['state']))
        self.timerOkDC.stop()

        if self.rules['state'] != weatherState.condNok and self.rules['state'] != weatherState.condMarginal and\
                self.rules['state'] != weatherState.Stabilizing:
            self.status = "NOK"
            if self.__rules_enable:
                if self.weatherBeep:
                    self.beep_signal.emit("blink", 2, self.weatherBeepNok)
                if self.weatherSound or self.chronostatus == Chrono.chronoStatus.InWait \
                    or self.chronostatus == Chrono.chronoStatus.Finished:
                    self.vocal.append("windalert")
                    #self.weather_sound_signal.emit("windalert")

        if self.rules['state'] == weatherState.init or self.rules['state'] == weatherState.Nominal:
            self.timerMarginal.start(self.weatherTimeOutMarginalcond)
            self.rules['state'] = weatherState.condNok
        elif self.rules['state'] == weatherState.Stabilizing:
            self.slot_Marginal()

    def slot_Marginal(self):
        if self.__debug:
            print("slot_marginal")
        self.timerMarginal.stop()
        self.rules['state'] = weatherState.condMarginal
        self.status = "MC"
        if self.inRun:
            self.rules['MCInRun'] = True
        if self.__rules_enable:
            if self.weatherBeep:
                self.beep_signal.emit("permanent", -1, 1000)
            if self.weatherSound or self.chronostatus == Chrono.chronoStatus.InWait \
                    or self.chronostatus == Chrono.chronoStatus.Finished:
                self.vocal.append("windmarginal")
                #self.weather_sound_signal.emit("windmarginal")

    def slot_weatherCondition(self):
        if self.__debug:
            print("slot weather Condition, state : " + str(self.rules['state']))
        self.timerMarginal.stop()

        if self.rules['state'] == weatherState.init or self.rules['state'] == weatherState.condNok:
            self.rules['state'] = weatherState.Nominal
            self.status = "OKDC"
            if self.__rules_enable:
                if self.weatherSound or self.chronostatus == Chrono.chronoStatus.InWait \
                    or self.chronostatus == Chrono.chronoStatus.Finished:
                    self.vocal.append("windok")
                    #self.weather_sound_signal.emit("windok")
        elif self.rules['state'] == weatherState.condMarginal:
            self.timerOkDC.start(self.weatherTimeOutOkDc)
            self.rules['state'] = weatherState.Stabilizing
            self.beep_signal.emit("stop", 0, 0)
            self.status = "STAB"

    def slot_chronostatus (self, status):
        self.chronostatus = status

    def getMCinRun(self):
        return (self.rules['MCInRun'])

    def getVocalSignal(self):
        return self.vocal.sound_signal


class weatherVocal(QTimer):
    sound_signal = pyqtSignal(str)

    def __init__(self, timeout):
        super().__init__()
        self.__debug = False
        self.timems = timeout
        self.timeout.connect(self.process)
        self.list = []

    def process(self):
        if self.__debug:
            print ('weathervocal len(list) : '+str(len(self.list)))
        if len(self.list)!=0:
            if self.__debug:
                print('weathervocal last msg : ' + self.list[-1])
            self.sound_signal.emit(self.list[-1])
            self.list.clear()
        else:
            self.stop()

    def append(self, msg):
        if self.isActive():
            if self.__debug:
                print('weathervocal timer actif, append : ' + msg)
            self.list.append(msg)
        else:
            if self.__debug:
                print('weathervocal timer inactif, play : ' + msg)
            self.sound_signal.emit(msg)
            #self.singleShot(self.timems, self.process)
            self.start(self.timems)
