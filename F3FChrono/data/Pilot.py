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

class Pilot:

    def __init__(self, name, first_name, pilot_id=None, f3x_vault_id=None, fai_id=None, national_id=None):
        self.id = pilot_id
        self.name = name
        self.first_name = first_name
        self.fai_id = fai_id
        self.national_ID = national_id
        self.f3x_vault_id = f3x_vault_id

    def get_f3x_vault_id(self):
        return self.f3x_vault_id

    def get_id(self):
        return self.id

    def to_string(self):
        return self.name + ' ' + self.first_name
