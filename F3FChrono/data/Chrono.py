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

import os

class Chrono:

    def __init__(self):
        self.id = None
        self.run_time = None
        self.min_wind_speed = None
        self.max_wind_speed = None
        self.mean_wind_speed = None
        self.wind_direction = None
        self.start_time = None
        self.end_time = None
        self.climbout_time = None
        self._lap_times = []

    def get_lap_time(self, i):
        if i < len(self._lap_times):
            return self._lap_times[i]
        else:
            return None

    def add_lap_time(self, lap_time):
        self._lap_times.append(lap_time)

    def reset(self):
        self.id = None
        self.run_time = None
        self.min_wind_speed = None
        self.max_wind_speed = None
        self.mean_wind_speed = None
        self.wind_direction = None
        self.start_time = None
        self.end_time = None
        self.climbout_time = None
        self._lap_times.clear()

    def to_string(self):
        result=''
        if (self.run_time!=None):
            result = os.linesep + "Chrono Data : " + os.linesep +\
                     "\tStart Time : " + str(self.start_time) + os.linesep +\
                     "\tEnd Time : " + str(self.end_time) + os.linesep +\
                     "\tWindMin : "+str(self.min_wind_speed)+", WindMax : "+str(self.max_wind_speed)+\
                     ", WindMean : "+str(self.mean_wind_speed)+", WindDir : "+str(self.wind_direction)+os.linesep+\
                     "\tClimout Time : "+str(self.climbout_time)+os.linesep+\
                     "\tRun Time : " + self.run_time_as_string() + os.linesep + "\tLapTime : "
            for lap in self._lap_times:
                if lap!=None:
                    result += "{:0>6.3f}".format(lap) + ","
            result += os.linesep
        return result

    def run_time_as_string(self):
        return "{:6.2f}".format(self.run_time)
