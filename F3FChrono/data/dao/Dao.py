import pymysql
import threading


class Dao:

    _db = pymysql.connect("localhost", "f3f_ctrl", "F3FCtrl", "f3f_chrono")
    _lock = threading.Lock()

    def __init__(self):
        Dao._lock.acquire()
        self._cursor = Dao._db.cursor()
        Dao._lock.release()

    def _execute_query(self, sql, *args):
        Dao._lock.acquire()
        self._cursor.execute(sql, args)
        result = self._cursor.fetchall()
        Dao._db.commit()
        Dao._lock.release()
        return result

    def _execute_insert(self, sql, *args):
        Dao._lock.acquire()
        self._cursor.execute(sql, args)
        Dao._lock.release()
        Dao._db.commit()

    def _execute_update(self, sql, *args):
        Dao._lock.acquire()
        self._cursor.execute(sql, args)
        Dao._db.commit()
        Dao._lock.release()

    def _execute_delete(self, sql, *args):
        Dao._lock.acquire()
        self._cursor.execute(sql, args)
        Dao._db.commit()
        Dao._lock.release()
