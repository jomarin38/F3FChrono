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

class Cell:

    def __init__(self, value, joker=False, winner=False, css_id=None):
        self.value = value
        self.joker = joker
        self.winner = winner
        self.css_id = css_id
        if winner:
            self.css_id = 'win'
        if joker:
            self.css_id = 'joker'

    def to_html(self):
        res = self.value
        if self.joker:
            res = '<strike>' + res + '</strike>'
        if self.winner:
            res = '<strong>' + res + '</strong>'
        return res
