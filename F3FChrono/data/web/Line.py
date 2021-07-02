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

class Line:

    def __init__(self, name=None):
        self.name = name
        self.values = []
        self.tag = 'td'

    def set_name(self, name):
        self.name = name

    def add_cell(self, cell):
        self.values.append(cell)

    def start_tag(self, css_id=None):
        if css_id is None:
            return '<'+self.tag+'>'
        else:
            return '<' + self.tag + ' id=\"'+css_id+'\">'

    def end_tag(self):
        return '</'+self.tag+'>'

    def to_html(self):
        res = '<tr>'
        res += self.start_tag() + self.name.to_html() + self.end_tag()
        for cell in self.values:
            res += self.start_tag(cell.css_id) + cell.to_html() + self.end_tag()
        res += '</tr>'
        return res
