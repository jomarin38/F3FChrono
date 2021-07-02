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

from F3FChrono.data.web.ResultTable import ResultTable
from F3FChrono.data.web.Header import Header
from F3FChrono.data.web.Link import Link
from F3FChrono.data.web.Utils import Utils


class PageHeader:

    def __init__(self, event=None, f3f_round=None, authenticated=False):

        self._base_url = Utils.get_base_url()

        self._table = ResultTable(title='', css_id='header')
        header = Header(name=Link('Back to events list', self._base_url))
        if event is not None:
            header.add_cell(Link('Back to event view', self._base_url + '/event_view?event_id=' + str(event.id)))
        if authenticated:
            header.add_cell(Link('Log out', Utils.get_logout_url()))
        self._table.set_header(header)

    def to_html(self):
        return self._table.to_html()
