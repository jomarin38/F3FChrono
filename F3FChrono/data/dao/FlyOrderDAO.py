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

from F3FChrono.data.dao.Dao import Dao
from F3FChrono.data.dao.RunDAO import RunDAO


class FlyOrderDAO(Dao):

    def get_order(self, event, round_number):
        sql = 'SELECT flight_order FROM imposed_fly_order WHERE event_id=%s AND round_number=%s'
        query_result = self._execute_query(sql, event.id, round_number)
        fly_order = None
        for row in query_result: #should return only one result
            fly_order = list(map(int,row[0].strip('\'').split(',')))
        return fly_order

    def get_groups(self, event, round_number):
        sql = 'SELECT groups FROM imposed_fly_order WHERE event_id=%s AND round_number=%s'
        query_result = self._execute_query(sql, event.id, round_number)
        groups = None
        for row in query_result: #should return only one result
            groups = list(map(int,row[0].strip('\'').split(',')))
        return groups

    def set_order(self, event, round_number, fly_order, groups):
        sql = 'INSERT INTO imposed_fly_order (event_id, round_number, flight_order, groups) ' \
              'VALUES (%s, %s, %s, %s)'
        self._execute_insert(sql, event.id, round_number, ','.join(map(str,fly_order)), ','.join(map(str,groups)))

    def delete_round(self, event, round_number):
        #Delete is intentionally not using group_id to directly delete all cancelled groups
        sql = 'DELETE FROM imposed_fly_order WHERE event_id=%s AND round_number=%s'
        self._execute_delete(sql, event.id, round_number)

    def delete(self, event):
        #Delete is intentionally not using group_id to directly delete all cancelled groups
        sql = 'DELETE FROM imposed_fly_order WHERE event_id=%s'
        self._execute_delete(sql, event.id)
