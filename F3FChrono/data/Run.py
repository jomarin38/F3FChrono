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

class Run:

    def __init__(self):
        self.id = None
        self.chrono = None
        self.penalty = 0.0
        self.round_group = None
        self.competitor = None
        self.valid = False
        self.reason = ""
        self.score = None

    def to_string(self):
        return self.competitor.display_name() + '\t:\t' + self.value_as_string()

    def value_as_string(self):
        res = self.chrono.run_time_as_string()
        if self.penalty > 0.0:
            res += '\tP\t' + str(self.penalty)
        return res

    def score_as_string(self):
        return '{:04.2f}'.format(self.score)

    def get_flight_time(self):
        return self.chrono.run_time
