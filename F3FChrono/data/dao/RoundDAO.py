from F3FChrono.data.dao.Dao import Dao
from F3FChrono.data.dao.RunDAO import RunDAO
from F3FChrono.data.Round import RoundGroup


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

    def get(self, f3f_round, fetch_runs=False):
        from F3FChrono.data.Round import Round
        sql = 'SELECT r.valid, rg.group_number, rg.start_date, rg.end_date ' \
              'FROM round r LEFT JOIN roundgroup rg ON r.event_id=rg.event_id AND r.round_number=rg.round_number ' \
              'WHERE r.event_id=%s AND r.round_number=%s'
        query_result = self._execute_query(sql, f3f_round.event.id, f3f_round.round_number)
        fetched_f3f_round = Round.new_round(f3f_round.event, add_initial_group=False)
        fetched_f3f_round.event = f3f_round.event
        fetched_f3f_round.round_number = f3f_round.round_number
        for row in query_result:
            fetched_f3f_round.valid = row[0]
            round_group = RoundGroup(fetched_f3f_round, group_number=row[1])
            round_group.start_time = row[2]
            round_group.end_time = row[3]
            fetched_f3f_round.add_group(round_group)
            if fetch_runs:
                RoundDAO._fetch_runs(round_group)
            if fetched_f3f_round.valid:
                fetched_f3f_round.validate_round(insert_database=False)
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

    def insert(self, f3f_round):
        sql = 'INSERT INTO round (round_number, event_id, valid) VALUES (%s, %s, %s)'
        self._execute_insert(sql, f3f_round.round_number, f3f_round.event.id, f3f_round.valid)
        sql = 'INSERT INTO roundgroup (event_id, round_number, group_number, start_date, end_date) ' \
              'VALUES (%s, %s, %s, %s, %s)'
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
                                 start_time, end_time)
            for competitor, runs in group.runs.items():
                for run in runs:
                    RoundDAO.run_dao.insert(run)

    def update(self, f3f_round):
        sql = 'UPDATE round SET valid=%s WHERE round_number=%s AND event_id=%s'
        self._execute_update(sql, f3f_round.valid, f3f_round.round_number, f3f_round.event.id)
        sql = 'UPDATE roundgroup SET start_date=%s, end_date=%s ' \
              'WHERE event_id=%s AND round_number=%s AND group_number=%s'
        for group in f3f_round.groups:
            self._execute_update(sql, group.start_time, group.end_time,
                                 f3f_round.event.id, f3f_round.round_number, group.group_number)
            for competitor, runs in group.runs.items():
                for run in runs:
                    RoundDAO.run_dao.update(run)

    def delete(self, f3f_round):
        sql = 'DELETE FROM roundgroup WHERE event_id=%s AND round_number=%s AND group_number=%s'
        for group in f3f_round.groups:
            for competitor, runs in group.runs.items():
                for run in runs:
                    RoundDAO.run_dao.delete(run)
            self._execute_delete(sql, f3f_round.event.id, f3f_round.round_number, group.group_number)
        sql = 'DELETE FROM round WHERE event_id=%s AND round_number=%s'
        self._execute_delete(sql, f3f_round.event.id, f3f_round.round_number)
