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

import pymysql
import threading
import os
from F3FChrono.chrono import ConfigReader


class Dao:
    _db = pymysql.connect(host=os.getenv('MYSQL_IP', 'localhost'),
                              user="f3f_ctrl",
                              password="F3FCtrl",
                              db="f3f_chrono")
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
