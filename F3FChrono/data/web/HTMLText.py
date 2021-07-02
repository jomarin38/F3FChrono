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

class HTMLText:

    def __init__(self, text=None, css_id=None):
        self.text = text
        self.header = None
        self.lines = []
        self.css_id = css_id

    def set_title(self, title):
        self.text = title

    def set_header(self, header):
        self.header = header

    def add_line(self, line):
        self.lines.append(line)

    def to_html(self):
        res = '<p '
        if self.css_id is not None:
            res += 'id=\"' + self.css_id + '\"'
        res += '>' + self.text + '</p>'
        return res
