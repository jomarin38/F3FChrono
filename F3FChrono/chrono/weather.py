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



class Weather(QTimer):
    windspeed_signal = pyqtSignal(float, str)
    winddir_signal = pyqtSignal(float)
    rain_signal = pyqtSignal(bool)
    # gui_weather_signal parameters wind_speed, wind_speed_unit,  wind_dir, rain, alarm
    gui_weather_signal = pyqtSignal(float, str, float, bool, bool)
    beep_signal = pyqtSignal(str, int, int)

    def __init__(self):
        super().__init__()
        self.windspeed_signal.connect(self.slot_wind_speed)
        self.winddir_signal.connect(self.slot_wind_dir)
        self.rain_signal.connect(self.rain_info)
        self.wind = collections.OrderedDict()
        self.rules = collections.OrderedDict()
        self.reset_wind()
        self.__debug = False
        self.rules['starttime'] = time.time()
        self.rules['endtime'] = time.time()
        self.rules['detected'] = False
        self.rules['alarm'] = False
        self.rules['ok_dc'] = False
        self.rules['beep_state'] = ""
        self.rules['speed_limit_min'] = -1.0
        self.rules['speed_limit_max'] = -1.0
        self.rules['dir_limit'] = -1.0
        self.__rules_enable = False
        self.timeout.connect(self.refresh_gui)
        self.start(1000)

    def __checkrules(self):
        if self.__rules_enable and self.rules['speed_limit_min'] is not -1.0 and \
                self.rules['speed_limit_max'] is not -1.0 and \
                self.rules['dir_limit'] is not -1.0:
            if self.__debug:
                print("checkrules")
            if abs(self.wind['orientation']) > self.rules['dir_limit'] or \
                    self.wind['speed'] < self.rules['speed_limit_min'] or \
                    self.wind['speed'] > self.rules['speed_limit_max'] or self.rain:
                if not self.rules['detected']:
                    self.rules['starttime'] = time.time()
                    self.rules['detected'] = True
                    self.rules['alarm'] = False
                    self.rules['ok_dc'] = False
                else:
                    self.rules['endtime'] = time.time()
                    if (time.time() - self.rules['starttime']) > 20:
                        self.rules['alarm'] = True
                        if self.rules['beep_state'] is not "alarm":
                            self.beep_signal.emit("permanent", -1, 1000)
                            self.rules['beep_state'] = "alarm_wait"
                            if self.__debug:
                                print("weather alarm")
                    else:
                        self.beep_signal.emit("blink", 1, 500)
                        if self.__debug:
                            print("weather not condition")
            else:
                if (time.time() - self.rules['endtime']) > 20 and not self.rules['ok_dc']:
                    if self.rules['beep_state'] is not "ok_dc":
                        self.beep_signal.emit("blink", 5, 250)
                        self.rules['beep_state'] = "ok_dc"
                        self.rules['ok_dc'] = True
                        if self.__debug:
                            print("weather ok for DC")
                else:
                    self.rules['detected'] = False
                    self.rules['alarm'] = False
                    if self.rules['beep_state'] is not "stop":
                        self.beep_signal.emit("stop", -1, 1000)
                        self.rules['beep_state'] = "stop"
                        if self.__debug:
                            print("stop beep")
                            
    def enable_rules(self, enable=False):
        self.__rules_enable = enable
        self.rules['starttime'] = time.time()
        self.rules['endtime'] = time.time()
        self.rules['detected'] = False
        self.rules['alarm'] = False
        self.rules['ok_dc'] = False
        self.rules['beep_state'] = ""
        if not self.__rules_enable:
            self.beep_signal.emit("stop", -1, 1000)
            self.rules['beep_state'] = "stop"
        
    def refresh_gui(self):
        self.gui_weather_signal.emit(self.wind['speed'], self.wind['unit'], self.wind['orientation'],
                                     self.rain, self.rules['alarm'])

    def slot_wind_speed(self, speed, unit):
        self.wind['speed'] = speed
        self.wind['unit'] = unit
        if self.inRun:
            self.wind['speed_nb'] += 1
            self.wind['speed_sum'] += speed

            if speed < self.wind['speed_min'] or self.wind['speed_min'] == -1:
                self.wind['speed_min'] = speed
            if speed > self.wind['speed_max'] or self.wind['speed_max'] == -1:
                self.wind['speed_max'] = speed

        self.__checkrules()

    def slot_wind_dir(self, orientation):
        self.wind['orientation'] = orientation
        if self.inRun:
            self.wind['orientation_sum'] += orientation
            self.wind['orientation_nb'] += 1

    def setInRun(self, inRun):
        if inRun:
            self.inRun = True
            self.wind['speed_sum'] = 0.0
            self.wind['speed_nb'] = 0.0
            self.wind['speed_min'] = -1.0
            self.wind['speed_max'] = -1.0
            self.wind['orientation_sum'] = 0.0
            self.wind['orientation_nb'] = 0.0
            if self.__debug:
                print("Wind InRun")
        else:
            self.inRun = False
            if self.__debug:
                print("Wind not InRun")

    def getMaxWindSpeed(self):
        return self.wind['speed_max']

    def getMinWindSpeed(self):
        return self.wind['speed_min']

    def getMeanWindSpeed(self):
        if (self.wind['speed_nb'] != 0):
            return self.wind['speed_sum'] / self.wind['speed_nb']
        else:
            return 0

    def getWindDir(self):
        if (self.wind['orientation_nb'] != 0):
            return self.wind['orientation_sum'] / self.wind['orientation_nb']
        else:
            return 0

    def rain_info(self, rain):
        self.rain = (rain == True)

    def getRain(self):
        return self.rain

    def set_rules_limit(self, speed_min, speed_max, dir):
        self.rules['speed_limit_min'] = speed_min
        self.rules['speed_limit_max'] = speed_max
        self.rules['dir_limit'] = dir

    def reset_wind(self):
        self.wind['speed'] = -1.0
        self.wind['unit'] = "m/s"
        self.wind['speed_sum'] = 0.0
        self.wind['speed_nb'] = 0.0
        self.wind['speed_min'] = -1.0
        self.wind['speed_max'] = -1.0
        self.wind['orientation'] = -1.0
        self.wind['orientation_sum'] = 0.0
        self.wind['orientation_nb'] = 0.0
        self.rain = False
        self.inRun = False

