import pymysql


class Dao:

    _db = pymysql.connect("localhost", "f3f_ctrl", "F3FCtrl", "f3f_chrono_sdaviet")

    def __init__(self):
        self._cursor = Dao._db.cursor()

    def _execute_query(self, sql, *args):
        self._cursor.execute(sql, args)
        result = self._cursor.fetchall()
        Dao._db.commit()
        return result

    def _execute_insert(self, sql, *args):
        self._cursor.execute(sql, args)
        Dao._db.commit()

    def _execute_update(self, sql, *args):
        self._cursor.execute(sql, args)
        Dao._db.commit()

    def _execute_delete(self, sql, *args):
        self._cursor.execute(sql, args)
        Dao._db.commit()
