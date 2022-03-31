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
from F3FChrono.data.Competitor import Competitor
from F3FChrono.data.Pilot import Pilot


class CompetitorDAO(Dao):

    def get_list(self, event):
        sql = 'SELECT c.pilot_id, c.bib_number, c.team, p.name, p.first_name, c.present, ' \
              'p.f3x_vault_id ,p.fai_id ,p.national_id ' \
              'FROM competitor c ' \
              'LEFT JOIN pilot p ON c.pilot_id=p.pilot_id ' \
              'WHERE event_id=%s'
        query_result = self._execute_query(sql, event.id)
        result = {}
        for row in query_result:
            bib_number = row[1]
            team = row[2]
            pilot = Pilot(row[3], row[4], pilot_id=row[0],
                          f3x_vault_id=row[6], fai_id=row[7], national_id=row[8])
            present = bool(row[5])
            result[bib_number] = Competitor.register_pilot(event, bib_number, pilot, team, present)
        return result

    def get(self, event, bib_number):
        sql = 'SELECT c.pilot_id, c.bib_number, c.team, c.present, ' \
              'p.name, p.first_name, p.fai_id, p.national_id, p.f3x_vault_id ' \
              'FROM competitor c ' \
              'LEFT JOIN pilot p  ON c.pilot_id=p.pilot_id ' \
              'WHERE event_id=%s AND bib_number=%s'
        query_result = self._execute_query(sql, event.id, bib_number)
        result = None
        #Query should return only one row
        for row in query_result:
            pilot = Pilot(row[4], row[5], pilot_id=row[0], f3x_vault_id=row[8], fai_id=row[6], national_id=row[7])
            return Competitor.register_pilot(event, int(bib_number), pilot, row[2], bool(row[3]))
        return None

    def insert(self, competitor):
        pilot_id = self._insert_or_update_pilot(competitor.pilot)
        sql = 'INSERT INTO competitor (pilot_id, event_id, team, bib_number, present) VALUES (%s, %s, %s, %s, %s)'
        self._execute_insert(sql, pilot_id, competitor.event.id, competitor.team, competitor.bib_number,
                             competitor.present)

    def update(self, competitor):
        pilot_id = self._insert_or_update_pilot(competitor.pilot)
        sql = 'UPDATE competitor SET team=%s, bib_number=%s, present=%s WHERE pilot_id=%s AND event_id=%s'
        self._execute_update(sql, competitor.team, competitor.bib_number, competitor.present,
                             pilot_id, competitor.event.id)

    def delete(self, competitor):
        #Delete only competitor object, pilot is not deleted
        sql = 'DELETE FROM competitor WHERE pilot_id=%s AND event_id=%s'
        self._execute_delete(sql, competitor.pilot.id, competitor.event.id)

    def _insert_or_update_pilot(self, pilot):
        pilot_id = self._pilot_id_from_database(pilot)
        if pilot_id is not None:
            sql = 'UPDATE pilot SET name=%s, first_name=%s, fai_id=%s, national_id=%s, f3x_vault_id=%s ' \
                  'WHERE pilot_id=%s'
            self._execute_update(sql, pilot.name, pilot.first_name, pilot.fai_id, pilot.national_ID, pilot.f3x_vault_id,
                                 pilot_id)
        else:
            sql = 'INSERT INTO pilot (name, first_name, fai_id, national_id, f3x_vault_id) ' \
                  'VALUES (%s, %s, %s, %s, %s)'
            self._execute_insert(sql, pilot.name, pilot.first_name, pilot.fai_id, pilot.national_ID, pilot.f3x_vault_id)
        return self._pilot_id_from_database(pilot)

    def _pilot_id_from_database(self, pilot):
        sql = 'SELECT pilot_id FROM pilot ' \
              'WHERE (name=%s AND first_name=%s) ' \
              'OR (fai_id=%s AND fai_id<>NULL) ' \
              'OR (national_id=%s AND national_id<>NULL)'
        query_result = self._execute_query(sql, pilot.name, pilot.first_name, pilot.fai_id, pilot.national_ID)
        # Query should return only one row
        for row in query_result:
            return row[0]
        return None
