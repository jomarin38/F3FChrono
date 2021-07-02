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

from F3FChrono.data.Event import Event
from F3FChrono.data.dao.EventDAO import EventDAO
from F3FChrono.data.dao.CompetitorDAO import CompetitorDAO
from F3FChrono.data.dao.RoundDAO import RoundDAO

login = input('F3X Vault login : ')
password = input('F3X Vault password : ')
contest_id = 1706

event = Event.from_f3x_vault(login, password, contest_id)

dao = EventDAO()

dao.insert(event)

event2 = dao.get_list()[-1]
event.id = event2.id

dao = CompetitorDAO()

for bib, competitor in event.get_competitors().items():
    dao.insert(competitor)

dao = RoundDAO()

for f3f_round in event.rounds:
    dao.insert(f3f_round)

print('Import finished')
