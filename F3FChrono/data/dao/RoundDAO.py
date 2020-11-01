from F3FChrono.data.dao.Dao import Dao
from F3FChrono.data.dao.RunDAO import RunDAO


class RoundDAO(Dao):

    run_dao = RunDAO()

    def get_list(self, event):
        from F3FChrono.data.Round import Round
        sql = 'SELECT round_number FROM round WHERE event_id=%s'
        query_result = self._execute_query(sql, event.id)
        result = []
        for row in query_result:
            f3f_round = Round()
            f3f_round.event = event
            f3f_round.round_number = row[0]
            result.append(f3f_round)
        return result

    def get(self, f3f_round, fetch_runs=False, fetch_cancelled_groups=False):
        from F3FChrono.data.Round import Round
        from F3FChrono.data.Round import RoundGroup
        sql = 'SELECT r.valid, rg.group_number, rg.start_date, rg.end_date, rg.flight_order, ' \
              'r.current_group, rg.valid, rg.cancelled, rg.group_id ' \
              'FROM round r LEFT JOIN roundgroup rg ON r.event_id=rg.event_id AND r.round_number=rg.round_number ' \
              'WHERE r.event_id=%s AND r.round_number=%s'
        if not fetch_cancelled_groups:
            sql += ' AND rg.cancelled=0'
        query_result = self._execute_query(sql, f3f_round.event.id, f3f_round.round_number)
        fetched_f3f_round = Round.new_round(f3f_round.event, add_initial_group=False)
        fetched_f3f_round.event = f3f_round.event
        fetched_f3f_round.round_number = f3f_round.round_number
        first_time_in_loop = True
        for row in query_result:
            if first_time_in_loop:
                fetched_f3f_round.valid = row[0]
                fetched_f3f_round.set_current_group_index(row[5])
            round_group = RoundGroup(fetched_f3f_round, group_number=row[1])
            round_group.start_time = row[2]
            round_group.end_time = row[3]
            if row[4] is not None:
                round_group.set_flight_order_from_db(row[4])
            else:
                round_group.set_flight_order([])
            round_group.valid = row[6]
            round_group.cancelled = row[7]
            round_group.group_id = row[8]
            fetched_f3f_round.add_group(round_group)
            if fetch_runs:
                RoundDAO._fetch_runs(round_group)
            if first_time_in_loop:
                if fetched_f3f_round.valid:
                    fetched_f3f_round.validate_round(insert_database=False)
                first_time_in_loop = False
        return fetched_f3f_round

    def get_from_ids(self, event_id, round_number, fetch_runs=False):
        from F3FChrono.data.dao.EventDAO import EventDAO
        from F3FChrono.data.Round import Round
        event = EventDAO().get(event_id, fetch_competitors=fetch_runs)
        f3f_round = Round()
        f3f_round.event = event
        f3f_round.round_number = round_number
        return self.get(f3f_round, fetch_runs)

    @staticmethod
    def _fetch_runs(round_group):
        dao = RunDAO()
        runs = dao.get_list(round_group)
        for run in runs:
            fetched_run = dao.get(run.id, run.round_group)
            round_group.add_run(fetched_run)
        #Warning : will not work if different groups are present ... maybe
        if len(runs)>0:
            round_group.set_flight_order_index(len(runs)-1)
        else:
            round_group.set_flight_order_index(0)

    def insert(self, f3f_round):
        sql = 'INSERT INTO round (round_number, event_id, valid, flight_order, current_group) ' \
              'VALUES (%s, %s, %s, %s, %s)'
        self._execute_insert(sql, f3f_round.round_number, f3f_round.event.id, f3f_round.valid,
                             f3f_round.get_serialized_flight_order(), f3f_round.get_current_group_index())
        sql = 'INSERT INTO roundgroup ' \
              '(event_id, round_number, group_number, start_date, end_date, flight_order, valid, cancelled) ' \
              'VALUES (%s, %s, %s, %s, %s, %s, %s, %s)'
        for group in f3f_round.groups:
            if group.start_time is not None:
                start_time = group.start_time.strftime('%Y-%m-%d %H:%M:%S')
            else:
                start_time = None
            if group.end_time is not None:
                end_time = group.end_time.strftime('%Y-%m-%d %H:%M:%S')
            else:
                end_time = None
            self._execute_insert(sql, f3f_round.event.id, f3f_round.round_number, group.group_number,
                                 start_time, end_time, group.get_serialized_flight_order(), group.valid,
                                 group.cancelled)
            for competitor, runs in group.runs.items():
                for run in runs:
                    RoundDAO.run_dao.insert(run)

    def add_group(self, group):
        sql = 'INSERT INTO roundgroup ' \
              '(event_id, round_number, group_number, start_date, end_date, flight_order, valid, cancelled) ' \
              'VALUES (%s, %s, %s, %s, %s, %s, %s, %s)'
        if group.start_time is not None:
            start_time = group.start_time.strftime('%Y-%m-%d %H:%M:%S')
        else:
            start_time = None
        if group.end_time is not None:
            end_time = group.end_time.strftime('%Y-%m-%d %H:%M:%S')
        else:
            end_time = None
        self._execute_insert(sql, group.round.event.id, group.round.round_number, group.group_number,
                             start_time, end_time, group.get_serialized_flight_order(), group.valid,
                             group.cancelled)

    def get_not_cancelled_group_id(self, event_id, round_number, group_number):
        from F3FChrono.data.Round import Round
        from F3FChrono.data.Round import RoundGroup
        sql = 'SELECT rg.group_id FROM roundgroup rg ' \
              'WHERE rg.event_id=%s AND rg.round_number=%s AND rg.group_number=%s'
        query_result = self._execute_query(sql, event_id, round_number, group_number)
        for row in query_result:
            return row[0]

    def update(self, f3f_round):
        sql = 'UPDATE round SET valid=%s, flight_order=%s, current_group=%s WHERE round_number=%s AND event_id=%s'
        self._execute_update(sql, f3f_round.valid, f3f_round.get_serialized_flight_order(),
                             f3f_round.get_current_group_index(), f3f_round.round_number, f3f_round.event.id)
        sql = 'UPDATE roundgroup SET start_date=%s, end_date=%s, flight_order=%s, valid=%s, cancelled=%s ' \
              'WHERE group_id=%s'
        for group in f3f_round.groups:
            self._execute_update(sql, group.start_time, group.end_time, group.get_serialized_flight_order(),
                                 group.valid, group.cancelled, group.group_id)
            for competitor, runs in group.runs.items():
                for run in runs:
                    RoundDAO.run_dao.update(run)

    def delete(self, f3f_round):
        #Delete is intentionally not using group_id to directly delete all cancelled groups
        sql = 'DELETE FROM roundgroup WHERE event_id=%s AND round_number=%s AND group_number=%s'
        for group in f3f_round.groups:
            for competitor, runs in group.runs.items():
                for run in runs:
                    RoundDAO.run_dao.delete(run)
            self._execute_delete(sql, f3f_round.event.id, f3f_round.round_number, group.group_number)
        sql = 'DELETE FROM round WHERE event_id=%s AND round_number=%s'
        self._execute_delete(sql, f3f_round.event.id, f3f_round.round_number)
