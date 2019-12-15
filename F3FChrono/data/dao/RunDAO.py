from F3FChrono.data.dao.Dao import Dao
from F3FChrono.data.dao.CompetitorDAO import CompetitorDAO
from F3FChrono.data.Run import Run
from F3FChrono.data.Competitor import Competitor
from F3FChrono.data.Pilot import Pilot
from F3FChrono.data.RoundGroup import RoundGroup
from F3FChrono.data.Round import Round
from F3FChrono.data.Chrono import Chrono


class RunDAO(Dao):

    def get_list(self, round_group):
        sql = 'SELECT r.run_id, c.pilot_id, c.bib_number, c.team, p.name, p.first_name FROM run r ' \
              'LEFT JOIN competitor c ON r.competitor_id=c.pilot_id AND r.event_id=c.event_id ' \
              'LEFT JOIN pilot p ON c.pilot_id=p.pilot_id ' \
              'WHERE r.event_id=%s AND r.round_number=%s AND r.group_number=%s ORDER BY c.bib_number'
        query_result = self._execute_query(sql, round_group.round.event.id, round_group.round.round_number,
                                           round_group.group_number)
        result = []
        for row in query_result:
            f3f_run = Run()
            f3f_run.round_group = round_group
            pilot = Pilot(row[4], row[5], pilot_id=row[1])
            f3f_run.competitor = Competitor.register_pilot(round_group.round.event, row[2], pilot, row[3])
            f3f_run.id = row[0]
            result.append(f3f_run)
        return result

    def get_chrono_list(self, event_id):
        sql = 'SELECT chrono_id, start_date, run_time FROM chrono ' \
              'ORDER BY start_date DESC'
        query_result = self._execute_query(sql)
        result = []
        for row in query_result:
            chrono = Chrono()
            chrono.id = row[0]
            chrono.start_time = row[1]
            chrono.run_time = row[2]
            result.append(chrono)
        return result

    def get(self, run_id, round_group):
        sql = 'SELECT r.run_id, c.pilot_id, c.bib_number, c.team, p.name, p.first_name, ' \
              'r.penalty, r.round_number, r.group_number, r.event_id, ' \
              'r.valid, r.reason, ' \
              'ch.run_time, ch.min_wind_speed, ch.max_wind_speed, ch.wind_direction, ch.start_date, ch.end_date, ' \
              'ch.lap1, ch.lap2, ch.lap3, ch.lap4, ch.lap5, ch.lap6, ch.lap7, ch.lap8, ch.lap9, ch.lap10, ' \
              'ch.chrono_id ' \
              'FROM run r ' \
              'LEFT JOIN competitor c ON r.competitor_id=c.pilot_id AND r.event_id=c.event_id ' \
              'LEFT JOIN pilot p ON c.pilot_id=p.pilot_id ' \
              'LEFT JOIN chrono ch ON r.chrono_id=ch.chrono_id ' \
              'WHERE r.run_id=%s AND r.event_id=%s AND r.round_number=%s AND r.group_number=%s '
        query_result = self._execute_query(sql, run_id, round_group.round.event.id, round_group.round.round_number,
                                           round_group.group_number)
        f3f_run = Run()
        f3f_run.id = run_id
        for row in query_result:
            f3f_run.penalty = row[6]
            f3f_run.round_group = round_group
            f3f_round = Round()
            pilot = Pilot(row[4], row[5], pilot_id=row[1])
            f3f_run.competitor = Competitor.register_pilot(round_group.round.event, row[2], pilot, row[3])
            f3f_run.valid = row[10]
            f3f_run.penalty = row[6]
            f3f_run.reason = row[11]

            chrono = Chrono()
            chrono.run_time = row[12]
            chrono.min_wind_speed = row[13]
            chrono.max_wind_speed = row[14]
            chrono.wind_direction = row[15]
            chrono.start_time = row[16]
            chrono.end_time = row[17]
            for i in range(18, 28):
                chrono.add_lap_time(row[i])
            chrono.id = row[28]

            f3f_run.chrono = chrono

        return f3f_run

    def insert(self, run):
        chrono = run.chrono
        if chrono is not None:
            sql = 'INSERT INTO chrono (run_time, min_wind_speed, max_wind_speed, wind_direction, start_date, end_date, ' \
                  'lap1, lap2, lap3, lap4, lap5, lap6, lap7, lap8, lap9, lap10) ' \
                  'VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
            if chrono.start_time is not None:
                start_time = chrono.start_time.strftime('%Y-%m-%d %H:%M:%S')
            else:
                start_time = None
            if chrono.end_time is not None:
                end_time = chrono.end_time.strftime('%Y-%m-%d %H:%M:%S')
            else:
                end_time = None
            self._execute_insert(sql, chrono.run_time, chrono.min_wind_speed, chrono.max_wind_speed,
                                 chrono.wind_direction, start_time, end_time, chrono.get_lap_time(0),
                                 chrono.get_lap_time(1), chrono.get_lap_time(2), chrono.get_lap_time(3),
                                 chrono.get_lap_time(4), chrono.get_lap_time(5), chrono.get_lap_time(6),
                                 chrono.get_lap_time(7), chrono.get_lap_time(8), chrono.get_lap_time(9))

            sql = 'SELECT LAST_INSERT_ID()'
            query_result = self._execute_query(sql)
            for row in query_result:
                chrono_id = row[0]
        else:
            chrono_id = None

        sql = 'INSERT INTO run (competitor_id, chrono_id, penalty, valid, reason, round_number, group_number, ' \
              'event_id) ' \
              'VALUES (%s, %s, %s, %s, %s, %s, %s, %s)'
        if run.competitor.pilot.id is None:
            run.competitor = CompetitorDAO().get(run.round_group.round.event, run.competitor.bib_number)
        self._execute_insert(sql, run.competitor.pilot.id, chrono_id, run.penalty, run.valid, run.reason,
                             run.round_group.round.round_number, run.round_group.group_number,
                             run.round_group.round.event.id)

    def update(self, run):
        sql = 'UPDATE run SET competitor_id=%s, event_id=%, chrono_id=%, penalty=%, valid=%, round_number=%, ' \
              'group_number=% ' \
              'WHERE run_id=%'
        self._execute_update(sql, run.competitor.pilot.id, run.round_group.round.event.id, run.chrono.id, run.penalty,
                             run.valid, run.round_group.round.round_number, run.round_group.group_number)

    def delete(self, run):
        sql = 'DELETE FROM run WHERE run_id=%s'
        self._execute_delete(sql, run.id)
