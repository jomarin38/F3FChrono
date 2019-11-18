from F3FChrono.data.dao.Dao import Dao
from F3FChrono.data.Event import Event

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

    def get(self, event_id):
        sql = 'SELECT event_id, begin_date, end_date, location, name, min_allowed_wind_speed, ' \
              'max_allowed_wind_speed, max_wind_dir_dev, max_interruption_time, f3x_vault_id ' \
              'FROM event WHERE event_id=%s'
        query_result = self._execute_query(sql, event_id)
        #Query should return only one row
        for row in query_result:
            result = Event()
            result.id = row[0]
            result.begin_date = row[1]
            result.end_date = row[2]
            result.location = row[3]
            result.name = row[4]
            result.min_allowed_wind_speed = row[5]
            result.max_allowed_wind_speed = row[6]
            result.max_wind_dir_dev = row[7]
            result.max_interruption_time = row[8]
            result.f3x_vault_id = row[9]
            return result
        return None

    def insert(self, event):
        """
        This function inserts only the event in event table. In normal mode runs should be inserted one by one
        :param event:
        :return:
        """
        sql = 'INSERT INTO event (begin_date, end_date, location, name, min_allowed_wind_speed, ' \
              'max_allowed_wind_speed, max_wind_dir_dev, max_interruption_time, f3x_vault_id) VALUES ' \
              '(%s, %s, %s, %s, %s, %s, %s, %s, %s)'

        self._execute_insert(sql, event.begin_date.strftime('%Y-%m-%d %H:%M:%S'),
                             event.end_date.strftime('%Y-%m-%d %H:%M:%S'), event.location, event.name,
                             event.min_allowed_wind_speed, event.max_allowed_wind_speed, event.max_wind_dir_dev,
                             event.max_interruption_time, event.f3x_vault_id)

    def update(self, event):
        sql = 'UPDATE event SET begin_date=%s, end_date=%s, location=%s, name=%s, ' \
              'min_allowed_wind_speed=%s, max_allowed_wind_speed=%s, max_wind_dir_dev=%s, max_interruption_time=%s, ' \
              'f3x_vault_id=%s WHERE event_id=%s'
        self._execute_update(sql, event.begin_date.strftime('%Y-%m-%d %H:%M:%S'),
                             event.end_date.strftime('%Y-%m-%d %H:%M:%S'), event.location, event.name,
                             event.min_allowed_wind_speed, event.max_allowed_wind_speed, event.max_wind_dir_dev,
                             event.max_interruption_time, event.f3x_vault_id, event.id)

    def delete(self, event):
        #TODO: delete all related stuff in other tables
        sql = 'DELETE FROM event WHERE event_id=%s'
        self._execute_delete(sql, event.id)

