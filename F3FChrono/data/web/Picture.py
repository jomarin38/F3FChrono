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
import os.path
import base64

class Picture:
    def __init__(self, file=None):
        self.file = file

    def is_present(self):
        if self.file is not None:
            return os.path.isfile(self.file)

    def to_html(self):
        image_data = base64.b64encode(open(self.file, 'rb').read()).decode('utf-8')
        res = ('<tr>' + '<td><img src="data:image/png;base64,{0}" width="400" height="195"></img></td></tr>'
               .format(image_data))
        return res
