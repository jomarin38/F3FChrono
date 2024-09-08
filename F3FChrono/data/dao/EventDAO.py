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
from F3FChrono.data.Event import Event
from F3FChrono.data.dao.CompetitorDAO import CompetitorDAO
from F3FChrono.data.dao.RoundDAO import RoundDAO


class EventDAO(Dao):

    def get_list(self):
        sql = 'SELECT event_id, name FROM event'
        query_result = self._execute_query(sql)
        result = []
        for row in query_result:
            event = Event()
            event.id = row[0]
            event.name = row[1]
            result.append(event)
        return result

    def get(self, event_id, fetch_competitors=False, fetch_rounds=False,
            fetch_runs=False, fetch_runs_lastround=False):
        sql = 'SELECT event_id, begin_date, end_date, location, name, min_allowed_wind_speed, ' \
              'max_allowed_wind_speed, max_wind_dir_dev, max_interruption_time, bib_start, flights_before_refly, '\
                'dayduration, f3x_vault_id, groups_number FROM event WHERE event_id=%s'
        query_result = self._execute_query(sql, event_id)
        #Query should return only one row
        for row in query_result:
            result = Event()
            result.id = row[0]
            result.begin_date = row[1]
            result.end_date = row[2]
            result.location = row[3]
            result.name = row[4]
            result.min_allowed_wind_speed = int(row[5])
            result.max_allowed_wind_speed = int(row[6])
            result.max_wind_dir_dev = int(row[7])
            result.max_interruption_time = int(row[8])
            result.bib_start = row[9]
            result.flights_before_refly = row[10]
            result.dayduration = row[11]
            result.f3x_vault_id = row[12]
            result.groups_number = row[13]
            if fetch_competitors:
                EventDAO._fetch_competitors(result)
            if fetch_rounds:
                EventDAO._fetch_rounds(result, fetch_runs, fetch_runs_lastround)
            return result
        return None

    @staticmethod
    def _fetch_competitors(event):
        event.set_competitors(CompetitorDAO().get_list(event))

    @staticmethod
    def _fetch_rounds(event, fetch_runs, fetch_runs_lastround):
        dao = RoundDAO()
        rounds = dao.get_list(event)
        nb_rounds = len (rounds)
        for index, f3f_round in enumerate(rounds, 0):
            if fetch_runs and fetch_runs_lastround :
                local_fetch_run = (index==nb_rounds-1)
                fetched_round = dao.get(f3f_round, local_fetch_run)
            else:
                fetched_round = dao.get(f3f_round, fetch_runs)
            event.add_existing_round(fetched_round)
        round_numbers = [f3f_round.round_number for f3f_round in rounds]
        if len(round_numbers) < 1:
            event.create_new_round(insert_database=True)
        else:
            event.current_round = len(rounds)-1
            if (event.get_current_round().has_run()):
                #Switch to next Pilot
                event.get_current_round().next_pilot_database()


    def insert(self, event):
        """
        This function inserts only the event in event table. In normal mode runs should be inserted one by one
        :param event:
        :return:
        """
        sql = 'INSERT INTO event (begin_date, end_date, location, name, min_allowed_wind_speed, '\
                'max_allowed_wind_speed, max_wind_dir_dev, max_interruption_time, bib_start, flights_before_refly, '\
                'dayduration, f3x_vault_id, groups_number) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'

        self._execute_insert(sql, event.begin_date.strftime('%Y-%m-%d %H:%M:%S'),
                             event.end_date.strftime('%Y-%m-%d %H:%M:%S'), event.location, event.name,
                             event.min_allowed_wind_speed, event.max_allowed_wind_speed, event.max_wind_dir_dev,
                             event.max_interruption_time, event.bib_start, event.flights_before_refly,
                             event.dayduration, event.f3x_vault_id, event.groups_number)

        sql = 'SELECT LAST_INSERT_ID()'
        query_result = self._execute_query(sql)
        event_id = None
        for row in query_result:
            event_id = row[0]

        return event_id

    def update(self, event):
        sql = 'UPDATE event SET begin_date=%s, end_date=%s, location=%s, name=%s, ' \
              'min_allowed_wind_speed=%s, max_allowed_wind_speed=%s, max_wind_dir_dev=%s, max_interruption_time=%s, ' \
              'bib_start=%s, flights_before_refly=%s, dayduration=%s, f3x_vault_id=%s, groups_number=%  s ' \
              'WHERE event_id=%s'
        self._execute_update(sql, event.begin_date.strftime('%Y-%m-%d %H:%M:%S'),
                             event.end_date.strftime('%Y-%m-%d %H:%M:%S'), event.location, event.name,
                             event.min_allowed_wind_speed, event.max_allowed_wind_speed, event.max_wind_dir_dev,
                             event.max_interruption_time, event.bib_start, event.flights_before_refly,
                             event.dayduration, event.f3x_vault_id, event.groups_number, event.id)

    def delete(self, event):
        #Get chrono ids to be deleted later
        sql = 'SELECT chrono_id FROM f3f_chrono.run WHERE event_id=%s'
        query_result = self._execute_query(sql, event.id)

        sql = 'DELETE FROM f3f_chrono.run WHERE event_id=%s'
        self._execute_delete(sql, event.id)

        #Should be made in one request if speed optimisation is needed
        for row in query_result:
            sql = 'DELETE FROM f3f_chrono.chrono WHERE chrono_id=%s'
            self._execute_delete(sql, row[0])

        sql = 'DELETE FROM f3f_chrono.roundgroup WHERE event_id=%s'
        self._execute_delete(sql, event.id)

        sql = 'DELETE FROM f3f_chrono.round WHERE event_id=%s'
        self._execute_delete(sql, event.id)

        sql = 'DELETE FROM f3f_chrono.competitor WHERE event_id=%s'
        self._execute_delete(sql, event.id)

        sql = 'DELETE FROM f3f_chrono.imposed_fly_order WHERE event_id=%s'
        self._execute_delete(sql, event.id)

        sql = 'DELETE FROM event WHERE event_id=%s'
        self._execute_delete(sql, event.id)
